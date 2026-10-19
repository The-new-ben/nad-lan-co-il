# -*- coding: utf-8 -*-
"""make deploy472.py from deploy471.py: the free walk (assets/walk/ashira/: the page, its thumbnail, its textures; all new)
and the ashira_472 hunk (the walk bar)."""
import hashlib, os
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config"); WD = os.path.join(PLUG, "assets", "walk", "ashira")
FILES = []
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy471.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set()"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = 'PHP_RELS = ["inc/project-stage.php"]  # 1.72.472: the ashira_472 hunk, restored from .bak472'
src = "\n".join(lines)
for a, b in [("1.72.471", "1.72.472"), ("ps471", "ps472"), ("bak471", "bak472"), ("make_deploy471", "make_deploy472"),
             ("deploy-result-471", "deploy-result-472"), ("speed-471", "speed-472"), ("posts-before-471", "posts-before-472"),
             ("ashira_471", "ashira_472"), ("deploy-result-470", "deploy-result-471"), ("1.72.470", "1.72.471"),
             ("range(470, 329", "range(471, 329"), ("?t471w=1", "?t472w=1"), ("?t471d=1", "?t472d=1"), ("?t471c=1", "?t472c=1"), ("?t471b=1", "?t472b=1"), ("?t471=1", "?t472=1")]:
    src = src.replace(a, b)
src = src.replace("'window.__nlpsWalk'], []),", "'window.__nlpsWalk', 'nlps-walkov__h'], []),")
assert "nlps-walkov__h" in src
src = src.replace('print("RELEASE 1.72.472 LIVE: Ashira free walk on the page (card over the films, full screen)")', 'print("RELEASE 1.72.472 LIVE: the walk full screen gets its top bar")')
open(os.path.join(H, "deploy472.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy472.py written;", len(FILES), "files")
