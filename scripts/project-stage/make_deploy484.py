# -*- coding: utf-8 -*-
"""make deploy484.py from deploy483.py: the afford tool (afford.js new) + the registry; then place_tools.py 519=afford."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
NEWF = ["assets/instruments/tools/afford.js"]
FILES = ["inc/instruments.php"] + NEWF
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy483.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEWF) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.484: no hunk; instruments.php comes back from .bak, the new file is unlinked on rollback"
src = "\n".join(lines)
for a, b in [("1.72.483", "1.72.484"), ("ps483", "ps484"), ("bak483", "bak484"), ("make_deploy483", "make_deploy484"),
             ("deploy-result-483", "deploy-result-484"), ("speed-483", "speed-484"), ("posts-before-483", "posts-before-484"),
             ("ashira_483", "ashira_484"), ("deploy-result-482", "deploy-result-483"), ("1.72.482", "1.72.483")]:
    src = src.replace(a, b)
src = re.sub(r"\?t483([a-z]?)=1", r"?t484\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(483, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/nrm.js?t484m=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/afford.js?t484f=1', ['NLAF', \"register('afford'\"], []),\n"
                       "    ('/israel-mortgage-non-residents/?t484n=1', ['data-nli=\"nrm\"', 'lang=\"en\"', 'Short answer'], []),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.484 LIVE: [^"]*"\)', 'print("RELEASE 1.72.484 LIVE: the afford tool")', src)
open(os.path.join(H, "deploy484.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy484.py written;", len(FILES), "files,", len(NEWF), "new")
