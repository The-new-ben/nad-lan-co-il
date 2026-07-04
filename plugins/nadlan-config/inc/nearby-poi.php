<?php
/**
 * nadlan-config - Nearby POI (schools/transit/amenities) via OpenStreetMap Overpass (v1.11.0)
 *
 * Realtor.com/Rightmove-parity "what's nearby" tab. Free data (no API key) via
 * Overpass API; 10k req/day/IP rate limit so we aggressively cache (24h transient
 * per coords+radius bucket). Designed to fail silent - if Overpass is down or
 * times out, the panel just hides.
 *
 * Categories shown: schools (amenity=school), kindergarten, supermarket,
 * pharmacy, transit (bus_stop+railway_station+subway). 1km radius.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_poi_fetch' ) ) {
	function nadlan_poi_fetch( $lat, $lng, $radius_m = 1000 ) {
		$bucket = round( $lat, 4 ) . ',' . round( $lng, 4 ) . ',' . $radius_m;
		$key    = 'nadlan_poi_' . md5( $bucket );
		$cached = get_transient( $key );
		if ( is_array( $cached ) ) { return $cached; }
		$q = '[out:json][timeout:25];(' .
			'node(around:' . (int) $radius_m . ',' . (float) $lat . ',' . (float) $lng . ')[amenity~"^(school|kindergarten|pharmacy|supermarket|hospital|clinic)$"];' .
			'node(around:' . (int) $radius_m . ',' . (float) $lat . ',' . (float) $lng . ')[highway=bus_stop];' .
			'node(around:' . (int) $radius_m . ',' . (float) $lat . ',' . (float) $lng . ')[railway~"^(station|subway_entrance|tram_stop)$"];' .
			');out tags 200;';
		$res = wp_remote_post( 'https://overpass-api.de/api/interpreter', array(
			'timeout' => 12, 'body' => array( 'data' => $q ),
			'headers' => array( 'User-Agent' => 'nadlan-config/1.11 (nad-lan.co.il)' ),
		) );
		if ( is_wp_error( $res ) ) { return array(); }
		$j = json_decode( wp_remote_retrieve_body( $res ), true );
		$els = $j['elements'] ?? array();
		$groups = array( 'schools' => array(), 'kindergartens' => array(), 'transit' => array(), 'shops' => array(), 'health' => array() );
		foreach ( $els as $e ) {
			$t = $e['tags'] ?? array();
			$name = $t['name:he'] ?? ( $t['name'] ?? '' );
			$item = array( 'name' => $name, 'lat' => $e['lat'] ?? null, 'lng' => $e['lon'] ?? null );
			if ( ! $name ) { continue; }
			if ( ( $t['amenity'] ?? '' ) === 'school' )           { $groups['schools'][] = $item; }
			elseif ( ( $t['amenity'] ?? '' ) === 'kindergarten' ) { $groups['kindergartens'][] = $item; }
			elseif ( in_array( $t['amenity'] ?? '', array( 'supermarket', 'pharmacy' ), true ) ) { $groups['shops'][] = $item; }
			elseif ( in_array( $t['amenity'] ?? '', array( 'hospital', 'clinic' ), true ) )      { $groups['health'][] = $item; }
			elseif ( isset( $t['highway'] ) || isset( $t['railway'] ) )                          { $groups['transit'][] = $item; }
		}
		set_transient( $key, $groups, DAY_IN_SECONDS );
		return $groups;
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
		<?php $labels = array( 'schools' => 'בתי ספר', 'kindergartens' => 'גני ילדים', 'transit' => 'תחבורה', 'shops' => 'מרכולים / בתי מרקחת', 'health' => 'בריאות' );
		foreach ( $labels as $k => $lbl ) :
			$list = array_slice( $g[ $k ], 0, 6 );
			if ( ! $list ) { continue; } ?>
		<div class="nlpoi-col">
			<div class="nlpoi-h"><?php echo esc_html( $lbl ); ?> <span class="nlpoi-n">(<?php echo count( $g[ $k ] ); ?>)</span></div>
			<ul><?php foreach ( $list as $it ) : ?><li><?php echo esc_html( $it['name'] ); ?></li><?php endforeach; ?></ul>
		</div>
		<?php endforeach; ?>
	</div>
	<p class="nlpoi-src">מקור: OpenStreetMap · בטווח של ~1 ק"מ</p>
</div>
<style>
.nlpoi{margin:18px 0;border-top:1px solid rgba(27,26,23,.1);padding-top:16px}
.nlpoi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
.nlpoi-col{background:#FAF7F1;padding:12px;border-radius:6px}
.nlpoi-h{font-weight:600;margin-bottom:6px}
.nlpoi-n{color:#777;font-weight:400;font-size:13px}
.nlpoi-col ul{margin:0;padding-inline-start:18px;font-size:14px}
.nlpoi-src{font-size:11px;color:#999;margin-top:8px}
</style>
	<?php
	return $content . ob_get_clean();
}, 23 );
