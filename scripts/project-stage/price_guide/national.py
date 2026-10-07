# -*- coding: utf-8 -*-
"""PriceGuide, the "national" variant (design system 7.10.2026, HAD-460): the Israel page (/apartment-prices/) gets no
single-city calculator. It gets the official medians of every city that has a price page, side by side: 3 / 4 / 5 rooms,
the change against the same quarter a year earlier, the quarter, a link to each city's price page, and the Israel-wide
figures on top. Sortable (price / change / city name) with a few lines of script; on phones the table becomes cards.
  html(d_nat, cities, wa, sfx) -> the section's markup (the whole table is in the HTML; the script only re-orders rows)
  CSS_N, JS_N                  -> the variant's style (scoped through render.scope) and script
Data: cities/apartment-prices.json (d_nat, Israel series) and cities/<page-slug>.json (the cities). Stored data only: no
network at render time. A missing value shows the dot (render.py's NA), never a guess."""
import json
from collections import Counter
from urllib.parse import quote

import render as R

E, rich, num = R.E, R.rich, R.num
ROOMS = ("3", "4", "5")
FOLD = 8  # phone cards shown before the "all cities" button
TITLE = "מחירון דירות לפי עיר: חציון לפי חדרים"  # the CEO's title (7.10.2026); its first 4 words match no H2 on the live page
NA = '<span class="nlpg__na" aria-label="לא פורסם">·</span>'
NA_CHG = '<span class="nlpg__chg nlpg__chg--na" aria-label="אין חציון לאותו רבעון לפני שנה">·</span>'
WA_TEXT = "שלום, בדקתי במחירון הדירות לפי עיר באתר. אשמח לפרטים נוספים (nad-lan.co.il)"


def mil(v):
    """1,677,400 -> '1.68' (millions, two decimals, trailing zeros cut), as rooms.m()."""
    return ("%.2f" % (v / 1e6)).rstrip("0").rstrip(".")


def ils(v):
    return num("{:,}".format(int(v))) + " ₪"


def pct(v):
    """One decimal, sign in front, never '-0%' or '%'."""
    v = round(float(v), 1)
    if v == 0:
        return "0%"
    s = "%.1f" % abs(v)
    if s.endswith(".0"):
        s = s[:-2]
    return ("+" if v > 0 else "-") + s + "%"


def cls(v):
    return "up" if v > 0 else ("down" if v < 0 else "flat")


def prev_year(q):
    """'1-3.2026' -> '1-3.2025'."""
    a, y = q.rsplit(".", 1)
    return a + "." + str(int(y) - 1)


def at(series, q):
    for lab, v in series or []:
        if lab == q:
            return v
    return None


def m4(c):
    return ((c.get("rooms") or {}).get("4") or {}).get("latest")


def c4(c):
    return ((c.get("rooms") or {}).get("4") or {}).get("change_pct")


def israel_row(d_nat, rows, q):
    """Israel in the cities' own quarter (same-quarter comparison), from the Israel series in apartment-prices.json
    (fallback: a city file's `israel` block of that quarter). The change is the files' own method: the median of q against
    the median of the same quarter a year earlier, both stored in the series; no stored pair, no change."""
    out = {}
    for r in ROOMS:
        ser = ((d_nat.get("rooms") or {}).get(r) or {}).get("quarters") or []
        v = at(ser, q)
        if v is None:
            for c in rows:
                blk = c.get("israel") or {}
                if blk.get("quarter") == q and blk.get(r):
                    v = blk[r]
                    break
        y0 = at(ser, prev_year(q))
        out[r] = {"latest": v, "quarter": q, "change_pct": round((v - y0) / float(y0) * 100, 1) if v and y0 else None}
    return out


def cell(x, r, q_row):
    lab = r + " חדרים"
    if not x or not x.get("latest"):
        return '<td class="nlpg__m" data-l="' + E(lab) + '">' + NA + '</td>'
    ch = x.get("change_pct")
    h = '<td class="nlpg__m" data-l="' + E(lab) + '"><b class="nlpg__v">' + ils(x["latest"]) + '</b>'
    if ch is None:
        h += NA_CHG
    else:
        h += '<em class="nlpg__chg nlpg__chg--' + cls(ch) + '">' + num(pct(ch)) + '<span class="nlpg__yr"> בשנה</span></em>'
    if x.get("quarter") and x["quarter"] != q_row:  # the newest published median of this room count is from another quarter
        h += '<small class="nlpg__q">' + num(x["quarter"]) + '</small>'
    return h + '</td>'


def html(d_nat, cities=None, wa="{{WA}}", sfx=""):
    """d_nat = cities/apartment-prices.json; cities = the city dicts (cities/<slug>.json, or d_nat['cities'] when None)."""
    if cities is None:
        cities = d_nat.get("cities") or []
    own = d_nat.get("slug")
    rows = [c for c in cities if c.get("slug") != own and c.get("city_he")]
    rows.sort(key=lambda c: (m4(c) is None, -(m4(c) or 0), c["city_he"]))  # the default order: 4 rooms, dearest first
    qs = Counter(c.get("data_quarter") for c in rows if c.get("data_quarter")).most_common(1)
    cq = qs[0][0] if qs else d_nat.get("data_quarter", "")
    rn = d_nat.get("rooms") or {}
    upd = d_nat.get("updated_he", "")
    n = len(rows)

    out = ['<section class="nlds nlpg nlpg--national" id="nlpg' + sfx + '" aria-labelledby="nlpg-t' + sfx + '" dir="rtl" lang="he">',
           '<div class="nlpg__in">',
           '<header class="nlpg__head"><p class="nlds-kicker">מחירון רשמי · עודכן ' + num(upd) + '</p>',
           # "לפי" stays with its word (a no-break space): at 360-390px the title broke as "...לפי / עיר:"
           '<h2 class="nlpg__title" id="nlpg-t' + sfx + '">' + E((d_nat.get("title_national") or TITLE).replace("לפי ", "לפי\u00a0")) + '</h2>',
           '<p class="nlpg__answer">' + rich(d_nat["answer"]) + '</p></header>', '<ul class="nlpg__tiles">']
    for r in ROOMS:  # Israel, the newest quarter of the Israel series
        x = rn.get(r) or {}
        if not x.get("latest"):
            continue
        ch = x.get("change_pct")
        out.append('<li><b>' + num(mil(x["latest"])) + ' מיליון ₪</b><span>חציון מחיר העסקה בכל הארץ, דירת ' + r + ' חדרים</span><i>' +
                   num(x.get("quarter") or d_nat.get("data_quarter", "")) +
                   (' · <em class="nlpg__chg nlpg__chg--' + cls(ch) + '">' + num(pct(ch)) + ' בשנה</em>' if ch is not None else '') + '</i></li>')
    out.append('</ul><div class="nlpg__list nlpg__nat">')

    stat = "מהעיר היקרה לזולה, לפי חציון דירת 4 חדרים"
    out.append('<div class="nlpg__sort" role="radiogroup" aria-labelledby="nlpg-sl' + sfx + '" hidden><span class="nlpg__sl" id="nlpg-sl' + sfx + '">סדר לפי</span>'
               '<div class="nlpg__seg">' + ''.join(
                   '<label><input type="radio" name="nlpg-s' + sfx + '" value="' + k + '"' + (' checked' if k == "m4" else '') + '><span>' + t + '</span></label>'
                   for k, t in (("m4", "המחיר"), ("c4", "השינוי"), ("n", "שם העיר"))) +
               '</div><p class="nlpg__sorted" aria-live="polite">' + stat + '</p></div>')

    sub = '<span class="nlpg__ths">חציון, שינוי בשנה</span>'
    out.append('<table class="nlpg__table nlpg__table--nat"><caption class="nlpg__cap">חציון מחיר העסקה ב-' + num(str(n)) + ' ערים, ' + num(cq) +
               '</caption><thead><tr><th scope="col" data-sk="n">העיר</th>'
               '<th scope="col">3 חדרים' + sub + '</th><th scope="col" data-sk="m4" aria-sort="descending">4 חדרים' + sub + '</th>'
               '<th scope="col">5 חדרים' + sub + '</th><th scope="col">רבעון</th></tr></thead>')
    isr = israel_row(d_nat, rows, cq)
    if any(isr[r]["latest"] for r in ROOMS):
        out.append('<tbody class="nlpg__isr"><tr><th scope="row" class="nlpg__city"><b>כל הארץ</b><span>להשוואה, באותו רבעון. השינוי מחושב*</span></th>' +
                   ''.join(cell(isr[r], r, cq) for r in ROOMS) + '<td class="nlpg__qd" data-l="רבעון">' + num(cq) + '</td></tr></tbody>')
    out.append('<tbody class="nlpg__cities">')
    for c in rows:
        name, page, q, rr = c["city_he"], c.get("page"), c.get("data_quarter") or cq, c.get("rooms") or {}
        v4, ch4 = m4(c), c4(c)
        out.append('<tr data-n="' + E(name) + '" data-m4="' + (str(int(v4)) if v4 else '') + '" data-c4="' + (str(ch4) if ch4 is not None else '') + '">'
                   '<th scope="row" class="nlpg__city">' + ('<a href="' + E(page) + '">' + E(name) + '</a>' if page else '<b>' + E(name) + '</b>') + '</th>' +
                   ''.join(cell(rr.get(r), r, q) for r in ROOMS) + '<td class="nlpg__qd" data-l="רבעון">' + num(q) + '</td></tr>')
    out.append('</tbody></table>')
    if n > FOLD:
        out.append('<button class="nlpg__more" type="button" aria-expanded="false">לכל הערים <span class="nlds-num">(' + str(n) + ')</span></button>')
    out.append('</div><div class="nlpg__foot">')
    if wa:
        out.append('<a class="nlds-btn nlds-btn--primary nlpg__wa" data-pg="wa" target="_blank" rel="noopener" data-nlps-ev="pg-wa" href="https://wa.me/' +
                   E(wa) + '?text=' + quote(WA_TEXT, safe="") + '">לקבלת פרטים נוספים בוואטסאפ</a>')
    out.append('<p class="nlpg__links"><a href="https://nad-lan.co.il/property-value-estimator/">להערכת שווי לדירה מסוימת ←</a>'
               '<a href="https://nad-lan.co.il/apartment-purchase-cost-calculator/">לכל עלויות הקנייה ←</a></p>')
    has_na = any(not (x or {}).get("latest") or (x or {}).get("change_pct") is None
                 for c in rows for x in ((c.get("rooms") or {}).get(r) for r in ROOMS))
    out.append('<p class="nlpg__fine">חציון הוא המחיר שבאמצע: חצי מהעסקאות נסגרו מעליו וחצי מתחתיו. השינוי הוא לעומת אותו רבעון לפני שנה. '
               'רבעון קטן מתחת למחיר הוא הרבעון האחרון שפורסם לאותה עיר ולאותו מספר חדרים.' +
               (' נקודה במקום מספר: לא פורסם נתון.' if has_na else '') +
               # the CEO (7.10.2026): the Israel row's yearly change is shown, labelled as computed, not as an official figure
               (' * השינוי בשורת "כל הארץ" מחושב משני חציונים רשמיים, ' + num(cq) + ' מול ' +
                num(cq[:-4] + str(int(cq[-4:]) - 1) if cq[-4:].isdigit() else cq) + ', data.nadlan.gov.il, ואינו נתון רשמי בפני עצמו.'
                if any(isr[r]["latest"] for r in ROOMS) else '') +
               ' דירה מסוימת יכולה להיות רחוקה מהחציון בגלל הקומה, המצב, החניה והשכונה.</p></div>')
    out.append('<p class="nlpg__src">' + rich(d_nat["src_line"]) + '</p></div></section>')
    return "".join(out)


CSS_N = R.scope(r"""
.nlpg--national .nlpg__nat{display:grid !important;gap:12px !important;min-width:0 !important}
.nlpg__sort{display:flex !important;flex-wrap:wrap !important;align-items:center !important;gap:8px 12px !important;margin:0 !important}
.nlpg__sort[hidden]{display:none !important}
.nlpg__sl{font-size:13.5px !important;font-weight:700 !important;color:var(--pg-ink2) !important}
.nlpg__sorted{flex:1 1 240px !important;margin:0 !important;font-size:13.5px !important;line-height:1.45 !important;color:var(--pg-ink2) !important}
.nlpg--national .nlpg__table--nat thead th{vertical-align:bottom !important}
.nlpg__ths{display:block !important;font-size:11.5px !important;font-weight:400 !important;letter-spacing:0 !important;color:var(--pg-ink2) !important;margin-top:2px !important}
.nlpg--national .nlpg__table--nat td,.nlpg--national .nlpg__table--nat tbody th{padding:9px 8px !important}
.nlpg__city a{color:var(--pg-sea) !important;font-weight:700 !important;font-size:15px !important;text-decoration:underline !important;text-decoration-color:var(--nlds-link-underline,rgba(47,111,134,.4)) !important;text-underline-offset:3px !important}
.nlpg__city a:hover{color:var(--pg-seah) !important;text-decoration-color:currentColor !important}
.nlpg__v{font-weight:600 !important;white-space:nowrap !important}
.nlpg--national .nlpg__chg{font-style:normal !important;font-weight:700 !important;white-space:nowrap !important}
.nlpg--national .nlpg__chg--up{color:#2c6a46 !important}
.nlpg--national .nlpg__chg--down{color:#a5361f !important}
.nlpg--national .nlpg__chg--flat,.nlpg--national .nlpg__chg--na{color:var(--pg-ink2) !important}
.nlpg__m .nlpg__chg{font-size:13px !important;font-weight:600 !important;margin-inline-start:10px !important}
.nlpg__yr{display:none !important}
.nlpg--national .nlpg__q{display:block !important;font-size:11.5px !important;color:var(--pg-ink2) !important;font-weight:400 !important}
.nlpg__qd{font-size:13px !important;color:var(--pg-ink2) !important}
.nlpg--national .nlpg__table .nlpg__isr th,.nlpg--national .nlpg__table .nlpg__isr td{background:var(--pg-paper) !important}
.nlpg--national .nlpg__more{display:none !important}
.nlpg__foot{display:grid !important;grid-template-columns:auto minmax(0,1fr) !important;align-items:center !important;gap:8px 24px !important}
.nlpg--national .nlpg__wa{width:auto !important;min-width:300px !important}
.nlpg__foot .nlpg__fine{grid-column:1/-1 !important}
@container nlpg (max-width:860px){
 .nlpg__m .nlpg__chg{display:block !important;margin-inline-start:0 !important}
 .nlpg__foot{grid-template-columns:minmax(0,1fr) !important}
 .nlpg--national .nlpg__wa{width:100% !important;min-width:0 !important}
}
@container nlpg (max-width:620px){
 .nlpg--national:not(.is-open) .nlpg__table{display:block !important}
 .nlpg--national .nlpg__table--nat td,.nlpg--national .nlpg__table--nat tbody th{padding:0 !important}
 .nlpg--national .nlpg__table tbody tr:not(.nlpg__gh){grid-template-columns:repeat(3,minmax(0,1fr)) !important;gap:4px 10px !important;align-items:start !important}
 .nlpg--national .nlpg__table tbody tr:not(.nlpg__gh) th{grid-column:1/3 !important;grid-row:1 !important;align-self:center !important}
 .nlpg--national .nlpg__table td.nlpg__qd{grid-column:3 !important;grid-row:1 !important;justify-self:end !important;align-self:center !important}
 .nlpg--national .nlpg__table td.nlpg__qd::before{display:none !important}
 .nlpg--national .nlpg__table td.nlpg__m{grid-row:2 !important;min-width:0 !important}
 .nlpg--national .nlpg__isr tr{padding:12px 10px !important;border-radius:12px !important;border-bottom:0 !important;background:var(--pg-paper) !important}
 .nlpg--national .nlpg__table .nlpg__isr th,.nlpg--national .nlpg__table .nlpg__isr td{background:transparent !important}
 .nlpg__city a{min-height:44px !important;display:inline-flex !important;align-items:center !important;font-size:16px !important}
 .nlpg__yr{display:inline !important}
 .nlpg--national.is-js:not(.is-open) .nlpg__cities tr:nth-child(n+FOLD1){display:none !important}
 .nlpg--national.is-js:not(.is-open) .nlpg__more{display:block !important}
 .nlpg__sort .nlpg__seg{flex:1 1 100% !important;flex-wrap:nowrap !important}
 .nlpg__sort .nlpg__seg label{flex:1 1 0 !important;min-width:0 !important}
 .nlpg__sort .nlpg__seg label>span{width:100% !important;justify-content:center !important;padding-inline:6px !important;text-align:center !important}
}
""".replace("FOLD1", str(FOLD + 1)))

JS_N = r"""
(function(){var T={m4:['מהעיר היקרה לזולה, לפי חציון דירת 4 חדרים','מהעיר הזולה ליקרה, לפי חציון דירת 4 חדרים'],
 c4:['מהעלייה הגדולה לירידה הגדולה, דירת 4 חדרים לעומת לפני שנה','מהירידה הגדולה לעלייה הגדולה, דירת 4 חדרים לעומת לפני שנה'],
 n:['לפי שם העיר, מא׳ עד ת׳','לפי שם העיר, מת׳ עד א׳']},DEF={m4:-1,c4:-1,n:1};
var co=(window.Intl&&Intl.Collator)?new Intl.Collator('he'):null;
var byN=function(a,b){return co?co.compare(a,b):(a<b?-1:a>b?1:0)};
function one(root){if(root.__nlpgn)return;var tb=root.querySelector('.nlpg__cities');if(!tb)return;root.__nlpgn=1;root.classList.add('is-js');
 var bar=root.querySelector('.nlpg__sort'),st=root.querySelector('.nlpg__sorted'),S={k:'m4',d:-1};
 function sort(){var rows=Array.prototype.slice.call(tb.rows),k=S.k,d=S.d;
  rows.sort(function(a,b){var na=a.getAttribute('data-n'),nb=b.getAttribute('data-n');if(k==='n')return d*byN(na,nb);
   var x=a.getAttribute('data-'+k),y=b.getAttribute('data-'+k);if(x===''&&y==='')return byN(na,nb);if(x==='')return 1;if(y==='')return -1;
   return d*(parseFloat(x)-parseFloat(y))||byN(na,nb)});
  for(var i=0;i<rows.length;i++)tb.appendChild(rows[i]);
  if(st)st.textContent=T[k][d===DEF[k]?0:1];
  var hs=root.querySelectorAll('thead th[data-sk]');for(var j=0;j<hs.length;j++){var s=hs[j].getAttribute('data-sk');
   if(s===k||(k==='c4'&&s==='m4'))hs[j].setAttribute('aria-sort',k==='c4'?'other':(d>0?'ascending':'descending'));else hs[j].removeAttribute('aria-sort')}}
 if(bar){bar.hidden=false;bar.addEventListener('click',function(e){var t=e.target;if(!t||t.tagName!=='INPUT')return;
  if(t.value===S.k)S.d=-S.d;else{S.k=t.value;S.d=DEF[t.value]||1}sort()})}
 var mb=root.querySelector('.nlpg__more');if(mb)mb.addEventListener('click',function(){root.classList.add('is-open');mb.setAttribute('aria-expanded','true');
  var r=tb.rows[FOLDN],a=r&&r.querySelector('a');if(a&&a.focus)a.focus({preventScroll:true})})}
var all=document.querySelectorAll('.nlpg--national');for(var i=0;i<all.length;i++){try{one(all[i])}catch(e){}}})();
""".replace("FOLDN", str(FOLD))


if __name__ == "__main__":
    import glob, io, os
    here = os.path.dirname(os.path.abspath(__file__))
    d = json.load(io.open(os.path.join(here, "cities", "apartment-prices.json"), encoding="utf-8"))
    cs = [json.load(io.open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(here, "cities", "*.json")))]
    h = html(d, cs, "972525101555")
    print(len(h), "bytes of markup;", len(CSS_N), "css;", len(JS_N), "js;", h.count("<tr data-n="), "city rows")
