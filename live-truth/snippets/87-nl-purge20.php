add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-purge/v1', '/run', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){ do_action('litespeed_purge_all'); wp_cache_flush(); return array('r'=>'purged'); }));
});
