# -*- coding: utf-8 -*-
"""PriceGuide (design system component, 7.10.2026, HAD-433): one price list + one price calculator for a project page.
One source for the design system preview and for the plugin's server-rendered section:
  html(data, wa)  -> the section's markup (the table and the default result are in the HTML, for readers without script and
                     for search; the script only recalculates)
  CSS, JS         -> the component's style and script (scoped to .nlpg)
Data: price_guide/<slug>.json (every number has a source there; the page shows dates only)."""
import html as _h
import json
import math
import re

E = lambda s: _h.escape(str(s), quote=True)


def num(s):
    """Numbers and ranges as one LTR island inside the Hebrew line."""
    return '<span class="nlds-num">' + E(s) + '</span>' if s else ''


NUMRE = re.compile(r'\d[\d,.]*(?:-\d[\d,.]*)?')


def rich(t):
    """Escaped text with every number or range as one LTR island (no break inside 63,000-68,000)."""
    return NUMRE.sub(lambda m: '<span class="nlds-num">' + m.group(0) + '</span>', E(t))


def big(s):
    """'כ-65,000 ₪' / '9.58-10.63 מיליון ₪' -> the prefix and the words stay Hebrew, the number is one LTR island."""
    pre = ''
    for p in ('כ-', 'מעל '):
        if s.startswith(p):
            pre, s = p, s[len(p):]
    suf = ''
    for w in (' מיליון ₪', ' ₪'):
        if s.endswith(w):
            suf, s = w, s[:-len(w)]
            break
    return pre + num(s) + suf


def mil(n):
    v = n / 1e6
    s = ('%.2f' % v).rstrip('0').rstrip('.')
    return s


def thou(n):
    return '{:,}'.format(int(round(n / 100.0) * 100))


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


def default_result(d):
    c = d['calc']
    area, floor = 140, 20
    p = tower_m2(c, floor)
    b = c['modes'][0]['band']
    lo, hi = p * (1 - b), p * (1 + b)
    mid = p * area
    t = tax(mid, c['tax_single'])
    return {'range': '%s-%s מיליון ₪' % (mil(lo * area), mil(hi * area)), 'm2': '%s-%s' % (thou(lo), thou(hi)),
            'tax': thou(round(t / 1000.0) * 1000), 'total': mil(mid + t)}


def chart_svg():
    # the frame only; the script draws into it (a reader without script sees the numbers above)
    return ('<svg class="nlpg__chart" data-pg="ch" viewBox="0 0 340 138" direction="ltr" role="img" focusable="false">'
            '<title>המחיר למ״ר לפי הקומה במגדלים, עם העסקאות שפורסמו</title></svg>')


def html(d, wa='{{WA}}', sfx=''):
    c = d['calc']
    r = default_result(d)
    out = ['<section class="nlds nlpg" id="nlpg' + sfx + '" aria-labelledby="nlpg-t' + sfx + '" dir="rtl" lang="he">', '<div class="nlpg__in">',
           '<header class="nlpg__head"><p class="nlds-kicker">מחירון · עודכן ' + num(d['updated_he']) + '</p>',
           '<h2 class="nlpg__title" id="nlpg-t' + sfx + '">כמה עולה דירה במגדלי כיכר המדינה</h2>',
           '<p class="nlpg__answer">' + rich(d['answer']) + '</p></header>', '<ul class="nlpg__tiles">']
    for t in d['tiles']:
        out.append('<li><b>' + big(t['big']) + '</b><span>' + rich(t['small']) + '</span><i>' + num(t['date']) + '</i></li>')
    out.append('</ul><div class="nlpg__grid"><div class="nlpg__list">')
    out.append('<table class="nlpg__table"><caption class="nlpg__cap">המחירון</caption><thead><tr>'
               '<th scope="col">הנכס</th><th scope="col">₪ למ״ר</th><th scope="col">מחיר הדירה, ₪</th><th scope="col">הנתון</th>'
               '<th scope="col">מועד</th></tr></thead>')
    for gi, g in enumerate(d['groups']):
        out.append('<tbody class="nlpg__grp' + (' nlpg__grp--more' if gi else '') + '"><tr class="nlpg__gh"><th colspan="5" scope="colgroup">' +
                   E(g['name']) + '</th></tr>')
        for row in g['rows']:
            m2 = row['m2']
            pre = ''
            for p in ('כ-', 'מעל '):
                if m2.startswith(p):
                    pre, m2 = p, m2[len(p):]
            price = row['price']
            ppre = ''
            if price.startswith('כ-'):
                ppre, price = 'כ-', price[2:]
            pr = (ppre + num(price.replace(' מיליון', '')) + ' מיליון') if price else '<span class="nlpg__na" aria-label="לא פורסם">·</span>'
            out.append('<tr><th scope="row"><b>' + rich(row['what']) + '</b>' + ('<span>' + rich(row['sub']) + '</span>' if row['sub'] else '') + '</th>'
                       '<td data-l="₪ למ״ר">' + ((pre + num(m2)) if m2 else '<span class="nlpg__na" aria-label="לא פורסם">·</span>') + '</td>'
                       '<td data-l="מחיר">' + pr + '</td>'
                       '<td data-l="הנתון"><span class="nlpg__k nlpg__k--' + E(row['kind']) + '">' + E(d['kinds'][row['kind']]) + '</span></td>'
                       '<td data-l="מועד">' + num(row['date']) + '</td></tr>')
        out.append('</tbody>')
    more = sum(len(g['rows']) for g in d['groups'][1:])
    allr = sum(len(g['rows']) for g in d['groups'])
    out.append('</table><button class="nlpg__more" type="button" aria-expanded="false">'
               '<span class="nlpg__mt">לכל המחירון: סביב הכיכר ולהשוואה <span class="nlds-num">(' + str(more) + ')</span></span>'
               '<span class="nlpg__mp">למחירון המלא <span class="nlds-num">(' + str(allr) + ')</span></span></button></div>')
    cfg = {'modes': [{k: v for k, v in m.items() if k not in ('src',)} for m in c['modes']], 'deals': c['deals_plot'],
           'avg': c['avg_line'], 'ta': c['ta_median'], 'tax1': c['tax_single'], 'tax2': c['tax_more'], 'wa': wa}
    out.append('<form class="nlpg__calc" data-cfg="' + E(json.dumps(cfg, ensure_ascii=False, separators=(',', ':'))) +
               '" novalidate><h3 class="nlpg__ct">מחשבון מחיר דירה בכיכר המדינה</h3>')
    out.append('<fieldset class="nlpg__f"><legend>איפה הדירה</legend><div class="nlpg__seg">')
    for i, m in enumerate(c['modes']):
        out.append('<label><input type="radio" name="nlpg-m' + sfx + '" value="' + E(m['id']) + '"' + (' checked' if i == 0 else '') + '><span>' +
                   E(m['label']) + '</span></label>')
    out.append('</div></fieldset>')
    out.append('<div class="nlpg__f"><label for="nlpg-a' + sfx + '">שטח הדירה</label><div class="nlpg__rng"><input type="range" id="nlpg-a' + sfx + '" data-pg="a" min="50" '
               'max="300" step="5" value="140"><output data-pg="ao" for="nlpg-a' + sfx + '"><span class="nlds-num">140</span> מ״ר</output></div></div>')
    out.append('<div class="nlpg__f" data-pg="fl"><label for="nlpg-fs' + sfx + '">קומה</label><div class="nlpg__rng"><input type="range" id="nlpg-fs' + sfx + '" data-pg="fs" '
               'min="1" max="40" step="1" value="20"><output data-pg="fo" for="nlpg-fs' + sfx + '">קומה <span class="nlds-num">20</span></output></div></div>')
    out.append('<fieldset class="nlpg__f"><legend>מס רכישה</legend><div class="nlpg__seg nlpg__seg--2">'
               '<label><input type="radio" name="nlpg-t' + sfx + '" value="single" checked><span>דירה יחידה</span></label>'
               '<label><input type="radio" name="nlpg-t' + sfx + '" value="more"><span>דירה נוספת</span></label></div></fieldset>')
    out.append('<div class="nlpg__out" aria-live="polite" aria-atomic="true"><p class="nlpg__ol">אומדן מחיר</p>'
               '<p class="nlpg__big" data-pg="p">' + num(r['range'].replace(' מיליון ₪', '')) + ' מיליון ₪</p>'
               '<p class="nlpg__pm" data-pg="pm">כ-' + num(r['m2']) + ' ₪ למ״ר</p>' + chart_svg() +
               '<dl class="nlpg__rows"><div><dt>מס רכישה</dt><dd data-pg="tx">כ-' + num(r['tax']) + ' ₪</dd></div>'
               '<div><dt>סה״כ עם מס רכישה</dt><dd data-pg="tt">כ-' + num(r['total']) + ' מיליון ₪</dd></div></dl>'
               '<p class="nlpg__why" data-pg="why">' + rich(c['modes'][0]['why']) + '</p></div>')
    if wa:
        out.append('<a class="nlds-btn nlds-btn--primary nlpg__wa" data-pg="wa" target="_blank" rel="noopener" data-nlps-ev="pg-wa" href="https://wa.me/' +
                   E(wa) + '?text=">לקבלת פרטים נוספים בוואטסאפ</a>')
    out.append('<p class="nlpg__links"><a href="https://nad-lan.co.il/apartment-purchase-cost-calculator/">לכל עלויות הקנייה ←</a>'
               '<a href="https://nad-lan.co.il/mortgage-calculator/">לחישוב המשכנתא ←</a></p>')
    out.append('<p class="nlpg__fine">אומדן לא מחייב, לפי העסקאות והמחירים שפורסמו עד ' + num(d['updated_he']) + '. ' + rich(c['gap']) +
               ' המחיר נקבע מול המוכר.</p></form></div>')
    out.append('<p class="nlpg__src">' + rich(d['src_line']) + '</p></div></section>')
    return ''.join(out)


CSS = r"""
.nlpg{--pg-sea:var(--nlds-sa-sea,#2f6f86);--pg-seah:var(--nlds-sa-seah,#255c70);--pg-ink:var(--nlds-sa-ink,#14212b);--pg-ink2:var(--nlds-sa-ink2,#3b4753);--pg-line:var(--nlds-sa-line,#e3e1da);--pg-paper:var(--nlds-sa-paper,#f7f6f2);--pg-sand:var(--nlds-sa-sand,#eee9dd);--pg-surf:var(--nlds-sa-surf,#fff);--pg-deep:var(--nlds-sa-deep,#1f4b5c);--pg-serif:var(--nlds-font-serif,"Noto Serif Hebrew","David Libre",Georgia,serif);--pg-sans:var(--nlds-font-sans,Assistant,"Segoe UI",Arial,sans-serif);display:block !important;container-type:inline-size !important;container-name:nlpg !important;margin:clamp(18px,3vw,34px) auto 0 !important;max-width:var(--nlds-container,1240px) !important;padding:0 clamp(16px,3vw,32px) !important;box-sizing:border-box !important;font-family:var(--pg-sans) !important;color:var(--pg-ink) !important}
.nlpg *,.nlpg *::before,.nlpg *::after{box-sizing:border-box !important}
.nlps-page>.nlpg{grid-area:prices !important;margin:6px 0 0 !important;padding:0 !important;max-width:none !important;width:auto !important}
.nlpg .nlds-num{font-size:inherit !important;font-weight:inherit !important;color:inherit !important;direction:ltr !important;unicode-bidi:isolate !important;display:inline-block !important;font-variant-numeric:tabular-nums lining-nums !important}
.nlpg__in{display:grid !important;gap:var(--nlds-space-18,18px) !important;background:var(--pg-surf) !important;border:1px solid var(--pg-line) !important;border-radius:var(--nlds-radius-22,22px) !important;padding:clamp(18px,3vw,34px) !important}
.nlpg__head{display:grid !important;gap:8px !important}
.nlpg__title{font-family:var(--pg-serif) !important;font-weight:600 !important;font-size:clamp(23px,1.2rem + 1.1vw,31px) !important;line-height:1.22 !important;letter-spacing:-.005em !important;color:var(--pg-ink) !important;margin:0 !important;text-wrap:balance !important}
.nlpg__answer{font-size:clamp(15.5px,1rem + .15vw,17px) !important;line-height:1.7 !important;color:var(--pg-ink2) !important;margin:0 !important;max-width:78ch !important}
.nlpg__tiles{display:grid !important;grid-template-columns:repeat(3,minmax(0,1fr)) !important;gap:var(--nlds-space-12,12px) !important;margin:0 !important;padding:0 !important;list-style:none !important}
.nlpg__tiles li{display:grid !important;gap:3px !important;align-content:start !important;padding:14px 16px !important;background:var(--pg-paper) !important;border:1px solid var(--pg-line) !important;border-radius:var(--nlds-radius-14,14px) !important;margin:0 !important}
.nlpg__tiles b{font-family:var(--pg-serif) !important;font-size:clamp(20px,1rem + .9vw,25px) !important;font-weight:600 !important;line-height:1.2 !important;color:var(--pg-ink) !important}
.nlpg__tiles li>span{font-size:13.5px !important;line-height:1.45 !important;color:var(--pg-ink2) !important}
.nlpg__tiles i{font-style:normal !important;font-size:12.5px !important;color:var(--pg-ink2) !important}
.nlpg__grid{display:grid !important;grid-template-columns:minmax(0,1.25fr) minmax(300px,1fr) !important;gap:clamp(16px,2.4vw,28px) !important;align-items:start !important}
.nlpg__list{display:grid !important;gap:10px !important;min-width:0 !important}
.nlpg__table{width:100% !important;border-collapse:collapse !important;font-size:14.5px !important;line-height:1.45 !important;margin:0 !important;background:transparent !important}
.nlpg__cap{caption-side:top !important;text-align:start !important;font-family:var(--pg-serif) !important;font-weight:600 !important;font-size:19px !important;color:var(--pg-ink) !important;padding:0 0 6px !important}
.nlpg__table thead th{text-align:start !important;font-size:12px !important;font-weight:700 !important;letter-spacing:.03em !important;color:var(--pg-ink2) !important;padding:8px !important;border-bottom:1px solid var(--pg-line) !important;white-space:nowrap !important;background:transparent !important}
.nlpg__table td,.nlpg__table tbody th{padding:10px 8px !important;border-bottom:1px solid var(--pg-line) !important;vertical-align:middle !important;color:var(--pg-ink) !important;text-align:start !important;background:transparent !important;font-weight:400 !important}
.nlpg__table tbody th b{display:block !important;font-weight:600 !important;font-size:14.5px !important;color:var(--pg-ink) !important}
.nlpg__table tbody th>span{display:block !important;font-size:12.5px !important;color:var(--pg-ink2) !important;margin-top:1px !important}
.nlpg__table td{white-space:nowrap !important;font-variant-numeric:tabular-nums !important}
.nlpg__gh th{padding:16px 8px 6px !important;font-family:var(--pg-serif) !important;font-weight:600 !important;font-size:15.5px !important;color:var(--pg-deep) !important;border-bottom:1px solid var(--pg-line) !important;background:transparent !important}
.nlpg__grp:first-of-type .nlpg__gh th{padding-top:8px !important}
.nlpg__na{color:var(--pg-ink2) !important}
.nlpg__k{display:inline-block !important;font-size:12px !important;font-weight:600 !important;line-height:1 !important;padding:5px 9px !important;border-radius:999px !important;border:1px solid var(--pg-line) !important;color:var(--pg-ink2) !important;background:var(--pg-surf) !important;white-space:nowrap !important}
.nlpg__k--deal{background:#e6f0f3 !important;border-color:#c8dde4 !important;color:var(--pg-deep) !important}
.nlpg__k--ask{background:var(--pg-sand) !important;border-color:#ddd5c3 !important;color:#4a4232 !important}
.nlpg__k--med{background:#eef3ee !important;border-color:#cfdccf !important;color:#2c4a35 !important}
.nlpg__k--est,.nlpg__k--mkt{background:var(--pg-paper) !important;border-style:dashed !important;color:var(--pg-ink2) !important}
.nlpg:not(.is-open) .nlpg__grp--more{display:none !important}
.nlpg__more{justify-self:start !important;font:600 14.5px/1.2 var(--pg-sans) !important;color:var(--pg-sea) !important;background:transparent !important;border:1px solid var(--pg-line) !important;border-radius:999px !important;padding:10px 16px !important;min-height:44px !important;cursor:pointer !important}
.nlpg__more:hover{border-color:var(--pg-sea) !important;background:var(--pg-paper) !important}
.nlpg.is-open .nlpg__more{display:none !important}
.nlpg__mp{display:none !important}
.nlpg__calc{display:grid !important;gap:14px !important;background:var(--pg-paper) !important;border:1px solid var(--pg-line) !important;border-radius:var(--nlds-radius-16,16px) !important;padding:clamp(16px,2vw,22px) !important;box-shadow:var(--nlds-shadow-price-card,0 8px 24px rgba(17,17,15,.07),0 2px 6px rgba(17,17,15,.04)) !important;margin:0 !important}
.nlpg__ct{font-family:var(--pg-serif) !important;font-weight:600 !important;font-size:19px !important;line-height:1.3 !important;color:var(--pg-ink) !important;margin:0 !important}
.nlpg__f{display:grid !important;gap:7px !important;border:0 !important;margin:0 !important;padding:0 !important;min-width:0 !important}
.nlpg__f legend,.nlpg__f>label{font-size:13.5px !important;font-weight:700 !important;color:var(--pg-ink2) !important;padding:0 !important;margin:0 0 7px !important}
.nlpg__seg{display:flex !important;flex-wrap:wrap !important;gap:6px !important}
.nlpg__seg label{position:relative !important;margin:0 !important;cursor:pointer !important}
.nlpg__seg input{position:absolute !important;opacity:0 !important;inset:0 !important;margin:0 !important;cursor:pointer !important}
.nlpg__seg label>span{display:inline-flex !important;align-items:center !important;min-height:40px !important;padding:8px 14px !important;border-radius:999px !important;border:1px solid var(--pg-line) !important;background:var(--pg-surf) !important;font-size:14.5px !important;font-weight:600 !important;color:var(--pg-ink) !important;transition:background .2s,border-color .2s,color .2s !important}
.nlpg__seg label:hover>span{border-color:var(--pg-sea) !important}
.nlpg__seg input:checked+span{background:var(--pg-sea) !important;border-color:var(--pg-sea) !important;color:var(--nlds-on-sea,#fff) !important}
.nlpg__seg input:focus-visible+span{outline:2px solid var(--pg-sea) !important;outline-offset:3px !important}
.nlpg__rng{display:flex !important;align-items:center !important;gap:12px !important}
.nlpg__rng input[type=range]{flex:1 1 auto !important;min-width:0 !important;height:44px !important;margin:0 !important;accent-color:var(--pg-sea) !important;background:transparent !important;cursor:pointer !important}
.nlpg__rng output{flex:0 0 auto !important;min-width:86px !important;text-align:center !important;font-weight:700 !important;font-size:15px !important;color:var(--pg-ink) !important;background:var(--pg-surf) !important;border:1px solid var(--pg-line) !important;border-radius:10px !important;padding:7px 10px !important}
.nlpg__f[hidden]{display:none !important}
.nlpg__out{display:grid !important;gap:4px !important;background:var(--pg-surf) !important;border:1px solid var(--pg-line) !important;border-radius:14px !important;padding:14px 16px !important}
.nlpg__ol{font-size:12.5px !important;font-weight:700 !important;letter-spacing:.04em !important;color:var(--pg-sea) !important;margin:0 !important}
.nlpg__big{font-family:var(--pg-serif) !important;font-weight:600 !important;font-size:clamp(25px,1.1rem + 1.3vw,32px) !important;line-height:1.15 !important;color:var(--pg-ink) !important;margin:0 !important}
.nlpg__pm{font-size:14.5px !important;color:var(--pg-ink2) !important;margin:0 0 4px !important}
.nlpg__chart{direction:ltr !important;display:block !important;width:100% !important;height:auto !important;max-width:100% !important;margin:4px 0 2px !important;overflow:visible !important}
.nlpg__chart text{font-family:var(--pg-sans) !important;font-size:10.5px !important;fill:var(--pg-ink2) !important}
.nlpg__rows{display:grid !important;gap:2px !important;margin:6px 0 0 !important;padding:8px 0 0 !important;border-top:1px solid var(--pg-line) !important}
.nlpg__rows div{display:flex !important;justify-content:space-between !important;gap:12px !important;font-size:14.5px !important}
.nlpg__rows dt{color:var(--pg-ink2) !important;font-weight:400 !important;margin:0 !important}
.nlpg__rows dd{margin:0 !important;font-weight:700 !important;color:var(--pg-ink) !important}
.nlpg__why{font-size:12.5px !important;line-height:1.5 !important;color:var(--pg-ink2) !important;margin:6px 0 0 !important}
.nlpg__wa{display:flex !important;align-items:center !important;justify-content:center !important;width:100% !important;min-height:52px !important;margin:0 !important;padding:10px 22px !important;border-radius:999px !important;background:var(--pg-sea) !important;border:1px solid var(--pg-sea) !important;color:var(--nlds-on-sea,#fff) !important;font:700 16.5px/1.2 var(--pg-sans) !important;text-decoration:none !important;text-align:center !important}
.nlpg__wa:hover{background:var(--pg-seah) !important;border-color:var(--pg-seah) !important}
.nlpg__wa:focus-visible{outline:2px solid var(--pg-sea) !important;outline-offset:3px !important}
.nlpg__links{display:flex !important;flex-wrap:wrap !important;gap:6px 18px !important;margin:0 !important;font-size:14.5px !important}
.nlpg__links a{color:var(--pg-sea) !important;font-weight:600 !important;text-decoration:underline !important;text-decoration-color:var(--nlds-link-underline,rgba(47,111,134,.4)) !important;text-underline-offset:3px !important;min-height:44px !important;display:inline-flex !important;align-items:center !important}
.nlpg__fine{font-size:12.5px !important;line-height:1.55 !important;color:var(--pg-ink2) !important;margin:0 !important}
.nlpg__src{font-size:12.5px !important;line-height:1.55 !important;color:var(--pg-ink2) !important;margin:0 !important;max-width:90ch !important}
@container nlpg (max-width:860px){
 .nlpg__grid{grid-template-columns:minmax(0,1fr) !important}
 .nlpg__calc{order:-1 !important}
}
@container nlpg (max-width:620px){
 .nlpg__tiles{grid-template-columns:minmax(0,1fr) !important}
 .nlpg__tiles li{grid-template-columns:auto 1fr !important;column-gap:12px !important;align-items:baseline !important;padding:11px 14px !important}
 .nlpg__tiles li>span{grid-column:1/-1 !important}
 .nlpg__tiles li i{grid-row:1 !important;grid-column:2 !important;justify-self:end !important}
 .nlpg__table thead{display:none !important}
 .nlpg__table,.nlpg__table tbody,.nlpg__table tr{display:block !important;width:100% !important}
 .nlpg__table tbody tr:not(.nlpg__gh){display:grid !important;grid-template-columns:1fr 1fr !important;gap:4px 12px !important;padding:12px 0 !important;border-bottom:1px solid var(--pg-line) !important}
 .nlpg__table tbody tr:not(.nlpg__gh) th{grid-column:1/-1 !important;padding:0 !important;border:0 !important}
 .nlpg__table td{display:block !important;padding:0 !important;border:0 !important;white-space:normal !important}
 .nlpg__table td::before{content:attr(data-l) !important;display:block !important;font-size:11.5px !important;font-weight:700 !important;color:var(--pg-ink2) !important}
 .nlpg__gh th{display:block !important;padding:14px 0 4px !important}
 .nlpg__seg label>span{min-height:44px !important}
 .nlpg__in{border-radius:var(--nlds-radius-16,16px) !important;padding:16px !important}
 .nlpg:not(.is-open) .nlpg__table{display:none !important}
 .nlpg__mt{display:none !important}
 .nlpg__mp{display:inline !important}
 .nlpg__more{justify-self:stretch !important}
 .nlpg__chart text{font-size:12.5px !important}
}
@container nlpg (min-width:861px){.nlpg:not(.is-open) .nlpg__grp--more{display:table-row-group !important}.nlpg__more{display:none !important}}
@media (prefers-reduced-motion:reduce){.nlpg__seg label>span{transition:none !important}}
"""

JS = r"""
(function(){var NS='http://www.w3.org/2000/svg';
var nf=function(n){return new Intl.NumberFormat('he-IL',{maximumFractionDigits:0}).format(Math.round(n/100)*100)};
var mil=function(n){return (n/1e6).toFixed(2).replace(/\.?0+$/,'')};
var isl=function(s){return '<span class="nlds-num">'+s+'</span>'};
function tax(p,br){var a=0,prev=0;for(var i=0;i<br.length;i++){var cap=br[i][0],r=br[i][1],top=cap===null?p:Math.min(p,cap);if(top>prev)a+=(top-prev)*r;if(cap===null||p<=cap)break;prev=cap}return a}
function el(t,a,txt){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;return e}
function one(root){var f=root.querySelector('.nlpg__calc');if(!f||f.__nlpg)return;f.__nlpg=1;var C;try{C=JSON.parse(f.getAttribute('data-cfg'))}catch(e){return}
 var q=function(k){return f.querySelector('[data-pg="'+k+'"]')};
 var val=function(n){var x=f.querySelector('input[name^="'+n+'"]:checked');return x?x.value:''};
 var mode=function(){var id=val('nlpg-m');for(var i=0;i<C.modes.length;i++)if(C.modes[i].id===id)return C.modes[i];return C.modes[0]};
 function draw(m,lo,hi,floor){var s=q('ch');if(!s)return;while(s.lastChild&&s.lastChild.nodeName!=='title')s.removeChild(s.lastChild);
  var L=44,R=330,T=12,B=112;
  if(m.floor){var y0=50000,y1=82000,X=function(fl){return L+(fl-1)*(R-L)/39},Y=function(v){return B-(v-y0)*(B-T)/(y1-y0)};
   var up=[],dn=[];for(var fl=1;fl<=40;fl++){var p=m.lo_floor1+(fl-1)*(m.hi_floor39-m.lo_floor1)/38;up.push(X(fl)+','+Y(p*(1+m.band)));dn.unshift(X(fl)+','+Y(p*(1-m.band)))}
   [[60000,'60,000'],[70000,'70,000'],[80000,'80,000']].forEach(function(g){s.appendChild(el('line',{x1:L,x2:R,y1:Y(g[0]),y2:Y(g[0]),stroke:'#e3e1da','stroke-width':1}));s.appendChild(el('text',{x:L-6,y:Y(g[0])+3.5,'text-anchor':'end'},g[1]))});
   s.appendChild(el('polygon',{points:up.concat(dn).join(' '),fill:'rgba(47,111,134,.14)'}));
   s.appendChild(el('line',{x1:L,x2:R,y1:Y(C.avg),y2:Y(C.avg),stroke:'#1f4b5c','stroke-width':1.2,'stroke-dasharray':'4 3'}));
   s.appendChild(el('text',{x:L+4,y:Y(C.avg)-5,'text-anchor':'start'},'ממוצע העסקאות, כ-65,000'));
   var fx=X(floor),pm=(lo+hi)/2;s.appendChild(el('line',{x1:fx,x2:fx,y1:T-4,y2:B,stroke:'#2f6f86','stroke-width':1.5}));
   s.appendChild(el('circle',{cx:fx,cy:Y(pm),r:5.5,fill:'#2f6f86',stroke:'#fff','stroke-width':2}));
   C.deals.forEach(function(d){s.appendChild(el('circle',{cx:X(d[0]),cy:Y(d[1]),r:4,fill:'#fff',stroke:'#14212b','stroke-width':1.6}))});
   s.appendChild(el('text',{x:X(36.6),y:Y(77600),'text-anchor':'end'},'עסקאות שפורסמו'));
   s.appendChild(el('text',{x:L,y:B+16,'text-anchor':'start'},'קומה 1'));s.appendChild(el('text',{x:R,y:B+16,'text-anchor':'end'},'קומה 40'));
   s.appendChild(el('text',{x:(L+R)/2,y:B+16,'text-anchor':'middle'},'₪ למ״ר לפי הקומה'));
   s.setAttribute('aria-label','אומדן של '+nf(lo)+' עד '+nf(hi)+' ₪ למ״ר בקומה '+floor+', מול ממוצע העסקאות במגדלים, כ-65,000 ₪');
  }else{var x0=40000,x1=115000,X2=function(v){return L+(v-x0)*(R-L)/(x1-x0)};
   [['הבחירה שלכם',m.lo,m.hi,1],['מגדלי כיכר המדינה, ממוצע',C.avg,C.avg,0],['תל אביב יפו, חציון',C.ta,C.ta,0]].forEach(function(r,i){var y=24+i*36;
    s.appendChild(el('text',{x:R,y:y-9,'text-anchor':'end'},r[0]));
    s.appendChild(el('line',{x1:X2(x0),x2:X2(x1),y1:y,y2:y,stroke:'#e3e1da','stroke-width':6,'stroke-linecap':'round'}));
    if(r[3]){s.appendChild(el('line',{x1:X2(r[1]),x2:X2(r[2]),y1:y,y2:y,stroke:'#2f6f86','stroke-width':8,'stroke-linecap':'round'}));
     s.appendChild(el('text',{x:X2(r[1]),y:y+17,'text-anchor':'middle'},nf(r[1])));s.appendChild(el('text',{x:X2(r[2]),y:y+17,'text-anchor':'middle'},nf(r[2])))}
    else{s.appendChild(el('circle',{cx:X2(r[1]),cy:y,r:5.5,fill:'#1f4b5c',stroke:'#fff','stroke-width':2}));s.appendChild(el('text',{x:X2(r[1]),y:y+17,'text-anchor':'middle'},nf(r[1])))}});
   s.setAttribute('aria-label',m.label+': '+nf(m.lo)+' עד '+nf(m.hi)+' ₪ למ״ר, מול ממוצע המגדלים כ-65,000 ₪ ותל אביב יפו 52,856 ₪');
  }}
 function run(){var m=mode(),a=+q('a').value,fl=+q('fs').value,lo,hi;
  q('fl').hidden=!m.floor;q('ao').innerHTML=isl(a)+' מ״ר';q('fo').innerHTML='קומה '+isl(fl);
  if(m.floor){var p=m.lo_floor1+(fl-1)*(m.hi_floor39-m.lo_floor1)/38;lo=p*(1-m.band);hi=p*(1+m.band)}else{lo=m.lo;hi=m.hi}
  var mid=(lo+hi)/2*a,t=tax(mid,val('nlpg-t')==='more'?C.tax2:C.tax1);
  q('p').innerHTML=isl(mil(lo*a)+'-'+mil(hi*a))+' מיליון ₪';q('pm').innerHTML='כ-'+isl(nf(lo)+'-'+nf(hi))+' ₪ למ״ר';
  q('tx').innerHTML='כ-'+isl(new Intl.NumberFormat('he-IL').format(Math.round(t/1000)*1000))+' ₪';q('tt').innerHTML='כ-'+isl(mil(mid+t))+' מיליון ₪';
  q('why').textContent=m.why;draw(m,lo,hi,fl);
  var w=q('wa');if(w&&C.wa){var tx='שלום, בדקתי במחירון של מגדלי כיכר המדינה: '+m.label+', '+a+' מ״ר'+(m.floor?', קומה '+fl:'')+', אומדן '+mil(lo*a)+'-'+mil(hi*a)+' מיליון ₪. אשמח לפרטים נוספים (nad-lan.co.il)';w.href='https://wa.me/'+C.wa+'?text='+encodeURIComponent(tx)}}
 f.addEventListener('input',run);f.addEventListener('change',run);f.addEventListener('submit',function(e){e.preventDefault()});
 var mb=root.querySelector('.nlpg__more');if(mb)mb.addEventListener('click',function(){root.classList.add('is-open');mb.setAttribute('aria-expanded','true');var g=root.querySelector('.nlpg__grp--more .nlpg__gh th');if(g){g.setAttribute('tabindex','-1');g.focus({preventScroll:true})}});
 run()}
var all=document.querySelectorAll('.nlpg');for(var i=0;i<all.length;i++)one(all[i])})();
"""


if __name__ == '__main__':
    import io, os, sys
    here = os.path.dirname(os.path.abspath(__file__))
    d = json.load(io.open(os.path.join(here, 'hamedina.json'), encoding='utf-8'))
    print(default_result(d))
    print(len(html(d, '972525101555')), 'bytes of markup;', len(CSS), 'css;', len(JS), 'js')
