# -*- coding: utf-8 -*-
"""Writes deploy455.py from the released deploy454.py: 1.72.455 = the questions-to-the-developer generator (HAD-534)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ask_455  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["inc/instruments.php", "assets/instruments/core.js", "assets/instruments/core.css", "assets/instruments/tools/soilask.js"]
NEW = ["assets/instruments/tools/soilask.js"]
s = io.open(os.path.join(HERE, "deploy454.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import soil_454 as PX  # noqa: E402 (1.72.454: the Sde Dov soil map + PFAS calculator)\n", "    import ask_455 as PX  # noqa: E402 (1.72.455: the questions-to-the-developer generator)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.454)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.455)")')
rep('print("RELEASE 1.72.454 LIVE: the Sde Dov soil map and the PFAS calculator (the page comes next)")', 'print("RELEASE 1.72.455 LIVE: the questions-to-the-developer generator (placed on the soil page next)")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/sde-dov/contamination/", ['data-nli="soilmap"', 'data-nli="pfas"', 'instruments/core.js?ver=1.72.455', 'tools/soilmap.js?ver=1.72.455'], [])]
OLD = "# 1.72.454 (soil map): the tool pages load the new engine; the soil page is created after the release\n"
rep(OLD, "# 1.72.455 (letter generator): the soil page keeps its tools on the new engine\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.454", "1.72.455"), (".bak454", ".bak455"), ("PS454", "PS455"), ("ps454", "ps455"), ("deploy454", "deploy455"),
             ("result-454", "result-455"), ("speed-454", "speed-455"), ("posts-before-454", "posts-before-455"), ("make_deploy454", "make_deploy455")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-453.json")', '_prev = os.path.join(QA, "deploy-result-454.json")'),
             ('"FATAL: release 1.72.453 is still in flight', '"FATAL: release 1.72.454 is still in flight'),
             ('WANT_LIVE = "1.72.453"  # the checks name ?ver=1.72.455: this runner is for the release right after 1.72.453',
              'WANT_LIVE = "1.72.454"  # the checks name ?ver=1.72.455: this runner is for the release right after 1.72.454'),
             ("        for n in range(453, 329, -1):", "        for n in range(454, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy455.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy455.py")
