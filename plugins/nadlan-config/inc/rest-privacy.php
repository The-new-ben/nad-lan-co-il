<?php
/**
 * RestPrivacy (28.9.2026, Linear HAD-262): the site's own records stop showing their internal fields in the public
 * REST API. The audit of 23.9 found every professional's, listing's and project's record open at /wp-json/wp/v2/...
 * with its contact email and phone fields, the owner's user id, the claim status, the paid tier, boost and pin flags,
 * the drop keys and the private unit-journey marker. Counted on 28.9: no professional had an email or an owner filled
 * yet (0 of 2,846), one listing and one project had an owner id, one project a phone. The fields fill as soon as
 * brokers and professionals join, so they close now.
 *
 * Only for visitors who cannot edit the record: the owner, editors and the site's own scripts (app password) still get
 * everything, and the site's pages never read these endpoints (checked 28.9: no front-end call to wp/v2/nadlan_*).
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_rest_private_keys' ) ) {
	/** The meta keys a visitor never sees through the REST API. */
	function nadlan_rest_private_keys() {
		return array(
			'email', 'phone', 'owner_user_id', 'claim_status', 'boost_multiplier', 'is_pinned', 'is_sponsored',
			'paid_tier', 'priority_weight', 'nl_tier', 'nl_auto_publish', 'nl_drop_on', 'nl_drop_id', 'nl_card_key',
			'nl_broker_auto', 'data_quality', 'calendar_url', 'meeting_url', '_nadlan_private_unit_journey',
			'_nadlan_flagship_source_post_id',
		);
	}
}

foreach ( array( 'nadlan_professional', 'nadlan_property', 'nadlan_project' ) as $nadlan_rp_type ) {
	add_filter( 'rest_prepare_' . $nadlan_rp_type, function ( $response, $post ) {
		if ( ! ( $response instanceof WP_REST_Response ) ) {
			return $response;
		}
		if ( $post instanceof WP_Post && current_user_can( 'edit_post', $post->ID ) ) {
			return $response;
		}
		$data = $response->get_data();
		if ( isset( $data['meta'] ) && is_array( $data['meta'] ) ) {
			foreach ( nadlan_rest_private_keys() as $k ) {
				unset( $data['meta'][ $k ] );
			}
			$response->set_data( $data );
		}
		return $response;
	}, 20, 2 );
}
unset( $nadlan_rp_type );
