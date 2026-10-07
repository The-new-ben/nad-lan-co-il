# -*- coding: utf-8 -*-
"""Release 1.72.432: PriceGuide v1.3, style only (HAD-460). On phones the theme's `.entry-content p, .entry-content li
{font-size:16px!important}` (0,1,1) beat the component's lone-class rules (0,1,0): the estimate showed at 16px instead of 25-32,
the fine print at 16 instead of 12.5 (measured live on 1.72.431 through the CSS inspector). Every component rule now starts with
the root class (.nlpg .nlpg__big = 0,2,0). The helper block is regenerated whole from price_guide/; nothing else changes."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_430 as P0  # noqa: E402

RELS = ["inc/project-stage.php"]
FILES = {}
_START = "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"
_END = P0._FILM_T


def apply(rel, txt):
    if ".nlpg .nlpg__big{" in txt:
        raise SystemExit("price_432: already applied")
    if txt.count(_START) != 1 or txt.count(_END) != 1 or '"prices prices"' not in txt:
        raise SystemExit("price_432: the 1.72.431 helper and grid row are not there")
    a, b = txt.find(_START), txt.find(_END)
    if not 0 < a < b or 'id="nlpg"' not in txt[a:b]:
        raise SystemExit("price_432: the live helper is not the PriceGuide one")
    return txt[:a] + P0.HELPER + txt[b:]
