add_action( 'rest_api_init', function () {
    register_rest_route( 'nlagent313/v1', '/put', array(
        'methods' => 'POST',
        'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
        'callback' => function ( $req ) {
            $code = gzuncompress( base64_decode( (string) $req->get_param( 'b64' ) ) );
            if ( $code === false || md5( $code ) !== (string) $req->get_param( 'md5' ) ) { return array( 'ok' => false, 'error' => 'md5-in' ); }
            $up = wp_upload_dir();
            $path = $up['basedir'] . '/2026/08/six8-mobile-demo.html';
            file_put_contents( $path, $code );
            do_action( 'litespeed_purge_all' ); wp_cache_flush();
            return array( 'ok' => true, 'written' => md5_file( $path ), 'url' => $up['baseurl'] . '/2026/08/six8-mobile-demo.html' );
        },
    ) );
} );