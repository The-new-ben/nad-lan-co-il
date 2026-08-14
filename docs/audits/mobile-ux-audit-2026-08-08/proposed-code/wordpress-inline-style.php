<?php
/**
 * NadLan selected-unit CSS enqueue example.
 *
 * PROPOSAL ONLY / NOT APPLIED.
 * DO NOT drop this file into WordPress or include it on production as-is.
 *
 * Intended future location of the integration call:
 * plugins/nadlan-config/inc/showroom-engine.php, inside the showroom shortcode,
 * immediately after `nadlan-engine-css` has been enqueued.
 */

defined( 'ABSPATH' ) || exit;

/**
 * Attach the selected-unit surface rules to the existing engine stylesheet.
 *
 * This keeps `nadlan-engine-css` as the single CSS owner and ensures the inline
 * block appears after showroom.css. The file is read server-side; it is not a
 * second browser request and it is not enqueued under a competing handle.
 *
 * @return bool True when the CSS was attached successfully.
 */
function nadlan_proposal_add_selected_unit_inline_style() {
	$css_path = dirname( __DIR__ ) . '/assets/showroom-engine/unit-surface.css';

	if ( ! is_readable( $css_path ) ) {
		return false;
	}

	$css = file_get_contents( $css_path ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents

	if ( false === $css || '' === trim( $css ) ) {
		return false;
	}

	return wp_add_inline_style( 'nadlan-engine-css', $css );
}

/*
 * PROPOSED CALL SITE — do not execute from this proposal file:
 *
 * wp_enqueue_style(
 *     'nadlan-engine-css',
 *     $base . 'showroom.css',
 *     array( 'nadlan-engine-tokens' ),
 *     NADLAN_CONFIG_VERSION
 * );
 *
 * nadlan_proposal_add_selected_unit_inline_style();
 *
 * Deployment rule:
 * - engine.js, unit-surface.css, i18n.js and this PHP call must ship in one
 *   versioned artifact.
 * - Do not place the call on `wp_footer`, in premium-ui.php, or in another
 *   late emergency-CSS layer.
 * - In the production implementation, rename the proposal-prefixed helper
 *   only after sandbox acceptance.
 */
