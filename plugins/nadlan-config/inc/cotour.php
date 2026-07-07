<?php
/**
 * nadlan-config - LIVE CO-TOURING (enhancement #3, the crown jewel - Realsee's
 * killer feature, unseen in the off-plan world).
 *
 * An agent and a buyer navigate the SAME 3D building together: the agent's
 * camera, selected apartment, lighting and filter broadcast every ~1.5s; the
 * buyer's screen follows. Transport is plain REST + transients - no sockets,
 * no external service, works on shared hosting. A room lives 5 minutes past
 * its last broadcast; the room code is the only secret (share the join link
 * only with your buyer).
 *
 *  POST /nadlan/v1/cotour   {room, state}   - the host broadcasts
 *  GET  /nadlan/v1/cotour?room=...          - the viewer follows
 *
 * The engine drives it via ?cotour=host|join&room=<code> on any project page,
 * with a one-click "share live tour" button in the theater.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/cotour', array(
		array(
			'methods' => 'POST', 'permission_callback' => '__return_true',
			'callback' => function ( WP_REST_Request $req ) {
				$p    = $req->get_json_params();
				$room = preg_replace( '/[^a-z0-9]/i', '', (string) ( $p['room'] ?? '' ) );
				if ( strlen( $room ) < 4 || strlen( $room ) > 24 ) {
					return new WP_REST_Response( array( 'ok' => false ), 400 );
				}
				// broadcast throttle: 2/sec per room is plenty
				$tk = 'nlct_rl_' . md5( $room );
				if ( (int) get_transient( $tk ) > 8 ) { return new WP_REST_Response( array( 'ok' => false, 'throttled' => true ), 429 ); }
				set_transient( $tk, (int) get_transient( $tk ) + 1, 3 );
				$state = array(
					'p' => sanitize_text_field( (string) ( $p['state']['p'] ?? '' ) ),
					'u' => sanitize_text_field( (string) ( $p['state']['u'] ?? '' ) ),
					'o' => sanitize_text_field( (string) ( $p['state']['o'] ?? '' ) ),
					'l' => sanitize_text_field( (string) ( $p['state']['l'] ?? '' ) ),
					'f' => sanitize_text_field( (string) ( $p['state']['f'] ?? '' ) ),
					'v' => sanitize_text_field( (string) ( $p['state']['v'] ?? '' ) ),
					't' => time(),
				);
				set_transient( 'nlct_' . md5( $room ), $state, 5 * MINUTE_IN_SECONDS );
				return new WP_REST_Response( array( 'ok' => true ), 200 );
			},
		),
		array(
			'methods' => 'GET', 'permission_callback' => '__return_true',
			'callback' => function ( WP_REST_Request $req ) {
				$room = preg_replace( '/[^a-z0-9]/i', '', (string) $req->get_param( 'room' ) );
				$st   = get_transient( 'nlct_' . md5( $room ) );
				return new WP_REST_Response( array( 'ok' => (bool) $st, 'state' => $st ?: null ), 200 );
			},
		),
	) );
} );
