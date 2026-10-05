<?php
/**
 * HAD-256 release rehearsal (bench only, NEVER on a real site): a small stand-in for the Code Snippets plugin, so
 * scripts/had-256/deploy_had256.py can be run end to end against 127.0.0.1 before main runs it on the live site.
 *
 *   - snippets live in the option nlj_emu_snippets (id => name, code, active, scope, priority, desc), seeded once from
 *     wp-content/nlj-emu-seed/<id>-<name>.php (the live base bodies: 638 x-skin-a, 690 x-broker-drop 1.1.3,
 *     699 x-broker-join, 707 x-owner-wizard 1.0.0; the opening tag removed as Code Snippets stores them);
 *   - the REST routes the runners use: GET/POST /code-snippets/v1/snippets, GET/PUT/DELETE /snippets/<id>,
 *     PUT /snippets/<id>/activate|deactivate (manage_options);
 *   - active snippets run at plugins_loaded priority 1, in id order, through eval(), as Code Snippets runs them; a
 *     snippet that throws is switched off (as Code Snippets' safe handling does) and logged to wp-content/nlj-emu.log;
 *   - an application password for the bench admin (synthetic), written to wp-content/nlj-emu-auth.txt for --bench-auth;
 *     application passwords are allowed over http on this loopback bench only.
 * Active only when wp-content/nlj-variant.txt starts with "rehearsal".
 */
if ( ! defined( 'ABSPATH' ) ) { return; }
if ( strpos( (string) @file_get_contents( WP_CONTENT_DIR . '/nlj-variant.txt' ), 'rehearsal' ) !== 0 ) { return; }
define( 'NLJ_SNIPPET_EMU', true );

function nlj_emu_all() {
	$a = get_option( 'nlj_emu_snippets', null );
	if ( ! is_array( $a ) ) {
		$a = array();
		foreach ( (array) glob( WP_CONTENT_DIR . '/nlj-emu-seed/*.php' ) as $f ) {
			if ( preg_match( '/^(\d+)-([a-z0-9-]+)\.php$/', basename( $f ), $m ) ) {
				$a[ (int) $m[1] ] = array( 'name' => $m[2], 'code' => (string) file_get_contents( $f ), 'active' => true, 'scope' => 'global', 'priority' => 10, 'desc' => 'seeded from the live base (bench)' );
			}
		}
		ksort( $a );
		update_option( 'nlj_emu_snippets', $a, false );
	}
	return $a;
}

function nlj_emu_save( $a ) {
	ksort( $a );
	update_option( 'nlj_emu_snippets', $a, false );
}

function nlj_emu_out( $id, $s ) {
	return array( 'id' => (int) $id, 'name' => $s['name'], 'desc' => $s['desc'] ?? '', 'code' => $s['code'], 'scope' => $s['scope'] ?? 'global', 'priority' => (int) ( $s['priority'] ?? 10 ), 'active' => (bool) $s['active'] );
}

/* run the active snippets after every plugin, as Code Snippets does */
add_action( 'plugins_loaded', function () {
	foreach ( nlj_emu_all() as $id => $s ) {
		if ( empty( $s['active'] ) ) { continue; }
		try {
			eval( $s['code'] );   // phpcs:ignore -- the bench's stand-in for Code Snippets
		} catch ( Throwable $e ) {
			$a = nlj_emu_all();
			$a[ $id ]['active'] = false;
			nlj_emu_save( $a );
			@file_put_contents( WP_CONTENT_DIR . '/nlj-emu.log', gmdate( 'c' ) . ' snippet ' . $id . ' switched off: ' . get_class( $e ) . ' ' . $e->getMessage() . "\n", FILE_APPEND );
		}
	}
}, 1 );

add_filter( 'wp_is_application_passwords_available', '__return_true' );

add_action( 'init', function () {
	if ( get_option( 'nlj_emu_auth' ) ) { return; }
	$u = get_user_by( 'email', 'bench.admin@example.test' );
	if ( ! $u || ! class_exists( 'WP_Application_Passwords' ) ) { return; }
	$r = WP_Application_Passwords::create_new_application_password( $u->ID, array( 'name' => 'had256 rehearsal' ) );
	if ( is_wp_error( $r ) ) { return; }
	@file_put_contents( WP_CONTENT_DIR . '/nlj-emu-auth.txt', $u->user_login . ':' . $r[0] );
	update_option( 'nlj_emu_auth', 1, false );
}, 70 );

add_action( 'rest_api_init', function () {
	$ns   = 'code-snippets/v1';
	$perm = function () { return current_user_can( 'manage_options' ); };
	$one  = function ( WP_REST_Request $r ) {
		$a  = nlj_emu_all();
		$id = (int) $r['id'];
		return isset( $a[ $id ] ) ? array( $a, $id ) : null;
	};
	register_rest_route( $ns, '/snippets', array(
		array( 'methods' => 'GET', 'permission_callback' => $perm, 'callback' => function () {
			$out = array();
			foreach ( nlj_emu_all() as $id => $s ) { $out[] = nlj_emu_out( $id, $s ); }
			return $out;
		} ),
		array( 'methods' => 'POST', 'permission_callback' => $perm, 'callback' => function ( WP_REST_Request $r ) {
			$a  = nlj_emu_all();
			$id = max( 1000, $a ? max( array_keys( $a ) ) + 1 : 1000 );
			$a[ $id ] = array( 'name' => (string) $r['name'], 'code' => (string) $r['code'], 'active' => ! empty( $r['active'] ), 'scope' => (string) ( $r['scope'] ?: 'global' ), 'priority' => 10, 'desc' => (string) $r['desc'] );
			nlj_emu_save( $a );
			return nlj_emu_out( $id, $a[ $id ] );
		} ),
	) );
	register_rest_route( $ns, '/snippets/(?P<id>\d+)', array(
		array( 'methods' => 'GET', 'permission_callback' => $perm, 'callback' => function ( WP_REST_Request $r ) use ( $one ) {
			$x = $one( $r );
			return $x ? nlj_emu_out( $x[1], $x[0][ $x[1] ] ) : new WP_Error( 'nf', 'no snippet', array( 'status' => 404 ) );
		} ),
		array( 'methods' => 'PUT', 'permission_callback' => $perm, 'callback' => function ( WP_REST_Request $r ) use ( $one ) {
			$x = $one( $r );
			if ( ! $x ) { return new WP_Error( 'nf', 'no snippet', array( 'status' => 404 ) ); }
			list( $a, $id ) = $x;
			foreach ( array( 'name', 'code', 'scope', 'desc' ) as $k ) { if ( null !== $r[ $k ] ) { $a[ $id ][ $k ] = (string) $r[ $k ]; } }
			if ( null !== $r['active'] ) { $a[ $id ]['active'] = (bool) $r['active']; }
			nlj_emu_save( $a );
			return nlj_emu_out( $id, $a[ $id ] );
		} ),
		array( 'methods' => 'DELETE', 'permission_callback' => $perm, 'callback' => function ( WP_REST_Request $r ) use ( $one ) {
			$x = $one( $r );
			if ( ! $x ) { return new WP_Error( 'nf', 'no snippet', array( 'status' => 404 ) ); }
			list( $a, $id ) = $x;
			unset( $a[ $id ] );
			nlj_emu_save( $a );
			return array( 'deleted' => true, 'id' => $id );
		} ),
	) );
	foreach ( array( 'activate' => true, 'deactivate' => false ) as $verb => $on ) {
		register_rest_route( $ns, '/snippets/(?P<id>\d+)/' . $verb, array( 'methods' => 'PUT', 'permission_callback' => $perm, 'callback' => function ( WP_REST_Request $r ) use ( $one, $on ) {
			$x = $one( $r );
			if ( ! $x ) { return new WP_Error( 'nf', 'no snippet', array( 'status' => 404 ) ); }
			list( $a, $id ) = $x;
			if ( $on ) {   // as Code Snippets: a body that does not parse is not switched on
				try { token_get_all( "<?php\n" . $a[ $id ]['code'], TOKEN_PARSE ); }
				catch ( ParseError $e ) { return new WP_Error( 'parse', $e->getMessage(), array( 'status' => 400 ) ); }
			}
			$a[ $id ]['active'] = $on;
			nlj_emu_save( $a );
			return nlj_emu_out( $id, $a[ $id ] );
		} ) );
	}
} );
