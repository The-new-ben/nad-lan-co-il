# -*- coding: utf-8 -*-
"""Release 1.72.437: AreaMap v1 (design system 219; HAD-460; Ben 7.10.2026: "map the compound in 3D ... the businesses around
iconic pages"). A separate helper block, next to the price guide's, opens the shortcode [nadlan_area_map key="rova-4"]: the
server-rendered section (heading, filters, placeholder, the list of every place) with its CSS and script; MapLibre, the RTL plugin
and the tiles load only when the section nears the screen. Data: area_map/rova-4.json (sources in docs/design/area-map-3d).
Inserted before the ProjectFilm strings helper of the LIVE inc/project-stage.php text that 1.72.436 wrote."""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "area_map"))
sys.path.insert(0, HERE)
import render_map as RM  # noqa: E402
import price_430 as P0  # noqa: E402

RELS = ["inc/project-stage.php"]
FILES = {}
KEYS = ("rova-4",)
MARK = "AreaMap v1 (design system 219"


def _helper():
    pays = {}
    for k in KEYS:
        d = json.load(io.open(os.path.join(HERE, "area_map", k + ".json"), encoding="utf-8"))
        pays[k] = RM.html(d)
    labels = {k: "NLAM_" + k.upper().replace("-", "_") for k in pays}
    for h in list(pays.values()) + [RM.CSS, RM.JS]:
        if any(x in h for x in list(labels.values()) + ["NLAM_CSS", "NLAM_JS"]):
            raise SystemExit("map_437: a nowdoc label appears inside a payload")
    php = ["if ( ! function_exists( 'nadlan_am_html' ) ) {\n",
           f"\t/** {MARK}, HAD-460): the 3D neighbourhood map. Built by scripts/project-stage/area_map/render_map.py from\n",
           "\t *  area_map/<key>.json (every position has its source in docs/design/area-map-3d/data.json). Keys: " + ", ".join(pays) + ". */\n",
           "\tfunction nadlan_am_html( $key ) {\n", "\t\tswitch ( $key ) {\n"]
    for k, h in pays.items():
        php.append(f"\t\t\tcase '{k}':\n\t\t\t\treturn <<<'{labels[k]}'\n{h}\n{labels[k]};\n")
    php += ["\t\t}\n", "\t\treturn '';\n", "\t}\n",
            "\tadd_action( 'init', function () {\n",
            "\t\tadd_shortcode( 'nadlan_area_map', function ( $atts ) {\n",
            "\t\t\tstatic $assets = false;\n",
            "\t\t\t$a = shortcode_atts( array( 'key' => '' ), (array) $atts, 'nadlan_area_map' );\n",
            "\t\t\t$h = nadlan_am_html( sanitize_key( (string) $a['key'] ) );\n",
            "\t\t\tif ( '' === $h ) { return ''; }\n",
            "\t\t\tif ( $assets ) { return $h; }\n",
            "\t\t\t$assets = true;\n",
            "\t\t\t$css = <<<'NLAM_CSS'\n" + RM.CSS.strip() + "\nNLAM_CSS;\n",
            "\t\t\t$js  = <<<'NLAM_JS'\n" + RM.JS.strip() + "\nNLAM_JS;\n",
            "\t\t\treturn '<style id=\"nlam-css\">' . $css . '</style>' . $h . '<script id=\"nlam-js\">' . $js . '</script>';\n",
            "\t\t} );\n", "\t} );\n", "}\n\n"]
    return "".join(php)


HELPER = _helper()


def apply(rel, txt):
    if MARK in txt:
        raise SystemExit("map_437: already applied")
    if txt.count(P0._FILM_T) != 1 or "PriceGuide v2.3 (design system" not in txt:
        raise SystemExit("map_437: the 1.72.436 text is not there")
    return txt.replace(P0._FILM_T, HELPER + P0._FILM_T)
