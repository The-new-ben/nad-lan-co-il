<?php
/**
 * Language context + hreflang + chrome retranslation for PATH-BASED page
 * variants: /en/<slug>/, /fr/<slug>/, /ru/<slug>/, /ar/<slug>/.
 *
 * WHY (content-agent site audit 2026-08-07, verified live): the language ROOT
 * pages (/en/ /fr/ /ru/) rendered lang="he-IL" dir="rtl", and no page-level
 * variant printed hreflang. inc/project-lang.php covers only nadlan_project
 * slug-suffix variants; pillar PAGES (like /new-projects/) publish their
 * language versions as child pages under the existing en/fr/ru/ar root pages,
 * so the same three repairs are rebuilt here for that shape, additively:
 *  1. lang context + CORRECT lang/dir on <html> (server-side, not JS).
 *  2. bidirectional hreflang cluster per page family (he at root = x-default).
 *  3. footer chrome retranslation, reusing project-lang's string map.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_pglang_lang' ) ) {
	/** Language of the current page from its top-level ancestor slug, '' for none. */
	function nadlan_pglang_lang() {
		if ( ! is_page() ) {
			return '';
		}
		$id   = get_queried_object_id();
		$tree = array_merge( array( $id ), get_post_ancestors( $id ) );
		$top  = (string) get_post_field( 'post_name', end( $tree ) );
		return in_array( $top, array( 'en', 'fr', 'ru', 'ar' ), true ) ? $top : '';
	}
}

add_action( 'wp', function () {
	$lang = nadlan_pglang_lang();
	if ( '' !== $lang && function_exists( 'nadlan_set_lang' ) ) {
		nadlan_set_lang( $lang );
	}
}, 1 );

/* Server-side <html lang dir> repair: the theme hardcodes he-IL/rtl. */
add_filter( 'language_attributes', function ( $output ) {
	$lang = function_exists( 'nadlan_pglang_lang' ) ? nadlan_pglang_lang() : '';
	if ( '' === $lang ) {
		return $output;
	}
	$dir = ( 'ar' === $lang ) ? 'rtl' : 'ltr';
	return 'lang="' . esc_attr( $lang ) . '" dir="' . esc_attr( $dir ) . '"';
}, 20 );

if ( ! function_exists( 'nadlan_pglang_restpath' ) ) {
	/** The page's full path with any leading lang prefix stripped: the family key. */
	function nadlan_pglang_restpath( $post_id ) {
		$uri = trim( (string) get_page_uri( $post_id ), '/' );
		return preg_replace( '#^(en|fr|ru|ar)/#', '', $uri );
	}
}

if ( ! function_exists( 'nadlan_pglang_family' ) ) {
	/**
	 * Existing published variants of the current page family, lang => url.
	 * Family key = the page PATH minus the lang prefix, so nested guides work
	 * too: he lives at /<rest>/, others at /<lang>/<rest>/ (spokes ship at
	 * /guides/<slug>/ vs /en/guides/<slug>/ - a leaf-only key broke there).
	 * The lang root pages themselves are skipped (rest = the lang code).
	 */
	function nadlan_pglang_family( $post_id ) {
		$rest = nadlan_pglang_restpath( $post_id );
		if ( '' === $rest || in_array( $rest, array( 'en', 'fr', 'ru', 'ar' ), true ) ) {
			return array();
		}
		$tkey = 'nlpglang_fam_' . md5( $rest );
		$fam  = get_transient( $tkey );
		if ( is_array( $fam ) ) {
			return $fam;
		}
		$fam = array();
		foreach ( array( 'he' => $rest, 'en' => 'en/' . $rest, 'fr' => 'fr/' . $rest, 'ru' => 'ru/' . $rest, 'ar' => 'ar/' . $rest ) as $lang => $path ) {
			$p = get_page_by_path( $path, OBJECT, 'page' );
			if ( $p && 'publish' === $p->post_status ) {
				$fam[ $lang ] = get_permalink( $p );
			}
		}
		set_transient( $tkey, $fam, 12 * HOUR_IN_SECONDS );
		return $fam;
	}
}

add_action( 'save_post_page', function ( $post_id ) {
	delete_transient( 'nlpglang_fam_' . md5( nadlan_pglang_restpath( $post_id ) ) );
} );

add_action( 'wp_head', function () {
	static $done = false;
	if ( $done || ! is_page() ) {
		return;
	}
	$done = true;
	$fam = nadlan_pglang_family( get_queried_object_id() );
	if ( count( $fam ) < 2 || empty( $fam['he'] ) ) {
		return;
	}
	echo "\n<!-- page language cluster -->\n";
	foreach ( $fam as $lang => $url ) {
		printf( '<link rel="alternate" hreflang="%s" href="%s" />' . "\n", esc_attr( $lang ), esc_url( $url ) );
	}
	printf( '<link rel="alternate" hreflang="x-default" href="%s" />' . "\n", esc_url( $fam['he'] ) );
}, 3 );

add_action( 'wp_footer', function () {
	$lang = nadlan_pglang_lang();
	if ( '' === $lang || ! function_exists( 'nadlan_plang_chrome_map' ) ) {
		return;
	}
	$map = nadlan_plang_chrome_map( $lang );
	if ( ! $map ) {
		return;
	}
	?>
<script>
(function () {
	'use strict';
	var MAP = <?php echo wp_json_encode( $map ); ?>;
	var zones = document.querySelectorAll('.nlpc-site-header, header, footer, a[href="#content"], .skip-link');
	zones.forEach(function (zone) {
		var walker = document.createTreeWalker(zone, NodeFilter.SHOW_TEXT, null);
		var node;
		while ((node = walker.nextNode())) {
			var t = node.nodeValue.trim();
			if (t && Object.prototype.hasOwnProperty.call(MAP, t)) {
				node.nodeValue = node.nodeValue.replace(t, MAP[t]);
			}
		}
	});
})();
</script>
	<?php
}, 21 );
