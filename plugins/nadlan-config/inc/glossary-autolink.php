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

/* ---- discoverability: add glossary + professionals + projects to the primary nav ---- */
add_filter( 'wp_nav_menu_items', function ( $items, $args ) {
	$primary = isset( $args->theme_location ) && in_array( $args->theme_location, array( 'primary', 'menu-1', 'main', 'header', 'top' ), true );
	if ( ! $primary ) { return $items; }
	$extras = '';
	if ( strpos( (string) $items, '/professionals/' ) === false ) {
		$extras .= '<li class="menu-item nadlan-nav-extra"><a href="' . esc_url( home_url( '/professionals/' ) ) . '">בעלי מקצוע</a></li>';
	}
	if ( strpos( (string) $items, '/glossary/' ) === false ) {
		$extras .= '<li class="menu-item nadlan-nav-extra"><a href="' . esc_url( home_url( '/glossary/' ) ) . '">מילון נדל"ן</a></li>';
	}
	return $items . $extras;
}, 10, 2 );

/* footer fallback links — owner-approved location for all directory entry points
 * (2026-06-01: "Only add to the footer, links to whatever"). Reachable on every page. */
add_action( 'wp_footer', function () {
	if ( is_admin() || is_front_page() ) { return; } // front page: mega footer owns this (v2)
	$pro   = (int) wp_count_posts( 'nadlan_professional' )->publish;
	$proj  = (int) wp_count_posts( 'nadlan_project' )->publish;
	$terms = (int) wp_count_posts( 'nadlan_term' )->publish;
	$links = array(
		array( home_url( '/professionals/' ), 'מאגר בעלי המקצוע',          $pro   ? number_format( $pro )   : '' ),
		array( home_url( '/projects/' ), 'פרויקטים והתחדשות עירונית', $proj  ? number_format( $proj )  : '' ),
		array( home_url( '/glossary/' ),      'מילון מונחי נדל״ן',           $terms ? number_format( $terms ) : '' ),
		array( home_url( '/catalog/' ),       'קטלוג ראשי',                  '' ),
	);
	$html = '<div class="nadlan-nav-foot" style="text-align:center;padding:20px 14px;margin:24px 0 0;background:#FBF9F5;border-top:1px solid rgba(27,26,23,.08);font-family:var(--font-sans,Heebo,sans-serif);font-size:13.5px;display:flex;justify-content:center;gap:28px;flex-wrap:wrap;direction:rtl">';
	foreach ( $links as $L ) {
		$html .= '<a href="' . esc_url( $L[0] ) . '" style="color:#9C7A3C;text-decoration:none;font-weight:600">'
			   . esc_html( $L[1] )
			   . ( $L[2] ? ' <span style="color:#999;font-weight:400">(' . esc_html( $L[2] ) . ')</span>' : '' )
			   . ' ←</a>';
	}
	$html .= '</div>';
	echo $html;
}, 99 );

/* ---- v1.25.0: homepage discoverability block ----
 * Owner confirmed (2026-06-01) to KEEP this block exactly as it is currently live.
 * Injects a "מה תמצאו כאן" pillar-card block on the homepage linking to the
 * professional directory, glossary, urban-renewal hub and legal guide. */
/* Front-page pillar block removed 2026-07-02 (module audit): stacked below the
   v2 homepage. Areas/tools/professionals bands now carry these links. */

/* NOTE: inc/homepage.php provides [nadlan_home_sections] / [nadlan_hero_search]
 * shortcodes only (auto-injection disabled) — available if the owner wants them. */
