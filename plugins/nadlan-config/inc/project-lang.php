<?php
/**
 * Language context + hreflang + chrome retranslation for ALL project
 * language variants.
 *
 * WHY (owner report 2026-08-03): rainbow-tel-aviv-en/-ru exist and are fully
 * translated, but rendered "Hebrew with English in the middle". The language
 * context was set only by inc/utopia-sde-dov.php, which is intentionally
 * limited to the UTOPIA slug family - every other project variant rendered
 * with Hebrew chrome. On top of that, even on UTOPIA the theme-rendered
 * platform header (nav, brand tagline, skip link) and footer stay Hebrew on
 * every language: the theme does not route through nadlan_i18n(). And no
 * variant page printed hreflang at all, utopia included.
 *
 * Three repairs, all additive:
 *  1. Any published nadlan_project slug ending -(en|fr|ru|ar) sets the shared
 *     language context, exactly like utopia does (idempotent with it).
 *  2. Every member of a variant family prints the full bidirectional
 *     hreflang cluster with x-default on Hebrew. Canonicals are NOT touched,
 *     that stays whoever owns it today.
 *  3. On non-Hebrew variants a small footer script retranslates the fixed
 *     theme chrome strings (nav labels, brand tagline, skip link, footer
 *     contact) by exact text match. Chrome only - article content is real
 *     translated CMS text and is not touched.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_plang_suffix' ) ) {
	/** Language of the current singular project by slug suffix, '' for none. */
	function nadlan_plang_suffix() {
		if ( ! is_singular( 'nadlan_project' ) ) {
			return '';
		}
		$slug = (string) get_post_field( 'post_name', get_queried_object_id() );
		return preg_match( '/-(en|fr|ru|ar)$/', $slug, $m ) ? $m[1] : '';
	}
}

add_action( 'wp', function () {
	$lang = nadlan_plang_suffix();
	if ( '' !== $lang && function_exists( 'nadlan_set_lang' ) ) {
		nadlan_set_lang( $lang );
	}
}, 1 );

if ( ! function_exists( 'nadlan_plang_family' ) ) {
	/**
	 * Existing published variants of the current project, lang => url.
	 * Cached 12h per base slug; refreshed on any project save.
	 */
	function nadlan_plang_family( $post_id ) {
		$slug = (string) get_post_field( 'post_name', $post_id );
		$base = preg_replace( '/-(en|fr|ru|ar)$/', '', $slug );
		$tkey = 'nlplang_fam_' . md5( $base );
		$fam  = get_transient( $tkey );
		if ( is_array( $fam ) ) {
			return $fam;
		}
		$fam = array();
		foreach ( array( 'he' => $base, 'en' => $base . '-en', 'fr' => $base . '-fr', 'ru' => $base . '-ru', 'ar' => $base . '-ar' ) as $lang => $s ) {
			$p = get_page_by_path( $s, OBJECT, 'nadlan_project' );
			if ( $p && 'publish' === $p->post_status ) {
				$fam[ $lang ] = get_permalink( $p );
			}
		}
		set_transient( $tkey, $fam, 12 * HOUR_IN_SECONDS );
		return $fam;
	}
}

add_action( 'save_post_nadlan_project', function ( $post_id ) {
	$slug = (string) get_post_field( 'post_name', $post_id );
	$base = preg_replace( '/-(en|fr|ru|ar)$/', '', $slug );
	delete_transient( 'nlplang_fam_' . md5( $base ) );
} );

add_action( 'wp_head', function () {
	if ( ! is_singular( 'nadlan_project' ) ) {
		return;
	}
	$fam = nadlan_plang_family( get_queried_object_id() );
	if ( count( $fam ) < 2 ) {
		return;
	}
	$codes = array( 'he' => 'he', 'en' => 'en', 'fr' => 'fr', 'ru' => 'ru', 'ar' => 'ar' );
	echo "\n<!-- project language cluster -->\n";
	foreach ( $fam as $lang => $url ) {
		printf( '<link rel="alternate" hreflang="%s" href="%s" />' . "\n", esc_attr( $codes[ $lang ] ), esc_url( $url ) );
	}
	$xdef = isset( $fam['he'] ) ? $fam['he'] : reset( $fam );
	printf( '<link rel="alternate" hreflang="x-default" href="%s" />' . "\n", esc_url( $xdef ) );
}, 3 );

if ( ! function_exists( 'nadlan_plang_chrome_map' ) ) {
	/**
	 * The theme's fixed Hebrew chrome strings, per language. Chrome only:
	 * these are interface labels, the systematic layer nadlan_i18n() was
	 * built for. Exact-match swaps, so an untranslated string stays Hebrew
	 * rather than half-guessed.
	 */
	function nadlan_plang_chrome_map( $lang ) {
		$map = array(
			'en' => array(
				'פרויקטים'              => 'Projects',
				'קטלוג תלת ממד'         => '3D Catalog',
				'אזורי ביקוש'           => 'Top Areas',
				'מחשבונים'              => 'Calculators',
				'נדל"ן בחו"ל'           => 'Global Properties',
				'נדל״ן בחו״ל'           => 'Global Properties',
				'אנשי מקצוע'            => 'Professionals',
				'מדריכים'               => 'Guides',
				'נדל״ן לפני שפונים ליזם' => 'Check everything before the developer',
				'דלג לתוכן'             => 'Skip to content',
				'צור קשר'               => 'Contact',
			),
			'fr' => array(
				'פרויקטים'              => 'Projets',
				'קטלוג תלת ממד'         => 'Catalogue 3D',
				'אזורי ביקוש'           => 'Quartiers prisés',
				'מחשבונים'              => 'Simulateurs',
				'נדל"ן בחו"ל'           => 'Immobilier à l\'étranger',
				'נדל״ן בחו״ל'           => 'Immobilier à l\'étranger',
				'אנשי מקצוע'            => 'Professionnels',
				'מדריכים'               => 'Guides',
				'נדל״ן לפני שפונים ליזם' => 'Tout vérifier avant le promoteur',
				'דלג לתוכן'             => 'Aller au contenu',
				'צור קשר'               => 'Contact',
			),
			'ru' => array(
				'פרויקטים'              => 'Проекты',
				'קטלוג תלת ממד'         => '3D-каталог',
				'אזורי ביקוש'           => 'Востребованные районы',
				'מחשבונים'              => 'Калькуляторы',
				'נדל"ן בחו"ל'           => 'Недвижимость за рубежом',
				'נדל״ן בחו״ל'           => 'Недвижимость за рубежом',
				'אנשי מקצוע'            => 'Специалисты',
				'מדריכים'               => 'Руководства',
				'נדל״ן לפני שפונים ליזם' => 'Проверьте всё до застройщика',
				'דלג לתוכן'             => 'К содержимому',
				'צור קשר'               => 'Контакты',
			),
			'ar' => array(
				'פרויקטים'              => 'مشاريع',
				'קטלוג תלת ממד'         => 'كتالوج ثلاثي الأبعاد',
				'אזורי ביקוש'           => 'مناطق مطلوبة',
				'מחשבונים'              => 'حاسبات',
				'נדל"ן בחו"ל'           => 'عقارات في الخارج',
				'נדל״ן בחו״ל'           => 'عقارات في الخارج',
				'אנשי מקצוע'            => 'مختصون',
				'מדריכים'               => 'أدلة',
				'נדל״ן לפני שפונים ליזם' => 'تحقق من كل شيء قبل المطور',
				'דלג לתוכן'             => 'تخطي إلى المحتوى',
				'צור קשר'               => 'اتصل بنا',
			),
		);
		return isset( $map[ $lang ] ) ? $map[ $lang ] : array();
	}
}

add_action( 'wp_footer', function () {
	$lang = nadlan_plang_suffix();
	if ( '' === $lang ) {
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
	var LANG = <?php echo wp_json_encode( $lang ); ?>;
	/* chrome only: header, skip link, footer - never the article */
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
	document.documentElement.lang = LANG;
})();
</script>
	<?php
}, 21 );
