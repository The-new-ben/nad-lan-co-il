# -*- coding: utf-8 -*-
"""make deploy473.py from deploy472.py: the Kochav HaTzafon walk (assets/walk/kochav/: all new files), no code hunk."""
import hashlib, os
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config"); WD = os.path.join(PLUG, "assets", "walk", "kochav")
FILES = ["assets/walk/kochav/" + f for f in ("index.html", "thumb.jpg", "city.json", "places.json", "quarter.json")] + sorted("assets/walk/kochav/tex/" + f for f in os.listdir(os.path.join(WD, "tex")))
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy472.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(FILES) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.473: no hunk; the new files are unlinked on rollback"
src = "\n".join(lines)
for a, b in [("1.72.472", "1.72.473"), ("ps472", "ps473"), ("bak472", "bak473"), ("make_deploy472", "make_deploy473"),
             ("deploy-result-472", "deploy-result-473"), ("speed-472", "speed-473"), ("posts-before-472", "posts-before-473"),
             ("ashira_472", "ashira_473"), ("deploy-result-471", "deploy-result-472"), ("1.72.471", "1.72.472"),
             ("range(472, 329", "range(473, 329"), ("?t472w=1", "?t473w=1"), ("?t472d=1", "?t473d=1"), ("?t472c=1", "?t473c=1"), ("?t472b=1", "?t473b=1"), ("?t472=1", "?t473=1")]:
    src = src.replace(a, b)
old = "    ('/projects/ashira-sde-dov/?t473w=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/walk/kochav/index.html?t473k=1', ['כוכב הצפון והגשר', 'bridgePath', 'cineFrame', 'noindex'], []),\n" + old)
src = src.replace('print("RELEASE 1.72.473 LIVE: the walk full screen gets its top bar")', 'print("RELEASE 1.72.473 LIVE: the Kochav HaTzafon walk with the planned bridge (assets/walk/kochav)")')
open(os.path.join(H, "deploy473.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy473.py written;", len(FILES), "files")
