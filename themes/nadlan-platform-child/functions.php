<?php
/**
 * NadLan Platform Child functions.
 * Presentation only. Business logic remains in nadlan-config and NadLan Platform Orchestrator.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function nlpc_theme_version() {
	$theme = wp_get_theme();
	return $theme && $theme->get( 'Version' ) ? $theme->get( 'Version' ) : '0.1.0';
}

add_action( 'wp_enqueue_scripts', function () {
	$parent = get_template_directory() . '/style.css';
	if ( file_exists( $parent ) ) {
		wp_enqueue_style(
			'nlpc-parent-style',
			get_template_directory_uri() . '/style.css',
			array(),
			(string) filemtime( $parent )
		);
	}

	$platform = get_stylesheet_directory() . '/assets/css/platform.css';
	wp_enqueue_style(
		'nlpc-platform',
		get_stylesheet_directory_uri() . '/assets/css/platform.css',
		array_filter( array( wp_style_is( 'nlpc-parent-style', 'registered' ) ? 'nlpc-parent-style' : null ) ),
		file_exists( $platform ) ? (string) filemtime( $platform ) : nlpc_theme_version()
	);
}, 60 );

add_filter( 'body_class', function ( $classes ) {
	$classes[] = 'nlpc-platform';
	if ( is_singular( 'nadlan_project' ) ) {
		$classes[] = 'nlpc-project-page';
	}
	if ( is_post_type_archive( 'nadlan_project' ) ) {
		$classes[] = 'nlpc-project-archive';
	}
	if ( is_front_page() ) {
		$classes[] = 'nlpc-home';
	}
	return $classes;
} );

add_action( 'after_setup_theme', function () {
	add_theme_support( 'wp-block-styles' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'editor-styles' );
	add_editor_style( 'assets/css/platform.css' );
} );
