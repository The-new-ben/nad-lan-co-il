# -*- coding: utf-8 -*-
"""Release 1.72.440: AreaMap v1.1 (design system 224; HAD-460). The AreaMap block that 1.72.437 put before the price block is
regenerated whole:
- languages: area_map/<key>.<lang>.json ("ui": lang, dir, words); nadlan_am_html( $key, $lang ) switches on "key|lang";
  the shortcode [nadlan_area_map key="rova-4"] takes lang="" or the page's language (page-lang.php: /en/<path>/ pages), and
  renders NOTHING when that language has no file (never Hebrew on a language page);
- a layer without places gets no filter and no list heading; the card title lines up (logical margin);
- the second instance: key "sde-dov" (/sde-dov/, plan 4444 line, 9 projects on official lots, 25 places; sources in
  docs/design/area-map-3d/sde-dov-sources.json). The page gets the shortcode after this release.
The Hebrew rova-4 section is byte-identical to v1 except the card title rule in the shared CSS (render_map.py)."""
import glob
import json
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "area_map"))
sys.path.insert(0, HERE)
import render_map as RM  # noqa: E402
import price_430 as P0  # noqa: E402

RELS = ["inc/project-stage.php"]
FILES = {}
KEYS = ("rova-4", "sde-dov")
LANGS = ("he", "en", "fr", "ru", "ar")
MARK = "AreaMap v1.1 (design system 224"
_AM_START = "if ( ! function_exists( 'nadlan_am_html' ) ) {\n"
_PG_START = "if ( ! function_exists( 'nadlan_pg_render' ) ) {\n"


def _payloads():
    out = {}
    for k in KEYS:
        for lang in LANGS:
            fn = os.path.join(HERE, "area_map", k + (".json" if lang == "he" else "." + lang + ".json"))
            if os.path.exists(fn):
                out[(k, lang)] = RM.html(json.load(io.open(fn, encoding="utf-8")))
    return out


def _helper():
    pays = _payloads()
    labels = {kl: "NLAM_" + (kl[0] + "_" + kl[1]).upper().replace("-", "_") for kl in pays}
    for h in list(pays.values()) + [RM.CSS, RM.JS]:
        if any(x in h for x in list(labels.values()) + ["NLAM_CSS", "NLAM_JS"]):
            raise SystemExit("map_440: a nowdoc label appears inside a payload")
    php = [_AM_START,
           f"\t/** {MARK}, HAD-460): the 3D neighbourhood map. Built by scripts/project-stage/area_map/render_map.py from\n",
           "\t *  area_map/<key>.json and <key>.<lang>.json. Cases: " + ", ".join(k + "|" + l for k, l in pays) + ". */\n",
           "\tfunction nadlan_am_html( $key, $lang = 'he' ) {\n", "\t\tswitch ( $key . '|' . $lang ) {\n"]
    for (k, lang), h in pays.items():
        lab = labels[(k, lang)]
        php.append(f"\t\t\tcase '{k}|{lang}':\n\t\t\t\treturn <<<'{lab}'\n{h}\n{lab};\n")
    php += ["\t\t}\n", "\t\treturn '';\n", "\t}\n",
            "\tadd_action( 'init', function () {\n",
            "\t\tadd_shortcode( 'nadlan_area_map', function ( $atts ) {\n",
            "\t\t\tstatic $assets = false;\n",
            "\t\t\t$a    = shortcode_atts( array( 'key' => '', 'lang' => '' ), (array) $atts, 'nadlan_area_map' );\n",
            "\t\t\t$lang = sanitize_key( (string) $a['lang'] );\n",
            "\t\t\tif ( '' === $lang ) {\n",
            "\t\t\t\t$lang = function_exists( 'nadlan_pglang_lang' ) ? (string) nadlan_pglang_lang() : '';\n",
            "\t\t\t\t$lang = '' === $lang ? 'he' : $lang;\n",
            "\t\t\t}\n",
            "\t\t\t$h = nadlan_am_html( sanitize_key( (string) $a['key'] ), $lang );\n",
            "\t\t\tif ( '' === $h ) { return ''; }\n",
            "\t\t\tif ( $assets ) { return $h; }\n",
            "\t\t\t$assets = true;\n",
            "\t\t\t$css = <<<'NLAM_CSS'\n" + RM.CSS.strip() + "\nNLAM_CSS;\n",
            "\t\t\t$js  = <<<'NLAM_JS'\n" + RM.JS.strip() + "\nNLAM_JS;\n",
            "\t\t\treturn '<style id=\"nlam-css\">' . $css . '</style>' . $h . '<script id=\"nlam-js\">' . $js . '</script>';\n",
            "\t\t} );\n", "\t} );\n", "}\n\n"]
    return "".join(php), pays


HELPER, PAYS = _helper()


def apply(rel, txt):
    if MARK in txt:
        raise SystemExit("map_440: already applied")
    if txt.count(_AM_START) != 1 or txt.count(_PG_START) != 1 or "AreaMap v1 (design system 219" not in txt or "PriceGuide v2.6 (design system" not in txt:
        raise SystemExit("map_440: the 1.72.439 text is not there")
    a, b = txt.find(_AM_START), txt.find(_PG_START)
    if not a < b:
        raise SystemExit("map_440: the AreaMap block is not right before the price block")
    return txt[:a] + HELPER + txt[b:]
