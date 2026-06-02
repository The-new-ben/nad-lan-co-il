<?php
/**
 * Public URL governance.
 *
 * Public Hebrew copy is allowed. Public Hebrew/non-ASCII URL slugs are not.
 * This module prevents future public content from creating percent-encoded
 * Hebrew paths and gives all agents one code-level guardrail.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_url_has_non_ascii_slug' ) ) {
	function nadlan_url_has_non_ascii_slug( $slug ) {
		$decoded = rawurldecode( (string) $slug );
		return (bool) preg_match( '/[^\x20-\x7E]/', $decoded );
	}
}

if ( ! function_exists( 'nadlan_url_ascii_slug_base' ) ) {
	function nadlan_url_ascii_slug_base( $text, $fallback = 'content' ) {
		$text = wp_strip_all_tags( html_entity_decode( (string) $text, ENT_QUOTES, 'UTF-8' ) );
		$text = strtr( $text, array(
			'א' => 'a', 'ב' => 'b', 'ג' => 'g', 'ד' => 'd', 'ה' => 'h', 'ו' => 'v', 'ז' => 'z',
			'ח' => 'h', 'ט' => 't', 'י' => 'y', 'כ' => 'k', 'ך' => 'k', 'ל' => 'l', 'מ' => 'm',
			'ם' => 'm', 'נ' => 'n', 'ן' => 'n', 'ס' => 's', 'ע' => 'a', 'פ' => 'p', 'ף' => 'p',
			'צ' => 'ts', 'ץ' => 'ts', 'ק' => 'k', 'ר' => 'r', 'ש' => 'sh', 'ת' => 't',
			'׳' => '', '״' => '', '"' => '', "'" => '', '`' => '',
		) );
		$text = remove_accents( $text );
		$text = strtolower( $text );
		$text = preg_replace( '/[^a-z0-9]+/', '-', $text );
		$text = trim( (string) $text, '-' );
		if ( strlen( $text ) > 80 ) {
			$text = trim( substr( $text, 0, 80 ), '-' );
		}
		return $text !== '' ? $text : $fallback;
	}
}

if ( ! function_exists( 'nadlan_url_should_govern_post_type' ) ) {
	function nadlan_url_should_govern_post_type( $post_type ) {
		if ( in_array( $post_type, array( 'revision', 'nav_menu_item', 'wp_navigation', 'attachment' ), true ) ) {
			return false;
		}
		$obj = get_post_type_object( $post_type );
		return $obj && ! empty( $obj->public );
	}
}

add_filter( 'wp_insert_post_data', function ( $data, $postarr ) {
	$post_type = isset( $data['post_type'] ) ? (string) $data['post_type'] : '';
	if ( ! nadlan_url_should_govern_post_type( $post_type ) ) { return $data; }

	$status = isset( $data['post_status'] ) ? (string) $data['post_status'] : '';
	if ( in_array( $status, array( 'inherit', 'auto-draft' ), true ) ) { return $data; }

	$slug = isset( $data['post_name'] ) ? (string) $data['post_name'] : '';
	if ( $slug !== '' && ! nadlan_url_has_non_ascii_slug( $slug ) ) { return $data; }

	$post_id = isset( $postarr['ID'] ) ? (int) $postarr['ID'] : 0;
	$title   = isset( $data['post_title'] ) ? (string) $data['post_title'] : '';
	$base    = nadlan_url_ascii_slug_base( $slug !== '' ? $slug : $title, $post_type . ( $post_id ? '-' . $post_id : '' ) );
	$data['post_name'] = wp_unique_post_slug( $base, $post_id, $status ?: 'publish', $post_type, 0 );

	return $data;
}, 20, 2 );
