<?php
/**
 * Plugin Name: NadLan Config
 * Description: Registers the nadlan_lead CPT, the lead-form admin-post handler,
 *              and the WordPress 7.0 Abilities API endpoints under nadlan/*.
 *              Lives in mu-plugins so it always loads regardless of theme state
 *              or UPress sync issues. Read skills/strategy-master.md before edits.
 * Version: 1.0.0
 * Author: nad-lan.co.il
 * License: GPL-2.0+
 *
 * To install: drop this single file into /wp-content/mu-plugins/ on the server.
 * No activation required — mu-plugins auto-load.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------- nadlan_lead CPT ---------- */
add_action( 'init', function () {
	register_post_type( 'nadlan_lead', array(
		'labels'       => array( 'name' => 'NadLan Leads', 'singular_name' => 'NadLan Lead' ),
		'public'       => false,
		'show_ui'      => true,
		'show_in_menu' => true,
		'menu_icon'    => 'dashicons-money-alt',
		'supports'     => array( 'title', 'editor', 'custom-fields' ),
	) );
} );

/* ---------- Lead-form handler ---------- */
function nadlan_config_clean( $key ) {
	return isset( $_POST[ $key ] ) ? sanitize_text_field( wp_unslash( $_POST[ $key ] ) ) : '';
}

function nadlan_config_handle_lead() {
	if ( ! isset( $_POST['nadlan_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_nonce'] ) ), 'nadlan_lead' ) ) {
		wp_safe_redirect( add_query_arg( 'lead', 'bad_nonce', home_url( '/' ) ) ); exit;
	}
	$fields = array(
		'name'     => nadlan_config_clean( 'lead_name' ),
		'phone'    => nadlan_config_clean( 'lead_phone' ),
		'email'    => sanitize_email( wp_unslash( $_POST['lead_email'] ?? '' ) ),
		'goal'     => nadlan_config_clean( 'lead_goal' ),
		'city'     => nadlan_config_clean( 'lead_city' ),
		'budget'   => nadlan_config_clean( 'lead_budget' ),
		'timeline' => nadlan_config_clean( 'lead_timeline' ),
		'message'  => sanitize_textarea_field( wp_unslash( $_POST['lead_message'] ?? '' ) ),
		'source_url'   => esc_url_raw( wp_get_referer() ?: home_url( '/' ) ),
		'utm_source'   => nadlan_config_clean( 'utm_source' ),
		'utm_campaign' => nadlan_config_clean( 'utm_campaign' ),
	);
	$title = sprintf( '%s - %s - %s', $fields['name'] ?: 'Lead', $fields['goal'] ?: 'General', current_time( 'Y-m-d H:i' ) );
	$id = wp_insert_post( array(
		'post_type'    => 'nadlan_lead',
		'post_status'  => 'private',
		'post_title'   => $title,
		'post_content' => $fields['message'],
	), true );
	if ( ! is_wp_error( $id ) ) {
		foreach ( $fields as $k => $v ) { update_post_meta( $id, $k, $v ); }
		wp_mail( get_option( 'admin_email' ), 'NadLan lead: ' . $title, print_r( $fields, true ) );
	}
	wp_safe_redirect( add_query_arg( 'lead', 'received', home_url( '/' ) ) ); exit;
}
add_action( 'admin_post_nopriv_nadlan_lead', 'nadlan_config_handle_lead' );
add_action( 'admin_post_nadlan_lead',        'nadlan_config_handle_lead' );

/* ---------- Abilities API (WP 7.0) ---------- */
add_action( 'init', function () {
	if ( ! function_exists( 'wp_register_ability' ) ) { return; }

	$empty_in = array( 'type' => 'object', 'properties' => new \stdClass(), 'additionalProperties' => false );

	wp_register_ability( 'nadlan/get-pillars', array(
		'label'        => 'List pillar pages',
		'description'  => 'Returns slug/title/url for nad-lan pillar pages (buying, selling, investment, mortgage, tax-legal, urban-renewal, professionals, new-projects, commercial).',
		'input_schema' => $empty_in,
		'output_schema'=> array( 'type' => 'array' ),
		'execute_callback'    => function () {
			$slugs = array(
				'buying-apartment','selling-apartment','investment-apartment',
				'real-estate-tax-advisor','real-estate-lawyer','urban-renewal',
				'professionals','new-projects','commercial-real-estate',
			);
			$out = array();
			foreach ( $slugs as $s ) {
				$p = get_page_by_path( $s );
				if ( $p ) { $out[] = array( 'slug' => $s, 'title' => get_the_title( $p ), 'url' => get_permalink( $p ) ); }
			}
			return $out;
		},
		'permission_callback' => '__return_true',
	) );

	wp_register_ability( 'nadlan/get-calculators', array(
		'label'        => 'List on-site calculators',
		'description'  => 'Returns slug/title/url for the five nad-lan calculator pages.',
		'input_schema' => $empty_in,
		'output_schema'=> array( 'type' => 'array' ),
		'execute_callback'    => function () {
			$slugs = array(
				'mortgage-calculator','purchase-tax-calculator','property-value-estimator',
				'investment-property-cashflow-calculator','apartment-purchase-cost-calculator',
			);
			$out = array();
			foreach ( $slugs as $s ) {
				$p = get_page_by_path( $s );
				if ( $p ) { $out[] = array( 'slug' => $s, 'title' => get_the_title( $p ), 'url' => get_permalink( $p ) ); }
			}
			return $out;
		},
		'permission_callback' => '__return_true',
	) );

	wp_register_ability( 'nadlan/get-cities', array(
		'label'        => 'List city / neighborhood pages',
		'description'  => 'Returns published Pages whose slug ends in -apartment-prices or -house-prices.',
		'input_schema' => $empty_in,
		'output_schema'=> array( 'type' => 'array' ),
		'execute_callback'    => function () {
			$q = new WP_Query( array( 'post_type' => 'page', 'post_status' => 'publish', 'posts_per_page' => 200, 'fields' => 'ids' ) );
			$out = array();
			foreach ( $q->posts as $id ) {
				$slug = get_post_field( 'post_name', $id );
				if ( str_ends_with( $slug, '-apartment-prices' ) || str_ends_with( $slug, '-house-prices' ) ) {
					$out[] = array( 'slug' => $slug, 'title' => get_the_title( $id ), 'url' => get_permalink( $id ) );
				}
			}
			return $out;
		},
		'permission_callback' => '__return_true',
	) );

	wp_register_ability( 'nadlan/get-lead-stats', array(
		'label'        => 'Lead-form counts 7/30/90d (no PII)',
		'description'  => 'Returns counts of nadlan_lead CPT entries over the last 7, 30, 90 days. manage_options gated.',
		'input_schema' => $empty_in,
		'output_schema'=> array( 'type' => 'object' ),
		'execute_callback'    => function () {
			$out = array();
			foreach ( array( 7, 30, 90 ) as $d ) {
				$q = new WP_Query( array(
					'post_type' => 'nadlan_lead', 'post_status' => 'any',
					'posts_per_page' => -1, 'fields' => 'ids',
					'date_query' => array( array( 'after' => $d . ' days ago' ) ),
				) );
				$out[ "last_{$d}_days" ] = (int) $q->found_posts;
			}
			return $out;
		},
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
	) );
}, 20 );
