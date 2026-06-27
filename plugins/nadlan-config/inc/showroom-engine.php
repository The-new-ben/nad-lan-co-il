<?php
/**
 * nadlan-config — Showroom Engine bridge (Claude Design port, slice 1).
 *
 * Mounts the data-driven showroom engine
 * (assets/showroom-engine/, ported from handoff/claude-design/2026-06-27-showroom-engine)
 * via a self-contained shortcode, so it can be previewed on a real WordPress page
 * WITHOUT touching the existing project-3d showroom. No stacking: this renders the
 * new engine only where the shortcode is placed.
 *
 *   [nadlan_showroom_engine]                       -> project page, ashira-sde-dov
 *   [nadlan_showroom_engine page="home"]           -> homepage gallery
 *   [nadlan_showroom_engine project="rainbow"]     -> a specific project
 *
 * Slice 1 renders from the bundled prototype payload (assets/showroom-engine/data.js)
 * with asset paths and the lead endpoint rewritten for this site. Slice 1b swaps the
 * payload source to live nadlan_project CMS meta (same window.NADLAN_SHOWROOM shape).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_showroom_engine_base_url' ) ) {
	function nadlan_showroom_engine_base_url() {
		// inc/ -> plugin root -> assets/showroom-engine/
		return plugins_url( 'assets/showroom-engine/', dirname( __DIR__ ) . '/nadlan-config.php' );
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_dir' ) ) {
	function nadlan_showroom_engine_dir() {
		return dirname( __DIR__ ) . '/assets/showroom-engine/';
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_payload_js' ) ) {
	/**
	 * Slice 1: read the bundled prototype payload and make it site-correct —
	 * resolve relative model/poster/facade paths to the plugin URL, and point the
	 * lead endpoint at this site's REST route. Returns a JS string that assigns
	 * window.NADLAN_SHOWROOM, or '' if the bundle is missing.
	 */
	function nadlan_showroom_engine_payload_js() {
		$file = nadlan_showroom_engine_dir() . 'data.js';
		if ( ! is_readable( $file ) ) { return ''; }
		$js = file_get_contents( $file );
		if ( $js === false ) { return ''; }
		$base = trailingslashit( nadlan_showroom_engine_base_url() );
		$js   = str_replace( 'engine/models/', $base . 'models/', $js );
		$js   = str_replace( '/wp-json/nadlan/v1/lead', esc_url_raw( rest_url( 'nadlan/v1/lead' ) ), $js );
		return $js;
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_shortcode' ) ) {
	function nadlan_showroom_engine_shortcode( $atts ) {
		$atts = shortcode_atts(
			array(
				'page'    => 'project',          // project | home
				'project' => 'ashira-sde-dov',   // initial project slug
			),
			$atts,
			'nadlan_showroom_engine'
		);
		$page = ( $atts['page'] === 'home' ) ? 'home' : 'project';
		$base = trailingslashit( nadlan_showroom_engine_base_url() );

		// styles
		wp_enqueue_style( 'nadlan-engine-tokens', $base . 'tokens.css', array(), '1.69.42' );
		wp_enqueue_style( 'nadlan-engine-css', $base . 'showroom.css', array( 'nadlan-engine-tokens' ), '1.69.42' );

		// model-viewer (module)
		wp_enqueue_script( 'nadlan-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js', array(), '4.0.0', true );
		wp_script_add_data( 'nadlan-model-viewer', 'type', 'module' );

		// i18n -> payload (inline, before) -> engine
		wp_enqueue_script( 'nadlan-engine-i18n', $base . 'i18n.js', array(), '1.69.42', true );
		wp_enqueue_script( 'nadlan-engine-core', $base . 'engine.js', array( 'nadlan-engine-i18n' ), '1.69.42', true );

		$payload = nadlan_showroom_engine_payload_js();
		if ( $payload !== '' ) {
			// optional initial project override from the shortcode
			$slug = sanitize_title( $atts['project'] );
			if ( $slug !== '' ) {
				$payload .= "\ntry{window.NADLAN_SHOWROOM.config.default_project=" . wp_json_encode( $slug ) . ";}catch(e){}";
			}
			wp_add_inline_script( 'nadlan-engine-core', $payload, 'before' );
		}

		return '<div id="nl-root" data-page="' . esc_attr( $page ) . '"></div>';
	}
}
add_shortcode( 'nadlan_showroom_engine', 'nadlan_showroom_engine_shortcode' );
