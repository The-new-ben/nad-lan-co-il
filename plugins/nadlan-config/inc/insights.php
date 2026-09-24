<?php
/**
 * Broker and professional insights, private to the site owner (owner order 24.9.2026):
 * "I need an indicator for every broker: first whether they get traffic, and if so, a way to settle accounts.
 * Meital does not pay me today, but I may ask for something when she closes deals. Between us: never on the site."
 *
 * 1. Events. A small beacon on a professional's card, on a broker's own site pages and on their listings counts
 *    views and clicks: the broker's WhatsApp, a call, "תיאום סיור", and the SITE's own WhatsApp button (leads
 *    that reach the owner). Pages are cached, so the count comes from the browser, not from PHP. No IP is stored:
 *    a visitor is a hash that changes every day. Crawlers and headless browsers are not counted.
 * 2. A private dashboard: NadLan Ops > "מתווכים: תנועה ועסקאות", per broker and per listing, 7/30/90 days.
 * 3. A private deals ledger: the owner records a closed deal and what was agreed, and marks it settled.
 *    The screen carries the legal note: a percentage of a deal is a brokerage fee in substance; a fixed fee is safe.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_INSIGHTS_DB_VERSION = '1';

if ( ! function_exists( 'nadlan_insights_tables' ) ) {
	function nadlan_insights_tables() {
		global $wpdb;
		return array( 'ev' => $wpdb->prefix . 'nadlan_ev', 'ledger' => $wpdb->prefix . 'nadlan_broker_ledger' );
	}
}

if ( ! function_exists( 'nadlan_insights_install' ) ) {
	function nadlan_insights_install() {
		if ( get_option( 'nadlan_insights_db_version' ) === NADLAN_INSIGHTS_DB_VERSION ) { return; }
		global $wpdb;
		$t = nadlan_insights_tables();
		$c = $wpdb->get_charset_collate();
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		dbDelta( "CREATE TABLE {$t['ev']} (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			ts DATETIME NOT NULL,
			day DATE NOT NULL,
			ev VARCHAR(16) NOT NULL,
			pro BIGINT UNSIGNED NOT NULL DEFAULT 0,
			post BIGINT UNSIGNED NOT NULL DEFAULT 0,
			slot VARCHAR(40) NOT NULL DEFAULT '',
			sid CHAR(16) NOT NULL DEFAULT '',
			ref VARCHAR(80) NOT NULL DEFAULT '',
			PRIMARY KEY  (id),
			KEY pro_day (pro,day),
			KEY post_day (post,day),
			KEY ev_day (ev,day),
			KEY sid (sid)
		) $c;" );
		dbDelta( "CREATE TABLE {$t['ledger']} (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			pro BIGINT UNSIGNED NOT NULL,
			post BIGINT UNSIGNED NOT NULL DEFAULT 0,
			deal_date DATE NULL,
			deal_price BIGINT NULL,
			amount INT NULL,
			status VARCHAR(12) NOT NULL DEFAULT 'open',
			note TEXT NULL,
			created_by BIGINT UNSIGNED NOT NULL DEFAULT 0,
			created_at DATETIME NOT NULL,
			PRIMARY KEY  (id),
			KEY pro (pro)
		) $c;" );
		update_option( 'nadlan_insights_db_version', NADLAN_INSIGHTS_DB_VERSION, false );
	}
}
add_action( 'admin_init', 'nadlan_insights_install' );

/* ---------------- which professional a page belongs to ---------------- */
if ( ! function_exists( 'nadlan_insights_context' ) ) {
	/** array( pro, post, wa digits ) for a professional's card, a broker's site page or an owned listing; null elsewhere. */
	function nadlan_insights_context() {
		if ( is_admin() || ! is_singular() ) { return null; }
		$id  = (int) get_queried_object_id();
		$pro = 0;
		if ( is_singular( 'nadlan_professional' ) ) {
			$pro = $id;
		} elseif ( ( is_singular( 'nadlan_property' ) || is_page() ) && function_exists( 'nadlan_property_owner' ) ) {
			$pro = (int) nadlan_property_owner( $id );
		}
		if ( $pro <= 0 || 'nadlan_professional' !== get_post_type( $pro ) ) { return null; }
		$phone = (string) get_post_meta( $pro, 'phone', true );
		$wa    = function_exists( 'nadlan_prof_wa_digits' ) ? (string) nadlan_prof_wa_digits( $phone ) : preg_replace( '/\D/', '', $phone );
		return array( 'pro' => $pro, 'post' => $id, 'wa' => $wa );
	}
}

add_action( 'wp_footer', function () {
	$c = nadlan_insights_context();
	if ( ! $c || '0' === (string) get_option( 'nadlan_insights_on', '1' ) ) { return; }
	$cfg = wp_json_encode( array( 'url' => esc_url_raw( rest_url( 'nadlan/v1/ev' ) ), 'pro' => $c['pro'], 'post' => $c['post'], 'wa' => $c['wa'] ) );
	// the broker's own WhatsApp opens with a prefilled line; "סיור" in it marks a tour request
	echo "\n<script id=\"nadlan-insights\">(function(){var c=" . $cfg . ";if(!navigator.sendBeacon)return;function s(e,x){try{navigator.sendBeacon(c.url,new Blob([JSON.stringify({e:e,pro:c.pro,post:c.post,slot:x||''})],{type:'application/json'}))}catch(_){}}s('view');document.addEventListener('click',function(v){var a=v.target.closest&&v.target.closest('a,button');if(!a||a.closest('.nlpl'))return;var k=a.getAttribute('data-nl-ev');if(k){s(k,a.getAttribute('data-nl-slot'));return}var h=a.getAttribute('href')||'';if(h.indexOf('tel:')===0){s('call');return}if(h.indexOf('https://wa.me/')===0||h.indexOf('https://api.whatsapp.com/')===0){var own=c.wa&&h.indexOf(c.wa)>-1;var t='';try{t=decodeURIComponent(h)}catch(_){t=h}s(own?(t.indexOf('\\u05e1\\u05d9\\u05d5\\u05e8')>-1?'tour':'wa'):'site_wa')}},true)})();</script>\n";
}, 40 );

/* ---------------- the beacon endpoint ---------------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/ev', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => 'nadlan_insights_ev',
	) );
	// the same numbers as the dashboard, for the owner's reports (admin only)
	register_rest_route( 'nadlan/v1', '/ev-stats', array(
		'methods'             => 'GET',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => function ( WP_REST_Request $req ) {
			nadlan_insights_install();
			global $wpdb;
			$t    = nadlan_insights_tables();
			$days = max( 1, min( 365, (int) ( $req->get_param( 'days' ) ?: 30 ) ) );
			$rows = $wpdb->get_results( $wpdb->prepare( "SELECT pro, post, ev, COUNT(*) n FROM {$t['ev']} WHERE day >= %s GROUP BY pro, post, ev", gmdate( 'Y-m-d', time() - $days * DAY_IN_SECONDS ) ), ARRAY_A );
			return array( 'days' => $days, 'rows' => $rows );
		},
	) );
} );

if ( ! function_exists( 'nadlan_insights_ev' ) ) {
	function nadlan_insights_ev( WP_REST_Request $req ) {
		$ok = new WP_REST_Response( null, 204 );
		if ( '0' === (string) get_option( 'nadlan_insights_on', '1' ) ) { return $ok; }
		$ua = isset( $_SERVER['HTTP_USER_AGENT'] ) ? (string) $_SERVER['HTTP_USER_AGENT'] : '';
		if ( '' === $ua || preg_match( '/bot|crawl|spider|slurp|preview|headless|lighthouse|screaming|python|curl|wget|facebookexternalhit/i', $ua ) ) { return $ok; }
		$b    = $req->get_json_params();
		$ev   = is_array( $b ) ? (string) ( $b['e'] ?? '' ) : '';
		$pro  = is_array( $b ) ? (int) ( $b['pro'] ?? 0 ) : 0;
		$post = is_array( $b ) ? (int) ( $b['post'] ?? 0 ) : 0;
		$slot = is_array( $b ) ? substr( sanitize_key( (string) ( $b['slot'] ?? '' ) ), 0, 40 ) : '';
		if ( ! in_array( $ev, array( 'view', 'wa', 'call', 'tour', 'site_wa', 'lead', 'place_view', 'place_click' ), true ) ) { return $ok; }
		if ( $pro <= 0 || 'nadlan_professional' !== get_post_type( $pro ) || 'publish' !== get_post_status( $pro ) ) { return $ok; }
		if ( $post > 0 && 'publish' !== get_post_status( $post ) ) { $post = 0; }
		$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? (string) $_SERVER['REMOTE_ADDR'] : '';
		$day = current_time( 'Y-m-d' );
		// a visitor is a daily hash: no IP is kept, and nobody can be followed from one day to the next
		$sid = substr( hash( 'sha256', $ip . '|' . $ua . '|' . $day . '|' . wp_salt( 'auth' ) ), 0, 16 );
		$rk  = 'nlev_' . substr( $sid, 0, 12 );
		$n   = (int) get_transient( $rk );
		if ( $n >= 60 ) { return $ok; }
		set_transient( $rk, $n + 1, 10 * MINUTE_IN_SECONDS );
		nadlan_insights_install();
		global $wpdb;
		$t = nadlan_insights_tables();
		if ( 'view' === $ev || 'place_view' === $ev ) {
			$seen = $wpdb->get_var( $wpdb->prepare( "SELECT id FROM {$t['ev']} WHERE sid = %s AND ev = %s AND post = %d AND pro = %d AND ts > %s LIMIT 1",
				$sid, $ev, $post, $pro, gmdate( 'Y-m-d H:i:s', time() - 30 * MINUTE_IN_SECONDS ) ) );
			if ( $seen ) { return $ok; }
		}
		$ref = '';
		if ( ! empty( $_SERVER['HTTP_REFERER'] ) ) {
			$host = wp_parse_url( (string) $_SERVER['HTTP_REFERER'], PHP_URL_HOST );
			$ref  = substr( (string) $host, 0, 80 );
		}
		$wpdb->insert( $t['ev'], array( 'ts' => gmdate( 'Y-m-d H:i:s' ), 'day' => $day, 'ev' => $ev, 'pro' => $pro, 'post' => $post, 'slot' => $slot, 'sid' => $sid, 'ref' => $ref ) );
		return $ok;
	}
}

/* ---------------- the private dashboard ---------------- */
add_action( 'admin_menu', function () {
	add_submenu_page( 'nadlan-ops', 'מתווכים: תנועה ועסקאות', 'מתווכים: תנועה ועסקאות', 'manage_options', 'nadlan-insights', 'nadlan_insights_screen' );
}, 30 );

add_action( 'admin_post_nadlan_ledger_save', function () {
	if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'forbidden', 403 ); }
	check_admin_referer( 'nadlan_ledger' );
	nadlan_insights_install();
	global $wpdb;
	$t  = nadlan_insights_tables();
	$id = isset( $_POST['id'] ) ? (int) $_POST['id'] : 0;
	if ( $id > 0 && isset( $_POST['settle'] ) ) {
		$wpdb->update( $t['ledger'], array( 'status' => 'settled' ), array( 'id' => $id ) );
	} else {
		$row = array(
			'pro'        => isset( $_POST['pro'] ) ? (int) $_POST['pro'] : 0,
			'post'       => isset( $_POST['post'] ) ? (int) $_POST['post'] : 0,
			'deal_date'  => isset( $_POST['deal_date'] ) && preg_match( '/^\d{4}-\d{2}-\d{2}$/', (string) $_POST['deal_date'] ) ? (string) $_POST['deal_date'] : null,
			'deal_price' => isset( $_POST['deal_price'] ) && '' !== $_POST['deal_price'] ? (int) preg_replace( '/\D/', '', (string) $_POST['deal_price'] ) : null,
			'amount'     => isset( $_POST['amount'] ) && '' !== $_POST['amount'] ? (int) preg_replace( '/\D/', '', (string) $_POST['amount'] ) : null,
			'status'     => 'open',
			'note'       => isset( $_POST['note'] ) ? sanitize_textarea_field( wp_unslash( (string) $_POST['note'] ) ) : '',
			'created_by' => get_current_user_id(),
			'created_at' => gmdate( 'Y-m-d H:i:s' ),
		);
		if ( $row['pro'] > 0 ) { $wpdb->insert( $t['ledger'], $row ); }
	}
	wp_safe_redirect( admin_url( 'admin.php?page=nadlan-insights&saved=1' ) );
	exit;
} );

if ( ! function_exists( 'nadlan_insights_screen' ) ) {
	function nadlan_insights_screen() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		nadlan_insights_install();
		global $wpdb;
		$t    = nadlan_insights_tables();
		$days = isset( $_GET['days'] ) ? max( 1, min( 365, (int) $_GET['days'] ) ) : 30;
		$from = gmdate( 'Y-m-d', time() - $days * DAY_IN_SECONDS );
		$rows = $wpdb->get_results( $wpdb->prepare( "SELECT pro, ev, COUNT(*) n FROM {$t['ev']} WHERE day >= %s GROUP BY pro, ev", $from ), ARRAY_A );
		$by   = array();
		foreach ( (array) $rows as $r ) { $by[ (int) $r['pro'] ][ $r['ev'] ] = (int) $r['n']; }
		$brokers = get_posts( array( 'post_type' => 'nadlan_professional', 'post_status' => 'publish', 'numberposts' => 200, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'profession', 'value' => 'metavech' ) ) ) );
		$ids = array_unique( array_merge( array_map( 'intval', $brokers ), array_keys( $by ) ) );
		$ledger = $wpdb->get_results( "SELECT * FROM {$t['ledger']} ORDER BY id DESC LIMIT 200", ARRAY_A );
		$due    = array();
		foreach ( (array) $ledger as $l ) { if ( 'open' === $l['status'] ) { $due[ (int) $l['pro'] ] = ( $due[ (int) $l['pro'] ] ?? 0 ) + (int) $l['amount']; } }
		$cols = array( 'view' => 'צפיות', 'wa' => 'וואטסאפ למתווך', 'call' => 'חיוג', 'tour' => 'בקשות סיור', 'site_wa' => 'פניות אלינו (הכפתור של האתר)', 'place_view' => 'הופעות בשיבוץ', 'place_click' => 'לחיצות בשיבוץ' );
		echo '<div class="wrap" dir="rtl"><h1>מתווכים: תנועה ועסקאות</h1>';
		echo '<p>פרטי. לא מוצג באתר. הספירה מהדפדפן של המבקרים, בלי כתובות IP, בלי רובוטים ובלי דפדפנים אוטומטיים. צפייה חוזרת של אותו מבקר באותו עמוד בתוך 30 דקות נספרת פעם אחת.</p>';
		echo '<p>';
		foreach ( array( 7, 30, 90 ) as $d ) {
			echo $d === $days ? '<strong>' . (int) $d . ' ימים</strong> ' : '<a href="' . esc_url( admin_url( 'admin.php?page=nadlan-insights&days=' . $d ) ) . '">' . (int) $d . ' ימים</a> ';
		}
		echo '</p><table class="widefat striped"><thead><tr><th>מתווך או בעל מקצוע</th>';
		foreach ( $cols as $label ) { echo '<th>' . esc_html( $label ) . '</th>'; }
		echo '<th>פניות בטופס</th><th>פתוח ביומן העסקאות (₪)</th></tr></thead><tbody>';
		foreach ( $ids as $pid ) {
			if ( 'nadlan_professional' !== get_post_type( $pid ) ) { continue; }
			$leads = function_exists( 'nadlan_ac_lead_count' ) ? (int) nadlan_ac_lead_count( $pid ) : 0;
			echo '<tr><td><a href="' . esc_url( get_permalink( $pid ) ) . '" target="_blank">' . esc_html( get_the_title( $pid ) ) . '</a></td>';
			foreach ( array_keys( $cols ) as $k ) { echo '<td>' . number_format_i18n( $by[ $pid ][ $k ] ?? 0 ) . '</td>'; }
			echo '<td>' . number_format_i18n( $leads ) . '</td><td>' . number_format_i18n( $due[ $pid ] ?? 0 ) . '</td></tr>';
		}
		echo '</tbody></table>';

		// the listings behind the numbers, for the brokers with traffic
		$top = $wpdb->get_results( $wpdb->prepare( "SELECT pro, post, SUM(ev='view') v, SUM(ev IN ('wa','call','tour')) c FROM {$t['ev']} WHERE day >= %s AND post > 0 GROUP BY pro, post ORDER BY v DESC LIMIT 30", $from ), ARRAY_A );
		if ( $top ) {
			echo '<h2>העמודים שמביאים את התנועה</h2><table class="widefat striped"><thead><tr><th>עמוד</th><th>של</th><th>צפיות</th><th>לחיצות ליצירת קשר</th></tr></thead><tbody>';
			foreach ( $top as $r ) {
				echo '<tr><td><a href="' . esc_url( get_permalink( (int) $r['post'] ) ) . '" target="_blank">' . esc_html( get_the_title( (int) $r['post'] ) ) . '</a></td><td>' . esc_html( get_the_title( (int) $r['pro'] ) ) . '</td><td>' . (int) $r['v'] . '</td><td>' . (int) $r['c'] . '</td></tr>';
			}
			echo '</tbody></table>';
		}

		echo '<h2>יומן עסקאות</h2>';
		echo '<div style="background:#fff8e5;border:1px solid #e0c36a;padding:10px 14px;max-width:760px">לשימוש פנימי בלבד. אחוז מעסקה שנסגרה נחשב בחוק דמי תיווך, ואתר בלי רישיון תיווך לא יכול לגבות אותם. מחיר קבוע לחודש או לפנייה בטוח. לפני גבייה של אחוזים: עורך דין.</div>';
		echo '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '" style="margin:14px 0;display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end">';
		wp_nonce_field( 'nadlan_ledger' );
		echo '<input type="hidden" name="action" value="nadlan_ledger_save">';
		echo '<label>מתווך<br><select name="pro" required>';
		foreach ( $ids as $pid ) { if ( 'nadlan_professional' === get_post_type( $pid ) ) { echo '<option value="' . (int) $pid . '">' . esc_html( get_the_title( $pid ) ) . '</option>'; } }
		echo '</select></label>';
		echo '<label>מזהה הנכס (לא חובה)<br><input type="number" name="post" min="0" style="width:110px"></label>';
		echo '<label>תאריך<br><input type="date" name="deal_date"></label>';
		echo '<label>מחיר העסקה (₪)<br><input type="text" name="deal_price" inputmode="numeric" style="width:130px"></label>';
		echo '<label>הסכום שסוכם איתנו (₪)<br><input type="text" name="amount" inputmode="numeric" style="width:130px"></label>';
		echo '<label>הערה<br><input type="text" name="note" style="width:220px"></label>';
		echo '<button class="button button-primary">הוספה ליומן</button></form>';
		if ( $ledger ) {
			echo '<table class="widefat striped"><thead><tr><th>#</th><th>מתווך</th><th>נכס</th><th>תאריך</th><th>מחיר העסקה</th><th>סוכם</th><th>מצב</th><th>הערה</th><th></th></tr></thead><tbody>';
			foreach ( $ledger as $l ) {
				echo '<tr><td>' . (int) $l['id'] . '</td><td>' . esc_html( get_the_title( (int) $l['pro'] ) ) . '</td><td>' . ( (int) $l['post'] ? esc_html( get_the_title( (int) $l['post'] ) ) : '' ) . '</td><td>' . esc_html( (string) $l['deal_date'] ) . '</td><td>' . ( null !== $l['deal_price'] ? number_format_i18n( (int) $l['deal_price'] ) : '' ) . '</td><td>' . ( null !== $l['amount'] ? number_format_i18n( (int) $l['amount'] ) : '' ) . '</td><td>' . ( 'settled' === $l['status'] ? 'הוסדר' : 'פתוח' ) . '</td><td>' . esc_html( (string) $l['note'] ) . '</td><td>';
				if ( 'open' === $l['status'] ) {
					echo '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '">';
					wp_nonce_field( 'nadlan_ledger' );
					echo '<input type="hidden" name="action" value="nadlan_ledger_save"><input type="hidden" name="id" value="' . (int) $l['id'] . '"><button class="button" name="settle" value="1">סימון כהוסדר</button></form>';
				}
				echo '</td></tr>';
			}
			echo '</tbody></table>';
		}
		echo '</div>';
	}
}
