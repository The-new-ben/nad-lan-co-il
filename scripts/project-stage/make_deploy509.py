# -*- coding: utf-8 -*-
"""make deploy509.py from deploy508.py: 1.72.509 (Ben 23.10.2026, Brevo): inc/mailer.php gets a settings screen (Settings >
מייל יוצא) where the owner pastes the SMTP login and key himself (write-only key field, test button), and the SMTP switch needs a
saved key, so the site keeps sending through the server until then. No hunk."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["inc/mailer.php"]
NEW = []
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
src = open(os.path.join(H, "deploy508.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"): lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("): lines[i] = "NEWFILES = set(" + repr(NEW) + ")"
    elif l.startswith("FILES = ["): lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["): lines[i] = "PHP_RELS = []  # 1.72.509: no hunk; the file comes back from .bak on rollback"
src = "\n".join(lines)
for a, b in [("1.72.508", "1.72.509"), ("ps508", "ps509"), ("bak508", "bak509"), ("make_deploy508", "make_deploy509"),
             ("deploy-result-508", "deploy-result-509"), ("speed-508", "speed-509"), ("posts-before-508", "posts-before-509"),
             ("ashira_508", "ashira_509"), ("deploy-result-507", "deploy-result-508"), ("1.72.507", "1.72.508")]:
    src = src.replace(a, b)
src = re.sub(r"\?t508([a-z]?)=1", r"?t509\1=1", src)
src = re.sub(r"&t508([a-z]?)=1", r"&t509\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(508, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_509 as PX  # noqa: E402 \([^)]*\)", "import ashira_509 as PX  # noqa: E402 (1.72.509: no hunk)", src); assert n == 1, n
old = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t509d=1',"
assert src.count(old) == 1, src.count(old)
ADD = [
    ("/properties/kochav-hatzafon-new-mini-penthouse-for-sale/?t509k=1", ['id="nadlan-pview"'], []),
]
src = src.replace(old, "".join("    (%r, %r, %r),\n" % t for t in ADD) + old)
src = re.sub(r'print\("RELEASE 1\.72\.509 LIVE: [^"]*"\)', 'print("RELEASE 1.72.509 LIVE: the outgoing-mail settings screen")', src)
open(os.path.join(H, "deploy509.py"), "w", encoding="utf-8", newline="\n").write(src)
open(os.path.join(H, "ashira_509.py"), "w", encoding="utf-8", newline="\n").write(
    '# -*- coding: utf-8 -*-\n"""Release 1.72.509: the outgoing-mail settings screen. No hunk."""\nRELS = []\n\n\ndef apply(rel, txt):\n    return txt\n')
print("deploy509.py + ashira_509.py written")
