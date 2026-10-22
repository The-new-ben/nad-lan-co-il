# -*- coding: utf-8 -*-
"""make deploy502.py from deploy501.py: 1.72.502 (HAD-592): the price map on phones: each cell of its tables carries a phone-only
label (the site's phone style hides table headers), the city zoom is square on a narrow screen, and a place name is printed only
where it does not cover another. No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["assets/instruments/tools/grprice.js"]
NEW = []
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy501.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEW) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.502: no hunk; the file comes back from .bak on rollback"
src = "\n".join(lines)
for a, b in [("1.72.501", "1.72.502"), ("ps501", "ps502"), ("bak501", "bak502"), ("make_deploy501", "make_deploy502"),
             ("deploy-result-501", "deploy-result-502"), ("speed-501", "speed-502"), ("posts-before-501", "posts-before-502"),
             ("ashira_501", "ashira_502"), ("deploy-result-500", "deploy-result-501"), ("1.72.500", "1.72.501")]:
    src = src.replace(a, b)
src = re.sub(r"\?t501([a-z]?)=1", r"?t502\1=1", src)
src = re.sub(r"&t501([a-z]?)=1", r"&t502\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(501, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_502 as PX  # noqa: E402 \([^)]*\)", "import ashira_502 as PX  # noqa: E402 (1.72.502: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t502d=1',"
assert src.count(old) == 1, src.count(old)
ADD = [
    ("/wp-content/plugins/nadlan-config/assets/instruments/tools/grprice.js?t502p=1", ["NLGP", "nlgp .l{display:none}", "boxes.some"], []),
    ("/prices-greece/?t502g=1", ['data-nli="grmap"', "מחירון נדל״ן ביוון"], []),
]
src = src.replace(old, "".join("    (%r, %r, %r),\n" % t for t in ADD) + old)
src = re.sub(r'print\("RELEASE 1\.72\.502 LIVE: [^"]*"\)', 'print("RELEASE 1.72.502 LIVE: the price map reads well on phones")', src)
open(os.path.join(H, "deploy502.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_502.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.502 (HAD-592): the price map on phones. No hunk."""\nRELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy502.py + ashira_502.py written")
