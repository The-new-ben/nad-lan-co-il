add_action('rest_api_init', function () {
  register_rest_route('nadlan-fix', '/contact', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can('manage_options'); },
    'callback' => function () {
      // Owner WhatsApp already public in shipped code (listings-ux wa.me link)
      update_option('nadlan_whatsapp_e164', '972525101555');
      update_option('nadlan_phone', '052-510-1555');
      update_option('nadlan_owner_whatsapp', '972525101555');
      return array('whatsapp' => get_option('nadlan_whatsapp_e164'), 'phone' => get_option('nadlan_phone'), 'cta_wa' => get_option('nadlan_owner_whatsapp'));
    },
  ));
});