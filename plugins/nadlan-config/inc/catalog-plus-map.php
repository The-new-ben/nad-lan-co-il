<?php
/* x-catalog-plus · map v2 (6.9.2026, owner: "small square on top, click opens a real map centred where I am, prices on the pins, heat map")
 * Concatenated after catalog-plus.php by scripts/catalog-plus/deploycp.py. Additive; nothing here edits the drone map module.
 *  - Thumbnail: a Mapbox static image (light style) with HTML price chips projected onto it (Web Mercator, in JS). One <a>, one image.
 *  - Full map (opens on click, Mapbox GL loaded on demand): project pins as price pills (Booking pattern), clusters, mini card,
 *    heat: Tel Aviv neighborhoods choropleth (₪/sqm from Tax Authority deals) + city circles for the other 19 cities, "near me", pulse.
 *  - Project pages: "מה קורה מסביב" from find-place (schools, light rail, parks, active construction, plans) + a static mini map. */

if ( ! function_exists( 'nadlan_cp_mapbox_token' ) ) {
	function nadlan_cp_mapbox_token() { return trim( (string) get_option( 'nadlan_mapbox_token', '' ) ); }
}
if ( ! function_exists( 'nadlan_cp_uploads_url' ) ) {
	function nadlan_cp_uploads_url( $file ) { $up = wp_get_upload_dir(); return trailingslashit( $up['baseurl'] ) . 'nadlan-skin/' . $file; }
}
if ( ! function_exists( 'nadlan_cp_uploads_path' ) ) {
	function nadlan_cp_uploads_path( $file ) { $up = wp_get_upload_dir(); return trailingslashit( $up['basedir'] ) . 'nadlan-skin/' . $file; }
}
if ( ! function_exists( 'nadlan_cp_map_cities' ) ) {
	/** Cities with coordinates + ₪/sqm + project count: the data behind the thumbnail chips and the city heat circles. */
	function nadlan_cp_map_cities( $facets ) {
		$coords = nadlan_cp_city_coords(); $counts = array();
		foreach ( (array) ( $facets['cities'] ?? array() ) as $c ) { $counts[ nadlan_cp_city_key( $c['name'] ) ] = (int) $c['n']; }
		$out = array();
		foreach ( $coords as $name => $ll ) {
			$row = nadlan_cp_city_data( $name ); $n = $counts[ nadlan_cp_city_key( $name ) ] ?? 0;
			if ( ! $row && ! $n ) { continue; }
			$out[] = array( 'name' => $name, 'lat' => $ll[0], 'lng' => $ll[1], 'psqm' => $row ? (int) $row['psqm_all'] : 0, 'deals' => $row ? (int) $row['deals_24m'] : 0, 'period' => $row ? nadlan_cp_period( $row ) : '', 'n' => $n, 'url' => nadlan_cp_city_hub_url( $name ) );
		}
		usort( $out, function ( $a, $b ) { return $b['n'] - $a['n']; } );
		return $out;
	}
}
if ( ! function_exists( 'nadlan_cp_map_thumb_html' ) ) {
	function nadlan_cp_map_thumb_html() {
		$tok = nadlan_cp_mapbox_token(); if ( '' === $tok ) { return ''; }
		/* portrait crop of the whole country; chips are placed by JS from the same center/zoom */
		$src = 'https://api.mapbox.com/styles/v1/mapbox/light-v11/static/34.88,32.02,7.15,0/240x240@2x?access_token=' . rawurlencode( $tok ) . '&attribution=false&logo=false';
		return '<a class="nlcp-mapthumb" id="nlcp-mapthumb" href="#map" data-center="34.88,32.02" data-zoom="7.15" data-w="240" data-h="240" aria-label="פתיחת מפת הפרויקטים והמחירים">'
			. '<img src="' . esc_url( $src ) . '" alt="מפת פרויקטים חדשים ומחיר למ״ר לפי עיר" width="240" height="240" loading="eager" decoding="async" referrerpolicy="no-referrer-when-downgrade">'
			. '<span class="nlcp-mapthumb__chips" aria-hidden="true"></span>'
			. '<span class="nlcp-mapthumb__cta"><b>מפת מחירים ופרויקטים</b><small>מחיר למ״ר על כל פרויקט · לחיצה פותחת</small></span>'
			. '<span class="nlcp-mapthumb__near"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>פרויקטים לידי</span></a>';
	}
}
if ( ! function_exists( 'nadlan_cp_map_shell_html' ) ) {
	function nadlan_cp_map_shell_html() {
		return '<div class="nlcp-map" id="nlcp-map" hidden role="dialog" aria-modal="true" aria-label="מפת הפרויקטים והמחירים">'
			. '<div class="nlcp-map__bar"><button type="button" class="nlcp-map__close" id="nlcp-map-close">סגירה</button>'
			. '<div class="nlcp-map__title"><b>מפת פרויקטים חדשים ומחירים</b><span id="nlcp-map-sub">מחיר למ״ר בסביבת כל פרויקט, לפי עסקאות שדווחו לרשות המסים</span></div>'
			. '<div class="nlcp-map__tools"><button type="button" class="nlcp-map__tool" id="nlcp-map-near">פרויקטים לידי</button>'
			. '<label class="nlcp-map__tool nlcp-map__toggle"><input type="checkbox" id="nlcp-map-heat" checked> מפת חום מחירים</label></div></div>'
			. '<div class="nlcp-map__stage" id="nlcp-map-stage"></div>'
			. '<div class="nlcp-map__legend" id="nlcp-map-legend"><span>₪ למ״ר</span><i style="background:#DCEBF0"></i><small>עד 20K</small><i style="background:#9CC4D1"></i><small>30K</small><i style="background:#5F98AB"></i><small>45K</small><i style="background:#2F6F86"></i><small>60K</small><i style="background:#1F4B5C"></i><small>70K+</small></div>'
			. '<aside class="nlcp-map__card" id="nlcp-map-card" hidden></aside></div>';
	}
}
if ( ! function_exists( 'nadlan_cp_map_assets' ) ) {
	function nadlan_cp_map_assets( $facets ) {
		$cities = wp_json_encode( nadlan_cp_map_cities( $facets ), JSON_UNESCAPED_UNICODE );
		$cfg = wp_json_encode( array(
			'token' => nadlan_cp_mapbox_token(), 'projects' => esc_url_raw( rest_url( 'nadlan/v1/project-map' ) ),
			'hoods' => file_exists( nadlan_cp_uploads_path( 'tlv-neighborhoods-psqm.geojson' ) ) ? nadlan_cp_uploads_url( 'tlv-neighborhoods-psqm.geojson' ) : '',
			'gl' => 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js', 'glcss' => 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css', 'rtl' => 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js',
		), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
		return <<<HTML
<style id="nlcp-map-css">
.nlcp-herogrid{display:grid;grid-template-columns:minmax(0,1fr) 240px;gap:14px;max-width:1180px;margin:14px auto 0;align-items:stretch}
.nlcp-herogrid .nlcp-bar{margin:0}
.nlcp-herogrid{align-items:start}
.nlcp-mapthumb{position:relative;display:block;border-radius:14px;overflow:hidden;border:1px solid var(--sa-line,#E3E1DA);background:#EAF0F2;text-decoration:none;color:inherit;aspect-ratio:1/1;width:100%;box-shadow:0 12px 30px rgba(20,33,43,.06)}
.nlcp-mapthumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;display:block;filter:saturate(.85)}
.nlcp-mapthumb__chips{position:absolute;inset:0}
.nlcp-chip{position:absolute;transform:translate(-50%,-100%);background:var(--sa-deep,#1F4B5C);color:#fff;font-size:10.5px;font-weight:700;padding:2px 6px;border-radius:999px;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,.25);font-variant-numeric:tabular-nums}
.nlcp-chip::after{content:"";position:absolute;left:50%;bottom:-4px;width:6px;height:6px;background:inherit;transform:translateX(-50%) rotate(45deg)}
.nlcp-chip--hot{background:var(--sa-sea,#2F6F86)}
.nlcp-mapthumb__cta{position:absolute;inset-inline:10px;bottom:10px;background:rgba(255,255,255,.94);border-radius:10px;padding:8px 10px;display:flex;flex-direction:column;gap:1px}
.nlcp-mapthumb__cta b{font-size:13px;color:var(--sa-ink,#14212B)}.nlcp-mapthumb__cta small{font-size:11px;color:var(--sa-mute,#6B7680)}
.nlcp-mapthumb__near{position:absolute;top:10px;inset-inline-start:10px;background:var(--sa-sea,#2F6F86);color:#fff;font-size:11.5px;font-weight:700;padding:5px 9px;border-radius:999px;display:inline-flex;gap:5px;align-items:center}
.nlcp-mapthumb:hover img{filter:saturate(1)}
@media(max-width:1000px){.nlcp-herogrid{grid-template-columns:1fr}.nlcp-mapthumb{max-width:300px;margin:0 auto}}
.nlcp-map{position:fixed;inset:0;z-index:99999;background:#F7F6F2;display:flex;flex-direction:column}
.nlcp-map[hidden]{display:none}
.nlcp-map__bar{display:flex;align-items:center;gap:12px;padding:10px 14px;background:#fff;border-bottom:1px solid var(--sa-line,#E3E1DA);flex-wrap:wrap}
.nlcp-map__title{flex:1;min-width:200px;display:flex;flex-direction:column}.nlcp-map__title b{font-size:15px;color:var(--sa-ink,#14212B)}.nlcp-map__title span{font-size:12px;color:var(--sa-mute,#6B7680)}
.nlcp-map__close{border:0;border-radius:999px;background:var(--sa-deep,#1F4B5C);color:#fff;font:inherit;font-weight:700;padding:8px 14px;cursor:pointer}
.nlcp-map__tools{display:flex;gap:8px;align-items:center}
.nlcp-map__tool{border:1px solid var(--sa-line,#E3E1DA);background:#fff;border-radius:999px;padding:7px 12px;font:inherit;font-size:13px;font-weight:600;color:var(--sa-deep,#1F4B5C);cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.nlcp-map__tool.is-busy{opacity:.6}
.nlcp-map__stage{flex:1;min-height:0}
.nlcp-map__legend{position:absolute;bottom:14px;inset-inline-start:14px;background:rgba(255,255,255,.95);border:1px solid var(--sa-line,#E3E1DA);border-radius:10px;padding:7px 10px;display:flex;align-items:center;gap:5px;font-size:11px;color:var(--sa-ink2,#3B4753)}
.nlcp-map__legend i{width:16px;height:10px;border-radius:2px;display:inline-block}.nlcp-map__legend span{font-weight:700;margin-inline-end:4px}
.nlcp-map__card{position:absolute;top:70px;inset-inline-end:14px;width:300px;max-width:calc(100vw - 28px);background:#fff;border:1px solid var(--sa-line,#E3E1DA);border-radius:14px;box-shadow:0 20px 50px rgba(0,0,0,.18);overflow:hidden;z-index:2}
.nlcp-map__card[hidden]{display:none}
.nlcp-map__card img{width:100%;height:150px;object-fit:cover;display:block}
.nlcp-map__card .in{padding:12px 14px}.nlcp-map__card h3{margin:0 0 4px;font-size:15px;line-height:1.3;color:var(--sa-ink,#14212B)}
.nlcp-map__card .meta{font-size:12.5px;color:var(--sa-ink2,#3B4753);display:flex;flex-wrap:wrap;gap:4px 10px;margin-bottom:8px}
.nlcp-map__card .ctx{background:var(--sa-sand,#EEE9DD);border-radius:9px;padding:8px 10px;font-size:12.5px;margin-bottom:10px}.nlcp-map__card .ctx b{color:var(--sa-ink,#14212B)}
.nlcp-map__card a.go{display:inline-block;background:var(--sa-sea,#2F6F86);color:#fff;border-radius:999px;padding:8px 14px;font-weight:700;font-size:13px;text-decoration:none}
.nlcp-map__card .x{position:absolute;top:8px;inset-inline-start:8px;border:0;border-radius:50%;width:28px;height:28px;background:rgba(255,255,255,.9);cursor:pointer;font-size:16px;line-height:1}
.mapboxgl-marker{width:auto!important;max-width:none!important}
.nlcp-pin{display:inline-block;width:max-content;max-width:none;background:var(--sa-deep,#1F4B5C);color:#fff;border-radius:999px;padding:3px 8px;font:700 12px/1.3 Assistant,Heebo,sans-serif;white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,.28);cursor:pointer;font-variant-numeric:tabular-nums;border:2px solid #fff}
.mapboxgl-marker.nlcp-pin.is-dot{width:13px!important;min-width:13px;height:13px;padding:0;border-radius:50%;background:var(--sa-sea,#2F6F86)!important;border-color:#fff!important}.nlcp-pin.is-dot:hover{box-shadow:0 0 0 4px rgba(47,111,134,.25)}.nlcp-pin.is-dot::after{display:none}
/* escaping: Code Snippets strips one slash level, the PHP heredoc another; write \\n here to get 
 in JS. never set position on .nlcp-pin/.nlcp-cluster: Mapbox positions markers with position:absolute + transform; a relative pin lands hundreds of px off its coordinate */
.nlcp-pin::after{content:"";position:absolute;left:50%;bottom:-6px;width:8px;height:8px;background:var(--sa-deep,#1F4B5C);transform:translateX(-50%) rotate(45deg)}
.nlcp-pin.is-featured{background:var(--sa-sea,#2F6F86)}.nlcp-pin.is-featured::after{background:var(--sa-sea,#2F6F86)}
.nlcp-pin.is-city{background:#fff;color:var(--sa-deep,#1F4B5C);border-color:var(--sa-deep,#1F4B5C)}.nlcp-pin.is-city::after{background:#fff}
.nlcp-pin.is-active{background:#C2563A}.nlcp-pin.is-active::after{background:#C2563A}
.nlcp-pin.is-pulse::before{content:"";position:absolute;inset:-6px;border-radius:999px;border:2px solid var(--sa-sea,#2F6F86);animation:nlcpPulse 1.4s ease-out 3}
@keyframes nlcpPulse{0%{transform:scale(.9);opacity:.9}100%{transform:scale(1.8);opacity:0}}
@media(max-width:640px){.nlcp-map__bar{gap:8px;padding:8px 10px}.nlcp-map__close{order:0;padding:7px 12px;font-size:13px}.nlcp-map__tools{order:1;margin-inline-start:auto}.nlcp-map__tool{padding:6px 9px;font-size:12px}.nlcp-map__title{order:2;flex:1 1 100%;min-width:0}.nlcp-map__title b{font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.nlcp-map__title span{font-size:11.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.nlcp-map__card{top:auto;bottom:14px;inset-inline-end:14px;inset-inline-start:14px;width:auto;max-width:none}.nlcp-map__legend{bottom:auto;top:132px;padding:5px 8px}}
.nlcp-cluster{display:grid;width:38px!important;height:38px;border-radius:50%;background:var(--sa-deep,#1F4B5C);color:#fff;display:grid;place-items:center;font:700 13px Assistant,Heebo,sans-serif;border:3px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,.25);cursor:pointer}
.mapboxgl-popup{z-index:3}
body.nlcp-map-open{overflow:hidden}
</style>
<script id="nlcp-map-js">
(function(){
	var CFG=$cfg, CITIES=$cities;
	var thumb=document.getElementById('nlcp-mapthumb'), shell=document.getElementById('nlcp-map');
	if(!thumb||!shell||!CFG.token)return;
	/* --- thumbnail chips: Web Mercator projection onto the static image --- */
	function proj(lng,lat,z){var s=256*Math.pow(2,z);var x=(lng+180)/360*s;var r=lat*Math.PI/180;var y=(1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2*s;return [x,y];}
	function placeChips(){var c=thumb.dataset.center.split(',').map(Number),z=+thumb.dataset.zoom,W=+thumb.dataset.w,H=+thumb.dataset.h;var box=thumb.getBoundingClientRect();var sx=box.width/W,sy=box.height/H;var cen=proj(c[0],c[1],z);var host=thumb.querySelector('.nlcp-mapthumb__chips');host.innerHTML='';
		var max=Math.max.apply(null,CITIES.map(function(x){return x.psqm||0;}));
		var placed=[];
		CITIES.filter(function(x){return x.psqm>0;}).slice(0,14).forEach(function(x){var p=proj(x.lng,x.lat,z);var px=(W/2+(p[0]-cen[0]))*sx,py=(H/2+(p[1]-cen[1]))*sy;if(px<36||py<44||px>box.width-36||py>box.height-66)return;if(placed.some(function(q){return Math.abs(q[0]-px)<70&&Math.abs(q[1]-py)<18;}))return;placed.push([px,py]);var el=document.createElement('span');el.className='nlcp-chip'+(x.psqm>=max*.8?' nlcp-chip--hot':'');el.style.left=px+'px';el.style.top=py+'px';el.textContent=x.name+' '+Math.round(x.psqm/1000)+'K';host.appendChild(el);});}
	placeChips();window.addEventListener('resize',placeChips);
	/* --- full map --- */
	var map=null,markers={},loaded=false,active=null,cardEl=document.getElementById('nlcp-map-card'),catalogState=function(){try{return new URLSearchParams(location.search).get('city')||'';}catch(e){return '';}};
	function loadScript(src){return new Promise(function(res,rej){if(document.querySelector('script[src="'+src+'"]'))return res();var s=document.createElement('script');s.src=src;s.onload=res;s.onerror=rej;document.head.appendChild(s);});}
	function loadCss(href){if(document.querySelector('link[href="'+href+'"]'))return;var l=document.createElement('link');l.rel='stylesheet';l.href=href;document.head.appendChild(l);}
	function color(p){return p>=70000?'#1F4B5C':p>=60000?'#2F6F86':p>=45000?'#5F98AB':p>=30000?'#9CC4D1':p>0?'#DCEBF0':'#EEE9DD';}
	function nis(n){return Number(n).toLocaleString('he-IL')+' ₪';}
	function cityOf(name){var k=(name||'').replace(/[-־]/g,' ').replace(/\s+/g,' ').trim();if(!k)return null;if(k.indexOf('תל אביב')===0)k='תל אביב יפו';k=k.replace('הרצלייה','הרצליה').replace('פתח תקוה','פתח תקווה');return CITIES.find(function(c){return c.name===k||k.indexOf(c.name)===0||c.name.indexOf(k)===0;});}
	function open(opts){opts=opts||{};shell.hidden=false;document.body.classList.add('nlcp-map-open');if(map){setTimeout(function(){try{map.resize();}catch(e){}},50);}if(!loaded){loaded=true;loadCss(CFG.glcss);loadScript(CFG.gl).then(function(){return loadScript(CFG.rtl).catch(function(){});}).then(function(){boot(opts);}).catch(function(){document.getElementById('nlcp-map-sub').textContent='המפה לא נטענה. נסו שוב או המשיכו ברשימה.';});}else if(map){focus(opts);}}
	function close(){shell.hidden=true;document.body.classList.remove('nlcp-map-open');if(location.hash.indexOf('#map')===0)history.replaceState(null,'',location.pathname+location.search);}
	function boot(opts){mapboxgl.accessToken=CFG.token;try{if(mapboxgl.getRTLTextPluginStatus&&mapboxgl.getRTLTextPluginStatus()==='unavailable')mapboxgl.setRTLTextPlugin(CFG.rtl,null,true);}catch(e){}
		var stage=document.getElementById('nlcp-map-stage');stage.innerHTML='';
		map=new mapboxgl.Map({container:stage,style:'mapbox://styles/mapbox/light-v11',center:[34.85,32.0],zoom:8.2,attributionControl:true,cooperativeGestures:false});
		window.NLCP_MAP.map=map;
		map.on('error',function(e){console.warn('nlcp-map error: '+(e&&e.error&&e.error.message||e)+' | src='+(e&&e.sourceId||'-')+' | keys='+Object.keys(e||{}).join(',')+' | type='+(e&&e.error&&e.error.name||'')+(e&&e.error&&e.error.stack?' | '+String(e.error.stack).split('\\n').slice(0,3).join(' / '):''));});
		map.addControl(new mapboxgl.NavigationControl({showCompass:false}),'top-left');
		var built=false;function build(){if(built)return;built=true;try{addHeat();}catch(e){console.warn('nlcp heat',e);}try{addProjects(opts);}catch(e){console.warn('nlcp projects',e);}}
		map.on('load',build);map.once('idle',build);map.on('style.load',function(){build();});setTimeout(function(){build();},5000);
		[150,600,1500].forEach(function(t){setTimeout(function(){try{map.resize();}catch(e){}},t);});
	}
	function addHeat(){
		map.addSource('nlcp-cities',{type:'geojson',data:{type:'FeatureCollection',features:CITIES.filter(function(c){return c.psqm>0;}).map(function(c){return {type:'Feature',properties:{name:c.name,psqm:c.psqm,n:c.n,color:color(c.psqm),r:Math.max(10,Math.min(34,6+Math.sqrt(c.n)*2.6))},geometry:{type:'Point',coordinates:[c.lng,c.lat]}};})}});
		map.addLayer({id:'nlcp-city-heat',type:'circle',source:'nlcp-cities',paint:{'circle-color':['get','color'],'circle-radius':['interpolate',['linear'],['zoom'],6,['get','r'],11,['*',['get','r'],2.2],13,1],'circle-opacity':['interpolate',['linear'],['zoom'],6,.55,11,.35,12.5,0],'circle-blur':.6}});
		map.addLayer({id:'nlcp-city-label',type:'symbol',source:'nlcp-cities',minzoom:6.5,maxzoom:12,layout:{'text-field':['concat',['get','name'],'\\n',['number-format',['get','psqm'],{'locale':'he','max-fraction-digits':0}],' ₪'],'text-size':11,'text-offset':[0,0],'text-font':['DIN Pro Medium','Arial Unicode MS Regular']},paint:{'text-color':'#14212B','text-halo-color':'#fff','text-halo-width':1.2}});
		if(CFG.hoods){map.addSource('nlcp-hoods',{type:'geojson',data:CFG.hoods});
			map.addLayer({id:'nlcp-hoods-fill',type:'fill',source:'nlcp-hoods',minzoom:10.5,paint:{'fill-color':['case',['>',['coalesce',['get','psqm'],0],0],['interpolate',['linear'],['get','psqm'],20000,'#DCEBF0',30000,'#9CC4D1',45000,'#5F98AB',60000,'#2F6F86',75000,'#1F4B5C'],'#EEE9DD'],'fill-opacity':.42}},'nlcp-city-heat');
			map.addLayer({id:'nlcp-hoods-line',type:'line',source:'nlcp-hoods',minzoom:10.5,paint:{'line-color':'#fff','line-width':1}});
			map.addLayer({id:'nlcp-hoods-label',type:'symbol',source:'nlcp-hoods',minzoom:12,layout:{'text-field':['case',['>',['coalesce',['get','psqm'],0],0],['concat',['get','name'],'\\n',['number-format',['get','psqm'],{'locale':'he','max-fraction-digits':0}],' ₪'],['get','name']],'text-size':11,'text-font':['DIN Pro Medium','Arial Unicode MS Regular']},paint:{'text-color':'#14212B','text-halo-color':'#fff','text-halo-width':1.4}});
			map.on('click','nlcp-hoods-fill',function(e){var p=e.features[0].properties;if(!p.psqm)return;new mapboxgl.Popup({closeButton:true,offset:6}).setLngLat(e.lngLat).setHTML('<div style="font:13px Assistant,Heebo,sans-serif;direction:rtl"><b>'+p.name+'</b><br>מחיר למ״ר: <b>'+nis(p.psqm)+'</b><br><small>'+p.deals_24m+' עסקאות, '+p.period_from+' עד '+p.period_to+(p.price_4r?'<br>דירת 4 חדרים, חציון: '+nis(p.price_4r):'')+'</small></div>').addTo(map);});}
		var heat=document.getElementById('nlcp-map-heat');heat.addEventListener('change',function(){var v=heat.checked?'visible':'none';['nlcp-city-heat','nlcp-city-label','nlcp-hoods-fill','nlcp-hoods-line','nlcp-hoods-label'].forEach(function(id){if(map.getLayer(id))map.setLayoutProperty(id,'visibility',v);});});
	}
	function addProjects(opts){fetch(CFG.projects,{headers:{Accept:'application/json'}}).then(function(r){return r.json();}).then(function(d){var items=(d&&d.items)||[];
			var feats=items.filter(function(p){return p.lat&&p.lng;}).map(function(p){var c=cityOf(p.city);var ctx=p.psqm>0?p.psqm:(c?c.psqm:0);return {type:'Feature',properties:{id:p.id,title:p.title,url:p.url,city:p.city,img:p.img||p.poster||'',units:p.units||0,status:p.status||'',own:p.psqm>0?1:0,psqm:ctx,featured:p.featured?1:0},geometry:{type:'Point',coordinates:[+p.lng,+p.lat]}};});
			map.addSource('nlcp-proj',{type:'geojson',data:{type:'FeatureCollection',features:feats},cluster:true,clusterMaxZoom:11,clusterRadius:38  /* integer only: a fractional maxZoom makes supercluster throw 'Invalid array length' */});
			map.addLayer({id:'nlcp-proj-hidden',type:'circle',source:'nlcp-proj',paint:{'circle-opacity':0,'circle-radius':1}});
			map.on('sourcedata',function(e){if(e&&e.sourceId==='nlcp-proj')sync();});map.on('moveend',sync);map.on('idle',sync);sync();focus(opts);map.once('idle',function(){if(!opts.project&&!opts.lnglat)setTimeout(function(){pulseIn(map.getBounds());},300);});
		}).catch(function(){document.getElementById('nlcp-map-sub').textContent='רשימת הפרויקטים לא נטענה למפה.';});}
	function sync(){if(!map.getSource('nlcp-proj')||!map.isSourceLoaded('nlcp-proj'))return;var feats=map.querySourceFeatures('nlcp-proj');var keep={};
		feats.forEach(function(f){var p=f.properties,id=p.cluster?'c'+p.cluster_id:'p'+p.id;keep[id]=1;if(markers[id])return;var el=document.createElement('div');
			if(p.cluster){el.className='nlcp-cluster';el.textContent=p.point_count;el.addEventListener('click',function(){map.getSource('nlcp-proj').getClusterExpansionZoom(p.cluster_id,function(err,z){if(err)return;map.easeTo({center:f.geometry.coordinates,zoom:z+.4});});});}
			else{el.className='nlcp-pin'+(p.featured?' is-featured':'')+(p.own?'':' is-city is-dot');el.innerHTML=p.own?('<b>'+Math.round(p.psqm/1000)+'K</b> ₪/מ״ר'):'';el.title=p.title;el.addEventListener('click',function(){showCard(f);});}
			markers[id]=new mapboxgl.Marker({element:el,anchor:(p.cluster||!p.own)?'center':'bottom'}).setLngLat(f.geometry.coordinates).addTo(map);});
		Object.keys(markers).forEach(function(id){if(!keep[id]){markers[id].remove();delete markers[id];}});}
	function showCard(f){var p=f.properties;active=p.id;document.querySelectorAll('.nlcp-pin.is-active').forEach(function(e){e.classList.remove('is-active');});var m=markers['p'+p.id];if(m)m.getElement().classList.add('is-active');
		var c=cityOf(p.city);var ctx=p.own?('מחיר למ״ר בפרויקט, לפי היזם: <b>'+nis(p.psqm)+'</b>'+(c&&c.psqm?'<br>בעיר: '+nis(c.psqm):'')):(c&&c.psqm?'מחיר למ״ר ב'+c.name+': <b>'+nis(c.psqm)+'</b><br><small>'+c.deals.toLocaleString('he-IL')+' עסקאות, '+c.period+' · רשות המסים</small>':'');
		cardEl.innerHTML='<button type="button" class="x" aria-label="סגירה">×</button>'+(p.img?'<img src="'+p.img+'" alt="">':'')+'<div class="in"><h3>'+p.title+'</h3><div class="meta">'+(p.city?'<span>'+p.city+'</span>':'')+(p.units?'<span>'+p.units+' יח״ד</span>':'')+'</div>'+(ctx?'<div class="ctx">'+ctx+'</div>':'')+'<a class="go" href="'+p.url+'">לעמוד הפרויקט</a></div>';
		cardEl.hidden=false;cardEl.querySelector('.x').addEventListener('click',function(){cardEl.hidden=true;});map.easeTo({center:f.geometry.coordinates,offset:[0,60]});}
	function pulseIn(bounds){setTimeout(function(){Object.keys(markers).forEach(function(id){if(id[0]!=='p')return;var ll=markers[id].getLngLat();if(bounds.contains(ll))markers[id].getElement().classList.add('is-pulse');});setTimeout(function(){document.querySelectorAll('.nlcp-pin.is-pulse').forEach(function(e){e.classList.remove('is-pulse');});},4500);},700);}
	function focus(opts){if(!map)return;var sub=document.getElementById('nlcp-map-sub');
		if(opts.project){var f=(map.getSource('nlcp-proj')&&map.getSource('nlcp-proj')._data.features||[]).find(function(x){return String(x.properties.id)===String(opts.project);});if(f){map.jumpTo({center:f.geometry.coordinates,zoom:14.5});setTimeout(function(){showCard(f);var m=markers['p'+f.properties.id];if(m)m.getElement().classList.add('is-pulse');},900);return;}}
		if(opts.lnglat){map.flyTo({center:opts.lnglat,zoom:13,speed:1.4});sub.textContent='הפרויקטים החדשים סביב המיקום שלכם.';map.once('moveend',function(){pulseIn(map.getBounds());});return;}
		var city=cityOf(opts.city||catalogState());if(city){map.flyTo({center:[city.lng,city.lat],zoom:city.name==='תל אביב יפו'?12.3:12,speed:1.4});sub.textContent='פרויקטים חדשים ב'+city.name+(city.psqm?' · מחיר למ״ר בעיר: '+nis(city.psqm):'');map.once('moveend',function(){pulseIn(map.getBounds());});}
		else{map.fitBounds([[34.25,29.45],[35.9,33.35]],{padding:20,duration:0});}}
	function near(btn){if(!navigator.geolocation){open({});return;}btn&&btn.classList.add('is-busy');navigator.geolocation.getCurrentPosition(function(pos){btn&&btn.classList.remove('is-busy');open({lnglat:[pos.coords.longitude,pos.coords.latitude]});},function(){btn&&btn.classList.remove('is-busy');open({});},{timeout:8000,maximumAge:600000});}
	thumb.addEventListener('click',function(e){e.preventDefault();if(e.target.closest('.nlcp-mapthumb__near')){near(e.target.closest('.nlcp-mapthumb__near'));return;}history.replaceState(null,'',location.pathname+location.search+'#map');open({});});
	document.getElementById('nlcp-map-close').addEventListener('click',close);
	document.getElementById('nlcp-map-near').addEventListener('click',function(){near(this);});
	document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!shell.hidden)close();});
	var pm=document.querySelector('.nlcp-pricemap');if(pm){var b=document.createElement('button');b.type='button';b.className='nlcp-near';b.style.marginTop='8px';b.textContent='פתיחת המפה המלאה';b.addEventListener('click',function(){open({});});pm.appendChild(b);}
	if(location.hash.indexOf('#map')===0){var hm=location.hash.match(/^#map(?:=(\d+))?/);var go=function(){setTimeout(function(){open(hm&&hm[1]?{project:hm[1]}:{});},250);};if(document.readyState==='complete')go();else window.addEventListener('load',go);}
	window.NLCP_MAP={open:open,close:close};
})();
</script>
HTML;
	}
}

/* ------------------------------------------------------------------ project pages: what surrounds the project (find-place) */
if ( ! function_exists( 'nadlan_cp_surroundings' ) ) {
	function nadlan_cp_surroundings( $id ) {
		static $d = null;
		if ( null === $d ) {
			$d = get_transient( 'nadlan_cp_surr_v1' );
			if ( ! is_array( $d ) ) { $p = nadlan_cp_uploads_path( 'project-surroundings-v1.json' ); $d = file_exists( $p ) ? (array) json_decode( (string) file_get_contents( $p ), true ) : array(); set_transient( 'nadlan_cp_surr_v1', $d, 6 * HOUR_IN_SECONDS ); }
		}
		return $d['projects'][ (string) $id ] ?? null;
	}
}
if ( ! function_exists( 'nadlan_cp_plan_status_he' ) ) {
	function nadlan_cp_plan_status_he( $s ) { $m = array( 'approved' => 'מאושרת', 'in_force' => 'בתוקף', 'deposited' => 'בהפקדה', 'in_progress' => 'בתהליך', 'proposed' => 'מוצעת', 'not_applicable' => '' ); return $m[ (string) $s ] ?? (string) $s; }
}
if ( ! function_exists( 'nadlan_cp_surroundings_html' ) ) {
	function nadlan_cp_surroundings_html( $id ) {
		$s = nadlan_cp_surroundings( $id ); if ( ! $s ) { return ''; }
		$lat = (float) get_post_meta( $id, 'lat', true ); $lng = (float) get_post_meta( $id, 'lng', true ); $tok = nadlan_cp_mapbox_token();
		$tiles = array();
		if ( ! empty( $s['rail'] ) ) { $r = $s['rail']; $tiles[] = array( 'רכבת קלה', $r['name'], $r['operational'] ? 'פעילה, ' . $r['m'] . ' מ׳ הליכה' : ( 'approved' === ( $r['planning'] ?? '' ) ? 'מאושרת, ' . $r['m'] . ' מ׳' : $r['m'] . ' מ׳' ) ); }
		if ( ! empty( $s['schools'] ) ) { $names = array_map( function ( $x ) { return str_replace( 'בית הספר ', '', $x['name'] ); }, array_slice( $s['schools'], 0, 3 ) ); $tiles[] = array( 'בתי ספר במרחק הליכה', implode( ' · ', $names ), count( $s['schools'] ) . ' עד 900 מ׳' ); }
		if ( ! empty( $s['kindergartens_600m'] ) ) { $tiles[] = array( 'גני ילדים', (string) $s['kindergartens_600m'], 'עד 600 מ׳' ); }
		if ( ! empty( $s['parks'] ) ) { $tiles[] = array( 'פארקים וחופים', implode( ' · ', array_map( function ( $x ) { return $x['name']; }, $s['parks'] ) ), $s['parks'][0]['m'] . ' מ׳ לקרוב' ); }
		if ( ! empty( $s['construction'] ) ) { $c = $s['construction']; $tiles[] = array( 'בנייה מסביב', $c['active_500m'] . ' אתרים פעילים', 'ברדיוס 500 מ׳ · הקרוב: ' . $c['nearest']['name'] . ', ' . $c['nearest']['m'] . ' מ׳' ); }
		if ( ! empty( $s['plans'] ) ) { $p = $s['plans'][0]; $tiles[] = array( 'תכנון עתידי', $p['name'], trim( nadlan_cp_plan_status_he( $p['status'] ) . ( $p['inside'] ? ' · הפרויקט בתחום התוכנית' : '' ) ) ); }
		if ( ! $tiles ) { return ''; }
		$nb = ! empty( $s['neighborhood'] ) ? $s['neighborhood'] : '';
		if ( $nb && "'" === mb_substr( $nb, 0, 1 ) ) { $nb = mb_substr( $nb, 1 ) . "'"; }
		$img = '';
		if ( $tok && $lat && $lng ) {
			$src = 'https://api.mapbox.com/styles/v1/mapbox/light-v11/static/pin-l+2F6F86(' . $lng . ',' . $lat . ')/' . $lng . ',' . $lat . ',14.2,0/640x300@2x?access_token=' . rawurlencode( $tok ) . '&attribution=false&logo=false';
			$img = '<a class="nlcp-surr__map" href="' . esc_url( home_url( '/projects/#map=' . (int) $id ) ) . '"><img src="' . esc_url( $src ) . '" alt="מפת הסביבה של ' . esc_attr( get_the_title( $id ) ) . ( $nb ? ', ' . esc_attr( $nb ) : '' ) . '" width="640" height="300" loading="lazy" decoding="async"><span>פתיחת המפה עם המחירים מסביב</span></a>';
		}
		$h  = '<section class="nlcp-surr" dir="rtl" aria-label="מה קורה מסביב"><div class="nlcp-surr__head"><span class="nlcp-projctx__k">מה קורה מסביב</span><h2>' . ( $nb ? 'הסביבה: ' . esc_html( $nb ) : 'הסביבה של הפרויקט' ) . '</h2><p>מה שקיים ומה שמתוכנן במרחק הליכה: תחבורה, חינוך, פארקים, בנייה ותוכניות. מקור: find-place, שכבות מידע עירוניות וממשלתיות.</p></div><div class="nlcp-surr__grid">' . $img . '<div class="nlcp-surr__tiles">';
		foreach ( $tiles as $t ) { $h .= '<div class="nlcp-tile"><small>' . esc_html( $t[0] ) . '</small><b>' . esc_html( $t[1] ) . '</b><span>' . esc_html( $t[2] ) . '</span></div>'; }
		$h .= '</div></div></section>';
		$h .= '<style>.nlcp-surr{max-width:1180px;margin:0 auto 22px;padding:20px clamp(16px,2.5vw,28px);background:var(--sa-surf,#fff);border:1px solid var(--sa-line,#E3E1DA);border-radius:18px}.nlcp-surr h2{margin:0 0 6px;font-family:var(--sa-serif,"Noto Serif Hebrew",serif);font-size:clamp(20px,2.2vw,26px);color:var(--sa-ink,#14212B)}.nlcp-surr__head p{margin:0 0 14px;color:var(--sa-ink2,#3B4753);font-size:14.5px;line-height:1.55}.nlcp-surr__grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:14px;align-items:start}.nlcp-surr__map{position:relative;display:block;border-radius:14px;overflow:hidden;border:1px solid var(--sa-line,#E3E1DA)}.nlcp-surr__map img{display:block;width:100%;height:auto}.nlcp-surr__map span{position:absolute;bottom:10px;inset-inline-start:10px;background:var(--sa-sea,#2F6F86);color:#fff;font-size:12.5px;font-weight:700;padding:6px 12px;border-radius:999px}.nlcp-surr__tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.nlcp-surr .nlcp-tile b{font-size:15px;line-height:1.3}@media(max-width:800px){.nlcp-surr__grid{grid-template-columns:1fr}}</style>';
		return $h;
	}
}
