# -*- coding: utf-8 -*-
"""Release 1.72.433: PriceGuide v2 in five languages (HAD-460; Ben 7.10.2026: the five languages; the CEO's condition: after the
Hebrew is live and checked, which 1.72.430-432 did). The helper is rebuilt by price_guide/pg_helper.py with one server-rendered
section per language data file (he, en, fr, ru, ar) and the interface words in each language (render.UI_HE / each file's "ui");
the parts function stops limiting the section to the Hebrew page; the shortcode [nadlan_price_guide key="..."] opens the same
section on a regular page (Hebrew; first user: the Rova 4 page). On the LIVE inc/project-stage.php text 1.72.432 wrote."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "price_guide"))
sys.path.insert(0, HERE)
import pg_helper  # noqa: E402
import price_430 as P0  # noqa: E402

RELS = ["inc/project-stage.php"]
FILES = {}
HELPER, LANGS = pg_helper.helper()
_START = "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"
_END = P0._FILM_T
_GATE = "'prices' => ( $he && function_exists( 'nadlan_pg_render' ) ) ? nadlan_pg_render( $ps, $wa ) : '', // PriceGuide v1\n"
_GATE_NEW = "'prices' => function_exists( 'nadlan_pg_render' ) ? nadlan_pg_render( $ps, $wa ) : '', // PriceGuide v2: every language with a data file\n"


def apply(rel, txt):
    if "PriceGuide v2 (design system" in txt:
        raise SystemExit("price_433: already applied")
    if txt.count(_START) != 1 or txt.count(_END) != 1 or ".nlpg .nlpg__big{" not in txt:
        raise SystemExit("price_433: the 1.72.432 helper is not there")
    a, b = txt.find(_START), txt.find(_END)
    if not 0 < a < b:
        raise SystemExit("price_433: anchors out of order")
    txt = txt[:a] + HELPER + txt[b:]
    if txt.count(_GATE) != 1:
        raise SystemExit("price_433: the Hebrew-only gate x%d" % txt.count(_GATE))
    return txt.replace(_GATE, _GATE_NEW)
