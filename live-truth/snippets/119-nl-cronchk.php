add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/cronchk', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      return array('renewals_next'=> wp_next_scheduled('nadlan_renewals_tick') ? date('Y-m-d H:i', wp_next_scheduled('nadlan_renewals_tick')) : 'NOT SCHEDULED');
    }));
});
