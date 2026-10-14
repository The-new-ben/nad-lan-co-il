# -*- coding: utf-8 -*-
"""Writes deploy452.py from the released deploy451.py: 1.72.452 = Instruments cells hold their own padding and fonts on
phones, table.phoneHide in the engine, the warranty status cell with its end date. HAD-527 / HAD-533."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fix_452  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["assets/instruments/core.css", "assets/instruments/core.js", "assets/instruments/tools/warranty.js"]
NEW = []
s = io.open(os.path.join(HERE, "deploy451.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import fix_451 as PX  # noqa: E402 (1.72.451: wrapping table cells)\n", "    import fix_452 as PX  # noqa: E402 (1.72.452: Instruments cells on phones)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.451)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.452)")')
rep('print("RELEASE 1.72.451 LIVE: Instruments table cells wrap on phones")', 'print("RELEASE 1.72.452 LIVE: Instruments cells hold padding and fonts on phones; warranty status cell")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/new-projects/construction-input-index/", ['data-nli="indexation"', 'instruments/core.js?ver=1.72.452', 'instruments/core.css?ver=1.72.452'], [])]
OLD = "# 1.72.451 (wrapping cells): the cpi page loads the new engine css\n"
rep(OLD, "# 1.72.452 (cells on phones): the indexation page loads the new engine\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.451", "1.72.452"), (".bak451", ".bak452"), ("PS451", "PS452"), ("ps451", "ps452"), ("deploy451", "deploy452"),
             ("result-451", "result-452"), ("speed-451", "speed-452"), ("posts-before-451", "posts-before-452"), ("make_deploy451", "make_deploy452")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-450.json")', '_prev = os.path.join(QA, "deploy-result-451.json")'),
             ('"FATAL: release 1.72.450 is still in flight', '"FATAL: release 1.72.451 is still in flight'),
             ('WANT_LIVE = "1.72.450"  # the checks name ?ver=1.72.452: this runner is for the release right after 1.72.450',
              'WANT_LIVE = "1.72.451"  # the checks name ?ver=1.72.452: this runner is for the release right after 1.72.451'),
             ("        for n in range(450, 329, -1):", "        for n in range(451, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy452.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy452.py")
