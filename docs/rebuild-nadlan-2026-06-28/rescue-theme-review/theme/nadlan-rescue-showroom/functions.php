<?php
/**
 * NadLan Rescue Showroom theme.
 * Safe intent: one renderer, standalone routes, reversible activation.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

define( 'NADLAN_RESCUE_VERSION', '1.0.0' );

add_action( 'after_switch_theme', function () {
    nadlan_rescue_register_rewrites();
    flush_rewrite_rules();
} );

add_action( 'init', 'nadlan_rescue_register_rewrites' );
function nadlan_rescue_register_rewrites() {
    add_rewrite_rule( '^projects/?$', 'index.php?nadlan_rescue_view=projects', 'top' );
    add_rewrite_rule( '^projects/([^/]+)/?$', 'index.php?nadlan_rescue_view=project&nadlan_rescue_project=$matches[1]', 'top' );

    register_post_type( 'nadlan_rescue_lead', array(
        'labels' => array( 'name' => 'NadLan Rescue Leads', 'singular_name' => 'NadLan Rescue Lead' ),
        'public' => false,
        'show_ui' => true,
        'show_in_menu' => true,
        'supports' => array( 'title', 'custom-fields' ),
        'capability_type' => 'post',
    ) );
}

add_filter( 'query_vars', function ( $vars ) {
    $vars[] = 'nadlan_rescue_view';
    $vars[] = 'nadlan_rescue_project';
    return $vars;
} );

add_filter( 'template_include', function ( $template ) {
    $view = get_query_var( 'nadlan_rescue_view' );
    if ( 'projects' === $view ) {
        return get_template_directory() . '/templates/projects.php';
    }
    if ( 'project' === $view ) {
        return get_template_directory() . '/templates/project.php';
    }
    return $template;
} );

add_action( 'wp_enqueue_scripts', function () {
    $uri = trailingslashit( get_template_directory_uri() );
    wp_enqueue_style( 'nadlan-rescue-theme', get_stylesheet_uri(), array(), NADLAN_RESCUE_VERSION );
    wp_enqueue_style( 'nadlan-rescue-tokens', $uri . 'assets/engine/tokens.css', array(), NADLAN_RESCUE_VERSION );
    wp_enqueue_style( 'nadlan-rescue-showroom', $uri . 'assets/engine/showroom.css', array( 'nadlan-rescue-tokens' ), NADLAN_RESCUE_VERSION );
    wp_enqueue_style( 'nadlan-rescue-editorial', $uri . 'assets/engine/editorial.css', array( 'nadlan-rescue-showroom' ), NADLAN_RESCUE_VERSION );

    wp_enqueue_script( 'nadlan-rescue-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js', array(), '4.0.0', true );
    wp_enqueue_script( 'nadlan-rescue-i18n', $uri . 'assets/engine/i18n.js', array(), NADLAN_RESCUE_VERSION, true );
    wp_enqueue_script( 'nadlan-rescue-data', $uri . 'assets/engine/data.js', array(), NADLAN_RESCUE_VERSION, true );

    $defaults = nadlan_rescue_current_context();
    $inline = 'window.NADLAN_ASSET_BASE=' . wp_json_encode( $uri . 'assets/' ) . ';' . "\n";
    $inline .= 'window.NADLAN_RESCUE_CONTEXT=' . wp_json_encode( $defaults ) . ';' . "\n";
    $inline .= "(function(){\n";
    $inline .= " var ctx=window.NADLAN_RESCUE_CONTEXT||{};\n";
    $inline .= " if(window.NADLAN_SHOWROOM){\n";
    $inline .= "   window.NADLAN_SHOWROOM.config.default_project=ctx.project||window.NADLAN_SHOWROOM.config.default_project;\n";
    $inline .= "   window.NADLAN_SHOWROOM.config.default_lang=ctx.lang||window.NADLAN_SHOWROOM.config.default_lang;\n";
    $inline .= "   window.NADLAN_SHOWROOM.config.lead_endpoint=ctx.lead_endpoint||window.NADLAN_SHOWROOM.config.lead_endpoint;\n";
    $inline .= "   window.NADLAN_SHOWROOM.config.whatsapp=ctx.whatsapp||'';\n";
    $inline .= "   Object.keys(window.NADLAN_SHOWROOM.projects||{}).forEach(function(k){\n";
    $inline .= "     var p=window.NADLAN_SHOWROOM.projects[k]; p.url=(ctx.project_urls&&ctx.project_urls[k])||('/projects/'+k+'/');\n";
    $inline .= "     p.lang_urls=(ctx.lang_urls&&ctx.lang_urls[k])||{};\n";
    $inline .= "   });\n";
    $inline .= " }\n";
    $inline .= "})();";
    wp_enqueue_script( 'nadlan-rescue-engine', $uri . 'assets/engine/engine.js', array( 'nadlan-rescue-i18n', 'nadlan-rescue-data' ), NADLAN_RESCUE_VERSION, true );
    wp_add_inline_script( 'nadlan-rescue-engine', $inline, 'before' );
} );

add_filter( 'script_loader_tag', function ( $tag, $handle, $src ) {
    if ( 'nadlan-rescue-model-viewer' === $handle ) {
        return '<script type="module" src="' . esc_url( $src ) . '"></script>' . "\n";
    }
    return $tag;
}, 10, 3 );

function nadlan_rescue_current_context() {
    $raw = get_query_var( 'nadlan_rescue_project' );
    if ( ! $raw && is_singular() ) {
        $raw = get_post_field( 'post_name', get_queried_object_id() );
    }
    $raw = $raw ? sanitize_title( $raw ) : 'ashira-sde-dov';
    $lang = 'he';
    if ( preg_match( '/-(en|fr|ru|ar)$/', $raw, $m ) ) {
        $lang = $m[1];
        $project = preg_replace( '/-(en|fr|ru|ar)$/', '', $raw );
    } else {
        $project = $raw;
    }
    $known = array( 'ashira-sde-dov', 'rainbow-tel-aviv', 'dimri-yama' );
    if ( ! in_array( $project, $known, true ) ) { $project = 'ashira-sde-dov'; }

    $langs = array( 'he' => '', 'en' => '-en', 'fr' => '-fr', 'ru' => '-ru', 'ar' => '-ar' );
    $project_urls = array();
    $lang_urls = array();
    foreach ( $known as $slug ) {
        $project_urls[ $slug ] = home_url( '/projects/' . $slug . '/' );
        $lang_urls[ $slug ] = array();
        foreach ( $langs as $l => $suffix ) {
            $lang_urls[ $slug ][ $l ] = home_url( '/projects/' . $slug . $suffix . '/' );
        }
    }

    return array(
        'project' => $project,
        'lang' => $lang,
        'project_urls' => $project_urls,
        'lang_urls' => $lang_urls,
        'lead_endpoint' => esc_url_raw( rest_url( 'nadlan-rescue/v1/lead' ) ),
        'whatsapp' => preg_replace( '/[^0-9]/', '', (string) get_theme_mod( 'nadlan_rescue_whatsapp', '' ) ),
    );
}

add_action( 'wp_head', function () {
    $ctx = nadlan_rescue_current_context();
    $project = $ctx['project'];
    if ( empty( $ctx['lang_urls'][ $project ] ) ) { return; }
    foreach ( $ctx['lang_urls'][ $project ] as $lng => $url ) {
        printf( '<link rel="alternate" hreflang="%s" href="%s">' . "\n", esc_attr( $lng ), esc_url( $url ) );
    }
    printf( '<link rel="alternate" hreflang="x-default" href="%s">' . "\n", esc_url( $ctx['lang_urls'][ $project ]['he'] ) );
}, 5 );

add_action( 'rest_api_init', function () {
    register_rest_route( 'nadlan-rescue/v1', '/lead', array(
        'methods' => 'POST',
        'permission_callback' => '__return_true',
        'callback' => function ( WP_REST_Request $request ) {
            $p = $request->get_json_params();
            if ( ! is_array( $p ) ) { $p = array(); }
            $name = sanitize_text_field( $p['name'] ?? '' );
            $phone = sanitize_text_field( $p['phone'] ?? '' );
            $email = sanitize_email( $p['email'] ?? '' );
            if ( '' === $name || ( '' === $phone && '' === $email ) ) {
                return new WP_Error( 'nadlan_rescue_missing_fields', 'Missing required fields', array( 'status' => 400 ) );
            }
            $project = sanitize_text_field( $p['project'] ?? '' );
            $unit = sanitize_text_field( $p['unit'] ?? '' );
            $id = wp_insert_post( array(
                'post_type' => 'nadlan_rescue_lead',
                'post_status' => 'private',
                'post_title' => sprintf( 'Lead: %s · %s · %s', $name, $project, $unit ),
            ), true );
            if ( is_wp_error( $id ) ) { return $id; }
            update_post_meta( $id, '_nadlan_rescue_payload', wp_json_encode( $p, JSON_UNESCAPED_UNICODE ) );
            update_post_meta( $id, '_nadlan_rescue_name', $name );
            update_post_meta( $id, '_nadlan_rescue_phone', $phone );
            update_post_meta( $id, '_nadlan_rescue_email', $email );
            update_post_meta( $id, '_nadlan_rescue_unit', $unit );
            return rest_ensure_response( array( 'ok' => true, 'id' => $id ) );
        },
    ) );
} );

add_filter( 'the_content', function ( $html ) {
    if ( ! in_the_loop() || ! is_main_query() ) { return $html; }
    $open = '<main class="nlv2-showroom"';
    $s = strpos( $html, $open );
    if ( false !== $s ) {
        $e = strpos( $html, '</main>', $s );
        if ( false !== $e ) { $html = substr( $html, 0, $s ) . substr( $html, $e + 7 ); }
    }
    return $html;
}, 7 );

add_theme_support( 'title-tag' );
add_theme_support( 'post-thumbnails' );
