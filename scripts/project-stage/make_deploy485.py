# -*- coding: utf-8 -*-
"""make deploy485.py from deploy484.py: the Kochav building in 3D (walk index.html replaced; building.json + bldg.jpg new)."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
NEWF = ["assets/walk/kochav/building.json", "assets/walk/kochav/bldg.jpg"]
FILES = ["assets/walk/kochav/index.html"] + NEWF
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy484.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEWF) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.485: no hunk; index.html comes back from .bak, the new files are unlinked on rollback"
src = "\n".join(lines)
for a, b in [("1.72.484", "1.72.485"), ("ps484", "ps485"), ("bak484", "bak485"), ("make_deploy484", "make_deploy485"),
             ("deploy-result-484", "deploy-result-485"), ("speed-484", "speed-485"), ("posts-before-484", "posts-before-485"),
             ("ashira_484", "ashira_485"), ("deploy-result-483", "deploy-result-484"), ("1.72.483", "1.72.484")]:
    src = src.replace(a, b)
src = re.sub(r"\?t484([a-z]?)=1", r"?t485\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(484, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/afford.js?t485f=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/walk/kochav/index.html?t485z=1', ['openBuilding', 'b=1', 'noindex', 'bldBtn'], []),\n"
                       "    ('/wp-content/plugins/nadlan-config/assets/walk/kochav/building.json?t485y=1', ['home_floor', 'ring'], []),\n"
                       "    ('/mortgage-calculator/mortgage-repayment-capacity/?t485r=1', ['data-nli=\"afford\"'], []),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.485 LIVE: [^"]*"\)', 'print("RELEASE 1.72.485 LIVE: the Kochav building in 3D")', src)
open(os.path.join(H, "deploy485.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy485.py written;", len(FILES), "files,", len(NEWF), "new")
