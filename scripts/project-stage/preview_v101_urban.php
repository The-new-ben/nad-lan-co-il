<?php
define( 'ABSPATH', __DIR__ . '/' );
$GLOBALS['SC'] = array();
function add_shortcode( $n, $cb ) { $GLOBALS['SC'][ $n ] = $cb; } function add_action() {} function add_filter() {} function register_rest_route() {}
function rest_url( $p ) { return 'https://nad-lan.co.il/wp-json/' . $p; } function esc_url( $s ) { return $s; } function esc_js( $s ) { return $s; }
function esc_html( $s ) { return htmlspecialchars( (string) $s ); } function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function get_option( $k, $d = '' ) { return $d; } function wp_json_encode( $v, $f = 0 ) { return json_encode( $v, $f ); }
function nadlan_cmpmap_token() { return getenv( 'NL_PK' ); } function nadlan_ur_map_seo_html() { return ''; }
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/urban-map.php';
if ( ! function_exists( 'nadlan_ur_map_on' ) ) { function nadlan_ur_map_on() { return true; } }
echo call_user_func( $GLOBALS['SC']['nadlan_ur_map'] );
