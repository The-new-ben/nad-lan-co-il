# -*- coding: utf-8 -*-
"""make deploy508.py from deploy507.py: 1.72.508: the admin preview of the morning email takes ?day=YYYY-MM-DD, so the
property-views table can be checked on any day before the first 08:00 email. No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["inc/owner-morning.php"]
NEW = []
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy507.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEW) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.508: no hunk; the file comes back from .bak on rollback"
src = "\n".join(lines)
for a, b in [("1.72.507", "1.72.508"), ("ps507", "ps508"), ("bak507", "bak508"), ("make_deploy507", "make_deploy508"),
             ("deploy-result-507", "deploy-result-508"), ("speed-507", "speed-508"), ("posts-before-507", "posts-before-508"),
             ("ashira_507", "ashira_508"), ("deploy-result-506", "deploy-result-507"), ("1.72.506", "1.72.507")]:
    src = src.replace(a, b)
src = re.sub(r"\?t507([a-z]?)=1", r"?t508\1=1", src)
src = re.sub(r"&t507([a-z]?)=1", r"&t508\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(507, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_508 as PX  # noqa: E402 \([^)]*\)", "import ashira_508 as PX  # noqa: E402 (1.72.508: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t508d=1',"
assert src.count(old) == 1, src.count(old)
ADD = [
    ("/properties/kochav-hatzafon-new-mini-penthouse-for-sale/?t508k=1", ['id="nadlan-pview"', "go('read')"], []),
    ("/wp-json/nadlan/v1?t508n=1", ["pview", "om-preview"], []),
]
src = src.replace(old, "".join("    (%r, %r, %r),\n" % t for t in ADD) + old)
src = re.sub(r'print\("RELEASE 1\.72\.507 LIVE: [^"]*"\)', 'print("RELEASE 1.72.508 LIVE: morning-email preview by day")', src)
open(os.path.join(H, "deploy508.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_508.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.508: morning-email preview by day. No hunk."""\nRELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy508.py + ashira_508.py written")
