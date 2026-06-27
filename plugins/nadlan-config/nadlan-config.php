<?php
/**
 * Plugin Name: NadLan Config
 * Description: Lead-capture foundation: nadlan_lead CPT + lead-form handler + healthcheck. Read skills/nadlan-config-plugin.md.
 * Version: 1.69.46
 * Author: nad-lan.co.il
 * License: GPL-2.0+
 * Requires PHP: 7.4
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/* ---------- v1.5.0: directory cards, claim funnel, auction engine ----------
 * Modular includes. Each is guarded internally with function_exists. They add:
 *   catalog-meta.php  — project + professional (contractor/service) meta + claim meta
 *   claim.php         — free-card → claim → verified-owner funnel (REST + admin + caps)
 *   import.php        — data.gov.il CKAN importer (רשם הקבלנים + התחדשות עירונית) + enrich REST + WP-CLI
 *   schema.php        — JSON-LD per card + thin-content noindex guard (anti-cannibalization)
 *   cards-render.php  — facts table + gallery + claim CTA + provenance on card views
 *   auction.php       — timed auctions: proxy bid, soft-close, custom bids table, REST
 * See skills/listings-auction-directory-architecture.md for the full design.
 */
foreach ( array( 'catalog-meta', 'claim', 'import', 'schema', 'cards-render', 'auction', 'listings-ux', 'avm-deals', 'saved-search', 'ai-provider', 'ai-features', 'city-hubs', 'media', 'compare', 'nearby-poi', 'esign', 'map', 'lead-drip', 'ops-dashboard', 'facets', 'breadcrumbs', 'autocomplete', 'tiers', 'glossary', 'glossary-autolink', 'homepage', 'directory', 'reviews', 'lead-ledger', 'ai-concierge', 'archive-grid', 'calculators', 'catalog-shine', 'conversion-cta', 'whatsapp-lead-ingestion', 'lead-routing', 'feature-flags', 'compounds', 'compound-map', 'project-3d', 'project-page-assembly', 'offers', 'lead-e2e', 'lead-inbox', 'preferred-partners', 'featured-upsell', 'sponsored-spot', 'pricing-schema', 'claim-prompt', 'ga4-events', 'sitemap-ping', 'social-proof', 'term-faq-schema', 'og-image', 'owner-config-rest', 'studio', 'studio-rest', 'profile-extras', 'advertiser-center', 'advertiser-orders', 'premium-ui', 'geo-search', 'roles', 'greeninvoice-recurring', 'placement-auction', 'admin-control', 'contextual-help', 'business-metrics', 'health', 'final-hardening', 'lead-ai-qualify', 'lead-nurture', 'showroom-engine' ) as $nadlan_mod ) {
	$nadlan_mod_file = __DIR__ . '/inc/' . $nadlan_mod . '.php';
	if ( file_exists( $nadlan_mod_file ) ) {
		require_once $nadlan_mod_file;
	}
}
unset( $nadlan_mod, $nadlan_mod_file );

if ( ! function_exists( 'nadlan_config_register_cpt' ) ) {
	function nadlan_config_register_cpt() {
		register_post_type(
			'nadlan_lead',
			array(
				'labels'        => array(
					'name'          => 'NadLan Leads',
					'singular_name' => 'NadLan Lead',
				),
				'public'        => false,
				'show_ui'       => true,
				'show_in_menu'  => true,
				'menu_icon'     => 'dashicons-money-alt',
				'menu_position' => 25,
				'supports'      => array( 'title', 'editor', 'custom-fields' ),
			)
		);
	}
}
add_action( 'init', 'nadlan_config_register_cpt' );

if ( ! function_exists( 'nadlan_config_healthcheck' ) ) {
	function nadlan_config_healthcheck() {
		register_rest_route(
			'nadlan/v1',
			'/healthcheck',
			array(
				'methods'             => 'GET',
				'callback'            => 'nadlan_config_healthcheck_response',
				'permission_callback' => '__return_true',
			)
		);
	}
}
add_action( 'rest_api_init', 'nadlan_config_healthcheck' );

if ( ! function_exists( 'nadlan_config_healthcheck_response' ) ) {
	function nadlan_config_healthcheck_response() {
		$out = array(
			'plugin'              => 'nadlan-config',
			'version'             => '1.69.46',
			'cpt_present'         => post_type_exists( 'nadlan_lead' ),
			'lead_handler_loaded' => (bool) has_action( 'admin_post_nadlan_lead' ),
			'php_version'         => PHP_VERSION,
			'wp_version'          => get_bloginfo( 'version' ),
			'catalog'             => nadlan_config_catalog_status(),
			'directory'           => array(
				'claim_cpt'        => post_type_exists( 'nadlan_claim' ),
				'auction_cpt'      => post_type_exists( 'nadlan_auction' ),
				'bids_table'       => get_option( 'nadlan_auction_db_version' ) === '1',
				'import_offset_kab'=> (int) get_option( 'nadlan_import_offset_contractors', 0 ),
				'ga4_hardcode'     => defined( 'NADLAN_GA4_HARDCODE' ) ? NADLAN_GA4_HARDCODE : null,
			),
		);
		return apply_filters( 'nadlan_config_healthcheck', $out );
	}
}

if ( ! function_exists( 'nadlan_config_clean' ) ) {
	function nadlan_config_clean( $key ) {
		if ( ! isset( $_POST[ $key ] ) ) {
			return '';
		}
		return sanitize_text_field( wp_unslash( $_POST[ $key ] ) );
	}
}

if ( ! function_exists( 'nadlan_config_valid_lead_card_id' ) ) {
	function nadlan_config_valid_lead_card_id( $card_id ) {
		$card_id = absint( $card_id );
		if ( ! $card_id ) { return 0; }
		$post = get_post( $card_id );
		if ( ! $post || ! in_array( $post->post_type, array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ), true ) ) {
			return 0;
		}
		return $card_id;
	}
}

if ( ! function_exists( 'nadlan_config_handle_lead' ) ) {
	function nadlan_config_handle_lead() {
		$nonce_raw = isset( $_POST['nadlan_nonce'] ) ? sanitize_text_field( wp_unslash( $_POST['nadlan_nonce'] ) ) : '';
		if ( $nonce_raw === '' || ! wp_verify_nonce( $nonce_raw, 'nadlan_lead' ) ) {
			wp_safe_redirect( add_query_arg( 'lead', 'bad_nonce', home_url( '/' ) ) );
			exit;
		}

		$email_raw   = isset( $_POST['lead_email'] ) ? wp_unslash( $_POST['lead_email'] ) : '';
		$message_raw = isset( $_POST['lead_message'] ) ? wp_unslash( $_POST['lead_message'] ) : '';

		$fields = array(
			'name'         => nadlan_config_clean( 'lead_name' ),
			'phone'        => nadlan_config_clean( 'lead_phone' ),
			'email'        => sanitize_email( $email_raw ),
			'goal'         => nadlan_config_clean( 'lead_goal' ),
			'city'         => nadlan_config_clean( 'lead_city' ),
			'budget'       => nadlan_config_clean( 'lead_budget' ),
			'timeline'     => nadlan_config_clean( 'lead_timeline' ),
			'message'      => sanitize_textarea_field( $message_raw ),
			'source_url'   => esc_url_raw( wp_get_referer() ? wp_get_referer() : home_url( '/' ) ),
			'utm_source'   => nadlan_config_clean( 'utm_source' ),
			'utm_campaign' => nadlan_config_clean( 'utm_campaign' ),
		);
		$lead_card_raw = 0;
		if ( isset( $_POST['card_id'] ) ) {
			$lead_card_raw = wp_unslash( $_POST['card_id'] );
		} elseif ( isset( $_POST['lead_card_id'] ) ) {
			$lead_card_raw = wp_unslash( $_POST['lead_card_id'] );
		}
		$lead_card_id = nadlan_config_valid_lead_card_id( $lead_card_raw );

		if ( function_exists( 'nadlan_lead_e2e_enabled' ) && nadlan_lead_e2e_enabled() && function_exists( 'nadlan_lead_e2e_capture' ) ) {
			$result = nadlan_lead_e2e_capture( $fields, $lead_card_id, 'admin_post' );
			$lead_result = is_wp_error( $result ) ? 'error' : 'received';
			wp_safe_redirect( add_query_arg( 'lead', $lead_result, home_url( '/' ) ) );
			exit;
		}

		$name_for_title = $fields['name'] !== '' ? $fields['name'] : 'Lead';
		$goal_for_title = $fields['goal'] !== '' ? $fields['goal'] : 'General';
		$title          = $name_for_title . ' - ' . $goal_for_title . ' - ' . current_time( 'Y-m-d H:i' );

		$lead_id = wp_insert_post(
			array(
				'post_type'    => 'nadlan_lead',
				'post_status'  => 'private',
				'post_title'   => $title,
				'post_content' => $fields['message'],
			),
			true
		);

		if ( ! is_wp_error( $lead_id ) ) {
			foreach ( $fields as $k => $v ) {
				if ( $v !== '' ) {
					update_post_meta( $lead_id, $k, $v );
				}
			}
			if ( $lead_card_id ) {
				update_post_meta( $lead_id, 'lead_card_id', $lead_card_id );
			}
			if ( function_exists( 'nadlan_lead_route' ) ) {
				nadlan_lead_route( $lead_id, $lead_card_id, $fields, 'admin_post' );
			}

			$admin_email = get_option( 'admin_email' );
			if ( $admin_email ) {
				$body  = "New lead on nad-lan.co.il\n";
				$body .= 'Name: ' . $fields['name'] . "\n";
				$body .= 'Phone: ' . $fields['phone'] . "\n";
				$body .= 'Email: ' . $fields['email'] . "\n";
				$body .= 'Goal: ' . $fields['goal'] . "\n";
				$body .= 'City: ' . $fields['city'] . "\n";
				$body .= 'Budget: ' . $fields['budget'] . "\n";
				$body .= 'Timeline: ' . $fields['timeline'] . "\n";
				$body .= 'Source: ' . $fields['source_url'] . "\n\n";
				$body .= 'Message: ' . $fields['message'] . "\n";
				wp_mail( $admin_email, 'NadLan lead: ' . $title, $body );
			}
		}

		wp_safe_redirect( add_query_arg( 'lead', 'received', home_url( '/' ) ) );
		exit;
	}
}
add_action( 'admin_post_nopriv_nadlan_lead', 'nadlan_config_handle_lead' );
add_action( 'admin_post_nadlan_lead',        'nadlan_config_handle_lead' );

/* ---------- v1.0.5: expose Yoast meta keys for REST writes ----------
 * Yoast SEO Free does not register its meta keys with show_in_rest, so bulk
 * editing meta descriptions / titles / cornerstone via the REST API silently
 * fails. We register them here (only as a REST-exposed mirror; Yoast still
 * owns the rendering). auth_callback requires edit_posts so only logged-in
 * editors can write. Read skills/nadlan-config-plugin.md.
 */
if ( ! function_exists( 'nadlan_config_register_yoast_meta' ) ) {
	function nadlan_config_register_yoast_meta() {
		$keys = array(
			'_yoast_wpseo_metadesc'       => 'string',
			'_yoast_wpseo_title'          => 'string',
			'_yoast_wpseo_focuskw'        => 'string',
			'_yoast_wpseo_is_cornerstone' => 'string',
		);
		$post_types = array( 'page', 'post' );
		foreach ( $post_types as $pt ) {
			foreach ( $keys as $key => $type ) {
				register_post_meta( $pt, $key, array(
					'show_in_rest'  => true,
					'single'        => true,
					'type'          => $type,
					'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
				) );
			}
		}
	}
}
add_action( 'init', 'nadlan_config_register_yoast_meta', 11 );

/* ---------- v1.1.0: Catalog CPTs (properties, projects, professionals) ----------
 * Foundation for the properties catalog. English labels (admin-only) per lessons.
 * function_exists guards per failure rules. Single capability addition per release.
 * See skills/properties-catalog.md for the full architecture and roadmap.
 */
if ( ! function_exists( 'nadlan_config_register_catalog_cpts' ) ) {
    function nadlan_config_register_catalog_cpts() {
		$listing_cap_args = array(
			'capability_type' => array( 'listing', 'listings' ),
			'map_meta_cap'    => true,
			'capabilities'    => function_exists( 'nadlan_listing_capabilities' ) ? nadlan_listing_capabilities() : array(),
		);
        register_post_type( 'nadlan_property', array_merge( array(
            'labels' => array(
                'name' => 'NadLan Properties', 'singular_name' => 'NadLan Property',
                'menu_name' => 'NadLan Properties',
            ),
            'public' => true, 'show_in_rest' => true,
            'has_archive' => 'properties', 'rewrite' => array( 'slug' => 'properties' ),
            'menu_icon' => 'dashicons-admin-home', 'menu_position' => 26,
            'supports' => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'excerpt' ),
        ), $listing_cap_args ) );
        register_post_type( 'nadlan_project', array_merge( array(
            'labels' => array(
                'name' => 'NadLan Projects', 'singular_name' => 'NadLan Project',
            ),
            'public' => true, 'show_in_rest' => true,
            'has_archive' => 'projects', 'rewrite' => array( 'slug' => 'projects' ),
            'menu_icon' => 'dashicons-building', 'menu_position' => 27,
            'supports' => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'excerpt' ),
        ), $listing_cap_args ) );
        register_post_type( 'nadlan_professional', array_merge( array(
            'labels' => array(
                'name' => 'NadLan Professionals', 'singular_name' => 'NadLan Professional',
            ),
            'public' => true, 'show_in_rest' => true,
            'has_archive' => 'professionals', 'rewrite' => array( 'slug' => 'professionals' ),
            'menu_icon' => 'dashicons-businessperson', 'menu_position' => 28,
            'supports' => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'excerpt' ),
        ), $listing_cap_args ) );
        register_taxonomy( 'nadlan_city', array( 'nadlan_property', 'nadlan_project' ),
            array( 'public' => true, 'hierarchical' => true, 'show_in_rest' => true,
                'rewrite' => array( 'slug' => 'cities' ),
                'labels' => array( 'name' => 'Cities', 'singular_name' => 'City' ) ) );
        register_taxonomy( 'nadlan_profession', array( 'nadlan_professional' ),
            array( 'public' => true, 'hierarchical' => false, 'show_in_rest' => true,
                'rewrite' => array( 'slug' => 'profession' ),
                'labels' => array( 'name' => 'Professions', 'singular_name' => 'Profession' ) ) );
    }
}
add_action( 'init', 'nadlan_config_register_catalog_cpts' );

/* Healthcheck reports catalog readiness too */
if ( ! function_exists( 'nadlan_config_catalog_status' ) ) {
    function nadlan_config_catalog_status() {
        return array(
            'nadlan_property_cpt' => post_type_exists( 'nadlan_property' ),
            'nadlan_project_cpt' => post_type_exists( 'nadlan_project' ),
            'nadlan_professional_cpt' => post_type_exists( 'nadlan_professional' ),
            'nadlan_city_tax' => taxonomy_exists( 'nadlan_city' ),
        );
    }
}

/* ---------- v1.1.2: IndexNow auto-ping on publish/update ----------
 * Pings Bing, Yandex (and others honoring IndexNow) the moment a page/post
 * publishes or updates. This is the legitimate "instant indexing" — Rank Math
 * uses the same protocol. Google does not officially honor IndexNow as of
 * 2026-05 but reads the Yoast XML sitemap which already includes <lastmod>.
 *
 * One-time setup: an IndexNow key (an 8-128 char hex string) we host at:
 *   /<key>.txt  (a static endpoint returning the key)
 * We auto-generate the key on first load and store it in wp_options. We
 * expose it via a virtual /wp-json/nadlan/v1/indexnow-key endpoint AND via
 * a dynamic rewrite that returns the key at /<key>.txt (handled by WP's
 * 404 fallback hooked into 'template_redirect').
 */
if ( ! function_exists( 'nadlan_config_indexnow_key' ) ) {
    function nadlan_config_indexnow_key() {
        $k = get_option( 'nadlan_indexnow_key' );
        if ( ! $k ) {
            $k = strtolower( bin2hex( random_bytes( 16 ) ) ); // 32 hex chars
            update_option( 'nadlan_indexnow_key', $k, true );
        }
        return $k;
    }
}
if ( ! function_exists( 'nadlan_config_indexnow_serve_key' ) ) {
    function nadlan_config_indexnow_serve_key() {
        if ( ! isset( $_SERVER['REQUEST_URI'] ) ) { return; }
        $uri = strtok( $_SERVER['REQUEST_URI'], '?' );
        $k   = nadlan_config_indexnow_key();
        if ( $uri === '/' . $k . '.txt' ) {
            header( 'Content-Type: text/plain; charset=us-ascii' );
            echo $k;
            exit;
        }
    }
}
add_action( 'init', 'nadlan_config_indexnow_serve_key', 1 );

if ( ! function_exists( 'nadlan_config_indexnow_ping' ) ) {
    function nadlan_config_indexnow_ping( $url ) {
        if ( ! $url || strpos( $url, 'http' ) !== 0 ) { return; }
        $key  = nadlan_config_indexnow_key();
        $host = wp_parse_url( home_url(), PHP_URL_HOST );
        $body = wp_json_encode( array(
            'host'        => $host,
            'key'         => $key,
            'keyLocation' => home_url( '/' . $key . '.txt' ),
            'urlList'     => array( $url ),
        ) );
        wp_remote_post( 'https://api.indexnow.org/IndexNow', array(
            'timeout' => 6, 'blocking' => false, 'body' => $body,
            'headers' => array( 'Content-Type' => 'application/json; charset=utf-8' ),
        ) );
        // Bing direct (some hosts route this differently)
        wp_remote_post( 'https://www.bing.com/indexnow', array(
            'timeout' => 6, 'blocking' => false, 'body' => $body,
            'headers' => array( 'Content-Type' => 'application/json; charset=utf-8' ),
        ) );
        // store last ping for stats
        $log = get_option( 'nadlan_indexnow_log', array() );
        if ( ! is_array( $log ) ) { $log = array(); }
        array_unshift( $log, array( 'url' => $url, 't' => time() ) );
        $log = array_slice( $log, 0, 50 );
        update_option( 'nadlan_indexnow_log', $log, false );
    }
}
if ( ! function_exists( 'nadlan_config_indexnow_on_save' ) ) {
    function nadlan_config_indexnow_on_save( $post_id, $post = null, $update = null ) {
        if ( ! $post ) { $post = get_post( $post_id ); }
        if ( ! $post ) { return; }
        if ( wp_is_post_revision( $post_id ) || wp_is_post_autosave( $post_id ) ) { return; }
        if ( $post->post_status !== 'publish' ) { return; }
        if ( ! in_array( $post->post_type, array( 'post', 'page', 'nadlan_property', 'nadlan_project', 'nadlan_professional' ), true ) ) { return; }
        nadlan_config_indexnow_ping( get_permalink( $post_id ) );
    }
}
add_action( 'save_post', 'nadlan_config_indexnow_on_save', 20, 2 );

/* Surface key + recent pings in the healthcheck (admin context only) */
add_filter( 'rest_pre_dispatch', function( $r, $server, $request ) {
    if ( $request->get_route() === '/nadlan/v1/healthcheck' ) {
        add_filter( 'nadlan_config_healthcheck_extra', function( $arr ) {
            $arr['indexnow'] = array(
                'key_set'    => (bool) get_option( 'nadlan_indexnow_key' ),
                'last_pings' => array_slice( (array) get_option( 'nadlan_indexnow_log', array() ), 0, 5 ),
            );
            return $arr;
        } );
    }
    return $r;
}, 10, 3 );

/* Quietly remove the public WordPress "generator" meta — no need to advertise the stack */
remove_action( 'wp_head', 'wp_generator' );
add_filter( 'the_generator', '__return_empty_string' );

/* ---------- v1.2.0: self-hosted auto-update via plugin-update-checker ----------
 * After this version is installed ONCE manually, WordPress shows a normal
 * "Update available" notice whenever plugin-dist/nadlan-config.json (in the
 * GitHub repo, served via raw.githubusercontent) advertises a higher version.
 * The owner clicks Update inside WP — no more ZIP uploads.
 * Workflow to ship a new version is documented in skills/plugin-auto-update.md.
 */
if ( ! function_exists( 'nadlan_config_boot_updater' ) ) {
    function nadlan_config_boot_updater() {
        $loader = __DIR__ . '/lib/plugin-update-checker/plugin-update-checker.php';
        if ( ! file_exists( $loader ) ) { return; }
        require_once $loader;
        if ( ! class_exists( '\\YahnisElsts\\PluginUpdateChecker\\v5\\PucFactory' ) ) { return; }
        try {
            $checker = \YahnisElsts\PluginUpdateChecker\v5\PucFactory::buildUpdateChecker(
                'https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config.json',
                __FILE__,
                'nadlan-config'
            );
        } catch ( \Throwable $e ) {
            error_log( 'nadlan-config updater: ' . $e->getMessage() );
        }
    }
}
add_action( 'init', 'nadlan_config_boot_updater', 5 );

/* ---------- v1.2.1: tighten generator suppression + property meta REST ---------- */

/* Suppress Site Kit's <meta name="generator"> too (not just core's). Output buffer at wp_loaded. */
if ( ! function_exists( 'nadlan_config_strip_all_generators' ) ) {
	function nadlan_config_strip_all_generators( $html ) {
		if ( strpos( $html, 'name="generator"' ) !== false || strpos( $html, "name='generator'" ) !== false ) {
			$html = preg_replace( '~<meta[^>]+name=["\']generator["\'][^>]*>\s*~i', '', $html );
		}
		// v1.38.0: remove the WordPress theme-compat "powered by" credit paragraph that
		// get_footer() prints on plugin-rendered archives in a block theme. Targeted:
		// only the <p> that links to wordpress.org. Nothing else is touched.
		if ( strpos( $html, 'wordpress.org' ) !== false ) {
			$html = preg_replace(
				'~<p>\s*[^<]*<a[^>]*href=["\']https?://(?:[a-z]+\.)?wordpress\.org/?["\'][^>]*>[^<]*</a>\s*</p>~i',
				'',
				$html
			);
		}
		return $html;
	}
}
add_action( 'template_redirect', function() {
	ob_start( 'nadlan_config_strip_all_generators' );
}, 0 );

/* Property meta exposed for REST so we can seed properties via the API */
if ( ! function_exists( 'nadlan_config_register_property_meta' ) ) {
	function nadlan_config_register_property_meta() {
		$fields = array(
			'listing_type'   => 'string',  'property_type'  => 'string',
			'price'          => 'integer', 'price_per_sqm'  => 'integer',
			'rooms'          => 'number',  'floor'          => 'integer',
			'total_floors'   => 'integer', 'size_sqm'       => 'integer',
			'balcony_sqm'    => 'integer',
			'parking'        => 'boolean', 'elevator'       => 'boolean',
			'ac'             => 'boolean', 'protected_room' => 'boolean',
			'street'         => 'string',  'building_number' => 'string',
			'lat'            => 'number',  'lng'            => 'number',
			'status'         => 'string',  'source'         => 'string',
			'is_sponsored'   => 'boolean', 'sponsor_name'   => 'string',
			'photos_csv'     => 'string',
		);
		foreach ( $fields as $k => $type ) {
			register_post_meta( 'nadlan_property', $k, array(
				'show_in_rest'  => true,
				'single'        => true,
				'type'          => $type,
				'auth_callback' => function( $allowed, $meta_key, $post_id ) { return current_user_can( 'edit_post', (int) $post_id ); },
			) );
		}
	}
}
add_action( 'init', 'nadlan_config_register_property_meta', 12 );

/* Healthcheck augmenter via proper filter (wired into the refactored response above) */
if ( ! function_exists( 'nadlan_config_healthcheck_augment' ) ) {
	function nadlan_config_healthcheck_augment( $arr ) {
		$arr['indexnow'] = array(
			'key_present'  => (bool) get_option( 'nadlan_indexnow_key' ),
			'recent_pings' => array_slice( (array) get_option( 'nadlan_indexnow_log', array() ), 0, 5 ),
		);
		return $arr;
	}
}
add_filter( 'nadlan_config_healthcheck', 'nadlan_config_healthcheck_augment' );

/* ---------- v1.3.0: robots.txt with sitemap + disable wptexturize ----------
 * Two fixes:
 * 1) Serve a proper robots.txt (with the Yoast sitemap_index reference) via the
 *    WordPress robots_txt filter. NOTE: this only takes effect if the web server
 *    routes /robots.txt to WordPress (index.php). If a physical robots.txt or an
 *    nginx rule intercepts the path first, add the file/route at server level.
 * 2) Disable wptexturize on titles/content/excerpts. wptexturize auto-converts
 *    " - " (space-hyphen-space) into an en-dash (–) at render time, which violated
 *    the owner's no-dash typography rule and reintroduced AI-tell punctuation even
 *    after the stored text was cleaned. Removing it keeps punctuation as authored.
 */
if ( ! function_exists( 'nadlan_config_robots_txt' ) ) {
	function nadlan_config_robots_txt( $output, $public ) {
		if ( '0' === (string) $public ) {
			return $output; // respect "discourage search engines" toggle
		}
		$sitemap = home_url( '/sitemap_index.xml' );
		$out  = "User-agent: *\n";
		$out .= "Allow: /\n";
		$out .= "Disallow: /wp-admin/\n";
		$out .= "Allow: /wp-admin/admin-ajax.php\n";
		$out .= "Disallow: /cart/\n";
		$out .= "Disallow: /checkout/\n";
		$out .= "Disallow: /my-account/\n";
		$out .= "Disallow: /*?s=\n";
		$out .= "Disallow: /*add-to-cart=\n";
		$out .= "\nSitemap: " . esc_url_raw( $sitemap ) . "\n";
		return $out;
	}
}
add_filter( 'robots_txt', 'nadlan_config_robots_txt', 20, 2 );

if ( ! function_exists( 'nadlan_config_disable_texturize' ) ) {
	function nadlan_config_disable_texturize() {
		foreach ( array( 'the_content', 'the_title', 'the_excerpt', 'single_post_title',
			'comment_text', 'widget_text_content', 'widget_block_content', 'nav_menu_description',
			'term_description', 'list_cats', 'wp_title', 'document_title' ) as $f ) {
			remove_filter( $f, 'wptexturize' );
		}
	}
}
add_action( 'init', 'nadlan_config_disable_texturize', 20 );

/**
 * GA4 direct tag (G-G3QRV5646E).
 *
 * Owner-approved 2026-06-01 ("hardcode now, consolidate later"). The live site
 * was tagging Google Tag GT-W6VHT5TK via Site Kit, but the owner's GA4 property
 * G-G3QRV5646E received no hits. This emits the GA4 config directly so that
 * property starts collecting immediately.
 *
 * RESOLVED 2026-06-01: Site Kit is confirmed already tagging G-G3QRV5646E correctly
 * (the "no data" the owner saw was Site Kit's "exclude logged-in users" — admin
 * self-views; verified working in incognito). So the direct hardcode would
 * DOUBLE-COUNT. Default is now FALSE — Site Kit owns GA4. To force the direct tag
 * back on (e.g. if Site Kit is ever removed), add define('NADLAN_GA4_HARDCODE', true)
 * to wp-config.php. No code edit needed to toggle.
 */
if ( ! defined( 'NADLAN_GA4_HARDCODE' ) ) {
	define( 'NADLAN_GA4_HARDCODE', false );
}
if ( ! function_exists( 'nadlan_config_ga4_tag' ) ) {
	function nadlan_config_ga4_tag() {
		if ( ! NADLAN_GA4_HARDCODE || is_admin() ) {
			return;
		}
		$id = 'G-G3QRV5646E';
		echo "\n<!-- nadlan-config GA4 (direct) -->\n";
		echo '<script async src="https://www.googletagmanager.com/gtag/js?id=' . esc_attr( $id ) . '"></script>' . "\n";
		echo "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','" . esc_js( $id ) . "');</script>\n";
	}
}
add_action( 'wp_head', 'nadlan_config_ga4_tag', 5 );
