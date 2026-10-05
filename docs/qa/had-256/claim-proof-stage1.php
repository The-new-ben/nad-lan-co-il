<?php
/**
 * HAD-256 staged proof, stage 1 of 3: read-only facts about the database engine. Writes nothing, anywhere.
 *
 * Install as a temporary Code Snippet (body = this file without the opening tag), with __TOKEN__ replaced by a fresh
 * token; POST /wp-json/nadlan-h256c/v1/s1 {"token": TOKEN} as an administrator; then deactivate and delete the snippet.
 * Body options:
 *   "steps": ["hello"]                     only the hello answer, no database query at all (run this first);
 *            ["vars"] ["tables"] ["cols"] ["index"] or any mix; default: all four after hello
 *   "enc": 0                               a readable answer; default 1 = the whole answer as one base64 field "b64"
 *   "verbose": 1                           add the database's own error text next to each error number (default: number only)
 * Safety: no write; database errors are suppressed for the run (never printed into the answer or the PHP log) and
 * reported as numbers; no credential constant is read. Answers only manage_options + the token; refuses an unreplaced token.
 */
if ( ! function_exists( 'nl_h256c_s1_run' ) ) {
	function nl_h256c_s1_run( $b ) {
		global $wpdb;
		$t0    = microtime( true );
		$steps = isset( $b['steps'] ) ? array_map( 'strval', (array) $b['steps'] ) : array( 'vars', 'tables', 'cols', 'index' );
		$on    = function ( $s ) use ( $steps ) { return in_array( $s, $steps, true ); };
		$verb  = ! empty( $b['verbose'] );
		$out   = array(
			'kit'    => 'h256c-s1 v1',
			'hello'  => 'ok',
			'at_gmt' => gmdate( 'c' ),
			'php'    => PHP_VERSION,
			'wp'     => (string) get_bloginfo( 'version' ),
			'debug'  => array(
				'wp_debug'         => defined( 'WP_DEBUG' ) && WP_DEBUG,
				'wp_debug_display' => defined( 'WP_DEBUG_DISPLAY' ) ? (bool) WP_DEBUG_DISPLAY : null,
				'db_show_errors'   => (bool) $wpdb->show_errors,
				'ext_object_cache' => function_exists( 'wp_using_ext_object_cache' ) ? (bool) wp_using_ext_object_cache() : null,
				'charset'          => (string) $wpdb->charset,
				'collate'          => (string) $wpdb->collate,
			),
			'errors' => array(),
		);
		$errno = function () use ( $wpdb ) {
			$h = $wpdb->dbh;
			return ( $h instanceof mysqli ) ? (int) mysqli_errno( $h ) : -1;
		};
		$prev = $wpdb->suppress_errors( true );
		try {
			$rows = function ( $label, $q ) use ( $wpdb, &$out, $errno, $verb ) {
				$r = $wpdb->get_results( $q, ARRAY_A );
				if ( '' !== (string) $wpdb->last_error ) {
					$out['errors'][ $label ] = array( 'no' => $errno() ) + ( $verb ? array( 'text' => substr( (string) $wpdb->last_error, 0, 200 ) ) : array() );
					return array();
				}
				return is_array( $r ) ? $r : array();
			};
			if ( $on( 'vars' ) ) {
				// SHOW VARIABLES never fails on a name the engine does not know (tx_isolation / transaction_isolation differ by engine and version)
				$v = array();
				foreach ( $rows( 'vars', "SHOW VARIABLES WHERE Variable_name IN ('version','version_comment','innodb_version','autocommit','tx_isolation','transaction_isolation','sql_mode','character_set_database','collation_database','lower_case_table_names')" ) as $r ) {
					$v[ (string) $r['Variable_name'] ] = (string) $r['Value'];
				}
				$out['vars'] = $v;
			}
			if ( $on( 'tables' ) ) {
				$t = array();
				foreach ( array( 'options' => $wpdb->options, 'postmeta' => $wpdb->postmeta, 'posts' => $wpdb->posts ) as $k => $tbl ) {
					$r = $rows( 'tables_' . $k, $wpdb->prepare( 'SELECT ENGINE AS e, TABLE_COLLATION AS c FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s', $tbl ) );
					$t[ $k ] = $r ? (string) $r[0]['e'] . ' / ' . (string) $r[0]['c'] : 'unknown';
				}
				$out['tables'] = $t;
			}
			if ( $on( 'cols' ) ) {
				$c = array();
				foreach ( array( array( $wpdb->options, 'option_name' ), array( $wpdb->options, 'option_value' ), array( $wpdb->postmeta, 'meta_value' ), array( $wpdb->posts, 'post_status' ) ) as $p ) {
					$r = $rows( 'cols_' . $p[1], $wpdb->prepare( 'SELECT COLUMN_TYPE AS t, CHARACTER_SET_NAME AS s, COLLATION_NAME AS c FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s', $p[0], $p[1] ) );
					$c[ $p[1] ] = $r ? (string) $r[0]['t'] . ' / ' . (string) $r[0]['s'] . ' / ' . (string) $r[0]['c'] : 'unknown';
				}
				$out['cols'] = $c;
			}
			if ( $on( 'index' ) ) {
				// the one-row-per-name rule rests on this: option_name must be the first column of a UNIQUE index
				$r    = $rows( 'index', $wpdb->prepare( "SELECT INDEX_NAME AS n, NON_UNIQUE AS u, SEQ_IN_INDEX AS q FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = 'option_name'", $wpdb->options ) );
				$uniq = false;
				foreach ( $r as $i ) { if ( 0 === (int) $i['u'] && 1 === (int) $i['q'] ) { $uniq = true; } }
				if ( ! $r ) {   // an engine without information_schema statistics: the SHOW form
					foreach ( $rows( 'index_show', "SHOW INDEX FROM {$wpdb->options} WHERE Column_name = 'option_name'" ) as $i ) {
						if ( 0 === (int) $i['Non_unique'] && 1 === (int) $i['Seq_in_index'] ) { $uniq = true; }
					}
				}
				$out['index'] = array( 'option_name_unique' => $uniq, 'rows' => count( $r ) );
			}
		} catch ( Throwable $e ) {
			$out['thrown'] = get_class( $e );
		} finally {
			$wpdb->suppress_errors( $prev );
		}
		$out['ms'] = (int) round( ( microtime( true ) - $t0 ) * 1000 );
		return $out;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-h256c/v1', '/s1', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => function ( $req ) {
			$b   = $req->get_json_params();
			$tok = '__TOKEN__';
			if ( $tok === '__' . 'TOKEN__' || ! is_array( $b ) || ! hash_equals( $tok, (string) ( $b['token'] ?? '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$r = nl_h256c_s1_run( $b );
			if ( ! isset( $b['enc'] ) || ! empty( $b['enc'] ) ) { $r = array( 'b64' => base64_encode( (string) wp_json_encode( $r ) ) ); }
			return new WP_REST_Response( $r, 200, array( 'Cache-Control' => 'no-store' ) );
		},
	) );
} );
