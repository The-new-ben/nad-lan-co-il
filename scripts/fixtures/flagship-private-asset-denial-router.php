<?php
/** Local HTTP fixture for the terminal flagship private-asset denial contract. */

declare(strict_types=1);

define( 'ABSPATH', __DIR__ . '/wordpress-stub/' );
define( 'OBJECT', 'OBJECT' );

final class WP_Error {
	private $code;

	public function __construct( $code, $message = '' ) {
		unset( $message );
		$this->code = (string) $code;
	}

	public function get_error_code() {
		return $this->code;
	}
}

function add_action( $hook, $callback, $priority = 10, $accepted_args = 1 ) {
	unset( $hook, $callback, $priority, $accepted_args );
}

function add_filter( $hook, $callback, $priority = 10, $accepted_args = 1 ) {
	unset( $hook, $callback, $priority, $accepted_args );
}

function wp_unslash( $value ) {
	return (string) $value;
}

function wp_parse_url( $value ) {
	return parse_url( (string) $value );
}

function is_wp_error( $value ) {
	return $value instanceof WP_Error;
}

function sanitize_key( $value ) {
	return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $value ) );
}

function status_header( $status ) {
	http_response_code( (int) $status );
}

function nocache_headers() {
	header( 'Expires: Wed, 11 Jan 1984 05:00:00 GMT', true );
	header( 'Cache-Control: no-cache, must-revalidate, max-age=0', true );
}

function esc_html__( $value ) {
	return (string) $value;
}

function wp_die( $message, $title = '', $args = array() ) {
	unset( $title );
	$status = isset( $args['response'] ) ? (int) $args['response'] : 500;
	status_header( $status );
	header( 'Content-Type: text/plain; charset=UTF-8', true );
	echo (string) $message; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- fixture sentinel.
	exit;
}

/* Force the descriptor-error branch without needing a WordPress database. */
function nadlan_flagship_v3_private_asset_descriptor( $project_contract_id, $requested_name ) {
	unset( $project_contract_id, $requested_name );
	return new WP_Error( 'fixture_private_asset_denied' );
}

require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/flagship-surface.php';

function fixture_dirty_nested_output_buffers() {
	ob_start();
	echo 'outer-buffer-junk'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- fixture sentinel.
	ob_start();
	echo 'inner-buffer-junk'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- fixture sentinel.
}

$request_path = isset( $_SERVER['REQUEST_URI'] ) ? (string) parse_url( (string) $_SERVER['REQUEST_URI'], PHP_URL_PATH ) : '/';

if ( '/fixture-health' === $request_path ) {
	http_response_code( 204 );
	exit;
}

if ( '/ordinary-page-validation' === $request_path ) {
	fixture_dirty_nested_output_buffers();
	nadlan_flagship_v3_fail_closed();
}

if ( '/direct-private-wrapper' === $request_path ) {
	fixture_dirty_nested_output_buffers();
	require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/assets/flagship-v3/private-assets/einstein-tower/model-hd.glb.asset.php';
	exit;
}

if ( '/flagship-private-asset' === $request_path || 0 === strpos( $request_path, '/flagship-private-asset/' ) ) {
	fixture_dirty_nested_output_buffers();
	nadlan_flagship_v3_private_asset_template();
	http_response_code( 500 );
	echo 'private-asset-handler-returned'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- unreachable regression sentinel.
	exit;
}

http_response_code( 404 );
echo 'fixture-route-not-found'; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- fixture sentinel.
