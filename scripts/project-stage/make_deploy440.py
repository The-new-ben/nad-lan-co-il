# -*- coding: utf-8 -*-
"""Writes deploy440.py from the released deploy439.py: release 1.72.440 = AreaMap v1.1 (map_440.py): languages, no empty layer,
the card title aligned, the Sde Dov instance. Rova 4 keeps its map (now with the logical-margin title rule); /sde-dov/ carries no
map until insert_area_map runs after the release."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import map_440  # noqa: E402,F401
s = io.open(os.path.join(HERE, "deploy439.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import price_439 as PX  # noqa: E402 (1.72.439: PriceGuide v2.6, wave 2 and the national variant)\n",
    "    import map_440 as PX  # noqa: E402 (1.72.440: AreaMap v1.1, languages and the Sde Dov instance)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.439 price-guide wave-2 hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.440 area-map v1.1 hunk)")')
rep('print("RELEASE 1.72.439 LIVE: PriceGuide v2.6, wave 2 and the national variant")',
    'print("RELEASE 1.72.440 LIVE: AreaMap v1.1, languages and the Sde Dov instance")')
# after 439 the wave-2 pages and the Israel page got their lists: the inherited "not yet on its page" rows now expect them
import price_439  # noqa: E402
for c in price_439.WAVE2:
    rep(f"('/{c}/', [], ['id=\"nlpg\"', '[nadlan_price_guide'])", f"('/{c}/', ['id=\"nlpg\"', 'nlpg--rooms', 'מחירון ומחשבון: מחיר דירה ב'], ['[nadlan_price_guide'])")
rep("('/apartment-prices/', [], ['id=\"nlpg\"', '[nadlan_price_guide'])",
    "('/apartment-prices/', ['id=\"nlpg\"', 'nlds nlpg nlpg--national', 'מחירון דירות לפי'], ['[nadlan_price_guide', 'class=\"nlpg__calc'])")
rows = [("/north-tel-aviv/rova-4/", ['class="nlds nlam"', 'margin-inline-end:34px', 'התחדשות עירונית', 'id="nlpg"'], ['[nadlan_area_map']),
        ("/sde-dov/", [], ['class="nlds nlam"', '[nadlan_area_map']),
        ("/projects/hamedina/", ['id="nlpg"'], ['class="nlds nlam"'])]
OLD = "# 1.72.439 (PriceGuide v2.6): wave 2 and the national variant served, not yet on their pages\n"
rep(OLD, "# 1.72.440 (AreaMap v1.1): the map's languages and the Sde Dov instance served\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.439", "1.72.440"), (".bak439", ".bak440"), ("PS439", "PS440"), ("ps439", "ps440"), ("deploy439", "deploy440"),
             ("result-439", "result-440"), ("speed-439", "speed-440"), ("posts-before-439", "posts-before-440"), ("make_deploy439", "make_deploy440")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-438.json")', '_prev = os.path.join(QA, "deploy-result-439.json")'),
             ('"FATAL: release 1.72.438 is still in flight', '"FATAL: release 1.72.439 is still in flight'),
             ('WANT_LIVE = "1.72.438"  # the checks name ?ver=1.72.440: this runner is for the release right after 1.72.438',
              'WANT_LIVE = "1.72.439"  # the checks name ?ver=1.72.440: this runner is for the release right after 1.72.439'),
             ("        for n in range(438, 329, -1):", "        for n in range(439, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy440.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy440.py with", len(rows), "new checks")
