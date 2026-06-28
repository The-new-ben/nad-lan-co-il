<?php
/**
 * Plugin Name: NadLan Platform Orchestrator
 * Description: Safe presentation and content orchestration layer for NadLan. Delegates project showroom rendering to the existing NadLan engine.
 * Version: 0.1.2
 * Author: NadLan
 * Text Domain: nadlan-platform-orchestrator
 * Requires at least: 6.5
 * Requires PHP: 8.1
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'NLPO_VERSION', '0.1.2' );
define( 'NLPO_FILE', __FILE__ );
define( 'NLPO_DIR', plugin_dir_path( __FILE__ ) );
define( 'NLPO_URL', plugin_dir_url( __FILE__ ) );

require_once NLPO_DIR . 'inc/helpers.php';
require_once NLPO_DIR . 'inc/shortcodes.php';
require_once NLPO_DIR . 'inc/admin.php';
require_once NLPO_DIR . 'inc/content-gaps.php';
require_once NLPO_DIR . 'inc/rest.php';

register_activation_hook( __FILE__, function () {
	update_option( 'nlpo_activated_at', current_time( 'mysql' ), false );
	if ( get_option( 'nlpo_auto_insert_home_band', null ) === null ) {
		update_option( 'nlpo_auto_insert_home_band', '0', false );
	}
} );

add_action( 'wp_enqueue_scripts', function () {
	$css = NLPO_DIR . 'assets/css/orchestrator.css';
	wp_enqueue_style( 'nlpo-orchestrator', NLPO_URL . 'assets/css/orchestrator.css', array(), file_exists( $css ) ? (string) filemtime( $css ) : NLPO_VERSION );
	$js = NLPO_DIR . 'assets/js/orchestrator.js';
	wp_enqueue_script( 'nlpo-orchestrator', NLPO_URL . 'assets/js/orchestrator.js', array(), file_exists( $js ) ? (string) filemtime( $js ) : NLPO_VERSION, true );
}, 70 );

/* Optional home band. OFF by default. Uses a unique wrapper and a guard to prevent duplication. */
add_filter( 'the_content', function ( $content ) {
	if ( is_admin() || ! is_front_page() || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	$preview = current_user_can( 'manage_options' )
		&& isset( $_GET['nlpo_preview'] )
		&& sanitize_text_field( wp_unslash( $_GET['nlpo_preview'] ) ) === '1';
	if ( get_option( 'nlpo_auto_insert_home_band', '0' ) !== '1' && ! $preview ) {
		return $content;
	}
	if ( strpos( $content, 'data-nlpo-home-projects' ) !== false ) {
		return $content;
	}
	try {
		$band = do_shortcode( '[nadlan_platform_home_projects limit="4"]' );
	} catch ( Throwable $e ) {
		error_log( 'NadLan Platform home band failed: ' . $e->getMessage() );
		return $content;
	}
	if ( ! is_string( $band ) || trim( $band ) === '' ) {
		return $content;
	}
	return $content . $band;
}, 30 );
