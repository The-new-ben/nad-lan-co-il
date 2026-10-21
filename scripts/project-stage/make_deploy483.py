# -*- coding: utf-8 -*-
"""make deploy483.py from deploy482.py: the nrm tool (English, non-resident mortgage: nrm.js + nrm.json + boi-fx.json new), the
engine (core.js: inputs can be redrawn from onField; inc/instruments.php: 'only' => 'en' tools, Latin fonts, the registry)."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
NEWF = ["assets/instruments/tools/nrm.js", "assets/instruments/data/nrm.json", "assets/instruments/data/boi-fx.json"]
FILES = ["inc/instruments.php", "assets/instruments/core.js"] + NEWF
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy482.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEWF) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.483: no hunk; instruments.php + core.js come back from .bak, the new files are unlinked on rollback"
src = "\n".join(lines)
for a, b in [("1.72.482", "1.72.483"), ("ps482", "ps483"), ("bak482", "bak483"), ("make_deploy482", "make_deploy483"),
             ("deploy-result-482", "deploy-result-483"), ("speed-482", "speed-483"), ("posts-before-482", "posts-before-483"),
             ("ashira_482", "ashira_483"), ("deploy-result-481", "deploy-result-482"), ("1.72.481", "1.72.482")]:
    src = src.replace(a, b)
src = re.sub(r"\?t482([a-z]?)=1", r"?t483\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(482, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/arnona.js?t483a=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/nrm.js?t483m=1', ['NLNR', \"register('nrm'\"], []),\n"
                       "    ('/wp-content/plugins/nadlan-config/assets/instruments/data/boi-fx.json?t483x=1', ['\"key\":\"fx\"', 'USD'], []),\n"
                       "    ('/arnona/?t483o=1', ['data-nli=\"arnona\"', 'FAQPage', '112.99'], []),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.483 LIVE: [^"]*"\)', 'print("RELEASE 1.72.483 LIVE: the nrm non-resident mortgage tool (English) + engine redraw/only")', src)
open(os.path.join(H, "deploy483.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy483.py written;", len(FILES), "files,", len(NEWF), "new")
