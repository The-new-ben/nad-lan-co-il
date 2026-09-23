<?php
/**
 * nadlan-config · Broker drop box (x-broker-drop) · v1.0.0 · 23.9.2026
 *
 * Owner order 23.9.2026 (voice): a broker gets one private address, throws photos and a few lines at it,
 * and the system builds the property in the broker's own website. No replies. No login. No owner step.
 * For every future broker, not only the first one.
 *
 * The address is a personal link: https://nad-lan.co.il/drop/<token>/
 *   photos + free text  ->  the AI reads the facts and keeps only what the broker wrote (numbers are checked)
 *   ->  it writes the page in the luxury-broker voice (docs/dna/luxury-broker-copy-dna-2026-09.md), gated
 *   ->  a Hebrew listing at /properties/<latin-slug>/ and, when the broker has an English site, its English twin
 *   ->  the property shows first in the broker's own site, with hreflang between the languages.
 * The broker sees the result on the same screen; nothing is sent to anyone.
 * The same screen lists the broker's properties: sold or let in one tap (Brokers Ethics Regulations,
 * reg. 19(c): a publication is removed or updated once the property is off the market), a new price in two.
 * Every listing carries the broker's name, "broker" status and licence number (reg. 19(a)).
 *
 * Installed as the persistent Code Snippet "x-broker-drop" by scripts/broker-drop/deploydrop.py.
 * Rollback: python scripts/broker-drop/deploydrop.py --off
 */

if ( ! defined( 'ABSPATH' ) ) { return; }
if ( defined( 'NL_DROP_VERSION' ) ) { return; }
define( 'NL_DROP_VERSION', '1.0.0' );
define( 'NL_DROP_MAX_BYTES', 15728640 );
define( 'NL_DROP_MAX_PHOTOS', 30 );

/* =====================================================================================================
 * Registration: meta the deploy script and the admin box write, and the private submissions log.
 * ===================================================================================================== */
add_action( 'init', function () {
	$auth = function () { return current_user_can( 'edit_posts' ); };
	$str  = array( 'type' => 'string', 'single' => true, 'show_in_rest' => true, 'auth_callback' => $auth );
	foreach ( array( 'nl_drop_on', 'nl_drop_token', 'nl_name_he', 'nl_name_en', 'nl_brand_en', 'nl_gender', 'nl_site_he', 'nl_site_en', 'nl_auto_publish' ) as $k ) {
		register_post_meta( 'nadlan_professional', $k, $str );
	}
	foreach ( array( 'nadlan_property', 'page' ) as $t ) {
		foreach ( array( 'nl_broker_id', 'nl_card_key', 'nl_twin', 'nl_status', 'nl_broker_site', 'nl_lang', 'nl_drop_id' ) as $k ) {
			register_post_meta( $t, $k, $str );
		}
	}
	register_post_type( 'nadlan_drop', array(
		'labels'          => array( 'name' => 'תיבת נכסים', 'singular_name' => 'שליחה', 'menu_name' => 'תיבת נכסים', 'all_items' => 'תיבת נכסים' ),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => 'edit.php?post_type=nadlan_professional',
		'supports'        => array( 'title', 'editor' ),
		'capability_type' => 'post',
		'map_meta_cap'    => true,
		'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
	) );
}, 20 );

/* =====================================================================================================
 * Brokers
 * ===================================================================================================== */
function nl_drop_broker( $pid ) {
	$p = get_post( (int) $pid );
	if ( ! $p || $p->post_type !== 'nadlan_professional' ) { return null; }
	$m = function ( $k ) use ( $p ) { return trim( (string) get_post_meta( $p->ID, $k, true ) ); };
	$parts   = preg_split( '/\s*·\s*/u', (string) $p->post_title );
	$name_he = $m( 'nl_name_he' ) !== '' ? $m( 'nl_name_he' ) : trim( (string) $parts[0] );
	$phone   = $m( 'phone' );
	$digits  = preg_replace( '/\D+/', '', $phone );
	if ( $digits !== '' && $digits[0] === '0' ) { $digits = '972' . substr( $digits, 1 ); }
	$nat  = strpos( $digits, '972' ) === 0 ? substr( $digits, 3 ) : '';
	$intl = strlen( $nat ) >= 8 ? '+972 ' . substr( $nat, 0, 2 ) . '-' . substr( $nat, 2, 3 ) . '-' . substr( $nat, 5 ) : $phone;
	return array(
		'id'         => (int) $p->ID,
		'name_he'    => $name_he,
		'name_en'    => $m( 'nl_name_en' ) !== '' ? $m( 'nl_name_en' ) : $name_he,
		'brand_he'   => $m( 'company_name' ),
		'brand_en'   => $m( 'nl_brand_en' ) !== '' ? $m( 'nl_brand_en' ) : $m( 'company_name' ),
		'license'    => $m( 'license_number' ),
		'phone'      => $phone,
		'phone_intl' => $intl,
		'wa'         => $digits,
		'female'     => $m( 'nl_gender' ) === 'f',
		'site_he'    => (int) $m( 'nl_site_he' ),
		'site_en'    => (int) $m( 'nl_site_en' ),
		'auto'       => $m( 'nl_auto_publish' ) !== '0',
		'on'         => $m( 'nl_drop_on' ) === '1',
		'token'      => $m( 'nl_drop_token' ),
		'areas'      => array_values( array_filter( array_map( 'trim', explode( ',', $m( 'areas_served' ) ) ) ) ),
	);
}

function nl_drop_broker_by_token( $token ) {
	$token = (string) $token;
	if ( ! preg_match( '/^[a-z0-9]{24}$/', $token ) ) { return null; }
	$ids = get_posts( array(
		'post_type'        => 'nadlan_professional',
		'post_status'      => 'publish',
		'numberposts'      => 1,
		'fields'           => 'ids',
		'no_found_rows'    => true,
		'suppress_filters' => true,
		'meta_query'       => array( array( 'key' => 'nl_drop_token', 'value' => $token ) ),
	) );
	if ( ! $ids ) { return null; }
	$b = nl_drop_broker( $ids[0] );
	if ( ! $b || ! $b['on'] || $b['token'] === '' || ! hash_equals( $b['token'], $token ) ) { return null; }
	return $b;
}

function nl_drop_new_token() {
	return substr( bin2hex( random_bytes( 16 ) ), 0, 24 );
}

function nl_drop_author() {
	$a = (int) get_option( 'nl_drop_author', 0 );
	if ( $a && get_userdata( $a ) ) { return $a; }
	$admins = get_users( array( 'role' => 'administrator', 'number' => 1, 'fields' => 'ID', 'orderby' => 'ID', 'order' => 'ASC' ) );
	return $admins ? (int) $admins[0] : 1;
}

function nl_drop_rate( $bid, $bucket, $limit, $window ) {
	$k = 'nldrop_' . $bucket . '_' . (int) $bid;
	$n = (int) get_transient( $k );
	if ( $n >= $limit ) { return true; }
	set_transient( $k, $n + 1, $window );
	return false;
}

function nl_drop_site_url( $b, $lang ) {
	$id = $lang === 'en' ? (int) $b['site_en'] : (int) $b['site_he'];
	return $id ? (string) get_permalink( $id ) : '';
}

/* =====================================================================================================
 * Words, numbers, icons
 * ===================================================================================================== */
function nl_drop_t( $lang, $k ) {
	static $T = array(
		'he' => array(
			'sale' => 'למכירה', 'rent' => 'להשכרה', 'exclusive' => 'בלעדיות', 'sqm' => 'מ״ר', 'of' => 'מתוך', 'yes' => 'יש',
			'f_rooms' => 'חדרים', 'f_size' => 'שטח', 'f_balcony' => 'מרפסת', 'f_garden' => 'גינה', 'f_floor' => 'קומה', 'f_parking' => 'חניה',
			'f_storage' => 'מחסן', 'f_safe' => 'ממ״ד', 'f_lift' => 'מעלית', 'f_condition' => 'מצב', 'f_entry' => 'כניסה', 'f_furnished' => 'ריהוט',
			'c_new' => 'חדש', 'c_renovated' => 'משופץ', 'c_good' => 'שמור', 'c_needs_renovation' => 'דורש שיפוץ', 'furnished' => 'מרוהט',
			'price_sale' => 'מחיר', 'price_rent' => 'שכר דירה לחודש', 'ask_sale' => 'המחיר נמסר בפנייה ישירה', 'ask_rent' => 'שכר הדירה נמסר בפנייה ישירה',
			'psqm_sale' => 'למ״ר', 'psqm_rent' => 'למ״ר לחודש', 'year' => 'בשנה',
			'cta' => 'תיאום סיור פרטי', 'call' => 'חיוג', 'wa' => 'וואטסאפ', 'home' => 'הבית', 'photos' => 'תמונות', 'photos_h2' => 'הנכס בתמונות',
			'broker_f' => 'המתווכת', 'broker_m' => 'המתווך', 'broker_ex_f' => 'המתווכת בבלעדיות', 'broker_ex_m' => 'המתווך בבלעדיות',
			'lic_f' => 'מתווכת במקרקעין, רישיון', 'lic_m' => 'מתווך במקרקעין, רישיון', 'site' => 'האתר של %s', 'switch' => 'English',
			'toc' => 'תוכן העמוד', 'rail' => 'מחיר ויצירת קשר', 'sold' => 'הנכס נמכר', 'rented' => 'הנכס הושכר', 'more' => 'לנכסים נוספים של %s',
			'card_view' => 'לעמוד הנכס', 'updated' => 'עודכן', 'month' => 'לחודש', 'ask_short' => 'המחיר נמסר בפנייה', 'ask_short_rent' => 'שכר הדירה נמסר בפנייה',
			'ask_sub' => 'פרטים בפנייה ישירה', 'rooms_n' => '%s חדרים', 'size_n' => '%s מ״ר', 'balcony_n' => 'מרפסת %s מ״ר', 'garden_n' => 'גינה %s מ״ר',
			'floor_of' => 'קומה %1$s מתוך %2$s', 'floor_n' => 'קומה %s', 'parking_n' => '%s חניות', 'parking_1' => 'חניה', 'entry_n' => 'כניסה: %s',
			'wa_text' => 'שלום %1$s, אשמח לפרטים ולתיאום סיור: %2$s (nad-lan.co.il)',
		),
		'en' => array(
			'sale' => 'For sale', 'rent' => 'For rent', 'exclusive' => 'Exclusive', 'sqm' => 'sqm', 'of' => 'of', 'yes' => 'Yes',
			'f_rooms' => 'Rooms', 'f_size' => 'Area', 'f_balcony' => 'Balcony', 'f_garden' => 'Garden', 'f_floor' => 'Floor', 'f_parking' => 'Parking',
			'f_storage' => 'Storage', 'f_safe' => 'Safe room', 'f_lift' => 'Lift', 'f_condition' => 'Condition', 'f_entry' => 'Entry', 'f_furnished' => 'Furniture',
			'c_new' => 'New', 'c_renovated' => 'Renovated', 'c_good' => 'Well kept', 'c_needs_renovation' => 'Needs renovation', 'furnished' => 'Furnished',
			'price_sale' => 'Asking price', 'price_rent' => 'Monthly rent', 'ask_sale' => 'Price on request', 'ask_rent' => 'Rent on request',
			'psqm_sale' => 'Per sqm', 'psqm_rent' => 'Per sqm a month', 'year' => 'A year',
			'cta' => 'Book a private viewing', 'call' => 'Call', 'wa' => 'WhatsApp', 'home' => 'The residence', 'photos' => 'Photographs', 'photos_h2' => 'The home in pictures',
			'broker_f' => 'Broker', 'broker_m' => 'Broker', 'broker_ex_f' => 'Exclusive broker', 'broker_ex_m' => 'Exclusive broker',
			'lic_f' => 'licensed real estate broker, licence', 'lic_m' => 'licensed real estate broker, licence', 'site' => 'More from %s', 'switch' => 'עברית',
			'toc' => 'On this page', 'rail' => 'Price and contact', 'sold' => 'This home has been sold', 'rented' => 'This home has been let', 'more' => 'More homes from %s',
			'card_view' => 'Listing page', 'updated' => 'Updated', 'month' => 'a month', 'ask_short' => 'Price on request', 'ask_short_rent' => 'Rent on request',
			'ask_sub' => 'Details given on direct enquiry', 'rooms_n' => '%s rooms', 'size_n' => '%s sqm', 'balcony_n' => '%s sqm balcony', 'garden_n' => '%s sqm garden',
			'floor_of' => 'Floor %1$s of %2$s', 'floor_n' => 'Floor %s', 'parking_n' => '%s parking', 'parking_1' => 'Parking', 'entry_n' => 'Entry: %s',
			'wa_text' => 'Hello %1$s, I would like details and a viewing: %2$s (nad-lan.co.il)',
		),
	);
	$lang = $lang === 'en' ? 'en' : 'he';
	return isset( $T[ $lang ][ $k ] ) ? $T[ $lang ][ $k ] : $k;
}

function nl_drop_type_label( $t, $lang ) {
	static $he = array( 'apartment' => 'דירה', 'penthouse' => 'פנטהאוז', 'mini_penthouse' => 'מיני פנטהאוז', 'garden' => 'דירת גן', 'duplex' => 'דופלקס', 'villa' => 'וילה', 'cottage' => 'קוטג׳', 'studio' => 'סטודיו', 'other' => 'נכס' );
	static $en = array( 'apartment' => 'Apartment', 'penthouse' => 'Penthouse', 'mini_penthouse' => 'Mini penthouse', 'garden' => 'Garden apartment', 'duplex' => 'Duplex', 'villa' => 'Villa', 'cottage' => 'Cottage', 'studio' => 'Studio', 'other' => 'Property' );
	$t = isset( $en[ (string) $t ] ) ? (string) $t : 'other';
	return $lang === 'en' ? $en[ $t ] : $he[ $t ];
}

function nl_drop_fmt_int( $n ) {
	return number_format( (float) $n, 0, '.', ',' );
}

function nl_drop_fmt_num( $n ) {
	$n = (float) $n;
	if ( floor( $n ) == $n ) { return number_format( $n, 0, '.', ',' ); }
	return rtrim( rtrim( number_format( $n, 2, '.', ',' ), '0' ), '.' );
}

function nl_drop_money_html( $n, $lang ) {
	$num = '<span class="nlx-num">' . esc_html( nl_drop_fmt_int( $n ) ) . '</span>';
	return '<span class="nlx-money">' . ( $lang === 'en' ? 'NIS&nbsp;' . $num : $num . '&nbsp;₪' ) . '</span>';
}

function nl_drop_price_text( $n, $lang ) {
	return $lang === 'en' ? 'NIS ' . nl_drop_fmt_int( $n ) : nl_drop_fmt_int( $n ) . ' ש״ח';
}

/** Every number a broker wrote, including "4.2 מיליון" as 4200000 and "15 אלף" as 15000. */
function nl_drop_nums_in_text( $text ) {
	$out = array();
	if ( preg_match_all( '/(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(\s*(?:מיליון|מליון|million|mil\b|M\b|אלף|thousand|K\b|k\b))?/u', (string) $text, $mm, PREG_SET_ORDER ) ) {
		foreach ( $mm as $x ) {
			$n     = (float) str_replace( ',', '', $x[1] );
			$out[] = $n;
			$mul   = isset( $x[2] ) ? trim( $x[2] ) : '';
			if ( $mul !== '' ) {
				$out[] = preg_match( '/^(מיליון|מליון|million|mil|M)$/u', $mul ) ? $n * 1000000 : $n * 1000;
			}
		}
	}
	return $out;
}

function nl_drop_nums_in_copy( $s ) {
	$out = array();
	$s   = str_replace( '{{PRICE}}', ' ', (string) $s );
	if ( preg_match_all( '/\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?/u', $s, $m ) ) {
		foreach ( $m[0] as $x ) { $out[] = (float) str_replace( ',', '', $x ); }
	}
	return $out;
}

function nl_drop_num_ok( $n, $allowed ) {
	foreach ( (array) $allowed as $a ) {
		if ( abs( (float) $n - (float) $a ) <= max( 0.011, abs( (float) $a ) * 0.005 ) ) { return true; }
	}
	return false;
}

function nl_drop_norm( $s ) {
	$s = (string) $s;
	$s = str_replace( array( '״', '"', '׳', "'", '’', '`' ), array( '"', '"', "'", "'", "'", "'" ), $s );
	$s = preg_replace( '/\s+/u', ' ', $s );
	return function_exists( 'mb_strtolower' ) ? mb_strtolower( trim( $s ) ) : strtolower( trim( $s ) );
}

function nl_drop_icon( $k ) {
	static $p = array(
		'rooms'   => '<path d="M3.5 20V9.5L12 4l8.5 5.5V20M9.5 20v-5.5h5V20"/>',
		'area'    => '<rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M4 9h3M4 14h3M9 4v3M14 4v3"/>',
		'balcony' => '<path d="M7 11V5h10v6M4 11h16M6 11v8M10 11v8M14 11v8M18 11v8M4 19h16"/>',
		'floor'   => '<path d="M4 20h4v-4h4v-4h4V8h4"/>',
		'parking' => '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M10 16.5v-9h3.2a2.7 2.7 0 010 5.4H10"/>',
		'storage' => '<path d="M4 8.2L12 4l8 4.2v7.6L12 20l-8-4.2z"/><path d="M4 8.2l8 4.2 8-4.2M12 12.4V20"/>',
		'shield'  => '<path d="M12 3.5l7 2.8v5.1c0 4.6-2.9 7.6-7 9.1-4.1-1.5-7-4.5-7-9.1V6.3z"/>',
		'lift'    => '<rect x="5.5" y="3.5" width="13" height="17" rx="1.5"/><path d="M9.5 9.5l2.5-2.5 2.5 2.5M9.5 14.5l2.5 2.5 2.5-2.5"/>',
		'key'     => '<circle cx="8" cy="12" r="3.6"/><path d="M11.6 12H20.5M17.5 12v3M20.5 12v2.4"/>',
		'sea'     => '<path d="M3 11c2.4 0 2.6-2 5-2s2.6 2 5 2 2.6-2 5-2 2.4 2 3 2M3 16c2.4 0 2.6-2 5-2s2.6 2 5 2 2.6-2 5-2 2.4 2 3 2"/>',
		'arrow'   => '<path d="M5 12h14M13 6l6 6-6 6"/>',
		'phone'   => '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2"/>',
		'wa'      => '<path fill="currentColor" stroke="none" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/>',
	);
	if ( ! isset( $p[ $k ] ) ) { return ''; }
	return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' . $p[ $k ] . '</svg>';
}

/* =====================================================================================================
 * The language gate (the same families the Meital runner refuses) and the no-invention check
 * ===================================================================================================== */
function nl_drop_banned( $lang ) {
	if ( $lang === 'en' ) {
		return array( 'madlan', 'yad2', 'instagram', 'not verified', 'unverified', 'according to the broker', 'per the listing', 'not published', 'not confirmed', 'the marketer',
			'once in a lifetime', 'dream', 'stunning', 'breathtaking', 'must see', "won't last", 'hurry', 'unique opportunity', 'luxury at its finest', '—', '–', '!' );
	}
	return array( 'לפי המשווקת', 'המשווקת', 'לפי המתווכת', 'לפי המתווך', 'מדלן', 'יד2', 'יד 2', 'אינסטגרם', 'לא אומת', 'יש לאמת', 'לא פורסם', 'זמינות בבדיקה',
		'הזדמנות', 'חלום', 'מושלם', 'מדהים', 'פנטסטי', 'חוויה', 'לא תחזור', 'יוקרה במיטבה', 'בעידן', '—', '–', '!' );
}

function nl_drop_gate_str( $s, $lang, $allowed, $stated = null, $names = array() ) {
	$issues = array();
	$low    = nl_drop_norm( $s );
	foreach ( nl_drop_banned( $lang ) as $w ) {
		if ( $w !== '' && strpos( $low, nl_drop_norm( $w ) ) !== false ) { $issues[] = 'banned:' . $w; }
	}
	foreach ( nl_drop_nums_in_copy( $s ) as $n ) {
		if ( ! nl_drop_num_ok( $n, $allowed ) ) { $issues[] = 'number:' . $n; }
	}
	if ( preg_match( '/https?:|www\./i', (string) $s ) ) { $issues[] = 'link'; }
	if ( is_array( $stated ) ) {
		$bare = (string) $s;
		foreach ( (array) $names as $nm ) {
			if ( $nm !== '' && $nm !== null ) { $bare = str_ireplace( nl_drop_he_typo( $nm ), ' ', str_ireplace( $nm, ' ', $bare ) ); }
		}
		foreach ( nl_drop_claims_in( $bare ) as $g ) {
			if ( ! in_array( $g, $stated, true ) ) { $issues[] = 'claim:' . $g; }
		}
	}
	return $issues;
}

/** Hebrew typography: מ"ר -> מ״ר, ג'קוזי -> ג׳קוזי. */
function nl_drop_he_typo( $s ) {
	$s = preg_replace( '/(?<=[\x{05D0}-\x{05EA}])"(?=[\x{05D0}-\x{05EA}])/u', '״', (string) $s );
	return preg_replace( "/(?<=[\\x{05D0}-\\x{05EA}])'/u", '׳', $s );
}

/** Descriptive claims a page may make only when the broker made them. */
function nl_drop_claim_groups() {
	return array(
		'sea'      => array( 'ים', 'לים', 'הים', 'מהים', 'בים', 'וים', 'sea', 'seafront', 'beach', 'חוף', 'לחוף', 'החוף' ),
		'view'     => array( 'נוף', 'לנוף', 'הנוף', 'ונוף', 'נופים', 'view', 'views' ),
		'park'     => array( 'פארק', 'לפארק', 'הפארק', 'park' ),
		'quiet'    => array( 'שקט', 'שקטה', 'שקטים', 'בשקט', 'quiet', 'peaceful', 'calm' ),
		'bright'   => array( 'מואר', 'מוארת', 'מוארים', 'אור', 'bright', 'light-filled', 'sunlit' ),
		'new'      => array( 'חדש', 'חדשה', 'חדשים', 'חדשות', 'new', 'brand-new' ),
		'reno'     => array( 'משופץ', 'משופצת', 'שופץ', 'שופצה', 'renovated', 'refurbished' ),
		'boutique' => array( 'בוטיק', 'boutique' ),
		'design'   => array( 'מעצב', 'מעצבת', 'מעוצב', 'מעוצבת', 'designer', 'designed' ),
		'luxury'   => array( 'יוקרה', 'יוקרתי', 'יוקרתית', 'יוקרתיים', 'luxury', 'luxurious', 'prestigious' ),
		'spacious' => array( 'מרווח', 'מרווחת', 'מרווחים', 'spacious', 'generous', 'roomy' ),
		'garden'   => array( 'גינה', 'לגינה', 'הגינה', 'garden' ),
		'pool'     => array( 'בריכה', 'בריכת', 'pool' ),
		'gym'      => array( 'כושר', 'gym', 'fitness' ),
		'guard'    => array( 'שומר', 'שמירה', 'מאבטח', 'לובי', 'guard', 'security', 'concierge', 'lobby' ),
		'walk'     => array( 'הליכה', 'דקות', 'walk', 'minutes', 'minute' ),
		'school'   => array( 'בית ספר', 'בתי ספר', 'גן ילדים', 'school', 'schools', 'kindergarten' ),
		'transit'  => array( 'רכבת', 'הרכבת', 'אוטובוס', 'train', 'rail', 'metro', 'bus' ),
		'size'     => array( 'רחב', 'רחבה', 'רחבים', 'רחבות', 'ענק', 'ענקית', 'עצום', 'עצומה', 'גדול', 'גדולה', 'גדולים', 'expansive', 'wide', 'large', 'huge', 'vast', 'sweeping', 'ample' ),
		'quality'  => array( 'איכותי', 'איכותית', 'איכותיים', 'איכות', 'גימור', 'high-quality', 'quality', 'premium', 'high-end', 'fine' ),
		'advanced' => array( 'מתקדם', 'מתקדמת', 'מתקדמים', 'מתקדמות', 'חדשני', 'חדשנית', 'advanced', 'state-of-the-art', 'cutting-edge', 'modern' ),
		'living'   => array( 'סלון', 'מהסלון', 'לסלון', 'living', 'lounge' ),
		'control'  => array( 'שליטה', 'control', 'centralized' ),
		'family'   => array( 'משפחה', 'משפחות', 'family', 'families' ),
		'light'    => array( 'אור', 'שמש', 'sun', 'sunny', 'daylight' ),
	);
}

function nl_drop_words( $s ) {
	$s = nl_drop_norm( $s );
	$s = preg_replace( '/[^\p{L}\p{N}\s-]+/u', ' ', $s );
	return array_values( array_filter( preg_split( '/\s+/u', $s ) ) );
}

function nl_drop_claims_in( $s ) {
	$words = array();
	foreach ( nl_drop_words( $s ) as $w ) {
		$words[ $w ] = true;
		// Hebrew one- and two-letter prefixes: ושקטה, הים, לנוף, מהים
		if ( preg_match( '/^[\x{05D5}\x{05D4}\x{05D1}\x{05DC}\x{05DE}\x{05E9}\x{05DB}]{1,2}(?=\p{Hebrew}{2,})/u', $w ) ) {
			$words[ preg_replace( '/^[\x{05D5}\x{05D4}\x{05D1}\x{05DC}\x{05DE}\x{05E9}\x{05DB}]/u', '', $w ) ] = true;
			$words[ preg_replace( '/^[\x{05D5}\x{05D4}\x{05D1}\x{05DC}\x{05DE}\x{05E9}\x{05DB}]{2}/u', '', $w ) ] = true;
		}
	}
	$low   = ' ' . implode( ' ', array_keys( $words ) ) . ' ';
	$found = array();
	foreach ( nl_drop_claim_groups() as $g => $list ) {
		foreach ( $list as $w ) {
			$hit = strpos( $w, ' ' ) !== false ? strpos( $low, ' ' . $w . ' ' ) !== false : isset( $words[ $w ] );
			if ( $hit ) { $found[ $g ] = true; break; }
		}
	}
	return array_keys( $found );
}

function nl_drop_allowed_numbers( $f, $text ) {
	$a = nl_drop_nums_in_text( $text );
	foreach ( array( 'rooms', 'size_sqm', 'balcony_sqm', 'garden_sqm', 'floor', 'total_floors', 'parking_count', 'price' ) as $k ) {
		if ( isset( $f[ $k ] ) && $f[ $k ] !== null && $f[ $k ] !== '' ) { $a[] = (float) $f[ $k ]; }
	}
	if ( ! empty( $f['price'] ) && ! empty( $f['size_sqm'] ) ) { $a[] = round( (float) $f['price'] / (float) $f['size_sqm'] ); }
	return $a;
}

/* =====================================================================================================
 * The model call (JSON out). Uses the site's own keys; Claude when the site is set to Anthropic.
 * ===================================================================================================== */
function nl_drop_parse_json( $txt ) {
	$txt = trim( (string) $txt );
	$txt = preg_replace( '/^```(?:json)?\s*|\s*```$/m', '', $txt );
	$a   = strpos( $txt, '{' );
	$b   = strrpos( $txt, '}' );
	if ( $a === false || $b === false || $b < $a ) { return null; }
	$j = json_decode( substr( $txt, $a, $b - $a + 1 ), true );
	return is_array( $j ) ? $j : null;
}

function nl_drop_llm_json( $system, $user, $max_tokens, &$err = null ) {
	$user = function_exists( 'mb_substr' ) ? mb_substr( (string) $user, 0, 6000 ) : substr( (string) $user, 0, 6000 );
	if ( defined( 'NADLAN_DISABLE_AI' ) && NADLAN_DISABLE_AI ) { $err = 'disabled'; return null; }
	$cap  = (int) get_option( 'nadlan_ai_daily_token_cap_global', 200000 );
	$cap  = $cap < 10000 ? 200000 : $cap;
	$used = (int) get_option( 'nadlan_ai_tokens_today_' . gmdate( 'Ymd' ), 0 );
	if ( $used > $cap ) { $err = 'budget'; return null; }
	$prov = (string) get_option( 'nl_drop_provider', function_exists( 'nadlan_ai_provider' ) ? nadlan_ai_provider() : 'openai' );
	$akey = function_exists( 'nadlan_ai_anthropic_key' ) ? (string) nadlan_ai_anthropic_key() : '';
	$okey = function_exists( 'nadlan_ai_openai_key' ) ? (string) nadlan_ai_openai_key() : '';
	if ( $prov === 'anthropic' && $akey !== '' ) {
		$model = (string) get_option( 'nl_drop_anthropic_model', 'claude-sonnet-5' );
		$resp  = wp_remote_post( 'https://api.anthropic.com/v1/messages', array(
			'timeout' => 90,
			'headers' => array( 'x-api-key' => $akey, 'anthropic-version' => '2023-06-01', 'content-type' => 'application/json' ),
			'body'    => wp_json_encode( array(
				'model'      => $model,
				'max_tokens' => (int) $max_tokens,
				'system'     => (string) $system,
				'messages'   => array( array( 'role' => 'user', 'content' => (string) $user ) ),
			), JSON_UNESCAPED_UNICODE ),
		) );
		if ( is_wp_error( $resp ) ) { $err = $resp->get_error_message(); return null; }
		$code = (int) wp_remote_retrieve_response_code( $resp );
		$data = json_decode( wp_remote_retrieve_body( $resp ), true );
		if ( $code < 200 || $code >= 300 || ! is_array( $data ) ) { $err = 'http_' . $code; return null; }
		$txt = '';
		foreach ( (array) ( $data['content'] ?? array() ) as $blk ) {
			if ( ( $blk['type'] ?? '' ) === 'text' ) { $txt .= (string) $blk['text']; }
		}
		if ( function_exists( 'nadlan_ai_record_usage' ) ) { nadlan_ai_record_usage( 'anthropic', $model, (array) ( $data['usage'] ?? array() ), 0, 'ok' ); }
		$j = nl_drop_parse_json( $txt );
		if ( ! is_array( $j ) ) { $err = 'badjson'; }
		return $j;
	}
	if ( $okey === '' ) { $err = 'nokey'; return null; }
	$models = array_values( array_unique( array( (string) get_option( 'nl_drop_openai_model', 'gpt-4.1' ), 'gpt-4o', 'gpt-4o-mini' ) ) );
	foreach ( $models as $model ) {
		$resp = wp_remote_post( 'https://api.openai.com/v1/chat/completions', array(
			'timeout' => 90,
			'headers' => array( 'Authorization' => 'Bearer ' . $okey, 'Content-Type' => 'application/json' ),
			'body'    => wp_json_encode( array(
				'model'           => $model,
				'store'           => false,
				'temperature'     => 0.2,
				'max_tokens'      => (int) $max_tokens,
				'response_format' => array( 'type' => 'json_object' ),
				'messages'        => array(
					array( 'role' => 'system', 'content' => (string) $system ),
					array( 'role' => 'user', 'content' => (string) $user ),
				),
			), JSON_UNESCAPED_UNICODE ),
		) );
		if ( is_wp_error( $resp ) ) { $err = $resp->get_error_message(); continue; }
		$code = (int) wp_remote_retrieve_response_code( $resp );
		$data = json_decode( wp_remote_retrieve_body( $resp ), true );
		if ( $code >= 200 && $code < 300 && is_array( $data ) ) {
			if ( function_exists( 'nadlan_ai_record_usage' ) ) { nadlan_ai_record_usage( 'openai', $model, (array) ( $data['usage'] ?? array() ), 0, 'ok' ); }
			$j = nl_drop_parse_json( (string) ( $data['choices'][0]['message']['content'] ?? '' ) );
			if ( is_array( $j ) ) { return $j; }
			$err = 'badjson';
			continue;
		}
		$err = 'http_' . $code . ':' . $model;
		if ( $code === 401 || $code === 429 ) { break; }
	}
	return null;
}

/* =====================================================================================================
 * Step 1: read the facts. Only what the broker wrote survives.
 * ===================================================================================================== */
function nl_drop_extract_prompt() {
	return <<<'NLPROMPT'
You read ONE message that an Israeli real-estate broker wrote about ONE property, in Hebrew or English, often informal. Return ONLY a JSON object with exactly these keys:
listing_type ("sale" or "rent" or null), property_type ("apartment", "penthouse", "mini_penthouse", "garden", "duplex", "villa", "cottage", "studio", "other" or null), exclusive (true or false),
city_he, city_en, area_he, area_en, street_he,
rooms, size_sqm, balcony_sqm, garden_sqm, floor, total_floors, price, parking_count,
parking, storage, elevator, protected_room, ac, furnished (each true, false or null),
condition ("new", "renovated", "good", "needs_renovation" or null),
entry_he, entry_en, view_he, view_en, features_he (array), features_en (array), notes_he, notes_en.

Rules, all strict:
1. Use null whenever the message does not say it. Never guess, never fill a typical value, never infer a number.
2. Every number you return must be written in the message. You may convert only units that are written: "4.2 מיליון" is 4200000, "15 אלף" is 15000, "4,650,000" is 4650000.
3. listing_type: "sale" when the message sells (למכירה, מחיר, מיליון, for sale); "rent" when it rents (להשכרה, לחודש, שכ"ד, for rent). null if neither is clear.
4. price: the asking price in NIS for a sale, or the monthly rent for a rental. Only if written.
5. floor: 0 for a ground floor only if the message says קרקע or ground. "5 מתוך 8" means floor 5 and total_floors 8.
6. exclusive: true only if the message says בלעדיות, בבלעדיות, בלעדי or exclusive.
7. area_he: the neighborhood or area exactly as written in the message. area_en: its usual English spelling (Tzukei Aviv, Nofei Yam, Kochav HaTzafon, Ramat Aviv HaHadasha, Herzliya Pituach, Sarona, Neve Tzedek, Old North, Bavli, Florentin). city_he and city_en: only if written, or if the neighborhood is unmistakably inside one city (נופי ים, צוקי אביב, כוכב הצפון, רמת אביב, שרונה, בבלי are in תל אביב-יפו / Tel Aviv-Yafo; הרצליה פיתוח is in הרצליה / Herzliya).
8. street_he: only if a street is written. It is kept private and never published.
9. parking_count: only if a number of parking spaces is written. parking: true if parking is mentioned at all.
10. features_he: up to 8 short items taken from the message (materials, brands, systems, facilities, what the balcony faces), each under 40 characters, in Hebrew, with no praise words the message does not use. features_en: the same items in English, in the same order.
11. view_he and view_en: only if the message says what is seen (ים or sea, פארק or park, העיר or the city).
12. entry_he: as written (מיידית, 1.10, גמיש). entry_en: the same in English (Immediate, 1 October, Flexible).
13. notes_he and notes_en: other facts from the message that a buyer or tenant needs (a tenant in place, payment terms, building services), under 300 characters, or null.
Output JSON only.
NLPROMPT;
}

function nl_drop_extract( $text, $b, &$err = null ) {
	$sys = nl_drop_extract_prompt();
	if ( ! empty( $b['areas'] ) ) { $sys .= "\nThis broker usually works in: " . implode( ', ', $b['areas'] ) . '. Use this only to spell an area the message names, never to add one.'; }
	$j = nl_drop_llm_json( $sys, $text, 1100, $err );
	$f = is_array( $j ) ? $j : nl_drop_extract_basic( $text );
	return nl_drop_clean_facts( $f, $text );
}

/** Used only when no model is available: the plainest reading of the message. */
function nl_drop_extract_basic( $text ) {
	$t = (string) $text;
	$f = array();
	if ( preg_match( '/להשכרה|לחודש|שכ"ד|שכ״ד|for rent/iu', $t ) ) { $f['listing_type'] = 'rent'; }
	elseif ( preg_match( '/למכירה|מיליון|מליון|for sale/iu', $t ) ) { $f['listing_type'] = 'sale'; }
	if ( preg_match( '/(\d+(?:\.\d)?)\s*(?:חדרים|חד׳|חד\'|חד\b|rooms)/u', $t, $m ) ) { $f['rooms'] = (float) $m[1]; }
	if ( preg_match( '/(\d{2,4})\s*(?:מ״ר|מ"ר|מטר|sqm|m2)/u', $t, $m ) ) { $f['size_sqm'] = (int) $m[1]; }
	if ( preg_match( '/קומה\s*(\d+)(?:\s*(?:מתוך|מ-)\s*(\d+))?/u', $t, $m ) ) { $f['floor'] = (int) $m[1]; if ( ! empty( $m[2] ) ) { $f['total_floors'] = (int) $m[2]; } }
	if ( preg_match( '/מרפסת[^\d]{0,12}(\d{1,3})\s*(?:מ״ר|מ"ר|מטר)/u', $t, $m ) ) { $f['balcony_sqm'] = (int) $m[1]; }
	$max = 0;
	foreach ( nl_drop_nums_in_text( $t ) as $n ) { if ( $n >= 1000 && $n > $max ) { $max = $n; } }
	if ( $max ) { $f['price'] = (int) $max; }
	if ( preg_match( '/בלעדי/u', $t ) ) { $f['exclusive'] = true; }
	foreach ( array( 'חניה' => 'parking', 'חנייה' => 'parking', 'מחסן' => 'storage', 'מעלית' => 'elevator', 'ממ״ד' => 'protected_room', 'ממ"ד' => 'protected_room', 'מרוהט' => 'furnished' ) as $w => $k ) {
		if ( strpos( $t, $w ) !== false ) { $f[ $k ] = true; }
	}
	return $f;
}

function nl_drop_clean_facts( $j, $text ) {
	$nums = nl_drop_nums_in_text( $text );
	$norm = nl_drop_norm( $text );
	$str  = function ( $v, $max ) {
		if ( ! is_string( $v ) && ! is_numeric( $v ) ) { return null; }
		$v = trim( wp_strip_all_tags( (string) $v ) );
		if ( $v === '' || strtolower( $v ) === 'null' ) { return null; }
		return function_exists( 'mb_substr' ) ? mb_substr( $v, 0, $max ) : substr( $v, 0, $max );
	};
	$bool = function ( $v ) {
		if ( $v === true || $v === 'true' || $v === 1 || $v === '1' ) { return true; }
		if ( $v === false || $v === 'false' || $v === 0 || $v === '0' ) { return false; }
		return null;
	};
	$f = array();
	$f['listing_type']  = in_array( $j['listing_type'] ?? null, array( 'sale', 'rent' ), true ) ? $j['listing_type'] : null;
	$types              = array( 'apartment', 'penthouse', 'mini_penthouse', 'garden', 'duplex', 'villa', 'cottage', 'studio', 'other' );
	$f['property_type'] = in_array( $j['property_type'] ?? null, $types, true ) ? $j['property_type'] : null;
	$f['exclusive']     = $bool( $j['exclusive'] ?? false ) === true && preg_match( '/בלעדי|exclusive/iu', (string) $text );
	foreach ( array( 'rooms' => 30, 'size_sqm' => 5000, 'balcony_sqm' => 2000, 'garden_sqm' => 20000, 'floor' => 120, 'total_floors' => 120, 'price' => 500000000, 'parking_count' => 20 ) as $k => $max ) {
		$v = $j[ $k ] ?? null;
		if ( ! is_numeric( $v ) ) { $f[ $k ] = null; continue; }
		$v = (float) $v;
		if ( $v < 0 || $v > $max ) { $f[ $k ] = null; continue; }
		if ( $k === 'floor' && $v == 0 ) { $f[ $k ] = preg_match( '/קרקע|ground/iu', (string) $text ) ? 0 : null; continue; }
		$f[ $k ] = nl_drop_num_ok( $v, $nums ) ? ( in_array( $k, array( 'rooms' ), true ) ? $v : (int) round( $v ) ) : null;
	}
	if ( $f['total_floors'] !== null && $f['floor'] !== null && $f['total_floors'] < $f['floor'] ) { $f['total_floors'] = null; }
	foreach ( array( 'parking', 'storage', 'elevator', 'protected_room', 'ac', 'furnished' ) as $k ) { $f[ $k ] = $bool( $j[ $k ] ?? null ); }
	if ( $f['parking_count'] ) { $f['parking'] = true; }
	$f['condition'] = in_array( $j['condition'] ?? null, array( 'new', 'renovated', 'good', 'needs_renovation' ), true ) ? $j['condition'] : null;
	foreach ( array( 'city_he' => 60, 'city_en' => 60, 'area_he' => 60, 'area_en' => 60, 'street_he' => 80, 'entry_he' => 60, 'entry_en' => 60, 'view_he' => 60, 'view_en' => 60, 'notes_he' => 320, 'notes_en' => 320 ) as $k => $max ) {
		$f[ $k ] = $str( $j[ $k ] ?? null, $max );
	}
	foreach ( array( 'city_he', 'area_he', 'street_he', 'entry_he', 'view_he', 'notes_he' ) as $k ) {
		if ( $f[ $k ] !== null ) { $f[ $k ] = nl_drop_he_typo( $f[ $k ] ); }
	}
	// the area must be written in the message; a city may follow from a named neighborhood
	if ( $f['area_he'] !== null && strpos( $norm, nl_drop_norm( $f['area_he'] ) ) === false ) { $f['area_he'] = null; $f['area_en'] = null; }
	if ( $f['area_he'] === null && $f['area_en'] !== null && strpos( $norm, nl_drop_norm( $f['area_en'] ) ) === false ) { $f['area_en'] = null; }
	if ( $f['view_he'] !== null && strpos( $norm, nl_drop_norm( $f['view_he'] ) ) === false && ! preg_match( '/נוף|ים|view|sea/iu', (string) $text ) ) { $f['view_he'] = null; $f['view_en'] = null; }
	foreach ( array( 'features_he', 'features_en' ) as $k ) {
		$list = array();
		foreach ( (array) ( $j[ $k ] ?? array() ) as $item ) {
			$item = $str( $item, 60 );
			if ( $item === null ) { continue; }
			$ok = true;
			foreach ( nl_drop_nums_in_copy( $item ) as $n ) { if ( ! nl_drop_num_ok( $n, $nums ) ) { $ok = false; } }
			if ( $ok ) { $list[] = $k === 'features_he' ? nl_drop_he_typo( $item ) : $item; }
			if ( count( $list ) >= 8 ) { break; }
		}
		$f[ $k ] = $list;
	}
	foreach ( array( 'notes_he', 'notes_en', 'entry_he', 'entry_en' ) as $k ) {
		if ( $f[ $k ] === null ) { continue; }
		foreach ( nl_drop_nums_in_copy( $f[ $k ] ) as $n ) { if ( ! nl_drop_num_ok( $n, $nums ) ) { $f[ $k ] = null; break; } }
	}
	return $f;
}

/** What still stops a page from being built. Hebrew, for the broker's screen. */
function nl_drop_missing( $f, $photos ) {
	$miss = array();
	if ( empty( $f['listing_type'] ) ) { $miss[] = 'למכירה או להשכרה'; }
	if ( empty( $f['area_he'] ) && empty( $f['city_he'] ) ) { $miss[] = 'שכונה או עיר'; }
	if ( empty( $f['rooms'] ) && empty( $f['size_sqm'] ) ) { $miss[] = 'מספר חדרים או שטח במ״ר'; }
	if ( empty( $photos ) ) { $miss[] = 'לפחות תמונה אחת'; }
	return $miss;
}

function nl_drop_summary( $f ) {
	$p = array();
	if ( ! empty( $f['listing_type'] ) ) { $p[] = nl_drop_t( 'he', $f['listing_type'] ); }
	if ( ! empty( $f['property_type'] ) && $f['property_type'] !== 'other' ) { $p[] = nl_drop_type_label( $f['property_type'], 'he' ); }
	if ( ! empty( $f['rooms'] ) ) { $p[] = sprintf( nl_drop_t( 'he', 'rooms_n' ), nl_drop_fmt_num( $f['rooms'] ) ); }
	if ( ! empty( $f['size_sqm'] ) ) { $p[] = sprintf( nl_drop_t( 'he', 'size_n' ), nl_drop_fmt_int( $f['size_sqm'] ) ); }
	$place = trim( implode( ', ', array_filter( array( $f['area_he'] ?? '', $f['city_he'] ?? '' ) ) ) );
	if ( $place !== '' ) { $p[] = $place; }
	$p[] = ! empty( $f['price'] ) ? nl_drop_price_text( $f['price'], 'he' ) : 'מחיר בפנייה';
	return implode( ' · ', $p );
}

/* =====================================================================================================
 * Step 2: write the page. Hebrew first, English as its faithful translation. Gated field by field.
 * ===================================================================================================== */
function nl_drop_write_prompt( $b ) {
	$p = <<<'NLPROMPT'
You write the listing page for ONE property on the website of an Israeli luxury real-estate broker. You receive FACTS (JSON, already checked against the broker's words) and the broker's own MESSAGE. Write in Hebrew and in English. Return ONLY a JSON object {"he": {...}, "en": {...}} where each has exactly these keys:
title, card_title, dek, story_h2, story, features, chips, card_hi, seo_title, seo_desc.

Hard rules. A field that breaks one is thrown away:
1. Use only what is in FACTS and MESSAGE. Do not add a view, a direction, a floor, a facility, a distance, a year, a building name, a material or a number that is not there. The examples below show the style only; never copy their facts.
2. Wherever you state the price or the rent, write the token {{PRICE}} exactly, never the number. If FACTS.price is null, do not mention the price at all.
3. Never mention the street or the address. Never mention the broker, a licence, a listing site, a portal or a source.
4. No exclamation marks. No long dashes; use a comma or a colon. No hype: no הזדמנות, חלום, מושלם, מדהים, חוויה, and no "once in a lifetime", "dream", "stunning", "breathtaking".
5. Specific details beat adjectives. Quiet, precise sentences, the way a top Tel Aviv broker writes to a private client.
6. Numbers as digits, exactly as in FACTS (110 מ״ר, 4.5 חדרים, קומה 5 מתוך 8; 110 sqm, 4.5 rooms, floor 5 of 8).

Fields (English is a faithful translation of the Hebrew):
- title: [type or rooms] [what is rare], [area]. Max 60 characters. Style: "3 חדרים עם מרפסת של 20 מ״ר ו-2 חניות, נופי ים" / "Three Rooms with a 20 sqm Balcony, Nofei Yam".
- card_title: a shorter title for a card, max 45 characters, without the area.
- dek: 25 to 45 words. Order: location, what is rare, two or three facts, then {{PRICE}} if there is a price. Style: "בקומה 5 בבניין בוטיק ברמת אביב: 4 חדרים על 110 מ״ר, מרפסת של 12 מ״ר, חניה ומחסן. {{PRICE}}."
- story_h2: a short heading for the home, max 50 characters.
- story: an array of 2 or 3 short paragraphs. First the home (layout, rooms, balcony, what it faces only if given). Then the finish and systems, only if given. Then the building and the surroundings, only if given. If there is little to say, write 2 short paragraphs, never padding.
- features: 4 to 6 pairs [short bold line, short second line], each from the facts.
- chips: 2 very short facts, max 28 characters each.
- card_hi: 3 short highlights for a card, max 40 characters each.
- seo_title: max 65 characters, holds the property type or rooms, the deal (למכירה or להשכרה; for Sale or for Rent) and the area.
- seo_desc: max 155 characters, the key facts, {{PRICE}} if there is a price.

Typography and words:
- Hebrew uses gershayim and geresh: מ״ר, ממ״ד, ש״ח, ג׳קוזי. Never a plain quote mark inside a Hebrew word.
- English: "lift" (not elevator), "safe room" (not protected room), "sqm", "floor 5 of 7".
- features: the bold line is the fact itself, the second line is its context from the MESSAGE. If the MESSAGE gives no context, the second line is "" (empty). Never pad: no "high-quality finish", "advanced systems", "access from the living room", "Yes", "כן".
- Descriptive words are claims. sea, view, quiet, bright, spacious, new, renovated, boutique, designer, luxury, and their Hebrew forms, may appear only if the MESSAGE says so.

A worked example about a DIFFERENT property. Copy the voice and the structure, never its facts:
MESSAGE: "להשכרה בבלעדיות: 3 חדרים 90 מ"ר, מרפסת 20 מ"ר לשטח פתוח, קומה 5 מתוך 7, בניין על עמודים עם מעלית, ממ"ד, 2 חניות נפרדות ומחסן גדול ליד החניה. 9,500 לחודש, כניסה 1.10 גמיש. נופי ים."
OUTPUT he: title "3 חדרים עם מרפסת של 20 מ״ר ו-2 חניות, נופי ים"; card_title "3 חדרים עם מרפסת של 20 מ״ר"; dek "בקומה 5 מתוך 7 בנופי ים: 3 חדרים על 90 מ״ר עם מרפסת של 20 מ״ר לשטח פתוח, ממ״ד, 2 חניות נפרדות ומחסן גדול. {{PRICE}} לחודש."; story_h2 "3 חדרים ומרפסת של 20 מ״ר בנופי ים"; story ["3 חדרים על 90 מ״ר, מרפסת של 20 מ״ר הפונה לשטח פתוח, וממ״ד, בקומה 5 בבניין בן 7 קומות על עמודים עם מעלית.", "לדירה 2 חניות נפרדות ומחסן גדול ליד החניה. שכר הדירה {{PRICE}} לחודש, והכניסה ב-1.10 בגמישות."]; features [["90 מ״ר ומרפסת של 20 מ״ר", "3 חדרים"], ["ממ״ד בתוך הדירה", "מרחב מוגן דירתי"], ["2 חניות נפרדות", "ומחסן גדול ליד החניה"], ["קומה 5 מתוך 7", "בניין על עמודים עם מעלית"]]; chips ["ממ״ד, 2 חניות ומחסן", "כניסה ב-1.10, גמיש"]; card_hi ["מרפסת לשטח פתוח", "מחסן גדול ליד החניה", "בניין על עמודים עם מעלית"]; seo_title "דירת 3 חדרים להשכרה בנופי ים, מרפסת 20 מ״ר ו-2 חניות".
OUTPUT en: title "Three Rooms with a 20 sqm Balcony and Two Parking Spaces, Nofei Yam"; dek "On floor 5 of 7 in Nofei Yam: three rooms on 90 sqm with a 20 sqm balcony facing an open area, a safe room, two separate parking spaces and a large storage room. {{PRICE}} a month."; features [["90 sqm plus a 20 sqm balcony", "Three rooms"], ["Safe room inside the unit", "An in-apartment protected room"], ["Two separate parking spaces", "And a large storage room by the parking"], ["Floor 5 of 7", "A building on pillars with a lift"]].
NLPROMPT;
	return $p;
}

function nl_drop_write( $f, $text, $b, &$err = null ) {
	$pub = $f;
	unset( $pub['street_he'] );
	$user = wp_json_encode( array( 'FACTS' => $pub, 'MESSAGE' => (string) $text ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
	$j    = nl_drop_llm_json( nl_drop_write_prompt( $b ), $user, 2600, $err );
	return nl_drop_finish_copy( is_array( $j ) ? $j : array(), $f, $text );
}

function nl_drop_finish_copy( $j, $f, $text ) {
	$allowed = nl_drop_allowed_numbers( $f, $text );
	$names   = array_values( array_filter( array( $f['area_he'] ?? '', $f['area_en'] ?? '', $f['city_he'] ?? '', $f['city_en'] ?? '' ) ) );
	$msg     = (string) $text;
	foreach ( $names as $nm ) { $msg = str_ireplace( $nm, ' ', $msg ); }
	$stated  = nl_drop_claims_in( $msg . ' ' . implode( ' ', array_merge( (array) ( $f['features_he'] ?? array() ), (array) ( $f['features_en'] ?? array() ) ) ) . ' ' . ( $f['view_he'] ?? '' ) . ' ' . ( $f['view_en'] ?? '' ) . ' ' . ( $f['notes_he'] ?? '' ) . ' ' . ( $f['notes_en'] ?? '' ) );
	if ( ! empty( $f['garden_sqm'] ) ) { $stated[] = 'garden'; }
	$out     = array();
	$caps    = array( 'title' => 90, 'card_title' => 70, 'dek' => 460, 'story_h2' => 80, 'seo_title' => 90, 'seo_desc' => 200 );
	foreach ( array( 'he', 'en' ) as $lang ) {
		$src = isset( $j[ $lang ] ) && is_array( $j[ $lang ] ) ? $j[ $lang ] : array();
		$tpl = nl_drop_tpl( $f, $lang );
		$c   = array();
		$fix = function ( $s ) use ( $f, $lang ) {
			$s = trim( wp_strip_all_tags( (string) $s ) );
			if ( ! empty( $f['price'] ) ) {
				$num = preg_quote( nl_drop_fmt_int( $f['price'] ), '/' );
				$raw = preg_quote( (string) (int) $f['price'], '/' );
				$s   = preg_replace( '/(?:NIS\s*|₪\s*)?(?<![\d,.])(?:' . $num . '|' . $raw . ')(?!\d|,\d|\.\d)(?:\s*(?:ש״ח|ש"ח|₪|שקלים|NIS))?/u', '{{PRICE}}', $s );
			}
			$s = preg_replace( '/\s+/u', ' ', $s );
			return $lang === 'he' ? nl_drop_he_typo( $s ) : $s;
		};
		$ok = function ( $s ) use ( $lang, $allowed, $stated, $names ) { return $s !== '' && ! nl_drop_gate_str( $s, $lang, $allowed, $stated, $names ); };
		foreach ( $caps as $k => $max ) {
			$v   = $fix( $src[ $k ] ?? '' );
			$v   = function_exists( 'mb_substr' ) ? mb_substr( $v, 0, $max ) : substr( $v, 0, $max );
			$c[ $k ] = $ok( $v ) ? $v : $tpl[ $k ];
		}
		$story = array();
		foreach ( array_slice( (array) ( $src['story'] ?? array() ), 0, 3 ) as $para ) {
			$para = $fix( $para );
			if ( $ok( $para ) ) { $story[] = function_exists( 'mb_substr' ) ? mb_substr( $para, 0, 800 ) : $para; }
		}
		$c['story'] = count( $story ) >= 1 ? $story : $tpl['story'];
		$feat = array();
		foreach ( array_slice( (array) ( $src['features'] ?? array() ), 0, 6 ) as $pair ) {
			$pair = array_values( (array) $pair );
			$bo   = $fix( $pair[0] ?? '' );
			$sm   = $fix( $pair[1] ?? '' );
			if ( $sm !== '' && ( ! $ok( $sm ) || in_array( nl_drop_norm( $sm ), array( 'כן', 'yes', 'יש', 'included' ), true ) ) ) { $sm = ''; }
			if ( $ok( $bo ) ) { $feat[] = array( $bo, $sm ); }
		}
		$c['features'] = count( $feat ) >= 3 ? $feat : $tpl['features'];
		foreach ( array( 'chips' => array( 2, 40 ), 'card_hi' => array( 3, 60 ) ) as $k => $lim ) {
			$list = array();
			foreach ( array_slice( (array) ( $src[ $k ] ?? array() ), 0, $lim[0] ) as $s ) {
				$s = $fix( $s );
				if ( $ok( $s ) ) { $list[] = function_exists( 'mb_substr' ) ? mb_substr( $s, 0, $lim[1] ) : $s; }
			}
			$c[ $k ] = $list ? $list : $tpl[ $k ];
		}
		$out[ $lang ] = $c;
	}
	return $out;
}

/** The plain version: used field by field whenever the model is unavailable or a field fails the gate. */
function nl_drop_tpl( $f, $lang ) {
	$he    = $lang !== 'en';
	$deal  = ( $f['listing_type'] ?? '' ) === 'rent' ? 'rent' : 'sale';
	$area  = $he ? ( $f['area_he'] ?: ( $f['city_he'] ?: '' ) ) : ( $f['area_en'] ?: ( $f['city_en'] ?: '' ) );
	$city  = $he ? ( $f['city_he'] ?? '' ) : ( $f['city_en'] ?? '' );
	$type  = $f['property_type'] ?: '';
	$rooms = ! empty( $f['rooms'] ) ? nl_drop_fmt_num( $f['rooms'] ) : '';
	$plain = in_array( $type, array( '', 'apartment', 'other' ), true );
	if ( $he ) {
		$head = $rooms !== '' ? ( $plain ? $rooms . ' חדרים' : nl_drop_type_label( $type, 'he' ) . ' ' . $rooms . ' חדרים' ) : nl_drop_type_label( $type ?: 'other', 'he' );
		$rare = ! empty( $f['balcony_sqm'] ) ? ' עם מרפסת של ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' מ״ר' : ( ! empty( $f['garden_sqm'] ) ? ' עם גינה של ' . nl_drop_fmt_int( $f['garden_sqm'] ) . ' מ״ר' : '' );
		$bits = array();
		if ( ! empty( $f['size_sqm'] ) ) { $bits[] = ( $rooms !== '' ? $rooms . ' חדרים על ' : '' ) . nl_drop_fmt_int( $f['size_sqm'] ) . ' מ״ר'; }
		elseif ( $rooms !== '' ) { $bits[] = $rooms . ' חדרים'; }
		if ( ! empty( $f['balcony_sqm'] ) ) { $bits[] = 'מרפסת של ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' מ״ר'; }
		if ( isset( $f['floor'] ) && $f['floor'] !== null ) { $bits[] = $f['floor'] == 0 ? 'קומת קרקע' : 'קומה ' . (int) $f['floor'] . ( ! empty( $f['total_floors'] ) ? ' מתוך ' . (int) $f['total_floors'] : '' ); }
		if ( ! empty( $f['parking_count'] ) ) { $bits[] = $f['parking_count'] > 1 ? (int) $f['parking_count'] . ' חניות' : 'חניה'; }
		elseif ( ! empty( $f['parking'] ) ) { $bits[] = 'חניה'; }
		if ( ! empty( $f['storage'] ) ) { $bits[] = 'מחסן'; }
		if ( ! empty( $f['protected_room'] ) ) { $bits[] = 'ממ״ד'; }
		$place = trim( $area . ( $city && $city !== $area ? ', ' . $city : '' ) );
		$dek   = ( $place !== '' ? $place . ': ' : '' ) . implode( ', ', $bits ) . '.';
		if ( ! empty( $f['price'] ) ) { $dek .= ' {{PRICE}}' . ( $deal === 'rent' ? ' לחודש' : '' ) . '.'; }
		$story = array( rtrim( $dek, '.' ) . '.' );
		if ( ! empty( $f['features_he'] ) ) { $story[] = 'בנכס: ' . implode( ', ', array_slice( $f['features_he'], 0, 6 ) ) . '.'; }
		if ( ! empty( $f['notes_he'] ) ) { $story[] = rtrim( $f['notes_he'], '.' ) . '.'; }
		$feat = array();
		if ( ! empty( $f['size_sqm'] ) ) { $feat[] = array( nl_drop_fmt_int( $f['size_sqm'] ) . ' מ״ר', $rooms !== '' ? $rooms . ' חדרים' : '' ); }
		if ( ! empty( $f['balcony_sqm'] ) ) { $feat[] = array( 'מרפסת של ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' מ״ר', $f['view_he'] ? 'נוף ל' . $f['view_he'] : '' ); }
		if ( isset( $f['floor'] ) && $f['floor'] !== null ) { $feat[] = array( $f['floor'] == 0 ? 'קומת קרקע' : 'קומה ' . (int) $f['floor'] . ( ! empty( $f['total_floors'] ) ? ' מתוך ' . (int) $f['total_floors'] : '' ), ! empty( $f['elevator'] ) ? 'עם מעלית' : '' ); }
		if ( ! empty( $f['parking'] ) || ! empty( $f['storage'] ) ) { $feat[] = array( trim( ( ! empty( $f['parking_count'] ) && $f['parking_count'] > 1 ? (int) $f['parking_count'] . ' חניות' : ( ! empty( $f['parking'] ) ? 'חניה' : '' ) ) . ( ! empty( $f['storage'] ) ? ( ! empty( $f['parking'] ) ? ' ומחסן' : 'מחסן' ) : '' ) ), 'צמודים לנכס' ); }
		if ( ! empty( $f['protected_room'] ) ) { $feat[] = array( 'ממ״ד', 'מרחב מוגן דירתי' ); }
		if ( ! empty( $f['entry_he'] ) ) { $feat[] = array( 'כניסה: ' . $f['entry_he'], '' ); }
		foreach ( array_slice( $f['features_he'] ?? array(), 0, max( 0, 6 - count( $feat ) ) ) as $x ) { $feat[] = array( $x, '' ); }
		$seo_head = $rooms !== '' ? ( $plain ? 'דירת ' . $rooms . ' חדרים' : nl_drop_type_label( $type, 'he' ) . ' ' . $rooms . ' חדרים' ) : nl_drop_type_label( $type ?: 'other', 'he' );
		return array(
			'title'      => $head . $rare . ( $area !== '' ? ', ' . $area : '' ),
			'card_title' => $head . $rare,
			'dek'        => $dek,
			'story_h2'   => $head . ( $area !== '' ? ' ב' . $area : '' ),
			'story'      => $story,
			'features'   => array_slice( $feat, 0, 6 ),
			'chips'      => array_slice( array_filter( array( ! empty( $f['size_sqm'] ) ? nl_drop_fmt_int( $f['size_sqm'] ) . ' מ״ר' : '', ! empty( $f['entry_he'] ) ? 'כניסה: ' . $f['entry_he'] : ( ! empty( $f['protected_room'] ) ? 'ממ״ד' : '' ) ) ), 0, 2 ),
			'card_hi'    => array_slice( array_merge( $f['features_he'] ?? array(), array_filter( array( ! empty( $f['storage'] ) ? 'מחסן' : '', ! empty( $f['elevator'] ) ? 'מעלית' : '' ) ) ), 0, 3 ),
			'seo_title'  => $seo_head . ' ' . nl_drop_t( 'he', $deal ) . ( $area !== '' ? ' ב' . $area : '' ),
			'seo_desc'   => function_exists( 'mb_substr' ) ? mb_substr( $dek, 0, 155 ) : $dek,
		);
	}
	$head = $rooms !== '' ? ( $plain ? $rooms . '-Room ' . ( $type === 'apartment' || $type === '' ? 'Apartment' : 'Home' ) : $rooms . '-Room ' . nl_drop_type_label( $type, 'en' ) ) : nl_drop_type_label( $type ?: 'other', 'en' );
	$rare = ! empty( $f['balcony_sqm'] ) ? ' with a ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' sqm Balcony' : ( ! empty( $f['garden_sqm'] ) ? ' with a ' . nl_drop_fmt_int( $f['garden_sqm'] ) . ' sqm Garden' : '' );
	$bits = array();
	if ( ! empty( $f['size_sqm'] ) ) { $bits[] = ( $rooms !== '' ? $rooms . ' rooms on ' : '' ) . nl_drop_fmt_int( $f['size_sqm'] ) . ' sqm'; }
	elseif ( $rooms !== '' ) { $bits[] = $rooms . ' rooms'; }
	if ( ! empty( $f['balcony_sqm'] ) ) { $bits[] = 'a ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' sqm balcony'; }
	if ( isset( $f['floor'] ) && $f['floor'] !== null ) { $bits[] = $f['floor'] == 0 ? 'ground floor' : 'floor ' . (int) $f['floor'] . ( ! empty( $f['total_floors'] ) ? ' of ' . (int) $f['total_floors'] : '' ); }
	if ( ! empty( $f['parking_count'] ) ) { $bits[] = $f['parking_count'] > 1 ? (int) $f['parking_count'] . ' parking spaces' : 'parking'; }
	elseif ( ! empty( $f['parking'] ) ) { $bits[] = 'parking'; }
	if ( ! empty( $f['storage'] ) ) { $bits[] = 'a storage room'; }
	if ( ! empty( $f['protected_room'] ) ) { $bits[] = 'a safe room'; }
	$place = trim( $area . ( $city && $city !== $area ? ', ' . $city : '' ) );
	$dek   = ( $place !== '' ? $place . ': ' : '' ) . implode( ', ', $bits ) . '.';
	if ( ! empty( $f['price'] ) ) { $dek .= ' {{PRICE}}' . ( $deal === 'rent' ? ' a month' : '' ) . '.'; }
	$story = array( $dek );
	if ( ! empty( $f['features_en'] ) ) { $story[] = 'The home includes ' . implode( ', ', array_slice( $f['features_en'], 0, 6 ) ) . '.'; }
	if ( ! empty( $f['notes_en'] ) ) { $story[] = rtrim( $f['notes_en'], '.' ) . '.'; }
	$feat = array();
	if ( ! empty( $f['size_sqm'] ) ) { $feat[] = array( nl_drop_fmt_int( $f['size_sqm'] ) . ' sqm', $rooms !== '' ? $rooms . ' rooms' : '' ); }
	if ( ! empty( $f['balcony_sqm'] ) ) { $feat[] = array( 'A ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' sqm balcony', $f['view_en'] ? 'Facing the ' . $f['view_en'] : '' ); }
	if ( isset( $f['floor'] ) && $f['floor'] !== null ) { $feat[] = array( $f['floor'] == 0 ? 'Ground floor' : 'Floor ' . (int) $f['floor'] . ( ! empty( $f['total_floors'] ) ? ' of ' . (int) $f['total_floors'] : '' ), ! empty( $f['elevator'] ) ? 'With a lift' : '' ); }
	if ( ! empty( $f['parking'] ) || ! empty( $f['storage'] ) ) { $feat[] = array( trim( ( ! empty( $f['parking_count'] ) && $f['parking_count'] > 1 ? (int) $f['parking_count'] . ' parking spaces' : ( ! empty( $f['parking'] ) ? 'Parking' : '' ) ) . ( ! empty( $f['storage'] ) ? ( ! empty( $f['parking'] ) ? ' and storage' : 'Storage' ) : '' ) ), 'Attached to the unit' ); }
	if ( ! empty( $f['protected_room'] ) ) { $feat[] = array( 'Safe room', 'An in-apartment protected room' ); }
	if ( ! empty( $f['entry_en'] ) ) { $feat[] = array( 'Entry: ' . $f['entry_en'], '' ); }
	foreach ( array_slice( $f['features_en'] ?? array(), 0, max( 0, 6 - count( $feat ) ) ) as $x ) { $feat[] = array( $x, '' ); }
	return array(
		'title'      => $head . $rare . ( $area !== '' ? ', ' . $area : '' ),
		'card_title' => $head . $rare,
		'dek'        => $dek,
		'story_h2'   => $head . ( $area !== '' ? ' in ' . $area : '' ),
		'story'      => $story,
		'features'   => array_slice( $feat, 0, 6 ),
		'chips'      => array_slice( array_filter( array( ! empty( $f['size_sqm'] ) ? nl_drop_fmt_int( $f['size_sqm'] ) . ' sqm' : '', ! empty( $f['entry_en'] ) ? 'Entry: ' . $f['entry_en'] : ( ! empty( $f['protected_room'] ) ? 'Safe room' : '' ) ) ), 0, 2 ),
		'card_hi'    => array_slice( array_merge( $f['features_en'] ?? array(), array_filter( array( ! empty( $f['storage'] ) ? 'Storage' : '', ! empty( $f['elevator'] ) ? 'Lift' : '' ) ) ), 0, 3 ),
		'seo_title'  => $head . ' ' . ( $deal === 'rent' ? 'for Rent' : 'for Sale' ) . ( $area !== '' ? ', ' . $area : '' ),
		'seo_desc'   => substr( $dek, 0, 155 ),
	);
}

/* =====================================================================================================
 * Latin slug: area, type, rooms, deal. No word twice. Never Hebrew.
 * ===================================================================================================== */
function nl_drop_slug( $f, $b ) {
	$latin = function ( $s ) {
		$s = strtolower( remove_accents( (string) $s ) );
		$s = preg_replace( '/[^a-z0-9]+/', '-', $s );
		return trim( $s, '-' );
	};
	$area  = $latin( $f['area_en'] ?? '' );
	if ( $area === '' ) { $area = $latin( $f['city_en'] ?? '' ); }
	$words = array();
	if ( $area !== '' ) { $words[] = $area; }
	$type = array( 'penthouse' => 'penthouse', 'mini_penthouse' => 'mini-penthouse', 'garden' => 'garden-apartment', 'duplex' => 'duplex', 'villa' => 'villa', 'cottage' => 'cottage', 'studio' => 'studio' );
	if ( isset( $type[ $f['property_type'] ?? '' ] ) ) { $words[] = $type[ $f['property_type'] ]; }
	if ( ! empty( $f['rooms'] ) ) { $words[] = str_replace( '.', '-', nl_drop_fmt_num( $f['rooms'] ) ) . '-rooms'; }
	$words[] = ( $f['listing_type'] ?? '' ) === 'rent' ? 'for-rent' : 'for-sale';
	$seen = array();
	$out  = array();
	foreach ( explode( '-', implode( '-', $words ) ) as $w ) {
		if ( $w === '' ) { continue; }
		if ( ! ctype_digit( $w ) && isset( $seen[ $w ] ) ) { continue; }
		$seen[ $w ] = 1;
		$out[]      = $w;
	}
	$slug = implode( '-', $out );
	if ( count( $out ) < 3 ) { $slug = 'property-' . $slug; }
	$base = $slug;
	for ( $i = 2; $i < 60; $i++ ) {
		$taken = get_page_by_path( $slug, OBJECT, 'nadlan_property' );
		if ( ! $taken && ! empty( $b['site_en'] ) ) { $taken = get_page_by_path( get_page_uri( (int) $b['site_en'] ) . '/' . $slug, OBJECT, 'page' ); }
		if ( ! $taken ) { break; }
		$slug = $base . '-' . $i;
	}
	return $slug;
}

/* =====================================================================================================
 * The listing page (same design and classes as the approved broker listing pages)
 * ===================================================================================================== */
function nl_drop_listing_css() {
	return <<<'NLXCSS'
.nlx{
  --nlx-paper:#F7F6F2; --nlx-surf:#FFFFFF; --nlx-ink:#14212B; --nlx-ink2:#3B4753; --nlx-mute:#6B7680;
  --nlx-line:#E3E1DA; --nlx-sea:#2F6F86; --nlx-seah:#255C70; --nlx-deep:#1F4B5C; --nlx-sand:#EEE9DD; --nlx-mist:#CFE3EA;
  --nlx-on-deep:#F7F6F2; --nlx-on-deep-2:rgba(247,246,242,.74); --nlx-on-deep-line:rgba(247,246,242,.18); --nlx-on-deep-fill:rgba(247,246,242,.08);
  --nlx-serif:'Noto Serif Hebrew','Noto Serif','David Libre',Georgia,serif;
  --nlx-sans:Assistant,'Segoe UI',Arial,sans-serif;
  --nlx-r:8px; --nlx-r-lg:22px;
  --nlx-shadow:0 8px 24px rgba(17,17,15,.07),0 2px 6px rgba(17,17,15,.04);
  color:var(--nlx-ink); font-family:var(--nlx-sans); font-size:17px; line-height:1.65;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
}
.nlx *,.nlx *::before,.nlx *::after{box-sizing:border-box}
.nlx :where(h1,h2,h3,h4,p,ul,ol,dl,dd,figure,table){margin:0;padding:0}
.nlx :where(ul,ol){list-style:none}
.nlx img{max-width:100%;height:auto;display:block}
.nlx a{color:var(--nlx-sea);text-decoration-thickness:1px;text-underline-offset:3px}
.nlx a:hover{color:var(--nlx-seah)}
.nlx :focus-visible{outline:2px solid var(--nlx-sea);outline-offset:3px;border-radius:4px}
.nlx .nlx-num{font-variant-numeric:tabular-nums lining-nums;font-feature-settings:"tnum" 1,"lnum" 1;direction:ltr;unicode-bidi:isolate;display:inline-block}
.nlx .nlx-wrap{max-width:1240px;margin-inline:auto;padding-inline:clamp(16px,3vw,32px)}
.nlx .nlx-sr{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.nlx.nlx .nlx-title,.nlx.nlx .nlx-h2,.nlx.nlx .nlx-h3,.nlx.nlx .nlx-serif{font-family:var(--nlx-serif)!important;font-weight:600!important;color:var(--nlx-ink)!important;letter-spacing:-.005em;text-wrap:balance}
.nlx.nlx .nlx-title{font-size:clamp(34px,4.4vw,56px);line-height:1.12}
.nlx.nlx .nlx-h2{font-size:clamp(26px,2.6vw,34px);line-height:1.2}
.nlx.nlx .nlx-h3{font-size:21px;line-height:1.3}
.nlx .nlx-kicker,.nlx .nlx-eyebrow{font-family:var(--nlx-sans)!important;font-size:13px;font-weight:700;letter-spacing:.04em;color:var(--nlx-sea);margin:0}
.nlx[lang="en"] .nlx-kicker,.nlx[lang="en"] .nlx-eyebrow{text-transform:uppercase;letter-spacing:.09em;font-size:12px}
.nlx.nlx .nlx-dek{font-family:var(--nlx-serif)!important;font-weight:500;font-size:clamp(19px,1.7vw,23px);line-height:1.55;color:var(--nlx-ink2);max-width:40ch}
.nlx .nlx-muted{color:var(--nlx-mute)}
.nlx .nlx-small{font-size:14px;line-height:1.55}
.nlx .nlx-chips{display:flex;flex-wrap:wrap;gap:8px}
.nlx .nlx-chip{display:inline-flex;align-items:center;gap:6px;padding:5px 12px;border-radius:999px;background:var(--nlx-sand);border:1px solid var(--nlx-line);color:var(--nlx-deep);font-size:14px;font-weight:600;line-height:1.3}
.nlx .nlx-chip--sea{background:var(--nlx-surf);border-color:var(--nlx-sea);color:var(--nlx-sea)}
.nlx .nlx-tag{display:inline-block;padding:1px 7px;border-radius:999px;font-size:11.5px;font-weight:700;line-height:1.6;letter-spacing:.02em;white-space:nowrap;vertical-align:middle;border:1px solid var(--nlx-line);color:var(--nlx-mute);background:var(--nlx-surf)}
.nlx .nlx-tag--broker{color:#5C5347;background:#F4EFE6;border-color:#E2D8C6}
.nlx .nlx-tag--calc{color:var(--nlx-ink2);background:var(--nlx-paper)}
.nlx .nlx-tag--src{color:var(--nlx-sea);border-color:#BFD6DE;background:#F2F8FA}
.nlx .nlx-tag--tx{color:#FFFFFF;background:var(--nlx-deep);border-color:var(--nlx-deep)}
.nlx sup.nlx-fn{font-size:11px;font-weight:700;margin-inline-start:2px;vertical-align:super;line-height:0}
.nlx sup.nlx-fn a{text-decoration:none}
.nlx .nlx-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:10px 20px;border-radius:999px;background:var(--nlx-sea);color:#fff!important;font-weight:700;font-size:16px;text-decoration:none!important;border:1px solid var(--nlx-sea);transition:background .15s ease}
.nlx .nlx-btn:hover{background:var(--nlx-seah);border-color:var(--nlx-seah)}
.nlx .nlx-btn--ghost{background:var(--nlx-surf);color:var(--nlx-deep)!important;border-color:var(--nlx-line)}
.nlx .nlx-btn--ghost:hover{background:var(--nlx-sand);border-color:var(--nlx-line)}
.nlx .nlx-btn svg{width:18px;height:18px;flex:none}
.nlx .nlx-mast{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(24px,4vw,56px);align-items:end;padding-block:clamp(24px,4vw,48px) clamp(20px,3vw,36px)}
.nlx .nlx-mast-copy{display:grid;gap:18px;align-content:end}
.nlx .nlx-plate{position:relative;aspect-ratio:4/3;max-width:100%;border-radius:var(--nlx-r);overflow:hidden;background:var(--nlx-sand);border:1px solid var(--nlx-line)}
.nlx .nlx-plate--rent{background:#E4EEF1}
.nlx .nlx-plate svg{position:absolute;inset:0;width:100%;height:100%}
.nlx .nlx-plate figcaption{position:absolute;inset-inline:14px;bottom:12px;font-size:13px;color:var(--nlx-ink2);background:rgba(255,255,255,.82);padding:6px 10px;border-radius:6px;line-height:1.4;max-width:calc(100% - 28px)}
.nlx .nlx-plate-name{position:absolute;inset-inline-start:22px;top:18px;font-family:var(--nlx-serif)!important;font-weight:600;font-size:clamp(22px,2.4vw,30px);color:var(--nlx-deep);line-height:1.2;max-width:70%}
.nlx .nlx-facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-block:1px solid var(--nlx-line)}
.nlx .nlx-fact{padding:18px 16px 16px;display:grid;gap:4px;align-content:start;border-inline-start:1px solid var(--nlx-line)}
.nlx .nlx-fact:first-child{border-inline-start:0}
.nlx .nlx-fact dt{font-size:13px;color:var(--nlx-mute);font-weight:600}
.nlx .nlx-fact dd{font-size:23px;font-weight:700;line-height:1.25;color:var(--nlx-ink)}
.nlx .nlx-fact dd .nlx-unit{font-size:15px;font-weight:600;color:var(--nlx-ink2);margin-inline-start:4px}
.nlx .nlx-fact .nlx-tag{justify-self:start}
.nlx .nlx-facts-note{display:flex;align-items:center;gap:8px;font-size:13.5px;color:var(--nlx-mute);padding-top:10px}
.nlx .nlx-money{white-space:nowrap}
.nlx .nlx-item-title{font-weight:600}
.nlx .nlx-spec-group h3 .nlx-tag{margin-inline-start:8px;letter-spacing:0}
.nlx .nlx-layout{display:grid;grid-template-columns:minmax(0,1fr) 352px;gap:clamp(32px,4.5vw,64px);align-items:start;padding-block:clamp(28px,4vw,48px)}
.nlx .nlx-main{min-width:0;display:grid;grid-template-columns:minmax(0,1fr);gap:0}
.nlx .nlx-main>*,.nlx .nlx-sec>*,.nlx .nlx-band>*,.nlx .nlx-band-grid>*,.nlx .nlx-two>*,.nlx .nlx-rail>*{min-width:0}
.nlx .nlx-rail{position:sticky;top:calc(var(--nlx-header-offset,96px) + env(safe-area-inset-top,0px));display:grid;gap:16px}
.nlx .nlx-card{background:var(--nlx-surf);border:1px solid var(--nlx-line);border-radius:var(--nlx-r);padding:22px}
.nlx .nlx-price-card{box-shadow:var(--nlx-shadow);display:grid;gap:14px}
.nlx .nlx-price-lbl{font-size:13px;font-weight:700;color:var(--nlx-mute);letter-spacing:.02em}
.nlx .nlx-price{font-size:clamp(30px,3vw,38px);font-weight:700;line-height:1.1;color:var(--nlx-ink)}
.nlx .nlx-price-sub{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:14px;color:var(--nlx-ink2)}
.nlx .nlx-price-rows{display:grid;gap:8px;border-top:1px solid var(--nlx-line);padding-top:14px}
.nlx .nlx-price-rows div{display:flex;justify-content:space-between;gap:12px;font-size:15px}
.nlx .nlx-price-rows dt{color:var(--nlx-mute)}
.nlx .nlx-price-rows dd{font-weight:700;text-align:end}
.nlx .nlx-cta{display:grid;gap:10px}
.nlx .nlx-agent-mini{display:grid;grid-template-columns:44px 1fr;gap:12px;align-items:center;font-size:14px;line-height:1.45}
.nlx .nlx-monogram{width:44px;height:44px;border-radius:50%;background:var(--nlx-deep);color:var(--nlx-on-deep);display:grid;place-items:center;font-family:var(--nlx-serif)!important;font-weight:600;font-size:18px}
.nlx .nlx-sec{padding-block:clamp(36px,4.5vw,56px);border-top:1px solid var(--nlx-line);display:grid;gap:22px;scroll-margin-top:96px}
.nlx .nlx-sec:first-child{border-top:0;padding-top:0}
.nlx .nlx-sec-head{display:grid;gap:8px;max-width:62ch}
.nlx .nlx-lead{font-size:18px;color:var(--nlx-ink2);max-width:64ch}
.nlx .nlx-prose{display:grid;gap:16px;max-width:66ch}
.nlx .nlx-prose p{font-size:18px;line-height:1.8;color:var(--nlx-ink)}
.nlx .nlx-toc{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:14.5px;font-weight:600;padding-block:14px;border-bottom:1px solid var(--nlx-line)}
.nlx .nlx-toc a{color:var(--nlx-ink2);text-decoration:none}
.nlx .nlx-toc a:hover{color:var(--nlx-sea)}
.nlx .nlx-features{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px}
.nlx .nlx-features li{padding:14px 0;border-top:1px solid var(--nlx-line);display:grid;gap:2px}
.nlx .nlx-features b{font-weight:700;color:var(--nlx-ink)}
.nlx .nlx-features span{color:var(--nlx-ink2);font-size:16px}
.nlx .nlx-spec{display:grid;gap:28px}
.nlx .nlx-spec-group{display:grid;gap:0}
.nlx .nlx-spec-group h3{font-family:var(--nlx-sans)!important;font-size:14px!important;font-weight:700!important;color:var(--nlx-mute)!important;letter-spacing:.03em;padding-bottom:8px}
.nlx .nlx-rows{display:grid}
.nlx .nlx-row{display:grid;grid-template-columns:minmax(120px,.8fr) minmax(0,1.6fr) auto;gap:6px 18px;padding:12px 0;border-top:1px solid var(--nlx-line);align-items:baseline}
.nlx .nlx-row dt{color:var(--nlx-ink2);font-weight:600;font-size:15.5px}
.nlx .nlx-row dd{color:var(--nlx-ink);font-size:16px}
.nlx .nlx-row .nlx-row-tag{justify-self:end}
.nlx .nlx-dist{display:grid}
.nlx .nlx-dist li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 16px;padding:12px 0;border-top:1px solid var(--nlx-line);align-items:center}
.nlx .nlx-dist .nlx-dist-name{font-weight:600}
.nlx .nlx-dist .nlx-dist-val{font-weight:700;text-align:end}
.nlx .nlx-dist .nlx-meter{grid-column:1/-1;height:4px;border-radius:4px;background:var(--nlx-sand);overflow:hidden}
.nlx .nlx-dist .nlx-meter i{display:block;height:100%;background:var(--nlx-sea);border-radius:4px}
.nlx .nlx-dist .nlx-dist-note{grid-column:1/-1;font-size:13.5px;color:var(--nlx-mute)}
.nlx .nlx-items{display:grid}
.nlx .nlx-item{padding:14px 0;border-top:1px solid var(--nlx-line);display:grid;gap:5px}
.nlx .nlx-item-top{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 14px}
.nlx .nlx-item-title{font-weight:700;color:var(--nlx-ink)}
.nlx .nlx-item p{font-size:15.5px;color:var(--nlx-ink2)}
.nlx .nlx-two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 40px}
.nlx .nlx-subhead{font-family:var(--nlx-sans)!important;font-size:15px!important;font-weight:700!important;color:var(--nlx-ink)!important;margin-bottom:4px}
.nlx .nlx-band{background:var(--nlx-deep);color:var(--nlx-on-deep);border-radius:var(--nlx-r-lg);padding:clamp(24px,4vw,48px);display:grid;gap:28px;margin-block:clamp(8px,2vw,16px)}
.nlx.nlx .nlx-band .nlx-h2,.nlx.nlx .nlx-band .nlx-h3,.nlx.nlx .nlx-band h2,.nlx.nlx .nlx-band h3{color:var(--nlx-on-deep)!important}
.nlx .nlx-band .nlx-eyebrow{color:var(--nlx-mist)}
.nlx .nlx-band p,.nlx .nlx-band li,.nlx .nlx-band dt,.nlx .nlx-band dd,.nlx .nlx-band span,.nlx .nlx-band td,.nlx .nlx-band th,.nlx .nlx-band small,.nlx .nlx-band label{color:var(--nlx-on-deep)}
.nlx .nlx-band .nlx-muted,.nlx .nlx-band .nlx-small{color:var(--nlx-on-deep-2)!important}
.nlx .nlx-band a{color:var(--nlx-mist)}
.nlx .nlx-band .nlx-tag{background:transparent;border-color:var(--nlx-on-deep-line);color:var(--nlx-on-deep-2)}
.nlx .nlx-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--nlx-on-deep-line);border:1px solid var(--nlx-on-deep-line);border-radius:var(--nlx-r);overflow:hidden}
.nlx .nlx-kpi{background:var(--nlx-deep);padding:18px;display:grid;gap:6px;align-content:start}
.nlx .nlx-kpi dt{font-size:13px;color:var(--nlx-on-deep-2)!important;font-weight:600}
.nlx .nlx-kpi dd{font-size:clamp(22px,2.2vw,28px);font-weight:700;line-height:1.15}
.nlx .nlx-kpi .nlx-small{font-size:13px}
.nlx .nlx-ledger{display:grid}
.nlx .nlx-ledger div{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 16px;padding:11px 0;border-top:1px solid var(--nlx-on-deep-line);align-items:baseline}
.nlx .nlx-ledger dt{font-size:15.5px}
.nlx .nlx-ledger dd{font-weight:700;text-align:end;font-size:16.5px}
.nlx .nlx-ledger .nlx-ledger-note{grid-column:1/-1;font-size:13px;color:var(--nlx-on-deep-2)!important}
.nlx .nlx-band-grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:clamp(24px,4vw,48px)}
.nlx .nlx-seg{display:grid;gap:14px}
.nlx .nlx-seg > input{position:absolute;opacity:0;pointer-events:none}
.nlx .nlx-seg-labels{display:flex;flex-wrap:wrap;gap:8px}
.nlx .nlx-seg-labels label{cursor:pointer;padding:8px 14px;border-radius:999px;border:1px solid var(--nlx-on-deep-line);font-size:14.5px;font-weight:700;color:var(--nlx-on-deep);background:transparent;line-height:1.3}
.nlx .nlx-seg-panel{display:none}
.nlx .nlx-seg > input:nth-of-type(1):checked ~ .nlx-seg-labels label:nth-of-type(1),
.nlx .nlx-seg > input:nth-of-type(2):checked ~ .nlx-seg-labels label:nth-of-type(2),
.nlx .nlx-seg > input:nth-of-type(3):checked ~ .nlx-seg-labels label:nth-of-type(3),
.nlx .nlx-seg > input:nth-of-type(4):checked ~ .nlx-seg-labels label:nth-of-type(4){background:var(--nlx-on-deep);color:var(--nlx-deep);border-color:var(--nlx-on-deep)}
.nlx .nlx-seg > input:nth-of-type(1):checked ~ .nlx-seg-panels .nlx-seg-panel:nth-of-type(1),
.nlx .nlx-seg > input:nth-of-type(2):checked ~ .nlx-seg-panels .nlx-seg-panel:nth-of-type(2),
.nlx .nlx-seg > input:nth-of-type(3):checked ~ .nlx-seg-panels .nlx-seg-panel:nth-of-type(3),
.nlx .nlx-seg > input:nth-of-type(4):checked ~ .nlx-seg-panels .nlx-seg-panel:nth-of-type(4){display:grid}
.nlx .nlx-seg > input:focus-visible ~ .nlx-seg-labels label{outline:1px dashed var(--nlx-on-deep-line)}
.nlx .nlx-bars{display:grid;gap:12px;align-content:start}
.nlx .nlx-seg{align-content:start}
.nlx .nlx-kpis--1{grid-template-columns:minmax(0,1fr)}
.nlx .nlx-kpis--2{grid-template-columns:repeat(2,minmax(0,1fr))}
.nlx .nlx-kpis--3,.nlx .nlx-kpis--6{grid-template-columns:repeat(3,minmax(0,1fr))}
.nlx .nlx-kpis--wide{grid-template-columns:repeat(2,minmax(0,1fr))}
.nlx .nlx-bar{display:grid;gap:6px}
.nlx .nlx-bar-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;font-size:14.5px}
.nlx .nlx-bar-top>span:last-child{white-space:nowrap}
.nlx .nlx-bar-track{height:10px;border-radius:6px;background:var(--nlx-on-deep-fill);overflow:hidden}
.nlx .nlx-bar-track i{display:block;height:100%;border-radius:6px;background:var(--nlx-on-deep-2)}
.nlx .nlx-bar--this .nlx-bar-track i{background:var(--nlx-mist)}
.nlx .nlx-bar--this .nlx-bar-top{font-weight:700}
.nlx .nlx-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--nlx-line);border-radius:var(--nlx-r);background:var(--nlx-surf)}
.nlx table.nlx-table{width:100%;border-collapse:collapse;font-size:15px;min-width:640px}
.nlx .nlx-table th{font-size:12.5px;font-weight:700;color:var(--nlx-mute);text-align:start;padding:11px 14px;background:var(--nlx-paper);border-bottom:1px solid var(--nlx-line);white-space:nowrap}
.nlx .nlx-table td{padding:11px 14px;border-bottom:1px solid var(--nlx-line);vertical-align:top;color:var(--nlx-ink)}
.nlx .nlx-table tr:last-child td{border-bottom:0}
.nlx .nlx-table td.nlx-r{text-align:end;white-space:nowrap}
.nlx .nlx-table caption{caption-side:bottom;text-align:start;padding:10px 14px;font-size:13px;color:var(--nlx-mute)}
.nlx .nlx-stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px}
.nlx .nlx-stats div{padding:12px 0;border-top:1px solid var(--nlx-line);display:grid;gap:2px}
.nlx .nlx-stats dt{font-size:14px;color:var(--nlx-mute)}
.nlx .nlx-stats dd{font-weight:600;line-height:1.5}
.nlx .nlx-checks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 36px;counter-reset:nlxq}
.nlx .nlx-checks li{padding:12px 0;border-top:1px solid var(--nlx-line);display:grid;grid-template-columns:28px 1fr;gap:10px;font-size:15.5px;color:var(--nlx-ink2)}
.nlx .nlx-checks li::before{content:"";width:18px;height:18px;margin-top:3px;border:1.5px solid var(--nlx-sea);border-radius:4px}
.nlx .nlx-faq{display:grid}
.nlx .nlx-faq details{border-top:1px solid var(--nlx-line)}
.nlx .nlx-faq summary{cursor:pointer;list-style:none;padding:16px 0;font-weight:700;font-size:17px;display:flex;justify-content:space-between;gap:16px}
.nlx .nlx-faq summary::-webkit-details-marker{display:none}
.nlx .nlx-faq summary::after{content:"+";font-weight:400;color:var(--nlx-sea);font-size:22px;line-height:1}
.nlx .nlx-faq details[open] summary::after{content:"\2212"}
.nlx .nlx-faq .nlx-faq-a{padding:0 0 18px;color:var(--nlx-ink2);max-width:66ch}
.nlx .nlx-agent{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:18px 24px;align-items:center;background:var(--nlx-sand);border:1px solid var(--nlx-line);border-radius:var(--nlx-r-lg);padding:clamp(20px,3vw,32px)}
.nlx .nlx-agent .nlx-monogram{width:64px;height:64px;font-size:26px}
.nlx .nlx-agent-name{font-family:var(--nlx-serif)!important;font-weight:600;font-size:24px;line-height:1.25}
.nlx .nlx-agent .nlx-cta{grid-auto-flow:column}
.nlx .nlx-sources{display:grid;gap:10px;font-size:13.5px;color:var(--nlx-ink2)}
.nlx .nlx-sources ol{list-style:decimal;padding-inline-start:22px;display:grid;gap:6px}
.nlx .nlx-sources li{padding-inline-start:4px;overflow-wrap:anywhere}
.nlx .nlx-legend{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font-size:13.5px;color:var(--nlx-mute)}
.nlx .nlx-disclaimer{font-size:13.5px;line-height:1.65;color:var(--nlx-mute);max-width:90ch}
.nlx .nlx-mbar{display:none}
@media (max-width:1080px){
  .nlx .nlx-layout{grid-template-columns:minmax(0,1fr)}
  .nlx .nlx-rail{position:static;order:-1;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
  .nlx .nlx-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}
  .nlx .nlx-band-grid{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:760px){
  .nlx{font-size:16.5px}
  .nlx .nlx-mast{grid-template-columns:minmax(0,1fr);align-items:start}
  .nlx .nlx-plate{aspect-ratio:4/3}
  .nlx .nlx-facts{grid-template-columns:repeat(2,minmax(0,1fr))}
  .nlx .nlx-fact:nth-child(odd){border-inline-start:0}
  .nlx .nlx-fact{border-top:1px solid var(--nlx-line)}
  .nlx .nlx-fact:nth-child(-n+2){border-top:0}
  .nlx .nlx-features,.nlx .nlx-two,.nlx .nlx-checks,.nlx .nlx-stats{grid-template-columns:minmax(0,1fr)}
  .nlx .nlx-row{grid-template-columns:minmax(0,1fr) auto}
  .nlx .nlx-row dd{grid-column:1/-1;grid-row:2}
  .nlx .nlx-row .nlx-row-tag{grid-column:2;grid-row:1}
  .nlx .nlx-kpis{grid-template-columns:minmax(0,1fr)}
  .nlx .nlx-agent{grid-template-columns:auto minmax(0,1fr)}
  .nlx .nlx-agent .nlx-cta{grid-column:1/-1;grid-auto-flow:row}
  .nlx .nlx-prose p{font-size:17px}
  .nlx .nlx-mbar{display:grid;grid-template-columns:1fr 1fr;gap:10px;position:sticky;bottom:0;z-index:20;padding:10px 0 calc(10px + env(safe-area-inset-bottom,0px));background:linear-gradient(to top,var(--nlx-paper) 72%,rgba(247,246,242,0))}
}
@media (prefers-reduced-motion:reduce){.nlx *{transition:none!important;scroll-behavior:auto!important}}
@media print{.nlx .nlx-rail,.nlx .nlx-mbar,.nlx .nlx-cta{display:none!important}.nlx .nlx-band{background:#fff;color:#000;border:1px solid #999}}
.nlx.nlx-cat{padding-block:clamp(24px,4vw,48px)}
.nlx .nlx-cat-head{display:grid;gap:8px;margin-block-end:clamp(20px,3vw,32px);max-width:62ch}
.nlx.nlx .nlx-cat-title{font-family:var(--nlx-serif)!important;font-weight:600!important;font-size:clamp(28px,3.4vw,40px)!important;line-height:1.2!important;color:var(--nlx-ink)!important;margin:0!important;text-wrap:balance}
.nlx .nlx-cat-lead{margin:0;color:var(--nlx-ink2)}
.nlx .nlx-cat-group{margin-block:clamp(20px,3vw,32px) 12px;font-size:13px;font-weight:700;letter-spacing:.05em;color:var(--nlx-mute)}
.nlx .nlx-cat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:18px}
.nlx a.nlx-card-l{display:grid;grid-template-rows:auto auto 1fr auto;gap:10px;background:var(--nlx-surf);border:1px solid var(--nlx-line);border-radius:var(--nlx-r);padding:20px 22px 16px;text-decoration:none!important;color:inherit!important;transition:border-color .2s ease,box-shadow .2s ease}
.nlx a.nlx-card-l:hover{border-color:var(--nlx-sea);box-shadow:var(--nlx-shadow)}
.nlx a.nlx-card-l:focus-visible{outline:2px solid var(--nlx-sea);outline-offset:3px}
.nlx .nlx-card-kicker{font-size:12.5px;font-weight:700;letter-spacing:.04em;color:var(--nlx-sea)}
.nlx.nlx .nlx-card-title{font-family:var(--nlx-serif)!important;font-weight:600!important;font-size:20px!important;line-height:1.35!important;color:var(--nlx-ink)!important;margin:0!important;text-wrap:balance}
.nlx .nlx-card-body{display:grid;gap:8px;align-content:start}
.nlx .nlx-card-price{font-size:22px;font-weight:700;line-height:1.2}
.nlx .nlx-card-price small{font-size:14px;font-weight:600;color:var(--nlx-mute)}
.nlx .nlx-card-specs{display:flex;flex-wrap:wrap;gap:2px 14px;margin:0;padding:0;list-style:none;font-size:14.5px;color:var(--nlx-ink2)}
.nlx .nlx-card-foot{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--nlx-line);padding-top:10px;font-size:12.5px;color:var(--nlx-mute)}
.nlx .nlx-card-foot b{color:var(--nlx-sea);font-weight:700;white-space:nowrap}
.nlx .nlx-plate--photo{background:var(--nlx-deep)}
.nlx .nlx-plate--photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;max-width:none}
.nlx .nlx-plate--photo .nlx-plate-name{color:#fff;text-shadow:0 1px 12px rgba(0,0,0,.45)}
.nlx .nlx-sec{scroll-margin-top:calc(var(--nlx-header-offset,96px) + 16px)}
.single-nadlan_property .nlps-price,.single-nadlan_property .nlps-facts,.single-nadlan_property .nlps-chips,.single-nadlan_property .nlps-trust,.single-nadlan_property .nlps-hl,.single-nadlan_property .nlps-3d,.single-nadlan_property .nlps-facade,.single-nadlan_property .nlps-costs,.single-nadlan_property .nlps-map-sec,.single-nadlan_property .nlps-share,.single-nadlan_property .nlps-report,.single-nadlan_property .nlcard{display:none!important}
.single-nadlan_property .nlps{margin:0!important;padding:0!important}
.single-nadlan_property .nlps-title{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;white-space:nowrap!important}
.single-nadlan_property .entry-content>article.nlx~*{display:none!important}
.nlx .nlx-toc .nlx-home{font-weight:600;color:var(--nlx-sea,#2F6F86)}
.single-nadlan_property .yoast-breadcrumbs,.single-nadlan_property .nlcta-start,.single-nadlan_property .nlcta-wa{display:none!important}
.single-nadlan_property .wp-block-post-featured-image{display:none!important}
.single-nadlan_property .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:auto!important;margin-right:auto!important}
.nlx .nlx-wrap{max-width:1180px;margin-inline:auto;padding-inline:clamp(16px,3vw,28px)}
.nlx .nlx-plate--photo{background:var(--nlx-deep);aspect-ratio:var(--nlx-cover-ar,1.5);height:auto;max-height:78vh;position:relative;overflow:hidden}
.nlx .nlx-plate--photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;max-width:none}
.nlx .nlx-gallery{columns:3;column-gap:12px;margin:0}
.nlx .nlx-gallery figure{break-inside:avoid;margin:0 0 12px;border-radius:var(--nlx-r,8px);overflow:hidden;background:var(--nlx-sand,#EEE9DD)}
.nlx .nlx-gallery img{width:100%;height:auto;display:block}
.nlx .nlx-toc .nlx-lang{margin-inline-start:auto;font-weight:600}
@media (max-width:900px){.nlx .nlx-gallery{columns:2}}
@media (max-width:520px){.nlx .nlx-gallery{columns:1}}
NLXCSS;
}

function nl_drop_fill( $s, $f, $lang ) {
	$s = (string) $s;
	if ( strpos( $s, '{{PRICE}}' ) === false ) { return $s; }
	$deal = ( $f['listing_type'] ?? '' ) === 'rent' ? 'rent' : 'sale';
	$rep  = ! empty( $f['price'] ) ? nl_drop_price_text( $f['price'], $lang ) : nl_drop_t( $lang, 'ask_' . $deal );
	return str_replace( '{{PRICE}}', $rep, $s );
}

function nl_drop_nums_html( $s ) {
	return preg_replace_callback( '/(&#?[a-z0-9]+;)|(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)/iu', function ( $m ) {
		return $m[1] !== '' ? $m[1] : '<span class="nlx-num">' . $m[2] . '</span>';
	}, esc_html( (string) $s ) );
}

function nl_drop_wa_link( $b, $lang, $title ) {
	if ( empty( $b['wa'] ) ) { return ''; }
	$name = $lang === 'en' ? $b['name_en'] : $b['name_he'];
	$txt  = sprintf( nl_drop_t( $lang, 'wa_text' ), $name, $title );
	return 'https://wa.me/' . rawurlencode( $b['wa'] ) . '?text=' . rawurlencode( $txt );
}

function nl_drop_licence_line( $b, $lang ) {
	$brand = $lang === 'en' ? $b['brand_en'] : $b['brand_he'];
	$lic   = $b['license'] !== '' ? nl_drop_t( $lang, $b['female'] ? 'lic_f' : 'lic_m' ) . ' ' . $b['license'] : '';
	return trim( implode( ' · ', array_filter( array( $brand, $lic ) ) ) );
}

/**
 * @param array $d id, facts, copy, photos[{id,url,w,h,alt}], broker, url, alt_url, page_id, date
 */
function nl_drop_listing_html( $d, $lang ) {
	$he    = $lang !== 'en';
	$f     = $d['facts'];
	$c     = $d['copy'][ $he ? 'he' : 'en' ];
	$b     = $d['broker'];
	$uid   = 'd' . (int) $d['id'] . '-' . ( $he ? 'he' : 'en' );
	$deal  = ( $f['listing_type'] ?? '' ) === 'rent' ? 'rent' : 'sale';
	$area  = $he ? ( $f['area_he'] ?: ( $f['city_he'] ?? '' ) ) : ( $f['area_en'] ?: ( $f['city_en'] ?? '' ) );
	$city  = $he ? ( $f['city_he'] ?? '' ) : ( $f['city_en'] ?? '' );
	$name  = $he ? $b['name_he'] : $b['name_en'];
	$fill  = function ( $s ) use ( $f, $lang ) { return nl_drop_fill( $s, $f, $lang ); };
	$title = $fill( $c['title'] );
	$site  = nl_drop_site_url( $b, $he ? 'he' : 'en' );
	$wa    = nl_drop_wa_link( $b, $he ? 'he' : 'en', $title );
	$tel   = $b['wa'] !== '' ? 'tel:+' . $b['wa'] : '';
	$photos = array_values( (array) $d['photos'] );
	$cover  = $photos ? $photos[0] : null;
	$kick   = array( nl_drop_t( $lang, $deal ) );
	if ( ! empty( $f['exclusive'] ) ) { $kick[] = nl_drop_t( $lang, 'exclusive' ); }
	$place = trim( $area . ( $city && $city !== $area ? ', ' . $city : '' ) );
	if ( $place !== '' ) { $kick[] = $place; }

	$h = '<article class="nlx" lang="' . ( $he ? 'he' : 'en' ) . '" dir="' . ( $he ? 'rtl' : 'ltr' ) . '" id="nlx-' . esc_attr( $uid ) . '" data-listing="' . esc_attr( $uid ) . '">' . "\n" . '<div class="nlx-wrap">' . "\n";
	$h .= '<header class="nlx-mast">' . "\n" . '<div class="nlx-mast-copy">' . "\n";
	$h .= '<p class="nlx-kicker">' . esc_html( implode( ' · ', $kick ) ) . '</p>' . "\n";
	$tag = $he ? 'h2' : 'h1';
	$h .= '<' . $tag . ' class="nlx-title">' . nl_drop_nums_html( $title ) . '</' . $tag . '>' . "\n";
	$h .= '<p class="nlx-dek">' . nl_drop_nums_html( $fill( $c['dek'] ) ) . '</p>' . "\n";
	$chips = '<span class="nlx-chip nlx-chip--sea">' . esc_html( ( ! empty( $f['exclusive'] ) ? nl_drop_t( $lang, 'exclusive' ) . ' · ' : '' ) . $name ) . '</span>';
	foreach ( (array) $c['chips'] as $ch ) { $chips .= '<span class="nlx-chip">' . esc_html( $fill( $ch ) ) . '</span>'; }
	$h .= '<div class="nlx-chips">' . $chips . '</div>' . "\n" . '</div>' . "\n";
	if ( $cover ) {
		$ar = ( $cover['w'] > 0 && $cover['h'] > 0 ) ? $cover['w'] / $cover['h'] : 1.5;
		$ar = max( 0.56, min( 1.8, $ar ) );
		$h .= '<figure class="nlx-plate nlx-plate--photo" style="--nlx-cover-ar:' . esc_attr( sprintf( '%.3f', $ar ) ) . '"><img src="' . esc_url( $cover['url'] ) . '" alt="' . esc_attr( $title ) . '" width="' . (int) $cover['w'] . '" height="' . (int) $cover['h'] . '" loading="eager" decoding="async" fetchpriority="high">';
		$h .= $area !== '' ? '<span class="nlx-plate-name">' . esc_html( $area ) . '</span>' : '';
		$h .= '</figure>' . "\n";
	}
	$h .= '</header>' . "\n";

	// facts: only what the broker wrote
	$facts = array();
	$sq    = nl_drop_t( $lang, 'sqm' );
	if ( ! empty( $f['rooms'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_rooms' ), '<span class="nlx-num">' . esc_html( nl_drop_fmt_num( $f['rooms'] ) ) . '</span>' ); }
	if ( ! empty( $f['size_sqm'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_size' ), '<span class="nlx-num">' . esc_html( nl_drop_fmt_int( $f['size_sqm'] ) ) . '</span> ' . $sq ); }
	if ( ! empty( $f['balcony_sqm'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_balcony' ), '<span class="nlx-num">' . esc_html( nl_drop_fmt_int( $f['balcony_sqm'] ) ) . '</span> ' . $sq ); }
	if ( ! empty( $f['garden_sqm'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_garden' ), '<span class="nlx-num">' . esc_html( nl_drop_fmt_int( $f['garden_sqm'] ) ) . '</span> ' . $sq ); }
	if ( isset( $f['floor'] ) && $f['floor'] !== null ) {
		$fl = $f['floor'] == 0 ? ( $he ? 'קרקע' : 'Ground' ) : '<span class="nlx-num">' . (int) $f['floor'] . '</span>' . ( ! empty( $f['total_floors'] ) ? ' ' . nl_drop_t( $lang, 'of' ) . ' <span class="nlx-num">' . (int) $f['total_floors'] . '</span>' : '' );
		$facts[] = array( nl_drop_t( $lang, 'f_floor' ), $fl );
	}
	if ( ! empty( $f['parking'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_parking' ), ! empty( $f['parking_count'] ) ? '<span class="nlx-num">' . (int) $f['parking_count'] . '</span>' : nl_drop_t( $lang, 'yes' ) ); }
	if ( ! empty( $f['storage'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_storage' ), nl_drop_t( $lang, 'yes' ) ); }
	if ( ! empty( $f['protected_room'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_safe' ), nl_drop_t( $lang, 'yes' ) ); }
	if ( ! empty( $f['elevator'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_lift' ), nl_drop_t( $lang, 'yes' ) ); }
	if ( ! empty( $f['furnished'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_furnished' ), nl_drop_t( $lang, 'furnished' ) ); }
	if ( ! empty( $f['condition'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_condition' ), nl_drop_t( $lang, 'c_' . $f['condition'] ) ); }
	$entry = $he ? ( $f['entry_he'] ?? '' ) : ( $f['entry_en'] ?? '' );
	if ( $entry ) { $facts[] = array( nl_drop_t( $lang, 'f_entry' ), esc_html( $entry ) ); }
	if ( $facts ) {
		$h .= '<dl class="nlx-facts">' . "\n";
		foreach ( array_slice( $facts, 0, 8 ) as $x ) { $h .= '<div class="nlx-fact"><dt>' . esc_html( $x[0] ) . '</dt><dd>' . $x[1] . '</dd></div>' . "\n"; }
		$h .= '</dl>' . "\n";
	}

	$gallery = array_slice( $photos, 1 );
	$toc     = '';
	if ( $site ) { $toc .= '<a class="nlx-home" href="' . esc_url( $site ) . '">' . esc_html( sprintf( nl_drop_t( $lang, 'site' ), $name ) ) . '</a>'; }
	if ( $gallery ) { $toc .= '<a href="#photos-' . esc_attr( $uid ) . '">' . esc_html( nl_drop_t( $lang, 'photos' ) ) . '</a>'; }
	$toc .= '<a href="#home-' . esc_attr( $uid ) . '">' . esc_html( nl_drop_t( $lang, 'home' ) ) . '</a>';
	$toc .= '<a href="#broker-' . esc_attr( $uid ) . '">' . esc_html( $he ? ( $b['female'] ? 'המתווכת' : 'המתווך' ) : 'Broker' ) . '</a>';
	if ( ! empty( $d['alt_url'] ) ) {
		$al   = $he ? 'en' : 'he';
		$toc .= '<a class="nlx-lang" href="' . esc_url( $d['alt_url'] ) . '" hreflang="' . $al . '" lang="' . $al . '">' . esc_html( nl_drop_t( $lang, 'switch' ) ) . '</a>';
	}
	$h .= '<nav class="nlx-toc" aria-label="' . esc_attr( nl_drop_t( $lang, 'toc' ) ) . '">' . $toc . '</nav>' . "\n";

	$h .= '<div class="nlx-layout">' . "\n" . '<div class="nlx-main">' . "\n";
	if ( $gallery ) {
		$h .= '<section class="nlx-sec" id="photos-' . esc_attr( $uid ) . '"><div class="nlx-sec-head"><p class="nlx-eyebrow">' . esc_html( nl_drop_t( $lang, 'photos' ) ) . '</p><h2 class="nlx-h2">' . esc_html( nl_drop_t( $lang, 'photos_h2' ) ) . '</h2></div><div class="nlx-gallery">';
		foreach ( $gallery as $i => $g ) {
			$h .= '<figure><img src="' . esc_url( $g['url'] ) . '" alt="' . esc_attr( $title . ' · ' . ( $i + 2 ) ) . '" loading="lazy" decoding="async"' . ( $g['w'] ? ' width="' . (int) $g['w'] . '" height="' . (int) $g['h'] . '"' : '' ) . '></figure>';
		}
		$h .= '</div></section>' . "\n";
	}
	$h .= '<section class="nlx-sec" id="home-' . esc_attr( $uid ) . '">' . "\n";
	$h .= '<div class="nlx-sec-head"><p class="nlx-eyebrow">' . esc_html( nl_drop_t( $lang, 'home' ) ) . '</p><h2 class="nlx-h2">' . nl_drop_nums_html( $fill( $c['story_h2'] ) ) . '</h2></div>' . "\n";
	$h .= '<div class="nlx-prose">';
	foreach ( (array) $c['story'] as $para ) { $h .= '<p>' . nl_drop_nums_html( $fill( $para ) ) . '</p>'; }
	$h .= '</div>' . "\n";
	if ( ! empty( $c['features'] ) ) {
		$h .= '<ul class="nlx-features">';
		foreach ( (array) $c['features'] as $pair ) {
			$h .= '<li><b>' . nl_drop_nums_html( $fill( $pair[0] ?? '' ) ) . '</b>' . ( ! empty( $pair[1] ) ? '<span>' . nl_drop_nums_html( $fill( $pair[1] ) ) . '</span>' : '' ) . '</li>';
		}
		$h .= '</ul>' . "\n";
	}
	$h .= '</section>' . "\n";

	$eyebrow = nl_drop_t( $lang, ( ! empty( $f['exclusive'] ) ? 'broker_ex_' : 'broker_' ) . ( $b['female'] ? 'f' : 'm' ) );
	$lic     = nl_drop_licence_line( $b, $lang );
	$mono    = function_exists( 'mb_substr' ) ? mb_substr( $name, 0, 1 ) : substr( $name, 0, 1 );
	$btn_wa  = $wa ? '<a class="nlx-btn" href="' . esc_url( $wa ) . '" rel="noopener" target="_blank">' . nl_drop_icon( 'wa' ) . '<span>' . esc_html( nl_drop_t( $lang, 'cta' ) ) . '</span></a>' : '';
	$btn_tel = $tel ? '<a class="nlx-btn nlx-btn--ghost" href="' . esc_url( $tel ) . '">' . nl_drop_icon( 'phone' ) . '<span>' . esc_html( nl_drop_t( $lang, 'call' ) . ' ' . ( $he ? $b['phone'] : $b['phone_intl'] ) ) . '</span></a>' : '';
	$h .= '<section class="nlx-sec" id="broker-' . esc_attr( $uid ) . '">' . "\n" . '<div class="nlx-agent">' . "\n";
	$h .= '<span class="nlx-monogram" aria-hidden="true">' . esc_html( $mono ) . '</span>' . "\n";
	$h .= '<div><p class="nlx-eyebrow">' . esc_html( $eyebrow ) . '</p><p class="nlx-agent-name">' . esc_html( $name ) . '</p><p class="nlx-small">' . nl_drop_nums_html( $lic ) . '</p></div>' . "\n";
	$h .= '<div class="nlx-cta">' . $btn_wa . $btn_tel . '</div>' . "\n" . '</div>' . "\n" . '</section>' . "\n";
	$h .= '</div>' . "\n";

	// the rail
	$h .= '<aside class="nlx-rail" aria-label="' . esc_attr( nl_drop_t( $lang, 'rail' ) ) . '">' . "\n" . '<div class="nlx-card nlx-price-card">' . "\n";
	$h .= '<span class="nlx-price-lbl">' . esc_html( nl_drop_t( $lang, 'price_' . $deal ) ) . '</span>' . "\n";
	if ( ! empty( $f['price'] ) ) {
		$h .= '<span class="nlx-price">' . nl_drop_money_html( $f['price'], $lang ) . '</span>' . "\n";
		$rows = '';
		if ( ! empty( $f['size_sqm'] ) ) { $rows .= '<div><dt>' . esc_html( nl_drop_t( $lang, 'psqm_' . $deal ) ) . '</dt><dd>' . nl_drop_money_html( round( $f['price'] / $f['size_sqm'] ), $lang ) . '</dd></div>'; }
		if ( $deal === 'rent' ) { $rows .= '<div><dt>' . esc_html( nl_drop_t( $lang, 'year' ) ) . '</dt><dd>' . nl_drop_money_html( $f['price'] * 12, $lang ) . '</dd></div>'; }
		if ( $entry ) { $rows .= '<div><dt>' . esc_html( nl_drop_t( $lang, 'f_entry' ) ) . '</dt><dd>' . esc_html( $entry ) . '</dd></div>'; }
		if ( $rows ) { $h .= '<dl class="nlx-price-rows">' . $rows . '</dl>' . "\n"; }
	} else {
		$h .= '<span class="nlx-price nlx-price--ask">' . esc_html( nl_drop_t( $lang, 'ask_' . $deal ) ) . '</span>' . "\n";
	}
	$h .= '<div class="nlx-cta">' . $btn_wa . ( $tel ? '<a class="nlx-btn nlx-btn--ghost" href="' . esc_url( $tel ) . '">' . nl_drop_icon( 'phone' ) . '<span>' . esc_html( nl_drop_t( $lang, 'call' ) ) . '</span></a>' : '' ) . '</div>' . "\n" . '</div>' . "\n";
	$h .= '<div class="nlx-card nlx-agent-mini"><span class="nlx-monogram" aria-hidden="true">' . esc_html( $mono ) . '</span><div><b>' . esc_html( $name ) . '</b><br><span class="nlx-muted">' . nl_drop_nums_html( $lic ) . '</span></div></div>' . "\n";
	$h .= '</aside>' . "\n" . '</div>' . "\n";
	if ( $wa || $tel ) {
		$h .= '<div class="nlx-mbar">' . ( $wa ? '<a class="nlx-btn" href="' . esc_url( $wa ) . '" rel="noopener" target="_blank">' . nl_drop_icon( 'wa' ) . '<span>' . esc_html( nl_drop_t( $lang, 'wa' ) ) . '</span></a>' : '' ) . ( $tel ? '<a class="nlx-btn nlx-btn--ghost" href="' . esc_url( $tel ) . '">' . nl_drop_icon( 'phone' ) . '<span>' . esc_html( nl_drop_t( $lang, 'call' ) ) . '</span></a>' : '' ) . '</div>' . "\n";
	}
	$h .= '</div>' . "\n";

	if ( ! $he ) {
		$imgs = array();
		foreach ( $photos as $p ) { $imgs[] = $p['url']; }
		$node = array(
			'@type'       => 'RealEstateListing',
			'name'        => $title,
			'description' => $fill( $c['seo_desc'] ),
			'url'         => (string) $d['url'],
			'inLanguage'  => 'en',
			'datePosted'  => (string) $d['date'],
			'image'       => $imgs,
			'about'       => array_filter( array(
				'@type'         => in_array( $f['property_type'] ?? '', array( 'villa', 'cottage' ), true ) ? 'SingleFamilyResidence' : 'Apartment',
				'name'          => $title,
				'numberOfRooms' => ! empty( $f['rooms'] ) ? (float) $f['rooms'] : null,
				'floorSize'     => ! empty( $f['size_sqm'] ) ? array( '@type' => 'QuantitativeValue', 'value' => (int) $f['size_sqm'], 'unitCode' => 'MTK' ) : null,
				'address'       => array_filter( array( '@type' => 'PostalAddress', 'addressLocality' => $f['city_en'] ?? null, 'addressRegion' => $f['area_en'] ?? null, 'addressCountry' => 'IL' ) ),
			) ),
		);
		if ( ! empty( $f['price'] ) ) { $node['offers'] = array( '@type' => 'Offer', 'price' => (int) $f['price'], 'priceCurrency' => 'ILS', 'availability' => 'https://schema.org/InStock' ); }
		$h .= '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => array( $node ) ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	}
	$h .= '</article>';

	$css = nl_drop_listing_css();
	if ( ! empty( $d['page_id'] ) ) {
		$pid  = (int) $d['page_id'];
		$css .= "\nbody.page-id-{$pid} .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:auto!important;margin-right:auto!important}"
			. "\nbody.page-id-{$pid} .wp-block-post-featured-image,body.page-id-{$pid} .yoast-breadcrumbs,body.page-id-{$pid} .nlcta-start,body.page-id-{$pid} .nlcta-wa{display:none!important}";
	}
	$css .= "\n.nlx .nlx-price--ask{font-size:20px;line-height:1.35}";
	return "<!-- wp:html -->\n<style>\n" . $css . "\n</style>\n" . $h . "\n<!-- /wp:html -->";
}

/* =====================================================================================================
 * Build: the Hebrew listing, the English twin, the photos, the language map, the caches
 * ===================================================================================================== */
function nl_drop_kses_off() {
	$had = has_filter( 'content_save_pre', 'wp_filter_post_kses' ) !== false;
	if ( $had ) { kses_remove_filters(); }
	return $had;
}

function nl_drop_kses_on( $had ) {
	if ( $had ) { kses_init_filters(); }
}

function nl_drop_photos( $ids, $title ) {
	$out = array();
	foreach ( array_values( (array) $ids ) as $i => $id ) {
		$id  = (int) $id;
		$url = wp_get_attachment_url( $id );
		if ( ! $url ) { continue; }
		$m     = wp_get_attachment_metadata( $id );
		$out[] = array( 'id' => $id, 'url' => $url, 'w' => (int) ( $m['width'] ?? 0 ), 'h' => (int) ( $m['height'] ?? 0 ) );
	}
	return $out;
}

function nl_drop_purge( $ids ) {
	foreach ( array_unique( array_filter( array_map( 'intval', (array) $ids ) ) ) as $id ) {
		clean_post_cache( $id );
		do_action( 'litespeed_purge_post', $id );
		$u = get_permalink( $id );
		if ( $u ) { do_action( 'litespeed_purge_url', $u ); }
	}
}

function nl_drop_data_for( $he_id, $b ) {
	$f      = json_decode( (string) get_post_meta( $he_id, 'nl_facts', true ), true );
	$c      = json_decode( (string) get_post_meta( $he_id, 'nl_copy', true ), true );
	$photos = json_decode( (string) get_post_meta( $he_id, 'nl_photos_json', true ), true );
	if ( ! is_array( $f ) || ! is_array( $c ) ) { return null; }
	return array( 'facts' => $f, 'copy' => $c, 'photos' => is_array( $photos ) ? $photos : array(), 'broker' => $b );
}

/** Writes both pages from the stored facts and copy. Used on first build, and on every price change. */
function nl_drop_render_pair( $he_id, $en_id, $b ) {
	$data = nl_drop_data_for( $he_id, $b );
	if ( ! $data ) { return false; }
	$url_he = (string) get_permalink( $he_id );
	$url_en = $en_id ? (string) get_permalink( $en_id ) : '';
	$date   = get_post_time( 'Y-m-d', false, $he_id );
	$had = nl_drop_kses_off();
	wp_update_post( array( 'ID' => $he_id, 'post_excerpt' => nl_drop_fill( $data['copy']['he']['dek'], $data['facts'], 'he' ), 'post_content' => nl_drop_listing_html( array_merge( $data, array( 'id' => $he_id, 'url' => $url_he, 'alt_url' => $url_en, 'page_id' => 0, 'date' => $date ) ), 'he' ) ) );
	if ( $en_id ) {
		wp_update_post( array( 'ID' => $en_id, 'post_excerpt' => nl_drop_fill( $data['copy']['en']['dek'], $data['facts'], 'en' ), 'post_content' => nl_drop_listing_html( array_merge( $data, array( 'id' => $he_id, 'url' => $url_en, 'alt_url' => $url_he, 'page_id' => $en_id, 'date' => $date ) ), 'en' ) ) );
	}
	nl_drop_kses_on( $had );
	update_post_meta( $he_id, '_yoast_wpseo_title', wp_slash( nl_drop_fill( $data['copy']['he']['seo_title'], $data['facts'], 'he' ) ) );
	update_post_meta( $he_id, '_yoast_wpseo_metadesc', wp_slash( nl_drop_fill( $data['copy']['he']['seo_desc'], $data['facts'], 'he' ) ) );
	if ( $en_id ) {
		update_post_meta( $en_id, '_yoast_wpseo_title', wp_slash( nl_drop_fill( $data['copy']['en']['seo_title'], $data['facts'], 'en' ) ) );
		update_post_meta( $en_id, '_yoast_wpseo_metadesc', wp_slash( nl_drop_fill( $data['copy']['en']['seo_desc'], $data['facts'], 'en' ) ) );
	}
	return true;
}

function nl_drop_build( $drop_id, $b ) {
	$prev = get_post_meta( $drop_id, 'nl_result', true );
	if ( is_array( $prev ) && ! empty( $prev['he_id'] ) ) { return $prev; }
	$f      = json_decode( (string) get_post_meta( $drop_id, 'nl_facts', true ), true );
	$text   = (string) get_post_meta( $drop_id, 'nl_text', true );
	$ids    = array_map( 'intval', (array) get_post_meta( $drop_id, 'nl_photos', true ) );
	if ( ! is_array( $f ) ) { return new WP_Error( 'nofacts', 'no facts' ); }
	update_post_meta( $drop_id, 'nl_state', 'writing' );
	$err  = null;
	$copy = nl_drop_write( $f, $text, $b, $err );
	$slug = nl_drop_slug( $f, $b );
	$pub  = $f;
	unset( $pub['street_he'] );
	$photos = nl_drop_photos( $ids, $copy['he']['title'] );
	$author = nl_drop_author();
	$status = $b['auto'] ? 'publish' : 'draft';

	$had   = nl_drop_kses_off();
	$he_id = wp_insert_post( array(
		'post_type'    => 'nadlan_property',
		'post_status'  => $status,
		'post_title'   => nl_drop_fill( $copy['he']['title'], $f, 'he' ),
		'post_name'    => $slug,
		'post_excerpt' => nl_drop_fill( $copy['he']['dek'], $f, 'he' ),
		'post_content' => '',
		'post_author'  => $author,
	), true );
	nl_drop_kses_on( $had );
	if ( is_wp_error( $he_id ) ) { update_post_meta( $drop_id, 'nl_state', 'failed' ); return $he_id; }

	$type_map = array( 'mini_penthouse' => 'penthouse', 'villa' => 'cottage' );
	$ptype    = $f['property_type'] ? ( $type_map[ $f['property_type'] ] ?? $f['property_type'] ) : 'apartment';
	$meta     = array(
		'listing_type'   => $f['listing_type'],
		'property_type'  => $ptype,
		'price'          => $f['price'],
		'rooms'          => $f['rooms'],
		'floor'          => $f['floor'],
		'total_floors'   => $f['total_floors'],
		'size_sqm'       => $f['size_sqm'],
		'sqm'            => $f['size_sqm'],
		'balcony_sqm'    => $f['balcony_sqm'],
		'city'           => $f['city_he'],
		'neighborhood'   => $f['area_he'],
		'parking'        => $f['parking'],
		'elevator'       => $f['elevator'],
		'ac'             => $f['ac'],
		'protected_room' => $f['protected_room'],
		'storage'        => $f['storage'],
		'entry_date'     => $f['entry_he'],
		'condition'      => $f['condition'],
		'highlights_csv' => implode( '|', array_slice( $f['features_he'] ?? array(), 0, 6 ) ),
	);
	foreach ( $meta as $k => $v ) {
		if ( $v !== null && $v !== '' ) { update_post_meta( $he_id, $k, $v ); }
	}
	update_post_meta( $he_id, 'status', 'active' );
	update_post_meta( $he_id, 'claim_status', 'verified' );
	update_post_meta( $he_id, 'source', 'broker_drop' );
	update_post_meta( $he_id, 'nl_broker_id', (string) $b['id'] );
	update_post_meta( $he_id, 'nl_status', 'active' );
	update_post_meta( $he_id, 'nl_drop_id', (string) $drop_id );
	update_post_meta( $he_id, 'nl_facts', wp_slash( wp_json_encode( $pub, JSON_UNESCAPED_UNICODE ) ) );
	update_post_meta( $he_id, 'nl_copy', wp_slash( wp_json_encode( $copy, JSON_UNESCAPED_UNICODE ) ) );
	update_post_meta( $he_id, 'nl_photos_json', wp_slash( wp_json_encode( $photos, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ) );
	update_post_meta( $he_id, 'photos_csv', implode( ',', wp_list_pluck( $photos, 'url' ) ) );
	update_post_meta( $he_id, '_yoast_wpseo_title', nl_drop_fill( $copy['he']['seo_title'], $f, 'he' ) );
	update_post_meta( $he_id, '_yoast_wpseo_metadesc', nl_drop_fill( $copy['he']['seo_desc'], $f, 'he' ) );
	if ( $photos ) { set_post_thumbnail( $he_id, $photos[0]['id'] ); }
	foreach ( $photos as $i => $p ) {
		wp_update_post( array( 'ID' => $p['id'], 'post_parent' => $he_id ) );
		update_post_meta( $p['id'], '_wp_attachment_image_alt', wp_slash( nl_drop_fill( $copy['he']['title'], $f, 'he' ) . ( $i ? ' · ' . ( $i + 1 ) : '' ) ) );
	}

	$en_id = 0;
	if ( ! empty( $b['site_en'] ) && get_post( (int) $b['site_en'] ) ) {
		$had   = nl_drop_kses_off();
		$en_id = wp_insert_post( array(
			'post_type'    => 'page',
			'post_status'  => $status,
			'post_parent'  => (int) $b['site_en'],
			'post_title'   => nl_drop_fill( $copy['en']['title'], $f, 'en' ),
			'post_name'    => $slug,
			'post_excerpt' => nl_drop_fill( $copy['en']['dek'], $f, 'en' ),
			'post_content' => '',
			'post_author'  => $author,
		), true );
		nl_drop_kses_on( $had );
		if ( is_wp_error( $en_id ) ) { $en_id = 0; }
	}
	if ( $en_id ) {
		update_post_meta( $en_id, 'nl_broker_id', (string) $b['id'] );
		update_post_meta( $en_id, 'nl_twin', (string) $he_id );
		update_post_meta( $en_id, 'nl_status', 'active' );
		update_post_meta( $en_id, 'source', 'broker_drop' );
		update_post_meta( $en_id, '_yoast_wpseo_title', nl_drop_fill( $copy['en']['seo_title'], $f, 'en' ) );
		update_post_meta( $en_id, '_yoast_wpseo_metadesc', nl_drop_fill( $copy['en']['seo_desc'], $f, 'en' ) );
		if ( $photos ) { set_post_thumbnail( $en_id, $photos[0]['id'] ); }
		update_post_meta( $he_id, 'nl_twin', (string) $en_id );
	}
	nl_drop_render_pair( $he_id, $en_id, $b );
	$url_he = (string) get_permalink( $he_id );
	$url_en = $en_id ? (string) get_permalink( $en_id ) : '';
	if ( $en_id ) {
		$map = wp_slash( wp_json_encode( array( 'he' => $url_he, 'en' => $url_en ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) );
		update_post_meta( $he_id, 'nl_hreflang', $map );
		update_post_meta( $en_id, 'nl_hreflang', $map );
	}
	nl_drop_purge( array( $he_id, $en_id, $b['site_he'], $b['site_en'] ) );
	$res = array(
		'state'  => $status === 'publish' ? 'published' : 'draft',
		'he_id'  => (int) $he_id,
		'en_id'  => (int) $en_id,
		'url_he' => $url_he,
		'url_en' => $url_en,
		'title'  => nl_drop_fill( $copy['he']['title'], $f, 'he' ),
		'ai'     => $err ? 'fallback:' . $err : 'ok',
	);
	update_post_meta( $drop_id, 'nl_result', $res );
	update_post_meta( $drop_id, 'nl_state', $res['state'] );
	return $res;
}

/* =====================================================================================================
 * REST: the only doors. The token in the path is the identity; nothing works without a live broker.
 * ===================================================================================================== */
add_action( 'rest_api_init', function () {
	$t = '/drop/(?P<token>[a-z0-9]{24})';
	register_rest_route( 'nadlan/v1', $t . '/photo', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nl_drop_rest_photo' ) );
	register_rest_route( 'nadlan/v1', $t . '/submit', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nl_drop_rest_submit' ) );
	register_rest_route( 'nadlan/v1', $t . '/build/(?P<drop>\d+)', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nl_drop_rest_build' ) );
	register_rest_route( 'nadlan/v1', $t . '/listings', array( 'methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => 'nl_drop_rest_listings' ) );
	register_rest_route( 'nadlan/v1', $t . '/update', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nl_drop_rest_update' ) );
} );

function nl_drop_rest_broker( $req ) {
	$b = nl_drop_broker_by_token( (string) $req['token'] );
	if ( ! $b ) { return new WP_Error( 'nl_drop_off', 'הקישור לא פעיל.', array( 'status' => 404 ) ); }
	return $b;
}

function nl_drop_strip_gps( $file, $type ) {
	if ( $type !== 'image/jpeg' || ! function_exists( 'exif_read_data' ) || ! function_exists( 'imagecreatefromjpeg' ) ) { return; }
	$ex = @exif_read_data( $file );
	if ( ! is_array( $ex ) || empty( $ex['GPSLatitude'] ) ) { return; }
	$im = @imagecreatefromjpeg( $file );
	if ( ! $im ) { return; }
	$o = (int) ( $ex['Orientation'] ?? 1 );
	if ( $o === 3 ) { $im = imagerotate( $im, 180, 0 ); }
	elseif ( $o === 6 ) { $im = imagerotate( $im, -90, 0 ); }
	elseif ( $o === 8 ) { $im = imagerotate( $im, 90, 0 ); }
	imagejpeg( $im, $file, 90 );
	imagedestroy( $im );
}

function nl_drop_rest_photo( WP_REST_Request $req ) {
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	if ( nl_drop_rate( $b['id'], 'photo', 150, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה תמונות בשעה האחרונה. אפשר להמשיך בעוד כמה דקות.', array( 'status' => 429 ) ); }
	$files = $req->get_file_params();
	$f     = $files['photo'] ?? null;
	if ( ! is_array( $f ) || empty( $f['tmp_name'] ) ) { return new WP_Error( 'nofile', 'לא התקבל קובץ.', array( 'status' => 400 ) ); }
	if ( (int) $f['size'] > NL_DROP_MAX_BYTES ) { return new WP_Error( 'big', 'התמונה גדולה מ-15MB.', array( 'status' => 400 ) ); }
	$mimes = array( 'jpg|jpeg|jpe' => 'image/jpeg', 'png' => 'image/png', 'webp' => 'image/webp', 'heic' => 'image/heic', 'heif' => 'image/heif' );
	$check = wp_check_filetype_and_ext( $f['tmp_name'], $f['name'], $mimes );
	if ( empty( $check['type'] ) || strpos( (string) $check['type'], 'image/' ) !== 0 ) { return new WP_Error( 'type', 'אפשר להעלות תמונות בלבד.', array( 'status' => 400 ) ); }
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	$f['name'] = 'nadlan-' . $b['id'] . '-' . gmdate( 'Ymd-His' ) . '-' . wp_rand( 100, 999 ) . '.' . ( $check['ext'] ?: 'jpg' );
	$moved     = wp_handle_upload( $f, array( 'test_form' => false, 'mimes' => $mimes ) );
	if ( isset( $moved['error'] ) ) { return new WP_Error( 'upload', 'ההעלאה נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	nl_drop_strip_gps( $moved['file'], $moved['type'] );
	$att = wp_insert_attachment( array(
		'post_mime_type' => $moved['type'],
		'post_title'     => 'nadlan-drop-' . $b['id'],
		'post_status'    => 'inherit',
		'post_author'    => nl_drop_author(),
	), $moved['file'] );
	if ( is_wp_error( $att ) || ! $att ) { return new WP_Error( 'insert', 'ההעלאה נכשלה.', array( 'status' => 500 ) ); }
	wp_update_attachment_metadata( $att, wp_generate_attachment_metadata( $att, $moved['file'] ) );
	update_post_meta( $att, 'nl_drop_broker', (string) $b['id'] );
	$m = wp_get_attachment_metadata( $att );
	return array( 'id' => (int) $att, 'url' => (string) wp_get_attachment_url( $att ), 'w' => (int) ( $m['width'] ?? 0 ), 'h' => (int) ( $m['height'] ?? 0 ) );
}

function nl_drop_rest_submit( WP_REST_Request $req ) {
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	if ( nl_drop_rate( $b['id'], 'submit', 40, DAY_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הגעתם למכסת הנכסים להיום.', array( 'status' => 429 ) ); }
	$text = trim( sanitize_textarea_field( (string) $req->get_param( 'text' ) ) );
	$text = function_exists( 'mb_substr' ) ? mb_substr( $text, 0, 4000 ) : substr( $text, 0, 4000 );
	$ids  = array();
	foreach ( (array) $req->get_param( 'photos' ) as $id ) {
		$id = (int) $id;
		if ( $id && get_post_type( $id ) === 'attachment' && (string) get_post_meta( $id, 'nl_drop_broker', true ) === (string) $b['id'] && ! in_array( $id, $ids, true ) ) { $ids[] = $id; }
		if ( count( $ids ) >= NL_DROP_MAX_PHOTOS ) { break; }
	}
	if ( ( function_exists( 'mb_strlen' ) ? mb_strlen( $text ) : strlen( $text ) ) < 8 ) {
		return array( 'state' => 'held', 'missing' => array( 'כמה שורות על הנכס' ) );
	}
	@set_time_limit( 170 );
	$drop_id = wp_insert_post( array(
		'post_type'    => 'nadlan_drop',
		'post_status'  => 'private',
		'post_title'   => $b['name_he'] . ' · ' . wp_date( 'j.n.Y H:i' ),
		'post_content' => $text,
		'post_author'  => nl_drop_author(),
	), true );
	if ( is_wp_error( $drop_id ) ) { return new WP_Error( 'save', 'השמירה נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	update_post_meta( $drop_id, 'nl_broker_id', (string) $b['id'] );
	update_post_meta( $drop_id, 'nl_text', wp_slash( $text ) );
	update_post_meta( $drop_id, 'nl_photos', $ids );
	update_post_meta( $drop_id, 'nl_door', 'link' );
	update_post_meta( $drop_id, 'nl_state', 'reading' );
	$err = null;
	$f   = nl_drop_extract( $text, $b, $err );
	update_post_meta( $drop_id, 'nl_facts', wp_slash( wp_json_encode( $f, JSON_UNESCAPED_UNICODE ) ) );
	if ( $err ) { update_post_meta( $drop_id, 'nl_ai', 'fallback:' . $err ); }
	$miss = nl_drop_missing( $f, $ids );
	if ( $miss ) {
		update_post_meta( $drop_id, 'nl_state', 'held' );
		update_post_meta( $drop_id, 'nl_missing', $miss );
		return array( 'state' => 'held', 'drop' => (int) $drop_id, 'missing' => $miss, 'summary' => nl_drop_summary( $f ) );
	}
	update_post_meta( $drop_id, 'nl_state', 'ready' );
	return array( 'state' => 'ready', 'drop' => (int) $drop_id, 'summary' => nl_drop_summary( $f ) );
}

function nl_drop_rest_build( WP_REST_Request $req ) {
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	$drop = (int) $req['drop'];
	if ( get_post_type( $drop ) !== 'nadlan_drop' || (string) get_post_meta( $drop, 'nl_broker_id', true ) !== (string) $b['id'] ) {
		return new WP_Error( 'nf', 'לא נמצא.', array( 'status' => 404 ) );
	}
	$state = (string) get_post_meta( $drop, 'nl_state', true );
	if ( ! in_array( $state, array( 'ready', 'writing', 'published', 'draft' ), true ) ) { return new WP_Error( 'state', 'חסרים פרטים.', array( 'status' => 409 ) ); }
	@set_time_limit( 170 );
	$res = nl_drop_build( $drop, $b );
	if ( is_wp_error( $res ) ) { return new WP_Error( 'build', 'בניית העמוד נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	return $res;
}

/** The broker's properties, newest first: the pages built here and the ones linked to the broker. */
function nl_drop_broker_listings( $bid, $lang = 'he', $only_live = true ) {
	$q = get_posts( array(
		'post_type'        => 'nadlan_property',
		'post_status'      => $only_live ? array( 'publish' ) : array( 'publish', 'draft' ),
		'numberposts'      => 200,
		'orderby'          => 'date',
		'order'            => 'DESC',
		'suppress_filters' => true,
		'meta_query'       => array( array( 'key' => 'nl_broker_id', 'value' => (string) (int) $bid ) ),
	) );
	$out = array();
	foreach ( $q as $p ) {
		$twin = (int) get_post_meta( $p->ID, 'nl_twin', true );
		if ( $lang === 'en' && ( ! $twin || get_post_status( $twin ) !== 'publish' ) ) { continue; }
		$st = (string) get_post_meta( $p->ID, 'nl_status', true );
		$out[] = array(
			'id'       => (int) $p->ID,
			'twin'     => $twin,
			'url'      => (string) get_permalink( $lang === 'en' ? $twin : $p->ID ),
			'title'    => (string) ( $lang === 'en' && $twin ? get_the_title( $twin ) : get_the_title( $p ) ),
			'deal'     => (string) get_post_meta( $p->ID, 'listing_type', true ) === 'rent' ? 'rent' : 'sale',
			'status'   => in_array( $st, array( 'sold', 'rented' ), true ) ? $st : 'active',
			'card_key' => (string) get_post_meta( $p->ID, 'nl_card_key', true ),
			'source'   => (string) get_post_meta( $p->ID, 'source', true ),
			'price'    => (int) get_post_meta( $p->ID, 'price', true ),
			'cover'    => (string) get_the_post_thumbnail_url( $p->ID, 'medium' ),
			'date'     => get_post_time( 'U', true, $p->ID ),
			'modified' => get_post_modified_time( 'U', true, $p->ID ),
		);
	}
	return $out;
}

function nl_drop_rest_listings( WP_REST_Request $req ) {
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	$rows = array();
	foreach ( nl_drop_broker_listings( $b['id'], 'he', false ) as $L ) {
		$rows[] = array(
			'id'       => $L['id'],
			'title'    => html_entity_decode( $L['title'], ENT_QUOTES, 'UTF-8' ),
			'url'      => $L['url'],
			'cover'    => $L['cover'],
			'deal'     => $L['deal'],
			'status'   => $L['status'],
			'price'    => $L['price'] ? nl_drop_price_text( $L['price'], 'he' ) . ( $L['deal'] === 'rent' ? ' לחודש' : '' ) : '',
			'editable' => $L['source'] === 'broker_drop',
			'live'     => get_post_status( $L['id'] ) === 'publish',
		);
	}
	return array( 'name' => $b['name_he'], 'site' => nl_drop_site_url( $b, 'he' ), 'listings' => $rows );
}

function nl_drop_rest_update( WP_REST_Request $req ) {
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	if ( nl_drop_rate( $b['id'], 'update', 120, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'יותר מדי עדכונים בשעה האחרונה.', array( 'status' => 429 ) ); }
	$id = (int) $req->get_param( 'id' );
	if ( get_post_type( $id ) !== 'nadlan_property' || (string) get_post_meta( $id, 'nl_broker_id', true ) !== (string) $b['id'] ) {
		return new WP_Error( 'nf', 'הנכס לא נמצא.', array( 'status' => 404 ) );
	}
	$twin = (int) get_post_meta( $id, 'nl_twin', true );
	if ( ! $twin ) {
		$tw = get_posts( array( 'post_type' => 'page', 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids', 'meta_query' => array( array( 'key' => 'nl_twin', 'value' => (string) $id ) ) ) );
		$twin = $tw ? (int) $tw[0] : 0;
	}
	$status = (string) $req->get_param( 'status' );
	if ( in_array( $status, array( 'sold', 'rented', 'active' ), true ) ) {
		foreach ( array_filter( array( $id, $twin ) ) as $pid ) {
			update_post_meta( $pid, 'nl_status', $status );
			update_post_meta( $pid, 'status', $status );
		}
		nl_drop_purge( array( $id, $twin, $b['site_he'], $b['site_en'] ) );
		return array( 'ok' => true, 'status' => $status );
	}
	$price = $req->get_param( 'price' );
	if ( $price !== null && $price !== '' ) {
		if ( (string) get_post_meta( $id, 'source', true ) !== 'broker_drop' ) { return new WP_Error( 'static', 'את המחיר של הנכס הזה מעדכנים מול nad-lan.', array( 'status' => 409 ) ); }
		$p = (int) preg_replace( '/\D+/', '', (string) $price );
		if ( $p < 500 || $p > 500000000 ) { return new WP_Error( 'price', 'המחיר לא נראה תקין.', array( 'status' => 400 ) ); }
		$f = json_decode( (string) get_post_meta( $id, 'nl_facts', true ), true );
		if ( ! is_array( $f ) ) { return new WP_Error( 'nofacts', 'לא ניתן לעדכן.', array( 'status' => 409 ) ); }
		$f['price'] = $p;
		update_post_meta( $id, 'nl_facts', wp_slash( wp_json_encode( $f, JSON_UNESCAPED_UNICODE ) ) );
		update_post_meta( $id, 'price', $p );
		nl_drop_render_pair( $id, $twin, $b );
		nl_drop_purge( array( $id, $twin, $b['site_he'], $b['site_en'] ) );
		return array( 'ok' => true, 'price' => nl_drop_price_text( $p, 'he' ) );
	}
	return new WP_Error( 'nothing', 'לא התקבל עדכון.', array( 'status' => 400 ) );
}

/* =====================================================================================================
 * The broker's own site: new properties first, off-market cards out, the counters right
 * ===================================================================================================== */
function nl_drop_remove_li( $html, $id ) {
	$p = strpos( $html, 'id="' . $id . '"' );
	if ( $p === false ) { return $html; }
	$start = strrpos( substr( $html, 0, $p ), '<li' );
	if ( $start === false ) { return $html; }
	$depth = 0;
	$i     = $start;
	$len   = strlen( $html );
	while ( $i < $len ) {
		$o = strpos( $html, '<li', $i );
		$c = strpos( $html, '</li>', $i );
		if ( $c === false ) { return $html; }
		if ( $o !== false && $o < $c ) { $depth++; $i = $o + 3; continue; }
		$depth--;
		$i = $c + 5;
		if ( $depth === 0 ) { return substr( $html, 0, $start ) . substr( $html, $i ); }
	}
	return $html;
}

function nl_drop_card_html( $L, $lang, $b ) {
	$he   = $lang !== 'en';
	$data = nl_drop_data_for( $L['id'], $b );
	if ( ! $data ) { return ''; }
	$f    = $data['facts'];
	$c    = $data['copy'][ $he ? 'he' : 'en' ];
	$deal = $L['deal'];
	$ttl  = nl_drop_fill( $c['card_title'] ?? $c['title'], $f, $lang );
	$url  = $L['url'];
	$cov  = ! empty( $data['photos'][0]['url'] ) ? $data['photos'][0]['url'] : $L['cover'];
	$area = $he ? ( $f['area_he'] ?: ( $f['city_he'] ?? '' ) ) : ( $f['area_en'] ?: ( $f['city_en'] ?? '' ) );
	$kick = trim( nl_drop_type_label( $f['property_type'] ?: 'apartment', $lang ) . ( $area !== '' ? ' · ' . $area : '' ) );
	$num  = function ( $n ) { return '<span class="nlb-num">' . esc_html( $n ) . '</span>'; };
	$h  = '<li class="nlb-lcard" data-deal="' . esc_attr( $deal ) . '" id="nlb-' . ( $he ? 'he' : 'en' ) . '-d' . (int) $L['id'] . '">' . "\n";
	$h .= '<a class="nlb-lcard-media" href="' . esc_url( $url ) . '" tabindex="-1" aria-hidden="true">' . ( $cov ? '<img src="' . esc_url( $cov ) . '" alt="" loading="lazy" decoding="async">' : '' );
	$h .= '<span class="nlb-badges"><span class="nlb-badge nlb-badge--' . esc_attr( $deal ) . '">' . esc_html( nl_drop_t( $lang, $deal ) ) . '</span></span></a>' . "\n";
	$h .= '<p class="nlb-lcard-kicker">' . esc_html( $kick ) . '</p>' . "\n";
	$h .= '<h3 class="nlb-lcard-title"><a href="' . esc_url( $url ) . '">' . esc_html( $ttl ) . '</a></h3>' . "\n";
	if ( ! empty( $f['price'] ) ) {
		$money = $he ? '<span>' . $num( nl_drop_fmt_int( $f['price'] ) ) . '&nbsp;₪</span>' : '<span>NIS&nbsp;' . $num( nl_drop_fmt_int( $f['price'] ) ) . '</span>';
		$sub   = '';
		if ( ! empty( $f['size_sqm'] ) ) {
			$ps  = nl_drop_fmt_int( round( $f['price'] / $f['size_sqm'] ) );
			$sub = $he ? '<span>' . $num( $ps ) . '&nbsp;₪ ' . ( $deal === 'rent' ? 'למ״ר לחודש' : 'למ״ר' ) . '</span>' : '<span>NIS&nbsp;' . $num( $ps ) . ' ' . ( $deal === 'rent' ? 'per sqm a month' : 'per sqm' ) . '</span>';
		}
		$h .= '<div class="nlb-price"><strong>' . $money . ( $deal === 'rent' ? ' <small>' . esc_html( nl_drop_t( $lang, 'month' ) ) . '</small>' : '' ) . '</strong>' . $sub . '</div>' . "\n";
	} else {
		$h .= '<div class="nlb-price"><strong class="nlb-ask">' . esc_html( nl_drop_t( $lang, $deal === 'rent' ? 'ask_short_rent' : 'ask_short' ) ) . '</strong><span>' . esc_html( nl_drop_t( $lang, 'ask_sub' ) ) . '</span></div>' . "\n";
	}
	$specs = array();
	if ( ! empty( $f['rooms'] ) ) { $specs[] = array( 'rooms', sprintf( esc_html( nl_drop_t( $lang, 'rooms_n' ) ), $num( nl_drop_fmt_num( $f['rooms'] ) ) ) ); }
	if ( ! empty( $f['size_sqm'] ) ) { $specs[] = array( 'area', sprintf( esc_html( nl_drop_t( $lang, 'size_n' ) ), $num( nl_drop_fmt_int( $f['size_sqm'] ) ) ) ); }
	if ( ! empty( $f['balcony_sqm'] ) ) { $specs[] = array( 'balcony', sprintf( esc_html( nl_drop_t( $lang, 'balcony_n' ) ), $num( nl_drop_fmt_int( $f['balcony_sqm'] ) ) ) ); }
	elseif ( ! empty( $f['garden_sqm'] ) ) { $specs[] = array( 'balcony', sprintf( esc_html( nl_drop_t( $lang, 'garden_n' ) ), $num( nl_drop_fmt_int( $f['garden_sqm'] ) ) ) ); }
	if ( isset( $f['floor'] ) && $f['floor'] !== null && $f['floor'] > 0 ) {
		$specs[] = array( 'floor', ! empty( $f['total_floors'] ) ? sprintf( esc_html( nl_drop_t( $lang, 'floor_of' ) ), $num( (int) $f['floor'] ), $num( (int) $f['total_floors'] ) ) : sprintf( esc_html( nl_drop_t( $lang, 'floor_n' ) ), $num( (int) $f['floor'] ) ) );
	}
	if ( $specs ) {
		$h .= '<ul class="nlb-specs">';
		foreach ( array_slice( $specs, 0, 4 ) as $s ) { $h .= '<li>' . nl_drop_icon( $s[0] ) . '<span>' . $s[1] . '</span></li>'; }
		$h .= '</ul>' . "\n";
	}
	$hi = array_slice( (array) ( $c['card_hi'] ?? array() ), 0, 3 );
	if ( $hi ) {
		$h .= '<ul class="nlb-hi">';
		foreach ( $hi as $x ) { $h .= '<li>' . esc_html( nl_drop_fill( $x, $f, $lang ) ) . '</li>'; }
		$h .= '</ul>' . "\n";
	}
	$amen = array();
	if ( ! empty( $f['parking'] ) ) { $amen[] = array( 'parking', ! empty( $f['parking_count'] ) && $f['parking_count'] > 1 ? sprintf( nl_drop_t( $lang, 'parking_n' ), (int) $f['parking_count'] ) : nl_drop_t( $lang, 'parking_1' ) ); }
	if ( ! empty( $f['storage'] ) ) { $amen[] = array( 'storage', nl_drop_t( $lang, 'f_storage' ) ); }
	if ( ! empty( $f['protected_room'] ) ) { $amen[] = array( 'shield', nl_drop_t( $lang, 'f_safe' ) ); }
	if ( ! empty( $f['elevator'] ) ) { $amen[] = array( 'lift', nl_drop_t( $lang, 'f_lift' ) ); }
	if ( $amen ) {
		$h .= '<div class="nlb-amen">';
		foreach ( array_slice( $amen, 0, 4 ) as $a ) { $h .= '<span>' . nl_drop_icon( $a[0] ) . esc_html( $a[1] ) . '</span>'; }
		$h .= '</div>' . "\n";
	}
	$entry = $he ? ( $f['entry_he'] ?? '' ) : ( $f['entry_en'] ?? '' );
	$date  = $he ? wp_date( 'j.n.Y', $L['modified'] ) : wp_date( 'j M Y', $L['modified'] );
	$h .= '<p class="nlb-lcard-meta">' . ( $entry ? '<span>' . nl_drop_icon( 'key' ) . esc_html( sprintf( nl_drop_t( $lang, 'entry_n' ), $entry ) ) . '</span>' : '<span></span>' ) . '<span class="nlb-num">' . esc_html( nl_drop_t( $lang, 'updated' ) . ' ' . $date ) . '</span></p>' . "\n";
	$wa = nl_drop_wa_link( $b, $lang, $ttl );
	$h .= '<div class="nlb-lcard-cta">';
	if ( $wa ) { $h .= '<a class="nlb-btn nlb-btn--sea" href="' . esc_url( $wa ) . '" target="_blank" rel="noopener" aria-label="' . esc_attr( nl_drop_t( $lang, 'wa' ) . ': ' . $ttl ) . '">' . nl_drop_icon( 'wa' ) . '<span>' . esc_html( nl_drop_t( $lang, 'wa' ) ) . '</span></a>'; }
	$h .= '<a class="nlb-btn nlb-btn--line" href="' . esc_url( $url ) . '" aria-label="' . esc_attr( nl_drop_t( $lang, 'card_view' ) . ': ' . $ttl ) . '"><span>' . esc_html( nl_drop_t( $lang, 'card_view' ) ) . '</span>' . nl_drop_icon( 'arrow' ) . '</a>';
	$h .= '</div>' . "\n" . '</li>' . "\n";
	return $h;
}

function nl_drop_is_current( $pid ) {
	return $pid && ! ( defined( 'REST_REQUEST' ) && REST_REQUEST ) && ! is_admin() && (int) $pid === (int) get_queried_object_id();
}

add_filter( 'the_content', function ( $html ) {
	$pid = (int) get_the_ID();
	if ( ! nl_drop_is_current( $pid ) ) { return $html; }
	$bid = (int) get_post_meta( $pid, 'nl_broker_site', true );
	if ( ! $bid || strpos( $html, '<ul class="nlb-grid">' ) === false ) { return $html; }
	$b = nl_drop_broker( $bid );
	if ( ! $b ) { return $html; }
	$lang = get_post_meta( $pid, 'nl_lang', true ) === 'en' ? 'en' : 'he';
	$all  = nl_drop_broker_listings( $bid, $lang );
	foreach ( $all as $L ) {
		if ( $L['card_key'] !== '' && $L['status'] !== 'active' ) { $html = nl_drop_remove_li( $html, 'nlb-' . $lang . '-' . $L['card_key'] ); }
	}
	$cards = '';
	foreach ( $all as $L ) {
		if ( $L['source'] === 'broker_drop' && $L['status'] === 'active' ) { $cards .= nl_drop_card_html( $L, $lang, $b ); }
	}
	if ( $cards !== '' ) {
		$pos  = strpos( $html, '<ul class="nlb-grid">' ) + strlen( '<ul class="nlb-grid">' );
		$html = substr( $html, 0, $pos ) . "\n" . $cards . substr( $html, $pos );
	}
	$sale = substr_count( $html, 'class="nlb-lcard" data-deal="sale"' );
	$rent = substr_count( $html, 'class="nlb-lcard" data-deal="rent"' );
	$html = preg_replace_callback( '/(<label class="nlb-l-(all|sale|rent)"[^>]*>[^<]*<span class="nlb-num">)\d+(<\/span>)/u', function ( $m ) use ( $sale, $rent ) {
		$n = $m[2] === 'all' ? $sale + $rent : ( $m[2] === 'sale' ? $sale : $rent );
		return $m[1] . $n . $m[3];
	}, $html );
	$html = preg_replace_callback( '/(<dt>(?:נכסים|Listings)<\/dt><dd><span class="nlb-num">)\d+(<\/span>)/u', function ( $m ) use ( $sale, $rent ) {
		return $m[1] . ( $sale + $rent ) . $m[2];
	}, $html );
	return $html;
}, 26 );

/* A property that is off the market says so at the top, and stops asking for viewings (reg. 19(c)). */
add_filter( 'the_content', function ( $html ) {
	$pid = (int) get_the_ID();
	if ( ! nl_drop_is_current( $pid ) ) { return $html; }
	$st = (string) get_post_meta( $pid, 'nl_status', true );
	if ( $st !== 'sold' && $st !== 'rented' ) { return $html; }
	$at = strpos( $html, '<div class="nlx-wrap">' );
	if ( $at === false ) { return $html; }
	$lang = get_post_type( $pid ) === 'page' ? 'en' : 'he';
	$b    = nl_drop_broker( get_post_meta( $pid, 'nl_broker_id', true ) );
	$site = $b ? nl_drop_site_url( $b, $lang ) : '';
	$name = $b ? ( $lang === 'en' ? $b['name_en'] : $b['name_he'] ) : '';
	$bar  = '<style>.nlx .nlx-soldbar{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;margin:16px 0 0;padding:12px 16px;border-radius:8px;background:#1F4B5C;color:#fff;font-weight:600}'
		. '.nlx .nlx-soldbar a{color:#fff!important;text-decoration:underline;font-weight:500}.nlx .nlx-rail .nlx-cta,.nlx .nlx-mbar,.nlx .nlx-agent .nlx-cta{display:none!important}</style>'
		. '<div class="nlx-soldbar" role="status"><span>' . esc_html( nl_drop_t( $lang, $st ) ) . '</span>'
		. ( $site ? '<a href="' . esc_url( $site ) . '">' . esc_html( sprintf( nl_drop_t( $lang, 'more' ), $name ) ) . '</a>' : '' ) . '</div>';
	$at += strlen( '<div class="nlx-wrap">' );
	return substr( $html, 0, $at ) . $bar . substr( $html, $at );
}, 25 );

/* =====================================================================================================
 * The address itself: /drop/<token>/  (a private tool page, never linked, never cached)
 * ===================================================================================================== */
add_action( 'parse_request', function () {
	$path = trim( (string) wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '', PHP_URL_PATH ), '/' );
	if ( ! preg_match( '#^drop/([a-z0-9]{24})$#', $path, $m ) ) { return; }
	nl_drop_page( $m[1] );
	exit;
}, 0 );

function nl_drop_page( $token ) {
	do_action( 'litespeed_control_set_nocache', 'nadlan broker drop page' );
	nocache_headers();
	header( 'Cache-Control: no-store, private, max-age=0' );
	header( 'X-LiteSpeed-Cache-Control: no-cache' );
	header( 'Referrer-Policy: no-referrer' );
	header( 'X-Frame-Options: SAMEORIGIN' );
	header( 'Content-Type: text/html; charset=utf-8' );
	$b = nl_drop_broker_by_token( $token );
	if ( ! $b ) {
		status_header( 404 );
		echo '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>nad-lan</title></head><body style="font-family:Arial,sans-serif;padding:40px 16px;color:#14212B;background:#F7F6F2"><p>הקישור הזה לא פעיל.</p></body></html>';
		return;
	}
	status_header( 200 );
	$cfg = array(
		'api'  => esc_url_raw( rest_url( 'nadlan/v1/drop/' . $token ) ),
		'name' => $b['name_he'],
		'site' => nl_drop_site_url( $b, 'he' ),
	);
	$css = nl_drop_page_css();
	$js  = nl_drop_page_js();
	$ex  = 'למכירה, 4 חדרים, 110 מ״ר, קומה 5 מתוך 8, מרפסת 12 מ״ר, חניה ומחסן, ממ״ד. רמת אביב החדשה. 4,200,000 ש״ח. כניסה מיידית. בלעדיות.';
	echo '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">';
	echo '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="referrer" content="no-referrer">';
	echo '<meta name="theme-color" content="#1F4B5C"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="' . esc_attr( 'שליחת נכס' ) . '">';
	echo '<title>' . esc_html( 'שליחת נכס · ' . $b['name_he'] ) . '</title>';
	echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>';
	echo '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Noto+Serif+Hebrew:wght@500;600&display=swap">';
	echo '<style>' . $css . '</style></head><body>';
	echo '<header class="top"><div class="wrap"><div class="who"><b>' . esc_html( $b['name_he'] ) . '</b><span>' . esc_html( $b['brand_he'] ) . '</span></div>';
	if ( $cfg['site'] ) { echo '<a class="tosite" href="' . esc_url( $cfg['site'] ) . '" target="_blank" rel="noopener">לאתר שלכם</a>'; }
	echo '</div></header><main class="wrap">';
	echo '<section class="card" aria-labelledby="h-new"><h1 id="h-new">נכס חדש</h1>';
	echo '<p class="lead">בוחרים תמונות, כותבים כמה שורות על הנכס ושולחים. העמוד נבנה ועולה לאתר שלכם בתוך דקה. אפשר גם להכתיב: נוגעים במיקרופון שבמקלדת ומדברים.</p>';
	echo '<form id="f" novalidate>';
	echo '<div class="pick"><input type="file" id="files" accept="image/*" multiple><label for="files" class="btn btn--ghost" id="pickbtn">' . nl_drop_icon( 'area' ) . '<span>בחירת תמונות</span></label><span class="count" id="count" aria-live="polite"></span></div>';
	echo '<ul class="thumbs" id="thumbs" aria-label="התמונות שנבחרו"></ul>';
	echo '<p class="hint" id="hint" hidden>התמונה הראשונה היא התמונה הראשית של העמוד. נגיעה בתמונה אחרת הופכת אותה לראשית.</p>';
	echo '<label for="txt" class="lbl">פרטי הנכס</label>';
	echo '<textarea id="txt" rows="7" dir="rtl" placeholder="' . esc_attr( 'לדוגמה: ' . $ex ) . '"></textarea>';
	echo '<p class="hint">כדאי לכתוב: למכירה או להשכרה, שכונה, חדרים, מ״ר, קומה, מרפסת, חניה ומחסן, מחיר, מתי אפשר להיכנס, ומה מיוחד בנכס. מה שלא נכתב לא יופיע בעמוד.</p>';
	echo '<div class="bar"><button type="submit" class="btn" id="send">שליחה והעלאה לאתר</button></div>';
	echo '</form><div class="status" id="status" role="status" aria-live="polite" hidden></div></section>';
	echo '<section class="card" aria-labelledby="h-mine"><h2 id="h-mine">הנכסים שלי</h2><p class="lead small">נכס שנמכר או הושכר מסמנים כאן בנגיעה אחת. העמוד שלו נשאר עם הודעה מתאימה, והכרטיס יורד מהאתר.</p><ul class="mine" id="mine"><li class="muted">טוען…</li></ul></section>';
	echo '<p class="foot">הקישור הזה אישי. כל מי שמחזיק בו יכול להעלות נכסים לאתר שלכם, ולכן שומרים אותו לעצמכם.</p>';
	echo '</main>';
	echo '<div class="sheet" id="sheet" hidden><div class="sheet-in" role="dialog" aria-modal="true" aria-labelledby="sheet-t"><p id="sheet-t"></p><div class="sheet-f" id="sheet-f"></div><div class="sheet-b"><button type="button" class="btn" id="sheet-ok">אישור</button><button type="button" class="btn btn--ghost" id="sheet-no">ביטול</button></div></div></div>';
	echo '<script>window.NLDROP=' . wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ';</script>';
	echo '<script>' . $js . '</script></body></html>';
}

function nl_drop_page_css() {
	return <<<'NLCSS'
:root{--paper:#F7F6F2;--surf:#FFFFFF;--ink:#14212B;--ink2:#3B4753;--mute:#6B7680;--line:#E3E1DA;--sea:#2F6F86;--seah:#255C70;--deep:#1F4B5C;--sand:#EEE9DD;--ok:#2E7D5B;--warn:#9A6A12;--bad:#B3261E;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--paper:#0F1A21;--surf:#16242D;--ink:#EEF2F4;--ink2:#C9D3D9;--mute:#93A2AC;--line:#2A3A44;--sea:#6FB3C9;--seah:#8CC4D6;--deep:#0B141A;--sand:#1E2E38;--ok:#6FC39A;--warn:#E0B35C;--bad:#F08A80;color-scheme:dark}}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--paper);color:var(--ink);font:17px/1.6 Assistant,'Segoe UI',Arial,sans-serif;padding-bottom:env(safe-area-inset-bottom,0px)}
.wrap{max-width:600px;margin:0 auto;padding-inline:16px}
.top{background:var(--deep);color:#fff;padding-top:env(safe-area-inset-top,0px)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:60px}
.who{display:flex;flex-direction:column;line-height:1.2}
.who b{font-family:'Noto Serif Hebrew','Noto Serif',Georgia,serif;font-weight:600;font-size:18px}
.who span{font-size:13px;opacity:.8}
.tosite{color:#fff;font-size:14px;text-decoration:underline;text-underline-offset:3px}
main.wrap{padding-block:20px 40px;display:flex;flex-direction:column;gap:18px}
.card{background:var(--surf);border:1px solid var(--line);border-radius:14px;padding:22px 18px}
h1,h2{font-family:'Noto Serif Hebrew','Noto Serif',Georgia,serif;font-weight:600;margin:0 0 6px;line-height:1.25;text-wrap:balance}
h1{font-size:26px}
h2{font-size:21px}
.lead{margin:0 0 16px;color:var(--ink2)}
.lead.small{font-size:15px}
.pick{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.pick input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
.count{font-size:15px;color:var(--mute);font-variant-numeric:tabular-nums}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:50px;padding:10px 20px;border-radius:999px;border:1px solid var(--sea);background:var(--sea);color:#fff;font:700 17px/1.2 Assistant,'Segoe UI',Arial,sans-serif;cursor:pointer;text-decoration:none}
.btn:hover{background:var(--seah);border-color:var(--seah)}
.btn:disabled{opacity:.55;cursor:default}
.btn svg{width:20px;height:20px}
.btn--ghost{background:transparent;color:var(--sea)}
.btn--ghost:hover{background:var(--sand);color:var(--ink)}
.btn--small{min-height:38px;padding:6px 14px;font-size:15px;font-weight:600}
:focus-visible{outline:3px solid var(--sea);outline-offset:2px}
.pick input:focus-visible+label{outline:3px solid var(--sea);outline-offset:2px}
.thumbs{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.thumbs:empty{display:none}
.thumbs li{position:relative;aspect-ratio:1;border-radius:10px;overflow:hidden;background:var(--sand)}
.thumbs button.face{all:unset;display:block;width:100%;height:100%;cursor:pointer}
.thumbs img{width:100%;height:100%;object-fit:cover;display:block}
.thumbs .cover{position:absolute;top:6px;inset-inline-start:6px;background:var(--deep);color:#fff;font-size:12px;font-weight:700;padding:2px 8px;border-radius:999px}
.thumbs .x{position:absolute;top:4px;inset-inline-end:4px;width:30px;height:30px;border-radius:50%;border:0;background:rgba(20,33,43,.72);color:#fff;font-size:18px;line-height:30px;cursor:pointer}
.thumbs .st{position:absolute;inset-inline:0;bottom:0;height:4px;background:transparent}
.thumbs li[data-s="up"] .st{background:linear-gradient(90deg,var(--sea),var(--sand));animation:nlp 1.1s linear infinite;background-size:200% 100%}
.thumbs li[data-s="ok"] .st{background:var(--ok)}
.thumbs li[data-s="err"] .st{background:var(--bad)}
@keyframes nlp{to{background-position:-200% 0}}
@media (prefers-reduced-motion:reduce){.thumbs li[data-s="up"] .st{animation:none}}
.hint{font-size:14px;color:var(--mute);margin:8px 0 0}
.lbl{display:block;font-weight:700;margin:18px 0 6px}
textarea{width:100%;min-height:150px;border:1px solid var(--line);border-radius:12px;padding:12px 14px;font:17px/1.55 Assistant,'Segoe UI',Arial,sans-serif;background:var(--paper);color:var(--ink);resize:vertical}
textarea:focus{outline:3px solid var(--sea);outline-offset:1px;border-color:transparent}
.bar{margin-top:16px}
.bar .btn{width:100%}
@media (max-width:640px){.bar{position:sticky;bottom:0;margin-inline:-18px;padding:12px 18px calc(12px + env(safe-area-inset-bottom,0px));background:var(--surf);border-top:1px solid var(--line)}}
.status{margin-top:16px;padding:14px 16px;border-radius:12px;background:var(--sand);color:var(--ink)}
.status b{display:block;font-size:18px;margin-bottom:4px}
.status[data-k="ok"]{background:color-mix(in srgb,var(--ok) 14%,var(--surf));border:1px solid var(--ok)}
.status[data-k="warn"]{background:color-mix(in srgb,var(--warn) 14%,var(--surf));border:1px solid var(--warn)}
.status[data-k="bad"]{background:color-mix(in srgb,var(--bad) 12%,var(--surf));border:1px solid var(--bad)}
.status .row{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}
.status ul{margin:6px 0 0;padding-inline-start:20px}
.mine{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-direction:column}
.mine li{display:grid;grid-template-columns:64px 1fr;gap:12px;padding:12px 0;border-top:1px solid var(--line)}
.mine li:first-child{border-top:0}
.mine li.muted{display:block;color:var(--mute)}
.mine img,.mine .ph{width:64px;height:64px;border-radius:10px;object-fit:cover;background:var(--sand);display:block}
.mine .t{font-weight:700;line-height:1.35}
.mine .t a{color:var(--ink);text-decoration:none}
.mine .t a:hover{text-decoration:underline}
.mine .m{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;font-size:14px;color:var(--mute);margin-top:2px}
.pill{display:inline-block;padding:1px 10px;border-radius:999px;font-size:13px;font-weight:700;border:1px solid var(--line)}
.pill--active{color:var(--ok);border-color:var(--ok)}
.pill--sold,.pill--rented{color:var(--warn);border-color:var(--warn)}
.pill--draft{color:var(--mute)}
.acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;grid-column:2}
.foot{font-size:13px;color:var(--mute);text-align:center;margin:4px 0 0}
.sheet{position:fixed;inset:0;background:rgba(15,26,33,.55);display:flex;align-items:flex-end;justify-content:center;z-index:9;padding:16px}
.sheet-in{background:var(--surf);color:var(--ink);border-radius:16px;padding:20px;width:100%;max-width:520px;margin-bottom:env(safe-area-inset-bottom,0px)}
.sheet-in p{margin:0 0 12px;font-weight:600}
.sheet-f input{width:100%;min-height:48px;border:1px solid var(--line);border-radius:10px;padding:8px 12px;font:18px Assistant,Arial,sans-serif;background:var(--paper);color:var(--ink);direction:ltr;text-align:right;font-variant-numeric:tabular-nums}
.sheet-b{display:flex;gap:10px;margin-top:14px}
.sheet-b .btn{flex:1}
[hidden]{display:none!important}
NLCSS;
}

function nl_drop_page_js() {
	return <<<'NLJS'
(function(){
'use strict';
var C=window.NLDROP||{},api=C.api||'';
var $=function(id){return document.getElementById(id);};
var items=[],seq=0,busy=false;
var files=$('files'),thumbs=$('thumbs'),count=$('count'),hint=$('hint'),txt=$('txt'),send=$('send'),statusEl=$('status'),mine=$('mine');
try{var d=localStorage.getItem('nldrop-draft');if(d&&!txt.value){txt.value=d;}}catch(e){}
txt.addEventListener('input',function(){try{localStorage.setItem('nldrop-draft',txt.value);}catch(e){}});
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function say(kind,html){statusEl.hidden=false;statusEl.setAttribute('data-k',kind||'');statusEl.innerHTML=html;}
function shrink(file){
  return new Promise(function(res){
    var url=URL.createObjectURL(file),img=new Image();
    img.onload=function(){
      try{
        var max=2400,w=img.naturalWidth,h=img.naturalHeight,s=Math.min(1,max/Math.max(w,h));
        var c=document.createElement('canvas');c.width=Math.round(w*s);c.height=Math.round(h*s);
        c.getContext('2d').drawImage(img,0,0,c.width,c.height);
        c.toBlob(function(b){URL.revokeObjectURL(url);res(b||file);},'image/jpeg',0.86);
      }catch(e){URL.revokeObjectURL(url);res(file);}
    };
    img.onerror=function(){URL.revokeObjectURL(url);res(file);};
    img.src=url;
  });
}
function render(){
  thumbs.innerHTML='';
  items.forEach(function(it,i){
    var li=document.createElement('li');li.setAttribute('data-s',it.s);
    li.innerHTML='<button type="button" class="face" aria-label="'+(i?'הפיכה לתמונה הראשית':'התמונה הראשית')+'"><img alt="" src="'+it.preview+'"></button>'+(i===0?'<span class="cover">ראשית</span>':'')+'<button type="button" class="x" aria-label="הסרת התמונה">×</button><span class="st"></span>';
    li.querySelector('.face').addEventListener('click',function(){if(i>0){items.unshift(items.splice(i,1)[0]);render();}});
    li.querySelector('.x').addEventListener('click',function(){items.splice(i,1);render();});
    thumbs.appendChild(li);
  });
  var up=items.filter(function(x){return x.s==='up';}).length;
  count.textContent=items.length?(items.length+' תמונות'+(up?', מעלים '+up:'')):'';
  hint.hidden=items.length<2;
}
function upload(it){
  it.s='up';render();
  return shrink(it.file).then(function(blob){
    var fd=new FormData();fd.append('photo',blob,'photo.jpg');
    return fetch(api+'/photo',{method:'POST',body:fd,credentials:'omit'});
  }).then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j};});})
  .then(function(x){if(x.ok&&x.j&&x.j.id){it.id=x.j.id;it.s='ok';}else{it.s='err';it.err=(x.j&&x.j.message)||'';}render();})
  .catch(function(){it.s='err';render();});
}
var queue=Promise.resolve();
files.addEventListener('change',function(){
  Array.prototype.forEach.call(files.files,function(f){
    if(!/^image\//.test(f.type)&&!/\.(heic|heif|jpe?g|png|webp)$/i.test(f.name)){return;}
    var it={k:++seq,file:f,preview:URL.createObjectURL(f),s:'wait',id:0};
    items.push(it);
    queue=queue.then(function(){return items.indexOf(it)>-1?upload(it):null;});
  });
  files.value='';render();
});
function post(path,body){
  return fetch(api+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body||{}),credentials:'omit'})
    .then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j};});});
}
$('f').addEventListener('submit',function(e){
  e.preventDefault();if(busy){return;}
  var text=txt.value.trim();
  if(!items.length){say('warn','<b>חסרות תמונות</b>בוחרים לפחות תמונה אחת של הנכס.');return;}
  if(text.length<8){say('warn','<b>חסרים פרטים</b>כותבים כמה שורות על הנכס: חדרים, שטח, שכונה ומחיר.');txt.focus();return;}
  busy=true;send.disabled=true;
  say('','<b>מעלים את התמונות</b>עוד רגע.');
  queue.then(function(){
    var failed=items.filter(function(x){return x.s==='err';});
    if(failed.length){
      say('warn','<b>'+failed.length+' תמונות לא עלו</b>אפשר להסיר אותן בנגיעה ב-× ולשלוח שוב, או לבחור אותן מחדש.');
      throw 'stop';
    }
    say('','<b>קוראים את הפרטים</b>זה לוקח כמה שניות.');
    return post('/submit',{text:text,photos:items.map(function(x){return x.id;})});
  }).then(function(x){
    if(!x.ok){say('bad','<b>השליחה לא עברה</b>'+esc((x.j&&x.j.message)||'אפשר לנסות שוב בעוד רגע.'));throw 'stop';}
    if(x.j.state==='held'){
      say('warn','<b>חסרים כמה פרטים כדי לבנות עמוד</b>'+(x.j.summary?'<div>הבנו: '+esc(x.j.summary)+'</div>':'')+'<ul>'+(x.j.missing||[]).map(function(m){return '<li>'+esc(m)+'</li>';}).join('')+'</ul><div>מוסיפים אותם בטקסט ושולחים שוב. התמונות כבר למעלה.</div>');
      throw 'stop';
    }
    say('','<b>כותבים את העמוד</b>'+esc(x.j.summary||'')+'<div>עד דקה.</div>');
    var drop=x.j.drop;
    return post('/build/'+drop,{}).catch(function(){return post('/build/'+drop,{});});
  }).then(function(x){
    if(!x||!x.ok||!x.j||!x.j.url_he){say('bad','<b>בניית העמוד לא הושלמה</b>אפשר ללחוץ שוב על שליחה. שום דבר לא יוכפל.');throw 'stop';}
    var live=x.j.state==='published';
    say('ok','<b>'+(live?'הנכס עלה לאתר':'העמוד נשמר כטיוטה')+'</b>'+esc(x.j.title||'')+'<div class="row"><a class="btn btn--small" href="'+esc(x.j.url_he)+'" target="_blank" rel="noopener">לצפייה בעמוד</a>'+(x.j.url_en?'<a class="btn btn--small btn--ghost" href="'+esc(x.j.url_en)+'" target="_blank" rel="noopener">בעמוד באנגלית</a>':'')+'<button type="button" class="btn btn--small btn--ghost" id="again">נכס נוסף</button></div>');
    var again=$('again');if(again){again.addEventListener('click',function(){items=[];render();txt.value='';try{localStorage.removeItem('nldrop-draft');}catch(e){}statusEl.hidden=true;window.scrollTo(0,0);});}
    try{localStorage.removeItem('nldrop-draft');}catch(e){}
    load();
  }).catch(function(err){if(err!=='stop'){say('bad','<b>אין חיבור</b>בודקים את האינטרנט ושולחים שוב.');}})
  .then(function(){busy=false;send.disabled=false;});
});
/* confirmations live in the page, never in browser pop-ups */
var sheet=$('sheet'),sheetT=$('sheet-t'),sheetF=$('sheet-f'),okB=$('sheet-ok'),noB=$('sheet-no'),onOk=null;
function ask(text,withInput,cb){sheetT.textContent=text;sheetF.innerHTML=withInput?'<input id="sheet-in" inputmode="numeric" autocomplete="off" aria-label="מחיר חדש בש״ח">':'';onOk=cb;sheet.hidden=false;var i=$('sheet-in');(i||okB).focus();}
okB.addEventListener('click',function(){var i=$('sheet-in'),v=i?i.value:'';sheet.hidden=true;if(onOk){onOk(v);}});
noB.addEventListener('click',function(){sheet.hidden=true;});
sheet.addEventListener('click',function(e){if(e.target===sheet){sheet.hidden=true;}});
function load(){
  fetch(api+'/listings',{credentials:'omit'}).then(function(r){return r.json();}).then(function(j){
    var L=(j&&j.listings)||[];
    if(!L.length){mine.innerHTML='<li class="muted">עוד אין נכסים. הנכס הראשון יופיע כאן.</li>';return;}
    mine.innerHTML='';
    L.forEach(function(x){
      var li=document.createElement('li');
      var st=x.live?x.status:'draft',lab={active:'באוויר',sold:'נמכר',rented:'הושכר',draft:'טיוטה'}[st];
      var off=x.deal==='rent'?'rented':'sold',offLab=x.deal==='rent'?'הושכר':'נמכר';
      li.innerHTML=(x.cover?'<img alt="" src="'+esc(x.cover)+'">':'<span class="ph"></span>')+
        '<div><div class="t"><a href="'+esc(x.url)+'" target="_blank" rel="noopener">'+esc(x.title)+'</a></div><div class="m"><span class="pill pill--'+st+'">'+lab+'</span>'+(x.price?'<span>'+esc(x.price)+'</span>':'')+'</div></div>'+
        '<div class="acts">'+(x.status==='active'?'<button type="button" class="btn btn--small btn--ghost" data-a="off">'+offLab+'</button>':'<button type="button" class="btn btn--small btn--ghost" data-a="on">החזרה לפרסום</button>')+(x.editable?'<button type="button" class="btn btn--small btn--ghost" data-a="price">עדכון מחיר</button>':'')+'</div>';
      var bOff=li.querySelector('[data-a="off"]'),bOn=li.querySelector('[data-a="on"]'),bP=li.querySelector('[data-a="price"]');
      if(bOff){bOff.addEventListener('click',function(){ask('לסמן את "'+x.title+'" כ'+offLab+'? העמוד יישאר עם הודעה, והכרטיס יירד מהאתר שלכם.',false,function(){post('/update',{id:x.id,status:off}).then(load);});});}
      if(bOn){bOn.addEventListener('click',function(){post('/update',{id:x.id,status:'active'}).then(load);});}
      if(bP){bP.addEventListener('click',function(){ask('מחיר חדש בש״ח ל"'+x.title+'"',true,function(v){if(!v){return;}post('/update',{id:x.id,price:v}).then(function(r){if(!r.ok){say('bad','<b>המחיר לא עודכן</b>'+esc((r.j&&r.j.message)||''));}load();});});});}
      mine.appendChild(li);
    });
  }).catch(function(){mine.innerHTML='<li class="muted">לא הצלחנו לטעון את הרשימה. מרעננים את העמוד.</li>';});
}
load();render();
})();
NLJS;
}

/* =====================================================================================================
 * Admin: the broker record gets its link; the log lists every submission
 * ===================================================================================================== */
add_action( 'add_meta_boxes_nadlan_professional', function () {
	add_meta_box( 'nl_drop_box', 'תיבת נכסים: קישור שליחה אישי', 'nl_drop_metabox', 'nadlan_professional', 'side', 'high' );
} );

function nl_drop_metabox( $post ) {
	$b = nl_drop_broker( $post->ID );
	wp_nonce_field( 'nl_drop_save', 'nl_drop_nonce' );
	$url = ( $b && $b['token'] !== '' ) ? home_url( '/drop/' . $b['token'] . '/' ) : '';
	echo '<p><label><input type="checkbox" name="nl_drop_on" value="1"' . checked( $b && $b['on'], true, false ) . '> פעילה</label></p>';
	if ( $url && $b['on'] ) {
		echo '<p style="margin:6px 0 2px">הקישור ששולחים למתווך:</p><input type="text" readonly value="' . esc_attr( $url ) . '" style="width:100%;direction:ltr" onclick="this.select()">';
		echo '<p><label><input type="checkbox" name="nl_drop_rotate" value="1"> קישור חדש (הקישור הקודם יפסיק לעבוד)</label></p>';
	}
	$fields = array( 'nl_name_he' => 'שם בעברית', 'nl_name_en' => 'שם באנגלית', 'nl_brand_en' => 'שם העסק באנגלית', 'nl_site_he' => 'מזהה עמוד האתר בעברית', 'nl_site_en' => 'מזהה עמוד האתר באנגלית' );
	foreach ( $fields as $k => $label ) {
		echo '<p style="margin:8px 0 2px">' . esc_html( $label ) . '</p><input type="text" name="' . esc_attr( $k ) . '" value="' . esc_attr( (string) get_post_meta( $post->ID, $k, true ) ) . '" style="width:100%">';
	}
	$g = (string) get_post_meta( $post->ID, 'nl_gender', true );
	echo '<p style="margin:8px 0 2px">לשון</p><select name="nl_gender"><option value="m"' . selected( $g !== 'f', true, false ) . '>מתווך</option><option value="f"' . selected( $g, 'f', false ) . '>מתווכת</option></select>';
	echo '<p><label><input type="checkbox" name="nl_auto_publish" value="1"' . checked( ! $b || $b['auto'], true, false ) . '> פרסום מיידי (בלי: נשמר כטיוטה)</label></p>';
	echo '<p class="description">רישיון ותיווך מגיעים מהשדות "מספר רישיון" ו"טלפון" של הכרטיס.</p>';
}

add_action( 'save_post_nadlan_professional', function ( $pid ) {
	if ( ! isset( $_POST['nl_drop_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nl_drop_nonce'] ) ), 'nl_drop_save' ) ) { return; }
	if ( ! current_user_can( 'edit_post', $pid ) || wp_is_post_revision( $pid ) ) { return; }
	$on = ! empty( $_POST['nl_drop_on'] );
	update_post_meta( $pid, 'nl_drop_on', $on ? '1' : '0' );
	if ( $on && ( (string) get_post_meta( $pid, 'nl_drop_token', true ) === '' || ! empty( $_POST['nl_drop_rotate'] ) ) ) {
		update_post_meta( $pid, 'nl_drop_token', nl_drop_new_token() );
	}
	foreach ( array( 'nl_name_he', 'nl_name_en', 'nl_brand_en' ) as $k ) {
		if ( isset( $_POST[ $k ] ) ) { update_post_meta( $pid, $k, sanitize_text_field( wp_unslash( $_POST[ $k ] ) ) ); }
	}
	foreach ( array( 'nl_site_he', 'nl_site_en' ) as $k ) {
		if ( isset( $_POST[ $k ] ) ) { update_post_meta( $pid, $k, (string) absint( wp_unslash( $_POST[ $k ] ) ) ); }
	}
	update_post_meta( $pid, 'nl_gender', ( isset( $_POST['nl_gender'] ) && $_POST['nl_gender'] === 'f' ) ? 'f' : 'm' );
	update_post_meta( $pid, 'nl_auto_publish', ! empty( $_POST['nl_auto_publish'] ) ? '1' : '0' );
} );

add_filter( 'manage_nadlan_drop_posts_columns', function ( $cols ) {
	return array( 'cb' => $cols['cb'] ?? '', 'title' => 'שליחה', 'nl_state' => 'מצב', 'nl_page' => 'העמוד', 'date' => 'תאריך' );
} );

add_action( 'manage_nadlan_drop_posts_custom_column', function ( $col, $pid ) {
	if ( $col === 'nl_state' ) {
		$map = array( 'reading' => 'בקריאה', 'held' => 'חסרים פרטים', 'ready' => 'מוכן לבנייה', 'writing' => 'בכתיבה', 'published' => 'פורסם', 'draft' => 'טיוטה', 'failed' => 'נכשל' );
		$st  = (string) get_post_meta( $pid, 'nl_state', true );
		echo esc_html( $map[ $st ] ?? $st );
		$miss = (array) get_post_meta( $pid, 'nl_missing', true );
		if ( $st === 'held' && $miss ) { echo '<br><small>' . esc_html( implode( ', ', $miss ) ) . '</small>'; }
	}
	if ( $col === 'nl_page' ) {
		$r = get_post_meta( $pid, 'nl_result', true );
		if ( is_array( $r ) && ! empty( $r['url_he'] ) ) {
			echo '<a href="' . esc_url( $r['url_he'] ) . '" target="_blank" rel="noopener">עברית</a>';
			if ( ! empty( $r['url_en'] ) ) { echo ' · <a href="' . esc_url( $r['url_en'] ) . '" target="_blank" rel="noopener">English</a>'; }
		}
	}
}, 10, 2 );

/* =====================================================================================================
 * Health
 * ===================================================================================================== */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$since = gmdate( 'Y-m-d H:i:s', time() - 7 * DAY_IN_SECONDS );
	$q     = function ( $state = null ) use ( $since ) {
		$a = array( 'post_type' => 'nadlan_drop', 'post_status' => 'private', 'fields' => 'ids', 'numberposts' => 500, 'date_query' => array( array( 'after' => $since, 'column' => 'post_date_gmt' ) ), 'suppress_filters' => true );
		if ( $state ) { $a['meta_query'] = array( array( 'key' => 'nl_state', 'value' => $state ) ); }
		return count( get_posts( $a ) );
	};
	$out['broker_drop'] = array(
		'version'      => NL_DROP_VERSION,
		'brokers_on'   => count( get_posts( array( 'post_type' => 'nadlan_professional', 'fields' => 'ids', 'numberposts' => 200, 'meta_query' => array( array( 'key' => 'nl_drop_on', 'value' => '1' ) ), 'suppress_filters' => true ) ) ),
		'drops_7d'     => $q(),
		'published_7d' => $q( 'published' ),
		'held_7d'      => $q( 'held' ),
	);
	return $out;
} );
