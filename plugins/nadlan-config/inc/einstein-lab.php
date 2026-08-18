<?php
/**
 * nadlan-config - Einstein showroom lab (the NEW 3D-page standard, prototyped
 * on one page before it becomes the fleet template).
 *
 * Owner order 2026-08-16 ("בנה"): full-height theater with nothing to scroll
 * inside, a floor tap that answers IN PLACE without the page jumping, the unit
 * card never covering the building, image tiles instead of text-only tool
 * doors, and reserved section heights so the site footer can never paint
 * mid-page while the engine boots.
 *
 * Scope law: EINSTEIN ONLY (post 4867). The shared engine is frozen - this
 * module builds around it with page-scoped CSS/JS and never reaches inside.
 * When the owner approves the look, this file's rules graduate into the
 * standard for every new 3D project page.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_einstein_lab_post_id' ) ) {
	function nadlan_einstein_lab_post_id() {
		return 4867;
	}
}

if ( ! function_exists( 'nadlan_einstein_lab_active' ) ) {
	function nadlan_einstein_lab_active() {
		return is_singular( 'nadlan_project' )
			&& (int) get_queried_object_id() === nadlan_einstein_lab_post_id();
	}
}

add_filter( 'body_class', function ( $classes ) {
	if ( nadlan_einstein_lab_active() ) {
		$classes[] = 'nlx-einstein-lab';
	}
	return $classes;
} );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nadlan_einstein_lab_active() ) {
		return;
	}
	$base = plugins_url( 'assets/einstein-lab/', dirname( __DIR__ ) . '/nadlan-config.php' );
	wp_enqueue_style( 'nadlan-einstein-lab', $base . 'lab.css', array(), NADLAN_CONFIG_VERSION );
	wp_enqueue_script( 'nadlan-einstein-lab', $base . 'lab.js', array(), NADLAN_CONFIG_VERSION, true );
}, 30 );
