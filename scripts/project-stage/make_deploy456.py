# -*- coding: utf-8 -*-
"""Writes deploy456.py from the released deploy455.py: 1.72.456 = FAQPage JSON-LD on Instruments pages (HAD-534)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import faq_456  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["inc/instruments.php"]
NEW = []
s = io.open(os.path.join(HERE, "deploy455.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import ask_455 as PX  # noqa: E402 (1.72.455: the questions-to-the-developer generator)\n", "    import faq_456 as PX  # noqa: E402 (1.72.456: FAQPage JSON-LD on Instruments pages)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.455)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.456)")')
rep('print("RELEASE 1.72.455 LIVE: the questions-to-the-developer generator (placed on the soil page next)")', 'print("RELEASE 1.72.456 LIVE: FAQPage JSON-LD on Instruments pages")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/sde-dov/contamination/", ['"@type":"FAQPage"', 'data-nli="soilask"'], [])]
OLD = "# 1.72.455 (letter generator): the soil page keeps its tools on the new engine\n"
rep(OLD, "# 1.72.456 (FAQPage): the soil page carries its FAQ as JSON-LD\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.455", "1.72.456"), (".bak455", ".bak456"), ("PS455", "PS456"), ("ps455", "ps456"), ("deploy455", "deploy456"),
             ("result-455", "result-456"), ("speed-455", "speed-456"), ("posts-before-455", "posts-before-456"), ("make_deploy455", "make_deploy456")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-454.json")', '_prev = os.path.join(QA, "deploy-result-455.json")'),
             ('"FATAL: release 1.72.454 is still in flight', '"FATAL: release 1.72.455 is still in flight'),
             ('WANT_LIVE = "1.72.454"  # the checks name ?ver=1.72.456: this runner is for the release right after 1.72.454',
              'WANT_LIVE = "1.72.455"  # the checks name ?ver=1.72.456: this runner is for the release right after 1.72.455'),
             ("        for n in range(454, 329, -1):", "        for n in range(455, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy456.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy456.py")
