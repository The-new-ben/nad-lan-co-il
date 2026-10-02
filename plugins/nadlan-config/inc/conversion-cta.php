<?php
/**
 * nadlan-config - Conversion CTA layer (v1.40.3)
 *
 * STRIPPED 2026-06-03 per owner: the sticky bottom bar AND the exit-intent modal
 * are KILLED everywhere (mobile + desktop). They were too intrusive on mobile
 * (mouseout-based exit detection fired on scroll, sticky bar jumped the layout).
 *
 * What remains:
 *   - Floating WhatsApp click-to-chat button (owner-controlled via Settings → NadLan CTA)
 *   - window.nadlanGA() dataLayer helper (other plugin scripts depend on it)
 *   - /nadlan/v1/lead REST endpoint (still used by claim-prompt, AI concierge handoff, etc.)
 *   - Settings page for the WhatsApp number
 *
 * If we ever want the popup/sticky back, restore from git history of this file
 * (last good version: v1.40.2). Don't re-introduce them without a UX plan.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cta_enabled' ) ) {
	function nadlan_cta_enabled() {
		if ( defined( 'NADLAN_DISABLE_CONVERSION_CTA' ) && NADLAN_DISABLE_CONVERSION_CTA ) { return false; }
		// the WhatsApp pill is on every page for every visitor, logged-in included (owner order 28.9.2026: the money button, on every page)
		if ( is_admin() ) { return false; }
		if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) { return false; }
		return true;
	}
}

if ( ! function_exists( 'nadlan_cta_whatsapp_number' ) ) {
	function nadlan_cta_whatsapp_number() {
		$raw = (string) get_option( 'nadlan_owner_whatsapp', '' );
		return preg_replace( '/[^0-9+]/', '', $raw );
	}
}

add_action( 'wp_footer', function () {
	if ( ! nadlan_cta_enabled() ) { return; }
	$wa = nadlan_cta_whatsapp_number();
	if ( ! $wa ) {
		// PublishPage v70: pages owned by a broker or an owner empty the site number (their own buttons carry the lead); on
		// wide screens the owner's own WhatsApp then floats in the pill's corner, so no page is left without a floating WhatsApp
		echo '<style id="nlcta-owned">@media (min-width:721px){html body .nlb .nlb-mbar{display:block;position:fixed;bottom:20px;inset-inline-end:20px;z-index:9990;padding:0;background:none;border:0}html body .nlb .nlb-mbar > :not(:first-child){display:none}html body .nlb .nlb-mbar .nlb-btn{min-height:54px;padding:0 22px;border-radius:999px;box-shadow:0 10px 24px rgba(20,33,43,.28)}}@media (min-width:761px){html body .nlx .nlx-mbar{display:block;position:fixed;bottom:20px;inset-inline-end:20px;z-index:9990;padding:0;background:none}html body .nlx .nlx-mbar > :not(:first-child){display:none}html body .nlx .nlx-mbar .nlx-btn{min-height:54px;padding:0 22px;border-radius:999px;box-shadow:0 10px 24px rgba(20,33,43,.28)}}</style>' . "\n";
		// No WhatsApp configured - still emit the GA helper so other modules can use it.
		echo "<script>window.dataLayer=window.dataLayer||[];window.nadlanGA=window.nadlanGA||function(n,p){try{window.dataLayer.push(Object.assign({event:n},p||{}));}catch(e){}};</script>\n";
		return;
	}
	/* V8 (owner order 22.8): the circle grows into a WIDE pill — WhatsApp glyph
	   + "לפרטים נוספים" + the NadLan brand chip — localized via the i18n tables
	   so English (and fr/ru/ar) pages speak their language. The page-context
	   pull stays in wa-source.php, which stamps this link on click. */
	$cta_b    = function_exists( 'nadlan_i18n' ) ? nadlan_i18n( 'cta_wa_b' ) : 'לפרטים נוספים';
	$cta_s    = function_exists( 'nadlan_i18n' ) ? nadlan_i18n( 'cta_wa_s' ) : 'מענה מהיר בוואטסאפ';
	$cta_aria = function_exists( 'nadlan_i18n' ) ? nadlan_i18n( 'cta_wa_aria' ) : 'וואטסאפ · לפרטים נוספים';
	$cta_msg  = function_exists( 'nadlan_i18n' ) ? nadlan_i18n( 'cta_wa_msg' ) : 'שלום, אשמח לפרטים נוספים.';
	/* Review voice on independent project pages (owner order 31.8.2026): the
	 * floating pill must never read like the developer's sales channel. */
	if ( is_singular( 'nadlan_project' ) && function_exists( 'nadlan_project_mode' ) && 'showroom' !== nadlan_project_mode( get_queried_object_id() ) ) {
		$rv_lang = function_exists( 'nadlan_project_self_lang' ) ? nadlan_project_self_lang() : '';
		if ( '' === $rv_lang ) { $rv_lang = 'he'; }
		$rv = array(
			// ApartmentExperience-1 (v101, 29.9.2026): "ייעוץ חינם" on every page; the independence stays in the small line
			'he' => array( "ייעוץ חינם", "לא מטעם היזם · מענה בוואטסאפ", "וואטסאפ · ייעוץ חינם על הפרויקט", "שלום, יש לי שאלה על הפרויקט." ),
			'en' => array( "Free consultation", "Not the developer · on WhatsApp", "WhatsApp: free consultation on the project", "Hi, I have a question about this project." ),
			'fr' => array( "Conseil gratuit", "Pas le promoteur · sur WhatsApp", "WhatsApp : conseil gratuit sur le projet", "Bonjour, j'ai une question sur ce projet." ),
			'ru' => array( "Бесплатная консультация", "Не от застройщика · в WhatsApp", "WhatsApp: бесплатная консультация по проекту", "Здравствуйте, у меня вопрос по проекту." ),
			'ar' => array( "استشارة مجانية", "ليست من المطور · على واتساب", "واتساب · استشارة مجانية حول المشروع", "مرحبا، لدي سؤال حول المشروع." ),
		);
		$rv_v = isset( $rv[ $rv_lang ] ) ? $rv[ $rv_lang ] : $rv['he'];
		$cta_b = $rv_v[0]; $cta_s = $rv_v[1]; $cta_aria = $rv_v[2]; $cta_msg = $rv_v[3];
	}
	$cta_rtl  = true;
	if ( function_exists( 'nadlan_lang_is_rtl' ) && function_exists( 'nadlan_current_lang' ) ) {
		$cta_rtl = nadlan_lang_is_rtl( nadlan_current_lang() );
	}
	?>
<div id="nlcta" dir="<?php echo $cta_rtl ? 'rtl' : 'ltr'; ?>">
	<a class="nlcta-wa" data-nl-whatsapp href="https://wa.me/<?php echo esc_attr( $wa ); ?>?text=<?php echo rawurlencode( $cta_msg ); ?>" target="_blank" rel="noopener" aria-label="<?php echo esc_attr( $cta_aria ); ?>">
		<span class="nlcta-glyph" aria-hidden="true"><svg viewBox="0 0 24 24" width="21" height="21" fill="#fff"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.85 9.85 0 0 0 12.04 2zm0 18.15h-.01a8.22 8.22 0 0 1-4.19-1.15l-.3-.18-3.11.82.83-3.04-.2-.31a8.22 8.22 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.24-8.25 8.24zm4.52-6.16c-.25-.12-1.47-.72-1.7-.81-.22-.08-.39-.12-.55.13-.16.25-.62.81-.76.97-.14.17-.28.19-.53.06-.25-.13-1.05-.39-2-1.23a7.5 7.5 0 0 1-1.38-1.72c-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.16.04-.31-.02-.43-.06-.12-.55-1.33-.76-1.83-.2-.48-.4-.41-.55-.42l-.47-.01c-.16 0-.42.06-.64.31-.22.25-.84.82-.84 2.01s.86 2.33.98 2.49c.12.16 1.7 2.6 4.13 3.65.58.25 1.02.4 1.37.51.58.18 1.1.16 1.52.1.46-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.1-.23-.16-.48-.29z"/></svg></span>
		<span class="nlcta-txt"><b><?php echo esc_html( $cta_b ); ?></b><small><?php echo esc_html( $cta_s ); ?></small></span>
		<span class="nlcta-brand" aria-hidden="true"><svg viewBox="0 0 64 64" width="30" height="30"><rect width="64" height="64" rx="14" fill="#F7F6F2"/><rect x="10" y="30" width="11" height="22" rx="1.5" fill="#1F4B5C" opacity=".72"/><rect x="26.5" y="14" width="11" height="38" rx="1.5" fill="#1F4B5C"/><rect x="43" y="24" width="11" height="28" rx="1.5" fill="#1F4B5C" opacity=".86"/><rect x="8" y="55" width="48" height="2.6" rx="1.3" fill="#1F4B5C"/></svg></span>
	</a>
</div>
<?php
	// ConsultSheet (v101): a click on the pill opens a short message sheet (inc/cta-sheet.php); without it the pill is a plain link.
	// v103.1 (30.9.2026, owner): "one button, one click... don't put obstacles" - the pill opens WhatsApp directly with a ready
	// message (wa-source.php adds the page). The sheet stays in the code, off; the filter turns it back on.
	if ( apply_filters( 'nadlan_cta_sheet_on', false ) && function_exists( 'nadlan_cta_sheet_html' ) ) {
		$cs_lang = function_exists( 'nadlan_current_lang' ) ? (string) nadlan_current_lang() : 'he';
		echo nadlan_cta_sheet_html( $wa, $cta_rtl, in_array( $cs_lang, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $cs_lang : 'he' ); // phpcs:ignore -- escaped inside
	}
?>
<style>
#nlcta{position:fixed;bottom:20px;inset-inline-end:20px;z-index:99989;font-family:var(--font-sans,Heebo,system-ui,sans-serif)}
/* 24.9.2026, from the design system (Button, wa-green): a deep WhatsApp green. White on #25D366 read at 1.98:1 and
   the pill stood out from the page at 1.83:1; on #0F7A63 the white lines read at 5.27:1 and the pill at 4.87:1. */
.nlcta-wa{display:flex;align-items:center;gap:10px;min-height:54px;padding:8px 14px;border-radius:999px;background:#0F7A63;box-shadow:0 10px 24px rgba(15,122,99,.30);text-decoration:none;transition:transform .2s,box-shadow .2s,filter .2s}
.nlcta-wa:hover{transform:translateY(-3px);filter:brightness(1.06);box-shadow:0 14px 36px rgba(15,122,99,.38)}
body.nl-skin-a #nlcta .nlcta-wa{box-shadow:0 10px 24px rgba(15,122,99,.30)!important}
.nlcta-glyph{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,.18);flex:0 0 auto}
.nlcta-txt{display:flex;flex-direction:column;line-height:1.15;color:#fff;white-space:nowrap}
.nlcta-txt b{font:800 15px/1.2 var(--font-sans,Heebo,system-ui,sans-serif);color:#fff}
.nlcta-txt small{font:500 11px/1.2 var(--font-sans,Heebo,system-ui,sans-serif);color:#fff;margin-top:2px}
.nlcta-brand{display:grid;place-items:center;flex:0 0 auto;border-radius:7px;overflow:hidden;line-height:0}
@media(max-width:520px){#nlcta{bottom:14px;inset-inline-end:14px}.nlcta-wa{min-height:50px;max-width:min(62vw,250px);padding:7px 12px;gap:8px}}
@media(max-width:380px){.nlcta-txt small{display:none}}
@media(prefers-reduced-motion:reduce){.nlcta-wa{transition:none}.nlcta-wa:hover{transform:none}}
/* V9 (owner order 22.8): the pill shows on engine project pages too — it
   rides ABOVE the showroom sticky cluster instead of hiding behind it
   (overrides showroom.css body.nl-has-engine #nlcta{display:none}) */
body.nl-has-engine #nlcta{display:block!important;bottom:92px!important}
@media(max-width:760px){body.nl-has-engine #nlcta{bottom:calc(env(safe-area-inset-bottom,0px) + 148px)!important}}
/* ApartmentExperience-1 (design system v101, 29.9.2026): the pill stays wide on every width and at every scroll: the NadLan
   mark, WhatsApp and "ייעוץ חינם". The round 54px button after 120px of scrolling (PublishPage v48-69) is gone. It still never
   hides, and over a form button or the stage's floor card it moves up instead (v69, v91). */
@media(max-width:520px){.nlcta-wa{max-width:min(72vw,280px)}}
/* P8 (1.72.370): the Russian words ("Бесплатная консультация", 201px) pushed the NadLan mark past the pill and off a 360-390px
   screen; on Russian pages the pill may take a little more width and the words a slightly smaller size (measured: fits at 360) */
@media(max-width:520px){html[lang^="ru"] #nlcta .nlcta-wa{max-width:min(80vw,292px)}html[lang^="ru"] #nlcta .nlcta-txt b{font-size:13.5px;letter-spacing:-.1px}}
@media(max-width:600px){html body #nlcta.is-clear{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}}
/* v101.2: above the area map's cone, on every width (the script below sets is-cone and the lift) */
html body #nlcta.is-cone{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}
/* ConsultBand (design system v104.25, HAD-390, 2.10.2026): on a 3D-world page (.nlps-stage--world), at every width, the bar and
   the accessibility button share a band of their own at the foot of the screen. The bar used to hold its corner by rising to the
   nearest free slot between buttons, and text was no obstacle, so it parked on the price, the facts and the apartment button.
   The CSS owns the layout: --nlcta-band:1 tells both scripts to stand still. The page keeps the height of the band at its end,
   and the sticky 3D of a wide stage ends above the band. Keyboard focus and in-page links scroll with the band in mind
   (scroll-padding-bottom; Maya, 2.10: a native Tab put the apartment button half under the band). */
body:has(.nlps-stage--world){--nlcta-band:1;padding-bottom:calc(72px + env(safe-area-inset-bottom,0px))!important}html:has(.nlps-stage--world){scroll-padding-bottom:calc(84px + env(safe-area-inset-bottom,0px))}html body:has(.nlps-stage--world) #nlcta,html body:has(.nlps-stage--world) #nlcta.is-clear,html body:has(.nlps-stage--world) #nlcta.is-cone{left:0!important;right:0!important;bottom:0!important;display:flex;justify-content:flex-end;align-items:center;box-sizing:border-box;padding:8px 14px calc(8px + env(safe-area-inset-bottom,0px));padding-inline-start:80px;background:#FAF7F1;border-top:1px solid #E2DCD0;box-shadow:0 -6px 18px rgba(27,26,23,.07)}html body:has(.nlps-stage--world) #nlcta .nlcta-wa{max-width:min(100%,360px)!important;box-shadow:none}html body:has(.nlps-stage--world) #nla11y{bottom:calc(8px + env(safe-area-inset-bottom,0px))!important;transform:none!important}@media(min-width:521px){html body:has(.nlps-stage--world) #nlcta{padding-inline-end:20px;padding-inline-start:88px}}html body:has(.nlps-stage--world) .nlw.nlw--docked.nlw--side{height:clamp(440px,calc(100svh - 168px - env(safe-area-inset-bottom,0px)),760px)}
/* WhatsAppBarEverywhere (design system v103, 29.9.2026, owner order): the site's "ייעוץ חינם" bar is on EVERY page, broker
   and owner pages included, even where the page has its own WhatsApp. Broker pages are built once with
   ".nlcta-wa{display:none!important}" baked into their styles (broker-drop.php); this stronger rule brings the bar back.
   On wide screens the broker's own WhatsApp still floats in the same corner, now ABOVE the site bar (bottom 88px), never
   under it. On phones the broker's bottom bar stays, and the site bar rises above it (the script's collision list). */
html body #nlcta .nlcta-wa{display:flex!important}
@media (min-width:721px){html body .nlb .nlb-mbar{display:block;position:fixed;bottom:88px;inset-inline-end:20px;z-index:9990;padding:0;background:none;border:0}html body .nlb .nlb-mbar > :not(:first-child){display:none}html body .nlb .nlb-mbar .nlb-btn{min-height:54px;padding:0 22px;border-radius:999px;box-shadow:0 10px 24px rgba(20,33,43,.28)}}
@media (min-width:761px){html body .nlx .nlx-mbar{display:block;position:fixed;bottom:88px;inset-inline-end:20px;z-index:9990;padding:0;background:none}html body .nlx .nlx-mbar > :not(:first-child){display:none}html body .nlx .nlx-mbar .nlx-btn{min-height:54px;padding:0 22px;border-radius:999px;box-shadow:0 10px 24px rgba(20,33,43,.28)}}
</style>
<script>
(function(){
	window.dataLayer=window.dataLayer||[];
	window.nadlanGA=window.nadlanGA||function(n,p){try{window.dataLayer.push(Object.assign({event:n},p||{}));}catch(e){}};
	var wa=document.querySelector('.nlcta-wa');
	// with the sheet, the click that counts is the sheet's own "open in WhatsApp" (inc/cta-sheet.php); the pill alone stays a link
	if(wa&&!document.getElementById('nlcta-sheet'))wa.addEventListener('click',function(){window.nadlanGA('whatsapp_click');});
	var box=document.getElementById('nlcta');
	if(box&&window.matchMedia){
		var mq=window.matchMedia('(max-width:600px)'),tick=false,back=0;
		// v103: the broker's and the owner's bottom bars count too, so the site bar rises above them instead of covering them
		var subs=[].slice.call(document.querySelectorAll('form button,form input[type=submit],.nlow button,.nlb-mbar,.nlx-mbar'));
		/* StagePillClear v91 (28.9.2026): the 3D stage's floor card opens at the foot of the phone's screen with its buttons in
		   the pill's corner ("לקבלת תוכניות ומחירים" half under the circle); a stage button in that corner lifts the pill too.
		   Only the pill's own column counts, and its column does not move when it is lifted, so it never flickers. */
		// the lift clears the whole card (its top + 10px), not a fixed 150px that left the circle on the card's next button
		var wa0=box.querySelector('.nlcta-wa');
		/* PhoneFirstScreen (design system v104.1, P9a, 30.9.2026): the pill finds a free place in its own column. The page top's
		   buttons (.nlps-hero__cta, as one block) join the stage's controls (each climbed to its card, as v91) as places the pill
		   never covers; it takes the free place NEAREST its resting place, a little lower or higher, never closer than 16px to the
		   screen's foot and at most 70% up. Before, it rose over the world's tabs straight onto the third hero button, and on a
		   lift below its resting place it could drop onto the tabs. A world's map labels (.nlw-labels) move with the camera: the
		   pill floats over the map as over a picture instead of chasing them. Nothing here depends on where the pill itself is,
		   so it never flickers. */
		var safeB=null,safe=function(){
			if(null===safeB){safeB=0;try{var sp=document.createElement('div');sp.style.cssText='position:fixed;left:0;bottom:0;width:1px;height:0;visibility:hidden;pointer-events:none;padding-bottom:env(safe-area-inset-bottom,0px)';document.body.appendChild(sp);safeB=sp.offsetHeight||0;sp.parentNode.removeChild(sp);}catch(e){safeB=0;}}
			return safeB;
		};
		window.addEventListener('resize',function(){safeB=null;});
		var stageHit=function(h){
			if(!wa0)return 0;
			var rest=Number(box.getAttribute('data-rest'))||0,p=wa0.getBoundingClientRect(),ph=p.height;
			if(!rest||!ph)return 0;
			var top0=h-rest,obs=[],seen=[],els=document.querySelectorAll('.nlps-hero__cta,#nlps button,#nlps a,#nlps input,#nlps-pick button,#nlps-pick a,.nlps-steps button,.nlps-steps a,#nlps-view-cta button,#nlps-view-cta a,#nlps summary');
			for(var i=0;i<els.length;i++){
				var e=els[i];
				if(e.closest&&e.closest('.nlw-labels'))continue;
				var r=e.getBoundingClientRect();
				if(!r.height||r.bottom<h*0.25||r.top>h||r.left>=p.right+8||r.right<=p.left-8)continue;
				var c=e;
				if(!e.classList.contains('nlps-hero__cta')){while(c.parentElement&&c.parentElement.id!=='nlps'&&c.parentElement.id!=='nlps-pick'&&c.parentElement.getBoundingClientRect().height<h*0.55){c=c.parentElement;}}
				if(seen.indexOf(c)>-1)continue;
				seen.push(c);
				var q=c.getBoundingClientRect();
				obs.push([q.top-10,q.bottom+10]);
			}
			var free=function(t){for(var k=0;k<obs.length;k++){if(obs[k][1]>t&&obs[k][0]<t+ph)return false;}return true;};
			if(free(top0))return 0;
			var lo=Math.round(h*0.3),hi=Math.round(h-ph-Math.max(16,safe()+8)),best=null,cand=[];
			for(var j=0;j<obs.length;j++){cand.push(obs[j][0]-ph,obs[j][1]);}
			for(var n=0;n<cand.length;n++){var t=cand[n];if(t<lo||t>hi||!free(t))continue;if(null===best||Math.abs(t-top0)<Math.abs(best-top0))best=t;}
			if(null===best){var raw=[];for(var i2=0;i2<els.length;i2++){var e2=els[i2];if(e2.closest&&e2.closest('.nlw-labels'))continue;var r2=e2.getBoundingClientRect();if(!r2.height||r2.left>=p.right+8||r2.right<=p.left-8)continue;raw.push([r2.top-6,r2.bottom+6]);}var ov=function(t){var s=0;for(var k=0;k<raw.length;k++){s+=Math.max(0,Math.min(raw[k][1],t+ph)-Math.max(raw[k][0],t));}return s;},bo=null;cand.push(top0,lo);for(var k2=0;k2<raw.length;k2++){cand.push(raw[k2][0]-ph,raw[k2][1]);}for(var n2=0;n2<cand.length;n2++){var t2=Math.min(Math.max(cand[n2],lo),Math.max(lo,hi));var v=ov(t2);if(null===bo||v<bo-0.5||(Math.abs(v-bo)<=0.5&&Math.abs(t2-top0)<Math.abs(best-top0))){bo=v;best=t2;}}}
			return Math.max(1,Math.round(h-best-ph-safe()));
		};
		/* ApartmentMapLanding (design system v101.2, 29.9.2026): the pill never covers the direction the buyer chose. When the
		   area map's cone (bridge.js, on stage pages) meets the pill's resting place, the pill rises 10px above it, on every
		   width, and comes back once the cone has passed. The test is against the resting place (data-rest: its top, counted
		   from the screen's foot, measured whenever it rests), so the pill does not flicker. bridge.js reads data-rest too, to
		   land the map above it. */
		var coneHit=function(h){
			var w=document.querySelector('.nlps-cone path'),rest=Number(box.getAttribute('data-rest'))||0;
			if(!w||!wa0||!rest)return 0;
			var r=w.getBoundingClientRect(),m=w.closest('.mapboxgl-map'),p=wa0.getBoundingClientRect();
			if(!r.height)return 0;
			if(m){var mr=m.getBoundingClientRect();if(r.bottom<mr.top||r.top>mr.bottom)return 0;}
			var top=h-rest;
			if(r.bottom>top-8&&r.top<top+p.height+8&&r.left<p.right+8&&r.right>p.left-8)return Math.min(Math.round(h-r.top+10),Math.round(h*0.7));
			return 0;
		};
		var fit=function(){
			tick=false;if(getComputedStyle(document.body).getPropertyValue('--nlcta-band').trim()==='1'){box.classList.remove('is-clear','is-cone');box.style.removeProperty('--nlcta-lift');return;}/* ConsultBand v104.25: the band (CSS) owns the bar's place on this page, no lifts */
			var h=window.innerHeight||0;
			if(wa0&&!box.classList.contains('is-clear')&&!box.classList.contains('is-cone')&&!box.classList.contains('is-typing')){var t0=wa0.getBoundingClientRect();if(t0.height>0)box.setAttribute('data-rest',Math.round(h-t0.top));}
			var lift=mq.matches?stageHit(h):0,cone=coneHit(h),clash=subs.some(function(el){var r=el.getBoundingClientRect();return r.height>0&&r.bottom>h-110&&r.top<h;})||lift>0;
			if(cone>lift){lift=cone;}
			if(lift>0){box.style.setProperty('--nlcta-lift',lift+'px');}else{box.style.removeProperty('--nlcta-lift');}
			box.classList.toggle('is-clear',mq.matches&&clash);
			box.classList.toggle('is-cone',cone>0);
		};
		var ask=function(){if(!tick){tick=true;window.requestAnimationFrame(fit);}};
		window.addEventListener('scroll',ask,{passive:true});
		window.addEventListener('resize',ask);
		// P7.1 (1.72.370): measure again once the page has loaded (fonts, the first picture, a stage's own bar): on a phone's first screen the pill sat on the controls until the first scroll
		window.addEventListener('load',ask);
		// P9a (1.72.371): and twice more after it: a stage paints its own buttons after the page's load (DUO's card on the first screen)
		window.addEventListener('load',function(){setTimeout(ask,1200);setTimeout(ask,3000);});
		if(mq.addEventListener){mq.addEventListener('change',fit);}
		// the stage's card opens and closes without a scroll: look again after a tap on the stage and on its floor events
		document.addEventListener('click',function(e){if(e.target&&e.target.closest&&e.target.closest('#nlps,#nlps-pick,.nlps-steps,#nlps-view-cta')){setTimeout(ask,350);}},true);
		['nl:floor','nl:facing'].forEach(function(n){window.addEventListener(n,function(){setTimeout(ask,350);setTimeout(ask,1100);});});
		fit();
		var typing=function(t){return t&&t.matches&&t.matches('textarea,select,input:not([type=checkbox]):not([type=radio]):not([type=button]):not([type=submit]):not([type=hidden])');};
		document.addEventListener('focusin',function(e){if(typing(e.target)){clearTimeout(back);box.classList.add('is-typing');}});
		document.addEventListener('focusout',function(e){if(typing(e.target)){clearTimeout(back);back=setTimeout(function(){box.classList.remove('is-typing');fit();},700);}});
	}
})();
</script>
	<?php
}, 90 );

/* Public lead REST endpoint - kept (used by other modules: claim-prompt, AI concierge, etc.) */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/lead', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( $req ) {
			$p = $req->get_json_params() ?: array();
			$name  = sanitize_text_field( (string) ( $p['name'] ?? '' ) );
			$phone = preg_replace( '/[^0-9+]/', '', (string) ( $p['phone'] ?? '' ) );
			$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
			$goal  = sanitize_text_field( (string) ( $p['goal'] ?? ( $p['topic'] ?? '' ) ) );
			$msg   = sanitize_textarea_field( (string) ( $p['message'] ?? '' ) );
			$src   = sanitize_text_field( (string) ( $p['source'] ?? '' ) );
			$requested_card_id = absint( $p['card_id'] ?? ( $p['lead_card_id'] ?? 0 ) );
			$card_id = $requested_card_id;
			/* A private journey lead is part of the password-gated surface.  REST
			 * requests carry the same wp-postpass cookie as the unlocked page; an
			 * anonymous caller that only guesses the post ID must fail before the
			 * honeypot, rate counter, insert, routing or notification paths. */
			$is_private_lab = $card_id > 0 && 'nadlan_project' === get_post_type( $card_id ) && (
				( function_exists( 'nadlan_unit_journey_is_private_lab' )
					&& nadlan_unit_journey_is_private_lab( $card_id ) )
				|| 'private-unit-journey-v2' === (string) get_post_meta( $card_id, '_nadlan_private_unit_journey', true )
			);
			if ( $is_private_lab ) {
				$post = get_post( $card_id );
				$has_password = $post instanceof WP_Post && '' !== (string) $post->post_password;
				if ( ! $has_password || post_password_required( $card_id ) ) {
					return new WP_Error( 'not_found', 'Not found.', array( 'status' => 404 ) );
				}
			}
			if ( function_exists( 'nadlan_config_valid_lead_card_id' ) ) {
				$card_id = nadlan_config_valid_lead_card_id( $card_id );
			} else {
				$post = $card_id ? get_post( $card_id ) : null;
				if ( ! $post || ! in_array( $post->post_type, array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ), true ) ) {
					$card_id = 0;
				}
			}
			/* A supplied but invalid card uses the same opaque response as a locked
			 * private card. This avoids turning the lead endpoint into an ID oracle;
			 * truly generic leads still omit card_id and continue normally. */
			if ( $requested_card_id > 0 && $card_id <= 0 ) {
				return new WP_Error( 'not_found', 'Not found.', array( 'status' => 404 ) );
			}
			$hp    = (string) ( $p['company'] ?? '' );
			if ( $hp !== '' ) {
				return new WP_Error( 'spam', 'Request rejected.', array( 'status' => 400 ) );
			}
			if ( ! $name || ( ! $phone && ! $email ) ) {
				return new WP_Error( 'invalid', 'נדרשים שם וטלפון או אימייל.', array( 'status' => 400 ) );
			}
			if ( $src === 'showroom_unit_journey_v2' && empty( $p['consent'] ) ) {
				return new WP_Error( 'consent_required', 'נדרשת הסכמה לתנאי הפנייה.', array( 'status' => 400 ) );
			}
			$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
			$tk = 'nadlan_lead_rl_' . md5( $ip );
			$ct = (int) get_transient( $tk );
			if ( $ct >= 8 ) {
				return new WP_Error( 'rate', 'יותר מדי בקשות.', array( 'status' => 429 ) );
			}
			set_transient( $tk, $ct + 1, HOUR_IN_SECONDS );
			$lead_payload = array(
				'name'              => $name,
				'phone'             => $phone,
				'email'             => $email,
				'goal'              => $goal,
				'message'           => $msg,
				'source'            => $src,
				'budget'            => sanitize_text_field( (string) ( $p['budget'] ?? '' ) ),
				'timeline'          => sanitize_text_field( (string) ( $p['timeline'] ?? '' ) ),
				'unit'              => sanitize_text_field( (string) ( $p['unit'] ?? '' ) ),
				'floor'             => isset( $p['floor'] ) ? (int) $p['floor'] : '',
				'rooms'             => sanitize_text_field( (string) ( $p['rooms'] ?? '' ) ),
				'sqm'               => sanitize_text_field( (string) ( $p['sqm'] ?? '' ) ),
				'building'          => sanitize_text_field( (string) ( $p['building'] ?? '' ) ),
				'availability'      => sanitize_text_field( (string) ( $p['availability'] ?? '' ) ),
				'market_note'       => sanitize_textarea_field( (string) ( $p['market_note'] ?? '' ) ),
				'advisor'           => sanitize_key( (string) ( $p['advisor'] ?? '' ) ),
				'purchase_intent'   => ! empty( $p['purchase_intent'] ) ? 1 : '',
				'reservation_state' => sanitize_key( (string) ( $p['reservation_state'] ?? '' ) ),
				'view_bearing'      => isset( $p['view_bearing'] ) ? (float) $p['view_bearing'] : '',
				'view_altitude_m'   => isset( $p['view_altitude_m'] ) ? (float) $p['view_altitude_m'] : '',
				'project_slug'      => sanitize_title( (string) ( $p['project_slug'] ?? '' ) ),
				'project_title'     => sanitize_text_field( (string) ( $p['project_title'] ?? '' ) ),
				'project_wp_id'     => absint( $p['project_wp_id'] ?? ( $p['wp_id'] ?? 0 ) ),
				'direction'         => sanitize_key( (string) ( $p['direction'] ?? '' ) ),
				'unit_status'       => sanitize_key( (string) ( $p['status'] ?? '' ) ),
				'consent'           => ! empty( $p['consent'] ) ? 1 : '',
				'consent_text'      => sanitize_textarea_field( (string) ( $p['consent_text'] ?? '' ) ),
				'consent_recorded'  => ! empty( $p['consent'] ) ? current_time( 'mysql', true ) : '',
			);
			if ( function_exists( 'nadlan_lead_e2e_enabled' ) && nadlan_lead_e2e_enabled() && function_exists( 'nadlan_lead_e2e_capture' ) ) {
				$cap = nadlan_lead_e2e_capture( $lead_payload, $card_id, 'rest' );
				// the test-mode path gets the same key, for the lead as persisted (Codex LEAD-E2E-UNIT-CONTRACT)
				if ( is_array( $cap ) && ! empty( $cap['lead_id'] ) && function_exists( 'nadlan_rfp_lead_key_for' ) ) {
					$k = nadlan_rfp_lead_key_for( $cap['lead_id'], $lead_payload['project_slug'], $lead_payload['unit'] );
					if ( '' !== $k ) { $cap['lead_key'] = $k; }
				}
				return $cap;
			}
			$lid = wp_insert_post( array(
				'post_type'    => 'nadlan_lead',
				'post_status'  => 'private',
				'post_title'   => $name . ' - ' . ( $goal ?: 'general' ) . ' - ' . current_time( 'Y-m-d H:i' ),
				'post_content' => $msg,
			), true );
			if ( is_wp_error( $lid ) ) { return $lid; }
			update_post_meta( $lid, 'name', $name );
			update_post_meta( $lid, 'phone', $phone );
			if ( $email ) { update_post_meta( $lid, 'email', $email ); }
			update_post_meta( $lid, 'goal', $goal );
			if ( $src ) { update_post_meta( $lid, 'utm_source', $src ); }
			if ( $card_id ) { update_post_meta( $lid, 'lead_card_id', $card_id ); }
			foreach ( array( 'budget', 'timeline', 'unit', 'floor', 'rooms', 'sqm', 'building', 'availability', 'market_note', 'advisor', 'purchase_intent', 'reservation_state', 'view_bearing', 'view_altitude_m', 'project_slug', 'project_title', 'project_wp_id', 'direction', 'unit_status', 'consent', 'consent_text', 'consent_recorded' ) as $extra_key ) {
				if ( isset( $lead_payload[ $extra_key ] ) && $lead_payload[ $extra_key ] !== '' ) {
					update_post_meta( $lid, $extra_key, $lead_payload[ $extra_key ] );
				}
			}
			if ( function_exists( 'nadlan_lead_route' ) ) {
				nadlan_lead_route( $lid, $card_id, $lead_payload, 'rest' );
			}
			if ( function_exists( 'nadlan_offers_capture_nonbinding_inquiry' ) && ( $lead_payload['reservation_state'] ?? '' ) === 'non_binding_inquiry' ) {
				nadlan_offers_capture_nonbinding_inquiry( $lid, $card_id, $lead_payload );
			}
			$admin = get_option( 'admin_email' );
			if ( $admin ) {
				$body  = "ליד חדש מהאתר\n\nשם: $name\nטלפון: $phone\nאימייל: $email\nנושא: $goal\nמקור: $src\n\nהודעה: $msg\n\n";
				$body .= "ניהול: " . admin_url( 'post.php?post=' . $lid . '&action=edit' );
				wp_mail( $admin, '[נדלן] ליד חדש - ' . $name, $body );
			}
			$out = array( 'ok' => true, 'lead_id' => $lid );
			// UnitDesignRequest v102 (inc/rfp.php): a lead that names a project and a unit gets a key; only its holder can attach
			// the request document to it (a bare lead id no longer links anything)
			if ( function_exists( 'nadlan_rfp_lead_key_for' ) ) {
				$k = nadlan_rfp_lead_key_for( $lid, $lead_payload['project_slug'], $lead_payload['unit'] );
				if ( '' !== $k ) { $out['lead_key'] = $k; }
			}
			return $out;
		},
	) );
} );

/* Settings page - kept (for the WhatsApp number) */
add_action( 'admin_menu', function () {
	add_options_page( 'NadLan CTA + WhatsApp', 'NadLan CTA', 'manage_options', 'nadlan-cta', function () {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( ! empty( $_POST['nadlan_cta_save'] ) && check_admin_referer( 'nadlan_cta_save' ) ) {
			update_option( 'nadlan_owner_whatsapp', preg_replace( '/[^0-9+]/', '', sanitize_text_field( wp_unslash( $_POST['wa'] ?? '' ) ) ) );
			$new_secret = sanitize_text_field( wp_unslash( $_POST['wa_ingest_secret'] ?? '' ) );
			if ( ! empty( $_POST['clear_wa_ingest_secret'] ) ) {
				delete_option( 'nadlan_wa_ingest_secret' );
			} elseif ( $new_secret !== '' ) {
				update_option( 'nadlan_wa_ingest_secret', $new_secret, false );
			}
			echo '<div class="notice notice-success"><p>נשמר.</p></div>';
		}
		$wa = (string) get_option( 'nadlan_owner_whatsapp', '' );
		$wa_secret_set = (string) get_option( 'nadlan_wa_ingest_secret', '' ) !== '';
		echo '<div class="wrap" style="direction:rtl;font-family:Heebo,sans-serif"><h1>NadLan CTA + WhatsApp</h1>';
		echo '<p style="background:#fff;border-inline-start:4px solid #DC2626;padding:10px 14px;color:#5a5a5a">הסטיקי-בר וה-pop-up בוטלו ב-v1.40.3 לבקשת הבעלים. נשאר רק כפתור WhatsApp צף.</p>';
		echo '<form method="post">';
		wp_nonce_field( 'nadlan_cta_save' );
		echo '<table class="form-table"><tr><th>WhatsApp Number (E.164)</th><td><input type="text" name="wa" value="' . esc_attr( $wa ) . '" style="width:280px" placeholder="972501234567"> <br><small>מספר טלפון להפנייה ל-WhatsApp. ריק = הכפתור יוסתר.</small></td></tr>';
		echo '<tr><th>WhatsApp lead ingest secret</th><td><input type="password" name="wa_ingest_secret" value="" style="width:360px" placeholder="' . esc_attr( $wa_secret_set ? 'סוד שמור. הדביקו חדש רק אם מחליפים.' : 'הגדירו סוד ל-/wp-json/nadlan/v1/wa-lead' ) . '"> <br><small>משמש ל-iPhone Shortcut, Android share או Cloud API relay. הסוד לא מוצג במסך ולא נשמר כ-autoload.</small> <br><label><input type="checkbox" name="clear_wa_ingest_secret" value="1"> מחק סוד קיים</label></td></tr></table>';
		echo '<p class="submit"><button type="submit" name="nadlan_cta_save" value="1" class="button-primary">שמור</button></p></form></div>';
	} );
} );
