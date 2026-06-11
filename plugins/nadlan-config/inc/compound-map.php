<?php
/**
 * nadlan-config - compound 3D fly-over map.
 *
 * Renders a Mapbox GL JS district map for project compounds such as Sde Dov.
 * Ships dark behind nadlan_feature_compound_map.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cmpmap_enabled' ) ) {
	function nadlan_cmpmap_enabled() {
		return (bool) apply_filters( 'nadlan_cmpmap_enabled', get_option( 'nadlan_feature_compound_map', '0' ) === '1' );
	}
}

if ( ! function_exists( 'nadlan_cmpmap_token' ) ) {
	function nadlan_cmpmap_token() {
		return trim( (string) get_option( 'nadlan_mapbox_token', '' ) );
	}
}

if ( ! function_exists( 'nadlan_cmpmap_clamp_float' ) ) {
	function nadlan_cmpmap_clamp_float( $value, $default, $min, $max ) {
		if ( ! is_numeric( $value ) ) { return (float) $default; }
		$value = (float) $value;
		if ( $value < $min ) { return (float) $min; }
		if ( $value > $max ) { return (float) $max; }
		return $value;
	}
}

if ( ! function_exists( 'nadlan_cmpmap_attrs' ) ) {
	function nadlan_cmpmap_attrs( $atts ) {
		$term = is_tax( 'nadlan_compound' ) ? get_queried_object() : null;
		$default_compound = ( $term && ! empty( $term->slug ) ) ? $term->slug : 'sde-dov';
		$atts = shortcode_atts(
			array(
				'compound' => $default_compound,
				'lat'      => '32.1108',
				'lng'      => '34.7805',
				'zoom'     => '14.2',
				'pitch'    => '60',
				'bearing'  => '-20',
			),
			(array) $atts,
			'nadlan_compound_map'
		);
		return array(
			'compound' => sanitize_title( (string) $atts['compound'] ),
			'lat'      => nadlan_cmpmap_clamp_float( $atts['lat'], 32.1108, -90, 90 ),
			'lng'      => nadlan_cmpmap_clamp_float( $atts['lng'], 34.7805, -180, 180 ),
			'zoom'     => nadlan_cmpmap_clamp_float( $atts['zoom'], 14.2, 3, 19 ),
			'pitch'    => nadlan_cmpmap_clamp_float( $atts['pitch'], 60, 0, 85 ),
			'bearing'  => nadlan_cmpmap_clamp_float( $atts['bearing'], -20, -180, 180 ),
		);
	}
}

if ( ! function_exists( 'nadlan_cmpmap_project_pins' ) ) {
	function nadlan_cmpmap_project_pins( $compound_slug ) {
		$compound_slug = sanitize_title( (string) $compound_slug );
		if ( $compound_slug === '' || ! taxonomy_exists( 'nadlan_compound' ) ) { return array(); }
		$term = get_term_by( 'slug', $compound_slug, 'nadlan_compound' );
		if ( ! $term || is_wp_error( $term ) ) { return array(); }

		$q = new WP_Query(
			array(
				'post_type'      => 'nadlan_project',
				'post_status'    => 'publish',
				'posts_per_page' => 100,
				'no_found_rows'  => true,
				'fields'         => 'ids',
				'tax_query'      => array(
					array(
						'taxonomy' => 'nadlan_compound',
						'field'    => 'term_id',
						'terms'    => (int) $term->term_id,
					),
				),
				'meta_query'     => array(
					array( 'key' => 'lat', 'compare' => 'EXISTS' ),
					array( 'key' => 'lng', 'compare' => 'EXISTS' ),
				),
			)
		);

		$pins = array();
		foreach ( $q->posts as $pid ) {
			$lat = get_post_meta( $pid, 'lat', true );
			$lng = get_post_meta( $pid, 'lng', true );
			if ( ! is_numeric( $lat ) || ! is_numeric( $lng ) ) { continue; }
			$lat = (float) $lat;
			$lng = (float) $lng;
			if ( $lat < -90 || $lat > 90 || $lng < -180 || $lng > 180 ) { continue; }
			$status = (string) get_post_meta( $pid, 'project_status', true );
			if ( $status === '' ) { $status = (string) get_post_meta( $pid, 'status', true ); }
			$units = get_post_meta( $pid, 'num_units', true );
			$pins[] = array(
				'id'        => (int) $pid,
				'title'     => wp_strip_all_tags( get_the_title( $pid ) ),
				'lat'       => $lat,
				'lng'       => $lng,
				'permalink' => get_permalink( $pid ),
				'status'    => sanitize_text_field( $status ),
				'units'     => is_numeric( $units ) ? (int) $units : 0,
			);
		}
		wp_reset_postdata();
		return $pins;
	}
}

if ( ! function_exists( 'nadlan_cmpmap_needs_assets' ) ) {
	function nadlan_cmpmap_needs_assets() {
		if ( ! nadlan_cmpmap_enabled() || nadlan_cmpmap_token() === '' ) { return false; }
		if ( is_tax( 'nadlan_compound' ) ) { return true; }
		if ( is_singular() ) {
			$post = get_post();
			return $post && has_shortcode( (string) $post->post_content, 'nadlan_compound_map' );
		}
		return false;
	}
}

if ( ! function_exists( 'nadlan_cmpmap_enqueue_assets' ) ) {
	function nadlan_cmpmap_enqueue_assets() {
		if ( ! nadlan_cmpmap_enabled() || nadlan_cmpmap_token() === '' ) { return; }
		if ( wp_style_is( 'nadlan-compound-map', 'enqueued' ) ) { return; }

		wp_enqueue_style( 'mapbox-gl', 'https://api.mapbox.com/mapbox-gl-js/v3.14.0/mapbox-gl.css', array(), '3.14.0' );
		wp_register_style( 'nadlan-compound-map', '', array( 'mapbox-gl' ), '1.58.0' );
		wp_enqueue_style( 'nadlan-compound-map' );
		wp_add_inline_style( 'nadlan-compound-map', '.nlcmp{margin:28px calc(50% - 50vw) 34px;width:100vw;max-width:100vw;padding:0 14px;box-sizing:border-box;direction:rtl}.nlcmp-shell{position:relative;overflow:hidden;border:1px solid rgba(214,190,137,.46);border-radius:18px;background:#071919;color:#fff;box-shadow:0 26px 80px rgba(5,18,20,.22)}.nlcmp-head{position:absolute;z-index:3;top:18px;right:18px;left:18px;display:flex;justify-content:space-between;gap:14px;align-items:flex-start;pointer-events:none}.nlcmp-copy{max-width:460px;padding:14px 16px;border:1px solid rgba(231,217,183,.38);border-radius:14px;background:linear-gradient(135deg,rgba(7,25,25,.86),rgba(18,42,45,.62));box-shadow:0 18px 44px rgba(0,0,0,.28);backdrop-filter:blur(12px)}.nlcmp-eyebrow{display:block;font-size:12px;letter-spacing:.08em;color:#e7d9b7}.nlcmp-title{margin:.18em 0 .2em;font-family:Frank Ruhl Libre,Georgia,serif;font-size:clamp(25px,3vw,42px);font-weight:600;line-height:1.08;color:#fff}.nlcmp-sub{margin:0;color:#f4ead2;font-size:14px;line-height:1.55}.nlcmp-motion{pointer-events:auto;border:1px solid rgba(231,217,183,.48);border-radius:999px;padding:10px 14px;background:rgba(7,25,25,.72);color:#fff;cursor:pointer;font-weight:700}.nlcmp-map{height:clamp(430px,62vh,720px);min-height:420px}.nlcmp-map canvas{outline:none}.nlcmp-pin{display:flex;align-items:center;gap:7px;border:1px solid rgba(255,255,255,.58);border-radius:999px;padding:8px 10px;background:linear-gradient(135deg,#f7ebc9,#b99656);color:#14100a;box-shadow:0 10px 24px rgba(0,0,0,.22);font:700 13px/1.2 Heebo,Arial,sans-serif;cursor:pointer;transition:transform .16s ease,box-shadow .16s ease}.nlcmp-pin:hover,.nlcmp-pin.is-hover{transform:translateY(-3px);box-shadow:0 16px 34px rgba(0,0,0,.3)}.nlcmp-pin:focus-visible{outline:3px solid #fff;outline-offset:3px}.nlcmp-pin-dot{width:9px;height:9px;border-radius:99px;background:#071919;box-shadow:0 0 0 3px rgba(7,25,25,.12)}.nlcmp-popup{direction:rtl;text-align:right;min-width:210px;font-family:Heebo,Arial,sans-serif}.nlcmp-popup h3{margin:0 0 7px;font-size:17px;line-height:1.25;color:#17130c}.nlcmp-popup p{margin:0 0 10px;color:#4a4031;font-size:13px}.nlcmp-popup a{display:inline-flex;align-items:center;min-height:38px;padding:0 13px;border-radius:9px;background:#17130c;color:#fff;text-decoration:none;font-weight:700}.nlcmp-notice{margin:24px auto;padding:22px;border:1px solid #e4d6b7;border-radius:14px;background:#fffaf0;color:#30271a;text-align:center;max-width:760px}.nlcmp-note{position:absolute;left:16px;bottom:14px;z-index:3;padding:7px 10px;border-radius:999px;background:rgba(7,25,25,.72);color:#f4ead2;font-size:12px;pointer-events:none}@media(max-width:700px){.nlcmp{margin:18px calc(50% - 50vw);padding:0 10px}.nlcmp-head{position:relative;top:auto;right:auto;left:auto;padding:14px;background:#071919}.nlcmp-shell{border-radius:14px}.nlcmp-copy{max-width:none;padding:0;border:0;background:transparent;box-shadow:none;backdrop-filter:none}.nlcmp-motion{display:none}.nlcmp-map{height:430px;min-height:430px}.nlcmp-note{position:static;border-radius:0;background:#071919;padding:10px 14px}}' );

		wp_enqueue_script( 'mapbox-gl', 'https://api.mapbox.com/mapbox-gl-js/v3.14.0/mapbox-gl.js', array(), '3.14.0', true );
		wp_register_script( 'nadlan-compound-map', '', array( 'mapbox-gl' ), '1.58.0', true );
		wp_enqueue_script( 'nadlan-compound-map' );
		wp_add_inline_script( 'nadlan-compound-map', nadlan_cmpmap_inline_js() );
	}
}

add_action( 'wp_enqueue_scripts', function () {
	if ( nadlan_cmpmap_needs_assets() ) { nadlan_cmpmap_enqueue_assets(); }
} );

if ( ! function_exists( 'nadlan_cmpmap_inline_js' ) ) {
	function nadlan_cmpmap_inline_js() {
		return <<<'JS'
(function(){
	function parseConfig(wrap){
		var node=wrap.querySelector('.nlcmp-data');
		if(!node){return null;}
		try{return JSON.parse(node.textContent||'{}');}catch(e){return null;}
	}
	function text(v){return (v===undefined||v===null)?'':String(v);}
	function popupNode(pin){
		var box=document.createElement('div');box.className='nlcmp-popup';box.setAttribute('dir','rtl');
		var h=document.createElement('h3');h.textContent=text(pin.title);box.appendChild(h);
		var facts=[];
		if(pin.status){facts.push(pin.status);}
		if(pin.units){facts.push(new Intl.NumberFormat('he-IL').format(pin.units)+' יח"ד');}
		var p=document.createElement('p');p.textContent=facts.length?facts.join(' · '):'פרויקט במתחם';box.appendChild(p);
		var a=document.createElement('a');a.href=pin.permalink;a.textContent='לעמוד הפרויקט';box.appendChild(a);
		return box;
	}
	function addFallbackBuildings(map){
		if(!map.getSource('composite') || map.getLayer('nlcmp-3d-buildings')){return;}
		var layers=map.getStyle().layers||[];
		var label=null;
		for(var i=0;i<layers.length;i++){if(layers[i].type==='symbol'&&layers[i].layout&&layers[i].layout['text-field']){label=layers[i].id;break;}}
		try{
			map.addLayer({id:'nlcmp-3d-buildings',source:'composite','source-layer':'building',filter:['==','extrude','true'],type:'fill-extrusion',minzoom:14,paint:{'fill-extrusion-color':'#c9c0ad','fill-extrusion-height':['interpolate',['linear'],['zoom'],14,0,15.2,['coalesce',['get','height'],18]],'fill-extrusion-base':['interpolate',['linear'],['zoom'],14,0,15.2,['coalesce',['get','min_height'],0]],'fill-extrusion-opacity':0.62}},label||undefined);
		}catch(e){}
	}
	function initMap(wrap){
		if(wrap.dataset.ready==='1'){return;}
		wrap.dataset.ready='1';
		var cfg=parseConfig(wrap),mapEl=wrap.querySelector('.nlcmp-map');
		if(!cfg||!mapEl){return;}
		if(!window.mapboxgl){wrap.classList.add('is-error');mapEl.textContent='המפה תופעל בקרוב';return;}
		mapboxgl.accessToken=cfg.token;
		var paused=false,raf=0,map=null,loaded=false;
		function pause(){paused=true;if(raf){cancelAnimationFrame(raf);raf=0;}}
		function build(style){
			map=new mapboxgl.Map({container:mapEl,style:style,center:[cfg.lng,cfg.lat],zoom:11,pitch:0,bearing:0,antialias:true,cooperativeGestures:true});
			map.addControl(new mapboxgl.NavigationControl({visualizePitch:true}),'bottom-left');
			['mousedown','touchstart','wheel','dragstart','rotatestart','pitchstart','keydown'].forEach(function(ev){map.on(ev,pause);});
			map.on('error',function(){
				if(!loaded&&style.indexOf('/standard')!==-1){try{map.remove();}catch(e){} build('mapbox://styles/mapbox/streets-v12');}
			});
			map.on('load',function(){
				loaded=true;
				addFallbackBuildings(map);
				(cfg.pins||[]).forEach(function(pin){
					var el=document.createElement('button');el.type='button';el.className='nlcmp-pin';el.setAttribute('aria-label',text(pin.title));el.innerHTML='<span class="nlcmp-pin-dot" aria-hidden="true"></span><span></span>';el.lastChild.textContent=text(pin.title);
					var popup=new mapboxgl.Popup({offset:18,closeButton:true,maxWidth:'280px'}).setDOMContent(popupNode(pin));
					new mapboxgl.Marker({element:el,anchor:'bottom'}).setLngLat([pin.lng,pin.lat]).setPopup(popup).addTo(map);
					el.addEventListener('mouseenter',function(){el.classList.add('is-hover');});
					el.addEventListener('mouseleave',function(){el.classList.remove('is-hover');});
				});
				setTimeout(function(){if(paused){return;}map.flyTo({center:[cfg.lng,cfg.lat],zoom:cfg.zoom,pitch:cfg.pitch,bearing:cfg.bearing,duration:5200,essential:true});},450);
				setTimeout(function(){
					if(paused){return;}
					var started=null;
					function orbit(ts){
						if(paused){return;}
						if(started===null){started=ts;}
						var elapsed=(ts-started)%20000;
						map.setBearing(cfg.bearing+(elapsed/20000)*360);
						raf=requestAnimationFrame(orbit);
					}
					raf=requestAnimationFrame(orbit);
				},6100);
			});
		}
		build('mapbox://styles/mapbox/standard');
		var btn=wrap.querySelector('.nlcmp-motion');
		if(btn){btn.addEventListener('click',function(){paused=false;if(map){map.flyTo({center:[cfg.lng,cfg.lat],zoom:cfg.zoom,pitch:cfg.pitch,bearing:cfg.bearing,duration:3600,essential:true});}});}
	}
	function watch(wrap){
		if('IntersectionObserver' in window){
			var io=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){io.disconnect();initMap(wrap);}});},{rootMargin:'180px 0px'});
			io.observe(wrap);
		}else{initMap(wrap);}
	}
	document.querySelectorAll('.nlcmp[data-nlcmp]').forEach(watch);
})();
JS;
	}
}

if ( ! function_exists( 'nadlan_cmpmap_notice' ) ) {
	function nadlan_cmpmap_notice() {
		return '<div class="nlcmp-notice" dir="rtl" role="status"><strong>המפה תופעל בקרוב</strong><br><span>אנו מכינים את שכבת התלת-ממד של המתחם.</span></div>';
	}
}

if ( ! function_exists( 'nadlan_cmpmap_render' ) ) {
	function nadlan_cmpmap_render( $atts = array() ) {
		if ( ! nadlan_cmpmap_enabled() ) { return ''; }
		$cfg = nadlan_cmpmap_attrs( $atts );
		if ( nadlan_cmpmap_token() === '' ) { return nadlan_cmpmap_notice(); }
		nadlan_cmpmap_enqueue_assets();
		$pins = nadlan_cmpmap_project_pins( $cfg['compound'] );
		$id = 'nlcmp-' . wp_generate_uuid4();
		$data = array(
			'token'   => nadlan_cmpmap_token(),
			'lat'     => $cfg['lat'],
			'lng'     => $cfg['lng'],
			'zoom'    => $cfg['zoom'],
			'pitch'   => $cfg['pitch'],
			'bearing' => $cfg['bearing'],
			'pins'    => $pins,
		);
		$label = sprintf( 'מפת תלת-ממד של מתחם %s', $cfg['compound'] );
		ob_start(); ?>
<section class="nlcmp" data-nlcmp dir="rtl" aria-label="<?php echo esc_attr( $label ); ?>">
	<div class="nlcmp-shell">
		<div class="nlcmp-head">
			<div class="nlcmp-copy">
				<span class="nlcmp-eyebrow">מפת מתחם</span>
				<h2 class="nlcmp-title">רובע שדה דב ממבט רחפן</h2>
				<p class="nlcmp-sub">בחרו פרויקט על המפה, עברו לעמוד הפרויקט והשאירו פנייה ישירה.</p>
			</div>
			<button class="nlcmp-motion" type="button">הפעל תנועה</button>
		</div>
		<div id="<?php echo esc_attr( $id ); ?>" class="nlcmp-map" role="application" aria-label="<?php echo esc_attr( $label ); ?>" tabindex="0"></div>
		<p class="nlcmp-note">הדמיית מפה תלת-ממדית. נתוני פרויקטים מתעדכנים מתוך הכרטיסים באתר.</p>
		<script type="application/json" class="nlcmp-data"><?php echo wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT ); ?></script>
	</div>
</section>
		<?php
		return ob_get_clean();
	}
}

add_shortcode( 'nadlan_compound_map', 'nadlan_cmpmap_render' );

add_action( 'loop_start', function ( $query ) {
	static $printed = false;
	if ( $printed || ! nadlan_cmpmap_enabled() || is_admin() || ! $query->is_main_query() || ! is_tax( 'nadlan_compound' ) ) { return; }
	$term = get_queried_object();
	if ( ! $term || empty( $term->slug ) ) { return; }
	$printed = true;
	echo nadlan_cmpmap_render( array( 'compound' => $term->slug ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
}, 1 );

if ( ! function_exists( 'nadlan_cmpmap_largest_pins_count' ) ) {
	function nadlan_cmpmap_largest_pins_count() {
		if ( ! taxonomy_exists( 'nadlan_compound' ) ) { return 0; }
		$terms = get_terms( array( 'taxonomy' => 'nadlan_compound', 'hide_empty' => false ) );
		if ( is_wp_error( $terms ) || ! $terms ) { return 0; }
		$max = 0;
		foreach ( $terms as $term ) {
			$max = max( $max, count( nadlan_cmpmap_project_pins( $term->slug ) ) );
		}
		return (int) $max;
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['compound_map'] = array(
		'enabled'       => nadlan_cmpmap_enabled(),
		'token_present' => nadlan_cmpmap_token() !== '',
		'pins_count'    => nadlan_cmpmap_largest_pins_count(),
	);
	return $out;
} );
