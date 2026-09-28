<?php
/**
 * TogetherRoom: the shared viewing room (design system TogetherRoom, version 77, 28.9.2026).
 *
 * The owner, 28.9: the video call is not a button and not a booking form, it is a live room inside the apartment. The
 * representative opens it; the buyer, the partner, friends, the interior designer and the engineer join from a link;
 * everyone sees the same apartment at the same moment; the representative leads the view; anyone pins a note to a point in
 * the apartment. The notes are kept in the apartment's file, and at the end the file goes on WhatsApp.
 *
 *  - The room page is the project page itself with ?room=<id> (no new URL: one word, one owner URL). Only then the room's
 *    container is printed and assets/together/together.js + together.css are loaded. No robots meta is added here:
 *    indexing is the owner's decision, and a query-string room page is linked from nowhere.
 *  - Video and the data channel run on LiveKit (Settings > חדר צפייה משותף: server URL, API key, API secret; the secret is
 *    write-only). Without a key the room still works: no video tiles, the view and the notes sync over this REST API, the
 *    way inc/cotour.php does it (the leader posts the state, the others poll every 1.5 s).
 *  - REST (nadlan/v1): POST /room, POST /room/token, GET|POST /room/state, GET|POST /room/notes, GET /room/file.
 *  - Storage: a room is one post of the private type nadlan_room (post_name = the room id, meta = the project and the
 *    notes, one meta row per note). A post and not an option because the notes are durable records that must outlive the
 *    live call (the file link sent on WhatsApp keeps working for the retention days), they need a date to be cleaned up by
 *    (a daily WP-Cron deletes rooms older than the retention days, default 30) and they must never ride in autoloaded
 *    options. The live part (who is in, who leads, the camera ten times a second) is short-lived and lives in transients,
 *    like the co-tour: a room closes after 6 hours without activity, and a representative who enters reopens it.
 *  - The hero button "שיחת וידאו עם נציג" (inc/project-stage.php) gets a small chooser when a representative is marked
 *    available: "עכשיו, בחדר משותף" (?room=new creates a room and enters as a buyer) or "לתאם מועד" (the booking band
 *    #nlsch, as today). A logged-in user with edit_posts opens ?room=new as the representative.
 *  - The words: the call is with NadLan's team, an independent platform, not on behalf of the developer; it is not
 *    recorded; changes to the apartment are subject to the developer's approval. NadLan is never presented as a broker.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NADLAN_TR_LK_LIB' ) ) {
	// livekit-client, pinned to an exact 2.x build (checked 28.9.2026: HTTP 200); loaded by the room only after the join click
	define( 'NADLAN_TR_LK_LIB', 'https://cdn.jsdelivr.net/npm/livekit-client@2.22.3/dist/livekit-client.esm.mjs' );
}

/* ---------------------------------------------------------------- settings */

if ( ! function_exists( 'nadlan_tr_opt' ) ) {
	function nadlan_tr_opt( $key, $default = '' ) {
		$v = get_option( 'nadlan_tr_' . $key, $default );
		return is_string( $v ) ? trim( $v ) : $v;
	}
}
if ( ! function_exists( 'nadlan_tr_lk_ready' ) ) {
	/** LiveKit is on when the server URL, the key and the secret are all set. */
	function nadlan_tr_lk_ready() {
		return '' !== (string) nadlan_tr_opt( 'lk_url' ) && '' !== (string) nadlan_tr_opt( 'lk_key' ) && '' !== (string) nadlan_tr_opt( 'lk_secret' );
	}
}
if ( ! function_exists( 'nadlan_tr_rep_now' ) ) {
	function nadlan_tr_rep_now() { return '1' === (string) nadlan_tr_opt( 'rep_now', '0' ); }
}
if ( ! function_exists( 'nadlan_tr_retention_days' ) ) {
	function nadlan_tr_retention_days() {
		$d = (int) nadlan_tr_opt( 'retention', 30 );
		return $d >= 1 && $d <= 365 ? $d : 30;
	}
}
if ( ! function_exists( 'nadlan_tr_roles' ) ) {
	/** role => its colour group (design system: rep, buyer, family and friends, professionals). */
	function nadlan_tr_roles() {
		return array( 'rep' => 'rep', 'buyer' => 'buyer', 'partner' => 'family', 'friend' => 'family', 'designer' => 'pro', 'engineer' => 'pro', 'lawyer' => 'pro' );
	}
}

/* ---------------------------------------------------------------- storage */

add_action( 'init', function () {
	register_post_type( 'nadlan_room', array(
		'labels'              => array( 'name' => 'חדרי צפייה', 'singular_name' => 'חדר צפייה' ),
		'public'              => false,
		'publicly_queryable'  => false,
		'exclude_from_search' => true,
		'show_ui'             => false,
		'show_in_rest'        => false,
		'show_in_nav_menus'   => false,
		'rewrite'             => false,
		'query_var'           => false,
		'can_export'          => false,
		'supports'            => array( 'title' ),
	) );
	if ( ! wp_next_scheduled( 'nadlan_tr_cleanup' ) ) {
		wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nadlan_tr_cleanup' );
	}
}, 20 );

/* the retention: rooms (and with them their notes) older than the retention days are deleted, 200 a day at most */
add_action( 'nadlan_tr_cleanup', function () {
	$ids = get_posts( array(
		'post_type'        => 'nadlan_room',
		'post_status'      => 'any',
		'fields'           => 'ids',
		'numberposts'      => 200,
		'no_found_rows'    => true,
		'suppress_filters' => true,
		'date_query'       => array( array( 'before' => gmdate( 'Y-m-d H:i:s', time() - nadlan_tr_retention_days() * DAY_IN_SECONDS ), 'column' => 'post_date_gmt' ) ),
	) );
	foreach ( (array) $ids as $id ) {
		$room = (string) get_post_field( 'post_name', $id );
		wp_delete_post( (int) $id, true );
		if ( '' !== $room ) { delete_transient( 'nltr_l_' . $room ); delete_transient( 'nltr_s_' . $room ); }
	}
} );

if ( ! function_exists( 'nadlan_tr_rand' ) ) {
	/** $n random base32 characters (a-z, 2-7): 5 bits each. */
	function nadlan_tr_rand( $n ) {
		$alpha = 'abcdefghijklmnopqrstuvwxyz234567';
		$bytes = random_bytes( $n );
		$out   = '';
		for ( $i = 0; $i < $n; $i++ ) { $out .= $alpha[ ord( $bytes[ $i ] ) & 31 ]; }
		return $out;
	}
}
if ( ! function_exists( 'nadlan_tr_valid_id' ) ) {
	function nadlan_tr_valid_id( $id ) {
		$id = strtolower( (string) $id );
		return preg_match( '/^[a-z2-7]{12}$/', $id ) ? $id : '';
	}
}
if ( ! function_exists( 'nadlan_tr_post' ) ) {
	/** The room's post id, or 0. */
	function nadlan_tr_post( $room ) {
		$room = nadlan_tr_valid_id( $room );
		if ( '' === $room ) { return 0; }
		$ids = get_posts( array( 'post_type' => 'nadlan_room', 'name' => $room, 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true ) );
		return $ids ? (int) $ids[0] : 0;
	}
}
if ( ! function_exists( 'nadlan_tr_project_ok' ) ) {
	/** A room belongs to a published project page that has the stage (inc/project-stage.php). */
	function nadlan_tr_project_ok( $pid ) {
		$pid = (int) $pid;
		if ( $pid <= 0 || 'nadlan_project' !== get_post_type( $pid ) || 'publish' !== get_post_status( $pid ) ) { return false; }
		if ( post_password_required( $pid ) || get_post_meta( $pid, '_nadlan_private_unit_journey', true ) ) { return false; }
		if ( function_exists( 'nadlan_ps_config' ) ) {
			$all = nadlan_ps_config();
			return isset( $all[ (string) get_post_field( 'post_name', $pid ) ] );
		}
		return true;
	}
}
if ( ! function_exists( 'nadlan_tr_ps' ) ) {
	/** The stage's config of the room's project (name, units, sectors), or an empty array. */
	function nadlan_tr_ps( $pid ) {
		if ( ! function_exists( 'nadlan_ps_config' ) ) { return array(); }
		$all  = nadlan_ps_config();
		$slug = (string) get_post_field( 'post_name', (int) $pid );
		return isset( $all[ $slug ] ) ? $all[ $slug ] : array();
	}
}
if ( ! function_exists( 'nadlan_tr_live' ) ) {
	/** The live part of a room (participants, leader, notes revision), or null when the room is closed. */
	function nadlan_tr_live( $room ) {
		$l = get_transient( 'nltr_l_' . $room );
		return is_array( $l ) ? $l : null;
	}
}
if ( ! function_exists( 'nadlan_tr_save_live' ) ) {
	function nadlan_tr_save_live( $room, $live ) {
		$live['t'] = time();
		set_transient( 'nltr_l_' . $room, $live, 6 * HOUR_IN_SECONDS ); // closes after 6 hours idle
	}
}
if ( ! function_exists( 'nadlan_tr_rl' ) ) {
	/** A fixed-window rate limit per IP (a transient per window): true while under $max in $window seconds. */
	function nadlan_tr_rl( $bucket, $max, $window ) {
		$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? (string) $_SERVER['REMOTE_ADDR'] : '0'; // phpcs:ignore
		$k  = 'nltr_rl_' . md5( $bucket . '|' . $ip . '|' . (int) floor( time() / $window ) );
		$n  = (int) get_transient( $k );
		if ( $n >= $max ) { return false; }
		set_transient( $k, $n + 1, $window );
		return true;
	}
}
if ( ! function_exists( 'nadlan_tr_hash' ) ) {
	function nadlan_tr_hash( $key ) { return hash_hmac( 'sha256', (string) $key, wp_salt( 'auth' ) ); }
}
if ( ! function_exists( 'nadlan_tr_who' ) ) {
	/** The participant a request speaks for (pid + key), or null. */
	function nadlan_tr_who( $live, $pid, $key ) {
		$pid = preg_replace( '/[^a-z2-7]/', '', strtolower( (string) $pid ) );
		if ( ! is_array( $live ) || '' === $pid || empty( $live['p'][ $pid ] ) || '' === (string) $key ) { return null; }
		$p = $live['p'][ $pid ];
		return hash_equals( (string) $p['k'], nadlan_tr_hash( $key ) ) ? array_merge( $p, array( 'pid' => $pid ) ) : null;
	}
}
if ( ! function_exists( 'nadlan_tr_people' ) ) {
	/** The participants as others may see them: no keys. "on" = seen in the last 25 seconds. */
	function nadlan_tr_people( $live ) {
		$out = array();
		foreach ( (array) ( $live['p'] ?? array() ) as $pid => $p ) {
			$out[] = array( 'pid' => (string) $pid, 'name' => (string) $p['n'], 'role' => (string) $p['r'], 'on' => ( time() - (int) $p['s'] ) < 25 );
		}
		return $out;
	}
}
if ( ! function_exists( 'nadlan_tr_err' ) ) {
	function nadlan_tr_err( $code, $status ) { return new WP_REST_Response( array( 'ok' => false, 'error' => $code ), $status ); }
}

/* ---------------------------------------------------------------- cleaning what comes in */

if ( ! function_exists( 'nadlan_tr_num' ) ) {
	function nadlan_tr_num( $v, $lim, $dec = 4 ) {
		if ( ! is_numeric( $v ) ) { return null; }
		$f = (float) $v;
		return is_finite( $f ) && abs( $f ) <= $lim ? round( $f, $dec ) : null;
	}
}
if ( ! function_exists( 'nadlan_tr_side' ) ) {
	function nadlan_tr_side( $v ) { $v = strtolower( (string) $v ); return preg_match( '/^[a-z]{1,3}$/', $v ) ? $v : ''; }
}
if ( ! function_exists( 'nadlan_tr_mode' ) ) {
	function nadlan_tr_mode( $v ) { $v = (string) $v; return in_array( $v, array( 'building', 'plan', 'inside', 'view' ), true ) ? $v : ''; }
}
if ( ! function_exists( 'nadlan_tr_clean_anchor' ) ) {
	/** A note's anchor: {mode, floor, side, scene, x, y, z (the stage), yaw, pitch (360: radians; the view: degrees), sx, sy (0..1)}. */
	function nadlan_tr_clean_anchor( $a ) {
		$a   = is_array( $a ) ? $a : array();
		$out = array( 'mode' => nadlan_tr_mode( $a['mode'] ?? '' ) ?: 'building' );
		$f   = (int) ( $a['floor'] ?? 0 );
		if ( $f > 0 && $f < 200 ) { $out['floor'] = $f; }
		$s = nadlan_tr_side( $a['side'] ?? '' );
		if ( '' !== $s ) { $out['side'] = $s; }
		$sc = strtolower( (string) ( $a['scene'] ?? '' ) );
		if ( preg_match( '/^[a-z0-9-]{1,24}$/', $sc ) ) { $out['scene'] = $sc; }
		foreach ( array( 'x' => 100000, 'y' => 100000, 'z' => 100000, 'yaw' => 10000, 'pitch' => 10000 ) as $k => $lim ) {
			$n = nadlan_tr_num( $a[ $k ] ?? null, $lim );
			if ( null !== $n ) { $out[ $k ] = $n; }
		}
		foreach ( array( 'sx', 'sy' ) as $k ) {
			$n = nadlan_tr_num( $a[ $k ] ?? null, 1, 5 );
			if ( null !== $n && $n >= 0 ) { $out[ $k ] = $n; }
		}
		return $out;
	}
}
if ( ! function_exists( 'nadlan_tr_clean_state' ) ) {
	/**
	 * The leader's state: m (mode), u (the example apartment "25-w"), f (floor), v (the camera of the mode: the stage
	 * {t:[x,y,z], r, p, th, hf}, the 360 {s, y, p, f}, the view {b, v}), pt (the pointer, an anchor-like point), n (name).
	 */
	function nadlan_tr_clean_state( $s ) {
		$s   = is_array( $s ) ? $s : array();
		$out = array( 'm' => nadlan_tr_mode( $s['m'] ?? '' ) ?: 'building' );
		$u   = strtolower( (string) ( $s['u'] ?? '' ) );
		if ( preg_match( '/^\d{1,3}-[a-z]{1,3}$/', $u ) ) { $out['u'] = $u; }
		$f = (int) ( $s['f'] ?? 0 );
		if ( $f > 0 && $f < 200 ) { $out['f'] = $f; }
		$v = is_array( $s['v'] ?? null ) ? $s['v'] : array();
		$cv = array();
		if ( isset( $v['t'] ) && is_array( $v['t'] ) && 3 === count( $v['t'] ) ) {
			$t = array_map( function ( $x ) { return nadlan_tr_num( $x, 100000, 2 ); }, array_values( $v['t'] ) );
			if ( ! in_array( null, $t, true ) ) { $cv['t'] = $t; }
		}
		foreach ( array( 'r' => 100000, 'p' => 10, 'th' => 10000, 'hf' => 4, 'y' => 10000, 'f' => 180, 'b' => 3600, 'v' => 360 ) as $k => $lim ) {
			$n = nadlan_tr_num( $v[ $k ] ?? null, $lim );
			if ( null !== $n ) { $cv[ $k ] = $n; }
		}
		$sc = strtolower( (string) ( $v['s'] ?? '' ) );
		if ( preg_match( '/^[a-z0-9-]{1,24}$/', $sc ) ) { $cv['s'] = $sc; }
		if ( $cv ) { $out['v'] = $cv; }
		if ( isset( $s['pt'] ) && is_array( $s['pt'] ) ) { $out['pt'] = nadlan_tr_clean_anchor( $s['pt'] ); }
		return $out;
	}
}

/* ---------------------------------------------------------------- LiveKit */

if ( ! function_exists( 'nadlan_tr_b64u' ) ) {
	function nadlan_tr_b64u( $s ) { return rtrim( strtr( base64_encode( $s ), '+/', '-_' ), '=' ); }
}
if ( ! function_exists( 'nadlan_tr_jwt' ) ) {
	/** A JWT signed HS256 (the LiveKit access token format). */
	function nadlan_tr_jwt( array $claims, $secret ) {
		$h = nadlan_tr_b64u( wp_json_encode( array( 'alg' => 'HS256', 'typ' => 'JWT' ) ) );
		$p = nadlan_tr_b64u( wp_json_encode( $claims, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) );
		return $h . '.' . $p . '.' . nadlan_tr_b64u( hash_hmac( 'sha256', $h . '.' . $p, (string) $secret, true ) );
	}
}
if ( ! function_exists( 'nadlan_tr_lk_token' ) ) {
	/** A LiveKit access token for one participant of one room, valid two hours. */
	function nadlan_tr_lk_token( $room, $identity, $name, $role, $key, $secret ) {
		$now = time();
		return nadlan_tr_jwt( array(
			'iss'      => (string) $key,
			'sub'      => (string) $identity,
			'name'     => (string) $name,
			'nbf'      => $now - 5,
			'exp'      => $now + 2 * HOUR_IN_SECONDS,
			'video'    => array( 'room' => 'nadlan-' . $room, 'roomJoin' => true, 'canPublish' => true, 'canSubscribe' => true, 'canPublishData' => true ),
			'metadata' => wp_json_encode( array( 'role' => (string) $role ) ),
		), $secret );
	}
}

/* ---------------------------------------------------------------- the file */

if ( ! function_exists( 'nadlan_tr_keep_sel' ) ) {
	/** The file's apartment (floor and side), written only when it changes; a note without a side keeps the side it had. */
	function nadlan_tr_keep_sel( $post, $floor, $side ) {
		$prev = (array) get_post_meta( $post, '_nltr_sel', true );
		if ( '' === $side && (int) ( $prev['floor'] ?? 0 ) === $floor ) { $side = (string) ( $prev['side'] ?? '' ); }
		if ( (int) ( $prev['floor'] ?? 0 ) === $floor && (string) ( $prev['side'] ?? '' ) === $side ) { return; }
		update_post_meta( $post, '_nltr_sel', array( 'floor' => $floor, 'side' => $side ) );
	}
}

if ( ! function_exists( 'nadlan_tr_notes' ) ) {
	/** The room's notes, oldest first. */
	function nadlan_tr_notes( $post ) {
		$rows = get_post_meta( (int) $post, '_nltr_note', false );
		$out  = array();
		foreach ( (array) $rows as $r ) { if ( is_array( $r ) && isset( $r['id'], $r['n'] ) ) { $out[] = $r; } }
		usort( $out, function ( $a, $b ) { return ( (int) $a['n'] <=> (int) $b['n'] ) ?: ( (int) $a['t'] <=> (int) $b['t'] ); } );
		return $out;
	}
}
if ( ! function_exists( 'nadlan_tr_facing' ) ) {
	/** What lies toward an example apartment's side, in the project's own words ("לכיוון הים"), or ''. */
	function nadlan_tr_facing( $ps, $side ) {
		$b = null;
		foreach ( (array) ( $ps['units'] ?? array() ) as $u ) { if ( (string) $u[0] === (string) $side ) { $b = (float) $u[1]; } }
		if ( null === $b ) { return ''; }
		$x = fmod( fmod( $b, 360 ) + 360, 360 );
		foreach ( (array) ( $ps['sectors'] ?? array() ) as $s ) {
			$from = fmod( fmod( (float) $s[0], 360 ) + 360, 360 );
			$to   = fmod( fmod( (float) $s[1], 360 ) + 360, 360 );
			if ( $from <= $to ? ( $x >= $from && $x < $to ) : ( $x >= $from || $x < $to ) ) { return (string) $s[2]; }
		}
		return '';
	}
}
if ( ! function_exists( 'nadlan_tr_file' ) ) {
	function nadlan_tr_file( $post, $room ) {
		$pid   = (int) get_post_meta( $post, '_nltr_project', true );
		$ps    = nadlan_tr_ps( $pid );
		$sel   = (array) get_post_meta( $post, '_nltr_sel', true );
		$floor = (int) ( $sel['floor'] ?? 0 );
		$side  = (string) ( $sel['side'] ?? '' );
		$url   = get_permalink( $pid );
		return array(
			'ok'      => true,
			'room'    => $room,
			'open'    => null !== nadlan_tr_live( $room ),
			'created' => (int) get_post_meta( $post, '_nltr_created', true ),
			'project' => array( 'id' => $pid, 'name' => (string) ( $ps['name'] ?? get_the_title( $pid ) ), 'url' => $url ),
			'floor'   => $floor > 0 ? $floor : null,
			'side'    => $side,
			'facing'  => '' !== $side ? nadlan_tr_facing( $ps, $side ) : '',
			'sample'  => true, // an example apartment, always (the owner's decision of 25.9.2026)
			'notes'   => nadlan_tr_notes( $post ),
			'join'    => $url ? add_query_arg( 'room', $room, $url ) : '',
		);
	}
}

/* ---------------------------------------------------------------- REST */

add_action( 'rest_api_init', function () {
	$ns = 'nadlan/v1';

	/* a new room for a project page: a representative any time; a visitor only while a representative is marked available */
	register_rest_route( $ns, '/room', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$p   = (array) $req->get_json_params();
			$pid = (int) ( $p['post'] ?? $p['post_id'] ?? 0 );
			$rep = current_user_can( 'edit_posts' );
			if ( ! nadlan_tr_project_ok( $pid ) ) { return nadlan_tr_err( 'project', 400 ); }
			if ( ! $rep && ! nadlan_tr_rep_now() ) { return nadlan_tr_err( 'no_rep', 403 ); }
			if ( ! nadlan_tr_rl( 'room', $rep ? 60 : 4, HOUR_IN_SECONDS ) ) { return nadlan_tr_err( 'rate', 429 ); }
			$room = '';
			for ( $i = 0; $i < 4 && '' === $room; $i++ ) {
				$try = nadlan_tr_rand( 12 );
				if ( ! nadlan_tr_post( $try ) ) { $room = $try; }
			}
			if ( '' === $room ) { return nadlan_tr_err( 'busy', 503 ); }
			$post = wp_insert_post( array( 'post_type' => 'nadlan_room', 'post_status' => 'publish', 'post_title' => 'room ' . $room, 'post_name' => $room ), true );
			if ( is_wp_error( $post ) || ! $post ) { return nadlan_tr_err( 'store', 500 ); }
			update_post_meta( $post, '_nltr_project', $pid );
			update_post_meta( $post, '_nltr_created', time() );
			update_post_meta( $post, '_nltr_by', $rep ? 'rep' : 'buyer' );
			nadlan_tr_save_live( $room, array( 'p' => array(), 'lead' => '', 'rev' => 0, 'post' => (int) $post, 'project' => $pid ) );
			do_action( 'nadlan_together_room_created', $room, $pid, $rep ? 'rep' : 'buyer' );
			$url = get_permalink( $pid );
			return new WP_REST_Response( array( 'ok' => true, 'room' => $room, 'join_url' => add_query_arg( 'room', $room, $url ), 'file_url' => add_query_arg( array( 'room' => $room, 'file' => '1' ), $url ) ), 201 );
		},
	) );

	/* entering: a name and a role; back a participant id and key, and a LiveKit token (or {mode: 'fallback'}) */
	register_rest_route( $ns, '/room/token', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$p    = (array) $req->get_json_params();
			$room = nadlan_tr_valid_id( $p['room'] ?? '' );
			if ( '' === $room ) { return nadlan_tr_err( 'room', 400 ); }
			if ( ! nadlan_tr_rl( 'token', 30, 600 ) ) { return nadlan_tr_err( 'rate', 429 ); }
			$post = nadlan_tr_post( $room );
			if ( ! $post ) { return nadlan_tr_err( 'room', 404 ); }
			$role  = sanitize_key( (string) ( $p['role'] ?? '' ) );
			$roles = nadlan_tr_roles();
			if ( ! isset( $roles[ $role ] ) ) { return nadlan_tr_err( 'role', 400 ); }
			if ( 'rep' === $role && ! current_user_can( 'edit_posts' ) ) { return nadlan_tr_err( 'role', 403 ); }
			$name = trim( preg_replace( '/\s+/u', ' ', sanitize_text_field( (string) ( $p['name'] ?? '' ) ) ) );
			$name = function_exists( 'mb_substr' ) ? mb_substr( $name, 0, 40 ) : substr( $name, 0, 40 );
			if ( '' === $name ) { return nadlan_tr_err( 'name', 400 ); }
			$live = nadlan_tr_live( $room );
			if ( null === $live ) {
				if ( 'rep' !== $role ) { return nadlan_tr_err( 'closed', 410 ); }
				$live = array( 'p' => array(), 'lead' => '', 'rev' => 0, 'post' => $post, 'project' => (int) get_post_meta( $post, '_nltr_project', true ) ); // a representative reopens it
			}
			// the ones not seen for ten minutes leave the list
			foreach ( (array) $live['p'] as $k => $pp ) { if ( time() - (int) $pp['s'] > 600 ) { unset( $live['p'][ $k ] ); } }
			$pid = preg_replace( '/[^a-z2-7]/', '', strtolower( (string) ( $p['pid'] ?? '' ) ) );
			$key = preg_replace( '/[^a-z2-7]/', '', strtolower( (string) ( $p['key'] ?? '' ) ) );
			$me  = nadlan_tr_who( $live, $pid, $key );
			if ( ! $me ) {
				// the same browser coming back after the list lost it keeps its id; anyone else gets a new one
				$fresh = ! ( 8 === strlen( $pid ) && 22 === strlen( $key ) && empty( $live['p'][ $pid ] ) );
				if ( $fresh ) { $pid = nadlan_tr_rand( 8 ); $key = nadlan_tr_rand( 22 ); }
				$on = 0;
				foreach ( (array) $live['p'] as $pp ) { if ( time() - (int) $pp['s'] < 60 ) { $on++; } }
				if ( $on >= 12 ) { return nadlan_tr_err( 'full', 409 ); }
				$live['p'][ $pid ] = array( 'n' => $name, 'r' => $role, 'k' => nadlan_tr_hash( $key ), 'j' => time(), 's' => time() );
			} else {
				$live['p'][ $pid ]['n'] = $name;
				$live['p'][ $pid ]['r'] = $role;
				$live['p'][ $pid ]['s'] = time();
			}
			nadlan_tr_save_live( $room, $live );
			$st  = get_transient( 'nltr_s_' . $room );
			$out = array(
				'ok' => true, 'room' => $room, 'pid' => $pid, 'key' => $key, 'name' => $name, 'role' => $role,
				'leader' => (string) $live['lead'], 'participants' => nadlan_tr_people( $live ), 'rev' => (int) $live['rev'],
				'state' => is_array( $st ) ? $st['state'] : null, 't' => is_array( $st ) ? (float) $st['t'] : 0,
			);
			if ( nadlan_tr_lk_ready() ) {
				$out['mode']  = 'livekit';
				$out['url']   = (string) nadlan_tr_opt( 'lk_url' );
				$out['token'] = nadlan_tr_lk_token( $room, $pid, $name, $role, nadlan_tr_opt( 'lk_key' ), nadlan_tr_opt( 'lk_secret' ) );
			} else {
				$out['mode'] = 'fallback';
			}
			return new WP_REST_Response( $out, 200 );
		},
	) );

	/* the sync without video: the leader posts the state, everyone polls (every 1.5 s); presence rides on the polls */
	register_rest_route( $ns, '/room/state', array(
		array(
			'methods'             => 'GET',
			'permission_callback' => '__return_true',
			'callback'            => function ( WP_REST_Request $req ) {
				$room = nadlan_tr_valid_id( $req->get_param( 'room' ) );
				if ( '' === $room ) { return nadlan_tr_err( 'room', 400 ); }
				$live = nadlan_tr_live( $room );
				if ( null === $live ) { return nadlan_tr_err( 'closed', 410 ); }
				$me  = nadlan_tr_who( $live, $req->get_param( 'pid' ), (string) $req->get_param( 'key' ) );
				$out = array( 'ok' => true );
				if ( $me ) {
					if ( time() - (int) $live['p'][ $me['pid'] ]['s'] > 8 ) { // presence, written at most every 8 seconds
						$live['p'][ $me['pid'] ]['s'] = time();
						nadlan_tr_save_live( $room, $live );
					}
				} elseif ( '' !== (string) $req->get_param( 'pid' ) ) {
					$out['rejoin'] = true;
				}
				$st    = get_transient( 'nltr_s_' . $room );
				$since = (float) $req->get_param( 'since' );
				if ( is_array( $st ) && (float) $st['t'] > $since ) { $out['state'] = $st['state']; }
				$out['t']            = is_array( $st ) ? (float) $st['t'] : 0;
				$out['leader']       = (string) $live['lead'];
				$out['participants'] = nadlan_tr_people( $live );
				$out['rev']          = (int) $live['rev'];
				return new WP_REST_Response( $out, 200 );
			},
		),
		array(
			'methods'             => 'POST',
			'permission_callback' => '__return_true',
			'callback'            => function ( WP_REST_Request $req ) {
				$p    = (array) $req->get_json_params();
				$room = nadlan_tr_valid_id( $p['room'] ?? '' );
				if ( '' === $room ) { return nadlan_tr_err( 'room', 400 ); }
				$live = nadlan_tr_live( $room );
				if ( null === $live ) { return nadlan_tr_err( 'closed', 410 ); }
				$me = nadlan_tr_who( $live, $p['pid'] ?? '', (string) ( $p['key'] ?? '' ) );
				if ( ! $me ) { return nadlan_tr_err( 'who', 403 ); }
				// a room's writes: 3 a second is plenty (the co-tour's throttle)
				$tk = 'nltr_w_' . $room . '_' . (int) floor( time() / 3 );
				$wn = (int) get_transient( $tk );
				if ( $wn > 9 ) { return nadlan_tr_err( 'rate', 429 ); }
				set_transient( $tk, $wn + 1, 3 );
				$live['p'][ $me['pid'] ]['s'] = time();
				if ( ! empty( $p['leave'] ) ) {
					unset( $live['p'][ $me['pid'] ] );
					if ( $live['lead'] === $me['pid'] ) { $live['lead'] = ''; }
					nadlan_tr_save_live( $room, $live );
					return new WP_REST_Response( array( 'ok' => true ), 200 );
				}
				if ( array_key_exists( 'lead', $p ) ) {
					if ( $p['lead'] ) {
						if ( 'rep' !== $me['r'] ) { return nadlan_tr_err( 'role', 403 ); } // "עקבו אחריי" is the representative's
						$live['lead'] = $me['pid'];
					} elseif ( $live['lead'] === $me['pid'] ) {
						$live['lead'] = '';
					}
				}
				$t = 0;
				if ( isset( $p['state'] ) ) {
					if ( $live['lead'] !== $me['pid'] ) { nadlan_tr_save_live( $room, $live ); return nadlan_tr_err( 'not_leader', 409 ); }
					$state      = nadlan_tr_clean_state( $p['state'] );
					$state['n'] = (string) $me['n'];
					$t          = round( microtime( true ), 3 );
					set_transient( 'nltr_s_' . $room, array( 'state' => $state, 't' => $t, 'by' => $me['pid'] ), 6 * HOUR_IN_SECONDS );
					if ( ! empty( $state['f'] ) ) {
						nadlan_tr_keep_sel( (int) $live['post'], (int) $state['f'], ! empty( $state['u'] ) ? substr( (string) strrchr( $state['u'], '-' ), 1 ) : '' );
					}
				}
				nadlan_tr_save_live( $room, $live );
				return new WP_REST_Response( array( 'ok' => true, 't' => $t, 'leader' => (string) $live['lead'] ), 200 );
			},
		),
	) );

	/* the notes: anyone with the room's link reads them; a participant adds one (and deletes his own; a representative any) */
	register_rest_route( $ns, '/room/notes', array(
		array(
			'methods'             => 'GET',
			'permission_callback' => '__return_true',
			'callback'            => function ( WP_REST_Request $req ) {
				$room = nadlan_tr_valid_id( $req->get_param( 'room' ) );
				$post = $room ? nadlan_tr_post( $room ) : 0;
				if ( ! $post ) { return nadlan_tr_err( 'room', 404 ); }
				$live = nadlan_tr_live( $room );
				return new WP_REST_Response( array( 'ok' => true, 'notes' => nadlan_tr_notes( $post ), 'rev' => $live ? (int) $live['rev'] : 0 ), 200 );
			},
		),
		array(
			'methods'             => 'POST',
			'permission_callback' => '__return_true',
			'callback'            => function ( WP_REST_Request $req ) {
				$p    = (array) $req->get_json_params();
				$room = nadlan_tr_valid_id( $p['room'] ?? '' );
				if ( '' === $room ) { return nadlan_tr_err( 'room', 400 ); }
				$live = nadlan_tr_live( $room );
				if ( null === $live ) { return nadlan_tr_err( 'closed', 410 ); }
				$me = nadlan_tr_who( $live, $p['pid'] ?? '', (string) ( $p['key'] ?? '' ) );
				if ( ! $me ) { return nadlan_tr_err( 'who', 403 ); }
				if ( ! nadlan_tr_rl( 'note', 40, 600 ) ) { return nadlan_tr_err( 'rate', 429 ); }
				$post = (int) $live['post'];
				if ( ! empty( $p['delete'] ) ) {
					foreach ( nadlan_tr_notes( $post ) as $n ) {
						if ( (string) $n['id'] === (string) $p['delete'] && ( $n['pid'] === $me['pid'] || 'rep' === $me['r'] ) ) {
							delete_post_meta( $post, '_nltr_note', $n );
							$live['rev'] = (int) $live['rev'] + 1;
							nadlan_tr_save_live( $room, $live );
							return new WP_REST_Response( array( 'ok' => true, 'rev' => (int) $live['rev'] ), 200 );
						}
					}
					return nadlan_tr_err( 'note', 404 );
				}
				$text = trim( sanitize_textarea_field( (string) ( $p['text'] ?? '' ) ) );
				$text = function_exists( 'mb_substr' ) ? mb_substr( $text, 0, 400 ) : substr( $text, 0, 400 );
				if ( '' === $text ) { return nadlan_tr_err( 'text', 400 ); }
				$where = trim( sanitize_text_field( (string) ( $p['where'] ?? '' ) ) );
				$where = function_exists( 'mb_substr' ) ? mb_substr( $where, 0, 60 ) : substr( $where, 0, 60 );
				$all = nadlan_tr_notes( $post );
				if ( count( $all ) >= 200 ) { return nadlan_tr_err( 'full', 409 ); }
				$n = 1;
				foreach ( $all as $x ) { $n = max( $n, (int) $x['n'] + 1 ); }
				$anchor = nadlan_tr_clean_anchor( $p['anchor'] ?? array() );
				$note   = array(
					'id' => nadlan_tr_rand( 8 ), 'n' => $n, 'text' => $text, 'where' => $where, 'anchor' => $anchor,
					'author' => (string) $me['n'], 'role' => (string) $me['r'], 'pid' => (string) $me['pid'],
					'change' => ! empty( $p['change'] ), 't' => time(),
				);
				add_post_meta( $post, '_nltr_note', $note ); // one row per note: two notes at once never overwrite each other
				if ( ! empty( $anchor['floor'] ) ) { nadlan_tr_keep_sel( $post, (int) $anchor['floor'], (string) ( $anchor['side'] ?? '' ) ); }
				$live['rev']                  = (int) $live['rev'] + 1;
				$live['p'][ $me['pid'] ]['s'] = time();
				nadlan_tr_save_live( $room, $live );
				return new WP_REST_Response( array( 'ok' => true, 'note' => $note, 'rev' => (int) $live['rev'] ), 201 );
			},
		),
	) );

	/* is a representative available now? (the hero button's chooser asks at idle time, so a cached page never lies) */
	register_rest_route( $ns, '/room/available', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			$r = new WP_REST_Response( array( 'ok' => true, 'now' => nadlan_tr_rep_now() ), 200 );
			$r->header( 'Cache-Control', 'no-store' );
			return $r;
		},
	) );

	/* the apartment's file, as data: the project, the floor and the side, the numbered notes */
	register_rest_route( $ns, '/room/file', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$room = nadlan_tr_valid_id( $req->get_param( 'room' ) );
			$post = $room ? nadlan_tr_post( $room ) : 0;
			if ( ! $post ) { return nadlan_tr_err( 'room', 404 ); }
			return new WP_REST_Response( nadlan_tr_file( $post, $room ), 200 );
		},
	) );
} );

/* ---------------------------------------------------------------- the page */

if ( ! function_exists( 'nadlan_tr_request' ) ) {
	/** On a project page with the stage: the ?room= value ('new' or a valid id), else ''. */
	function nadlan_tr_request() {
		static $memo = array();
		$raw = isset( $_GET['room'] ) ? (string) wp_unslash( $_GET['room'] ) : null; // phpcs:ignore
		$key = null === $raw ? '' : 'r:' . $raw;
		if ( isset( $memo[ $key ] ) ) { return $memo[ $key ]; }
		$out = '';
		if ( null !== $raw && ! is_admin() && function_exists( 'nadlan_ps_current' ) && nadlan_ps_current() ) {
			$v   = strtolower( sanitize_text_field( $raw ) );
			$out = 'new' === $v ? 'new' : nadlan_tr_valid_id( $v );
		}
		return $memo[ $key ] = $out;
	}
}
if ( ! function_exists( 'nadlan_tr_asset' ) ) {
	function nadlan_tr_asset( $file ) {
		$ver = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
		return plugins_url( 'assets/together/' . $file, dirname( __FILE__ ) ) . '?ver=' . $ver;
	}
}
if ( ! function_exists( 'nadlan_tr_lang' ) ) {
	function nadlan_tr_lang() {
		$l = function_exists( 'nadlan_current_lang' ) ? (string) nadlan_current_lang() : 'he';
		return in_array( $l, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $l : 'he';
	}
}

/* the room's sheet in the head (no flash of the page before the room covers it), only with ?room= */
add_action( 'wp_head', function () {
	if ( '' === nadlan_tr_request() ) { return; }
	echo '<link rel="stylesheet" id="nadlan-together-css" href="' . esc_url( nadlan_tr_asset( 'together.css' ) ) . '">' . "\n";
}, 1000 );

/* the room's container and its script, only with ?room= (after the stage's bridge, which is printed at 60) */
add_action( 'wp_footer', function () {
	$req = nadlan_tr_request();
	if ( '' === $req ) { return; }
	$ps   = nadlan_ps_current();
	$rep  = current_user_can( 'edit_posts' );
	$user = $rep ? wp_get_current_user() : null;
	$cfg  = array(
		'rest'   => esc_url_raw( rest_url( 'nadlan/v1/' ) ),
		'nonce'  => is_user_logged_in() ? wp_create_nonce( 'wp_rest' ) : '',
		'post'   => (int) $ps['id'],
		'name'   => (string) $ps['name'],
		'nameEn' => (string) ( $ps['name_en'] ?? '' ),
		'url'    => (string) get_permalink( (int) $ps['id'] ),
		'wa'     => function_exists( 'nadlan_cta_whatsapp_number' ) ? preg_replace( '/\D/', '', (string) nadlan_cta_whatsapp_number() ) : '',
		'lang'   => nadlan_tr_lang(),
		'canRep' => $rep,
		'user'   => $user ? (string) $user->display_name : '',
		'repNow' => nadlan_tr_rep_now(),
		'lk'     => nadlan_tr_lk_ready(),
		'lkLib'  => NADLAN_TR_LK_LIB,
	);
	echo "\n" . '<div id="nltg-root" hidden data-cfg="' . esc_attr( wp_json_encode( $cfg ) ) . '"></div>' . "\n";
	echo '<script type="module" id="nadlan-together" src="' . esc_url( nadlan_tr_asset( 'together.js' ) ) . '"></script>' . "\n";
}, 70 );

/* the hero button "שיחת וידאו עם נציג": a small chooser while a representative is marked available (else the button keeps
   going to the booking band, as today). The page is the same either way (page caches): the script asks /room/available
   once the page is idle, and only a "yes" turns the button into the chooser. */
add_action( 'wp_footer', function () {
	if ( '' !== nadlan_tr_request() || ! function_exists( 'nadlan_ps_current' ) || ! nadlan_ps_current() ) { return; }
	$l = nadlan_tr_lang();
	$t = array(
		'he' => array( 'חדר צפייה משותף', 'נציג זמין עכשיו. נכנסים יחד לדירה לדוגמה, בווידאו, ואפשר להזמין בן או בת זוג ואנשי מקצוע.', 'עכשיו, בחדר משותף', 'לתאם מועד', 'סגירה' ),
		'en' => array( 'Shared viewing room', 'A representative is available now. Walk through the example apartment together on video, and invite a partner or professionals.', 'Now, in a shared room', 'Book a time', 'Close' ),
		'fr' => array( 'Salle de visite partagée', 'Un conseiller est disponible. Visitez ensemble l’appartement type en vidéo, et invitez un proche ou des professionnels.', 'Maintenant, en salle partagée', 'Prendre rendez-vous', 'Fermer' ),
		'ru' => array( 'Общий просмотр', 'Представитель на связи. Посмотрите пример квартиры вместе по видео и пригласите близких или специалистов.', 'Сейчас, в общей комнате', 'Назначить время', 'Закрыть' ),
		'ar' => array( 'غرفة مشاهدة مشتركة', 'ممثل متاح الآن. تجولوا معًا في الشقة النموذجية بالفيديو، ويمكن دعوة الشريك وأهل الاختصاص.', 'الآن، في غرفة مشتركة', 'تحديد موعد', 'إغلاق' ),
	);
	$s   = $t[ $l ] ?? $t['he'];
	$rtl = in_array( $l, array( 'he', 'ar' ), true );
	?>
<style id="nadlan-together-chooser">
.nltg-ch{position:absolute;z-index:100005;width:min(340px,calc(100vw - 24px));box-sizing:border-box;padding:18px;border-radius:18px;background:#fff;border:1px solid #E2DCD0;box-shadow:0 18px 44px rgba(27,26,23,.18);color:#1B1A17;font-family:Assistant,Heebo,Arial,sans-serif;text-align:start}
.nltg-ch[hidden]{display:none}
.nltg-ch h3{margin:0 0 6px!important;font:600 19px/1.25 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:#1B1A17!important}
.nltg-ch p{margin:0 0 14px!important;font:400 14.5px/1.6 Assistant,Heebo,Arial,sans-serif!important;color:#3B4753!important}
.nltg-ch .r{display:flex;gap:8px;flex-wrap:wrap}
.nltg-ch button{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 16px;border-radius:12px;border:1px solid #E2DCD0;background:#fff;color:#1B1A17;font:700 14.5px/1 Assistant,Heebo,Arial,sans-serif;cursor:pointer;flex:1 1 auto}
.nltg-ch button.t{background:#1F4B5C;border-color:#1F4B5C;color:#fff}
.nltg-ch .x{position:absolute;inset-block-start:8px;inset-inline-end:8px;flex:none;width:44px;min-height:44px;padding:0;border:0;background:transparent;font-size:22px;color:#6B6558}
.nltg-ch button:focus-visible{outline:3px solid #C2563A;outline-offset:2px}
@media(max-width:600px){.nltg-ch button{min-height:48px}}
</style>
<script id="nadlan-together-chooser-js">
(function(){
	var S=<?php echo wp_json_encode( $s, JSON_UNESCAPED_UNICODE ); ?>,RTL=<?php echo $rtl ? 'true' : 'false'; ?>,box=null,opener=null,NOW=false;
	var ask=function(){try{fetch(<?php echo wp_json_encode( esc_url_raw( rest_url( 'nadlan/v1/room/available' ) ) ); ?>,{credentials:'omit',cache:'no-store'}).then(function(r){return r.json()}).then(function(j){NOW=!!(j&&j.now)}).catch(function(){})}catch(e){}};
	if(document.querySelector('a[data-nlps-ev="hero-video"]')){if('requestIdleCallback' in window)requestIdleCallback(ask,{timeout:4000});else setTimeout(ask,2500);}
	function close(){if(box){box.hidden=true;if(opener)opener.focus();}}
	function open(a){
		opener=a;
		if(!box){
			box=document.createElement('div');box.className='nltg-ch';box.setAttribute('role','dialog');box.setAttribute('aria-label',S[0]);box.dir=RTL?'rtl':'ltr';
			var x=document.createElement('button');x.type='button';x.className='x';x.setAttribute('aria-label',S[4]);x.textContent='×';x.onclick=close;
			var h=document.createElement('h3');h.textContent=S[0];var p=document.createElement('p');p.textContent=S[1];
			var r=document.createElement('div');r.className='r';
			var now=document.createElement('button');now.type='button';now.className='t';now.textContent=S[2];
			now.onclick=function(){try{if(window.nadlanGA)window.nadlanGA('room_now_click',{source:'hero-video'})}catch(e){}var u=new URL(location.href);u.searchParams.set('room','new');u.hash='';location.href=u.toString();};
			var later=document.createElement('button');later.type='button';later.textContent=S[3];
			later.onclick=function(){close();var t=document.getElementById('nlsch');if(t)t.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});};
			r.appendChild(now);r.appendChild(later);box.appendChild(x);box.appendChild(h);box.appendChild(p);box.appendChild(r);document.body.appendChild(box);
			document.addEventListener('keydown',function(e){if(e.key==='Escape'&&box&&!box.hidden)close();});
			document.addEventListener('click',function(e){if(box&&!box.hidden&&!box.contains(e.target)&&!(e.target.closest&&e.target.closest('[data-nlps-ev="hero-video"]')))close();},true);
		}
		var rc=a.getBoundingClientRect(),w=Math.min(340,innerWidth-24);
		var left=RTL?rc.right-w:rc.left;left=Math.max(12,Math.min(left,innerWidth-w-12));
		box.style.visibility='hidden';box.hidden=false;
		var hh=box.offsetHeight,top=rc.bottom+8;
		if(top+hh>innerHeight-8&&rc.top-hh-8>8)top=rc.top-hh-8; /* no room under the button: above it */
		box.style.left=(left+scrollX)+'px';box.style.top=(top+scrollY)+'px';box.style.visibility='';box.querySelector('button.t').focus();
	}
	document.addEventListener('click',function(e){
		var a=e.target&&e.target.closest?e.target.closest('a[data-nlps-ev="hero-video"]'):null;
		if(!a||!NOW)return; /* no representative now: the link goes to the booking band, as today */
		e.preventDefault();open(a);
	});
})();
</script>
	<?php
}, 72 );

/* ---------------------------------------------------------------- settings page */

add_action( 'admin_menu', function () {
	add_options_page( 'חדר צפייה משותף', 'חדר צפייה משותף', 'manage_options', 'nadlan-together', function () {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( ! empty( $_POST['nadlan_tr_save'] ) && check_admin_referer( 'nadlan_tr_save' ) ) {
			$url = trim( (string) wp_unslash( $_POST['lk_url'] ?? '' ) ); // phpcs:ignore
			$url = '' === $url ? '' : esc_url_raw( $url, array( 'wss', 'https' ) );
			update_option( 'nadlan_tr_lk_url', $url, false );
			update_option( 'nadlan_tr_lk_key', sanitize_text_field( wp_unslash( $_POST['lk_key'] ?? '' ) ), false ); // phpcs:ignore
			$secret = trim( (string) wp_unslash( $_POST['lk_secret'] ?? '' ) ); // phpcs:ignore
			if ( ! empty( $_POST['lk_secret_clear'] ) ) {
				delete_option( 'nadlan_tr_lk_secret' );
			} elseif ( '' !== $secret ) {
				update_option( 'nadlan_tr_lk_secret', sanitize_text_field( $secret ), false ); // write-only: never printed back
			}
			update_option( 'nadlan_tr_rep_now', empty( $_POST['rep_now'] ) ? '0' : '1', false );
			$days = (int) ( $_POST['retention'] ?? 30 ); // phpcs:ignore
			update_option( 'nadlan_tr_retention', (string) ( $days >= 1 && $days <= 365 ? $days : 30 ), false );
			echo '<div class="notice notice-success"><p>נשמר.</p></div>';
		}
		$has_secret = '' !== (string) nadlan_tr_opt( 'lk_secret' );
		echo '<div class="wrap" dir="rtl" style="font-family:Assistant,Heebo,sans-serif"><h1>חדר צפייה משותף</h1>';
		echo '<p style="max-width:760px">חדר חי בתוך הדירה לדוגמה: הנציג, הקונים, בני המשפחה ואנשי המקצוע באותה דירה, בווידאו, עם הערות שנצמדות לנקודה בדירה ונשמרות בתיק הדירה. הכתובת היא עמוד הפרויקט עם ‎?room=‎. בלי מפתח לייב־קיט החדר עובד בלי וידאו: המבט וההערות מסתנכרנים דרך האתר, ובמקום הווידאו יש כפתור שיחה בוואטסאפ.</p>';
		echo '<form method="post">';
		wp_nonce_field( 'nadlan_tr_save' );
		echo '<table class="form-table" role="presentation">';
		echo '<tr><th scope="row"><label for="nltg-url">כתובת שרת לייב־קיט</label></th><td><input id="nltg-url" type="url" name="lk_url" dir="ltr" value="' . esc_attr( (string) nadlan_tr_opt( 'lk_url' ) ) . '" class="regular-text" placeholder="wss://your-project.livekit.cloud"><p class="description">מתוך פרויקט הלייב־קיט (Settings בפרויקט): הכתובת שמתחילה ב־wss://.</p></td></tr>';
		echo '<tr><th scope="row"><label for="nltg-key">מפתח API</label></th><td><input id="nltg-key" type="text" name="lk_key" dir="ltr" value="' . esc_attr( (string) nadlan_tr_opt( 'lk_key' ) ) . '" class="regular-text" autocomplete="off"></td></tr>';
		echo '<tr><th scope="row"><label for="nltg-secret">סוד API</label></th><td><input id="nltg-secret" type="password" name="lk_secret" dir="ltr" value="" class="regular-text" autocomplete="new-password" placeholder="' . esc_attr( $has_secret ? 'נשמר' : '' ) . '"> ' . ( $has_secret ? '<strong>נשמר</strong>' : '<span>לא הוגדר</span>' ) . '<p class="description">הסוד לא מוצג שוב. מדביקים חדש רק כשמחליפים אותו.</p>' . ( $has_secret ? '<label><input type="checkbox" name="lk_secret_clear" value="1"> למחוק את הסוד השמור</label>' : '' ) . '</td></tr>';
		echo '<tr><th scope="row">נציג זמין עכשיו</th><td><label><input type="checkbox" name="rep_now" value="1"' . checked( nadlan_tr_rep_now(), true, false ) . '> כשמסומן, הכפתור "שיחת וידאו עם נציג" בעמוד הפרויקט מציע גם "עכשיו, בחדר משותף"</label></td></tr>';
		echo '<tr><th scope="row"><label for="nltg-days">שמירת החדרים וההערות (ימים)</label></th><td><input id="nltg-days" type="number" min="1" max="365" name="retention" value="' . esc_attr( (string) nadlan_tr_retention_days() ) . '" class="small-text"><p class="description">אחרי מספר הימים הזה החדר והערותיו נמחקים (בדיקה יומית).</p></td></tr>';
		echo '</table><p class="submit"><button type="submit" name="nadlan_tr_save" value="1" class="button button-primary">שמירה</button></p></form>';
		echo '<p><strong>מצב:</strong> ' . ( nadlan_tr_lk_ready() ? 'לייב־קיט מוגדר: וידאו וערוץ נתונים.' : 'בלי לייב־קיט: סנכרון דרך האתר, בלי וידאו.' ) . '</p>';
		// open a room for a project, as the representative
		if ( function_exists( 'nadlan_ps_config' ) ) {
			echo '<h2>פתיחת חדר</h2><ul>';
			foreach ( nadlan_ps_config() as $slug => $cfg ) {
				$pp = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
				if ( $pp && 'publish' === $pp->post_status ) {
					echo '<li><a class="button" target="_blank" rel="noopener" href="' . esc_url( add_query_arg( 'room', 'new', get_permalink( $pp ) ) ) . '">חדר חדש ב' . esc_html( (string) $cfg['name'] ) . '</a></li>';
				}
			}
			echo '</ul>';
		}
		// the rooms of the last days: live or closed, who is in, how many notes
		$rooms = get_posts( array( 'post_type' => 'nadlan_room', 'post_status' => 'any', 'numberposts' => 30, 'orderby' => 'date', 'order' => 'DESC', 'no_found_rows' => true, 'suppress_filters' => true ) );
		echo '<h2>החדרים האחרונים</h2>';
		if ( ! $rooms ) {
			echo '<p>עדיין אין חדרים.</p>';
		} else {
			echo '<table class="widefat striped" style="max-width:1000px"><thead><tr><th>חדר</th><th>פרויקט</th><th>נפתח</th><th>מצב</th><th>בחדר עכשיו</th><th>הערות</th><th></th></tr></thead><tbody>';
			foreach ( $rooms as $r ) {
				$id   = (string) $r->post_name;
				$pid  = (int) get_post_meta( $r->ID, '_nltr_project', true );
				$live = nadlan_tr_live( $id );
				$in   = array();
				if ( $live ) { foreach ( nadlan_tr_people( $live ) as $pp ) { if ( $pp['on'] ) { $in[] = $pp['name'] . ' (' . $pp['role'] . ')'; } } }
				$url  = get_permalink( $pid );
				echo '<tr><td dir="ltr">' . esc_html( $id ) . '</td><td>' . esc_html( get_the_title( $pid ) ) . '</td><td>' . esc_html( get_date_from_gmt( $r->post_date_gmt, 'j.n.Y H:i' ) ) . ( 'buyer' === get_post_meta( $r->ID, '_nltr_by', true ) ? ' · <strong>קונה מחכה</strong>' : '' ) . '</td>'
					. '<td>' . ( $live ? 'פתוח' : 'נסגר' ) . '</td><td>' . esc_html( implode( ', ', $in ) ) . '</td><td>' . count( nadlan_tr_notes( $r->ID ) ) . '</td>'
					. '<td>' . ( $url ? '<a href="' . esc_url( add_query_arg( 'room', $id, $url ) ) . '" target="_blank" rel="noopener">כניסה</a> · <a href="' . esc_url( add_query_arg( array( 'room' => $id, 'file' => '1' ), $url ) ) . '" target="_blank" rel="noopener">תיק הדירה</a>' : '' ) . '</td></tr>';
			}
			echo '</tbody></table>';
		}
		echo '</div>';
	} );
} );
