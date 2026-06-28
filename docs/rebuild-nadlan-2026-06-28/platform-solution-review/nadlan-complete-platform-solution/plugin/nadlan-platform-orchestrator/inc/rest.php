<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-platform/v1', '/content-gaps', array(
		'methods'             => WP_REST_Server::READABLE,
		'callback'            => function () {
			return rest_ensure_response( array(
				'ok'   => true,
				'gaps' => nlpo_scan_content_gaps( 120 ),
			) );
		},
		'permission_callback' => function () {
			return current_user_can( 'manage_options' );
		},
	) );
} );
