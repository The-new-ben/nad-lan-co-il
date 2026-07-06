<?php
/**
 * nadlan-config - Tier renewals (month 2 and onward), owner core-business ask
 * 2026-07-06.
 *
 * The gap: paid tiers (advertiser-orders.php) activate for N days and then
 * silently drop to free - no renewal path, month-2 revenue was manual.
 *
 * The machine (competitor-standard shape, sized to what we run today):
 *  - 3 days before a paid tier expires, a RENEWAL ORDER for the same product
 *    and the same card is created automatically and the customer receives the
 *    standard WooCommerce invoice email with a one-click pay link
 *    (order-pay page -> Morning credit card / Bit / Google Pay).
 *  - Payment flows through the existing woocommerce_payment_complete hook,
 *    which extends campaign_end from the current end (stacking is already
 *    built into nadlan_ao_apply_order_item) - zero double logic here.
 *  - Unpaid renewals: the existing downgrade cron drops the tier at expiry
 *    exactly as before; the pending order stays payable for 7 more days
 *    (late payment re-activates from the payment date), then auto-cancels.
 *
 * Upgrade path (documented in AGENT-LOG): WooCommerce Subscriptions + the
 * Morning gateway's native token support makes month-2 charges automatic
 * with no email step. This module is forward-compatible: it skips any card
 * whose product becomes a true subscription product.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_RENEW_LEAD_DAYS  = 3;   // create the renewal order this many days before expiry
const NADLAN_RENEW_GRACE_DAYS = 7;   // keep the pending order payable this long after expiry

add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'nadlan_renewals_tick' ) ) {
		wp_schedule_event( time() + 300, 'twicedaily', 'nadlan_renewals_tick' );
	}
} );

add_action( 'nadlan_renewals_tick', 'nadlan_renewals_run' );

if ( ! function_exists( 'nadlan_renewals_run' ) ) {
	function nadlan_renewals_run() {
		if ( ! function_exists( 'wc_create_order' ) || ! function_exists( 'nadlan_ao_product' ) ) { return; }
		$now  = current_time( 'timestamp' );
		$soon = $now + ( NADLAN_RENEW_LEAD_DAYS * DAY_IN_SECONDS );
		$q = new WP_Query( array(
			'post_type'      => array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ),
			'post_status'    => 'publish',
			'posts_per_page' => 50,
			'fields'         => 'ids',
			'no_found_rows'  => true,
			'meta_query'     => array( 'relation' => 'AND',
				array( 'key' => 'paid_tier', 'value' => array( 'pro', 'premier' ), 'compare' => 'IN' ),
				array( 'key' => 'campaign_end', 'value' => $soon, 'compare' => '<=', 'type' => 'NUMERIC' ),
				array( 'key' => 'campaign_end', 'value' => $now - ( NADLAN_RENEW_GRACE_DAYS * DAY_IN_SECONDS ), 'compare' => '>=', 'type' => 'NUMERIC' ),
			),
		) );
		foreach ( $q->posts as $card_id ) { nadlan_renewals_maybe_create( (int) $card_id ); }
		nadlan_renewals_cancel_stale();
	}
}

if ( ! function_exists( 'nadlan_renewals_maybe_create' ) ) {
	function nadlan_renewals_maybe_create( $card_id ) {
		// an open renewal already exists and is still payable -> nothing to do
		$existing = (int) get_post_meta( $card_id, 'renewal_order_id', true );
		if ( $existing ) {
			$eo = wc_get_order( $existing );
			if ( $eo && in_array( $eo->get_status(), array( 'pending', 'on-hold' ), true ) ) { return; }
			if ( $eo && $eo->get_status() === 'completed' ) {
				// paid renewal already applied; clear the pointer for the next cycle
				delete_post_meta( $card_id, 'renewal_order_id' );
			}
		}
		$product_id = (int) get_post_meta( $card_id, 'paid_product_id', true );
		$product    = $product_id ? nadlan_ao_product( $product_id ) : null;
		if ( ! $product ) { return; }
		$last_order_id = (int) get_post_meta( $card_id, 'paid_order_id', true );
		$last_order    = $last_order_id ? wc_get_order( $last_order_id ) : null;
		if ( ! $last_order ) { return; }
		$customer_id = (int) $last_order->get_customer_id();
		if ( ! $customer_id ) { return; } // guest checkout: manual follow-up via lead inbox
		// same-cycle guard: never create twice for the same expiry
		$cycle = (int) get_post_meta( $card_id, 'campaign_end', true );
		if ( (int) get_post_meta( $card_id, 'renewal_cycle_end', true ) === $cycle ) { return; }

		$order = wc_create_order( array( 'customer_id' => $customer_id ) );
		if ( is_wp_error( $order ) ) { return; }
		$item_id = $order->add_product( wc_get_product( $product_id ), 1 );
		if ( $item_id ) {
			$item = $order->get_item( $item_id );
			if ( $item ) { $item->add_meta_data( '_nadlan_card_id', (int) $card_id, true ); $item->save(); }
		}
		$order->set_address( $last_order->get_address( 'billing' ), 'billing' );
		$order->update_meta_data( '_nadlan_renewal_for_card', (int) $card_id );
		$order->calculate_totals();
		$order->update_status( 'pending', 'Nadlan renewal: tier ' . $product['tier'] . ' for card #' . $card_id . '.' );
		$order->save();

		update_post_meta( $card_id, 'renewal_order_id', (int) $order->get_id() );
		update_post_meta( $card_id, 'renewal_cycle_end', $cycle );

		// the standard WooCommerce invoice email carries the one-click pay link
		if ( function_exists( 'WC' ) && WC()->mailer() ) {
			$mails = WC()->mailer()->get_emails();
			if ( isset( $mails['WC_Email_Customer_Invoice'] ) ) { $mails['WC_Email_Customer_Invoice']->trigger( $order->get_id(), $order ); }
		}
		$order->add_order_note( 'Renewal invoice sent to customer #' . $customer_id . ' (expiry ' . date_i18n( 'd/m/Y', $cycle ) . ').' );
	}
}

if ( ! function_exists( 'nadlan_renewals_cancel_stale' ) ) {
	/** Pending renewal orders whose grace window passed are cancelled so the
	 *  books stay clean; a returning customer simply buys again from join-pro. */
	function nadlan_renewals_cancel_stale() {
		if ( ! function_exists( 'wc_get_orders' ) ) { return; }
		$orders = wc_get_orders( array(
			'status'     => array( 'pending', 'on-hold' ),
			'limit'      => 50,
			'meta_key'   => '_nadlan_renewal_for_card',
			'date_created' => '<' . ( time() - ( ( NADLAN_RENEW_LEAD_DAYS + NADLAN_RENEW_GRACE_DAYS + 1 ) * DAY_IN_SECONDS ) ),
		) );
		foreach ( $orders as $order ) {
			$order->update_status( 'cancelled', 'Nadlan renewal window passed without payment.' );
			$card_id = (int) $order->get_meta( '_nadlan_renewal_for_card' );
			if ( $card_id && (int) get_post_meta( $card_id, 'renewal_order_id', true ) === (int) $order->get_id() ) {
				delete_post_meta( $card_id, 'renewal_order_id' );
			}
		}
	}
}
