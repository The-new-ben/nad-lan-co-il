# -*- coding: utf-8 -*-
"""Builds the PHP for PriceGuide v2 (7.10.2026): server-rendered sections per (key, language) from the data files in this folder
(<key>.json = Hebrew, <key>.<lang>.json = en/fr/ru/ar), the shared CSS and script, and two doors:
  nadlan_pg_render( $ps, $wa )          on a project page (key = the project slug, language = $ps['lang'])
  [nadlan_price_guide key="rova-4"]     on any page (Hebrew; the site's WhatsApp number)
A (key, language) without a file renders nothing. Nowdoc labels are checked against the payloads."""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render as PG  # noqa: E402

LANGS = ("he", "en", "fr", "ru", "ar")
KEYS = ("hamedina", "rova-4")


def payloads():
    out = {}
    for key in KEYS:
        for lang in LANGS:
            fn = os.path.join(HERE, f"{key}.json" if lang == "he" else f"{key}.{lang}.json")
            if os.path.exists(fn):
                d = json.load(io.open(fn, encoding="utf-8"))
                out[(key, lang)] = PG.html(d, "{{WA}}")
    return out


def helper():
    P = payloads()
    if ("hamedina", "he") not in P:
        raise SystemExit("pg_helper: the Kikar Hebrew data is missing")
    lab = {k: "NLPG_" + re.sub(r"[^A-Z0-9]", "_", (k[0] + "_" + k[1]).upper()) for k in P}
    every = list(lab.values()) + ["NLPG_CSS", "NLPG_JS"]
    for h in list(P.values()) + [PG.CSS, PG.JS]:
        if any(x in h for x in every):
            raise SystemExit("pg_helper: a nowdoc label appears inside a payload")
    php = ["if ( ! function_exists( 'nadlan_pg_render' ) ) {\n",
           "\t/** PriceGuide v2.1 (design system 7.10.2026, HAD-460): the price list and the price calculator. Built by\n",
           "\t *  scripts/project-stage/price_guide/pg_helper.py from <key>.json and <key>.<lang>.json (every number has its source there).\n",
           "\t *  Sections: " + ", ".join(f"{k}/{l}" for k, l in sorted(P)) + ". */\n",
           "\tfunction nadlan_pg_html( $key, $lang ) {\n",
           "\t\tswitch ( $key . '|' . $lang ) {\n"]
    for (k, l), h in sorted(P.items()):
        php.append(f"\t\t\tcase '{k}|{l}':\n\t\t\t\treturn <<<'{lab[(k, l)]}'\n{h}\n{lab[(k, l)]};\n")
    php += ["\t\t}\n", "\t\treturn '';\n", "\t}\n",
            "\tfunction nadlan_pg_wrap( $html, $wa ) {\n",
            "\t\tstatic $assets = false;\n",
            "\t\tif ( '' === $html ) { return ''; }\n",
            "\t\t$wa = preg_replace( '/\\D/', '', (string) $wa );\n",
            "\t\tif ( '' === $wa ) {\n",
            "\t\t\t$html = (string) preg_replace( '#<a class=\"nlds-btn nlds-btn--primary nlpg__wa\"[^>]*>.*?</a>#s', '', $html );\n",
            "\t\t\t$html = str_replace( '&quot;wa&quot;:&quot;{{WA}}&quot;', '&quot;wa&quot;:&quot;&quot;', $html );\n",
            "\t\t}\n",
            "\t\t$html = str_replace( '{{WA}}', $wa, $html );\n",
            "\t\tif ( $assets ) { return $html; }\n",
            "\t\t$assets = true;\n",
            "\t\t$css = <<<'NLPG_CSS'\n" + PG.CSS.strip() + "\nNLPG_CSS;\n",
            "\t\t$js  = <<<'NLPG_JS'\n" + PG.JS.strip() + "\nNLPG_JS;\n",
            "\t\treturn '<style id=\"nlpg-css\">' . $css . '</style>' . $html . '<script id=\"nlpg-js\">' . $js . '</script>';\n",
            "\t}\n",
            "\tfunction nadlan_pg_render( $ps, $wa ) {\n",
            "\t\tstatic $done = false;\n",
            "\t\t$slug = (string) ( $ps['slug'] ?? '' );\n",
            "\t\tif ( $done || '' === $slug ) { return ''; }\n",
            "\t\t$key  = (string) preg_replace( '/-(en|fr|ru|ar)$/', '', $slug ); // the project's key, without a language ending\n",
            "\t\t$html = nadlan_pg_html( $key, (string) ( $ps['lang'] ?? 'he' ) );\n",
            "\t\tif ( '' === $html ) { return ''; }\n",
            "\t\t$done = true;\n",
            "\t\treturn nadlan_pg_wrap( $html, $wa );\n",
            "\t}\n",
            "\tadd_action( 'init', function () {\n",
            "\t\tadd_shortcode( 'nadlan_price_guide', function ( $atts ) {\n",
            "\t\t\t$a  = shortcode_atts( array( 'key' => '' ), (array) $atts, 'nadlan_price_guide' );\n",
            "\t\t\t$wa = function_exists( 'nadlan_cta_whatsapp_number' ) ? (string) nadlan_cta_whatsapp_number() : '';\n",
            "\t\t\treturn nadlan_pg_wrap( nadlan_pg_html( sanitize_key( (string) $a['key'] ), 'he' ), $wa );\n",
            "\t\t} );\n",
            "\t} );\n",
            "}\n\n"]
    return "".join(php), sorted(P)


if __name__ == "__main__":
    h, keys = helper()
    print(len(h), "bytes of PHP;", keys)
