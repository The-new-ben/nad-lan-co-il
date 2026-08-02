<?php
/**
 * Pretty tour URLs.
 *
 * The standalone 3D experiences live as flat HTML in the uploads library, which
 * is fine for serving but ugly for sharing: a link that says wp-content/uploads
 * in a pitch to a developer reads as internals, not product. /tour/{slug}/
 * streams the same file from a clean path.
 *
 * The files are streamed verbatim - no <base> injection - because both tours
 * reference their models by absolute URL, and Somail carries a bare "?rm=0"
 * link that a <base> tag would silently redirect into the uploads folder.
 * Query strings (?demo=1) pass through untouched.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_tour_map' ) ) {
	/** Allowlist: slug => path under the uploads basedir. Nothing else is served. */
	function nadlan_tour_map() {
		return array(
			'sde-dov' => '2026/07/sde-dov-tour.html',
			'somail'  => '2026/07/somail-tour.html',
		);
	}
}

add_action( 'init', function () {
	add_rewrite_rule( '^tour/([a-z0-9-]+)/?$', 'index.php?nadlan_tour=$matches[1]', 'top' );
	/* rules regenerate once per plugin version, so new tours appear without a
	   manual permalink save */
	if ( get_option( 'nadlan_tour_routes_flushed' ) !== NADLAN_CONFIG_VERSION ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_tour_routes_flushed', NADLAN_CONFIG_VERSION );
	}
} );

add_filter( 'query_vars', function ( $vars ) {
	$vars[] = 'nadlan_tour';
	return $vars;
} );

add_action( 'template_redirect', function () {
	$slug = (string) get_query_var( 'nadlan_tour' );
	if ( '' === $slug ) {
		return;
	}
	$map = nadlan_tour_map();
	if ( ! isset( $map[ $slug ] ) ) {
		status_header( 404 );
		exit;
	}
	$u    = wp_get_upload_dir();
	$file = trailingslashit( $u['basedir'] ) . $map[ $slug ];
	if ( ! file_exists( $file ) ) {
		status_header( 404 );
		exit;
	}
	header( 'Content-Type: text/html; charset=utf-8' );
	header( 'Cache-Control: public, max-age=300' );
	readfile( $file ); // phpcs:ignore WordPress.WP.AlternativeFunctions
	exit;
} );
