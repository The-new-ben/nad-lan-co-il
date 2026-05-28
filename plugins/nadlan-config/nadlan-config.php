<?php
/**
 * Plugin Name: NadLan Config
 * Plugin URI: https://nad-lan.co.il
 * Description: Registers the nadlan_lead custom post type and the lead-form admin-post handler for nad-lan.co.il. Foundation for the lead-capture monetization model (see skills/monetization-lawyer-angle.md). Intentionally minimal — does NOT touch theme, does NOT add Abilities API yet (deferred to a separate plugin once the WP 7.0 ability registration signature is verified on this host).
 * Version: 1.0.1
 * Author: nad-lan.co.il
 * License: GPL-2.0+
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Requires PHP: 7.2
 * Requires at least: 6.7
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------- nadlan_lead CPT ---------- */
add_action( 'init', function () {
	register_post_type( 'nadlan_lead', array(
		'labels'          => array(
			'name'          => 'NadLan Leads',
			'singular_name' => 'NadLan Lead',
			'menu_name'     => 'NadLan Leads',
			'add_new'       => 'הוסף ליד',
			'add_new_item'  => 'ליד חדש',
			'edit_item'     => 'עריכת ליד',
			'view_item'     => 'צפייה בליד',
			'search_items'  => 'חיפוש לידים',
		),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => true,
		'show_in_rest'    => false,
		'menu_position'   => 25,
		'menu_icon'       => 'dashicons-money-alt',
		'supports'        => array( 'title', 'editor', 'custom-fields' ),
		'capability_type' => 'post',
		'map_meta_cap'    => true,
	) );
} );

/* ---------- Lead-form helper ---------- */
function nadlan_config_clean( $key ) {
	return isset( $_POST[ $key ] ) ? sanitize_text_field( wp_unslash( $_POST[ $key ] ) ) : '';
}

/* ---------- Lead-form admin-post handler ---------- */
function nadlan_config_handle_lead() {
	if ( ! isset( $_POST['nadlan_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_nonce'] ) ), 'nadlan_lead' ) ) {
		wp_safe_redirect( add_query_arg( 'lead', 'bad_nonce', home_url( '/' ) ) );
		exit;
	}

	$fields = array(
		'name'         => nadlan_config_clean( 'lead_name' ),
		'phone'        => nadlan_config_clean( 'lead_phone' ),
		'email'        => isset( $_POST['lead_email'] ) ? sanitize_email( wp_unslash( $_POST['lead_email'] ) ) : '',
		'goal'         => nadlan_config_clean( 'lead_goal' ),
		'city'         => nadlan_config_clean( 'lead_city' ),
		'budget'       => nadlan_config_clean( 'lead_budget' ),
		'timeline'     => nadlan_config_clean( 'lead_timeline' ),
		'message'      => isset( $_POST['lead_message'] ) ? sanitize_textarea_field( wp_unslash( $_POST['lead_message'] ) ) : '',
		'source_url'   => esc_url_raw( wp_get_referer() ? wp_get_referer() : home_url( '/' ) ),
		'utm_source'   => nadlan_config_clean( 'utm_source' ),
		'utm_campaign' => nadlan_config_clean( 'utm_campaign' ),
	);

	$title = sprintf( '%s - %s - %s',
		$fields['name'] ? $fields['name'] : 'Lead',
		$fields['goal'] ? $fields['goal'] : 'General',
		current_time( 'Y-m-d H:i' )
	);

	$lead_id = wp_insert_post( array(
		'post_type'    => 'nadlan_lead',
		'post_status'  => 'private',
		'post_title'   => $title,
		'post_content' => $fields['message'],
	), true );

	if ( ! is_wp_error( $lead_id ) ) {
		foreach ( $fields as $k => $v ) {
			update_post_meta( $lead_id, $k, $v );
		}
		$admin_email = get_option( 'admin_email' );
		if ( $admin_email ) {
			wp_mail( $admin_email, 'NadLan lead: ' . $title, print_r( $fields, true ) );
		}
	}

	wp_safe_redirect( add_query_arg( 'lead', 'received', home_url( '/' ) ) );
	exit;
}
add_action( 'admin_post_nopriv_nadlan_lead', 'nadlan_config_handle_lead' );
add_action( 'admin_post_nadlan_lead',        'nadlan_config_handle_lead' );

/* ---------- Healthcheck: a tiny REST endpoint that confirms this plugin loaded ---------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/healthcheck', array(
		'methods'  => 'GET',
		'callback' => function () {
			return array(
				'plugin'       => 'nadlan-config',
				'version'      => '1.0.1',
				'cpt_present'  => post_type_exists( 'nadlan_lead' ),
				'php_version'  => PHP_VERSION,
				'wp_version'   => get_bloginfo( 'version' ),
				'timestamp'    => current_time( 'c' ),
			);
		},
		'permission_callback' => '__return_true',
	) );
} );
