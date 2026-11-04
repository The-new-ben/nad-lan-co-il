<?php
/**
 * nadlan-config - Near finder v1: "find a property near me" (HAD-672, child HAD-673). Release 1.72.584.
 * Owner order 4.11.2026 (Ben, through the coordinator) and its three addenda the same day; design "NadLan Instruments"
 * (Claude Design canvas https://claude.ai/artifact/4bwg1ozXd9wjXK42CuAC7y: Main, Card, Desktop).
 *
 * Where it shows (one condition, nadlan_nf_context()):
 *  - /properties/ (owns "דירות למכירה"): the inline section + the launcher (sale tab);
 *  - the home page: the launcher only (sale tab); nothing else on the page changes;
 *  - the rent page /דירות-להשכרה/ (page 8648, owns "דירות להשכרה"): the launcher only (rent tab); its title, H1 and text stay;
 *  - a broker's own pages (Meital Katzir: her card 7833 and her site /brokers/meital-katzir/): her listings only, no projects,
 *    no ads, no other broker, no "add your property" line (inc/property-owner.php: a listing that belongs to someone is that
 *    person's page, not a portal page);
 *  - never /projects/ or a project page.
 * The launcher ("חפשו נכס לידי", on a broker's page "הנכסים שלה לידכם") opens a full-screen dialog; its deep link is #lidi.
 *
 * What it adds, additive only:
 *  - REST GET /nadlan/v1/near-finder[?broker=ID] (public, no personal data, cached 10 minutes). Listings: post_status
 *    publish only (the free wizard creates 'pending', so an admin's approval is the moderation gate), never a demo
 *    (nadlan_pl_is_demo, IDs 4951-4957 today), never rented or sold, never one an admin hid with meta nadlan_nf_hidden = '1'.
 *    A listing with no coordinates of its own is placed at its neighbourhood (table below), else at its city, and marked
 *    approx: never an address. Projects: the projects map's own payload (nadlan_drone_map_data, inc/drone-map.php), only the
 *    confidences that are real points (compound, parcel, address); 'city' and '' are not points.
 *  - promoted: true while a paid tier is active (inc/advertiser-orders.php: paid_tier pro/premier and campaign_end still
 *    ahead; product 490 for a listing, 489 for a project). Shown as one quiet "מודעה מקודמת". Never on a broker's page.
 *  - nadlan_nf_render(): the inline section (H2 + one answer paragraph + the app root + the owners' quiet line), printed by
 *    nadlan_pl_render() (inc/archive-grid.php, one guarded line before the old map line) and by [nadlan_near_finder].
 *  - nadlan_nf_launcher(): the launcher + its dialog, printed in wp_footer. Without the inline section the dialog carries
 *    its own app root and no heading (the page's outline is unchanged).
 *  - assets/near-finder/finder.js + finder.css, enqueued only where nadlan_nf_context() says so (version = the plugin's).
 *  - An admin-only side box on listings and projects: "hide from the map" (meta nadlan_nf_hidden, never in REST).
 * No negative layer of any kind (no hazards, fuel, soil or asbestos): distances, the sea, my places.
 * The visitor's own location never leaves the page: it is not in a URL and not sent here.
 *
 * v3 (release 1.72.586, the counted benchmark of 4.11.2026: draw a zone, full filters, travel time, the phone sheet):
 *  - each listing row also carries floor (int, or null when the listing does not state it), elevator, parking (true only
 *    when the listing says so) and balcony (m², 0 when none is stated), via nadlan_nf_extras(); the finder shows a filter
 *    only when at least one listing has that fact. The cache key moved to nadlan_nf_v3 (the payload gained fields).
 *  - the travel-time area is the one place a point leaves the browser: the visitor's chosen place (or location), rounded to
 *    about 100 m, goes to the Mapbox Isochrone API only, only when the visitor asks for it, never here (finder.js).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NADLAN_NF_CACHE' ) ) {
	define( 'NADLAN_NF_CACHE', 'nadlan_nf_v3' ); // bump on a rerun after a rollback (a rolled-back run leaves its transient); v3: floor, elevator, parking, balcony
}

if ( ! function_exists( 'nadlan_nf_extras' ) ) {
	/**
	 * The facts the v3 filters use, only as the listing states them (never a guess):
	 *  floor:    an apartment's floor (0 = ground); null when not stated, when the type has no floor (a house, a plot) or
	 *            when it reads 0 with no building height (the empty default of the wizard);
	 *  elevator, parking: true only when the listing says so (an empty value is not "no", it is "not stated");
	 *  balcony:  the balcony's m² when stated, else 0.
	 */
	function nadlan_nf_extras( $id ) {
		$yes   = array( '1', 'true', 'yes', 'on', 'כן' );
		$ptype = (string) get_post_meta( $id, 'property_type', true );
		$floor = null;
		$raw   = trim( (string) get_post_meta( $id, 'floor', true ) );
		if ( in_array( $ptype, array( 'apartment', 'penthouse', 'duplex', 'studio', 'garden', 'office', '' ), true ) && '' !== $raw && is_numeric( $raw ) ) {
			$f     = (int) round( (float) $raw );
			$total = (int) round( (float) get_post_meta( $id, 'total_floors', true ) );
			if ( $f >= -3 && $f <= 120 && ( 0 !== $f || $total > 0 || 'garden' === $ptype ) ) { $floor = $f; }
		}
		$park = strtolower( trim( (string) get_post_meta( $id, 'parking', true ) ) );
		$balc = (float) get_post_meta( $id, 'balcony_sqm', true );
		return array(
			'floor'    => $floor,
			'elevator' => in_array( strtolower( trim( (string) get_post_meta( $id, 'elevator', true ) ) ), $yes, true ),
			'parking'  => in_array( $park, $yes, true ) || ( is_numeric( $park ) && (float) $park > 0 ),
			'balcony'  => $balc > 0 && $balc < 1000 ? (int) round( $balc ) : 0,
		);
	}
}

if ( ! function_exists( 'nadlan_nf_norm' ) ) {
	/** A place name as a key: no hyphen or maqaf, single spaces ("תל אביב-יפו" = "תל אביב יפו"). */
	function nadlan_nf_norm( $s ) {
		$s = html_entity_decode( (string) $s, ENT_QUOTES, 'UTF-8' );
		$s = preg_replace( '/[\x{05BE}\x{2010}\x{2011}\-]+/u', ' ', $s );
		$s = trim( preg_replace( '/\s+/u', ' ', $s ) );
		return str_replace( array( 'הרצלייה', 'פתח תקוה' ), array( 'הרצליה', 'פתח תקווה' ), $s );
	}
}

if ( ! function_exists( 'nadlan_nf_hoods' ) ) {
	/**
	 * Neighbourhood centroids, key "city|neighbourhood" (both normalized) => array( lat, lng, display name ).
	 * Source: OpenStreetMap Nominatim, search API, 4.11.2026 (11 requests, 1 a second), place type "suburb".
	 * Left out on purpose: "מגדלי נאמן" (Nominatim returns the building itself; a pin there would be the address, so
	 * those listings fall to their neighbourhood "צוקי אביב") and "שפירא, אופקים" (Nominatim returned another street;
	 * that listing falls to the city of Ofakim). Add a row only from a named source, with its date.
	 */
	function nadlan_nf_hoods() {
		return array(
			'תל אביב יפו|נופי ים'     => array( 32.11481, 34.78729, 'נופי ים' ),     // OSM way 819842290
			'תל אביב יפו|רמת אביב'    => array( 32.10886, 34.79509, 'רמת אביב' ),    // OSM way 819845420
			'תל אביב יפו|שרונה'       => array( 32.07069, 34.78491, 'שרונה' ),       // OSM way 819219037
			'תל אביב יפו|צוקי אביב'   => array( 32.13103, 34.79121, 'צוקי אביב' ),   // OSM way 819839404
			'תל אביב יפו|כוכב הצפון'  => array( 32.10074, 34.78459, 'כוכב הצפון' ),  // OSM way 819855107
			'הרצליה|הרצליה פיתוח'     => array( 32.17394, 34.80818, 'הרצליה פיתוח' ), // OSM node 1025002630
		);
	}
}

if ( ! function_exists( 'nadlan_nf_cities' ) ) {
	/** City centroids, normalized name => array( lat, lng ). Own rows first (OSM Nominatim 4.11.2026 for יבנאל, קרית אתא,
	 *  אופקים; תל אביב יפו and הרצליה as in nadlan_cp_city_coords), then the catalogue's table when it is loaded. */
	function nadlan_nf_cities() {
		static $c = null;
		if ( null !== $c ) { return $c; }
		$c = array(
			'תל אביב יפו' => array( 32.0853, 34.7818 ),
			'הרצליה'      => array( 32.1663, 34.8433 ),
			'יבנאל'       => array( 32.70546, 35.50526 ), // OSM relation 1387228
			'קרית אתא'    => array( 32.81159, 35.11637 ), // OSM relation 1387454
			'אופקים'      => array( 31.31258, 34.62085 ), // OSM relation 1379102
		);
		if ( function_exists( 'nadlan_cp_city_coords' ) ) {
			foreach ( (array) nadlan_cp_city_coords() as $name => $ll ) {
				$k = nadlan_nf_norm( $name );
				if ( ! isset( $c[ $k ] ) && is_array( $ll ) && 2 === count( $ll ) ) { $c[ $k ] = array( (float) $ll[0], (float) $ll[1] ); }
			}
		}
		return $c;
	}
}

if ( ! function_exists( 'nadlan_nf_place' ) ) {
	/** Where a listing goes on the map: its own point, else its neighbourhood, else its city. approx = '' | 'hood' | 'city' | 'none'. */
	function nadlan_nf_place( $id, $city, $hood ) {
		$lat = (float) get_post_meta( $id, 'lat', true );
		$lng = (float) get_post_meta( $id, 'lng', true );
		if ( $lat && $lng && abs( $lat ) <= 90 && abs( $lng ) <= 180 ) {
			return array( 'lat' => round( $lat, 5 ), 'lng' => round( $lng, 5 ), 'approx' => '', 'area' => '' );
		}
		$ck = nadlan_nf_norm( $city );
		$hoods = nadlan_nf_hoods();
		if ( '' !== trim( (string) $hood ) ) {
			$parts = array_merge( array( $hood ), preg_split( '/[,،\/]+/u', (string) $hood ) );
			foreach ( $parts as $p ) {
				$k = $ck . '|' . nadlan_nf_norm( $p );
				if ( isset( $hoods[ $k ] ) ) {
					return array( 'lat' => $hoods[ $k ][0], 'lng' => $hoods[ $k ][1], 'approx' => 'hood', 'area' => $hoods[ $k ][2] );
				}
			}
		}
		$cities = nadlan_nf_cities();
		if ( '' !== $ck && isset( $cities[ $ck ] ) ) {
			return array( 'lat' => $cities[ $ck ][0], 'lng' => $cities[ $ck ][1], 'approx' => 'city', 'area' => trim( (string) $city ) );
		}
		return array( 'lat' => null, 'lng' => null, 'approx' => 'none', 'area' => '' );
	}
}

if ( ! function_exists( 'nadlan_nf_promoted_ids' ) ) {
	/** Posts of one type whose paid tier is active now (inc/advertiser-orders.php: paid_tier + campaign_end). One query. */
	function nadlan_nf_promoted_ids( $pt ) {
		$now = current_time( 'timestamp' ); // the same clock advertiser-orders.php writes campaign_end with
		$ids = get_posts( array(
			'post_type' => $pt, 'post_status' => 'publish', 'posts_per_page' => -1, 'fields' => 'ids', 'no_found_rows' => true,
			'suppress_filters' => true,
			'meta_query' => array( 'relation' => 'AND',
				array( 'key' => 'paid_tier', 'value' => array( 'pro', 'premier' ), 'compare' => 'IN' ),
				array( 'key' => 'campaign_end', 'value' => $now, 'compare' => '>', 'type' => 'NUMERIC' ),
			),
		) );
		return array_flip( array_map( 'intval', (array) $ids ) );
	}
}

if ( ! function_exists( 'nadlan_nf_hidden_ids' ) ) {
	/** Listings and projects an admin pulled from the finder (meta nadlan_nf_hidden = '1'). One query. */
	function nadlan_nf_hidden_ids() {
		$ids = get_posts( array(
			'post_type' => array( 'nadlan_property', 'nadlan_project' ), 'post_status' => 'any', 'posts_per_page' => -1,
			'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
			'meta_query' => array( array( 'key' => 'nadlan_nf_hidden', 'value' => '1' ) ),
		) );
		return array_flip( array_map( 'intval', (array) $ids ) );
	}
}

if ( ! function_exists( 'nadlan_nf_thumbs' ) ) {
	/** id => the featured image at size 'medium' (never the full file), for many posts in three queries. */
	function nadlan_nf_thumbs( $ids ) {
		global $wpdb;
		$ids = array_values( array_filter( array_map( 'intval', (array) $ids ) ) );
		$map = array();
		foreach ( array_chunk( $ids, 400 ) as $chunk ) {
			$in   = implode( ',', $chunk ); // integers only
			$rows = $wpdb->get_results( "SELECT post_id, meta_value FROM {$wpdb->postmeta} WHERE meta_key = '_thumbnail_id' AND post_id IN ($in)" ); // phpcs:ignore
			foreach ( (array) $rows as $r ) { if ( (int) $r->meta_value > 0 ) { $map[ (int) $r->post_id ] = (int) $r->meta_value; } }
		}
		if ( ! $map ) { return array(); }
		if ( function_exists( '_prime_post_caches' ) ) { _prime_post_caches( array_values( array_unique( $map ) ), false, true ); }
		$out = array();
		foreach ( $map as $pid => $aid ) {
			$src = wp_get_attachment_image_src( $aid, 'medium' );
			if ( $src && ! empty( $src[0] ) ) { $out[ $pid ] = esc_url_raw( $src[0] ); }
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_nf_is_demo' ) ) {
	function nadlan_nf_is_demo( $id ) {
		if ( function_exists( 'nadlan_pl_is_demo' ) ) { return nadlan_pl_is_demo( $id ); }
		return in_array( (string) get_post_meta( $id, 'is_demo', true ), array( '1', 'true' ), true ) || 'demo_seed' === (string) get_post_meta( $id, 'source', true );
	}
}

if ( ! function_exists( 'nadlan_nf_listings' ) ) {
	/** $broker > 0: that broker's own listings only (meta nl_broker_id), with no promotion flag (her page carries no ads). */
	function nadlan_nf_listings( $hidden, $broker = 0 ) {
		$posts = get_posts( array(
			'post_type' => 'nadlan_property', 'post_status' => 'publish', 'posts_per_page' => 300, 'no_found_rows' => true,
			'orderby' => 'date', 'order' => 'DESC', 'suppress_filters' => true,
		) );
		$promo = $broker > 0 ? array() : nadlan_nf_promoted_ids( 'nadlan_property' );
		$types = array( 'apartment' => 'דירה', 'penthouse' => 'פנטהאוז', 'garden' => 'דירת גן', 'cottage' => 'קוטג׳', 'villa' => 'בית פרטי', 'duplex' => 'דופלקס', 'studio' => 'סטודיו', 'house' => 'בית פרטי', 'land' => 'מגרש', 'office' => 'משרד' );
		$gone  = array( 'rented', 'sold', 'מושכר', 'נמכר', 'הושכר' );
		$yes   = array( '1', 'true', 'yes', 'on' );
		$rows  = array();
		$need  = array();
		foreach ( $posts as $p ) {
			$id = (int) $p->ID;
			if ( isset( $hidden[ $id ] ) || nadlan_nf_is_demo( $id ) ) { continue; }
			if ( $broker > 0 && (string) $broker !== trim( (string) get_post_meta( $id, 'nl_broker_id', true ) ) ) { continue; }
			$st  = strtolower( trim( (string) get_post_meta( $id, 'status', true ) ) );
			$nst = strtolower( trim( (string) get_post_meta( $id, 'nl_status', true ) ) );
			if ( in_array( $st, $gone, true ) || in_array( $nst, $gone, true ) ) { continue; }
			$deal = (string) get_post_meta( $id, 'listing_type', true );
			if ( ! in_array( $deal, array( 'sale', 'rent' ), true ) ) { continue; }
			$city = trim( (string) get_post_meta( $id, 'city', true ) );
			$hood = trim( (string) get_post_meta( $id, 'neighborhood', true ) );
			$pl   = nadlan_nf_place( $id, $city, $hood );
			$price = (float) get_post_meta( $id, 'price', true );
			$rooms = (float) get_post_meta( $id, 'rooms', true );
			$sqm   = (float) get_post_meta( $id, 'size_sqm', true );
			$rows[ $id ] = nadlan_nf_extras( $id ) + array( // v3: floor, elevator, parking, balcony first; the v1 keys follow as before
				'id'       => $id,
				'url'      => get_permalink( $id ),
				'title'    => html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ),
				'deal'     => $deal,
				'ptype'    => $types[ (string) get_post_meta( $id, 'property_type', true ) ] ?? '',
				'price'    => $price > 0 ? (int) round( $price ) : 0,
				'rooms'    => $rooms > 0 ? $rooms : 0,
				'sqm'      => $sqm > 0 ? (int) round( $sqm ) : 0,
				// the listing's own published ₪/m² wins over price / size, so the map never shows a second figure
				'psqm'     => max( 0, (int) round( (float) get_post_meta( $id, 'price_per_sqm', true ) ) ),
				'mamad'    => in_array( strtolower( (string) get_post_meta( $id, 'protected_room', true ) ), $yes, true ),
				'city'     => $city,
				'hood'     => $hood,
				'area'     => $pl['area'],
				'img'      => '',
				'lat'      => $pl['lat'],
				'lng'      => $pl['lng'],
				'approx'   => $pl['approx'],
				'promoted' => isset( $promo[ $id ] ),
			);
			$need[] = $id;
		}
		$th = nadlan_nf_thumbs( $need );
		foreach ( $rows as $id => $r ) {
			if ( isset( $th[ $id ] ) ) { $rows[ $id ]['img'] = $th[ $id ]; continue; }
			// no featured image: the listing's first own photo, at 'medium' when it is a media-library file; never a full file
			$csv = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) );
			$first = $csv ? reset( $csv ) : '';
			if ( '' !== $first ) {
				$aid = attachment_url_to_postid( $first );
				$src = $aid ? wp_get_attachment_image_src( $aid, 'medium' ) : false;
				if ( $src && ! empty( $src[0] ) ) { $rows[ $id ]['img'] = esc_url_raw( $src[0] ); }
			}
		}
		return array_values( $rows );
	}
}

if ( ! function_exists( 'nadlan_nf_projects' ) ) {
	function nadlan_nf_projects( $hidden ) {
		if ( ! function_exists( 'nadlan_drone_map_data' ) ) { return array(); }
		$d     = nadlan_drone_map_data();
		$ok    = array( 'compound-verified' => 1, 'parcel-centroid-verified' => 1, 'address' => 1, 'address-approx' => 1 );
		$promo = nadlan_nf_promoted_ids( 'nadlan_project' );
		$rows  = array();
		foreach ( (array) ( $d['items'] ?? array() ) as $it ) {
			$id = (int) ( $it['id'] ?? 0 );
			if ( ! $id || isset( $hidden[ $id ] ) || ! isset( $ok[ (string) ( $it['conf'] ?? '' ) ] ) ) { continue; }
			$lat = (float) ( $it['lat'] ?? 0 );
			$lng = (float) ( $it['lng'] ?? 0 );
			if ( ! $lat || ! $lng ) { continue; }
			$st = (string) ( $it['status'] ?? '' );
			$rows[ $id ] = array(
				'id'       => $id,
				'url'      => (string) ( $it['url'] ?? '' ),
				'title'    => html_entity_decode( (string) ( $it['title'] ?? '' ), ENT_QUOTES, 'UTF-8' ),
				'city'     => (string) ( $it['city'] ?? '' ),
				'status'   => in_array( $st, array( 'marketing', 'construction', 'planning' ), true ) ? $st : '',
				'units'    => max( 0, (int) ( $it['units'] ?? 0 ) ),
				'psqm'     => max( 0, (int) round( (float) ( $it['psqm'] ?? 0 ) ) ),
				'img'      => '',
				'lat'      => round( $lat, 5 ),
				'lng'      => round( $lng, 5 ),
				'exact'    => 'address-approx' !== (string) $it['conf'],
				'promoted' => isset( $promo[ $id ] ),
			);
		}
		foreach ( nadlan_nf_thumbs( array_keys( $rows ) ) as $id => $src ) { $rows[ $id ]['img'] = $src; }
		return array_values( $rows );
	}
}

if ( ! function_exists( 'nadlan_nf_brokers' ) ) {
	/** The brokers whose own pages carry the finder (Ben 4.11.2026: Meital Katzir, card 7833). */
	function nadlan_nf_brokers() { return array_values( array_filter( array_map( 'intval', (array) apply_filters( 'nadlan_nf_brokers', array( 7833 ) ) ) ) ); }
}

if ( ! function_exists( 'nadlan_nf_data' ) ) {
	/** The finder's payload. $broker > 0: a broker's own page (her listings only, no projects, no ads). */
	function nadlan_nf_data( $broker = 0 ) {
		$broker = max( 0, (int) $broker );
		$key = NADLAN_NF_CACHE . ( $broker ? '_b' . $broker : '' );
		$c = get_transient( $key );
		if ( is_array( $c ) && ! empty( $c['ok'] ) ) { return $c; }
		$hidden = nadlan_nf_hidden_ids();
		$out = array(
			'ok'       => true,
			'mode'     => $broker ? 'broker' : 'portal',
			'listings' => nadlan_nf_listings( $hidden, $broker ),
			'projects' => $broker ? array() : nadlan_nf_projects( $hidden ),
			'updated'  => gmdate( 'c' ),
		);
		set_transient( $key, $out, 10 * MINUTE_IN_SECONDS );
		return $out;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/near-finder', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'args' => array( 'broker' => array( 'type' => 'integer', 'minimum' => 0, 'required' => false ) ),
		'callback' => function ( $req ) {
			$b = absint( $req->get_param( 'broker' ) );
			if ( $b && 'nadlan_professional' !== get_post_type( $b ) ) { // not a professional: an empty list, never the portal's
				$d = array( 'ok' => true, 'mode' => 'broker', 'listings' => array(), 'projects' => array(), 'updated' => gmdate( 'c' ) );
			} else {
				$d = nadlan_nf_data( $b );
			}
			$r = new WP_REST_Response( $d, 200 );
			$r->header( 'Cache-Control', 'public, max-age=300' );
			return $r;
		},
	) );
} );

if ( ! function_exists( 'nadlan_nf_flush' ) ) {
	function nadlan_nf_flush() {
		delete_transient( NADLAN_NF_CACHE );
		foreach ( nadlan_nf_brokers() as $b ) { delete_transient( NADLAN_NF_CACHE . '_b' . $b ); }
	}
}
add_action( 'save_post_nadlan_property', 'nadlan_nf_flush' );
add_action( 'save_post_nadlan_project', 'nadlan_nf_flush' );
add_action( 'nadlan_advertiser_paid_tier_activated', 'nadlan_nf_flush' );
add_action( 'nadlan_advertiser_paid_tier_expired', 'nadlan_nf_flush' );
foreach ( array( 'added_post_meta', 'updated_post_meta', 'deleted_post_meta' ) as $nadlan_nf_hook ) {
	// a status, a price or a paid tier changed by code without save_post (the broker's "rented" button, the daily downgrade)
	add_action( $nadlan_nf_hook, function ( $mid, $pid, $key ) {
		if ( in_array( (string) $key, array( 'nadlan_nf_hidden', 'nl_status', 'status', 'price', 'paid_tier', 'campaign_end', 'lat', 'lng', 'neighborhood', 'city', 'nl_broker_id',
				'rooms', 'size_sqm', 'floor', 'total_floors', 'elevator', 'parking', 'balcony_sqm', 'protected_room' ), true ) // v3: the filters' facts
			&& in_array( get_post_type( (int) $pid ), array( 'nadlan_property', 'nadlan_project' ), true ) ) {
			nadlan_nf_flush();
		}
	}, 10, 3 );
}
unset( $nadlan_nf_hook );

/* ---------------------------------------------------------------- the admin's off switch (admin-only, not in REST) */
add_action( 'add_meta_boxes', function () {
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	foreach ( array( 'nadlan_property', 'nadlan_project' ) as $pt ) {
		add_meta_box( 'nadlan_nf_box', 'מפת החיפוש לפי מיקום', function ( $post ) {
			wp_nonce_field( 'nadlan_nf_hide_' . $post->ID, 'nadlan_nf_nonce' );
			echo '<p><label><input type="checkbox" name="nadlan_nf_hidden" value="1"' . checked( '1', (string) get_post_meta( $post->ID, 'nadlan_nf_hidden', true ), false ) . '> להסתיר מהמפה</label></p>';
			echo '<p class="description">הפרסום נשאר כמו שהוא. רק לא מוצג במפת החיפוש לפי מיקום.</p>';
		}, $pt, 'side', 'low' );
	}
} );
add_action( 'save_post', function ( $post_id, $post ) {
	if ( ! $post || ! in_array( $post->post_type, array( 'nadlan_property', 'nadlan_project' ), true ) ) { return; }
	if ( wp_is_post_autosave( $post_id ) || wp_is_post_revision( $post_id ) || ! isset( $_POST['nadlan_nf_nonce'] ) ) { return; }
	if ( ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_nf_nonce'] ) ), 'nadlan_nf_hide_' . $post_id ) || ! current_user_can( 'manage_options' ) ) { return; }
	if ( ! empty( $_POST['nadlan_nf_hidden'] ) ) {
		update_post_meta( $post_id, 'nadlan_nf_hidden', '1' );
	} else {
		delete_post_meta( $post_id, 'nadlan_nf_hidden' );
	}
	nadlan_nf_flush();
}, 30, 2 );

/* ---------------------------------------------------------------- where it shows: one condition */
if ( ! function_exists( 'nadlan_nf_rent_page' ) ) {
	/** The rent page /דירות-להשכרה/ (it owns "דירות להשכרה"): the launcher only, rent tab. Its title, H1 and text are not touched. */
	function nadlan_nf_rent_page() { return (int) apply_filters( 'nadlan_nf_rent_page', 8648 ); }
}
if ( ! function_exists( 'nadlan_nf_broker_here' ) ) {
	/** The broker whose own page this is: her professional card, or her site page (nl_site_he, or /brokers/<her slug>/). */
	function nadlan_nf_broker_here() {
		static $b = null;
		if ( null !== $b ) { return $b; }
		$b = 0;
		if ( ! is_singular() ) { return $b; }
		$id = (int) get_queried_object_id();
		foreach ( nadlan_nf_brokers() as $bid ) {
			if ( 'publish' !== get_post_status( $bid ) || 'nadlan_professional' !== get_post_type( $bid ) ) { continue; }
			if ( $id === $bid || $id === (int) get_post_meta( $bid, 'nl_site_he', true ) ) { $b = $bid; break; }
			foreach ( array_unique( array_filter( array( trim( (string) get_post_meta( $bid, 'nl_slug', true ) ), (string) get_post_field( 'post_name', $bid ) ) ) ) as $slug ) {
				$pg = get_page_by_path( 'brokers/' . $slug, OBJECT, 'page' );
				if ( $pg && (int) $pg->ID === $id ) { $b = $bid; break 2; }
			}
		}
		return $b;
	}
}
if ( ! function_exists( 'nadlan_nf_context' ) ) {
	/** Where the finder shows and how. Empty = not on this page (never /projects/ or a project page). */
	function nadlan_nf_context() {
		static $c = null;
		if ( null !== $c ) { return $c; }
		$c = array();
		if ( is_admin() || is_feed() || ( function_exists( 'wp_is_json_request' ) && wp_is_json_request() ) ) { return $c; }
		$portal = 'דירות למכירה ולהשכרה על המפה';
		$label  = 'חפשו נכס לידי';
		if ( is_post_type_archive( 'nadlan_property' ) ) {
			$c = array( 'mode' => 'portal', 'deal' => '', 'title' => $portal, 'label' => $label, 'inline' => true, 'broker' => 0 );
		} elseif ( is_front_page() ) {
			$c = array( 'mode' => 'portal', 'deal' => 'sale', 'title' => $portal, 'label' => $label, 'inline' => false, 'broker' => 0 );
		} elseif ( nadlan_nf_rent_page() > 0 && is_page( nadlan_nf_rent_page() ) ) {
			$c = array( 'mode' => 'portal', 'deal' => 'rent', 'title' => 'דירות להשכרה על המפה', 'label' => $label, 'inline' => false, 'broker' => 0 );
		} else {
			$bid = nadlan_nf_broker_here();
			if ( $bid > 0 ) {
				$bk    = function_exists( 'nl_drop_broker' ) ? nl_drop_broker( $bid ) : null;
				$parts = preg_split( '/\s*·\s*/u', html_entity_decode( get_the_title( $bid ), ENT_QUOTES, 'UTF-8' ) );
				$name  = $bk && ! empty( $bk['name_he'] ) ? (string) $bk['name_he'] : trim( (string) $parts[0] );
				$g     = (string) get_post_meta( $bid, 'nl_gender', true );
				$lab   = 'f' === $g ? 'הנכסים שלה לידכם' : ( 'm' === $g ? 'הנכסים שלו לידכם' : 'נכסים לידכם' );
				$c = array( 'mode' => 'broker', 'deal' => 'sale', 'title' => 'הנכסים של ' . $name . ' על המפה', 'label' => $lab, 'inline' => false, 'broker' => $bid );
			} else {
				$p = is_singular() ? get_post() : null;
				if ( $p && has_shortcode( (string) $p->post_content, 'nadlan_near_finder' ) ) {
					$c = array( 'mode' => 'portal', 'deal' => '', 'title' => $portal, 'label' => $label, 'inline' => true, 'broker' => 0, 'shortcode' => true );
				}
			}
		}
		return $c;
	}
}

/* ---------------------------------------------------------------- assets: only where the finder shows */
if ( ! function_exists( 'nadlan_nf_url' ) ) {
	function nadlan_nf_url( $rel ) { return plugins_url( 'assets/near-finder/' . $rel, dirname( __DIR__ ) . '/nadlan-config.php' ); } // the plugin root, not inc/
}
if ( ! function_exists( 'nadlan_nf_register' ) ) {
	function nadlan_nf_register() {
		$v = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
		if ( ! wp_style_is( 'nadlan-nli-fonts', 'registered' ) ) {
			wp_register_style( 'nadlan-nli-fonts', 'https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap', array(), null );
		}
		if ( ! wp_style_is( 'nadlan-nf', 'registered' ) ) { wp_register_style( 'nadlan-nf', nadlan_nf_url( 'finder.css' ), array( 'nadlan-nli-fonts' ), $v ); }
		if ( ! wp_script_is( 'nadlan-nf', 'registered' ) ) { wp_register_script( 'nadlan-nf', nadlan_nf_url( 'finder.js' ), array(), $v, true ); }
	}
}
add_action( 'wp_enqueue_scripts', function () {
	if ( ! nadlan_nf_context() ) { return; }
	nadlan_nf_register();
	wp_enqueue_style( 'nadlan-nf' );
	wp_enqueue_script( 'nadlan-nf' );
}, 20 );
add_filter( 'script_loader_tag', function ( $tag, $handle ) {
	return 'nadlan-nf' === $handle && false === strpos( $tag, ' defer' ) ? str_replace( ' src=', ' defer src=', $tag ) : $tag;
}, 10, 2 );

/* ---------------------------------------------------------------- markup */
if ( ! function_exists( 'nadlan_nf_app_html' ) ) {
	/** The app root: data attributes only, the script builds the rest (one root per page). */
	function nadlan_nf_app_html( $deal, $city, $broker ) {
		$tok = function_exists( 'nadlan_cp_mapbox_token' ) ? (string) nadlan_cp_mapbox_token() : trim( (string) get_option( 'nadlan_mapbox_token', '' ) );
		$api = rest_url( 'nadlan/v1/near-finder' );
		if ( $broker > 0 ) { $api = add_query_arg( 'broker', (int) $broker, $api ); }
		return '<div class="nlnf__app" id="nlnf-app"'
			. ' data-api="' . esc_url( $api ) . '"'
			. ' data-mode="' . ( $broker > 0 ? 'broker' : 'portal' ) . '"'
			. ' data-deal="' . esc_attr( $deal ) . '"'
			. ' data-city="' . esc_attr( $city ) . '"'
			. ' data-mb="' . esc_attr( $tok ) . '"'
			. ' data-gl="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js"'
			. ' data-glcss="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css"'
			. ' data-rtl="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js"'
			. ' aria-busy="true"><p class="nlnf__wait">הדירות נטענות…</p></div>';
	}
}

if ( ! function_exists( 'nadlan_nf_own_html' ) ) {
	/** The owners' one quiet line (portal pages only, never on a broker's page): no popup, no banner, no sticky bar. */
	function nadlan_nf_own_html() {
		$p490 = ( 'product' === get_post_type( 490 ) && 'publish' === get_post_status( 490 ) ) ? get_permalink( 490 ) : '';
		return '<div class="nlnf__own"><p class="nlnf__own-a">יש לכם נכס למכירה או להשכרה? <a href="' . esc_url( home_url( '/post-listing/' ) ) . '">הוסיפו אותו למפה</a></p>'
			. '<p class="nlnf__own-b">פרסום רגיל בחינם.' . ( $p490 ? ' רוצים יותר חשיפה? <a href="' . esc_url( $p490 ) . '">מודעה מקודמת ל־60 יום</a>' : '' ) . '</p></div>';
	}
}

if ( ! function_exists( 'nadlan_nf_render' ) ) {
	/**
	 * The inline section. $args: deal ('' | 'sale' | 'rent', the page's tab), city (the page's filter, a starting place).
	 * The H2 leads with this page's own words (the page owns "דירות למכירה"); "באזור" is never the near-me word here.
	 */
	function nadlan_nf_render( $args = array() ) {
		$deal = isset( $args['deal'] ) && in_array( $args['deal'], array( 'sale', 'rent' ), true ) ? $args['deal'] : '';
		$city = isset( $args['city'] ) ? sanitize_text_field( (string) $args['city'] ) : '';
		nadlan_nf_register();
		wp_enqueue_style( 'nadlan-nf' );
		wp_enqueue_script( 'nadlan-nf' );
		do_action( 'nadlan_nf_rendered' );
		$h  = '<section class="nlnf" id="nlnf" dir="rtl" lang="he" aria-labelledby="nlnf-h">';
		$h .= '<header class="nlnf__head"><h2 class="nlnf__h" id="nlnf-h">דירות למכירה ולהשכרה על המפה, קרוב אליכם</h2>';
		$h .= '<p class="nlnf__lead">דירות למכירה, דירות להשכרה ופרויקטים חדשים סביבכם, לפי המיקום שלכם או לפי העיר והשכונה שתבחרו. ליד כל דירה תראו כמה היא רחוקה מכם ומהים, ואם תסמנו את העבודה, את ההורים או את הגן, גם מהם. המיקום שלכם נשאר במכשיר.</p></header>';
		$h .= nadlan_nf_app_html( $deal, $city, 0 ) . nadlan_nf_own_html();
		$h .= '</section>';
		return $h;
	}
}

if ( ! function_exists( 'nadlan_nf_launcher' ) ) {
	/** The floating launcher and its full-screen dialog. Hidden until the script runs (no script, no button). */
	function nadlan_nf_launcher( $c ) {
		$inline = ! empty( $c['inline'] );
		$h  = '<div class="nlnf nlnf-lidi" id="nlnf-lidi" dir="rtl" lang="he" data-mode="' . esc_attr( $c['mode'] ) . '">';
		$h .= '<button type="button" class="nlnf-launch" id="nlnf-launch" aria-haspopup="dialog" aria-controls="nlnf-dlg" hidden>'
			. '<span class="nlnf-radar" aria-hidden="true"><i></i><i></i><i></i><b></b></span><span class="nlnf-launch__t">' . esc_html( $c['label'] ) . '</span></button>';
		$h .= '<div class="nlnf-dlg" id="nlnf-dlg" role="dialog" aria-modal="true" aria-labelledby="nlnf-dlg-t" tabindex="-1" hidden>'
			. '<div class="nlnf-dlg__bar"><p class="nlnf-dlg__t" id="nlnf-dlg-t">' . esc_html( $c['title'] ) . '</p>'
			. '<button type="button" class="nlnf-dlg__x" id="nlnf-dlg-x" aria-label="סגירה"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18"></path></svg></button></div>'
			. '<div class="nlnf-dlg__body" id="nlnf-dlg-body">';
		if ( ! $inline ) {
			$h .= nadlan_nf_app_html( (string) $c['deal'], '', (int) $c['broker'] ) . ( 'broker' === $c['mode'] ? '' : nadlan_nf_own_html() );
		}
		$h .= '</div></div></div>';
		return $h;
	}
}
add_action( 'wp_footer', function () {
	$c = nadlan_nf_context();
	if ( ! $c || ! empty( $c['shortcode'] ) ) { return; } // a page holding the shortcode gets the inline block only
	if ( ! empty( $c['inline'] ) && ! did_action( 'nadlan_nf_rendered' ) ) { $c['inline'] = false; } // no inline section printed: the dialog brings its own
	echo nadlan_nf_launcher( $c ); // phpcs:ignore -- escaped above
}, 30 );

add_shortcode( 'nadlan_near_finder', function ( $atts ) {
	$a = shortcode_atts( array( 'deal' => '', 'city' => '' ), (array) $atts, 'nadlan_near_finder' );
	return nadlan_nf_render( $a );
} );
