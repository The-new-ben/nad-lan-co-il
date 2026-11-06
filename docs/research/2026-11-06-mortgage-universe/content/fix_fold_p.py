# -*- coding: utf-8 -*-
"""Round P follow-up 3 (HAD-675): after the wrapper fix the phone fold also folded what-is-mortgage and mortgage-tracks (benchmark
words_rendered 5222 -> 4905). The definition of the head word stays open: both ids join the fold's skip list. One anchored edit."""
import io, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "fx"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/121?context=edit&_fields=content,link"); assert s == 200, s
raw = r["content"]["raw"]; a = '"faq":1,"mortgage-map":1};'; b = '"faq":1,"mortgage-map":1,"what-is-mortgage":1,"mortgage-tracks":1};'
assert raw.count(a) == 1, raw.count(a); new = raw.replace(a, b)
if "--dry" in sys.argv: print("ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-121-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/121", {"content": new}); assert s2 in (200, 201), s2
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("live:", b in page)
