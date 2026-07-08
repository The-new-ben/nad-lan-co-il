<?php
/**
 * Script to deploy HTML mockups as WordPress Draft Pages
 * Usage: wp eval-file deploy_drafts.php
 */

$mockups_dir = dirname(__DIR__) . '/draft-mockups';
if (!is_dir($mockups_dir)) {
    WP_CLI::error("Draft mockups directory not found: $mockups_dir");
}

$files = glob($mockups_dir . '/*.html');

foreach ($files as $file) {
    $basename = basename($file, '.html');
    $title = "Mockup: " . ucwords(str_replace('-', ' ', $basename));
    $content = file_get_contents($file);

    // Check if draft already exists
    $existing = get_page_by_title($title, OBJECT, 'page');
    
    if ($existing) {
        $post_id = wp_update_post([
            'ID' => $existing->ID,
            'post_content' => $content,
            'post_status' => 'draft'
        ]);
        WP_CLI::success("Updated Draft: $title (ID: $post_id) - Preview: " . get_preview_post_link($post_id));
    } else {
        $post_id = wp_insert_post([
            'post_title' => $title,
            'post_content' => $content,
            'post_type' => 'page',
            'post_status' => 'draft'
        ]);
        WP_CLI::success("Created Draft: $title (ID: $post_id) - Preview: " . get_preview_post_link($post_id));
    }
}
WP_CLI::success("Deployment complete.");
