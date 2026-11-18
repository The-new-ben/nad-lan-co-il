<?php
/**
 * nad-lan professionals' forum: one-tap video calls inside a discussion (12.11.2026).
 *
 * Loaded by ONE line the forum module adds at the end of inc/pro-forum.php (see docs/research/2026-11-12-pro-forum/CALL-NOTES.md):
 *   if ( file_exists( __DIR__ . '/pro-forum-call.php' ) ) { require_once __DIR__ . '/pro-forum-call.php'; }
 * It uses the forum's own functions (nlf_me, nlf_gate_open, nlf_nonce_for, nlf_topic, nlf_members, nlf_author, nlf_mail,
 * nlf_topic_url, nlf_link_token, nlf_link_read, nlf_key, nlf_ip_hash, nlf_t, nlf_surface, nlf_rendering, nlf_nocache) and edits no
 * forum file. Every route checks that they exist and answers 400 when the forum is not loaded.
 *
 * REST (nadlan/v1/forum/call...), every error HTTP 400 (never 403: the host turns a 403 into its own page):
 *   POST call/open    {topic, with, room?}  -> {room, title, topic_url, with}   a new room, or one more person in my room
 *   POST call/token   {room}                -> {url, token, identity, ...}       my LiveKit token for a room I belong to
 *   GET  call/status  {room?}               -> {invites, pref} or {exists, ...}  the in-forum notification (polled) and a room's state
 *   POST call/pref    {video, mail}         -> {pref}                            my own two switches
 *   POST call/room    {topic?}              -> {room, topic, card, title, topic_url, link, max, open, locked}   a new OPEN video room (board 19)
 *   POST call/join    {room}                -> the same fields                   come into an open room by its link
 *   POST call/lock    {room, lock}          -> {room, lock}                      the host locks or opens his open room
 * Board 19 (18.11.2026): an open room is the button every visitor sees (forum home, every live discussion, every card page);
 * whoever holds its link and is a forum member may come in, up to NLFC_ROOM_PEOPLE, unless the host locked it.
 * Rules: only a signed-in forum member; only with a member who switched video calls on. 18.11.2026 (board 18): any member in good
 * standing may call such a member from that member's card (POST call/open {card}; the room carries the card instead of a
 * discussion) or from any LIVE discussion that member wrote in; the first rule (author and answerer) stays as one more path.
 * Never oneself, at most 3 new rooms a day from one caller to the same person. 8 new rooms a day per member and per hashed IP, 40 a day
 * for the whole forum (own buckets, separate from together.php and designer.php). No recording, nothing stored about the call
 * beyond a six-hour transient, no mail to the site owner. The invited member gets the in-forum notice and, only if he switched
 * it on, one mail.
 * LiveKit: rooms 'nadlan-frm-<12 a-z2-7>'. The token comes from exactly the source designer.php uses (nadlan_dsg_call_lk():
 * a local key when the site has one, else the shared project's edge function, HMAC-signed with together.php's stored proxy
 * secret). Nothing here reads a secret except through those functions at request time; no secret is printed or stored.
 */

if ( ! defined( 'ABSPATH' ) && ! defined( 'NLFC_PURE_ONLY' ) ) { exit; }

/* =========================================================================================================
 * 1. Pure functions (no WordPress). tests-local/pro-forum-call-test.php loads only this part (NLFC_PURE_ONLY).
 * ======================================================================================================= */

if ( ! defined( 'NLFC_PREFIX' ) ) { define( 'NLFC_PREFIX', 'nadlan-frm-' ); }
if ( ! defined( 'NLFC_ROOM_TTL' ) ) { define( 'NLFC_ROOM_TTL', 6 * 3600 ); }
if ( ! defined( 'NLFC_MAX_PEOPLE' ) ) { define( 'NLFC_MAX_PEOPLE', 4 ); } // the two who talk, plus up to two more they invite
if ( ! defined( 'NLFC_ROOM_PEOPLE' ) ) { define( 'NLFC_ROOM_PEOPLE', 6 ); } // an OPEN video room (board 19): whoever has the link, up to six

/** $n characters of a-z and 2-7 (the alphabet of the designer's and together's rooms); $bytes only for the tests */
function nlfc_rand( $n, $bytes = null ) {
	$alpha = 'abcdefghijklmnopqrstuvwxyz234567';
	$bytes = null === $bytes ? random_bytes( (int) $n ) : (string) $bytes;
	$out   = '';
	for ( $i = 0; $i < (int) $n; $i++ ) { $out .= $alpha[ ord( $bytes[ $i % strlen( $bytes ) ] ) & 31 ]; }
	return $out;
}

function nlfc_room_valid( $id ) { return is_string( $id ) && 1 === preg_match( '/^[a-z2-7]{12}$/', $id ); }

/** the LiveKit room of a forum room id */
function nlfc_lk_room( $room ) { return NLFC_PREFIX . $room; }

function nlfc_lk_room_valid( $name ) { return is_string( $name ) && 1 === preg_match( '/^nadlan-frm-[a-z2-7]{12}$/', $name ); }

/** the index of a fixed window (UTC days for $window = 86400) */
function nlfc_window( $now, $window ) { return (int) floor( (int) $now / max( 1, (int) $window ) ); }

/** the transient name of one counter: bucket, who (member id or hashed IP or 'all'), window */
function nlfc_rl_key( $bucket, $who, $now, $window ) {
	return 'nlfc_rl_' . md5( (string) $bucket . '|' . (string) $who . '|' . nlfc_window( $now, $window ) );
}

/** the daily caps (member, ip, forum) */
function nlfc_caps() { return array( 'member' => 8, 'ip' => 8, 'forum' => 40 ); }

/** '' when one more room may open, else the cap that is full: 'rate_member' | 'rate_ip' | 'rate_forum' */
function nlfc_limits_verdict( array $counts, array $caps = array() ) {
	$caps = array_merge( nlfc_caps(), $caps );
	if ( (int) ( $counts['member'] ?? 0 ) >= (int) $caps['member'] ) { return 'rate_member'; }
	if ( (int) ( $counts['ip'] ?? 0 ) >= (int) $caps['ip'] ) { return 'rate_ip'; }
	if ( (int) ( $counts['forum'] ?? 0 ) >= (int) $caps['forum'] ) { return 'rate_forum'; }
	return '';
}

/** the ids of the members who wrote a LIVE reply in the discussion; $replies = rows with member_id and status */
function nlfc_repliers( array $replies ) {
	$out = array();
	foreach ( $replies as $r ) {
		if ( 'live' === (string) ( $r['status'] ?? '' ) && (int) ( $r['member_id'] ?? 0 ) > 0 ) { $out[ (int) $r['member_id'] ] = true; }
	}
	return array_keys( $out );
}

/**
 * May $caller open a call with $with inside $topic? '' = yes, else the refusal code.
 * $topic: id, member_id (who opened it), status. $replies: rows {member_id, status}. $video_on: member id => bool (the switch).
 * $member_ok: member id => bool (status 'ok'). Both must have written; one of the two is the person who opened the discussion.
 */
function nlfc_can_call( array $topic, array $replies, $caller, $with, array $video_on, array $member_ok ) {
	$caller = (int) $caller;
	$with   = (int) $with;
	if ( (int) ( $topic['id'] ?? 0 ) <= 0 || 'live' !== (string) ( $topic['status'] ?? '' ) ) { return 'topic'; }
	if ( $caller <= 0 || $with <= 0 ) { return 'with'; }
	if ( $caller === $with ) { return 'self'; }
	$author   = (int) ( $topic['member_id'] ?? 0 );
	$repliers = nlfc_repliers( $replies );
	$wrote    = function ( $m ) use ( $author, $repliers ) { return $m === $author || in_array( $m, $repliers, true ); };
	if ( ! $wrote( $caller ) || ! $wrote( $with ) ) { return 'wrote'; }
	if ( $caller !== $author && $with !== $author ) { return 'pair'; }
	if ( $caller === $author && ! in_array( $with, $repliers, true ) ) { return 'wrote'; } // the other one answered
	if ( $with === $author && ! in_array( $caller, $repliers, true ) ) { return 'wrote'; }
	if ( empty( $member_ok[ $with ] ) ) { return 'member'; }
	if ( empty( $video_on[ $with ] ) ) { return 'video_off'; }
	return '';
}

/** the members $caller may call in $topic (same rules), in the order they first answered */
function nlfc_targets( array $topic, array $replies, $caller, array $video_on, array $member_ok ) {
	$caller = (int) $caller;
	$cands  = array_merge( array( (int) ( $topic['member_id'] ?? 0 ) ), nlfc_repliers( $replies ) );
	$out    = array();
	foreach ( array_unique( $cands ) as $m ) {
		if ( $m > 0 && '' === nlfc_can_call( $topic, $replies, $caller, $m, $video_on, $member_ok ) ) { $out[] = $m; }
	}
	return $out;
}

/** the daily cap from one caller to the same person (18.11.2026) */
function nlfc_pair_cap() { return 3; }

/**
 * The rule of 18.11.2026 (board 18): a signed-in member in good standing may call ANY member who switched video on, from that
 * member's card or from a discussion that member wrote in. Never himself, at most nlfc_pair_cap() calls a day to the same
 * person. '' = yes, else the refusal code. (The caller's own standing is checked by nlfc_member() before this.)
 */
function nlfc_can_reach( $caller, $with, $with_ok, $with_video, $pair_today = 0 ) {
	$caller = (int) $caller;
	$with   = (int) $with;
	if ( $caller <= 0 || $with <= 0 ) { return 'with'; }
	if ( $caller === $with ) { return 'self'; }
	if ( ! $with_ok ) { return 'member'; }
	if ( ! $with_video ) { return 'video_off'; }
	if ( (int) $pair_today >= nlfc_pair_cap() ) { return 'rate_pair'; }
	return '';
}

/**
 * A call from inside a discussion: the first rule (author and answerer, nlfc_can_call) stays as one path; the second path is
 * the 18.11.2026 rule, for a member $with who wrote in the discussion (opened it, or a live answer). '' = yes.
 */
function nlfc_can_call_open( array $topic, array $replies, $caller, $with, array $video_on, array $member_ok, $pair_today = 0 ) {
	$caller = (int) $caller;
	$with   = (int) $with;
	if ( '' === nlfc_can_call( $topic, $replies, $caller, $with, $video_on, $member_ok ) ) {
		return (int) $pair_today >= nlfc_pair_cap() ? 'rate_pair' : '';
	}
	if ( (int) ( $topic['id'] ?? 0 ) <= 0 || 'live' !== (string) ( $topic['status'] ?? '' ) ) { return 'topic'; }
	if ( $caller <= 0 || $with <= 0 ) { return 'with'; }
	if ( $caller === $with ) { return 'self'; }
	if ( $with !== (int) ( $topic['member_id'] ?? 0 ) && ! in_array( $with, nlfc_repliers( $replies ), true ) ) { return 'nowrote'; }
	return nlfc_can_reach( $caller, $with, ! empty( $member_ok[ $with ] ), ! empty( $video_on[ $with ] ), $pair_today );
}

/**
 * The video pills of a discussion page, for anyone looking (a guest too: the press asks him to enter first): every member who
 * wrote in it and switched video on, except the viewer. op = he opened it; replies = the ids of all his live answers.
 */
function nlfc_page_pills( array $topic, array $replies, $viewer, array $video_on, array $member_ok ) {
	$viewer = (int) $viewer;
	$author = (int) ( $topic['member_id'] ?? 0 );
	if ( 'live' !== (string) ( $topic['status'] ?? '' ) ) { return array(); }
	$by = array();
	if ( $author > 0 ) { $by[ $author ] = array(); }
	foreach ( $replies as $r ) {
		if ( 'live' !== (string) ( $r['status'] ?? '' ) || (int) ( $r['member_id'] ?? 0 ) <= 0 ) { continue; }
		$by[ (int) $r['member_id'] ][] = (int) ( $r['id'] ?? 0 );
	}
	$out = array();
	foreach ( $by as $m => $ids ) {
		if ( $m === $viewer || empty( $video_on[ $m ] ) || empty( $member_ok[ $m ] ) ) { continue; }
		$ids   = array_values( array_filter( $ids ) );
		$out[] = array( 'with' => $m, 'op' => $m === $author ? 1 : 0, 'replies' => $ids, 'reply' => $ids ? (int) end( $ids ) : 0 );
	}
	return $out;
}

/**
 * An OPEN video room (board 19, 18.11.2026): opened by one member, from the forum home (topic 0), a live discussion (topic id)
 * or a card page (also topic 0: the room never names the card's person). ok = member id => LiveKit identity ('' until a token).
 */
function nlfc_room_new_open( $mid, $topic, $now ) {
	return array( 't' => (int) $now, 'topic' => max( 0, (int) $topic ), 'card' => 0, 'by' => (int) $mid, 'ok' => array( (int) $mid => '' ), 'open' => 1, 'lock' => 0 );
}

/** an open room with no discussion and no card: the "home room", its place is the forum home */
function nlfc_room_is_home( array $r ) { return ! empty( $r['open'] ) && (int) ( $r['topic'] ?? 0 ) <= 0 && (int) ( $r['card'] ?? 0 ) <= 0; }

/** how many people a room holds: an open room 6, a direct call 4 */
function nlfc_room_max( array $r ) { return ! empty( $r['open'] ) ? NLFC_ROOM_PEOPLE : NLFC_MAX_PEOPLE; }

/** May $mid come into $room by its link? '' = yes (or already in), else 'notin' | 'locked' | 'full' */
function nlfc_can_join( array $room, $mid, $max ) {
	$ok = isset( $room['ok'] ) && is_array( $room['ok'] ) ? $room['ok'] : array();
	if ( (int) $mid > 0 && array_key_exists( (int) $mid, $ok ) ) { return ''; }
	if ( empty( $room['open'] ) ) { return 'notin'; } // a direct call is by invitation only
	if ( ! empty( $room['lock'] ) ) { return 'locked'; }
	if ( count( $ok ) >= (int) $max ) { return 'full'; }
	return '';
}

/** '' or the reason a write request is refused: the browser's own fetch-site and origin headers (when sent) must be this site */
function nlfc_fetch_refusal( array $h, $home_host ) {
	$sfs = strtolower( trim( (string) ( $h['sec_fetch_site'] ?? '' ) ) );
	if ( '' !== $sfs && 'same-origin' !== $sfs ) { return 'site'; }
	$origin = trim( (string) ( $h['origin'] ?? '' ) );
	if ( '' !== $origin ) {
		$oh = strtolower( (string) parse_url( $origin, PHP_URL_HOST ) ); // phpcs:ignore -- pure part, no WordPress here
		if ( '' === $oh || $oh !== strtolower( (string) $home_host ) ) { return 'origin'; }
	}
	return '';
}

/** the Hebrew message of every refusal (all answered as HTTP 400); $room = an open video room, where 'full' and 'gone' read as a room */
function nlfc_msg( $code, $room = false ) {
	if ( $room ) {
		$r = array(
			'full'  => 'החדר מלא. בחדר וידאו יש מקום לעד 6 אנשים.',
			'gone'  => 'החדר הזה כבר נסגר.',
			'notin' => 'אין לכם גישה לחדר הזה.',
			'rate'  => 'נסו שוב בעוד כמה דקות.',
		);
		if ( isset( $r[ $code ] ) ) { return $r[ $code ]; }
	}
	$m = array(
		'locked'      => 'החדר נעול. בקשו ממי שפתח אותו לפתוח את הנעילה.',
		'host'        => 'רק מי שפתח את החדר יכול לנעול אותו.',
		'rate_join'   => 'נכנסתם היום להרבה חדרים. אפשר שוב מחר.',
		'closed'      => 'הדף לא נמצא.',
		'off'         => 'שיחות וידאו לא זמינות כרגע.',
		'need_entry'  => 'כדי לפתוח שיחה צריך להיכנס לפורום. זה צעד אחד.',
		'nonce'       => 'הדף ישן. רעננו אותו ונסו שוב.',
		'blocked'     => 'החשבון הזה לא יכול לפתוח שיחות כרגע.',
		'site'        => 'הבקשה לא תקינה.',
		'origin'      => 'הבקשה לא תקינה.',
		'topic'       => 'הדיון לא נמצא.',
		'with'        => 'לא ברור עם מי לפתוח את השיחה.',
		'self'        => 'אי אפשר להתקשר אל עצמכם.',
		'wrote'       => 'שיחת וידאו נפתחת רק עם מי שכבר ענה בדיון, ורק אחרי ששניכם כתבתם בו.',
		'pair'        => 'שיחת וידאו נפתחת בין מי שפתח את הדיון לבין מי שענה לו.',
		'member'      => 'המשתתף הזה לא זמין כרגע.',
		'video_off'   => 'המשתתף הזה לא פתח שיחות וידאו. אפשר לכתוב לו בדיון.',
		'rate_member' => 'פתחתם היום 8 שיחות. אפשר לפתוח עוד מחר.',
		'rate_ip'     => 'נפתחו היום הרבה שיחות מהחיבור הזה. נסו שוב מחר.',
		'rate_forum'  => 'נפתחו היום הרבה שיחות בפורום. נסו שוב מחר.',
		'rate'        => 'נסו שוב בעוד כמה דקות.',
		'gone'        => 'השיחה הזו כבר הסתיימה.',
		'notin'       => 'אין לכם הזמנה לשיחה הזו.',
		'full'        => 'השיחה מלאה.',
		'already'     => 'המשתתף הזה כבר מוזמן לשיחה.',
		'lk'          => 'לא הצלחנו לחבר את השיחה. נסו שוב בעוד רגע.',
		'nowrote'     => 'מתוך דיון אפשר להתקשר למי שכתב בו.',
		'card'        => 'הכרטיס לא נמצא.',
		'rate_pair'   => 'כבר התקשרתם היום 3 פעמים לאותו אדם. אפשר שוב מחר.',
	);
	return $m[ $code ] ?? 'משהו השתבש. נסו שוב.';
}

/** one line of plain text (names and titles go into a mail subject) */
function nlfc_line( $s, $n ) {
	$s = trim( (string) preg_replace( '/\s+/u', ' ', (string) $s ) );
	return function_exists( 'mb_substr' ) ? mb_substr( $s, 0, (int) $n, 'UTF-8' ) : substr( $s, 0, (int) $n );
}

/** the invitation mail: subject and body ($card: the call started from the receiver's own card, there is no discussion) */
function nlfc_mail_parts( $name, $title, $link, $stop, $card = false ) {
	$name  = nlfc_line( $name, 40 );
	$title = nlfc_line( $title, 120 );
	$subj  = $card ? $name . ' מזמין אתכם לשיחת וידאו מהכרטיס שלכם' : $name . ' מזמין אתכם לשיחת וידאו על ' . $title;
	$body  = ( $card ? $name . " מזמין אתכם לשיחת וידאו מהכרטיס שלכם בנדל\"ן.\n\n" : $name . ' מזמין אתכם לשיחת וידאו על הדיון "' . $title . "\" בפורום נדל\"ן.\n\n" )
		. 'להצטרפות לשיחה: ' . $link . "\n"
		. ( $card ? "הקישור פותח את השיחה בכרטיס שלכם. " : 'הקישור פותח את השיחה בתוך הדיון. ' ) . "נכנסים עם מצלמה ומיקרופון כבויים, ומפעילים כשרוצים.\n"
		. "השיחה לא מוקלטת.\n\n"
		. 'לא לקבל עוד מיילים על שיחות וידאו: ' . $stop . "\n";
	return array( $subj, $body );
}

/** the invites a member still has: newest first, at most $max, none older than $ttl seconds, one per room */
function nlfc_invites_prune( array $list, $now, $ttl = 900, $max = 5 ) {
	$seen = array();
	$out  = array();
	usort( $list, function ( $a, $b ) { return (int) ( $b['t'] ?? 0 ) <=> (int) ( $a['t'] ?? 0 ); } );
	foreach ( $list as $i ) {
		$room = (string) ( $i['room'] ?? '' );
		if ( ! nlfc_room_valid( $room ) || isset( $seen[ $room ] ) || (int) $now - (int) ( $i['t'] ?? 0 ) > $ttl ) { continue; }
		$seen[ $room ] = true;
		$out[]         = $i;
		if ( count( $out ) >= $max ) { break; }
	}
	return $out;
}

if ( defined( 'NLFC_PURE_ONLY' ) ) { return; }

/* =========================================================================================================
 * 2. Switches, table, answers
 * ======================================================================================================= */

/** the module's own switch (option nadlan_forum_call, on unless the owner sets '0') and the forum module present */
function nlfc_on() {
	return function_exists( 'nlf_gate_open' ) && function_exists( 'nlf_me' ) && '0' !== (string) get_option( 'nadlan_forum_call', '1' );
}

function nlfc_err( $code, $room = false ) {
	if ( function_exists( 'nlf_nocache' ) ) { nlf_nocache(); }
	return new WP_Error( 'nlfc_' . $code, nlfc_msg( $code, $room ), array( 'status' => 400 ) );
}

function nlfc_ok( array $data ) {
	if ( function_exists( 'nlf_nocache' ) ) { nlf_nocache(); }
	$r = new WP_REST_Response( array_merge( array( 'ok' => 1 ), $data ), 200 );
	$r->header( 'Cache-Control', 'no-store, max-age=0' );
	$r->header( 'X-Robots-Tag', 'noindex, nofollow' );
	return $r;
}

function nlfc_table() { global $wpdb; return $wpdb->prefix . 'nadlan_forum_callpref'; }

/** the switches table, once (option nadlan_forum_call_db); a failed attempt waits an hour */
function nlfc_install() {
	if ( '1' === (string) get_option( 'nadlan_forum_call_db' ) || get_transient( 'nlfc_install_wait' ) ) { return; }
	global $wpdb;
	require_once ABSPATH . 'wp-admin/includes/upgrade.php';
	dbDelta( 'CREATE TABLE ' . nlfc_table() . ' (
		member_id BIGINT UNSIGNED NOT NULL,
		video_on TINYINT(1) NOT NULL DEFAULT 0,
		mail_on TINYINT(1) NOT NULL DEFAULT 0,
		updated_at DATETIME NOT NULL,
		PRIMARY KEY  (member_id)
	) ' . $wpdb->get_charset_collate() . ';' );
	if ( nlfc_table() !== (string) $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $wpdb->esc_like( nlfc_table() ) ) ) ) {
		set_transient( 'nlfc_install_wait', 1, HOUR_IN_SECONDS );
		return;
	}
	update_option( 'nadlan_forum_call_db', '1', true );
}
add_action( 'admin_init', 'nlfc_install' );

/** member id => array( video => bool, mail => bool ); a member with no row has both OFF */
function nlfc_prefs( array $ids ) {
	$ids = array_values( array_unique( array_filter( array_map( 'intval', $ids ) ) ) );
	$out = array();
	foreach ( $ids as $id ) { $out[ $id ] = array( 'video' => false, 'mail' => false ); }
	if ( ! $ids || '1' !== (string) get_option( 'nadlan_forum_call_db' ) ) { return $out; }
	global $wpdb;
	$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT member_id, video_on, mail_on FROM ' . nlfc_table() . ' WHERE member_id IN (' . implode( ',', array_fill( 0, count( $ids ), '%d' ) ) . ')', $ids ), ARRAY_A );
	foreach ( (array) $rows as $r ) { $out[ (int) $r['member_id'] ] = array( 'video' => (bool) (int) $r['video_on'], 'mail' => (bool) (int) $r['mail_on'] ); }
	return $out;
}

function nlfc_pref_set( $mid, $video, $mail ) {
	nlfc_install();
	global $wpdb;
	return false !== $wpdb->replace( nlfc_table(), array( 'member_id' => (int) $mid, 'video_on' => $video ? 1 : 0, 'mail_on' => $mail ? 1 : 0, 'updated_at' => gmdate( 'Y-m-d H:i:s' ) ) );
}

/* counters: transients named by nlfc_rl_key, one window long */
function nlfc_rl_peek( $bucket, $who, $window ) { return (int) get_transient( nlfc_rl_key( $bucket, $who, time(), $window ) ); }

function nlfc_rl_hit( $bucket, $who, $window ) {
	$k = nlfc_rl_key( $bucket, $who, time(), $window );
	set_transient( $k, (int) get_transient( $k ) + 1, $window );
}

/** true while under $max in the window, and counts this one */
function nlfc_rl( $bucket, $who, $max, $window ) {
	if ( nlfc_rl_peek( $bucket, $who, $window ) >= $max ) { return false; }
	nlfc_rl_hit( $bucket, $who, $window );
	return true;
}

/**
 * The member of this request, or a WP_Error 400: the module on, the forum gate open (else 'closed' for everybody, even with a
 * session), the session cookie, the forum's per-session header nonce, status ok, and for writes the browser's same-site headers.
 */
function nlfc_member( WP_REST_Request $r, $write ) {
	if ( ! function_exists( 'nlf_gate_open' ) || ! nlf_gate_open() ) { return nlfc_err( 'closed' ); }
	if ( ! nlfc_on() || ! function_exists( 'nlf_nonce_for' ) || ! function_exists( 'nlf_topic' ) ) { return nlfc_err( 'off' ); }
	if ( function_exists( 'nlf_install' ) ) { nlf_install(); }
	if ( $write ) {
		$why = nlfc_fetch_refusal( array( 'sec_fetch_site' => (string) $r->get_header( 'sec_fetch_site' ), 'origin' => (string) $r->get_header( 'origin' ) ), (string) wp_parse_url( home_url(), PHP_URL_HOST ) );
		if ( '' !== $why ) { return nlfc_err( $why ); }
	}
	$m = nlf_me();
	if ( ! $m ) { return nlfc_err( 'need_entry' ); }
	if ( ! hash_equals( nlf_nonce_for( $m ), (string) $r->get_header( 'x_nlf_nonce' ) ) ) { return nlfc_err( 'nonce' ); }
	if ( 'ok' !== (string) $m['status'] ) { return nlfc_err( 'blocked' ); }
	nlfc_install();
	return $m;
}

/* =========================================================================================================
 * 3. LiveKit: the same source as the designer's call
 * ======================================================================================================= */

/**
 * LiveKit's settings, or null. designer.php's nadlan_dsg_call_lk() first (it reads together.php's options at request time:
 * a local key, or the shared project's edge-function address + its 64-character HMAC secret); the same reading here when the
 * designer module is not loaded. The secret never leaves this request.
 */
function nlfc_lk() {
	if ( function_exists( 'nadlan_dsg_call_lk' ) ) { return nadlan_dsg_call_lk(); }
	if ( ! function_exists( 'nadlan_tr_opt' ) || ! function_exists( 'nadlan_tr_lk_ready' ) || ! nadlan_tr_lk_ready() ) { return null; }
	$key = (string) nadlan_tr_opt( 'lk_key' );
	if ( '' !== $key && function_exists( 'nadlan_tr_jwt' ) ) { return array( 'mode' => 'key', 'url' => (string) nadlan_tr_opt( 'lk_url' ), 'key' => $key, 'secret' => (string) nadlan_tr_opt( 'lk_secret' ) ); }
	$proxy = (string) nadlan_tr_opt( 'lk_proxy' );
	$sec   = (string) nadlan_tr_opt( 'lk_proxy_secret' );
	if ( '' === $proxy || 64 !== strlen( $sec ) ) { return null; }
	return array( 'mode' => 'proxy', 'proxy' => $proxy, 'proxy_secret' => $sec );
}

/**
 * The server address and the token of one person in one forum room, or null. The request to the edge function is the
 * designer's (nadlan_dsg_call_grant) with the room name 'nadlan-frm-<id>' in place of 'nadlan-dsg-<id>': HMAC-SHA256 of
 * room|identity|time under the stored proxy secret. The edge function serves 'nadlan-*' rooms only. Two hours.
 */
function nlfc_grant( $room, $identity, $name, $role, array $lk ) {
	$lk_room = nlfc_lk_room( $room );
	if ( 'key' === ( $lk['mode'] ?? '' ) ) {
		if ( ! function_exists( 'nadlan_tr_jwt' ) ) { return null; }
		$now = time();
		$tok = nadlan_tr_jwt( array(
			'iss'        => $lk['key'],
			'sub'        => (string) $identity,
			'name'       => (string) $name,
			'nbf'        => $now - 5,
			'exp'        => $now + 2 * HOUR_IN_SECONDS,
			'video'      => array( 'room' => $lk_room, 'roomJoin' => true, 'canPublish' => true, 'canSubscribe' => true, 'canPublishData' => true ),
			'metadata'   => wp_json_encode( array( 'role' => (string) $role ) ),
			'attributes' => array( 'role' => (string) $role ),
		), $lk['secret'] );
		return array( 'url' => (string) $lk['url'], 'token' => (string) $tok );
	}
	if ( 'proxy' !== ( $lk['mode'] ?? '' ) ) { return null; }
	$ts  = time();
	$sig = hash_hmac( 'sha256', $lk_room . '|' . $identity . '|' . $ts, (string) $lk['proxy_secret'] );
	$res = wp_remote_post( (string) $lk['proxy'], array(
		'timeout' => 8,
		'headers' => array( 'content-type' => 'application/json' ),
		'body'    => wp_json_encode( array( 'room' => $lk_room, 'identity' => (string) $identity, 'name' => (string) $name, 'role' => 'host' === $role ? 'buyer' : 'friend', 'ts' => $ts, 'sig' => $sig ) ),
	) );
	$body = is_wp_error( $res ) ? null : json_decode( (string) wp_remote_retrieve_body( $res ), true );
	if ( ! is_array( $body ) || empty( $body['token'] ) || empty( $body['url'] ) ) { return null; }
	return array( 'url' => (string) $body['url'], 'token' => (string) $body['token'] );
}

/* =========================================================================================================
 * 4. Rooms and invites (transients only; nothing about a call is kept after six hours)
 * ======================================================================================================= */

function nlfc_room_get( $room ) { $r = nlfc_room_valid( $room ) ? get_transient( 'nlfc_room_' . $room ) : false; return is_array( $r ) ? $r : null; }

function nlfc_room_put( $room, array $r ) {
	$left = NLFC_ROOM_TTL - ( time() - (int) ( $r['t'] ?? time() ) );
	set_transient( 'nlfc_room_' . $room, $r, max( 60, $left ) );
}

/** the live replies of a discussion: member_id, status, id */
function nlfc_replies( $tid ) {
	global $wpdb;
	return (array) $wpdb->get_results( $wpdb->prepare( 'SELECT id, member_id, status FROM ' . nlf_t( 'replies' ) . " WHERE topic_id = %d AND status = 'live' ORDER BY id ASC LIMIT 300", (int) $tid ), ARRAY_A );
}

/** a member's public face for the call: name and trade label (nlf_author) */
function nlfc_face( $m ) {
	$a = nlf_author( $m );
	return array( 'id' => $m ? (int) $m['id'] : 0, 'name' => (string) $a['name'], 'label' => (string) $a['label'] );
}

/** the call link inside the discussion (opens the gate while the forum is hidden; the room travels in the #fragment only) */
function nlfc_link( $tid, $room ) { return nlf_topic_url( (int) $tid, 'call=' . $room ); }

/** a card a call may start from (18.11.2026): published, not removed by its owner, and a JOINED member behind it; else null */
function nlfc_card_member( $card ) {
	$card = (int) $card;
	if ( $card <= 0 || 'nadlan_professional' !== get_post_type( $card ) || 'publish' !== get_post_status( $card ) ) { return null; }
	if ( function_exists( 'nlf_pro_removed' ) && nlf_pro_removed( $card ) ) { return null; }
	return function_exists( 'nlf_pro_member' ) ? nlf_pro_member( $card ) : null;
}

/** the title of a card room: the person's name */
function nlfc_card_title( $card ) {
	return function_exists( 'nadlan_prof_person_name' ) ? (string) nadlan_prof_person_name( (int) $card ) : (string) get_the_title( (int) $card );
}

/** the card's address (the gate opens while the forum is hidden), with the room in the #fragment when given */
function nlfc_card_url( $card, $room = '' ) {
	$u = (string) get_permalink( (int) $card );
	if ( function_exists( 'nlf_public' ) && ! nlf_public() ) { $u = add_query_arg( 'forum', 'on', $u ); }
	return $u . ( '' !== $room ? '#call=' . $room : '' );
}

/** a room's context: its discussion or its card. array( topic, card, title, url ) or null when that place is gone */
function nlfc_ctx( array $r ) {
	if ( nlfc_room_is_home( $r ) ) { return array( 'topic' => 0, 'card' => 0, 'title' => 'חדר וידאו', 'url' => nlfc_home_room_url() ); }
	if ( ! empty( $r['card'] ) ) {
		if ( ! nlfc_card_member( (int) $r['card'] ) ) { return null; }
		return array( 'topic' => 0, 'card' => (int) $r['card'], 'title' => nlfc_card_title( (int) $r['card'] ), 'url' => nlfc_card_url( (int) $r['card'] ) );
	}
	$t = nlf_topic( (int) ( $r['topic'] ?? 0 ) );
	if ( ! $t || 'live' !== (string) $t['status'] ) { return null; }
	return array( 'topic' => (int) $t['id'], 'card' => 0, 'title' => (string) $t['title'], 'url' => nlf_topic_url( (int) $t['id'] ) );
}

/** the forum home, the place of a home room (the gate opens while the forum is hidden, as nlf_topic_url does), room in the #fragment */
function nlfc_home_room_url( $room = '' ) {
	$u = home_url( '/forum/' );
	if ( function_exists( 'nlf_public' ) && ! nlf_public() ) { $u = add_query_arg( 'forum', 'on', $u ); }
	return $u . ( '' !== $room ? '#call=' . $room : '' );
}

/** the join link of a room in its context */
function nlfc_ctx_link( array $ctx, $room ) {
	if ( ! empty( $ctx['card'] ) ) { return nlfc_card_url( (int) $ctx['card'], $room ); }
	if ( (int) ( $ctx['topic'] ?? 0 ) <= 0 ) { return nlfc_home_room_url( $room ); }
	return nlfc_link( (int) $ctx['topic'], $room );
}

/** the fields every room answer carries: its place, the join link, the size */
function nlfc_room_fields( array $r, array $ctx, $room ) {
	return array( 'room' => $room, 'topic' => (int) $ctx['topic'], 'card' => (int) $ctx['card'], 'title' => (string) $ctx['title'], 'topic_url' => (string) $ctx['url'],
		'link' => nlfc_ctx_link( $ctx, $room ), 'max' => nlfc_room_max( $r ), 'open' => empty( $r['open'] ) ? 0 : 1, 'locked' => empty( $r['lock'] ) ? 0 : 1 );
}

/** the three daily limits of a NEW room (member, hashed IP, the whole forum): '' or the refusal code */
function nlfc_room_limits( $mid ) {
	return nlfc_limits_verdict( array(
		'member' => nlfc_rl_peek( 'room', 'm' . (int) $mid, DAY_IN_SECONDS ),
		'ip'     => nlfc_rl_peek( 'room', nlf_ip_hash(), DAY_IN_SECONDS ),
		'forum'  => nlfc_rl_peek( 'room', 'all', DAY_IN_SECONDS ),
	), array( 'forum' => max( 1, (int) get_option( 'nadlan_forum_call_day_cap', 40 ) ) ) );
}

/** a free room id, or '' */
function nlfc_room_free_id() {
	for ( $i = 0; $i < 4; $i++ ) { $try = nlfc_rand( 12 ); if ( ! nlfc_room_get( $try ) ) { return $try; } }
	return '';
}

/** counts one new room against the three daily limits */
function nlfc_room_hits( $mid ) {
	nlfc_rl_hit( 'room', 'm' . (int) $mid, DAY_IN_SECONDS );
	nlfc_rl_hit( 'room', nlf_ip_hash(), DAY_IN_SECONDS );
	nlfc_rl_hit( 'room', 'all', DAY_IN_SECONDS );
}

/** the people in a room for the call screen (members who took a token): name, label, identity */
function nlfc_room_people( array $r ) {
	$out = array();
	$ok  = isset( $r['ok'] ) && is_array( $r['ok'] ) ? $r['ok'] : array();
	if ( ! $ok ) { return $out; }
	foreach ( nlf_members( array_keys( $ok ) ) as $om ) {
		$idt = (string) ( $ok[ (int) $om['id'] ] ?? '' );
		if ( '' === $idt ) { continue; }
		$f     = nlfc_face( $om );
		$out[] = array( 'id' => $f['id'], 'name' => $f['name'], 'label' => $f['label'], 'identity' => $idt );
	}
	return $out;
}

/** the in-forum notice (polled by call.js) and, only when the member switched it on, one mail. $ctx from nlfc_ctx(). */
function nlfc_invite( $to_member, $from_member, array $ctx, $room ) {
	$k    = 'nlfc_inv_' . (int) $to_member['id'];
	$list = get_transient( $k );
	$list = is_array( $list ) ? $list : array();
	$from = nlfc_face( $from_member );
	$list[] = array( 'room' => $room, 't' => time(), 'topic' => (int) $ctx['topic'], 'card' => (int) $ctx['card'], 'title' => nlfc_line( $ctx['title'], 120 ), 'from' => $from['name'], 'label' => $from['label'] );
	set_transient( $k, nlfc_invites_prune( $list, time() ), 15 * MINUTE_IN_SECONDS );
	$pref = nlfc_prefs( array( (int) $to_member['id'] ) );
	if ( empty( $pref[ (int) $to_member['id'] ]['mail'] ) || '' === (string) $to_member['contact'] ) { return; }
	if ( ! nlfc_rl( 'mail', 'm' . (int) $to_member['id'], 6, DAY_IN_SECONDS ) ) { return; } // a member never gets more than 6 call mails a day
	$stop = add_query_arg( 'nlfc_stop', nlf_link_token( 'cmo', 'm' . (int) $to_member['id'], 0, nlf_key() ), home_url( '/' ) );
	list( $subj, $body ) = nlfc_mail_parts( $from['name'], $ctx['title'], nlfc_ctx_link( $ctx, $room ), $stop, ! empty( $ctx['card'] ) );
	nlf_mail( (string) $to_member['contact'], $subj, $body, $stop );
}

/* =========================================================================================================
 * 5. REST
 * ======================================================================================================= */

add_action( 'rest_api_init', function () {
	$reg = function ( $path, $method, $cb ) {
		register_rest_route( 'nadlan/v1', '/forum/call' . $path, array( 'methods' => $method, 'permission_callback' => '__return_true', 'callback' => $cb, 'show_in_index' => false ) );
	};

	// a new room with a member of the discussion or the member of a card (18.11.2026), or (room given) one more member into my room
	$reg( '/open', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfc_member( $q, true );
		if ( is_wp_error( $m ) ) { return $m; }
		if ( null === nlfc_lk() ) { return nlfc_err( 'off' ); }
		$mid  = (int) $m['id'];
		$card = (int) $q->get_param( 'card' );
		$with = (int) $q->get_param( 'with' );
		$room = (string) $q->get_param( 'room' );
		if ( $card > 0 ) { // from a card: the member behind it, nobody else
			$wm = nlfc_card_member( $card );
			if ( ! $wm ) { return nlfc_err( 'card' ); }
			if ( $with > 0 && $with !== (int) $wm['id'] ) { return nlfc_err( 'with' ); }
			$with = (int) $wm['id'];
			$room = ''; // a card call never joins someone else's room
			$pref = nlfc_prefs( array( $with ) );
			$why  = nlfc_can_reach( $mid, $with, 'ok' === (string) $wm['status'], ! empty( $pref[ $with ]['video'] ), nlfc_rl_peek( 'pair', 'm' . $mid . 'w' . $with, DAY_IN_SECONDS ) );
			if ( '' !== $why ) { return nlfc_err( $why ); }
			$ctx = array( 'topic' => 0, 'card' => $card, 'title' => nlfc_card_title( $card ), 'url' => nlfc_card_url( $card ) );
		} else {
			$t = nlf_topic( (int) $q->get_param( 'topic' ) );
			if ( ! $t ) { return nlfc_err( 'topic' ); }
			$reps = nlfc_replies( (int) $t['id'] );
			$mem  = nlf_members( array( $with ) );
			$wm   = $mem[ $with ] ?? null;
			$pref = nlfc_prefs( array( $with ) );
			$pair = '' === $room ? nlfc_rl_peek( 'pair', 'm' . $mid . 'w' . $with, DAY_IN_SECONDS ) : 0;
			$why  = nlfc_can_call_open( $t, $reps, $mid, $with, array( $with => ! empty( $pref[ $with ]['video'] ) ), array( $with => $wm && 'ok' === (string) $wm['status'] ), $pair );
			if ( '' !== $why ) { return nlfc_err( $why ); }
			$ctx = array( 'topic' => (int) $t['id'], 'card' => 0, 'title' => (string) $t['title'], 'url' => nlf_topic_url( (int) $t['id'] ) );
		}
		if ( '' !== $room ) { // "הזמינו עוד מישהו": into a room I am in, for the same discussion
			$r     = nlfc_room_get( $room );
			$open  = $r && ! empty( $r['open'] );
			if ( ! $r || ! empty( $r['card'] ) || (int) $r['topic'] !== (int) $ctx['topic'] ) { return nlfc_err( 'gone', $open ); }
			if ( ! isset( $r['ok'][ $mid ] ) ) { return nlfc_err( 'notin', $open ); }
			if ( isset( $r['ok'][ $with ] ) ) { return nlfc_err( 'already' ); }
			if ( count( $r['ok'] ) >= nlfc_room_max( $r ) ) { return nlfc_err( 'full', $open ); } // an open room holds 6, a direct call 4
			if ( ! nlfc_rl( 'inv', 'm' . $mid, 20, DAY_IN_SECONDS ) ) { return nlfc_err( 'rate' ); }
			$r['ok'][ $with ] = '';
			nlfc_room_put( $room, $r );
		} else {
			$v = nlfc_room_limits( $mid );
			if ( '' !== $v ) { return nlfc_err( $v ); }
			$room = nlfc_room_free_id();
			if ( '' === $room ) { return nlfc_err( 'rate' ); }
			nlfc_room_hits( $mid );
			nlfc_rl_hit( 'pair', 'm' . $mid . 'w' . $with, DAY_IN_SECONDS ); // at most 3 a day from one caller to the same person
			// ok: member id => LiveKit identity ('' until that member takes a token); by: who opened it; topic OR card (18.11.2026)
			nlfc_room_put( $room, array( 't' => time(), 'topic' => (int) $ctx['topic'], 'card' => (int) $ctx['card'], 'by' => $mid, 'ok' => array( $mid => '', $with => '' ) ) );
		}
		nlfc_invite( $wm, $m, $ctx, $room );
		return nlfc_ok( array( 'room' => $room, 'topic' => (int) $ctx['topic'], 'card' => (int) $ctx['card'], 'title' => (string) $ctx['title'], 'topic_url' => (string) $ctx['url'], 'with' => nlfc_face( $wm ) ) );
	} );

	// my token for a room I belong to; the others' names and trades for the call screen
	$reg( '/token', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfc_member( $q, true );
		if ( is_wp_error( $m ) ) { return $m; }
		$lk = nlfc_lk();
		if ( null === $lk ) { return nlfc_err( 'off' ); }
		$mid  = (int) $m['id'];
		$room = strtolower( (string) $q->get_param( 'room' ) );
		$r    = nlfc_room_get( $room );
		if ( ! $r ) { return nlfc_err( 'gone' ); }
		if ( ! isset( $r['ok'][ $mid ] ) ) { return nlfc_err( 'notin' ); }
		if ( ! nlfc_rl( 'tok', 'm' . $mid, 30, 600 ) ) { return nlfc_err( 'rate' ); }
		$ctx = nlfc_ctx( $r );
		if ( ! $ctx ) { return nlfc_err( ! empty( $r['card'] ) ? 'card' : 'topic' ); }
		$id = (string) $r['ok'][ $mid ];
		if ( 1 !== preg_match( '/^[a-z2-7]{10}$/', $id ) ) { $id = nlfc_rand( 10 ); $r['ok'][ $mid ] = $id; nlfc_room_put( $room, $r ); } // a reconnect keeps its identity
		$me    = nlfc_face( $m );
		$grant = nlfc_grant( $room, $id, $me['name'], (int) $r['by'] === $mid ? 'host' : 'guest', $lk );
		if ( null === $grant || '' === $grant['url'] || '' === $grant['token'] ) { return nlfc_err( 'lk' ); }
		// my notice for this room is answered
		$k    = 'nlfc_inv_' . $mid;
		$list = get_transient( $k );
		if ( is_array( $list ) ) { set_transient( $k, array_values( array_filter( $list, function ( $i ) use ( $room ) { return ( $i['room'] ?? '' ) !== $room; } ) ), 15 * MINUTE_IN_SECONDS ); }
		$others = array();
		foreach ( nlf_members( array_keys( $r['ok'] ) ) as $om ) {
			if ( (int) $om['id'] === $mid ) { continue; }
			$f = nlfc_face( $om );
			$f['identity'] = (string) $r['ok'][ (int) $om['id'] ]; // '' until that member takes a token
			$others[]      = $f; // id is the forum member id the page already prints on its call buttons
		}
		// board 19: open, locked, host, link, max for the open room's screen (the invite sheet and the lock switch)
		return nlfc_ok( array( 'url' => $grant['url'], 'token' => $grant['token'], 'identity' => $id, 'room' => $room, 'topic' => (int) $ctx['topic'], 'card' => (int) $ctx['card'],
			'title' => (string) $ctx['title'], 'topic_url' => (string) $ctx['url'], 'me' => array( 'name' => $me['name'], 'label' => $me['label'] ), 'others' => $others,
			'open' => empty( $r['open'] ) ? 0 : 1, 'locked' => empty( $r['lock'] ) ? 0 : 1, 'host' => (int) $r['by'] === $mid ? 1 : 0, 'link' => nlfc_ctx_link( $ctx, $room ), 'max' => nlfc_room_max( $r ) ) );
	} );

	// the in-forum notification (my invites) and my switches; with ?room=, that room's state for me
	$reg( '/status', 'GET', function ( WP_REST_Request $q ) {
		$m = nlfc_member( $q, false );
		if ( is_wp_error( $m ) ) { return $m; }
		$mid = (int) $m['id'];
		if ( ! nlfc_rl( 'st', 'm' . $mid, 300, HOUR_IN_SECONDS ) ) { return nlfc_err( 'rate' ); }
		$room = strtolower( (string) $q->get_param( 'room' ) );
		if ( '' !== $room ) {
			$r    = nlfc_room_get( $room );
			$open = $r && ! empty( $r['open'] );
			$in   = $r && isset( $r['ok'][ $mid ] );
			if ( ! $r || ( ! $in && ! $open ) ) { return nlfc_ok( array( 'exists' => 0 ) ); } // a direct call stays invisible to anyone not invited
			$ctx = nlfc_ctx( $r );
			$joined = 0;
			foreach ( $r['ok'] as $idt ) { if ( '' !== (string) $idt ) { $joined++; } }
			$by  = nlf_members( array( (int) $r['by'] ) );
			$out = array( 'exists' => $ctx ? 1 : 0, 'joined' => $joined, 'topic' => $ctx ? (int) $ctx['topic'] : 0, 'card' => $ctx ? (int) $ctx['card'] : 0, 'title' => $ctx ? (string) $ctx['title'] : '',
				'topic_url' => $ctx ? (string) $ctx['url'] : '', 'from' => nlfc_face( $by[ (int) $r['by'] ] ?? null ), 'mine' => (int) $r['by'] === $mid ? 1 : 0 );
			if ( $open && $ctx ) { // board 19: an open room, for anyone holding its link
				$out += array( 'open' => 1, 'locked' => empty( $r['lock'] ) ? 0 : 1, 'in' => $in ? 1 : 0, 'max' => nlfc_room_max( $r ), 'full' => count( (array) $r['ok'] ) >= nlfc_room_max( $r ) ? 1 : 0 );
				if ( $in ) { $out['people'] = nlfc_room_people( $r ); } // the names on the call screen, only for those inside
			}
			return nlfc_ok( $out );
		}
		$list = get_transient( 'nlfc_inv_' . $mid );
		$list = nlfc_invites_prune( is_array( $list ) ? $list : array(), time() );
		$out  = array();
		foreach ( $list as $i ) {
			if ( ! nlfc_room_get( (string) $i['room'] ) ) { continue; }
			$card  = (int) ( $i['card'] ?? 0 );
			$out[] = array( 'room' => (string) $i['room'], 'topic' => (int) $i['topic'], 'card' => $card, 'title' => (string) $i['title'], 'from' => (string) $i['from'], 'label' => (string) $i['label'],
				'url' => nlfc_ctx_link( array( 'topic' => (int) $i['topic'], 'card' => $card ), (string) $i['room'] ) );
		}
		$p = nlfc_prefs( array( $mid ) );
		return nlfc_ok( array( 'invites' => $out, 'pref' => $p[ $mid ] ) );
	} );

	// board 19: a new OPEN video room, from the forum home or a card (topic 0) or a live discussion (topic id). Same three daily
	// limits as a new call (member 8, hashed IP 8, forum 40 or the owner's option), counted in the same buckets.
	$reg( '/room', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfc_member( $q, true );
		if ( is_wp_error( $m ) ) { return $m; }
		if ( null === nlfc_lk() ) { return nlfc_err( 'off' ); }
		$mid   = (int) $m['id'];
		$topic = max( 0, (int) $q->get_param( 'topic' ) );
		if ( $topic > 0 ) {
			$t = nlf_topic( $topic );
			if ( ! $t || 'live' !== (string) $t['status'] ) { return nlfc_err( 'topic' ); }
			$topic = (int) $t['id'];
		}
		$v = nlfc_room_limits( $mid );
		if ( '' !== $v ) { return nlfc_err( $v ); }
		$room = nlfc_room_free_id();
		if ( '' === $room ) { return nlfc_err( 'rate' ); }
		$r   = nlfc_room_new_open( $mid, $topic, time() );
		$ctx = nlfc_ctx( $r );
		if ( ! $ctx ) { return nlfc_err( 'topic' ); }
		nlfc_room_hits( $mid );
		nlfc_room_put( $room, $r );
		return nlfc_ok( nlfc_room_fields( $r, $ctx, $room ) );
	} );

	// board 19: come into an open room by its link (a member of the forum in good standing; not locked; at most 6 people)
	$reg( '/join', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfc_member( $q, true );
		if ( is_wp_error( $m ) ) { return $m; }
		if ( null === nlfc_lk() ) { return nlfc_err( 'off' ); }
		$mid  = (int) $m['id'];
		$room = strtolower( (string) $q->get_param( 'room' ) );
		$r    = nlfc_room_get( $room );
		if ( ! $r ) { return nlfc_err( 'gone', true ); }
		$ctx = nlfc_ctx( $r );
		if ( ! $ctx ) { return nlfc_err( 'gone', true ); }
		$why = nlfc_can_join( $r, $mid, nlfc_room_max( $r ) );
		if ( '' !== $why ) { return nlfc_err( $why, true ); }
		if ( ! isset( $r['ok'][ $mid ] ) ) {
			if ( ! nlfc_rl( 'join', 'm' . $mid, 30, DAY_IN_SECONDS ) ) { return nlfc_err( 'rate_join' ); }
			$r['ok'][ $mid ] = '';
			nlfc_room_put( $room, $r );
		}
		return nlfc_ok( nlfc_room_fields( $r, $ctx, $room ) );
	} );

	// board 19: the host locks or opens his open room (nobody new comes in by the link while it is locked)
	$reg( '/lock', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfc_member( $q, true );
		if ( is_wp_error( $m ) ) { return $m; }
		$mid  = (int) $m['id'];
		$room = strtolower( (string) $q->get_param( 'room' ) );
		$r    = nlfc_room_get( $room );
		if ( ! $r || empty( $r['open'] ) ) { return nlfc_err( 'gone', true ); }
		if ( (int) $r['by'] !== $mid ) { return nlfc_err( 'host' ); }
		if ( ! nlfc_rl( 'lock', 'm' . $mid, 60, HOUR_IN_SECONDS ) ) { return nlfc_err( 'rate' ); }
		$r['lock'] = '1' === (string) (int) $q->get_param( 'lock' ) ? 1 : 0;
		nlfc_room_put( $room, $r );
		return nlfc_ok( array( 'room' => $room, 'lock' => (int) $r['lock'] ) );
	} );

	// my own two switches: calls allowed, and the invitation mail
	$reg( '/pref', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfc_member( $q, true );
		if ( is_wp_error( $m ) ) { return $m; }
		if ( ! nlfc_rl( 'pref', 'm' . (int) $m['id'], 60, HOUR_IN_SECONDS ) ) { return nlfc_err( 'rate' ); }
		$cur   = nlfc_prefs( array( (int) $m['id'] ) )[ (int) $m['id'] ];
		$video = null === $q->get_param( 'video' ) ? $cur['video'] : '1' === (string) (int) $q->get_param( 'video' );
		$mail  = null === $q->get_param( 'mail' ) ? $cur['mail'] : '1' === (string) (int) $q->get_param( 'mail' );
		nlfc_pref_set( (int) $m['id'], $video, $mail );
		return nlfc_ok( array( 'pref' => array( 'video' => (bool) $video, 'mail' => (bool) $mail ),
			'message' => $video ? 'אפשר לפנות אליכם בשיחת וידאו מהכרטיס שלכם ומדיון שכתבתם בו.' : 'שיחות וידאו כבויות. פונים אליכם רק בכתב.' ) );
	} );
} );

/* =========================================================================================================
 * 6. The one-click "no more call mails" link (?nlfc_stop=), works with the gate closed; acts at once (harmless)
 * ======================================================================================================= */

add_action( 'template_redirect', function () {
	if ( ! isset( $_GET['nlfc_stop'] ) || is_admin() || ! function_exists( 'nlf_link_read' ) ) { return; } // phpcs:ignore
	$link = nlf_link_read( sanitize_text_field( wp_unslash( $_GET['nlfc_stop'] ) ), time(), nlf_key() ); // phpcs:ignore -- signed token
	if ( ! $link || 'cmo' !== $link[0] || ! preg_match( '/^m(\d+)$/', $link[1], $mm ) ) { return; } // a made-up token shows the normal page
	$GLOBALS['nlf_act_page'] = true; // the forum's style on this page (nlf_surface)
	nlf_nocache();
	$mid  = (int) $mm[1];
	$cur  = nlfc_prefs( array( $mid ) )[ $mid ];
	nlfc_pref_set( $mid, $cur['video'], false );
	status_header( 200 );
	if ( function_exists( 'nlf_shell_open' ) ) { nlf_shell_open(); } else { get_header(); }
	echo '<div class="nlf nlf-page nlf-act" dir="rtl"><h1 class="nlf-h1">' . esc_html( 'לא תקבלו עוד מיילים על שיחות וידאו.' ) . '</h1><p>'
		. esc_html( 'הזמנות לשיחה עדיין יופיעו כשתיכנסו לפורום. אפשר לשנות את זה בכל רגע תחת "שיחות וידאו".' ) . '</p></div>';
	if ( function_exists( 'nlf_shell_close' ) ) { nlf_shell_close(); } else { get_footer(); }
	exit;
}, -99 );

/* =========================================================================================================
 * 7. The page script (forum surfaces only, gate open): call.js as a module + call.css, and the targets of this discussion
 * ======================================================================================================= */

/**
 * The video pills of a discussion page (18.11.2026: next to EVERY answer whose author switched video on, and on the opening
 * message when its author did; for a guest too, whose press asks him to enter first). $me may be null.
 * Each: with, op (the opening message), replies (all his live answers), reply (the newest), name, label.
 */
function nlfc_page_targets( $t, $me ) {
	if ( ! $t || 'live' !== (string) $t['status'] ) { return array(); }
	$reps   = nlfc_replies( (int) $t['id'] );
	$ids    = array_merge( array( (int) $t['member_id'] ), nlfc_repliers( $reps ) );
	$mem    = nlf_members( $ids );
	$prefs  = nlfc_prefs( $ids );
	$video  = array(); $ok = array();
	foreach ( $ids as $i ) { $video[ $i ] = ! empty( $prefs[ $i ]['video'] ); $ok[ $i ] = isset( $mem[ $i ] ) && 'ok' === (string) $mem[ $i ]['status']; }
	$out = array();
	foreach ( nlfc_page_pills( $t, $reps, $me ? (int) $me['id'] : 0, $video, $ok ) as $p ) {
		$f = nlfc_face( $mem[ $p['with'] ] ?? null );
		$out[] = $p + array( 'name' => $f['name'], 'label' => $f['label'] );
	}
	return $out;
}

/* ---------------------------------------------------------------- board 19: the open video room's buttons, printed for guests too */

/** the buttons show only when the module is on and LiveKit is set up (a press must lead to a working room) */
function nlfc_rooms_ready() {
	static $ready = null;
	if ( null === $ready ) { $ready = nlfc_on() && null !== nlfc_lk(); }
	return $ready;
}

/** the camera mark (a constant of this file, never text from a person) */
function nlfc_cam_svg( $size ) {
	$s = (int) $size;
	return '<svg aria-hidden="true" focusable="false" width="' . $s . '" height="' . $s . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/></svg>';
}

/** part א: the band on the forum home, right under the writing row */
function nlfc_room_band_html() {
	$steps = array( 'פותחים חדר', 'שולחים קישור בוואטסאפ', 'מדברים, עד ' . (int) NLFC_ROOM_PEOPLE . ' אנשים' );
	$li    = '';
	foreach ( $steps as $i => $s ) { $li .= '<li><span class="nlfc-rb-n">' . (int) ( $i + 1 ) . '</span><span class="nlfc-rb-s">' . esc_html( $s ) . '</span></li>'; }
	return '<section class="nlfc-roomband" aria-labelledby="nlfc-rb-h" dir="rtl">'
		. '<div class="nlfc-rb-id"><span class="nlfc-rb-mark">' . nlfc_cam_svg( 26 ) . '</span><div class="nlfc-rb-tx"><h2 class="nlfc-rb-h" id="nlfc-rb-h">' . esc_html( 'חדר וידאו' ) . '</h2>'
		. '<p class="nlfc-rb-p">' . esc_html( 'מדברים פנים אל פנים, מראים תוכנית או תמונה ומסמנים עליה יחד.' ) . '</p></div></div>'
		. '<ol class="nlfc-rb-steps">' . $li . '</ol>'
		. '<div class="nlfc-rb-go"><button type="button" class="nlfc-rb-btn" data-nlf-room="0">' . esc_html( 'פתיחת חדר וידאו' ) . '</button>'
		. '<p class="nlfc-rb-fine">' . esc_html( 'בדפדפן, בלי התקנה ובלי תשלום. השיחה לא מוקלטת.' ) . '</p></div>'
		. '</section>';
}

/** part ב: one row, in every live discussion ($topic id) and on every card ($topic 0; never the card owner's name) */
function nlfc_room_row_html( $topic, $title, $sub, $btn ) {
	return '<div class="nlfc-roomrow" dir="rtl"><span class="nlfc-rr-mark">' . nlfc_cam_svg( 22 ) . '</span>'
		. '<div class="nlfc-rr-tx"><span class="nlfc-rr-t">' . esc_html( $title ) . '</span><span class="nlfc-rr-s">' . esc_html( $sub ) . '</span></div>'
		. '<button type="button" class="nlfc-rr-btn" data-nlf-room="' . (int) $topic . '">' . esc_html( $btn ) . '</button></div>';
}

// HOOK nlf_home_after_start (inc/pro-forum-render.php, nlf_render_home): the band, for every visitor
add_filter( 'nlf_home_after_start', function ( $html ) {
	return nlfc_rooms_ready() ? $html . nlfc_room_band_html() : $html;
}, 10, 1 );

// HOOK nlf_topic_after_body (shared with the social module, which runs at 10): the row of a LIVE discussion, after its output
add_filter( 'nlf_topic_after_body', function ( $html, $t ) {
	if ( ! is_array( $t ) || 'live' !== (string) ( $t['status'] ?? '' ) || ! nlfc_rooms_ready() ) { return $html; }
	return $html . nlfc_room_row_html( (int) $t['id'], 'שיחת וידאו על הדיון הזה', 'עם מי שכתב כאן, או עם כל מי שתשלחו לו קישור', 'פתיחה' );
}, 20, 2 );

// HOOK nlf_card_after_mast (inc/pro-forum-render.php, nlf_card_embed): the row on every card, before the tabs. A home room: most
// cards belong to people from public registers who did not join, so the row never names the card's person.
add_filter( 'nlf_card_after_mast', function ( $html ) {
	return nlfc_rooms_ready() ? $html . nlfc_room_row_html( 0, 'חדר וידאו', 'פותחים חדר, שולחים קישור, מדברים ומסמנים על תוכנית יחד', 'פתיחה' ) : $html;
}, 10, 1 );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nlfc_on() || ! function_exists( 'nlf_surface' ) || ! nlf_surface() ) { return; }
	if ( '' === nlf_rendering() && ! empty( $GLOBALS['nlf_act_page'] ) ) { return; } // a one-click page needs no call
	// 1.72.671: handle 'nlf-call' ('nlfc' is facility-chips.php's own handle, registered without a file, so call.css never loaded)
	wp_enqueue_style( 'nlf-call', plugins_url( 'assets/proforum/call.css', dirname( __FILE__ ) ), array(), function_exists( 'nlf_ver' ) ? nlf_ver() : '1' );
}, 31 );

add_action( 'wp_footer', function () {
	if ( ! nlfc_on() || ! function_exists( 'nlf_surface' ) || ! nlf_surface() ) { return; }
	if ( '' === nlf_rendering() && ! empty( $GLOBALS['nlf_act_page'] ) ) { return; }
	$ver = function_exists( 'nlf_ver' ) ? nlf_ver() : '1';
	$me  = nlf_me();
	$t   = 'topic' === nlf_rendering() && isset( $GLOBALS['nlf_topic'] ) ? $GLOBALS['nlf_topic'] : null;
	$cfg = array(
		'rest'    => esc_url_raw( rest_url( 'nadlan/v1/forum/' ) ),
		'lib'     => esc_url_raw( add_query_arg( 'v', $ver, plugins_url( 'assets/designer/call.js', dirname( __FILE__ ) ) ) ),
		'member'  => $me ? 1 : 0,
		'topic'   => $t ? (int) $t['id'] : 0,
		'title'   => $t ? (string) $t['title'] : '',
		'targets' => $t ? nlfc_page_targets( $t, $me ) : array(),
		'card'    => is_singular( 'nadlan_professional' ) ? (int) get_queried_object_id() : 0,
		'photo'   => '', // no forum route accepts an image yet: "צלמו תמונה לבקשה" stays hidden (CALL-NOTES.md)
	);
	echo '<script>window.NLFCALL=' . nlf_json_script( $cfg ) . ';</script>' . "\n"; // phpcs:ignore -- nlf_json_script escapes for a script tag
	echo '<script type="module" src="' . esc_url( add_query_arg( 'v', $ver, plugins_url( 'assets/proforum/call.js', dirname( __FILE__ ) ) ) ) . '"></script>' . "\n"; // phpcs:ignore
}, 25 );
