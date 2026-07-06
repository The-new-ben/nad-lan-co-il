<?php
/**
 * nadlan-config - First-party accessibility widget + statement (owner 2026-07-07:
 * "the accessibility icon is not showing anywhere, bundled under the plus").
 *
 * No third-party a11y plugin exists on the site, and Israeli regulation
 * (תקנות שוויון זכויות לאנשים עם מוגבלות, תקן 5568 / WCAG 2.0 AA) requires a
 * visible accessibility control and a statement page. This module ships both:
 * a standalone, always-visible button (NOT bundled in the floating CTA
 * cluster) opening a panel of real adjustments, each applied as an <html>
 * class and persisted in localStorage; plus a link to the statement page.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'wp_footer', function () {
	?>
<div id="nla11y" dir="rtl">
	<button type="button" id="nla11y-btn" aria-expanded="false" aria-controls="nla11y-panel" aria-label="תפריט נגישות" title="נגישות">
		<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="4.4" r="2"/><path d="M4.5 8.2c5 1.4 10 1.4 15 0M12 9.5v4.2m0 0-3.2 6m3.2-6 3.2 6"/></svg>
	</button>
	<div id="nla11y-panel" role="dialog" aria-label="הגדרות נגישות" hidden>
		<div class="nla11y-head">נגישות<button type="button" id="nla11y-x" aria-label="סגירה">✕</button></div>
		<button type="button" data-k="fontup">הגדלת טקסט</button>
		<button type="button" data-k="contrast">ניגודיות גבוהה</button>
		<button type="button" data-k="links">הדגשת קישורים</button>
		<button type="button" data-k="readable">גופן קריא</button>
		<button type="button" data-k="stopmotion">עצירת אנימציות</button>
		<button type="button" id="nla11y-reset">איפוס</button>
		<a href="<?php echo esc_url( home_url( '/accessibility-statement/' ) ); ?>">הצהרת נגישות</a>
	</div>
</div>
<style>
#nla11y{position:fixed;top:50%;transform:translateY(-50%);<?php echo is_rtl() ? 'right' : 'left'; ?>:14px;z-index:99998;font-family:Heebo,system-ui,sans-serif}
#nla11y-btn{width:52px;height:52px;border-radius:50%;background:#14130F;color:#E9D9A8;border:1px solid #9C7A3C;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px -10px rgba(27,26,23,.55)}
#nla11y-btn:hover{background:#2A251B}
#nla11y-btn:focus-visible,#nla11y-panel button:focus-visible,#nla11y-panel a:focus-visible{outline:3px solid #C2563A;outline-offset:2px}
#nla11y-panel{position:absolute;top:60px;right:0;width:218px;background:#FAF7F1;border:1px solid #D6C189;border-radius:14px;padding:10px;box-shadow:0 22px 48px -20px rgba(27,26,23,.5)}
.nla11y-head{display:flex;justify-content:space-between;align-items:center;font:700 15px/1 Heebo;color:#1B1A17;padding:4px 4px 10px}
#nla11y-x{background:none;border:0;font-size:14px;cursor:pointer;color:#6D665C;padding:4px}
#nla11y-panel>button{display:block;width:100%;text-align:right;background:#fff;border:1px solid #E2DCD0;border-radius:9px;font:500 13.5px/1 Heebo;color:#1B1A17;padding:10px 12px;margin:5px 0;cursor:pointer}
#nla11y-panel>button[aria-pressed="true"]{border-color:#9C7A3C;background:#F3EEE3;font-weight:700}
#nla11y-panel>a{display:block;text-align:center;font:600 12.5px/1 Heebo;color:#9C7A3C;padding:9px 0 4px;text-decoration:underline}
html.nla11y-fontup{font-size:115%}
html.nla11y-fontup body{font-size:1.06em}
html.nla11y-contrast body{background:#fff!important;color:#000!important}
html.nla11y-contrast body :is(p,li,h1,h2,h3,h4,span,td,th,label,figcaption){color:#000!important}
html.nla11y-contrast body :is(a,a *){color:#0000C7!important}
html.nla11y-links body a{text-decoration:underline!important;background:#FFF3C4;color:#1B1A17!important}
html.nla11y-readable body,html.nla11y-readable body *{font-family:Arial,Helvetica,sans-serif!important}
html.nla11y-stopmotion *,html.nla11y-stopmotion *::before,html.nla11y-stopmotion *::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}

</style>
<script>
(function(){
	var KEYS=["fontup","contrast","links","readable","stopmotion"],
		btn=document.getElementById("nla11y-btn"),
		panel=document.getElementById("nla11y-panel"),
		saved={};
	try{saved=JSON.parse(localStorage.getItem("nla11y")||"{}")}catch(e){}
	function apply(){
		KEYS.forEach(function(k){
			document.documentElement.classList.toggle("nla11y-"+k,!!saved[k]);
			var b=panel.querySelector('[data-k="'+k+'"]');
			if(b)b.setAttribute("aria-pressed",saved[k]?"true":"false");
		});
		try{localStorage.setItem("nla11y",JSON.stringify(saved))}catch(e){}
	}
	btn.addEventListener("click",function(){
		var open=panel.hasAttribute("hidden");
		if(open){panel.removeAttribute("hidden")}else{panel.setAttribute("hidden","")}
		btn.setAttribute("aria-expanded",open?"true":"false");
	});
	document.getElementById("nla11y-x").addEventListener("click",function(){panel.setAttribute("hidden","");btn.setAttribute("aria-expanded","false");btn.focus()});
	panel.querySelectorAll("[data-k]").forEach(function(b){
		b.addEventListener("click",function(){saved[b.dataset.k]=!saved[b.dataset.k];apply()});
	});
	document.getElementById("nla11y-reset").addEventListener("click",function(){saved={};apply()});
	document.addEventListener("keydown",function(e){if(e.key==="Escape"&&!panel.hasAttribute("hidden")){panel.setAttribute("hidden","");btn.setAttribute("aria-expanded","false");btn.focus()}});
	apply();
})();
</script>
	<?php
}, 60 );
