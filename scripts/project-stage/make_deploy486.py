# -*- coding: utf-8 -*-
"""make deploy486.py from deploy485.py: photoreal images on the Kochav cards (Ben 21.10 "not amateur"): bldg.jpg and thumb.jpg
replaced by gpt-image illustrations made from our 3D frames, bldg-real.jpg new (the building at dusk, opened from the floor card),
the walk index.html replaced (the "הבניין בהדמיה" button, captions per image)."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
NEWF = ["assets/walk/kochav/bldg-real.jpg"]
FILES = ["assets/walk/kochav/index.html", "assets/walk/kochav/bldg.jpg", "assets/walk/kochav/thumb.jpg"] + NEWF
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy485.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEWF) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.486: no hunk; the replaced files come back from .bak, the new file is unlinked on rollback"
src = "\n".join(lines)
for a, b in [("1.72.485", "1.72.486"), ("ps485", "ps486"), ("bak485", "bak486"), ("make_deploy485", "make_deploy486"),
             ("deploy-result-485", "deploy-result-486"), ("speed-485", "speed-486"), ("posts-before-485", "posts-before-486"),
             ("ashira_485", "ashira_486"), ("deploy-result-484", "deploy-result-485"), ("1.72.484", "1.72.485")]:
    src = src.replace(a, b)
src = re.sub(r"\?t485([a-z]?)=1", r"?t486\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(485, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/walk/kochav/index.html?t486z=1', ['openBuilding', 'b=1', 'noindex', 'bldBtn'], []),"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/walk/kochav/index.html?t486z=1', ['openBuilding', 'b=1', 'noindex', 'bldBtn', 'bldg-real.jpg', 'bvCap'], []),")
src = re.sub(r'print\("RELEASE 1\.72\.486 LIVE: [^"]*"\)', 'print("RELEASE 1.72.486 LIVE: photoreal Kochav card images + the building illustration in the 3D")', src)
open(os.path.join(H, "deploy486.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy486.py written;", len(FILES), "files,", len(NEWF), "new")
