<?php
/**
 * nadlan-config — Leaflet archive map with clustering (v1.12.0)
 *
 * Madlan/Yad2-style map on the properties archive + city hubs. Uses Leaflet
 * (no API key, OSM tiles) + leaflet.markercluster (CDN). RTL-aware. Renders
 * via a [nadlan_map] shortcode AND auto-appends to /properties/ archive.
 *
 * Data via REST GET /nadlan/v1/map?city=&listing_type= — returns only
 * lat/lng/title/price/url for the bounding-box. Limit 500 per request to
 * keep payload small. No PII.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/map', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$mq = array( 'relation' => 'AND',
				array( 'key' => 'lat', 'compare' => 'EXISTS' ),
				array( 'key' => 'lng', 'compare' => 'EXISTS' ),
			);
			$city = trim( (string) $req->get_param( 'city' ) );
			$lt   = trim( (string) $req->get_param( 'listing_type' ) );
			if ( $city !== '' ) { $mq[] = array( 'key' => 'city', 'value' => sanitize_text_field( $city ) ); }
			if ( $lt   !== '' ) { $mq[] = array( 'key' => 'listing_type', 'value' => sanitize_text_field( $lt ) ); }
			$ids = get_posts( array(
				'post_type' => 'nadlan_property', 'posts_per_page' => 500,
				'fields' => 'ids', 'meta_query' => $mq, 'no_found_rows' => true,
			) );
			$out = array();
			foreach ( $ids as $id ) {
				$lat = (float) get_post_meta( $id, 'lat', true );
				$lng = (float) get_post_meta( $id, 'lng', true );
				if ( ! $lat || ! $lng ) { continue; }
				$out[] = array(
					'id' => $id, 'lat' => $lat, 'lng' => $lng,
					'title' => get_the_title( $id ), 'url' => get_permalink( $id ),
					'price' => (int) get_post_meta( $id, 'price', true ),
					'rooms' => (float) get_post_meta( $id, 'rooms', true ),
				);
			}
			return new WP_REST_Response( array( 'ok' => true, 'count' => count( $out ), 'items' => $out ), 200 );
		},
	) );
} );

if ( ! function_exists( 'nadlan_map_render' ) ) {
	function nadlan_map_render( $atts = array() ) {
		$a = shortcode_atts( array( 'city' => '', 'listing_type' => '', 'height' => '480px',
			'center_lat' => '31.7683', 'center_lng' => '35.2137', 'zoom' => '8' ), $atts );
		$id = 'nlmap_' . wp_generate_password( 6, false, false );
		$qs = http_build_query( array_filter( array( 'city' => $a['city'], 'listing_type' => $a['listing_type'] ) ) );
		ob_start(); ?>
<div id="<?php echo esc_attr( $id ); ?>" class="nlmap" dir="rtl" style="height:<?php echo esc_attr( $a['height'] ); ?>"></div>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
<style>.nlmap{width:100%;border-radius:6px;overflow:hidden}.nlmap .leaflet-control-container{direction:ltr}</style>
<script>
(function(){
	function init(){
		var m=L.map('<?php echo esc_js( $id ); ?>',{center:[<?php echo esc_js( $a['center_lat'] ); ?>,<?php echo esc_js( $a['center_lng'] ); ?>],zoom:<?php echo (int) $a['zoom']; ?>});
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap'}).addTo(m);
		var cluster=L.markerClusterGroup();
		fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/map' ) ); ?>?<?php echo esc_js( $qs ); ?>').then(function(r){return r.json();}).then(function(j){
			if(!j.ok||!j.items.length){return;}
			var bounds=L.latLngBounds([]);
			j.items.forEach(function(it){
				var mk=L.marker([it.lat,it.lng]).bindPopup('<strong><a href="'+it.url+'">'+it.title+'</a></strong><br>'+(it.price?'₪'+it.price.toLocaleString():'')+(it.rooms?' · '+it.rooms+' חד׳':''));
				cluster.addLayer(mk);bounds.extend([it.lat,it.lng]);
			});
			m.addLayer(cluster);
			if(j.items.length>1){m.fitBounds(bounds.pad(0.1));}
		});
	}
	if(typeof L!=='undefined'){init();}
	else{var iv=setInterval(function(){if(typeof L!=='undefined'){clearInterval(iv);init();}},120);}
})();
</script>
		<?php
		return ob_get_clean();
	}
}
add_shortcode( 'nadlan_map', 'nadlan_map_render' );

/* Auto-prepend map on /properties/ archive */
add_action( 'loop_start', function ( $q ) {
	if ( ! $q->is_main_query() || ! is_post_type_archive( 'nadlan_property' ) ) { return; }
	echo nadlan_map_render( array( 'height' => '420px' ) );
} );
