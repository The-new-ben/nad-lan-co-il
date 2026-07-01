<?php
/**
 * NadLan Revenue functions and definitions.
 *
 * @link https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package WordPress
 * @subpackage NadLan_Revenue
 * @since NadLan Revenue 1.0
 */

if ( ! function_exists( 'nadlan_revenue_post_format_setup' ) ) :
	/**
	 * Adds theme support for post formats.
	 *
	 * @since NadLan Revenue 1.0
	 *
	 * @return void
	 */
	function nadlan_revenue_post_format_setup() {
		add_theme_support( 'post-formats', array( 'aside', 'audio', 'chat', 'gallery', 'image', 'link', 'quote', 'status', 'video' ) );
	}
endif;
add_action( 'after_setup_theme', 'nadlan_revenue_post_format_setup' );

if ( ! function_exists( 'nadlan_revenue_editor_style' ) ) :
	/**
	 * Enqueues editor-style.css in the editors.
	 *
	 * @since NadLan Revenue 1.0
	 *
	 * @return void
	 */
	function nadlan_revenue_editor_style() {
		add_editor_style( 'assets/css/editor-style.css' );
	}
endif;
add_action( 'after_setup_theme', 'nadlan_revenue_editor_style' );

if ( ! function_exists( 'nadlan_revenue_enqueue_styles' ) ) :
	/**
	 * Enqueues the theme stylesheet on the front.
	 *
	 * @since NadLan Revenue 1.0
	 *
	 * @return void
	 */
	function nadlan_revenue_enqueue_styles() {
		$suffix = SCRIPT_DEBUG ? '' : '.min';
		$src    = 'style' . $suffix . '.css';

		wp_enqueue_style(
			'nadlan-revenue-style',
			get_parent_theme_file_uri( $src ),
			array(),
			wp_get_theme()->get( 'Version' )
		);
		wp_style_add_data(
			'nadlan-revenue-style',
			'path',
			get_parent_theme_file_path( $src )
		);

		$premium_path = get_parent_theme_file_path( 'assets/css/nadlan-premium-sitewide.css' );
		if ( file_exists( $premium_path ) ) {
			wp_enqueue_style(
				'nadlan-revenue-premium-sitewide',
				get_parent_theme_file_uri( 'assets/css/nadlan-premium-sitewide.css' ),
				array( 'nadlan-revenue-style' ),
				(string) filemtime( $premium_path )
			);
		}

		$revenue_path = get_parent_theme_file_path( 'assets/css/nadlan-premium-revenue.css' );
		if ( file_exists( $revenue_path ) ) {
			wp_enqueue_style(
				'nadlan-revenue-premium-revenue',
				get_parent_theme_file_uri( 'assets/css/nadlan-premium-revenue.css' ),
				array( 'nadlan-revenue-premium-sitewide' ),
				(string) filemtime( $revenue_path )
			);
		}
	}
endif;
add_action( 'wp_enqueue_scripts', 'nadlan_revenue_enqueue_styles' );

if ( ! function_exists( 'nadlan_revenue_enqueue_project_showroom_assets' ) ) :
	function nadlan_revenue_enqueue_project_showroom_assets() {
		if ( is_admin() ) {
			return;
		}

		$post = get_post();
		$content = $post ? (string) $post->post_content : '';
		$template_has_home = false;

		if ( is_front_page() || is_home() ) {
			$home_template_path = get_parent_theme_file_path( 'templates/home.html' );
			if ( file_exists( $home_template_path ) ) {
				$home_template = (string) file_get_contents( $home_template_path );
				$template_has_home = false !== strpos( $home_template, 'nadlan-revenue/nadlan-home-showroom' ) || false !== strpos( $home_template, 'data-nle-home-showroom' );
			}
		}

		if ( ! is_singular() && ! $template_has_home ) {
			return;
		}

		$has_v1        = false !== strpos( $content, 'data-nlps-showroom' );
		$has_v2        = false !== strpos( $content, 'data-nlv2-showroom' );
		$has_home      = false !== strpos( $content, 'data-nle-home-showroom' ) || $template_has_home;
		$needs_model   = $has_v1 || $has_v2 || $has_home;

		if ( ! $has_v1 && ! $has_v2 && ! $has_home ) {
			return;
		}

		if ( $has_v1 ) {
			$showroom_path = get_parent_theme_file_path( 'assets/css/nadlan-project-showroom.css' );
			if ( file_exists( $showroom_path ) ) {
				wp_enqueue_style(
					'nadlan-project-showroom',
					get_parent_theme_file_uri( 'assets/css/nadlan-project-showroom.css' ),
					array( 'nadlan-revenue-style' ),
					(string) filemtime( $showroom_path )
				);
			}
		}

		if ( $has_v2 ) {
			$showroom_v2_path = get_parent_theme_file_path( 'assets/css/nadlan-showroom-v2.css' );
			if ( file_exists( $showroom_v2_path ) ) {
				wp_enqueue_style(
					'nadlan-showroom-v2',
					get_parent_theme_file_uri( 'assets/css/nadlan-showroom-v2.css' ),
					array( 'nadlan-revenue-style' ),
					(string) filemtime( $showroom_v2_path )
				);
			}
		}

		if ( $has_home ) {
			$engine_path = get_parent_theme_file_path( 'assets/css/nadlan-showroom-engine.css' );
			if ( file_exists( $engine_path ) ) {
				wp_enqueue_style(
					'nadlan-showroom-engine',
					get_parent_theme_file_uri( 'assets/css/nadlan-showroom-engine.css' ),
					array( 'nadlan-revenue-style' ),
					(string) filemtime( $engine_path )
				);
			}

			$home_showroom_path = get_parent_theme_file_path( 'assets/css/nadlan-home-showroom.css' );
			if ( file_exists( $home_showroom_path ) ) {
				wp_enqueue_style(
					'nadlan-home-showroom',
					get_parent_theme_file_uri( 'assets/css/nadlan-home-showroom.css' ),
					array( 'nadlan-showroom-engine' ),
					(string) filemtime( $home_showroom_path )
				);
			}
		}

		if ( $needs_model ) {
			if ( ! wp_script_is( 'nadlan-model-viewer', 'registered' ) ) {
				wp_register_script( 'nadlan-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js', array(), '4.3.1', true );
			}
			wp_enqueue_script( 'nadlan-model-viewer' );
		}

		if ( $has_v1 ) {
			$script_path = get_parent_theme_file_path( 'assets/js/nadlan-project-showroom.js' );
			if ( file_exists( $script_path ) ) {
				wp_enqueue_script(
					'nadlan-project-showroom',
					get_parent_theme_file_uri( 'assets/js/nadlan-project-showroom.js' ),
					array(),
					(string) filemtime( $script_path ),
					true
				);
			}
		}

		if ( $has_v2 ) {
			$script_v2_path = get_parent_theme_file_path( 'assets/js/nadlan-showroom-v2.js' );
			if ( file_exists( $script_v2_path ) ) {
				wp_enqueue_script(
					'nadlan-showroom-v2',
					get_parent_theme_file_uri( 'assets/js/nadlan-showroom-v2.js' ),
					array(),
					(string) filemtime( $script_v2_path ),
					true
				);
			}
		}

		if ( $has_home ) {
			$engine_script_path = get_parent_theme_file_path( 'assets/js/nadlan-showroom-engine.js' );
			if ( file_exists( $engine_script_path ) ) {
				wp_enqueue_script(
					'nadlan-showroom-engine',
					get_parent_theme_file_uri( 'assets/js/nadlan-showroom-engine.js' ),
					array(),
					(string) filemtime( $engine_script_path ),
					true
				);
			}
		}
	}
endif;
add_action( 'wp_enqueue_scripts', 'nadlan_revenue_enqueue_project_showroom_assets', 20 );

/*
	Legacy showroom asset order retained above:
	- data-nlps-showroom loads only the old nlps assets.
	- data-nlv2-showroom loads only the clean nlv2 assets.
	Do not add compatibility selectors between the two systems.
*/

add_filter(
	'script_loader_tag',
	function ( $tag, $handle, $src ) {
		if ( 'nadlan-model-viewer' !== $handle ) {
			return $tag;
		}

		return '<script type="module" src="' . esc_url( $src ) . '" id="nadlan-model-viewer-js"></script>' . "\n";
	},
	10,
	3
);

/* ---------------------------------------------------------------------------
 * Accessibility widget (IS 5568 / WCAG) — self-contained JS, front-end only.
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_revenue_enqueue_accessibility' ) ) :
	function nadlan_revenue_enqueue_accessibility() {
		if ( is_admin() ) { return; }
		$path = get_parent_theme_file_path( 'assets/js/nadlan-accessibility.js' );
		if ( ! file_exists( $path ) ) { return; }
		wp_enqueue_script(
			'nadlan-accessibility',
			get_parent_theme_file_uri( 'assets/js/nadlan-accessibility.js' ),
			array(),
			(string) filemtime( $path ),
			true
		);
	}
endif;
add_action( 'wp_enqueue_scripts', 'nadlan_revenue_enqueue_accessibility' );

if ( ! function_exists( 'nadlan_revenue_enqueue_premium_revenue_script' ) ) :
	function nadlan_revenue_enqueue_premium_revenue_script() {
		if ( is_admin() ) { return; }
		$path = get_parent_theme_file_path( 'assets/js/nadlan-premium-revenue.js' );
		if ( ! file_exists( $path ) ) { return; }
		wp_enqueue_script(
			'nadlan-premium-revenue',
			get_parent_theme_file_uri( 'assets/js/nadlan-premium-revenue.js' ),
			array(),
			(string) filemtime( $path ),
			true
		);
	}
endif;
add_action( 'wp_enqueue_scripts', 'nadlan_revenue_enqueue_premium_revenue_script' );

/* ---------------------------------------------------------------------------
 * CMS-editable hero image. Adds a Customizer control (Appearance → Customize →
 * "נדל״ן — תמונת שער") so the owner can swap the homepage/hero image without code.
 * When set, it overrides the CSS --nlx-hero variable via an inline <style>.
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_revenue_customize_hero' ) ) :
	function nadlan_revenue_customize_hero( $wp_customize ) {
		$wp_customize->add_section( 'nadlan_premium_media', array(
			'title'    => 'נדל״ן — תמונות פרימיום',
			'priority' => 30,
		) );
		$fields = array(
			'nadlan_hero_image'     => 'תמונת שער (עמוד הבית / ארכיונים)',
			'nadlan_coast_image'    => 'תמונת קו חוף (כרטיסי פרויקטים)',
			'nadlan_interior_image' => 'תמונת פנים (נכסים)',
		);
		foreach ( $fields as $key => $label ) {
			$wp_customize->add_setting( $key, array(
				'default'           => '',
				'sanitize_callback' => 'esc_url_raw',
				'transport'         => 'refresh',
			) );
			$wp_customize->add_control( new WP_Customize_Image_Control( $wp_customize, $key, array(
				'label'   => $label,
				'section' => 'nadlan_premium_media',
				'settings'=> $key,
			) ) );
		}
	}
endif;
add_action( 'customize_register', 'nadlan_revenue_customize_hero' );

if ( ! function_exists( 'nadlan_revenue_hero_inline_css' ) ) :
	function nadlan_revenue_hero_inline_css() {
		$hero     = esc_url( (string) get_theme_mod( 'nadlan_hero_image', '' ) );
		$coast    = esc_url( (string) get_theme_mod( 'nadlan_coast_image', '' ) );
		$interior = esc_url( (string) get_theme_mod( 'nadlan_interior_image', '' ) );
		if ( ! $hero && ! $coast && ! $interior ) { return; }
		$vars = '';
		if ( $hero )     { $vars .= '--nlx-hero:url("' . $hero . '");'; }
		if ( $coast )    { $vars .= '--nlx-coast:url("' . $coast . '");'; }
		if ( $interior ) { $vars .= '--nlx-interior:url("' . $interior . '");'; }
		echo "\n<style id=\"nadlan-hero-cms\">:root{" . $vars . "}</style>\n";
	}
endif;
add_action( 'wp_head', 'nadlan_revenue_hero_inline_css', 99 );


if ( ! function_exists( 'nadlan_revenue_block_styles' ) ) :
	/**
	 * Registers custom block styles.
	 *
	 * @since NadLan Revenue 1.0
	 *
	 * @return void
	 */
	function nadlan_revenue_block_styles() {
		register_block_style(
			'core/list',
			array(
				'name'         => 'checkmark-list',
				'label'        => __( 'Checkmark', 'nadlan-revenue' ),
				'inline_style' => '
				ul.is-style-checkmark-list {
					list-style-type: "\2713";
				}

				ul.is-style-checkmark-list li {
					padding-inline-start: 1ch;
				}',
			)
		);
	}
endif;
add_action( 'init', 'nadlan_revenue_block_styles' );

if ( ! function_exists( 'nadlan_revenue_pattern_categories' ) ) :
	/**
	 * Registers pattern categories.
	 *
	 * @since NadLan Revenue 1.0
	 *
	 * @return void
	 */
	function nadlan_revenue_pattern_categories() {

		register_block_pattern_category(
			'nadlan_revenue_page',
			array(
				'label'       => __( 'Pages', 'nadlan-revenue' ),
				'description' => __( 'A collection of full page layouts.', 'nadlan-revenue' ),
			)
		);

		register_block_pattern_category(
			'nadlan_revenue_post-format',
			array(
				'label'       => __( 'Post formats', 'nadlan-revenue' ),
				'description' => __( 'A collection of post format patterns.', 'nadlan-revenue' ),
			)
		);
	}
endif;
add_action( 'init', 'nadlan_revenue_pattern_categories' );

if ( ! function_exists( 'nadlan_revenue_register_block_bindings' ) ) :
	/**
	 * Registers the post format block binding source.
	 *
	 * @since NadLan Revenue 1.0
	 *
	 * @return void
	 */
	function nadlan_revenue_register_block_bindings() {
		register_block_bindings_source(
			'nadlan-revenue/format',
			array(
				'label'              => _x( 'Post format name', 'Label for the block binding placeholder in the editor', 'nadlan-revenue' ),
				'get_value_callback' => 'nadlan_revenue_format_binding',
			)
		);
	}
endif;
add_action( 'init', 'nadlan_revenue_register_block_bindings' );

if ( ! function_exists( 'nadlan_revenue_format_binding' ) ) :
	/**
	 * Callback function for the post format name block binding source.
	 *
	 * @since NadLan Revenue 1.0
	 *
	 * @return string|void Post format name, or nothing if the format is 'standard'.
	 */
	function nadlan_revenue_format_binding() {
		$post_format_slug = get_post_format();

		if ( $post_format_slug && 'standard' !== $post_format_slug ) {
			return get_post_format_string( $post_format_slug );
		}
	}
endif;

/* ============================================================================
 * NadLan Revenue customizations
 * Added 2026-05-28. Read skills/strategy-master.md before changing.
 *
 * Adds:
 *  - The nadlan_lead custom post type used by the public lead form.
 *  - The lead form admin-post handler with sanitization, nonce, and meta storage.
 *  - WordPress 7.0 Abilities API registrations under the nadlan/ namespace so
 *    AI agents (Codex, ChatGPT Operator, Antigravity, Claude) can discover
 *    what this site can do. See skills/abilities-api.md.
 *  - A small image-size for listing cards on archive pages.
 *
 * Intentionally NOT added (do not re-add without a skill-file revision):
 *  - register_nav_menus — block theme uses the block navigation, not classic
 *    nav menus.
 *  - A hand-rolled WebSite JSON-LD — Yoast SEO emits one already; two would
 *    conflict (see skills/yoast-config.md).
 * ========================================================================= */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_revenue_register_lead_type' ) ) :
	function nadlan_revenue_register_lead_type() {
		register_post_type(
			'nadlan_lead',
			array(
				'labels'       => array(
					'name'          => __( 'NadLan Leads', 'nadlan-revenue' ),
					'singular_name' => __( 'NadLan Lead', 'nadlan-revenue' ),
				),
				'public'       => false,
				'show_ui'      => true,
				'show_in_menu' => true,
				'menu_icon'    => 'dashicons-money-alt',
				'supports'     => array( 'title', 'editor', 'custom-fields' ),
				'capability_type' => 'post',
				'map_meta_cap'    => true,
			)
		);
	}
endif;
add_action( 'init', 'nadlan_revenue_register_lead_type' );

if ( ! function_exists( 'nadlan_revenue_clean' ) ) :
	function nadlan_revenue_clean( $key ) {
		return isset( $_POST[ $key ] ) ? sanitize_text_field( wp_unslash( $_POST[ $key ] ) ) : '';
	}
endif;

if ( ! function_exists( 'nadlan_revenue_handle_lead' ) ) :
	function nadlan_revenue_handle_lead() {
		if ( ! isset( $_POST['nadlan_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_nonce'] ) ), 'nadlan_lead' ) ) {
			wp_safe_redirect( add_query_arg( 'lead', 'bad_nonce', home_url( '/' ) ) );
			exit;
		}

		$name     = nadlan_revenue_clean( 'lead_name' );
		$phone    = nadlan_revenue_clean( 'lead_phone' );
		$email    = sanitize_email( wp_unslash( $_POST['lead_email'] ?? '' ) );
		$goal     = nadlan_revenue_clean( 'lead_goal' );
		$city     = nadlan_revenue_clean( 'lead_city' );
		$budget   = nadlan_revenue_clean( 'lead_budget' );
		$timeline = nadlan_revenue_clean( 'lead_timeline' );
		$message  = sanitize_textarea_field( wp_unslash( $_POST['lead_message'] ?? '' ) );

		$title   = sprintf( '%s - %s - %s', $name ?: 'Lead', $goal ?: 'General', current_time( 'Y-m-d H:i' ) );
		$lead_id = wp_insert_post(
			array(
				'post_type'    => 'nadlan_lead',
				'post_status'  => 'private',
				'post_title'   => $title,
				'post_content' => $message,
			),
			true
		);

		if ( ! is_wp_error( $lead_id ) ) {
			$fields = array(
				'name'         => $name,
				'phone'        => $phone,
				'email'        => $email,
				'goal'         => $goal,
				'city'         => $city,
				'budget'       => $budget,
				'timeline'     => $timeline,
				'source_url'   => esc_url_raw( wp_get_referer() ?: home_url( '/' ) ),
				'utm_source'   => nadlan_revenue_clean( 'utm_source' ),
				'utm_campaign' => nadlan_revenue_clean( 'utm_campaign' ),
			);
			foreach ( $fields as $key => $value ) {
				update_post_meta( $lead_id, $key, $value );
			}

			$admin_email = get_option( 'admin_email' );
			wp_mail( $admin_email, 'NadLan lead: ' . $title, print_r( $fields, true ) );
		}

		wp_safe_redirect( add_query_arg( 'lead', 'received', home_url( '/' ) ) );
		exit;
	}
endif;
add_action( 'admin_post_nopriv_nadlan_lead', 'nadlan_revenue_handle_lead' );
add_action( 'admin_post_nadlan_lead', 'nadlan_revenue_handle_lead' );

/* ----------------------------------------------------------------------------
 * WordPress 7.0 Abilities API registrations.
 * Lets AI agents discover what nad-lan.co.il can do via /wp-json/wp-abilities/v1/abilities
 * Safe-guarded with function_exists checks; if the Abilities API is unavailable
 * (older WP, disabled plugin) nothing fires.
 * ------------------------------------------------------------------------- */

if ( ! function_exists( 'nadlan_revenue_register_abilities' ) ) :
	function nadlan_revenue_register_abilities() {
		if ( ! function_exists( 'wp_register_ability' ) ) {
			return;
		}

		wp_register_ability(
			'nadlan/get-pillars',
			array(
				'label'              => __( 'List pillar pages', 'nadlan-revenue' ),
				'description'        => __( 'Returns the pillar pages defined in the nad-lan content strategy: buying, selling, investment, mortgage, tax/legal, urban renewal, professionals, new projects.', 'nadlan-revenue' ),
				'input_schema'       => array( 'type' => 'object', 'properties' => new \stdClass(), 'additionalProperties' => false ),
				'output_schema'      => array(
					'type'  => 'array',
					'items' => array(
						'type'       => 'object',
						'properties' => array(
							'slug'  => array( 'type' => 'string' ),
							'title' => array( 'type' => 'string' ),
							'url'   => array( 'type' => 'string' ),
						),
					),
				),
				'execute_callback'   => 'nadlan_revenue_ability_pillars',
				'permission_callback' => '__return_true',
			)
		);

		wp_register_ability(
			'nadlan/get-calculators',
			array(
				'label'              => __( 'List on-site calculators', 'nadlan-revenue' ),
				'description'        => __( 'Returns the slugs and URLs of all calculator pages on nad-lan.co.il: mortgage, purchase tax, valuation, investment cashflow, total purchase cost.', 'nadlan-revenue' ),
				'input_schema'       => array( 'type' => 'object', 'properties' => new \stdClass(), 'additionalProperties' => false ),
				'output_schema'      => array(
					'type'  => 'array',
					'items' => array(
						'type'       => 'object',
						'properties' => array(
							'slug'  => array( 'type' => 'string' ),
							'title' => array( 'type' => 'string' ),
							'url'   => array( 'type' => 'string' ),
						),
					),
				),
				'execute_callback'   => 'nadlan_revenue_ability_calculators',
				'permission_callback' => '__return_true',
			)
		);

		wp_register_ability(
			'nadlan/get-cities',
			array(
				'label'              => __( 'List city / neighborhood content pages', 'nadlan-revenue' ),
				'description'        => __( 'Returns the city and neighborhood price-guide pages currently published.', 'nadlan-revenue' ),
				'input_schema'       => array( 'type' => 'object', 'properties' => new \stdClass(), 'additionalProperties' => false ),
				'output_schema'      => array( 'type' => 'array' ),
				'execute_callback'   => 'nadlan_revenue_ability_cities',
				'permission_callback' => '__return_true',
			)
		);

		wp_register_ability(
			'nadlan/get-lead-stats',
			array(
				'label'              => __( 'Lead-form submission stats (private)', 'nadlan-revenue' ),
				'description'        => __( 'Returns count of leads received in the last 7 / 30 / 90 days. Requires manage_options. Never exposes lead PII.', 'nadlan-revenue' ),
				'input_schema'       => array( 'type' => 'object', 'properties' => new \stdClass(), 'additionalProperties' => false ),
				'output_schema'      => array(
					'type'       => 'object',
					'properties' => array(
						'last_7_days'  => array( 'type' => 'integer' ),
						'last_30_days' => array( 'type' => 'integer' ),
						'last_90_days' => array( 'type' => 'integer' ),
					),
				),
				'execute_callback'    => 'nadlan_revenue_ability_lead_stats',
				'permission_callback' => function () { return current_user_can( 'manage_options' ); },
			)
		);
	}
endif;
add_action( 'init', 'nadlan_revenue_register_abilities', 20 );

if ( ! function_exists( 'nadlan_revenue_ability_pillars' ) ) :
	function nadlan_revenue_ability_pillars() {
		$slugs = array(
			'buying-apartment'      => 'קניית דירה',
			'selling-apartment'     => 'מכירת דירה',
			'investment-apartment'  => 'דירה להשקעה',
			'real-estate-tax-advisor' => 'מיסוי מקרקעין',
			'real-estate-lawyer'    => 'עורך דין מקרקעין',
			'urban-renewal'         => 'התחדשות עירונית',
			'professionals'         => 'אנשי מקצוע',
			'new-projects'          => 'דירה מקבלן',
			'commercial-real-estate' => 'נדל"ן מסחרי',
		);
		$out = array();
		foreach ( $slugs as $slug => $label ) {
			$p = get_page_by_path( $slug );
			if ( $p ) {
				$out[] = array(
					'slug'  => $slug,
					'title' => $label,
					'url'   => get_permalink( $p ),
				);
			}
		}
		return $out;
	}
endif;

if ( ! function_exists( 'nadlan_revenue_ability_calculators' ) ) :
	function nadlan_revenue_ability_calculators() {
		$slugs = array(
			'mortgage-calculator',
			'purchase-tax-calculator',
			'property-value-estimator',
			'investment-property-cashflow-calculator',
			'apartment-purchase-cost-calculator',
		);
		$out = array();
		foreach ( $slugs as $slug ) {
			$p = get_page_by_path( $slug );
			if ( $p ) {
				$out[] = array(
					'slug'  => $slug,
					'title' => get_the_title( $p ),
					'url'   => get_permalink( $p ),
				);
			}
		}
		return $out;
	}
endif;

if ( ! function_exists( 'nadlan_revenue_ability_cities' ) ) :
	function nadlan_revenue_ability_cities() {
		$q = new WP_Query(
			array(
				'post_type'      => 'page',
				'post_status'    => 'publish',
				'posts_per_page' => 200,
				'fields'         => 'ids',
				'meta_query'     => array(),
			)
		);
		$patterns = array( '-apartment-prices', '-house-prices' );
		$out      = array();
		foreach ( $q->posts as $id ) {
			$slug = get_post_field( 'post_name', $id );
			foreach ( $patterns as $needle ) {
				if ( false !== strpos( $slug, $needle ) ) {
					$out[] = array(
						'slug'  => $slug,
						'title' => get_the_title( $id ),
						'url'   => get_permalink( $id ),
					);
					break;
				}
			}
		}
		return $out;
	}
endif;

if ( ! function_exists( 'nadlan_revenue_ability_lead_stats' ) ) :
	function nadlan_revenue_ability_lead_stats() {
		$out = array(
			'last_7_days'  => 0,
			'last_30_days' => 0,
			'last_90_days' => 0,
		);
		foreach ( array( 7, 30, 90 ) as $days ) {
			$q = new WP_Query(
				array(
					'post_type'      => 'nadlan_lead',
					'post_status'    => 'any',
					'posts_per_page' => -1,
					'fields'         => 'ids',
					'date_query'     => array(
						array( 'after' => $days . ' days ago' ),
					),
				)
			);
			$out[ "last_{$days}_days" ] = (int) $q->found_posts;
		}
		return $out;
	}
endif;

/* ============================================================================
 * Premium site-wide presentation layer - theme owned, no plugin edits.
 *
 * This is intentionally CMS-backed: homepage counts, project cards, professional
 * cards, tool links and guide links are pulled from WordPress data at render time.
 * It replaces the weak front-page block composition while keeping one canonical
 * homepage URL and leaving nadlan-config business logic untouched.
 * ========================================================================= */

if ( ! function_exists( 'nadlan_revenue_premium_asset' ) ) :
	function nadlan_revenue_premium_asset( $file ) {
		return get_parent_theme_file_uri( 'assets/premium-site/' . ltrim( $file, '/' ) );
	}
endif;

if ( ! function_exists( 'nadlan_revenue_count_posts_safe' ) ) :
	function nadlan_revenue_count_posts_safe( $post_type ) {
		$count = wp_count_posts( $post_type );
		return isset( $count->publish ) ? (int) $count->publish : 0;
	}
endif;

if ( ! function_exists( 'nadlan_revenue_page_url' ) ) :
	function nadlan_revenue_page_url( $path, $fallback = '' ) {
		$page = get_page_by_path( $path );
		return $page ? get_permalink( $page ) : home_url( $fallback ?: '/' . trim( $path, '/' ) . '/' );
	}
endif;

if ( ! function_exists( 'nadlan_revenue_card_media' ) ) :
	function nadlan_revenue_card_media( $post_id, $fallback = 'architectural-model.jpg' ) {
		if ( has_post_thumbnail( $post_id ) ) {
			$thumb = get_the_post_thumbnail_url( $post_id, 'large' );
			if ( $thumb ) { return $thumb; }
		}
		$photos = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $post_id, 'photos_csv', true ) ) ) );
		if ( ! empty( $photos[0] ) ) { return $photos[0]; }
		return nadlan_revenue_premium_asset( $fallback );
	}
endif;

if ( ! function_exists( 'nadlan_revenue_premium_projects' ) ) :
	function nadlan_revenue_premium_projects() {
		$ids = array();
		$q1  = new WP_Query( array(
			'post_type'      => 'nadlan_project',
			'post_status'    => 'publish',
			'posts_per_page' => 4,
			'fields'         => 'ids',
			'meta_query'     => array(
				array( 'key' => 'paid_tier', 'value' => array( 'premier', 'pro' ), 'compare' => 'IN' ),
			),
			'orderby'        => 'modified',
			'order'          => 'DESC',
		) );
		$ids = $q1->posts;
		wp_reset_postdata();
		if ( count( $ids ) < 4 ) {
			$q2 = new WP_Query( array(
				'post_type'      => 'nadlan_project',
				'post_status'    => 'publish',
				'posts_per_page' => 4 - count( $ids ),
				'fields'         => 'ids',
				'post__not_in'   => $ids,
				'orderby'        => 'modified',
				'order'          => 'DESC',
			) );
			$ids = array_merge( $ids, $q2->posts );
			wp_reset_postdata();
		}
		return array_slice( array_unique( array_map( 'intval', $ids ) ), 0, 4 );
	}
endif;

if ( ! function_exists( 'nadlan_revenue_premium_professionals' ) ) :
	function nadlan_revenue_premium_professionals() {
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_professional',
			'post_status'    => 'publish',
			'posts_per_page' => 6,
			'fields'         => 'ids',
			'orderby'        => 'modified',
			'order'          => 'DESC',
		) );
		$ids = $q->posts;
		wp_reset_postdata();
		return array_map( 'intval', $ids );
	}
endif;

if ( ! function_exists( 'nadlan_revenue_premium_front_page' ) ) :
	function nadlan_revenue_premium_front_page() {
		$projects_count = nadlan_revenue_count_posts_safe( 'nadlan_project' );
		$pros_count     = nadlan_revenue_count_posts_safe( 'nadlan_professional' );
		$terms_count    = nadlan_revenue_count_posts_safe( 'nadlan_term' );
		$project_url    = get_post_type_archive_link( 'nadlan_project' ) ?: home_url( '/projects/' );
		$pro_url        = get_post_type_archive_link( 'nadlan_professional' ) ?: home_url( '/professionals/' );
		$property_url   = get_post_type_archive_link( 'nadlan_property' ) ?: home_url( '/properties/' );
		$join_url       = home_url( '/join-pro/' );
		$studio_url     = home_url( '/studio/' );
		$rainbow_url    = home_url( '/projects/rainbow-tel-aviv/' );
		$projects       = nadlan_revenue_premium_projects();
		$pros           = nadlan_revenue_premium_professionals();

		ob_start();
		?>
<div class="nlux-home" dir="rtl">
	<section class="nlux-hero" aria-label="NadLan">
		<div class="nlux-hero-media" aria-hidden="true"></div>
		<div class="nlux-hero-copy">
			<p class="nlux-kicker">פרויקטים חדשים · ישראל</p>
			<h1>NadLan: בוחרים פרויקט ודירה לפני שפונים ליזם</h1>
			<p class="nlux-intro">סיורי פרויקטים בתלת ממד, בחירת דירה על הבניין, אומדני מחיר, סביבת הפרויקט, מחשבונים ואנשי מקצוע במקום אחד, לרוכשים בישראל ולמשקיעים מחוץ לישראל.</p>
			<form class="nlux-search" method="get" action="<?php echo esc_url( $project_url ); ?>">
				<input type="search" name="q" placeholder="חפשו פרויקט, עיר או יזם">
				<input type="text" name="city" placeholder="עיר">
				<button type="submit">חפשו פרויקט</button>
			</form>
			<div class="nlux-actions">
				<a href="<?php echo esc_url( $rainbow_url ); ?>">ראו בחירת דירה בתלת ממד</a>
				<a href="<?php echo esc_url( $project_url ); ?>">לכל הפרויקטים</a>
				<a href="<?php echo esc_url( $join_url ); ?>">מסלולי יזמים</a>
			</div>
		</div>
		<div class="nlux-hero-panel" aria-label="נתוני המאגר">
			<div><b><?php echo number_format_i18n( $projects_count ); ?></b><span>פרויקטים</span></div>
			<div><b><?php echo number_format_i18n( $pros_count ); ?></b><span>בעלי מקצוע</span></div>
			<div><b><?php echo number_format_i18n( $terms_count ); ?></b><span>מונחים ומדריכים</span></div>
		</div>
	</section>


	<section class="nlux-paths" aria-label="מסלולי פעולה">
		<a class="nlux-path" href="<?php echo esc_url( $rainbow_url ); ?>"><span>01</span><h2>פותחים סיור פרויקט</h2><p>בחרו דירה על הבניין, בדקו קומה, כיוון ונוף, ורק אחר כך פנו ליזם.</p></a>
		<a class="nlux-path" href="<?php echo esc_url( $project_url ); ?>"><span>02</span><h2>משווים פרויקטים לפי עיר</h2><p>דירה מקבלן, התחדשות עירונית, סטטוס פרויקט ותמונות במקום אחד.</p></a>
		<a class="nlux-path" href="<?php echo esc_url( nadlan_revenue_page_url( 'mortgage-calculator', '/mortgage-calculator/' ) ); ?>"><span>03</span><h2>מחשבים עלויות לפני חתימה</h2><p>משכנתא, מס רכישה ועלויות עסקה לפני שמתקדמים לשיחה או חוזה.</p></a>
		<a class="nlux-path" href="<?php echo esc_url( $join_url ); ?>"><span>04</span><h2>מציגים פרויקט למשקיעים</h2><p>עמוד פרויקט עם תמונות, מפה, בחירת דירות ופנייה מסודרת לקונים בארץ ומחוץ לישראל.</p></a>
	</section>

	<section class="nlux-showcase" aria-label="פרויקטים נבחרים">
		<div class="nlux-section-head">
			<p class="nlux-kicker">פרויקטים חדשים</p>
			<h2>פרויקטים שאפשר להתחיל לבדוק עכשיו</h2>
			<a href="<?php echo esc_url( $project_url ); ?>">לכל הפרויקטים</a>
		</div>
		<div class="nlux-project-grid">
			<?php foreach ( $projects as $i => $id ) :
				$city   = trim( (string) get_post_meta( $id, 'city', true ) );
				$status = trim( (string) get_post_meta( $id, 'project_status', true ) );
				$dev    = trim( (string) get_post_meta( $id, 'developer_name', true ) );
				$units  = trim( (string) get_post_meta( $id, 'num_units', true ) );
				$nlux_fallbacks = array( 'tel-aviv-coast-skyline.jpg', 'sea-view-interior.jpg', 'tel-aviv-skyline-blueprint.jpg' );
				$img    = nadlan_revenue_card_media( $id, $nlux_fallbacks[ $i % count( $nlux_fallbacks ) ] );
				?>
				<a class="nlux-project-card" href="<?php echo esc_url( get_permalink( $id ) ); ?>">
					<img src="<?php echo esc_url( $img ); ?>" alt="<?php echo esc_attr( get_the_title( $id ) ); ?>" loading="lazy">
					<span class="nlux-card-chip"><?php echo $status ? esc_html( $status ) : 'פרויקט'; ?></span>
					<div>
						<h3><?php echo esc_html( get_the_title( $id ) ); ?></h3>
						<p><?php echo esc_html( implode( ' · ', array_filter( array( $city, $dev, $units ? $units . ' יח״ד' : '' ) ) ) ); ?></p>
					</div>
				</a>
			<?php endforeach; ?>
		</div>
	</section>

	<section class="nlux-data-band" aria-label="למה NadLan">
		<div><strong>בחירת דירה חזותית</strong><span>כאשר יש נתונים, רואים קומה, כיוון ונקודת מבט</span></div>
		<div><strong>מקורות גלויים</strong><span>פרויקטים, יזמים ובעלי מקצוע עם מידע שניתן לבדוק</span></div>
		<div><strong>פנייה אחרי בדיקה</strong><span>משווים, מחשבים ורק אז מתקדמים לשיחה מסודרת</span></div>
	</section>

	<section class="nlux-tools" aria-label="כלים ומדריכים">
		<div class="nlux-section-head">
			<p class="nlux-kicker">לפני שחותמים</p>
			<h2>מחשבונים וכלים חינמיים לבדיקת העסקה</h2>
		</div>
		<div class="nlux-tool-grid">
			<a href="<?php echo esc_url( nadlan_revenue_page_url( 'purchase-tax-calculator', '/purchase-tax-calculator/' ) ); ?>">מס רכישה</a>
			<a href="<?php echo esc_url( nadlan_revenue_page_url( 'mortgage-calculator', '/mortgage-calculator/' ) ); ?>">מחשבון משכנתא</a>
			<a href="<?php echo esc_url( nadlan_revenue_page_url( 'property-value', '/property-value/' ) ); ?>">בדיקת שווי</a>
			<a href="<?php echo esc_url( nadlan_revenue_page_url( 'real-estate-lawyer/land-purchase-checklist', '/real-estate-lawyer/land-purchase-checklist/' ) ); ?>">בדיקת מסמכים</a>
			<a href="<?php echo esc_url( $property_url ); ?>">נכסים</a>
			<a href="<?php echo esc_url( home_url( '/glossary/' ) ); ?>">מילון נדל״ן</a>
		</div>
	</section>

	<section class="nlux-pros" aria-label="אנשי מקצוע נבחרים">
		<div class="nlux-section-head">
			<p class="nlux-kicker">אינדקס בעלי מקצוע</p>
			<h2>בעלי מקצוע מאומתים לנדל״ן</h2>
			<a href="<?php echo esc_url( $pro_url ); ?>">לכל אנשי המקצוע</a>
		</div>
		<div class="nlux-pro-grid">
			<?php foreach ( $pros as $id ) :
				$city = trim( (string) get_post_meta( $id, 'city', true ) );
				$cls  = trim( (string) get_post_meta( $id, 'classification', true ) );
				$name = trim( wp_strip_all_tags( get_the_title( $id ) ) );
				$mark = function_exists( 'mb_substr' ) ? mb_substr( $name, 0, 1 ) : substr( $name, 0, 1 );
				?>
				<a class="nlux-pro-card" href="<?php echo esc_url( get_permalink( $id ) ); ?>">
					<span><?php echo esc_html( $mark ); ?></span>
					<h3><?php echo esc_html( get_the_title( $id ) ); ?></h3>
					<p><?php echo esc_html( implode( ' · ', array_filter( array( $city, $cls ) ) ) ); ?></p>
				</a>
			<?php endforeach; ?>
		</div>
	</section>

	<section class="nlux-final-cta" aria-label="פרסום פרימיום">
		<div>
			<p class="nlux-kicker">תצוגת פרויקט ליזמים</p>
			<h2>רוצים להציג פרויקט ברמה שמתאימה למשקיעים?</h2>
			<p>נבנה עמוד פרויקט עם תמונות, מפה, בחירת דירות, מידע סביבתי ופנייה ישירה. מתאים ליזמים שרוצים להראות את הפרויקט לפני שיחת מכירה.</p>
		</div>
		<div class="nlux-actions">
			<a href="<?php echo esc_url( $join_url ); ?>">מסלולי יזמים</a>
			<a href="<?php echo esc_url( $studio_url ); ?>">כניסת מפרסמים</a>
		</div>
	</section>
</div>
		<?php
		return ob_get_clean();
	}
endif;

add_filter( 'the_content', function ( $content ) {
	if ( is_front_page() && in_the_loop() && is_main_query() ) {
		// LIVE (owner-approved): the designed home-showroom homepage (gallery 3D + multilingual)
		// is now active for all visitors. Fully reversible WITHOUT a code edit: return false from
		// the nadlan_revenue_use_home_showroom filter (or add a small mu-plugin) to fall back to the
		// legacy front page instantly.
		$home_showroom = get_parent_theme_file_path( 'patterns/nadlan-home-showroom.php' );
		if ( apply_filters( 'nadlan_revenue_use_home_showroom', true ) && file_exists( $home_showroom ) ) {
			ob_start();
			include $home_showroom;
			$out = trim( (string) ob_get_clean() );
			if ( $out !== '' ) {
				return $out;
			}
		}
		return nadlan_revenue_premium_front_page();
	}
	return $content;
}, 99 );

if ( ! function_exists( 'nadlan_revenue_home_seo_title' ) ) :
	function nadlan_revenue_home_seo_title() {
		return 'דירות חדשות ופרויקטים עם בחירת דירה בתלת ממד | NadLan';
	}
endif;

if ( ! function_exists( 'nadlan_revenue_home_seo_description' ) ) :
	function nadlan_revenue_home_seo_description() {
		return 'השוו פרויקטים חדשים בישראל, בדקו זמינות דירות לפי קומה ונוף, ראו אומדן מחיר לא מחייב וקבלו מידע ברור בעברית ובשפות למשקיעים מחו״ל.';
	}
endif;

add_filter( 'pre_get_document_title', function ( $title ) {
	if ( is_front_page() ) {
		return nadlan_revenue_home_seo_title();
	}
	return $title;
}, 40 );

add_filter( 'wpseo_title', function ( $title ) {
	if ( is_front_page() ) {
		return nadlan_revenue_home_seo_title();
	}
	return $title;
}, 40 );

add_filter( 'wpseo_metadesc', function ( $description ) {
	if ( is_front_page() ) {
		return nadlan_revenue_home_seo_description();
	}
	return $description;
}, 40 );

if ( ! function_exists( 'nadlan_revenue_home_schema_projects' ) ) :
	function nadlan_revenue_home_schema_projects() {
		$items = array();
		$path  = get_parent_theme_file_path( 'assets/engine/projects.json' );
		if ( file_exists( $path ) ) {
			$raw  = (string) file_get_contents( $path );
			$data = json_decode( $raw, true );
			if ( is_array( $data ) && ! empty( $data['projects'] ) && is_array( $data['projects'] ) ) {
				foreach ( $data['projects'] as $project ) {
					if ( ! is_array( $project ) || empty( $project['name'] ) || empty( $project['project_url'] ) ) {
						continue;
					}
					$items[] = array(
						'name'        => sanitize_text_field( (string) $project['name'] ),
						'url'         => home_url( '/' . ltrim( (string) $project['project_url'], '/' ) ),
						'description' => sanitize_text_field( (string) ( $project['sub'] ?? $project['location'] ?? '' ) ),
					);
				}
			}
		}
		return array_slice( $items, 0, 6 );
	}
endif;

if ( ! function_exists( 'nadlan_revenue_home_jsonld' ) ) :
	function nadlan_revenue_home_jsonld() {
		if ( ! is_front_page() ) {
			return;
		}

		$home_url = home_url( '/' );
		$graph    = array(
			array(
				'@type' => 'Organization',
				'@id'   => $home_url . '#organization',
				'name'  => 'NadLan',
				'url'   => $home_url,
			),
			array(
				'@type'           => 'WebSite',
				'@id'             => $home_url . '#website',
				'name'            => 'NadLan',
				'url'             => $home_url,
				'inLanguage'      => 'he-IL',
				'publisher'       => array( '@id' => $home_url . '#organization' ),
				'potentialAction' => array(
					'@type'       => 'SearchAction',
					'target'      => home_url( '/?s={search_term_string}' ),
					'query-input' => 'required name=search_term_string',
				),
			),
			array(
				'@type'       => 'WebPage',
				'@id'         => $home_url . '#webpage',
				'name'        => nadlan_revenue_home_seo_title(),
				'description' => nadlan_revenue_home_seo_description(),
				'url'         => $home_url,
				'inLanguage'  => 'he-IL',
				'isPartOf'    => array( '@id' => $home_url . '#website' ),
			),
		);

		$projects = nadlan_revenue_home_schema_projects();
		if ( $projects ) {
			$list = array(
				'@type'           => 'ItemList',
				'@id'             => $home_url . '#projects',
				'name'            => 'פרויקטים חדשים להשוואה',
				'itemListElement' => array(),
			);
			foreach ( $projects as $index => $project ) {
				$list['itemListElement'][] = array(
					'@type'    => 'ListItem',
					'position' => $index + 1,
					'url'      => $project['url'],
					'name'     => $project['name'],
				);
			}
			$graph[] = $list;
		}

		$schema = array(
			'@context' => 'https://schema.org',
			'@graph'   => $graph,
		);
		echo '<script type="application/ld+json" id="nadlan-home-schema">' . wp_json_encode( $schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	}
endif;
add_action( 'wp_head', 'nadlan_revenue_home_jsonld', 20 );

add_filter( 'render_block', function ( $block_content, $block ) {
	if (
		isset( $block['blockName'] )
		&& $block['blockName'] === 'core/post-title'
		&& ( is_front_page() || is_page( array( 'join-pro', 'sitemap' ) ) )
	) {
		return '';
	}
	return $block_content;
}, 9, 2 );

/* ---------------------------------------------------------------------------
 * Premium revenue journey layer.
 *
 * Theme-owned presentation and journey safety only: no plugin module edits, no
 * product IDs changed, no order activation logic changed.
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_revenue_money_product_ids' ) ) :
	function nadlan_revenue_money_product_ids() {
		return array( 475, 476, 477, 489, 490 );
	}
endif;

if ( ! function_exists( 'nadlan_revenue_request_path' ) ) :
	function nadlan_revenue_request_path() {
		$uri = isset( $_SERVER['REQUEST_URI'] ) ? (string) wp_unslash( $_SERVER['REQUEST_URI'] ) : '/';
		$path = (string) wp_parse_url( $uri, PHP_URL_PATH );
		return '/' . ltrim( $path, '/' );
	}
endif;

if ( ! function_exists( 'nadlan_revenue_is_money_path' ) ) :
	function nadlan_revenue_is_money_path() {
		$product_ids = nadlan_revenue_money_product_ids();
		$add_to_cart = isset( $_GET['add-to-cart'] ) ? absint( wp_unslash( $_GET['add-to-cart'] ) ) : 0; // phpcs:ignore WordPress.Security.NonceVerification.Recommended
		if ( $add_to_cart && in_array( $add_to_cart, $product_ids, true ) ) {
			return true;
		}

		$path = nadlan_revenue_request_path();
		$money_prefixes = array( '/cart', '/checkout', '/my-account', '/join-pro' );
		foreach ( $money_prefixes as $prefix ) {
			if ( strpos( $path, $prefix ) === 0 ) {
				return true;
			}
		}

		if ( function_exists( 'is_cart' ) && is_cart() ) { return true; }
		if ( function_exists( 'is_checkout' ) && is_checkout() ) { return true; }
		if ( function_exists( 'is_account_page' ) && is_account_page() ) { return true; }
		if ( function_exists( 'is_product' ) && is_product() ) {
			$product_id = get_queried_object_id();
			if ( in_array( (int) $product_id, $product_ids, true ) ) {
				return true;
			}
		}

		return false;
	}
endif;

if ( ! function_exists( 'nadlan_revenue_is_commerce_screen' ) ) :
	function nadlan_revenue_is_commerce_screen() {
		$path = nadlan_revenue_request_path();
		$commerce_prefixes = array( '/cart', '/checkout', '/my-account', '/shop', '/product' );
		foreach ( $commerce_prefixes as $prefix ) {
			if ( strpos( $path, $prefix ) === 0 ) {
				return true;
			}
		}

		if ( function_exists( 'is_cart' ) && is_cart() ) { return true; }
		if ( function_exists( 'is_checkout' ) && is_checkout() ) { return true; }
		if ( function_exists( 'is_account_page' ) && is_account_page() ) { return true; }
		if ( function_exists( 'is_product' ) && is_product() ) { return true; }
		if ( function_exists( 'is_shop' ) && is_shop() ) { return true; }
		if ( function_exists( 'is_product_taxonomy' ) && is_product_taxonomy() ) { return true; }

		return false;
	}
endif;

add_action( 'template_redirect', function () {
	if ( ! is_admin() && ! nadlan_revenue_is_commerce_screen() && function_exists( 'wc_clear_notices' ) ) {
		wc_clear_notices();
	}
}, 0 );

add_action( 'wp_enqueue_scripts', function () {
	if ( is_admin() || nadlan_revenue_is_commerce_screen() ) {
		return;
	}

	$styles = array(
		'woocommerce-general',
		'woocommerce-layout',
		'woocommerce-smallscreen',
		'woocommerce-blocktheme',
		'woocommerce-blocktheme-rtl',
		'wc-blocks-style',
		'wc-blocks-style-all-products',
		'wc-blocks-style-mini-cart',
		'wc-blocks-style-mini-cart-contents',
		'wc-blocks-style-mini-cart-contents-rtl',
		'wc-blocks-packages-style',
		'wc-blocks-vendors-style',
		'wc-blocks-style-components',
		'wc-blocks-style-reviews',
	);
	foreach ( $styles as $handle ) {
		wp_dequeue_style( $handle );
	}

	$scripts = array(
		'wc-add-to-cart',
		'woocommerce',
		'wc-cart-fragments',
		'wc-blocks',
		'wc-blocks-vendors',
		'wc-blocks-data-store',
		'wc-blocks-middleware',
		'wc-block-mini-cart-frontend',
		'wc-block-mini-cart-contents',
		'wc-blocks-checkout',
		'wc-interactivity',
	);
	foreach ( $scripts as $handle ) {
		wp_dequeue_script( $handle );
	}
}, 100 );

add_filter( 'render_block', function ( $block_content, $block ) {
	$block_name = isset( $block['blockName'] ) ? (string) $block['blockName'] : '';
	$slug       = isset( $block['attrs']['slug'] ) ? (string) $block['attrs']['slug'] : '';

	if ( ! is_admin() && ! nadlan_revenue_is_commerce_screen() && strpos( $block_name, 'woocommerce/' ) === 0 ) {
		return '';
	}

	if (
		$block_name === 'core/pattern'
		&& $slug === 'nadlan-revenue/more-posts'
		&& is_singular( array( 'nadlan_project', 'nadlan_professional', 'nadlan_property' ) )
	) {
		return '';
	}

	return $block_content;
}, 20, 2 );

add_filter( 'woocommerce_coming_soon_exclude', function ( $is_excluded ) {
	if ( nadlan_revenue_is_money_path() ) {
		return true;
	}
	return $is_excluded;
}, 20 );

if ( ! function_exists( 'nadlan_revenue_is_public_customer_gate' ) ) :
	function nadlan_revenue_is_public_customer_gate() {
		$path = nadlan_revenue_request_path();
		if ( get_query_var( 'nadlan_advertiser_center' ) || get_query_var( 'nadlan_studio' ) ) {
			return true;
		}
		return strpos( $path, '/advertiser-center' ) === 0
			|| strpos( $path, '/advertiser-dashboard' ) === 0
			|| strpos( $path, '/studio' ) === 0;
	}
endif;

if ( ! function_exists( 'nadlan_revenue_premium_gateway_markup' ) ) :
	function nadlan_revenue_premium_gateway_markup( $mode = 'center' ) {
		$is_studio = $mode === 'studio';
		$my_account = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'myaccount' ) : '';
		$account_url = add_query_arg(
			'redirect_to',
			rawurlencode( $is_studio ? home_url( '/studio/' ) : home_url( '/advertiser-center/' ) ),
			$my_account ?: home_url( '/my-account/' )
		);
		$pricing_url = home_url( '/join-pro/' );
		$claim_url   = home_url( '/professionals/' );

		ob_start();
		?>
<main class="nlrx-gate" dir="rtl">
	<section class="nlrx-gate-hero">
		<div class="nlrx-gate-copy">
			<p class="nlrx-eyebrow">מערכת פרסום וניהול נכסים</p>
			<h1><?php echo esc_html( $is_studio ? 'כניסה לסטודיו העריכה של NadLan' : 'מרכז הפרסום של NadLan' ); ?></h1>
			<p>כאן מפרסמים מנהלים פרויקט, נכס או כרטיס מקצועי: תמונות, פרטי קשר, מיקום, פניות ושדרוגי חשיפה. קודם מתחברים לחשבון, ואז ממשיכים לעריכה או למסלול הפרסום.</p>
			<div class="nlrx-actions">
				<a class="nlrx-btn nlrx-btn-primary" href="<?php echo esc_url( $account_url ); ?>">כניסה או פתיחת חשבון</a>
				<a class="nlrx-btn nlrx-btn-ghost" href="<?php echo esc_url( $pricing_url ); ?>">מסלולי פרסום</a>
			</div>
		</div>
		<div class="nlrx-gate-panel" aria-label="שלבי התחלה">
			<div><span>01</span><strong>יוצרים חשבון</strong><p>שם, אימייל וסיסמה. אין צורך לדעת וורדפרס.</p></div>
			<div><span>02</span><strong>בוחרים או תובעים כרטיס</strong><p>פרויקט, נכס או כרטיס מקצועי שכבר קיים במאגר.</p></div>
			<div><span>03</span><strong>מעלים תמונות ומידע</strong><p>סטודיו עריכה עם שדות ברורים ותצוגה ציבורית.</p></div>
			<div><span>04</span><strong>משדרגים חשיפה</strong><p>Pro, Premier, פרויקט או נכס מקודם במסלול תשלום מאובטח.</p></div>
		</div>
	</section>
	<section class="nlrx-gate-proof">
		<a href="<?php echo esc_url( $claim_url ); ?>">איתור כרטיס קיים</a>
		<a href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">צפייה בפרויקטים</a>
		<a href="<?php echo esc_url( home_url( '/properties/' ) ); ?>">נכסים</a>
	</section>
</main>
		<?php
		return ob_get_clean();
	}
endif;

add_action( 'template_redirect', function () {
	if ( is_admin() || is_user_logged_in() || ! nadlan_revenue_is_public_customer_gate() ) {
		return;
	}
	$mode = strpos( nadlan_revenue_request_path(), '/studio' ) === 0 || get_query_var( 'nadlan_studio' ) ? 'studio' : 'center';
	status_header( 200 );
	get_header();
	echo nadlan_revenue_premium_gateway_markup( $mode ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
	get_footer();
	exit;
}, 1 );

if ( ! function_exists( 'nadlan_revenue_price_plans' ) ) :
	function nadlan_revenue_price_plans() {
		return array(
			array(
				'id'       => 476,
				'name'     => 'Pro מקצועי',
				'price'    => '₪349',
				'period'   => 'לחודש חשיפה',
				'tone'     => 'ink',
				'badge'    => 'לכרטיס מקצועי',
				'features' => array( 'כרטיס בולט יותר בתוצאות', 'תמונות ופרטי קשר מסודרים', 'כניסה למרכז הפרסום', 'שדרוג לכרטיס קיים' ),
			),
			array(
				'id'       => 477,
				'name'     => 'Premier מקצועי',
				'price'    => '₪749',
				'period'   => 'לחודש חשיפה',
				'tone'     => 'gold',
				'badge'    => 'מומלץ',
				'features' => array( 'נוכחות פרימיום בכרטיס', 'חשיפה חזקה יותר בקטלוג', 'עמוד עשיר עם תמונות ומידע', 'מתאים למשרדים ומומחים מובילים' ),
			),
			array(
				'id'       => 489,
				'name'     => 'Project Premier',
				'price'    => '₪3,990',
				'period'   => 'קמפיין לפרויקט',
				'tone'     => 'deep',
				'badge'    => 'ליזמים',
				'features' => array( 'פרויקט מובלט בקטלוג', 'גלריה ותיאור עשיר', 'הפניות למתעניינים', 'מתאים לשיווק פרויקט חדש' ),
			),
			array(
				'id'       => 490,
				'name'     => 'Property Pro',
				'price'    => '₪299',
				'period'   => 'לנכס מקודם',
				'tone'     => 'light',
				'badge'    => 'לנכס בודד',
				'features' => array( 'נכס מודגש בתוצאות', 'תמונות, מיקום ופרטי קשר', 'מסלול מהיר לפרסום', 'מתאים למוכרים ומשכירים' ),
			),
		);
	}
endif;

if ( ! function_exists( 'nadlan_revenue_premium_join_page' ) ) :
	function nadlan_revenue_premium_join_page() {
		$plans = nadlan_revenue_price_plans();
		ob_start();
		?>
<div class="nlrx-pricing" dir="rtl">
	<section class="nlrx-pricing-hero">
		<div>
			<p class="nlrx-eyebrow">פרסום נדל״ן פרימיום</p>
			<h1>מסלולי חשיפה לפרויקטים, נכסים ואנשי מקצוע</h1>
			<p>בונים נוכחות שמרגישה כמו נכס יוקרתי: עמוד עשיר, תמונות, פרטי קשר, מיקום, פניות ומרכז ניהול אחד. המטרה פשוטה: להפוך מבקר למתעניין אמיתי.</p>
		</div>
		<div class="nlrx-pricing-proof">
			<strong>תשלום מאובטח + חשבונית</strong>
			<span>תשלום מאובטח, הזמנה מסודרת, חיבור לכרטיס לאחר רכישה.</span>
		</div>
	</section>
	<section class="nlrx-plan-grid" aria-label="מסלולי פרסום">
		<?php foreach ( $plans as $plan ) : ?>
			<article class="nlrx-plan nlrx-plan-<?php echo esc_attr( $plan['tone'] ); ?>">
				<span class="nlrx-plan-badge"><?php echo esc_html( $plan['badge'] ); ?></span>
				<h2><?php echo esc_html( $plan['name'] ); ?></h2>
				<p class="nlrx-price"><b><?php echo esc_html( $plan['price'] ); ?></b><span><?php echo esc_html( $plan['period'] ); ?></span></p>
				<ul>
					<?php foreach ( $plan['features'] as $feature ) : ?>
						<li><?php echo esc_html( $feature ); ?></li>
					<?php endforeach; ?>
				</ul>
				<a class="nlrx-btn <?php echo $plan['tone'] === 'gold' || $plan['tone'] === 'deep' ? 'nlrx-btn-primary' : 'nlrx-btn-secondary'; ?>" href="<?php echo esc_url( home_url( '/cart/?add-to-cart=' . (int) $plan['id'] ) ); ?>">בחירת מסלול</a>
			</article>
		<?php endforeach; ?>
	</section>
	<section class="nlrx-revenue-flow" aria-label="איך זה עובד">
		<div><span>1</span><strong>בוחרים מסלול</strong><p>הכרטיס או הפרויקט מקבל את מסלול החשיפה הנכון.</p></div>
		<div><span>2</span><strong>משלימים תשלום</strong><p>המערכת פותחת הזמנה מסודרת ומחברת אותה לכרטיס לאחר הרכישה.</p></div>
		<div><span>3</span><strong>מחברים לכרטיס</strong><p>אם כבר יש כרטיס, מחברים אותו. אם לא, מרכז הפרסום מאפשר בחירה.</p></div>
		<div><span>4</span><strong>מעלים תמונות ומידע</strong><p>הסטודיו מציג שדות ברורים, גלריה ומפה.</p></div>
	</section>
</div>
		<?php
		return ob_get_clean();
	}
endif;

add_filter( 'the_content', function ( $content ) {
	if ( is_page( 'join-pro' ) && in_the_loop() && is_main_query() ) {
		return nadlan_revenue_premium_join_page();
	}
	return $content;
}, 98 );

add_action( 'login_enqueue_scripts', function () {
	$logo = esc_url( get_site_icon_url( 96 ) );
	?>
	<style>
		body.login{min-height:100vh;background:radial-gradient(circle at 72% 8%,rgba(215,189,130,.18),transparent 34%),linear-gradient(135deg,#081d1d,#17130f 58%,#f4efe6 58.2%,#f8f3eb)!important;font-family:Heebo,Arial,sans-serif!important;color:#15130f}
		body.login #login{width:min(420px,calc(100% - 36px));padding:clamp(42px,8vw,84px) 0 32px}
		body.login h1 a{width:96px;height:96px;border-radius:50%;background:<?php echo $logo ? 'url(' . $logo . ') center/68px 68px no-repeat,' : ''; ?>linear-gradient(135deg,#f6e4ad,#926b2b)!important;box-shadow:0 24px 60px rgba(0,0,0,.28),inset 0 0 0 1px rgba(255,255,255,.42)}
		body.login form{border:1px solid rgba(167,124,53,.22);border-radius:24px;background:rgba(255,253,248,.92);box-shadow:0 28px 90px rgba(13,13,11,.18);padding:28px}
		body.login label{font-weight:800;color:#1d1912}
		body.login input.input{min-height:48px;border:1px solid #d6cbbb;border-radius:14px;background:#fffdf8;box-shadow:none;font-size:16px}
		body.login input.input:focus{border-color:#a77c35;box-shadow:0 0 0 3px rgba(167,124,53,.18)}
		body.login .button-primary{min-height:48px;border:0;border-radius:999px;background:linear-gradient(135deg,#16130f,#3a2f20 58%,#a77c35)!important;font-weight:900;box-shadow:0 16px 34px rgba(13,13,11,.2)}
		body.login #nav a,body.login #backtoblog a{color:#f4e8d2!important;font-weight:800;text-decoration:none}
	</style>
	<?php
} );

add_filter( 'login_headerurl', function () {
	return home_url( '/' );
} );

add_filter( 'login_headertext', function () {
	return get_bloginfo( 'name' );
} );

/**
 * TEMPORARY: patches the nadlan-platform-child header from the parent theme.
 *
 * UPress's Git deploy is only connected to this parent theme's path
 * (/wp-content/themes/nadlan-revenue/). The child theme is not Git-tracked
 * on this install, so edits to themes/nadlan-platform-child/ in the repo
 * never reach production. Until a second UPress Git connection exists for
 * the child theme, this enqueues a CSS override + a small JS-injected
 * hamburger menu from here instead, since the parent theme IS deployable.
 *
 * Safe to remove entirely once the child theme has its own working deploy
 * path and themes/nadlan-platform-child/assets/{css/platform.css,js/platform-nav.js}
 * are confirmed live on their own.
 */
add_action( 'wp_enqueue_scripts', function () {
	if ( is_admin() ) {
		return;
	}
	if ( get_stylesheet() !== 'nadlan-platform-child' ) {
		return;
	}
	$css = get_parent_theme_file_path( 'assets/css/nlpc-header-parent-override.css' );
	if ( file_exists( $css ) ) {
		wp_enqueue_style(
			'nlpc-header-parent-override',
			get_parent_theme_file_uri( 'assets/css/nlpc-header-parent-override.css' ),
			array( 'nlpc-platform' ),
			(string) filemtime( $css )
		);
	}
	$js = get_parent_theme_file_path( 'assets/js/nlpc-header-nav-inject.js' );
	if ( file_exists( $js ) ) {
		wp_enqueue_script(
			'nlpc-header-nav-inject',
			get_parent_theme_file_uri( 'assets/js/nlpc-header-nav-inject.js' ),
			array(),
			(string) filemtime( $js ),
			true
		);
	}
}, 70 );

// SEO: demote the site-title block from <h1> to <div> on non-front pages, so the
// page's own heading is the sole <h1> (fixes duplicate-H1 on project/tool/archive
// views). Front page keeps the site title as H1. From Codex's buyer-journey work.
add_filter( 'render_block_core/site-title', function ( $block_content, $block ) {
	if ( ! is_front_page() && ! is_home() ) {
		$block_content = preg_replace( '/^<h1/i', '<div', trim( $block_content ) );
		$block_content = preg_replace( '/<\/h1>$/i', '</div>', $block_content );
	}
	return $block_content;
}, 10, 2 );
