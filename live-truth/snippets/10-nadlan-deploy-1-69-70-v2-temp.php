add_action('rest_api_init', function () {
  register_rest_route('nadlan-deploy', '/run', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can('update_plugins'); },
    'callback' => function () {
      require_once ABSPATH . 'wp-admin/includes/file.php';
      require_once ABSPATH . 'wp-admin/includes/misc.php';
      require_once ABSPATH . 'wp-admin/includes/plugin.php';
      require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
      $p = 'nadlan-config/nadlan-config.php';
      $u = 'https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config-1.69.70.zip';
      $s = new WP_Ajax_Upgrader_Skin();
      $up = new Plugin_Upgrader($s);
      $ok = $up->install($u, array('overwrite_package' => true));
      if ( ! is_plugin_active($p) ) { activate_plugin($p); }
      flush_rewrite_rules();
      if ( ! function_exists('get_plugin_data') ) { require_once ABSPATH.'wp-admin/includes/plugin.php'; }
      $data = get_plugin_data(WP_PLUGIN_DIR.'/'.$p, false, false);
      return array(
        'result' => is_wp_error($ok) ? ('ERR:'.$ok->get_error_message()) : var_export($ok, true),
        'installed_version' => isset($data['Version']) ? $data['Version'] : null,
        'active' => is_plugin_active($p),
        'messages' => $s->get_upgrade_messages(),
      );
    },
  ));
});