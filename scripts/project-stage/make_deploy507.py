# -*- coding: utf-8 -*-
"""make deploy507.py from deploy506.py: 1.72.507 (Ben 22.10.2026: "make the emails efficient; alert me when people view
properties"): inc/owner-morning.php (NEW: property-view beacon + /nadlan/v1/pview, hot alerts capped, one morning email at 08:00
Israel), inc/alerts.php (daily lead reminder stands down; loads the module), inc/lead-inbox.php (daily summary stands down),
inc/health.php (technical alerts queued into the morning email), inc/lead-e2e.php (no second email per lead). No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["inc/owner-morning.php", "inc/alerts.php", "inc/lead-inbox.php", "inc/health.php", "inc/lead-e2e.php"]
NEW = ["inc/owner-morning.php"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy506.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEW) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.507: no hunk; the files come back from .bak on rollback, the new ones are removed"
src = "\n".join(lines)
for a, b in [("1.72.506", "1.72.507"), ("ps506", "ps507"), ("bak506", "bak507"), ("make_deploy506", "make_deploy507"),
             ("deploy-result-506", "deploy-result-507"), ("speed-506", "speed-507"), ("posts-before-506", "posts-before-507"),
             ("ashira_506", "ashira_507"), ("deploy-result-505", "deploy-result-506"), ("1.72.505", "1.72.506")]:
    src = src.replace(a, b)
src = re.sub(r"\?t506([a-z]?)=1", r"?t507\1=1", src)
src = re.sub(r"&t506([a-z]?)=1", r"&t507\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(506, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_507 as PX  # noqa: E402 \([^)]*\)", "import ashira_507 as PX  # noqa: E402 (1.72.507: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t507d=1',"
assert src.count(old) == 1, src.count(old)
ADD = [
    ("/properties/kochav-hatzafon-new-mini-penthouse-for-sale/?t507k=1", ['id="nadlan-pview"', "wp-json/nadlan/v1/pview", "go('read')"], []),
    ("/properties/bialik-rg-4r-demo/?t507d=1", [], ['id="nadlan-pview"']),
    ("/wp-json/nadlan/v1?t507n=1", ["pview", "om-preview"], []),
    ("/real-estate-lawyer/condo-documents/?t507c=1", ['data-nli="condo"', 'data-nli="condomaj"'], []),
]
src = src.replace(old, "".join("    (%r, %r, %r),\n" % t for t in ADD) + old)
src = re.sub(r'print\("RELEASE 1\.72\.507 LIVE: [^"]*"\)', 'print("RELEASE 1.72.507 LIVE: one morning email, property-view alerts")', src)
open(os.path.join(H, "deploy507.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_507.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.507: one morning email and property-view alerts. No hunk."""\nRELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy507.py + ashira_507.py written")
