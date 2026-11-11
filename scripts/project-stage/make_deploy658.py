# -*- coding: utf-8 -*-
"""make deploy658.py from deploy657.py: 1.72.658 = HAD-712, the Kikar showroom in English (Ben 11.11.2026 night: the English board
approved; "the showroom in English"). The four showroom files take their words from a he/en/fr dictionary and their direction from the
page language (world/showroom-i18n.js; the Hebrew page renders identically: docs/research/2026-11-11-kikar-journey/evidence/i18n-test-2026-11-11).
  FILES  world/showroom.js, showroom.css, cockpit.js, cockpit.css, journey.js, NEW world/showroom-i18n.js, basket/basket.js
  HUNKS  inc/project-stage.php (live 652 text): the Kikar showcase gate takes he and en; the aerial alt in English; the page language
         passed to the cockpit and journey settings.
         inc/basket.php: the basket on the Hebrew and English Kikar pages; its settings carry the language.
The English page keeps the old 3D stage under the showroom (Ben: keep the view); French follows after the English page is checked."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

W = "assets/project-stage/world/"
FILES = [W + "showroom.js", W + "showroom.css", W + "cockpit.js", W + "cockpit.css", W + "journey.js", W + "showroom-i18n.js", "assets/basket/basket.js"]
NEW = [W + "showroom-i18n.js"]
HE_ALT = "$alt = 'הדמיה של מגדלי כיכר המדינה מהאוויר: שלושת המגדלים, הפארק בתוך טבעת הכיכר, הירקון והים';"
HUNKS = {
    "inc/project-stage.php": [
        ("return 'hamedina' === (string) ( $ps['dir'] ?? '' ) && 'he' === (string) ( $ps['lang'] ?? 'he' ); // HAD-699 (1.72.639): every visitor; ?kikar=next stays harmless",
         "return 'hamedina' === (string) ( $ps['dir'] ?? '' ) && in_array( (string) ( $ps['lang'] ?? 'he' ), array( 'he', 'en' ), true ); // HAD-699 (1.72.639): every visitor; 1.72.658 (HAD-712): the English page too"),
        ("\t\t\t" + HE_ALT,
         "\t\t\t" + HE_ALT + "\n\t\t\tif ( 'he' !== $tl ) { $alt = 'Kikar Hamedina Towers from the air: the three towers, the park inside the ring of the square, the Yarkon and the sea, illustrative visualisation'; } // 1.72.658"),
        ("\t\t\t\t\t'avail'  => function_exists( 'rest_url' ) ? rest_url( 'nadlan/v1/room/available' ) : '',\n",
         "\t\t\t\t\t'avail'  => function_exists( 'rest_url' ) ? rest_url( 'nadlan/v1/room/available' ) : '',\n\t\t\t\t\t'lang'   => $tl, // 1.72.658 (HAD-712): the cockpit's words and direction\n"),
        ("\t\t\t\t\t'aerial' => plugins_url( $base . 'aerial.json', dirname( __FILE__ ) ) . $v,\n",
         "\t\t\t\t\t'aerial' => plugins_url( $base . 'aerial.json', dirname( __FILE__ ) ) . $v,\n\t\t\t\t\t'lang'   => $tl, // 1.72.658 (HAD-712): the showroom's words and direction\n"),
    ],
    "inc/basket.php": [
        ("return $ps && 'he' === ( $ps['lang'] ?? 'he' ); // Hebrew-only for now (HAD-361)",
         "return $ps && ( 'he' === ( $ps['lang'] ?? 'he' ) || ( 'en' === ( $ps['lang'] ?? '' ) && 'hamedina' === (string) ( $ps['dir'] ?? '' ) ) ); // Hebrew; 1.72.658 (HAD-712): and the English Kikar page"),
        ("\t\t'slug'    => (string) $ps['slug'],\n", "\t\t'slug'    => (string) $ps['slug'],\n\t\t'lang'    => (string) ( $ps['lang'] ?? 'he' ), // 1.72.658: the basket's words and direction\n"),
    ],
}
import hashlib, json  # noqa: E402
PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-657.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
assert "inc/project-stage.php" not in (rp.get("files") or {}) and "inc/basket.php" not in (rp.get("files") or {}), "1.72.657 wrote a file this release hunks"
LIVE = {"inc/project-stage.php": "fc61f8e4b57891299b27bc5fdffd99a5",  # deploy-result-652.json; 653-657 did not write it
        "inc/basket.php": hashlib.md5(open(os.path.join(PLUG, "inc", "basket.php"), "rb").read()).hexdigest()}  # the runner proves it live
ROWS = ("    ('/projects/hamedina-en/?t658s=1', ['journey.js?ver=1.72.658', '&quot;lang&quot;:&quot;en&quot;', 'id=\"nadlan-basket-cfg\"', '\"lang\":\"en\"'], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('/projects/hamedina/?t658s=1', ['journey.js?ver=1.72.658', 'id=\"nadlan-basket-cfg\"'], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/showroom-i18n.js?t658s=1', ['Illustrative visualisation', 'NadLan advisor'], [], []),\n")
kl_release.build_release(657, 658, FILES, NEW, HUNKS, LIVE, ROWS, "the Kikar showroom in English (words he/en/fr, direction by language); the English basket",
                         "the English Kikar showroom")
# the check rows that asked for code lines this release rewrote (words now from the dictionary): the same check, the new line
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy658.py")
_s = open(_p, encoding="utf-8").read()
for _a, _b in [("'body:has(.nlsr) .nlps-stagebox{display:none!important}'", "'body:has(.nlsr[lang=\"he\"]) .nlps-stagebox{display:none!important}'"),
               ("\"[['הדירה הזאת', 0]]\"", "\"[[t('ck_pano_this'), 0]]\""),
               ("\"u.label ? ' · ' + u.label\"", "'u.label && !(EN() && heb(u.label))'"),
               ("\"label: d.label ?\"", "\"label: !tw && d.label ?\"")]:
    assert _s.count(_a) >= 1, "no row with " + _a
    _s = _s.replace(_a, _b)
open(_p, "w", encoding="utf-8", newline="\n").write(_s)
print("[rows] four check rows follow the rewritten lines")
# the English page row of 1.72.635 forbade the showroom there (journey.js, cockpit.js, aerial.json) and asked for the old poster: since
# 1.72.658 the English page carries the showroom on Ben's word; the row now asks for it (the first run of 658 rolled back on the old row)
_s = open(_p, encoding="utf-8").read()
_L = _s.split("\n")
_n = [i for i, l in enumerate(_L) if "('/projects/hamedina-en/?t658e=1'" in l]
assert len(_n) == 1, _n
_L[_n[0]] = "    ('/projects/hamedina-en/?t658e=1', ['<h1 id=\"nl-project-page-title\" class=\"nlps-h1\">', 'world\\/journey.js', 'aerial.json', 'world\\/cockpit.js'], ['Fatal error', 'Warning</b>'], []),"
open(_p, "w", encoding="utf-8", newline="\n").write("\n".join(_L))
print("[rows] the English page row asks for the showroom")
