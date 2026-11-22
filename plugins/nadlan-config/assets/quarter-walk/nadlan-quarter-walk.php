<?php
/**
 * Plugin Name: Nadlan Quarter Walk
 * Description: A street photograph from the local tour and an on-demand walk for a WordPress page.
 * Version: 1.1.0
 * Requires PHP: 7.4
 */
defined('ABSPATH') || exit;

function nadlan_walk_styles() {
    $handle = 'nadlan-quarter-walk';
    if (wp_style_is($handle, 'registered')) return;
    $url = plugin_dir_url(__FILE__);
    $css = file_get_contents(__DIR__ . '/walk.css');
    if ($css === false) {
        wp_register_style($handle, $url . 'walk.css', array(), '1.1.0');
        return;
    }
    // WordPress prints this small stylesheet with the page. Keep fonts local to the plugin.
    $css = str_replace("url('./fonts/", "url('" . esc_url_raw($url . 'fonts/'), $css);
    wp_register_style($handle, false, array(), '1.1.0');
    wp_add_inline_style($handle, $css);
}
function nadlan_walk_article_styles() {
    $post = get_post();
    if ($post && has_shortcode($post->post_content,'nadlan_walk')) {
        nadlan_walk_styles();
        wp_enqueue_style('nadlan-quarter-walk');
    }
}
add_action('wp_enqueue_scripts','nadlan_walk_article_styles');

function nadlan_walk_render($attributes = array()) {
    static $instance = 0;
    ++$instance;
    $args = shortcode_atts(array('place' => '', 'lang' => '', 'open' => 'dialog'), (array) $attributes, 'nadlan_walk');
    static $data = null;
    if ($data === null) $data = json_decode(file_get_contents(__DIR__ . '/entries.json'), true);
    $language = strtolower(substr($args['lang'] ?: determine_locale(), 0, 2));
    if (!isset($data['copy'][$language])) $language = 'he';
    $copy = $data['copy'][$language];
    $bar_labels = array();
    foreach ($data['copy'] as $locale => $labels) {
        $bar_labels[$locale] = array('close' => $labels['close'], 'open' => $labels['standalone']);
    }
    $dated_title = preg_match('/^(.+?)\s+([0-9]{4})$/u', $copy['title'], $heading);
    $place = isset($data['places'][$args['place']]) ? $args['place'] : '';
    $target = $place ? $data['places'][$place] : $data['home'];
    $plugin_url = plugin_dir_url(__FILE__);
    $tour = trailingslashit(apply_filters('nadlan_walk_tour_url', home_url($data['path'])));
    $url = $language === 'he' ? $tour : add_query_arg('lang', $language, $tour);
    $directory = $language === 'he' ? $tour.'places/' : add_query_arg('lang', $language, $tour.'places/');
    $entry_link = $url . ($place ? '#p=' . rawurlencode($place) : '');
    $caption = $target['caption'][$language];
    $entry_label = $place ? str_replace('{place}', $target['short'][$language], $copy['startAt']) : $copy['enter'];
    $image = $target['cover'];
    $sources = trailingslashit(apply_filters('nadlan_walk_cover_url', $tour . 'media/wordpress/covers/'));
    $id = wp_unique_id('nl-walk-');
    $dir = in_array($language, array('he','ar'), true) ? 'rtl' : 'ltr';
    wp_enqueue_script('nadlan-quarter-walk', $plugin_url . 'walk.js', array(), 'a9329e9d862a', true);
    nadlan_walk_styles();
    ob_start();
    if (!wp_style_is('nadlan-quarter-walk','done')) wp_print_styles(array('nadlan-quarter-walk'));
    ?>
    <section class="nlq<?php echo $place ? ' nlq-context' : ''; ?>" dir="<?php echo esc_attr($dir); ?>" lang="<?php echo esc_attr($language); ?>" aria-labelledby="<?php echo esc_attr($id); ?>-title"
       data-nlq data-view="<?php echo $args['open'] === 'page' ? 'page' : 'dialog'; ?>" data-instance="<?php echo esc_attr(($place ?: 'home').'-'.$instance); ?>" data-resume="<?php echo esc_attr($copy['resume']); ?>" data-close="<?php echo esc_attr($copy['close']); ?>"
       data-loading="<?php echo esc_attr($copy['loading']); ?>" data-failure="<?php echo esc_attr($copy['failure']); ?>"
       data-bar-labels="<?php echo esc_attr(wp_json_encode($bar_labels)); ?>" data-open="<?php echo esc_attr($copy['standalone']); ?>">
      <figure class="nlq-cover">
        <picture>
          <?php if ($image === $data['home']['cover']) : ?>
          <source type="image/avif" media="(max-width: 640px)" width="750" height="440" sizes="100vw" srcset="<?php echo esc_url($sources.$image.'-375.avif'); ?> 375w, <?php echo esc_url($sources.$image.'-750.avif'); ?> 750w">
          <source type="image/avif" media="(min-width: 641px)" width="1440" height="800" sizes="(min-width: 1250px) 875px, 70vw" srcset="<?php echo esc_url($sources.$image.'-960.avif'); ?> 960w, <?php echo esc_url($sources.$image.'-1440.avif'); ?> 1440w">
          <?php endif; ?>
          <source width="750" height="440" media="(max-width: 640px)" srcset="<?php echo esc_url($sources.$image.'-phone.webp'); ?>">
          <img width="1440" height="800" src="<?php echo esc_url($sources.$image.'-wide.webp'); ?>" alt="<?php echo esc_attr($target['alt'][$language]); ?>" loading="<?php echo $instance === 1 ? 'eager' : 'lazy'; ?>" fetchpriority="<?php echo $instance === 1 ? 'high' : 'low'; ?>" decoding="async"></picture>
        <figcaption><span lang="he" dir="rtl">הדמיה להמחשה, על פי התכנית</span><?php if ($language !== 'he') : ?> · <span><?php echo esc_html($copy['disclosure']); ?></span><?php endif; ?></figcaption>
      </figure>
      <div class="nlq-sign"><h2 id="<?php echo esc_attr($id); ?>-title"><?php if ($place) echo esc_html($target['short'][$language]); elseif ($dated_title) echo '<span class="nlq-name">' . esc_html($heading[1]) . '</span> <bdi>' . esc_html($heading[2]) . '</bdi>'; else echo esc_html($copy['title']); ?></h2>
        <p><?php echo esc_html($caption); ?></p>
        <a class="nlq-enter" data-entry="<?php echo esc_attr($place); ?>" href="<?php echo esc_url($entry_link); ?>"><?php echo esc_html($entry_label); ?></a>
      </div>
      <nav class="nlq-stops" aria-label="<?php echo esc_attr($copy['choose']); ?>">
        <?php foreach ($data['links'] as $key) : ?>
        <a data-entry="<?php echo esc_attr($key); ?>" href="<?php echo esc_url($url.'#p='.rawurlencode($key)); ?>"><?php echo esc_html($data['places'][$key]['short'][$language]); ?></a>
        <?php endforeach; ?>
        <a href="<?php echo esc_url($directory); ?>"><?php echo esc_html($copy['records']); ?></a>
      </nav>
    </section>
    <?php return ob_get_clean();
}
add_shortcode('nadlan_walk','nadlan_walk_render');
