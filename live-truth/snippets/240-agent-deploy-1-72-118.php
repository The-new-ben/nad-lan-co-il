add_action( 'rest_api_init', function () {
  register_rest_route( 'agentdeploy/v1', '/run', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
    'callback' => function () {
      require_once ABSPATH . 'wp-admin/includes/file.php';
      require_once ABSPATH . 'wp-admin/includes/misc.php';
      require_once ABSPATH . 'wp-admin/includes/plugin.php';
      require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
      $plugin = 'nadlan-config/nadlan-config.php';
      $zip = 'https://nad-lan.co.il/wp-content/uploads/2026/07/nadlan-config-1.72.118.zip?nlcb=' . time();
      $skin = new WP_Ajax_Upgrader_Skin();
      $up = new Plugin_Upgrader( $skin );
      $ok = $up->install( $zip, array( 'overwrite_package' => true ) );
      if ( ! is_plugin_active( $plugin ) ) { activate_plugin( $plugin ); }
      do_action( 'litespeed_purge_all' ); wp_cache_flush();
      return array( 'result' => is_wp_error( $ok ) ? $ok->get_error_message() : var_export( $ok, true ),
                     'active' => is_plugin_active( $plugin ) );
    },
  ) );
} );
