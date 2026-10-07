
add_action( 'rest_api_init', function () {
  register_rest_route( 'nlsix8/v1', '/put', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
    'callback' => function ( $req ) {
      $p = $req->get_json_params();
      $rel = sanitize_file_name( (string) $p['name'] );
      $data = base64_decode( (string) $p['b64'] );
      if ( $rel === '' || $data === false ) { return new WP_Error( 'bad', 'bad input', array( 'status' => 400 ) ); }
      $dir = wp_upload_dir();
      $path = trailingslashit( $dir['basedir'] ) . '2026/08/' . $rel;
      file_put_contents( $path, $data );
      return array( 'md5' => md5_file( $path ), 'url' => trailingslashit( $dir['baseurl'] ) . '2026/08/' . $rel, 'len' => strlen( $data ) );
    },
  ) );
} );
