<?php
/**
 * Titles and descriptions the site crawl of 24.9.2026 found missing (4,398 sitemap URLs, Screaming Frog):
 *  - 2,726 professional cards had no description, and the 2,698 contractor cards imported from the
 *    contractors register had a bare "{name} - נדלן" title (four cards share "מחאמיד מוחמד - נדלן");
 *  - 144 glossary terms and about 80 other pages and posts had no description.
 *
 * Everything here fills only an EMPTY description or a BARE title, from data the post already holds.
 * A hand-written Yoast title or description, or a module's own filter, always wins. Demo cards
 * (source demo_seed) are left exactly as they are: the owner decides about them (HAD-248).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_seo_gap_plain' ) ) {
	function nadlan_seo_gap_plain( $s ) {
		$s = html_entity_decode( wp_strip_all_tags( (string) $s ), ENT_QUOTES, 'UTF-8' );
		return trim( preg_replace( '/\s+/u', ' ', $s ) );
	}
}

if ( ! function_exists( 'nadlan_seo_gap_cut' ) ) {
	/** At most $max characters, cut at a word boundary. */
	function nadlan_seo_gap_cut( $s, $max = 155 ) {
		$s = nadlan_seo_gap_plain( $s );
		if ( mb_strlen( $s ) <= $max ) { return $s; }
		$s = mb_substr( $s, 0, $max );
		$sp = mb_strrpos( $s, ' ' );
		return rtrim( $sp > 60 ? mb_substr( $s, 0, $sp ) : $s, " ,;:-" );
	}
}

if ( ! function_exists( 'nadlan_seo_gap_is_bare_title' ) ) {
	function nadlan_seo_gap_is_bare_title( $title, $post_id ) {
		$t    = nadlan_seo_gap_plain( $title );
		$name = nadlan_seo_gap_plain( get_the_title( $post_id ) );
		$site = nadlan_seo_gap_plain( get_bloginfo( 'name' ) );
		return '' === $t || $t === $name || $t === $name . ' - ' . $site || $t === $name . ' | ' . $site;
	}
}

if ( ! function_exists( 'nadlan_seo_gap_is_demo' ) ) {
	function nadlan_seo_gap_is_demo( $post_id ) {
		$demo = get_post_meta( $post_id, 'is_demo', true );
		return 'demo_seed' === (string) get_post_meta( $post_id, 'source', true ) || '1' === (string) $demo || true === $demo;
	}
}

if ( ! function_exists( 'nadlan_seo_gap_trade' ) ) {
	/**
	 * What the card holder does, in words a searcher uses. A register contractor gets the trade of the first
	 * branch the register lists for them ("שיפוצים" -> "קבלן שיפוצים"); anyone else the directory's own
	 * profession label, in the card's grammatical gender.
	 */
	function nadlan_seo_gap_trade( $post_id ) {
		$prof = (string) get_post_meta( $post_id, 'profession', true );
		if ( 'kablan' === $prof ) {
			$map = array(
				'שיפוצ' => 'קבלן שיפוצים', 'חשמל' => 'קבלן חשמל', 'אינסטלצ' => 'קבלן אינסטלציה', 'מיזוג' => 'קבלן מיזוג אוויר',
				'איטום' => 'קבלן איטום', 'בריכ' => 'קבלן בריכות', 'סולאר' => 'קבלן מערכות סולאריות', 'פיתוח' => 'קבלן פיתוח',
				'כביש' => 'קבלן תשתיות', 'תשתי' => 'קבלן תשתיות', 'שלד' => 'קבלן בנייה', 'בני' => 'קבלן בנייה',
			);
			foreach ( explode( '·', (string) get_post_meta( $post_id, 'classification', true ) ) as $branch ) {
				foreach ( $map as $needle => $label ) {
					if ( false !== mb_strpos( $branch, $needle ) ) { return $label; }
				}
			}
			return 'קבלן רשום';
		}
		if ( '' === $prof ) { return ''; }
		return function_exists( 'nadlan_dir_prof_label' ) ? nadlan_dir_prof_label( $prof, $post_id ) : '';
	}
}

/* Professional cards: "{name}: {trade} ב{city} | נדלן" instead of "{name} - נדלן". */
if ( ! function_exists( 'nadlan_seo_gap_title' ) ) {
	function nadlan_seo_gap_title( $title ) {
		if ( ! is_singular( 'nadlan_professional' ) ) { return $title; }
		$id = get_queried_object_id();
		if ( ! $id || nadlan_seo_gap_is_demo( $id ) || ! nadlan_seo_gap_is_bare_title( $title, $id ) ) { return $title; }
		$trade = nadlan_seo_gap_trade( $id );
		if ( '' === $trade || false !== mb_strpos( nadlan_seo_gap_plain( get_the_title( $id ) ), $trade ) ) { return $title; }
		$city = trim( (string) get_post_meta( $id, 'city', true ) );
		// plain text: Yoast escapes the title once on output (a quote shows as &quot; live, checked 24.9.2026)
		return nadlan_seo_gap_plain( get_the_title( $id ) ) . ': ' . $trade . ( '' !== $city ? ' ב' . $city : '' ) . ' | נדלן';
	}
}
add_filter( 'wpseo_title', 'nadlan_seo_gap_title', 30 );
add_filter( 'pre_get_document_title', 'nadlan_seo_gap_title', 30 );

/* Descriptions: professional cards from their register facts, everything else from its own opening text. */
if ( ! function_exists( 'nadlan_seo_gap_description' ) ) {
	function nadlan_seo_gap_description( $desc ) {
		if ( '' !== trim( (string) $desc ) || ! is_singular() ) { return $desc; }
		$id = get_queried_object_id();
		if ( ! $id || nadlan_seo_gap_is_demo( $id ) ) { return $desc; }
		$type = get_post_type( $id );
		if ( 'nadlan_professional' === $type ) {
			$name  = nadlan_seo_gap_plain( get_the_title( $id ) );
			$trade = nadlan_seo_gap_trade( $id );
			$city  = trim( (string) get_post_meta( $id, 'city', true ) );
			$reg   = trim( (string) get_post_meta( $id, 'registry_number', true ) );
			$d     = $name . ( '' !== $trade ? ': ' . $trade : '' ) . ( '' !== $city ? ' ב' . $city : '' ) . '.';
			if ( 'pinkas_hakablanim' === (string) get_post_meta( $id, 'source', true ) && '' !== $reg ) {
				$branches = preg_replace( '/\s*\(סיווג\s*\d+\)/u', '', (string) get_post_meta( $id, 'classification', true ) );
				$branches = implode( ', ', array_slice( array_filter( array_map( 'trim', explode( '·', $branches ) ) ), 0, 3 ) );
				$d .= ' רשום בפנקס הקבלנים, מספר ' . $reg . '.' . ( '' !== $branches ? ' תחומי רישום: ' . $branches . '.' : '' );
			} else {
				$areas = trim( (string) get_post_meta( $id, 'areas_served', true ) );
				if ( '' !== $areas ) { $d .= ' אזורי עבודה: ' . implode( ', ', array_slice( array_map( 'trim', explode( ',', $areas ) ), 0, 4 ) ) . '.'; }
			}
			return nadlan_seo_gap_cut( $d );
		}
		$post = get_post( $id );
		if ( ! $post || post_password_required( $post ) ) { return $desc; }
		$src = has_excerpt( $id ) ? $post->post_excerpt : '';
		if ( '' === nadlan_seo_gap_plain( $src ) ) {
			// the first paragraph that reads as a sentence, shortcodes and blocks removed
			if ( preg_match_all( '#<p\b[^>]*>(.*?)</p>#is', strip_shortcodes( (string) $post->post_content ), $m ) ) {
				foreach ( $m[1] as $p ) {
					if ( mb_strlen( nadlan_seo_gap_plain( $p ) ) >= 60 ) { $src = $p; break; }
				}
			}
		}
		$src = nadlan_seo_gap_cut( $src );
		return '' !== $src ? $src : $desc; // Yoast escapes the attribute on output
	}
}
add_filter( 'wpseo_metadesc', 'nadlan_seo_gap_description', 90 );
