<?php
/**
 * Plugin Name: NadLan Config
 * Description: Registers nadlan_lead CPT.
 * Version: 1.0.2
 * Author: nad-lan.co.il
 * License: GPL-2.0+
 * Requires PHP: 7.2
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

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
			'supports'     => array( 'title', 'editor', 'custom-fields' ),
		)
	);
}
add_action( 'init', 'nadlan_config_register_cpt' );

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
		'plugin'      => 'nadlan-config',
		'version'     => '1.0.2',
		'cpt_present' => post_type_exists( 'nadlan_lead' ),
		'php_version' => PHP_VERSION,
		'wp_version'  => get_bloginfo( 'version' ),
	);
}
