add_action('rest_api_init', function () {
  register_rest_route('nadlan-deploy', '/run', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can('update_plugins'); },
    'callback' => function () {
      require_once ABSPATH . 'wp-admin/includes/file.php';
      require_once ABSPATH . 'wp-admin/includes/misc.php';
      require_once ABSPATH . 'wp-admin/includes/plugin.php';
      require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
      $plugin = 'nadlan-config/nadlan-config.php';
      $url = 'https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config-1.69.69.zip';
      $t = get_site_transient('update_plugins');
      if ( ! is_object($t) ) { $t = new stdClass(); }
      if ( empty($t->response) || ! is_array($t->response) ) { $t->response = array(); }
      $t->response[$plugin] = (object) array('slug'=>'nadlan-config','plugin'=>$plugin,'new_version'=>'1.69.69','package'=>$url,'url'=>'https://nad-lan.co.il');
      set_site_transient('update_plugins', $t);
      $skin = new WP_Ajax_Upgrader_Skin();
      $up = new Plugin_Upgrader($skin);
      $ok = $up->upgrade($plugin);
      if ( ! is_plugin_active($plugin) ) { activate_plugin($plugin); }
      return array(
        'result' => is_wp_error($ok) ? ('ERR:'.$ok->get_error_message()) : var_export($ok, true),
        'messages' => $skin->get_upgrade_messages(),
      );
    },
  ));
});