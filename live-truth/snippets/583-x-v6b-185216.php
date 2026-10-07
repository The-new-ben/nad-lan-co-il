add_action( 'rest_api_init', function () {
	register_rest_route( 'nlagent/v1', '/v6b185216', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback' => function ( $req ) {
			$f = json_decode( (string) $req->get_param( 'f' ), true );
			$u = wp_get_upload_dir();
			$dest = trailingslashit( $u['basedir'] ) . $f['dst'];
			$live = file_exists( $dest ) ? md5_file( $dest ) : 'absent';
			if ( $live !== $f['base_md5'] ) { return array( 'ABORT' => 'base-drift', 'live' => $live ); }
			$raw = gzuncompress( base64_decode( trim( (string) file_get_contents( trailingslashit( $u['path'] ) . $f['payload'] ) ), true ) );
			if ( false === $raw || md5( $raw ) !== $f['md5'] ) { return array( 'ABORT' => 'payload' ); }
			if ( ! file_exists( $dest . '.bakV6B' ) ) { copy( $dest, $dest . '.bakV6B' ); }
			file_put_contents( $dest, $raw );
			$ok = ( md5_file( $dest ) === $f['md5'] );
			do_action( 'litespeed_purge_all' );
			wp_cache_flush();
			return array( 'bak' => true, 'md5_written_ok' => $ok );
		},
	) );
} );