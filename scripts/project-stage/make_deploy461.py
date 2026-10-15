# -*- coding: utf-8 -*-
"""Writes deploy461.py from the released deploy460.py: 1.72.461 (Ben 15.10.2026): (1) the health check tells the truth about
Morning: the old probe read the API base URL, which answers 404 by design, so every check and agent said "Morning is broken";
now it reports whether Morning answers and how many Morning payment methods the checkout offers (inc/health.php); (2) the
soil content guard is removed (Ben: no content filters); the project pages stay clean at the source (cleaned in the CMS)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import names_457 as _  # noqa: E402,F401  (no hunk: same module shape)
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["inc/instruments.php", "inc/health.php"]
NEW = []
s = io.open(os.path.join(HERE, "deploy460.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.460)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.461)")')
rep('print("RELEASE 1.72.460 LIVE: the soil guard on every project page")', 'print("RELEASE 1.72.461 LIVE: the health check tells the truth about Morning; no content guard")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
OLD = "# 1.72.460 (soil guard): no project page carries the soil subject\n"
rep(OLD, "# 1.72.461 (health): the project pages stay clean without a guard (the 460 rows still forbid the subject)\n" + OLD)
for x, y in (("1.72.460", "1.72.461"), (".bak460", ".bak461"), ("PS460", "PS461"), ("ps460", "ps461"), ("deploy460", "deploy461"),
             ("result-460", "result-461"), ("speed-460", "speed-461"), ("posts-before-460", "posts-before-461"), ("make_deploy460", "make_deploy461")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-459.json")', '_prev = os.path.join(QA, "deploy-result-460.json")'),
             ('"FATAL: release 1.72.459 is still in flight', '"FATAL: release 1.72.460 is still in flight'),
             ('WANT_LIVE = "1.72.459"  # the checks name ?ver=1.72.461: this runner is for the release right after 1.72.459',
              'WANT_LIVE = "1.72.460"  # the checks name ?ver=1.72.461: this runner is for the release right after 1.72.460'),
             ("        for n in range(459, 329, -1):", "        for n in range(460, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy461.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy461.py")
