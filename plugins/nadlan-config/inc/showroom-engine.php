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

if ( ! function_exists( 'nadlan_unit_journey_is_v2_render' ) ) {
	/** Rendering feature flag. This says nothing about public visibility. */
	function nadlan_unit_journey_is_v2_render( $post_id = 0 ) {
		$post_id = (int) $post_id;
		if ( $post_id <= 0 && function_exists( 'get_queried_object_id' ) ) {
			$post_id = (int) get_queried_object_id();
		}
		return $post_id > 0
			&& 'nadlan_project' === get_post_type( $post_id )
			&& 'on' === (string) get_post_meta( $post_id, 'nl_unit_scene_v2', true );
	}
}

if ( ! function_exists( 'nadlan_unit_journey_is_private_lab' ) ) {
	/**
	 * Dedicated privacy marker, independent from the v2 rendering flag. The
	 * marker remains fail-closed even if the post password is removed by
	 * mistake, so losing one defence cannot silently restore discovery.
	 */
	function nadlan_unit_journey_is_private_lab( $post_id = 0 ) {
		$post_id = (int) $post_id;
		if ( $post_id <= 0 && function_exists( 'get_queried_object_id' ) ) {
			$post_id = (int) get_queried_object_id();
		}
		return $post_id > 0
			&& 'nadlan_project' === get_post_type( $post_id )
			&& (
				'private-unit-journey-v2' === (string) get_post_meta( $post_id, '_nadlan_private_unit_journey', true )
				|| ( function_exists( 'nadlan_flagship_v3_is_private_candidate' ) && nadlan_flagship_v3_is_private_candidate( $post_id ) )
			);
	}
}

if ( ! function_exists( 'nadlan_unit_journey_private_lab_has_password' ) ) {
	/** The dedicated marker is valid for front-end access only with core's password gate. */
	function nadlan_unit_journey_private_lab_has_password( $post_id ) {
		$post_id = (int) $post_id;
		$post    = $post_id ? get_post( $post_id ) : null;
		return $post instanceof WP_Post
			&& nadlan_unit_journey_is_private_lab( $post_id )
			&& '' !== (string) $post->post_password;
	}
}

if ( ! function_exists( 'nadlan_unit_journey_private_project_ids' ) ) {
	/** Published private-lab IDs for sitemap/count guards; never a public list. */
	function nadlan_unit_journey_private_project_ids() {
		static $ids = null;
		if ( is_array( $ids ) ) {
			return $ids;
		}
		$ids = get_posts( array(
			'post_type'                         => 'nadlan_project',
			'post_status'                       => 'publish',
			'posts_per_page'                    => -1,
			'fields'                            => 'ids',
			'meta_key'                          => '_nadlan_private_unit_journey',
			'meta_value'                        => 'private-unit-journey-v2',
			'no_found_rows'                     => true,
			'nadlan_include_private_unit_journey' => true,
		) );
		if ( function_exists( 'nadlan_flagship_v3_registry' ) ) {
			foreach ( (array) nadlan_flagship_v3_registry()['contracts'] as $contract ) {
				$sandbox = is_array( $contract ) && isset( $contract['sandbox'] ) && is_array( $contract['sandbox'] )
					? $contract['sandbox']
					: array();
				$slug = empty( $contract['public_release_enabled'] ) && isset( $sandbox['exact_slug'] )
					? (string) $sandbox['exact_slug']
					: '';
				$post = '' !== $slug ? get_page_by_path( $slug, OBJECT, 'nadlan_project' ) : null;
				if ( $post instanceof WP_Post && 'publish' === (string) $post->post_status && '' !== (string) $post->post_password ) {
					$ids[] = (int) $post->ID;
				}
			}
		}
		$ids = array_values( array_unique( array_map( 'intval', (array) $ids ) ) );
		return $ids;
	}
}

if ( ! function_exists( 'nadlan_unit_journey_public_project_count' ) ) {
	/** Public aggregate count without revealing the private lab in home chrome. */
	function nadlan_unit_journey_public_project_count() {
		$counts = wp_count_posts( 'nadlan_project' );
		$total  = isset( $counts->publish ) ? (int) $counts->publish : 0;
		return max( 0, $total - count( nadlan_unit_journey_private_project_ids() ) );
	}
}

if ( ! function_exists( 'nadlan_unit_journey_can_manage_private_labs' ) ) {
	/** Editors/admins may inspect the private object; subscribers may not. */
	function nadlan_unit_journey_can_manage_private_labs() {
		if ( ! is_user_logged_in() ) {
			return false;
		}
		if ( current_user_can( 'manage_options' ) ) {
			return true;
		}
		foreach ( nadlan_unit_journey_private_project_ids() as $post_id ) {
			if ( current_user_can( 'edit_post', $post_id ) ) {
				return true;
			}
		}
		return false;
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
		$project_name = get_the_title( $id );
		if ( nadlan_unit_journey_is_private_lab( $id ) ) {
			$private_source_name = sanitize_text_field( (string) get_post_meta( $id, '_nadlan_private_unit_journey_project_name', true ) );
			if ( '' !== $private_source_name ) {
				$project_name = $private_source_name;
			}
		}

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
			'wp_id'          => (int) $id,
			'name'           => $project_name,
			'name_key'       => $project_name,
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
			// DEFAULT MODEL (owner 2026-07-11): a project with no model of its
			// own shows the STANDARD Israeli street building - a form
			// developers recognize as "could be my project" - honestly labeled
			// as a general illustration, never as the building. It conforms to
			// the engine hotspot formula (26.4m at origin, floors from y=0,
			// fh 3.05) so generic projects get working facade hotspots free.
			'model_glb'      => ( function () use ( $id ) {
				$own = esc_url_raw( (string) get_post_meta( $id, 'project_model_glb', true ) );
				return $own !== '' ? $own : nadlan_showroom_engine_base_url() . 'models/standard-residential.glb';
			} )(),
			'model_generic'  => get_post_meta( $id, 'project_model_glb', true ) === '',
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
			// The DEFAULT walk (owner law: a default, not a fallback): the standard
			// apartment + building set from media (standard-default-*), shown on every
			// project until the developer's dedicated tour replaces it.
			'default_tour'   => nadlan_showroom_default_tour_for( $id ),
			'default_tour_tier' => nadlan_showroom_default_tour_tier( $id ),
			'project_walk'   => nadlan_showroom_project_walk( $id, $post->post_name ),
			'orientation'    => $orientation,
			'geo'            => array(
				'lat' => (float) get_post_meta( $id, 'lat', true ),
				'lng' => (float) get_post_meta( $id, 'lng', true ),
				// city-centroid coordinates (bulk geocode) are honest for the map
				// but NOT for a per-apartment window view - the engine gates on this.
				'confidence' => (string) get_post_meta( $id, 'geo_confidence', true ),
			),
			// Hero truth (audit + owner 2026-08-13): the eyebrow was a hardcoded
			// "רובע שדה דב" on EVERY project. Per-project meta wins, the true
			// city is the fallback; the i18n default remains only when both
			// are empty. units_total feeds an honest homes figure when no
			// unit is actually marked available.
			'hero_eyebrow'   => ( (string) get_post_meta( $id, 'project_hero_eyebrow', true ) )
				?: (string) get_post_meta( $id, 'city', true ),
			// boot camera (SIX-8 v2): the stage markup honors default_orbit /
			// default_target when present; empty meta keeps engine defaults.
			'default_orbit'  => (string) get_post_meta( $id, 'project_3d_default_orbit', true ),
			'default_target' => (string) get_post_meta( $id, 'project_3d_default_target', true ),
			'units_total'    => (int) get_post_meta( $id, 'num_units', true ),
			// Beam v2: named public landmarks (sea, rail, park...) with real
			// coordinates from meta project_env_landmarks. The engine computes
			// true bearings + aerial distances so the window beam answers "what
			// do I actually face" instead of a bare compass word. Never invented:
			// empty meta means no landmark ring.
			'landmarks'      => nadlan_showroom_engine_landmarks( $id ),
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
			// Gallery (engine media block reads p.gallery as plain URLs). Meta
			// project_gallery_json: ["url", ...] or [{"src":"url"}, ...]. Real
			// media only - empty meta renders nothing.
			'gallery'        => ( function () use ( $id ) {
				$out = array();
				foreach ( array_slice( (array) nadlan_showroom_engine_json_meta( $id, 'project_gallery_json' ), 0, 24 ) as $g ) {
					$u = is_array( $g ) ? (string) ( $g['src'] ?? '' ) : (string) $g;
					$u = esc_url_raw( $u );
					if ( $u !== '' ) { $out[] = $u; }
				}
				return $out;
			} )(),
			// FAQ (visible accordion). Same meta the FAQPage JSON-LD uses (schema.php) - we
			// only render the visible Q&A here, no duplicate structured data.
			'faq'            => array_values( (array) nadlan_showroom_engine_json_meta( $id, 'project_faq_json' ) ),
			'units'          => array_values( (array) $units ),
		);
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_landmarks' ) ) {
	/* Beam v2 source data. Meta project_env_landmarks holds a JSON array of
	 * { label: {he,en,fr,ru,ar}|string, lat, lng }. Hard cap of 8; anything
	 * without a usable label or coordinates is dropped, never guessed. */
	function nadlan_showroom_engine_landmarks( $id ) {
		$raw = nadlan_showroom_engine_json_meta( $id, 'project_env_landmarks' );
		if ( ! is_array( $raw ) ) { return array(); }
		$out = array();
		foreach ( array_slice( array_values( $raw ), 0, 8 ) as $lm ) {
			if ( ! is_array( $lm ) ) { continue; }
			$lat = isset( $lm['lat'] ) ? (float) $lm['lat'] : 0.0;
			$lng = isset( $lm['lng'] ) ? (float) $lm['lng'] : 0.0;
			if ( ! $lat || ! $lng || abs( $lat ) > 90 || abs( $lng ) > 180 ) { continue; }
			$label = isset( $lm['label'] ) ? $lm['label'] : '';
			if ( is_array( $label ) ) {
				$clean = array();
				foreach ( array( 'he', 'en', 'fr', 'ru', 'ar' ) as $lg ) {
					if ( ! empty( $label[ $lg ] ) ) {
						$clean[ $lg ] = sanitize_text_field( (string) $label[ $lg ] );
					}
				}
				$label = $clean;
			} else {
				$label = sanitize_text_field( (string) $label );
			}
			if ( empty( $label ) ) { continue; }
			$out[] = array( 'label' => $label, 'lat' => $lat, 'lng' => $lng );
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_config' ) ) {
	function nadlan_showroom_engine_config( $default_slug ) {
		$post_id = (int) get_queried_object_id();
		if ( $post_id <= 0 ) {
			$post_id = (int) get_the_ID();
		}
		$selected_unit_surface_v2 = nadlan_unit_journey_is_v2_render( $post_id );
		$private_unit_journey_lab = nadlan_unit_journey_is_private_lab( $post_id );
		return array(
			'brand_key'      => 'brand',
			'lead_endpoint'  => esc_url_raw( rest_url( 'nadlan/v1/lead' ) ),
			/* The private lab has no public derivative endpoint. The REST route
			 * independently rejects it as the server-side boundary. */
			'brochure_endpoint' => $private_unit_journey_lab ? '' : esc_url_raw( rest_url( 'nadlan/v1/brochure' ) ),
			'cotour_endpoint'   => esc_url_raw( rest_url( 'nadlan/v1/cotour' ) ),
			'whatsapp'       => preg_replace( '/\D+/', '', (string) get_option( 'nadlan_whatsapp_e164', '' ) ),
			'phone'          => (string) get_option( 'nadlan_phone', '' ),
			'mapbox_token'   => (string) get_option( 'nadlan_mapbox_token', '' ),
			'demo'           => false,
			'default_project'=> $default_slug,
			'default_lang'   => 'he',
			'languages'      => array( 'he', 'en', 'fr', 'ru', 'ar' ),
			'rtl_languages'  => array( 'he', 'ar' ),
			'home_url'       => esc_url_raw( home_url() ),
			/* apartment studio: modular per the developer's package. Option is
			 * the site default; a project can override via project_studio_mode
			 * meta ('on'|'off'). */
			'studio'         => in_array( (string) get_option( 'nadlan_studio_mode', 'on' ), array( 'on', 'off' ), true ) ? (string) get_option( 'nadlan_studio_mode', 'on' ) : 'on',
			/* SELECTED-UNIT SURFACE flag (audit 2026-08-08): per-post sandbox
			 * gate. Production behavior is untouched until a post carries
			 * nl_unit_scene=on (or the site option flips after phone approval). */
			'selected_unit_surface' => $selected_unit_surface_v2
				|| ( 'on' === (string) get_post_meta( $post_id, 'nl_unit_scene', true ) )
				|| ( 'on' === (string) get_option( 'nadlan_selected_unit_surface', '' ) ),
			/* Private journey v2 is deliberately post-scoped. There is no global
			 * option: wider rollout still requires a separate, reviewed release. */
			'selected_unit_surface_v2' => $selected_unit_surface_v2,
			'private_unit_journey_lab' => $private_unit_journey_lab,
		);
	}
}

if ( ! function_exists( 'nadlan_showroom_engine_gallery_posts' ) ) {
	/** All published projects, paid/featured tier first (monetization placement). */
	function nadlan_showroom_engine_gallery_posts() {
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_project',
			'post_status'    => 'publish',
			'nadlan_private_visibility_applied' => true,
			'meta_query'     => array(
				'relation' => 'OR',
				array(
					'key'     => '_nadlan_private_unit_journey',
					'compare' => 'NOT EXISTS',
				),
				array(
					'key'     => '_nadlan_private_unit_journey',
					'value'   => 'private-unit-journey-v2',
					'compare' => '!=',
				),
			),
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
	/** A private payload may only be built on its own, already-unlocked singular. */
	function nadlan_unit_journey_target_is_renderable( $post_id ) {
		$post_id = (int) $post_id;
		if ( ! nadlan_unit_journey_is_private_lab( $post_id ) ) {
			return true;
		}
		return is_singular( 'nadlan_project' )
			&& (int) get_queried_object_id() === $post_id
			&& ! post_password_required( $post_id );
	}

	/** Resolve which post(s) the shortcode renders, from atts or page context. */
	function nadlan_showroom_engine_resolve_target( $atts ) {
		if ( $atts['page'] === 'home' ) {
			return nadlan_showroom_engine_gallery_posts();
		}
		if ( $atts['id'] ) {
			$p = get_post( (int) $atts['id'] );
			// international flagships run the SAME engine when addressed explicitly (owner 2026-07-12)
			if ( $p && in_array( $p->post_type, array( 'nadlan_project', 'nadlan_intl' ), true )
				&& nadlan_unit_journey_target_is_renderable( $p->ID ) ) { return array( $p ); }
		}
		if ( $atts['project'] ) {
			$p = get_page_by_path( sanitize_title( $atts['project'] ), OBJECT, 'nadlan_project' );
			if ( $p && nadlan_unit_journey_target_is_renderable( $p->ID ) ) { return array( $p ); }
		}
		if ( is_singular( 'nadlan_project' ) ) {
			$p = get_post( get_queried_object_id() );
			if ( $p && nadlan_unit_journey_target_is_renderable( $p->ID ) ) { return array( $p ); }
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
		$post_id = (int) get_the_ID();
		$is_unit_journey_v2 = $post_id > 0
			&& ( 'on' === (string) get_post_meta( $post_id, 'nl_unit_scene_v2', true ) );
		$is_private_lab = nadlan_unit_journey_is_private_lab( $post_id );

		/* A protected project must never leak its showroom payload, assets or
		 * unit inventory before WordPress accepts the post password. */
		if ( $post_id > 0 && post_password_required( $post_id ) ) {
			return '';
		}

		// assets
		wp_enqueue_style( 'nadlan-engine-tokens', $base . 'tokens.css', array(), NADLAN_CONFIG_VERSION );
		wp_enqueue_style( 'nadlan-engine-css', $base . 'showroom.css', array( 'nadlan-engine-tokens' ), NADLAN_CONFIG_VERSION );
		if ( ! $is_private_lab ) {
			wp_enqueue_style( 'nadlan-engine-editorial', $base . 'editorial.css', array( 'nadlan-engine-tokens' ), NADLAN_CONFIG_VERSION );
		}

		/* selected-unit surface CSS: attached inline on the engine handle ONLY
		 * where the flag is on (sandbox post / approved rollout) - explicit
		 * cascade order, same artifact as the engine, zero effect elsewhere */
		if ( $is_unit_journey_v2 ) {
			/* V2 replaces the selected-unit visual source. Do not load the v1
			 * stylesheet underneath it and repair the cascade afterwards. */
			$nl_unit_css = @file_get_contents( __DIR__ . '/../assets/showroom-engine/unit-journey.css' );
			if ( is_string( $nl_unit_css ) && '' !== $nl_unit_css ) {
				wp_add_inline_style( 'nadlan-engine-css', $nl_unit_css );
			}
		} elseif ( ( 'on' === (string) get_post_meta( $post_id, 'nl_unit_scene', true ) )
			|| ( 'on' === (string) get_option( 'nadlan_selected_unit_surface', '' ) ) ) {
			$nl_unit_css = @file_get_contents( __DIR__ . '/../assets/showroom-engine/unit-surface.css' );
			if ( is_string( $nl_unit_css ) && '' !== $nl_unit_css ) {
				wp_add_inline_style( 'nadlan-engine-css', $nl_unit_css );
			}
		}

		/* Cascade repair (measured live on /projects/duo-tel-aviv/ 2026-07-30): the theme ships
		   .single-nadlan_project .entry-content h2{color:var(--nlx-ink)!important} and
		   nadlan-premium-revenue.css .nlpf-name{color:#FFF8E7!important}. Both outrank showroom.css,
		   so every heading on a dark showroom surface rendered near-black (1.02-1.12:1, invisible -
		   including the inquiry form headline) while the project name rendered cream on the white
		   profile card. Repeated class selectors win the cascade here, so neither the theme nor
		   showroom.css has to be edited; the colours are the ones those components already declare. */
		wp_add_inline_style( 'nadlan-engine-css',
			'.nl-theater__title.nl-theater__title.nl-theater__title h2{color:var(--theater-fore)!important}'
			. '.nl-inquiry.nl-inquiry.nl-inquiry h2{color:#fff!important}'
			. '.nl-card--dark.nl-card--dark.nl-card--dark h2,.nl-card--dark.nl-card--dark.nl-card--dark h3{color:var(--cream)!important}'
			. '.nlpf-name.nlpf-name{color:#1B1A17!important}'
		);
		// 4.3.1 to match what retired project-3d registered on GLB pages - no silent downgrade.
		wp_enqueue_script( 'nadlan-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js', array(), '4.3.1', true );
		wp_script_add_data( 'nadlan-model-viewer', 'type', 'module' );
		wp_enqueue_script( 'nadlan-engine-i18n', $base . 'i18n.js', array(), NADLAN_CONFIG_VERSION, true );
		wp_enqueue_script( 'nadlan-engine-core', $base . 'engine.js', array( 'nadlan-engine-i18n' ), NADLAN_CONFIG_VERSION, true );
		if ( ! $is_private_lab ) {
			// buy-flow v1: "build me an offer" overlay (configure > capture > dispatch)
			wp_enqueue_script( 'nadlan-engine-buyflow', $base . 'buyflow.js', array( 'nadlan-engine-core' ), NADLAN_CONFIG_VERSION, true );
			// apartment studio: design-before-you-buy overlay (drag furniture,
			// accessibility clearances, notes -> travels inside the RFP)
			wp_enqueue_script( 'nadlan-engine-studio', $base . 'studio.js', array( 'nadlan-engine-core' ), NADLAN_CONFIG_VERSION, true );
		}

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
				// area per project: CMS surroundings (project_area_json) when authored,
				// else the minimal default so block 8 always renders; map.center feeds
				// the real Mapbox mount. Empty spokes/stats collapse cleanly.
				$areas = array();
				$i18n_add = array();
				$spokes_reg = array();
				foreach ( $projects as $slug => $proj ) {
					$custom = nadlan_showroom_area_from_meta( $proj['wp_id'], $proj, $i18n_add, $spokes_reg );
					$areas[ 'area_' . $slug ] = $custom ?: array(
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
					// honest per-project comps attribution: the global i18n footer says
					// Madlan/Tax-Authority, which is FALSE for press-sourced deals.
					$csrc = (string) get_post_meta( $proj['wp_id'], 'project_comps_source_note', true );
					if ( $csrc !== '' && $page === 'project' ) {
						foreach ( array( 'he', 'en', 'fr', 'ru', 'ar' ) as $clg ) {
							$i18n_add[ $clg ]['comps_source'] = sanitize_text_field( $csrc );
						}
					}
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
					'spokes'   => $spokes_reg,
				);
				$js = 'window.NADLAN_SHOWROOM=' . wp_json_encode( $payload ) . ';';
				wp_add_inline_script( 'nadlan-engine-core', $js, 'before' );
				// page-scoped i18n extension (area content + comps attribution) - the
				// engine reads keys through NADLAN_I18N, so extend it after i18n.js.
				if ( ! empty( $i18n_add ) ) {
					wp_add_inline_script( 'nadlan-engine-i18n',
						'(function(){var W=window.NADLAN_I18N;if(!W||!W.langs)return;var A=' . wp_json_encode( $i18n_add ) .
						';for(var l in A){W.langs[l]=W.langs[l]||{};for(var k in A[l]){W.langs[l][k]=A[l][k];}}})();' );
				}
				// an empty nearby-projects strip must collapse with its heading (DNA law)
				wp_add_inline_style( 'nadlan-engine-css',
					'#nl-root .nl-cards:empty{display:none}#nl-root h3:has(+ .nl-cards:empty){display:none}' );
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

if ( ! function_exists( 'nadlan_showroom_area_from_meta' ) ) {
	/* CMS surroundings (owner 20.8.2026, SIX-8 build): meta project_area_json
	 * fills engine block 8 (world spokes + stats) with per-language RESEARCHED
	 * content instead of bare headings. Shape:
	 *   { "label":{"he":..}, "blurb":{"he":..}, "coast_x":16,
	 *     "stats":[{"value":"2025","label":{"he":..,"en":..}}],
	 *     "groups":[{"icon":"train","label":{"he":..},"items":[{"he":..,"en":..}]}] }
	 * The engine consumes i18n KEYS only, so this synthesizes page-scoped keys
	 * (pa<ID>_*) and pours their per-language strings into $i18n_add for the
	 * i18n layer extension script. Missing/invalid meta returns null and the
	 * caller keeps the minimal default area. Never invented: only meta content. */
	function nadlan_showroom_area_from_meta( $pid, $proj, &$i18n_add, &$spokes_reg ) {
		$raw = nadlan_showroom_engine_json_meta( $pid, 'project_area_json' );
		if ( ! is_array( $raw ) || ( empty( $raw['stats'] ) && empty( $raw['groups'] ) ) ) { return null; }
		$langs = array( 'he', 'en', 'fr', 'ru', 'ar' );
		$put = function ( $key, $labels ) use ( &$i18n_add, $langs ) {
			$labels = is_array( $labels ) ? $labels : array( 'he' => (string) $labels );
			foreach ( $langs as $lg ) {
				if ( ! empty( $labels[ $lg ] ) ) {
					$i18n_add[ $lg ][ $key ] = sanitize_text_field( (string) $labels[ $lg ] );
				}
			}
		};
		$pfx = 'pa' . (int) $pid . '_';
		$put( $pfx . 'label', isset( $raw['label'] ) ? $raw['label'] : '' );
		$put( $pfx . 'blurb', isset( $raw['blurb'] ) ? $raw['blurb'] : '' );
		$icons = array( 'train', 'school', 'store', 'landmark', 'pin', 'cube' );
		$stats = array();
		foreach ( array_slice( (array) ( $raw['stats'] ?? array() ), 0, 6 ) as $i => $st ) {
			if ( ! is_array( $st ) || ! isset( $st['value'], $st['label'] ) ) { continue; }
			$k = $pfx . 'st' . $i;
			$put( $k, $st['label'] );
			$stats[] = array( 'id' => $k, 'value' => sanitize_text_field( (string) $st['value'] ), 'label_key' => $k );
		}
		$groups = array();
		foreach ( array_slice( (array) ( $raw['groups'] ?? array() ), 0, 5 ) as $gi => $g ) {
			if ( ! is_array( $g ) || empty( $g['items'] ) ) { continue; }
			$gk = $pfx . 'g' . $gi;
			$put( $gk, isset( $g['label'] ) ? $g['label'] : '' );
			$icon = in_array( (string) ( $g['icon'] ?? '' ), $icons, true ) ? (string) $g['icon'] : 'landmark';
			$items = array();
			foreach ( array_slice( (array) $g['items'], 0, 8 ) as $ii => $it ) {
				$ik = $gk . 'i' . $ii;
				$put( $ik, $it );
				$spokes_reg[ $ik ] = array( 'icon' => $icon, 'label_key' => $ik );
				$items[] = $ik;
			}
			if ( $items ) {
				$groups[] = array( 'id' => $gk, 'icon' => $icon, 'label_key' => $gk, 'items' => $items );
			}
		}
		return array(
			'label_key'    => $pfx . 'label',
			'blurb_key'    => $pfx . 'blurb',
			'map'          => array(
				'center'      => array( 'lat' => $proj['geo']['lat'], 'lng' => $proj['geo']['lng'] ),
				'project_pin' => array( 'x' => 50, 'y' => 50 ),
				'pins'        => array(),
				'coast_x'     => (int) ( $raw['coast_x'] ?? 16 ),
			),
			'spoke_groups' => $groups,
			'stats'        => $stats,
		);
	}
}

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
	/* Core has already replaced the body with the password form. Returning it
	 * unchanged is the privacy boundary: do not prepend an engine root. */
	if ( post_password_required( $pid ) ) {
		return $content;
	}
	/* Flagship v3 owns the complete selected surface. Read the reviewed raw
	 * dossier from this exact post; never feed it content already decorated by
	 * earlier project filters and never recurse through the_content here. */
	if ( function_exists( 'nadlan_flagship_v3_is_selected' ) && nadlan_flagship_v3_is_selected( $pid ) ) {
		$nl_flagship_v3_article = (string) get_post_field( 'post_content', $pid, 'raw' );
		return function_exists( 'nadlan_flagship_v3_dispatch' )
			? nadlan_flagship_v3_dispatch( $pid, $nl_flagship_v3_article )
			: '';
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
	/* Anything earlier filters prepended - the profile card that carries the
	   page's only <h1> (priority 5) and the price band (priority 7) - lives
	   BEFORE the legacy <main>. Slicing from the article section onward threw
	   it away: measured live, ashira-sde-dov was serving zero <h1> because of
	   exactly this, while its own id is the example in the comment above.
	   Only the isolate-the-article branch below loses it; the fallback branch
	   already preserves it, so this is captured and re-attached there only. */
	$prefix = '';
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
				if ( preg_match( '#<main\b[^>]*class="[^"]*nlv2-showroom[^"]*"#i', $original, $mm, PREG_OFFSET_CAPTURE ) ) {
					$prefix = substr( $original, 0, $mm[0][1] );
				}
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
	/* The private v2 page is a focused product lab, not a second SEO article.
	 * Keep the normal theme chrome, then lead directly with the real engine. */
	if ( nadlan_unit_journey_is_private_lab( $pid ) ) {
		return '<h1 id="nl-unit-v2-page-title" class="screen-reader-text">' . esc_html( get_the_title( $pid ) ) . '</h1>' . $engine;
	}
	// Wrap the article so editorial.css can style it (cream/gold system).
	/* The engine owns the page identity: one machine-readable <h1> first in
	 * the DOM (the theater shows the title visually). The legacy directory
	 * profile header used to carry the only <h1> and now steps aside on
	 * engine pages (see inc/directory.php), so without this line these pages
	 * would serve zero <h1>. */
	/* Facility chips moved out of the prefix weld into the article head -
	 * the facility-chips module skips engine pages for exactly this reason. */
	$chips = '';
	if ( function_exists( 'nadlan_fc_for_project' ) && function_exists( 'nadlan_fc_chips_html' )
		&& ! preg_match( '/-(en|fr|ru|ar)$/', (string) get_post_field( 'post_name', $pid ) ) ) {
		$fc_keys = nadlan_fc_for_project( $pid );
		if ( $fc_keys ) {
			$chips = '<div class="nlfc-hero" dir="rtl" aria-label="מתקנים ושירותים בפרויקט">'
				. nadlan_fc_chips_html( $fc_keys, array( 'limit' => 8, 'link' => true ) ) . '</div>';
		}
	}
	return '<h1 id="nl-project-page-title" class="screen-reader-text" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(1px,1px,1px,1px);white-space:nowrap;margin:0;padding:0">'
		. esc_html( get_the_title( $pid ) ) . '</h1>'
		. $engine . $prefix . '<div class="nadlan-project-article nadlan-guide">' . $chips . nadlan_showroom_engine_weave( $article, $pid ) . '</div>';
}, 8 );

/* Several mature project modules re-compose `the_content` at very late
 * priorities. Register this final pass only after WordPress has completed its
 * main query, so the private lab cannot inherit profile cards, notices,
 * feature bars or an SEO article after the focused engine filter above ran.
 * Assets/payload were already enqueued by the priority-8 pass; this callback
 * deliberately emits only the one existing engine mount point. */
add_action( 'wp', function () {
	if ( ! is_singular( 'nadlan_project' ) ) {
		return;
	}
	$pid = get_queried_object_id();
	if ( ! $pid || ! nadlan_unit_journey_is_private_lab( $pid ) ) {
		return;
	}
	/* Nothing project-specific may render around a locked private lab. Named
	 * emitters are removed here (before wp_head/wp_footer), while the final
	 * content pass below is the single owner of the password/body surface. */
	remove_action( 'wp_footer', 'nadlan_card_assets' );
	if ( nadlan_unit_journey_is_private_lab( $pid ) ) {
		remove_action( 'wp_head', 'nadlan_card_jsonld', 20 );
		remove_action( 'wp_head', 'nadlan_pjx_faq_jsonld', 30 );
		remove_action( 'wp_head', 'wp_oembed_add_discovery_links', 10 );
		remove_action( 'wp_head', 'wp_oembed_add_host_js', 10 );
		remove_action( 'wp_head', 'wp_shortlink_wp_head', 10 );
		remove_action( 'wp_head', 'rel_canonical' );
	}
	add_filter( 'the_content', function ( $content ) use ( $pid ) {
		global $post;
		if ( ! in_the_loop() || ! is_main_query() || ! $post || (int) $post->ID !== (int) $pid ) {
			return $content;
		}
		if ( post_password_required( $pid ) ) {
			/* Do not trust content assembled by any earlier project module: a
			 * fresh core form is the complete locked body, every time. */
			return get_the_password_form( get_post( $pid ) );
		}
		if ( function_exists( 'nadlan_flagship_v3_is_selected' ) && nadlan_flagship_v3_is_selected( $pid ) ) {
			if ( false !== strpos( (string) $content, 'data-nl-flagship="v3"' ) ) {
				return $content;
			}
			$nl_flagship_v3_article = (string) get_post_field( 'post_content', $pid, 'raw' );
			return function_exists( 'nadlan_flagship_v3_dispatch' )
				? nadlan_flagship_v3_dispatch( $pid, $nl_flagship_v3_article )
				: '';
		}
		return '<h1 id="nl-unit-v2-page-title" class="screen-reader-text">' . esc_html( get_the_title( $pid ) )
			. '</h1><div id="nl-root" data-page="project"></div>';
	}, PHP_INT_MAX );
}, PHP_INT_MAX );

/* Private sandbox indexing and cache boundary. The page is also created with
 * a WordPress post password and Yoast noindex meta; these headers are an
 * independent defence and remain present after the password cookie is set. */
add_filter( 'wp_robots', function ( $robots ) {
	if ( is_singular( 'nadlan_project' ) ) {
		$pid = get_queried_object_id();
		if ( $pid && nadlan_unit_journey_is_private_lab( $pid ) ) {
			$robots['noindex']   = true;
			$robots['nofollow']  = true;
			$robots['noarchive'] = true;
		}
	}
	return $robots;
}, 99 );

add_action( 'send_headers', function () {
	if ( is_singular( 'nadlan_project' ) ) {
		$pid = get_queried_object_id();
		if ( $pid && nadlan_unit_journey_is_private_lab( $pid ) ) {
			nocache_headers();
			header( 'X-Robots-Tag: noindex, nofollow, noarchive', true );
			/* Do not disclose the private URL to third-party map/tool requests,
			 * and do not allow the password surface to be framed off-origin. These
			 * response-only guards do not restrict the page's own child iframes. */
			header( 'Referrer-Policy: no-referrer', true );
			header( 'X-Content-Type-Options: nosniff', true );
			header( 'X-Frame-Options: SAMEORIGIN', true );
		}
	}
}, 99 );

add_filter( 'body_class', function ( $classes ) {
	if ( is_singular( 'nadlan_project' ) ) {
		$pid = get_queried_object_id();
		if ( $pid
			&& nadlan_unit_journey_is_private_lab( $pid )
			&& ! post_password_required( $pid ) ) {
			$classes[] = 'nl-unit-v2-sandbox';
		}
	}
	return array_values( array_unique( $classes ) );
} );

/* A password gives direct-link access; these query guards keep private v2
 * sandboxes out of public catalogs, search, REST collections and sitemaps.
 * They are deliberately meta-scoped so unrelated protected posts keep their
 * existing WordPress behaviour. */
if ( ! function_exists( 'nadlan_unit_journey_public_meta_query' ) ) {
	function nadlan_unit_journey_public_meta_query( $existing = array() ) {
		$private_exclusion = array(
			'relation' => 'OR',
			array(
				'key'     => '_nadlan_private_unit_journey',
				'compare' => 'NOT EXISTS',
			),
			array(
				'key'     => '_nadlan_private_unit_journey',
				'value'   => 'private-unit-journey-v2',
				'compare' => '!=',
			),
		);
		if ( empty( $existing ) ) {
			return $private_exclusion;
		}
		return array(
			'relation' => 'AND',
			$existing,
			$private_exclusion,
		);
	}
}

if ( ! function_exists( 'nadlan_unit_journey_query_may_discover_projects' ) ) {
	/** True for public project/list/search queries, but never the direct singular lab. */
	function nadlan_unit_journey_query_may_discover_projects( $query ) {
		if ( ! $query instanceof WP_Query ) {
			return false;
		}
		if ( $query->is_main_query() && $query->is_singular( 'nadlan_project' ) ) {
			return false;
		}
		$post_type = $query->get( 'post_type' );
		if ( 'nadlan_project' === $post_type || 'any' === $post_type ) {
			return true;
		}
		if ( is_array( $post_type ) && in_array( 'nadlan_project', $post_type, true ) ) {
			return true;
		}
		if ( $query->is_tax() ) {
			$taxonomy = get_taxonomy( (string) $query->get( 'taxonomy' ) );
			if ( $taxonomy && in_array( 'nadlan_project', (array) $taxonomy->object_type, true ) ) {
				return true;
			}
		}
		return $query->is_post_type_archive( 'nadlan_project' ) || $query->is_search();
	}
}

add_action( 'pre_get_posts', function ( $query ) {
	if ( ( is_admin() && ! wp_doing_ajax() )
		|| $query->get( 'nadlan_include_private_unit_journey' )
		|| $query->get( 'nadlan_private_visibility_applied' )
		|| ! nadlan_unit_journey_query_may_discover_projects( $query ) ) {
		return;
	}
	$query->set( 'meta_query', nadlan_unit_journey_public_meta_query( $query->get( 'meta_query' ) ) );
	$query->set( 'post__not_in', array_values( array_unique( array_merge(
		(array) $query->get( 'post__not_in' ),
		nadlan_unit_journey_private_project_ids()
	) ) ) );
	$query->set( 'nadlan_private_visibility_applied', true );
}, 20 );

add_filter( 'rest_nadlan_project_query', function ( $args, $request ) {
	if ( ! nadlan_unit_journey_can_manage_private_labs() ) {
		$args['meta_query'] = nadlan_unit_journey_public_meta_query(
			isset( $args['meta_query'] ) ? $args['meta_query'] : array()
		);
		$args['nadlan_private_visibility_applied'] = true;
		$args['post__not_in'] = array_values( array_unique( array_merge(
			isset( $args['post__not_in'] ) ? (array) $args['post__not_in'] : array(),
			nadlan_unit_journey_private_project_ids()
		) ) );
	}
	return $args;
}, 20, 2 );

/* Core /wp/v2/search can otherwise disclose a protected project's title,
 * URL and subtype without ever touching the project REST collection. */
add_filter( 'rest_post_search_query', function ( $args, $request ) {
	if ( ! nadlan_unit_journey_can_manage_private_labs() ) {
		$args['meta_query'] = nadlan_unit_journey_public_meta_query(
			isset( $args['meta_query'] ) ? $args['meta_query'] : array()
		);
		$args['nadlan_private_visibility_applied'] = true;
		$args['post__not_in'] = array_values( array_unique( array_merge(
			isset( $args['post__not_in'] ) ? (array) $args['post__not_in'] : array(),
			nadlan_unit_journey_private_project_ids()
		) ) );
	}
	return $args;
}, 20, 2 );

add_filter( 'rest_prepare_nadlan_project', function ( $response, $post, $request ) {
	if ( $post instanceof WP_Post
		&& nadlan_unit_journey_is_private_lab( $post->ID )
		&& ! current_user_can( 'edit_post', $post->ID ) ) {
		return new WP_Error(
			'rest_post_invalid_id',
			__( 'Invalid post ID.' ),
			array( 'status' => 404 )
		);
	}
	return $response;
}, 20, 3 );

add_filter( 'wp_sitemaps_posts_query_args', function ( $args, $post_type ) {
	if ( 'nadlan_project' === $post_type ) {
		$args['meta_query'] = nadlan_unit_journey_public_meta_query(
			isset( $args['meta_query'] ) ? $args['meta_query'] : array()
		);
		$args['nadlan_private_visibility_applied'] = true;
		$args['post__not_in'] = array_values( array_unique( array_merge(
			isset( $args['post__not_in'] ) ? (array) $args['post__not_in'] : array(),
			nadlan_unit_journey_private_project_ids()
		) ) );
	}
	return $args;
}, 20, 2 );

add_filter( 'wpseo_exclude_from_sitemap_by_post_ids', function ( $post_ids ) {
	return array_values( array_unique( array_merge(
		(array) $post_ids,
		nadlan_unit_journey_private_project_ids()
	) ) );
} );

/* Yoast's graph can re-create Article/WebPage nodes after the explicit schema
 * callbacks above were removed. The private lab has no public graph. */
add_filter( 'wpseo_json_ld_output', function ( $data ) {
	return nadlan_unit_journey_is_private_lab() ? false : $data;
}, 99 );

foreach ( array(
	'wpseo_metadesc',
	'wpseo_opengraph_title',
	'wpseo_opengraph_desc',
	'wpseo_twitter_title',
	'wpseo_twitter_description',
) as $nadlan_private_head_filter ) {
	add_filter( $nadlan_private_head_filter, function ( $value ) {
		return nadlan_unit_journey_is_private_lab() ? '' : $value;
	}, 99 );
}

/* Some special-project modules replace Yoast's canonical at priority 100.
 * Privacy remains the final owner for the dedicated lab marker. */
add_filter( 'wpseo_canonical', function ( $canonical ) {
	return nadlan_unit_journey_is_private_lab() ? false : $canonical;
}, PHP_INT_MAX );

if ( ! function_exists( 'nadlan_unit_journey_id_from_public_url' ) ) {
	/** Resolve only same-site URLs; used to make the core oEmbed endpoint opaque. */
	function nadlan_unit_journey_id_from_public_url( $url ) {
		$url       = esc_url_raw( (string) $url );
		$url_parts = wp_parse_url( $url );
		$home      = wp_parse_url( home_url( '/' ) );
		if ( empty( $url_parts['host'] ) || empty( $home['host'] )
			|| strtolower( $url_parts['host'] ) !== strtolower( $home['host'] ) ) {
			return 0;
		}
		$post_id = (int) url_to_postid( $url );
		if ( $post_id ) {
			return $post_id;
		}
		$path  = trim( isset( $url_parts['path'] ) ? $url_parts['path'] : '', '/' );
		$parts = array_values( array_filter( explode( '/', $path ) ) );
		$slug  = $parts ? end( $parts ) : '';
		$post  = $slug ? get_page_by_path( sanitize_title( $slug ), OBJECT, 'nadlan_project' ) : null;
		return $post instanceof WP_Post ? (int) $post->ID : 0;
	}
}

add_filter( 'rest_pre_dispatch', function ( $result, $server, $request ) {
	if ( '/oembed/1.0/embed' !== $request->get_route() ) {
		return $result;
	}
	$post_id = nadlan_unit_journey_id_from_public_url( $request->get_param( 'url' ) );
	if ( $post_id && nadlan_unit_journey_is_private_lab( $post_id )
		&& ! current_user_can( 'edit_post', $post_id ) ) {
		return new WP_Error(
			'oembed_invalid_url',
			__( 'Not found.' ),
			array( 'status' => 404 )
		);
	}
	return $result;
}, 20, 3 );

add_action( 'template_redirect', function () {
	$post_id = (int) get_queried_object_id();
	if ( is_feed() && ! $post_id ) {
		$post_id = absint( get_query_var( 'p' ) );
		$slug    = (string) get_query_var( 'name' );
		if ( '' === $slug ) {
			$slug = (string) get_query_var( 'nadlan_project' );
		}
		if ( ! $post_id && '' !== $slug ) {
			$feed_post = get_page_by_path( sanitize_title( $slug ), OBJECT, 'nadlan_project' );
			$post_id   = $feed_post instanceof WP_Post ? (int) $feed_post->ID : 0;
		}
	}
	if ( ( is_embed() || is_feed() ) && nadlan_unit_journey_is_private_lab( $post_id )
		&& ! current_user_can( 'edit_post', $post_id ) ) {
		nocache_headers();
		wp_die(
			esc_html__( 'Not found.' ),
			esc_html__( 'Not found.' ),
			array( 'response' => 404 )
		);
	}
}, 0 );

/* A private marker without a core post password is a broken two-factor gate,
 * not permission to publish. Fail closed before wp_head/enqueues can expose
 * the payload. Editors repair the object in wp-admin; front-end requests fail
 * closed for every role while the password is missing. */
add_action( 'template_redirect', function () {
	$post_id = (int) get_queried_object_id();
	$post    = $post_id ? get_post( $post_id ) : null;
	if ( ! $post instanceof WP_Post
		|| ! nadlan_unit_journey_is_private_lab( $post_id )
		|| nadlan_unit_journey_private_lab_has_password( $post_id ) ) {
		return;
	}
	nocache_headers();
	header( 'X-Robots-Tag: noindex, nofollow, noarchive', true );
	wp_die(
		esc_html__( 'Not found.' ),
		esc_html__( 'Not found.' ),
		array( 'response' => 404 )
	);
}, -10 );

/* Project modules enqueue globally on singular projects. Keep only the actual
 * showroom dependencies for an unlocked v2 lab; no Leaflet, article modules,
 * feature bars or walkthrough bundles should reach either locked HTML or the
 * focused unit journey. */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! nadlan_unit_journey_is_private_lab() ) {
		return;
	}
	$handles = array(
		'leaflet', 'nadlan-pjx', 'nadlan-pjx-js', 'nadlan-apl',
		'nadlan-feature-bar', 'nlfc', 'nadlan-devlink',
		'nadlan-milestones', 'nadlan-reviews', 'nlsdt',
	);
	foreach ( $handles as $handle ) {
		wp_dequeue_style( $handle );
		wp_deregister_style( $handle );
		wp_dequeue_script( $handle );
		wp_deregister_script( $handle );
	}
}, PHP_INT_MAX );

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
		// Articles authored with their own <section> wrappers must split at the
		// section boundary - splitting at <h2> orphans the wrapper tags and the
		// page renders stray empty <section> shells (found on DUO, 12 shells).
		$by_plain = ! $by_section && preg_match_all( '#<section\b#i', $article ) >= 4;
		$parts = $by_section
			? preg_split( '/(?=<section\b[^>]*class="[^"]*nlv2-section)/i', $article )
			: ( $by_plain
				? preg_split( '/(?=<section\b)/i', $article )
				: preg_split( '/(?=<h2\b)/i', $article ) );
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
	/* The private lab needs the schematic-tour provider after unlock, but the
	 * locked password response must not receive walkthrough CSS/JS. */
	if ( nadlan_unit_journey_is_private_lab() && post_password_required( get_queried_object_id() ) ) { return; }
	echo nadlan_ifp_assets_html(); // phpcs:ignore
} );

/* hreflang: emit the reciprocal language set so each sibling post is crawlable and
   Google serves the right language. Only for siblings that exist and are published. */
add_action( 'wp_head', function () {
	if ( ! is_singular( 'nadlan_project' ) ) { return; }
	if ( nadlan_unit_journey_is_private_lab() ) { return; }
	/* project-lang.php (prio 3) owns the cluster now; this stays only as a
	   fallback for a request where it did not print (one emitter, never two) */
	if ( ! empty( $GLOBALS['nl_plang_printed'] ) ) { return; }
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

if ( ! function_exists( 'nadlan_showroom_scan_walk_media' ) ) {
	/**
	 * Scan media for walk steps titled <prefix><space>, canonical order
	 * building -> apartment, naming aliases normalized, 360-* excluded
	 * (equirectangular panoramas belong to the pano layer, not flat frames).
	 */
	function nadlan_showroom_scan_walk_media( $prefix ) {
		$q = new WP_Query( array(
			'post_type' => 'attachment', 'post_status' => 'inherit',
			'post_mime_type' => 'image', 'posts_per_page' => 40, 'fields' => 'ids',
			's' => rtrim( $prefix, '-' ), 'no_found_rows' => true,
		) );
		$found = array();
		foreach ( $q->posts as $aid ) {
			$title = (string) get_the_title( $aid );
			if ( strpos( $title, $prefix ) !== 0 ) { continue; }
			$key = preg_replace( '/\.(png|jpe?g|webp)$/i', '', substr( $title, strlen( $prefix ) ) );
			if ( strpos( $key, '360-' ) === 0 || strpos( $key, '360_' ) === 0 ) { continue; }
			$aliases = array( 'building-exterior' => 'exterior', 'building-entrance' => 'entrance', 'facade' => 'exterior', 'bedroom' => 'second-bedroom' );
			if ( isset( $aliases[ $key ] ) ) { $key = $aliases[ $key ]; }
			$url = wp_get_attachment_image_url( $aid, 'large' );
			if ( ! $url ) { $url = wp_get_attachment_url( $aid ); }
			if ( $key !== '' && $url ) { $found[ $key ] = array( 'key' => $key, 'url' => esc_url_raw( $url ) ); }
		}
		$order = array( 'exterior', 'street-entrance', 'entrance', 'lobby', 'stairwell', 'elevator', 'entry-hall', 'living-room', 'kitchen', 'master-bedroom', 'second-bedroom', 'bathroom', 'balcony' );
		$out = array();
		foreach ( $order as $k ) { if ( isset( $found[ $k ] ) ) { $out[] = $found[ $k ]; unset( $found[ $k ] ); } }
		foreach ( $found as $extra ) { $out[] = $extra; }
		return $out;
	}
}

if ( ! function_exists( 'nadlan_showroom_default_tour' ) ) {
	/** The standard default walk set (standard-default-*). Self-maintaining. */
	function nadlan_showroom_default_tour() {
		$cache = get_transient( 'nadlan_default_tour_v1' );
		if ( is_array( $cache ) ) { return $cache; }
		$out = nadlan_showroom_scan_walk_media( 'standard-default-' );
		set_transient( 'nadlan_default_tour_v1', $out, HOUR_IN_SECONDS );
		return $out;
	}
	add_action( 'add_attachment', function () { delete_transient( 'nadlan_default_tour_v1' ); } );
}

if ( ! function_exists( 'nadlan_showroom_project_walk' ) ) {
	/**
	 * DEDICATED walk for one project (CMS path, owner ask 2026-07-06): upload
	 * media titled walk-<project-slug>-<space> (developer material or paid
	 * listing assets) and the page walk switches from the standard set to the
	 * project's own pictures automatically.
	 */
	function nadlan_showroom_project_walk( $id, $slug ) {
		$slug = sanitize_title( $slug );
		if ( $slug === '' ) { return array(); }
		// language siblings share the parent's dedicated walk
		$slug = preg_replace( '/-(en|fr|ru|ar)$/', '', $slug );
		$tkey = 'nadlan_pwalk_' . md5( $slug );
		$cache = get_transient( $tkey );
		if ( is_array( $cache ) ) { return $cache; }
		$out = nadlan_showroom_scan_walk_media( 'walk-' . $slug . '-' );
		set_transient( $tkey, $out, 30 * MINUTE_IN_SECONDS );
		return $out;
	}
}

if ( ! function_exists( 'nadlan_showroom_premium_tour' ) ) {
	/** The premium default walk set (premium-default-*), for featured projects. */
	function nadlan_showroom_premium_tour() {
		$cache = get_transient( 'nadlan_premium_tour_v1' );
		if ( is_array( $cache ) ) { return $cache; }
		$out = nadlan_showroom_scan_walk_media( 'premium-default-' );
		set_transient( 'nadlan_premium_tour_v1', $out, HOUR_IN_SECONDS );
		return $out;
	}
	add_action( 'add_attachment', function () { delete_transient( 'nadlan_premium_tour_v1' ); } );
}

if ( ! function_exists( 'nadlan_showroom_default_tour_tier' ) ) {
	/** Featured projects get the premium sample set once it is rich enough (4+ spaces). */
	function nadlan_showroom_default_tour_tier( $id ) {
		if ( get_post_meta( $id, 'project_featured', true ) && count( nadlan_showroom_premium_tour() ) >= 4 ) { return 'premium'; }
		return 'standard';
	}
	function nadlan_showroom_default_tour_for( $id ) {
		return nadlan_showroom_default_tour_tier( $id ) === 'premium' ? nadlan_showroom_premium_tour() : nadlan_showroom_default_tour();
	}
}
