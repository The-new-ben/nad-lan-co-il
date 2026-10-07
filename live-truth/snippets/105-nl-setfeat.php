add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/setfeat', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      $out=array();
      foreach ( array(4744,4464,4745,4893) as $id ) { update_post_meta($id,'project_featured','1'); $out[$id]=get_post_meta($id,'project_featured',true); }
      delete_transient('nadlan_project_map_v1'); do_action('litespeed_purge_all'); wp_cache_flush();
      return $out;
    }));
});
