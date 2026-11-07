/* NadLan Instruments · panatomy v1 (HAD-681, Ben 7.11.2026): "מה יש בתוך המחיר של דירה חדשה" on /apartment-prices/.
   The bill of materials of a new apartment's price, with STRICT HONESTY: a part gets a number only with a named, dated public
   source kept in anatomy.json (tools/instruments/build_anatomy_data.py), shown next to it; a part with no such source is a named
   slice with its explanation and no number.
   - The developer's side: the Bank of Israel split (land about a third, construction about a third, the rest to developer profit
     and taxes; national average 2009-2010), or the land share alone for the centre (about a third) and the periphery (about a
     tenth) at the 2011 peak; the VAT inside the price computed exactly at today's 18%. Tap a part: its sub-parts (land, development
     levies, betterment levy 50% of the added value, purchase tax on land; frame, finishing, systems, safe room, underground parking,
     elevators with the construction-input index trend; VAT, developer profit, financing, planning and permits, marketing).
   - The buyer's side on top of the price: purchase tax by bracket for the chosen price and track (ptax.json), lawyer, broker,
     appraiser, inspection and the mortgage file fee (cost.json), and the index linkage of a new apartment's payments.
   It ends with the two calculators that own the exact numbers: /purchase-tax-calculator/ and /apartment-purchase-cost-calculator/. */
(function () {
  'use strict';
  if (!window.NadLanInstruments || !window.NLPH || !window.NLPH.ui) return;
  var NI = window.NadLanInstruments, P = window.NLPH, U = P.ui, esc = U.esc;
  var COL = { land: '#F2D15A', build: '#2F6F86', vat: '#4A3F78', rest: '#8E7CC3' };
  var AREA = [['nat', 'ממוצע ארצי'], ['center', 'מרכז הארץ'], ['periph', 'פריפריה']];
  function css() {
    if (document.getElementById('nlpa-css')) return;
    var s = document.createElement('style'); s.id = 'nlpa-css';
    s.textContent = [
      '.nlpa-form{display:grid;gap:14px;grid-template-columns:minmax(0,1fr);margin:0 0 6px;position:relative}',
      '@media (min-width:700px){.nlpa-form{grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px 24px}}',
      '.nlpa-form>.nli__f{align-content:start}.nlpa-form .nli__seg{align-items:flex-start;align-content:flex-start}',
      '.nlpa-bar{display:flex;height:64px;border:1.5px solid var(--nli-ink);border-radius:2px;overflow:hidden;background:var(--nli-surface)}',
      'html body .nli button.nlpa-seg{all:unset;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center;gap:1px;padding:0 8px;min-width:0;cursor:pointer;overflow:hidden;border-inline-start:1.5px solid var(--nli-ink);font:600 13px/16px var(--nli-sans);color:#fff;white-space:nowrap;position:relative}',
      'html body .nli button.nlpa-seg:first-child{border-inline-start:0}',
      'html body .nli button.nlpa-seg small{font:500 12px/15px var(--nli-mono);opacity:.92}',
      'html body .nli button.nlpa-seg span,html body .nli button.nlpa-seg small{display:block;overflow:hidden;text-overflow:ellipsis}',
      'html body .nli button.nlpa-seg.is-light{color:var(--nli-ink)}',
      'html body .nli button.nlpa-seg.is-x{background:repeating-linear-gradient(135deg,#F6F8F9 0 7px,#DCE4E9 7px 8px);color:var(--nli-ink2)}',
      'html body .nli button.nlpa-seg[aria-pressed="true"]{box-shadow:inset 0 0 0 3px var(--nli-ink)}',
      'html body .nli button.nlpa-seg:focus-visible{outline:3px solid var(--nli-focus);outline-offset:-3px}',
      '.nlpa-scale{display:flex;justify-content:space-between;font:400 11px/16px var(--nli-mono);color:var(--nli-mute);margin:4px 0 0;direction:rtl}',
      '.nlpa-list{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:0;border-top:1px solid var(--nli-line)}',
      '.nlpa-list li{margin:0;border-bottom:1px solid var(--nli-line)}',
      'html body .nli button.nlpa-row{all:unset;box-sizing:border-box;width:100%;display:grid;grid-template-columns:14px minmax(0,1fr) auto 16px;gap:10px;align-items:center;padding:12px 4px;cursor:pointer;min-height:52px}',
      'html body .nli button.nlpa-row:focus-visible{outline:2px solid var(--nli-focus);outline-offset:-2px}',
      '.nlpa-row i{width:14px;height:14px;border-radius:2px;display:block;border:1px solid rgba(18,32,42,.35)}',
      '.nlpa-row b{font:600 15px/20px var(--nli-sans);color:var(--nli-ink)}.nlpa-row b small{display:block;font:400 12.5px/17px var(--nli-sans);color:var(--nli-mute)}',
      '.nlpa-row em{font:500 14px/18px var(--nli-mono);font-style:normal;color:var(--nli-ink);text-align:left;white-space:nowrap}',
      '.nlpa-row u{text-decoration:none;font:400 14px/1 var(--nli-sans);color:var(--nli-sea);transition:transform .15s}',
      'html body .nli button.nlpa-row[aria-expanded="true"] u{transform:rotate(90deg)}',
      '.nlpa-det{padding:2px 4px 16px 4px;display:grid;gap:10px}',
      '.nlpa-det>p{margin:0;font:400 14.5px/23px var(--nli-sans);color:var(--nli-ink2);max-width:74ch}',
      '.nlpa-subs{list-style:none;margin:0;padding:0;display:grid;gap:8px;grid-template-columns:minmax(0,1fr)}',
      '@media (min-width:760px){.nlpa-subs{grid-template-columns:repeat(2,minmax(0,1fr))}}',
      '.nlpa-subs li{margin:0;padding:10px 12px;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);display:grid;gap:4px;align-content:start}',
      '.nlpa-subs h4{margin:0 !important;font:600 14.5px/20px var(--nli-sans) !important;color:var(--nli-ink) !important}',
      '.nlpa-subs p{margin:0;font:400 13.5px/21px var(--nli-sans);color:var(--nli-ink2)}',
      '.nlpa-num{font:600 13.5px/19px var(--nli-mono);color:var(--nli-ink);direction:rtl;unicode-bidi:plaintext}',
      '.nlpa-none{font:500 12px/16px var(--nli-sans);color:var(--nli-mute);border:1px dashed #A9B6BF;border-radius:999px;padding:1px 8px;justify-self:start}',
      '.nlpa-claim{font:500 12px/16px var(--nli-sans);color:var(--nli-survey);border:1px solid currentColor;border-radius:999px;padding:1px 8px;justify-self:start}',
      '.nlpa-cite{font:400 12px/17px var(--nli-sans);color:var(--nli-mute)}',
      'html body .nli .nlpa-cite a{color:var(--nli-sea) !important;text-decoration:underline;text-underline-offset:2px}',
      '.nlpa-fact{margin:0;padding:10px 12px;border-inline-start:3px solid var(--nli-sea);background:var(--nli-ground);font:400 14px/22px var(--nli-sans);color:var(--nli-ink)}',
      '.nlpa-buy{display:grid;gap:0;margin:0;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface)}',
      '.nlpa-buy div{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 14px;padding:10px 12px;border-bottom:1px solid var(--nli-line)}',
      '.nlpa-buy dt{margin:0;font:500 14px/20px var(--nli-sans);color:var(--nli-ink)}.nlpa-buy dt small{display:block;font:400 12.5px/18px var(--nli-sans);color:var(--nli-mute)}',
      '.nlpa-buy dd{margin:0;font:500 14px/20px var(--nli-mono);color:var(--nli-ink);text-align:left;white-space:nowrap;direction:rtl;unicode-bidi:plaintext}',
      '.nlpa-buy .tot{background:var(--nli-ink);border-bottom:0;border-radius:0 0 var(--nli-r-s) var(--nli-r-s)}.nlpa-buy .tot dt,.nlpa-buy .tot dd{color:#fff}.nlpa-buy .tot dt small{color:#C9D6DD}',
      '.nlpa-go{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 0}',
      'html body .nli a.nlpa-btn{display:inline-flex;align-items:center;min-height:46px;padding:10px 18px;border-radius:var(--nli-r-s);background:var(--nli-sea);color:#fff !important;font:600 15px/20px var(--nli-sans);text-decoration:none !important}',
      'html body .nli a.nlpa-btn.is-ghost{background:var(--nli-surface);color:var(--nli-sea) !important;border:1px solid var(--nli-sea)}',
      'html body .nli a.nlpa-btn:hover{background:var(--nli-sea-deep);color:#fff !important}',
      '.nlpa-gap{margin:14px 0 0;font:400 13px/20px var(--nli-sans);color:var(--nli-ink2);padding:10px 12px;border:1px dashed #A9B6BF;border-radius:var(--nli-r-s)}'
    ].join('');
    document.head.appendChild(s);
  }
  function inputIndex(data) { for (var k in data) { var d = data[k]; if (d && d.id === 200010 && d.months) return d; } return null; }
  function fmtDate(s) { var p = String(s).split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : p.length === 2 ? P.monLabel(s) : s; }

  /* the developer-side bar for an area: [{id, w, label, sub, color, x}] (w: share of the price; x: no official split) */
  function devBar(A, area, vat) {
    var g = {}; A.dev.forEach(function (x) { g[x.id] = x; });
    var land = g.land.share[area] || g.land.share.nat, out = [{ id: 'land', w: land.v, label: g.land.he, sub: land.say, color: COL.land, light: true }];
    var vw = vat / (1 + vat);
    if (area === 'nat') {
      out.push({ id: 'build', w: g.build.share.nat.v, label: g.build.he, sub: g.build.share.nat.say, color: COL.build });
      var rest = g.rest.share.nat.v;
      out.push({ id: 'rest', w: vw, label: 'מע״מ', sub: (100 * vw).toFixed(1) + '%', color: COL.vat, vat: true });
      out.push({ id: 'rest', w: Math.max(0, rest - vw), label: 'רווח, מימון, שיווק', sub: 'בלי חלוקה רשמית', color: COL.rest });
    } else {
      out.push({ id: 'rest', w: vw, label: 'מע״מ', sub: (100 * vw).toFixed(1) + '%', color: COL.vat, vat: true });
      out.push({ id: 'build', w: Math.max(0, 1 - land.v - vw), label: 'הבנייה, הרווח ושאר הרכיבים', sub: 'אין חלוקה רשמית לאזור', x: true });
    }
    return out;
  }
  /* the buyer's side: [{label, lo, hi, note}] */
  function buyer(A, PT, v) {
    var B = A.buyer, vat = B.vat, tx = P.ptax(v.price, PT.tracks[v.track] || PT.tracks.single), loan = v.price * Math.max(0, Math.min(v.ltv, 100)) / 100;
    var mf = loan > 0 ? Math.min(loan * B.mortgage_fee.rate, B.mortgage_fee.max) : 0;
    var L = [{ k: 'tax', label: 'מס רכישה', lo: tx.tax, hi: tx.tax, note: tx.parts.length ? tx.parts.map(function (p) { return (100 * p.rate).toFixed(p.rate * 1000 % 10 ? 1 : 0) + '% על ' + U.ils(p.to - p.from); }).join(' · ') : '', exact: true },
      { k: 'law', label: 'עורך דין', lo: v.price * B.lawyer.from / 100 * (1 + vat), hi: v.price * B.lawyer.to / 100 * (1 + vat), note: B.lawyer.from + '% עד ' + B.lawyer.to + '% מהמחיר, ועוד מע״מ' }];
    if (v.broker) L.push({ k: 'brk', label: 'תיווך', lo: v.price * B.broker.customary / 100 * (1 + vat), hi: v.price * B.broker.customary / 100 * (1 + vat), note: 'מקובל ' + B.broker.customary + '%, ועוד מע״מ' });
    L.push({ k: 'app', label: 'שמאי לבנק', lo: B.appraiser[0], hi: B.appraiser[1], note: 'טווח מקובל' });
    L.push({ k: 'insp', label: 'בדק בית', lo: B.inspection[0], hi: B.inspection[1], note: 'טווח מקובל' });
    if (loan > 0) L.push({ k: 'mf', label: 'פתיחת תיק משכנתא', lo: mf, hi: mf, note: (100 * B.mortgage_fee.rate).toFixed(2) + '% מההלוואה, עד ' + U.ils(B.mortgage_fee.max), exact: true });
    var lo = 0, hi = 0; L.forEach(function (x) { lo += x.lo; hi += x.hi; });
    return { lines: L, lo: lo, hi: hi, tax: tx, loan: loan };
  }
  window.NLPH.anatomy = { devBar: devBar, buyer: buyer };

  NI.register('panatomy', {
    custom: function (root, data) {
      var A = data.anatomy, PT = data.ptax, CO = data.cost, H = data.phub, IN = inputIndex(data); U.css(); css();
      if (!root.closest('.nli')) root.classList.add('nli');
      root.setAttribute('dir', 'rtl');
      var set = {}; try { set = JSON.parse(root.getAttribute('data-nli-set') || '{}'); } catch (e) {}
      root.innerHTML = '';
      var S = A.src, vat = CO.vat;
      var med = function (n) { var arr = n ? (H.city.filter(function (c) { return c.n === n; })[0] || {}).r4 : H.il.r4, i = P.lastIdx(arr || []); return i < 0 ? null : { v: arr[i], q: H.q[i] }; };
      var mIL = med(), mTA = med('תל אביב יפו'), mBS = med('באר שבע');
      var st = { price: set.price > 100000 ? set.price : Math.round(mIL.v), area: /^(nat|center|periph)$/.test(set.region) ? set.region : 'nat', track: set.track === 'extra' ? 'extra' : 'single', broker: false, ltv: 75, open: 'land' };

      var panel = U.el('div', 'nli__panel nlph'); root.appendChild(panel);
      panel.appendChild(U.el('p', 'nli__kicker', 'פירוק · מחיר דירה חדשה'));
      panel.appendChild(U.el('h2', 'nli__title', 'מה יש בתוך המחיר של דירה חדשה'));
      panel.appendChild(U.el('p', 'nli__lede', esc('קרקע, בנייה, מסים, רווח היזם, ומה שהקונה משלם מעל המחיר. כל חלק עם המקור שלו והתאריך, ומה שאין לו מקור ציבורי מופיע בשם בלבד, בלי מספר.')));
      var preset = U.el('div', 'nlph-tabs is-sea'); preset.setAttribute('role', 'group'); preset.setAttribute('aria-label', 'מקרים מוכנים');
      preset.appendChild(U.el('span', 'lab', 'מקרים מוכנים:'));
      var PR = [{ k: 'il', l: 'החציון הארצי, 4 חדרים', set: { price: Math.round(mIL.v), area: 'nat' } }];
      if (mTA) PR.push({ k: 'ta', l: 'תל אביב, 4 חדרים', set: { price: Math.round(mTA.v), area: 'center' } });
      if (mBS) PR.push({ k: 'bs', l: 'באר שבע, 4 חדרים', set: { price: Math.round(mBS.v), area: 'periph' } });
      PR.forEach(function (p) { var b = U.el('button', '', esc(p.l)); b.type = 'button'; b.setAttribute('data-k', p.k); b.addEventListener('click', function () { Object.keys(p.set).forEach(function (k) { st[k] = p.set[k]; }); form(); run(); }); preset.appendChild(b); });
      panel.appendChild(preset);
      var fbox = U.el('form', 'nlpa-form'); fbox.style.marginTop = '14px'; fbox.addEventListener('submit', function (e) { e.preventDefault(); }); panel.appendChild(fbox);
      var sec1 = U.el('section', 'nlph-sec'); panel.appendChild(sec1);
      var sec2 = U.el('section', 'nlph-sec'); panel.appendChild(sec2);
      var gap = U.el('p', 'nlpa-gap'); panel.appendChild(gap);
      var src = U.el('p', 'nli__src'); panel.appendChild(src);
      var shareText = '';
      panel.appendChild(U.share(function () { return shareText; }));

      function form() {
        fbox.innerHTML = '';
        var w = U.el('div', 'nli__f'), id = 'nlpa-p-' + Math.random().toString(36).slice(2, 7), lab = U.el('label', '', 'מחיר הדירה, כולל מע״מ'); lab.htmlFor = id; w.appendChild(lab);
        var ib = U.el('div', 'nli__in'), inp = document.createElement('input'); inp.id = id; inp.type = 'text'; inp.inputMode = 'numeric'; inp.value = U.num(st.price);
        inp.addEventListener('input', function () { var n = parseFloat(inp.value.replace(/[^\d.]/g, '')); if (isFinite(n) && n >= 100000) { st.price = n; marks(); run(); } });
        inp.addEventListener('blur', function () { inp.value = U.num(st.price); });
        ib.appendChild(inp); ib.appendChild(U.el('span', 'nli__unit', '₪')); w.appendChild(ib);
        w.appendChild(U.el('span', 'nli__help', esc('בפתיחה: החציון הארצי לדירת 4 חדרים, ' + P.qLabel(mIL.q) + ' (כל העסקאות, רשות המסים).')));
        fbox.appendChild(w);
        fbox.appendChild(U.seg('איפה הדירה', AREA.map(function (a) { return { value: a[0], label: a[1] }; }), st.area, function (v) { st.area = v; marks(); run(); }));
        fbox.appendChild(U.seg('מי קונה', [{ value: 'single', label: 'דירה יחידה' }, { value: 'extra', label: 'דירה נוספת' }], st.track, function (v) { st.track = v; run(); }));
        fbox.appendChild(U.seg('דרך מתווך?', [{ value: false, label: 'בלי מתווך' }, { value: true, label: 'עם מתווך' }], st.broker, function (v) { st.broker = v; run(); }));
        marks();
      }
      function marks() { [].forEach.call(preset.querySelectorAll('button'), function (b) { var p = PR.filter(function (z) { return z.k === b.getAttribute('data-k'); })[0]; b.setAttribute('aria-pressed', String(!!p && p.set.price === st.price && p.set.area === st.area)); }); }

      function cite(key) { var s = S[key]; if (!s) return ''; return '<span class="nlpa-cite">מקור: ' + (s.url ? '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.he) + '</a>' : esc(s.he)) + (s.date && /^\d{4}/.test(s.date) ? ', ' + esc(fmtDate(s.date)) : '') + '</span>'; }
      function subHtml(g, x) {
        var num = '';
        if (x.vat) num = '<span class="nlpa-num">' + esc('18% על המחיר לפני מע״מ = ' + (100 * vat / (1 + vat)).toFixed(1) + '% מהמחיר: ' + U.ils(P.vatIn(st.price, vat))) + '</span>';
        else if (x.rule) num = '<span class="nlpa-num">' + esc(x.rule) + '</span>';
        else if (x.claim) num = '<span class="nlpa-num">' + esc(x.claim.lo + '% עד ' + x.claim.hi + '% ממחזור המכירות') + '</span><span class="nlpa-claim">טענה של חברת שיווק, לא נתון רשמי</span>';
        else if (!x.facts) num = '<span class="nlpa-none">אין מספר ציבורי</span>';
        var facts = '';
        if (x.facts) {
          var f = A.facts;
          facts = '<span class="nlpa-num">' + esc('ריבית הפריים: ' + f.prime.v.toFixed(2) + '% מ־' + fmtDate(f.prime.from)) + '</span>' + cite(f.prime.src) +
            '<p>' + esc('במבצעי מימון: ב־' + f.runi.year + ' היו כ־' + Math.round(100 * f.runi.deals) + '% מהעסקאות בשוק החופשי, וההטבה נאמדה בממוצע בכ־' + Math.round(100 * f.runi.disc) + '% ממחיר הדירה, כהנחה במחיר האפקטיבי.') + '</p>' + cite(f.runi.src) + '<span class="nlpa-none">חלק המימון במחיר: אין מספר ציבורי</span>';
        }
        return '<li><h4>' + esc(x.he) + '</h4>' + num + '<p>' + esc(x.txt) + '</p>' + facts + (x.src && !x.facts ? cite(x.src) : '') + '</li>';
      }
      function trend() {
        if (!IN) return '';
        var ks = Object.keys(IN.months).sort(), last = ks[ks.length - 1], v = IN.months[last], y = IN.months[P.addM(last, -12)], b = IN.months['2021-01'];
        return '<p class="nlpa-fact">' + esc('מדד תשומות הבנייה למגורים של הלמ״ס, ' + P.monLabel(last) + ': ' + U.pctTxt(P.chg(v, y)) + ' בשנה, ' + U.pctTxt(P.chg(v, b)) + ' מינואר 2021. בדירה מקבלן חלק מהתשלומים צמוד למדד הזה.') + ' <a class="nlph-a" href="/new-projects/construction-input-index/">מחשבון ההצמדה למדד תשומות הבנייה</a></p>';
      }
      function run() {
        var bar = devBar(A, st.area, vat), g = {}; A.dev.forEach(function (x) { g[x.id] = x; });
        var area = AREA.filter(function (a) { return a[0] === st.area; })[0][1], land = g.land.share[st.area] || g.land.share.nat;
        var head = '<h3 class="nlph-h">מה היזם מכניס למחיר</h3><p class="nlph-sub">' + esc(st.area === 'nat'
          ? 'לפי בנק ישראל, בממוצע הארצי של 2009 עד 2010 הקרקע הייתה כשליש ממחיר הדירה, הבנייה כשליש, והיתר הלך לרווח היזם ולמסים. המע״מ מחושב כאן לפי השיעור של היום. לחצו על חלק כדי לפרק אותו.'
          : 'לפי בנק ישראל, בשיא של 2011 מחיר הקרקע ליחידת דיור היה ' + land.say + ' ממחיר דירה טיפוסית של 3.5 עד 4 חדרים ב' + (st.area === 'center' ? 'מרכז הארץ' : 'פריפריה') + '. לשאר הרכיבים באזור הזה אין חלוקה רשמית, ולכן הם מופיעים יחד, בלי מספר.') + '</p>';
        var segs = bar.map(function (b, i) {
          var light = b.light ? ' is-light' : '', on = st.open === b.id && !b.x;
          return '<button type="button" class="nlpa-seg' + light + (b.x ? ' is-x' : '') + '" style="flex:' + b.w.toFixed(4) + ' 1 0;' + (b.x ? '' : 'background:' + b.color) + '" data-id="' + b.id + '" aria-pressed="' + on + '" aria-label="' + esc(b.label + ', ' + b.sub) + '">' +
            (b.w > 0.09 ? '<span>' + esc(b.label) + '</span><small>' + esc(b.sub) + '</small>' : '') + '</button>';
        }).join('');
        var list = A.dev.map(function (x) {
          var sh = x.share[st.area], shown = sh ? sh.say : 'אין חלוקה רשמית לאזור', when = sh ? sh.when : '', open = st.open === x.id;
          return '<li><button type="button" class="nlpa-row" data-id="' + x.id + '" aria-expanded="' + open + '" aria-controls="nlpa-d-' + x.id + '"><i style="background:' + COL[x.id] + '"></i><b>' + esc(x.he) + '<small>' + esc(when ? 'בנק ישראל, ' + when : 'לפי בנק ישראל אין פירוק לאזור הזה') + '</small></b><em>' + esc(shown) + '</em><u aria-hidden="true">‹</u></button>' +
            '<div class="nlpa-det" id="nlpa-d-' + x.id + '"' + (open ? '' : ' hidden') + '><p>' + esc(x.txt) + '</p>' + (sh ? cite(sh.src) : '') + (x.trend ? trend() : '') + '<ul class="nlpa-subs">' + x.sub.map(function (y) { return subHtml(x, y); }).join('') + '</ul></div></li>';
        }).join('');
        sec1.innerHTML = head + '<div class="nlpa-bar" role="group" aria-label="' + esc('החלקים של מחיר דירה חדשה, ' + area) + '">' + segs + '</div><div class="nlpa-scale" aria-hidden="true"><span>0%</span><span>50%</span><span>100% מהמחיר</span></div><ul class="nlpa-list">' + list + '</ul>';
        [].forEach.call(sec1.querySelectorAll('[data-id]'), function (b) { if (b.classList.contains('is-x')) return; b.addEventListener('click', function () { var id = b.getAttribute('data-id'); st.open = st.open === id && b.classList.contains('nlpa-row') ? '' : id; run(); var r = sec1.querySelector('.nlpa-row[data-id="' + id + '"]'); if (r && b.classList.contains('nlpa-seg')) { r.focus({ preventScroll: true }); if (r.getBoundingClientRect().top > innerHeight - 80) r.scrollIntoView({ block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); } }); });

        var Bq = buyer(A, PT, st), tr = st.track === 'extra' ? 'דירה נוספת' : 'דירה יחידה';
        var rng = function (x) { return Math.round(x.lo) === Math.round(x.hi) ? U.ils(x.lo) : U.num(x.lo) + ' עד ' + U.ils(x.hi); };
        sec2.innerHTML = '<h3 class="nlph-h">מה הקונה משלם מעל המחיר</h3><p class="nlph-sub">' + esc('על דירה של ' + U.ils(st.price) + ', ' + tr + (st.broker ? ', דרך מתווך' : '') + ', עם משכנתא של ' + st.ltv + '% מהמחיר. מס הרכישה מדויק לפי המדרגות של רשות המסים; השאר בטווחים שפורסמו.') + '</p>' +
          '<dl class="nlpa-buy">' + Bq.lines.map(function (x) { return '<div><dt>' + esc(x.label) + (x.note ? '<small>' + esc(x.note) + '</small>' : '') + '</dt><dd>' + esc(x.exact ? U.ils(x.lo) : rng(x)) + '</dd></div>'; }).join('') +
          '<div class="tot"><dt>' + esc('סך הכול מעל המחיר') + '<small>' + esc('כ־' + (100 * Bq.lo / st.price).toFixed(1) + '% עד ' + (100 * Bq.hi / st.price).toFixed(1) + '% מהמחיר') + '</small></dt><dd>' + esc(rng(Bq)) + '</dd></div></dl>' +
          '<p class="nlph-fine">' + cite('ptax') + ' · ' + cite('fees') + '</p>' +
          (IN ? '<p class="nlpa-fact" style="margin-top:12px">' + esc('ובדירה מקבלן: התשלומים לקבלן צמודים בחלקם למדד תשומות הבנייה עד המסירה, לפי חוק המכר. ') + '<a class="nlph-a" href="/new-projects/construction-input-index/">' + esc('כמה ההצמדה תוסיף לכם') + '</a></p>' : '') +
          '<div class="nlpa-go"><a class="nlpa-btn" href="/purchase-tax-calculator/">מחשבון מס רכישה</a><a class="nlpa-btn is-ghost" href="/apartment-purchase-cost-calculator/">כל עלויות הקנייה במחשבון אחד</a></div>';
        gap.innerHTML = '<b>' + esc('בלי מספר, בכוונה:') + '</b> ' + esc('לא מצאנו מקור ציבורי מתוארך ל' + A.none.join(', ') + '. כשיפורסם מקור כזה, הוא ייכנס כאן עם התאריך שלו.');
        src.innerHTML = U.srcs(['boi13', 'hashbacha', 'runi26', 'vat', 'ptax', 'fees', 'prime', 'input', 'mkt'].map(function (k) { var s = S[k]; return { label: s.he + (s.date && /^\d{4}/.test(s.date) ? ' (' + fmtDate(s.date) + ')' : ''), url: s.url }; }));
        shareText = 'מה יש בתוך המחיר של דירה חדשה (' + area + '): ' + bar.filter(function (b) { return !b.x; }).map(function (b) { return b.label + ' ' + b.sub; }).join(', ') + '. מעל המחיר של ' + U.ils(st.price) + ' (' + tr + '): ' + rng(Bq) + ', מתוכם מס רכישה ' + U.ils(Bq.tax.tax) + '.';
      }
      form(); run();
    }
  });
})();
