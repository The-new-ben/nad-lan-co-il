# -*- coding: utf-8 -*-
"""Release 1.72.439: PriceGuide v2.6 (HAD-460; the CEO's approvals of 7.10.2026): wave 2 of the city price lists (10 cities) and
the national variant for the Israel page /apartment-prices/ (national.py: the Israel medians and a sortable table of the 23
cities with a price page, linked; no calculator; the Israel row's yearly change computed from two official medians and
footnoted). Design system 223. The pages get the shortcode after this release (insert_city_guides.py, which stops on an H2
twin), measured before/after with city_perf.py under the CEO's stop rule.
The price block is regenerated whole by price_guide/pg_helper.py on the LIVE text 1.72.438 wrote; the AreaMap block sits before
it and is not touched."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "price_guide"))
sys.path.insert(0, HERE)
import pg_helper  # noqa: E402
import price_430 as P0  # noqa: E402
import price_438  # noqa: E402

RELS = ["inc/project-stage.php"]
FILES = {}
WAVE2 = ("beer-sheva-apartment-prices", "bnei-brak-apartment-prices", "givatayim-apartment-prices", "holon-apartment-prices",
         "kfar-saba-apartment-prices", "modiin-apartment-prices", "raanana-apartment-prices", "ramat-hasharon-apartment-prices",
         "rehovot-apartment-prices", "rishon-lezion-apartment-prices")
pg_helper.KEYS = price_438.pg_helper.KEYS
pg_helper.CITIES = ("tel-aviv-apartment-prices", "jerusalem-apartment-prices", "haifa-apartment-prices") + price_438.WAVE1 + WAVE2
pg_helper.NATIONAL = "apartment-prices"
_h, LANGS = pg_helper.helper()
if _h.count("PriceGuide v2.4 (design system") != 1:
    raise SystemExit("price_439: pg_helper does not build the v2.4 block")
HELPER = _h.replace("PriceGuide v2.4 (design system", "PriceGuide v2.6 (design system", 1)
_START = "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"
_END = P0._FILM_T


def apply(rel, txt):
    if "PriceGuide v2.6 (design system" in txt:
        raise SystemExit("price_439: already applied")
    if txt.count(_START) != 1 or txt.count(_END) != 1 or "PriceGuide v2.5 (design system" not in txt or "AreaMap v1 (design system 219" not in txt:
        raise SystemExit("price_439: the 1.72.438 text is not there")
    a, b = txt.find(_START), txt.find(_END)
    if txt.find("AreaMap v1 (design system 219") > a:
        raise SystemExit("price_439: the AreaMap block is inside the price span; it would be lost")
    return txt[:a] + HELPER + txt[b:]
