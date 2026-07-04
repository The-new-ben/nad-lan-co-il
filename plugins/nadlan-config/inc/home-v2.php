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
		if ( has_post_thumbnail( $id ) ) { return get_the_post_thumbnail_url( $id, 'large' ); }
		$poster = (string) get_post_meta( $id, 'project_model_poster', true );
		if ( $poster ) { return $poster; }
		$photos = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) );
		return $photos ? $photos[0] : '';
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
		$hit = get_transient( 'nadlan_hv2_cities' );
		if ( is_array( $hit ) ) { return array_slice( $hit, 0, $limit ); }
		global $wpdb;
		$rows = $wpdb->get_results( "SELECT pm.meta_value city, p.post_type pt, COUNT(*) n
			FROM {$wpdb->postmeta} pm INNER JOIN {$wpdb->posts} p ON p.ID = pm.post_id
			WHERE pm.meta_key = 'city' AND pm.meta_value <> '' AND p.post_status = 'publish'
			AND p.post_type IN ('nadlan_project','nadlan_property')
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
		set_transient( 'nadlan_hv2_cities', $map, 12 * HOUR_IN_SECONDS );
		return array_slice( $map, 0, $limit );
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
				AND p.post_type = 'nadlan_project' AND p.post_status = 'publish'";
			if ( $city_like ) {
				$sql .= $wpdb->prepare( " AND p.ID IN (SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key='city' AND meta_value LIKE %s)", '%' . $wpdb->esc_like( $city_like ) . '%' );
			}
			return (int) $wpdb->get_var( $sql );
		};
		$snap['ppsqm_tlv']  = $avg( 'תל אביב' );
		$snap['ppsqm_il']   = $avg( '' );
		$snap['listings_n'] = (int) wp_count_posts( 'nadlan_property' )->publish;
		$snap['projects_n'] = (int) wp_count_posts( 'nadlan_project' )->publish;
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
		if ( empty( $s ) ) { $s = nadlan_hv2_snapshot_compute(); }
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
	<details><summary><?php nadlan_e( 'm_apts' ); ?></summary><div class="nlhv2-mega">
		<a href="<?php echo esc_url( home_url( '/properties/?listing_type=sale' ) ); ?>"><b><?php nadlan_e( 'apts_sale' ); ?></b></a>
		<a href="<?php echo esc_url( home_url( '/properties/?listing_type=rent' ) ); ?>"><b><?php nadlan_e( 'apts_rent' ); ?></b></a>
		<?php foreach ( $cities as $c ) : ?>
		<a href="<?php echo esc_url( home_url( '/properties/?city=' . rawurlencode( $c['name'] ) ) ); ?>"><?php nadlan_e( 'apts_in' ); ?><?php echo esc_html( $c['name'] ); ?></a>
		<?php endforeach; ?>
		<a href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>" class="nlhv2-mega-cta"><?php nadlan_e( 'post_free' ); ?></a>
	</div></details>
	<details><summary><?php nadlan_e( 'm_projects' ); ?></summary><div class="nlhv2-mega">
		<a href="<?php echo esc_url( home_url( '/projects/' ) ); ?>"><b><?php nadlan_e( 'all_projects' ); ?></b></a>
		<?php foreach ( array_slice( $cities, 0, 6 ) as $c ) : if ( ! $c['projects'] ) { continue; } ?>
		<a href="<?php echo esc_url( home_url( '/projects/?city=' . rawurlencode( $c['name'] ) ) ); ?>"><?php nadlan_e( 'projects_in' ); ?><?php echo esc_html( $c['name'] ); ?></a>
		<?php endforeach; ?>
		<a href="<?php echo esc_url( home_url( '/projects/?project_type=pinui_binui' ) ); ?>"><?php nadlan_e( 'pinui' ); ?></a>
		<a href="<?php echo esc_url( home_url( '/projects/?project_type=tama38' ) ); ?>"><?php nadlan_e( 'tama' ); ?></a>
	</div></details>
	<details><summary><?php nadlan_e( 'm_prices' ); ?></summary><div class="nlhv2-mega">
		<a href="<?php echo esc_url( home_url( '/property-value-estimator/' ) ); ?>"><b><?php nadlan_e( 'my_value' ); ?></b></a>
		<?php foreach ( array_slice( $cities, 0, 5 ) as $c ) : ?>
		<a href="<?php echo esc_url( home_url( '/projects/?city=' . rawurlencode( $c['name'] ) ) ); ?>"><?php nadlan_e( 'prices_in' ); ?><?php echo esc_html( $c['name'] ); ?></a>
		<?php endforeach; ?>
	</div></details>
	<details><summary><?php nadlan_e( 'm_guides' ); ?></summary><div class="nlhv2-mega">
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
</nav>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_hero' ) ) {
	function nadlan_hv2_band_hero() {
		$counts = array(
			'projects'      => (int) wp_count_posts( 'nadlan_project' )->publish,
			'professionals' => (int) wp_count_posts( 'nadlan_professional' )->publish,
		);
		$cities = nadlan_hv2_cities( 12 );
		$flag   = nadlan_hv2_featured_projects( 1 );
		$flag   = $flag ? $flag[0] : null;
		?>
	<section class="nlhv2-hero">
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
		<?php
		// Hero media (owner surgical spec 2026-07-02): the promo video lives HERE,
		// beside the H1, gif-like (autoplay muted loop, no controls), lazy-loaded
		// after page load so LCP is untouched. The Ashira card left the hero -
		// it was a duplicate of the projects band below. Flag card = fallback
		// only when no video is configured.
		$vurl    = trim( (string) get_option( 'nadlan_home_video_url', '' ) );
		$vwebm   = trim( (string) get_option( 'nadlan_home_video_webm', '' ) );
		$vposter = trim( (string) get_option( 'nadlan_home_video_poster', '' ) );
		if ( ( $vurl || $vwebm ) && preg_match( '~\.(mp4|webm)(\?|$)~i', $vurl . ' ' . $vwebm ) ) : ?>
		<div class="nlhv2-hero-flag nlhv2-hero-video" aria-label="נדלן - סרטון היכרות">
			<span class="nlhv2-hv-brand" aria-hidden="true">נדלן</span>
			<video id="nlhv2-hv" muted autoplay loop playsinline preload="auto"<?php echo $vposter ? ' poster="' . esc_url( $vposter ) . '"' : ''; ?>><?php
				// Native <source> children so the browser autoplays with ZERO JS
				// dependency (the data-* lazy pattern left desktop stuck on the poster).
				if ( $vwebm ) { echo '<source src="' . esc_url( $vwebm ) . '" type="video/webm">'; }
				if ( $vurl )  { echo '<source src="' . esc_url( $vurl ) . '" type="video/mp4">'; }
			?></video>
		</div>
		<?php elseif ( $flag ) : $fimg = nadlan_hv2_img( $flag->ID ); ?>
		<a class="nlhv2-hero-flag" href="<?php echo esc_url( get_permalink( $flag ) ); ?>">
			<span class="nlhv2-hero-flag-media"<?php echo $fimg ? ' style="background-image:url(' . esc_url( $fimg ) . ')"' : ''; ?>><em><?php nadlan_e( 'flag_pick' ); ?></em></span>
			<span class="nlhv2-hero-flag-cap"><b><?php echo esc_html( get_the_title( $flag ) ); ?></b><span><?php echo esc_html( get_post_meta( $flag->ID, 'city', true ) ); ?></span></span>
		</a>
		<?php endif; ?>
	</section>
		<?php
	}
}

if ( ! function_exists( 'nadlan_hv2_band_video' ) ) {
	function nadlan_hv2_band_video() {
		$url = trim( (string) get_option( 'nadlan_home_video_url', '' ) );
		if ( ! $url ) { return; }
		$embed = '';
		if ( preg_match( '~(?:youtube\.com/(?:watch\?v=|shorts/|embed/)|youtu\.be/)([A-Za-z0-9_-]{6,20})~', $url, $m ) ) {
			$embed = '<iframe src="https://www.youtube-nocookie.com/embed/' . esc_attr( $m[1] ) . '?rel=0&amp;modestbranding=1" title="נדלן - סרטון" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
		} elseif ( preg_match( '~vimeo\.com/(\d+)~', $url, $m ) ) {
			$embed = '<iframe src="https://player.vimeo.com/video/' . esc_attr( $m[1] ) . '" title="נדלן - סרטון" loading="lazy" allowfullscreen></iframe>';
		} elseif ( preg_match( '~\.(mp4|webm)(\?|$)~i', $url ) ) {
			$embed = '<video controls preload="metadata" playsinline src="' . esc_url( $url ) . '"></video>';
		}
		if ( ! $embed ) { return; }
		echo '<section class="nlhv2-band nlhv2-videoband" aria-label="סרטון היכרות"><header><p class="nlhv2-kicker">רגע לפני שמתחילים</p><h2>ככה בוחרים דירה בנדלן</h2></header><div class="nlhv2-video-frame">' . $embed . '</div></section>'; // phpcs:ignore
	}
}

if ( ! function_exists( 'nadlan_hv2_band_market' ) ) {
	function nadlan_hv2_band_market() {
		$s = (array) get_option( 'nadlan_market_snapshot', array() );
		$cards = array();
		if ( ! empty( $s['ppsqm_tlv'] ) ) { $cards[] = array( number_format( (int) $s['ppsqm_tlv'] ) . ' ₪', nadlan_i18n( 'mk_tlv' ), home_url( '/projects/?city=' . rawurlencode( 'תל אביב' ) ) ); }
		// Same honesty gate as the ticker: no fake "national" number from a TLV-only sample.
		if ( ! empty( $s['ppsqm_il'] ) && ( empty( $s['ppsqm_tlv'] ) || abs( (int) $s['ppsqm_il'] - (int) $s['ppsqm_tlv'] ) >= 0.2 * (int) $s['ppsqm_tlv'] ) ) { $cards[] = array( number_format( (int) $s['ppsqm_il'] ) . ' ₪', nadlan_i18n( 'mk_watch' ), home_url( '/projects/' ) ); }
		if ( ! empty( $s['yoy'] ) ) { $cards[] = array( esc_html( $s['yoy'] ), nadlan_i18n( 'mk_yoy' ), home_url( '/investment/' ) ); }
		if ( ! empty( $s['mortgage_rate'] ) ) { $cards[] = array( esc_html( $s['mortgage_rate'] ), nadlan_i18n( 'mk_rate' ), home_url( '/mortgage-calculator/' ) ); }
		if ( count( $cards ) < 2 ) { return; }
		$note = nadlan_i18n( 'mk_note_pre' ) . esc_html( ! empty( $s['updated'] ) ? $s['updated'] : current_time( 'd/m/Y' ) );
		echo '<section class="nlhv2-band"><header><h2>' . esc_html( nadlan_i18n( 'mk_title' ) ) . '</h2><span class="nlhv2-note">' . $note . '</span></header><div class="nlhv2-market">'; // phpcs:ignore
		foreach ( $cards as $c ) {
			echo '<a href="' . esc_url( $c[2] ) . '"><b>' . $c[0] . '</b><span>' . $c[1] . '</span></a>'; // phpcs:ignore
		}
		echo '</div></section>';
	}
}

if ( ! function_exists( 'nadlan_hv2_band_projects' ) ) {
	function nadlan_hv2_band_projects() {
		$projects = nadlan_hv2_featured_projects( 3 );
		if ( ! $projects ) { return; }
		?>
	<section class="nlhv2-dark">
		<header><p class="nlhv2-kicker"><?php nadlan_e( 'pj_kicker' ); ?></p><h2><?php nadlan_e( 'pj_title' ); ?></h2>
			<a class="nlhv2-dark-all" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>"><?php nadlan_e( 'pj_all' ); ?></a></header>
		<div class="nlhv2-projgrid">
			<?php foreach ( $projects as $p ) :
				$img = nadlan_hv2_img( $p->ID );
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
			$img = nadlan_hv2_img( $l->ID );
			$pr = (int) get_post_meta( $l->ID, 'price', true ); $rm = (float) get_post_meta( $l->ID, 'rooms', true );
			$sq = (int) get_post_meta( $l->ID, 'size_sqm', true ); $fl = get_post_meta( $l->ID, 'floor', true );
			echo '<a class="nlhv2-list" href="' . esc_url( get_permalink( $l ) ) . '">';
			echo '<span class="nlhv2-list-media"' . ( $img ? ' style="background-image:url(' . esc_url( $img ) . ')"' : '' ) . '></span>';
			echo '<b>' . ( $pr ? number_format( $pr ) . ' ₪' : esc_html( get_the_title( $l ) ) ) . '</b>';
			$bits = array_filter( array(
				$rm ? rtrim( rtrim( number_format( $rm, 1 ), '0' ), '.' ) . ' ' . nadlan_i18n( 'u_rooms' ) : '',
				$sq ? $sq . ' ' . nadlan_i18n( 'u_sqm' ) : '',
				$fl !== '' && $fl !== null ? nadlan_i18n( 'u_floor' ) . ' ' . esc_html( (string) $fl ) : '',
				(string) get_post_meta( $l->ID, 'city', true ),
			) );
			echo '<span>' . esc_html( implode( ' · ', $bits ) ) . '</span></a>';
		};
		?>
	<section class="nlhv2-band nlhv2-alt">
		<header><p class="nlhv2-kicker"><?php nadlan_e( 'ls_kicker' ); ?></p><h2><?php nadlan_e( 'ls_title' ); ?></h2>
			<a href="<?php echo esc_url( home_url( '/properties/' ) ); ?>"><?php nadlan_e( 'ls_all' ); ?></a></header>
		<div class="nlhv2-listtabs"><button type="button" class="is-on" data-pane="sale"><?php nadlan_e( 'tab_buy' ); ?></button><button type="button" data-pane="rent"><?php nadlan_e( 'tab_rent' ); ?></button></div>
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
				<span><?php echo $c['projects'] ? (int) $c['projects'] . ' ' . nadlan_i18n( 'ar_projects' ) : ''; ?><?php echo $c['projects'] && $c['properties'] ? ' · ' : ''; ?><?php echo $c['properties'] ? (int) $c['properties'] . ' ' . nadlan_i18n( 'ar_apts' ) : ''; ?></span>
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
				<span class="nlhv2-list-media"<?php echo $img ? ' style="background-image:url(' . esc_url( $img ) . ')"' : ''; ?>></span>
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
		<a href="<?php echo esc_url( home_url( '/en/' ) ); ?>">Explore in English →</a>
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
		$default = array( 'ticker', 'browse', 'hero', 'market', 'projects', 'listings', 'areas', 'magazine', 'tools', 'pros', 'intl', 'megafooter' ); // 'video' band retired: the promo lives in the hero card
		$bands   = get_option( 'nadlan_home_bands', $default );
		if ( ! is_array( $bands ) || ! $bands ) { $bands = $default; }
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
.nlhv2-browse{display:flex;gap:4px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding:6px 0 10px;margin-bottom:8px;position:relative;z-index:40}
.nlhv2-browse details{position:relative}
.nlhv2-browse summary{list-style:none;cursor:pointer;font-size:13.5px;font-weight:600;padding:9px 14px;border-radius:8px;user-select:none}
.nlhv2-browse summary::-webkit-details-marker{display:none}
.nlhv2-browse summary::after{content:" ▾";font-size:10px;color:var(--warm)}
.nlhv2-browse details[open] summary{background:var(--band)}
.nlhv2-mega{position:absolute;top:100%;inset-inline-start:0;min-width:230px;background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 18px 44px rgba(27,26,23,.14);padding:10px;display:grid;gap:2px;z-index:50}
.nlhv2-mega a{display:block;font-size:13.5px;color:var(--ink);text-decoration:none;padding:8px 10px;border-radius:7px}
.nlhv2-mega a:hover{background:var(--band)}
.nlhv2-mega a b{font-weight:700}
.nlhv2-mega-cta{color:var(--terra)!important;font-weight:700}
.nlhv2-hero{display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center;padding:30px 0 26px}
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
.nlhv2-hero-flag-media em{position:absolute;bottom:12px;inset-inline-start:12px;font-style:normal;font-size:12px;font-weight:700;background:rgba(27,26,23,.85);color:#E6D4AE;border-radius:6px;padding:6px 11px}
.nlhv2-hero-flag-cap{display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:12px 16px}
.nlhv2-hero-flag-cap b{font-family:var(--font-serif,serif);font-size:1.1rem}
.nlhv2-hero-flag-cap span{font-size:12.5px;color:var(--warm)}
.nlhv2-hero-video{position:relative;aspect-ratio:16/11;background:linear-gradient(160deg,#211F19,var(--dark));display:block}
.nlhv2-hero-video video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;opacity:1}
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
.nlhv2-list-media{display:block;aspect-ratio:4/3;background:var(--band) center/cover no-repeat;margin-bottom:8px}
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
.nlhv2-cta-tile{justify-content:center;background:var(--band);border-style:dashed}
.nlhv2-cta-tile b{color:var(--gold)}
.nlhv2-en{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;border-radius:16px;background:linear-gradient(160deg,#211F19,var(--dark));color:#FAF8F3;padding:26px 28px;margin:26px 0}
.nlhv2-en h2{color:#FAF8F3;font-size:1.4rem;margin:0 0 6px}
.nlhv2-en p{margin:0;font-size:13.5px;color:#C9C2B2;max-width:520px}
.nlhv2-en a{background:#E6D4AE;color:var(--ink);font-weight:700;font-size:14px;border-radius:9px;padding:13px 22px;text-decoration:none;white-space:nowrap}
.nlhv2-mfoot{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:22px;border-top:1px solid var(--line);padding:28px 0 10px}
.nlhv2-mfoot-col p{font-size:11.5px;font-weight:700;letter-spacing:.12em;color:var(--gold);margin:0 0 8px}
.nlhv2-mfoot-col a{display:block;font-size:13px;color:var(--warm);text-decoration:none;padding:4px 0}
.nlhv2-mfoot-col a:hover{color:var(--ink)}
.nlhv2-legal{font-size:11.5px;color:var(--warm);border-top:1px solid var(--line);padding:14px 0 20px;margin:16px 0 0}
@media(max-width:560px){.nlhv2-trust{gap:14px}.nlhv2-box button{padding:0 18px}.nlhv2-dark{margin:26px -14px;border-radius:0}}
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
	document.querySelectorAll(".nlhv2-proj-live").forEach(function(b){
		b.addEventListener("click",function(){
			var wrap=document.getElementById("nlhv2-viewerwrap"),slot=document.getElementById("nlhv2-viewer-slot");
			if(!wrap||!slot||!b.dataset.glb){return}
			wrap.hidden=false;
			ensureMV(function(){
				var mv=slot.querySelector("model-viewer");
				if(!mv){mv=document.createElement("model-viewer");mv.setAttribute("camera-controls","");mv.setAttribute("auto-rotate","");mv.setAttribute("shadow-intensity","0.6");mv.setAttribute("exposure","0.9");slot.appendChild(mv)}
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
