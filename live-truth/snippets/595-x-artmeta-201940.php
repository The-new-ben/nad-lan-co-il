add_action( 'rest_api_init', function () {
	register_rest_route( 'nlagent/v1', '/artmeta201940', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback' => function ( $req ) {
			$pid = (int) $req->get_param( 'post_id' );
			update_post_meta( $pid, '_yoast_wpseo_title', (string) $req->get_param( 'title' ) );
			update_post_meta( $pid, '_yoast_wpseo_metadesc', (string) $req->get_param( 'desc' ) );
			do_action( 'litespeed_purge_all' );
			wp_cache_flush();
			return array( 'ok' => true );
		},
	) );
} );