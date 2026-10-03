'use strict';
// "Advertise with us" entry points on every cy-prus page (portal research 3.10.2026): top menu, footer, a one-line
// WhatsApp invite on project pages, and a band at the end of the project catalogues. Hebrew by default; English for
// ?lang=en and the other non-Hebrew languages. No prices, fees or paid prominence anywhere.
(function(){
 const C=window.CYPX_ADV||{};if(!C.url)return;
 const q=new URLSearchParams(location.search).get('lang')||'',html=(document.documentElement.lang||'').toLowerCase();
 const en=q?q!=='he':!html.startsWith('he');
 const T=en?C.en:C.he,href=C.url+(en?'?lang=en':'');
 const link=(cls,text,to)=>{const a=document.createElement('a');a.className=cls;a.href=to||href;a.textContent=text;return a;};
 const here=location.pathname.replace(/\/+$/,'/')===new URL(C.url,location.href).pathname;
 // Top menu: a quiet outlined item after the guides, before the buyers' "find a property" button.
 const links=document.querySelector('.cy-nav .cy-nav-links');
 if(links&&!links.querySelector('.cyadv-nav')){const a=link('cyadv-nav',T.nav);if(here)a.setAttribute('aria-current','page');const cta=links.querySelector('.cy-nav-cta');cta?links.insertBefore(a,cta):links.append(a);}
 // Footer: the CY-PRUS column, right above its WhatsApp line.
 const cols=document.querySelectorAll('.cy-footer .cy-footer-col');
 if(cols.length&&!document.querySelector('.cyadv-foot')){const col=cols[cols.length-1],w=col.querySelector('a[href*="wa.me"]'),a=link('cyadv-foot',T.nav);w?col.insertBefore(a,w):col.append(a);}
 // Project pages: one line under the page's WhatsApp card; it opens WhatsApp with this project already named.
 const main=document.querySelector('#atlas-main.atlas-view-place'),card=main&&main.querySelector('.atlas-wa-wrap');
 if(card&&/\/[a-z]+_project\/[^/]+\/?$/.test(location.pathname)&&!document.querySelector('.cyadv-line')){
  const name=((main.querySelector('h1')||{}).textContent||'').trim();
  let city='';main.querySelectorAll('.atlas-facts dt').forEach(dt=>{if(/מחוז|District/i.test(dt.textContent)){const dd=dt.nextElementSibling;if(dd)city=dd.textContent.trim();}});
  const page=location.origin+location.pathname+(en?'?lang=en':'');
  const msg=en?['Hello, I came from the CY-PRUS site.','I am writing on behalf of the '+name+' project'+(city?' in '+city:'')+' and would like to update and complete its details on the site.',page]
             :['שלום, הגעתי מהאתר CY-PRUS.','פונה מטעם הפרויקט '+name+(city?' ב'+city:'')+', ואשמח לעדכן ולהשלים את הפרטים שלו באתר.',page];
  const p=document.createElement('p');p.className='cyadv-line';p.append(T.lineQ+' ');
  const a=link('',T.lineA,'https://wa.me/'+C.wa+'?text='+encodeURIComponent(msg.join('\n')));a.target='_blank';a.rel='noopener';p.append(a);card.after(p);
 }
 // Catalogues: a soft band at the end of the district project hubs and of the map search.
 const hub=location.pathname.match(/^\/(limassol|paphos|larnaca)\/[a-z]+_project\/$/),browse=/^\/browse\/$/.test(location.pathname);
 if((hub||browse)&&!document.querySelector('.cyadv-band')){
  const host=document.querySelector('#atlas-main')||document.querySelector('.wp-block-post-content');
  if(host){const d=hub?T.districts[hub[1]]:'';const b=document.createElement('aside');b.className='cyadv-band';
   const t=document.createElement('p');const s=document.createElement('strong');s.textContent=d?T.bandQ.replace('{d}',d):T.bandQAny;t.append(s,' '+T.band);
   b.append(t,link('cyadv-band-link',T.nav));host.append(b);}
 }
})();
