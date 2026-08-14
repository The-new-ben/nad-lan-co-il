<?php
/**
 * Visual breadcrumbs + language switcher at the TOP of every project page.
 *
 * WHY (owner, 2026-08-07, verified live): breadcrumbs existed only as schema,
 * never visually; the language switcher was injected by engine JS ~1,265px
 * deep on mobile - a visitor who cannot read Hebrew never discovers that the
 * page exists in their language. Both belong at the very top, server-rendered.
 *
 * Mechanics: prepend at the_content 32 (above the recomposed lead at 21 and
 * every other prepender in the map), plus a PHP_INT_MAX repair pass for pages
 * that rebuild content wholesale (utopia) - registered after feature-bar's
 * repair so the tie-break keeps this bar above the feature bar.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_ptop_strings' ) ) {
	function nadlan_ptop_strings( $lang ) {
		$t = array(
			'he' => array( 'בית', 'פרויקטים' ),
			'en' => array( 'Home', 'Projects' ),
			'fr' => array( 'Accueil', 'Projets' ),
			'ru' => array( 'Главная', 'Проекты' ),
			'ar' => array( 'الرئيسية', 'المشاريع' ),
		);
		return isset( $t[ $lang ] ) ? $t[ $lang ] : $t['he'];
	}
}

if ( ! function_exists( 'nadlan_ptop_render' ) ) {
	function nadlan_ptop_render( $content ) {
		if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}
		if ( false !== strpos( $content, 'class="nlptop"' ) ) {
			return $content;
		}
		$id   = get_queried_object_id();
		$lang = function_exists( 'nadlan_plang_suffix' ) ? nadlan_plang_suffix() : '';
		if ( '' === $lang ) {
			$lang = 'he';
		}
		$s     = nadlan_ptop_strings( $lang );
		$title = get_the_title( $id );

		$crumbs = '<div class="nlptop-c"><a href="' . esc_url( home_url( '/' ) ) . '">' . esc_html( $s[0] ) . '</a>'
			. '<i>›</i><a href="' . esc_url( home_url( '/projects/' ) ) . '">' . esc_html( $s[1] ) . '</a>'
			. '<i>›</i><b>' . esc_html( wp_html_excerpt( $title, 44, '…' ) ) . '</b></div>';

		$langs = '';
		if ( function_exists( 'nadlan_plang_family' ) ) {
			$fam = nadlan_plang_family( $id );
			if ( count( $fam ) > 1 ) {
				$names = array( 'he' => 'עב', 'en' => 'EN', 'fr' => 'FR', 'ru' => 'RU', 'ar' => 'AR' );
				$langs = '<div class="nlptop-l" aria-label="Languages">';
				foreach ( array( 'he', 'en', 'fr', 'ru', 'ar' ) as $l ) {
					if ( empty( $fam[ $l ] ) ) {
						continue;
					}
					$langs .= ( $l === $lang )
						? '<b>' . esc_html( $names[ $l ] ) . '</b>'
						: '<a href="' . esc_url( $fam[ $l ] ) . '" hreflang="' . esc_attr( $l ) . '">' . esc_html( $names[ $l ] ) . '</a>';
				}
				$langs .= '</div>';
			}
		}

		static $css_done = false;
		$css = '';
		if ( ! $css_done ) {
			$css_done = true;
			$css = '<style>.nlptop{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;'
				. 'margin:0 0 14px;padding:9px 12px;background:#FBF7EC;border:1px solid #E2DCD0;border-radius:12px;'
				. 'font:500 13px/1.5 Heebo,system-ui,sans-serif}'
				. '.nlptop-c{display:flex;align-items:center;gap:7px;min-width:0}'
				. '.nlptop-c a{color:#6B4E1E;text-decoration:none}.nlptop-c a:hover{text-decoration:underline}'
				. '.nlptop-c i{color:#B7AE9C;font-style:normal}'
				. '.nlptop-c b{color:#1B1A17;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:46vw}'
				. '.nlptop-l{display:flex;gap:4px}'
				. '.nlptop-l a,.nlptop-l b{padding:3px 9px;border-radius:999px;text-decoration:none;font-weight:700;font-size:12px}'
				. '.nlptop-l a{color:#6B4E1E;border:1px solid #D9D2C4;background:#fff}'
				. '.nlptop-l b{color:#F6F1E6;background:#1B1A17}</style>';
		}
		return $css . '<nav class="nlptop" aria-label="breadcrumbs">' . $crumbs . $langs . '</nav>' . $content;
	}
}
/* 32 > every prepender in the feature-bar map, so this bar tops the page */
add_filter( 'the_content', 'nadlan_ptop_render', 32 );
/* repair pass for wholesale rebuilders (utopia) - the presence check makes it
   a no-op everywhere else; registered after feature-bar so this runs later
   and lands on top */
add_filter( 'the_content', 'nadlan_ptop_render', PHP_INT_MAX );
