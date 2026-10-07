add_action('rest_api_init', function () {
  register_rest_route('nadlan-fix', '/autoupdate-off', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can('manage_options'); },
    'callback' => function () {
      $p = 'nadlan-config/nadlan-config.php';
      $before = (array) get_option('auto_update_plugins', array());
      $after = array_values(array_diff($before, array($p)));
      update_option('auto_update_plugins', $after);
      $now = (array) get_option('auto_update_plugins', array());
      return array(
        'before' => $before,
        'after'  => $now,
        'nadlan_auto_update_now_off' => ! in_array($p, $now, true),
      );
    },
  ));
});