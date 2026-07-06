<?php
/**
 * nadlan-config - close-out seams, privacy, and endpoint hardening (v1.51.0).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_hardening_client_key' ) ) {
	function nadlan_hardening_client_key() {
		$ip = '';
		foreach ( array( 'HTTP_CF_CONNECTING_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR' ) as $k ) {
			if ( ! empty( $_SERVER[ $k ] ) ) {
				$ip = (string) wp_unslash( $_SERVER[ $k ] );
				break;
			}
		}
		if ( strpos( $ip, ',' ) !== false ) {
			$parts = explode( ',', $ip );
			$ip = trim( $parts[0] );
		}
		$user = get_current_user_id();
		return $user ? 'u' . $user : 'ip' . md5( substr( $ip, 0, 80 ) );
	}
}

if ( ! function_exists( 'nadlan_anthropic_messages_url' ) ) {
	function nadlan_anthropic_messages_url() {
		return esc_url_raw( apply_filters( 'nadlan_anthropic_messages_url', get_option( 'nadlan_anthropic_messages_url', 'https://api.anthropic.com/v1/messages' ) ) );
	}
}

if ( ! function_exists( 'nadlan_hardening_public_post_routes' ) ) {
	function nadlan_hardening_public_post_routes() {
		return apply_filters( 'nadlan_hardening_public_post_routes', array(
			'#^/nadlan/v1/lead$#',
			'#^/nadlan/v1/claim$#',
			'#^/nadlan/v1/saved-search$#',
			'#^/nadlan/v1/review-submit$#',
			'#^/nadlan/v1/concierge$#',
			'#^/nadlan/v1/concierge-lead$#',
			'#^/nadlan/v1/referral/route$#',
			'#^/nadlan/v1/referral/[a-z0-9]+/accept$#',
			'#^/nadlan/v1/referral/[a-z0-9]+/status$#',
			'#^/auctions/v1/[0-9]+/bids$#',
		) );
	}
}

if ( ! function_exists( 'nadlan_hardening_route_is_limited' ) ) {
	function nadlan_hardening_route_is_limited( $route ) {
		foreach ( nadlan_hardening_public_post_routes() as $pattern ) {
			if ( preg_match( $pattern, $route ) ) { return true; }
		}
		return false;
	}
}

if ( ! function_exists( 'nadlan_hardening_rate_limit' ) ) {
	function nadlan_hardening_rate_limit( $bucket, $limit = 8, $window = MINUTE_IN_SECONDS ) {
		$bucket = sanitize_key( (string) $bucket );
		$key = 'nadlan_postrl_' . md5( $bucket . '|' . nadlan_hardening_client_key() );
		$count = (int) get_transient( $key );
		if ( $count >= $limit ) { return false; }
		set_transient( $key, $count + 1, $window );
		return true;
	}
}

add_filter( 'rest_pre_dispatch', function ( $result, $server, $request ) {
	if ( strtoupper( $request->get_method() ) !== 'POST' ) { return $result; }
	$route = (string) $request->get_route();
	if ( ! nadlan_hardening_route_is_limited( $route ) ) { return $result; }
	$limit = (int) apply_filters( 'nadlan_hardening_public_post_limit', 8, $route );
	$window = (int) apply_filters( 'nadlan_hardening_public_post_window', MINUTE_IN_SECONDS, $route );
	if ( ! nadlan_hardening_rate_limit( $route, max( 1, $limit ), max( 10, $window ) ) ) {
		return new WP_Error( 'nadlan_rate_limited', 'rate_limited', array( 'status' => 429 ) );
	}
	return $result;
}, 10, 3 );

add_filter( 'rest_post_dispatch', function ( $response, $server, $request ) {
	if ( strtoupper( $request->get_method() ) !== 'GET' ) { return $response; }
	if ( preg_match( '#^/nadlan/v1/(directory|projects|suggest|map|avm|nl-search)$#', (string) $request->get_route() ) ) {
		do_action( 'nadlan_search_executed', $request->get_params(), get_current_user_id() );
	}
	return $response;
}, 10, 3 );

if ( ! function_exists( 'nadlan_maybe_fire_after_lead_closed' ) ) {
	function nadlan_maybe_fire_after_lead_closed( $meta_id, $object_id, $meta_key, $meta_value ) {
		if ( get_post_type( $object_id ) !== 'nadlan_lead' ) { return; }
		if ( ! in_array( $meta_key, array( 'status', 'lead_status', 'deal_status' ), true ) ) { return; }
		$value = sanitize_key( (string) $meta_value );
		if ( ! in_array( $value, array( 'closed', 'won', 'lost', 'paid' ), true ) ) { return; }
		if ( get_post_meta( $object_id, '_nadlan_after_lead_closed_fired', true ) ) { return; }
		update_post_meta( $object_id, '_nadlan_after_lead_closed_fired', time() );
		do_action( 'nadlan_after_lead_closed', (int) $object_id );
	}
}
add_action( 'added_post_meta', 'nadlan_maybe_fire_after_lead_closed', 10, 4 );
add_action( 'updated_post_meta', 'nadlan_maybe_fire_after_lead_closed', 10, 4 );

if ( ! function_exists( 'nadlan_build_real_estate_listing_jsonld' ) ) {
	function nadlan_build_real_estate_listing_jsonld( $post_id ) {
		$post_id = absint( $post_id );
		if ( ! $post_id || get_post_type( $post_id ) !== 'nadlan_property' ) { return array(); }
		$g = function ( $key ) use ( $post_id ) { return get_post_meta( $post_id, $key, true ); };
		$data = array_filter( array(
			'@context'   => 'https://schema.org',
			'@type'      => 'RealEstateListing',
			'name'       => get_the_title( $post_id ),
			'url'        => get_permalink( $post_id ),
			'datePosted' => get_the_date( 'c', $post_id ),
			'address'    => array_filter( array(
				'@type'           => 'PostalAddress',
				'streetAddress'   => $g( 'address' ) ?: null,
				'addressLocality' => $g( 'city' ) ?: null,
				'addressCountry'  => 'IL',
			) ),
			'floorSize'  => (float) $g( 'sqm' ) > 0 ? array(
				'@type'    => 'QuantitativeValue',
				'value'    => (float) $g( 'sqm' ),
				'unitCode' => 'MTK',
			) : null,
		) );
		if ( (float) $g( 'price' ) > 0 ) {
			$data['offers'] = array(
				'@type' => 'Offer',
				'price' => (float) $g( 'price' ),
				'priceCurrency' => 'ILS',
				'availability' => 'https://schema.org/InStock',
			);
		}
		if ( (float) $g( 'lat' ) && (float) $g( 'lng' ) ) {
			$data['geo'] = array(
				'@type' => 'GeoCoordinates',
				'latitude' => (float) $g( 'lat' ),
				'longitude' => (float) $g( 'lng' ),
			);
		}
		return apply_filters( 'nadlan_real_estate_listing_jsonld', $data, $post_id );
	}
}

add_filter( 'wp_privacy_personal_data_exporters', function ( $exporters ) {
	$exporters['nadlan-leads'] = array(
		'exporter_friendly_name' => 'NadLan leads',
		'callback'               => 'nadlan_privacy_export_leads',
	);
	$exporters['nadlan-ai-log'] = array(
		'exporter_friendly_name' => 'NadLan AI log',
		'callback'               => 'nadlan_privacy_export_ai_log',
	);
	return $exporters;
} );

if ( ! function_exists( 'nadlan_privacy_export_leads' ) ) {
	function nadlan_privacy_export_leads( $email_address, $page = 1 ) {
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_lead',
			'post_status'    => 'any',
			'fields'         => 'ids',
			'posts_per_page' => 25,
			'paged'          => max( 1, (int) $page ),
			'meta_query'     => array( array( 'key' => 'email', 'value' => sanitize_email( $email_address ) ) ),
		) );
		$data = array();
		foreach ( (array) $q->posts as $lead_id ) {
			$data[] = array(
				'group_id'    => 'nadlan-leads',
				'group_label' => 'NadLan leads',
				'item_id'     => 'lead-' . $lead_id,
				'data'        => array(
					array( 'name' => 'Lead ID', 'value' => (string) $lead_id ),
					array( 'name' => 'Name', 'value' => (string) get_post_meta( $lead_id, 'name', true ) ),
					array( 'name' => 'Email', 'value' => (string) get_post_meta( $lead_id, 'email', true ) ),
					array( 'name' => 'Phone', 'value' => (string) get_post_meta( $lead_id, 'phone', true ) ),
					array( 'name' => 'Goal', 'value' => (string) get_post_meta( $lead_id, 'goal', true ) ),
				),
			);
		}
		return array( 'data' => $data, 'done' => count( (array) $q->posts ) < 25 );
	}
}

if ( ! function_exists( 'nadlan_privacy_export_ai_log' ) ) {
	function nadlan_privacy_export_ai_log( $email_address, $page = 1 ) {
		$rows = get_option( 'nadlan_ai_quality_log', array() );
		$data = array();
		foreach ( is_array( $rows ) ? $rows : array() as $i => $row ) {
			if ( ! is_array( $row ) || sanitize_email( (string) ( $row['email'] ?? '' ) ) !== sanitize_email( $email_address ) ) { continue; }
			$data[] = array(
				'group_id'    => 'nadlan-ai-log',
				'group_label' => 'NadLan AI log',
				'item_id'     => 'ai-' . $i,
				'data'        => array(
					array( 'name' => 'Timestamp', 'value' => (string) ( $row['ts'] ?? '' ) ),
					array( 'name' => 'Escalated', 'value' => ! empty( $row['escalated'] ) ? 'yes' : 'no' ),
					array( 'name' => 'Grounded', 'value' => ! empty( $row['grounded'] ) ? 'yes' : 'no' ),
				),
			);
		}
		return array( 'data' => $data, 'done' => true );
	}
}

add_filter( 'wp_privacy_personal_data_erasers', function ( $erasers ) {
	$erasers['nadlan-leads'] = array(
		'eraser_friendly_name' => 'NadLan leads',
		'callback'             => 'nadlan_privacy_erase_leads',
	);
	$erasers['nadlan-ai-log'] = array(
		'eraser_friendly_name' => 'NadLan AI log',
		'callback'             => 'nadlan_privacy_erase_ai_log',
	);
	return $erasers;
} );

if ( ! function_exists( 'nadlan_privacy_erase_leads' ) ) {
	function nadlan_privacy_erase_leads( $email_address, $page = 1 ) {
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_lead',
			'post_status'    => 'any',
			'fields'         => 'ids',
			'posts_per_page' => 25,
			'paged'          => 1,
			'meta_query'     => array( array( 'key' => 'email', 'value' => sanitize_email( $email_address ) ) ),
		) );
		foreach ( (array) $q->posts as $lead_id ) {
			foreach ( array( 'name', 'email', 'phone' ) as $meta_key ) {
				update_post_meta( $lead_id, $meta_key, '[erased]' );
			}
			wp_update_post( array( 'ID' => $lead_id, 'post_content' => '', 'post_title' => 'Lead erased #' . $lead_id ) );
		}
		return array(
			'items_removed'  => false,
			'items_retained' => count( (array) $q->posts ) > 0,
			'messages'       => count( (array) $q->posts ) ? array( 'Lead contact fields erased, record retained for audit.' ) : array(),
			'done'           => count( (array) $q->posts ) < 25,
		);
	}
}

if ( ! function_exists( 'nadlan_privacy_erase_ai_log' ) ) {
	function nadlan_privacy_erase_ai_log( $email_address, $page = 1 ) {
		$rows = get_option( 'nadlan_ai_quality_log', array() );
		if ( ! is_array( $rows ) ) {
			return array( 'items_removed' => false, 'items_retained' => false, 'messages' => array(), 'done' => true );
		}
		$removed = false;
		foreach ( $rows as $i => $row ) {
			if ( is_array( $row ) && sanitize_email( (string) ( $row['email'] ?? '' ) ) === sanitize_email( $email_address ) ) {
				unset( $rows[ $i ] );
				$removed = true;
			}
		}
		if ( $removed ) { update_option( 'nadlan_ai_quality_log', array_values( $rows ), false ); }
		return array( 'items_removed' => $removed, 'items_retained' => false, 'messages' => array(), 'done' => true );
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['hardening'] = array(
		'loaded'            => true,
		'rate_limit_routes' => count( nadlan_hardening_public_post_routes() ),
		'privacy_hooks'     => true,
		'lead_closed_seam'  => has_action( 'added_post_meta', 'nadlan_maybe_fire_after_lead_closed' ) !== false,
	);
	return $out;
} );

/* OWNER LAW: no long dashes anywhere. wptexturize silently converts " - " to an
 * en dash and "--" to an em dash at render time, re-violating the law on every
 * page even when the stored content is clean. Straight characters, always. */
add_filter( 'run_wptexturize', '__return_false' );

/* SELF-HEALING REWRITE RULES (incident 2026-07-06: /projects/ + /professionals/
 * + all project singles 404ed after a deploy - CPT rewrite rules were flushed
 * during the plugin swap window). On every version change, re-flush once with
 * the plugin fully loaded so the catalog can never silently drop off the site. */
add_action( 'init', function () {
	if ( ! defined( 'NADLAN_CONFIG_VERSION' ) ) { return; }
	if ( get_option( 'nadlan_rw_flushed_for' ) !== NADLAN_CONFIG_VERSION ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_rw_flushed_for', NADLAN_CONFIG_VERSION, false );
	}
}, 99 );
