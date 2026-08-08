<?php
/**
 * [nl_matcher] - the project matcher: pick what matters in a few taps,
 * get ranked matches with an honest percentage.
 *
 * Owner spec (2026-08-07/08): practical intents FIRST (budget, rooms, city,
 * delivery), facilities second; minimum clicks, zero typing; material-rich
 * projects lead inside equal scores because they convert and their developers
 * are the paying side; every other project still appears by match probability;
 * results shareable (the URL hash records the selection). Benchmarks:
 * Apartment List's quiz flow, 1.5%->4.3% conversion via simplified journeys.
 *
 * Data: real meta only - price_min/max, city, completion_year,
 * project_3d_units (rooms), project_facilities (canonical keys), lat/lng,
 * project_model_glb. A criterion a project has no data for earns nothing:
 * the percentage stays honest.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_matcher_dataset' ) ) {
	function nadlan_matcher_dataset() {
		/* Do not reuse a pre-privacy aggregate: its rows may already contain a
		 * private-lab title, URL and matching signals. */
		$cached = get_transient( 'nl_matcher_v3_public' );
		if ( is_array( $cached ) ) {
			return $cached;
		}
		$public_meta = function_exists( 'nadlan_unit_journey_public_meta_query' )
			? nadlan_unit_journey_public_meta_query()
			: array(
				'relation' => 'OR',
				array( 'key' => '_nadlan_private_unit_journey', 'compare' => 'NOT EXISTS' ),
				array(
					'key'     => '_nadlan_private_unit_journey',
					'value'   => 'private-unit-journey-v2',
					'compare' => '!=',
				),
			);
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_project',
			'post_status'    => 'publish',
			'posts_per_page' => -1,
			'no_found_rows'  => true,
			'fields'         => 'ids',
			'meta_query'     => $public_meta,
			'nadlan_private_visibility_applied' => true,
		) );
		$rows   = array();
		$cities = array();
		foreach ( $q->posts as $id ) {
			$slug = (string) get_post_field( 'post_name', $id );
			if ( preg_match( '/-(en|fr|ru|ar)$/', $slug ) ) {
				continue;
			}
			$city = trim( (string) get_post_meta( $id, 'city', true ) );
			/* one city, one name: the imported rows say "תל אביב יפו" while the
			   flagship metas say "תל אביב" - unnormalized, the flagships lost
			   every city match (found live on the first matcher run) */
			$city_norm = array(
				'תל אביב יפו'  => 'תל אביב',
				'תל אביב-יפו'  => 'תל אביב',
				'פתח תקוה'     => 'פתח תקווה',
			);
			if ( isset( $city_norm[ $city ] ) ) {
				$city = $city_norm[ $city ];
			}
			$fac  = array();
			$fraw = (string) get_post_meta( $id, 'project_facilities', true );
			if ( '' !== $fraw && function_exists( 'nadlan_fc_canonical' ) ) {
				$fac = array_values( nadlan_fc_canonical( array_map( 'trim', explode( ',', $fraw ) ) ) );
			}
			$rooms = array();
			$units = (string) get_post_meta( $id, 'project_3d_units', true );
			if ( '' !== $units && '[]' !== $units ) {
				$uj = json_decode( $units, true );
				if ( is_array( $uj ) ) {
					foreach ( $uj as $u ) {
						if ( isset( $u['rooms'] ) && is_numeric( $u['rooms'] ) ) {
							$rooms[ (string) (int) $u['rooms'] ] = true;
						}
					}
				}
			}
			$pmin = (float) get_post_meta( $id, 'price_min', true );
			$pmax = (float) get_post_meta( $id, 'price_max', true );
			$year = (int) get_post_meta( $id, 'completion_year', true );
			$lat  = (float) get_post_meta( $id, 'lat', true );
			$lng  = (float) get_post_meta( $id, 'lng', true );
			$glb  = '' !== (string) get_post_meta( $id, 'project_model_glb', true );

			/* rows with no matchable signal at all would only dilute results */
			if ( '' === $city && ! $fac && ! $rooms && $pmin <= 0 && ! $glb ) {
				continue;
			}
			if ( '' !== $city ) {
				$cities[ $city ] = isset( $cities[ $city ] ) ? $cities[ $city ] + 1 : 1;
			}
			$rows[] = array(
				's' => $slug,
				'n' => html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ),
				'u' => get_permalink( $id ),
				'c' => $city,
				'f' => $fac,
				'r' => array_map( 'intval', array_keys( $rooms ) ),
				'p' => ( $pmin > 0 ? array( $pmin, $pmax > 0 ? $pmax : $pmin ) : null ),
				'y' => $year > 2000 ? $year : null,
				'g' => $glb ? 1 : 0,
				'll' => ( $lat && $lng ) ? array( round( $lat, 5 ), round( $lng, 5 ) ) : null,
			);
		}
		arsort( $cities );
		$out = array( 'rows' => $rows, 'cities' => array_slice( array_keys( $cities ), 0, 8 ) );
		set_transient( 'nl_matcher_v3_public', $out, HOUR_IN_SECONDS );
		return $out;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/matcher-data', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			return nadlan_matcher_dataset();
		},
	) );
} );

add_action( 'save_post_nadlan_project', function () {
	delete_transient( 'nl_matcher_v2' );
	delete_transient( 'nl_matcher_v3_public' );
} );

add_shortcode( 'nl_matcher', function () {
	$data   = nadlan_matcher_dataset();
	$cities = $data['cities'];

	ob_start();
	?>
<style>
.nlmx{margin:26px 0;padding:20px 18px;background:#1B1A17;color:#F6F1E6;border-radius:16px}
.nlmx h2{margin:0 0 4px;font-size:21px;color:#F6F1E6}
.nlmx .sub{margin:0 0 16px;font-size:13.5px;color:#B7AE9C}
.nlmx .grp{margin-bottom:13px}
.nlmx .grp b{display:block;font-size:12.5px;color:#D8C79A;margin-bottom:7px}
.nlmx .chips{display:flex;flex-wrap:wrap;gap:7px}
.nlmx .chips button{padding:8px 14px;border-radius:999px;border:1px solid #4A443B;background:transparent;
color:#EAE4D8;font:600 13px Heebo,system-ui,sans-serif;cursor:pointer}
.nlmx .chips button.on{background:#D8C79A;border-color:#D8C79A;color:#1B1A17}
.nlmx .act{display:flex;gap:10px;align-items:center;margin-top:16px;flex-wrap:wrap}
.nlmx .go{padding:11px 26px;border-radius:999px;border:0;background:#B85410;color:#fff;
font:700 15px Heebo,system-ui,sans-serif;cursor:pointer}
.nlmx .share{padding:10px 18px;border-radius:999px;border:1px solid #4A443B;background:transparent;
color:#EAE4D8;font:600 13px Heebo,sans-serif;cursor:pointer;display:none}
.nlmx .res{margin-top:18px;display:none}
.nlmx .res h3{font-size:16px;color:#F6F1E6;margin:0 0 10px}
.nlmx .cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.nlmx .card{display:block;background:#242219;border:1px solid #3A362E;border-radius:12px;
padding:13px 15px;text-decoration:none;color:#F6F1E6}
.nlmx .card:hover{border-color:#D8C79A}
.nlmx .card .pct{display:inline-block;background:#2E7D4F;color:#fff;border-radius:8px;
padding:2px 9px;font:800 13px Heebo,sans-serif;margin-bottom:6px}
.nlmx .card .pct.mid{background:#A9691B}
.nlmx .card b{display:block;font-size:14.5px;margin-bottom:3px}
.nlmx .card s{display:block;text-decoration:none;font-size:12px;color:#B7AE9C}
.nlmx .card .why{margin-top:6px;font-size:11.5px;color:#D8C79A;line-height:1.5}
.nlmx .empty{color:#B7AE9C;font-size:13.5px}
</style>
<section class="nlmx" id="nlmx">
<h2>איזו דירה אתם מחפשים?</h2>
<p class="sub">סמנו מה שחשוב לכם, בלי להקליד. נציג את הפרויקטים שהכי מתאימים לכם, עם אחוז התאמה אמיתי לפי הנתונים שיש לנו.</p>
<div class="grp" data-k="c"><b>איפה?</b><div class="chips">
<?php foreach ( $cities as $c ) : ?><button type="button" data-v="<?php echo esc_attr( $c ); ?>"><?php echo esc_html( $c ); ?></button><?php endforeach; ?>
</div></div>
<div class="grp" data-k="r"><b>כמה חדרים?</b><div class="chips">
<button type="button" data-v="2">2</button><button type="button" data-v="3">3</button>
<button type="button" data-v="4">4</button><button type="button" data-v="5">5 ומעלה</button>
</div></div>
<div class="grp" data-k="p"><b>תקציב</b><div class="chips">
<button type="button" data-v="0-3000000">עד 3 מיליון</button>
<button type="button" data-v="3000000-5000000">3 עד 5 מיליון</button>
<button type="button" data-v="5000000-10000000">5 עד 10 מיליון</button>
<button type="button" data-v="10000000-99000000">מעל 10 מיליון</button>
</div></div>
<div class="grp" data-k="y"><b>מתי נכנסים?</b><div class="chips">
<button type="button" data-v="2027">עד 2027</button><button type="button" data-v="2028">עד 2028</button>
<button type="button" data-v="2031">גם בעוד כמה שנים</button>
</div></div>
<div class="grp" data-k="f" data-multi="1"><b>מה חשוב שיהיה? (אפשר כמה)</b><div class="chips">
<button type="button" data-v="בריכה">בריכה</button><button type="button" data-v="ספא">ספא</button>
<button type="button" data-v="חדר כושר">חדר כושר</button><button type="button" data-v="קונסיירז'">קונסיירז'</button>
<button type="button" data-v="חניון">חניון</button><button type="button" data-v="ממ&quot;ד">ממ"ד</button>
<button type="button" data-v="אזורי ילדים">אזורי ילדים</button><button type="button" data-v="מסחר">מסחר למטה</button>
<button type="button" data-v="_sea">קרוב לים</button><button type="button" data-v="_3d">עם בחירת דירה בתלת ממד</button>
</div></div>
<div class="act">
<button type="button" class="go">הצגת ההתאמות שלי</button>
<button type="button" class="share">העתקת קישור לתוצאות</button>
</div>
<div class="res"><h3></h3><div class="cards"></div></div>
</section>
<script>
(function(){
'use strict';
var ROOT=document.getElementById('nlmx');if(!ROOT)return;
var DATA=null,SEL={c:[],r:[],p:[],y:[],f:[]};
function fetchData(cb){if(DATA){cb();return;}
fetch('<?php echo esc_url( rest_url( 'nadlan/v1/matcher-data' ) ); ?>').then(function(r){return r.json();})
.then(function(j){DATA=j;cb();}).catch(function(){});}
ROOT.querySelectorAll('.grp').forEach(function(g){
var k=g.getAttribute('data-k'),multi=g.getAttribute('data-multi');
g.querySelectorAll('button').forEach(function(b){
b.addEventListener('click',function(){
var v=b.getAttribute('data-v');
if(multi){var i=SEL[k].indexOf(v);if(i>-1){SEL[k].splice(i,1);b.classList.remove('on');}
else{SEL[k].push(v);b.classList.add('on');}}
else{var was=b.classList.contains('on');
g.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});
SEL[k]=[];if(!was){b.classList.add('on');SEL[k]=[v];}}
});});});
function score(row){
/* facilities carry 30 vs city 20: matching what the visitor EXPLICITLY
   asked to have must outrank merely being in the right city - on the
   first live run city-only compounds outranked full-match flagships */
var earned=0,possible=0,why=[];
if(SEL.c.length){possible+=20;if(row.c&&SEL.c.indexOf(row.c)>-1){earned+=20;why.push(row.c);}}
if(SEL.r.length){possible+=20;var want=parseInt(SEL.r[0],10);
if(row.r&&row.r.length){var hit=row.r.some(function(x){return want>=5?x>=5:x===want;});
if(hit){earned+=20;why.push(want+' חדרים');}}}
if(SEL.p.length){possible+=20;if(row.p){var pr=SEL.p[0].split('-'),lo=+pr[0],hi=+pr[1];
if(row.p[0]<=hi&&row.p[1]>=lo){earned+=20;why.push('בתקציב');}}}
if(SEL.y.length){possible+=10;if(row.y&&row.y<=parseInt(SEL.y[0],10)){earned+=10;why.push('אכלוס '+row.y);}}
if(SEL.f.length){var per=30/SEL.f.length;possible+=30;
SEL.f.forEach(function(f){
if(f==='_sea'){if(row.ll&&row.ll[1]<34.787&&row.ll[1]>34.76){earned+=per;why.push('קרוב לים');}}
else if(f==='_3d'){if(row.g){earned+=per;why.push('תלת ממד');}}
else if(row.f&&row.f.length){
var ok=row.f.some(function(x){return x.indexOf(f.replace('"',''))>-1||f.indexOf(x)>-1;});
if(ok){earned+=per;why.push(f);}}});}
if(!possible)return null;
var pct=Math.round(earned/possible*100);
var material=(row.g?40:0)+(row.f?row.f.length*3:0)+(row.p?5:0);
return{pct:pct,material:material,why:why,row:row};
}
function run(){
fetchData(function(){
var out=[];DATA.rows.forEach(function(r){var s=score(r);if(s&&s.pct>0)out.push(s);});
out.sort(function(a,b){return b.pct-a.pct||b.material-a.material;});
out=out.slice(0,12);
var res=ROOT.querySelector('.res'),cards=ROOT.querySelector('.cards'),h=ROOT.querySelector('.res h3');
res.style.display='block';cards.innerHTML='';
if(!out.length){h.textContent='';cards.innerHTML='<p class="empty">לא נמצאו התאמות לשילוב הזה. נסו להוריד קריטריון אחד.</p>';return;}
h.textContent='מצאנו '+out.length+' פרויקטים שמתאימים לכם';
out.forEach(function(s){
var a=document.createElement('a');a.className='card';a.href=s.row.u;
a.innerHTML='<span class="pct'+(s.pct<70?' mid':'')+'">'+s.pct+'% התאמה</span>'+
'<b></b><s></s><span class="why"></span>';
a.querySelector('b').textContent=s.row.n;
a.querySelector('s').textContent=s.row.c||'';
a.querySelector('.why').textContent=s.why.slice(0,4).join(' · ');
cards.appendChild(a);});
ROOT.querySelector('.share').style.display='inline-block';
var parts=[];Object.keys(SEL).forEach(function(k){if(SEL[k].length)parts.push(k+':'+SEL[k].join(','));});
try{history.replaceState(null,'','#m='+encodeURIComponent(parts.join('|')));}catch(e){}
res.scrollIntoView({behavior:'smooth',block:'nearest'});
});}
ROOT.querySelector('.go').addEventListener('click',run);
ROOT.querySelector('.share').addEventListener('click',function(){
var b=this;navigator.clipboard.writeText(location.href).then(function(){
b.textContent='הקישור הועתק!';setTimeout(function(){b.textContent='העתקת קישור לתוצאות';},2000);});});
if(location.hash.indexOf('#m=')===0){
try{var h=decodeURIComponent(location.hash.slice(3));
h.split('|').forEach(function(seg){var kv=seg.split(':'),k=kv[0],vs=kv[1].split(',');
vs.forEach(function(v){var g=ROOT.querySelector('.grp[data-k="'+k+'"]');if(!g)return;
g.querySelectorAll('button').forEach(function(b){if(b.getAttribute('data-v')===v)b.click();});});});
run();}catch(e){}}
})();
</script>
	<?php
	return ob_get_clean();
} );
