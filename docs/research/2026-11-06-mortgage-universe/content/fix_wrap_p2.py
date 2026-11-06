# -*- coding: utf-8 -*-
"""Round P follow-up 2 (HAD-675): the table styles live under `.nadlan-guide .nlu1`, so the wrapper around what-is-mortgage and
mortgage-tracks becomes the same two-level wrapper the other chapters sit in. Two anchored edits. python fix_wrap_p2.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "fx"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/121?context=edit&_fields=content,link"); assert s == 200, s
raw = r["content"]["raw"]
OPEN = '<div class="nlu1" id="nlu1-what">'
assert raw.count(OPEN) == 1
i = raw.index('<section id="mortgage-tracks"'); depth = 0
for m in re.finditer(r'<section\b|</section>', raw[i:]):
    depth += 1 if m.group(0) == '<section' else -1
    if depth == 0:
        e = i + m.end(); break
assert raw[e:e + 7] == "\n</div>", repr(raw[e:e + 12])
new = raw[:e] + "\n</div></div>" + raw[e + 7:]
new = new.replace(OPEN, '<div class="nadlan-guide" id="nlu1-what"><div class="wrap nlu1">', 1)
print("bytes", len(raw), "->", len(new))
if "--dry" in sys.argv: sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-121-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/121", {"content": new}); assert s2 in (200, 201), s2
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("live:", 'class="nadlan-guide" id="nlu1-what"' in page)
