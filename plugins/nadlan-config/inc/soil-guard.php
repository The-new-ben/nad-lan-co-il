<?php
/**
 * Soil guard (Ben 15.10.2026, an order with a commitment): NOTHING about the soil tests (PFAS, contamination) appears on any
 * project page, in any language. The subject lives on one page only, /sde-dov/contamination/, without project or company
 * names. This guard is the system, not a note: on every project page it drops, before display, any heading, paragraph, list
 * item or table row that mentions the subject, so content brought back by an import, an old package or an agent never
 * reaches the screen. It fails open: if anything goes wrong, the content is returned as it was.
 * Loaded from inc/instruments.php (a module the live plugin already loads).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_soil_guard_pattern' ) ) {
	function nadlan_soil_guard_pattern() {
		return '/PFAS|PFOS|PFOA|contaminat|pollut|загрязн|تلوث|ملوث|dépollu|זיהום|מזוהמ/iu';
	}

	/** Drops every block that mentions the subject; returns the input unchanged on any failure. */
	function nadlan_soil_guard_clean( $html ) {
		if ( ! is_string( $html ) || '' === $html || ! preg_match( nadlan_soil_guard_pattern(), $html ) ) { return $html; }
		$out = preg_replace_callback( '/<(h[2-6]|p|li|tr|dt|dd|figcaption)\b[^>]*>.*?<\/\1>/su', function ( $m ) {
			return preg_match( nadlan_soil_guard_pattern(), $m[0] ) ? '' : $m[0];
		}, $html );
		return ( is_string( $out ) && '' !== trim( $out ) ) ? $out : $html;
	}

	add_filter( 'the_content', function ( $html ) {
		return is_singular( 'nadlan_project' ) ? nadlan_soil_guard_clean( $html ) : $html;
	}, 99 );
}
