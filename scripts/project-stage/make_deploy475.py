# -*- coding: utf-8 -*-
"""make deploy475.py from deploy474.py: the Kochav home tour, furnished / empty (home.html replaced, pano/*-empty-2k.jpg new), no hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config"); WD = os.path.join(PLUG, "assets", "walk", "kochav")
NEWF = sorted("assets/walk/kochav/pano/" + f for f in os.listdir(os.path.join(WD, "pano")) if f.endswith("-empty-2k.jpg"))
FILES = ["assets/walk/kochav/home.html"] + NEWF
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy474.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEWF) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.475: no hunk; home.html is put back from the .bak on rollback, the new panos unlinked"
src = "\n".join(lines)
for a, b in [("1.72.474", "1.72.475"), ("ps474", "ps475"), ("bak474", "bak475"), ("make_deploy474", "make_deploy475"),
             ("deploy-result-474", "deploy-result-475"), ("speed-474", "speed-475"), ("posts-before-474", "posts-before-475"),
             ("ashira_474", "ashira_475"), ("deploy-result-473", "deploy-result-474"), ("1.72.473", "1.72.474"),
             ("?t474h=1", "?t475h=1"), ("?t474k=1", "?t475k=1"), ("?t474w=1", "?t475w=1"), ("?t474d=1", "?t475d=1"), ("?t474c=1", "?t475c=1"), ("?t474b=1", "?t475b=1"), ("?t474=1", "?t475=1")]:
    src = src.replace(a, b)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(474, 329, -1)", src); assert n == 1, n
old = "['window.__home', 'pano/', 'lang=en', 'noindex']"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "['window.__home', 'pano/', 'lang=en', 'noindex', 'id=\"furn\"', '-empty', 'body.emb']")
src = re.sub(r'print\("RELEASE 1\.72\.475 LIVE: [^"]*"\)', 'print("RELEASE 1.72.475 LIVE: the Kochav home tour, furnished / empty (assets/walk/kochav/home.html, pano/*-empty-2k.jpg)")', src)
open(os.path.join(H, "deploy475.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy475.py written;", len(FILES), "files,", len(NEWF), "new")
