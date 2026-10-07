add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/regstate', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      return array(
        'users_can_register' => (bool) get_option('users_can_register'),
        'default_role' => get_option('default_role'),
        'gi_key_present' => get_option('nadlan_gi_key','') !== '' || get_option('nadlan_greeninvoice_key','') !== '',
      );
    }));
});
