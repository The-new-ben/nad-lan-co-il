# -*- coding: utf-8 -*-
"""make deploy487.py from deploy486.py: the tools column in the site footer (inc/legal-links.php replaced), no hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["inc/legal-links.php"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy486.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set([])"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.487: no hunk; legal-links.php comes back from .bak on rollback"
src = "\n".join(lines)
for a, b in [("1.72.486", "1.72.487"), ("ps486", "ps487"), ("bak486", "bak487"), ("make_deploy486", "make_deploy487"),
             ("deploy-result-486", "deploy-result-487"), ("speed-486", "speed-487"), ("posts-before-486", "posts-before-487"),
             ("ashira_486", "ashira_487"), ("deploy-result-485", "deploy-result-486"), ("1.72.485", "1.72.486")]:
    src = src.replace(a, b)
src = re.sub(r"\?t486([a-z]?)=1", r"?t487\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(486, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/walk/kochav/index.html?t487z=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/?t487a=1', ['class=\"nlpc-footer-tools\"', 'מחשבונים וכלים', '/arnona/', 'nlpc-footer-legal'], []),\n"
                       "    ('/en/sde-dov/?t487b=1', ['class=\"nlpc-footer-tools\"', 'Israeli mortgage from abroad'], []),\n"
                       "    ('/purchase-tax-calculator/?t487c=1', ['class=\"nlpc-footer-tools\"', '/property-value-estimator/'], []),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.487 LIVE: [^"]*"\)', 'print("RELEASE 1.72.487 LIVE: the tools column in the footer")', src)
open(os.path.join(H, "deploy487.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy487.py written;", len(FILES), "files")
