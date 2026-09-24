<?php
/**
 * nadlan-config - Property photo viewer (HAD-247, 24.9.2026)
 *
 * One light full-screen viewer for every photo of a listing:
 *   - the photo at the top of the portal template (the theme's featured image,
 *     or .nlps-cover when the listing has no featured image),
 *   - the .nlcard-gallery thumbnails (links to the file stay as the no-JS path),
 *   - the broker block: article.nlx .nlx-mast (the cover) and .nlx-gallery
 *     (Meital's listings, drop-box listings and their language twins).
 * Swipe is native CSS scroll-snap; arrows and keys on desktop; Escape, the X,
 * a tap beside the photo or the phone's back gesture close it; focus stays
 * inside while it is open. No library, inline only.
 *
 * It must keep running on owned listings: the property-owner rule unhooks the
 * portal layers (nadlan_pshow_*, nadlan_card_*), never nadlan_pgal_*.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_pgal_wanted' ) ) {
	function nadlan_pgal_wanted() {
		if ( is_admin() || ! is_singular() ) { return false; }
		if ( is_singular( 'nadlan_property' ) ) { return true; }
		$p = get_queried_object();
		return ( $p instanceof WP_Post ) && false !== strpos( (string) $p->post_content, '<article class="nlx' );
	}
}

if ( ! function_exists( 'nadlan_pgal_css' ) ) {
	function nadlan_pgal_css() {
		return '
.nlpg-zoom{cursor:zoom-in}
.nlpg-zoom:focus-visible{outline:2px solid #9C7A3C;outline-offset:3px}
.single-nadlan_property .wp-block-post-featured-image,.nlps-cover{position:relative}
.nlpg-pills{position:absolute;inset-inline-start:14px;bottom:14px;z-index:2;display:flex;flex-wrap:wrap;gap:8px}
.nlpg-pill{display:inline-flex;align-items:center;gap:7px;min-height:38px;padding:9px 14px;border-radius:999px;border:1px solid rgba(27,26,23,.14);background:rgba(250,247,241,.94);color:#1B1A17;font:600 13px/1 Heebo,system-ui,sans-serif;cursor:pointer;box-shadow:0 2px 10px rgba(17,17,15,.16)}
.nlpg-pill:hover{background:#fff}
.nlpg-pill:focus-visible{outline:2px solid #9C7A3C;outline-offset:2px}
.nlpg-pill svg{width:15px;height:15px;flex:none}
.nlpg{position:fixed;inset:0;z-index:2147483000;display:flex;flex-direction:column;background:#0E0D0B;color:#F5EFE2;font-family:Heebo,system-ui,sans-serif}
.nlpg[hidden]{display:none}
.nlpg-top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 14px;flex:none}
.nlpg-n{font:600 13px/1 Heebo,system-ui,sans-serif;letter-spacing:.05em;direction:ltr;unicode-bidi:isolate;opacity:.86}
.nlpg-x{width:44px;height:44px;border-radius:50%;border:1px solid rgba(245,239,226,.35);background:transparent;color:#F5EFE2;font:400 26px/1 system-ui,sans-serif;cursor:pointer}
.nlpg-x:hover,.nlpg-nav:hover{background:rgba(245,239,226,.12)}
.nlpg-x:focus-visible,.nlpg-nav:focus-visible{outline:2px solid #C9A961;outline-offset:2px}
.nlpg-track{flex:1;min-height:0;display:flex;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;overscroll-behavior:contain;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.nlpg-track::-webkit-scrollbar{display:none}
.nlpg-slide{flex:0 0 100%;width:100%;height:100%;margin:0;padding:0 clamp(0px,5vw,84px) 18px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;scroll-snap-align:center;scroll-snap-stop:always}
.nlpg-slide img{display:block;max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;border-radius:4px;-webkit-user-select:none;user-select:none}
.nlpg-nav{direction:ltr;position:absolute;top:50%;margin-top:-24px;width:48px;height:48px;border-radius:50%;border:1px solid rgba(245,239,226,.35);background:rgba(20,19,15,.55);color:#F5EFE2;font:400 30px/1 system-ui,sans-serif;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0 0 3px}
.nlpg-prev{left:14px}
.nlpg-next{right:14px}
.nlpg-nav[disabled]{opacity:.22;cursor:default}
@media (hover:none) and (pointer:coarse){.nlpg-nav{display:none}}
html.nlpg-lock,html.nlpg-lock body{overflow:hidden!important}
';
	}
}

if ( ! function_exists( 'nadlan_pgal_js' ) ) {
	function nadlan_pgal_js() {
		return <<<'NLPGJS'
(function(){
"use strict";
var d=document,H=d.documentElement,L=(H.lang||"he").slice(0,2).toLowerCase();
var T={he:["סגירה","התמונה הבאה","התמונה הקודמת","תמונות","תמונות הנכס","פתיחת התמונה בגודל מלא"],
en:["Close","Next photo","Previous photo","photos","Property photos","Open the photo full size"],
ru:["Закрыть","Следующее фото","Предыдущее фото","фото","Фотографии объекта","Открыть фото целиком"],
fr:["Fermer","Photo suivante","Photo précédente","photos","Photos du bien","Voir la photo en grand"]};
var S=T[L]||T.en,items=[],box,track,num,prevB,nextB,xB,cur=0,isOpen=false,pushed=false,back=null;
var ICON='<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="1.5" y="1.5" width="5.5" height="5.5" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/><rect x="9" y="1.5" width="5.5" height="5.5" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/><rect x="1.5" y="9" width="5.5" height="5.5" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/><rect x="9" y="9" width="5.5" height="5.5" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>';
function norm(u){var a=d.createElement("a");a.href=u;return a.host+a.pathname.replace(/-\d+x\d+(?=\.[a-z0-9]+$)/i,"");}
function shown(el){return !!(el.offsetWidth||el.offsetHeight||el.getClientRects().length);}
function big(img){var s=img.getAttribute("src")||"",best=s||img.currentSrc,bw=0,ss=img.getAttribute("srcset");
if(s&&!/-\d+x\d+\.[a-z0-9]+(\?|$)/i.test(s)){return s;}
if(ss){ss.split(",").forEach(function(c){var p=c.trim().split(/\s+/),w=parseInt(p[1],10)||0;if(p[0]&&w>bw){bw=w;best=p[0];}});}
return best;}
function add(src,alt){var k=norm(src);for(var i=0;i<items.length;i++){if(items[i].k===k){return i;}}items.push({k:k,src:src,alt:alt||""});return items.length-1;}
function bind(el,i){if(el.__nlpg){return;}el.__nlpg=1;el.classList.add("nlpg-zoom");
if(el.tagName!=="A"){var alt=el.getAttribute("alt");el.setAttribute("tabindex","0");el.setAttribute("role","button");el.setAttribute("aria-label",S[5]+(alt?": "+alt:""));
el.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();show(i);}});}
el.addEventListener("click",function(e){e.preventDefault();show(i);});}
function collect(){var sel=".single-nadlan_property .wp-block-post-featured-image img,.nlps-cover img,.nlcard-gallery a[href],article.nlx .nlx-mast img,article.nlx .nlx-gallery img";
[].forEach.call(d.querySelectorAll(sel),function(el){var isA=el.tagName==="A",img=isA?el.querySelector("img"):el;
if(!img||!shown(el)){return;}
if(!isA&&img.closest("a")){return;}
if(isA&&!/\.(jpe?g|png|webp|avif|gif)(\?|#|$)/i.test(el.getAttribute("href")||"")){return;}
bind(isA?el:img,add(isA?el.href:big(img),img.getAttribute("alt")));});}
function build(){box=d.createElement("div");box.className="nlpg";box.hidden=true;box.setAttribute("role","dialog");box.setAttribute("aria-modal","true");box.setAttribute("aria-label",S[4]);
box.innerHTML='<div class="nlpg-top"><span class="nlpg-n" aria-live="polite"></span><button type="button" class="nlpg-x" aria-label="'+S[0]+'">×</button></div><div class="nlpg-track" dir="ltr"></div><button type="button" class="nlpg-nav nlpg-prev" aria-label="'+S[2]+'">‹</button><button type="button" class="nlpg-nav nlpg-next" aria-label="'+S[1]+'">›</button>';
track=box.querySelector(".nlpg-track");num=box.querySelector(".nlpg-n");prevB=box.querySelector(".nlpg-prev");nextB=box.querySelector(".nlpg-next");xB=box.querySelector(".nlpg-x");
items.forEach(function(it){var f=d.createElement("figure"),im=d.createElement("img");f.className="nlpg-slide";im.alt=it.alt;im.decoding="async";im.draggable=false;im.setAttribute("data-src",it.src);f.appendChild(im);
f.addEventListener("click",function(e){if(e.target===f){close();}});track.appendChild(f);});
xB.addEventListener("click",function(){close();});
prevB.addEventListener("click",function(){go(cur-1);});
nextB.addEventListener("click",function(){go(cur+1);});
if("IntersectionObserver" in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&e.intersectionRatio>=0.6){var i=[].indexOf.call(track.children,e.target);if(i>-1&&isOpen){set(i);}}});},{root:track,threshold:[0.6]});
[].forEach.call(track.children,function(s){io.observe(s);});}
else{track.addEventListener("scroll",function(){if(isOpen){set(Math.round(track.scrollLeft/Math.max(1,track.clientWidth)));}},{passive:true});}
d.body.appendChild(box);}
function load(i){var s=track.children[i];if(!s){return;}var im=s.firstChild;if(!im.getAttribute("src")){im.src=im.getAttribute("data-src");}}
function set(i){cur=Math.max(0,Math.min(items.length-1,i));num.textContent=(cur+1)+" / "+items.length;load(cur);load(cur+1);load(cur-1);prevB.disabled=cur===0;nextB.disabled=cur===items.length-1;}
function go(i){if(i<0||i>=items.length){return;}load(i);try{track.scrollTo({left:i*track.clientWidth,behavior:"smooth"});}catch(e){track.scrollLeft=i*track.clientWidth;}set(i);}
function show(i){if(!items.length){return;}if(!box){build();}back=d.activeElement;isOpen=true;box.hidden=false;H.classList.add("nlpg-lock");
track.scrollLeft=i*track.clientWidth;set(i);try{xB.focus({preventScroll:true});}catch(e){xB.focus();}
if(!pushed){try{history.pushState({nlpg:1},"");pushed=true;}catch(e){}}}
function close(fromPop){if(!isOpen){return;}isOpen=false;box.hidden=true;H.classList.remove("nlpg-lock");
if(back&&back.focus){try{back.focus({preventScroll:true});}catch(e){}}
if(pushed){pushed=false;if(!fromPop){try{history.back();}catch(e){}}}}
window.addEventListener("popstate",function(){if(isOpen){pushed=false;close(true);}});
window.addEventListener("resize",function(){if(isOpen){track.scrollLeft=cur*track.clientWidth;}});
d.addEventListener("keydown",function(e){if(!isOpen){return;}
if(e.key==="Escape"){e.preventDefault();close();}
else if(e.key==="ArrowRight"){e.preventDefault();go(cur+1);}
else if(e.key==="ArrowLeft"){e.preventDefault();go(cur-1);}
else if(e.key==="Tab"){var f=[].filter.call(box.querySelectorAll("button"),function(b){return !b.disabled&&b.offsetParent!==null;});if(!f.length){return;}
e.preventDefault();var a=f.indexOf(d.activeElement);f[e.shiftKey?(a<=0?f.length-1:a-1):(a+1)%f.length].focus();}});
function pills(fig){var p=fig.querySelector(".nlpg-pills");if(!p){p=d.createElement("div");p.className="nlpg-pills";fig.appendChild(p);}return p;}
function init(){collect();window.nlpgOpen=show;
if(items.length>1){var fig=d.querySelector(".nlps-cover")||d.querySelector(".single-nadlan_property .wp-block-post-featured-image");
if(fig&&shown(fig)){var b=d.createElement("button");b.type="button";b.className="nlpg-pill nlpg-pill--photos";b.innerHTML=ICON+"<span>"+items.length+" "+S[3]+"</span>";
b.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();show(0);});pills(fig).insertBefore(b,pills(fig).firstChild);}}}
if(d.readyState==="loading"){d.addEventListener("DOMContentLoaded",init);}else{init();}
})();
NLPGJS;
	}
}

if ( ! function_exists( 'nadlan_pgal_assets' ) ) {
	function nadlan_pgal_assets() {
		if ( ! nadlan_pgal_wanted() ) { return; }
		wp_register_style( 'nadlan-pgal', false, array(), NADLAN_CONFIG_VERSION );
		wp_enqueue_style( 'nadlan-pgal' );
		wp_add_inline_style( 'nadlan-pgal', nadlan_pgal_css() );
		wp_register_script( 'nadlan-pgal-js', false, array(), NADLAN_CONFIG_VERSION, true );
		wp_enqueue_script( 'nadlan-pgal-js' );
		wp_add_inline_script( 'nadlan-pgal-js', nadlan_pgal_js() );
	}
}
add_action( 'wp_enqueue_scripts', 'nadlan_pgal_assets', 30 );
