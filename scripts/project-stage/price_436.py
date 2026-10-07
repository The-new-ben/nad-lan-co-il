# -*- coding: utf-8 -*-
"""Release 1.72.436: PriceGuide v2.3, the rooms variant for the city price pages (design system 218; HAD-460; the CEO's terms:
three test cities first, stored data only, heading "מחשבון מחיר דירה ב{עיר}", a source line with the data date). The build
carries the official medians of Tel Aviv, Jerusalem and Haifa (price_guide/cities/<page>.json) for the shortcode door; the pages
get the shortcode after this release (insert_city_guides.py). Also: the rooms CSS and script join the shared assets.
The helper block is regenerated whole by price_guide/pg_helper.py, on the LIVE text 1.72.435 wrote."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "price_guide"))
sys.path.insert(0, HERE)
import pg_helper  # noqa: E402
import price_430 as P0  # noqa: E402

RELS = ["inc/project-stage.php", "i18n/lang-pages.json"]
FILES = {}
# the language pages' dictionary (scripts/i18n/build_lang_pages.py): the 7.10 card H2 "המחירים סביב הפרויקט ב{עיר}" and the link
# "מחירי דירות ב{עיר}" (snippet 661) printed Hebrew on the en/fr/ru/ar project pages; the first 436 run caught it and rolled back
LP_OLD_MD5 = "6712a2c4bc98d98fa84dc2725421840d"
LP_NEW = open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config", "i18n", "lang-pages.json"), encoding="utf-8").read()
pg_helper.KEYS = ("hamedina", "rova-4", "rainbow-tel-aviv", "duo-tel-aviv", "dimri-yama-sde-dov", "ashira-sde-dov", "h-infinity-somail-tel-aviv")
pg_helper.CITIES = ("tel-aviv-apartment-prices", "jerusalem-apartment-prices", "haifa-apartment-prices")
HELPER, LANGS = pg_helper.helper()
_START = "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"
_END = P0._FILM_T


def apply(rel, txt):
    if rel == "i18n/lang-pages.json":
        import hashlib
        import json
        # the second 436 run (7.10) rolled back on a false check but left the new dictionary live (the rollback list missed it):
        # the new build already live is fine, it is the state snippet 661 needs
        if hashlib.md5(txt.encode("utf-8")).hexdigest() not in (LP_OLD_MD5, hashlib.md5(LP_NEW.encode("utf-8")).hexdigest()):
            raise SystemExit("price_436: the live lang-pages.json is not the 28.9 build; diff it first")
        if "המחירים סביב הפרויקט ב" not in LP_NEW or len(json.loads(LP_NEW)["patterns"]) != 20:
            raise SystemExit("price_436: rebuild lang-pages.json (python scripts/i18n/build_lang_pages.py)")
        return LP_NEW
    if "PriceGuide v2.3 (design system" in txt:
        raise SystemExit("price_436: already applied")
    if txt.count(_START) != 1 or txt.count(_END) != 1 or "PriceGuide v2.2 (design system" not in txt:
        raise SystemExit("price_436: the 1.72.435 helper is not there")
    a, b = txt.find(_START), txt.find(_END)
    return txt[:a] + HELPER + txt[b:]
