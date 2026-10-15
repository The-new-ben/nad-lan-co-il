# -*- coding: utf-8 -*-
"""Writes deploy460.py from the released deploy459.py: 1.72.460 = the soil guard (Ben 15.10.2026): nothing about the soil
tests on any project page, in any language, enforced by the plugin (inc/soil-guard.php, new, loaded from inc/instruments.php).
The 8 pages that carried it (Ashira and Dimri Yama in en/fr/ru/ar) were cleaned in the CMS the same day."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import names_457 as _  # noqa: E402,F401  (no hunk: same module shape)
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = ["inc/instruments.php", "inc/soil-guard.php"]
NEW = ["inc/soil-guard.php"]
s = io.open(os.path.join(HERE, "deploy459.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.459)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.460)")')
rep('print("RELEASE 1.72.459 LIVE: green project buildings on the soil map")', 'print("RELEASE 1.72.460 LIVE: the soil guard on every project page")')
i = s.index("NEWFILES = set("); j = s.index("\n", s.index("\nFILES = [", i) + 1)
s = s[:i] + "NEWFILES = set(" + repr(NEW) + ")\nFILES = " + repr(FILES) + "\n" + s[j:]
i = s.index("PIN = {"); j = s.index("\n", i)
s = s[:i] + "PIN = " + repr(pin) + s[j:]
rows = [("/projects/dimri-yama-sde-dov-en/", ["<h1"], ["PFAS", "contaminat"]), ("/projects/ashira-sde-dov-ru/", ["<h1"], ["PFAS"])]
OLD = "# 1.72.459 (green buildings): the soil page loads the new map (the 457 row now names ?ver=1.72.459)\n"
rep(OLD, "# 1.72.460 (soil guard): no project page carries the soil subject\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.459", "1.72.460"), (".bak459", ".bak460"), ("PS459", "PS460"), ("ps459", "ps460"), ("deploy459", "deploy460"),
             ("result-459", "result-460"), ("speed-459", "speed-460"), ("posts-before-459", "posts-before-460"), ("make_deploy459", "make_deploy460")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-458.json")', '_prev = os.path.join(QA, "deploy-result-459.json")'),
             ('"FATAL: release 1.72.458 is still in flight', '"FATAL: release 1.72.459 is still in flight'),
             ('WANT_LIVE = "1.72.458"  # the checks name ?ver=1.72.460: this runner is for the release right after 1.72.458',
              'WANT_LIVE = "1.72.459"  # the checks name ?ver=1.72.460: this runner is for the release right after 1.72.459'),
             ("        for n in range(458, 329, -1):", "        for n in range(459, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy460.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy460.py")
