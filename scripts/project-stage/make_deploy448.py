# -*- coding: utf-8 -*-
"""Writes deploy448.py from the released deploy447.py: 1.72.448 = the prime tool (prime.js + boi-rate.json, new) and the woven
related links in inc/instruments.php (HAD-527 turn 3)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import prime_448  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["inc/instruments.php", "assets/instruments/tools/prime.js", "assets/instruments/data/boi-rate.json"]
NEW = ["assets/instruments/tools/prime.js", "assets/instruments/data/boi-rate.json"]
s = io.open(os.path.join(HERE, "deploy447.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import cpi_447 as PX  # noqa: E402 (1.72.447: the CPI tool)\n", "    import prime_448 as PX  # noqa: E402 (1.72.448: the prime tool)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.447)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.448)")')
rep('print("RELEASE 1.72.447 LIVE: the CPI tool, aligned CBS data, engine fixes")', 'print("RELEASE 1.72.448 LIVE: the prime tool and the woven tool links")')
i = s.index("NEWFILES = set(["); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/cpi-calculator/", ['data-nli="cpi"', 'tools/cpi.js?ver=1.72.448', '/mortgage-calculator/mortgage-interest-rates/'], [])]
OLD = "# 1.72.447 (Instruments turn 2): the CPI tool ships; the page comes after\n"
rep(OLD, "# 1.72.448 (Instruments turn 3): the prime tool ships; the cpi page links the rates page\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.447", "1.72.448"), (".bak447", ".bak448"), ("PS447", "PS448"), ("ps447", "ps448"), ("deploy447", "deploy448"),
             ("result-447", "result-448"), ("speed-447", "speed-448"), ("posts-before-447", "posts-before-448"), ("make_deploy447", "make_deploy448")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-446.json")', '_prev = os.path.join(QA, "deploy-result-447.json")'),
             ('"FATAL: release 1.72.446 is still in flight', '"FATAL: release 1.72.447 is still in flight'),
             ('WANT_LIVE = "1.72.446"  # the checks name ?ver=1.72.448: this runner is for the release right after 1.72.446',
              'WANT_LIVE = "1.72.447"  # the checks name ?ver=1.72.448: this runner is for the release right after 1.72.447'),
             ("        for n in range(446, 329, -1):", "        for n in range(447, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy448.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy448.py")
