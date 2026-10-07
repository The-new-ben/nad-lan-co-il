# -*- coding: utf-8 -*-
"""HAD-460 alignment (Ben 7.10.2026: every new piece of content is checked against the related content and aligned): the pages
that placed Kikar HaMedina, Bavli or Miriam HaHashmonait in the Old North are corrected to the facts (Rova 4 = the New North;
docs/content/rova-4-2026-10/facts.md), with a link to the new page /north-tel-aviv/rova-4/.
Edits: docs/content/rova-4-2026-10/align-edits.json (each "old" matched once in the live page). They are applied to the RAW
content (context=edit); a page with any edit that does not match its raw text exactly once is skipped whole (all or nothing
per page). Every page is backed up before the write (content, title, Yoast meta) and read back after it.
App password in-process, never printed.   python apply_align_rova4.py [--dry | --rollback <backup.json>]"""
import io
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
EDITS = os.path.join(REPO, "docs", "content", "rova-4-2026-10", "align-edits.json")
BK = os.path.join(REPO, "docs", "qa", "had-460", "align-backup")
ARGS = sys.argv[1:]


def helpers():
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
    ns = {"__name__": "align"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
    return ns["req"]


req = helpers()


def get(pid):
    s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=id,link,title,content,meta,modified")
    if s != 200:
        raise SystemExit(f"FATAL read {pid}: {s}")
    return b


if "--rollback" in ARGS:
    bk = json.load(io.open(ARGS[ARGS.index("--rollback") + 1], encoding="utf-8"))
    s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{bk['id']}", {"content": bk["content"], "title": bk["title"], "meta": bk["meta_yoast"]})
    b = get(bk["id"])
    print("[rollback]", bk["id"], s, "identical:", b["content"]["raw"] == bk["content"] and b["title"]["raw"] == bk["title"])
    raise SystemExit(0)

data = json.load(io.open(EDITS, encoding="utf-8"))
by_page = {}
for e in data["edits"]:
    by_page.setdefault(int(e["page_id"]), []).append(e)
s, h, _ = req("GET", "/wp-json/wp/v2/pages?slug=rova-4&parent=4866&_fields=id,status")
if not (isinstance(h, list) and h and h[0]["status"] == "publish"):
    raise SystemExit("FATAL: /north-tel-aviv/rova-4/ is not published yet; the link edits must wait")
os.makedirs(BK, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
report = []
for pid, edits in sorted(by_page.items()):
    b = get(pid)
    raw, title = b["content"]["raw"], b["title"]["raw"]
    meta = {k: (b.get("meta") or {}).get(k, "") for k in ("_yoast_wpseo_title", "_yoast_wpseo_metadesc")}
    new_raw, new_title, new_meta, bad = raw, title, dict(meta), []
    for e in sorted(edits, key=lambda x: x["n"]):
        f = e.get("field", "content")
        if f == "content":
            c = new_raw.count(e["old"])
            if c != 1:
                bad.append((e["n"], c)); continue
            new_raw = new_raw.replace(e["old"], e["new"])
        elif f == "title":
            if new_title != e["old"]:
                bad.append((e["n"], "title")); continue
            new_title = e["new"]
        elif f == "yoast_title":
            if new_meta["_yoast_wpseo_title"]:  # an explicit Yoast title; an empty one follows the post title
                if e["old"] not in new_meta["_yoast_wpseo_title"]:
                    bad.append((e["n"], "yoast_title")); continue
                new_meta["_yoast_wpseo_title"] = new_meta["_yoast_wpseo_title"].replace(e["old"], e["new"])
        elif f == "yoast_description":
            if e["old"] not in new_meta["_yoast_wpseo_metadesc"]:
                bad.append((e["n"], "yoast_description")); continue
            new_meta["_yoast_wpseo_metadesc"] = new_meta["_yoast_wpseo_metadesc"].replace(e["old"], e["new"])
    print(f"[page {pid}] {b['link']}: {len(edits)} edits, {len(bad)} not matching the raw text {bad}")
    if bad:
        report.append({"id": pid, "skipped": True, "bad": bad}); continue
    if "--dry" in ARGS:
        report.append({"id": pid, "dry": True}); continue
    bkp = os.path.join(BK, f"page-{pid}-{stamp}.json")
    io.open(bkp, "w", encoding="utf-8").write(json.dumps({"id": pid, "link": b["link"], "content": raw, "title": title, "meta_yoast": meta,
                                                          "modified": b["modified"]}, ensure_ascii=False))
    payload = {"content": new_raw}
    if new_title != title:
        payload["title"] = new_title
    if new_meta != meta:
        payload["meta"] = {k: v for k, v in new_meta.items() if v != meta[k]}
    s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", payload)
    a = get(pid)
    ok = s == 200 and a["content"]["raw"] == new_raw and a["title"]["raw"] == new_title
    print(f"   written {s}, read-back identical: {ok}; backup {os.path.relpath(bkp, REPO)}")
    report.append({"id": pid, "ok": ok, "backup": os.path.relpath(bkp, REPO)})
    if not ok:
        raise SystemExit(f"FATAL: page {pid} did not read back; roll back with --rollback {bkp}")
io.open(os.path.join(BK, f"report-{stamp}.json"), "w", encoding="utf-8").write(json.dumps(report, ensure_ascii=False, indent=1))
print("[done]", report)
