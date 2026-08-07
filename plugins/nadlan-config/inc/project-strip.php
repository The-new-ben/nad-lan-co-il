<?php
/**
 * [nl_project_strip] - a light live-inventory strip for pillar pages.
 *
 * WHY (owner directive 2026-08-06): the new-projects anchor "must display
 * projects for traffic", not merely link out. /catalog/ is a heavy
 * self-contained maplibre page; embedding it into an 18k-word article would
 * double its weight. This strip is the light server-side answer: the latest
 * Hebrew-base projects as cards + CTAs into the full catalog and archive.
 * Reusable on any pillar (michraz, commercial) by dropping the shortcode.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_shortcode( 'nl_project_strip', function ( $atts ) {
	$atts = shortcode_atts( array( 'count' => 8 ), $atts, 'nl_project_strip' );
	$lang = function_exists( 'nadlan_pglang_lang' ) ? nadlan_pglang_lang() : '';
	if ( '' === $lang ) {
		$lang = 'he';
	}
	$t = array(
		'he' => array( 'רוצים לראות מלאי אמיתי? אלו הפרויקטים המובילים במאגר', 'למדף הפרויקטים הנבחרים', 'לכל הפרויקטים' ),
		'en' => array( 'The leading projects in the catalog', 'The curated project shelf', 'All projects' ),
		'fr' => array( 'Les projets phares du catalogue', 'La selection premium', 'Tous les projets' ),
		'ru' => array( 'Ведущие проекты каталога', 'Отобранная витрина', 'Все проекты' ),
		'ar' => array( 'المشاريع الرائدة في الكتالوج', 'الرف المختار', 'جميع المشاريع' ),
	);
	$s = isset( $t[ $lang ] ) ? $t[ $lang ] : $t['he'];

	/* CURATION LAW (owner 2026-08-07): the strip leads with the projects that
	   carry the most material - 3D model first, then sourced facilities -
	   because they convert and because their developers are the paying side.
	   Bare cards are not banned sitewide, they just never lead. DETERMINISTIC
	   material queries, NOT a recency sample: meta updates do not bump
	   post_modified, so the flagship GLB projects fell out of a modified-DESC
	   sample entirely (found live on the 166 strip - rainbow/duo missing). */
	$cards  = array();
	$seen   = array();
	$rounds = array(
		array( 'key' => 'project_model_glb', 'score_base' => 40 ),
		array( 'key' => 'project_facilities', 'score_base' => 10 ),
	);
	foreach ( $rounds as $round ) {
		if ( count( $cards ) >= (int) $atts['count'] ) {
			break;
		}
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_project',
			'post_status'    => 'publish',
			'posts_per_page' => 60,
			'no_found_rows'  => true,
			'meta_query'     => array(
				array(
					'key'     => $round['key'],
					'value'   => '',
					'compare' => '!=',
				),
			),
		) );
		$scored = array();
		foreach ( $q->posts as $p ) {
			/* Hebrew base entries only - language variants of the same
			   building would render as duplicates in every language. */
			if ( isset( $seen[ $p->ID ] ) || preg_match( '/-(en|fr|ru|ar)$/', $p->post_name ) ) {
				continue;
			}
			$score = $round['score_base'];
			$fac   = (string) get_post_meta( $p->ID, 'project_facilities', true );
			if ( '' !== $fac ) {
				$score += min( 3 * count( array_filter( array_map( 'trim', explode( ',', $fac ) ) ) ), 18 );
			}
			if ( '' !== (string) get_post_meta( $p->ID, 'lat', true ) ) {
				$score += 6;
			}
			if ( '' !== (string) get_post_meta( $p->ID, '_nl_faq_schema', true ) ) {
				$score += 8;
			}
			$scored[] = array( $score, $p );
		}
		usort( $scored, function ( $a, $b ) {
			return $b[0] - $a[0];
		} );
		foreach ( $scored as $row ) {
			$cards[]            = $row[1];
			$seen[ $row[1]->ID ] = true;
			if ( count( $cards ) >= (int) $atts['count'] ) {
				break;
			}
		}
	}
	if ( ! $cards ) {
		return '';
	}

	static $css_done = false;
	$out = '';
	if ( ! $css_done ) {
		$css_done = true;
		$out .= '<style>.nlpstrip{margin:26px 0;padding:18px;border:1px solid #E2DCD0;border-radius:14px;background:#FBF7EC}'
			. '.nlpstrip h2{margin:0 0 12px;font-size:20px}'
			. '.nlpstrip .g{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}'
			. '.nlpstrip .g a{display:block;padding:12px 14px;border:1px solid #D9D2C4;border-radius:10px;background:#fff;'
			. 'text-decoration:none;font-weight:600;line-height:1.4}'
			. '.nlpstrip .cta{margin-top:14px;display:flex;flex-wrap:wrap;gap:10px}'
			. '.nlpstrip .cta a{display:inline-block;padding:10px 18px;border-radius:999px;background:#1B1A17;color:#F6F1E6;'
			. 'text-decoration:none;font-weight:700}'
			. '.nlpstrip .cta a + a{background:transparent;color:#1B1A17;border:1px solid #1B1A17}</style>';
	}
	$out .= '<section class="nlpstrip"><h2>' . esc_html( $s[0] ) . '</h2><div class="g">';
	foreach ( $cards as $p ) {
		$out .= '<a href="' . esc_url( get_permalink( $p ) ) . '">' . esc_html( get_the_title( $p ) ) . '</a>';
	}
	/* /premium/ is the curated shelf; /catalog/ failed the quality gate
	   (demo rows, em dashes, no imagery) and gets no traffic from us */
	$out .= '</div><div class="cta">'
		. '<a href="' . esc_url( home_url( '/premium/' ) ) . '">' . esc_html( $s[1] ) . '</a>'
		. '<a href="' . esc_url( home_url( '/projects/' ) ) . '">' . esc_html( $s[2] ) . '</a>'
		. '</div></section>';
	return $out;
} );
