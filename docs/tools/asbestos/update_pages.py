# -*- coding: utf-8 -*-
"""HAD-668: update the live /asbestos/ or /en/asbestos/ content from page.html / page-en.html (the id from published-<lang>.json).
Backup of the live raw content first (docs/qa/asbestos/backup-<lang>-<time>.json), then the write, then a read of the rendered
page: one H1, the four tool hosts, the page CSS, the FAQPage. Any failed check restores the backup.
  python update_pages.py he|en [--undo <backup.json>]"""
import io
import json
import os
import re
import sys
import time
import urllib.request

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "asbupdate"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
LANG = sys.argv[1]
pid = json.load(io.open(os.path.join(H, f"published-{LANG}.json"), encoding="utf-8"))["id"]
QA = os.path.join(REPO, "docs", "qa", "asbestos")
if "--undo" in sys.argv:
    bk = json.load(io.open(sys.argv[sys.argv.index("--undo") + 1], encoding="utf-8"))
    print("[undo]", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": bk["raw"]})[0]); raise SystemExit(0)
html = io.open(os.path.join(H, "page.html" if LANG == "he" else "page-en.html"), encoding="utf-8").read()
meta = json.load(io.open(os.path.join(H, "meta.json" if LANG == "he" else "meta-en.json"), encoding="utf-8"))
bad = [w for w in meta.get("forbid", []) if w in html]
if bad:
    raise SystemExit(f"FATAL: forbidden text: {bad}")
s, cur, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=id,content,link")
if s != 200:
    raise SystemExit(f"FATAL read {s}")
if cur["content"]["raw"] == html:
    print("[same] nothing to write"); raise SystemExit(0)
bk = os.path.join(QA, f"backup-{LANG}-{time.strftime('%Y%m%d-%H%M%S')}.json")
json.dump({"id": pid, "raw": cur["content"]["raw"]}, io.open(bk, "w", encoding="utf-8"), ensure_ascii=False)
s, b, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": html})
print("[write]", s, "backup", bk)
time.sleep(4)
live = urllib.request.urlopen(urllib.request.Request(cur["link"] + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
body = live[live.find("<body"):]
checks = {"one h1": body.count("<h1") == 1, "hosts": all(f'data-nli="{t}"' in body for t in meta["tools"]), "css": 'id="nadlan-asb-css"' in live,
          "faq": '"FAQPage"' in live, "wrapped hotline": '<span dir="ltr">*6911</span>' in body}
for k, v in checks.items():
    print("  ", "OK " if v else "BAD", k)
if s != 200 or not all(checks.values()):
    print("[restore]", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": cur["content"]["raw"]})[0]); raise SystemExit(1)
print("[done]", cur["link"])
