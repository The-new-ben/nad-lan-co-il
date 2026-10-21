# -*- coding: utf-8 -*-
"""make deploy482.py from deploy481.py: the arnona tool (arnona.js + arnona-tlv.json new) and the registry; then the new page /arnona/."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
NEWF = ["assets/instruments/tools/arnona.js", "assets/instruments/data/arnona-tlv.json"]
FILES = ["inc/instruments.php"] + NEWF
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy481.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEWF) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.482: no hunk; instruments.php comes back from .bak, the new files are unlinked on rollback"
src = "\n".join(lines)
for a, b in [("1.72.481", "1.72.482"), ("ps481", "ps482"), ("bak481", "bak482"), ("make_deploy481", "make_deploy482"),
             ("deploy-result-481", "deploy-result-482"), ("speed-481", "speed-482"), ("posts-before-481", "posts-before-482"),
             ("ashira_481", "ashira_482"), ("deploy-result-480", "deploy-result-481"), ("1.72.480", "1.72.481")]:
    src = src.replace(a, b)
src = re.sub(r"\?t481([a-z]?)=1", r"?t482\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(481, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/pval.js?t482v=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/arnona.js?t482a=1', ['NLAR', \"register('arnona'\"], []),\n"
                       "    ('/wp-content/plugins/nadlan-config/assets/instruments/data/arnona-tlv.json?t482t=1', ['\"key\":\"arnona\"', '112.99'], []),\n"
                       "    ('/property-value-estimator/?t482e=1', ['data-nli=\"pval\"', 'FAQPage'], ['id=\"npv-area\"']),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.482 LIVE: [^"]*"\)', 'print("RELEASE 1.72.482 LIVE: the Tel Aviv arnona tool")', src)
open(os.path.join(H, "deploy482.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy482.py written;", len(FILES), "files,", len(NEWF), "new")
