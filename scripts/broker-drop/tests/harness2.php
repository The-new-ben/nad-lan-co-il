<?php
// harness 2: more WordPress stubs, for the 1.1 language layer and the engine-built site
error_reporting( E_ALL );
ini_set( 'display_errors', '1' );
define( 'ABSPATH', __DIR__ . '/' );
define( 'HOUR_IN_SECONDS', 3600 );
define( 'DAY_IN_SECONDS', 86400 );
$GLOBALS['META']  = array();
$GLOBALS['OPT']   = array();
$GLOBALS['POSTS'] = array();
function add_action() {}
function add_filter() {}
function add_shortcode() {}
function register_post_meta() {}
function register_post_type() {}
function register_rest_route() {}
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url_raw( $s ) { return (string) $s; }
function esc_textarea( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function wp_strip_all_tags( $s ) { return strip_tags( (string) $s ); }
function wp_json_encode( $d, $f = 0 ) { return json_encode( $d, $f ); }
function remove_accents( $s ) { return $s; }
function sanitize_title( $s ) { return trim( preg_replace( '/[^a-z0-9]+/', '-', strtolower( (string) $s ) ), '-' ); }
function sanitize_text_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function sanitize_key( $s ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $s ) ); }
function get_option( $k, $d = false ) { return $GLOBALS['OPT'][ $k ] ?? $d; }
function get_permalink( $id ) { return $GLOBALS['POSTS'][ $id ]['link'] ?? 'https://nad-lan.co.il/p/' . $id . '/'; }
function get_post_meta( $id, $k, $single = false ) { return $GLOBALS['META'][ $id ][ $k ] ?? ''; }
function update_post_meta( $id, $k, $v ) { $GLOBALS['META'][ $id ][ $k ] = is_string( $v ) ? stripslashes( $v ) : $v; return true; }
function wp_slash( $v ) { return $v; }
function wp_date( $f, $t = null ) { return date( $f, $t ?: time() ); }
function get_post_time( $f, $gmt = false, $id = 0 ) { return date( $f ); }
function get_post_modified_time( $f, $gmt = false, $id = 0 ) { return time(); }
function get_post_status( $id ) { return $GLOBALS['POSTS'][ $id ]['status'] ?? false; }
function get_post( $id ) { return isset( $GLOBALS['POSTS'][ $id ] ) ? (object) array_merge( array( 'ID' => $id ), $GLOBALS['POSTS'][ $id ] ) : null; }
function get_the_title( $id ) { return $GLOBALS['POSTS'][ $id ]['post_title'] ?? ''; }
function get_the_post_thumbnail_url( $id, $s = '' ) { return ''; }
function wp_get_attachment_url( $id ) { return $id ? 'https://nad-lan.co.il/wp-content/uploads/hero-' . $id . '.jpg' : false; }
function wp_get_attachment_metadata( $id ) { return array( 'width' => 2048, 'height' => 1152 ); }
function get_post_field( $f, $id ) { return $GLOBALS['POSTS'][ $id ][ $f ] ?? ''; }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function rest_url( $p = '' ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function get_posts( $a ) {
	$out = array();
	foreach ( $GLOBALS['POSTS'] as $id => $p ) {
		if ( ( $p['post_type'] ?? '' ) !== ( $a['post_type'] ?? '' ) ) { continue; }
		if ( ! in_array( $p['status'], (array) ( $a['post_status'] ?? array( 'publish' ) ), true ) ) { continue; }
		$ok = true;
		foreach ( (array) ( $a['meta_query'] ?? array() ) as $mq ) {
			if ( (string) ( $GLOBALS['META'][ $id ][ $mq['key'] ] ?? '' ) !== (string) $mq['value'] ) { $ok = false; }
		}
		if ( $ok ) { $out[] = (object) array_merge( array( 'ID' => $id ), $p ); }
	}
	return $out;
}
require __DIR__ . '/../../../plugins/nadlan-config/inc/broker-drop.php';
