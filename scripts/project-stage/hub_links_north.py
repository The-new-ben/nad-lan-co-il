# -*- coding: utf-8 -*-
"""HAD-460 alignment: the North Tel Aviv hub (/north-tel-aviv/, page 4866) never linked to its own neighbourhood guides. One
paragraph at the end of its section "מהו צפון תל אביב והשכונות" links down to them, Rova 4 included (the hub owns the area, each
guide owns its neighbourhood: no new heading, no repeated title). Backup before, read-back after.
python hub_links_north.py [--dry | --rollback <backup.json>]"""
import io
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BK = os.path.join(REPO, "docs", "qa", "had-460", "align-backup")
PID = 4866
MARK = "nl-hub-guides"
PARA = ('<p class="' + MARK + '">המדריכים לשכונות של צפון תל אביב: '
        '<a href="https://nad-lan.co.il/north-tel-aviv/old-north/">הצפון הישן</a> (רובע 3, ממערב לאבן גבירול), '
        '<a href="https://nad-lan.co.il/north-tel-aviv/rova-4/">רובע 4</a> (הצפון החדש וכיכר המדינה), '
        '<a href="https://nad-lan.co.il/north-tel-aviv/bavli/">שכונת בבלי</a>, '
        '<a href="https://nad-lan.co.il/north-tel-aviv/miriam-hahashmonait/">מרים החשמונאית</a> '
        'ו<a href="https://nad-lan.co.il/north-tel-aviv/shchunat-lamed/">שכונת ל׳</a>.</p>\n')
ARGS = sys.argv[1:]
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "hub"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{PID}?context=edit&_fields=id,link,content,modified")
raw = b["content"]["raw"]
if "--rollback" in ARGS:
    bk = json.load(io.open(ARGS[ARGS.index("--rollback") + 1], encoding="utf-8"))
    s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{PID}", {"content": bk["content"]})
    print("[rollback]", s); raise SystemExit(0)
if MARK in raw:
    raise SystemExit("already applied")
m = list(re.finditer(r"<h2[^>]*>\s*אופי האזור ואיכות החיים\s*</h2>", raw))
if len(m) != 1:
    raise SystemExit("FATAL: the anchor heading was found %d times in the raw content" % len(m))
new = raw[:m[0].start()] + PARA + raw[m[0].start():]
print("[plan] insert", len(PARA), "chars before the heading at", m[0].start())
if "--dry" in ARGS:
    raise SystemExit(0)
os.makedirs(BK, exist_ok=True)
bkp = os.path.join(BK, f"page-{PID}-{time.strftime('%Y%m%dT%H%M%S')}.json")
io.open(bkp, "w", encoding="utf-8").write(json.dumps({"id": PID, "content": raw, "modified": b["modified"]}, ensure_ascii=False))
s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{PID}", {"content": new})
s2, a, _ = req("GET", f"/wp-json/wp/v2/pages/{PID}?context=edit&_fields=content")
print("[write]", s, "read-back identical:", a["content"]["raw"] == new, "| backup", os.path.relpath(bkp, REPO))
