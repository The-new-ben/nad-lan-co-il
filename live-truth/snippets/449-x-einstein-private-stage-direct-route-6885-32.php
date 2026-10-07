add_action( 'pre_get_posts', function ( $query ) {
	$method = isset( $_SERVER['REQUEST_METHOD'] ) ? strtoupper( (string) $_SERVER['REQUEST_METHOD'] ) : '';
	if ( is_admin() || ( defined( 'REST_REQUEST' ) && REST_REQUEST )
		|| ! in_array( $method, array( 'GET', 'HEAD' ), true )
		|| ! $query instanceof WP_Query || ! $query->is_main_query()
		|| $query->is_feed() || $query->is_embed() || $query->is_preview()
		|| $query->is_trackback() || $query->is_search() || $query->is_archive() ) {
		return;
	}
	$request_uri = isset( $_SERVER['REQUEST_URI'] )
		? (string) wp_unslash( $_SERVER['REQUEST_URI'] )
		: '';
	$path = wp_parse_url( $request_uri, PHP_URL_PATH );
	$query_string = wp_parse_url( $request_uri, PHP_URL_QUERY );
	if ( null !== $query_string && '' !== (string) $query_string
		&& 1 !== preg_match( '/\Acb=[a-z0-9-]{1,128}\z/D', (string) $query_string ) ) {
		return;
	}
	if ( '/projects/sandbox-einstein-tower-flagship-v3-review' !== untrailingslashit( (string) $path ) ) {
		return;
	}
	$slug = 'sandbox-einstein-tower-flagship-v3-review';
	$name = (string) $query->get( 'name' );
	$project = (string) $query->get( 'nadlan_project' );
	if ( 'nadlan_project' !== (string) $query->get( 'post_type' )
		|| ! in_array( $name, array( '', $slug ), true )
		|| ! in_array( $project, array( '', $slug ), true )
		|| ( $slug !== $name && $slug !== $project ) ) {
		return;
	}
	$query->set( 'nadlan_include_private_unit_journey', true );
}, 1 );
