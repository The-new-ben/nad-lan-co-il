# -*- coding: utf-8 -*-
"""Release 1.72.441: PriceGuide v2.7 (design system 225; HAD-460; the CEO's approval 7.10.2026, one script release): the area
chart's rows 42 units apart and its upper range label inside the frame (penthouse mode overlapped the next row on phones), the
explanation line keeps its numbers as islands (a range no longer breaks at its hyphen), the Rova 4 chart shows the area title, and
the shortcode takes lang="" or the page's language (/en/<path>/ pages; nothing when that language has no file). Same keys,
cities and national variant as 1.72.439. The price block is regenerated whole; the AreaMap block before it is not touched."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "price_guide"))
sys.path.insert(0, HERE)
import pg_helper  # noqa: E402
import price_430 as P0  # noqa: E402
import price_439  # noqa: E402

RELS = ["inc/project-stage.php"]
FILES = {}
pg_helper.KEYS = price_439.pg_helper.KEYS
pg_helper.CITIES = price_439.pg_helper.CITIES
pg_helper.NATIONAL = "apartment-prices"
_h, LANGS = pg_helper.helper()
if _h.count("PriceGuide v2.4 (design system") != 1:
    raise SystemExit("price_441: pg_helper does not build the v2.4 block")
HELPER = _h.replace("PriceGuide v2.4 (design system", "PriceGuide v2.7 (design system", 1)
_START = "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"
_END = P0._FILM_T


def apply(rel, txt):
    if "PriceGuide v2.7 (design system" in txt:
        raise SystemExit("price_441: already applied")
    if txt.count(_START) != 1 or txt.count(_END) != 1 or "PriceGuide v2.6 (design system" not in txt or "AreaMap v1.1 (design system 224" not in txt:
        raise SystemExit("price_441: the 1.72.440 text is not there")
    a, b = txt.find(_START), txt.find(_END)
    if txt.find("AreaMap v1.1 (design system 224") > a:
        raise SystemExit("price_441: the AreaMap block is inside the price span; it would be lost")
    return txt[:a] + HELPER + txt[b:]
