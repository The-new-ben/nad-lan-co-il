<?php
/**
 * nadlan-config - First-person interior view (v1.69.84)
 *
 * The owner's repeated ask, delivered practically: a walk-inside view of an
 * apartment generated ENTIRELY from real unit data (rooms, sqm, mamad, balcony,
 * direction) - no GLB, no materials required, works for every listing/unit.
 * Pure CSS-3D (perspective + transformed wall planes) + vanilla JS:
 *   - eye-height camera inside the room, drag / touch-drag to look around
 *   - door hotspots walk between rooms (salon → kitchen → bedrooms → mamad → balcony)
 *   - window light placed on the compass wall matching the unit's direction meta
 *   - honest "הדמיה סכמטית" label; upgraded automatically when a contractor feeds
 *     real assets later (tour_url via media.php takes precedence upstream)
 *
 * Shared surface: [nadlan_interior_fp] shortcode + nadlan_interior_fp_html()
 * used by listings (property-showroom plan view) and projects (unit selector).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ifp_rooms' ) ) {
	/**
	 * Build the room list from real meta. Every room: key, label, w (meters), d, window wall.
	 */
	function nadlan_ifp_rooms( $rooms_count, $size_sqm, $has_mamad, $balcony_sqm, $direction ) {
		$rooms_count = max( 1, min( 8, (float) $rooms_count ) );
		$size_sqm    = max( 30, (int) $size_sqm ?: 85 );
		$bedrooms    = max( 0, (int) ceil( $rooms_count ) - 1 );
		// crude but honest area split: salon 40%, kitchen 12%, each bedroom shares the rest
		$salon_a = $size_sqm * 0.40;
		$bed_a   = $bedrooms ? ( $size_sqm * 0.42 ) / $bedrooms : 0;
		$dir_wall = 'n';
		$d = (string) $direction;
		if ( mb_strpos( $d, 'דרום' ) !== false ) { $dir_wall = 's'; }
		elseif ( mb_strpos( $d, 'מזרח' ) !== false ) { $dir_wall = 'e'; }
		elseif ( mb_strpos( $d, 'מערב' ) !== false ) { $dir_wall = 'w'; }
		$out = array();
		$out[] = array( 'key' => 'salon', 'label' => 'סלון ופינת אוכל', 'w' => round( sqrt( $salon_a * 1.4 ), 1 ), 'd' => round( sqrt( $salon_a / 1.4 ), 1 ), 'win' => $dir_wall );
		$out[] = array( 'key' => 'kitchen', 'label' => 'מטבח', 'w' => 3.4, 'd' => round( max( 2.4, $size_sqm * 0.12 / 3.4 ), 1 ), 'win' => 'n' );
		for ( $i = 1; $i <= $bedrooms; $i++ ) {
			$is_mamad = ( $has_mamad && $i === $bedrooms );
			$out[] = array( 'key' => 'bed' . $i, 'label' => $is_mamad ? 'ממ״ד' : ( 1 === $i ? 'חדר שינה הורים' : 'חדר שינה ' . $i ), 'w' => round( sqrt( $bed_a * 1.15 ), 1 ), 'd' => round( sqrt( $bed_a / 1.15 ), 1 ), 'win' => $is_mamad ? '' : ( 'n' === $dir_wall ? 'e' : $dir_wall ), 'mamad' => $is_mamad );
		}
		if ( (int) $balcony_sqm > 0 ) {
			$out[] = array( 'key' => 'balcony', 'label' => 'מרפסת (' . (int) $balcony_sqm . ' מ״ר)', 'w' => round( sqrt( $balcony_sqm * 2.2 ), 1 ), 'd' => round( sqrt( $balcony_sqm / 2.2 ), 1 ), 'win' => 'open' );
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_interior_fp_html' ) ) {
	function nadlan_interior_fp_html( $args ) {
		$rooms = nadlan_ifp_rooms(
			$args['rooms'] ?? 4, $args['size_sqm'] ?? 0,
			! empty( $args['protected_room'] ), $args['balcony_sqm'] ?? 0,
			$args['direction'] ?? ''
		);
		$uid  = 'nlifp-' . wp_unique_id();
		$html = '<div class="nlifp" id="' . esc_attr( $uid ) . '" data-rooms="' . esc_attr( wp_json_encode( $rooms ) ) . '">'
			. '<div class="nlifp-stage" tabindex="0" role="application" aria-label="סיור פנימי בדירה - גררו כדי להביט סביב">'
			. '<div class="nlifp-cam"><div class="nlifp-world"></div></div>'
			. '<div class="nlifp-hud"><span class="nlifp-room"></span><span class="nlifp-hint">גררו להסתכל · לחצו על דלת למעבר חדר</span></div>'
			. '<span class="nlifp-tag">הדמיה סכמטית להמחשה - נוצרה מנתוני הדירה</span>'
			. '</div>'
			. '<div class="nlifp-doors"></div>'
			. '</div>';
		return nadlan_ifp_assets_html() . $html;
	}
}

if ( ! function_exists( 'nadlan_ifp_assets_html' ) ) {
	/** The FP walkthrough CSS+JS, printed once per request. Reused by the
	 *  showroom engine (unit panel walk-inside) via wp_footer. */
	function nadlan_ifp_assets_html() {
		static $done_assets = false;
		if ( $done_assets ) { return ''; }
		$done_assets = true;
		ob_start(); ?>
<style>
.nlifp{margin:10px 0}
.nlifp-stage{position:relative;height:340px;border-radius:12px;border:1px solid #E2DCD0;overflow:hidden;background:#141310;perspective:520px;cursor:grab;touch-action:pan-y;outline-offset:2px}
.nlifp-stage:active{cursor:grabbing}
.nlifp-cam{position:absolute;inset:0;transform-style:preserve-3d}
.nlifp-world{position:absolute;left:50%;top:52%;transform-style:preserve-3d}
.nlifp-face{position:absolute;transform-style:preserve-3d;background:#F5F1E8;border:1.5px solid #2E2B26;box-sizing:border-box}
.nlifp-face .nlifp-skirt{position:absolute;bottom:0;left:0;right:0;height:7%;background:#E9E2D2;border-top:1.5px solid #2E2B26}
.nlifp-floor{background:repeating-linear-gradient(90deg,#EAE3D3 0 60px,#E2D9C6 60px 62px)}
.nlifp-ceil{background:#FBF9F4}
.nlifp-win{position:absolute;top:18%;left:22%;width:56%;height:48%;background:linear-gradient(180deg,#DCE9EE 0%,#EDF3F0 55%,#F2EEDC 100%);border:2.5px solid #2E2B26;box-shadow:inset 0 0 0 3px #F5F1E8, inset 0 0 40px rgba(255,246,214,.9)}
.nlifp-win::after{content:"";position:absolute;inset:0;border-inline-start:2px solid #2E2B26;left:50%}
.nlifp-door{position:absolute;bottom:0;width:26%;height:78%;left:37%;background:#2E2B26;border-radius:3px 3px 0 0;cursor:pointer;display:flex;align-items:flex-end;justify-content:center;padding-bottom:10px;color:#E6D4AE;font:700 11px/1.3 Heebo,sans-serif;text-align:center;transition:background .2s}
.nlifp-door:hover{background:#4A443A}
.nlifp-door small{pointer-events:none}
.nlifp-hud{position:absolute;top:10px;inset-inline-start:10px;display:flex;flex-direction:column;gap:3px;pointer-events:none}
.nlifp-room{background:rgba(27,26,23,.88);color:#FAF8F3;font:700 13px/1 Heebo,sans-serif;border-radius:7px;padding:7px 12px;width:max-content}
.nlifp-hint{background:rgba(27,26,23,.6);color:#D8D2C4;font:400 10.5px/1 Heebo,sans-serif;border-radius:6px;padding:5px 9px;width:max-content}
.nlifp-tag{position:absolute;bottom:8px;inset-inline-end:10px;font:400 10px/1 Heebo,sans-serif;color:#B7AE9E;pointer-events:none}
.nlifp-doors{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.nlifp-doors button{font:600 12px/1 Heebo,sans-serif;border:1px solid #E2DCD0;background:#FFFDFC;color:#1B1A17;border-radius:999px;padding:8px 13px;cursor:pointer;min-height:34px}
.nlifp-doors button.is-on{background:#1B1A17;color:#fff;border-color:#1B1A17}
</style>
<script>
(function(){
function initFP(root){
	if(root._fp){return}root._fp=1;
	var rooms=JSON.parse(root.dataset.rooms||"[]"),world=root.querySelector(".nlifp-world"),
		stage=root.querySelector(".nlifp-stage"),hud=root.querySelector(".nlifp-room"),
		bar=root.querySelector(".nlifp-doors"),cur=0,yaw=0,pitch=0,SC=120; /* 1m = 120px */
	function build(i){
		cur=i;var r=rooms[i];if(!r){return}
		var W=r.w*SC,D=r.d*SC,H=2.65*SC;yaw=0;pitch=0;
		world.innerHTML="";
		function face(w,h,tf,cls){var e=document.createElement("div");e.className="nlifp-face "+(cls||"");e.style.width=w+"px";e.style.height=h+"px";e.style.transform="translate(-50%,-50%) "+tf;var sk=document.createElement("div");sk.className="nlifp-skirt";if(!cls){e.appendChild(sk)}return e}
		var walls=[
			{k:"n",el:face(W,H,"translateZ("+(-D/2)+"px)")},
			{k:"s",el:face(W,H,"rotateY(180deg) translateZ("+(-D/2)+"px)")},
			{k:"e",el:face(D,H,"rotateY(-90deg) translateZ("+(-W/2)+"px)")},
			{k:"w",el:face(D,H,"rotateY(90deg) translateZ("+(-W/2)+"px)")}
		];
		walls.forEach(function(wl){
			if(r.win===wl.k){var win=document.createElement("div");win.className="nlifp-win";wl.el.appendChild(win)}
			world.appendChild(wl.el);
		});
		if(r.win==="open"){walls.forEach(function(wl){if(wl.k==="n"){var win=document.createElement("div");win.className="nlifp-win";win.style.cssText+="top:8%;left:6%;width:88%;height:70%";wl.el.appendChild(win)}})}
		world.appendChild(face(W,D,"rotateX(90deg) translateZ("+(-H/2)+"px)","nlifp-floor"));
		world.appendChild(face(W,D,"rotateX(-90deg) translateZ("+(-H/2)+"px)","nlifp-ceil"));
		var nxt=rooms[(i+1)%rooms.length];
		if(rooms.length>1){var door=document.createElement("div");door.className="nlifp-door";door.innerHTML="<small>אל "+nxt.label+" ←</small>";door.addEventListener("click",function(ev){ev.stopPropagation();build((i+1)%rooms.length)});walls[1].el.appendChild(door)}
		hud.textContent=r.label+" · כ-"+Math.round(r.w*r.d)+' מ"ר';
		bar.querySelectorAll("button").forEach(function(b,bi){b.classList.toggle("is-on",bi===i)});
		apply();
	}
	function apply(){world.style.transform="rotateX("+pitch+"deg) rotateY("+yaw+"deg)"}
	var drag=null;
	stage.addEventListener("pointerdown",function(e){drag={x:e.clientX,y:e.clientY,yaw:yaw,pitch:pitch};stage.setPointerCapture(e.pointerId)});
	stage.addEventListener("pointermove",function(e){if(!drag){return}yaw=drag.yaw+(e.clientX-drag.x)*0.28;pitch=Math.max(-24,Math.min(18,drag.pitch-(e.clientY-drag.y)*0.14));apply()});
	stage.addEventListener("pointerup",function(){drag=null});
	stage.addEventListener("keydown",function(e){if(e.key==="ArrowLeft"){yaw-=8;apply()}if(e.key==="ArrowRight"){yaw+=8;apply()}});
	rooms.forEach(function(r,i){var b=document.createElement("button");b.type="button";b.textContent=r.label;b.addEventListener("click",function(){build(i)});bar.appendChild(b)});
	build(0);
	var spin=setInterval(function(){if(drag){return}yaw+=0.12;apply()},50);
	stage.addEventListener("pointerdown",function(){clearInterval(spin)},{once:true});
}
function scan(){document.querySelectorAll(".nlifp").forEach(initFP)}
if(document.readyState!=="loading"){scan()}else{document.addEventListener("DOMContentLoaded",scan)}
window.nadlanInitFP=scan;
})();
</script>
<?php
		return ob_get_clean();
	}
}

add_shortcode( 'nadlan_interior_fp', function ( $atts ) {
	$a = shortcode_atts( array( 'rooms' => 4, 'sqm' => 90, 'mamad' => 1, 'balcony' => 10, 'direction' => 'דרום' ), $atts );
	return nadlan_interior_fp_html( array(
		'rooms' => (float) $a['rooms'], 'size_sqm' => (int) $a['sqm'],
		'protected_room' => (bool) $a['mamad'], 'balcony_sqm' => (int) $a['balcony'], 'direction' => $a['direction'],
	) );
} );
