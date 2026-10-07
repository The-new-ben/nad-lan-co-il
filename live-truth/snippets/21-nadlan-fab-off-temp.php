add_action('rest_api_init', function () {
  register_rest_route('nadlan-fix', '/fab-off', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can('manage_options'); },
    'callback' => function () { update_option('nadlan_ai_enabled', 0); return array('nadlan_ai_enabled' => (int) get_option('nadlan_ai_enabled')); },
  ));
});