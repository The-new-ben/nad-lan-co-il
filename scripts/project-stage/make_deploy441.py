# -*- coding: utf-8 -*-
"""Writes deploy441.py from the released deploy440.py: release 1.72.441 = PriceGuide v2.7 (price_441.py). Checks: the Rova 4 chart
title, the spacing and the islands in the script, and nothing else moved (run pretest_checks.py first)."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_441  # noqa: E402,F401
s = io.open(os.path.join(HERE, "deploy440.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import map_440 as PX  # noqa: E402 (1.72.440: AreaMap v1.1, languages and the Sde Dov instance)\n",
    "    import price_441 as PX  # noqa: E402 (1.72.441: PriceGuide v2.7, small fixes and the shortcode language)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.440 area-map v1.1 hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.441 price-guide v2.7 hunk)")')
rep('print("RELEASE 1.72.440 LIVE: AreaMap v1.1, languages and the Sde Dov instance")',
    'print("RELEASE 1.72.441 LIVE: PriceGuide v2.7, small fixes and the shortcode language")')
# the Sde Dov hub got its map after 440: the inherited row now expects it
rep("('/sde-dov/', [], ['class=\"nlds nlam\"', '[nadlan_area_map'])",
    "('/sde-dov/', ['class=\"nlds nlam\"'], ['[nadlan_area_map'])")
rows = [("/north-tel-aviv/rova-4/", ["המחיר למ״ר לבחירה שלכם, מול ממוצע מגדלי כיכר המדינה", "24+i*42", "q('why').innerHTML=esc(m.why)"], ["[nadlan_price_guide"]),
        ("/projects/hamedina/", ['id="nlpg"', "24+i*42"], [])]
OLD = "# 1.72.440 (AreaMap v1.1): the map's languages and the Sde Dov instance served\n"
rep(OLD, "# 1.72.441 (PriceGuide v2.7): small fixes and the shortcode language door\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.440", "1.72.441"), (".bak440", ".bak441"), ("PS440", "PS441"), ("ps440", "ps441"), ("deploy440", "deploy441"),
             ("result-440", "result-441"), ("speed-440", "speed-441"), ("posts-before-440", "posts-before-441"), ("make_deploy440", "make_deploy441")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-439.json")', '_prev = os.path.join(QA, "deploy-result-440.json")'),
             ('"FATAL: release 1.72.439 is still in flight', '"FATAL: release 1.72.440 is still in flight'),
             ('WANT_LIVE = "1.72.439"  # the checks name ?ver=1.72.441: this runner is for the release right after 1.72.439',
              'WANT_LIVE = "1.72.440"  # the checks name ?ver=1.72.441: this runner is for the release right after 1.72.440'),
             ("        for n in range(439, 329, -1):", "        for n in range(440, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy441.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy441.py with", len(rows), "new checks")
