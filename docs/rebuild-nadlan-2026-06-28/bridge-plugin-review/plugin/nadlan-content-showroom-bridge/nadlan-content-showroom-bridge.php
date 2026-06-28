<?php
/**
 * Plugin Name: NadLan Content Showroom Bridge
 * Description: Adds a design-system showroom layer, 3D/facade shortcodes, project gallery, hreflang and styled SEO wrappers without replacing the existing NadLan theme, content, calculators, listings, professionals or monetization modules.
 * Version: 0.2.0
 * Author: OpenAI
 * Text Domain: nadlan-content-showroom-bridge
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

define( 'NLCB_VERSION', '0.2.0' );
define( 'NLCB_DIR', plugin_dir_path( __FILE__ ) );
define( 'NLCB_URL', plugin_dir_url( __FILE__ ) );

function nlcb_languages() { return array( 'he', 'en', 'fr', 'ru', 'ar' ); }

function nlcb_slug_lang( $slug ) {
    $slug = (string) $slug;
    foreach ( array( 'en', 'fr', 'ru', 'ar' ) as $lang ) {
        if ( preg_match( '/-' . preg_quote( $lang, '/' ) . '$/', $slug ) ) { return $lang; }
    }
    return 'he';
}

function nlcb_canon_slug( $slug ) {
    return preg_replace( '/-(en|fr|ru|ar)$/', '', (string) $slug );
}

function nlcb_asset_url( $path ) {
    return NLCB_URL . ltrim( $path, '/' );
}

function nlcb_enqueue_assets() {
    wp_enqueue_style( 'nlcb-bridge', nlcb_asset_url( 'assets/bridge.css' ), array(), NLCB_VERSION );
    wp_enqueue_script( 'nlcb-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js', array(), '4.0.0', true );
    wp_script_add_data( 'nlcb-model-viewer', 'type', 'module' );
    wp_enqueue_script( 'nlcb-bridge', nlcb_asset_url( 'assets/bridge.js' ), array(), NLCB_VERSION, true );
}

function nlcb_upload_or_raw_url( $value ) {
    if ( empty( $value ) ) { return ''; }
    if ( is_numeric( $value ) ) {
        $url = wp_get_attachment_url( absint( $value ) );
        return $url ? $url : '';
    }
    $value = trim( (string) $value );
    if ( preg_match( '#^https?://#i', $value ) || strpos( $value, '/' ) === 0 ) { return esc_url_raw( $value ); }
    return $value;
}

function nlcb_meta_first( $post_id, $keys, $default = '' ) {
    foreach ( (array) $keys as $key ) {
        $value = get_post_meta( $post_id, $key, true );
        if ( $value !== '' && $value !== null && $value !== array() ) { return $value; }
    }
    return $default;
}

function nlcb_decode_units( $raw ) {
    if ( empty( $raw ) ) { return array(); }
    if ( is_array( $raw ) ) { return $raw; }
    $raw = trim( (string) $raw );
    $decoded = json_decode( $raw, true );
    return is_array( $decoded ) ? $decoded : array();
}

function nlcb_default_comps() {
    return array(
        array( 'address' => 'שדה דב 4', 'rooms' => 4, 'sqm' => 115, 'price' => '₪8.9M', 'date' => '04/2026' ),
        array( 'address' => 'המעגן 11', 'rooms' => 4, 'sqm' => 122, 'price' => '₪9.4M', 'date' => '03/2026' ),
        array( 'address' => 'נמל ת״א 9', 'rooms' => 5, 'sqm' => 140, 'price' => '₪11.2M', 'date' => '02/2026' ),
    );
}

function nlcb_fallback_projects() {
    $plan4 = nlcb_asset_url( 'assets/plans/plan-4br.svg' );
    $plan3 = nlcb_asset_url( 'assets/plans/plan-3br.svg' );
    $plan5 = nlcb_asset_url( 'assets/plans/plan-5br.svg' );
    $base = array(
        'area_label' => 'רובע שדה דב · תל אביב',
        'avg_price_per_sqm' => 77000,
        'comps' => nlcb_default_comps(),
        'default_plan' => $plan4,
    );
    return array(
        'ashira-sde-dov' => array_merge( $base, array(
            'slug' => 'ashira-sde-dov', 'title' => 'Ashira', 'floors' => 20,
            'url' => home_url( '/projects/ashira-sde-dov/' ),
            'model' => nlcb_asset_url( 'assets/engine/models/ashira.glb' ),
            'poster' => nlcb_asset_url( 'assets/engine/models/ashira-poster.jpg' ),
            'facade' => nlcb_asset_url( 'assets/engine/models/ashira-facade.jpg' ),
            'content' => array(
                'he' => array( 'hero_p' => 'דירות חדשות מול הים בשדה דב. בוחרים דירה מתוך הבניין, רואים קומה, כיוון ונוף, ובודקים אומדן מחיר וסביבה לפני פנייה.', 'seo_h' => 'דירות למכירה ב-Ashira שדה דב: מה לבדוק לפני בחירה', 'seo_p' => 'בחירת דירה ב-Ashira אינה רק מספר חדרים. רוכש רציני צריך להבין את הקומה, הכיוון, הנוף, המרחק לים והרובע המתפתח סביב הפרויקט.' ),
                'en' => array( 'hero_p' => 'New seafront homes in Sde Dov. Choose an apartment from the building, see floor, facing and view, and check the neighborhood before you enquire.', 'seo_h' => 'Ashira Sde Dov apartments for sale: what to check before choosing', 'seo_p' => 'Choosing a home at Ashira is not only a room count. Buyers need to understand the floor, facing, view, sea proximity and the district around the project.' ),
            ),
            'units' => array(
                array( 'id'=>'ashira-18-west','label'=>'18W','floor'=>18,'rooms'=>5,'sqm'=>132,'balcony'=>18,'dir'=>'west','status'=>'available','view'=>'ים וארובת רידינג','stage_x'=>42,'stage_y'=>30,'plan'=>$plan5 ),
                array( 'id'=>'ashira-14-city','label'=>'14C','floor'=>14,'rooms'=>4,'sqm'=>104,'balcony'=>12,'dir'=>'east','status'=>'available','view'=>'רובע שדה דב והעיר','stage_x'=>58,'stage_y'=>42,'plan'=>$plan4 ),
                array( 'id'=>'ashira-10-corner','label'=>'10P','floor'=>10,'rooms'=>4,'sqm'=>118,'balcony'=>14,'dir'=>'south-west','status'=>'reserved','view'=>'ים וחצר פנימית','stage_x'=>32,'stage_y'=>56,'plan'=>$plan4 ),
                array( 'id'=>'ashira-07-east','label'=>'7A','floor'=>7,'rooms'=>3,'sqm'=>82,'balcony'=>10,'dir'=>'east','status'=>'sold','view'=>'חזית עירונית','stage_x'=>64,'stage_y'=>66,'plan'=>$plan3 ),
                array( 'id'=>'ashira-04-garden','label'=>'4G','floor'=>4,'rooms'=>3,'sqm'=>92,'balcony'=>16,'dir'=>'west','status'=>'available','view'=>'גן, ים ושדרה','stage_x'=>48,'stage_y'=>78,'plan'=>$plan3 ),
            ),
        ) ),
        'rainbow-tel-aviv' => array_merge( $base, array(
            'slug' => 'rainbow-tel-aviv', 'title' => 'Rainbow', 'floors' => 38,
            'url' => home_url( '/projects/rainbow-tel-aviv/' ),
            'model' => nlcb_asset_url( 'assets/engine/models/rainbow.glb' ),
            'poster' => nlcb_asset_url( 'assets/engine/models/rainbow-poster.jpg' ),
            'facade' => nlcb_asset_url( 'assets/engine/models/rainbow-facade.jpg' ),
            'content' => array( 'he' => array( 'hero_p' => 'מגדל מגורים מול הים ברובע שדה דב, עם בחירת דירה לפי קומה, כיוון ונוף.' ), 'en' => array( 'hero_p' => 'A seafront residential tower in Sde Dov with apartment choice by floor, facing and view.' ) ),
            'units' => array(
                array( 'id'=>'rainbow-31','floor'=>31,'rooms'=>5,'sqm'=>156,'balcony'=>22,'dir'=>'west','status'=>'available','view'=>'ים פתוח','stage_x'=>46,'stage_y'=>24,'plan'=>$plan5 ),
                array( 'id'=>'rainbow-24','floor'=>24,'rooms'=>4,'sqm'=>128,'balcony'=>16,'dir'=>'north-west','status'=>'available','view'=>'ים ופארק','stage_x'=>34,'stage_y'=>40,'plan'=>$plan4 ),
                array( 'id'=>'rainbow-16','floor'=>16,'rooms'=>4,'sqm'=>112,'balcony'=>14,'dir'=>'west','status'=>'reserved','view'=>'קו החוף','stage_x'=>50,'stage_y'=>56,'plan'=>$plan4 ),
                array( 'id'=>'rainbow-08','floor'=>8,'rooms'=>3,'sqm'=>82,'balcony'=>10,'dir'=>'south-west','status'=>'available','view'=>'חצר וים','stage_x'=>40,'stage_y'=>72,'plan'=>$plan3 ),
            ),
        ) ),
        'dimri-yama' => array_merge( $base, array(
            'slug' => 'dimri-yama', 'title' => 'דימרי ימה', 'floors' => 28,
            'url' => home_url( '/projects/dimri-yama/' ),
            'model' => nlcb_asset_url( 'assets/engine/models/dimri.glb' ),
            'poster' => nlcb_asset_url( 'assets/engine/models/dimri-poster.jpg' ),
            'facade' => nlcb_asset_url( 'assets/engine/models/dimri-facade.jpg' ),
            'content' => array( 'he' => array( 'hero_p' => 'בניין גן מול הים בשדה דב, עם בחירת דירות ומידע סביבתי במקום אחד.' ), 'en' => array( 'hero_p' => 'A garden building by the sea in Sde Dov with apartment choice and neighborhood context in one place.' ) ),
            'units' => array(
                array( 'id'=>'dimri-22','floor'=>22,'rooms'=>5,'sqm'=>165,'balcony'=>24,'dir'=>'west','status'=>'available','view'=>'ים','stage_x'=>48,'stage_y'=>28,'plan'=>$plan5 ),
                array( 'id'=>'dimri-15','floor'=>15,'rooms'=>4,'sqm'=>120,'balcony'=>18,'dir'=>'south-west','status'=>'available','view'=>'טיילת וים','stage_x'=>38,'stage_y'=>50,'plan'=>$plan4 ),
                array( 'id'=>'dimri-09','floor'=>9,'rooms'=>3,'sqm'=>88,'balcony'=>12,'dir'=>'north-west','status'=>'reserved','view'=>'פארק','stage_x'=>52,'stage_y'=>68,'plan'=>$plan3 ),
            ),
        ) ),
    );
}

function nlcb_default_project_by_slug( $slug ) {
    $canon = nlcb_canon_slug( $slug );
    $fallback = nlcb_fallback_projects();
    if ( isset( $fallback[ $canon ] ) ) { return $fallback[ $canon ]; }
    $keys = array_keys( $fallback );
    return $fallback[ $keys[0] ];
}

function nlcb_lang_urls( $slug ) {
    $canon = nlcb_canon_slug( $slug );
    $out = array();
    $suffixes = array( 'he'=>'', 'en'=>'-en', 'fr'=>'-fr', 'ru'=>'-ru', 'ar'=>'-ar' );
    foreach ( $suffixes as $lang => $suffix ) {
        $path = $canon . $suffix;
        $post = get_page_by_path( $path, OBJECT, 'nadlan_project' );
        if ( $post && $post->post_status === 'publish' ) { $out[ $lang ] = get_permalink( $post ); }
        else { $out[ $lang ] = home_url( '/projects/' . $path . '/' ); }
    }
    return $out;
}

function nlcb_normalize_unit( $unit, $i, $project ) {
    $unit = is_array( $unit ) ? $unit : array();
    $id = ! empty( $unit['id'] ) ? sanitize_title( $unit['id'] ) : 'unit-' . ( $i + 1 );
    $floor = isset( $unit['floor'] ) ? intval( $unit['floor'] ) : ( 4 + ( $i * 4 ) );
    $rooms = isset( $unit['rooms'] ) ? intval( $unit['rooms'] ) : 4;
    $sqm = isset( $unit['sqm'] ) ? intval( $unit['sqm'] ) : 100;
    $status = isset( $unit['status'] ) ? sanitize_key( $unit['status'] ) : 'available';
    if ( ! in_array( $status, array( 'available', 'reserved', 'sold' ), true ) ) { $status = 'available'; }
    $dir = isset( $unit['dir'] ) ? sanitize_text_field( $unit['dir'] ) : ( isset( $unit['direction'] ) ? sanitize_text_field( $unit['direction'] ) : 'west' );
    $plan = isset( $unit['plan'] ) ? nlcb_upload_or_raw_url( $unit['plan'] ) : $project['default_plan'];
    if ( $plan && strpos( $plan, 'http' ) !== 0 && strpos( $plan, '/' ) !== 0 ) { $plan = nlcb_asset_url( 'assets/plans/' . basename( $plan ) . '.svg' ); }
    return array(
        'id' => $id,
        'label' => isset( $unit['label'] ) ? sanitize_text_field( $unit['label'] ) : strtoupper( substr( $id, -3 ) ),
        'floor' => $floor,
        'rooms' => $rooms,
        'rooms_label' => isset( $unit['roomsLabel'] ) ? sanitize_text_field( $unit['roomsLabel'] ) : '',
        'sqm' => $sqm,
        'balcony' => isset( $unit['balcony'] ) ? intval( $unit['balcony'] ) : 12,
        'dir' => $dir,
        'status' => $status,
        'view' => isset( $unit['view'] ) ? sanitize_text_field( $unit['view'] ) : '',
        'stage_x' => isset( $unit['stage_x'] ) ? floatval( $unit['stage_x'] ) : ( 34 + ( $i * 8 ) % 30 ),
        'stage_y' => isset( $unit['stage_y'] ) ? floatval( $unit['stage_y'] ) : ( 30 + ( $i * 10 ) ),
        'plan' => $plan,
    );
}

function nlcb_project_from_post( $post ) {
    $fallback = nlcb_default_project_by_slug( $post->post_name );
    $slug = $post->post_name;
    $canon = nlcb_canon_slug( $slug );
    $lang = nlcb_slug_lang( $slug );
    $model = nlcb_upload_or_raw_url( nlcb_meta_first( $post->ID, array( 'project_model_glb', 'project_3d_model_glb', 'model_glb', '_nadlan_model_glb' ), $fallback['model'] ) );
    $poster = nlcb_upload_or_raw_url( nlcb_meta_first( $post->ID, array( 'project_model_poster', 'project_3d_model_poster', 'model_poster', '_nadlan_model_poster' ), '' ) );
    if ( ! $poster ) {
        $thumb = get_post_thumbnail_id( $post->ID );
        $poster = $thumb ? wp_get_attachment_url( $thumb ) : $fallback['poster'];
    }
    $facade = nlcb_upload_or_raw_url( nlcb_meta_first( $post->ID, array( 'project_3d_facade_image', 'project_facade_image', 'facade_image' ), $fallback['facade'] ) );
    $floors = absint( nlcb_meta_first( $post->ID, array( 'project_floors', 'project_3d_floors', 'floors' ), $fallback['floors'] ) );
    $avg = floatval( nlcb_meta_first( $post->ID, array( 'project_3d_avg_price_per_sqm', 'avg_price_per_sqm' ), $fallback['avg_price_per_sqm'] ) );
    $raw_units = nlcb_meta_first( $post->ID, array( 'project_3d_units', 'project_units', 'units_json', '_nadlan_units' ), array() );
    $units = nlcb_decode_units( $raw_units );
    if ( empty( $units ) ) { $units = $fallback['units']; }
    $project = array_merge( $fallback, array(
        'slug' => $slug,
        'canon_slug' => $canon,
        'title' => get_the_title( $post ),
        'url' => get_permalink( $post ),
        'model' => $model,
        'poster' => $poster,
        'facade' => $facade,
        'floors' => $floors,
        'avg_price_per_sqm' => $avg,
        'lang_urls' => nlcb_lang_urls( $slug ),
    ) );
    $project['content'][ $lang ]['hero_p'] = get_the_excerpt( $post ) ? wp_strip_all_tags( get_the_excerpt( $post ) ) : ( $fallback['content'][ $lang ]['hero_p'] ?? $fallback['content']['he']['hero_p'] );
    $project['units'] = array();
    foreach ( array_values( $units ) as $i => $unit ) { $project['units'][] = nlcb_normalize_unit( $unit, $i, $project ); }
    if ( ! empty( $project['units'][0]['id'] ) ) { $project['selected_unit'] = $project['units'][0]['id']; }
    return $project;
}

function nlcb_get_project( $slug = '', $post_id = 0 ) {
    if ( $post_id ) {
        $post = get_post( $post_id );
        if ( $post ) { return nlcb_project_from_post( $post ); }
    }
    if ( ! $slug && is_singular( 'nadlan_project' ) ) { return nlcb_project_from_post( get_post() ); }
    if ( $slug ) {
        $post = get_page_by_path( sanitize_title( $slug ), OBJECT, 'nadlan_project' );
        if ( $post ) { return nlcb_project_from_post( $post ); }
        $fallback = nlcb_default_project_by_slug( $slug );
        $fallback['slug'] = sanitize_title( $slug );
        $fallback['lang_urls'] = nlcb_lang_urls( $slug );
        return $fallback;
    }
    return nlcb_default_project_by_slug( 'ashira-sde-dov' );
}

function nlcb_project_query() {
    if ( post_type_exists( 'nadlan_project' ) ) {
        $q = new WP_Query( array( 'post_type'=>'nadlan_project', 'post_status'=>'publish', 'posts_per_page'=>12, 'orderby'=>'menu_order date', 'order'=>'DESC' ) );
        $projects = array();
        foreach ( $q->posts as $post ) { $projects[] = nlcb_project_from_post( $post ); }
        wp_reset_postdata();
        if ( ! empty( $projects ) ) { return $projects; }
    }
    return array_values( nlcb_fallback_projects() );
}

function nlcb_payload( $project = null, $lang = '' ) {
    if ( ! $project ) { $project = nlcb_get_project(); }
    if ( ! $lang ) { $lang = nlcb_slug_lang( $project['slug'] ?? '' ); }
    return array(
        'lang' => $lang,
        'languages' => nlcb_languages(),
        'config' => array(
            'default_lang' => $lang,
            'home_url' => home_url( '/' ),
            'catalog_url' => home_url( '/projects/' ),
            'lead_endpoint' => esc_url_raw( rest_url( 'nadlan-bridge/v1/lead' ) ),
        ),
        'project' => $project,
    );
}

function nlcb_json_attr( $payload ) {
    return esc_attr( wp_json_encode( $payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) );
}

function nlcb_shortcode_project( $atts = array() ) {
    nlcb_enqueue_assets();
    $atts = shortcode_atts( array( 'project'=>'', 'lang'=>'' ), $atts, 'nadlan_project_showroom' );
    $project = nlcb_get_project( $atts['project'] );
    $payload = nlcb_payload( $project, $atts['lang'] ? sanitize_key( $atts['lang'] ) : nlcb_slug_lang( $project['slug'] ) );
    return '<div class="nlcb-shell nlcb-showroom" data-payload="' . nlcb_json_attr( $payload ) . '"></div>';
}

function nlcb_shortcode_gallery( $atts = array() ) {
    nlcb_enqueue_assets();
    $atts = shortcode_atts( array( 'lang'=>'he' ), $atts, 'nadlan_project_gallery' );
    $payload = array(
        'lang' => sanitize_key( $atts['lang'] ),
        'languages' => nlcb_languages(),
        'config' => array( 'home_url'=>home_url('/'), 'catalog_url'=>home_url('/projects/') ),
        'projects' => nlcb_project_query(),
    );
    return '<div class="nlcb-shell nlcb-gallery-root" data-payload="' . nlcb_json_attr( $payload ) . '"></div>';
}

function nlcb_shortcode_seo_booster( $atts = array() ) {
    $atts = shortcode_atts( array( 'project'=>'', 'lang'=>'' ), $atts, 'nadlan_seo_booster' );
    $project = nlcb_get_project( $atts['project'] );
    $payload = nlcb_payload( $project, $atts['lang'] ? sanitize_key( $atts['lang'] ) : nlcb_slug_lang( $project['slug'] ) );
    nlcb_enqueue_assets();
    return '<div class="nlcb-shell"><section class="nlcb-section nlcb-wrap"><div class="nlcb-seo"><span class="nlcb-eyebrow">מידע לרוכשים</span><h2>מה חשוב לבדוק לפני פנייה לפרויקט</h2><p>עמוד פרויקט איכותי צריך לענות על שאלות אמיתיות של רוכשים: מיקום, כיוון, קומה, נוף, תכנית, סביבת מגורים, עסקאות באזור ותהליך הפנייה. התוסף מוסיף שכבת תוכן זו בלי למחוק את גוף העמוד הקיים.</p><div class="nlcb-note"><strong>הערת אמינות</strong><span>יש לאמת מחיר, זמינות ותנאים מול היזם. אין באמור הצעה או התחייבות.</span></div></div></section></div>';
}

add_shortcode( 'nadlan_project_showroom', 'nlcb_shortcode_project' );
add_shortcode( 'nadlan_showroom_engine', 'nlcb_shortcode_project' );
add_shortcode( 'nadlan_listing_3d', 'nlcb_shortcode_project' );
add_shortcode( 'nadlan_project_gallery', 'nlcb_shortcode_gallery' );
add_shortcode( 'nadlan_home_project_gallery', 'nlcb_shortcode_gallery' );
add_shortcode( 'nadlan_seo_booster', 'nlcb_shortcode_seo_booster' );

function nlcb_strip_legacy_showroom( $html ) {
    $open = '<main class="nlv2-showroom"';
    $s = strpos( $html, $open );
    if ( $s !== false ) {
        $e = strpos( $html, '</main>', $s );
        if ( $e !== false ) { $html = substr( $html, 0, $s ) . substr( $html, $e + 7 ); }
    }
    return $html;
}

add_filter( 'the_content', function( $content ) {
    if ( is_admin() || ! in_the_loop() || ! is_main_query() ) { return $content; }
    $content = nlcb_strip_legacy_showroom( $content );
    if ( is_singular( 'nadlan_project' ) ) {
        if ( strpos( $content, 'nlcb-showroom' ) === false && strpos( $content, '[nadlan_project_showroom' ) === false && apply_filters( 'nlcb_auto_single_project_showroom', true ) ) {
            $content = nlcb_shortcode_project( array( 'project'=>get_post_field( 'post_name', get_the_ID() ) ) ) . '<div class="nlcb-existing-content nadlan-project-article nadlan-guide">' . $content . '</div>';
        }
    } elseif ( is_front_page() && apply_filters( 'nlcb_auto_home_gallery', false ) ) {
        if ( strpos( $content, 'nlcb-gallery-root' ) === false && strpos( $content, '[nadlan_home_project_gallery' ) === false ) {
            $content .= nlcb_shortcode_gallery( array( 'lang'=>'he' ) );
        }
    }
    return $content;
}, 7 );

add_filter( 'language_attributes', function( $output ) {
    if ( is_singular( 'nadlan_project' ) ) {
        $lang = nlcb_slug_lang( get_post_field( 'post_name', get_queried_object_id() ) );
        $dir = in_array( $lang, array( 'he', 'ar' ), true ) ? 'rtl' : 'ltr';
        return 'lang="' . esc_attr( $lang ) . '" dir="' . esc_attr( $dir ) . '"';
    }
    return $output;
} );

add_action( 'wp_head', function() {
    if ( ! is_singular( 'nadlan_project' ) ) { return; }
    $post = get_post();
    if ( ! $post ) { return; }
    $urls = nlcb_lang_urls( $post->post_name );
    foreach ( $urls as $lang => $url ) {
        printf( "<link rel=\"alternate\" hreflang=\"%s\" href=\"%s\" />\n", esc_attr( $lang ), esc_url( $url ) );
    }
    $xd = isset( $urls['he'] ) ? $urls['he'] : reset( $urls );
    if ( $xd ) { printf( "<link rel=\"alternate\" hreflang=\"x-default\" href=\"%s\" />\n", esc_url( $xd ) ); }
}, 5 );

add_action( 'wp_head', function() {
    if ( is_singular( 'nadlan_project' ) ) {
        $project = nlcb_get_project( '', get_queried_object_id() );
        $schema = array(
            '@context' => 'https://schema.org',
            '@type' => 'Residence',
            'name' => $project['title'],
            'url' => get_permalink(),
            'address' => array( '@type'=>'PostalAddress', 'addressLocality'=>'Tel Aviv', 'addressCountry'=>'IL' ),
            'description' => wp_strip_all_tags( get_the_excerpt() ),
        );
        echo '<script type="application/ld+json">' . wp_json_encode( $schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
    } elseif ( is_front_page() ) {
        $schema = array( '@context'=>'https://schema.org', '@type'=>'WebSite', 'name'=>get_bloginfo('name'), 'url'=>home_url('/') );
        echo '<script type="application/ld+json">' . wp_json_encode( $schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
    }
}, 20 );

add_action( 'rest_api_init', function() {
    register_rest_route( 'nadlan-bridge/v1', '/lead', array(
        'methods' => 'POST',
        'permission_callback' => '__return_true',
        'callback' => function( WP_REST_Request $request ) {
            $data = $request->get_json_params();
            if ( ! is_array( $data ) ) { $data = array(); }
            $name = sanitize_text_field( $data['name'] ?? '' );
            $phone = sanitize_text_field( $data['phone'] ?? '' );
            $email = sanitize_email( $data['email'] ?? '' );
            if ( ! $name || ( ! $phone && ! $email ) ) {
                return new WP_REST_Response( array( 'ok'=>false, 'message'=>'missing_required_fields' ), 400 );
            }
            $type = post_type_exists( 'nadlan_lead' ) ? 'nadlan_lead' : 'post';
            $lead_id = wp_insert_post( array(
                'post_type' => $type,
                'post_status' => $type === 'post' ? 'private' : 'publish',
                'post_title' => sprintf( 'NadLan showroom lead - %s', $name ),
                'post_content' => wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ),
            ), true );
            if ( is_wp_error( $lead_id ) ) { return new WP_REST_Response( array( 'ok'=>false ), 500 ); }
            foreach ( array( 'name', 'phone', 'email', 'project', 'unit' ) as $key ) {
                if ( isset( $data[ $key ] ) ) { update_post_meta( $lead_id, 'nlcb_' . $key, sanitize_text_field( $data[ $key ] ) ); }
            }
            return new WP_REST_Response( array( 'ok'=>true, 'id'=>$lead_id ), 200 );
        },
    ) );
} );
