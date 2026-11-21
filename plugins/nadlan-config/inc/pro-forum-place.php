<?php
/**
 * nad-lan professionals' forum: the forum inside a place or project page (19.11.2026, Claude Design board 24,
 * forum-design/project/PlaceEmbed.dc.html). Prefix nlfp2_ (PHP) and nlfpl- (classes); the prefix nlfp alone belongs to others.
 *
 *  א. At the END of a registered place page's content (after the article, the_content priority 90), only on that singular page
 *     and only while the forum's gate is open: the kicker, the live count of this week, the heading (owner-approved wording in
 *     the option nadlan_forum_place_headings), a one-line ask box that opens the forum's own compose sheet (#nlf-compose) with the
 *     title and the place, the 3 most recently active live discussions of the place, and "לכל השאלות על <label>" to
 *     /forum/?place=<key>. With no discussion yet: kicker, heading, ask box and "עוד אין שאלות. שאלו ראשונים." only.
 *     The forum's footer sheets print there through $GLOBALS['nlf_card_printed'] (as on a professional's card); this module
 *     loads forum.css / forum.js itself on the place page, so the heavier layers (social, rep, card, media, call) stay off it.
 *     The board's video room row is NOT built: a room "על <place>" needs a place room kind (its invite link would otherwise lead
 *     to /forum/, not to the place); the forum's topic-less room is the forum home's room.
 *  ב. In the forum: a discussion asked from the page carries the place (side table {prefix}nadlan_forum_place, one row per
 *     topic), the thread shows a chip with the place before the category tag and a line back to the place page, and
 *     /forum/?place=<key> lists only that place's discussions, with the chip "<label> ✕" at the top.
 *
 * Loaded by ONE line at the end of inc/pro-forum.php. Hooks this module fills (one-line hooks marked "HOOK (place module ...)"):
 *   nlf_filter_args, nlf_home_url_args, nlf_home_where_sql (inc/pro-forum.php), nlf_topic_meta_tags (inc/pro-forum-render.php).
 * Existing hooks it uses: nlf_post_check / nlf_post_created (the place of a new discussion; no new route), nlf_moderated,
 *   nlf_home_after_start (1), nlf_topic_after_body (1), nlf_kinds (30: no "דירה לדיון" in the sheet on a place page).
 * Rules: no new address (only a query value on /forum/), no crawl or index directives, no redirects, no JSON-LD on the place page,
 *   nothing on any page other than the registered ones, the block sits after the article and pushes nothing above it.
 *   No long dashes in this file.
 */

if ( ! defined( 'ABSPATH' ) && ! defined( 'NLFP2_PURE_ONLY' ) ) { exit; }
if ( defined( 'NLFP2_LOADED' ) ) { return; }
define( 'NLFP2_LOADED', true );
define( 'NLFP2_DB', '1' );

/* =========================================================================================================
 * 1. Pure functions (no WordPress). tests-local/pro-forum-place-test.php loads only this part (NLFP2_PURE_ONLY), after the
 *    forum's own pure part.
 * ======================================================================================================= */

/**
 * The registered places: key => label, page path, default heading, ask placeholder.
 * TO ADD A PLACE: one line in the list below, key => array( the name as it reads after "על", the page's path ). The key is latin,
 * lower case, at most 20 characters, and is never changed afterwards (discussions are tagged with it). Nothing else is needed:
 * the heading ("שאלות של קונים על <name>", Ben's wording of 21.11.2026), the ask line, the filter /forum/?place=<key> and the link
 * back all follow. A page that is not published or not found simply shows nothing.
 */
function nlfp2_places() {
	return array(
		'sde-dov'  => array( 'שדה דב', '/sde-dov/' ),
		'hamedina' => array( 'כיכר המדינה', '/projects/hamedina/' ),
	);
}

function nlfp2_registry() {
	$out = array();
	foreach ( nlfp2_places() as $k => $x ) {
		$out[ $k ] = array( 'label' => $x[0], 'path' => $x[1], 'heading' => nlfp2_default_heading( $x[0] ), 'ask' => 'מה תרצו לשאול על ' . $x[0] . '?' );
	}
	return $out;
}

function nlfp2_default_heading( $label ) { return 'שאלות של קונים על ' . (string) $label; }

/** the defaults of the option nadlan_forum_place_headings: key => heading */
function nlfp2_default_headings() {
	$out = array();
	foreach ( nlfp2_registry() as $k => $p ) { $out[ $k ] = $p['heading']; }
	return $out;
}

function nlfp2_key_ok( $key ) { return is_string( $key ) && '' !== $key && isset( nlfp2_registry()[ $key ] ); }

/** a raw value (a form field, a query value) as a registered key, '' otherwise */
function nlfp2_valid( $raw ) {
	if ( ! is_scalar( $raw ) ) { return ''; }
	$k = strtolower( trim( (string) $raw ) );
	return nlfp2_key_ok( $k ) ? $k : '';
}

/** a path as compared: decoded, lower case, no query or fragment, one slash at each end, no double slashes */
function nlfp2_path_norm( $path ) {
	$p = (string) $path;
	$p = preg_replace( '/[?#].*$/s', '', $p );
	$p = strtolower( rawurldecode( (string) $p ) );
	$p = preg_replace( '~/+~', '/', '/' . trim( (string) $p, '/' ) . '/' );
	return (string) $p;
}

/** the key whose page path is this path, '' for any other page */
function nlfp2_key_for_path( $path ) {
	$n = nlfp2_path_norm( $path );
	if ( '/' === $n ) { return ''; }
	foreach ( nlfp2_registry() as $k => $p ) { if ( nlfp2_path_norm( $p['path'] ) === $n ) { return $k; } }
	return '';
}

/** the heading of a place: the option's text for that key when it is a usable string, else the default; '' for an unknown key */
function nlfp2_heading( $key, $opt ) {
	if ( ! nlfp2_key_ok( $key ) ) { return ''; }
	if ( is_array( $opt ) && isset( $opt[ $key ] ) && is_string( $opt[ $key ] ) ) {
		$h = trim( preg_replace( '/\s+/u', ' ', $opt[ $key ] ) );
		if ( '' !== $h && nlf_len( $h ) <= 120 ) { return $h; }
	}
	return nlfp2_registry()[ $key ]['heading'];
}

/** "N דיונים פעילים השבוע"; '' for zero (an empty count is omitted, never "0") */
function nlfp2_week_text( $n ) {
	$n = (int) $n;
	if ( $n < 1 ) { return ''; }
	return 1 === $n ? 'דיון אחד פעיל השבוע' : number_format( $n ) . ' דיונים פעילים השבוע';
}

/** the facts line of a row: "4 תשובות · לפני שעה" (past a week: $date), or "מחכה לתשובה ראשונה" */
function nlfp2_row_meta( $replies, $last_ts, $now, $date = '' ) {
	$n = (int) $replies;
	if ( $n < 1 ) { return 'מחכה לתשובה ראשונה'; }
	$ago = nlf_ago( (int) $last_ts, (int) $now );
	return implode( ' · ', array_filter( array( nlf_count_words( $n, 'תשובה אחת', 'תשובות' ), '' !== $ago ? $ago : (string) $date ) ) );
}

/** the tint of a row's count box (board 24): 3 answers and more raspberry, 1 to 2 sea, none grey */
function nlfp2_row_tint( $replies ) {
	$n = (int) $replies;
	if ( $n >= 3 ) { return array( '#FBE7EF', '#8A0F3D' ); }
	if ( $n >= 1 ) { return array( '#E6F0F4', '#1F4B5C' ); }
	return array( '#EEF2F4', '#3A4650' );
}

function nlfp2_all_text( $label ) { return 'לכל השאלות על ' . (string) $label; }

function nlfp2_back_text( $label ) { return 'כל המידע על ' . (string) $label . ': מחירים, פרויקטים ומפה'; }

function nlfp2_none_text() { return 'עוד אין שאלות. שאלו ראשונים.'; }

if ( defined( 'NLFP2_PURE_ONLY' ) ) { return; }

/* =========================================================================================================
 * 2. The table, the option, the place of this request
 * ======================================================================================================= */

function nlfp2_t() { global $wpdb; return $wpdb->prefix . 'nadlan_forum_place'; }

function nlfp2_ready() { return NLFP2_DB === (string) get_option( 'nadlan_forum_place_db' ); }

/** the table once per NLFP2_DB (never on every request), and the headings option with its defaults; a failure waits an hour */
function nlfp2_install() {
	if ( nlfp2_ready() || get_transient( 'nlfp2_install_wait' ) || ! function_exists( 'nlf_db_ready' ) || ! nlf_db_ready() ) { return; }
	global $wpdb;
	require_once ABSPATH . 'wp-admin/includes/upgrade.php';
	dbDelta( 'CREATE TABLE ' . nlfp2_t() . " (
		topic_id BIGINT UNSIGNED NOT NULL,
		place VARCHAR(20) NOT NULL DEFAULT '',
		PRIMARY KEY  (topic_id),
		KEY place (place)
	) " . $wpdb->get_charset_collate() . ';' );
	if ( nlfp2_t() !== (string) $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $wpdb->esc_like( nlfp2_t() ) ) ) ) {
		set_transient( 'nlfp2_install_wait', 1, HOUR_IN_SECONDS );
		return;
	}
	add_option( 'nadlan_forum_place_headings', nlfp2_default_headings(), '', false ); // the owner approves the wording; editable without code
	update_option( 'nadlan_forum_place_db', NLFP2_DB, true );
}
add_action( 'admin_init', 'nlfp2_install', 26 );

/** a place with its heading resolved from the option, or null */
function nlfp2_place( $key ) {
	if ( ! nlfp2_key_ok( $key ) ) { return null; }
	$p = nlfp2_registry()[ $key ];
	$p['key']     = $key;
	$p['heading'] = nlfp2_heading( $key, get_option( 'nadlan_forum_place_headings', nlfp2_default_headings() ) );
	return $p;
}

/** the registered key of the singular page this request shows, '' for every other request (decided after 'wp') */
function nlfp2_page_key() {
	static $k = null;
	if ( null !== $k ) { return $k; }
	if ( ! did_action( 'wp' ) ) { return ''; }
	$k = '';
	if ( is_admin() || ! is_singular() || ( function_exists( 'nlf_rendering' ) && '' !== nlf_rendering() ) ) { return $k; }
	$id = (int) get_queried_object_id();
	if ( $id <= 0 || 'publish' !== get_post_status( $id ) ) { return $k; }
	$path = (string) wp_parse_url( (string) get_permalink( $id ), PHP_URL_PATH );
	$base = rtrim( (string) wp_parse_url( home_url( '/' ), PHP_URL_PATH ), '/' ); // a site in a sub-folder
	if ( '' !== $base && 0 === strpos( $path, $base . '/' ) ) { $path = substr( $path, strlen( $base ) ); }
	$k = nlfp2_key_for_path( $path );
	return $k;
}

/** this request shows the block: a registered page and the forum's gate open */
function nlfp2_on_page() { return '' !== nlfp2_page_key() && function_exists( 'nlf_gate_open' ) && nlf_gate_open(); }

/** the forum list's place filter (?place=), '' when none or not registered */
function nlfp2_filter_key() {
	return isset( $_GET['place'] ) ? nlfp2_valid( sanitize_key( wp_unslash( $_GET['place'] ) ) ) : ''; // phpcs:ignore -- a list filter, checked against the registry
}

/** the place of a discussion, '' for none */
function nlfp2_topic_place( $tid ) {
	static $memo = array();
	$tid = (int) $tid;
	if ( $tid <= 0 || ! nlfp2_ready() ) { return ''; }
	if ( array_key_exists( $tid, $memo ) ) { return $memo[ $tid ]; }
	global $wpdb;
	return $memo[ $tid ] = nlfp2_valid( (string) $wpdb->get_var( $wpdb->prepare( 'SELECT place FROM ' . nlfp2_t() . ' WHERE topic_id = %d', $tid ) ) );
}

/** the live discussions of a place, most recently active first */
function nlfp2_recent( $key, $n = 3 ) {
	global $wpdb;
	return (array) $wpdb->get_results( $wpdb->prepare( 'SELECT t.id, t.title, t.reply_count, t.last_at FROM ' . nlf_t( 'topics' ) . ' t JOIN ' . nlfp2_t() . " p ON p.topic_id = t.id
		WHERE p.place = %s AND t.status = 'live' ORDER BY t.last_at DESC LIMIT %d", $key, (int) $n ), ARRAY_A );
}

/** live discussions of a place with activity in the last 7 days */
function nlfp2_week_count( $key ) {
	global $wpdb;
	return (int) $wpdb->get_var( $wpdb->prepare( 'SELECT COUNT(*) FROM ' . nlf_t( 'topics' ) . ' t JOIN ' . nlfp2_t() . " p ON p.topic_id = t.id
		WHERE p.place = %s AND t.status = 'live' AND t.last_at >= %s", $key, gmdate( 'Y-m-d H:i:s', time() - 7 * DAY_IN_SECONDS ) ) );
}

/** a cached copy of the place page is renewed when its discussions change (no-op without LiteSpeed Cache) */
function nlfp2_purge_page( $key ) {
	$p = nlfp2_place( $key );
	if ( $p ) { do_action( 'litespeed_purge_url', home_url( $p['path'] ) ); }
}

/* =========================================================================================================
 * 3. A new discussion carries its place (the forum's own topic route; no new route)
 * ======================================================================================================= */

// HOOK nlf_post_check (inc/pro-forum.php, the topic route, before the insert): the table is ready before the row is written.
// A place that is not registered is ignored (the discussion is published without a place), never an error.
add_filter( 'nlf_post_check', function ( $err, $type, $m = null, $q = null, $t = null ) {
	if ( '' === (string) $err && 'topic' === $type && $q instanceof WP_REST_Request && '' !== nlfp2_valid( $q->get_param( 'place' ) ) ) { nlfp2_install(); }
	return $err;
}, 30, 5 );

// HOOK nlf_post_created (inc/pro-forum.php, after the insert): the place row of a new discussion; an answer renews the place page
add_action( 'nlf_post_created', function ( $type, $id, $m, $q, $status, $tid ) {
	if ( ! nlfp2_ready() ) { return; }
	if ( 'topic' === $type && $q instanceof WP_REST_Request ) {
		$key = nlfp2_valid( $q->get_param( 'place' ) );
		if ( '' === $key ) { return; }
		global $wpdb;
		$wpdb->replace( nlfp2_t(), array( 'topic_id' => (int) $id, 'place' => $key ), array( '%d', '%s' ) );
		if ( 'live' === $status ) { nlfp2_purge_page( $key ); }
		return;
	}
	if ( 'reply' === $type && 'live' === $status ) {
		$key = nlfp2_topic_place( (int) $tid );
		if ( '' !== $key ) { nlfp2_purge_page( $key ); }
	}
}, 30, 6 );

// HOOK nlf_moderated (inc/pro-forum.php, nlf_moderate): a discussion of a place goes live, hides or goes, or an answer in one does
add_action( 'nlf_moderated', function ( $type, $id ) {
	if ( ! nlfp2_ready() ) { return; }
	$tid = (int) $id;
	if ( 'reply' === $type ) { $r = nlf_reply( (int) $id ); $tid = $r ? (int) $r['topic_id'] : 0; }
	$key = nlfp2_topic_place( $tid );
	if ( '' !== $key ) { nlfp2_purge_page( $key ); }
}, 30, 2 );

// HOOK nlf_kinds (inc/pro-forum.php): the apartment sheet lives on the forum's pages only, so its kind is not offered on a place page
add_filter( 'nlf_kinds', function ( $k ) {
	if ( did_action( 'wp' ) && '' !== nlfp2_page_key() ) { unset( $k['home'] ); }
	return $k;
}, 30 );

/* =========================================================================================================
 * 4. The forum list: /forum/?place=<key>
 * ======================================================================================================= */

// HOOK nlf_filter_args (inc/pro-forum.php): the list's place filter, '' or a registered key
add_filter( 'nlf_filter_args', function ( $a ) {
	$a = (array) $a;
	$a['place'] = nlfp2_filter_key();
	return $a;
} );

// HOOK nlf_home_where_sql (inc/pro-forum.php, nlf_render_home): only the place's discussions (a prepared condition on topics.id)
add_filter( 'nlf_home_where_sql', function ( $sql, $a ) {
	$key = is_array( $a ) ? (string) ( $a['place'] ?? '' ) : '';
	if ( '' === $key ) { return $sql; }
	nlfp2_install();
	if ( ! nlfp2_ready() ) { return '1 = 0'; } // no table yet: no discussion has a place
	global $wpdb;
	return $wpdb->prepare( 'id IN (SELECT topic_id FROM ' . nlfp2_t() . ' WHERE place = %s)', $key );
}, 10, 2 );

// HOOK nlf_home_url_args (inc/pro-forum.php, nlf_home_url): on the filtered list, its sort, topic and page links keep the place;
// a link that names 'place' itself (the chip's ✕, with '') decides for itself
add_filter( 'nlf_home_url_args', function ( $args ) {
	$args = (array) $args;
	if ( array_key_exists( 'place', $args ) || ! function_exists( 'nlf_rendering' ) || 'home' !== nlf_rendering() ) { return $args; }
	$key = nlfp2_filter_key();
	if ( '' !== $key ) { $args['place'] = $key; }
	return $args;
} );

// HOOK nlf_home_after_start (1, before the apartment card at 5 and the video room band at 10): the chip "<label> ✕"
add_filter( 'nlf_home_after_start', function ( $html ) {
	$p = nlfp2_place( nlfp2_filter_key() );
	if ( ! $p ) { return $html; }
	$a   = nlf_filter_args();
	$off = nlf_home_url( array( 'c' => $a['c'], 'v' => $a['v'], 'place' => '' ) );
	return $html . '<div class="nlfpl-filter" dir="rtl"><a class="nlfpl-fchip" href="' . esc_url( $off ) . '" aria-label="' . esc_attr( 'הסרת הסינון: ' . $p['label'] ) . '">'
		. esc_html( $p['label'] ) . ' <span aria-hidden="true">✕</span></a></div>';
}, 1, 1 );

/* =========================================================================================================
 * 5. The thread: the place chip before the category tag, the line back to the place page
 * ======================================================================================================= */

// HOOK nlf_topic_meta_tags (inc/pro-forum-render.php, nlf_render_topic): the chip
add_filter( 'nlf_topic_meta_tags', function ( $html, $t ) {
	$p = is_array( $t ) ? nlfp2_place( nlfp2_topic_place( (int) $t['id'] ) ) : null;
	return $p ? $html . '<span class="nlfpl-chip">' . esc_html( $p['label'] ) . '</span>' : $html;
}, 10, 2 );

// HOOK nlf_topic_after_body (1: before the pictures at 5, the social chips at 10, the apartment at 12, the video row at 20)
add_filter( 'nlf_topic_after_body', function ( $html, $t ) {
	$p = is_array( $t ) ? nlfp2_place( nlfp2_topic_place( (int) $t['id'] ) ) : null;
	if ( ! $p ) { return $html; }
	return $html . '<p class="nlfpl-backp"><a class="nlfpl-back" href="' . esc_url( home_url( $p['path'] ) ) . '">' . esc_html( nlfp2_back_text( $p['label'] ) ) . '</a></p>';
}, 1, 2 );

/* =========================================================================================================
 * 6. The block at the end of the place page (board 24 part א)
 * ======================================================================================================= */

/** one discussion as a row: the answers in a tinted box, the title, one facts line */
function nlfp2_row_html( array $t ) {
	$n    = (int) $t['reply_count'];
	$ts   = nlf_ts( $t['last_at'] );
	$meta = nlfp2_row_meta( $n, $ts, time(), $ts > 0 ? wp_date( 'j.n.Y', $ts ) : '' );
	return '<a class="nlfpl-row" href="' . esc_url( home_url( '/forum/' . (int) $t['id'] . '/' ) ) . '"><span class="nlfpl-num" style="' . nlf_tint_style( nlfp2_row_tint( $n ) ) . '" aria-hidden="true">' . $n . '</span>'
		. '<span class="nlfpl-rt"><span class="nlfpl-rtitle">' . esc_html( $t['title'] ) . '</span><span class="nlfpl-rmeta">' . esc_html( $meta ) . '</span></span></a>';
}

/** the whole block of a place; '' when the place is unknown */
function nlfp2_embed_html( $key ) {
	$p = nlfp2_place( $key );
	if ( ! $p ) { return ''; }
	$rows = nlfp2_ready() ? nlfp2_recent( $key, 3 ) : array();
	$week = $rows ? nlfp2_week_text( nlfp2_week_count( $key ) ) : '';
	$uid  = 'nlfpl-' . $key;
	$h  = '<section class="nlf nlf-win nlfpl" dir="rtl" aria-labelledby="' . esc_attr( $uid ) . '-h" data-pro="0" data-pro-name="" data-cat="general" data-nlfpl="' . esc_attr( $key ) . '"><div class="nlfpl-box">';
	$h .= '<div class="nlfpl-top"><span class="nlfpl-kick">מהפורום של נדל"ן</span>'
		. ( '' !== $week ? '<span class="nlfpl-live"><i aria-hidden="true"></i>' . esc_html( $week ) . '</span>' : '' ) . '</div>';
	$h .= '<h2 class="nlfpl-h" id="' . esc_attr( $uid ) . '-h">' . esc_html( $p['heading'] ) . '</h2>';
	// data-nlf-ask: forum.js opens its own compose sheet with this title (a guest is asked to enter when he publishes)
	$h .= '<form class="nlfpl-ask" data-nlf-ask novalidate><label class="nlfpl-sr" for="' . esc_attr( $uid ) . '-q">' . esc_html( $p['ask'] ) . '</label>'
		. '<div class="nlfpl-askrow"><input id="' . esc_attr( $uid ) . '-q" type="text" name="q" maxlength="140" autocomplete="off" placeholder="' . esc_attr( $p['ask'] ) . '">'
		. '<button type="submit">לשאול</button></div></form>';
	if ( $rows ) {
		$h .= '<div class="nlfpl-list">';
		foreach ( $rows as $t ) { $h .= nlfp2_row_html( $t ); }
		$h .= '</div><a class="nlfpl-all" href="' . esc_url( add_query_arg( 'place', $key, home_url( '/forum/' ) ) ) . '">' . esc_html( nlfp2_all_text( $p['label'] ) ) . '</a>';
	} else {
		$h .= '<p class="nlfpl-none">' . esc_html( nlfp2_none_text() ) . '</p>';
	}
	return $h . '</div></section>';
}

/* after the article: late (90), once, only in the main loop of the registered page itself, only with the gate open */
add_filter( 'the_content', function ( $content ) {
	static $done = false;
	if ( $done || is_admin() || ! is_main_query() || ! in_the_loop() || ! nlfp2_on_page() ) { return $content; }
	if ( (int) get_the_ID() !== (int) get_queried_object_id() || post_password_required() ) { return $content; }
	nlf_install();
	if ( ! nlf_db_ready() ) { return $content; }
	nlfp2_install();
	$done = true;
	$GLOBALS['nlf_card_printed'] = true; // the forum's footer sheets (compose, entry, report) print on this page (inc/pro-forum-render.php)
	return $content . nlfp2_embed_html( nlfp2_page_key() );
}, 90 );

/* LiteSpeed: the gate cookie and the session vary the place page as they vary the forum's own pages (core, section 2) */
add_filter( 'litespeed_vary_curr_cookies', function ( $list ) {
	$list = (array) $list;
	if ( did_action( 'wp' ) && '' !== nlfp2_page_key() ) { $list[] = 'nlf_gate'; $list[] = 'nlf_s'; }
	return array_values( array_unique( $list ) );
} );

/* =========================================================================================================
 * 7. Assets
 * ======================================================================================================= */

/** the page script's words: the place this page tags a new discussion with */
function nlfp2_config( $key ) {
	$p = nlfp2_place( $key );
	return array( 'place' => $p ? $key : '', 'label' => $p ? $p['label'] : '' );
}

add_action( 'wp_enqueue_scripts', function () {
	if ( ! function_exists( 'nlf_rendering' ) ) { return; }
	$base = plugins_url( 'assets/proforum/', dirname( __FILE__ ) );
	$ver  = nlf_ver();
	$view = nlf_rendering();
	if ( '' !== $view ) { // the forum's own pages: the filtered list, or a discussion that has a place
		$key = 'home' === $view ? nlfp2_filter_key() : ( 'topic' === $view && ! empty( $GLOBALS['nlf_topic'] ) ? nlfp2_topic_place( (int) $GLOBALS['nlf_topic']['id'] ) : '' );
		if ( '' === $key ) { return; }
		wp_enqueue_style( 'nlf-place', $base . 'place.css', array( 'nlf' ), $ver );
		if ( 'home' === $view ) { // a discussion written from the filtered list is tagged too (the sheet says so, one press undoes it)
			wp_enqueue_script( 'nlf-place', $base . 'place.js', wp_script_is( 'nlf-media', 'enqueued' ) ? array( 'nlf', 'nlf-media' ) : array( 'nlf' ), $ver, true );
			wp_add_inline_script( 'nlf-place', 'window.NLFPL=' . nlf_json_script( nlfp2_config( $key ) ) . ';', 'before' );
		}
		return;
	}
	if ( ! nlfp2_on_page() ) { return; }
	// the place page: the forum's own style and script (as inc/pro-forum.php section 12 loads them on a forum surface), then ours
	if ( ! wp_style_is( 'nlf', 'enqueued' ) ) {
		wp_enqueue_style( 'nlf-fonts', 'https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Rubik:wght@500;700;800&display=swap', array(), null );
		wp_enqueue_style( 'nlf', $base . 'forum.css', array(), $ver );
	}
	if ( ! wp_script_is( 'nlf', 'enqueued' ) ) {
		wp_enqueue_script( 'nlf', $base . 'forum.js', array(), $ver, true );
		wp_add_inline_script( 'nlf', 'window.NLF=' . nlf_json_script( array(
			'rest'    => esc_url_raw( rest_url( 'nadlan/v1/forum/' ) ),
			'wpnonce' => is_user_logged_in() ? wp_create_nonce( 'wp_rest' ) : '',
			'home'    => home_url( '/forum/' ),
		) ) . ';', 'before' );
	}
	wp_enqueue_style( 'nlf-place', $base . 'place.css', array( 'nlf' ), $ver );
	wp_enqueue_script( 'nlf-place', $base . 'place.js', array( 'nlf' ), $ver, true );
	wp_add_inline_script( 'nlf-place', 'window.NLFPL=' . nlf_json_script( nlfp2_config( nlfp2_page_key() ) ) . ';', 'before' );
}, 37 );

/**
 * The test kit (scripts/project-stage/forum_testkit.py, `clean`): the place rows of the discussions the removed members opened.
 * Rows are deleted. Returns the count.
 */
function nlfp2_purge_topics( array $tids ) {
	$tids = array_values( array_filter( array_map( 'intval', $tids ) ) );
	if ( ! $tids || ! nlfp2_ready() ) { return 0; }
	global $wpdb;
	return (int) $wpdb->query( 'DELETE FROM ' . nlfp2_t() . ' WHERE topic_id IN (' . implode( ',', $tids ) . ')' ); // phpcs:ignore -- integers only
}
