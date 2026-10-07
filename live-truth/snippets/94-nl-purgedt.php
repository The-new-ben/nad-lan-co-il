add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/purgedt', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){ delete_transient('nadlan_default_tour_v1'); do_action('litespeed_purge_all'); wp_cache_flush(); return array('r'=>'ok'); }));
});
