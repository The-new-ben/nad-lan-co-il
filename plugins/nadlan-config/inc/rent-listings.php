<?php
/* G5 (26.10.2026): [nadlan_rent_listings limit="12"] for /דירות-להשכרה/. Reads only; uses inc/archive-grid.php's card. */
if ( ! defined( 'ABSPATH' ) ) { exit; }
add_shortcode( 'nadlan_rent_listings', function ( $atts ) {
	if ( ! function_exists( 'nadlan_plist_card' ) || ! function_exists( 'nadlan_pl_nodemo' ) || ! function_exists( 'nadlan_pl_is_demo' ) ) { return ''; }
	$a   = shortcode_atts( array( 'limit' => 12 ), $atts );
	$ids = get_posts( array( 'post_type' => 'nadlan_property', 'post_status' => 'publish', 'posts_per_page' => -1, 'fields' => 'ids', 'no_found_rows' => true,
		'orderby' => 'date', 'order' => 'DESC', 'meta_query' => array( 'relation' => 'AND', nadlan_pl_nodemo(), array( 'key' => 'listing_type', 'value' => 'rent' ) ) ) );
	$ids = array_values( array_filter( $ids, function ( $id ) { return ! nadlan_pl_is_demo( $id ); } ) );
	$arch = add_query_arg( 'listing_type', 'rent', get_post_type_archive_link( 'nadlan_property' ) );
	$css  = '<style id="nlrh-list-css">' . file_get_contents( __DIR__ . '/../assets/rent-listings.css' ) . '</style>';  // listings.css shipped as assets/rent-listings.css
	if ( ! $ids ) { return $css . '<p class="nlrh-count">אין כרגע מודעות להשכרה באתר. <a href="' . esc_url( $arch ) . '">לכל המודעות</a></p>'; }
	$by = array();
	foreach ( $ids as $id ) { $c = trim( (string) get_post_meta( $id, 'city', true ) ); if ( '' !== $c ) { $by[ $c ] = ( $by[ $c ] ?? 0 ) + 1; } }
	arsort( $by );
	$parts = array(); foreach ( $by as $c => $k ) { $parts[] = ( 1 === $k ? 'אחת ב' : $k . ' ב' ) . $c; }
	$n = count( $ids );
	// Hebrew join: commas, then "ו" before the last part ("ו-" before a digit): "10 בתל אביב-יפו ואחת בקרית אתא"
	$last = $parts ? array_pop( $parts ) : ''; $joined = ( $parts ? implode( ', ', $parts ) . ' ' . ( preg_match( '/^\d/', $last ) ? 'ו-' : 'ו' ) : '' ) . $last; if ( '' !== $last ) { $parts[] = $last; }
	$h = $css . '<div class="nlrh-list"><p class="nlrh-count"><b>' . (int) $n . '</b> ' . ( 1 === $n ? 'מודעה להשכרה באתר' : 'מודעות להשכרה באתר' ) . ( $parts ? ': ' . esc_html( $joined ) : '' ) . '.</p><div class="nlpl-grid">';
	$items = array(); $pos = 1;
	foreach ( array_slice( $ids, 0, max( 1, (int) $a['limit'] ) ) as $id ) {
		$h .= nadlan_plist_card( $id );
		$items[] = array( '@type' => 'ListItem', 'position' => $pos++, 'url' => get_permalink( $id ), 'name' => html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) );
	}
	$h .= '</div><p class="nlrh-more"><a href="' . esc_url( $arch ) . '">לכל המודעות באתר, עם סינון לפי עיר, חדרים ומחיר</a></p></div>';
	$h .= '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => 'דירות להשכרה באתר', 'numberOfItems' => $n, 'itemListElement' => $items ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>';
	return $h;
} );
