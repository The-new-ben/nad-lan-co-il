# -*- coding: utf-8 -*-
"""HAD-460 alignment of /sde-dov/prices/ (page 4758) with the Sde Dov price list (price_guide/sde-dov-prices.json): the audit
(docs/qa/had-460/sde-dov-prices-audit.md) found 17 of the page's 21 price claims in conflict with dated sources or unsourced
(an average of 81,000 where every survey says ~83,000; a rooms table whose 3.81M is a Jerusalem project's average). The edits in
docs/content/sde-dov-prices-2026-10/align-edits.json replace each number with a sourced, dated one (align-check.md: 0 unsourced).
Rules: applied to the RAW content in order; each "old" must match exactly once (or exactly expect_matches times when replace_all);
the rooms table ("spans_tags") falls back to the <table> element that holds "<th>סוג דירה</th>". Any miss = nothing is written
(all or nothing). Backup before (content, title, Yoast meta), read-back after, the rendered page checked for the new figures.
App password in-process, never printed.   python apply_align_sdedov.py [--dry | --rollback <backup.json>]"""
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
EDITS = os.path.join(REPO, "docs", "content", "sde-dov-prices-2026-10", "align-edits.json")
BK = os.path.join(REPO, "docs", "qa", "had-460", "sde-dov-backup")
PID = 4758
ARGS = sys.argv[1:]
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "alignsd"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]


def get():
    s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{PID}?context=edit&_fields=id,link,title,content,meta,modified")
    if s != 200:
        raise SystemExit(f"FATAL read {PID}: {s}")
    return b


if "--rollback" in ARGS:
    bk = json.load(io.open(ARGS[ARGS.index("--rollback") + 1], encoding="utf-8"))
    s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{PID}", {"content": bk["content"]})
    print("[rollback]", s, "identical:", get()["content"]["raw"] == bk["content"])
    raise SystemExit(0)

edits = sorted(json.load(io.open(EDITS, encoding="utf-8"))["edits"], key=lambda e: e["n"])
b = get()
raw = b["content"]["raw"]
new, bad = raw, []
for e in edits:
    if e.get("field", "content") != "content":
        bad.append((e["n"], "field " + e.get("field", ""))); continue
    c = new.count(e["old"])
    if e.get("replace_all"):
        if c != int(e.get("expect_matches", 2)):
            bad.append((e["n"], c)); continue
        new = new.replace(e["old"], e["new"])
    elif c == 1:
        new = new.replace(e["old"], e["new"])
    elif c == 0 and e.get("spans_tags"):
        i = new.find("<th>סוג דירה</th>")
        a, z = new.rfind("<table", 0, i), new.find("</table>", i)
        if i < 0 or a < 0 or z < 0 or new.count("<th>סוג דירה</th>") != 1:
            bad.append((e["n"], "table not found")); continue
        new = new[:a] + e["new"] + new[z + len("</table>"):]
        print(f"   #{e['n']}: the rooms table replaced by its element (raw line breaks differ from the rendered text)")
    else:
        bad.append((e["n"], c))
print(f"[page {PID}] {b['link']}: {len(edits)} edits, {len(bad)} not matching {bad}; {len(raw):,} -> {len(new):,} chars")
if bad:
    raise SystemExit("nothing written (all or nothing)")
if "--dry" in ARGS:
    raise SystemExit(0)
os.makedirs(BK, exist_ok=True)
bkp = os.path.join(BK, f"page-{PID}-{time.strftime('%Y%m%dT%H%M%S')}.json")
meta = {k: (b.get("meta") or {}).get(k, "") for k in ("_yoast_wpseo_title", "_yoast_wpseo_metadesc")}
io.open(bkp, "w", encoding="utf-8").write(json.dumps({"id": PID, "link": b["link"], "content": raw, "title": b["title"]["raw"], "meta_yoast": meta,
                                                      "modified": b["modified"]}, ensure_ascii=False))
s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{PID}", {"content": new})
same = get()["content"]["raw"] == new
u = b["link"] + "?nlal=%d" % time.time()
h = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-align"}), timeout=90).read().decode("utf-8", "replace")
body = re.sub(r"<[^>]+>", " ", h[h.find("<body"):])
left = [x for x in ("סביב 81,000", "3.81 מיליון", "46.8 מ״ר", "43.75 מיליון", "11,000 יחידות") if x in body]
print(f"[write] {s}, read-back identical: {same}; old figures still visible: {left}; backup {os.path.relpath(bkp, REPO)}")
if s != 200 or not same or left:
    print("[rollback]", req("POST", f"/wp-json/wp/v2/pages/{PID}", {"content": raw})[0]); raise SystemExit(1)
