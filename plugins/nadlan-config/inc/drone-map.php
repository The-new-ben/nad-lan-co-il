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
			'he' => array( 'title' => 'מפת הפרויקטים החיה', 'sub' => 'לוויין ובניינים בתלת ממד מעל כל הקטלוג. הקישו על אשכול כדי לצלול לעיר.', 'toggle' => 'מפת רחפן חיה · לוויין ובניינים בתלת ממד מעל כל הקטלוג', 'note' => 'כל הקטלוג על המפה: מיקומים מאומתים, שכונתיים וברמת עיר (מקובצים). הדיוק משתפר עם אימות כתובות מול היזמים.', 'to_project' => 'לעמוד הפרויקט ←', 'projects_n' => 'פרויקטים', 'more_n' => 'ועוד {n} פרויקטים בעיר', 'city_level' => 'מיקום ברמת עיר' ),
			'en' => array( 'title' => 'The Live Project Map', 'sub' => 'Satellite and 3D buildings over the full catalog. Click a cluster to dive into a city.', 'toggle' => 'Live drone map · satellite and 3D buildings over the full catalog', 'note' => 'The whole catalog on one map: verified, neighborhood and city-level locations (clustered). Accuracy improves as addresses are verified with developers.', 'to_project' => 'To the project page →', 'projects_n' => 'projects', 'more_n' => 'and {n} more projects in this city', 'city_level' => 'city-level location' ),
			'fr' => array( 'title' => 'La carte des projets en direct', 'sub' => 'Satellite et batiments 3D sur tout le catalogue. Cliquez sur un groupe pour plonger dans une ville.', 'toggle' => 'Carte drone en direct · satellite et batiments 3D', 'note' => 'Tout le catalogue sur une carte : localisations verifiees, de quartier et de ville (regroupees). La precision s\'ameliore avec la verification des adresses.', 'to_project' => 'Vers la page du projet →', 'projects_n' => 'projets', 'more_n' => 'et {n} autres projets dans cette ville', 'city_level' => 'localisation au niveau de la ville' ),
			'ru' => array( 'title' => 'Живая карта проектов', 'sub' => 'Спутник и 3D здания над всем каталогом. Нажмите на кластер, чтобы погрузиться в город.', 'toggle' => 'Живая карта · спутник и 3D здания', 'note' => 'Весь каталог на одной карте: проверенные, районные и городские локации (сгруппированы). Точность растет с проверкой адресов.', 'to_project' => 'На страницу проекта →', 'projects_n' => 'проектов', 'more_n' => 'и еще {n} проектов в этом городе', 'city_level' => 'локация на уровне города' ),
			'ar' => array( 'title' => 'خريطة المشاريع الحية', 'sub' => 'قمر صناعي ومبان ثلاثية الأبعاد فوق الكتالوج كاملا. انقروا على مجموعة للغوص في مدينة.', 'toggle' => 'خريطة حية · قمر صناعي ومبان ثلاثية الأبعاد', 'note' => 'الكتالوج كله على خريطة واحدة: مواقع موثقة وعلى مستوى الحي والمدينة (مجمعة). تتحسن الدقة مع توثيق العناوين.', 'to_project' => 'إلى صفحة المشروع ←', 'projects_n' => 'مشاريع', 'more_n' => 'و {n} مشاريع أخرى في هذه المدينة', 'city_level' => 'موقع على مستوى المدينة' ),
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
	<?php else : ?>
	<button type="button" class="nldrone-toggle" id="nldrone-toggle" aria-expanded="false" aria-controls="nldrone-stage">
		<span class="nldrone-toggle__ic" aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M12 3v4m0 10v4M3 12h4m10 0h4"/><circle cx="12" cy="12" r="3.2"/><circle cx="12" cy="12" r="7.5" stroke-dasharray="2 3"/></svg></span>
		<span><?php echo esc_html( $L['toggle'] ); ?></span>
		<span class="nldrone-toggle__arrow" aria-hidden="true">▾</span>
	</button>
	<?php endif; ?>
	<div class="nldrone-stage" id="nldrone-stage" <?php echo 'showcase' === $mode ? '' : 'hidden'; ?>>
		<div class="nldrone-map" id="nldrone-map"></div>
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
			var map=new mapboxgl.Map({container:"nldrone-map",style:"mapbox://styles/mapbox/satellite-streets-v12",center:[34.78,32.09],zoom:11.4,pitch:58,bearing:-17,attributionControl:true});
			map.addControl(new mapboxgl.NavigationControl({visualizePitch:true}));
			map.on("load",function(){
				var layers=map.getStyle().layers,lab;
				for(var i=0;i<layers.length;i++){if(layers[i].type==="symbol"&&layers[i].layout&&layers[i].layout["text-field"]){lab=layers[i].id;break}}
				try{map.addLayer({id:"nl-3d",source:"composite","source-layer":"building",filter:["==","extrude","true"],type:"fill-extrusion",minzoom:13,paint:{"fill-extrusion-color":"#d8d2c4","fill-extrusion-height":["get","height"],"fill-extrusion-base":["get","min_height"],"fill-extrusion-opacity":.72}},lab)}catch(e){}
			});
			fetch(band.dataset.rest).then(function(r){return r.json()}).then(function(d){
				var items=d.items||[]; if(!items.length)return;
				/* the whole catalog is geocoded now (mostly city-level), so pins
				   are CLUSTERED - an honest "197 projects" bubble on a city center
				   instead of 197 stacked pins pretending to be exact addresses. */
				var gj={type:"FeatureCollection",features:items.map(function(p){
					return {type:"Feature",geometry:{type:"Point",coordinates:[p.lng,p.lat]},
						properties:{id:p.id,title:p.title,url:p.url,city:p.city||"",img:p.img||"",conf:p.conf||""}};
				})};
				var addData=function(){
					if(map.getSource("nlprojects"))return;
					map.addSource("nlprojects",{type:"geojson",data:gj,cluster:true,clusterRadius:44,clusterMaxZoom:22});
					map.addLayer({id:"nl-clusters",type:"circle",source:"nlprojects",filter:["has","point_count"],
						paint:{"circle-color":"#9C7A3C","circle-opacity":.92,"circle-stroke-width":2,"circle-stroke-color":"#FAF7F1",
							"circle-radius":["step",["get","point_count"],16,10,20,50,26,150,32]}});
					map.addLayer({id:"nl-cluster-count",type:"symbol",source:"nlprojects",filter:["has","point_count"],
						layout:{"text-field":["get","point_count_abbreviated"],"text-size":13,"text-font":["DIN Pro Medium","Arial Unicode MS Bold"]},
						paint:{"text-color":"#FAF7F1"}});
					map.addLayer({id:"nl-points",type:"circle",source:"nlprojects",filter:["!",["has","point_count"]],
						paint:{"circle-color":"#C2563A","circle-radius":8,"circle-stroke-width":2,"circle-stroke-color":"#FAF7F1"}});
					function popHtml(p){return '<div class="nldrone-pop" dir="auto"><b>'+p.title+"</b>"+(p.img?'<img src="'+p.img+'" alt="" loading="lazy">':"")+(p.city?'<div style="font-size:12px;color:#6D665C">'+p.city+(p.conf==="city"?" · "+L.city:"")+"</div>":"")+'<a href="'+p.url+'">'+L.top+"</a></div>"}
					map.on("click","nl-points",function(e){
						var p=e.features[0].properties;
						new mapboxgl.Popup({offset:14,maxWidth:"250px"}).setLngLat(e.features[0].geometry.coordinates).setHTML(popHtml(p)).addTo(map);
					});
					map.on("click","nl-clusters",function(e){
						var f=e.features[0],cid=f.properties.cluster_id,src=map.getSource("nlprojects");
						var same=map.getZoom()>=15.5;
						if(same){
							src.getClusterLeaves(cid,8,0,function(err,leaves){
								if(err)return;
								var list=leaves.map(function(l){return '<a href="'+l.properties.url+'" style="display:block;margin:4px 0">'+l.properties.title+"</a>"}).join("");
								var more=f.properties.point_count>8?'<div style="font-size:11px;color:#6D665C">ועוד '+(f.properties.point_count-8)+' פרויקטים בעיר</div>':"";
								new mapboxgl.Popup({offset:14,maxWidth:"280px"}).setLngLat(f.geometry.coordinates).setHTML('<div class="nldrone-pop" dir="auto"><b>'+f.properties.point_count+" "+L.pn+"</b>"+list+more+"</div>").addTo(map);
							});
						} else {
							src.getClusterExpansionZoom(cid,function(err,z){
								if(err)return;
								map.easeTo({center:f.geometry.coordinates,zoom:Math.min(z,15.6)});
							});
						}
					});
					["nl-points","nl-clusters"].forEach(function(l){
						map.on("mouseenter",l,function(){map.getCanvas().style.cursor="pointer"});
						map.on("mouseleave",l,function(){map.getCanvas().style.cursor=""});
					});
				};
				if(map.loaded()||map.isStyleLoaded()){addData()}else{map.on("load",addData)}
				var b=new mapboxgl.LngLatBounds();
				items.forEach(function(p){b.extend([p.lng,p.lat])});
				map.fitBounds(b,{padding:70,pitch:58,bearing:-17,maxZoom:12.5});
			}).catch(function(){});
		}
		if(window.mapboxgl){go();return}
		var l=document.createElement("link");l.rel="stylesheet";l.href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css";document.head.appendChild(l);
		var sc=document.createElement("script");sc.src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js";sc.onload=go;document.head.appendChild(sc);
	}
	if(band.dataset.mode==="showcase"){
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
