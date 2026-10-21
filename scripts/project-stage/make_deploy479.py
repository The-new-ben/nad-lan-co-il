# -*- coding: utf-8 -*-
"""make deploy479.py from deploy478.py: ptax.js (the note out of the result lines) + inc/instruments.php (the FAQ heading may
carry words after "שאלות נפוצות"), both replaced, no hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["inc/instruments.php", "assets/instruments/tools/ptax.js"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy478.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set([])"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.479: no hunk; both files come back from their .bak on rollback"
src = "\n".join(lines)
for a, b in [("1.72.478", "1.72.479"), ("ps478", "ps479"), ("bak478", "bak479"), ("make_deploy478", "make_deploy479"),
             ("deploy-result-478", "deploy-result-479"), ("speed-478", "speed-479"), ("posts-before-478", "posts-before-479"),
             ("ashira_478", "ashira_479"), ("deploy-result-477", "deploy-result-478"), ("1.72.477", "1.72.478")]:
    src = src.replace(a, b)
src = re.sub(r"\?t478([a-z]?)=1", r"?t479\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(478, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/ptax.js?t479p=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/purchase-tax-calculator/?t479f=1', ['data-nli=\"ptax\"', 'FAQPage', 'האם מחשבון מס רכישה מספיק לפני חתימה?'], ['nlc-ptx']),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.479 LIVE: [^"]*"\)', 'print("RELEASE 1.72.479 LIVE: ptax note + FAQ heading match")', src)
open(os.path.join(H, "deploy479.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy479.py written;", len(FILES), "files")
