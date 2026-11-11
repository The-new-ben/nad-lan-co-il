# -*- coding: utf-8 -*-
"""Read a Kikar post's LIVE raw text (context=edit) into a file. GET only.  python scripts/kikar/_read_post.py <id> <out>"""
import hashlib, io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "rd"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
pid = int(sys.argv[1])
s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % pid)
assert s == 200, s
raw = g["content"]["raw"]
io.open(sys.argv[2], "w", encoding="utf-8", newline="").write(raw)
print(g["slug"], g["modified"], len(raw), hashlib.md5(raw.encode("utf-8")).hexdigest())
