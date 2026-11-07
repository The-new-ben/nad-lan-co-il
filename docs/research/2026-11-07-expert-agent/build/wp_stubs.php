<?php
// Minimal WordPress stubs for testing inc/expert-advisor.php outside WordPress (HAD-680). The LLM key is read from the local
// secrets file only inside this process and is never printed.
define( 'ABSPATH', __DIR__ . '/' ); define( 'DAY_IN_SECONDS', 86400 ); define( 'MINUTE_IN_SECONDS', 60 ); define( 'HOUR_IN_SECONDS', 3600 );
$GLOBALS['OPT'] = array(); $GLOBALS['TR'] = array(); $GLOBALS['POSTS'] = array(); $GLOBALS['ROUTES'] = array();
function get_option( $k, $d = false ) { return array_key_exists( $k, $GLOBALS['OPT'] ) ? $GLOBALS['OPT'][ $k ] : $d; }
function update_option( $k, $v, $a = null ) { $GLOBALS['OPT'][ $k ] = $v; return true; }
function delete_option( $k ) { unset( $GLOBALS['OPT'][ $k ] ); return true; }
function get_transient( $k ) { return $GLOBALS['TR'][ $k ] ?? false; }
function set_transient( $k, $v, $t = 0 ) { $GLOBALS['TR'][ $k ] = $v; return true; }
function wp_salt( $s = '' ) { return 'test-salt-' . $s; }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function rest_url( $p = '' ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function get_permalink( $id ) { return $GLOBALS['POSTS'][ is_object( $id ) ? $id->ID : $id ]->url ?? ''; }
function get_post( $id ) { return $GLOBALS['POSTS'][ $id ] ?? null; }
function get_post_type( $id ) { return $GLOBALS['POSTS'][ $id ]->post_type ?? ''; }
function get_the_title( $id ) { $p = is_object( $id ) ? $id : ( $GLOBALS['POSTS'][ $id ] ?? null ); return $p ? $p->post_title : ''; }
function get_post_meta( $id, $k, $s = false ) { return $GLOBALS['POSTS'][ $id ]->meta[ $k ] ?? ''; }
function wp_strip_all_tags( $t, $r = false ) { $t = preg_replace( '@<(script|style)[^>]*?>.*?</\1>@si', '', (string) $t ); $t = strip_tags( $t ); return $r ? preg_replace( '/[\r\n\t ]+/', ' ', $t ) : $t; }
function strip_shortcodes( $t ) { return preg_replace( '/\[[a-z_]+[^\]]*\]/i', '', $t ); }
function wp_json_encode( $d, $o = 0 ) { return json_encode( $d, $o ); }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function untrailingslashit( $s ) { return rtrim( $s, '/' ); }
function sanitize_key( $k ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( $k ) ); }
function absint( $n ) { return abs( (int) $n ); }
function wp_unslash( $v ) { return $v; }
function add_action() {} function add_filter() {} function do_action() {}
function apply_filters( $t, $v ) { return $v; }
function post_type_exists( $t ) { return true; }
function wp_date( $f ) { return date( $f ); }
function is_wp_error( $x ) { return $x instanceof WP_Error; }
class WP_Error { public $c; public $m; function __construct( $c = '', $m = '' ) { $this->c = $c; $this->m = $m; } function get_error_code() { return $this->c; } function get_error_message() { return $this->m; } }
class WP_Query { public $posts = array(); function __construct( $a ) { $q = mb_strtolower( $a['s'] ); foreach ( $GLOBALS['SEARCH'] ?? array() as $id => $t ) { if ( mb_strpos( mb_strtolower( $t ), $q ) !== false ) { $this->posts[] = $id; } } } }
function wp_remote_post( $url, $a ) {
	$h = array(); foreach ( $a['headers'] as $k => $v ) { $h[] = $k . ': ' . $v; }
	$ch = curl_init( $url ); curl_setopt_array( $ch, array( CURLOPT_POST => true, CURLOPT_POSTFIELDS => $a['body'], CURLOPT_HTTPHEADER => $h, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => $a["timeout"] ?? 45, CURLOPT_CAINFO => "C:/Program Files/Git/mingw64/etc/ssl/certs/ca-bundle.crt" ) );
	$b = curl_exec( $ch ); $code = curl_getinfo( $ch, CURLINFO_HTTP_CODE ); $err = curl_error( $ch ); curl_close( $ch );
	if ( false === $b ) { return new WP_Error( 'http', $err ); }
	$GLOBALS["CALLS"][] = array( "req" => json_decode( $a["body"], true ), "code" => $code, "resp" => $b );
	return array( 'code' => $code, 'body' => $b );
}
function wp_remote_retrieve_response_code( $r ) { return $r['code']; }
function wp_remote_retrieve_body( $r ) { return $r['body']; }
