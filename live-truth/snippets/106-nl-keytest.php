add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/keytest', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      $key = function_exists('nadlan_ai_openai_key') ? nadlan_ai_openai_key() : (string) get_option('nadlan_ai_openai_key','');
      if ($key==='') return array('ok'=>false,'why'=>'no key stored');
      $r = wp_remote_get('https://api.openai.com/v1/models', array('timeout'=>15,'headers'=>array('Authorization'=>'Bearer '.$key)));
      if (is_wp_error($r)) return array('ok'=>false,'why'=>$r->get_error_message());
      $code = wp_remote_retrieve_response_code($r);
      $n = 0;
      if ($code===200){ $b=json_decode(wp_remote_retrieve_body($r),true); $n=count($b['data']??array()); }
      return array('ok'=>$code===200,'http'=>$code,'models_visible'=>$n);
    }));
});
