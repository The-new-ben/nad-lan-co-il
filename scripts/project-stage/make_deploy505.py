# -*- coding: utf-8 -*-
"""make deploy505.py from deploy504.py: 1.72.505 (HAD-592): the contractor check, three fixes seen live on a phone: level ק
written as the official "ק" (not "אק"), "נמצא קבלן אחד" for one result, and choosing a job clears the typed name. No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["assets/instruments/tools/pinkas.js"]
NEW = []
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy504.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEW) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.505: no hunk; the file comes back from .bak on rollback"
src = "\n".join(lines)
for a, b in [("1.72.504", "1.72.505"), ("ps504", "ps505"), ("bak504", "bak505"), ("make_deploy504", "make_deploy505"),
             ("deploy-result-504", "deploy-result-505"), ("speed-504", "speed-505"), ("posts-before-504", "posts-before-505"),
             ("ashira_504", "ashira_505"), ("deploy-result-503", "deploy-result-504"), ("1.72.503", "1.72.504")]:
    src = src.replace(a, b)
src = re.sub(r"\?t504([a-z]?)=1", r"?t505\1=1", src)
src = re.sub(r"&t504([a-z]?)=1", r"&t505\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(504, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_505 as PX  # noqa: E402 \([^)]*\)", "import ashira_505 as PX  # noqa: E402 (1.72.505: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t505d=1',"
assert src.count(old) == 1, src.count(old)
ADD = [
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/pinkas.js?t505k=1", ["function code(g, l)", "קבלן אחד", "st.q = ''; qi.value = ''"], []),
    ("/pinkas-hakablanim/?t505p=1", ['data-nli="pinkas"', 'data-nli="sivug"', "בדיקת קבלן רשום"], []),
]
src = src.replace(old, "".join("    (%r, %r, %r),\n" % t for t in ADD) + old)
src = re.sub(r'print\("RELEASE 1\.72\.505 LIVE: [^"]*"\)', 'print("RELEASE 1.72.505 LIVE: the contractor check reads right")', src)
open(os.path.join(H, "deploy505.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_505.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.505 (HAD-592): contractor check fixes. No hunk."""\nRELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy505.py + ashira_505.py written")
