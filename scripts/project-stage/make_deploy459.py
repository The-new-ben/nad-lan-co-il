# -*- coding: utf-8 -*-
"""Writes deploy459.py from the released deploy458.py: 1.72.459 = Mission A v1 (Ben 15.10): every project in marketing in the
district as a GREEN schematic building on the soil map (a low base on its lot + the main tower at its published height), nameless
project cards with the published facts and the ask button, phases derived from our project pages (plot 106 corrected), no
"nearest exceedance" line, a numbers-only search. Files: tools/soilmap.js, core.css, data/sde-dov-soil.json. HAD-534."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import names_457 as _  # noqa: E402,F401  (no hunk: same module shape)
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["assets/instruments/core.css", "assets/instruments/tools/soilmap.js", "assets/instruments/data/sde-dov-soil.json"]
NEW = []
s = io.open(os.path.join(HERE, "deploy458.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.458)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.459)")')
rep('print("RELEASE 1.72.458 LIVE: the plot card reads cleanly")', 'print("RELEASE 1.72.459 LIVE: green project buildings on the soil map")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
OLD = "# 1.72.458 (card): the soil page loads the cleaned map (the 457 row now names ?ver=1.72.458)\n"
rep(OLD, "# 1.72.459 (green buildings): the soil page loads the new map (the 457 row now names ?ver=1.72.459)\n" + OLD)
for x, y in (("1.72.458", "1.72.459"), (".bak458", ".bak459"), ("PS458", "PS459"), ("ps458", "ps459"), ("deploy458", "deploy459"),
             ("result-458", "result-459"), ("speed-458", "speed-459"), ("posts-before-458", "posts-before-459"), ("make_deploy458", "make_deploy459")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-457.json")', '_prev = os.path.join(QA, "deploy-result-458.json")'),
             ('"FATAL: release 1.72.457 is still in flight', '"FATAL: release 1.72.458 is still in flight'),
             ('WANT_LIVE = "1.72.457"  # the checks name ?ver=1.72.459: this runner is for the release right after 1.72.457',
              'WANT_LIVE = "1.72.458"  # the checks name ?ver=1.72.459: this runner is for the release right after 1.72.458'),
             ("        for n in range(457, 329, -1):", "        for n in range(458, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy459.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy459.py")
