add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/geo-ingest', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function( WP_REST_Request $req ){
      $rows = $req->get_json_params();
      $written = 0; $skipped_existing = 0; $missing = 0;
      foreach ( (array) $rows as $r ) {
        $id = (int) ($r['id'] ?? 0);
        if ( ! $id || get_post_type($id) !== 'nadlan_project' ) { $missing++; continue; }
        if ( get_post_meta($id,'lat',true) !== '' ) { $skipped_existing++; continue; }
        $la=(float)$r['lat']; $ln=(float)$r['lng'];
        if ($la<29.4||$la>33.4||$ln<34.2||$ln>35.9) { continue; }
        update_post_meta($id,'lat',$la);
        update_post_meta($id,'lng',$ln);
        update_post_meta($id,'geo_confidence',sanitize_key($r['conf'] ?? 'city'));
        $written++;
      }
      delete_transient('nadlan_project_map_v1');
      return array('written'=>$written,'skipped_existing'=>$skipped_existing,'missing'=>$missing);
    }));
});
