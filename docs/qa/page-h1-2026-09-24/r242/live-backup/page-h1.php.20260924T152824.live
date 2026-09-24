<?php
/**
 * One visible H1 on every regular page (24.9.2026). The full-site crawl found 217 pages with no H1 at all: the
 * theme's page template prints no title, and the guides, calculators, city guides and legal pages were written
 * with their title as an H2 or with no title. Some of them are 2,000 to 4,700 word guides that rank for money
 * searches, and the reader lands on a paragraph with no name.
 *
 * Rules, in order (only when the page content has no <h1 of its own):
 *  1. A hero that already shows a title (a <section class="hero ..."> with an <h2>): that heading becomes the H1.
 *     The page's own CSS for h2 is copied for h1, so it looks exactly as before.
 *  2. The content opens with an <h2> before any paragraph: the same promotion.
 *  3. A guide wrapper (<div class="nadlan-guide"><div class="wrap">): the page title as an H1 at the top of it,
 *     in the design system's PageHeader style.
 *  4. Anything else: the page title as an H1 above the content.
 * Off switch: option nadlan_page_h1 = '0'.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_page_h1_title' ) ) {
	function nadlan_page_h1_title( $id ) {
		$t = trim( html_entity_decode( wp_strip_all_tags( get_the_title( $id ) ), ENT_QUOTES, 'UTF-8' ) );
		// a title that carries the site name ("... | נדלן") shows without it
		return trim( preg_replace( '/\s*[|\-]\s*(נדלן|NadLan)\s*$/u', '', $t ) );
	}
}

if ( ! function_exists( 'nadlan_page_h1_promote' ) ) {
	/** Turns the h2 that starts at $pos into an h1 and teaches the page's own <style> blocks the same rules for h1. */
	function nadlan_page_h1_promote( $content, $pos ) {
		$end = strpos( $content, '</h2>', $pos );
		if ( false === $end ) { return null; }
		$open = substr( $content, $pos, 3 );
		if ( '<h2' !== $open ) { return null; }
		$heading = '<h1' . substr( $content, $pos + 3, $end - $pos - 3 ) . '</h1>';
		$heading = preg_replace( '/^<h1\b([^>]*)\bclass="([^"]*)"/', '<h1$1class="$2 nl-h1-from-h2"', $heading, 1, $n );
		if ( ! $n ) { $heading = preg_replace( '/^<h1\b/', '<h1 class="nl-h1-from-h2"', $heading, 1 ); }
		$content = substr( $content, 0, $pos ) . $heading . substr( $content, $end + 5 );
		// every rule in the page's own CSS that styles an h2 now styles the promoted h1 too
		$content = preg_replace_callback( '#<style\b[^>]*>(.*?)</style>#s', function ( $m ) {
			$extra = '';
			if ( preg_match_all( '/([^{}]+)\{([^{}]*)\}/', $m[1], $rules, PREG_SET_ORDER ) ) {
				foreach ( $rules as $r ) {
					$sel = trim( $r[1] );
					if ( '' === $sel || '@' === $sel[0] || ! preg_match( '/(^|[\s>+~,(])h2(?![\w-])/', $sel ) ) { continue; }
					$parts = array();
					foreach ( explode( ',', $sel ) as $s ) {
						if ( preg_match( '/(^|[\s>+~(])h2(?![\w-])/', $s ) ) { $parts[] = preg_replace( '/(^|[\s>+~(])h2(?![\w-])/', '$1h1.nl-h1-from-h2', trim( $s ) ); }
					}
					if ( $parts ) { $extra .= implode( ',', $parts ) . '{' . $r[2] . '}'; }
				}
			}
			return '' === $extra ? $m[0] : str_replace( '</style>', $extra . '</style>', $m[0] );
		}, $content );
		return $content;
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( '0' === (string) get_option( 'nadlan_page_h1', '1' ) ) { return $content; }
	if ( ! is_page() || is_front_page() || ! in_the_loop() || ! is_main_query() ) { return $content; }
	if ( false !== stripos( $content, '<h1' ) ) { return $content; }
	$id    = get_the_ID();
	$title = nadlan_page_h1_title( $id );
	if ( '' === $title ) { return $content; }

	// 1. a hero that shows a title
	if ( preg_match( '/<section\b[^>]*class="[^"]*\bhero\b[^"]*"[^>]*>/i', $content, $hm, PREG_OFFSET_CAPTURE ) ) {
		$hero_end = stripos( $content, '</section>', $hm[0][1] );
		$h2       = stripos( $content, '<h2', $hm[0][1] );
		if ( false !== $h2 && ( false === $hero_end || $h2 < $hero_end ) ) {
			$out = nadlan_page_h1_promote( $content, $h2 );
			if ( null !== $out ) { return $out; }
		}
	}
	// 2. the content opens with an h2, before any real paragraph, and that h2 is the page's title in other words
	// (an opening section called "פתיחה" is not a title: the page title goes on top instead)
	$h2 = stripos( $content, '<h2' );
	if ( false !== $h2 ) {
		$before = wp_strip_all_tags( preg_replace( '#<style\b.*?</style>#s', '', substr( $content, 0, $h2 ) ) );
		$h2end  = stripos( $content, '</h2>', $h2 );
		$words  = function ( $s ) {
			$stop = array( 'של', 'על', 'את', 'עם', 'או', 'גם', 'מה', 'איך', 'לפני', 'כל', 'לא', 'זה', 'הוא', 'היא', 'the', 'and', 'of' );
			$w    = preg_split( '/[^\p{L}\p{N}]+/u', mb_strtolower( (string) $s ), -1, PREG_SPLIT_NO_EMPTY );
			return array_values( array_diff( array_filter( $w, function ( $x ) { return mb_strlen( $x ) > 1; } ), $stop ) );
		};
		$tw    = $words( $title );
		$hw    = false !== $h2end ? $words( wp_strip_all_tags( substr( $content, $h2, $h2end - $h2 ) ) ) : array();
		$share = $tw ? count( array_intersect( $tw, $hw ) ) / count( $tw ) : 0;
		// a short heading ("נכסים נבחרים") is a section, not the title of a longer page name
		if ( mb_strlen( trim( $before ) ) < 40 && $share >= 0.4 && ! ( count( $hw ) <= 3 && count( $tw ) > count( $hw ) ) ) {
			$out = nadlan_page_h1_promote( $content, $h2 );
			if ( null !== $out ) { return $out; }
		}
	}
	$header = '<header class="nlds-pagehead nlds-pagehead--inpage"><h1 class="nlds-pagehead__title">' . esc_html( $title ) . '</h1></header>';
	// 3. inside the guide wrapper
	if ( preg_match( '/<div\b[^>]*class="[^"]*\bnadlan-guide\b[^"]*"[^>]*>\s*<div\b[^>]*class="[^"]*\bwrap\b[^"]*"[^>]*>/i', $content, $gm, PREG_OFFSET_CAPTURE ) ) {
		$at = $gm[0][1] + strlen( $gm[0][0] );
		return substr( $content, 0, $at ) . $header . substr( $content, $at );
	}
	// 4. above the content
	return $header . $content;
}, 1000 );

add_action( 'wp_head', function () {
	if ( '0' === (string) get_option( 'nadlan_page_h1', '1' ) || ! is_page() || is_front_page() ) { return; }
	// the PageHeader title of the NadLan design system (Claude Design), on the Skin A tokens the site already loads
	echo "\n<style id=\"nadlan-page-h1\">.nlds-pagehead--inpage{padding-block:4px 6px;direction:rtl}.nlds-pagehead--inpage .nlds-pagehead__title{font-family:var(--sa-serif,'Noto Serif Hebrew','David Libre',Georgia,serif);font-weight:600;font-size:clamp(30px,3.4vw,46px);line-height:1.1;letter-spacing:-.005em;color:var(--sa-ink,#14212B);margin:0 0 14px;text-wrap:balance}@media(max-width:600px){.nlds-pagehead--inpage .nlds-pagehead__title{font-size:30px}}</style>\n";
}, 30 );
