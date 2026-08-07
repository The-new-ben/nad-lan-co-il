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
		'he' => array( 'רוצים לראות מלאי אמיתי? אלו פרויקטים חיים מהמאגר', 'לקטלוג המלא עם מפה', 'לכל הפרויקטים' ),
		'en' => array( 'Live projects from the catalog', 'Full catalog with map', 'All projects' ),
		'fr' => array( 'Projets en direct du catalogue', 'Catalogue complet avec carte', 'Tous les projets' ),
		'ru' => array( 'Живые проекты из каталога', 'Полный каталог с картой', 'Все проекты' ),
		'ar' => array( 'مشاريع حية من الكتالوج', 'الكتالوج الكامل مع الخريطة', 'جميع المشاريع' ),
	);
	$s = isset( $t[ $lang ] ) ? $t[ $lang ] : $t['he'];

	/* 100, not 24: recent content deploys touch the LANGUAGE VARIANTS, so the
	   top of the modified-DESC list can be variants wall to wall - live 164
	   rendered an empty strip exactly that way. Variants are filtered below. */
	$q = new WP_Query( array(
		'post_type'      => 'nadlan_project',
		'post_status'    => 'publish',
		'posts_per_page' => 100,
		'orderby'        => 'modified',
		'order'          => 'DESC',
		'no_found_rows'  => true,
	) );
	$cards = array();
	foreach ( $q->posts as $p ) {
		/* Hebrew base entries only - language variants of the same building
		   would render as duplicates in every language. */
		if ( preg_match( '/-(en|fr|ru|ar)$/', $p->post_name ) ) {
			continue;
		}
		$cards[] = $p;
		if ( count( $cards ) >= (int) $atts['count'] ) {
			break;
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
	$out .= '</div><div class="cta">'
		. '<a href="' . esc_url( home_url( '/catalog/' ) ) . '">' . esc_html( $s[1] ) . '</a>'
		. '<a href="' . esc_url( home_url( '/projects/' ) ) . '">' . esc_html( $s[2] ) . '</a>'
		. '</div></section>';
	return $out;
} );
