<?php
/**
 * Structured-data printer from post meta.
 *
 * WHY: JSON-LD embedded inside post_content gets mangled by content filters.
 * Found live 2026-08-04 on /michraz-dirot/: a Hebrew FAQ answer containing
 * gershayim (the " in רמ"י) came out of the filter chain with a corrupted
 * escape and the whole FAQPage block failed JSON.parse, so Google saw
 * nothing. Content is for humans; schema lives in meta and prints in
 * wp_head, past no filter.
 *
 * Contract: post meta `_nl_faq_schema` holds the COMPLETE JSON-LD object as
 * a string (validated at build time by the seeding pipeline). This module
 * prints it verbatim inside a script tag. It never builds or edits the
 * JSON; broken meta means a build-stage bug, not a render-stage patch.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'wp_head', function () {
	if ( ! is_singular() ) {
		return;
	}
	$json = (string) get_post_meta( get_queried_object_id(), '_nl_faq_schema', true );
	if ( '' === $json ) {
		return;
	}
	/* stored JSON is machine-written by the seed pipeline; a paranoia decode
	   keeps a hand-corrupted value from ever reaching the page */
	if ( null === json_decode( $json ) ) {
		return;
	}
	echo "\n" . '<script type="application/ld+json">' . $json . '</script>' . "\n"; // phpcs:ignore WordPress.Security.EscapeOutput
}, 6 );
