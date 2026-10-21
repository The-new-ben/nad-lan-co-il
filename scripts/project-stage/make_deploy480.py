# -*- coding: utf-8 -*-
"""make deploy480.py from deploy479.py: the pcost tool (pcost.js + cost.json new, the registry in inc/instruments.php), no hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
NEWF = ["assets/instruments/tools/pcost.js", "assets/instruments/data/cost.json"]
FILES = ["inc/instruments.php"] + NEWF
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy479.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEWF) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.480: no hunk; instruments.php comes back from .bak, the new files are unlinked on rollback"
src = "\n".join(lines)
for a, b in [("1.72.479", "1.72.480"), ("ps479", "ps480"), ("bak479", "bak480"), ("make_deploy479", "make_deploy480"),
             ("deploy-result-479", "deploy-result-480"), ("speed-479", "speed-480"), ("posts-before-479", "posts-before-480"),
             ("ashira_479", "ashira_480"), ("deploy-result-478", "deploy-result-479"), ("1.72.478", "1.72.479")]:
    src = src.replace(a, b)
src = re.sub(r"\?t479([a-z]?)=1", r"?t480\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(479, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/ptax.js?t480p=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/pcost.js?t480g=1', ['NLPC', \"register('pcost'\"], []),\n"
                       "    ('/wp-content/plugins/nadlan-config/assets/instruments/data/cost.json?t480h=1', ['\"key\": \"cost\"', 'mortgage_fee'], []),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.480 LIVE: [^"]*"\)', 'print("RELEASE 1.72.480 LIVE: the pcost total purchase cost tool")', src)
open(os.path.join(H, "deploy480.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy480.py written;", len(FILES), "files")
