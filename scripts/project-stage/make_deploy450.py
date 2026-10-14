# -*- coding: utf-8 -*-
"""Writes deploy450.py from the released deploy449.py: 1.72.450 = the phone fixes of the Instruments (core.css: answer figure
bidi + wrapping text cells; warranty.js: four-column table with the status second). HAD-527 / HAD-533."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fix_450  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["assets/instruments/core.css", "assets/instruments/tools/warranty.js"]
NEW = []
s = io.open(os.path.join(HERE, "deploy449.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import warranty_449 as PX  # noqa: E402 (1.72.449: the warranty tool)\n", "    import fix_450 as PX  # noqa: E402 (1.72.450: Instruments phone fixes)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.449)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.450)")')
rep('print("RELEASE 1.72.449 LIVE: the warranty tool")', 'print("RELEASE 1.72.450 LIVE: Instruments phone fixes (answer bidi, wrapping cells, warranty table)")')
i = s.index("NEWFILES = set(["); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/real-estate-lawyer/construction-defects-lawsuit/", ['data-nli="warranty"', 'tools/warranty.js?ver=1.72.450', 'instruments/core.css?ver=1.72.450'], [])]
OLD = "# 1.72.449 (Instruments turn 4): the warranty tool ships; the rates page keeps its tool\n"
rep(OLD, "# 1.72.450 (Instruments phone fixes): the defects page keeps the warranty tool on the new engine css\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.449", "1.72.450"), (".bak449", ".bak450"), ("PS449", "PS450"), ("ps449", "ps450"), ("deploy449", "deploy450"),
             ("result-449", "result-450"), ("speed-449", "speed-450"), ("posts-before-449", "posts-before-450"), ("make_deploy449", "make_deploy450")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-448.json")', '_prev = os.path.join(QA, "deploy-result-449.json")'),
             ('"FATAL: release 1.72.448 is still in flight', '"FATAL: release 1.72.449 is still in flight'),
             ('WANT_LIVE = "1.72.448"  # the checks name ?ver=1.72.450: this runner is for the release right after 1.72.448',
              'WANT_LIVE = "1.72.449"  # the checks name ?ver=1.72.450: this runner is for the release right after 1.72.449'),
             ("        for n in range(448, 329, -1):", "        for n in range(449, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy450.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy450.py")
