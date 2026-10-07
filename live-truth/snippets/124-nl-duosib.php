add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/duosib', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function( WP_REST_Request $req ){
      $p = $req->get_json_params();
      $parent = 4893; $out = array();
      $meta_all = get_post_meta( $parent );
      foreach ( (array) $p['siblings'] as $sib ) {
        $slug = sanitize_title( $sib['slug'] );
        $existing = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
        if ( $existing ) { $out[ $slug ] = array('id'=>$existing->ID,'status'=>'exists'); continue; }
        $pid = wp_insert_post( array(
          'post_type' => 'nadlan_project', 'post_status' => 'publish',
          'post_title' => sanitize_text_field( $sib['title'] ),
          'post_name' => $slug,
          'post_content' => wp_kses_post( $sib['content'] ),
        ) );
        if ( is_wp_error( $pid ) || ! $pid ) { $out[ $slug ] = array('status'=>'failed'); continue; }
        $copied = 0;
        foreach ( $meta_all as $k => $vals ) {
          if ( strpos( $k, 'project_' ) === 0 || in_array( $k, array( 'lat','lng','city','address','geo_confidence','developer','_yoast_wpseo_metadesc' ), true ) ) {
            update_post_meta( $pid, $k, maybe_unserialize( $vals[0] ) ); $copied++;
          }
        }
        $out[ $slug ] = array('id'=>$pid,'status'=>'created','meta_copied'=>$copied,'url'=>get_permalink($pid));
      }
      delete_transient('nadlan_project_map_v1');
      do_action('litespeed_purge_all'); wp_cache_flush();
      return $out;
    }));
});
