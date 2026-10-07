add_action( 'rest_api_init', function () {
	register_rest_route( 'nlagent/v1', '/v5d180700', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback' => function ( $req ) {
			$files = json_decode( (string) $req->get_param( 'files' ), true );
			if ( ! is_array( $files ) ) { return array( 'err' => 'manifest' ); }
			$u = wp_get_upload_dir();
			$out = array();
			foreach ( $files as $f ) {
				$r = array();
				$dest = trailingslashit( $u['basedir'] ) . $f['dst'];
				$live_md5 = file_exists( $dest ) ? md5_file( $dest ) : 'absent';
				if ( $live_md5 !== $f['base_md5'] ) { $out[ $f['dst'] ] = array( 'ABORT' => 'base-drift', 'live' => $live_md5 ); continue; }
				$raw = gzuncompress( base64_decode( trim( (string) file_get_contents( trailingslashit( $u['path'] ) . $f['payload'] ) ), true ) );
				if ( false === $raw || md5( $raw ) !== $f['md5'] ) { $out[ $f['dst'] ] = 'payload-fail'; continue; }
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