<?php
/* x-aurelia-experience v1.0 - Aurelia Sde Dov flagship layer (post {{POST_ID}}).
 * Additive around the shared showroom engine; engine.js untouched.
 * Adds: geometric unit selection (surface tap + projected hotspots with
 * occlusion), unit price row in the panel, per-unit 360 interior tour route,
 * compact mobile card guarantees, i18n text overrides. */

if ( ! defined( 'NADLAN_AURELIA_POST' ) ) {
	define( 'NADLAN_AURELIA_POST', {{POST_ID}} );
}

if ( ! function_exists( 'nadlan_aurelia_is_page' ) ) {
	function nadlan_aurelia_is_page() {
		return is_singular( 'nadlan_project' ) && NADLAN_AURELIA_POST === (int) get_queried_object_id();
	}
}

/* body class hook for scoped CSS */
if ( ! function_exists( 'nadlan_aurelia_body_class' ) ) {
	function nadlan_aurelia_body_class( $classes ) {
		if ( nadlan_aurelia_is_page() ) { $classes[] = 'nl-aurelia'; }
		return $classes;
	}
	add_filter( 'body_class', 'nadlan_aurelia_body_class' );
}

/* front assets: selection adapter + price row + i18n overrides, inline on the engine handle */
if ( ! function_exists( 'nadlan_aurelia_assets' ) ) {
	function nadlan_aurelia_assets() {
		if ( ! nadlan_aurelia_is_page() || ! wp_script_is( 'nadlan-engine-core', 'enqueued' ) ) { return; }

		$css = '
body.nl-aurelia .nl-hot{opacity:0;pointer-events:none}
body.nl-aurelia .nlaur-overlay{position:absolute;inset:0;z-index:6;overflow:hidden;pointer-events:none}
body.nl-aurelia .nlaur-dot{position:absolute;width:44px;height:44px;padding:0;transform:translate(-50%,-50%);border:1px solid rgba(202,164,94,.75);border-radius:50%;background:rgba(20,21,18,.92);color:#fff;font:700 12px/1 system-ui,sans-serif;pointer-events:auto;cursor:pointer}
body.nl-aurelia .nlaur-dot.is-active{background:#e7c284;color:#171510}
body.nl-aurelia .nlaur-dot:focus-visible{outline:3px solid #f1c879;outline-offset:3px}
body.nl-aurelia .nlaur-dot[hidden]{display:none}
body.nl-aurelia .nl-aurelia-unit-price{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:10px 0;padding:10px 12px;border:1px solid rgba(190,146,70,.34);border-radius:12px;background:linear-gradient(135deg,rgba(214,173,96,.13),rgba(255,255,255,.035));color:inherit}
body.nl-aurelia .nl-aurelia-unit-price-label{font-size:12px;opacity:.78}
body.nl-aurelia .nl-aurelia-unit-price-value{font-size:clamp(17px,2.2vw,24px);white-space:nowrap;font-variant-numeric:tabular-nums}
@media (max-width:680px){
 body.nl-aurelia .nl-aurelia-unit-price{margin:7px 0;padding:8px 10px}
 body.nl-aurelia .nlaur-dot{width:48px;height:48px}
}
@media (prefers-reduced-motion:reduce){body.nl-aurelia .nlaur-dot{transition:none}}';
		wp_add_inline_style( 'nadlan-engine-css', $css );

		$units_json = (string) get_post_meta( NADLAN_AURELIA_POST, 'project_3d_units', true );
		if ( '' === $units_json ) { return; }

		$i18n = array(
			'he' => array( 'price_nonbinding' => 'מחיר הדירה', 'price_title' => 'מחירים באורליה שדה דב', 'price_pending' => 'המחיר המלא של כל דירה מוצג בכרטיס שלה.', 'comps_pending' => 'המחירים מוצגים לפי הדירה שנבחרה.', 'model_error' => 'עברו לתצוגת החזית והמשיכו לבחור דירה.', 'winview_note' => 'גררו להביט סביב; הגובה והכיוון מתעדכנים לפי הדירה שנבחרה.', 'dtour_tag' => 'סיור בדירת אורליה', 'dtour_tag_units' => 'פנים הדירות בפרויקט', 'nlst_honest' => 'תרשים הדירה לפי מידותיה וחלוקתה.' ),
			'en' => array( 'price_nonbinding' => 'Residence price', 'price_title' => 'Aurelia Sde Dov prices', 'price_pending' => 'Each residence shows its full price on its card.', 'comps_pending' => 'Prices follow the selected residence.', 'model_error' => 'Switch to the elevation view and continue choosing.', 'winview_note' => 'Drag to look around; height and orientation follow the selected residence.', 'dtour_tag' => 'Aurelia residence tour', 'dtour_tag_units' => 'Project residence interiors', 'nlst_honest' => 'Residence diagram based on its dimensions and layout.' ),
			'fr' => array( 'price_nonbinding' => 'Prix de l’appartement', 'price_title' => 'Prix à Aurelia Sde Dov' ),
			'ru' => array( 'price_nonbinding' => 'Цена квартиры', 'price_title' => 'Цены в Aurelia Sde Dov' ),
			'ar' => array( 'price_nonbinding' => 'سعر الشقة', 'price_title' => 'الأسعار في أوريليا سديه دوف' ),
		);

		$boot = '(function(){"use strict";'
		. 'var IO=' . wp_json_encode( $i18n, JSON_UNESCAPED_UNICODE ) . ';'
		. 'function mergeI18n(){var W=window.NADLAN_I18N;if(!W||!W.langs){return;}Object.keys(IO).forEach(function(l){W.langs[l]=Object.assign({},W.langs[l]||{},IO[l]);});}'
		. 'mergeI18n();'
		. 'var FH=3.05,HALF=FH/2,MAXD=6.4,MINDOT=0.34;'
		. 'function project(){var sr=window.NADLAN_SHOWROOM;if(!sr||!sr.projects){return null;}if(Array.isArray(sr.projects)){return sr.projects[0]||null;}return sr.projects["aurelia"]||Object.values(sr.projects)[0]||null;}'
		. 'function vec(s){var a=String(s||"").trim().split(/\s+/).map(Number);return a.length===3&&a.every(isFinite)?a:null;}'
		. 'function anchors(units){var out=[];units.forEach(function(u){var p=vec(u.hotspot_position),n=vec(u.hotspot_normal||"0 0 1");if(!p||!n){return;}out.push({u:u,p:p,n:n,minY:p[1]-HALF-0.2,maxY:p[1]+HALF+0.2});});return out;}'
		. 'function trigger(id){var root=document.getElementById("nl-root");if(!root){return;}var b=document.createElement("button");b.setAttribute("data-act","select");b.setAttribute("data-id",id);b.style.cssText="position:absolute;left:-9999px;top:0";root.appendChild(b);b.click();setTimeout(function(){b.remove();},0);}'
		. 'var st={sel:null,frame:0,reps:[]};'
		. 'function pick(units,hit){if(!hit||!hit.position||!hit.normal){return null;}var best=null;anchors(units).forEach(function(a){var y=hit.position.y;if(y<a.minY||y>a.maxY){return;}var dot=hit.normal.x*a.n[0]+hit.normal.y*a.n[1]+hit.normal.z*a.n[2];if(dot<MINDOT){return;}var d=Math.hypot(hit.position.x-a.p[0],hit.position.y-a.p[1],hit.position.z-a.p[2]);if(d>MAXD){return;}var score=d+(1-dot)*2.4;if(!best||score<best.score){best={a:a,score:score,d:d,dot:dot};}});return best;}'
		. 'function reps(units){var av=units.filter(function(u){return u.status!=="sold";});var picks=[0,.2,.4,.6,.8,1].map(function(r){return av[Math.round((av.length-1)*r)];}).filter(Boolean);var sel=av.find(function(u){return u.id===st.sel;});var m=new Map();[sel].concat(picks).filter(Boolean).forEach(function(u){m.set(u.id,u);});return Array.from(m.values()).slice(0,6);}'
		. 'function boot(){var p=project();var model=document.querySelector("#nl-root model-viewer");if(!p||!model||!Array.isArray(p.units)||!p.units.length){return false;}'
		. 'var host=model.parentElement;if(!host){return false;}if(getComputedStyle(host).position==="static"){host.style.position="relative";}'
		. 'var overlay=host.querySelector(".nlaur-overlay");if(!overlay){overlay=document.createElement("div");overlay.className="nlaur-overlay";overlay.setAttribute("aria-label","דירות לבחירה על המודל");host.appendChild(overlay);}'
		. 'var units=p.units;var start=null;'
		. 'host.addEventListener("pointerdown",function(e){if(!e.isPrimary||e.button!==0||e.target.closest(".nlaur-dot")){return;}start={id:e.pointerId,x:e.clientX,y:e.clientY,t:performance.now()};},true);'
		. 'host.addEventListener("pointerup",function(e){var s=start;start=null;if(!s||s.id!==e.pointerId||e.target.closest(".nlaur-dot")){return;}if(Math.hypot(e.clientX-s.x,e.clientY-s.y)>6||performance.now()-s.t>900){return;}if(!model.positionAndNormalFromPoint){return;}var hit=model.positionAndNormalFromPoint(e.clientX,e.clientY);var m=pick(units,hit);if(!m){return;}st.sel=m.a.u.id;trigger(m.a.u.id);render();},true);'
		. 'function markers(){model.querySelectorAll(".nlaur-anchor").forEach(function(n){n.remove();});reps(units).forEach(function(u){var a=vec(u.hotspot_position);if(!a){return;}var mk=document.createElement("button");mk.className="nlaur-anchor";mk.slot="nlaur-"+u.id;mk.dataset.position=a.map(function(v){return v+"m";}).join(" ");mk.dataset.normal=String(u.hotspot_normal||"0 0 1");mk.dataset.unitId=u.id;mk.style.cssText="pointer-events:none;opacity:0.001";model.appendChild(mk);});}'
		. 'function render(){markers();overlay.textContent="";reps(units).forEach(function(u){var b=document.createElement("button");b.className="nlaur-dot"+(u.id===st.sel?" is-active":"");b.dataset.slot="nlaur-"+u.id;b.dataset.uid=u.id;b.setAttribute("aria-label",(u.label||u.id)+", קומה "+u.floor);b.textContent=u.floor;b.addEventListener("click",function(ev){ev.stopPropagation();st.sel=u.id;trigger(u.id);render();});overlay.appendChild(b);});place();}'
		. 'function place(){cancelAnimationFrame(st.frame);st.frame=requestAnimationFrame(function(){if(!model.queryHotspot){return;}var r=model.getBoundingClientRect();overlay.querySelectorAll(".nlaur-dot").forEach(function(b){var q=model.queryHotspot(b.dataset.slot);var pt=q&&q.canvasPosition;var inside=pt&&pt.x>=0&&pt.y>=0&&pt.x<=model.clientWidth&&pt.y<=model.clientHeight;var hit=inside&&model.positionAndNormalFromPoint?model.positionAndNormalFromPoint(r.left+pt.x,r.top+pt.y):null;var dl=hit&&q.position?Math.hypot(hit.position.x-q.position.x,hit.position.y-q.position.y,hit.position.z-q.position.z):Infinity;b.hidden=!q||!q.facingCamera||!inside||dl>4;if(!b.hidden){b.style.left=Math.max(22,Math.min(model.clientWidth-22,pt.x))+"px";b.style.top=Math.max(22,Math.min(model.clientHeight-22,pt.y))+"px";}});});}'
		. 'model.addEventListener("camera-change",place);model.addEventListener("load",function(){render();});window.addEventListener("resize",place,{passive:true});'
		. 'document.addEventListener("click",function(e){var t=e.target.closest("[data-act=select][data-id]");if(t&&!t.classList.contains("nlaur-tmp")){st.sel=t.getAttribute("data-id");render();}},true);'
		. 'render();return true;}'
		. 'function priceRow(){var body=document.querySelector("#nl-panel-body,.nl-panel__body,.nl-panel");if(!body){return;}var tr=body.querySelector("[data-act=rfp][data-id],[data-act=studio][data-id]");if(!tr){return;}var id=tr.getAttribute("data-id");var p=project();var u=p&&(p.units||[]).find(function(x){return String(x.id)===String(id);});var amount=u&&Number(u.price||0);var old=body.querySelector(".nl-aurelia-unit-price");if(!amount){if(old){old.remove();}return;}if(old&&old.getAttribute("data-unit-id")===String(id)){return;}if(old){old.remove();}var lang=(document.documentElement.lang||"he").slice(0,2);var W=window.NADLAN_I18N;var label=(W&&W.langs&&W.langs[lang]&&W.langs[lang].price_nonbinding)||"מחיר הדירה";var row=document.createElement("div");row.className="nl-aurelia-unit-price";row.setAttribute("data-unit-id",String(id));var lb=document.createElement("span");lb.className="nl-aurelia-unit-price-label";lb.textContent=label;var vl=document.createElement("strong");vl.className="nl-aurelia-unit-price-value";vl.textContent=new Intl.NumberFormat("he-IL",{maximumFractionDigits:0}).format(amount)+" ₪";row.appendChild(lb);row.appendChild(vl);var head=body.querySelector(".nl-panel__head");if(head){head.insertAdjacentElement("afterend",row);}else{body.insertBefore(row,body.firstChild);}}'
		. 'function watch(){var target=document.getElementById("nl-root");if(!target){return;}new MutationObserver(function(){window.requestAnimationFrame(priceRow);}).observe(target,{childList:true,subtree:true});priceRow();}'
		. 'var tries=0;(function retry(){if(boot()){watch();return;}if(++tries<40){setTimeout(retry,250);}})();'
		. '})();';
		wp_add_inline_script( 'nadlan-engine-core', $boot, 'after' );
	}
	add_action( 'wp_enqueue_scripts', 'nadlan_aurelia_assets', 10001 );
}

/* per-unit 360 interior tour: /projects/aurelia/?aurelia_tour=<unit_id>&lang=xx (noindex) */
if ( ! function_exists( 'nadlan_aurelia_tour' ) ) {
	function nadlan_aurelia_tour() {
		if ( empty( $_GET['aurelia_tour'] ) || NADLAN_AURELIA_POST !== (int) get_queried_object_id() ) { return; }
		$unit_id = sanitize_key( wp_unslash( $_GET['aurelia_tour'] ) );
		$units   = json_decode( (string) get_post_meta( NADLAN_AURELIA_POST, 'project_3d_units', true ), true );
		$unit    = array();
		foreach ( (array) $units as $c ) {
			if ( is_array( $c ) && isset( $c['id'] ) && $unit_id === sanitize_key( $c['id'] ) ) { $unit = $c; break; }
		}
		if ( ! $unit ) { status_header( 404 ); exit; }
		$lang = isset( $_GET['lang'] ) ? sanitize_key( wp_unslash( $_GET['lang'] ) ) : 'he';
		if ( ! in_array( $lang, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ) { $lang = 'he'; }
		$rtl  = in_array( $lang, array( 'he', 'ar' ), true );
		$copy = array(
			'he' => array( 'title' => 'סיור בדירת אורליה', 'drag' => 'גררו כדי להביט סביב', 'living' => 'חלל המגורים', 'living_d' => 'הסלון, פינת האוכל והמטבח יוצרים רצף אחד מול הים.', 'terrace' => 'מרפסת הים', 'terrace_d' => 'המרפסת ממשיכה את חלל האירוח מערבה אל הים והטיילת.', 'kitchen' => 'המטבח', 'kitchen_d' => 'אי עבודה רחב, אחסון מלא וקשר ישיר לפינת האוכל.', 'plan' => 'תוכנית הדירה', 'floor' => 'קומה', 'rooms' => 'חדרים', 'sqm' => 'שטח', 'balcony' => 'מרפסת', 'direction' => 'כיוון', 'back' => 'חזרה לבחירת הדירה', 'cta' => 'קבלו תוכניות ומחיר', 'left' => 'הביטו למרפסת', 'center' => 'חזרו לסלון', 'right' => 'הביטו למטבח' ),
			'en' => array( 'title' => 'Tour the Aurelia residence', 'drag' => 'Drag to look around', 'living' => 'Living space', 'living_d' => 'Living, dining and kitchen form one continuous space facing the sea.', 'terrace' => 'Sea terrace', 'terrace_d' => 'The terrace extends the entertaining space west toward the sea.', 'kitchen' => 'Kitchen', 'kitchen_d' => 'A generous island, full-height storage and a direct dining connection.', 'plan' => 'Residence plan', 'floor' => 'Floor', 'rooms' => 'Rooms', 'sqm' => 'Area', 'balcony' => 'Terrace', 'direction' => 'Orientation', 'back' => 'Back to residence selection', 'cta' => 'Get plans and price', 'left' => 'Look toward the terrace', 'center' => 'Return to the living room', 'right' => 'Look toward the kitchen' ),
		);
		$c = isset( $copy[ $lang ] ) ? $copy[ $lang ] : $copy['he'];
		$pano = '{{PANO_LIVING_URL}}';
		$plan = isset( $unit['plan'] ) ? esc_url_raw( (string) $unit['plan'] ) : '';
		$back = get_permalink( NADLAN_AURELIA_POST ) . '?unit=' . rawurlencode( $unit_id ) . '#nl-root';
		$floor = isset( $unit['floor'] ) ? (int) $unit['floor'] : 0;
		$rooms = isset( $unit['rooms'] ) ? (float) $unit['rooms'] : 0;
		$sqm   = isset( $unit['sqm'] ) ? (float) $unit['sqm'] : 0;
		$balc  = isset( $unit['balcony'] ) ? (float) $unit['balcony'] : 0;
		$dir   = isset( $unit['dir'] ) ? sanitize_text_field( (string) $unit['dir'] ) : '';
		nocache_headers();
		header( 'Content-Type: text/html; charset=' . get_bloginfo( 'charset' ) );
		header( 'X-Robots-Tag: noindex, nofollow', true );
		?><!doctype html>
<html lang="<?php echo esc_attr( $lang ); ?>" dir="<?php echo $rtl ? 'rtl' : 'ltr'; ?>">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex,nofollow">
<title><?php echo esc_html( $c['title'] . ' · ' . $unit_id ); ?></title>
<style>:root{color-scheme:dark;--gold:#d5a65b;--line:rgba(255,255,255,.18)}*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:#090908;color:#fff;font-family:Arial,sans-serif}body{overflow:hidden}.tour{min-height:100dvh;display:grid;grid-template-rows:auto 1fr auto}.bar{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:12px clamp(14px,3vw,34px);background:#0d0d0c;border-bottom:1px solid var(--line)}.brand b{font-size:clamp(15px,2vw,21px)}.brand span{display:block;font-size:12px;color:#c9c3b9}.back,.cta{min-height:44px;display:inline-flex;align-items:center;border-radius:999px;padding:0 16px;text-decoration:none;font-weight:700}.back{border:1px solid var(--line);color:#fff}.cta{background:var(--gold);color:#17120b}.stage{position:relative;overflow:hidden;touch-action:none;cursor:grab;background:#111}.pano{position:absolute;inset:-4%;background-image:url('<?php echo esc_url( $pano ); ?>');background-repeat:no-repeat;background-size:auto 108%;background-position:50% 50%;transition:background-position .55s cubic-bezier(.2,.8,.2,1)}.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.18),transparent 38%,rgba(0,0,0,.46));pointer-events:none}.hint{position:absolute;top:14px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,.62);border:1px solid var(--line);border-radius:999px;padding:9px 14px;font-size:13px;white-space:nowrap}.hs{position:absolute;left:var(--x);top:var(--y);width:46px;height:46px;transform:translate(-50%,-50%);border:2px solid #fff;border-radius:50%;background:var(--gold);color:#16120c;font-weight:900;box-shadow:0 0 0 8px rgba(213,166,91,.2);cursor:pointer}.hs[aria-pressed="true"]{box-shadow:0 0 0 12px rgba(213,166,91,.32)}.card{position:absolute;inset-inline-start:clamp(14px,3vw,34px);bottom:22px;width:min(390px,calc(100% - 28px));padding:16px;border:1px solid var(--line);border-radius:16px;background:rgba(16,16,14,.9);backdrop-filter:blur(12px)}.card h1{font-size:clamp(21px,3vw,30px);margin:0 0 7px}.card p{margin:0;color:#ddd4c5;line-height:1.5}.dock{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:12px clamp(14px,3vw,34px);background:#0d0d0c;border-top:1px solid var(--line)}.looks{display:flex;justify-content:center;gap:8px}.looks button,.planbtn{min-height:44px;border:1px solid var(--line);border-radius:999px;background:#171715;color:#fff;padding:0 14px;cursor:pointer}.planbtn{display:inline-flex;align-items:center;text-decoration:none}.looks button[aria-pressed="true"]{border-color:var(--gold);color:#f7cf8b}.facts{display:flex;gap:12px;flex-wrap:wrap;color:#cfc7bb;font-size:12px}.facts b{color:#fff}.plan{position:fixed;inset:0;z-index:20;display:none;place-items:center;padding:24px;background:rgba(0,0,0,.82)}.plan:target{display:grid}.planbox{position:relative;width:min(900px,96vw);max-height:88vh;padding:16px;border-radius:18px;background:#f5f1e8}.planbox img{display:block;max-width:100%;max-height:74vh;margin:auto}.close{position:absolute;top:10px;right:10px;width:44px;height:44px;border-radius:50%;background:#111;color:#fff;font-size:20px;text-decoration:none;display:grid;place-items:center}@media(max-width:760px){.dock{grid-template-columns:1fr}.facts{justify-content:center}.looks{overflow-x:auto}.planbtn{position:absolute;right:14px;bottom:150px;z-index:5}.card{bottom:16px;padding:13px}.pano{background-size:auto 100%}}</style>
</head>
<body>
<main class="tour">
<header class="bar"><div class="brand"><b>Aurelia Sde Dov · אורליה שדה דב</b><span><?php echo esc_html( $c['title'] . ' · ' . $unit_id ); ?></span></div><a class="back" href="<?php echo esc_url( $back ); ?>"><?php echo esc_html( $c['back'] ); ?></a></header>
<section class="stage" id="stage" aria-label="<?php echo esc_attr( $c['title'] ); ?>">
<div class="pano" id="pano"></div><div class="shade"></div><div class="hint"><?php echo esc_html( $c['drag'] ); ?></div>
<button class="hs" style="--x:18%;--y:51%" data-stop="terrace" aria-pressed="false" aria-label="<?php echo esc_attr( $c['terrace'] ); ?>">1</button>
<button class="hs" style="--x:52%;--y:57%" data-stop="living" aria-pressed="true" aria-label="<?php echo esc_attr( $c['living'] ); ?>">2</button>
<button class="hs" style="--x:82%;--y:53%" data-stop="kitchen" aria-pressed="false" aria-label="<?php echo esc_attr( $c['kitchen'] ); ?>">3</button>
<article class="card" aria-live="polite"><h1 id="t1"><?php echo esc_html( $c['living'] ); ?></h1><p id="t2"><?php echo esc_html( $c['living_d'] ); ?></p></article>
<?php if ( $plan ) : ?><a class="planbtn" href="#plan"><?php echo esc_html( $c['plan'] ); ?></a><?php endif; ?>
</section>
<footer class="dock"><div class="facts"><span><b><?php echo esc_html( $c['floor'] ); ?></b> <?php echo (int) $floor; ?></span><span><b><?php echo esc_html( $c['rooms'] ); ?></b> <?php echo esc_html( $rooms ); ?></span><span><b><?php echo esc_html( $c['sqm'] ); ?></b> <?php echo esc_html( $sqm ); ?> מ״ר</span><span><b><?php echo esc_html( $c['balcony'] ); ?></b> <?php echo esc_html( $balc ); ?> מ״ר</span><span><b><?php echo esc_html( $c['direction'] ); ?></b> <?php echo esc_html( $dir ); ?></span></div><div class="looks"><button data-look="18"><?php echo esc_html( $c['left'] ); ?></button><button data-look="52" aria-pressed="true"><?php echo esc_html( $c['center'] ); ?></button><button data-look="82"><?php echo esc_html( $c['right'] ); ?></button></div><a class="cta" href="<?php echo esc_url( $back ); ?>"><?php echo esc_html( $c['cta'] ); ?></a></footer>
</main>
<?php if ( $plan ) : ?><div class="plan" id="plan" role="dialog" aria-label="<?php echo esc_attr( $c['plan'] ); ?>"><div class="planbox"><a class="close" href="#stage" aria-label="Close">×</a><img src="<?php echo esc_url( $plan ); ?>" alt="<?php echo esc_attr( $c['plan'] ); ?>"></div></div><?php endif; ?>
<script>(function(){"use strict";var stops={terrace:{x:18,t:<?php echo wp_json_encode( $c['terrace'] ); ?>,d:<?php echo wp_json_encode( $c['terrace_d'] ); ?>},living:{x:52,t:<?php echo wp_json_encode( $c['living'] ); ?>,d:<?php echo wp_json_encode( $c['living_d'] ); ?>},kitchen:{x:82,t:<?php echo wp_json_encode( $c['kitchen'] ); ?>,d:<?php echo wp_json_encode( $c['kitchen_d'] ); ?>}};var stage=document.getElementById("stage"),pano=document.getElementById("pano"),t1=document.getElementById("t1"),t2=document.getElementById("t2"),pos=52,sx=0,sp=52,drag=false;function clamp(v){return Math.max(5,Math.min(95,v));}function look(x,id){pos=clamp(Number(x)||52);pano.style.backgroundPosition=pos+"% 50%";document.querySelectorAll("[data-look]").forEach(function(b){b.setAttribute("aria-pressed",Math.abs(Number(b.dataset.look)-pos)<2?"true":"false");});document.querySelectorAll("[data-stop]").forEach(function(b){b.setAttribute("aria-pressed",b.dataset.stop===id?"true":"false");});if(id&&stops[id]){t1.textContent=stops[id].t;t2.textContent=stops[id].d;}}document.querySelectorAll("[data-look]").forEach(function(b){b.addEventListener("click",function(){var v=Number(b.dataset.look);look(v,v<30?"terrace":(v>70?"kitchen":"living"));});});document.querySelectorAll("[data-stop]").forEach(function(b){b.addEventListener("click",function(){look(stops[b.dataset.stop].x,b.dataset.stop);});});stage.addEventListener("pointerdown",function(e){if(e.target.closest("button,a")){return;}drag=true;sx=e.clientX;sp=pos;stage.setPointerCapture(e.pointerId);});stage.addEventListener("pointermove",function(e){if(!drag){return;}look(sp-(e.clientX-sx)/stage.clientWidth*70);});stage.addEventListener("pointerup",function(){drag=false;});stage.addEventListener("keydown",function(e){if(e.key==="ArrowLeft"){look(pos-7);}if(e.key==="ArrowRight"){look(pos+7);}});look(52,"living");})();</script>
</body></html><?php
		exit;
	}
	add_action( 'template_redirect', 'nadlan_aurelia_tour', -100 );
}

/* the standalone-portal notice steps aside on the flagship page (owner order 26.8) */
if ( ! function_exists( 'nadlan_aurelia_clean_html' ) ) {
	function nadlan_aurelia_clean_html( $html ) {
		$html = preg_replace( '#<aside\b[^>]*class=(["\'])[^"\']*\bnl-projnotice\b[^"\']*\1[^>]*>.*?</aside>#isu', '', $html );
		return str_replace( ' · בקרוב', '', $html );
	}
	function nadlan_aurelia_buffer() {
		if ( nadlan_aurelia_is_page() && empty( $_GET['aurelia_tour'] ) ) { ob_start( 'nadlan_aurelia_clean_html' ); }
	}
	add_action( 'template_redirect', 'nadlan_aurelia_buffer', 0 );
}
