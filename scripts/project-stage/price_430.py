# -*- coding: utf-8 -*-
"""Release 1.72.430: PriceGuide v1 (design system 7.10.2026, version 212; HAD-433). Ben, 7.10.2026: a real price list and a
price calculator on the Kikar HaMedina page, "up on the page, not before the first paragraph", the kind of prices AI answers cite.
- /projects/hamedina/ (Hebrew only; the language pages follow after the Hebrew is live and checked, the CEO's condition):
  the section sits right after the opening paragraph and the three buttons, before the stage.
- The markup is server-rendered (the table, the tiles and the default estimate are in the HTML); the script only recalculates.
- Data: scripts/project-stage/price_guide/hamedina.json (every number with its source; the page shows dates only).
Applied to the LIVE inc/project-stage.php text (what 1.72.429 wrote); every anchor exactly once."""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "price_guide"))
import render as PG  # noqa: E402

DATA = json.load(io.open(os.path.join(HERE, "price_guide", "hamedina.json"), encoding="utf-8"))
RELS = ["inc/project-stage.php"]
FILES = {}
MARK = "nadlan_pg_render"

_html = PG.html(DATA, "{{WA}}")
for bad in ("NLPG_HTML", "NLPG_CSS", "NLPG_JS"):
    if bad in _html or bad in PG.CSS or bad in PG.JS:
        raise SystemExit("price_430: a nowdoc label appears inside the payload")

HELPER = (
    "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"
    "\t/** PriceGuide v1 (design system 7.10.2026, HAD-433): the price list and the price calculator, right after the opening\n"
    "\t *  paragraph and the buttons. Kikar HaMedina in Hebrew only for now. The markup comes from\n"
    "\t *  scripts/project-stage/price_guide/render.py with hamedina.json (every number has its source there). */\n"
    "\tfunction nadlan_pg_render( $ps, $wa ) {\n"
    "\t\tstatic $done = false;\n"
    "\t\tif ( $done || 'hamedina' !== (string) ( $ps['slug'] ?? '' ) ) { return ''; }\n"
    "\t\t$done = true;\n"
    "\t\t$wa   = preg_replace( '/\\D/', '', (string) $wa );\n"
    "\t\t$html = <<<'NLPG_HTML'\n" + _html + "\nNLPG_HTML;\n"
    "\t\t$css  = <<<'NLPG_CSS'\n" + PG.CSS.strip() + "\nNLPG_CSS;\n"
    "\t\t$js   = <<<'NLPG_JS'\n" + PG.JS.strip() + "\nNLPG_JS;\n"
    "\t\tif ( '' === $wa ) {\n"
    "\t\t\t$html = (string) preg_replace( '#<a class=\"nlds-btn nlds-btn--primary nlpg__wa\"[^>]*>.*?</a>#s', '', $html );\n"
    "\t\t\t$html = str_replace( '&quot;wa&quot;:&quot;{{WA}}&quot;', '&quot;wa&quot;:&quot;&quot;', $html );\n"
    "\t\t}\n"
    "\t\treturn '<style id=\"nlpg-css\">' . $css . '</style>' . str_replace( '{{WA}}', $wa, $html ) . '<script id=\"nlpg-js\">' . $js . '</script>';\n"
    "\t}\n"
    "}\n\n")

_FILM_T = "if ( ! function_exists( 'nadlan_ps_film_t' ) ) {\n"
_RET = "\t\treturn array( 'hero' => $hero, 'cta' => $cta, 'stagebox' => $stagebox, 'rail' => $rail, 'facts' => $facts, 'below' => $below, 'tour' => '', 'deals' => $he ? nadlan_ps_deals( $ps ) : '' );\n"
_RET_NEW = ("\t\treturn array( 'hero' => $hero, 'cta' => $cta, 'prices' => ( $he && function_exists( 'nadlan_pg_render' ) ) ? nadlan_pg_render( $ps, $wa ) : '', // PriceGuide v1\n"
            "\t\t\t'stagebox' => $stagebox, 'rail' => $rail, 'facts' => $facts, 'below' => $below, 'tour' => '', 'deals' => $he ? nadlan_ps_deals( $ps ) : '' );\n")
_PAGE = "$parts['hero'] . $lead . $parts['cta'] . $parts['stagebox'] ."
_PAGE_NEW = "$parts['hero'] . $lead . $parts['cta'] . ( $parts['prices'] ?? '' ) . $parts['stagebox'] ."  # PriceGuide v1: after the lead and the buttons

EDITS = [(_FILM_T, HELPER + _FILM_T), (_RET, _RET_NEW), (_PAGE, _PAGE_NEW)]


def apply(rel, txt):
    if MARK in txt:
        raise SystemExit("price_430: already applied")
    for old, new in EDITS:
        if txt.count(old) != 1:
            raise SystemExit("price_430: anchor x%d: %r" % (txt.count(old), old[:90]))
        txt = txt.replace(old, new)
    return txt


if __name__ == "__main__":
    src = sys.argv[1]
    t = io.open(src, encoding="utf-8").read().replace("\r\n", "\n")
    out = apply("inc/project-stage.php", t)
    io.open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(out)
    print("applied:", len(out) - len(t), "bytes added")
