# -*- coding: utf-8 -*-
"""make deploy465.py from deploy464.py: the 21 Ashira facility files (modified, not new), re-pinned; no hunk (ashira_465)."""
import hashlib, os, re, shutil
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
GEN = os.path.join(REPO, "docs", "sales", "ashira-meeting-2026-10", "tour", "gen", "out")
FILES = []
for n in ["cinema", "club", "gym", "kids", "lobby", "pool", "spa"]:
    for s in ("-2k", "-card", ""):
        rel = f"assets/project-stage/ashira/tour/fac-{n}{s}.jpg"
        shutil.copyfile(os.path.join(GEN, f"fac-{n}{s}.jpg"), os.path.join(PLUG, *rel.split("/")))
        FILES.append(rel)
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy464.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set()"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
src = "\n".join(lines)
for a, b in [("1.72.464", "1.72.465"), ("ps464", "ps465"), ("bak464", "bak465"), ("gen_deploy464", "make_deploy465"),
             ("deploy-result-464", "deploy-result-465"), ("speed-464", "speed-465"), ("posts-before-464", "posts-before-465"),
             ("ashira_464", "ashira_465"), ("deploy-result-463", "deploy-result-464"), ("1.72.463", "1.72.464"),
             ("range(463, 329", "range(464, 329"), ('"1.72.464 writes no post', '"1.72.465 writes no post')]:
    src = src.replace(a, b)
src = src.replace('print("RELEASE 1.72.465 LIVE: Ashira 360 rooms and facilities on the page")',
                  'print("RELEASE 1.72.465 LIVE: Ashira facility 360s replaced (checked against the developer renders)")')
open(os.path.join(H, "deploy465.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy465.py written;", len(FILES), "files")
left = [(i + 1, l.strip()[:140]) for i, l in enumerate(src.split("\n")) if re.search(r"(?<![0-9A-Za-z])46[34](?![0-9A-Za-z])", l) and not l.startswith(("PIN", "FILES"))]
for x in left: print("  review", x)
