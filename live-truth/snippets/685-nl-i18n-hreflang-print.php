// nl-i18n-hreflang-print (nad-lan, 17.9.2026)
// WHY: inc/page-lang.php builds the language cluster from PATH SYMMETRY - Hebrew at
// /<rest>/ and the translation at /<lang>/<rest>/ - and prints only for is_page().
// A broker listing pair is not symmetrical: Hebrew lives on nadlan_property at
// /properties/<slug>/ while English lives on a page at /en/brokers/<broker>/<slug>/.
// So neither side printed alternates. This prints them from the post meta
// nl_hreflang (JSON of lang => url, written by runners/meital_site.py), and stays
// silent wherever the portal's own printer already prints.
add_action('wp_head', function () {
    if (!is_singular(array('page', 'nadlan_property'))) {
        return;
    }
    $id = get_queried_object_id();
    // the portal already printed a cluster for this page: never print twice
    if (is_page() && function_exists('nadlan_pglang_family')) {
        $fam = nadlan_pglang_family($id);
        if (is_array($fam) && count($fam) >= 2 && !empty($fam['he'])) {
            return;
        }
    }
    $raw = get_post_meta($id, 'nl_hreflang', true);
    if (!is_string($raw) || '' === $raw) {
        return;
    }
    $map = json_decode($raw, true);
    if (!is_array($map) || count($map) < 2 || empty($map['he'])) {
        return;
    }
    echo "\n<!-- listing language cluster -->\n";
    foreach ($map as $lang => $url) {
        if (!is_string($lang) || !is_string($url) || '' === $url) {
            continue;
        }
        printf('<link rel="alternate" hreflang="%s" href="%s" />' . "\n", esc_attr($lang), esc_url($url));
    }
    printf('<link rel="alternate" hreflang="x-default" href="%s" />' . "\n", esc_url($map['he']));
}, 4);
