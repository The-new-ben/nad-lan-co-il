<?php
/**
 * nadlan-config — Showroom Engine bridge (Claude Design port).
 *
 * Mounts the data-driven showroom engine (assets/showroom-engine/) via a
 * project-agnostic shortcode. The engine renders ANY project from a payload built
 * from that project's CMS meta — the factory. New project = new nadlan_project post
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
			'viewbox'        => (string) get_post_meta( $id, 'project_3d_viewbox', true ),
			'model_glb'      => esc_url_raw( (string) get_post_meta( $id, 'project_model_glb', true ) ),
			'model_poster'   => esc_url_raw( (string) get_post_meta( $id, 'project_model_poster', true ) ),
			'facade_image'   => $facade,
			'concept'        => (bool) get_post_meta( $id, 'project_3d_demo', true ),
			'video_url'      => esc_url_raw( (string) get_post_meta( $id, 'project_3d_video_url', true ) ),
			'tour_url'       => esc_url_raw( (string) get_post_meta( $id, 'project_3d_tour_url', true ) ),
			'orientation'    => $orientation,
			'geo'            => array(
				'lat' => (float) get_post_meta( $id, 'lat', true ),
				'lng' => (float) get_post_meta( $id, 'lng', true ),
			),
			// monetization: paid tier lifts a project in gallery / map / nearby order.
			'featured'       => (bool) get_post_meta( $id, 'project_featured', true ),
			'tier'           => $tier,
			'url'            => get_permalink( $id ),
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
		wp_enqueue_style( 'nadlan-engine-tokens', $base . 'tokens.css', array(), '1.69.49' );
		wp_enqueue_style( 'nadlan-engine-css', $base . 'showroom.css', array( 'nadlan-engine-tokens' ), '1.69.49' );
		wp_enqueue_script( 'nadlan-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js', array(), '4.0.0', true );
		wp_script_add_data( 'nadlan-model-viewer', 'type', 'module' );
		wp_enqueue_script( 'nadlan-engine-i18n', $base . 'i18n.js', array(), '1.69.49', true );
		wp_enqueue_script( 'nadlan-engine-core', $base . 'engine.js', array( 'nadlan-engine-i18n' ), '1.69.49', true );

		// Real Mapbox only when a token is configured; otherwise the stylized map stays.
		if ( (string) get_option( 'nadlan_mapbox_token', '' ) !== '' ) {
			wp_enqueue_style( 'mapbox-gl', 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css', array(), '3.7.0' );
			wp_enqueue_script( 'mapbox-gl', 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js', array(), '3.7.0', true );
			wp_enqueue_script( 'nadlan-engine-mapbox', $base . 'mapbox-init.js', array( 'nadlan-engine-core', 'mapbox-gl' ), '1.69.49', true );
		}

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
				$payload = array(
					'config'   => nadlan_showroom_engine_config( $order[0] ),
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
 * model. When the developer's official BIM arrives, edit the field — done.
 * Runs once, guarded by an option.
 * ----------------------------------------------------------------------- */
add_action( 'init', function () {
	if ( get_option( 'nadlan_showroom_seed_ashira_v1' ) === '1' ) { return; }
	$glb = trailingslashit( nadlan_showroom_engine_base_url() ) . 'models/ashira-massing.glb';
	if ( ! file_exists( nadlan_showroom_engine_dir() . 'models/ashira-massing.glb' ) ) { return; }
	$slugs = array( 'ashira-sde-dov', 'ashira-sde-dov-en', 'ashira-sde-dov-fr', 'ashira-sde-dov-ru', 'ashira-sde-dov-ar' );
	foreach ( $slugs as $slug ) {
		$p = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
		if ( ! $p ) { continue; }
		if ( get_post_meta( $p->ID, 'project_model_glb', true ) === '' ) {
			update_post_meta( $p->ID, 'project_model_glb', esc_url_raw( $glb ) );
		}
	}
	update_option( 'nadlan_showroom_seed_ashira_v1', '1' );
} );

/* -------------------------------------------------------------------------
 * Slice 3 — safe per-project swap: render the NEW engine on a project page
 * instead of the OLD project-3d showroom. Default OFF, reversible. No stacking:
 * when active for a project, the old showroom disables itself (it is gated by
 * the nadlan_p3d_enabled filter), and the engine renders in its place.
 *
 * Turn it on per project:  set post meta  nlp3d_use_engine = 1
 * Turn it on site-wide:    set option     nadlan_showroom_engine_enable = 1
 * ----------------------------------------------------------------------- */

if ( ! function_exists( 'nadlan_showroom_engine_active_for' ) ) {
	function nadlan_showroom_engine_active_for( $post_id ) {
		if ( get_option( 'nadlan_showroom_engine_enable', '0' ) === '1' ) { return true; }
		if ( get_post_meta( (int) $post_id, 'nlp3d_use_engine', true ) === '1' ) { return true; }
		// Projects switched to the new engine by default (no manual setting needed).
		$default_on = apply_filters( 'nadlan_showroom_engine_default_on', array( 'ashira-sde-dov', 'ashira-sde-dov-en', 'ashira-sde-dov-fr', 'ashira-sde-dov-ru', 'ashira-sde-dov-ar' ) );
		$slug = get_post_field( 'post_name', (int) $post_id );
		return in_array( $slug, (array) $default_on, true );
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
	$engine = nadlan_showroom_engine_shortcode( array( 'page' => 'project', 'project' => '', 'id' => '' ) );
	return $engine . $content;
}, 8 );
