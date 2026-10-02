# -*- coding: utf-8 -*-
"""The two hunks of release 1.72.401 (design v104.28): the Kikar film, low on the world page, in the page's language. Applied by
deploy401.py to the LIVE text of inc/project-stage.php (each anchor exactly once), and by --apply to the repo copy."""
import io, os, sys

U = "https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-"

A1 = ". $parts['tour'] . $parts['deals'] . '</div>';"
N1 = (". $parts['tour'] . $parts['deals'] . ( function_exists( 'nadlan_ps_world_film' ) ? nadlan_ps_world_film( $ps ) : '' ) . '</div>';"
      " // v104.28: the film, after the deals, outside the post content")

A2 = "if ( ! function_exists( 'nadlan_ps_langs_on' ) ) {\n"
N2 = r"""if ( ! function_exists( 'nadlan_ps_world_film' ) ) {
	/** KikarHamedinaWorld v104.28 (3.10.2026, the owner's order: "English goes to all the foreign languages and Hebrew to the Hebrew
	 *  ... somewhere downstairs"): the project's film after the deals, in the page's language. A native video with no autoplay and
	 *  no download until pressed (preload none); the wide film over 700 px, the upright one on phones; labelled as an illustration.
	 *  Hebrew film on the Hebrew page, the English film on en/fr/ru/ar. No VideoObject while the film is a draft for his decision. */
	function nadlan_ps_world_film( $ps ) {
		if ( empty( $ps['world'] ) || 'hamedina' !== (string) ( $ps['slug'] ?? '' ) ) { return ''; }
		$lang = (string) ( $ps['lang'] ?? 'he' );
		$T = array(
			'he' => array( 'הסרט של כיכר המדינה', 'דקה וחצי על הפרויקט: בחירת הדירה, הנוף מהקומות, העיצוב, המתקנים והסביבה.', 'הדמיה להמחשה', 'rtl' ),
			'en' => array( 'The Kikar Hamedina film', 'Ninety seconds on the project: choosing an apartment, the view from the floors, the finishes, the facilities and the area.', 'Illustrative visualisation', 'ltr' ),
			'fr' => array( 'Le film de Kikar Hamedina', 'Une minute et demie sur le projet : le choix d’un appartement, la vue depuis les étages, les finitions, les équipements et le quartier. Film en anglais.', 'Visualisation illustrative', 'ltr' ),
			'ru' => array( 'Фильм о Кикар ха-Медина', 'Полторы минуты о проекте: выбор квартиры, вид с этажей, отделка, удобства и район. Фильм на английском языке.', 'Иллюстративная визуализация', 'ltr' ),
			'ar' => array( 'فيلم كيكار همدينا', 'دقيقة ونصف عن المشروع: اختيار الشقة، الإطلالة من الطوابق، التشطيبات، المرافق والمنطقة. الفيلم باللغة الإنجليزية.', 'تصور توضيحي', 'rtl' ),
		);
		if ( ! isset( $T[ $lang ] ) ) { $lang = 'he'; }
		$t = $T[ $lang ];
		$k = 'he' === $lang ? 'he' : 'en';
		$u = '__U__';
		$v = function ( $f, $cls ) use ( $u, $k ) {
			return '<video class="nlws-film__v nlws-film__v--' . $cls . '" controls playsinline preload="none" poster="' . esc_url( $u . $k . '-' . $f . '-preview-poster.jpg' ) . '">'
				. '<source src="' . esc_url( $u . $k . '-' . $f . '-preview.mp4' ) . '" type="video/mp4"></video>';
		};
		return '<section class="nlws-film" id="nlws-film" dir="' . $t[3] . '" lang="' . esc_attr( $lang ) . '" aria-labelledby="nlws-film-h">'
			. '<h2 id="nlws-film-h">' . esc_html( $t[0] ) . '</h2><p class="nlws-film__p">' . esc_html( $t[1] ) . '</p>'
			. '<figure class="nlws-film__fig">' . $v( '16x9', 'wide' ) . $v( '9x16', 'tall' ) . '<figcaption>' . esc_html( $t[2] ) . '</figcaption></figure></section>'
			. '<style id="nlws-film-css">.nlws-film{max-width:1100px;margin:40px auto 8px;padding:0 16px}.nlws-film h2{margin:0 0 6px}'
			. '.nlws-film__p{margin:0 0 14px;max-width:62ch;color:#4A5560}.nlws-film__fig{margin:0}'
			. '.nlws-film__v{display:block;width:100%;height:auto;border-radius:16px;background:#14130F}'
			. '.nlws-film__v--tall{display:none;max-width:420px;margin:0 auto}'
			. '@media(max-width:700px){.nlws-film__v--wide{display:none}.nlws-film__v--tall{display:block}}'
			. '.nlws-film figcaption{margin-top:8px;font-size:13px;color:#6B6558}</style>';
	}
}

if ( ! function_exists( 'nadlan_ps_langs_on' ) ) {
""".replace("__U__", U)

HUNKS = [(A1, N1), (A2, N2)]

if __name__ == "__main__" and "--apply" in sys.argv:
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "inc", "project-stage.php")
    t = io.open(p, encoding="utf-8", newline="").read()
    crlf = "\r\n" in t
    t = t.replace("\r\n", "\n")
    for o, n in HUNKS:
        if t.count(o) != 1:
            raise SystemExit(f"repo anchor x{t.count(o)}: {o[:60]!r}")
        t = t.replace(o, n)
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
    print("applied to the repo copy")
