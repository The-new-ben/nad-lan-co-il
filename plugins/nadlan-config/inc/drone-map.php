<?php
/**
 * nadlan-config - Drone map on the projects catalog (owner ask 2026-07-06).
 *
 * A cinematic satellite + 3D-buildings Mapbox view of every GEOCODED project,
 * injected as a collapsible band on the /projects/ archive. Pins are gold
 * NadLan markers; clicking flies in low over the site (drone feel) and opens
 * a popup linking to the project page.
 *
 * HONESTY: only projects with real lat/lng meta appear (language siblings
 * excluded). Today that is the flagship set; the map grows automatically as
 * the geocode pass covers the wide catalog. The band says so, plainly.
 * Lazy: Mapbox GL loads only when the band is opened. No token -> no band.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/project-map', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function () {
			$cache = get_transient( 'nadlan_project_map_v1' );
			if ( is_array( $cache ) ) { return new WP_REST_Response( $cache, 200 ); }
			$q = new WP_Query( array(
				'post_type' => 'nadlan_project', 'post_status' => 'publish',
				'posts_per_page' => 200, 'fields' => 'ids', 'no_found_rows' => true,
				'nadlan_no_lang_siblings' => true,
				'meta_query' => array( 'relation' => 'AND',
					array( 'key' => 'lat', 'compare' => 'EXISTS' ),
					array( 'key' => 'lng', 'compare' => 'EXISTS' ),
				),
			) );
			$items = array();
			foreach ( $q->posts as $id ) {
				$lat = (float) get_post_meta( $id, 'lat', true );
				$lng = (float) get_post_meta( $id, 'lng', true );
				if ( ! $lat || ! $lng ) { continue; }
				$items[] = array(
					'id' => $id, 'lat' => $lat, 'lng' => $lng,
					'title' => get_the_title( $id ),
					'url'   => get_permalink( $id ),
					'city'  => (string) get_post_meta( $id, 'city', true ),
					'img'   => esc_url_raw( (string) get_post_meta( $id, 'project_3d_image', true ) ),
				);
			}
			$out = array( 'ok' => true, 'count' => count( $items ), 'items' => $items );
			set_transient( 'nadlan_project_map_v1', $out, 6 * HOUR_IN_SECONDS );
			return new WP_REST_Response( $out, 200 );
		},
	) );
} );
add_action( 'save_post_nadlan_project', function () { delete_transient( 'nadlan_project_map_v1' ); } );

if ( ! function_exists( 'nadlan_drone_map_band' ) ) {
	function nadlan_drone_map_band() {
		$token = trim( (string) get_option( 'nadlan_mapbox_token', '' ) );
		if ( $token === '' ) { return ''; }
		$rest = esc_url( rest_url( 'nadlan/v1/project-map' ) );
		ob_start(); ?>
<section class="nldrone" id="nldrone" data-token="<?php echo esc_attr( $token ); ?>" data-rest="<?php echo esc_attr( $rest ); ?>">
	<button type="button" class="nldrone-toggle" id="nldrone-toggle" aria-expanded="false" aria-controls="nldrone-stage">
		<span class="nldrone-toggle__ic" aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M12 3v4m0 10v4M3 12h4m10 0h4"/><circle cx="12" cy="12" r="3.2"/><circle cx="12" cy="12" r="7.5" stroke-dasharray="2 3"/></svg></span>
		<span><b>מפת רחפן חיה</b> · לוויין ובניינים בתלת ממד מעל הפרויקטים המובילים</span>
		<span class="nldrone-toggle__arrow" aria-hidden="true">▾</span>
	</button>
	<div class="nldrone-stage" id="nldrone-stage" hidden>
		<div class="nldrone-map" id="nldrone-map"></div>
		<p class="nldrone-note">מוצגים פרויקטים עם מיקום מאומת או משוער. פרויקטים נוספים מצטרפים למפה עם אימות מיקומם.</p>
	</div>
</section>
<style>
.nldrone{max-width:1240px;margin:6px auto 22px;padding:0 4px}
.nldrone-toggle{display:flex;align-items:center;gap:12px;width:100%;text-align:start;font:inherit;font-size:14.5px;color:#1B1A17;background:linear-gradient(135deg,#F7F1E3,#F3EEE3);border:1px solid #D6C189;border-radius:14px;padding:14px 18px;cursor:pointer;transition:border-color .2s}
.nldrone-toggle:hover{border-color:#9C7A3C}
.nldrone-toggle__ic{color:#9C7A3C;display:flex}
.nldrone-toggle__arrow{margin-inline-start:auto;color:#9C7A3C;transition:transform .25s}
.nldrone.is-open .nldrone-toggle__arrow{transform:rotate(180deg)}
.nldrone-stage{margin-top:10px}
.nldrone-map{height:520px;border-radius:16px;border:1px solid #E2DCD0;background:#14130F;overflow:hidden}
.nldrone-note{font-size:12px;color:#6D665C;margin:8px 2px 0}
.nldrone-pin{width:30px;height:38px;cursor:pointer;filter:drop-shadow(0 3px 6px rgba(0,0,0,.45))}
.nldrone-pop b{font-size:13.5px}
.nldrone-pop a{display:inline-block;margin-top:6px;font-weight:700;color:#9C7A3C;text-decoration:none;font-size:12.5px}
.nldrone-pop img{width:100%;height:86px;object-fit:cover;border-radius:8px;margin:6px 0 2px;display:block}
@media(max-width:640px){.nldrone-map{height:400px}}
</style>
<script>
(function(){
	var band=document.getElementById("nldrone"),btn=document.getElementById("nldrone-toggle"),stage=document.getElementById("nldrone-stage");
	if(!band||!btn)return;
	var booted=false;
	function boot(){
		if(booted)return;booted=true;
		function go(){
			if(!window.mapboxgl)return;
			mapboxgl.accessToken=band.dataset.token;
			var map=new mapboxgl.Map({container:"nldrone-map",style:"mapbox://styles/mapbox/satellite-streets-v12",center:[34.78,32.09],zoom:11.4,pitch:58,bearing:-17,attributionControl:true});
			map.addControl(new mapboxgl.NavigationControl({visualizePitch:true}));
			map.on("load",function(){
				var layers=map.getStyle().layers,lab;
				for(var i=0;i<layers.length;i++){if(layers[i].type==="symbol"&&layers[i].layout&&layers[i].layout["text-field"]){lab=layers[i].id;break}}
				try{map.addLayer({id:"nl-3d",source:"composite","source-layer":"building",filter:["==","extrude","true"],type:"fill-extrusion",minzoom:13,paint:{"fill-extrusion-color":"#d8d2c4","fill-extrusion-height":["get","height"],"fill-extrusion-base":["get","min_height"],"fill-extrusion-opacity":.72}},lab)}catch(e){}
			});
			fetch(band.dataset.rest).then(function(r){return r.json()}).then(function(d){
				(d.items||[]).forEach(function(p){
					var el=document.createElement("div");
					el.className="nldrone-pin";
					el.innerHTML='<svg viewBox="0 0 30 38"><path d="M15 1C7.8 1 2 6.8 2 14c0 9.6 13 23 13 23s13-13.4 13-23C28 6.8 22.2 1 15 1z" fill="#9C7A3C" stroke="#FAF7F1" stroke-width="2"/><circle cx="15" cy="14" r="5.5" fill="#FAF7F1"/></svg>';
					var pop=new mapboxgl.Popup({offset:22,maxWidth:"250px"}).setHTML('<div class="nldrone-pop" dir="rtl"><b>'+p.title+"</b>"+(p.img?'<img src="'+p.img+'" alt="" loading="lazy">':"")+(p.city?'<div style="font-size:12px;color:#6D665C">'+p.city+"</div>":"")+'<a href="'+p.url+'">לעמוד הפרויקט ←</a></div>');
					var mk=new mapboxgl.Marker({element:el,anchor:"bottom"}).setLngLat([p.lng,p.lat]).setPopup(pop).addTo(map);
					el.addEventListener("click",function(){map.flyTo({center:[p.lng,p.lat],zoom:16.2,pitch:62,bearing:-30,speed:.9})});
				});
				if(d.items&&d.items.length){
					var b=new mapboxgl.LngLatBounds();
					d.items.forEach(function(p){b.extend([p.lng,p.lat])});
					map.fitBounds(b,{padding:90,pitch:58,bearing:-17,maxZoom:13.5});
				}
			}).catch(function(){});
		}
		if(window.mapboxgl){go();return}
		var l=document.createElement("link");l.rel="stylesheet";l.href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css";document.head.appendChild(l);
		var sc=document.createElement("script");sc.src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js";sc.onload=go;document.head.appendChild(sc);
	}
	btn.addEventListener("click",function(){
		var open=stage.hidden;
		stage.hidden=!open;
		band.classList.toggle("is-open",open);
		btn.setAttribute("aria-expanded",open?"true":"false");
		if(open)boot();
	});
})();
</script>
<?php
		return ob_get_clean();
	}
}
