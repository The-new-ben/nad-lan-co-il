# -*- coding: utf-8 -*-
"""Round N follow-up (HAD-675): the 49 map links were 40 px tall on phones (benchmark tap44_share 0.83 -> 0.73); make them 44 px.
One anchored replacement in the map CSS of page 121; nothing else changes. python fix_tap44_n.py [--dry]"""
import io, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "fx"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/121?context=edit&_fields=content,link"); assert s == 200, s
raw = r["content"]["raw"]; a = "min-height:40px;padding:6px 0;"; b = "min-height:44px;padding:6px 0;"
assert raw.count(a) == 1 and raw.count('id="nlmap-css"') == 1, raw.count(a)
new = raw.replace(a, b); print("bytes", len(raw), "->", len(new))
if "--dry" in sys.argv: sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-121-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/121", {"content": new}); assert s2 in (200, 201), s2
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("live has 44:", b in page, "| 40 gone:", a not in page)
