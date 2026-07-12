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
				'posts_per_page' => -1, 'fields' => 'ids', 'no_found_rows' => true,
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
					'conf'  => (string) get_post_meta( $id, 'geo_confidence', true ),
					'featured' => (bool) get_post_meta( $id, 'project_featured', true ),
					'poster'   => esc_url_raw( (string) get_post_meta( $id, 'project_model_poster', true ) ),
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

if ( ! function_exists( 'nadlan_drone_map_i18n' ) ) {
	function nadlan_drone_map_i18n( $lang ) {
		$T = array(
			'he' => array( 'title' => 'מפת הפרויקטים החיה', 'sub' => 'איפה תרצו לגור? התקרבו לעיר ובחרו פרויקט.', 'near' => 'פרויקטים לידי', 'toggle' => 'מפת רחפן חיה · לוויין ובניינים בתלת ממד מעל כל הקטלוג', 'note' => 'חלק מהמיקומים משוערים עד לאימות מול היזם.', 'to_project' => 'לעמוד הפרויקט ←', 'projects_n' => 'פרויקטים', 'more_n' => 'ועוד {n} פרויקטים בעיר', 'city_level' => 'מיקום ברמת עיר' ),
			'en' => array( 'title' => 'The Live Project Map', 'sub' => 'Where do you want to live? Zoom to your city and pick a project.', 'near' => 'Projects near me', 'toggle' => 'Live drone map · satellite and 3D buildings over the full catalog', 'note' => 'Some locations are approximate until verified with the developer.', 'to_project' => 'To the project page →', 'projects_n' => 'projects', 'more_n' => 'and {n} more projects in this city', 'city_level' => 'city-level location' ),
			'fr' => array( 'title' => 'La carte des projets en direct', 'sub' => 'Ou voulez-vous vivre ? Zoomez sur votre ville et choisissez un projet.', 'near' => 'Projets pres de moi', 'toggle' => 'Carte drone en direct · satellite et batiments 3D', 'note' => 'Certaines localisations sont approximatives jusqu\'a verification avec le promoteur.', 'to_project' => 'Vers la page du projet →', 'projects_n' => 'projets', 'more_n' => 'et {n} autres projets dans cette ville', 'city_level' => 'localisation au niveau de la ville' ),
			'ru' => array( 'title' => 'Живая карта проектов', 'sub' => 'Где вы хотите жить? Приблизьте свой город и выберите проект.', 'near' => 'Проекты рядом со мной', 'toggle' => 'Живая карта · спутник и 3D здания', 'note' => 'Некоторые локации приблизительны до подтверждения застройщиком.', 'to_project' => 'На страницу проекта →', 'projects_n' => 'проектов', 'more_n' => 'и еще {n} проектов в этом городе', 'city_level' => 'локация на уровне города' ),
			'ar' => array( 'title' => 'خريطة المشاريع الحية', 'sub' => 'أين تريدون السكن؟ قربوا على مدينتكم واختاروا مشروعا.', 'near' => 'مشاريع بالقرب مني', 'toggle' => 'خريطة حية · قمر صناعي ومبان ثلاثية الأبعاد', 'note' => 'بعض المواقع تقريبية حتى التوثيق مع المطور.', 'to_project' => 'إلى صفحة المشروع ←', 'projects_n' => 'مشاريع', 'more_n' => 'و {n} مشاريع أخرى في هذه المدينة', 'city_level' => 'موقع على مستوى المدينة' ),
		);
		return isset( $T[ $lang ] ) ? $T[ $lang ] : $T['he'];
	}
}

if ( ! function_exists( 'nadlan_drone_map_band' ) ) {
	/**
	 * $mode 'toggle'   - collapsible band (projects catalog).
	 * $mode 'showcase' - always-visible designed band that boots itself when
	 *                    scrolled into view (homepage / premium). Same map.
	 */
	function nadlan_drone_map_band( $mode = 'toggle', $lang = 'he' ) {
		$token = trim( (string) get_option( 'nadlan_mapbox_token', '' ) );
		if ( $token === '' ) { return ''; }
		$rest = esc_url( rest_url( 'nadlan/v1/project-map' ) );
		$L = nadlan_drone_map_i18n( $lang );
		ob_start(); ?>
<section class="nldrone nldrone--<?php echo esc_attr( $mode ); ?>" id="nldrone" data-mode="<?php echo esc_attr( $mode ); ?>" data-token="<?php echo esc_attr( $token ); ?>" data-rest="<?php echo esc_attr( $rest ); ?>"
	data-l-top="<?php echo esc_attr( $L['to_project'] ); ?>" data-l-pn="<?php echo esc_attr( $L['projects_n'] ); ?>" data-l-more="<?php echo esc_attr( $L['more_n'] ); ?>" data-l-city="<?php echo esc_attr( $L['city_level'] ); ?>">
	<?php if ( 'showcase' === $mode ) : ?>
	<div class="nldrone-head">
		<span class="nldrone-head__eyebrow"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M12 3v4m0 10v4M3 12h4m10 0h4"/><circle cx="12" cy="12" r="3.2"/><circle cx="12" cy="12" r="7.5" stroke-dasharray="2 3"/></svg> LIVE</span>
		<h2 class="nldrone-head__title"><?php echo esc_html( $L['title'] ); ?></h2>
		<p class="nldrone-head__sub"><?php echo esc_html( $L['sub'] ); ?></p>
	</div>
	<?php elseif ( 'toggle' === $mode ) : ?>
	<button type="button" class="nldrone-toggle" id="nldrone-toggle" aria-expanded="false" aria-controls="nldrone-stage">
		<span class="nldrone-toggle__ic" aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M12 3v4m0 10v4M3 12h4m10 0h4"/><circle cx="12" cy="12" r="3.2"/><circle cx="12" cy="12" r="7.5" stroke-dasharray="2 3"/></svg></span>
		<span><?php echo esc_html( $L['toggle'] ); ?></span>
		<span class="nldrone-toggle__arrow" aria-hidden="true">▾</span>
	</button>
	<?php endif; ?>
	<div class="nldrone-stage" id="nldrone-stage" <?php echo 'toggle' === $mode ? 'hidden' : ''; ?>>
		<div class="nldrone-map" id="nldrone-map">
			<button type="button" class="nldrone-near" id="nldrone-near" hidden><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3m0 14v3M2 12h3m14 0h3"/></svg> <?php echo esc_html( $L['near'] ); ?></button>
		</div>
		<p class="nldrone-note"><?php echo esc_html( $L['note'] ); ?></p>
	</div>
</section>
<style>
.nldrone{max-width:1240px;margin:6px auto 22px;padding:0 4px}
.nldrone--showcase{margin:34px auto 40px;padding:0 clamp(14px,3vw,28px)}
.nldrone-head{margin-bottom:16px}
.nldrone-head__eyebrow{display:inline-flex;align-items:center;gap:7px;color:#9C7A3C;font:700 11.5px/1 Heebo,sans-serif;letter-spacing:.14em;background:#F7F1E3;border:1px solid #D6C189;border-radius:999px;padding:6px 13px}
.nldrone-head__title{font-family:"Frank Ruhl Libre",serif;font-size:clamp(1.5rem,1.1rem+1.6vw,2.2rem);color:#1B1A17;margin:10px 0 4px}
.nldrone-head__sub{color:#6D665C;font-size:14.5px;margin:0;max-width:640px}
.nldrone--showcase .nldrone-map{height:560px;border-radius:20px;box-shadow:0 24px 60px -28px rgba(27,26,23,.45);border:1px solid #D6C189}
@media(max-width:640px){.nldrone--showcase .nldrone-map{height:420px}}
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
.nldrone--hero{max-width:none;margin:0;padding:0;position:absolute;inset:0}
.nldrone--hero .nldrone-stage{margin:0;height:100%}
.nldrone--hero .nldrone-map{height:100%;border-radius:0;border:0}
.nldrone--hero .nldrone-note{position:absolute;bottom:8px;inset-inline-end:14px;z-index:5;color:#CDC5B4;margin:0;text-shadow:0 1px 3px rgba(0,0,0,.6)}
.nldrone--hero .nldrone-near{top:auto;bottom:46px;inset-inline-start:auto;inset-inline-end:14px}
.nldrone-map{position:relative}
.nldrone-near{position:absolute;z-index:5;top:12px;inset-inline-start:12px;display:inline-flex;align-items:center;gap:7px;font:600 12.5px/1 Heebo,sans-serif;color:#1B1A17;background:#FAF7F1;border:1px solid #D6C189;border-radius:999px;padding:9px 14px;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.25);transition:border-color .2s}
.nldrone-near:hover{border-color:#9C7A3C}
.nldrone-flag{display:flex;flex-direction:column;align-items:center;text-decoration:none;cursor:pointer}
.nldrone-flag__pole{width:2px;height:26px;background:#FAF7F1;box-shadow:0 0 4px rgba(0,0,0,.5)}
.nldrone-flag__card{display:flex;align-items:center;gap:7px;background:rgba(20,19,15,.88);border:1px solid #D6C189;border-radius:10px;padding:5px 9px 5px 6px;transform:translateY(-2px)}
.nldrone-flag__card img{width:30px;height:30px;object-fit:cover;border-radius:6px}
.nldrone-flag__card b{color:#FAF7F1;font:700 12px/1.2 Heebo,sans-serif;max-width:130px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nldrone-flag__card i{font:800 9.5px/1 Heebo,sans-serif;font-style:normal;color:#14130F;background:#D6C189;border-radius:5px;padding:3px 5px}
.nldrone-flag:hover .nldrone-flag__card{border-color:#9C7A3C}
</style>
<script>
(function(){
	var band=document.getElementById("nldrone"),btn=document.getElementById("nldrone-toggle"),stage=document.getElementById("nldrone-stage");
	if(!band)return;
	var L={top:band.dataset.lTop,pn:band.dataset.lPn,more:band.dataset.lMore,city:band.dataset.lCity};
	var booted=false;
	function boot(){
		if(booted)return;booted=true;
		function go(){
			if(!window.mapboxgl)return;
			mapboxgl.accessToken=band.dataset.token;
			/* Hebrew renders REVERSED without the RTL text plugin (caught on the live hero) */
			try{if(mapboxgl.getRTLTextPluginStatus&&mapboxgl.getRTLTextPluginStatus()==="unavailable"){mapboxgl.setRTLTextPlugin("https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js",null,true)}}catch(e){}
			/* cooperativeGestures (owner 2026-07-11): page scroll must never zoom the map */
			/* owner 2026-07-12: the black map was hard to read (mobile most of all).
			   Only the hero fallback stays night; every in-page band is LIGHT in the
			   brand palette - cream ground, ink labels, terracotta pins (the Zillow
			   principle: a dull-toned base so the pins carry the color). */
			var isHero=band.dataset.mode==="hero";
			var PAL=isHero
				?{pin:"#E9D9A8",pinStroke:"#14130F",label:"#E9E2D2",halo:"#14130F",chip:"#F3EEE3",chipHalo:"#14130F"}
				:{pin:"#C2563A",pinStroke:"#FAF7F1",label:"#51483A",halo:"#FAF7F1",chip:"#1B1A17",chipHalo:"#FAF7F1"};
			var map=new mapboxgl.Map({container:"nldrone-map",style:isHero?"mapbox://styles/mapbox/dark-v11":"mapbox://styles/mapbox/light-v11",center:[34.86,31.95],zoom:8.6,pitch:isHero?55:46,bearing:-10,attributionControl:true,cooperativeGestures:true,locale:{"CooperativeGesturesHandler.WindowsHelpText":"\u05dc\u05d7\u05e6\u05d5 Ctrl \u05d5\u05d2\u05dc\u05dc\u05d5 \u05db\u05d3\u05d9 \u05dc\u05d4\u05ea\u05e7\u05e8\u05d1 \u05d1\u05de\u05e4\u05d4","CooperativeGesturesHandler.MacHelpText":"\u05dc\u05d7\u05e6\u05d5 \u2318 \u05d5\u05d2\u05dc\u05dc\u05d5 \u05db\u05d3\u05d9 \u05dc\u05d4\u05ea\u05e7\u05e8\u05d1 \u05d1\u05de\u05e4\u05d4","TouchPanBlocker.Message":"\u05d4\u05d6\u05d9\u05d6\u05d5 \u05d0\u05ea \u05d4\u05de\u05e4\u05d4 \u05d1\u05e9\u05ea\u05d9 \u05d0\u05e6\u05d1\u05e2\u05d5\u05ea"}});
			map.addControl(new mapboxgl.NavigationControl({visualizePitch:true}));
			map.on("load",function(){
				if(isHero){
					/* night tuning (hero fallback only) */
					try{map.setPaintProperty("water","fill-color","#0E1A20")}catch(e){}
					try{map.setPaintProperty("land","background-color","#17150F")}catch(e){}
					try{map.setFog({color:"#14130F","horizon-blend":0.06,"star-intensity":0.25})}catch(e){}
				} else {
					/* cream tuning: warm paper ground, soft water */
					try{map.setPaintProperty("water","fill-color","#B3C7CC")}catch(e){}
					try{map.setPaintProperty("land","background-color","#F0EBE1")}catch(e){}
				}
				try{map.getStyle().layers.forEach(function(l){if(l.type==="symbol"&&l.layout&&l.layout["text-field"]){map.setLayoutProperty(l.id,"text-field",["coalesce",["get","name_he"],["get","name:he"],["get","name"]])}})}catch(e){}
				var layers=map.getStyle().layers,lab;
				for(var i=0;i<layers.length;i++){if(layers[i].type==="symbol"&&layers[i].layout&&layers[i].layout["text-field"]){lab=layers[i].id;break}}
				try{map.addLayer({id:"nl-3d",source:"composite","source-layer":"building",filter:["==","extrude","true"],type:"fill-extrusion",minzoom:13,paint:{"fill-extrusion-color":isHero?"#3A342A":"#DAD2C1","fill-extrusion-height":["get","height"],"fill-extrusion-base":["get","min_height"],"fill-extrusion-opacity":.72}},lab)}catch(e){}
				try{map.addSource("nl-dem",{type:"raster-dem",url:"mapbox://mapbox.mapbox-terrain-dem-v1",tileSize:512,maxzoom:14});map.setTerrain({source:"nl-dem",exaggeration:1.35})}catch(e){}
				if(isHero){try{map.addLayer({id:"nl-sky",type:"sky",paint:{"sky-type":"atmosphere","sky-atmosphere-sun-intensity":6}})}catch(e){}}
			});
			fetch(band.dataset.rest).then(function(r){return r.json()}).then(function(d){
				var all=d.items||[]; if(!all.length)return;
				/* paid/flagship projects fly a FLAG visible from distance, with the
				   3D model badge - one click to the full 3D experience. */
				var flags=all.filter(function(p){return p.featured&&p.conf!=="city"});
				var items=all.filter(function(p){return !(p.featured&&p.conf!=="city")});
				flags.forEach(function(p){
					var el=document.createElement("a");
					el.className="nldrone-flag"; el.href=p.url;
					el.innerHTML='<span class="nldrone-flag__pole"></span><span class="nldrone-flag__card">'+(p.poster?'<img src="'+p.poster+'" alt="" loading="lazy">':"")+'<b>'+p.title.split("|")[0].split(" - ")[0]+"</b><i>3D</i></span>";
					new mapboxgl.Marker({element:el,anchor:"bottom"}).setLngLat([p.lng,p.lat]).addTo(map);
				});
				/* DE-CLUSTERED (owner 2026-07-12): the anonymous count-bubbles took
				   3-4 taps to reach a project and were misery on phones. Progressive
				   disclosure instead: country view shows NAMED CITY CHIPS ("City - 43");
				   one tap flies into the city where every project is a labeled pin;
				   one tap on a pin opens its card. Two taps, never a blind bundle. */
				var gj={type:"FeatureCollection",features:items.map(function(p){
					return {type:"Feature",geometry:{type:"Point",coordinates:[p.lng,p.lat]},
						properties:{id:p.id,title:p.title,short:String(p.title||"").split(/\s[-|\u00b7]\s|\s\u2013\s/)[0].trim(),url:p.url,city:p.city||"",img:p.img||"",conf:p.conf||""}};
				})};
				var cities={};
				items.forEach(function(p){
					var c=p.city||"";if(!c)return;
					if(!cities[c]){cities[c]={n:0,lng:0,lat:0}}
					cities[c].n++;cities[c].lng+=p.lng;cities[c].lat+=p.lat;
				});
				var cityGj={type:"FeatureCollection",features:Object.keys(cities).map(function(c){
					var v=cities[c];
					return {type:"Feature",geometry:{type:"Point",coordinates:[v.lng/v.n,v.lat/v.n]},
						properties:{city:c,n:v.n,label:c+" \u00b7 "+v.n}};
				})};
				var CITY_MAX=10.6,PT_MIN=10.2;
				var addData=function(){
					if(map.getSource("nlprojects"))return;
					map.addSource("nlprojects",{type:"geojson",data:gj});
					map.addSource("nlcities",{type:"geojson",data:cityGj});
					/* named city chips at country zoom - big, legible, one tap */
					map.addLayer({id:"nl-city-chips",type:"symbol",source:"nlcities",maxzoom:CITY_MAX,
						layout:{"text-field":["get","label"],"text-size":["interpolate",["linear"],["zoom"],7,12,10,14.5],"text-font":["DIN Pro Bold","Arial Unicode MS Bold"],"text-allow-overlap":false,"text-padding":6},
						paint:{"text-color":PAL.chip,"text-halo-color":PAL.chipHalo,"text-halo-width":1.8}});
					map.addLayer({id:"nl-points",type:"circle",source:"nlprojects",minzoom:PT_MIN,
						paint:{"circle-color":PAL.pin,"circle-radius":["interpolate",["linear"],["zoom"],10.2,4.5,13,6,15,7.5],"circle-stroke-width":1.6,"circle-stroke-color":PAL.pinStroke}});
					/* project names beside the pins; collisions hide text, never the pin */
					map.addLayer({id:"nl-point-labels",type:"symbol",source:"nlprojects",minzoom:PT_MIN,
						layout:{"text-field":["get","short"],"text-size":11,"text-font":["DIN Pro Medium","Arial Unicode MS Bold"],"text-anchor":"top","text-offset":[0,0.7],"text-optional":true,"text-allow-overlap":false},
						paint:{"text-color":PAL.label,"text-halo-color":PAL.halo,"text-halo-width":1.3}});
					function popHtml(p){return '<div class="nldrone-pop" dir="auto"><b>'+p.title+"</b>"+(p.img?'<img src="'+p.img+'" alt="" loading="lazy">':"")+(p.city?'<div style="font-size:12px;color:#6D665C">'+p.city+(p.conf==="city"?" \u00b7 "+L.city:"")+"</div>":"")+'<a href="'+p.url+'">'+L.top+"</a></div>"}
					var openPin=function(e){
						var p=e.features[0].properties;
						new mapboxgl.Popup({offset:14,maxWidth:"250px"}).setLngLat(e.features[0].geometry.coordinates).setHTML(popHtml(p)).addTo(map);
					};
					// the NAME LABEL is a far bigger tap target than the dot - both open the card
					map.on("click","nl-points",openPin);
					map.on("click","nl-point-labels",openPin);
					map.on("click","nl-city-chips",function(e){
						map.easeTo({center:e.features[0].geometry.coordinates,zoom:11.8,pitch:isHero?55:46,duration:1100});
					});
					["nl-points","nl-point-labels","nl-city-chips"].forEach(function(l){
						map.on("mouseenter",l,function(){map.getCanvas().style.cursor="pointer"});
						map.on("mouseleave",l,function(){map.getCanvas().style.cursor=""});
					});
				};
				if(map.loaded()||map.isStyleLoaded()){addData()}else{map.on("load",addData)}
				/* least-effort locality: silent IP-level approximation opens the map
				   near the visitor (no permission prompt); the button uses precise
				   browser geolocation only when the user asks. */
				var near=document.getElementById("nldrone-near");
				if(near){
					near.hidden=false;
					near.addEventListener("click",function(){
						if(!navigator.geolocation)return;
						navigator.geolocation.getCurrentPosition(function(pos){
							map.easeTo({center:[pos.coords.longitude,pos.coords.latitude],zoom:12.2,pitch:58,duration:1400});
						},function(){},{ enableHighAccuracy:false, timeout:6000, maximumAge:600000 });
					});
				}
				try{
					fetch("https://ipwho.is/").then(function(r){return r.json()}).then(function(g){
						if(g&&g.success&&g.country_code==="IL"&&g.latitude){
							map.easeTo({center:[g.longitude,g.latitude],zoom:10.2,pitch:56,duration:1600});
						}
					}).catch(function(){});
				}catch(e){}
			}).catch(function(){});
		}
		if(window.mapboxgl){go();return}
		var l=document.createElement("link");l.rel="stylesheet";l.href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css";document.head.appendChild(l);
		var sc=document.createElement("script");sc.src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js";sc.onload=go;document.head.appendChild(sc);
	}
	if(band.dataset.mode==="hero"){
		// the hero map is the site opener - boot when the browser breathes
		if("requestIdleCallback" in window){requestIdleCallback(boot,{timeout:1800})}else{setTimeout(boot,400)}
	} else if(band.dataset.mode==="showcase"){
		// present itself: boot when the band approaches the viewport
		if("IntersectionObserver" in window){
			var io=new IntersectionObserver(function(es){
				es.forEach(function(e){ if(e.isIntersecting){ io.disconnect(); boot(); } });
			},{rootMargin:"260px"});
			io.observe(band);
		} else { boot(); }
	} else if(btn){
		btn.addEventListener("click",function(){
			var open=stage.hidden;
			stage.hidden=!open;
			band.classList.toggle("is-open",open);
			btn.setAttribute("aria-expanded",open?"true":"false");
			if(open)boot();
		});
	}
})();
</script>
<?php
		return ob_get_clean();
	}
}
