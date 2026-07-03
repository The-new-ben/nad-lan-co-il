<?php
/**
 * Project-page PREVIEW (2026-07-03) — proves the new modular project-page
 * design runs inside WordPress, not just as a standalone HTML file.
 *
 * A REST route serves the complete self-contained design (from
 * assets/preview/<slug>.html) with the Mapbox token injected from the keys hub
 * and the 3D model pointed at the plugin asset. A shortcode embeds it in an
 * isolated iframe so no theme CSS can collide with it.
 *
 * Usage: create a page and add  [nadlan_project_preview slug="duo"]
 * Preview URL (direct):  /wp-json/nadlan/v1/preview/duo
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_project_preview_render_html' ) ) {
	function nadlan_project_preview_render_html( $slug ) {
		$slug = preg_replace( '/[^a-z0-9\-]/', '', (string) $slug );
		$file = __DIR__ . '/../assets/preview/' . $slug . '.html';
		if ( ! $slug || ! file_exists( $file ) ) {
			return '';
		}
		$html  = (string) file_get_contents( $file );
		$token = (string) get_option( 'nadlan_mapbox_token', '' );
		$glb   = plugins_url( 'assets/preview/' . $slug . '.glb', dirname( __DIR__ ) . '/nadlan-config.php' );
		$html  = str_replace( '__MAPBOX_TOKEN__', esc_js( $token ), $html );
		$html  = str_replace( '__GLB_URL__', esc_url_raw( $glb ), $html );
		return $html;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/preview/(?P<slug>[a-z0-9\-]+)', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function ( $req ) {
			$html = nadlan_project_preview_render_html( $req['slug'] );
			if ( '' === $html ) {
				return new WP_Error( 'not_found', 'preview not found', array( 'status' => 404 ) );
			}
			header( 'Content-Type: text/html; charset=utf-8' );
			header( 'X-Frame-Options: SAMEORIGIN' );
			echo $html; // phpcs:ignore WordPress.Security.EscapeOutput
			exit;
		},
	) );
} );

if ( ! function_exists( 'nadlan_project_preview_shortcode' ) ) {
	function nadlan_project_preview_shortcode( $atts ) {
		$atts = shortcode_atts( array( 'slug' => 'duo', 'height' => '100vh' ), $atts, 'nadlan_project_preview' );
		$slug = preg_replace( '/[^a-z0-9\-]/', '', (string) $atts['slug'] );
		if ( ! $slug || ! file_exists( __DIR__ . '/../assets/preview/' . $slug . '.html' ) ) {
			return '';
		}
		$src = esc_url( rest_url( 'nadlan/v1/preview/' . $slug ) );
		$h   = preg_replace( '/[^0-9a-z%vhpx]/', '', (string) $atts['height'] );
		return '<iframe src="' . $src . '" title="נדלן — תצוגת פרויקט" loading="lazy" '
			. 'style="display:block;width:100%;height:' . esc_attr( $h ) . ';border:0;margin:0"></iframe>';
	}
}
add_shortcode( 'nadlan_project_preview', 'nadlan_project_preview_shortcode' );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['project_preview'] = array(
		'loaded'       => true,
		'duo_html'     => file_exists( __DIR__ . '/../assets/preview/duo.html' ),
		'duo_glb'      => file_exists( __DIR__ . '/../assets/preview/duo.glb' ),
		'route'        => rest_url( 'nadlan/v1/preview/duo' ),
		'token_set'    => (bool) get_option( 'nadlan_mapbox_token', '' ),
	);
	return $out;
} );
