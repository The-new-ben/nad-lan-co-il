# -*- coding: utf-8 -*-
"""Writes deploy447.py from deploy446.py: 1.72.447 = the CPI tool + engine fixes + aligned data (HAD-527 turn 2)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cpi_447  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["inc/instruments.php", "assets/instruments/core.css", "assets/instruments/core.js", "assets/instruments/tools/cpi.js",
         "assets/instruments/data/cbs-200010.json", "assets/instruments/data/cbs-120010.json"]
NEW = ["assets/instruments/tools/cpi.js"]
s = io.open(os.path.join(HERE, "deploy446.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import fix_446 as PX  # noqa: E402 (1.72.446: the Instruments asset URLs)\n", "    import cpi_447 as PX  # noqa: E402 (1.72.447: the CPI tool)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.446)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.447)")')
rep('print("RELEASE 1.72.446 LIVE: the Instruments asset URLs fixed")', 'print("RELEASE 1.72.447 LIVE: the CPI tool, aligned CBS data, engine fixes")')
rep("NEWFILES = set([])\nFILES = ['inc/instruments.php']\n", "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n")
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/new-projects/construction-input-index/", ['data-nli="indexation"', 'tools/indexation.js?ver=1.72.447'], [])]
OLD = "# 1.72.446 (Instruments, HAD-527): the engine ships; no page carries a tool yet\n"
rep(OLD, "# 1.72.447 (Instruments turn 2): the CPI tool ships; the page comes after\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.446", "1.72.447"), (".bak446", ".bak447"), ("PS446", "PS447"), ("ps446", "ps447"), ("deploy446", "deploy447"),
             ("result-446", "result-447"), ("speed-446", "speed-447"), ("posts-before-446", "posts-before-447"), ("make_deploy446", "make_deploy447")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-445.json")', '_prev = os.path.join(QA, "deploy-result-446.json")'),
             ('"FATAL: release 1.72.445 is still in flight', '"FATAL: release 1.72.446 is still in flight'),
             ('WANT_LIVE = "1.72.445"  # the checks name ?ver=1.72.447: this runner is for the release right after 1.72.445',
              'WANT_LIVE = "1.72.446"  # the checks name ?ver=1.72.447: this runner is for the release right after 1.72.446'),
             ("        for n in range(445, 329, -1):", "        for n in range(446, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy447.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy447.py")
