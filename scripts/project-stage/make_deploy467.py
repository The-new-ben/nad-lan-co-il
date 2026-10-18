# -*- coding: utf-8 -*-
"""make deploy467.py from deploy466.py: no files, only the ashira_467 hunk on the live inc/project-stage.php (restored from .bak467)."""
import os, re
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "deploy466.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = {}"
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set()"
    elif l.startswith("FILES = ["): lines[i] = "FILES = []"
    elif l.startswith("PHP_RELS = ["): lines[i] = 'PHP_RELS = ["inc/project-stage.php"]  # 1.72.467: the ashira_467 hunk, restored from .bak467 on rollback'
src = "\n".join(lines)
for a, b in [("1.72.466", "1.72.467"), ("ps466", "ps467"), ("bak466", "bak467"), ("make_deploy466", "make_deploy467"),
             ("deploy-result-466", "deploy-result-467"), ("speed-466", "speed-467"), ("posts-before-466", "posts-before-467"),
             ("ashira_466", "ashira_467"), ("deploy-result-465", "deploy-result-466"), ("1.72.465", "1.72.466"),
             ("range(465, 329", "range(466, 329"), ("?t466=1", "?t467=1")]:
    src = src.replace(a, b)
old = "    ('/projects/ashira-sde-dov/?t467=1', ['class=\"nlds nlps-howtowrap\"',"
assert src.count(old) == 1
src = src.replace(old, "    ('/projects/ashira-sde-dov/?t467b=1', ['class=\"nlds nlps-howtom\"', ':root body .nlps-howtom{display:none}'], []),\n" + old)
src = src.replace('print("RELEASE 1.72.467 LIVE: Ashira how-to film under the broker slot in the side rail")',
                  'print("RELEASE 1.72.467 LIVE: Ashira how-to film also under the stage on phones")')
open(os.path.join(H, "deploy467.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy467.py written")
