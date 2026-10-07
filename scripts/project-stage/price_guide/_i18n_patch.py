# -*- coding: utf-8 -*-
"""One-off: replaces render.py's Hebrew-only helpers and html() with the language-table version (PriceGuide v2, 7.10.2026)."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "render.py")
s = io.open(P, encoding="utf-8").read()
a = s.index("def num(s):")
b = s.index('CSS = r"""')
NEW = r'''UI_HE = {
    "lang": "he", "dir": "rtl", "loc": "he-IL", "grp": ",", "dec": ".",
    "kicker": "מחירון · עודכן", "cap": "המחירון",
    "th": ["הנכס", "₪ למ״ר", "מחיר הדירה, ₪", "הנתון", "מועד"], "dl": ["₪ למ״ר", "מחיר", "הנתון", "מועד"], "na": "לא פורסם",
    "more_t": "לכל המחירון: סביב הכיכר ולהשוואה", "more_p": "למחירון המלא",
    "where": "איפה הדירה", "area": "שטח הדירה", "floor": "קומה", "taxlg": "מס רכישה", "single": "דירה יחידה", "more": "דירה נוספת",
    "out": "אומדן מחיר", "tax": "מס רכישה", "total": "סה״כ עם מס רכישה", "wa": "לקבלת פרטים נוספים בוואטסאפ",
    "links": [["לכל עלויות הקנייה ←", "https://nad-lan.co.il/apartment-purchase-cost-calculator/"],
              ["לחישוב המשכנתא ←", "https://nad-lan.co.il/mortgage-calculator/"]],
    "fine1": "אומדן לא מחייב, לפי העסקאות והמחירים שפורסמו עד", "fine2": "המחיר נקבע מול המוכר.",
    "chart": "המחיר למ״ר לפי הקומה במגדלים, עם העסקאות שפורסמו",
    "u_m2": "{n} מ״ר", "u_floor": "קומה {n}", "u_mil": "{n} מיליון ₪", "u_ils": "{n} ₪", "u_pm2": "{n} ₪ למ״ר", "approx": "כ-{n}",
    "js": {"avg": "ממוצע העסקאות, כ-{n}", "deals": "עסקאות שפורסמו", "f1": "קומה 1", "f40": "קומה 40", "axis": "₪ למ״ר לפי הקומה",
           "you": "הבחירה שלכם", "tw": "מגדלי כיכר המדינה, ממוצע", "ta": "תל אביב יפו, חציון",
           "aria_t": "אומדן של {lo} עד {hi} ₪ למ״ר בקומה {f}, מול ממוצע העסקאות במגדלים, כ-{avg} ₪",
           "aria_a": "{m}: {lo} עד {hi} ₪ למ״ר, מול ממוצע המגדלים כ-{avg} ₪ ותל אביב יפו {ta} ₪",
           "wa": "שלום, בדקתי במחירון של מגדלי כיכר המדינה: {m}, {a} מ״ר{f}, אומדן {r} מיליון ₪. אשמח לפרטים נוספים (nad-lan.co.il)",
           "wa_f": ", קומה {f}"},
}


def ui(d):
    u = dict(UI_HE)
    u.update({k: v for k, v in (d.get("ui") or {}).items() if k != "js"})
    js = dict(UI_HE["js"])
    js.update((d.get("ui") or {}).get("js") or {})
    u["js"] = js
    return u


def num(s):
    """A number or range as one LTR island (inside RTL lines and as a no-break unit in LTR ones)."""
    return '<span class="nlds-num">' + E(s) + '</span>' if s != '' else ''


NUMRE = re.compile('\\d(?:[\\d,.  ]*\\d)?(?:-\\d(?:[\\d,.  ]*\\d)?)?')


def rich(t):
    """Escaped text with every number or range as one island (no break inside 63,000-68,000 or 63 000-68 000)."""
    return NUMRE.sub(lambda m: '<span class="nlds-num">' + m.group(0) + '</span>', E(t))


def mil(n, u=UI_HE):
    s = ('%.2f' % (n / 1e6)).rstrip('0').rstrip('.')
    return s.replace('.', u["dec"])


def thou(n, u=UI_HE):
    return '{:,}'.format(int(round(n / 100.0) * 100)).replace(',', u["grp"])


def put(pat, n_html):
    """A unit pattern such as '{n} מ״ר' around a number that is already HTML."""
    a, b = pat.split('{n}')
    return E(a) + n_html + E(b)


def tax(price, br):
    acc, prev = 0.0, 0
    for cap, rate in br:
        top = price if cap is None else min(price, cap)
        if top > prev:
            acc += (top - prev) * rate
        if cap is None or price <= cap:
            break
        prev = cap
    return acc


def tower_m2(c, floor):
    m = c['modes'][0]
    return m['lo_floor1'] + (floor - 1) * (m['hi_floor39'] - m['lo_floor1']) / 38.0


def default_result(d, u=UI_HE):
    c = d['calc']
    area, floor = 140, 20
    p = tower_m2(c, floor)
    b = c['modes'][0]['band']
    lo, hi = p * (1 - b), p * (1 + b)
    mid = p * area
    t = tax(mid, c['tax_single'])
    return {'range': '%s-%s' % (mil(lo * area, u), mil(hi * area, u)), 'm2': '%s-%s' % (thou(lo, u), thou(hi, u)),
            'tax': thou(round(t / 1000.0) * 1000, u), 'total': mil(mid + t, u)}


def html(d, wa='{{WA}}', sfx=''):
    u = ui(d)
    c = d['calc']
    r = default_result(d, u)
    NA = '<span class="nlpg__na" aria-label="' + E(u["na"]) + '">·</span>'
    upd = d.get('updated_shown') or d['updated_he']
    out = ['<section class="nlds nlpg" id="nlpg' + sfx + '" aria-labelledby="nlpg-t' + sfx + '" dir="' + u["dir"] + '" lang="' + u["lang"] + '">',
           '<div class="nlpg__in">',
           '<header class="nlpg__head"><p class="nlds-kicker">' + E(u["kicker"]) + ' ' + num(upd) + '</p>',
           '<h2 class="nlpg__title" id="nlpg-t' + sfx + '">' + E(d['title']) + '</h2>',
           '<p class="nlpg__answer">' + rich(d['answer']) + '</p></header>', '<ul class="nlpg__tiles">']
    for t in d['tiles']:
        out.append('<li><b>' + rich(t['big']) + '</b><span>' + rich(t['small']) + '</span><i>' + num(t['date']) + '</i></li>')
    out.append('</ul><div class="nlpg__grid"><div class="nlpg__list">')
    out.append('<table class="nlpg__table"><caption class="nlpg__cap">' + E(u["cap"]) + '</caption><thead><tr>' +
               ''.join('<th scope="col">' + E(h) + '</th>' for h in u["th"]) + '</tr></thead>')
    for gi, g in enumerate(d['groups']):
        out.append('<tbody class="nlpg__grp' + (' nlpg__grp--more' if gi else '') + '"><tr class="nlpg__gh"><th colspan="5" scope="colgroup">' +
                   E(g['name']) + '</th></tr>')
        for row in g['rows']:
            out.append('<tr><th scope="row"><b>' + rich(row['what']) + '</b>' + ('<span>' + rich(row['sub']) + '</span>' if row['sub'] else '') + '</th>'
                       '<td data-l="' + E(u["dl"][0]) + '">' + (rich(row['m2']) if row['m2'] else NA) + '</td>'
                       '<td data-l="' + E(u["dl"][1]) + '">' + (rich(row['price']) if row['price'] else NA) + '</td>'
                       '<td data-l="' + E(u["dl"][2]) + '"><span class="nlpg__k nlpg__k--' + E(row['kind']) + '">' + E(d['kinds'][row['kind']]) + '</span></td>'
                       '<td data-l="' + E(u["dl"][3]) + '">' + num(row['date']) + '</td></tr>')
        out.append('</tbody>')
    more = sum(len(g['rows']) for g in d['groups'][1:])
    allr = sum(len(g['rows']) for g in d['groups'])
    out.append('</table><button class="nlpg__more" type="button" aria-expanded="false">'
               '<span class="nlpg__mt">' + E(u["more_t"]) + ' <span class="nlds-num">(' + str(more) + ')</span></span>'
               '<span class="nlpg__mp">' + E(u["more_p"]) + ' <span class="nlds-num">(' + str(allr) + ')</span></span></button></div>')
    t = dict(u["js"])
    for k in ("u_m2", "u_floor", "u_mil", "u_ils", "u_pm2", "approx"):
        t[k] = u[k]
    cfg = {'modes': [{k: v for k, v in m.items() if k not in ('src',)} for m in c['modes']], 'deals': c['deals_plot'],
           'avg': c['avg_line'], 'ta': c['ta_median'], 'tax1': c['tax_single'], 'tax2': c['tax_more'], 'wa': wa,
           'loc': u["loc"], 'dec': u["dec"], 't': t}
    out.append('<form class="nlpg__calc" data-cfg="' + E(json.dumps(cfg, ensure_ascii=False, separators=(',', ':'))) +
               '" novalidate><h3 class="nlpg__ct">' + E(d['calc_title']) + '</h3>')
    out.append('<fieldset class="nlpg__f"><legend>' + E(u["where"]) + '</legend><div class="nlpg__seg">')
    for i, m in enumerate(c['modes']):
        out.append('<label><input type="radio" name="nlpg-m' + sfx + '" value="' + E(m['id']) + '"' + (' checked' if i == 0 else '') + '><span>' +
                   E(m['label']) + '</span></label>')
    out.append('</div></fieldset>')
    out.append('<div class="nlpg__f"><label for="nlpg-a' + sfx + '">' + E(u["area"]) + '</label><div class="nlpg__rng"><input type="range" id="nlpg-a' + sfx +
               '" data-pg="a" min="50" max="300" step="5" value="140"><output data-pg="ao" for="nlpg-a' + sfx + '">' + put(u["u_m2"], num('140')) + '</output></div></div>')
    out.append('<div class="nlpg__f" data-pg="fl"><label for="nlpg-fs' + sfx + '">' + E(u["floor"]) + '</label><div class="nlpg__rng"><input type="range" id="nlpg-fs' + sfx +
               '" data-pg="fs" min="1" max="40" step="1" value="20"><output data-pg="fo" for="nlpg-fs' + sfx + '">' + put(u["u_floor"], num('20')) + '</output></div></div>')
    out.append('<fieldset class="nlpg__f"><legend>' + E(u["taxlg"]) + '</legend><div class="nlpg__seg nlpg__seg--2">'
               '<label><input type="radio" name="nlpg-t' + sfx + '" value="single" checked><span>' + E(u["single"]) + '</span></label>'
               '<label><input type="radio" name="nlpg-t' + sfx + '" value="more"><span>' + E(u["more"]) + '</span></label></div></fieldset>')
    out.append('<div class="nlpg__out" aria-live="polite" aria-atomic="true"><p class="nlpg__ol">' + E(u["out"]) + '</p>'
               '<p class="nlpg__big" data-pg="p">' + put(u["u_mil"], num(r['range'])) + '</p>'
               '<p class="nlpg__pm" data-pg="pm">' + put(u["approx"], put(u["u_pm2"], num(r['m2']))) + '</p>'
               '<svg class="nlpg__chart" data-pg="ch" viewBox="0 0 340 138" direction="ltr" role="img" focusable="false"><title>' + E(u["chart"]) + '</title></svg>'
               '<dl class="nlpg__rows"><div><dt>' + E(u["tax"]) + '</dt><dd data-pg="tx">' + put(u["approx"], put(u["u_ils"], num(r['tax']))) + '</dd></div>'
               '<div><dt>' + E(u["total"]) + '</dt><dd data-pg="tt">' + put(u["approx"], put(u["u_mil"], num(r['total']))) + '</dd></div></dl>'
               '<p class="nlpg__why" data-pg="why">' + rich(c['modes'][0]['why']) + '</p></div>')
    if wa:
        out.append('<a class="nlds-btn nlds-btn--primary nlpg__wa" data-pg="wa" target="_blank" rel="noopener" data-nlps-ev="pg-wa" href="https://wa.me/' +
                   E(wa) + '?text=">' + E(u["wa"]) + '</a>')
    out.append('<p class="nlpg__links">' + ''.join('<a href="' + E(h) + '">' + E(x) + '</a>' for x, h in u["links"]) + '</p>')
    out.append('<p class="nlpg__fine">' + E(u["fine1"]) + ' ' + num(upd) + '. ' + rich(c['gap']) + ' ' + E(u["fine2"]) + '</p></form></div>')
    out.append('<p class="nlpg__src">' + rich(d['src_line']) + '</p></div></section>')
    return ''.join(out)


'''
s = s[:a] + NEW + s[b:]
# the script reads its words and number formats from cfg.t, cfg.loc and cfg.dec
JS_OLD_START = s.index('JS = r"""')
JS_OLD_END = s.index('"""', JS_OLD_START + 10) + 3
JS = r'''JS = r"""
(function(){var NS='http://www.w3.org/2000/svg';
function tax(p,br){var a=0,prev=0;for(var i=0;i<br.length;i++){var cap=br[i][0],r=br[i][1],top=cap===null?p:Math.min(p,cap);if(top>prev)a+=(top-prev)*r;if(cap===null||p<=cap)break;prev=cap}return a}
function el(t,a,txt){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;return e}
function one(root){var f=root.querySelector('.nlpg__calc');if(!f||f.__nlpg)return;f.__nlpg=1;var C;try{C=JSON.parse(f.getAttribute('data-cfg'))}catch(e){return}
 var T=C.t||{},LOC=C.loc||'he-IL';
 var nf=function(n){return new Intl.NumberFormat(LOC,{maximumFractionDigits:0}).format(Math.round(n/100)*100)};
 var nfk=function(n){return new Intl.NumberFormat(LOC).format(Math.round(n/1000)*1000)};
 var mil=function(n){return (n/1e6).toFixed(2).replace(/\.?0+$/,'').replace('.',C.dec||'.')};
 var isl=function(s){return '<span class="nlds-num">'+s+'</span>'};
 var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
 var put=function(p,h){var i=p.indexOf('{n}');return esc(p.slice(0,i))+h+esc(p.slice(i+3))};
 var fill=function(p,o){return p.replace(/\{(\w+)\}/g,function(_,k){return o[k]!=null?o[k]:''})};
 var q=function(k){return f.querySelector('[data-pg="'+k+'"]')};
 var val=function(n){var x=f.querySelector('input[name^="'+n+'"]:checked');return x?x.value:''};
 var mode=function(){var id=val('nlpg-m');for(var i=0;i<C.modes.length;i++)if(C.modes[i].id===id)return C.modes[i];return C.modes[0]};
 function draw(m,lo,hi,floor){var s=q('ch');if(!s)return;while(s.lastChild&&s.lastChild.nodeName!=='title')s.removeChild(s.lastChild);
  var L=44,R=330,T0=12,B=112;
  if(m.floor){var y0=50000,y1=82000,X=function(fl){return L+(fl-1)*(R-L)/39},Y=function(v){return B-(v-y0)*(B-T0)/(y1-y0)};
   var up=[],dn=[];for(var fl=1;fl<=40;fl++){var p=m.lo_floor1+(fl-1)*(m.hi_floor39-m.lo_floor1)/38;up.push(X(fl)+','+Y(p*(1+m.band)));dn.unshift(X(fl)+','+Y(p*(1-m.band)))}
   [60000,70000,80000].forEach(function(g){s.appendChild(el('line',{x1:L,x2:R,y1:Y(g),y2:Y(g),stroke:'#e3e1da','stroke-width':1}));s.appendChild(el('text',{x:L-6,y:Y(g)+3.5,'text-anchor':'end'},nf(g)))});
   s.appendChild(el('polygon',{points:up.concat(dn).join(' '),fill:'rgba(47,111,134,.14)'}));
   s.appendChild(el('line',{x1:L,x2:R,y1:Y(C.avg),y2:Y(C.avg),stroke:'#1f4b5c','stroke-width':1.2,'stroke-dasharray':'4 3'}));
   s.appendChild(el('text',{x:L+4,y:Y(C.avg)-5,'text-anchor':'start'},fill(T.avg,{n:nf(C.avg)})));
   var fx=X(floor),pm=(lo+hi)/2;s.appendChild(el('line',{x1:fx,x2:fx,y1:T0-4,y2:B,stroke:'#2f6f86','stroke-width':1.5}));
   s.appendChild(el('circle',{cx:fx,cy:Y(pm),r:5.5,fill:'#2f6f86',stroke:'#fff','stroke-width':2}));
   C.deals.forEach(function(d){s.appendChild(el('circle',{cx:X(d[0]),cy:Y(d[1]),r:4,fill:'#fff',stroke:'#14212b','stroke-width':1.6}))});
   s.appendChild(el('text',{x:X(36.6),y:Y(77600),'text-anchor':'end'},T.deals));
   s.appendChild(el('text',{x:L,y:B+16,'text-anchor':'start'},T.f1));s.appendChild(el('text',{x:R,y:B+16,'text-anchor':'end'},T.f40));
   s.appendChild(el('text',{x:(L+R)/2,y:B+16,'text-anchor':'middle'},T.axis));
   s.setAttribute('aria-label',fill(T.aria_t,{lo:nf(lo),hi:nf(hi),f:floor,avg:nf(C.avg)}));
  }else{var x0=40000,x1=115000,X2=function(v){return L+(v-x0)*(R-L)/(x1-x0)};
   [[T.you,m.lo,m.hi,1],[T.tw,C.avg,C.avg,0],[T.ta,C.ta,C.ta,0]].forEach(function(r,i){var y=24+i*36;
    s.appendChild(el('text',{x:R,y:y-9,'text-anchor':'end'},r[0]));
    s.appendChild(el('line',{x1:X2(x0),x2:X2(x1),y1:y,y2:y,stroke:'#e3e1da','stroke-width':6,'stroke-linecap':'round'}));
    if(r[3]){s.appendChild(el('line',{x1:X2(r[1]),x2:X2(r[2]),y1:y,y2:y,stroke:'#2f6f86','stroke-width':8,'stroke-linecap':'round'}));
     s.appendChild(el('text',{x:X2(r[1]),y:y+17,'text-anchor':'middle'},nf(r[1])));s.appendChild(el('text',{x:X2(r[2]),y:y+17,'text-anchor':'middle'},nf(r[2])))}
    else{s.appendChild(el('circle',{cx:X2(r[1]),cy:y,r:5.5,fill:'#1f4b5c',stroke:'#fff','stroke-width':2}));s.appendChild(el('text',{x:X2(r[1]),y:y+17,'text-anchor':'middle'},nf(r[1])))}});
   s.setAttribute('aria-label',fill(T.aria_a,{m:m.label,lo:nf(m.lo),hi:nf(m.hi),avg:nf(C.avg),ta:nf(C.ta)}));
  }}
 function run(){var m=mode(),a=+q('a').value,fl=+q('fs').value,lo,hi;
  q('fl').hidden=!m.floor;q('ao').innerHTML=put(T.u_m2,isl(a));q('fo').innerHTML=put(T.u_floor,isl(fl));
  if(m.floor){var p=m.lo_floor1+(fl-1)*(m.hi_floor39-m.lo_floor1)/38;lo=p*(1-m.band);hi=p*(1+m.band)}else{lo=m.lo;hi=m.hi}
  var mid=(lo+hi)/2*a,t=tax(mid,val('nlpg-t')==='more'?C.tax2:C.tax1),rng=mil(lo*a)+'-'+mil(hi*a);
  q('p').innerHTML=put(T.u_mil,isl(rng));q('pm').innerHTML=put(T.approx,put(T.u_pm2,isl(nf(lo)+'-'+nf(hi))));
  q('tx').innerHTML=put(T.approx,put(T.u_ils,isl(nfk(t))));q('tt').innerHTML=put(T.approx,put(T.u_mil,isl(mil(mid+t))));
  q('why').textContent=m.why;draw(m,lo,hi,fl);
  var w=q('wa');if(w&&C.wa){w.href='https://wa.me/'+C.wa+'?text='+encodeURIComponent(fill(T.wa,{m:m.label,a:a,f:m.floor?fill(T.wa_f,{f:fl}):'',r:rng}))}}
 f.addEventListener('input',run);f.addEventListener('change',run);f.addEventListener('submit',function(e){e.preventDefault()});
 var mb=root.querySelector('.nlpg__more');if(mb)mb.addEventListener('click',function(){root.classList.add('is-open');mb.setAttribute('aria-expanded','true');var g=root.querySelector('.nlpg__grp--more .nlpg__gh th');if(g){g.setAttribute('tabindex','-1');g.focus({preventScroll:true})}});
 run()}
var all=document.querySelectorAll('.nlpg');for(var i=0;i<all.length;i++)one(all[i])})();
"""'''
s = s[:JS_OLD_START] + JS + s[JS_OLD_END:]
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("render.py rewritten:", len(s), "chars")
