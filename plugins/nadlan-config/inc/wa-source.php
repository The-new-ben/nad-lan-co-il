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
		if(href.indexOf("%D7%9E%D7%A7%D7%95%D7%A8%3A")>-1||href.indexOf("מקור:")>-1)return; // already stamped
		var title=(document.title||"").split("|")[0].trim().slice(0,70);
		var stamp="\n\nמקור: "+title+"\n"+location.origin+location.pathname+location.search;
		try{
			var u=new URL(href,location.origin);
			var t=u.searchParams.get("text")||"";
			u.searchParams.set("text",(t?t:"")+stamp);
			a.setAttribute("href",u.toString());
		}catch(err){
			var sep=href.indexOf("?")>-1?"&":"?";
			if(href.indexOf("text=")===-1){a.setAttribute("href",href+sep+"text="+encodeURIComponent(stamp))}
		}
	},true);
})();
</script>
	<?php
}, 60 );
