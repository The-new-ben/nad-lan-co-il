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
    add_theme_support('editor-styles');
    add_theme_support('html5', ['search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script']);
    add_editor_style('style.css');
    register_nav_menus([
        'primary' => __('Primary Menu', 'nadlan-revenue'),
    ]);
}
add_action('after_setup_theme', 'nadlan_revenue_setup');

function nadlan_revenue_assets(): void {
    wp_enqueue_style('nadlan-revenue-style', get_stylesheet_uri(), [], wp_get_theme()->get('Version'));
}
add_action('wp_enqueue_scripts', 'nadlan_revenue_assets');

function nadlan_revenue_lead_statuses(): array {
    return [
        'new' => __('New', 'nadlan-revenue'),
        'qualified' => __('Qualified', 'nadlan-revenue'),
        'contacted' => __('Contacted', 'nadlan-revenue'),
        'partner_sent' => __('Sent to partner', 'nadlan-revenue'),
        'closed_won' => __('Closed won', 'nadlan-revenue'),
        'closed_lost' => __('Closed lost', 'nadlan-revenue'),
    ];
}

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

    $meta_fields = [
        'lead_name',
        'lead_phone',
        'lead_email',
        'lead_goal',
        'lead_city',
        'lead_budget',
        'lead_timeline',
        'lead_consent',
        'lead_status',
        'landing_url',
        'referrer_url',
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_term',
        'utm_content',
    ];

    foreach ($meta_fields as $field) {
        register_post_meta('nadlan_lead', $field, [
            'type' => 'string',
            'single' => true,
            'show_in_rest' => true,
            'sanitize_callback' => 'sanitize_text_field',
            'auth_callback' => static function (): bool {
                return current_user_can('edit_posts');
            },
        ]);
    }
}
add_action('init', 'nadlan_revenue_register_lead_type');

function nadlan_revenue_clean(string $key): string {
    return isset($_POST[$key]) ? sanitize_text_field(wp_unslash($_POST[$key])) : '';
}

function nadlan_revenue_clean_url(string $key): string {
    return isset($_POST[$key]) ? esc_url_raw(wp_unslash($_POST[$key])) : '';
}

function nadlan_revenue_initial_status(string $goal, string $city, string $budget, string $timeline): string {
    $signals = 0;

    foreach ([$goal, $city, $budget, $timeline] as $value) {
        if ($value !== '') {
            $signals++;
        }
    }

    return $signals >= 2 ? 'qualified' : 'new';
}

function nadlan_revenue_handle_lead(): void {
    if (!isset($_POST['nadlan_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['nadlan_nonce'])), 'nadlan_lead')) {
        wp_safe_redirect(add_query_arg('lead', 'bad_nonce', home_url('/')));
        exit;
    }

    if (nadlan_revenue_clean('company_website') !== '') {
        wp_safe_redirect(add_query_arg('lead', 'received', home_url('/')));
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
    $consent = isset($_POST['lead_consent']) ? 'yes' : '';

    if ($name === '' || $phone === '' || $consent !== 'yes') {
        wp_safe_redirect(add_query_arg('lead', 'missing_required', home_url('/#lead')));
        exit;
    }

    $initial_status = nadlan_revenue_initial_status($goal, $city, $budget, $timeline);

    $title = sprintf('%s - %s - %s', $name ?: 'Lead', $goal ?: 'General', current_time('Y-m-d H:i'));
    $lead_id = wp_insert_post([
        'post_type' => 'nadlan_lead',
        'post_status' => 'private',
        'post_title' => $title,
        'post_content' => $message,
    ], true);

    if (!is_wp_error($lead_id)) {
        $fields = [
            'lead_name' => $name,
            'lead_phone' => $phone,
            'lead_email' => $email,
            'lead_goal' => $goal,
            'lead_city' => $city,
            'lead_budget' => $budget,
            'lead_timeline' => $timeline,
            'lead_consent' => $consent,
            'lead_status' => $initial_status,
            'landing_url' => nadlan_revenue_clean_url('landing_url') ?: home_url('/'),
            'referrer_url' => nadlan_revenue_clean_url('referrer_url') ?: esc_url_raw(wp_get_referer() ?: ''),
            'utm_source' => nadlan_revenue_clean('utm_source'),
            'utm_medium' => nadlan_revenue_clean('utm_medium'),
            'utm_campaign' => nadlan_revenue_clean('utm_campaign'),
            'utm_term' => nadlan_revenue_clean('utm_term'),
            'utm_content' => nadlan_revenue_clean('utm_content'),
        ];
        foreach ($fields as $key => $value) {
            update_post_meta($lead_id, $key, $value);
        }

        $admin_email = get_option('admin_email');
        wp_mail($admin_email, 'NadLan lead: ' . $title, wp_json_encode($fields, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
    }

    wp_safe_redirect(add_query_arg('lead', 'received', home_url('/')));
    exit;
}
add_action('admin_post_nopriv_nadlan_lead', 'nadlan_revenue_handle_lead');
add_action('admin_post_nadlan_lead', 'nadlan_revenue_handle_lead');

function nadlan_revenue_lead_columns(array $columns): array {
    $new_columns = [];
    foreach ($columns as $key => $label) {
        $new_columns[$key] = $label;
        if ($key === 'title') {
            $new_columns['lead_phone'] = __('Phone', 'nadlan-revenue');
            $new_columns['lead_goal'] = __('Goal', 'nadlan-revenue');
            $new_columns['lead_city'] = __('City', 'nadlan-revenue');
            $new_columns['lead_status'] = __('Status', 'nadlan-revenue');
            $new_columns['utm_source'] = __('UTM source', 'nadlan-revenue');
            $new_columns['landing_url'] = __('Landing URL', 'nadlan-revenue');
        }
    }
    return $new_columns;
}
add_filter('manage_nadlan_lead_posts_columns', 'nadlan_revenue_lead_columns');

function nadlan_revenue_lead_column_content(string $column, int $post_id): void {
    if (in_array($column, ['lead_phone', 'lead_goal', 'lead_city', 'utm_source', 'landing_url'], true)) {
        echo esc_html((string) get_post_meta($post_id, $column, true));
        return;
    }

    if ($column === 'lead_status') {
        $statuses = nadlan_revenue_lead_statuses();
        $status = (string) get_post_meta($post_id, 'lead_status', true);
        echo esc_html($statuses[$status] ?? $status);
    }
}
add_action('manage_nadlan_lead_posts_custom_column', 'nadlan_revenue_lead_column_content', 10, 2);

function nadlan_revenue_lead_meta_box(): void {
    add_meta_box(
        'nadlan_lead_details',
        __('Lead details', 'nadlan-revenue'),
        'nadlan_revenue_render_lead_meta_box',
        'nadlan_lead',
        'normal',
        'high'
    );
}
add_action('add_meta_boxes_nadlan_lead', 'nadlan_revenue_lead_meta_box');

function nadlan_revenue_render_lead_meta_box(WP_Post $post): void {
    wp_nonce_field('nadlan_lead_admin', 'nadlan_lead_admin_nonce');
    $statuses = nadlan_revenue_lead_statuses();
    $current_status = (string) get_post_meta($post->ID, 'lead_status', true);
    $rows = [
        __('Name', 'nadlan-revenue') => get_post_meta($post->ID, 'lead_name', true),
        __('Phone', 'nadlan-revenue') => get_post_meta($post->ID, 'lead_phone', true),
        __('Email', 'nadlan-revenue') => get_post_meta($post->ID, 'lead_email', true),
        __('Goal', 'nadlan-revenue') => get_post_meta($post->ID, 'lead_goal', true),
        __('City', 'nadlan-revenue') => get_post_meta($post->ID, 'lead_city', true),
        __('Budget', 'nadlan-revenue') => get_post_meta($post->ID, 'lead_budget', true),
        __('Timeline', 'nadlan-revenue') => get_post_meta($post->ID, 'lead_timeline', true),
        __('Landing URL', 'nadlan-revenue') => get_post_meta($post->ID, 'landing_url', true),
        __('Referrer URL', 'nadlan-revenue') => get_post_meta($post->ID, 'referrer_url', true),
        __('UTM source', 'nadlan-revenue') => get_post_meta($post->ID, 'utm_source', true),
        __('UTM campaign', 'nadlan-revenue') => get_post_meta($post->ID, 'utm_campaign', true),
    ];
    ?>
    <p>
        <label for="lead_status"><strong><?php esc_html_e('Status', 'nadlan-revenue'); ?></strong></label>
        <select id="lead_status" name="lead_status">
            <?php foreach ($statuses as $value => $label) : ?>
                <option value="<?php echo esc_attr($value); ?>" <?php selected($current_status ?: 'new', $value); ?>><?php echo esc_html($label); ?></option>
            <?php endforeach; ?>
        </select>
    </p>
    <table class="widefat striped">
        <tbody>
            <?php foreach ($rows as $label => $value) : ?>
                <tr>
                    <th scope="row"><?php echo esc_html($label); ?></th>
                    <td><?php echo esc_html((string) $value); ?></td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
    <?php
}

function nadlan_revenue_save_lead_status(int $post_id): void {
    if (!isset($_POST['nadlan_lead_admin_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['nadlan_lead_admin_nonce'])), 'nadlan_lead_admin')) {
        return;
    }

    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }

    if (!current_user_can('edit_post', $post_id)) {
        return;
    }

    $status = nadlan_revenue_clean('lead_status');
    if (array_key_exists($status, nadlan_revenue_lead_statuses())) {
        update_post_meta($post_id, 'lead_status', $status);
    }
}
add_action('save_post_nadlan_lead', 'nadlan_revenue_save_lead_status');

function nadlan_revenue_lead_board_menu(): void {
    add_submenu_page(
        'edit.php?post_type=nadlan_lead',
        __('Revenue Board', 'nadlan-revenue'),
        __('Revenue Board', 'nadlan-revenue'),
        'edit_posts',
        'nadlan-revenue-board',
        'nadlan_revenue_render_lead_board'
    );
}
add_action('admin_menu', 'nadlan_revenue_lead_board_menu');

function nadlan_revenue_render_lead_board(): void {
    $statuses = nadlan_revenue_lead_statuses();
    $leads = get_posts([
        'post_type' => 'nadlan_lead',
        'post_status' => 'private',
        'numberposts' => 50,
        'orderby' => 'date',
        'order' => 'DESC',
    ]);

    $status_counts = array_fill_keys(array_values($statuses), 0);
    $source_counts = [];
    $landing_counts = [];

    foreach ($leads as $lead) {
        $status_key = (string) get_post_meta($lead->ID, 'lead_status', true);
        $status_label = $statuses[$status_key ?: 'new'] ?? $status_key;
        $status_counts[$status_label] = ($status_counts[$status_label] ?? 0) + 1;

        $source = trim((string) get_post_meta($lead->ID, 'utm_source', true)) ?: __('Direct / unknown', 'nadlan-revenue');
        $landing = trim((string) get_post_meta($lead->ID, 'landing_url', true)) ?: __('Home / unknown', 'nadlan-revenue');
        $source_counts[$source] = ($source_counts[$source] ?? 0) + 1;
        $landing_counts[$landing] = ($landing_counts[$landing] ?? 0) + 1;
    }

    $status_counts = array_filter($status_counts, static function ($count): bool {
        return (int) $count > 0;
    });
    arsort($status_counts);
    arsort($source_counts);
    arsort($landing_counts);

    $render_counts = static function (array $counts, string $empty_label): void {
        if (!$counts) {
            echo '<tr><td colspan="2">' . esc_html($empty_label) . '</td></tr>';
            return;
        }

        foreach (array_slice($counts, 0, 10, true) as $label => $count) {
            echo '<tr><td style="word-break: break-word;">' . esc_html((string) $label) . '</td><td>' . esc_html(number_format_i18n((int) $count)) . '</td></tr>';
        }
    };
    ?>
    <div class="wrap">
        <h1><?php esc_html_e('Revenue Board', 'nadlan-revenue'); ?></h1>
        <p><?php esc_html_e('Last 50 private leads by status, source, and landing page for weekly revenue triage.', 'nadlan-revenue'); ?></p>
        <p><a class="button button-primary" href="<?php echo esc_url(wp_nonce_url(admin_url('admin-post.php?action=nadlan_export_lead_board'), 'nadlan_export_lead_board')); ?>"><?php esc_html_e('Export board CSV', 'nadlan-revenue'); ?></a></p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 16px 0;">
            <div class="card" style="max-width: none;">
                <h2><?php esc_html_e('Status', 'nadlan-revenue'); ?></h2>
                <table class="widefat striped"><tbody><?php $render_counts($status_counts, __('No leads yet.', 'nadlan-revenue')); ?></tbody></table>
            </div>
            <div class="card" style="max-width: none;">
                <h2><?php esc_html_e('UTM source', 'nadlan-revenue'); ?></h2>
                <table class="widefat striped"><tbody><?php $render_counts($source_counts, __('No source data yet.', 'nadlan-revenue')); ?></tbody></table>
            </div>
            <div class="card" style="max-width: none;">
                <h2><?php esc_html_e('Landing URL', 'nadlan-revenue'); ?></h2>
                <table class="widefat striped"><tbody><?php $render_counts($landing_counts, __('No landing data yet.', 'nadlan-revenue')); ?></tbody></table>
            </div>
        </div>
        <h2><?php esc_html_e('Latest leads', 'nadlan-revenue'); ?></h2>
        <table class="widefat striped">
            <thead>
                <tr>
                    <th scope="col"><?php esc_html_e('Date', 'nadlan-revenue'); ?></th>
                    <th scope="col"><?php esc_html_e('Lead', 'nadlan-revenue'); ?></th>
                    <th scope="col"><?php esc_html_e('Status', 'nadlan-revenue'); ?></th>
                    <th scope="col"><?php esc_html_e('UTM source', 'nadlan-revenue'); ?></th>
                    <th scope="col"><?php esc_html_e('Landing URL', 'nadlan-revenue'); ?></th>
                </tr>
            </thead>
            <tbody>
                <?php if (!$leads) : ?>
                    <tr><td colspan="5"><?php esc_html_e('No leads yet.', 'nadlan-revenue'); ?></td></tr>
                <?php endif; ?>
                <?php foreach ($leads as $lead) : ?>
                    <?php
                    $status_key = (string) get_post_meta($lead->ID, 'lead_status', true);
                    $landing_url = (string) get_post_meta($lead->ID, 'landing_url', true);
                    $lead_title = get_the_title($lead) ?: sprintf(__('Lead #%d', 'nadlan-revenue'), $lead->ID);
                    ?>
                    <tr>
                        <td><?php echo esc_html(get_the_date('', $lead)); ?></td>
                        <td><a href="<?php echo esc_url((string) get_edit_post_link($lead->ID)); ?>"><?php echo esc_html($lead_title); ?></a></td>
                        <td><?php echo esc_html($statuses[$status_key ?: 'new'] ?? $status_key); ?></td>
                        <td><?php echo esc_html((string) get_post_meta($lead->ID, 'utm_source', true)); ?></td>
                        <td style="word-break: break-all;"><?php echo $landing_url ? '<a href="' . esc_url($landing_url) . '" target="_blank" rel="noopener">' . esc_html($landing_url) . '</a>' : esc_html__('Home / unknown', 'nadlan-revenue'); ?></td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <?php
}

function nadlan_revenue_export_lead_board(): void {
    if (!current_user_can('edit_posts')) {
        wp_die(esc_html__('You are not allowed to export this board.', 'nadlan-revenue'));
    }

    check_admin_referer('nadlan_export_lead_board');

    $statuses = nadlan_revenue_lead_statuses();
    $leads = get_posts([
        'post_type' => 'nadlan_lead',
        'post_status' => 'private',
        'numberposts' => 50,
        'orderby' => 'date',
        'order' => 'DESC',
    ]);

    nocache_headers();
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="nadlan-lead-board-' . gmdate('Y-m-d') . '.csv"');

    $output = fopen('php://output', 'w');
    if ($output === false) {
        wp_die(esc_html__('Could not open CSV output stream.', 'nadlan-revenue'));
    }

    fputcsv($output, ['lead_id', 'date', 'status', 'utm_source', 'utm_medium', 'utm_campaign', 'landing_url', 'edit_url']);

    foreach ($leads as $lead) {
        $status_key = (string) get_post_meta($lead->ID, 'lead_status', true);
        fputcsv($output, [
            $lead->ID,
            get_the_date('Y-m-d H:i:s', $lead),
            $statuses[$status_key ?: 'new'] ?? $status_key,
            get_post_meta($lead->ID, 'utm_source', true),
            get_post_meta($lead->ID, 'utm_medium', true),
            get_post_meta($lead->ID, 'utm_campaign', true),
            get_post_meta($lead->ID, 'landing_url', true),
            get_edit_post_link($lead->ID, 'raw'),
        ]);
    }

    fclose($output);
    exit;
}
add_action('admin_post_nadlan_export_lead_board', 'nadlan_revenue_export_lead_board');

function nadlan_revenue_schema(): void {
    if (!is_front_page()) {
        return;
    }
    $schema = [
        '@context' => 'https://schema.org',
        '@type' => 'RealEstateAgent',
        'name' => 'NadLan',
        'url' => home_url('/'),
        'areaServed' => 'IL',
        'inLanguage' => 'he-IL',
        'serviceType' => ['Real estate buyer guidance', 'Mortgage and purchase tax lead routing'],
    ];
    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . '</script>';
}
add_action('wp_head', 'nadlan_revenue_schema');

function nadlan_revenue_attribution_script(): void {
    if (!is_front_page()) {
        return;
    }
    ?>
    <script>
    (function () {
        var params = new URLSearchParams(window.location.search);
        var keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
        keys.forEach(function (key) {
            var value = params.get(key) || window.localStorage.getItem('nadlan_' + key) || '';
            if (params.get(key)) {
                window.localStorage.setItem('nadlan_' + key, params.get(key));
            }
            var input = document.querySelector('[name="' + key + '"]');
            if (input) {
                input.value = value;
            }
        });
        var landing = document.querySelector('[name="landing_url"]');
        var referrer = document.querySelector('[name="referrer_url"]');
        if (landing) {
            landing.value = window.location.href;
        }
        if (referrer) {
            referrer.value = document.referrer;
        }
    }());
    </script>
    <?php
}
add_action('wp_footer', 'nadlan_revenue_attribution_script');

function nadlan_revenue_conversion_event_script(): void {
    if (!is_front_page() || !isset($_GET['lead']) || sanitize_text_field(wp_unslash($_GET['lead'])) !== 'received') {
        return;
    }

    $payload = [
        'event' => 'generate_lead',
        'lead_form' => 'nadlan_lead',
        'portfolio_site' => 'nad-lan.co.il',
        'lead_result' => 'received',
        'conversion_source' => 'wordpress_thank_you_query',
    ];
    ?>
    <script>
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(<?php echo wp_json_encode($payload); ?>);
    </script>
    <?php
}
add_action('wp_footer', 'nadlan_revenue_conversion_event_script');
