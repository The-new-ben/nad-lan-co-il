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
	}
endif;
add_action( 'wp_enqueue_scripts', 'nadlan_revenue_enqueue_styles' );

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
		$projects       = nadlan_revenue_premium_projects();
		$pros           = nadlan_revenue_premium_professionals();

		ob_start();
		?>
<div class="nlux-home" dir="rtl">
	<section class="nlux-hero" aria-label="נדל״ן חכם">
		<div class="nlux-hero-media" aria-hidden="true"></div>
		<div class="nlux-hero-copy">
			<p class="nlux-kicker">נדל״ן חכם · ישראל</p>
			<h1>הדרך היוקרתית לבדוק, להשוות ולהתקדם בעסקת נדל״ן</h1>
			<p class="nlux-lead">פרויקטים חדשים, אנשי מקצוע רשומים, מדריכים וכלים במקום אחד. חוויה נקייה, ויזואלית ומבוססת נתונים, בלי רעש של לוח מודעות.</p>
			<form class="nlux-search" method="get" action="<?php echo esc_url( $project_url ); ?>">
				<input type="search" name="q" placeholder="חפשו פרויקט, עיר, יזם או בעל מקצוע">
				<input type="text" name="city" placeholder="עיר">
				<button type="submit">חיפוש</button>
			</form>
			<div class="nlux-actions">
				<a href="<?php echo esc_url( $project_url ); ?>">פרויקטים חדשים</a>
				<a href="<?php echo esc_url( $pro_url ); ?>">אנשי מקצוע</a>
				<a href="<?php echo esc_url( $join_url ); ?>">פרסום פרימיום</a>
			</div>
		</div>
		<div class="nlux-hero-panel" aria-label="נתוני המאגר">
			<div><b><?php echo number_format_i18n( $projects_count ); ?></b><span>פרויקטים</span></div>
			<div><b><?php echo number_format_i18n( $pros_count ); ?></b><span>בעלי מקצוע</span></div>
			<div><b><?php echo number_format_i18n( $terms_count ); ?></b><span>מונחים ומדריכים</span></div>
		</div>
	</section>

	<section class="nlux-paths" aria-label="מסלולי פעולה">
		<a class="nlux-path" href="<?php echo esc_url( $project_url ); ?>"><span>01</span><h2>מחפשים פרויקט</h2><p>ראו פרויקטים חדשים והתחדשות עירונית עם עיר, יזם, סטטוס ותמונות.</p></a>
		<a class="nlux-path" href="<?php echo esc_url( $pro_url ); ?>"><span>02</span><h2>בודקים אנשי מקצוע</h2><p>קבלנים, שמאים, עורכי דין ויועצים עם מקור רשמי ופרטי קשר מסודרים.</p></a>
		<a class="nlux-path" href="<?php echo esc_url( nadlan_revenue_page_url( 'mortgage-calculator', '/mortgage-calculator/' ) ); ?>"><span>03</span><h2>מחשבים עלויות</h2><p>משכנתא, מס רכישה, עלויות עסקה והשוואות לפני החלטה.</p></a>
		<a class="nlux-path" href="<?php echo esc_url( $join_url ); ?>"><span>04</span><h2>מפרסמים נכס או פרויקט</h2><p>חשיפה נקייה ומכובדת לפרויקטים, נכסים ואנשי מקצוע שרוצים להיראות רציני.</p></a>
	</section>

	<section class="nlux-showcase" aria-label="פרויקטים נבחרים">
		<div class="nlux-section-head">
			<p class="nlux-kicker">תצוגת פרויקטים</p>
			<h2>כרטיסים חיים מתוך המאגר, עם תמונה במקום ריק</h2>
			<a href="<?php echo esc_url( $project_url ); ?>">לכל הפרויקטים</a>
		</div>
		<div class="nlux-project-grid">
			<?php foreach ( $projects as $i => $id ) :
				$city   = trim( (string) get_post_meta( $id, 'city', true ) );
				$status = trim( (string) get_post_meta( $id, 'project_status', true ) );
				$dev    = trim( (string) get_post_meta( $id, 'developer_name', true ) );
				$units  = trim( (string) get_post_meta( $id, 'num_units', true ) );
				$img    = nadlan_revenue_card_media( $id, $i % 2 ? 'tel-aviv-coast-skyline.jpg' : 'architectural-model.jpg' );
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

	<section class="nlux-data-band" aria-label="אמון ונתונים">
		<div><strong>data.gov.il</strong><span>מקורות רשמיים כשאפשר</span></div>
		<div><strong>מאגר חי</strong><span>כרטיסים, פרויקטים, מדריכים וכלים</span></div>
		<div><strong>פרימיום</strong><span>תמונה, היררכיה, טיפוגרפיה ותנועה שקטה</span></div>
	</section>

	<section class="nlux-tools" aria-label="כלים ומדריכים">
		<div class="nlux-section-head">
			<p class="nlux-kicker">לפני חתימה</p>
			<h2>כלים שמרגישים כמו מערכת, לא כמו תבנית</h2>
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
			<p class="nlux-kicker">מאגר מקצועי</p>
			<h2>בעלי מקצוע שמופיעים מתוך המערכת</h2>
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
			<p class="nlux-kicker">נראות שמוכרת אמון</p>
			<h2>יש לכם פרויקט, נכס או כרטיס מקצועי?</h2>
			<p>המערכת צריכה לעזור לכם להיראות כמו גוף רציני: תמונות, טקסט, מפה, חשיפה ומעקב במקום אחד.</p>
		</div>
		<div class="nlux-actions">
			<a href="<?php echo esc_url( $join_url ); ?>">מסלולי פרסום</a>
			<a href="<?php echo esc_url( $studio_url ); ?>">פתיחת סטודיו</a>
		</div>
	</section>
</div>
		<?php
		return ob_get_clean();
	}
endif;

add_filter( 'the_content', function ( $content ) {
	if ( is_front_page() && in_the_loop() && is_main_query() ) {
		return nadlan_revenue_premium_front_page();
	}
	return $content;
}, 3 );

add_filter( 'render_block', function ( $block_content, $block ) {
	if ( is_front_page() && isset( $block['blockName'] ) && $block['blockName'] === 'core/post-title' ) {
		return '';
	}
	return $block_content;
}, 9, 2 );
