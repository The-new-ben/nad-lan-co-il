# -*- coding: utf-8 -*-
"""Ben 15.10.2026: NOTHING about the soil tests (PFAS, contamination) on any project page, in any language. The subject lives
on /sde-dov/contamination/ only. This removes every block (heading, paragraph, list item, table row) that mentions it from
the given nadlan_project posts, plus the paragraphs under a removed heading that continue the same topic, plus the empty
block wrappers. Backup before, read-back after, the live page checked: no mention left, one H1.
   python remove_soil_mentions.py <id> [<id> ...] [--dry]"""
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "soilclean"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
PAT = re.compile(r"PFAS|PFOS|PFOA|contaminat|pollut|загрязн|تلوث|ملوث|dépollu|זיהום|מזוהמ", re.I)
ENV = re.compile(r"environment|environnement|окружающ|экологи|البيئ|soil|\bsol\b|грунт|تربة|groundwater|eaux souterraines|мияе|المياه الجوفية", re.I)
BLK = re.compile(r"<(h[2-6]|p|li|tr|dt|dd|details|figcaption)\b[^>]*>.*?</\1>", re.S)
BK = os.path.join(REPO, "docs", "qa", "had-534", "page-backup")


def spans(raw):
    blocks = list(BLK.finditer(raw))
    cut = []
    for i, m in enumerate(blocks):
        if PAT.search(m.group(0)):
            cut.append((m.start(), m.end()))
            if m.group(1).startswith("h"):  # the section under a removed heading, while it stays on the topic
                for n in blocks[i + 1:]:
                    if n.group(1).startswith("h"):
                        break
                    if n.group(1) == "p" and (PAT.search(n.group(0)) or ENV.search(n.group(0))):
                        cut.append((n.start(), n.end()))
                    else:
                        break
    out = []
    for a, b in sorted(set(cut)):  # widen to the block wrapper comments
        pre = re.search(r"<!-- wp:[a-z/-]+(?: \{[^>]*\})? -->\s*$", raw[:a])
        post = re.match(r"\s*<!-- /wp:[a-z/-]+ -->", raw[b:])
        if pre and post:
            a, b = pre.start(), b + post.end()
        out.append((a, b))
    return out


def clean(raw):
    new, last, removed = [], 0, []
    for a, b in spans(raw):
        if a < last:
            continue
        new.append(raw[last:a]); removed.append(raw[a:b]); last = b
    new.append(raw[last:])
    s = "".join(new)
    s = re.sub(r"<(ul|ol)\b[^>]*>\s*</\1>", "", s)  # a list left empty
    s = re.sub(r"<!-- wp:list(?: \{[^>]*\})? -->\s*<!-- /wp:list -->", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s, removed


for pid in [int(x) for x in sys.argv[1:] if x.isdigit()]:
    s, b, _ = req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=content,link,meta,excerpt")
    raw, link = b["content"]["raw"], b["link"]
    new, removed = clean(raw)
    meta_hits = [k for k, v in (b.get("meta") or {}).items() if isinstance(v, str) and PAT.search(v)]
    print(f"=== {pid} {link}: {len(removed)} blocks, {len(raw) - len(new)} chars out, left in content: {len(PAT.findall(new))}, meta fields with a mention: {meta_hits}")
    for r in removed:
        print("   -", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r)).strip()[:110])
    if "--dry" in sys.argv:
        continue
    os.makedirs(BK, exist_ok=True)
    bk = os.path.join(BK, f"project-{pid}-{time.strftime('%Y%m%dT%H%M%S')}.json")
    json.dump({"id": pid, "link": link, "raw": raw}, io.open(bk, "w", encoding="utf-8"), ensure_ascii=False)
    s2, _, _ = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": new})
    if s2 not in (200, 201):
        raise SystemExit(f"FATAL update {pid}: {s2}")
    _, b3, _ = req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=content")
    assert b3["content"]["raw"] == new, f"read-back differs on {pid}"
    time.sleep(2)
    live = urllib.request.urlopen(urllib.request.Request(link + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", live[live.find("<body"):], flags=re.S)
    ok = {"no mention on the live page": not PAT.search(body), "one h1": body.count("<h1") == 1}
    print("   backup", os.path.basename(bk), "| read-back OK |", " ".join(("OK " if v else "BAD ") + k for k, v in ok.items()))
    if not all(ok.values()):
        print("   [restore]", req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": raw})[0]); raise SystemExit(1)
