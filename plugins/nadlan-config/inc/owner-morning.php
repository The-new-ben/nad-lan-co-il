<?php
/**
 * Owner mail, one useful email a day (Ben 22.10.2026: "I get lots of notices, about leads closed long ago ... make it efficient.
 * What does interest me: when people view properties I want alerts, and I don't get them"). Loaded from inc/alerts.php.
 *
 * 1. Property views that survive the page cache. The old counter (listings-ux.php) runs in PHP on template_redirect, which the
 *    cache skips, so almost nothing was counted. A small script on every property page reports, to /wp-json/nadlan/v1/pview:
 *    view (the page opened), read (15 seconds with the tab visible), wa / tel (a tap on WhatsApp or the phone), tour (a tap on
 *    the tour). Each visitor is a random id kept in the browser (no name, no IP stored). Logged-in visits (Ben, brokers) and
 *    bots are not counted. Demo listings (slug ending -demo) are not counted.
 * 2. Instant alerts only for hot signals, at most 6 a day: a tap on WhatsApp or the phone inside a property, or a visitor who
 *    comes back to the same property on another day. One alert per visitor and property per week.
 * 3. The morning email (08:00 Israel), sent only when there is something to say: new leads of the last 24 hours, leads still
 *    marked new (each lead appears in at most two mornings, then never again, so closed leads stop coming back), yesterday's
 *    property views per property with sources, items waiting in the inbox, and technical notices in plain words. It replaces the
 *    daily "סיכום יומי" (lead-inbox.php) and the daily lead reminder (alerts.php), which now stand down while this module is
 *    loaded; technical alerts (health.php) are queued here instead of mailed one by one.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_om_table' ) ) {

	function nadlan_om_table() { global $wpdb; return $wpdb->prefix . 'nadlan_pview'; }

	/** The views table, created once. */
	function nadlan_om_db() {
		if ( '2' === get_option( 'nadlan_pview_db' ) ) { return; }
		global $wpdb;
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		dbDelta( 'CREATE TABLE ' . nadlan_om_table() . " (
			id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
			post_id bigint(20) unsigned NOT NULL,
			vid varchar(20) NOT NULL,
			ev varchar(8) NOT NULL,
			src varchar(12) NOT NULL DEFAULT '',
			day date NOT NULL,
			ts int(10) unsigned NOT NULL,
			PRIMARY KEY  (id),
			KEY post_day (post_id,day),
			KEY vid_post (vid,post_id)
		) " . $wpdb->get_charset_collate() . ';' );
		update_option( 'nadlan_pview_db', '2', false );
	}
	add_action( 'init', 'nadlan_om_db' );

	function nadlan_om_today() { return wp_date( 'Y-m-d' ); }

	/** A property we count: published, not a demo listing. */
	function nadlan_om_counts( $id ) {
		$p = get_post( $id );
		return $p && 'nadlan_property' === $p->post_type && 'publish' === $p->post_status && ! preg_match( '/-demo$/', $p->post_name );
	}

	/** Queue a line for the morning email (technical notices and the like), kept 7 days, at most 40 lines. */
	function nadlan_om_queue( $kind, $line ) {
		$q = (array) get_option( 'nadlan_om_queue', array() );
		$q[] = array( 'k' => sanitize_key( $kind ), 'l' => wp_strip_all_tags( (string) $line ), 't' => time() );
		$q = array_slice( array_values( array_filter( $q, function ( $x ) { return $x['t'] > time() - 7 * DAY_IN_SECONDS; } ) ), -40 );
		update_option( 'nadlan_om_queue', $q, false );
	}

	function nadlan_om_mail( $subject, $html ) {
		$to = get_option( 'admin_email' );
		if ( ! $to ) { return false; }
		$body = '<div dir="rtl" style="font-family:Arial,sans-serif;font-size:15px;line-height:1.6;color:#12202A;max-width:640px">' . $html .
			'<p style="color:#5E6A75;font-size:12px;margin-top:24px">נדלן · מייל אחד בבוקר, והתראות מיידיות רק על פנייה או מבקר חוזר.</p></div>';
		return wp_mail( $to, $subject, $body, array( 'Content-Type: text/html; charset=UTF-8' ) );
	}

	/* ---------- 1. the beacon on property pages ---------- */
	add_action( 'wp_footer', function () {
		if ( ! is_singular( 'nadlan_property' ) || ! nadlan_om_counts( get_queried_object_id() ) ) { return; }
		$id = (int) get_queried_object_id(); $u = esc_url_raw( rest_url( 'nadlan/v1/pview' ) );
		echo "<script id=\"nadlan-pview\">(function(){var b=document.body;if(!b||b.classList.contains('logged-in')||b.classList.contains('admin-bar')||/bot|crawl|spider|headless|lighthouse/i.test(navigator.userAgent))return;"
			. "var v;try{v=localStorage.getItem('nlpv');if(!v){v=Math.random().toString(36).slice(2,12)+Date.now().toString(36).slice(-4);localStorage.setItem('nlpv',v)}}catch(e){v='s'+Math.random().toString(36).slice(2,14)}"
			. "var r=document.referrer,s=!r?'direct':/google\\./.test(r)?'google':/facebook\\.|fb\\.|instagram\\./.test(r)?'social':/whatsapp|wa\\.me/.test(r)?'whatsapp':/nad-lan\\.co\\.il/.test(r)?'site':'other';"
			. "function go(e){try{var d=JSON.stringify({id:" . $id . ",ev:e,vid:v,src:s});if(navigator.sendBeacon){navigator.sendBeacon('" . $u . "',new Blob([d],{type:'application/json'}))}else{fetch('" . $u . "',{method:'POST',headers:{'Content-Type':'application/json'},body:d,keepalive:true})}}catch(x){}}"
			. "go('view');var t=0,i=setInterval(function(){if(document.visibilityState==='visible'&&++t>=15){clearInterval(i);go('read')}},1000);"
			. "document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'';if(/wa\\.me|whatsapp/.test(h))go('wa');else if(/^tel:/.test(h))go('tel');else if(/walk|tour|360/.test(h))go('tour')},true)})();</script>\n";
	}, 99 );

	add_action( 'rest_api_init', function () {
		register_rest_route( 'nadlan/v1', '/pview', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nadlan_om_pview' ) );
	} );

	function nadlan_om_pview( WP_REST_Request $req ) {
		$p = $req->get_json_params(); if ( ! is_array( $p ) ) { $p = json_decode( (string) $req->get_body(), true ); } if ( ! is_array( $p ) ) { $p = array(); }
		$id = (int) ( $p['id'] ?? 0 ); $ev = sanitize_key( $p['ev'] ?? '' ); $vid = preg_replace( '/[^a-z0-9]/', '', strtolower( (string) ( $p['vid'] ?? '' ) ) );
		$src = sanitize_key( $p['src'] ?? '' ); $ua = isset( $_SERVER['HTTP_USER_AGENT'] ) ? (string) $_SERVER['HTTP_USER_AGENT'] : '';
		$ok = new WP_REST_Response( array( 'ok' => true ), 200 );
		if ( ! in_array( $ev, array( 'view', 'read', 'wa', 'tel', 'tour' ), true ) || strlen( $vid ) < 8 || ! nadlan_om_counts( $id ) || preg_match( '/bot|crawl|spider|headless|lighthouse/i', $ua ) ) { return $ok; }
		if ( ! in_array( $src, array( 'direct', 'google', 'social', 'whatsapp', 'site', 'other' ), true ) ) { $src = 'other'; }
		global $wpdb; $t = nadlan_om_table(); $day = nadlan_om_today(); $vid = substr( $vid, 0, 20 );
		// the same visitor, property and event count once a day
		if ( $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $t WHERE vid=%s AND post_id=%d AND ev=%s AND day=%s LIMIT 1", $vid, $id, $ev, $day ) ) ) { return $ok; }
		$wpdb->insert( $t, array( 'post_id' => $id, 'vid' => $vid, 'ev' => $ev, 'src' => $src, 'day' => $day, 'ts' => time() ) );
		if ( 'view' === $ev ) { update_post_meta( $id, 'view_count', (int) get_post_meta( $id, 'view_count', true ) + 1 ); }
		$hot = '';
		if ( 'wa' === $ev || 'tel' === $ev ) { $hot = 'wa' === $ev ? 'לחצו על וואטסאפ בתוך הנכס' : 'לחצו על הטלפון בתוך הנכס'; }
		elseif ( 'view' === $ev ) {
			$days = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(DISTINCT day) FROM $t WHERE vid=%s AND post_id=%d AND ev='view'", $vid, $id ) );
			if ( $days >= 2 ) { $hot = 'מבקר חזר לנכס ביום נוסף (' . $days . ' ימים שונים)'; }
		}
		if ( $hot ) { nadlan_om_hot( $id, $vid, $hot, $src ); }
		return $ok;
	}

	/** An instant alert: one per visitor and property per week, at most 6 a day. */
	function nadlan_om_hot( $id, $vid, $what, $src ) {
		$k = 'nadlan_om_hot_' . md5( $vid . '|' . $id );
		if ( get_transient( $k ) ) { return; }
		$cap = 'nadlan_om_hot_n_' . nadlan_om_today(); $n = (int) get_transient( $cap );
		if ( $n >= 6 ) { nadlan_om_queue( 'hot', get_the_title( $id ) . ': ' . $what . ' (אחרי מכסת ההתראות היומית)' ); return; }
		set_transient( $k, 1, 7 * DAY_IN_SECONDS ); set_transient( $cap, $n + 1, DAY_IN_SECONDS );
		global $wpdb; $t = nadlan_om_table();
		$seen = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $t WHERE post_id=%d AND ev='view' AND day>=%s", $id, wp_date( 'Y-m-d', time() - 6 * DAY_IN_SECONDS ) ) );
		$src_he = array( 'direct' => 'כניסה ישירה', 'google' => 'גוגל', 'social' => 'רשת חברתית', 'whatsapp' => 'וואטסאפ', 'site' => 'מתוך האתר', 'other' => 'אתר אחר' );
		nadlan_om_mail( '🔥 ' . get_the_title( $id ) . ': ' . $what,
			'<p style="font-size:17px"><b>' . esc_html( get_the_title( $id ) ) . '</b></p><p>' . esc_html( $what ) . '. הגיע מ: ' . esc_html( $src_he[ $src ] ?? $src ) . '. צפיות בנכס ב־7 הימים האחרונים: ' . $seen . '.</p>'
			. '<p><a href="' . esc_url( get_permalink( $id ) ) . '">לעמוד הנכס</a></p><p style="color:#5E6A75;font-size:13px">אנחנו לא יודעים מי המבקר: אין שם ואין טלפון, רק סימן שהוא מתעניין ברצינות. אם הוא ישאיר פרטים, תקבלו מייל ליד כרגיל.</p>' );
	}

	/* ---------- 3. the morning email ---------- */
	add_action( 'init', function () {
		if ( ! wp_next_scheduled( 'nadlan_om_morning' ) ) {
			$d = new DateTime( 'tomorrow 08:00', wp_timezone() );
			wp_schedule_event( $d->getTimestamp(), 'daily', 'nadlan_om_morning' );
		}
	} );
	add_action( 'nadlan_om_morning', 'nadlan_om_send' );

	/** Build (and with $send send) the morning email; returns the HTML ('' when there is nothing to say). */
	function nadlan_om_send( $send = true, $day = '' ) {
		global $wpdb; $out = '';
		// new leads, last 24 hours
		$new = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => 30, 'date_query' => array( array( 'after' => '24 hours ago' ) ) ) );
		if ( $new ) {
			$out .= '<h3 style="margin:18px 0 6px">לידים חדשים ב־24 השעות האחרונות: ' . count( $new ) . '</h3><ul style="padding-right:18px;margin:0">';
			foreach ( $new as $l ) {
				$pr = (int) get_post_meta( $l->ID, 'project_wp_id', true );
				$out .= '<li>' . esc_html( get_post_meta( $l->ID, 'name', true ) . ' · ' . get_post_meta( $l->ID, 'phone', true ) ) . ( $pr ? ' · ' . esc_html( get_the_title( $pr ) ) : '' ) . '</li>';
			}
			$out .= '</ul>';
		}
		// leads still "new": 20 hours to 7 days old, each in at most two mornings
		$wait = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => 30,
			'date_query' => array( array( 'before' => '20 hours ago', 'after' => '7 days ago' ) ),
			'meta_query' => array( array( 'key' => 'lead_status', 'value' => 'new' ) ) ) );
		$wl = '';
		foreach ( $wait as $l ) {
			$c = (int) get_post_meta( $l->ID, 'lead_om_reminded', true );
			if ( $c >= 2 ) { continue; }
			if ( $send ) { update_post_meta( $l->ID, 'lead_om_reminded', $c + 1 ); }
			$wl .= '<li>' . esc_html( get_post_meta( $l->ID, 'name', true ) . ' · ' . get_post_meta( $l->ID, 'phone', true ) . ' · ' . wp_date( 'j.n', strtotime( $l->post_date_gmt . ' UTC' ) ) ) . ' · <a href="' . esc_url( admin_url( 'post.php?post=' . $l->ID . '&action=edit' ) ) . '">סמן כטופל</a></li>';
		}
		if ( $wl ) { $out .= '<h3 style="margin:18px 0 6px">לידים שעוד לא סומנו כטופלו</h3><p style="margin:0 0 4px;color:#5E6A75;font-size:13px">כל ליד מופיע כאן לכל היותר בשני בקרים, ואחר כך לא שוב.</p><ul style="padding-right:18px;margin:0">' . $wl . '</ul>'; }
		// yesterday's property views
		$t = nadlan_om_table(); $y = preg_match( '/^\d{4}-\d{2}-\d{2}$/', (string) $day ) ? $day : wp_date( 'Y-m-d', time() - DAY_IN_SECONDS ); $w7 = wp_date( 'Y-m-d', time() - 7 * DAY_IN_SECONDS );
		$rows = $wpdb->get_results( $wpdb->prepare( "SELECT post_id, SUM(ev='view') v, SUM(ev='read') r, SUM(ev IN ('wa','tel')) c, SUM(ev='tour') u,
			SUM(ev='view' AND src='google') g, SUM(ev='view' AND src='whatsapp') w, SUM(ev='view' AND src='social') s FROM $t WHERE day=%s GROUP BY post_id ORDER BY v DESC", $y ) );
		if ( $rows ) {
			$out .= '<h3 style="margin:18px 0 6px">מי ראה את הנכסים אתמול</h3><table cellpadding="6" style="border-collapse:collapse;font-size:14px;width:100%"><tr style="background:#EEF2F6"><th align="right">נכס</th><th>צפיות</th><th>קראו</th><th>חזרו</th><th>וואטסאפ / טלפון</th><th>מאיפה</th></tr>';
			foreach ( $rows as $r ) {
				$ret = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM (SELECT vid FROM $t WHERE post_id=%d AND ev='view' AND day>=%s GROUP BY vid HAVING COUNT(DISTINCT day)>=2 AND MAX(day)=%s) x", $r->post_id, $w7, $y ) );
				$from = array_filter( array( $r->g ? 'גוגל ' . $r->g : '', $r->w ? 'וואטסאפ ' . $r->w : '', $r->s ? 'רשתות ' . $r->s : '' ) );
				$out .= '<tr style="border-top:1px solid #DDE3EA"><td><a href="' . esc_url( get_permalink( $r->post_id ) ) . '">' . esc_html( get_the_title( $r->post_id ) ) . '</a></td><td align="center">' . (int) $r->v . '</td><td align="center">' . (int) $r->r . '</td><td align="center">' . $ret . '</td><td align="center">' . (int) $r->c . '</td><td>' . esc_html( implode( ' · ', $from ) ) . '</td></tr>';
			}
			$out .= '</table><p style="margin:4px 0 0;color:#5E6A75;font-size:13px">״קראו״ = נשארו בעמוד לפחות 15 שניות. ״חזרו״ = מבקרים שהיו בנכס גם ביום אחר השבוע. הכניסות שלכם ושל רובוטים לא נספרות.</p>';
		}
		// waiting in the inbox
		if ( function_exists( 'nadlan_inbox_counts' ) ) {
			$c = nadlan_inbox_counts(); $pend = array();
			if ( ! empty( $c['claims_pending'] ) ) { $pend[] = 'בקשות בעלות על כרטיס: ' . (int) $c['claims_pending']; }
			if ( ! empty( $c['reviews_pending'] ) ) { $pend[] = 'חוות דעת לאישור: ' . (int) $c['reviews_pending']; }
			if ( ! empty( $c['paid_24h'] ) ) { $pend[] = 'רכישות ב־24 השעות האחרונות: ' . (int) $c['paid_24h']; }
			if ( $pend ) { $out .= '<h3 style="margin:18px 0 6px">מחכה לך</h3><p style="margin:0">' . esc_html( implode( ' · ', $pend ) ) . ' · <a href="' . esc_url( admin_url( 'admin.php?page=nadlan-inbox' ) ) . '">לתיבה</a></p>'; }
		}
		// queued notices (technical, capped hot alerts)
		$q = (array) get_option( 'nadlan_om_queue', array() );
		if ( $q ) {
			$out .= '<h3 style="margin:18px 0 6px">הודעות מהמערכת</h3><ul style="padding-right:18px;margin:0;color:#3E4C58;font-size:14px">';
			foreach ( array_slice( $q, -10 ) as $x ) { $out .= '<li>' . esc_html( ( 'tech' === $x['k'] ? 'תקלה טכנית: ' : '' ) . $x['l'] ) . '</li>'; }
			$out .= '</ul>';
			if ( $send ) { update_option( 'nadlan_om_queue', array(), false ); }
		}
		if ( '' === $out ) { return ''; }
		$html = '<h2 style="margin:0 0 4px">בוקר טוב · נדלן · ' . esc_html( wp_date( 'j.n.Y' ) ) . '</h2>' . $out;
		if ( $send ) { nadlan_om_mail( 'בוקר טוב מנדלן · ' . wp_date( 'j.n' ) . ( $new ? ' · ' . count( $new ) . ' לידים חדשים' : '' ) . ( $rows ? ' · צפיות בנכסים' : '' ), $html ); }
		return $html;
	}

	/** Admin-only preview of the morning email, without sending or marking anything: GET /wp-json/nadlan/v1/om-preview[?day=YYYY-MM-DD for the views of that day] */
	add_action( 'rest_api_init', function () {
		register_rest_route( 'nadlan/v1', '/om-preview', array( 'methods' => 'GET', 'permission_callback' => function () { return current_user_can( 'manage_options' ); },
			'callback' => function ( $r ) { global $wpdb; $t = nadlan_om_table(); return new WP_REST_Response( array( 'html' => nadlan_om_send( false, (string) $r->get_param( 'day' ) ), 'views_total' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM $t" ), 'next' => wp_next_scheduled( 'nadlan_om_morning' ) ), 200 ); } ) );
	} );
}
