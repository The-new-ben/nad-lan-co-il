add_action('rest_api_init', function () {
  register_rest_route('nadlan-fix', '/brand-schema', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can('manage_options'); },
    'callback' => function () {
      $t = (array) get_option('wpseo_titles', array());
      $changed = array();
      foreach ( array('company_name','website_name','alternate_website_name','open_graph_frontpage_title') as $k ) {
        if ( isset($t[$k]) && is_string($t[$k]) && $t[$k] !== '' ) {
          $before = $t[$k];
          $t[$k] = str_replace(array('נדל"ן חכם','נדל״ן חכם','נדלן חכם'), 'נדלן', $t[$k]);
          if ( $before !== $t[$k] ) { $changed[$k] = $t[$k]; }
        }
      }
      if ( empty($t['company_name']) ) { $t['company_name'] = 'נדלן'; $changed['company_name'] = 'נדלן'; }
      update_option('wpseo_titles', $t);
      if ( class_exists('WPSEO_Options') ) { WPSEO_Options::clear_cache(); }
      return array('changed' => $changed);
    },
  ));
});