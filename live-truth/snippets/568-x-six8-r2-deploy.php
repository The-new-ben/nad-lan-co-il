add_action( 'rest_api_init', function () {
    $perm = function () { return current_user_can( 'update_plugins' ); };
    register_rest_route( 'nlagent303/v1', '/lint', array(
        'methods' => 'POST', 'permission_callback' => $perm,
        'callback' => function ( $req ) {
            $code = gzuncompress( base64_decode( (string) $req->get_param( 'b64' ) ) );
            if ( $code === false ) { return array( 'ok' => false, 'error' => 'decode' ); }
            try { token_get_all( $code, TOKEN_PARSE ); }
            catch ( ParseError $e ) { return array( 'ok' => false, 'error' => $e->getMessage(), 'line' => $e->getLine() ); }
            return array( 'ok' => true, 'md5' => md5( $code ), 'len' => strlen( $code ) );
        },
    ) );
    register_rest_route( 'nlagent303/v1', '/swap', array(
        'methods' => 'POST', 'permission_callback' => $perm,
        'callback' => function ( $req ) {
            $rel = (string) $req->get_param( 'rel' );
            $allowed = array( 'inc/showroom-engine.php', 'nadlan-config.php' );
            if ( ! in_array( $rel, $allowed, true ) ) { return array( 'ok' => false, 'error' => 'path' ); }
            $code = gzuncompress( base64_decode( (string) $req->get_param( 'b64' ) ) );
            if ( $code === false || md5( $code ) !== (string) $req->get_param( 'md5' ) ) { return array( 'ok' => false, 'error' => 'md5-in' ); }
            $path = WP_PLUGIN_DIR . '/nadlan-config/' . $rel;
            if ( ! file_exists( $path ) ) { return array( 'ok' => false, 'error' => 'missing' ); }
            $bak = $path . '.bak302';
            if ( ! file_exists( $bak ) ) { copy( $path, $bak ); }
            file_put_contents( $path, $code );
            if ( function_exists( 'opcache_invalidate' ) ) { opcache_invalidate( $path, true ); }
            return array( 'ok' => true, 'written' => md5_file( $path ), 'bak' => basename( $bak ) );
        },
    ) );
    register_rest_route( 'nlagent303/v1', '/seed', array(
        'methods' => 'POST', 'permission_callback' => $perm,
        'callback' => function ( $req ) {
            $pid = 7219;
            $m = (array) $req->get_param( 'meta' );
            $keys = array( 'project_comps_json', 'project_price_updated', 'project_comps_source_note', 'project_area_json' );
            $out = array();
            foreach ( $keys as $k ) {
                if ( ! isset( $m[ $k ] ) ) { continue; }
                update_post_meta( $pid, $k, wp_slash( (string) $m[ $k ] ) );
                $out[ $k ] = (string) get_post_meta( $pid, $k, true );
            }
            $lm = (string) get_post_meta( $pid, 'project_env_landmarks', true );
            do_action( 'litespeed_purge_all' ); wp_cache_flush();
            return array( 'ok' => true, 'meta' => $out, 'landmarks_len' => strlen( $lm ) );
        },
    ) );
    register_rest_route( 'nlagent303/v1', '/purge', array(
        'methods' => 'POST', 'permission_callback' => $perm,
        'callback' => function () {
            do_action( 'litespeed_purge_all' ); wp_cache_flush();
            if ( function_exists( 'opcache_reset' ) ) { @opcache_reset(); }
            return array( 'ok' => true, 'version' => defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '' );
        },
    ) );
} );