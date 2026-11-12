<?php
/**
 * nad-lan professionals' forum: the social layer (12.11.2026, Claude Design board 11 "עבודה שסיימתי, פרגון וריאקציות").
 *
 * Loaded by ONE line at the end of inc/pro-forum.php:
 *   if ( file_exists( __DIR__ . '/pro-forum-social.php' ) ) { require_once __DIR__ . '/pro-forum-social.php'; }
 * It edits no forum file. It fills six hook points that inc/pro-forum-render.php offers (each keeps the old output when this
 * file is absent): nlf_topic_actions, nlf_reply_actions, nlf_name_extra, nlf_topic_after_body, nlf_home_notices,
 * nlf_card_member_block. Page script and style: assets/proforum/social.js + social.css (forum.js and forum.css are not touched).
 *
 * What it adds, all keyed on FORUM MEMBERS (a register card whose person did not join is never shown, addressed or counted):
 *  1. Five positive reactions (מפרגן, מועיל, מקצועי, יפה, תודה) on a discussion and on every answer: one per member per item,
 *     changeable, removable. "תודה" stays in the forum's own thanks table (every old thanks row counts, thanks_count is
 *     recounted exactly as the core route does); the other four live in nadlan_forum_react. No negative reaction exists.
 *  2. "לא עזר לי": a private signal on an answer, one per member, never shown as a number (nadlan_forum_unhelpful).
 *  3. פרגון: one member to another, 10 to 240 characters + the relationship, one per pair, only from a member with 2 approved
 *     posts; links and phones refused, live when clean (first-post rules), else waits for the owner; the receiver hides any.
 *  4. Skills: a member with a trade lists up to 5 (2 to 40 characters, reviewed like a first post); others confirm in one tap.
 *  5. "עבודה שסיימתי": the author tags up to 4 other members ("עבדו יחד"); the tagged member sees it in his notices and removes it.
 *  6. "עונה בדרך כלל תוך יום": computed only, 5+ answers in 90 days to discussions he did not open, 80% within 24 hours.
 * REST (nadlan/v1/forum/social/...), every error HTTP 400 with a Hebrew message, every write through nlf_guard (gate, trap,
 * signed form time, proof of work, session, header nonce, member state, the forum's per-IP and per-member ceilings).
 * Tables are created by nlfs_install() once per NLFS_DB (option nadlan_forum_social_db), the same pattern as nlf_install:
 * a failed attempt waits an hour and the forum keeps working without this layer. Nothing is mailed to members; nothing is
 * sent to anyone automatically. No redirects, no robots changes. No long dashes in this file.
 */

if ( ! defined( 'ABSPATH' ) && ! defined( 'NLFS_PURE_ONLY' ) ) { exit; }
if ( defined( 'NLFS_LOADED' ) ) { return; }
define( 'NLFS_LOADED', true );
define( 'NLFS_DB', '1' );

/* =========================================================================================================
 * 1. Pure functions (no WordPress). tests-local/pro-forum-social-test.php loads only this part (NLFS_PURE_ONLY), after the
 *    forum's own pure part (nlf_len, nlf_has_link, nlf_has_phone, nlf_first_post_flag, nlf_dup_key).
 * ======================================================================================================= */

/** kind => array( label, pill background, pill text, dot ) (board 11) */
function nlfs_kinds() {
	return array(
		'pargen' => array( 'מפרגן', '#FBE9F0', '#8C0F3E', '#B0144F' ),
		'useful' => array( 'מועיל', '#DCEFE3', '#1B4D33', '#1B4D33' ),
		'pro'    => array( 'מקצועי', '#DCE6F2', '#1D3B66', '#2F6F86' ),
		'nice'   => array( 'יפה', '#E7E1FA', '#43308F', '#43308F' ),
		'thanks' => array( 'תודה', '#F2F4F5', '#101820', '#5B6770' ),
	);
}

function nlfs_kind_ok( $k ) { return is_string( $k ) && isset( nlfs_kinds()[ $k ] ); }

/** the member's reaction after pressing $pressed while holding $current: the same one again removes it */
function nlfs_react_next( $current, $pressed ) {
	if ( ! nlfs_kind_ok( $pressed ) ) { return ''; }
	return (string) $current === (string) $pressed ? '' : (string) $pressed;
}

/**
 * One map of who reacted how: "type|id" => array( member id => kind ). $thanks: rows (member_id, target_type, target_id) of the
 * forum's thanks table, each one a "תודה"; $reacts: rows of the reactions table with a kind. A member with both (possible only
 * through an old cached page) counts once, with his reaction from the reactions table.
 */
function nlfs_merge( array $thanks, array $reacts ) {
	$out = array();
	foreach ( $thanks as $r ) {
		$out[ (string) $r['target_type'] . '|' . (int) $r['target_id'] ][ (int) $r['member_id'] ] = 'thanks';
	}
	foreach ( $reacts as $r ) {
		if ( ! nlfs_kind_ok( (string) $r['kind'] ) ) { continue; }
		$out[ (string) $r['target_type'] . '|' . (int) $r['target_id'] ][ (int) $r['member_id'] ] = (string) $r['kind'];
	}
	return $out;
}

/** array( member => kind ) to array( total, by => kind => n (most first, board order on a tie), top => up to 3 kinds ) */
function nlfs_summary( array $by_member ) {
	$order = array_keys( nlfs_kinds() );
	$by    = array();
	foreach ( $by_member as $k ) { if ( nlfs_kind_ok( $k ) ) { $by[ $k ] = ( $by[ $k ] ?? 0 ) + 1; } }
	uksort( $by, function ( $a, $b ) use ( $by, $order ) {
		return $by[ $b ] <=> $by[ $a ] ?: array_search( $a, $order, true ) <=> array_search( $b, $order, true );
	} );
	return array( 'total' => array_sum( $by ), 'by' => $by, 'top' => array_slice( array_keys( $by ), 0, 3 ) );
}

/** the words for a screen reader, '' for none ("5: מפרגן 3, מועיל 2") */
function nlfs_summary_words( array $sum ) {
	if ( (int) $sum['total'] < 1 ) { return ''; }
	$k = nlfs_kinds();
	$p = array();
	foreach ( $sum['by'] as $kind => $n ) { $p[] = $k[ $kind ][0] . ' ' . (int) $n; }
	return number_format( (int) $sum['total'] ) . ' פרגונים: ' . implode( ', ', $p );
}

/** relationship key => words (board 11 rules: the relationship is stated) */
function nlfs_rels() { return array( 'together' => 'עבדנו יחד', 'client' => 'הייתי לקוח', 'known' => 'מכיר מקצועית' ); }

/**
 * '' when a פרגון may be written, else the Hebrew message. $c: from, to, approved (the writer's approved posts), to_ok (the
 * receiver is a member in good standing), already (this pair has one).
 */
function nlfs_kudos_error( $text, $rel, array $c ) {
	if ( (int) $c['from'] === (int) $c['to'] ) { return 'אי אפשר לפרגן לעצמכם.'; }
	if ( empty( $c['to_ok'] ) ) { return 'המשתתף הזה לא זמין כרגע.'; }
	if ( (int) $c['approved'] < 2 ) { return 'פרגון אפשר לכתוב אחרי שתי הודעות שאושרו בפורום.'; }
	if ( ! empty( $c['already'] ) ) { return 'כבר פרגנתם לו. פרגון אחד לכל אחד.'; }
	if ( ! isset( nlfs_rels()[ (string) $rel ] ) ) { return 'בחרו איך אתם מכירים.'; }
	$n = nlf_len( $text );
	if ( $n < 10 ) { return 'כתבו משפט, לפחות 10 תווים.'; }
	if ( $n > 240 ) { return 'הפרגון ארוך מדי. עד 240 תווים.'; }
	if ( nlf_has_link( $text ) ) { return 'בפרגון אי אפשר לכתוב קישור או כתובת מייל.'; }
	if ( nlf_has_phone( $text ) ) { return 'בפרגון אי אפשר לכתוב מספר טלפון.'; }
	return '';
}

/** '' = clean; else why the פרגון waits for the owner (the forum's first-post flags, plus words that are not praise) */
function nlfs_kudos_flag( $text ) {
	$f = nlf_first_post_flag( $text );
	if ( '' !== $f ) { return $f; }
	foreach ( array( 'לא ממליץ', 'לא ממליצה', 'להתרחק', 'גרוע', 'נוראי', 'רמאי', 'נוכל', 'שקרן', 'גנב', 'זבל', 'בושה' ) as $w ) {
		if ( false !== strpos( (string) $text, $w ) ) { return 'negative'; }
	}
	return '';
}

/** '' when a skill may be added; $existing = the member's current skill labels (not removed) */
function nlfs_skill_error( $label, array $existing ) {
	$n = nlf_len( $label );
	if ( $n < 2 ) { return 'כתבו מיומנות, לפחות 2 תווים.'; }
	if ( $n > 40 ) { return 'עד 40 תווים למיומנות.'; }
	if ( nlf_has_link( $label ) || nlf_has_phone( $label ) ) { return 'במיומנות אי אפשר לכתוב קישור או מספר טלפון.'; }
	if ( count( $existing ) >= 5 ) { return 'אפשר עד 5 מיומנויות. הסירו אחת כדי להוסיף.'; }
	$key = nlf_dup_key( $label );
	foreach ( $existing as $e ) { if ( hash_equals( nlf_dup_key( $e ), $key ) ) { return 'המיומנות הזאת כבר ברשימה.'; } }
	return '';
}

/** a member "with a trade": linked to a card, or chose a trade from the list */
function nlfs_has_trade( $m ) {
	if ( ! is_array( $m ) ) { return false; }
	return (int) ( $m['pro_id'] ?? 0 ) > 0 || ( 'pro' === (string) ( $m['role_label'] ?? '' ) && '' !== (string) ( $m['trade'] ?? '' ) );
}

/** answers to other people's discussions: array( n, within 24 hours ); $pairs = array( discussion opened (unix), answer (unix) ) */
function nlfs_badge_counts( array $pairs ) {
	$n = 0; $fast = 0;
	foreach ( $pairs as $p ) {
		$n++;
		$d = (int) $p[1] - (int) $p[0];
		if ( $d >= 0 && $d <= 86400 ) { $fast++; }
	}
	return array( $n, $fast );
}

/** earned: at least 5 answers and at least 80 percent of them within a day */
function nlfs_badge_earned( $n, $fast ) { return (int) $n >= 5 && 5 * (int) $fast >= 4 * (int) $n; }

/**
 * '' when the author may tag this member on this discussion. $c: kind, author, me, tagged, tagged_ok (a member in good
 * standing), count (active tags now), state ('' none, 'on', 'off_author', 'off_member').
 */
function nlfs_tag_error( array $c ) {
	if ( 'work' !== (string) $c['kind'] ) { return 'מתייגים רק ב"עבודה שסיימתי".'; }
	if ( (int) $c['author'] !== (int) $c['me'] ) { return 'רק מי שפרסם את העבודה יכול לתייג.'; }
	if ( (int) $c['tagged'] === (int) $c['me'] ) { return 'אי אפשר לתייג את עצמכם.'; }
	if ( empty( $c['tagged_ok'] ) ) { return 'המשתתף הזה לא זמין כרגע.'; }
	if ( 'on' === (string) $c['state'] ) { return 'הוא כבר מתויג.'; }
	if ( 'off_member' === (string) $c['state'] ) { return 'הוא הסיר את התיוג בעצמו.'; }
	if ( (int) $c['count'] >= 4 ) { return 'אפשר לתייג עד 4 אנשים.'; }
	return '';
}

/** the WhatsApp text of a פרגון: the sentence, who about whom, the link */
function nlfs_wa_text( $body, $from, $to, $url ) {
	return '"' . trim( (string) $body ) . '"' . "\n" . trim( (string) $from ) . ' על ' . trim( (string) $to ) . ', בפורום נדל"ן:' . "\n" . (string) $url;
}

/** wa.me with NO phone number: the person picks the recipient himself */
function nlfs_wa_url( $text ) { return 'https://wa.me/?text=' . rawurlencode( (string) $text ); }

/** the first word of a name ("אבי ב." -> "אבי") */
function nlfs_first( $name ) {
	$w = preg_split( '/\s+/u', trim( (string) $name ) );
	return ( $w && '' !== $w[0] ) ? $w[0] : (string) $name;
}

if ( defined( 'NLFS_PURE_ONLY' ) ) { return; }

/* =========================================================================================================
 * 2. Tables (own version, the nlf_install pattern)
 * ======================================================================================================= */

function nlfs_t( $name ) { global $wpdb; return $wpdb->prefix . 'nadlan_forum_' . $name; }

function nlfs_ready() { return NLFS_DB === (string) get_option( 'nadlan_forum_social_db' ); }

/** the six tables once per NLFS_DB; only after the forum's own tables exist; a failed attempt waits an hour */
function nlfs_install() {
	if ( nlfs_ready() || get_transient( 'nlfs_install_wait' ) || ! function_exists( 'nlf_db_ready' ) || ! nlf_db_ready() ) { return; }
	global $wpdb;
	require_once ABSPATH . 'wp-admin/includes/upgrade.php';
	$c = $wpdb->get_charset_collate();
	dbDelta( 'CREATE TABLE ' . nlfs_t( 'react' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		member_id BIGINT UNSIGNED NOT NULL,
		target_type VARCHAR(10) NOT NULL,
		target_id BIGINT UNSIGNED NOT NULL,
		kind VARCHAR(10) NOT NULL,
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY one_react (member_id,target_type,target_id),
		KEY target (target_type,target_id)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlfs_t( 'unhelpful' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		member_id BIGINT UNSIGNED NOT NULL,
		reply_id BIGINT UNSIGNED NOT NULL,
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY one_signal (member_id,reply_id),
		KEY reply_id (reply_id)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlfs_t( 'kudos' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		from_member BIGINT UNSIGNED NOT NULL,
		to_member BIGINT UNSIGNED NOT NULL,
		rel VARCHAR(10) NOT NULL DEFAULT '',
		body VARCHAR(400) NOT NULL DEFAULT '',
		status VARCHAR(10) NOT NULL DEFAULT 'pending',
		to_hidden TINYINT(1) NOT NULL DEFAULT 0,
		ip_hash CHAR(64) NOT NULL DEFAULT '',
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY one_pair (from_member,to_member),
		KEY to_member (to_member,status)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlfs_t( 'skills' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		member_id BIGINT UNSIGNED NOT NULL,
		label VARCHAR(60) NOT NULL DEFAULT '',
		status VARCHAR(10) NOT NULL DEFAULT 'pending',
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		KEY member_id (member_id,status)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlfs_t( 'skillok' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		skill_id BIGINT UNSIGNED NOT NULL,
		member_id BIGINT UNSIGNED NOT NULL,
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY one_ok (skill_id,member_id),
		KEY member_id (member_id)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlfs_t( 'worktags' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		topic_id BIGINT UNSIGNED NOT NULL,
		member_id BIGINT UNSIGNED NOT NULL,
		by_member BIGINT UNSIGNED NOT NULL,
		state VARCHAR(12) NOT NULL DEFAULT 'on',
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY one_tag (topic_id,member_id),
		KEY member_id (member_id,state)
	) $c;" );
	foreach ( array( 'react', 'unhelpful', 'kudos', 'skills', 'skillok', 'worktags' ) as $name ) {
		if ( nlfs_t( $name ) !== (string) $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $wpdb->esc_like( nlfs_t( $name ) ) ) ) ) {
			set_transient( 'nlfs_install_wait', 1, HOUR_IN_SECONDS ); // the version is stored only when every table exists
			return;
		}
	}
	update_option( 'nadlan_forum_social_db', NLFS_DB, true );
}
add_action( 'admin_init', 'nlfs_install', 20 ); // after nlf_install (priority 10)
/* on a forum surface, before the forum page is printed (template_redirect priority 1 prints and exits) */
add_action( 'template_redirect', function () {
	if ( function_exists( 'nlf_rendering' ) && ( '' !== nlf_rendering() || ( is_singular( 'nadlan_professional' ) && nlf_gate_open() ) ) ) { nlfs_install(); }
}, 0 );

/* =========================================================================================================
 * 3. Reading
 * ======================================================================================================= */

/** "type|id" => array( member => kind ) for a discussion and all its answers (two queries, memoised per request) */
function nlfs_thread_map( $tid ) {
	static $memo = array();
	$tid = (int) $tid;
	if ( isset( $memo[ $tid ] ) ) { return $memo[ $tid ]; }
	global $wpdb;
	$rt  = nlf_t( 'replies' );
	$w   = $wpdb->prepare( "(target_type = 'topic' AND target_id = %d) OR (target_type = 'reply' AND target_id IN (SELECT id FROM $rt WHERE topic_id = %d))", $tid, $tid );
	$th  = (array) $wpdb->get_results( 'SELECT member_id, target_type, target_id FROM ' . nlf_t( 'thanks' ) . " WHERE $w", ARRAY_A ); // phpcs:ignore -- prepared above
	$rx  = (array) $wpdb->get_results( 'SELECT member_id, target_type, target_id, kind FROM ' . nlfs_t( 'react' ) . " WHERE $w", ARRAY_A ); // phpcs:ignore
	return $memo[ $tid ] = nlfs_merge( $th, $rx );
}

/** the map of one item, fresh from the tables (after a write) */
function nlfs_item_map( $type, $id ) {
	global $wpdb;
	$th = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT member_id, target_type, target_id FROM ' . nlf_t( 'thanks' ) . ' WHERE target_type = %s AND target_id = %d', $type, (int) $id ), ARRAY_A );
	$rx = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT member_id, target_type, target_id, kind FROM ' . nlfs_t( 'react' ) . ' WHERE target_type = %s AND target_id = %d', $type, (int) $id ), ARRAY_A );
	$m  = nlfs_merge( $th, $rx );
	return $m[ $type . '|' . (int) $id ] ?? array();
}

/** the reply ids this member marked "לא עזר לי" in one discussion (his own view only) */
function nlfs_my_unhelpful( $mid, $tid ) {
	static $memo = array();
	$k = (int) $mid . '|' . (int) $tid;
	if ( isset( $memo[ $k ] ) ) { return $memo[ $k ]; }
	global $wpdb;
	$ids = $wpdb->get_col( $wpdb->prepare( 'SELECT u.reply_id FROM ' . nlfs_t( 'unhelpful' ) . ' u JOIN ' . nlf_t( 'replies' ) . ' r ON r.id = u.reply_id WHERE u.member_id = %d AND r.topic_id = %d', (int) $mid, (int) $tid ) );
	return $memo[ $k ] = array_flip( array_map( 'intval', (array) $ids ) );
}

/** "עונה בדרך כלל תוך יום": computed, cached 6 hours under a key that changes with every new approved post of the member */
function nlfs_badge( $m ) {
	static $memo = array();
	if ( ! is_array( $m ) || 'ok' !== (string) $m['status'] ) { return false; }
	$k = 'nlfs_rb_' . (int) $m['id'] . '_' . (int) $m['approved_posts'];
	if ( isset( $memo[ $k ] ) ) { return $memo[ $k ]; }
	$v = get_transient( $k );
	if ( false === $v ) {
		global $wpdb;
		$rows = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT t.created_at AS tc, r.created_at AS rc FROM ' . nlf_t( 'replies' ) . ' r JOIN ' . nlf_t( 'topics' ) . " t ON t.id = r.topic_id
			WHERE r.member_id = %d AND r.status = 'live' AND t.status = 'live' AND t.member_id <> %d AND r.created_at >= %s", (int) $m['id'], (int) $m['id'], gmdate( 'Y-m-d H:i:s', time() - 90 * DAY_IN_SECONDS ) ), ARRAY_A );
		$pairs = array();
		foreach ( $rows as $r ) { $pairs[] = array( nlf_ts( $r['tc'] ), nlf_ts( $r['rc'] ) ); }
		list( $n, $fast ) = nlfs_badge_counts( $pairs );
		$v = nlfs_badge_earned( $n, $fast ) ? '1' : '0';
		set_transient( $k, $v, 6 * HOUR_IN_SECONDS );
	}
	return $memo[ $k ] = ( '1' === (string) $v );
}

/* a new live answer bumps approved_posts, so the key above changes by itself; this also drops the old entry at once */
add_filter( 'rest_request_after_callbacks', function ( $res, $handler, $req ) {
	if ( $req instanceof WP_REST_Request && '/nadlan/v1/forum/reply' === $req->get_route() && function_exists( 'nlf_me' ) && ! is_wp_error( $res ) ) {
		$m = nlf_me();
		if ( $m ) { delete_transient( 'nlfs_rb_' . (int) $m['id'] . '_' . (int) $m['approved_posts'] ); }
	}
	return $res;
}, 10, 3 );

/** a member who may be shown by id: in good standing and already visible in the forum (an approved post or a linked card) */
function nlfs_visible_member( $m ) {
	return is_array( $m ) && 'ok' === (string) $m['status'] && ( (int) $m['approved_posts'] > 0 || (int) $m['pro_id'] > 0 );
}

function nlfs_member( $id ) {
	$x = nlf_members( array( (int) $id ) );
	return $x ? reset( $x ) : null;
}

/** name, label and tint of a member (a chosen trade gets its group's tint, as in the card's forum) */
function nlfs_face( $m ) {
	$a = function_exists( 'nlf_emb_author' ) ? nlf_emb_author( $m ) : nlf_author( $m );
	return array( 'id' => $m ? (int) $m['id'] : 0, 'name' => (string) $a['name'], 'label' => (string) $a['label'], 'bg' => (string) $a['tint'][0], 'fg' => (string) $a['tint'][1] );
}

/** where a member is shown: his public card, else the forum home with his sheet opened (#nlfs-m<id>) */
function nlfs_member_url( $m ) {
	$pro = (int) $m['pro_id'];
	if ( $pro > 0 && 'publish' === get_post_status( $pro ) && ! nlf_pro_removed( $pro ) ) { return (string) get_permalink( $pro ); }
	$u = home_url( '/forum/' );
	if ( ! nlf_public() ) { $u = add_query_arg( 'forum', 'on', $u ); }
	return $u . '#nlfs-m' . (int) $m['id'];
}

/** the פרגונים shown about a member: live, not hidden by him, from a member in good standing; $with_hidden for his own view */
function nlfs_kudos_for( $mid, $with_hidden = false, $limit = 20 ) {
	global $wpdb;
	return (array) $wpdb->get_results( $wpdb->prepare( 'SELECT k.* FROM ' . nlfs_t( 'kudos' ) . ' k JOIN ' . nlf_t( 'members' ) . " f ON f.id = k.from_member
		WHERE k.to_member = %d AND k.status = 'live' AND f.status = 'ok'" . ( $with_hidden ? '' : ' AND k.to_hidden = 0' ) . ' ORDER BY k.id DESC LIMIT %d', (int) $mid, (int) $limit ), ARRAY_A );
}

/** a member's skills with counts and whether the viewer confirmed each; pending ones only for his own view */
function nlfs_skills_for( $mid, $viewer, $own ) {
	global $wpdb;
	$st   = $own ? "status IN ('live','pending')" : "status = 'live'";
	$rows = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT s.id, s.label, s.status, (SELECT COUNT(*) FROM ' . nlfs_t( 'skillok' ) . ' o JOIN ' . nlf_t( 'members' ) . " om ON om.id = o.member_id AND om.status = 'ok' WHERE o.skill_id = s.id) AS n,
		(SELECT COUNT(*) FROM " . nlfs_t( 'skillok' ) . ' o2 WHERE o2.skill_id = s.id AND o2.member_id = %d) AS mine FROM ' . nlfs_t( 'skills' ) . " s WHERE s.member_id = %d AND s.$st ORDER BY n DESC, s.id ASC LIMIT 5", (int) $viewer, (int) $mid ), ARRAY_A );
	$out = array();
	foreach ( $rows as $r ) { $out[] = array( 'id' => (int) $r['id'], 'label' => (string) $r['label'], 'n' => (int) $r['n'], 'mine' => (int) $r['mine'] > 0, 'status' => (string) $r['status'] ); }
	return $out;
}

/** the reason a viewer cannot write a פרגון to $to right now ('' = may), for the page script's message */
function nlfs_kudos_block( $me, $to ) {
	if ( ! $me ) { return 'guest'; }
	if ( (int) $me['id'] === (int) $to['id'] ) { return 'self'; }
	if ( (int) $me['approved_posts'] < 2 ) { return 'posts'; }
	global $wpdb;
	if ( $wpdb->get_var( $wpdb->prepare( 'SELECT id FROM ' . nlfs_t( 'kudos' ) . ' WHERE from_member = %d AND to_member = %d', (int) $me['id'], (int) $to['id'] ) ) ) { return 'done'; }
	return '';
}

/** one פרגון as data for the page script and for the PHP card */
function nlfs_kudo_data( $k, $mem, $to, $viewer_id ) {
	$fm   = $mem[ (int) $k['from_member'] ] ?? null;
	$from = nlfs_face( $fm );
	$tof  = nlfs_face( $to );
	$rels = nlfs_rels();
	return array( 'id' => (int) $k['id'], 'rel' => $rels[ $k['rel'] ] ?? '', 'text' => (string) $k['body'], 'from' => $from, 'to' => $tof,
		'wa' => nlfs_wa_url( nlfs_wa_text( $k['body'], $from['name'], $tof['name'], nlfs_member_url( $to ) ) ),
		'hidden' => (int) $k['to_hidden'] === 1, 'mine' => (int) $viewer_id === (int) $to['id'] );
}

/* =========================================================================================================
 * 4. HTML (board 11). Every person's text through esc_html / esc_attr.
 * ======================================================================================================= */

function nlfs_check_svg() {
	return '<svg aria-hidden="true" focusable="false" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12l5 5L20 6"/></svg>';
}

/** the stacked dots and the total; '' attribute hidden when nobody reacted (a zero prints nothing) */
function nlfs_sum_html( array $sum ) {
	$k = nlfs_kinds();
	$d = '';
	foreach ( $sum['top'] as $kind ) { $d .= '<i style="background:' . esc_attr( $k[ $kind ][3] ) . '"></i>'; }
	return '<span class="nlfs-sum" data-nlfs-sum' . ( $sum['total'] < 1 ? ' hidden' : '' ) . '><span class="nlfs-dots" aria-hidden="true">' . $d . '</span>'
		. '<span class="nlfs-total" aria-hidden="true">' . ( $sum['total'] > 0 ? esc_html( number_format( (int) $sum['total'] ) ) : '' ) . '</span>'
		. '<span class="nlfs-sr">' . esc_html( nlfs_summary_words( $sum ) ) . '</span></span>';
}

/** the reaction bar of one item: the button, the five pills (board 11), the dots with the total */
function nlfs_rx_html( $type, $id, array $map, $me, $own ) {
	$sum  = nlfs_summary( $map );
	$k    = nlfs_kinds();
	$mid  = $me ? (int) $me['id'] : 0;
	$mine = $mid && isset( $map[ $mid ] ) ? $map[ $mid ] : '';
	$pid  = 'nlfs-pk-' . $type . (int) $id;
	$h    = '<div class="nlfs-rx" data-nlfs-rx="' . esc_attr( $type ) . '" data-id="' . (int) $id . '" data-mine="' . esc_attr( $mine ) . '">';
	if ( ! $own ) {
		$st = $mine ? ' style="--nlfs-bg:' . esc_attr( $k[ $mine ][1] ) . ';--nlfs-fg:' . esc_attr( $k[ $mine ][2] ) . '"' : '';
		$h .= '<button type="button" class="nlf-pill nlfs-rx-btn' . ( $mine ? ' is-on' : '' ) . '"' . $st . ' aria-expanded="false" aria-controls="' . esc_attr( $pid ) . '" data-nlfs-rx-open>'
			. esc_html( $mine ? $k[ $mine ][0] : 'מפרגן' ) . '</button>';
	}
	$h .= nlfs_sum_html( $sum );
	if ( ! $own ) {
		$h .= '<div class="nlfs-pick" id="' . esc_attr( $pid ) . '" role="group" aria-label="בחרו פרגון" hidden>';
		foreach ( $k as $key => $x ) {
			$h .= '<button type="button" data-nlfs-kind="' . esc_attr( $key ) . '" style="--nlfs-bg:' . esc_attr( $x[1] ) . ';--nlfs-fg:' . esc_attr( $x[2] ) . '" aria-pressed="' . ( $mine === $key ? 'true' : 'false' ) . '">' . esc_html( $x[0] ) . '</button>';
		}
		$h .= '</div>';
	}
	return $h . '</div>';
}

add_filter( 'nlf_topic_actions', function ( $html, $t, $me ) {
	if ( ! nlfs_ready() ) { return $html; }
	$map = nlfs_thread_map( (int) $t['id'] );
	return nlfs_rx_html( 'topic', (int) $t['id'], $map[ 'topic|' . (int) $t['id'] ] ?? array(), $me, $me && (int) $me['id'] === (int) $t['member_id'] );
}, 10, 3 );

add_filter( 'nlf_reply_actions', function ( $html, $r, $me, $t = null ) {
	if ( ! nlfs_ready() ) { return $html; }
	$map = nlfs_thread_map( (int) $r['topic_id'] );
	$own = $me && (int) $me['id'] === (int) $r['member_id'];
	$h   = nlfs_rx_html( 'reply', (int) $r['id'], $map[ 'reply|' . (int) $r['id'] ] ?? array(), $me, $own );
	if ( ! $own ) { // private: only this member ever sees his own mark, never a number
		$on = $me && isset( nlfs_my_unhelpful( (int) $me['id'], (int) $r['topic_id'] )[ (int) $r['id'] ] );
		$h .= '<button type="button" class="nlf-pill nlf-mute nlfs-unh' . ( $on ? ' is-on' : '' ) . '" data-nlfs-unhelpful="' . (int) $r['id'] . '" aria-pressed="' . ( $on ? 'true' : 'false' ) . '" aria-describedby="nlfs-unh-note">לא עזר לי</button>';
	}
	return $h;
}, 10, 4 );

/* after the name: the response badge when earned, and the member id the page script uses to open his sheet */
add_filter( 'nlf_name_extra', function ( $html, $m ) {
	if ( ! nlfs_ready() || ! nlfs_visible_member( $m ) ) { return $html; }
	$h = '<span hidden data-nlfs-mid="' . (int) $m['id'] . '"></span>';
	if ( nlfs_badge( $m ) ) { $h .= '<span class="nlfs-badge">' . nlfs_check_svg() . 'עונה בדרך כלל תוך יום</span>'; }
	return $html . $h;
}, 10, 2 );

/* "עבדו יחד" under a finished work (board 11 chips in the member's trade tint); the author tags, the tagged member removes */
add_filter( 'nlf_topic_after_body', function ( $html, $t, $me ) {
	if ( ! nlfs_ready() || 'work' !== (string) $t['kind'] ) { return $html; }
	global $wpdb;
	$rows   = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT member_id FROM ' . nlfs_t( 'worktags' ) . " WHERE topic_id = %d AND state = 'on' ORDER BY id ASC LIMIT 4", (int) $t['id'] ), ARRAY_A );
	$mem    = nlf_members( array_map( function ( $r ) { return (int) $r['member_id']; }, $rows ) );
	$author = $me && (int) $me['id'] === (int) $t['member_id'];
	$chips  = '';
	$n      = 0;
	foreach ( $rows as $r ) {
		$m = $mem[ (int) $r['member_id'] ] ?? null;
		if ( ! $m || 'ok' !== (string) $m['status'] ) { continue; }
		$n++;
		$f  = nlfs_face( $m );
		$tx = $f['name'] . ( '' !== $f['label'] ? ' · ' . $f['label'] : '' );
		$x  = ( $author || ( $me && (int) $me['id'] === (int) $m['id'] ) )
			? '<button type="button" class="nlfs-chip-x" data-nlfs-untag="' . (int) $m['id'] . '" aria-label="' . esc_attr( 'הסרת התיוג של ' . $f['name'] ) . '"><svg aria-hidden="true" focusable="false" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' : '';
		$chips .= '<span class="nlfs-chip" style="--nlfs-bg:' . esc_attr( $f['bg'] ) . ';--nlfs-fg:' . esc_attr( $f['fg'] ) . '"><button type="button" class="nlfs-chip-b" data-nlfs-member="' . (int) $m['id'] . '">' . esc_html( $tx ) . '</button>' . $x . '</span>';
	}
	if ( ! $n && ! $author ) { return $html; }
	$h = '<div class="nlfs-team" data-nlfs-team="' . (int) $t['id'] . '"><div class="nlfs-team-row"><span class="nlfs-team-t">עבדו יחד:</span>' . $chips;
	if ( $author && $n < 4 && 'live' === (string) $t['status'] ) {
		$h .= '<button type="button" class="nlfs-team-add" data-nlfs-tag-open aria-expanded="false" aria-controls="nlfs-find-' . (int) $t['id'] . '">' . ( $n ? '+ עוד מישהו' : '+ תייגו מי שעבד איתכם' ) . '</button>';
	}
	$h .= '</div>';
	if ( $author ) {
		$h .= '<div class="nlfs-find" id="nlfs-find-' . (int) $t['id'] . '" hidden><label for="nlfs-q-' . (int) $t['id'] . '">חפשו לפי שם משתתף בפורום</label>'
			. '<input id="nlfs-q-' . (int) $t['id'] . '" type="search" maxlength="40" autocomplete="off" data-nlfs-find><ul class="nlfs-found" data-nlfs-found></ul>'
			. '<span class="nlf-sub">אפשר לתייג עד 4 משתתפים. מי שתויג רואה את זה אצלו ויכול להסיר.</span></div>';
	}
	return $html . $h . '<p class="nlfs-msg" role="status" aria-live="polite"></p></div>';
}, 10, 3 );

/** a פרגון as board 11's dark card */
function nlfs_kudo_html( array $d, $viewer ) {
	$h = '<article class="nlfs-kudo" data-nlfs-kudo="' . (int) $d['id'] . '"' . ( $d['hidden'] ? ' data-hidden="1"' : '' ) . '>'
		. '<span class="nlfs-kudo-tag">' . esc_html( 'פרגון' . ( '' !== $d['rel'] ? ' · ' . $d['rel'] : '' ) ) . '</span>'
		. '<p class="nlfs-kudo-q">' . esc_html( '"' . $d['text'] . '"' ) . '</p>'
		. '<span class="nlfs-kudo-by">' . esc_html( 'מאת ' . $d['from']['name'] . ( '' !== $d['from']['label'] ? ', ' . $d['from']['label'] : '' ) . ', על ' . $d['to']['name'] . ( '' !== $d['to']['label'] ? ', ' . $d['to']['label'] : '' ) ) . '</span>'
		. '<div class="nlfs-kudo-b"><a class="nlfs-kudo-wa" href="' . esc_url( $d['wa'] ) . '" target="_blank" rel="noopener">שלחו בוואטסאפ</a>';
	if ( $d['mine'] ) {
		$h .= '<button type="button" class="nlfs-kudo-alt" data-nlfs-kudo-hide="' . (int) $d['id'] . '" aria-pressed="' . ( $d['hidden'] ? 'true' : 'false' ) . '">' . ( $d['hidden'] ? 'להחזיר לפרופיל' : 'הסתרה מהפרופיל' ) . '</button>';
	} elseif ( ! $viewer || (int) $viewer['id'] !== (int) $d['from']['id'] ) {
		$h .= '<button type="button" class="nlfs-kudo-alt" data-nlfs-kudos-open="' . (int) $d['to']['id'] . '">גם אני מפרגן</button>';
	}
	return $h . '</div></article>';
}

/** the skills section (board 11): confirm in one tap, the count from 1; his own view lists pending ones and the add box */
function nlfs_skills_html( $m, $skills, $own, $first ) {
	if ( ! $skills && ! ( $own && nlfs_has_trade( $m ) ) ) { return ''; }
	$h = '<section class="nlfs-skills" data-nlfs-skills="' . (int) $m['id'] . '"><h3 class="nlfs-h">' . esc_html( $own ? 'המיומנויות שלי' : 'מכירים את העבודה של ' . $first . '?' ) . '</h3>'
		. '<span class="nlfs-sub">' . esc_html( $own ? 'עד 5 מיומנויות. משתתפים אחרים מאשרים אותן בלחיצה.' : 'אשרו מיומנות אחת בלחיצה. האישור מופיע בפרופיל שלו בפורום.' ) . '</span><div class="nlfs-chips">';
	foreach ( $skills as $s ) {
		$tx = $s['label'] . ( $s['n'] > 0 ? ' · ' . number_format( $s['n'] ) : '' );
		if ( $own ) {
			$h .= '<span class="nlfs-skill is-own">' . esc_html( $tx ) . ( 'pending' === $s['status'] ? '<em>ממתינה לבדיקה</em>' : '' )
				. '<button type="button" class="nlfs-chip-x" data-nlfs-skill-del="' . (int) $s['id'] . '" aria-label="' . esc_attr( 'הסרת ' . $s['label'] ) . '"><svg aria-hidden="true" focusable="false" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button></span>';
		} else {
			$h .= '<button type="button" class="nlfs-skill' . ( $s['mine'] ? ' is-on' : '' ) . '" data-nlfs-endorse="' . (int) $s['id'] . '" data-label="' . esc_attr( $s['label'] ) . '" aria-pressed="' . ( $s['mine'] ? 'true' : 'false' ) . '">'
				. ( $s['mine'] ? nlfs_check_svg() : '' ) . '<span>' . esc_html( $tx ) . '</span></button>';
		}
	}
	$h .= '</div>';
	if ( $own && count( $skills ) < 5 ) {
		$h .= '<form class="nlfs-skill-add" data-nlfs-skill-add novalidate><label class="nlfs-sr" for="nlfs-sk-' . (int) $m['id'] . '">מיומנות חדשה</label>'
			. '<input id="nlfs-sk-' . (int) $m['id'] . '" type="text" name="label" maxlength="40" placeholder="למשל: שמאות לבנק" autocomplete="off"><button type="submit" class="nlf-btn nlf-btn-line">הוספה</button>'
			. nlf_trap() . '</form>';
	}
	return $h . '<p class="nlfs-msg" role="status" aria-live="polite"></p></section>';
}

/** the member's block inside the professional card window: badge, פרגונים, skills (only for a JOINED member) */
function nlfs_member_block( $m ) {
	if ( ! nlfs_visible_member( $m ) ) { return ''; }
	$me    = nlf_me();
	$own   = $me && (int) $me['id'] === (int) $m['id'];
	$face  = nlfs_face( $m );
	$first = nlfs_first( $face['name'] );
	$rows  = nlfs_kudos_for( (int) $m['id'], false, 3 );
	$all_n = 0;
	if ( $rows ) {
		global $wpdb;
		$all_n = (int) $wpdb->get_var( $wpdb->prepare( 'SELECT COUNT(*) FROM ' . nlfs_t( 'kudos' ) . ' k JOIN ' . nlf_t( 'members' ) . " f ON f.id = k.from_member WHERE k.to_member = %d AND k.status = 'live' AND k.to_hidden = 0 AND f.status = 'ok'", (int) $m['id'] ) );
	}
	$mem   = nlf_members( array_map( function ( $k ) { return (int) $k['from_member']; }, $rows ) );
	$h     = '<div class="nlfs-mb" data-nlfs-mb="' . (int) $m['id'] . '">';
	if ( nlfs_badge( $m ) ) { $h .= '<span class="nlfs-badge nlfs-badge-lg">' . nlfs_check_svg() . 'עונה בדרך כלל תוך יום</span>'; }
	foreach ( array_slice( $rows, 0, 2 ) as $k ) { $h .= nlfs_kudo_html( nlfs_kudo_data( $k, $mem, $m, $me ? (int) $me['id'] : 0 ), $me ); }
	if ( $all_n > 2 ) {
		$h .= '<button type="button" class="nlf-link nlfs-all" data-nlfs-member="' . (int) $m['id'] . '">' . esc_html( 'כל ' . number_format( $all_n ) . ' הפרגונים' ) . '</button>';
	}
	if ( ! $rows && ! $own ) {
		$h .= '<div class="nlfs-cta"><span>' . esc_html( 'מכירים את העבודה של ' . $first . '?' ) . '</span><button type="button" class="nlf-btn nlf-btn-line" data-nlfs-kudos-open="' . (int) $m['id'] . '">' . esc_html( 'פרגנו ל' . $first ) . '</button></div>';
	}
	if ( $own ) {
		$h .= '<button type="button" class="nlf-link nlfs-all" data-nlfs-member="' . (int) $m['id'] . '">הפרגונים עליי</button>';
	}
	$h .= nlfs_skills_html( $m, nlfs_skills_for( (int) $m['id'], $me ? (int) $me['id'] : 0, $own ), $own, $first );
	return $h . '</div>';
}

add_filter( 'nlf_card_member_block', function ( $html, $m, $pro ) {
	if ( ! nlfs_ready() || ! is_array( $m ) ) { return $html; }
	return $html . nlfs_member_block( $m );
}, 10, 3 );

/* the member's own notices on the forum home: tags on finished works, new פרגונים about him, and his own forum profile */
add_filter( 'nlf_home_notices', function ( $html, $me ) {
	if ( ! nlfs_ready() || ! $me ) { return $html; }
	global $wpdb;
	$since = gmdate( 'Y-m-d H:i:s', time() - 60 * DAY_IN_SECONDS );
	$tags  = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT w.topic_id, w.by_member, t.title FROM ' . nlfs_t( 'worktags' ) . ' w JOIN ' . nlf_t( 'topics' ) . " t ON t.id = w.topic_id
		WHERE w.member_id = %d AND w.state = 'on' AND t.status = 'live' AND w.created_at >= %s ORDER BY w.id DESC LIMIT 5", (int) $me['id'], $since ), ARRAY_A );
	$kud   = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT k.id, k.from_member FROM ' . nlfs_t( 'kudos' ) . ' k JOIN ' . nlf_t( 'members' ) . " f ON f.id = k.from_member
		WHERE k.to_member = %d AND k.status = 'live' AND f.status = 'ok' AND k.created_at >= %s ORDER BY k.id DESC LIMIT 3", (int) $me['id'], gmdate( 'Y-m-d H:i:s', time() - 30 * DAY_IN_SECONDS ) ), ARRAY_A );
	$ids   = array();
	foreach ( $tags as $r ) { $ids[] = (int) $r['by_member']; }
	foreach ( $kud as $r ) { $ids[] = (int) $r['from_member']; }
	$mem   = nlf_members( $ids );
	$items = '';
	foreach ( $tags as $r ) {
		$by = nlfs_face( $mem[ (int) $r['by_member'] ] ?? null );
		$items .= '<li data-nlfs-team="' . (int) $r['topic_id'] . '"><span>' . esc_html( $by['name'] . ' תייג אתכם ב"עבודה שסיימתי": ' ) . '<a href="' . esc_url( home_url( '/forum/' . (int) $r['topic_id'] . '/' ) ) . '">' . esc_html( nlf_excerpt( $r['title'], 70 ) ) . '</a></span>'
			. '<button type="button" class="nlf-link" data-nlfs-untag="' . (int) $me['id'] . '">הסרת התיוג</button><p class="nlfs-msg" role="status" aria-live="polite"></p></li>';
	}
	foreach ( $kud as $r ) {
		$by = nlfs_face( $mem[ (int) $r['from_member'] ] ?? null );
		$items .= '<li><span>' . esc_html( $by['name'] . ' פרגן לכם.' ) . '</span><button type="button" class="nlf-link" data-nlfs-member="' . (int) $me['id'] . '">לקריאה</button></li>';
	}
	$h = '<div class="nlfs-notes">';
	if ( '' !== $items ) { $h .= '<h2 class="nlfs-notes-h">אצלכם בפורום</h2><ul>' . $items . '</ul>'; }
	return $html . $h . '<button type="button" class="nlf-link nlfs-mine" data-nlfs-member="' . (int) $me['id'] . '">הפרופיל שלי בפורום</button></div>';
}, 10, 2 );

/* =========================================================================================================
 * 5. Assets and the member sheet (forum surfaces only)
 * ======================================================================================================= */

function nlfs_surface() {
	if ( ! function_exists( 'nlf_surface' ) || ! nlfs_ready() ) { return false; }
	if ( '' === nlf_rendering() && ! empty( $GLOBALS['nlf_act_page'] ) ) { return false; } // a one-click page needs none of this
	return nlf_surface();
}

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nlfs_surface() ) { return; }
	$base = plugins_url( 'assets/proforum/', dirname( __FILE__ ) );
	$ver  = function_exists( 'nlf_ver' ) ? nlf_ver() : '1';
	wp_enqueue_style( 'nlf-social', $base . 'social.css', array( 'nlf' ), $ver );
	wp_enqueue_script( 'nlf-social', $base . 'social.js', array( 'nlf' ), $ver, true );
	wp_add_inline_script( 'nlf-social', 'window.NLFS=' . nlf_json_script( array( 'kinds' => nlfs_kinds(), 'rels' => nlfs_rels() ) ) . ';', 'before' );
}, 32 );

add_action( 'wp_footer', function () {
	if ( ! nlfs_surface() || ( '' === nlf_rendering() && empty( $GLOBALS['nlf_card_printed'] ) ) ) { return; }
	?>
<p class="nlfs-sr" id="nlfs-unh-note">רק אתם רואים את הסימון הזה. הוא עוזר לנו לסדר את התשובות.</p>
<dialog class="nlf nlf-sheet nlfs-sheet" id="nlfs-member" dir="rtl" aria-labelledby="nlfs-m-h">
	<div class="nlf-sheet-h"><button type="button" class="nlf-ico" data-nlf-close aria-label="סגירה"><?php echo nlf_svg( 'close' ); // phpcs:ignore ?></button><h2 class="nlf-h2" id="nlfs-m-h">פרופיל בפורום</h2></div>
	<div class="nlfs-body" data-nlfs-body></div>
	<form class="nlf-form nlfs-kform" data-nlfs-kudosform novalidate hidden>
		<h3 class="nlfs-h" data-nlfs-kh>פרגון</h3>
		<fieldset class="nlf-radios nlf-radios-col"><legend>איך אתם מכירים?</legend>
			<?php foreach ( nlfs_rels() as $k => $l ) : ?><label><input type="radio" name="rel" value="<?php echo esc_attr( $k ); ?>"> <?php echo esc_html( $l ); ?></label><?php endforeach; ?>
		</fieldset>
		<div class="nlf-field"><label for="nlfs-k-body">משפט אחד של פרגון</label><textarea id="nlfs-k-body" name="body" rows="3" maxlength="240" placeholder="מה היה טוב בעבודה איתו"></textarea><span class="nlf-sub" data-nlfs-kcount aria-live="polite"></span></div>
		<?php echo nlf_trap(); // phpcs:ignore ?>
		<button type="submit" class="nlf-btn nlf-btn-hot nlf-btn-big">פרסום הפרגון</button>
		<p class="nlf-sub nlf-center">פרגון חיובי בלבד, אחד לכל אחד. בלי קישורים ובלי טלפון. מי שקיבל אותו יכול להסתיר.</p>
	</form>
	<p class="nlf-msg" data-nlfs-sheetmsg role="status" aria-live="polite"></p>
</dialog>
	<?php
}, 6 ); // before the footer scripts (forum.js wires every dialog.nlf when it runs)

/* =========================================================================================================
 * 6. REST: nadlan/v1/forum/social/...
 * ======================================================================================================= */

/** nlf_guard plus this layer's tables; the member row or a WP_Error 400 */
function nlfs_guard( WP_REST_Request $q, $kind ) {
	if ( ! function_exists( 'nlf_guard' ) ) { return new WP_Error( 'nlfs_off', 'הפעולה לא זמינה כרגע.', array( 'status' => 400 ) ); }
	$m = nlf_guard( $q, $kind );
	if ( is_wp_error( $m ) ) { return $m; }
	nlfs_install();
	if ( ! nlfs_ready() ) { return nlf_err( 'הפעולה לא זמינה כרגע. נסו שוב בעוד כמה דקות.' ); }
	return $m;
}

/** a pending פרגון or skill: one mail to the owner with one-click approve / reject (a press on the page does it) */
function nlfs_mail_pending( $what, $id, $text, $m ) {
	$tok  = ( 'kudos' === $what ? 'k' : 's' ) . (int) $id;
	$link = function ( $a ) use ( $tok ) { return add_query_arg( 'nlfs_act', nlf_link_token( $a, $tok, time() + 14 * DAY_IN_SECONDS, nlf_key() ), home_url( '/' ) ); };
	$body = ( 'kudos' === $what ? 'פרגון' : 'מיומנות' ) . " חדש מחכה לבדיקה.\n\nמאת: " . $m['display_name'] . ' (' . $m['contact'] . ")\n\n" . nlf_excerpt( $text, 400 ) . "\n\n"
		. 'אישור: ' . $link( 'ok' ) . "\nדחייה: " . $link( 'no' ) . "\n";
	nlf_mail( nlf_admin_to(), '[פורום] ' . ( 'kudos' === $what ? 'פרגון' : 'מיומנות' ) . ' מחכה לבדיקה', $body );
}

add_action( 'rest_api_init', function () {
	$reg = function ( $path, $method, $cb ) {
		register_rest_route( 'nadlan/v1', '/forum/social/' . $path, array( 'methods' => $method, 'permission_callback' => '__return_true', 'callback' => $cb, 'show_in_index' => false ) );
	};

	// one of the five reactions; the same one again removes it
	$reg( 'react', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfs_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		$type = 'reply' === (string) $q->get_param( 'type' ) ? 'reply' : 'topic';
		$id   = (int) $q->get_param( 'id' );
		$kind = sanitize_key( (string) $q->get_param( 'kind' ) );
		if ( ! nlfs_kind_ok( $kind ) ) { return nlf_err( 'בחרו פרגון.' ); }
		$row = 'topic' === $type ? nlf_topic( $id ) : nlf_reply( $id );
		if ( ! $row || 'live' !== $row['status'] ) { return nlf_err( 'ההודעה לא נמצאה.' ); }
		if ( 'reply' === $type ) { $tp = nlf_topic( (int) $row['topic_id'] ); if ( ! $tp || 'live' !== $tp['status'] ) { return nlf_err( 'ההודעה לא נמצאה.' ); } }
		if ( (int) $row['member_id'] === (int) $m['id'] ) { return nlf_err( 'אי אפשר לפרגן לעצמכם.' ); }
		global $wpdb;
		$tt   = nlf_t( 'thanks' ); $rt = nlfs_t( 'react' );
		$map  = nlfs_item_map( $type, $id );
		$next = nlfs_react_next( $map[ (int) $m['id'] ] ?? '', $kind );
		$wpdb->delete( $tt, array( 'member_id' => (int) $m['id'], 'target_type' => $type, 'target_id' => $id ) );
		$wpdb->delete( $rt, array( 'member_id' => (int) $m['id'], 'target_type' => $type, 'target_id' => $id ) );
		if ( 'thanks' === $next ) { // "תודה" stays in the forum's own thanks table: every old row keeps counting
			$wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO $tt (member_id, target_type, target_id) VALUES (%d, %s, %d)", (int) $m['id'], $type, $id ) );
		} elseif ( '' !== $next ) {
			$wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO $rt (member_id, target_type, target_id, kind, created_at) VALUES (%d, %s, %d, %s, %s)", (int) $m['id'], $type, $id, $next, nlf_now_sql() ) );
		}
		// thanks_count exactly as the core route counts it (the rows of the thanks table), for every code that reads it
		$n = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $tt WHERE target_type = %s AND target_id = %d", $type, $id ) );
		$wpdb->update( nlf_t( 'topic' === $type ? 'topics' : 'replies' ), array( 'thanks_count' => $n ), array( 'id' => $id ) );
		$sum = nlfs_summary( nlfs_item_map( $type, $id ) );
		return nlf_ok( array( 'mine' => $next, 'total' => (int) $sum['total'], 'top' => $sum['top'], 'words' => nlfs_summary_words( $sum ) ) );
	} );

	// "לא עזר לי": private, one per member per answer, a toggle; never counted on screen
	$reg( 'unhelpful', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfs_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		$r = nlf_reply( (int) $q->get_param( 'id' ) );
		if ( ! $r || 'live' !== $r['status'] ) { return nlf_err( 'התשובה לא נמצאה.' ); }
		if ( (int) $r['member_id'] === (int) $m['id'] ) { return nlf_err( 'זו התשובה שלכם.' ); }
		global $wpdb;
		$ut  = nlfs_t( 'unhelpful' );
		$has = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $ut WHERE member_id = %d AND reply_id = %d", (int) $m['id'], (int) $r['id'] ) );
		if ( $has ) { $wpdb->delete( $ut, array( 'id' => $has ) ); }
		else { $wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO $ut (member_id, reply_id, created_at) VALUES (%d, %d, %s)", (int) $m['id'], (int) $r['id'], nlf_now_sql() ) ); }
		return nlf_ok( array( 'on' => $has ? 0 : 1, 'message' => $has ? 'הסימון הוסר.' : 'נרשם. רק אתם רואים את הסימון הזה.' ) );
	} );

	// a member's sheet: name, badge, פרגונים, skills, and what the viewer may do
	$reg( 'member', 'GET', function ( WP_REST_Request $q ) {
		$g = nlfs_guard( $q, 'view' );
		if ( is_wp_error( $g ) ) { return $g; }
		$m  = nlfs_member( (int) $q->get_param( 'id' ) );
		$me = nlf_me();
		$own = $me && $m && (int) $me['id'] === (int) $m['id'];
		if ( ! $m || ! ( nlfs_visible_member( $m ) || ( $own && 'ok' === (string) $m['status'] ) ) ) { return nlf_err( 'המשתתף לא נמצא.' ); }
		$face = nlfs_face( $m );
		$rows = nlfs_kudos_for( (int) $m['id'], $own, 20 );
		$mem  = nlf_members( array_map( function ( $k ) { return (int) $k['from_member']; }, $rows ) );
		$kud  = array();
		foreach ( $rows as $k ) { $kud[] = nlfs_kudo_data( $k, $mem, $m, $me ? (int) $me['id'] : 0 ); }
		return nlf_ok( array(
			'member' => array( 'id' => $face['id'], 'name' => $face['name'], 'first' => nlfs_first( $face['name'] ), 'label' => $face['label'], 'bg' => $face['bg'], 'fg' => $face['fg'],
				'badge' => nlfs_badge( $m ), 'url' => nlfs_member_url( $m ), 'trade' => nlfs_has_trade( $m ) ),
			'own'    => $own ? 1 : 0,
			'viewer' => $me ? (int) $me['id'] : 0,
			'block'  => $own ? 'self' : nlfs_kudos_block( $me, $m ),
			'kudos'  => $kud,
			'skills' => nlfs_skills_for( (int) $m['id'], $me ? (int) $me['id'] : 0, $own ),
		) );
	} );

	// write a פרגון
	$reg( 'kudos', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfs_guard( $q, 'post' );
		if ( is_wp_error( $m ) ) { return $m; }
		$to   = nlfs_member( (int) $q->get_param( 'to' ) );
		$rel  = sanitize_key( (string) $q->get_param( 'rel' ) );
		$text = nlf_text_norm( (string) $q->get_param( 'body' ), true );
		global $wpdb;
		$kt  = nlfs_t( 'kudos' );
		$e   = nlfs_kudos_error( $text, $rel, array( 'from' => (int) $m['id'], 'to' => $to ? (int) $to['id'] : 0, 'approved' => (int) $m['approved_posts'],
			'to_ok' => nlfs_visible_member( $to ), 'already' => $to && $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $kt WHERE from_member = %d AND to_member = %d", (int) $m['id'], (int) $to['id'] ) ) ) );
		if ( '' !== $e ) { return nlf_err( $e ); }
		if ( ! nlf_rl( 'kudos', 10, DAY_IN_SECONDS, 'm' . (int) $m['id'] ) ) { return nlf_err( 'כתבתם היום הרבה פרגונים. אפשר להמשיך מחר.' ); }
		$auto   = '0' !== (string) get_option( 'nadlan_forum_autoapprove', '1' );
		$status = ( $auto && '' === nlfs_kudos_flag( $text ) ) ? 'live' : 'pending';
		$ok = $wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO $kt (from_member, to_member, rel, body, status, to_hidden, ip_hash, created_at) VALUES (%d, %d, %s, %s, %s, 0, %s, %s)",
			(int) $m['id'], (int) $to['id'], $rel, $text, $status, nlf_ip_hash(), nlf_now_sql() ) );
		$id = (int) $wpdb->insert_id;
		if ( ! $ok || $id <= 0 ) { return nlf_err( 'כבר פרגנתם לו. פרגון אחד לכל אחד.' ); }
		nlf_write_counted( $m );
		if ( 'pending' === $status ) { nlfs_mail_pending( 'kudos', $id, $text, $m ); }
		return nlf_ok( array( 'id' => $id, 'status' => $status, 'message' => 'live' === $status ? 'הפרגון פורסם. תודה שפרגנתם.' : 'הפרגון יעלה אחרי בדיקה קצרה.' ) );
	} );

	// the receiver hides a פרגון about himself, or shows it again
	$reg( 'kudos-hide', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfs_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		global $wpdb;
		$kt = nlfs_t( 'kudos' );
		$k  = $wpdb->get_row( $wpdb->prepare( "SELECT * FROM $kt WHERE id = %d", (int) $q->get_param( 'id' ) ), ARRAY_A );
		if ( ! $k || (int) $k['to_member'] !== (int) $m['id'] ) { return nlf_err( 'רק מי שקיבל את הפרגון יכול להסתיר אותו.' ); }
		$hide = '1' === (string) $q->get_param( 'hide' );
		$wpdb->update( $kt, array( 'to_hidden' => $hide ? 1 : 0 ), array( 'id' => (int) $k['id'] ) );
		return nlf_ok( array( 'hidden' => $hide ? 1 : 0, 'message' => $hide ? 'הפרגון הוסתר מהפרופיל שלכם.' : 'הפרגון חזר לפרופיל שלכם.' ) );
	} );

	// add one of my skills (a member with a trade, up to 5)
	$reg( 'skill', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfs_guard( $q, 'post' );
		if ( is_wp_error( $m ) ) { return $m; }
		if ( ! nlfs_has_trade( $m ) ) { return nlf_err( 'מיומנויות מוסיף בעל מקצוע שבחר תחום.' ); }
		$label = nlf_text_norm( (string) $q->get_param( 'label' ), true );
		global $wpdb;
		$st  = nlfs_t( 'skills' );
		$cur = (array) $wpdb->get_col( $wpdb->prepare( "SELECT label FROM $st WHERE member_id = %d AND status IN ('live','pending')", (int) $m['id'] ) );
		$e   = nlfs_skill_error( $label, $cur );
		if ( '' !== $e ) { return nlf_err( $e ); }
		$status = nlf_first_status( 0, $label, '0' !== (string) get_option( 'nadlan_forum_autoapprove', '1' ) ); // reviewed like a first post
		$wpdb->insert( $st, array( 'member_id' => (int) $m['id'], 'label' => $label, 'status' => $status, 'created_at' => nlf_now_sql() ) );
		$id = (int) $wpdb->insert_id;
		if ( $id <= 0 ) { return nlf_err( 'משהו השתבש. נסו שוב.' ); }
		nlf_write_counted( $m );
		if ( 'pending' === $status ) { nlfs_mail_pending( 'skill', $id, $label, $m ); }
		return nlf_ok( array( 'id' => $id, 'status' => $status, 'message' => 'live' === $status ? 'המיומנות נוספה.' : 'המיומנות תופיע אחרי בדיקה קצרה.' ) );
	} );

	// remove one of my skills (and its confirmations)
	$reg( 'skill-remove', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfs_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		global $wpdb;
		$id = (int) $q->get_param( 'id' );
		$s  = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlfs_t( 'skills' ) . ' WHERE id = %d', $id ), ARRAY_A );
		if ( ! $s || (int) $s['member_id'] !== (int) $m['id'] ) { return nlf_err( 'המיומנות לא נמצאה.' ); }
		$wpdb->delete( nlfs_t( 'skillok' ), array( 'skill_id' => $id ) );
		$wpdb->delete( nlfs_t( 'skills' ), array( 'id' => $id ) );
		return nlf_ok( array( 'message' => 'המיומנות הוסרה.' ) );
	} );

	// confirm someone else's skill in one tap (a toggle); never your own
	$reg( 'endorse', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfs_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		global $wpdb;
		$s = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlfs_t( 'skills' ) . " WHERE id = %d AND status = 'live'", (int) $q->get_param( 'id' ) ), ARRAY_A );
		$owner = $s ? nlfs_member( (int) $s['member_id'] ) : null;
		if ( ! $s || ! nlfs_visible_member( $owner ) ) { return nlf_err( 'המיומנות לא נמצאה.' ); }
		if ( (int) $s['member_id'] === (int) $m['id'] ) { return nlf_err( 'אי אפשר לאשר מיומנות של עצמכם.' ); }
		if ( (int) $m['approved_posts'] < 1 ) { return nlf_err( 'אישור מיומנות אפשר אחרי הודעה אחת שאושרה בפורום.' ); }
		$ot  = nlfs_t( 'skillok' );
		$has = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $ot WHERE skill_id = %d AND member_id = %d", (int) $s['id'], (int) $m['id'] ) );
		if ( $has ) { $wpdb->delete( $ot, array( 'id' => $has ) ); }
		else { $wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO $ot (skill_id, member_id, created_at) VALUES (%d, %d, %s)", (int) $s['id'], (int) $m['id'], nlf_now_sql() ) ); }
		$n = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $ot o JOIN " . nlf_t( 'members' ) . " om ON om.id = o.member_id AND om.status = 'ok' WHERE o.skill_id = %d", (int) $s['id'] ) );
		return nlf_ok( array( 'on' => $has ? 0 : 1, 'n' => $n ) );
	} );

	// find a member by name to tag on a finished work (signed-in members only; visible members only; at most 8)
	$reg( 'find', 'GET', function ( WP_REST_Request $q ) {
		$g = nlfs_guard( $q, 'view' );
		if ( is_wp_error( $g ) ) { return $g; }
		$me = nlf_me();
		if ( ! $me ) { return nlf_err( 'כדי לתייג צריך להיכנס.', 'nlf_need_entry' ); }
		if ( ! nlf_rl( 'nlfs_find', 120, HOUR_IN_SECONDS, 'm' . (int) $me['id'] ) ) { return nlf_err( 'נסו שוב מאוחר יותר.' ); }
		$s = nlf_text_norm( (string) $q->get_param( 'q' ), true );
		if ( nlf_len( $s ) < 2 ) { return nlf_ok( array( 'items' => array() ) ); }
		global $wpdb;
		$rows = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlf_t( 'members' ) . " WHERE status = 'ok' AND id <> %d AND (approved_posts > 0 OR pro_id IS NOT NULL) AND display_name LIKE %s ORDER BY last_seen DESC LIMIT 8",
			(int) $me['id'], '%' . $wpdb->esc_like( mb_substr( $s, 0, 40 ) ) . '%' ), ARRAY_A );
		$out = array();
		foreach ( $rows as $r ) { $f = nlfs_face( $r ); $out[] = array( 'id' => $f['id'], 'name' => $f['name'], 'label' => $f['label'] ); }
		return nlf_ok( array( 'items' => $out ) );
	} );

	// tag a member on my finished work
	$reg( 'tag', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfs_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		$t = nlf_topic( (int) $q->get_param( 'topic' ) );
		if ( ! $t || 'live' !== $t['status'] ) { return nlf_err( 'הדיון לא נמצא.' ); }
		$who = nlfs_member( (int) $q->get_param( 'member' ) );
		global $wpdb;
		$wt  = nlfs_t( 'worktags' );
		$cur = $who ? (string) $wpdb->get_var( $wpdb->prepare( "SELECT state FROM $wt WHERE topic_id = %d AND member_id = %d", (int) $t['id'], (int) $who['id'] ) ) : '';
		$e   = nlfs_tag_error( array( 'kind' => $t['kind'], 'author' => (int) $t['member_id'], 'me' => (int) $m['id'], 'tagged' => $who ? (int) $who['id'] : 0,
			'tagged_ok' => nlfs_visible_member( $who ), 'state' => $cur,
			'count' => (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $wt WHERE topic_id = %d AND state = 'on'", (int) $t['id'] ) ) ) );
		if ( '' !== $e ) { return nlf_err( $e ); }
		if ( '' === $cur ) {
			$wpdb->insert( $wt, array( 'topic_id' => (int) $t['id'], 'member_id' => (int) $who['id'], 'by_member' => (int) $m['id'], 'state' => 'on', 'created_at' => nlf_now_sql() ) );
		} else {
			$wpdb->update( $wt, array( 'state' => 'on', 'created_at' => nlf_now_sql() ), array( 'topic_id' => (int) $t['id'], 'member_id' => (int) $who['id'] ) );
		}
		$f = nlfs_face( $who );
		return nlf_ok( array( 'member' => array( 'id' => $f['id'], 'name' => $f['name'], 'label' => $f['label'], 'bg' => $f['bg'], 'fg' => $f['fg'] ), 'message' => 'התיוג נוסף. ' . $f['name'] . ' יראה אותו אצלו בפורום.' ) );
	} );

	// remove a tag: the author removes anyone, the tagged member removes himself (and then cannot be tagged there again)
	$reg( 'untag', 'POST', function ( WP_REST_Request $q ) {
		$m = nlfs_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		$t   = nlf_topic( (int) $q->get_param( 'topic' ) );
		$who = (int) $q->get_param( 'member' );
		if ( ! $t ) { return nlf_err( 'הדיון לא נמצא.' ); }
		$self = $who === (int) $m['id'];
		if ( ! $self && (int) $t['member_id'] !== (int) $m['id'] ) { return nlf_err( 'רק מי שפרסם את העבודה או מי שתויג יכולים להסיר.' ); }
		global $wpdb;
		$wpdb->update( nlfs_t( 'worktags' ), array( 'state' => $self ? 'off_member' : 'off_author' ), array( 'topic_id' => (int) $t['id'], 'member_id' => $who ) );
		return nlf_ok( array( 'message' => 'התיוג הוסר.' ) );
	} );
} );

/* =========================================================================================================
 * 7. One-click approve / reject for a pending פרגון or skill (?nlfs_act=, signed, 14 days; a press on the page does it,
 *    because mail scanners open links by themselves). Same pattern as the forum's ?nlf_act=.
 * ======================================================================================================= */

add_action( 'template_redirect', function () {
	if ( ! isset( $_GET['nlfs_act'] ) || is_admin() || ! function_exists( 'nlf_link_read' ) ) { return; } // phpcs:ignore
	$tok  = sanitize_text_field( wp_unslash( $_GET['nlfs_act'] ) ); // phpcs:ignore -- signed token, checked below
	$link = nlf_link_read( $tok, time(), nlf_key() );
	if ( ! $link || ! in_array( $link[0], array( 'ok', 'no' ), true ) || ! preg_match( '/^([ks])(\d+)$/', $link[1], $mm ) ) { return; } // a made-up token shows the normal page
	$GLOBALS['nlf_act_page'] = true;
	nlf_nocache();
	nlfs_install();
	global $wpdb;
	$tab = 'k' === $mm[1] ? nlfs_t( 'kudos' ) : nlfs_t( 'skills' );
	$row = nlfs_ready() ? $wpdb->get_row( $wpdb->prepare( "SELECT * FROM $tab WHERE id = %d", (int) $mm[2] ), ARRAY_A ) : null;
	$ok  = 'ok' === $link[0];
	$body = '';
	if ( ! $row ) {
		$h = 'הפריט לא נמצא.';
	} elseif ( 'pending' !== $row['status'] ) {
		$h = 'הפריט כבר טופל.';
	} elseif ( 'POST' === ( $_SERVER['REQUEST_METHOD'] ?? '' ) && isset( $_POST['nlfs_confirm'] ) ) { // phpcs:ignore -- the signed token is the authority
		$wpdb->update( $tab, array( 'status' => $ok ? 'live' : 'removed' ), array( 'id' => (int) $row['id'] ) );
		$h = $ok ? 'אושר ועלה לפורום.' : 'נדחה.';
	} else {
		$h    = $ok ? 'אישור' : 'דחייה';
		$body = '<blockquote class="nlf-quote">' . esc_html( 'k' === $mm[1] ? $row['body'] : $row['label'] ) . '</blockquote>'
			. '<form method="post" action="' . esc_url( add_query_arg( 'nlfs_act', $tok, home_url( '/' ) ) ) . '"><input type="hidden" name="nlfs_confirm" value="1">'
			. '<button type="submit" class="nlf-btn ' . ( $ok ? 'nlf-btn-fill' : 'nlf-btn-danger' ) . ' nlf-btn-big">' . ( $ok ? 'אישור' : 'דחייה' ) . '</button></form>';
	}
	status_header( 200 );
	nlf_shell_open();
	echo '<div class="nlf nlf-page nlf-act" dir="rtl"><h1 class="nlf-h1">' . esc_html( $h ) . '</h1>' . $body . '</div>'; // phpcs:ignore -- escaped parts
	nlf_shell_close();
	exit;
}, -98 );
