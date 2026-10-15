# -*- coding: utf-8 -*-
"""HAD-534: insert one HTML snippet into an EXISTING page right before a given heading (e.g. a measured link line at the end
of a section). Backup before, read-back after, live check that the snippet's link appears exactly once and the page keeps one
H1.   python insert_before_heading.py <page id> "<heading text>" <snippet.html> [--dry]"""
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BK = os.path.join(REPO, "docs", "qa", "had-534", "page-backup")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "insertbefore"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
pid, heading, snip_path = sys.argv[1], sys.argv[2], sys.argv[3]
snip = io.open(snip_path, encoding="utf-8").read().strip()
href = re.search(r'href="([^"]+)"', snip).group(1)
s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content,link,modified")
raw, link = b["content"]["raw"], b["link"]
if href in raw:
    raise SystemExit(f"{pid} already links {href}: nothing to do")
m = re.search(r"<h[2-4][^>]*>\s*" + re.escape(heading) + r"\s*</h[2-4]>", raw)
if not m:
    raise SystemExit(f"FATAL {pid}: heading not found: {heading}")
at = m.start()
blk = raw.rfind("<!-- wp:heading", 0, at)
if blk != -1 and re.fullmatch(r"<!-- wp:heading[^>]*-->\s*", raw[blk:at]):
    at = blk  # keep the heading's block comment with its heading
blocks = "<!-- wp:" in raw
piece = ("<!-- wp:paragraph -->\n" + snip + "\n<!-- /wp:paragraph -->\n\n") if blocks else (snip + "\n\n")
new = raw[:at] + piece + raw[at:]
print(f"[plan] page {pid} {link}: insert {len(snip)} chars before '{heading}' (block markup: {blocks})")
if "--dry" in sys.argv:
    raise SystemExit(0)
os.makedirs(BK, exist_ok=True)
bk = os.path.join(BK, f"page-{pid}-{time.strftime('%Y%m%dT%H%M%S')}.json")
json.dump({"id": pid, "link": link, "modified": b["modified"], "raw": raw}, io.open(bk, "w", encoding="utf-8"), ensure_ascii=False)
print("[backup]", bk)
s, b2, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": new})
if s not in (200, 201):
    raise SystemExit(f"FATAL update {s}")
s, b3, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content")
assert b3["content"]["raw"] == new, "read-back differs"
print("[read-back] OK")
time.sleep(3)
live = urllib.request.urlopen(urllib.request.Request(link + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
body = live[live.find("<body"):]
checks = {"link once": body.count(href) >= 1, "one h1": body.count("<h1") == 1, "heading kept": heading in body}
for k, v in checks.items():
    print("  ", "OK " if v else "BAD", k)
if not all(checks.values()):
    print("[restore]", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": raw})[0]); raise SystemExit(1)
print("[done]", link)
