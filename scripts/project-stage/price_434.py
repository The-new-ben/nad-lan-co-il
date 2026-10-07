# -*- coding: utf-8 -*-
"""Release 1.72.434: PriceGuide on the regular project pages (HAD-460; Ben 7.10.2026: price lists and calculators on every
real-estate page we write). First: Rainbow (/projects/rainbow-tel-aviv/) and DUO (/projects/duo-tel-aviv/), Hebrew.
- The helper is rebuilt by price_guide/pg_helper.py: the project key is the slug without a language ending, so every project
  with a data file gets its section (Rainbow, DUO, Kikar; Rova 4 through the shortcode); the chart takes each project's y range
  and floor count (Rainbow 39, DUO 50).
- The regular pages' parts (nadlan_ps_parts) return the section too, and their three grid templates gain the "prices" row right
  after the first fold (the text column with the stage, and the rail on wide screens), before the area map.
- Kikar: a link from its price list to the Rova 4 page, and from Rova 4 back (the "see" lines).
On the LIVE inc/project-stage.php text that 1.72.433 wrote; every anchor exactly once."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "price_guide"))
sys.path.insert(0, HERE)
import pg_helper  # noqa: E402
import price_430 as P0  # noqa: E402

RELS = ["inc/project-stage.php"]
FILES = {}
pg_helper.KEYS = ("hamedina", "rova-4", "rainbow-tel-aviv", "duo-tel-aviv")
HELPER, LANGS = pg_helper.helper()
_START = "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"
_END = P0._FILM_T
_PARTS = "\t\treturn array( 'hero' => $hero, 'cta' => $cta, 'stagebox' => $stagebox, 'rail' => $rail, 'facts' => $facts, 'below' => $below, 'tour' => $tour, 'deals' => nadlan_ps_deals( $ps ) );\n"
_PARTS_NEW = ("\t\treturn array( 'hero' => $hero, 'cta' => $cta, 'prices' => function_exists( 'nadlan_pg_render' ) ? nadlan_pg_render( $ps, $wa ) : '', // PriceGuide v2.1\n"
              "\t\t\t'stagebox' => $stagebox, 'rail' => $rail, 'facts' => $facts, 'below' => $below, 'tour' => $tour, 'deals' => nadlan_ps_deals( $ps ) );\n")
GRIDS = [('grid-template-areas:"hero stage rail" "lead stage rail" "cta stage rail" "below below below"',
          'grid-template-areas:"hero stage rail" "lead stage rail" "cta stage rail" "prices prices prices" "below below below"'),
         ('grid-template-areas:"hero stage" "lead stage" "cta stage" "below below" "facts facts" "tour tour"',
          'grid-template-areas:"hero stage" "lead stage" "cta stage" "prices prices" "below below" "facts facts" "tour tour"'),
         ('grid-template-areas:"hero" "lead" "cta" "stage" "below" "facts" "tour"',
          'grid-template-areas:"hero" "lead" "cta" "stage" "prices" "below" "facts" "tour"')]


def apply(rel, txt):
    if "PriceGuide v2.1" in txt:
        raise SystemExit("price_434: already applied")
    if txt.count(_START) != 1 or txt.count(_END) != 1 or "PriceGuide v2 (design system" not in txt:
        raise SystemExit("price_434: the 1.72.433 helper is not there")
    a, b = txt.find(_START), txt.find(_END)
    txt = txt[:a] + HELPER + txt[b:]
    for old, new in [(_PARTS, _PARTS_NEW)] + GRIDS:
        if txt.count(old) != 1:
            raise SystemExit("price_434: anchor x%d: %r" % (txt.count(old), old[:90]))
        txt = txt.replace(old, new)
    return txt
