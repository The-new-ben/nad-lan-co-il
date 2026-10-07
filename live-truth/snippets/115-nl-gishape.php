add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/gishape', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      $o = get_option('greeninvoice_options');
      if (!is_array($o)) return array('type'=>gettype($o));
      $shape = array();
      foreach ($o as $k=>$v) {
        if (is_string($v)) { $shape[$k] = $v==='' ? 'EMPTY' : (substr($v,0,4).'... ('.strlen($v).')'); }
        else { $shape[$k] = gettype($v).(is_array($v)?'['.count($v).']':''); }
      }
      return $shape;
    }));
});
