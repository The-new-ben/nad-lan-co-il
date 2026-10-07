
add_action( 'rest_api_init', function () {
	register_rest_route( 'agentfix/v1', '/poi-diag', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback'            => function () {
			$out = array();
			$q = '[out:json][timeout:20];(node(around:800,32.10317,34.78446)[highway=bus_stop];);out tags 50;';
			foreach ( array( 'https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter' ) as $ep ) {
				$t0 = microtime( true );
				$res = wp_remote_post( $ep, array( 'timeout' => 14, 'body' => array( 'data' => $q ),
					'headers' => array( 'User-Agent' => 'nadlan-config/2.0 (nad-lan.co.il)' ) ) );
				if ( is_wp_error( $res ) ) {
					$out[ $ep ] = array( 'error' => $res->get_error_message(), 'ms' => round( ( microtime( true ) - $t0 ) * 1000 ) );
				} else {
					$b = (string) wp_remote_retrieve_body( $res );
					$j = json_decode( $b, true );
					$out[ $ep ] = array( 'code' => wp_remote_retrieve_response_code( $res ),
						'elements' => is_array( $j ) ? count( $j['elements'] ?? array() ) : null,
						'body_head' => mb_substr( $b, 0, 120 ), 'ms' => round( ( microtime( true ) - $t0 ) * 1000 ) );
				}
			}
			return $out;
		},
	) );
} );
