<?php
/**
 * nadlan-config — Catalog meta (v1.5.0)
 *
 * Registers REST-exposed post meta for the directory "cards":
 *   - nadlan_project       (real-estate projects / developments)
 *   - nadlan_professional  (contractors + service givers: kablan, shamai, bedek-bait, etc.)
 * plus the SHARED claim/ownership meta on all three card CPTs (property/project/professional)
 * that powers the free-card → claim → upgrade funnel.
 *
 * Design: parallels nadlan_config_register_property_meta(). Public read meta is
 * show_in_rest true; write auth requires edit_posts EXCEPT claim_status/owner which
 * are managed server-side via the claim flow (inc/claim.php), so they are read-only
 * over REST (auth_callback false for writes).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cards_register_meta_set' ) ) {
	/**
	 * Helper: register a {key=>type} map as single, REST-exposed meta on a post type.
	 *
	 * @param string $post_type
	 * @param array  $fields   key => WP meta type
	 * @param bool   $writable whether REST clients with edit_posts may write
	 */
	function nadlan_cards_register_meta_set( $post_type, $fields, $writable = true ) {
		foreach ( $fields as $key => $type ) {
			register_post_meta( $post_type, $key, array(
				'show_in_rest'  => true,
				'single'        => true,
				'type'          => $type,
				'auth_callback' => $writable
					? function () { return current_user_can( 'edit_posts' ); }
					: '__return_false',
			) );
		}
	}
}

if ( ! function_exists( 'nadlan_cards_register_meta' ) ) {
	function nadlan_cards_register_meta() {

		/* ---- PROJECT fields ---- */
		nadlan_cards_register_meta_set( 'nadlan_project', array(
			'developer_name'  => 'string',  // יזם
			'contractor_name' => 'string',  // קבלן מבצע
			'address'         => 'string',
			'city'            => 'string',
			'neighborhood'    => 'string',
			'gush'            => 'string',   // גוש
			'helka'           => 'string',   // חלקה
			'project_type'    => 'string',   // new|tama38|pinui_binui|mehir_lamishtaken|other
			'project_status'  => 'string',   // planning|marketing|construction|completed
			'num_units'       => 'integer',
			'num_buildings'   => 'integer',
			'num_floors'      => 'integer',
			'completion_year' => 'integer',
			'price_min'       => 'integer',
			'price_max'       => 'integer',
			'website'         => 'string',
			'phone'           => 'string',
			'lat'             => 'number',
			'lng'             => 'number',
			'photos_csv'      => 'string',
			'video_url'       => 'string',
			'tour3d_url'      => 'string',
			'source'          => 'string',
			'source_url'      => 'string',
		) );

		/* ---- PROFESSIONAL (contractor + service givers) fields ---- */
		nadlan_cards_register_meta_set( 'nadlan_professional', array(
			'profession'      => 'string',  // kablan|shamai|bedek_bait|mashkanta|architect|lawyer|inspector|other
			'registry_number' => 'string',  // מס' רשם הקבלנים
			'classification'  => 'string',   // סיווג (ענף + היקף)
			'license_number'  => 'string',
			'company_name'    => 'string',
			'address'         => 'string',
			'city'            => 'string',
			'areas_served'    => 'string',   // CSV of cities/regions
			'phone'           => 'string',
			'email'           => 'string',
			'website'         => 'string',
			'years_active'    => 'integer',
			'project_count'   => 'integer',
			'rating'          => 'number',
			'reviews_count'   => 'integer',
			'photos_csv'      => 'string',
			'logo_url'        => 'string',
			'source'          => 'string',
			'source_url'      => 'string',
		) );

		/* ---- SHARED claim / ownership / provenance meta (all card CPTs) ----
		 * claim_status + owner_user_id are server-managed (read-only over REST).
		 * source_id enables idempotent re-import (dedupe). is_demo flags seeded
		 * sample cards so they can be bulk-removed and never mistaken for real data.
		 */
		$shared_readonly = array(
			'claim_status'  => 'string',   // unclaimed|pending|verified
			'owner_user_id' => 'integer',
			'verified_at'   => 'integer',
		);
		$shared_writable = array(
			'source_id'     => 'string',   // stable external id for upsert dedupe
			'is_demo'       => 'boolean',
			'data_quality'  => 'string',   // stub|enriched  (drives thin-content noindex)
		);
		foreach ( array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ) as $pt ) {
			nadlan_cards_register_meta_set( $pt, $shared_readonly, false );
			nadlan_cards_register_meta_set( $pt, $shared_writable, true );
		}
	}
}
add_action( 'init', 'nadlan_cards_register_meta', 13 );

/**
 * Default new cards to claim_status=unclaimed so the claim CTA shows and queries
 * by status work from day one.
 */
if ( ! function_exists( 'nadlan_cards_default_claim_status' ) ) {
	function nadlan_cards_default_claim_status( $post_id, $post ) {
		if ( wp_is_post_revision( $post_id ) || wp_is_post_autosave( $post_id ) ) { return; }
		if ( ! in_array( $post->post_type, array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ), true ) ) { return; }
		if ( get_post_meta( $post_id, 'claim_status', true ) === '' ) {
			update_post_meta( $post_id, 'claim_status', 'unclaimed' );
		}
	}
}
add_action( 'save_post', 'nadlan_cards_default_claim_status', 5, 2 );
