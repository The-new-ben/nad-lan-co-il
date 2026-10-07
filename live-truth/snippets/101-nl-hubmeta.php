add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/hubmeta', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      $id = 5154;
      update_post_meta($id,'_yoast_wpseo_title','Buying Property in Israel from Abroad 2026: Taxes, Process, 3D Apartments');
      update_post_meta($id,'_yoast_wpseo_metadesc','Buy property in Israel from abroad: 2026 purchase tax for foreign buyers, non-resident mortgages, the Sale Law protection, and 3D apartment selection you can do from anywhere.');
      update_post_meta($id,'_yoast_wpseo_focuskw','buy property in israel from abroad');
      do_action('litespeed_purge_all'); wp_cache_flush();
      return array('ok'=>true);
    }));
});
