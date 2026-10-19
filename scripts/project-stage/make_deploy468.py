# -*- coding: utf-8 -*-
"""make deploy468.py from deploy467.py: the 25 floor-25 living-room files (modified) + the ashira_468 hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config"); T = os.path.join(PLUG, "assets", "project-stage", "ashira", "tour")
FILES = sorted("assets/project-stage/ashira/tour/" + f for f in os.listdir(T) if f.startswith("living-25"))
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy467.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set()"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = 'PHP_RELS = ["inc/project-stage.php"]  # 1.72.468: the ashira_468 hunk, restored from .bak468 on rollback'
src = "\n".join(lines)
for a, b in [("1.72.467", "1.72.468"), ("ps467", "ps468"), ("bak467", "bak468"), ("make_deploy467", "make_deploy468"),
             ("deploy-result-467", "deploy-result-468"), ("speed-467", "speed-468"), ("posts-before-467", "posts-before-468"),
             ("ashira_467", "ashira_468"), ("deploy-result-466", "deploy-result-467"), ("1.72.466", "1.72.467"),
             ("range(466, 329", "range(467, 329"), ("?t467b=1", "?t468b=1"), ("?t467=1", "?t468=1")]:
    src = src.replace(a, b)
old = "    ('/projects/ashira-sde-dov/?t468b=1',"
assert src.count(old) == 1
src = src.replace(old, "    ('/projects/ashira-sde-dov/?t468c=1', ['לכיוון תל ברוך והרצליה', 'הנוף בחלון הוא הדמיה לפי הכיוון והגובה של הקומה'], ['לכיוון נמל תל אביב והירקון']),\n" + old)
src = src.replace('print("RELEASE 1.72.468 LIVE: Ashira how-to film also under the stage on phones")', 'print("RELEASE 1.72.468 LIVE: Ashira floor-25 living room in ChatGPT quality, directions fixed")')
open(os.path.join(H, "deploy468.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy468.py written;", len(FILES), "files")
