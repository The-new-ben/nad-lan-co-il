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

/* 1.72.7xx (HAD-793, gap 24 of the long film): an article in English, French, Russian or Arabic printed its author's name in Hebrew
   ("Written by בן בטש", the meta author, the share labels and the Person schema). The name now follows the page's language: the
   user meta nadlan_name_latin when set, else the author's own URL slug spelling (ben-betesh = "Ben Betesh"). Hebrew pages unchanged. */
if ( ! function_exists( 'nadlan_pglang_author_latin' ) ) {
	function nadlan_pglang_author_latin( $user_id ) {
		$user_id = (int) $user_id;
		if ( $user_id < 1 ) {
			return '';
		}
		$own = trim( (string) get_user_meta( $user_id, 'nadlan_name_latin', true ) );
		if ( '' !== $own ) {
			return $own;
		}
		$map  = array( 'ben-betesh' => 'Ben Betesh' );
		$slug = (string) get_the_author_meta( 'user_nicename', $user_id );
		return isset( $map[ $slug ] ) ? $map[ $slug ] : '';
	}
}

if ( ! function_exists( 'nadlan_pglang_foreign' ) ) {
	/** The page's language when it is one of the four foreign languages, else ''. */
	function nadlan_pglang_foreign() {
		$l = function_exists( 'nadlan_pglang_lang' ) ? nadlan_pglang_lang() : '';
		return in_array( $l, array( 'en', 'fr', 'ru', 'ar' ), true ) ? $l : '';
	}
}

if ( ! function_exists( 'nadlan_pglang_author_pair' ) ) {
	/** array( hebrew display name, latin name ) of the queried post's author, or null. */
	function nadlan_pglang_author_pair() {
		if ( '' === nadlan_pglang_foreign() || ! is_singular() ) {
			return null;
		}
		$uid   = (int) get_post_field( 'post_author', get_queried_object_id() );
		$latin = nadlan_pglang_author_latin( $uid );
		$he    = (string) get_the_author_meta( 'display_name', $uid );
		return ( '' !== $latin && '' !== $he && $he !== $latin ) ? array( $he, $latin ) : null;
	}
}

add_filter( 'render_block_core/post-author-name', function ( $html ) {
	$p = nadlan_pglang_author_pair();
	return $p ? str_replace( esc_html( $p[0] ), esc_html( $p[1] ), (string) $html ) : $html;
}, 20 );

add_filter( 'wpseo_meta_author', function ( $name ) {
	$p = nadlan_pglang_author_pair();
	return ( $p && (string) $name === $p[0] ) ? $p[1] : $name;
}, 20 );

/* the share card labels ("נכתב על יד", "זמן קריאה מוערך") in the page's language */
add_filter( 'wpseo_enhanced_slack_data', function ( $data ) {
	$lang = nadlan_pglang_foreign();
	if ( '' === $lang || ! is_array( $data ) ) {
		return $data;
	}
	$p  = nadlan_pglang_author_pair();
	$lb = array(
		'en' => array( 'Written by', 'Est. reading time', '%d minutes' ),
		'fr' => array( 'Écrit par', 'Temps de lecture estimé', '%d minutes' ),
		'ru' => array( 'Автор', 'Время чтения', '%d мин.' ),
		'ar' => array( 'كتبه', 'مدة القراءة التقديرية', '%d دقيقة' ),
	);
	$out = array();
	foreach ( $data as $k => $v ) {
		if ( false !== strpos( (string) $k, 'נכתב' ) ) {
			$out[ $lb[ $lang ][0] ] = ( $p && (string) $v === $p[0] ) ? $p[1] : $v;
		} elseif ( false !== strpos( (string) $k, 'זמן קריאה' ) && preg_match( '/\d+/', (string) $v, $m ) ) {
			$out[ $lb[ $lang ][1] ] = sprintf( $lb[ $lang ][2], (int) $m[0] );
		} else {
			$out[ $k ] = $v;
		}
	}
	return $out;
}, 20 );

add_filter( 'wpseo_schema_person', function ( $data ) {
	$p = nadlan_pglang_author_pair();
	if ( ! $p || ! is_array( $data ) || ! isset( $data['name'] ) || $data['name'] !== $p[0] ) {
		return $data;
	}
	$data['name'] = $p[1];
	if ( isset( $data['image']['caption'] ) && $data['image']['caption'] === $p[0] ) {
		$data['image']['caption'] = $p[1];
	}
	if ( 'Ben Betesh' === $p[1] && 'en' === nadlan_pglang_foreign() ) {
		$data['description'] = 'Ben Betesh is a lawyer working in real estate, family and commercial law, with an office at 18 Raoul Wallenberg St., Tel Aviv.';
	}
	return $data;
}, 20 );

add_filter( 'wpseo_schema_article', function ( $data ) {
	$p = nadlan_pglang_author_pair();
	if ( $p && is_array( $data ) && isset( $data['author']['name'] ) && $data['author']['name'] === $p[0] ) {
		$data['author']['name'] = $p[1];
	}
	return $data;
}, 20 );

/* the article's own title and headings on an English, French or Russian post were set in the Hebrew serif (1.72.7xx: !important, the theme's
   heading rule outranked the first version), so Latin and Cyrillic
   fell back to a Times-like face; they now use IBM Plex Sans (already loaded on these pages). On a wide screen the empty margin
   beside the opening carries the article's contents (it scrolls with the page: nothing floats). */
add_action( 'wp_head', function () {
	$lang = nadlan_pglang_foreign();
	if ( ! in_array( $lang, array( 'en', 'fr', 'ru' ), true ) || ! is_singular( 'post' ) ) {
		return;
	}
	echo '<style id="nlpglang-latin">html[lang="' . esc_attr( $lang ) . '"] body.single-post h1.wp-block-post-title,html[lang="' . esc_attr( $lang ) . '"] body.single-post .wp-block-post-content>h2,html[lang="' . esc_attr( $lang ) . '"] body.single-post .wp-block-post-content>div>h2,html[lang="' . esc_attr( $lang ) . '"] body.single-post .wp-block-post-content>h3,html[lang="' . esc_attr( $lang ) . '"] body.single-post .wp-block-post-content>div>h3{font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif!important;font-weight:600!important;letter-spacing:-.01em}'
		. '.nlpg-toc{display:none}@media (min-width:1440px){body.single-post .wp-block-post-content{position:relative}.nlpg-toc{display:block;position:absolute;top:0;left:0;width:260px;margin:0;padding:14px 0 0;border-top:2px solid #12202A;font:400 14px/1.45 "IBM Plex Sans",system-ui,sans-serif;color:#3E4C58}'
		. '.nlpg-toc b{display:block;margin:0 0 8px;font:500 12px/1.3 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase;color:#2F6F86}.nlpg-toc ol{margin:0;padding:0;list-style:none;counter-reset:t}.nlpg-toc li{counter-increment:t;margin:0;padding:6px 0;border-bottom:1px solid #D3DCE2}'
		. '.nlpg-toc li::before{content:counter(t,decimal-leading-zero) "  ";font:500 12px "IBM Plex Mono",monospace;color:#5E6A75}.nlpg-toc a{color:#12202A;text-decoration:none}.nlpg-toc a:hover{color:#2F6F86;text-decoration:underline}.nlpg-toc a:focus-visible{outline:2px solid #2F6F86;outline-offset:2px}}</style>' . "\n";
}, 30 );

add_action( 'wp_footer', function () {
	$lang = nadlan_pglang_foreign();
	if ( ! in_array( $lang, array( 'en', 'fr', 'ru' ), true ) || ! is_singular( 'post' ) ) {
		return;
	}
	$t = array( 'en' => 'On this page', 'fr' => 'Sur cette page', 'ru' => 'На этой странице' );
	?>
<script>
(function () {
	'use strict';
	var box = document.querySelector('body.single-post .wp-block-post-content');
	if (!box || box.querySelector('.nlpg-toc')) { return; }
	var root = box;  /* an article may sit inside one wrapper (div.nadlan-en-article) */
	while (root.children.length === 1 && root.firstElementChild.tagName === 'DIV') { root = root.firstElementChild; }
	var hs = [].slice.call(root.querySelectorAll(':scope > h2')).filter(function (h) { return h.textContent.trim().length > 2; });
	if (hs.length < 4) { return; }
	var used = {};
	var items = hs.slice(0, 24).map(function (h, i) {
		if (!h.id) {
			var base = h.textContent.trim().toLowerCase().replace(/[^a-z0-9Ѐ-ӿÀ-ſ]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60) || ('s' + (i + 1));
			var id = base, n = 2;
			while (used[id] || document.getElementById(id)) { id = base + '-' + n++; }
			h.id = id;
		}
		used[h.id] = 1;
		var li = document.createElement('li'), a = document.createElement('a');
		a.href = '#' + h.id; a.textContent = h.textContent.trim();
		li.appendChild(a);
		return li;
	});
	var nav = document.createElement('nav'), b = document.createElement('b'), ol = document.createElement('ol');
	nav.className = 'nlpg-toc'; nav.setAttribute('aria-label', <?php echo wp_json_encode( $t[ $lang ] ); ?>);
	b.textContent = <?php echo wp_json_encode( $t[ $lang ] ); ?>;
	items.forEach(function (li) { ol.appendChild(li); });
	nav.appendChild(b); nav.appendChild(ol);
	box.insertBefore(nav, box.firstChild);
	/* place it in the empty margin beside the text column, measured (the content box spans the whole screen) */
	function place() {
		var r = box.getBoundingClientRect(), right = 0, top = null;
		[].slice.call(root.children, root === box ? 1 : 0, 16).forEach(function (c) {
			var q = c.getBoundingClientRect();
			if (q.width > 0) { right = Math.max(right, q.right); if (top === null) { top = q.top; } }
		});
		var space = r.right - right;
		if (window.innerWidth < 1440 || space < 300) { nav.style.display = 'none'; return; }
		nav.style.display = '';
		nav.style.left = Math.round(right - r.left + 40) + 'px';
		nav.style.top = Math.round((top === null ? r.top : top) - r.top) + 'px';
		nav.style.width = Math.round(Math.min(280, space - 80)) + 'px';
	}
	place();
	window.addEventListener('resize', place, { passive: true });
	window.addEventListener('load', place);
})();
</script>
	<?php
}, 22 );
