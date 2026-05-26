<?php
/**
 * NadLan Revenue theme functions.
 */

if (!defined('ABSPATH')) {
    exit;
}

function nadlan_revenue_setup(): void {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', ['search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script']);
    register_nav_menus([
        'primary' => __('Primary Menu', 'nadlan-revenue'),
    ]);
}
add_action('after_setup_theme', 'nadlan_revenue_setup');

function nadlan_revenue_assets(): void {
    wp_enqueue_style('nadlan-revenue-style', get_stylesheet_uri(), [], wp_get_theme()->get('Version'));
}
add_action('wp_enqueue_scripts', 'nadlan_revenue_assets');

function nadlan_revenue_register_lead_type(): void {
    register_post_type('nadlan_lead', [
        'labels' => [
            'name' => __('NadLan Leads', 'nadlan-revenue'),
            'singular_name' => __('NadLan Lead', 'nadlan-revenue'),
        ],
        'public' => false,
        'show_ui' => true,
        'show_in_menu' => true,
        'menu_icon' => 'dashicons-money-alt',
        'supports' => ['title', 'editor', 'custom-fields'],
    ]);
}
add_action('init', 'nadlan_revenue_register_lead_type');

function nadlan_revenue_clean(string $key): string {
    return isset($_POST[$key]) ? sanitize_text_field(wp_unslash($_POST[$key])) : '';
}

function nadlan_revenue_handle_lead(): void {
    if (!isset($_POST['nadlan_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['nadlan_nonce'])), 'nadlan_lead')) {
        wp_safe_redirect(add_query_arg('lead', 'bad_nonce', home_url('/')));
        exit;
    }

    $name = nadlan_revenue_clean('lead_name');
    $phone = nadlan_revenue_clean('lead_phone');
    $email = sanitize_email(wp_unslash($_POST['lead_email'] ?? ''));
    $goal = nadlan_revenue_clean('lead_goal');
    $city = nadlan_revenue_clean('lead_city');
    $budget = nadlan_revenue_clean('lead_budget');
    $timeline = nadlan_revenue_clean('lead_timeline');
    $message = sanitize_textarea_field(wp_unslash($_POST['lead_message'] ?? ''));

    $title = sprintf('%s - %s - %s', $name ?: 'Lead', $goal ?: 'General', current_time('Y-m-d H:i'));
    $lead_id = wp_insert_post([
        'post_type' => 'nadlan_lead',
        'post_status' => 'private',
        'post_title' => $title,
        'post_content' => $message,
    ], true);

    if (!is_wp_error($lead_id)) {
        $fields = [
            'name' => $name,
            'phone' => $phone,
            'email' => $email,
            'goal' => $goal,
            'city' => $city,
            'budget' => $budget,
            'timeline' => $timeline,
            'source_url' => esc_url_raw(wp_get_referer() ?: home_url('/')),
            'utm_source' => nadlan_revenue_clean('utm_source'),
            'utm_campaign' => nadlan_revenue_clean('utm_campaign'),
        ];
        foreach ($fields as $key => $value) {
            update_post_meta($lead_id, $key, $value);
        }

        $admin_email = get_option('admin_email');
        wp_mail($admin_email, 'NadLan lead: ' . $title, print_r($fields, true));
    }

    wp_safe_redirect(add_query_arg('lead', 'received', home_url('/')));
    exit;
}
add_action('admin_post_nopriv_nadlan_lead', 'nadlan_revenue_handle_lead');
add_action('admin_post_nadlan_lead', 'nadlan_revenue_handle_lead');

function nadlan_revenue_schema(): void {
    if (!is_front_page()) {
        return;
    }
    $schema = [
        '@context' => 'https://schema.org',
        '@type' => 'WebSite',
        'name' => 'NadLan',
        'url' => home_url('/'),
        'inLanguage' => 'he-IL',
        'potentialAction' => [
            '@type' => 'SearchAction',
            'target' => home_url('/?s={search_term_string}'),
            'query-input' => 'required name=search_term_string',
        ],
    ];
    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . '</script>';
}
add_action('wp_head', 'nadlan_revenue_schema');
