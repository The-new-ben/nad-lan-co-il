add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/gihunt2', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      global $wpdb;
      $rows = $wpdb->get_results("SELECT option_name, LENGTH(option_value) AS len, LEFT(option_value,4) AS head FROM {$wpdb->options} WHERE option_name LIKE '%gi\\_%' OR option_name LIKE '%green%' OR option_name LIKE '%invoice%' OR option_name LIKE '%morning%' OR option_name LIKE '%meshulam%' ORDER BY option_name", ARRAY_A);
      $direct = array();
      foreach (array('nadlan_gi_api_key','nadlan_gi_ipn_secret','nadlan_gi_sig_scheme','nadlan_gi_reconcile_url','nadlan_gi_plan_url_pro','nadlan_gi_plan_url_premier') as $k) {
        $v = get_option($k);
        $direct[$k] = (is_string($v) && $v!=='') ? (substr($v,0,4).'... ('.strlen($v).')') : 'EMPTY';
      }
      return array('direct'=>$direct,'scan'=>$rows);
    }));
});
