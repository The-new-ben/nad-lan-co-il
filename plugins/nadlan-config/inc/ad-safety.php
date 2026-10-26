<?php
/**
 * nadlan-config - Advertising safety rules (local patch 26.10.2026, not live).
 *
 * Before the site sells exposure to more advertisers, every paid surface follows four rules (Google:
 * developers.google.com/search/docs/crawling-indexing/qualify-outbound-links and the link-spam and site
 * reputation policies; research: docs/research/2026-10-26-advertisers/adams-research.md, section 6):
 *  1) every outbound link that a paying advertiser gets is rel="sponsored noopener" (nadlan_ad_rel);
 *  2) every paid card or profile carries a visible "פרסומת" / "ממומן" label, and a paid profile says so;
 *  3) paid text lives on the advertiser's own profile or mini-site, never as a guide page: guides that give
 *     neutral advice can be marked ad-free (post meta nadlan_ad_free = 1, or a path in the option
 *     nadlan_ad_free_paths) and then no paid card renders on them;
 *  4) a cap on paid cards per page (option nadlan_ad_paid_cap, default 3), counted across the inline
 *     professional cards, the end-of-article experts row and placements.
 * Paid wrappers carry data-paid="1" so tools/seo/paid_link_check.py can audit the raw HTML.
 * Unpaid business links keep their current rel unless the filter nadlan_ad_rel_unpaid says otherwise.
 * Indexing is untouched: no noindex, no robots change, no redirect.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ad_is_paid' ) ) {
	/** A card is paid while its tier is pro/premier or a content sponsorship is running. */
	function nadlan_ad_is_paid( $post_id ) {
		$post_id = (int) $post_id;
		if ( $post_id <= 0 ) { return false; }
		$tier = (string) get_post_meta( $post_id, 'paid_tier', true );
		if ( in_array( $tier, array( 'pro', 'premier' ), true ) ) { return true; }
		return (int) get_post_meta( $post_id, 'procard_sponsor_until', true ) >= time();
	}
}

if ( ! function_exists( 'nadlan_ad_rel' ) ) {
	/** The rel for an outbound link printed for this card: sponsored when paid. */
	function nadlan_ad_rel( $post_id ) {
		if ( nadlan_ad_is_paid( $post_id ) ) { return 'sponsored noopener'; }
		return (string) apply_filters( 'nadlan_ad_rel_unpaid', 'noopener', (int) $post_id );
	}
}

if ( ! function_exists( 'nadlan_ad_free_page' ) ) {
	/** True on pages that give neutral advice and must stay free of paid cards. */
	function nadlan_ad_free_page( $post_id = 0 ) {
		$post_id = $post_id ? (int) $post_id : (int) get_queried_object_id();
		if ( $post_id && '1' === (string) get_post_meta( $post_id, 'nadlan_ad_free', true ) ) { return true; }
		$here  = '/' . trim( rawurldecode( (string) wp_parse_url( (string) ( $_SERVER['REQUEST_URI'] ?? '' ), PHP_URL_PATH ) ), '/' ) . '/';
		$paths = preg_split( '/\R/', (string) get_option( 'nadlan_ad_free_paths', '' ) );
		foreach ( (array) $paths as $p ) {
			$p = trim( (string) $p );
			if ( '' !== $p && '/' . trim( $p, '/' ) . '/' === $here ) { return true; }
		}
		return false;
	}
}

if ( ! function_exists( 'nadlan_ad_slot_take' ) ) {
	/** Takes one paid slot on this request; false once the page reached the cap. */
	function nadlan_ad_slot_take() {
		static $used = 0;
		$cap = max( 0, (int) get_option( 'nadlan_ad_paid_cap', 3 ) );
		if ( $used >= $cap ) { return false; }
		$used++;
		return true;
	}
}

/* rule 2 on the profile itself: a paying advertiser's own page says it is a paid profile */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_professional' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$id = get_the_ID();
	if ( ! nadlan_ad_is_paid( $id ) ) { return $content; }
	$label = '<p class="nlad-label" data-paid="1" dir="rtl">פרופיל ממומן · הפרטים והתוכן נמסרו על ידי העסק ובאחריותו</p>'
		. '<style>.nlad-label{display:inline-block;margin:0 0 12px;padding:4px 9px;border:1px solid #12202A;border-radius:2px;font:600 12px/1.4 "IBM Plex Sans Hebrew",Heebo,sans-serif;color:#12202A;background:#fff}</style>';
	return $label . $content;
}, 31 );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['ad_safety'] = array(
		'paid_rel'  => 'sponsored noopener',
		'paid_cap'  => (int) get_option( 'nadlan_ad_paid_cap', 3 ),
		'ad_free_paths' => count( array_filter( preg_split( '/\R/', (string) get_option( 'nadlan_ad_free_paths', '' ) ) ) ),
	);
	return $out;
} );
