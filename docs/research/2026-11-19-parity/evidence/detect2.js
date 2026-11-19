(function(){var Q=function(s){return document.querySelector(s)};var A=function(s){return [].slice.call(document.querySelectorAll(s))};
var html=document.documentElement.outerHTML;
var inMain=function(e){return !e.closest('header,footer,nav.nlhp-nav,.nlhp-mega,.wp-block-template-part')};
var acts=A('button,a').filter(inMain);var txt=function(e){return (e.innerText||e.textContent||'').trim()};
var has360=acts.some(function(e){return /360/.test(txt(e))});
var vids=A('video').map(function(v){return (v.currentSrc||v.getAttribute('src')||(v.querySelector('source')||{}).src||'')}).filter(Boolean);
return {u:location.pathname, lang:document.documentElement.lang, status:document.title.slice(0,60),
tower: !!(Q('[data-nlps-step]')||Q('script[src*="project-stage/"][src*="stage"]')||/project-stage\/[a-z]+\/stage\.js/.test(html)),
towerDir:(html.match(/project-stage\/([a-z0-9-]+)\/(stage|poster)/)||[])[1]||'',
floorView: !!(Q('[data-nlps-step="view"]')||Q('[data-nlps-ev="hero-pick"]')),
designerStep: !!Q('[data-nlps-step="design"]'),
designerLink: A('a[href*="tour/designer"]').filter(inMain).length,
designerProj: A('a[href*="tour/designer/?"]').map(function(a){return a.getAttribute('href')}).slice(0,2),
call: A('a[href="#nlsch"],.nlps-hero__video,a[href*="room="],[data-nl-call]').filter(inMain).length,
callBooking: !!Q('#nlsch'),
basket: A('[class*="basket"],[data-nlps-step="basket"]').length,
alert: !!Q('#nlnu.nlpa-root,.nlpa-root'),
film: !!(Q('.nlps-hero__film,#nlfilm,script#nadlan-ps-film'))||vids.length>0, vids:vids.map(function(v){return v.split('/').pop().slice(0,50)}).slice(0,2),
v360: has360, surr: !!(Q('.nlpjx-maplayers,.nlcp-surr,[data-layer="schools"]')),
engine: !!Q('.nlse,[class*="nlse-"]'), einsteinLab: /einstein-lab/.test(html), kikar: /hamedina\//.test(html),
h1:(Q('h1')||{}).innerText||''}})()
