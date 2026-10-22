# -*- coding: utf-8 -*-
"""make deploy504.py from deploy503.py: 1.72.504 (HAD-592, the page loop): the registered-contractor check for /pinkas-hakablanim/.
  - inc/pinkas.php (NEW): the REST search /wp-json/nadlan/v1/pinkas over the 17,874 contractors (no phone, email or street).
  - data/pinkas-register.php (NEW): the register for the search, starting with "<?php exit; ?>" (a direct request returns nothing).
  - assets/instruments/tools/pinkas.js (NEW): the tools pinkas (search + "my job") and sivug (the classification ladder).
  - assets/instruments/data/pinkas-meta.json (NEW): the table in force, thresholds, branches, cities, counts.
  - inc/instruments.php: the two tools in the registry, their plain summaries, and the require of inc/pinkas.php.
  - assets/instruments/tools/grprice.js: the map dots lose their radius animation (a paused tab kept the old size).
No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["inc/pinkas.php", "data/pinkas-register.php", "assets/instruments/tools/pinkas.js", "assets/instruments/data/pinkas-meta.json", "inc/instruments.php", "assets/instruments/tools/grprice.js"]
NEW = ["inc/pinkas.php", "data/pinkas-register.php", "assets/instruments/tools/pinkas.js", "assets/instruments/data/pinkas-meta.json"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy503.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEW) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.504: no hunk; the files come back from .bak on rollback, the new ones are removed"
src = "\n".join(lines)
for a, b in [("1.72.503", "1.72.504"), ("ps503", "ps504"), ("bak503", "bak504"), ("make_deploy503", "make_deploy504"),
             ("deploy-result-503", "deploy-result-504"), ("speed-503", "speed-504"), ("posts-before-503", "posts-before-504"),
             ("ashira_503", "ashira_504"), ("deploy-result-502", "deploy-result-503"), ("1.72.502", "1.72.503")]:
    src = src.replace(a, b)
src = re.sub(r"\?t503([a-z]?)=1", r"?t504\1=1", src)
src = re.sub(r"&t503([a-z]?)=1", r"&t504\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(503, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_504 as PX  # noqa: E402 \([^)]*\)", "import ashira_504 as PX  # noqa: E402 (1.72.504: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t504d=1',"
assert src.count(old) == 1, src.count(old)
ADD = [
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/pinkas.js?t504k=1", ["NLPK", "register('pinkas'", "register('sivug'", "rasham/details/"], []),
    ("/wp-content/plugins/nadlan-config/assets/instruments/data/pinkas-meta.json?t504m=1", ['"key":"pk"', '"thr"', '"sqm"'], []),
    ("/wp-json/nadlan/v1/pinkas?q=3470&t504r=1", ['"n":3470', '"total":1', '"b":[['], ["MISPAR_TEL", "EMAIL", "SHEM_REHOV"]),
    ("/wp-content/plugins/nadlan-config/data/pinkas-register.php?t504x=1", [], ['"rows"', '"cities"']),
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/grprice.js?t504p=1", ["NLGP", "lastW = cw"], ["transition:r"]),
    ("/prices-greece/?t504g=1", ['data-nli="grmap"', "מחירון נדל״ן ביוון"], []),
]
src = src.replace(old, "".join("    (%r, %r, %r),\n" % t for t in ADD) + old)
src = re.sub(r'print\("RELEASE 1\.72\.504 LIVE: [^"]*"\)', 'print("RELEASE 1.72.504 LIVE: the registered-contractor check and its search")', src)
open(os.path.join(H, "deploy504.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_504.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.504 (HAD-592): the registered-contractor check. No hunk."""\nRELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy504.py + ashira_504.py written")
