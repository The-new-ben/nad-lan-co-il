# -*- coding: utf-8 -*-
"""make deploy500.py from deploy499.py: 1.72.500 (HAD-592 C14, the purchase-tax upgrade; research docs/research/2026-10-22-purchase-tax/brief.md).
  - assets/instruments/tools/ptax.js v2: every track with its own end date (the additional-home rate is a temporary order to
    31.12.2026), the oleh cap (12A does not apply above 20,183,565) and regulation 12, the disabled (regulation 11), land, gifts,
    the upgrader's sell-by date with the war extension (instruction 2/2026), presets; data/ptax.json carries the new rules.
  - tools/pcost.js + tools/afford.js: the oleh cap. inc/instruments.php: the ptax summary and description by track.
No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["assets/instruments/tools/ptax.js", "assets/instruments/data/ptax.json", "assets/instruments/tools/pcost.js", "assets/instruments/tools/afford.js", "inc/instruments.php"]
NEW = []
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy499.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEW) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.500: no hunk; the files come back from .bak on rollback"
src = "\n".join(lines)
for a, b in [("1.72.499", "1.72.500"), ("ps499", "ps500"), ("bak499", "bak500"), ("make_deploy499", "make_deploy500"),
             ("deploy-result-499", "deploy-result-500"), ("speed-499", "speed-500"), ("posts-before-499", "posts-before-500"),
             ("ashira_499", "ashira_500"), ("deploy-result-498", "deploy-result-499"), ("1.72.498", "1.72.499")]:
    src = src.replace(a, b)
src = re.sub(r"\?t499([a-z]?)=1", r"?t500\1=1", src)
src = re.sub(r"&t499([a-z]?)=1", r"&t500\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(499, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_500 as PX  # noqa: E402 \([^)]*\)", "import ashira_500 as PX  # noqa: E402 (1.72.500: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t500d=1',"
assert src.count(old) == 1, src.count(old)
NO_LOGO_H1 = '<h1><a href="https://nad-lan.co.il/">'
ADD = [
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/ptax.js?t500p=1", ["NLPT", "register('ptax'", "sellBy", "oleh12"], []),
    ("/wp-content/plugins/nadlan-config/assets/instruments/data/ptax.json?t500q=1", ['"valid"', "2026-12-31", '"oleh_cap"', '"upgrader"'], []),
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/pcost.js?t500c=1", ["NLPC", "oleh_cap"], []),
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/afford.js?t500a=1", ["NLAF", "oleh_cap"], []),
    ("/purchase-tax-calculator/?t500s=1", ['data-nli="ptax"', "הוראת שעה עד 31.12.2026", "20,183,565"], []),
]
src = src.replace(old, "".join("    (%r, %r, %r),\n" % t for t in ADD) + old)
src = re.sub(r'print\("RELEASE 1\.72\.500 LIVE: [^"]*"\)', 'print("RELEASE 1.72.500 LIVE: the purchase-tax tool by track, with the upgrader date")', src)
open(os.path.join(H, "deploy500.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_500.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.500 (HAD-592 C14): the purchase-tax tool by track, with the upgrader date. No hunk."""\n'
    'RELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy500.py + ashira_500.py written")
