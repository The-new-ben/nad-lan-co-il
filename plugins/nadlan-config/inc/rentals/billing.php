<?php
/**
 * nadlan-config - RENTALS v2: the landlord's subscription (HAD-383, 3.10.2026).
 *
 * The landlord pays nad-lan for the software, through the shop the site
 * already runs: WooCommerce + the Morning (GreenInvoice) gateway (card, Bit,
 * Google Pay, Apple Pay), which also issues the tax invoice. The RENT never
 * passes here (research 2026-10-03-rent-collection-psp: only a licensed
 * payment company may move it).
 *
 * The products are ordinary WooCommerce products marked with the meta
 * _nlrm_plan = pro | business (and _nlrm_days, default 30). Prices live in
 * the shop, so the owner sets them there. A payment extends the plan from the
 * current end (never shortens it); three days before the end a renewal order
 * with a one-click pay link is emailed (the same pattern as renewals.php for
 * the professionals' tiers); seven days after the end without payment the
 * account is back to the free plan. Nothing is ever deleted: above the free
 * limit the landlord keeps every apartment and cannot add new ones.
 *
 * The switch (option nlrm_billing):
 *   'off'  (default) - no offer shown, no limit enforced (the v1 promise:
 *                      free for everyone, nobody loses a feature);
 *   'test'           - administrators see the offer; nobody is charged;
 *   'live'           - everyone sees it and the free limit applies.
 * Prices were not approved yet (3.10.2026): the products are created as
 * DRAFTS and the switch stays 'off' until the owner's word.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NLRM_PLAN_GRACE_DAYS' ) ) { define( 'NLRM_PLAN_GRACE_DAYS', 7 ); }
if ( ! defined( 'NLRM_PLAN_RENEW_DAYS' ) ) { define( 'NLRM_PLAN_RENEW_DAYS', 3 ); }

if ( ! function_exists( 'nlrm_billing_mode' ) ) {
	function nlrm_billing_mode() {
		$m = (string) get_option( 'nlrm_billing', 'off' );
		return in_array( $m, array( 'off', 'test', 'live' ), true ) ? $m : 'off';
	}
}
if ( ! function_exists( 'nlrm_plan_limits' ) ) {
	function nlrm_plan_limits( $plan ) {
		$limits = array(
			'free'     => array( 'units' => 3, 'docs_mb' => 200, 'ai' => 20 ),
			'pro'      => array( 'units' => 50, 'docs_mb' => 5000, 'ai' => 500 ),
			'business' => array( 'units' => 2000, 'docs_mb' => 50000, 'ai' => 5000 ),
		);
		return $limits[ $plan ] ?? $limits['free'];
	}
}
if ( ! function_exists( 'nlrm_plan' ) ) {
	/* the plan in force for an account, with its limits and dates */
	function nlrm_plan( $owner ) {
		$plan = (string) get_user_meta( $owner, 'nlrm_plan', true );
		if ( ! in_array( $plan, array( 'free', 'pro', 'business' ), true ) ) { $plan = 'free'; }
		$until = (int) get_user_meta( $owner, 'nlrm_plan_until', true ); /* 0 = no end (granted by the site) */
		$state = 'active';
		if ( 'free' !== $plan && $until ) {
			$now = nlrm_time();
			if ( $now > $until + NLRM_PLAN_GRACE_DAYS * DAY_IN_SECONDS ) { $plan = 'free'; $state = 'expired'; }
			elseif ( $now > $until ) { $state = 'grace'; }
		}
		$mode = nlrm_billing_mode();
		/* until billing is live nobody is limited (no feature is taken away) */
		$limits = 'live' === $mode ? nlrm_plan_limits( $plan ) : nlrm_plan_limits( 'business' );
		return array( 'id' => $plan, 'limits' => $limits, 'until' => $until ? gmdate( 'Y-m-d', $until ) : null, 'state' => $state, 'billing' => $mode, 'offer' => nlrm_billing_offer( $owner ) );
	}
}

/* ---------- the products (found by their meta, any status) ---------- */
if ( ! function_exists( 'nlrm_billing_products' ) ) {
	function nlrm_billing_products( $reset = false ) {
		static $cache = null;
		if ( $reset ) { $cache = null; }
		if ( null !== $cache ) { return $cache; }
		$cache = array();
		if ( ! function_exists( 'wc_get_products' ) ) { return $cache; }
		foreach ( (array) wc_get_products( array( 'limit' => 20, 'status' => array( 'publish', 'draft', 'private' ), 'meta_key' => '_nlrm_plan' ) ) as $p ) {
			$plan = (string) $p->get_meta( '_nlrm_plan' );
			if ( ! in_array( $plan, array( 'pro', 'business' ), true ) || isset( $cache[ $plan ] ) ) { continue; }
			$cache[ $plan ] = array( 'id' => (int) $p->get_id(), 'price' => (float) $p->get_price(), 'status' => $p->get_status(), 'days' => max( 1, (int) ( $p->get_meta( '_nlrm_days' ) ?: 30 ) ) );
		}
		return $cache;
	}
}
if ( ! function_exists( 'nlrm_billing_offer' ) ) {
	/* what the app may show: nothing while 'off'; to administrators in 'test'; to all in 'live' */
	function nlrm_billing_offer( $owner ) {
		$mode = nlrm_billing_mode();
		if ( 'off' === $mode || ( 'test' === $mode && ! current_user_can( 'manage_options' ) ) ) { return null; }
		$out = array();
		foreach ( nlrm_billing_products() as $plan => $p ) {
			if ( 'live' === $mode && 'publish' !== $p['status'] ) { continue; }
			$out[ $plan ] = array( 'price' => $p['price'], 'days' => $p['days'], 'units' => nlrm_plan_limits( $plan )['units'], 'buy' => function_exists( 'wc_get_checkout_url' ) ? add_query_arg( array( 'add-to-cart' => $p['id'] ), wc_get_checkout_url() ) : '', 'test' => 'test' === $mode );
		}
		return $out ? $out : null;
	}
}

/* ---------- a paid order extends the plan (once per order) ---------- */
if ( ! function_exists( 'nlrm_billing_apply_order' ) ) {
	function nlrm_billing_apply_order( $order_id ) {
		if ( ! function_exists( 'wc_get_order' ) ) { return 0; }
		$order = wc_get_order( $order_id );
		if ( ! $order || $order->get_meta( '_nlrm_applied' ) ) { return 0; }
		$user = (int) $order->get_customer_id();
		if ( ! $user ) { return 0; }
		$n = 0;
		foreach ( $order->get_items() as $item ) {
			$product = $item->get_product();
			$plan = $product ? (string) $product->get_meta( '_nlrm_plan' ) : '';
			if ( ! in_array( $plan, array( 'pro', 'business' ), true ) ) { continue; }
			$days = max( 1, (int) ( $product->get_meta( '_nlrm_days' ) ?: 30 ) ) * max( 1, (int) $item->get_quantity() );
			$cur = (string) get_user_meta( $user, 'nlrm_plan', true );
			$until = (int) get_user_meta( $user, 'nlrm_plan_until', true );
			$from = ( $cur === $plan && $until > nlrm_time() ) ? $until : nlrm_time();
			update_user_meta( $user, 'nlrm_plan', $plan );
			update_user_meta( $user, 'nlrm_plan_until', $from + $days * DAY_IN_SECONDS );
			update_user_meta( $user, 'nlrm_plan_product', (int) $product->get_id() );
			update_user_meta( $user, 'nlrm_plan_order', (int) $order->get_id() );
			delete_user_meta( $user, 'nlrm_plan_renewal' );
			nlrm_event( $user, 'shop', '', 0, 'plan_paid', '', '', array( 'plan' => $plan, 'order' => (int) $order->get_id(), 'until' => gmdate( 'Y-m-d', $from + $days * DAY_IN_SECONDS ) ) );
			$n++;
		}
		if ( $n ) {
			$order->update_meta_data( '_nlrm_applied', gmdate( 'c' ) );
			$order->add_order_note( 'Rentals plan extended for user #' . $user . '.' );
			$order->save();
		}
		return $n;
	}
}
add_action( 'woocommerce_payment_complete', 'nlrm_billing_apply_order', 20 );
add_action( 'woocommerce_order_status_completed', 'nlrm_billing_apply_order', 20 );

/* ---------- renewals: an invoice with a pay link three days before the end ---------- */
add_action( 'nlrm_daily', function () {
	if ( 'live' === nlrm_billing_mode() ) { nlrm_billing_renewals(); }
}, 20 );
if ( ! function_exists( 'nlrm_billing_renewals' ) ) {
	function nlrm_billing_renewals() {
		global $wpdb;
		if ( ! function_exists( 'wc_create_order' ) ) { return 0; }
		$soon = nlrm_time() + NLRM_PLAN_RENEW_DAYS * DAY_IN_SECONDS;
		$users = $wpdb->get_col( $wpdb->prepare( 'SELECT user_id FROM ' . $wpdb->usermeta . " WHERE meta_key = 'nlrm_plan_until' AND CAST(meta_value AS UNSIGNED) BETWEEN %d AND %d", nlrm_time() - NLRM_PLAN_GRACE_DAYS * DAY_IN_SECONDS, $soon ) );
		$n = 0;
		foreach ( (array) $users as $u ) {
			$u = (int) $u;
			$until = (int) get_user_meta( $u, 'nlrm_plan_until', true );
			if ( (int) get_user_meta( $u, 'nlrm_plan_renewal_cycle', true ) === $until ) { continue; }
			$pid = (int) get_user_meta( $u, 'nlrm_plan_product', true );
			$product = $pid ? wc_get_product( $pid ) : null;
			$last = wc_get_order( (int) get_user_meta( $u, 'nlrm_plan_order', true ) );
			if ( ! $product || ! $last ) { continue; }
			$order = wc_create_order( array( 'customer_id' => $u ) );
			if ( is_wp_error( $order ) ) { continue; }
			$order->add_product( $product, 1 );
			$order->set_address( $last->get_address( 'billing' ), 'billing' );
			$order->update_meta_data( '_nlrm_renewal_for', $u );
			$order->calculate_totals();
			$order->update_status( 'pending', 'Rentals plan renewal for user #' . $u . '.' );
			$order->save();
			update_user_meta( $u, 'nlrm_plan_renewal', (int) $order->get_id() );
			update_user_meta( $u, 'nlrm_plan_renewal_cycle', $until );
			if ( function_exists( 'WC' ) && WC()->mailer() ) {
				$mails = WC()->mailer()->get_emails();
				if ( isset( $mails['WC_Email_Customer_Invoice'] ) ) { $mails['WC_Email_Customer_Invoice']->trigger( $order->get_id(), $order ); }
			}
			$n++;
		}
		return $n;
	}
}

/* ---------- the site's administrator can grant a plan (a pilot, a partner) ---------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/rm/plan-grant', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( WP_REST_Request $r ) {
			$u = (int) $r->get_param( 'user_id' );
			$plan = in_array( $r->get_param( 'plan' ), array( 'free', 'pro', 'business' ), true ) ? (string) $r->get_param( 'plan' ) : 'free';
			$days = (int) $r->get_param( 'days' ); /* 0 = no end */
			if ( ! $u || ! get_userdata( $u ) ) { return new WP_Error( 'nlrm_404', 'no such user', array( 'status' => 404 ) ); }
			update_user_meta( $u, 'nlrm_plan', $plan );
			if ( $days > 0 ) { update_user_meta( $u, 'nlrm_plan_until', nlrm_time() + $days * DAY_IN_SECONDS ); } else { delete_user_meta( $u, 'nlrm_plan_until' ); }
			nlrm_event( $u, 'u:' . get_current_user_id(), '', 0, 'plan_grant', '', '', array( 'plan' => $plan, 'days' => $days ) );
			return nlrm_plan( $u );
		},
	) );
} );
