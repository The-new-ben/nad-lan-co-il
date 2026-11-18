<?php
/**
 * nad-lan professionals' forum: "הדירה שמדברים עליה" (18.11.2026, Claude Design board 23, forum-design/project/HomeTalk.dc.html).
 * A member presents an apartment (no house number, no phone), everyone votes on the asking price in one tap (guests too, no
 * entry), members give a price estimate in their answers, and the public average of closed deals sits beside it.
 *
 * Loaded by ONE line at the end of inc/pro-forum.php, after the media module:
 *   if ( file_exists( __DIR__ . '/pro-forum-home.php' ) ) { require_once __DIR__ . '/pro-forum-home.php'; }
 * Tables (own version option nadlan_forum_home_db, the house names of nlf_t()): {prefix}nadlan_forum_homes (one row per
 *   discussion of kind 'home'), {prefix}nadlan_forum_votes (one row per voter per discussion), {prefix}nadlan_forum_estimates
 *   (one row per member per discussion, the latest wins).
 * Hooks this module fills (added to the forum's own files as one-line hooks marked "HOOK (home module ...)"):
 *   nlf_kinds (filter, inc/pro-forum.php)  'home' => 'דירה לדיון'
 *   nlf_reply_before_body (filter, inc/pro-forum-render.php)  the chip "ההערכה שלי: ₪3,250,000" of an answer
 * Existing hooks it uses: nlf_post_check / nlf_post_created (the estimate of an answer; the generic route refuses kind 'home'),
 *   nlf_home_after_start (5, the card of part א or the invitation of part ד), nlf_topic_after_body (12, parts ב and ג).
 * The board's "נמכרו ברחוב" (part ב) is NOT built: street-level deals are not public to us (the /street/ files answer 403 and are
 *   never called). In its place: the city's and the chosen neighbourhood's average closed-deal price for the same number of rooms,
 *   from the public files data.nadlan.gov.il/api/pages/settlement|neighborhood/buy/<id>.json (server side, cached 7 days, a
 *   failed fetch hides the box and is retried after an hour).
 * REST (nadlan/v1/forum/..., hidden from the index, errors are HTTP 400): POST home (a member presents an apartment),
 *   GET home/nbhd?code= (the city's neighbourhoods), POST home/vote (one tap, a member or a guest browser).
 * The site is not a broker: no lead form, no "contact the seller"; the author's phone and email are never shown. Nothing here
 * claims a valuation: estimates are members' opinions and say so. No redirects, no robots changes, no long dashes in this file.
 */

if ( ! defined( 'ABSPATH' ) && ! defined( 'NLFH_PURE_ONLY' ) ) { exit; }
if ( defined( 'NLFH_LOADED' ) ) { return; }
define( 'NLFH_LOADED', true );
define( 'NLFH_DB', '1' );

/* =========================================================================================================
 * 1. Pure functions (no WordPress). tests-local/pro-forum-home-test.php loads only this part (NLFH_PURE_ONLY), after the
 *    forum's own pure part.
 * ======================================================================================================= */

/** city => settlement code of data.nadlan.gov.il (the 24 cities of assets/instruments/data/prices-hub.json, HAD-681) */
function nlfh_cities() {
	return array(
		'תל אביב יפו' => 5000, 'ירושלים' => 3000, 'חיפה' => 4000, 'ראשון לציון' => 8300, 'פתח תקווה' => 7900, 'אשדוד' => 70,
		'נתניה' => 7400, 'באר שבע' => 9000, 'בני ברק' => 6100, 'חולון' => 6600, 'רמת גן' => 8600, 'אשקלון' => 7100,
		'רחובות' => 8400, 'בת ים' => 6200, 'הרצליה' => 6400, 'כפר סבא' => 6900, 'מודיעין מכבים רעות' => 1200, 'רעננה' => 8700,
		'גבעתיים' => 6300, 'הוד השרון' => 9700, 'רמת השרון' => 2650, 'קריית אונו' => 2620, 'יבנה' => 2660, 'אילת' => 2600,
	);
}

/** the settlement code of a city name, 0 when it is not one of the 24 */
function nlfh_city_code( $name ) {
	$c = nlfh_cities();
	return isset( $c[ (string) $name ] ) ? (int) $c[ (string) $name ] : 0;
}

/** a code is one of the 24 */
function nlfh_code_ok( $code ) { return (int) $code > 0 && in_array( (int) $code, array_map( 'intval', nlfh_cities() ), true ); }

/** state chips of board 23 part ד: key => (chip, the line on the discussion) */
function nlfh_states() {
	return array( 'second' => array( 'יד שנייה', 'יד שנייה' ), 'new' => array( 'דירה מקבלן', 'דירה מקבלן' ), 'reno' => array( 'צריכה שיפוץ', 'צריכה שיפוץ' ) );
}

/** intent chips: key => (chip, the neutral line on the discussion) */
function nlfh_intents() {
	return array( 'seller' => array( 'אני מוכר', 'מוכרים את הדירה' ), 'buyer' => array( 'שוקל לקנות אותה', 'שוקלים לקנות אותה' ), 'curious' => array( 'סתם סקרן', 'שואלים מסקרנות' ) );
}

/** '' when the street is fine; the Hebrew message otherwise. No house number at the end, no phone, no link. Empty is fine. */
function nlfh_street_error( $s ) {
	$s = trim( (string) $s );
	if ( '' === $s ) { return ''; }
	if ( nlf_has_phone( $s ) ) { return 'בשם הרחוב אי אפשר לכתוב מספר טלפון.'; }
	if ( nlf_has_link( $s ) ) { return 'בשם הרחוב אי אפשר לכתוב קישור.'; }
	// a house number at the end: "הרצל 12", "הרצל 12א", "הרצל12", "הרצל 12/3", "הרצל מס' 5", "הרצל 12 דירה 4", or digits alone
	if ( preg_match( '~\d{1,5}\s*[א-ת]?[\'׳"]?\s*$~u', $s ) ) {
		return 'בלי מספר בית, רק שם הרחוב.';
	}
	if ( nlf_len( $s ) < 2 ) { return 'שם הרחוב קצר מדי.'; }
	if ( nlf_len( $s ) > 40 ) { return 'שם הרחוב ארוך מדי. עד 40 תווים.'; }
	return '';
}

/** rooms 1 to 12, halves allowed; 0 when not valid */
function nlfh_rooms_norm( $v ) {
	$v = str_replace( ',', '.', trim( (string) $v ) );
	if ( ! preg_match( '/^\d{1,2}(?:\.[05])?$/', $v ) ) { return 0.0; }
	$r = (float) $v;
	return ( $r >= 1 && $r <= 12 ) ? $r : 0.0;
}

/** "4" / "3.5" */
function nlfh_rooms_text( $r ) {
	$r = (float) $r;
	return abs( $r - round( $r ) ) < 0.01 ? (string) (int) round( $r ) : rtrim( rtrim( number_format( $r, 1, '.', '' ), '0' ), '.' );
}

/** a whole number inside a range from a form value, null when empty, false when not valid */
function nlfh_int_field( $v, $min, $max ) {
	$v = trim( (string) $v );
	if ( '' === $v ) { return null; }
	if ( ! preg_match( '/^-?\d{1,4}$/', $v ) ) { return false; }
	$n = (int) $v;
	return ( $n >= $min && $n <= $max ) ? $n : false;
}

/** a shekel amount from what people type ("3,450,000", "₪ 3450000"); 0 when there are no digits or it is out of 100,000..200,000,000 */
function nlfh_amount_parse( $s ) {
	$s = (string) $s;
	if ( preg_match( '/[.,]\d{1,2}$/', trim( $s ) ) && ! preg_match( '/,\d{3}$/', trim( $s ) ) ) { return 0; } // agorot are not a price
	$d = preg_replace( '/\D+/', '', $s );
	if ( '' === $d || strlen( $d ) > 10 ) { return 0; }
	$n = (int) $d;
	return ( $n >= 100000 && $n <= 200000000 ) ? $n : 0;
}

/** "₪3,250,000" */
function nlfh_money( $n ) { return '₪' . number_format( (int) $n ); }

/** "₪3.21 מ'" for a million and more, "₪850 אלף" below it */
function nlfh_money_short( $n ) {
	$n = (int) $n;
	if ( $n >= 1000000 ) {
		$m = rtrim( rtrim( number_format( $n / 1000000, 2, '.', '' ), '0' ), '.' );
		return '₪' . $m . " מ'";
	}
	return '₪' . number_format( (int) round( $n / 1000 ) ) . ' אלף';
}

/** "קומה 6 מתוך 9", "קומת קרקע", "קומה 3"; '' without a floor */
function nlfh_floor_text( $floor, $floors ) {
	if ( null === $floor || '' === $floor ) { return ''; }
	$f = (int) $floor;
	$t = 0 === $f ? 'קומת קרקע' : 'קומה ' . $f;
	return ( null !== $floors && '' !== $floors && (int) $floors > 0 ) ? $t . ' מתוך ' . (int) $floors : $t;
}

/** the headline of the card: "4 חדרים, 98 מ"ר, קומה 6 מתוך 9" (parts that are empty are left out) */
function nlfh_headline( array $f ) {
	$r     = (float) ( $f['rooms'] ?? 0 );
	$parts = array();
	if ( $r > 0 ) { $parts[] = 1.0 === $r ? 'חדר אחד' : nlfh_rooms_text( $r ) . ' חדרים'; }
	if ( ! empty( $f['sqm'] ) ) { $parts[] = (int) $f['sqm'] . ' מ"ר'; }
	$fl = nlfh_floor_text( $f['floor'] ?? null, $f['floors'] ?? null );
	if ( '' !== $fl ) { $parts[] = $fl; }
	return implode( ', ', $parts );
}

/** "רחוב הרצל, רמת גן" / "רמת גן" */
function nlfh_place( array $f ) {
	$street = trim( (string) ( $f['street'] ?? '' ) );
	$city   = trim( (string) ( $f['city'] ?? '' ) );
	return implode( ', ', array_filter( array( '' !== $street ? 'רחוב ' . $street : '', $city ) ) );
}

/** the discussion's title, built on the server: "<rooms> חדרים, <m²> מ"ר, קומה <f> מתוך <F> · <street>, <city>: כמה היא שווה?" */
function nlfh_title( array $f ) {
	$head  = nlfh_headline( $f );
	$street = trim( (string) ( $f['street'] ?? '' ) );
	$place = implode( ', ', array_filter( array( $street, trim( (string) ( $f['city'] ?? '' ) ) ) ) );
	$t     = implode( ' · ', array_filter( array( $head, $place ) ) );
	return ( '' !== $t ? $t : 'דירה' ) . ': כמה היא שווה?';
}

/** the median of a list of numbers; 0 for none */
function nlfh_median( array $a ) {
	$a = array_values( array_map( 'floatval', $a ) );
	$n = count( $a );
	if ( ! $n ) { return 0; }
	sort( $a );
	$m = intdiv( $n, 2 );
	return $n % 2 ? $a[ $m ] : ( $a[ $m - 1 ] + $a[ $m ] ) / 2;
}

/** the p-th percentile (0..100), linear between the two nearest ranks (the spreadsheet PERCENTILE.INC) */
function nlfh_pct( array $a, $p ) {
	$a = array_values( array_map( 'floatval', $a ) );
	$n = count( $a );
	if ( ! $n ) { return 0; }
	sort( $a );
	$x  = ( $n - 1 ) * max( 0, min( 100, (float) $p ) ) / 100;
	$lo = (int) floor( $x );
	$hi = (int) ceil( $x );
	return $a[ $lo ] + ( $a[ $hi ] - $a[ $lo ] ) * ( $x - $lo );
}

/** for each amount: true when it lies outside 0.3x..3x of the median of the OTHER amounts (kept in the list, left out of the band) */
function nlfh_outliers( array $a ) {
	$a   = array_values( array_map( 'floatval', $a ) );
	$out = array();
	foreach ( $a as $i => $v ) {
		$others = $a;
		unset( $others[ $i ] );
		if ( ! $others ) { $out[] = false; continue; }
		$m     = nlfh_median( $others );
		$out[] = $m > 0 && ( $v < 0.3 * $m || $v > 3 * $m );
	}
	return $out;
}

/** the summary box of part ב: count (all), and the median and the 25-75% band of the amounts that are not outliers */
function nlfh_est_summary( array $amounts ) {
	$amounts = array_values( array_map( 'intval', $amounts ) );
	$flags   = nlfh_outliers( $amounts );
	$kept    = array();
	foreach ( $amounts as $i => $v ) { if ( empty( $flags[ $i ] ) ) { $kept[] = $v; } }
	if ( ! $kept ) { $kept = $amounts; }
	return array(
		'count'  => count( $amounts ),
		'kept'   => count( $kept ),
		'median' => (int) round( nlfh_median( $kept ) ),
		'p25'    => (int) round( nlfh_pct( $kept, 25 ) ),
		'p75'    => (int) round( nlfh_pct( $kept, 75 ) ),
	);
}

/** below 3 estimates the box waits: how many more are needed (0 = show it) */
function nlfh_est_missing( $count ) { return max( 0, 3 - (int) $count ); }

/**
 * Positions on the track of part ב, as percentages from the RIGHT edge (right to left: the price grows to the left, as on the
 * board). The scale covers the band, the median and the asking price with 15% air on each side.
 */
function nlfh_track( $lo, $hi, $med, $ask = 0 ) {
	$vals = array_filter( array( (float) $lo, (float) $hi, (float) $med, (float) $ask ), function ( $v ) { return $v > 0; } );
	if ( ! $vals ) { return null; }
	$a   = min( $vals );
	$b   = max( $vals );
	$pad = $b > $a ? ( $b - $a ) * 0.15 : max( 1, $a * 0.05 );
	$a  -= $pad;
	$b  += $pad;
	$pos = function ( $v ) use ( $a, $b ) { return round( ( (float) $v - $a ) / ( $b - $a ) * 100, 1 ); };
	return array(
		'band_r' => $pos( $lo ),
		'band_w' => round( max( 1.5, $pos( $hi ) - $pos( $lo ) ), 1 ),
		'med'    => $pos( $med ),
		'ask'    => (float) $ask > 0 ? $pos( $ask ) : null,
	);
}

/** the three parts of the vote bar: 1 זול, 2 הוגן, 3 יקר => whole percentages that add up to 100 (largest remainder) */
function nlfh_vote_split( array $counts ) {
	$c   = array( 1 => (int) ( $counts[1] ?? 0 ), 2 => (int) ( $counts[2] ?? 0 ), 3 => (int) ( $counts[3] ?? 0 ) );
	$sum = array_sum( $c );
	if ( $sum < 1 ) { return array( 1 => 0, 2 => 0, 3 => 0 ); }
	$p = array(); $rem = array();
	foreach ( $c as $k => $n ) { $x = $n * 100 / $sum; $p[ $k ] = (int) floor( $x ); $rem[ $k ] = $x - $p[ $k ]; }
	$left = 100 - array_sum( $p );
	arsort( $rem );
	foreach ( array_keys( $rem ) as $k ) { if ( $left <= 0 ) { break; } $p[ $k ]++; $left--; }
	ksort( $p );
	return $p;
}

/** the vote labels */
function nlfh_vote_words() { return array( 1 => 'זול', 2 => 'הוגן', 3 => 'יקר' ); }

/** the key of a voter: a member by id, a guest browser by its random cookie; '' for neither */
function nlfh_voter_key( $member_id, $cookie, $key ) {
	if ( (int) $member_id > 0 ) { return hash_hmac( 'sha256', 'vm|' . (int) $member_id, (string) $key ); }
	if ( preg_match( '/^[a-f0-9]{32}$/', (string) $cookie ) ) { return hash_hmac( 'sha256', 'vg|' . $cookie, (string) $key ); }
	return '';
}

/** JSON of the public files: a UTF-8 BOM may open them; null when it is not an object */
function nlfh_json( $raw ) {
	$raw = (string) $raw;
	if ( "\xEF\xBB\xBF" === substr( $raw, 0, 3 ) ) { $raw = substr( $raw, 3 ); }
	$j = json_decode( $raw, true );
	return is_array( $j ) ? $j : null;
}

/** '20-08-2026' -> '20.8.2026'; '' when it is not a date */
function nlfh_version_date( $v ) {
	if ( ! preg_match( '/^(\d{1,2})-(\d{1,2})-(\d{4})$/', trim( (string) $v ), $m ) ) { return ''; }
	return (int) $m[1] . '.' . (int) $m[2] . '.' . $m[3];
}

/** the bucket of the public files for a number of rooms: '3', '4', '5', or 'all' outside them */
function nlfh_room_bucket( $rooms ) {
	$f = (int) floor( (float) $rooms );
	return in_array( $f, array( 3, 4, 5 ), true ) ? (string) $f : 'all';
}

/** "דירות 4 חדרים" / "כל הדירות" */
function nlfh_bucket_label( $b ) { return 'all' === (string) $b ? 'כל הדירות' : 'דירות ' . (string) $b . ' חדרים'; }

/** trends.rooms[] -> bucket => last year's average closed-deal price (only real positive numbers) */
function nlfh_rooms_avgs( $j ) {
	$out = array();
	foreach ( (array) ( $j['trends']['rooms'] ?? array() ) as $r ) {
		if ( ! is_array( $r ) || ! isset( $r['numRooms'] ) ) { continue; }
		$k = (string) $r['numRooms'];
		$v = $r['summary']['lastYearAvgPrice'] ?? null;
		if ( ! in_array( $k, array( '3', '4', '5', 'all' ), true ) || ! is_numeric( $v ) || (float) $v <= 0 ) { continue; }
		$out[ $k ] = (int) round( (float) $v );
	}
	return $out;
}

/** a settlement file -> array( name, version, nbhds id => title, rooms bucket => average ); null when it is not one */
function nlfh_settlement_parse( $raw ) {
	$j = nlfh_json( $raw );
	if ( ! $j || ! isset( $j['settlementName'] ) ) { return null; }
	$nb = array();
	foreach ( (array) ( $j['otherNeighborhoods'] ?? array() ) as $n ) {
		if ( is_array( $n ) && isset( $n['id'], $n['title'] ) && (int) $n['id'] > 0 && '' !== trim( (string) $n['title'] ) ) {
			$nb[ (int) $n['id'] ] = mb_substr( trim( (string) $n['title'] ), 0, 80 );
		}
	}
	return array( 'name' => (string) $j['settlementName'], 'version' => (string) ( $j['version'] ?? '' ), 'nbhds' => $nb, 'rooms' => nlfh_rooms_avgs( $j ) );
}

/** a neighbourhood file -> array( name, settlement, version, rooms bucket => average ); null when it is not one */
function nlfh_nbhd_parse( $raw ) {
	$j = nlfh_json( $raw );
	if ( ! $j || ! isset( $j['neighborhoodName'] ) ) { return null; }
	return array( 'name' => (string) $j['neighborhoodName'], 'settlement' => (int) ( $j['settlementID'] ?? 0 ), 'version' => (string) ( $j['version'] ?? '' ), 'rooms' => nlfh_rooms_avgs( $j ) );
}

/** the address of a public file; only the two kinds this module reads (never /street/) */
function nlfh_data_url( $kind, $id ) {
	if ( ! in_array( $kind, array( 'settlement', 'neighborhood' ), true ) || (int) $id <= 0 ) { return ''; }
	return 'https://data.nadlan.gov.il/api/pages/' . $kind . '/buy/' . (int) $id . '.json';
}

/** the discussion of the week: rows of array( id, score, created ) -> the id with the highest score, the newest on a tie; 0 for none */
function nlfh_hot_pick( array $rows ) {
	$best = 0; $bs = -1; $bt = '';
	foreach ( $rows as $r ) {
		$s = (int) ( $r['score'] ?? 0 ); $t = (string) ( $r['created'] ?? '' ); $id = (int) ( $r['id'] ?? 0 );
		if ( $id <= 0 ) { continue; }
		if ( $s > $bs || ( $s === $bs && ( $t > $bt || ( $t === $bt && $id > $best ) ) ) ) { $best = $id; $bs = $s; $bt = $t; }
	}
	return $best;
}

/** the share text of part ה */
function nlfh_share_text( $title, $url ) { return 'כמה הייתם נותנים על הדירה הזו? ' . (string) $title . ' ' . (string) $url; }

/** "212 הצביעו · 31 תגובות · 4 אנשי מקצוע" without the parts that are zero */
function nlfh_stats_line( $votes, $replies, $pros ) {
	$p = array();
	if ( (int) $votes > 0 ) { $p[] = 1 === (int) $votes ? 'הצבעה אחת' : number_format( (int) $votes ) . ' הצביעו'; }
	if ( (int) $replies > 0 ) { $p[] = 1 === (int) $replies ? 'תגובה אחת' : number_format( (int) $replies ) . ' תגובות'; }
	if ( (int) $pros > 0 ) { $p[] = 1 === (int) $pros ? 'איש מקצוע אחד' : number_format( (int) $pros ) . ' אנשי מקצוע'; }
	return implode( ' · ', $p );
}

if ( defined( 'NLFH_PURE_ONLY' ) ) { return; }

/* =========================================================================================================
 * 2. Tables, the public files, the rows of one discussion
 * ======================================================================================================= */

function nlfh_t( $name ) { global $wpdb; return $wpdb->prefix . 'nadlan_forum_' . $name; }

function nlfh_ready() { return NLFH_DB === (string) get_option( 'nadlan_forum_home_db' ); }

/** the three tables once per NLFH_DB (never on every request); a failed attempt waits an hour */
function nlfh_install() {
	if ( nlfh_ready() || get_transient( 'nlfh_install_wait' ) || ! function_exists( 'nlf_db_ready' ) || ! nlf_db_ready() ) { return; }
	global $wpdb;
	require_once ABSPATH . 'wp-admin/includes/upgrade.php';
	$c = $wpdb->get_charset_collate();
	dbDelta( 'CREATE TABLE ' . nlfh_t( 'homes' ) . " (
		topic_id BIGINT UNSIGNED NOT NULL,
		city VARCHAR(60) NOT NULL DEFAULT '',
		settlement_code INT UNSIGNED NOT NULL DEFAULT 0,
		nbhd_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
		nbhd_name VARCHAR(80) NOT NULL DEFAULT '',
		street VARCHAR(60) NOT NULL DEFAULT '',
		rooms DECIMAL(3,1) NOT NULL DEFAULT 0,
		sqm SMALLINT UNSIGNED NULL,
		floor SMALLINT NULL,
		floors SMALLINT UNSIGNED NULL,
		asking BIGINT UNSIGNED NULL,
		state VARCHAR(10) NOT NULL DEFAULT '',
		intent VARCHAR(10) NOT NULL DEFAULT '',
		PRIMARY KEY  (topic_id),
		KEY settlement_code (settlement_code)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlfh_t( 'votes' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		topic_id BIGINT UNSIGNED NOT NULL,
		voter_key CHAR(64) NOT NULL,
		vote TINYINT UNSIGNED NOT NULL DEFAULT 0,
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY one_vote (topic_id,voter_key),
		KEY topic_created (topic_id,created_at)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlfh_t( 'estimates' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		topic_id BIGINT UNSIGNED NOT NULL,
		member_id BIGINT UNSIGNED NOT NULL,
		reply_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
		amount BIGINT UNSIGNED NOT NULL DEFAULT 0,
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY one_estimate (topic_id,member_id),
		KEY reply_id (reply_id)
	) $c;" );
	foreach ( array( 'homes', 'votes', 'estimates' ) as $name ) {
		if ( nlfh_t( $name ) !== (string) $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $wpdb->esc_like( nlfh_t( $name ) ) ) ) ) {
			set_transient( 'nlfh_install_wait', 1, HOUR_IN_SECONDS );
			return;
		}
	}
	update_option( 'nadlan_forum_home_db', NLFH_DB, true );
}
add_action( 'admin_init', 'nlfh_install', 25 );

/**
 * One public file, parsed and kept 7 days ('settlement' or 'neighborhood'); null when it is missing or the fetch failed (a failure
 * is remembered for an hour, so a page never waits on it twice). The files answer with a UTF-8 BOM; nlfh_json() takes it off.
 */
function nlfh_data( $kind, $id ) {
	$url = nlfh_data_url( $kind, $id );
	if ( '' === $url ) { return null; }
	$tk = 'nlfh_' . ( 'settlement' === $kind ? 's' : 'n' ) . '_' . (int) $id;
	$c  = get_transient( $tk );
	if ( is_array( $c ) ) { return empty( $c['fail'] ) ? $c : null; }
	$r = wp_remote_get( $url, array( 'timeout' => 6, 'redirection' => 0, 'headers' => array( 'Accept' => 'application/json' ) ) );
	$p = null;
	if ( ! is_wp_error( $r ) && 200 === (int) wp_remote_retrieve_response_code( $r ) ) {
		$body = (string) wp_remote_retrieve_body( $r );
		$p    = 'settlement' === $kind ? nlfh_settlement_parse( $body ) : nlfh_nbhd_parse( $body );
	}
	if ( ! $p ) { set_transient( $tk, array( 'fail' => 1 ), HOUR_IN_SECONDS ); return null; }
	set_transient( $tk, $p, 7 * DAY_IN_SECONDS );
	return $p;
}

/** the apartment row of a discussion, or null */
function nlfh_home( $tid ) {
	static $memo = array();
	$tid = (int) $tid;
	if ( $tid <= 0 || ! nlfh_ready() ) { return null; }
	if ( array_key_exists( $tid, $memo ) ) { return $memo[ $tid ]; }
	global $wpdb;
	$r = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlfh_t( 'homes' ) . ' WHERE topic_id = %d', $tid ), ARRAY_A );
	return $memo[ $tid ] = $r ? $r : null;
}

/** 1 => n, 2 => n, 3 => n */
function nlfh_vote_counts( $tid ) {
	global $wpdb;
	$c = array( 1 => 0, 2 => 0, 3 => 0 );
	foreach ( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT vote, COUNT(*) AS n FROM ' . nlfh_t( 'votes' ) . ' WHERE topic_id = %d GROUP BY vote', (int) $tid ), ARRAY_A ) as $r ) {
		if ( isset( $c[ (int) $r['vote'] ] ) ) { $c[ (int) $r['vote'] ] = (int) $r['n']; }
	}
	return $c;
}

/** this request's voter key (member, or the guest browser's cookie) */
function nlfh_my_key() {
	$m = function_exists( 'nlf_me' ) ? nlf_me() : null;
	return nlfh_voter_key( $m ? (int) $m['id'] : 0, isset( $_COOKIE['nlfh_v'] ) ? (string) $_COOKIE['nlfh_v'] : '', nlf_key() );
}

/** the vote this request gave on a discussion (1..3), 0 for none */
function nlfh_my_vote( $tid ) {
	$k = nlfh_my_key();
	if ( '' === $k ) { return 0; }
	global $wpdb;
	return (int) $wpdb->get_var( $wpdb->prepare( 'SELECT vote FROM ' . nlfh_t( 'votes' ) . ' WHERE topic_id = %d AND voter_key = %s', (int) $tid, $k ) );
}

/** the estimates of a discussion whose answer is live: rows of reply_id, member_id, amount (oldest first) */
function nlfh_estimates( $tid ) {
	static $memo = array();
	$tid = (int) $tid;
	if ( isset( $memo[ $tid ] ) ) { return $memo[ $tid ]; }
	global $wpdb;
	$rows = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT e.reply_id, e.member_id, e.amount FROM ' . nlfh_t( 'estimates' ) . ' e JOIN ' . nlf_t( 'replies' ) . " r ON r.id = e.reply_id
		WHERE e.topic_id = %d AND r.status = 'live' ORDER BY e.id ASC LIMIT 500", $tid ), ARRAY_A );
	return $memo[ $tid ] = $rows;
}

/** members with a trade who answered (a linked card, or a member who chose a trade) */
function nlfh_pros_count( $tid ) {
	global $wpdb;
	return (int) $wpdb->get_var( $wpdb->prepare( 'SELECT COUNT(DISTINCT r.member_id) FROM ' . nlf_t( 'replies' ) . ' r JOIN ' . nlf_t( 'members' ) . " m ON m.id = r.member_id
		WHERE r.topic_id = %d AND r.status = 'live' AND ( ( m.pro_id IS NOT NULL AND m.pro_id > 0 ) OR ( m.role_label = 'pro' AND m.trade <> '' ) )", (int) $tid ) );
}

/** the shown pictures of the opening message (media module), in their order; array() without the module */
function nlfh_photos( $tid ) {
	if ( ! function_exists( 'nlfmd_ready' ) || ! nlfmd_ready() ) { return array(); }
	global $wpdb;
	$out = array();
	foreach ( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlfmd_t( 'media' ) . " WHERE topic_id = %d AND reply_id IS NULL AND kind = 'image' AND status = 'ok' ORDER BY sort ASC, id ASC LIMIT 20", (int) $tid ), ARRAY_A ) as $r ) {
		if ( nlfmd_rel_ok( (string) $r['path'] ) ) { $out[] = $r; }
	}
	return $out;
}

/* =========================================================================================================
 * 3. Hooks into the forum's core: the kind, the generic route, the estimate of an answer
 * ======================================================================================================= */

// HOOK nlf_kinds (inc/pro-forum.php): the kind of the presented apartment (labels, tags, the compose sheet's grid)
add_filter( 'nlf_kinds', function ( $k ) {
	$k = (array) $k;
	$k['home'] = 'דירה לדיון';
	return $k;
} );

/** this request is the home route itself (the generic topic route refuses kind 'home': it has no apartment row) */
function nlfh_creating( $on = null ) {
	static $f = false;
	if ( null !== $on ) { $f = (bool) $on; }
	return $f;
}

// HOOK nlf_post_check (inc/pro-forum.php, the topic and reply routes, before the insert)
add_filter( 'nlf_post_check', function ( $err, $type, $m, $q, $t = null ) {
	if ( '' !== (string) $err || ! ( $q instanceof WP_REST_Request ) || ! is_array( $m ) ) { return $err; }
	if ( 'topic' === $type ) {
		return ( 'home' === sanitize_key( (string) $q->get_param( 'kind' ) ) && ! nlfh_creating() ) ? 'כדי להציג דירה, השתמשו בטופס "כמה הדירה שלכם שווה?".' : $err;
	}
	$raw = trim( (string) $q->get_param( 'estimate' ) );
	if ( 'reply' !== $type || '' === $raw ) { return $err; }
	if ( ! is_array( $t ) || 'home' !== (string) $t['kind'] ) { return 'הערכת מחיר אפשר לתת רק בדיון על דירה.'; }
	if ( (int) $t['member_id'] === (int) $m['id'] ) { return 'את הדירה שלכם לא מעריכים. ההערכות הן של חברי הפורום.'; }
	if ( nlfh_amount_parse( $raw ) <= 0 ) { return 'ההערכה צריכה להיות מחיר בשקלים, למשל 3,250,000.'; }
	nlfh_install();
	return nlfh_ready() ? $err : 'הערכות מחיר לא זמינות כרגע. שלחו בלי ההערכה או נסו שוב בעוד רגע.';
}, 20, 5 );

// HOOK nlf_post_created (inc/pro-forum.php, after the insert of a reply): one estimate per member per discussion, the latest wins
add_action( 'nlf_post_created', function ( $type, $id, $m, $q, $status, $tid ) {
	if ( 'reply' !== $type || ! ( $q instanceof WP_REST_Request ) || ! nlfh_ready() ) { return; }
	$amount = nlfh_amount_parse( (string) $q->get_param( 'estimate' ) );
	if ( $amount <= 0 ) { return; }
	global $wpdb;
	$wpdb->query( $wpdb->prepare( 'INSERT INTO ' . nlfh_t( 'estimates' ) . ' (topic_id, member_id, reply_id, amount, created_at) VALUES (%d, %d, %d, %d, %s)
		ON DUPLICATE KEY UPDATE reply_id = VALUES(reply_id), amount = VALUES(amount), created_at = VALUES(created_at)', (int) $tid, (int) $m['id'], (int) $id, $amount, nlf_now_sql() ) );
	delete_transient( 'nlfh_hot' );
}, 20, 6 );

// HOOK nlf_reply_before_body (inc/pro-forum-render.php): "ההערכה שלי: ₪3,250,000" on the answer that holds the member's estimate
add_filter( 'nlf_reply_before_body', function ( $html, $r, $t ) {
	if ( ! is_array( $t ) || 'home' !== (string) ( $t['kind'] ?? '' ) || ! is_array( $r ) || ! nlfh_ready() ) { return $html; }
	global $wpdb;
	static $by = array();
	if ( ! isset( $by[ (int) $t['id'] ] ) ) {
		$by[ (int) $t['id'] ] = array();
		foreach ( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT reply_id, amount FROM ' . nlfh_t( 'estimates' ) . ' WHERE topic_id = %d', (int) $t['id'] ), ARRAY_A ) as $e ) {
			$by[ (int) $t['id'] ][ (int) $e['reply_id'] ] = (int) $e['amount'];
		}
	}
	$a = $by[ (int) $t['id'] ][ (int) $r['id'] ] ?? 0;
	return $a > 0 ? $html . '<span class="nlfh-chip">' . esc_html( 'ההערכה שלי: ' . nlfh_money( $a ) ) . '</span>' : $html;
}, 10, 3 );

/* =========================================================================================================
 * 4. REST: nadlan/v1/forum/home, home/nbhd, home/vote
 * ======================================================================================================= */

/** the one-tap vote's guard: gate, trap, form time (1 second), the proof of work (single use), 200 votes a day per hashed IP */
function nlfh_vote_guard( WP_REST_Request $q ) {
	if ( ! nlf_gate_open() ) { return nlf_err( 'הדף לא נמצא.', 'nlf_closed' ); }
	nlf_install();
	nlfh_install();
	if ( ! nlfh_ready() ) { return nlf_err( 'ההצבעה לא זמינה כרגע. נסו שוב בעוד רגע.' ); }
	if ( '' !== trim( (string) $q->get_param( 'website' ) ) ) { return nlf_err( 'לא הצלחנו לשלוח. נסו שוב.' ); }
	$e = nlf_form_ts_error( (string) $q->get_param( 'ts' ), nlf_key(), time(), 1 );
	if ( '' !== $e ) { return nlf_err( $e, 'nlf_ts' ); }
	$salt = nlf_challenge_check( (string) $q->get_param( 'ch' ), (string) $q->get_param( 'n' ), nlf_key(), time(), 600 );
	if ( '' === $salt || get_transient( 'nlf_pw_' . $salt ) ) { return nlf_err( 'בדיקת האבטחה לא הושלמה. נסו שוב.', 'nlf_pow' ); }
	set_transient( 'nlf_pw_' . $salt, 1, 15 * MINUTE_IN_SECONDS );
	if ( ! nlf_rl( 'nlfh_v', 200, DAY_IN_SECONDS ) ) { return nlf_err( 'הגעתם למספר ההצבעות המרבי להיום.' ); }
	$m = nlf_me();
	if ( $m ) {
		if ( ! hash_equals( nlf_nonce_for( $m ), (string) $q->get_header( 'x_nlf_nonce' ) ) ) { return nlf_err( 'הדף ישן. רעננו אותו ונסו שוב.', 'nlf_nonce' ); }
		if ( 'ok' !== (string) $m['status'] ) { return nlf_err( 'החשבון הזה לא יכול להצביע כרגע.', 'nlf_blocked' ); }
		return $m;
	}
	return array();
}

/** what the page script gets back after a vote: the three parts and the count */
function nlfh_vote_payload( $tid, $mine ) {
	$c = nlfh_vote_counts( $tid );
	return array( 'mine' => (int) $mine, 'counts' => $c, 'pct' => nlfh_vote_split( $c ), 'total' => array_sum( $c ), 'line' => nlfh_stats_line( array_sum( $c ), 0, 0 ) );
}

add_action( 'rest_api_init', function () {
	$reg = function ( $path, $method, $cb ) {
		register_rest_route( 'nadlan/v1', '/forum/' . $path, array( 'methods' => $method, 'permission_callback' => '__return_true', 'callback' => $cb, 'show_in_index' => false ) );
	};

	// a member presents an apartment (board 23 part ד); the title is built here, never taken from the page
	$reg( 'home', 'POST', function ( WP_REST_Request $q ) {
		$m = nlf_guard( $q, 'post' );
		if ( is_wp_error( $m ) ) { return $m; }
		nlfh_install();
		if ( ! nlfh_ready() ) { return nlf_err( 'הטופס לא זמין כרגע. נסו שוב בעוד רגע.' ); }
		$city = mb_substr( nlf_text_norm( (string) $q->get_param( 'city' ), true ), 0, 40 );
		$code = nlfh_city_code( $city );
		if ( nlf_len( $city ) < 2 ) { return nlf_err( 'בחרו עיר.' ); }
		if ( ! $code && ( nlf_has_link( $city ) || nlf_has_phone( $city ) || preg_match( '/\d/', $city ) ) ) { return nlf_err( 'כתבו רק את שם העיר.' ); }
		$street = mb_substr( nlf_text_norm( (string) $q->get_param( 'street' ), true ), 0, 60 );
		$street = preg_replace( '/^רחוב\s+/u', '', $street );
		$e = nlfh_street_error( $street );
		if ( '' !== $e ) { return nlf_err( $e ); }
		$rooms = nlfh_rooms_norm( (string) $q->get_param( 'rooms' ) );
		if ( $rooms <= 0 ) { return nlf_err( 'בחרו כמה חדרים, מ-1 עד 12.' ); }
		$sqm    = nlfh_int_field( (string) $q->get_param( 'sqm' ), 10, 1000 );
		$floor  = nlfh_int_field( (string) $q->get_param( 'floor' ), -3, 99 );
		$floors = nlfh_int_field( (string) $q->get_param( 'floors' ), 1, 99 );
		if ( false === $sqm ) { return nlf_err( 'שטח בין 10 ל-1,000 מ"ר, במספר שלם.' ); }
		if ( false === $floor || false === $floors ) { return nlf_err( 'קומה ומספר הקומות במספרים שלמים.' ); }
		if ( null !== $floor && null !== $floors && $floor > $floors ) { return nlf_err( 'הקומה גבוהה ממספר הקומות בבניין.' ); }
		if ( null === $floor ) { $floors = null; } // "מתוך 9" means nothing without the floor
		$ask_raw = trim( (string) $q->get_param( 'asking' ) );
		$asking  = '' === $ask_raw ? 0 : nlfh_amount_parse( $ask_raw );
		if ( '' !== $ask_raw && $asking <= 0 ) { return nlf_err( 'המחיר המבוקש בשקלים, למשל 3,450,000. אפשר גם להשאיר ריק.' ); }
		$state  = sanitize_key( (string) $q->get_param( 'state' ) );
		$state  = isset( nlfh_states()[ $state ] ) ? $state : '';
		$intent = sanitize_key( (string) $q->get_param( 'intent' ) );
		$intent = isset( nlfh_intents()[ $intent ] ) ? $intent : '';
		$nbhd_id = (int) $q->get_param( 'nbhd' );
		$nbhd    = '';
		if ( $nbhd_id > 0 ) { // only a neighbourhood the city's public file lists; its name comes from the file, not from the page
			$sd = $code ? nlfh_data( 'settlement', $code ) : null;
			if ( ! $sd || ! isset( $sd['nbhds'][ $nbhd_id ] ) ) { $nbhd_id = 0; } else { $nbhd = (string) $sd['nbhds'][ $nbhd_id ]; }
		}
		$body = nlf_text_norm( (string) $q->get_param( 'body' ) );
		$e    = nlf_body_error( $body, false );
		if ( '' !== $e ) { return nlf_err( $e ); }
		$f     = array( 'rooms' => $rooms, 'sqm' => $sqm, 'floor' => $floor, 'floors' => $floors, 'street' => $street, 'city' => $city );
		$title = nlfh_title( $f );
		$e     = nlf_title_error( $title );
		if ( '' !== $e ) { return nlf_err( $e ); }
		$e = nlf_post_limits( $m, true, $title . "\n" . $body . "\n" . $city );
		if ( '' !== $e ) { return nlf_err( $e ); }
		nlfh_creating( true );
		$e = (string) apply_filters( 'nlf_post_check', '', 'topic', $m, $q, null ); // the media module checks the pictures
		nlfh_creating( false );
		if ( '' !== $e ) { return nlf_err( $e ); }
		global $wpdb;
		$status = nlf_first_status( $m['approved_posts'], $title . "\n" . $body, '0' !== (string) get_option( 'nadlan_forum_autoapprove', '1' ) );
		$now    = nlf_now_sql();
		$wpdb->insert( nlf_t( 'topics' ), array( 'cat' => 'value', 'kind' => 'home', 'title' => $title, 'body' => $body, 'member_id' => (int) $m['id'], 'pro_id' => null,
			'city' => $city, 'status' => $status, 'body_hash' => nlf_dup_key( $title . "\n" . $body . "\n" . $city ), 'ip_hash' => nlf_ip_hash(), 'created_at' => $now, 'last_at' => $now ) );
		$id = (int) $wpdb->insert_id;
		if ( $id <= 0 ) { return nlf_err( 'משהו השתבש. נסו שוב.' ); }
		$wpdb->insert( nlfh_t( 'homes' ), array( 'topic_id' => $id, 'city' => $city, 'settlement_code' => $code, 'nbhd_id' => $nbhd_id, 'nbhd_name' => $nbhd, 'street' => $street,
			'rooms' => $rooms, 'sqm' => $sqm, 'floor' => $floor, 'floors' => $floors, 'asking' => $asking > 0 ? $asking : null, 'state' => $state, 'intent' => $intent ) );
		do_action( 'nlf_post_created', 'topic', $id, $m, $q, $status, $id ); // the media module attaches the pictures
		nlf_write_counted( $m );
		nlf_follow( (int) $m['id'], $id, true );
		if ( 'live' === $status ) { nlf_on_topic_live( $id ); } else { nlf_mail_admin_pending( 'topic', $id ); }
		if ( $code ) { nlfh_data( 'settlement', $code ); } // warm the averages for the first visitors
		if ( $nbhd_id ) { nlfh_data( 'neighborhood', $nbhd_id ); }
		delete_transient( 'nlfh_hot' );
		return nlf_ok( array( 'id' => $id, 'url' => home_url( '/forum/' . $id . '/' ), 'status' => $status,
			'message' => 'live' === $status ? 'הדירה הוצגה לפורום.' : 'ההודעה תעלה אחרי בדיקה קצרה.' ) );
	} );

	// the city's neighbourhoods for the form's second list (from the city's public file, cached 7 days)
	$reg( 'home/nbhd', 'GET', function ( WP_REST_Request $q ) {
		if ( ! nlf_gate_open() ) { return nlf_err( 'הדף לא נמצא.', 'nlf_closed' ); }
		$code = (int) $q->get_param( 'code' );
		if ( ! nlfh_code_ok( $code ) || ! nlf_rl( 'nlfh_nb', 120, HOUR_IN_SECONDS ) ) { return nlf_ok( array( 'items' => array() ) ); }
		$sd    = nlfh_data( 'settlement', $code );
		$items = array();
		foreach ( (array) ( $sd['nbhds'] ?? array() ) as $id => $title ) { $items[] = array( 'id' => (int) $id, 'title' => (string) $title ); }
		usort( $items, function ( $a, $b ) { return strcmp( $a['title'], $b['title'] ); } );
		return nlf_ok( array( 'items' => $items ) );
	} );

	// one tap: זול / הוגן / יקר. A member once (a change is allowed); a guest browser once per discussion (cookie), and one new
	// guest vote per discussion per hashed IP a day. The author does not vote on his own price; the results come back.
	$reg( 'home/vote', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfh_vote_guard( $q );
		if ( is_wp_error( $m ) ) { return $m; }
		$tid  = (int) $q->get_param( 'topic_id' );
		$vote = (int) $q->get_param( 'vote' );
		$t    = nlf_topic( $tid );
		$h    = nlfh_home( $tid );
		if ( ! $t || 'live' !== $t['status'] || 'home' !== $t['kind'] || ! $h ) { return nlf_err( 'הדיון לא נמצא.' ); }
		if ( empty( $h['asking'] ) ) { return nlf_err( 'בדירה הזו לא צוין מחיר, אז אין על מה להצביע. אפשר לתת הערכה בתגובה.' ); }
		if ( ! isset( nlfh_vote_words()[ $vote ] ) ) { return nlf_err( 'בחרו זול, הוגן או יקר.' ); }
		if ( $m && (int) $m['id'] === (int) $t['member_id'] ) { return nlf_err( 'על המחיר של הדירה שלכם לא מצביעים. התוצאות מוצגות לכם.' ); }
		$cookie = isset( $_COOKIE['nlfh_v'] ) ? (string) $_COOKIE['nlfh_v'] : '';
		if ( ! $m && ! preg_match( '/^[a-f0-9]{32}$/', $cookie ) ) {
			$cookie = bin2hex( random_bytes( 16 ) );
			nlf_cookie( 'nlfh_v', $cookie, time() + 365 * DAY_IN_SECONDS, true );
		}
		$key = nlfh_voter_key( $m ? (int) $m['id'] : 0, $cookie, nlf_key() );
		global $wpdb;
		$vt  = nlfh_t( 'votes' );
		$had = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $vt WHERE topic_id = %d AND voter_key = %s", $tid, $key ) );
		if ( $had ) {
			$wpdb->update( $vt, array( 'vote' => $vote ), array( 'id' => $had ) );
		} else {
			$ipk = 'nlfh_ip_' . md5( $tid . '|' . nlf_ip_hash() . '|' . gmdate( 'Ymd' ) );
			if ( ! $m && get_transient( $ipk ) ) { return nlf_err( 'מהחיבור הזה כבר הצביעו היום על הדירה הזו.' ); }
			$wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO $vt (topic_id, voter_key, vote, created_at) VALUES (%d, %s, %d, %s)", $tid, $key, $vote, nlf_now_sql() ) );
			if ( ! $m ) { set_transient( $ipk, 1, DAY_IN_SECONDS ); }
		}
		return nlf_ok( nlfh_vote_payload( $tid, $vote ) + array( 'message' => 'ההצבעה נקלטה. כך הצביעו כולם:' ) );
	} );
} );

/* =========================================================================================================
 * 5. HTML: the card of part א, the results of part ב, the actions of part ג, the sheet of part ד
 * ======================================================================================================= */

/** the dark one-tap box, or the three-part bar for someone who voted / the author (board 23 parts א and ב) */
function nlfh_vote_html( $tid, $asking, $mine, $is_author ) {
	$tid = (int) $tid;
	if ( (int) $asking <= 0 ) { return ''; }
	$c = nlfh_vote_counts( $tid );
	if ( $mine || $is_author ) { return nlfh_bar_html( $c, (int) $mine, $is_author ); }
	$h = '<div class="nlfh-vote" data-nlfh-votebox data-topic="' . $tid . '"><span class="nlfh-vote-q" id="nlfh-vq' . $tid . '">המחיר הזה, לדעתכם:</span>'
		. '<div class="nlfh-vote-btns" role="group" aria-labelledby="nlfh-vq' . $tid . '">';
	foreach ( nlfh_vote_words() as $k => $w ) { $h .= '<button type="button" class="nlfh-vbtn" data-nlfh-vote="' . (int) $k . '">' . esc_html( $w ) . '</button>'; }
	return $h . '</div><span class="nlfh-vote-s">אחרי ההצבעה רואים מה כולם חשבו</span><p class="nlfh-msg" role="status" aria-live="polite"></p></div>';
}

/** the bar: green זול, sea הוגן, raspberry יקר; a part narrower than 22% shows its number only */
function nlfh_bar_html( array $counts, $mine, $is_author ) {
	$total = array_sum( $counts );
	$pct   = nlfh_vote_split( $counts );
	$words = nlfh_vote_words();
	$h     = '<div class="nlfh-res" data-nlfh-res>';
	if ( $total > 0 ) {
		$h .= '<div class="nlfh-bar" role="img" aria-label="' . esc_attr( 'זול ' . $pct[1] . '%, הוגן ' . $pct[2] . '%, יקר ' . $pct[3] . '%' ) . '">';
		foreach ( array( 1 => 'cheap', 2 => 'fair', 3 => 'dear' ) as $k => $cls ) {
			if ( $pct[ $k ] < 1 ) { continue; }
			$h .= '<span class="nlfh-bar-' . $cls . '" style="width:' . (int) $pct[ $k ] . '%">' . esc_html( ( $pct[ $k ] >= 22 ? $words[ $k ] . ' ' : '' ) . $pct[ $k ] . '%' ) . '</span>';
		}
		$h .= '</div>';
	}
	$who = $mine ? 'הצבעתם: ' . $words[ (int) $mine ] : ( $is_author ? 'כך הקהל רואה את המחיר שלכם' : '' );
	$cnt = $total > 0 ? nlfh_stats_line( $total, 0, 0 ) : 'עוד אין הצבעות';
	$h  .= '<span class="nlfh-res-s">' . esc_html( implode( ' · ', array_filter( array( $cnt, $who ) ) ) ) . '</span>';
	return $h . '</div>';
}

/** members' estimates (part ב): the track with the band, the median dot and the asking marker; below 3, the waiting line */
function nlfh_est_html( $tid, $asking ) {
	$rows = nlfh_estimates( $tid );
	$n    = count( $rows );
	$miss = nlfh_est_missing( $n );
	$h    = '<div class="nlfh-box nlfh-est" id="nlfh-sum"><span class="nlfh-box-h">' . esc_html( 'הערכות מחיר של חברים' . ( $n > 0 ? ' (' . $n . ')' : '' ) ) . '</span>';
	if ( $miss > 0 ) {
		return $h . '<span class="nlfh-wait">' . esc_html( 1 === $miss ? 'עוד הערכה אחת ונראה את התמונה' : 'עוד ' . $miss . ' הערכות ונראה את התמונה' ) . '</span>'
			. '<span class="nlfh-fine">דעות של חברי הפורום, לא שמאות.</span></div>';
	}
	$s  = nlfh_est_summary( array_column( $rows, 'amount' ) );
	$tr = nlfh_track( $s['p25'], $s['p75'], $s['median'], (int) $asking );
	$aria = 'אמצע ההערכות ' . nlfh_money( $s['median'] ) . ', חצי מההערכות בין ' . nlfh_money( $s['p25'] ) . ' ל-' . nlfh_money( $s['p75'] ) . ( (int) $asking > 0 ? ', המבוקש ' . nlfh_money( $asking ) : '' );
	$h .= '<div class="nlfh-track" role="img" aria-label="' . esc_attr( $aria ) . '"><i class="nlfh-tr-line"></i>'
		. '<i class="nlfh-tr-band" style="right:' . esc_attr( $tr['band_r'] ) . '%;width:' . esc_attr( $tr['band_w'] ) . '%"></i>'
		. '<span class="nlfh-tr-med" style="right:calc(' . esc_attr( $tr['med'] ) . '% - 11px)"></span>'
		. ( null !== $tr['ask'] ? '<span class="nlfh-tr-ask" style="right:calc(' . esc_attr( $tr['ask'] ) . '% - 2px)"></span>' : '' ) . '</div>'
		. '<div class="nlfh-tr-keys"><span><b>' . esc_html( nlfh_money_short( $s['median'] ) ) . '</b> אמצע ההערכות</span>'
		. ( (int) $asking > 0 ? '<span class="nlfh-ask-k"><b>' . esc_html( nlfh_money_short( $asking ) ) . '</b> המבוקש</span>' : '' ) . '</div>'
		. '<span class="nlfh-fine">' . esc_html( 'חצי מההערכות בין ' . nlfh_money_short( $s['p25'] ) . ' ל-' . nlfh_money_short( $s['p75'] ) . '. דעות של חברי הפורום, לא שמאות.' ) . '</span>';
	return $h . '</div>';
}

/** the public averages box that replaces the board's street deals box (part ב): the city, and the neighbourhood when one was chosen */
function nlfh_avg_html( array $h ) {
	$code = (int) $h['settlement_code'];
	if ( ! nlfh_code_ok( $code ) ) { return ''; }
	$b    = nlfh_room_bucket( (float) $h['rooms'] );
	$rows = array();
	$ver  = '';
	$sd   = nlfh_data( 'settlement', $code );
	if ( $sd ) {
		$k = isset( $sd['rooms'][ $b ] ) ? $b : '';
		if ( '' !== $k ) { $rows[] = array( $sd['name'] . ' · ' . nlfh_bucket_label( $k ), $sd['rooms'][ $k ] ); $ver = nlfh_version_date( $sd['version'] ); }
	}
	if ( (int) $h['nbhd_id'] > 0 ) {
		$nd = nlfh_data( 'neighborhood', (int) $h['nbhd_id'] );
		if ( $nd && (int) $nd['settlement'] === $code && isset( $nd['rooms'][ $b ] ) ) {
			$rows[] = array( 'שכונת ' . $nd['name'] . ' · ' . nlfh_bucket_label( $b ), $nd['rooms'][ $b ] );
			if ( '' === $ver ) { $ver = nlfh_version_date( $nd['version'] ); }
		}
	}
	if ( ! $rows ) { return ''; }
	$o = '<div class="nlfh-box nlfh-avg"><span class="nlfh-box-h">ממוצע העסקאות בשנה האחרונה (רשות המסים)</span>';
	foreach ( $rows as $i => $r ) {
		$o .= '<div class="nlfh-avg-r' . ( $i < count( $rows ) - 1 ? ' is-line' : '' ) . '"><span>' . esc_html( $r[0] ) . '</span><b>' . esc_html( nlfh_money( $r[1] ) ) . '</b></div>';
	}
	return $o . '<span class="nlfh-fine">' . esc_html( 'נתונים פתוחים של רשות המסים' . ( '' !== $ver ? ', עדכון ' . $ver : '' ) . '. ממוצע לעיר או לשכונה, לא לרחוב ולא לבניין.' ) . '</span></div>';
}

/** the facts line under the headline: street, city · neighbourhood · state · intent · asking price */
function nlfh_facts( array $h ) {
	$st = nlfh_states(); $in = nlfh_intents();
	return implode( ' · ', array_filter( array(
		nlfh_place( $h ),
		'' !== (string) $h['nbhd_name'] ? 'שכונת ' . $h['nbhd_name'] : '',
		isset( $st[ $h['state'] ] ) ? $st[ $h['state'] ][1] : '',
		isset( $in[ $h['intent'] ] ) ? $in[ $h['intent'] ][1] : '',
		(int) $h['asking'] > 0 ? 'מבקשים ' . nlfh_money( (int) $h['asking'] ) : '',
	) ) );
}

/** the WhatsApp address with the text of part ה (no number: the person picks who gets it) */
function nlfh_wa( $t ) { return 'https://wa.me/?text=' . rawurlencode( nlfh_share_text( $t['title'], home_url( '/forum/' . (int) $t['id'] . '/' ) ) ); }

// HOOK nlf_topic_after_body (12: after the pictures at 5 and the social chips at 10, before the video row at 20): parts ב and ג
add_filter( 'nlf_topic_after_body', function ( $html, $t, $me = null ) {
	if ( ! is_array( $t ) || 'home' !== (string) ( $t['kind'] ?? '' ) ) { return $html; }
	$h = nlfh_home( (int) $t['id'] );
	if ( ! $h ) { return $html; }
	$author = is_array( $me ) && (int) $me['id'] === (int) $t['member_id'];
	$live   = 'live' === (string) $t['status'];
	$o  = '<div class="nlfh-topic" dir="rtl">';
	$o .= '<p class="nlfh-facts">' . esc_html( nlfh_facts( $h ) ) . '</p>';
	if ( $live ) { $o .= nlfh_vote_html( (int) $t['id'], (int) $h['asking'], nlfh_my_vote( (int) $t['id'] ), $author ); }
	$o .= nlfh_est_html( (int) $t['id'], (int) $h['asking'] );
	$o .= nlfh_avg_html( $h );
	if ( $live ) {
		$o .= '<div class="nlfh-acts">' . ( $author ? '' : '<a class="nlfh-btn nlfh-btn-sea" href="#nlf-reply-body" data-nlfh-estimate>להעריך את המחיר</a>' )
			. '<a class="nlfh-btn nlfh-btn-line" href="' . esc_url( nlfh_wa( $t ) ) . '" target="_blank" rel="noopener">לשלוח לחבר</a></div>';
	}
	return $html . $o . '</div>';
}, 12, 3 );

/** the discussion of the week (part א): the live home discussion with the most votes and answers in the last 7 days; 10 minutes */
function nlfh_hot_id() {
	$c = get_transient( 'nlfh_hot' );
	if ( false !== $c ) { return (int) $c; }
	global $wpdb;
	$since = gmdate( 'Y-m-d H:i:s', time() - 7 * DAY_IN_SECONDS );
	$rows  = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT t.id, t.created_at AS created,
		(SELECT COUNT(*) FROM ' . nlfh_t( 'votes' ) . ' v WHERE v.topic_id = t.id AND v.created_at >= %s)
		+ (SELECT COUNT(*) FROM ' . nlf_t( 'replies' ) . " r WHERE r.topic_id = t.id AND r.status = 'live' AND r.created_at >= %s) AS score
		FROM " . nlf_t( 'topics' ) . " t WHERE t.kind = 'home' AND t.status = 'live' ORDER BY t.id DESC LIMIT 200", $since, $since ), ARRAY_A );
	$id = nlfh_hot_pick( $rows );
	set_transient( 'nlfh_hot', $id, 10 * MINUTE_IN_SECONDS );
	return $id;
}

/** part ד's invitation: the heading and one button */
function nlfh_invite_html( $compact = false ) {
	if ( $compact ) { return '<button type="button" class="nlfh-btn nlfh-btn-ink nlfh-wide" data-nlfh-open aria-haspopup="dialog">כמה הדירה שלכם שווה? תשאלו את הפורום</button>'; }
	return '<section class="nlfh-invite" dir="rtl" aria-labelledby="nlfh-inv-h"><h2 class="nlfh-h" id="nlfh-inv-h">כמה הדירה שלכם שווה? תשאלו את הפורום</h2>'
		. '<p>מציגים את הדירה בלי מספר בית ובלי טלפון. הקהל מצביע על המחיר, וחברי הפורום ואנשי המקצוע נותנים הערכה.</p>'
		. '<button type="button" class="nlfh-btn nlfh-btn-hot nlfh-wide" data-nlfh-open aria-haspopup="dialog">להציג דירה לפורום</button></section>';
}

/** the card of part א */
function nlfh_card_html( $t, array $h ) {
	$tid    = (int) $t['id'];
	$url    = home_url( '/forum/' . $tid . '/' );
	$me     = nlf_me();
	$author = $me && (int) $me['id'] === (int) $t['member_id'];
	$pics   = nlfh_photos( $tid );
	$votes  = array_sum( nlfh_vote_counts( $tid ) );
	$o  = '<section class="nlfh-hot" dir="rtl" aria-labelledby="nlfh-hot-h"><a class="nlfh-hot-ph" href="' . esc_url( $url ) . '" tabindex="-1" aria-hidden="true">';
	if ( $pics ) {
		$p    = $pics[0];
		$rel  = (string) $p['path'];
		$w    = max( 1, (int) $p['w'] ); $hh = max( 1, (int) $p['h'] );
		$o   .= '<img src="' . esc_url( nlfmd_url( nlfmd_variant( $rel, '-480' ) ) ) . '" srcset="' . esc_url( nlfmd_url( nlfmd_variant( $rel, '-480' ) ) ) . ' 480w, ' . esc_url( nlfmd_url( $rel ) ) . ' ' . $w . 'w"'
			. ' sizes="(max-width:760px) 100vw, 728px" width="' . $w . '" height="' . $hh . '" alt="" loading="lazy" decoding="async">';
	}
	$o .= '<span class="nlfh-badge">הדירה שמדברים עליה</span>' . ( count( $pics ) > 1 ? '<span class="nlfh-count">1 / ' . count( $pics ) . '</span>' : '' ) . '</a>';
	$o .= '<div class="nlfh-hot-b"><h2 class="nlfh-hot-t" id="nlfh-hot-h"><a href="' . esc_url( $url ) . '">' . esc_html( nlfh_headline( $h ) ) . '</a></h2>'
		. '<span class="nlfh-hot-f">' . esc_html( nlfh_facts( $h ) ) . '</span>';
	$o .= (int) $h['asking'] > 0 ? nlfh_vote_html( $tid, (int) $h['asking'], nlfh_my_vote( $tid ), $author )
		: '<a class="nlfh-btn nlfh-btn-sea nlfh-wide" href="' . esc_url( $url . '#nlf-reply-body' ) . '">כמה הייתם נותנים עליה? להעריך את המחיר</a>';
	$line = nlfh_stats_line( $votes, (int) $t['reply_count'], nlfh_pros_count( $tid ) );
	if ( '' !== $line ) { $o .= '<span class="nlfh-hot-s">' . esc_html( $line ) . '</span>'; }
	return $o . nlfh_invite_html( true ) . '</div></section>';
}

// HOOK nlf_home_after_start (5, before the video room band at 10 and the leaders at 20): part א, or part ד's invitation
add_filter( 'nlf_home_after_start', function ( $html ) {
	$a = function_exists( 'nlf_filter_args' ) ? nlf_filter_args() : array();
	if ( (int) ( $a['pg'] ?? 1 ) > 1 ) { return $html; }
	nlfh_install();
	if ( ! nlfh_ready() ) { return $html; }
	$id = nlfh_hot_id();
	$t  = $id ? nlf_topic( $id ) : null;
	$h  = $t && 'live' === $t['status'] ? nlfh_home( $id ) : null;
	return $html . ( $h ? nlfh_card_html( $t, $h ) : nlfh_invite_html() );
}, 5, 1 );

/** the sheet of part ד */
function nlfh_sheet_html() {
	$opt = '<option value="">בחרו עיר</option>';
	foreach ( array_keys( nlfh_cities() ) as $c ) { $opt .= '<option value="' . esc_attr( $c ) . '" data-code="' . (int) nlfh_city_code( $c ) . '">' . esc_html( $c ) . '</option>'; }
	$opt .= '<option value="other">עיר אחרת</option>';
	$rooms = '<option value="">בחרו</option>';
	for ( $r = 1.0; $r <= 12.0; $r += 0.5 ) { $rooms .= '<option value="' . esc_attr( nlfh_rooms_text( $r ) ) . '">' . esc_html( nlfh_rooms_text( $r ) ) . '</option>'; }
	$chips = function ( $name, $list ) {
		$o = '';
		foreach ( $list as $k => $l ) { $o .= '<button type="button" class="nlfh-chipbtn" data-nlfh-chip="' . esc_attr( $name ) . '" data-v="' . esc_attr( $k ) . '" aria-pressed="false">' . esc_html( $l[0] ) . '</button>'; }
		return $o;
	};
	return '<dialog class="nlf nlf-sheet nlfh-sheet" id="nlfh-compose" dir="rtl" aria-labelledby="nlfh-c-h">'
		. '<div class="nlf-sheet-h"><button type="button" class="nlf-ico" data-nlf-close aria-label="סגירה">' . nlf_svg( 'close' ) . '</button><h2 class="nlf-h2" id="nlfh-c-h">כמה הדירה שלכם שווה? תשאלו את הפורום</h2></div>'
		. '<form class="nlf-form nlfh-form" data-nlfh-form data-nlfmd-compose novalidate>'
		. '<div class="nlf-grid2">'
		. '<div class="nlf-field"><label for="nlfh-city">עיר</label><select id="nlfh-city" name="city" required>' . $opt . '</select></div>'
		. '<div class="nlf-field" data-nlfh-nbhd hidden><label for="nlfh-nbhd">שכונה (לא חובה)</label><select id="nlfh-nbhd" name="nbhd"><option value="">בחרו שכונה</option></select></div>'
		. '<div class="nlf-field" data-nlfh-other hidden><label for="nlfh-city2">שם העיר</label><input id="nlfh-city2" name="city_other" type="text" maxlength="40" autocomplete="address-level2"></div>'
		. '<div class="nlf-field"><label for="nlfh-street">רחוב, בלי מספר</label><input id="nlfh-street" name="street" type="text" maxlength="40" autocomplete="off" aria-describedby="nlfh-street-n"></div>'
		. '<div class="nlf-field"><label for="nlfh-rooms">חדרים</label><select id="nlfh-rooms" name="rooms" required>' . $rooms . '</select></div>'
		. '<div class="nlf-field"><label for="nlfh-sqm">מ"ר</label><input id="nlfh-sqm" name="sqm" type="text" inputmode="numeric" maxlength="4" autocomplete="off"></div>'
		. '<div class="nlf-field"><label for="nlfh-floor">קומה</label><input id="nlfh-floor" name="floor" type="text" inputmode="numeric" maxlength="3" autocomplete="off"></div>'
		. '<div class="nlf-field"><label for="nlfh-floors">מתוך קומות</label><input id="nlfh-floors" name="floors" type="text" inputmode="numeric" maxlength="2" autocomplete="off"></div>'
		. '</div>'
		. '<p class="nlfh-note" id="nlfh-street-n">בלי מספר בית: מספיק שם הרחוב.</p>'
		. '<div class="nlf-field"><label for="nlfh-ask">מחיר מבוקש (לא חובה)</label><input id="nlfh-ask" name="asking" type="text" inputmode="numeric" maxlength="14" autocomplete="off" placeholder="₪"></div>'
		. '<fieldset class="nlfh-chips"><legend>הדירה</legend>' . $chips( 'state', nlfh_states() ) . '</fieldset>'
		. '<fieldset class="nlfh-chips"><legend>אתם</legend>' . $chips( 'intent', nlfh_intents() ) . '</fieldset>'
		. '<div class="nlf-field"><label for="nlfh-body">מה תרצו לשאול? (לא חובה)</label><textarea id="nlfh-body" name="body" rows="3" maxlength="4000" placeholder="למשל: שווה לבקש יותר בגלל המרפסת?"></textarea></div>'
		. nlf_trap()
		. '<button type="submit" class="nlf-btn nlf-btn-hot nlf-btn-big">להציג לפורום</button>'
		. '<p class="nlfh-note">המיקום יוסר מהתמונות. מי שרוצה לפנות אליכם כותב דרך הפורום, והטלפון שלכם לא מוצג.</p>'
		. '<p class="nlf-msg" role="status" aria-live="polite"></p>'
		. '</form></dialog>';
}

/* =========================================================================================================
 * 6. The topic page's head: og:image = the first picture (Yoast prints the site's default picture there today)
 * ======================================================================================================= */

/** the first shown picture of the home discussion this page renders, or null */
function nlfh_og_photo() {
	static $p = false;
	if ( false !== $p ) { return $p; }
	$p = null;
	if ( 'topic' !== nlf_rendering() || empty( $GLOBALS['nlf_topic'] ) || 'home' !== (string) $GLOBALS['nlf_topic']['kind'] || 'live' !== (string) $GLOBALS['nlf_topic']['status'] ) { return $p; }
	$pics = nlfh_photos( (int) $GLOBALS['nlf_topic']['id'] );
	if ( $pics ) { $p = $pics[0]; }
	return $p;
}

/* Yoast's og:image presenter is taken off only on a home discussion that has a picture; this module prints the picture instead
   (before Yoast's block, at priority 0, so it comes first even on a Yoast without the presenters filter) */
add_filter( 'wpseo_frontend_presenters', function ( $presenters ) {
	if ( ! is_array( $presenters ) || ! nlfh_og_photo() ) { return $presenters; }
	return array_values( array_filter( $presenters, function ( $x ) { return ! ( is_object( $x ) && 'Yoast\WP\SEO\Presenters\Open_Graph\Image_Presenter' === get_class( $x ) ); } ) );
}, 20 );

add_action( 'wp_head', function () {
	$p = nlfh_og_photo();
	if ( ! $p ) { return; }
	if ( ! defined( 'WPSEO_VERSION' ) ) { echo '<meta property="og:title" content="' . esc_attr( (string) $GLOBALS['nlf_topic']['title'] ) . '">' . "\n"; } // Yoast prints the title itself
	echo '<meta property="og:image" content="' . esc_url( nlfmd_url( (string) $p['path'] ) ) . '">' . "\n"
		. '<meta property="og:image:width" content="' . (int) $p['w'] . '">' . "\n" . '<meta property="og:image:height" content="' . (int) $p['h'] . '">' . "\n"
		. '<meta property="og:image:type" content="image/jpeg">' . "\n";
}, 0 );

/* =========================================================================================================
 * 7. Assets (forum pages only), the sheet, and the test kit's clean
 * ======================================================================================================= */

/** the page script's numbers: the discussion (when it is a home discussion), whether estimates are open, whether I wrote it */
function nlfh_config() {
	$t  = 'topic' === nlf_rendering() && ! empty( $GLOBALS['nlf_topic'] ) ? $GLOBALS['nlf_topic'] : null;
	$me = nlf_me();
	$home = $t && 'home' === (string) $t['kind'];
	return array(
		'rest'   => esc_url_raw( rest_url( 'nadlan/v1/forum/' ) ),
		'topic'  => $home ? (int) $t['id'] : 0,
		'est'    => $home && 'live' === (string) $t['status'] && ! ( $me && (int) $me['id'] === (int) $t['member_id'] ) ? 1 : 0,
	);
}

add_action( 'wp_enqueue_scripts', function () {
	if ( ! function_exists( 'nlf_rendering' ) || '' === nlf_rendering() ) { return; } // the forum's own pages only
	nlfh_install();
	if ( ! nlfh_ready() ) { return; }
	$base = plugins_url( 'assets/proforum/', dirname( __FILE__ ) );
	$ver  = function_exists( 'nlf_ver' ) ? nlf_ver() : '1';
	wp_enqueue_style( 'nlf-home', $base . 'home.css', array( 'nlf' ), $ver );
	// after media.js: the answer form's nlfExtra() of the media module is wrapped, never replaced
	wp_enqueue_script( 'nlf-home', $base . 'home.js', wp_script_is( 'nlf-media', 'enqueued' ) ? array( 'nlf', 'nlf-media' ) : array( 'nlf' ), $ver, true );
	wp_add_inline_script( 'nlf-home', 'window.NLFH=' . nlf_json_script( nlfh_config() ) . ';', 'before' );
}, 36 );

add_action( 'wp_footer', function () {
	if ( ! function_exists( 'nlf_rendering' ) || '' === nlf_rendering() || ! nlfh_ready() ) { return; }
	echo nlfh_sheet_html(); // phpcs:ignore -- escaped inside
}, 6 ); // before the footer scripts: forum.js wires every dialog.nlf when it runs

/**
 * The test kit (scripts/project-stage/forum_testkit.py, `clean`): the apartment rows, votes and estimates of the discussions the
 * removed members opened, and the votes and estimates they gave anywhere. Rows are deleted. Returns the count.
 */
function nlfh_purge_members( array $ids, array $tids = array() ) {
	$ids  = array_values( array_filter( array_map( 'intval', $ids ) ) );
	$tids = array_values( array_filter( array_map( 'intval', $tids ) ) );
	if ( ! $ids || ! nlfh_ready() ) { return 0; }
	global $wpdb;
	$in   = implode( ',', $ids );
	$keys = array();
	foreach ( $ids as $id ) { $keys[] = "'" . nlfh_voter_key( $id, '', nlf_key() ) . "'"; } // hex only
	$n = (int) $wpdb->query( 'DELETE FROM ' . nlfh_t( 'estimates' ) . " WHERE member_id IN ($in)" . ( $tids ? ' OR topic_id IN (' . implode( ',', $tids ) . ')' : '' ) ); // phpcs:ignore -- integers only
	$n += (int) $wpdb->query( 'DELETE FROM ' . nlfh_t( 'votes' ) . ' WHERE voter_key IN (' . implode( ',', $keys ) . ')' . ( $tids ? ' OR topic_id IN (' . implode( ',', $tids ) . ')' : '' ) ); // phpcs:ignore -- hex and integers only
	if ( $tids ) { $n += (int) $wpdb->query( 'DELETE FROM ' . nlfh_t( 'homes' ) . ' WHERE topic_id IN (' . implode( ',', $tids ) . ')' ); } // phpcs:ignore -- integers only
	delete_transient( 'nlfh_hot' );
	return $n;
}
