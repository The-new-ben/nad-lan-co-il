# -*- coding: utf-8 -*-
"""make deploy481.py from deploy480.py: the pval tool (pval.js + value.json new), core.js (select optionsFrom) and the registry."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
NEWF = ["assets/instruments/tools/pval.js", "assets/instruments/data/value.json"]
FILES = ["inc/instruments.php", "assets/instruments/core.js"] + NEWF
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy480.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEWF) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.481: no hunk; instruments.php + core.js come back from .bak, the new files are unlinked on rollback"
src = "\n".join(lines)
for a, b in [("1.72.480", "1.72.481"), ("ps480", "ps481"), ("bak480", "bak481"), ("make_deploy480", "make_deploy481"),
             ("deploy-result-480", "deploy-result-481"), ("speed-480", "speed-481"), ("posts-before-480", "posts-before-481"),
             ("ashira_480", "ashira_481"), ("deploy-result-479", "deploy-result-480"), ("1.72.479", "1.72.480")]:
    src = src.replace(a, b)
src = re.sub(r"\?t480([a-z]?)=1", r"?t481\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(480, 329, -1)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/pcost.js?t481g=1',"
assert src.count(old) == 1, src.count(old)
src = src.replace(old, "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/pval.js?t481v=1', ['NLPV', \"register('pval'\"], []),\n"
                       "    ('/wp-content/plugins/nadlan-config/assets/instruments/data/value.json?t481u=1', ['\"key\":\"value\"', 'הצפון החדש'], []),\n"
                       "    ('/apartment-purchase-cost-calculator/?t481c=1', ['data-nli=\"pcost\"', 'FAQPage'], ['id=\"nap-price\"']),\n" + old)
src = re.sub(r'print\("RELEASE 1\.72\.481 LIVE: [^"]*"\)', 'print("RELEASE 1.72.481 LIVE: the pval home value tool + select optionsFrom")', src)
open(os.path.join(H, "deploy481.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy481.py written;", len(FILES), "files,", len(NEWF), "new")
