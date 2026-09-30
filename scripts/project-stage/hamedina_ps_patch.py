# -*- coding: utf-8 -*-
"""KikarHamedinaWorld (design system v104, HAD-375, phase P7a): the change to inc/project-stage.php, as anchored hunks.

Why hunks and not the branch file: the branch's inc/project-stage.php also carries Batch 1/2 (v101, v101.2, v102), which are
LOCAL ONLY and wait for Codex's acceptance. The release must add Kikar Hamedina and nothing else, so the file that goes live
is the LIVE base (65af09be, md5 9e03f257..., written by 1.72.361) + these hunks. The same hunks were applied to the branch
file, so the two never drift: gen_deploy369.py checks that every hunk's new text is in the branch file and builds the release
copy from `git show 65af09be:...` (each anchor must match exactly once, in both).

  python scripts/project-stage/hamedina_ps_patch.py --branch     rebuild the working file as git HEAD + every hunk
  python scripts/project-stage/hamedina_ps_patch.py --check      show which hunks the working file and 65af09be carry
"""
import io, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REL = "plugins/nadlan-config/inc/project-stage.php"
BASE_COMMIT = "65af09be"

# ------------------------------------------------------------------------------------------------ 1. the config entry
CONFIG_ANCHOR = """					array( 195, 240, 'לכיוון הצפון הישן' ),
				),
			),
		);
	}
}
"""
CONFIG_NEW = """					array( 195, 240, 'לכיוון הצפון הישן' ),
				),
			),
			// KikarHamedinaWorld v104 (30.9.2026, HAD-375): Kikar Hamedina Towers on the SHARED world module
			// (assets/project-stage/world/world.js, mountWorld), not a stage.js copy: one walkable scene of the whole area
			// (docs/design/kikar-hamedina/KikarHamedinaWorld-v104-README.md). Every fact below is in
			// docs/research/2026-09-30-kikar-hamedina/facts.md or area.md with its source. No interiors ship yet: no 'units', no
			// 360, no tour words (the world branch never prints Rainbow's). The URL word law: "hamedina" is owned by this page.
			'hamedina' => array(
				'dir'            => 'hamedina',
				'mount'          => 'mountWorld',
				'world'          => array(
					'data'   => 'world.json',
					'poster' => array( 'wide' => 'poster-1600', 'tall' => 'poster-800', 'w' => 1600, 'h' => 1000, 'tw' => 800 ),
					'mode'   => 'aerial',
					'season' => 9,
					'hour'   => 10,
					'pond'   => true, // the pond is sourced (Mako 24.9.2026: 1 m deep); its outline is drawn and labelled "הדמיה להמחשה בלבד"
				),
				'bearing_offset' => 0,
				'name'           => 'מגדלי כיכר המדינה',
				'name_en'        => 'Kikar Hamedina Towers',
				'h1_he'          => 'מגדלי כיכר המדינה, תל אביב', // the design's H1 (serp-dna.md): the searched name and the city
				'developer'      => 'בנייה: אלקטרה ואשטרום', // the developers are the landowners; Electra and Ashtrom build (Globes 14.12.2022)
				'place'          => 'כיכר המדינה, צפון תל אביב',
				'rail'           => array(),
				'poster_alt'     => 'הדמיה של מגדלי כיכר המדינה בתל אביב: שלושה מגדלים מסתובבים סביב הפארק והאגם, בלב טבעת הבניינים של הכיכר ובתוך העיר עד הים',
				'src_line'       => 'מקורות ההדמיה: הבניינים, הגבהים, הרחובות, הגנים והעצים לפי עיריית <span>תל אביב-יפו</span> (מידע גאוגרפי פתוח, 9.2026); המגדלים לפי קונטור הבניין במאגר העירייה והסיבוב שפורסם, 1.25° בכל קומה. מיקום האגם והמתקנים בפארק להמחשה בלבד.',
				// ProjectFacts: six quick facts, each with its source (facts.md 1.4, 1.5, 1.8; area.md 1)
				'facts'          => array(
					array( 'מיקום', 'כיכר המדינה, תל אביב', 'על טבעת רחוב ה׳ באייר, צפון העיר' ),
					array( 'מגדלים', '3 מגדלים מסתובבים', '40, 40 ו-37 קומות, לפי ויקיפדיה ואשטרום' ),
					array( 'דירות', '453', 'לפי אשטרום וגלובס' ),
					array( 'הסיבוב', '1.25° בכל קומה', 'כ-50° לאורך מגדל של 40 קומות, לפי ויקיפדיה' ),
					array( 'הפארק', 'כ-40 דונם', 'עם אגם אקולוגי, בית ספר ומרכז קהילתי, לפי גלובס ומאקו' ),
					array( 'מצב', 'השלד הושלם', 'ב-23.4.2026, לפי רישום אתר הבנייה בעירייה' ),
				),
				// ProjectProgress: the plan in force 24.6.2013, the permit 12.2022 (Globes), the frame 23.4.2026 (TLV GIS 499); the
				// delivery is not one date: the statements are a dated table in the page's text (Ashtrom 2026 ... Bizportal end of 2028)
				'progress'       => array(
					array( 'תכנית', '6.2013', 'done' ),
					array( 'היתר בנייה', '12.2022', 'done' ),
					array( 'השלד הושלם', '4.2026', 'done' ),
					array( 'בבנייה', 'עכשיו', 'now' ),
					array( 'אכלוס', 'לפי המקורות, 2026 עד 2028', 'next' ),
				),
				// ProjectDeals: the three deals the press tied to a floor (Globes 2.5.2025, did=1001508911); which tower was not
				// published, so no row opens a floor (n = 0). No buyer is named.
				'deals_intro'    => 'שלוש העסקאות במגדלים שפורסמו עם הקומה שלהן, כולן דירות 4 חדרים של 140 מ״ר, לפי גלובס (2.5.2025). באיזה מגדל נמכרה כל דירה לא פורסם, ולא כל העסקאות פורסמו.',
				'deals'          => array(
					array( 'floor' => '38', 'n' => 0, 'bld' => 'המגדל לא פורסם', 'apt' => '4 חדרים · 140 מ״ר', 'price' => '10.63 מיליון ₪', 'psqm' => 'כ-75,900 ₪', 'date' => '12.2024', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001508911', 'via' => '' ),
					array( 'floor' => '39', 'n' => 0, 'bld' => 'המגדל לא פורסם', 'apt' => '4 חדרים · 140 מ״ר', 'price' => '9.59 מיליון ₪', 'psqm' => 'כ-68,500 ₪', 'date' => '5.2024', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001508911', 'via' => '' ),
					array( 'floor' => '38', 'n' => 0, 'bld' => 'המגדל לא פורסם', 'apt' => '4 חדרים · 140 מ״ר', 'price' => '9.58 מיליון ₪', 'psqm' => 'כ-68,400 ₪', 'date' => '4.2024', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001508911', 'via' => '' ),
				),
				// the area price line (facts.md 1.14 and 3): the towers' average per the press, the Tax Authority's deals around the square
				'deals_sum'      => array(
					array( '9.58 עד 10.63 מיליון ₪', 'שלוש דירות 4 חדרים בקומות 38 ו-39, 4.2024 עד 12.2024, לפי גלובס' ),
					array( 'כ-65,000 ₪ למ״ר', 'ממוצע העסקאות במגדלים, ובקומות הגבוהות ובפנטהאוזים 80,000 עד 150,000 ₪ למ״ר, לפי מאקו (24.9.2026)' ),
					array( '63,000 עד 66,000 ₪ למ״ר', 'רוב העסקאות סביב כיכר המדינה בשנה האחרונה, לפי נתוני רשות המסים (ice, 28.4.2026)' ),
				),
				// the plot centre (area.md 1: the area-weighted centre of plan 2500ב's lots 101, 201-208 and 303, TLV GIS 837)
				'tower_lat'      => 32.086758,
				'tower_lng'      => 34.789776,
				// what lies that way from the plot centre, true bearings (sight-landmarks.json, 30.9.2026): the sea 293°, the port 314°,
				// Reading 327-334°, Sportek 355°, Ramat Aviv 12°, the university 27°, Park HaYarkon 55°, Moshe Aviv 106°, Savidor 109°,
				// Azrieli 170-173°, Sarona 183°, Habima 213°, City Hall 238°
				'sectors'        => array(
					array( 250, 345, 'לכיוון הים ונמל תל אביב' ),
					array( 345, 70, 'לכיוון פארק הירקון ורמת אביב' ),
					array( 70, 140, 'לכיוון רמת גן ותחנת סבידור' ),
					array( 140, 200, 'לכיוון מגדלי עזריאלי' ),
					array( 200, 250, 'לכיוון כיכר רבין ומרכז העיר' ),
				),
				// the English page's own words (the world branch prints them directly: nothing waits for a dictionary)
				'i18n'           => array(
					'en' => array(
						'name'       => 'Kikar Hamedina Towers',
						'developer'  => 'Built by Electra and Ashtrom',
						'place'      => 'Kikar Hamedina, north Tel Aviv',
						'poster_alt' => 'Illustration of Kikar Hamedina Towers in Tel Aviv: three twisting towers around the park and the pond, inside the square’s ring of buildings, with the city stretching to the sea',
						'src_line'   => 'Sources of the illustration: buildings, heights, streets, gardens and trees from the <span>Tel Aviv-Yafo</span> municipality (open GIS data, 9.2026); the towers from the municipal building outline and the published turn of 1.25° per floor. The places of the pond and of the park’s features are illustrative.',
						'facts'      => array(
							array( 'Location', 'Kikar Hamedina, Tel Aviv', 'On the He Be’Iyar ring road, north Tel Aviv' ),
							array( 'Towers', '3 twisting towers', '40, 40 and 37 floors, per Wikipedia and Ashtrom' ),
							array( 'Apartments', '453', 'Per Ashtrom and Globes' ),
							array( 'The twist', '1.25° per floor', 'About 50° over a 40-floor tower, per Wikipedia' ),
							array( 'The park', 'About 40 dunams', 'With an ecological pond, a school and a community centre, per Globes and Mako' ),
							array( 'Status', 'Frame completed', 'On 23.4.2026, per the municipal building-site record' ),
						),
						'progress'   => array(
							array( 'Plan', '6.2013', 'done' ),
							array( 'Building permit', '12.2022', 'done' ),
							array( 'Frame completed', '4.2026', 'done' ),
							array( 'Construction', 'now', 'now' ),
							array( 'Occupancy', 'per the sources, 2026 to 2028', 'next' ),
						),
					),
				),
			),
		);
	}
}
"""

# ------------------------------------------------------------------------------------------------ 2. the page's stage check
CURRENT_ANCHOR = """		$file = dirname( __DIR__ ) . '/assets/project-stage/' . $all[ $slug ]['dir'] . '/stage.js';
		if ( ! file_exists( $file ) ) { return $memo; }
"""
CURRENT_NEW = """		// KikarHamedinaWorld v104: a project on the shared world module needs the module and its world data, not a stage.js
		$world = ! empty( $all[ $slug ]['world'] );
		$file  = dirname( __DIR__ ) . '/assets/project-stage/' . ( $world ? 'world/world.js' : $all[ $slug ]['dir'] . '/stage.js' );
		if ( ! file_exists( $file ) || ( $world && ! is_readable( dirname( __DIR__ ) . '/assets/project-stage/' . $all[ $slug ]['dir'] . '/world.json' ) ) ) { return $memo; }
"""

# ------------------------------------------------------------------------------------------------ 3. the parts: the world's own
PARTS_ANCHOR = """	function nadlan_ps_parts( $ps, $h1, $map ) {
		$id  = (int) $ps['id'];
"""
PARTS_NEW = """	function nadlan_ps_parts( $ps, $h1, $map ) {
		if ( ! empty( $ps['world'] ) && function_exists( 'nadlan_ps_world_parts' ) ) { return nadlan_ps_world_parts( $ps, $h1, $map ); } // KikarHamedinaWorld v104
		$id  = (int) $ps['id'];
"""

# ------------------------------------------------------------------------------------------------ 4. the grid's modifier
PAGE_ANCHOR = """		$page = '<div class="nlps-page" dir="rtl" lang="he">' . $parts['hero']"""
PAGE_NEW = """		$page = '<div class="nlps-page' . ( ! empty( $ps['world'] ) ? ' nlps-page--world' : '' ) . '" dir="rtl" lang="he">' . $parts['hero']"""

# ------------------------------------------------------------------------------------------------ 5. the head: the poster only
HEAD_ANCHOR = """	echo '<link rel="modulepreload" href="https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js" crossorigin>' . "\\n";
	$ps   = nadlan_ps_current();
"""
HEAD_NEW = """	$ps   = nadlan_ps_current();
	// KikarHamedinaWorld v104: on a world page three.js and the world load on intent, after the page has painted: the head holds
	// the import map and the first picture only
	if ( ! empty( $ps['world'] ) && function_exists( 'nadlan_ps_world_head' ) ) { nadlan_ps_world_head( $ps ); return; }
	echo '<link rel="modulepreload" href="https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js" crossorigin>' . "\\n";
"""

# ------------------------------------------------------------------------------------------------ 6. the footer: the world, not bridge.js
FOOT_ANCHOR = """add_action( 'wp_footer', function () {
	if ( ! nadlan_ps_current() ) { return; }
	$src = plugins_url( 'assets/project-stage/bridge.js', dirname( __FILE__ ) ) . '?ver=' . nadlan_ps_ver();
"""
FOOT_NEW = """add_action( 'wp_footer', function () {
	if ( ! nadlan_ps_current() ) { return; }
	$wps = nadlan_ps_current();
	if ( ! empty( $wps['world'] ) && function_exists( 'nadlan_ps_world_script' ) ) { echo nadlan_ps_world_script( $wps ); return; } // KikarHamedinaWorld v104: the world draws its own floor view
	$src = plugins_url( 'assets/project-stage/bridge.js', dirname( __FILE__ ) ) . '?ver=' . nadlan_ps_ver();
"""

# ------------------------------------------------------------------------------------------------ 7. the world's functions + style
FUNCS_ANCHOR = """/* The visible H1 of a project page without a stage (design system ProjectTitle, version 39; Linear HAD-332; checklist C1).
"""
FUNCS_NEW = r"""/* KikarHamedinaWorld (design system v104, 30.9.2026, HAD-375): a project page on the SHARED world module
   (assets/project-stage/world/world.js, mountWorld) instead of a per-project stage.js copy. The page keeps the fleet's order
   (checklist C1-C8: the H1, the answer paragraph, the buttons, the stage, the map, the facts, the tools, the article); the world
   is one walkable scene of the whole area with four ways in (the aerial view, a walk, a tower's floor and view with the sun,
   what is nearby). Everything here runs only for a config with 'world' (Kikar Hamedina today): the four stage projects never
   reach it, so their pages stay byte for byte as they were. There is no bridge.js on these pages: the world draws its own view
   from the floor and sets window.__nlpsPick for the WhatsApp source line. No interiors ship yet, so there is no 360, no
   example apartment and no steps row. */
if ( ! function_exists( 'nadlan_ps_world_words' ) ) {
	/** The page top's own words in the page's language; the world speaks Hebrew and English (fr, ru, ar come at P8). */
	function nadlan_ps_world_words( $lang ) {
		$w = array(
			'he' => array(
				'wa'    => 'ייעוץ חינם',
				'wa_tx' => 'שלום, אשמח לייעוץ חינם על %s (nad-lan.co.il)',
				'sale'  => 'דירות למכירה במגדלים',
				'tour'  => 'סיור וירטואלי בכיכר',
				'stage' => 'סיור וירטואלי ב%s: המגדלים, הקומות והנוף',
				'hint'  => 'בחרו מגדל, קומה וכיוון, וראו בהדמיה את הנוף ואת שעות השמש מהחלון. אפשר גם לצאת לסיור ברגל בכיכר ובפארק, ולגלות מה נמצא במרחק הליכה.',
				'facts' => 'עובדות בקצרה',
				'prog'  => 'שלב הפרויקט',
				'rail'  => 'אנשי מקצוע באזור',
			),
			'en' => array(
				'wa'    => 'Free advice',
				'wa_tx' => 'Hello, I would like free advice on %s (nad-lan.co.il)',
				'sale'  => 'Apartments for sale in the towers',
				'tour'  => 'Virtual tour of the square',
				'stage' => 'Virtual tour of %s: the towers, the floors and the view',
				'hint'  => 'Choose a tower, a floor and a facing to see an illustration of the view and the hours of sun from the window. Or take a walk around the square and the park, and discover what lies within walking distance.',
				'facts' => 'Key facts',
				'prog'  => 'Project stage',
				'rail'  => 'Professionals in the area',
			),
		);
		return isset( $w[ $lang ] ) ? $w[ $lang ] : $w['en'];
	}
}
if ( ! function_exists( 'nadlan_ps_world_media' ) ) {
	/** The world's first picture: a wide frame for screens over 700 px and an upright one for phones (the same scene). */
	function nadlan_ps_world_media( $ps ) {
		$base = 'assets/project-stage/' . $ps['dir'] . '/';
		$v    = '?ver=' . nadlan_ps_ver();
		$pw   = (array) ( $ps['world']['poster'] ?? array() );
		$wide = (string) ( $pw['wide'] ?? 'poster-1600' );
		$tall = (string) ( $pw['tall'] ?? 'poster-800' );
		return array(
			'jpg'  => plugins_url( $base . $wide . '.jpg', dirname( __FILE__ ) ) . $v,
			'wide' => plugins_url( $base . $wide . '.webp', dirname( __FILE__ ) ) . $v,
			'tall' => plugins_url( $base . $tall . '.webp', dirname( __FILE__ ) ) . $v,
			'w'    => (int) ( $pw['w'] ?? 1600 ),
			'h'    => (int) ( $pw['h'] ?? 1000 ),
			'tw'   => (int) ( $pw['tw'] ?? 800 ),
		);
	}
}
if ( ! function_exists( 'nadlan_ps_world_parts' ) ) {
	/** The pieces of a world page's top, in the same keys as nadlan_ps_parts(); $h1 is the page's own h1 text. */
	function nadlan_ps_world_parts( $ps, $h1, $map ) {
		$lang = (string) ( $ps['lang'] ?? 'he' );
		$he   = 'he' === $lang;
		$tl   = $he ? 'he' : 'en';
		$L    = $he ? $ps : array_merge( $ps, (array) ( $ps['i18n'][ $lang ] ?? ( $ps['i18n']['en'] ?? array() ) ) );
		$T    = nadlan_ps_world_words( $tl );
		$la   = ' dir="' . ( in_array( $lang, array( 'he', 'ar' ), true ) ? 'rtl' : 'ltr' ) . '" lang="' . esc_attr( $lang ) . '"';
		$wa   = function_exists( 'nadlan_cta_whatsapp_number' ) ? preg_replace( '/\D/', '', (string) nadlan_cta_whatsapp_number() ) : '';
		$name = (string) $L['name'];
		$link = '' !== $wa ? 'https://wa.me/' . $wa . '?text=' . rawurlencode( sprintf( $T['wa_tx'], $name ) ) : '';
		$m    = nadlan_ps_world_media( $ps );
		$v    = '?ver=' . nadlan_ps_ver();
		$base = 'assets/project-stage/' . $ps['dir'] . '/';
		$pw   = (array) $ps['world'];
		$alt  = (string) ( $L['poster_alt'] ?? $name );
		$cfg  = array(
			'world'  => plugins_url( 'assets/project-stage/world/world.js', dirname( __FILE__ ) ) . $v,
			'data'   => plugins_url( $base . (string) ( $pw['data'] ?? 'world.json' ), dirname( __FILE__ ) ) . $v,
			'places' => is_readable( dirname( __DIR__ ) . '/' . $base . 'places.json' ) ? plugins_url( $base . 'places.json', dirname( __FILE__ ) ) . $v : '',
			'lang'   => $tl,
			'name'   => $name,
			'wa'     => $link,
			'mode'   => (string) ( $pw['mode'] ?? 'aerial' ),
			'season' => (int) ( $pw['season'] ?? 9 ),
			'hour'   => (int) ( $pw['hour'] ?? 10 ),
			'pond'   => ! array_key_exists( 'pond', $pw ) || ! empty( $pw['pond'] ),
			'poster' => array( 'src' => $m['jpg'], 'srcset' => $m['tall'] . ' ' . $m['tw'] . 'w, ' . $m['wide'] . ' ' . $m['w'] . 'w', 'sizes' => '(max-width:700px) 100vw, 70vw', 'alt' => $alt ),
		);
		$hero = '';
		$cta  = '';
		if ( '' !== $h1 ) {
			$en   = (string) ( $ps['name_en'] ?? '' );
			$hero = '<header class="nlds nlps-herowrap"' . $la . '><div class="nlps-hero">'
				. ( $he
					? '<h1 id="nl-project-page-title" class="nlps-h1">' . esc_html( (string) ( $ps['h1_he'] ?? $ps['name'] ) ) . ( '' !== $en ? ' <span class="nlps-h1__en" lang="en">' . esc_html( $en ) . '</span>' : '' ) . '</h1>'
					: '<h1 id="nl-project-page-title" class="nlps-h1">' . esc_html( $h1 ) . '</h1>' ) // the language page's own title
				. ( ! empty( $L['developer'] ) || ! empty( $L['place'] ) ? '<div class="nlps-kicker">' . ( ! empty( $L['developer'] ) ? '<b>' . esc_html( $L['developer'] ) . '</b>' : '' ) . ( ! empty( $L['developer'] ) && ! empty( $L['place'] ) ? ' · ' : '' ) . esc_html( (string) ( $L['place'] ?? '' ) ) . '</div>' : '' )
				. '</div></header>';
			// the design's three buttons: free advice on WhatsApp (one tap), the apartments for sale, the virtual tour
			$cta  = '<div class="nlds nlps-ctawrap"' . $la . '><div class="nlps-hero__cta">'
				. ( '' !== $wa ? '<a class="nlds-btn nlds-btn--primary" target="_blank" rel="noopener" data-nlps-ev="hero-wa" href="https://wa.me/' . esc_attr( $wa ) . '?text=' . rawurlencode( sprintf( $T['wa_tx'], $name ) ) . '">' . ( function_exists( 'nlds_icon' ) ? nlds_icon( 'whatsapp' ) : '' ) . '<span>' . esc_html( $T['wa'] ) . '</span></a>' : '' )
				. '<a class="nlds-btn nlds-btn--secondary" href="#nlws-sale" data-nlps-ev="hero-sale"><span>' . esc_html( $T['sale'] ) . '</span></a>'
				. '<a class="nlds-btn nlds-btn--secondary" href="#nlps-t" data-nlps-ev="hero-world"><span>' . esc_html( $T['tour'] ) . '</span></a>'
				. '</div></div>';
		}
		// the first picture, painted with the page (a wide frame, an upright one on phones); the world adopts the same files
		$pic = '<picture class="nlps-ssr-pic"><source media="(max-width:700px)" type="image/webp" srcset="' . esc_url( $m['tall'] ) . '"><source type="image/webp" srcset="' . esc_url( $m['wide'] ) . '">'
			. '<img class="nlps-ssr-poster" src="' . esc_url( $m['jpg'] ) . '" width="' . (int) $m['w'] . '" height="' . (int) $m['h'] . '" alt="' . esc_attr( $alt ) . '" fetchpriority="high" decoding="async"></picture>';
		$src = ! empty( $L['src_line'] ) ? '<p class="nlps-src">' . wp_kses( (string) $L['src_line'], array( 'span' => array() ) ) . '</p>' : '';
		$stagebox = '<div class="nlps-stagebox"><h2 class="nlps-srt" id="nlps-t">' . esc_html( sprintf( $T['stage'], $name ) ) . '</h2>'
			. '<section class="nlps-stage nlps-stage--world" id="nlps" aria-labelledby="nlps-t" data-cfg="' . esc_attr( wp_json_encode( $cfg ) ) . '"><div class="nlps-stage__mount" id="nlps-stage">' . $pic . '</div></section>'
			. '<div class="nlds"' . $la . '><p class="nlps-hint" id="nlps-hint">' . esc_html( $T['hint'] ) . '</p>' . $src . '</div></div>';
		$rail = '';
		foreach ( (array) ( $ps['rail'] ?? array() ) as $pid ) { $rail .= nadlan_ps_square( $pid, $ps ); }
		if ( $he ) { $rail .= nadlan_ps_slot(); }
		$rail = '' !== $rail ? '<aside class="nlps-rail" aria-label="' . esc_attr( $T['rail'] ) . '">' . $rail . '</aside>' : '';
		$facts = '';
		if ( ! empty( $L['facts'] ) || ! empty( $L['progress'] ) ) {
			$facts = '<div class="nlds nlps-factswrap"' . $la . '>';
			if ( ! empty( $L['facts'] ) ) {
				$facts .= '<div class="nlpf" role="list" aria-label="' . esc_attr( $T['facts'] ) . '">';
				foreach ( (array) $L['facts'] as $f ) {
					$facts .= '<div class="nlpf__item" role="listitem"><p class="nlpf__k">' . esc_html( $f[0] ) . '</p><p class="nlpf__v">' . esc_html( $f[1] ) . '</p>' . ( ! empty( $f[2] ) ? '<p class="nlpf__s">' . esc_html( $f[2] ) . '</p>' : '' ) . '</div>';
				}
				$facts .= '</div>';
			}
			if ( ! empty( $L['progress'] ) ) {
				$facts .= '<ol class="nlprog" aria-label="' . esc_attr( $T['prog'] ) . '">';
				foreach ( (array) $L['progress'] as $st ) {
					$cls = 'done' === $st[2] ? ' is-done' : ( 'now' === $st[2] ? ' is-now' : '' );
					$facts .= '<li class="nlprog__step' . $cls . '"' . ( 'now' === $st[2] ? ' aria-current="step"' : '' ) . '><b>' . esc_html( $st[0] ) . '</b>' . esc_html( $st[1] ) . '</li>';
				}
				$facts .= '</ol>';
			}
			$facts .= '</div>';
		}
		// one map on the page (the recipe, row 18): the area map, right under the world; the view from a floor is in the world itself
		$below = '' !== $map ? '<div class="nlps-below nlps-below--solo">' . $map . '</div>' : '';
		return array( 'hero' => $hero, 'cta' => $cta, 'stagebox' => $stagebox, 'rail' => $rail, 'facts' => $facts, 'below' => $below, 'tour' => '', 'deals' => $he ? nadlan_ps_deals( $ps ) : '' );
	}
}
if ( ! function_exists( 'nadlan_ps_world_head' ) ) {
	/** The world page's head: the first picture, fetched at once (the phone's or the wide one); three.js waits for intent. */
	function nadlan_ps_world_head( $ps ) {
		$m = nadlan_ps_world_media( $ps );
		echo '<link rel="preload" as="image" type="image/webp" href="' . esc_url( $m['tall'] ) . '" media="(max-width:700px)" fetchpriority="high">' . "\n";
		echo '<link rel="preload" as="image" type="image/webp" href="' . esc_url( $m['wide'] ) . '" media="(min-width:701px)" fetchpriority="high">' . "\n";
	}
}
if ( ! function_exists( 'nadlan_ps_world_script' ) ) {
	/** The world on the page: mountWorld() once the page has painted (idle after load); the 3D itself starts when the stage is
	 *  in view or on the tour button. The consult links in the page's text (#nlws-wa) open the same WhatsApp message. */
	function nadlan_ps_world_script( $ps ) {
		$js = <<<'NLWJS'
const root = document.getElementById('nlps'), host = document.getElementById('nlps-stage');
let c = {};
try { c = JSON.parse((root && root.dataset.cfg) || '{}'); } catch (e) { c = {}; }
const ga = (n, p) => { try { if (window.nadlanGA) window.nadlanGA(n, Object.assign({ project: c.name || '' }, p || {})); } catch (e) { /* none */ } };
let P = null;
function mount() {
  if (P) return P;
  P = import(c.world).then((m) => {
    const w = m.mountWorld(host, { dataUrl: c.data, placesUrl: c.places || null, lang: c.lang, name: c.name, wa: c.wa || null, poster: c.poster,
      intent: 'visible', mode: c.mode, season: c.season, hour: c.hour, pond: c.pond !== false });
    window.__nlpsWorld = w;
    // the page's own first picture steps aside once the world's copy of it (the same files) is painted
    const own = host.querySelector('.nlps-ssr-pic'), wp = host.querySelector('.nlw-poster');
    const drop = () => { if (own && own.parentNode) own.remove(); };
    if (wp && wp.decode) wp.decode().then(drop, () => setTimeout(drop, 1500)); else setTimeout(drop, 1500);
    return w;
  }).catch((e) => { console.warn('[world]', e); P = null; return null; });
  return P;
}
if (root && host && c.world) {
  const later = () => ('requestIdleCallback' in window ? requestIdleCallback(mount, { timeout: 2000 }) : setTimeout(mount, 200));
  if (document.readyState === 'complete') later(); else addEventListener('load', later, { once: true });
  document.addEventListener('click', (e) => {
    const a = e.target && e.target.closest ? e.target.closest('[data-nlps-ev="hero-world"],[data-nlps-ev="hero-sale"]') : null;
    if (!a) return;
    const ev = a.getAttribute('data-nlps-ev');
    ga('stage_step', { step: ev });
    if (ev !== 'hero-world') return;
    // the whole world in view, its foot at the screen's foot (clear of the site's sticky header), then the walk
    e.preventDefault();
    root.scrollIntoView({ block: 'end', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    mount().then((w) => { if (w) w.setMode('walk', 'user'); });
  });
  if (c.wa) for (const a of document.querySelectorAll('a[href="#nlws-wa"]')) { a.href = c.wa; a.target = '_blank'; a.rel = 'noopener'; }
  addEventListener('nl:floor', (e) => { const d = e.detail || {}; if (d.source === 'user') ga('stage_floor', { tower: d.tower, floor: d.floor }); });
  addEventListener('nl:facing', (e) => { const d = e.detail || {}; if (d.source === 'user') ga('stage_facing', { tower: d.tower, floor: d.floor, facing: d.facing }); });
}
NLWJS;
		return "\n" . '<script type="module" id="nadlan-ps-world">' . "\n" . $js . '</script>' . "\n";
	}
}
/* The world page's own layout and the style of its text sections (.nlws: the facts table, the prices, when it is ready, the
   timeline, the park, the square, the transport and the FAQ in the post's content), after the stage pages' layout. */
add_action( 'wp_head', function () {
	$ps = nadlan_ps_current();
	if ( ! $ps || empty( $ps['world'] ) ) { return; }
	$pc = 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > section.nlws';
	echo '<style id="nadlan-ps-world-css">'
		// the first fold: the text column and the world side by side (no rail column: the world needs the width); the
		// professionals' square goes to the end of the page top
		. ':root body .nlps-page.nlps-page--world{grid-template-columns:minmax(300px,380px) minmax(0,1fr);grid-template-areas:"hero stage" "lead stage" "cta stage" "below below" "facts facts" "deals deals" "rail rail"}'
		. ':root body .nlps-page--world>.nlps-rail{grid-template-columns:repeat(auto-fill,minmax(240px,320px));margin-top:6px!important}'
		. ':root body .nlps-page--world .nlps-stage--world{height:clamp(560px,calc(100svh - 190px),760px)}'
		. ':root body .nlps-stage--world .nlps-ssr-pic{position:absolute;inset:0;display:block}'
		. ':root body .nlps-stage--world .nlps-ssr-poster{object-position:50% 50%}'
		. ':root body .nlps-stage--world .nlw:not(.nlw--full){background:transparent}'
		. ':root body .nlps-page--world .nlds .nlps-hint{margin:10px 0 0}'
		. ':root body .nlps-page--world #nlps-t,:root body section.nlws{scroll-margin-top:120px}'
		. '@media(max-width:1099px){:root body .nlps-page.nlps-page--world{grid-template-columns:minmax(0,1fr);grid-template-areas:"hero" "lead" "cta" "stage" "below" "facts" "deals" "rail"}:root body .nlps-page--world .nlps-stage--world{height:68svh;min-height:440px}}'
		. '@media(max-width:600px){:root body .nlps-page--world .nlps-stage--world{height:72svh;min-height:460px}}'
		// the text sections: a reading column, tables as spec sheets with the source under each value, the timeline, the FAQ
		. $pc . '{max-width:min(880px,calc(100% - 24px))!important;margin:0 auto 36px!important;padding:0 16px!important;box-sizing:border-box}'
		. ':root body .nlws h2{margin:0 0 10px!important;font:600 clamp(22px,2.4vw,28px)/1.25 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:#1B1A17!important;text-wrap:balance}'
		. ':root body .nlws h3{margin:18px 0 6px!important;font:600 18px/1.4 Heebo,Assistant,sans-serif!important;color:#1B1A17!important}'
		. ':root body .nlws p{max-width:none!important;margin:0 0 12px!important;font-size:16px!important;line-height:1.75!important;color:#2A2823}'
		. ':root body .nlws p.nlws-k{margin:0 0 4px!important;font:700 12.5px/1.4 Heebo,Assistant,sans-serif!important;letter-spacing:.06em;color:#8A6A2E!important}'
		. ':root body .nlws p.nlws-note{font-size:13.5px!important;line-height:1.6!important;color:#6B6558!important}'
		. ':root body .nlws a{color:#6B4E1E;text-underline-offset:3px}'
		. ':root body .nlws table{width:100%!important;margin:12px 0 20px!important;background:#fff!important;border:1px solid #E2DCD0!important;border-radius:16px!important;border-collapse:separate!important;border-spacing:0!important;overflow:hidden!important;box-shadow:0 1px 2px rgba(27,26,23,.04)!important}'
		. ':root body .nlws table :is(th,td){padding:12px 16px!important;background:none!important;border:0!important;border-top:1px solid #EFE9DD!important;text-align:start!important;vertical-align:top!important;font-size:15px!important;line-height:1.6!important;color:#1B1A17!important}'
		. ':root body .nlws table tr:first-child>:is(th,td){border-top:0!important}'
		. ':root body .nlws table thead th{background:#FAF7F1!important;font-size:12.5px!important;font-weight:700!important;color:#8A6A2E!important}'
		. ':root body .nlws table thead+tbody tr:first-child>:is(th,td){border-top:1px solid #E2DCD0!important}'
		. ':root body .nlws table tbody th{width:28%!important;font-size:13.5px!important;font-weight:700!important;color:#8A6A2E!important}'
		. ':root body .nlws table td small{display:block!important;margin-top:3px!important;font-size:12.5px!important;font-weight:400!important;line-height:1.5!important;color:#6B6558!important}'
		. ':root body .nlws ol.nlws-time{list-style:none!important;margin:14px 0 20px!important;padding:0!important;border-inline-start:2px solid #E2DCD0}'
		. ':root body .nlws ol.nlws-time li{position:relative;margin:0 0 14px!important;padding:0 18px!important;font-size:15.5px;line-height:1.6;color:#2A2823}'
		. ':root body .nlws ol.nlws-time li::before{content:"";position:absolute;inset-inline-start:-7px;top:6px;width:12px;height:12px;border-radius:50%;background:#FAF7F1;border:2px solid #9C7A3C;box-sizing:border-box}'
		. ':root body .nlws ol.nlws-time li.is-now::before{background:#9C7A3C}'
		. ':root body .nlws ol.nlws-time li b{display:block;font-size:13.5px;color:#8A6A2E;font-weight:700}'
		. ':root body .nlws ul.nlws-list{margin:8px 0 16px!important;padding-inline-start:20px!important}:root body .nlws ul.nlws-list li{margin:0 0 6px!important;font-size:15.5px;line-height:1.65}'
		. ':root body .nlws a.nlws-wa{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:0 22px;border-radius:999px;background:#0F7A63;color:#fff!important;font:700 15.5px/1 Heebo,Assistant,sans-serif;text-decoration:none!important;margin:4px 0 8px}'
		. ':root body .nlws.nlws-faq h3{margin:0!important;padding-top:18px!important;border-top:1px solid #E2DCD0!important}'
		. ':root body .nlws.nlws-faq h2+h3{padding-top:6px!important;border-top:0!important}'
		. ':root body .nlws.nlws-faq h3+p{margin:6px 0 18px!important}'
		. '@media(max-width:600px){'
		. ':root body .nlws table{display:block!important;padding:2px 14px!important}:root body .nlws table :is(thead,tbody){display:block!important}'
		. ':root body .nlws table tr{display:grid!important;grid-template-columns:minmax(0,1fr)!important;gap:2px!important;margin:0!important;padding:11px 0!important;background:none!important;border:0!important;border-top:1px solid #EFE9DD!important;border-radius:0!important;box-shadow:none!important}'
		. ':root body .nlws table :is(thead,tbody) tr:first-child,:root body .nlws table thead+tbody tr:first-child{border-top:0!important}'
		. ':root body .nlws table thead+tbody tr:first-child>:is(th,td){border-top:0!important}'
		// a row of three or more cells: its first cell a heading line, the others two by two (ProjectDossier v67's phone rows)
		. ':root body .nlws table tr:has(>:nth-child(3)){grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;gap:4px 14px!important}'
		. ':root body .nlws table tr:has(>:nth-child(3))>:first-child{grid-column:1/-1!important;font-weight:700!important}'
		. ':root body .nlws table :is(th,td){display:block!important;width:auto!important;padding:0!important;border:0!important;border-bottom:0!important;font-size:14.5px!important}'
		. ':root body .nlws table thead{display:none!important}'
		. ':root body .nlws p{font-size:15.5px!important}}'
		. '</style>' . "\n";
}, 1000 );

/* The visible H1 of a project page without a stage (design system ProjectTitle, version 39; Linear HAD-332; checklist C1).
"""

# ------------------------------------------------------------------------------------------------ 8. no stage dictionary on a world page
I18N_ANCHOR = """add_action( 'wp_footer', function () {
	$ps = nadlan_ps_current();
	if ( ! $ps || 'he' === ( $ps['lang'] ?? 'he' ) ) { return; }
"""
I18N_NEW = """add_action( 'wp_footer', function () {
	$ps = nadlan_ps_current();
	if ( ! $ps || 'he' === ( $ps['lang'] ?? 'he' ) || ! empty( $ps['world'] ) ) { return; } // KikarHamedinaWorld v104: the world speaks the page's language itself
"""

HUNKS = [
    ("config", CONFIG_ANCHOR, CONFIG_NEW),
    ("current", CURRENT_ANCHOR, CURRENT_NEW),
    ("parts", PARTS_ANCHOR, PARTS_NEW),
    ("page-class", PAGE_ANCHOR, PAGE_NEW),
    ("head", HEAD_ANCHOR, HEAD_NEW),
    ("footer", FOOT_ANCHOR, FOOT_NEW),
    ("functions", FUNCS_ANCHOR, FUNCS_NEW),
    ("i18n-footer", I18N_ANCHOR, I18N_NEW),
]


def apply(text, label=""):
    """text (LF) -> text with every hunk applied; each anchor must be found exactly once"""
    for name, old, new in HUNKS:
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"FATAL hunk {name}: anchor x{n} in {label}")
        text = text.replace(old, new)
    return text


def carries(text):
    """which hunks' new text the file already holds"""
    return {name: (new in text) for name, old, new in HUNKS}


def base_text():
    out = subprocess.run(["git", "-C", REPO, "show", f"{BASE_COMMIT}:{REL}"], capture_output=True)
    if out.returncode != 0:
        raise SystemExit("FATAL git show " + BASE_COMMIT)
    return out.stdout.decode("utf-8")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    path = os.path.join(REPO, *REL.split("/"))
    cur = io.open(path, encoding="utf-8", newline="").read()
    if "--branch" in sys.argv:
        # the working file is always git HEAD + every hunk (rebuilt, so an edited hunk replaces its older text)
        head = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + REL], capture_output=True).stdout.decode("utf-8")
        if all(carries(head).values()):
            raise SystemExit("git HEAD already carries the hunks (committed): edit the file directly or rebuild from HEAD~1")
        io.open(path, "w", encoding="utf-8", newline="").write(apply(head, "git HEAD"))
        print("rebuilt", REL, "= git HEAD +", [h[0] for h in HUNKS])
    else:
        print("working file:", carries(cur))
        b = base_text()
        print(BASE_COMMIT + ":", carries(b), "| applies cleanly:", bool(apply(b, BASE_COMMIT)))
