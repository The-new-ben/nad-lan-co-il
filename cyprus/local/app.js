'use strict';
// Five-language contract, two implemented locales. No silent fake translations.
const LOCALES={he:{dir:'rtl',enabled:true},en:{dir:'ltr',enabled:true},fr:{dir:'ltr',enabled:false},ru:{dir:'ltr',enabled:false},ar:{dir:'rtl',enabled:false}};
const COPY={he:{explore:'לבחירת בית',plans:'תוכניות הבית',compare:'השוואת שטחים',intro:'ארבעה בתים בשני זוגות, ארבעה חדרי שינה בכל בית. בחרו בית בתוכנית המגרש, היכנסו לתוכניות הקומות שלו והשוו בין השטחים.',exteriorNote:'הדמיית האדריכל: שני זוגות הבתים מהרחוב.',exteriorAlt:'הדמיית אדריכל של בתי DUNE: שני זוגות בתים לבנים בני שתי קומות עם מסגרות עץ',collection:'הבתים',choose:'מה מתאים לכם?',selectionNote:'בחירת בית לצפייה בפרטים, לא אישור זמינות.',sitePlan:'תוכנית המגרש',siteHint:'לחצו על בית בתוכנית או ברשימה. הבית שבחרתם מודגש.',siteAlt:'תוכנית המגרש: ארבעה בתים בשני זוגות, A01 ו-A02 משמאל, B01 ו-B02 מימין',residence:'הבית שבחרתם',save:'הוספה להשוואה',saved:'נוסף להשוואה',prepare:'הכנת פרטים לשיחה',areaNote:'השטחים לפי חוברת הפרויקט.',inside:'בתוך הבית',planTitle:'תוכניות הקומות',ground:'קומת קרקע',upper:'קומה עליונה',level:'קומה',expand:'הגדלת התוכנית',planNote:'תוכנית שיווקית להמחשה, ללא קנה מידה. הבית השכן מוצג בגוון בהיר.',planAlt:'תוכנית {level} של הבתים {pair}01 ו-{pair}02',roomExplore:'החדרים בקומה',roomPick:'בחרו חדר כדי לראות אותו בתוכנית.',roomNoSize:'מידות החדרים אינן מופיעות בתוכנית.',kitchen:'מטבח',living:'סלון',dining:'פינת אוכל',terrace:'מרפסת',stairs:'מדרגות',bed:'חדר שינה {n}',close:'סגירה',zoomOut:'הקטנה',zoomIn:'הגדלה',reset:'איפוס',zoomHint:'הגדילו וגררו כדי לנוע בתוכנית.',viewPlans:'לתוכניות הבית',sideBySide:'מבט אחד על ההבדלים',comparisonTitle:'הבחירה שלכם, זה לצד זה',footer:'תצוגה מקומית. אין שיגור פנייה או הזמנה.',beds:'חדרי שינה',baths:'חדרי רחצה',interior:'שטח מקורה',terraceArea:'מרפסות מקורות',parking:'חניה מקורה',totalCovered:'סך שטח מקורה',sqm:'מ״ר',remove:'הסרה',empty:'בחרו בית והוסיפו אותו להשוואה.',prepareBody:'פרטי הבית שבחרתם מרוכזים כאן להמשך השיחה.',selectedDetails:'פרטי הבחירה',copy:'העתקת הפרטים',copied:'הפרטים הועתקו',noSend:'לא נשלחת פנייה מהתצוגה המקומית.',count:'בתים בהשוואה',loadError:'נתוני הבתים לא נטענו. יש להפעיל את השרת המקומי.'},
 en:{explore:'Explore the residences',plans:'Floor plans',compare:'Compare areas',intro:'Four residences in two pairs, four bedrooms in each. Select a home on the site plan, step into its floor plans and compare the areas.',exteriorNote:'Architect’s visualisation: both pairs of homes from the street.',exteriorAlt:'Architect’s rendering of the DUNE residences: two pairs of white two-storey homes with timber frames',collection:'The collection',choose:'Find your fit.',selectionNote:'Explore a residence. Selection does not confirm availability.',sitePlan:'Site plan',siteHint:'Tap a home on the plan or in the list. Your selection is highlighted.',siteAlt:'Site plan: four homes in two pairs, A01 and A02 on the left, B01 and B02 on the right',residence:'Your selected residence',save:'Add to comparison',saved:'Added to comparison',prepare:'Prepare your enquiry',areaNote:'Areas from the project brochure.',inside:'Inside the home',planTitle:'Floor plans',ground:'Ground floor',upper:'Upper floor',level:'Floor',expand:'Enlarge plan',planNote:'Marketing plan for illustration, not to scale. The neighbouring home is shown faded.',planAlt:'{level} plan of homes {pair}01 and {pair}02',roomExplore:'Rooms on this floor',roomPick:'Select a room to see it on the plan.',roomNoSize:'Room dimensions are not shown on the plan.',kitchen:'Kitchen',living:'Living room',dining:'Dining',terrace:'Terrace',stairs:'Stairs',bed:'Bedroom {n}',close:'Close',zoomOut:'Zoom out',zoomIn:'Zoom in',reset:'Reset',zoomHint:'Zoom in and drag to move around the plan.',viewPlans:'View floor plans',sideBySide:'A closer look',comparisonTitle:'Your choices, side by side.',footer:'Local preview. No enquiry or reservation is sent.',beds:'Bedrooms',baths:'Bathrooms',interior:'Covered area',terraceArea:'Covered terraces',parking:'Covered parking',totalCovered:'Total covered area',sqm:'m²',remove:'Remove',empty:'Select a residence and add it to your comparison.',prepareBody:'Keep your selected residence details together for a conversation.',selectedDetails:'Your selection',copy:'Copy details',copied:'Details copied',noSend:'This local preview does not send an enquiry.',count:'residences compared',loadError:'The residence data did not load. Start the local server.'}};
const AREAS=['interior','terrace','parking'],LABEL={terrace:'terraceArea'},ZOOMS=[1,1.5,2,3,4];
const q=new URLSearchParams(location.search);
let data,lang=q.get('lang')==='en'?'en':'he',selected,level=q.get('level')==='upper'?'upper':'ground',room=null,saved=[],zoom=1;
const $=s=>document.querySelector(s),t=(k,v={})=>COPY[lang][k].replace(/\{(\w+)\}/g,(_,x)=>v[x]??''),e=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const lab=k=>t(LABEL[k]||k),unit=()=>data.units.find(x=>x.id===selected),sheet=()=>DUNE_PLANS.pairs[selected[0]][level];
const roomName=r=>r.kind==='bed'?t('bed',{n:r.number}):t(r.kind);
// Room points are drawn on the 01 half; the 02 home is the mirror image around the party wall.
const roomX=(r,s)=>selected.endsWith('02')?2*s.split-r.at[0]:r.at[0];
function toast(msg){const n=$('#toast');n.textContent=msg;n.classList.add('show');setTimeout(()=>n.classList.remove('show'),2000);}
function img(box,src,w,h,alt,eager){
 let i=box.querySelector('img');
 if(!i){i=new Image();i.decoding='async';i.onload=()=>box.classList.remove('loading');box.prepend(i);}
 if(i.getAttribute('src')!==src){box.classList.add('loading');i.loading=eager?'eager':'lazy';i.width=w;i.height=h;i.src=src;if(i.complete&&i.naturalWidth)box.classList.remove('loading');}
 i.alt=alt;return i;
}
function renderSite(){
 const s=DUNE_PLANS.site,box=$('#site-canvas');img(box,s.src,s.width,s.height,t('siteAlt'),true);
 let svg=box.querySelector('svg');if(!svg){svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox',`0 0 ${s.width} ${s.height}`);box.append(svg);}
 svg.innerHTML=Object.entries(s.units).map(([id,p])=>`<g class="site-unit" data-unit="${e(id)}" tabindex="0" role="button" aria-label="${e(id)}" aria-pressed="${id===selected}"><polygon points="${p.points}"/><text x="${p.label[0]}" y="${p.label[1]}">${e(id)}</text></g>`).join('');
}
function renderPlan(){
 const s=sheet(),box=$('#plan-canvas'),pair=selected[0],mirror=selected.endsWith('02');
 img(box,s.src,s.width,s.height,t('planAlt',{level:t(level),pair}));
 box.style.setProperty('--split',s.split*100+'%');box.dataset.side=mirror?'right':'left';
 // The whole floor stays inside one screen on a desktop; phones are width-bound anyway.
 box.style.maxWidth=`min(820px, calc((100vh - 250px) * ${(s.width/s.height).toFixed(3)}))`;
 box.querySelectorAll('.room-pin,.veil').forEach(n=>n.remove());
 box.insertAdjacentHTML('beforeend','<span class="veil" aria-hidden="true"></span>'+s.rooms.map((r,i)=>`<button class="room-pin" data-room="${r.id}" style="left:${(roomX(r,s)*100).toFixed(2)}%;top:${(r.at[1]*100).toFixed(2)}%" aria-label="${e(roomName(r))}" aria-pressed="${r.id===room}">${i+1}</button>`).join(''));
 $('#plan-unit').textContent=selected;
 document.querySelectorAll('[data-level]').forEach(n=>n.setAttribute('aria-pressed',String(n.dataset.level===level)));
 $('#room-buttons').innerHTML=s.rooms.map((r,i)=>`<button class="room-chip" data-room="${r.id}" aria-pressed="${r.id===room}"><span>${i+1}</span>${e(roomName(r))}</button>`).join('');
 const r=s.rooms.find(x=>x.id===room);
 $('#room-details').innerHTML=r?`<h3>${e(roomName(r))}</h3><p>${e(selected)} · ${e(t(level))}</p><p class="small">${e(t('roomNoSize'))}</p>`:`<p class="small">${e(t('roomPick'))}</p>`;
 // Warm the other floor of the same pair so switching floors is instant.
 const other=DUNE_PLANS.pairs[pair][level==='ground'?'upper':'ground'];if(!renderPlan.warm?.has(other.src)){(renderPlan.warm??=new Set).add(other.src);setTimeout(()=>{new Image().src=other.src;},1200);}
}
function render(){
 document.documentElement.lang=lang;document.documentElement.dir=LOCALES[lang].dir;
 document.querySelectorAll('[data-t]').forEach(n=>n.textContent=t(n.dataset.t));
 document.querySelectorAll('[data-label]').forEach(n=>n.setAttribute('aria-label',t(n.dataset.label)));
 document.querySelectorAll('[data-lang]').forEach(n=>n.setAttribute('aria-pressed',String(n.dataset.lang===lang)));
 $('#district').textContent=data.district;$('#exterior').alt=t('exteriorAlt');
 $('#units').innerHTML=data.units.map(u=>`<button class="unit" data-unit="${e(u.id)}" aria-pressed="${u.id===selected}"><strong>${e(u.id)}</strong><span>${u.interior} ${t('sqm')}</span></button>`).join('');
 const u=unit();$('#board-id').textContent=$('#detail-id').textContent=u.id;
 renderSite();
 $('#breakdown').innerHTML=AREAS.map(k=>`<div><b>${u[k]} <small>${t('sqm')}</small></b>${lab(k)}</div>`).join('');
 $('#specs').innerHTML=[['beds',u.bedrooms],['baths',u.bathrooms],['totalCovered',u.totalCovered],['terrace',u.terrace]].map(([k,v])=>`<div><b>${v}${['terrace','totalCovered'].includes(k)?` <small>${t('sqm')}</small>`:''}</b><span>${lab(k)}</span></div>`).join('');
 $('#save').textContent=t(saved.includes(selected)?'saved':'save');$('#save').setAttribute('aria-pressed',String(saved.includes(selected)));
 renderPlan();
 $('#count').textContent=saved.length+' '+t('count');
 $('#comparison-cards').innerHTML=saved.length?saved.map(id=>{let v=data.units.find(x=>x.id===id);return `<article class="compare-card"><h3>${e(id)}</h3><dl>${['interior','terrace','parking','totalCovered'].map(k=>`<div><dt>${lab(k)}</dt><dd>${v[k]} ${t('sqm')}</dd></div>`).join('')}</dl><button data-view="${e(id)}">${t('viewPlans')}</button><button data-remove="${e(id)}">${t('remove')}</button></article>`}).join(''):`<p class="empty">${t('empty')}</p>`;
 if($('#plan-dialog').open)fillLarge();
 const url=new URL(location);url.searchParams.set('lang',lang);url.searchParams.set('unit',selected);url.searchParams.set('level',level);history.replaceState(null,'',url);
}
function choose(id,from){
 if(id!==selected){selected=id;room=null;}render();
 const back=from?.closest('#site-canvas')?`#site-canvas [data-unit="${id}"]`:`#units [data-unit="${id}"]`;$(back)?.focus({preventScroll:true});
}
// The enlarged plan: fit the whole drawing at 100%, then zoom around the centre of the view.
function fillLarge(){
 const s=sheet();$('#large-plan-title').textContent=`${selected} · ${t(level)}`;
 const i=$('#large-plan'),f=$('#large-plan-frame');if(i.getAttribute('src')!==s.src){i.width=s.width;i.height=s.height;i.src=s.src;}i.alt=t('planAlt',{level:t(level),pair:selected[0]});
 f.style.setProperty('--split',s.split*100+'%');f.dataset.side=selected.endsWith('02')?'right':'left';
}
function setZoom(z){
 const box=$('#large-plan-scroll'),f=$('#large-plan-frame'),s=sheet();
 let cx=(box.scrollLeft+box.clientWidth/2)/Math.max(box.scrollWidth,1),cy=(box.scrollTop+box.clientHeight/2)/Math.max(box.scrollHeight,1);
 // Leaving the full view: zoom towards the chosen home, not the middle of the pair.
 if(zoom===1&&z>1){cx=selected.endsWith('02')?(1+s.split)/2:s.split/2;cy=.5;}
 zoom=z;const fit=Math.min(box.clientWidth,box.clientHeight*s.width/s.height);
 f.style.width=Math.round(fit*zoom)+'px';$('#zoom-value').textContent=Math.round(zoom*100)+'%';
 $('#zoom-out').disabled=zoom<=ZOOMS[0];$('#zoom-in').disabled=zoom>=ZOOMS.at(-1);box.classList.toggle('zoomed',zoom>1);
 box.scrollLeft=cx*box.scrollWidth-box.clientWidth/2;box.scrollTop=cy*box.scrollHeight-box.clientHeight/2;
}
function openLarge(){fillLarge();$('#plan-dialog').showModal();requestAnimationFrame(()=>setZoom(1));}
const step=d=>setZoom(ZOOMS[Math.min(ZOOMS.length-1,Math.max(0,ZOOMS.indexOf(zoom)+d))]);
document.addEventListener('click',event=>{const b=event.target.closest('button,[data-unit]');if(!data)return;
 if(!b){if(event.target.closest('#plan-canvas'))openLarge();return;}
 if(b.dataset.unit)choose(b.dataset.unit,b);
 if(b.dataset.lang){lang=b.dataset.lang;render();}
 if(b.dataset.level&&b.dataset.level!==level){level=b.dataset.level;room=null;render();}
 if(b.dataset.room){room=room===b.dataset.room?null:b.dataset.room;renderPlan();$(`#room-buttons [data-room="${b.dataset.room}"]`)?.focus({preventScroll:true});}
 if(b.dataset.view){choose(b.dataset.view);$('#plans').scrollIntoView({block:'start'});}
 if(b.dataset.remove){saved=saved.filter(x=>x!==b.dataset.remove);render();}
});
document.addEventListener('keydown',event=>{const g=event.target.closest?.('g[data-unit]');if(g&&(event.key==='Enter'||event.key===' ')){event.preventDefault();choose(g.dataset.unit,g);}});
$('#save').onclick=()=>{if(!saved.includes(selected))saved.push(selected);render();};
$('#prepare').onclick=()=>{const u=unit();$('#brief').value=[data.name,u.id,`${t('beds')}: ${u.bedrooms}`,...['interior','terrace','parking','totalCovered'].map(k=>`${lab(k)}: ${u[k]} ${t('sqm')}`)].join('\n');$('#conversation').showModal();};
$('#close').onclick=()=>$('#conversation').close();
$('#copy').onclick=async()=>{try{await navigator.clipboard.writeText($('#brief').value);toast(t('copied'));}catch{$('#brief').focus();$('#brief').select();}};
$('#expand-plan').onclick=openLarge;
$('#close-plan').onclick=()=>$('#plan-dialog').close();
$('#zoom-in').onclick=()=>step(1);$('#zoom-out').onclick=()=>step(-1);$('#zoom-reset').onclick=()=>setZoom(1);
$('#large-plan').addEventListener('load',()=>{if($('#plan-dialog').open)setZoom(zoom);});
addEventListener('resize',()=>{if($('#plan-dialog').open)setZoom(zoom);});
// Mouse drag pans the zoomed plan; touch keeps the browser's own scrolling.
{const box=$('#large-plan-scroll');let drag=null;
 box.addEventListener('pointerdown',ev=>{if(ev.pointerType!=='mouse'||zoom<=1)return;drag={x:ev.clientX,y:ev.clientY,l:box.scrollLeft,t:box.scrollTop};box.setPointerCapture(ev.pointerId);box.classList.add('dragging');});
 box.addEventListener('pointermove',ev=>{if(!drag)return;box.scrollLeft=drag.l-(ev.clientX-drag.x);box.scrollTop=drag.t-(ev.clientY-drag.y);});
 const end=()=>{drag=null;box.classList.remove('dragging');};box.addEventListener('pointerup',end);box.addEventListener('pointercancel',end);}
fetch('/api/project').then(r=>{if(!r.ok)throw Error('Local source unavailable');return r.json()}).then(packet=>{data=packet;let id=q.get('unit');selected=data.units.some(u=>u.id===id)?id:data.units[0].id;render();}).catch(()=>{['#residences','#plans','#compare'].forEach(s=>$(s).hidden=true);$('#load-error').textContent=t('loadError');$('#load-error').hidden=false;});
