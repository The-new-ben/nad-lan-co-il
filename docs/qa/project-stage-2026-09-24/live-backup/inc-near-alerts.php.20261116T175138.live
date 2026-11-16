<?php
/**
 * nadlan-config - Near finder v2: alerts by email (HAD-672 follow-up, owner order 4.11.2026). Release 1.72.585.
 * Design: Claude Design canvas https://claude.ai/artifact/4bwg1ozXd9wjXK42CuAC7y, project/Alerts.dc.html ("NadLan Instruments").
 *
 * What a visitor can ask for, from inside the finder (assets/near-finder/finder.js), email only:
 *  1. new:  a listing for sale or rent published inside the chosen area, with the finder's filters (rooms, price ceiling, ממ״ד);
 *  2. drop: a price drop on a listing saved with the heart ("שמרו"): the old price, the new price, the gap in ₪;
 *  3. proj: a change in a followed project ("עקבו"): the estimated ₪/m² (project_3d_avg_price_per_sqm), the stage
 *           (project_status) or the number of units (num_units).
 *  The area ₪/m² alert is NOT offered: the site has no live source for it (the deals table is empty, /avm answers
 *  insufficient_data, data/radius-prices.json is a snapshot of 28 projects with deals up to 08.2024). Never faked.
 *  Frequency: immediately (a single event 5 minutes after a change, at most one mail per 30 minutes), daily, weekly.
 *
 * Reuse, not a parallel system:
 *  - the store is the existing private CPT nadlan_saved_search (inc/saved-search.php), with its meta names email, token,
 *    params, confirmed, last_run; an alert row is post_status 'private' + meta kind = 'nf'. The old daily loop
 *    nadlan_ss_run_alerts() reads get_posts() without a post_status (= 'publish' only), so it never touches these rows;
 *  - the schedule is the existing daily cron nadlan_ss_daily (priority 20, after the old loop), plus one single event
 *    nadlan_na_instant for the "immediately" rows, scheduled only while such a confirmed row exists;
 *  - the sender is wp_mail, so inc/mailer.php's envelope, DKIM and the Brevo SMTP (when the owner saved a key) apply;
 *  - the admin list is the CPT's own screen (columns, the last send result); delete = the normal trash / delete.
 *
 * Privacy (Privacy Protection Law, amendment 13, and the site's notice): the sheet says at the point of collection what the
 * email is for, that it is voluntary and what refusing means, who keeps it and how to reach them, and links the policy.
 * Double opt-in: nothing but the confirmation mail is sent until the visitor confirms (a button on the page the mail
 * links to, so a mail scanner that opens links cannot confirm). Every mail carries a one-click unsubscribe link with a
 * signed token (HMAC of the row and its random token) and the List-Unsubscribe headers; unsubscribing deletes the row.
 * Stored: the email, the area (the centre rounded to 0.001°, about 100 m, a radius and a place name the server checks),
 * the filters, the frequency, the saved or followed ids, the consent time. Never the visitor's live location, never an IP.
 * URLs carry only the row id and its signed token. Unconfirmed rows are deleted after 7 days. Sign-ups are rate-limited
 * per device (6 an hour) and per email (3 confirmation mails a day); the generic public-POST limit applies too.
 *
 * Price history: every change of nadlan_property price and of nadlan_project psqm / status / units is recorded on save
 * (any update_post_meta, also a delete + add) as meta _nadlan_ph, a list of {t, k, o, n} (time, key, old, new), last 40.
 * A drop is computed from that history only, never from a guess. The first publish time of a listing is _nadlan_pub_at.
 * Honesty: a mail names only real published items: never a demo (nadlan_pl_is_demo, slug -demo), never rented or sold,
 * never nadlan_nf_hidden. A drop of more than half is treated as a typing error and not sent.
 *
 * v3 (release 1.72.586): the area may be the zone the visitor drew on the map: params.poly = up to 60 [lat, lng] points
 * rounded to 4 decimals (about 11 m), inside Israel, at most 0.6° across; its centre (rounded to 0.001°) names it and r is 0.
 * The new-listing alert also keeps the v3 filters: rooms from-to (halves), price from-to, m² from-to, floor from-to,
 * elevator, parking, balcony. A listing that does not state a fact never matches a filter on that fact. The notice
 * version moved to nf3 (the sheet now names the drawn zone among what is kept).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NADLAN_NA_NOTICE' ) ) {
	define( 'NADLAN_NA_NOTICE', 'nf3-2026-11-04' ); // the version of the collection notice the visitor saw (kept with the consent); nf3: the drawn zone
}

if ( ! function_exists( 'nadlan_na_enabled' ) ) {
	/**
	 * Email alerts are DORMANT until the owner turns them on (Settings › "מייל יוצא (Brevo)": option nadlan_na_enabled = '1';
	 * absent = off, the default). Off: the portal pages print no #nlna-cfg, so the finder shows no alert button, no alert sheet,
	 * no "עקבו" and no alert circle (the heart stays: a device-only saved list); the sign-up and items routes answer 403
	 * 'disabled'; no event is scheduled and no mail is sent. The confirm and unsubscribe links keep working, so an old link
	 * never breaks. The price history keeps recording on save: it costs nothing and builds the drop history.
	 */
	function nadlan_na_enabled() { return '1' === (string) get_option( 'nadlan_na_enabled', '' ); }
}

/* ================================================================ 1. the price history (on save) */
if ( ! function_exists( 'nadlan_na_watched' ) ) {
	/** The short name of a watched meta key on this post, or ''. */
	function nadlan_na_watched( $pid, $key ) {
		static $w = array(
			'nadlan_property' => array( 'price' => 'price' ),
			'nadlan_project'  => array( 'project_3d_avg_price_per_sqm' => 'psqm', 'project_status' => 'status', 'num_units' => 'units' ),
		);
		if ( ! in_array( $key, array( 'price', 'project_3d_avg_price_per_sqm', 'project_status', 'num_units' ), true ) ) { return ''; }
		$pt = get_post_type( (int) $pid );
		return isset( $w[ $pt ][ $key ] ) ? $w[ $pt ][ $key ] : '';
	}

	/** A project's stage as the enum the finder uses (inc/drone-map.php), '' when unknown. */
	function nadlan_na_status_enum( $raw ) {
		$raw = trim( (string) $raw );
		$map = array(
			'marketing' => 'marketing', 'construction' => 'construction', 'planning' => 'planning', 'completed' => 'completed', 'permits' => 'permits',
			'בשיווק' => 'marketing', 'שיווק' => 'marketing', 'בביצוע' => 'construction', 'בבנייה' => 'construction', 'ביצוע' => 'construction',
			'בתכנון' => 'planning', 'תכנון' => 'planning', 'מאושר' => 'planning', 'בהיתר' => 'permits',
			'הסתיים' => 'completed', 'אוכלס' => 'completed', 'הושלם' => 'completed',
		);
		return isset( $map[ $raw ] ) ? $map[ $raw ] : '';
	}

	/** A value as the history keeps it: whole shekels / units, or the stage enum ('?raw' when the stage is not known). */
	function nadlan_na_norm( $short, $v ) {
		if ( is_array( $v ) || is_object( $v ) ) { return null; }
		if ( 'status' === $short ) {
			$raw = trim( (string) $v );
			$e   = nadlan_na_status_enum( $raw );
			return '' !== $e ? $e : ( '' === $raw ? '' : '?' . mb_substr( $raw, 0, 30 ) );
		}
		$s = preg_replace( '/[^0-9.]/', '', (string) $v ); // "4,200,000" -> 4200000
		return '' === $s ? 0 : (int) round( (float) $s );
	}

	function nadlan_na_hist( $pid ) {
		$h = get_post_meta( (int) $pid, '_nadlan_ph', true );
		return is_array( $h ) ? array_values( $h ) : array();
	}

	/** Append one change (old != new) to the post's history; the last 40 are kept. */
	function nadlan_na_hist_push( $pid, $short, $old, $new, $t = null ) {
		$o = nadlan_na_norm( $short, $old );
		$n = nadlan_na_norm( $short, $new );
		if ( null === $o || null === $n || $o === $n ) { return false; }
		$h   = nadlan_na_hist( $pid );
		$h[] = array( 't' => $t ? (int) $t : time(), 'k' => $short, 'o' => $o, 'n' => $n );
		if ( count( $h ) > 40 ) { $h = array_slice( $h, -40 ); }
		update_post_meta( (int) $pid, '_nadlan_ph', $h );
		nadlan_na_poke();
		return true;
	}

	/** The old value of a watched key, kept between the "before" filter and the "after" action of the same request. */
	function nadlan_na_stash( $op, $pid, $key, $val = null ) {
		static $s = array();
		$k = (int) $pid . '|' . $key;
		if ( 'set' === $op ) { $s[ $k ] = $val; return null; }
		if ( ! array_key_exists( $k, $s ) ) { return array( false, null ); }
		$v = $s[ $k ];
		unset( $s[ $k ] );
		return array( true, $v );
	}
}

add_filter( 'update_post_metadata', function ( $check, $pid, $key, $value, $prev ) {
	if ( null === $check && '' !== nadlan_na_watched( (int) $pid, (string) $key ) && metadata_exists( 'post', (int) $pid, (string) $key ) ) {
		nadlan_na_stash( 'set', (int) $pid, (string) $key, get_post_meta( (int) $pid, (string) $key, true ) );
	}
	return $check;
}, 5, 5 );
add_filter( 'delete_post_metadata', function ( $check, $pid, $key, $value, $all ) { // a delete followed by an add is a change too
	if ( null === $check && ! $all && '' !== nadlan_na_watched( (int) $pid, (string) $key ) && metadata_exists( 'post', (int) $pid, (string) $key ) ) {
		nadlan_na_stash( 'set', (int) $pid, (string) $key, get_post_meta( (int) $pid, (string) $key, true ) );
	}
	return $check;
}, 5, 5 );
foreach ( array( 'updated_post_meta', 'added_post_meta' ) as $nadlan_na_hook ) {
	add_action( $nadlan_na_hook, function ( $mid, $pid, $key, $value ) {
		$short = nadlan_na_watched( (int) $pid, (string) $key );
		if ( '' === $short ) { return; }
		list( $had, $old ) = nadlan_na_stash( 'take', (int) $pid, (string) $key );
		if ( $had ) { nadlan_na_hist_push( (int) $pid, $short, $old, $value ); }
	}, 5, 4 );
}
unset( $nadlan_na_hook );

/* the first time a listing is published (the free wizard creates 'pending'; an admin's approval is the moment it is new) */
add_action( 'transition_post_status', function ( $new, $old, $post ) {
	if ( 'publish' !== $new || 'publish' === $old || ! $post || 'nadlan_property' !== $post->post_type ) { return; }
	if ( '' === (string) get_post_meta( $post->ID, '_nadlan_pub_at', true ) ) {
		update_post_meta( $post->ID, '_nadlan_pub_at', time() );
		nadlan_na_poke();
	}
}, 20, 3 );

/* ================================================================ 2. the detectors (pure: no WordPress call) */
if ( ! function_exists( 'nadlan_na_drop' ) ) {
	/**
	 * A price drop in the history after $since. The old price is the price at $since (the first change's old value, or
	 * when the listing had no price then, its first price after it); the new price is the last recorded one and must be
	 * the price the listing carries now ($current), else the history missed a write and nothing is said.
	 * Returns null (no drop), array( 'skip' => reason ), or array( old, new, gap, pct, t ).
	 */
	function nadlan_na_drop( $hist, $since, $current ) {
		$e = array();
		foreach ( (array) $hist as $x ) {
			if ( is_array( $x ) && 'price' === ( $x['k'] ?? '' ) && (int) ( $x['t'] ?? 0 ) > (int) $since ) { $e[] = $x; }
		}
		if ( ! $e ) { return null; }
		usort( $e, function ( $a, $b ) { return (int) $a['t'] - (int) $b['t']; } );
		$base = (int) $e[0]['o'];
		if ( $base <= 0 ) {
			$base = 0;
			foreach ( $e as $x ) { if ( (int) $x['n'] > 0 ) { $base = (int) $x['n']; break; } }
		}
		$last = $e[ count( $e ) - 1 ];
		$new  = (int) $last['n'];
		if ( (int) $current !== $new ) { return array( 'skip' => 'inconsistent' ); }
		if ( $base <= 0 || $new <= 0 || $new >= $base ) { return null; }
		if ( $new < $base * 0.5 ) { return array( 'skip' => 'suspect', 'old' => $base, 'new' => $new ); } // a typing error, not a drop
		return array( 'old' => $base, 'new' => $new, 'gap' => $base - $new, 'pct' => round( ( $base - $new ) * 100 / $base, 1 ), 't' => (int) $last['t'] );
	}

	/**
	 * A followed project's changes after $since, per key: from the value at $since to the value now. $current = the values
	 * now (key => normalized value); a key whose last recorded value is not the current one is left out. Stages only when
	 * both are known; numbers only when both are positive and within a factor of 2 (beyond that it is a data fix).
	 */
	function nadlan_na_proj_changes( $hist, $since, $current = array() ) {
		$by = array();
		foreach ( (array) $hist as $x ) {
			$k = is_array( $x ) ? (string) ( $x['k'] ?? '' ) : '';
			if ( in_array( $k, array( 'psqm', 'status', 'units' ), true ) && (int) ( $x['t'] ?? 0 ) > (int) $since ) { $by[ $k ][] = $x; }
		}
		$out = array();
		foreach ( array( 'psqm', 'status', 'units' ) as $k ) {
			if ( empty( $by[ $k ] ) ) { continue; }
			$e = $by[ $k ];
			usort( $e, function ( $a, $b ) { return (int) $a['t'] - (int) $b['t']; } );
			$from = $e[0]['o'];
			$to   = $e[ count( $e ) - 1 ]['n'];
			if ( array_key_exists( $k, (array) $current ) && $current[ $k ] !== $to ) { continue; }
			if ( $from === $to ) { continue; }
			if ( 'status' === $k ) {
				if ( ! is_string( $from ) || ! is_string( $to ) || '' === $from || '' === $to || '?' === $from[0] || '?' === $to[0] ) { continue; }
			} else {
				$a = (int) $from; $b = (int) $to;
				if ( $a <= 0 || $b <= 0 || max( $a, $b ) > 2 * min( $a, $b ) ) { continue; }
			}
			$out[] = array( 'k' => $k, 'from' => $from, 'to' => $to );
		}
		return $out;
	}

	function nadlan_na_km( $lat1, $lng1, $lat2, $lng2 ) {
		$t = M_PI / 180;
		$x = sin( ( $lat2 - $lat1 ) * $t / 2 ) ** 2 + cos( $lat1 * $t ) * cos( $lat2 * $t ) * sin( ( $lng2 - $lng1 ) * $t / 2 ) ** 2;
		return 2 * 6371 * asin( min( 1, sqrt( $x ) ) );
	}

	/** Is a point inside a polygon of [lat, lng] points (even-odd rule; the ring need not be closed)? */
	function nadlan_na_in_poly( $lat, $lng, $poly ) {
		$poly = array_values( (array) $poly );
		$n    = count( $poly );
		if ( $n < 3 ) { return false; }
		$in = false;
		for ( $i = 0, $j = $n - 1; $i < $n; $j = $i++ ) {
			$ai = (float) $poly[ $i ][0]; $oi = (float) $poly[ $i ][1]; $aj = (float) $poly[ $j ][0]; $oj = (float) $poly[ $j ][1];
			if ( ( $ai > $lat ) !== ( $aj > $lat ) && $lng < ( $oj - $oi ) * ( $lat - $ai ) / ( ( $aj - $ai ) ?: 1e-12 ) + $oi ) { $in = ! $in; }
		}
		return $in;
	}

	/** Does a listing row (nadlan_na_listing_row) match a row's area and filters? A fact the listing does not state never matches. */
	function nadlan_na_matches( $row, $p ) {
		if ( ! $row || null === $row['lat'] || null === $row['lng'] ) { return false; }
		if ( ! empty( $p['deal'] ) && $p['deal'] !== $row['deal'] ) { return false; }
		if ( ! empty( $p['rooms'] ) && ! ( (float) $row['rooms'] >= (float) $p['rooms'] ) ) { return false; }
		if ( ! empty( $p['rmax'] ) && ! ( (float) $row['rooms'] > 0 && (float) $row['rooms'] <= (float) $p['rmax'] ) ) { return false; }
		if ( ! empty( $p['pmin'] ) && ! ( $row['price'] > 0 && $row['price'] >= (int) $p['pmin'] ) ) { return false; }
		if ( ! empty( $p['pmax'] ) && ! ( $row['price'] > 0 && $row['price'] <= (int) $p['pmax'] ) ) { return false; }
		if ( ! empty( $p['smin'] ) && ! ( (int) ( $row['sqm'] ?? 0 ) > 0 && (int) $row['sqm'] >= (int) $p['smin'] ) ) { return false; }
		if ( ! empty( $p['smax'] ) && ! ( (int) ( $row['sqm'] ?? 0 ) > 0 && (int) $row['sqm'] <= (int) $p['smax'] ) ) { return false; }
		$fl = array_key_exists( 'floor', (array) $row ) ? $row['floor'] : null;
		if ( isset( $p['fmin'] ) && null !== $p['fmin'] && ! ( null !== $fl && (int) $fl >= (int) $p['fmin'] ) ) { return false; }
		if ( isset( $p['fmax'] ) && null !== $p['fmax'] && ! ( null !== $fl && (int) $fl <= (int) $p['fmax'] ) ) { return false; }
		if ( ! empty( $p['mamad'] ) && empty( $row['mamad'] ) ) { return false; }
		if ( ! empty( $p['elev'] ) && empty( $row['elevator'] ) ) { return false; }
		if ( ! empty( $p['park'] ) && empty( $row['parking'] ) ) { return false; }
		if ( ! empty( $p['balc'] ) && ! ( (int) ( $row['balcony'] ?? 0 ) > 0 ) ) { return false; }
		if ( ! empty( $p['poly'] ) && is_array( $p['poly'] ) ) { return nadlan_na_in_poly( (float) $row['lat'], (float) $row['lng'], $p['poly'] ); }
		return nadlan_na_km( (float) $p['lat'], (float) $p['lng'], (float) $row['lat'], (float) $row['lng'] ) <= (float) $p['r'] + 0.0001;
	}

	/** The visitor's drawn zone from a request: up to 60 [lat, lng] points rounded to 4 decimals inside Israel, at most 0.6°
	 *  across. array() when none was sent, false when one was sent and is not a usable zone. */
	function nadlan_na_poly_in( $raw ) {
		if ( empty( $raw ) ) { return array(); }
		if ( ! is_array( $raw ) || count( $raw ) > 61 ) { return false; }
		$out = array();
		foreach ( $raw as $pt ) {
			if ( ! is_array( $pt ) || ! isset( $pt[0], $pt[1] ) || ! is_numeric( $pt[0] ) || ! is_numeric( $pt[1] ) ) { return false; }
			$a = round( (float) $pt[0], 4 ); $o = round( (float) $pt[1], 4 );
			if ( $a < 29.3 || $a > 33.5 || $o < 34.2 || $o > 35.95 ) { return false; }
			$last = $out ? $out[ count( $out ) - 1 ] : null;
			if ( ! $last || $last[0] !== $a || $last[1] !== $o ) { $out[] = array( $a, $o ); }
		}
		if ( count( $out ) > 3 && $out[0] === $out[ count( $out ) - 1 ] ) { array_pop( $out ); } // a closed ring is kept open
		if ( count( $out ) < 3 || count( $out ) > 60 ) { return false; }
		$la = array_column( $out, 0 ); $lo = array_column( $out, 1 );
		if ( max( $la ) - min( $la ) > 0.6 || max( $lo ) - min( $lo ) > 0.6 || max( $la ) - min( $la ) < 0.0005 || max( $lo ) - min( $lo ) < 0.0005 ) { return false; }
		return $out;
	}
}

/* ================================================================ 3. the rows */
if ( ! function_exists( 'nadlan_na_sig' ) ) {
	function nadlan_na_sig( $act, $sid ) {
		$tok = (string) get_post_meta( (int) $sid, 'token', true );
		if ( '' === $tok ) { return ''; }
		return substr( hash_hmac( 'sha256', 'nlna|' . $act . '|' . (int) $sid . '|' . $tok, wp_salt( 'auth' ) ), 0, 32 );
	}
	function nadlan_na_check( $act, $sid, $sig ) {
		$sid = (int) $sid;
		if ( $sid <= 0 || ! is_string( $sig ) || '' === $sig || 'nadlan_saved_search' !== get_post_type( $sid ) || 'nf' !== (string) get_post_meta( $sid, 'kind', true ) ) { return false; }
		$want = nadlan_na_sig( $act, $sid );
		return '' !== $want && hash_equals( $want, $sig );
	}
	function nadlan_na_url( $act, $sid ) {
		return add_query_arg( array( 's' => (int) $sid, 't' => nadlan_na_sig( $act, $sid ) ), rest_url( 'nadlan/v1/near-alerts/' . $act ) );
	}
	function nadlan_na_ids( $v ) { // stored id => time maps
		$out = array();
		foreach ( (array) $v as $id => $t ) { if ( (int) $id > 0 ) { $out[ (int) $id ] = (int) $t; } }
		return $out;
	}
	function nadlan_na_get( $sid ) {
		$sid = (int) $sid;
		$p   = json_decode( (string) get_post_meta( $sid, 'params', true ), true );
		$w   = get_post_meta( $sid, 'nf_what', true );
		return array(
			'id'        => $sid,
			'email'     => (string) get_post_meta( $sid, 'email', true ),
			'p'         => is_array( $p ) ? $p : array(),
			'what'      => is_array( $w ) ? array_values( $w ) : array(),
			'freq'      => (string) get_post_meta( $sid, 'nf_freq', true ),
			'items'     => nadlan_na_ids( get_post_meta( $sid, 'nf_items', true ) ),
			'follow'    => nadlan_na_ids( get_post_meta( $sid, 'nf_follow', true ) ),
			'confirmed' => '1' === (string) get_post_meta( $sid, 'confirmed', true ),
			'last_run'  => (int) get_post_meta( $sid, 'last_run', true ),
			'sent_at'   => (int) get_post_meta( $sid, 'nf_sent_at', true ),
			'seen'      => array_map( 'intval', (array) get_post_meta( $sid, 'nf_seen', true ) ),
		);
	}
	function nadlan_na_freq_text( $f ) {
		return 'now' === $f ? 'מיד כשיש עדכון' : ( 'week' === $f ? 'פעם בשבוע' : 'פעם ביום' );
	}
	function nadlan_na_where( $p ) { // "רמת אביב והסביבה", for subjects and mails
		$l = trim( (string) ( $p['label'] ?? '' ) );
		return '' !== $l ? $l . ' והסביבה' : ( ! empty( $p['poly'] ) ? 'האזור שציירתם במפה' : 'האזור שסימנתם במפה' );
	}
	function nadlan_na_scope( $p ) { // v3: "ברדיוס 1.5 ק״מ", or for a drawn zone "באזור שציירתם במפה"
		if ( ! empty( $p['poly'] ) ) { return 'באזור שציירתם במפה'; }
		return 'ברדיוס ' . rtrim( rtrim( number_format( (float) ( $p['r'] ?? 1.5 ), 1 ), '0' ), '.' ) . ' ק״מ';
	}
	function nadlan_na_privacy_url() {
		$u = function_exists( 'get_privacy_policy_url' ) ? get_privacy_policy_url() : '';
		return $u ? $u : home_url( '/privacy/' );
	}
	function nadlan_na_limit( $bucket, $max, $window ) {
		$k = 'nadlan_na_rl_' . md5( (string) $bucket );
		$n = (int) get_transient( $k );
		if ( $n >= $max ) { return false; }
		set_transient( $k, $n + 1, $window );
		return true;
	}
	function nadlan_na_client() {
		if ( function_exists( 'nadlan_hardening_client_key' ) ) { return nadlan_hardening_client_key(); }
		return 'ip' . md5( substr( (string) ( $_SERVER['REMOTE_ADDR'] ?? '' ), 0, 80 ) ); // phpcs:ignore -- hashed, never stored
	}
	function nadlan_na_recount() {
		$ids = get_posts( array( 'post_type' => 'nadlan_saved_search', 'post_status' => 'private', 'posts_per_page' => -1, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
			'meta_query' => array( array( 'key' => 'kind', 'value' => 'nf' ), array( 'key' => 'confirmed', 'value' => '1' ), array( 'key' => 'nf_freq', 'value' => 'now' ) ) ) );
		update_option( 'nadlan_na_now', count( $ids ) );
	}
	/** An "immediately" row may be due: one single event, 5 minutes on, so a batch of edits makes one mail. */
	function nadlan_na_poke() {
		if ( ! nadlan_na_enabled() || (int) get_option( 'nadlan_na_now', 0 ) < 1 || wp_next_scheduled( 'nadlan_na_instant' ) ) { return; }
		wp_schedule_single_event( time() + 5 * MINUTE_IN_SECONDS, 'nadlan_na_instant' );
	}
}

/* ---------------------------------------------------------------- what may be named in a mail */
if ( ! function_exists( 'nadlan_na_listing_ok' ) ) {
	function nadlan_na_gone( $id ) {
		$g = array( 'rented', 'sold', 'מושכר', 'נמכר', 'הושכר' );
		return in_array( strtolower( trim( (string) get_post_meta( $id, 'status', true ) ) ), $g, true )
			|| in_array( strtolower( trim( (string) get_post_meta( $id, 'nl_status', true ) ) ), $g, true );
	}
	function nadlan_na_listing_ok( $id ) {
		$p = get_post( (int) $id );
		if ( ! $p || 'nadlan_property' !== $p->post_type || 'publish' !== $p->post_status || preg_match( '/-demo$/', (string) $p->post_name ) ) { return false; }
		if ( function_exists( 'nadlan_nf_is_demo' ) && nadlan_nf_is_demo( (int) $id ) ) { return false; }
		if ( '1' === (string) get_post_meta( $id, 'nadlan_nf_hidden', true ) || nadlan_na_gone( $id ) ) { return false; }
		return in_array( (string) get_post_meta( $id, 'listing_type', true ), array( 'sale', 'rent' ), true );
	}
	function nadlan_na_project_ok( $id ) {
		$p = get_post( (int) $id );
		return $p && 'nadlan_project' === $p->post_type && 'publish' === $p->post_status && '1' !== (string) get_post_meta( $id, 'nadlan_nf_hidden', true );
	}
	/** A listing as a mail shows it (the finder's own placement: its point, else its neighbourhood, else its city). */
	function nadlan_na_listing_row( $id ) {
		static $c = array();
		$id = (int) $id;
		if ( array_key_exists( $id, $c ) ) { return $c[ $id ]; }
		if ( ! nadlan_na_listing_ok( $id ) ) { return $c[ $id ] = null; }
		$city = trim( (string) get_post_meta( $id, 'city', true ) );
		$hood = trim( (string) get_post_meta( $id, 'neighborhood', true ) );
		$pl   = function_exists( 'nadlan_nf_place' ) ? nadlan_nf_place( $id, $city, $hood ) : array( 'lat' => null, 'lng' => null, 'approx' => 'none', 'area' => '' );
		$types = array( 'apartment' => 'דירה', 'penthouse' => 'פנטהאוז', 'garden' => 'דירת גן', 'cottage' => 'קוטג׳', 'villa' => 'בית פרטי', 'duplex' => 'דופלקס', 'studio' => 'סטודיו', 'house' => 'בית פרטי', 'land' => 'מגרש', 'office' => 'משרד' );
		$img  = '';
		if ( function_exists( 'nadlan_nf_thumbs' ) ) { $th = nadlan_nf_thumbs( array( $id ) ); $img = $th[ $id ] ?? ''; }
		$x = function_exists( 'nadlan_nf_extras' ) ? nadlan_nf_extras( $id ) : array( 'floor' => null, 'elevator' => false, 'parking' => false, 'balcony' => 0 ); // v3: the filters' facts
		$c[ $id ] = $x + array(
			'id'     => $id,
			'url'    => get_permalink( $id ),
			'title'  => html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ),
			'deal'   => (string) get_post_meta( $id, 'listing_type', true ),
			'ptype'  => $types[ (string) get_post_meta( $id, 'property_type', true ) ] ?? '',
			'price'  => nadlan_na_norm( 'price', get_post_meta( $id, 'price', true ) ),
			'rooms'  => max( 0, (float) get_post_meta( $id, 'rooms', true ) ),
			'sqm'    => max( 0, (int) round( (float) get_post_meta( $id, 'size_sqm', true ) ) ),
			'mamad'  => in_array( strtolower( (string) get_post_meta( $id, 'protected_room', true ) ), array( '1', 'true', 'yes', 'on' ), true ),
			'city'   => $city,
			'hood'   => $hood,
			'lat'    => $pl['lat'],
			'lng'    => $pl['lng'],
			'approx' => $pl['approx'],
			'img'    => $img,
		);
		return $c[ $id ];
	}
	/** Up to 30 ids of one kind that may be named (published, real). */
	function nadlan_na_clean_ids( $ids, $pt ) {
		$out = array();
		foreach ( array_slice( array_unique( array_map( 'intval', (array) $ids ) ), 0, 30 ) as $id ) {
			if ( $id > 0 && ( 'nadlan_property' === $pt ? nadlan_na_listing_ok( $id ) : nadlan_na_project_ok( $id ) ) ) { $out[] = $id; }
		}
		return $out;
	}
	/** The places the finder's own data names: neighbourhood and city centroids (inc/near-finder.php). norm => [name, lat, lng, kind]. */
	function nadlan_na_places() {
		static $k = null;
		if ( null !== $k ) { return $k; }
		$k = array();
		if ( function_exists( 'nadlan_nf_hoods' ) ) {
			foreach ( nadlan_nf_hoods() as $h ) { $k[ nadlan_nf_norm( $h[2] ) ] = array( $h[2], (float) $h[0], (float) $h[1], 'hood' ); }
		}
		if ( function_exists( 'nadlan_nf_cities' ) ) {
			foreach ( nadlan_nf_cities() as $name => $ll ) { $n = nadlan_nf_norm( $name ); if ( ! isset( $k[ $n ] ) ) { $k[ $n ] = array( (string) $name, (float) $ll[0], (float) $ll[1], 'city' ); } }
		}
		return $k;
	}
	/**
	 * The area's name in a mail. The visitor's hint is used only when it is one of the finder's own places and lies near
	 * the point; otherwise the nearest neighbourhood (1.5 km) or city (5 km); otherwise ''. Never the requester's free text.
	 */
	function nadlan_na_label( $lat, $lng, $hint ) {
		$K = nadlan_na_places();
		$h = function_exists( 'nadlan_nf_norm' ) ? nadlan_nf_norm( (string) $hint ) : trim( (string) $hint );
		if ( '' !== $h && isset( $K[ $h ] ) && nadlan_na_km( $lat, $lng, $K[ $h ][1], $K[ $h ][2] ) <= ( 'city' === $K[ $h ][3] ? 8 : 3 ) ) { return $K[ $h ][0]; }
		$best = ''; $bd = 1e9;
		foreach ( $K as $p ) {
			$d = nadlan_na_km( $lat, $lng, $p[1], $p[2] );
			$s = 'hood' === $p[3] ? $d : $d + 10; // a neighbourhood before a city
			if ( $d <= ( 'hood' === $p[3] ? 1.5 : 5 ) && $s < $bd ) { $bd = $s; $best = $p[0]; }
		}
		return $best;
	}
}

/* ================================================================ 4. REST */
if ( ! function_exists( 'nadlan_na_rest' ) ) {
	function nadlan_na_rest( $data, $status = 200 ) {
		$r = new WP_REST_Response( $data, $status );
		$r->header( 'Cache-Control', 'no-store' );
		return $r;
	}

	/** POST /nadlan/v1/near-alerts: a new request; one confirmation mail; nothing else until it is confirmed. */
	function nadlan_na_signup( $req ) {
		if ( ! nadlan_na_enabled() ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'disabled' ), 200 ); } // dormant (200: the uPress edge swaps a PHP 403 for its own nginx 405 page)
		$p = $req->get_json_params();
		if ( ! is_array( $p ) ) { $p = (array) $req->get_body_params(); }
		if ( ! empty( $p['company'] ) ) { return nadlan_na_rest( array( 'ok' => true, 'confirm' => true ) ); } // the honeypot: looks done, nothing happens
		$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
		if ( ! is_email( $email ) || strlen( $email ) > 100 ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'email' ), 400 ); }
		$poly = nadlan_na_poly_in( $p['poly'] ?? null ); // v3: the zone the visitor drew
		if ( false === $poly ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'area' ), 400 ); }
		if ( $poly ) { // the zone's centre names it; the radius does not apply
			$lat = array_sum( array_column( $poly, 0 ) ) / count( $poly );
			$lng = array_sum( array_column( $poly, 1 ) ) / count( $poly );
		} else {
			$lat = (float) ( $p['lat'] ?? 0 );
			$lng = (float) ( $p['lng'] ?? 0 );
		}
		if ( $lat < 29.3 || $lat > 33.5 || $lng < 34.2 || $lng > 35.95 ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'area' ), 400 ); }
		$lat = round( $lat, 3 ); // about 100 m: the area, never the visitor's exact place
		$lng = round( $lng, 3 );
		$r   = 1.5;
		foreach ( array( 1, 1.5, 2, 3, 5 ) as $ok ) { if ( abs( (float) ( $p['r'] ?? 0 ) - $ok ) < 0.01 ) { $r = (float) $ok; } }
		if ( $poly ) { $r = 0; }
		$deal  = in_array( (string) ( $p['deal'] ?? '' ), array( 'sale', 'rent' ), true ) ? (string) $p['deal'] : '';
		$half  = function ( $v ) { $v = round( (float) $v * 2 ) / 2; return $v >= 1 && $v <= 10 ? ( floor( $v ) == $v ? (int) $v : $v ) : 0; }; // rooms 1 to 10, halves (v2 sent 3, 4 or 5)
		$rooms = $half( $p['rooms'] ?? 0 );
		$rmax  = $half( $p['rmax'] ?? 0 );
		if ( $rooms && $rmax && $rmax < $rooms ) { list( $rooms, $rmax ) = array( $rmax, $rooms ); }
		$pmax  = max( 0, min( 100000000, (int) ( $p['pmax'] ?? 0 ) ) );
		$pmin  = max( 0, min( 100000000, (int) ( $p['pmin'] ?? 0 ) ) );
		if ( $pmin && $pmax && $pmin > $pmax ) { list( $pmin, $pmax ) = array( $pmax, $pmin ); }
		$smin  = max( 0, min( 5000, (int) ( $p['smin'] ?? 0 ) ) );
		$smax  = max( 0, min( 5000, (int) ( $p['smax'] ?? 0 ) ) );
		if ( $smin && $smax && $smin > $smax ) { list( $smin, $smax ) = array( $smax, $smin ); }
		$flo   = function ( $v ) { return null !== $v && '' !== $v && is_numeric( $v ) && (int) $v >= -3 && (int) $v <= 120 ? (int) $v : null; };
		$fmin  = $flo( $p['fmin'] ?? null );
		$fmax  = $flo( $p['fmax'] ?? null );
		if ( null !== $fmin && null !== $fmax && $fmin > $fmax ) { list( $fmin, $fmax ) = array( $fmax, $fmin ); }
		$mamad = ! empty( $p['mamad'] );
		$elev  = ! empty( $p['elev'] );
		$park  = ! empty( $p['park'] );
		$balc  = ! empty( $p['balc'] );
		$what  = array_values( array_intersect( array( 'new', 'drop', 'proj' ), array_map( 'strval', (array) ( $p['what'] ?? array() ) ) ) );
		if ( ! $what ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'what' ), 400 ); }
		$freq   = in_array( (string) ( $p['freq'] ?? '' ), array( 'now', 'day', 'week' ), true ) ? (string) $p['freq'] : 'day';
		$items  = in_array( 'drop', $what, true ) ? nadlan_na_clean_ids( $p['items'] ?? array(), 'nadlan_property' ) : array();
		$follow = in_array( 'proj', $what, true ) ? nadlan_na_clean_ids( $p['follow'] ?? array(), 'nadlan_project' ) : array();
		if ( ! nadlan_na_limit( 'su|' . nadlan_na_client(), 6, HOUR_IN_SECONDS ) ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'rate' ), 429 ); }
		$em = strtolower( $email );
		if ( ! nadlan_na_limit( 'em|' . $em, 3, DAY_IN_SECONDS ) ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'rate' ), 429 ); }
		$pending = get_posts( array( 'post_type' => 'nadlan_saved_search', 'post_status' => 'private', 'posts_per_page' => 3001, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
			'meta_query' => array( array( 'key' => 'kind', 'value' => 'nf' ), array( 'key' => 'confirmed', 'value' => '0' ) ) ) );
		if ( count( $pending ) > 3000 ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'busy' ), 503 ); }

		$label  = nadlan_na_label( $lat, $lng, (string) ( $p['place'] ?? '' ) );
		$params = array( 'lat' => $lat, 'lng' => $lng, 'r' => $r, 'label' => $label, 'deal' => $deal, 'rooms' => $rooms, 'pmax' => $pmax, 'mamad' => $mamad );
		// v3: only the filters that were chosen are kept (a v2 row and a v3 row with no new filter read the same)
		foreach ( array( 'rmax' => $rmax, 'pmin' => $pmin, 'smin' => $smin, 'smax' => $smax, 'elev' => $elev, 'park' => $park, 'balc' => $balc ) as $k => $v ) { if ( $v ) { $params[ $k ] = $v; } }
		if ( null !== $fmin ) { $params['fmin'] = $fmin; }
		if ( null !== $fmax ) { $params['fmax'] = $fmax; }
		if ( $poly ) { $params['poly'] = $poly; }
		$hk = array( $lat, $lng, $r, $deal, $rooms, $pmax, $mamad );
		$hx = array_diff_key( $params, array_flip( array( 'lat', 'lng', 'r', 'label', 'deal', 'rooms', 'pmax', 'mamad' ) ) );
		if ( $hx ) { ksort( $hx ); $hk[] = $hx; }
		$hash   = md5( $em . '|' . wp_json_encode( $hk ) );
		$now    = time();
		$items  = array_fill_keys( $items, $now );
		$follow = array_fill_keys( $follow, $now );
		// one pending request per email and area: a repeat refreshes it (and its 7 days) instead of piling up
		$same = get_posts( array( 'post_type' => 'nadlan_saved_search', 'post_status' => 'private', 'posts_per_page' => 1, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
			'meta_query' => array( array( 'key' => 'kind', 'value' => 'nf' ), array( 'key' => 'nf_hash', 'value' => $hash ), array( 'key' => 'confirmed', 'value' => '0' ) ) ) );
		if ( $same ) {
			$sid = (int) $same[0];
			wp_update_post( array( 'ID' => $sid, 'post_date' => current_time( 'mysql' ), 'post_date_gmt' => current_time( 'mysql', 1 ) ) );
			$items  = nadlan_na_ids( get_post_meta( $sid, 'nf_items', true ) ) + $items;
			$follow = nadlan_na_ids( get_post_meta( $sid, 'nf_follow', true ) ) + $follow;
		} else {
			$sid = wp_insert_post( array( 'post_type' => 'nadlan_saved_search', 'post_status' => 'private', 'post_author' => 0,
				'post_title' => $email . ' · ' . ( '' !== $label ? $label : 'אזור על המפה' ) ), true );
			if ( is_wp_error( $sid ) || ! $sid ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'store' ), 500 ); }
			update_post_meta( $sid, 'kind', 'nf' );
			update_post_meta( $sid, 'email', $email );
			update_post_meta( $sid, 'user_id', 0 );
			update_post_meta( $sid, 'confirmed', '0' );
			update_post_meta( $sid, 'token', bin2hex( random_bytes( 16 ) ) );
			update_post_meta( $sid, 'nf_hash', $hash );
		}
		update_post_meta( $sid, 'params', wp_json_encode( $params, JSON_UNESCAPED_UNICODE ) );
		update_post_meta( $sid, 'nf_what', $what );
		update_post_meta( $sid, 'nf_freq', $freq );
		update_post_meta( $sid, 'nf_items', array_slice( $items, 0, 30, true ) );
		update_post_meta( $sid, 'nf_follow', array_slice( $follow, 0, 30, true ) );
		update_post_meta( $sid, 'nf_consent', array( 't' => $now, 'v' => preg_replace( '/[^a-z0-9.\-]/', '', (string) ( $p['v'] ?? NADLAN_NA_NOTICE ) ) ) );
		$m = nadlan_na_confirm_mail( (int) $sid );
		nadlan_na_send( $email, $m['subject'], $m['html'], $m['text'], '', 'confirm' );
		return nadlan_na_rest( array( 'ok' => true, 'confirm' => true, 's' => (int) $sid, 'k' => nadlan_na_sig( 'manage', (int) $sid ) ) );
	}

	/** POST /nadlan/v1/near-alerts/items: the heart and "עקבו" on the device that made the request ({s, k} kept there). */
	function nadlan_na_items_route( $req ) {
		if ( ! nadlan_na_enabled() ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'disabled' ), 200 ); } // dormant (200: the uPress edge swaps a PHP 403 for its own nginx 405 page)
		$p   = (array) $req->get_json_params();
		$sid = (int) ( $p['s'] ?? 0 );
		if ( ! nadlan_na_limit( 'it|' . nadlan_na_client(), 60, HOUR_IN_SECONDS ) ) { return nadlan_na_rest( array( 'ok' => false, 'error' => 'rate' ), 429 ); }
		if ( ! nadlan_na_check( 'manage', $sid, (string) ( $p['k'] ?? '' ) ) ) { return nadlan_na_rest( array( 'ok' => false, 'gone' => true ) ); }
		$items  = nadlan_na_ids( get_post_meta( $sid, 'nf_items', true ) );
		$follow = nadlan_na_ids( get_post_meta( $sid, 'nf_follow', true ) );
		$what   = (array) get_post_meta( $sid, 'nf_what', true );
		$now    = time();
		foreach ( array_slice( (array) ( $p['add'] ?? array() ), 0, 30 ) as $a ) {
			$id = (int) ( $a['id'] ?? 0 );
			if ( 'l' === ( $a['t'] ?? '' ) && ! isset( $items[ $id ] ) && count( $items ) < 30 && nadlan_na_listing_ok( $id ) ) { $items[ $id ] = $now; $what[] = 'drop'; }
			if ( 'p' === ( $a['t'] ?? '' ) && ! isset( $follow[ $id ] ) && count( $follow ) < 30 && nadlan_na_project_ok( $id ) ) { $follow[ $id ] = $now; $what[] = 'proj'; }
		}
		foreach ( array_slice( (array) ( $p['del'] ?? array() ), 0, 60 ) as $a ) {
			$id = (int) ( $a['id'] ?? 0 );
			if ( 'l' === ( $a['t'] ?? '' ) ) { unset( $items[ $id ] ); }
			if ( 'p' === ( $a['t'] ?? '' ) ) { unset( $follow[ $id ] ); }
		}
		update_post_meta( $sid, 'nf_items', $items );
		update_post_meta( $sid, 'nf_follow', $follow );
		update_post_meta( $sid, 'nf_what', array_values( array_unique( array_intersect( array_map( 'strval', $what ), array( 'new', 'drop', 'proj' ) ) ) ) );
		return nadlan_na_rest( array( 'ok' => true, 'items' => count( $items ), 'follow' => count( $follow ) ) );
	}

	/** GET: a page with one button (a mail scanner opening the link confirms nothing); POST: the confirmation. */
	function nadlan_na_confirm_route( $req ) {
		$sid = (int) $req->get_param( 's' );
		$sig = (string) $req->get_param( 't' );
		if ( ! nadlan_na_check( 'confirm', $sid, $sig ) ) {
			nadlan_na_page( 'הקישור אינו בתוקף', '<p>ייתכן שהבקשה כבר אושרה, בוטלה או נמחקה אחרי 7 ימים בלי אישור. אפשר לבקש התראות מחדש מהמפה באתר.</p>' . nadlan_na_page_back() );
		}
		$s = nadlan_na_get( $sid );
		if ( 'POST' !== $req->get_method() ) {
			if ( $s['confirmed'] ) { nadlan_na_page( 'ההתראות כבר פעילות', nadlan_na_summary_html( $s ) . nadlan_na_page_back() ); }
			$form = '<form method="post" action="' . esc_url( rest_url( 'nadlan/v1/near-alerts/confirm' ) ) . '"><input type="hidden" name="s" value="' . (int) $sid . '"><input type="hidden" name="t" value="' . esc_attr( $sig ) . '">'
				. '<button type="submit" class="go">אשרו את ההתראות</button></form>';
			nadlan_na_page( 'אשרו את ההתראות', '<p>ביקשתם התראות במייל מנדלן על ' . esc_html( nadlan_na_where( $s['p'] ) ) . ', ' . esc_html( nadlan_na_scope( $s['p'] ) ) . ':</p>' . nadlan_na_summary_html( $s ) . $form
				. '<p class="fine">אם לא ביקשתם, סגרו את העמוד. בלי אישור לא נשלח דבר, והבקשה נמחקת אחרי 7 ימים.</p>' );
		}
		if ( ! nadlan_na_limit( 'cf|' . nadlan_na_client(), 30, HOUR_IN_SECONDS ) ) { nadlan_na_page( 'נסו שוב בעוד כמה דקות', '<p>נשלחו מהמכשיר הזה הרבה בקשות בזמן קצר.</p>', 429 ); }
		if ( ! $s['confirmed'] ) {
			$now = time();
			update_post_meta( $sid, 'confirmed', '1' );
			update_post_meta( $sid, 'nf_confirmed_at', $now );
			update_post_meta( $sid, 'last_run', $now ); // alerts start from now: nothing older is ever sent
			$items = array();
			foreach ( $s['items'] as $id => $t ) { $items[ $id ] = max( $t, $now ); }
			update_post_meta( $sid, 'nf_items', $items );
			$follow = array();
			foreach ( $s['follow'] as $id => $t ) { $follow[ $id ] = max( $t, $now ); }
			update_post_meta( $sid, 'nf_follow', $follow );
			wp_update_post( array( 'ID' => $sid, 'post_title' => $s['email'] . ' · ' . ( '' !== (string) ( $s['p']['label'] ?? '' ) ? $s['p']['label'] : 'אזור על המפה' ) ) );
			// the same email and area confirmed before: the new row replaces it; at most 5 confirmed rows per email
			$mine = get_posts( array( 'post_type' => 'nadlan_saved_search', 'post_status' => 'private', 'posts_per_page' => 50, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
				'orderby' => 'date', 'order' => 'DESC', 'meta_query' => array( array( 'key' => 'kind', 'value' => 'nf' ), array( 'key' => 'confirmed', 'value' => '1' ), array( 'key' => 'email', 'value' => $s['email'] ) ) ) );
			$hash = (string) get_post_meta( $sid, 'nf_hash', true );
			$kept = 1;
			foreach ( $mine as $other ) {
				if ( (int) $other === $sid ) { continue; }
				if ( (string) get_post_meta( $other, 'nf_hash', true ) === $hash || $kept >= 5 ) { wp_delete_post( (int) $other, true ); continue; }
				$kept++;
			}
			nadlan_na_recount();
			$s = nadlan_na_get( $sid );
		}
		if ( ! nadlan_na_enabled() ) { // an old link while the alerts are off: the link still works, and the page says what is true
			nadlan_na_page( 'האישור התקבל', '<p>שמרנו את הבקשה:</p>' . nadlan_na_summary_html( $s ) . '<p>ההתראות במייל מושהות כרגע באתר, ולכן לא יישלח אליכם מייל עד שיחזרו. אפשר לבטל בכל רגע מהקישור שבמייל.</p>' . nadlan_na_page_back() );
		}
		nadlan_na_page( 'ההתראות פעילות', '<p>מעכשיו נשלח לכם מייל כשיש עדכון:</p>' . nadlan_na_summary_html( $s )
			. '<p class="fine">בתחתית כל מייל יש קישור לביטול בלחיצה אחת.</p>' . nadlan_na_page_back() );
	}

	/** GET (the link in the mail) or POST (List-Unsubscribe-Post): unsubscribe at once; the row is deleted. */
	function nadlan_na_off_route( $req ) {
		$sid = (int) $req->get_param( 's' );
		$sig = (string) $req->get_param( 't' );
		$ok  = nadlan_na_check( 'off', $sid, $sig );
		$where = '';
		if ( $ok ) {
			$where = nadlan_na_where( nadlan_na_get( $sid )['p'] );
			wp_delete_post( $sid, true );
			nadlan_na_recount();
		}
		if ( 'POST' === $req->get_method() && false !== strpos( (string) $req->get_body(), 'One-Click' ) ) { // a mail client's one-click call
			return nadlan_na_rest( array( 'ok' => (bool) $ok ) );
		}
		if ( ! $ok ) { nadlan_na_page( 'הקישור אינו בתוקף', '<p>ייתכן שההתראות כבר בוטלו. אם עדיין מגיעים מיילים, כתבו ל־info@nad-lan.co.il ונמחק את הפרטים.</p>' . nadlan_na_page_back() ); }
		nadlan_na_page( 'ההתראות בוטלו', '<p>לא נשלח אליכם עוד מייל על ' . esc_html( $where ) . '. המייל והאזור נמחקו.</p>' . nadlan_na_page_back() );
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/near-alerts', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nadlan_na_signup' ) );
	register_rest_route( 'nadlan/v1', '/near-alerts/items', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nadlan_na_items_route' ) );
	register_rest_route( 'nadlan/v1', '/near-alerts/confirm', array( 'methods' => array( 'GET', 'POST' ), 'permission_callback' => '__return_true', 'callback' => 'nadlan_na_confirm_route' ) );
	register_rest_route( 'nadlan/v1', '/near-alerts/off', array( 'methods' => array( 'GET', 'POST' ), 'permission_callback' => '__return_true', 'callback' => 'nadlan_na_off_route' ) );
	register_rest_route( 'nadlan/v1', '/near-alerts/preview', array( // admin only: the two mails as HTML, with real listings; nothing is sent
		'methods' => 'GET', 'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$s = array( 'id' => 0, 'email' => 'name@example.com', 'p' => array( 'lat' => 32.109, 'lng' => 34.795, 'r' => 1.5, 'label' => 'רמת אביב', 'deal' => '', 'rooms' => 0, 'pmax' => 0, 'mamad' => false ),
				'what' => array( 'new', 'drop', 'proj' ), 'freq' => 'day', 'items' => array(), 'follow' => array(), 'confirmed' => true, 'last_run' => 0, 'sent_at' => 0, 'seen' => array() );
			if ( 'alert' === (string) $req->get_param( 'kind' ) ) {
				$c = nadlan_na_collect( $s, time(), time() - 30 * DAY_IN_SECONDS );
				$m = nadlan_na_alert_mail( $s, $c, '#' );
			} else {
				$m = nadlan_na_confirm_mail( 0, $s, '#' );
			}
			header( 'Content-Type: text/html; charset=utf-8' );
			echo $m['html']; // phpcs:ignore -- built from escaped parts
			exit;
		},
	) );
} );
add_filter( 'nadlan_hardening_public_post_routes', function ( $r ) { // the site's generic public-POST limit (inc/final-hardening.php)
	$r[] = '#^/nadlan/v1/near-alerts$#';
	$r[] = '#^/nadlan/v1/near-alerts/items$#';
	$r[] = '#^/nadlan/v1/near-alerts/confirm$#';
	return $r;
} );

/* ================================================================ 5. matching and the runs */
if ( ! function_exists( 'nadlan_na_collect' ) ) {
	/** What a row should hear about now. $floor = the oldest time looked at (a preview looks back further). */
	function nadlan_na_collect( $s, $now, $floor = null ) {
		$p     = $s['p'];
		$since = null === $floor ? max( (int) $s['last_run'], $now - 8 * DAY_IN_SECONDS ) : (int) $floor;
		$out   = array( 'new' => array(), 'drop' => array(), 'proj' => array() );
		if ( in_array( 'new', $s['what'], true ) && isset( $p['lat'], $p['lng'], $p['r'] ) ) {
			$ids = get_posts( array( 'post_type' => 'nadlan_property', 'post_status' => 'publish', 'posts_per_page' => 80, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
				'orderby' => 'date', 'order' => 'DESC', 'meta_query' => array( array( 'key' => '_nadlan_pub_at', 'value' => $since, 'compare' => '>', 'type' => 'NUMERIC' ) ) ) );
			$seen = array_flip( $s['seen'] );
			foreach ( $ids as $id ) {
				if ( isset( $seen[ (int) $id ] ) ) { continue; }
				$row = nadlan_na_listing_row( (int) $id );
				if ( $row && nadlan_na_matches( $row, $p ) ) {
					$row['km'] = nadlan_na_km( (float) $p['lat'], (float) $p['lng'], (float) $row['lat'], (float) $row['lng'] );
					$out['new'][] = $row;
				}
			}
			usort( $out['new'], function ( $a, $b ) { return $a['km'] <=> $b['km']; } );
		}
		if ( in_array( 'drop', $s['what'], true ) ) {
			foreach ( $s['items'] as $id => $at ) {
				$row = nadlan_na_listing_row( (int) $id );
				if ( ! $row ) { continue; }
				$d = nadlan_na_drop( nadlan_na_hist( (int) $id ), max( null === $floor ? (int) $s['last_run'] : (int) $floor, (int) $at ), (int) $row['price'] );
				if ( is_array( $d ) && isset( $d['gap'] ) ) { $out['drop'][] = $row + array( 'drop' => $d ); }
			}
		}
		if ( in_array( 'proj', $s['what'], true ) ) {
			foreach ( $s['follow'] as $id => $at ) {
				if ( ! nadlan_na_project_ok( (int) $id ) ) { continue; }
				$cur = array(
					'psqm'   => nadlan_na_norm( 'psqm', get_post_meta( $id, 'project_3d_avg_price_per_sqm', true ) ),
					'status' => nadlan_na_norm( 'status', get_post_meta( $id, 'project_status', true ) ),
					'units'  => nadlan_na_norm( 'units', get_post_meta( $id, 'num_units', true ) ),
				);
				$ch = nadlan_na_proj_changes( nadlan_na_hist( (int) $id ), max( null === $floor ? (int) $s['last_run'] : (int) $floor, (int) $at ), $cur );
				if ( $ch ) {
					$out['proj'][] = array( 'id' => (int) $id, 'url' => get_permalink( $id ), 'title' => html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ),
						'city' => (string) get_post_meta( $id, 'city', true ), 'changes' => $ch );
				}
			}
		}
		$out['new']  = array_slice( $out['new'], 0, 8 );
		$out['drop'] = array_slice( $out['drop'], 0, 10 );
		$out['proj'] = array_slice( $out['proj'], 0, 10 );
		return $out;
	}

	/** One row: collect, mail, move its clock only after a mail went out (a failed send is tried again next run). */
	function nadlan_na_process( $sid, $now ) {
		$s = nadlan_na_get( $sid );
		if ( ! $s['confirmed'] || ! is_email( $s['email'] ) ) { return 'skip'; }
		$c = nadlan_na_collect( $s, $now );
		if ( ! $c['new'] && ! $c['drop'] && ! $c['proj'] ) {
			update_post_meta( $sid, 'last_run', $now );
			return 'none';
		}
		$m = nadlan_na_alert_mail( $s, $c );
		if ( ! nadlan_na_send( $s['email'], $m['subject'], $m['html'], $m['text'], nadlan_na_url( 'off', $sid ), 'alert' ) ) { return 'fail'; }
		update_post_meta( $sid, 'last_run', $now );
		update_post_meta( $sid, 'nf_sent_at', $now );
		update_post_meta( $sid, 'nf_seen', array_slice( array_values( array_unique( array_merge( $s['seen'], wp_list_pluck( $c['new'], 'id' ) ) ) ), -300 ) );
		return 'sent';
	}

	/** $mode 'instant' (the single event) or 'daily' (the existing nadlan_ss_daily cron: daily + weekly rows, and a catch-up for "immediately"). */
	function nadlan_na_run( $mode ) {
		if ( get_transient( 'nadlan_na_running' ) ) { return array( 'busy' => 1 ); }
		set_transient( 'nadlan_na_running', 1, 10 * MINUTE_IN_SECONDS );
		$now = time();
		$res = array( 'sent' => 0, 'none' => 0, 'fail' => 0, 'skip' => 0, 'purged' => 0 );
		$ids = get_posts( array( 'post_type' => 'nadlan_saved_search', 'post_status' => 'private', 'posts_per_page' => 1000, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
			'meta_query' => array( array( 'key' => 'kind', 'value' => 'nf' ), array( 'key' => 'confirmed', 'value' => '1' ) ) ) );
		foreach ( nadlan_na_enabled() ? $ids : array() as $sid ) { // dormant: nothing is sent
			$f    = (string) get_post_meta( $sid, 'nf_freq', true );
			$last = (int) get_post_meta( $sid, 'last_run', true );
			$sent = (int) get_post_meta( $sid, 'nf_sent_at', true );
			if ( 'instant' === $mode ) {
				$due = 'now' === $f && $now - $sent >= 30 * MINUTE_IN_SECONDS;
			} else {
				$due = ( 'now' === $f && $now - $sent >= 30 * MINUTE_IN_SECONDS ) || ( 'week' === $f ? $now - $last >= 6.5 * DAY_IN_SECONDS : ( 'day' === $f && $now - $last >= 20 * HOUR_IN_SECONDS ) );
			}
			if ( ! $due ) { continue; }
			$r = nadlan_na_process( (int) $sid, $now );
			$res[ $r ] = ( $res[ $r ] ?? 0 ) + 1;
			if ( $res['sent'] >= 250 ) { break; } // the provider's daily quota is shared with the site's other mail
		}
		if ( 'daily' === $mode ) { // unconfirmed requests are deleted after 7 days
			foreach ( get_posts( array( 'post_type' => 'nadlan_saved_search', 'post_status' => 'private', 'posts_per_page' => 500, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
				'date_query' => array( array( 'before' => '7 days ago', 'column' => 'post_date_gmt' ) ),
				'meta_query' => array( array( 'key' => 'kind', 'value' => 'nf' ), array( 'key' => 'confirmed', 'value' => '0' ) ) ) ) as $old ) {
				wp_delete_post( (int) $old, true );
				$res['purged']++;
			}
			nadlan_na_recount();
		}
		update_option( 'nadlan_na_last_run', array( 't' => $now, 'mode' => $mode, 'on' => nadlan_na_enabled() ? 1 : 0 ) + $res, false );
		delete_transient( 'nadlan_na_running' );
		return $res;
	}
}
add_action( 'nadlan_ss_daily', function () { nadlan_na_run( 'daily' ); }, 20 );
add_action( 'nadlan_na_instant', function () { nadlan_na_run( 'instant' ); } );
add_action( 'after_delete_post', function ( $id, $post = null ) {
	if ( $post && 'nadlan_saved_search' === $post->post_type ) { nadlan_na_recount(); }
}, 10, 2 );
add_action( 'trashed_post', function ( $id ) { if ( 'nadlan_saved_search' === get_post_type( $id ) ) { nadlan_na_recount(); } } );

/* ================================================================ 6. the mails (NadLan Instruments, inline for mail clients) */
if ( ! function_exists( 'nadlan_na_send' ) ) {
	function nadlan_na_nis( $n ) { return number_format( (float) $n ) . ' ₪'; }
	function nadlan_na_ltr( $s, $style = '' ) { return '<span dir="ltr" style="white-space:nowrap;' . $style . '">' . esc_html( $s ) . '</span>'; } // a number or an address inside Hebrew
	function nadlan_na_dist( $km ) {
		if ( $km < 1 ) { return max( 50, (int) ( round( $km * 20 ) * 50 ) ) . ' מ׳'; }
		return ( $km < 10 ? (string) round( $km, 1 ) : (string) round( $km ) ) . ' ק״מ';
	}
	function nadlan_na_stage( $e ) {
		$m = array( 'marketing' => 'בשיווק', 'construction' => 'בבנייה', 'planning' => 'בתכנון', 'permits' => 'בהיתר', 'completed' => 'אוכלס' );
		return $m[ $e ] ?? '';
	}
	function nadlan_na_cut( $s, $n ) { $s = (string) $s; return mb_strlen( $s ) > $n ? rtrim( mb_substr( $s, 0, $n - 1 ) ) . '…' : $s; }
	function nadlan_na_half( $v ) { $v = (float) $v; return floor( $v ) == $v ? (string) (int) $v : rtrim( rtrim( number_format( $v, 1 ), '0' ), '.' ); }
	function nadlan_na_floor_name( $f ) { return 0 === (int) $f ? 'קרקע' : (string) (int) $f; }
	function nadlan_na_filters_text( $p ) {
		$a = array( 'rent' === ( $p['deal'] ?? '' ) ? 'להשכרה' : ( 'sale' === ( $p['deal'] ?? '' ) ? 'למכירה' : 'למכירה ולהשכרה' ) );
		$r0 = (float) ( $p['rooms'] ?? 0 ); $r1 = (float) ( $p['rmax'] ?? 0 );
		if ( $r0 && $r1 ) { $a[] = ( $r0 == $r1 ? nadlan_na_half( $r0 ) : nadlan_na_half( $r0 ) . ' עד ' . nadlan_na_half( $r1 ) ) . ' חדרים'; }
		elseif ( $r0 ) { $a[] = nadlan_na_half( $r0 ) . ' חדרים ומעלה'; }
		elseif ( $r1 ) { $a[] = 'עד ' . nadlan_na_half( $r1 ) . ' חדרים'; }
		$p0 = (int) ( $p['pmin'] ?? 0 ); $p1 = (int) ( $p['pmax'] ?? 0 );
		if ( $p0 && $p1 ) { $a[] = 'מ־' . nadlan_na_nis( $p0 ) . ' עד ' . nadlan_na_nis( $p1 ); }
		elseif ( $p0 ) { $a[] = 'מ־' . nadlan_na_nis( $p0 ); }
		elseif ( $p1 ) { $a[] = 'עד ' . nadlan_na_nis( $p1 ); }
		$s0 = (int) ( $p['smin'] ?? 0 ); $s1 = (int) ( $p['smax'] ?? 0 );
		if ( $s0 && $s1 ) { $a[] = number_format( $s0 ) . ' עד ' . number_format( $s1 ) . ' מ״ר'; }
		elseif ( $s0 ) { $a[] = 'מ־' . number_format( $s0 ) . ' מ״ר'; }
		elseif ( $s1 ) { $a[] = 'עד ' . number_format( $s1 ) . ' מ״ר'; }
		$f0 = isset( $p['fmin'] ) && null !== $p['fmin'] ? (int) $p['fmin'] : null; $f1 = isset( $p['fmax'] ) && null !== $p['fmax'] ? (int) $p['fmax'] : null;
		if ( null !== $f0 && null !== $f1 ) { $a[] = $f0 === $f1 ? ( 0 === $f0 ? 'קומת קרקע' : 'קומה ' . $f0 ) : 'קומות ' . nadlan_na_floor_name( $f0 ) . ' עד ' . nadlan_na_floor_name( $f1 ); }
		elseif ( null !== $f0 ) { $a[] = 0 === $f0 ? 'מקומת קרקע' : 'מקומה ' . $f0; }
		elseif ( null !== $f1 ) { $a[] = 0 === $f1 ? 'קומת קרקע' : 'עד קומה ' . $f1; }
		if ( ! empty( $p['mamad'] ) ) { $a[] = 'עם ממ״ד'; }
		if ( ! empty( $p['elev'] ) ) { $a[] = 'עם מעלית'; }
		if ( ! empty( $p['park'] ) ) { $a[] = 'עם חניה'; }
		if ( ! empty( $p['balc'] ) ) { $a[] = 'עם מרפסת'; }
		return 1 === count( $a ) ? $a[0] . ', בכל מחיר ובכל מספר חדרים' : implode( ', ', $a );
	}

	/** The frame of every mail. $blocks = HTML already escaped. */
	function nadlan_na_frame( $pre, $h1, $blocks, $foot ) {
		$sans = "'IBM Plex Sans Hebrew',Arial,Helvetica,sans-serif";
		return '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light">'
			. '<title>' . esc_html( $h1 ) . '</title><link href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"></head>'
			. '<body style="margin:0;padding:0;background:#F6F8F9">'
			. '<div style="display:none;max-height:0;overflow:hidden;opacity:0">' . esc_html( $pre ) . '</div>'
			. '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F6F8F9;border-collapse:collapse"><tr><td align="center" style="padding:24px 12px">'
			. '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" dir="rtl" style="max-width:600px;border-collapse:collapse;font-family:' . $sans . ';color:#12202A;text-align:right">'
			. '<tr><td style="padding:0 0 12px;border-bottom:2px solid #2F6F86"><a href="' . esc_url( home_url( '/' ) ) . '" style="font-family:Karantina,' . $sans . ';font-weight:700;font-size:36px;line-height:36px;color:#12202A;text-decoration:none">נדלן</a></td></tr>'
			. '<tr><td style="padding:20px 0 6px"><h1 style="margin:0;font-family:Karantina,' . $sans . ';font-weight:700;font-size:40px;line-height:44px;color:#12202A">' . esc_html( $h1 ) . '</h1></td></tr>'
			. '<tr><td style="padding:0">' . $blocks . '</td></tr>'
			. '<tr><td style="padding:20px 0 0;border-top:1px solid #D3DCE2;font-size:12px;line-height:18px;color:#5E6A75">' . $foot . '</td></tr>'
			. '</table></td></tr></table></body></html>';
	}
	function nadlan_na_p( $html, $size = 15, $color = '#3E4C58', $extra = '' ) {
		return '<p style="margin:0 0 12px;font-size:' . (int) $size . 'px;line-height:1.6;color:' . $color . ';' . $extra . '">' . $html . '</p>';
	}
	function nadlan_na_button( $url, $text ) {
		return '<a href="' . esc_url( $url ) . '" style="display:inline-block;background:#2F6F86;border:1px solid #1F4B5C;color:#FFFFFF;font-weight:600;font-size:15px;line-height:20px;padding:12px 20px;border-radius:2px;text-decoration:none">' . esc_html( $text ) . '</a>';
	}
	function nadlan_na_card( $row, $inner ) { // one listing or project, a bordered white box
		$img = ! empty( $row['img'] ) ? '<td width="112" valign="top" style="padding:12px 12px 12px 0;width:112px"><a href="' . esc_url( $row['url'] ) . '"><img src="' . esc_url( $row['img'] ) . '" width="112" height="84" alt="" style="display:block;width:112px;height:84px;object-fit:cover;border-radius:2px;border:0"></a></td>' : '';
		return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:separate;background:#FFFFFF;border:1px solid #D3DCE2;border-radius:6px;margin:0 0 12px"><tr>'
			. $img . '<td valign="top" style="padding:12px 14px">' . $inner . '</td></tr></table>';
	}
	function nadlan_na_h2( $t ) {
		return '<h2 style="margin:20px 0 10px;font-size:17px;line-height:24px;font-weight:600;color:#12202A">' . esc_html( $t ) . '</h2>';
	}
	function nadlan_na_foot( $s, $off ) {
		$p = $s['p'];
		return 'קיבלתם את המייל כי ביקשתם באתר נדלן התראות על ' . esc_html( nadlan_na_where( $p ) ) . ', ' . esc_html( nadlan_na_scope( $p ) ) . ', ' . esc_html( nadlan_na_freq_text( $s['freq'] ) ) . '.<br>'
			. '<a href="' . esc_url( $off ) . '" style="color:#1F4B5C;text-decoration:underline">לביטול ההתראות בלחיצה אחת</a> · <a href="' . esc_url( nadlan_na_privacy_url() ) . '" style="color:#1F4B5C;text-decoration:underline">מדיניות הפרטיות</a><br>'
			. 'פרטי המודעות באחריות המפרסמים. נדלן · ' . nadlan_na_ltr( 'nad-lan.co.il' ) . ' · ' . nadlan_na_ltr( 'info@nad-lan.co.il' );
	}

	/** The confirmation mail. $s may be given (the preview). */
	function nadlan_na_confirm_mail( $sid, $s = null, $url = null ) {
		$s   = $s ? $s : nadlan_na_get( $sid );
		$url = $url ? $url : nadlan_na_url( 'confirm', $sid );
		$b   = nadlan_na_p( 'ביקשתם באתר נדלן התראות במייל על ' . esc_html( nadlan_na_where( $s['p'] ) ) . ', ' . esc_html( nadlan_na_scope( $s['p'] ) ) . ':' )
			. nadlan_na_summary_html( $s, true )
			. '<p style="margin:16px 0 16px">' . nadlan_na_button( $url, 'אשרו את ההתראות' ) . '</p>'
			. nadlan_na_p( 'עד שתאשרו, לא נשלח שום התראה. אם לא ביקשתם, אפשר להתעלם מהמייל: בלי אישור, הבקשה והמייל נמחקים אחרי 7 ימים.', 13, '#5E6A75' );
		$foot = 'נשתמש במייל רק כדי לשלוח את ההתראות שבחרתם. <a href="' . esc_url( nadlan_na_privacy_url() ) . '" style="color:#1F4B5C;text-decoration:underline">מדיניות הפרטיות</a><br>נדלן · ' . nadlan_na_ltr( 'nad-lan.co.il' ) . ' · ' . nadlan_na_ltr( 'info@nad-lan.co.il' );
		$text = "ביקשתם באתר נדלן התראות במייל על " . nadlan_na_where( $s['p'] ) . ".\n" . wp_strip_all_tags( str_replace( '</li>', "\n", nadlan_na_summary_html( $s, true ) ) )
			. "\nלאישור ההתראות:\n" . $url . "\n\nעד שתאשרו, לא נשלח שום התראה. בלי אישור, הבקשה נמחקת אחרי 7 ימים.\n" . nadlan_na_privacy_url();
		return array( 'subject' => 'אשרו את ההתראות מנדלן', 'html' => nadlan_na_frame( 'לחצו לאישור, ונעדכן אתכם על ' . nadlan_na_where( $s['p'] ), 'אשרו את ההתראות', $b, $foot ), 'text' => $text );
	}

	/** What the row asked for, as a short list (the confirmation mail and pages). */
	function nadlan_na_summary_html( $s, $mail = false ) {
		$li = array();
		if ( in_array( 'new', $s['what'], true ) ) { $li[] = 'נכס חדש באזור: ' . nadlan_na_filters_text( $s['p'] ); }
		if ( in_array( 'drop', $s['what'], true ) ) { $n = count( $s['items'] ); $li[] = 'ירידת מחיר בנכס ששמרתם' . ( $n ? ' (' . ( 1 === $n ? 'נכס אחד' : $n . ' נכסים' ) . ')' : '' ); }
		if ( in_array( 'proj', $s['what'], true ) ) { $n = count( $s['follow'] ); $li[] = 'עדכון בפרויקט שאתם עוקבים אחריו' . ( $n ? ' (' . ( 1 === $n ? 'פרויקט אחד' : $n . ' פרויקטים' ) . ')' : '' ); }
		$li[] = 'תדירות: ' . nadlan_na_freq_text( $s['freq'] );
		$st = $mail ? ' style="margin:0 0 6px;font-size:15px;line-height:1.5;color:#12202A"' : '';
		return '<ul' . ( $mail ? ' style="margin:0 0 4px;padding:0 20px 0 0"' : '' ) . '>' . implode( '', array_map( function ( $x ) use ( $st ) { return '<li' . $st . '>' . esc_html( $x ) . '</li>'; }, $li ) ) . '</ul>';
	}

	/** The alert mail: new listings, drops, project changes, in that order of sections (drops first when there are). */
	function nadlan_na_alert_mail( $s, $c, $off = null ) {
		$off   = $off ? $off : nadlan_na_url( 'off', $s['id'] );
		$where = nadlan_na_where( $s['p'] );
		$mono  = "font-family:'IBM Plex Mono',Arial,sans-serif;";
		$b = ''; $t = '';
		if ( $c['drop'] ) {
			$b .= nadlan_na_h2( 1 === count( $c['drop'] ) ? 'ירד המחיר בנכס ששמרתם' : 'ירד המחיר בנכסים ששמרתם' );
			foreach ( $c['drop'] as $r ) {
				$d   = $r['drop'];
				$per = 'rent' === $r['deal'] ? ' לחודש' : '';
				$in  = '<p style="margin:0 0 2px;font-size:13px;line-height:18px;color:#5E6A75">' . esc_html( implode( ' · ', array_filter( array( $r['ptype'], implode( ', ', array_filter( array( $r['hood'], $r['city'] ) ) ) ) ) ) ) . '</p>'
					. '<p style="margin:0 0 8px;font-size:16px;line-height:22px;font-weight:600"><a href="' . esc_url( $r['url'] ) . '" style="color:#12202A;text-decoration:none">' . esc_html( $r['title'] ) . '</a></p>'
					. '<p style="margin:0;font-size:13px;line-height:20px;color:#5E6A75">המחיר הקודם: ' . nadlan_na_ltr( nadlan_na_nis( $d['old'] ), $mono . 'color:#3E4C58' ) . esc_html( $per ) . '</p>'
					. '<p style="margin:2px 0 0;font-size:13px;line-height:28px;color:#5E6A75">המחיר עכשיו: ' . nadlan_na_ltr( nadlan_na_nis( $d['new'] ), $mono . 'font-size:20px;font-weight:500;color:#12202A;border-bottom:2px solid #C42550' ) . esc_html( $per ) . '</p>'
					. '<p style="margin:6px 0 0;font-size:14px;line-height:20px;color:#12202A">ירד ב־' . nadlan_na_ltr( nadlan_na_nis( $d['gap'] ), $mono ) . ' · ' . nadlan_na_ltr( rtrim( rtrim( number_format( $d['pct'], 1 ), '0' ), '.' ) . '%', $mono ) . '</p>'
					. '<p style="margin:2px 0 0;font-size:12px;line-height:18px;color:#5E6A75">המחיר עודכן ב־' . nadlan_na_ltr( wp_date( 'j.n.Y', $d['t'] ) ) . '</p>'
					. '<p style="margin:12px 0 0">' . nadlan_na_button( $r['url'], 'לעמוד הנכס' ) . '</p>';
				$b .= nadlan_na_card( $r, $in );
				$t .= "ירד המחיר: " . $r['title'] . "\n" . 'המחיר עכשיו ' . nadlan_na_nis( $d['new'] ) . $per . ', במקום ' . nadlan_na_nis( $d['old'] ) . ' (ירד ב־' . nadlan_na_nis( $d['gap'] ) . ")\n" . $r['url'] . "\n\n";
			}
		}
		if ( $c['new'] ) {
			$b .= nadlan_na_h2( ( 1 === count( $c['new'] ) ? 'נכס חדש: ' : count( $c['new'] ) . ' נכסים חדשים: ' ) . $where );
			foreach ( $c['new'] as $r ) {
				$facts = array();
				if ( $r['rooms'] > 0 ) { $facts[] = ( floor( $r['rooms'] ) == $r['rooms'] ? (int) $r['rooms'] : $r['rooms'] ) . ' חדרים'; }
				if ( $r['sqm'] > 0 ) { $facts[] = number_format( $r['sqm'] ) . ' מ״ר'; }
				if ( $r['mamad'] ) { $facts[] = 'ממ״ד'; }
				$facts[] = 'rent' === $r['deal'] ? 'להשכרה' : 'למכירה';
				$near = ( in_array( $r['approx'], array( 'hood', 'city' ), true ) ? 'כ־' : '' ) . nadlan_na_dist( $r['km'] ) . ' ממרכז האזור, בקו אווירי' . ( 'hood' === $r['approx'] ? ' (המיקום לפי השכונה)' : ( 'city' === $r['approx'] ? ' (המיקום לפי העיר)' : '' ) );
				$in = '<p style="margin:0 0 2px;font-size:13px;line-height:18px;color:#5E6A75">' . esc_html( implode( ' · ', array_filter( array( $r['ptype'], implode( ', ', array_filter( array( $r['hood'], $r['city'] ) ) ) ) ) ) ) . '</p>'
					. '<p style="margin:0 0 6px;font-size:16px;line-height:22px;font-weight:600"><a href="' . esc_url( $r['url'] ) . '" style="color:#12202A;text-decoration:none">' . esc_html( $r['title'] ) . '</a></p>'
					. ( $r['price'] > 0 ? '<p style="margin:0;font-size:13px;line-height:24px;color:#5E6A75">' . nadlan_na_ltr( nadlan_na_nis( $r['price'] ), $mono . 'font-size:18px;font-weight:500;color:#12202A' ) . ( 'rent' === $r['deal'] ? ' לחודש' : '' ) . '</p>' : '' )
					. '<p style="margin:4px 0 0;font-size:13px;line-height:20px;color:#3E4C58">' . esc_html( implode( ' · ', $facts ) ) . '</p>'
					. '<p style="margin:2px 0 0;font-size:12px;line-height:18px;color:#5E6A75">' . esc_html( $near ) . '</p>'
					. '<p style="margin:12px 0 0">' . nadlan_na_button( $r['url'], 'לעמוד הנכס' ) . '</p>';
				$b .= nadlan_na_card( $r, $in );
				$t .= "נכס חדש: " . $r['title'] . ( $r['price'] > 0 ? ' · ' . nadlan_na_nis( $r['price'] ) : '' ) . "\n" . $r['url'] . "\n\n";
			}
		}
		if ( $c['proj'] ) {
			$b .= nadlan_na_h2( 1 === count( $c['proj'] ) ? 'עדכון בפרויקט שאתם עוקבים אחריו' : 'עדכונים בפרויקטים שאתם עוקבים אחריהם' );
			foreach ( $c['proj'] as $r ) {
				$rows = '';
				$t   .= "עדכון בפרויקט: " . $r['title'] . "\n";
				foreach ( $r['changes'] as $ch ) {
					if ( 'psqm' === $ch['k'] ) { $l = 'המחיר המוערך למ״ר: ' . nadlan_na_ltr( nadlan_na_nis( $ch['to'] ), $mono . 'color:#12202A' ) . ', במקום ' . nadlan_na_ltr( nadlan_na_nis( $ch['from'] ) ); }
					elseif ( 'status' === $ch['k'] ) { $l = 'שלב הפרויקט: ' . esc_html( nadlan_na_stage( $ch['to'] ) ) . ', במקום ' . esc_html( nadlan_na_stage( $ch['from'] ) ); }
					else { $l = 'מספר הדירות בפרויקט: ' . nadlan_na_ltr( number_format( (int) $ch['to'] ), $mono . 'color:#12202A' ) . ', במקום ' . nadlan_na_ltr( number_format( (int) $ch['from'] ) ); }
					$rows .= '<p style="margin:4px 0 0;font-size:14px;line-height:20px;color:#3E4C58">' . $l . '</p>';
					$t    .= wp_strip_all_tags( $l ) . "\n";
				}
				$in = ( $r['city'] ? '<p style="margin:0 0 2px;font-size:13px;line-height:18px;color:#5E6A75">' . esc_html( $r['city'] ) . '</p>' : '' )
					. '<p style="margin:0 0 4px;font-size:16px;line-height:22px;font-weight:600"><a href="' . esc_url( $r['url'] ) . '" style="color:#12202A;text-decoration:none">' . esc_html( $r['title'] ) . '</a></p>'
					. $rows . '<p style="margin:12px 0 0">' . nadlan_na_button( $r['url'], 'לעמוד הפרויקט' ) . '</p>';
				$b .= nadlan_na_card( $r, $in );
				$t .= $r['url'] . "\n\n";
			}
		}
		$nd = count( $c['drop'] ); $nn = count( $c['new'] ); $np = count( $c['proj'] );
		if ( $nd ) { $subj = 1 === $nd ? 'ירד המחיר: ' . nadlan_na_cut( $c['drop'][0]['title'], 50 ) : 'ירד המחיר ב־' . $nd . ' נכסים ששמרתם'; }
		elseif ( $nn ) { $subj = ( 1 === $nn ? 'נכס חדש ' . ( 'rent' === $c['new'][0]['deal'] ? 'להשכרה' : 'למכירה' ) : $nn . ' נכסים חדשים' ) . ': ' . $where; }
		else { $subj = 1 === $np ? 'עדכון בפרויקט ' . nadlan_na_cut( $c['proj'][0]['title'], 50 ) : 'עדכונים ב־' . $np . ' פרויקטים שאתם עוקבים אחריהם'; }
		if ( ( $nd ? 1 : 0 ) + ( $nn ? 1 : 0 ) + ( $np ? 1 : 0 ) > 1 ) { $subj .= ', ועוד עדכונים'; }
		$h1 = $nd ? 'ירד המחיר' : ( $nn ? ( 1 === $nn ? 'נכס חדש באזור' : 'נכסים חדשים באזור' ) : 'עדכון בפרויקט' );
		return array( 'subject' => $subj, 'html' => nadlan_na_frame( $subj, $h1, $b, nadlan_na_foot( $s, $off ) ),
			'text' => $t . "לביטול ההתראות: " . $off . "\n" . nadlan_na_privacy_url() );
	}

	/** wp_mail with a plain-text twin and the List-Unsubscribe headers; the last result is kept for the admin screen. */
	function nadlan_na_send( $to, $subject, $html, $text, $unsub, $kind ) {
		if ( ! nadlan_na_enabled() || ! apply_filters( 'nadlan_na_can_send', true, $kind ) ) { return false; } // dormant: no mail at all
		$err  = '';
		$fail = function ( $e ) use ( &$err ) { $err = is_wp_error( $e ) ? $e->get_error_message() : 'failed'; };
		$alt  = function ( $pm ) use ( $text ) { $pm->AltBody = $text; };
		add_action( 'wp_mail_failed', $fail );
		add_action( 'phpmailer_init', $alt, 99 );
		$h = array( 'Content-Type: text/html; charset=UTF-8' );
		if ( $unsub ) { $h[] = 'List-Unsubscribe: <' . esc_url_raw( $unsub ) . '>'; $h[] = 'List-Unsubscribe-Post: List-Unsubscribe=One-Click'; }
		$ok = (bool) wp_mail( $to, $subject, $html, $h );
		remove_action( 'wp_mail_failed', $fail );
		remove_action( 'phpmailer_init', $alt, 99 );
		$st = (array) get_option( 'nadlan_na_stats', array() );
		$k  = $kind . ( $ok ? '_ok' : '_fail' );
		$st[ $k ] = (int) ( $st[ $k ] ?? 0 ) + 1;
		update_option( 'nadlan_na_stats', $st, false );
		update_option( 'nadlan_na_mail_last', array( 't' => time(), 'ok' => $ok, 'kind' => $kind,
			'err' => mb_substr( preg_replace( '/[^\s<>()"]+@[^\s<>()"]+/', '[mail]', wp_strip_all_tags( (string) $err ) ), 0, 160 ) ), false ); // never the address
		return $ok;
	}
}

/* ================================================================ 7. the confirm and unsubscribe pages */
if ( ! function_exists( 'nadlan_na_page' ) ) {
	function nadlan_na_page_back() {
		return '<p><a class="btn" href="' . esc_url( home_url( '/properties/' ) ) . '">לדירות למכירה ולהשכרה על המפה</a></p>';
	}
	function nadlan_na_page( $title, $body, $status = 200 ) {
		nocache_headers();
		do_action( 'litespeed_control_set_nocache', 'nadlan near alerts page' );
		status_header( (int) $status );
		header( 'Content-Type: text/html; charset=utf-8' );
		echo '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' . esc_html( $title ) . ' · נדלן</title>'
			. '<link href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&display=swap" rel="stylesheet">'
			. '<style>body{margin:0;background:#F6F8F9;color:#12202A;font:16px/1.6 "IBM Plex Sans Hebrew",Arial,sans-serif}main{max-width:560px;margin:0 auto;padding:24px 16px 64px}'
			. '.brand{display:inline-block;padding-bottom:10px;border-bottom:2px solid #2F6F86;font:700 36px/1 Karantina,"IBM Plex Sans Hebrew",Arial,sans-serif;color:#12202A;text-decoration:none}'
			. 'h1{margin:24px 0 12px;font:700 44px/1.05 Karantina,"IBM Plex Sans Hebrew",Arial,sans-serif}p{margin:0 0 14px;color:#3E4C58}ul{margin:0 0 18px;padding:12px 32px 12px 16px;background:#fff;border:1px solid #D3DCE2;border-radius:6px}li{margin:4px 0}'
			. '.go,.btn{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;background:#2F6F86;color:#fff;border:1px solid #1F4B5C;border-radius:2px;font:600 16px/1.2 "IBM Plex Sans Hebrew",Arial,sans-serif;text-decoration:none;cursor:pointer}'
			. '.go:hover,.btn:hover{background:#1F4B5C}.btn{background:#fff;color:#1F4B5C;border-color:#2F6F86}.btn:hover{background:#F6F8F9}form{margin:0 0 18px}.fine{font-size:13px;color:#5E6A75}'
			. ':focus-visible{outline:2px solid #2F6F86;outline-offset:2px}</style></head><body><main><a class="brand" href="' . esc_url( home_url( '/' ) ) . '">נדלן</a><h1>' . esc_html( $title ) . '</h1>'
			. $body . '</main></body></html>'; // phpcs:ignore -- built from escaped parts
		exit;
	}
}

/* ================================================================ 8. the finder's settings (portal pages only, never a broker's page) */
add_action( 'wp_footer', function () {
	if ( ! function_exists( 'nadlan_nf_context' ) ) { return; }
	$c = nadlan_nf_context();
	if ( ! $c || 'portal' !== ( $c['mode'] ?? '' ) ) { return; }
	if ( ! nadlan_na_enabled() ) { return; } // dormant: no #nlna-cfg, so the finder shows no alert surface
	$cfg = array( 'api' => rest_url( 'nadlan/v1/near-alerts' ), 'items' => rest_url( 'nadlan/v1/near-alerts/items' ), 'privacy' => nadlan_na_privacy_url(), 'v' => NADLAN_NA_NOTICE );
	echo '<script type="application/json" id="nlna-cfg">' . wp_json_encode( $cfg, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP ) . '</script>' . "\n"; // phpcs:ignore
}, 29 );

/* ================================================================ 9. admin: the CPT's own list */
add_filter( 'manage_nadlan_saved_search_posts_columns', function ( $cols ) {
	$out = array();
	foreach ( $cols as $k => $v ) {
		$out[ $k ] = $v;
		if ( 'title' === $k ) {
			$out['nlna_state'] = 'מצב';
			$out['nlna_what']  = 'התראות';
			$out['nlna_freq']  = 'תדירות';
			$out['nlna_sent']  = 'נשלח לאחרונה';
		}
	}
	return $out;
} );
add_action( 'manage_nadlan_saved_search_posts_custom_column', function ( $col, $id ) {
	if ( 0 !== strpos( $col, 'nlna_' ) ) { return; }
	if ( 'nf' !== (string) get_post_meta( $id, 'kind', true ) ) { echo 'nlna_state' === $col ? 'חיפוש שמור (הטופס הישן)' : ''; return; }
	$s = nadlan_na_get( $id );
	if ( 'nlna_state' === $col ) { echo $s['confirmed'] ? 'פעיל' : 'ממתין לאישור במייל'; }
	if ( 'nlna_what' === $col ) {
		$a = array();
		if ( in_array( 'new', $s['what'], true ) ) { $a[] = 'נכס חדש (' . esc_html( nadlan_na_filters_text( $s['p'] ) ) . ', ' . esc_html( nadlan_na_scope( $s['p'] ) ) . ')'; }
		if ( in_array( 'drop', $s['what'], true ) ) { $a[] = 'ירידת מחיר (' . count( $s['items'] ) . ')'; }
		if ( in_array( 'proj', $s['what'], true ) ) { $a[] = 'פרויקטים (' . count( $s['follow'] ) . ')'; }
		echo implode( '<br>', $a ); // phpcs:ignore -- escaped above
	}
	if ( 'nlna_freq' === $col ) { echo esc_html( nadlan_na_freq_text( $s['freq'] ) ); }
	if ( 'nlna_sent' === $col ) { echo $s['sent_at'] ? esc_html( wp_date( 'j.n.Y H:i', $s['sent_at'] ) ) : '-'; }
}, 10, 2 );
add_action( 'admin_notices', function () {
	$sc = function_exists( 'get_current_screen' ) ? get_current_screen() : null;
	if ( ! $sc || 'edit-nadlan_saved_search' !== $sc->id || ! current_user_can( 'manage_options' ) ) { return; }
	$l  = (array) get_option( 'nadlan_na_mail_last', array() );
	$st = (array) get_option( 'nadlan_na_stats', array() );
	$r  = (array) get_option( 'nadlan_na_last_run', array() );
	$transport = '' !== (string) get_option( 'nadlan_smtp_host', '' ) && '' !== (string) get_option( 'nadlan_smtp_pass', '' ) ? 'דרך ' . (string) get_option( 'nadlan_smtp_host' ) : 'דרך שרת האחסון (אין מפתח SMTP שמור)';
	echo '<div class="notice notice-info"><p><b>התראות לידי</b> (מהמפה באתר): כל שורה היא מייל אחד ואזור אחד. מחיקה: העבירו לפח ומחקו לצמיתות. המיילים יוצאים ' . esc_html( $transport ) . '.</p><p>'
		. 'נשלחו: אישורים ' . (int) ( $st['confirm_ok'] ?? 0 ) . ', התראות ' . (int) ( $st['alert_ok'] ?? 0 ) . '; נכשלו ' . (int) ( ( $st['confirm_fail'] ?? 0 ) + ( $st['alert_fail'] ?? 0 ) ) . '.'
		. ( $l ? ' השליחה האחרונה: ' . esc_html( wp_date( 'j.n.Y H:i', (int) $l['t'] ) ) . ', ' . ( ! empty( $l['ok'] ) ? 'יצאה' : 'נכשלה' . ( ! empty( $l['err'] ) ? ' (' . esc_html( $l['err'] ) . ')' : '' ) ) . '.' : '' )
		. ( $r ? ' הריצה האחרונה: ' . esc_html( wp_date( 'j.n.Y H:i', (int) $r['t'] ) ) . '.' : '' ) . '</p>'
		. '<p>מצב: ' . ( nadlan_na_enabled() ? 'פעילות.' : 'כבויות: גולשים לא רואים כפתור התראות, ושום מייל לא נשלח.' ) . ' <a href="' . esc_url( admin_url( 'options-general.php?page=nadlan-mail' ) ) . '">להפעלה או לכיבוי</a></p></div>';
} );


/* ================================================================ 10. the owner's switch, on the existing Brevo screen (Settings › "מייל יוצא (Brevo)", inc/mailer.php)
 * Off until the owner turns it on; nothing changes for visitors until then. A change purges the page cache (the portal pages print
 * #nlna-cfg only while on); turning it off also drops a pending single event. Admins only, its own nonce. */
add_action( 'admin_init', function () {
	if ( empty( $_POST['nadlan_na_switch_nonce'] ) || ! current_user_can( 'manage_options' ) ) { return; }
	if ( ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_na_switch_nonce'] ) ), 'nadlan_na_switch' ) ) { return; }
	$want = ! empty( $_POST['nadlan_na_enabled'] );
	$was  = nadlan_na_enabled();
	if ( $want ) { update_option( 'nadlan_na_enabled', '1', true ); } else { delete_option( 'nadlan_na_enabled' ); }
	if ( $want !== $was ) {
		do_action( 'litespeed_purge_all' );
		if ( ! $want ) { wp_clear_scheduled_hook( 'nadlan_na_instant' ); }
		update_option( 'nadlan_na_switch_log', array( 't' => time(), 'on' => $want ? 1 : 0, 'by' => get_current_user_id() ), false );
	}
	wp_safe_redirect( add_query_arg( array( 'page' => 'nadlan-mail', 'nlna' => $want ? 'on' : 'off' ), admin_url( 'options-general.php' ) ) );
	exit;
} );
add_action( 'admin_notices', function () {
	$sc = function_exists( 'get_current_screen' ) ? get_current_screen() : null;
	if ( ! $sc || 'settings_page_nadlan-mail' !== $sc->id || ! current_user_can( 'manage_options' ) ) { return; }
	$on  = nadlan_na_enabled();
	$key = '' !== (string) get_option( 'nadlan_smtp_host', '' ) && '' !== (string) get_option( 'nadlan_smtp_pass', '' );
	echo '<div class="notice notice-' . ( $on ? 'success' : 'warning' ) . '" dir="rtl"><form method="post" action="' . esc_url( admin_url( 'options-general.php?page=nadlan-mail' ) ) . '">'
		. wp_nonce_field( 'nadlan_na_switch', 'nadlan_na_switch_nonce', true, false )
		. '<p><b>התראות במייל מהמפה "חפשו נכס לידי"</b>: ' . ( $on ? 'פעילות. גולשים יכולים לבקש התראות.' : 'כבויות. גולשים לא רואים כפתור התראות, ושום מייל לא נשלח.' ) . '</p>'
		. '<p>לפני הפעלה: מפתח SMTP שמור בטופס שלמטה (' . ( $key ? 'שמור' : 'עדיין לא' ) . '), והמשפט על ההתראות במדיניות הפרטיות מאושר.</p>'
		. '<p><label><input type="checkbox" name="nadlan_na_enabled" value="1"' . ( $on ? ' checked' : '' ) . '> להפעיל התראות במייל לגולשים</label> <button class="button">שמירה</button></p></form></div>'; // phpcs:ignore -- escaped above
} );
