<?php
/**
 * HAD-256 staged proof, stage 2 of 3: the single-connection row-count checks behind the build lock, the one-listing
 * rule, the fenced status and the draft compare-and-swap of snapshot 3 / 2.0.1 (x-broker-drop 1.1.4 lines 2070, 2079,
 * 2106, 2113, 2143-2145, 2157, 2165, 2203; x-owner-wizard lines 359, 924, 960, 1218-1219, 1388-1391): the same statement
 * texts, run on rows this stage creates and deletes itself.
 *
 * Install as a temporary Code Snippet (body = this file without the opening tag), __TOKEN__ replaced by a fresh token;
 * POST /wp-json/nadlan-h256c/v1/s2 {"token": TOKEN} as an administrator; then deactivate and delete the snippet.
 * Body options:
 *   "groups": [1,2,...]   run only these groups (their prerequisites are added); default 1-9. 0 (setup) always runs.
 *                         1 lock, 2 fenced commit, 3 takeover, 4 fenced status, 5 one post per language,
 *                         6 draft compare-and-swap, 7 create key, 8 photo slot, 9 release
 *   "enc": 0              a readable answer; default 1 = the whole answer as one base64 field "b64"
 *   "verbose": 1          add the database's own error text next to each error number
 * Touches only: one wp_posts row (post_type nl_had256_probe, status draft then pending, inserted without hooks), its
 * wp_postmeta rows, and five wp_options rows named after that row's id and a random run id (autoload no). All deleted in
 * finally and counted again ("cleanup", every count must be 0). Database errors are suppressed for the run and reported
 * as numbers. No credential constant is read.
 */
if ( ! function_exists( 'nl_h256c_s2_run' ) ) {
	function nl_h256c_s2_run( $b ) {
		global $wpdb;
		$t0   = microtime( true );
		$verb = ! empty( $b['verbose'] );
		$run  = substr( bin2hex( random_bytes( 8 ) ), 0, 12 );
		$out  = array( 'kit' => 'h256c-s2 v1', 'run' => $run, 'at_gmt' => gmdate( 'c' ), 'checks' => array(), 'info' => array(), 'errors' => array() );
		$fail = 0;
		$want = isset( $b['groups'] ) ? array_map( 'intval', (array) $b['groups'] ) : range( 1, 9 );
		$deps = array( 2 => array( 1 ), 3 => array( 1, 2 ), 4 => array( 1, 2, 3 ), 9 => array( 1, 2, 3 ) );
		foreach ( $want as $g ) { if ( isset( $deps[ $g ] ) ) { $want = array_merge( $want, $deps[ $g ] ); } }
		$want = array_values( array_unique( $want ) );
		sort( $want );
		$out['groups'] = $want;
		$errno = function () use ( $wpdb ) {
			$h = $wpdb->dbh;
			return ( $h instanceof mysqli ) ? (int) mysqli_errno( $h ) : -1;
		};
		$check = function ( $id, $got, $expect, $note = '' ) use ( &$out, &$fail ) {
			$ok = is_array( $expect ) ? in_array( $got, $expect, true ) : ( $got === $expect );
			if ( ! $ok ) { $fail++; }
			$out['checks'][ $id ] = array( 'got' => $got, 'expect' => $expect, 'pass' => $ok ) + ( '' !== $note ? array( 'note' => $note ) : array() );
		};
		// a statement's row count, or "refused" with the error number when the database answered an error
		$n = function ( $label, $res ) use ( $wpdb, &$out, $errno, $verb ) {
			if ( false === $res || '' !== (string) $wpdb->last_error ) {
				$out['errors'][ $label ] = array( 'no' => $errno() ) + ( $verb ? array( 'text' => substr( (string) $wpdb->last_error, 0, 200 ) ) : array() );
				return 'refused';
			}
			return (int) $res;
		};
		$prev  = $wpdb->suppress_errors( true );
		$probe = 0;
		$names = array();
		try {
			/* ---- group 0: the throwaway post row (unregistered type, never public), written without any hook ---- */
			$now = current_time( 'mysql' );
			$gmt = current_time( 'mysql', true );
			$ok  = $wpdb->insert( $wpdb->posts, array(
				'post_author' => (int) get_current_user_id(), 'post_date' => $now, 'post_date_gmt' => $gmt, 'post_content' => '', 'post_title' => 'had256-probe-' . $run,
				'post_excerpt' => '', 'post_status' => 'draft', 'comment_status' => 'closed', 'ping_status' => 'closed', 'post_password' => '', 'post_name' => 'had256-probe-' . $run,
				'to_ping' => '', 'pinged' => '', 'post_modified' => $now, 'post_modified_gmt' => $gmt, 'post_content_filtered' => '', 'post_parent' => 0, 'guid' => '',
				'menu_order' => 0, 'post_type' => 'nl_had256_probe', 'post_mime_type' => '', 'comment_count' => 0,
			) );
			$probe = 1 === $ok ? (int) $wpdb->insert_id : 0;
			$check( 'g0.probe_row', $probe > 0, true );
			if ( $probe <= 0 ) {
				$out['errors']['g0'] = array( 'no' => $errno() );
				throw new Exception( 'no probe row' );
			}
			$out['info']['probe'] = $probe;
			$lock  = 'nl_drop_lock_' . $probe;          $names[] = $lock;
			$pub   = 'nl_pub_' . $probe . '_he';         $names[] = $pub;
			$att   = 'nl_att_had256probe' . $run;        $names[] = $att;
			$ck    = 'nl_owner_ck_' . md5( 'had256probe|' . $run ); $names[] = $ck;
			$S     = array();

			// the statement texts of the live code (only the values are probe values)
			$add   = function ( $name, $val ) use ( $wpdb ) { return $wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO {$wpdb->options} (option_name, option_value, autoload) VALUES (%s, %s, 'no')", $name, $val ) ); };
			$read  = function ( $name ) use ( $wpdb ) { return $wpdb->get_var( $wpdb->prepare( "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s LIMIT 1", $name ) ); };
			$stamp = function ( $val, $name, $seed ) use ( $wpdb ) { return $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->options} SET option_value = %s WHERE option_name = %s AND option_value = %s", $val, $name, $seed ) ); };
			$cad   = function ( $name, $raw ) use ( $wpdb ) { return $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s", $name, $raw ) ); };
			$fence = function ( $value, $drop_id, $key, $mine ) use ( $wpdb ) {
				return $wpdb->query( $wpdb->prepare(
					"UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = %s AND EXISTS ( SELECT 1 FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s )",
					maybe_serialize( $value ), $drop_id, $key, 'nl_drop_lock_' . $drop_id, $mine
				) );
			};
			$meta  = function ( $key ) use ( $wpdb, $probe ) { return $wpdb->get_var( $wpdb->prepare( "SELECT meta_value FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key = %s ORDER BY meta_id ASC LIMIT 1", $probe, $key ) ); };
			$lv    = function ( $who, $tok ) { return wp_json_encode( array( 'who' => $who, 't' => time(), 'tok' => $tok, 'r' => wp_generate_password( 12, false, false ) ) ); };

			if ( in_array( 1, $want, true ) ) {   // the build lock: one row per name, the winner stamps its own seed
				$S['seedA'] = $lv( 'had256:A', 0 );
				$S['seedB'] = $lv( 'had256:B', 0 );
				$check( 'g1.first_writer', $n( 'g1a', $add( $lock, $S['seedA'] ) ), 1 );
				$check( 'g1.second_writer', $n( 'g1b', $add( $lock, $S['seedB'] ) ), 0 );
				$check( 'g1.row_is_first', $read( $lock ) === $S['seedA'], true );
				$S['valA'] = $lv( 'had256:A', 1 );
				$check( 'g1.stamp_own_seed', $n( 'g1c', $stamp( $S['valA'], $lock, $S['seedA'] ) ), 1 );
				$check( 'g1.stamp_stale_seed', $n( 'g1d', $stamp( $S['seedB'], $lock, $S['seedA'] ) ), 0 );
				$check( 'g1.row_after_stamp', $read( $lock ) === $S['valA'], true );
			}
			if ( in_array( 2, $want, true ) ) {   // the commit, fenced by the lock row
				$wpdb->insert( $wpdb->postmeta, array( 'post_id' => $probe, 'meta_key' => 'nl_result', 'meta_value' => '' ) );
				$S['resA'] = array( 'he_id' => 1, 'state' => 'publish', 'run' => 'A' );
				$check( 'g2.own_lock', $n( 'g2a', $fence( $S['resA'], $probe, 'nl_result', $S['valA'] ) ), 1 );
				$same = $n( 'g2b', $fence( $S['resA'], $probe, 'nl_result', $S['valA'] ) );
				$check( 'g2.same_value', $same, array( 0, 1 ), 'MySQL/MariaDB count changed rows (0); the code then re-checks its fence' );
				$out['info']['same_value_rows'] = $same;
				$check( 'g2.stale_token', $n( 'g2c', $fence( array( 'he_id' => 2 ), $probe, 'nl_result', $S['seedA'] ) ), 0, 'MUST be 0' );
				$check( 'g2.value_kept', $meta( 'nl_result' ) === maybe_serialize( $S['resA'] ), true );
			}
			if ( in_array( 3, $want, true ) ) {   // takeover after the TTL: compare-and-remove, then a fresh first writer
				$check( 'g3.remove_with_old_value', $n( 'g3a', $cad( $lock, $S['seedA'] ) ), 0 );
				$check( 'g3.remove_with_current_value', $n( 'g3b', $cad( $lock, $S['valA'] ) ), 1 );
				$S['seedC'] = $lv( 'had256:C', 0 );
				$check( 'g3.taker_writes', $n( 'g3c', $add( $lock, $S['seedC'] ) ), 1 );
				$check( 'g3.second_taker', $n( 'g3d', $add( $lock, $S['seedB'] ) ), 0 );
				$S['valC'] = $lv( 'had256:C', 2 );
				$check( 'g3.taker_stamps', $n( 'g3e', $stamp( $S['valC'], $lock, $S['seedC'] ) ), 1 );
				$check( 'g3.old_holder_commit', $n( 'g3f', $fence( array( 'he_id' => 3 ), $probe, 'nl_result', $S['valA'] ) ), 0, 'MUST be 0' );
				$check( 'g3.new_holder_commit', $n( 'g3g', $fence( array( 'he_id' => 1, 'run' => 'C' ), $probe, 'nl_result', $S['valC'] ) ), 1 );
			}
			if ( in_array( 4, $want, true ) ) {   // the status, fenced the same way; the probe never becomes public
				$st  = function ( $status, $slug, $first, $he, $drop_id, $mine ) use ( $wpdb ) {
					$now = current_time( 'mysql' );
					$gmt = current_time( 'mysql', true );
					return $wpdb->query( $wpdb->prepare(
						"UPDATE {$wpdb->posts} SET post_status = %s, post_name = %s, post_modified = %s, post_modified_gmt = %s" . ( $first ? ', post_date = %s, post_date_gmt = %s' : '' ) .
						" WHERE ID = %d AND EXISTS ( SELECT 1 FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s )",
						array_merge( array( $status, $slug, $now, $gmt ), $first ? array( $now, $gmt ) : array(), array( $he, 'nl_drop_lock_' . $drop_id, $mine ) )
					) );
				};
				$now_st = function () use ( $wpdb, $probe ) { return (string) $wpdb->get_var( $wpdb->prepare( "SELECT post_status FROM {$wpdb->posts} WHERE ID = %d", $probe ) ); };
				$check( 'g4.old_holder_first_shape', $n( 'g4a', $st( 'publish', 'had256-probe-' . $run, true, $probe, $probe, $S['valA'] ) ), 0, 'MUST be 0' );
				$check( 'g4.old_seed_plain_shape', $n( 'g4b', $st( 'publish', 'had256-probe-' . $run, false, $probe, $probe, $S['seedA'] ) ), 0, 'MUST be 0' );
				$check( 'g4.still_draft', $now_st(), 'draft' );
				$check( 'g4.holder_first_shape', $n( 'g4c', $st( 'pending', 'had256-probe-' . $run, true, $probe, $probe, $S['valC'] ) ), 1 );
				$check( 'g4.now_pending', $now_st(), 'pending' );
			}
			if ( in_array( 5, $want, true ) ) {   // one post per drop and language
				$check( 'g5.first', $n( 'g5a', $add( $pub, wp_json_encode( array( 'post' => 111, 'tok' => 2, 't' => time() ) ) ) ), 1 );
				$check( 'g5.second', $n( 'g5b', $add( $pub, wp_json_encode( array( 'post' => 222, 'tok' => 3, 't' => time() ) ) ) ), 0 );
				$cj = json_decode( (string) $read( $pub ), true );
				$check( 'g5.read_first_post', is_array( $cj ) ? (int) ( $cj['post'] ?? 0 ) : 0, 111 );
			}
			if ( in_array( 6, $want, true ) ) {   // the draft compare-and-swap
				$cas = function ( $json, $id, $old_raw ) use ( $wpdb ) { return $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = 'nl_draft' AND meta_value = %s", $json, (int) $id, (string) $old_raw ) ); };
				$enc = function ( $a ) { return wp_json_encode( $a, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); };
				$r1  = $enc( array( 'v' => 2, 'rev' => 1, 'fields' => array( 'city' => 'תל אביב יפו', 'desc' => 'tel aviv, קומה 3' ), 'photos' => array(), 'step' => 'details', 'saved_at' => time() ) );
				$wpdb->insert( $wpdb->postmeta, array( 'post_id' => $probe, 'meta_key' => 'nl_draft', 'meta_value' => $r1 ) );
				$r2  = $enc( array( 'v' => 2, 'rev' => 2, 'fields' => array( 'city' => 'תל אביב יפו', 'desc' => 'Tel Aviv, קומה 3' ), 'photos' => array(), 'step' => 'details', 'saved_at' => time() ) );
				$check( 'g6.fresh_text', $n( 'g6a', $cas( $r2, $probe, $r1 ) ), 1 );
				$r3  = $enc( array( 'v' => 2, 'rev' => 2, 'fields' => array( 'city' => 'x' ), 'photos' => array(), 'step' => 'details', 'saved_at' => time() ) );
				$check( 'g6.stale_text', $n( 'g6b', $cas( $r3, $probe, $r1 ) ), 0, 'MUST be 0' );
				$check( 'g6.value_kept', $meta( 'nl_draft' ) === $r2, true );
				$r2c = str_replace( 'Tel Aviv', 'TEL AVIV', $r2 );
				$r4  = $enc( array( 'v' => 2, 'rev' => 3, 'fields' => array( 'city' => 'probe' ), 'photos' => array(), 'step' => 'details', 'saved_at' => time() ) );
				$ci  = $n( 'g6c', $cas( $r4, $probe, $r2c ) );
				$out['info']['compare_ignores_case'] = 1 === $ci;
				$check( 'g6.case_only_difference', $ci, array( 0, 1 ), '1 = a _ci collation; harmless, every save bumps rev' );
				if ( 1 === $ci ) { $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = 'nl_draft'", $r2, $probe ) ); }
				$r5  = $enc( array( 'v' => 2, 'rev' => 3, 'fields' => array( 'desc' => 'מרפסת 🌅 לים' ), 'photos' => array(), 'step' => 'details', 'saved_at' => time() ) );
				$check( 'g6.four_byte_char', $n( 'g6d', $cas( $r5, $probe, $r2 ) ), 1, 'refused = the column is not utf8mb4' );
				$check( 'g6.four_byte_roundtrip', $meta( 'nl_draft' ) === $r5, true );
				$big = $enc( array( 'v' => 2, 'rev' => 4, 'fields' => array( 'desc' => str_repeat( 'דירה מוארת עם מרפסת. ', 600 ) ), 'photos' => array_fill( 0, 30, array( 'ref' => str_repeat( 'a', 32 ) ) ), 'step' => 'photos', 'saved_at' => time() ) );
				$check( 'g6.large_text', $n( 'g6e', $cas( $big, $probe, $r5 ) ), 1, strlen( $big ) . ' bytes' );
				$check( 'g6.large_text_stale', $n( 'g6f', $cas( $r5, $probe, $r5 ) ), 0 );
			}
			if ( in_array( 7, $want, true ) ) {   // the create key: a double tap is the same draft
				$check( 'g7.first', $n( 'g7a', $add( $ck, 'pending|' . time() ) ), 1 );
				$check( 'g7.double_tap', $n( 'g7b', $add( $ck, 'pending|' . time() ) ), 0 );
				$check( 'g7.resolve', $n( 'g7c', $wpdb->update( $wpdb->options, array( 'option_value' => $probe . '|' . time() ), array( 'option_name' => $ck ) ) ), 1 );
			}
			if ( in_array( 8, $want, true ) ) {   // a photo's attachment slot
				$add( $att, 'pending' );
				$rm = function () use ( $wpdb, $att ) { return $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s AND option_value NOT LIKE %s", $att, '%"att":%' ) ); };
				$check( 'g8.clear_unfinished', $n( 'g8a', $rm() ), 1 );
				$check( 'g8.first', $n( 'g8b', $add( $att, wp_json_encode( array( 'att' => 333, 't' => time() ) ) ) ), 1 );
				$check( 'g8.finished_kept', $n( 'g8c', $rm() ), 0 );
				$check( 'g8.second', $n( 'g8d', $add( $att, wp_json_encode( array( 'att' => 444, 't' => time() ) ) ) ), 0 );
			}
			if ( in_array( 9, $want, true ) ) {   // release: only the holder's own value goes
				$check( 'g9.old_value', $n( 'g9a', $cad( $lock, $S['valA'] ) ), 0 );
				$check( 'g9.own_value', $n( 'g9b', $cad( $lock, $S['valC'] ) ), 1 );
			}
		} catch ( Throwable $e ) {
			$fail++;
			$out['thrown'] = get_class( $e ) . ( $verb ? ': ' . substr( $e->getMessage(), 0, 200 ) : '' );
		} finally {
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
	register_rest_route( 'nadlan-h256c/v1', '/s2', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => function ( $req ) {
			$b   = $req->get_json_params();
			$tok = '__TOKEN__';
			if ( $tok === '__' . 'TOKEN__' || ! is_array( $b ) || ! hash_equals( $tok, (string) ( $b['token'] ?? '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$r = nl_h256c_s2_run( $b );
			if ( ! isset( $b['enc'] ) || ! empty( $b['enc'] ) ) { $r = array( 'b64' => base64_encode( (string) wp_json_encode( $r ) ) ); }
			return new WP_REST_Response( $r, 200, array( 'Cache-Control' => 'no-store' ) );
		},
	) );
} );
