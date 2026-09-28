<?php
/**
 * php -S router for the TogetherRoom harness (scripts/together/harness.py): runs the real inc/together.php on the
 * WordPress stand-in (wp-stub.php).
 *
 *   php -S 127.0.0.1:8765 scripts/together/router.php
 *
 *   /wp-json/nadlan/v1/room...   the module's REST routes (X-WP-Nonce: rep-nonce = a logged-in representative;
 *                                X-Test-IP sets the caller's address for the rate limits)
 *   /__head?room=...             what the module prints in <head> on a project page
 *   /__footer?room=...&rep=1     what it prints before </body> (the room's container and script, or the chooser)
 *   /__reset?rep_now=1&lk=0      a clean store; rep_now marks a representative available
 *   /__admin                     the settings page (as an administrator)
 *   /harness.html, /plugins/...  static files from the repository (the offline harness page and the assets)
 */
$path = (string) parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH );
if ( '/favicon.ico' === $path ) { http_response_code( 204 ); exit; }
$root = dirname( __DIR__, 2 );
if ( '/harness.html' === $path || 0 === strpos( $path, '/plugins/' ) ) {
	$f = realpath( ( '/harness.html' === $path ? __DIR__ : $root ) . $path );
	if ( ! $f || 0 !== strpos( $f, realpath( $root ) ) || ! is_file( $f ) ) { http_response_code( 404 ); exit; }
	$types = array( 'html' => 'text/html; charset=utf-8', 'js' => 'text/javascript; charset=utf-8', 'css' => 'text/css; charset=utf-8', 'jpg' => 'image/jpeg', 'json' => 'application/json' );
	header( 'Content-Type: ' . ( $types[ pathinfo( $f, PATHINFO_EXTENSION ) ] ?? 'application/octet-stream' ) );
	readfile( $f );
	exit;
}
if ( ! empty( $_SERVER['HTTP_X_TEST_IP'] ) ) { $_SERVER['REMOTE_ADDR'] = (string) $_SERVER['HTTP_X_TEST_IP']; }
require __DIR__ . '/wp-stub.php';
if ( 'rep-nonce' === ( $_SERVER['HTTP_X_WP_NONCE'] ?? '' ) || ! empty( $_GET['rep'] ) ) { $GLOBALS['__nltr_user'] = 7; }
header( 'Access-Control-Allow-Origin: *' );

if ( '/__reset' === $path ) {
	__nltr_reset();
	if ( ! empty( $_GET['rep_now'] ) ) { update_option( 'nadlan_tr_rep_now', '1', false ); }
	if ( ! empty( $_GET['lk'] ) ) {
		update_option( 'nadlan_tr_lk_url', 'wss://livekit.invalid', false ); // a reserved name: no real server is ever contacted
		update_option( 'nadlan_tr_lk_key', 'APIharnesskey', false );
		update_option( 'nadlan_tr_lk_secret', 'harness-secret-0123456789abcdef', false );
	}
	header( 'Content-Type: application/json' );
	echo '{"ok":true}';
	exit;
}
if ( '/__head' === $path || '/__footer' === $path ) {
	header( 'Content-Type: text/html; charset=utf-8' );
	__nltr_run( '/__head' === $path ? 'wp_head' : 'wp_footer', 'together.php' );
	exit;
}
if ( '/__admin' === $path ) {
	$GLOBALS['__nltr_user'] = 7;
	header( 'Content-Type: text/html; charset=utf-8' );
	echo '<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><body>';
	// the settings page's callback, as WordPress would call it from the menu
	__nltr_run( 'admin_menu', 'together.php' );
	$page = $GLOBALS['__nltr_pages']['nadlan-together'] ?? null;
	if ( $page ) { $page(); }
	echo '</body></html>';
	exit;
}
if ( 0 === strpos( $path, '/wp-json/' ) ) {
	$route  = '/' . substr( $path, strlen( '/wp-json/' ) );
	$route  = rtrim( $route, '/' );
	$ns     = 'nadlan/v1';
	$rel    = substr( $route, strlen( '/' . $ns ) );
	$body   = json_decode( (string) file_get_contents( 'php://input' ), true );
	list( $status, $data ) = __nltr_call( $_SERVER['REQUEST_METHOD'], $ns . $rel, $_GET, is_array( $body ) ? $body : array() );
	http_response_code( $status );
	header( 'Content-Type: application/json; charset=utf-8' );
	echo json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
	exit;
}
http_response_code( 404 );
echo 'not found';
