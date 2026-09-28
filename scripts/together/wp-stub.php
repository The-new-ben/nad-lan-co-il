<?php
/**
 * A minimal WordPress stand-in for testing inc/together.php outside WordPress (TogetherRoom, 28.9.2026).
 * Used by router.php (php -S, the browser harness) and php_selftest.php (the CLI checks). Never loaded by the site.
 * The store (options, transients, posts, post meta, cron) is one JSON file: NLTR_STORE, else the temp folder.
 */
if ( ! defined( 'ABSPATH' ) ) { define( 'ABSPATH', __DIR__ . '/' ); }
define( 'MINUTE_IN_SECONDS', 60 );
define( 'HOUR_IN_SECONDS', 3600 );
define( 'DAY_IN_SECONDS', 86400 );
define( 'NADLAN_CONFIG_VERSION', 'harness' );
define( 'OBJECT', 'OBJECT' );
define( 'NLTR_PLUGIN', dirname( __DIR__, 2 ) . '/plugins/nadlan-config' );
define( 'NLTR_SITE', 'https://nad-lan.co.il' );

$GLOBALS['__nltr_store_file'] = getenv( 'NLTR_STORE' ) ?: sys_get_temp_dir() . '/nltr-store.json';
$GLOBALS['__nltr_hooks']      = array();
$GLOBALS['__nltr_routes']     = array();
$GLOBALS['__nltr_user']       = 0; // 0 = a visitor; 7 = a representative (edit_posts, manage_options)
$GLOBALS['__nltr_now']        = null;

function __nltr_empty() {
	return array( 'options' => array(), 'transients' => array(), 'posts' => array(
		101 => array( 'ID' => 101, 'post_type' => 'nadlan_project', 'post_name' => 'rainbow-tel-aviv', 'post_title' => 'ריינבו תל אביב', 'post_status' => 'publish', 'post_date_gmt' => '2026-01-01 00:00:00' ),
	), 'meta' => array(), 'next' => 1000, 'cron' => array() );
}
function __nltr_load() {
	$f = $GLOBALS['__nltr_store_file'];
	$d = is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : null;
	$GLOBALS['__nltr'] = is_array( $d ) ? $d : __nltr_empty();
}
function __nltr_save() { file_put_contents( $GLOBALS['__nltr_store_file'], json_encode( $GLOBALS['__nltr'], JSON_UNESCAPED_UNICODE ), LOCK_EX ); }
function __nltr_reset() { $GLOBALS['__nltr'] = __nltr_empty(); __nltr_save(); }
function __nltr_time() { return null !== $GLOBALS['__nltr_now'] ? (int) $GLOBALS['__nltr_now'] : time(); }
__nltr_load();

/* hooks */
function add_action( $h, $cb, $p = 10, $n = 1 ) {
	$bt = debug_backtrace( DEBUG_BACKTRACE_IGNORE_ARGS, 2 );
	$file = basename( (string) ( $bt[0]['file'] ?? '' ) );
	if ( 'wp-stub.php' === $file && isset( $bt[1]['file'] ) ) { $file = basename( (string) $bt[1]['file'] ); } // add_filter
	$GLOBALS['__nltr_hooks'][ $h ][ $p ][] = array( $cb, $file );
	return true;
}
function add_filter( $h, $cb, $p = 10, $n = 1 ) { return add_action( $h, $cb, $p, $n ); }
function do_action( $h, ...$a ) { __nltr_run( $h, null, $a ); }
/** Run a hook's callbacks, only those registered by $file when given (e.g. 'together.php'). */
function __nltr_run( $h, $file = null, $a = array() ) {
	if ( empty( $GLOBALS['__nltr_hooks'][ $h ] ) ) { return; }
	ksort( $GLOBALS['__nltr_hooks'][ $h ] );
	foreach ( $GLOBALS['__nltr_hooks'][ $h ] as $cbs ) {
		foreach ( $cbs as $c ) { if ( null === $file || $c[1] === $file ) { call_user_func_array( $c[0], $a ); } }
	}
}
function register_post_type( $t, $a ) { return true; }
function add_options_page( $t = '', $m = '', $cap = '', $slug = '', $cb = null ) { $GLOBALS['__nltr_pages'][ $slug ] = $cb; return true; }
function add_meta_box() { return true; }
function wp_next_scheduled( $h ) { return $GLOBALS['__nltr']['cron'][ $h ] ?? false; }
function wp_schedule_event( $t, $r, $h ) { $GLOBALS['__nltr']['cron'][ $h ] = $t; __nltr_save(); return true; }

/* options and transients */
function get_option( $k, $d = false ) { return array_key_exists( $k, $GLOBALS['__nltr']['options'] ) ? $GLOBALS['__nltr']['options'][ $k ]['v'] : $d; }
function update_option( $k, $v, $autoload = null ) { $GLOBALS['__nltr']['options'][ $k ] = array( 'v' => $v, 'autoload' => false === $autoload ? 'off' : 'on' ); __nltr_save(); return true; }
function delete_option( $k ) { unset( $GLOBALS['__nltr']['options'][ $k ] ); __nltr_save(); return true; }
function get_transient( $k ) {
	$t = $GLOBALS['__nltr']['transients'][ $k ] ?? null;
	if ( ! $t ) { return false; }
	if ( $t['exp'] && $t['exp'] < __nltr_time() ) { unset( $GLOBALS['__nltr']['transients'][ $k ] ); return false; }
	return $t['v'];
}
function set_transient( $k, $v, $exp = 0 ) { $GLOBALS['__nltr']['transients'][ $k ] = array( 'v' => $v, 'exp' => $exp ? __nltr_time() + (int) $exp : 0 ); __nltr_save(); return true; }
function delete_transient( $k ) { unset( $GLOBALS['__nltr']['transients'][ $k ] ); __nltr_save(); return true; }

/* posts and meta */
function __nltr_post( $id ) { return $GLOBALS['__nltr']['posts'][ (int) $id ] ?? null; }
function get_posts( $q ) {
	$out = array();
	foreach ( $GLOBALS['__nltr']['posts'] as $p ) {
		if ( ! empty( $q['post_type'] ) && $p['post_type'] !== $q['post_type'] ) { continue; }
		if ( isset( $q['name'] ) && $p['post_name'] !== $q['name'] ) { continue; }
		if ( ! empty( $q['date_query'][0]['before'] ) && strcmp( $p['post_date_gmt'], $q['date_query'][0]['before'] ) >= 0 ) { continue; }
		$out[] = $p;
	}
	usort( $out, function ( $a, $b ) { return strcmp( $b['post_date_gmt'], $a['post_date_gmt'] ); } );
	$n = (int) ( $q['numberposts'] ?? 5 );
	if ( $n > 0 ) { $out = array_slice( $out, 0, $n ); }
	if ( ( $q['fields'] ?? '' ) === 'ids' ) { return array_map( function ( $p ) { return $p['ID']; }, $out ); }
	return array_map( function ( $p ) { return (object) $p; }, $out );
}
function wp_insert_post( $a, $err = false ) {
	$id = ++$GLOBALS['__nltr']['next'];
	$GLOBALS['__nltr']['posts'][ $id ] = array( 'ID' => $id, 'post_type' => $a['post_type'], 'post_name' => $a['post_name'], 'post_title' => $a['post_title'], 'post_status' => $a['post_status'], 'post_date_gmt' => gmdate( 'Y-m-d H:i:s', __nltr_time() ) );
	__nltr_save();
	return $id;
}
function wp_delete_post( $id, $force = false ) { unset( $GLOBALS['__nltr']['posts'][ (int) $id ], $GLOBALS['__nltr']['meta'][ (int) $id ] ); __nltr_save(); return true; }
function get_post_field( $f, $id ) { $p = __nltr_post( $id ); return $p ? ( $p[ $f ] ?? '' ) : ''; }
function get_post_type( $id ) { $p = __nltr_post( $id ); return $p ? $p['post_type'] : false; }
function get_post_status( $id ) { $p = __nltr_post( $id ); return $p ? $p['post_status'] : false; }
function post_password_required( $id ) { return false; }
function get_the_title( $id ) { return get_post_field( 'post_title', $id ); }
function get_permalink( $id ) { $p = __nltr_post( is_object( $id ) ? $id->ID : $id ); return $p && 'nadlan_project' === $p['post_type'] ? NLTR_SITE . '/projects/' . $p['post_name'] . '/' : false; }
function get_page_by_path( $slug, $o = null, $type = 'page' ) { foreach ( $GLOBALS['__nltr']['posts'] as $p ) { if ( $p['post_name'] === $slug && $p['post_type'] === $type ) { return (object) $p; } } return null; }
function get_date_from_gmt( $d, $f ) { return date( $f, strtotime( $d . ' UTC' ) ); }
function get_post_meta( $id, $k = '', $single = false ) {
	$rows = $GLOBALS['__nltr']['meta'][ (int) $id ][ $k ] ?? array();
	return $single ? ( $rows ? $rows[0] : '' ) : $rows;
}
function update_post_meta( $id, $k, $v ) { $GLOBALS['__nltr']['meta'][ (int) $id ][ $k ] = array( $v ); __nltr_save(); return true; }
function add_post_meta( $id, $k, $v ) { $GLOBALS['__nltr']['meta'][ (int) $id ][ $k ][] = $v; __nltr_save(); return true; }
function delete_post_meta( $id, $k, $v = '' ) {
	$rows = $GLOBALS['__nltr']['meta'][ (int) $id ][ $k ] ?? array();
	$GLOBALS['__nltr']['meta'][ (int) $id ][ $k ] = array_values( array_filter( $rows, function ( $r ) use ( $v ) { return '' !== $v && json_encode( $r ) !== json_encode( $v ); } ) );
	__nltr_save();
	return true;
}

/* users */
function current_user_can( $cap ) { return 7 === $GLOBALS['__nltr_user']; }
function is_user_logged_in() { return $GLOBALS['__nltr_user'] > 0; }
function wp_get_current_user() { return (object) array( 'ID' => $GLOBALS['__nltr_user'], 'display_name' => 'דנה' ); }
function wp_create_nonce( $a ) { return 'rep-nonce'; }
function check_admin_referer( $a ) { return true; }
function wp_nonce_field( $a ) { echo '<input type="hidden" name="_wpnonce" value="x">'; }
function wp_salt( $s ) { return 'harness-salt-' . $s; }

/* text */
function wp_unslash( $v ) { return is_string( $v ) ? stripslashes( $v ) : $v; }
function sanitize_key( $k ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $k ) ); }
function sanitize_text_field( $s ) { $s = strip_tags( (string) $s ); $s = preg_replace( '/[\r\n\t ]+/', ' ', $s ); return trim( $s ); }
function sanitize_textarea_field( $s ) { $s = strip_tags( (string) $s ); return trim( preg_replace( '/[ \t]+/', ' ', $s ) ); }
function esc_url_raw( $u, $protocols = null ) {
	$u = trim( (string) $u );
	$ok = $protocols ?: array( 'http', 'https' );
	$scheme = strtolower( (string) parse_url( $u, PHP_URL_SCHEME ) );
	return in_array( $scheme, $ok, true ) ? $u : '';
}
function esc_url( $u ) { return htmlspecialchars( (string) $u, ENT_QUOTES ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function checked( $a, $b = true, $echo = true ) { $r = $a === $b ? ' checked="checked"' : ''; if ( $echo ) { echo $r; } return $r; }
function wp_json_encode( $v, $f = 0 ) { return json_encode( $v, $f ); }
function is_admin() { return false; }
function rest_url( $p = '' ) { return NLTR_SITE . '/wp-json/' . ltrim( $p, '/' ); }
function plugins_url( $p, $file ) { return NLTR_SITE . '/wp-content/plugins/nadlan-config/' . ltrim( $p, '/' ); }
function add_query_arg( $k, $v = null, $url = null ) {
	if ( is_array( $k ) ) { $url = $v; $args = $k; } else { $args = array( $k => $v ); }
	$parts = explode( '?', (string) $url, 2 );
	parse_str( $parts[1] ?? '', $q );
	return $parts[0] . '?' . http_build_query( array_merge( $q, $args ) );
}

/* REST */
class WP_Error { public $code; public $msg; public $data; public function __construct( $c = '', $m = '', $d = array() ) { $this->code = $c; $this->msg = $m; $this->data = $d; } }
function is_wp_error( $x ) { return $x instanceof WP_Error; }
class WP_REST_Response { public $data; public $status; public $headers = array(); public function __construct( $d = null, $s = 200 ) { $this->data = $d; $this->status = $s; } public function header( $k, $v ) { $this->headers[ $k ] = $v; } }
class WP_REST_Request {
	public $method; public $query; public $body;
	public function __construct( $method, $query = array(), $body = array() ) { $this->method = $method; $this->query = $query; $this->body = $body; }
	public function get_json_params() { return $this->body; }
	public function get_param( $k ) { return $this->query[ $k ] ?? ( $this->body[ $k ] ?? null ); }
}
function register_rest_route( $ns, $route, $args ) {
	$list = isset( $args['methods'] ) ? array( $args ) : $args;
	foreach ( $list as $a ) {
		foreach ( (array) explode( ',', $a['methods'] ) as $m ) { $GLOBALS['__nltr_routes'][ trim( $m ) . ' ' . $ns . $route ] = $a['callback']; }
	}
}
/** Call a registered route: back [status, data]. */
function __nltr_call( $method, $path, $query = array(), $body = array() ) {
	$cb = $GLOBALS['__nltr_routes'][ $method . ' ' . $path ] ?? null;
	if ( ! $cb ) { return array( 404, array( 'code' => 'rest_no_route' ) ); }
	$r = $cb( new WP_REST_Request( $method, $query, $body ) );
	if ( $r instanceof WP_Error ) { return array( $r->data['status'] ?? 400, array( 'code' => $r->code ) ); }
	return array( $r->status, $r->data );
}

/* the site's own helpers the module leans on */
function nadlan_ps_current() { $all = nadlan_ps_config(); return array_merge( $all['rainbow-tel-aviv'], array( 'id' => 101, 'slug' => 'rainbow-tel-aviv' ) ); }
function nadlan_cta_whatsapp_number() { return '972525101555'; }
function nadlan_current_lang() { return 'he'; }
// the real stage config (units, sectors) from inc/project-stage.php; a copy of its Rainbow keys if that file cannot load
try {
	require_once NLTR_PLUGIN . '/inc/project-stage.php';
} catch ( \Throwable $e ) {
	function nadlan_ps_config() {
		return array( 'rainbow-tel-aviv' => array( 'dir' => 'rainbow', 'mount' => 'mountRainbowStage', 'name' => 'ריינבו תל אביב',
			'units' => array( array( 'n', 0 ), array( 'e', 90 ), array( 's', 180 ), array( 'w', 270 ) ),
			'sectors' => array( array( 230, 345, 'לכיוון הים' ), array( 345, 30, 'לכיוון תל ברוך והרצליה' ), array( 30, 105, 'לכיוון רמת אביב והאוניברסיטה' ), array( 105, 150, 'לכיוון פארק הירקון' ), array( 150, 195, 'לכיוון מגדלי העיר' ), array( 195, 230, 'לכיוון הצפון הישן' ) ) ) );
	}
}
require_once NLTR_PLUGIN . '/inc/together.php';
do_action( 'init' );
do_action( 'rest_api_init' );
