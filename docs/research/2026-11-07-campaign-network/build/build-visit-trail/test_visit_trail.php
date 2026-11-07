<?php
/**
 * visit trail build (7.11.2026, HAD-678) · PHP test of plugins/nadlan-config/inc/visit-trail.php on WordPress stubs and a fake $wpdb that
 * records every query: the batch check (frame, allow list per event, cut texts, bearings, floors, the event clock), the REST answers
 * (400 empty, 413 too big, 403 another site, 204 for GPC / DNT / robots / the owner switch off, 429 after 30 a minute, 400 not a project),
 * what reaches the database (two tables, the country, never the IP), the cap per visit, the lead link (meta + upsert, not under GPC, a
 * failure never stops the lead), the timeline in plain Hebrew, the new-lead email block, the admin screen (escaped), the 12-month clean-up.
 * Run:  php docs/research/2026-11-07-campaign-network/build/build-visit-trail/test_visit_trail.php      (exit 1 on any failure)
 */
error_reporting( E_ALL );
define( 'ABSPATH', __DIR__ . '/' );
define( 'MINUTE_IN_SECONDS', 60 ); define( 'HOUR_IN_SECONDS', 3600 ); define( 'DAY_IN_SECONDS', 86400 );
define( 'ARRAY_A', 'ARRAY_A' );
$GLOBALS['T_HOOKS'] = array(); $GLOBALS['T_OPT'] = array(); $GLOBALS['T_TR'] = array(); $GLOBALS['T_META'] = array(); $GLOBALS['T_TYPES'] = array();
function add_action( $h, $cb, $p = 10, $n = 1 ) { $GLOBALS['T_HOOKS'][ $h ][] = array( $cb, $p, $n ); return true; }
function add_filter( $h, $cb, $p = 10, $n = 1 ) { return add_action( $h, $cb, $p, $n ); }
function has_action( $h, $cb = false ) { foreach ( $GLOBALS['T_HOOKS'][ $h ] ?? array() as $x ) { if ( $x[0] === $cb ) { return $x[1]; } } return false; }
function run_hook( $h, ...$args ) { $l = $GLOBALS['T_HOOKS'][ $h ] ?? array(); usort( $l, function ( $a, $b ) { return $a[1] <=> $b[1]; } ); foreach ( $l as $x ) { $r = call_user_func_array( $x[0], array_slice( $args, 0, $x[2] ) ); if ( $r !== null ) { $args[0] = $r; } } return $args[0] ?? null; }
function apply_filters( $h, $v ) { return $v; }
function get_option( $k, $d = false ) { return array_key_exists( $k, $GLOBALS['T_OPT'] ) ? $GLOBALS['T_OPT'][ $k ] : $d; }
function update_option( $k, $v, $a = null ) { $GLOBALS['T_OPT'][ $k ] = $v; return true; }
function get_transient( $k ) { return $GLOBALS['T_TR'][ $k ] ?? false; }
function set_transient( $k, $v, $e ) { $GLOBALS['T_TR'][ $k ] = $v; return true; }
function wp_strip_all_tags( $s ) { return trim( strip_tags( (string) $s ) ); }
function sanitize_key( $k ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $k ) ); }
function sanitize_text_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function wp_json_encode( $v, $f = 0 ) { return json_encode( $v, $f ); }
function wp_unslash( $v ) { return is_string( $v ) ? stripslashes( $v ) : $v; }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function admin_url( $p = '' ) { return 'https://nad-lan.co.il/wp-admin/' . $p; }
function rest_url( $p = '' ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function add_query_arg( $args, $url ) { return $url . ( strpos( $url, '?' ) === false ? '?' : '&' ) . http_build_query( $args ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return esc_html( $s ); }
function esc_url( $s ) { return esc_html( $s ); }
function esc_url_raw( $s ) { return (string) $s; }
function number_format_i18n( $n ) { return number_format( (float) $n ); }
function checked( $a, $b, $e = true ) { return $a == $b ? ' checked' : ''; }
function selected( $a, $b, $e = true ) { return $a == $b ? ' selected' : ''; }
function wp_list_pluck( $l, $f ) { return array_map( function ( $x ) use ( $f ) { return is_object( $x ) ? $x->$f : $x[ $f ]; }, $l ); }
function wp_date( $f, $ts = null ) { return gmdate( $f, ( $ts ?? time() ) + 2 * 3600 ); }
function get_the_title( $id ) { return array( 7001 => 'ריינבו תל אביב', 7002 => 'Rainbow Tel Aviv', 900 => 'דנה כהן - general' )[ $id ] ?? ''; }
function get_post_type( $id ) { return $GLOBALS['T_TYPES'][ (int) $id ] ?? false; }
function get_post( $id ) { return isset( $GLOBALS['T_TYPES'][ (int) $id ] ) ? (object) array( 'ID' => (int) $id, 'post_type' => $GLOBALS['T_TYPES'][ (int) $id ] ) : null; }
function get_edit_post_link( $id, $c = 'display' ) { return 'https://nad-lan.co.il/wp-admin/post.php?post=' . (int) $id . '&action=edit'; }
function update_post_meta( $id, $k, $v ) { $GLOBALS['T_META'][ (int) $id ][ $k ] = $v; return true; }
function get_post_meta( $id, $k, $s = false ) { return $GLOBALS['T_META'][ (int) $id ][ $k ] ?? ''; }
function delete_metadata( $t, $id, $k, $v, $all ) { foreach ( $GLOBALS['T_META'] as $pid => $m ) { if ( ( $m[ $k ] ?? null ) === $v ) { unset( $GLOBALS['T_META'][ $pid ][ $k ] ); } } return true; }
function wp_nonce_field( $a, $n, $r, $e ) { return '<input type="hidden" name="' . $n . '" value="nonce">'; }
function current_user_can( $c ) { return true; }
function is_wp_error( $x ) { return $x instanceof WP_Error; }
class WP_Error { public $c; public $m; public $d; function __construct( $c = '', $m = '', $d = array() ) { $this->c = $c; $this->m = $m; $this->d = $d; } function get_error_code() { return $this->c; } function get_error_data() { return $this->d; } }
class WP_REST_Response { public $data; public $status; function __construct( $d = null, $s = 200 ) { $this->data = $d; $this->status = $s; } }
class T_Req {
	public $body; public $h; public $route; public $params;
	function __construct( $body, $h = array(), $route = '/nadlan/v1/trail', $params = array() ) { $this->body = $body; $this->h = $h; $this->route = $route; $this->params = $params; }
	function get_body() { return $this->body; }
	function get_header( $k ) { $k = strtolower( str_replace( '-', '_', $k ) ); return $this->h[ $k ] ?? null; }
	function get_method() { return 'POST'; }
	function get_route() { return $this->route; }
	function get_param( $k ) { return $this->params[ $k ] ?? null; }
}
class T_DB {
	public $prefix = 'wp_'; public $q = array(); public $var = null; public $results = array(); public $row = array(); public $col = array();
	function get_charset_collate() { return 'DEFAULT CHARSET=utf8mb4'; }
	function esc_like( $s ) { return addcslashes( $s, '_%\\' ); }
	function prepare( $sql, ...$args ) {
		if ( count( $args ) === 1 && is_array( $args[0] ) ) { $args = $args[0]; }
		$i = 0;
		return preg_replace_callback( '/%[sd]/', function ( $m ) use ( &$i, $args ) { $v = $args[ $i++ ] ?? ''; return '%d' === $m[0] ? (string) (int) $v : "'" . addslashes( (string) $v ) . "'"; }, $sql );
	}
	function query( $sql ) { $this->q[] = $sql; return 1; }
	function get_var( $sql ) { $this->q[] = $sql; if ( stripos( $sql, 'SHOW TABLES LIKE' ) !== false ) { return preg_match( "/'([^']+)'/", $sql, $m ) ? str_replace( array( '\_', '\%' ), array( '_', '%' ), stripslashes( $m[1] ) ) : null; } /* MySQL reads the LIKE escapes */ return is_callable( $this->var ) ? call_user_func( $this->var, $sql ) : $this->var; }
	function get_results( $sql ) { $this->q[] = $sql; return is_callable( $this->results ) ? call_user_func( $this->results, $sql ) : $this->results; }
	function get_row( $sql, $o = null ) { $this->q[] = $sql; return $this->row; }
	function get_col( $sql ) { $this->q[] = $sql; return $this->col; }
	function delete( $t, $w, $f ) { $this->q[] = 'DELETE FROM ' . $t . ' WHERE ' . json_encode( $w ); return 1; }
}
$GLOBALS['wpdb'] = new T_DB();
$GLOBALS['T_OPT']['nadlan_vt_db'] = '1';
$GLOBALS['T_TYPES'] = array( 7001 => 'nadlan_project', 7002 => 'nadlan_project', 55 => 'page', 900 => 'nadlan_lead' );

$FILE = dirname( __DIR__, 5 ) . '/plugins/nadlan-config/inc/visit-trail.php';
require $FILE;
$SRC = file_get_contents( $FILE );

$fails = 0; $n = 0;
function ok( $c, $name, $got = null ) { global $fails, $n; $n++; if ( ! $c ) { $fails++; } echo ( $c ? '  ok   ' : '  FAIL ' ) . $name . ( null !== $got ? '  [' . ( is_string( $got ) ? $got : json_encode( $got, JSON_UNESCAPED_UNICODE ) ) . ']' : '' ) . "\n"; }
function frame( $ev, $x = array() ) { return array_merge( array( 'v' => 1, 'vid' => 'AbCdEfGhIjKlMnOpQrStUv', 'pv' => 'pv0000000001', 'seq' => 0, 'page' => 7001, 'path' => '/projects/rainbow-tel-aviv/', 'lang' => 'he', 'dev' => 'm', 'ref' => 'google.co.il', 'now' => 1762500000000, 'ev' => $ev ), $x ); }
$NOW = 1762500000;

echo "1. the batch check\n";
$b = nadlan_vt_clean_batch( frame( array( array( 't' => 'open', 'at' => 1762500000000 ) ) ), $NOW );
ok( ! is_wp_error( $b ) && 1 === count( $b['ev'] ) && 'AbCdEfGhIjKlMnOpQrStUv' === $b['vid'] && 'google.co.il' === $b['ref'], 'a good frame passes' );
foreach ( array( 'vid' => array( 'vid' => 'short' ), 'pv' => array( 'pv' => 'a b' ), 'page' => array( 'page' => 0 ), 'v' => array( 'v' => 2 ) ) as $why => $bad ) {
	$e = nadlan_vt_clean_batch( frame( array(), $bad ), $NOW );
	ok( is_wp_error( $e ) && 'nlvt_bad' === $e->get_error_code() && $why === $e->get_error_data()['why'], "a bad $why is refused (400 nlvt_bad)" );
}
$e = nadlan_vt_clean_batch( frame( array_fill( 0, 61, array( 't' => 'open' ) ) ), $NOW );
ok( is_wp_error( $e ) && 'ev' === $e->get_error_data()['why'], '61 events in one batch are refused' );
ok( is_wp_error( nadlan_vt_clean_batch( 'x', $NOW ) ) && is_wp_error( nadlan_vt_clean_batch( frame( 'x' ), $NOW ) ), 'a body or an event list that is not an array is refused' );
$b = nadlan_vt_clean_batch( frame( array(
	array( 't' => 'floor', 'f' => 23, 'tw' => 'A', 'src' => 'user', 'heightM' => 74.2, 'name' => 'דנה', 'phone' => '0501234567' ),
	array( 't' => 'facing', 'f' => '23', 'b' => -90, 'u' => '23-w', 'lbl' => str_repeat( 'א', 90 ) ),
	array( 't' => 'facing', 'f' => 999, 'b' => 725.6 ),
	array( 't' => 'view', 'b' => 'abc' ),
	array( 't' => 'drop table' ), array( 't' => array( 'x' ) ), 'not an event',
	array( 't' => 'click', 'l' => 'no kind' ),
	array( 't' => 'click', 'k' => 'WA<script>', 'l' => '<b>ייעוץ</b> חינם', 'w' => 'bar' ),
	array( 't' => 'leave', 'vis' => 99999999999, 'sc' => 140 ),
	array( 't' => 'form', 'k' => 'lead', 'id' => 'f', 'lead_phone' => '0501234567', 'lead_name' => 'דנה כהן' ),
	array( 't' => 'tour', 'o' => 'yes', 's' => array( 'nested' ) ),
) ), $NOW );
$by = array(); foreach ( $b['ev'] as $x ) { $by[ $x['t'] ][] = $x['d']; }
ok( 8 === count( $b['ev'] ), 'unknown types, broken events and a click without a kind are dropped (8 of 12 kept)', count( $b['ev'] ) );
ok( array( 'f' => 23, 'tw' => 'A', 'src' => 'user' ) === $by['floor'][0], 'floor keeps f, tw, src only (no height, no name, no phone)', $by['floor'][0] );
ok( 23 === $by['facing'][0]['f'] && 270 === $by['facing'][0]['b'] && 40 === mb_strlen( $by['facing'][0]['lbl'] ), 'facing: "23" is 23, -90 is 270, the label cut at 40', $by['facing'][0]['b'] );
ok( ! isset( $by['facing'][1]['f'] ) && 6 === $by['facing'][1]['b'], 'floor 999 is dropped, 725.6 is 6', $by['facing'][1] );
ok( array() === $by['view'][0], 'a bearing that is not a number is dropped' );
ok( array( 'k' => 'wascript', 'l' => 'ייעוץ חינם', 'w' => 'bar' ) === $by['click'][0], 'click: the kind is a key, the label loses its tags', $by['click'][0] );
ok( array( 'vis' => 86400000, 'sc' => 100 ) === $by['leave'][0], 'leave: time capped at one day, scroll at 100%' );
ok( array( 'k' => 'lead', 'id' => 'f' ) === $by['form'][0], 'form: kind and id only, the phone and the name never stored', $by['form'][0] );
ok( array( 'o' => 1 ) === $by['tour'][0], 'tour: open as 1, a nested value dropped' );
ok( false === strpos( json_encode( $b, JSON_UNESCAPED_UNICODE ), '0501234567' ) && false === strpos( json_encode( $b, JSON_UNESCAPED_UNICODE ), 'דנה' ), 'no phone and no name anywhere in the cleaned batch' );
$b = nadlan_vt_clean_batch( frame( array( array( 't' => 'open', 'at' => 1762500000000 - 30000 ), array( 't' => 'open', 'at' => 1762500000000 + 99000 ), array( 't' => 'open', 'at' => 1 ), array( 't' => 'open' ) ) ), $NOW );
ok( array( $NOW - 30, $NOW, $NOW - 7200, $NOW ) === array_column( $b['ev'], 'ts' ), 'the event clock: 30 s ago, a future time is now, at most two hours back, no time is now', array_column( $b['ev'], 'ts' ) );
$b = nadlan_vt_clean_batch( frame( array(), array( 'lang' => 'xx', 'dev' => 'tv', 'ref' => 'evil.com/path?q=<x>' ) ), $NOW );
ok( '' === $b['lang'] && '' === $b['dev'] && '' === $b['ref'], 'an unknown language, device and a referrer that is not a bare host are emptied' );

echo "2. the REST answers\n";
$db = $GLOBALS['wpdb'];
$st = function ( $r ) { return $r instanceof WP_Error ? $r->get_error_data()['status'] . ' ' . $r->get_error_code() : ( $r instanceof WP_REST_Response ? (string) $r->status : 'other' ); };
$okb = json_encode( frame( array( array( 't' => 'open', 'at' => 1762500000000 ), array( 't' => 'floor', 'f' => 23, 'at' => 1762500000000 ) ) ) );
$UA = 'Mozilla/5.0 (iPhone) Safari/605';
$_SERVER['REMOTE_ADDR'] = '203.0.113.77'; $_SERVER['HTTP_CF_IPCOUNTRY'] = 'fr';
ok( '400 nlvt_bad' === $st( nadlan_vt_rest( new T_Req( '' ) ) ), 'an empty body: 400 nlvt_bad (the release check)' );
ok( '413 nlvt_big' === $st( nadlan_vt_rest( new T_Req( str_repeat( 'x', 16385 ) ) ) ), 'over 16 KB: 413' );
$db->q = array();
ok( '204' === $st( nadlan_vt_rest( new T_Req( $okb, array( 'sec_gpc' => '1', 'user_agent' => $UA ) ) ) ) && ! $db->q, 'Sec-GPC: 1: 204 and not one query' );
ok( '204' === $st( nadlan_vt_rest( new T_Req( $okb, array( 'dnt' => '1', 'user_agent' => $UA ) ) ) ) && ! $db->q, 'DNT: 1: 204 and not one query' );
ok( '403 nlvt_origin' === $st( nadlan_vt_rest( new T_Req( $okb, array( 'origin' => 'https://evil.example', 'user_agent' => $UA ) ) ) ), 'another site\'s Origin: 403' );
ok( '403 nlvt_origin' === $st( nadlan_vt_rest( new T_Req( $okb, array( 'origin' => 'null', 'user_agent' => $UA ) ) ) ), 'Origin null: 403' );
ok( '204' === $st( nadlan_vt_rest( new T_Req( $okb, array( 'user_agent' => 'Googlebot/2.1' ) ) ) ) && ! $db->q, 'a robot: 204 and nothing stored' );
$GLOBALS['T_OPT']['nadlan_visit_trail'] = '0';
ok( '204' === $st( nadlan_vt_rest( new T_Req( $okb, array( 'user_agent' => $UA ) ) ) ) && ! $db->q, 'the owner switch off: 204 and nothing stored' );
unset( $GLOBALS['T_OPT']['nadlan_visit_trail'] );
ok( '400 nlvt_bad' === $st( nadlan_vt_rest( new T_Req( json_encode( frame( array( array( 't' => 'open' ) ), array( 'page' => 55 ) ) ), array( 'user_agent' => $UA ) ) ) ), 'a page that is not a project: 400' );
$db->q = array(); $db->var = 0;
$r = nadlan_vt_rest( new T_Req( $okb, array( 'origin' => 'https://www.nad-lan.co.il', 'user_agent' => $UA ) ) );
$all = implode( "\n", $db->q );
ok( '204' === $st( $r ), 'a good batch from the site (www or not): 204' );
ok( false !== strpos( $all, 'INSERT INTO wp_nadlan_visits' ) && false !== strpos( $all, 'INSERT INTO wp_nadlan_visit_events' ), 'stored in the two tables' );
ok( false !== strpos( $all, "'FR'" ), 'the country from the CF header (fr -> FR)' );
ok( false === strpos( $all, '203.0.113' ) && false === strpos( json_encode( $GLOBALS['T_TR'] ), '203.0.113' ), 'the IP is in no query and in no stored counter' );
ok( 1 === preg_match( "/VALUES \('AbCdEfGhIjKlMnOpQrStUv','pv0000000001','[0-9: -]{19}',7001,'he','open',''\),\('AbCdEfGhIjKlMnOpQrStUv','pv0000000001','[0-9: -]{19}',7001,'he','floor','\{\\\\\"f\\\\\":23\}'\)/", $all ), 'the event rows: vid, pv, time, page, lang, kind, the cleaned JSON' );
ok( 2 === (int) get_transient( 'nadlan_vt_day_' . gmdate( 'Ymd' ) ), 'the day counter counts the events' );
$GLOBALS['T_TR'] = array(); $codes = array();
for ( $i = 0; $i < 31; $i++ ) { $codes[] = $st( nadlan_vt_rest( new T_Req( $okb, array( 'user_agent' => $UA ) ) ) ); }
ok( 30 === count( array_keys( $codes, '204' ) ) && '429 nlvt_rate' === $codes[30], '30 batches a minute from one visitor, the 31st: 429' );
$GLOBALS['T_TR'] = array( 'nadlan_vt_day_' . gmdate( 'Ymd' ) => 200000 );
ok( '429 nlvt_rate' === $st( nadlan_vt_rest( new T_Req( $okb, array( 'user_agent' => $UA ) ) ) ), '200,000 events in a day for the site: 429' );
$GLOBALS['T_TR'] = array();
$db->q = array(); $db->var = 2999;
nadlan_vt_rest( new T_Req( $okb, array( 'user_agent' => $UA ) ) );
ok( 1 === preg_match_all( "/\('AbCdEfGhIjKlMnOpQrStUv','pv0000000001'/", implode( "\n", $db->q ) ), 'a visit at 2,999 events stores one more and stops at 3,000' );
$db->q = array(); $db->var = 3000;
nadlan_vt_rest( new T_Req( $okb, array( 'user_agent' => $UA ) ) );
ok( false === strpos( implode( "\n", $db->q ), 'INSERT' ), 'a full visit stores nothing more' );
$db->var = 0;

echo "3. the lead link\n";
$_SERVER['HTTP_X_NL_VISIT'] = 'VisitFromHeader0000001';
ok( 'VisitFromHeader0000001' === nadlan_vt_request_vid(), 'the X-NL-Visit header' );
$_SERVER['HTTP_X_NL_VISIT'] = "bad id'; DROP"; $_POST['nl_visit'] = 'VisitFromForm00000002';
ok( 'VisitFromForm00000002' === nadlan_vt_request_vid(), 'a bad header is ignored; the form field nl_visit' );
unset( $_SERVER['HTTP_X_NL_VISIT'], $_POST['nl_visit'] );
run_hook( 'rest_pre_dispatch', null, null, new T_Req( '{}', array( 'x_nl_visit' => 'VisitFromRest000000003' ), '/nadlan/v1/lead' ) );
ok( 'VisitFromRest000000003' === nadlan_vt_request_vid(), 'a REST lead request: the header kept by rest_pre_dispatch' );
$db->q = array();
run_hook( 'wp_after_insert_post', 900, (object) array( 'post_type' => 'nadlan_lead' ), false );
ok( 'VisitFromRest000000003' === get_post_meta( 900, '_nl_visit' ), 'a new lead gets _nl_visit' );
ok( 1 === preg_match( "/INSERT INTO wp_nadlan_visits \(vid, first_at, last_at, lead_id\) VALUES \('VisitFromRest000000003','[^']+','[^']+',900\)\s+ON DUPLICATE KEY UPDATE lead_id = IF\(lead_id = 0/", implode( "\n", $db->q ) ), 'the visit row gets the lead (a stub when the trail is still on its way; the first lead stays)' );
$GLOBALS['T_META'] = array(); $db->q = array();
run_hook( 'wp_after_insert_post', 900, (object) array( 'post_type' => 'nadlan_lead' ), true );
run_hook( 'wp_after_insert_post', 901, (object) array( 'post_type' => 'post' ), false );
ok( ! $GLOBALS['T_META'] && ! $db->q, 'an update, or another post type: nothing' );
$_SERVER['HTTP_SEC_GPC'] = '1';
run_hook( 'wp_after_insert_post', 900, (object) array( 'post_type' => 'nadlan_lead' ), false );
ok( ! $GLOBALS['T_META'], 'a lead sent with Global Privacy Control on: no link' );
unset( $_SERVER['HTTP_SEC_GPC'] );
$GLOBALS['T_OPT']['nadlan_vt_db'] = ''; $saved = $GLOBALS['wpdb'];
$GLOBALS['wpdb'] = new class extends T_DB { function get_charset_collate() { throw new RuntimeException( 'db down' ); } };
$thrown = false;
try { run_hook( 'wp_after_insert_post', 900, (object) array( 'post_type' => 'nadlan_lead' ), false ); } catch ( \Throwable $e ) { $thrown = true; }
ok( ! $thrown, 'a database failure inside the link never reaches the lead\'s own code' );
$GLOBALS['wpdb'] = $saved; $db = $saved; $GLOBALS['T_OPT']['nadlan_vt_db'] = '1';
unset( $GLOBALS['nadlan_vt_rest_vid'] );

echo "4. the timeline in plain Hebrew\n";
ok( 'מערב' === nadlan_vt_dir_word( 268 ) && 'צפון' === nadlan_vt_dir_word( 359 ) && 'צפון מזרח' === nadlan_vt_dir_word( 45 ) && 'דרום' === nadlan_vt_dir_word( -180 ), 'directions: 268 west, 359 north, 45 north-east, -180 south' );
$L = array(
	array( 'open', array(), 'נכנס לעמוד ריינבו תל אביב' ),
	array( 'floor', array( 'f' => 23, 'src' => 'user' ), 'בחר קומה 23' ),
	array( 'floor', array( 'f' => 7, 'src' => 'auto' ), 'בחר קומה 7 (אוטומטית)' ),
	array( 'facing', array( 'f' => 23, 'b' => 268, 'u' => '23-w' ), 'בחר כיוון בקומה 23: מערב (268°), דירה 23-w' ),
	array( 'facing', array( 'f' => 12, 'tw' => 'B', 'dir' => 'לכיוון הים', 'lbl' => 'B-12-3' ), 'בחר כיוון בקומה 12 במגדל B: לכיוון הים, B-12-3' ),
	array( 'view', array( 'b' => 90 ), 'סובב את הנוף מהקומה אל המזרח (90°)' ),
	array( 'ftour', array( 'n' => 'בריכה' ), 'נכנס לסיור 360° במתקן "בריכה"' ),
	array( 'fcta', array( 'f' => 23, 'b' => 268 ), 'לחץ על וואטסאפ מכרטיס הקומה 23, מבט למערב (268°)' ),
	array( 'faction', array( 'a' => 'inside', 'f' => 23 ), 'נכנס לדירה ב־360° מקומה 23' ),
	array( 'tour', array( 'o' => 1, 's' => 'living' ), 'פתח סיור בתוך הדירה (living)' ),
	array( 'example', array( 'o' => 1, 'id' => 'B4', 'f' => 18, 'dir' => 'צפון' ), 'פתח דירה לדוגמה B4 בקומה 18, מבט לצפון' ),
	array( 'click', array( 'k' => 'wa', 'l' => 'ייעוץ חינם', 'w' => 'bar' ), 'לחץ על וואטסאפ "ייעוץ חינם" בפס הוואטסאפ' ),
	array( 'click', array( 'k' => 'tel', 'w' => 'hero' ), 'לחץ על חיוג בראש העמוד' ),
	array( 'click', array( 'k' => 'book_day' ), 'בחר יום לפגישה' ),
	array( 'click', array( 'k' => 'cta', 'l' => 'סיור וירטואלי בכיכר', 'w' => 'hero' ), 'לחץ על "סיור וירטואלי בכיכר" בראש העמוד' ),
	array( 'click', array( 'k' => 'deal_floor', 'f' => 30 ), 'לחץ "לקומה במגדל" בטבלת העסקאות (קומה 30)' ),
	array( 'form', array( 'k' => 'lead', 'id' => 'nl-lead' ), 'שלח טופס פנייה (nl-lead)' ),
	array( 'leave', array( 'vis' => 754000, 'sc' => 82 ), 'יצא מהעמוד אחרי 12:34 דקות בעמוד, גלל עד 82% מהעמוד' ),
);
foreach ( $L as $x ) { $got = nadlan_vt_line( $x[0], $x[1], 7001, 'he' ); ok( $got === $x[2], $x[0] . ': ' . $x[2], $got === $x[2] ? null : $got ); }
ok( 'נכנס לעמוד Rainbow Tel Aviv (אנגלית)' === nadlan_vt_line( 'open', array(), 7002, 'en' ), 'an English page names its language' );
$rows = array();
foreach ( array( array( 'open', '' ), array( 'leave', '{"vis":5000}' ), array( 'floor', '{"f":3}' ), array( 'leave', '{"vis":9000}' ) ) as $i => $x ) {
	$rows[] = (object) array( 'vid' => 'v', 'pv' => 'p1', 'at' => '2026-11-07 10:00:0' . $i, 'page' => 7001, 'lang' => 'he', 'ev' => $x[0], 'd' => $x[1] );
}
$ln = nadlan_vt_lines( $rows );
ok( 3 === count( $ln ) && 'leave' === $ln[2]['ev'] && false !== strpos( $ln[2]['text'], '0:09' ), 'two leave records of one page view: only the last is shown', array_column( $ln, 'text' ) );
ok( '12:00' === $ln[0]['time'], 'times in the site\'s clock (Israel, wp_date)' );

echo "5. the new-lead email, the admin screen, the clean-up\n";
$GLOBALS['T_META'][900] = array( '_nl_visit' => 'AbCdEfGhIjKlMnOpQrStUv', 'name' => 'דנה כהן' );
$db->results = function ( $sql ) use ( $rows ) {
	if ( false !== strpos( $sql, 'FROM wp_nadlan_visit_events WHERE vid IN' ) ) { return array_map( function ( $r ) { $r->vid = 'AbCdEfGhIjKlMnOpQrStUv'; return $r; }, array_map( function ( $r ) { return clone $r; }, $rows ) ); }
	if ( false !== strpos( $sql, 'FROM wp_nadlan_visits WHERE' ) ) { return array( (object) array( 'vid' => 'AbCdEfGhIjKlMnOpQrStUv', 'first_at' => '2026-11-07 10:00:00', 'last_at' => '2026-11-07 10:12:00', 'country' => 'IL', 'lang' => 'he', 'dev' => 'm', 'ref' => 'google.co.il', 'entry' => 7001, 'pages' => 2, 'events' => 4, 'lead_id' => 900 ) ); }
	return array();
};
run_hook( 'nadlan_lead_rich_alert', 900 );
ok( ! isset( $GLOBALS['nadlan_vt_alert'] ), 'the alert flag is set and cleared around the alert' );
$GLOBALS['nadlan_vt_alert'] = 900;
$m = run_hook( 'wp_mail', array( 'to' => 'a@b', 'subject' => '[נדלן] ליד חדש: דנה כהן', 'message' => "שם: דנה כהן\n\n-- nad-lan.co.il 2026-11-07 10:12 UTC" ) );
ok( false !== strpos( $m['message'], "מה עשה בעמוד הפרויקט לפני הפנייה:\n" ) && false !== strpos( $m['message'], 'בחר קומה 3' ) && strpos( $m['message'], 'בחר קומה 3' ) < strpos( $m['message'], '-- nad-lan.co.il' ), 'the rich lead email gets the timeline, above its footer' );
ok( false !== strpos( $m['message'], 'page=nadlan-visit-trails&vid=AbCdEfGhIjKlMnOpQrStUv' ), 'and a link to the whole trail' );
$m2 = run_hook( 'wp_mail', array( 'to' => 'a@b', 'subject' => '[נדלן] ליד חדש: x', 'message' => 'x' ) );
ok( 'x' === $m2['message'], 'once only (a second mail in the same alert is untouched)' );
$GLOBALS['nadlan_vt_alert'] = 900;
$m3 = run_hook( 'wp_mail', array( 'to' => 'a@b', 'subject' => '[נדלן] משתמש חדש נרשם', 'message' => 'y' ) );
ok( 'y' === $m3['message'], 'another email is untouched' );
unset( $GLOBALS['nadlan_vt_alert'] );
$GLOBALS['T_TYPES'][900] = 'nadlan_lead';
$db->row = array( 'visits' => 12, 'floor' => 7, 'tour' => 3, 'wa' => 2 ); $db->var = 1; $db->col = array( 7001 );
$rows[1]->d = '{"vis":5000}';
$rows[2]->d = '{"f":3,"tw":"<script>alert(1)<\/script>"}';
$html = nadlan_vt_admin_html( array( 'leads' => 1 ) );
ok( false !== strpos( $html, '<h1>מסלולי ביקור</h1>' ) && false !== strpos( $html, 'דנה כהן' ) && false !== strpos( $html, 'ריינבו תל אביב' ), 'the screen: the title, the lead\'s name next to the visit, the project' );
ok( false === strpos( $html, '<script>alert' ) && false !== strpos( $html, '&lt;script&gt;' ), 'a stored text is escaped on the screen' );
ok( false !== strpos( $html, 'lead_id > 0' ) || false !== strpos( implode( "\n", $db->q ), 'lead_id > 0' ), 'the filter "only visits that became leads" reaches the query' );
ok( false !== strpos( $html, 'name="action" value="nadlan_vt_delete"' ) && false !== strpos( $html, '_wpnonce' ), 'each visit can be deleted (nonce)' );
$db->q = array();
nadlan_vt_delete_visit( 'AbCdEfGhIjKlMnOpQrStUv' );
ok( 2 === count( array_filter( $db->q, function ( $q ) { return 0 === strpos( $q, 'DELETE FROM' ); } ) ) && '' === get_post_meta( 900, '_nl_visit' ), 'delete: both tables and the lead\'s link' );
$db->q = array();
nadlan_vt_prune();
$pq = implode( "\n", $db->q );
preg_match( "/DELETE FROM wp_nadlan_visit_events WHERE at < '([^']+)'/", $pq, $pm );
$days = $pm ? round( ( time() - strtotime( $pm[1] . ' UTC' ) ) / 86400 ) : -1;
ok( 365 == $days && false !== strpos( $pq, 'DELETE FROM wp_nadlan_visits WHERE last_at <' ), 'the daily clean-up deletes what is older than 12 months (365 days)', $days );
ok( 5 === has_action( 'wp_after_insert_post', 'nadlan_vt_after_insert' ) && false !== has_action( 'nadlan_vt_prune', 'nadlan_vt_prune' ), 'hooked: the lead (priority 5, before the routing and the alerts), the clean-up' );
$hc = run_hook( 'nadlan_config_healthcheck', array() );
ok( '1.0.0' === $hc['visit_trail']['version'] && true === $hc['visit_trail']['on'], 'the healthcheck line visit_trail 1.0.0' );

$db->var = 1; $db->results = array(); $db->row = array();
$stt = nadlan_vt_selftest();
ok( '1.0.0' === $stt['version'] && 1 === $stt['db'] && 1 === $stt['tables'] && 4 === $stt['clean'] && 1 === $stt['no_phone'] && 1 === $stt['admin_title'] && true === $stt['lead_hook'], 'the release bridge self-test: tables, 4 of 5 sample events kept, the phone dropped, the screen, the lead hook', $stt );
ok( 'בחר כיוון בקומה 23: מערב (268°), דירה 23-w' === $stt['line'], 'the self-test line', $stt['line'] );

echo "6. the file\n";
ok( ! preg_match( '/[\x{2013}\x{2014}]/u', $SRC ), 'no long dash' );
ok( 1 === substr_count( $SRC, "\$_SERVER['REMOTE_ADDR']" ) && false !== strpos( $SRC, "'ip' . md5( substr( (string) ( \$_SERVER['REMOTE_ADDR']" ), 'REMOTE_ADDR is read once, hashed for the minute counter only' );
ok( false !== strpos( $SRC, 'PRIMARY KEY  (vid)' ) && false !== strpos( $SRC, 'PRIMARY KEY  (id)' ), 'dbDelta: two spaces after PRIMARY KEY' );

echo "\n" . ( $n - $fails ) . " of $n passed" . ( $fails ? ", $fails FAILED" : '' ) . "\n";
exit( $fails ? 1 : 0 );
