<?php
/**
 * nadlan-config - Guide schema + hreflang for cornerstone SEO guides.
 *
 * Flagship guide articles (e.g. the "elevated apartment living" guide) are
 * ordinary WordPress posts, but they need three things Yoast does not add on
 * its own for a hand-authored bilingual guide:
 *   1. FAQPage JSON-LD (AEO / Google "People also ask" + AI answer surfaces),
 *      printed in wp_head so content filters cannot mangle an inline <script>.
 *   2. Reciprocal hreflang between the HE and EN siblings (no Polylang/WPML on
 *      this site), so Google serves the right language and never treats the two
 *      as duplicate content.
 *   3. A crawlable, visible language switch is the theme's job; here we only
 *      emit the machine signals.
 *
 * Data lives in post meta so this is reusable for every future guide:
 *   guide_faq_json   JSON array of {q, a}
 *   guide_hreflang   JSON object { he: url, en: url, x-default: url }
 *   guide_cornerstone "1" marks it (also used to widen the internal-link net)
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_guide_register_meta' ) ) {
	function nadlan_guide_register_meta() {
		foreach ( array( 'guide_faq_json', 'guide_hreflang', 'guide_cornerstone', 'guide_reading_minutes' ) as $key ) {
			register_post_meta( 'post', $key, array(
				'show_in_rest'  => true,
				'single'        => true,
				'type'          => 'string',
				'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
			) );
		}
	}
}
add_action( 'init', 'nadlan_guide_register_meta' );

if ( ! function_exists( 'nadlan_guide_json_meta' ) ) {
	function nadlan_guide_json_meta( $post_id, $key ) {
		$raw = trim( (string) get_post_meta( (int) $post_id, $key, true ) );
		if ( $raw === '' ) { return null; }
		$d = json_decode( $raw, true );
		return is_array( $d ) ? $d : null;
	}
}

/* FAQPage JSON-LD (printed only when the guide carries a FAQ). */
add_action( 'wp_head', function () {
	if ( ! is_singular( 'post' ) ) { return; }
	$id  = get_queried_object_id();
	$faq = nadlan_guide_json_meta( $id, 'guide_faq_json' );
	if ( ! $faq ) { return; }
	$items = array();
	foreach ( $faq as $qa ) {
		$q = isset( $qa['q'] ) ? wp_strip_all_tags( (string) $qa['q'] ) : '';
		$a = isset( $qa['a'] ) ? wp_strip_all_tags( (string) $qa['a'] ) : '';
		if ( $q === '' || $a === '' ) { continue; }
		$items[] = array(
			'@type'          => 'Question',
			'name'           => $q,
			'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $a ),
		);
	}
	if ( ! $items ) { return; }
	$graph = array(
		'@context'   => 'https://schema.org',
		'@type'      => 'FAQPage',
		'mainEntity' => $items,
	);
	echo "\n" . '<script type="application/ld+json">' . wp_json_encode( $graph, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
}, 31 );

/* Reciprocal hreflang for the bilingual guide siblings. */
add_action( 'wp_head', function () {
	if ( ! is_singular( 'post' ) ) { return; }
	$id  = get_queried_object_id();
	$alt = nadlan_guide_json_meta( $id, 'guide_hreflang' );
	if ( ! $alt ) { return; }
	$out = '';
	foreach ( $alt as $lang => $url ) {
		$lang = sanitize_text_field( (string) $lang );
		$url  = esc_url( (string) $url );
		if ( $url === '' ) { continue; }
		$out .= '<link rel="alternate" hreflang="' . esc_attr( $lang ) . '" href="' . $url . '" />' . "\n";
	}
	if ( $out !== '' ) { echo "\n" . $out; }
}, 5 );

/* Set html lang/dir correctly on an English guide (the site default is he-IL). */
add_filter( 'language_attributes', function ( $output ) {
	if ( ! is_singular( 'post' ) ) { return $output; }
	$alt = nadlan_guide_json_meta( get_queried_object_id(), 'guide_hreflang' );
	if ( ! $alt || empty( $alt['en'] ) ) { return $output; }
	$self = get_permalink( get_queried_object_id() );
	if ( isset( $alt['en'] ) && trailingslashit( $self ) === trailingslashit( $alt['en'] ) ) {
		return 'lang="en-US"';
	}
	return $output;
}, 20 );
