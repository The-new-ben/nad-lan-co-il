<?php
/**
 * nadlan-config - URBAN RENEWAL HUB glue (L1, 2026-07-11).
 *
 * The /urban-renewal/ pillar and its spokes are CMS pages (edited via REST,
 * like every guide). This module ships only what pages cannot:
 *  1. GET /nadlan/v1/renewal-lookup - public compound lookup over the ~938
 *     gov.il urban-renewal compounds already imported as nadlan_project stubs
 *     (source=urban_renewal meta, import.php). Rate limited 30/hr/IP.
 *  2. [nadlan_ur_lookup] - the "is my building in a declared compound?"
 *     teaser embedded on the pillar. Works logged-out, honest miss copy.
 *  3. nadlan_ur_interlinks() - the hub URL map used by the spoke grid.
 *
 * Prefix law: inc/renewals.php is the BILLING module - everything urban
 * renewal uses urban-* files and nadlan_ur_/nlur prefixes.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ur_interlinks' ) ) {
	function nadlan_ur_interlinks() {
		return apply_filters( 'nadlan_ur_interlinks', array(
			'pillar'      => home_url( '/urban-renewal/' ),
			'tama38'      => home_url( '/urban-renewal/tama-38/' ),
			'pinui_binui' => home_url( '/urban-renewal/pinui-binui/' ),
			'check'       => home_url( '/urban-renewal/check/' ),
			'map'         => home_url( '/urban-renewal/map/' ),
			'glossary'    => home_url( '/glossary/' ),
			'pros'        => home_url( '/professionals/' ),
		) );
	}
}

if ( ! function_exists( 'nadlan_ur_lookup_rate_limited' ) ) {
	function nadlan_ur_lookup_rate_limited() {
		$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '0';
		$key = 'nadlan_ur_lk_' . md5( $ip );
		$n   = (int) get_transient( $key );
		if ( $n >= 30 ) { return true; }
		set_transient( $key, $n + 1, HOUR_IN_SECONDS );
		return false;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/renewal-lookup', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'args'                => array(
			'city' => array( 'type' => 'string', 'required' => false ),
			'q'    => array( 'type' => 'string', 'required' => false ),
		),
		'callback'            => function ( $req ) {
			if ( nadlan_ur_lookup_rate_limited() ) {
				return new WP_Error( 'rate_limited', 'too many lookups', array( 'status' => 429 ) );
			}
			$city = trim( sanitize_text_field( (string) $req->get_param( 'city' ) ) );
			$q    = trim( sanitize_text_field( (string) $req->get_param( 'q' ) ) );
			if ( '' === $city && '' === $q ) {
				return new WP_Error( 'bad_request', 'city or q required', array( 'status' => 400 ) );
			}
			$args = array(
				'post_type'      => 'nadlan_project',
				'post_status'    => 'publish',
				'posts_per_page' => 8,
				'no_found_rows'  => true,
				'meta_query'     => array( array( 'key' => 'source', 'value' => 'urban_renewal' ) ),
			);
			if ( '' !== $q ) { $args['s'] = $q; }
			if ( '' !== $city ) {
				$args['meta_query'][] = array( 'key' => 'city', 'value' => $city, 'compare' => 'LIKE' );
			}
			$out = array();
			foreach ( get_posts( $args ) as $p ) {
				$out[] = array(
					'title'          => get_the_title( $p ),
					'url'            => get_permalink( $p ),
					'city'           => (string) get_post_meta( $p->ID, 'city', true ),
					'plan_number'    => (string) get_post_meta( $p->ID, 'plan_number', true ),
					'project_status' => (string) get_post_meta( $p->ID, 'project_status', true ),
					'project_type'   => (string) get_post_meta( $p->ID, 'project_type', true ),
					'units_existing' => (int) get_post_meta( $p->ID, 'units_existing', true ),
					'units_added'    => (int) get_post_meta( $p->ID, 'units_added', true ),
				);
			}
			return array( 'found' => count( $out ) > 0, 'matches' => $out );
		},
	) );
} );

add_shortcode( 'nadlan_ur_lookup', function () {
	$rest = esc_url( rest_url( 'nadlan/v1/renewal-lookup' ) );
	ob_start(); ?>
<div class="nlur-lookup" dir="rtl">
	<h3 class="nlur-lookup__t">האם הבניין שלכם במתחם התחדשות מוכרז?</h3>
	<p class="nlur-lookup__s">בדיקה מול מאגר המתחמים הרשמי של הרשות הממשלתית להתחדשות עירונית (data.gov.il).</p>
	<form class="nlur-lookup__f" onsubmit="return false">
		<input type="text" id="nlur-city" placeholder="עיר" autocomplete="address-level2">
		<input type="text" id="nlur-q" placeholder="שם רחוב או מתחם (לא חובה)">
		<button type="button" id="nlur-go">בדיקה</button>
	</form>
	<div class="nlur-lookup__r" id="nlur-res" aria-live="polite"></div>
	<p class="nlur-lookup__n">המאגר כולל מתחמים מוכרזים בלבד. אם הבניין לא נמצא, ייתכן שעדיין יש פוטנציאל במסלול בניין בודד - זה לא אומר שאין אפשרות.</p>
</div>
<style>
.nlur-lookup{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:16px;padding:22px;margin:26px 0}
.nlur-lookup__t{font-family:"Frank Ruhl Libre",Georgia,serif;color:#1B1A17;margin:0 0 4px;font-size:1.25rem}
.nlur-lookup__s{color:#6D665C;font:400 13.5px/1.5 Heebo,sans-serif;margin:0 0 12px}
.nlur-lookup__f{display:flex;gap:8px;flex-wrap:wrap}
.nlur-lookup__f input{flex:1;min-width:140px;border:1px solid #E2DCD0;border-radius:10px;padding:12px 14px;font:400 14px Heebo,sans-serif;background:#fff}
.nlur-lookup__f button{background:#C2563A;color:#FAF7F1;border:0;border-radius:10px;padding:12px 22px;font:700 14px Heebo,sans-serif;cursor:pointer}
.nlur-lookup__f button:hover{filter:brightness(1.06)}
.nlur-lookup__r{margin-top:12px}
.nlur-hit{background:#fff;border:1px solid #E2DCD0;border-radius:10px;padding:12px 14px;margin-top:8px;font:400 13.5px/1.6 Heebo,sans-serif}
.nlur-hit b{color:#1B1A17}
.nlur-hit i{font-style:normal;color:#9C7A3C;font-weight:600}
.nlur-lookup__n{color:#8E877A;font:400 12px/1.5 Heebo,sans-serif;margin:12px 0 0}
</style>
<script>
(function(){
	var b=document.getElementById("nlur-go");if(!b)return;
	b.addEventListener("click",function(){
		var c=(document.getElementById("nlur-city").value||"").trim(),q=(document.getElementById("nlur-q").value||"").trim();
		var r=document.getElementById("nlur-res");
		if(!c&&!q){r.textContent="הזינו עיר או שם רחוב";return}
		r.textContent="בודקים מול המאגר...";
		fetch("<?php echo $rest; // phpcs:ignore ?>?city="+encodeURIComponent(c)+"&q="+encodeURIComponent(q))
			.then(function(x){return x.json()}).then(function(d){
				if(!d||!d.matches||!d.matches.length){r.innerHTML='<div class="nlur-hit">לא נמצא מתחם מוכרז תואם במאגר. זה לא אומר שאין פוטנציאל - מסלול בניין בודד לא מופיע במאגר המתחמים.</div>';return}
				r.innerHTML=d.matches.map(function(m){
					var t=m.project_type==="pinui_binui"?"פינוי בינוי":(m.project_type==="tama38"?"תמא 38":"התחדשות");
					return '<div class="nlur-hit"><b>'+m.title+'</b> · '+m.city+' · <i>'+t+'</i>'+(m.plan_number?' · תכנית '+m.plan_number:'')+(m.project_status?' · '+m.project_status:'')+(m.units_existing?' · '+m.units_existing+' יח׳ קיימות'+(m.units_added?" + "+m.units_added+" תוספת":""):'')+' · <a href="'+m.url+'">לעמוד המתחם</a></div>';
				}).join("");
			}).catch(function(){r.textContent="שגיאה זמנית, נסו שוב"});
	});
})();
</script>
	<?php
	return ob_get_clean();
} );
