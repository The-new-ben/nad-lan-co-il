<?php
/**
 * Plugin Name: NadLan Config
 * Description: Lead-capture foundation for nad-lan.co.il. Registers the nadlan_lead CPT and the public lead-form admin-post handler. Read skills/nadlan-config-plugin.md before editing.
 * Version: 1.0.3
 * Author: nad-lan.co.il
 * License: GPL-2.0+
 * Requires PHP: 7.4
 * Requires at least: 6.7
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/* ---------- nadlan_lead CPT (English labels; admin-only) ---------- */
function nadlan_config_register_cpt() {
	register_post_type(
		'nadlan_lead',
		array(
			'labels'       => array(
				'name'          => 'NadLan Leads',
				'singular_name' => 'NadLan Lead',
			),
			'public'       => false,
			'show_ui'      => true,
			'show_in_menu' => true,
			'menu_icon'    => 'dashicons-money-alt',
			'menu_position'=> 25,
			'supports'     => array( 'title', 'editor', 'custom-fields' ),
		)
	);
}
add_action( 'init', 'nadlan_config_register_cpt' );

/* ---------- Healthcheck REST endpoint ---------- */
function nadlan_config_healthcheck() {
	register_rest_route(
		'nadlan/v1',
		'/healthcheck',
		array(
			'methods'             => 'GET',
			'callback'            => 'nadlan_config_healthcheck_response',
			'permission_callback' => '__return_true',
		)
	);
}
add_action( 'rest_api_init', 'nadlan_config_healthcheck' );

function nadlan_config_healthcheck_response() {
	return array(
		'plugin'              => 'nadlan-config',
		'version'             => '1.0.3',
		'cpt_present'         => post_type_exists( 'nadlan_lead' ),
		'lead_handler_loaded' => has_action( 'admin_post_nadlan_lead' ) ? true : false,
		'php_version'         => PHP_VERSION,
		'wp_version'          => get_bloginfo( 'version' ),
	);
}

/* ---------- Lead-form helper ---------- */
function nadlan_config_clean( $key ) {
	if ( ! isset( $_POST[ $key ] ) ) {
		return '';
	}
	return sanitize_text_field( wp_unslash( $_POST[ $key ] ) );
}

/* ---------- Lead-form admin-post handler ---------- *
 * Public form should POST to /wp-admin/admin-post.php with:
 *   action=nadlan_lead
 *   nadlan_nonce=<wp_create_nonce('nadlan_lead')>
 *   lead_name, lead_phone, lead_email, lead_goal, lead_city,
 *   lead_budget, lead_timeline, lead_message (+ optional utm_source, utm_campaign)
 */
function nadlan_config_handle_lead() {
	$nonce_ok = isset( $_POST['nadlan_nonce'] )
		&& wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_nonce'] ) ), 'nadlan_lead' );

	if ( ! $nonce_ok ) {
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
		'ip_hash'      => isset( $_SERVER['REMOTE_ADDR'] ) ? wp_hash( $_SERVER['REMOTE_ADDR'] . get_option( 'admin_email' ) ) : '',
	);

	$title_name = $fields['name'] !== '' ? $fields['name'] : 'Lead';
	$title_goal = $fields['goal'] !== '' ? $fields['goal'] : 'General';
	$title      = sprintf( '%s - %s - %s', $title_name, $title_goal, current_time( 'Y-m-d H:i' ) );

	$lead_id = wp_insert_post(
		array(
			'post_type'    => 'nadlan_lead',
			'post_status'  => 'private',
			'post_title'   => $title,
			'post_content' => $fields['message'],
		),
		true
	);

	if ( ! is_wp_error( $lead_id ) ) {
		foreach ( $fields as $k => $v ) {
			if ( $v !== '' ) {
				update_post_meta( $lead_id, $k, $v );
			}
		}

		$admin_email = get_option( 'admin_email' );
		if ( $admin_email ) {
			$body  = "New lead on nad-lan.co.il\n\n";
			$body .= 'Time:    ' . current_time( 'Y-m-d H:i' ) . "\n";
			$body .= 'Name:    ' . $fields['name']  . "\n";
			$body .= 'Phone:   ' . $fields['phone'] . "\n";
			$body .= 'Email:   ' . $fields['email'] . "\n";
			$body .= 'Goal:    ' . $fields['goal']  . "\n";
			$body .= 'City:    ' . $fields['city']  . "\n";
			$body .= 'Budget:  ' . $fields['budget']   . "\n";
			$body .= 'When:    ' . $fields['timeline'] . "\n";
			$body .= 'Source:  ' . $fields['source_url'] . "\n";
			$body .= "\nMessage:\n" . $fields['message'] . "\n";
			wp_mail( $admin_email, 'NadLan lead: ' . $title, $body );
		}
	}

	wp_safe_redirect( add_query_arg( 'lead', 'received', home_url( '/' ) ) );
	exit;
}
add_action( 'admin_post_nopriv_nadlan_lead', 'nadlan_config_handle_lead' );
add_action( 'admin_post_nadlan_lead',        'nadlan_config_handle_lead' );

/* ---------- Filter to expose the nonce to themes/blocks via [nadlan_lead_nonce] shortcode ---------- *
 * The Codex-built homepage form uses raw HTML inside a Gutenberg block. To make the nonce
 * available without writing PHP into the block, register a tiny shortcode the block can call.
 */
function nadlan_config_nonce_shortcode() {
	return '<input type="hidden" name="nadlan_nonce" value="' . esc_attr( wp_create_nonce( 'nadlan_lead' ) ) . '">'
		 . '<input type="hidden" name="action" value="nadlan_lead">';
}
add_shortcode( 'nadlan_lead_nonce', 'nadlan_config_nonce_shortcode' );
