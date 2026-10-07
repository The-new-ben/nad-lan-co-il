add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/encboot', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function( WP_REST_Request $req ){
      $map = (array) $req->get_json_params();
      $q = new WP_Query(array('post_type'=>'nadlan_term','post_status'=>'draft','posts_per_page'=>250,'fields'=>'ids',
        'meta_query'=>array(array('key'=>'entity_type','compare'=>'EXISTS'))));
      $set=0;
      foreach ($q->posts as $pid) {
        $t = get_the_title($pid);
        if (isset($map[$t])) { update_post_meta($pid,'enc_priority',(int)$map[$t]); $set++; }
      }
      update_option('nadlan_enc_writer_model','gpt-4o-mini',false);
      if ( function_exists('nadlan_enc_writer_run') ) { nadlan_enc_writer_run(); }
      return array('priorities_set'=>$set,'model'=>get_option('nadlan_enc_writer_model'),
        'stat'=>get_option('nadlan_enc_writer_stat'));
    }));
});
