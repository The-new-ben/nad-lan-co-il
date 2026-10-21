# -*- coding: utf-8 -*-
"""make deploy476.py from deploy475.py: the September 2026 index data (assets/instruments/data/*.json replaced), no hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["assets/instruments/data/cbs-120010.json", "assets/instruments/data/cbs-200010.json", "assets/instruments/data/boi-rate.json"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy475.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set([])"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.476: no hunk; the three data files are put back from their .bak on rollback"
src = "\n".join(lines)
for a, b in [("1.72.475", "1.72.476"), ("ps475", "ps476"), ("bak475", "bak476"), ("make_deploy475", "make_deploy476"),
             ("deploy-result-475", "deploy-result-476"), ("speed-475", "speed-476"), ("posts-before-475", "posts-before-476"),
             ("ashira_475", "ashira_476"), ("deploy-result-474", "deploy-result-475"), ("1.72.474", "1.72.475"),
             ("?t475h=1", "?t476h=1"), ("?t475k=1", "?t476k=1"), ("?t475w=1", "?t476w=1"), ("?t475d=1", "?t476d=1"), ("?t475c=1", "?t476c=1"), ("?t475b=1", "?t476b=1"), ("?t475=1", "?t476=1")]:
    src = src.replace(a, b)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(475, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/walk/kochav/home.html?t476h=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/instruments/data/cbs-120010.json?t476i=1', ['\"2026-09\"'], []),\n"
                       "    ('/wp-content/plugins/nadlan-config/assets/instruments/data/cbs-200010.json?t476j=1', ['\"2026-09\"'], []),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.476 LIVE: [^"]*"\)', 'print("RELEASE 1.72.476 LIVE: September 2026 index data (CPI, construction input, Bank of Israel rate)")', src)
open(os.path.join(H, "deploy476.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy476.py written;", len(FILES), "files")
