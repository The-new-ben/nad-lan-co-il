<?php
/**
 * nadlan-config - Visit trail (v1.0.0, 7.11.2026, Linear HAD-678; LOCAL until release 1.72.602).
 *
 * Ben, 7.11.2026: "record what visitors click and choose on the project pages and show me who clicked what". Hotjar
 * cannot see inside the 3D stage (a canvas), so the floor, the direction, the opened tour and the WhatsApp tap were lost.
 *  - assets/visit-trail/trail.js (enqueued on project stage pages only, nadlan_ps_current()) listens to the stage's own
 *    window events (nl:floor, nl:facing, nl:view, nl:quarter, nl:facility, nl:facility-tour, nl:floor-cta,
 *    nl:floor-action, nl:tour, nl:example) and to taps on the page's calls to action, and sends small batches here.
 *    Nothing in the stage, in bridge.js or in showroom-engine/engine.js (frozen) is touched: it only listens.
 *  - POST /wp-json/nadlan/v1/trail: the batch is checked again field by field (an allow list per event, every text cut
 *    short), limited (16 KB, 60 events, 30 batches a minute per visitor, 3,000 events per visit, 200,000 a day for the
 *    site) and stored in two tables of our own ({prefix}nadlan_visits, {prefix}nadlan_visit_events, dbDelta). The
 *    country comes from the host's country header when there is one (Cloudflare / uPress); the IP address is never
 *    stored, not even cut short (the per-minute limit keeps a hashed key in a two-minute transient, as campaign-brief.php
 *    does). A browser with Global Privacy Control or Do Not Track gets nothing stored (the script does not even run).
 *  - The lead link: trail.js adds the visit id to the page's own lead requests (the header X-NL-Visit on same-origin
 *    POSTs to /wp-json/nadlan/v1/*, a hidden nl_visit field on forms posted to admin-post.php). When a nadlan_lead is
 *    created (wp_after_insert_post, any module: conversion-cta.php /lead, lead-e2e.php, scheduler.php, the theme's form)
 *    in a request that carries the id, the lead gets the meta _nl_visit and the visit row its lead_id. No lead module is
 *    edited. A WhatsApp conversation is not a lead row on the site, so it shows as the tap only.
 *  - Admin: "מסלולי ביקור" under Lead Inbox (manage_options): recent visits, each with its timeline in plain Hebrew
 *    (קומה 23, מבט למערב, נכנס לסיור, לחץ על וואטסאפ) and, for a visit that became a lead, the lead's name. The lead's own
 *    edit screen gets a box with its visit, the leads list a column, and the rich new-lead email of alerts.php (the
 *    action nadlan_lead_rich_alert) gets the timeline appended. A visit can be deleted from the list (a privacy request).
 *  - Retention: 12 months (a daily cron deletes older rows). Owner switch: the option nadlan_visit_trail = '0' stops
 *    everything (no script, nothing stored, no lead link). The team's own visits (users who can edit posts) are not
 *    recorded unless the page is opened with ?nlvt=1.
 * Loaded from the module list of nadlan-config.php ('visit-trail', after 'campaign-brief'). No long dashes, no tech words
 * on any visitor surface (this module has none).
 *
 * v1.1.0 (19.11.2026, Linear HAD-791, package 5 of the long-film gaps; Ben: "מוצר גמור"):
 *  - window.nlTrack(name, data): ONE small event call for every tool (designer, basket, offer, video call, mortgage, language),
 *    stored as the new event type 'act' (an allow list of fields, see nadlan_vt_schema). Contract for the sibling modules:
 *    docs/research/2026-11-19-buyer-events/CONTRACT.md. Also picked up with no change in their files: the nadlanGA() calls of
 *    the existing modules (basket_, cockpit_, offer_, room_, tour_, journey_, showroom_ ...), the designer's
 *    nadlan:design-order event, a number typed into a mortgage calculator (never the number) and, on the showroom engine
 *    pages (Rainbow, Ashira, DUO, H Infinity), a read-only look at window.NadLanEngine.state (engine.js stays frozen).
 *  - The script now loads on every front page: 'full' on a project page (as before, and now also on the engine's showroom
 *    pages, which recorded nothing until today), 'lite' elsewhere (only the explicit events above; no page-open record, no
 *    taps, no time on page).
 *  - Every event carries the PROJECT it belongs to (column proj, the Hebrew base project: a language page counts for its
 *    project), so the developer report (inc/dev-report.php, required at the end of this file) adds the tools on other pages
 *    (/tour/designer/, the basket) to the project's funnel.
 *  - The visitor's own opt-out: window.nlTrack.off() or any link to #nl-trail-off sets localStorage nl_vt_off=1; nothing runs
 *    after that (as with Global Privacy Control / Do Not Track).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
if ( defined( 'NADLAN_VT_VERSION' ) ) { return; }
define( 'NADLAN_VT_VERSION', '1.1.1' );
define( 'NADLAN_VT_DB', '2' );

if ( ! function_exists( 'nadlan_vt_tables' ) ) {
	function nadlan_vt_tables() {
		global $wpdb;
		return array( 'v' => $wpdb->prefix . 'nadlan_visits', 'e' => $wpdb->prefix . 'nadlan_visit_events' );
	}

	function nadlan_vt_on() { return '0' !== (string) get_option( 'nadlan_visit_trail', '1' ); }

	function nadlan_vt_limits() {
		return apply_filters( 'nadlan_vt_limits', array( 'body' => 16384, 'batch' => 60, 'client_min' => 30, 'visit' => 3000, 'day' => 200000, 'keep_days' => 365 ) );
	}

	/** the tables, created once (dbDelta) and again when NADLAN_VT_DB changes */
	function nadlan_vt_install( $force = false ) {
		if ( ! $force && NADLAN_VT_DB === (string) get_option( 'nadlan_vt_db', '' ) ) { return true; }
		global $wpdb;
		$t = nadlan_vt_tables();
		$c = $wpdb->get_charset_collate();
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		dbDelta( "CREATE TABLE {$t['v']} (
			vid VARCHAR(32) NOT NULL,
			first_at DATETIME NOT NULL,
			last_at DATETIME NOT NULL,
			country CHAR(2) NOT NULL DEFAULT '',
			lang VARCHAR(5) NOT NULL DEFAULT '',
			dev CHAR(1) NOT NULL DEFAULT '',
			ref VARCHAR(100) NOT NULL DEFAULT '',
			entry BIGINT UNSIGNED NOT NULL DEFAULT 0,
			pages INT UNSIGNED NOT NULL DEFAULT 0,
			events INT UNSIGNED NOT NULL DEFAULT 0,
			lead_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
			PRIMARY KEY  (vid),
			KEY last_at (last_at),
			KEY lead_id (lead_id)
		) $c;" );
		dbDelta( "CREATE TABLE {$t['e']} (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			vid VARCHAR(32) NOT NULL,
			pv VARCHAR(24) NOT NULL DEFAULT '',
			at DATETIME NOT NULL,
			page BIGINT UNSIGNED NOT NULL DEFAULT 0,
			lang VARCHAR(5) NOT NULL DEFAULT '',
			ev VARCHAR(12) NOT NULL,
			d VARCHAR(400) NOT NULL DEFAULT '',
			proj BIGINT UNSIGNED NOT NULL DEFAULT 0,
			PRIMARY KEY  (id),
			KEY vid_at (vid,at),
			KEY at (at),
			KEY page_at (page,at),
			KEY proj_at (proj,at)
		) $c;" );
		$ok = nadlan_vt_tables_exist( true );
		if ( $ok ) {
			// v2 (1.1.0): the rows of v1 were all recorded on a project page: their project is that page's base project
			$was = (string) get_option( 'nadlan_vt_db', '' );
			if ( '1' === $was ) {
				$pages = $wpdb->get_col( "SELECT DISTINCT page FROM {$t['e']} WHERE proj = 0 AND page > 0 LIMIT 2000" ); // phpcs:ignore
				foreach ( (array) $pages as $pg ) {
					$pj = nadlan_vt_canon_project( (int) $pg );
					if ( $pj > 0 ) { $wpdb->query( $wpdb->prepare( "UPDATE {$t['e']} SET proj = %d WHERE proj = 0 AND page = %d", $pj, (int) $pg ) ); } // phpcs:ignore
				}
			}
			update_option( 'nadlan_vt_db', NADLAN_VT_DB, true );
		}
		return $ok;
	}

	function nadlan_vt_tables_exist( $fresh = false ) {
		static $memo = null;
		if ( null !== $memo && ! $fresh ) { return $memo; }
		global $wpdb;
		$t = nadlan_vt_tables();
		$memo = $t['v'] === $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $wpdb->esc_like( $t['v'] ) ) )
			&& $t['e'] === $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $wpdb->esc_like( $t['e'] ) ) );
		return $memo;
	}

	function nadlan_vt_ready() {
		if ( NADLAN_VT_DB === (string) get_option( 'nadlan_vt_db', '' ) ) { return true; }
		return nadlan_vt_install( true );
	}

	/** a project page's base project: a language page (<slug>-en|fr|ru|ar) counts for its Hebrew project; 0 when not a published project */
	function nadlan_vt_canon_project( $id ) {
		static $memo = array();
		$id = (int) $id;
		if ( $id <= 0 ) { return 0; }
		if ( isset( $memo[ $id ] ) ) { return $memo[ $id ]; }
		$p = get_post( $id );
		if ( ! $p || 'nadlan_project' !== $p->post_type || 'publish' !== $p->post_status ) { return $memo[ $id ] = 0; }
		if ( preg_match( '/^(.+)-(en|fr|ru|ar)$/', (string) $p->post_name, $m ) ) {
			$b = get_page_by_path( $m[1], OBJECT, 'nadlan_project' );
			if ( $b && 'publish' === $b->post_status ) { return $memo[ $id ] = (int) $b->ID; }
		}
		return $memo[ $id ] = $id;
	}

	/** a project named by an event: a WordPress id or a slug ("rainbow-tel-aviv"; a short key "ashira" matches one project
	 *  whose slug starts with it); 0 for "mine", "example" or anything unknown */
	function nadlan_vt_project_ref( $ref ) {
		static $memo = array();
		if ( is_int( $ref ) || ( is_string( $ref ) && ctype_digit( $ref ) ) ) { return nadlan_vt_canon_project( (int) $ref ); }
		$s = sanitize_title( (string) $ref );
		if ( '' === $s || in_array( $s, array( 'mine', 'example', 'demo' ), true ) ) { return 0; }
		if ( isset( $memo[ $s ] ) ) { return $memo[ $s ]; }
		$tk = 'nadlan_vt_pref_' . md5( $s );
		$hit = get_transient( $tk );
		if ( false !== $hit ) { return $memo[ $s ] = (int) $hit; }
		$id = 0;
		$p  = get_page_by_path( $s, OBJECT, 'nadlan_project' );
		if ( $p ) {
			$id = nadlan_vt_canon_project( (int) $p->ID );
		} else {
			global $wpdb;
			$ids = $wpdb->get_col( $wpdb->prepare( "SELECT ID FROM {$wpdb->posts} WHERE post_type = 'nadlan_project' AND post_status = 'publish' AND post_name LIKE %s AND post_name NOT REGEXP '-(en|fr|ru|ar)$' LIMIT 3", $wpdb->esc_like( $s ) . '-%' ) ); // phpcs:ignore
			if ( 1 === count( (array) $ids ) ) { $id = nadlan_vt_canon_project( (int) $ids[0] ); }
		}
		set_transient( $tk, $id, 6 * HOUR_IN_SECONDS );
		return $memo[ $s ] = $id;
	}

	/* ---------------------------------------------------------------- what may be stored: an allow list per event */

	/** event => field => rule: an int is the longest text kept; 'f' floor, 'b' bearing, 'o' 0/1, 'ms' milliseconds, 'pct' 0-100 */
	function nadlan_vt_schema() {
		return array(
			'open'     => array(),
			'floor'    => array( 'f' => 'f', 'tw' => 16, 'src' => 8 ),
			'facing'   => array( 'f' => 'f', 'b' => 'b', 'dir' => 24, 'u' => 24, 'tw' => 16, 'lbl' => 40, 'src' => 8 ),
			'view'     => array( 'b' => 'b', 'src' => 8 ),
			'quarter'  => array( 'k' => 24, 'n' => 60 ),
			'facility' => array( 'n' => 60, 'id' => 32 ),
			'ftour'    => array( 'id' => 32, 'n' => 60 ),
			'fcta'     => array( 'f' => 'f', 'b' => 'b', 'tw' => 16 ),
			'faction'  => array( 'a' => 16, 'f' => 'f', 'u' => 24, 'tw' => 16 ),
			'tour'     => array( 'o' => 'o', 's' => 32 ),
			'example'  => array( 'o' => 'o', 'id' => 32, 'f' => 'f', 'tw' => 16, 'dir' => 24 ),
			'click'    => array( 'k' => 'key', 'l' => 40, 'w' => 'key', 'id' => 32, 'f' => 'f' ),
			'form'     => array( 'k' => 'key', 'id' => 32 ),
			'leave'    => array( 'vis' => 'ms', 'sc' => 'pct' ),
			// 1.1.0: one event of a tool, named by window.nlTrack(name, data) or mirrored from nadlanGA (n = the name)
			'act'      => array( 'n' => 'name', 'a' => 24, 'p' => 60, 'f' => 'f', 'u' => 24, 'tw' => 16, 'b' => 'b', 'dir' => 24,
				'rooms' => 'num', 'k' => 24, 'v' => 'num', 'src' => 12, 'to' => 'lang' ),
		);
	}

	/** the event types a page that is not a project page may send (the 'lite' tracker) */
	function nadlan_vt_lite_types() { return array( 'act' ); }

	function nadlan_vt_text( $s, $n ) {
		if ( ! is_scalar( $s ) ) { return ''; }
		$s = wp_strip_all_tags( (string) $s );
		$s = preg_replace( '/[\x00-\x1F\x7F]+/u', ' ', $s );
		$s = trim( (string) preg_replace( '/\s+/u', ' ', (string) $s ) );
		if ( '' === $s ) { return ''; }
		return function_exists( 'mb_substr' ) ? mb_substr( $s, 0, $n, 'UTF-8' ) : substr( $s, 0, $n );
	}

	/** one event, cleaned: array( type, data ) or null */
	function nadlan_vt_clean_event( $e ) {
		if ( ! is_array( $e ) ) { return null; }
		$sch  = nadlan_vt_schema();
		$type = isset( $e['t'] ) && is_string( $e['t'] ) ? $e['t'] : '';
		if ( ! isset( $sch[ $type ] ) ) { return null; }
		$o = array();
		foreach ( $sch[ $type ] as $k => $rule ) {
			if ( ! isset( $e[ $k ] ) || is_array( $e[ $k ] ) ) { continue; }
			$v = $e[ $k ];
			if ( 'f' === $rule ) {
				if ( ! is_numeric( $v ) ) { continue; }
				$v = (int) round( (float) $v );
				if ( $v < -5 || $v > 300 ) { continue; }
			} elseif ( 'b' === $rule ) {
				if ( ! is_numeric( $v ) ) { continue; }
				$v = ( (int) round( (float) $v ) % 360 + 360 ) % 360;
			} elseif ( 'o' === $rule ) {
				$v = $v ? 1 : 0;
			} elseif ( 'ms' === $rule ) {
				if ( ! is_numeric( $v ) ) { continue; }
				$v = max( 0, min( 86400000, (int) $v ) );
			} elseif ( 'pct' === $rule ) {
				if ( ! is_numeric( $v ) ) { continue; }
				$v = max( 0, min( 100, (int) $v ) );
			} elseif ( 'key' === $rule ) {
				$v = substr( sanitize_key( (string) $v ), 0, 16 );
				if ( '' === $v ) { continue; }
			} elseif ( 'name' === $rule ) {
				$v = strtolower( (string) $v );
				if ( ! preg_match( '/^[a-z][a-z0-9_.-]{1,39}$/', $v ) ) { continue; }
			} elseif ( 'num' === $rule ) {
				if ( ! is_numeric( $v ) ) { continue; }
				$v = (int) round( (float) $v );
				if ( $v < 0 || $v > 100000 ) { continue; }
			} elseif ( 'lang' === $rule ) {
				$v = strtolower( substr( (string) $v, 0, 2 ) );
				if ( ! in_array( $v, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ) { continue; }
			} else {
				$v = nadlan_vt_text( $v, (int) $rule );
				if ( '' === $v ) { continue; }
			}
			$o[ $k ] = $v;
		}
		if ( 'click' === $type && empty( $o['k'] ) ) { return null; }
		if ( 'act' === $type && empty( $o['n'] ) ) { return null; }
		return array( $type, $o );
	}

	/** the whole batch, cleaned; a WP_Error when its frame is wrong (the events that fail the allow list are dropped) */
	function nadlan_vt_clean_batch( $p, $now ) {
		$bad = function ( $why ) { return new WP_Error( 'nlvt_bad', 'Bad request.', array( 'status' => 400, 'why' => $why ) ); };
		if ( ! is_array( $p ) ) { return $bad( 'body' ); }
		if ( 1 !== (int) ( $p['v'] ?? 0 ) ) { return $bad( 'v' ); }
		$vid = is_string( $p['vid'] ?? null ) ? $p['vid'] : '';
		$pv  = is_string( $p['pv'] ?? null ) ? $p['pv'] : '';
		if ( ! preg_match( '/^[A-Za-z0-9_-]{16,32}$/', $vid ) ) { return $bad( 'vid' ); }
		if ( ! preg_match( '/^[A-Za-z0-9_-]{8,24}$/', $pv ) ) { return $bad( 'pv' ); }
		$page = (int) ( $p['page'] ?? 0 );
		$mode = 'lite' === ( $p['mode'] ?? '' ) ? 'lite' : 'full';
		if ( $page < 0 || ( $page <= 0 && 'full' === $mode ) ) { return $bad( 'page' ); }
		$evs = isset( $p['ev'] ) && is_array( $p['ev'] ) ? array_values( $p['ev'] ) : null;
		$lim = nadlan_vt_limits();
		if ( null === $evs || count( $evs ) > (int) $lim['batch'] ) { return $bad( 'ev' ); }
		$lang = is_string( $p['lang'] ?? null ) ? strtolower( substr( $p['lang'], 0, 2 ) ) : '';
		$dev  = is_string( $p['dev'] ?? null ) ? $p['dev'] : '';
		$ref  = is_string( $p['ref'] ?? null ) ? strtolower( $p['ref'] ) : '';
		$cnow = is_numeric( $p['now'] ?? null ) ? (float) $p['now'] : 0.0;
		$out  = array(
			'vid'  => $vid,
			'pv'   => $pv,
			'seq'  => max( 0, min( 100000, (int) ( $p['seq'] ?? 0 ) ) ),
			'page' => $page,
			'mode' => $mode,
			'proj' => max( 0, (int) ( $p['proj'] ?? 0 ) ),
			'lang' => in_array( $lang, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $lang : '',
			'dev'  => in_array( $dev, array( 'm', 't', 'd' ), true ) ? $dev : '',
			'ref'  => preg_match( '/^[a-z0-9.-]{3,100}$/', $ref ) ? $ref : '',
			'ev'   => array(),
		);
		foreach ( $evs as $e ) {
			$c = nadlan_vt_clean_event( $e );
			if ( ! $c ) { continue; }
			// the event's time on the server's clock: the client's age of the event (now - at), at most two hours back
			$age = 0;
			if ( $cnow > 0 && is_array( $e ) && is_numeric( $e['at'] ?? null ) ) {
				$age = (int) max( 0, min( 7200, round( ( $cnow - (float) $e['at'] ) / 1000 ) ) );
			}
			$out['ev'][] = array( 't' => $c[0], 'd' => $c[1], 'ts' => (int) $now - $age );
		}
		return $out;
	}

	/* ---------------------------------------------------------------- the request */

	function nadlan_vt_country() {
		foreach ( array( 'HTTP_CF_IPCOUNTRY', 'HTTP_X_COUNTRY_CODE', 'HTTP_X_GEO_COUNTRY', 'HTTP_X_UPRESS_COUNTRY', 'HTTP_GEOIP_COUNTRY_CODE', 'GEOIP_COUNTRY_CODE', 'HTTP_X_GEOIP_COUNTRY' ) as $k ) {
			if ( empty( $_SERVER[ $k ] ) ) { continue; }
			$c = strtoupper( substr( preg_replace( '/[^A-Za-z]/', '', (string) wp_unslash( $_SERVER[ $k ] ) ), 0, 2 ) ); // phpcs:ignore -- two letters only
			if ( preg_match( '/^[A-Z]{2}$/', $c ) && ! in_array( $c, array( 'XX', 'T1', 'ZZ', 'EU', 'AP' ), true ) ) { return $c; }
		}
		return '';
	}

	/** Global Privacy Control or Do Not Track on the request: nothing is stored */
	function nadlan_vt_signal( $req = null ) {
		$gpc = $req ? (string) $req->get_header( 'sec_gpc' ) : (string) ( $_SERVER['HTTP_SEC_GPC'] ?? '' ); // phpcs:ignore
		$dnt = $req ? (string) $req->get_header( 'dnt' ) : (string) ( $_SERVER['HTTP_DNT'] ?? '' ); // phpcs:ignore
		return '1' === trim( $gpc ) || '1' === trim( $dnt );
	}

	function nadlan_vt_robot_ua( $ua ) {
		return '' === trim( (string) $ua ) || (bool) preg_match( '/bot|crawl|spider|slurp|headless|lighthouse|pagespeed|gtmetrix|pingdom|prerender|curl|wget|python-requests|httpclient/i', (string) $ua );
	}

	/** a counter in a transient: false once $max is reached inside the window */
	function nadlan_vt_limit( $bucket, $max, $window ) {
		$k = 'nadlan_vt_rl_' . md5( (string) $bucket );
		$n = (int) get_transient( $k );
		if ( $n >= $max ) { return false; }
		set_transient( $k, $n + 1, $window );
		return true;
	}
	function nadlan_vt_client() {
		if ( function_exists( 'nadlan_hardening_client_key' ) ) { return nadlan_hardening_client_key(); }
		return 'ip' . md5( substr( (string) ( $_SERVER['REMOTE_ADDR'] ?? '' ), 0, 80 ) ); // phpcs:ignore -- hashed, never stored
	}
	/** a browser request from another site is refused; a request without Origin (an old browser) is allowed, and limited */
	function nadlan_vt_same_origin( $req ) {
		$o = (string) $req->get_header( 'origin' );
		if ( '' === $o ) { return true; }
		if ( 'null' === $o ) { return false; }
		$h  = strtolower( (string) wp_parse_url( $o, PHP_URL_HOST ) );
		$me = strtolower( (string) wp_parse_url( home_url( '/' ), PHP_URL_HOST ) );
		$strip = function ( $x ) { return preg_replace( '/^www\./', '', $x ); };
		return '' !== $h && $strip( $h ) === $strip( $me );
	}

	/** POST /wp-json/nadlan/v1/trail. 204 when stored (or when nothing may be stored), an error otherwise. */
	function nadlan_vt_rest( $req ) {
		$none = new WP_REST_Response( null, 204 );
		$lim  = nadlan_vt_limits();
		$raw  = (string) $req->get_body();
		if ( strlen( $raw ) > (int) $lim['body'] ) { return new WP_Error( 'nlvt_big', 'Request too large.', array( 'status' => 413 ) ); }
		$p = json_decode( $raw, true );
		if ( ! is_array( $p ) ) { return new WP_Error( 'nlvt_bad', 'Bad request.', array( 'status' => 400 ) ); }
		if ( ! nadlan_vt_on() || nadlan_vt_signal( $req ) ) { return $none; }
		if ( ! nadlan_vt_same_origin( $req ) ) { return new WP_Error( 'nlvt_origin', 'Forbidden.', array( 'status' => 403 ) ); }
		if ( nadlan_vt_robot_ua( $req->get_header( 'user_agent' ) ) ) { return $none; }
		$now = time();
		$b   = nadlan_vt_clean_batch( $p, $now );
		if ( is_wp_error( $b ) ) { return $b; }
		if ( ! $b['ev'] ) { return $none; }
		// the page's project: a project page records everything; any other page (or a route with no post, page 0) only the
		// explicit tool events ('lite'), each counted for the project it names (or the batch's project, or none)
		$pp = $b['page'] > 0 && 'nadlan_project' === get_post_type( $b['page'] ) ? nadlan_vt_canon_project( $b['page'] ) : 0;
		if ( 'full' === $b['mode'] && $pp <= 0 ) { return new WP_Error( 'nlvt_bad', 'Bad request.', array( 'status' => 400, 'why' => 'page' ) ); }
		// 1.1.1 (owner live alerts): /developers/ and /marketing/ send one 'open' in lite mode, kept here so the owner hears of the visit
		$watch = function_exists( 'nadlan_ol_watch_path' ) && is_string( $p['path'] ?? null ) ? nadlan_ol_watch_path( $p['path'] ) : '';
		if ( $pp <= 0 ) {
			if ( $b['page'] > 0 && 'publish' !== get_post_status( $b['page'] ) ) { return new WP_Error( 'nlvt_bad', 'Bad request.', array( 'status' => 400, 'why' => 'page' ) ); }
			$lite = nadlan_vt_lite_types();
			if ( '' !== $watch ) { $lite[] = 'open'; }
			$b['ev'] = array_values( array_filter( $b['ev'], function ( $e ) use ( $lite ) { return in_array( $e['t'], $lite, true ); } ) );
			if ( ! $b['ev'] ) { return $none; }
		}
		$bp = $pp > 0 ? $pp : ( $b['proj'] > 0 ? nadlan_vt_canon_project( $b['proj'] ) : 0 );
		foreach ( $b['ev'] as $i => $e ) {
			$ep = isset( $e['d']['p'] ) ? nadlan_vt_project_ref( $e['d']['p'] ) : 0;
			$b['ev'][ $i ]['proj'] = $ep > 0 ? $ep : $bp;
		}
		if ( ! nadlan_vt_limit( 'c|' . nadlan_vt_client() . '|' . gmdate( 'YmdHi', $now ), (int) $lim['client_min'], 2 * MINUTE_IN_SECONDS ) ) {
			return new WP_Error( 'nlvt_rate', 'Too many requests.', array( 'status' => 429 ) );
		}
		$dk = 'nadlan_vt_day_' . gmdate( 'Ymd', $now );
		$day = (int) get_transient( $dk );
		if ( $day >= (int) $lim['day'] ) { return new WP_Error( 'nlvt_rate', 'Too many requests.', array( 'status' => 429 ) ); }
		if ( ! nadlan_vt_ready() ) { return new WP_Error( 'nlvt_store', 'Could not save.', array( 'status' => 500 ) ); }
		$n = nadlan_vt_store( $b, nadlan_vt_country(), $now );
		set_transient( $dk, $day + $n, DAY_IN_SECONDS + HOUR_IN_SECONDS );
		if ( $n > 0 ) { do_action( 'nadlan_vt_stored', $b, $watch ); } // owner-live.php: alerts, sent after the response
		return $none;
	}

	/** the batch into the two tables; the number of events stored */
	function nadlan_vt_store( $b, $country, $now ) {
		global $wpdb;
		$t    = nadlan_vt_tables();
		$lim  = nadlan_vt_limits();
		$have = (int) $wpdb->get_var( $wpdb->prepare( "SELECT events FROM {$t['v']} WHERE vid = %s", $b['vid'] ) );
		$room = (int) $lim['visit'] - $have;
		if ( $room <= 0 ) { return 0; }
		$evs = array_slice( $b['ev'], 0, $room );
		if ( ! $evs ) { return 0; }
		$first = $now;
		$last  = 0;
		$open  = 0;
		$entry = 'full' === ( $b['mode'] ?? 'full' ) ? (int) $b['page'] : 0;
		$vals  = array();
		$args  = array();
		foreach ( $evs as $e ) {
			$first = min( $first, $e['ts'] );
			$last  = max( $last, $e['ts'] );
			if ( 'open' === $e['t'] ) { $open++; }
			$d = $e['d'] ? wp_json_encode( $e['d'], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) : '';
			if ( ! is_string( $d ) || ( function_exists( 'mb_strlen' ) ? mb_strlen( $d, 'UTF-8' ) : strlen( $d ) ) > 400 ) { $d = ''; }
			$vals[] = '(%s,%s,%s,%d,%s,%s,%s,%d)';
			array_push( $args, $b['vid'], $b['pv'], gmdate( 'Y-m-d H:i:s', $e['ts'] ), $b['page'], $b['lang'], $e['t'], $d, (int) ( $e['proj'] ?? 0 ) );
			if ( ! $entry && ! empty( $e['proj'] ) ) { $entry = (int) $e['proj']; }
		}
		$wpdb->query( $wpdb->prepare(
			"INSERT INTO {$t['v']} (vid, first_at, last_at, country, lang, dev, ref, entry, pages, events, lead_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%d,%d,%d,0)
			ON DUPLICATE KEY UPDATE first_at = LEAST(first_at, VALUES(first_at)), last_at = GREATEST(last_at, VALUES(last_at)),
			country = IF(country = '', VALUES(country), country), lang = IF(lang = '', VALUES(lang), lang), dev = IF(dev = '', VALUES(dev), dev),
			ref = IF(ref = '', VALUES(ref), ref), entry = IF(entry = 0, VALUES(entry), entry), pages = pages + VALUES(pages), events = events + VALUES(events)",
			$b['vid'], gmdate( 'Y-m-d H:i:s', $first ), gmdate( 'Y-m-d H:i:s', $last ), (string) $country, $b['lang'], $b['dev'], $b['ref'], $entry, $open, count( $evs )
		) );
		$wpdb->query( $wpdb->prepare( "INSERT INTO {$t['e']} (vid, pv, at, page, lang, ev, d, proj) VALUES " . implode( ',', $vals ), $args ) ); // phpcs:ignore -- placeholders only
		return count( $evs );
	}

	/* ---------------------------------------------------------------- the lead link */

	/** the visit id the current request carries (the header X-NL-Visit, the REST param or the form field nl_visit), or '' */
	function nadlan_vt_request_vid() {
		$c = array();
		if ( isset( $GLOBALS['nadlan_vt_rest_vid'] ) ) { $c[] = $GLOBALS['nadlan_vt_rest_vid']; }
		if ( ! empty( $_SERVER['HTTP_X_NL_VISIT'] ) ) { $c[] = wp_unslash( $_SERVER['HTTP_X_NL_VISIT'] ); } // phpcs:ignore -- matched below
		if ( isset( $_POST['nl_visit'] ) ) { $c[] = wp_unslash( $_POST['nl_visit'] ); } // phpcs:ignore -- matched below, no nonce: it is an id, not an action
		foreach ( $c as $v ) {
			if ( is_string( $v ) && preg_match( '/^[A-Za-z0-9_-]{16,32}$/', $v ) ) { return $v; }
		}
		return '';
	}

	/** the lead carries the visit (meta _nl_visit) and the visit its first lead (a stub row when the trail has not arrived yet) */
	function nadlan_vt_link_lead( $lead_id, $vid ) {
		$lead_id = (int) $lead_id;
		if ( $lead_id <= 0 || '' === (string) $vid || ! nadlan_vt_on() || nadlan_vt_signal() ) { return false; }
		update_post_meta( $lead_id, '_nl_visit', $vid );
		if ( ! nadlan_vt_ready() ) { return false; }
		global $wpdb;
		$t   = nadlan_vt_tables();
		$now = gmdate( 'Y-m-d H:i:s' );
		$wpdb->query( $wpdb->prepare(
			"INSERT INTO {$t['v']} (vid, first_at, last_at, lead_id) VALUES (%s,%s,%s,%d)
			ON DUPLICATE KEY UPDATE lead_id = IF(lead_id = 0, VALUES(lead_id), lead_id), last_at = GREATEST(last_at, VALUES(last_at))",
			$vid, $now, $now, $lead_id
		) );
		return true;
	}

	/* ---------------------------------------------------------------- the timeline, in plain Hebrew */

	function nadlan_vt_dir_word( $b ) {
		if ( null === $b || '' === $b ) { return ''; }
		$w = array( 'צפון', 'צפון מזרח', 'מזרח', 'דרום מזרח', 'דרום', 'דרום מערב', 'מערב', 'צפון מערב' );
		return $w[ (int) round( ( ( (int) $b % 360 + 360 ) % 360 ) / 45 ) % 8 ];
	}

	function nadlan_vt_title( $page ) {
		static $memo = array();
		$page = (int) $page;
		if ( ! isset( $memo[ $page ] ) ) { $memo[ $page ] = $page > 0 ? (string) get_the_title( $page ) : ''; }
		return $memo[ $page ];
	}

	function nadlan_vt_langs() { return array( 'he' => 'עברית', 'en' => 'אנגלית', 'fr' => 'צרפתית', 'ru' => 'רוסית', 'ar' => 'ערבית' ); }

	/** 1.1.0: one tool event (type 'act') as plain words, in Hebrew or English: "בחר קומה 23" / "Chose floor 23" */
	function nadlan_vt_act_text( $d, $lang = 'he' ) {
		$d  = is_array( $d ) ? $d : array();
		$en = 'en' === $lang;
		$n  = (string) ( $d['n'] ?? '' );
		$g  = function ( $k ) use ( $d ) { return isset( $d[ $k ] ) ? (string) $d[ $k ] : ''; };
		$fl = '' !== $g( 'f' ) ? ( $en ? ' floor ' : ' קומה ' ) . $g( 'f' ) : '';
		$un = '' !== $g( 'u' ) ? ( $en ? ', unit ' : ', דירה ' ) . $g( 'u' ) : '';
		$dw = '' !== $g( 'dir' ) ? $g( 'dir' ) : ( '' !== $g( 'b' ) ? ( $en ? nadlan_vt_dir_word_en( (int) $g( 'b' ) ) : nadlan_vt_dir_word( (int) $g( 'b' ) ) ) : '' );
		$langs = $en ? array( 'he' => 'Hebrew', 'en' => 'English', 'fr' => 'French', 'ru' => 'Russian', 'ar' => 'Arabic' ) : nadlan_vt_langs();
		$acts = array( // designer_action a=...
			'finish' => array( 'בחר גימור', 'picked a finish' ), 'partition-add' => array( 'הוסיף קיר', 'added a wall' ),
			'partition-remove' => array( 'הסיר קיר', 'removed a wall' ), 'point-add' => array( 'הוסיף נקודת חשמל או מים', 'added a power or water point' ),
			'point-move' => array( 'הזיז נקודה', 'moved a point' ), 'item-add' => array( 'הוסיף רהיט', 'added furniture' ),
			'note' => array( 'השאיר הערה על התוכנית', 'left a note on the plan' ), 'walk' => array( 'הלך בתוך הדירה', 'walked through the apartment' ),
			'plan-load' => array( 'העלה תוכנית משלו', 'loaded his own plan' ), 'scan' => array( 'צילם את הדירה לתוכנית', 'scanned the apartment' ),
		);
		$i = $en ? 1 : 0;
		$map = array(
			'floor_select'     => array( 'בחר' . ( $fl ?: ' קומה' ), 'Chose' . ( $fl ?: ' a floor' ) ),
			'direction_select' => array( 'בחר כיוון' . ( $dw ? ': ' . $dw : '' ) . $fl . $un, 'Chose a side' . ( $dw ? ': ' . $dw : '' ) . $fl . $un ),
			'unit_open'        => array( 'פתח דירה' . $fl . $un, 'Opened an apartment' . $fl . $un ),
			'view_open'        => array( 'פתח את הנוף' . ( $fl ? ' מ' . trim( $fl ) : '' ) . ( $dw ? ', ' . $dw : '' ), 'Opened the view' . ( $fl ? ' from' . $fl : '' ) . ( $dw ? ', ' . $dw : '' ) ),
			'view_turn'        => array( 'סובב את הנוף' . ( $dw ? ' אל ה' . $dw : '' ), 'Turned the view' . ( $dw ? ' to ' . $dw : '' ) ),
			'designer_open'    => array( 'פתח את מעצב הדירה' . $un, 'Opened the apartment designer' . $un ),
			'designer_action'  => array( 'במעצב: ' . ( $acts[ $g( 'a' ) ][0] ?? 'פעולה' ), 'Designer: ' . ( $acts[ $g( 'a' ) ][1] ?? 'a step' ) ),
			'design_order'     => array( 'הוסיף את העיצוב לסל' . $un, 'Added the design to the basket' . $un ),
			'mortgage_check'   => array( 'בדק החזר חודשי', 'Checked the monthly payment' ),
			'basket_add'       => array( 'הוסיף לסל' . $un, 'Added to the basket' . $un ),
			'basket_remove'    => array( 'הוציא מהסל' . $un, 'Removed from the basket' . $un ),
			'basket_open'      => array( 'פתח את הסל', 'Opened the basket' ),
			'call_open'        => array( 'פתח שיחת וידאו', 'Opened the video call' ),
			'call_book'        => array( 'קבע שיחה', 'Booked a call' ),
			'call_join'        => array( 'נכנס לשיחה חיה', 'Joined a live call' ),
			'rfp_open'         => array( 'פתח בקשה להצעה', 'Opened the offer request' ),
			'rfp_send'         => array( 'שלח בקשה להצעה', 'Sent an offer request' ),
			'reserve_start'    => array( 'פתח את שריון הדירה' . $un, 'Opened the reservation step' . $un ),
			'reserve_request'  => array( 'ביקש לשריין את הדירה' . $un, 'Asked to reserve the apartment' . $un ),
			'lang_switch'      => array( 'עבר לשפה ' . ( $langs[ $g( 'to' ) ] ?? '' ), 'Switched to ' . ( $langs[ $g( 'to' ) ] ?? 'another language' ) ),
			'favorite'         => array( 'שמר דירה' . $un, 'Saved an apartment' . $un ),
			'share'            => array( 'שיתף' . $un, 'Shared' . $un ),
			'plan_open'        => array( 'פתח את תוכנית הדירה' . $un, 'Opened the floor plan' . $un ),
			'tour_open'        => array( 'נכנס לסיור בדירה' . $un, 'Entered the apartment tour' . $un ),
			'area_open'        => array( 'פתח את הסביבה', 'Opened the area' ),
			'contact_open'     => array( 'פתח את טופס הפנייה', 'Opened the contact form' ),
			'compare_open'     => array( 'השווה דירות', 'Compared apartments' ),
		);
		if ( isset( $map[ $n ] ) ) { return trim( $map[ $n ][ $i ] ); }
		// a mirrored nadlanGA name: shown as it is, readable
		return ( $en ? 'Action: ' : 'פעולה: ' ) . str_replace( '_', ' ', $n ) . ( '' !== $g( 'k' ) ? ' (' . $g( 'k' ) . ')' : '' );
	}

	function nadlan_vt_dir_word_en( $b ) {
		$w = array( 'north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west' );
		return $w[ (int) round( ( ( (int) $b % 360 + 360 ) % 360 ) / 45 ) % 8 ];
	}

	/** one event as one plain line: "בחר כיוון בקומה 23: מערב (268°), דירה 23-w" */
	function nadlan_vt_line( $ev, $d, $page = 0, $lang = '' ) {
		$d  = is_array( $d ) ? $d : array();
		$g  = function ( $k ) use ( $d ) { return isset( $d[ $k ] ) ? (string) $d[ $k ] : ''; };
		$fl = '' !== $g( 'f' ) ? 'קומה ' . $g( 'f' ) : '';
		$tw = '' !== $g( 'tw' ) ? ' במגדל ' . $g( 'tw' ) : '';
		$deg = '' !== $g( 'b' ) ? ' (' . $g( 'b' ) . '°)' : '';
		$dir = '' !== $g( 'dir' ) ? $g( 'dir' ) : nadlan_vt_dir_word( '' !== $g( 'b' ) ? (int) $g( 'b' ) : null );
		$auto = ( '' !== $g( 'src' ) && 'user' !== $g( 'src' ) ) ? ' (אוטומטית)' : '';
		$where = array( 'bar' => 'בפס הוואטסאפ', 'card' => 'בכרטיס', 'view' => 'באזור הנוף', 'stage' => 'בהדמיה', 'hero' => 'בראש העמוד',
			'booking' => 'בתיאום הפגישה', 'price' => 'במחירון', 'footer' => 'בתחתית העמוד', 'header' => 'בתפריט', 'article' => 'בכתבה' );
		$at = isset( $where[ $g( 'w' ) ] ) ? ' ' . $where[ $g( 'w' ) ] : '';
		$q  = function ( $s ) { return '' !== $s ? ' "' . $s . '"' : ''; };
		switch ( $ev ) {
			case 'open':
				$langs = nadlan_vt_langs();
				return 'נכנס לעמוד ' . ( nadlan_vt_title( $page ) ?: 'הפרויקט' ) . ( $lang && 'he' !== $lang && isset( $langs[ $lang ] ) ? ' (' . $langs[ $lang ] . ')' : '' );
			case 'floor':
				return 'בחר ' . ( $fl ?: 'קומה' ) . $tw . $auto;
			case 'facing':
				return 'בחר כיוון' . ( $fl ? ' ב' . $fl : '' ) . $tw . ': ' . ( $dir ?: 'לא ידוע' ) . $deg
					. ( '' !== $g( 'lbl' ) ? ', ' . $g( 'lbl' ) : ( '' !== $g( 'u' ) ? ', דירה ' . $g( 'u' ) : '' ) ) . $auto;
			case 'view':
				return 'סובב את הנוף מהקומה' . ( $dir ? ' אל ה' . $dir : '' ) . $deg;
			case 'quarter':
				return 'לחץ במפת הסביבה על' . $q( $g( 'n' ) ) . ( '' !== $g( 'k' ) ? ' (' . $g( 'k' ) . ')' : '' );
			case 'facility':
				return 'פתח את המתקן' . $q( $g( 'n' ) );
			case 'ftour':
				return 'נכנס לסיור 360° במתקן' . $q( $g( 'n' ) ?: $g( 'id' ) );
			case 'fcta':
				return 'לחץ על וואטסאפ מכרטיס ה' . ( $fl ?: 'קומה' ) . $tw . ( $dir ? ', מבט ל' . $dir . $deg : '' );
			case 'faction':
				$acts = array( 'inside' => 'נכנס לדירה ב־360°', 'view' => 'פתח את הנוף', 'design' => 'פתח את עיצוב הדירה' );
				return ( isset( $acts[ $g( 'a' ) ] ) ? $acts[ $g( 'a' ) ] : 'לחץ בכרטיס הקומה על' . $q( $g( 'a' ) ) ) . ( $fl ? ' מ' . $fl : '' ) . $tw . ( '' !== $g( 'u' ) ? ', דירה ' . $g( 'u' ) : '' );
			case 'tour':
				return $g( 'o' ) ? 'פתח סיור בתוך הדירה' . ( '' !== $g( 's' ) ? ' (' . $g( 's' ) . ')' : '' ) : 'סגר את הסיור בדירה';
			case 'example':
				return $g( 'o' ) ? 'פתח דירה לדוגמה' . ( '' !== $g( 'id' ) ? ' ' . $g( 'id' ) : '' ) . ( $fl ? ' ב' . $fl : '' ) . $tw . ( '' !== $g( 'dir' ) ? ', מבט ל' . $g( 'dir' ) : '' ) : 'סגר את הדירה לדוגמה';
			case 'click':
				$k = $g( 'k' );
				$names = array( 'wa' => 'לחץ על וואטסאפ', 'tel' => 'לחץ על חיוג', 'mail' => 'לחץ על מייל', 'book' => 'לחץ בתיאום הפגישה',
					'book_day' => 'בחר יום לפגישה', 'book_time' => 'בחר שעה לפגישה', 'book_send' => 'שלח בקשה לפגישה', 'tour_btn' => 'לחץ על הסיור בדירה',
					'send' => 'לחץ על שליחה בטופס' );
				if ( 'deal_floor' === $k ) { return 'לחץ "לקומה במגדל" בטבלת העסקאות' . ( $fl ? ' (' . $fl . ')' : '' ); }
				if ( 'step' === $k ) { return 'לחץ על השלב' . $q( $g( 'l' ) ?: $g( 'id' ) ) . $at; }
				if ( isset( $names[ $k ] ) ) { return $names[ $k ] . ( 'send' !== $k && 'book_day' !== $k && 'book_time' !== $k ? $q( $g( 'l' ) ) : '' ) . $at; }
				return 'לחץ על' . ( $q( $g( 'l' ) ) ?: ' כפתור' ) . ( 'cta' !== $k ? ' (' . $k . ')' : '' ) . $at;
			case 'form':
				$fk = array( 'lead' => 'שלח טופס פנייה', 'book' => 'שלח טופס פגישה' );
				return ( isset( $fk[ $g( 'k' ) ] ) ? $fk[ $g( 'k' ) ] : 'שלח טופס' ) . ( '' !== $g( 'id' ) ? ' (' . $g( 'id' ) . ')' : '' );
			case 'act':
				return nadlan_vt_act_text( $d, 'he' );
			case 'leave':
				$s = (int) round( (int) $g( 'vis' ) / 1000 );
				return 'יצא מהעמוד אחרי ' . floor( $s / 60 ) . ':' . str_pad( (string) ( $s % 60 ), 2, '0', STR_PAD_LEFT ) . ' דקות בעמוד' . ( '' !== $g( 'sc' ) ? ', גלל עד ' . $g( 'sc' ) . '% מהעמוד' : '' );
		}
		return $ev;
	}

	/** the events of visits, by visit id, oldest first (at most $per each) */
	function nadlan_vt_events_of( $vids, $per = 300 ) {
		global $wpdb;
		$vids = array_values( array_filter( array_map( 'strval', (array) $vids ), function ( $v ) { return (bool) preg_match( '/^[A-Za-z0-9_-]{16,32}$/', $v ); } ) );
		if ( ! $vids || ! nadlan_vt_tables_exist() ) { return array(); }
		$t   = nadlan_vt_tables();
		$in  = implode( ',', array_fill( 0, count( $vids ), '%s' ) );
		$rows = $wpdb->get_results( $wpdb->prepare( "SELECT vid, pv, at, page, lang, ev, d FROM {$t['e']} WHERE vid IN ($in) ORDER BY at ASC, id ASC LIMIT %d", array_merge( $vids, array( count( $vids ) * $per ) ) ) ); // phpcs:ignore
		$out = array();
		foreach ( (array) $rows as $r ) {
			if ( isset( $out[ $r->vid ] ) && count( $out[ $r->vid ] ) >= $per ) { continue; }
			$out[ $r->vid ][] = $r;
		}
		return $out;
	}

	/** the timeline as lines "14:03 · בחר קומה 23"; a leave event is kept only as the page view's last one */
	function nadlan_vt_lines( $rows, $fmt = 'H:i' ) {
		$rows = array_values( (array) $rows );
		$lastLeave = array();
		foreach ( $rows as $i => $r ) { if ( 'leave' === $r->ev ) { $lastLeave[ $r->pv ] = $i; } }
		$out = array();
		foreach ( $rows as $i => $r ) {
			if ( 'leave' === $r->ev && $lastLeave[ $r->pv ] !== $i ) { continue; }
			$ts = strtotime( $r->at . ' UTC' );
			$out[] = array( 'time' => function_exists( 'wp_date' ) ? wp_date( $fmt, $ts ) : gmdate( $fmt, $ts ), 'text' => nadlan_vt_line( $r->ev, json_decode( (string) $r->d, true ), $r->page, $r->lang ), 'ev' => $r->ev );
		}
		return $out;
	}

	/** the lines of a lead's visit (the last $max), plain text */
	function nadlan_vt_lead_lines( $lead_id, $max = 25 ) {
		$vid = (string) get_post_meta( (int) $lead_id, '_nl_visit', true );
		if ( '' === $vid ) { return array(); }
		$ev  = nadlan_vt_events_of( array( $vid ) );
		$ln  = nadlan_vt_lines( $ev[ $vid ] ?? array(), 'd/m H:i' );
		if ( count( $ln ) > $max ) { $ln = array_slice( $ln, -$max ); }
		return array_map( function ( $l ) { return $l['time'] . ' · ' . $l['text']; }, $ln );
	}

	function nadlan_vt_admin_url( $args = array() ) { return add_query_arg( $args, admin_url( 'admin.php?page=nadlan-visit-trails' ) ); }

	/* ---------------------------------------------------------------- the admin screen */

	function nadlan_vt_summary( $days = 7 ) {
		global $wpdb;
		if ( ! nadlan_vt_tables_exist() ) { return array(); }
		$t    = nadlan_vt_tables();
		$from = gmdate( 'Y-m-d H:i:s', time() - $days * DAY_IN_SECONDS );
		$row  = $wpdb->get_row( $wpdb->prepare( "SELECT COUNT(DISTINCT vid) AS visits,
			COUNT(DISTINCT CASE WHEN ev IN ('floor','facing') THEN vid END) AS floor,
			COUNT(DISTINCT CASE WHEN ev IN ('tour','example','ftour','faction') THEN vid END) AS tour,
			COUNT(DISTINCT CASE WHEN (ev = 'click' AND d LIKE %s) OR ev = 'fcta' THEN vid END) AS wa
			FROM {$t['e']} WHERE at >= %s", '%"k":"wa"%', $from ), ARRAY_A ); // phpcs:ignore
		$leads = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$t['v']} WHERE lead_id > 0 AND last_at >= %s", $from ) ); // phpcs:ignore
		return array_merge( array_map( 'intval', (array) $row ), array( 'leads' => $leads ) );
	}

	/** the screen's HTML; $a: leads (1 = only visits that became leads), vid, project, paged */
	function nadlan_vt_admin_html( $a ) {
		global $wpdb;
		$h  = '<div class="wrap nlvt" dir="rtl"><h1>מסלולי ביקור</h1>';
		$h .= '<p class="description">מה מבקרים בחרו ולחצו בעמודי הפרויקטים: קומה, כיוון, סיור, דירה לדוגמה, וואטסאפ ותיאום פגישה. בלי מה שהוקלד ובלי כתובת IP; נמחק אחרי 12 חודשים.'
			. ( nadlan_vt_on() ? '' : ' <b>התיעוד כבוי כרגע (האפשרות nadlan_visit_trail).</b>' ) . '</p>';
		$h .= '<style>.nlvt table td{vertical-align:top}.nlvt details summary{cursor:pointer;color:#2271b1}.nlvt ol{margin:6px 22px 4px 0;padding:0}.nlvt ol li{margin:2px 0;font-size:13px}.nlvt .t{color:#646970;font-variant-numeric:tabular-nums;margin-left:8px}.nlvt .k-click,.nlvt .k-fcta,.nlvt .k-form{font-weight:600}.nlvt .sum{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}.nlvt .sum div{background:#fff;border:1px solid #dcdcde;border-radius:6px;padding:8px 14px}.nlvt .sum b{display:block;font-size:20px}</style>';
		if ( ! nadlan_vt_tables_exist() ) {
			return $h . '<p>עוד לא נרשם אף ביקור.</p></div>';
		}
		$s = nadlan_vt_summary( 7 );
		$h .= '<div class="sum">';
		foreach ( array( 'visits' => 'ביקורים ב־7 ימים', 'floor' => 'בחרו קומה או כיוון', 'tour' => 'פתחו סיור או דירה לדוגמה', 'wa' => 'לחצו על וואטסאפ', 'leads' => 'השאירו פנייה' ) as $k => $lbl ) {
			$h .= '<div><b>' . esc_html( number_format_i18n( (int) ( $s[ $k ] ?? 0 ) ) ) . '</b>' . esc_html( $lbl ) . '</div>';
		}
		$h .= '</div>';
		$t     = nadlan_vt_tables();
		$where = array( '1=1' );
		$args  = array();
		$vid   = isset( $a['vid'] ) && preg_match( '/^[A-Za-z0-9_-]{16,32}$/', (string) $a['vid'] ) ? (string) $a['vid'] : '';
		if ( $vid ) { $where[] = 'vid = %s'; $args[] = $vid; }
		if ( ! empty( $a['leads'] ) ) { $where[] = 'lead_id > 0'; }
		$proj = (int) ( $a['project'] ?? 0 );
		if ( $proj > 0 ) { $where[] = "vid IN (SELECT DISTINCT vid FROM {$t['e']} WHERE page = %d)"; $args[] = $proj; }
		$per   = 30;
		$paged = max( 1, (int) ( $a['paged'] ?? 1 ) );
		$sqlw  = implode( ' AND ', $where );
		$total = (int) $wpdb->get_var( $args ? $wpdb->prepare( "SELECT COUNT(*) FROM {$t['v']} WHERE $sqlw", $args ) : "SELECT COUNT(*) FROM {$t['v']} WHERE $sqlw" ); // phpcs:ignore
		$rows  = $wpdb->get_results( $wpdb->prepare( "SELECT * FROM {$t['v']} WHERE $sqlw ORDER BY last_at DESC LIMIT %d OFFSET %d", array_merge( $args, array( $per, ( $paged - 1 ) * $per ) ) ) ); // phpcs:ignore
		// filters
		$pages = $wpdb->get_col( $wpdb->prepare( "SELECT DISTINCT page FROM {$t['e']} WHERE at >= %s AND page > 0 LIMIT 200", gmdate( 'Y-m-d H:i:s', time() - 90 * DAY_IN_SECONDS ) ) ); // phpcs:ignore
		$h .= '<form method="get" style="margin:10px 0"><input type="hidden" name="page" value="nadlan-visit-trails">';
		$h .= '<label><input type="checkbox" name="leads" value="1"' . checked( ! empty( $a['leads'] ), true, false ) . '> רק ביקורים שהפכו לפנייה</label> &nbsp; ';
		$h .= '<select name="project"><option value="0">כל הפרויקטים</option>';
		foreach ( (array) $pages as $pid ) { $h .= '<option value="' . (int) $pid . '"' . selected( $proj, (int) $pid, false ) . '>' . esc_html( nadlan_vt_title( $pid ) ?: ( '#' . (int) $pid ) ) . '</option>'; }
		$h .= '</select> <button class="button">הצגה</button>';
		if ( $vid ) { $h .= ' <a class="button-link" href="' . esc_url( nadlan_vt_admin_url() ) . '">לכל הביקורים</a>'; }
		$h .= '</form>';
		if ( ! $rows ) { return $h . '<p>אין ביקורים להצגה.</p></div>'; }
		$evs   = nadlan_vt_events_of( wp_list_pluck( $rows, 'vid' ) );
		$langs = nadlan_vt_langs();
		$devs  = array( 'm' => 'טלפון', 't' => 'טאבלט', 'd' => 'מחשב' );
		$h .= '<table class="widefat striped"><thead><tr><th>מתי</th><th>פרויקט</th><th>מה עשה</th><th>פנייה</th><th>מאיפה</th><th></th></tr></thead><tbody>';
		foreach ( $rows as $r ) {
			$lines = nadlan_vt_lines( $evs[ $r->vid ] ?? array() );
			$f = strtotime( $r->first_at . ' UTC' );
			$l = strtotime( $r->last_at . ' UTC' );
			$mins = max( 0, (int) round( ( $l - $f ) / 60 ) );
			$lead = '';
			if ( (int) $r->lead_id > 0 && get_post( (int) $r->lead_id ) ) {
				$nm   = (string) get_post_meta( (int) $r->lead_id, 'name', true );
				$lead = '<a href="' . esc_url( get_edit_post_link( (int) $r->lead_id, 'url' ) ) . '"><b>' . esc_html( $nm ?: get_the_title( (int) $r->lead_id ) ) . '</b></a>';
			}
			$picks = array();
			foreach ( $lines as $ln ) { if ( in_array( $ln['ev'], array( 'facing', 'tour', 'example', 'ftour', 'fcta', 'click', 'form', 'act' ), true ) ) { $picks[] = $ln['text']; } }
			$picks = array_slice( array_values( array_unique( $picks ) ), 0, 3 );
			$h .= '<tr><td>' . esc_html( wp_date( 'd/m H:i', $l ) ) . '<br><small>' . esc_html( $mins . ' דק׳, ' . (int) $r->pages . ' עמודים' ) . '</small></td>';
			$h .= '<td>' . esc_html( nadlan_vt_title( $r->entry ) ?: '-' ) . '<br><small>' . esc_html( trim( ( $langs[ $r->lang ] ?? '' ) . ' · ' . ( $devs[ $r->dev ] ?? '' ), ' ·' ) ) . '</small></td>';
			$h .= '<td>' . ( $picks ? esc_html( implode( ' · ', $picks ) ) : '<small>' . esc_html( count( $lines ) . ' רישומים' ) . '</small>' );
			$h .= '<details' . ( $vid ? ' open' : '' ) . '><summary>המסלול המלא (' . count( $lines ) . ')</summary><ol>';
			foreach ( $lines as $ln ) { $h .= '<li class="k-' . esc_attr( $ln['ev'] ) . '"><span class="t">' . esc_html( $ln['time'] ) . '</span>' . esc_html( $ln['text'] ) . '</li>'; }
			$h .= '</ol></details></td>';
			$h .= '<td>' . ( $lead ?: '<small>-</small>' ) . '</td>';
			$h .= '<td><small>' . esc_html( trim( ( $r->country ?: '' ) . ( $r->ref ? ' · ' . $r->ref : '' ), ' ·' ) ?: '-' ) . '</small></td>';
			$h .= '<td><form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '" onsubmit="return confirm(\'למחוק את הביקור הזה לצמיתות?\')">'
				. '<input type="hidden" name="action" value="nadlan_vt_delete"><input type="hidden" name="vid" value="' . esc_attr( $r->vid ) . '">'
				. wp_nonce_field( 'nadlan_vt_delete_' . $r->vid, '_wpnonce', true, false ) . '<button class="button-link" style="color:#b32d2e">מחיקה</button></form></td></tr>';
		}
		$h .= '</tbody></table>';
		$pagesN = (int) ceil( $total / $per );
		if ( $pagesN > 1 ) {
			$h .= '<p>';
			for ( $i = 1; $i <= min( $pagesN, 40 ); $i++ ) {
				$u = nadlan_vt_admin_url( array_filter( array( 'leads' => ! empty( $a['leads'] ) ? 1 : 0, 'project' => $proj, 'paged' => $i ) ) );
				$h .= $i === $paged ? '<b>' . $i . '</b> ' : '<a href="' . esc_url( $u ) . '">' . $i . '</a> ';
			}
			$h .= '</p>';
		}
		return $h . '</div>';
	}

	function nadlan_vt_delete_visit( $vid ) {
		global $wpdb;
		if ( ! preg_match( '/^[A-Za-z0-9_-]{16,32}$/', (string) $vid ) || ! nadlan_vt_tables_exist() ) { return false; }
		$t = nadlan_vt_tables();
		$wpdb->delete( $t['e'], array( 'vid' => $vid ), array( '%s' ) );
		$wpdb->delete( $t['v'], array( 'vid' => $vid ), array( '%s' ) );
		delete_metadata( 'post', 0, '_nl_visit', $vid, true ); // the lead keeps its own text; only the link to the deleted visit goes
		return true;
	}

	/** the daily clean-up: rows older than the retention (12 months) */
	function nadlan_vt_prune() {
		global $wpdb;
		if ( ! nadlan_vt_tables_exist() ) { return 0; }
		$t   = nadlan_vt_tables();
		$lim = nadlan_vt_limits();
		$cut = gmdate( 'Y-m-d H:i:s', time() - max( 30, (int) $lim['keep_days'] ) * DAY_IN_SECONDS );
		$n   = 0;
		for ( $i = 0; $i < 20; $i++ ) {
			$k = (int) $wpdb->query( $wpdb->prepare( "DELETE FROM {$t['e']} WHERE at < %s LIMIT 20000", $cut ) ); // phpcs:ignore
			$n += $k;
			if ( $k < 20000 ) { break; }
		}
		$n += (int) $wpdb->query( $wpdb->prepare( "DELETE FROM {$t['v']} WHERE last_at < %s", $cut ) ); // phpcs:ignore
		return $n;
	}

	/** for the release's bridge (read only, except the one-time table creation the module does anyway): proves the module works on the live PHP */
	function nadlan_vt_selftest() {
		$ok_db = nadlan_vt_ready();
		$now   = time();
		$smp   = nadlan_vt_clean_batch( array( 'v' => 1, 'vid' => 'selftestselftest00', 'pv' => 'selftest01', 'page' => 1, 'lang' => 'he', 'dev' => 'm', 'now' => $now * 1000,
			'ev' => array( array( 't' => 'floor', 'at' => $now * 1000, 'f' => 23 ), array( 't' => 'facing', 'f' => 23, 'b' => 268, 'u' => '23-w' ), array( 't' => 'click', 'k' => 'wa', 'l' => 'ייעוץ חינם', 'w' => 'bar' ),
				array( 't' => 'nope' ), array( 't' => 'form', 'k' => 'lead', 'id' => 'x', 'name' => 'ignored', 'phone' => '0500000000' ) ) ), $now );
		$html = '';
		if ( current_user_can( 'manage_options' ) ) { $html = nadlan_vt_admin_html( array() ); }
		return array(
			'version' => NADLAN_VT_VERSION, 'db' => $ok_db ? 1 : 0, 'tables' => nadlan_vt_tables_exist( true ) ? 1 : 0,
			'clean' => is_wp_error( $smp ) ? $smp->get_error_code() : count( $smp['ev'] ),
			'no_phone' => ( ! is_wp_error( $smp ) && false === strpos( wp_json_encode( $smp ), '0500000000' ) ) ? 1 : 0,
			'line' => is_wp_error( $smp ) ? '' : nadlan_vt_line( 'facing', $smp['ev'][1]['d'] ),
			'admin_bytes' => strlen( $html ), 'admin_title' => substr_count( $html, '<h1>מסלולי ביקור</h1>' ),
			'route' => (bool) ( function_exists( 'rest_get_server' ) && isset( rest_get_server()->get_routes()['/nadlan/v1/trail'] ) ),
			'lead_hook' => false !== has_action( 'wp_after_insert_post', 'nadlan_vt_after_insert' ),
			'on' => nadlan_vt_on(),
		);
	}

	function nadlan_vt_after_insert( $post_id, $post, $update ) {
		if ( $update || ! $post || 'nadlan_lead' !== ( $post->post_type ?? '' ) ) { return; }
		try {
			nadlan_vt_link_lead( (int) $post_id, nadlan_vt_request_vid() );
		} catch ( \Throwable $e ) { // a lead is never lost because of its trail
			if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) { error_log( 'nadlan visit-trail: ' . $e->getMessage() ); } // phpcs:ignore
		}
	}
}

/* ---------------------------------------------------------------- hooks */

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/trail', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nadlan_vt_rest' ) );
} );

/* the visit id a REST request carries (header or param), kept for the lead hook of the same request */
add_filter( 'rest_pre_dispatch', function ( $result, $server, $request ) {
	if ( 'POST' === strtoupper( (string) $request->get_method() ) && 0 === strpos( (string) $request->get_route(), '/nadlan/v1/' ) ) {
		$v = $request->get_header( 'x_nl_visit' );
		if ( ! $v ) { $v = $request->get_param( 'nl_visit' ); }
		if ( is_string( $v ) && '' !== $v ) { $GLOBALS['nadlan_vt_rest_vid'] = $v; }
	}
	return $result;
}, 1, 3 );

add_action( 'wp_after_insert_post', 'nadlan_vt_after_insert', 5, 3 );

add_action( 'admin_init', function () { if ( current_user_can( 'manage_options' ) ) { nadlan_vt_install(); } } );

add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'nadlan_vt_prune' ) ) { wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nadlan_vt_prune' ); }
} );
add_action( 'nadlan_vt_prune', 'nadlan_vt_prune' );

/* the script. 1.0.0 loaded it on project stage pages only; 1.1.0 loads it on every front page: 'full' on a project page (a stage
   page, the engine's showroom page, any published project and its language pages), 'lite' everywhere else (the tools' events) */
function nadlan_vt_page_cfg() {
	$lang = function_exists( 'nadlan_ps_current' ) && ( $ps = nadlan_ps_current() ) && ! empty( $ps['lang'] ) ? (string) $ps['lang'] : '';
	if ( '' === $lang ) {
		$hl   = strtolower( substr( (string) get_bloginfo( 'language' ), 0, 2 ) );
		$lang = in_array( $hl, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $hl : 'he';
	}
	$qid = (int) get_queried_object_id();
	if ( is_singular( 'nadlan_project' ) && $qid > 0 ) {
		$slug = (string) get_post_field( 'post_name', $qid );
		if ( preg_match( '/-(en|fr|ru|ar)$/', $slug, $m ) ) { $lang = $m[1]; }
		$proj = nadlan_vt_canon_project( $qid );
		if ( $proj > 0 ) { return array( 'mode' => 'full', 'page' => $qid, 'proj' => $proj, 'lang' => $lang ); }
	}
	$cfg = array( 'mode' => 'lite', 'page' => is_singular() && $qid > 0 ? $qid : 0, 'proj' => 0, 'lang' => $lang );
	if ( function_exists( 'nadlan_ol_watch_path' ) && '' !== nadlan_ol_watch_path( (string) wp_parse_url( (string) ( $_SERVER['REQUEST_URI'] ?? '' ), PHP_URL_PATH ) ) ) { $cfg['watch'] = 1; } // phpcs:ignore -- compared only
	return $cfg;
}

/** for a page printed outside the theme (the designer at /tour/designer/ prints its own HTML): the same two tags, ready to echo
 *  in its <head>. $a: proj (a project id or slug the page belongs to), lang. Logged-in team members get only the no-op stub. */
function nadlan_vt_tags( $a = array() ) {
	if ( ! nadlan_vt_on() ) { return '<script>window.nlTrack=window.nlTrack||function(){};</script>'; }
	if ( is_user_logged_in() && current_user_can( 'edit_posts' ) && ! isset( $_GET['nlvt'] ) ) { return '<script>window.nlTrack=window.nlTrack||function(){};</script>'; } // phpcs:ignore
	$proj = isset( $a['proj'] ) ? nadlan_vt_project_ref( $a['proj'] ) : 0;
	$lang = isset( $a['lang'] ) && in_array( $a['lang'], array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $a['lang'] : 'he';
	$cfg  = array( 'endpoint' => esc_url_raw( rest_url( 'nadlan/v1/trail' ) ), 'mode' => 'lite', 'page' => 0, 'proj' => $proj, 'lang' => $lang );
	$ver  = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : NADLAN_VT_VERSION;
	return '<script>window.NL_TRAIL_CFG=' . wp_json_encode( $cfg, JSON_UNESCAPED_SLASHES ) . ';window.nlTrack=window.nlTrack||function(){(window.nlTrackQ=window.nlTrackQ||[]).push([arguments[0],arguments[1],Date.now()])};</script>'
		. '<script defer src="' . esc_url( add_query_arg( 'ver', $ver, plugins_url( 'assets/visit-trail/trail.js', dirname( __FILE__ ) ) ) ) . '"></script>';
}

add_action( 'wp_enqueue_scripts', function () {
	if ( is_admin() || ! nadlan_vt_on() || is_feed() || is_404() ) { return; }
	if ( is_user_logged_in() && current_user_can( 'edit_posts' ) && ! isset( $_GET['nlvt'] ) ) { // phpcs:ignore -- the team's own visits stay out
		wp_register_script( 'nadlan-visit-trail-stub', false, array(), NADLAN_VT_VERSION, array( 'in_footer' => false ) );
		wp_enqueue_script( 'nadlan-visit-trail-stub' );
		wp_add_inline_script( 'nadlan-visit-trail-stub', 'window.nlTrack=window.nlTrack||function(){};' ); // the tools may call it; nothing is recorded
		return;
	}
	$ver = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : NADLAN_VT_VERSION;
	$pc  = nadlan_vt_page_cfg();
	$cfg = array_merge( array( 'endpoint' => esc_url_raw( rest_url( 'nadlan/v1/trail' ) ) ), $pc );
	// the queue: a tool that calls window.nlTrack before trail.js ran is kept (trail.js empties window.nlTrackQ)
	wp_register_script( 'nadlan-visit-trail-stub', false, array(), NADLAN_VT_VERSION, array( 'in_footer' => false ) );
	wp_enqueue_script( 'nadlan-visit-trail-stub' );
	wp_add_inline_script( 'nadlan-visit-trail-stub', 'window.NL_TRAIL_CFG=' . wp_json_encode( $cfg, JSON_UNESCAPED_SLASHES ) . ';window.nlTrack=window.nlTrack||function(){(window.nlTrackQ=window.nlTrackQ||[]).push([arguments[0],arguments[1],Date.now()])};' );
	wp_enqueue_script( 'nadlan-visit-trail', plugins_url( 'assets/visit-trail/trail.js', dirname( __FILE__ ) ), array(), $ver, array( 'in_footer' => true, 'strategy' => 'defer' ) );
}, 30 );

/* the admin screen, under Lead Inbox (inc/lead-inbox.php) */
add_action( 'admin_menu', function () {
	add_submenu_page( 'nadlan-inbox', 'מסלולי ביקור', 'מסלולי ביקור', 'manage_options', 'nadlan-visit-trails', function () {
		if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'אין הרשאה.' ); }
		echo nadlan_vt_admin_html( array( // phpcs:ignore -- escaped inside
			'leads' => ! empty( $_GET['leads'] ), 'vid' => sanitize_text_field( wp_unslash( $_GET['vid'] ?? '' ) ), // phpcs:ignore
			'project' => absint( $_GET['project'] ?? 0 ), 'paged' => absint( $_GET['paged'] ?? 1 ), // phpcs:ignore
		) );
		if ( isset( $_GET['deleted'] ) ) { echo '<div class="notice notice-success"><p>הביקור נמחק.</p></div>'; } // phpcs:ignore
	} );
}, 30 );

add_action( 'admin_post_nadlan_vt_delete', function () {
	$vid = sanitize_text_field( wp_unslash( $_POST['vid'] ?? '' ) ); // phpcs:ignore -- nonce below
	if ( ! current_user_can( 'manage_options' ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['_wpnonce'] ?? '' ) ), 'nadlan_vt_delete_' . $vid ) ) { wp_die( 'אין הרשאה.' ); }
	nadlan_vt_delete_visit( $vid );
	wp_safe_redirect( nadlan_vt_admin_url( array( 'deleted' => 1 ) ) );
	exit;
} );

/* the lead's own screen: its visit */
add_action( 'add_meta_boxes_nadlan_lead', function () {
	add_meta_box( 'nadlan-vt-lead', 'מסלול הביקור', function ( $p ) {
		$vid = (string) get_post_meta( $p->ID, '_nl_visit', true );
		if ( '' === $vid ) { echo '<p>לפנייה הזו אין מסלול ביקור (היא לא נשלחה מעמוד פרויקט, או שהדפדפן ביקש לא לתעד).</p>'; return; }
		$ev = nadlan_vt_events_of( array( $vid ) );
		$ln = nadlan_vt_lines( $ev[ $vid ] ?? array(), 'd/m H:i' );
		if ( ! $ln ) { echo '<p>המסלול עוד לא הגיע או נמחק.</p>'; return; }
		echo '<ol dir="rtl" style="margin:0 20px 0 0">';
		foreach ( array_slice( $ln, -60 ) as $l ) { echo '<li><span style="color:#646970;margin-left:8px">' . esc_html( $l['time'] ) . '</span>' . esc_html( $l['text'] ) . '</li>'; }
		echo '</ol><p><a href="' . esc_url( nadlan_vt_admin_url( array( 'vid' => $vid ) ) ) . '">כל המסלול</a></p>';
	}, null, 'normal', 'high' );
} );

/* the leads list: a column with the visit */
add_filter( 'manage_nadlan_lead_posts_columns', function ( $c ) { $c['nlvt'] = 'מסלול'; return $c; }, 30 );
add_action( 'manage_nadlan_lead_posts_custom_column', function ( $col, $id ) {
	if ( 'nlvt' !== $col ) { return; }
	$vid = (string) get_post_meta( $id, '_nl_visit', true );
	echo '' === $vid ? '-' : '<a href="' . esc_url( nadlan_vt_admin_url( array( 'vid' => $vid ) ) ) . '">מה עשה בעמוד</a>';
}, 30, 2 );

/* the rich new-lead email (inc/alerts.php, the action nadlan_lead_rich_alert): the visit's timeline is appended */
add_action( 'nadlan_lead_rich_alert', function ( $lead_id ) { $GLOBALS['nadlan_vt_alert'] = (int) $lead_id; }, 1 );
add_action( 'nadlan_lead_rich_alert', function () { unset( $GLOBALS['nadlan_vt_alert'] ); }, 99 );
add_filter( 'wp_mail', function ( $a ) {
	$lid = (int) ( $GLOBALS['nadlan_vt_alert'] ?? 0 );
	if ( $lid <= 0 || ! is_array( $a ) || false === strpos( (string) ( $a['subject'] ?? '' ), 'ליד חדש' ) || ! is_string( $a['message'] ?? null ) ) { return $a; }
	unset( $GLOBALS['nadlan_vt_alert'] ); // once
	try {
		$lines = nadlan_vt_lead_lines( $lid, 25 );
	} catch ( \Throwable $e ) {
		return $a;
	}
	if ( ! $lines ) { return $a; }
	$vid   = (string) get_post_meta( $lid, '_nl_visit', true );
	$block = "\nמה עשה בעמוד הפרויקט לפני הפנייה:\n" . implode( "\n", $lines ) . "\nהמסלול המלא: " . nadlan_vt_admin_url( array( 'vid' => $vid ) ) . "\n";
	$cut   = strpos( $a['message'], "\n\n-- nad-lan.co.il " );
	$a['message'] = false === $cut ? $a['message'] . "\n" . $block : substr( $a['message'], 0, $cut ) . "\n" . $block . substr( $a['message'], $cut );
	return $a;
}, 20 );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['visit_trail'] = array( 'version' => NADLAN_VT_VERSION, 'on' => nadlan_vt_on(), 'db' => (string) get_option( 'nadlan_vt_db', '' ) );
	return $out;
} );

/* 1.1.0: the developer report (a funnel per project, a signed link, CSV) */
if ( is_readable( __DIR__ . '/dev-report.php' ) ) { require_once __DIR__ . '/dev-report.php'; }
if ( is_readable( __DIR__ . '/owner-live.php' ) ) { require_once __DIR__ . '/owner-live.php'; }
