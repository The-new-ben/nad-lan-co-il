<?php
// HAD-707 local preview only: expands [nadlan_designer], [nadlan_designers] and [nadlan_tool] in a page body with the REAL plugin
// functions on minimal WordPress stubs, and points every plugin URL at the local file server (repo root on 127.0.0.1:47961).
//   php render_shortcodes.php < body.html > expanded.html
define( 'ABSPATH', __DIR__ . '/' );
define( 'MINUTE_IN_SECONDS', 60 ); define( 'HOUR_IN_SECONDS', 3600 ); define( 'DAY_IN_SECONDS', 86400 );
define( 'NADLAN_CONFIG_VERSION', 'local' );
$GLOBALS['F'] = array();
class WP_Error { function __construct( $c = '', $m = '', $d = null ) {} }
function is_wp_error( $x ) { return $x instanceof WP_Error; }
function get_option( $k, $d = false ) { return $d; }
function get_transient( $k ) { return false; }
function set_transient( $k, $v, $t = 0 ) { return true; }
function wp_salt( $s = '' ) { return 'local-' . $s; }
function wp_unslash( $v ) { return $v; }
function wp_json_encode( $d, $o = 0 ) { return json_encode( $d, $o ); }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function rest_url( $p = '' ) { return '/wp-json/' . $p; }
function plugins_url( $p, $f ) { return '/plugins/nadlan-config/' . $p; }
function wp_strip_all_tags( $t, $r = false ) { return trim( strip_tags( (string) $t ) ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s, $p = null ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function antispambot( $s ) { return $s; }
function is_admin() { return false; }
function has_shortcode( $c, $t ) { return false !== strpos( (string) $c, '[' . $t ); }
function is_singular() { return true; } function get_post() { return null; }
function shortcode_atts( $pairs, $atts, $sc = '' ) { $atts = (array) $atts; $o = array(); foreach ( $pairs as $k => $v ) { $o[ $k ] = array_key_exists( $k, $atts ) ? $atts[ $k ] : $v; } return $o; }
function add_filter( $t, $cb, $p = 10, $n = 1 ) { $GLOBALS['F'][ $t ][] = $cb; }
function apply_filters( $t, $v, ...$a ) { foreach ( $GLOBALS['F'][ $t ] ?? array() as $cb ) { $v = $cb( $v, ...$a ); } return $v; }
function add_action() {} function add_shortcode() {}
function nadlan_ps_current() { return false; }
$PLUG = dirname( __DIR__, 3 ) . '/plugins/nadlan-config';
require $PLUG . '/inc/designer.php';
require $PLUG . '/inc/design-tools.php';

$html = stream_get_contents( STDIN );
$atts = function ( $s ) { preg_match_all( '/([a-z]+)="([^"]*)"/', $s, $m, PREG_SET_ORDER ); $o = array(); foreach ( $m as $x ) { $o[ $x[1] ] = $x[2]; } return $o; };
$html = preg_replace_callback( '/\[nadlan_designer(?![a-z])([^\]]*)\]/', function ( $m ) use ( $atts ) { return nadlan_dsg_shortcode( $atts( $m[1] ) ); }, $html );
$html = preg_replace_callback( '/\[nadlan_designers\]/', function () { return nadlan_dpg_designers_shortcode(); }, $html );
$html = preg_replace_callback( '/\[nadlan_room_photo\]/', function () { return nadlan_dsg_room_photo_shortcode( array() ); }, $html );
$tools = apply_filters( 'nadlan_nli_tools', array() );
$html  = preg_replace_callback( '/\[nadlan_tool([^\]]*)\]/', function ( $m ) use ( $atts, $tools ) {
	$a = $atts( $m[1] ); $id = $a['id'] ?? '';
	if ( ! isset( $tools[ $id ] ) ) { return '<p style="color:red">UNKNOWN TOOL ' . esc_html( $id ) . '</p>'; }
	$t = $tools[ $id ]; $set = isset( $a['preset'] ) ? array( 'preset' => $a['preset'] ) : array();
	$h = '<section class="nli" dir="rtl" lang="he" aria-label="' . esc_attr( $t['name'] ) . '"><div class="nli-host" data-nli="' . esc_attr( $id ) . '" data-nli-data="/plugins/nadlan-config/assets/instruments/data/design.json"' . ( $set ? ' data-nli-set="' . esc_attr( json_encode( $set, JSON_UNESCAPED_UNICODE ) ) . '"' : '' ) . '>'
		. '<div class="nli__panel"><p class="nli__kicker">' . esc_html( $t['kicker'] ) . '</p><h2 class="nli__title">' . esc_html( $t['name'] ) . '</h2>' . nadlan_dsg_summary( $id ) . '</div></div>'
		. '<nav class="nli__rel" aria-label="כלים קשורים"><span>כלים קשורים:</span><a href="/design-studio/">עיצוב דירה אונליין</a></nav></section>';
	return apply_filters( 'do_shortcode_tag', $h, 'nadlan_tool', $a );
}, $html );
echo $html;
