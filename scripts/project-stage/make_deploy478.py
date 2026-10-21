# -*- coding: utf-8 -*-
"""make deploy478.py from deploy477.py: the ptax tool (2 new files + the registry) (the dossier guard goes to the snippet x-broker-drop separately)."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
NEWF = ["assets/instruments/tools/ptax.js", "assets/instruments/data/ptax.json"]
FILES = ["inc/instruments.php"] + NEWF
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy477.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEWF) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.478: no hunk; the two PHP files come back from .bak, the new files are unlinked on rollback"
src = "\n".join(lines)
for a, b in [("1.72.477", "1.72.478"), ("ps477", "ps478"), ("bak477", "bak478"), ("make_deploy477", "make_deploy478"),
             ("deploy-result-477", "deploy-result-478"), ("speed-477", "speed-478"), ("posts-before-477", "posts-before-478"),
             ("ashira_477", "ashira_478"), ("deploy-result-476", "deploy-result-477"), ("1.72.476", "1.72.477"),
             ("?t477n=1", "?t478n=1"), ("?t477s=1", "?t478s=1"), ("?t477i=1", "?t478i=1"), ("?t477j=1", "?t478j=1"), ("?t477h=1", "?t478h=1"), ("?t477k=1", "?t478k=1"), ("?t477w=1", "?t478w=1"), ("?t477d=1", "?t478d=1"), ("?t477c=1", "?t478c=1"), ("?t477b=1", "?t478b=1"), ("?t477=1", "?t478=1")]:
    src = src.replace(a, b)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(477, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/core.js?t478n=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/ptax.js?t478p=1', ['NLPT', \"register('ptax'\"], []),\n"
                       "    ('/wp-content/plugins/nadlan-config/assets/instruments/data/ptax.json?t478q=1', ['\"key\": \"ptax\"', '20183565'], []),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.478 LIVE: [^"]*"\)', 'print("RELEASE 1.72.478 LIVE: the ptax purchase tax tool + the dossier guard in the drop engine")', src)
open(os.path.join(H, "deploy478.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy478.py written;", len(FILES), "files,", len(NEWF), "new")
