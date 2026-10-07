# -*- coding: utf-8 -*-
"""Release 1.72.435: PriceGuide v2.2 (HAD-460). Data and small fixes, on the LIVE inc/project-stage.php text 1.72.434 wrote:
- Dimri Yama and Ashira (Sde Dov) get their price lists (regular project pages, the grid row exists since 1.72.434); H Infinity's
  data is in the build for the shortcode door (its page has no stage block: placement later).
- Rainbow: the row "about 1,280 apartments sold" no longer says "in the year" (sources conflict: the original survey says "so far").
- The chart's grid lines follow each project's price range (Rainbow lacked its 90,000 line); the base script skips the rooms
  variant and every section starts inside try/catch.
- See lines: Rainbow -> /sde-dov/prices/ ("מחירי דירות בשדה דב", the CEO's anchor), DUO -> /north-tel-aviv/rova-4/.
The helper block is regenerated whole by price_guide/pg_helper.py."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "price_guide"))
sys.path.insert(0, HERE)
import pg_helper  # noqa: E402
import price_430 as P0  # noqa: E402

RELS = ["inc/project-stage.php"]
FILES = {}
pg_helper.KEYS = ("hamedina", "rova-4", "rainbow-tel-aviv", "duo-tel-aviv", "dimri-yama-sde-dov", "ashira-sde-dov", "h-infinity-somail-tel-aviv")
HELPER, LANGS = pg_helper.helper()
_START = "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"
_END = P0._FILM_T


def apply(rel, txt):
    if "PriceGuide v2.2 (design system" in txt:
        raise SystemExit("price_435: already applied")
    if txt.count(_START) != 1 or txt.count(_END) != 1 or "PriceGuide v2.1 (design system" not in txt:
        raise SystemExit("price_435: the 1.72.434 helper is not there")
    a, b = txt.find(_START), txt.find(_END)
    return txt[:a] + HELPER + txt[b:]
