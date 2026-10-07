add_action( 'rest_api_init', function () {
	register_rest_route( 'nlagent/v1', '/v8get101621', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback' => function ( $req ) {
			$p = trailingslashit( WP_PLUGIN_DIR ) . (string) $req->get_param( 'path' );
			if ( ! file_exists( $p ) ) { return array( 'exists' => false ); }
			return array( 'md5' => md5_file( $p ), 'b64' => base64_encode( (string) file_get_contents( $p ) ) );
		},
	) );
} );