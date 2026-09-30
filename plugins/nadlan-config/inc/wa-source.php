<?php
/**
 * nadlan-config - WHATSAPP SOURCE TRACKING (owner order 2026-07-12).
 *
 * Problem: WhatsApp inquiries arrive with no clue which page the visitor
 * came from - the owner cannot read intent or see which pages convert.
 * The wa.me deep link carries context only through its `text` parameter,
 * so we stamp it there.
 *
 * ONE site-wide interceptor (covers plugin CTAs, theme buttons, everything):
 * on click of any wa.me link that targets a PHONE NUMBER (wa.me/9725... =
 * a message to the business), append a source line with the page title +
 * URL to the prefilled text. Share-to-a-friend links (wa.me/?text=..., no
 * number) are left untouched - stamping those would spam users' friends.
 * The stamp is applied at click time so SPAs/tabs always carry the CURRENT
 * page, and it is idempotent (never doubles).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'wp_footer', function () {
	?>
<script id="nadlan-wa-source">
(function(){
	if(window.nadlanWaSrc)return;window.nadlanWaSrc=1;
	document.addEventListener("click",function(e){
		var a=e.target&&e.target.closest&&e.target.closest('a[href*="wa.me/"],a[href*="api.whatsapp.com/send"]');
		if(!a)return;
		var href=a.getAttribute("href")||"";
		// only messages TO a number (the business); leave share links alone
		var toNumber=/wa\.me\/\d{6,}/.test(href)||/api\.whatsapp\.com\/send.*phone=\d{6,}/.test(href);
		if(!toNumber)return;
		/* V8: the source label follows the page language, and idempotence
		   recognises every variant (raw + URL-encoded) */
		var labels=["מקור","Source","Источник","المصدر"];
		var stamped=labels.some(function(s){return href.indexOf(s+":")>-1||href.indexOf(encodeURIComponent(s+":"))>-1});
		if(stamped)return;
		/* v103.1 (30.9.2026, owner): one tap, zero friction, and the message says where the visitor came from in a SHORT line:
		   the page's own name (its h1), what kind of page it is, the floor chosen on a project stage, and a link only when it is
		   short and readable (a Hebrew address becomes a long %-string, so it is left out). On a broker's or an owner's page
		   the site bar's message says the listing is theirs, never as if the site owned it. */
		var L=(document.documentElement.lang||"he").slice(0,2);
		var W=({he:{s:"מקור",pr:"פרויקט",li:"נכס",bl:"מודעה של מתווך",bs:"אתר של מתווך",pro:"איש מקצוע",fl:"קומה"},
			en:{s:"Source",pr:"project",li:"listing",bl:"a broker's listing",bs:"a broker's site",pro:"professional",fl:"floor"},
			fr:{s:"Source",pr:"projet",li:"bien",bl:"annonce d'un agent",bs:"site d'un agent",pro:"professionnel",fl:"étage"},
			ru:{s:"Источник",pr:"проект",li:"объект",bl:"объявление брокера",bs:"сайт брокера",pro:"специалист",fl:"этаж"},
			ar:{s:"المصدر",pr:"مشروع",li:"عقار",bl:"إعلان وسيط",bs:"موقع وسيط",pro:"مهني",fl:"طابق"}})[L]||null;
		if(!W){W={s:"מקור",pr:"פרויקט",li:"נכס",bl:"מודעה של מתווך",bs:"אתר של מתווך",pro:"איש מקצוע",fl:"קומה"};}
		var SRC=W.s,bc=document.body.className||"",own=a.matches&&a.matches(".nlcta-wa");
		var h1=document.querySelector("h1");
		var title=((h1&&h1.textContent)||(document.title||"").split("|")[0]).replace(/\s+/g," ").trim().slice(0,60);
		var kind=own&&document.querySelector(".nlx")?W.bl:own&&document.querySelector(".nlb")?W.bs:/\bsingle-nadlan_project\b/.test(bc)?W.pr:/\bsingle-nadlan_property\b/.test(bc)?W.li:/\bsingle-nadlan_professional\b/.test(bc)?W.pro:"";
		/* P7 (30.9.2026): the facing chosen on the stage joins the floor on the same line ("קומה 30 · מגדל C · מערבה"); only with
		   a floor, and short (the stages' own words: a sector such as "לכיוון הים", or the world's "מערבה") */
		var pk=window.__nlpsPick,fc=(pk&&typeof pk.facing==="string")?pk.facing.replace(/\s+/g," ").trim().slice(0,40):"",
			fl=(pk&&pk.floor!=null&&pk.floor!=="")?" · "+W.fl+" "+pk.floor+(fc?" · "+fc:""):"";
		var path=location.pathname,link=(path.length<=45&&/^[A-Za-z0-9\/._-]*$/.test(path))?"\n"+location.host+path:"";
		var stamp="\n\n"+SRC+": "+title+(kind?" · "+kind:"")+fl+link;
		try{
			var u=new URL(href,location.origin);
			var t=u.searchParams.get("text")||"";
			u.searchParams.delete("text");
			/* v71: encodeURIComponent keeps spaces as %20; URLSearchParams wrote "+", which some phones show as a plus sign */
			var base=u.toString();
			a.setAttribute("href",base+(base.indexOf("?")>-1?"&":"?")+"text="+encodeURIComponent((t?t:"")+stamp));
		}catch(err){
			var sep=href.indexOf("?")>-1?"&":"?";
			if(href.indexOf("text=")===-1){a.setAttribute("href",href+sep+"text="+encodeURIComponent(stamp))}
		}
	},true);
})();
</script>
	<?php
}, 60 );
