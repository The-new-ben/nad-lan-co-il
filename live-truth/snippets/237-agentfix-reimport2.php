
add_action( 'rest_api_init', function () {
	register_rest_route( 'agentfix/v1', '/reimport-urban', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback'            => function ( WP_REST_Request $req ) {
			$off = (int) $req->get_param( 'offset' );
			$lim = max( 10, min( 200, (int) $req->get_param( 'limit' ) ?: 100 ) );
			$r = nadlan_import_urban_batch( $lim, $off );
			if ( is_wp_error( $r ) ) { return $r; }
			delete_transient( 'nadlan_ur_mapdata_v3' );
			delete_transient( 'nadlan_ur_mapseo_v3' );
			return $r;
		},
	) );
} );
