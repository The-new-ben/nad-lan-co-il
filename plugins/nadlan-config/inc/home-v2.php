<?php
/**
 * nadlan-config - Homepage v2: the 12-band rich homepage (v1.69.87)
 *
 * Implements handoff/claude-design/2026-07-02-homepage/homepage-spec.md and the
 * standalone mockup (factory-run drop). The homepage's jobs: convert brand
 * traffic, distribute link equity into ranking surfaces, look like an
 * institution. Everything renders from CMS data; a band with missing data
 * collapses cleanly. Band order/on-off via option `nadlan_home_bands`.
 *
 * Bands: ticker · browse (mega-menu links) · hero · market · projects(dark) ·
 * listings · areas · magazine · tools · pros · intl(dark) · megafooter.
 *
 * Honesty rules: every figure prints value + source + date; catalog-derived
 * stats are labeled as such; sponsored slots carry a visible label; no "3D"
 * in headings (badge on cards only); no em-dash in copy.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ============================ data helpers ============================ */

if ( ! function_exists( 'nadlan_hv2_img' ) ) {
	function nadlan_hv2_img( $id ) {
		// IMAGERY PIVOT (owner decision 1, 2026-07-07): the real model render
		// leads; the sketch featured image is the fallback, not the face.
		$poster = (string) get_post_meta( $id, 'project_model_poster', true );
		if ( $poster ) { return $poster; }
		if ( has_post_thumbnail( $id ) ) { return get_the_post_thumbnail_url( $id, 'large' ); }
		$photos = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) );
		return $photos ? $photos[0] : '';
	}
}

if ( ! function_exists( 'nadlan_hv2_interior_pool' ) ) {
	/* Our own generated interior stills (media library, post_name interior-*),
	   ID-ascending for a stable, deterministic order. Static + transient cache. */
	function nadlan_hv2_interior_pool() {
		static $pool = null;
		if ( is_array( $pool ) ) { return $pool; }
		$pool = get_transient( 'nadlan_hv2_interiors' );
		if ( ! is_array( $pool ) ) {
			global $wpdb;
			$ids  = $wpdb->get_col( "SELECT ID FROM {$wpdb->posts} WHERE post_type='attachment' AND post_mime_type LIKE 'image/%' AND post_name LIKE 'interior-%' ORDER BY ID ASC LIMIT 40" );
			$pool = array();
			foreach ( (array) $ids as $aid ) {
				$u = wp_get_attachment_image_url( (int) $aid, 'medium_large' );
				if ( $u ) { $pool[] = $u; }
			}
			set_transient( 'nadlan_hv2_interiors', $pool, 6 * HOUR_IN_SECONDS );
		}
		return $pool;
	}
}

if ( ! function_exists( 'nadlan_hv2_listing_media' ) ) {
	/* LISTING IMAGERY LADDER (owner 2026-07-29: the pencil sketch plates read
	   unprofessional as the card face). (a) a real listing photo when one
	   exists; (b) else one of OUR OWN generated interior stills, rotated
	   deterministically by listing id (demo listings + our renders; the card
	   carries an honest הדמיה tag); (c) else a rich gradient placeholder in
	   the flagship visual language. The sketch plate never leads a card.
	   Returns array( url_or_empty, 'photo'|'interior'|'ph' ). */
	function nadlan_hv2_listing_media( $id ) {
		$is_sketch = function ( $u ) {
			return '' === $u || preg_match( '~listing-plate|sketch~i', $u ) || preg_match( '~\.svg(\?|$)~i', $u );
		};
		$photos = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) );
		foreach ( $photos as $p ) {
			if ( preg_match( '~^https?://~i', $p ) && ! $is_sketch( $p ) ) { return array( $p, 'photo' ); }
		}
		$thumb = has_post_thumbnail( $id ) ? (string) get_the_post_thumbnail_url( $id, 'medium_large' ) : '';
		if ( $thumb && ! $is_sketch( $thumb ) ) { return array( $thumb, 'photo' ); }
		$pool = nadlan_hv2_interior_pool();
		if ( $pool ) { return array( $pool[ absint( $id ) % count( $pool ) ], 'interior' ); }
		return array( '', 'ph' );
	}
}

if ( ! function_exists( 'nadlan_mapbox_token' ) ) {
	function nadlan_mapbox_token() { return trim( (string) get_option( 'nadlan_mapbox_token', '' ) ); }
}

/* Owner pastes the Mapbox public token in wp-admin -> Settings -> General. */
/* Also expose the two owner settings over the REST settings endpoint so the
   agent can set them without a wp-admin session (show_in_rest requires the
   registration to run on rest_api_init as well as admin_init). */
add_action( 'rest_api_init', function () {
	register_setting( 'general', 'nadlan_mapbox_token', array( 'type' => 'string', 'sanitize_callback' => 'sanitize_text_field', 'default' => '', 'show_in_rest' => true ) );
	register_setting( 'general', 'nadlan_home_video_url', array( 'type' => 'string', 'sanitize_callback' => 'esc_url_raw', 'default' => '', 'show_in_rest' => true ) );
	register_setting( 'general', 'nadlan_home_video_webm', array( 'type' => 'string', 'sanitize_callback' => 'esc_url_raw', 'default' => '', 'show_in_rest' => true ) );
	register_setting( 'general', 'nadlan_home_video_poster', array( 'type' => 'string', 'sanitize_callback' => 'esc_url_raw', 'default' => '', 'show_in_rest' => true ) );
	register_setting( 'general', 'nadlan_home_hero_aerial', array( 'type' => 'string', 'sanitize_callback' => 'esc_url_raw', 'default' => '', 'show_in_rest' => true ) );
	register_setting( 'general', 'nadlan_ur_band_img', array( 'type' => 'string', 'sanitize_callback' => 'esc_url_raw', 'default' => '', 'show_in_rest' => true ) );
	register_setting( 'general', 'nadlan_rm_band_img', array( 'type' => 'string', 'sanitize_callback' => 'esc_url_raw', 'default' => '', 'show_in_rest' => true ) );
} );

add_action( 'admin_init', function () {
	register_setting( 'general', 'nadlan_mapbox_token', array( 'type' => 'string', 'sanitize_callback' => 'sanitize_text_field', 'default' => '' ) );
	add_settings_field( 'nadlan_mapbox_token', 'Mapbox Token (נדלן)', function () {
		printf( '<input type="text" id="nadlan_mapbox_token" name="nadlan_mapbox_token" value="%s" class="regular-text" dir="ltr" placeholder="pk.xxxx"><p class="description">אסימון ציבורי (pk.) של Mapbox. מומלץ להגביל אותו לדומיין nad-lan.co.il בחשבון Mapbox.</p>', esc_attr( get_option( 'nadlan_mapbox_token', '' ) ) );
	}, 'general' );
	register_setting( 'general', 'nadlan_home_video_url', array( 'type' => 'string', 'sanitize_callback' => 'esc_url_raw', 'default' => '' ) );
	add_settings_field( 'nadlan_home_video_url', 'סרטון עמוד הבית (נדלן)', function () {
		printf( '<input type="url" id="nadlan_home_video_url" name="nadlan_home_video_url" value="%s" class="regular-text" dir="ltr" placeholder="https://youtu.be/..."><p class="description">קישור YouTube / Vimeo או קובץ MP4 מספריית המדיה. משאירים ריק כדי להסתיר את רצועת הסרטון.</p>', esc_attr( get_option( 'nadlan_home_video_url', '' ) ) );
	}, 'general' );
} );

/* Front-page title + description per homepage-spec. A filter in versioned code,
   NOT a live snippet - the one-shot snippet approach took the site down on
   2026-07-02 and is banned. */
add_filter( 'wpseo_title', function ( $title ) {
	return is_front_page() ? 'נדלן - דירות למכירה, פרויקטים חדשים ומחירי דירות בישראל' : $title;
}, 20 );
add_filter( 'wpseo_metadesc', function ( $desc ) {
	return is_front_page() ? 'דירות למכירה ולהשכרה, פרויקטים חדשים עם בחירת דירה מתוך הבניין, מחירי עסקאות אמיתיים, מחשבונים ובעלי מקצוע מאומתים. הכל במקום אחד - נדלן.' : $desc;
}, 20 );
/* The wpseo_title filter was observed NOT changing the rendered <title> on this
   install (Yoast serves the page's stored custom title). pre_get_document_title
   at a late priority wins over every generator for the actual tag. */
add_filter( 'pre_get_document_title', function ( $title ) {
	return is_front_page() ? 'נדלן - דירות למכירה, פרויקטים חדשים ומחירי דירות בישראל' : $title;
}, 9999 );

/* Top cities by real inventory (cached). [ ['name','projects','properties'], ... ] */
if ( ! function_exists( 'nadlan_hv2_cities' ) ) {
	function nadlan_hv2_cities( $limit = 10 ) {
		$hit = get_transient( 'nadlan_hv2_cities_v2' );
		if ( is_array( $hit ) ) { return array_slice( $hit, 0, $limit ); }
		global $wpdb;
		$rows = $wpdb->get_results( "SELECT pm.meta_value city, p.post_type pt, COUNT(*) n
			FROM {$wpdb->postmeta} pm INNER JOIN {$wpdb->posts} p ON p.ID = pm.post_id
			WHERE pm.meta_key = 'city' AND pm.meta_value <> '' AND p.post_status = 'publish'
			AND p.post_type IN ('nadlan_project','nadlan_property')
			AND (p.post_type <> 'nadlan_project' OR NOT EXISTS (
				SELECT 1 FROM {$wpdb->postmeta} private_v2
				WHERE private_v2.post_id=p.ID AND private_v2.meta_key='_nadlan_private_unit_journey' AND private_v2.meta_value='private-unit-journey-v2'
			))
			GROUP BY pm.meta_value, p.post_type", ARRAY_A );
		$map = array();
		foreach ( (array) $rows as $r ) {
			$c = trim( (string) $r['city'] );
			if ( $c === '' || mb_strlen( $c ) > 30 ) { continue; }
			if ( ! isset( $map[ $c ] ) ) { $map[ $c ] = array( 'name' => $c, 'projects' => 0, 'properties' => 0 ); }
			$map[ $c ][ $r['pt'] === 'nadlan_project' ? 'projects' : 'properties' ] += (int) $r['n'];
		}
		usort( $map, function ( $a, $b ) { return ( $b['projects'] + $b['properties'] ) <=> ( $a['projects'] + $a['properties'] ); } );
		$map = array_values( $map );
		set_transient( 'nadlan_hv2_cities_v2', $map, 12 * HOUR_IN_SECONDS );
		return array_slice( $map, 0, $limit );
	}
}

/* Projects that actually have a picture to show. The dark band used to call
   nadlan_hv2_featured_projects(), whose EXISTS check matches an EMPTY glb meta
   and whose backfill query has no requirement at all - so it served the three
   newest projects, image or not, and they rendered as black rectangles
   (owner, 2026-07-29). This one filters on the real image ladder instead and
   does NOT demand a 3D model: a new contractor project with a good photo and
   facility badges earns its place. $exclude keeps the flagships from repeating. */
if ( ! function_exists( 'nadlan_hv2_image_projects' ) ) {
	function nadlan_hv2_image_projects( $n = 3, $exclude = array() ) {
		$exclude = array_map( 'intval', (array) $exclude );
		$pool = get_posts( array(
			'post_type'      => 'nadlan_project',
			'post_status'    => 'publish',
			'posts_per_page' => 40,
			'no_found_rows'  => true,
			'post__not_in'   => $exclude,
		) );
		$out = array();
		foreach ( $pool as $p ) {
			if ( preg_match( '/-(en|fr|ru|ar)$/', $p->post_name ) ) { continue; } // language sibling
			if ( '' === (string) nadlan_hv2_img( $p->ID ) ) { continue; }         // no picture, no slot
			$out[] = $p;
			if ( count( $out ) >= $n ) { break; }
		}
		return $out;
	}
}

/* Featured projects: engine-quality, DISTINCT (no language siblings). */
if ( ! function_exists( 'nadlan_hv2_featured_projects' ) ) {
	function nadlan_hv2_featured_projects( $n = 3 ) {
		$sib = function ( $p ) { return (bool) preg_match( '/-(en|fr|ru|ar)$/', $p->post_name ); };
		$pool = get_posts( array( 'post_type' => 'nadlan_project', 'posts_per_page' => 12, 'no_found_rows' => true,
			'meta_query' => array( array( 'key' => 'project_model_glb', 'compare' => 'EXISTS' ) ) ) );
		$out = array_slice( array_values( array_filter( $pool, function ( $p ) use ( $sib ) { return ! $sib( $p ); } ) ), 0, $n );
		if ( count( $out ) < $n ) {
			$more = get_posts( array( 'post_type' => 'nadlan_project', 'posts_per_page' => 12, 'no_found_rows' => true, 'post__not_in' => wp_list_pluck( $out, 'ID' ) ) );
			$more = array_values( array_filter( $more, function ( $p ) use ( $sib ) { return ! $sib( $p ); } ) );
			$out  = array_merge( $out, array_slice( $more, 0, $n - count( $out ) ) );
		}
		return $out;
	}
}

/* ---------- market snapshot: real catalog-derived figures, daily cron ---------- */
if ( ! function_exists( 'nadlan_hv2_snapshot_compute' ) ) {
	function nadlan_hv2_snapshot_compute() {
		global $wpdb;
		$snap = (array) get_option( 'nadlan_market_snapshot', array() );
		$avg  = function ( $city_like ) use ( $wpdb ) {
			$sql = "SELECT AVG(CAST(pm.meta_value AS UNSIGNED)) FROM {$wpdb->postmeta} pm
				INNER JOIN {$wpdb->posts} p ON p.ID = pm.post_id
				WHERE pm.meta_key = 'project_3d_avg_price_per_sqm' AND CAST(pm.meta_value AS UNSIGNED) > 1000
				AND p.post_type = 'nadlan_project' AND p.post_status = 'publish'
				AND NOT EXISTS (SELECT 1 FROM {$wpdb->postmeta} private_v2
					WHERE private_v2.post_id=p.ID AND private_v2.meta_key='_nadlan_private_unit_journey' AND private_v2.meta_value='private-unit-journey-v2')";
			if ( $city_like ) {
				$sql .= $wpdb->prepare( " AND p.ID IN (SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key='city' AND meta_value LIKE %s)", '%' . $wpdb->esc_like( $city_like ) . '%' );
			}
			return (int) $wpdb->get_var( $sql );
		};
		$snap['ppsqm_tlv']  = $avg( 'תל אביב' );
		$snap['ppsqm_il']   = $avg( '' );
		$snap['listings_n'] = (int) wp_count_posts( 'nadlan_property' )->publish;
		$snap['projects_n'] = function_exists( 'nadlan_unit_journey_public_project_count' )
			? nadlan_unit_journey_public_project_count()
			: (int) wp_count_posts( 'nadlan_project' )->publish;
		$snap['privacy_v2'] = 1;
		$snap['updated']    = current_time( 'd/m/Y' );
		// yoy + mortgage_rate are OWNER-SET (external sources); never computed, never invented.
		update_option( 'nadlan_market_snapshot', $snap, false );
		return $snap;
	}
}
add_action( 'nadlan_hv2_snapshot_daily', 'nadlan_hv2_snapshot_compute' );
add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'nadlan_hv2_snapshot_daily' ) ) {
		wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nadlan_hv2_snapshot_daily' );
	}
} );

/* Sponsored slot: one professional per profession (sponsored first, else top-rated). */
if ( ! function_exists( 'nadlan_hv2_pro_slot' ) ) {
	function nadlan_hv2_pro_slot( $profession ) {
		$q = get_posts( array( 'post_type' => 'nadlan_professional', 'posts_per_page' => 1, 'no_found_rows' => true, 'fields' => 'ids',
			'meta_query' => array(
				array( 'key' => 'profession', 'value' => $profession ),
				array( 'key' => 'sponsored_until', 'value' => current_time( 'Y-m-d' ), 'compare' => '>=', 'type' => 'DATE' ),
			) ) );
		if ( $q ) { return array( 'id' => $q[0], 'sponsored' => true ); }
		$q = get_posts( array( 'post_type' => 'nadlan_professional', 'posts_per_page' => 1, 'no_found_rows' => true, 'fields' => 'ids',
			'meta_key' => 'rating', 'orderby' => 'meta_value_num', 'order' => 'DESC',
			'meta_query' => array( array( 'key' => 'profession', 'value' => $profession ) ) ) );
		return $q ? array( 'id' => $q[0], 'sponsored' => false ) : null;
	}
}

/* ============================ band renderers ============================ */

if ( ! function_exists( 'nadlan_hv2_band_ticker' ) ) {
	function nadlan_hv2_band_ticker() {
		$s = (array) get_option( 'nadlan_market_snapshot', array() );
		if ( empty( $s ) || empty( $s['privacy_v2'] ) ) { $s = nadlan_hv2_snapshot_compute(); }
		$items = array();
		if ( ! empty( $s['ppsqm_tlv'] ) ) { $items[] = array( nadlan_i18n( 'tk_tlv' ), number_format( (int) $s['ppsqm_tlv'] ) . ' ₪', home_url( '/projects/?city=' . rawurlencode( 'תל אביב' ) ) ); }
		// Honesty gate: the "national" average comes from the same small catalog
		// sample; when it is basically the TLV number it would mislead - hide it.
		if ( ! empty( $s['ppsqm_il'] ) && ( empty( $s['ppsqm_tlv'] ) || abs( (int) $s['ppsqm_il'] - (int) $s['ppsqm_tlv'] ) >= 0.2 * (int) $s['ppsqm_tlv'] ) ) { $items[] = array( nadlan_i18n( 'tk_watch' ), number_format( (int) $s['ppsqm_il'] ) . ' ₪', home_url( '/projects/' ) ); }
		if ( ! empty( $s['mortgage_rate'] ) ) { $items[] = array( nadlan_i18n( 'mk_rate' ), esc_html( $s['mortgage_rate'] ), home_url( '/mortgage-calculator/' ) ); }
		if ( ! empty( $s['projects_n'] ) ) { $items[] = array( nadlan_i18n( 'tk_projects' ), number_format( (int) $s['projects_n'] ), home_url( '/projects/' ) ); }
		if ( ! $items ) { return; }
		echo '<div class="nlhv2-ticker" dir="' . ( nadlan_lang_is_rtl( nadlan_current_lang() ) ? 'rtl' : 'ltr' ) . '"><span class="nlhv2-ticker-date">' . esc_html( ! empty( $s['updated'] ) ? $s['updated'] : current_time( 'd/m/Y' ) ) . ' · ' . nadlan_i18n( 'tk_source' ) . '</span>';
		foreach ( $items as $i ) {
			echo '<a href="' . esc_url( $i[2] ) . '"><b>' . esc_html( $i[1] ) . '</b> ' . esc_html( $i[0] ) . '</a>';
		}
		echo '</div>';
	}
}

if ( ! function_exists( 'nadlan_hv2_band_browse' ) ) {
	function nadlan_hv2_band_browse() {
		$cities = nadlan_hv2_cities( 8 );
		$profs  = function_exists( 'nadlan_dir_professions_all' ) ? nadlan_dir_professions_all() : array();
		?>
<nav class="nlhv2-browse" dir="<?php echo nadlan_lang_is_rtl( nadlan_current_lang() ) ? 'rtl' : 'ltr'; ?>" aria-label="<?php echo esc_attr( nadlan_i18n( 'nav_label' ) ); ?>">
	<?php /* V7 (owner order 22.8): ONE horizontal mega nav, SEO-first order —
	   the head-term hubs (projects, prices) sit first so every crawl of the
	   homepage meets them earliest; the prices panel now links the REAL city
	   price pages (they convert in GSC) instead of catalog facets; a 3D-tours
	   group joins (the tours hub is the canonical share URL). Panels stay
	   tight on purpose — nav-wide link dumps dilute PageRank. */ ?>
	<details><summary><?php nadlan_e( 'm_projects' ); ?></summary><div class="nlhv2-mega">
		<a href="<?php echo esc_url( home_url( '/projects/' ) ); ?>"><b><?php nadlan_e( 'all_projects' ); ?></b></a>
		<?php foreach ( array_slice( $cities, 0, 6 ) as $c ) : if ( ! $c['projects'] ) { continue; } ?>
		<a href="<?php echo esc_url( home_url( '/projects/?city=' . rawurlencode( $c['name'] ) ) ); ?>"><?php nadlan_e( 'projects_in' ); ?><?php echo esc_html( $c['name'] ); ?></a>
		<?php endforeach; ?>
		<a href="<?php echo esc_url( home_url( '/projects/?project_type=pinui_binui' ) ); ?>"><?php nadlan_e( 'pinui' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/projects/?project_type=tama38' ) ); ?>"><?php nadlan_e( 'tama' ); ?></a>
	</div></details>
	<details><summary><?php nadlan_e( 'm_prices' ); ?></summary><div class="nlhv2-mega">
		<a href="<?php echo esc_url( home_url( '/apartment-prices/' ) ); ?>"><b><?php nadlan_e( 'prices_index' ); ?></b></a>
		<a href="<?php echo esc_url( home_url( '/property-value-estimator/' ) ); ?>"><b><?php nadlan_e( 'my_value' ); ?></b></a>
		<a href="<?php echo esc_url( home_url( '/tel-aviv-apartment-prices/' ) ); ?>"><?php nadlan_e( 'prices_in' ); ?>תל אביב</a>
		<a href="<?php echo esc_url( home_url( '/jerusalem-apartment-prices/' ) ); ?>"><?php nadlan_e( 'prices_in' ); ?>ירושלים</a>
		<a href="<?php echo esc_url( home_url( '/herzliya-apartment-prices/' ) ); ?>"><?php nadlan_e( 'prices_in' ); ?>הרצליה</a>
		<a href="<?php echo esc_url( home_url( '/ramat-gan-apartment-prices/' ) ); ?>"><?php nadlan_e( 'prices_in' ); ?>רמת גן</a>
		<a href="<?php echo esc_url( home_url( '/netanya-apartment-prices/' ) ); ?>"><?php nadlan_e( 'prices_in' ); ?>נתניה</a>
	</div></details>
	<details><summary><?php nadlan_e( 'm_apts' ); ?></summary><div class="nlhv2-mega">
		<a href="<?php echo esc_url( home_url( '/properties/?listing_type=sale' ) ); ?>"><b><?php nadlan_e( 'apts_sale' ); ?></b></a>
		<a href="<?php echo esc_url( home_url( '/properties/?listing_type=rent' ) ); ?>"><b><?php nadlan_e( 'apts_rent' ); ?></b></a>
		<?php foreach ( $cities as $c ) : ?>
		<a href="<?php echo esc_url( home_url( '/properties/?city=' . rawurlencode( $c['name'] ) ) ); ?>"><?php nadlan_e( 'apts_in' ); ?><?php echo esc_html( $c['name'] ); ?></a>
		<?php endforeach; ?>
		<a href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>" class="nlhv2-mega-cta"><?php nadlan_e( 'post_free' ); ?></a>
	</div></details>
	<details><summary><?php nadlan_e( 'm_tours' ); ?></summary><div class="nlhv2-mega">
		<a href="<?php echo esc_url( home_url( '/tours/' ) ); ?>"><b><?php nadlan_e( 'tours_all' ); ?></b></a>
		<a href="<?php echo esc_url( home_url( '/tour/sde-dov/' ) ); ?>"><?php nadlan_e( 'tour_sd' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/tour/somail/' ) ); ?>"><?php nadlan_e( 'tour_so' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/earth/sde-dov/' ) ); ?>"><?php nadlan_e( 'tour_esd' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/earth/somail/' ) ); ?>"><?php nadlan_e( 'tour_eso' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/tour/designer/' ) ); ?>"><?php nadlan_e( 'tour_des' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/premium/' ) ); ?>"><?php nadlan_e( 'tour_catalog' ); ?></a>
	</div></details>
	<details><summary><?php nadlan_e( 'm_guides' ); ?></summary><div class="nlhv2-mega">
		<a href="<?php echo esc_url( home_url( '/guides/' ) ); ?>"><b><?php nadlan_e( 'guides_all' ); ?></b></a>
		<a href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>"><?php nadlan_e( 'calc_mortgage' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/purchase-tax-calculator/' ) ); ?>"><?php nadlan_e( 'calc_tax' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/apartment-purchase-cost-calculator/' ) ); ?>"><?php nadlan_e( 'calc_full' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/property-value-estimator/' ) ); ?>"><?php nadlan_e( 'value' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/buying-apartment/' ) ); ?>"><?php nadlan_e( 'buying_guide' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/tabu-extract-check/' ) ); ?>"><?php nadlan_e( 'tabu' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/investment/' ) ); ?>"><?php nadlan_e( 'invest' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/glossary/' ) ); ?>"><?php nadlan_e( 'glossary' ); ?></a>
	</div></details>
	<details><summary><?php nadlan_e( 'm_pros' ); ?></summary><div class="nlhv2-mega">
		<a href="<?php echo esc_url( home_url( '/professionals/' ) ); ?>"><b><?php nadlan_e( 'all_pros' ); ?></b></a>
		<?php foreach ( array_slice( (array) $profs, 0, 10, true ) as $key => $pm ) : ?>
		<a href="<?php echo esc_url( home_url( '/professionals/?profession=' . rawurlencode( $key ) ) ); ?>"><?php echo esc_html( is_array( $pm ) ? ( $pm['label'] ?? $key ) : $key ); ?></a>
		<?php endforeach; ?>
		<a href="<?php echo esc_url( home_url( '/advertise/' ) ); ?>" class="nlhv2-mega-cta"><?php nadlan_e( 'join_dir' ); ?></a>
	</div></details>
	<?php /* V7: the two theme-nav destinations without a group of their own —
	   plain links so nothing the old row offered disappears from the homepage */ ?>
	<a class="nlhv2-plain" href="<?php echo esc_url( home_url( '/sde-dov/' ) ); ?>"><?php nadlan_e( 'nav_areas' ); ?></a>
	<a class="nlhv2-plain" href="<?php echo esc_url( home_url( '/global/' ) ); ?>"><?php nadlan_e( 'nav_global' ); ?></a>
</nav>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_hero' ) ) {
	function nadlan_hv2_band_hero() {
		$counts = array(
			'projects'      => function_exists( 'nadlan_unit_journey_public_project_count' )
				? nadlan_unit_journey_public_project_count()
				: (int) wp_count_posts( 'nadlan_project' )->publish,
			'professionals' => (int) wp_count_posts( 'nadlan_professional' )->publish,
		);
		$cities = nadlan_hv2_cities( 12 );
		$flag   = nadlan_hv2_featured_projects( 1 );
		$flag   = $flag ? $flag[0] : null;
		?>
	<?php $aerial = trim( (string) get_option( 'nadlan_home_hero_aerial', '' ) ); ?>
	<section class="nlhv2-hero nlhv2-hero--map<?php echo $aerial ? ' nlhv2-hero--aerial' : ''; ?>">
		<?php if ( $aerial ) : ?>
		<?php /* owner 2026-07-12: the black live map was hard to read (mobile most of
		        all); the hero is an impressive AERIAL IMAGE - fast, legible, cinematic.
		        The LIVE map moved to its own light band lower on the page. */ ?>
		<div class="nlhv2-hero-mapbg" style="background-image:url('<?php echo esc_url( $aerial ); ?>')" aria-hidden="true">
			<div class="nlhv2-hero-veil" aria-hidden="true"></div>
		</div>
		<?php elseif ( function_exists( 'nadlan_drone_map_band' ) ) : ?>
		<div class="nlhv2-hero-mapbg" aria-hidden="false">
			<?php echo nadlan_drone_map_band( 'hero', function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
			<div class="nlhv2-hero-veil" aria-hidden="true"></div>
		</div>
		<?php endif; ?>
		<div class="nlhv2-hero-copy">
			<h1><?php nadlan_e( 'hero_h1' ); ?></h1>
			<p class="nlhv2-sub"><?php nadlan_e( 'hero_sub' ); ?></p>
			<form class="nlhv2-search" action="<?php echo esc_url( home_url( '/properties/' ) ); ?>" method="get" role="search">
				<div class="nlhv2-tabs" role="tablist">
					<button type="button" class="is-on" data-action="<?php echo esc_url( home_url( '/properties/' ) ); ?>" data-extra="listing_type=sale"><?php nadlan_e( 'tab_buy' ); ?></button>
					<button type="button" data-action="<?php echo esc_url( home_url( '/properties/' ) ); ?>" data-extra="listing_type=rent"><?php nadlan_e( 'tab_rent' ); ?></button>
					<button type="button" data-action="<?php echo esc_url( home_url( '/projects/' ) ); ?>" data-extra=""><?php nadlan_e( 'tab_projects' ); ?></button>
					<button type="button" data-action="<?php echo esc_url( home_url( '/professionals/' ) ); ?>" data-extra=""><?php nadlan_e( 'tab_pros' ); ?></button>
				</div>
				<div class="nlhv2-box">
					<input type="search" name="q" list="nlhv2-cities" placeholder="<?php echo esc_attr( nadlan_i18n( 'search_ph' ) ); ?>" aria-label="<?php echo esc_attr( nadlan_i18n( 'search_btn' ) ); ?>">
					<datalist id="nlhv2-cities"><?php foreach ( $cities as $c ) { echo '<option value="' . esc_attr( $c['name'] ) . '">'; } ?></datalist>
					<button type="submit"><?php nadlan_e( 'search_btn' ); ?></button>
				</div>
			</form>
			<div class="nlhv2-trust">
				<a href="<?php echo esc_url( home_url( '/projects/' ) ); ?>"><b><?php echo number_format( $counts['projects'] ); ?></b> <?php nadlan_e( 'trust_projects' ); ?></a>
				<a href="<?php echo esc_url( home_url( '/professionals/' ) ); ?>"><b><?php echo number_format( $counts['professionals'] ); ?></b> <?php nadlan_e( 'trust_pros' ); ?></a>
				<a href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>"><b>5</b> <?php nadlan_e( 'trust_calc' ); ?></a>
				<a href="<?php echo esc_url( home_url( '/professionals/?profession=lawyer' ) ); ?>"><b><?php nadlan_e( 'trust_law_pre' ); ?></b> <?php nadlan_e( 'trust_law' ); ?></a>
			</div>
		</div>
		<?php // hero media retired 2026-07-07: the live night map IS the hero (the promo video moved to its own band below) ?>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_video' ) ) {
	function nadlan_hv2_band_video() {
		$embed = nadlan_hv2_video_embed();
		if ( ! $embed ) { return; }
		echo '<section class="nlhv2-band nlhv2-videoband" aria-label="סרטון היכרות"><header><p class="nlhv2-kicker">רגע לפני שמתחילים</p><h2>ככה בוחרים דירה בנדלן</h2></header><div class="nlhv2-video-frame">' . $embed . '</div></section>'; // phpcs:ignore
	}
}

/* The embed builder, split out of the band so the tour+video pair can reuse it
   verbatim (owner 2026-07-29: the video rides beside the tour under the hero). */
if ( ! function_exists( 'nadlan_hv2_video_embed' ) ) {
	function nadlan_hv2_video_embed() {
		$url = trim( (string) get_option( 'nadlan_home_video_url', '' ) );
		if ( ! $url ) { return ''; }
		$embed = '';
		if ( preg_match( '~(?:youtube\.com/(?:watch\?v=|shorts/|embed/)|youtu\.be/)([A-Za-z0-9_-]{6,20})~', $url, $m ) ) {
			$embed = '<iframe src="https://www.youtube-nocookie.com/embed/' . esc_attr( $m[1] ) . '?rel=0&amp;modestbranding=1" title="נדלן - סרטון" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
		} elseif ( preg_match( '~vimeo\.com/(\d+)~', $url, $m ) ) {
			$embed = '<iframe src="https://player.vimeo.com/video/' . esc_attr( $m[1] ) . '" title="נדלן - סרטון" loading="lazy" allowfullscreen></iframe>';
		} elseif ( preg_match( '~\.(mp4|webm)(\?|$)~i', $url ) ) {
			// gif-like, poster-backed: a controls-only mp4 rendered as a huge
			// black rectangle before play (owner sweep 2026-07-07)
			$poster = trim( (string) get_option( 'nadlan_home_video_poster', '' ) );
			$embed  = '<video muted autoplay loop playsinline preload="metadata"' . ( $poster ? ' poster="' . esc_url( $poster ) . '"' : '' ) . '><source src="' . esc_url( $url ) . '"></video>';
		}
		return $embed;
	}
}

/* THE PAIR (owner 2026-07-29): the 3D quarter tour leads the page with the intro
   video beside it, directly under the hero. Either half may be missing - the
   survivor then takes the full width, and if both are gone nothing renders. */
if ( ! function_exists( 'nadlan_hv2_band_tourvideo' ) ) {
	function nadlan_hv2_band_tourvideo() {
		$lang  = function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he';
		$tour  = ( function_exists( 'nadlan_sdedov_tour_band' ) && 'he' === $lang ) ? nadlan_sdedov_tour_band( 'pair' ) : '';
		$embed = nadlan_hv2_video_embed();
		if ( '' === $tour && '' === $embed ) { return; }
		$solo = ( '' === $tour || '' === $embed ) ? ' is-solo' : '';
		echo '<section class="nlhv2-band nlhv2-tourvideo' . esc_attr( $solo ) . '" aria-label="סיור תלת ממדי וסרטון היכרות">'; // phpcs:ignore
		if ( '' !== $tour ) { echo $tour; } // phpcs:ignore
		if ( '' !== $embed ) {
			echo '<div class="nlhv2-tvvid"><div class="nlhv2-video-frame">' . $embed . '</div><p class="nlhv2-note">ככה בוחרים דירה בנדלן</p></div>'; // phpcs:ignore
		}
		echo '</section>';
	}
}

if ( ! function_exists( 'nadlan_hv2_band_dronemap' ) ) {
	/* the LIVE map as its own designed band (light style; the hero is aerial imagery) */
	function nadlan_hv2_band_dronemap() {
		if ( ! function_exists( 'nadlan_drone_map_band' ) ) { return; }
		echo '<section class="nlhv2-band nlhv2-dronemap" id="nlhv2-map">';
		echo nadlan_drone_map_band( 'showcase', function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he' ); // phpcs:ignore WordPress.Security.EscapeOutput
		echo '</section>';
	}
}

if ( ! function_exists( 'nadlan_hv2_band_renewal' ) ) {
	/* the urban renewal PRODUCT on the homepage (owner 2026-07-12): the room is
	   a product, not a page - it earns a band like the flagships do. */
	function nadlan_hv2_band_renewal() {
		?>
	<?php $ur_img = trim( (string) get_option( 'nadlan_ur_band_img', '' ) ); ?>
	<section class="nlhv2-band nlhv2-renewal<?php echo $ur_img ? ' has-img' : ''; ?>">
		<?php if ( $ur_img ) : ?><div class="nlhv2-band-art" style="background-image:url(<?php echo esc_url( $ur_img ); ?>)" role="img" aria-label=""></div><?php endif; ?>
		<div class="nlhv2-renewal-in">
			<p class="nlhv2-kicker nlhv2-renewal-k"><?php nadlan_e( 'ur_kicker' ); ?></p>
			<h2><?php nadlan_e( 'ur_title' ); ?></h2>
			<p class="nlhv2-renewal-sub"><?php nadlan_e( 'ur_sub' ); ?></p>
			<div class="nlhv2-renewal-steps">
				<span><i>1</i><?php nadlan_e( 'ur_step1' ); ?></span>
				<span><i>2</i><?php nadlan_e( 'ur_step2' ); ?></span>
				<span><i>3</i><?php nadlan_e( 'ur_step3' ); ?></span>
			</div>
			<div class="nlhv2-renewal-ctas">
				<a class="nlhv2-renewal-go" href="<?php echo esc_url( home_url( '/urban-renewal/check/' ) ); ?>"><?php nadlan_e( 'ur_cta1' ); ?></a>
				<a class="nlhv2-renewal-alt" href="<?php echo esc_url( home_url( '/my-renewal/' ) ); ?>"><?php nadlan_e( 'ur_cta2' ); ?></a>
			</div>
			<p class="nlhv2-renewal-note"><?php nadlan_e( 'ur_note' ); ?></p>
		</div>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_rentals' ) ) {
	/* rentals manager on the homepage - LIGHT band (the de-darken law) */
	function nadlan_hv2_band_rentals() {
		if ( ! function_exists( 'nadlan_rm_on' ) || ! nadlan_rm_on() ) { return; }
		?>
	<?php $rm_img = trim( (string) get_option( 'nadlan_rm_band_img', '' ) ); ?>
	<section class="nlhv2-band nlhv2-rentals<?php echo $rm_img ? ' has-img' : ''; ?>">
		<?php if ( $rm_img ) : ?><div class="nlhv2-band-art" style="background-image:url(<?php echo esc_url( $rm_img ); ?>)" role="img" aria-label=""></div><?php endif; ?>
		<div class="nlhv2-rentals-in">
			<p class="nlhv2-kicker"><?php nadlan_e( 'rm_kicker' ); ?></p>
			<h2><?php nadlan_e( 'rm_title' ); ?></h2>
			<p class="nlhv2-rentals-sub"><?php nadlan_e( 'rm_sub' ); ?></p>
			<div class="nlhv2-renewal-steps nlhv2-rentals-steps">
				<span><i>1</i><?php nadlan_e( 'rm_step1' ); ?></span>
				<span><i>2</i><?php nadlan_e( 'rm_step2' ); ?></span>
				<span><i>3</i><?php nadlan_e( 'rm_step3' ); ?></span>
			</div>
			<div class="nlhv2-renewal-ctas">
				<a class="nlhv2-renewal-go" href="<?php echo esc_url( home_url( '/my-rentals/' ) ); ?>"><?php nadlan_e( 'rm_cta' ); ?></a>
			</div>
			<p class="nlhv2-rentals-note"><?php nadlan_e( 'rm_note' ); ?></p>
		</div>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_flagships' ) ) {
	/* The differentiator band (owner audit 2026-07-06): the four flagship 3D
	   projects, right under the hero. Hero plates + 3D badge; every card links
	   into the full showroom. Cards render only for slugs that exist. */
	function nadlan_hv2_band_flagships() {
		$slugs = array( 'rainbow-tel-aviv', 'ashira-sde-dov', 'dimri-yama-sde-dov', 'duo-tel-aviv' );
		$cards = array();
		foreach ( $slugs as $slug ) {
			$p = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
			if ( $p && get_post_status( $p ) === 'publish' ) { $cards[] = $p; }
		}
		if ( count( $cards ) < 2 ) { return; }
		/* THE SHOWCASE (owner 2026-07-11, per the approved
		   docs/previews/nadlan-homepage-target.html): the band under the map
		   hero is a LIVE auto-rotating model of a flagship, with selector
		   cards that swap the stage. Perf laws: model-viewer boots only when
		   the band nears the viewport (IntersectionObserver), the poster is a
		   CSS background BEHIND a transparent viewer (burned-in lesson), and
		   phones show the poster with an explicit tap-to-spin. */
		$show = array();
		foreach ( $cards as $p ) {
			$glb = esc_url( (string) get_post_meta( $p->ID, 'project_model_glb', true ) );
			if ( '' === $glb ) { continue; } // showcase carries REAL models only
			$show[] = array(
				'glb'    => $glb,
				'poster' => esc_url( (string) get_post_meta( $p->ID, 'project_model_poster', true ) ),
				'img'    => esc_url( (string) get_post_meta( $p->ID, 'project_3d_image', true ) ),
				'href'   => get_permalink( $p ),
				'title'  => get_the_title( $p ),
				'city'   => (string) get_post_meta( $p->ID, 'city', true ),
				'floors' => (int) get_post_meta( $p->ID, 'floors', true ),
				'units'  => (int) get_post_meta( $p->ID, 'num_units', true ),
			);
		}
		if ( count( $show ) < 2 ) { return; }
		$first = $show[0];
		/* the flagship IDs are handed to the projects band so it never repeats them */
		$GLOBALS['nadlan_hv2_shown_ids'] = wp_list_pluck( $cards, 'ID' );
		?>
	<section class="nlhv2-band nlhv2-flagships">
		<header><p class="nlhv2-kicker"><?php nadlan_e( 'fl_kicker' ); ?></p><h2><?php nadlan_e( 'fl_title' ); ?></h2>
			<a href="<?php echo esc_url( home_url( '/premium/' ) ); ?>"><?php nadlan_e( 'fl_all' ); ?></a></header>
		<p class="nlhv2-flagsub"><?php nadlan_e( 'fl_sub' ); ?>
			<a class="nlhv2-flagdev" href="<?php echo esc_url( home_url( '/advertise/' ) ); ?>"><?php nadlan_e( 'fl_dev' ); ?> ←</a></p>
		<div class="nlhv2-show">
			<div class="nlhv2-show-stage" id="nlhv2-shstage" data-glb="<?php echo esc_attr( $first['glb'] ); ?>"<?php echo $first['poster'] ? ' style="background-image:url(' . esc_url( $first['poster'] ) . ')"' : ''; ?>>
				<button class="nlhv2-show-spin" id="nlhv2-shspin" type="button"><?php nadlan_e( 'sh_spin' ); ?></button>
				<span class="nlhv2-show-chip"><?php nadlan_e( 'sh_chip' ); ?></span>
				<a class="nlhv2-show-go" id="nlhv2-shgo" href="<?php echo esc_url( $first['href'] ); ?>"><?php nadlan_e( 'fl_go' ); ?></a>
			</div>
			<div class="nlhv2-show-cards" id="nlhv2-shcards">
				<?php foreach ( $show as $i => $f ) : ?>
				<button type="button" class="nlhv2-shcard<?php echo 0 === $i ? ' is-on' : ''; ?>" data-glb="<?php echo esc_attr( $f['glb'] ); ?>" data-poster="<?php echo esc_attr( $f['poster'] ); ?>" data-href="<?php echo esc_url( $f['href'] ); ?>">
					<span class="nlhv2-shcard-media">
						<?php if ( $f['img'] || $f['poster'] ) : ?><img src="<?php echo esc_url( $f['img'] ? $f['img'] : $f['poster'] ); ?>" alt="<?php echo esc_attr( $f['title'] ); ?>" loading="lazy"><?php endif; ?>
						<i class="nlhv2-tag nlhv2-tag--3d">3D</i>
						<?php if ( $f['city'] ) : ?><i class="nlhv2-tag"><?php echo esc_html( $f['city'] ); ?></i><?php endif; ?>
					</span>
					<span class="nlhv2-shcard-body">
						<b dir="auto"><?php echo esc_html( $f['title'] ); ?></b>
						<span class="nlhv2-chiprow">
							<?php if ( $f['floors'] ) : ?><i><?php echo (int) $f['floors']; ?> <?php nadlan_e( 'sh_floors' ); ?></i><?php endif; ?>
							<?php if ( $f['units'] ) : ?><i><?php echo number_format( $f['units'] ); ?> <?php nadlan_e( 'ar_apts' ); ?></i><?php endif; ?>
						</span>
					</span>
				</button>
				<?php endforeach; ?>
			</div>
		</div>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_market' ) ) {
	function nadlan_hv2_band_market() {
		/* THE DATA PANEL (owner decision 7, 2026-07-07): official CBS figures
		 * only, dated, sourced - or nothing. Defaults = CBS release 150/2026
		 * (15 May 2026): average free-market transaction price per dwelling,
		 * Q1 2026, by large city. CMS-editable via option nadlan_market_cbs. */
		$d = (array) get_option( 'nadlan_market_cbs', array() );
		$cities = isset( $d['cities'] ) && is_array( $d['cities'] ) && $d['cities'] ? $d['cities'] : array(
			array( 'תל אביב-יפו', 4594.5 ),
			array( 'הרצליה', 3849.4 ),
			array( 'ירושלים', 3096.2 ),
			array( 'רמת גן', 3028.8 ),
			array( 'חיפה', 1805.2 ),
			array( 'באר שבע', 1241.4 ),
		);
		$period = ! empty( $d['period'] ) ? $d['period'] : 'רבעון 1, 2026';
		$src    = ! empty( $d['source_url'] ) ? $d['source_url'] : 'https://www.cbs.gov.il/he/mediarelease/Madad/DocLib/2026/150/10_26_150b.pdf';
		$yoy    = ! empty( $d['index_yoy'] ) ? $d['index_yoy'] : '-1.3%';
		$max = 0.0;
		foreach ( $cities as $c ) { $max = max( $max, (float) $c[1] ); }
		if ( $max <= 0 ) { return; }
		echo '<section class="nlhv2-band"><header><h2>' . esc_html( nadlan_i18n( 'mk_title' ) ) . '</h2><span class="nlhv2-note">מחיר ממוצע לדירה בשוק החופשי · ' . esc_html( $period ) . '</span></header>';
		echo '<div class="nlhv2-cbs"><div class="nlhv2-cbs-bars">';
		foreach ( array_slice( $cities, 0, 6 ) as $i => $c ) {
			$h = max( 8, round( (float) $c[1] / $max * 100 ) );
			$m = round( (float) $c[1] / 1000, 2 );
			echo '<div class="nlhv2-cbs-bar' . ( 0 === $i ? ' is-top' : '' ) . '"><b>₪' . esc_html( number_format( $m, $m < 10 ? 2 : 1 ) ) . 'M</b><i style="height:' . (int) $h . '%"></i><span>' . esc_html( $c[0] ) . '</span></div>';
		}
		echo '</div><p class="nlhv2-cbs-src">שינוי מדד מחירי הדירות בשנה האחרונה: ' . esc_html( $yoy ) . ' · המקור: <a href="' . esc_url( $src ) . '" target="_blank" rel="noopener">הלשכה המרכזית לסטטיסטיקה</a> · מתעדכן רבעונית</p></div></section>';
	}
}

if ( ! function_exists( 'nadlan_hv2_band_projects' ) ) {
	function nadlan_hv2_band_projects() {
		$shown    = isset( $GLOBALS['nadlan_hv2_shown_ids'] ) ? (array) $GLOBALS['nadlan_hv2_shown_ids'] : array();
		$projects = nadlan_hv2_image_projects( 3, $shown );
		/* an empty tile is worse than no band: under two real pictures, stay silent */
		if ( count( $projects ) < 2 ) { return; }
		?>
	<section class="nlhv2-dark">
		<header><p class="nlhv2-kicker"><?php nadlan_e( 'pj_kicker' ); ?></p><h2><?php nadlan_e( 'pj_title' ); ?></h2>
			<a class="nlhv2-dark-all" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>"><?php nadlan_e( 'pj_all' ); ?></a></header>
		<div class="nlhv2-projgrid">
			<?php foreach ( $projects as $p ) :
				$img = nadlan_hv2_img( $p->ID );
				$is_poster = $img && $img === (string) get_post_meta( $p->ID, 'project_model_poster', true );
				$glb = (string) get_post_meta( $p->ID, 'project_model_glb', true );
				$pp  = (int) get_post_meta( $p->ID, 'project_3d_avg_price_per_sqm', true );
				$units = json_decode( (string) get_post_meta( $p->ID, 'project_3d_units', true ), true );
				$un = is_array( $units ) ? count( $units ) : 0; ?>
			<div class="nlhv2-proj">
				<a class="nlhv2-proj-media" href="<?php echo esc_url( get_permalink( $p ) ); ?>"<?php echo $img ? ' style="background-image:url(' . esc_url( $img ) . ')"' : ''; ?> data-glb="<?php echo esc_url( $glb ); ?>" data-poster="<?php echo esc_url( $img ); ?>">
					<em><?php nadlan_e( 'pj_pick' ); ?></em>
				</a>
				<div class="nlhv2-proj-body">
					<b><?php echo esc_html( get_the_title( $p ) ); ?></b>
					<span><?php echo esc_html( get_post_meta( $p->ID, 'city', true ) ); ?><?php echo $un ? ' · ' . (int) $un . ' ' . nadlan_i18n( 'pj_units_pick' ) : ''; ?></span>
					<?php if ( $pp ) : ?><i><?php nadlan_e( 'pj_est_pre' ); ?><?php echo number_format( $pp ); ?> <?php nadlan_e( 'pj_est_suf' ); ?></i><?php endif; ?>
					<?php if ( $glb ) : ?><button type="button" class="nlhv2-proj-live" data-glb="<?php echo esc_url( $glb ); ?>" data-title="<?php echo esc_attr( get_the_title( $p ) ); ?>"><?php nadlan_e( 'pj_live' ); ?></button><?php endif; ?>
					<?php if ( function_exists( 'nadlan_sdedov_card_tour_btn' ) ) { echo nadlan_sdedov_card_tour_btn( $p ); } // phpcs:ignore ?>
				</div>
			</div>
			<?php endforeach; ?>
		</div>
		<div class="nlhv2-viewerwrap" id="nlhv2-viewerwrap" hidden><div id="nlhv2-viewer-slot"></div><p class="nlhv2-note"><?php nadlan_e( 'pj_viewer_note' ); ?></p></div>
		<p class="nlhv2-note nlhv2-dark-note"><?php nadlan_e( 'pj_dark_note' ); ?></p>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_listings' ) ) {
	function nadlan_hv2_band_listings() {
		$grab = function ( $type ) {
			return get_posts( array( 'post_type' => 'nadlan_property', 'posts_per_page' => 4, 'no_found_rows' => true,
				'meta_query' => array( array( 'key' => 'listing_type', 'value' => $type ) ) ) );
		};
		$sale = $grab( 'sale' ); $rent = $grab( 'rent' );
		if ( ! $sale && ! $rent ) { $sale = get_posts( array( 'post_type' => 'nadlan_property', 'posts_per_page' => 4, 'no_found_rows' => true ) ); }
		if ( ! $sale && ! $rent ) { return; }
		$cities = nadlan_hv2_cities( 8 );
		$card = function ( $l ) {
			/* PORTAL-GRADE RESKIN (owner 2026-07-29): price big and first
			   (tabular numbers), ONE quiet city-rooms-sqm-floor line, the
			   facility chips, and a real visual - never the sketch plate.
			   Same structure and count as before: a reskin, not a rebuild. */
			list( $img, $src ) = nadlan_hv2_listing_media( $l->ID );
			$pr = (int) get_post_meta( $l->ID, 'price', true ); $rm = (float) get_post_meta( $l->ID, 'rooms', true );
			$sq = (int) get_post_meta( $l->ID, 'size_sqm', true ); $fl = get_post_meta( $l->ID, 'floor', true );
			$city = (string) get_post_meta( $l->ID, 'city', true );
			echo '<a class="nlhv2-list" href="' . esc_url( get_permalink( $l ) ) . '">';
			echo '<span class="nlhv2-list-media' . ( '' === $img ? ' nlfc-ph' : '' ) . '">' .
				( $img ? '<img src="' . esc_url( $img ) . '" alt="' . esc_attr( get_the_title( $l ) ) . '" loading="lazy" decoding="async">' : '<i class="nlfc-ph-mark" aria-hidden="true">נדלן</i>' ) .
				( 'interior' === $src ? '<i class="nlfc-imgtag">הדמיה</i>' : '' ) .
			'</span>';
			echo '<b class="nlfc-price">' . ( $pr ? number_format( $pr ) . ' ₪' : esc_html( get_the_title( $l ) ) ) . '</b>';
			$bits = array_filter( array(
				$city,
				$rm ? rtrim( rtrim( number_format( $rm, 1 ), '0' ), '.' ) . ' ' . nadlan_i18n( 'u_rooms' ) : '',
				$sq ? $sq . ' ' . nadlan_i18n( 'u_sqm' ) : '',
				$fl !== '' && $fl !== null ? nadlan_i18n( 'u_floor' ) . ' ' . (string) $fl : '',
			) );
			if ( $bits ) { echo '<span class="nlfc-line">' . esc_html( implode( ' · ', $bits ) ) . '</span>'; }
			// facility chips carry Hebrew labels - Hebrew homepage only (the nlsdt-band rule)
			$fc_he = ! function_exists( 'nadlan_current_lang' ) || 'he' === nadlan_current_lang();
			if ( $fc_he && function_exists( 'nadlan_fc_for_property' ) && ( $fk = nadlan_fc_for_property( $l->ID ) ) ) {
				echo nadlan_fc_chips_html( $fk, array( 'limit' => 3, 'link' => false, 'class' => 'nlfc-onlist' ) ); // phpcs:ignore WordPress.Security.EscapeOutput
			}
			echo '</a>';
		};
		?>
	<section class="nlhv2-band nlhv2-alt">
		<header><p class="nlhv2-kicker"><?php nadlan_e( 'ls_kicker' ); ?></p><h2><?php nadlan_e( 'ls_title' ); ?></h2>
			<a href="<?php echo esc_url( home_url( '/properties/' ) ); ?>"><?php nadlan_e( 'ls_all' ); ?></a></header>
		<div class="nlhv2-listtabs nl-tabs"><button type="button" class="is-on" data-pane="sale"><?php nadlan_e( 'tab_buy' ); ?></button><button type="button" data-pane="rent"><?php nadlan_e( 'tab_rent' ); ?></button></div>
		<div class="nlhv2-listgrid" data-pane-id="sale"<?php echo $sale ? '' : ' hidden'; ?>>
			<?php foreach ( $sale as $l ) { $card( $l ); } ?>
			<a class="nlhv2-list nlhv2-cta-tile" href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>"><b><?php nadlan_e( 'ls_cta_b' ); ?></b><span><?php nadlan_e( 'ls_cta_s' ); ?></span></a>
		</div>
		<div class="nlhv2-listgrid" data-pane-id="rent" hidden>
			<?php foreach ( $rent as $l ) { $card( $l ); } ?>
			<a class="nlhv2-list nlhv2-cta-tile" href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>"><b><?php nadlan_e( 'ls_cta_b' ); ?></b><span><?php nadlan_e( 'ls_cta_s' ); ?></span></a>
		</div>
		<?php if ( $cities ) : ?>
		<p class="nlhv2-cityrow"><?php foreach ( $cities as $c ) : ?><a href="<?php echo esc_url( home_url( '/properties/?city=' . rawurlencode( $c['name'] ) ) ); ?>"><?php nadlan_e( 'ls_city_pre' ); ?><?php echo esc_html( $c['name'] ); ?></a><?php endforeach; ?></p>
		<?php endif; ?>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_areas' ) ) {
	function nadlan_hv2_band_areas() {
		$cities = nadlan_hv2_cities( 8 );
		if ( count( $cities ) < 3 ) { return; }
		?>
	<section class="nlhv2-band">
		<header><p class="nlhv2-kicker"><?php nadlan_e( 'ar_kicker' ); ?></p><h2><?php nadlan_e( 'ar_title' ); ?></h2></header>
		<div class="nlhv2-areas">
			<?php foreach ( $cities as $c ) : ?>
			<a href="<?php echo esc_url( home_url( $c['projects'] >= $c['properties'] ? '/projects/?city=' . rawurlencode( $c['name'] ) : '/properties/?city=' . rawurlencode( $c['name'] ) ) ); ?>">
				<b><?php echo esc_html( $c['name'] ); ?></b>
				<span><?php echo $c['projects'] ? ( 1 === (int) $c['projects'] ? esc_html( nadlan_i18n( 'ar_project_one' ) ) : (int) $c['projects'] . ' ' . nadlan_i18n( 'ar_projects' ) ) : ''; ?><?php echo $c['projects'] && $c['properties'] ? ' · ' : ''; ?><?php echo $c['properties'] ? ( 1 === (int) $c['properties'] ? esc_html( nadlan_i18n( 'ar_apt_one' ) ) : (int) $c['properties'] . ' ' . nadlan_i18n( 'ar_apts' ) ) : ''; ?></span>
			</a>
			<?php endforeach; ?>
		</div>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_magazine' ) ) {
	function nadlan_hv2_band_magazine() {
		// Hebrew homepage: only the news category feeds this band. The EN cluster
		// (category "english") stays out so English headlines never mix in.
		$posts = get_posts( array( 'post_type' => 'post', 'posts_per_page' => 5, 'no_found_rows' => true,
			'category_name' => 'nadlan-news',
			'date_query' => array( array( 'after' => '120 days ago' ) ) ) );
		if ( count( $posts ) < 3 ) { return; } // spec: an empty news band is worse than none
		$lead = array_shift( $posts );
		$img  = get_the_post_thumbnail_url( $lead->ID, 'large' );
		?>
	<section class="nlhv2-band nlhv2-alt">
		<header><p class="nlhv2-kicker"><?php nadlan_e( 'mg_kicker' ); ?></p><h2><?php nadlan_e( 'mg_title' ); ?></h2></header>
		<div class="nlhv2-mag">
			<a class="nlhv2-mag-lead" href="<?php echo esc_url( get_permalink( $lead ) ); ?>">
				<span class="nlhv2-list-media<?php echo $img && preg_match( '/\.svg(\?|$)/i', $img ) ? ' is-sketch' : ''; ?>"<?php echo $img ? ' style="background-image:url(' . esc_url( $img ) . ')"' : ''; ?>></span>
				<b><?php echo esc_html( get_the_title( $lead ) ); ?></b>
				<span><?php echo esc_html( get_the_date( 'd/m/Y', $lead ) ); ?></span>
			</a>
			<div class="nlhv2-mag-rows">
				<?php foreach ( $posts as $po ) : ?>
				<a href="<?php echo esc_url( get_permalink( $po ) ); ?>"><b><?php echo esc_html( get_the_title( $po ) ); ?></b><span><?php echo esc_html( get_the_date( 'd/m/Y', $po ) ); ?></span></a>
				<?php endforeach; ?>
			</div>
			<div class="nlhv2-mag-rail">
				<p><?php nadlan_e( 'mg_rail' ); ?></p>
				<a href="<?php echo esc_url( home_url( '/buying-apartment/' ) ); ?>"><?php nadlan_e( 'guide_buy' ); ?></a>
				<a href="<?php echo esc_url( home_url( '/tabu-extract-check/' ) ); ?>"><?php nadlan_e( 'tabu' ); ?></a>
				<a href="<?php echo esc_url( home_url( '/investment/' ) ); ?>"><?php nadlan_e( 'invest' ); ?></a>
				<a href="<?php echo esc_url( home_url( '/glossary/' ) ); ?>"><?php nadlan_e( 'glossary' ); ?></a>
			</div>
		</div>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_tools' ) ) {
	function nadlan_hv2_band_tools() {
		?>
	<section class="nlhv2-band">
		<header><p class="nlhv2-kicker"><?php nadlan_e( 'tl_kicker' ); ?></p><h2><?php nadlan_e( 'tl_title' ); ?></h2></header>
		<div class="nlhv2-tools">
			<a class="nlhv2-tool-lead" href="<?php echo esc_url( home_url( '/property-value-estimator/' ) ); ?>"><b><?php nadlan_e( 'tl_lead_b' ); ?></b><span><?php nadlan_e( 'tl_lead_s' ); ?></span></a>
			<a href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>"><b><?php nadlan_e( 'calc_mortgage' ); ?></b><span><?php nadlan_e( 'tl_mort_s' ); ?></span></a>
			<a href="<?php echo esc_url( home_url( '/purchase-tax-calculator/' ) ); ?>"><b><?php nadlan_e( 'tl_tax_b' ); ?></b><span><?php nadlan_e( 'tl_tax_s' ); ?></span></a>
			<a href="<?php echo esc_url( home_url( '/apartment-purchase-cost-calculator/' ) ); ?>"><b><?php nadlan_e( 'calc_full' ); ?></b><span><?php nadlan_e( 'tl_full_s' ); ?></span></a>
			<a href="<?php echo esc_url( home_url( '/glossary/' ) ); ?>"><b><?php nadlan_e( 'glossary' ); ?></b><span><?php nadlan_e( 'tl_glos_s' ); ?></span></a>
		</div>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_pros' ) ) {
	function nadlan_hv2_band_pros() {
		$cats = array(
			'lawyer'    => nadlan_i18n( 'pr_lawyer' ),
			'shamai'    => nadlan_i18n( 'pr_shamai' ),
			'mashkanta' => nadlan_i18n( 'pr_mashkanta' ),
			'bedek_bait'=> nadlan_i18n( 'pr_bedek' ),
		);
		$total = (int) wp_count_posts( 'nadlan_professional' )->publish;
		$slots = array();
		foreach ( $cats as $key => $label ) {
			$s = nadlan_hv2_pro_slot( $key );
			if ( $s ) { $slots[ $key ] = $s + array( 'label' => $label ); }
		}
		if ( ! $slots ) { return; }
		?>
	<section class="nlhv2-band nlhv2-alt">
		<header><p class="nlhv2-kicker"><?php nadlan_e( 'pr_kicker' ); ?></p><h2><?php nadlan_e( 'pr_title' ); ?></h2>
			<a href="<?php echo esc_url( home_url( '/professionals/' ) ); ?>"><?php nadlan_e( 'pr_more_pre' ); ?> <?php echo number_format( $total ); ?> <?php nadlan_e( 'pr_more_suf' ); ?></a></header>
		<div class="nlhv2-prosgrid">
			<?php foreach ( $slots as $key => $s ) :
				$pid = $s['id'];
				$rating = (float) get_post_meta( $pid, 'rating', true );
				$pm = function_exists( 'nadlan_prof_meta_of' ) ? nadlan_prof_meta_of( $key ) : array( 'color' => '#1B1A17' ); ?>
			<a class="nlhv2-pro" href="<?php echo esc_url( get_permalink( $pid ) ); ?>">
				<?php if ( $s['sponsored'] ) : ?><i class="nlhv2-spon"><?php nadlan_e( 'pr_sponsored' ); ?></i><?php endif; ?>
				<?php echo function_exists( 'nadlan_prof_monogram_svg' ) ? nadlan_prof_monogram_svg( get_the_title( $pid ), $pm['color'] ?? '#1B1A17' ) : ''; // phpcs:ignore ?>
				<b><?php echo esc_html( get_the_title( $pid ) ); ?></b>
				<span><?php echo esc_html( $s['label'] ); ?><?php echo esc_html( ( $c = get_post_meta( $pid, 'city', true ) ) ? ' · ' . $c : '' ); ?><?php echo $rating ? ' · ★ ' . number_format( $rating, 1 ) : ''; ?></span>
			</a>
			<?php endforeach; ?>
			<a class="nlhv2-pro nlhv2-cta-tile" href="<?php echo esc_url( home_url( '/advertise/' ) ); ?>"><b><?php nadlan_e( 'pr_join_b' ); ?></b><span><?php nadlan_e( 'pr_join_s' ); ?></span></a>
		</div>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_intl' ) ) {
	function nadlan_hv2_band_intl() {
		if ( function_exists( 'nadlan_current_lang' ) && nadlan_current_lang() !== 'he' ) { return; }
		?>
	<section class="nlhv2-en" dir="ltr">
		<div>
			<p class="nlhv2-kicker" style="color:#C9A45C">International buyers</p>
			<h2>Buying property in Israel, guided in your language</h2>
			<p>New-build projects with apartment selection from inside the building, verified professionals and legal guidance for foreign buyers.</p>
		</div>
		<div class="nlhv2-en__links">
			<a href="<?php echo esc_url( home_url( '/en/' ) ); ?>">Explore in English →</a>
			<a href="<?php echo esc_url( home_url( '/en/buy-property-in-israel/' ) ); ?>">Buying from abroad: taxes, process, 3D apartments →</a>
		</div>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_megafooter' ) ) {
	function nadlan_hv2_band_megafooter() {
		$cities = nadlan_hv2_cities( 10 );
		$profs  = function_exists( 'nadlan_dir_professions_all' ) ? array_slice( (array) nadlan_dir_professions_all(), 0, 8, true ) : array();
		?>
	<section class="nlhv2-mfoot" dir="rtl" aria-label="כל הקישורים">
		<div class="nlhv2-mfoot-col"><p><?php nadlan_e( 'mf_apts_city' ); ?></p>
			<?php foreach ( $cities as $c ) : ?><a href="<?php echo esc_url( home_url( '/properties/?city=' . rawurlencode( $c['name'] ) ) ); ?>"><?php nadlan_e( 'apts_in' ); ?><?php echo esc_html( $c['name'] ); ?></a><?php endforeach; ?>
		</div>
		<div class="nlhv2-mfoot-col"><p><?php nadlan_e( 'mf_proj_city' ); ?></p>
			<?php foreach ( $cities as $c ) : if ( ! $c['projects'] ) { continue; } ?><a href="<?php echo esc_url( home_url( '/projects/?city=' . rawurlencode( $c['name'] ) ) ); ?>"><?php nadlan_e( 'projects_in' ); ?><?php echo esc_html( $c['name'] ); ?></a><?php endforeach; ?>
			<a href="<?php echo esc_url( home_url( '/projects/?project_type=pinui_binui' ) ); ?>"><?php nadlan_e( 'pinui' ); ?></a>
			<a href="<?php echo esc_url( home_url( '/projects/?project_type=tama38' ) ); ?>"><?php nadlan_e( 'tama' ); ?></a>
		</div>
		<div class="nlhv2-mfoot-col"><p><?php nadlan_e( 'mf_calc' ); ?></p>
			<a href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>"><?php nadlan_e( 'calc_mortgage' ); ?></a>
			<a href="<?php echo esc_url( home_url( '/purchase-tax-calculator/' ) ); ?>"><?php nadlan_e( 'calc_tax' ); ?></a>
			<a href="<?php echo esc_url( home_url( '/apartment-purchase-cost-calculator/' ) ); ?>"><?php nadlan_e( 'calc_full' ); ?></a>
			<a href="<?php echo esc_url( home_url( '/property-value-estimator/' ) ); ?>"><?php nadlan_e( 'value' ); ?></a>
			<a href="<?php echo esc_url( home_url( '/buying-apartment/' ) ); ?>"><?php nadlan_e( 'buying_kablan' ); ?></a>
			<a href="<?php echo esc_url( home_url( '/tabu-extract-check/' ) ); ?>"><?php nadlan_e( 'tabu' ); ?></a>
			<a href="<?php echo esc_url( home_url( '/investment/' ) ); ?>"><?php nadlan_e( 'invest' ); ?></a>
			<a href="<?php echo esc_url( home_url( '/glossary/' ) ); ?>"><?php nadlan_e( 'glossary' ); ?></a>
		</div>
		<div class="nlhv2-mfoot-col"><p><?php nadlan_e( 'mf_pros' ); ?></p>
			<?php foreach ( $profs as $key => $pm ) : ?><a href="<?php echo esc_url( home_url( '/professionals/?profession=' . rawurlencode( $key ) ) ); ?>"><?php echo esc_html( is_array( $pm ) ? ( $pm['label'] ?? $key ) : $key ); ?></a><?php endforeach; ?>
			<a href="<?php echo esc_url( home_url( '/professionals/' ) ); ?>"><?php nadlan_e( 'all_pros' ); ?></a>
		</div>
		<div class="nlhv2-mfoot-col"><p><?php nadlan_e( 'mf_brand' ); ?></p>
			<a href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>"><?php nadlan_e( 'post_free' ); ?></a>
			<a href="<?php echo esc_url( home_url( '/advertise/' ) ); ?>"><?php nadlan_e( 'advertise_pros' ); ?></a>
			<a href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"><?php nadlan_e( 'contact' ); ?></a>
			<?php $nlgw_lbl = array( 'he' => 'השקעות נדל"ן בחו"ל', 'en' => 'Global Investment', 'fr' => 'Investissement global', 'ru' => 'Инвестиции за рубежом', 'ar' => 'استثمار عالمي' ); $nlgw_l = function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he'; ?>
			<a href="<?php echo esc_url( home_url( '/global/' . ( 'he' === $nlgw_l ? '' : '?lang=en' ) ) ); ?>"><?php echo esc_html( isset( $nlgw_lbl[ $nlgw_l ] ) ? $nlgw_lbl[ $nlgw_l ] : $nlgw_lbl['he'] ); ?></a>
			<?php $nlsm_lbl = array( 'he' => 'מפת האתר', 'en' => 'Site Map', 'fr' => 'Plan du site', 'ru' => 'Карта сайта', 'ar' => 'خريطة الموقع' ); $nlsm_l = function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he'; ?>
			<a href="<?php echo esc_url( home_url( '/site-map/' . ( 'he' === $nlsm_l ? '' : '?lang=en' ) ) ); ?>"><?php echo esc_html( isset( $nlsm_lbl[ $nlsm_l ] ) ? $nlsm_lbl[ $nlsm_l ] : $nlsm_lbl['he'] ); ?></a>
			<a href="<?php echo esc_url( home_url( '/en/' ) ); ?>">English</a>
		</div>
	</section>
	<p class="nlhv2-legal" dir="rtl"><?php nadlan_e( 'legal' ); ?></p>
		<?php
	}
}

/* ============================ shortcode ============================ */

if ( ! function_exists( 'nadlan_home_v2_shortcode' ) ) {
	function nadlan_home_v2_shortcode( $atts = array() ) {
		$atts = shortcode_atts( array( 'lang' => '' ), (array) $atts, 'nadlan_home_v2' );
		if ( $atts['lang'] && function_exists( 'nadlan_set_lang' ) ) {
			nadlan_set_lang( $atts['lang'] );
			$GLOBALS['nadlan_is_lang_home'] = ( nadlan_current_lang() !== 'he' );
		}
		$lang = function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he';
		$dir  = ( function_exists( 'nadlan_lang_is_rtl' ) && ! nadlan_lang_is_rtl( $lang ) ) ? 'ltr' : 'rtl';
		$default = array( 'ticker', 'browse', 'hero', 'market', 'projects', 'video', 'listings', 'areas', 'magazine', 'tools', 'pros', 'intl', 'megafooter' ); // video band back: the hero is the live map now (owner 2026-07-07)
		$bands   = get_option( 'nadlan_home_bands', $default );
		if ( ! is_array( $bands ) || ! $bands ) { $bands = $default; }
		// the standalone video band is retired: it now rides beside the tour
		// (owner 2026-07-29). Defensive - a stored nadlan_home_bands option
		// would otherwise resurrect it below the fold.
		$bands = array_values( array_diff( $bands, array( 'video' ) ) );
		// the flagship 3D band always rides right after the hero (owner 2026-07-06)
		if ( ! in_array( 'flagships', $bands, true ) ) {
			$hi = array_search( 'hero', $bands, true );
			if ( false !== $hi ) { array_splice( $bands, $hi + 1, 0, 'flagships' ); }
			else { array_unshift( $bands, 'flagships' ); }
		}
		// ONE-map law: with the aerial hero the LIVE map gets its own light band
		// after the dark projects band; with the map-hero fallback it stays hero-only.
		$bands = array_values( array_diff( $bands, array( 'dronemap' ) ) );
		if ( trim( (string) get_option( 'nadlan_home_hero_aerial', '' ) ) ) {
			// the LIVE map sits directly under the 3D gallery (owner 2026-07-29):
			// it was buried mid-page and visitors never reached it.
			$fi = array_search( 'flagships', $bands, true );
			array_splice( $bands, false !== $fi ? $fi + 1 : count( $bands ), 0, 'dronemap' );
		}
		// the tour+video pair leads, immediately after the hero and before the 3D
		// gallery. Spliced AFTER flagships so the result is hero, pair, gallery.
		if ( ! in_array( 'tourvideo', $bands, true ) ) {
			$hi2 = array_search( 'hero', $bands, true );
			array_splice( $bands, false !== $hi2 ? $hi2 + 1 : 0, 0, 'tourvideo' );
		}
		// the urban renewal product rides the homepage (owner 2026-07-12)
		if ( ! in_array( 'renewal', $bands, true ) ) {
			$ti = array_search( 'tools', $bands, true );
			array_splice( $bands, false !== $ti ? $ti + 1 : count( $bands ), 0, 'renewal' );
		}
		// the rentals manager rides too (owner 2026-07-12): free product, discoverable
		if ( ! in_array( 'rentals', $bands, true ) ) {
			$ri = array_search( 'listings', $bands, true );
			array_splice( $bands, false !== $ri ? $ri + 1 : count( $bands ), 0, 'rentals' );
		}
		// (2026-07-12 pushed the video below the areas band to keep two media
		// stages apart. Superseded 2026-07-29: the video is now paired with the
		// tour at the top, which is one stage, so that rule is gone.)
		ob_start();
		echo '<div class="nlhv2" dir="' . esc_attr( $dir ) . '" lang="' . esc_attr( $lang ) . '">';
		if ( function_exists( 'nadlan_lang_switcher' ) ) { echo '<div class="nlhv2-langbar">' . nadlan_lang_switcher() . '</div>'; }
		foreach ( $bands as $b ) {
			$fn = 'nadlan_hv2_band_' . sanitize_key( $b );
			if ( function_exists( $fn ) ) { call_user_func( $fn ); }
		}
		echo '</div>';
		return ob_get_clean();
	}
}
add_shortcode( 'nadlan_home_v2', 'nadlan_home_v2_shortcode' );

/* FRONT-PAGE CONTENT GUARD (2026-07-02 root cause). Legacy parent-theme code
   that is NOT in this repo swaps the front page's content with the old "home
   showroom" pattern at render time - which is why homepage releases looked
   dead to visitors while head-asset substring checks passed. This runs at the
   very end of the chain: if the front page's rendered content is not the v2
   homepage, replace it with ours. Remove only after the legacy renderer is
   deleted from the parent theme on the server. */
add_filter( 'the_content', function ( $content ) {
	if ( is_admin() || ! is_front_page() || ! in_the_loop() || ! is_main_query() ) { return $content; }
	if ( strpos( (string) $content, 'nlhv2-' ) !== false ) { return $content; }
	return nadlan_home_v2_shortcode();
}, PHP_INT_MAX - 5 );

/* ============================ assets ============================ */

/* V9: stamp every page that renders the home-v2 mega nav (the Hebrew front
   page AND the /en /ru /fr /ar homepages) so the duplicate theme row can be
   hidden by class — same detection the asset gate below already uses. */
add_filter( 'body_class', function ( $classes ) {
	$oid          = get_queried_object_id();
	$is_home_page = is_front_page() && get_option( 'show_on_front' ) === 'page';
	if ( $is_home_page || ( is_singular() && has_shortcode( (string) get_post_field( 'post_content', $oid ), 'nadlan_home_v2' ) ) ) {
		$classes[] = 'nlhv2-on';
	}
	return $classes;
} );

if ( ! function_exists( 'nadlan_hv2_assets' ) ) {
	function nadlan_hv2_assets() {
		$oid = get_queried_object_id();
		$is_home_page = is_front_page() && get_option( 'show_on_front' ) === 'page';
		if ( ! ( is_singular() && has_shortcode( (string) get_post_field( 'post_content', $oid ), 'nadlan_home_v2' ) ) && ! $is_home_page ) { return; }
		wp_register_style( 'nadlan-hv2', false );
		wp_enqueue_style( 'nadlan-hv2' );
		wp_add_inline_style( 'nadlan-hv2', '
.nlhv2{--ink:#1B1A17;--warm:#6D665C;--gold:#9C7A3C;--terra:#C2563A;--line:#E2DCD0;--band:#F3EEE3;--dark:#14130F;font-family:var(--font-sans,Heebo,system-ui,sans-serif);color:var(--ink)}
.nlhv2 h1{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500;font-size:clamp(1.8rem,4.6vw,3rem);line-height:1.1;margin:0 0 12px;letter-spacing:-.01em}
.nlhv2 h2{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500;font-size:clamp(1.35rem,2.6vw,1.8rem);margin:0}
.nlhv2-kicker{font-size:11.5px;font-weight:700;letter-spacing:.14em;color:var(--gold);margin:0 0 2px;text-transform:uppercase}
.nlhv2-note{font-size:11.5px;color:var(--warm)}
.nlhv2-langbar{display:flex;justify-content:flex-end;padding:8px 0 2px}
.nlhv2-langs{display:inline-flex;gap:2px;background:var(--band,#F3EEE3);border-radius:999px;padding:3px}
.nlhv2-langs a{font-size:12.5px;font-weight:600;color:var(--soft,#4A463E);padding:4px 11px;border-radius:999px;text-decoration:none}
.nlhv2-langs a.on{background:#fff;color:var(--ink,#1B1A17);box-shadow:0 1px 4px rgba(0,0,0,.08)}
.nlhv2-ticker{display:flex;gap:20px;align-items:center;overflow-x:auto;scrollbar-width:none;background:var(--ink);color:#CFC8B8;font-size:12px;padding:9px 16px;margin:0 -20px 10px;white-space:nowrap}
.nlhv2-ticker::-webkit-scrollbar{display:none}
.nlhv2-ticker a{color:#CFC8B8;text-decoration:none}
.nlhv2-ticker a b{color:#F4EEDE;font-size:13px}
.nlhv2-ticker a:hover b{color:#E6D4AE}
.nlhv2-ticker-date{color:#8D8676;flex-shrink:0}
/* V7 (owner order 22.8): the homepage carries ONE horizontal nav — this mega
   nav. The static theme row duplicated it 1:1, so it steps aside here only;
   every destination it offered lives inside the mega groups, and the
   sitewide nav keeps serving every other page unchanged. NO apostrophes in
   this comment — it lives inside a single-quoted PHP string (the 2026-07-12
   outage class; the server lint gate caught this once already).
   V9: the LANGUAGE homepages (/en/ /ru/ /fr/ /ar/) render this same mega nav
   as regular pages without the .home body class — the owner caught the
   double menu there. The body_class filter below stamps .nlhv2-on on every
   page that renders the mega, and the hide rule follows that class. */
.home .nlpc-site-header .nlpc-primary-nav.nlpc-primary-nav,
.nlhv2-on .nlpc-site-header .nlpc-primary-nav.nlpc-primary-nav{display:none!important}
.nlhv2-browse{display:flex;gap:4px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding:6px 0 10px;margin-bottom:8px;position:relative;z-index:40}
.nlhv2-browse details{position:relative}
.nlhv2-browse summary{list-style:none;cursor:pointer;font-size:13.5px;font-weight:600;padding:9px 14px;border-radius:8px;user-select:none}
.nlhv2-browse summary::-webkit-details-marker{display:none}
.nlhv2-browse summary::after{content:" ▾";font-size:10px;color:var(--warm)}
.nlhv2-browse details[open] summary{background:var(--band)}
.nlhv2-plain{font-size:13.5px;font-weight:600;padding:9px 14px;border-radius:8px;color:var(--ink);text-decoration:none}
.nlhv2-plain:hover{background:var(--band)}
.nlhv2-mega{position:absolute;top:100%;inset-inline-start:0;min-width:230px;background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 18px 44px rgba(27,26,23,.14);padding:10px;display:grid;gap:2px;z-index:50}
.nlhv2-mega a{display:block;font-size:13.5px;color:var(--ink);text-decoration:none;padding:8px 10px;border-radius:7px}
.nlhv2-mega a:hover{background:var(--band)}
.nlhv2-mega a b{font-weight:700}
.nlhv2-mega-cta{color:var(--terra)!important;font-weight:700}
.nlhv2-hero{display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center;padding:30px 0 26px}
/* THE MAP HERO (owner decision 2, 2026-07-07): the live night map is the opener */
.nlhv2-hero--map{display:block;position:relative;min-height:560px;padding:0;border-radius:22px;overflow:hidden;margin:8px 0 16px;background:#14130F;border:1px solid #2A251B}
@media(max-width:860px){.nlhv2-hero--map{min-height:520px;border-radius:16px}}
.nlhv2-hero-mapbg{position:absolute;inset:0}
.nlhv2-hero--aerial .nlhv2-hero-mapbg{background-position:center;background-size:cover;background-repeat:no-repeat}
.nlhv2-hero--aerial{min-height:540px}
@media(max-width:860px){.nlhv2-hero--aerial{min-height:480px}}
.nlhv2-dronemap{padding:0}
/* light band (owner 2026-07-12: the page had too many dark blocks) */
.nlhv2-renewal{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:22px;padding:clamp(26px,4vw,44px)}
.nlhv2-renewal-in{max-width:760px}
.nlhv2-renewal-k{color:#9C7A3C!important}
.nlhv2-renewal h2{color:#1B1A17;font-family:"Frank Ruhl Libre",serif;font-size:clamp(1.5rem,1.1rem+1.6vw,2.1rem);margin:6px 0 8px}
.nlhv2-renewal-sub{color:#51483A;font:400 14.5px/1.75 Heebo,sans-serif;margin:0 0 18px;max-width:620px}
.nlhv2-renewal-steps{display:flex;gap:12px;flex-wrap:wrap;margin:0 0 20px}
.nlhv2-renewal-steps span{display:inline-flex;align-items:center;gap:9px;background:#fff;border:1px solid #E2DCD0;border-radius:999px;padding:9px 16px 9px 10px;color:#51483A;font:600 13px Heebo,sans-serif}
.nlhv2-renewal-steps i{display:inline-block;width:24px;height:24px;border-radius:50%;background:#9C7A3C;color:#FAF7F1;font:700 12px/24px "Frank Ruhl Libre",serif;font-style:normal;text-align:center}
.nlhv2-renewal-ctas{display:flex;gap:12px;flex-wrap:wrap}
.nlhv2-renewal-go{background:#C2563A;color:#FAF7F1;border-radius:11px;padding:14px 24px;font:700 14.5px Heebo,sans-serif;text-decoration:none;box-shadow:0 12px 28px -12px rgba(194,86,58,.45)}
.nlhv2-renewal-alt{border:1.5px solid #9C7A3C;color:#1B1A17;background:#fff;border-radius:11px;padding:14px 24px;font:700 14.5px Heebo,sans-serif;text-decoration:none}
.nlhv2-renewal-go:hover,.nlhv2-renewal-alt:hover{filter:brightness(1.05)}
.nlhv2-renewal-note{color:#8E877A;font:600 12px Heebo,sans-serif;margin:14px 0 0}
.nlhv2-rentals{background:#FFFFFF;border:1.5px solid #9C7A3C;border-radius:22px;padding:clamp(26px,4vw,44px)}
.nlhv2-rentals-in{max-width:760px}
.nlhv2-rentals h2{font-family:"Frank Ruhl Libre",serif;font-size:clamp(1.5rem,1.1rem+1.6vw,2.1rem);margin:6px 0 8px;color:#1B1A17}
.nlhv2-rentals-sub{color:#51483A;font:400 14.5px/1.75 Heebo,sans-serif;margin:0 0 18px;max-width:620px}
.nlhv2-rentals-steps span{background:#F3EEE3;border-color:#E2DCD0;color:#51483A}
.nlhv2-rentals-note{color:#8E877A;font:600 12px Heebo,sans-serif;margin:14px 0 0}
.nlhv2-renewal.has-img,.nlhv2-rentals.has-img,.nlhv2-tourvideo{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(18px,3vw,34px);align-items:center}
.nlhv2-band-art{order:2;min-height:300px;height:100%;border-radius:16px;background-position:center;background-size:cover;background-repeat:no-repeat;border:1px solid #E2DCD0}
.nlhv2-renewal.has-img .nlhv2-band-art{border-color:#3A342A}
@media(max-width:860px){.nlhv2-renewal.has-img,.nlhv2-rentals.has-img{grid-template-columns:1fr}.nlhv2-band-art{order:0;min-height:220px}}
.nlhv2-flagdev{display:block;margin-top:8px;color:#9C7A3C;font-weight:700;text-decoration:none;font-size:13.5px}
.nlhv2-flagdev:hover{text-decoration:underline}
/* sketch-plate listing art must never be cropped - the facilities must stay visible */
.nlhv2-list-media.is-sketch{background-size:contain!important;background-color:#F3EEE3}
/* Cascade repair (measured live 2026-07-30): nadlan-premium-sitewide.css ships
   .page .entry-content h2{color:var(--nlx-ink)!important} and platform.css ships
   body.nlpc-platform h1,h2,h3{color:var(--nlp-ink)}. Both outrank the band rules
   above, so every headline sitting on a dark surface was painted near-black:
   the hero H1 measured 1.07:1 and the dark bands 1.18:1 - invisible, not merely
   low contrast. Winning on specificity here keeps the theme and the sitewide
   sheet untouched. */
.entry-content .nlhv2 .nlhv2-hero--map h1{color:#FAF7F1!important}
.entry-content .nlhv2 .nlhv2-dark header h2{color:#F4EEDE!important}
.entry-content .nlhv2 .nlhv2-en h2{color:#FAF8F3!important}
.nlhv2-hero-veil{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(20,19,15,.86) 0%,rgba(20,19,15,.55) 26%,rgba(20,19,15,.1) 52%,rgba(20,19,15,.45) 100%)}
.nlhv2-hero--map .nlhv2-hero-copy{position:relative;z-index:6;max-width:640px;margin:26px clamp(12px,3vw,36px);padding:26px clamp(16px,3vw,32px);pointer-events:none;background:linear-gradient(180deg,rgba(20,19,15,.62),rgba(20,19,15,.42));border:1px solid rgba(233,217,168,.16);border-radius:18px;backdrop-filter:blur(3px)}
.nlhv2-hero--map .nlhv2-hero-copy>*{pointer-events:auto}
.nlhv2-hero--map h1{color:#FAF7F1;text-shadow:0 2px 6px rgba(0,0,0,.85),0 6px 24px rgba(0,0,0,.6)}
.nlhv2-hero--map .nlhv2-sub{color:#E4DDCE;text-shadow:0 1px 8px rgba(0,0,0,.5)}
.nlhv2-hero--map .nlhv2-tabs button{background:rgba(250,247,241,.14);color:#F3EEE3;border-color:rgba(233,217,168,.35);backdrop-filter:blur(4px)}
.nlhv2-hero--map .nlhv2-tabs button.is-on{background:#FAF7F1;color:#1B1A17}
.nlhv2-hero--map .nlhv2-box{box-shadow:0 26px 54px -20px rgba(0,0,0,.65)}
.nlhv2-hero--map .nlhv2-trust a{color:#E4DDCE;text-shadow:0 1px 6px rgba(0,0,0,.6)}
.nlhv2-hero--map .nlhv2-trust b{color:#E9D9A8}
/* the CBS data panel (decision 7): real bars, tabular numbers, dated source */
.nlhv2-cbs{background:#fff;border:1px solid var(--line,#E2DCD0);border-radius:16px;padding:24px 26px 14px}
.nlhv2-cbs-bars{display:grid;grid-template-columns:repeat(6,1fr);gap:18px;align-items:end;height:190px}
@media(max-width:720px){.nlhv2-cbs-bars{grid-template-columns:repeat(3,1fr);height:auto;row-gap:26px}}
.nlhv2-cbs-bar{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:7px;height:100%;min-height:130px}
.nlhv2-cbs-bar b{font:700 13.5px/1 Heebo,sans-serif;font-variant-numeric:tabular-nums;color:#1B1A17}
.nlhv2-cbs-bar i{width:70%;max-width:54px;border-radius:7px 7px 0 0;background:#C9BC9C}
.nlhv2-cbs-bar.is-top i{background:var(--gold,#9C7A3C)}
.nlhv2-cbs-bar span{font:500 12.5px/1.2 Heebo,sans-serif;color:#6D665C;text-align:center}
.nlhv2-cbs-src{font-size:12px;color:#6D665C;border-top:1px solid var(--line,#E2DCD0);margin:16px 0 0;padding:10px 2px 2px}
.nlhv2-cbs-src a{color:#9C7A3C}
/* the vacant CTA tile reads INTENTIONAL, not broken (owner sweep 2026-07-07) */
.nlhv2-cta-tile{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:6px;border:1.6px dashed #C9A55C!important;background:#FBF8F2!important;border-radius:14px}
.nlhv2-cta-tile::before{content:"+";font:700 30px/1 Heebo,sans-serif;color:#9C7A3C}
.nlhv2-cta-tile b{color:#1B1A17}
.nlhv2-cta-tile:hover{border-style:solid!important}
/* the promo video lives in a confined frame - never full-bleed (owner 2026-07-07) */
.nlhv2-videoband .nlhv2-video-frame{max-width:820px;margin:0 auto;aspect-ratio:16/9;border-radius:18px;overflow:hidden;border:1px solid #D6C189;background:#14130F;box-shadow:0 22px 48px -26px rgba(27,26,23,.5)}
.nlhv2-videoband .nlhv2-video-frame video,.nlhv2-videoband .nlhv2-video-frame iframe{width:100%;height:100%;object-fit:cover;display:block;border:0}
.nlhv2-videoband header{text-align:center}
@media(max-width:640px){.nlhv2-videoband .nlhv2-video-frame{border-radius:12px}}
@media(max-width:860px){.nlhv2-hero{grid-template-columns:1fr}}
.nlhv2-sub{color:var(--warm);max-width:560px;margin:0 0 20px;font-size:15.5px}
.nlhv2-search{max-width:640px}
.nlhv2-tabs{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:-1px}
.nlhv2-tabs button{font:600 13.5px/1 inherit;font-family:inherit;border:1px solid var(--line);border-bottom:0;background:#FAF8F3;color:var(--warm);border-radius:10px 10px 0 0;padding:11px 18px;cursor:pointer;min-height:40px}
.nlhv2-tabs button.is-on{background:#fff;color:var(--ink);font-weight:700}
.nlhv2-box{display:flex;background:#fff;border:1px solid var(--line);border-radius:0 12px 12px 12px;padding:7px;box-shadow:0 14px 34px rgba(27,26,23,.08)}
.nlhv2-box input{flex:1;border:0;font:inherit;font-size:15px;padding:12px 14px;background:none;min-width:0;outline-offset:-2px}
.nlhv2-box button{font:700 15px/1 inherit;font-family:inherit;border:0;background:var(--terra);color:#fff;border-radius:8px;padding:0 26px;cursor:pointer;min-height:46px}
.nlhv2-box button:hover{background:#A7452E}
.nlhv2-trust{display:flex;gap:22px;flex-wrap:wrap;margin-top:20px;font-size:12.5px;color:var(--warm)}
.nlhv2-trust a{color:var(--warm);text-decoration:none}
.nlhv2-trust a:hover b{color:var(--gold)}
.nlhv2-trust b{color:var(--ink);font-size:15px;display:block}
.nlhv2-hero-flag{display:block;border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff;text-decoration:none;color:var(--ink);box-shadow:0 20px 50px rgba(27,26,23,.1);transition:transform .25s}
.nlhv2-hero-flag:hover{transform:translateY(-3px)}
.nlhv2-hero-flag-media{display:block;aspect-ratio:16/11;background:var(--band) center/cover no-repeat;position:relative}
.nlhv2-flagships .nlhv2-flagsub{color:var(--muted,#6D665C);font-size:14.5px;margin:2px 0 16px;max-width:720px}
.nlhv2-flaggrid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
/* THE SHOWCASE (2026-07-11): live spinning flagship + selector cards */
.nlhv2-show{display:grid;grid-template-columns:1.35fr .85fr;gap:16px;align-items:stretch}
@media(max-width:900px){.nlhv2-show{grid-template-columns:1fr}}
.nlhv2-show-stage{position:relative;min-height:440px;border-radius:18px;overflow:hidden;background:#14130F center/cover no-repeat;border:1px solid #2A251B;box-shadow:0 24px 60px rgba(27,26,23,.18)}
@media(max-width:700px){.nlhv2-show-stage{min-height:340px}}
.nlhv2-show-stage model-viewer{position:absolute;inset:0;width:100%;height:100%;direction:ltr;--poster-color:transparent;background:transparent;opacity:0;transition:opacity .6s}
.nlhv2-show-stage.is-loaded model-viewer{opacity:1}
.nlhv2-show-stage{transition:background-image .4s}
.nlhv2-show-chip{position:absolute;top:12px;inset-inline-start:12px;z-index:3;background:rgba(20,19,15,.82);color:#E9D9A8;font:600 12px/1 Heebo,sans-serif;padding:7px 12px;border-radius:999px;border:1px solid rgba(233,217,168,.4);pointer-events:none}
.nlhv2-show-go{position:absolute;bottom:14px;inset-inline-start:14px;z-index:3;background:linear-gradient(180deg,#b9923f,#9C7A3C);color:#FAF7F1;font:700 13px/1 Heebo,sans-serif;padding:12px 18px;border-radius:10px;text-decoration:none;box-shadow:0 10px 26px -8px rgba(0,0,0,.5)}
.nlhv2-show-go:hover{filter:brightness(1.06)}
.nlhv2-show-spin{position:absolute;inset-block-start:50%;inset-inline-start:50%;transform:translate(-50%,-50%);z-index:3;background:rgba(20,19,15,.85);color:#F5EFE2;font:700 13.5px/1 Heebo,sans-serif;border:1px solid rgba(233,217,168,.45);border-radius:999px;padding:14px 20px;cursor:pointer;backdrop-filter:blur(3px)}
.nlhv2-show-stage.is-live .nlhv2-show-spin{display:none}
.nlhv2-show-cards{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-content:start}
@media(max-width:520px){.nlhv2-show-cards{grid-template-columns:1fr 1fr}}
.nlhv2-shcard{display:flex;flex-direction:column;text-align:start;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;cursor:pointer;padding:0;transition:transform .2s,border-color .2s;font-family:inherit}
.nlhv2-shcard:hover{transform:translateY(-2px);border-color:var(--gold,#9C7A3C)}
.nlhv2-shcard.is-on{border-color:var(--gold,#9C7A3C);box-shadow:0 0 0 2px rgba(156,122,60,.25)}
.nlhv2-shcard-media{position:relative;display:block;aspect-ratio:16/10;background:var(--band);overflow:hidden}
.nlhv2-shcard-media img{width:100%;height:100%;object-fit:cover;display:block}
/* T1 27.8.2026 (owner order): flagship plates full-frame 4:3, no crop */
.nlhv2-shcard-media.nlhv2-shcard-media{aspect-ratio:4/3;background:#EFEAE0}
.nlhv2-shcard-media.nlhv2-shcard-media img{object-fit:contain}

.nlhv2-tag{position:absolute;top:8px;inset-inline-start:8px;font-style:normal;font:700 10.5px/1 Heebo,sans-serif;background:rgba(20,19,15,.85);color:#E9D9A8;border-radius:6px;padding:5px 9px}
.nlhv2-tag--3d{inset-inline-start:auto;inset-inline-end:8px;background:var(--gold,#9C7A3C);color:#14130F}
.nlhv2-shcard-body{display:flex;flex-direction:column;gap:6px;padding:10px 12px 12px}
.nlhv2-shcard-body b{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:.98rem;line-height:1.25;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;unicode-bidi:plaintext;text-align:start}
.nlhv2-chiprow{display:flex;gap:6px;flex-wrap:wrap}
.nlhv2-chiprow i{font-style:normal;font:600 11.5px/1 Heebo,sans-serif;color:#51483A;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:999px;padding:5px 9px}
@media(max-width:980px){.nlhv2-flaggrid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.nlhv2-flaggrid{grid-template-columns:1fr}}
.nlhv2-flag{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;text-decoration:none;color:var(--ink);transition:transform .22s,border-color .22s;box-shadow:0 2px 10px rgba(27,26,23,.05)}
.nlhv2-flag:hover{transform:translateY(-3px);border-color:var(--gold,#9C7A3C)}
.nlhv2-flag-media{display:block;aspect-ratio:4/3;background:var(--band) center/cover no-repeat;position:relative}
.nlhv2-flag-media.is-poster{background-size:contain;background-color:#14130F}
.nlhv2-flag-3d{position:absolute;top:8px;inset-inline-end:8px;width:52px;height:52px;border-radius:10px;background:#14130F center/cover no-repeat;border:1.5px solid var(--gold,#9C7A3C)}
.nlhv2-flag-3d b{position:absolute;bottom:-1px;inset-inline-end:-1px;font-size:9px;font-weight:800;background:var(--gold,#9C7A3C);color:#14130F;border-radius:7px 0 8px 0;padding:1px 5px}
.nlhv2-flag-body{display:flex;flex-direction:column;gap:4px;padding:12px 14px 14px}
.nlhv2-flag-body b{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:1.02rem;line-height:1.3;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;unicode-bidi:plaintext;text-align:start}
.nlhv2-flag-meta{font-size:12.5px;color:var(--muted,#6D665C)}
.nlhv2-flag-go{font-size:12.5px;font-weight:700;color:var(--gold,#9C7A3C);margin-top:2px}
.nlhv2-hero-flag-media em{position:absolute;bottom:12px;inset-inline-start:12px;font-style:normal;font-size:12px;font-weight:700;background:rgba(27,26,23,.85);color:#E6D4AE;border-radius:6px;padding:6px 11px}
.nlhv2-hero-flag-cap{display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:12px 16px}
.nlhv2-hero-flag-cap b{font-family:var(--font-serif,serif);font-size:1.1rem}
.nlhv2-hero-flag-cap span{font-size:12.5px;color:var(--warm)}
.nlhv2-hero-video{position:relative;aspect-ratio:16/9;background:linear-gradient(160deg,#211F19,var(--dark));display:block}
.nlhv2-hero-video video{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;display:block;opacity:1}
.nlhv2-hv-brand{position:absolute;inset:0;display:grid;place-items:center;font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:2.2rem;color:#E6D4AE;letter-spacing:.06em}
.nlhv2-band{padding:30px 0;border-top:1px solid var(--line)}
.nlhv2-alt{background:linear-gradient(180deg,#FAF8F3,transparent)}
.nlhv2-band header{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.nlhv2-band header>a{color:var(--gold);font-size:13.5px;font-weight:700;text-decoration:none}
.nlhv2-video-frame{aspect-ratio:16/9;border-radius:16px;overflow:hidden;background:var(--dark);box-shadow:0 20px 50px rgba(27,26,23,.14)}
.nlhv2-video-frame iframe,.nlhv2-video-frame video{width:100%;height:100%;border:0;display:block}
.nlhv2-market{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.nlhv2-market a{display:block;border:1px solid var(--line);border-radius:12px;background:#fff;padding:18px;text-decoration:none;color:var(--ink);transition:border-color .2s}
.nlhv2-market a:hover{border-color:var(--gold)}
.nlhv2-market b{display:block;font-family:var(--font-serif,serif);font-size:1.7rem}
.nlhv2-market span{font-size:12.5px;color:var(--warm)}
.nlhv2-dark{background:linear-gradient(160deg,#211F19,var(--dark));border-radius:18px;padding:30px 26px;margin:26px -6px;color:#F4EEDE}
.nlhv2-dark header{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:18px}
.nlhv2-dark h2{color:#F4EEDE}
.nlhv2-dark .nlhv2-kicker{color:#C9A45C}
.nlhv2-dark-all{color:#E6D4AE;font-size:13.5px;font-weight:700;text-decoration:none}
.nlhv2-projgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.nlhv2-proj{border:1px solid rgba(244,238,222,.14);border-radius:14px;overflow:hidden;background:rgba(255,255,255,.03)}
.nlhv2-proj-media{display:block;aspect-ratio:16/10;background:#26241D center/cover no-repeat;position:relative}
.nlhv2-proj-media em{position:absolute;top:10px;inset-inline-start:10px;font-style:normal;font-size:11px;font-weight:700;background:rgba(20,19,15,.85);color:#E6D4AE;border-radius:5px;padding:4px 9px}
.nlhv2-proj-body{padding:12px 14px 14px}
.nlhv2-proj-body b{display:block;font-family:var(--font-serif,serif);font-size:1.1rem;color:#F4EEDE}
.nlhv2-proj-body span{display:block;font-size:12.5px;color:#B8B1A0}
.nlhv2-proj-body i{display:block;font-style:normal;font-size:12px;color:#C9A45C;margin-top:4px}
.nlhv2-proj-live{margin-top:10px;font:700 12.5px/1 inherit;font-family:inherit;border:1px solid rgba(230,212,174,.4);background:none;color:#E6D4AE;border-radius:8px;padding:9px 14px;cursor:pointer}
.nlhv2-proj-live:hover{background:rgba(230,212,174,.12)}
.nlhv2-viewerwrap{margin-top:16px}
#nlhv2-viewer-slot model-viewer{width:100%;height:380px;border-radius:12px;background:#EFEAE0}
.nlhv2-dark-note{color:#8D8676;margin:14px 0 0}
.nlhv2-listtabs{display:flex;gap:6px;margin-bottom:14px}
.nlhv2-listtabs button{font:600 13px/1 inherit;font-family:inherit;border:1px solid var(--line);background:#fff;color:var(--warm);border-radius:999px;padding:9px 18px;cursor:pointer}
.nlhv2-listtabs button.is-on{background:var(--ink);border-color:var(--ink);color:#fff;font-weight:700}
.nlhv2-listgrid,.nlhv2-prosgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.nlhv2-list{display:block;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#fff;text-decoration:none;color:var(--ink);padding-bottom:10px;transition:border-color .2s}
.nlhv2-list:hover{border-color:var(--gold)}
.nlhv2-list-media{position:relative;display:block;aspect-ratio:4/3;background:var(--band);margin-bottom:8px;overflow:hidden}
.nlhv2-list-media img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s ease}
.nlhv2-list:hover .nlhv2-list-media img{transform:scale(1.04)}
.nlhv2-list b{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:1.06rem}
.nlhv2-list .nlhv2-chiprow{padding:6px 12px 0}
.nlhv2-list b{display:block;padding:0 12px;font-size:15px}
.nlhv2-list>span{display:block;padding:0 12px;font-size:12px;color:var(--warm)}
.nlhv2-cityrow{margin:16px 0 0;font-size:12.5px;display:flex;gap:6px 16px;flex-wrap:wrap}
.nlhv2-cityrow a{color:var(--warm);text-decoration:none}
.nlhv2-cityrow a:hover{color:var(--gold)}
.nlhv2-areas{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
.nlhv2-areas a{display:block;border:1px solid var(--line);border-radius:12px;background:#fff;padding:16px 18px;text-decoration:none;color:var(--ink);transition:border-color .2s,transform .2s}
.nlhv2-areas a:hover{border-color:var(--gold);transform:translateY(-2px)}
.nlhv2-areas b{display:block;font-family:var(--font-serif,serif);font-size:1.15rem}
.nlhv2-areas span{font-size:12px;color:var(--warm)}
.nlhv2-mag{display:grid;grid-template-columns:1.2fr 1fr .8fr;gap:18px}
@media(max-width:900px){.nlhv2-mag{grid-template-columns:1fr}}
.nlhv2-mag-lead{display:block;text-decoration:none;color:var(--ink);border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff}
.nlhv2-mag-lead b{display:block;font-family:var(--font-serif,serif);font-size:1.2rem;padding:4px 14px 0;line-height:1.3}
.nlhv2-mag-lead span{display:block;padding:4px 14px 12px;font-size:12px;color:var(--warm)}
.nlhv2-mag-rows{display:flex;flex-direction:column;gap:2px}
.nlhv2-mag-rows a{display:block;text-decoration:none;color:var(--ink);padding:12px 4px;border-bottom:1px solid var(--line)}
.nlhv2-mag-rows b{display:block;font-size:14.5px;line-height:1.35}
.nlhv2-mag-rows span{font-size:11.5px;color:var(--warm)}
.nlhv2-mag-rail{border-inline-start:1px solid var(--line);padding-inline-start:18px}
.nlhv2-mag-rail p{font-size:11.5px;font-weight:700;letter-spacing:.12em;color:var(--gold);margin:0 0 8px}
.nlhv2-mag-rail a{display:block;font-size:13.5px;color:var(--ink);text-decoration:none;padding:7px 0;border-bottom:1px dashed var(--line)}
.nlhv2-mag-rail a:hover{color:var(--gold)}
.nlhv2-tools{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
.nlhv2-tools a{display:block;border:1px solid var(--line);border-radius:10px;background:#fff;padding:14px 16px;text-decoration:none;color:var(--ink);transition:border-color .2s,transform .2s}
.nlhv2-tools a:hover{border-color:var(--gold);transform:translateY(-2px)}
.nlhv2-tools b{display:block;font-size:14.5px}
.nlhv2-tools span{font-size:12px;color:var(--warm)}
.nlhv2-tool-lead{background:var(--band)!important;border-color:var(--gold)!important}
.nlhv2-pro{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;border:1px solid var(--line);border-radius:12px;background:#fff;padding:16px 10px;text-decoration:none;color:var(--ink);transition:border-color .2s}
.nlhv2-pro:hover{border-color:var(--gold)}
.nlhv2-pro svg{width:56px;height:56px}
.nlhv2-pro b{font-size:13.5px;line-height:1.2}
.nlhv2-pro span{font-size:11.5px;color:var(--warm)}
.nlhv2-spon{position:absolute;top:8px;inset-inline-start:8px;font-style:normal;font-size:10px;font-weight:700;color:var(--warm);border:1px solid var(--line);border-radius:4px;padding:2px 6px;background:#FAF8F3}
.nlhv2-cta-tile{justify-content:center;align-items:center;text-align:center;gap:6px;background:linear-gradient(150deg,#F7F1E3,var(--band));border:1px solid #D6C189;position:relative}.nlhv2-cta-tile::before{content:"+";display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--gold,#9C7A3C);color:#FAF7F1;font-size:20px;font-weight:700;margin-bottom:2px}
.nlhv2-cta-tile b{color:var(--gold)}
.nlhv2-en{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;border-radius:16px;background:linear-gradient(160deg,#211F19,var(--dark));color:#FAF8F3;padding:26px 28px;margin:26px 0}
.nlhv2 .nlhv2-en h2,.nlhv2-en h2{color:#FAF8F3!important;font-size:1.4rem;margin:0 0 6px}
.nlhv2-en p{margin:0;font-size:13.5px;color:#C9C2B2;max-width:520px}
.nlhv2-en a{background:#E6D4AE;color:var(--ink);font-weight:700;font-size:14px;border-radius:9px;padding:13px 22px;text-decoration:none;white-space:nowrap}
.nlhv2-mfoot{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:22px;border-top:1px solid var(--line);padding:28px 0 10px}
.nlhv2-mfoot-col p{font-size:11.5px;font-weight:700;letter-spacing:.12em;color:var(--gold);margin:0 0 8px}
.nlhv2-mfoot-col a{display:block;font-size:13px;color:var(--warm);text-decoration:none;padding:4px 0}
.nlhv2-mfoot-col a:hover{color:var(--ink)}
.nlhv2-legal{font-size:11.5px;color:var(--warm);border-top:1px solid var(--line);padding:14px 0 20px;margin:16px 0 0}
@media(max-width:560px){.nlhv2-trust{gap:14px}.nlhv2-box button{padding:0 18px}.nlhv2-dark{margin:26px -14px;border-radius:0}}
/* LISTINGS RESKIN (owner 2026-07-29): price-first portal cards; sketch plates retired */
.nlhv2-list .nlfc-price{display:block;padding:0 12px;font:700 1.28rem/1.25 Heebo,sans-serif;font-variant-numeric:tabular-nums;color:var(--ink);letter-spacing:-.01em}
.nlhv2-list .nlfc-line{display:block;padding:3px 12px 0;font-size:12.5px;color:var(--warm);line-height:1.45}
.nlhv2-list .nlfc-onlist{padding:7px 12px 0}
.nlhv2-list-media.nlfc-ph{display:grid;place-items:center;background:radial-gradient(120% 90% at 50% 20%,#2A2418 0%,#14130F 70%);border-bottom:2px solid var(--gold,#9C7A3C)}
.nlfc-ph-mark{font:500 1.5rem/1 "Frank Ruhl Libre",serif;font-style:normal;color:#E6D4AE;opacity:.85;letter-spacing:.04em}
.nlfc-imgtag{position:absolute;bottom:8px;inset-inline-start:8px;font:600 10.5px/1 Heebo,sans-serif;font-style:normal;color:#F4EEDE;background:rgba(20,19,15,.72);border-radius:6px;padding:4px 8px}
' );
		wp_register_script( 'nadlan-hv2-js', false, array(), '1.69.87', true );
		wp_enqueue_script( 'nadlan-hv2-js' );
		wp_add_inline_script( 'nadlan-hv2-js', '
(function(){document.addEventListener("DOMContentLoaded",function(){
	// hero search tabs
	var f=document.querySelector(".nlhv2-search");
	if(f){f.querySelectorAll(".nlhv2-tabs button").forEach(function(b){
		b.addEventListener("click",function(){
			f.querySelectorAll(".nlhv2-tabs button").forEach(function(x){x.classList.toggle("is-on",x===b)});
			f.action=b.dataset.action;
			f.querySelectorAll("input[type=hidden]").forEach(function(h){h.remove()});
			if(b.dataset.extra){var kv=b.dataset.extra.split("=");var h=document.createElement("input");h.type="hidden";h.name=kv[0];h.value=kv[1];f.appendChild(h)}
		});
	})}
	// hero video: gif-like (muted autoplay loop, no controls). Starts right after
	// DOM ready (idle callback) so it never blocks LCP; respects data-saver and
	// reduced-motion (they keep the elegant dark brand card). If autoplay is
	// still blocked, the first tap/click anywhere retries playback.
	// Hero video: native <source> + muted/autoplay/loop makes the browser start it
	// with NO JS dependency (that is the reliable desktop path). JS only (a) nudges
	// play() for engagement-gated browsers, and (b) HONESTLY degrades to the poster
	// for data-saver / reduced-motion users instead of silently killing it for all.
	var hv=document.getElementById("nlhv2-hv");
	if(hv){
		var c=navigator.connection||{};
		var save=(c.saveData===true)||/(^|\b)2g/.test(c.effectiveType||"");
		var reduce=(window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches);
		if(save||reduce){
			// Accessible/bandwidth-honest fallback: hold on the (real) poster frame.
			hv.removeAttribute("autoplay");try{hv.pause()}catch(e){}
		}else{
			var hvPlay=function(){try{hv.muted=true;var p=hv.play();if(p&&p.catch){p.catch(function(){})}}catch(e){}};
			hvPlay();
			["loadedmetadata","loadeddata","canplay","canplaythrough"].forEach(function(ev){hv.addEventListener(ev,hvPlay)});
			// last-resort: first user gesture on desktop unlocks any remaining gate.
			["pointerdown","keydown","scroll","touchstart"].forEach(function(ev){window.addEventListener(ev,hvPlay,{once:true,passive:true})});
		}
	}
	// browse menus: close others when one opens; close on outside click
	var ds=document.querySelectorAll(".nlhv2-browse details");
	ds.forEach(function(d){d.addEventListener("toggle",function(){if(d.open){ds.forEach(function(o){if(o!==d){o.open=false}})}})});
	document.addEventListener("click",function(e){if(!e.target.closest(".nlhv2-browse")){ds.forEach(function(o){o.open=false})}});
	// listings tabs
	var lt=document.querySelectorAll(".nlhv2-listtabs button");
	lt.forEach(function(b){b.addEventListener("click",function(){
		lt.forEach(function(x){x.classList.toggle("is-on",x===b)});
		document.querySelectorAll(".nlhv2-listgrid").forEach(function(g){g.hidden=g.dataset.paneId!==b.dataset.pane});
	})});
	// ONE shared lazy model-viewer for the dark projects band
	var mvLoaded=false;
	function ensureMV(cb){
		if(mvLoaded||window.customElements&&customElements.get("model-viewer")){mvLoaded=true;cb();return}
		var s=document.createElement("script");s.type="module";
		s.src="https://unpkg.com/@google/model-viewer@3.5.0/dist/model-viewer.min.js";
		s.onload=function(){mvLoaded=true;cb()};document.head.appendChild(s);
	}
	// THE SHOWCASE: spin the flagship when the band nears the viewport
	(function(){
		var st=document.getElementById("nlhv2-shstage");if(!st)return;
		var live=false;
		function boot(){
			ensureMV(function(){
				var mv=st.querySelector("model-viewer");
				if(!mv){
					mv=document.createElement("model-viewer");
					mv.setAttribute("camera-controls","");
					mv.setAttribute("interaction-prompt","none");mv.setAttribute("shadow-intensity","0.55");
					mv.setAttribute("exposure","0.95");mv.setAttribute("environment-image","neutral");
					// scroll must never get trapped over the stage (owner 2026-07-12):
					// no wheel-zoom on the homepage showcase - drag rotates, wheel scrolls the page
					mv.setAttribute("touch-action","pan-y");mv.setAttribute("disable-zoom","");
					// the poster is a LOADING state only: once the real model renders,
					// clear it so the 3D never spins on top of a frozen photo
					mv.addEventListener("load",function(){
						st.style.backgroundImage="radial-gradient(ellipse at 50% 32%, #2A2418 0%, #14130F 68%)";
						st.classList.add("is-loaded");
					});
					st.insertBefore(mv,st.firstChild);
				}
				mv.setAttribute("src",st.dataset.glb);
				live=true;st.classList.add("is-live");
			});
		}
		var spin=document.getElementById("nlhv2-shspin");
		if(window.matchMedia&&matchMedia("(max-width:700px)").matches){
			if(spin){spin.addEventListener("click",boot)}
		}else{
			if(spin){spin.hidden=true}
			if("IntersectionObserver" in window){
				new IntersectionObserver(function(en,ob){if(en[0]&&en[0].isIntersecting){ob.disconnect();boot()}},{rootMargin:"240px"}).observe(st);
			}else{boot()}
		}
		var go=document.getElementById("nlhv2-shgo");
		document.querySelectorAll(".nlhv2-shcard").forEach(function(c){
			c.addEventListener("click",function(){
				document.querySelectorAll(".nlhv2-shcard").forEach(function(x){x.classList.toggle("is-on",x===c)});
				st.dataset.glb=c.dataset.glb;
				// re-show a poster only while the 3D is not yet live; once live the
				// old model keeps rendering until the new one swaps in seamlessly
				if(c.dataset.poster&&!live){st.style.backgroundImage="url("+c.dataset.poster+")"}
				if(go&&c.dataset.href){go.href=c.dataset.href}
				var mv=st.querySelector("model-viewer");
				if(mv&&live){mv.setAttribute("src",c.dataset.glb)}
			});
		});
	})();
	document.querySelectorAll(".nlhv2-proj-live").forEach(function(b){
		b.addEventListener("click",function(){
			var wrap=document.getElementById("nlhv2-viewerwrap"),slot=document.getElementById("nlhv2-viewer-slot");
			if(!wrap||!slot||!b.dataset.glb){return}
			wrap.hidden=false;
			ensureMV(function(){
				var mv=slot.querySelector("model-viewer");
				if(!mv){mv=document.createElement("model-viewer");mv.setAttribute("camera-controls","");mv.setAttribute("shadow-intensity","0.6");mv.setAttribute("exposure","0.9");mv.setAttribute("touch-action","pan-y");mv.setAttribute("disable-zoom","");slot.appendChild(mv)}
				mv.setAttribute("src",b.dataset.glb);
				mv.setAttribute("alt",b.dataset.title||"");
				wrap.scrollIntoView({behavior:"smooth",block:"nearest"});
			});
		});
	});
});})();
' );
	}
}
add_action( 'wp_enqueue_scripts', 'nadlan_hv2_assets' );

if ( ! function_exists( 'nadlan_hv2_band_dronemap' ) ) {
	function nadlan_hv2_band_dronemap() {
		if ( ! function_exists( 'nadlan_drone_map_band' ) ) { return; }
		$lang = function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he';
		echo nadlan_drone_map_band( 'showcase', $lang ); // phpcs:ignore WordPress.Security.EscapeOutput
	}
}
