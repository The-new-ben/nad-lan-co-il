<?php
/**
 * nadlan-config - Archive SEO and public hierarchy polish (v1.35.0)
 *
 * Keeps the directory/archive layer consumer-facing, unique, crawlable, and
 * safer for Google title selection. Public copy here must never mention SEO,
 * revenue, CRM, paid leads, suppliers, or internal strategy.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_archive_seo_map' ) ) {
	function nadlan_archive_seo_map() {
		return array(
			'nadlan_professional' => array(
				'archive_title' => 'מאגר בעלי המקצוע',
				'h1'            => 'מצאו בעל מקצוע מאומת לנדל״ן',
				'doc_title'     => 'מאגר בעלי מקצוע בנדל״ן | קבלנים, שמאים ויועצים מאומתים | נדל״ן חכם',
				'description'   => 'מאגר בעלי מקצוע לנדל״ן עם קבלנים, שמאים, יועצי משכנתאות, עורכי דין ואנשי בדק בית. חפשו לפי עיר, תחום, אימות וחוות דעת.',
				'schema_name'   => 'מאגר בעלי מקצוע בנדל״ן',
			),
			'nadlan_project' => array(
				'archive_title' => 'פרויקטים והתחדשות עירונית',
				'h1'            => 'פרויקטים חדשים והתחדשות עירונית',
				'doc_title'     => 'פרויקטים חדשים והתחדשות עירונית | פינוי בינוי ותמ״א 38 | נדל״ן חכם',
				'description'   => 'בדקו פרויקטים חדשים, פינוי בינוי ותמ״א 38 לפי עיר, יזם, סטטוס, מספר יחידות ושלב התקדמות לפני שמתחילים להשוות הצעות.',
				'schema_name'   => 'פרויקטים חדשים והתחדשות עירונית',
			),
			'nadlan_property' => array(
				'archive_title' => 'נכסים למכירה והשקעה',
				'h1'            => 'נכסים למכירה והשקעה',
				'doc_title'     => 'נכסים למכירה והשקעה | דירות, בתים והזדמנויות נדל״ן | נדל״ן חכם',
				'description'   => 'חיפוש נכסים למכירה ולהשקעה עם נתוני מחיר, חדרים, שטח, עיר ושיקולי בדיקה ראשוניים לקונים ולמשקיעים.',
				'schema_name'   => 'נכסים למכירה והשקעה',
			),
			'nadlan_term' => array(
				'archive_title' => 'מילון נדל״ן ומושגים חשובים',
				'h1'            => 'מילון נדל״ן ומושגים חשובים',
				'doc_title'     => 'מילון נדל״ן | מושגים, חוזים, מיסוי ומשכנתאות | נדל״ן חכם',
				'description'   => 'מילון נדל״ן בעברית עם מושגים מעולם רכישת דירה, חוזים, מיסוי מקרקעין, משכנתאות, תכנון, בנייה והשקעות.',
				'schema_name'   => 'מילון נדל״ן',
			),
		);
	}
}

if ( ! function_exists( 'nadlan_archive_current_post_type' ) ) {
	function nadlan_archive_current_post_type() {
		if ( is_post_type_archive( 'nadlan_professional' ) ) { return 'nadlan_professional'; }
		if ( is_post_type_archive( 'nadlan_project' ) ) { return 'nadlan_project'; }
		if ( is_post_type_archive( 'nadlan_property' ) ) { return 'nadlan_property'; }
		if ( is_post_type_archive( 'nadlan_term' ) ) { return 'nadlan_term'; }
		return '';
	}
}

if ( ! function_exists( 'nadlan_archive_seo_for_current' ) ) {
	function nadlan_archive_seo_for_current() {
		$pt  = nadlan_archive_current_post_type();
		$map = nadlan_archive_seo_map();
		return ( $pt && isset( $map[ $pt ] ) ) ? $map[ $pt ] : array();
	}
}

if ( ! function_exists( 'nadlan_archive_get_label' ) ) {
	function nadlan_archive_get_label( $post_type, $key, $fallback = '' ) {
		$map = nadlan_archive_seo_map();
		return isset( $map[ $post_type ][ $key ] ) ? $map[ $post_type ][ $key ] : $fallback;
	}
}

if ( ! function_exists( 'nadlan_archive_render_header' ) ) {
	function nadlan_archive_render_header() {
		ob_start();
		get_header();
		$html = (string) ob_get_clean();
		$html = nadlan_archive_replace_theme_compat_header( $html );
		echo nadlan_archive_demote_first_site_h1( $html );
	}
}

if ( ! function_exists( 'nadlan_archive_render_footer' ) ) {
	function nadlan_archive_render_footer() {
		ob_start();
		get_footer();
		$html = (string) ob_get_clean();
		echo nadlan_archive_replace_theme_compat_footer( $html );
	}
}

if ( ! function_exists( 'nadlan_archive_render_template_part' ) ) {
	function nadlan_archive_render_template_part( $slug ) {
		if ( ! function_exists( 'do_blocks' ) ) { return ''; }
		$block = '<!-- wp:template-part {"slug":"' . esc_attr( $slug ) . '"} /-->';
		return trim( (string) do_blocks( $block ) );
	}
}

if ( ! function_exists( 'nadlan_archive_replace_theme_compat_header' ) ) {
	function nadlan_archive_replace_theme_compat_header( $html ) {
		if ( ! function_exists( 'wp_is_block_theme' ) || ! wp_is_block_theme() ) { return $html; }
		$part = nadlan_archive_render_template_part( 'header' );
		if ( $part === '' ) { return $html; }
		$pattern = '#<div id="header"[^>]*>.*?</div>\s*</div>\s*<hr\s*/?>#is';
		$fixed = preg_replace( $pattern, $part, $html, 1 );
		return is_string( $fixed ) && $fixed !== '' ? $fixed : $html;
	}
}

if ( ! function_exists( 'nadlan_archive_replace_theme_compat_footer' ) ) {
	function nadlan_archive_replace_theme_compat_footer( $html ) {
		if ( ! function_exists( 'wp_is_block_theme' ) || ! wp_is_block_theme() ) { return $html; }
		$part = nadlan_archive_render_template_part( 'footer' );
		if ( $part === '' ) { return $html; }
		$pattern = '#<hr\s*/?>\s*<div id="footer"[^>]*>.*?</div>#is';
		$fixed = preg_replace( $pattern, $part, $html, 1 );
		return is_string( $fixed ) && $fixed !== '' ? $fixed : $html;
	}
}

if ( ! function_exists( 'nadlan_archive_demote_first_site_h1' ) ) {
	function nadlan_archive_demote_first_site_h1( $html ) {
		if ( ! is_string( $html ) || $html === '' ) { return $html; }
		$needle = 'נדלן חכם';
		if ( strpos( wp_strip_all_tags( $html ), $needle ) === false && strpos( wp_strip_all_tags( $html ), 'נדל״ן חכם' ) === false ) {
			return $html;
		}
		$pattern = '/<h1(\s+[^>]*)?>(\s*<a\b[^>]*>.*?<\/a>\s*)<\/h1>/is';
		$fixed = preg_replace( $pattern, '<div class="nadlan-header-title">$2</div>', $html, 1 );
		return is_string( $fixed ) && $fixed !== '' ? $fixed : $html;
	}
}

if ( ! function_exists( 'nadlan_archive_is_public_catalog_archive' ) ) {
	function nadlan_archive_is_public_catalog_archive() {
		return (bool) nadlan_archive_seo_for_current();
	}
}

if ( ! function_exists( 'nadlan_archive_filter_title' ) ) {
	function nadlan_archive_filter_title( $title ) {
		$seo = nadlan_archive_seo_for_current();
		return ! empty( $seo['archive_title'] ) ? $seo['archive_title'] : $title;
	}
}
add_filter( 'get_the_archive_title', 'nadlan_archive_filter_title', 30 );

if ( ! function_exists( 'nadlan_archive_filter_document_title' ) ) {
	function nadlan_archive_filter_document_title( $title ) {
		$seo = nadlan_archive_seo_for_current();
		return ! empty( $seo['doc_title'] ) ? $seo['doc_title'] : $title;
	}
}
add_filter( 'pre_get_document_title', 'nadlan_archive_filter_document_title', 40 );
add_filter( 'wpseo_title', 'nadlan_archive_filter_document_title', 40 );
add_filter( 'wpseo_opengraph_title', 'nadlan_archive_filter_document_title', 40 );
add_filter( 'wpseo_twitter_title', 'nadlan_archive_filter_document_title', 40 );

if ( ! function_exists( 'nadlan_archive_filter_description' ) ) {
	function nadlan_archive_filter_description( $description ) {
		$seo = nadlan_archive_seo_for_current();
		return ! empty( $seo['description'] ) ? $seo['description'] : $description;
	}
}
add_filter( 'wpseo_metadesc', 'nadlan_archive_filter_description', 40 );
add_filter( 'wpseo_opengraph_desc', 'nadlan_archive_filter_description', 40 );
add_filter( 'wpseo_twitter_description', 'nadlan_archive_filter_description', 40 );

if ( ! function_exists( 'nadlan_archive_document_title_parts' ) ) {
	function nadlan_archive_document_title_parts( $parts ) {
		$seo = nadlan_archive_seo_for_current();
		if ( ! empty( $seo['doc_title'] ) ) {
			$parts['title'] = $seo['doc_title'];
			unset( $parts['site'] );
		}
		return $parts;
	}
}
add_filter( 'document_title_parts', 'nadlan_archive_document_title_parts', 40 );

if ( ! function_exists( 'nadlan_archive_collection_schema' ) ) {
	function nadlan_archive_collection_schema() {
		if ( ! nadlan_archive_is_public_catalog_archive() ) { return; }
		$seo = nadlan_archive_seo_for_current();
		if ( empty( $seo['schema_name'] ) ) { return; }
		$data = array(
			'@context'    => 'https://schema.org',
			'@type'       => 'CollectionPage',
			'name'        => $seo['schema_name'],
			'description' => $seo['description'],
			'url'         => get_post_type_archive_link( nadlan_archive_current_post_type() ),
			'isPartOf'    => array(
				'@type' => 'WebSite',
				'name'  => 'נדל״ן חכם',
				'url'   => home_url( '/' ),
			),
		);
		echo "\n<script type=\"application/ld+json\">" . wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	}
}
add_action( 'wp_head', 'nadlan_archive_collection_schema', 30 );

if ( ! function_exists( 'nadlan_archive_viewport_fallback' ) ) {
	function nadlan_archive_viewport_fallback() {
		if ( ! nadlan_archive_is_public_catalog_archive() ) { return; }
		echo "\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n";
	}
}
add_action( 'wp_head', 'nadlan_archive_viewport_fallback', 1 );
