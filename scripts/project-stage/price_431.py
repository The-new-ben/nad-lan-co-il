# -*- coding: utf-8 -*-
"""Release 1.72.431: PriceGuide v1.2, the place on the page (design system 7.10.2026; HAD-460). 1.72.430 put the section in the
right SOURCE order, but the world page is a named grid ("hero stage" / "lead stage" / "cta stage" / "below below" ...), so a child
without an area fell to the end of the page (measured live: top 3,226 px on a 1366 screen, 5,083 px on a phone).
- The world page's two grid templates gain a "prices" row right after the first fold: on a wide screen after the text column
  and the stage ("prices prices"), on narrower screens right after the stage. The first fold stays as it is (the phone's landing
  lane, P9a), and the price guide comes before the area map.
- The section takes that area and the page's own gutters (no second padding).
On the LIVE inc/project-stage.php text that 1.72.430 wrote; every anchor exactly once."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_430 as P0  # noqa: E402 (rebuilds the helper with the current CSS and data)

RELS = ["inc/project-stage.php"]
FILES = {}
_START = "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"
_END = P0._FILM_T
_W = ('grid-template-areas:"hero stage" "lead stage" "cta stage" "below below" "facts facts" "deals deals" "rail rail"}\'',
      'grid-template-areas:"hero stage" "lead stage" "cta stage" "prices prices" "below below" "facts facts" "deals deals" "rail rail"}\'')
_N = ('grid-template-areas:"hero" "lead" "cta" "stage" "below" "facts" "deals" "rail"}',
      'grid-template-areas:"hero" "lead" "cta" "stage" "prices" "below" "facts" "deals" "rail"}')


def apply(rel, txt):
    if '"prices prices"' in txt:
        raise SystemExit("price_431: already applied")
    if txt.count(_START) != 1 or txt.count(_END) != 1:
        raise SystemExit("price_431: the 1.72.430 helper is not there once")
    a, b = txt.find(_START), txt.find(_END)
    if not 0 < a < b or "id=\"nlpg\"" not in txt[a:b]:
        raise SystemExit("price_431: the live helper is not the PriceGuide one")
    txt = txt[:a] + P0.HELPER + txt[b:]
    for old, new in (_W, _N):
        if txt.count(old) != 1:
            raise SystemExit("price_431: grid anchor x%d: %r" % (txt.count(old), old[:80]))
        txt = txt.replace(old, new)
    return txt
