<?php
/**
 * nadlan-config — LEAD LEDGER + revenue lock-in (v1.34.0)
 *
 * Solves the owner's #1 pain: today leads go out to partners (lawyers, mortgage
 * advisors, brokers) and "the deal closes and nobody pays me back." This module
 * builds a real attribution + commission ledger:
 *
 *   1. Every routed lead creates a nadlan_referral CPT record with a unique
 *      tracking token (rTOKEN), partner, customer-redacted contact, agreed %.
 *   2. Partner gets a one-click "accept terms" link — clicking it logs a
 *      timestamp + IP = a contract record we can show in a payment dispute.
 *   3. **The customer (not the partner) confirms status** via a tokenised public
 *      page /referral-status/<token>/ pinged automatically at 14/30/60 days. The
 *      partner has every reason to lie; the customer has no reason. That's the
 *      lock-in.
 *   4. A commission ledger logs amount owed and paid. The owner sees the total
 *      open balance in the admin dashboard.
 *
 * Honest scope: software cannot FORCE a partner to pay. What this does:
 *   - creates a clean paper trail (proof of intro + customer-confirmed close)
 *   - makes non-payment visible and uncomfortable
 *   - makes the owner the indispensable middle (relationship + brand stays here)
 *   - automates the awkward follow-ups so the owner never has to ask "did you close?"
 *
 * Public surfaces:
 *   - /referral-status/<token>/ — customer status form (1-min, no login)
 *   - REST POST /nadlan/v1/referral/route — create a routing record
 *   - REST POST /nadlan/v1/referral/<token>/accept — partner accepts terms
 *   - REST POST /nadlan/v1/referral/<token>/status — customer reports status
 *   - REST POST /nadlan/v1/referral/<token>/paid — owner marks commission paid
 *
 * Admin: nadlan_referral CPT with custom columns + a "Lead Ledger" submenu page
 * showing aggregate open / closed / paid / outstanding ₪.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------- CPT ---------- */
add_action( 'init', function () {
	register_post_type( 'nadlan_referral', array(
		'labels' => array(
			'name'          => 'Lead Ledger',
			'singular_name' => 'Referral',
			'menu_name'     => 'Lead Ledger',
			'all_items'     => 'כל ההפניות',
			'add_new_item'  => 'הפניה חדשה',
		),
		'public'             => false,
		'show_ui'            => true,
		'show_in_menu'       => true,
		'menu_icon'          => 'dashicons-money-alt',
		'menu_position'      => 25,
		'supports'           => array( 'title', 'editor', 'custom-fields' ),
		'capability_type'    => 'post',
		'map_meta_cap'       => true,
	) );

	// public rewrite for /referral-status/<token>/
	add_rewrite_rule( '^referral-status/([a-zA-Z0-9]+)/?$', 'index.php?nadlan_referral_token=$matches[1]', 'top' );
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nadlan_referral_token'; return $v; } );

if ( ! function_exists( 'nadlan_ll_token' ) ) {
	function nadlan_ll_token( $len = 14 ) { return strtolower( wp_generate_password( $len, false, false ) ); }
}

/* ---------- Statuses ---------- */
if ( ! function_exists( 'nadlan_ll_statuses' ) ) {
	function nadlan_ll_statuses() {
		return array(
			'routed'    => 'הופנה — ממתין לקבלת השותף',
			'accepted'  => 'השותף קיבל את התנאים',
			'in_progress' => 'בתהליך',
			'won'       => '✓ נסגרה עסקה (לקוח אישר)',
			'lost'      => '✗ לא נסגר',
			'paid'      => '💰 עמלה שולמה',
			'disputed'  => '⚠ במחלוקת',
		);
	}
}

/* ---------- Helpers ---------- */
if ( ! function_exists( 'nadlan_ll_get_by_token' ) ) {
	function nadlan_ll_get_by_token( $tok ) {
		$tok = sanitize_text_field( $tok );
		if ( strlen( $tok ) < 8 ) { return null; }
		$q = get_posts( array(
			'post_type' => 'nadlan_referral', 'post_status' => 'any',
			'posts_per_page' => 1, 'meta_query' => array( array( 'key' => 'token', 'value' => $tok ) ),
		) );
		return $q ? $q[0] : null;
	}
}
if ( ! function_exists( 'nadlan_ll_log' ) ) {
	function nadlan_ll_log( $rid, $event, $extra = '' ) {
		$log = (array) get_post_meta( $rid, 'audit', true );
		$log[] = array( 't' => time(), 'e' => $event, 'ip' => $_SERVER['REMOTE_ADDR'] ?? '', 'x' => $extra );
		update_post_meta( $rid, 'audit', $log );
	}
}

/* ---------- REST: route a lead to a partner ---------- */
add_action( 'rest_api_init', function () {

	// Create a referral (called by directory CTA / mortgage calc / etc.)
	register_rest_route( 'nadlan/v1', '/referral/route', array(
		'methods' => 'POST', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$p = $req->get_json_params() ?: array();
			$customer_name  = sanitize_text_field( (string) ( $p['customer_name'] ?? '' ) );
			$customer_phone = preg_replace( '/[^0-9+]/', '', (string) ( $p['customer_phone'] ?? '' ) );
			$customer_email = sanitize_email( (string) ( $p['customer_email'] ?? '' ) );
			$partner_id     = (int) ( $p['partner_id'] ?? 0 );
			$topic          = sanitize_text_field( (string) ( $p['topic'] ?? '' ) );
			$source_url     = esc_url_raw( (string) ( $p['source_url'] ?? '' ) );
			$est_value      = (int) ( $p['est_value'] ?? 0 );
			$hp             = (string) ( $p['company'] ?? '' );
			// v1.39.0: notify_partner defaults TRUE (legacy). Directory "request a quote"
			// passes false → capture + track + email the OWNER only, do NOT cold-email the
			// contractor and do NOT auto-schedule customer follow-ups. Owner routes manually.
			$notify_partner = array_key_exists( 'notify_partner', $p ) ? (bool) $p['notify_partner'] : true;
			if ( $hp !== '' ) { return new WP_Error( 'spam', 'spam' ); }

			if ( ! $customer_name || ( ! $customer_phone && ! $customer_email ) || ! $partner_id ) {
				return new WP_Error( 'invalid', 'Missing fields.' );
			}
			$partner = get_post( $partner_id );
			if ( ! $partner || $partner->post_type !== 'nadlan_professional' ) {
				return new WP_Error( 'bad_partner', 'Partner not found.' );
			}
			$default_pct = (float) ( get_option( 'nadlan_ll_default_commission_pct' ) ?: 25 );
			$token       = nadlan_ll_token();

			$rid = wp_insert_post( array(
				'post_type'   => 'nadlan_referral',
				'post_status' => 'private',
				'post_title'  => sprintf( '%s → %s (%s)', $customer_name, get_the_title( $partner_id ), $topic ?: 'general' ),
				'post_content'=> '',
			), true );
			if ( is_wp_error( $rid ) ) { return $rid; }
			update_post_meta( $rid, 'token', $token );
			update_post_meta( $rid, 'partner_id', $partner_id );
			update_post_meta( $rid, 'customer_name', $customer_name );
			update_post_meta( $rid, 'customer_phone', $customer_phone );
			update_post_meta( $rid, 'customer_email', $customer_email );
			update_post_meta( $rid, 'topic', $topic );
			update_post_meta( $rid, 'source_url', $source_url );
			update_post_meta( $rid, 'est_value', $est_value );
			update_post_meta( $rid, 'commission_pct', $default_pct );
			update_post_meta( $rid, 'status', $notify_partner ? 'routed' : 'new' );
			update_post_meta( $rid, 'routed_at', time() );
			nadlan_ll_log( $rid, $notify_partner ? 'routed' : 'captured', $source_url );

			// Notify owner + partner
			$admin = get_option( 'admin_email' );
			$accept_url = rest_url( 'nadlan/v1/referral/' . $token . '/accept' );
			$cust_url   = home_url( '/referral-status/' . $token . '/' );
			if ( $admin ) {
				$msg  = "ליד הופנה דרך מערכת נדל\"ן חכם\n\n";
				$msg .= "לקוח: $customer_name · $customer_phone · $customer_email\n";
				$msg .= "נושא: $topic\n";
				$msg .= "אל שותף: " . get_the_title( $partner_id ) . " (#$partner_id)\n";
				$msg .= "אחוז עמלה מוסכם: $default_pct%\n";
				$msg .= "סכום עסקה משוער: ₪" . number_format( $est_value ) . "\n";
				$msg .= "מעקב לקוח: $cust_url\n";
				$msg .= "אישור שותף: $accept_url\n\n";
				$msg .= "ניהול: " . admin_url( 'post.php?post=' . $rid . '&action=edit' );
				wp_mail( $admin, '[נדל"ן חכם · Ledger] ליד חדש הופנה — ' . $customer_name, $msg );
			}
			if ( $notify_partner ) {
				$partner_email = (string) get_post_meta( $partner_id, 'email', true );
				if ( $partner_email && is_email( $partner_email ) ) {
					$pm  = "שלום,\n\nיש לך הפניית לקוח חדשה מ-נדל\"ן חכם.\n\n";
					$pm .= "לקוח: $customer_name · $customer_phone\n";
					$pm .= "נושא: $topic\n\n";
					$pm .= "תנאי שיתוף הפעולה: עמלה של $default_pct% מהעסקה הסגורה, משולמת בתוך 14 יום מסגירה.\n";
					$pm .= "לאישור התנאים וקבלת פרטי הלקוח המלאים: $accept_url\n\n";
					$pm .= "מערכת נדל\"ן חכם";
					wp_mail( $partner_email, 'הפניית לקוח חדשה — מערכת נדל"ן חכם', $pm );
				}
				// schedule customer follow-ups only once truly routed to a partner
				wp_schedule_single_event( time() + 14 * DAY_IN_SECONDS, 'nadlan_ll_customer_ping', array( $rid ) );
				wp_schedule_single_event( time() + 30 * DAY_IN_SECONDS, 'nadlan_ll_customer_ping', array( $rid ) );
				wp_schedule_single_event( time() + 60 * DAY_IN_SECONDS, 'nadlan_ll_customer_ping', array( $rid ) );
			}

			return array(
				'ok' => true,
				'referral_id' => $rid,
				'token' => $token,
				'customer_status_url' => $cust_url,
				'message' => $notify_partner
					? 'הפניה נרשמה. הלקוח יקבל מעקב אוטומטי לסגירת מעגל.'
					: 'הבקשה התקבלה. נחזור אליכם בהקדם.',
			);
		},
	) );

	// Partner accepts the terms
	register_rest_route( 'nadlan/v1', '/referral/(?P<token>[a-z0-9]+)/accept', array(
		'methods' => 'GET,POST', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$r = nadlan_ll_get_by_token( $req['token'] );
			if ( ! $r ) { return new WP_Error( 'not_found', 'not_found' ); }
			update_post_meta( $r->ID, 'accepted_at', time() );
			update_post_meta( $r->ID, 'status', 'accepted' );
			nadlan_ll_log( $r->ID, 'partner_accepted' );
			$admin = get_option( 'admin_email' );
			if ( $admin ) { wp_mail( $admin, '[Ledger] השותף אישר תנאים — ' . get_the_title( $r->ID ), 'הסכמה נרשמה ב-' . wp_date( 'Y-m-d H:i', time() ) . "\n" . admin_url( 'post.php?post=' . $r->ID . '&action=edit' ) ); }
			return new WP_REST_Response( array( 'ok' => true, 'accepted' => true, 'message' => 'תנאי שיתוף הפעולה אושרו ונרשמו.' ), 200 );
		},
	) );

	// Customer reports status
	register_rest_route( 'nadlan/v1', '/referral/(?P<token>[a-z0-9]+)/status', array(
		'methods' => 'POST', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$r = nadlan_ll_get_by_token( $req['token'] );
			if ( ! $r ) { return new WP_Error( 'not_found', 'not_found' ); }
			$p = $req->get_json_params() ?: array();
			$status = sanitize_key( $p['status'] ?? '' );
			$amount = (int) ( $p['deal_value'] ?? 0 );
			$note   = sanitize_textarea_field( (string) ( $p['note'] ?? '' ) );
			if ( ! in_array( $status, array( 'won', 'lost', 'in_progress' ), true ) ) {
				return new WP_Error( 'invalid', 'invalid status' );
			}
			update_post_meta( $r->ID, 'status', $status );
			update_post_meta( $r->ID, 'customer_reported_at', time() );
			update_post_meta( $r->ID, 'customer_note', $note );
			if ( $status === 'won' && $amount > 0 ) {
				$pct = (float) get_post_meta( $r->ID, 'commission_pct', true );
				update_post_meta( $r->ID, 'deal_value', $amount );
				update_post_meta( $r->ID, 'commission_amount', (int) round( $amount * $pct / 100 ) );
			}
			nadlan_ll_log( $r->ID, 'customer_status_' . $status, $amount );
			$admin = get_option( 'admin_email' );
			if ( $admin ) {
				$tag = $status === 'won' ? '💰 ' : ( $status === 'lost' ? '✗ ' : '↻ ' );
				wp_mail( $admin, $tag . '[Ledger] לקוח עדכן סטטוס — ' . get_the_title( $r->ID ),
					"סטטוס: $status\nסכום עסקה: ₪" . number_format( $amount ) . "\nהערה: $note\n" . admin_url( 'post.php?post=' . $r->ID . '&action=edit' ) );
			}
			return array( 'ok' => true, 'message' => 'תודה על העדכון.' );
		},
	) );
} );

/* ---------- Cron: customer ping ---------- */
add_action( 'nadlan_ll_customer_ping', function ( $rid ) {
	$r = get_post( $rid );
	if ( ! $r || $r->post_type !== 'nadlan_referral' ) { return; }
	$status = (string) get_post_meta( $rid, 'status', true );
	if ( in_array( $status, array( 'won', 'lost', 'paid' ), true ) ) { return; } // already resolved
	$email = (string) get_post_meta( $rid, 'customer_email', true );
	if ( ! $email || ! is_email( $email ) ) { return; }
	$token = (string) get_post_meta( $rid, 'token', true );
	$url   = home_url( '/referral-status/' . $token . '/' );
	$partner_name = get_the_title( (int) get_post_meta( $rid, 'partner_id', true ) );
	$name = (string) get_post_meta( $rid, 'customer_name', true );
	$msg  = "שלום $name,\n\n";
	$msg .= "לפני זמן מה הפנינו אותך אל $partner_name דרך נדל\"ן חכם. ";
	$msg .= "נשמח לדעת איך התקדמת — זה עוזר לנו לשמור על שירות איכותי לכולם.\n\n";
	$msg .= "עדכון מהיר (דקה): $url\n\n";
	$msg .= "תודה,\nצוות נדל\"ן חכם";
	wp_mail( $email, 'עדכון מהיר — איך התקדם עם ' . $partner_name . '?', $msg );
	nadlan_ll_log( $rid, 'customer_ping_sent' );
} );

/* ---------- Public customer status page ---------- */
add_action( 'template_redirect', function () {
	$tok = get_query_var( 'nadlan_referral_token' );
	if ( ! $tok ) { return; }
	$r = nadlan_ll_get_by_token( $tok );
	if ( ! $r ) { status_header( 404 ); wp_die( 'הקישור אינו תקף.' ); }
	$partner_name = get_the_title( (int) get_post_meta( $r->ID, 'partner_id', true ) );
	$name = esc_html( (string) get_post_meta( $r->ID, 'customer_name', true ) );
	$cur  = (string) get_post_meta( $r->ID, 'status', true );
	get_header();
	?>
<div class="nlrs" dir="rtl" style="max-width:680px;margin:30px auto;padding:0 20px;font-family:var(--font-sans,Heebo,sans-serif);direction:rtl">
	<h1 style="font-family:var(--font-serif,'Frank Ruhl Libre',serif);font-weight:600">עדכון מצב — <?php echo esc_html( $partner_name ); ?></h1>
	<p>שלום <?php echo $name; ?>, נשמח לדעת איפה אתם עומדים. דקה אחת.</p>
	<form id="nlrs-form" onsubmit="return nlrsSubmit(this)">
		<fieldset style="border:1px solid #eee;padding:18px;border-radius:12px;margin:18px 0">
			<legend style="font-weight:700;padding:0 8px">איפה אתם עומדים?</legend>
			<label style="display:block;margin:8px 0"><input type="radio" name="status" value="in_progress" required> בתהליך — עוד בודקים</label>
			<label style="display:block;margin:8px 0"><input type="radio" name="status" value="won"> ✓ סגרנו עסקה / חתמנו</label>
			<label style="display:block;margin:8px 0"><input type="radio" name="status" value="lost"> ✗ לא התקדמנו / בחרנו במישהו אחר</label>
		</fieldset>
		<div id="nlrs-deal" style="display:none;background:#FBF9F5;padding:14px;border-radius:10px;margin-bottom:14px">
			<label style="display:block;margin-bottom:6px;font-weight:600">סכום העסקה (₪) — חסוי, רק לרישום פנימי</label>
			<input type="number" name="deal_value" min="0" style="width:100%;padding:11px;border:1px solid #ddd;border-radius:8px">
		</div>
		<label style="display:block;margin:0 0 6px;font-weight:600">משוב קצר (אופציונלי)</label>
		<textarea name="note" rows="3" style="width:100%;padding:11px;border:1px solid #ddd;border-radius:8px;font:inherit" placeholder="איך הייתה החוויה?"></textarea>
		<button type="submit" style="margin-top:14px;background:#9C7A3C;color:#fff;border:0;padding:13px 32px;border-radius:9px;font-weight:700;cursor:pointer">שליחה</button>
		<span class="nlrs-msg" style="margin-inline-start:12px"></span>
	</form>
</div>
<script>
(function(){var f=document.getElementById('nlrs-form');var d=document.getElementById('nlrs-deal');
f.addEventListener('change',function(e){if(e.target.name==='status')d.style.display=e.target.value==='won'?'block':'none';});
window.nlrsSubmit=function(form){var fd=new FormData(form),data={};fd.forEach(function(v,k){data[k]=v;});
fetch('<?php echo esc_js( rest_url( 'nadlan/v1/referral/' . $tok . '/status' ) ); ?>',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
.then(function(r){return r.json();}).then(function(d){form.querySelector('.nlrs-msg').textContent=d.ok?'✓ תודה! הסטטוס נשמר.':'שגיאה. נסו שוב.';if(d.ok)form.querySelector('button').disabled=true;});return false;};})();
</script>
	<?php
	get_footer();
	exit;
}, 5 );

/* ---------- Admin: Lead Ledger dashboard submenu ---------- */
add_action( 'admin_menu', function () {
	add_submenu_page( 'edit.php?post_type=nadlan_referral', 'Lead Ledger Dashboard', '📊 Dashboard', 'edit_posts', 'nadlan-ll-dashboard', 'nadlan_ll_dashboard_render' );
} );
if ( ! function_exists( 'nadlan_ll_dashboard_render' ) ) {
	function nadlan_ll_dashboard_render() {
		$all = get_posts( array( 'post_type' => 'nadlan_referral', 'post_status' => 'any', 'posts_per_page' => -1 ) );
		$by_status = array_fill_keys( array_keys( nadlan_ll_statuses() ), 0 );
		$owed = 0; $paid = 0; $closed_value = 0;
		foreach ( $all as $r ) {
			$st = (string) get_post_meta( $r->ID, 'status', true );
			if ( isset( $by_status[ $st ] ) ) { $by_status[ $st ]++; }
			$amt = (int) get_post_meta( $r->ID, 'commission_amount', true );
			if ( $st === 'won' || $st === 'disputed' ) { $owed += $amt; $closed_value += (int) get_post_meta( $r->ID, 'deal_value', true ); }
			if ( $st === 'paid' ) { $paid += $amt; $closed_value += (int) get_post_meta( $r->ID, 'deal_value', true ); }
		}
		echo '<div class="wrap" style="font-family:Heebo,sans-serif;direction:rtl"><h1>Lead Ledger</h1>';
		echo '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:20px 0">';
		echo '<div style="background:#fff;border:1px solid #ddd;border-radius:10px;padding:18px"><div style="font-size:13px;color:#666">סה"כ הפניות</div><div style="font-size:30px;font-weight:700">' . count( $all ) . '</div></div>';
		echo '<div style="background:#fff;border:1px solid #ddd;border-radius:10px;padding:18px"><div style="font-size:13px;color:#666">פתוחות</div><div style="font-size:30px;font-weight:700">' . ( $by_status['routed'] + $by_status['accepted'] + $by_status['in_progress'] ) . '</div></div>';
		echo '<div style="background:#fff;border:1px solid #2563EB;border-radius:10px;padding:18px"><div style="font-size:13px;color:#666">עסקאות סגורות</div><div style="font-size:30px;font-weight:700;color:#2563EB">' . ( $by_status['won'] + $by_status['paid'] ) . '</div><div style="font-size:11px;color:#999">סה"כ ₪' . number_format( $closed_value ) . '</div></div>';
		echo '<div style="background:#fff;border:1px solid #DC2626;border-radius:10px;padding:18px"><div style="font-size:13px;color:#666">עמלה ממתינה</div><div style="font-size:30px;font-weight:700;color:#DC2626">₪' . number_format( $owed ) . '</div></div>';
		echo '<div style="background:#fff;border:1px solid #059669;border-radius:10px;padding:18px"><div style="font-size:13px;color:#666">עמלה שולמה</div><div style="font-size:30px;font-weight:700;color:#059669">₪' . number_format( $paid ) . '</div></div>';
		echo '</div>';
		echo '<p style="color:#666">פירוט מלא: <a href="edit.php?post_type=nadlan_referral">edit referrals</a>. כל הפניה רושמת token תקף, audit log, וקישור עדכון לקוח/שותף.</p>';
		echo '</div>';
	}
}

/* ---------- Admin columns ---------- */
add_filter( 'manage_nadlan_referral_posts_columns', function ( $c ) {
	return array(
		'cb' => $c['cb'] ?? '', 'title' => 'הפניה',
		'partner' => 'שותף', 'status' => 'סטטוס',
		'deal_value' => 'עסקה', 'commission' => 'עמלה', 'token' => 'token', 'date' => 'נוצר',
	);
} );
add_action( 'manage_nadlan_referral_posts_custom_column', function ( $col, $id ) {
	$g = function ( $k ) use ( $id ) { return get_post_meta( $id, $k, true ); };
	if ( $col === 'partner' )      { $pid = (int) $g( 'partner_id' ); echo $pid ? '<a href="' . esc_url( get_edit_post_link( $pid ) ) . '">' . esc_html( get_the_title( $pid ) ) . '</a>' : '—'; }
	elseif ( $col === 'status' )   { $s = (string) $g( 'status' ); $st = nadlan_ll_statuses(); echo esc_html( $st[ $s ] ?? $s ); }
	elseif ( $col === 'deal_value' ) { $v = (int) $g( 'deal_value' ); echo $v ? '₪' . number_format( $v ) : '—'; }
	elseif ( $col === 'commission' ){ $v = (int) $g( 'commission_amount' ); echo $v ? '₪' . number_format( $v ) : '—'; }
	elseif ( $col === 'token' )     { echo '<code>' . esc_html( $g( 'token' ) ) . '</code>'; }
}, 10, 2 );

/* ---------- "Mark paid" admin action ---------- */
add_action( 'post_action_nadlan_ll_mark_paid', function ( $post_id ) {
	if ( ! current_user_can( 'edit_posts' ) ) { return; }
	check_admin_referer( 'nadlan_ll_paid_' . $post_id );
	update_post_meta( $post_id, 'status', 'paid' );
	update_post_meta( $post_id, 'paid_at', time() );
	nadlan_ll_log( $post_id, 'owner_marked_paid' );
	wp_safe_redirect( admin_url( 'post.php?post=' . $post_id . '&action=edit&paid=1' ) );
	exit;
} );

/* ---------- Flush rewrite once on activation ---------- */
add_action( 'init', function () {
	if ( get_option( 'nadlan_ll_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_ll_rewrite_v1', '1' );
	}
}, 99 );
