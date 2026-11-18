<?php
/**
 * nad-lan professionals' forum: the chat inside a video room (18.11.2026, Claude Design board 22 "צ'אט בתוך חדר הווידאו",
 * forum-design/project/VideoChat.dc.html, parts א to ג; part ד is the owner's comparison table, not UI).
 *
 * Loaded by ONE line at the end of inc/pro-forum.php, after the media module:
 *   if ( file_exists( __DIR__ . '/pro-forum-chat.php' ) ) { require_once __DIR__ . '/pro-forum-chat.php'; }
 * It uses the call module (nlfc_member, nlfc_room_get, nlfc_room_put, nlfc_can_join, nlfc_room_max, nlfc_ctx, nlfc_rl, nlfc_rl_peek,
 * nlfc_rl_hit, nlfc_ok), the forum (nlf_text_norm, nlf_text_rule_error, nlf_members, nlf_author, nlf_post_limits, nlf_first_status,
 * nlf_on_reply_live, nlf_mail_admin_pending, nlf_write_counted, nlf_report_reasons) and, when present, the media module
 * (nlfmd_rows, nlfmd_public, nlfmd_gone_rows, nlfmd_avatar_url) and the reputation module (nlfr_stats, nlfr_stars_text). It edits no
 * other file; every route answers 400 when the call module is not loaded.
 *
 * Table {prefix}nlf_chat (own version option nadlan_forum_chat_db): one row per message of a room, body at most 1000 characters,
 * one file (media_id, a row of the media module set to status 'chat' so the media module's own daily clean-up leaves it), pinned,
 * reactions as JSON {"useful":[member ids],"thanks":[member ids]}, attached (the host put it into the discussion), created_at.
 * Rows go after 7 days (daily WP-Cron nlfch_gc) unless attached; their files go with them.
 *
 * REST (nadlan/v1/forum/chat..., hidden from the index, every error HTTP 400). Only a member who is IN the room (nlfc_can_join
 * answers '' and the member is on the room's list, i.e. he came in) may read or write:
 *   GET  chat          {room}                    -> {rows, pinned, host, me}      the history (last 200)
 *   POST chat/send     {room, body, media?}      -> {row}                         one message (30 a minute, 400 a day per member)
 *   POST chat/react    {room, id, kind}          -> {id, reacts, mine}            "מועיל" or "תודה", one per person per message
 *   POST chat/pin      {room, id, on}            -> {pinned}                      the host pins one message
 *   POST chat/delete   {room, id}                -> {id}                          the author, or the host, deletes
 *   POST chat/report   {room, id, reason?}       -> {message}                     the forum's flags table, target_type 'chat'
 *   GET  chat/summary  {room}                    -> {can, title, pinned, media, rest}   the host's end-of-call sheet (part ג)
 *   POST chat/attach   {room, pin, media, rest}  -> {id, url, status, message}    ONE answer "מה סוכם בשיחה" on the discussion
 * Live delivery is the page's: after the server saved a message, call.js publishes the saved row on the LiveKit data topic 'chat'.
 * No redirects, no robots changes, no long dashes in this file.
 */

if ( ! defined( 'ABSPATH' ) && ! defined( 'NLFCH_PURE_ONLY' ) ) { exit; }
if ( defined( 'NLFCH_LOADED' ) ) { return; }
define( 'NLFCH_LOADED', true );
define( 'NLFCH_DB', '1' );

/* =========================================================================================================
 * 1. Pure functions (no WordPress). tests-local/pro-forum-chat-test.php loads only this part (NLFCH_PURE_ONLY), after the
 *    forum's own pure part.
 * ======================================================================================================= */

/** every number of this layer in one place */
function nlfch_limits() {
	return array(
		'body'   => 1000,  // characters in one message
		'minute' => 30,    // messages a minute per member
		'day'    => 400,   // messages a day per member
		'keep'   => 7,     // days a message stays in the room when it was not attached to the discussion
		'list'   => 200,   // messages the history returns
		'files'  => 10,    // files on the one answer "מה סוכם בשיחה" (the media module's limit for an answer)
		'sum'    => 3900,  // characters of that answer (the forum allows 4,000)
		'hide'   => 3,     // reports from different members that take a message off
	);
}

/** the two word reactions under a message (board 22 part ב), key => word */
function nlfch_reacts() { return array( 'useful' => 'מועיל', 'thanks' => 'תודה' ); }

/** a message as it is kept: the forum's text rule (no control or bidi characters, at most one empty line), trimmed */
function nlfch_body_clean( $s ) {
	if ( function_exists( 'nlf_text_norm' ) ) { return nlf_text_norm( (string) $s ); }
	return trim( (string) preg_replace( '/[\x00-\x09\x0B-\x1F\x7F]/u', ' ', (string) $s ) );
}

function nlfch_len( $s ) { return function_exists( 'mb_strlen' ) ? mb_strlen( (string) $s, 'UTF-8' ) : strlen( (string) $s ); }

/** '' when the message may go, else the Hebrew message. A message is text, a file, or both; never longer than the limit (refused, not cut) */
function nlfch_body_error( $body, $has_media ) {
	$n = nlfch_len( $body );
	if ( $n < 1 && ! $has_media ) { return 'כתבו הודעה או צרפו קובץ.'; }
	if ( $n > nlfch_limits()['body'] ) { return 'ההודעה ארוכה מדי. עד 1,000 תווים.'; }
	return '';
}

/** links, mail addresses and phone numbers wait until a member has 2 approved posts: the forum's own rule, word for word */
function nlfch_rule_error( $body, $approved ) {
	if ( function_exists( 'nlf_text_rule_error' ) ) { return nlf_text_rule_error( $body, (int) $approved ); }
	return '';
}

/** the index of a fixed window (minutes for 60, UTC days for 86400) */
function nlfch_window( $now, $window ) { return (int) floor( (int) $now / max( 1, (int) $window ) ); }

/** '' when one more message may go, else the message. $minute and $day are what the member already sent in this window */
function nlfch_rate_error( $minute, $day ) {
	$l = nlfch_limits();
	if ( (int) $day >= $l['day'] ) { return 'שלחתם היום ' . $l['day'] . ' הודעות בצ\'אט. אפשר לכתוב שוב מחר.'; }
	if ( (int) $minute >= $l['minute'] ) { return 'שלחתם הרבה הודעות בדקה האחרונה. רגע, ונסו שוב.'; }
	return '';
}

/** the oldest moment a message not attached to the discussion stays (UTC, SQL format) */
function nlfch_cutoff( $now, $days = null ) {
	$days = null === $days ? nlfch_limits()['keep'] : (int) $days;
	return gmdate( 'Y-m-d H:i:s', (int) $now - max( 1, $days ) * 86400 );
}

/** a reaction key, or '' */
function nlfch_react_norm( $kind ) { $k = (string) $kind; return isset( nlfch_reacts()[ $k ] ) ? $k : ''; }

/** the stored reactions as array( key => list of member ids ), from JSON or an array; anything else counts as none */
function nlfch_reacts_read( $raw ) {
	$a   = is_array( $raw ) ? $raw : json_decode( (string) $raw, true );
	$out = array();
	foreach ( array_keys( nlfch_reacts() ) as $k ) {
		$ids     = is_array( $a ) && isset( $a[ $k ] ) && is_array( $a[ $k ] ) ? $a[ $k ] : array();
		$out[ $k ] = array_values( array_unique( array_filter( array_map( 'intval', $ids ), function ( $v ) { return $v > 0; } ) ) );
	}
	return $out;
}

/**
 * One reaction per person per message: pressing the word you gave takes it back, pressing the other word moves you there.
 * Returns the new map (array( key => ids )).
 */
function nlfch_reacts_toggle( $raw, $member, $kind ) {
	$map  = nlfch_reacts_read( $raw );
	$kind = nlfch_react_norm( $kind );
	$mid  = (int) $member;
	if ( '' === $kind || $mid <= 0 ) { return $map; }
	$had = in_array( $mid, $map[ $kind ], true );
	foreach ( $map as $k => $ids ) { $map[ $k ] = array_values( array_diff( $ids, array( $mid ) ) ); }
	if ( ! $had ) { $map[ $kind ][] = $mid; }
	return $map;
}

/** counts for everyone: array( useful => n, thanks => n ) */
function nlfch_reacts_counts( $raw ) {
	$out = array();
	foreach ( nlfch_reacts_read( $raw ) as $k => $ids ) { $out[ $k ] = count( $ids ); }
	return $out;
}

/** the word this member gave, or '' */
function nlfch_reacts_mine( $raw, $member ) {
	foreach ( nlfch_reacts_read( $raw ) as $k => $ids ) { if ( in_array( (int) $member, $ids, true ) ) { return $k; } }
	return '';
}

/** "תמונה אחת ותוכנית אחת", "3 תמונות", "2 תוכניות" ... ('' for none) */
function nlfch_media_label( $images, $pdfs ) {
	$i = (int) $images;
	$p = (int) $pdfs;
	$a = $i > 0 ? ( 1 === $i ? 'תמונה אחת' : $i . ' תמונות' ) : '';
	$b = $p > 0 ? ( 1 === $p ? 'תוכנית אחת' : $p . ' תוכניות' ) : '';
	if ( '' === $a ) { return $b; }
	if ( '' === $b ) { return $a; }
	return $a . ( preg_match( '/^\d/', $b ) ? ' ו-' : ' ו' ) . $b;
}

/** whole minutes of a call, at least one */
function nlfch_minutes( $t0, $now ) { return max( 1, (int) round( ( (int) $now - (int) $t0 ) / 60 ) ); }

/**
 * The room's messages split for the end-of-call sheet. $rows in their order, each: id, name, body, media_id, media_kind, pinned.
 * array( pin => the pinned row or null, media => rows with a picture or a plan, rest => every other row that has words )
 */
function nlfch_summary_parts( array $rows ) {
	$pin   = null;
	$media = array();
	$rest  = array();
	foreach ( $rows as $r ) {
		if ( null === $pin && ! empty( $r['pinned'] ) ) { $pin = $r; continue; }
		if ( '' !== trim( (string) ( $r['body'] ?? '' ) ) ) { $rest[] = $r; }
	}
	foreach ( $rows as $r ) {
		if ( (int) ( $r['media_id'] ?? 0 ) > 0 && in_array( (string) ( $r['media_kind'] ?? '' ), array( 'image', 'pdf' ), true ) ) { $media[] = $r; }
	}
	return array( 'pin' => $pin, 'media' => $media, 'rest' => $rest );
}

/**
 * What the host chose: array( items => list of array( name, text ) for the answer, media => rows whose file goes on it (at most
 * $max_files), ids => every chat row that is now part of the discussion ). The pinned message first, then the others in order.
 */
function nlfch_summary_choose( array $parts, $want_pin, $want_media, $want_rest, $max_files = null ) {
	$max   = null === $max_files ? nlfch_limits()['files'] : (int) $max_files;
	$items = array();
	$ids   = array();
	$pin   = $parts['pin'] ?? null;
	if ( $want_pin && $pin ) {
		if ( '' !== trim( (string) $pin['body'] ) ) { $items[] = array( 'name' => (string) $pin['name'], 'text' => (string) $pin['body'] ); }
		$ids[] = (int) $pin['id'];
	}
	if ( $want_rest ) {
		foreach ( (array) ( $parts['rest'] ?? array() ) as $r ) { $items[] = array( 'name' => (string) $r['name'], 'text' => (string) $r['body'] ); $ids[] = (int) $r['id']; }
	}
	$media = array();
	if ( $want_media ) {
		foreach ( (array) ( $parts['media'] ?? array() ) as $r ) {
			if ( count( $media ) >= $max ) { break; }
			$media[] = $r;
			$ids[]   = (int) $r['id'];
		}
	}
	return array( 'items' => $items, 'media' => $media, 'ids' => array_values( array_unique( $ids ) ) );
}

/**
 * The answer's text: the line "מה סוכם בשיחה", then one line "שם: טקסט" per chosen message (each message on one line). When the
 * whole would pass $max characters the last lines stay out and one line says how many.
 */
function nlfch_summary_text( array $items, $max = null ) {
	$max  = null === $max ? nlfch_limits()['sum'] : (int) $max;
	$head = 'מה סוכם בשיחה';
	$out  = $head;
	$n    = count( $items );
	foreach ( array_values( $items ) as $i => $it ) {
		$text = trim( (string) preg_replace( '/\s+/u', ' ', (string) ( $it['text'] ?? '' ) ) );
		$name = trim( (string) preg_replace( '/\s+/u', ' ', (string) ( $it['name'] ?? '' ) ) );
		if ( '' === $text ) { continue; }
		$line = ( '' !== $name ? $name . ': ' : '' ) . $text;
		$left = $n - $i;
		$tail = "\n" . ( 1 === $left ? 'ועוד הודעה אחת מהשיחה.' : 'ועוד ' . $left . ' הודעות מהשיחה.' );
		if ( nlfch_len( $out . "\n" . $line ) + ( $left > 1 ? nlfch_len( $tail ) : 0 ) > $max ) { return $out . $tail; }
		$out .= ( $head === $out ? "\n\n" : "\n" ) . $line;
	}
	return $out;
}

/** the Hebrew message of every refusal of this module (all answered as HTTP 400) */
function nlfch_msg( $code ) {
	$m = array(
		'off'      => 'הצ\'אט לא זמין כרגע.',
		'room'     => 'החדר הזה כבר נסגר.',
		'notin'    => 'הצ\'אט פתוח רק למי שנמצא בחדר.',
		'gone'     => 'ההודעה לא נמצאה.',
		'host'     => 'רק מי שפתח את החדר יכול לעשות את זה.',
		'own'      => 'אפשר למחוק רק הודעה שלכם.',
		'self'     => 'אי אפשר להגיב להודעה של עצמכם.',
		'media'    => 'הקובץ כבר לא זמין. צרפו אותו שוב.',
		'home'     => 'לחדר הזה אין דיון לצרף אליו.',
		'already'  => 'הסיכום כבר צורף לדיון.',
		'nothing'  => 'סמנו מה לצרף.',
		'topic'    => 'הדיון לא נמצא.',
		'rate'     => 'נסו שוב בעוד כמה דקות.',
		'reason'   => 'בחרו סיבה.',
	);
	return $m[ $code ] ?? 'משהו השתבש. נסו שוב.';
}

if ( defined( 'NLFCH_PURE_ONLY' ) ) { return; }

/* =========================================================================================================
 * 2. Switch, table, the room check
 * ======================================================================================================= */

/** on unless the owner sets option nadlan_forum_chat to '0', and only with the call module */
function nlfch_on() {
	return function_exists( 'nlfc_on' ) && nlfc_on() && function_exists( 'nlfc_member' ) && '0' !== (string) get_option( 'nadlan_forum_chat', '1' );
}

function nlfch_t() { global $wpdb; return $wpdb->prefix . 'nlf_chat'; }

function nlfch_ready() { return NLFCH_DB === (string) get_option( 'nadlan_forum_chat_db' ); }

/** the table once per NLFCH_DB; a failed attempt waits an hour */
function nlfch_install() {
	if ( nlfch_ready() || get_transient( 'nlfch_install_wait' ) ) { return; }
	global $wpdb;
	require_once ABSPATH . 'wp-admin/includes/upgrade.php';
	dbDelta( 'CREATE TABLE ' . nlfch_t() . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		room CHAR(12) NOT NULL DEFAULT '',
		member_id BIGINT UNSIGNED NOT NULL,
		body TEXT NOT NULL,
		media_id BIGINT UNSIGNED NULL,
		pinned TINYINT(1) NOT NULL DEFAULT 0,
		reactions TEXT NULL,
		attached TINYINT(1) NOT NULL DEFAULT 0,
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		KEY room_id (room,id),
		KEY member_id (member_id),
		KEY created_at (created_at)
	) " . $wpdb->get_charset_collate() . ';' );
	if ( nlfch_t() !== (string) $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $wpdb->esc_like( nlfch_t() ) ) ) ) {
		set_transient( 'nlfch_install_wait', 1, HOUR_IN_SECONDS );
		return;
	}
	update_option( 'nadlan_forum_chat_db', NLFCH_DB, true );
}
add_action( 'admin_init', 'nlfch_install', 25 );

function nlfch_err( $code, $msg = '' ) {
	if ( function_exists( 'nlf_nocache' ) ) { nlf_nocache(); }
	return new WP_Error( 'nlfch_' . $code, '' !== $msg ? $msg : nlfch_msg( $code ), array( 'status' => 400 ) );
}

/**
 * The member and his room, or a WP_Error 400: the call module's member check (gate, session, header nonce, status, same-site
 * headers for writes), the room still open, and the member IN it: nlfc_can_join() answers '' AND he is on its list.
 * array( m, r, room, host )
 */
function nlfch_ctx( WP_REST_Request $q, $write ) {
	if ( ! nlfch_on() ) { return nlfch_err( 'off' ); }
	$m = nlfc_member( $q, $write );
	if ( is_wp_error( $m ) ) { return $m; }
	nlfch_install();
	if ( ! nlfch_ready() ) { return nlfch_err( 'off' ); }
	$room = strtolower( (string) $q->get_param( 'room' ) );
	$r    = nlfc_room_get( $room );
	if ( ! $r ) { return nlfch_err( 'room' ); }
	$mid = (int) $m['id'];
	if ( '' !== nlfc_can_join( $r, $mid, nlfc_room_max( $r ) ) || ! isset( $r['ok'][ $mid ] ) ) { return nlfch_err( 'notin' ); }
	return array( 'm' => $m, 'r' => $r, 'room' => $room, 'host' => (int) $r['by'] === $mid );
}

/** one message of this room by id, or null */
function nlfch_row( $room, $id ) {
	global $wpdb;
	$row = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlfch_t() . ' WHERE id = %d AND room = %s', (int) $id, (string) $room ), ARRAY_A );
	return $row ? $row : null;
}

/** the files of chat rows that were never attached: gone with their rows (the media module deletes the files) */
function nlfch_drop_media( array $rows ) {
	$ids = array();
	foreach ( $rows as $r ) { if ( (int) ( $r['media_id'] ?? 0 ) > 0 ) { $ids[] = (int) $r['media_id']; } }
	if ( ! $ids || ! function_exists( 'nlfmd_rows' ) || ! function_exists( 'nlfmd_gone_rows' ) ) { return 0; }
	$gone = array();
	foreach ( nlfmd_rows( $ids ) as $mr ) { if ( 'chat' === (string) $mr['status'] && empty( $mr['topic_id'] ) && empty( $mr['reply_id'] ) ) { $gone[] = $mr; } }
	return nlfmd_gone_rows( $gone );
}

/** delete chat rows (with their reports and their never-attached files) */
function nlfch_delete_rows( array $rows ) {
	if ( ! $rows ) { return 0; }
	global $wpdb;
	nlfch_drop_media( $rows );
	$in = implode( ',', array_map( 'intval', array_column( $rows, 'id' ) ) );
	if ( function_exists( 'nlf_t' ) ) { $wpdb->query( 'DELETE FROM ' . nlf_t( 'flags' ) . " WHERE target_type = 'chat' AND target_id IN ($in)" ); } // phpcs:ignore -- integers only
	return (int) $wpdb->query( 'DELETE FROM ' . nlfch_t() . " WHERE id IN ($in)" ); // phpcs:ignore -- integers only
}

/**
 * Rows as the page draws them: who (name, label, stars, initials, tint, picture, LiveKit identity), time, text, file, reactions,
 * whether I may delete it. $r = the room (identities), $mid = me, $host = I opened the room.
 */
function nlfch_public( array $rows, array $r, $mid, $host ) {
	if ( ! $rows ) { return array(); }
	$mem   = nlf_members( array_column( $rows, 'member_id' ) );
	$stats = function_exists( 'nlfr_stats' ) ? nlfr_stats( array_keys( $mem ) ) : array();
	$files = function_exists( 'nlfmd_rows' ) ? nlfmd_rows( array_filter( array_map( 'intval', array_column( $rows, 'media_id' ) ) ) ) : array();
	$ok    = isset( $r['ok'] ) && is_array( $r['ok'] ) ? $r['ok'] : array();
	$faces = array();
	$out   = array();
	foreach ( $rows as $row ) {
		$aid = (int) $row['member_id'];
		if ( ! isset( $faces[ $aid ] ) ) {
			$a     = nlf_author( $mem[ $aid ] ?? null );
			$s     = $stats[ $aid ] ?? null;
			$stars = is_array( $s ) && empty( $s['excluded'] ) && isset( $s['level']['n'] ) && (int) $s['level']['n'] > 0 && function_exists( 'nlfr_stars_text' ) ? nlfr_stars_text( (int) $s['level']['n'] ) : '';
			$faces[ $aid ] = array( 'id' => $aid, 'name' => (string) $a['name'], 'label' => (string) $a['label'], 'stars' => $stars,
				'initials' => nlf_initials( $a['name'] ), 'bg' => (string) $a['tint'][0], 'fg' => (string) $a['tint'][1],
				'pic' => function_exists( 'nlfmd_avatar_url' ) ? (string) nlfmd_avatar_url( $aid ) : '', 'identity' => (string) ( $ok[ $aid ] ?? '' ) );
		}
		$ts   = function_exists( 'nlf_ts' ) ? nlf_ts( $row['created_at'] ) : strtotime( $row['created_at'] . ' UTC' );
		$file = null;
		$fr   = $files[ (int) $row['media_id'] ] ?? null;
		if ( $fr && 'gone' !== (string) $fr['status'] && in_array( (string) $fr['kind'], array( 'image', 'pdf' ), true ) && function_exists( 'nlfmd_public' ) ) { $file = nlfmd_public( $fr ); }
		$out[] = array( 'id' => (int) $row['id'], 'who' => $faces[ $aid ], 'mine' => $aid === (int) $mid ? 1 : 0, 'body' => (string) $row['body'], 'media' => $file,
			'pinned' => (int) $row['pinned'] ? 1 : 0, 'reacts' => nlfch_reacts_counts( $row['reactions'] ), 'my' => nlfch_reacts_mine( $row['reactions'], $mid ),
			'at' => (int) $ts, 'time' => function_exists( 'wp_date' ) ? (string) wp_date( 'H:i', (int) $ts ) : gmdate( 'H:i', (int) $ts ),
			'del' => ( $aid === (int) $mid || $host ) ? 1 : 0 );
	}
	return $out;
}

/** the room's rows in order, oldest first (at most the list limit, the newest ones) */
function nlfch_room_rows( $room ) {
	global $wpdb;
	$rows = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlfch_t() . ' WHERE room = %s ORDER BY id DESC LIMIT %d', (string) $room, nlfch_limits()['list'] ), ARRAY_A );
	return array_reverse( $rows );
}

/** the rows for the summary: id, name, body, media_id, media_kind, pinned, member_id */
function nlfch_summary_rows( $room ) {
	$rows  = nlfch_room_rows( $room );
	$mem   = nlf_members( array_column( $rows, 'member_id' ) );
	$files = function_exists( 'nlfmd_rows' ) ? nlfmd_rows( array_filter( array_map( 'intval', array_column( $rows, 'media_id' ) ) ) ) : array();
	$out   = array();
	foreach ( $rows as $row ) {
		$a  = nlf_author( $mem[ (int) $row['member_id'] ] ?? null );
		$fr = $files[ (int) $row['media_id'] ] ?? null;
		$ok = $fr && 'chat' === (string) $fr['status'] && empty( $fr['topic_id'] ) && empty( $fr['reply_id'] ) && (int) $fr['member_id'] === (int) $row['member_id'];
		$out[] = array( 'id' => (int) $row['id'], 'member_id' => (int) $row['member_id'], 'name' => (string) $a['name'], 'body' => (string) $row['body'],
			'media_id' => $ok ? (int) $row['media_id'] : 0, 'media_kind' => $ok ? (string) $fr['kind'] : '', 'pinned' => (int) $row['pinned'] );
	}
	return $out;
}

/* =========================================================================================================
 * 3. REST
 * ======================================================================================================= */

add_action( 'rest_api_init', function () {
	$reg = function ( $path, $method, $cb ) {
		register_rest_route( 'nadlan/v1', '/forum/chat' . $path, array( 'methods' => $method, 'permission_callback' => '__return_true', 'callback' => $cb, 'show_in_index' => false ) );
	};

	// the history of the room (also after a pin, a delete or a reaction someone else made: the page asks again)
	$reg( '', 'GET', function ( WP_REST_Request $q ) {
		$c = nlfch_ctx( $q, false );
		if ( is_wp_error( $c ) ) { return $c; }
		if ( ! nlfc_rl( 'chl', 'm' . (int) $c['m']['id'], 900, HOUR_IN_SECONDS ) ) { return nlfch_err( 'rate' ); }
		$rows   = nlfch_public( nlfch_room_rows( $c['room'] ), $c['r'], (int) $c['m']['id'], $c['host'] );
		$pinned = 0;
		foreach ( $rows as $x ) { if ( $x['pinned'] ) { $pinned = $x['id']; } }
		return nlfc_ok( array( 'rows' => $rows, 'pinned' => $pinned, 'host' => $c['host'] ? 1 : 0, 'me' => (int) $c['m']['id'] ) );
	} );

	// one message: text, a file the member uploaded through the media module (POST media), or both
	$reg( '/send', 'POST', function ( WP_REST_Request $q ) {
		$c = nlfch_ctx( $q, true );
		if ( is_wp_error( $c ) ) { return $c; }
		$m     = $c['m'];
		$mid   = (int) $m['id'];
		$body  = nlfch_body_clean( (string) $q->get_param( 'body' ) );
		$media = max( 0, (int) $q->get_param( 'media' ) );
		$e     = nlfch_body_error( $body, $media > 0 );
		if ( '' === $e ) { $e = nlfch_rate_error( nlfc_rl_peek( 'chm', 'm' . $mid, MINUTE_IN_SECONDS ), nlfc_rl_peek( 'chd', 'm' . $mid, DAY_IN_SECONDS ) ); }
		if ( '' === $e ) { $e = nlfch_rule_error( $body, (int) $m['approved_posts'] ); }
		if ( '' !== $e ) { return nlfch_err( 'rule', $e ); }
		global $wpdb;
		if ( $media > 0 ) { // the file must be the member's own, just uploaded and on no post: it becomes a chat file (status 'chat')
			if ( ! function_exists( 'nlfmd_t' ) || ! function_exists( 'nlfmd_ready' ) || ! nlfmd_ready() ) { return nlfch_err( 'media' ); }
			$n = $wpdb->query( $wpdb->prepare( 'UPDATE ' . nlfmd_t( 'media' ) . " SET status = 'chat' WHERE id = %d AND member_id = %d AND topic_id IS NULL AND reply_id IS NULL AND status = 'pending' AND kind IN ('image','pdf')", $media, $mid ) );
			if ( 1 !== (int) $n ) { return nlfch_err( 'media' ); }
		}
		$wpdb->insert( nlfch_t(), array( 'room' => $c['room'], 'member_id' => $mid, 'body' => $body, 'media_id' => $media > 0 ? $media : null, 'pinned' => 0,
			'reactions' => '', 'attached' => 0, 'created_at' => gmdate( 'Y-m-d H:i:s' ) ) );
		$id = (int) $wpdb->insert_id;
		if ( $id <= 0 ) { return nlfch_err( 'fail' ); }
		nlfc_rl_hit( 'chm', 'm' . $mid, MINUTE_IN_SECONDS );
		nlfc_rl_hit( 'chd', 'm' . $mid, DAY_IN_SECONDS );
		$rows = nlfch_public( array( nlfch_row( $c['room'], $id ) ), $c['r'], $mid, $c['host'] );
		return nlfc_ok( array( 'row' => $rows[0] ) );
	} );

	// "מועיל" / "תודה": one per person per message, never on one's own message; the counts are everyone's
	$reg( '/react', 'POST', function ( WP_REST_Request $q ) {
		$c = nlfch_ctx( $q, true );
		if ( is_wp_error( $c ) ) { return $c; }
		$mid  = (int) $c['m']['id'];
		$kind = nlfch_react_norm( (string) $q->get_param( 'kind' ) );
		$row  = nlfch_row( $c['room'], (int) $q->get_param( 'id' ) );
		if ( ! $row || '' === $kind ) { return nlfch_err( 'gone' ); }
		if ( (int) $row['member_id'] === $mid ) { return nlfch_err( 'self' ); }
		if ( ! nlfc_rl( 'chx', 'm' . $mid, 120, HOUR_IN_SECONDS ) ) { return nlfch_err( 'rate' ); }
		$map = nlfch_reacts_toggle( $row['reactions'], $mid, $kind );
		global $wpdb;
		$wpdb->update( nlfch_t(), array( 'reactions' => wp_json_encode( $map ) ), array( 'id' => (int) $row['id'] ) );
		return nlfc_ok( array( 'id' => (int) $row['id'], 'reacts' => nlfch_reacts_counts( $map ), 'mine' => nlfch_reacts_mine( $map, $mid ) ) );
	} );

	// the host pins one message (a second press on the pinned one takes it off)
	$reg( '/pin', 'POST', function ( WP_REST_Request $q ) {
		$c = nlfch_ctx( $q, true );
		if ( is_wp_error( $c ) ) { return $c; }
		if ( ! $c['host'] ) { return nlfch_err( 'host' ); }
		$row = nlfch_row( $c['room'], (int) $q->get_param( 'id' ) );
		if ( ! $row ) { return nlfch_err( 'gone' ); }
		if ( ! nlfc_rl( 'chp', 'm' . (int) $c['m']['id'], 120, HOUR_IN_SECONDS ) ) { return nlfch_err( 'rate' ); }
		$on = '1' === (string) (int) $q->get_param( 'on' );
		global $wpdb;
		$wpdb->query( $wpdb->prepare( 'UPDATE ' . nlfch_t() . ' SET pinned = 0 WHERE room = %s AND pinned = 1', $c['room'] ) );
		if ( $on ) { $wpdb->update( nlfch_t(), array( 'pinned' => 1 ), array( 'id' => (int) $row['id'] ) ); }
		return nlfc_ok( array( 'pinned' => $on ? (int) $row['id'] : 0 ) );
	} );

	// the author deletes his own message; the host deletes any message of his room
	$reg( '/delete', 'POST', function ( WP_REST_Request $q ) {
		$c = nlfch_ctx( $q, true );
		if ( is_wp_error( $c ) ) { return $c; }
		$row = nlfch_row( $c['room'], (int) $q->get_param( 'id' ) );
		if ( ! $row ) { return nlfch_err( 'gone' ); }
		if ( (int) $row['member_id'] !== (int) $c['m']['id'] && ! $c['host'] ) { return nlfch_err( 'own' ); }
		if ( ! nlfc_rl( 'chdel', 'm' . (int) $c['m']['id'], 120, HOUR_IN_SECONDS ) ) { return nlfch_err( 'rate' ); }
		nlfch_delete_rows( array( $row ) );
		return nlfc_ok( array( 'id' => (int) $row['id'] ) );
	} );

	// a report goes into the forum's flags table (target_type 'chat'); three different members take the message off
	$reg( '/report', 'POST', function ( WP_REST_Request $q ) {
		$c = nlfch_ctx( $q, true );
		if ( is_wp_error( $c ) ) { return $c; }
		$mid    = (int) $c['m']['id'];
		$row    = nlfch_row( $c['room'], (int) $q->get_param( 'id' ) );
		$reason = sanitize_key( (string) $q->get_param( 'reason' ) );
		$reason = '' === $reason ? 'other' : $reason;
		if ( ! $row ) { return nlfch_err( 'gone' ); }
		if ( (int) $row['member_id'] === $mid ) { return nlfch_err( 'self' ); }
		if ( ! function_exists( 'nlf_report_reasons' ) || ! isset( nlf_report_reasons()[ $reason ] ) ) { return nlfch_err( 'reason' ); }
		if ( ! nlfc_rl( 'chr', 'm' . $mid, 30, HOUR_IN_SECONDS ) ) { return nlfch_err( 'rate' ); }
		global $wpdb;
		$ft = nlf_t( 'flags' );
		$wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO $ft (target_type, target_id, member_id, ip_hash, reason, created_at) VALUES ('chat', %d, %d, %s, %s, %s)",
			(int) $row['id'], $mid, nlf_ip_hash(), $reason, gmdate( 'Y-m-d H:i:s' ) ) );
		$n = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(DISTINCT member_id) FROM $ft WHERE target_type = 'chat' AND target_id = %d", (int) $row['id'] ) );
		$gone = 0;
		if ( $n >= nlfch_limits()['hide'] ) {
			$gone = (int) $row['id'];
			if ( function_exists( 'nlf_mail' ) && function_exists( 'nlf_admin_to' ) ) {
				nlf_mail( nlf_admin_to(), '[פורום] הודעת צ\'אט הוסרה אחרי 3 דיווחים',
					"שלושה משתתפים בחדר וידאו דיווחו על הודעה בצ'אט, והיא הוסרה.\n\n" . nlf_excerpt( (string) $row['body'], 800 ) . "\n" );
			}
			nlfch_delete_rows( array( $row ) );
		}
		return nlfc_ok( array( 'message' => 'תודה. הדיווח התקבל.', 'gone' => $gone ) );
	} );

	// the host's end-of-call sheet (board 22 part ג): what there is to attach
	$reg( '/summary', 'GET', function ( WP_REST_Request $q ) {
		$c = nlfch_ctx( $q, false );
		if ( is_wp_error( $c ) ) { return $c; }
		if ( ! $c['host'] ) { return nlfch_err( 'host' ); }
		$ctx = nlfc_ctx( $c['r'] );
		$can = $ctx && (int) $ctx['topic'] > 0 && empty( $c['r']['sum'] );
		if ( ! $can ) { return nlfc_ok( array( 'can' => 0 ) ); }
		$p    = nlfch_summary_parts( nlfch_summary_rows( $c['room'] ) );
		$imgs = 0; $pdfs = 0;
		foreach ( array_slice( $p['media'], 0, nlfch_limits()['files'] ) as $x ) { if ( 'pdf' === $x['media_kind'] ) { $pdfs++; } else { $imgs++; } }
		$pin = $p['pin'] && '' !== trim( (string) $p['pin']['body'] ) ? array( 'id' => (int) $p['pin']['id'], 'text' => (string) $p['pin']['body'] ) : null;
		return nlfc_ok( array( 'can' => 1, 'topic' => (int) $ctx['topic'], 'title' => (string) $ctx['title'], 'pinned' => $pin,
			'media' => array( 'n' => $imgs + $pdfs, 'label' => nlfch_media_label( $imgs, $pdfs ) ), 'rest' => count( $p['rest'] ) ) );
	} );

	// ONE answer on the discussion, through the forum's own steps for an answer (limits, rules, status, counters, reputation, mail)
	$reg( '/attach', 'POST', function ( WP_REST_Request $q ) {
		$c = nlfch_ctx( $q, true );
		if ( is_wp_error( $c ) ) { return $c; }
		if ( ! $c['host'] ) { return nlfch_err( 'host' ); }
		$m   = $c['m'];
		$r   = $c['r'];
		$ctx = nlfc_ctx( $r );
		if ( ! $ctx || (int) $ctx['topic'] <= 0 ) { return nlfch_err( 'home' ); }
		if ( ! empty( $r['sum'] ) ) { return nlfch_err( 'already' ); }
		$t = function_exists( 'nlf_topic' ) ? nlf_topic( (int) $ctx['topic'] ) : null;
		if ( ! $t || 'live' !== (string) $t['status'] ) { return nlfch_err( 'topic' ); }
		$pick = nlfch_summary_choose( nlfch_summary_parts( nlfch_summary_rows( $c['room'] ) ), '1' === (string) (int) $q->get_param( 'pin' ),
			'1' === (string) (int) $q->get_param( 'media' ), '1' === (string) (int) $q->get_param( 'rest' ) );
		if ( ! $pick['items'] && ! $pick['media'] ) { return nlfch_err( 'nothing' ); }
		$body = nlf_text_norm( nlfch_summary_text( $pick['items'] ) );
		// the forum's write ceiling (nlf_guard 'post') and its content limits for an answer, as the reply route runs them
		if ( nlf_writes_hour( $m ) >= 20 ) { return nlfch_err( 'rule', 'הגעתם למספר ההודעות המרבי לשעה. נסו שוב מאוחר יותר.' ); }
		$e = nlf_body_error( $body, true );
		if ( '' === $e ) { $e = nlf_post_limits( $m, false, $body ); }
		$fake = new WP_REST_Request( 'POST', '/nadlan/v1/forum/reply' );
		$fake->set_param( 'topic_id', (int) $t['id'] );
		$fake->set_param( 'body', $body );
		if ( '' === $e ) { $e = (string) apply_filters( 'nlf_post_check', '', 'reply', $m, $fake, $t ); }
		if ( '' !== $e ) { return nlfch_err( 'rule', $e ); }
		global $wpdb;
		$status = nlf_first_status( $m['approved_posts'], $body, '0' !== (string) get_option( 'nadlan_forum_autoapprove', '1' ) );
		$wpdb->insert( nlf_t( 'replies' ), array( 'topic_id' => (int) $t['id'], 'member_id' => (int) $m['id'], 'body' => $body, 'quote_id' => null,
			'status' => $status, 'body_hash' => nlf_dup_key( $body ), 'ip_hash' => nlf_ip_hash(), 'created_at' => nlf_now_sql() ) );
		$id = (int) $wpdb->insert_id;
		if ( $id <= 0 ) { return nlfch_err( 'fail' ); }
		do_action( 'nlf_post_created', 'reply', $id, $m, $fake, $status, (int) $t['id'] ); // the other modules see a normal answer
		// the files of the chat go on the answer with their owners kept (the media module's own guarded update: on no post yet)
		if ( function_exists( 'nlfmd_t' ) ) {
			foreach ( $pick['media'] as $i => $x ) {
				$wpdb->query( $wpdb->prepare( 'UPDATE ' . nlfmd_t( 'media' ) . " SET topic_id = %d, reply_id = %d, caption = '', sort = %d, status = %s
					WHERE id = %d AND member_id = %d AND topic_id IS NULL AND reply_id IS NULL AND status = 'chat' AND kind IN ('image','pdf')",
					(int) $t['id'], $id, (int) $i, 'live' === $status ? 'ok' : 'pending', (int) $x['media_id'], (int) $x['member_id'] ) );
			}
		}
		nlf_write_counted( $m );
		if ( 'live' === $status ) { nlf_on_reply_live( $id ); } else { nlf_mail_admin_pending( 'reply', $id ); }
		if ( $pick['ids'] ) { $wpdb->query( 'UPDATE ' . nlfch_t() . ' SET attached = 1 WHERE id IN (' . implode( ',', array_map( 'intval', $pick['ids'] ) ) . ')' ); } // phpcs:ignore -- integers only
		$r['sum'] = $id;
		nlfc_room_put( $c['room'], $r );
		return nlfc_ok( array( 'id' => $id, 'status' => $status, 'url' => nlf_topic_url( (int) $t['id'], 'r' . $id ),
			'message' => 'live' === $status ? 'הסיכום צורף לדיון.' : 'הסיכום יעלה לדיון אחרי בדיקה קצרה.' ) );
	} );
} );

/* =========================================================================================================
 * 4. Retention: messages not attached to the discussion go after 7 days, with their files (daily, WP-Cron)
 * ======================================================================================================= */

function nlfch_gc() {
	if ( ! nlfch_ready() ) { return 0; }
	global $wpdb;
	$rows = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT id, media_id FROM ' . nlfch_t() . ' WHERE attached = 0 AND created_at < %s ORDER BY id ASC LIMIT 2000', nlfch_cutoff( time() ) ), ARRAY_A );
	return nlfch_delete_rows( $rows );
}
add_action( 'nlfch_gc', 'nlfch_gc' );
add_action( 'init', function () {
	if ( nlfch_ready() && function_exists( 'wp_next_scheduled' ) && ! wp_next_scheduled( 'nlfch_gc' ) ) { wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nlfch_gc' ); }
}, 30 );

/**
 * The test kit (scripts/project-stage/forum_testkit.py, `clean`): every chat row the removed members wrote, with its reports and
 * its never-attached files. Returns the count.
 */
function nlfch_purge_members( array $ids ) {
	$ids = array_values( array_filter( array_map( 'intval', $ids ) ) );
	if ( ! $ids || ! nlfch_ready() ) { return 0; }
	global $wpdb;
	$rows = (array) $wpdb->get_results( 'SELECT id, media_id FROM ' . nlfch_t() . ' WHERE member_id IN (' . implode( ',', $ids ) . ')', ARRAY_A ); // phpcs:ignore -- integers only
	return nlfch_delete_rows( $rows );
}
