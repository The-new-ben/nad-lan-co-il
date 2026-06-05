<?php
/**
 * nadlan-config - GAP 5 geo search.
 *
 * Adds radius and bounding-box queries over the existing postmeta lat/lng model.
 * Paid placement still wins first; distance is the secondary ordering signal.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_geo_float' ) ) {
	function nadlan_geo_float( $value ) {
		return is_numeric( $value ) ? (float) $value : null;
	}
}

if ( ! function_exists( 'nadlan_geo_clamp_radius' ) ) {
	function nadlan_geo_clamp_radius( $radius_km ) {
		return max( 0.5, min( 100.0, (float) $radius_km ) );
	}
}

if ( ! function_exists( 'nadlan_geo_valid_lat_lng' ) ) {
	function nadlan_geo_valid_lat_lng( $lat, $lng ) {
		return is_numeric( $lat ) && is_numeric( $lng )
			&& (float) $lat >= -90 && (float) $lat <= 90
			&& (float) $lng >= -180 && (float) $lng <= 180;
	}
}

if ( ! function_exists( 'nadlan_geo_search_args' ) ) {
	function nadlan_geo_search_args( $args, $lat, $lng, $radius_km ) {
		$lat = (float) $lat;
		$lng = (float) $lng;
		$args['nadlan_geo'] = array(
			'lat'       => $lat,
			'lng'       => $lng,
			'radius_km' => nadlan_geo_clamp_radius( $radius_km ),
		);
		$args['orderby'] = 'none';
		$args['nadlan_paid_placement_boost'] = 1;
		return $args;
	}
}

if ( ! function_exists( 'nadlan_geo_box_args' ) ) {
	function nadlan_geo_box_args( $args, $lat_min, $lat_max, $lng_min, $lng_max ) {
		$lat_min = max( -90.0, min( 90.0, (float) $lat_min ) );
		$lat_max = max( -90.0, min( 90.0, (float) $lat_max ) );
		$lng_min = max( -180.0, min( 180.0, (float) $lng_min ) );
		$lng_max = max( -180.0, min( 180.0, (float) $lng_max ) );
		$args['nadlan_geo_box'] = array(
			'lat_min' => min( $lat_min, $lat_max ),
			'lat_max' => max( $lat_min, $lat_max ),
			'lng_min' => min( $lng_min, $lng_max ),
			'lng_max' => max( $lng_min, $lng_max ),
			'lat'     => ( $lat_min + $lat_max ) / 2,
			'lng'     => ( $lng_min + $lng_max ) / 2,
		);
		$args['orderby'] = 'none';
		$args['nadlan_paid_placement_boost'] = 1;
		return $args;
	}
}

if ( ! function_exists( 'nadlan_geo_distance_expr' ) ) {
	function nadlan_geo_distance_expr( $lat, $lng, $lat_cast, $lng_cast ) {
		global $wpdb;
		return $wpdb->prepare(
			"(6371.0088 * ACOS(LEAST(1.0, GREATEST(-1.0, COS(RADIANS(%f)) * COS(RADIANS({$lat_cast})) * COS(RADIANS({$lng_cast}) - RADIANS(%f)) + SIN(RADIANS(%f)) * SIN(RADIANS({$lat_cast}))))))",
			(float) $lat,
			(float) $lng,
			(float) $lat
		);
	}
}

if ( ! function_exists( 'nadlan_geo_clauses' ) ) {
	function nadlan_geo_clauses( $clauses, $query ) {
		$geo = $query->get( 'nadlan_geo' );
		$box = $query->get( 'nadlan_geo_box' );
		if ( empty( $geo ) && empty( $box ) ) {
			return $clauses;
		}

		global $wpdb;
		$lat_alias  = 'nadlan_geo_lat_pm';
		$lng_alias  = 'nadlan_geo_lng_pm';
		$tier_alias = 'nadlan_paid_tier_pm';

		if ( strpos( $clauses['join'], " AS {$lat_alias} " ) === false ) {
			$clauses['join'] .= $wpdb->prepare(
				" INNER JOIN {$wpdb->postmeta} AS {$lat_alias} ON ({$wpdb->posts}.ID = {$lat_alias}.post_id AND {$lat_alias}.meta_key = %s)",
				'lat'
			);
		}
		if ( strpos( $clauses['join'], " AS {$lng_alias} " ) === false ) {
			$clauses['join'] .= $wpdb->prepare(
				" INNER JOIN {$wpdb->postmeta} AS {$lng_alias} ON ({$wpdb->posts}.ID = {$lng_alias}.post_id AND {$lng_alias}.meta_key = %s)",
				'lng'
			);
		}
		if ( strpos( $clauses['join'], " AS {$tier_alias} " ) === false ) {
			$clauses['join'] .= $wpdb->prepare(
				" LEFT JOIN {$wpdb->postmeta} AS {$tier_alias} ON ({$wpdb->posts}.ID = {$tier_alias}.post_id AND {$tier_alias}.meta_key = %s)",
				'paid_tier'
			);
		}

		$lat_cast = "CAST({$lat_alias}.meta_value AS DECIMAL(10,6))";
		$lng_cast = "CAST({$lng_alias}.meta_value AS DECIMAL(10,6))";

		if ( ! empty( $box ) ) {
			$lat = (float) $box['lat'];
			$lng = (float) $box['lng'];
			$lat_min = (float) $box['lat_min'];
			$lat_max = (float) $box['lat_max'];
			$lng_min = (float) $box['lng_min'];
			$lng_max = (float) $box['lng_max'];
			$radius_km = null;
		} else {
			$lat = (float) $geo['lat'];
			$lng = (float) $geo['lng'];
			$radius_km = nadlan_geo_clamp_radius( $geo['radius_km'] ?? 25 );
			$lat_delta = $radius_km / 111.045;
			$lng_delta = $radius_km / ( 111.045 * max( 0.01, cos( deg2rad( $lat ) ) ) );
			$lat_min = max( -90.0, $lat - $lat_delta );
			$lat_max = min( 90.0, $lat + $lat_delta );
			$lng_min = max( -180.0, $lng - $lng_delta );
			$lng_max = min( 180.0, $lng + $lng_delta );
		}

		$clauses['where'] .= $wpdb->prepare(
			" AND {$lat_cast} BETWEEN %f AND %f AND {$lng_cast} BETWEEN %f AND %f",
			$lat_min,
			$lat_max,
			$lng_min,
			$lng_max
		);

		$distance_expr = nadlan_geo_distance_expr( $lat, $lng, $lat_cast, $lng_cast );
		$clauses['fields'] .= ", {$distance_expr} AS nadlan_distance_km";
		if ( $radius_km !== null ) {
			$clauses['where'] .= $wpdb->prepare( " AND {$distance_expr} <= %f", $radius_km );
		}
		$clauses['distinct'] = 'DISTINCT';
		$paid_order = "CASE {$tier_alias}.meta_value WHEN 'premier' THEN 2 WHEN 'pro' THEN 1 ELSE 0 END DESC";
		$incoming_order = trim( (string) ( $clauses['orderby'] ?? '' ) );
		if ( strpos( $incoming_order, "CASE {$tier_alias}.meta_value" ) !== false ) {
			$parts = explode( ',', $incoming_order, 2 );
			$paid_order = trim( $parts[0] );
		}
		$clauses['orderby'] = $paid_order . ", nadlan_distance_km ASC, {$wpdb->posts}.post_date DESC, {$wpdb->posts}.ID DESC";
		return $clauses;
	}
}
add_filter( 'posts_clauses', 'nadlan_geo_clauses', 30, 2 );

if ( ! function_exists( 'nadlan_geo_capture_post_distances' ) ) {
	function nadlan_geo_capture_post_distances( $posts, $query ) {
		if ( empty( $posts ) || ( ! $query->get( 'nadlan_geo' ) && ! $query->get( 'nadlan_geo_box' ) ) ) {
			return $posts;
		}
		if ( ! isset( $GLOBALS['nadlan_geo_distances'] ) || ! is_array( $GLOBALS['nadlan_geo_distances'] ) ) {
			$GLOBALS['nadlan_geo_distances'] = array();
		}
		foreach ( $posts as $post ) {
			if ( isset( $post->nadlan_distance_km ) ) {
				$GLOBALS['nadlan_geo_distances'][ (int) $post->ID ] = round( (float) $post->nadlan_distance_km, 2 );
			}
		}
		return $posts;
	}
}
add_filter( 'the_posts', 'nadlan_geo_capture_post_distances', 10, 2 );

add_filter( 'nadlan_geo_card_distance', function ( $distance, $post_id ) {
	$post_id = (int) $post_id;
	return isset( $GLOBALS['nadlan_geo_distances'][ $post_id ] ) ? (float) $GLOBALS['nadlan_geo_distances'][ $post_id ] : $distance;
}, 10, 2 );

if ( ! function_exists( 'nadlan_geo_rate_limit' ) ) {
	function nadlan_geo_rate_limit() {
		$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '0';
		$key = 'nadlan_geo_rl_' . md5( (string) $ip );
		$count = (int) get_transient( $key );
		if ( $count >= 8 ) {
			return new WP_Error( 'rate', 'יותר מדי בקשות.', array( 'status' => 429 ) );
		}
		set_transient( $key, $count + 1, MINUTE_IN_SECONDS );
		return true;
	}
}

if ( ! function_exists( 'nadlan_geo_post_type' ) ) {
	function nadlan_geo_post_type( $type ) {
		$type = sanitize_key( (string) $type );
		if ( $type === '' || $type === 'project' || $type === 'projects' || $type === 'nadlan_project' ) {
			return 'nadlan_project';
		}
		if ( $type === 'professional' || $type === 'professionals' || $type === 'nadlan_professional' ) {
			return 'nadlan_professional';
		}
		if ( $type === 'property' || $type === 'properties' || $type === 'nadlan_property' ) {
			return 'nadlan_property';
		}
		if ( $type === 'all' ) {
			return array( 'nadlan_project', 'nadlan_professional', 'nadlan_property' );
		}
		return null;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/near', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function ( $req ) {
			$limited = nadlan_geo_rate_limit();
			if ( is_wp_error( $limited ) ) { return $limited; }

			$post_type = nadlan_geo_post_type( $req->get_param( 'type' ) );
			if ( ! $post_type ) {
				return new WP_Error( 'invalid_type', 'type must be project, professional, property, or all', array( 'status' => 422 ) );
			}

			$per_page = min( 50, max( 1, absint( $req->get_param( 'per_page' ) ?: 24 ) ) );
			$args = array(
				'post_type'      => $post_type,
				'post_status'    => 'publish',
				'posts_per_page' => $per_page,
				'no_found_rows'  => true,
			);

			$has_box = $req->get_param( 'lat_min' ) !== null || $req->get_param( 'lat_max' ) !== null || $req->get_param( 'lng_min' ) !== null || $req->get_param( 'lng_max' ) !== null;
			if ( $has_box ) {
				$lat_min = $req->get_param( 'lat_min' );
				$lat_max = $req->get_param( 'lat_max' );
				$lng_min = $req->get_param( 'lng_min' );
				$lng_max = $req->get_param( 'lng_max' );
				if ( ! is_numeric( $lat_min ) || ! is_numeric( $lat_max ) || ! is_numeric( $lng_min ) || ! is_numeric( $lng_max ) ) {
					return new WP_Error( 'invalid_geo', 'bounding box values must be numeric', array( 'status' => 422 ) );
				}
				if ( (float) $lng_min > (float) $lng_max ) {
					return new WP_Error( 'antimeridian', 'antimeridian boxes are not supported yet', array( 'status' => 422 ) );
				}
				$args = nadlan_geo_box_args( $args, $lat_min, $lat_max, $lng_min, $lng_max );
			} else {
				$lat = $req->get_param( 'lat' );
				$lng = $req->get_param( 'lng' );
				if ( ! nadlan_geo_valid_lat_lng( $lat, $lng ) ) {
					return new WP_Error( 'invalid_geo', 'lat and lng must be numeric and in range', array( 'status' => 422 ) );
				}
				$radius = $req->get_param( 'radius_km' );
				$radius = is_numeric( $radius ) ? (float) $radius : 25.0;
				$args = nadlan_geo_search_args( $args, (float) $lat, (float) $lng, $radius );
			}

			$q = new WP_Query( $args );
			$results = array();
			foreach ( $q->posts as $post ) {
				$distance = isset( $post->nadlan_distance_km ) ? round( (float) $post->nadlan_distance_km, 2 ) : null;
				$results[] = array(
					'id'                 => (int) $post->ID,
					'title'              => get_the_title( $post ),
					'permalink'          => get_permalink( $post ),
					'paid_tier'          => (string) get_post_meta( $post->ID, 'paid_tier', true ),
					'nadlan_distance_km' => $distance,
				);
			}
			wp_reset_postdata();
			do_action( 'nadlan_geo_results', $results );
			return array(
				'ok'      => true,
				'count'   => count( $results ),
				'results' => $results,
			);
		},
	) );
} );

if ( ! function_exists( 'nadlan_geo_sample_count' ) ) {
	function nadlan_geo_sample_count() {
		global $wpdb;
		return (int) $wpdb->get_var(
			"SELECT COUNT(DISTINCT p.ID)
			 FROM {$wpdb->posts} p
			 INNER JOIN {$wpdb->postmeta} latm ON p.ID = latm.post_id AND latm.meta_key = 'lat'
			 INNER JOIN {$wpdb->postmeta} lngm ON p.ID = lngm.post_id AND lngm.meta_key = 'lng'
			 WHERE p.post_status = 'publish'
			   AND p.post_type IN ('nadlan_project','nadlan_professional','nadlan_property')"
		);
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['geo'] = array(
		'loaded'           => true,
		'sample_row_count' => nadlan_geo_sample_count(),
	);
	return $out;
} );
