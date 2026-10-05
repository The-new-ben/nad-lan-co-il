<?php
/**
 * HAD-256 theme-integration bench (open item 4). NEVER install on a real site.
 *
 * Runs only inside the WordPress Playground site that `start.mjs theme <commit> 9405` builds (127.0.0.1 only). It turns
 * the bench into the closest local copy of the live /post-listing/ that the repo allows:
 *   - the site's real themes: nadlan-revenue (parent, the repo root) + nadlan-platform-child (themes/), the child active,
 *     the child's platform.css replaced by the LIVE public bytes (the repo copy differs from live, see THEME.md);
 *   - the real nadlan-config plugin, every module of its list, active (activation hooks run once by hand);
 *   - the live Code Snippets, in the order Code Snippets runs them (plugins_loaded, priority 1, after every plugin):
 *     x-skin-a (638, the live text read on 2.10), x-broker-drop + x-broker-join (699) + x-owner-wizard (707) from the
 *     pinned commit's plugins/nadlan-config/inc (broker-drop 1.1.4, owner-wizard 2.0.0 = snapshot 3);
 *   - option nadlan_skin_a = 'all' (the live page carries body.nl-skin-a for an anonymous visitor);
 *   - page /post-listing/ with the live page text (scripts/broker-drop/pages/post-listing-he.html: an H1, a paragraph and
 *     the shortcode block); /terms/, /privacy/, /accessibility-statement/, /brokers/ as placeholders.
 * The bench helpers (accounts, mail sink, blocked outbound HTTP, reset/fault/state routes) come from the snapshot's
 * nlj-bench.php with its stubs and module loader cut out (start.mjs does the cut and checks every anchor).
 * Not here (third-party plugins of the live site): WooCommerce, Paid Member Subscriptions, Yoast, Site Kit, LiteSpeed,
 * Code Snippets itself, the consent-aware Hotjar loader. Their CSS is not loaded; THEME.md lists the effect.
 */
if ( ! defined( 'ABSPATH' ) ) { return; }
if ( strpos( (string) @file_get_contents( WP_CONTENT_DIR . '/nlj-variant.txt' ), 'theme' ) !== 0 ) { return; }

define( 'NLJ_THEME_BENCH', true );

/* the real plugin and the real theme, from the first request on (both are read after the mu-plugins) */
if ( ! in_array( 'nadlan-config/nadlan-config.php', (array) get_option( 'active_plugins', array() ), true ) ) {
	update_option( 'active_plugins', array( 'nadlan-config/nadlan-config.php' ) );
}
if ( get_option( 'stylesheet' ) !== 'nadlan-platform-child' ) {
	update_option( 'template', 'nadlan-revenue' );
	update_option( 'stylesheet', 'nadlan-platform-child' );
	update_option( 'current_theme', 'NadLan Platform Child' );
}

/* the live Code Snippets, after every plugin, as Code Snippets runs them */
add_action( 'plugins_loaded', function () {
	foreach ( array( 'x-skin-a-638.php', 'x-broker-drop.php', 'x-broker-join-699.php', 'x-owner-wizard-707.php' ) as $f ) {
		$p = WP_CONTENT_DIR . '/nlj-snippets/' . $f;
		if ( file_exists( $p ) ) { require_once $p; }
		else { @file_put_contents( WP_CONTENT_DIR . '/nlj-theme.log', gmdate( 'c' ) . ' missing snippet ' . $f . "\n", FILE_APPEND ); }
	}
}, 1 );

/* the live site is Hebrew (WPLANG he_IL, <html dir="rtl" lang="he-IL">). The bench has no he_IL language pack (no
   download, and WordPress refuses WPLANG without one), so the locale is filtered and the direction set right after
   WP_Locale is built (wp-settings builds it after setup_theme), before any style is enqueued: what the pack would do,
   minus the translated core strings. */
add_filter( 'locale', function () { return 'he_IL'; } );
add_action( 'after_setup_theme', function () {
	if ( isset( $GLOBALS['wp_locale'] ) && is_object( $GLOBALS['wp_locale'] ) ) { $GLOBALS['wp_locale']->text_direction = 'rtl'; }
}, -1000 );

/* once: the live options, the activation hooks, the pages */
add_action( 'init', function () {
	if ( get_option( 'nlj_theme_setup' ) === '3' ) { return; }
	update_option( 'timezone_string', 'Asia/Jerusalem' );
	update_option( 'nadlan_skin_a', 'all' );
	if ( function_exists( 'nadlan_roles_setup' ) ) { nadlan_roles_setup(); }
	if ( function_exists( 'nadlan_deals_maybe_install' ) ) { nadlan_deals_maybe_install(); }
	$live = (string) @file_get_contents( WP_CONTENT_DIR . '/nlj-post-listing.html' );
	$pl   = get_page_by_path( 'post-listing' );
	$arr  = array( 'post_type' => 'page', 'post_status' => 'publish', 'post_name' => 'post-listing', 'post_title' => 'פרסום נכס', 'post_content' => $live !== '' ? $live : '[nadlan_listing_wizard]' );
	if ( $pl ) { $arr['ID'] = $pl->ID; wp_update_post( wp_slash( $arr ) ); } else { wp_insert_post( wp_slash( $arr ) ); }
	foreach ( array( 'terms' => 'תנאי שימוש', 'privacy' => 'מדיניות פרטיות', 'accessibility-statement' => 'הצהרת נגישות', 'brokers' => 'אתר למתווכים' ) as $slug => $t ) {
		if ( ! get_page_by_path( $slug ) ) { wp_insert_post( array( 'post_type' => 'page', 'post_status' => 'publish', 'post_name' => $slug, 'post_title' => $t, 'post_content' => '<!-- wp:paragraph --><p>(bench placeholder)</p><!-- /wp:paragraph -->' ) ); }
	}
	flush_rewrite_rules( false );
	update_option( 'nlj_theme_setup', '3' );
}, 60 );

/* what the bench really runs, for THEME.md (127.0.0.1 only, as every nlj-test route) */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nlj-test/v1', '/theme', array( 'methods' => 'GET', 'permission_callback' => function () { return in_array( (string) ( $GLOBALS['nlj_real_ip'] ?? $_SERVER['REMOTE_ADDR'] ?? '' ), array( '127.0.0.1', '::1', '' ), true ); }, 'callback' => function () {
		$t = wp_get_theme();
		$snips = array();
		foreach ( (array) glob( WP_CONTENT_DIR . '/nlj-snippets/*.php' ) as $f ) { $snips[ basename( $f ) ] = hash_file( 'sha256', $f ); }
		return array(
			'theme'        => $t->get( 'Name' ) . ' ' . $t->get( 'Version' ),
			'parent'       => $t->parent() ? $t->parent()->get( 'Name' ) . ' ' . $t->parent()->get( 'Version' ) : null,
			'plugins'      => get_option( 'active_plugins' ),
			'nadlan'       => defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : null,
			'owner'        => defined( 'NL_OWNER_VERSION' ) ? NL_OWNER_VERSION : null,
			'drop'         => defined( 'NL_DROP_VERSION' ) ? NL_DROP_VERSION : null,
			'skin_a'       => function_exists( 'nadlan_skin_a_on' ) ? get_option( 'nadlan_skin_a' ) : 'snippet missing',
			'snippets'     => $snips,
			'shortcode'    => isset( $GLOBALS['shortcode_tags']['nadlan_listing_wizard'] ) ? ( is_string( $GLOBALS['shortcode_tags']['nadlan_listing_wizard'] ) ? $GLOBALS['shortcode_tags']['nadlan_listing_wizard'] : 'closure' ) : null,
			'texturize'    => apply_filters( 'run_wptexturize', true ),
			'php'          => PHP_VERSION,
			'wp'           => get_bloginfo( 'version' ),
			'db'           => $GLOBALS['wpdb']->db_server_info(),
		);
	} ) );
} );
