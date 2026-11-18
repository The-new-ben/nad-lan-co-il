<?php
/**
 * nad-lan professionals' forum: reputation (18.11.2026, Claude Design board 20 "כוכבים ודרגות",
 * docs/design-lab/pro-forum/canvas-source/Reputation.dc.html, parts א to ה).
 *
 * Loaded by ONE line at the end of inc/pro-forum.php, after the card module:
 *   if ( file_exists( __DIR__ . '/pro-forum-rep.php' ) ) { require_once __DIR__ . '/pro-forum-rep.php'; }
 * It edits no forum file and creates no table: points are COUNTED from rows that already exist (topics, replies, members,
 * thanks, and the social layer's react, kudos, skills, skillok, worktags). It fills hooks that inc/pro-forum-render.php offers:
 *   nlf_name_extra (15, after the social badge)  the stars chip after every author name in a discussion        (part א)
 *   nlf_home_after_start (20, after the video band)  "המובילים החודש", or a compact invitation               (part ג)
 *   nlf_member_bar_extra (20)  "הכוכבים שלי" in the member's own bar                                           (part ה)
 *   nlf_home_notices (1)  the dark level-up notice, once                                                      (part ה)
 *   nlf_card_member_block (5)  the chip of a joined member on his card                                        (part א)
 * Page script and style: assets/proforum/rep.js + rep.css. The member's sheet (part ב) and the rules (part ד) are two
 * dialogs printed in the footer; the rules are real HTML in the page source.
 * REST: GET nadlan/v1/forum/rep/member?id= (nlf_guard 'view': the forum gate and the per-IP read ceiling). Nothing private.
 *
 * The rules are printed to the public, so nlfr_weights() / nlfr_levels() / nlfr_gate() / nlfr_post_cap() are the ONE source:
 * the PHP counts with them, the rules dialog prints them, and the page script reads them as JSON (window.NLFR).
 * Members whose status is not 'ok' and fixture members (contact ending '@example.invalid') give nothing, get nothing and
 * never appear. A member's own actions never count. No points are ever negative. No long dashes in this file.
 */

if ( ! defined( 'ABSPATH' ) && ! defined( 'NLFR_PURE_ONLY' ) ) { exit; }
if ( defined( 'NLFR_LOADED' ) ) { return; }
define( 'NLFR_LOADED', true );
define( 'NLFR_VER', '1' ); // part of every cache key: bump it when a rule changes
define( 'NLFR_FIXTURE', '@example.invalid' );

/* =========================================================================================================
 * 1. Pure functions (no WordPress). tests-local/pro-forum-rep-test.php loads only this part (NLFR_PURE_ONLY), after the
 *    forum's own pure part.
 * ======================================================================================================= */

/** points per counted event (board 20, part ד) */
function nlfr_weights() {
	return array( 'helped' => 15, 'kudos' => 10, 'together' => 10, 'skills' => 3, 'reacts' => 2, 'posts' => 1 );
}

/** answers + discussions that count per calendar day */
function nlfr_post_cap() { return 5; }

/** level 5 also needs this many different askers who marked a helped answer, and this many days since joining */
function nlfr_gate() { return array( 'askers' => 5, 'days' => 90 ); }

/** the levels, named after building stages; n = stars */
function nlfr_levels() {
	return array(
		array( 'n' => 0, 'min' => 0, 'name' => 'חדש בזירה' ),
		array( 'n' => 1, 'min' => 10, 'name' => 'יסודות' ),
		array( 'n' => 2, 'min' => 50, 'name' => 'שלד' ),
		array( 'n' => 3, 'min' => 150, 'name' => 'גמר' ),
		array( 'n' => 4, 'min' => 400, 'name' => 'מסירה' ),
		array( 'n' => 5, 'min' => 1000, 'name' => 'מפתח' ),
	);
}

function nlfr_max_stars() { $l = nlfr_levels(); return (int) end( $l )['n']; }

/** the six counts with every key present, never negative */
function nlfr_counts_norm( array $c ) {
	$out = array();
	foreach ( array_keys( nlfr_weights() ) as $k ) { $out[ $k ] = max( 0, (int) ( $c[ $k ] ?? 0 ) ); }
	return $out;
}

/** lifetime points from the six counts (helped, kudos, together, skills, reacts, posts) */
function nlfr_points( array $counts ) {
	$p = 0;
	$c = nlfr_counts_norm( $counts );
	foreach ( nlfr_weights() as $k => $w ) { $p += $w * $c[ $k ]; }
	return max( 0, $p );
}

/** the level row for these points; the top level also needs the two gates, else the member stays one below */
function nlfr_level( $points, $helped_askers, $days ) {
	$all = nlfr_levels();
	$lv  = $all[0];
	foreach ( $all as $row ) { if ( (int) $points >= $row['min'] ) { $lv = $row; } }
	$g = nlfr_gate();
	if ( $lv['n'] === nlfr_max_stars() && ( (int) $helped_askers < $g['askers'] || (int) $days < $g['days'] ) ) {
		$lv = $all[ count( $all ) - 2 ];
	}
	return $lv;
}

/**
 * The way to the next level: next (name, '' at the top), missing points, pct 0..100 inside the current level, and for a member
 * who has the points of the top level but not its gates: need_askers and need_days.
 */
function nlfr_progress( $points, $helped_askers, $days ) {
	$points = max( 0, (int) $points );
	$all    = nlfr_levels();
	$lv     = nlfr_level( $points, $helped_askers, $days );
	$next   = $all[ $lv['n'] + 1 ] ?? null;
	$out    = array( 'next' => '', 'next_n' => 0, 'missing' => 0, 'pct' => 100, 'need_askers' => 0, 'need_days' => 0 );
	if ( ! $next ) { return $out; }
	$out['next']    = $next['name'];
	$out['next_n']  = $next['n'];
	$out['missing'] = max( 0, $next['min'] - $points );
	$span           = $next['min'] - $lv['min'];
	$out['pct']     = $span > 0 ? (int) max( 0, min( 100, round( ( $points - $lv['min'] ) * 100 / $span ) ) ) : 100;
	if ( 0 === $out['missing'] ) { // the points are there; a gate holds the member back
		$g = nlfr_gate();
		$out['need_askers'] = max( 0, $g['askers'] - (int) $helped_askers );
		$out['need_days']   = max( 0, $g['days'] - (int) $days );
	}
	return $out;
}

/** "★★★" (the glyphs only; colour and aria-hidden are the caller's) */
function nlfr_stars_text( $n ) { return str_repeat( '★', max( 0, min( nlfr_max_stars(), (int) $n ) ) ); }

function nlfr_num( $n ) { return number_format( (int) $n ); }

function nlfr_points_words( $n ) { return 1 === (int) $n ? 'נקודה אחת' : nlfr_num( $n ) . ' נקודות'; }

/** the chip's accessible name: "דרגת גמר, 3 מתוך 5 כוכבים, 212 נקודות" */
function nlfr_chip_label( array $lv, $points ) {
	return 'דרגת ' . $lv['name'] . ', ' . (int) $lv['n'] . ' מתוך ' . nlfr_max_stars() . ' כוכבים, ' . nlfr_points_words( $points );
}

/** the line under the progress bar in the sheet */
function nlfr_progress_text( array $p ) {
	if ( '' === $p['next'] ) { return 'הדרגה הגבוהה בפורום'; }
	if ( $p['missing'] > 0 ) { return 'עוד ' . nlfr_points_words( $p['missing'] ) . ' לדרגת ' . $p['next']; }
	if ( $p['need_askers'] > 0 ) {
		return 'לדרגת ' . $p['next'] . ' חסרות עוד ' . ( 1 === $p['need_askers'] ? 'תשובה אחת' : nlfr_num( $p['need_askers'] ) . ' תשובות' ) . ' "עזרה לי" משואלים שונים';
	}
	return 'דרגת ' . $p['next'] . ' בעוד ' . ( 1 === $p['need_days'] ? 'יום אחד' : nlfr_num( $p['need_days'] ) . ' ימים' ) . ' בפורום';
}

/** the short form in the member's bar: "עוד 88 לגמר" ('' at the top) */
function nlfr_progress_short( array $p ) {
	if ( '' === $p['next'] ) { return ''; }
	if ( $p['missing'] > 0 ) { return 'עוד ' . nlfr_num( $p['missing'] ) . ' ל' . $p['next']; }
	if ( $p['need_askers'] > 0 ) { return 'ל' . $p['next'] . ': עוד ' . nlfr_num( $p['need_askers'] ) . ' שואלים'; }
	return 'ל' . $p['next'] . ': עוד ' . nlfr_num( $p['need_days'] ) . ' ימים';
}

/** "שני כוכבים" for the level-up notice */
function nlfr_star_words( $n ) {
	$w = array( 1 => 'כוכב אחד', 2 => 'שני כוכבים', 3 => 'שלושה כוכבים', 4 => 'ארבעה כוכבים', 5 => 'חמישה כוכבים' );
	return $w[ (int) $n ] ?? nlfr_num( $n ) . ' כוכבים';
}

/** a sample or test member: his contact ends with @example.invalid */
function nlfr_is_fixture( $contact ) {
	$c = strtolower( trim( (string) $contact ) );
	return '' !== $c && substr( $c, -strlen( NLFR_FIXTURE ) ) === NLFR_FIXTURE;
}

/** out of the whole system: no row, a status that is not 'ok', or a fixture member */
function nlfr_excluded( $m ) {
	return ! is_array( $m ) || 'ok' !== (string) ( $m['status'] ?? '' ) || nlfr_is_fixture( $m['contact'] ?? '' );
}

/**
 * Reactions that count: one per giver per calendar day. $rows: array( giver, day ) (a reaction from the reactions table and a
 * thanks row are both rows; a giver with both on the same day counts once). The member's own reactions never count.
 */
function nlfr_count_reacts( array $rows, $member_id = 0 ) {
	$seen = array();
	foreach ( $rows as $r ) {
		$g = (int) ( $r['giver'] ?? 0 );
		$d = (string) ( $r['day'] ?? '' );
		if ( $g <= 0 || '' === $d || $g === (int) $member_id ) { continue; }
		$seen[ $g . '|' . $d ] = true;
	}
	return count( $seen );
}

/** answers and discussions that count: per calendar day at most nlfr_post_cap(); $rows: array( day, n ) (n defaults to 1) */
function nlfr_count_posts( array $rows ) {
	$by = array();
	foreach ( $rows as $r ) {
		$d = (string) ( $r['day'] ?? '' );
		if ( '' === $d ) { continue; }
		$by[ $d ] = ( $by[ $d ] ?? 0 ) + max( 0, (int) ( $r['n'] ?? 1 ) );
	}
	$n = 0;
	foreach ( $by as $x ) { $n += min( nlfr_post_cap(), $x ); }
	return $n;
}

/** the level-up decision: show the notice or not, and what to store. Nothing stored yet = store silently (an existing member). */
function nlfr_levelup( $stored, $current ) {
	$current = (int) $current;
	if ( null === $stored || '' === $stored ) { return array( 'show' => false, 'store' => $current ); }
	$stored = (int) $stored;
	if ( $current > $stored ) { return array( 'show' => true, 'store' => $current ); }
	if ( $current < $stored ) { return array( 'show' => false, 'store' => $current ); } // a removed message can take points away
	return array( 'show' => false, 'store' => null );
}

/** the rows of the member's sheet (part ב, board order); the skills row only when it has a count, so the rows add up */
function nlfr_breakdown( array $counts ) {
	$c = nlfr_counts_norm( $counts );
	$w = nlfr_weights();
	$l = array(
		'helped'   => 'תשובות שהשואל סימן "עזרה לי"',
		'reacts'   => 'תגובות חיוביות מחברים אחרים',
		'kudos'    => 'פרגונים',
		'together' => '"עבדו יחד" שאושר',
		'posts'    => 'תשובות ודיונים שכתב',
		'skills'   => 'מיומנויות שחברים אישרו',
	);
	$out = array();
	foreach ( $l as $k => $label ) {
		if ( 'skills' === $k && 0 === $c[ $k ] ) { continue; }
		$out[] = array( 'key' => $k, 'label' => $label, 'n' => $c[ $k ], 'pts' => $c[ $k ] * $w[ $k ] );
	}
	return $out;
}

/** the point rows of the public rules (part ד); a פרגון and "עבדו יחד" share a row while they weigh the same */
function nlfr_rule_rows() {
	$w = nlfr_weights();
	$r = array( array( 'השואל סימן את התשובה שלכם "עזרה לי"', $w['helped'] ) );
	if ( $w['kudos'] === $w['together'] ) {
		$r[] = array( 'פרגון מחבר אחר, או "עבדו יחד" שאושר', $w['kudos'] );
	} else {
		$r[] = array( 'פרגון מחבר אחר', $w['kudos'] );
		$r[] = array( '"עבדו יחד" שאושר', $w['together'] );
	}
	$r[] = array( 'חבר אישר מיומנות שלכם', $w['skills'] );
	$r[] = array( 'תגובה חיובית על הודעה שלכם (אחת ביום מכל חבר)', $w['reacts'] );
	$r[] = array( 'תשובה שכתבתם, או דיון שפתחתם וקיבל תשובה (עד ' . nlfr_post_cap() . ' ביום)', $w['posts'] );
	usort( $r, function ( $a, $b ) { return $b[1] <=> $a[1]; } );
	return $r;
}

/** the fine line under the rules */
function nlfr_rules_fine() {
	$g    = nlfr_gate();
	$l    = nlfr_levels();
	$top  = end( $l )['name'];
	$from = 5 === $g['askers'] ? 'מחמישה' : 'מ-' . nlfr_num( $g['askers'] );
	return 'לדרגת ' . $top . ' צריך גם ' . nlfr_num( $g['askers'] ) . ' תשובות שסומנו "עזרה לי" ' . $from . ' שואלים שונים, ו-' . nlfr_num( $g['days'] ) . ' יום בפורום. תגובה של אדם על עצמו לא נספרת.';
}

/** "נובמבר 2026" */
function nlfr_month_he( $ts ) {
	if ( (int) $ts <= 0 ) { return ''; }
	$m = array( 1 => 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר' );
	return $m[ (int) gmdate( 'n', (int) $ts ) ] . ' ' . gmdate( 'Y', (int) $ts );
}

/** the leaders' order: points, then helped answers, then the older member */
function nlfr_leader_sort( array $rows ) {
	usort( $rows, function ( $a, $b ) { return $b['points'] <=> $a['points'] ?: $b['helped'] <=> $a['helped'] ?: $a['id'] <=> $b['id']; } );
	return $rows;
}

if ( defined( 'NLFR_PURE_ONLY' ) ) { return; }

/* =========================================================================================================
 * 2. Counting (grouped SQL, one batch for any number of members; no N+1)
 * ======================================================================================================= */

function nlfr_social_ready() { return function_exists( 'nlfs_ready' ) && nlfs_ready() && function_exists( 'nlfs_t' ); }

/** seconds to add to a stored UTC time to get the site's calendar day */
function nlfr_tz_offset() { return (int) round( (float) get_option( 'gmt_offset', 0 ) * HOUR_IN_SECONDS ); }

/**
 * The raw counts per member. $ids: member ids (cast to int here) or null for every member (the leaders);
 * $since: '' for lifetime, else a UTC 'Y-m-d H:i:s' (events at or after it). Returns mid => array( six counts, helped_askers ).
 * Every giver is a real member (status 'ok', not a fixture) and never the receiver. Seven queries at most, each grouped.
 */
function nlfr_query_counts( $ids, $since = '' ) {
	global $wpdb;
	if ( is_array( $ids ) ) {
		$ids = array_values( array_unique( array_filter( array_map( 'intval', $ids ) ) ) );
		if ( ! $ids ) { return array(); }
	}
	$in  = function ( $col ) use ( $ids ) { return is_array( $ids ) ? ' AND ' . $col . ' IN (' . implode( ',', $ids ) . ')' : ''; }; // ints only
	$sn  = function ( $col, array &$args ) use ( $since ) { if ( '' === $since ) { return ''; } $args[] = $since; return ' AND ' . $col . ' >= %s'; };
	$rl  = function ( $a, array &$args ) use ( $wpdb ) { $args[] = '%' . $wpdb->esc_like( NLFR_FIXTURE ); return " AND $a.status = 'ok' AND $a.contact NOT LIKE %s"; };
	$off = nlfr_tz_offset();
	$rt  = nlf_t( 'replies' ); $tt = nlf_t( 'topics' ); $mt = nlf_t( 'members' ); $ht = nlf_t( 'thanks' );
	$out = array();
	$put = function ( $mid, $k, $v ) use ( &$out ) {
		$mid = (int) $mid;
		if ( ! isset( $out[ $mid ] ) ) { $out[ $mid ] = array( 'helped' => 0, 'kudos' => 0, 'together' => 0, 'skills' => 0, 'reacts' => 0, 'posts' => 0, 'helped_askers' => 0 ); }
		$out[ $mid ][ $k ] = (int) $v;
	};

	// 1. helped: my live answer is the solved answer of a live discussion opened by someone else (a real member)
	$a = array();
	$q = "SELECT r.member_id AS mid, COUNT(*) AS n, COUNT(DISTINCT t.member_id) AS askers
		FROM $rt r
		JOIN $tt t ON t.id = r.topic_id AND t.solved_reply_id = r.id
		JOIN $mt a ON a.id = t.member_id
		WHERE r.status = 'live' AND t.status = 'live' AND t.member_id <> r.member_id" . $rl( 'a', $a ) . $in( 'r.member_id' ) . $sn( 'r.created_at', $a ) . '
		GROUP BY r.member_id';
	foreach ( (array) $wpdb->get_results( $wpdb->prepare( $q, $a ), ARRAY_A ) as $r ) { $put( $r['mid'], 'helped', $r['n'] ); $put( $r['mid'], 'helped_askers', $r['askers'] ); } // phpcs:ignore -- prepared

	// 6. posts: my live answers (in a live discussion), and my live discussions with a live answer by another real member
	$a  = array( $off );
	$q1 = "SELECT r.member_id AS mid, DATE(DATE_ADD(r.created_at, INTERVAL %d SECOND)) AS d
		FROM $rt r JOIN $tt t ON t.id = r.topic_id
		WHERE r.status = 'live' AND t.status = 'live'" . $in( 'r.member_id' ) . $sn( 'r.created_at', $a );
	$a[] = $off;
	$q2 = "SELECT t.member_id AS mid, DATE(DATE_ADD(t.created_at, INTERVAL %d SECOND)) AS d
		FROM $tt t
		WHERE t.status = 'live'" . $in( 't.member_id' ) . $sn( 't.created_at', $a ) . "
		AND EXISTS (SELECT 1 FROM $rt r2 JOIN $mt o ON o.id = r2.member_id WHERE r2.topic_id = t.id AND r2.status = 'live' AND r2.member_id <> t.member_id" . $rl( 'o', $a ) . ')';
	$posts = array();
	foreach ( (array) $wpdb->get_results( $wpdb->prepare( "SELECT p.mid, p.d, COUNT(*) AS n FROM ($q1 UNION ALL $q2) p GROUP BY p.mid, p.d", $a ), ARRAY_A ) as $r ) { // phpcs:ignore -- prepared
		$posts[ (int) $r['mid'] ][] = array( 'day' => (string) $r['d'], 'n' => (int) $r['n'] );
	}
	foreach ( $posts as $mid => $rows ) { $put( $mid, 'posts', nlfr_count_posts( $rows ) ); }

	// 5. reactions: distinct (receiver, giver, day) over the social reactions table and the core thanks table. A thanks row has no
	//    time of its own, so it is dated by the message it thanks.
	$a  = array();
	$br = array();
	if ( nlfr_social_ready() ) {
		$xt   = nlfs_t( 'react' );
		$a[]  = $off;
		$br[] = "SELECT r.member_id AS mid, e.member_id AS giver, DATE(DATE_ADD(e.created_at, INTERVAL %d SECOND)) AS d
			FROM $rt r JOIN $tt t ON t.id = r.topic_id JOIN $xt e ON e.target_type = 'reply' AND e.target_id = r.id
			WHERE r.status = 'live' AND t.status = 'live'" . $in( 'r.member_id' ) . $sn( 'e.created_at', $a );
		$a[]  = $off;
		$br[] = "SELECT t.member_id AS mid, e.member_id AS giver, DATE(DATE_ADD(e.created_at, INTERVAL %d SECOND)) AS d
			FROM $tt t JOIN $xt e ON e.target_type = 'topic' AND e.target_id = t.id
			WHERE t.status = 'live'" . $in( 't.member_id' ) . $sn( 'e.created_at', $a );
	}
	$a[]  = $off;
	$br[] = "SELECT r.member_id AS mid, h.member_id AS giver, DATE(DATE_ADD(r.created_at, INTERVAL %d SECOND)) AS d
		FROM $rt r JOIN $tt t ON t.id = r.topic_id JOIN $ht h ON h.target_type = 'reply' AND h.target_id = r.id
		WHERE r.status = 'live' AND t.status = 'live'" . $in( 'r.member_id' ) . $sn( 'r.created_at', $a );
	$a[]  = $off;
	$br[] = "SELECT t.member_id AS mid, h.member_id AS giver, DATE(DATE_ADD(t.created_at, INTERVAL %d SECOND)) AS d
		FROM $tt t JOIN $ht h ON h.target_type = 'topic' AND h.target_id = t.id
		WHERE t.status = 'live'" . $in( 't.member_id' ) . $sn( 't.created_at', $a );
	$q = 'SELECT DISTINCT x.mid, x.giver, x.d FROM (' . implode( ' UNION ALL ', $br ) . ") x JOIN $mt g ON g.id = x.giver WHERE x.giver <> x.mid" . $rl( 'g', $a );
	$reacts = array();
	foreach ( (array) $wpdb->get_results( $wpdb->prepare( $q, $a ), ARRAY_A ) as $r ) { // phpcs:ignore -- prepared
		$reacts[ (int) $r['mid'] ][] = array( 'giver' => (int) $r['giver'], 'day' => (string) $r['d'] );
	}
	foreach ( $reacts as $mid => $rows ) { $put( $mid, 'reacts', nlfr_count_reacts( $rows, $mid ) ); }

	if ( nlfr_social_ready() ) {
		$kt = nlfs_t( 'kudos' ); $wt = nlfs_t( 'worktags' ); $st = nlfs_t( 'skills' ); $ot = nlfs_t( 'skillok' );

		// 2. kudos: live, from a real member who is not me
		$a = array();
		$q = "SELECT k.to_member AS mid, COUNT(*) AS n
			FROM $kt k JOIN $mt f ON f.id = k.from_member
			WHERE k.status = 'live' AND k.from_member <> k.to_member" . $rl( 'f', $a ) . $in( 'k.to_member' ) . $sn( 'k.created_at', $a ) . '
			GROUP BY k.to_member';
		foreach ( (array) $wpdb->get_results( $wpdb->prepare( $q, $a ), ARRAY_A ) as $r ) { $put( $r['mid'], 'kudos', $r['n'] ); } // phpcs:ignore -- prepared

		// 3. together: an active "עבדו יחד" tag on me, by another real member, on a live discussion
		$a = array();
		$q = "SELECT w.member_id AS mid, COUNT(*) AS n
			FROM $wt w JOIN $tt t ON t.id = w.topic_id JOIN $mt b ON b.id = w.by_member
			WHERE w.state = 'on' AND t.status = 'live' AND w.by_member <> w.member_id" . $rl( 'b', $a ) . $in( 'w.member_id' ) . $sn( 'w.created_at', $a ) . '
			GROUP BY w.member_id';
		foreach ( (array) $wpdb->get_results( $wpdb->prepare( $q, $a ), ARRAY_A ) as $r ) { $put( $r['mid'], 'together', $r['n'] ); } // phpcs:ignore -- prepared

		// 4. skills: a confirmation of one of my live skills by another real member
		$a = array();
		$q = "SELECT s.member_id AS mid, COUNT(*) AS n
			FROM $st s JOIN $ot o ON o.skill_id = s.id JOIN $mt c ON c.id = o.member_id
			WHERE s.status = 'live' AND o.member_id <> s.member_id" . $rl( 'c', $a ) . $in( 's.member_id' ) . $sn( 'o.created_at', $a ) . '
			GROUP BY s.member_id';
		foreach ( (array) $wpdb->get_results( $wpdb->prepare( $q, $a ), ARRAY_A ) as $r ) { $put( $r['mid'], 'skills', $r['n'] ); } // phpcs:ignore -- prepared
	}
	return $out;
}

/** one member's full result from his row and his raw counts */
function nlfr_result( $m, array $raw ) {
	$counts = nlfr_counts_norm( $raw );
	$askers = (int) ( $raw['helped_askers'] ?? 0 );
	$joined = function_exists( 'nlf_ts' ) ? nlf_ts( $m['created_at'] ?? '' ) : 0;
	$days   = $joined > 0 ? (int) floor( ( time() - $joined ) / DAY_IN_SECONDS ) : 0;
	$points = nlfr_points( $counts );
	return array( 'excluded' => false, 'counts' => $counts, 'points' => $points, 'level' => nlfr_level( $points, $askers, $days ),
		'progress' => nlfr_progress( $points, $askers, $days ), 'helped_askers' => $askers, 'joined' => $joined, 'days' => $days ) + $counts;
}

/**
 * Lifetime stats for members: id => result (or array( 'excluded' => true )). Each member is cached 5 minutes in his own
 * transient; the misses are counted together in one batch.
 */
function nlfr_stats( array $member_ids ) {
	static $memo = array();
	$ids  = array_values( array_unique( array_filter( array_map( 'intval', $member_ids ) ) ) );
	$out  = array();
	$miss = array();
	foreach ( $ids as $id ) {
		if ( isset( $memo[ $id ] ) ) { $out[ $id ] = $memo[ $id ]; continue; }
		$c = get_transient( 'nlfr_s' . NLFR_VER . '_' . $id );
		if ( is_array( $c ) ) { $out[ $id ] = $memo[ $id ] = $c; } else { $miss[] = $id; }
	}
	if ( $miss ) {
		$mem  = nlf_members( $miss );
		$real = array();
		foreach ( $miss as $id ) { if ( ! nlfr_excluded( $mem[ $id ] ?? null ) ) { $real[] = $id; } }
		$raw = $real ? nlfr_query_counts( $real, '' ) : array();
		foreach ( $miss as $id ) {
			$v = in_array( $id, $real, true ) ? nlfr_result( $mem[ $id ], $raw[ $id ] ?? array() ) : array( 'excluded' => true );
			set_transient( 'nlfr_s' . NLFR_VER . '_' . $id, $v, 5 * MINUTE_IN_SECONDS );
			$out[ $id ] = $memo[ $id ] = $v;
		}
	}
	return $out;
}

function nlfr_stat( $id ) { $s = nlfr_stats( array( (int) $id ) ); return $s[ (int) $id ] ?? array( 'excluded' => true ); }

/** name, label, tint and avatar shape of a member, as the forum prints him */
function nlfr_face( $m ) {
	$a = function_exists( 'nlf_emb_author' ) ? nlf_emb_author( $m ) : nlf_author( $m );
	return array( 'id' => $m ? (int) $m['id'] : 0, 'name' => (string) $a['name'], 'label' => (string) $a['label'], 'bg' => (string) $a['tint'][0],
		'fg' => (string) $a['tint'][1], 'sq' => (int) $a['pro'] > 0, 'initials' => nlf_initials( $a['name'] ), 'female' => ! empty( $a['female'] ) );
}

/**
 * The leaders of the last $days days: real members with points in the window, by points then helped answers. Cached 15
 * minutes. array() when fewer than 3 members qualify. Each row: id, name, label, bg, fg, sq, initials, points (window),
 * helped (window), stars and level name (lifetime).
 */
function nlfr_leaders( $days = 30, $limit = 5 ) {
	$days  = max( 1, (int) $days );
	$limit = max( 1, (int) $limit );
	$key   = 'nlfr_l' . NLFR_VER . '_' . $days . '_' . $limit;
	$c     = get_transient( $key );
	if ( is_array( $c ) && isset( $c['rows'] ) ) { return $c['rows']; }
	$raw  = nlfr_query_counts( null, gmdate( 'Y-m-d H:i:s', time() - $days * DAY_IN_SECONDS ) );
	$cand = array();
	foreach ( $raw as $mid => $r ) {
		$p = nlfr_points( $r );
		if ( $p > 0 ) { $cand[] = array( 'id' => (int) $mid, 'points' => $p, 'helped' => (int) $r['helped'] ); }
	}
	$mem  = $cand ? nlf_members( array_column( $cand, 'id' ) ) : array();
	$cand = array_values( array_filter( $cand, function ( $x ) use ( $mem ) { return ! nlfr_excluded( $mem[ $x['id'] ] ?? null ); } ) );
	$rows = array();
	if ( count( $cand ) >= 3 ) {
		$top  = array_slice( nlfr_leader_sort( $cand ), 0, $limit );
		$life = nlfr_stats( array_column( $top, 'id' ) );
		foreach ( $top as $x ) {
			$f  = nlfr_face( $mem[ $x['id'] ] );
			$lv = empty( $life[ $x['id'] ]['excluded'] ) ? $life[ $x['id'] ]['level'] : nlfr_levels()[0];
			$rows[] = $f + array( 'points' => $x['points'], 'helped' => $x['helped'], 'stars' => (int) $lv['n'], 'level' => $lv['name'] );
		}
	}
	set_transient( $key, array( 'rows' => $rows ), 15 * MINUTE_IN_SECONDS );
	return $rows;
}

/* =========================================================================================================
 * 3. HTML (board 20). Every person's text through esc_html / esc_attr.
 * ======================================================================================================= */

/** part א: the chip after a name ('' for an excluded member; a quiet text chip under 10 points) */
function nlfr_chip_html( $mid, $s ) {
	if ( ! is_array( $s ) || ! empty( $s['excluded'] ) ) { return ''; }
	$lv = $s['level'];
	if ( (int) $lv['n'] < 1 ) { return '<span class="nlfr-chip nlfr-chip-new">' . esc_html( $lv['name'] ) . '</span>'; }
	return '<button type="button" class="nlfr-chip" data-nlfr-member="' . (int) $mid . '" aria-haspopup="dialog" aria-label="' . esc_attr( nlfr_chip_label( $lv, $s['points'] ) ) . '">'
		. '<span class="nlfr-st" aria-hidden="true">' . esc_html( nlfr_stars_text( $lv['n'] ) ) . '</span><span>' . esc_html( $lv['name'] ) . '</span></button>';
}

/** on a discussion page: every author's stats in one batch, before the first name is printed */
function nlfr_prefetch_thread() {
	static $done = false;
	if ( $done || empty( $GLOBALS['nlf_topic'] ) || ! is_array( $GLOBALS['nlf_topic'] ) ) { return; }
	$done = true;
	global $wpdb;
	$t   = $GLOBALS['nlf_topic'];
	$ids = (array) $wpdb->get_col( $wpdb->prepare( 'SELECT DISTINCT member_id FROM ' . nlf_t( 'replies' ) . " WHERE topic_id = %d AND status = 'live'", (int) $t['id'] ) );
	$ids[] = (int) $t['member_id'];
	nlfr_stats( $ids );
}

add_filter( 'nlf_name_extra', function ( $html, $m ) {
	if ( ! is_array( $m ) || nlfr_excluded( $m ) ) { return $html; }
	nlfr_prefetch_thread();
	return $html . nlfr_chip_html( (int) $m['id'], nlfr_stat( (int) $m['id'] ) );
}, 15, 2 );

/* the chip of a joined member on his card, above the social block */
add_filter( 'nlf_card_member_block', function ( $html, $m ) {
	if ( ! is_array( $m ) || nlfr_excluded( $m ) ) { return $html; }
	$c = nlfr_chip_html( (int) $m['id'], nlfr_stat( (int) $m['id'] ) );
	return '' !== $c ? $html . '<div class="nlfr-cardrow"><span class="nlfr-cardrow-t">בפורום:</span>' . $c . '</div>' : $html;
}, 5, 2 );

/** the initials avatar in the member's tint (round, square for a linked card, as the forum prints avatars) */
function nlfr_avatar_html( array $f, $cls = '' ) {
	return '<span class="nlf-av nlfr-av' . ( $f['sq'] ? ' nlf-av-sq' : '' ) . ( '' !== $cls ? ' ' . $cls : '' ) . '" style="--nlf-bg:' . esc_attr( $f['bg'] ) . ';--nlf-fg:' . esc_attr( $f['fg'] ) . '" aria-hidden="true">' . esc_html( $f['initials'] ) . '</span>';
}

/** part ג: the leaders strip, or the compact invitation */
function nlfr_leaders_html( array $rows ) {
	if ( ! $rows ) {
		return '<section class="nlfr-leaders nlfr-invite" aria-labelledby="nlfr-l-h"><div class="nlfr-inv-t"><h2 class="nlfr-h" id="nlfr-l-h">כוכבים בזירה</h2>'
			. '<p>עונים, עוזרים ומקבלים כוכבים ליד השם. הכוכבים באים רק מעזרה שמישהו אחר אישר.</p></div>'
			. '<button type="button" class="nlfr-btn" data-nlfr-rules aria-haspopup="dialog">איך צוברים כוכבים</button></section>';
	}
	$h = '<section class="nlfr-leaders" aria-labelledby="nlfr-l-h"><div class="nlfr-lh"><h2 class="nlfr-h" id="nlfr-l-h">המובילים החודש</h2>'
		. '<button type="button" class="nlfr-link" data-nlfr-rules aria-haspopup="dialog">איך צוברים כוכבים</button></div><ol class="nlfr-list">';
	foreach ( array_values( $rows ) as $i => $r ) {
		$lbl = 'מקום ' . ( $i + 1 ) . ', ' . $r['name'] . ( '' !== $r['label'] ? ', ' . $r['label'] : '' ) . ', דרגת ' . $r['level'] . ', ' . nlfr_points_words( $r['points'] ) . ' החודש';
		$h  .= '<li><button type="button" class="nlfr-row' . ( 0 === $i ? ' is-first' : '' ) . '" data-nlfr-member="' . (int) $r['id'] . '" aria-haspopup="dialog" aria-label="' . esc_attr( $lbl ) . '">'
			. '<span class="nlfr-rank" aria-hidden="true">' . ( $i + 1 ) . '</span>' . nlfr_avatar_html( $r )
			. '<span class="nlfr-who" aria-hidden="true"><b>' . esc_html( $r['name'] ) . '</b>' . ( '' !== $r['label'] ? '<small>' . esc_html( $r['label'] ) . '</small>' : '' ) . '</span>'
			. ( $r['stars'] > 0 ? '<span class="nlfr-st" aria-hidden="true">' . esc_html( nlfr_stars_text( $r['stars'] ) ) . '</span>' : '' )
			. '<b class="nlfr-plus" aria-hidden="true">+' . esc_html( nlfr_num( $r['points'] ) ) . '</b></button></li>';
	}
	return $h . '</ol><p class="nlfr-fine">הרשימה מתחלפת כל יום, לפי 30 הימים האחרונים. היא מופיעה רק כשיש לפחות שלושה חברים שצברו נקודות.</p></section>';
}

add_filter( 'nlf_home_after_start', function ( $html ) {
	$a = function_exists( 'nlf_filter_args' ) ? nlf_filter_args() : array();
	if ( (int) ( $a['pg'] ?? 1 ) > 1 ) { return $html; } // the first page of the list only
	return $html . nlfr_leaders_html( nlfr_leaders( 30, 5 ) );
}, 20, 1 );

/* part ה: "הכוכבים שלי" in the member's own bar; a press opens his sheet */
add_filter( 'nlf_member_bar_extra', function ( $html, $me ) {
	if ( ! is_array( $me ) || nlfr_excluded( $me ) ) { return $html; }
	$s = nlfr_stat( (int) $me['id'] );
	if ( ! empty( $s['excluded'] ) ) { return $html; }
	$lv   = $s['level'];
	$next = nlfr_progress_short( $s['progress'] );
	$lbl  = 'הכוכבים שלי: ' . nlfr_chip_label( $lv, $s['points'] ) . ( '' !== $next ? '. ' . $next : '' );
	return $html . '<button type="button" class="nlfr-mine" data-nlfr-member="' . (int) $me['id'] . '" data-nlfr-level="' . (int) $lv['n'] . '" aria-haspopup="dialog" aria-label="' . esc_attr( $lbl ) . '">'
		. '<span class="nlfr-mine-t" aria-hidden="true">הכוכבים שלי</span>'
		. ( $lv['n'] > 0 ? '<span class="nlfr-st" aria-hidden="true">' . esc_html( nlfr_stars_text( $lv['n'] ) ) . '</span>' : '' )
		. '<span aria-hidden="true">' . esc_html( $lv['name'] . ' · ' . nlfr_points_words( $s['points'] ) ) . '</span>'
		. ( '' !== $next ? '<span class="nlfr-mine-n" aria-hidden="true">' . esc_html( $next ) . '</span>' : '' ) . '</button>';
}, 20, 2 );

/** the last level each member saw (option nlfr_seen: id => level, ints only, not autoloaded) */
function nlfr_seen_get() { $s = get_option( 'nlfr_seen', array() ); return is_array( $s ) ? $s : array(); }

/* part ה: the dark notice, once, when the member's level went up since he last saw it */
add_filter( 'nlf_home_notices', function ( $html, $me ) {
	if ( ! is_array( $me ) || nlfr_excluded( $me ) ) { return $html; }
	$s = nlfr_stat( (int) $me['id'] );
	if ( ! empty( $s['excluded'] ) ) { return $html; }
	$seen = nlfr_seen_get();
	$id   = (int) $me['id'];
	$d    = nlfr_levelup( $seen[ $id ] ?? null, (int) $s['level']['n'] );
	if ( null !== $d['store'] ) {
		$seen[ $id ] = (int) $d['store'];
		update_option( 'nlfr_seen', $seen, false );
	}
	if ( ! $d['show'] ) { return $html; }
	$lv = $s['level'];
	return $html . '<div class="nlfr-up" role="status"><span class="nlfr-up-i" aria-hidden="true">★</span><div class="nlfr-up-t"><b>' . esc_html( 'עליתם לדרגת ' . $lv['name'] ) . '</b>'
		. '<span>' . esc_html( nlfr_star_words( $lv['n'] ) . ' ליד השם שלכם בכל הפורום.' ) . '</span></div></div>';
}, 1, 2 );

/** part ד: the rules, as real HTML (inside the rules dialog) */
function nlfr_rules_html() {
	$h = '<p class="nlfr-lead">כוכבים באים מעזרה שמישהו אחר אישר. אי אפשר לקנות אותם, ואין נקודות שליליות.</p><ol class="nlfr-tiles">';
	foreach ( nlfr_levels() as $l ) {
		if ( $l['n'] < 1 ) { continue; }
		$h .= '<li data-nlfr-tile="' . (int) $l['n'] . '"><span class="nlfr-st" aria-hidden="true">' . esc_html( nlfr_stars_text( $l['n'] ) ) . '</span><b>' . esc_html( $l['name'] ) . '</b>'
			. '<small><span class="nlfr-sr">' . esc_html( nlfr_star_words( $l['n'] ) . ', מ-' ) . '</span>' . esc_html( nlfr_num( $l['min'] ) ) . '<span class="nlfr-sr"> נקודות</span></small></li>';
	}
	$h .= '</ol><ul class="nlfr-pts">';
	foreach ( nlfr_rule_rows() as $r ) { $h .= '<li><span>' . esc_html( $r[0] ) . '</span><b>' . esc_html( nlfr_num( $r[1] ) ) . '<span class="nlfr-sr"> נקודות</span></b></li>'; }
	return $h . '</ul><p class="nlfr-fine">' . esc_html( nlfr_rules_fine() ) . '</p>';
}

/* =========================================================================================================
 * 4. Assets and the two dialogs (forum surfaces only)
 * ======================================================================================================= */

function nlfr_surface() {
	if ( ! function_exists( 'nlf_surface' ) ) { return false; }
	if ( '' === nlf_rendering() && ! empty( $GLOBALS['nlf_act_page'] ) ) { return false; } // a one-click page needs none of this
	return nlf_surface();
}

/** the numbers the page script uses: the same functions the PHP counts with */
function nlfr_public_rules() {
	return array( 'weights' => nlfr_weights(), 'levels' => nlfr_levels(), 'gate' => nlfr_gate(), 'cap' => nlfr_post_cap(), 'max' => nlfr_max_stars() );
}

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nlfr_surface() ) { return; }
	$base = plugins_url( 'assets/proforum/', dirname( __FILE__ ) );
	$ver  = function_exists( 'nlf_ver' ) ? nlf_ver() : '1';
	wp_enqueue_style( 'nlf-rep', $base . 'rep.css', array( 'nlf' ), $ver );
	wp_enqueue_script( 'nlf-rep', $base . 'rep.js', array( 'nlf' ), $ver, true );
	wp_add_inline_script( 'nlf-rep', 'window.NLFR=' . nlf_json_script( nlfr_public_rules() ) . ';', 'before' );
}, 33 );

function nlfr_dialogs_html() {
	$close = '<button type="button" class="nlf-ico nlfr-x" data-nlf-close aria-label="סגירה">' . nlf_svg( 'close' ) . '</button>';
	return '<dialog class="nlf nlf-sheet nlfr-sheet" id="nlfr-member" dir="rtl" aria-labelledby="nlfr-m-h">'
		. '<div class="nlfr-mh"><span class="nlf-av nlfr-av nlfr-av-lg" data-nlfr-av aria-hidden="true"></span><div class="nlfr-mh-t"><h2 class="nlfr-h" id="nlfr-m-h">כוכבים ודרגה</h2><span class="nlfr-mh-s" data-nlfr-sub></span></div>' . $close . '</div>'
		. '<div class="nlfr-body" data-nlfr-body></div>'
		. '<p class="nlf-msg" data-nlfr-msg role="status" aria-live="polite"></p>'
		. '<button type="button" class="nlfr-btn nlfr-btn-wide" data-nlfr-rules aria-haspopup="dialog">איך צוברים כוכבים</button>'
		. '</dialog>'
		. '<dialog class="nlf nlf-sheet nlfr-sheet nlfr-rules" id="nlfr-rules" dir="rtl" aria-labelledby="nlfr-r-h">'
		. '<div class="nlfr-mh"><h2 class="nlfr-h" id="nlfr-r-h">איך צוברים כוכבים</h2>' . $close . '</div>'
		. nlfr_rules_html()
		. '</dialog>';
}

add_action( 'wp_footer', function () {
	if ( ! nlfr_surface() || ( '' === nlf_rendering() && empty( $GLOBALS['nlf_card_printed'] ) ) ) { return; }
	echo nlfr_dialogs_html(); // phpcs:ignore -- escaped inside
}, 6 ); // before the footer scripts (forum.js wires every dialog.nlf when it runs)

/* =========================================================================================================
 * 5. REST: GET nadlan/v1/forum/rep/member?id=  (public read; nothing private, no contact)
 * ======================================================================================================= */

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/forum/rep/member', array( 'methods' => 'GET', 'permission_callback' => '__return_true', 'show_in_index' => false,
		'callback' => function ( WP_REST_Request $q ) {
			if ( ! function_exists( 'nlf_guard' ) ) { return new WP_Error( 'nlfr_off', 'הפעולה לא זמינה כרגע.', array( 'status' => 400 ) ); }
			$g = nlf_guard( $q, 'view' ); // the forum gate + the per-IP read ceiling
			if ( is_wp_error( $g ) ) { return $g; }
			$id  = (int) $q->get_param( 'id' );
			$mem = $id > 0 ? nlf_members( array( $id ) ) : array();
			$m   = $mem[ $id ] ?? null;
			$me  = nlf_me();
			$own = $me && $m && (int) $me['id'] === $id;
			// shown only when already visible in the forum (an approved post or a linked card), or to himself
			if ( nlfr_excluded( $m ) || ! ( (int) $m['approved_posts'] > 0 || (int) $m['pro_id'] > 0 || $own ) ) { return nlf_err( 'המשתתף לא נמצא.' ); }
			$s = nlfr_stat( $id );
			if ( ! empty( $s['excluded'] ) ) { return nlf_err( 'המשתתף לא נמצא.' ); }
			$f  = nlfr_face( $m );
			$lv = $s['level'];
			$sub = array_filter( array( $f['label'], $s['joined'] > 0 ? ( $f['female'] ? 'חברה' : 'חבר' ) . ' מאז ' . nlfr_month_he( $s['joined'] ) : '' ) );
			return nlf_ok( array(
				'member' => array( 'id' => $id, 'name' => $f['name'], 'label' => $f['label'], 'sub' => implode( ' · ', $sub ), 'bg' => $f['bg'], 'fg' => $f['fg'], 'sq' => $f['sq'] ? 1 : 0, 'initials' => $f['initials'] ),
				'own'    => $own ? 1 : 0,
				'rep'    => array( 'points' => (int) $s['points'], 'stars' => (int) $lv['n'], 'level' => $lv['name'], 'pct' => (int) $s['progress']['pct'],
					'next' => $s['progress']['next'], 'text' => nlfr_progress_text( $s['progress'] ), 'label' => nlfr_chip_label( $lv, $s['points'] ) ),
				'rows'   => nlfr_breakdown( $s['counts'] ),
			) );
		},
	) );
} );
