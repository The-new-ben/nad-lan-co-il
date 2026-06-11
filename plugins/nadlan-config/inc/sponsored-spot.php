<?php
/**
 * nadlan-config — Sponsored-spot CTA on directory (v1.41.1 — REWRITTEN, ob-free)
 *
 * ⚠️ v1.40.0 BUG FIXED HERE: the old version used ob_start() on template_redirect
 * and called nadlan_ss_card() (which itself used ob_start/ob_get_clean) from
 * inside that output-buffer handler. PHP forbids nested output buffering inside
 * an ob handler → FATAL → blank page. This blanked BOTH /professionals/ and
 * /projects/ (everything rendered by directory.php) from v1.40.0 to v1.41.0.
 *
 * New approach — zero output buffering:
 *   • nadlan_ss_card() builds a plain string (no ob_start).
 *   • Server-side injection via the `nadlan_dir_cards_html` filter that
 *     directory.php applies to its rendered cards (added v1.41.1). We insert a
 *     sponsored card after the 6th real card.
 *   • AJAX load-more injection via rest_post_dispatch (unchanged logic, now uses
 *     the ob-free card).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ss_card' ) ) {
	function nadlan_ss_card( $mode = 'professional' ) {
		$pricing = esc_url( home_url( '/join-pro/' ) );
		$cart    = $mode === 'project' ? esc_url( home_url( '/?add-to-cart=489&ref=ss' ) ) : esc_url( home_url( '/?add-to-cart=476&ref=ss' ) );
		$copy_h  = $mode === 'project' ? 'הציגו את הפרויקט שלכם כאן' : 'הכרטיס שלכם יכול להיות במקום זה';
		$copy_p  = $mode === 'project' ? 'הפרויקט שלכם בקדמת הבמה, מול קונים ומשקיעים פעילים. ₪3,990 לקמפיין.' : 'הצטרפו למאגר אנשי המקצוע המוביל בישראל. תוכנית Pro מ-₪349 לחודש.';
		// Plain string — NO ob_start (safe to call anywhere, incl. filters).
		return '<a class="nldc nldc-sponsored-spot" href="' . $cart . '">'
			. '<span class="nldc-sponsor nldc-sponsor-slot">מקודם · פנוי</span>'
			. '<div class="nldc-sponsored-body">'
			. '<svg class="nldc-sponsored-mark" aria-hidden="true" viewBox="0 0 48 48"><circle cx="24" cy="24" r="22" fill="none" stroke="currentColor" stroke-width="1" opacity=".25"/><circle cx="24" cy="24" r="14" fill="none" stroke="currentColor" stroke-width="1" opacity=".4"/><circle cx="24" cy="24" r="6" fill="currentColor" opacity=".85"/></svg>'
			. '<h3 class="nldc-name nldc-sponsored-h">' . esc_html( $copy_h ) . '</h3>'
			. '<p class="nldc-sponsored-p">' . esc_html( $copy_p ) . '</p>'
			. '<span class="nldc-go">בקשו מידע ←</span>'
			. '<small class="nldc-sponsored-foot">או <a href="' . $pricing . '">השוואה מלאה</a></small>'
			. '</div></a>';
	}
}

/* Insert a sponsored card after the 6th real card in a rendered cards string.
 * Pure string ops — no regex backtracking risk, no output buffering. */
if ( ! function_exists( 'nadlan_ss_inject' ) ) {
	function nadlan_ss_inject( $html, $post_type ) {
		if ( ! is_string( $html ) || strpos( $html, 'class="nldc' ) === false ) { return $html; }
		if ( strpos( $html, 'nldir-empty' ) !== false ) { return $html; }
		$mode = ( $post_type === 'nadlan_project' ) ? 'project' : 'professional';
		// split on the close of each card link; cards end with </a>
		$parts = explode( '</a>', $html );
		// need at least 6 cards to inject after the 6th
		if ( count( $parts ) <= 6 ) { return $html; }
		$out = '';
		foreach ( $parts as $i => $part ) {
			if ( $part === '' ) { continue; }
			$out .= $part . '</a>';
			if ( $i === 5 ) { $out .= nadlan_ss_card( $mode ); } // after the 6th card
		}
		return $out;
	}
}

/* Server-side: hook the directory's cards filter (added in directory.php v1.41.1). */
add_filter( 'nadlan_dir_cards_html', 'nadlan_ss_inject', 10, 2 );

/* AJAX load-more: inject one sponsored card per batch (safe — not inside an ob handler). */
add_filter( 'rest_post_dispatch', function ( $response, $server, $request ) {
	$route = $request->get_route();
	if ( $route !== '/nadlan/v1/directory' && $route !== '/nadlan/v1/projects' ) { return $response; }
	$data = $response->get_data();
	if ( empty( $data['html'] ) || ! is_string( $data['html'] ) ) { return $response; }
	$mode = ( $route === '/nadlan/v1/projects' ) ? 'project' : 'professional';
	// inject after the first card in the batch
	$pos = strpos( $data['html'], '</a>' );
	if ( $pos !== false ) {
		$data['html'] = substr( $data['html'], 0, $pos + 4 ) . nadlan_ss_card( $mode ) . substr( $data['html'], $pos + 4 );
		$response->set_data( $data );
	}
	return $response;
}, 10, 3 );
