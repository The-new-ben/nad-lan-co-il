# -*- coding: utf-8 -*-
"""make deploy506.py from deploy505.py: 1.72.506 (HAD-592, board item C12): the condo-documents tools for
/real-estate-lawyer/condo-documents/: tools/condo.js (NEW: condo = which document answers my question, on a sample drawing;
condomaj = who must agree), data/condo.json (NEW, official sources), inc/instruments.php (registry + plain summaries). No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["assets/instruments/tools/condo.js", "assets/instruments/data/condo.json", "inc/instruments.php"]
NEW = ["assets/instruments/tools/condo.js", "assets/instruments/data/condo.json"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy505.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEW) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.506: no hunk; the files come back from .bak on rollback, the new ones are removed"
src = "\n".join(lines)
for a, b in [("1.72.505", "1.72.506"), ("ps505", "ps506"), ("bak505", "bak506"), ("make_deploy505", "make_deploy506"),
             ("deploy-result-505", "deploy-result-506"), ("speed-505", "speed-506"), ("posts-before-505", "posts-before-506"),
             ("ashira_505", "ashira_506"), ("deploy-result-504", "deploy-result-505"), ("1.72.504", "1.72.505")]:
    src = src.replace(a, b)
src = re.sub(r"\?t505([a-z]?)=1", r"?t506\1=1", src)
src = re.sub(r"&t505([a-z]?)=1", r"&t506\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(505, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_506 as PX  # noqa: E402 \([^)]*\)", "import ashira_506 as PX  # noqa: E402 (1.72.506: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t506d=1',"
assert src.count(old) == 1, src.count(old)
ADD = [
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/condo.js?t506c=1", ["NLCD", "register('condo'", "register('condomaj'", "grid-template-areas"], []),
    ("/wp-content/plugins/nadlan-config/assets/instruments/data/condo.json?t506j=1", ['"key": "condo"', '"chips"', '"maj"', '"den": 3'], []),
    ("/pinkas-hakablanim/?t506p=1", ['data-nli="pinkas"', 'data-nli="sivug"', "בדיקת קבלן רשום"], []),
]
src = src.replace(old, "".join("    (%r, %r, %r),\n" % t for t in ADD) + old)
src = re.sub(r'print\("RELEASE 1\.72\.506 LIVE: [^"]*"\)', 'print("RELEASE 1.72.506 LIVE: the condo-documents tools")', src)
open(os.path.join(H, "deploy506.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_506.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.506 (HAD-592): the condo-documents tools. No hunk."""\nRELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy506.py + ashira_506.py written")
