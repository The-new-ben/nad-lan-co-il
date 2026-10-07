add_action( 'rest_api_init', function () {
    $perm = function () { return current_user_can( 'update_plugins' ); };
    register_rest_route( 'nlagent310/v1', '/board', array(
        'methods' => 'POST', 'permission_callback' => $perm,
        'callback' => function ( $req ) {
            $code = gzuncompress( base64_decode( (string) $req->get_param( 'b64' ) ) );
            if ( $code === false || md5( $code ) !== (string) $req->get_param( 'md5' ) ) { return array( 'ok' => false, 'error' => 'md5-in' ); }
            $up = wp_upload_dir();
            $path = $up['basedir'] . '/2026/08/owner-board.html';
            if ( ! file_exists( $path ) ) { return array( 'ok' => false, 'error' => 'missing' ); }
            $bak = $path . '.bakSIX8';
            if ( ! file_exists( $bak ) ) { copy( $path, $bak ); }
            file_put_contents( $path, $code );
            $slug_t = 'nadlan_pwalk_' . md5( 'six-8-herbert-samuel-tel-aviv' );
            delete_transient( $slug_t );
            delete_transient( 'nlpjx_near_v2_7219' );
            delete_transient( 'nlpjx_comps_v2_7219' );
            do_action( 'litespeed_purge_all' ); wp_cache_flush();
            return array( 'ok' => true, 'written' => md5_file( $path ), 'pwalk_busted' => $slug_t );
        },
    ) );
} );