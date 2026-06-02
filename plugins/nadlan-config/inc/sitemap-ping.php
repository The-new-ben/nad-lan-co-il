<?php
/**
 * nadlan-config — Sitemap ping on content change (v1.40.0 / shark #13)
 *
 * When meaningful content changes (a glossary term is enriched, a new
 * professional is verified, a new project is enriched), ping the Yoast sitemap
 * and warm the Google index. Free SEO speed-up — pages get crawled days faster
 * than they would by default.
 *
 * Throttle: max 1 ping per hour total (Google rate-limits anyway).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_sitemap_ping' ) ) {
	function nadlan_sitemap_ping( $reason = '' ) {
		if ( get_transient( 'nadlan_sitemap_ping_throttle' ) ) { return; }
		set_transient( 'nadlan_sitemap_ping_throttle', 1, HOUR_IN_SECONDS );
		$sitemap = home_url( '/sitemap_index.xml' );
		$urls = array(
			'https://www.google.com/ping?sitemap=' . rawurlencode( $sitemap ),
			'https://www.bing.com/ping?sitemap=' . rawurlencode( $sitemap ),
		);
		foreach ( $urls as $u ) {
			wp_remote_get( $u, array( 'timeout' => 6, 'blocking' => false ) );
		}
		update_option( 'nadlan_sitemap_last_ping', array( 't' => time(), 'reason' => $reason ) );
	}
}

add_action( 'save_post_nadlan_term', function ( $id ) {
	if ( wp_is_post_revision( $id ) || wp_is_post_autosave( $id ) ) { return; }
	if ( get_post_status( $id ) !== 'publish' ) { return; }
	nadlan_sitemap_ping( 'term_save_' . $id );
} );
add_action( 'save_post_nadlan_professional', function ( $id ) {
	if ( wp_is_post_revision( $id ) || wp_is_post_autosave( $id ) ) { return; }
	if ( get_post_meta( $id, 'data_quality', true ) !== 'enriched' ) { return; }
	nadlan_sitemap_ping( 'pro_enriched_' . $id );
} );
add_action( 'save_post_nadlan_project', function ( $id ) {
	if ( wp_is_post_revision( $id ) || wp_is_post_autosave( $id ) ) { return; }
	if ( get_post_meta( $id, 'data_quality', true ) !== 'enriched' ) { return; }
	nadlan_sitemap_ping( 'proj_enriched_' . $id );
} );
add_action( 'transition_post_status', function ( $new, $old, $post ) {
	if ( $new !== 'publish' || $old === 'publish' ) { return; }
	if ( ! in_array( $post->post_type, array( 'page', 'post' ), true ) ) { return; }
	nadlan_sitemap_ping( 'new_' . $post->post_type . '_' . $post->ID );
}, 10, 3 );
