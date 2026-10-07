# -*- coding: utf-8 -*-
"""PriceGuide, the "rooms" variant (design system 7.10.2026, HAD-460): the price list of a city from the official medians (deals
reported to the Tax Authority, by number of rooms, per quarter) and a check: the reader picks the rooms, sees the median and its
8-quarter trend, types the price he saw in an ad and learns how far it is from the median, with the purchase tax.
Data: price_guide/cities/<page-slug>.json (built from data.nadlan.gov.il settlement summaries; missing values stay null).
Shares the base classes and the scoped CSS of render.py; adds CSS_R and JS_R."""
import json

import render as R

E, rich, num = R.E, R.rich, R.num
ROOMS = ("3", "4", "5")


def m(v):
    """1,234,567 -> '1.23' (millions, two decimals, trailing zeros cut)."""
    return ("%.2f" % (v / 1e6)).rstrip("0").rstrip(".")


def pct(v):
    return ("+" if v > 0 else "") + ("%.1f" % v).rstrip("0").rstrip(".") + "%"


def html(d, wa="{{WA}}", sfx=""):
    rooms, isr = d["rooms"], d.get("israel") or {}
    city, q = d["city_he"], d["data_quarter"]
    NA = '<span class="nlpg__na" aria-label="לא פורסם">·</span>'
    upd = d.get("updated_he", "")
    out = ['<section class="nlds nlpg nlpg--rooms" id="nlpg' + sfx + '" aria-labelledby="nlpg-t' + sfx + '" dir="rtl" lang="he">',
           '<div class="nlpg__in">',
           '<header class="nlpg__head"><p class="nlds-kicker">מחירון רשמי · עודכן ' + num(upd) + '</p>',
           '<h2 class="nlpg__title" id="nlpg-t' + sfx + '">' + E(d["title"]) + '</h2>',
           '<p class="nlpg__answer">' + rich(d["answer"]) + '</p></header>', '<ul class="nlpg__tiles">']
    for r in ROOMS:
        x = rooms.get(r) or {}
        if not x.get("latest"):
            continue
        ch = x.get("change_pct")
        out.append('<li><b>' + num(m(x["latest"])) + ' מיליון ₪</b><span>חציון מחיר העסקה, דירת ' + r + ' חדרים</span><i>' + num(x.get("quarter") or q) +
                   (' · <em class="nlpg__chg nlpg__chg--' + ('up' if ch > 0 else 'down') + '">' + num(pct(ch)) + ' בשנה</em>' if ch is not None else '') +
                   '</i></li>')
    out.append('</ul><div class="nlpg__grid"><div class="nlpg__list">')
    out.append('<table class="nlpg__table"><caption class="nlpg__cap">המחירון ב' + E(city) + '</caption><thead><tr>'
               '<th scope="col">הדירה</th><th scope="col">חציון, ' + E(q) + '</th><th scope="col">לפני שנה</th><th scope="col">שינוי</th>'
               '<th scope="col">בכל הארץ</th></tr></thead><tbody class="nlpg__grp">')
    for r, label in (("3", "3 חדרים"), ("4", "4 חדרים"), ("5", "5 חדרים"), ("all", "כל הדירות")):
        x = rooms.get(r) or {}
        if not x.get("latest"):
            continue
        ch = x.get("change_pct")
        iv = (isr.get(r) or None)
        out.append('<tr><th scope="row"><b>' + E(label) + '</b></th>'
                   '<td data-l="חציון">' + num('{:,}'.format(int(x["latest"]))) + ' ₪' + ('<small class="nlpg__q">' + num(x["quarter"]) + '</small>' if x.get("quarter") and x["quarter"] != q else '') + '</td>'
                   '<td data-l="לפני שנה">' + (num('{:,}'.format(int(x["year_ago"]))) + ' ₪' if x.get("year_ago") else NA) + '</td>'
                   '<td data-l="שינוי">' + ('<span class="nlpg__chg nlpg__chg--' + ('up' if ch > 0 else 'down') + '">' + num(pct(ch)) + '</span>' if ch is not None else NA) + '</td>'
                   '<td data-l="בכל הארץ">' + (num('{:,}'.format(int(iv))) + ' ₪' if iv else NA) + '</td></tr>')
    out.append('</tbody></table>')
    nb = [n for n in (d.get("neighbourhoods") or []) if any((n.get("rooms") or {}).get(r) for r in ROOMS)]
    if nb:
        out.append('<table class="nlpg__table nlpg__table--nb nlpg__grp--more"><caption class="nlpg__cap">לפי שכונה, ' + E(q) + '</caption><thead><tr>'
                   '<th scope="col">השכונה</th><th scope="col">3 חדרים</th><th scope="col">4 חדרים</th><th scope="col">5 חדרים</th></tr></thead><tbody>')
        for n in nb:
            rr = n.get("rooms") or {}
            out.append('<tr><th scope="row"><b>' + E(n["name"]) + '</b></th>' + ''.join(
                '<td data-l="' + r + ' חדרים">' + (num(m(rr[r])) + ' מיליון' if rr.get(r) else NA) + '</td>' for r in ROOMS) + '</tr>')
        out.append('</tbody></table><button class="nlpg__more" type="button" aria-expanded="false"><span class="nlpg__mt">לכל השכונות <span class="nlds-num">(' +
                   str(len(nb)) + ')</span></span><span class="nlpg__mp">לכל השכונות <span class="nlds-num">(' + str(len(nb)) + ')</span></span></button>')
    out.append(''.join('<p class="nlpg__see"><a href="' + E(x['href']) + '">' + E(x['text']) + '</a></p>' for x in d.get('see', [])) + '</div>')
    cfg = {"variant": "rooms", "rooms": {r: {"latest": (rooms.get(r) or {}).get("latest"), "qt": (rooms.get(r) or {}).get("quarter") or q, "q": (rooms.get(r) or {}).get("quarters") or []} for r in ROOMS},
           "israel": {r: isr.get(r) for r in ROOMS}, "tax1": d["tax_single"], "tax2": d["tax_more"], "wa": wa, "city": city, "quarter": q}
    first = next((r for r in ("4", "3", "5") if (rooms.get(r) or {}).get("latest")), "4")
    x0 = rooms[first]["latest"]
    t0 = R.tax(x0, d["tax_single"])
    out.append('<form class="nlpg__calc" data-cfg="' + E(json.dumps(cfg, ensure_ascii=False, separators=(",", ":"))) + '" novalidate>'
               '<h3 class="nlpg__ct">מחשבון מחיר דירה ב' + E(city) + '</h3>'
               '<fieldset class="nlpg__f"><legend>כמה חדרים</legend><div class="nlpg__seg">' + ''.join(
                   '<label><input type="radio" name="nlpg-r' + sfx + '" value="' + r + '"' + (' checked' if r == first else '') + '><span>' + r + ' חדרים</span></label>'
                   for r in ROOMS if (rooms.get(r) or {}).get("latest")) + '</div></fieldset>'
               '<div class="nlpg__f"><label for="nlpg-pr' + sfx + '">המחיר שראיתם במודעה, ₪</label><input class="nlpg__in-price" id="nlpg-pr' + sfx +
               '" data-pg="pr" type="text" inputmode="numeric" autocomplete="off" placeholder="לדוגמה 4,200,000"></div>'
               '<fieldset class="nlpg__f"><legend>מס רכישה</legend><div class="nlpg__seg nlpg__seg--2">'
               '<label><input type="radio" name="nlpg-t' + sfx + '" value="single" checked><span>דירה יחידה</span></label>'
               '<label><input type="radio" name="nlpg-t' + sfx + '" value="more"><span>דירה נוספת</span></label></div></fieldset>'
               '<div class="nlpg__out" aria-live="polite" aria-atomic="true"><p class="nlpg__ol">חציון מחיר העסקה</p>'
               '<p class="nlpg__big" data-pg="p">' + num(m(x0)) + ' מיליון ₪</p>'
               '<p class="nlpg__pm" data-pg="pm">דירת ' + first + ' חדרים ב' + E(city) + ', ' + num(rooms[first].get("quarter") or q) + '</p>'
               '<p class="nlpg__cmp" data-pg="cmp" hidden></p>'
               '<svg class="nlpg__chart" data-pg="ch" viewBox="0 0 340 138" direction="ltr" role="img" focusable="false"><title>חציון מחיר העסקה לפי רבעון</title></svg>'
               '<dl class="nlpg__rows"><div><dt data-pg="txl">מס רכישה על החציון</dt><dd data-pg="tx">' + ('0 ₪ (פטור)' if t0 < 500 else 'כ-' + num('{:,}'.format(int(round(t0 / 1000) * 1000))) + ' ₪') + '</dd></div>'
               '<div><dt>סה״כ עם מס רכישה</dt><dd data-pg="tt">כ-' + num(m(x0 + t0)) + ' מיליון ₪</dd></div></dl></div>')
    if wa:
        out.append('<a class="nlds-btn nlds-btn--primary nlpg__wa" data-pg="wa" target="_blank" rel="noopener" data-nlps-ev="pg-wa" href="https://wa.me/' +
                   E(wa) + '?text=">לקבלת פרטים נוספים בוואטסאפ</a>')
    out.append('<p class="nlpg__links"><a href="https://nad-lan.co.il/apartment-purchase-cost-calculator/">לכל עלויות הקנייה ←</a>'
               '<a href="https://nad-lan.co.il/property-value-estimator/">להערכת שווי לדירה מסוימת ←</a></p>')
    out.append('<p class="nlpg__fine">חציון הוא המחיר שבאמצע: חצי מהעסקאות נסגרו מעליו וחצי מתחתיו. דירה מסוימת יכולה להיות רחוקה ממנו בגלל הקומה, '
               'המצב, החניה והשכונה. המחיר נקבע מול המוכר.</p></form></div>')
    out.append('<p class="nlpg__src">' + rich(d["src_line"]) + '</p></div></section>')
    return "".join(out)


CSS_R = R.scope(r"""
.nlpg__chg{font-style:normal !important;font-weight:700 !important;white-space:nowrap !important}
.nlpg__chg--up{color:#2c6a46 !important}
.nlpg__chg--down{color:#a5361f !important}
.nlpg__in-price{width:100% !important;min-height:48px !important;border:1px solid var(--pg-line) !important;border-radius:10px !important;background:var(--pg-surf) !important;padding:10px 14px !important;font:600 17px/1.2 var(--pg-sans) !important;color:var(--pg-ink) !important;direction:ltr !important;text-align:right !important}
.nlpg__in-price:focus-visible{outline:2px solid var(--pg-sea) !important;outline-offset:2px !important}
.nlpg__cmp{margin:2px 0 4px !important;font-size:15px !important;font-weight:700 !important;color:var(--pg-deep) !important}
.nlpg__table--nb{margin-top:14px !important}
.nlpg__q{display:block !important;font-size:11.5px !important;color:var(--pg-ink2) !important;font-weight:400 !important}
.nlpg:not(.is-open) .nlpg__table--nb.nlpg__grp--more{display:none !important}
@container nlpg (min-width:861px){.nlpg:not(.is-open) .nlpg__table--nb.nlpg__grp--more{display:table !important}}
""")

JS_R = r"""
(function(){var NS='http://www.w3.org/2000/svg';
function tax(p,br){var a=0,prev=0;for(var i=0;i<br.length;i++){var cap=br[i][0],r=br[i][1],top=cap===null?p:Math.min(p,cap);if(top>prev)a+=(top-prev)*r;if(cap===null||p<=cap)break;prev=cap}return a}
function el(t,a,txt){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;return e}
var nf=function(n){return new Intl.NumberFormat('he-IL',{maximumFractionDigits:0}).format(n)};
var mil=function(n){return (n/1e6).toFixed(2).replace(/\.?0+$/,'')};
var isl=function(s){return '<span class="nlds-num">'+s+'</span>'};
function one(root){var f=root.querySelector('.nlpg__calc');if(!f||f.__nlpgr)return;f.__nlpgr=1;var C;try{C=JSON.parse(f.getAttribute('data-cfg'))}catch(e){return}
 if(C.variant!=='rooms')return;
 var q=function(k){return f.querySelector('[data-pg="'+k+'"]')};
 var val=function(n){var x=f.querySelector('input[name^="'+n+'"]:checked');return x?x.value:''};
 function draw(r){var s=q('ch');if(!s)return;while(s.lastChild&&s.lastChild.nodeName!=='title')s.removeChild(s.lastChild);
  var Q=(C.rooms[r]&&C.rooms[r].q||[]).filter(function(p){return p[1]});if(Q.length<2)return;
  var vals=Q.map(function(p){return p[1]}),isr=C.israel[r];if(isr)vals.push(isr);
  var lo=Math.min.apply(null,vals)*0.94,hi=Math.max.apply(null,vals)*1.04,L=44,R=330,T=14,B=108;
  var X=function(i){return L+i*(R-L)/(Q.length-1)},Y=function(v){return B-(v-lo)*(B-T)/(hi-lo)};
  [lo+(hi-lo)*0.2,lo+(hi-lo)*0.6].forEach(function(g){s.appendChild(el('line',{x1:L,x2:R,y1:Y(g),y2:Y(g),stroke:'#e3e1da','stroke-width':1}));s.appendChild(el('text',{x:L-6,y:Y(g)+3.5,'text-anchor':'end'},mil(g)))});
  if(isr){s.appendChild(el('line',{x1:L,x2:R,y1:Y(isr),y2:Y(isr),stroke:'#1f4b5c','stroke-width':1.2,'stroke-dasharray':'4 3'}));s.appendChild(el('text',{x:L+4,y:Y(isr)-5,'text-anchor':'start'},'בכל הארץ, '+mil(isr)))}
  s.appendChild(el('polyline',{points:Q.map(function(p,i){return X(i)+','+Y(p[1])}).join(' '),fill:'none',stroke:'#2f6f86','stroke-width':2.2}));
  Q.forEach(function(p,i){s.appendChild(el('circle',{cx:X(i),cy:Y(p[1]),r:i===Q.length-1?5:3.2,fill:i===Q.length-1?'#2f6f86':'#fff',stroke:'#2f6f86','stroke-width':1.6}))});
  s.appendChild(el('text',{x:L,y:B+18,'text-anchor':'start'},Q[0][0]));s.appendChild(el('text',{x:R,y:B+18,'text-anchor':'end'},Q[Q.length-1][0]));
  s.setAttribute('aria-label','חציון מחיר העסקה לדירת '+r+' חדרים ב'+C.city+', מ-'+mil(Q[0][1])+' מיליון ₪ ב-'+Q[0][0]+' ל-'+mil(Q[Q.length-1][1])+' מיליון ב-'+Q[Q.length-1][0])}
 function run(){var r=val('nlpg-r')||'4',med=C.rooms[r]&&C.rooms[r].latest;if(!med)return;
  var raw=(q('pr').value||'').replace(/[^\d]/g,''),p=raw?parseInt(raw,10):0;if(p&&p<100000)p=0;
  q('p').innerHTML=isl(mil(med))+' מיליון ₪';q('pm').innerHTML='דירת '+r+' חדרים ב'+C.city+', '+isl(C.rooms[r].qt||C.quarter);
  var c=q('cmp');if(p){var d=(p-med)/med*100;c.hidden=false;c.innerHTML=Math.abs(d)<1?'המחיר שראיתם כמעט זהה לחציון':'המחיר שראיתם '+(d>0?'גבוה':'נמוך')+' ב-'+isl(Math.abs(d).toFixed(0)+'%')+' מהחציון'}else{c.hidden=true}
  var base=p||med,t=tax(base,val('nlpg-t')==='more'?C.tax2:C.tax1);
  q('txl').textContent=p?'מס רכישה על המחיר שראיתם':'מס רכישה על החציון';q('tx').innerHTML=t<500?'0 ₪ (פטור)':'כ-'+isl(nf(Math.round(t/1000)*1000))+' ₪';q('tt').innerHTML='כ-'+isl(mil(base+t))+' מיליון ₪';
  draw(r);
  var w=q('wa');if(w&&C.wa){w.href='https://wa.me/'+C.wa+'?text='+encodeURIComponent('שלום, בדקתי במחירון של '+C.city+': דירת '+r+' חדרים'+(p?', מחיר במודעה '+nf(p)+' ₪':'')+'. אשמח לפרטים נוספים (nad-lan.co.il)')}}
 f.addEventListener('input',run);f.addEventListener('change',run);f.addEventListener('submit',function(e){e.preventDefault()});
 var mb=root.querySelector('.nlpg__more');if(mb)mb.addEventListener('click',function(){root.classList.add('is-open');mb.setAttribute('aria-expanded','true')});
 run()}
var all=document.querySelectorAll('.nlpg--rooms');for(var i=0;i<all.length;i++){try{one(all[i])}catch(e){}}})();
"""
