# -*- coding: utf-8 -*-
"""make deploy477.py from deploy476.py: the bilingual Instruments engine (6 files replaced), no hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["inc/instruments.php", "assets/instruments/core.js", "assets/instruments/core.css", "assets/instruments/tools/soilmap.js",
         "assets/instruments/tools/pfas.js", "assets/instruments/tools/soilask.js"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy476.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set([])"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.477: no hunk; the six files are put back from their .bak on rollback"
src = "\n".join(lines)
for a, b in [("1.72.476", "1.72.477"), ("ps476", "ps477"), ("bak476", "bak477"), ("make_deploy476", "make_deploy477"),
             ("deploy-result-476", "deploy-result-477"), ("speed-476", "speed-477"), ("posts-before-476", "posts-before-477"),
             ("ashira_476", "ashira_477"), ("deploy-result-475", "deploy-result-476"), ("1.72.475", "1.72.476"),
             ("?t476i=1", "?t477i=1"), ("?t476j=1", "?t477j=1"), ("?t476h=1", "?t477h=1"), ("?t476k=1", "?t477k=1"), ("?t476w=1", "?t477w=1"), ("?t476d=1", "?t477d=1"), ("?t476c=1", "?t477c=1"), ("?t476b=1", "?t477b=1"), ("?t476=1", "?t477=1")]:
    src = src.replace(a, b)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(476, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/data/cbs-120010.json?t477i=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/instruments/core.js?t477n=1', ['langOf', 'he-IL'], []),\n"
                       "    ('/sde-dov/contamination/?t477s=1', ['data-nli=\"soilmap\"', 'class=\"nli\" dir=\"rtl\" lang=\"he\"', 'nadlan-nli-ld'], []),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.477 LIVE: [^"]*"\)', 'print("RELEASE 1.72.477 LIVE: the Instruments engine in English for the soil tools (Hebrew unchanged)")', src)
open(os.path.join(H, "deploy477.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy477.py written;", len(FILES), "files")
