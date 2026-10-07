add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/encdiag', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      $key = function_exists('nadlan_ai_openai_key') ? nadlan_ai_openai_key() : '';
      $resp = wp_remote_post('https://api.openai.com/v1/chat/completions', array(
        'timeout'=>60,
        'headers'=>array('Authorization'=>'Bearer '.$key,'Content-Type'=>'application/json'),
        'body'=>wp_json_encode(array(
          'model'=>(string)get_option('nadlan_enc_writer_model','gpt-4o-mini'),
          'temperature'=>0.4,'max_tokens'=>3000,
          'messages'=>array(array('role'=>'user','content'=>'כתוב פסקה אחת של 60 מילים על בטון מזוין.')),
        )),
      ));
      if (is_wp_error($resp)) return array('wp_error'=>$resp->get_error_message());
      $code = wp_remote_retrieve_response_code($resp);
      $body = json_decode(wp_remote_retrieve_body($resp), true);
      $err  = $body['error']['message'] ?? '';
      $txt  = $body['choices'][0]['message']['content'] ?? '';
      return array('http'=>$code,'error'=>substr((string)$err,0,300),'sample_words'=>count(preg_split('/\s+/',trim($txt))));
    }));
});
