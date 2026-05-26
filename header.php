<?php
/**
 * Theme header.
 */
?><!doctype html>
<html <?php language_attributes(); ?> dir="rtl">
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<div class="site-shell">
<header class="site-header">
    <div class="container header-inner">
        <a class="logo" href="<?php echo esc_url(home_url('/')); ?>" aria-label="NadLan home">
            <span class="logo-mark">נ</span>
            <span><?php bloginfo('name'); ?></span>
        </a>
        <nav class="nav" aria-label="ניווט ראשי">
            <?php
            if (has_nav_menu('primary')) {
                wp_nav_menu([
                    'theme_location' => 'primary',
                    'container' => false,
                    'items_wrap' => '%3$s',
                    'fallback_cb' => false,
                ]);
            } else {
                echo '<a href="#tools">מחשבונים</a><a href="/buying-apartment/">קניית דירה</a><a href="/real-estate-lawyer/">עורך דין מקרקעין</a>';
            }
            ?>
        </nav>
        <a class="header-cta" href="#lead">בדיקת התאמה</a>
    </div>
</header>
