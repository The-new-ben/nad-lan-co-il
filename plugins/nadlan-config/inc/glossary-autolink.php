<?php
/**
 * nadlan-config — Glossary in-text auto-linker + discoverability (v1.22.0)
 *
 * Two jobs that compound the glossary's SEO value with zero per-term work:
 *
 *  1) AUTO-LINK: on any singular post/page/pillar/term, the FIRST occurrence of a
 *     published glossary term's title (whole-word, Hebrew-aware) becomes a link to
 *     /glossary/<slug>/. Builds internal links INTO the glossary from the whole
 *     site, automatically, as new terms are published. Caps at 4 links/page so it
 *     never looks spammy, skips headings/existing links/the term's own page.
 *
 *  2) DISCOVERABILITY: the glossary archive (/glossary/) is live but is not linked
 *     from the site, so visitors (and the owner) can't find it. We append a glossary
 *     link to the primary nav menu and a footer credit, so it's reachable.
 *
 * The term map is cached (transient, 6h) and rebuilt when a term is saved.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_AUTOLINK_MAX = 4;

/* ---- build & cache the term => permalink map ---- */
if ( ! function_exists( 'nadlan_autolink_map' ) ) {
	function nadlan_autolink_map() {
		$cached = get_transient( 'nadlan_autolink_map' );
		if ( is_array( $cached ) ) { return $cached; }
		$terms = get_posts( array(
			'post_type'      => 'nadlan_term',
			'post_status'    => 'publish',
			'posts_per_page' => 500,
			'fields'         => 'ids',
		) );
		$map = array();
		foreach ( $terms as $tid ) {
			$title = trim( get_the_title( $tid ) );
			// Only auto-link meaningful multi-char terms; skip 1-2 char noise.
			if ( mb_strlen( $title ) < 3 ) { continue; }
			$map[ $title ] = array( 'id' => $tid, 'url' => get_permalink( $tid ) );
		}
		// Longest titles first so "חכירה לדורות" wins over "חכירה".
		uksort( $map, function ( $a, $b ) { return mb_strlen( $b ) - mb_strlen( $a ); } );
		set_transient( 'nadlan_autolink_map', $map, 6 * HOUR_IN_SECONDS );
		return $map;
	}
}
add_action( 'save_post_nadlan_term', function () { delete_transient( 'nadlan_autolink_map' ); } );

/* ---- the linker ---- */
if ( ! function_exists( 'nadlan_autolink_content' ) ) {
	function nadlan_autolink_content( $content ) {
		if ( is_admin() || ! is_singular() || ! in_the_loop() || ! is_main_query() ) { return $content; }
		// Don't self-link a glossary term page to other terms aggressively, and never to itself.
		$self_id = get_the_ID();
		$map = nadlan_autolink_map();
		if ( ! $map ) { return $content; }

		$done = 0;
		foreach ( $map as $term => $info ) {
			if ( $done >= NADLAN_AUTOLINK_MAX ) { break; }
			if ( (int) $info['id'] === (int) $self_id ) { continue; }
			$quoted = preg_quote( $term, '/' );
			// Match the term when not already inside a tag/attribute or an existing link.
			// Hebrew has no \b, so we bound on non-letter (or string edge) on both sides.
			$pattern = '/(?<![\p{L}\p{N}])(' . $quoted . ')(?![\p{L}\p{N}])/u';
			$replaced = false;
			$content = nadlan_autolink_replace_first_outside_tags( $content, $pattern, $info['url'], $term, $replaced );
			if ( $replaced ) { $done++; }
		}
		return $content;
	}
}

/* Replace only the first match that is NOT inside an HTML tag, an <a>, or a heading. */
if ( ! function_exists( 'nadlan_autolink_replace_first_outside_tags' ) ) {
	function nadlan_autolink_replace_first_outside_tags( $html, $pattern, $url, $term, &$replaced ) {
		// Split on tags so we only touch text nodes; track open <a>/<h1-6> to skip them.
		$parts = preg_split( '/(<[^>]+>)/', $html, -1, PREG_SPLIT_DELIM_CAPTURE );
		$skip_depth = 0; // inside <a> or heading
		foreach ( $parts as $i => $chunk ) {
			if ( $chunk === '' ) { continue; }
			if ( $chunk[0] === '<' ) {
				if ( preg_match( '/^<\s*(a|h[1-6])\b/i', $chunk ) ) { $skip_depth++; }
				elseif ( preg_match( '/^<\s*\/\s*(a|h[1-6])\s*>/i', $chunk ) && $skip_depth > 0 ) { $skip_depth--; }
				continue; // never edit tag chunks
			}
			if ( $skip_depth > 0 ) { continue; }
			if ( preg_match( $pattern, $chunk ) ) {
				$link = '<a href="' . esc_url( $url ) . '" class="nadlan-gloss-link" title="' . esc_attr( $term ) . ' — מילון נדל"ן">$1</a>';
				$parts[ $i ] = preg_replace( $pattern, $link, $chunk, 1 );
				$replaced = true;
				break;
			}
		}
		return implode( '', $parts );
	}
}
add_filter( 'the_content', 'nadlan_autolink_content', 24 );

/* subtle styling for the auto-links */
add_action( 'wp_head', function () {
	if ( ! is_singular() ) { return; }
	echo '<style>.nadlan-gloss-link{color:inherit;text-decoration:none;border-bottom:1px dotted #9C7A3C;background:linear-gradient(transparent 88%,rgba(156,122,60,.14) 0)}.nadlan-gloss-link:hover{color:#9C7A3C}</style>' . "\n";
}, 60 );

/* ---- discoverability: add the glossary to the primary nav ---- */
add_filter( 'wp_nav_menu_items', function ( $items, $args ) {
	// Add once, to the first/primary menu only, and only if not already present.
	if ( strpos( (string) $items, '/glossary/' ) !== false ) { return $items; }
	$primary = isset( $args->theme_location ) && in_array( $args->theme_location, array( 'primary', 'menu-1', 'main', 'header', 'top' ), true );
	if ( ! $primary ) { return $items; }
	$link = '<li class="menu-item nadlan-gloss-nav"><a href="' . esc_url( home_url( '/glossary/' ) ) . '">מילון נדל"ן</a></li>';
	return $items . $link;
}, 10, 2 );

/* footer fallback link (always reachable even if the theme has no nav menu) */
add_action( 'wp_footer', function () {
	if ( is_admin() ) { return; }
	echo '<div class="nadlan-gloss-foot" style="text-align:center;padding:14px;font-family:var(--font-sans,Heebo,sans-serif);font-size:13px"><a href="' . esc_url( home_url( '/glossary/' ) ) . '" style="color:#9C7A3C;text-decoration:none">מילון מונחי נדל"ן ←</a></div>';
}, 99 );
