add_action( 'rest_api_init', function () {
	register_rest_route( 'nlagent/v1', '/v7ls002039', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback' => function () {
			$u = wp_get_upload_dir();
			$out = array();
			foreach ( glob( trailingslashit( $u['basedir'] ) . '2026/*/*.html' ) as $p ) {
				$out[] = str_replace( trailingslashit( $u['basedir'] ), '', $p ) . ' | ' . filesize( $p );
			}
			return $out;
		},
	) );
} );