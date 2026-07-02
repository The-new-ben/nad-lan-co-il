<?php
/**
 * nadlan-config — Advertiser Center (v1.41.2)
 *
 * A customer-facing command center for claimed professionals, project advertisers,
 * and promoted property owners. It closes the post-payment gap by giving every
 * logged-in advertiser one place for owned cards, completion checks, views,
 * inquiries, reviews, recent orders, Studio edit links, and upgrade paths.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ac_products' ) ) {
	function nadlan_ac_products() {
		return array(
			476 => array( 'label' => 'Pro', 'price' => '₪349', 'type' => 'professional', 'href' => home_url( '/?add-to-cart=476&ref=advertiser-center' ) ),
			477 => array( 'label' => 'Premier', 'price' => '₪749', 'type' => 'professional', 'href' => home_url( '/?add-to-cart=477&ref=advertiser-center' ) ),
			489 => array( 'label' => 'קמפיין פרויקט', 'price' => '₪3,990', 'type' => 'project', 'href' => home_url( '/?add-to-cart=489&ref=advertiser-center' ) ),
			490 => array( 'label' => 'מודעה מקודמת לנכס', 'price' => '₪299', 'type' => 'property', 'href' => home_url( '/?add-to-cart=490&ref=advertiser-center' ) ),
		);
	}
}

add_action( 'init', function () {
	add_rewrite_rule( '^advertiser-center/?$', 'index.php?nadlan_advertiser_center=1', 'top' );
	add_rewrite_rule( '^advertiser-dashboard/?$', 'index.php?nadlan_advertiser_center=1', 'top' );
} );
add_filter( 'query_vars', function ( $vars ) {
	$vars[] = 'nadlan_advertiser_center';
	return $vars;
} );

add_action( 'init', function () {
	if ( get_option( 'nadlan_advertiser_center_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_advertiser_center_rewrite_v1', '1' );
	}
}, 99 );

add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_advertiser_center' ) ) { return; }
	if ( ! is_user_logged_in() ) {
		wp_safe_redirect( wp_login_url( home_url( '/advertiser-center/' ) ) );
		exit;
	}
	nadlan_ac_render_page();
	exit;
}, 7 );

add_shortcode( 'nadlan_advertiser_center', function () {
	if ( ! is_user_logged_in() ) {
		return '<div class="nadlan-ac-login" dir="rtl"><a href="' . esc_url( wp_login_url( home_url( '/advertiser-center/' ) ) ) . '">כניסה למרכז הפרסום</a></div>';
	}
	return nadlan_ac_render_inner();
} );

if ( ! function_exists( 'nadlan_ac_owned_cards' ) ) {
	function nadlan_ac_owned_cards( $user_id ) {
		$args = array(
			'post_type'      => array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ),
			'post_status'    => array( 'publish', 'pending', 'draft', 'private' ),
			'posts_per_page' => 50,
			'orderby'        => 'modified',
			'order'          => 'DESC',
			'meta_query'     => array( array( 'key' => 'owner_user_id', 'value' => (int) $user_id ) ),
		);
		$q = new WP_Query( $args );
		$cards = $q->posts;
		wp_reset_postdata();

		if ( ! $cards && current_user_can( 'manage_options' ) && isset( $_GET['all'] ) && $_GET['all'] === '1' ) {
			$q = new WP_Query( array(
				'post_type'      => array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ),
				'post_status'    => array( 'publish', 'pending', 'draft' ),
				'posts_per_page' => 24,
				'orderby'        => 'modified',
				'order'          => 'DESC',
			) );
			$cards = $q->posts;
			wp_reset_postdata();
		}
		return $cards;
	}
}

if ( ! function_exists( 'nadlan_ac_card_type_label' ) ) {
	function nadlan_ac_card_type_label( $type ) {
		$labels = array(
			'nadlan_professional' => 'כרטיס בעל מקצוע',
			'nadlan_project'      => 'כרטיס פרויקט',
			'nadlan_property'     => 'מודעת נכס',
		);
		return isset( $labels[ $type ] ) ? $labels[ $type ] : $type;
	}
}

if ( ! function_exists( 'nadlan_ac_photos' ) ) {
	function nadlan_ac_photos( $post_id ) {
		$photos = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $post_id, 'photos_csv', true ) ) ) );
		if ( has_post_thumbnail( $post_id ) ) {
			array_unshift( $photos, (string) get_the_post_thumbnail_url( $post_id, 'medium' ) );
		}
		return array_values( array_unique( array_filter( $photos ) ) );
	}
}

if ( ! function_exists( 'nadlan_ac_completion' ) ) {
	function nadlan_ac_completion( $post_id ) {
		$post = get_post( $post_id );
		if ( ! $post ) { return array( 'score' => 0, 'done' => array(), 'missing' => array() ); }
		$photos = nadlan_ac_photos( $post_id );
		$desc = (string) get_post_meta( $post_id, 'description', true );
		if ( $desc === '' ) { $desc = wp_strip_all_tags( (string) $post->post_content ); }
		$checks = array(
			'שם ברור'       => trim( get_the_title( $post_id ) ) !== '',
			'תיאור איכותי'  => function_exists( 'mb_strlen' ) ? mb_strlen( $desc ) >= 80 : strlen( $desc ) >= 80,
			'עיר או כתובת'  => (string) get_post_meta( $post_id, 'city', true ) !== '' || (string) get_post_meta( $post_id, 'address', true ) !== '',
			'טלפון או אימייל' => (string) get_post_meta( $post_id, 'phone', true ) !== '' || (string) get_post_meta( $post_id, 'email', true ) !== '',
			'תמונות'        => count( $photos ) > 0,
			'מפה'           => (string) get_post_meta( $post_id, 'lat', true ) !== '' && (string) get_post_meta( $post_id, 'lng', true ) !== '',
			'וידאו או סיור' => (string) get_post_meta( $post_id, 'video_url', true ) !== '' || (string) get_post_meta( $post_id, 'tour_url', true ) !== '',
			'בעלות מאומתת' => (string) get_post_meta( $post_id, 'claim_status', true ) === 'verified',
		);
		if ( get_post_type( $post_id ) === 'nadlan_project' ) {
			$checks['פרטי יזם'] = (string) get_post_meta( $post_id, 'developer_name', true ) !== '';
			$checks['סטטוס פרויקט'] = (string) get_post_meta( $post_id, 'project_status', true ) !== '';
		}
		$done = array();
		$missing = array();
		foreach ( $checks as $label => $ok ) {
			if ( $ok ) { $done[] = $label; } else { $missing[] = $label; }
		}
		$score = $checks ? (int) round( count( $done ) * 100 / count( $checks ) ) : 0;
		return array( 'score' => $score, 'done' => $done, 'missing' => $missing );
	}
}

if ( ! function_exists( 'nadlan_ac_lead_count' ) ) {
	function nadlan_ac_lead_count( $post_id ) {
		$post_id = (int) $post_id;
		if ( ! $post_id ) { return 0; }
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_lead',
			'post_status'    => 'any',
			'posts_per_page' => 1,
			'fields'         => 'ids',
			'meta_query'     => array(
				array(
					'key'     => 'lead_card_id',
					'value'   => $post_id,
					'compare' => '=',
					'type'    => 'NUMERIC',
				),
			),
		) );
		$count = (int) $q->found_posts;
		wp_reset_postdata();
		return $count;
	}
}

if ( ! function_exists( 'nadlan_ac_recent_leads' ) ) {
	function nadlan_ac_recent_leads( $cards, $limit = 12 ) {
		$card_ids = array();
		$user_id = (int) apply_filters( 'nadlan_effective_user_id', get_current_user_id() );
		$paid_tiers = function_exists( 'nadlan_lead_route_paid_tiers' ) ? nadlan_lead_route_paid_tiers() : array( 'pro', 'premier' );
		foreach ( (array) $cards as $card ) {
			if ( is_object( $card ) && ! empty( $card->ID ) ) {
				$owner_id = (int) get_post_meta( (int) $card->ID, 'owner_user_id', true );
				if ( $owner_id !== (int) $user_id && ! current_user_can( 'manage_options' ) ) {
					continue;
				}
				$tier = (string) get_post_meta( (int) $card->ID, 'paid_tier', true );
				if ( in_array( $tier, $paid_tiers, true ) ) {
					$card_ids[] = (int) $card->ID;
				}
			}
		}
		$card_ids = array_values( array_unique( array_filter( $card_ids ) ) );
		if ( ! $card_ids ) { return array(); }
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_lead',
			'post_status'    => 'any',
			'posts_per_page' => max( 1, (int) $limit ),
			'orderby'        => 'date',
			'order'          => 'DESC',
			'meta_query'     => array(
				array(
					'key'     => 'lead_card_id',
					'value'   => $card_ids,
					'compare' => 'IN',
					'type'    => 'NUMERIC',
				),
			),
		) );
		$allowed = array_fill_keys( $card_ids, true );
		$leads = array();
		foreach ( (array) $q->posts as $lead ) {
			$lead_card_id = (int) get_post_meta( (int) $lead->ID, 'lead_card_id', true );
			if ( ! isset( $allowed[ $lead_card_id ] ) ) { continue; }
			$owner_id = (int) get_post_meta( $lead_card_id, 'owner_user_id', true );
			if ( $owner_id !== (int) $user_id && ! current_user_can( 'manage_options' ) ) { continue; }
			$tier = (string) get_post_meta( $lead_card_id, 'paid_tier', true );
			if ( ! in_array( $tier, $paid_tiers, true ) ) { continue; }
			$leads[] = $lead;
		}
		wp_reset_postdata();
		return $leads;
	}
}

if ( ! function_exists( 'nadlan_ac_lead_status_label' ) ) {
	function nadlan_ac_lead_status_label( $lead_id ) {
		if ( function_exists( 'nadlan_lead_e2e_enabled' ) && nadlan_lead_e2e_enabled() && function_exists( 'nadlan_lead_e2e_status_label' ) ) {
			$workflow_status = (string) get_post_meta( (int) $lead_id, 'lead_status', true );
			if ( $workflow_status !== '' ) {
				return nadlan_lead_e2e_status_label( $workflow_status );
			}
		}
		$status = (string) get_post_meta( (int) $lead_id, 'lead_route_status', true );
		$labels = array(
			'delivered_owner' => 'נמסרה אליכם',
			'fallback_admin'  => 'בטיפול האתר',
			'skipped_self'    => 'בדיקת בעלות',
			'failed_email'    => 'בדיקה נדרשת',
		);
		return isset( $labels[ $status ] ) ? $labels[ $status ] : 'נקלטה';
	}
}

if ( ! function_exists( 'nadlan_ac_orders' ) ) {
	function nadlan_ac_orders( $user_id, $limit = 5 ) {
		if ( ! function_exists( 'wc_get_orders' ) ) { return array(); }
		return wc_get_orders( array(
			'customer_id' => (int) $user_id,
			'limit'       => (int) $limit,
			'orderby'     => 'date',
			'order'       => 'DESC',
			'status'      => array( 'pending', 'processing', 'completed', 'on-hold' ),
		) );
	}
}

if ( ! function_exists( 'nadlan_ac_order_has_paid_product' ) ) {
	function nadlan_ac_order_has_paid_product( $order ) {
		if ( ! $order ) { return false; }
		$ids = array_keys( nadlan_ac_products() );
		foreach ( $order->get_items() as $item ) {
			if ( in_array( (int) $item->get_product_id(), $ids, true ) ) { return true; }
		}
		return false;
	}
}

if ( ! function_exists( 'nadlan_ac_css' ) ) {
	function nadlan_ac_css() {
		return '<style>
.nlac{font-family:var(--font-sans,Heebo,Arial,sans-serif);direction:rtl;color:#1B1A17;max-width:1180px;margin:0 auto;padding:28px 20px 52px}
.nlac a{color:inherit}.nlac-hero{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(260px,.6fr);gap:22px;align-items:end;border-bottom:1px solid rgba(27,26,23,.12);padding-bottom:22px;margin-bottom:22px}
.nlac-kicker{font-size:12px;color:#8A6B2F;font-weight:800;margin-bottom:8px}.nlac h1{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:clamp(30px,4vw,52px);line-height:1.05;margin:0 0 10px;letter-spacing:0}
.nlac-hero p{font-size:16px;line-height:1.65;color:#5A5A5A;margin:0;max-width:760px}.nlac-actions{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end}
.nlac-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;border:1px solid #1B1A17;background:#1B1A17;color:#fff;text-decoration:none;border-radius:6px;padding:11px 16px;font-weight:800;font-size:13.5px;min-height:44px}
.nlac-btn.alt{background:#fff;color:#1B1A17}.nlac-btn.gold{background:#9C7A3C;border-color:#9C7A3C;color:#fff}.nlac-btn.soft{background:#FBF9F5;color:#1B1A17;border-color:#E2DCD0}
.nlac-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0 28px}.nlac-metric{background:#fff;border:1px solid rgba(27,26,23,.12);border-radius:8px;padding:15px}
.nlac-metric b{display:block;font-size:26px;line-height:1;color:#1B1A17}.nlac-metric span{display:block;margin-top:7px;font-size:12px;color:#6B7280}
.nlac-section{margin-top:30px}.nlac-section h2{font-size:21px;margin:0 0 14px;font-family:var(--font-serif,"Frank Ruhl Libre",serif);letter-spacing:0}
.nlac-card{background:#fff;border:1px solid rgba(27,26,23,.12);border-radius:8px;padding:17px;margin-bottom:14px}.nlac-card-head{display:flex;justify-content:space-between;gap:14px;align-items:flex-start}
.nlac-card-title{font-size:19px;font-weight:800;margin:0 0 4px}.nlac-muted{font-size:13px;color:#6B7280}.nlac-pill{display:inline-flex;align-items:center;border-radius:999px;padding:5px 10px;background:#F3F4F6;color:#374151;font-size:12px;font-weight:800}
.nlac-pill.good{background:#ECFDF5;color:#047857}.nlac-pill.warn{background:#FEF3C7;color:#92400E}.nlac-progress{height:9px;background:#F3F4F6;border-radius:999px;overflow:hidden;margin:13px 0 8px}.nlac-progress i{display:block;height:100%;background:#9C7A3C;border-radius:999px}
.nlac-facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:14px 0}.nlac-fact{background:#FBF9F5;border-radius:7px;padding:10px}.nlac-fact b{display:block;font-size:18px}.nlac-fact span{font-size:12px;color:#6B7280}
.nlac-missing{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.nlac-missing span{font-size:12px;background:#FFF7ED;color:#9A3412;border:1px solid #FED7AA;border-radius:999px;padding:4px 9px}
.nlac-card-actions{display:flex;gap:9px;flex-wrap:wrap;margin-top:14px}.nlac-split{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.45fr);gap:16px}.nlac-list{display:grid;gap:10px}
.nlac-order,.nlac-step{border:1px solid rgba(27,26,23,.1);border-radius:8px;padding:13px;background:#fff}.nlac-step b{display:block;margin-bottom:4px}.nlac-empty{background:#FBF9F5;border:1px dashed #D8CDB8;border-radius:8px;padding:24px;text-align:center;color:#5A5A5A}
.nlac-leads-panel{background:linear-gradient(135deg,#fff,#FBF9F5);border:1px solid rgba(156,122,60,.22);border-radius:8px;padding:18px}.nlac-leads{display:grid;gap:10px}
.nlac-lead{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:start;background:#fff;border:1px solid rgba(27,26,23,.1);border-radius:8px;padding:14px}
.nlac-lead-title{font-weight:900;font-size:15px}.nlac-lead-meta,.nlac-lead-contact{font-size:12.5px;color:#6B7280;margin-top:5px}.nlac-lead-contact{display:flex;gap:10px;flex-wrap:wrap}.nlac-lead-msg{margin-top:8px;font-size:13px;line-height:1.55;color:#374151}
.nlac-lead-e2e{margin-top:10px;display:grid;gap:8px}.nlac-lead-state{display:flex;gap:8px;flex-wrap:wrap;align-items:center;font-size:12px;color:#5A5A5A}.nlac-lead-status-form{display:grid;grid-template-columns:minmax(120px,.5fr) minmax(160px,1fr) auto;gap:8px;align-items:center}.nlac-lead-status-form select,.nlac-lead-status-form input{min-height:40px;border:1px solid #D8CDB8;border-radius:6px;padding:7px 9px;background:#fff;color:#1B1A17}.nlac-lead-status-form button{min-height:40px;border:0;border-radius:6px;padding:8px 12px;background:#1B1A17;color:#fff;font-weight:800;cursor:pointer}.nlac-lead-status-msg{font-size:12px;color:#047857;min-height:16px}
.nlac-products{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.nlac-product{background:#fff;border:1px solid rgba(27,26,23,.12);border-radius:8px;padding:16px}.nlac-product strong{display:block;font-size:17px}.nlac-product small{color:#6B7280}
@media(max-width:860px){.nlac-hero,.nlac-split{grid-template-columns:1fr}.nlac-actions{justify-content:flex-start}.nlac-grid,.nlac-facts{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){.nlac{padding-inline:14px}.nlac-grid,.nlac-facts{grid-template-columns:1fr}.nlac-card-head{display:block}.nlac-btn{width:100%}.nlac-lead{grid-template-columns:1fr}.nlac-lead-status-form{grid-template-columns:1fr}}
</style>';
	}
}

if ( ! function_exists( 'nadlan_ac_render_page' ) ) {
	function nadlan_ac_render_page() {
		get_header();
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
		echo nadlan_ac_render_inner();
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'footer' ); }
		get_footer();
	}
}

if ( ! function_exists( 'nadlan_ac_render_inner' ) ) {
	function nadlan_ac_render_inner() {
		$user_id = (int) apply_filters( 'nadlan_effective_user_id', get_current_user_id() );
		$cards = nadlan_ac_owned_cards( $user_id );
		$orders = nadlan_ac_orders( $user_id );
		$total_views = 0;
		$total_inquiries = 0;
		$total_reviews = 0;
		foreach ( $cards as $card ) {
			$total_views += (int) get_post_meta( $card->ID, 'view_count', true );
			$total_inquiries += nadlan_ac_lead_count( $card->ID );
			$total_reviews += (int) get_post_meta( $card->ID, 'reviews_count', true );
		}
		$recent_leads = nadlan_ac_recent_leads( $cards, 12 );
		ob_start();
		echo nadlan_ac_css();
		?>
<main class="nlac" dir="rtl">
	<section class="nlac-hero">
		<div>
			<div class="nlac-kicker">מרכז פרסום</div>
			<h1>הכרטיסים, הפרויקטים והביצועים שלכם במקום אחד</h1>
			<p>כאן רואים מה פורסם, מה חסר כדי שהעמוד יראה חזק יותר, כמה צפיות ופניות זוהו, ומה הצעד הבא אחרי רכישה או שדרוג.</p>
		</div>
		<div class="nlac-actions">
			<a class="nlac-btn gold" href="<?php echo esc_url( home_url( '/studio/' ) ); ?>">פתחו סטודיו</a>
			<a class="nlac-btn alt" href="<?php echo esc_url( home_url( '/join-pro/' ) ); ?>">מסלולי פרסום</a>
		</div>
	</section>

	<section class="nlac-grid" aria-label="סיכום">
		<div class="nlac-metric"><b><?php echo (int) count( $cards ); ?></b><span>כרטיסים משויכים</span></div>
		<div class="nlac-metric"><b><?php echo number_format_i18n( $total_views ); ?></b><span>צפיות מזוהות</span></div>
		<div class="nlac-metric"><b><?php echo number_format_i18n( $total_inquiries ); ?></b><span>פניות מזוהות</span></div>
		<div class="nlac-metric"><b><?php echo number_format_i18n( $total_reviews ); ?></b><span>ביקורות</span></div>
	</section>

	<section class="nlac-section nlac-leads-panel" aria-label="הפניות שקיבלתי">
		<h2>הפניות שקיבלתי</h2>
		<?php if ( ! $cards ) : ?>
			<div class="nlac-empty">הפניות יופיעו כאן אחרי שיוך כרטיס לחשבון.</div>
		<?php elseif ( ! $recent_leads ) : ?>
			<div class="nlac-empty">פירוט הפניות יופיע כאן עבור כרטיסים במסלול פעיל.</div>
		<?php else : ?>
			<div class="nlac-leads">
				<?php foreach ( $recent_leads as $lead ) :
					$lead_id = (int) $lead->ID;
					$lead_card_id = (int) get_post_meta( $lead_id, 'lead_card_id', true );
					$lead_name = (string) get_post_meta( $lead_id, 'name', true );
					$lead_phone = (string) get_post_meta( $lead_id, 'phone', true );
					$lead_email = (string) get_post_meta( $lead_id, 'email', true );
					$lead_goal = (string) get_post_meta( $lead_id, 'goal', true );
					$lead_message = (string) get_post_meta( $lead_id, 'message', true );
					if ( $lead_message === '' ) { $lead_message = (string) $lead->post_content; }
					$phone_href = preg_replace( '/[^0-9+]/', '', $lead_phone );
					$lead_e2e_on = function_exists( 'nadlan_lead_e2e_enabled' ) && nadlan_lead_e2e_enabled();
					$lead_workflow_status = (string) get_post_meta( $lead_id, 'lead_status', true );
					if ( $lead_workflow_status === '' ) { $lead_workflow_status = 'new'; }
					$lead_ack_label = (int) get_post_meta( $lead_id, 'ack_sent_at', true ) > 0 ? 'אישור נשלח ללקוח' : 'אישור לא נשלח';
					$lead_response_label = function_exists( 'nadlan_lead_e2e_response_label' ) ? nadlan_lead_e2e_response_label( $lead_id ) : '';
					$lead_can_manage = $lead_e2e_on && function_exists( 'nadlan_lead_e2e_user_can_manage_lead' ) && nadlan_lead_e2e_user_can_manage_lead( $lead_id );
					?>
					<article class="nlac-lead">
						<div>
							<div class="nlac-lead-title"><?php echo esc_html( $lead_name ?: 'פנייה חדשה' ); ?></div>
							<div class="nlac-lead-meta">
								<?php echo esc_html( get_the_date( 'd/m/Y H:i', $lead ) ); ?>
								<?php if ( $lead_card_id ) : ?> · <?php echo esc_html( get_the_title( $lead_card_id ) ); ?><?php endif; ?>
								<?php if ( $lead_goal ) : ?> · <?php echo esc_html( $lead_goal ); ?><?php endif; ?>
							</div>
							<div class="nlac-lead-contact">
								<?php if ( $phone_href ) : ?><a href="<?php echo esc_url( 'tel:' . $phone_href ); ?>"><?php echo esc_html( $lead_phone ); ?></a><?php endif; ?>
								<?php if ( is_email( $lead_email ) ) : ?><a href="<?php echo esc_url( 'mailto:' . $lead_email ); ?>"><?php echo esc_html( $lead_email ); ?></a><?php endif; ?>
							</div>
							<?php if ( $lead_message ) : ?>
								<div class="nlac-lead-msg"><?php echo esc_html( wp_trim_words( wp_strip_all_tags( $lead_message ), 22, '...' ) ); ?></div>
							<?php endif; ?>
							<?php if ( $lead_e2e_on ) : ?>
								<div class="nlac-lead-e2e">
									<div class="nlac-lead-state">
										<span><?php echo esc_html( $lead_ack_label ); ?></span>
										<?php if ( $lead_response_label ) : ?><span><?php echo esc_html( $lead_response_label ); ?></span><?php endif; ?>
									</div>
									<?php if ( $lead_can_manage ) : ?>
										<form class="nlac-lead-status-form" data-lead-status-form>
											<input type="hidden" name="lead_id" value="<?php echo (int) $lead_id; ?>">
											<select name="status" aria-label="סטטוס פנייה">
												<?php foreach ( nadlan_lead_e2e_valid_statuses() as $status_key ) : ?>
													<option value="<?php echo esc_attr( $status_key ); ?>" <?php selected( $lead_workflow_status, $status_key ); ?>><?php echo esc_html( nadlan_lead_e2e_status_label( $status_key ) ); ?></option>
												<?php endforeach; ?>
											</select>
											<input type="text" name="note" maxlength="500" placeholder="הערה פרטית">
											<button type="submit">שמור</button>
											<div class="nlac-lead-status-msg" aria-live="polite"></div>
										</form>
									<?php endif; ?>
								</div>
							<?php endif; ?>
						</div>
						<span class="nlac-pill good"><?php echo esc_html( nadlan_ac_lead_status_label( $lead_id ) ); ?></span>
					</article>
				<?php endforeach; ?>
			</div>
		<?php endif; ?>
	</section>
	<?php if ( function_exists( 'nadlan_lead_e2e_enabled' ) && nadlan_lead_e2e_enabled() ) : ?>
	<script>
	(function(){
		var endpoint=<?php echo wp_json_encode( rest_url( 'nadlan/v1/lead/status' ) ); ?>;
		var nonce=<?php echo wp_json_encode( wp_create_nonce( 'wp_rest' ) ); ?>;
		document.querySelectorAll('[data-lead-status-form]').forEach(function(form){
			form.addEventListener('submit',function(e){
				e.preventDefault();
				var msg=form.querySelector('.nlac-lead-status-msg');
				var payload={
					lead_id:form.querySelector('[name="lead_id"]').value,
					status:form.querySelector('[name="status"]').value,
					note:form.querySelector('[name="note"]').value
				};
				if(msg)msg.textContent='שומר...';
				fetch(endpoint,{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json','X-WP-Nonce':nonce},body:JSON.stringify(payload)})
					.then(function(r){return r.json().then(function(j){if(!r.ok){throw j;}return j;});})
					.then(function(j){if(msg)msg.textContent='נשמר'; var pill=form.closest('.nlac-lead').querySelector('.nlac-pill'); if(pill&&j.label){pill.textContent=j.label;}})
					.catch(function(){if(msg)msg.textContent='לא נשמר. נסו שוב.';});
			});
		});
	})();
	</script>
	<?php endif; ?>

	<div class="nlac-split">
		<section class="nlac-section">
			<h2>הנכסים הפרסומיים שלכם</h2>
			<?php if ( ! $cards ) : ?>
				<div class="nlac-empty">
					<p><strong>עדיין אין כרטיס שמחובר לחשבון הזה.</strong></p>
					<p>אפשר לחפש כרטיס קיים ולבקש בעלות, או להתחיל קמפיין לפרויקט חדש.</p>
					<div class="nlac-card-actions" style="justify-content:center">
						<a class="nlac-btn soft" href="<?php echo esc_url( home_url( '/professionals/' ) ); ?>">חיפוש כרטיס קיים</a>
						<a class="nlac-btn gold" href="<?php echo esc_url( home_url( '/?add-to-cart=489&ref=advertiser-center-empty' ) ); ?>">קמפיין פרויקט</a>
					</div>
					<?php if ( current_user_can( 'manage_options' ) ) : ?>
						<p class="nlac-muted">מנהלי אתר יכולים להוסיף <a href="<?php echo esc_url( add_query_arg( 'all', '1', home_url( '/advertiser-center/' ) ) ); ?>">?all=1</a> כדי לראות דוגמת כרטיסים.</p>
					<?php endif; ?>
				</div>
			<?php endif; ?>

			<?php foreach ( $cards as $card ) :
				$completion = nadlan_ac_completion( $card->ID );
				$tier = (string) get_post_meta( $card->ID, 'paid_tier', true );
				if ( $tier === '' ) { $tier = 'free'; }
				$views = (int) get_post_meta( $card->ID, 'view_count', true );
				$inquiries = nadlan_ac_lead_count( $card->ID );
				$reviews = (int) get_post_meta( $card->ID, 'reviews_count', true );
				$photos = nadlan_ac_photos( $card->ID );
				$is_project = $card->post_type === 'nadlan_project';
				?>
				<article class="nlac-card">
					<div class="nlac-card-head">
						<div>
							<h3 class="nlac-card-title"><?php echo esc_html( get_the_title( $card ) ); ?></h3>
							<div class="nlac-muted"><?php echo esc_html( nadlan_ac_card_type_label( $card->post_type ) ); ?> · עודכן <?php echo esc_html( get_the_modified_date( 'd/m/Y', $card ) ); ?></div>
						</div>
						<span class="nlac-pill <?php echo in_array( $tier, array( 'pro', 'premier' ), true ) ? 'good' : 'warn'; ?>"><?php echo esc_html( strtoupper( $tier ) ); ?></span>
					</div>
					<div class="nlac-progress" aria-label="השלמת פרופיל"><i style="width:<?php echo (int) $completion['score']; ?>%"></i></div>
					<div class="nlac-muted">השלמת עמוד: <?php echo (int) $completion['score']; ?>%</div>
					<?php if ( function_exists( 'nadlan_ao_campaign_badge' ) ) { echo nadlan_ao_campaign_badge( $card->ID ); } ?>
					<div class="nlac-facts">
						<div class="nlac-fact"><b><?php echo number_format_i18n( $views ); ?></b><span>צפיות</span></div>
						<div class="nlac-fact"><b><?php echo number_format_i18n( $inquiries ); ?></b><span>פניות</span></div>
						<div class="nlac-fact"><b><?php echo number_format_i18n( $reviews ); ?></b><span>ביקורות</span></div>
						<div class="nlac-fact"><b><?php echo number_format_i18n( count( $photos ) ); ?></b><span>תמונות</span></div>
					</div>
					<?php if ( $completion['missing'] ) : ?>
						<div class="nlac-muted">כדאי להשלים:</div>
						<div class="nlac-missing">
							<?php foreach ( array_slice( $completion['missing'], 0, 5 ) as $miss ) : ?>
								<span><?php echo esc_html( $miss ); ?></span>
							<?php endforeach; ?>
						</div>
					<?php endif; ?>
					<div class="nlac-card-actions">
						<a class="nlac-btn" href="<?php echo esc_url( home_url( '/studio/?id=' . (int) $card->ID ) ); ?>">עריכה והעלאת תמונות</a>
						<a class="nlac-btn alt" href="<?php echo esc_url( get_permalink( $card ) ); ?>" target="_blank" rel="noopener">תצוגה ציבורית</a>
						<?php if ( ! in_array( $tier, array( 'pro', 'premier' ), true ) ) : ?>
							<a class="nlac-btn gold" href="<?php echo esc_url( home_url( '/?add-to-cart=' . ( $is_project ? '489' : '476' ) . '&ref=advertiser-center-card&card_id=' . (int) $card->ID ) ); ?>">שדרוג</a>
						<?php endif; ?>
					</div>
				</article>
			<?php endforeach; ?>
		</section>

		<aside class="nlac-section">
			<h2>הצעדים הקרובים</h2>
			<div class="nlac-list">
				<div class="nlac-step"><b>1. השלימו את העמוד</b><span class="nlac-muted">תיאור, תמונות, מיקום ופרטי קשר הופכים כרטיס רגיל לעמוד שאפשר לשווק.</span></div>
				<div class="nlac-step"><b>2. בדקו את התצוגה הציבורית</b><span class="nlac-muted">פתחו את העמוד כמו לקוח וודאו שהמסר ברור תוך כמה שניות.</span></div>
				<div class="nlac-step"><b>3. עקבו אחרי פניות וצפיות</b><span class="nlac-muted">המספרים כאן הם בסיס לדוח החודשי ולשיחת שיפור.</span></div>
			</div>

			<h2 style="margin-top:24px">רכישות אחרונות</h2>
			<div class="nlac-list">
				<?php if ( ! $orders ) : ?>
					<div class="nlac-order"><span class="nlac-muted">לא נמצאו הזמנות פרסום בחשבון הזה.</span></div>
				<?php endif; ?>
				<?php foreach ( $orders as $order ) : ?>
					<div class="nlac-order">
						<strong>#<?php echo (int) $order->get_id(); ?> · <?php echo esc_html( wc_get_order_status_name( $order->get_status() ) ); ?></strong>
						<div class="nlac-muted"><?php echo wp_kses_post( wc_price( $order->get_total(), array( 'currency' => $order->get_currency() ) ) ); ?> · <?php echo esc_html( $order->get_date_created() ? $order->get_date_created()->date_i18n( 'd/m/Y' ) : '' ); ?></div>
						<?php if ( function_exists( 'nadlan_ao_order_summary' ) ) { echo nadlan_ao_order_summary( $order ); } ?>
					</div>
				<?php endforeach; ?>
			</div>
			<?php if ( function_exists( 'nadlan_ao_render_link_box' ) ) { echo nadlan_ao_render_link_box( $orders, $cards ); } ?>
		</aside>
	</div>

	<section class="nlac-section">
		<h2>מסלולי פרסום זמינים</h2>
		<div class="nlac-products">
			<?php foreach ( nadlan_ac_products() as $pid => $product ) : ?>
				<div class="nlac-product">
					<strong><?php echo esc_html( $product['label'] ); ?></strong>
					<small><?php echo esc_html( $product['price'] ); ?></small>
					<p class="nlac-muted"><?php echo $pid === 489 ? 'עמוד פרויקט, תמונות, מיקום ודוח ביצועים.' : 'מיקום משופר, פרטי קשר גלויים ודוח חודשי.'; ?></p>
					<a class="nlac-btn soft" href="<?php echo esc_url( $product['href'] ); ?>">בחירת מסלול</a>
				</div>
			<?php endforeach; ?>
		</div>
	</section>
</main>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_ac_thankyou_panel' ) ) {
	function nadlan_ac_thankyou_panel( $order_id ) {
		if ( ! $order_id || ! function_exists( 'wc_get_order' ) ) { return; }
		$order = wc_get_order( $order_id );
		if ( ! nadlan_ac_order_has_paid_product( $order ) ) { return; }
		?>
<div class="nlac-thanks" dir="rtl" style="margin:24px 0;padding:20px;border:1px solid #E2DCD0;border-radius:8px;background:#FBF9F5;font-family:Heebo,Arial,sans-serif">
	<h2 style="margin-top:0">ההזמנה נקלטה. זה הצעד הבא.</h2>
	<p>מרכז הפרסום מרכז את העמודים, התמונות, הצפיות, הפניות והדוחות שלכם. התחילו בהשלמת העמוד או בבקשת הקמה לפרויקט חדש.</p>
	<p><a href="<?php echo esc_url( home_url( '/advertiser-center/' ) ); ?>" style="display:inline-block;background:#1B1A17;color:#fff;text-decoration:none;border-radius:6px;padding:11px 16px;font-weight:700">פתחו את מרכז הפרסום</a></p>
</div>
		<?php
	}
}
add_action( 'woocommerce_thankyou', 'nadlan_ac_thankyou_panel', 18 );

add_action( 'woocommerce_account_dashboard', function () {
	echo '<p dir="rtl"><a class="button" href="' . esc_url( home_url( '/advertiser-center/' ) ) . '">מרכז הפרסום של נדלן</a></p>';
}, 12 );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['advertiser_center'] = array(
		'route' => home_url( '/advertiser-center/' ),
		'shortcode' => '[nadlan_advertiser_center]',
		'products' => array_keys( nadlan_ac_products() ),
	);
	return $out;
} );
