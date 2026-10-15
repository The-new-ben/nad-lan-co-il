# -*- coding: utf-8 -*-
"""Writes deploy457.py from the released deploy456.py: 1.72.457 = the soil page without names, with plot phases and the
ask-for-details button (HAD-534)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import names_457  # noqa: E402,F401
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["inc/instruments.php", "assets/instruments/core.css", "assets/instruments/tools/soilmap.js", "assets/instruments/tools/soilask.js",
         "assets/instruments/data/sde-dov-soil.json"]
NEW = []
s = io.open(os.path.join(HERE, "deploy456.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep("    import faq_456 as PX  # noqa: E402 (1.72.456: FAQPage JSON-LD on Instruments pages)\n", "    import names_457 as PX  # noqa: E402 (1.72.457: the soil page without names)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.456)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.457)")')
rep('print("RELEASE 1.72.456 LIVE: FAQPage JSON-LD on Instruments pages")', 'print("RELEASE 1.72.457 LIVE: the soil page tools without names, with phases and the ask button")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/sde-dov/contamination/", ['tools/soilmap.js?ver=1.72.457', 'data-nli="soilask"'], [])]
OLD = "# 1.72.456 (FAQPage): the soil page carries its FAQ as JSON-LD\n"
rep(OLD, "# 1.72.457 (no names): the soil page loads the new map\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.456", "1.72.457"), (".bak456", ".bak457"), ("PS456", "PS457"), ("ps456", "ps457"), ("deploy456", "deploy457"),
             ("result-456", "result-457"), ("speed-456", "speed-457"), ("posts-before-456", "posts-before-457"), ("make_deploy456", "make_deploy457")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-455.json")', '_prev = os.path.join(QA, "deploy-result-456.json")'),
             ('"FATAL: release 1.72.455 is still in flight', '"FATAL: release 1.72.456 is still in flight'),
             ('WANT_LIVE = "1.72.455"  # the checks name ?ver=1.72.457: this runner is for the release right after 1.72.455',
              'WANT_LIVE = "1.72.456"  # the checks name ?ver=1.72.457: this runner is for the release right after 1.72.456'),
             ("        for n in range(455, 329, -1):", "        for n in range(456, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy457.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy457.py")
