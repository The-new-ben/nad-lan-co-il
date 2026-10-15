# -*- coding: utf-8 -*-
"""Writes deploy454.py from the released deploy453.py: 1.72.454 = the Sde Dov soil map + the PFAS calculator (HAD-534)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import soil_454  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["inc/instruments.php", "assets/instruments/core.js", "assets/instruments/core.css", "assets/instruments/tools/soilmap.js",
         "assets/instruments/tools/pfas.js", "assets/instruments/data/sde-dov-soil.json"]
NEW = ["assets/instruments/tools/soilmap.js", "assets/instruments/tools/pfas.js", "assets/instruments/data/sde-dov-soil.json"]
s = io.open(os.path.join(HERE, "deploy453.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import fix_453 as PX  # noqa: E402 (1.72.453: phone tables of indexation and delay)\n", "    import soil_454 as PX  # noqa: E402 (1.72.454: the Sde Dov soil map + PFAS calculator)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.453)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.454)")')
rep('print("RELEASE 1.72.453 LIVE: the indexation and delay tables fit a phone")', 'print("RELEASE 1.72.454 LIVE: the Sde Dov soil map and the PFAS calculator (the page comes next)")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/new-projects/construction-input-index/", ['data-nli="indexation"', 'instruments/core.js?ver=1.72.454', 'instruments/core.css?ver=1.72.454'], [])]
OLD = "# 1.72.453 (phone tables): the delay page loads the new delay.js\n"
rep(OLD, "# 1.72.454 (soil map): the tool pages load the new engine; the soil page is created after the release\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.453", "1.72.454"), (".bak453", ".bak454"), ("PS453", "PS454"), ("ps453", "ps454"), ("deploy453", "deploy454"),
             ("result-453", "result-454"), ("speed-453", "speed-454"), ("posts-before-453", "posts-before-454"), ("make_deploy453", "make_deploy454")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-452.json")', '_prev = os.path.join(QA, "deploy-result-453.json")'),
             ('"FATAL: release 1.72.452 is still in flight', '"FATAL: release 1.72.453 is still in flight'),
             ('WANT_LIVE = "1.72.452"  # the checks name ?ver=1.72.454: this runner is for the release right after 1.72.452',
              'WANT_LIVE = "1.72.453"  # the checks name ?ver=1.72.454: this runner is for the release right after 1.72.453'),
             ("        for n in range(452, 329, -1):", "        for n in range(453, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy454.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy454.py")
