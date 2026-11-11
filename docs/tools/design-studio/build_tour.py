# -*- coding: utf-8 -*-
"""HAD-708: build the page every project opens for "עיצוב הדירה": plugins/nadlan-config/assets/tours/designer-tour.html.
The address /tour/designer/ already exists and every project page links to it (inc/tour-routes.php streams the plugin copy);
this file REPLACES the July demonstration with the new designer: the project's own plans when we hold them (plans/index.json),
else the example apartments, and always "התוכנית שלי" (the visitor's own plan). No page of the site changes, nothing redirects.
The page stays noindex exactly as the file it replaces.     python build_tour.py <plugin version, e.g. 1.72.653>"""
import io, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
DSG = os.path.join(REPO, "plugins", "nadlan-config", "assets", "designer")
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "tours", "designer-tour.html")
if len(sys.argv) < 2 or not re.match(r"^\d+\.\d+\.\d+$", sys.argv[1]):
    raise SystemExit("usage: python build_tour.py <version like 1.72.653>")
V = sys.argv[1]
B = "/wp-content/plugins/nadlan-config/assets/designer/"
SHIP = ("budget.js", "call.js", "catalog.js", "core.js", "designer.js", "plan.js", "planbuild.js", "planmaker.js", "space.js", "strings.js", "studio.js")
EXTRA = tuple(a for a in sys.argv[2:] if a.endswith(".js"))  # modules a later release adds: python build_tour.py <version> roomscan.js ...
mods = sorted(f for f in SHIP + EXTRA if os.path.isfile(os.path.join(DSG, f)))
assert len(mods) == len(SHIP) + len(EXTRA), "a module of the page is missing on disk"
imports = ['"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js"', '"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"']
imports += ['"%s%s":"%s%s?v=%s"' % (B, f, B, f, V) for f in mods]
IMPORTMAP = '{"imports":{' + ",".join(imports) + "}}"

HTML = r"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0F2233">
<title>עיצוב הדירה בתלת ממד | nad-lan.co.il</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" data-nd-fonts href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Hebrew:wght@400;600;700&display=swap">
<script type="importmap">__IMPORTMAP__</script>
<style>
:root{--sheet:#F2F5F7;--ink:#0F2233;--ink2:#46596A;--blue:#1F5FA8;--blue2:#D6E5F6;--line:#B9C6CF;--card:#fff}
*{box-sizing:border-box}
html,body{height:100%;margin:0;overflow:hidden;max-width:100%}
body{background:var(--sheet);color:var(--ink);font:15px/1.4 "IBM Plex Sans Hebrew",Arial,sans-serif;display:grid;grid-template-rows:auto auto auto minmax(0,1fr);grid-template-columns:minmax(0,1fr);height:100vh;height:100dvh;overflow:hidden;-webkit-tap-highlight-color:transparent}
a{color:inherit}
button{font:inherit;color:inherit;cursor:pointer}
:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
[hidden]{display:none!important}
.top{display:flex;align-items:stretch;gap:0;background:var(--card);border-bottom:2px solid var(--ink);min-height:52px}
.top .back{flex:none;width:52px;display:flex;align-items:center;justify-content:center;border-inline-end:2px solid var(--ink);text-decoration:none}
.top .back svg{width:22px;height:22px}
.ttl{flex:1;min-width:0;display:flex;flex-direction:column;justify-content:center;padding:4px 12px}
.ttl b{font-size:16px;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ttl span{font-size:12px;color:var(--ink2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.top .send{flex:none;display:flex;align-items:center;gap:8px;padding:0 14px;background:var(--blue);color:#fff;border:0;border-inline-start:2px solid var(--ink);font-weight:700;font-size:14px}
.top .send svg{width:20px;height:20px;fill:currentColor;flex:none}
.top .send i{font-style:normal}.top .send b{font-weight:inherit}
.pick{display:flex;gap:0;padding:8px 10px 8px;overflow-x:auto;scrollbar-width:none;background:var(--sheet)}
.pick::-webkit-scrollbar{display:none}
.pick button{flex:none;min-height:44px;padding:0 14px;background:var(--card);border:2px solid var(--ink);margin-inline-start:-2px;font-size:14px;font-weight:600;white-space:nowrap}
.pick button:first-child{margin-inline-start:0}
.pick button[aria-pressed=true]{background:var(--ink);color:#fff}
.pick button.is-mine{border-color:var(--blue);color:var(--blue);position:relative;z-index:1;margin-inline-end:10px}
.pick button.is-mine[aria-pressed=true]{background:var(--blue);color:#fff}
.tip{display:flex;align-items:stretch;gap:0;margin:0 10px 8px;font-size:13.5px;color:var(--ink);background:var(--blue2);border-inline-start:4px solid var(--blue)}
.tip p{margin:0;flex:1;min-width:0;padding:6px 10px;align-self:center}
.tip button{flex:none;width:44px;min-height:44px;border:0;background:none;font-size:20px;line-height:1}
.top{grid-row:1}.pick{grid-row:2}.tip{grid-row:3}
#host{grid-row:4;position:relative;min-height:0;min-width:0;width:100%;height:100%;border-top:2px solid var(--ink);overflow:hidden;contain:layout paint}
.wait{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--ink2);font-size:14px}
dialog{border:2px solid var(--ink);padding:0;max-width:min(92vw,440px);background:var(--card);color:var(--ink)}
dialog::backdrop{background:rgba(15,34,51,.55)}
.dl{padding:18px 18px 16px}
.dl h2{margin:0 0 8px;font-size:18px}
.dl p{margin:0 0 14px;font-size:14.5px;line-height:1.55}
.dl .go{display:flex;align-items:center;justify-content:center;gap:8px;min-height:48px;background:var(--blue);color:#fff;font-weight:700;text-decoration:none;padding:0 14px}
.dl .go svg{width:20px;height:20px;fill:currentColor}
.dl .no{display:block;width:100%;min-height:44px;margin-top:8px;background:none;border:2px solid var(--ink);font-weight:600}
@media (max-width:520px){.top .send b{display:none}.top .send{padding:0 12px;gap:6px}.ttl{padding:4px 10px}}
</style>
</head>
<body>
<header class="top">
  <a class="back" id="back" href="/design-studio/" aria-label="חזרה"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></a>
  <div class="ttl"><b id="ttl">עיצוב הדירה</b><span id="sub">תוכנית ותלת ממד, רהיטים במידות אמיתיות ותקציב משוער</span></div>
  <button class="send" id="send" type="button" aria-label="שליחת העיצוב לנציג בוואטסאפ"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.87 9.87 0 0 0 4.79 1.22c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Z"/></svg><span><i>שליחה</i><b> לנציג</b></span></button>
</header>
<div class="pick nadlan-designer-pick" id="pick" role="group" hidden></div>
<div class="tip" id="tip" hidden><p>יש לכם תוכנית של הדירה? לחצו על ״התוכנית שלי״ וטענו אותה.</p><button type="button" id="tipx" aria-label="סגירה">×</button></div>
<main id="host" class="nadlan-designer"><div class="wait" id="wait">טוען את המעצב</div></main>
<dialog id="dlg" aria-labelledby="dlgh">
  <div class="dl">
    <h2 id="dlgh">שליחת העיצוב לנציג</h2>
    <p>שלחו לנו את העיצוב בוואטסאפ: התוכנית, הריהוט והתקציב המשוער. נציג נדל״ן יחזור אליכם ויתאם את ההמשך מול היזם. אין תשלום באתר ואין התחייבות.</p>
    <a class="go" id="wa" href="https://wa.me/972525101555" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.87 9.87 0 0 0 4.79 1.22c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Z"/></svg><span>שליחת העיצוב לנציג בוואטסאפ</span></a>
    <button class="no" type="button" id="dlgx">חזרה לעיצוב</button>
  </div>
</dialog>
<noscript><p style="padding:16px">המעצב צריך דפדפן עם JavaScript. <a href="/design-studio/">לדף עיצוב הדירה</a></p></noscript>
<script type="module">
const V = '__V__', B = '__B__', WA = 'https://wa.me/972525101555';
const $ = (id) => document.getElementById(id);
const q = new URLSearchParams(location.search);
const clean = (s, n) => String(s || '').replace(/[<>"'`\\]/g, '').replace(/\s+/g, ' ').trim().slice(0, n);
const pn = clean(q.get('pn'), 60), ul = clean(q.get('ul'), 80), unit = clean(q.get('unit'), 40).replace(/[^A-Za-z0-9_.-]/g, '');
let ref = null;
try { ref = document.referrer ? new URL(document.referrer) : null; } catch (e) { ref = null; }
const sameRef = !!ref && ref.origin === location.origin;
const refProject = sameRef ? (ref.pathname.match(/^\/projects\/([a-z0-9-]+)\/?$/) || [])[1] || '' : '';
const slug = (clean(q.get('project'), 80).toLowerCase().replace(/[^a-z0-9-]/g, '') || refProject).replace(/-(en|fr|ru|ar)$/, '');

// the way back: the project page the visitor came from, else that project's page, else the design page
const back = $('back');
if (refProject) { back.href = ref.pathname; back.setAttribute('aria-label', 'חזרה לפרויקט'); }
else if (slug) { back.href = '/projects/' + slug + '/'; back.setAttribute('aria-label', 'חזרה לפרויקט'); }
else if (sameRef && history.length > 1) { back.addEventListener('click', (e) => { e.preventDefault(); history.back(); }); }
if (pn) { $('ttl').textContent = 'עיצוב הדירה · ' + pn; document.title = 'עיצוב הדירה · ' + pn + ' | nad-lan.co.il'; }
if (ul) $('sub').textContent = ul;

const host = $('host'), pick = $('pick');
let st = null, catalog = null;
const roomsWanted = Number((ul.match(/(\d)(?:[.,]5)?\s*חדרים/) || [])[1] || 0);

(async () => {
  let idx = null;
  try { const r = await fetch(B + 'plans/index.json?v=' + V); idx = r.ok ? await r.json() : null; } catch (e) { idx = null; }
  const all = (idx && Array.isArray(idx.plans) ? idx.plans : []).filter((p) => p && p.file);
  const projects = (idx && idx.projects) || {};
  const pkey = slug ? Object.keys(projects).find((k) => k === slug || projects[k].slug === slug) || '' : '';
  const url = (p) => B + 'plans/' + p.file + '?v=' + V;
  const real = pkey ? all.filter((p) => p.project === pkey).sort((a, b) => a.rooms - b.rooms) : [];
  let plans, dflt;
  if (real.length) {
    plans = real.map((p) => ({ k: url(p).split('?')[0], url: url(p), label: p.rooms + ' חדרים · ' + p.type, real: true, type: p.type, rooms: p.rooms }));
    const want = real.find((p) => roomsWanted && p.rooms === roomsWanted) || real.find((p) => p.type === projects[pkey].default) || real[0];
    dflt = url(want);
  } else {
    const ex = all.filter((p) => !p.project).sort((a, b) => a.rooms - b.rooms);
    plans = (ex.length ? ex : [{ file: 'example-4r.json', rooms: 4 }]).map((p) => ({ k: url(p).split('?')[0], url: url(p), label: p.rooms + ' חדרים', rooms: p.rooms }));
    const want = plans.find((p) => roomsWanted && p.rooms === roomsWanted) || plans.find((p) => p.rooms === 4) || plans[0];
    dflt = want.url;
  }
  const mk = (pl, u, x) => {
    const plan = JSON.parse(JSON.stringify(pl));
    const o = { plan, lang: 'he', version: V };
    if (x && x.mine) { o.title = 'התוכנית שלי'; o.unitLabel = 'שרטוט שלכם'; return o; }
    if (slug) plan.unit = Object.assign({}, plan.unit, { project: slug, unit_id: unit || plan.unit.unit_id || null }); // the design is kept for THIS project and unit
    if (x && x.real) { o.title = 'טיפוס ' + x.type; o.unitLabel = 'לפי תוכנית המכר שפורסמה'; }
    else { o.title = 'דירה לדוגמה'; if (slug || pn) o.unitLabel = 'לא תוכנית הדירה בפרויקט'; }
    return o;
  };
  try {
    const { mountStudio } = await import(B + 'studio.js?v=' + V);
    $('wait').remove();
    st = await mountStudio(host, pick, { plans, planUrl: dflt, mk, lang: 'he', version: V, project: slug || null, scope: slug || '', helpUrl: '/design-studio/#get-plan', rest: '/wp-json/nadlan/v1/designer/', // the video call (HAD-706): rooms and tokens from the site, the apartment travels in the call
      start: q.get('plan') === 'mine' ? 'mine' : '', onChange: (kind) => { if (kind !== 'plan') hideTip(); } });
  } catch (e) { st = null; if (window.console) console.error(e); }
  if (!st) { host.innerHTML = '<div class="wait">המעצב לא נטען. <a href="/design-studio/">לדף עיצוב הדירה</a></div>'; return; }
  let seen = false;
  try { seen = localStorage.getItem('nl-dsg-tip') === '1'; } catch (e) { seen = false; }
  if (!seen && st.current !== 'mine') $('tip').hidden = false;
})();
function hideTip() { $('tip').hidden = true; try { localStorage.setItem('nl-dsg-tip', '1'); } catch (e) { /* storage blocked */ } }
$('tipx').addEventListener('click', hideTip);

// the request path the old page had: the design goes to a representative by WhatsApp, written from the design itself
async function waText() {
  const L = ['היי נד״לן! סיימתי לעצב דירה במעצב הדירות:'];
  if (pn) L.push('• פרויקט: ' + pn);
  if (ul) L.push('• הדירה: ' + ul);
  const d = st && st.designer;
  if (d) {
    try {
      catalog = catalog || (await import(B + 'catalog.js'));
      const qn = d.quantities(), ds = d.getDesign(), nf = new Intl.NumberFormat('he-IL');
      const src = st.current === 'mine' ? 'התוכנית שלי' : (d.store && d.store.apt && d.store.apt.source && d.store.apt.source.label_he) || '';
      if (src) L.push('• התוכנית: ' + src);
      L.push('• שטח: ' + qn.net.toFixed(1) + ' מ״ר' + (qn.balcony ? ' ועוד מרפסת ' + qn.balcony.toFixed(1) + ' מ״ר' : ''));
      const names = Object.keys(qn.items || {}).map((k) => (catalog.ITEMS[k] ? catalog.ITEMS[k].he + (qn.items[k] > 1 ? ' ×' + qn.items[k] : '') : '')).filter(Boolean);
      if (names.length) L.push('• ריהוט שהוספתי: ' + names.slice(0, 12).join(', '));
      const b = d.budget && d.budget();
      if (b && b.ready && b.lo) L.push('• תקציב משוער: ' + nf.format(b.lo) + (b.open || b.hi == null ? ' ₪ ומעלה' : ' עד ' + nf.format(b.hi) + ' ₪'));
      const g = (ds && ds.geometry) || {};
      if ((g.added || []).length || (g.removed || []).length) L.push('• שינויי מחיצות: ' + ((g.added || []).length + (g.removed || []).length));
    } catch (e) { /* the message still goes, shorter */ }
  }
  L.push('אשמח שנתקדם!');
  return L.join('\n');
}
const dlg = $('dlg');
$('send').addEventListener('click', async () => {
  $('wa').href = WA + '?text=' + encodeURIComponent(await waText());
  if (dlg.showModal) dlg.showModal(); else window.open($('wa').href, '_blank', 'noopener');
});
$('dlgx').addEventListener('click', () => dlg.close());
$('wa').addEventListener('click', () => { if (dlg.open) dlg.close(); });
</script>
</body>
</html>
"""
html = HTML.replace("__IMPORTMAP__", IMPORTMAP).replace("__V__", V).replace("__B__", B)
if "—" in html or "–" in html:
    raise SystemExit("a long dash in the page text")
with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print("written", os.path.relpath(OUT, REPO), len(html.encode("utf-8")), "bytes | modules in the map:", len(mods), "| version", V)
