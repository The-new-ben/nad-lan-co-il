# -*- coding: utf-8 -*-
"""Release 1.72.442: data only (HAD-439/HAD-460): the Sde Dov price list and 3D map in en/fr/ru/ar
(price_guide/sde-dov-prices.<lang>.json, area_map/sde-dov.<lang>.json; numbers check docs/content/sde-dov-i18n-2026-10/
components-check.md: 0 mismatches). Both blocks are regenerated whole from the same code as 1.72.440/441 (markers PriceGuide
v2.8 and AreaMap v1.2 mark the data release); the shortcodes already take the page's language, so the files show on the coming
/<lang>/sde-dov/ pages and nowhere else."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_441  # noqa: E402
import map_440  # noqa: E402
import price_430 as P0  # noqa: E402

RELS = ["inc/project-stage.php"]
FILES = {}
PG = price_441.HELPER.replace("PriceGuide v2.7 (design system", "PriceGuide v2.8 (design system", 1)
AM = map_440.HELPER.replace("AreaMap v1.1 (design system 224", "AreaMap v1.2 (design system 224", 1)
if "PriceGuide v2.8" not in PG or "AreaMap v1.2" not in AM:
    raise SystemExit("data_442: markers not set")
for need in ("sde-dov|en", "sde-dov|ar"):
    if f"case '{need}'" not in AM:
        raise SystemExit("data_442: the map block lacks " + need)
_AM, _PG, _END = map_440._AM_START, price_441._START, P0._FILM_T


def apply(rel, txt):
    if "PriceGuide v2.8 (design system" in txt:
        raise SystemExit("data_442: already applied")
    if not ("PriceGuide v2.7 (design system" in txt and "AreaMap v1.1 (design system 224" in txt):
        raise SystemExit("data_442: the 1.72.441 text is not there")
    a, b, c = txt.find(_AM), txt.find(_PG), txt.find(_END)
    if not (0 <= a < b < c) or txt.count(_AM) != 1 or txt.count(_PG) != 1 or txt.count(_END) != 1:
        raise SystemExit("data_442: block order is not AreaMap < PriceGuide < film helper")
    return txt[:a] + AM + PG + txt[c:]
