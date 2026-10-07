
add_action( 'rest_api_init', function () {
  register_rest_route( 'nlsix8m/v1', '/meta', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
    'callback' => function ( $req ) {
      $p = $req->get_json_params();
      $id = (int) $p['post_id'];
      if ( get_post_type( $id ) !== 'nadlan_project' ) { return new WP_Error( 'bad', 'not a project', array( 'status' => 400 ) ); }
      $out = array();
      foreach ( (array) $p['meta'] as $k => $v ) {
        update_post_meta( $id, sanitize_key( $k ), wp_slash( (string) $v ) );
        $out[ $k ] = (string) get_post_meta( $id, sanitize_key( $k ), true );
      }
      return $out;
    },
  ) );
} );
