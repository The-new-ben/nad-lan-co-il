# -*- coding: utf-8 -*-
"""Owner order 24.9.2026: "Madlan" out of every visible text on nad-lan.co.il ("say official sources, sources on
the web"). Applies the reviewed rewrite map (146 content replacements, 13 meta values, 37 posts) through the
token-gated bridge, with a drift guard per post (the live text must be exactly what the map was written against),
a local backup of every value before it changes, a cache purge, and a public re-read that must show 0 mentions.

  python scripts/ops/apply_madlan.py MAP.json POSTS.json [--dry]
"""
import io, json, os, re, sys, time, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nlbridge import Bridge, backup, md5

MAP, POSTS = sys.argv[1], sys.argv[2]
DRY = "--dry" in sys.argv
m = json.load(open(MAP, encoding="utf-8"))
before = json.load(open(POSTS, encoding="utf-8"))
NEEDLE = re.compile(r"מדלן|madlan", re.I)

by_post = {}
for r in m["posts"]:
    by_post.setdefault(int(r["id"]), []).append(r)
ids = sorted(set(by_post) | {int(x["id"]) for x in m["meta"]})
print("posts with content edits:", len(by_post), "| meta edits:", len(m["meta"]), "| ids:", len(ids))

with Bridge("madlan") as b:
    live = b.ops({"get": {"ids": ids, "meta": sorted({x["key"] for x in m["meta"]})}})["get"]
    backup("madlan-live-before-apply", live)
    sets, skipped = [], []
    for pid, reps in by_post.items():
        cur = live[str(pid)]
        if cur["md5"] != before[str(pid)]["md5"]:
            skipped.append((pid, "content changed since the map was written"))
            continue
        fields = {"content": cur["content"], "title": cur["title"], "excerpt": cur["excerpt"]}
        ok = True
        for r in reps:
            f = r.get("field", "content")
            if fields[f].count(r["old"]) != 1:
                skipped.append((pid, "old string not unique/found: " + r["old"][:40]))
                ok = False
                break
            fields[f] = fields[f].replace(r["old"], r["new"])
        if not ok:
            continue
        left = sum(len(NEEDLE.findall(v)) for v in fields.values())
        if left:
            skipped.append((pid, f"{left} mentions would remain"))
            continue
        row = {"id": pid, "content": fields["content"], "expect": cur["md5"]}
        if fields["title"] != cur["title"]:
            row["title"] = fields["title"]
        if fields["excerpt"] != cur["excerpt"]:
            row["excerpt"] = fields["excerpt"]
        sets.append(row)
    metas = []
    for x in m["meta"]:
        cur = live[str(x["id"])]["meta"].get(x["key"], {})
        if cur.get("md5") != x["old_md5"]:
            skipped.append((x["id"], "meta changed: " + x["key"]))
            continue
        metas.append({"id": int(x["id"]), "key": x["key"], "value": x["new"], "expect": x["old_md5"]})
    print("ready: %d post updates, %d meta updates, %d skipped" % (len(sets), len(metas), len(skipped)))
    for s in skipped:
        print("  SKIP", s)
    if DRY:
        raise SystemExit(0)
    res = []
    for i in range(0, len(sets), 6):  # small batches: each save runs the site's save hooks
        res += b.ops({"set_post": sets[i:i + 6]}, timeout=300)["set_post"]
    bad = [r for r in res if r.get("err")]
    print("post saves:", len(res), "errors:", bad)
    mres = b.ops({"set_meta": metas})["set_meta"] if metas else []
    print("meta saves:", len(mres), "errors:", [r for r in mres if r.get("err")])
    print("purge:", b.ops({"purge": 1, "purge_ids": ids}).get("purged"))
    after = b.ops({"get": {"ids": ids, "meta": sorted({x["key"] for x in m["meta"]})}})["get"]
    backup("madlan-live-after-apply", after)

# public re-read: the rendered pages must not say Madlan anywhere in the body
time.sleep(3)
fails = 0
for pid in ids:
    link = after[str(pid)]["link"]
    status = after[str(pid)]["status"]
    if status != "publish":
        continue
    r = urllib.request.Request(link + ("&" if "?" in link else "?") + "nlm=" + str(int(time.time())), headers={"User-Agent": "Mozilla/5.0 Chrome/128"})
    html = urllib.request.urlopen(r, timeout=90).read().decode("utf-8", "replace")
    body = html.split("<body", 1)[-1]
    body = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", "", body, flags=re.S)
    n = len(NEEDLE.findall(re.sub(r"<[^>]+>", " ", body)))
    if n:
        fails += 1
        ctx = [body[max(0, mm.start() - 80): mm.end() + 60] for mm in NEEDLE.finditer(re.sub(r"<[^>]+>", " ", body))][:2]
        print(f"  STILL {n} in {pid} {link[:70]} | {ctx}")
print("pages still showing Madlan:", fails)
