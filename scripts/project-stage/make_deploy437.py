# -*- coding: utf-8 -*-
"""Writes deploy437.py from the released deploy436.py: release 1.72.437 = AreaMap v1 (map_437.py), the 3D neighbourhood map door
[nadlan_area_map key="rova-4"]. The Rova 4 page gets the shortcode after this release (insert_area_map_rova4.py). Checks: nothing
else moved (the inherited set), the Kikar page still carries its price guide, and no page carries the map yet."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import map_437  # noqa: E402,F401
s = io.open(os.path.join(HERE, "deploy436.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import price_436 as PX  # noqa: E402 (1.72.436: PriceGuide v2.3, the rooms variant for city pages)\n",
    "    import map_437 as PX  # noqa: E402 (1.72.437: AreaMap v1, the 3D neighbourhood map door)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.436 price-guide city hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.437 area-map hunk)")')
rep('print("RELEASE 1.72.436 LIVE: PriceGuide v2.3, the rooms variant for the city price pages")',
    'print("RELEASE 1.72.437 LIVE: AreaMap v1, the 3D neighbourhood map door")')
# 1.72.436 patched the language dictionary too; 1.72.437 patches only inc/project-stage.php (a rollback restores what it wrote)
rep("PHP_RELS = ['inc/project-stage.php', 'i18n/lang-pages.json']", "PHP_RELS = ['inc/project-stage.php']")
# after 1.72.436 insert_city_guides.py put the price list on the three test cities: the inherited rows now expect it
for _c in ("tel-aviv", "jerusalem", "haifa"):
    rep(f"('/{_c}-apartment-prices/', [], ['id=\"nlpg\"', '[nadlan_price_guide'])",
        f"('/{_c}-apartment-prices/', ['id=\"nlpg\"', 'nlpg--rooms'], ['[nadlan_price_guide'])")
# H Infinity has no stage block: its price list sits in the article (insert_city_guides.py --project), after the lead paragraph
rep("('/projects/h-infinity-somail-tel-aviv/', [], ['id=\"nlpg\"'])",
    "('/projects/h-infinity-somail-tel-aviv/', ['id=\"nlpg\"', 'כמה עולה דירה במגדל אינפיניטי'], ['[nadlan_price_guide'])")
rows = [("/projects/hamedina/", ['id="nlpg"'], ['id="nlam"']), ("/north-tel-aviv/rova-4/", ['id="nlpg"'], ['[nadlan_area_map'])]
OLD = "# 1.72.436 (PriceGuide v2.3): the rooms variant is served, the city pages unchanged until the shortcode\n"
rep(OLD, "# 1.72.437 (AreaMap v1): the door only\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.436", "1.72.437"), (".bak436", ".bak437"), ("PS436", "PS437"), ("ps436", "ps437"), ("deploy436", "deploy437"),
             ("result-436", "result-437"), ("speed-436", "speed-437"), ("posts-before-436", "posts-before-437"), ("make_deploy436", "make_deploy437")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-435.json")', '_prev = os.path.join(QA, "deploy-result-436.json")'),
             ('"FATAL: release 1.72.435 is still in flight', '"FATAL: release 1.72.436 is still in flight'),
             ('WANT_LIVE = "1.72.435"  # the checks name ?ver=1.72.437: this runner is for the release right after 1.72.435',
              'WANT_LIVE = "1.72.436"  # the checks name ?ver=1.72.437: this runner is for the release right after 1.72.436'),
             ("        for n in range(435, 329, -1):", "        for n in range(436, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy437.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy437.py with", len(rows), "checks")
