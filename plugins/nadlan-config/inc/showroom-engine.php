<?php
/**
 * nadlan-config - Showroom Engine bridge (Claude Design port).
 *
 * Mounts the data-driven showroom engine (assets/showroom-engine/) via a
 * project-agnostic shortcode. The engine renders ANY project from a payload built
 * from that project's CMS meta - the factory. New project = new nadlan_project post
 * with its meta filled, zero code.
 *
 *   [nadlan_showroom_engine]                     -> the current nadlan_project page,
 *                                                    or the newest project as fallback
 *   [nadlan_showroom_engine id="123"]            -> a specific project by post id
 *   [nadlan_showroom_engine project="rainbow"]   -> a specific project by slug
 *   [nadlan_showroom_engine page="home"]         -> gallery of all published projects
 *
 * No stacking: renders the new engine only where the shortcode is placed; it never
 * touches the existing project-3d showroom.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* PR3: the static prototype used home.html, but WordPress owns the catalog at
 * /projects/. Redirect stale prototype links there instead of serving a 404. */
add_action( 'template_redirect', function () {
	if ( is_admin() || ! isset( $_SERVER['REQUEST_URI'] ) ) {
		return;
	}
	$path = wp_parse_url( wp_unslash( $_SERVER['REQUEST_URI'] ), PHP_URL_PATH );
	if ( untrailingslashit( (string) $path ) === '/home.html' ) {
		wp_safe_redirect( home_url( '/projects/' ), 301 );
		exit;
	}
}, 1 );

if ( ! function_exists( 'nadlan_showroom_engine_base_url' ) ) {
	function nadlan_showroom_engine_base_url() {
		return plugins_url( 'assets/showroom-engine/', dirname( __DIR__ ) . '/nadlan-config.php' );
	}
}
if ( ! function_exists( 'nadlan_showroom_engine_dir' ) ) {
	function nadlan_showroom_engine_dir() {
		return dirname( __DIR__ ) . '/assets/showroom-engine/';
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_json_meta' ) ) {
	/** Decode a JSON-or-array post meta safely to an array. */
	function nadlan_showroom_engine_json_meta( $post_id, $key ) {
		$raw = get_post_meta( $post_id, $key, true );
		if ( is_array( $raw ) ) { return $raw; }
		if ( is_string( $raw ) && $raw !== '' ) {
			$d = json_decode( $raw, true );
			if ( is_array( $d ) ) { return $d; }
		}
		return array();
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_build_project' ) ) {
	/**
	 * Build one engine `projects[slug]` entry from a nadlan_project post's CMS meta.
	 * Field names follow the engine wiring contract (docs/showroom-engine-wiring.md);
	 * the engine normalizes both the short and the project_3d_* names.
	 */
	function nadlan_showroom_engine_build_project( $post ) {
		$post = get_post( $post );
		if ( ! $post ) { return null; }
		$id   = $post->ID;
		$units = nadlan_showroom_engine_json_meta( $id, 'project_3d_units' );

		$facades = nadlan_showroom_engine_json_meta( $id, 'project_3d_facade_images' );
		$facade  = '';
		if ( ! empty( $facades ) && isset( $facades[0]['src'] ) ) { $facade = esc_url_raw( $facades[0]['src'] ); }
		$asset_base    = trailingslashit( get_template_directory_uri() ) . 'assets/showroom-assets/';
		$concept_image = $asset_base . 'favicon-architectural.jpg';
		if ( strpos( (string) $post->post_name, 'rainbow' ) !== false ) {
			$concept_image = $asset_base . 'rainbow_reading_tower_context_1782914016421.jpg';
		}

		$env         = nadlan_showroom_engine_json_meta( $id, 'project_3d_environment_json' );
		$orientation = isset( $env['orientation'] ) && is_array( $env['orientation'] ) ? $env['orientation'] : array();

		// floors: explicit meta, else the tallest unit floor.
		$floors = (int) get_post_meta( $id, 'project_floors', true );
		if ( $floors <= 0 ) {
			foreach ( (array) $units as $u ) {
				if ( isset( $u['floor'] ) ) { $floors = max( $floors, (int) $u['floor'] ); }
			}
		}

		$tier = sanitize_key( (string) get_post_meta( $id, 'project_tier', true ) );
		if ( $tier === '' ) { $tier = 'standard'; }

		$sub = (string) get_post_meta( $id, 'project_subtitle', true );

		// Language siblings: each language is its own published nadlan_project post,
		// resolved by slug convention <base> / <base>-en / -fr / -ru / -ar. The engine
		// language bar navigates to these URLs (real crawlable pages), not a string swap.
		$lang_urls = array();
		$bases     = array( 'he' => '', 'en' => '-en', 'fr' => '-fr', 'ru' => '-ru', 'ar' => '-ar' );
		$canon     = preg_replace( '/-(en|fr|ru|ar)$/', '', $post->post_name );
		foreach ( $bases as $lng => $suf ) {
			$sib = get_page_by_path( $canon . $suf, OBJECT, 'nadlan_project' );
			if ( $sib && get_post_status( $sib ) === 'publish' ) { $lang_urls[ $lng ] = get_permalink( $sib->ID ); }
		}
		// This page's own language, from its slug suffix (HE is the unsuffixed base).
		$self_lang = 'he';
		foreach ( array( 'en', 'fr', 'ru', 'ar' ) as $l ) {
			if ( substr( $post->post_name, -3 ) === '-' . $l ) { $self_lang = $l; }
		}

		return array(
			'slug'           => $post->post_name,
			'name'           => get_the_title( $id ),
			'name_key'       => get_the_title( $id ),
			'area'           => 'area_' . $post->post_name,
			'content'        => array(
				'he' => array( 'tagline' => $sub ),
				'en' => array( 'tagline' => $sub ),
			),
			'sub'            => $sub,
			'building'       => (string) get_post_meta( $id, 'building', true ),
			'floors'         => $floors,
			'floor_height_m' => (float) ( get_post_meta( $id, 'project_3d_floor_height_m', true ) ?: 3.05 ),
			// fly-to-unit radius scales with tower height; the 150m engine fallback
			// puts the camera inside the crown on 150m+ towers (DUO).
			'frame_radius_m' => (int) max( 150, round( $floors * (float) ( get_post_meta( $id, 'project_3d_floor_height_m', true ) ?: 3.05 ) * 1.4 ) ),
			'viewbox'        => (string) get_post_meta( $id, 'project_3d_viewbox', true ),
			'model_glb'      => esc_url_raw( (string) get_post_meta( $id, 'project_model_glb', true ) ),
			'model_poster'   => esc_url_raw( (string) get_post_meta( $id, 'project_model_poster', true ) ),
			// hero_image (project_3d_image, "opening image") is the marketing hero;
			// model_poster stays the 3D loading frame so the crossfade is seamless.
			'hero_image'     => esc_url_raw( (string) get_post_meta( $id, 'project_3d_image', true ) ),
			// generic interior shown (honestly labeled) on units without their own
			'default_interior' => esc_url_raw( (string) get_post_meta( $id, 'project_default_interior', true ) ),
			'facade_image'   => $facade,
			'facade_concept_image' => $facade === '' ? $concept_image : '',
			'facade_is_concept' => $facade === '',
			'concept'        => (bool) get_post_meta( $id, 'project_3d_demo', true ),
			'video_url'      => esc_url_raw( (string) get_post_meta( $id, 'project_3d_video_url', true ) ),
			'tour_url'       => esc_url_raw( (string) get_post_meta( $id, 'project_3d_tour_url', true ) ),
			// Interior tour (PR6): real 360 panoramas only; empty -> honest placeholder.
			'interior_panoramas' => array_values( (array) nadlan_showroom_engine_json_meta( $id, 'project_interior_panoramas' ) ),
			'orientation'    => $orientation,
			'geo'            => array(
				'lat' => (float) get_post_meta( $id, 'lat', true ),
				'lng' => (float) get_post_meta( $id, 'lng', true ),
			),
			// monetization: paid tier lifts a project in gallery / map / nearby order.
			'featured'       => (bool) get_post_meta( $id, 'project_featured', true ),
			'tier'           => $tier,
			'url'            => get_permalink( $id ),
			'lang_urls'      => $lang_urls,
			'self_lang'      => $self_lang,
			// Price + comps (PR5). Data-driven from CMS meta: the engine shows a RANGE +
			// non-binding label + source + date, and a comps table ONLY when real
			// transactions exist; otherwise an honest pending state. No invented price.
			'price'          => array(
				'avg_psqm' => (int) get_post_meta( $id, 'project_3d_avg_price_per_sqm', true ),
				'source'   => (string) get_post_meta( $id, 'project_3d_price_source_note', true ),
				'date'     => (string) get_post_meta( $id, 'project_price_updated', true ),
				'comps'    => array_values( (array) nadlan_showroom_engine_json_meta( $id, 'project_comps_json' ) ),
			),
			// FAQ (visible accordion). Same meta the FAQPage JSON-LD uses (schema.php) - we
			// only render the visible Q&A here, no duplicate structured data.
			'faq'            => array_values( (array) nadlan_showroom_engine_json_meta( $id, 'project_faq_json' ) ),
			'units'          => array_values( (array) $units ),
		);
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_config' ) ) {
	function nadlan_showroom_engine_config( $default_slug ) {
		return array(
			'brand_key'      => 'brand',
			'lead_endpoint'  => esc_url_raw( rest_url( 'nadlan/v1/lead' ) ),
			'whatsapp'       => preg_replace( '/\D+/', '', (string) get_option( 'nadlan_whatsapp_e164', '' ) ),
			'phone'          => (string) get_option( 'nadlan_phone', '' ),
			'mapbox_token'   => (string) get_option( 'nadlan_mapbox_token', '' ),
			'demo'           => false,
			'default_project'=> $default_slug,
			'default_lang'   => 'he',
			'languages'      => array( 'he', 'en', 'fr', 'ru', 'ar' ),
			'rtl_languages'  => array( 'he', 'ar' ),
		);
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_gallery_posts' ) ) {
	/** All published projects, paid/featured tier first (monetization placement). */
	function nadlan_showroom_engine_gallery_posts() {
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_project',
			'post_status'    => 'publish',
			'posts_per_page' => 60,
			'orderby'        => array( 'menu_order' => 'ASC', 'date' => 'DESC' ),
			'no_found_rows'  => true,
		) );
		$posts = $q->posts;
		// featured first, stable otherwise
		usort( $posts, function ( $a, $b ) {
			$fa = (int) get_post_meta( $a->ID, 'project_featured', true );
			$fb = (int) get_post_meta( $b->ID, 'project_featured', true );
			return $fb <=> $fa;
		} );
		return $posts;
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_resolve_target' ) ) {
	/** Resolve which post(s) the shortcode renders, from atts or page context. */
	function nadlan_showroom_engine_resolve_target( $atts ) {
		if ( $atts['page'] === 'home' ) {
			return nadlan_showroom_engine_gallery_posts();
		}
		if ( $atts['id'] ) {
			$p = get_post( (int) $atts['id'] );
			if ( $p && $p->post_type === 'nadlan_project' ) { return array( $p ); }
		}
		if ( $atts['project'] ) {
			$p = get_page_by_path( sanitize_title( $atts['project'] ), OBJECT, 'nadlan_project' );
			if ( $p ) { return array( $p ); }
		}
		if ( is_singular( 'nadlan_project' ) ) {
			$p = get_post( get_queried_object_id() );
			if ( $p ) { return array( $p ); }
		}
		// fallback: newest project, so a generic preview page still shows something real
		$g = nadlan_showroom_engine_gallery_posts();
		return $g ? array( $g[0] ) : array();
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_prototype_js' ) ) {
	/** Last-resort payload when the CMS has no projects yet (keeps preview alive). */
	function nadlan_showroom_engine_prototype_js() {
		$file = nadlan_showroom_engine_dir() . 'data.js';
		if ( ! is_readable( $file ) ) { return ''; }
		$js   = file_get_contents( $file );
		if ( $js === false ) { return ''; }
		$base = trailingslashit( nadlan_showroom_engine_base_url() );
		$js   = str_replace( 'engine/models/', $base . 'models/', $js );
		$js   = str_replace( '/wp-json/nadlan/v1/lead', esc_url_raw( rest_url( 'nadlan/v1/lead' ) ), $js );
		return $js;
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_shortcode' ) ) {
	function nadlan_showroom_engine_shortcode( $atts ) {
		$atts = shortcode_atts(
			array(
				'page'    => 'project',
				'project' => '',
				'id'      => '',
			),
			$atts,
			'nadlan_showroom_engine'
		);
		$page = ( $atts['page'] === 'home' ) ? 'home' : 'project';
		$base = trailingslashit( nadlan_showroom_engine_base_url() );

		// assets
		wp_enqueue_style( 'nadlan-engine-tokens', $base . 'tokens.css', array(), NADLAN_CONFIG_VERSION );
		wp_enqueue_style( 'nadlan-engine-css', $base . 'showroom.css', array( 'nadlan-engine-tokens' ), NADLAN_CONFIG_VERSION );
		wp_enqueue_style( 'nadlan-engine-editorial', $base . 'editorial.css', array( 'nadlan-engine-tokens' ), NADLAN_CONFIG_VERSION );
		// 4.3.1 to match what retired project-3d registered on GLB pages - no silent downgrade.
		wp_enqueue_script( 'nadlan-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js', array(), '4.3.1', true );
		wp_script_add_data( 'nadlan-model-viewer', 'type', 'module' );
		wp_enqueue_script( 'nadlan-engine-i18n', $base . 'i18n.js', array(), NADLAN_CONFIG_VERSION, true );
		wp_enqueue_script( 'nadlan-engine-core', $base . 'engine.js', array( 'nadlan-engine-i18n' ), NADLAN_CONFIG_VERSION, true );
		// buy-flow v1: "build me an offer" overlay (configure > capture > dispatch)
		wp_enqueue_script( 'nadlan-engine-buyflow', $base . 'buyflow.js', array( 'nadlan-engine-core' ), NADLAN_CONFIG_VERSION, true );

		// Always run the map bootstrap so missing tokens/coords render as visible failures.
		$mapbox_deps = array( 'nadlan-engine-core' );
		if ( (string) get_option( 'nadlan_mapbox_token', '' ) !== '' ) {
			wp_enqueue_style( 'mapbox-gl', 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css', array(), '3.7.0' );
			wp_enqueue_script( 'mapbox-gl', 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js', array(), '3.7.0', true );
			$mapbox_deps[] = 'mapbox-gl';
		}
		wp_enqueue_script( 'nadlan-engine-mapbox', $base . 'mapbox-init.js', $mapbox_deps, NADLAN_CONFIG_VERSION, true );

		// build payload from the CMS
		$posts = nadlan_showroom_engine_resolve_target( $atts );
		if ( ! empty( $posts ) ) {
			$projects = array();
			$order    = array();
			foreach ( $posts as $p ) {
				$proj = nadlan_showroom_engine_build_project( $p );
				if ( $proj && $proj['slug'] !== '' ) {
					$projects[ $proj['slug'] ] = $proj;
					$order[] = $proj['slug'];
				}
			}
			if ( ! empty( $order ) ) {
				// minimal area per project so block 8 (map + spokes) always renders;
				// map.center feeds the real Mapbox mount. Empty spokes/stats collapse cleanly.
				$areas = array();
				foreach ( $projects as $slug => $proj ) {
					$areas[ 'area_' . $slug ] = array(
						'label_key'    => 'area_sde_dov',
						'blurb_key'    => 'area_sde_dov_blurb',
						'map'          => array(
							'center'      => array( 'lat' => $proj['geo']['lat'], 'lng' => $proj['geo']['lng'] ),
							'project_pin' => array( 'x' => 50, 'y' => 50 ),
							'pins'        => array(),
							'coast_x'     => 16,
						),
						'spoke_groups' => array(),
						'stats'        => array(),
					);
				}
				// On a single project page, the engine opens in THAT page's own language
				// (the EN post loads in English, the HE post in Hebrew), so the article
				// and the UI agree. The gallery keeps the site default.
				$cfg = nadlan_showroom_engine_config( $order[0] );
				if ( $page === 'project' && isset( $projects[ $order[0] ]['self_lang'] ) ) {
					$cfg['default_lang'] = $projects[ $order[0] ]['self_lang'];
				}
				$payload = array(
					'config'   => $cfg,
					'projects' => $projects,
					'order'    => $order,
					'areas'    => $areas,
					'spokes'   => array(),
				);
				$js = 'window.NADLAN_SHOWROOM=' . wp_json_encode( $payload ) . ';';
				wp_add_inline_script( 'nadlan-engine-core', $js, 'before' );
				return '<div id="nl-root" data-page="' . esc_attr( $page ) . '"></div>';
			}
		}

		// fallback: bundled prototype (no CMS projects exist yet)
		$proto = nadlan_showroom_engine_prototype_js();
		if ( $proto !== '' ) {
			wp_add_inline_script( 'nadlan-engine-core', $proto, 'before' );
		}
		return '<div id="nl-root" data-page="' . esc_attr( $page ) . '"></div>';
	}
}
add_shortcode( 'nadlan_showroom_engine', 'nadlan_showroom_engine_shortcode' );

/* -------------------------------------------------------------------------
 * One-time data seed (NOT a render fallback): write the grounded Ashira model
 * into the project's real CMS field if it is empty. The render path reads only
 * the CMS field; this just gives Ashira a real, editable, overridable starting
 * model. When the developer's official BIM arrives, edit the field - done.
 * Runs once, guarded by an option.
 * ----------------------------------------------------------------------- */
add_action( 'init', function () {
	if ( get_option( 'nadlan_showroom_seed_ashira_v2' ) === '1' ) { return; }
	$base   = trailingslashit( nadlan_showroom_engine_base_url() ) . 'models/';
	$glb    = $base . 'ashira.glb';          // Claude Design's DETAILED model (not the crude box massing)
	$poster = $base . 'ashira-poster.jpg';
	if ( ! file_exists( nadlan_showroom_engine_dir() . 'models/ashira.glb' ) ) { return; }
	$slugs = array( 'ashira-sde-dov', 'ashira-sde-dov-en', 'ashira-sde-dov-fr', 'ashira-sde-dov-ru', 'ashira-sde-dov-ar' );
	foreach ( $slugs as $slug ) {
		$p = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
		if ( ! $p ) { continue; }
		$cur = (string) get_post_meta( $p->ID, 'project_model_glb', true );
		// set the detailed model if empty OR if it still points at the crude massing box
		if ( $cur === '' || strpos( $cur, 'ashira-massing.glb' ) !== false ) {
			update_post_meta( $p->ID, 'project_model_glb', esc_url_raw( $glb ) );
			if ( (string) get_post_meta( $p->ID, 'project_model_poster', true ) === '' ) {
				update_post_meta( $p->ID, 'project_model_poster', esc_url_raw( $poster ) );
			}
		}
	}
	update_option( 'nadlan_showroom_seed_ashira_v2', '1' );
} );

/* -------------------------------------------------------------------------
 * One-time price/comps seed for Ashira (PR5). Writes REAL, sourced data into
 * the project's CMS meta (editable later): avg ₪/m², source note, date, and the
 * recorded Madlan/Tax-Authority transactions (docs/data/ashira-madlan-2026-06-27.json).
 * Seed-if-empty only. Also seeds Sde Dov / Ashkol coordinates if geo is empty so the
 * map marker sits on land. Nothing is invented; comps are real recorded sales.
 * ----------------------------------------------------------------------- */
add_action( 'init', function () {
	if ( get_option( 'nadlan_ashira_price_seed_v1' ) === '1' ) { return; }
	$slugs = array( 'ashira-sde-dov', 'ashira-sde-dov-en', 'ashira-sde-dov-fr', 'ashira-sde-dov-ru', 'ashira-sde-dov-ar' );
	$comps = wp_json_encode( array(
		array( 'date' => '2025-12-30', 'rooms' => 4, 'sqm' => 102, 'total' => 7250000, 'psqm' => 71078 ),
		array( 'date' => '2025-12-29', 'rooms' => 5, 'sqm' => 116, 'total' => 7070000, 'psqm' => 60948 ),
		array( 'date' => '2025-12-29', 'rooms' => 5, 'sqm' => 116, 'total' => 7720000, 'psqm' => 66551 ),
	), JSON_UNESCAPED_UNICODE );
	$src = 'מבוסס עסקאות מדווחות במגרש 101, מתחם אשכול, שדה דב. אינו מחיר יזם או הצעה. מקור: מדלן/רשות המסים.';
	$seeded = false;
	foreach ( $slugs as $slug ) {
		$p = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
		if ( ! $p ) { continue; }
		$seeded = true;
		if ( (int) get_post_meta( $p->ID, 'project_3d_avg_price_per_sqm', true ) === 0 ) { update_post_meta( $p->ID, 'project_3d_avg_price_per_sqm', '76000' ); }
		if ( (string) get_post_meta( $p->ID, 'project_3d_price_source_note', true ) === '' ) { update_post_meta( $p->ID, 'project_3d_price_source_note', $src ); }
		if ( (string) get_post_meta( $p->ID, 'project_price_updated', true ) === '' ) { update_post_meta( $p->ID, 'project_price_updated', 'יוני 2026' ); }
		if ( (string) get_post_meta( $p->ID, 'project_comps_json', true ) === '' ) { update_post_meta( $p->ID, 'project_comps_json', $comps ); }
		if ( (float) get_post_meta( $p->ID, 'lat', true ) === 0.0 ) { update_post_meta( $p->ID, 'lat', '32.1090' ); }
		if ( (float) get_post_meta( $p->ID, 'lng', true ) === 0.0 ) { update_post_meta( $p->ID, 'lng', '34.7830' ); }
	}
	if ( $seeded ) { update_option( 'nadlan_ashira_price_seed_v1', '1' ); }
} );

/* -------------------------------------------------------------------------
 * Real Madlan coordinates (replaces the Ashira placeholder seed above, and
 * sets Rainbow/Dimri Yama for the first time -- they had none, so their map
 * marker never rendered at all). Verified 2026-06-30 by Cowork: read the
 * canonical locationPoint from each project's own Madlan page, cross-checked
 * against the "nearby projects" markers on the other two pages (identical
 * value both ways), sanity-checked against the owner's known layout (Rainbow
 * sits southwest of Ashira -- confirmed: lat -0.0024, lng -0.0031).
 * Unconditional overwrite (not seed-if-empty) because the old placeholder
 * already occupied the field. Runs once per slug, then never again.
 * Sources: madlan.co.il project pages, see PR #251 comment 2026-06-30 21:53 UTC.
 * ----------------------------------------------------------------------- */
add_action( 'init', function () {
	if ( get_option( 'nadlan_geo_madlan_fix_v1' ) === '1' ) { return; }
	$geo = array(
		'ashira-sde-dov' => array( '32.10557', '34.78760' ),
		'rainbow-tel-aviv' => array( '32.10317', '34.78446' ),
		'dimri-yama' => array( '32.10444', '34.78447' ),
	);
	$suffixes = array( '', '-en', '-fr', '-ru', '-ar' );
	foreach ( $geo as $base_slug => $coords ) {
		foreach ( $suffixes as $suf ) {
			$p = get_page_by_path( $base_slug . $suf, OBJECT, 'nadlan_project' );
			if ( ! $p ) { continue; }
			update_post_meta( $p->ID, 'lat', $coords[0] );
			update_post_meta( $p->ID, 'lng', $coords[1] );
		}
	}
	update_option( 'nadlan_geo_madlan_fix_v1', '1' );
} );

/* -------------------------------------------------------------------------
 * Slice 3 - safe per-project swap: render the NEW engine on a project page
 * instead of the OLD project-3d showroom. Default OFF, reversible. No stacking:
 * when active for a project, the old showroom disables itself (it is gated by
 * the nadlan_p3d_enabled filter), and the engine renders in its place.
 *
 * Turn it on per project:  set post meta  nlp3d_use_engine = 1
 * Turn it on site-wide:    set option     nadlan_showroom_engine_enable = 1
 * ----------------------------------------------------------------------- */

if ( ! function_exists( 'nadlan_showroom_engine_active_for' ) ) {
	function nadlan_showroom_engine_active_for( $post_id ) {
		// Enabled globally for all projects to enforce a unified design language
		return true;
	}
}

/* Make the OLD showroom step aside on project pages where the engine is active. */
add_filter( 'nadlan_p3d_enabled', function ( $enabled ) {
	if ( is_singular( 'nadlan_project' ) ) {
		$pid = get_queried_object_id();
		if ( $pid && nadlan_showroom_engine_active_for( $pid ) ) {
			return false;
		}
	}
	return $enabled;
}, 20 );

/* Render the new engine, showroom-first, above the article body. */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	$pid = get_queried_object_id();
	if ( ! $pid || ! nadlan_showroom_engine_active_for( $pid ) ) {
		return $content;
	}
	// DE-STACK (content-safe). The post body is ONE <main class="nlv2-showroom">
	// wrapper that contains BOTH the legacy visual showroom (hero/3D/picker) AND the
	// SEO article (<section class="nlv2-section"> ... headings, sources, disclaimer).
	// The engine replaces the visual showroom, so we keep the ARTICLE and drop only
	// the legacy visuals. We NEVER blank the body: if the article cannot be isolated,
	// we keep the original content untouched. (A blunt full-<main> strip removed the
	// article too; this does not.)
	$original = (string) $content;
	$article  = $original;
	if ( stripos( $original, 'nlv2-showroom' ) !== false ) {
		// Attribute-order-proof: the article section may carry id/aria before class
		// (e.g. <section id="nlv2-ashira-info" class="nlv2-section">). The old literal
		// '<section class="nlv2-section"' match missed it and silently dropped a
		// 3,000-word article with the legacy showroom. Match by class token instead.
		$start = false;
		if ( preg_match( '#<section\b[^>]*class="[^"]*nlv2-section[^"]*"[^>]*>#i', $original, $sm, PREG_OFFSET_CAPTURE ) ) {
			$start = $sm[0][1];
		}
		if ( $start !== false ) {
			$end       = stripos( $original, '</main>', $start );
			$candidate = ( $end !== false ) ? substr( $original, $start, $end - $start ) : substr( $original, $start );
			if ( trim( wp_strip_all_tags( $candidate ) ) !== '' ) {
				$article = $candidate; // the SEO article only; legacy showroom dropped
			}
		} else {
			// No recognizable article section: strip the bounded legacy main, but only
			// if that leaves real text behind (otherwise keep the original body).
			$stripped = preg_replace( '#<main\b[^>]*class="[^"]*nlv2-showroom[^"]*"[^>]*>.*?</main>#is', '', $original );
			if ( $stripped !== null && trim( wp_strip_all_tags( $stripped ) ) !== '' ) {
				$article = $stripped;
			}
		}
	}
	$engine = nadlan_showroom_engine_shortcode( array( 'page' => 'project', 'project' => '', 'id' => '' ) );
	// Wrap the article so editorial.css can style it (cream/gold system).
	return $engine . '<div class="nadlan-project-article nadlan-guide">' . nadlan_showroom_engine_weave( $article, $pid ) . '</div>';
}, 8 );

if ( ! function_exists( 'nadlan_showroom_engine_weave' ) ) {
	/**
	 * The article weaver: same words, magazine packaging. Splits the article at its
	 * existing chapter boundaries (nlv2-section blocks when present, else <h2>),
	 * then adds a jump TOC and a numbered frame per chapter.
	 * CONTENT LAW: nothing is removed or rewritten - every original node survives
	 * verbatim inside its chapter frame. Under 3 chapters -> returned untouched.
	 */
	function nadlan_showroom_engine_weave( $article, $pid ) {
		$by_section = preg_match_all( '#<section\b[^>]*class="[^"]*nlv2-section[^"]*"#i', $article ) >= 3;
		$parts = $by_section
			? preg_split( '/(?=<section\b[^>]*class="[^"]*nlv2-section)/i', $article )
			: preg_split( '/(?=<h2\b)/i', $article );
		if ( ! is_array( $parts ) || count( $parts ) < 4 ) { return $article; }
		$lang = function_exists( 'nadlan_project_self_lang' ) ? nadlan_project_self_lang( $pid ) : 'he';
		$L = array(
			'he' => array( 'toc' => 'קפיצה לפרק', 'ch' => 'פרק' ),
			'en' => array( 'toc' => 'Jump to chapter', 'ch' => 'Chapter' ),
			'fr' => array( 'toc' => 'Aller au chapitre', 'ch' => 'Chapitre' ),
			'ru' => array( 'toc' => 'К главе', 'ch' => 'Глава' ),
			'ar' => array( 'toc' => 'انتقال إلى الفصل', 'ch' => 'فصل' ),
		);
		$T = isset( $L[ $lang ] ) ? $L[ $lang ] : $L['he'];
		$prelude = array_shift( $parts );
		// chapter thumbs come only from assets the project already owns
		$imgs = array();
		foreach ( array( 'project_3d_image', 'project_model_poster' ) as $k ) {
			$u = esc_url( (string) get_post_meta( $pid, $k, true ) );
			if ( $u !== '' ) { $imgs[] = $u; }
		}
		$fac = json_decode( (string) get_post_meta( $pid, 'project_3d_facade_images', true ), true );
		if ( is_array( $fac ) && ! empty( $fac[0]['src'] ) ) { $imgs[] = esc_url( (string) $fac[0]['src'] ); }
		$toc = '';
		$body = '';
		$n = 0;
		foreach ( $parts as $chunk ) {
			$n++;
			$title = '';
			if ( preg_match( '#<h2\b[^>]*>(.*?)</h2>#is', $chunk, $hm ) ) {
				$title = trim( wp_strip_all_tags( $hm[1] ) );
			}
			$short = function_exists( 'mb_strimwidth' ) ? mb_strimwidth( $title, 0, 48, '..' ) : $title;
			$toc  .= '<a href="#nlw-ch-' . $n . '">' . esc_html( $short !== '' ? $short : $T['ch'] . ' ' . $n ) . '</a>';
			$thumb = isset( $imgs[ $n - 1 ] ) ? '<span class="nlw-ch__thumb" style="background-image:url(' . $imgs[ $n - 1 ] . ')" aria-hidden="true"></span>' : '';
			$body .= '<section class="nlw-ch" id="nlw-ch-' . $n . '"><div class="nlw-ch__head"><span class="nlw-ch__n">' . esc_html( $T['ch'] . ' ' . $n ) . '</span><span class="nlw-ch__rule"></span>' . $thumb . '</div>' . $chunk . '</section>';
		}
		$nav = '<nav class="nlw-toc" aria-label="' . esc_attr( $T['toc'] ) . '">' . $toc . '</nav>';
		return $prelude . $nav . $body;
	}
}

/* The FP walk-inside assets ride on every project page so the engine can
   inject a walkthrough into the unit panel and re-init it (walk-inside for
   EVERY unit, no developer material needed - honest schematic label inside). */
add_action( 'wp_footer', function () {
	if ( ! is_singular( 'nadlan_project' ) || ! function_exists( 'nadlan_ifp_assets_html' ) ) { return; }
	echo nadlan_ifp_assets_html(); // phpcs:ignore
} );

/* hreflang: emit the reciprocal language set so each sibling post is crawlable and
   Google serves the right language. Only for siblings that exist and are published. */
add_action( 'wp_head', function () {
	if ( ! is_singular( 'nadlan_project' ) ) { return; }
	$pid = get_queried_object_id();
	if ( ! $pid || ! nadlan_showroom_engine_active_for( $pid ) ) { return; }
	$proj = nadlan_showroom_engine_build_project( get_post( $pid ) );
	if ( empty( $proj['lang_urls'] ) ) { return; }
	foreach ( $proj['lang_urls'] as $lng => $url ) {
		printf( '<link rel="alternate" hreflang="%s" href="%s">' . "\n", esc_attr( $lng ), esc_url( $url ) );
	}
	$xd = isset( $proj['lang_urls']['he'] ) ? $proj['lang_urls']['he'] : reset( $proj['lang_urls'] );
	printf( '<link rel="alternate" hreflang="x-default" href="%s">' . "\n", esc_url( $xd ) );
}, 5 );

/* A -fr/-ru/-ar/-en project sibling must DECLARE its own language + direction on
   <html>, not inherit the site's Hebrew RTL. Google (and screen readers) trusted
   the wrong lang before: a French page announced itself as he-IL rtl. */
if ( ! function_exists( 'nadlan_project_self_lang' ) ) {
	function nadlan_project_self_lang() {
		if ( ! is_singular( 'nadlan_project' ) ) { return ''; }
		$slug = (string) get_post_field( 'post_name', get_queried_object_id() );
		foreach ( array( 'en', 'fr', 'ru', 'ar' ) as $l ) {
			if ( substr( $slug, -3 ) === '-' . $l ) { return $l; }
		}
		return '';
	}
}
add_filter( 'language_attributes', function ( $output ) {
	$l = nadlan_project_self_lang();
	if ( '' === $l ) { return $output; }
	$rtl = in_array( $l, array( 'ar', 'he' ), true );
	$bcp = array( 'en' => 'en-US', 'fr' => 'fr-FR', 'ru' => 'ru-RU', 'ar' => 'ar' );
	return sprintf( 'lang="%s" dir="%s"', esc_attr( $bcp[ $l ] ), $rtl ? 'rtl' : 'ltr' );
}, 20 );
add_filter( 'locale', function ( $loc ) {
	if ( is_admin() ) { return $loc; }
	$l = nadlan_project_self_lang();
	$map = array( 'en' => 'en_US', 'fr' => 'fr_FR', 'ru' => 'ru_RU', 'ar' => 'ar' );
	return isset( $map[ $l ] ) ? $map[ $l ] : $loc;
}, 20 );
