add_action( 'rest_api_init', function () {
	register_rest_route( 'nlagent/v1', '/v6peek184929', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback' => function ( $req ) {
			$root = (string) $req->get_param( 'root' );
			$rel  = (string) $req->get_param( 'path' );
			$u = wp_get_upload_dir();
			$base = ( 'plugin' === $root ) ? trailingslashit( WP_PLUGIN_DIR ) : trailingslashit( $u['basedir'] );
			$p = $base . $rel;
			if ( ! file_exists( $p ) ) { return array( 'exists' => false ); }
			return array( 'exists' => true, 'md5' => md5_file( $p ), 'bytes' => filesize( $p ) );
		},
	) );
	register_rest_route( 'nlagent/v1', '/v6swap184929', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback' => function ( $req ) {
			$files = json_decode( (string) $req->get_param( 'files' ), true );
			if ( ! is_array( $files ) ) { return array( 'err' => 'manifest' ); }
			$u = wp_get_upload_dir();
			$out = array();
			foreach ( $files as $f ) {
				$r = array();
				$base = ( isset( $f['root'] ) && 'plugin' === $f['root'] ) ? trailingslashit( WP_PLUGIN_DIR ) : trailingslashit( $u['basedir'] );
				$dest = $base . $f['dst'];
				$live_md5 = file_exists( $dest ) ? md5_file( $dest ) : 'absent';
				if ( $live_md5 !== $f['base_md5'] ) { $out[ $f['dst'] ] = array( 'ABORT' => 'base-drift', 'live' => $live_md5 ); continue; }
				$raw = gzuncompress( base64_decode( trim( (string) file_get_contents( trailingslashit( $u['path'] ) . $f['payload'] ) ), true ) );
				if ( false === $raw ) { $out[ $f['dst'] ] = 'inflate-fail'; continue; }
				$r['md5_in_ok'] = ( md5( $raw ) === $f['md5'] );
				if ( ! $r['md5_in_ok'] ) { $out[ $f['dst'] ] = $r; continue; }
				if ( substr( $f['dst'], -4 ) === '.php' ) {
					try { token_get_all( $raw, TOKEN_PARSE ); $r['lint'] = 'ok'; }
					catch ( ParseError $e ) { $out[ $f['dst'] ] = array( 'ABORT' => 'php-parse', 'msg' => $e->getMessage() ); continue; }
				}
				if ( ! file_exists( $dest . '.bakV6' ) ) { copy( $dest, $dest . '.bakV6' ); }
				$r['bak'] = true;
				file_put_contents( $dest, $raw );
				$r['md5_written_ok'] = ( md5_file( $dest ) === $f['md5'] );
				$out[ $f['dst'] ] = $r;
			}
			do_action( 'litespeed_purge_all' );
			wp_cache_flush();
			return $out;
		},
	) );
} );