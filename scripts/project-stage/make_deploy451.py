# -*- coding: utf-8 -*-
"""Writes deploy451.py from the released deploy450.py: 1.72.451 = core.css lets text cells wrap (the forced-table rule had
nowrap on every cell). HAD-527 / HAD-533."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fix_451  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["assets/instruments/core.css"]
NEW = []
s = io.open(os.path.join(HERE, "deploy450.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import fix_450 as PX  # noqa: E402 (1.72.450: Instruments phone fixes)\n", "    import fix_451 as PX  # noqa: E402 (1.72.451: wrapping table cells)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.450)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.451)")')
rep('print("RELEASE 1.72.450 LIVE: Instruments phone fixes (answer bidi, wrapping cells, warranty table)")', 'print("RELEASE 1.72.451 LIVE: Instruments table cells wrap on phones")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/cpi-calculator/", ['data-nli="cpi"', 'instruments/core.css?ver=1.72.451'], [])]
OLD = "# 1.72.450 (Instruments phone fixes): the defects page keeps the warranty tool on the new engine css\n"
rep(OLD, "# 1.72.451 (wrapping cells): the cpi page loads the new engine css\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.450", "1.72.451"), (".bak450", ".bak451"), ("PS450", "PS451"), ("ps450", "ps451"), ("deploy450", "deploy451"),
             ("result-450", "result-451"), ("speed-450", "speed-451"), ("posts-before-450", "posts-before-451"), ("make_deploy450", "make_deploy451")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-449.json")', '_prev = os.path.join(QA, "deploy-result-450.json")'),
             ('"FATAL: release 1.72.449 is still in flight', '"FATAL: release 1.72.450 is still in flight'),
             ('WANT_LIVE = "1.72.449"  # the checks name ?ver=1.72.451: this runner is for the release right after 1.72.449',
              'WANT_LIVE = "1.72.450"  # the checks name ?ver=1.72.451: this runner is for the release right after 1.72.450'),
             ("        for n in range(449, 329, -1):", "        for n in range(450, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy451.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy451.py")
