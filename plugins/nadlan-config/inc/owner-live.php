<?php
/**
 * OwnerLive 1.0.0 (HAD-791 follow-up; Ben 22.11.2026: "I want an instant alert: someone wrote in the forum, someone pressed something
 * in a project, someone looked at the developers page, someone checked the plans, someone tried to sign up ... but do not load the
 * site and do not hurt SEO"). Loaded from inc/visit-trail.php. Design board: https://claude.ai/artifact/7fdnJgxn8scFBeM63vyD9e
 *
 * Sources, all server side, no new script and no new request on a page:
 *  - the visit trail (nlTrack): every batch it stores is offered here (action nadlan_vt_stored). Alerts: a press inside a project
 *    page (stage, floors, apartment card, WhatsApp, phone, tour), plans and the apartment designer, the basket / RFP / reservation /
 *    video call, the rentals sign-up and new property (rent_*), and a visit to /developers/ or /marketing/ (the trail's lite mode
 *    sends one 'open' there; visit-trail.php keeps it).
 *  - the forum: every new discussion or answer (action nlf_post_created).
 *  - sign-up attempts, read from the REST response after it is built: forum code, pros and brokers join, site and owner sign-up,
 *    the basket order and the RFP (route names only; nothing is added to those routes).
 * Lead forms are NOT mailed here: owner-mail.php already sends the lead card at once.
 *
 * Delivery: one mail per alert to the owner address (admin_email, the address that gets the lead cards), sent after the visitor's
 * response is finished (shutdown + fastcgi_finish_request). The same visitor + the same kind + the same page at most once in 10
 * minutes; at most 40 mails an hour (the rest only on the live screen). Every alert is also written to a small log (option
 * nadlan_ol_log, 300 lines, not autoloaded) that the private live screen shows: a signed link (HMAC, like the developer report),
 * newest first, one strip per visit. Team members signed in and robots are never counted (the trail already drops them).
 * No new personal data: the visit record the trail already keeps, plus only what a visitor typed (a name, a forum post).
 * The host sends no city header today; a city appears only if one of the known headers arrives.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ol_on' ) ) {

	define( 'NADLAN_OL_VERSION', '1.0.1' );

	function nadlan_ol_on() { return '0' !== (string) get_option( 'nadlan_ol_on', '1' ); }
	function nadlan_ol_mail_on() { return '0' !== (string) get_option( 'nadlan_ol_mail', '1' ); }

	function nadlan_ol_kinds() {
		return array(
			'project' => 'לחיצה בפרויקט',
			'plans'   => 'תוכניות ומעצב הדירה',
			'basket'  => 'סל, הצעה ושיחה',
			'rent'    => 'השכרות נדל״ן',
			'page'    => 'עמוד היזמים והשיווק',
			'signup'  => 'הרשמה',
			'forum'   => 'פורום',
		);
	}

	/* ---------------------------------------------------------------- what counts */

	/** the alert kind of one stored trail event, or '' ($full: the batch came from a project page) */
	function nadlan_ol_kind( $ev, $d, $full ) {
		$d = is_array( $d ) ? $d : array();
		$n = (string) ( $d['n'] ?? '' );
		if ( 'open' === $ev ) { return $full ? '' : 'page'; }
		if ( 'act' === $ev ) {
			if ( preg_match( '/^rent_(signup|property_add|lease_add|tenant_invite)$/', $n ) ) { return 'rent'; }
			if ( preg_match( '/^(basket|rfp|offer|reserve|cart)_/', $n ) || 'call_start' === $n ) { return 'basket'; }
			if ( preg_match( '/^(designer|design|plan|plans)_/', $n ) ) { return 'plans'; }
			if ( $full && ! preg_match( '/^(mortgage|lang|price_alert|nudge|est_)/', $n ) ) { return 'project'; }
			return '';
		}
		if ( ! $full ) { return ''; }
		if ( in_array( $ev, array( 'leave', 'scroll', 'vis', 'ping', 'err', 'perf' ), true ) ) { return ''; }
		if ( isset( $d['src'] ) && 'user' !== (string) $d['src'] ) { return ''; } // moved by the page itself, not a press
		return 'project';
	}

	/** /developers/ or /marketing/ (any language prefix): 'developers' | 'marketing' | '' */
	function nadlan_ol_watch_path( $path ) {
		$path = strtolower( (string) $path );
		return preg_match( '#^/(?:(?:en|fr|ru|ar)/)?(developers|marketing)(?:/|$)#', $path, $m ) ? $m[1] : '';
	}

	function nadlan_ol_src( $ref ) {
		$ref = strtolower( (string) $ref );
		if ( '' === $ref ) { return 'כניסה ישירה'; }
		$map = array( 'google' => 'גוגל', 'bing' => 'בינג', 'facebook' => 'פייסבוק', 'fb.' => 'פייסבוק', 'instagram' => 'אינסטגרם', 'whatsapp' => 'וואטסאפ',
			'wa.me' => 'וואטסאפ', 'linkedin' => 'לינקדאין', 't.co' => 'X', 'twitter' => 'X', 'youtube' => 'יוטיוב', 'tiktok' => 'טיקטוק',
			'chatgpt' => 'ChatGPT', 'openai' => 'ChatGPT', 'perplexity' => 'Perplexity', 'gemini' => 'Gemini', 'nad-lan.co.il' => 'מתוך האתר', 'mail' => 'מייל' );
		foreach ( $map as $k => $v ) { if ( false !== strpos( $ref, $k ) ) { return $v; } }
		return $ref;
	}
	function nadlan_ol_dev( $d ) { return array( 'm' => 'טלפון', 't' => 'טאבלט', 'd' => 'מחשב' )[ (string) $d ] ?? ''; }
	function nadlan_ol_lang( $l ) { return array( 'he' => 'עברית', 'en' => 'אנגלית', 'fr' => 'צרפתית', 'ru' => 'רוסית', 'ar' => 'ערבית' )[ (string) $l ] ?? ''; }
	function nadlan_ol_city() {
		foreach ( array( 'HTTP_CF_IPCITY', 'HTTP_X_CITY', 'HTTP_X_GEO_CITY', 'HTTP_X_UPRESS_CITY', 'GEOIP_CITY' ) as $k ) {
			if ( ! empty( $_SERVER[ $k ] ) ) { return mb_substr( sanitize_text_field( wp_unslash( $_SERVER[ $k ] ) ), 0, 40 ); } // phpcs:ignore
		}
		return '';
	}
	function nadlan_ol_title( $id ) {
		return $id > 0 ? trim( wp_strip_all_tags( html_entity_decode( (string) get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ) ) : '';
	}
	function nadlan_ol_team() { return is_user_logged_in() && current_user_can( 'edit_posts' ); }

	/* ---------------------------------------------------------------- collect (cheap, during the request) */

	function nadlan_ol_add( $a ) {
		if ( ! nadlan_ol_on() ) { return; }
		$GLOBALS['nadlan_ol_q'][] = $a;
		if ( empty( $GLOBALS['nadlan_ol_hooked'] ) ) {
			$GLOBALS['nadlan_ol_hooked'] = 1;
			add_action( 'shutdown', 'nadlan_ol_flush', 1000 );
		}
	}

	/** the trail stored a batch: one alert per kind and page in it (the first event of that kind names it) */
	add_action( 'nadlan_vt_stored', function ( $b, $watch = '' ) {
		if ( ! nadlan_ol_on() || empty( $b['ev'] ) ) { return; }
		$full = 'full' === ( $b['mode'] ?? '' );
		$seen = array();
		foreach ( $b['ev'] as $e ) {
			$k = nadlan_ol_kind( $e['t'], $e['d'] ?? array(), $full );
			if ( '' === $k || ( 'page' === $k && '' === $watch ) ) { continue; }
			$proj = (int) ( $e['proj'] ?? 0 );
			$key  = $k . '|' . ( $proj ? $proj : (int) $b['page'] );
			if ( isset( $seen[ $key ] ) ) { $seen[ $key ]['more']++; continue; }
			$seen[ $key ] = array( 'src' => 'trail', 'k' => $k, 'vid' => (string) $b['vid'], 'page' => (int) $b['page'], 'proj' => $proj, 'watch' => $watch,
				'lang' => (string) $b['lang'], 'dev' => (string) $b['dev'], 'ref' => (string) $b['ref'], 'ev' => (string) $e['t'], 'd' => $e['d'] ?? array(),
				'ts' => (int) $e['ts'], 'more' => 0 );
		}
		foreach ( $seen as $a ) { nadlan_ol_add( $a ); }
	}, 10, 2 );

	/** the forum: a new discussion or answer (live or waiting for approval) */
	add_action( 'nlf_post_created', function ( $type, $id, $m, $q, $status = '', $topic_id = 0 ) {
		if ( nadlan_ol_team() || ! in_array( $type, array( 'topic', 'reply' ), true ) ) { return; }
		if ( apply_filters( 'nadlan_ol_forum_skip', false, $type, (int) $id, (int) $topic_id ) ) { return; }
		$title = '';
		if ( 'topic' === $type && is_object( $q ) && method_exists( $q, 'get_param' ) ) { $title = (string) $q->get_param( 'title' ); }
		elseif ( function_exists( 'nlf_t' ) && $topic_id ) { global $wpdb; $title = (string) $wpdb->get_var( $wpdb->prepare( 'SELECT title FROM ' . nlf_t( 'topics' ) . ' WHERE id = %d', (int) $topic_id ) ); }
		$body = is_object( $q ) && method_exists( $q, 'get_param' ) ? (string) $q->get_param( 'body' ) : '';
		nadlan_ol_add( array( 'src' => 'forum', 'k' => 'forum', 'vid' => 'f' . (int) ( $m['id'] ?? 0 ), 'type' => $type, 'status' => (string) $status,
			'title' => mb_substr( wp_strip_all_tags( $title ), 0, 120 ), 'body' => mb_substr( trim( preg_replace( '/\s+/u', ' ', wp_strip_all_tags( $body ) ) ), 0, 220 ),
			'name' => mb_substr( (string) ( $m['display_name'] ?? '' ), 0, 40 ), 'url' => home_url( '/forum/' . (int) ( $topic_id ? $topic_id : $id ) . '/' ), 'ts' => time() ) );
	}, 20, 6 );

	/** sign-up attempts and basket orders, read from the finished REST response (any outcome) */
	function nadlan_ol_routes() {
		return array(
			'#^/nadlan/v1/forum/code$#'            => array( 'signup', 'ביקש קוד כניסה לפורום' ),
			'#^/nadlan/v1/pros/join$#'             => array( 'signup', 'ביקש להצטרף כבעל מקצוע' ),
			'#^/nadlan/v1/brokers/join$#'          => array( 'signup', 'ביקש להצטרף כמתווך' ),
			'#^/nadlan/v1/auth-signup$#'           => array( 'signup', 'נרשם לאתר' ),
			'#^/nadlan/v1/quick-register$#'        => array( 'signup', 'נרשם בהרשמה מהירה' ),
			'#^/nadlan/v1/owner/account/signup$#'  => array( 'signup', 'בעל דירה נרשם' ),
			'#^/nadlan/v1/cart/order$#'            => array( 'basket', 'שלח את הסל' ),
			'#^/nadlan/v1/rfp$#'                   => array( 'basket', 'שלח בקשה להצעת מחיר' ),
		);
	}
	add_filter( 'rest_post_dispatch', function ( $res, $server, $req ) {
		if ( ! nadlan_ol_on() || 'POST' !== $req->get_method() || nadlan_ol_team() ) { return $res; }
		$route = (string) $req->get_route();
		if ( 0 !== strpos( $route, '/nadlan/v1/' ) ) { return $res; }
		foreach ( nadlan_ol_routes() as $re => $def ) {
			if ( ! preg_match( $re, $route ) ) { continue; }
			if ( function_exists( 'nadlan_vt_robot_ua' ) && nadlan_vt_robot_ua( $req->get_header( 'user_agent' ) ) ) { break; }
			$code = $res instanceof WP_HTTP_Response ? (int) $res->get_status() : 200;
			$vid  = function_exists( 'nadlan_vt_request_vid' ) ? (string) nadlan_vt_request_vid() : '';
			if ( '' === $vid ) { $vid = 'c' . substr( md5( function_exists( 'nadlan_vt_client' ) ? nadlan_vt_client() : '' ), 0, 14 ); }
			$name = '';
			foreach ( array( 'name', 'display_name', 'full_name' ) as $p ) { if ( is_string( $req->get_param( $p ) ) && '' !== trim( $req->get_param( $p ) ) ) { $name = mb_substr( sanitize_text_field( $req->get_param( $p ) ), 0, 40 ); break; } }
			nadlan_ol_add( array( 'src' => 'route', 'k' => $def[0], 'vid' => $vid, 'what' => $def[1] . ( $code >= 400 ? ' (לא הושלם)' : '' ),
				'name' => $name, 'url' => (string) wp_get_referer(), 'ts' => time() ) );
			break;
		}
		return $res;
	}, 99, 3 );

	/* ---------------------------------------------------------------- deliver (after the response) */

	function nadlan_ol_flush() {
		$q = isset( $GLOBALS['nadlan_ol_q'] ) ? (array) $GLOBALS['nadlan_ol_q'] : array();
		$GLOBALS['nadlan_ol_q'] = array();
		if ( ! $q ) { return; }
		if ( function_exists( 'fastcgi_finish_request' ) ) { @fastcgi_finish_request(); } // phpcs:ignore -- the visitor is answered first
		$log = get_option( 'nadlan_ol_log', array() );
		$log = is_array( $log ) ? $log : array();
		foreach ( $q as $a ) {
			$x = nadlan_ol_describe( $a );
			$x['mailed'] = nadlan_ol_should_mail( $a ) ? ( nadlan_ol_mail( $a, $x ) ? 1 : 3 ) : 2;
			$log[] = $x;
		}
		$log = array_slice( $log, -300 );
		update_option( 'nadlan_ol_log', $log, false );
	}

	/** 1 = mail, else: 10 minutes for this visitor + kind + page, 40 an hour, the switch */
	function nadlan_ol_should_mail( $a ) {
		if ( ! nadlan_ol_mail_on() ) { return false; }
		$key = 'nadlan_ol_t_' . md5( $a['vid'] . '|' . $a['k'] . '|' . ( $a['proj'] ?? 0 ) . '|' . ( $a['page'] ?? 0 ) . '|' . ( $a['url'] ?? '' ) . '|' . ( $a['what'] ?? '' ) );
		if ( 'forum' !== $a['k'] && get_transient( $key ) ) { return false; }
		$hk = 'nadlan_ol_h_' . gmdate( 'YmdH' );
		$h  = (int) get_transient( $hk );
		if ( $h >= 40 ) { return false; }
		set_transient( $key, 1, 10 * MINUTE_IN_SECONDS );
		set_transient( $hk, $h + 1, HOUR_IN_SECONDS + 300 );
		return true;
	}

	/** the plain facts of an alert, for the mail and the live screen */
	function nadlan_ol_describe( $a ) {
		$x = array( 't' => (int) ( $a['ts'] ?? time() ), 'k' => (string) $a['k'], 'v' => substr( md5( (string) $a['vid'] ), 0, 8 ), 'name' => '', 'url' => '',
			'what' => '', 'meta' => '', 'note' => '' );
		if ( 'trail' === $a['src'] ) {
			$id = $a['proj'] > 0 ? (int) $a['proj'] : (int) $a['page'];
			$x['name'] = nadlan_ol_title( $id );
			if ( '' === $x['name'] && 'developers' === $a['watch'] ) { $x['name'] = 'עמוד היזמים'; }
			if ( '' === $x['name'] && 'marketing' === $a['watch'] ) { $x['name'] = 'עמוד השיווק'; }
			if ( '' === $x['name'] ) { $x['name'] = 'האתר'; }
			$pg = (int) $a['page'] > 0 ? (int) $a['page'] : $id;
			$x['url'] = $pg > 0 ? (string) get_permalink( $pg ) : ( $a['watch'] ? home_url( '/' . $a['watch'] . '/' ) : home_url( '/' ) );
			$x['what'] = 'open' === $a['ev'] ? 'נכנס לעמוד' : ( function_exists( 'nadlan_vt_line' ) ? (string) nadlan_vt_line( $a['ev'], $a['d'], $a['page'], $a['lang'] ) : $a['ev'] );
			if ( $a['more'] > 0 ) { $x['what'] .= ' (ועוד ' . (int) $a['more'] . ')'; }
			$sw = nadlan_ol_src( $a['ref'] );
			$x['from'] = 'כניסה ישירה' === $sw ? 'נכנס ישירות' : ( 'מתוך האתר' === $sw ? 'הגיע מתוך האתר' : 'הגיע מ' . $sw );
			$x['meta'] = implode( ' · ', array_filter( array( nadlan_ol_dev( $a['dev'] ), nadlan_ol_lang( $a['lang'] ), $x['from'], nadlan_ol_city() ) ) );
			$x['vid'] = (string) $a['vid'];
		} elseif ( 'forum' === $a['src'] ) {
			$x['name'] = 'הפורום' . ( '' !== $a['title'] ? ': ' . $a['title'] : '' );
			$x['url']  = (string) $a['url'];
			$x['what'] = ( 'topic' === $a['type'] ? 'דיון חדש' : 'תשובה חדשה' ) . ( '' !== $a['name'] ? ' מאת ' . $a['name'] : '' ) . ( 'live' !== $a['status'] ? ' (ממתין לאישור)' : '' );
			$x['note'] = (string) $a['body'];
		} else {
			$x['name'] = 'signup' === $a['k'] ? 'הרשמה' : 'הסל';
			$x['url']  = (string) $a['url'];
			$x['what'] = (string) $a['what'] . ( '' !== $a['name'] ? ': ' . $a['name'] : '' );
			$x['meta'] = nadlan_ol_city();
		}
		return $x;
	}

	function nadlan_ol_mail( $a, $x ) {
		if ( ! function_exists( 'nadlan_omx_send' ) || ! function_exists( 'nadlan_omx_doc' ) ) { return false; }
		$when  = wp_date( 'H:i', $x['t'] );
		$steps = '';
		if ( 'trail' === $a['src'] && function_exists( 'nadlan_vt_tables' ) && function_exists( 'nadlan_vt_lines' ) ) {
			global $wpdb; $t = nadlan_vt_tables();
			$rows = array_reverse( (array) $wpdb->get_results( $wpdb->prepare( "SELECT pv, at, page, lang, ev, d FROM {$t['e']} WHERE vid = %s ORDER BY id DESC LIMIT 10", $a['vid'] ) ) );
			foreach ( nadlan_vt_lines( $rows ) as $l ) {
				$steps .= '<div style="font-size:13px;line-height:20px"><span style="font-family:Consolas,monospace;color:#4A5866">' . esc_html( $l['time'] ) . '</span> · ' . esc_html( $l['text'] ) . '</div>';
			}
		}
		$subj = $x['name'] . ' · ' . $x['what'];
		if ( ! empty( $x['from'] ) ) { $subj = $x['name'] . ' · ' . $x['from'] . ' · ' . $x['what']; }
		$subj = mb_substr( trim( preg_replace( '/\s+/u', ' ', $subj ) ), 0, 150 );
		$rows = '<tr><td style="padding:0"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
			. '<td width="62" style="background:#D2352A;color:#FFFFFF;text-align:center;font-family:Consolas,monospace;font-size:15px;font-weight:700;padding:10px 4px">' . esc_html( $when ) . '</td>'
			. '<td style="padding:12px 14px"><div style="font-size:19px;line-height:25px;font-weight:700;color:#0D1B2A">' . esc_html( $x['name'] ) . '</div>'
			. ( '' !== $x['meta'] ? '<div style="font-size:13px;line-height:20px;color:#4A5866;margin-top:2px">' . esc_html( $x['meta'] ) . '</div>' : '' )
			. '<div style="font-size:16px;line-height:23px;color:#1E4FD6;font-weight:700;margin-top:6px">' . esc_html( $x['what'] ) . '</div>'
			. ( '' !== $x['note'] ? '<div style="font-size:14px;line-height:21px;color:#0D1B2A;margin-top:6px">' . esc_html( $x['note'] ) . '</div>' : '' )
			. '</td></tr></table></td></tr>';
		if ( '' !== $steps ) { $rows .= '<tr><td style="padding:4px 18px 10px;border-top:1px solid #E3E8EC"><div style="font-size:12px;color:#4A5866;margin:8px 0 4px">הביקור עד עכשיו</div>' . $steps . '</td></tr>'; }
		$rows .= '<tr><td style="padding:10px 18px 6px">' . ( '' !== $x['url'] ? nadlan_omx_btn( $x['url'], 'לעמוד', '#1E4FD6' ) : '' )
			. nadlan_omx_btn( nadlan_ol_url( time() + 30 * DAY_IN_SECONDS ), 'למסך החי', '#FFFFFF', '#0D1B2A', '#B8C4CF' ) . '</td></tr>';
		$foot = 'התראה על כל לחיצה משמעותית באתר; לאותו מבקר ולאותו סוג לכל היותר פעם ב־10 דקות, ועד 40 מיילים בשעה (השאר במסך החי). צוות מחובר ורובוטים לא נספרים.'
			. ' אין לנו שם או טלפון של מבקר שלא השאיר פרטים.';
		$text = $x['name'] . "\n" . $x['what'] . "\n" . $x['meta'] . "\n" . $x['note'] . "\n" . $x['url'];
		return nadlan_omx_send( $subj, nadlan_omx_doc( $x['what'], nadlan_omx_strip( 'נדל״ן · ביקור חי · ' . esc_html( $when ) ), $rows, $foot ), $text, 'live' );
	}

	/* ---------------------------------------------------------------- the live screen (signed link) */

	function nadlan_ol_sig( $x ) {
		return substr( hash_hmac( 'sha256', 'nlol|' . (int) $x . '|' . (int) get_option( 'nadlan_ol_rev', 0 ), wp_salt( 'auth' ) ), 0, 32 );
	}
	function nadlan_ol_url( $x ) { return add_query_arg( array( 'x' => (int) $x, 's' => nadlan_ol_sig( $x ) ), rest_url( 'nadlan/v1/owner-live' ) ); }
	function nadlan_ol_valid( $x, $s ) { return (int) $x > time() && is_string( $s ) && hash_equals( nadlan_ol_sig( $x ), $s ); }

	/** the log grouped into strips: one per visitor within 30 minutes, newest first */
	function nadlan_ol_strips( $log, $max = 60 ) {
		$out = array();
		$idx = array();
		foreach ( array_reverse( (array) $log ) as $e ) {
			$key = $e['v'];
			if ( isset( $idx[ $key ] ) && $out[ $idx[ $key ] ]['first'] - $e['t'] < 1800 ) {
				$i = $idx[ $key ];
				array_unshift( $out[ $i ]['steps'], $e );
				$out[ $i ]['first'] = $e['t'];
				continue;
			}
			if ( count( $out ) >= $max ) { break; }
			$idx[ $key ] = count( $out );
			$out[] = array( 'last' => $e['t'], 'first' => $e['t'], 'steps' => array( $e ) );
		}
		return $out;
	}

	function nadlan_ol_screen_html( $log ) {
		$now = time();
		$strips = nadlan_ol_strips( $log );
		$live = 0; $today = 0; $d0 = strtotime( wp_date( 'Y-m-d 00:00:00' ) . ' ' . wp_timezone_string() );
		foreach ( $strips as $s ) { if ( $now - $s['last'] < 120 ) { $live++; } if ( $s['last'] >= $d0 ) { $today++; } }
		$money = array( 'basket', 'signup', 'forum', 'rent' );
		$h = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="20">'
			. '<title>עכשיו באתר · נדל״ן</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Hebrew:wght@400;600;700&display=swap">'
			. '<style>*{box-sizing:border-box}body{margin:0;background:#F4F6F8;color:#0D1B2A;font-family:"IBM Plex Sans Hebrew",Arial,sans-serif}'
			. 'header{background:#0D1B2A;color:#F4F6F8;padding:20px 16px 14px}h1{margin:0;font-size:22px}.n{font-family:"IBM Plex Mono",monospace;font-size:20px;font-weight:600;color:#fff}'
			. '.sub{color:#CFDBF3;font-size:14px;display:flex;gap:18px;margin-top:8px}.chips{display:flex;gap:8px;flex-wrap:wrap;padding:12px 16px;border-bottom:1px solid #B8C4CF}'
			. '.chips button{min-height:44px;padding:0 16px;border-radius:22px;font:600 15px inherit;font-family:inherit;border:1px solid #B8C4CF;background:#fff;color:#0D1B2A}.chips button[aria-pressed=true]{background:#0D1B2A;color:#fff;border-color:#0D1B2A}'
			. 'main{padding:12px;display:flex;flex-direction:column;gap:8px;max-width:720px;margin:0 auto}.s{display:grid;grid-template-columns:62px minmax(0,1fr);background:#fff;border:1px solid #B8C4CF;border-radius:6px;overflow:hidden}'
			. '.c{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:6px 4px;font-size:11px;font-weight:600;text-align:center}.c b{font-family:"IBM Plex Mono",monospace;font-size:15px}'
			. '.live{background:#D2352A;color:#fff}.money{background:#0B7A6F;color:#fff}.gone{background:#CFDBF3;color:#0D1B2A}.b{padding:9px 12px;min-width:0}.t{display:flex;gap:8px;align-items:baseline}.t a{font-size:16px;font-weight:700;color:#0D1B2A;text-decoration:none;flex-grow:1}'
			. '.ago{font-family:"IBM Plex Mono",monospace;font-size:12px;color:#4A5866}.m{font-size:12px;color:#4A5866}.st{font-size:14px;line-height:21px}.st span{color:#1E4FD6;font-weight:600}.st span.k{color:#0B7A6F;font-weight:700}.note{font-size:13px;color:#2E3B48;margin-top:4px}'
			. 'footer{padding:16px;max-width:720px;margin:0 auto;font-size:13px;color:#4A5866}footer button{min-height:48px;padding:0 14px;border-radius:8px;border:1px solid #B8C4CF;background:#fff;font:600 14px inherit;font-family:inherit;color:#0D1B2A}</style></head><body>'
			. '<header><h1>עכשיו באתר</h1><div class="sub"><div><span class="n">' . (int) $live . '</span> חיים עכשיו</div><div><span class="n">' . (int) $today . '</span> ביקורים עם צעד היום</div><div>מתעדכן כל 20 שניות</div></div></header>'
			. '<div class="chips" role="group" aria-label="סינון"><button type="button" data-f="" aria-pressed="true">הכל</button><button type="button" data-f="project plans page">פרויקטים</button><button type="button" data-f="rent">השכרות</button><button type="button" data-f="basket signup">סל והרשמה</button><button type="button" data-f="forum">פורום</button></div><main>';
		if ( ! $strips ) { $h .= '<p>עדיין אין כאן ביקורים. כל לחיצה משמעותית באתר תופיע כאן ובמייל.</p>'; }
		foreach ( $strips as $s ) {
			$last  = $s['steps'][ count( $s['steps'] ) - 1 ];
			$kinds = array_unique( array_map( function ( $e ) { return $e['k']; }, $s['steps'] ) );
			$isMoney = (bool) array_intersect( $kinds, $money );
			$cls = $now - $s['last'] < 120 ? 'live' : ( $isMoney ? 'money' : 'gone' );
			$tag = 'live' === $cls ? 'חי' : ( $isMoney ? 'צעד חשוב' : 'יצא' );
			$ago = max( 0, (int) round( ( $now - $s['last'] ) / 60 ) );
			$steps = array();
			foreach ( $s['steps'] as $e ) { $steps[] = '<span class="' . ( in_array( $e['k'], $money, true ) ? 'k' : '' ) . '">' . esc_html( $e['what'] ) . '</span>'; }
			$h .= '<article class="s" data-k="' . esc_attr( implode( ' ', $kinds ) ) . '"><div class="c ' . $cls . '"><b>' . esc_html( wp_date( 'H:i', $s['first'] ) ) . '</b>' . esc_html( $tag ) . '</div><div class="b">'
				. '<div class="t"><a href="' . esc_url( $last['url'] ) . '" rel="noreferrer">' . esc_html( $last['name'] ) . '</a><span class="ago">' . ( $ago < 1 ? 'עכשיו' : 'לפני ' . $ago . ' דק׳' ) . '</span></div>'
				. ( '' !== $last['meta'] ? '<div class="m">' . esc_html( $last['meta'] ) . '</div>' : '' )
				. '<div class="st">' . implode( ' ← ', $steps ) . '</div>' . ( '' !== $last['note'] ? '<div class="note">' . esc_html( $last['note'] ) . '</div>' : '' ) . '</div></article>';
		}
		$h .= '</main><footer><button type="button" id="mine">זה הטלפון שלי: לא לספור את הביקורים שלי</button><p id="mine-s"></p>'
			. '<p>קישור פרטי. אפשר לבטל אותו מהניהול (לידים › התראות חיות). מייל על כל לחיצה, לאותו מבקר ולאותו סוג לכל היותר פעם ב־10 דקות.</p></footer>'
			. '<script>(function(){var bs=document.querySelectorAll(".chips button");for(var i=0;i<bs.length;i++){bs[i].onclick=function(){var f=this.getAttribute("data-f");for(var j=0;j<bs.length;j++){bs[j].setAttribute("aria-pressed",bs[j]===this?"true":"false")}'
			. 'var a=document.querySelectorAll("article.s");for(var k=0;k<a.length;k++){var ks=a[k].getAttribute("data-k").split(" ");a[k].style.display=!f||f.split(" ").some(function(x){return ks.indexOf(x)>-1})?"":"none"}}}'
			. 'var m=document.getElementById("mine"),s=document.getElementById("mine-s");function st(){var on=false;try{on=localStorage.getItem("nl_vt_off")==="1"}catch(e){}s.textContent=on?"הטלפון הזה מסומן: הביקורים ממנו לא נספרים ולא שולחים מייל.":""}'
			. 'm.onclick=function(){try{localStorage.setItem("nl_vt_off","1")}catch(e){}st()};st()})();</script></body></html>';
		return $h;
	}

	add_action( 'rest_api_init', function () {
		register_rest_route( 'nadlan/v1', '/owner-live', array( 'methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => function ( WP_REST_Request $r ) {
			$ok = nadlan_ol_valid( (int) $r->get_param( 'x' ), (string) $r->get_param( 's' ) ) || current_user_can( 'manage_options' );
			$send = function_exists( 'nadlan_dr_send' ) ? 'nadlan_dr_send' : null;
			if ( ! $ok ) {
				if ( $send ) { $send( '<!doctype html><meta charset="utf-8"><p dir="rtl">הקישור לא תקף או שפג תוקפו.</p>', 'text/html', 403 ); }
				return new WP_Error( 'nlol_no', 'Forbidden.', array( 'status' => 403 ) );
			}
			$html = nadlan_ol_screen_html( get_option( 'nadlan_ol_log', array() ) );
			if ( $send ) { $send( $html, 'text/html' ); }
			return new WP_REST_Response( array( 'html' => $html ), 200 );
		} ) );
	} );

	/* ---------------------------------------------------------------- admin: Lead Inbox › התראות חיות */

	add_action( 'admin_menu', function () {
		add_submenu_page( 'nadlan-inbox', 'התראות חיות', 'התראות חיות', 'manage_options', 'nadlan-owner-live', function () {
			if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'אין הרשאה.' ); }
			$link = nadlan_ol_url( time() + 90 * DAY_IN_SECONDS );
			$log  = array_reverse( array_slice( (array) get_option( 'nadlan_ol_log', array() ), -25 ) );
			$st   = array( 1 => 'נשלח מייל', 2 => 'בלי מייל (10 דקות / מכסה)', 3 => 'המייל נכשל' );
			echo '<div class="wrap" dir="rtl"><h1>התראות חיות לבעלים</h1><p>מייל על כל לחיצה משמעותית באתר, אל ' . esc_html( get_option( 'admin_email' ) ) . '. המסך החי בקישור פרטי (90 יום):</p>'
				. '<p><input type="text" readonly style="width:100%" value="' . esc_attr( $link ) . '"> <a class="button" href="' . esc_url( $link ) . '" target="_blank" rel="noreferrer">לפתוח</a></p>'
				. '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '">' . wp_nonce_field( 'nadlan_ol_save', '_wpnonce', true, false ) . '<input type="hidden" name="action" value="nadlan_ol_save">'
				. '<p><label><input type="checkbox" name="on" value="1"' . checked( nadlan_ol_on(), true, false ) . '> לאסוף התראות</label> &nbsp; <label><input type="checkbox" name="mail" value="1"' . checked( nadlan_ol_mail_on(), true, false ) . '> לשלוח מייל</label>'
				. ' &nbsp; <label><input type="checkbox" name="revoke" value="1"> לבטל את כל הקישורים למסך החי</label></p><p><button class="button button-primary">שמירה</button></p></form>'
				. '<h2>אחרונות</h2><table class="widefat striped"><tbody>';
			foreach ( $log as $e ) {
				echo '<tr><td>' . esc_html( wp_date( 'd.m H:i', $e['t'] ) ) . '</td><td>' . esc_html( $e['name'] ) . '</td><td>' . esc_html( $e['what'] ) . '</td><td>' . esc_html( $e['meta'] ) . '</td><td>' . esc_html( $st[ $e['mailed'] ] ?? '' ) . '</td></tr>';
			}
			echo '</tbody></table></div>';
		} );
	}, 30 );
	add_action( 'admin_post_nadlan_ol_save', function () {
		if ( ! current_user_can( 'manage_options' ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['_wpnonce'] ?? '' ) ), 'nadlan_ol_save' ) ) { wp_die( 'אין הרשאה.' ); }
		update_option( 'nadlan_ol_on', empty( $_POST['on'] ) ? '0' : '1', false );
		update_option( 'nadlan_ol_mail', empty( $_POST['mail'] ) ? '0' : '1', false );
		if ( ! empty( $_POST['revoke'] ) ) { update_option( 'nadlan_ol_rev', (int) get_option( 'nadlan_ol_rev', 0 ) + 1, false ); }
		wp_safe_redirect( admin_url( 'admin.php?page=nadlan-owner-live' ) );
		exit;
	} );

	add_filter( 'nadlan_config_healthcheck', function ( $out ) { $out['owner_live'] = array( 'version' => NADLAN_OL_VERSION, 'on' => nadlan_ol_on(), 'mail' => nadlan_ol_mail_on() ); return $out; } );
}
