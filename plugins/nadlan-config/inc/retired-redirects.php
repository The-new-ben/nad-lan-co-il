<?php
/**
 * nadlan-config - RETIRED PAGES, 301 to the nearest general page (1.72.697).
 * The site's standing rule is no redirects. This file exists only for pages the owner retired by name and for which he ordered a
 * 301 himself: Ben, 17.11.2026, Meital Katsir's listings, her broker mini-site (he/en/fr/ru) and her broker card. The pages are
 * drafts (kept, restorable), and their old addresses send visitors to the matching general page.
 * Data: assets/redirects/retired.json {"map": {"/old/path/": "/target/"}}. Exact path match only; nothing else on the site is touched.
 * Loaded by inc/directory.php (only if present).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_retired_map' ) ) {

	function nadlan_retired_map() {
		static $m = null;
		if ( null !== $m ) { return $m; }
		$f = dirname( __DIR__ ) . '/assets/redirects/retired.json';
		$j = is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : null;
		$m = ( is_array( $j ) && ! empty( $j['map'] ) && is_array( $j['map'] ) ) ? $j['map'] : array();
		return $m;
	}

	add_action( 'template_redirect', function () {
		if ( is_admin() || ! isset( $_SERVER['REQUEST_URI'] ) ) { return; }
		$path = (string) wp_parse_url( wp_unslash( $_SERVER['REQUEST_URI'] ), PHP_URL_PATH );
		$path = rawurldecode( $path );
		if ( '' === $path ) { return; }
		if ( '/' !== substr( $path, -1 ) ) { $path .= '/'; }
		$m = nadlan_retired_map();
		if ( ! isset( $m[ $path ] ) ) { return; }
		if ( is_user_logged_in() && current_user_can( 'edit_posts' ) && isset( $_GET['preview'] ) ) { return; } // an editor can still preview the draft
		wp_redirect( home_url( $m[ $path ] ), 301, 'nad-lan.co.il' );
		exit;
	}, 1 );
}
