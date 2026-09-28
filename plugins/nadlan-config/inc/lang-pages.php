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
		return function_exists( 'nadlan_plang_suffix' ) ? (string) nadlan_plang_suffix() : '';
	}
}

if ( ! function_exists( 'nadlan_lp_dict' ) ) {
	function nadlan_lp_dict() {
		static $d = null;
		if ( null !== $d ) { return $d; }
		$f = dirname( __DIR__ ) . '/i18n/lang-pages.json';
		$d = is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : null;
		if ( ! is_array( $d ) ) { $d = array(); }
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
		$seg = preg_replace_callback( '#<(script|style|textarea|noscript|template)\b.*?</\1\s*>|<!--.*?-->#is', function ( $m ) use ( &$keep ) {
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
		$b = strpos( $html, '<body' );
		if ( false === $b ) { return $html; }
		// the parts that are never touched: the article (real translated text) and the lead
		$skip = array();
		foreach ( array( '#<(\w+)\b[^>]*\bclass="[^"]*\bnadlan-project-article\b[^"]*"#', '#<(div)\b[^>]*\bclass="nl-lead"#' ) as $re ) {
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
