<?php
/**
 * nadlan-config - URBAN RENEWAL MAP + advisor wiring (L5, 2026-07-12).
 *
 * 1. Adds the renewal advisor kinds to the RFP matcher (filter added in
 *    rfp.php): shamai / mefakeach / organizer, so the wizard and the
 *    project space can request quotes from the real directory.
 * 2. /urban-renewal/map/: city-cluster map over the ~938 imported gov.il
 *    compounds. HONEST V1: the import carries no lat/lng, so the map shows
 *    CITY AGGREGATES with counts by track (never fake per-building pins);
 *    per-compound pins arrive after a geocoding enrichment pass.
 *
 * Feature gate: option nadlan_feature_renewal_map ('1' = on).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_filter( 'nadlan_rfp_advisor_map', function ( $map ) {
	$map['shamai']    = array( 'shamai', 'appraiser' );
	$map['mefakeach'] = array( 'mefakeach', 'inspector', 'bedek_bait' );
	$map['organizer'] = array( 'organizer', 'urban_renewal_manager' );
	return $map;
} );

if ( ! function_exists( 'nadlan_ur_map_on' ) ) {
	function nadlan_ur_map_on() { return get_option( 'nadlan_feature_renewal_map', '1' ) === '1'; }
}

/* filterable He city -> [lng, lat] centroids for the aggregate map */
if ( ! function_exists( 'nadlan_ur_city_centroids' ) ) {
	function nadlan_ur_city_centroids() {
		return apply_filters( 'nadlan_ur_city_centroids', array(
			'תל אביב'      => array( 34.7818, 32.0853 ), 'תל אביב-יפו' => array( 34.7818, 32.0853 ),
			'ירושלים'      => array( 35.2137, 31.7683 ), 'חיפה' => array( 34.9896, 32.7940 ),
			'ראשון לציון'  => array( 34.7894, 31.9730 ), 'פתח תקווה' => array( 34.8878, 32.0871 ),
			'אשדוד'        => array( 34.6553, 31.8014 ), 'נתניה' => array( 34.8532, 32.3215 ),
			'באר שבע'      => array( 34.7913, 31.2530 ), 'בני ברק' => array( 34.8338, 32.0807 ),
			'חולון'        => array( 34.7722, 32.0158 ), 'רמת גן' => array( 34.8114, 32.0684 ),
			'בת ים'        => array( 34.7519, 32.0171 ), 'רחובות' => array( 34.8113, 31.8928 ),
			'הרצליה'       => array( 34.8434, 32.1663 ), 'כפר סבא' => array( 34.9068, 32.1750 ),
			'חדרה'         => array( 34.9196, 32.4340 ), 'לוד' => array( 34.8903, 31.9514 ),
			'רמלה'         => array( 34.8722, 31.9293 ), 'גבעתיים' => array( 34.8100, 32.0723 ),
			'קרית אונו'    => array( 34.8555, 32.0636 ), 'רעננה' => array( 34.8708, 32.1836 ),
			'קרית ים'      => array( 35.0691, 32.8497 ), 'קרית ביאליק' => array( 35.0856, 32.8275 ),
			'קרית מוצקין'  => array( 35.0777, 32.8369 ), 'עכו' => array( 35.0818, 32.9281 ),
			'נהריה'        => array( 35.0925, 33.0058 ), 'טבריה' => array( 35.5312, 32.7922 ),
			'אשקלון'       => array( 34.5715, 31.6688 ), 'דימונה' => array( 35.0320, 31.0658 ),
			'אילת'         => array( 34.9482, 29.5581 ), 'בית שמש' => array( 34.9886, 31.7304 ),
			'הוד השרון'    => array( 34.8878, 32.1556 ), 'רמת השרון' => array( 34.8395, 32.1461 ),
			'יהוד'         => array( 34.8907, 32.0331 ), 'אור יהודה' => array( 34.8500, 32.0292 ),
			'גבעת שמואל'   => array( 34.8480, 32.0781 ), 'קרית גת' => array( 34.7642, 31.6100 ),
			'נצרת'         => array( 35.2985, 32.7021 ), 'עפולה' => array( 35.2908, 32.6078 ),
		) );
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/renewal-map-data', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			if ( ! nadlan_ur_map_on() ) { return array( 'cities' => array() ); }
			$hit = get_transient( 'nadlan_ur_mapdata_v2' );
			if ( is_array( $hit ) ) { return $hit; }
			global $wpdb;
			$rows = $wpdb->get_results( "
				SELECT c.meta_value AS city, t.meta_value AS track, COUNT(*) AS n
				FROM {$wpdb->posts} p
				JOIN {$wpdb->postmeta} s ON s.post_id = p.ID AND s.meta_key = 'source' AND s.meta_value = 'urban_renewal'
				JOIN {$wpdb->postmeta} c ON c.post_id = p.ID AND c.meta_key = 'city'
				LEFT JOIN {$wpdb->postmeta} t ON t.post_id = p.ID AND t.meta_key = 'project_type'
				WHERE p.post_type = 'nadlan_project' AND p.post_status = 'publish'
				GROUP BY c.meta_value, t.meta_value
			", ARRAY_A );
			$cities = array();
			$cent = nadlan_ur_city_centroids();
			// normalize: gov.il city names vary in hyphenation ("תל אביב יפו" vs "תל אביב-יפו")
			$cent_norm = array();
			foreach ( $cent as $k => $v ) { $cent_norm[ str_replace( array( '-', '  ' ), ' ', $k ) ] = $v; }
			foreach ( (array) $rows as $r ) {
				$city = trim( (string) $r['city'] );
				if ( '' === $city ) { continue; }
				if ( ! isset( $cities[ $city ] ) ) {
					$cities[ $city ] = array( 'city' => $city, 'count' => 0, 'pinui_binui' => 0, 'tama38' => 0,
						'lnglat' => $cent[ $city ] ?? ( $cent_norm[ str_replace( array( '-', '  ' ), ' ', $city ) ] ?? null ) );
				}
				$cities[ $city ]['count'] += (int) $r['n'];
				if ( 'pinui_binui' === $r['track'] ) { $cities[ $city ]['pinui_binui'] += (int) $r['n']; }
				if ( 'tama38' === $r['track'] ) { $cities[ $city ]['tama38'] += (int) $r['n']; }
			}
			$out = array( 'total' => array_sum( wp_list_pluck( $cities, 'count' ) ), 'cities' => array_values( $cities ) );
			set_transient( 'nadlan_ur_mapdata_v2', $out, 6 * HOUR_IN_SECONDS );
			return $out;
		},
	) );
} );

add_shortcode( 'nadlan_ur_map', function () {
	if ( ! nadlan_ur_map_on() ) { return ''; }
	$token = '';
	if ( function_exists( 'nadlan_cmpmap_token' ) ) { $token = nadlan_cmpmap_token(); }
	if ( ! $token && function_exists( 'nadlan_drone_token' ) ) { $token = nadlan_drone_token(); }
	if ( ! $token ) { $token = (string) get_option( 'nadlan_mapbox_token', '' ); }
	if ( '' === $token ) { return '<p>המפה תוצג לאחר הגדרת מפתח מפות.</p>'; }
	$rest = esc_url( rest_url( 'nadlan/v1/renewal-map-data' ) );
	ob_start(); ?>
<div class="nlurm" dir="rtl">
	<div id="nlurm-map"></div>
	<p class="nlurm-note">המפה מציגה ריכוזי מתחמים מוכרזים לפי עיר, מתוך המאגר הרשמי (data.gov.il). מיקום מדויק לכל מתחם יתווסף בהמשך; הקישו על עיר לרשימת המתחמים בה.</p>
	<div id="nlurm-list" aria-live="polite"></div>
</div>
<style>
#nlurm-map{height:520px;border-radius:16px;overflow:hidden;border:1px solid #E2DCD0;background:#14130F}
.nlurm-note{font:400 12.5px/1.6 Heebo,sans-serif;color:#6D665C;margin:10px 0}
.nlurm-pin{background:#9C7A3C;color:#FAF7F1;border:2px solid #FAF7F1;border-radius:999px;padding:6px 11px;font:700 12px Heebo,sans-serif;cursor:pointer;white-space:nowrap;box-shadow:0 6px 16px rgba(0,0,0,.35)}
#nlurm-list .nlur-hit{background:#fff;border:1px solid #E2DCD0;border-radius:10px;padding:12px 14px;margin-top:8px;font:400 13.5px/1.6 Heebo,sans-serif}
</style>
<script>
(function(){
	var host=document.getElementById("nlurm-map");if(!host||host.dataset.wired)return;host.dataset.wired="1";
	function boot(){
		mapboxgl.accessToken="<?php echo esc_js( $token ); ?>";
		var map=new mapboxgl.Map({container:"nlurm-map",style:"mapbox://styles/mapbox/light-v11",center:[34.9,31.9],zoom:7,attributionControl:true,cooperativeGestures:true,
			locale:{"CooperativeGesturesHandler.WindowsHelpText":"לחצו Ctrl וגללו כדי להתקרב במפה","CooperativeGesturesHandler.MacHelpText":"לחצו ⌘ וגללו כדי להתקרב במפה","TouchPanBlocker.Message":"הזיזו את המפה בשתי אצבעות"}});
		map.addControl(new mapboxgl.NavigationControl());
		fetch("<?php echo $rest; // phpcs:ignore ?>").then(function(r){return r.json()}).then(function(d){
			(d.cities||[]).forEach(function(c){
				if(!c.lnglat)return;
				var el=document.createElement("button");el.className="nlurm-pin";el.type="button";
				el.textContent=c.city+" · "+c.count;
				el.addEventListener("click",function(){
					var list=document.getElementById("nlurm-list");
					list.innerHTML='<div class="nlur-hit">טוענים את מתחמי '+c.city+'...</div>';
					fetch("<?php echo esc_url( rest_url( 'nadlan/v1/renewal-lookup' ) ); // phpcs:ignore ?>?city="+encodeURIComponent(c.city))
						.then(function(r){return r.json()}).then(function(x){
							list.innerHTML=(x.matches||[]).map(function(m){
								var t=m.project_type==="pinui_binui"?"פינוי בינוי":(m.project_type==="tama38"?"תמא 38":"התחדשות");
								return '<div class="nlur-hit"><b>'+m.title+'</b> · '+t+(m.plan_number?' · תכנית '+m.plan_number:'')+' · <a href="'+m.url+'">לעמוד המתחם</a></div>';
							}).join("")||'<div class="nlur-hit">אין מתחמים להצגה</div>';
						});
				});
				new mapboxgl.Marker({element:el,anchor:"bottom"}).setLngLat(c.lnglat).addTo(map);
			});
		});
	}
	if(window.mapboxgl){boot();return}
	var l=document.createElement("link");l.rel="stylesheet";l.href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css";document.head.appendChild(l);
	var s=document.createElement("script");s.src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js";s.onload=boot;document.head.appendChild(s);
})();
</script>
	<?php
	return ob_get_clean();
} );
