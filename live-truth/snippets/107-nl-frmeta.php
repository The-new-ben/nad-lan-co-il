add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/frmeta', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function( WP_REST_Request $req ){
      $p = $req->get_json_params(); $id = (int) $p['id'];
      update_post_meta($id,'_yoast_wpseo_title',sanitize_text_field($p['yoast_title']));
      update_post_meta($id,'_yoast_wpseo_metadesc',sanitize_text_field($p['yoast_desc']));
      update_post_meta($id,'_yoast_wpseo_focuskw',sanitize_text_field($p['focuskw']));
      update_post_meta($id,'guide_faq_json',wp_slash($p['faq_json']));
      update_post_meta($id,'guide_lang','fr');
      do_action('litespeed_purge_all'); wp_cache_flush();
      return array('ok'=>true,'faq_items'=>count(json_decode($p['faq_json'],true)));
    }));
});
