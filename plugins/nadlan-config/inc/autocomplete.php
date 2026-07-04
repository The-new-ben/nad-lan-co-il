<?php
/**
 * nadlan-config - City / professional / project autocomplete (v1.15.0)
 *
 * Powers the city input across facets, saved-search, AVM tool, and NL search
 * with a single fast REST endpoint backed by a daily-cached city index.
 *
 * GET /nadlan/v1/suggest?q=&type=city|professional|project   → top 10 matches.
 * For 'city': aggregates the distinct city meta values across the 3 card CPTs
 * with their counts (so "תל אביב (1240)" appears).
 *
 * Cache: full index in a 24h transient; query just filters in-PHP.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cities_index' ) ) {
	function nadlan_cities_index( $force = false ) {
		$key = 'nadlan_cities_idx';
		$idx = $force ? null : get_transient( $key );
		if ( is_array( $idx ) ) { return $idx; }
		global $wpdb;
		$rows = $wpdb->get_results(
			"SELECT pm.meta_value city, COUNT(*) n
			 FROM {$wpdb->postmeta} pm INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id
			 WHERE pm.meta_key='city' AND pm.meta_value<>''
			 AND p.post_status='publish'
			 AND p.post_type IN ('nadlan_property','nadlan_project','nadlan_professional')
			 GROUP BY pm.meta_value ORDER BY n DESC LIMIT 5000", ARRAY_A );
		$idx = array();
		foreach ( (array) $rows as $r ) { $idx[] = array( 'name' => $r['city'], 'count' => (int) $r['n'] ); }
		set_transient( $key, $idx, DAY_IN_SECONDS );
		return $idx;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/suggest', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$q    = trim( (string) $req->get_param( 'q' ) );
			$type = sanitize_key( (string) $req->get_param( 'type' ) ) ?: 'city';
			$out  = array();
			if ( $type === 'city' ) {
				$idx = nadlan_cities_index();
				foreach ( $idx as $row ) {
					if ( $q === '' || mb_stripos( $row['name'], $q ) !== false ) {
						$out[] = $row;
						if ( count( $out ) >= 10 ) { break; }
					}
				}
			} else {
				$pt = array( 'professional' => 'nadlan_professional', 'project' => 'nadlan_project' )[ $type ] ?? '';
				if ( $pt && $q !== '' ) {
					$posts = get_posts( array( 'post_type' => $pt, 'posts_per_page' => 10, 's' => $q ) );
					foreach ( $posts as $p ) {
						$out[] = array( 'name' => get_the_title( $p ), 'url' => get_permalink( $p ) );
					}
				}
			}
			return new WP_REST_Response( array( 'ok' => true, 'items' => $out ), 200 );
		},
	) );
} );

/* Invalidate the city index when cards change */
add_action( 'save_post', function ( $post_id, $post ) {
	if ( in_array( ( $post->post_type ?? '' ), array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ), true ) ) {
		delete_transient( 'nadlan_cities_idx' );
	}
}, 99, 2 );

/* Auto-wire city autocomplete on every input[name="city"] sitewide */
add_action( 'wp_footer', function () {
	?>
<script>
(function(){
	function wire(inp){
		if(inp._nlAc)return;inp._nlAc=1;
		var box=document.createElement('div');box.className='nlac-box';inp.parentNode.style.position='relative';inp.parentNode.appendChild(box);
		var sel=-1;
		inp.addEventListener('input',function(){
			var q=inp.value.trim();box.innerHTML='';sel=-1;
			fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/suggest' ) ); ?>?type=city&q='+encodeURIComponent(q))
			.then(function(r){return r.json();}).then(function(j){
				if(!j.ok||!j.items.length){box.style.display='none';return;}
				box.style.display='block';
				j.items.forEach(function(it,i){
					var d=document.createElement('div');d.className='nlac-it';d.textContent=it.name+' ('+it.count+')';
					d.onclick=function(){inp.value=it.name;box.style.display='none';};
					box.appendChild(d);
				});
			});
		});
		inp.addEventListener('keydown',function(e){
			var its=box.querySelectorAll('.nlac-it');if(!its.length)return;
			if(e.key==='ArrowDown'){sel=(sel+1)%its.length;}
			else if(e.key==='ArrowUp'){sel=(sel-1+its.length)%its.length;}
			else if(e.key==='Enter'&&sel>=0){e.preventDefault();its[sel].click();return;}
			else{return;}
			its.forEach(function(d,i){d.classList.toggle('on',i===sel);});
		});
		inp.addEventListener('blur',function(){setTimeout(function(){box.style.display='none';},150);});
	}
	document.querySelectorAll('input[name="city"]').forEach(wire);
	// also wire dynamically added (after AJAX)
	new MutationObserver(function(ml){ml.forEach(function(m){m.addedNodes.forEach(function(n){
		if(n.nodeType===1){if(n.matches&&n.matches('input[name="city"]'))wire(n);n.querySelectorAll&&n.querySelectorAll('input[name="city"]').forEach(wire);}
	});});}).observe(document.body,{childList:true,subtree:true});
})();
</script>
<style>
.nlac-box{position:absolute;background:#fff;border:1px solid #ccc;border-radius:0 0 4px 4px;max-height:280px;overflow:auto;z-index:9999;min-width:200px;display:none;font-family:var(--font-sans,Heebo,sans-serif)}
.nlac-it{padding:8px 12px;cursor:pointer;font-size:14px;direction:rtl;text-align:right}
.nlac-it:hover,.nlac-it.on{background:#FAF7F1}
</style>
	<?php
} );
