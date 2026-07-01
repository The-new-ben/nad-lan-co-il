<?php
/**
 * Bulk SEO fix for the long-tail nadlan_project catalog (966 pages per the live
 * sitemap, checked 2026-07-01 -- see docs/marketing/2026-07-01-marketing-seo-revenue-strategy.md).
 *
 * Most of these were imported with just an address as the post title and no
 * SEO meta, so WordPress/Yoast falls back to "{title} - {site name}" -- no
 * buyer intent, no "for sale", nothing a search engine or a buyer's eye
 * catches. A handful of flagship projects (Rainbow, Ashira) already have
 * hand-written, richer titles set via their own higher-priority filters
 * (see project-page-assembly.php) -- this file runs at LOWER priority so it
 * never overrides those; it only fills in the gap for everything else.
 *
 * Honesty rule: only real data is used (the post's own title, and its
 * nadlan_city term IF one is actually set). Never invents a city, price,
 * room count, or floor count that isn't already in the post.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_bulk_project_is_bare_title' ) ) {
	/**
	 * A "bare" title is exactly "{post title} - {site name}" (WordPress/Yoast's
	 * raw default) with none of the buyer-intent words a real listing needs.
	 * If a project already has any of these words in its live title, leave it
	 * alone -- it was written on purpose (imported richer, or hand-edited).
	 */
	function nadlan_bulk_project_is_bare_title( $title, $post_title ) {
		if ( $title === '' || $post_title === '' ) {
			return false;
		}
		$buyer_intent_markers = array( 'דירות', 'למכירה', 'מחיר', 'מחירים', 'קומות', 'יח״ד', 'בינוי', 'תמ״א' );
		foreach ( $buyer_intent_markers as $marker ) {
			if ( mb_strpos( $title, $marker ) !== false ) {
				return false; // already has real buyer-intent content, don't touch it.
			}
		}
		$site_name = get_bloginfo( 'name' );
		$bare_pattern = trim( $post_title ) . ' - ' . trim( $site_name );
		return trim( $title ) === $bare_pattern;
	}
}

if ( ! function_exists( 'nadlan_bulk_project_seo_title' ) ) {
	function nadlan_bulk_project_seo_title( $title ) {
		if ( ! is_singular( 'nadlan_project' ) ) {
			return $title;
		}
		$post_title = get_the_title();
		if ( ! nadlan_bulk_project_is_bare_title( $title, $post_title ) ) {
			return $title;
		}
		// Real data only: the post's own nadlan_city term, if one is actually set.
		$city = '';
		$post_id = get_queried_object_id();
		$terms = $post_id ? get_the_terms( $post_id, 'nadlan_city' ) : false;
		if ( is_array( $terms ) && ! empty( $terms ) && ! is_wp_error( $terms ) ) {
			$city = $terms[0]->name;
		}
		if ( $city !== '' ) {
			return sprintf( '%s — דירות למכירה ב%s | נדלן חכם', $post_title, $city );
		}
		return sprintf( '%s — דירות למכירה | נדלן חכם', $post_title );
	}
}

if ( ! function_exists( 'nadlan_bulk_project_seo_description' ) ) {
	function nadlan_bulk_project_seo_description( $description ) {
		if ( ! is_singular( 'nadlan_project' ) ) {
			return $description;
		}
		if ( trim( (string) $description ) !== '' ) {
			return $description; // real description already set (Yoast meta or content excerpt) -- don't touch it.
		}
		$post_title = get_the_title();
		if ( $post_title === '' ) {
			return $description;
		}
		$city = '';
		$post_id = get_queried_object_id();
		$terms = $post_id ? get_the_terms( $post_id, 'nadlan_city' ) : false;
		if ( is_array( $terms ) && ! empty( $terms ) && ! is_wp_error( $terms ) ) {
			$city = $terms[0]->name;
		}
		if ( $city !== '' ) {
			return sprintf( 'כל המידע על %1$s ב%2$s: פרטי הפרויקט, דירות ויצירת קשר עם נדלן חכם — לפני שמתקדמים בעסקה.', $post_title, $city );
		}
		return sprintf( 'כל המידע על %s: פרטי הפרויקט, דירות ויצירת קשר עם נדלן חכם — לפני שמתקדמים בעסקה.', $post_title );
	}
}

// Priority 5: runs early, so any project-specific filter set at a higher
// priority number (e.g. Rainbow's at 50) still overrides this for its own post.
add_filter( 'wpseo_title', 'nadlan_bulk_project_seo_title', 5 );
add_filter( 'pre_get_document_title', 'nadlan_bulk_project_seo_title', 5 );
add_filter( 'wpseo_metadesc', 'nadlan_bulk_project_seo_description', 5 );
