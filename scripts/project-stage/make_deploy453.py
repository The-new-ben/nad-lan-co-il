# -*- coding: utf-8 -*-
"""Writes deploy453.py from the released deploy452.py: 1.72.453 = the indexation and delay tables fit a phone
(table.phoneHide). HAD-527 / HAD-533."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fix_453  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["assets/instruments/tools/indexation.js", "assets/instruments/tools/delay.js"]
NEW = []
s = io.open(os.path.join(HERE, "deploy452.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import fix_452 as PX  # noqa: E402 (1.72.452: Instruments cells on phones)\n", "    import fix_453 as PX  # noqa: E402 (1.72.453: phone tables of indexation and delay)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.452)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.453)")')
rep('print("RELEASE 1.72.452 LIVE: Instruments cells hold padding and fonts on phones; warranty status cell")', 'print("RELEASE 1.72.453 LIVE: the indexation and delay tables fit a phone")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/new-projects/contractor-delay-compensation/", ['data-nli="delay"', 'tools/delay.js?ver=1.72.453'], [])]
OLD = "# 1.72.452 (cells on phones): the indexation page loads the new engine\n"
rep(OLD, "# 1.72.453 (phone tables): the delay page loads the new delay.js\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.452", "1.72.453"), (".bak452", ".bak453"), ("PS452", "PS453"), ("ps452", "ps453"), ("deploy452", "deploy453"),
             ("result-452", "result-453"), ("speed-452", "speed-453"), ("posts-before-452", "posts-before-453"), ("make_deploy452", "make_deploy453")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-451.json")', '_prev = os.path.join(QA, "deploy-result-452.json")'),
             ('"FATAL: release 1.72.451 is still in flight', '"FATAL: release 1.72.452 is still in flight'),
             ('WANT_LIVE = "1.72.451"  # the checks name ?ver=1.72.453: this runner is for the release right after 1.72.451',
              'WANT_LIVE = "1.72.452"  # the checks name ?ver=1.72.453: this runner is for the release right after 1.72.452'),
             ("        for n in range(451, 329, -1):", "        for n in range(452, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy453.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy453.py")
