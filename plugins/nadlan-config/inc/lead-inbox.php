<?php
/**
 * nadlan-config — Unified Lead Inbox + Owner Daily Digest (v1.40.0 / shark #3, #4)
 *
 * ONE admin page for every money signal:
 *   - new nadlan_lead (general lead capture, CTA bar, exit-intent, concierge)
 *   - new nadlan_referral (Lead Ledger, status=new = captured but not routed)
 *   - new nadlan_review (pending moderation)
 *   - new nadlan_claim (pending owner approval)
 *   - new Pro/Premier upgrades (WooCommerce paid orders for products 476/477/489)
 *
 * Plus a daily CRON email digest to the owner summarising the last 24h.
 * The owner stops checking 5 places — everything is in ONE inbox under
 * the menu "💰 Lead Inbox", count badge shows pending items.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_inbox_counts' ) ) {
	function nadlan_inbox_counts() {
		$out = array(
			'leads_24h' => 0,
			'referrals_open' => 0,
			'reviews_pending' => 0,
			'claims_pending' => 0,
			'paid_24h' => 0,
		);
		$out['leads_24h']      = (int) ( new WP_Query( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids', 'date_query' => array( array( 'after' => '24 hours ago' ) ) ) ) )->found_posts;
		$out['referrals_open'] = (int) ( new WP_Query( array( 'post_type' => 'nadlan_referral', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids', 'meta_query' => array( array( 'key' => 'status', 'value' => array( 'new', 'routed', 'accepted', 'in_progress' ), 'compare' => 'IN' ) ) ) ) )->found_posts;
		$out['reviews_pending']= (int) ( new WP_Query( array( 'post_type' => 'nadlan_review', 'post_status' => 'pending', 'posts_per_page' => 1, 'fields' => 'ids' ) ) )->found_posts;
		if ( post_type_exists( 'nadlan_claim' ) ) {
			$out['claims_pending'] = (int) ( new WP_Query( array( 'post_type' => 'nadlan_claim', 'post_status' => 'pending', 'posts_per_page' => 1, 'fields' => 'ids' ) ) )->found_posts;
		}
		// Woo paid orders in last 24h for our paid products
		if ( function_exists( 'wc_get_orders' ) ) {
			$orders = wc_get_orders( array(
				'status' => array( 'completed', 'processing' ),
				'date_created' => '>' . ( time() - DAY_IN_SECONDS ),
				'limit' => 50,
			) );
			$paid_ids = array( 476, 477, 489, 490 );
			foreach ( (array) $orders as $o ) {
				foreach ( $o->get_items() as $it ) {
					if ( in_array( (int) $it->get_product_id(), $paid_ids, true ) ) { $out['paid_24h']++; break; }
				}
			}
		}
		return $out;
	}
}

/* ---------- Admin menu + count badge ---------- */
add_action( 'admin_menu', function () {
	$c = nadlan_inbox_counts();
	$total = $c['referrals_open'] + $c['reviews_pending'] + $c['claims_pending'];
	$bubble = $total > 0 ? ' <span class="awaiting-mod">' . $total . '</span>' : '';
	add_menu_page( 'Lead Inbox', '💰 Lead Inbox' . $bubble, 'edit_posts', 'nadlan-inbox', 'nadlan_inbox_render', 'dashicons-email-alt', 2 );
}, 9 );

if ( ! function_exists( 'nadlan_inbox_render' ) ) {
	function nadlan_inbox_render() {
		$c = nadlan_inbox_counts();
		?>
<div class="wrap" style="direction:rtl;font-family:Heebo,sans-serif"><h1>💰 Lead Inbox — סקירת הכנסות 24h</h1>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:20px 0">
	<?php
	$cards = array(
		array( 'לידים חדשים (24h)', $c['leads_24h'], 'edit.php?post_type=nadlan_lead', '#2563EB' ),
		array( 'הפניות פתוחות', $c['referrals_open'], 'edit.php?post_type=nadlan_referral', '#9C7A3C' ),
		array( 'חוות דעת לאישור', $c['reviews_pending'], 'edit.php?post_status=pending&post_type=nadlan_review', '#F5A623' ),
		array( 'בקשות בעלות', $c['claims_pending'], post_type_exists( 'nadlan_claim' ) ? 'edit.php?post_status=pending&post_type=nadlan_claim' : '#', '#7C3AED' ),
		array( '💰 תשלומים (24h)', $c['paid_24h'], 'edit.php?post_type=shop_order', '#059669' ),
	);
	foreach ( $cards as $card ) {
		echo '<a href="' . esc_url( admin_url( $card[2] ) ) . '" style="background:#fff;border:1px solid #ddd;border-top:4px solid ' . esc_attr( $card[3] ) . ';border-radius:10px;padding:18px;text-decoration:none;color:inherit;display:block;transition:transform .15s,box-shadow .15s" onmouseover="this.style.transform=\'translateY(-3px)\';this.style.boxShadow=\'0 8px 20px rgba(0,0,0,.08)\'" onmouseout="this.style.transform=\'none\';this.style.boxShadow=\'none\'">';
		echo '<div style="font-size:13px;color:#666;margin-bottom:6px">' . esc_html( $card[0] ) . '</div>';
		echo '<div style="font-size:34px;font-weight:700;color:' . esc_attr( $card[3] ) . '">' . (int) $card[1] . '</div>';
		echo '</a>';
	}
	?>
</div>

<h2 style="margin-top:30px">פעולות מהירות</h2>
<div style="display:flex;gap:10px;flex-wrap:wrap">
	<a href="<?php echo esc_url( admin_url( 'edit.php?post_type=nadlan_referral' ) ); ?>" class="button button-primary">ניהול Lead Ledger</a>
	<a href="<?php echo esc_url( admin_url( 'edit.php?post_status=pending&post_type=nadlan_review' ) ); ?>" class="button">אישור חוות דעת</a>
	<a href="<?php echo esc_url( admin_url( 'admin.php?page=nadlan-partners' ) ); ?>" class="button">שותפים מועדפים</a>
	<a href="<?php echo esc_url( admin_url( 'options-general.php?page=nadlan-cta' ) ); ?>" class="button">הגדרות CTA + WhatsApp</a>
	<a href="<?php echo esc_url( admin_url( 'options-general.php?page=nadlan-ai' ) ); ?>" class="button">AI Concierge</a>
</div>

<h2 style="margin-top:30px">10 הלידים האחרונים</h2>
<table class="widefat striped"><thead><tr><th>תאריך</th><th>שם</th><th>טלפון</th><th>נושא</th><th>מקור</th><th></th></tr></thead><tbody>
<?php
$recent = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'posts_per_page' => 10 ) );
foreach ( $recent as $l ) {
	$ph = get_post_meta( $l->ID, 'phone', true );
	$gl = get_post_meta( $l->ID, 'goal', true );
	$src= get_post_meta( $l->ID, 'utm_source', true ) ?: get_post_meta( $l->ID, 'source_url', true );
	echo '<tr><td>' . esc_html( get_the_date( 'd/m H:i', $l ) ) . '</td>';
	echo '<td>' . esc_html( get_post_meta( $l->ID, 'name', true ) ) . '</td>';
	echo '<td>' . esc_html( $ph ) . '</td>';
	echo '<td>' . esc_html( $gl ) . '</td>';
	echo '<td><small>' . esc_html( $src ) . '</small></td>';
	echo '<td><a href="' . esc_url( get_edit_post_link( $l->ID ) ) . '">פתח →</a></td></tr>';
}
if ( ! $recent ) {
	$empty = function_exists( 'nadlan_help_empty_state' ) ? nadlan_help_empty_state( 'toplevel_page_nadlan-inbox', 'recent_leads_empty' ) : '';
	echo '<tr><td colspan="6">' . ( $empty ? $empty : esc_html( 'אין לידים עדיין' ) ) . '</td></tr>';
}
?>
</tbody></table>
</div>
		<?php
	}
}

/* ---------- Daily digest CRON ---------- */
add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'nadlan_inbox_daily_digest' ) ) {
		// daily at 08:00 site-local
		wp_schedule_event( strtotime( 'tomorrow 08:00' ), 'daily', 'nadlan_inbox_daily_digest' );
	}
} );
add_action( 'nadlan_inbox_daily_digest', function () {
	$admin = get_option( 'admin_email' );
	if ( ! $admin ) { return; }
	$c = nadlan_inbox_counts();
	$body  = "סיכום יומי — נדל\"ן חכם · " . wp_date( 'd/m/Y' ) . "\n\n";
	$body .= "📥 לידים חדשים ב-24h:        " . $c['leads_24h'] . "\n";
	$body .= "🤝 הפניות פתוחות:            " . $c['referrals_open'] . "\n";
	$body .= "⭐ חוות דעת לאישור:          " . $c['reviews_pending'] . "\n";
	$body .= "📝 בקשות בעלות:               " . $c['claims_pending'] . "\n";
	$body .= "💰 רכישות פייד ב-24h:        " . $c['paid_24h'] . "\n\n";
	$body .= "כניסה ל-Inbox: " . admin_url( 'admin.php?page=nadlan-inbox' ) . "\n\n";
	$body .= "מערכת נדל\"ן חכם · אוטומטי";
	wp_mail( $admin, '🦈 סיכום יומי נדל"ן חכם · ' . wp_date( 'd/m' ), $body );
} );

/* Admin notice banner when there are pending items (visible on every wp-admin page) */
add_action( 'admin_notices', function () {
	if ( ! current_user_can( 'edit_posts' ) ) { return; }
	$c = nadlan_inbox_counts();
	$total = $c['referrals_open'] + $c['reviews_pending'] + $c['claims_pending'];
	if ( $total < 1 ) { return; }
	echo '<div class="notice notice-info" style="direction:rtl"><p>💰 <strong>Lead Inbox:</strong> יש לך <strong>' . (int) $total . '</strong> פעולות ממתינות. <a href="' . esc_url( admin_url( 'admin.php?page=nadlan-inbox' ) ) . '">פתח את ה-Inbox →</a></p></div>';
} );
