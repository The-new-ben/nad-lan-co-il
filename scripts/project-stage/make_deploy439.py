# -*- coding: utf-8 -*-
"""Writes deploy439.py from the released deploy438.py: release 1.72.439 = PriceGuide v2.6 (price_439.py): wave 2 of the city
lists and the national variant for /apartment-prices/. The inherited 438 rows that forbade a list on wave 1 and on Sde Dov flip
(those pages got their lists after 438); wave 2 and the Israel page carry nothing until insert_city_guides.py runs."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_438  # noqa: E402
import price_439  # noqa: E402
s = io.open(os.path.join(HERE, "deploy438.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import price_438 as PX  # noqa: E402 (1.72.438: PriceGuide v2.5, the city titles and wave 1)\n",
    "    import price_439 as PX  # noqa: E402 (1.72.439: PriceGuide v2.6, wave 2 and the national variant)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.438 price-guide wave-1 hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.439 price-guide wave-2 hunk)")')
rep('print("RELEASE 1.72.438 LIVE: PriceGuide v2.5, the city titles and the wave-1 data")',
    'print("RELEASE 1.72.439 LIVE: PriceGuide v2.6, wave 2 and the national variant")')
# after 438 the wave-1 pages and Sde Dov got their lists: the inherited rows now expect them
for c in price_438.WAVE1:
    rep(f"('/{c}/', [], ['id=\"nlpg\"', '[nadlan_price_guide'])", f"('/{c}/', ['id=\"nlpg\"', 'nlpg--rooms', 'מחירון ומחשבון: מחיר דירה ב'], ['[nadlan_price_guide'])")
rep("('/sde-dov/prices/', ['לפי סקר דוחות היזמים מאפריל 2026'], ['id=\"nlpg\"', '[nadlan_price_guide', 'nlpg--fold'])",
    "('/sde-dov/prices/', ['לפי סקר דוחות היזמים מאפריל 2026', 'id=\"nlpg\"', 'nlds nlpg nlpg--fold', 'מחירון הדירות בשדה דב לפי פרויקט'], ['[nadlan_price_guide'])")
rows = [(f"/{c}/", [], ["id=\"nlpg\"", "[nadlan_price_guide"]) for c in price_439.WAVE2]
rows.append(("/apartment-prices/", [], ["id=\"nlpg\"", "[nadlan_price_guide"]))
rows.append(("/herzliya-apartment-prices/", ["nlpg--rooms", ".nlpg--national"], []))  # the national CSS is served with the shared assets
OLD = "# 1.72.438 (PriceGuide v2.5): the new city titles, wave 1 served but not yet on its pages\n"
rep(OLD, "# 1.72.439 (PriceGuide v2.6): wave 2 and the national variant served, not yet on their pages\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.438", "1.72.439"), (".bak438", ".bak439"), ("PS438", "PS439"), ("ps438", "ps439"), ("deploy438", "deploy439"),
             ("result-438", "result-439"), ("speed-438", "speed-439"), ("posts-before-438", "posts-before-439"), ("make_deploy438", "make_deploy439")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-437.json")', '_prev = os.path.join(QA, "deploy-result-438.json")'),
             ('"FATAL: release 1.72.437 is still in flight', '"FATAL: release 1.72.438 is still in flight'),
             ('WANT_LIVE = "1.72.437"  # the checks name ?ver=1.72.439: this runner is for the release right after 1.72.437',
              'WANT_LIVE = "1.72.438"  # the checks name ?ver=1.72.439: this runner is for the release right after 1.72.438'),
             ("        for n in range(437, 329, -1):", "        for n in range(438, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy439.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy439.py with", len(rows), "new checks")
