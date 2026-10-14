# -*- coding: utf-8 -*-
"""Writes deploy449.py from the released deploy448.py: 1.72.449 = the warranty tool (warranty.js, new) and its registry
entry + summary in inc/instruments.php (HAD-527 turn 4)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import warranty_449  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["inc/instruments.php", "assets/instruments/tools/warranty.js"]
NEW = ["assets/instruments/tools/warranty.js"]
s = io.open(os.path.join(HERE, "deploy448.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import prime_448 as PX  # noqa: E402 (1.72.448: the prime tool)\n", "    import warranty_449 as PX  # noqa: E402 (1.72.449: the warranty tool)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.448)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.449)")')
rep('print("RELEASE 1.72.448 LIVE: the prime tool and the woven tool links")', 'print("RELEASE 1.72.449 LIVE: the warranty tool")')
i = s.index("NEWFILES = set(["); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/mortgage-calculator/mortgage-interest-rates/", ['data-nli="prime"', 'tools/prime.js?ver=1.72.449'], [])]
OLD = "# 1.72.448 (Instruments turn 3): the prime tool ships; the cpi page links the rates page\n"
rep(OLD, "# 1.72.449 (Instruments turn 4): the warranty tool ships; the rates page keeps its tool\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.448", "1.72.449"), (".bak448", ".bak449"), ("PS448", "PS449"), ("ps448", "ps449"), ("deploy448", "deploy449"),
             ("result-448", "result-449"), ("speed-448", "speed-449"), ("posts-before-448", "posts-before-449"), ("make_deploy448", "make_deploy449")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-447.json")', '_prev = os.path.join(QA, "deploy-result-448.json")'),
             ('"FATAL: release 1.72.447 is still in flight', '"FATAL: release 1.72.448 is still in flight'),
             ('WANT_LIVE = "1.72.447"  # the checks name ?ver=1.72.449: this runner is for the release right after 1.72.447',
              'WANT_LIVE = "1.72.448"  # the checks name ?ver=1.72.449: this runner is for the release right after 1.72.448'),
             ("        for n in range(447, 329, -1):", "        for n in range(448, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy449.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy449.py")
