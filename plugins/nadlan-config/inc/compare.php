<?php
/**
 * nadlan-config — Compare listings (v1.11.0)
 *
 * Zillow/Redfin-grade side-by-side comparison. Pure client-side state (localStorage
 * = no auth required) + a server-rendered comparison view via shortcode and a
 * dedicated /compare/ rewrite. JSON-LD for the comparison page is intentionally
 * omitted (low-value for search; this is a UX/conversion feature, not an SEO page).
 *
 * UX: a "Compare" button is added to property singles via inline JS that toggles
 * the listing into the tray; tray floats bottom-right with current selections.
 * Capped at 4 items.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---- Rewrite /compare/ ---- */
add_action( 'init', function () {
	add_rewrite_rule( '^compare/?$', 'index.php?nadlan_compare=1', 'top' );
	add_rewrite_tag( '%nadlan_compare%', '1' );
} );

/* ---- REST: render comparison table for given ids (server-side so JSON-LD + meta land cleanly) ---- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/compare', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$ids = array_slice( array_filter( array_map( 'intval', explode( ',', (string) $req->get_param( 'ids' ) ) ) ), 0, 4 );
			$rows = array();
			foreach ( $ids as $id ) {
				if ( get_post_type( $id ) !== 'nadlan_property' ) { continue; }
				$rows[] = array(
					'id' => $id, 'title' => get_the_title( $id ), 'url' => get_permalink( $id ),
					'thumb' => get_the_post_thumbnail_url( $id, 'medium' ),
					'price' => (int) get_post_meta( $id, 'price', true ),
					'rooms' => (float) get_post_meta( $id, 'rooms', true ),
					'sqm'   => (int) get_post_meta( $id, 'size_sqm', true ),
					'floor' => (int) get_post_meta( $id, 'floor', true ),
					'city'  => (string) get_post_meta( $id, 'city', true ),
					'elevator' => (bool) get_post_meta( $id, 'elevator', true ),
					'parking'  => (bool) get_post_meta( $id, 'parking', true ),
					'protected_room' => (bool) get_post_meta( $id, 'protected_room', true ),
					'price_per_sqm'  => ( (int) get_post_meta( $id, 'size_sqm', true ) > 0 )
						? (int) round( (float) get_post_meta( $id, 'price', true ) / (int) get_post_meta( $id, 'size_sqm', true ) ) : 0,
				);
			}
			return new WP_REST_Response( array( 'ok' => true, 'items' => $rows ), 200 );
		},
	) );
} );

/* ---- Compare page render ---- */
add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_compare' ) ) { return; }
	get_header();
	if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); } ?>
<div class="nlcmp" dir="rtl"><h1>השוואת נכסים</h1><div class="nlcmp-empty">בחרו עד 4 נכסים מדף הנכס כדי להוסיף להשוואה.</div><div class="nlcmp-mount"></div></div>
<script>
function nlcmpEsc(x){var d=document.createElement('div');d.textContent=String(x==null?'':x);return d.innerHTML;}
(function(){
	var ids=JSON.parse(localStorage.getItem('nadlan_compare')||'[]');
	if(!ids.length){return;}
	fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/compare' ) ); ?>?ids='+ids.join(','))
	.then(function(r){return r.json();}).then(function(j){
		if(!j.ok||!j.items.length){return;}
		document.querySelector('.nlcmp-empty').style.display='none';
		var rows=[
			['','title','thumb','price','price_per_sqm','rooms','sqm','floor','city','elevator','parking','protected_room'],
			['','כותרת','תמונה','מחיר','₪ למ"ר','חדרים','מ"ר','קומה','עיר','מעלית','חניה','ממ"ד'],
		];
		var h='<table class="nlcmp-tbl"><thead><tr><th></th>';
		j.items.forEach(function(i){h+='<th><a href="'+i.url+'">'+nlcmpEsc(i.title)+'</a></th>';});
		h+='</tr></thead><tbody>';
		for(var k=2;k<rows[0].length;k++){
			h+='<tr><th>'+rows[1][k]+'</th>';
			j.items.forEach(function(i){
				var v=i[rows[0][k]];
				if(rows[0][k]==='thumb'){v=v?'<img src="'+v+'" alt="">':'-';}
				else if(rows[0][k]==='price'||rows[0][k]==='price_per_sqm'){v=v?'₪'+v.toLocaleString():'-';}
				else if(typeof v==='boolean'){v=v?'✓':'—';}
				else if(!v){v='—';}
				h+='<td>'+v+'</td>';
			});
			h+='</tr>';
		}
		h+='</tbody></table>';
		document.querySelector('.nlcmp-mount').innerHTML=h;
	});
})();
</script>
<style>
.nlcmp{max-width:1100px;margin:0 auto;padding:24px;font-family:var(--font-sans,Heebo,sans-serif)}
.nlcmp-tbl{width:100%;border-collapse:collapse;margin-top:18px}
.nlcmp-tbl th,.nlcmp-tbl td{padding:10px;border-bottom:1px solid rgba(27,26,23,.1);text-align:right;vertical-align:top}
.nlcmp-tbl thead th{font-weight:600}
.nlcmp-tbl img{max-width:140px;border-radius:4px}
</style>
	<?php
	if ( function_exists( 'block_template_part' ) ) { block_template_part( 'footer' ); }
	get_footer(); exit;
}, 6 );

/* ---- Compare button + floating tray on property singles ---- */
add_action( 'wp_footer', function () {
	if ( ! is_singular( 'nadlan_property' ) ) { return; }
	$id = get_the_ID(); ?>
<div id="nladd-cmp"><button type="button" onclick="nadlanCmpToggle(<?php echo (int) $id; ?>,this)">+ הוסף להשוואה</button></div>
<div id="nltray"></div>
<style>
#nladd-cmp{margin:14px 0}
#nladd-cmp button{padding:9px 16px;background:#fff;border:1px solid #1B1A17;color:#1B1A17;border-radius:4px;cursor:pointer;font:inherit}
#nladd-cmp button.on{background:#1B1A17;color:#FAF7F1}
#nltray{position:fixed;bottom:14px;inset-inline-end:14px;background:#1B1A17;color:#FAF7F1;border-radius:8px;padding:10px 14px;font:14px/1.4 var(--font-sans,Heebo,sans-serif);box-shadow:0 6px 24px rgba(0,0,0,.2);display:none;z-index:9500}
#nltray a{color:#9C7A3C;font-weight:600;margin-inline-start:8px}
</style>
<script>
function nadlanCmpRefresh(){
	var ids=JSON.parse(localStorage.getItem('nadlan_compare')||'[]');
	var t=document.getElementById('nltray');
	if(!ids.length){t.style.display='none';return;}
	t.style.display='block';
	t.innerHTML=ids.length+' להשוואה <a href="/compare/">צפו בהשוואה</a> <button onclick="localStorage.removeItem(\'nadlan_compare\');nadlanCmpRefresh();" style="background:transparent;color:#FAF7F1;border:0;cursor:pointer">×</button>';
}
function nadlanCmpToggle(id,btn){
	var ids=JSON.parse(localStorage.getItem('nadlan_compare')||'[]');
	var i=ids.indexOf(id);
	if(i>=0){ids.splice(i,1);btn.classList.remove('on');btn.textContent='+ הוסף להשוואה';}
	else if(ids.length>=4){alert('עד 4 נכסים להשוואה.');return;}
	else{ids.push(id);btn.classList.add('on');btn.textContent='✓ בהשוואה';}
	localStorage.setItem('nadlan_compare',JSON.stringify(ids));
	nadlanCmpRefresh();
}
(function(){
	var ids=JSON.parse(localStorage.getItem('nadlan_compare')||'[]');
	if(ids.indexOf(<?php echo (int) $id; ?>)>=0){var b=document.querySelector('#nladd-cmp button');if(b){b.classList.add('on');b.textContent='✓ בהשוואה';}}
	nadlanCmpRefresh();
})();
</script>
	<?php
} );
