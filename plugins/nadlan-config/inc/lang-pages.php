<?php
/**
 * LanguagePages (design system L9Nqz7Viv7K3MYeZrBc9s8 version 84, 28.9.2026): every word outside the article on a
 * project's language page speaks the page's language. The owner, 28.9: "the languages has to be, and the SEO has to be
 * perfect". Measured that day on the 56 language pages (/projects/<slug>-en|fr|ru|ar/): 46 to 118 Hebrew strings each,
 * none of them in the article: the header and the footer (the theme's; the chrome script of inc/project-lang.php swapped
 * a few in the browser only), the accessibility panel, the area-prices band under the lead (catalog-plus), where the
 * project stands (milestones), the price, finance and "everything around the project" sections (project-experience),
 * the card's facts (cards-render), the developer's name in the notice (legal-notice).
 *
 * One pass on the finished HTML, in the server, so the page's source (what a search engine reads) is right too:
 *  - the dictionary is i18n/lang-pages.json (built by scripts/i18n/build_lang_pages.py): exact strings, patterns with
 *    numbers and places, and names (developers, cities, streets, the nearby projects), keyed by the Hebrew the site prints;
 *  - text nodes and the aria-label, title, alt and placeholder attributes that hold Hebrew are translated; anything the
 *    dictionary does not know stays as it was (never a guess), and is counted in a comment at the end of the page;
 *  - the article (real translated text) and the lead are never touched, nor scripts, styles and form fields;
 *  - on the left-to-right languages a block that said dir="rtl" says dir="ltr", and lang="he" becomes the page's language.
 * Fails open: any error returns the page as it was. Off switch: option nadlan_lang_pages = '0'.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_lp_lang' ) ) {
	/** The page's language when this pass runs on it ('' = not a project's language page). */
	function nadlan_lp_lang() {
		if ( is_admin() || '0' === (string) get_option( 'nadlan_lang_pages', '1' ) ) { return ''; }
		$l = function_exists( 'nadlan_plang_suffix' ) ? (string) nadlan_plang_suffix() : '';
		$GLOBALS['nadlan_lp_project'] = '' !== $l;
		// every other language page too (28.9.2026): the language homes (/en/ ...) and the guides, by the language the page
		// already declares (inc/i18n.php, inc/page-lang.php); their bodies are real translated text and keep their words,
		// since only whole strings the dictionary knows, or lines made only of known names, are changed
		if ( '' === $l && function_exists( 'nadlan_current_lang' ) && ( is_singular() || is_front_page() ) ) {
			$c = (string) nadlan_current_lang();
			if ( in_array( $c, array( 'en', 'fr', 'ru', 'ar' ), true ) ) { $l = $c; }
		}
		return $l;
	}
}

if ( ! function_exists( 'nadlan_lp_dict' ) ) {
	function nadlan_lp_dict() {
		static $d = null;
		if ( null !== $d ) { return $d; }
		$f = dirname( __DIR__ ) . '/i18n/lang-pages.json';
		$d = is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : null;
		if ( ! is_array( $d ) ) { $d = array(); }
		// HAD-361: the stage's own words (i18n/stage-dict.json) and the other language pages' (i18n/lang-other.json) join
		foreach ( array( 'stage-dict.json', 'lang-other.json' ) as $x ) {
			$g = dirname( __DIR__ ) . '/i18n/' . $x;
			$e = is_readable( $g ) ? json_decode( (string) file_get_contents( $g ), true ) : null;
			if ( ! is_array( $e ) ) { continue; }
			$d['exact']    = array_merge( (array) ( $e['exact'] ?? array() ), (array) ( $d['exact'] ?? array() ) );
			$d['names']    = array_merge( (array) ( $e['names'] ?? array() ), (array) ( $d['names'] ?? array() ) );
			$d['patterns'] = array_merge( (array) ( $d['patterns'] ?? array() ), (array) ( $e['patterns'] ?? array() ) );
		}
		// the header and footer words the language homes had by a word-by-word swap (inc/i18n.php), now as whole strings
		if ( function_exists( 'nadlan_i18n_theme_map' ) ) {
			foreach ( array( 'en', 'fr', 'ru', 'ar' ) as $l ) {
				foreach ( (array) nadlan_i18n_theme_map( $l ) as $he => $tr ) {
					if ( ! isset( $d['exact'][ $he ][ $l ] ) ) { $d['exact'][ $he ][ $l ] = $tr; }
				}
			}
		}
		return $d;
	}
}

if ( ! function_exists( 'nadlan_lp_tr' ) ) {
	/** One string (trimmed, spaces collapsed) in $lang, or null when the dictionary does not know it. */
	function nadlan_lp_tr( $s, $lang ) {
		$d = nadlan_lp_dict();
		if ( isset( $d['exact'][ $s ][ $lang ] ) ) { return (string) $d['exact'][ $s ][ $lang ]; }
		if ( isset( $d['names'][ $s ][ $lang ] ) ) { return (string) $d['names'][ $s ][ $lang ]; }
		foreach ( (array) ( $d['patterns'] ?? array() ) as $p ) {
			if ( empty( $p['re'] ) || empty( $p[ $lang ] ) || ! preg_match( '#' . $p['re'] . '#u', $s, $m ) ) { continue; }
			$out = (string) $p[ $lang ];
			for ( $i = count( $m ) - 1; $i >= 1; $i-- ) {
				$c = $m[ $i ];
				if ( isset( $d['names'][ $c ][ $lang ] ) ) {
					$c = (string) $d['names'][ $c ][ $lang ];
				} elseif ( isset( $d['exact'][ $c ][ $lang ] ) ) {
					$c = (string) $d['exact'][ $c ][ $lang ];
				} elseif ( preg_match( '/[\x{0590}-\x{05FF}]/u', $c ) ) {
					return null; // a place the dictionary does not know: the whole line stays as it was, never half translated
				}
				$out = str_replace( '{' . $i . '}', $c, $out );
			}
			return $out;
		}
		// a known name inside a longer line (the notice: "... the official website of ישראל קנדה ..."), longest first
		static $nm = array();
		if ( ! isset( $nm[ $lang ] ) ) {
			$nm[ $lang ] = array();
			foreach ( (array) ( $d['names'] ?? array() ) as $he => $tr ) {
				if ( isset( $tr[ $lang ] ) ) { $nm[ $lang ][ (string) $he ] = (string) $tr[ $lang ]; }
			}
		}
		if ( $nm[ $lang ] ) {
			$t = strtr( $s, $nm[ $lang ] );
			if ( $t !== $s && ! preg_match( '/[\x{0590}-\x{05FF}]/u', $t ) ) { return $t; }
		}
		return null;
	}
}

if ( ! function_exists( 'nadlan_lp_close' ) ) {
	/** The offset just after the element that opens at $start closes (nesting of the same tag counted); 0 if none. */
	function nadlan_lp_close( $html, $start, $tag ) {
		$depth = 0;
		$pos   = $start;
		while ( preg_match( '#<(/?)' . $tag . '\b[^>]*>#i', $html, $m, PREG_OFFSET_CAPTURE, $pos ) ) {
			$depth += '/' === $m[1][0] ? -1 : 1;
			$pos    = $m[0][1] + strlen( $m[0][0] );
			if ( 0 === $depth ) { return $pos; }
		}
		return 0;
	}
}

if ( ! function_exists( 'nadlan_lp_swap' ) ) {
	/** The pass itself, on a stretch of HTML with no article in it. $n counts [translated, left]. */
	function nadlan_lp_swap( $seg, $lang, &$n ) {
		$he   = '/[\x{0590}-\x{05FF}]/u';
		$keep = array();
		// scripts, styles, form fields and comments are set aside and put back as they were
		// (and code: a guide names a Hebrew term on purpose in <code>, 28.9.2026)
		$seg = preg_replace_callback( '#<(script|style|textarea|noscript|template|code)\b.*?</\1\s*>|<!--.*?-->#is', function ( $m ) use ( &$keep ) {
			$keep[] = $m[0];
			return "\x01" . ( count( $keep ) - 1 ) . "\x01";
		}, $seg );
		if ( null === $seg ) { return null; }
		$one = function ( $raw ) use ( $lang, $he, &$n ) {
			$txt = html_entity_decode( $raw, ENT_QUOTES | ENT_HTML5, 'UTF-8' );
			$key = trim( preg_replace( '/\s+/u', ' ', $txt ) );
			if ( '' === $key || ! preg_match( $he, $key ) ) { return null; }
			$tr = nadlan_lp_tr( $key, $lang );
			if ( null === $tr ) { $n[1]++; return null; }
			$n[0]++;
			return $tr;
		};
		// text nodes
		$seg = preg_replace_callback( '#>([^<]++)<#u', function ( $m ) use ( $one ) {
			$tr = $one( $m[1] );
			if ( null === $tr ) { return $m[0]; }
			preg_match( '/^\s*/u', $m[1], $a );
			preg_match( '/\s*$/u', $m[1], $z );
			return '>' . $a[0] . esc_html( $tr ) . $z[0] . '<';
		}, $seg );
		if ( null === $seg ) { return null; }
		// the attributes a person reads or hears
		$seg = preg_replace_callback( '#(\s(?:aria-label|title|alt|placeholder)=")([^"]*+)"#u', function ( $m ) use ( $one ) {
			$tr = $one( $m[2] );
			return null === $tr ? $m[0] : $m[1] . esc_attr( $tr ) . '"';
		}, $seg );
		if ( null === $seg ) { return null; }
		// the direction and language of the blocks around the words
		if ( ! in_array( $lang, array( 'he', 'ar' ), true ) ) {
			$seg = preg_replace( '#(<[a-z][a-z0-9]*\b[^>]*?\s)dir="rtl"#i', '$1dir="ltr"', $seg );
		}
		$seg = preg_replace( '#(<[a-z][a-z0-9]*\b[^>]*?\s)lang="he"#i', '$1lang="' . esc_attr( $lang ) . '"', $seg );
		if ( null === $seg ) { return null; }
		return preg_replace_callback( "#\x01(\\d+)\x01#", function ( $m ) use ( $keep ) { return $keep[ (int) $m[1] ]; }, $seg );
	}
}

if ( ! function_exists( 'nadlan_lp_compose' ) ) {
	function nadlan_lp_compose( $html, $lang ) {
		if ( ! is_string( $html ) || '' === $lang ) { return $html; }
		// every structured-data block on the page (the project's own schema too, not only Yoast's graph), by the same
		// dictionary: an unknown string, a street address, stays as it was (1.72.349)
		if ( function_exists( 'nadlan_lp_schema_walk' ) && false !== strpos( $html, 'application/ld+json' ) ) {
			$ld = preg_replace_callback( '#(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)#is', function ( $m ) use ( $lang ) {
				if ( ! preg_match( '/[\x{0590}-\x{05FF}]/u', $m[2] ) ) { return $m[0]; }
				$j = json_decode( $m[2], true );
				if ( ! is_array( $j ) ) { return $m[0]; }
				$o = wp_json_encode( nadlan_lp_schema_walk( $j, $lang ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
				return is_string( $o ) ? $m[1] . str_replace( '</', '<\/', $o ) . $m[3] : $m[0];
			}, $html );
			if ( is_string( $ld ) ) { $html = $ld; }
		}
		$b = strpos( $html, '<body' );
		if ( false === $b ) { return $html; }
		// the parts that are never touched: the article (real translated text) and the lead
		$skip = array();
		$res  = array( '#<(\w+)\b[^>]*\bclass="[^"]*\bnadlan-project-article\b[^"]*"#', '#<(div)\b[^>]*\bclass="nl-lead"#' );
		// the other language pages (the guides, the buying guide ...): their body is the page's own translated text, kept
		// whole; the language homes' body is the home's blocks (the site's own words), which are translated
		$home = function_exists( 'nadlan_is_language_home' ) && nadlan_is_language_home();
		if ( empty( $GLOBALS['nadlan_lp_project'] ) && ! $home ) {
			$res[] = '#<(div)\b[^>]*\bclass="[^"]*\bentry-content\b[^"]*"#';
		}
		foreach ( $res as $re ) {
			if ( preg_match( $re, $html, $m, PREG_OFFSET_CAPTURE, $b ) ) {
				$e = nadlan_lp_close( $html, $m[0][1], $m[1][0] );
				if ( $e ) { $skip[] = array( $m[0][1], $e ); }
			}
		}
		usort( $skip, function ( $x, $y ) { return $x[0] - $y[0]; } );
		$out  = substr( $html, 0, $b );
		$pos  = $b;
		$n    = array( 0, 0 );
		foreach ( $skip as $s ) {
			if ( $s[0] < $pos ) { continue; } // nested in a part already kept
			$seg = nadlan_lp_swap( substr( $html, $pos, $s[0] - $pos ), $lang, $n );
			if ( null === $seg ) { return $html; }
			$out .= $seg . substr( $html, $s[0], $s[1] - $s[0] );
			$pos  = $s[1];
		}
		$seg = nadlan_lp_swap( substr( $html, $pos ), $lang, $n );
		if ( null === $seg ) { return $html; }
		$out .= $seg;
		// the count, for the audit (tools/lang_pages_check.py): translated / left in Hebrew
		$c = strrpos( $out, '</body>' );
		return false === $c ? $out : substr( $out, 0, $c ) . '<!-- nadlan-lang-pages ' . $lang . ' ' . (int) $n[0] . '/' . (int) $n[1] . ' -->' . substr( $out, $c );
	}
}

/* The outermost buffer on a language page: started before every other page buffer (the stage's and the title's at
   priority 0, catalog-plus at 1), so it runs last, on the finished HTML. */
add_action( 'template_redirect', function () {
	$lang = nadlan_lp_lang();
	if ( '' === $lang || 'he' === $lang ) { return; }
	ob_start( function ( $html ) use ( $lang ) {
		try {
			return nadlan_lp_compose( $html, $lang );
		} catch ( \Throwable $e ) {
			return $html;
		}
	} );
}, -5 );

/* The head of a language page (28.9.2026): what a search engine reads first. Measured that day on the 145 language
   pages: 51 titles ended in Hebrew (the project pages' ", תל אביב יפו - מחירים, דירות ובחירה מהבניין | נדלן" from
   inc/bulk-project-seo.php, the guides' "- נדלן"), the 89 pages that are not a project's said og:locale he_IL, every
   page named the site "נדלן" in og:site_name, and the structured data carried Hebrew descriptions, breadcrumbs and
   city names. Here, on a language page only: the site's Hebrew name at the end of a title becomes "| NadLan", Open
   Graph says the page's language and the site's Latin name, and the structured data's words go through the same
   dictionary (the site's name itself, "נדלן", is its registered name and stays). */
if ( ! function_exists( 'nadlan_lp_head_lang' ) ) {
	function nadlan_lp_head_lang() {
		$l = nadlan_lp_lang();
		return in_array( $l, array( 'en', 'fr', 'ru', 'ar' ), true ) ? $l : '';
	}
}

if ( ! function_exists( 'nadlan_lp_title' ) ) {
	function nadlan_lp_title( $title ) {
		$l = nadlan_lp_head_lang();
		if ( '' === $l || ! is_string( $title ) || ! preg_match( '/[\x{0590}-\x{05FF}]/u', $title ) ) { return $title; }
		$t = trim( (string) preg_replace( '/\s*[-|\x{2013}\x{2014}]\s*נדלן\s*$/u', '', $title ) );
		if ( $t !== $title && false === stripos( $t, 'nadlan' ) && false === stripos( $t, 'nad-lan' ) ) { $t .= ' | NadLan'; }
		if ( preg_match( '/[\x{0590}-\x{05FF}]/u', $t ) ) {
			$tr = nadlan_lp_tr( trim( preg_replace( '/\s+/u', ' ', $t ) ), $l );
			if ( null !== $tr ) { $t = $tr; }
		}
		return $t;
	}
}
foreach ( array( 'wpseo_title', 'wpseo_opengraph_title', 'wpseo_twitter_title' ) as $nadlan_lp_hook ) {
	add_filter( $nadlan_lp_hook, 'nadlan_lp_title', 9999 );
}
add_filter( 'pre_get_document_title', 'nadlan_lp_title', 10000 );
unset( $nadlan_lp_hook );

add_filter( 'wpseo_opengraph_site_name', function ( $name ) {
	return '' !== nadlan_lp_head_lang() ? 'NadLan' : $name;
}, 99 );

add_filter( 'wpseo_locale', function ( $locale ) {
	$map = array( 'en' => 'en_US', 'fr' => 'fr_FR', 'ru' => 'ru_RU', 'ar' => 'ar_AR' );
	$l   = nadlan_lp_head_lang();
	return isset( $map[ $l ] ) ? $map[ $l ] : $locale;
}, 99 );

if ( ! function_exists( 'nadlan_lp_schema_walk' ) ) {
	/** Every Hebrew string value in the structured data, by the dictionary; unknown ones stay as they were. */
	function nadlan_lp_schema_walk( $v, $l, $key = '' ) {
		if ( is_array( $v ) ) {
			foreach ( $v as $k => $x ) { $v[ $k ] = nadlan_lp_schema_walk( $x, $l, (string) $k ); }
			return $v;
		}
		if ( ! is_string( $v ) || 'נדלן' === $v || ! preg_match( '/[\x{0590}-\x{05FF}]/u', $v ) ) {
			return ( 'inLanguage' === $key && is_string( $v ) && 0 === strpos( $v, 'he' ) ) ? $l : $v;
		}
		if ( 'name' === $key || 'headline' === $key ) {
			$t = nadlan_lp_title( $v );
			if ( $t !== $v ) { return $t; }
		}
		$tr = nadlan_lp_tr( trim( preg_replace( '/\s+/u', ' ', $v ) ), $l );
		return null === $tr ? $v : $tr;
	}
}
add_filter( 'wpseo_schema_graph', function ( $graph ) {
	$l = nadlan_lp_head_lang();
	return ( '' === $l || ! is_array( $graph ) ) ? $graph : nadlan_lp_schema_walk( $graph, $l );
}, 99 );

/* The breadcrumbs (inc/breadcrumbs.php, the visible trail and its BreadcrumbList): on a language page they start at
   that language's home, and each step is in the page's language when the dictionary knows it. */
add_filter( 'nadlan_breadcrumbs_items', function ( $items ) {
	$l = nadlan_lp_head_lang();
	if ( '' === $l || ! is_array( $items ) || ! $items ) { return $items; }
	$home = array( 'en' => 'Home', 'fr' => 'Accueil', 'ru' => 'Главная', 'ar' => 'الرئيسية' );
	$items[0] = array( 'name' => $home[ $l ], 'url' => home_url( '/' . $l . '/' ) );
	foreach ( $items as $i => $it ) {
		if ( $i > 0 && isset( $it['name'] ) && preg_match( '/[\x{0590}-\x{05FF}]/u', (string) $it['name'] ) ) {
			$tr = nadlan_lp_tr( trim( (string) $it['name'] ), $l );
			if ( null !== $tr ) { $items[ $i ]['name'] = $tr; }
		}
	}
	return $items;
} );
