add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/gigw', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      $o = get_option('greeninvoice_options');
      $g = is_array($o) && isset($o['gateways']) ? $o['gateways'] : array();
      $out = array();
      foreach ((array)$g as $gk=>$gv) {
        if (!is_array($gv)) { $out[$gk]=gettype($gv); continue; }
        $row=array();
        foreach ($gv as $k=>$v) {
          if (is_string($v)) { $row[$k] = $v==='' ? 'EMPTY' : (substr($v,0,4).'... ('.strlen($v).')'); }
          else { $row[$k]=gettype($v); }
        }
        $out[$gk]=$row;
      }
      $plugins = get_option('active_plugins');
      return array('gateways'=>$out,'woocommerce_active'=> is_array($plugins) && (bool)preg_grep('/woocommerce/',$plugins),
        'active_plugins'=>array_values(array_filter((array)$plugins,function($p){return stripos($p,'green')!==false||stripos($p,'woo')!==false;})));
    }));
});
