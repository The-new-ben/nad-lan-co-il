# -*- coding: utf-8 -*-
"""Writes deploy438.py from the released deploy437.py: release 1.72.438 = PriceGuide v2.5 (price_438.py): the city list title
"מחירון ומחשבון: מחיר דירה ב{עיר} לפי חדרים" (the CEO's rule, no H2 twin on the page) and the data of wave 1 (10 cities). The
wave-1 pages carry nothing until insert_city_guides.py runs after the release, so their checks prove they did not move."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_438  # noqa: E402
s = io.open(os.path.join(HERE, "deploy437.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import map_437 as PX  # noqa: E402 (1.72.437: AreaMap v1, the 3D neighbourhood map door)\n",
    "    import price_438 as PX  # noqa: E402 (1.72.438: PriceGuide v2.5, the city titles and wave 1)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.437 area-map hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.438 price-guide wave-1 hunk)")')
rep('print("RELEASE 1.72.437 LIVE: AreaMap v1 (the 3D neighbourhood map door) + PriceGuide v2.4 (the narrow-phone fit)")',
    'print("RELEASE 1.72.438 LIVE: PriceGuide v2.5, the city titles and the wave-1 data")')
rows = []
for c, name in (("tel-aviv", "בתל אביב"), ("jerusalem", "בירושלים"), ("haifa", "בחיפה")):
    rows.append((f"/{c}-apartment-prices/", ["id=\"nlpg\"", f"מחירון ומחשבון: מחיר דירה {name} לפי חדרים"], [f"כמה עולה דירה {name} ב-2026", "[nadlan_price_guide"]))
for slug in ("rainbow-tel-aviv", "dimri-yama-sde-dov", "ashira-sde-dov"):
    rows.append((f"/projects/{slug}/", ["id=\"nlpg\"", "פרויקט חדש בתכנית ל, ממזרח לרובע"], []))
rows.append(("/sde-dov/prices/", ["לפי סקר דוחות היזמים מאפריל 2026"], ["id=\"nlpg\"", "[nadlan_price_guide", "nlpg--fold"]))
for c in price_438.WAVE1:
    rows.append((f"/{c}/", [], ["id=\"nlpg\"", "[nadlan_price_guide"]))
OLD = "# 1.72.437 (AreaMap v1): the door only\n"
rep(OLD, "# 1.72.438 (PriceGuide v2.5): the new city titles, wave 1 served but not yet on its pages\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.437", "1.72.438"), (".bak437", ".bak438"), ("PS437", "PS438"), ("ps437", "ps438"), ("deploy437", "deploy438"),
             ("result-437", "result-438"), ("speed-437", "speed-438"), ("posts-before-437", "posts-before-438"), ("make_deploy437", "make_deploy438")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-436.json")', '_prev = os.path.join(QA, "deploy-result-437.json")'),
             ('"FATAL: release 1.72.436 is still in flight', '"FATAL: release 1.72.437 is still in flight'),
             ('WANT_LIVE = "1.72.436"  # the checks name ?ver=1.72.438: this runner is for the release right after 1.72.436',
              'WANT_LIVE = "1.72.437"  # the checks name ?ver=1.72.438: this runner is for the release right after 1.72.437'),
             ("        for n in range(436, 329, -1):", "        for n in range(437, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy438.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy438.py with", len(rows), "checks")
