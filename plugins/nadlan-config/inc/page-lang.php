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
		// 1.72.524: a page or post may declare its own language (meta _nadlan_page_lang), for an English article that lives at the
		// root path (post 4962 /israel-mortgage-non-residents/ was English text inside lang="he-IL"); no URL change, no redirect
		if ( is_singular() ) {
			$own = (string) get_post_meta( get_queried_object_id(), '_nadlan_page_lang', true );
			if ( in_array( $own, array( 'en', 'fr', 'ru', 'ar' ), true ) ) {
				return $own;
			}
		}
		if ( ! is_page() ) {
			return '';
		}
		$id   = get_queried_object_id();
		$tree = array_merge( array( $id ), get_post_ancestors( $id ) );
		$top  = (string) get_post_field( 'post_name', end( $tree ) );
		return in_array( $top, array( 'en', 'fr', 'ru', 'ar' ), true ) ? $top : '';
	}
}

/* 1.72.524: the language override is set through the REST API by editors only (posts and pages) */
add_action( 'init', function () {
	foreach ( array( 'post', 'page' ) as $pt ) {
		register_post_meta( $pt, '_nadlan_page_lang', array( 'type' => 'string', 'single' => true, 'show_in_rest' => true,
			'auth_callback' => function () { return current_user_can( 'edit_posts' ); } ) );
	}
}, 20 );

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

/* 1.72.527: an article marked with its own language (the meta above) keeps the theme's Yoast trail, which started at "דף הבית"
   on an English page; it now starts at that language's home, with the label the language pages use (inc/lang-pages.php) */
add_filter( 'wpseo_breadcrumb_links', function ( $links ) {
	if ( ! is_singular() || ! is_array( $links ) || empty( $links[0] ) || ! is_array( $links[0] ) ) {
		return $links;
	}
	$own  = (string) get_post_meta( get_queried_object_id(), '_nadlan_page_lang', true );
	$home = array( 'en' => 'Home', 'fr' => 'Accueil', 'ru' => 'Главная', 'ar' => 'الرئيسية' );
	if ( isset( $home[ $own ] ) ) {
		$links[0]['text'] = $home[ $own ];
		$links[0]['url']  = home_url( '/' . $own . '/' );
	}
	return $links;
}, 30 );

/* 1.72.527 (found with the English posts): the single post template draws the featured picture in a 3:2 frame with object-fit
   cover, so a 1200x630 chart lost both sides (its title read "reign purchases"). The post's own picture now keeps its shape. */
add_filter( 'render_block_core/post-featured-image', function ( $html, $block, $instance = null ) {
	if ( ! is_singular( 'post' ) || false === strpos( (string) $html, 'aspect-ratio' ) ) {
		return $html;
	}
	$pid = ( $instance && isset( $instance->context['postId'] ) ) ? (int) $instance->context['postId'] : 0;
	if ( $pid && $pid !== (int) get_queried_object_id() ) {
		return $html;
	}
	return preg_replace( '/aspect-ratio:\s*[\d.\/ ]+;?|object-fit:\s*cover;?/', '', $html );
}, 20, 3 );

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
		// 1.72.514: /en|fr|ru|ar/projects/ are the language pages of the Hebrew catalog, which is the post-type archive, not a page
		if ( 'projects' === $rest && empty( $fam['he'] ) ) {
			$fam = array( 'he' => get_post_type_archive_link( 'nadlan_project' ) ) + $fam;
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
