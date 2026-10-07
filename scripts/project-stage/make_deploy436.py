# -*- coding: utf-8 -*-
"""Writes deploy436.py from the released deploy435.py: release 1.72.436 = PriceGuide v2.3 (price_436.py), the rooms variant and
the data of three test cities for the shortcode door. No page shows the city section until the shortcode is inserted after this
release, so the checks prove the build is served (the rooms CSS and script on a page with a price guide) and nothing else moved."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_436  # noqa: E402,F401
s = io.open(os.path.join(HERE, "deploy435.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import price_435 as PX  # noqa: E402 (1.72.435: PriceGuide v2.2, Dimri Yama and Ashira)\n",
    "    import price_436 as PX  # noqa: E402 (1.72.436: PriceGuide v2.3, the rooms variant for city pages)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.435 price-guide data hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.436 price-guide city hunk)")')
rep('print("RELEASE 1.72.435 LIVE: PriceGuide v2.2, Dimri Yama and Ashira")',
    'print("RELEASE 1.72.436 LIVE: PriceGuide v2.3, the rooms variant for the city price pages")')
# the 7.10 card H2 (snippet 661) and its city price link, translated on the language pages by the new lang-pages.json; Hebrew there is a fail
_HEB = "<h2>המחירים סביב הפרויקט ב"  # the visible H2 only: a language page embeds the whole dictionary (its Hebrew keys) in a script
rep("'What does an apartment cost in Tel Aviv-Yafo?', 'Price: where the project stands against its area', 'Everything around the project', 'Accessibility statement', 'nadlan-project-article'], ['aria-label=\"מחירי הסביבה\"']",
    "'Prices around the project in Tel Aviv-Yafo', 'Apartment prices in Tel Aviv-Yafo', 'Price: where the project stands against its area', 'Everything around the project', 'Accessibility statement', 'nadlan-project-article'], ['aria-label=\"מחירי הסביבה\"', '" + _HEB + "', '\">מחירי דירות ב']")
rep("'كم يبلغ سعر شقة في تل أبيب يافا؟', 'nadlan-project-article'], ['aria-label=\"מחירי הסביבה\"']",
    "'الأسعار حول المشروع في تل أبيب يافا', 'nadlan-project-article'], ['aria-label=\"מחירי הסביבה\"', '" + _HEB + "']")
rep("'Сколько стоит квартира в городе Тель-Авив-Яффо?'], ['aria-label=\"מחירי הסביבה\"']",
    "'Цены вокруг проекта в городе Тель-Авив-Яффо'], ['aria-label=\"מחירי הסביבה\"', '" + _HEB + "']")
rows = [("/projects/hamedina/", ['nlpg__in-price', ".nlpg--rooms')", 'id="nlpg"'], []),
        ("/tel-aviv-apartment-prices/", [], ['id="nlpg"', '[nadlan_price_guide']),
        ("/jerusalem-apartment-prices/", [], ['id="nlpg"', '[nadlan_price_guide']),
        ("/haifa-apartment-prices/", [], ['id="nlpg"', '[nadlan_price_guide'])]
OLD = "# 1.72.435 (PriceGuide v2.2): Dimri Yama, Ashira, fixes\n"
rep(OLD, "# 1.72.436 (PriceGuide v2.3): the rooms variant is served, the city pages unchanged until the shortcode\nCHECKS += " + repr(rows) + "\n" + OLD)
rep("PHP_RELS = ['inc/project-stage.php']", "PHP_RELS = ['inc/project-stage.php', 'i18n/lang-pages.json']")
for x, y in (("1.72.435", "1.72.436"), (".bak435", ".bak436"), ("PS435", "PS436"), ("ps435", "ps436"), ("deploy435", "deploy436"),
             ("result-435", "result-436"), ("speed-435", "speed-436"), ("posts-before-435", "posts-before-436"), ("make_deploy435", "make_deploy436")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-434.json")', '_prev = os.path.join(QA, "deploy-result-435.json")'),
             ('"FATAL: release 1.72.434 is still in flight', '"FATAL: release 1.72.435 is still in flight'),
             ('WANT_LIVE = "1.72.434"  # the checks name ?ver=1.72.436: this runner is for the release right after 1.72.434',
              'WANT_LIVE = "1.72.435"  # the checks name ?ver=1.72.436: this runner is for the release right after 1.72.435'),
             ("        for n in range(434, 329, -1):", "        for n in range(435, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy436.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy436.py with", len(rows), "checks")
