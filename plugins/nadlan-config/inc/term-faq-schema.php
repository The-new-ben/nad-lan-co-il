<?php
/**
 * nadlan-config - Auto FAQ schema + breadcrumbs on glossary terms (v1.40.0 / shark #15)
 *
 * Each term page has 3 H2 sections (הגדרה / מה זה אומר בפועל / טעות נפוצה).
 * Emit FAQPage JSON-LD so Google can show the term as a rich result with the
 * Q&A expanders directly in SERP - massive CTR uplift, free.
 *
 * Also emits BreadcrumbList schema (home → glossary → term).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'wp_head', function () {
	if ( ! is_singular( 'nadlan_term' ) ) { return; }
	$post = get_queried_object();
	if ( ! $post ) { return; }
	$html = (string) $post->post_content;
	$faqs = array();
	// 1.72.520: a term with a real "שאלות נפוצות" section gives its own visible questions (h3 + p), never questions made of headings
	if ( preg_match( '~<h2[^>]*>[^<]*שאלות נפוצות[^<]*</h2>(.*?)(?=<h2|$)~us', $html, $fq ) && preg_match_all( '~<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>~us', $fq[1], $qa, PREG_SET_ORDER ) && count( $qa ) >= 2 ) {
		foreach ( $qa as $x ) {
			$faqs[] = array( '@type' => 'Question', 'name' => trim( wp_strip_all_tags( $x[1] ) ), 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => trim( wp_strip_all_tags( $x[2] ) ) ) );
		}
		$m = array();
	} elseif ( ! preg_match_all( '~<h2[^>]*>(.*?)</h2>(.*?)(?=<h2|$)~us', $html, $m, PREG_SET_ORDER ) ) {
		$m = array(); // no sections: the breadcrumb below still prints
	}
	foreach ( $m as $sec ) {
		$q = trim( wp_strip_all_tags( $sec[1] ) );
		$a = trim( wp_strip_all_tags( $sec[2] ) );
		if ( mb_strlen( $a ) < 30 ) { continue; }
		// truncate answer to ~600 chars (FAQ schema spec)
		$a = mb_substr( $a, 0, 600 );
		$faqs[] = array(
			'@type' => 'Question',
			'name'  => $q . ' של ' . get_the_title( $post ) . '?',
			'acceptedAnswer' => array(
				'@type' => 'Answer',
				'text'  => $a,
			),
		);
	}
	if ( count( $faqs ) >= 2 ) {
		echo "\n<script type=\"application/ld+json\">" . wp_json_encode( array(
			'@context' => 'https://schema.org',
			'@type'    => 'FAQPage',
			'mainEntity' => $faqs,
		), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	}
	// BreadcrumbList
	echo "\n<script type=\"application/ld+json\">" . wp_json_encode( array(
		'@context' => 'https://schema.org',
		'@type'    => 'BreadcrumbList',
		'itemListElement' => array(
			array( '@type' => 'ListItem', 'position' => 1, 'name' => 'בית', 'item' => home_url( '/' ) ),
			array( '@type' => 'ListItem', 'position' => 2, 'name' => 'מילון', 'item' => home_url( '/glossary/' ) ),
			array( '@type' => 'ListItem', 'position' => 3, 'name' => get_the_title( $post ), 'item' => get_permalink( $post ) ),
		),
	), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
}, 22 );

/* 1.72.520: the Yoast title and description of a glossary term can be set through the REST API (like pages), so an upgraded term
   gets its searched title; editors only. */
add_action( 'init', function () {
	foreach ( array( '_yoast_wpseo_title', '_yoast_wpseo_metadesc' ) as $k ) {
		register_post_meta( 'nadlan_term', $k, array( 'type' => 'string', 'single' => true, 'show_in_rest' => true,
			'auth_callback' => function () { return current_user_can( 'edit_posts' ); } ) );
	}
}, 20 );
