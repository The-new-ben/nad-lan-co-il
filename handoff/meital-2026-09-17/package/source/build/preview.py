#!/usr/bin/env python3
"""Build the review preview: every listing in Hebrew and English plus the catalog, with hash routing."""
import json, os, html
import build as B
import package as P

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@300;400;500;600;700&family=Assistant:wght@300;400;500;600;700;800&family=Noto+Serif+Display:ital,wght@0,400;1,300&display=swap">'

CHROME_CSS = """
:root{--pv-ink:#14212B;--pv-mute:#6B7680;--pv-line:#E3E1DA;--pv-paper:#F7F6F2;--pv-sea:#2F6F86;--pv-deep:#1F4B5C;--nlx-header-offset:64px;color-scheme:light}
html,body{background:var(--pv-paper);color:var(--pv-ink)}
body{margin:0;font-family:Assistant,'Segoe UI',Arial,sans-serif}
.pv-bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:50;background:rgba(247,246,242,.94);backdrop-filter:saturate(1.2) blur(8px);-webkit-backdrop-filter:saturate(1.2) blur(8px);border-bottom:1px solid var(--pv-line)}
.pv-bar-in{max-width:1240px;margin:0 auto;padding:10px 16px;display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px}
.pv-brand{display:flex;align-items:baseline;gap:10px;min-width:0;margin-inline-end:auto}
.pv-brand b{font-family:'Noto Serif Hebrew',Georgia,serif;font-weight:600;font-size:18px;white-space:nowrap}
.pv-flag{font-size:12px;font-weight:700;letter-spacing:.03em;color:#7A4B12;background:#F6E7CF;border:1px solid #EBD3AC;border-radius:999px;padding:2px 10px;white-space:nowrap}
.pv-controls{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.pv-seg{display:inline-flex;border:1px solid var(--pv-line);border-radius:999px;background:#fff;padding:3px}
.pv-seg button{font:inherit;font-size:14px;font-weight:600;border:0;background:transparent;color:var(--pv-ink);padding:6px 14px;border-radius:999px;cursor:pointer}
.pv-seg button[aria-pressed="true"]{background:var(--pv-deep);color:#fff}
.pv-seg button:focus-visible,.pv-select:focus-visible,.pv-home:focus-visible{outline:2px solid var(--pv-sea);outline-offset:2px}
.pv-select{font:inherit;font-size:14px;max-width:min(78vw,340px);border:1px solid var(--pv-line);border-radius:999px;background:#fff;color:var(--pv-ink);padding:7px 12px}
.pv-home{font-size:14px;font-weight:600;color:var(--pv-sea);text-decoration:none;padding:6px 4px}
.pv-note{max-width:1240px;margin:0 auto;padding:14px 16px 0;font-size:14px;color:var(--pv-mute);line-height:1.6}
.pv-main{max-width:1240px;margin:0 auto;padding:8px 16px 72px}
@media (max-width:700px){
  :root{--nlx-header-offset:0px}
  .pv-bar{position:static}
  .pv-bar-in{gap:8px}
  .pv-controls{flex:1 1 100%;flex-wrap:nowrap}
  .pv-home{display:none}
  .pv-select{flex:1 1 0;width:0;min-width:0;max-width:none}
}
.pv-full{margin:0}
.pv-full .nlb-mbar{bottom:0}
.pv-toast{position:fixed;inset-inline:16px;bottom:calc(20px + env(safe-area-inset-bottom,0px));margin-inline:auto;max-width:420px;background:var(--pv-ink);color:#fff;font-size:14px;border-radius:10px;padding:10px 14px;text-align:center;z-index:60}
"""

JS = """
(function(){
  var views = Array.prototype.slice.call(document.querySelectorAll('.pv-view'));
  var jump = document.getElementById('pv-jump');
  var toast = document.getElementById('pv-toast');
  var langBtns = Array.prototype.slice.call(document.querySelectorAll('[data-pv-lang]'));
  var t;
  function parse(){
    var h = (location.hash || '').replace('#','');
    var m = h.match(/^(broker|catalog|L\\d\\d)-(he|en)$/);
    return m ? {id:m[1], lang:m[2]} : {id:'broker', lang:'he'};
  }
  function show(){
    var s = parse();
    var key = s.id + '-' + s.lang;
    views.forEach(function(v){ v.hidden = (v.getAttribute('data-key') !== key); });
    document.documentElement.setAttribute('lang', s.lang);
    document.documentElement.setAttribute('dir', s.lang === 'he' ? 'rtl' : 'ltr');
    langBtns.forEach(function(b){ b.setAttribute('aria-pressed', String(b.getAttribute('data-pv-lang') === s.lang)); });
    if (jump) { jump.value = s.id; }
    document.querySelectorAll('[data-pv-i18n]').forEach(function(el){
      var v = el.getAttribute('data-' + s.lang); if (v) { el.textContent = v; }
    });
    window.scrollTo(0, 0);
  }
  function go(id, lang){ location.hash = id + '-' + lang; }
  langBtns.forEach(function(b){ b.addEventListener('click', function(){ go(parse().id, b.getAttribute('data-pv-lang')); }); });
  if (jump) { jump.addEventListener('change', function(){ go(jump.value, parse().lang); }); }
  document.addEventListener('click', function(e){
    var a = e.target.closest ? e.target.closest('a') : null;
    if (!a) { return; }
    var card = a.closest('.nlx-card-l');
    if (card) { e.preventDefault(); go(card.getAttribute('data-listing'), parse().lang); return; }
    var bcard = a.closest('.nlb-lcard');
    if (bcard && !a.closest('.nlb-lcard-cta .nlb-btn--sea')) { e.preventDefault(); go(bcard.id.split('-').pop(), parse().lang); return; }
    if (a.closest('.nlb-feature') && a.classList.contains('nlb-btn--line')) { e.preventDefault(); go('L01', parse().lang); return; }
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) === '#' && href.length > 1 && !/^#(broker|catalog|L\\d\\d)-(he|en)$/.test(href)) {
      var target = document.getElementById(href.slice(1));
      if (target) { e.preventDefault(); target.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block:'start'}); }
      return;
    }
    if (a.closest('.nlx-cta') || a.closest('.nlx-mbar') || a.closest('.nlb-cta') || a.closest('.nlb-mbar') || a.closest('.nlb-lcard-cta') || a.closest('.nlb-igtile')) {
      e.preventDefault();
      toast.textContent = parse().lang === 'he' ? 'בתצוגה המקדימה קישורי וואטסאפ וחיוג מושבתים.' : 'WhatsApp and call links are disabled in this preview.';
      toast.hidden = false; clearTimeout(t); t = setTimeout(function(){ toast.hidden = true; }, 2600);
    }
  });
  window.addEventListener('hashchange', show);
  show();
})();
"""

def build_preview(full_document):
    res = B.render_all(P.IDS)
    eds = [B.load_ed(i) for i in P.IDS]
    css = open(B.B + 'assets/nlx-prestige.css').read() + open(B.B + 'broker/nlb-broker.css').read()
    opts_he, opts_en = [], []
    views = []
    full_views = []
    for lang in ('he', 'en'):
        bh = open(B.BASE + f'dist/broker/broker-{lang}.html').read()
        full_views.append(f'<div class="pv-view pv-full" data-key="broker-{lang}" hidden>{bh}</div>')
    for lang in ('he', 'en'):
        views.append(f'<div class="pv-view" data-key="catalog-{lang}" lang="{lang}" dir="{"rtl" if lang == "he" else "ltr"}" hidden>{P.catalog(eds, lang)}</div>')
    for ed in eds:
        for lang in ('he', 'en'):
            h = res[(ed['id'], lang)][0]
            views.append(f'<div class="pv-view" data-key="{ed["id"]}-{lang}" hidden>{h}</div>')
    options = ['<option value="broker" data-pv-i18n data-he="עמוד המתווכת: מיטל קציר" data-en="Broker page: Meital Katzir">עמוד המתווכת: מיטל קציר</option>',
               '<option value="catalog" data-pv-i18n data-he="כל הנכסים" data-en="All listings">כל הנכסים</option>']
    for ed in eds:
        t_he = B.L_(ed['title'], 'he'); t_en = B.L_(ed['title'], 'en')
        options.append(f'<option value="{ed["id"]}" data-pv-i18n data-he="{html.escape(ed["id"] + " · " + t_he)}" data-en="{html.escape(ed["id"] + " · " + t_en)}">{html.escape(ed["id"] + " · " + t_he)}</option>')
    bar = ('<header class="pv-bar"><div class="pv-bar-in">'
           '<div class="pv-brand"><b>nad-lan</b><span class="pv-flag" data-pv-i18n data-he="טיוטה פנימית, לא פורסם" data-en="Internal draft, not published">טיוטה פנימית, לא פורסם</span></div>'
           '<div class="pv-controls">'
           '<a class="pv-home" href="#broker-he" data-pv-i18n data-he="עמוד המתווכת" data-en="Broker page" onclick="event.preventDefault();location.hash=\'broker-\'+(document.documentElement.lang||\'he\');">עמוד המתווכת</a>'
           f'<label class="pv-sr" for="pv-jump" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Listing</label><select class="pv-select" id="pv-jump">{"".join(options)}</select>'
           '<div class="pv-seg" role="group" aria-label="Language"><button type="button" data-pv-lang="he" aria-pressed="true">עברית</button><button type="button" data-pv-lang="en" aria-pressed="false">English</button></div>'
           '</div></div></header>')
    note = ('<p class="pv-note" data-pv-i18n data-he="עמוד מתווכת ו-11 עמודי נכס בעברית ובאנגלית, מוכנים להעלאה כטיוטות לוורדפרס. הנתונים נכונים ל-16.9.2026. תמונות יתקבלו מהמשווקת, ועד אז מוצגים איורים שאינם מתארים את הנכסים. הערות פנימיות ורשימות אישור נמצאות בקבצי החבילה בלבד." '
            'data-en="A broker page and 11 listing pages in Hebrew and English, ready to import as WordPress drafts. Data as of 16 Sep 2026. Photos will come from the broker; until then illustrations that depict no real property are shown. Internal notes and approval lists live only in the package files.">'
            'עמוד מתווכת ו-11 עמודי נכס בעברית ובאנגלית, מוכנים להעלאה כטיוטות לוורדפרס. הנתונים נכונים ל-16.9.2026. תמונות יתקבלו מהמשווקת, ועד אז מוצגים איורים שאינם מתארים את הנכסים. הערות פנימיות ורשימות אישור נמצאות בקבצי החבילה בלבד.</p>')
    body = bar + note + ''.join(full_views) + '<main class="pv-main">' + ''.join(views) + '</main><div class="pv-toast" id="pv-toast" role="status" hidden></div><script>' + JS + '</script>'
    title = '<title>רשימות היוקרה של nad-lan</title>'
    style = '<style>' + CHROME_CSS + css + '</style>'
    if full_document:
        return '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + title + FONTS + style + '</head><body>' + body + '</body></html>'
    return title + FONTS + style + body

if __name__ == '__main__':
    art = build_preview(False)
    full = build_preview(True)
    os.makedirs(P.PKG + 'preview', exist_ok=True)
    open(P.PKG + 'preview/index.html', 'w').write(full)
    open(B.BASE + 'dist/preview-artifact.html', 'w').write(art)
    print('artifact', len(art.encode()), 'bytes; full', len(full.encode()))
