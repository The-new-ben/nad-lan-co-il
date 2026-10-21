<?php
/**
 * The legal pages in the footer (owner, 24.9.2026: "תנאי שימוש, privacy policy... תבנה משהו בסיסי מעצמך ותעשה אותו
 * ניתן לעריכה").
 *
 * The pages themselves are ordinary WordPress pages, /terms/ and /privacy/, edited in wp-admin like any other page; their
 * first text is kept in docs/legal/. The privacy page is also WordPress's own privacy-policy page (the broker join form
 * links to it through get_privacy_policy_url()). The footer is a static theme part, so the links are added here, in the
 * part's own markup, with no script: "תנאי שימוש · מדיניות פרטיות · הצהרת נגישות" in the footer's bottom line. A link
 * shows only when its page is published. The accessibility statement had no footer link before.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_filter( 'render_block', function ( $html, $block ) {
	if ( false === strpos( (string) $html, 'class="nlpc-footer-bottom"' ) || false !== strpos( (string) $html, 'class="nlpc-footer-legal"' ) ) { return $html; }
	$links = array( 'terms' => 'תנאי שימוש', 'privacy' => 'מדיניות פרטיות', 'accessibility-statement' => 'הצהרת נגישות' );
	$out   = array();
	foreach ( $links as $slug => $label ) {
		$pg = get_page_by_path( $slug );
		if ( $pg && 'publish' === $pg->post_status ) { $out[] = '<a href="' . esc_url( get_permalink( $pg ) ) . '">' . esc_html( $label ) . '</a>'; }
	}
	if ( ! $out ) { return $html; }
	$span = '<span class="nlpc-footer-legal">' . implode( '<span aria-hidden="true"> · </span>', $out ) . '</span>';
	$new  = preg_replace( '#(<div class="nlpc-footer-bottom">\s*<span>[^<]*</span>)#u', '$1' . $span, (string) $html, 1 );
	return null === $new ? $html : $new;
}, 10, 2 );

/* The tools in the footer (Ben 21.10.2026: "link the tools from the footer"): a fourth column after the three of the theme part.
   Hebrew pages get the Hebrew calculators; pages under /en/ /fr/ /ru/ /ar/ get the English tools only, so a reader abroad is never
   sent to a Hebrew-only calculator. Plain links, no script; the theme part itself is not edited. */
add_filter( 'render_block', function ( $html, $block ) {
	if ( false === strpos( (string) $html, 'class="nlpc-footer-links"' ) || false !== strpos( (string) $html, 'class="nlpc-footer-tools"' ) ) { return $html; }
	$lang = function_exists( 'nadlan_pglang_lang' ) ? (string) nadlan_pglang_lang() : '';
	if ( in_array( $lang, array( 'en', 'fr', 'ru', 'ar' ), true ) ) {
		$title = 'Tools';
		$links = array( '/israel-mortgage-non-residents/' => 'Israeli mortgage from abroad', '/israel-purchase-tax-foreign-residents/' => 'Purchase tax for foreign residents', '/en/sde-dov/contamination/' => 'Sde Dov soil map' );
	} else {
		$title = 'מחשבונים וכלים';
		$links = array( '/property-value-estimator/' => 'שווי דירה', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/mortgage-calculator/mortgage-repayment-capacity/' => 'כמה משכנתא אפשר לקחת',
			'/arnona/' => 'ארנונה בתל אביב', '/mortgage-calculator/mortgage-interest-rates/' => 'ריבית הפריים', '/cpi-calculator/' => 'הצמדה למדד', '/new-projects/construction-input-index/' => 'מדד תשומות הבנייה' );
	}
	$col = '<div class="nlpc-footer-tools"><strong>' . esc_html( $title ) . '</strong>';
	foreach ( $links as $path => $label ) { $col .= '<a href="' . esc_url( home_url( $path ) ) . '">' . esc_html( $label ) . '</a>'; }
	$col .= '</div>';
	$new = preg_replace( '#</div>(\s*)</nav>#u', '</div>' . $col . '$1</nav>', (string) $html, 1 );
	return null === $new ? $html : $new;
}, 11, 2 );

add_action( 'wp_head', function () {
	echo "\n<style id=\"nadlan-legal-links\">.nlpc-footer-legal a{color:inherit;text-decoration:underline;text-underline-offset:3px}.nlpc-footer-legal a:hover{text-decoration-thickness:2px}"
		. ".nlpc-footer-links{grid-template-columns:repeat(4,minmax(0,1fr))}@media (max-width:760px){.nlpc-footer-links{grid-template-columns:repeat(2,minmax(0,1fr))}}</style>\n";
}, 40 );
