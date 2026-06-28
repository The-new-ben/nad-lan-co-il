<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }

function nlpo_scan_content_gaps( $limit = 60 ) {
	$out = array();
	$q = nlpo_project_query( $limit );
	if ( ! $q->have_posts() ) { return $out; }
	while ( $q->have_posts() ) {
		$q->the_post();
		$post = get_post();
		$base = nlpo_base_project_slug( $post->post_name );
		if ( $post->post_name !== $base ) { continue; }
		$langs = nlpo_project_language_posts( $post );
		$missing = array();
		foreach ( nlpo_languages() as $lang => $suffix ) {
			if ( empty( $langs[ $lang ] ) ) { $missing[] = $lang; }
		}
		$thin = array();
		foreach ( $langs as $lang => $p ) {
			$words = str_word_count( wp_strip_all_tags( strip_shortcodes( (string) $p->post_content ) ) );
			if ( $words < 500 ) { $thin[ $lang ] = $words; }
		}
		$out[] = array(
			'base_slug' => $base,
			'post_id'   => $post->ID,
			'title'     => get_the_title( $post ),
			'missing'   => $missing,
			'thin'      => $thin,
			'langs'     => array_keys( $langs ),
		);
	}
	wp_reset_postdata();
	return $out;
}
