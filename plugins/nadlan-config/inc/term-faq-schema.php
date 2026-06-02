<?php
/**
 * nadlan-config — Auto FAQ schema + breadcrumbs on glossary terms (v1.40.0 / shark #15)
 *
 * Each term page has 3 H2 sections (הגדרה / מה זה אומר בפועל / טעות נפוצה).
 * Emit FAQPage JSON-LD so Google can show the term as a rich result with the
 * Q&A expanders directly in SERP — massive CTR uplift, free.
 *
 * Also emits BreadcrumbList schema (home → glossary → term).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'wp_head', function () {
	if ( ! is_singular( 'nadlan_term' ) ) { return; }
	$post = get_queried_object();
	if ( ! $post ) { return; }
	$html = (string) $post->post_content;
	// Extract sections — pattern: <h2>label</h2> ... up to next h2 or end
	if ( ! preg_match_all( '~<h2[^>]*>(.*?)</h2>(.*?)(?=<h2|$)~us', $html, $m, PREG_SET_ORDER ) ) { return; }
	$faqs = array();
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
