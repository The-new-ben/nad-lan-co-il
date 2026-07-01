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
			'lang_urls'      => $lang_urls,
			'self_lang'      => $self_lang,
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
		wp_enqueue_style( 'nadlan-engine-tokens', $base . 'tokens.css', array(), '1.69.56' );
		wp_enqueue_style( 'nadlan-engine-css', $base . 'showroom.css', array( 'nadlan-engine-tokens' ), '1.69.56' );
		wp_enqueue_style( 'nadlan-engine-editorial', $base . 'editorial.css', array( 'nadlan-engine-tokens' ), '1.69.56' );
		wp_enqueue_script( 'nadlan-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js', array(), '4.0.0', true );
		wp_script_add_data( 'nadlan-model-viewer', 'type', 'module' );
		wp_enqueue_script( 'nadlan-engine-i18n', $base . 'i18n.js', array(), '1.69.56', true );
		wp_enqueue_script( 'nadlan-engine-core', $base . 'engine.js', array( 'nadlan-engine-i18n' ), '1.69.56', true );

		// Real Mapbox only when a token is configured; otherwise the stylized map stays.
		if ( (string) get_option( 'nadlan_mapbox_token', '' ) !== '' ) {
			wp_enqueue_style( 'mapbox-gl', 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css', array(), '3.7.0' );
			wp_enqueue_script( 'mapbox-gl', 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js', array(), '3.7.0', true );
			wp_enqueue_script( 'nadlan-engine-mapbox', $base . 'mapbox-init.js', array( 'nadlan-engine-core', 'mapbox-gl' ), '1.69.56', true );
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
 * model. When the developer's official BIM arrives, edit the field — done.
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
		$start = stripos( $original, '<section class="nlv2-section"' );
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
	return $engine . '<div class="nadlan-project-article nadlan-guide">' . $article . '</div>';
}, 8 );

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

// Direct Access Meta Box for Showroom Engine
add_action("add_meta_boxes", function() {
    add_meta_box("nadlan_showroom_engine_meta", "Showroom Engine - Direct Access", "nadlan_showroom_engine_meta_cb", "nadlan_project", "normal", "high");
});

function nadlan_showroom_engine_meta_cb($post) {
    wp_nonce_field("nadlan_showroom_engine_nonce", "nadlan_showroom_engine_nonce_val");
    $use_engine = get_post_meta($post->ID, "nlp3d_use_engine", true);
    $poster = get_post_meta($post->ID, "project_model_poster", true);
    $glb = get_post_meta($post->ID, "project_model_glb", true);
    $lat = get_post_meta($post->ID, "lat", true);
    $lng = get_post_meta($post->ID, "lng", true);
    ?>
    <table class="form-table">
        <tr>
            <th><label for="nlp3d_use_engine">Enable Showroom Engine</label></th>
            <td><input type="checkbox" id="nlp3d_use_engine" name="nlp3d_use_engine" value="1" <?php checked($use_engine, "1"); ?> />
            <p class="description">Turn on the new 3D mapping and interactive showroom for this project.</p></td>
        </tr>
        <tr>
            <th><label for="project_model_poster">Sketch / Poster Image (URL)</label></th>
            <td><input type="text" id="project_model_poster" name="project_model_poster" value="<?php echo esc_attr($poster); ?>" class="regular-text" />
            <p class="description">Fallback sketch image to use instead of a 3D model (e.g. Rainbow style).</p></td>
        </tr>
        <tr>
            <th><label for="project_model_glb">3D Model (GLB URL)</label></th>
            <td><input type="text" id="project_model_glb" name="project_model_glb" value="<?php echo esc_attr($glb); ?>" class="regular-text" />
            <p class="description">Optional 3D model. Leave blank to rely entirely on the sketch/poster.</p></td>
        </tr>
        <tr>
            <th><label for="lat">Mapbox Latitude</label></th>
            <td><input type="text" id="lat" name="lat" value="<?php echo esc_attr($lat); ?>" class="regular-text" /></td>
        </tr>
        <tr>
            <th><label for="lng">Mapbox Longitude</label></th>
            <td><input type="text" id="lng" name="lng" value="<?php echo esc_attr($lng); ?>" class="regular-text" /></td>
        </tr>
    </table>
    <?php
}

add_action("save_post", function($post_id) {
    if (!isset($_POST["nadlan_showroom_engine_nonce_val"]) || !wp_verify_nonce($_POST["nadlan_showroom_engine_nonce_val"], "nadlan_showroom_engine_nonce")) {
        return;
    }
    if (defined("DOING_AUTOSAVE") && DOING_AUTOSAVE) return;
    if (!current_user_can("edit_post", $post_id)) return;

    if (isset($_POST["nlp3d_use_engine"])) {
        update_post_meta($post_id, "nlp3d_use_engine", "1");
    } else {
        delete_post_meta($post_id, "nlp3d_use_engine");
    }

    $fields = array("project_model_poster", "project_model_glb", "lat", "lng");
    foreach ($fields as $f) {
        if (isset($_POST[$f])) {
            update_post_meta($post_id, $f, sanitize_text_field($_POST[$f]));
        }
    }
});

