<?php
/**
 * nadlan-config - "הצעות מחיר" phase 1: non-binding offer collection on listings.
 * NOT a binding auction. Flat-fee monetization only (legal spec:
 * docs/2026-06-11-offers-feature-spec-cited.md). Dark behind nadlan_feature_offers.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_offers_enabled' ) ) {
	function nadlan_offers_enabled() {
		return (bool) apply_filters( 'nadlan_offers_enabled', get_option( 'nadlan_feature_offers', '0' ) === '1' );
	}
}

add_action( 'init', function () {
	register_post_type( 'nadlan_offer', array(
		'labels' => array( 'name' => 'הצעות מחיר', 'singular_name' => 'הצעת מחיר' ),
		'public' => false, 'show_ui' => true, 'show_in_menu' => 'edit.php?post_type=nadlan_lead',
		'supports' => array( 'title' ), 'capability_type' => 'post', 'map_meta_cap' => true,
	) );
} );

if ( ! function_exists( 'nadlan_offers_card_types' ) ) {
	function nadlan_offers_card_types() { return array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ); }
}

if ( ! function_exists( 'nadlan_offers_for_card' ) ) {
	function nadlan_offers_for_card( $card_id, $statuses = array( 'live' ) ) {
		$q = new WP_Query( array(
			'post_type' => 'nadlan_offer', 'post_status' => 'private', 'fields' => 'ids',
			'posts_per_page' => 100, 'no_found_rows' => true,
			'meta_query' => array(
				array( 'key' => 'offer_card_id', 'value' => (int) $card_id ),
				array( 'key' => 'offer_status', 'value' => (array) $statuses, 'compare' => 'IN' ),
			),
		) );
		wp_reset_postdata();
		return $q->posts;
	}
}

if ( ! function_exists( 'nadlan_offers_leading_amount' ) ) {
	function nadlan_offers_leading_amount( $card_id ) {
		$top = 0;
		foreach ( nadlan_offers_for_card( $card_id ) as $oid ) {
			$amt = (float) get_post_meta( $oid, 'offer_amount', true );
			if ( $amt > $top ) { $top = $amt; }
		}
		return $top;
	}
}

if ( ! function_exists( 'nadlan_offers_extend_window' ) ) {
	function nadlan_offers_extend_window( $card_id ) {
		// Anti-sniping: a new leading offer pushes the window at least 24h out.
		$end = (int) get_post_meta( $card_id, 'offers_window_end', true );
		$min = time() + DAY_IN_SECONDS;
		if ( $end && $end < $min ) { update_post_meta( $card_id, 'offers_window_end', $min ); }
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/offers', array(
		'methods' => 'POST', 'permission_callback' => '__return_true',
		'callback' => function ( WP_REST_Request $req ) {
			if ( ! nadlan_offers_enabled() ) { return new WP_Error( 'offers_disabled', 'offers_disabled', array( 'status' => 404 ) ); }
			$p = $req->get_json_params(); if ( ! is_array( $p ) ) { $p = $req->get_params(); }
			if ( ! empty( $p['company'] ) ) { return array( 'ok' => true ); } // honeypot: pretend success
			$ip = sanitize_text_field( $_SERVER['REMOTE_ADDR'] ?? '0' );
			$rl = 'nadlan_offer_rl_' . md5( $ip );
			if ( (int) get_transient( $rl ) >= 5 ) { return new WP_Error( 'rate', 'יותר מדי הצעות, נסו מאוחר יותר.', array( 'status' => 429 ) ); }
			set_transient( $rl, (int) get_transient( $rl ) + 1, HOUR_IN_SECONDS );

			$card_id = absint( $p['card_id'] ?? 0 );
			$card = get_post( $card_id );
			if ( ! $card || ! in_array( $card->post_type, nadlan_offers_card_types(), true ) ) { return new WP_Error( 'bad_card', 'bad_card', array( 'status' => 422 ) ); }
			if ( get_post_meta( $card_id, 'offers_enabled', true ) !== '1' ) { return new WP_Error( 'offers_off_for_card', 'הצעות אינן פתוחות לנכס זה.', array( 'status' => 403 ) ); }
			$amount = (float) ( $p['amount'] ?? 0 );
			$min = (float) get_post_meta( $card_id, 'offers_min', true );
			if ( $amount <= 0 || ( $min > 0 && $amount < $min ) ) { return new WP_Error( 'amount_low', 'סכום ההצעה נמוך מהסף שקבע המוכר.', array( 'status' => 422 ) ); }
			$name  = sanitize_text_field( (string) ( $p['name'] ?? '' ) );
			$phone = preg_replace( '/[^0-9+\-]/', '', (string) ( $p['phone'] ?? '' ) );
			$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
			if ( $name === '' || strlen( $phone ) < 9 ) { return new WP_Error( 'missing', 'שם וטלפון נדרשים.', array( 'status' => 422 ) ); }
			if ( empty( $p['nonbinding_ack'] ) ) { return new WP_Error( 'ack_required', 'יש לאשר שההצעה אינה מחייבת.', array( 'status' => 422 ) ); }

			// Dedupe: same phone+card within 24h updates the existing offer instead of duplicating.
			$fp = md5( $card_id . '|' . $phone );
			$guard = 'nadlan_offer_g_' . $fp;
			$existing = (int) get_option( $guard, 0 );
			if ( $existing && get_post_type( $existing ) === 'nadlan_offer' ) {
				update_post_meta( $existing, 'offer_amount', $amount );
				update_post_meta( $existing, 'offer_updated_at', time() );
				nadlan_offers_extend_window( $card_id );
				do_action( 'nadlan_offer_revised', $existing, $card_id, $amount );
				return array( 'ok' => true, 'revised' => true, 'leading' => nadlan_offers_leading_amount( $card_id ) );
			}
			$count = count( nadlan_offers_for_card( $card_id, array( 'live', 'pending_review' ) ) ) + 1;
			$oid = wp_insert_post( array(
				'post_type' => 'nadlan_offer', 'post_status' => 'private',
				'post_title' => sprintf( 'הצעה #%d לנכס %d', $count, $card_id ),
			) );
			if ( ! $oid || is_wp_error( $oid ) ) { return new WP_Error( 'save_failed', 'save_failed', array( 'status' => 500 ) ); }
			foreach ( array(
				'offer_card_id' => $card_id, 'offer_amount' => $amount, 'offer_name' => $name,
				'offer_phone' => $phone, 'offer_email' => $email,
				'offer_financing' => in_array( $p['financing'] ?? '', array( 'cash', 'preapproved', 'pending' ), true ) ? $p['financing'] : 'pending',
				'offer_flex_days' => absint( $p['flex_days'] ?? 0 ),
				'offer_message' => nadlan_offers_enabled() ? sanitize_textarea_field( (string) ( $p['message'] ?? '' ) ) : '',
				'offer_handle' => 'מציע #' . $count, 'offer_status' => 'live', 'offer_created_at' => time(),
				'offer_consent_contact' => ! empty( $p['consent_contact'] ) ? 1 : 0,
			) as $k => $v ) { update_post_meta( $oid, $k, $v ); }
			update_option( $guard, $oid, false );
			nadlan_offers_extend_window( $card_id );

			// Notify the card owner (or admin fallback) - amount + handle only, no contact details yet.
			$owner_id = (int) get_post_meta( $card_id, 'owner_user_id', true );
			$to = $owner_id ? get_the_author_meta( 'user_email', $owner_id ) : get_option( 'admin_email' );
			if ( $to ) {
				wp_mail( $to, 'הצעת מחיר חדשה: ' . get_the_title( $card_id ),
					"התקבלה הצעת מחיר חדשה לנכס שלכם.\n\nסכום: ₪" . number_format( $amount ) . "\nמימון: " . get_post_meta( $oid, 'offer_financing', true ) . "\n\nלצפייה בכל ההצעות היכנסו למרכז המפרסמים:\n" . home_url( '/advertiser-center/' ) );
			}
			do_action( 'nadlan_offer_submitted', $oid, $card_id, $amount );
			return array( 'ok' => true, 'offer_id' => $oid, 'handle' => 'מציע #' . $count, 'leading' => nadlan_offers_leading_amount( $card_id ) );
		},
	) );
	register_rest_route( 'nadlan/v1', '/offers/leading/(?P<card>\d+)', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( WP_REST_Request $req ) {
			if ( ! nadlan_offers_enabled() ) { return new WP_Error( 'offers_disabled', 'offers_disabled', array( 'status' => 404 ) ); }
			$card_id = absint( $req['card'] );
			$mode = get_post_meta( $card_id, 'offers_transparency', true );
			if ( $mode === 'sealed' ) { return array( 'mode' => 'sealed', 'offers_exist' => count( nadlan_offers_for_card( $card_id ) ) > 0 ); }
			return array( 'mode' => $mode ?: 'leading_amount', 'leading' => nadlan_offers_leading_amount( $card_id ), 'count' => count( nadlan_offers_for_card( $card_id ) ), 'window_end' => (int) get_post_meta( $card_id, 'offers_window_end', true ) );
		},
	) );
} );

// Register the offers routes in the public-POST rate-limit list.
add_filter( 'nadlan_hardening_public_post_routes', function ( $routes ) {
	$routes[] = '#^/nadlan/v1/offers$#';
	return $routes;
} );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$q = new WP_Query( array( 'post_type' => 'nadlan_offer', 'post_status' => 'private', 'fields' => 'ids', 'posts_per_page' => 1 ) );
	$out['offers'] = array( 'enabled' => nadlan_offers_enabled(), 'total_offers' => (int) $q->found_posts );
	wp_reset_postdata();
	return $out;
} );
