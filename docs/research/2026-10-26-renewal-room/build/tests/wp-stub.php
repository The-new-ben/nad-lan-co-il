<?php
/**
 * A minimal WordPress stand-in, so the room's real PHP (build/inc/*.php) runs outside WordPress: in the tests
 * (test_privacy.php, test_room.php) and behind the local preview server (preview/server.php). Nothing here talks to
 * any site. Storage is in memory, optionally loaded from and saved to a JSON state file (the preview server).
 * $wpdb is a fake that understands exactly the two queries renewal-room.php sends (raw read, compare-and-swap).
 */
if ( ! defined( 'ABSPATH' ) ) { define( 'ABSPATH', __DIR__ . '/' ); }
define( 'MINUTE_IN_SECONDS', 60 );
define( 'HOUR_IN_SECONDS', 3600 );
define( 'DAY_IN_SECONDS', 86400 );
define( 'NADLAN_CONFIG_VERSION', 'rrp-local' );

$GLOBALS['STUB'] = array(
	'posts' => array(), 'meta' => array(), 'options' => array(), 'transients' => array(), 'users' => array(),
	'next_id' => 5000, 'next_meta' => 1, 'uid' => 0, 'now' => '2026-10-26 10:00:00', 'mail' => array(),
	'actions' => array(), 'filters' => array(), 'routes' => array(), 'shortcodes' => array(),
	'rest_base' => 'http://127.0.0.1:8765/wp-json/', 'home' => 'https://nad-lan.co.il', 'before_update' => null, 'queries' => 0,
);
function stub_state_keys() { return array( 'posts', 'meta', 'options', 'transients', 'users', 'next_id', 'next_meta' ); }
function stub_load( $file ) {
	if ( ! is_readable( $file ) ) { return false; }
	$d = json_decode( (string) file_get_contents( $file ), true );
	if ( ! is_array( $d ) ) { return false; }
	foreach ( stub_state_keys() as $k ) { if ( isset( $d[ $k ] ) ) { $GLOBALS['STUB'][ $k ] = $d[ $k ]; } }
	return true;
}
function stub_save( $file ) {
	$d = array();
	foreach ( stub_state_keys() as $k ) { $d[ $k ] = $GLOBALS['STUB'][ $k ]; }
	file_put_contents( $file, json_encode( $d, JSON_UNESCAPED_UNICODE ) );
}
function stub_as( $uid ) { $GLOBALS['STUB']['uid'] = (int) $uid; }
function stub_now( $mysql ) { $GLOBALS['STUB']['now'] = $mysql; }
function stub_user( $id, $email, $name, $caps = array() ) { $GLOBALS['STUB']['users'][ (int) $id ] = array( 'ID' => (int) $id, 'user_email' => $email, 'display_name' => $name, 'caps' => $caps ); }

/* ---------- hooks ---------- */
function add_action( $h, $cb, $p = 10, $n = 1 ) { $GLOBALS['STUB']['actions'][ $h ][] = $cb; return true; }
function add_filter( $h, $cb, $p = 10, $n = 1 ) { $GLOBALS['STUB']['filters'][ $h ][] = array( $cb, $n ); return true; }
function remove_filter( $h, $cb ) { return true; }
function do_action( $h, ...$a ) { foreach ( $GLOBALS['STUB']['actions'][ $h ] ?? array() as $cb ) { call_user_func_array( $cb, $a ); } }
function apply_filters( $h, $v, ...$a ) { foreach ( $GLOBALS['STUB']['filters'][ $h ] ?? array() as $f ) { $v = call_user_func_array( $f[0], array_slice( array_merge( array( $v ), $a ), 0, max( 1, (int) $f[1] ) ) ); } return $v; }
function register_post_type( $t, $a ) { return true; }
function add_rewrite_rule() { return true; }
function flush_rewrite_rules() { return true; }
function add_shortcode( $t, $cb ) { $GLOBALS['STUB']['shortcodes'][ $t ] = $cb; }
function shortcode_exists( $t ) { return isset( $GLOBALS['STUB']['shortcodes'][ $t ] ); }
function do_shortcode( $s ) { if ( preg_match( '/^\[(\w+)\]$/', trim( $s ), $m ) && shortcode_exists( $m[1] ) ) { return call_user_func( $GLOBALS['STUB']['shortcodes'][ $m[1] ] ); } return $s; }
function get_query_var( $k ) { return $GLOBALS['STUB']['qv'][ $k ] ?? ''; }
function wp_next_scheduled( $h ) { return false; }
function wp_schedule_event() { return true; }
function wp_cache_delete() { return true; }
function nocache_headers() {}
function get_header() {}
function get_footer() {}
function wp_safe_redirect( $u ) { return true; }
function wp_login_url( $r = '' ) { return 'https://nad-lan.co.il/wp-login.php'; }
function wp_mail( $to, $s, $b ) { $GLOBALS['STUB']['mail'][] = array( $to, $s ); return true; }
function __( $s ) { return $s; }
function esc_html__( $s ) { return esc_html( $s ); }

/* ---------- urls ---------- */
function home_url( $p = '' ) { return $GLOBALS['STUB']['home'] . $p; }
function rest_url( $p = '' ) { return $GLOBALS['STUB']['rest_base'] . ltrim( $p, '/' ); }
function plugins_url( $p = '', $f = '' ) { return '/' . ltrim( $p, '/' ); }

/* ---------- options and transients ---------- */
function get_option( $k, $d = false ) { return array_key_exists( $k, $GLOBALS['STUB']['options'] ) ? $GLOBALS['STUB']['options'][ $k ] : $d; }
function update_option( $k, $v, $a = null ) { $GLOBALS['STUB']['options'][ $k ] = $v; return true; }
function add_option( $k, $v ) { if ( array_key_exists( $k, $GLOBALS['STUB']['options'] ) ) { return false; } $GLOBALS['STUB']['options'][ $k ] = $v; return true; }
function delete_option( $k ) { unset( $GLOBALS['STUB']['options'][ $k ] ); return true; }
function get_transient( $k ) { return array_key_exists( $k, $GLOBALS['STUB']['transients'] ) ? $GLOBALS['STUB']['transients'][ $k ] : false; }
function set_transient( $k, $v, $t = 0 ) { $GLOBALS['STUB']['transients'][ $k ] = $v; return true; }
function delete_transient( $k ) { unset( $GLOBALS['STUB']['transients'][ $k ] ); return true; }

/* ---------- posts and meta ---------- */
function wp_insert_post( $a, $err = false ) {
	$id = ++$GLOBALS['STUB']['next_id'];
	$GLOBALS['STUB']['posts'][ $id ] = array( 'ID' => $id, 'post_type' => $a['post_type'] ?? 'post', 'post_status' => $a['post_status'] ?? 'publish',
		'post_title' => $a['post_title'] ?? '', 'post_date' => current_time( 'mysql' ), 'post_author' => get_current_user_id() );
	$GLOBALS['STUB']['meta'][ $id ] = array();
	do_action( 'save_post_' . ( $a['post_type'] ?? 'post' ), $id );
	return $id;
}
function get_post( $id ) { $p = $GLOBALS['STUB']['posts'][ (int) $id ] ?? null; return $p ? (object) $p : null; }
function get_post_field( $f, $id ) { return $GLOBALS['STUB']['posts'][ (int) $id ][ $f ] ?? ''; }
function get_the_title( $id ) { return get_post_field( 'post_title', $id ); }
function get_post_time( $fmt, $gmt, $id ) { return strtotime( get_post_field( 'post_date', $id ) ); }
function stub_meta_rows( $id ) { return $GLOBALS['STUB']['meta'][ (int) $id ] ?? array(); }
function get_post_meta( $id, $key = '', $single = false ) {
	$vals = array();
	foreach ( stub_meta_rows( $id ) as $r ) { if ( '' === $key || $r[1] === $key ) { $vals[] = $r[2]; } }
	if ( '' === $key ) { return $vals; }
	return $single ? ( $vals ? $vals[0] : '' ) : $vals;
}
function add_post_meta( $id, $key, $val, $unique = false ) {
	if ( $unique ) { foreach ( stub_meta_rows( $id ) as $r ) { if ( $r[1] === $key ) { return false; } } }
	$GLOBALS['STUB']['meta'][ (int) $id ][] = array( $GLOBALS['STUB']['next_meta']++, $key, is_scalar( $val ) ? (string) wp_unslash( $val ) : $val );
	return true;
}
function update_post_meta( $id, $key, $val ) {
	$val = is_scalar( $val ) ? (string) wp_unslash( $val ) : $val;
	foreach ( $GLOBALS['STUB']['meta'][ (int) $id ] ?? array() as $i => $r ) {
		if ( $r[1] === $key ) { $GLOBALS['STUB']['meta'][ (int) $id ][ $i ][2] = $val; return true; }
	}
	$GLOBALS['STUB']['meta'][ (int) $id ][] = array( $GLOBALS['STUB']['next_meta']++, $key, $val );
	return true;
}
function delete_post_meta( $id, $key, $val = '' ) {
	$rows = stub_meta_rows( $id );
	$GLOBALS['STUB']['meta'][ (int) $id ] = array_values( array_filter( $rows, function ( $r ) use ( $key, $val ) { return ! ( $r[1] === $key && ( '' === $val || (string) $r[2] === (string) $val ) ); } ) );
	return true;
}
function get_posts( $a ) {
	$types = (array) ( $a['post_type'] ?? 'post' );
	$out = array();
	foreach ( $GLOBALS['STUB']['posts'] as $id => $p ) {
		if ( ! in_array( $p['post_type'], $types, true ) ) { continue; }
		if ( 'any' !== ( $a['post_status'] ?? 'publish' ) && ! in_array( $p['post_status'], (array) $a['post_status'], true ) ) { continue; }
		if ( 'trash' === $p['post_status'] ) { continue; }
		$ok = true;
		foreach ( (array) ( $a['meta_query'] ?? array() ) as $q ) {
			if ( ! is_array( $q ) || ! isset( $q['key'] ) ) { continue; }
			$vals = get_post_meta( $id, $q['key'], false );
			$cmp = $q['compare'] ?? '=';
			$hit = false;
			foreach ( $vals as $v ) {
				if ( 'LIKE' === $cmp && false !== stripos( (string) $v, (string) $q['value'] ) ) { $hit = true; }
				if ( 'IN' === $cmp && in_array( (string) $v, array_map( 'strval', (array) $q['value'] ), true ) ) { $hit = true; }
				if ( '=' === $cmp && (string) $v === (string) $q['value'] ) { $hit = true; }
			}
			if ( ! $hit ) { $ok = false; break; }
		}
		if ( $ok ) { $out[] = (int) $id; }
	}
	rsort( $out );
	$n = (int) ( $a['posts_per_page'] ?? 10 );
	if ( $n > 0 ) { $out = array_slice( $out, 0, $n ); }
	return $out;
}

/* ---------- the fake $wpdb (the two queries renewal-room.php sends) ---------- */
class Stub_WPDB {
	public $postmeta = 'wp_postmeta';
	public function prepare( $q, ...$a ) { return array( 'q' => $q, 'a' => $a ); }
	public function get_var( $p ) {
		$GLOBALS['STUB']['queries']++;
		if ( 0 === strpos( $p['q'], 'SELECT meta_value FROM' ) ) {
			list( $pid, $key ) = $p['a'];
			foreach ( stub_meta_rows( $pid ) as $r ) { if ( $r[1] === $key ) { return (string) $r[2]; } }
			return null;
		}
		throw new Exception( 'Stub_WPDB: unknown query ' . $p['q'] );
	}
	public function query( $p ) {
		$GLOBALS['STUB']['queries']++;
		if ( 0 !== strpos( $p['q'], 'UPDATE' ) ) { throw new Exception( 'Stub_WPDB: unknown query ' . $p['q'] ); }
		if ( is_callable( $GLOBALS['STUB']['before_update'] ) ) { $cb = $GLOBALS['STUB']['before_update']; $GLOBALS['STUB']['before_update'] = null; $cb(); } // a writer that slips in between
		list( $new, $pid, $key, $md5 ) = $p['a'];
		foreach ( $GLOBALS['STUB']['meta'][ (int) $pid ] ?? array() as $i => $r ) {
			if ( $r[1] === $key && md5( (string) $r[2] ) === $md5 ) { $GLOBALS['STUB']['meta'][ (int) $pid ][ $i ][2] = $new; return 1; }
		}
		return 0;
	}
}
$GLOBALS['wpdb'] = new Stub_WPDB();

/* ---------- users ---------- */
class Stub_User {
	public $ID = 0; public $user_email = ''; public $display_name = '';
	public function __construct( $u ) { if ( $u ) { $this->ID = (int) $u['ID']; $this->user_email = $u['user_email']; $this->display_name = $u['display_name']; } }
	public function exists() { return $this->ID > 0; }
}
function get_current_user_id() { return (int) $GLOBALS['STUB']['uid']; }
function is_user_logged_in() { return get_current_user_id() > 0; }
function get_userdata( $id ) { $u = $GLOBALS['STUB']['users'][ (int) $id ] ?? null; return $u ? new Stub_User( $u ) : false; }
function wp_get_current_user() { return new Stub_User( $GLOBALS['STUB']['users'][ get_current_user_id() ] ?? null ); }
function get_user_by( $f, $v ) { foreach ( $GLOBALS['STUB']['users'] as $u ) { if ( 'email' === $f && strtolower( $u['user_email'] ) === strtolower( (string) $v ) ) { return new Stub_User( $u ); } } return false; }
function user_can( $uid, $cap ) { $u = $GLOBALS['STUB']['users'][ (int) $uid ] ?? null; return $u && in_array( $cap, $u['caps'], true ); }
function current_user_can( $cap ) { return user_can( get_current_user_id(), $cap ); }
function wp_create_nonce() { return 'stubnonce'; }
function wp_generate_password( $n = 12 ) { $c = 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'; $s = ''; for ( $i = 0; $i < $n; $i++ ) { $s .= $c[ random_int( 0, strlen( $c ) - 1 ) ]; } return $s; }

/* ---------- time ---------- */
function current_time( $t ) { $now = $GLOBALS['STUB']['now']; return 'mysql' === $t ? $now : strtotime( $now ); }
function date_i18n( $f, $ts ) { return date( $f, $ts ); }

/* ---------- formatting and sanitizing (close enough to WordPress for this code) ---------- */
function wp_json_encode( $d, $o = 0 ) { return json_encode( $d, $o ); }
function wp_slash( $v ) { return is_string( $v ) ? addslashes( $v ) : $v; }
function wp_unslash( $v ) { return is_string( $v ) ? stripslashes( $v ) : $v; }
function sanitize_key( $k ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $k ) ); }
function sanitize_text_field( $s ) { $s = strip_tags( (string) $s ); $s = preg_replace( '/[\r\n\t ]+/', ' ', $s ); return trim( $s ); }
function sanitize_textarea_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function sanitize_email( $s ) { return preg_replace( '/[^a-zA-Z0-9@._+\-]/', '', (string) $s ); }
function sanitize_file_name( $s ) { return preg_replace( '/[^a-zA-Z0-9._\-]/', '', (string) $s ); }
function is_email( $s ) { return (bool) filter_var( $s, FILTER_VALIDATE_EMAIL ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url_raw( $s ) { return (string) $s; }
function esc_js( $s ) { return addslashes( (string) $s ); }
function wp_kses_post( $s ) { return (string) $s; }
function absint( $v ) { return abs( (int) $v ); }

/* ---------- REST ---------- */
class WP_Error {
	public $code; public $message; public $data;
	public function __construct( $c = '', $m = '', $d = array() ) { $this->code = $c; $this->message = $m; $this->data = $d; }
	public function get_error_code() { return $this->code; }
	public function get_error_message() { return $this->message; }
	public function get_error_data() { return $this->data; }
}
function is_wp_error( $x ) { return $x instanceof WP_Error; }
class WP_REST_Request implements ArrayAccess {
	private $m; private $url; private $body; private $query;
	public function __construct( $m, $url = array(), $body = array(), $query = array() ) { $this->m = $m; $this->url = $url; $this->body = $body; $this->query = $query; }
	public function get_method() { return $this->m; }
	public function get_param( $k ) { foreach ( array( $this->url, $this->body, $this->query ) as $s ) { if ( array_key_exists( $k, $s ) ) { return $s[ $k ]; } } return null; }
	public function get_json_params() { return $this->body; }
	public function get_file_params() { return array(); }
	#[\ReturnTypeWillChange] public function offsetGet( $k ) { return $this->get_param( $k ); }
	public function offsetExists( $k ): bool { return null !== $this->get_param( $k ); }
	public function offsetSet( $k, $v ): void { $this->url[ $k ] = $v; }
	public function offsetUnset( $k ): void { unset( $this->url[ $k ] ); }
}
function rest_ensure_response( $x ) { return $x; }
function register_rest_route( $ns, $route, $args ) { $GLOBALS['STUB']['routes'][] = array( $ns, $route, $args ); return true; }

/** Dispatches like the REST server: returns array( status, body ). */
function stub_rest( $method, $path, $body = array(), $query = array() ) {
	foreach ( $GLOBALS['STUB']['routes'] as $r ) {
		list( $ns, $route, $args ) = $r;
		$re = '@^/' . $ns . $route . '$@';
		if ( ! preg_match( $re, $path, $m ) ) { continue; }
		$methods = is_array( $args['methods'] ) ? $args['methods'] : array_map( 'trim', explode( ',', $args['methods'] ) );
		if ( ! in_array( $method, $methods, true ) ) { continue; }
		$url = array();
		foreach ( $m as $k => $v ) { if ( is_string( $k ) ) { $url[ $k ] = $v; } }
		$req = new WP_REST_Request( $method, $url, (array) $body, (array) $query );
		$perm = isset( $args['permission_callback'] ) ? call_user_func( $args['permission_callback'], $req ) : true;
		if ( true !== $perm ) {
			return array( is_user_logged_in() ? 403 : 401, array( 'code' => 'rest_forbidden', 'message' => 'Sorry, you are not allowed to do that.', 'data' => array( 'status' => is_user_logged_in() ? 403 : 401 ) ) );
		}
		$res = call_user_func( $args['callback'], $req );
		if ( is_wp_error( $res ) ) {
			$st = (int) ( $res->data['status'] ?? 500 );
			return array( $st, array( 'code' => $res->code, 'message' => $res->message, 'data' => $res->data ) );
		}
		return array( 200, $res );
	}
	return array( 404, array( 'code' => 'rest_no_route', 'message' => 'No route', 'data' => array( 'status' => 404 ) ) );
}

/** Loads the room's build files (and the live wizard file, read only, for nadlan_ur_rate_limited), then boots init + REST. */
function stub_boot_room( $build_dir, $live_base_dir ) {
	require_once $build_dir . '/inc/urban-tools.php';
	require_once $live_base_dir . '/inc__urban-wizard.php';
	require_once $build_dir . '/inc/urban-space.php';
	do_action( 'init' );
	do_action( 'rest_api_init' );
}
