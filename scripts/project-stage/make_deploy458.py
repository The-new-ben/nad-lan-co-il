# -*- coding: utf-8 -*-
"""Writes deploy458.py from the released deploy457.py: 1.72.458 = the plot card reads cleanly (PFOA below the threshold says
so, the sampling dates as a range, a partial report date hidden, depths without ".0"). HAD-534."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import names_457 as _  # noqa: E402,F401  (no hunk: same module shape)
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["assets/instruments/tools/soilmap.js"]
NEW = []
s = io.open(os.path.join(HERE, "deploy457.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.457)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.458)")')
rep('print("RELEASE 1.72.457 LIVE: the soil page tools without names, with phases and the ask button")', 'print("RELEASE 1.72.458 LIVE: the plot card reads cleanly")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
OLD = "# 1.72.457 (no names): the soil page loads the new map\n"
rep(OLD, "# 1.72.458 (card): the soil page loads the cleaned map (the 457 row now names ?ver=1.72.458)\n" + OLD)
for x, y in (("1.72.457", "1.72.458"), (".bak457", ".bak458"), ("PS457", "PS458"), ("ps457", "ps458"), ("deploy457", "deploy458"),
             ("result-457", "result-458"), ("speed-457", "speed-458"), ("posts-before-457", "posts-before-458"), ("make_deploy457", "make_deploy458")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-456.json")', '_prev = os.path.join(QA, "deploy-result-457.json")'),
             ('"FATAL: release 1.72.456 is still in flight', '"FATAL: release 1.72.457 is still in flight'),
             ('WANT_LIVE = "1.72.456"  # the checks name ?ver=1.72.458: this runner is for the release right after 1.72.456',
              'WANT_LIVE = "1.72.457"  # the checks name ?ver=1.72.458: this runner is for the release right after 1.72.457'),
             ("        for n in range(456, 329, -1):", "        for n in range(457, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy458.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy458.py")
