# -*- coding: utf-8 -*-
"""Writes deploy442.py from the released deploy441.py: release 1.72.442 = data only (data_442.py): the Sde Dov price list and map
in en/fr/ru/ar. Checks: the Hebrew Sde Dov pages and the live language pages keep their components; nothing else moved."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import data_442  # noqa: E402,F401
s = io.open(os.path.join(HERE, "deploy441.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import price_441 as PX  # noqa: E402 (1.72.441: PriceGuide v2.7, small fixes and the shortcode language)\n",
    "    import data_442 as PX  # noqa: E402 (1.72.442: data only, the Sde Dov components in four languages)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.441 price-guide v2.7 hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.442 data hunk)")')
rep('print("RELEASE 1.72.441 LIVE: PriceGuide v2.7, small fixes and the shortcode language")',
    'print("RELEASE 1.72.442 LIVE: data only, the Sde Dov price list and map in four languages")')
rows = [("/sde-dov/prices/", ['id="nlpg"', 'nlds nlpg nlpg--fold', 'lang="he"'], []),
        ("/sde-dov/", ['class="nlds nlam"', 'lang="he"'], []),
        ("/en/north-tel-aviv/rova-4/", ['id="nlpg"', 'lang="en"', 'class="nlds nlam"'], ['[nadlan_']),
        ("/ar/north-tel-aviv/rova-4/", ['id="nlpg"', 'lang="ar"', 'class="nlds nlam"'], ['[nadlan_'])]
OLD = "# 1.72.441 (PriceGuide v2.7): small fixes and the shortcode language door\n"
rep(OLD, "# 1.72.442 (data only): the Sde Dov components in four languages\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.441", "1.72.442"), (".bak441", ".bak442"), ("PS441", "PS442"), ("ps441", "ps442"), ("deploy441", "deploy442"),
             ("result-441", "result-442"), ("speed-441", "speed-442"), ("posts-before-441", "posts-before-442"), ("make_deploy441", "make_deploy442")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-440.json")', '_prev = os.path.join(QA, "deploy-result-441.json")'),
             ('"FATAL: release 1.72.440 is still in flight', '"FATAL: release 1.72.441 is still in flight'),
             ('WANT_LIVE = "1.72.440"  # the checks name ?ver=1.72.442: this runner is for the release right after 1.72.440',
              'WANT_LIVE = "1.72.441"  # the checks name ?ver=1.72.442: this runner is for the release right after 1.72.441'),
             ("        for n in range(440, 329, -1):", "        for n in range(441, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy442.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy442.py with", len(rows), "new checks")
