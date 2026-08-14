<?php
/**
 * [nl_child_index] - lists the PUBLISHED children of the current page as
 * cards. Built for the /guides/ hubs (he + four languages): scheduled spokes
 * appear here automatically on their publish day, so the hub never links to a
 * 404 and grows by itself as the daily releases go live.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_shortcode( 'nl_child_index', function () {
	$id = get_the_ID();
	if ( ! $id ) {
		return '';
	}
	$kids = get_pages( array(
		'parent'      => $id,
		'sort_column' => 'post_date',
		'sort_order'  => 'DESC',
		'post_status' => 'publish',
	) );
	if ( ! $kids ) {
		return '';
	}
	static $css_done = false;
	$out = '';
	if ( ! $css_done ) {
		$css_done = true;
		$out .= '<style>.nlgidx{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin:18px 0}'
			. '.nlgidx a{display:block;padding:16px 18px;border:1px solid #E2DCD0;border-radius:12px;background:#FBF7EC;'
			. 'text-decoration:none;color:#1B1A17;font-weight:700;line-height:1.5}'
			. '.nlgidx a:hover{border-color:#9C7A3C}'
			. '.nlgidx s{display:block;margin-top:5px;text-decoration:none;font-weight:400;font-size:12.5px;color:#8E877A}</style>';
	}
	$out .= '<div class="nlgidx">';
	foreach ( $kids as $k ) {
		$ex = trim( wp_strip_all_tags( get_post_field( 'post_excerpt', $k->ID ) ) );
		if ( '' === $ex ) {
			$ex = trim( wp_strip_all_tags( wp_html_excerpt( $k->post_content, 400 ) ) );
			$ex = mb_substr( preg_replace( '/\s+/', ' ', $ex ), 0, 110 );
		}
		$out .= '<a href="' . esc_url( get_permalink( $k ) ) . '">' . esc_html( get_the_title( $k ) )
			. '<s>' . esc_html( $ex ) . '</s></a>';
	}
	return $out . '</div>';
} );
