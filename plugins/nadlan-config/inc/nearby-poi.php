<?php
/**
 * nadlan-config - Nearby POI (schools/parks/transit/shops/health/food) via
 * OpenStreetMap Overpass. v2 (2026-07-13).
 *
 * v1 POST-MORTEM (the owner caught it: "filter chips don't do anything"):
 * - queried NODES only, but Israeli schools/supermarkets/parks are mapped
 *   as WAYS/RELATIONS in OSM -> whole categories came back empty;
 * - dropped nameless POIs (most bus stops) instead of labeling generically;
 * - cached EMPTY results for 24h, so one bad fetch blanked the map for a day;
 * - single endpoint, no mirror fallback.
 *
 * v2: nwr + "out tags center" (ways carry center coords), generic Hebrew
 * labels for nameless items, haversine distance on every item (sorted),
 * two Overpass mirrors, empty results cached only 15 minutes, real results
 * 3 days. More buyer categories: parks/playgrounds, cafes/restaurants.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_poi_dist_m' ) ) {
	function nadlan_poi_dist_m( $lat1, $lng1, $lat2, $lng2 ) {
		$r = 6371000.0;
		$a = sin( deg2rad( $lat2 - $lat1 ) / 2 ) ** 2
			+ cos( deg2rad( $lat1 ) ) * cos( deg2rad( $lat2 ) ) * sin( deg2rad( $lng2 - $lng1 ) / 2 ) ** 2;
		return (int) round( 2 * $r * asin( sqrt( $a ) ) );
	}
}

if ( ! function_exists( 'nadlan_poi_fetch' ) ) {
	function nadlan_poi_fetch( $lat, $lng, $radius_m = 1000 ) {
		$bucket = round( $lat, 4 ) . ',' . round( $lng, 4 ) . ',' . $radius_m;
		$key    = 'nadlan_poi2_' . md5( $bucket );
		$cached = get_transient( $key );
		if ( is_array( $cached ) ) { return $cached; }
		$r = (int) $radius_m; $la = (float) $lat; $ln = (float) $lng;
		$q = '[out:json][timeout:25];('
			. "nwr(around:$r,$la,$ln)[amenity~\"^(school|kindergarten|pharmacy|hospital|clinic|doctors|cafe|restaurant|community_centre|library)$\"];"
			. "nwr(around:$r,$la,$ln)[shop~\"^(supermarket|mall|convenience|bakery|greengrocer)$\"];"
			. "nwr(around:$r,$la,$ln)[leisure~\"^(park|playground|garden|fitness_centre|sports_centre|pitch)$\"];"
			. "node(around:$r,$la,$ln)[highway=bus_stop];"
			. "nwr(around:$r,$la,$ln)[railway~\"^(station|subway_entrance|tram_stop|halt)$\"];"
			. ');out tags center 400;';
		$els = null;
		foreach ( array( 'https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter' ) as $endpoint ) {
			$res = wp_remote_post( $endpoint, array(
				'timeout' => 14, 'body' => array( 'data' => $q ),
				'headers' => array( 'User-Agent' => 'nadlan-config/2.0 (nad-lan.co.il)' ),
			) );
			if ( is_wp_error( $res ) || 200 !== (int) wp_remote_retrieve_response_code( $res ) ) { continue; }
			$j = json_decode( wp_remote_retrieve_body( $res ), true );
			if ( is_array( $j ) && isset( $j['elements'] ) ) { $els = $j['elements']; break; }
		}
		if ( null === $els ) { return array(); } // both mirrors down: no caching, retry next view
		$generic = array(
			'bus_stop' => 'תחנת אוטובוס', 'park' => 'פארק', 'playground' => 'גן משחקים',
			'garden' => 'גינה ציבורית', 'pitch' => 'מגרש ספורט', 'kindergarten' => 'גן ילדים',
			'school' => 'בית ספר', 'supermarket' => 'סופרמרקט', 'pharmacy' => 'בית מרקחת',
			'clinic' => 'מרפאה', 'tram_stop' => 'תחנת רכבת קלה', 'station' => 'תחנת רכבת',
		);
		$groups = array( 'schools' => array(), 'kindergartens' => array(), 'parks' => array(),
			'transit' => array(), 'shops' => array(), 'health' => array(), 'food' => array() );
		foreach ( $els as $e ) {
			$t = $e['tags'] ?? array();
			$plat = $e['lat'] ?? ( $e['center']['lat'] ?? null );
			$plng = $e['lon'] ?? ( $e['center']['lon'] ?? null );
			if ( ! $plat || ! $plng ) { continue; }
			$kindkey = $t['amenity'] ?? ( $t['shop'] ?? ( $t['leisure'] ?? ( $t['railway'] ?? ( $t['highway'] ?? '' ) ) ) );
			$name = $t['name:he'] ?? ( $t['name'] ?? '' );
			if ( '' === $name ) { $name = $generic[ $kindkey ] ?? ''; }
			if ( '' === $name ) { continue; }
			$item = array(
				'name' => $name, 'lat' => $plat, 'lng' => $plng,
				'd'    => nadlan_poi_dist_m( $lat, $lng, $plat, $plng ),
			);
			$am = $t['amenity'] ?? ''; $sh = $t['shop'] ?? ''; $le = $t['leisure'] ?? '';
			if ( 'school' === $am || 'library' === $am )            { $groups['schools'][] = $item; }
			elseif ( 'kindergarten' === $am )                        { $groups['kindergartens'][] = $item; }
			elseif ( in_array( $le, array( 'park', 'playground', 'garden', 'fitness_centre', 'sports_centre', 'pitch' ), true ) ) { $groups['parks'][] = $item; }
			elseif ( 'pharmacy' === $am || '' !== $sh )              { $groups['shops'][] = $item; }
			elseif ( in_array( $am, array( 'hospital', 'clinic', 'doctors' ), true ) ) { $groups['health'][] = $item; }
			elseif ( in_array( $am, array( 'cafe', 'restaurant' ), true ) ) { $groups['food'][] = $item; }
			elseif ( 'community_centre' === $am )                    { $groups['parks'][] = $item; }
			elseif ( isset( $t['highway'] ) || isset( $t['railway'] ) ) { $groups['transit'][] = $item; }
		}
		foreach ( $groups as $k => $list ) {
			usort( $list, function ( $a, $b ) { return $a['d'] - $b['d']; } );
			$groups[ $k ] = $list;
		}
		$total = array_sum( array_map( 'count', $groups ) );
		// never let one empty/failed answer blank the maps for a day
		set_transient( $key, $groups, $total > 0 ? 3 * DAY_IN_SECONDS : 15 * MINUTE_IN_SECONDS );
		return $groups;
	}
}

if ( ! function_exists( 'nadlan_poi_dist_label' ) ) {
	function nadlan_poi_dist_label( $m ) {
		if ( $m >= 1000 ) { return 'כ-' . round( $m / 1000, 1 ) . ' ק"מ'; }
		return 'כ-' . ( (int) round( $m / 50 ) * 50 ?: 50 ) . ' מ\'';
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! ( is_singular( 'nadlan_property' ) && in_the_loop() && is_main_query() ) ) { return $content; }
	$id  = get_the_ID();
	$lat = (float) get_post_meta( $id, 'lat', true );
	$lng = (float) get_post_meta( $id, 'lng', true );
	if ( ! $lat || ! $lng ) { return $content; }
	$g = nadlan_poi_fetch( $lat, $lng );
	$total = array_sum( array_map( 'count', $g ) );
	if ( $total === 0 ) { return $content; } // silent if Overpass returned nothing
	ob_start(); ?>
<div class="nlpoi" dir="rtl">
	<h3>מה יש בסביבה</h3>
	<div class="nlpoi-grid">
		<?php $labels = array( 'schools' => 'בתי ספר וחינוך', 'kindergartens' => 'גני ילדים', 'parks' => 'פארקים ופנאי', 'transit' => 'תחבורה', 'shops' => 'קניות ובתי מרקחת', 'health' => 'בריאות', 'food' => 'בתי קפה ומסעדות' );
		foreach ( $labels as $k => $lbl ) :
			$list = array_slice( isset( $g[ $k ] ) ? $g[ $k ] : array(), 0, 6 );
			if ( ! $list ) { continue; } ?>
		<div class="nlpoi-col">
			<div class="nlpoi-h"><?php echo esc_html( $lbl ); ?> <span class="nlpoi-n">(<?php echo count( $g[ $k ] ); ?>)</span></div>
			<ul><?php foreach ( $list as $it ) : ?><li><?php echo esc_html( $it['name'] ); ?><?php if ( ! empty( $it['d'] ) ) : ?> <span class="nlpoi-d">· <?php echo esc_html( nadlan_poi_dist_label( $it['d'] ) ); ?></span><?php endif; ?></li><?php endforeach; ?></ul>
		</div>
		<?php endforeach; ?>
	</div>
	<p class="nlpoi-src">מקור: OpenStreetMap · מרחקים אוויריים בקירוב</p>
</div>
<style>
.nlpoi{margin:18px 0;border-top:1px solid rgba(27,26,23,.1);padding-top:16px}
.nlpoi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
.nlpoi-col{background:#FAF7F1;padding:12px;border-radius:6px}
.nlpoi-h{font-weight:600;margin-bottom:6px}
.nlpoi-n{color:#777;font-weight:400;font-size:13px}
.nlpoi-d{color:#9C7A3C;font-size:12px;white-space:nowrap}
.nlpoi-col ul{margin:0;padding-inline-start:18px;font-size:14px}
.nlpoi-src{font-size:11px;color:#999;margin-top:8px}
</style>
	<?php
	return $content . ob_get_clean();
}, 23 );
