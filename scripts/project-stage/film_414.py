# -*- coding: utf-8 -*-
"""Release 1.72.414 (design v104.36; the film, option B as relayed by Maya 3.10.2026; her film-safe-slice verdict): the 19.7 s
facilities clip under the Kikar film. The label is a line ABOVE the player (before play), in the page's language: an illustrative
visualisation of the facilities, not footage, not an official specification, not a full tour. Facilities posters only;
controls playsinline preload="none", no autoplay; wide over 700 px, upright on phones; the Hebrew clip on he, the English one on
en/fr/ru/ar. V1 (the film above it) is untouched. The media URLs are the exact uploaded ones (docs/qa/film-facilities/media.json,
byte-checked). One hunk in nadlan_ps_world_film(), applied to the LIVE inc/project-stage.php text (the anchor once)."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(io.open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "qa", "film-facilities", "media.json"), encoding="utf-8"))
U = {n: v["url"] for n, v in M.items()}
for n, v in M.items():
    if v.get("byte_check") != "OK":
        raise SystemExit("film_414: " + n + " was not byte-checked OK")

ANCHOR = ("\t\t\t. '<figure class=\"nlws-film__fig\">' . $v( '16x9', 'wide' ) . $v( '9x16', 'tall' ) . '<figcaption>' . esc_html( $t[2] ) . "
          "'</figcaption></figure></section>'\n")


def _u(n):
    return U[n].replace("'", "")


NEW = ("\t\t\t. '<figure class=\"nlws-film__fig\">' . $v( '16x9', 'wide' ) . $v( '9x16', 'tall' ) . '<figcaption>' . esc_html( $t[2] ) . "
       "'</figcaption></figure>'\n"
       "\t\t\t. nadlan_ps_world_facilities_clip( $lang, $k ) . '</section>' // v104.36: the facilities clip, labelled before play (option B)\n")

FUNC = """
if ( ! function_exists( 'nadlan_ps_world_facilities_clip' ) ) {
	/** KikarHamedinaWorld v104.36 (3.10.2026, the film, option B; Maya's film-safe-slice verdict): the 19.7 s facilities clip
	 *  (pool, gym, spa, car park; our own rooms, no map layer; music only) under the film. The label is above the player, so it
	 *  is read before play. Facilities posters only; preload none, no autoplay. The URLs are the uploaded files, byte-checked. */
	function nadlan_ps_world_facilities_clip( $lang, $k ) {
		$F = array(
			'he' => array( 'המתקנים בבניין: בריכה, חדר כושר, ספא וחניון', 'הדמיית מתקנים להמחשה: לא צילום ולא מפרט רשמי, ואינה סיור מלא בפרויקט.' ),
			'en' => array( "The building's facilities: pool, gym, spa and car park", 'An illustrative visualisation of the facilities: not footage, not an official specification, and not a full tour of the project.' ),
			'fr' => array( "Les équipements de l'immeuble : piscine, salle de sport, spa et parking", "Une visualisation illustrative des équipements : ni un tournage, ni une spécification officielle, ni une visite complète du projet. Libellés en anglais." ),
			'ru' => array( 'Удобства в здании: бассейн, спортзал, спа и паркинг', 'Иллюстративная визуализация удобств: не съёмка, не официальная спецификация и не полный тур по проекту. Подписи на английском.' ),
			'ar' => array( 'مرافق المبنى: المسبح، النادي الرياضي، السبا وموقف السيارات', 'تصوّر توضيحي للمرافق: ليس تصويرًا حقيقيًا ولا مواصفات رسمية، وليس جولة كاملة في المشروع. التسميات بالإنجليزية.' ),
		);
		$f = isset( $F[ $lang ] ) ? $F[ $lang ] : $F['he'];
		$src = array(
			'he' => array( '16x9' => array( '@HE169@', '@HE169P@' ), '9x16' => array( '@HE916@', '@HE916P@' ) ),
			'en' => array( '16x9' => array( '@EN169@', '@EN169P@' ), '9x16' => array( '@EN916@', '@EN916P@' ) ),
		);
		$s = $src[ 'he' === $k ? 'he' : 'en' ];
		$v = function ( $fmt, $cls ) use ( $s ) {
			return '<video class="nlws-film__v nlws-film__v--' . $cls . '" controls playsinline preload="none" poster="' . esc_url( $s[ $fmt ][1] ) . '">'
				. '<source src="' . esc_url( $s[ $fmt ][0] ) . '" type="video/mp4"></video>';
		};
		return '<div class="nlws-film__fac" id="nlws-facilities"><h3>' . esc_html( $f[0] ) . '</h3><p class="nlws-film__lbl">' . esc_html( $f[1] ) . '</p>'
			. '<figure class="nlws-film__fig">' . $v( '16x9', 'wide' ) . $v( '9x16', 'tall' ) . '</figure></div>'
			. '<style id="nlws-fac-css">.nlws-film__fac{margin-top:28px}.nlws-film__fac h3{margin:0 0 6px;font-size:20px}'
			. '.nlws-film__lbl{margin:0 0 12px;max-width:62ch;font-size:14px;color:#4A4740;background:#F3EEE3;border-radius:10px;padding:8px 12px}'
			. '.nlws-film__fac .nlws-film__v--tall{max-width:360px}</style>';
	}
}
"""
for key, name in (("@HE169@", "kikar-hamedina-facilities-he-16x9.mp4"), ("@HE169P@", "kikar-hamedina-facilities-he-16x9-poster.jpg"),
                  ("@HE916@", "kikar-hamedina-facilities-he-9x16.mp4"), ("@HE916P@", "kikar-hamedina-facilities-he-9x16-poster.jpg"),
                  ("@EN169@", "kikar-hamedina-facilities-en-16x9.mp4"), ("@EN169P@", "kikar-hamedina-facilities-en-16x9-poster.jpg"),
                  ("@EN916@", "kikar-hamedina-facilities-en-9x16.mp4"), ("@EN916P@", "kikar-hamedina-facilities-en-9x16-poster.jpg")):
    FUNC = FUNC.replace(key, _u(name))
FUNC_ANCHOR = "\nif ( ! function_exists( 'nadlan_ps_langs_on' ) ) {\n"


def apply(txt):
    if "nadlan_ps_world_facilities_clip" in txt:
        raise SystemExit("film_414: already applied")
    for a in (ANCHOR, FUNC_ANCHOR):
        if txt.count(a) != 1:
            raise SystemExit("film_414: an anchor is there " + str(txt.count(a)) + " times: " + a.strip()[:70])
    return txt.replace(ANCHOR, NEW).replace(FUNC_ANCHOR, FUNC + FUNC_ANCHOR)
