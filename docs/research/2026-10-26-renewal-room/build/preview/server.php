<?php
/**
 * Local preview server for RenewalRoomPro (never talks to nad-lan.co.il):
 *   php -S 127.0.0.1:8765 build/preview/server.php
 *   http://127.0.0.1:8765/room.html?as=staff            the organizer's room (portfolio), the REAL /my-renewal/ route code
 *   http://127.0.0.1:8765/room.html?as=staff&space=ID   one complex
 *   http://127.0.0.1:8765/room.html?as=neighbor&space=ID  what an approved neighbour gets
 *   http://127.0.0.1:8765/room.html?as=anon             the public landing with the sample room
 *   http://127.0.0.1:8765/__reset                       re-seed the sample data
 * The page body is printed by the plugin's own template_redirect handler for /my-renewal/; the JSON comes from the plugin's
 * own REST routes, run through build/tests/wp-stub.php with the sample data of build/tests/fixture.php ("נתוני דוגמה").
 * room.html carries a copy of the site skin's aggressive !important link and heading rules, to prove the room survives them.
 */
$B = dirname( __DIR__ );
$LIVE = dirname( $B ) . '/live-base';
$REPO = dirname( dirname( dirname( dirname( $B ) ) ) );
$STATE = getenv( 'RR_STATE' ) ?: sys_get_temp_dir() . '/rrp-preview-state.json';
$uri = parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );

/* static files */
if ( 0 === strpos( $uri, '/assets/' ) ) {
	$f = realpath( $B . $uri );
	if ( ! $f || 0 !== strpos( $f, realpath( $B . '/assets' ) ) ) { http_response_code( 404 ); exit; }
	header( 'Content-Type: ' . ( substr( $f, -3 ) === '.js' ? 'application/javascript' : 'text/css' ) . '; charset=utf-8' );
	header( 'Cache-Control: no-store' );
	readfile( $f ); exit;
}
if ( '/engine/models/standard-residential.glb' === $uri ) {
	header( 'Content-Type: model/gltf-binary' );
	readfile( $REPO . '/plugins/nadlan-config/assets/showroom-engine/models/standard-residential.glb' ); exit;
}
if ( '/favicon.ico' === $uri ) { http_response_code( 204 ); exit; }

require $B . '/tests/wp-stub.php';
require $B . '/tests/fixture.php';
$GLOBALS['STUB']['rest_base'] = 'http://' . $_SERVER['HTTP_HOST'] . '/wp-json/';
function nadlan_showroom_engine_base_url() { return '/engine/'; }
stub_boot_room( $B, $LIVE );
rr_users();
if ( '/__reset' === $uri || ! stub_load( $STATE ) ) {
	$GLOBALS['STUB']['posts'] = array(); $GLOBALS['STUB']['meta'] = array(); $GLOBALS['STUB']['options'] = array(); $GLOBALS['STUB']['transients'] = array();
	$ids = rr_seed( $B . '/preview/data/live-demo-payload.json' );
	update_option( 'rr_preview_ids', $ids );
	stub_save( $STATE );
	if ( '/__reset' === $uri ) { header( 'Content-Type: application/json' ); echo json_encode( $ids ); exit; }
}
$ids = get_option( 'rr_preview_ids', array() );
$who = array( 'anon' => 0, 'orgadmin' => RR_U_ORGADMIN, 'staff' => RR_U_FIELD, 'pm' => RR_U_PM, 'neighbor' => RR_U_NB, 'pending' => RR_U_NB_PENDING, 'committee' => RR_U_COMMITTEE, 'outsider' => RR_U_OUTSIDER, 'committee-room' => RR_U_LEGACY );
$as = isset( $_GET['as'] ) ? (string) $_GET['as'] : ( $_COOKIE['rr_as'] ?? 'staff' );
if ( isset( $_GET['as'] ) ) { setcookie( 'rr_as', $as, 0, '/' ); }
stub_as( $who[ $as ] ?? RR_U_FIELD );
stub_now( getenv( 'RR_NOW' ) ?: '2026-10-26 10:00:00' );
if ( '/__ids' === $uri ) { header( 'Content-Type: application/json' ); echo json_encode( $ids ); exit; }

/* REST */
if ( 0 === strpos( $uri, '/wp-json/' ) ) {
	$path = substr( $uri, strlen( '/wp-json' ) );
	$body = json_decode( (string) file_get_contents( 'php://input' ), true );
	$r = stub_rest( $_SERVER['REQUEST_METHOD'], $path, is_array( $body ) ? $body : array(), $_GET );
	if ( 'GET' !== $_SERVER['REQUEST_METHOD'] ) { stub_save( $STATE ); }
	http_response_code( $r[0] );
	header( 'Content-Type: application/json; charset=utf-8' );
	header( 'Cache-Control: no-store' );
	echo json_encode( $r[1], JSON_UNESCAPED_UNICODE );
	exit;
}

/* the page: room.html with the real /my-renewal/ output in place of its placeholder */
if ( '/room.html' === $uri || '/my-renewal/' === $uri || '/' === $uri ) {
	$shell = file_get_contents( __DIR__ . '/room.html' );
	$lang = isset( $_GET['lang'] ) ? (string) $_GET['lang'] : 'he';
	$shell = str_replace( array( '{{LANG}}', '{{DIR}}' ), array( htmlspecialchars( $lang ), 'he' === $lang ? 'rtl' : 'ltr' ), $shell );
	ob_start( function ( $html ) use ( $shell ) { return str_replace( '<!--RR_PAGE-->', $html, $shell ); } );
	$GLOBALS['STUB']['qv'] = array( 'nadlan_my_renewal' => '1' );
	do_action( 'template_redirect' ); // the plugin's own handler prints the landing or the dashboard, then exits
	exit;
}
http_response_code( 404 );
echo 'not found';
