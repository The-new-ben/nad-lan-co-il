// temp: rewrite dead asset URLs (raw.githubusercontent + missing plugin plans) on the 5 Rainbow siblings
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlanfix/v1', '/rainbow', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => function ( $req ) {
			$map = $req->get_param( 'map' ); // array of [search, replace] pairs, plain form
			$ids = array( 4464, 5060, 5071, 5072, 5074 );
			if ( ! is_array( $map ) || ! $map ) { return new WP_Error( 'nomap', 'map required', array( 'status' => 400 ) ); }
			$apply = function ( $s ) use ( $map ) {
				foreach ( $map as $pair ) {
					if ( ! is_array( $pair ) || count( $pair ) < 2 ) { continue; }
					$search = (string) $pair[0]; $replace = (string) $pair[1];
					$s = str_replace( $search, $replace, $s );
					// JSON-escaped variant (slashes escaped) as stored inside meta JSON strings
					$s = str_replace( str_replace( '/', '\\/', $search ), str_replace( '/', '\\/', $replace ), $s );
				}
				return $s;
			};
			$out = array();
			foreach ( $ids as $id ) {
				$rep = array( 'id' => $id, 'meta_changed' => array(), 'content_changed' => false );
				$all = get_post_meta( $id );
				foreach ( $all as $key => $vals ) {
					foreach ( $vals as $v ) {
						if ( ! is_string( $v ) || '' === $v ) { continue; }
						$nv = $apply( $v );
						if ( $nv !== $v ) {
							update_post_meta( $id, $key, wp_slash( $nv ), $v );
							$rep['meta_changed'][] = $key;
						}
					}
				}
				$p = get_post( $id );
				if ( $p ) {
					$nc = $apply( $p->post_content );
					if ( $nc !== $p->post_content ) {
						wp_update_post( array( 'ID' => $id, 'post_content' => wp_slash( $nc ) ) );
						$rep['content_changed'] = true;
					}
				}
				$rep['model_now'] = (string) get_post_meta( $id, 'project_model_glb', true );
				$out[] = $rep;
			}
			do_action( 'litespeed_purge_all' ); wp_cache_flush();
			return $out;
		},
	) );
} );
