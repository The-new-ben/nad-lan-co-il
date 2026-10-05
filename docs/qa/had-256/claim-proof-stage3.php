<?php
/**
 * HAD-256 staged proof, stage 3 of 3: a SECOND database connection (another PHP worker, in effect) sees the same
 * one-row-per-name rule and the same fenced commit as WordPress' own connection.
 *
 * Install as a temporary Code Snippet (body = this file without the opening tag), __TOKEN__ replaced by a fresh token;
 * POST /wp-json/nadlan-h256c/v1/s3 {"token": TOKEN} as an administrator; then deactivate and delete the snippet.
 * Body options: "enc": 0 for a readable answer (default 1 = one base64 field "b64"); "verbose": 1 adds error texts of
 * WordPress' own connection (never of the second one: a connect error can name the database user).
 * The second connection: plain mysqli, reporting off, a 5 s connect timeout, prepared statements. The connection
 * constants are passed to mysqli_real_connect() and to nothing else: never echoed, logged or put in the answer; only a
 * connect error NUMBER is reported. Touches only one throwaway wp_posts row (post_type nl_had256_probe, draft, no
 * hooks), its wp_postmeta row and two wp_options rows named after it and a random run id; all deleted in finally and
 * counted again ("cleanup", every count must be 0).
 */
if ( ! function_exists( 'nl_h256c_s3_run' ) ) {
	function nl_h256c_s3_run( $b ) {
		global $wpdb;
		$t0   = microtime( true );
		$verb = ! empty( $b['verbose'] );
		$run  = substr( bin2hex( random_bytes( 8 ) ), 0, 12 );
		$out  = array( 'kit' => 'h256c-s3 v1', 'run' => $run, 'at_gmt' => gmdate( 'c' ), 'checks' => array(), 'info' => array(), 'errors' => array() );
		$fail = 0;
		$check = function ( $id, $got, $expect, $note = '' ) use ( &$out, &$fail ) {
			$ok = ( $got === $expect );
			if ( ! $ok ) { $fail++; }
			$out['checks'][ $id ] = array( 'got' => $got, 'expect' => $expect, 'pass' => $ok ) + ( '' !== $note ? array( 'note' => $note ) : array() );
		};
		$errno = function () use ( $wpdb ) {
			$h = $wpdb->dbh;
			return ( $h instanceof mysqli ) ? (int) mysqli_errno( $h ) : -1;
		};
		$n1 = function ( $label, $res ) use ( $wpdb, &$out, $errno, $verb ) {
			if ( false === $res || '' !== (string) $wpdb->last_error ) {
				$out['errors'][ $label ] = array( 'no' => $errno() ) + ( $verb ? array( 'text' => substr( (string) $wpdb->last_error, 0, 200 ) ) : array() );
				return 'refused';
			}
			return (int) $res;
		};
		$prev  = $wpdb->suppress_errors( true );
		$probe = 0;
		$names = array();
		$c2    = null;
		try {
			$now = current_time( 'mysql' );
			$gmt = current_time( 'mysql', true );
			$ok  = $wpdb->insert( $wpdb->posts, array(
				'post_author' => (int) get_current_user_id(), 'post_date' => $now, 'post_date_gmt' => $gmt, 'post_content' => '', 'post_title' => 'had256-probe-' . $run,
				'post_excerpt' => '', 'post_status' => 'draft', 'comment_status' => 'closed', 'ping_status' => 'closed', 'post_password' => '', 'post_name' => 'had256-probe-' . $run,
				'to_ping' => '', 'pinged' => '', 'post_modified' => $now, 'post_modified_gmt' => $gmt, 'post_content_filtered' => '', 'post_parent' => 0, 'guid' => '',
				'menu_order' => 0, 'post_type' => 'nl_had256_probe', 'post_mime_type' => '', 'comment_count' => 0,
			) );
			$probe = 1 === $ok ? (int) $wpdb->insert_id : 0;
			$check( 'probe_row', $probe > 0, true );
			if ( $probe <= 0 ) { throw new Exception( 'no probe row' ); }
			$lock = 'nl_drop_lock_' . $probe;            $names[] = $lock;
			$x    = 'nl_had256probe_x_' . $run;           $names[] = $x;
			$mine = wp_json_encode( array( 'who' => 'had256:A', 't' => time(), 'tok' => 1, 'r' => wp_generate_password( 12, false, false ) ) );
			$old  = wp_json_encode( array( 'who' => 'had256:A', 't' => time(), 'tok' => 0, 'r' => wp_generate_password( 12, false, false ) ) );
			$wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO {$wpdb->options} (option_name, option_value, autoload) VALUES (%s, %s, 'no')", $lock, $mine ) );
			$wpdb->insert( $wpdb->postmeta, array( 'post_id' => $probe, 'meta_key' => 'nl_result', 'meta_value' => '' ) );

			// the second connection
			$out['info']['conn2'] = 'not opened';
			if ( function_exists( 'mysqli_init' ) && defined( 'DB_HOST' ) && defined( 'DB_USER' ) && defined( 'DB_PASSWORD' ) && defined( 'DB_NAME' ) && method_exists( $wpdb, 'parse_db_host' ) ) {
				mysqli_report( MYSQLI_REPORT_OFF );
				$hp = $wpdb->parse_db_host( DB_HOST );
				if ( is_array( $hp ) ) {
					$c2 = mysqli_init();
					@mysqli_options( $c2, MYSQLI_OPT_CONNECT_TIMEOUT, 5 );
					$host = (string) $hp[0];
					$port = ! empty( $hp[1] ) ? (int) $hp[1] : null;
					$sock = ! empty( $hp[2] ) ? (string) $hp[2] : null;
					if ( ! @mysqli_real_connect( $c2, $host, DB_USER, DB_PASSWORD, DB_NAME, $port, $sock ) ) {
						$out['info']['conn2_errno'] = (int) mysqli_connect_errno();
						$c2 = null;
					} else {
						@mysqli_set_charset( $c2, '' !== (string) $wpdb->charset ? (string) $wpdb->charset : 'utf8mb4' );
						$out['info']['conn2'] = 'open';
					}
				}
			}
			if ( $c2 ) {
				$run2 = function ( $q, $types, $vals ) use ( $c2 ) {
					$st = mysqli_prepare( $c2, $q );
					if ( ! $st ) { return 'prep_errno_' . (int) mysqli_errno( $c2 ); }
					mysqli_stmt_bind_param( $st, $types, ...$vals );
					$okx = mysqli_stmt_execute( $st );
					$r   = $okx ? (int) mysqli_stmt_affected_rows( $st ) : 'errno_' . (int) mysqli_stmt_errno( $st );
					mysqli_stmt_close( $st );
					return $r;
				};
				$add2 = "INSERT IGNORE INTO {$wpdb->options} (option_name, option_value, autoload) VALUES (?, ?, 'no')";
				$fen2 = "UPDATE {$wpdb->postmeta} SET meta_value = ? WHERE post_id = ? AND meta_key = ? AND EXISTS ( SELECT 1 FROM {$wpdb->options} WHERE option_name = ? AND option_value = ? )";
				$check( 'conn2.first_writer', $run2( $add2, 'ss', array( $x, 'conn2' ) ), 1 );
				$check( 'conn1.second_writer', $n1( 'c1a', $wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO {$wpdb->options} (option_name, option_value, autoload) VALUES (%s, %s, 'no')", $x, 'conn1' ) ) ), 0 );
				$check( 'conn2.third_writer', $run2( $add2, 'ss', array( $x, 'conn2-again' ) ), 0 );
				$check( 'conn1.reads_conn2_row', (string) $wpdb->get_var( $wpdb->prepare( "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s LIMIT 1", $x ) ), 'conn2' );
				$check( 'conn2.commit_old_token', $run2( $fen2, 'sisss', array( maybe_serialize( array( 'run' => 'conn2-old' ) ), $probe, 'nl_result', $lock, $old ) ), 0, 'MUST be 0' );
				$check( 'conn2.commit_own_token', $run2( $fen2, 'sisss', array( maybe_serialize( array( 'run' => 'conn2-own' ) ), $probe, 'nl_result', $lock, $mine ) ), 1, 'the positive control' );
				$check( 'conn1.reads_conn2_commit', (string) $wpdb->get_var( $wpdb->prepare( "SELECT meta_value FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key = 'nl_result' LIMIT 1", $probe ) ), maybe_serialize( array( 'run' => 'conn2-own' ) ) );
				$check( 'conn1.commit_old_token', $n1( 'c1b', $wpdb->query( $wpdb->prepare(
					"UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = %s AND EXISTS ( SELECT 1 FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s )",
					maybe_serialize( array( 'run' => 'conn1-old' ) ), $probe, 'nl_result', $lock, $old
				) ) ), 0, 'MUST be 0' );
			} else {
				$fail++;
				$out['checks']['conn2.opened'] = array( 'got' => false, 'expect' => true, 'pass' => false );
			}
		} catch ( Throwable $e ) {
			$fail++;
			$out['thrown'] = get_class( $e );
		} finally {
			if ( $c2 ) { @mysqli_close( $c2 ); $c2 = null; }
			foreach ( $names as $nm ) {
				$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s", $nm ) );
				wp_cache_delete( $nm, 'options' );
			}
			if ( $probe > 0 ) {
				$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->postmeta} WHERE post_id = %d", $probe ) );
				$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->posts} WHERE ID = %d AND post_type = 'nl_had256_probe'", $probe ) );
				wp_cache_delete( $probe, 'posts' );
				wp_cache_delete( $probe, 'post_meta' );
			}
			wp_cache_delete( 'notoptions', 'options' );
			$left = 0;
			foreach ( $names as $nm ) { $left += (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->options} WHERE option_name = %s", $nm ) ); }
			$out['cleanup'] = array(
				'options_left'  => $left,
				'postmeta_left' => $probe > 0 ? (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE post_id = %d", $probe ) ) : 0,
				'posts_left'    => $probe > 0 ? (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->posts} WHERE ID = %d", $probe ) ) : 0,
				'probe_type_anywhere' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = 'nl_had256_probe'" ),
			);
			if ( 0 !== array_sum( $out['cleanup'] ) ) { $fail++; }
			$wpdb->suppress_errors( $prev );
		}
		$out['failures'] = $fail;
		$out['all_pass'] = 0 === $fail;
		$out['ms']       = (int) round( ( microtime( true ) - $t0 ) * 1000 );
		return $out;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-h256c/v1', '/s3', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => function ( $req ) {
			$b   = $req->get_json_params();
			$tok = '__TOKEN__';
			if ( $tok === '__' . 'TOKEN__' || ! is_array( $b ) || ! hash_equals( $tok, (string) ( $b['token'] ?? '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$r = nl_h256c_s3_run( $b );
			if ( ! isset( $b['enc'] ) || ! empty( $b['enc'] ) ) { $r = array( 'b64' => base64_encode( (string) wp_json_encode( $r ) ) ); }
			return new WP_REST_Response( $r, 200, array( 'Cache-Control' => 'no-store' ) );
		},
	) );
} );
