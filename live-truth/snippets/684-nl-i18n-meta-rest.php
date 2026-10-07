// nl-i18n: REST access to the language map (nl_hreflang) and to Yoast title/description for the broker minisites (nad-lan, 17.9.2026).
// The portal itself prints the hreflang alternates from nl_hreflang; this snippet does not print anything.
add_action('init', function () {
    $auth = function () { return current_user_can('edit_posts'); };
    foreach (['page', 'nadlan_property'] as $type) {
        register_post_meta($type, 'nl_hreflang', ['type' => 'string', 'single' => true, 'show_in_rest' => true, 'auth_callback' => $auth]);
        foreach (['_yoast_wpseo_title', '_yoast_wpseo_metadesc'] as $k) {
            register_post_meta($type, $k, ['type' => 'string', 'single' => true, 'show_in_rest' => true, 'auth_callback' => $auth]);
        }
    }
}, 20);