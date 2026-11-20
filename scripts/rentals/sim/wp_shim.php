<?php
/**
 * A minimal WordPress for running the REAL rentals code (inc/rentals/*.php)
 * outside WordPress: $wpdb on SQLite (PDO), options, transients, user meta,
 * hooks, sanitizers, WP_Error, WP_REST_Request. Used by the 10-year
 * simulation (sim10.php). Only what the module calls is implemented, with
 * WordPress's semantics where they matter (prepare, insert NULLs, update
 * where, rows_affected, insert_id).
 *
 * Run with: php -d extension=pdo_sqlite -d extension=sodium
 */

if ( ! defined( 'ABSPATH' ) ) { define( 'ABSPATH', __DIR__ . '/' ); }
foreach ( array( 'AUTH_KEY', 'SECURE_AUTH_KEY', 'LOGGED_IN_KEY', 'NONCE_KEY' ) as $k ) {
	if ( ! defined( $k ) ) { define( $k, getenv( 'SIM_SALT' ) ? getenv( 'SIM_SALT' ) . $k : 'sim-salt-' . $k ); }
}
define( 'MINUTE_IN_SECONDS', 60 );
define( 'HOUR_IN_SECONDS', 3600 );
define( 'DAY_IN_SECONDS', 86400 );
define( 'ARRAY_A', 'ARRAY_A' );
define( 'OBJECT', 'OBJECT' );
define( 'NLRM_DIR_ASSETS', dirname( __DIR__, 3 ) . '/plugins/nadlan-config/assets/rentals/' );
define( 'NLRM_PRIVACY_VERSION', '2026-10-01' );

class WP_Error {
	public $code; public $message; public $data;
	function __construct( $code = '', $message = '', $data = array() ) { $this->code = $code; $this->message = $message; $this->data = $data; }
	function get_error_code() { return $this->code; }
	function get_error_message() { return $this->message; }
}
function is_wp_error( $x ) { return $x instanceof WP_Error; }

class WP_REST_Request {
	private $p; private $h; private $f;
	function __construct( $params = array(), $headers = array(), $files = array() ) { $this->p = $params; $this->h = $headers; $this->f = $files; }
	function get_param( $k ) { return $this->p[ $k ] ?? null; }
	function get_header( $k ) { return $this->h[ $k ] ?? null; }
	function get_file_params() { return $this->f; }
	function offsetGet( $k ) { return $this->p[ $k ] ?? null; }
}

/* ---------- hooks ---------- */
$GLOBALS['sim_hooks'] = array();
function add_action( $tag, $fn, $prio = 10, $n = 1 ) { $GLOBALS['sim_hooks'][ $tag ][] = $fn; }
function add_filter( $tag, $fn, $prio = 10, $n = 1 ) { $GLOBALS['sim_hooks'][ $tag ][] = $fn; }
function do_action( $tag, ...$args ) { foreach ( $GLOBALS['sim_hooks'][ $tag ] ?? array() as $fn ) { $fn( ...$args ); } }
function apply_filters( $tag, $value, ...$args ) { foreach ( $GLOBALS['sim_hooks'][ $tag ] ?? array() as $fn ) { $value = $fn( $value, ...$args ); } return $value; }
$GLOBALS['sim_routes'] = array();
function register_rest_route( $ns, $path, $args ) { $GLOBALS['sim_routes'][ $path ] = $args; }
/* call a registered route the way WordPress would: permission first */
function sim_rest( $path, $params = array(), $headers = array() ) {
	$r = $GLOBALS['sim_routes'][ $path ] ?? null;
	if ( ! $r ) { return new WP_Error( 'no_route', $path ); }
	$perm = $r['permission_callback'];
	if ( is_string( $perm ) ? ! $perm() : ! $perm() ) { return new WP_Error( 'rest_forbidden', 'forbidden', array( 'status' => 401 ) ); }
	return ( $r['callback'] )( new WP_REST_Request( $params, $headers ) );
}
function __return_true() { return true; }
function wp_next_scheduled() { return true; }
function wp_schedule_event() {}

/* ---------- options, transients, users ---------- */
/* options live in the database (wp_options), as in WordPress, so a second
   process (another request, another salt) sees the same site */
$GLOBALS['sim_opt'] = null;
$GLOBALS['sim_tr'] = array();
function sim_opts() {
	global $wpdb;
	if ( null === $GLOBALS['sim_opt'] ) {
		$GLOBALS['sim_opt'] = array();
		foreach ( $wpdb->get_results( 'SELECT option_name, option_value FROM wp_options', ARRAY_A ) as $r ) { $GLOBALS['sim_opt'][ $r['option_name'] ] = unserialize( $r['option_value'] ); }
	}
	return $GLOBALS['sim_opt'];
}
function get_option( $k, $d = false ) { $o = sim_opts(); return array_key_exists( $k, $o ) ? $o[ $k ] : $d; }
function update_option( $k, $v, $autoload = null ) {
	global $wpdb;
	sim_opts();
	$GLOBALS['sim_opt'][ $k ] = $v;
	$wpdb->query( $wpdb->prepare( 'INSERT OR REPLACE INTO wp_options (option_name, option_value) VALUES (%s, %s)', $k, serialize( $v ) ) );
	return true;
}
function delete_option( $k ) { global $wpdb; sim_opts(); unset( $GLOBALS['sim_opt'][ $k ] ); $wpdb->query( $wpdb->prepare( 'DELETE FROM wp_options WHERE option_name = %s', $k ) ); return true; }
function get_transient( $k ) {
	$t = $GLOBALS['sim_tr'][ $k ] ?? null;
	if ( ! $t || $t[1] < nlrm_time() ) { return false; }
	return $t[0];
}
function set_transient( $k, $v, $ttl = 0 ) { $GLOBALS['sim_tr'][ $k ] = array( $v, nlrm_time() + ( $ttl ?: 86400 * 365 ) ); return true; }
function delete_transient( $k ) { unset( $GLOBALS['sim_tr'][ $k ] ); return true; }
$GLOBALS['sim_user'] = 0;
function get_current_user_id() { return (int) $GLOBALS['sim_user']; }
function is_user_logged_in() { return $GLOBALS['sim_user'] > 0; }
function get_userdata( $id ) { return (object) array( 'ID' => $id, 'display_name' => 'Landlord ' . $id, 'user_email' => 'owner' . (int) $id . '@example.com' ); }
$GLOBALS['sim_mail'] = array();
if ( ! function_exists( 'wp_mail' ) ) { function wp_mail( $to, $subject, $body ) { $GLOBALS['sim_mail'][] = array( 'to' => $to, 'subject' => $subject, 'body' => $body ); return true; } }
function get_user_meta( $uid, $k, $single = false ) {
	global $wpdb;
	$v = $wpdb->get_var( $wpdb->prepare( 'SELECT meta_value FROM ' . $wpdb->usermeta . ' WHERE user_id = %d AND meta_key = %s ORDER BY umeta_id DESC LIMIT 1', $uid, $k ) );
	if ( null === $v ) { return $single ? '' : array(); }
	$u = @unserialize( $v );
	return false === $u && 'b:0;' !== $v ? $v : $u;
}
function update_user_meta( $uid, $k, $v ) {
	global $wpdb;
	$sv = is_array( $v ) || is_object( $v ) ? serialize( $v ) : (string) $v;
	$id = $wpdb->get_var( $wpdb->prepare( 'SELECT umeta_id FROM ' . $wpdb->usermeta . ' WHERE user_id = %d AND meta_key = %s', $uid, $k ) );
	if ( $id ) { $wpdb->update( $wpdb->usermeta, array( 'meta_value' => $sv ), array( 'umeta_id' => (int) $id ) ); }
	else { $wpdb->insert( $wpdb->usermeta, array( 'user_id' => $uid, 'meta_key' => $k, 'meta_value' => $sv ) ); }
	return true;
}

/* ---------- formatting and sanitizing ---------- */
function wp_json_encode( $v, $flags = 0 ) { return json_encode( $v, $flags | JSON_PARTIAL_OUTPUT_ON_ERROR ); }
function wp_unslash( $v ) { return $v; }
function sanitize_text_field( $s ) { $s = strip_tags( (string) $s ); $s = preg_replace( '/[\r\n\t ]+/', ' ', $s ); return trim( $s ); }
function sanitize_textarea_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function sanitize_email( $s ) { $s = trim( (string) $s ); return filter_var( $s, FILTER_VALIDATE_EMAIL ) ? $s : ''; }
function sanitize_key( $s ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $s ) ); }
function sanitize_file_name( $s ) { return preg_replace( '/[^\p{L}\p{N}._ -]/u', '', (string) $s ); }
function wp_strip_all_tags( $s ) { return trim( strip_tags( (string) $s ) ); }
function esc_url_raw( $s ) { return filter_var( (string) $s, FILTER_VALIDATE_URL ) ? (string) $s : ''; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function trailingslashit( $s ) { return rtrim( $s, '/\\' ) . '/'; }
function wp_mkdir_p( $d ) { return is_dir( $d ) || mkdir( $d, 0777, true ); }
function wp_upload_dir( $a = null, $b = true ) { return array( 'basedir' => $GLOBALS['sim_upload_dir'] ); }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function wp_salt( $s = 'auth' ) { return 'sim-salt-' . $s; }
function current_time( $type, $gmt = 0 ) { return gmdate( 'Y-m-d H:i:s', nlrm_time() ); }
function wp_generate_password( $n = 12, $sc = true, $esc = false ) { return substr( bin2hex( random_bytes( $n ) ), 0, $n ); }
function number_format_i18n( $n, $d = 0 ) { return number_format( $n, $d ); }

/* ---------- $wpdb on SQLite ---------- */
class SimWPDB {
	public $prefix = 'wp_';
	public $usermeta = 'wp_usermeta';
	public $insert_id = 0;
	public $rows_affected = 0;
	public $last_error = '';
	public $queries = 0;
	public $pdo;
	function __construct( $file ) {
		$this->pdo = new PDO( 'sqlite:' . $file );
		$this->pdo->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_SILENT );
		$this->pdo->exec( 'PRAGMA journal_mode = WAL; PRAGMA synchronous = OFF;' );
		$this->pdo->exec( 'CREATE TABLE IF NOT EXISTS wp_usermeta (umeta_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, meta_key TEXT, meta_value TEXT)' );
		$this->pdo->exec( 'CREATE TABLE IF NOT EXISTS wp_options (option_name TEXT PRIMARY KEY, option_value TEXT)' );
	}
	function get_charset_collate() { return ''; }
	/* WordPress's prepare: %d %s %f, args as varargs or one array */
	function prepare( $query, ...$args ) {
		if ( 1 === count( $args ) && is_array( $args[0] ) ) { $args = $args[0]; }
		$i = 0;
		$self = $this;
		return preg_replace_callback( '/%(%|d|s|f)/', function ( $m ) use ( &$i, $args, $self ) {
			if ( '%' === $m[1] ) { return '%'; }
			$v = $args[ $i++ ] ?? null;
			if ( 'd' === $m[1] ) { return (string) (int) $v; }
			if ( 'f' === $m[1] ) { return (string) (float) $v; }
			return $self->pdo->quote( (string) $v );
		}, $query );
	}
	private function sql( $q ) {
		$q = preg_replace( '/^\s*INSERT IGNORE INTO/i', 'INSERT OR IGNORE INTO', $q );
		$q = preg_replace( '/CAST\(([^)]*) AS UNSIGNED\)/i', 'CAST($1 AS INTEGER)', $q );
		return $q;
	}
	/* WordPress: query() answers a number (rows), never a statement */
	function query( $q ) {
		$st = $this->run( $q );
		return $st ? $this->rows_affected : false;
	}
	private function run( $q ) {
		$this->queries++;
		$q = $this->sql( $q );
		$this->last_error = '';
		$st = $this->pdo->prepare( $q );
		if ( ! $st ) { $this->last_error = implode( ' ', $this->pdo->errorInfo() ); fwrite( STDERR, "SQL ERROR: {$this->last_error}\n$q\n" ); return false; }
		if ( ! $st->execute() ) { $this->last_error = implode( ' ', $st->errorInfo() ); $this->rows_affected = 0; return false; }
		$this->rows_affected = $st->rowCount();
		if ( preg_match( '/^\s*INSERT/i', $q ) ) { $this->insert_id = $this->rows_affected ? (int) $this->pdo->lastInsertId() : 0; }
		return $st;
	}
	function get_results( $q, $out = OBJECT ) {
		$st = $this->run( $q );
		if ( ! $st ) { return array(); }
		$rows = $st->fetchAll( PDO::FETCH_ASSOC );
		return ARRAY_A === $out ? $rows : array_map( function ( $r ) { return (object) $r; }, $rows );
	}
	function get_row( $q, $out = OBJECT ) { $r = $this->get_results( $q, $out ); return $r ? $r[0] : null; }
	function get_var( $q ) { $st = $this->run( $q ); if ( ! $st ) { return null; } $v = $st->fetchColumn(); return false === $v ? null : $v; }
	function get_col( $q ) { $st = $this->run( $q ); return $st ? $st->fetchAll( PDO::FETCH_COLUMN, 0 ) : array(); }
	function insert( $t, $row ) {
		$cols = array_keys( $row );
		$vals = array_map( function ( $v ) { return null === $v ? 'NULL' : $this->pdo->quote( (string) $v ); }, array_values( $row ) );
		return $this->query( 'INSERT INTO ' . $t . ' (`' . implode( '`,`', $cols ) . '`) VALUES (' . implode( ',', $vals ) . ')' );
	}
	function update( $t, $data, $where ) {
		$set = array(); $w = array();
		foreach ( $data as $k => $v ) { $set[] = '`' . $k . '` = ' . ( null === $v ? 'NULL' : $this->pdo->quote( (string) $v ) ); }
		foreach ( $where as $k => $v ) { $w[] = '`' . $k . '` = ' . $this->pdo->quote( (string) $v ); }
		return $this->query( 'UPDATE ' . $t . ' SET ' . implode( ', ', $set ) . ' WHERE ' . implode( ' AND ', $w ) );
	}
	function delete( $t, $where ) {
		$w = array();
		foreach ( $where as $k => $v ) { $w[] = '`' . $k . '` = ' . $this->pdo->quote( (string) $v ); }
		return $this->query( 'DELETE FROM ' . $t . ' WHERE ' . implode( ' AND ', $w ) );
	}
}

/* dbDelta: MySQL CREATE TABLE -> SQLite table + indexes (unique keys kept) */
function dbDelta( $sql ) {
	global $wpdb;
	if ( ! preg_match( '/CREATE TABLE (\S+) \((.*)\)/s', $sql, $m ) ) { return; }
	$t = $m[1];
	$cols = array(); $idx = array();
	foreach ( preg_split( '/,\s*\r?\n/', trim( $m[2] ) ) as $line ) {
		$line = trim( $line );
		if ( preg_match( '/^PRIMARY KEY/', $line ) ) { continue; }
		if ( preg_match( '/^UNIQUE KEY (\w+) \(([^)]+)\)/', $line, $k ) ) { $idx[] = 'CREATE UNIQUE INDEX IF NOT EXISTS ' . $t . '_' . $k[1] . ' ON ' . $t . ' (' . $k[2] . ')'; continue; }
		if ( preg_match( '/^KEY (\w+) \(([^)]+)\)/', $line, $k ) ) { $idx[] = 'CREATE INDEX IF NOT EXISTS ' . $t . '_' . $k[1] . ' ON ' . $t . ' (' . $k[2] . ')'; continue; }
		if ( preg_match( '/^(\w+) bigint\(20\) unsigned NOT NULL AUTO_INCREMENT/', $line, $k ) ) { $cols[] = $k[1] . ' INTEGER PRIMARY KEY AUTOINCREMENT'; continue; }
		if ( ! preg_match( '/^(\w+) (\w+)/', $line, $k ) ) { continue; }
		$type = strtolower( $k[2] );
		$aff = in_array( $type, array( 'bigint', 'int', 'smallint', 'tinyint' ), true ) ? 'INTEGER' : ( 'decimal' === $type ? 'REAL' : 'TEXT' );
		$def = '';
		if ( preg_match( "/DEFAULT ('[^']*'|[\-0-9.]+|NULL)/", $line, $d ) ) { $def = ' DEFAULT ' . $d[1]; }
		$nn = false !== strpos( $line, 'NOT NULL' ) ? ' NOT NULL' : '';
		$cols[] = $k[1] . ' ' . $aff . $nn . $def;
	}
	$wpdb->query( 'CREATE TABLE IF NOT EXISTS ' . $t . ' (' . implode( ', ', $cols ) . ')' );
	foreach ( $idx as $q ) { $wpdb->query( $q ); }
}

function nadlan_rm_on() { return true; }
function current_user_can( $cap ) { return ! empty( $GLOBALS['sim_admin'] ); }
function delete_user_meta( $uid, $k ) { global $wpdb; $wpdb->query( $wpdb->prepare( 'DELETE FROM ' . $wpdb->usermeta . ' WHERE user_id = %d AND meta_key = %s', $uid, $k ) ); return true; }
function get_posts( $a = array() ) { return array(); }
function get_post_meta( $id, $k = '', $s = false ) { return ''; }
function get_post_field( $f, $id ) { return ''; }

/* load the real module */
function sim_boot( $dbfile, $upload_dir ) {
	$GLOBALS['wpdb'] = new SimWPDB( $dbfile );
	$GLOBALS['sim_upload_dir'] = $upload_dir;
	if ( ! is_dir( $upload_dir ) ) { mkdir( $upload_dir, 0777, true ); }
	$base = dirname( __DIR__, 3 ) . '/plugins/nadlan-config/inc/rentals/';
	foreach ( array( 'store', 'money', 'billing', 'rest', 'portal', 'lease', 'legacy', 'page' ) as $f ) { require_once $base . $f . '.php'; }
	do_action( 'rest_api_init' );
}
