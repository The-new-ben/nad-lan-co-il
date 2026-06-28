<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }

function nlpo_has_nadlan_config() {
	return function_exists( 'nadlan_showroom_engine_shortcode' ) || function_exists( 'nadlan_showroom_engine_build_project' ) || post_type_exists( 'nadlan_project' );
}

function nlpo_languages() {
	return array( 'he' => '', 'en' => '-en', 'fr' => '-fr', 'ru' => '-ru', 'ar' => '-ar' );
}

function nlpo_base_project_slug( $slug ) {
	return preg_replace( '/-(en|fr|ru|ar)$/', '', (string) $slug );
}

function nlpo_self_lang_from_slug( $slug ) {
	foreach ( array( 'en', 'fr', 'ru', 'ar' ) as $lang ) {
		if ( substr( (string) $slug, -3 ) === '-' . $lang ) {
			return $lang;
		}
	}
	return 'he';
}

function nlpo_project_language_posts( $post ) {
	$post = get_post( $post );
	if ( ! $post ) { return array(); }
	$base = nlpo_base_project_slug( $post->post_name );
	$out = array();
	foreach ( nlpo_languages() as $lang => $suffix ) {
		$p = get_page_by_path( $base . $suffix, OBJECT, 'nadlan_project' );
		if ( $p && get_post_status( $p ) === 'publish' ) {
			$out[ $lang ] = $p;
		}
	}
	return $out;
}

function nlpo_project_image( $post_id ) {
	$keys = array( 'project_model_poster', 'project_hero_image', 'project_image', 'thumbnail_url' );
	foreach ( $keys as $key ) {
		$value = (string) get_post_meta( $post_id, $key, true );
		if ( $value !== '' ) { return esc_url( $value ); }
	}
	$thumb = get_the_post_thumbnail_url( $post_id, 'large' );
	return $thumb ? esc_url( $thumb ) : '';
}

function nlpo_project_excerpt( $post_id ) {
	$custom = (string) get_post_meta( $post_id, 'project_subtitle', true );
	if ( $custom !== '' ) { return wp_strip_all_tags( $custom ); }
	$excerpt = get_the_excerpt( $post_id );
	if ( $excerpt !== '' ) { return wp_strip_all_tags( $excerpt ); }
	$content = get_post_field( 'post_content', $post_id );
	return wp_trim_words( wp_strip_all_tags( strip_shortcodes( (string) $content ) ), 28 );
}

function nlpo_project_query( $limit = 12 ) {
	return new WP_Query( array(
		'post_type'      => 'nadlan_project',
		'post_status'    => 'publish',
		'posts_per_page' => max( 1, min( 60, (int) $limit ) ),
		'orderby'        => array( 'menu_order' => 'ASC', 'date' => 'DESC' ),
		'no_found_rows'  => true,
		'meta_query'     => array(
			'relation' => 'OR',
			array( 'key' => 'project_featured', 'compare' => 'EXISTS' ),
			array( 'key' => 'project_featured', 'compare' => 'NOT EXISTS' ),
		),
	) );
}
