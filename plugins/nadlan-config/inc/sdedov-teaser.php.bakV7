<?php
/**
 * nadlan-config - Sde Dov quarter-tour teaser band (v1.72.120)
 *
 * One light band, three surfaces: the homepage (after the flagship strip),
 * the Sde Dov area page, and under the live map on every project page that
 * belongs to the quarter (Sde Dov + Einstein). Pure HTML/CSS with one lazy
 * poster image - the band never delays page load; the heavy 3D experience
 * lives on its own page and opens in a new tab.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

function nadlan_sdedov_tour_url() {
	return apply_filters( 'nadlan_sdedov_tour_url', 'https://nad-lan.co.il/wp-content/uploads/2026/07/sde-dov-tour.html' );
}

function nadlan_sdedov_tour_poster() {
	return apply_filters( 'nadlan_sdedov_tour_poster', 'https://nad-lan.co.il/wp-content/uploads/2026/07/sdedov-tour-poster.jpg' );
}

/* Every catalog project that belongs to the quarter. Filterable so new
 * projects join with one line and future compounds can reuse the module. */
function nadlan_sdedov_tour_slugs() {
	return apply_filters( 'nadlan_sdedov_tour_slugs', array(
		'rainbow-tel-aviv', 'ashira-sde-dov', 'dimri-yama-sde-dov',
		'utopia-sde-dov', 'first-sde-dov', 'zohi-sde-dov', 'gindi-vogue-sde-dov',
		'migdalei-hayam-sde-dov', 'shikun-binui-sde-dov',
		'einstein-tower', 'einstein-19', 'ashdar-einstein',
	) );
}

/* Flagships that have a named node inside the tour - deep link straight to them. */
function nadlan_sdedov_tour_focus( $slug ) {
	$map = array( 'rainbow-tel-aviv' => 'rainbow', 'ashira-sde-dov' => 'ashira', 'dimri-yama-sde-dov' => 'dimri' );
	return isset( $map[ $slug ] ) ? $map[ $slug ] : '';
}

/* Back-compat no-op: css/js now ship via wp_enqueue (kses-proof). */
function nadlan_sdedov_tour_css() { return ''; }

function nadlan_sdedov_tour_css_raw() {
	return ''
		. '.nlsdt{position:relative;overflow:hidden;border-radius:18px;margin:26px auto;max-width:1240px;background:#101826;color:#fff;direction:rtl}'
		. '.nlsdt-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55}'
		. '.nlsdt-in{position:relative;z-index:2;padding:34px 30px;background:linear-gradient(270deg,rgba(10,15,26,.88) 0%,rgba(10,15,26,.6) 55%,rgba(10,15,26,.2) 100%)}'
		. '.nlsdt-kick{font:700 13px/1 Heebo,sans-serif;letter-spacing:.12em;color:#F2C14E;margin:0 0 8px}'
		. '.nlsdt h2,.nlsdt-title{font:900 clamp(22px,3vw,32px)/1.2 Heebo,sans-serif;margin:0 0 8px;color:#fff}'
		. '.nlsdt-sub{font:400 15.5px/1.6 Heebo,sans-serif;color:#D9E0EC;max-width:34em;margin:0 0 14px}'
		. '.nlsdt-chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px;padding:0;list-style:none}'
		. '.nlsdt-chips li{font:600 12.5px/1 Heebo,sans-serif;color:#EFE3C8;border:1px solid rgba(242,193,78,.45);border-radius:999px;padding:7px 12px}'
		. '.nlsdt-cta{display:inline-block;background:#B85410;color:#fff;font:800 17px/1 Heebo,sans-serif;border-radius:10px;padding:14px 28px;text-decoration:none}'
		. '.nlsdt-cta:hover{background:#9C4409;color:#fff}'
		. '.nlsdt-cta2{display:inline-block;margin-inline-start:12px;color:#F2C14E;font:700 14px/1 Heebo,sans-serif;text-decoration:none}'
		. '.nlsdt-note{font:400 11.5px/1.5 Heebo,sans-serif;color:#94A0B4;margin:12px 0 0}'
		. '@media(max-width:640px){.nlsdt-in{padding:24px 18px;background:linear-gradient(180deg,rgba(10,15,26,.35) 0%,rgba(10,15,26,.9) 60%)}.nlsdt-cta{display:block;text-align:center}.nlsdt-cta2{display:block;margin:10px 0 0;text-align:center}}'
		. '.nlsdt-ov{position:fixed;inset:0;z-index:100000;background:#0b0f1a;display:none}'
		. '.nlsdt-ov.on{display:block}'
		. '.nlsdt-ovfr{position:absolute;inset:0;width:100%;height:100%;border:0;opacity:0;transition:opacity .3s}'
		. '.nlsdt-ov.ld .nlsdt-ovfr{opacity:1}'
		. '.nlsdt-ovx{position:absolute;top:14px;inset-inline-start:14px;z-index:2;width:44px;height:44px;border-radius:12px;border:1px solid rgba(255,255,255,.3);background:rgba(10,14,24,.72);color:#fff;font-size:18px;cursor:pointer}'
		. '.nlsdt-ovx:hover{background:rgba(30,38,58,.85)}'
		. '.nlsdt-ovsp{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#C9D2E2;font:600 15px/1 Heebo,sans-serif}'
		. '.nlsdt-ov.ld .nlsdt-ovsp{display:none}'
		. '.nlsdt-cardtour{display:inline-block;margin-top:7px;color:#F2C14E;font:700 13px/1 Heebo,sans-serif;text-decoration:none}'
		. '.nlsdt-cardtour:hover{color:#FFD98F}'
		. '@media(prefers-reduced-motion:no-preference){@keyframes nlsdtPulse{0%,100%{box-shadow:0 0 0 0 rgba(242,193,78,0)}50%{box-shadow:0 0 0 7px rgba(242,193,78,.22)}}.nlsdt-cta{animation:nlsdtPulse 2.6s ease-in-out infinite}}'
		. '.nlsdt--pair{margin:0;max-width:none;height:100%}'
		. '.nlsdt--pair .nlsdt-in{padding:26px 24px}'
		. '.nlhv2-tourvideo{align-items:stretch}'
		. '.nlhv2-tourvideo.is-solo{display:block}'
		. '.nlhv2-tvvid{display:flex;flex-direction:column;justify-content:center;gap:8px}'
		. '.nlhv2-tourvideo .nlhv2-video-frame{max-width:none;aspect-ratio:16/9;border-radius:18px;overflow:hidden;border:1px solid #D6C189;background:#14130F}'
		. '.nlhv2-tourvideo .nlhv2-video-frame video,.nlhv2-tourvideo .nlhv2-video-frame iframe{width:100%;height:100%;object-fit:cover;display:block;border:0}'
		. '@media(max-width:860px){.nlhv2-tourvideo{grid-template-columns:1fr}.nlsdt--pair .nlsdt-in{padding:24px 20px}}';
}

/* One overlay engine per page: click a .nlsdt-open control and the tour opens
 * full-screen IN PLACE (iframe layer) - the visitor never leaves the page.
 * Zero bytes are loaded until the click; hovering prefetches the tour HTML. */
function nadlan_sdedov_tour_overlay_js() { return ''; }

function nadlan_sdedov_tour_overlay_js_raw() {
	return '(function(){if(window.NLSDT)return;var ov,fr,cl;'
		. 'function build(){ov=document.createElement("div");ov.className="nlsdt-ov";ov.setAttribute("role","dialog");ov.setAttribute("aria-modal","true");ov.setAttribute("aria-label","סיור תלת ממדי");'
		. 'ov.innerHTML=\'<button class="nlsdt-ovx" aria-label="סגירת הסיור">✕</button><div class="nlsdt-ovsp">טוען את הסיור...</div><iframe class="nlsdt-ovfr" allow="fullscreen; xr-spatial-tracking" title="סיור תלת ממדי ברובע"></iframe>\';'
		. 'document.body.appendChild(ov);fr=ov.querySelector("iframe");cl=ov.querySelector(".nlsdt-ovx");'
		. 'cl.addEventListener("click",close);'
		. 'document.addEventListener("keydown",function(e){if(e.key==="Escape")close();});'
		. 'fr.addEventListener("load",function(){if(fr.src&&fr.src!=="about:blank")ov.classList.add("ld");});}'
		. 'function open(u){if(!ov)build();fr.src=u;ov.classList.remove("ld");ov.classList.add("on");document.documentElement.style.overflow="hidden";cl.focus();}'
		. 'function close(){if(!ov)return;ov.classList.remove("on","ld");fr.src="about:blank";document.documentElement.style.overflow="";}'
		. 'window.NLSDT={open:open,close:close};'
		. 'document.addEventListener("click",function(e){var a=e.target.closest(".nlsdt-open");if(!a)return;var u=a.getAttribute("data-url")||a.getAttribute("href");if(!u)return;e.preventDefault();open(u);});'
		. 'document.addEventListener("pointerover",function(e){var a=e.target.closest(".nlsdt-open");if(!a||a.__pf)return;a.__pf=1;var l=document.createElement("link");l.rel="prefetch";l.href=a.getAttribute("data-url")||a.getAttribute("href");document.head.appendChild(l);});'
		. '})();';
}

/* Site-wide enqueue of the teaser skin + overlay engine (~5KB inline).
 * Enqueued assets survive every content sanitizer, unlike in-band <style>/<script>. */
add_action( 'wp_enqueue_scripts', function () {
	$ver = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
	wp_register_style( 'nlsdt', false, array(), $ver );
	wp_enqueue_style( 'nlsdt' );
	wp_add_inline_style( 'nlsdt', nadlan_sdedov_tour_css_raw() );
	wp_register_script( 'nlsdt', false, array(), $ver, true );
	wp_enqueue_script( 'nlsdt' );
	wp_add_inline_script( 'nlsdt', nadlan_sdedov_tour_overlay_js_raw() );
}, 20 );

/* Small quarter-tour link for a flagship card (homepage gallery etc.):
 * opens the tour focused on that building, inside the overlay. */
function nadlan_sdedov_card_tour_btn( $post ) {
	$slug  = get_post_field( 'post_name', $post );
	if ( ! in_array( $slug, nadlan_sdedov_tour_slugs(), true ) ) { return ''; }
	$focus = nadlan_sdedov_tour_focus( $slug );
	$url   = nadlan_sdedov_tour_url() . ( $focus ? '?focus=' . rawurlencode( $focus ) . '&mode=explore' : '' );
	return '<a class="nlsdt-cardtour nlsdt-open" href="' . esc_url( $url ) . '" data-url="' . esc_url( $url ) . '" target="_blank" rel="noopener">סיור ברובע שדה דב ←</a>';
}

/**
 * The band itself.
 *
 * @param string $variant 'home' | 'project' | 'page'
 * @param string $focus   optional tour node key (rainbow|ashira|dimri)
 */
function nadlan_sdedov_tour_band( $variant = 'home', $focus = '' ) {
	$url  = nadlan_sdedov_tour_url();
	$link = $focus ? $url . '?focus=' . rawurlencode( $focus ) . '&mode=explore' : $url;
	$cls  = ( 'pair' === $variant ) ? 'nlsdt nlsdt--pair' : 'nlsdt';
	$html = '<section class="' . esc_attr( $cls ) . '" aria-label="סיור תלת ממדי ברובע שדה דב">'
		. '<img class="nlsdt-img" src="' . esc_url( nadlan_sdedov_tour_poster() ) . '" alt="" loading="lazy" decoding="async">'
		. '<div class="nlsdt-in">'
		. '<p class="nlsdt-kick">חדש · סיור תלת ממדי חי</p>'
		. '<p class="nlsdt-title">נכנסים לעתיד של רובע שדה דב</p>'
		. '<p class="nlsdt-sub">' . ( 'project' === $variant
			? 'הפרויקט הזה הוא חלק מרובע שלם שקם על קו החוף. מסתובבים ברחובות של 2035, עוברים בין המגדלים, ורואים איך הכול מתחבר.'
			: 'מסתובבים ברחובות הרובע של 2035, עוברים בין המגדלים, יורדים לטיילת, ובוחרים דירה מתוך הבניין. הדמיה חיה בדפדפן, בלי להוריד כלום.' )
		. '</p>'
		. '<ul class="nlsdt-chips"><li>מכונת זמן 2026 ⇄ 2035</li><li>סיור חופשי עם חצים</li><li>כל בניין לחיץ</li></ul>'
		. '<a class="nlsdt-cta nlsdt-open" href="' . esc_url( $link ) . '" data-url="' . esc_url( $link ) . '" target="_blank" rel="noopener">כניסה לסיור</a>'
		. ( ( 'project' === $variant && $focus ) ? '<a class="nlsdt-cta2 nlsdt-open" href="' . esc_url( $url ) . '" data-url="' . esc_url( $url ) . '" target="_blank" rel="noopener">או מתחילים מתצפית על כל הרובע ←</a>' : '' )
		. '<p class="nlsdt-note">הדמיה להמחשה על פי תכנית רובע שדה דב. אינה מטעם היזמים או גורם רשמי.</p>'
		. '</div></section>';
	return $html;
}

/* Surface 3: the Sde Dov area page gets the full band appended to its content. */
function nadlan_sdedov_tour_page_append( $content ) {
	if ( is_page( 'sde-dov' ) && in_the_loop() && is_main_query() ) {
		$content .= nadlan_sdedov_tour_band( 'page' );
	}
	return $content;
}
add_filter( 'the_content', 'nadlan_sdedov_tour_page_append', 21 );
