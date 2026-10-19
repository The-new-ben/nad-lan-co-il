# -*- coding: utf-8 -*-
"""make deploy469.py from deploy468.py: Ashira's apartment rooms (empty base + furnished 'warm' style, floors 25 and 10, the
balconies) and the ashira_469 hunks (project-stage.php, tour.js, bridge.js; all restored from .bak469 on rollback)."""
import hashlib, json, os
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config"); T = os.path.join(PLUG, "assets", "project-stage", "ashira", "tour")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
known = set()
for n in (464, 468):
    known |= set((json.load(open(os.path.join(QA, f"deploy-result-{n}.json"), encoding="utf-8")).get("files") or {}).keys())
FILES = sorted("assets/project-stage/ashira/tour/" + f for f in os.listdir(T) if f.startswith(("living-25", "living-10", "balcony-25w", "balcony-10w")))
NEWF = sorted(r for r in FILES if r not in known)
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy468.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEWF) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = 'PHP_RELS = ["inc/project-stage.php", "assets/project-stage/tour.js", "assets/project-stage/bridge.js"]  # 1.72.469 hunks, restored from .bak469'
src = "\n".join(lines)
for a, b in [("1.72.468", "1.72.469"), ("ps468", "ps469"), ("bak468", "bak469"), ("make_deploy468", "make_deploy469"),
             ("deploy-result-468", "deploy-result-469"), ("speed-468", "speed-469"), ("posts-before-468", "posts-before-469"),
             ("ashira_468", "ashira_469"), ("deploy-result-467", "deploy-result-468"), ("1.72.467", "1.72.468"),
             ("range(467, 329", "range(468, 329"), ("?t468c=1", "?t469c=1"), ("?t468b=1", "?t469b=1"), ("?t468=1", "?t469=1")]:
    src = src.replace(a, b)
old = "    ('/projects/ashira-sde-dov/?t469c=1',"
assert src.count(old) == 1
src = src.replace(old, "    ('/projects/ashira-sde-dov/?t469d=1', ['data-nlps-tour-style=\"warm\"', 'living-25n-warm.jpg', 'balcony-25w-warm.jpg', '-bare-thumb.jpg'], []),\n" + old)
src = src.replace('print("RELEASE 1.72.469 LIVE: Ashira floor-25 living room in ChatGPT quality, directions fixed")', 'print("RELEASE 1.72.469 LIVE: Ashira rooms with and without furniture, every direction, floors 25 and 10")')
open(os.path.join(H, "deploy469.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy469.py written;", len(FILES), "files,", len(NEWF), "new")
