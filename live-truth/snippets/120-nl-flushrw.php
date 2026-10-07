add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/flushrw', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      $before = (bool) get_option('rewrite_rules');
      flush_rewrite_rules( true );
      do_action('litespeed_purge_all'); wp_cache_flush();
      $rules = get_option('rewrite_rules');
      $proj = 0;
      foreach ( (array) $rules as $k => $v ) { if ( strpos( $k, 'projects' ) !== false ) { $proj++; } }
      return array('had_rules_before'=>$before,'rules_now'=>count((array)$rules),'project_rules'=>$proj,
        'cpt_registered'=> post_type_exists('nadlan_project'));
    }));
});
