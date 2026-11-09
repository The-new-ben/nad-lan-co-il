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
 * 1.72.613 (HAD-687): the mails use the OwnerMail card and signed actions of owner-mail.php; the morning mail opens with what to
 *    handle today, then what changed since yesterday in numbers, one action per line; it is not sent when nothing is new or repeated.
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

	/** An instant alert: one per visitor and property per week, at most 6 a day; a muted kind ("hot") waits for the morning mail. */
	function nadlan_om_hot( $id, $vid, $what, $src ) {
		$k = 'nadlan_om_hot_' . md5( $vid . '|' . $id );
		if ( get_transient( $k ) ) { return; }
		if ( function_exists( 'nadlan_omx_muted' ) && nadlan_omx_muted( 'hot' ) ) { set_transient( $k, 1, 7 * DAY_IN_SECONDS ); nadlan_om_queue( 'hot', get_the_title( $id ) . ': ' . $what . ' (מושתק, לכן רק כאן)' ); return; }
		$cap = 'nadlan_om_hot_n_' . nadlan_om_today(); $n = (int) get_transient( $cap );
		if ( $n >= 6 ) { nadlan_om_queue( 'hot', get_the_title( $id ) . ': ' . $what . ' (אחרי מכסת ההתראות היומית)' ); return; }
		set_transient( $k, 1, 7 * DAY_IN_SECONDS ); set_transient( $cap, $n + 1, DAY_IN_SECONDS );
		global $wpdb; $t = nadlan_om_table();
		$seen = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $t WHERE post_id=%d AND ev='view' AND day>=%s", $id, wp_date( 'Y-m-d', time() - 6 * DAY_IN_SECONDS ) ) );
		$src_he = array( 'direct' => 'כניסה ישירה', 'google' => 'גוגל', 'social' => 'רשת חברתית', 'whatsapp' => 'וואטסאפ', 'site' => 'מתוך האתר', 'other' => 'אתר אחר' );
		$title = wp_strip_all_tags( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) );
		if ( ! function_exists( 'nadlan_omx_doc' ) ) { nadlan_om_mail( $title . ': ' . $what, '<p><b>' . esc_html( $title ) . '</b></p><p>' . esc_html( $what ) . '</p><p><a href="' . esc_url( get_permalink( $id ) ) . '">לעמוד הנכס</a></p>' ); return; }
		$rows = '<tr><td style="padding:16px 18px 6px"><div style="font-size:20px;line-height:26px;font-weight:700">' . esc_html( $title ) . '</div>'
			. '<div style="font-size:15px;line-height:22px;margin:6px 0 10px">' . esc_html( $what ) . '. הגיע מ: ' . esc_html( $src_he[ $src ] ?? $src ) . '. צפיות בנכס ב־7 הימים האחרונים: <b>' . $seen . '</b>.</div>'
			. nadlan_omx_btn( get_permalink( $id ), 'לעמוד הנכס', '#2F6F86' ) . '</td></tr>'
			. '<tr><td style="padding:0 18px 12px;font-size:13px;line-height:20px;color:#3E4C58">אין לנו שם או טלפון של המבקר, רק סימן שהוא מתעניין ברצינות. אם הוא ישאיר פרטים, יגיע מייל ליד עם כפתורי חיוג.</td></tr>';
		nadlan_omx_send( 'מבקר חם · ' . $title . ' · ' . $what,
			nadlan_omx_doc( $title . ' · ' . $what, nadlan_omx_strip( 'נדל״ן · מבקר חם בנכס · ' . esc_html( wp_date( 'H:i' ) ) ), $rows,
				'התראה כזו מגיעה רק על לחיצת וואטסאפ או טלפון בתוך נכס, או על מבקר שחזר ביום אחר; לכל היותר 6 ביום.<br>' . nadlan_omx_mute_link( 'hot' ) ),
			$title . "\n" . $what . "\n" . get_permalink( $id ), 'hot' );
	}

	/* ---------- 3. the morning email ---------- */
	add_action( 'init', function () {
		if ( ! wp_next_scheduled( 'nadlan_om_morning' ) ) {
			$d = new DateTime( 'tomorrow 08:00', wp_timezone() );
			wp_schedule_event( $d->getTimestamp(), 'daily', 'nadlan_om_morning' );
		}
	} );
	add_action( 'nadlan_om_morning', 'nadlan_om_send' );

	/** One urgent row: who, the phone, where from and why it is here; the call button, then the three signed actions. */
	function nadlan_om_lead_row( $lid, $why ) {
		list( $intl, $tel, $pretty ) = nadlan_omx_phone( nadlan_omx_m( $lid, 'phone' ) );
		$h = nadlan_omx_heat( $lid ); $c = nadlan_omx_heat_color( $h['level'] ); $wh = nadlan_omx_where( $lid ); $nm = nadlan_omx_m( $lid, 'name' );
		$a = function ( $act, $lab ) use ( $lid ) { return '<a href="' . esc_url( nadlan_omx_url( $act, $lid ) ) . '" style="color:#1F4B5C;font-weight:700">' . esc_html( $lab ) . '</a>'; };
		return '<tr><td style="padding:10px 0;border-bottom:1px solid #E3E8EC">'
			. '<div style="font-size:15px;line-height:22px;font-weight:700">' . esc_html( '' !== $nm ? $nm : 'פונה בלי שם' ) . ( '' !== $pretty ? ' · <span dir="ltr">' . esc_html( $pretty ) . '</span>' : '' ) . '</div>'
			. '<div style="font-size:13px;line-height:19px;color:#5E6A75"><b style="color:' . $c[0] . '">' . $c[1] . ' ' . (int) $h['score'] . '</b> · ' . esc_html( $why ) . ( '' !== $wh ? ' · ' . esc_html( $wh ) : '' ) . '</div>'
			. '<div style="font-size:13px;line-height:22px;margin-top:2px">' . $a( 'contacted', '✓ חזרתי אליו' ) . ' &nbsp;·&nbsp; ' . $a( 'lost', 'לא רלוונטי' ) . ' &nbsp;·&nbsp; ' . $a( 'snooze', 'מחר בבוקר' ) . '</div></td>'
			. '<td align="left" valign="top" style="padding:10px 0;border-bottom:1px solid #E3E8EC;white-space:nowrap">'
			. ( $intl ? nadlan_omx_btn( 'tel:' . $tel, 'התקשר', '#2F6F86' ) . '<br>' . nadlan_omx_btn( 'https://wa.me/' . $intl . '?text=' . rawurlencode( nadlan_omx_wa_text( $lid ) ), 'וואטסאפ', '#0F7A63' ) : '' ) . '</td></tr>';
	}
	function nadlan_om_h( $t, $sub = '' ) {
		return '<tr><td style="padding:16px 18px 4px"><div style="font-size:17px;line-height:24px;font-weight:700">' . esc_html( $t ) . '</div>' . ( '' !== $sub ? '<div style="font-size:13px;color:#5E6A75">' . esc_html( $sub ) . '</div>' : '' ) . '</td></tr>';
	}

	/** Build (and with $send send) the morning email; returns the HTML ('' when there is nothing new). $mark=false sends a sample without marking anything. */
	function nadlan_om_send( $send = true, $day = '', $mark = null ) {
		global $wpdb;
		$mark  = null === $mark ? (bool) $send : (bool) $mark;
		$today = wp_date( 'Y-m-d' );
		$y     = preg_match( '/^\d{4}-\d{2}-\d{2}$/', (string) $day ) ? $day : wp_date( 'Y-m-d', time() - DAY_IN_SECONDS );
		if ( ! function_exists( 'nadlan_omx_doc' ) ) { return ''; }
		// 1. what to handle today: reminders asked for, new leads still open, leads waiting (each in at most two mornings)
		$urgent = array();
		foreach ( get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => 30, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'lead_omx_snooze', 'value' => $today, 'compare' => '<=', 'type' => 'DATE' ) ) ) ) as $id ) { $urgent[ $id ] = 'ביקשת תזכורת להיום'; }
		$new = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => 30, 'date_query' => array( array( 'after' => '24 hours ago' ) ) ) );
		foreach ( $new as $l ) {
			$st = (string) get_post_meta( $l->ID, 'lead_status', true );
			if ( ( '' === $st || 'new' === $st ) && ! isset( $urgent[ $l->ID ] ) ) { $urgent[ $l->ID ] = 'ליד חדש מ־' . wp_date( 'j.n H:i', strtotime( $l->post_date_gmt . ' UTC' ) ); }
		}
		$wait = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => 30,
			'date_query' => array( array( 'before' => '20 hours ago', 'after' => '7 days ago' ) ),
			'meta_query' => array( array( 'key' => 'lead_status', 'value' => 'new' ) ) ) );
		$remind = array();
		foreach ( $wait as $l ) {
			if ( isset( $urgent[ $l->ID ] ) ) { continue; }
			$c = (int) get_post_meta( $l->ID, 'lead_om_reminded', true );
			if ( $c >= 2 ) { continue; }
			$remind[ $l->ID ] = $c + 1;
			$urgent[ $l->ID ] = 'עוד לא סומן כטופל, מ־' . wp_date( 'j.n', strtotime( $l->post_date_gmt . ' UTC' ) ) . ( $c ? ' · פעם אחרונה כאן' : '' );
		}
		// 2. the numbers, yesterday against the day before and the week
		$kp = nadlan_omx_kpis( $y );
		// 3. yesterday's property views
		$t = nadlan_om_table(); $w7 = wp_date( 'Y-m-d', time() - 7 * DAY_IN_SECONDS );
		$rows = $wpdb->get_results( $wpdb->prepare( "SELECT post_id, SUM(ev='view') v, SUM(ev='read') r, SUM(ev IN ('wa','tel')) c,
			SUM(ev='view' AND src='google') g, SUM(ev='view' AND src='whatsapp') w, SUM(ev='view' AND src='social') s FROM $t WHERE day=%s GROUP BY post_id ORDER BY c DESC, v DESC LIMIT 12", $y ) );
		// 4. waiting in the inbox, 5. system notices
		$pend = array();
		if ( function_exists( 'nadlan_inbox_counts' ) ) {
			$ic = nadlan_inbox_counts();
			if ( ! empty( $ic['claims_pending'] ) ) { $pend[] = array( 'בקשות בעלות על כרטיס לאישור: ' . (int) $ic['claims_pending'], admin_url( 'admin.php?page=nadlan-inbox' ), 'לאישור' ); }
			if ( ! empty( $ic['reviews_pending'] ) ) { $pend[] = array( 'חוות דעת לאישור: ' . (int) $ic['reviews_pending'], admin_url( 'admin.php?page=nadlan-inbox' ), 'לאישור' ); }
			if ( ! empty( $ic['paid_24h'] ) ) { $pend[] = array( 'רכישות ב־24 השעות האחרונות: ' . (int) $ic['paid_24h'], admin_url( 'admin.php?page=nadlan-inbox' ), 'לפרטים' ); }
		}
		$q = (array) get_option( 'nadlan_om_queue', array() );
		// nothing new = no mail (HubSpot's rule too); the same content as the last mail = no mail
		$moved = 0;
		foreach ( $kp as $r ) { if ( false === strpos( $r[0], 'גוגל' ) && false === strpos( $r[0], 'צפיות' ) && empty( $r[6] ) && (int) $r[1] > 0 ) { $moved++; } }
		if ( ! $urgent && ! $rows && ! $pend && ! $q && ! $moved ) {
			if ( $send && $mark ) { nadlan_omx_log( 'morning', 'בוקר ' . $today, 'skipped_empty' ); }
			return '';
		}
		$fp = md5( wp_json_encode( array( array_keys( $urgent ), array_map( function ( $r ) { return array( $r[1], $r[2] ); }, $kp ), $rows, $pend, $q ) ) );
		if ( $send && $mark && get_option( 'nadlan_omx_morning_fp' ) === $fp ) { nadlan_omx_log( 'morning', 'בוקר ' . $today, 'skipped_repeat' ); return ''; }
		$out = '';
		if ( $urgent ) {
			$out .= nadlan_om_h( 'לטפל היום: ' . count( $urgent ), 'לחיצה על "חזרתי אליו" או "לא רלוונטי" מורידה את הליד מהרשימה. כל ליד ממתין מופיע לכל היותר בשני בקרים.' )
				. '<tr><td style="padding:0 18px 6px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">';
			foreach ( $urgent as $id => $why ) { $out .= nadlan_om_lead_row( $id, $why ); }
			$out .= '</table></td></tr>';
		}
		$out .= nadlan_om_h( 'מה השתנה מאתמול', 'אתמול ' . wp_date( 'j.n', strtotime( $y . ' 12:00:00' ) ) . ' מול היום שלפניו, ו־7 הימים האחרונים' )
			. '<tr><td style="padding:4px 18px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;line-height:20px">'
			. '<tr style="color:#5E6A75;font-size:12px"><td style="padding:4px 0">מדד</td><td align="center">אתמול</td><td align="center">שינוי</td><td align="center">7 ימים</td><td align="left">פעולה</td></tr>';
		foreach ( $kp as $r ) {
			$out .= '<tr><td style="padding:8px 0;border-top:1px solid #E3E8EC">' . esc_html( $r[0] ) . '</td><td align="center" style="border-top:1px solid #E3E8EC;font-size:18px;font-weight:700">' . esc_html( number_format_i18n( (int) $r[1] ) ) . '</td>'
				. '<td align="center" style="border-top:1px solid #E3E8EC;font-size:13px">' . nadlan_omx_delta( $r[1], $r[2], ! empty( $r[6] ) ) . '</td><td align="center" style="border-top:1px solid #E3E8EC;color:#3E4C58">' . esc_html( number_format_i18n( (int) $r[3] ) ) . '</td>'
				. '<td align="left" style="border-top:1px solid #E3E8EC;font-size:13px"><a href="' . esc_url( $r[4] ) . '" style="color:#1F4B5C">' . esc_html( $r[5] ) . '</a></td></tr>';
		}
		$out .= '</table></td></tr>';
		if ( $rows ) {
			$out .= nadlan_om_h( 'מי ראה נכסים אתמול', '"קראו" = לפחות 15 שניות בעמוד. "חזרו" = היו בנכס גם ביום אחר השבוע. הכניסות שלך ושל רובוטים לא נספרות.' )
				. '<tr><td style="padding:0 18px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-size:13px;line-height:19px">'
				. '<tr style="color:#5E6A75;font-size:12px"><td style="padding:4px 0">נכס</td><td align="center">צפו</td><td align="center">קראו</td><td align="center">חזרו</td><td align="center">וואטסאפ/טלפון</td><td align="left">פעולה</td></tr>';
			foreach ( $rows as $r ) {
				$ret  = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM (SELECT vid FROM $t WHERE post_id=%d AND ev='view' AND day>=%s GROUP BY vid HAVING COUNT(DISTINCT day)>=2 AND MAX(day)=%s) x", $r->post_id, $w7, $y ) );
				$from = array_filter( array( $r->g ? 'גוגל ' . $r->g : '', $r->w ? 'וואטסאפ ' . $r->w : '', $r->s ? 'רשתות ' . $r->s : '' ) );
				$out .= '<tr><td style="padding:7px 0;border-top:1px solid #E3E8EC">' . esc_html( wp_strip_all_tags( html_entity_decode( get_the_title( $r->post_id ), ENT_QUOTES, 'UTF-8' ) ) ) . ( $from ? '<div style="color:#5E6A75;font-size:12px">' . esc_html( implode( ' · ', $from ) ) . '</div>' : '' ) . '</td>'
					. '<td align="center" style="border-top:1px solid #E3E8EC">' . (int) $r->v . '</td><td align="center" style="border-top:1px solid #E3E8EC">' . (int) $r->r . '</td><td align="center" style="border-top:1px solid #E3E8EC">' . $ret . '</td>'
					. '<td align="center" style="border-top:1px solid #E3E8EC;' . ( (int) $r->c ? 'font-weight:700;color:#B42318' : '' ) . '">' . (int) $r->c . '</td>'
					. '<td align="left" style="border-top:1px solid #E3E8EC"><a href="' . esc_url( get_permalink( $r->post_id ) ) . '" style="color:#1F4B5C">לנכס</a></td></tr>';
			}
			$out .= '</table></td></tr>';
		}
		if ( $pend ) {
			$out .= nadlan_om_h( 'מחכה לאישור שלך' ) . '<tr><td style="padding:0 18px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-size:14px">';
			foreach ( $pend as $p ) { $out .= '<tr><td style="padding:7px 0;border-top:1px solid #E3E8EC">' . esc_html( $p[0] ) . '</td><td align="left" style="border-top:1px solid #E3E8EC"><a href="' . esc_url( $p[1] ) . '" style="color:#1F4B5C;font-weight:700">' . esc_html( $p[2] ) . '</a></td></tr>'; }
			$out .= '</table></td></tr>';
		}
		if ( $q ) {
			$out .= nadlan_om_h( 'הודעות מהמערכת' ) . '<tr><td style="padding:0 18px 8px"><ul style="padding-right:18px;margin:4px 0;color:#3E4C58;font-size:13px;line-height:20px">';
			foreach ( array_slice( $q, -10 ) as $x ) { $out .= '<li>' . esc_html( ( 'tech' === $x['k'] ? 'תקלה טכנית: ' : '' ) . $x['l'] ) . '</li>'; }
			$out .= '</ul></td></tr>';
		}
		$mutes = array_filter( (array) get_option( 'nadlan_omx_mute', array() ), function ( $tt ) { return (int) $tt > time(); } );
		$foot  = 'המייל נשלח רק כשיש משהו חדש, ולא נשלח פעמיים אותו דבר. לידים חדשים מגיעים מיד במייל נפרד.';
		$kinds = nadlan_omx_kinds();
		foreach ( $mutes as $mk => $mt ) { $foot .= '<br>מושתק עד ' . esc_html( wp_date( 'j.n', (int) $mt ) ) . ': ' . esc_html( $kinds[ $mk ] ?? $mk ) . ' · <a href="' . esc_url( nadlan_omx_url( 'unmute', 0, $mk ) ) . '" style="color:#5E6A75">בטל השתקה</a>'; }
		$leads_y = (int) ( $kp[0][1] ?? 0 );
		$bits = array_filter( array( $urgent ? count( $urgent ) . ' לטפל היום' : '', $leads_y ? $leads_y . ' לידים אתמול' : '', ! empty( $kp[1][1] ) ? (int) $kp[1][1] . ' נרשמים' : '' ) );
		$subj = 'בוקר טוב מנדל״ן · ' . wp_date( 'j.n' ) . ( $bits ? ' · ' . implode( ' · ', $bits ) : '' );
		$html = nadlan_omx_doc( $bits ? implode( ' · ', $bits ) : 'מה השתנה מאתמול', nadlan_omx_strip( 'נדל״ן · בוקר טוב · יום ' . array( 'ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת' )[ (int) wp_date( 'w' ) ] . ' ' . esc_html( wp_date( 'j.n.Y' ) ) ), $out, $foot );
		if ( $send ) {
			$text = 'בוקר טוב מנדל״ן · ' . wp_date( 'j.n' ) . "\n";
			foreach ( $urgent as $id => $why ) { $text .= '- ' . nadlan_omx_m( $id, 'name' ) . ' ' . nadlan_omx_m( $id, 'phone' ) . ' · ' . $why . ' · חזרתי אליו: ' . nadlan_omx_url( 'contacted', $id ) . "\n"; }
			foreach ( $kp as $r ) { $text .= $r[0] . ': ' . (int) $r[1] . ' (לפני יום ' . (int) $r[2] . ', 7 ימים ' . (int) $r[3] . ")\n"; }
			$ok = nadlan_omx_send( ( $mark ? '' : 'דוגמה · ' ) . $subj, $html, $text, 'morning' );
			if ( $ok && $mark ) {
				foreach ( $remind as $id => $c ) { update_post_meta( $id, 'lead_om_reminded', $c ); }
				foreach ( array_keys( $urgent ) as $id ) { if ( 'ביקשת תזכורת להיום' === $urgent[ $id ] ) { delete_post_meta( $id, 'lead_omx_snooze' ); } }
				update_option( 'nadlan_om_queue', array(), false );
				update_option( 'nadlan_omx_morning_fp', $fp, false );
			}
		}
		return $html;
	}

	/** Admin-only preview of the morning email, without sending or marking anything: GET /wp-json/nadlan/v1/om-preview[?day=YYYY-MM-DD for the views of that day] */
	add_action( 'rest_api_init', function () {
		register_rest_route( 'nadlan/v1', '/om-preview', array( 'methods' => 'GET', 'permission_callback' => function () { return current_user_can( 'manage_options' ); },
			'callback' => function ( $r ) { global $wpdb; $t = nadlan_om_table(); return new WP_REST_Response( array( 'html' => nadlan_om_send( false, (string) $r->get_param( 'day' ) ), 'views_total' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM $t" ), 'next' => wp_next_scheduled( 'nadlan_om_morning' ) ), 200 ); } ) );
	} );
}
