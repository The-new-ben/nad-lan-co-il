add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/gihunt', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      global $wpdb;
      $rows = $wpdb->get_results("SELECT option_name, LENGTH(option_value) AS len FROM {$wpdb->options} WHERE option_name LIKE '%gi_%' OR option_name LIKE '%green%' OR option_name LIKE '%invoice%' OR option_name LIKE '%morning%' OR option_name LIKE '%meshulam%' OR option_name LIKE '%payment%' ORDER BY option_name", ARRAY_A);
      $out = array();
      foreach ($rows as $r) {
        $v = (string) get_option($r['option_name']);
        $out[] = array('name'=>$r['option_name'],'len'=>(int)$r['len'],
          'shape'=> $v==='' ? 'EMPTY' : (is_serialized($v)?'serialized':substr($v,0,4).'...'));
      }
      // the exact fields the billing module reads
      $direct = array('nadlan_gi_api_key','nadlan_gi_ipn_secret','nadlan_gi_sig_scheme','nadlan_gi_reconcile_url');
      $d = array();
      foreach ($direct as $k) { $v=(string)get_option($k); $d[$k]= $v==='' ? 'EMPTY' : (substr($v,0,4).'... ('.strlen($v).' chars)'); }
      return array('direct'=>$d,'scan'=>$out);
    }));
});
