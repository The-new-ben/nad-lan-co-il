<?php
/**
 * HAD-256 bench only (NEVER on a real site): the three places where the live site's Yoast SEO prints a page's description,
 * so the bench HTML carries what the live HTML carries (main's live run 6.10: the old promise survived there, in Yoast's
 * head output, which the bench did not have).
 *   <meta name="description" content="...">            the stored _yoast_wpseo_metadesc, through 'wpseo_metadesc'
 *   <meta property="og:description" content="...">      the same, through 'wpseo_opengraph_desc'
 *   <script type="application/ld+json" class="yoast-schema-graph">  a WebPage piece whose "description" is the stored
 *                                                       text, through 'wpseo_schema_webpage' (Yoast's own filter names)
 * The live text is seeded once on /post-listing/ from wp-content/nlj-yoast-desc.txt (docs/qa/had-256/page-4958/
 * yoast-desc-old.txt = what deploydrop.py --post-listing wrote and the live page prints). Off when the real Yoast runs.
 */
if ( ! defined( 'ABSPATH' ) ) { return; }
$nlj_v = (string) @file_get_contents( WP_CONTENT_DIR . '/nlj-variant.txt' );
if ( strpos( $nlj_v, 'theme' ) !== 0 && strpos( $nlj_v, 'rehearsal' ) !== 0 ) { return; }
unset( $nlj_v );

add_action( 'init', function () {
	if ( defined( 'WPSEO_VERSION' ) || get_option( 'nlj_yoast_seeded' ) ) { return; }
	$pl = get_page_by_path( 'post-listing' );
	$d  = (string) @file_get_contents( WP_CONTENT_DIR . '/nlj-yoast-desc.txt' );
	if ( ! $pl || '' === $d ) { return; }
	update_post_meta( $pl->ID, '_yoast_wpseo_metadesc', wp_slash( $d ) );
	update_option( 'nlj_yoast_seeded', 1, false );
}, 80 );

add_action( 'wp_head', function () {
	if ( defined( 'WPSEO_VERSION' ) || ! is_singular() ) { return; }
	$id   = (int) get_queried_object_id();
	$desc = (string) get_post_meta( $id, '_yoast_wpseo_metadesc', true );
	if ( '' === $desc ) { return; }
	$meta = (string) apply_filters( 'wpseo_metadesc', $desc );
	$og   = (string) apply_filters( 'wpseo_opengraph_desc', $desc );
	$page = apply_filters( 'wpseo_schema_webpage', array( '@type' => 'WebPage', '@id' => get_permalink( $id ), 'url' => get_permalink( $id ), 'name' => get_the_title( $id ), 'inLanguage' => 'he-IL', 'description' => $desc ) );
	echo "\t<!-- HAD-256 bench: a stand-in for Yoast SEO's head output -->\n";
	echo "\t" . '<meta name="description" content="' . esc_attr( $meta ) . '" />' . "\n";
	echo "\t" . '<meta property="og:description" content="' . esc_attr( $og ) . '" />' . "\n";
	echo "\t" . '<script type="application/ld+json" class="yoast-schema-graph">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => array( $page ) ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
}, 1 );
