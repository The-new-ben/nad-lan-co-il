# -*- coding: utf-8 -*-
"""make deploy471.py from deploy470.py: the free walk (assets/walk/ashira/: the page, its thumbnail, its textures; all new)
and the ashira_471 hunk (the walk card over the films)."""
import hashlib, os
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config"); WD = os.path.join(PLUG, "assets", "walk", "ashira")
FILES = ["assets/walk/ashira/index.html", "assets/walk/ashira/thumb.jpg"] + sorted("assets/walk/ashira/tex/" + f for f in os.listdir(os.path.join(WD, "tex")))
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy470.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(FILES) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = 'PHP_RELS = ["inc/project-stage.php"]  # 1.72.471: the ashira_471 hunk, restored from .bak471'
src = "\n".join(lines)
for a, b in [("1.72.470", "1.72.471"), ("ps470", "ps471"), ("bak470", "bak471"), ("make_deploy470", "make_deploy471"),
             ("deploy-result-470", "deploy-result-471"), ("speed-470", "speed-471"), ("posts-before-470", "posts-before-471"),
             ("ashira_470", "ashira_471"), ("deploy-result-469", "deploy-result-470"), ("1.72.469", "1.72.470"),
             ("range(469, 329", "range(470, 329"), ("?t470d=1", "?t471d=1"), ("?t470c=1", "?t471c=1"), ("?t470b=1", "?t471b=1"), ("?t470=1", "?t471=1")]:
    src = src.replace(a, b)
old = "    ('/projects/ashira-sde-dov/?t471=1',"
assert src.count(old) == 1
src = src.replace(old, "    ('/projects/ashira-sde-dov/?t471w=1', ['data-nlps-walk', 'assets/walk/ashira/index.html?ver=1.72.471', 'assets/walk/ashira/thumb.jpg?ver=1.72.471', 'window.__nlpsWalk'], []),\n" + old)
src = src.replace('print("RELEASE 1.72.471 LIVE: Ashira film gallery (English, narrated): the showroom and the video call")', 'print("RELEASE 1.72.471 LIVE: Ashira free walk on the page (card over the films, full screen)")')
open(os.path.join(H, "deploy471.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy471.py written;", len(FILES), "files")
