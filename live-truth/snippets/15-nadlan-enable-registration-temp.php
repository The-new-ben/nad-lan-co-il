add_action('rest_api_init', function () {
  register_rest_route('nadlan-fix', '/registration', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can('manage_options'); },
    'callback' => function () {
      update_option('users_can_register', 1);
      update_option('default_role', 'subscriber');
      return array('users_can_register' => (int) get_option('users_can_register'), 'default_role' => get_option('default_role'));
    },
  ));
});