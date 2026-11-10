<?php
/**
 * nadlan-config · the /projects/ hub (1.72.513, Ben 25.10.2026: "this page is very, very important ... everything the
 * competitors have will be here, organised, with tools ... the title does not change").
 *
 * The catalog (inc/directory.php) prints the H1, the lead and the grid; snippet 661 (x-catalog-plus) injects its body copy and
 * its ItemList + FAQPage schema through nadlan_cp_body_html() and nadlan_cp_faq(), both declared there only "if ! function_exists".
 * This file is loaded with the plugin, before the snippets run, so these two functions are the ones the snippet calls: the
 * body after the grid and the one FAQ (markup and schema) come from here. Turning this file off gives the snippet's own copy back.
 *
 * Research behind every section: docs/research/2026-10-25-projects-hub/ (serp.md, competitors/dna.md, facts.md, our-page.md,
 * market.json). Numbers carry their date; developer prices are shown as the developer published them, with the date read.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NADLAN_PH_UPDATED' ) ) { define( 'NADLAN_PH_UPDATED', '2026-10-25' ); } // the language hubs (en, ru, fr) print this date: it changes only when THEY change
/* the Hebrew hub's own date (HAD-689): the immediate-occupancy section and the Tel Aviv-first order went live on 10.11.2026 */
if ( ! defined( 'NADLAN_PH_UPDATED_HE' ) ) { define( 'NADLAN_PH_UPDATED_HE', '2026-11-10' ); }
/* HAD-689 step 2: the top block shipped behind ?nlready=1 (1.72.628), was pressed live on a phone and a desktop on 10.11.2026, and is on for everyone from 1.72.629. */
if ( ! defined( 'NADLAN_PH_READY_LIVE' ) ) { define( 'NADLAN_PH_READY_LIVE', true ); }

if ( ! function_exists( 'nadlan_ph_json' ) ) {
	/** A JSON file of the plugin as an array (empty on any problem). */
	function nadlan_ph_json( $rel ) {
		static $c = array();
		if ( isset( $c[ $rel ] ) ) { return $c[ $rel ]; }
		$p = dirname( __DIR__ ) . '/' . $rel;
		$d = is_readable( $p ) ? json_decode( (string) file_get_contents( $p ), true ) : null;
		return $c[ $rel ] = is_array( $d ) ? $d : array();
	}
}

if ( ! function_exists( 'nadlan_ph_market' ) ) {
	/** Projects in marketing, as their developers publish them (data/projects-market.json, built from market.json). */
	function nadlan_ph_market() {
		$d = nadlan_ph_json( 'data/projects-market.json' );
		return isset( $d['projects'] ) && is_array( $d['projects'] ) ? $d : array( 'projects' => array(), 'read' => '' );
	}
}

if ( ! function_exists( 'nadlan_ph_value' ) ) {
	/** City medians by rooms, Tax Authority closed deals (assets/instruments/data/value.json). */
	function nadlan_ph_value() {
		$d = nadlan_ph_json( 'assets/instruments/data/value.json' );
		return isset( $d['cities'] ) && is_array( $d['cities'] ) ? $d['cities'] : array();
	}
}

if ( ! function_exists( 'nadlan_ph_nis' ) ) {
	function nadlan_ph_nis( $n ) { return number_format( (float) $n ) . ' ₪'; }
}
if ( ! function_exists( 'nadlan_ph_mil' ) ) {
	/** 5,229,800 -> "5.23 מיליון ₪" */
	function nadlan_ph_mil( $n ) {
		$n = (float) $n;
		return $n >= 1000000 ? rtrim( rtrim( number_format( $n / 1000000, 2 ), '0' ), '.' ) . ' מיליון ₪' : nadlan_ph_nis( $n );
	}
}

if ( ! function_exists( 'nadlan_ph_yoy' ) ) {
	/** 10.7 -> "עלייה של 10.7% בשנה", -1.8 -> "ירידה של 1.8% בשנה" */
	function nadlan_ph_yoy( $x ) {
		$x = (float) $x;
		return ( $x < 0 ? 'ירידה של ' : 'עלייה של ' ) . rtrim( rtrim( number_format( abs( $x ), 1 ), '0' ), '.' ) . '% בשנה';
	}
}

if ( ! function_exists( 'nadlan_ph_region' ) ) {
	/** The market region of a city, for the table filter. */
	function nadlan_ph_region( $city ) {
		$c = str_replace( array( '-', '–' ), ' ', trim( (string) $city ) );
		$map = array(
			'tlv'    => array( 'תל אביב', 'יפו' ),
			'dan'    => array( 'רמת גן', 'גבעתיים', 'גבעתים', 'בת ים', 'חולון', 'בני ברק', 'קרית אונו', 'קריית אונו', 'פתח תקווה', 'פתח תקוה', 'אור יהודה', 'יהוד', 'גני תקווה', 'אזור', 'סביון' ),
			'center' => array( 'ראשון לציון', 'רחובות', 'נס ציונה', 'לוד', 'רמלה', 'יבנה', 'מודיעין', 'שוהם', 'באר יעקב', 'ראש העין', 'גדרה', 'מזכרת בתיה' ),
			'sharon' => array( 'הרצליה', 'רעננה', 'כפר סבא', 'הוד השרון', 'רמת השרון', 'נתניה', 'כפר יונה', 'אבן יהודה', 'צור יגאל', 'כוכב יאיר' ),
			'south'  => array( 'אשדוד', 'אשקלון', 'באר שבע', 'אופקים', 'קרית גת', 'קריית גת', 'נתיבות', 'שדרות', 'דימונה', 'ערד', 'אילת', 'קרית מלאכי', 'קריית מלאכי', 'גן יבנה' ),
			'north'  => array( 'חיפה', 'קרית', 'קריית', 'טירת כרמל', 'נהריה', 'עכו', 'עפולה', 'חדרה', 'כרמיאל', 'נשר', 'יקנעם', 'זכרון יעקב', 'פרדס חנה', 'אור עקיבא', 'נוף הגליל', 'טבריה', 'צפת' ),
			'jlm'    => array( 'ירושלים', 'בית שמש', 'מבשרת', 'מעלה אדומים', 'גבעת זאב' ),
		);
		foreach ( $map as $k => $names ) { foreach ( $names as $n ) { if ( false !== mb_strpos( $c, $n ) ) { return $k; } } }
		return 'other';
	}
}
if ( ! function_exists( 'nadlan_ph_regions' ) ) {
	function nadlan_ph_regions() {
		return array( 'tlv' => 'תל אביב', 'dan' => 'גוש דן', 'center' => 'מרכז ושפלה', 'sharon' => 'השרון', 'south' => 'דרום', 'north' => 'חיפה והצפון', 'jlm' => 'ירושלים והסביבה', 'other' => 'ערים נוספות' );
	}
}
if ( ! function_exists( 'nadlan_ph_tlv_area' ) ) {
	/** A Tel Aviv neighbourhood -> one of five areas of the city. */
	function nadlan_ph_tlv_area( $hood ) {
		$h = (string) $hood;
		$map = array(
			'jaffa' => array( 'צפון יפו', 'עג׳מי', 'יפו ד', 'צהלון', 'גבעת התמרים', 'יפו העתיקה', 'נמל יפו' ),
			'north' => array( 'שדה דב', 'רמת אביב', 'אפקה', 'הדר יוסף', 'צפון', 'כיכר המדינה', 'בבלי', 'צהלה', 'פארק צמרת', 'נווה אביבים', 'נוה אביבים', 'תכנית ל', 'אוניברסיטה', 'רמת החייל', 'נווה שרת', 'נוה שרת', 'גני צהלה', 'כוכב הצפון', 'יפו - תל אביב צפון' ),
			'centre' => array( 'לב העיר', 'רוטשילד', 'כרם התימנים', 'שרונה', 'מונטיפיורי', 'קריית הממשלה', 'קרית הממשלה', 'מרכז העיר', 'הקריה', 'סומייל', 'נווה צדק', 'נוה צדק', 'כרמל', 'אבן גבירול', 'דיזנגוף' ),
			'east'  => array( 'יד אליהו', 'נחלת יצחק', 'ביצרון', 'רמת ישראל', 'הסוללים', 'תל חיים', 'ניר אביב', 'עמינדב', 'רמת הטייסים', 'נווה חן', 'נוה חן', 'דקר', 'נווה כפיר', 'כפיר' ),
			'south' => array( 'פלורנטין', 'שפירא', 'נווה שאנן', 'נוה שאנן', 'התקווה', 'קרית שלום', 'קריית שלום', 'נווה עופר', 'נוה עופר', 'תל כביר', 'גבעת הרצל', 'מכללת יפו', 'דרום' ),
		);
		foreach ( $map as $k => $names ) { foreach ( $names as $n ) { if ( false !== mb_strpos( $h, $n ) ) { return $k; } } }
		return false !== mb_strpos( $h, 'יפו' ) ? 'jaffa' : '';
	}
}

if ( ! function_exists( 'nadlan_ph_stage_counts' ) ) {
	/** The catalog by planning stage (the same posts the catalog counts: no language siblings, no private journeys). */
	function nadlan_ph_stage_counts() {
		$k = 'nadlan_ph_stages_v1';
		$c = get_transient( $k );
		if ( is_array( $c ) ) { return $c; }
		global $wpdb;
		$rows = $wpdb->get_results( "SELECT TRIM(pm.meta_value) v, COUNT(*) n FROM {$wpdb->postmeta} pm INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id WHERE pm.meta_key='project_status' AND p.post_type='nadlan_project' AND p.post_status='publish' AND p.post_name NOT REGEXP '-(en|fr|ru|ar)$' AND NOT EXISTS (SELECT 1 FROM {$wpdb->postmeta} x WHERE x.post_id=p.ID AND x.meta_key='_nadlan_private_unit_journey' AND x.meta_value='private-unit-journey-v2') GROUP BY TRIM(pm.meta_value)", ARRAY_A );
		$out = array( 'plan' => 0, 'approved' => 0, 'build' => 0, 'market' => 0 );
		foreach ( (array) $rows as $r ) {
			$v = (string) $r['v']; $n = (int) $r['n'];
			if ( '' === $v ) { continue; }
			if ( false !== mb_strpos( $v, 'בשיווק' ) ) { $out['market'] += $n; }
			elseif ( false !== mb_strpos( $v, 'במימוש' ) || false !== mb_strpos( $v, 'בבנייה' ) || false !== mb_strpos( $v, 'בהקמה' ) || 'construction' === $v ) { $out['build'] += $n; }
			elseif ( false !== mb_strpos( $v, 'מאושרת' ) || false !== mb_strpos( $v, 'היתר' ) || 'permits' === $v ) { $out['approved'] += $n; }
			elseif ( false !== mb_strpos( $v, 'תכנון' ) || false !== mb_strpos( $v, 'בתכנון' ) || 'planning' === $v ) { $out['plan'] += $n; }
		}
		$cities = $wpdb->get_col( "SELECT DISTINCT TRIM(pm.meta_value) FROM {$wpdb->postmeta} pm INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id WHERE pm.meta_key='city' AND pm.meta_value<>'' AND p.post_type='nadlan_project' AND p.post_status='publish' AND p.post_name NOT REGEXP '-(en|fr|ru|ar)$'" );
		$norm = array(); foreach ( (array) $cities as $c ) { $norm[ preg_replace( '/\s+/u', ' ', str_replace( array( '-', '–' ), ' ', (string) $c ) ) ] = 1; }
		$out['cities'] = count( $norm );
		set_transient( $k, $out, 6 * HOUR_IN_SECONDS );
		return $out;
	}
}
add_action( 'save_post_nadlan_project', function () { delete_transient( 'nadlan_ph_stages_v1' ); } );

/* ------------------------------------------------------------------------------------------------ the FAQ (markup + schema) */
if ( ! function_exists( 'nadlan_ph_faq_facts' ) ) {
	/** Counts for the short questions on Google's related searches, printed from the data file (never typed by hand). */
	function nadlan_ph_faq_facts() {
		static $f = null;
		if ( null !== $f ) { return $f; }
		$f = array( 'all' => 0, 'priced' => 0, 'u12' => 0, 'u15' => 0, 'u15south' => 0, 'deal' => 0, 'd2080' => 0, 'presale' => 0, 'presale_tlv' => 0, 'marketing' => 0, 'construction' => 0,
			'tlv' => 0, 'dan' => 0, 'sharon' => 0, 'center' => 0, 'ramat_aviv' => 0, 'cities' => 0 );
		$cities = array();
		foreach ( nadlan_ph_market()['projects'] as $p ) {
			$f['all']++;
			$city = (string) ( $p['city'] ?? '' ); $reg = nadlan_ph_region( $city ); $st = (string) ( $p['status'] ?? '' );
			if ( '' !== $city ) { $cities[ str_replace( array( '-', '–' ), ' ', $city ) ] = 1; }
			if ( isset( $f[ $reg ] ) && in_array( $reg, array( 'tlv', 'dan', 'sharon', 'center' ), true ) ) { $f[ $reg ]++; }
			if ( isset( $f[ $st ] ) && in_array( $st, array( 'presale', 'marketing', 'construction' ), true ) ) { $f[ $st ]++; }
			if ( 'presale' === $st && 'tlv' === $reg ) { $f['presale_tlv']++; }
			$pr = (float) ( $p['price_from'] ?? 0 );
			if ( $pr > 0 ) {
				$f['priced']++;
				if ( $pr <= 1200000 ) { $f['u12']++; }
				if ( $pr <= 1500000 ) { $f['u15']++; if ( 'south' === $reg ) { $f['u15south']++; } }
			}
			$deal = (string) ( $p['deal'] ?? '' );
			if ( '' !== $deal ) { $f['deal']++; if ( preg_match( '~(?:80|90|85)\s*[/\-]\s*(?:20|10|15)|(?:20|10|15)\s*[/\-]\s*(?:80|90|85)~u', $deal ) ) { $f['d2080']++; } }
			if ( false !== mb_strpos( (string) ( $p['name'] ?? '' ) . ' ' . (string) ( $p['neighbourhood'] ?? '' ), 'רמת אביב' ) ) { $f['ramat_aviv']++; }
		}
		$f['cities'] = count( $cities );
		return $f;
	}
}
if ( ! function_exists( 'nadlan_ph_faq_related' ) ) {
	/** HAD-697 (Ben, 10.11.2026): every search Google shows beside "פרויקטים חדשים" gets a short answer on the page, in passing:
	 * a question in Google's own wording, one or two lines, a link where a page of ours owns the topic. Not an article, not the
	 * focus. The questions that were already here (עד 1.2 מיליון, עד 2 מיליון, פריסייל בתל אביב, הטבות יזמים) stay as they are. */
	function nadlan_ph_faq_related() {
		$f = nadlan_ph_faq_facts();
		if ( $f['all'] < 1 ) { return array(); }
		$n = function ( $k ) use ( $f ) { return number_format( (int) $f[ $k ] ); };
		$q = array();
		if ( $f['u15'] > 0 ) {
			$q[] = array( 'יש דירות חדשות עד 1.5 מיליון שקל?', 'כן. בטבלת הפרויקטים בשיווק יש ' . $n( 'u15' ) . ' פרויקטים עם מחיר שמתחיל עד 1.5 מיליון ₪'
				. ( $f['u12'] > 0 ? ', ' . ( 1 === $f['u12'] ? 'אחד מהם' : $n( 'u12' ) . ' מהם' ) . ' עד 1.2 מיליון ₪' : '' )
				. ( $f['u15south'] * 2 > $f['u15'] ? '. רובם בערי הדרום' : '' ) . '. בסינון המחיר של הטבלה בוחרים "עד 1.5 מיליון ₪" או "עד 1.2 מיליון ₪" ורואים רק אותם.' );
		}
		if ( $f['deal'] > 0 ) {
			$q[] = array( 'איפה רואים מבצעי קבלנים על דירות חדשות?', $n( 'deal' ) . ' פרויקטים בטבלת הפרויקטים בשיווק מפרסמים מבצע או תנאי תשלום מיוחדים'
				. ( $f['d2080'] > 0 ? ', ' . $n( 'd2080' ) . ' מהם בתנאי 20/80, 10/90 או דומים' : '' ) . '. התנאים מופיעים בעמודה "תנאי תשלום", בלשון היזם. המדריך למבצעי קבלנים מסביר כמה כל מבצע שווה בכסף.', '/developer-deals/', 'מבצעי קבלנים 2026: 20/80, 10/90 והלוואת קבלן' );
		}
		$q[] = array( 'מה זה פרויקט 20/80?', 'בפרויקט 20/80 משלמים 20% ממחיר הדירה בחתימה על החוזה ואת 80% הנותרים סמוך למסירה. יש גם מבצעי 10/90 ו־15/85. לפני שחותמים בודקים אם היתרה מוצמדת למדד תשומות הבנייה, ואם יהיה אפשר לקבל משכנתא במועד המסירה.', '/developer-deals/', '20/80, 10/90 ו־15/85: רמות הסיכון' );
		$q[] = array( 'מה זה הלוואת קבלן?', 'הלוואת קבלן היא הלוואה שהרוכש לוקח מהבנק שמלווה את הפרויקט כדי לדחות את רוב התשלום למסירה, והיזם משלם את הריבית עליה בתקופת הבנייה. החוב עצמו נשאר של הרוכש, ובדרך כלל הוא נפרע במשכנתא במועד האכלוס.', '/developer-deals/', 'הלוואת קבלן: היזם משלם את הריבית, החוב נשאר שלכם' );
		$q[] = array( 'אילו פרויקטים חדשים בשיווק יש עכשיו?', $n( 'marketing' ) . ' פרויקטים חדשים בשיווק, ' . $n( 'construction' ) . ' פרויקטים בבנייה ו־' . $n( 'presale' ) . ' בפריסייל, מתוך ' . $n( 'all' ) . ' הפרויקטים החדשים שבעמוד הזה. בטבלת הפרויקטים בשיווק מסננים לפי שלב, אזור ומחיר.' );
		$q[] = array( 'מה ההבדל בין פרויקט בשיווק לפרויקט בבנייה?', 'פרויקט בשיווק כבר מוכר דירות, לפעמים עוד לפני שהבנייה התחילה. בפרויקט בבנייה העבודות בשטח כבר מתקדמות, ולכן המפתח קרוב יותר. בטבלה בעמוד הזה בוחרים בשלב "בבנייה", ומועד המסירה מופיע כשהיזם פרסם אותו.' );
		$q[] = array( 'אילו פרויקטים חדשים על הנייר יש?', 'דירה על הנייר היא דירה שנמכרת לפני שהבנייה הסתיימה. בעמוד הזה ' . $n( 'presale' ) . ' פרויקטים בפריסייל'
			. ( $f['presale_tlv'] > 0 ? ', ' . $n( 'presale_tlv' ) . ' מהם בתל אביב יפו' : '' ) . ', ועוד ' . $n( 'construction' ) . ' פרויקטים בבנייה. בטבלת הפרויקטים בשיווק מסננים לפי שלב.', '/new-projects/presale-apartment/', 'דירת פריסייל: מחיר אמיתי ובדיקות לפני חתימה' );
		$centre = $f['tlv'] + $f['dan'] + $f['sharon'] + $f['center'];
		if ( $centre > 0 ) {
			$q[] = array( 'יש פרויקטים חדשים במרכז?', 'כן. ' . number_format( $centre ) . ' מהפרויקטים החדשים שבעמוד נמצאים במרכז הארץ: ' . $n( 'tlv' ) . ' בתל אביב יפו, ' . $n( 'dan' ) . ' בגוש דן, ' . $n( 'sharon' ) . ' בשרון ו־' . $n( 'center' ) . ' בערי המרכז והשפלה. בטבלה בוחרים אזור ורואים רק אותם.' );
		}
		if ( $f['ramat_aviv'] > 0 ) {
			$q[] = array( 'אילו פרויקטים חדשים יש ברמת אביב?', 'בעמוד הזה ' . $n( 'ramat_aviv' ) . ' פרויקטים חדשים ברמת אביב. בטבלת הפרויקטים בשיווק בוחרים "תל אביב" ורואים אותם עם המחיר שהיזם פרסם, החדרים והשלב.', '/new-projects/north-tel-aviv-new-projects/', 'פרויקטים חדשים בצפון תל אביב' );
		}
		$q[] = array( 'יש בית פרטי חדש מקבלן?', 'רוב הפרויקטים החדשים שבעמוד הם דירות בבנייני מגורים. פרויקטים של בתים פרטיים וצמודי קרקע מקבלן מופיעים בטבלה כשהיזם מפרסם אותם. גם בבית פרטי חדש מקבלן חלים חוק המכר, הערבות על הכסף ותקופות הבדק והאחריות.' );
		$q[] = array( 'איפה יש דירות חדשות למכירה?', 'בעמוד הזה ' . $n( 'all' ) . ' פרויקטים חדשים עם דירות חדשות למכירה ישירות מהיזם, ב־' . $n( 'cities' ) . ' ערים ויישובים. ' . $n( 'priced' ) . ' מהם מפרסמים מחיר התחלתי, והוא מופיע בטבלה לצד מחירי העסקאות בעיר.' );
		return $q;
	}
}
if ( ! function_exists( 'nadlan_ph_faq' ) ) {
	/** [question, answer (plain text, also the schema answer), optional link path, optional link label] */
	function nadlan_ph_faq() {
		return array_merge( nadlan_ph_faq_core(), function_exists( 'nadlan_ph_faq_related' ) ? nadlan_ph_faq_related() : array() );
	}
}
if ( ! function_exists( 'nadlan_ph_faq_core' ) ) {
	function nadlan_ph_faq_core() {
		return array(
			array( 'מה נחשב פרויקט חדש מקבלן?', 'פרויקט מגורים שבו הדירות נמכרות לראשונה על ידי יזם או חברה קבלנית: בנייה חדשה על מגרש פנוי, או דירות חדשות בפרויקט התחדשות עירונית כמו פינוי בינוי ותמ"א 38. בקטלוג של נדל"ן מופיעים שני הסוגים, עם סוג הפרויקט, העיר, מספר יחידות הדיור והשלב התכנוני של כל אחד.' ),
			array( 'איפה אפשר למצוא פרויקטים חדשים בתל אביב?', 'בעמוד הזה: בקטלוג הפרויקטים מסננים לפי "תל אביב יפו", ובטבלת הפרויקטים בשיווק בוחרים "תל אביב" ורואים את המחיר שהיזם פרסם, החדרים ושלב השיווק. מרבית הבנייה החדשה בעיר מתרכזת ברובע שדה דב ובצפון העיר, בפרויקטי התחדשות עירונית במרכז ובמזרח, ובמתחמים חדשים בדרום וביפו.', '/sde-dov/', 'רובע שדה דב: פרויקטים ומחירים' ),
			array( 'האם יש פריסייל בתל אביב?', 'כן. יזמים מציעים מדי פעם דירות בשלב הפריסייל, לפני קבלת היתר הבנייה או בתחילת השיווק, במחיר נמוך ממחיר השיווק המלא. בטבלת הפרויקטים בשיווק מסננים לפי "פריסייל". בפריסייל משלמים על דירה רחוקה יותר מהמפתח, ולכן חשוב לבדוק את שלב ההיתר, את לוח הזמנים ואת הבטוחה על כל תשלום.', '/new-projects/presale-apartment/', 'דירת פריסייל: מחיר אמיתי ובדיקות לפני חתימה' ),
			array( 'אילו פרויקטים חדשים יש עד 2 מיליון שקל?', 'בשוק החופשי דירות חדשות עד 2 מיליון ₪ נמצאות בעיקר בערי הדרום, בחלק מערי השפלה ובפריפריה. בטבלת הפרויקטים בשיווק ממיינים לפי מחיר מהנמוך לגבוה. מי שזכאי לדירה בהנחה יכול לקנות דירה חדשה בהנחה ממחיר השוק, ובנק רשאי להעריך דירה כזאת לפי השמאי עד 2.1 מיליון ₪.' , '/dira-behanacha/', 'דירה בהנחה: הסיכוי לזכות בכל עיר' ),
			array( 'איפה אפשר למצוא דירות חדשות עד 1.2 מיליון שקל?', 'במחיר הזה כמעט אין דירות חדשות בשוק החופשי במרכז הארץ. הדרך המעשית היא תוכניות הדיור הממשלתיות, כמו דירה בהנחה, ופרויקטים בערי הפריפריה. בגרלת דירה בהנחה מספר 11 הוצעו 7,922 דירות ב־19 יישובים.', '/dira-behanacha/', 'דירה בהנחה: נתוני ההגרלות' ),
			array( 'איפה אפשר למצוא דירות מוכנות למכירה, באכלוס מיידי?', 'בטבלת הפרויקטים בשיווק מסננים לפי "אכלוס קרוב או מיידי". דירה גמורה מקבלן נבדקת בעיניים לפני החתימה, והתשלום מהיר יותר מאשר בדירה על הנייר. גם בה חלים חוק המכר, תקופות הבדק והאחריות והחובה לרשום את הבית המשותף.' ),
			array( 'מהי תוכנית הרובעים של תל אביב?', 'תוכניות הרובעים הן תוכניות מתאר מקומיות של עיריית תל אביב יפו שמעודדות התחדשות עירונית במרכז העיר ומחליפות את תוכנית ג׳ לבנייה על הגגות. תוכנית רובע 3 (תא/3616א) ותוכנית רובע 4 (תא/3729א) אושרו ב־2018, והן מגדירות כמה קומות אפשר להוסיף ואיך מחזקים או בונים מחדש בניין ישן.' ),
			array( 'האם יש בנייה חדשה בהרצליה?', 'כן. בהרצליה נבנים פרויקטים חדשים במרינה ובגליל ים, בהרצליה הירוקה ובפרויקטי התחדשות עירונית בעיר. בקטלוג מסננים לפי הרצליה, ולמדריך האזורי של העיר יש עמוד משלו.', '/herzliya-projects/', 'פרויקטים חדשים בהרצליה' ),
			array( 'כמה זמן לוקח מהחתימה ועד שמקבלים מפתח?', 'זה תלוי בשלב שבו חותמים. בניין מגורים נבנה בממוצע 31.8 חודשים מתחילת הבנייה (37.3 חודשים בשקלול לפי מספר הדירות), לפי הלשכה המרכזית לסטטיסטיקה. מי שחותם לפני ההיתר מוסיף את זמן הרישוי. 61% מהדירות שיזמים מכרו בשוק החופשי באוגוסט 2026 נמכרו "על הנייר", כלומר עם מסירה בעוד 24 חודשים לפחות.' ),
			array( 'האם כדאי לקנות דירה על הנייר?', 'דירה על הנייר נמכרת בדרך כלל במחיר נמוך ממחיר דירה גמורה, והתשלומים נפרסים לאורך הבנייה. מנגד, המפתח רחוק יותר וההצמדה למדד תשומות הבנייה מוסיפה לסכום. ההחלטה תלויה בזמן שאפשר לחכות, בהון העצמי ובבטוחה שהיזם נותן על כל תשלום.' ),
			array( 'מה בודקים לפני שחותמים על דירה מקבלן?', 'שהקבלן רשום בפנקס הקבלנים ובסיווג המתאים, שיש היתר בנייה, שכל תשלום מעל 7% מהמחיר מוגן בערבות חוק מכר או בטוחה אחרת ומשולם בשובר, שהמפרט הטכני חתום על הטופס הרשמי, ומה כתוב בחוזה על ההצמדה, מועד המסירה והפיצוי על איחור. רשימת תשע הבדיקות בעמוד הזה מקשרת לכל מקור רשמי.' ),
			array( 'איך בודקים את היזם ואת הקבלן?', 'מחפשים את הקבלן בפנקס הקבלנים של רשם הקבלנים, בודקים שהסטטוס פעיל ולא מוקפא או מותלה, ושהסיווג מתאים להיקף הבנייה. מעבר לפנקס כדאי לבדוק פרויקטים שהיזם כבר מסר ולשאול אם לפרויקט יש ליווי פיננסי של בנק או חברת ביטוח.', '/pinkas-hakablanim/', 'בדיקת קבלן רשום בפנקס הקבלנים' ),
			array( 'מה ההבדל בין בניין בוטיק לפרויקט גדול?', 'בניין בוטיק הוא בניין קטן, לרוב פחות מכמה עשרות דירות, עם פרטיות גבוהה ודמי ניהול נמוכים יותר. פרויקט גדול או מגדל מגורים מציע לובי, חדר כושר, בריכה ומתקנים לרווחת הדיירים, לצד דמי ניהול גבוהים יותר. בשני המקרים בודקים את אותם דברים: קבלן רשום, היתר, ערבות ומפרט.' ),
			array( 'האם דירה חדשה בתל אביב מתאימה להשקעה?', 'זו החלטה אישית שתלויה בתקציב, במימון ובטווח הזמן. כמה עובדות שכדאי להכיר: על דירה נוספת משלמים מס רכישה של 8% עד 6,055,070 ₪ ו־10% מעליו (הוראת שעה, הוארכה לרכישות עד 10.2.2027), בנק מממן למשקיע עד 50% ממחיר הדירה, ובסוף אוגוסט 2026 עמדו בתל אביב יפו כ־9,820 דירות חדשות לא מכורות.' ),
			array( 'אילו הטבות יזמים מציעים לרוכשים?', 'ההטבות הנפוצות הן תשלום של 10% או 20% בחתימה והיתרה במסירה (מבצעי 10/90 ו־20/80), הלוואת קבלן שבה היזם משלם את הריבית, מחיר השקה, ושדרוגי מפרט. בנק ישראל הגביל מאפריל 2025 את המימון המסובסד ואת הפרויקטים שבהם רוב הרוכשים דוחים יותר מ־40% מהמחיר למסירה, עד 31.12.2026.', '/developer-deals/', 'מבצעי קבלנים: מה באמת שווה כסף' ),
			array( 'מה ההבדל בין בנייה חדשה, פינוי בינוי ותמ"א 38?', 'בנייה חדשה היא פרויקט על מגרש פנוי, בדרך כלל בשכונה חדשה. פינוי בינוי הורס כמה בניינים ישנים ובונה במקומם מתחם חדש וגדול יותר. תמ"א 38 עוסקת בבניין בודד: חיזוק ותוספת קומות, או הריסה ובנייה מחדש. בשלושתם הרוכש מהיזם מקבל דירה חדשה עם הגנות חוק המכר.', '/urban-renewal/', 'התחדשות עירונית: המדריך המלא' ),
			array( 'מה ההבדל בין דירה חדשה מקבלן לדירה יד שנייה?', 'בדירה חדשה מקבלן מקבלים מפרט חדש, ערבות חוק מכר על הכסף, תקופות בדק ואחריות של שנה עד שבע שנים לפי סוג הליקוי, ולוח תשלומים שנפרס לאורך הבנייה. בדירה יד שנייה רואים בדיוק מה קונים, נכנסים מהר יותר ומנהלים משא ומתן מול בעל הדירה.' ),
			array( 'איך עובדת ההצמדה למדד תשומות הבנייה?', 'בחוזים שנחתמו מ־7.7.2022 מותר להצמיד למדד תשומות הבנייה עד מחצית מכל תשלום, ה־20% הראשונים של המחיר לא מוצמדים כלל, וההצמדה נעצרת במועד המסירה שבחוזה. לכן החלק המוצמד הוא לכל היותר 40% מהמחיר. מדד תשומות הבנייה למגורים לספטמבר 2026 עמד על 104.0, עלייה של 3.6% ב־12 חודשים.', '/new-projects/construction-input-index/', 'מחשבון הצמדה למדד תשומות הבנייה' ),
			array( 'מה הפיצוי אם היזם מאחר במסירת הדירה?', 'בחוזים מ־7.7.2022, אחרי חודש ראשון של איחור, הרוכש מקבל בלי להוכיח נזק: פי 1 משכר דירה דומה בחודשים 2 עד 4, פי 1.25 בחודשים 5 עד 10, ופי 1.5 מהחודש ה־11. לדוגמה, איחור של 12 חודשים בדירה ששכר הדירה שלה 10,000 ₪ מזכה ב־135,000 ₪.', '/new-projects/contractor-delay-compensation/', 'מחשבון פיצוי על איחור במסירה' ),
			array( 'כמה מס רכישה משלמים על דירה חדשה?', 'על דירה יחידה: 0% עד 1,978,745 ₪, 3.5% עד 2,347,040 ₪, 5% עד 6,055,070 ₪, 8% עד 20,183,565 ₪ ו־10% מעל. לדוגמה, דירה יחידה ב־3,000,000 ₪ חייבת במס של 45,538 ₪. בדירה מקבלן המס מחושב על המחיר כולל מע"מ.', '/purchase-tax-calculator/', 'מחשבון מס רכישה' ),
			array( 'מה זו ערבות חוק מכר ולמה משלמים בשוברים?', 'יזם לא רשאי לקבל יותר מ־7% מהמחיר בלי לתת בטוחה, ובדרך כלל זו ערבות בנקאית לפי חוק המכר. בפרויקט עם ליווי פיננסי משלמים רק דרך פנקס השוברים של הבנק המלווה, וכל תשלום מחייב הוצאת ערבות תוך 14 ימי עסקים. הערבות לא כוללת את רכיב המע"מ, שמוחזר לרוכש מקרן של משרד האוצר אם הערבות ממומשת.' ),
			array( 'כמה מימון בנק אפשר לקבל על דירה חדשה?', 'לפי הוראות בנק ישראל: עד 75% ממחיר הדירה לדירה יחידה, עד 70% לדירה חליפית ועד 50% לדירה להשקעה. ההחזר החודשי מוגבל ל־50% מההכנסה, החלק בריבית משתנה עד שני שלישים מההלוואה, ותקופת ההלוואה עד 30 שנה. ריבית בנק ישראל עומדת על 3.25% והפריים על 4.75%.', '/mortgage-calculator/', 'מחשבון משכנתא' ),
			array( 'איפה רואים מחירים של פרויקטים חדשים?', 'בטבלת הפרויקטים בשיווק בעמוד הזה מופיע המחיר שהיזם פרסם ("החל מ"), עם תאריך הבדיקה. לצידו מופיעים מחירי העסקאות בכל עיר לפי רשות המסים, כדי להשוות את מחיר השיווק למה ששולם בפועל. המחיר הסופי נקבע מול היזם ובחוזה.', '/apartment-prices/', 'מחירון הדירות של ישראל' ),
			array( 'כמה דירות חדשות לא נמכרו בישראל?', 'לפי הלשכה המרכזית לסטטיסטיקה, בסוף אוגוסט 2026 עמדו למכירה כ־85,680 דירות חדשות שטרם נמכרו, היצע של 26.7 חודשים. כ־26,330 מהן במחוז תל אביב וכ־9,820 בעיר תל אביב יפו. ביוני עד אוגוסט 2026 נמכרו כ־10,110 דירות חדשות, עלייה של 24.9% לעומת השנה הקודמת.' ),
		);
	}
}
if ( ! function_exists( 'nadlan_cp_faq' ) ) {
	/** Snippet 661 reads this for the FAQ markup and its FAQPage schema (one FAQPage on the page). */
	function nadlan_cp_faq() { return nadlan_ph_faq(); }
}

/* ------------------------------------------------------------------------------------------------ sections */
if ( ! function_exists( 'nadlan_ph_market_html' ) ) {
	function nadlan_ph_market_html() {
		$m = nadlan_ph_market(); $rows = $m['projects'];
		if ( ! $rows ) { return ''; }
		$regions = nadlan_ph_regions(); $used = array(); $tlv = 0;
		usort( $rows, function ( $a, $b ) {
			$pa = (int) ( $a['price_from'] ?? 0 ); $pb = (int) ( $b['price_from'] ?? 0 );
			if ( ! $pa !== ! $pb ) { return $pa ? -1 : 1; } // priced first
			return $pa - $pb;
		} );
		$st = array( 'presale' => 'פריסייל', 'marketing' => 'בשיווק', 'construction' => 'בבנייה', 'near_occupancy' => 'אכלוס קרוב', 'immediate' => 'אכלוס מיידי' );
		$count = array();
		foreach ( $rows as $p ) { $reg = nadlan_ph_region( $p['city'] ?? '' ); $used[ $reg ] = 1; $count[ $reg ] = ( $count[ $reg ] ?? 0 ) + 1; if ( 'tlv' === $reg ) { $tlv++; } }
		/* the selection on the page: every priced Tel Aviv project, then the lowest published price in each other city */
		foreach ( $rows as $k => $p ) { $rows[ $k ]['_k'] = $k; }
		$sel = array(); $seen = array();
		foreach ( $rows as $p ) {
			if ( empty( $p['price_from'] ) ) { continue; }
			$reg = nadlan_ph_region( $p['city'] ?? '' ); $ck = str_replace( '-', ' ', (string) ( $p['city'] ?? '' ) );
			if ( 'tlv' === $reg ) { $sel[] = $p; continue; }
			if ( isset( $seen[ $ck ] ) ) { continue; }
			$seen[ $ck ] = 1; $sel[] = $p;
		}
		$all_n = count( $rows );
		/* HAD-697 (10.11.2026): every project is in the HTML. Until now only the selection (95 rows) was printed and the rest came from
		 * the JSON on a click, so a crawler never saw 469 projects. The selection still opens the table; the others follow it, collapsed
		 * exactly as before the "show all" button, Tel Aviv and the centre first, priced before unpriced. */
		$in = array(); foreach ( $sel as $p ) { $in[ $p['_k'] ] = 1; }
		$rest = array(); foreach ( $rows as $p ) { if ( ! isset( $in[ $p['_k'] ] ) ) { $rest[] = $p; } }
		$rows = $sel;
		/* Ben, 10.11.2026: the table opens on Tel Aviv, then the centre; usort is not stable on old PHP, so the price order is kept by hand */
		$by_region = function ( $a, $b ) { $ra = nadlan_ph_region_rank( $a['city'] ?? '' ); $rb = nadlan_ph_region_rank( $b['city'] ?? '' ); return $ra !== $rb ? $ra - $rb : $a['_o'] - $b['_o']; };
		foreach ( $rows as $k => $p ) { $rows[ $k ]['_o'] = $k; }
		usort( $rows, $by_region );
		foreach ( $rest as $k => $p ) { $rest[ $k ]['_o'] = $k; }
		usort( $rest, $by_region );
		$rows = array_merge( $rows, $rest );
		$tr = '';
		foreach ( $rows as $i => $p ) {
			$reg = nadlan_ph_region( $p['city'] ?? '' );
			$name = esc_html( $p['name'] ?? '' );
			if ( ! empty( $p['url'] ) ) { $name = '<a href="' . esc_url( home_url( $p['url'] ) ) . '">' . $name . '</a>'; }
			$place = trim( ( $p['neighbourhood'] ?? '' ) . ( ! empty( $p['neighbourhood'] ) && ! empty( $p['city'] ) ? ', ' : '' ) . ( $p['city'] ?? '' ) );
			$price = (int) ( $p['price_from'] ?? 0 );
			$pcell = $price ? '<b>' . esc_html( nadlan_ph_nis( $price ) ) . '</b>' . ( ! empty( $p['price_note'] ) ? '<small>' . esc_html( $p['price_note'] ) . '</small>' : '' )
				: ( ! empty( $p['price_psqm'] ) ? '<b>' . esc_html( nadlan_ph_nis( $p['price_psqm'] ) ) . '</b><small>למ"ר</small>' : '<span class="nlph-na">לפי פנייה ליזם</span>' );
			$stv = (string) ( $p['status'] ?? '' );
			$tr .= '<tr data-reg="' . esc_attr( $reg ) . '" data-st="' . esc_attr( $stv ) . '" data-price="' . (int) $price . '"' . ( $i >= 16 ? ' class="nlph-more"' : '' ) . '>'
				. '<th scope="row">' . $name . '<small>' . esc_html( $place ) . '</small></th>'
				. '<td data-l="יזם">' . esc_html( $p['developer'] ?? '' ) . '</td>'
				. '<td data-l="חדרים">' . esc_html( $p['rooms'] ?? '' ) . '</td>'
				. '<td data-l="החל מ" class="nlph-p">' . $pcell . '</td>'
				. '<td data-l="תנאים">' . esc_html( $p['deal'] ?? '' ) . '</td>'
				. '<td data-l="שלב">' . ( isset( $st[ $stv ] ) ? '<span class="nlph-st nlph-st--' . esc_attr( $stv ) . '">' . esc_html( $st[ $stv ] ) . '</span>' : '' ) . ( ! empty( $p['delivery'] ) ? '<small>מסירה: ' . esc_html( $p['delivery'] ) . '</small>' : '' ) . '</td>'
				. '</tr>';
		}
		$chips = '<button type="button" class="is-on" data-reg="">כל הארץ <i>' . $all_n . '</i></button>';
		foreach ( $regions as $k => $label ) {
			if ( empty( $used[ $k ] ) ) { continue; }
			$chips .= '<button type="button" data-reg="' . esc_attr( $k ) . '">' . esc_html( $label ) . ' <i>' . (int) $count[ $k ] . '</i></button>';
		}
		$json = plugins_url( 'data/projects-market.json', dirname( __DIR__ ) . '/nadlan-config.php' );
		$jf = dirname( __DIR__ ) . '/data/projects-market.json';
		$json = add_query_arg( 'v', is_readable( $jf ) ? filemtime( $jf ) : 1, $json );
		$read = ! empty( $m['read'] ) ? date_i18n( 'j.n.Y', strtotime( $m['read'] ) ) : '';
		ob_start(); ?>
<section class="nlph-sec" id="nlph-market" aria-labelledby="nlph-market-h" data-src="<?php echo esc_url( $json ); ?>" data-all="<?php echo (int) $all_n; ?>" data-full="1" data-home="<?php echo esc_url( home_url( '/' ) ); ?>">
	<p class="nlph-kick">פרויקטים בשיווק · מחירים כפי שפרסמו היזמים</p>
	<h2 id="nlph-market-h">פרויקטים חדשים בשיווק: מחירים, חדרים ותנאי תשלום</h2>
	<p class="nlph-lede"><?php echo (int) $all_n; ?> פרויקטים חדשים שנמצאים עכשיו בשיווק, <?php echo (int) $tlv; ?> מהם בתל אביב, עם המחיר שהיזם פרסם, מספר החדרים, תנאי התשלום, שלב הפרויקט ומועד המסירה כשהוא פורסם. בוחרים אזור, ממיינים לפי מחיר ומשווים בין פרויקטים לפני שפונים ליזם. בראש הטבלה: כל הפרויקטים המתומחרים בתל אביב והמחיר הנמוך ביותר שפורסם בכל עיר, ואחריהם כל שאר הפרויקטים.</p>
	<div class="nlph-tools">
		<div class="nlph-chips" role="group" aria-label="סינון לפי אזור"><?php echo $chips; // phpcs:ignore ?></div>
		<div class="nlph-sel">
			<label>שלב <select data-f="st"><option value="">הכל</option><option value="presale">פריסייל</option><option value="marketing">בשיווק</option><option value="construction">בבנייה</option><option value="near">אכלוס קרוב או מיידי</option></select></label>
			<label>מחיר <select data-f="max"><option value="">כל המחירים</option><option value="1000000">עד מיליון ₪</option><option value="1200000">עד 1.2 מיליון ₪</option><option value="1500000">עד 1.5 מיליון ₪</option><option value="2000000">עד 2 מיליון ₪</option><option value="2500000">עד 2.5 מיליון ₪</option><option value="3000000">עד 3 מיליון ₪</option><option value="4000000">עד 4 מיליון ₪</option><option value="6000000">עד 6 מיליון ₪</option></select></label>
			<label>מיון <select data-f="sort"><option value="rec">מומלצים</option><option value="asc">מחיר: מהנמוך</option><option value="desc">מחיר: מהגבוה</option></select></label>
		</div>
	</div>
	<div class="nlph-tw"><table class="nlph-mt">
		<thead><tr><th scope="col">פרויקט</th><th scope="col">יזם</th><th scope="col">חדרים</th><th scope="col">החל מ</th><th scope="col">תנאי תשלום</th><th scope="col">שלב</th></tr></thead>
		<tbody><?php echo $tr; // phpcs:ignore ?></tbody>
	</table></div>
	<p class="nlph-empty" hidden>אין פרויקט שמתאים לסינון הזה. נסו אזור אחר או טווח מחירים רחב יותר.</p>
	<button type="button" class="nlph-btn nlph-btn--ghost" id="nlph-more">הצגת כל <?php echo (int) $all_n; ?> הפרויקטים בשיווק</button>
	<p class="nlph-src">המחירים, החדרים, התנאים ומועדי המסירה כפי שפרסמו היזמים באתריהם ובפרסומי השיווק של הפרויקטים<?php echo $read ? ', נכון ל־' . esc_html( $read ) : ''; ?>. מחיר "החל מ" הוא מחיר הדירה הזולה בפרויקט באותו יום. פרויקט בלי מחיר מופיע כ"לפי פנייה ליזם". המחיר הסופי נקבע מול היזם ובחוזה.</p>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_tlv_html' ) ) {
	function nadlan_ph_tlv_html( $facets ) {
		$v = nadlan_ph_value(); $t = $v['תל אביב יפו'] ?? array();
		$n_tlv = 0; foreach ( (array) ( $facets['cities'] ?? array() ) as $c ) { if ( false !== mb_strpos( $c['name'], 'תל אביב' ) ) { $n_tlv += (int) $c['n']; } }
		$m = nadlan_ph_market(); $areas = array( 'north' => array(), 'centre' => array(), 'east' => array(), 'south' => array(), 'jaffa' => array() );
		foreach ( $m['projects'] as $p ) {
			if ( 'tlv' !== nadlan_ph_region( $p['city'] ?? '' ) ) { continue; }
			$a = nadlan_ph_tlv_area( ( $p['neighbourhood'] ?? '' ) . ' ' . ( $p['street'] ?? '' ) ) ?: ( false !== mb_strpos( (string) ( $p['city'] ?? '' ), 'יפו' ) && false === mb_strpos( (string) ( $p['city'] ?? '' ), 'תל אביב' ) ? 'jaffa' : '' );
			if ( $a ) { $areas[ $a ][] = $p; }
		}
		$hood = array(); foreach ( (array) ( $t['hoods'] ?? array() ) as $h ) { $hood[ $h['n'] ] = $h; }
		$hp = function ( $name, $room = 'r4' ) use ( $hood ) { foreach ( $hood as $k => $h ) { if ( 0 === mb_strpos( $k, $name ) && ! empty( $h[ $room ][0] ) ) { return (int) $h[ $room ][0]; } } return 0; };
		$def = array(
			'north'  => array( 'צפון העיר', 'רובע שדה דב, רמת אביב, נאות אפקה, הדר יוסף, כיכר המדינה, הצפון הישן והחדש', 'הריכוז הגדול ביותר של מגדלי מגורים חדשים בעיר. הפרויקטים החדשים בתל אביב ליד הים נמצאים בעיקר כאן, ברובע שדה דב על קו החוף הצפוני. לצידם פרויקטי התחדשות עירונית בצפון הישן והחדש ובנאות אפקה.', array( array( 'בבלי', 'בבלי' ), array( 'הצפון החדש החלק הצפ', 'הצפון החדש, צפון' ), array( 'נאות אפקה א', 'נאות אפקה א׳' ), array( 'הדר יוסף', 'הדר יוסף' ) ), array( '/sde-dov/' => 'רובע שדה דב', '/north-tel-aviv/' => 'צפון תל אביב', '/projects/hamedina/' => 'כיכר המדינה' ) ),
			'centre' => array( 'מרכז העיר', 'לב העיר, הצפון הישן הדרומי, שרונה ומתחם סומייל', 'מגדלי יוקרה סביב אבן גבירול, קריית הממשלה ושרונה, ובנייני בוטיק ופרויקטי תמ"א 38 בתוך הרובעים הוותיקים.', array( array( 'לב העיר', 'לב העיר' ), array( 'גני שרונה', 'גני שרונה' ), array( 'כרם התימנים', 'כרם התימנים' ) ), array( '/projects/duo-tel-aviv/' => 'DUO', '/projects/h-infinity-somail-tel-aviv/' => 'H Infinity' ) ),
			'east'   => array( 'מזרח העיר', 'יד אליהו, נחלת יצחק, ביצרון ורמת ישראל, הסוללים', 'פינוי בינוי ובנייה חדשה לאורך דרך השלום, ביד אליהו ובנחלת יצחק, במחירים נמוכים יותר מצפון העיר.', array( array( 'נחלת יצחק', 'נחלת יצחק' ), array( 'ביצרון', 'ביצרון' ), array( 'יד אליהו', 'יד אליהו' ) ), array( '/tel-aviv-apartment-prices/' => 'מחירי דירות בתל אביב' ) ),
			'south'  => array( 'דרום העיר', 'פלורנטין, שפירא, נווה שאנן, קריית שלום, נווה עופר', 'מתחמי התחדשות עירונית ובנייה חדשה בשכונות הדרום, עם מחירי הכניסה הנמוכים בעיר.', array( array( 'קרית שלום', 'קריית שלום' ), array( 'דקר', 'דקר' ), array( 'נוה חן', 'נווה חן' ) ), array() ),
			'jaffa'  => array( 'יפו', 'צפון יפו, עג׳מי, יפו ד׳, צהלון', 'פרויקטים לאורך החוף ובתוך יפו העתיקה והחדשה, לצד שיכונים ותיקים שעוברים התחדשות.', array( array( 'צפון יפו', 'צפון יפו', 'r3' ), array( 'יפו ד', 'יפו ד׳', 'r3' ) ), array() ),
		);
		$cards = '';
		foreach ( $def as $k => $d ) {
			$ps = $areas[ $k ]; $lo = 0; $hi = 0; $names = array();
			foreach ( $ps as $p ) { $pr = (int) ( $p['price_from'] ?? 0 ); if ( $pr ) { $lo = $lo ? min( $lo, $pr ) : $pr; $hi = max( $hi, $pr ); } if ( count( $names ) < 6 ) { $names[] = esc_html( $p['name'] ); } }
			$med = '';
			foreach ( $d[3] as $hh ) { $r = $hh[2] ?? 'r4'; $x = $hp( $hh[0], $r ); if ( $x ) { $med .= '<li><span>' . esc_html( $hh[1] ) . '</span><b>' . esc_html( nadlan_ph_mil( $x ) ) . '</b><small>' . ( 'r3' === $r ? '3 חד׳' : '4 חד׳' ) . '</small></li>'; } }
			$links = ''; foreach ( $d[4] as $path => $label ) { $links .= '<a href="' . esc_url( home_url( $path ) ) . '">' . esc_html( $label ) . '</a>'; }
			$cards .= '<article class="nlph-area"><h3>' . esc_html( $d[0] ) . '</h3><p class="nlph-area__n">' . esc_html( $d[1] ) . '</p><p>' . esc_html( $d[2] ) . '</p>'
				. ( $ps ? '<p class="nlph-area__m"><b>' . count( $ps ) . '</b> פרויקטים בשיווק בטבלה' . ( $lo ? ', החל מ־<b>' . esc_html( nadlan_ph_nis( $lo ) ) . '</b>' . ( $hi > $lo ? ' ועד ' . esc_html( nadlan_ph_nis( $hi ) ) : '' ) : '' ) . '</p><p class="nlph-area__p">' . implode( ' · ', $names ) . '</p>' : '' )
				. ( $med ? '<p class="nlph-area__k">חציון עסקאות, 1-3.2026</p><ul class="nlph-area__med">' . $med . '</ul>' : '' )
				. ( $links ? '<p class="nlph-area__l">' . $links . '</p>' : '' ) . '</article>';
		}
		ob_start(); ?>
<section class="nlph-sec" id="nlph-tlv" aria-labelledby="nlph-tlv-h">
	<p class="nlph-kick">תל אביב יפו</p>
	<h2 id="nlph-tlv-h">פרויקטים חדשים בתל אביב: איפה בונים, כמה זה עולה ומה בדרך</h2>
	<p class="nlph-lede">תל אביב יפו היא העיר שבה מתחילים לבנות הכי הרבה דירות בישראל: 7,611 התחלות בנייה ב־12 החודשים שהסתיימו ביוני 2026, עלייה של 19.9%. בקטלוג של נדל"ן <?php echo (int) $n_tlv; ?> פרויקטים בעיר, מבנייה חדשה ברובע שדה דב ועד פינוי בינוי ביד אליהו. מחפשים דירות חדשות בתל אביב או דירות מקבלן בתל אביב? כאן רואים מה נבנה בכל אזור בעיר, כמה עולות הדירות בשכונה ואילו פרויקטים בשיווק עכשיו.</p>
	<ul class="nlph-stats">
		<li><b>7,611</b><span>התחלות בנייה בעיר, יולי 2025 עד יוני 2026, מקום ראשון בארץ</span></li>
		<li><b>9,820</b><span>דירות חדשות לא מכורות בעיר, סוף אוגוסט 2026</span></li>
		<li><b>878</b><span>דירות חדשות שנמכרו בעיר ביוני עד אוגוסט 2026</span></li>
		<?php if ( ! empty( $t['r4'] ) ) : ?><li><b><?php echo esc_html( nadlan_ph_mil( $t['r4'] ) ); ?></b><span>חציון עסקה לדירת 4 חדרים, <?php echo esc_html( $t['q4'] ?? '' ); ?><?php echo ! empty( $t['yoy4'] ) ? ', ' . esc_html( nadlan_ph_yoy( $t['yoy4'] ) ) : ''; ?></span></li><?php endif; ?>
	</ul>
	<div class="nlph-areas"><?php echo $cards; // phpcs:ignore ?></div>
	<h3>התוכניות שמעצבות את העיר</h3>
	<div class="nlph-tw"><table class="nlph-plans">
		<thead><tr><th scope="col">תוכנית</th><th scope="col">מה היא כוללת</th><th scope="col">איפה היא עומדת</th></tr></thead>
		<tbody>
			<tr><th scope="row"><a href="<?php echo esc_url( home_url( '/sde-dov/' ) ); ?>">רובע שדה דב</a></th><td data-l="מה כוללת">כ־16,000 דירות לכ־40,000 תושבים על כ־1,300 דונם, מהן כ־7,000 דירות לדיור בהישג יד, לצד מלונות, תעסוקה ומסחר</td><td data-l="איפה עומדת">מתחם אשכול (כ־4,800 דירות) אושר במאי 2021, המרכז (כ־7,100 דירות) אושר ב־2025, הצפון (כ־4,000 דירות) בתהליך אישור</td></tr>
			<tr><th scope="row">צפון מערב, תא/3700</th><td data-l="מה כוללת">רובע מגורים חדש לאורך החוף הצפוני, עם חמש תוכניות מפורטות (3700/1 עד 3700/5)</td><td data-l="איפה עומדת">ההתנגדויות לתוכניות המפורטות נשמעו ב־2019</td></tr>
			<tr><th scope="row">תוכניות הרובעים 3 ו־4</th><td data-l="מה כוללת">תא/3616א ו־תא/3729א: תוספת קומות, חיזוק ובנייה מחדש של בניינים ישנים במרכז העיר</td><td data-l="איפה עומדת">אושרו ב־2018 ומחליפות את תוכנית ג׳ לבנייה על הגגות</td></tr>
			<tr><th scope="row"><a href="<?php echo esc_url( home_url( '/projects/hamedina/' ) ); ?>">כיכר המדינה</a></th><td data-l="מה כוללת">תא/מק/2500/א: 453 דירות סביב הכיכר</td><td data-l="איפה עומדת">בתוקף מ־2013, שלב "גמר שלד" לפי אתר העירייה, אפריל 2026</td></tr>
			<tr><th scope="row"><a href="<?php echo esc_url( home_url( '/urban-renewal/' ) ); ?>">פינוי בינוי ותמ"א 38</a></th><td data-l="מה כוללת">כמעט מחצית מהתחלות הבנייה של "הריסה ובנייה" בישראל נמצאות במחוז תל אביב</td><td data-l="איפה עומדת">17,670 התחלות הריסה ובנייה ב־12 חודשים עד יוני 2026, 45.9% מהן במחוז תל אביב</td></tr>
		</tbody>
	</table></div>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_prices_html' ) ) {
	function nadlan_ph_prices_html( $facets ) {
		$v = nadlan_ph_value(); if ( ! $v ) { return ''; }
		$cnt = array(); foreach ( (array) ( $facets['cities'] ?? array() ) as $c ) { $cnt[ str_replace( '-', ' ', $c['name'] ) ] = (int) $c['n']; }
		$mk = array(); foreach ( nadlan_ph_market()['projects'] as $p ) { $pr = (int) ( $p['price_from'] ?? 0 ); if ( ! $pr ) { continue; } $k = str_replace( '-', ' ', (string) ( $p['city'] ?? '' ) ); $mk[ $k ] = isset( $mk[ $k ] ) ? min( $mk[ $k ], $pr ) : $pr; }
		$rows = array(); $max = 0;
		foreach ( $v as $city => $d ) { if ( empty( $d['r4'] ) ) { continue; } $rows[] = array( $city, $d ); $max = max( $max, (int) $d['r4'] ); }
		usort( $rows, function ( $a, $b ) { return (int) $b[1]['r4'] - (int) $a[1]['r4']; } );
		$alias = array( 'פתח תקווה' => 'פתח תקוה', 'קריית אונו' => 'קרית אונו', 'גבעתיים' => 'גבעתים' );
		$tr = ''; $bars = '';
		foreach ( $rows as $r ) {
			list( $city, $d ) = $r; $n = $cnt[ $city ] ?? ( $cnt[ $alias[ $city ] ?? '' ] ?? 0 );
			$q = esc_url( add_query_arg( 'city', $city, home_url( '/projects/' ) ) );
			$from = $mk[ $city ] ?? ( $mk[ $alias[ $city ] ?? '' ] ?? 0 );
			$tr .= '<tr><th scope="row"><a href="' . esc_url( home_url( $d['page'] ?? '/apartment-prices/' ) ) . '">' . esc_html( $city ) . '</a></th>'
				. '<td data-l="3 חדרים">' . ( ! empty( $d['r3'] ) ? esc_html( nadlan_ph_nis( $d['r3'] ) ) : '' ) . '</td>'
				. '<td data-l="4 חדרים"><b>' . esc_html( nadlan_ph_nis( $d['r4'] ) ) . '</b>' . ( isset( $d['yoy4'] ) ? '<small>' . esc_html( nadlan_ph_yoy( $d['yoy4'] ) ) . '</small>' : '' ) . '</td>'
				. '<td data-l="5 חדרים">' . ( ! empty( $d['r5'] ) ? esc_html( nadlan_ph_nis( $d['r5'] ) ) : '' ) . '</td>'
				. '<td data-l="פרויקט חדש החל מ">' . ( $from ? esc_html( nadlan_ph_nis( $from ) ) : '' ) . '</td>'
				. '<td data-l="בקטלוג">' . ( $n ? '<a href="' . $q . '">' . $n . ' פרויקטים</a>' : '' ) . '</td></tr>';
			$bars .= '<li style="--w:' . round( 100 * (int) $d['r4'] / max( 1, $max ), 1 ) . '%"' . ( 'תל אביב יפו' === $city ? ' class="is-tlv"' : '' ) . '><span>' . esc_html( $city ) . '</span><i></i><b>' . esc_html( nadlan_ph_mil( $d['r4'] ) ) . '</b></li>';
		}
		ob_start(); ?>
<section class="nlph-sec" id="nlph-prices" aria-labelledby="nlph-prices-h">
	<p class="nlph-kick">מחירים לפי עיר · עסקאות שנסגרו</p>
	<h2 id="nlph-prices-h">מחירי דירות חדשות לפי עיר</h2>
	<p class="nlph-lede">לפני שמשווים מחיר של פרויקט חדש, כדאי לדעת כמה שולם בפועל בעיר. הטבלה מציגה את חציון מחירי העסקאות לפי מספר חדרים בינואר עד מרץ 2026, לפי רשות המסים, ולצידו המחיר הנמוך ביותר שפרסם יזם בטבלת הפרויקטים בשיווק וכמה פרויקטים יש בקטלוג בכל עיר. שם העיר מוביל למחירון המלא שלה.</p>
	<ol class="nlph-bars" aria-label="חציון מחיר לדירת 4 חדרים לפי עיר"><?php echo $bars; // phpcs:ignore ?></ol>
	<div class="nlph-tw"><table class="nlph-pt">
		<thead><tr><th scope="col">עיר</th><th scope="col">3 חדרים</th><th scope="col">4 חדרים</th><th scope="col">5 חדרים</th><th scope="col">פרויקט חדש החל מ</th><th scope="col">בקטלוג</th></tr></thead>
		<tbody><?php echo $tr; // phpcs:ignore ?></tbody>
	</table></div>
	<p class="nlph-src">חציון כל העסקאות שדווחו לרשות המסים (דירות חדשות ויד שנייה), לפי אתר נדל"ן הממשלתי, ינואר עד מרץ 2026. "פרויקט חדש החל מ": המחיר הנמוך שפרסם יזם בעיר, מתוך טבלת הפרויקטים בשיווק.</p>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_catalog_html' ) ) {
	function nadlan_ph_catalog_html( $facets ) {
		$total = (int) ( $facets['total'] ?? 0 ); $types = (array) ( $facets['types'] ?? array() );
		$cities = (array) ( $facets['cities'] ?? array() );
		$s = nadlan_ph_stage_counts(); $ncity = (int) ( $s['cities'] ?? 0 ); unset( $s['cities'] ); $sum = max( 1, array_sum( $s ) );
		$tl = array( 'pinui_binui' => 'פינוי בינוי', 'new_build' => 'בנייה חדשה', 'tama38' => 'תמ״א 38' );
		$tb = ''; $tsum = 0; foreach ( $tl as $k => $label ) { $tsum += (int) ( $types[ $k ] ?? 0 ); }
		foreach ( $tl as $k => $label ) { $n = (int) ( $types[ $k ] ?? 0 ); if ( ! $n ) { continue; } $tb .= '<li style="--w:' . max( 1.5, round( 100 * $n / max( 1, $tsum ), 1 ) ) . '%"><span>' . esc_html( $label ) . '</span><i></i><b>' . number_format( $n ) . '</b></li>'; }
		$sl = array( 'plan' => 'בתכנון', 'approved' => 'תוכנית מאושרת', 'build' => 'בביצוע', 'market' => 'בשיווק' );
		$sb = ''; foreach ( $sl as $k => $label ) { if ( empty( $s[ $k ] ) ) { continue; } $sb .= '<li style="--w:' . max( 1.5, round( 100 * $s[ $k ] / $sum, 1 ) ) . '%"><span>' . esc_html( $label ) . '</span><i></i><b>' . number_format( $s[ $k ] ) . '</b></li>'; }
		$top = array_slice( $cities, 0, 5 ); $tn = array(); foreach ( $top as $c ) { $tn[] = esc_html( $c['name'] ) . ' (' . (int) $c['n'] . ')'; }
		ob_start(); ?>
<section class="nlph-sec" id="nlph-catalog" aria-labelledby="nlph-catalog-h">
	<p class="nlph-kick">הקטלוג</p>
	<h2 id="nlph-catalog-h">פרויקטים חדשים בישראל: מה יש בקטלוג</h2>
	<p class="nlph-lede">הקטלוג של נדל"ן מרכז <?php echo number_format( $total ); ?> פרויקטים חדשים למגורים ב־<?php echo (int) ( $ncity ?: count( $cities ) ); ?> ערים: בנייה חדשה על מגרשים פנויים, מתחמי פינוי בינוי ופרויקטי תמ"א 38. הערים עם הכי הרבה פרויקטים: <?php echo implode( ', ', $tn ); // phpcs:ignore ?>. לכל פרויקט חדש כרטיס אחד עם הנתונים שידועים: עיר ושכונה, יזם, סטטוס, מספר יחידות הדיור, קומות, מועד אכלוס משוער ובמתחמי התחדשות שנת תוקף התוכנית, ולצדם מחיר למ"ר בסביבה לפי עסקאות שדווחו לרשות המסים. מה שלא ידוע לא מופיע.</p>
	<div class="nlph-two">
		<div><h3>לפי סוג פרויקט</h3><ol class="nlph-bars nlph-bars--thin"><?php echo $tb; // phpcs:ignore ?></ol></div>
		<div><h3>לפי שלב</h3><ol class="nlph-bars nlph-bars--thin"><?php echo $sb; // phpcs:ignore ?></ol></div>
	</div>
	<p>רוב הפרויקטים בקטלוג הם מתחמי פינוי בינוי שנמצאים בשלבי תכנון ואישור, לפי נתוני התכנון הרשמיים. הם מראים איפה ייבנו הדירות החדשות של השנים הבאות. פרויקטים שכבר בשיווק מופיעים בטבלת הפרויקטים בשיווק למעלה, עם המחיר שפרסם היזם. מסננים את הקטלוג לפי עיר, סוג, שלב וגודל, או לוחצים "קרוב אליי" ומקבלים את הפרויקטים החדשים באזור.</p>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_timeline_html' ) ) {
	function nadlan_ph_timeline_html() {
		$steps = array(
			array( 'תכנון ואישור תוכנית', 'שנים, לפי סוג הפרויקט', 'התוכנית מאושרת בוועדה. בפינוי בינוי נדרשת גם הסכמת בעלי הדירות.', 'שלב שבו לרוב אין עדיין מכירה לציבור' ),
			array( 'היתר בנייה ותחילת שיווק', 'פריסייל ושיווק', 'היתר בנייה מאפשר להתחיל לבנות. חלק מהיזמים מוכרים כבר לפני ההיתר, בפריסייל.', 'תשלום ראשון: 7% לכל היותר בלי בטוחה' ),
			array( 'חפירה ויסודות', 'חודשים 0 עד 6', 'עבודות החפירה, הדיפון והיסודות. כאן מתחיל לוח הזמנים של הבנייה עצמה.', 'כל תשלום בשובר, ערבות תוך 14 ימי עסקים' ),
			array( 'שלד', 'חודשים 6 עד 20', 'הקומות עולות. שישה חודשים לפחות אחרי סיום היסודות נסגר החלון לבקשות שינוי במפרט.', 'תשלומים לפי קצב הבנייה, עד מחצית מכל תשלום צמודה' ),
			array( 'גמר ומערכות', 'חודשים 20 עד 32', 'טיח, ריצוף, מטבחים, מעליות ופיתוח סביבתי.', 'ההצמדה נעצרת במועד המסירה שבחוזה' ),
			array( 'טופס 4 ומסירה', 'כ־32 חודשים בממוצע', 'אישור אכלוס, בדיקת הדירה ומסירת המפתח. איחור של יותר מחודש מזכה בפיצוי לפי חוק המכר.', 'ליקויים גלויים מדווחים תוך שנה' ),
			array( 'רישום בית משותף', 'עד שנה מהמסירה', 'היזם רושם את הבניין כבית משותף בלשכת רישום המקרקעין.', 'תקופות בדק של 1 עד 7 שנים לפי סוג הליקוי' ),
			array( 'רישום הזכויות על שמכם', 'עד 6 חודשים מהרישום', 'הדירה נרשמת על שם הרוכש, והבטוחות מוחלפות ברישום.', 'אחריות של 3 שנים נוספות אחרי כל תקופת בדק' ),
		);
		$li = '';
		foreach ( $steps as $i => $s ) {
			$li .= '<li style="--i:' . $i . '"><span class="nlph-tl__n">' . ( $i + 1 ) . '</span><div><h3>' . esc_html( $s[0] ) . '</h3><p class="nlph-tl__t">' . esc_html( $s[1] ) . '</p><p>' . esc_html( $s[2] ) . '</p><p class="nlph-tl__g">' . esc_html( $s[3] ) . '</p></div></li>';
		}
		ob_start(); ?>
<section class="nlph-sec" id="nlph-timeline" aria-labelledby="nlph-timeline-h">
	<p class="nlph-kick">לוח זמנים</p>
	<h2 id="nlph-timeline-h">מהיתר בנייה ועד המפתח: כמה זמן לוקח פרויקט חדש</h2>
	<p class="nlph-lede">בניין מגורים בישראל נבנה בממוצע 31.8 חודשים, ו־37.3 חודשים בשקלול לפי מספר הדירות, לפי הלשכה המרכזית לסטטיסטיקה. מי שחותם בפריסייל או לפני ההיתר מוסיף לזה את זמן הרישוי. כך נראית הדרך מהתוכנית ועד הדירה הרשומה על שמכם, ומה מגן על הכסף בכל שלב.</p>
	<ol class="nlph-tl"><?php echo $li; // phpcs:ignore ?></ol>
	<p class="nlph-src">החודשים בשלבי הבנייה הם להמחשה לפי ממוצע של כ־32 חודשים לבניין. מועד המסירה המחייב הוא זה שבחוזה.</p>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_pay_html' ) ) {
	function nadlan_ph_pay_html() {
		$plans = array(
			array( 'לוח תשלומים רגיל (לדוגמה)', 'לפי קצב הבנייה', array( array( 15, 'חתימה' ), array( 20, 'יסודות' ), array( 25, 'שלד' ), array( 25, 'גמר' ), array( 15, 'מסירה' ) ) ),
			array( 'מבצע 20/80', '20% בחתימה, 80% במסירה', array( array( 20, 'חתימה' ), array( 80, 'מסירה' ) ) ),
			array( 'מבצע 10/90', '10% בחתימה, 90% במסירה', array( array( 10, 'חתימה' ), array( 90, 'מסירה' ) ) ),
		);
		$rows = '';
		foreach ( $plans as $p ) {
			$seg = ''; foreach ( $p[2] as $x ) { $seg .= '<i style="flex:' . (int) $x[0] . ' 1 0px"><b>' . (int) $x[0] . '%</b><small>' . esc_html( $x[1] ) . '</small></i>'; }
			$rows .= '<li><p><b>' . esc_html( $p[0] ) . '</b><span>' . esc_html( $p[1] ) . '</span></p><div class="nlph-paybar">' . $seg . '</div></li>';
		}
		ob_start(); ?>
<section class="nlph-sec" id="nlph-pay" aria-labelledby="nlph-pay-h">
	<p class="nlph-kick">תשלומים והצמדה</p>
	<h2 id="nlph-pay-h">איך משלמים על דירה מקבלן: לוח תשלומים, הצמדה ומבצעי 20/80</h2>
	<p class="nlph-lede">ברוב הפרויקטים החדשים משלמים בשלבים לאורך הבנייה. מבצעי 20/80 ו־10/90 דוחים את רוב התשלום למסירה. באוגוסט 2026 כ־30% מהדירות שיזמים מכרו בשוק החופשי, בחמישה מחוזות מס כולל תל אביב, נמכרו עם הטבת מימון כזאת, ובאזור המס תל אביב 21%.</p>
	<ul class="nlph-pay"><?php echo $rows; // phpcs:ignore ?></ul>
	<h3>ההצמדה למדד תשומות הבנייה, בתמונה אחת</h3>
	<div class="nlph-link" role="img" aria-label="מתוך מחיר הדירה: 20% הראשונים לא מוצמדים, ומהיתרה עד מחצית מכל תשלום מוצמדת, כלומר עד 40% מהמחיר">
		<i class="a" style="flex:20 1 0px"><b>20%</b><small>לא מוצמד</small></i><i class="b" style="flex:40 1 0px"><b>עד 40%</b><small>מותר להצמיד</small></i><i class="c" style="flex:40 1 0px"><b>40%</b><small>לא מוצמד</small></i>
	</div>
	<p>בחוזים שנחתמו מ־7.7.2022 (תיקון 9 לחוק המכר) מותר להצמיד עד מחצית מכל תשלום, התשלום הראשון של 20% מהמחיר לא מוצמד, וההצמדה נעצרת במועד המסירה שבחוזה גם אם המסירה מתאחרת. מדד תשומות הבנייה למגורים לספטמבר 2026: 104.0, עלייה של 3.6% ב־12 חודשים. כך, תשלום של מיליון ₪ שהמדד עלה עליו ב־3.6% יגדל לכל היותר ב־18,000 ₪.</p>
	<p>בנק ישראל הגביל מאפריל 2025 את מבצעי המימון: הלוואות בלון ובולט שהיזם משלם את הריבית שלהן מוגבלות ל־10% מהמשכנתאות של כל בנק ברבעון, ופרויקט שיותר מרבע מהחוזים בו דוחים יותר מ־40% מהמחיר למסירה מקבל דרישת הון גבוהה יותר. ההוראות בתוקף עד 31.12.2026.</p>
	<?php echo do_shortcode( '[nadlan_tool id="indexation"]' ); // phpcs:ignore ?>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_toolbox_html' ) ) {
	function nadlan_ph_toolbox_html() {
		$tools = array(
			'pcost'    => 'כמה כסף צריך',
			'ptax'     => 'מס רכישה',
			'afford'   => 'איזו דירה אפשר לקנות',
			'delay'    => 'פיצוי על איחור',
			'pinkas'   => 'בדיקת קבלן',
			'warranty' => 'בדק ואחריות',
		);
		$tabs = ''; $panels = ''; $i = 0;
		foreach ( $tools as $id => $label ) {
			$tabs .= '<button type="button" role="tab" id="nlph-tab-' . $id . '" aria-controls="nlph-pane-' . $id . '" aria-selected="' . ( 0 === $i ? 'true' : 'false' ) . '"' . ( 0 === $i ? '' : ' tabindex="-1"' ) . '>' . esc_html( $label ) . '</button>';
			$panels .= '<div role="tabpanel" id="nlph-pane-' . $id . '" aria-labelledby="nlph-tab-' . $id . '"' . ( 0 === $i ? '' : ' hidden' ) . '>' . do_shortcode( '[nadlan_tool id="' . $id . '"]' ) . '</div>';
			$i++;
		}
		ob_start(); ?>
<section class="nlph-sec" id="nlph-tools" aria-labelledby="nlph-tools-h">
	<p class="nlph-kick">מחשבונים</p>
	<h2 id="nlph-tools-h">מחשבונים לפני שקונים דירה מקבלן</h2>
	<p class="nlph-lede">שישה מחשבונים שעונים על השאלות של מי שקונה דירה בפרויקט חדש: כמה הון עצמי צריך, כמה מס רכישה ישולם, איזו דירה ההכנסה מאפשרת, כמה פיצוי מגיע על איחור, האם הקבלן רשום, ועד מתי אפשר לדרוש תיקון ליקויים. כל החישובים לפי הנתונים הרשמיים העדכניים.</p>
	<div class="nlph-tabs" role="tablist" aria-label="מחשבונים"><?php echo $tabs; // phpcs:ignore ?></div>
	<div class="nlph-panes"><?php echo $panels; // phpcs:ignore ?></div>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_checks_html' ) ) {
	function nadlan_ph_checks_html() {
		$checks = array(
			array( 'הקבלן רשום בפנקס הקבלנים', 'סטטוס פעיל, לא מוקפא ולא מותלה, וסיווג שמתאים להיקף הבנייה.', 'https://www.gov.il/apps/moch/rasham/home', 'פנקס הקבלנים, משרד הבינוי והשיכון', '/pinkas-hakablanim/', 'חיפוש קבלן אצלנו' ),
			array( 'יש בטוחה על כל שקל מעל 7%', 'ערבות חוק מכר, פוליסת ביטוח, משכנתא, הערת אזהרה או העברת בעלות. הערבות לא כוללת מע"מ, שמוחזר מקרן של משרד האוצר אם הערבות ממומשת.', 'https://he.wikisource.org/wiki/חוק_המכר_(דירות)_(הבטחת_השקעות_של_רוכשי_דירות)', 'חוק המכר (הבטחת השקעות), סעיף 2', '', '' ),
			array( 'משלמים רק בשוברים', 'בפרויקט עם ליווי פיננסי כל תשלום עובר דרך פנקס השוברים של הבנק המלווה, והערבות יוצאת תוך 14 ימי עסקים. יזם בלי ליווי חייב להודיע על כך בכתב לפני החתימה.', 'https://he.wikisource.org/wiki/חוק_המכר_(דירות)_(הבטחת_השקעות_של_רוכשי_דירות)', 'חוק המכר (הבטחת השקעות), סעיפים 2א1, 3ב', '', '' ),
			array( 'יש היתר בנייה', 'בתל אביב בודקים בתיק המידע ובמפת ההיתרים של העירייה. בפריסייל שואלים מתי צפוי ההיתר ומה קורה לכסף אם הוא מתעכב.', 'https://www.tel-aviv.gov.il/About/Pages/planning.aspx', 'מידע תכנוני, עיריית תל אביב יפו', '', '' ),
			array( 'המפרט הטכני חתום על הטופס הרשמי', 'מפרט לפי צו מכר דירות, עם מחירון לפריטים שאפשר לוותר עליהם או לשדרג, ומועד אחרון לבקשות שינוי.', 'https://he.wikisource.org/wiki/צו_מכר_דירות_(טופס_של_מפרט)', 'צו מכר דירות (טופס של מפרט)', '', '' ),
			array( 'ההצמדה בחוזה לפי החוק', 'עד מחצית מכל תשלום, בלי הצמדה על 20% הראשונים, ובלי הצמדה אחרי מועד המסירה שבחוזה.', 'https://fs.knesset.gov.il/24/law/24_lsr_628987.pdf', 'תיקון 9 לחוק המכר, סעיף 5ג', '/new-projects/construction-input-index/', 'מחשבון הצמדה' ),
			array( 'מועד המסירה והפיצוי כתובים', 'פיצוי לפי שכר דירה דומה מהחודש השני של האיחור, בלי ויתור כתנאי לקבלת המפתח.', 'https://fs.knesset.gov.il/24/law/24_lsr_628987.pdf', 'תיקון 9 לחוק המכר, סעיף 5א', '/new-projects/contractor-delay-compensation/', 'מחשבון פיצוי' ),
			array( 'שכר הטרחה של עורך דין היזם', 'עד 5,915 ₪ או 0.5% מהמחיר, הנמוך מביניהם, ועוד מע"מ. התקרה לא חלה על דירה מעל 4,642,750 ₪.', 'https://he.wikisource.org/wiki/תקנות_המכר_(דירות)_(הגבלת_גובה_ההוצאות_המשפטיות)', 'תקנות המכר (הגבלת ההוצאות המשפטיות)', '', '' ),
			array( 'נסח טאבו ותיק בית משותף', 'בודקים הערות אזהרה, משכנתאות ועיקולים. אחרי המסירה היזם רושם את הבית המשותף תוך שנה, ואת הזכויות על שמכם תוך 6 חודשים.', 'https://www.gov.il/he/service/land_registration_extract', 'נסח רישום מקרקעין, רשות מקרקעי ישראל ולשכות הרישום', '/real-estate-lawyer/condo-documents/', 'מסמכי בית משותף' ),
		);
		$li = '';
		foreach ( $checks as $i => $c ) {
			$li .= '<li><label><input type="checkbox" data-i="' . $i . '"><span><b>' . esc_html( $c[0] ) . '</b>' . esc_html( $c[1] ) . '</span></label><p class="nlph-ck__l"><a href="' . esc_url( $c[2] ) . '" target="_blank" rel="noopener">' . esc_html( $c[3] ) . '</a>' . ( $c[4] ? ' · <a href="' . esc_url( home_url( $c[4] ) ) . '">' . esc_html( $c[5] ) . '</a>' : '' ) . '</p></li>';
		}
		ob_start(); ?>
<section class="nlph-sec" id="nlph-checks" aria-labelledby="nlph-checks-h">
	<p class="nlph-kick">לפני החתימה</p>
	<h2 id="nlph-checks-h">דירה חדשה מקבלן: מה בודקים לפני שחותמים</h2>
	<p class="nlph-lede">תשע בדיקות שכדאי לעשות לפני שחותמים על חוזה עם יזם, כל אחת עם המקור הרשמי. מסמנים כל בדיקה שבוצעה, והרשימה נשמרת בדפדפן לפגישה הבאה.</p>
	<p class="nlph-ck__p" aria-live="polite"><b id="nlph-ck-n">0</b> מתוך <?php echo count( $checks ); ?> בדיקות בוצעו</p>
	<ol class="nlph-ck"><?php echo $li; // phpcs:ignore ?></ol>
	<p>המדריך המלא: <a href="<?php echo esc_url( home_url( '/new-projects/' ) ); ?>">המדריך המלא לקנייה מקבלן ובדיקת פרויקט חדש</a>. על המשא ומתן מול היזם: <a href="<?php echo esc_url( home_url( '/buying-new-apartment-developer-2026-negotiation/' ) ); ?>">קונים דירה מקבלן ב־2026</a>. ולפני כל קנייה: <a href="<?php echo esc_url( home_url( '/buying-apartment/' ) ); ?>">קניית דירה בישראל: בדיקות לפני חתימה</a>.</p>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_types_html' ) ) {
	function nadlan_ph_types_html() {
		$cols = array(
			array( 'בנייה חדשה', 'פרויקט על מגרש פנוי, לרוב בשכונה או ברובע חדש', 'בדרך כלל 3 שנים מתחילת הבנייה', 'מחיר השוק של האזור', 'עיכוב בהיתר או בבנייה', '/new-projects/', 'המדריך לקנייה מקבלן' ),
			array( 'פינוי בינוי', 'מתחם של כמה בניינים ישנים שנהרסים ונבנים מחדש', 'תכנון והסכמות לוקחים שנים, אחר כך בנייה רגילה', 'דומה לבנייה חדשה באזור', 'קצב ההסכמות והאישורים', '/urban-renewal/', 'התחדשות עירונית' ),
			array( 'תמ"א 38', 'בניין בודד: חיזוק ותוספת קומות, או הריסה ובנייה מחדש', 'קצר יותר, בניין אחד', 'לרוב דירות בודדות בבניין', 'עבודה ליד דיירים ותיקים', '/urban-renewal/', 'תמ"א 38 ופינוי בינוי' ),
			array( 'פריסייל', 'קנייה בשלב מוקדם, לרוב לפני היתר', 'ארוך יותר: מוסיפים את זמן הרישוי', 'נמוך ממחיר השיווק המלא', 'זמן עד המפתח וודאות ההיתר', '/new-projects/presale-apartment/', 'דירת פריסייל' ),
			array( 'דירה בהנחה', 'תוכנית ממשלתית בהגרלה לזכאים', 'לפי הפרויקט שבו זוכים', 'הנחה ממחיר השוק', 'הסיכוי לזכות בהגרלה', '/dira-behanacha/', 'דירה בהנחה' ),
			array( 'קבוצת רכישה', 'רוכשים שמתארגנים יחד וקונים קרקע', 'תלוי בהתארגנות ובאישורים', 'נמוך יותר כשהכול מצליח', 'סיכון גבוה יותר, בלי הגנות מלאות של קנייה מיזם', '/new-projects/purchasing-group/', 'קבוצת רכישה' ),
		);
		$rows = array( 'מה זה', 'זמן עד מפתח', 'מחיר', 'הסיכון העיקרי' );
		$th = ''; foreach ( $cols as $c ) { $th .= '<th scope="col">' . esc_html( $c[0] ) . '</th>'; }
		$tb = '';
		foreach ( $rows as $ri => $label ) {
			$tb .= '<tr><th scope="row">' . esc_html( $label ) . '</th>';
			foreach ( $cols as $c ) { $tb .= '<td data-l="' . esc_attr( $c[0] ) . '">' . esc_html( $c[ $ri + 1 ] ) . '</td>'; }
			$tb .= '</tr>';
		}
		$tb .= '<tr><th scope="row">להמשך קריאה</th>'; foreach ( $cols as $c ) { $tb .= '<td data-l="' . esc_attr( $c[0] ) . '"><a href="' . esc_url( home_url( $c[5] ) ) . '">' . esc_html( $c[6] ) . '</a></td>'; } $tb .= '</tr>';
		ob_start(); ?>
<section class="nlph-sec" id="nlph-types" aria-labelledby="nlph-types-h">
	<p class="nlph-kick">סוגי פרויקטים</p>
	<h2 id="nlph-types-h">בנייה חדשה, פינוי בינוי, תמ״א 38, פריסייל ודירה בהנחה: מה ההבדל לקונה</h2>
	<p class="nlph-lede">"פרויקט חדש" יכול להיות מגדל ברובע חדש, מתחם פינוי בינוי, בניין תמ"א 38 או דירה בהגרלה ממשלתית. בכולם קונים דירה חדשה מיזם עם הגנות חוק המכר, אבל הזמן עד המפתח, המחיר והסיכון שונים מאוד. ב־12 החודשים שהסתיימו ביוני 2026 התחילו לבנות בישראל 76,040 דירות, ו־17,670 מהן בפרויקטים של הריסה ובנייה מחדש.</p>
	<div class="nlph-tw"><table class="nlph-ty"><thead><tr><th scope="col"></th><?php echo $th; // phpcs:ignore ?></tr></thead><tbody><?php echo $tb; // phpcs:ignore ?></tbody></table></div>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_market_numbers_html' ) ) {
	function nadlan_ph_market_numbers_html() {
		$tiles = array(
			array( '10,110', 'דירות חדשות נמכרו ביוני עד אוגוסט 2026', 'עלייה של 24.9% לעומת השנה הקודמת', 'הלמ"ס' ),
			array( '85,680', 'דירות חדשות לא מכורות, סוף אוגוסט 2026', 'היצע של 26.7 חודשים', 'הלמ"ס' ),
			array( '26,330', 'מהן במחוז תל אביב', '30.7% מכל הדירות הלא מכורות', 'הלמ"ס' ),
			array( '76,040', 'התחלות בנייה ב־12 חודשים עד יוני 2026', '60,970 דירות הושלמו באותה תקופה', 'הלמ"ס' ),
			array( '61%', 'מהדירות שיזמים מכרו באוגוסט 2026 נמכרו על הנייר', 'מסירה בעוד 24 חודשים לפחות', 'משרד האוצר' ),
			array( '104.0', 'מדד תשומות הבנייה למגורים, ספטמבר 2026', 'עלייה של 3.6% ב־12 חודשים', 'הלמ"ס' ),
			array( '0.4%', 'ירידה במדד מחירי הדירות החדשות בשנה', 'מדד מחירי הדירות הכללי ירד ב־1.8%', 'הלמ"ס' ),
			array( '3.25%', 'ריבית בנק ישראל, הוחלט ב־21.10.2026', 'פריים 4.75%', 'בנק ישראל' ),
		);
		$li = ''; foreach ( $tiles as $t ) { $li .= '<li><b dir="ltr">' . esc_html( $t[0] ) . '</b><span>' . esc_html( $t[1] ) . '</span><small>' . esc_html( $t[2] ) . ' · ' . esc_html( $t[3] ) . '</small></li>'; }
		ob_start(); ?>
<section class="nlph-sec" id="nlph-numbers" aria-labelledby="nlph-numbers-h">
	<p class="nlph-kick">השוק במספרים · עדכון אוקטובר 2026</p>
	<h2 id="nlph-numbers-h">שוק הדירות החדשות במספרים</h2>
	<p class="nlph-lede">הנתונים הרשמיים האחרונים על מכירות, מלאי, בנייה ומחירים של דירות חדשות בישראל, מהלשכה המרכזית לסטטיסטיקה, ממשרד האוצר ומבנק ישראל. 41.8% מהדירות שנמכרו ביוני עד אוגוסט 2026 היו דירות חדשות.</p>
	<ul class="nlph-tiles"><?php echo $li; // phpcs:ignore ?></ul>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_cities_html' ) ) {
	function nadlan_ph_cities_html( $facets ) {
		$v = nadlan_ph_value(); $links = '';
		foreach ( array_slice( (array) ( $facets['cities'] ?? array() ), 0, 30 ) as $c ) {
			if ( (int) $c['n'] < 3 ) { continue; }
			$links .= '<a href="' . esc_url( add_query_arg( 'city', $c['name'], home_url( '/projects/' ) ) ) . '">פרויקטים חדשים ב' . esc_html( $c['name'] ) . ' <i>' . (int) $c['n'] . '</i></a>';
		}
		$prices = ''; foreach ( $v as $city => $d ) { if ( ! empty( $d['page'] ) ) { $prices .= '<a href="' . esc_url( home_url( $d['page'] ) ) . '">מחירי דירות ב' . esc_html( $city ) . '</a>'; } }
		ob_start(); ?>
<section class="nlph-sec" id="nlph-cities" aria-labelledby="nlph-cities-h">
	<h2 id="nlph-cities-h">פרויקטים חדשים לפי עיר</h2>
	<div class="nlcp-citylinks nlph-cl"><?php echo $links; // phpcs:ignore ?></div>
	<h3>מחירי דירות לפי עיר</h3>
	<div class="nlph-cl nlph-cl--s"><?php echo $prices; // phpcs:ignore ?></div>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_guides_html' ) ) {
	function nadlan_ph_guides_html() {
		$g = array(
			'/new-projects/'                              => array( 'המדריך לקנייה מקבלן', 'כל השלבים, מהפגישה הראשונה ועד המפתח' ),
			'/new-projects/presale-apartment/'            => array( 'דירת פריסייל', 'המחיר האמיתי, 20/80 ובדיקות לפני חתימה' ),
			'/developer-deals/'                           => array( 'מבצעי קבלנים', '20/80, 10/90 וההנחות ששוות כסף' ),
			'/new-projects/construction-input-index/'     => array( 'מדד תשומות הבנייה', 'חישוב ההצמדה על דירה מקבלן' ),
			'/new-projects/contractor-delay-compensation/' => array( 'איחור במסירה', 'הפיצוי לפי חוק המכר' ),
			'/new-projects/purchasing-group/'             => array( 'קבוצת רכישה', 'סיכונים, מיסוי והבדל מקנייה מקבלן' ),
			'/herzliya-projects/'                         => array( 'פרויקטים חדשים בהרצליה', 'המרינה, גליל ים והרצליה הירוקה' ),
			'/north-tel-aviv/'                            => array( 'צפון תל אביב', 'השכונות, הפרויקטים והמחירים' ),
			'/sde-dov/'                                   => array( 'רובע שדה דב', 'פרויקטים ודירות למכירה ברובע החדש' ),
			'/urban-renewal/map/'                         => array( 'מפת ההתחדשות העירונית', 'כל מתחמי פינוי בינוי לפי עיר' ),
			'/dira-behanacha/'                            => array( 'דירה בהנחה', 'הסיכוי לזכות בהגרלה בכל עיר' ),
			'/pinkas-hakablanim/'                         => array( 'פנקס הקבלנים', 'בדיקת קבלן רשום לפי שם או מספר' ),
			'/apartment-prices/'                          => array( 'מחירון הדירות של ישראל', 'כל הערים והמספרים במקום אחד' ),
			'/premium/'                                   => array( 'הקטלוג הפרימיום', 'פרויקטים עם בחירת דירה וסיור וירטואלי' ),
		);
		$li = ''; foreach ( $g as $path => $x ) { $li .= '<li><a href="' . esc_url( home_url( $path ) ) . '"><b>' . esc_html( $x[0] ) . '</b><span>' . esc_html( $x[1] ) . '</span></a></li>'; }
		ob_start(); ?>
<section class="nlph-sec" id="nlph-guides" aria-labelledby="nlph-guides-h">
	<h2 id="nlph-guides-h">מדריכים ומחשבונים לקונים דירה חדשה</h2>
	<ul class="nlph-guides"><?php echo $li; // phpcs:ignore ?></ul>
</section>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ph_faq_html' ) ) {
	function nadlan_ph_faq_html() {
		$h = '';
		foreach ( nadlan_ph_faq() as $qa ) {
			$h .= '<details><summary>' . esc_html( $qa[0] ) . '</summary><p>' . esc_html( $qa[1] ) . '</p>' . ( ! empty( $qa[2] ) ? '<p class="nlph-faq__l"><a href="' . esc_url( home_url( $qa[2] ) ) . '">' . esc_html( $qa[3] ?? '' ) . '</a></p>' : '' ) . '</details>';
		}
		return '<section class="nlph-sec" id="nlph-faq" aria-labelledby="nlph-faq-h"><h2 id="nlph-faq-h">שאלות נפוצות על פרויקטים חדשים ודירות מקבלן</h2><div class="nlcp-faq nlph-faq">' . $h . '</div></section>';
	}
}

if ( ! function_exists( 'nadlan_ph_sources_html' ) ) {
	function nadlan_ph_sources_html() {
		$s = array(
			'https://www.cbs.gov.il/he/mediarelease/DocLib/2026/317/04_26_317b.pdf' => 'הלשכה המרכזית לסטטיסטיקה: דירות בעסקאות נדל"ן, יוני עד אוגוסט 2026',
			'https://www.cbs.gov.il/he/mediarelease/DocLib/2026/297/04_26_297b.pdf' => 'הלשכה המרכזית לסטטיסטיקה: התחלות וגמר בנייה, יולי 2025 עד יוני 2026',
			'https://www.gov.il/BlobFolder/dynamiccollectorresultitem/review-real-estate-082026/he/reviews-and-publishes_review-real-estate-082026.pdf' => 'משרד האוצר, הכלכלן הראשי: סקירת שוק הדיור, אוגוסט 2026',
			'https://www.boi.org.il/media/ez4npagt/329.pdf' => 'בנק ישראל: הוראה 329, מגבלות על הלוואות לדיור',
			'https://www.boi.org.il/media/xwkag15z/h2816.pdf' => 'בנק ישראל: חוזר 2816, מבצעי מימון של יזמים',
			'https://www.gov.il/BlobFolder/policy/inst-01-2026/he/realestate_inst-01-2026.pdf' => 'רשות המסים: מדרגות מס רכישה 2026',
			'https://www.nadlan.gov.il/' => 'אתר נדל"ן הממשלתי: עסקאות שנסגרו',
			'https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx' => 'עיריית תל אביב יפו: רובע שדה דב',
			'https://www.tel-aviv.gov.il/Residents/Development/Pages/NewNeighborhoods.aspx' => 'עיריית תל אביב יפו: שכונות ופרויקטים חדשים',
			'https://www.gov.il/apps/moch/rasham/home' => 'משרד הבינוי והשיכון: פנקס הקבלנים',
		);
		$li = ''; foreach ( $s as $u => $l ) { $li .= '<li><a href="' . esc_url( $u ) . '" target="_blank" rel="noopener">' . esc_html( $l ) . '</a></li>'; }
		return '<section class="nlph-sec nlph-sec--src" id="nlph-sources" aria-labelledby="nlph-sources-h"><h2 id="nlph-sources-h">מקורות רשמיים</h2><ul class="nlph-srcs">' . $li . '</ul><p class="nlph-src">עודכן ב־' . esc_html( date_i18n( 'j.n.Y', strtotime( NADLAN_PH_UPDATED_HE ) ) ) . '. נדל"ן הוא אתר עצמאי. שמות פרויקטים ויזמים מופיעים לזיהוי בלבד.</p></section>';
	}
}

/* ------------------------------------------------------------------------------------------------ HAD-689 step 2 (Ben, 9-10.11.2026)
 * "דירות חדשות לאכלוס מיידי" on the ONE page of the new-projects intent, above the catalog, next to every other project.
 * The rows are the immediate / near-occupancy rows of data/projects-market.json, each checked by hand on 9.11.2026 against the
 * developer's page or the developer's listing (docs/research/2026-11-09-new-projects-hub/ready-verify/). Headings use the words
 * of Google's page 1 for the sub-intent (Ashtrom: "דירות חדשות לאכלוס מיידי"; Yad2: "לאכלוס קרוב"); the body carries the forms
 * people type (autocomplete 9.11): דירות מוכנות מקבלן, לכניסה מיידית, פרויקטים מאוכלסים. Unknown facts are omitted, never announced. */
if ( ! function_exists( 'nadlan_ph_market_counts' ) ) {
	/** Projects on the market by stage, from the data file. */
	function nadlan_ph_market_counts() {
		$c = array( 'all' => 0, 'immediate' => 0, 'near_occupancy' => 0, 'construction' => 0, 'marketing' => 0, 'presale' => 0 );
		foreach ( nadlan_ph_market()['projects'] as $p ) { $c['all']++; $k = (string) ( $p['status'] ?? '' ); if ( isset( $c[ $k ] ) ) { $c[ $k ]++; } }
		return $c;
	}
}
if ( ! function_exists( 'nadlan_ph_region_rank' ) ) {
	/** Ben, 10.11.2026: the lists open on Tel Aviv, then the centre of the country, then everything else (the variety stays, lower). */
	function nadlan_ph_region_rank( $city ) {
		$r = array( 'tlv' => 0, 'dan' => 1, 'sharon' => 2, 'center' => 3, 'jlm' => 4, 'north' => 5, 'south' => 6, 'other' => 7 );
		return $r[ nadlan_ph_region( $city ) ] ?? 7;
	}
}
if ( ! function_exists( 'nadlan_ph_ready_rows' ) ) {
	/** Tel Aviv first, then the centre; inside each area immediate before near occupancy, priced rows first from the lowest price. */
	function nadlan_ph_ready_rows() {
		$rows = array();
		foreach ( nadlan_ph_market()['projects'] as $p ) { if ( in_array( (string) ( $p['status'] ?? '' ), array( 'immediate', 'near_occupancy' ), true ) ) { $rows[] = $p; } }
		usort( $rows, function ( $a, $b ) {
			$ra = nadlan_ph_region_rank( $a['city'] ?? '' ); $rb = nadlan_ph_region_rank( $b['city'] ?? '' );
			if ( $ra !== $rb ) { return $ra - $rb; }
			$sa = 'immediate' === $a['status'] ? 0 : 1; $sb = 'immediate' === $b['status'] ? 0 : 1;
			if ( $sa !== $sb ) { return $sa - $sb; }
			$pa = (int) ( $a['price_from'] ?? 0 ); $pb = (int) ( $b['price_from'] ?? 0 );
			if ( ! $pa !== ! $pb ) { return $pa ? -1 : 1; }
			return $pa - $pb;
		} );
		return $rows;
	}
}
if ( ! function_exists( 'nadlan_ph_checked_date' ) ) {
	function nadlan_ph_checked_date() {
		$m = nadlan_ph_market(); $d = (string) ( $m['ready_checked'] ?? ( $m['read'] ?? '' ) );
		return '' !== $d ? date_i18n( 'j.n.Y', strtotime( $d ) ) : '';
	}
}
if ( ! function_exists( 'nadlan_ph_answer_html' ) ) {
	/** The answer paragraph under the H1: what is on the market today, by stage, printed from the data. */
	function nadlan_ph_answer_html() {
		$c = nadlan_ph_market_counts(); if ( $c['all'] < 1 ) { return ''; }
		$parts = array();
		if ( $c['immediate'] )      { $parts[] = '<a href="#nlph-ready"><b>' . (int) $c['immediate'] . '</b> לאכלוס מיידי</a>'; }
		if ( $c['near_occupancy'] ) { $parts[] = '<b>' . (int) $c['near_occupancy'] . '</b> באכלוס קרוב'; }
		if ( $c['construction'] )   { $parts[] = '<b>' . (int) $c['construction'] . '</b> בבנייה'; }
		if ( $c['marketing'] )      { $parts[] = '<b>' . (int) $c['marketing'] . '</b> בשיווק'; }
		if ( $c['presale'] )        { $parts[] = '<b>' . (int) $c['presale'] . '</b> בפריסייל'; }
		$last = count( $parts ) > 1 ? array_pop( $parts ) : '';
		$d = nadlan_ph_checked_date();
		return '<p class="nldir-lead nldir-answer"><strong>' . number_format( (int) $c['all'] ) . '</strong> פרויקטים חדשים ודירות חדשות מקבלן למכירה עכשיו: '
			. implode( ', ', $parts ) . ( '' !== $last ? ' ו־' . $last : '' ) . '. ליד המחיר שפרסם היזם מוצג מחיר העסקאות בעיר לפי רשות המסים.'
			. ( '' !== $d ? ' <span class="nldir-asof">נבדק ב־' . esc_html( $d ) . '</span>' : '' ) . '</p>';
	}
}
if ( ! function_exists( 'nadlan_ph_ready_html' ) ) {
	function nadlan_ph_ready_html() {
		$rows = nadlan_ph_ready_rows(); if ( ! $rows ) { return ''; }
		$n_im = 0; $n_nr = 0; $cities = array();
		foreach ( $rows as $p ) {
			if ( 'immediate' === $p['status'] ) { $n_im++; } else { $n_nr++; }
			$ck = trim( str_replace( '-', ' ', (string) ( $p['city'] ?? '' ) ) ); if ( '' !== $ck ) { $cities[ $ck ] = ( $cities[ $ck ] ?? 0 ) + 1; }
		}
		arsort( $cities );
		$open = isset( $cities['תל אביב יפו'] ) ? 'תל אביב יפו' : ''; // the city the section opens on
		$date = nadlan_ph_checked_date();
		$cards = ''; $i = 0;
		foreach ( $rows as $p ) {
			$st    = (string) $p['status'];
			$city  = trim( str_replace( '-', ' ', (string) ( $p['city'] ?? '' ) ) );
			$place = trim( ( $p['neighbourhood'] ?? '' ) . ( ! empty( $p['neighbourhood'] ) && '' !== $city ? ', ' : '' ) . $city );
			$price = (int) ( $p['price_from'] ?? 0 );
			$dl    = trim( (string) ( $p['delivery'] ?? '' ) );
			/* a published month that has already passed is not shown next to "אכלוס קרוב" (the developer's page still calls it near): unknown is omitted */
			if ( 'near_occupancy' === $st && preg_match( '#^(\d{2})/(\d{4})$#', $dl, $dm ) && ( $dm[2] . '-' . $dm[1] ) < substr( (string) ( nadlan_ph_market()['ready_checked'] ?? gmdate( 'Y-m-d' ) ), 0, 7 ) ) { $dl = ''; }
			$badge = 'immediate' === $st ? ( '' !== $dl ? $dl : 'אכלוס מיידי' ) : 'אכלוס קרוב' . ( '' !== $dl ? ' · ' . $dl : '' );
			preg_match_all( '/\d+(?:\.\d)?/', (string) ( $p['rooms'] ?? '' ), $rm );
			$rmin = $rm[0] ? min( array_map( 'floatval', $rm[0] ) ) : 0; $rmax = $rm[0] ? max( array_map( 'floatval', $rm[0] ) ) : 0;
			$name = esc_html( $p['name'] ?? '' );
			if ( ! empty( $p['url'] ) ) { $name = '<a href="' . esc_url( home_url( $p['url'] ) ) . '">' . $name . '</a>'; }
			$ctx = '';
			if ( function_exists( 'nadlan_cp_city_data' ) ) {
				$row = nadlan_cp_city_data( $city );
				if ( $row && ! empty( $row['psqm_all'] ) ) { $ctx = 'מחיר למ"ר ב' . esc_html( $row['key'] ?? $city ) . ' לפי עסקאות: <b>' . esc_html( nadlan_ph_nis( $row['psqm_all'] ) ) . '</b>'; }
			}
			$src = '';
			$su  = (string) ( $p['src_url'] ?? '' ); $host = $su ? (string) wp_parse_url( $su, PHP_URL_HOST ) : '';
			if ( '' !== $host && ! preg_match( '/yad2|madlan|nadlan\.com|bizportal|ynet|globes|calcalist/i', $host ) ) {
				$src = '<a href="' . esc_url( $su ) . '" target="_blank" rel="nofollow noopener">אתר היזם</a>';
			} elseif ( '' !== $host ) {
				$src = 'פרסום היזם';
			}
			$in = ( '' === $open || $city === $open );
			/* HAD-695 (10.11.2026): a project drawn in the picture series shows its picture (the drawing, 8:5) and the facts of its strip as
			 * text under it, per the approved canvas PhoneV2 + Fit. Rows without a picture keep the text card. */
			$pic = '';
			if ( ! empty( $p['img'] ) ) {
				$pic = '<div class="nlrd-pic"><img src="' . esc_url( (string) $p['img'] ) . '" width="960" height="600" alt="' . esc_attr( (string) ( $p['img_alt'] ?? $p['name'] ?? '' ) ) . '" loading="lazy" decoding="async"></div>';
				$chl = array_slice( array_filter( array_map( 'strval', (array) ( $p['chips'] ?? array() ) ) ), 0, 4 );
				if ( $chl ) { $pic .= '<ul class="nlrd-chips">'; foreach ( $chl as $c ) { $pic .= '<li>' . esc_html( $c ) . '</li>'; } $pic .= '</ul>'; }
			}
			$cards .= '<article class="nlrd-card' . ( $in ? ( $i >= 9 ? ' nlrd-more' : '' ) : ' is-off' ) . ( '' !== $pic ? ' has-pic' : '' ) . '" data-st="' . esc_attr( $st ) . '" data-city="' . esc_attr( $city ) . '" data-price="' . (int) $price . '" data-rmin="' . esc_attr( $rmin ) . '" data-rmax="' . esc_attr( $rmax ) . '">'
				. $pic
				. '<p class="nlrd-top"><span class="nlrd-badge nlrd-badge--' . esc_attr( $st ) . '">' . esc_html( $badge ) . '</span><span class="nlrd-place">' . esc_html( $place ) . '</span></p>'
				. '<h3>' . $name . '</h3>'
				. '<p class="nlrd-dev">' . esc_html( $p['developer'] ?? '' ) . ( ! empty( $p['rooms'] ) ? ' · ' . esc_html( $p['rooms'] ) . ' חדרים' : '' ) . '</p>'
				. ( $price ? '<p class="nlrd-price"><span>החל מ</span> <b>' . esc_html( nadlan_ph_nis( $price ) ) . '</b>' . ( ! empty( $p['price_note'] ) ? ' <small>' . esc_html( $p['price_note'] ) . '</small>' : '' ) . '</p>' : '' )
				. ( ! empty( $p['deal'] ) ? '<p class="nlrd-deal">תנאים שפרסם היזם: ' . esc_html( $p['deal'] ) . '</p>' : '' )
				. ( '' !== $ctx ? '<p class="nlrd-ctx">' . $ctx . '</p>' : '' )
				. ( '' !== $src || '' !== $date ? '<p class="nlrd-src">' . ( '' !== $date ? 'נבדק ב־' . esc_html( $date ) : '' ) . ( '' !== $src ? ( '' !== $date ? ' · ' : '' ) . $src : '' ) . '</p>' : '' )
				. '</article>';
			if ( $in ) { $i++; }
		}
		$copt = '<option value="">כל הארץ (' . count( $cities ) . ' ערים)</option>';
		foreach ( $cities as $ck => $n ) { $copt .= '<option value="' . esc_attr( $ck ) . '"' . ( $ck === $open ? ' selected' : '' ) . '>' . esc_html( $ck ) . ' (' . (int) $n . ')</option>'; }
		$total = count( $rows ); $shown = '' !== $open ? (int) $cities[ $open ] : $total;
		ob_start(); ?>
<section class="nlph-sec nlrd" id="nlph-ready" aria-labelledby="nlph-ready-h">
	<p class="nlph-kick">דירות מוכנות מקבלן<?php echo $date ? ' · נבדק מול פרסומי היזמים ב־' . esc_html( $date ) : ''; ?></p>
	<h2 id="nlph-ready-h">דירות חדשות לאכלוס מיידי: <?php echo (int) $n_im; ?> פרויקטים<?php echo $n_nr ? ', ועוד ' . (int) $n_nr . ' לאכלוס קרוב' : ''; ?></h2>
	<p class="nlph-lede">דירות חדשות מקבלן שאפשר להיכנס אליהן עכשיו או בקרוב, ב־<?php echo count( $cities ); ?> ערים: דירות מוכנות לכניסה מיידית בפרויקטים מאוכלסים, ודירות לקראת מסירה. דירה גמורה רואים בעיניים לפני החתימה, נכנסים אליה בלי שנים של המתנה, ומשלמים בלי הצמדה ארוכה למדד תשומות הבנייה. לכל פרויקט: היזם, החדרים, המחיר שהיזם פרסם ומועד המסירה.</p>
	<div class="nlph-tools">
		<div class="nlph-chips" role="group" aria-label="מתי נכנסים">
			<button type="button" class="is-on" data-st="">הכל <i><?php echo (int) $total; ?></i></button>
			<button type="button" data-st="immediate">לאכלוס מיידי <i><?php echo (int) $n_im; ?></i></button>
			<?php if ( $n_nr ) : ?><button type="button" data-st="near_occupancy">אכלוס קרוב <i><?php echo (int) $n_nr; ?></i></button><?php endif; ?>
		</div>
		<div class="nlph-sel">
			<label>עיר <select data-f="city"><?php echo $copt; // phpcs:ignore ?></select></label>
			<label>מחיר <select data-f="max"><option value="">כל המחירים</option><option value="2000000">עד 2 מיליון ₪</option><option value="3000000">עד 3 מיליון ₪</option><option value="4000000">עד 4 מיליון ₪</option><option value="5000000">עד 5 מיליון ₪</option></select></label>
			<label>חדרים <select data-f="rooms"><option value="">הכל</option><option value="3">3 חדרים</option><option value="4">4 חדרים</option><option value="5">5 חדרים ומעלה</option></select></label>
		</div>
	</div>
	<div class="nlrd-grid"><?php echo $cards; // phpcs:ignore ?></div>
	<p class="nlph-empty nlrd-empty" hidden>אין פרויקט שמתאים לסינון הזה. נסו עיר אחרת או טווח מחירים רחב יותר.</p>
	<?php if ( $shown > 9 ) : ?><button type="button" class="nlph-btn nlph-btn--ghost" id="nlrd-all">הצגת כל <?php echo (int) $shown; ?> הפרויקטים<?php echo '' !== $open ? ' ב' . esc_html( $open ) : ''; ?></button><?php endif; ?>
	<?php if ( '' !== $open ) : ?><button type="button" class="nlph-btn nlph-btn--ghost" id="nlrd-land">כל הארץ: <?php echo (int) $total; ?> פרויקטים לאכלוס מיידי וקרוב</button><?php endif; ?>
	<p class="nlph-src">המחירים, החדרים, התנאים ומועדי המסירה כפי שפרסמו היזמים<?php echo $date ? ', נבדקו אחד אחד ב־' . esc_html( $date ) : ''; ?>. פרויקט שפורסם כ"אכלוס מיידי" ומועד המסירה שפורסם לו עוד לא הגיע מופיע כאן כאכלוס קרוב. מחיר למ"ר בעיר: עסקאות שדווחו לרשות המסים. מה שלא פורסם לא מופיע. גם בדירה גמורה חלים חוק המכר, תקופות הבדק והאחריות: <a href="#nlph-checks">מה בודקים לפני שחותמים</a>.</p>
</section>
		<?php
		return ob_get_clean();
	}
}
if ( ! function_exists( 'nadlan_ph_top_wanted' ) ) {
	/** The top block (immediate occupancy + the marketing table, above the catalog) shows on the clean first page of the catalog.
	 *  A pure test of the request, so the template (inc/directory.php, which prints the block) and the body (built earlier by the
	 *  catalog snippet, which then skips the table and the CSS) always agree, whatever the order they run in. */
	function nadlan_ph_top_wanted() {
		static $w = null; if ( null !== $w ) { return $w; }
		if ( ! is_post_type_archive( 'nadlan_project' ) ) { return $w = false; }
		if ( ! NADLAN_PH_READY_LIVE && '1' !== (string) ( $_GET['nlready'] ?? '' ) ) { return $w = false; }
		if ( max( (int) get_query_var( 'paged' ), (int) ( $_GET['paged'] ?? 0 ) ) > 1 ) { return $w = false; }
		foreach ( array( 'city', 'q', 'project_type', 'status' ) as $k ) { if ( ! empty( $_GET[ $k ] ) ) { return $w = false; } }
		return $w = ! empty( nadlan_ph_market()['projects'] );
	}
}
if ( ! function_exists( 'nadlan_ph_top_html' ) ) {
	/** Above the catalog, on the clean first page only: the page CSS, the immediate-occupancy section, the marketing table. Printed by inc/directory.php right after the hero. */
	function nadlan_ph_top_html() {
		if ( ! nadlan_ph_top_wanted() ) { return ''; }
		$ready = ''; $market = '';
		try { $ready = nadlan_ph_ready_html(); } catch ( \Throwable $e ) { $ready = ''; }
		try { $market = nadlan_ph_market_html(); } catch ( \Throwable $e ) { $market = ''; }
		$css = nadlan_ph_assets_part( 'css' );
		return $css . '<style id="nlrd-css">'
			. '.nlph--top{margin-top:18px}'
			. '.nlrd-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:12px;margin:14px 0}'
			. '.nlrd-card{border:1px solid var(--li);border-radius:6px;padding:14px;background:#fff;display:flex;flex-direction:column;gap:6px;min-width:0}'
			. '.nlrd-card.nlrd-more,.nlrd-card.is-off{display:none}.nlrd.is-all .nlrd-card.nlrd-more:not(.is-off){display:flex}'
			. '.nlrd-card p{margin:0!important;font-size:14.5px!important;line-height:1.5!important;max-width:none}'
			. '.nlrd-card h3{margin:0!important;font-size:18px!important}.nlrd-card h3 a{color:var(--ink);text-decoration:underline;text-underline-offset:3px}'
			. '.nlrd-top{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center}.nlrd-card.has-pic{padding-top:0;overflow:hidden}.nlrd-pic{margin:0 -14px 2px;aspect-ratio:8/5;background:#E3EEF2;overflow:hidden}.nlrd-pic img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 0}.nlrd-chips{list-style:none;margin:0!important;padding:0!important;display:flex;flex-wrap:wrap;gap:6px}.nlrd-chips li{margin:0!important;background:#E3EEF2;color:#0A3A4C;font:600 13px/1.2 "IBM Plex Sans Hebrew",Heebo,system-ui,sans-serif;padding:5px 10px;border-radius:6px}.nlrd-place{color:var(--mu);font-size:13px}'
			. '.nlrd-badge{font-weight:600;font-size:13px;padding:3px 9px;border-radius:6px;border:1px solid var(--li)}'
			. '.nlrd-badge--immediate{background:#E3F1E5;border-color:#4F9A5C;color:#1F5A2A}.nlrd-badge--near_occupancy{background:#FBF1C7;border-color:#D9B530;color:#4A3B00}'
			. '.nlrd-dev{color:#24323E}.nlrd-price span{color:var(--mu);font-size:13px}.nlrd-price b{font:600 19px "IBM Plex Mono",ui-monospace,monospace;color:var(--ink)}.nlrd-price small{color:var(--mu);font-size:12.5px}'
			. '.nlrd-deal{background:#FBF1C7;border-radius:6px;padding:6px 9px;color:#12202A}.nlrd-ctx{color:var(--mu);font-size:13.5px!important}.nlrd-ctx b{color:var(--ink);font-variant-numeric:tabular-nums}'
			. '.nlrd-src{margin-top:auto!important;padding-top:6px;border-top:1px dashed var(--li);color:var(--mu);font-size:12.5px!important}'
			. '.nldir-answer b{font-variant-numeric:tabular-nums}.nldir-asof{white-space:nowrap;font-size:.85em;opacity:.8}'
			. '@media(max-width:640px){.nlrd-grid{grid-template-columns:1fr}}'
			. '</style>'
			. '<div class="nlph nlph--top" dir="rtl">' . $ready . $market . '</div>'
			. '<script id="nlrd-js">(function(){var s=document.getElementById("nlph-ready");if(!s)return;var cards=[].slice.call(s.querySelectorAll(".nlrd-card")),chips=[].slice.call(s.querySelectorAll(".nlph-chips button")),all=document.getElementById("nlrd-all"),empty=s.querySelector(".nlrd-empty"),st="";'
			. 'function v(k){var e=s.querySelector("[data-f="+k+"]");return e?e.value:"";}'
			. 'function f(){var c=v("city"),mx=+v("max")||0,r=+v("rooms")||0,n=0;cards.forEach(function(a){var p=+a.dataset.price,lo=+a.dataset.rmin,hi=+a.dataset.rmax;'
			. 'var ok=(!st||a.dataset.st===st)&&(!c||a.dataset.city===c)&&(!mx||(p&&p<=mx))&&(!r||(hi&&(r>=5?hi>=5:(lo<=r&&hi>=r))));a.classList.toggle("is-off",!ok);if(ok)n++;});'
			. 'if(st||c||mx||r)s.classList.add("is-all");if(empty)empty.hidden=n>0;if(all)all.hidden=s.classList.contains("is-all");}'
			. 'chips.forEach(function(b){b.addEventListener("click",function(){st=b.dataset.st;chips.forEach(function(x){x.classList.toggle("is-on",x===b);});f();});});'
			. '[].slice.call(s.querySelectorAll("select")).forEach(function(e){e.addEventListener("change",f);});'
			. 'if(all)all.addEventListener("click",function(){s.classList.add("is-all");all.hidden=true;});'
			. 'var land=document.getElementById("nlrd-land");if(land)land.addEventListener("click",function(){var c=s.querySelector("[data-f=city]");c.value="";s.classList.add("is-all");f();land.hidden=true;});'
			/* the catalog search sits above these sections: after the visitor searches or filters the catalog, bring its results into view */
			. 'var hero=document.querySelector(".nldir-hero"),res=document.getElementById("nldir-results"),want=0;'
			. 'if(hero&&res&&window.MutationObserver){["submit","change"].forEach(function(t){hero.addEventListener(t,function(){want=1;},true);});hero.addEventListener("click",function(e){if(e.target.closest&&e.target.closest(".nldir-pill,button[type=submit],.nlcp-go"))want=1;},true);'
			. 'new MutationObserver(function(){if(!want)return;want=0;var m=document.querySelector(".nldir-main");if(m&&m.getBoundingClientRect().top>window.innerHeight*0.6)m.scrollIntoView({behavior:"smooth",block:"start"});}).observe(res,{childList:true});}'
			. '})();</script>';
	}
}

/* ------------------------------------------------------------------------------------------------ the body after the grid */
if ( ! function_exists( 'nadlan_ph_rows_compact' ) ) {
	/** HAD-697: a short list of market rows (Tel Aviv and the centre first, then by price), each a line a buyer can scan. */
	function nadlan_ph_rows_compact( $rows, $limit = 10 ) {
		$st = array( 'presale' => 'פריסייל', 'marketing' => 'בשיווק', 'construction' => 'בבנייה', 'near_occupancy' => 'אכלוס קרוב', 'immediate' => 'אכלוס מיידי' );
		foreach ( $rows as $k => $p ) { $rows[ $k ]['_o'] = $k; }
		usort( $rows, function ( $a, $b ) {
			$ra = nadlan_ph_region_rank( $a['city'] ?? '' ); $rb = nadlan_ph_region_rank( $b['city'] ?? '' );
			if ( $ra !== $rb ) { return $ra - $rb; }
			$pa = (int) ( $a['price_from'] ?? 0 ); $pb = (int) ( $b['price_from'] ?? 0 );
			if ( ! $pa !== ! $pb ) { return $pa ? -1 : 1; }
			return $pa !== $pb ? $pa - $pb : $a['_o'] - $b['_o'];
		} );
		$li = '';
		foreach ( array_slice( $rows, 0, $limit ) as $p ) {
			$name = esc_html( $p['name'] ?? '' );
			if ( ! empty( $p['url'] ) ) { $name = '<a href="' . esc_url( home_url( $p['url'] ) ) . '">' . $name . '</a>'; }
			$city  = trim( str_replace( '-', ' ', (string) ( $p['city'] ?? '' ) ) );
			$place = trim( ( $p['neighbourhood'] ?? '' ) . ( ! empty( $p['neighbourhood'] ) && '' !== $city ? ', ' : '' ) . $city );
			$price = (int) ( $p['price_from'] ?? 0 );
			$li .= '<li><b>' . $name . '</b> <span>' . esc_html( $place ) . ( ! empty( $p['developer'] ) ? ' · ' . esc_html( $p['developer'] ) : '' ) . '</span>'
				. ( $price ? ' <em>החל מ־' . esc_html( nadlan_ph_nis( $price ) ) . '</em>' : '' )
				. ( isset( $st[ (string) ( $p['status'] ?? '' ) ] ) ? ' <i>' . esc_html( $st[ (string) $p['status'] ] ) . '</i>' : '' ) . '</li>';
		}
		return '' !== $li ? '<ul class="nlph-cl">' . $li . '</ul>' : '';
	}
}
if ( ! function_exists( 'nadlan_ph_city_min' ) ) {
	/** HAD-697: the cities of a set of rows with their count and lowest published price, Tel Aviv and the centre first. */
	function nadlan_ph_city_min( $rows, $limit = 8 ) {
		$c = array();
		foreach ( $rows as $p ) {
			$k = trim( str_replace( '-', ' ', (string) ( $p['city'] ?? '' ) ) ); if ( '' === $k ) { continue; }
			if ( ! isset( $c[ $k ] ) ) { $c[ $k ] = array( 'n' => 0, 'min' => 0 ); }
			$c[ $k ]['n']++;
			$pr = (int) ( $p['price_from'] ?? 0 );
			if ( $pr && ( ! $c[ $k ]['min'] || $pr < $c[ $k ]['min'] ) ) { $c[ $k ]['min'] = $pr; }
		}
		uksort( $c, function ( $a, $b ) use ( $c ) { $ra = nadlan_ph_region_rank( $a ); $rb = nadlan_ph_region_rank( $b ); return $ra !== $rb ? $ra - $rb : $c[ $b ]['n'] - $c[ $a ]['n']; } );
		$li = '';
		foreach ( array_slice( $c, 0, $limit, true ) as $k => $v ) {
			$li .= '<li><b>' . esc_html( $k ) . '</b> ' . (int) $v['n'] . ( 1 === $v['n'] ? ' פרויקט' : ' פרויקטים' ) . ( $v['min'] ? ', החל מ־' . esc_html( nadlan_ph_nis( $v['min'] ) ) : '' ) . '</li>';
		}
		return '' !== $li ? '<ul class="nlph-cm">' . $li . '</ul>' : '';
	}
}
if ( ! function_exists( 'nadlan_ph_budget_html' ) ) {
	/** HAD-697 (Google's budget ladder, needs-matrix row 2): "דירות חדשות עד 1.2 מיליון" is about 320 searches a month, close to the head,
	 * and no list page anywhere answers it exactly. One panel per rung in Google's own spelling, each in the shape of Google's AI box:
	 * one honest sentence with a number and a date, the cities with their "החל מ" price, then the projects. All panels are in the HTML. */
	function nadlan_ph_budget_html() {
		$m = nadlan_ph_market(); $rows = (array) $m['projects'];
		$priced = array_values( array_filter( $rows, function ( $p ) { return (int) ( $p['price_from'] ?? 0 ) > 0; } ) );
		if ( ! $priced ) { return ''; }
		usort( $priced, function ( $a, $b ) { return (int) $a['price_from'] - (int) $b['price_from']; } );
		$cheap = $priced[0]; $P = count( $priced );
		$date  = ! empty( $m['read'] ) ? date_i18n( 'j.n.Y', strtotime( $m['read'] ) ) : '';
		$rungs = array( 1000000 => 'עד מיליון', 1200000 => 'עד 1.2 מיליון', 1500000 => 'עד 1.5 מיליון', 2000000 => 'עד 2 מיליון', 2500000 => 'עד 2.5 מיליון', 3000000 => 'עד 3 מיליון' );
		$open  = 1200000; $tabs = ''; $panels = '';
		$cplace = function ( $p ) { $c = trim( str_replace( '-', ' ', (string) ( $p['city'] ?? '' ) ) ); $h = trim( (string) ( $p['neighbourhood'] ?? '' ) ); return ( '' !== $h && false === mb_strpos( (string) ( $p['name'] ?? '' ), $h ) ? $h . ', ' : '' ) . $c; };
		foreach ( $rungs as $max => $label ) {
			$in = array_values( array_filter( $priced, function ( $p ) use ( $max ) { return (int) $p['price_from'] <= $max; } ) );
			$n  = count( $in ); $id = 'nlph-b' . (int) ( $max / 100000 );
			if ( $n ) {
				$tl = array_values( array_filter( $in, function ( $p ) { return 'tlv' === nadlan_ph_region( $p['city'] ?? '' ); } ) );
				$lead = ( '' !== $date ? 'נכון ל־' . $date . ', ' : '' ) . ( 1 === $n ? 'פרויקט חדש אחד מתוך ' . $P . ' שפרסמו מחיר מתחיל' : $n . ' מתוך ' . $P . ' הפרויקטים החדשים שפרסמו מחיר מתחילים' ) . ' ב־' . nadlan_ph_nis( $max ) . ' או פחות. '
					. ( $max <= 1500000 ? ( 1 === $n ? 'הוא: ' : 'הזול שבהם: ' ) . $in[0]['name'] . ', ' . $cplace( $in[0] ) . ', החל מ־' . nadlan_ph_nis( $in[0]['price_from'] ) . '.'
						: ( $tl ? 'בתל אביב: ' . ( 1 === count( $tl ) ? 'אחד מהם, ' : count( $tl ) . ' מהם, הזול ' ) . $tl[0]['name'] . ', ' . $cplace( $tl[0] ) . ', החל מ־' . nadlan_ph_nis( $tl[0]['price_from'] ) . '.' : 'בתל אביב אין עדיין פרויקט חדש שפרסם מחיר עד הסכום הזה; הקרובים ביותר ברשימה למטה.' ) );
			} else {
				$lead = ( '' !== $date ? 'נכון ל־' . $date . ', ' : '' ) . 'אף אחד מ־' . $P . ' הפרויקטים החדשים שפרסמו מחיר לא מתחיל ' . $label . ' ₪. המחיר הנמוך ביותר שפורסם: ' . $cheap['name'] . ', ' . $cplace( $cheap ) . ', החל מ־' . nadlan_ph_nis( $cheap['price_from'] ) . '.';
			}
			$on = $max === $open;
			$tabs .= '<button type="button" role="tab" id="' . $id . '-t" aria-controls="' . $id . '" aria-selected="' . ( $on ? 'true' : 'false' ) . '"' . ( $on ? '' : ' tabindex="-1"' ) . '>' . esc_html( $label ) . ' <i>' . $n . '</i></button>';
			$panels .= '<div class="nlph-bp" role="tabpanel" id="' . $id . '" aria-labelledby="' . $id . '-t"' . ( $on ? '' : ' hidden' ) . '>'
				. '<h3>דירות חדשות ' . esc_html( $label ) . '</h3>'
				. '<p class="nlph-ans">' . esc_html( $lead ) . '</p>'
				. ( $n ? '<p class="nlph-mini">איפה:</p>' . nadlan_ph_city_min( $in ) . '<p class="nlph-mini">הפרויקטים, תל אביב והמרכז קודם:</p>' . nadlan_ph_rows_compact( $in, 10 )
					. '<button type="button" class="nlph-btn nlph-btn--ghost" data-nlph-go="max" data-v="' . (int) $max . '">כל ' . $n . ' הפרויקטים ' . esc_html( $label ) . ' בטבלה</button>' : '' )
				. '</div>';
		}
		ob_start(); ?>
<section class="nlph-sec" id="nlph-budget" aria-labelledby="nlph-budget-h">
	<p class="nlph-kick">לפי תקציב · מחירים שפרסמו היזמים</p>
	<h2 id="nlph-budget-h">דירות חדשות עד 1.2 מיליון, עד 1.5 מיליון ועד 3 מיליון</h2>
	<p class="nlph-lede">מה התקציב שלי קונה: בוחרים סכום ורואים כמה פרויקטים חדשים מתחילים בו, באילו ערים ומה הזול בכל עיר. המחיר הוא מחיר "החל מ" שהיזם פרסם, כלומר הדירה הזולה בפרויקט באותו יום; דירה גדולה יותר עולה יותר. <?php echo (int) ( count( $rows ) - $P ); ?> פרויקטים נוספים לא פרסמו מחיר ולכן לא נספרים כאן.</p>
	<div class="nlph-btabs" role="tablist" aria-label="תקציב"><?php echo $tabs; // phpcs:ignore ?></div>
	<?php echo $panels; // phpcs:ignore ?>
	<style>.nlph-btabs{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;margin:12px 0}.nlph-btabs::-webkit-scrollbar{display:none}.nlph-btabs button{flex:0 0 auto;font:500 14.5px "IBM Plex Sans Hebrew",sans-serif!important;border:1px solid #C9D3DA!important;background:#fff!important;color:#0F1D26!important;border-radius:22px!important;padding:0 14px!important;min-height:44px;cursor:pointer;box-shadow:none!important}.nlph-btabs button i{font-style:normal;color:#5B6975;margin-inline-start:4px}.nlph-btabs button[aria-selected="true"]{background:#0E4C63!important;border-color:#0E4C63!important;color:#fff!important}.nlph-btabs button[aria-selected="true"] i{color:#D6E8EE}.nlph-bp h3,.nlph-stb h3{font-size:19px!important;margin:6px 0!important}.nlph-ans{font-size:16px!important;line-height:1.6!important;color:#0F1D26!important;margin:0 0 8px!important}.nlph-mini{font-size:13px!important;color:#5B6975!important;margin:10px 0 4px!important}.nlph-cm,.nlph-cl{list-style:none;margin:0 0 10px!important;padding:0!important}.nlph-cm{display:flex;flex-wrap:wrap;gap:6px}.nlph-cm li{margin:0!important;background:#E3EEF2;color:#0A3A4C;border-radius:6px;padding:6px 10px;font-size:14px}.nlph-cl li{margin:0!important;padding:8px 0;border-bottom:1px solid #E3E8EC;font-size:14.5px;line-height:1.5}.nlph-cl li span{color:#3B4A56}.nlph-cl li em{font-style:normal;font-family:"IBM Plex Mono",monospace;font-weight:600;color:#0F1D26;white-space:nowrap}.nlph-cl li i{font-style:normal;font-size:12.5px;background:#ECEAF6;color:#2B2A72;border-radius:4px;padding:2px 6px;margin-inline-start:4px}.nlph-stb{margin:18px 0 0}</style>
	<script>(function(){var s=document.getElementById("nlph-budget");if(!s)return;var t=[].slice.call(s.querySelectorAll(".nlph-btabs [role=tab]"));t.forEach(function(b,i){b.addEventListener("click",function(){t.forEach(function(x){var on=x===b;x.setAttribute("aria-selected",on?"true":"false");x.tabIndex=on?0:-1;var p=document.getElementById(x.getAttribute("aria-controls"));if(p)p.hidden=!on;});});b.addEventListener("keydown",function(e){var j=-1;if(e.key==="ArrowLeft")j=(i+1)%t.length;if(e.key==="ArrowRight")j=(i-1+t.length)%t.length;if(j>-1){e.preventDefault();t[j].focus();t[j].click();}});});
	document.addEventListener("click",function(e){var g=e.target.closest&&e.target.closest("[data-nlph-go]");if(!g)return;var m=document.getElementById("nlph-market");if(!m)return;var sel=m.querySelector("select[data-f="+g.getAttribute("data-nlph-go")+"]");if(!sel)return;sel.value=g.getAttribute("data-v");sel.dispatchEvent(new Event("change",{bubbles:true}));m.scrollIntoView({behavior:"smooth",block:"start"});});})();</script>
</section>
		<?php
		return ob_get_clean();
	}
}
if ( ! function_exists( 'nadlan_ph_stages_html' ) ) {
	/** HAD-697 (needs-matrix rows 3 and 4): "פרויקטים חדשים על הנייר" (6 of 8 results shared with the head), "פריסייל תל אביב",
	 * "פרויקטים חדשים בשיווק" and "פרויקטים בבנייה". Counts from the market rows, Tel Aviv first; the explanations stay short and general. */
	function nadlan_ph_stages_html() {
		$m = nadlan_ph_market(); $rows = (array) $m['projects']; if ( ! $rows ) { return ''; }
		$date = ! empty( $m['read'] ) ? date_i18n( 'j.n.Y', strtotime( $m['read'] ) ) : '';
		$def = array(
			'presale'        => array( 'פריסייל', 'מכירה מוקדמת, לפני השיווק הרגיל של הפרויקט. ההמתנה למפתח היא הארוכה ביותר.', 'presale' ),
			'marketing'      => array( 'בשיווק', 'היזם מוכר דירות לפי מחירון ולוח תשלומים. המסירה בדרך כלל בעוד כמה שנים.', 'marketing' ),
			'construction'   => array( 'בבנייה', 'הבניין כבר נבנה, ואפשר לראות את ההתקדמות באתר.', 'construction' ),
			'near_occupancy' => array( 'אכלוס קרוב', 'המסירה קרובה, לפי מה שפרסם היזם.', 'near' ),
			'immediate'      => array( 'לאכלוס מיידי', 'הדירה גמורה, ואפשר לקבל מפתח זמן קצר אחרי החתימה.', 'near' ),
		);
		$by = array(); foreach ( $rows as $p ) { $by[ (string) ( $p['status'] ?? '' ) ][] = $p; }
		$paper = count( $by['presale'] ?? array() ) + count( $by['marketing'] ?? array() ) + count( $by['construction'] ?? array() );
		$tr = ''; $blocks = '';
		foreach ( $def as $k => $d ) {
			$set = $by[ $k ] ?? array(); if ( ! $set ) { continue; }
			$tlv = 0; $min = null;
			foreach ( $set as $p ) { if ( 'tlv' === nadlan_ph_region( $p['city'] ?? '' ) ) { $tlv++; } $pr = (int) ( $p['price_from'] ?? 0 ); if ( $pr && ( null === $min || $pr < (int) $min['price_from'] ) ) { $min = $p; } }
			$tr .= '<tr><th scope="row">' . esc_html( $d[0] ) . '</th><td data-l="פרויקטים">' . count( $set ) . '</td><td data-l="בתל אביב">' . $tlv . '</td>'
				. '<td data-l="המחיר הנמוך שפורסם">' . ( $min ? esc_html( nadlan_ph_nis( $min['price_from'] ) ) . '<small>' . esc_html( trim( str_replace( '-', ' ', (string) $min['city'] ) ) ) . '</small>' : '<span class="nlph-na">לא פורסם</span>' ) . '</td>'
				. '<td data-l="מה זה אומר">' . esc_html( $d[1] ) . '</td></tr>';
			if ( in_array( $k, array( 'presale', 'marketing', 'construction' ), true ) ) {
				$blocks .= '<div class="nlph-stb"><h3>' . esc_html( 'presale' === $k ? 'פריסייל בתל אביב ובכל הארץ' : ( 'marketing' === $k ? 'פרויקטים חדשים בשיווק' : 'פרויקטים בבנייה' ) ) . '</h3>'
					. '<p class="nlph-ans">' . esc_html( ( '' !== $date ? 'נכון ל־' . $date . ', ' : '' ) . count( $set ) . ' פרויקטים ' . ( 'presale' === $k ? 'בפריסייל' : ( 'marketing' === $k ? 'בשיווק' : 'בבנייה' ) ) . ', ' . $tlv . ' מהם בתל אביב' . ( $min ? '. המחיר הנמוך שפורסם: ' . $min['name'] . ', ' . trim( str_replace( '-', ' ', (string) $min['city'] ) ) . ', החל מ־' . nadlan_ph_nis( $min['price_from'] ) : '' ) . '.' ) . '</p>'
					. nadlan_ph_rows_compact( $set, 6 )
					. '<button type="button" class="nlph-btn nlph-btn--ghost" data-nlph-go="st" data-v="' . esc_attr( $d[2] ) . '">כל ' . count( $set ) . ' הפרויקטים ' . esc_html( 'presale' === $k ? 'בפריסייל' : $d[0] ) . ' בטבלה</button></div>';
			}
		}
		ob_start(); ?>
<section class="nlph-sec" id="nlph-stages" aria-labelledby="nlph-stages-h">
	<p class="nlph-kick">לפי שלב · מהנייר ועד המפתח</p>
	<h2 id="nlph-stages-h">פרויקטים חדשים על הנייר, בפריסייל ובבנייה</h2>
	<p class="nlph-lede"><?php echo esc_html( ( '' !== $date ? 'נכון ל־' . $date . ', ' : '' ) . $paper . ' פרויקטים חדשים עדיין לא הושלמו: ' . count( $by['presale'] ?? array() ) . ' בפריסייל, ' . count( $by['marketing'] ?? array() ) . ' בשיווק ו־' . count( $by['construction'] ?? array() ) . ' בבנייה (גם "בבניה"). דירה על הנייר נקנית לפני שהבניין גמור, וההמתנה למפתח ארוכה יותר. כך נראה כל שלב היום:' ); ?></p>
	<div class="nlph-tw"><table class="nlph-pt nlph-stt">
		<thead><tr><th scope="col">שלב</th><th scope="col">פרויקטים</th><th scope="col">בתל אביב</th><th scope="col">המחיר הנמוך שפורסם</th><th scope="col">מה זה אומר לקונה</th></tr></thead>
		<tbody><?php echo $tr; // phpcs:ignore ?></tbody>
	</table></div>
	<?php echo $blocks; // phpcs:ignore ?>
	<p class="nlph-src">איך משלמים בכל שלב, ומה המשמעות של מבצעי 20/80 והלוואת קבלן: <a href="<?php echo esc_url( home_url( '/developer-deals/' ) ); ?>">המדריך למבצעי קבלנים</a>.</p>
</section>
		<?php
		return ob_get_clean();
	}
}
if ( ! function_exists( 'nadlan_ph_devs_html' ) ) {
	/** HAD-697/698 ("מי בונה מה", needs-matrix row 10: Google's AI box for the head phrase is organised by developer): every developer
	 * with projects on the market list, how many, where, from what published price and at which stages. Counts only, no ranking words. */
	function nadlan_ph_devs_html() {
		$m = nadlan_ph_market(); $rows = (array) $m['projects']; if ( ! $rows ) { return ''; }
		$st = array( 'presale' => 'פריסייל', 'marketing' => 'בשיווק', 'construction' => 'בבנייה', 'near_occupancy' => 'אכלוס קרוב', 'immediate' => 'אכלוס מיידי' );
		$d = array();
		foreach ( $rows as $p ) {
			$k = trim( (string) ( $p['developer'] ?? '' ) ); if ( '' === $k ) { continue; }
			if ( ! isset( $d[ $k ] ) ) { $d[ $k ] = array( 'n' => 0, 'tlv' => 0, 'c' => array(), 'min' => 0, 's' => array() ); }
			$d[ $k ]['n']++;
			$c = trim( str_replace( '-', ' ', (string) ( $p['city'] ?? '' ) ) ); if ( '' !== $c ) { $d[ $k ]['c'][ $c ] = ( $d[ $k ]['c'][ $c ] ?? 0 ) + 1; }
			if ( 'tlv' === nadlan_ph_region( $p['city'] ?? '' ) ) { $d[ $k ]['tlv']++; }
			$pr = (int) ( $p['price_from'] ?? 0 ); if ( $pr && ( ! $d[ $k ]['min'] || $pr < $d[ $k ]['min'] ) ) { $d[ $k ]['min'] = $pr; }
			$s = (string) ( $p['status'] ?? '' ); if ( isset( $st[ $s ] ) ) { $d[ $k ]['s'][ $s ] = ( $d[ $k ]['s'][ $s ] ?? 0 ) + 1; }
		}
		uksort( $d, function ( $a, $b ) use ( $d ) { return $d[ $b ]['n'] !== $d[ $a ]['n'] ? $d[ $b ]['n'] - $d[ $a ]['n'] : ( $d[ $b ]['tlv'] - $d[ $a ]['tlv'] ?: strcmp( $a, $b ) ); } );
		$tr = ''; $i = 0; $date = ! empty( $m['read'] ) ? date_i18n( 'j.n.Y', strtotime( $m['read'] ) ) : '';
		$ones = array();
		foreach ( $d as $k => $v ) {
			if ( 1 === $v['n'] ) { $ones[] = $k . ' (' . implode( '', array_keys( $v['c'] ) ) . ')'; continue; }
			arsort( $v['c'] ); $cities = array_slice( array_keys( $v['c'] ), 0, 3 );
			$ss = array(); foreach ( $st as $sk => $sl ) { if ( ! empty( $v['s'][ $sk ] ) ) { $ss[] = $sl . ' ' . (int) $v['s'][ $sk ]; } }
			$tr .= '<tr' . ( $i >= 20 ? ' class="nlph-more"' : '' ) . '><th scope="row">' . esc_html( $k ) . '</th><td data-l="פרויקטים">' . (int) $v['n'] . '</td><td data-l="בתל אביב">' . (int) $v['tlv'] . '</td>'
				. '<td data-l="ערים">' . esc_html( implode( ', ', $cities ) . ( count( $v['c'] ) > 3 ? ' ועוד ' . ( count( $v['c'] ) - 3 ) : '' ) ) . '</td>'
				. '<td data-l="החל מ">' . ( $v['min'] ? esc_html( nadlan_ph_nis( $v['min'] ) ) : '<span class="nlph-na">לא פורסם</span>' ) . '</td>'
				. '<td data-l="שלבים">' . esc_html( implode( ' · ', $ss ) ) . '</td></tr>';
			$i++;
		}
		ob_start(); ?>
<section class="nlph-sec" id="nlph-devs" aria-labelledby="nlph-devs-h">
	<p class="nlph-kick">מי בונה מה · לפי פרסומי היזמים</p>
	<h2 id="nlph-devs-h">חברות בנייה ויזמות נדל״ן: מי בונה את הפרויקטים החדשים</h2>
	<p class="nlph-lede"><?php echo esc_html( ( '' !== $date ? 'נכון ל־' . $date . ', ' : '' ) . count( $d ) . ' חברות בנייה ויזמים משווקים ' . count( $rows ) . ' פרויקטים חדשים. לכל חברה: כמה פרויקטים, כמה מהם בתל אביב, באילו ערים, המחיר הנמוך שפרסמה ובאילו שלבים הם נמצאים. הסדר לפי מספר הפרויקטים בלבד.' ); ?></p>
	<div class="nlph-tw"><table class="nlph-pt nlph-devt"<?php echo $i > 20 ? ' data-all="0"' : ''; ?>>
		<thead><tr><th scope="col">חברה</th><th scope="col">פרויקטים</th><th scope="col">בתל אביב</th><th scope="col">ערים</th><th scope="col">החל מ</th><th scope="col">שלבים</th></tr></thead>
		<tbody><?php echo $tr; // phpcs:ignore ?></tbody>
	</table></div>
	<?php if ( $ones ) : ?><details class="nlph-ones"><summary>ועוד <?php echo count( $ones ); ?> חברות עם פרויקט חדש אחד</summary><p><?php echo esc_html( implode( ' · ', $ones ) ); ?></p></details><?php endif; ?>
	<?php if ( $i > 20 ) : ?><button type="button" class="nlph-btn nlph-btn--ghost" onclick="var t=this.previousElementSibling.querySelector('table');t.classList.add('is-all');this.hidden=true;">כל <?php echo (int) $i; ?> החברות</button><style>.nlph-devt tr.nlph-more{display:none}.nlph-devt.is-all tr.nlph-more{display:table-row}@media(max-width:640px){.nlph-devt.is-all tr.nlph-more{display:block}}</style><?php endif; ?>
</section>
		<?php
		return ob_get_clean();
	}
}
if ( ! function_exists( 'nadlan_ph_body' ) ) {
	function nadlan_ph_body( $facets ) {
		$out = '';
		/* /projects/page/2/ and on show the next cards (F1); the long sections stay on page 1. The FAQ stays on every page,
		 * because snippet 661 prints its FAQPage on every catalog page and the questions must be visible where they are marked. */
		if ( max( (int) get_query_var( 'paged' ), (int) ( $_GET['paged'] ?? 0 ) ) > 1 ) {
			return '<div class="nlph" dir="rtl">' . nadlan_ph_cities_html( $facets ) . nadlan_ph_guides_html() . nadlan_ph_faq_html() . '</div>' . nadlan_ph_assets();
		}
		foreach ( array(
			function () { return nadlan_ph_top_wanted() ? '' : nadlan_ph_market_html(); }, // HAD-689: on the clean first page the table sits above the catalog (nadlan_ph_top_html)
			function () use ( $facets ) { return nadlan_ph_tlv_html( $facets ); },
			function () { return function_exists( 'nadlan_ph_budget_html' ) ? nadlan_ph_budget_html() : ''; }, // HAD-697: Google's budget ladder
			function () { return function_exists( 'nadlan_ph_stages_html' ) ? nadlan_ph_stages_html() : ''; }, // HAD-697: the stages
			function () { return function_exists( 'nadlan_ph_devs_html' ) ? nadlan_ph_devs_html() : ''; }, // HAD-697: who builds what
			function () use ( $facets ) { return nadlan_ph_prices_html( $facets ); },
			function () use ( $facets ) { return nadlan_ph_catalog_html( $facets ); },
			function () { return nadlan_ph_timeline_html(); },
			function () { return nadlan_ph_pay_html(); },
			function () { return nadlan_ph_toolbox_html(); },
			function () { return nadlan_ph_checks_html(); },
			function () { return nadlan_ph_types_html(); },
			function () { return nadlan_ph_market_numbers_html(); },
			function () use ( $facets ) { return nadlan_ph_cities_html( $facets ); },
			function () { return nadlan_ph_guides_html(); },
			function () { return nadlan_ph_faq_html(); },
			function () { return nadlan_ph_sources_html(); },
		) as $part ) {
			try { $out .= $part(); } catch ( \Throwable $e ) { continue; } // one broken section never takes the page down
		}
		return '<div class="nlph" dir="rtl">' . $out . '</div>' . nadlan_ph_assets();
	}
}
if ( ! function_exists( 'nadlan_cp_body_html' ) ) {
	/** Snippet 661 injects this right after the catalog grid. */
	function nadlan_cp_body_html( $facets ) { return nadlan_ph_body( $facets ); }
}

if ( ! function_exists( 'nadlan_ph_assets_part' ) ) {
	/** 'css' = the <style> of the hub, 'js' = its script. The top block prints the CSS early (HAD-689), so nothing above the catalog shows unstyled. */
	function nadlan_ph_assets_part( $which ) {
		$a = nadlan_ph_assets_raw(); $p = strpos( $a, '</style>' );
		if ( false === $p ) { return 'css' === $which ? '' : $a; }
		$p += 8;
		return 'css' === $which ? substr( $a, 0, $p ) : substr( $a, $p );
	}
}
if ( ! function_exists( 'nadlan_ph_assets' ) ) {
	function nadlan_ph_assets() { return nadlan_ph_top_wanted() ? nadlan_ph_assets_part( 'js' ) : nadlan_ph_assets_raw(); }
}
if ( ! function_exists( 'nadlan_ph_assets_raw' ) ) {
	function nadlan_ph_assets_raw() {
		return '<style id="nlph-css">'
			. '.nlph{--ink:#14213D;--tx:#12202A;--mu:#4A5866;--li:#D3DCE2;--bg:#F4F6FA;--ac:#1F4B5C;--ac2:#2F6F86;--ok:#0F7A63;--warn:#9A5B00;'
			. 'max-width:1240px;margin:28px auto 0;padding:0 max(16px,env(safe-area-inset-left,0px));font-family:"IBM Plex Sans Hebrew",Heebo,system-ui,sans-serif;color:var(--tx)}'
			. '.nlph-sec{background:#fff;border:1px solid var(--li);border-radius:8px;padding:22px clamp(16px,3vw,32px);margin:0 0 18px}'
			. '.nlph-kick{font:500 12px/16px "IBM Plex Mono",ui-monospace,monospace;color:var(--mu);letter-spacing:.02em;margin:0 0 4px}'
			. '.nlph h2{font:700 clamp(22px,2.6vw,28px)/1.25 "IBM Plex Sans Hebrew",Heebo,sans-serif;color:var(--ink)!important;margin:0 0 10px;text-wrap:balance}'
			. '.nlph h3{font:600 18px/1.35 "IBM Plex Sans Hebrew",Heebo,sans-serif;color:var(--ink)!important;margin:18px 0 8px}'
			. '.nlph p{font-size:16px;line-height:1.7;margin:0 0 12px;max-width:78ch}.nlph a{color:var(--ac2)}'
			. '.nlph-lede{font-size:17px!important;color:#24323E}'
			. '.nlph-src{font-size:13px!important;color:var(--mu);line-height:1.6!important;margin-top:10px!important}'
			. '.nlph-tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:10px 0}'
			. '.nlph table{width:100%;border-collapse:collapse;font-size:15px}.nlph th,.nlph td{padding:10px 10px;border-bottom:1px solid var(--li);text-align:right;vertical-align:top}'
			. '.nlph thead th{font:600 13px/1.3 "IBM Plex Sans Hebrew",sans-serif;color:var(--mu);background:var(--bg);white-space:nowrap}'
			. '.nlph tbody th{font-weight:600;color:var(--ink)}.nlph td small,.nlph th small{display:block;color:var(--mu);font-size:12.5px;font-weight:400;margin-top:2px}'
			. '.nlph-mt .nlph-p b{font-family:"IBM Plex Mono",monospace;font-weight:600;color:var(--ink)}.nlph-na{color:var(--mu);font-size:13px}'
			. '.nlph-st{display:inline-block;font-size:12.5px;padding:2px 8px;border-radius:999px;background:var(--bg);border:1px solid var(--li)}'
			. '.nlph-st--presale{background:#EEF4FB;border-color:#B9CFE6}.nlph-st--near_occupancy,.nlph-st--immediate{background:#E9F5F0;border-color:#A9D5C2}'
			. '.nlph-tools{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between;margin:12px 0}'
			. '.nlph-chips{display:flex;flex-wrap:wrap;gap:6px}.nlph-chips button{font:500 14px "IBM Plex Sans Hebrew",sans-serif;border:1px solid var(--li);background:#fff;color:var(--tx);border-radius:999px;padding:7px 12px;min-height:40px;cursor:pointer}'
			. '.nlph-chips button i{font-style:normal;color:var(--mu);font-size:12px}.nlph-chips button.is-on{background:var(--ink);border-color:var(--ink);color:#fff}.nlph-chips button.is-on i{color:#C9D3E6}'
			. '.nlph-sel{display:flex;flex-wrap:wrap;gap:8px}.nlph-sel label{font-size:13px;color:var(--mu);display:flex;align-items:center;gap:6px}.nlph-sel select{font:500 14px "IBM Plex Sans Hebrew",sans-serif;border:1px solid var(--li);border-radius:6px;padding:7px 8px;min-height:40px;background:#fff;color:var(--tx)}'
			. '.nlph-mt tr.nlph-more,.nlph-mt tr.is-off{display:none!important}#nlph-market.is-busy .nlph-tw{opacity:.55}'
			. '.nlph-btn{font:600 15px "IBM Plex Sans Hebrew",sans-serif;border-radius:6px;padding:10px 18px;min-height:44px;cursor:pointer;border:1px solid var(--ink);background:var(--ink);color:#fff}'
			. '.nlph-btn--ghost{background:#fff;color:var(--ink)}'
			. '.nlph-stats,.nlph-tiles{list-style:none;padding:0;margin:14px 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}'
			. '.nlph-stats li,.nlph-tiles li{border:1px solid var(--li);border-radius:6px;padding:12px 14px;background:var(--bg)}'
			. '.nlph-stats b,.nlph-tiles b{display:block;font:600 24px/1.2 "IBM Plex Sans Hebrew",sans-serif;font-variant-numeric:tabular-nums;color:var(--ink);text-align:right}'
			. '.nlph-stats span,.nlph-tiles span{display:block;font-size:14px;line-height:1.45;margin-top:4px}.nlph-tiles small{display:block;color:var(--mu);font-size:12.5px;margin-top:6px}'
			. '.nlph-areas{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin:14px 0}'
			. '.nlph-area{border:1px solid var(--li);border-top:3px solid var(--ac);border-radius:6px;padding:14px}.nlph-area h3{margin:0 0 4px!important}'
			. '.nlph-area p{font-size:14.5px!important;line-height:1.6!important;margin:0 0 8px!important}.nlph-area__n{color:var(--mu)}.nlph-area__m b{font-family:"IBM Plex Mono",monospace}'
			. '.nlph-area__p{color:var(--mu)}.nlph-area__k{font:500 12px "IBM Plex Mono",monospace!important;color:var(--mu)}'
			. '.nlph-area__med{list-style:none;padding:0;margin:0 0 8px}.nlph-area__med li{display:flex;gap:8px;align-items:baseline;font-size:14px;padding:3px 0;border-bottom:1px dashed var(--li)}'
			. '.nlph-area__med span{flex:1}.nlph-area__med b{font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap}.nlph-area__med small{color:var(--mu);font-size:12px}'
			. '.nlph-area__l{display:flex;flex-wrap:wrap;gap:6px}.nlph-area__l a{font-size:13.5px;border:1px solid var(--li);border-radius:999px;padding:4px 10px;text-decoration:none}'
			. '.nlph-bars{list-style:none;padding:0;margin:14px 0;display:grid;gap:6px}.nlph-bars li{display:grid;grid-template-columns:minmax(92px,150px) 1fr auto;gap:10px;align-items:center;font-size:14px}'
			. '.nlph-bars i{display:block;height:14px;border-radius:3px;background:linear-gradient(90deg,var(--ac2),var(--ac));width:var(--w);transform-origin:right;animation:nlphGrow .9s ease-out both}'
			. '.nlph-bars li.is-tlv i{background:var(--ink)}.nlph-bars li.is-tlv span{font-weight:700}.nlph-bars b{font-weight:600;font-size:13.5px;font-variant-numeric:tabular-nums;white-space:nowrap}'
			. '.nlph-bars--thin i{height:10px}.nlph-two{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}'
			. '@keyframes nlphGrow{from{transform:scaleX(0)}to{transform:scaleX(1)}}'
			. '.nlph-tl{list-style:none;padding:0;margin:16px 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;counter-reset:s}'
			. '.nlph-tl li{position:relative;border:1px solid var(--li);border-radius:6px;padding:14px;background:#fff}'
			. '.nlph-tl__n{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--ink);color:#fff;font:600 14px "IBM Plex Mono",monospace;margin-bottom:8px}'
			. '.nlph-tl h3{font-size:16px!important;margin:0 0 2px!important}.nlph-tl p{font-size:14px!important;line-height:1.55!important;margin:0 0 6px!important}'
			. '.nlph-tl__t{font:500 12.5px "IBM Plex Mono",monospace!important;color:var(--ac2)}.nlph-tl__g{color:var(--ok);font-weight:500}'
			. '.nlph-pay{list-style:none;padding:0;margin:14px 0;display:grid;gap:12px}.nlph-pay p{margin:0 0 6px!important;display:flex;gap:10px;flex-wrap:wrap;align-items:baseline}'
			. '.nlph-pay p span{color:var(--mu);font-size:14px}.nlph-paybar{display:flex;border-radius:5px;overflow:hidden;border:1px solid var(--li)}'
			. '.nlph-paybar i{min-width:0;overflow:hidden;padding:6px 2px;font-style:normal;background:var(--bg);border-left:1px solid #fff;text-align:center}'
			. '.nlph-paybar i:last-child{background:#E3EAF2}.nlph-paybar b{display:block;font:600 14px "IBM Plex Mono",monospace;color:var(--ink)}.nlph-paybar small{display:block;font-size:11.5px;color:var(--mu)}'
			. '.nlph-link{display:flex;border-radius:5px;overflow:hidden;border:1px solid var(--li);margin:10px 0 14px}.nlph-link i{min-width:0;overflow:hidden;padding:10px 4px;font-style:normal;text-align:center}'
			. '.nlph-link .a,.nlph-link .c{background:var(--bg)}.nlph-link .b{background:repeating-linear-gradient(-45deg,#D9E6F0,#D9E6F0 8px,#EEF4F8 8px,#EEF4F8 16px)}'
			. '.nlph-link b{display:block;font:600 15px "IBM Plex Mono",monospace;color:var(--ink)}.nlph-link small{font-size:12px;color:var(--mu)}'
			. '.nlph-tabs{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}.nlph-tabs button{font:500 14.5px "IBM Plex Sans Hebrew",sans-serif;border:1px solid var(--li);background:#fff;color:var(--tx);border-radius:6px;padding:9px 14px;min-height:44px;cursor:pointer}'
			. '.nlph-tabs button[aria-selected="true"]{background:var(--ink);border-color:var(--ink);color:#fff}'
			. '.nlph-ck{list-style:none;padding:0;margin:12px 0;display:grid;gap:8px}.nlph-ck li{border:1px solid var(--li);border-radius:6px;padding:12px 14px}'
			. '.nlph-ck label{display:flex;gap:12px;align-items:flex-start;cursor:pointer}.nlph-ck input{width:22px;height:22px;margin-top:3px;accent-color:var(--ok);flex:0 0 auto}'
			. '.nlph-ck label b{display:block;color:var(--ink);font-size:16px}.nlph-ck label span{font-size:15px;line-height:1.6}.nlph-ck li.is-done{background:#F1F8F5;border-color:#A9D5C2}'
			. '.nlph-ck__l{font-size:13.5px!important;margin:6px 34px 0 0!important}.nlph-ck__p{font-size:15px!important}'
			. '.nlph-ty td,.nlph-ty th{font-size:14px;min-width:130px}.nlph-plans td{font-size:14.5px}'
			. '.nlph-cl{display:flex;flex-wrap:wrap;gap:8px}.nlph-cl a{border:1px solid var(--li);border-radius:999px;padding:7px 12px;font-size:14px;text-decoration:none;color:var(--tx)}'
			. '.nlph-cl a i{font-style:normal;color:var(--mu);font-size:12px}.nlph-cl--s a{font-size:13px;padding:5px 10px}'
			. '.nlph-guides{list-style:none;padding:0;margin:10px 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:8px}'
			. '.nlph-guides a{display:block;border:1px solid var(--li);border-radius:6px;padding:12px;text-decoration:none;color:var(--tx);height:100%}.nlph-guides b{display:block;color:var(--ink)}.nlph-guides span{font-size:13.5px;color:var(--mu)}'
			. '.nlph-faq details{border-bottom:1px solid var(--li);padding:12px 0}.nlph-faq summary{font:600 16px "IBM Plex Sans Hebrew",sans-serif;color:var(--ink);cursor:pointer;list-style-position:inside}'
			. '.nlph-faq details p{margin:8px 0 0!important}.nlph-faq__l{font-size:14px!important}'
			. '.nlph-srcs{columns:2 300px;padding-inline-start:18px;margin:8px 0}.nlph-srcs li{font-size:14px;margin:0 0 6px;break-inside:avoid}'
			. '@media(max-width:900px){.nlph-tl{grid-template-columns:repeat(2,minmax(0,1fr))}}'
			. '@media(max-width:640px){.nlph-tl{grid-template-columns:1fr}.nlph-tools{flex-direction:column;align-items:stretch}.nlph-sel{display:grid;grid-template-columns:1fr 1fr}.nlph-sel label:last-child{grid-column:1/-1}.nlph-sel select{width:100%}'
			. '.nlph-mt thead,.nlph-pt thead,.nlph-plans thead{display:none}.nlph-mt tr,.nlph-pt tr,.nlph-plans tr{display:block;border:1px solid var(--li);border-radius:6px;margin:0 0 8px;padding:6px 10px}'
			. '.nlph-mt th,.nlph-mt td,.nlph-pt th,.nlph-pt td,.nlph-plans th,.nlph-plans td{display:block;border:0;padding:4px 0}'
			. '.nlph-mt td[data-l]::before,.nlph-pt td[data-l]::before,.nlph-plans td[data-l]::before{content:attr(data-l) ": ";color:var(--mu);font-size:12.5px}'
			. '.nlph-mt td:empty,.nlph-pt td:empty{display:none}.nlph-bars li{grid-template-columns:96px 1fr auto}.nlph-paybar small{font-size:10.5px}}'
			. '@media(prefers-reduced-motion:reduce){.nlph-bars i{animation:none}}'
			. '</style>'
			. '<script id="nlph-js">(function(){'
			. 'var mt=document.querySelector(".nlph-mt");if(mt){var sec=document.getElementById("nlph-market"),reg="",tb=mt.tBodies[0],rows=[].slice.call(tb.rows),more=document.getElementById("nlph-more"),empty=sec.querySelector(".nlph-empty"),full=+(sec.dataset.full||0),busy=0;'
			. 'var ST={presale:"פריסייל",marketing:"בשיווק",construction:"בבנייה",near_occupancy:"אכלוס קרוב",immediate:"אכלוס מיידי"};'
			. 'function E(x){return String(x==null?"":x).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c];});}'
			. 'function RG(c){c=String(c||"").replace(/-/g," ");var m=[["tlv",["תל אביב","יפו"]],["dan",["רמת גן","גבעתיים","גבעתים","בת ים","חולון","בני ברק","קרית אונו","קריית אונו","פתח תקווה","פתח תקוה","אור יהודה","יהוד","גני תקווה","אזור","סביון"]],["center",["ראשון לציון","רחובות","נס ציונה","לוד","רמלה","יבנה","מודיעין","שוהם","באר יעקב","ראש העין","גדרה","מזכרת בתיה"]],["sharon",["הרצליה","רעננה","כפר סבא","הוד השרון","רמת השרון","נתניה","כפר יונה","אבן יהודה","צור יגאל","כוכב יאיר"]],["south",["אשדוד","אשקלון","באר שבע","אופקים","קרית גת","קריית גת","נתיבות","שדרות","דימונה","ערד","אילת","קרית מלאכי","קריית מלאכי","גן יבנה"]],["north",["חיפה","קרית","קריית","טירת כרמל","נהריה","עכו","עפולה","חדרה","כרמיאל","נשר","יקנעם","זכרון יעקב","פרדס חנה","אור עקיבא","נוף הגליל","טבריה","צפת"]],["jlm",["ירושלים","בית שמש","מבשרת","מעלה אדומים","גבעת זאב"]]];for(var i=0;i<m.length;i++){for(var j=0;j<m[i][1].length;j++){if(c.indexOf(m[i][1][j])>-1)return m[i][0];}}return "other";}'
			. 'function ROW(p){var n=E(p.name);if(p.url)n="<a href=\\""+E(sec.dataset.home.replace(/\\/$/,"")+p.url)+"\\">"+n+"</a>";var pl=(p.neighbourhood?p.neighbourhood+", ":"")+(p.city||"");'
			. 'var pc=p.price_from?"<b>"+Number(p.price_from).toLocaleString("en-US")+" ₪</b>"+(p.price_note?"<small>"+E(p.price_note)+"</small>":""):(p.price_psqm?"<b>"+Number(p.price_psqm).toLocaleString("en-US")+" ₪</b><small>למ\\"ר</small>":"<span class=\\"nlph-na\\">לפי פנייה ליזם</span>");'
			. 'var tr=document.createElement("tr");tr.dataset.reg=RG(p.city);tr.dataset.st=p.status||"";tr.dataset.price=p.price_from||0;'
			. 'tr.innerHTML="<th scope=\\"row\\">"+n+"<small>"+E(pl)+"</small></th><td data-l=\\"יזם\\">"+E(p.developer)+"</td><td data-l=\\"חדרים\\">"+E(p.rooms)+"</td><td data-l=\\"החל מ\\" class=\\"nlph-p\\">"+pc+"</td><td data-l=\\"תנאים\\">"+E(p.deal)+"</td><td data-l=\\"שלב\\">"+(ST[p.status]?"<span class=\\"nlph-st nlph-st--"+E(p.status)+"\\">"+ST[p.status]+"</span>":"")+(p.delivery?"<small>מסירה: "+E(p.delivery)+"</small>":"")+"</td>";return tr;}'
			. 'function load(cb){if(full||busy){if(full)cb();return;}busy=1;sec.classList.add("is-busy");fetch(sec.dataset.src).then(function(r){return r.json();}).then(function(d){var ps=(d&&d.projects)||[];if(ps.length){tb.innerHTML="";rows=ps.map(ROW);rows.forEach(function(r){tb.appendChild(r);});}full=1;busy=0;sec.classList.remove("is-busy");cb();}).catch(function(){full=1;busy=0;sec.classList.remove("is-busy");cb();});}'
			. 'function f(){var st=sec.querySelector("[data-f=st]").value,mx=+sec.querySelector("[data-f=max]").value||0,so=sec.querySelector("[data-f=sort]").value,shown=0;'
			. 'var RK={tlv:0,dan:1,sharon:2,center:3,jlm:4,north:5,south:6,other:7};rows.sort(function(a,b){var pa=+a.dataset.price||9e12,pb=+b.dataset.price||9e12;if(so==="desc")return (+b.dataset.price||0)-(+a.dataset.price||0);if(so==="rec"){var ra=RK[a.dataset.reg],rb=RK[b.dataset.reg];if(ra!==rb)return ra-rb;}return pa-pb;});rows.forEach(function(r){tb.appendChild(r);});'
			. 'var cap=!(reg||st||mx)&&mt.dataset.all!=="1";rows.forEach(function(r){var ok=(!reg||r.dataset.reg===reg)&&(!st||(st==="near"?(r.dataset.st==="near_occupancy"||r.dataset.st==="immediate"):r.dataset.st===st))&&(!mx||(+r.dataset.price&&+r.dataset.price<=mx));r.classList.toggle("is-off",!ok);if(ok)shown++;r.classList.toggle("nlph-more",ok&&cap&&shown>16);});'
			. 'if(more)more.hidden=!cap||shown<=16;if(empty)empty.hidden=shown>0;}'
			. 'sec.querySelectorAll(".nlph-chips button").forEach(function(b){b.addEventListener("click",function(){sec.querySelectorAll(".nlph-chips button").forEach(function(x){x.classList.toggle("is-on",x===b);});reg=b.dataset.reg;load(f);});});'
			. 'sec.querySelectorAll("select[data-f]").forEach(function(s){s.addEventListener("change",function(){load(f);});});if(more)more.addEventListener("click",function(){mt.dataset.all="1";load(f);});}'
			. 'var tabs=[].slice.call(document.querySelectorAll(".nlph-tabs [role=tab]"));tabs.forEach(function(t,i){t.addEventListener("click",function(){tabs.forEach(function(x){var on=x===t;x.setAttribute("aria-selected",on?"true":"false");x.tabIndex=on?0:-1;var p=document.getElementById(x.getAttribute("aria-controls"));if(p)p.hidden=!on;});});'
			. 't.addEventListener("keydown",function(e){var k=e.key,j=-1;if(k==="ArrowLeft")j=(i+1)%tabs.length;if(k==="ArrowRight")j=(i-1+tabs.length)%tabs.length;if(j>-1){e.preventDefault();tabs[j].focus();tabs[j].click();}});});'
			. 'var ck=[].slice.call(document.querySelectorAll(".nlph-ck input"));if(ck.length){var key="nlph-checks-v1",st={};try{st=JSON.parse(localStorage.getItem(key)||"{}")||{};}catch(e){st={};}'
			. 'function sync(){var n=0;ck.forEach(function(c){c.closest("li").classList.toggle("is-done",c.checked);if(c.checked)n++;});var o=document.getElementById("nlph-ck-n");if(o)o.textContent=n;}'
			. 'ck.forEach(function(c){c.checked=!!st[c.dataset.i];c.addEventListener("change",function(){st[c.dataset.i]=c.checked;try{localStorage.setItem(key,JSON.stringify(st));}catch(e){}sync();});});sync();}'
			. '})();</script>';
	}
}

/* ------------------------------------------------------------------------------------------------ tools, sharing, schema */
add_filter( 'nadlan_nli_page_ids', function ( $ids ) {
	if ( ! is_post_type_archive( 'nadlan_project' ) ) { return $ids; }
	return array_values( array_unique( array_merge( (array) $ids, array( 'indexation', 'pcost', 'ptax', 'afford', 'delay', 'pinkas', 'warranty' ) ) ) );
} );

/* F2 (our-page.md): og:title and the CollectionPage name were Yoast's archive default "ארכיון NadLan Projects - נדלן". The
 * <title> itself is untouched (inc/directory.php owns it); sharing and the schema now carry the same words. */
if ( ! function_exists( 'nadlan_ph_share_title' ) ) {
	function nadlan_ph_share_title() { return 'פרויקטים חדשים ודירות חדשות למכירה בישראל - מעודכן ל-2026 | נדלן'; } // HAD-689: = the <title>
}
add_filter( 'wpseo_opengraph_title', function ( $t ) { return is_post_type_archive( 'nadlan_project' ) ? nadlan_ph_share_title() : $t; }, 20 );
add_filter( 'wpseo_twitter_title', function ( $t ) { return is_post_type_archive( 'nadlan_project' ) ? nadlan_ph_share_title() : $t; }, 20 );
add_filter( 'wpseo_schema_webpage', function ( $d ) {
	if ( ! is_array( $d ) || ! is_post_type_archive( 'nadlan_project' ) ) { return $d; }
	$d['name'] = nadlan_ph_share_title();
	$d['description'] = 'פרויקטים חדשים ודירות מקבלן בישראל: קטלוג לפי עיר ויזם, פרויקטים בשיווק עם המחיר שפרסם היזם, פרויקטים חדשים בתל אביב, מחירי עסקאות לפי עיר, לוח זמנים מהיתר למפתח, מחשבונים ובדיקות לפני חתימה.';
	$d['dateModified'] = NADLAN_PH_UPDATED_HE . 'T08:00:00+02:00'; // winter time from 25.10
	return $d;
}, 25 );

/* HAD-700 (10.11.2026): where the server time of a page goes. Nothing runs and nothing is printed without the private key in
 * ?nlprof= (only its hash is here); with it, one HTML comment before </body> lists the phases, the WP_Query runs and the slowest
 * SQL of that one request. Measurement only: no visitor and no crawler sees any difference. */
if ( isset( $_GET['nlprof'] ) && is_string( $_GET['nlprof'] ) && hash_equals( 'b3c49f2a20285bfa3801f9c6719b372132f3b552f673bbaefe2cc8352bebd7d2', hash( 'sha256', $_GET['nlprof'] ) ) ) { // phpcs:ignore WordPress.Security.NonceVerification.Recommended
	if ( ! defined( 'SAVEQUERIES' ) ) { define( 'SAVEQUERIES', true ); }
	$GLOBALS['nlprof'] = array( 't0' => (float) ( $_SERVER['REQUEST_TIME_FLOAT'] ?? microtime( true ) ), 'load' => microtime( true ), 'marks' => array(), 'wq' => array() );
	foreach ( array( 'init', 'wp_loaded', 'parse_request', 'wp', 'template_redirect', 'get_header', 'wp_head', 'wp_body_open', 'loop_start', 'get_footer', 'wp_footer' ) as $nlprof_h ) {
		add_action( $nlprof_h, function () use ( $nlprof_h ) { if ( ! isset( $GLOBALS['nlprof']['marks'][ $nlprof_h ] ) ) { $GLOBALS['nlprof']['marks'][ $nlprof_h ] = microtime( true ); } }, -99999 );
	}
	add_filter( 'posts_request', function ( $sql, $q ) {
		$pt = $q->get( 'post_type' );
		$GLOBALS['nlprof']['wq'][] = '@' . (int) round( 1000 * ( microtime( true ) - $GLOBALS['nlprof']['t0'] ) ) . ' ' . ( is_array( $pt ) ? implode( '+', $pt ) : (string) $pt ) . ' main=' . ( $q->is_main_query() ? 1 : 0 )
			. ' boost=' . ( $q->get( 'nadlan_paid_placement_boost' ) ? 1 : 0 ) . ' ppp=' . (int) $q->get( 'posts_per_page' ) . ' fields=' . (string) $q->get( 'fields' ) . ' sqllen=' . strlen( (string) $sql );
		return $sql;
	}, 99999, 2 );
	add_action( 'wp_footer', function () {
		global $wpdb;
		$p = $GLOBALS['nlprof']; $now = microtime( true );
		$ms = function ( $x ) { return (int) round( 1000 * $x ); };
		$o = array( 'total_ms' => $ms( $now - $p['t0'] ), 'before_this_file_ms' => $ms( $p['load'] - $p['t0'] ), 'mem_mb' => round( memory_get_peak_usage() / 1048576, 1 ), 'savequeries' => ( defined( 'SAVEQUERIES' ) && SAVEQUERIES ) ? 1 : 0 );
		$prev = $p['load']; $ph = array();
		foreach ( $p['marks'] as $k => $t ) { $ph[] = $k . '+' . $ms( $t - $prev ); $prev = $t; }
		$ph[] = 'footer_end+' . $ms( $now - $prev );
		$o['phases_ms'] = implode( ' ', $ph );
		$qs = ( isset( $wpdb->queries ) && is_array( $wpdb->queries ) ) ? $wpdb->queries : array(); $tot = 0.0; $rows = array();
		foreach ( $qs as $q ) { $tot += (float) $q[1]; $rows[] = array( (float) $q[1], (string) $q[0], (string) ( $q[2] ?? '' ), (float) ( $q[3] ?? 0 ) ); }
		usort( $rows, function ( $a, $b ) { return $b[0] <=> $a[0]; } );
		$o['sql_count'] = count( $qs ); $o['sql_ms'] = $ms( $tot );
		$lines = array();
		foreach ( array_slice( $rows, 0, 14 ) as $r ) {
			$caller = implode( ' < ', array_slice( array_reverse( array_map( 'trim', explode( ',', $r[2] ) ) ), 0, 5 ) );
			$lines[] = $ms( $r[0] ) . 'ms @' . $ms( $r[3] - $p['t0'] ) . ' | ' . substr( (string) preg_replace( '/\s+/', ' ', $r[1] ), 0, 420 ) . ' | ' . $caller;
		}
		$txt = 'nlprof ' . wp_json_encode( $o ) . "\nWP_Query runs (" . count( $p['wq'] ) . "):\n" . implode( "\n", $p['wq'] ) . "\nslowest SQL:\n" . implode( "\n", $lines );
		echo "\n<!-- " . str_replace( array( '--', '<', '>' ), array( '- -', '(', ')' ), $txt ) . " -->\n"; // phpcs:ignore
	}, 99999 );
}

/* 1.72.514: the hub in English, Russian and French (/en|ru|fr/projects/). Loaded only when the file is there, so a rollback that
 * removes it never leaves this file requiring a missing one (the 25.10 incident). */
if ( file_exists( __DIR__ . '/projects-hub-lang.php' ) ) { require_once __DIR__ . '/projects-hub-lang.php'; }
