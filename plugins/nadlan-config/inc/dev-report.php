<?php
/**
 * nadlan-config - Developer buyer report (v1.0.0, 19.11.2026, Linear HAD-791, package 5 of the long-film gaps 10 and 11).
 *
 * Ben's film says "this is not a lead, this is a buyer": a developer gets, per project, what buyers chose and did before they
 * asked, with REAL counts only, from our own visit trail (inc/visit-trail.php, which requires this file):
 *  - the funnel: visits to the project, chose a floor or an apartment, opened the view, designed the apartment, checked the
 *    monthly payment, saved or added to the basket, asked for a call, sent an offer request, wrote on WhatsApp or phoned,
 *    left details. Each row counts distinct visits (visit ids), never a guess, never a model;
 *  - the floors chosen, the directions looked at, language, device, country, visits per day;
 *  - anonymous journeys (no name, no phone, no IP: country, language, device and the steps);
 *  - CSV export (Excel opens it, UTF-8 with BOM).
 * Access: GET /wp-json/nadlan/v1/dev-report?p=<project>&x=<expiry>&s=<signature>[&d=7|30|90|365][&l=he|en][&fmt=csv].
 *   The signature is an HMAC-SHA256 of "p|x|rev" with a key derived from the site's own salt; rev is the project's revocation
 *   counter (option nadlan_dr_rev): "ביטול הקישורים" in the admin screen raises it and every earlier link of that project stops.
 *   The link expires at x. The page is not linked from anywhere on the site; it sends Referrer-Policy: no-referrer so the link
 *   never leaks through a click. (No robots header is added: indexing decisions are Ben's, by his standing law.)
 * Admin: "דוח ליזם" under Lead Inbox (manage_options): pick a project, choose how long the link lives, copy it; preview as admin.
 * Design: Claude Design board https://claude.ai/artifact/UQcFLQxz3vwmKn1nWag5Rq (survey paper #EEF2F5, ink #0D1B2A, cobalt
 *   #1E4FD6, money-step teal #0B7A6F; IBM Plex Sans Hebrew + IBM Plex Mono for figures). No long dashes, no traffic numbers on any
 *   public page (this report is reachable only with a signed link or as an administrator).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
if ( defined( 'NADLAN_DR_VERSION' ) ) { return; }
define( 'NADLAN_DR_VERSION', '1.0.1' );

/** 1.0.1: the anonymous journeys reach a developer's signed link only after the lawyer's OK on the privacy wording (HAD-797);
 *  until then the option nadlan_dr_journeys stays '0' and a developer sees the totals only. The admin preview always shows them. */
function nadlan_dr_journeys_public() { return '1' === (string) get_option( 'nadlan_dr_journeys', '0' ); }

/* ---------------------------------------------------------------- signing */

function nadlan_dr_key() {
	return hash_hmac( 'sha256', 'nadlan-dev-report-v1', wp_salt( 'auth' ) );
}

function nadlan_dr_rev( $p ) {
	$all = get_option( 'nadlan_dr_rev', array() );
	return is_array( $all ) ? (int) ( $all[ (int) $p ] ?? 0 ) : 0;
}

function nadlan_dr_sig( $p, $x ) {
	return substr( hash_hmac( 'sha256', (int) $p . '|' . (int) $x . '|' . nadlan_dr_rev( $p ), nadlan_dr_key() ), 0, 32 );
}

function nadlan_dr_url( $p, $x, $args = array() ) {
	return add_query_arg( array_merge( array( 'p' => (int) $p, 'x' => (int) $x, 's' => nadlan_dr_sig( $p, $x ) ), $args ), rest_url( 'nadlan/v1/dev-report' ) );
}

/** true when the signed request is valid now */
function nadlan_dr_valid( $p, $x, $s ) {
	$p = (int) $p;
	$x = (int) $x;
	if ( $p <= 0 || $x < time() || ! is_string( $s ) || ! preg_match( '/^[a-f0-9]{32}$/', $s ) ) { return false; }
	if ( $x > time() + 400 * DAY_IN_SECONDS ) { return false; }
	return hash_equals( nadlan_dr_sig( $p, $x ), $s ) && nadlan_vt_canon_project( $p ) === $p;
}

/* ---------------------------------------------------------------- the funnel */

/** the funnel rows, in order: key => array( Hebrew, English, money step? ) */
function nadlan_dr_steps_def() {
	return array(
		'visit'   => array( 'ביקורים בפרויקט', 'Visits to the project', 0 ),
		'floor'   => array( 'בחרו קומה או דירה', 'Chose a floor or an apartment', 0 ),
		'view'    => array( 'פתחו את הנוף', 'Opened the view', 0 ),
		'design'  => array( 'עיצבו את הדירה', 'Designed the apartment', 0 ),
		'pay'     => array( 'בדקו החזר חודשי', 'Checked the monthly payment', 0 ),
		'basket'  => array( 'שמרו או הוסיפו לסל', 'Saved or added to the basket', 0 ),
		'call'    => array( 'ביקשו שיחה או פגישה', 'Asked for a call or a meeting', 1 ),
		'rfp'     => array( 'שלחו בקשה להצעה', 'Sent an offer request', 1 ),
		'reserve' => array( 'ביקשו לשריין דירה', 'Asked to reserve an apartment', 1 ),
		'contact' => array( 'פנו בוואטסאפ או בטלפון', 'Wrote on WhatsApp or phoned', 1 ),
		'lead'    => array( 'השאירו פרטים', 'Left their details', 1 ),
	);
}

/** the funnel steps one recorded event belongs to (an automatic pick of the page is not a choice) */
function nadlan_dr_steps_of( $ev, $d ) {
	$d    = is_array( $d ) ? $d : array();
	$auto = isset( $d['src'] ) && '' !== (string) $d['src'] && ! in_array( (string) $d['src'], array( 'user', 'engine', 'ga' ), true );
	switch ( $ev ) {
		case 'floor':
		case 'facing':
			return $auto ? array() : array( 'floor' );
		case 'fcta':
			return array( 'floor', 'contact' );
		case 'example':
		case 'tour':
			return ! empty( $d['o'] ) ? array( 'floor' ) : array();
		case 'view':
			return array( 'view' );
		case 'faction':
			$a = (string) ( $d['a'] ?? '' );
			return 'view' === $a ? array( 'floor', 'view' ) : ( 'design' === $a ? array( 'floor', 'design' ) : array( 'floor' ) );
		case 'click':
			$k = (string) ( $d['k'] ?? '' );
			if ( 'deal_floor' === $k ) { return array( 'floor' ); }
			if ( 'book_send' === $k ) { return array( 'call' ); }
			if ( in_array( $k, array( 'wa', 'tel', 'mail' ), true ) ) { return array( 'contact' ); }
			return array();
		case 'form':
			return 'book' === (string) ( $d['k'] ?? '' ) ? array( 'call' ) : array();
		case 'act':
			$n   = (string) ( $d['n'] ?? '' );
			$map = array(
				'floor_select' => 'floor', 'direction_select' => 'floor', 'unit_open' => 'floor', 'plan_open' => 'floor', 'tour_open' => 'floor',
				'compare_open' => 'floor', 'showroom_pick' => 'floor', 'cockpit_open' => 'floor',
				'view_open' => 'view', 'view_turn' => 'view', 'journey_view' => 'view',
				'designer_open' => 'design', 'designer_action' => 'design',
				'mortgage_check' => 'pay',
				'basket_add' => 'basket', 'favorite' => 'basket', 'cockpit_save' => 'basket', 'cockpit_basket' => 'basket', 'basket_team_add' => 'basket',
				'call_book' => 'call', 'call_join' => 'call', 'room_join' => 'call', 'room_create' => 'call', 'cockpit_room' => 'call', 'basket_room' => 'call', 'offer_video' => 'call',
				'rfp_send' => 'rfp', 'offer_sent' => 'rfp', 'basket_send' => 'rfp',
				'reserve_request' => 'reserve', 'reserve_start' => 'floor',
				'cockpit_wa' => 'contact', 'offer_wa' => 'contact', 'cockpit_call' => 'contact',
			);
			if ( 'design_order' === $n ) { return array( 'design', 'basket' ); }
			if ( isset( $map[ $n ] ) ) { return array( $map[ $n ] ); }
			if ( 0 === strpos( $n, 'mortgage_' ) ) { return array( 'pay' ); }
			return array();
	}
	return array();
}

/** a direction as one word in the report's language (the stage sends Hebrew words or a bearing, the engine English keys) */
function nadlan_dr_dir( $d, $lang ) {
	$en  = 'en' === $lang;
	$raw = strtolower( trim( (string) ( $d['dir'] ?? '' ) ) );
	$he2en = array( 'צפון' => 'north', 'צפון מזרח' => 'north-east', 'מזרח' => 'east', 'דרום מזרח' => 'south-east', 'דרום' => 'south',
		'דרום מערב' => 'south-west', 'מערב' => 'west', 'צפון מערב' => 'north-west' );
	$en2he = array_flip( $he2en );
	$raw = str_replace( array( '_', ' ' ), '-', $raw );
	if ( isset( $en2he[ $raw ] ) ) { return $en ? $raw : $en2he[ $raw ]; }
	$heRaw = str_replace( '-', ' ', (string) ( $d['dir'] ?? '' ) );
	if ( isset( $he2en[ $heRaw ] ) ) { return $en ? $he2en[ $heRaw ] : $heRaw; }
	if ( isset( $d['b'] ) && '' !== (string) $d['b'] ) { return $en ? nadlan_vt_dir_word_en( (int) $d['b'] ) : nadlan_vt_dir_word( (int) $d['b'] ); }
	return '';
}

function nadlan_dr_country( $c, $lang ) {
	$c = strtoupper( (string) $c );
	if ( '' === $c ) { return 'en' === $lang ? 'unknown' : 'לא ידוע'; }
	if ( 'en' === $lang ) { return $c; }
	$m = array( 'IL' => 'ישראל', 'FR' => 'צרפת', 'US' => 'ארה״ב', 'GB' => 'בריטניה', 'RU' => 'רוסיה', 'UA' => 'אוקראינה', 'DE' => 'גרמניה',
		'CA' => 'קנדה', 'BE' => 'בלגיה', 'CH' => 'שווייץ', 'AU' => 'אוסטרליה', 'NL' => 'הולנד', 'IT' => 'איטליה', 'ES' => 'ספרד',
		'AE' => 'איחוד האמירויות', 'CY' => 'קפריסין', 'BR' => 'ברזיל', 'AR' => 'ארגנטינה', 'MX' => 'מקסיקו', 'ZA' => 'דרום אפריקה',
		'PL' => 'פולין', 'AT' => 'אוסטריה', 'SE' => 'שוודיה', 'IE' => 'אירלנד', 'PT' => 'פורטוגל', 'GR' => 'יוון', 'TR' => 'טורקיה',
		'JO' => 'ירדן', 'EG' => 'מצרים', 'IN' => 'הודו', 'SG' => 'סינגפור', 'KZ' => 'קזחסטן', 'GE' => 'גאורגיה', 'MA' => 'מרוקו' );
	return $m[ $c ] ?? $c;
}

/** everything the report shows, from the stored rows only; cached five minutes */
function nadlan_dr_data( $proj, $days, $lang = 'he' ) {
	$proj = (int) $proj;
	$days = in_array( (int) $days, array( 7, 30, 90, 365 ), true ) ? (int) $days : 30;
	$lang = 'en' === $lang ? 'en' : 'he';
	$ck   = 'nadlan_dr_' . md5( $proj . '|' . $days . '|' . $lang . '|' . NADLAN_DR_VERSION );
	$hit  = get_transient( $ck );
	if ( is_array( $hit ) ) { return $hit; }
	global $wpdb;
	$out = array( 'proj' => $proj, 'days' => $days, 'lang' => $lang, 'steps' => array(), 'floors' => array(), 'dirs' => array(), 'langs' => array(),
		'devs' => array(), 'countries' => array(), 'daily' => array(), 'journeys' => array(), 'since' => '', 'partial' => 0, 'made' => time() );
	foreach ( nadlan_dr_steps_def() as $k => $v ) { $out['steps'][ $k ] = 0; }
	if ( ! function_exists( 'nadlan_vt_tables_exist' ) || ! nadlan_vt_tables_exist() || ! nadlan_vt_ready() ) { return $out; }
	$t     = nadlan_vt_tables();
	$since = $wpdb->get_var( $wpdb->prepare( "SELECT MIN(at) FROM {$t['e']} WHERE proj = %d", $proj ) ); // phpcs:ignore
	$out['since'] = $since ? (string) $since : '';
	$from  = gmdate( 'Y-m-d H:i:s', time() - $days * DAY_IN_SECONDS );
	$cap   = 250000;
	$rows  = $wpdb->get_results( $wpdb->prepare( "SELECT vid, at, lang, ev, d FROM {$t['e']} WHERE proj = %d AND at >= %s ORDER BY at ASC, id ASC LIMIT %d", $proj, $from, $cap ) ); // phpcs:ignore
	$out['partial'] = count( (array) $rows ) >= $cap ? 1 : 0;
	$V = array(); // per visit: steps, floors, dirs, chain, first lang, first/last
	foreach ( (array) $rows as $r ) {
		$vid = (string) $r->vid;
		if ( ! isset( $V[ $vid ] ) ) {
			$V[ $vid ] = array( 'steps' => array( 'visit' => 1 ), 'floors' => array(), 'dirs' => array(), 'chain' => array(), 'lang' => (string) $r->lang, 'first' => (string) $r->at, 'last' => (string) $r->at, 'days' => array() );
		}
		$v = &$V[ $vid ];
		$v['last'] = (string) $r->at;
		$ts = strtotime( $r->at . ' UTC' );
		$v['days'][ wp_date( 'Y-m-d', $ts ) ] = 1;
		$d  = json_decode( (string) $r->d, true );
		$d  = is_array( $d ) ? $d : array();
		$st = nadlan_dr_steps_of( (string) $r->ev, $d );
		foreach ( $st as $s ) {
			$v['steps'][ $s ] = 1;
			if ( 'floor' === $s && isset( $d['f'] ) && '' !== (string) $d['f'] ) { $v['floors'][ (int) $d['f'] ] = 1; }
			if ( in_array( $s, array( 'floor', 'view' ), true ) ) {
				$dw = nadlan_dr_dir( $d, $lang );
				if ( '' !== $dw && ( 'facing' === $r->ev || 'view' === $s || isset( $d['dir'] ) ) ) { $v['dirs'][ $dw ] = 1; }
			}
			// the journey: each step once, in the order the buyer reached it, with the floor / direction when known
			if ( ! isset( $v['chain'][ $s ] ) ) {
				$det = '';
				if ( 'floor' === $s && isset( $d['f'] ) ) { $det = ( 'en' === $lang ? 'floor ' : 'קומה ' ) . (int) $d['f']; }
				if ( 'view' === $s ) { $det = nadlan_dr_dir( $d, $lang ); }
				$v['chain'][ $s ] = $det;
			} elseif ( 'floor' === $s && '' === $v['chain'][ $s ] && isset( $d['f'] ) ) {
				$v['chain'][ $s ] = ( 'en' === $lang ? 'floor ' : 'קומה ' ) . (int) $d['f'];
			}
		}
		unset( $v );
	}
	if ( ! $V ) { set_transient( $ck, $out, 5 * MINUTE_IN_SECONDS ); return $out; }
	// the visits' own rows: device, country, lead
	$meta = array();
	foreach ( array_chunk( array_keys( $V ), 500 ) as $chunk ) {
		$in = implode( ',', array_fill( 0, count( $chunk ), '%s' ) );
		foreach ( (array) $wpdb->get_results( $wpdb->prepare( "SELECT vid, country, dev, lead_id FROM {$t['v']} WHERE vid IN ($in)", $chunk ) ) as $m ) { // phpcs:ignore
			$meta[ (string) $m->vid ] = $m;
		}
	}
	$devN = array( 'm' => array( 'טלפון', 'phone' ), 't' => array( 'טאבלט', 'tablet' ), 'd' => array( 'מחשב', 'computer' ) );
	$langN = 'en' === $lang ? array( 'he' => 'Hebrew', 'en' => 'English', 'fr' => 'French', 'ru' => 'Russian', 'ar' => 'Arabic' ) : nadlan_vt_langs();
	$li = 'en' === $lang ? 1 : 0;
	foreach ( $V as $vid => $v ) {
		$m = $meta[ $vid ] ?? null;
		if ( $m && (int) $m->lead_id > 0 ) { $V[ $vid ]['steps']['lead'] = 1; $V[ $vid ]['chain']['lead'] = ''; }
		foreach ( $V[ $vid ]['steps'] as $s => $one ) { $out['steps'][ $s ] = ( $out['steps'][ $s ] ?? 0 ) + 1; }
		foreach ( $v['floors'] as $f => $one ) { $out['floors'][ $f ] = ( $out['floors'][ $f ] ?? 0 ) + 1; }
		foreach ( $v['dirs'] as $dw => $one ) { $out['dirs'][ $dw ] = ( $out['dirs'][ $dw ] ?? 0 ) + 1; }
		$ln = $langN[ $v['lang'] ] ?? ( 'en' === $lang ? 'unknown' : 'לא ידוע' );
		$out['langs'][ $ln ] = ( $out['langs'][ $ln ] ?? 0 ) + 1;
		$dv = $m && isset( $devN[ $m->dev ] ) ? $devN[ $m->dev ][ $li ] : ( 'en' === $lang ? 'unknown' : 'לא ידוע' );
		$out['devs'][ $dv ] = ( $out['devs'][ $dv ] ?? 0 ) + 1;
		$cn = nadlan_dr_country( $m ? $m->country : '', $lang );
		$out['countries'][ $cn ] = ( $out['countries'][ $cn ] ?? 0 ) + 1;
		foreach ( $v['days'] as $day => $one ) { $out['daily'][ $day ] = ( $out['daily'][ $day ] ?? 0 ) + 1; }
	}
	arsort( $out['floors'] );
	$out['floors'] = array_slice( $out['floors'], 0, 12, true );
	arsort( $out['dirs'] );
	arsort( $out['langs'] );
	arsort( $out['devs'] );
	arsort( $out['countries'] );
	$out['countries'] = array_slice( $out['countries'], 0, 10, true );
	ksort( $out['daily'] );
	// journeys: the latest visits that went past the page (a choice, a tool, a request), newest first, at most 30
	uasort( $V, function ( $a, $b ) { return strcmp( $b['last'], $a['last'] ); } );
	$def = nadlan_dr_steps_def();
	foreach ( $V as $vid => $v ) {
		if ( count( $v['steps'] ) < 2 ) { continue; }
		$m = $meta[ $vid ] ?? null;
		$parts = array();
		foreach ( $v['chain'] as $s => $det ) {
			$parts[] = array( 'k' => $s, 't' => $def[ $s ][ $li ] ?? $s, 'd' => (string) $det, 'money' => (int) ( $def[ $s ][2] ?? 0 ) );
		}
		$out['journeys'][] = array(
			'at' => wp_date( 'd/m H:i', strtotime( $v['last'] . ' UTC' ) ),
			'who' => trim( ( $m && '' !== (string) $m->country ? nadlan_dr_country( $m->country, $lang ) . ' · ' : '' ) . ( $langN[ $v['lang'] ] ?? '' ) . ' · ' . ( $m && isset( $devN[ $m->dev ] ) ? $devN[ $m->dev ][ $li ] : '' ), ' ·' ),
			'steps' => $parts,
		);
		if ( count( $out['journeys'] ) >= 30 ) { break; }
	}
	set_transient( $ck, $out, 5 * MINUTE_IN_SECONDS );
	return $out;
}

/* ---------------------------------------------------------------- the page */

function nadlan_dr_words( $lang ) {
	$he = array(
		'kicker' => 'נדל״ן · דוח קונים ליזם', 'sub' => 'מה קונים בחרו ועשו בעמוד הפרויקט ובכלים שלו', 'days' => '%d הימים האחרונים',
		'updated' => 'עודכן', 'csv' => 'הורדה לאקסל (CSV)', 'funnel' => 'המשפך: מהכניסה לעמוד ועד הבקשה', 'of' => 'מהביקורים',
		'funnel_note' => 'כל שורה סופרת ביקורים שונים, מספרים אמיתיים בלבד. ביקור שבחר שלוש קומות נספר פעם אחת.',
		'floors' => 'הקומות שנבחרו', 'dirs' => 'לאיזה כיוון הסתכלו', 'who' => 'שפה, מכשיר, ארץ', 'who2' => 'שפה ומכשיר', 'daily' => 'ביקורים לפי יום',
		'journeys' => 'מסלולים של קונים (בלי שמות)', 'none' => 'עוד אין רישומים בתקופה הזו.', 'nodata' => 'אין עדיין נתון',
		'since' => 'המדידה בפרויקט הזה התחילה ב־%s.', 'notyet' => 'המדידה בפרויקט הזה עוד לא רשמה אף ביקור.',
		'excluded' => 'מה לא נספר: דפדפנים שביקשו לא לתעד (Global Privacy Control או Do Not Track), מבקרים שביקשו להפסיק את התיעוד, צוות האתר, רובוטים. בלי כתובות IP, בלי מה שהוקלד, בלי שמות.',
		'expires' => 'הקישור לדוח הזה חתום ופג תוקף ב־%s. אפשר לבטל אותו בכל רגע.', 'partial' => 'יותר מדי רישומים לתקופה: הוצגו הראשונים בלבד.',
		'lang' => 'English', 'langl' => 'en', 'title' => 'דוח קונים ליזם', 'admin' => 'תצוגת מנהל: הקישור החתום נוצר במסך "דוח ליזם".',
		'device' => 'מכשיר', 'language' => 'שפה', 'country' => 'ארץ', 'visits' => 'ביקורים', 'floor' => 'קומה',
	);
	$en = array(
		'kicker' => 'NadLan · buyer report for the developer', 'sub' => 'What buyers chose and did on the project page and its tools', 'days' => 'last %d days',
		'updated' => 'Updated', 'csv' => 'Download for Excel (CSV)', 'funnel' => 'The funnel: from the page to the request', 'of' => 'of visits',
		'funnel_note' => 'Each row counts distinct visits, real numbers only. A visit that chose three floors counts once.',
		'floors' => 'Floors chosen', 'dirs' => 'Directions looked at', 'who' => 'Language, device, country', 'who2' => 'Language and device', 'daily' => 'Visits per day',
		'journeys' => 'Buyer journeys (no names)', 'none' => 'Nothing recorded in this period yet.', 'nodata' => 'No data yet',
		'since' => 'Measuring on this project started on %s.', 'notyet' => 'Measuring on this project has not recorded a visit yet.',
		'excluded' => 'Not counted: browsers that ask not to be tracked (Global Privacy Control or Do Not Track), visitors who stopped the recording, the site team, robots. No IP addresses, nothing typed, no names.',
		'expires' => 'This report link is signed and expires on %s. It can be revoked at any time.', 'partial' => 'Too many records for this period: the first ones are shown.',
		'lang' => 'עברית', 'langl' => 'he', 'title' => 'Buyer report for the developer', 'admin' => 'Admin preview: the signed link is made in the "דוח ליזם" screen.',
		'device' => 'Device', 'language' => 'Language', 'country' => 'Country', 'visits' => 'Visits', 'floor' => 'Floor',
	);
	return 'en' === $lang ? $en : $he;
}

/** the report page; $link: function( $args ) returning the url of this report with other args (period, language, csv) */
function nadlan_dr_html( $proj, $days, $lang, $link, $expires = 0, $admin = false, $journeys = true ) {
	$D   = nadlan_dr_data( $proj, $days, $lang );
	$W   = nadlan_dr_words( $lang );
	$en  = 'en' === $lang;
	$li  = $en ? 1 : 0;
	$def = nadlan_dr_steps_def();
	$e   = function ( $s ) { return esc_html( (string) $s ); };
	$num = function ( $n ) { return esc_html( number_format( (int) $n ) ); };
	$title = (string) get_the_title( $proj );
	$base  = (int) ( $D['steps']['visit'] ?? 0 );
	$pct   = function ( $n ) use ( $base ) { return $base > 0 ? (int) round( 100 * $n / $base ) : 0; };
	$h  = '<!doctype html><html lang="' . ( $en ? 'en' : 'he' ) . '" dir="' . ( $en ? 'ltr' : 'rtl' ) . '"><head><meta charset="utf-8">';
	$h .= '<meta name="viewport" content="width=device-width,initial-scale=1"><title>' . $e( $W['title'] . ': ' . $title ) . '</title>';
	$h .= '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>';
	$h .= '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&amp;family=IBM+Plex+Sans+Hebrew:wght@400;600;700&amp;display=swap" rel="stylesheet">';
	$h .= '<style>
:root{--paper:#EEF2F5;--ink:#0D1B2A;--ink2:#3B4A58;--cob:#1E4FD6;--track:#CFDBF3;--teal:#0B7A6F;--track2:#CDE7E3;--rule:#B8C4CF}
*{box-sizing:border-box}html,body{margin:0;background:var(--paper);color:var(--ink)}
body{font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif;font-size:16px;line-height:1.5}
.m{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}
.wrap{max-width:1180px;margin:0 auto;padding:32px 24px 56px;display:flex;flex-direction:column;gap:28px}
.top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px;border-bottom:2px solid var(--ink);padding-bottom:16px}
.kick{font-size:13px;letter-spacing:.06em;color:var(--cob);font-weight:600}
h1{margin:4px 0;font-size:clamp(28px,4vw,40px);font-weight:700}
h2{margin:0 0 12px;font-size:22px}h3{margin:0 0 8px;font-size:17px}
.sub{color:var(--ink2);font-size:15px}
.ctl{display:flex;flex-wrap:wrap;gap:8px}
.ctl a{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border:2px solid var(--ink);color:var(--ink);text-decoration:none;font-weight:600}
.ctl a.on{background:var(--ink);color:var(--paper)}.ctl a.csv{border-color:var(--cob);color:var(--cob)}
.ctl a:focus-visible{outline:3px solid var(--cob);outline-offset:2px}
.fun{display:flex;flex-direction:column;gap:10px}
.fun .row{display:grid;grid-template-columns:minmax(150px,260px) minmax(0,1fr) 72px 64px;gap:16px;align-items:center}
.fun .l{font-weight:600}.fun .bar{height:26px;background:var(--track)}.fun .bar i{display:block;height:26px;background:var(--cob)}
.fun .n{font-weight:600}.fun .p{color:var(--ink2)}
.fun .money .l{color:var(--teal);font-weight:700}.fun .money .bar{background:var(--track2)}.fun .money .bar i{background:var(--teal)}
.note{font-size:13px;color:var(--ink2)}
.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.box{border-top:2px solid var(--ink);padding-top:12px}
.hist{display:grid;grid-template-columns:auto minmax(0,1fr) 44px;gap:6px 10px;align-items:center;font-size:14px}
.hist i{display:block;height:14px;background:var(--cob)}
.kv{font-size:14px;line-height:1.9}.kv b{font-family:"IBM Plex Mono",monospace}
.days{display:flex;align-items:flex-end;gap:2px;height:96px;border-bottom:2px solid var(--ink)}
.days i{flex:1 1 0;background:var(--cob);min-height:2px}
.jr{display:grid;grid-template-columns:96px 190px minmax(0,1fr);border-top:2px solid var(--ink);font-size:14px}
.jr>div{padding:10px 8px 10px 0;border-bottom:1px solid var(--rule)}
.jr .money{color:var(--teal);font-weight:700}
.foot{border-top:2px solid var(--ink);padding-top:12px;display:flex;flex-direction:column;gap:6px;font-size:13px;color:var(--ink2)}
.tag{align-self:flex-start;background:var(--ink);color:var(--paper);padding:6px 12px;font-size:13px}
@media (max-width:760px){.wrap{padding:20px 16px 40px}.fun .row{grid-template-columns:minmax(0,1fr) 56px 48px;gap:4px 10px}.fun .bar{grid-column:1/-1;grid-row:2;height:12px}.fun .bar i{height:12px}
.three{grid-template-columns:minmax(0,1fr)}.jr{grid-template-columns:minmax(0,1fr)}.jr>div{border-bottom:0;padding:4px 0}.jr>div:nth-child(3n){border-bottom:1px solid var(--rule);padding-bottom:10px}}
@media print{.ctl{display:none}body{background:#fff}}
</style></head><body><main class="wrap">';
	$h .= '<div class="top"><div><div class="kick">' . $e( $W['kicker'] ) . '</div><h1>' . $e( $title ) . '</h1><div class="sub">' . $e( $W['sub'] ) . ' · '
		. $e( sprintf( $W['days'], $days ) ) . ' · ' . $e( $W['updated'] ) . ' <span class="m">' . $e( wp_date( 'd/m/Y H:i', (int) $D['made'] ) ) . '</span></div></div>';
	$h .= '<nav class="ctl" aria-label="' . esc_attr( $en ? 'Period and export' : 'תקופה והורדה' ) . '">';
	foreach ( array( 7, 30, 90, 365 ) as $dd ) {
		$h .= '<a class="' . ( $dd === (int) $days ? 'on' : '' ) . '" href="' . esc_url( $link( array( 'd' => $dd, 'l' => $lang ) ) ) . '">' . $e( $en ? $dd . ' days' : $dd . ' ימים' ) . '</a>';
	}
	$h .= '<a href="' . esc_url( $link( array( 'd' => $days, 'l' => $W['langl'] ) ) ) . '" lang="' . esc_attr( $W['langl'] ) . '">' . $e( $W['lang'] ) . '</a>';
	$h .= '<a class="csv" href="' . esc_url( $link( array( 'd' => $days, 'l' => $lang, 'fmt' => 'csv' ) ) ) . '">' . $e( $W['csv'] ) . '</a></nav></div>';
	if ( $admin ) { $h .= '<div class="tag">' . $e( $W['admin'] ) . '</div>'; }
	if ( ! empty( $D['partial'] ) ) { $h .= '<div class="tag">' . $e( $W['partial'] ) . '</div>'; }

	// the funnel
	$h .= '<section aria-labelledby="dr-f"><h2 id="dr-f">' . $e( $W['funnel'] ) . '</h2>';
	if ( $base <= 0 ) {
		$h .= '<p>' . $e( $W['none'] ) . '</p>';
	}
	$h .= '<div class="fun" role="table">';
	foreach ( $def as $k => $row ) {
		$n = (int) ( $D['steps'][ $k ] ?? 0 );
		$p = $pct( $n );
		$h .= '<div class="row' . ( $row[2] ? ' money' : '' ) . '" role="row"><div class="l" role="rowheader">' . $e( $row[ $li ] ) . '</div>'
			. '<div class="bar" aria-hidden="true"><i style="width:' . ( $n > 0 ? max( 1, $p ) : 0 ) . '%"></i></div>'
			. '<div class="n m" role="cell">' . $num( $n ) . '</div><div class="p m" role="cell">' . ( 'visit' === $k ? '100%' : $p . '%' ) . '</div></div>';
	}
	$h .= '</div><p class="note">' . $e( $W['funnel_note'] ) . '</p></section>';

	// three boxes
	$hist = function ( $arr, $label ) use ( $e, $num ) {
		if ( ! $arr ) { return '<p class="note">' . $e( $label ) . '</p>'; }
		$max = max( $arr );
		$o = '<div class="hist">';
		foreach ( $arr as $k => $n ) {
			$o .= '<div>' . $e( $k ) . '</div><div aria-hidden="true"><i style="width:' . (int) round( 100 * $n / max( 1, $max ) ) . '%"></i></div><div class="m">' . $num( $n ) . '</div>';
		}
		return $o . '</div>';
	};
	$floors = array();
	foreach ( $D['floors'] as $f => $n ) { $floors[ ( $en ? 'Floor ' : 'קומה ' ) . $f ] = $n; }
	$kv = function ( $arr ) use ( $e, $pct, $base ) {
		$o = array();
		foreach ( $arr as $k => $n ) { $o[] = $e( $k ) . ' <b>' . (int) $pct( $n ) . '%</b>'; }
		return implode( ' · ', $o );
	};
	$h .= '<div class="three">';
	$h .= '<section class="box"><h3>' . $e( $W['floors'] ) . '</h3>' . $hist( $floors, $W['nodata'] ) . '</section>';
	$h .= '<section class="box"><h3>' . $e( $W['dirs'] ) . '</h3>' . $hist( $D['dirs'], $W['nodata'] ) . '</section>';
	$unk = $en ? 'unknown' : 'לא ידוע';
	$hasC = (bool) array_diff( array_keys( $D['countries'] ), array( $unk ) );
	$h .= '<section class="box"><h3>' . $e( $hasC ? $W['who'] : $W['who2'] ) . '</h3>' . ( $base > 0 ? '<div class="kv">' . $kv( $D['langs'] ) . '<br>' . $kv( $D['devs'] ) . ( $hasC ? '<br>' . $kv( $D['countries'] ) : '' ) . '</div>' : '<p class="note">' . $e( $W['nodata'] ) . '</p>' ) . '</section>';
	$h .= '</div>';

	// visits per day
	if ( $D['daily'] ) {
		$max = max( $D['daily'] );
		$h .= '<section class="box"><h3>' . $e( $W['daily'] ) . '</h3><div class="days" role="img" aria-label="' . esc_attr( $W['daily'] ) . '">';
		$start = strtotime( '-' . ( $days - 1 ) . ' days', current_time( 'timestamp' ) );
		for ( $i = 0; $i < $days; $i++ ) {
			$day = gmdate( 'Y-m-d', $start + $i * DAY_IN_SECONDS );
			$n   = (int) ( $D['daily'][ $day ] ?? 0 );
			$h  .= '<i title="' . esc_attr( gmdate( 'd/m', $start + $i * DAY_IN_SECONDS ) . ': ' . $n ) . '" style="height:' . ( $n > 0 ? max( 3, (int) round( 100 * $n / max( 1, $max ) ) ) : 0 ) . '%"></i>';
		}
		$h .= '</div></section>';
	}

	// journeys
	if ( $journeys ) {
	$h .= '<section aria-labelledby="dr-j"><h2 id="dr-j">' . $e( $W['journeys'] ) . '</h2>';
	if ( ! $D['journeys'] ) {
		$h .= '<p class="note">' . $e( $W['none'] ) . '</p>';
	} else {
		$h .= '<div class="jr">';
		foreach ( $D['journeys'] as $j ) {
			$chain = array();
			foreach ( $j['steps'] as $s ) {
				if ( 'visit' === $s['k'] ) { continue; }
				$txt = $s['t'] . ( '' !== $s['d'] ? ' (' . $s['d'] . ')' : '' );
				$chain[] = $s['money'] ? '<b class="money">' . $e( $txt ) . '</b>' : $e( $txt );
			}
			$h .= '<div class="m">' . $e( $j['at'] ) . '</div><div>' . $e( $j['who'] ) . '</div><div>' . implode( $en ? ' → ' : ' ← ', $chain ) . '</div>';
		}
		$h .= '</div>';
	}
	$h .= '</section>';
	}

	// the honest footer
	$h .= '<footer class="foot">';
	$h .= '<div>' . ( $D['since'] ? $e( sprintf( $W['since'], wp_date( 'd/m/Y', strtotime( $D['since'] . ' UTC' ) ) ) ) : $e( $W['notyet'] ) ) . '</div>';
	$h .= '<div>' . $e( $W['excluded'] ) . '</div>';
	if ( $expires > 0 ) { $h .= '<div>' . $e( sprintf( $W['expires'], wp_date( 'd/m/Y', (int) $expires ) ) ) . '</div>'; }
	$h .= '</footer></main></body></html>';
	return $h;
}

/** the same numbers as CSV (UTF-8 with BOM so Excel reads Hebrew) */
function nadlan_dr_csv( $proj, $days, $lang, $journeys = true ) {
	$D   = nadlan_dr_data( $proj, $days, $lang );
	$en  = 'en' === $lang;
	$li  = $en ? 1 : 0;
	$f   = fopen( 'php://temp', 'w+' );
	fwrite( $f, "\xEF\xBB\xBF" );
	$put = function ( $row ) use ( $f ) {
		// a cell that starts like a formula is written as text (CSV injection)
		$row = array_map( function ( $c ) { $c = (string) $c; return preg_match( '/^[=+\-@\t\r]/', $c ) ? "'" . $c : $c; }, $row );
		fputcsv( $f, $row );
	};
	$put( array( $en ? 'Project' : 'פרויקט', get_the_title( $proj ), $en ? 'Days' : 'ימים', $days, $en ? 'Made' : 'הופק', wp_date( 'Y-m-d H:i', (int) $D['made'] ) ) );
	$put( array() );
	$put( array( $en ? 'Step' : 'שלב', $en ? 'Visits' : 'ביקורים', '%' ) );
	$base = max( 1, (int) ( $D['steps']['visit'] ?? 0 ) );
	foreach ( nadlan_dr_steps_def() as $k => $row ) {
		$n = (int) ( $D['steps'][ $k ] ?? 0 );
		$put( array( $row[ $li ], $n, (int) round( 100 * $n / $base ) ) );
	}
	$put( array() );
	$put( array( $en ? 'Floor' : 'קומה', $en ? 'Visits' : 'ביקורים' ) );
	foreach ( $D['floors'] as $fl => $n ) { $put( array( $fl, $n ) ); }
	$put( array() );
	$put( array( $en ? 'Direction' : 'כיוון', $en ? 'Visits' : 'ביקורים' ) );
	foreach ( $D['dirs'] as $k => $n ) { $put( array( $k, $n ) ); }
	$put( array() );
	foreach ( array( 'langs' => $en ? 'Language' : 'שפה', 'devs' => $en ? 'Device' : 'מכשיר', 'countries' => $en ? 'Country' : 'ארץ' ) as $key => $lbl ) {
		$put( array( $lbl, $en ? 'Visits' : 'ביקורים' ) );
		foreach ( $D[ $key ] as $k => $n ) { $put( array( $k, $n ) ); }
		$put( array() );
	}
	$put( array( $en ? 'Day' : 'יום', $en ? 'Visits' : 'ביקורים' ) );
	foreach ( $D['daily'] as $k => $n ) { $put( array( $k, $n ) ); }
	$put( array() );
	if ( $journeys ) { $put( array( $en ? 'When' : 'מתי', $en ? 'Visitor' : 'מבקר', $en ? 'Steps' : 'שלבים' ) ); }
	foreach ( ( $journeys ? $D['journeys'] : array() ) as $j ) {
		$put( array( $j['at'], $j['who'], implode( ' > ', array_map( function ( $s ) { return $s['t'] . ( '' !== $s['d'] ? ' (' . $s['d'] . ')' : '' ); }, array_filter( $j['steps'], function ( $s ) { return 'visit' !== $s['k']; } ) ) ) ) );
	}
	rewind( $f );
	$csv = stream_get_contents( $f );
	fclose( $f );
	return $csv;
}

function nadlan_dr_send( $body, $type, $status = 200, $filename = '' ) {
	status_header( $status );
	nocache_headers();
	header( 'Content-Type: ' . $type . '; charset=UTF-8' );
	header( 'Referrer-Policy: no-referrer' );
	header( 'X-Content-Type-Options: nosniff' );
	header( 'X-Frame-Options: SAMEORIGIN' );
	if ( '' !== $filename ) { header( 'Content-Disposition: attachment; filename="' . $filename . '"' ); }
	echo $body; // phpcs:ignore -- escaped while built
	exit;
}

function nadlan_dr_refused() {
	$h = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>הקישור אינו בתוקף</title>'
		. '<style>body{margin:0;background:#EEF2F5;color:#0D1B2A;font:17px/1.6 system-ui,sans-serif}main{max-width:640px;margin:15vh auto;padding:0 20px}h1{font-size:26px}</style></head>'
		. '<body><main><h1>הקישור לדוח אינו בתוקף</h1><p>פג תוקפו או שבוטל. אפשר לבקש קישור חדש מצוות נדל״ן.</p><p lang="en" dir="ltr">This report link has expired or was revoked. Ask the NadLan team for a new one.</p></main></body></html>';
	nadlan_dr_send( $h, 'text/html', 403 );
}

/** GET /wp-json/nadlan/v1/dev-report */
function nadlan_dr_rest( $req ) {
	$p = (int) $req->get_param( 'p' );
	$x = (int) $req->get_param( 'x' );
	$s = (string) $req->get_param( 's' );
	if ( function_exists( 'nadlan_vt_limit' ) && ! nadlan_vt_limit( 'dr|' . nadlan_vt_client() . '|' . gmdate( 'YmdHi' ), 60, 2 * MINUTE_IN_SECONDS ) ) {
		nadlan_dr_send( 'Too many requests.', 'text/plain', 429 );
	}
	if ( ! nadlan_dr_valid( $p, $x, $s ) ) { nadlan_dr_refused(); }
	$d    = (int) $req->get_param( 'd' );
	$d    = in_array( $d, array( 7, 30, 90, 365 ), true ) ? $d : 30;
	$lang = 'en' === $req->get_param( 'l' ) ? 'en' : 'he';
	if ( 'csv' === $req->get_param( 'fmt' ) ) {
		nadlan_dr_send( nadlan_dr_csv( $p, $d, $lang, nadlan_dr_journeys_public() ), 'text/csv', 200, 'nadlan-report-' . $p . '-' . $d . 'd.csv' );
	}
	$link = function ( $args ) use ( $p, $x ) { return nadlan_dr_url( $p, $x, $args ); };
	nadlan_dr_send( nadlan_dr_html( $p, $d, $lang, $link, $x, false, nadlan_dr_journeys_public() ), 'text/html' );
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/dev-report', array( 'methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => 'nadlan_dr_rest' ) );
} );

/* ---------------------------------------------------------------- the admin screen: "דוח ליזם" */

function nadlan_dr_admin_url( $args = array() ) { return add_query_arg( $args, admin_url( 'admin.php?page=nadlan-dev-report' ) ); }

/** the projects with any recorded event in the last year, with their visits in 30 days */
function nadlan_dr_projects() {
	global $wpdb;
	if ( ! function_exists( 'nadlan_vt_tables_exist' ) || ! nadlan_vt_tables_exist() || NADLAN_VT_DB !== (string) get_option( 'nadlan_vt_db', '' ) ) { return array(); }
	$t = nadlan_vt_tables();
	$rows = $wpdb->get_results( $wpdb->prepare( "SELECT proj, COUNT(DISTINCT CASE WHEN at >= %s THEN vid END) AS v30, MAX(at) AS last FROM {$t['e']} WHERE proj > 0 AND at >= %s GROUP BY proj ORDER BY v30 DESC LIMIT 200",
		gmdate( 'Y-m-d H:i:s', time() - 30 * DAY_IN_SECONDS ), gmdate( 'Y-m-d H:i:s', time() - 365 * DAY_IN_SECONDS ) ) ); // phpcs:ignore
	return (array) $rows;
}

function nadlan_dr_admin_html() {
	$h  = '<div class="wrap" dir="rtl"><h1>דוח ליזם</h1>';
	if ( ! nadlan_dr_journeys_public() ) {
		$h .= '<div class="notice notice-info"><p>המסלולים האנונימיים מוצגים כאן בתצוגת המנהל בלבד. בקישור ליזם יופיעו רק המספרים, עד שעורך הדין יאשר את נוסח מדיניות הפרטיות (Linear HAD-797). עד אז לא שולחים ליזם קישור.</p></div>';
	}
	$h .= '<p class="description">לכל פרויקט: מה קונים בחרו ועשו (קומה, נוף, מעצב, החזר חודשי, סל, שיחה, בקשה להצעה, פנייה), מספרים אמיתיים בלבד, בלי שמות. יוצרים קישור חתום עם תאריך תפוגה ושולחים ליזם. "ביטול הקישורים" מבטל מיד את כל הקישורים של אותו פרויקט.</p>';
	$links = get_option( 'nadlan_dr_links', array() );
	$links = is_array( $links ) ? $links : array();
	if ( isset( $_GET['made'] ) ) { // phpcs:ignore
		$pm = absint( $_GET['made'] ); // phpcs:ignore
		if ( isset( $links[ $pm ]['url'] ) ) {
			$h .= '<div class="notice notice-success"><p>הקישור ל<b>' . esc_html( get_the_title( $pm ) ) . '</b> נוצר. העתיקו ושלחו ליזם:</p><p><input type="text" readonly style="width:100%;direction:ltr" onclick="this.select()" value="' . esc_attr( $links[ $pm ]['url'] ) . '"></p></div>';
		}
	}
	if ( isset( $_GET['revoked'] ) ) { $h .= '<div class="notice notice-warning"><p>כל הקישורים הקודמים של הפרויקט בוטלו.</p></div>'; } // phpcs:ignore
	$rows = nadlan_dr_projects();
	$form = function ( $pid ) {
		return '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '" style="display:inline-flex;gap:6px;align-items:center">'
			. '<input type="hidden" name="action" value="nadlan_dr_link"><input type="hidden" name="p" value="' . (int) $pid . '">'
			. wp_nonce_field( 'nadlan_dr_link', '_wpnonce', true, false )
			. '<select name="days"><option value="30">30 יום</option><option value="90" selected>90 יום</option><option value="365">שנה</option></select>'
			. '<button class="button button-primary">יצירת קישור ליזם</button></form>';
	};
	$h .= '<table class="widefat striped" style="max-width:1100px"><thead><tr><th>פרויקט</th><th>ביקורים ב־30 ימים</th><th>רישום אחרון</th><th>קישור ליזם</th><th></th></tr></thead><tbody>';
	if ( ! $rows ) { $h .= '<tr><td colspan="5">עוד לא נרשם אף אירוע עם פרויקט. אפשר ליצור קישור לפי מספר פרויקט למטה.</td></tr>'; }
	foreach ( $rows as $r ) {
		$pid = (int) $r->proj;
		$lk  = $links[ $pid ] ?? null;
		$h  .= '<tr><td><b>' . esc_html( get_the_title( $pid ) ?: '#' . $pid ) . '</b> <small>#' . $pid . '</small><br><a href="' . esc_url( add_query_arg( array( 'action' => 'nadlan_dr_preview', 'p' => $pid, '_wpnonce' => wp_create_nonce( 'nadlan_dr_preview' ) ), admin_url( 'admin-post.php' ) ) ) . '" target="_blank" rel="noopener">תצוגה כמנהל</a></td>';
		$h  .= '<td>' . esc_html( number_format_i18n( (int) $r->v30 ) ) . '</td><td>' . esc_html( wp_date( 'd/m/Y H:i', strtotime( $r->last . ' UTC' ) ) ) . '</td>';
		$h  .= '<td>' . $form( $pid ) . ( $lk && (int) ( $lk['x'] ?? 0 ) > time() ? '<br><small>קישור אחרון: פג ב־' . esc_html( wp_date( 'd/m/Y', (int) $lk['x'] ) ) . ' · <a href="' . esc_url( $lk['url'] ) . '" target="_blank" rel="noopener noreferrer">פתיחה</a></small>' : '' ) . '</td>';
		$h  .= '<td><form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '" onsubmit="return confirm(\'לבטל את כל הקישורים של הפרויקט הזה?\')"><input type="hidden" name="action" value="nadlan_dr_revoke"><input type="hidden" name="p" value="' . $pid . '">'
			. wp_nonce_field( 'nadlan_dr_revoke', '_wpnonce', true, false ) . '<button class="button-link" style="color:#b32d2e">ביטול הקישורים</button></form></td></tr>';
	}
	$h .= '</tbody></table>';
	$h .= '<h2>פרויקט אחר</h2><form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '"><input type="hidden" name="action" value="nadlan_dr_link">' . wp_nonce_field( 'nadlan_dr_link', '_wpnonce', true, false )
		. '<label>מספר הפרויקט (post ID) <input type="number" name="p" min="1" required></label> <select name="days"><option value="30">30 יום</option><option value="90" selected>90 יום</option><option value="365">שנה</option></select> <button class="button">יצירת קישור</button></form>';
	return $h . '</div>';
}

add_action( 'admin_menu', function () {
	add_submenu_page( 'nadlan-inbox', 'דוח ליזם', 'דוח ליזם', 'manage_options', 'nadlan-dev-report', function () {
		if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'אין הרשאה.' ); }
		echo nadlan_dr_admin_html(); // phpcs:ignore -- escaped inside
	} );
}, 31 );

add_action( 'admin_post_nadlan_dr_link', function () {
	if ( ! current_user_can( 'manage_options' ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['_wpnonce'] ?? '' ) ), 'nadlan_dr_link' ) ) { wp_die( 'אין הרשאה.' ); }
	$p    = nadlan_vt_canon_project( absint( $_POST['p'] ?? 0 ) );
	$days = in_array( (int) ( $_POST['days'] ?? 90 ), array( 30, 90, 365 ), true ) ? (int) $_POST['days'] : 90;
	if ( $p <= 0 ) { wp_die( 'זה לא מספר של פרויקט מפורסם.' ); }
	$x     = time() + $days * DAY_IN_SECONDS;
	$links = get_option( 'nadlan_dr_links', array() );
	$links = is_array( $links ) ? $links : array();
	$links[ $p ] = array( 'url' => nadlan_dr_url( $p, $x ), 'x' => $x, 'made' => time(), 'by' => get_current_user_id() );
	update_option( 'nadlan_dr_links', $links, false );
	wp_safe_redirect( nadlan_dr_admin_url( array( 'made' => $p ) ) );
	exit;
} );

add_action( 'admin_post_nadlan_dr_revoke', function () {
	if ( ! current_user_can( 'manage_options' ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['_wpnonce'] ?? '' ) ), 'nadlan_dr_revoke' ) ) { wp_die( 'אין הרשאה.' ); }
	$p   = absint( $_POST['p'] ?? 0 );
	$rev = get_option( 'nadlan_dr_rev', array() );
	$rev = is_array( $rev ) ? $rev : array();
	$rev[ $p ] = (int) ( $rev[ $p ] ?? 0 ) + 1;
	update_option( 'nadlan_dr_rev', $rev, false );
	$links = get_option( 'nadlan_dr_links', array() );
	if ( is_array( $links ) && isset( $links[ $p ] ) ) { unset( $links[ $p ] ); update_option( 'nadlan_dr_links', $links, false ); }
	wp_safe_redirect( nadlan_dr_admin_url( array( 'revoked' => 1 ) ) );
	exit;
} );

add_action( 'admin_post_nadlan_dr_preview', function () {
	if ( ! current_user_can( 'manage_options' ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_GET['_wpnonce'] ?? '' ) ), 'nadlan_dr_preview' ) ) { wp_die( 'אין הרשאה.' ); }
	$p    = nadlan_vt_canon_project( absint( $_GET['p'] ?? 0 ) );
	if ( $p <= 0 ) { wp_die( 'זה לא מספר של פרויקט מפורסם.' ); }
	$d    = in_array( (int) ( $_GET['d'] ?? 30 ), array( 7, 30, 90, 365 ), true ) ? (int) $_GET['d'] : 30;
	$lang = 'en' === ( $_GET['l'] ?? '' ) ? 'en' : 'he';
	$link = function ( $args ) use ( $p ) {
		return add_query_arg( array_merge( array( 'action' => 'nadlan_dr_preview', 'p' => $p, '_wpnonce' => wp_create_nonce( 'nadlan_dr_preview' ) ), $args ), admin_url( 'admin-post.php' ) );
	};
	if ( 'csv' === ( $_GET['fmt'] ?? '' ) ) { nadlan_dr_send( nadlan_dr_csv( $p, $d, $lang ), 'text/csv', 200, 'nadlan-report-' . $p . '-' . $d . 'd.csv' ); }
	nadlan_dr_send( nadlan_dr_html( $p, $d, $lang, $link, 0, true ), 'text/html' );
} );

/* ---------------------------------------------------------------- proof for the release bridge (read only) */

function nadlan_dr_selftest( $proj = 0 ) {
	$proj = (int) $proj;
	$x    = time() + 3600;
	$okSig = $proj > 0 ? nadlan_dr_valid( $proj, $x, nadlan_dr_sig( $proj, $x ) ) : null;
	$bad   = $proj > 0 ? nadlan_dr_valid( $proj, $x, str_repeat( 'a', 32 ) ) : null;
	$old   = $proj > 0 ? nadlan_dr_valid( $proj, time() - 10, nadlan_dr_sig( $proj, time() - 10 ) ) : null;
	$html  = $proj > 0 ? nadlan_dr_html( $proj, 30, 'he', function () { return '#'; }, $x ) : '';
	$csv   = $proj > 0 ? nadlan_dr_csv( $proj, 30, 'en' ) : '';
	$steps = array(
		nadlan_dr_steps_of( 'floor', array( 'f' => 23, 'src' => 'auto' ) ), nadlan_dr_steps_of( 'facing', array( 'f' => 23, 'b' => 268 ) ),
		nadlan_dr_steps_of( 'act', array( 'n' => 'design_order' ) ), nadlan_dr_steps_of( 'act', array( 'n' => 'mortgage_check' ) ),
		nadlan_dr_steps_of( 'click', array( 'k' => 'wa' ) ), nadlan_dr_steps_of( 'act', array( 'n' => 'offer_sent' ) ),
	);
	return array(
		'version' => NADLAN_DR_VERSION, 'sig_ok' => $okSig, 'sig_bad' => $bad, 'sig_old' => $old,
		'route' => (bool) ( function_exists( 'rest_get_server' ) && isset( rest_get_server()->get_routes()['/nadlan/v1/dev-report'] ) ),
		'html_bytes' => strlen( $html ), 'html_funnel_rows' => substr_count( $html, 'role="rowheader"' ), 'csv_bom' => 0 === strpos( $csv, "\xEF\xBB\xBF" ) ? 1 : 0,
		'steps' => $steps, 'data' => $proj > 0 ? array_intersect_key( nadlan_dr_data( $proj, 30 ), array( 'steps' => 1, 'since' => 1 ) ) : null,
	);
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['dev_report'] = array( 'version' => NADLAN_DR_VERSION );
	return $out;
} );
