# -*- coding: utf-8 -*-
"""Round P follow-up (HAD-675): the chapters what-is-mortgage and mortgage-tracks sit after the switcher, outside the page's
`.nlu1` wrapper, so their tables fell back to the theme's default (cream header). Wrap the two sections in <div class="nlu1">.
Two anchored inserts; nothing else. python fix_wrap_p.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "fx"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/121?context=edit&_fields=content,link"); assert s == 200, s
raw = r["content"]["raw"]
assert raw.count('<section id="what-is-mortgage">') == 1 and raw.count('<section id="mortgage-tracks">') == 1
assert '<div class="nlu1" id="nlu1-what">' not in raw
def sec_end(txt, sid):
    i = txt.index('<section id="%s"' % sid); depth = 0
    for m in re.finditer(r'<section\b|</section>', txt[i:]):
        depth += 1 if m.group(0) == '<section' else -1
        if depth == 0:
            return i + m.end()
a = raw.index('<section id="what-is-mortgage">'); e = sec_end(raw, "mortgage-tracks")
assert a < e
new = raw[:a] + '<div class="nlu1" id="nlu1-what">\n' + raw[a:e] + '\n</div>' + raw[e:]
print("bytes", len(raw), "->", len(new))
if "--dry" in sys.argv: sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-121-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/121", {"content": new}); assert s2 in (200, 201), s2
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("live wrapper:", 'id="nlu1-what"' in page)
