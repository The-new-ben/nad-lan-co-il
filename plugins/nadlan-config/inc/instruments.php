<?php
/**
 * NadLan Instruments (HAD-527, Ben 14.10.2026): the engine of the tools program. A page holds [nadlan_tool id="…"]; this
 * module loads the engine (assets/instruments/core.css + core.js), the tool's own logic (assets/instruments/tools/<id>.js) and
 * its official data (assets/instruments/data/*.json, built by tools/instruments/build_index_data.py), only on pages that use a
 * tool, with the fonts of the design system "NadLan Instruments" (https://claude.ai/artifact/ATybPAavyDEkAzH7cdg1bB:
 * Karantina, IBM Plex Sans Hebrew, IBM Plex Mono). Before the script runs, the shortcode prints a plain summary with the real
 * numbers (for search engines and AI answers); the script replaces it with the live instrument. Every tool also prints its
 * related tools (the organ: tools link each other and the guides), and the page gets SoftwareApplication JSON-LD.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

require_once __DIR__ . '/soil-guard.php';  // Ben 15.10.2026: nothing about the soil tests on any project page (the guard, not a note)

if ( ! function_exists( 'nadlan_nli_tools' ) ) {

	/** The registry: id => name, description, data files, related links (path => label). */
	function nadlan_nli_tools() {
		return apply_filters( 'nadlan_nli_tools', array(
			'indexation' => array(
				'name' => 'מחשבון הצמדה למדד תשומות הבנייה', 'cat' => 'FinanceApplication',
				'desc' => 'מחשב את תוספת ההצמדה של דירה מקבלן לפי לוח התשלומים, כללי חוק המכר (תיקון 9) והמדד הרשמי של הלשכה המרכזית לסטטיסטיקה.',
				'data' => array( 'cbs-200010.json' ),
				'related' => array( '/new-projects/contractor-delay-compensation/' => 'פיצוי על איחור במסירה', '/cpi-calculator/' => 'הצמדה למדד המחירים לצרכן', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/mortgage-calculator/' => 'מחשבון משכנתא', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/apartment-prices/' => 'מחירון הדירות לפי עיר' ),
			),
			'delay' => array(
				'name' => 'מחשבון פיצוי על איחור במסירת דירה', 'cat' => 'FinanceApplication',
				'desc' => 'מחשב את הפיצוי לפי סעיף 5א לחוק המכר (דירות), חודש אחרי חודש, לפי מועד החתימה, מועד המסירה בחוזה ודמי השכירות באזור.',
				'data' => array(),
				'related' => array( '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה', '/cpi-calculator/' => 'הצמדה למדד המחירים לצרכן', '/apartment-prices/' => 'מחירון הדירות לפי עיר', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/mortgage-calculator/' => 'מחשבון משכנתא' ),
			),
			'cpi' => array(
				'name' => 'מחשבון הצמדה למדד המחירים לצרכן', 'cat' => 'FinanceApplication',
				'desc' => 'מצמיד סכום, שכר דירה או חוב למדד המחירים לצרכן של הלשכה המרכזית לסטטיסטיקה, לפי המדד הידוע או המדד בגין, עם ריבית לפי הצורך.',
				'data' => array( 'cbs-120010.json' ),
				'related' => array( '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה', '/mortgage-calculator/mortgage-interest-rates/' => 'ריבית בנק ישראל והפריים', '/mortgage-calculator/' => 'מחשבון משכנתא', '/apartment-prices/' => 'מחירון הדירות לפי עיר', '/new-projects/contractor-delay-compensation/' => 'פיצוי על איחור במסירה' ),
			),
			'warranty' => array(
				'name' => 'שעון הבדק והאחריות של חוק המכר', 'cat' => 'UtilitiesApplication',
				'desc' => 'מתאריך מסירת הדירה: לכל סוג ליקוי לפי התוספת לחוק המכר, מתי נגמרות תקופת הבדק ותקופת האחריות, וכמה ימים נשארו.',
				'data' => array(),
				'related' => array( '/home-inspection/' => 'בדק בית', '/new-projects/contractor-delay-compensation/' => 'פיצוי על איחור במסירה', '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה', '/cpi-calculator/' => 'הצמדה למדד המחירים לצרכן' ),
			),
			'soilmap' => array(
				'name' => 'מפת בדיקות הקרקע בשדה דב', 'cat' => 'ReferenceApplication', 'kicker' => 'מפה · שדה דב',
				'desc' => 'מפה תלת־ממדית של מגרשי רובע שדה דב: לכל מגרש שפורסם עליו סקר קרקע, פי כמה ריכוז ה־PFOS מעל ערך הסף, באיזה עומק, כמה קידוחים חרגו, והדו"ח עצמו. בדיקה לפי מספר מגרש או פרויקט.',
				'data' => array( 'sde-dov-soil.json' ),
				'related' => array( '/sde-dov/' => 'המדריך לשדה דב', '/sde-dov/prices/' => 'מחירי הדירות בשדה דב', '/real-estate-lawyer/construction-defects-lawsuit/' => 'שעון הבדק והאחריות', '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה' ),
			),
			'pfas' => array(
				'name' => 'מחשבון PFAS: פי כמה מעל ערך הסף', 'cat' => 'UtilitiesApplication', 'kicker' => 'מחשבון · קרקע',
				'desc' => 'ממיר ריכוז של PFOS, PFOA או PFHxS מדו"ח סקר קרקע (ננוגרם, מיקרוגרם או מיליגרם לק"ג) לפי כמה הוא מעל ערך הסף למגע ישיר שמשמש בדו"חות של שדה דב, ומשווה לשיאים שפורסמו.',
				'data' => array( 'sde-dov-soil.json' ),
				'related' => array( '/sde-dov/' => 'המדריך לשדה דב', '/sde-dov/prices/' => 'מחירי הדירות בשדה דב' ),
			),
			'soilask' => array(
				'name' => 'מכתב שאלות ליזם על הקרקע במגרש', 'cat' => 'UtilitiesApplication', 'kicker' => 'מחולל · שדה דב',
				'desc' => 'מכתב מוכן ליזם על מצב הקרקע במגרש בשדה דב: נפתח במה שפורסם על המגרש ושואל על הדיגום לפי הנחיות 12.2.2026, הדו"ח המלא, אימוץ הממצאים, תכנית הטיפול, מועד המסירה, העלות והחוזה. מכתב מלא או הודעת וואטסאפ.',
				'data' => array( 'sde-dov-soil.json' ),
				'related' => array( '/real-estate-lawyer/' => 'עורך דין לקניית דירה', '/new-projects/contractor-delay-compensation/' => 'פיצוי על איחור במסירה', '/sde-dov/' => 'המדריך לשדה דב' ),
			),
			'prime' => array(
				'name' => 'מחשבון ריבית הפריים וההחזר החודשי', 'cat' => 'FinanceApplication',
				'desc' => 'מראה את ריבית בנק ישראל והפריים היום, את ההחזר החודשי במסלול הפריים, וכמה הוא משתנה בכל שינוי של רבע אחוז בריבית.',
				'data' => array( 'boi-rate.json' ),
				'related' => array( '/mortgage-calculator/' => 'מחשבון משכנתא', '/cpi-calculator/' => 'הצמדה למדד המחירים לצרכן', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/apartment-prices/' => 'מחירון הדירות לפי עיר' ),
			),
		) );
	}

	function nadlan_nli_url( $rel ) { return plugins_url( 'assets/instruments/' . $rel, dirname( __DIR__ ) . '/nadlan-config.php' ); } // the plugin root, not inc/
	function nadlan_nli_ver() { return defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1'; }

	/** The ids of the tools in a post's content. */
	function nadlan_nli_ids_in( $content ) {
		if ( false === strpos( (string) $content, '[nadlan_tool' ) ) { return array(); }
		preg_match_all( '/\[nadlan_tool\s+id="([a-z0-9-]+)"/', $content, $m );
		return array_values( array_intersect( array_unique( $m[1] ), array_keys( nadlan_nli_tools() ) ) );
	}

	function nadlan_nli_page_ids() {
		static $ids = null;
		if ( null !== $ids ) { return $ids; }
		$ids = array();
		if ( is_singular() ) { $p = get_post(); if ( $p ) { $ids = nadlan_nli_ids_in( $p->post_content ); } }
		return $ids;
	}

	/** One official series as data for the summary. */
	function nadlan_nli_series( $file ) {
		$path = dirname( __DIR__ ) . '/assets/instruments/data/' . $file;
		if ( ! is_readable( $path ) ) { return null; }
		$d = json_decode( (string) file_get_contents( $path ), true );
		return is_array( $d ) && ! empty( $d['months'] ) ? $d : null;
	}

	add_action( 'wp_enqueue_scripts', function () {
		$ids = nadlan_nli_page_ids();
		if ( ! $ids ) { return; }
		$v = nadlan_nli_ver();
		wp_enqueue_style( 'nadlan-nli-fonts', 'https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap', array(), null );
		wp_enqueue_style( 'nadlan-nli', nadlan_nli_url( 'core.css' ), array(), $v );
		wp_enqueue_script( 'nadlan-nli', nadlan_nli_url( 'core.js' ), array(), $v, true );
		foreach ( $ids as $id ) { wp_enqueue_script( 'nadlan-nli-' . $id, nadlan_nli_url( 'tools/' . $id . '.js' ), array( 'nadlan-nli' ), $v, true ); }
	}, 20 );

	add_filter( 'script_loader_tag', function ( $tag, $handle ) {
		return 0 === strpos( $handle, 'nadlan-nli' ) && false === strpos( $tag, ' defer' ) ? str_replace( ' src=', ' defer src=', $tag ) : $tag;
	}, 10, 2 );

	/** The summary printed before the script runs: the real numbers, for readers without JS, search engines and AI. */
	function nadlan_nli_summary( $id ) {
		if ( 'indexation' === $id ) {
			$d = nadlan_nli_series( 'cbs-200010.json' );
			if ( ! $d ) { return ''; }
			$ks = array_keys( $d['months'] ); $l = end( $ks ); $p = $ks[ count( $ks ) - 2 ];
			$y = ( (int) substr( $l, 0, 4 ) - 1 ) . substr( $l, 4 );
			$m1 = $d['months'][ $l ] / $d['months'][ $p ] - 1; $m12 = isset( $d['months'][ $y ] ) ? $d['months'][ $l ] / $d['months'][ $y ] - 1 : null;
			$lm = (int) substr( $l, 5 ) . '.' . substr( $l, 0, 4 );
			return '<p>מדד מחירי תשומה בבנייה למגורים, הנתון האחרון שפרסמה הלשכה המרכזית לסטטיסטיקה: ' . esc_html( $lm ) . '. שינוי בחודש: ' . esc_html( number_format( $m1 * 100, 1 ) ) . '%'
				. ( null !== $m12 ? '. שינוי ב־12 חודשים: ' . esc_html( number_format( $m12 * 100, 1 ) ) . '%' : '' ) . '. בחוזה מ־7.7.2022: 20% מהמחיר המשולמים בחתימה אינם צמודים, ומכל תשלום אחר מותר להצמיד עד מחצית, ורק עד מועד המסירה שבחוזה.</p>';
		}
		if ( 'cpi' === $id ) {
			$d = nadlan_nli_series( 'cbs-120010.json' );
			if ( ! $d ) { return ''; }
			$ks = array_keys( $d['months'] ); $l = end( $ks ); $p = $ks[ count( $ks ) - 2 ];
			$y = ( (int) substr( $l, 0, 4 ) - 1 ) . substr( $l, 4 );
			$m1 = $d['months'][ $l ] / $d['months'][ $p ] - 1; $m12 = isset( $d['months'][ $y ] ) ? $d['months'][ $l ] / $d['months'][ $y ] - 1 : null;
			return '<p>מדד המחירים לצרכן, הנתון האחרון שפרסמה הלשכה המרכזית לסטטיסטיקה: ' . esc_html( (int) substr( $l, 5 ) . '.' . substr( $l, 0, 4 ) ) . ' (בסיס ' . esc_html( $d['base'] ) . '). שינוי בחודש: ' . esc_html( number_format( $m1 * 100, 1 ) ) . '%'
				. ( null !== $m12 ? '. שינוי ב־12 חודשים: ' . esc_html( number_format( $m12 * 100, 1 ) ) . '%' : '' ) . '. המדד מתפרסם ב־15 בכל חודש, בשעה 18:30, עבור החודש הקודם.</p>';
		}
		if ( 'prime' === $id ) {
			$path = dirname( __DIR__ ) . '/assets/instruments/data/boi-rate.json';
			$b = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $b ) || empty( $b['changes'] ) ) { return ''; }
			$c = $b['changes']; $l = end( $c );
			return '<p>ריבית בנק ישראל: ' . esc_html( number_format( (float) $b['rate'], 2 ) ) . '%. ריבית הפריים: ' . esc_html( number_format( (float) $b['prime'], 2 ) ) . '% (ריבית בנק ישראל ועוד 1.5%). בתוקף מ־'
				. esc_html( date_i18n( 'j.n.Y', strtotime( $l['from'] ) ) ) . ', לפי בנק ישראל, נכון ל־' . esc_html( date_i18n( 'j.n.Y', strtotime( $b['asof'] ) ) ) . '.</p>';
		}
		if ( 'warranty' === $id ) {
			return '<p>לפי חוק המכר (דירות): תקופת הבדק מתחילה ביום מסירת הדירה ונמשכת בין שנה ל־7 שנים לפי סוג הליקוי (צנרת ואיטום 4 שנים, סדקים מעל 1.5 מ״מ 5 שנים, חיפויי חוץ 7 שנים), ואחריה 3 שנות אחריות. ליקוי יסודי בנשיאת המבנה: 20 שנה. ליקוי שנראה כבר במסירה: מודיעים לקבלן תוך שנה.</p>';
		}
		if ( 'soilmap' === $id || 'pfas' === $id ) {
			$path = dirname( __DIR__ ) . '/assets/instruments/data/sde-dov-soil.json';
			$s = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $s ) || empty( $s['records'] ) ) { return ''; }
			$rep = array_values( array_filter( $s['records'], function ( $r ) { return 'published_report' === $r['status'] && ! empty( $r['pfosMax'] ); } ) );
			usort( $rep, function ( $a, $b ) { return $b['pfosX'] <=> $a['pfosX']; } );
			$holes = 0; $over = 0; foreach ( $rep as $r ) { $holes += (int) $r['holes']; $over += (int) $r['pfosHoles']; }
			$th = $s['thresholds'];
			$p = '<p>לפי דו"חות סקרי הקרקע שפורסמו במאגר המשרד להגנת הסביבה, נכון ל־' . esc_html( date_i18n( 'j.n.Y', strtotime( $s['built'] ) ) ) . ': ' . count( $rep ) . ' מגרשים בשדה דב עם דו"ח, ' . $over . ' מתוך ' . $holes
				. ' קידוחים עם ערך PFOS מעל ערך הסף. הערך הגבוה: מגרש ' . esc_html( $rep[0]['plot'] ) . ', פי ' . esc_html( number_format( $rep[0]['pfosX'] ) ) . ' מערך הסף למגע ישיר (PFOS ' . esc_html( number_format( $th['pfos'], 1 ) ) . ' ננוגרם לק"ג).</p>';
			if ( 'pfas' === $id ) { return $p; }
			$p .= '<table><thead><tr><th>מגרש</th><th>שיא PFOS (ננוגרם לק"ג)</th><th>פי כמה מהסף</th><th>קידוחים מעל ערך הסף</th></tr></thead><tbody>';
			foreach ( $rep as $r ) { $p .= '<tr><td>' . esc_html( $r['plot'] ) . '</td><td>' . esc_html( number_format( $r['pfosMax'] ) ) . '</td><td>' . esc_html( number_format( $r['pfosX'], $r['pfosX'] < 10 ? 1 : 0 ) ) . '</td><td>' . (int) $r['pfosHoles'] . ' מתוך ' . (int) $r['holes'] . '</td></tr>'; }
			return $p . '</tbody></table>';
		}
		if ( 'soilask' === $id ) {
			return '<p>השאלות שכדאי לשאול את היזם על הקרקע במגרש בשדה דב: האם המגרש נדגם לפי ההנחיות של המשרד להגנת הסביבה מ־12.2.2026; את דו"ח סקר הקרקע המלא; האם המשרד אימץ את הממצאים בכתב; אם נמצאה חריגה, האם תכנית הטיפול אושרה; האם הטיפול עלול לדחות את מועד המסירה; מי נושא בעלות; ואילו תנאים יש בהיתר.</p>';
		}
		if ( 'delay' === $id ) {
			return '<p>פיצוי על איחור במסירה לפי סעיף 5א לחוק המכר (דירות): בחוזה מ־7.7.2022, אחרי חודש חסד, דמי שכירות של דירה דומה בחודשים 2 עד 4, דמי שכירות כפול 1.25 בחודשים 5 עד 10, וכפול 1.5 מהחודש ה־11. בחוזה עד 6.7.2022, כשהאיחור עובר 60 ימים, דמי שכירות כפול 1.5 מהמועד שבחוזה ועד סוף החודש השמיני, ומהחודש התשיעי כפול 1.25.</p>';
		}
		return '';
	}

	add_shortcode( 'nadlan_tool', function ( $atts ) {
		$a = shortcode_atts( array( 'id' => '' ), $atts );
		$tools = nadlan_nli_tools();
		$id = sanitize_key( $a['id'] );
		if ( ! isset( $tools[ $id ] ) ) { return ''; }
		$t = $tools[ $id ];
		$data = implode( ',', array_map( function ( $f ) { return esc_url( nadlan_nli_url( 'data/' . $f ) . '?ver=' . nadlan_nli_ver() ); }, $t['data'] ) );
		$h = '<section class="nli" dir="rtl" lang="he" aria-label="' . esc_attr( $t['name'] ) . '"><div class="nli-host" data-nli="' . esc_attr( $id ) . '"' . ( $data ? ' data-nli-data="' . $data . '"' : '' ) . '>'
			. '<div class="nli__panel"><p class="nli__kicker">' . esc_html( isset( $t['kicker'] ) ? $t['kicker'] : 'מחשבון' ) . '</p><h2 class="nli__title">' . esc_html( $t['name'] ) . '</h2>' . nadlan_nli_summary( $id ) . '</div></div>';
		if ( ! empty( $t['related'] ) ) {
			$h .= '<nav class="nli__rel" aria-label="כלים קשורים"><span>כלים קשורים:</span>';
			foreach ( $t['related'] as $path => $label ) { $h .= ' <a href="' . esc_url( home_url( $path ) ) . '">' . esc_html( $label ) . '</a>'; }
			$h .= '</nav>';
		}
		return $h . '</section>';
	} );

	/** FAQPage from the page's own "שאלות נפוצות" section (h3 question, then its paragraphs), for search engines and AI answers. */
	function nadlan_nli_faq( $html ) {
		$html = preg_replace( '/<!--.*?-->/s', '', (string) $html );
		if ( ! preg_match( '/<h2[^>]*>\s*(?:שאלות נפוצות|Frequently asked questions)\s*<\/h2>(.*?)(?=<h2|$)/su', $html, $m ) ) { return array(); }
		preg_match_all( '/<h3[^>]*>(.*?)<\/h3>\s*((?:<p[^>]*>.*?<\/p>\s*)+)/su', $m[1], $qa, PREG_SET_ORDER );
		$out = array();
		foreach ( $qa as $x ) { $q = trim( wp_strip_all_tags( $x[1] ) ); $a = trim( preg_replace( '/\s+/u', ' ', wp_strip_all_tags( $x[2] ) ) ); if ( $q && $a ) { $out[] = array( '@type' => 'Question', 'name' => $q, 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $a ) ); } }
		return count( $out ) >= 2 ? $out : array();
	}

	add_action( 'wp_head', function () {
		$ids = nadlan_nli_page_ids();
		if ( ! $ids ) { return; }
		$tools = nadlan_nli_tools(); $out = array();
		foreach ( $ids as $id ) {
			$t = $tools[ $id ];
			$out[] = array( '@type' => 'SoftwareApplication', 'name' => $t['name'], 'description' => $t['desc'], 'applicationCategory' => $t['cat'], 'operatingSystem' => 'Any',
				'inLanguage' => 'he', 'url' => get_permalink(), 'isAccessibleForFree' => true, 'offers' => array( '@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'ILS' ),
				'publisher' => array( '@type' => 'Organization', 'name' => 'nad-lan.co.il', 'url' => home_url( '/' ) ) );
		}
		$p = get_post(); $faq = $p ? nadlan_nli_faq( $p->post_content ) : array();
		if ( $faq ) { $out[] = array( '@type' => 'FAQPage', 'url' => get_permalink(), 'mainEntity' => $faq ); }
		echo '<script type="application/ld+json" id="nadlan-nli-ld">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => $out ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	}, 30 );
}
