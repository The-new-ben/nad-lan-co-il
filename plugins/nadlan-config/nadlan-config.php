<?php
/**
 * Plugin Name: NadLan Config
 * Description: Lead-capture foundation: nadlan_lead CPT + lead-form handler + healthcheck. Read skills/nadlan-config-plugin.md.
 * Version: 1.1.0
 * Author: nad-lan.co.il
 * License: GPL-2.0+
 * Requires PHP: 7.4
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_config_register_cpt' ) ) {
	function nadlan_config_register_cpt() {
		register_post_type(
			'nadlan_lead',
			array(
				'labels'        => array(
					'name'          => 'NadLan Leads',
					'singular_name' => 'NadLan Lead',
				),
				'public'        => false,
				'show_ui'       => true,
				'show_in_menu'  => true,
				'menu_icon'     => 'dashicons-money-alt',
				'menu_position' => 25,
				'supports'      => array( 'title', 'editor', 'custom-fields' ),
			)
		);
	}
}
add_action( 'init', 'nadlan_config_register_cpt' );

if ( ! function_exists( 'nadlan_config_healthcheck' ) ) {
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
}
add_action( 'rest_api_init', 'nadlan_config_healthcheck' );

if ( ! function_exists( 'nadlan_config_healthcheck_response' ) ) {
	function nadlan_config_healthcheck_response() {
		return array(
			'plugin'              => 'nadlan-config',
			'version'             => '1.1.0',
			'cpt_present'         => post_type_exists( 'nadlan_lead' ),
			'lead_handler_loaded' => (bool) has_action( 'admin_post_nadlan_lead' ),
			'php_version'         => PHP_VERSION,
			'wp_version'          => get_bloginfo( 'version' ),
			'catalog'             => nadlan_config_catalog_status(),
		);
	}
}

if ( ! function_exists( 'nadlan_config_clean' ) ) {
	function nadlan_config_clean( $key ) {
		if ( ! isset( $_POST[ $key ] ) ) {
			return '';
		}
		return sanitize_text_field( wp_unslash( $_POST[ $key ] ) );
	}
}

if ( ! function_exists( 'nadlan_config_handle_lead' ) ) {
	function nadlan_config_handle_lead() {
		$nonce_raw = isset( $_POST['nadlan_nonce'] ) ? sanitize_text_field( wp_unslash( $_POST['nadlan_nonce'] ) ) : '';
		if ( $nonce_raw === '' || ! wp_verify_nonce( $nonce_raw, 'nadlan_lead' ) ) {
			wp_safe_redirect( add_query_arg( 'lead', 'bad_nonce', home_url( '/' ) ) );
			exit;
		}

		$email_raw   = isset( $_POST['lead_email'] ) ? wp_unslash( $_POST['lead_email'] ) : '';
		$message_raw = isset( $_POST['lead_message'] ) ? wp_unslash( $_POST['lead_message'] ) : '';

		$fields = array(
			'name'         => nadlan_config_clean( 'lead_name' ),
			'phone'        => nadlan_config_clean( 'lead_phone' ),
			'email'        => sanitize_email( $email_raw ),
			'goal'         => nadlan_config_clean( 'lead_goal' ),
			'city'         => nadlan_config_clean( 'lead_city' ),
			'budget'       => nadlan_config_clean( 'lead_budget' ),
			'timeline'     => nadlan_config_clean( 'lead_timeline' ),
			'message'      => sanitize_textarea_field( $message_raw ),
			'source_url'   => esc_url_raw( wp_get_referer() ? wp_get_referer() : home_url( '/' ) ),
			'utm_source'   => nadlan_config_clean( 'utm_source' ),
			'utm_campaign' => nadlan_config_clean( 'utm_campaign' ),
		);

		$name_for_title = $fields['name'] !== '' ? $fields['name'] : 'Lead';
		$goal_for_title = $fields['goal'] !== '' ? $fields['goal'] : 'General';
		$title          = $name_for_title . ' - ' . $goal_for_title . ' - ' . current_time( 'Y-m-d H:i' );

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
				$body  = "New lead on nad-lan.co.il\n";
				$body .= 'Name: ' . $fields['name'] . "\n";
				$body .= 'Phone: ' . $fields['phone'] . "\n";
				$body .= 'Email: ' . $fields['email'] . "\n";
				$body .= 'Goal: ' . $fields['goal'] . "\n";
				$body .= 'City: ' . $fields['city'] . "\n";
				$body .= 'Budget: ' . $fields['budget'] . "\n";
				$body .= 'Timeline: ' . $fields['timeline'] . "\n";
				$body .= 'Source: ' . $fields['source_url'] . "\n\n";
				$body .= 'Message: ' . $fields['message'] . "\n";
				wp_mail( $admin_email, 'NadLan lead: ' . $title, $body );
			}
		}

		wp_safe_redirect( add_query_arg( 'lead', 'received', home_url( '/' ) ) );
		exit;
	}
}
add_action( 'admin_post_nopriv_nadlan_lead', 'nadlan_config_handle_lead' );
add_action( 'admin_post_nadlan_lead',        'nadlan_config_handle_lead' );

/* ---------- v1.0.5: expose Yoast meta keys for REST writes ----------
 * Yoast SEO Free does not register its meta keys with show_in_rest, so bulk
 * editing meta descriptions / titles / cornerstone via the REST API silently
 * fails. We register them here (only as a REST-exposed mirror; Yoast still
 * owns the rendering). auth_callback requires edit_posts so only logged-in
 * editors can write. Read skills/nadlan-config-plugin.md.
 */
if ( ! function_exists( 'nadlan_config_register_yoast_meta' ) ) {
	function nadlan_config_register_yoast_meta() {
		$keys = array(
			'_yoast_wpseo_metadesc'       => 'string',
			'_yoast_wpseo_title'          => 'string',
			'_yoast_wpseo_focuskw'        => 'string',
			'_yoast_wpseo_is_cornerstone' => 'string',
		);
		$post_types = array( 'page', 'post' );
		foreach ( $post_types as $pt ) {
			foreach ( $keys as $key => $type ) {
				register_post_meta( $pt, $key, array(
					'show_in_rest'  => true,
					'single'        => true,
					'type'          => $type,
					'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
				) );
			}
		}
	}
}
add_action( 'init', 'nadlan_config_register_yoast_meta', 11 );

/* ---------- v1.1.0: Catalog CPTs (properties, projects, professionals) ----------
 * Foundation for the properties catalog. English labels (admin-only) per lessons.
 * function_exists guards per failure rules. Single capability addition per release.
 * See skills/properties-catalog.md for the full architecture and roadmap.
 */
if ( ! function_exists( 'nadlan_config_register_catalog_cpts' ) ) {
    function nadlan_config_register_catalog_cpts() {
        register_post_type( 'nadlan_property', array(
            'labels' => array(
                'name' => 'NadLan Properties', 'singular_name' => 'NadLan Property',
                'menu_name' => 'NadLan Properties',
            ),
            'public' => true, 'show_in_rest' => true,
            'has_archive' => 'properties', 'rewrite' => array( 'slug' => 'properties' ),
            'menu_icon' => 'dashicons-admin-home', 'menu_position' => 26,
            'supports' => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'excerpt' ),
        ) );
        register_post_type( 'nadlan_project', array(
            'labels' => array(
                'name' => 'NadLan Projects', 'singular_name' => 'NadLan Project',
            ),
            'public' => true, 'show_in_rest' => true,
            'has_archive' => 'projects', 'rewrite' => array( 'slug' => 'projects' ),
            'menu_icon' => 'dashicons-building', 'menu_position' => 27,
            'supports' => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'excerpt' ),
        ) );
        register_post_type( 'nadlan_professional', array(
            'labels' => array(
                'name' => 'NadLan Professionals', 'singular_name' => 'NadLan Professional',
            ),
            'public' => true, 'show_in_rest' => true,
            'has_archive' => 'professionals', 'rewrite' => array( 'slug' => 'professionals' ),
            'menu_icon' => 'dashicons-businessperson', 'menu_position' => 28,
            'supports' => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'excerpt' ),
        ) );
        register_taxonomy( 'nadlan_city', array( 'nadlan_property', 'nadlan_project' ),
            array( 'public' => true, 'hierarchical' => true, 'show_in_rest' => true,
                'rewrite' => array( 'slug' => 'cities' ),
                'labels' => array( 'name' => 'Cities', 'singular_name' => 'City' ) ) );
        register_taxonomy( 'nadlan_profession', array( 'nadlan_professional' ),
            array( 'public' => true, 'hierarchical' => false, 'show_in_rest' => true,
                'rewrite' => array( 'slug' => 'profession' ),
                'labels' => array( 'name' => 'Professions', 'singular_name' => 'Profession' ) ) );
    }
}
add_action( 'init', 'nadlan_config_register_catalog_cpts' );

/* Healthcheck reports catalog readiness too */
if ( ! function_exists( 'nadlan_config_catalog_status' ) ) {
    function nadlan_config_catalog_status() {
        return array(
            'nadlan_property_cpt' => post_type_exists( 'nadlan_property' ),
            'nadlan_project_cpt' => post_type_exists( 'nadlan_project' ),
            'nadlan_professional_cpt' => post_type_exists( 'nadlan_professional' ),
            'nadlan_city_tax' => taxonomy_exists( 'nadlan_city' ),
        );
    }
}
