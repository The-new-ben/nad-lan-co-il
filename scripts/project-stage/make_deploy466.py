# -*- coding: utf-8 -*-
"""make deploy466.py from deploy465.py: Ashira's how-to film (2 new files) + the ashira_466 hunk on the live inc/project-stage.php
(restored from .bak466 on rollback), and one page check that the film card is in the side rail."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["assets/project-stage/ashira/howto-he.jpg", "assets/project-stage/ashira/howto-he.mp4"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy465.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(FILES) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = []"): lines[i] = 'PHP_RELS = ["inc/project-stage.php"]  # 1.72.466: the ashira_466 hunk, restored from .bak466 on rollback'
src = "\n".join(lines)
for a, b in [("1.72.465", "1.72.466"), ("ps465", "ps466"), ("bak465", "bak466"), ("make_deploy465", "make_deploy466"),
             ("deploy-result-465", "deploy-result-466"), ("speed-465", "speed-466"), ("posts-before-465", "posts-before-466"),
             ("ashira_465", "ashira_466"), ("deploy-result-464", "deploy-result-465"), ("1.72.464", "1.72.465"),
             ("range(464, 329", "range(465, 329")]:
    src = src.replace(a, b)
anchor = "    ('/projects/ashira-sde-dov/?t357=1',"
assert src.count(anchor) == 1
src = src.replace(anchor, "    ('/projects/ashira-sde-dov/?t466=1', ['class=\"nlds nlps-howtowrap\"', 'class=\"nlps-howto__v\"', 'assets/project-stage/ashira/howto-he.mp4?ver=1.72.466', 'assets/project-stage/ashira/howto-he.jpg?ver=1.72.466', 'איך משתמשים באולם התצוגה'], []),\n" + anchor)
src = src.replace('print("RELEASE 1.72.466 LIVE: Ashira facility 360s replaced (checked against the developer renders)")',
                  'print("RELEASE 1.72.466 LIVE: Ashira how-to film under the broker slot in the side rail")')
open(os.path.join(H, "deploy466.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy466.py written;", PIN)
for i, l in enumerate(src.split("\n")):
    if re.search(r"(?<![0-9A-Za-z])46[45](?![0-9A-Za-z])", l) and not l.startswith(("PIN", "FILES")): print("  review", i + 1, l.strip()[:130])
