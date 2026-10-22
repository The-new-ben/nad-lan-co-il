# -*- coding: utf-8 -*-
"""make deploy501.py from deploy500.py: 1.72.501 (HAD-592, Ben's Greece price list, 22.10.2026).
  - assets/instruments/tools/grprice.js (NEW): grmap (the price map of Greece, chips, city zooms, card, compare tray), grbudget (what a
    budget buys in 250 places), grisrael (an Israeli city's official median, in m² in every Greek place).
  - data/greece-prices.json (NEW, 263 places from docs/research/2026-10-22-greece-prices/prices.json), data/greece-map.json (NEW,
    Natural Earth 1:10m, public domain).
  - inc/instruments.php: the three tools in the registry, their plain summaries (the map's is the whole price table).
  - inc/global-worlds.php: the Greece hub lists the price list first among its guides.
No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["assets/instruments/tools/grprice.js", "assets/instruments/data/greece-prices.json", "assets/instruments/data/greece-map.json", "inc/instruments.php", "inc/global-worlds.php"]
NEW = ["assets/instruments/tools/grprice.js", "assets/instruments/data/greece-prices.json", "assets/instruments/data/greece-map.json"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy500.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEW) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.501: no hunk; the files come back from .bak on rollback, the new ones are removed"
src = "\n".join(lines)
for a, b in [("1.72.500", "1.72.501"), ("ps500", "ps501"), ("bak500", "bak501"), ("make_deploy500", "make_deploy501"),
             ("deploy-result-500", "deploy-result-501"), ("speed-500", "speed-501"), ("posts-before-500", "posts-before-501"),
             ("ashira_500", "ashira_501"), ("deploy-result-499", "deploy-result-500"), ("1.72.499", "1.72.500")]:
    src = src.replace(a, b)
src = re.sub(r"\?t500([a-z]?)=1", r"?t501\1=1", src)
src = re.sub(r"&t500([a-z]?)=1", r"&t501\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(500, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_501 as PX  # noqa: E402 \([^)]*\)", "import ashira_501 as PX  # noqa: E402 (1.72.501: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t501d=1',"
assert src.count(old) == 1, src.count(old)
ADD = [
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/grprice.js?t501g=1", ["NLGP", "register('grmap'", "register('grbudget'", "register('grisrael'"], []),
    ("/wp-content/plugins/nadlan-config/assets/instruments/data/greece-prices.json?t501j=1", ['"key":"gp"', '"places"', "ath-centre"], []),
    ("/wp-content/plugins/nadlan-config/assets/instruments/data/greece-map.json?t501m=1", ['"key":"gmap"', '"gr":"M'], []),
    ("/purchase-tax-calculator/?t501s=1", ['data-nli="ptax"', "הוראת שעה עד 31.12.2026"], []),
]
src = src.replace(old, "".join("    (%r, %r, %r),\n" % t for t in ADD) + old)
src = re.sub(r'print\("RELEASE 1\.72\.501 LIVE: [^"]*"\)', 'print("RELEASE 1.72.501 LIVE: the Greece price map, budget and Israel tools")', src)
open(os.path.join(H, "deploy501.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_501.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.501 (HAD-592): the Greece price map, budget and Israel tools. No hunk."""\nRELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy501.py + ashira_501.py written")
