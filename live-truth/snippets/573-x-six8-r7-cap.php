add_action( 'rest_api_init', function () {
    $perm = function () { return current_user_can( 'update_plugins' ); };
    register_rest_route( 'nlagent312/v1', '/lint', array(
        'methods' => 'POST', 'permission_callback' => $perm,
        'callback' => function ( $req ) {
            $code = gzuncompress( base64_decode( (string) $req->get_param( 'b64' ) ) );
            if ( $code === false ) { return array( 'ok' => false, 'error' => 'decode' ); }
            try { token_get_all( $code, TOKEN_PARSE ); }
            catch ( ParseError $e ) { return array( 'ok' => false, 'error' => $e->getMessage(), 'line' => $e->getLine() ); }
            return array( 'ok' => true, 'md5' => md5( $code ) );
        },
    ) );
    register_rest_route( 'nlagent312/v1', '/put', array(
        'methods' => 'POST', 'permission_callback' => $perm,
        'callback' => function ( $req ) {
            $rel = (string) $req->get_param( 'rel' );
            $allowed = array(
                'inc/showroom-engine.php',
                'nadlan-config.php',
                'assets/showroom-engine/unit-sheet.css',
                'assets/showroom-engine/unit-sheet.js',
            );
            if ( ! in_array( $rel, $allowed, true ) ) { return array( 'ok' => false, 'error' => 'path' ); }
            $code = gzuncompress( base64_decode( (string) $req->get_param( 'b64' ) ) );
            if ( $code === false || md5( $code ) !== (string) $req->get_param( 'md5' ) ) { return array( 'ok' => false, 'error' => 'md5-in' ); }
            $path = WP_PLUGIN_DIR . '/nadlan-config/' . $rel;
            if ( file_exists( $path ) ) {
                $bak = $path . '.bak312';
                if ( ! file_exists( $bak ) ) { copy( $path, $bak ); }
            }
            $dir = dirname( $path );
            if ( ! is_dir( $dir ) ) { return array( 'ok' => false, 'error' => 'dir' ); }
            file_put_contents( $path, $code );
            if ( function_exists( 'opcache_invalidate' ) ) { opcache_invalidate( $path, true ); }
            do_action( 'litespeed_purge_all' ); wp_cache_flush();
            if ( function_exists( 'opcache_reset' ) ) { @opcache_reset(); }
            return array( 'ok' => true, 'written' => md5_file( $path ),
                'version' => defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '' );
        },
    ) );
} );