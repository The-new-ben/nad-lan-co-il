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

if ( ! function_exists( 'nadlan_offers_private_card' ) ) {
	function nadlan_offers_private_card( $card_id ) {
		$card_id = (int) $card_id;
		return $card_id > 0 && 'nadlan_project' === get_post_type( $card_id ) && (
			( function_exists( 'nadlan_unit_journey_is_private_lab' )
				&& nadlan_unit_journey_is_private_lab( $card_id ) )
			|| 'private-unit-journey-v2' === (string) get_post_meta( $card_id, '_nadlan_private_unit_journey', true )
		);
	}
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

if ( ! function_exists( 'nadlan_offers_capture_nonbinding_inquiry' ) ) {
	function nadlan_offers_capture_nonbinding_inquiry( $lead_id, $card_id, $fields ) {
		$lead_id = (int) $lead_id;
		$card_id = (int) $card_id;
		if ( $lead_id <= 0 || $card_id <= 0 || ! nadlan_offers_enabled() ) { return 0; }
		if ( nadlan_offers_private_card( $card_id ) ) { return 0; }
		if ( sanitize_key( (string) ( $fields['reservation_state'] ?? '' ) ) !== 'non_binding_inquiry' ) { return 0; }
		$card = get_post( $card_id );
		if ( ! $card || ! in_array( $card->post_type, nadlan_offers_card_types(), true ) ) { return 0; }
		if ( ! add_post_meta( $lead_id, 'nonbinding_offer_attempted', 1, true ) ) {
			return (int) get_post_meta( $lead_id, 'nonbinding_offer_id', true );
		}
		$oid = wp_insert_post( array(
			'post_type'   => 'nadlan_offer',
			'post_status' => 'private',
			'post_title'  => sprintf( 'בדיקת רכישה לא מחייבת #%d לנכס %d', $lead_id, $card_id ),
		), true );
		if ( ! $oid || is_wp_error( $oid ) ) { return 0; }
		foreach ( array(
			'offer_card_id'       => $card_id,
			'offer_amount'        => 0,
			'offer_name'          => sanitize_text_field( (string) ( $fields['name'] ?? '' ) ),
			'offer_phone'         => preg_replace( '/[^0-9+\-]/', '', (string) ( $fields['phone'] ?? '' ) ),
			'offer_email'         => sanitize_email( (string) ( $fields['email'] ?? '' ) ),
			'offer_message'       => sanitize_textarea_field( (string) ( $fields['message'] ?? '' ) ),
			'offer_status'        => 'non_binding_inquiry',
			'offer_source'        => 'project_3d',
			'offer_source_lead_id'=> $lead_id,
			'offer_unit'          => sanitize_text_field( (string) ( $fields['unit'] ?? '' ) ),
			'offer_floor'         => isset( $fields['floor'] ) && $fields['floor'] !== '' ? (int) $fields['floor'] : '',
			'offer_rooms'         => sanitize_text_field( (string) ( $fields['rooms'] ?? '' ) ),
			'offer_sqm'           => sanitize_text_field( (string) ( $fields['sqm'] ?? '' ) ),
			'offer_building'      => sanitize_text_field( (string) ( $fields['building'] ?? '' ) ),
			'offer_availability'  => sanitize_text_field( (string) ( $fields['availability'] ?? '' ) ),
			'offer_market_note'   => sanitize_textarea_field( (string) ( $fields['market_note'] ?? '' ) ),
			'offer_advisor'       => sanitize_key( (string) ( $fields['advisor'] ?? '' ) ),
			'offer_created_at'    => time(),
		) as $k => $v ) {
			if ( $v !== '' ) { update_post_meta( $oid, $k, $v ); }
		}
		update_post_meta( $lead_id, 'nonbinding_offer_id', (int) $oid );
		do_action( 'nadlan_offer_nonbinding_inquiry', (int) $oid, $lead_id, $card_id, $fields );
		return (int) $oid;
	}
}

add_action( 'nadlan_lead_e2e_captured', function ( $lead_id, $card_id, $fields ) {
	nadlan_offers_capture_nonbinding_inquiry( $lead_id, $card_id, is_array( $fields ) ? $fields : array() );
}, 10, 3 );

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/offers', array(
		'methods' => 'POST', 'permission_callback' => '__return_true',
		'callback' => function ( WP_REST_Request $req ) {
			if ( ! nadlan_offers_enabled() ) { return new WP_Error( 'offers_disabled', 'offers_disabled', array( 'status' => 404 ) ); }
			$p = $req->get_json_params(); if ( ! is_array( $p ) ) { $p = $req->get_params(); }
			$card_id = absint( $p['card_id'] ?? 0 );
			if ( nadlan_offers_private_card( $card_id ) ) {
				return new WP_Error( 'not_found', 'not found', array( 'status' => 404 ) );
			}
			if ( ! empty( $p['company'] ) ) { return array( 'ok' => true ); } // honeypot: pretend success
			$ip = sanitize_text_field( $_SERVER['REMOTE_ADDR'] ?? '0' );
			$rl = 'nadlan_offer_rl_' . md5( $ip );
			if ( (int) get_transient( $rl ) >= 5 ) { return new WP_Error( 'rate', 'יותר מדי הצעות, נסו מאוחר יותר.', array( 'status' => 429 ) ); }
			set_transient( $rl, (int) get_transient( $rl ) + 1, HOUR_IN_SECONDS );

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
			// Audit fix 2026-07-02: was a permanent option (never expired, grew
			// unbounded); a transient makes "within 24h" actually true.
			$existing = (int) get_transient( $guard );
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
			if ( nadlan_offers_private_card( $card_id ) ) {
				return new WP_Error( 'not_found', 'not found', array( 'status' => 404 ) );
			}
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
	$nb = new WP_Query( array(
		'post_type'      => 'nadlan_offer',
		'post_status'    => 'private',
		'fields'         => 'ids',
		'posts_per_page' => 1,
		'meta_query'     => array( array( 'key' => 'offer_status', 'value' => 'non_binding_inquiry' ) ),
	) );
	$out['offers'] = array(
		'enabled'              => nadlan_offers_enabled(),
		'total_offers'         => (int) $q->found_posts,
		'nonbinding_inquiries' => (int) $nb->found_posts,
	);
	wp_reset_postdata();
	return $out;
} );
