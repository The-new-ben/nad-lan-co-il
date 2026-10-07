# -*- coding: utf-8 -*-
"""Release 1.72.438: PriceGuide v2.5 (HAD-460; the CEO's decisions of 7.10.2026, 13:00):
- every city list's title is "מחירון ומחשבון: מחיר דירה ב{עיר} לפי חדרים", unlike any H2 on its page (Jerusalem had two
  near-identical H2s: the page's "כמה עולה דירה בירושלים לפי הנתונים שנבדקו" and the list's "כמה עולה דירה בירושלים ב-2026");
- wave 1 of the other cities (10 pages, by Search Console impressions): their data joins the build; the pages get the shortcode
  after this release (insert_city_guides.py, which now stops on a duplicate H2), measured before/after with city_perf.py.
- the Sde Dov price list (price_guide/sde-dov-prices.json, 39 rows, 27 sources; for /sde-dov/prices/, whose numbers were aligned
  to the same sources the same day: docs/content/sde-dov-prices-2026-10) with the new fold mode ("open_groups": 2 keeps the long
  list at ~2,000px on desktop; render.py adds nlpg--fold; lists without the key are unchanged);
- the Program L row of Rainbow, Dimri Yama and Ashira: 52,000-57,000 (it showed 70-72K that belongs to a project elsewhere) and the
  "פרויקט אחר ברובע" calculator bound 71,000 (docs/content/sde-dov-prices-2026-10/project-files-fix.md).
The price block is regenerated whole by price_guide/pg_helper.py on the LIVE text 1.72.437 wrote; the AreaMap block sits before it
and is not touched. CSS: v2.4 (design system 220) plus one wide-screen rule for nlpg--fold (design system 222)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "price_guide"))
sys.path.insert(0, HERE)
import pg_helper  # noqa: E402
import price_430 as P0  # noqa: E402

RELS = ["inc/project-stage.php"]
FILES = {}
WAVE1 = ("herzliya-apartment-prices", "netanya-apartment-prices", "ramat-gan-apartment-prices", "bat-yam-apartment-prices",
         "hod-hasharon-apartment-prices", "ashdod-apartment-prices", "petah-tikva-apartment-prices", "ashkelon-apartment-prices",
         "eilat-apartment-prices", "kiryat-ono-apartment-prices")
pg_helper.KEYS = ("hamedina", "rova-4", "rainbow-tel-aviv", "duo-tel-aviv", "dimri-yama-sde-dov", "ashira-sde-dov", "h-infinity-somail-tel-aviv",
                  "sde-dov-prices")
pg_helper.CITIES = ("tel-aviv-apartment-prices", "jerusalem-apartment-prices", "haifa-apartment-prices") + WAVE1
_h, LANGS = pg_helper.helper()
if _h.count("PriceGuide v2.4 (design system") != 1:
    raise SystemExit("price_438: pg_helper does not build the v2.4 block")
HELPER = _h.replace("PriceGuide v2.4 (design system", "PriceGuide v2.5 (design system", 1)
_START = "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"
_END = P0._FILM_T


def apply(rel, txt):
    if "PriceGuide v2.5 (design system" in txt:
        raise SystemExit("price_438: already applied")
    if txt.count(_START) != 1 or txt.count(_END) != 1 or "PriceGuide v2.4 (design system" not in txt or "AreaMap v1 (design system 219" not in txt:
        raise SystemExit("price_438: the 1.72.437 text is not there")
    a, b = txt.find(_START), txt.find(_END)
    if txt.find("AreaMap v1 (design system 219") > a:
        raise SystemExit("price_438: the AreaMap block is inside the price span; it would be lost")
    return txt[:a] + HELPER + txt[b:]
