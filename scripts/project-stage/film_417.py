# -*- coding: utf-8 -*-
"""Release 1.72.417 (design v104.40; Ben's decision 3.10.2026 evening: "option A only", then "upload everything, with the narration
too; write nothing about credit, that is my responsibility"). The narrated v2 film leads the Kikar film section: Hebrew on he,
English on en/fr/ru/ar; preload none, no autoplay; the film's own title-card poster; the figcaption "הדמיה להמחשה" in the page's
language; NO credit or licence wording on the page. The wide film over 700 px, the upright one (gen 2, the 13 s fix) on phones.
V1 stays below it under a small "the first version" heading; the facilities clip stays last. The URLs are the exact uploaded ones
(docs/qa/film-v2r1/media.json, byte-checked). Applied to the LIVE inc/project-stage.php text (each anchor once)."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(io.open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "qa", "film-v2r1", "media.json"), encoding="utf-8"))
M.update(json.load(io.open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "qa", "film-v2r1", "media-9x16.json"), encoding="utf-8")))
for n, v in M.items():
    if v.get("byte_check") != "OK":
        raise SystemExit("film_417: " + n + " was not byte-checked OK")
U = {n: v["url"].replace("'", "") for n, v in M.items()}
RELS = ["inc/project-stage.php"]
FILES = {}

V1_LINE = ("\t\t\t. '<figure class=\"nlws-film__fig\">' . $v( '16x9', 'wide' ) . $v( '9x16', 'tall' ) . '<figcaption>' . esc_html( $t[2] ) . "
           "'</figcaption></figure>'\n")
NEW_LINES = ("\t\t\t. nadlan_ps_world_film_v2( $k, $t[2] ) // v104.40: the narrated v2 film leads (Ben, 3.10 evening)\n"
             "\t\t\t. '<h3 class=\"nlws-film__v1h\">' . esc_html( array( 'he' => 'הגרסה הראשונה', 'en' => 'The first version', "
             "'fr' => 'La première version', 'ru' => 'Первая версия', 'ar' => 'النسخة الأولى' )[ $lang ] ?? 'הגרסה הראשונה' ) . '</h3>'\n"
             + V1_LINE)
FUNC = """
if ( ! function_exists( 'nadlan_ps_world_film_v2' ) ) {
	/** KikarHamedinaWorld v104.40 (3.10.2026 evening, Ben: "upload everything, with the narration too"; nothing about credit on the
	 *  page): the narrated v2 film leads the film section. Hebrew on he, English elsewhere; preload none, no autoplay; the film's own
	 *  title-card poster. The wide film over 700 px, the upright one on phones (the same pattern as V1). */
	function nadlan_ps_world_film_v2( $k, $cap ) {
		$s = array( 'he' => array( '16x9' => array( '@HE@', '@HEP@' ), '9x16' => array( '@HET@', '@HETP@' ) ),
			'en' => array( '16x9' => array( '@EN@', '@ENP@' ), '9x16' => array( '@ENT@', '@ENTP@' ) ) );
		$f = $s[ 'he' === $k ? 'he' : 'en' ];
		$v = function ( $fmt, $cls ) use ( $f ) {
			return '<video class="nlws-film__v nlws-film__v--' . $cls . '" controls playsinline preload="none" poster="' . esc_url( $f[ $fmt ][1] ) . '">'
				. '<source src="' . esc_url( $f[ $fmt ][0] ) . '" type="video/mp4"></video>';
		};
		return '<figure class="nlws-film__fig nlws-film__v2" id="nlws-film-v2">' . $v( '16x9', 'wide' ) . $v( '9x16', 'tall' ) . '<figcaption>' . esc_html( $cap ) . '</figcaption></figure>'
			. '<style id="nlws-v2-css">.nlws-film__v2{margin:0 0 26px}.nlws-film__v1h{margin:8px 0;font-size:18px}</style>';
	}
}
"""
for key, name in (("@HET@", "kikar-hamedina-film-v2-he-9x16.mp4"), ("@HETP@", "kikar-hamedina-film-v2-he-9x16-poster.jpg"),
                  ("@ENT@", "kikar-hamedina-film-v2-en-9x16.mp4"), ("@ENTP@", "kikar-hamedina-film-v2-en-9x16-poster.jpg"),
                  ("@HE@", "kikar-hamedina-film-v2-he-16x9.mp4"), ("@HEP@", "kikar-hamedina-film-v2-he-16x9-poster.jpg"),
                  ("@EN@", "kikar-hamedina-film-v2-en-16x9.mp4"), ("@ENP@", "kikar-hamedina-film-v2-en-16x9-poster.jpg")):
    FUNC = FUNC.replace(key, U[name])
FUNC_ANCHOR = "\nif ( ! function_exists( 'nadlan_ps_langs_on' ) ) {\n"


def apply(rel, txt):
    if "nadlan_ps_world_film_v2" in txt:
        raise SystemExit("film_417: already applied")
    for a in (V1_LINE, FUNC_ANCHOR):
        if txt.count(a) != 1:
            raise SystemExit("film_417: an anchor is there " + str(txt.count(a)) + " times: " + a.strip()[:70])
    return txt.replace(V1_LINE, NEW_LINES).replace(FUNC_ANCHOR, FUNC + FUNC_ANCHOR)
