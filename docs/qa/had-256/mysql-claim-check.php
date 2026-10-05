<?php
/**
 * HAD-256 · MySQL / MariaDB proof kit for the atomic claim and the conditional updates (open item 1).
 *
 * WHY: every bench run so far was on SQLite (WordPress Playground). The release needs one proof, on the live database
 * engine, that the statements snapshot 3 (code 2ce0a741) relies on give the row counts the code expects:
 *   - INSERT IGNORE on wp_options.option_name (the build lock, the listing claim, the photo claim, the create key):
 *     1 for the winner, 0 for every later caller (also from a second connection);
 *   - the conditional UPDATEs (stamp, fenced meta, fenced status, draft compare-and-swap) and the compare-and-delete:
 *     1 while the caller's own lock row / read text is there, 0 with a stale token or a stale text.
 * It also reports what differs from SQLite and matters to the code: MySQL counts CHANGED rows (a same-value UPDATE is 0,
 * the code re-checks the fence then), the comparison collation of option_value / meta_value (a *_ci collation ignores
 * case: the code never relies on case, every write bumps a number in the text), and the column charset (a 4-byte
 * character, e.g. an emoji in a description, needs utf8mb4).
 *
 * WHAT IT TOUCHES: only rows it creates and deletes itself, named after one random run id and one new probe post:
 *   wp_posts      one row, post_type 'nl_had256_probe', status draft/pending (unregistered type: never listed, never
 *                 public; inserted with $wpdb->insert, so no save_post / transition hook runs);
 *   wp_postmeta   rows of that probe post only;
 *   wp_options    'nl_drop_lock_<probe id>', 'nl_pub_<probe id>_he', 'nl_att_had256probe<run>', 'nl_owner_ck_<md5 run>',
 *                 'nl_had256probe_x_<run>' (autoload 'no').
 * Everything is deleted in a finally block and counted again (cleanup.* must all be 0). No real user, drop, listing,
 * option or cache entry is read or written. Nothing is printed except the JSON report (no credentials, no paths).
 *
 * HOW MAIN RUNS IT ONCE (the deploydrop.py / deploy4xx bridge pattern):
 *   1. code = this file without the opening "<?php", with __TOKEN__ replaced by a fresh secrets.token_hex(24);
 *   2. POST /wp-json/code-snippets/v1/snippets {name: "tmp-had256-mysql-<ts>", code, scope: "global", active: false},
 *      lint first through the existing bridge op (token_get_all) if the runner has one, then PUT .../<id>/activate;
 *   3. POST /wp-json/nadlan-had256-ops/v1/mysql-claim-check {"token": TOKEN} (application password of an admin);
 *      save the JSON answer as docs/qa/had-256/mysql-claim-check.result.json; it must say "all_pass": true;
 *   4. PUT .../<id>/deactivate, DELETE .../<id>, then POST the route again: 404 (the bridge is gone).
 *   The route answers only an administrator (manage_options) AND the token; with __TOKEN__ left unreplaced it refuses.
 * Or: include the function in any existing admin-only bridge callback and return nl_had256_mysql_claim_check().
 *
 * SOURCE LINES (snapshot 3 = 2ce0a741; file:line, verbatim):
 *   broker-drop.php:2079  $n = $wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO {$wpdb->options} (option_name, option_value, autoload) VALUES (%s, %s, 'no')", $name, $val ) );
 *   broker-drop.php:2106  $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s", $name, $cur['raw'] ) );
 *   broker-drop.php:2113  $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->options} SET option_value = %s WHERE option_name = %s AND option_value = %s", $val, $name, $seed ) );
 *   broker-drop.php:2143  $n = $wpdb->query( $wpdb->prepare(
 *   broker-drop.php:2144      "UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = %s AND EXISTS ( SELECT 1 FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s )",
 *   broker-drop.php:2145      maybe_serialize( $value ), $drop_id, $key, 'nl_drop_lock_' . $drop_id, $mine
 *   broker-drop.php:2157  $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s", $name, $GLOBALS['nl_drop_locks'][ $drop_id ]['val'] ) );
 *   broker-drop.php:2070  $raw = $wpdb->get_var( $wpdb->prepare( "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s LIMIT 1", 'nl_drop_lock_' . (int) $drop_id ) );
 *   broker-drop.php:2165  $raw = $wpdb->get_var( $wpdb->prepare( "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s LIMIT 1", 'nl_pub_' . (int) $drop_id . '_' . nl_drop_L( $lang ) ) );
 *   broker-drop.php:2203  if ( nl_drop_lock_insert( 'nl_pub_' . $drop_id . '_' . nl_drop_L( $lang ), wp_json_encode( array( 'post' => (int) $ph, 'tok' => $tok, 't' => time() ) ) ) ) {
 *   owner-wizard.php:359  $n    = $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = 'nl_draft' AND meta_value = %s", $json, (int) $id, (string) $old_raw ) );
 *   owner-wizard.php:924  if ( ! nl_drop_lock_insert( $name, 'pending|' . time() ) ) {
 *   owner-wizard.php:960  $wpdb->update( $wpdb->options, array( 'option_value' => $id . '|' . time() ), array( 'option_name' => $name ) );
 *   owner-wizard.php:1218 $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s AND option_value NOT LIKE %s", 'nl_att_' . $ref, '%"att":%' ) );
 *   owner-wizard.php:1219 nl_drop_lock_insert( 'nl_att_' . $ref, wp_json_encode( array( 'att' => (int) $ph, 't' => time() ) ) );
 *   owner-wizard.php:1388 $n = $wpdb->query( $wpdb->prepare(
 *   owner-wizard.php:1389     "UPDATE {$wpdb->posts} SET post_status = %s, post_name = %s, post_modified = %s, post_modified_gmt = %s" . ( $first ? ', post_date = %s, post_date_gmt = %s' : '' ) .
 *   owner-wizard.php:1390     " WHERE ID = %d AND EXISTS ( SELECT 1 FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s )",
 *   owner-wizard.php:1391     array_merge( array( $status, $slug, $now, $gmt ), $first ? array( $now, $gmt ) : array(), array( $he, 'nl_drop_lock_' . $drop_id, $mine ) )
 * The kit runs these statement texts unchanged (the SQL strings below are copied, only the values are probe values).
 */

if ( ! function_exists( 'nl_had256_mysql_claim_check' ) ) {
	function nl_had256_mysql_claim_check() {
		global $wpdb;
		$t0    = microtime( true );
		$run   = substr( bin2hex( random_bytes( 8 ) ), 0, 12 );
		$rep   = array( 'kit' => 'had256-mysql-claim-check v1', 'snapshot' => '2ce0a741', 'run' => $run, 'at_gmt' => gmdate( 'c' ), 'checks' => array(), 'info' => array() );
		$fail  = 0;
		$check = function ( $id, $got, $want, $note = '' ) use ( &$rep, &$fail ) {
			$ok = is_array( $want ) ? in_array( $got, $want, true ) : ( $got === $want );
			if ( ! $ok ) { $fail++; }
			$rep['checks'][ $id ] = array( 'got' => $got, 'want' => $want, 'pass' => $ok ) + ( $note !== '' ? array( 'note' => $note ) : array() );
			return $ok;
		};
		$rows = function ( $n ) { return false === $n ? 'false (query refused: ' . (string) $GLOBALS['wpdb']->last_error . ')' : (int) $n; };

		// the engine
		$rep['info']['server_version'] = (string) $wpdb->get_var( 'SELECT VERSION()' );
		$rep['info']['version_comment'] = (string) $wpdb->get_var( 'SELECT @@version_comment' );
		$rep['info']['db_server_info']  = method_exists( $wpdb, 'db_server_info' ) ? (string) $wpdb->db_server_info() : '';
		$rep['info']['autocommit']      = (string) $wpdb->get_var( 'SELECT @@autocommit' );
		$iso = $wpdb->get_var( 'SELECT @@transaction_isolation' );
		if ( null === $iso ) { $iso = $wpdb->get_var( 'SELECT @@tx_isolation' ); }
		$rep['info']['isolation']       = (string) $iso;
		$rep['info']['sql_mode']        = (string) $wpdb->get_var( 'SELECT @@SESSION.sql_mode' );
		$rep['info']['wpdb_charset']    = (string) $wpdb->charset . ' / ' . (string) $wpdb->collate;
		$rep['info']['ext_object_cache'] = function_exists( 'wp_using_ext_object_cache' ) ? (bool) wp_using_ext_object_cache() : null;
		foreach ( array( 'options' => $wpdb->options, 'postmeta' => $wpdb->postmeta, 'posts' => $wpdb->posts ) as $k => $tbl ) {
			$st = $wpdb->get_row( $wpdb->prepare( 'SHOW TABLE STATUS LIKE %s', $tbl ), ARRAY_A );
			$rep['info'][ 'engine_' . $k ] = $st ? (string) $st['Engine'] . ' / ' . (string) $st['Collation'] : 'unknown';
		}
		$col = function ( $tbl, $c ) use ( $wpdb ) {
			$r = $wpdb->get_row( "SHOW FULL COLUMNS FROM {$tbl} LIKE '" . esc_sql( $c ) . "'", ARRAY_A );
			return $r ? (string) $r['Type'] . ' / ' . (string) $r['Collation'] : 'unknown';
		};
		$rep['info']['col_option_value'] = $col( $wpdb->options, 'option_value' );
		$rep['info']['col_meta_value']   = $col( $wpdb->postmeta, 'meta_value' );
		$rep['info']['col_post_status']  = $col( $wpdb->posts, 'post_status' );
		// the claim is only as strong as this index: wp_options.option_name must be UNIQUE
		$idx = $wpdb->get_results( "SHOW INDEX FROM {$wpdb->options} WHERE Column_name = 'option_name'", ARRAY_A );
		$uniq = false;
		foreach ( (array) $idx as $i ) { if ( (int) $i['Non_unique'] === 0 && (int) $i['Seq_in_index'] === 1 ) { $uniq = true; } }
		$check( 'index.option_name_unique', $uniq, true, 'INSERT IGNORE is a claim only on a UNIQUE option_name' );

		$probe   = 0;
		$names   = array();
		$created = array();
		try {
			// one throwaway post row (unregistered type, never public), inserted without any hook
			$now = current_time( 'mysql' );
			$gmt = current_time( 'mysql', true );
			$ok  = $wpdb->insert( $wpdb->posts, array(
				'post_author' => (int) get_current_user_id(), 'post_date' => $now, 'post_date_gmt' => $gmt, 'post_content' => '', 'post_title' => 'had256-probe-' . $run,
				'post_excerpt' => '', 'post_status' => 'draft', 'comment_status' => 'closed', 'ping_status' => 'closed', 'post_password' => '', 'post_name' => 'had256-probe-' . $run,
				'to_ping' => '', 'pinged' => '', 'post_modified' => $now, 'post_modified_gmt' => $gmt, 'post_content_filtered' => '', 'post_parent' => 0, 'guid' => '',
				'menu_order' => 0, 'post_type' => 'nl_had256_probe', 'post_mime_type' => '', 'comment_count' => 0,
			) );
			$probe = (int) $wpdb->insert_id;
			$check( 'setup.probe_post', $ok === 1 && $probe > 0, true );
			if ( $probe <= 0 ) { throw new Exception( 'no probe post' ); }
			$rep['info']['probe_post'] = $probe;

			$lock  = 'nl_drop_lock_' . $probe;   $names[] = $lock;
			$claim = 'nl_pub_' . $probe . '_he'; $names[] = $claim;
			$att   = 'nl_att_had256probe' . $run; $names[] = $att;
			$ck    = 'nl_owner_ck_' . md5( 'had256probe|' . $run ); $names[] = $ck;
			$x     = 'nl_had256probe_x_' . $run; $names[] = $x;

			/* ---- broker-drop.php:2079 (nl_drop_lock_insert): the lock row ---- */
			$ins  = function ( $name, $val ) use ( $wpdb ) { return $wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO {$wpdb->options} (option_name, option_value, autoload) VALUES (%s, %s, 'no')", $name, $val ) ); };
			$seedA = wp_json_encode( array( 'who' => 'had256:A', 't' => time(), 'tok' => 0, 'r' => wp_generate_password( 12, false, false ) ) );
			$seedB = wp_json_encode( array( 'who' => 'had256:B', 't' => time(), 'tok' => 0, 'r' => wp_generate_password( 12, false, false ) ) );
			$check( 'lock.insert_winner', $rows( $ins( $lock, $seedA ) ), 1 );
			$check( 'lock.insert_loser', $rows( $ins( $lock, $seedB ) ), 0 );
			$read = function ( $name ) use ( $wpdb ) { return $wpdb->get_var( $wpdb->prepare( "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s LIMIT 1", $name ) ); };
			$check( 'lock.row_is_winners', $read( $lock ) === $seedA, true, 'broker-drop.php:2070 read' );

			/* ---- broker-drop.php:2113: the winner stamps its token into its own row (compare-and-set on the seed) ---- */
			$valA = wp_json_encode( array( 'who' => 'had256:A', 't' => time(), 'tok' => 1, 'r' => wp_generate_password( 12, false, false ) ) );
			$stamp = function ( $val, $name, $seed ) use ( $wpdb ) { return $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->options} SET option_value = %s WHERE option_name = %s AND option_value = %s", $val, $name, $seed ) ); };
			$check( 'lock.stamp_own_seed', $rows( $stamp( $valA, $lock, $seedA ) ), 1 );
			$check( 'lock.stamp_stale_seed', $rows( $stamp( $seedB, $lock, $seedA ) ), 0, 'the seed is gone: nothing written' );
			$check( 'lock.row_after_stamp', $read( $lock ) === $valA, true );

			/* ---- broker-drop.php:2142-2146 (nl_drop_fenced_meta): the commit, fenced by the lock row ---- */
			$wpdb->insert( $wpdb->postmeta, array( 'post_id' => $probe, 'meta_key' => 'nl_result', 'meta_value' => '' ) );   // add_post_meta( ..., '', true ) of 2142
			$fenced = function ( $value, $drop_id, $key, $mine ) use ( $wpdb ) {
				return $wpdb->query( $wpdb->prepare(
					"UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = %s AND EXISTS ( SELECT 1 FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s )",
					maybe_serialize( $value ), $drop_id, $key, 'nl_drop_lock_' . $drop_id, $mine
				) );
			};
			$meta = function ( $key ) use ( $wpdb, $probe ) { return $wpdb->get_var( $wpdb->prepare( "SELECT meta_value FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key = %s ORDER BY meta_id ASC LIMIT 1", $probe, $key ) ); };
			$resA = array( 'he_id' => 1, 'state' => 'publish', 'run' => 'A' );
			$check( 'fenced_meta.own_lock', $rows( $fenced( $resA, $probe, 'nl_result', $valA ) ), 1 );
			$same = $rows( $fenced( $resA, $probe, 'nl_result', $valA ) );
			$check( 'fenced_meta.same_value_own_lock', $same, array( 0, 1 ), 'MySQL counts changed rows: 0 here, so the code re-checks the fence (broker-drop.php:2148) and accepts; SQLite says 1' );
			$rep['info']['same_value_update_rows'] = $same;
			$check( 'fenced_meta.stale_token', $rows( $fenced( array( 'he_id' => 2, 'run' => 'stale' ), $probe, 'nl_result', $seedA ) ), 0, 'a run holding an older lock value commits nothing' );
			$check( 'fenced_meta.value_kept', $meta( 'nl_result' ) === maybe_serialize( $resA ), true );

			/* ---- broker-drop.php:2106 + 2101/2107: takeover after the TTL = compare-and-delete, then insert-if-absent ---- */
			$cad = function ( $name, $raw ) use ( $wpdb ) { return $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s", $name, $raw ) ); };
			$check( 'takeover.delete_with_stale_value', $rows( $cad( $lock, $seedA ) ), 0, 'a taker that read an older value deletes nothing' );
			$check( 'takeover.delete_with_current_value', $rows( $cad( $lock, $valA ) ), 1 );
			$seedC = wp_json_encode( array( 'who' => 'had256:C', 't' => time(), 'tok' => 0, 'r' => wp_generate_password( 12, false, false ) ) );
			$check( 'takeover.insert', $rows( $ins( $lock, $seedC ) ), 1 );
			$check( 'takeover.second_taker_loses', $rows( $ins( $lock, $seedB ) ), 0 );
			$valC = wp_json_encode( array( 'who' => 'had256:C', 't' => time(), 'tok' => 2, 'r' => wp_generate_password( 12, false, false ) ) );
			$check( 'takeover.stamp', $rows( $stamp( $valC, $lock, $seedC ) ), 1 );
			$check( 'fenced_meta.old_holder_after_takeover', $rows( $fenced( array( 'he_id' => 3, 'run' => 'A-late' ), $probe, 'nl_result', $valA ) ), 0, 'MUST be 0: the run that lost the lock cannot commit' );
			$check( 'fenced_meta.new_holder', $rows( $fenced( array( 'he_id' => 1, 'run' => 'C' ), $probe, 'nl_result', $valC ) ), 1 );

			/* ---- owner-wizard.php:1388-1391 (nl_owner_set_status): the status commit, fenced by the lock row ---- */
			$status = function ( $status, $slug, $first, $he, $drop_id, $mine ) use ( $wpdb ) {
				$now = current_time( 'mysql' );
				$gmt = current_time( 'mysql', true );
				return $wpdb->query( $wpdb->prepare(
					"UPDATE {$wpdb->posts} SET post_status = %s, post_name = %s, post_modified = %s, post_modified_gmt = %s" . ( $first ? ', post_date = %s, post_date_gmt = %s' : '' ) .
					" WHERE ID = %d AND EXISTS ( SELECT 1 FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s )",
					array_merge( array( $status, $slug, $now, $gmt ), $first ? array( $now, $gmt ) : array(), array( $he, 'nl_drop_lock_' . $drop_id, $mine ) )
				) );
			};
			$pst = function () use ( $wpdb, $probe ) { return (string) $wpdb->get_var( $wpdb->prepare( "SELECT post_status FROM {$wpdb->posts} WHERE ID = %d", $probe ) ); };
			// the probe's statuses stay non-public: draft -> pending; the stale attempts ask for 'publish' and must change nothing
			$check( 'status.stale_token_first_publish_shape', $rows( $status( 'publish', 'had256-probe-' . $run, true, $probe, $probe, $valA ) ), 0, 'MUST be 0 (the $first shape with post_date)' );
			$check( 'status.stale_token_plain_shape', $rows( $status( 'publish', 'had256-probe-' . $run, false, $probe, $probe, $seedA ) ), 0, 'MUST be 0' );
			$check( 'status.unchanged_after_stale', $pst(), 'draft' );
			$check( 'status.own_lock_first_shape', $rows( $status( 'pending', 'had256-probe-' . $run, true, $probe, $probe, $valC ) ), 1 );
			$check( 'status.now', $pst(), 'pending' );

			/* ---- broker-drop.php:2203 (nl_drop_claim_post): one listing per drop and language ---- */
			$check( 'claim.winner', $rows( $ins( $claim, wp_json_encode( array( 'post' => 111, 'tok' => 2, 't' => time() ) ) ) ), 1 );
			$check( 'claim.loser', $rows( $ins( $claim, wp_json_encode( array( 'post' => 222, 'tok' => 3, 't' => time() ) ) ) ), 0 );
			$cj = json_decode( (string) $read( $claim ), true );
			$check( 'claim.read_is_winners_post', is_array( $cj ) ? (int) ( $cj['post'] ?? 0 ) : 0, 111, 'broker-drop.php:2165 read' );

			/* ---- a second connection (another PHP worker) sees the same unique key. Plain mysqli with reporting off and
			   prepared statements (no wpdb constructor: a failed connect there may wp_die or load db-error.php before
			   the clean-up); the credentials stay inside this process and are never part of the report. ---- */
			$c2 = null;
			if ( function_exists( 'mysqli_init' ) && defined( 'DB_USER' ) && defined( 'DB_PASSWORD' ) && defined( 'DB_NAME' ) && defined( 'DB_HOST' ) && method_exists( $wpdb, 'parse_db_host' ) ) {
				try {
					mysqli_report( MYSQLI_REPORT_OFF );
					$hp = $wpdb->parse_db_host( DB_HOST );
					if ( is_array( $hp ) ) {
						list( $h2, $p2, $s2 ) = $hp;
						$c2 = mysqli_init();
						@mysqli_options( $c2, MYSQLI_OPT_CONNECT_TIMEOUT, 5 );
						if ( ! @mysqli_real_connect( $c2, (string) $h2, DB_USER, DB_PASSWORD, DB_NAME, $p2 ? (int) $p2 : null, $s2 ? (string) $s2 : null ) ) { $c2 = null; }
						else { @mysqli_set_charset( $c2, (string) ( $wpdb->charset ?: 'utf8mb4' ) ); }
					}
				} catch ( Throwable $e ) { $c2 = null; }
			}
			if ( $c2 ) {
				$st = mysqli_prepare( $c2, "INSERT IGNORE INTO {$wpdb->options} (option_name, option_value, autoload) VALUES (?, ?, 'no')" );
				$v2 = 'conn2';
				mysqli_stmt_bind_param( $st, 'ss', $x, $v2 );
				mysqli_stmt_execute( $st );
				$check( 'conn2.insert_winner', (int) mysqli_stmt_affected_rows( $st ), 1 );
				mysqli_stmt_close( $st );
				$check( 'conn1.insert_loser', $rows( $ins( $x, 'conn1' ) ), 0 );
				$st = mysqli_prepare( $c2, "UPDATE {$wpdb->postmeta} SET meta_value = ? WHERE post_id = ? AND meta_key = ? AND EXISTS ( SELECT 1 FROM {$wpdb->options} WHERE option_name = ? AND option_value = ? )" );
				$m2 = maybe_serialize( array( 'run' => 'conn2-stale' ) );
				$k2 = 'nl_result';
				$l2 = 'nl_drop_lock_' . $probe;
				mysqli_stmt_bind_param( $st, 'sisss', $m2, $probe, $k2, $l2, $valA );
				mysqli_stmt_execute( $st );
				$check( 'conn2.fenced_meta_stale', (int) mysqli_stmt_affected_rows( $st ), 0 );
				mysqli_stmt_close( $st );
				mysqli_close( $c2 );
			} else {
				$rep['info']['conn2'] = 'no second connection (not MySQL, or it could not be opened); the single-connection checks still hold';
			}

			/* ---- owner-wizard.php:359 (nl_owner_draft_cas): the draft compare-and-swap ---- */
			$cas = function ( $json, $id, $old_raw ) use ( $wpdb ) { return $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = 'nl_draft' AND meta_value = %s", $json, (int) $id, (string) $old_raw ) ); };
			$enc = function ( $a ) { return wp_json_encode( $a, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); };
			$r1  = $enc( array( 'v' => 2, 'rev' => 1, 'fields' => array( 'city' => 'תל אביב יפו', 'desc' => 'tel aviv, קומה 3' ), 'photos' => array(), 'step' => 'details', 'saved_at' => time() ) );
			$wpdb->insert( $wpdb->postmeta, array( 'post_id' => $probe, 'meta_key' => 'nl_draft', 'meta_value' => $r1 ) );
			$r2  = $enc( array( 'v' => 2, 'rev' => 2, 'fields' => array( 'city' => 'תל אביב יפו', 'desc' => 'Tel Aviv, קומה 3' ), 'photos' => array(), 'step' => 'details', 'saved_at' => time() ) );
			$check( 'cas.fresh_read', $rows( $cas( $r2, $probe, $r1 ) ), 1 );
			$r3  = $enc( array( 'v' => 2, 'rev' => 2, 'fields' => array( 'city' => 'x' ), 'photos' => array(), 'step' => 'details', 'saved_at' => time() ) );
			$check( 'cas.stale_read', $rows( $cas( $r3, $probe, $r1 ) ), 0, 'MUST be 0: the other tab saved first (409 + the server version)' );
			$check( 'cas.value_kept', $meta( 'nl_draft' ) === $r2, true );
			// collation: does '=' on meta_value ignore case? (the code never depends on it: every save bumps rev)
			$r2case = str_replace( 'Tel Aviv', 'TEL AVIV', $r2 );
			$r4     = $enc( array( 'v' => 2, 'rev' => 3, 'fields' => array( 'city' => 'probe' ), 'photos' => array(), 'step' => 'details', 'saved_at' => time() ) );
			$ci     = $rows( $cas( $r4, $probe, $r2case ) );
			$rep['info']['meta_value_compare_ignores_case'] = 1 === $ci;
			$check( 'cas.case_only_difference', $ci, array( 0, 1 ), '1 = a *_ci collation: harmless here, a stale text always differs in its rev digits' );
			if ( 1 === $ci ) { $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = 'nl_draft'", $r2, $probe ) ); }
			// a 4-byte character (an emoji in the owner's description) through the same CAS
			$r5 = $enc( array( 'v' => 2, 'rev' => 3, 'fields' => array( 'desc' => 'מרפסת 🌅 לים' ), 'photos' => array(), 'step' => 'details', 'saved_at' => time() ) );
			$check( 'cas.utf8mb4_emoji', $rows( $cas( $r5, $probe, $r2 ) ), 1, 'false here = the column is not utf8mb4: every save with an emoji would answer as a conflict' );
			$check( 'cas.utf8mb4_roundtrip', $meta( 'nl_draft' ) === $r5, true );
			$big = $enc( array( 'v' => 2, 'rev' => 4, 'fields' => array( 'desc' => str_repeat( 'דירה מוארת עם מרפסת. ', 600 ) ), 'photos' => array_fill( 0, 30, array( 'ref' => str_repeat( 'a', 32 ) ) ), 'step' => 'photos', 'saved_at' => time() ) );
			$check( 'cas.large_text', $rows( $cas( $big, $probe, $r5 ) ), 1, strlen( $big ) . ' bytes' );
			$check( 'cas.large_text_stale', $rows( $cas( $r5, $probe, $r5 ) ), 0 );

			/* ---- owner-wizard.php:924 + 960: the create key (a double tap = the same draft) ---- */
			$check( 'create_key.winner', $rows( $ins( $ck, 'pending|' . time() ) ), 1 );
			$check( 'create_key.double_tap', $rows( $ins( $ck, 'pending|' . time() ) ), 0 );
			$check( 'create_key.resolve', $rows( $wpdb->update( $wpdb->options, array( 'option_value' => $probe . '|' . time() ), array( 'option_name' => $ck ) ) ), 1 );

			/* ---- owner-wizard.php:1218-1219: the photo's attachment claim ---- */
			$ins( $att, 'pending' );   // a claim row left by a run that died before writing its attachment id
			$check( 'att.clear_unfinished_claim', $rows( $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s AND option_value NOT LIKE %s", $att, '%"att":%' ) ) ), 1 );
			$check( 'att.claim_winner', $rows( $ins( $att, wp_json_encode( array( 'att' => 333, 't' => time() ) ) ) ), 1 );
			$check( 'att.finished_claim_kept', $rows( $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s AND option_value NOT LIKE %s", $att, '%"att":%' ) ) ), 0 );
			$check( 'att.claim_loser', $rows( $ins( $att, wp_json_encode( array( 'att' => 444, 't' => time() ) ) ) ), 0 );

			/* ---- broker-drop.php:2157 (nl_drop_lock_release): only the holder's own value is deleted ---- */
			$check( 'release.stale_value', $rows( $cad( $lock, $valA ) ), 0 );
			$check( 'release.own_value', $rows( $cad( $lock, $valC ) ), 1 );
		} catch ( Throwable $e ) {
			$fail++;
			$rep['error'] = get_class( $e ) . ': ' . $e->getMessage();
		} finally {
			foreach ( $names as $n ) { $wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s", $n ) ); wp_cache_delete( $n, 'options' ); }
			if ( $probe > 0 ) {
				$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->postmeta} WHERE post_id = %d", $probe ) );
				$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->posts} WHERE ID = %d AND post_type = 'nl_had256_probe'", $probe ) );
				wp_cache_delete( $probe, 'posts' );
				wp_cache_delete( $probe, 'post_meta' );
			}
			wp_cache_delete( 'notoptions', 'options' );
			wp_cache_delete( 'alloptions', 'options' );
			$left_o = 0;
			foreach ( $names as $n ) { $left_o += (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->options} WHERE option_name = %s", $n ) ); }
			$rep['cleanup'] = array(
				'options_left'  => $left_o,
				'postmeta_left' => $probe > 0 ? (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE post_id = %d", $probe ) ) : 0,
				'posts_left'    => $probe > 0 ? (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM {$wpdb->posts} WHERE ID = %d", $probe ) ) : 0,
				'probe_type_left_anywhere' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = 'nl_had256_probe'" ),
			);
			if ( array_sum( $rep['cleanup'] ) !== 0 ) { $fail++; }
		}
		$rep['failures'] = $fail;
		$rep['all_pass'] = 0 === $fail;
		$rep['ms']       = (int) round( ( microtime( true ) - $t0 ) * 1000 );
		return $rep;
	}
}

/* The temporary admin-only route (main's bridge pattern). __TOKEN__ is replaced by the runner; left as is, it refuses. */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-had256-ops/v1', '/mysql-claim-check', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => function ( $req ) {
			$b   = $req->get_json_params();
			$tok = '__TOKEN__';
			if ( $tok === '__' . 'TOKEN__' || ! is_array( $b ) || ! hash_equals( $tok, (string) ( $b['token'] ?? '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$r = nl_had256_mysql_claim_check();
			return new WP_REST_Response( $r, 200, array( 'Cache-Control' => 'no-store' ) );
		},
	) );
} );
