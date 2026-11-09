/* NadLan Instruments · buying3 v1 (HAD-686, Ben 8.11.2026: the best buying guide in Israel, every unit of the competitors' guides
   covered by count). Five more tools of the /buying-apartment/ guide, one file ('file' => 'buying3', after prices-common.js,
   buying.js and buying2.js, whose helpers it reuses through window.NLBH), plus the behaviour of the guide's reading layer.
   - bpay   the payment schedule of a second-hand deal: five payments in order, each with when, how much, to whom and what
            protects the buyer at that moment; the capital-gains advance rule is the bwho row (orechdin.json, the same source)
   - bsign  the signing day: what to bring, what is signed, what you leave with (buying.json sign); ticks kept in this browser
   - bkeys  the handover protocol: meter readings, keys and remotes, defects, what stays, the transfers; saved, printable
   - breg   from the signing to an extract in your name: ten steps, who does each, the proof, a status; saved
   - bmemo  six yes or no questions about a memorandum; a plain risk level and the next step; never saved (privacy)
   - the reading layer: nav#nlbg-map (chapters read, the chapter in view) and dl#nlbg-gloss (a filter with a live count)
   One signing date is shared by bdates, bpay and breg (nlbh-plan-v1 .sign, event nlbh:sign). Pure logic in window.NLBH3 and
   window.NLBG (tools/instruments/test_buying_hub.js). Design: BuyingGuide v109 (instruments palette and faces). */
(function () {
  'use strict';
  var W = typeof window !== 'undefined' ? window : this;
  var DOC = typeof document !== 'undefined' && document && document.querySelector && document.addEventListener ? document : null;

  /* ------------------------------------------------ the reading layer (needs no tool) ------------------------------------------------ */
  var G = W.NLBG = {};
  /* a search key: lower case, no niqqud, no quotes or geresh, a maqaf or hyphen is a space */
  G.norm = function (s) { return String(s || '').toLowerCase().replace(/[־‐‑\-_/]/g, ' ').replace(/[֑-ֽֿ-ׇ]/g, '').replace(/["'`׳״‘’“”]/g, '').replace(/\s+/g, ' ').trim(); };
  /* the share of a chapter above a reading line (0..1) */
  G.passed = function (top, height, line) { return height > 0 ? Math.max(0, Math.min(1, (line - top) / height)) : 0; };
  G.count = function (n) { return n === 1 ? 'מונח אחד' : n + ' מונחים'; };
  G.READ = 0.6;  // a chapter is read once 60% of it has passed the middle of the screen, while the reader stays on it

  function mapInit(map) {
    var KEY = 'nlbg-read-v1', read = {}, items = [];
    try { (JSON.parse(W.localStorage.getItem(KEY) || '[]') || []).forEach(function (id) { read[id] = 1; }); } catch (e) {}
    [].forEach.call(map.querySelectorAll('a[href^="#nlbg-c"]'), function (a) {
      var id = decodeURIComponent(a.getAttribute('href').slice(1)), sec = DOC.getElementById(id);
      if (!sec || !sec.classList.contains('nlbg-ch')) return;
      var dot = a.querySelector('i'); if (!dot) { dot = DOC.createElement('i'); a.appendChild(dot); } dot.setAttribute('aria-hidden', 'true');
      var vh = DOC.createElement('span'); vh.className = 'nlbg-vh'; a.appendChild(vh);
      items.push({ a: a, id: id, sec: sec, vh: vh });
    });
    if (!items.length) return;
    var prog = DOC.createElement('p'), ptx = DOC.createElement('span'), rb = DOC.createElement('button');
    prog.className = 'nlbg-map__prog'; prog.setAttribute('aria-live', 'polite'); rb.type = 'button'; rb.textContent = 'ניקוי הסימון';
    prog.appendChild(ptx); prog.appendChild(rb); map.appendChild(prog);
    function save() { try { W.localStorage.setItem(KEY, JSON.stringify(Object.keys(read))); } catch (e) {} }
    function paint() {
      var n = 0;
      items.forEach(function (it) { var r = !!read[it.id]; if (r) n++; it.a.classList.toggle('is-read', r); it.sec.classList.toggle('is-read', r); it.vh.textContent = r ? ' (נקרא)' : ''; });
      prog.hidden = !n; ptx.textContent = 'קראתם ' + n + ' מתוך ' + items.length + ' שלבים. הסימון נשמר רק בדפדפן הזה. ';
    }
    rb.addEventListener('click', function () { read = {}; save(); paint(); });
    var now = null;
    function current() {
      var line = W.innerHeight * 0.3, hit = null;
      items.forEach(function (it) { var r = it.sec.getBoundingClientRect(); if (r.top <= line && r.bottom > line) hit = it; });
      if (hit === now) return;
      if (now) { now.a.classList.remove('is-now'); now.a.removeAttribute('aria-current'); }
      now = hit; if (now) { now.a.classList.add('is-now'); now.a.setAttribute('aria-current', 'location'); }
    }
    function seen() {
      var Hh = W.innerHeight, ch = false;
      items.forEach(function (it) { if (read[it.id]) return; var r = it.sec.getBoundingClientRect(); if (r.bottom <= 0 || r.top >= Hh || r.height <= 0) return; if (G.passed(r.top, r.height, Hh * 0.5) >= G.READ) { read[it.id] = 1; ch = true; } });
      if (ch) { save(); paint(); }
    }
    var raf = 0, idle = 0;
    function onScroll() { if (!raf) { var fn = function () { raf = 0; current(); }; raf = W.requestAnimationFrame ? W.requestAnimationFrame(fn) : setTimeout(fn, 16); } clearTimeout(idle); idle = setTimeout(seen, 400); }  // read only where the reader stops, not on a jump through
    W.addEventListener('scroll', onScroll, { passive: true }); W.addEventListener('resize', onScroll);
    paint(); current(); idle = setTimeout(seen, 600);
  }

  function glossInit(dl) {
    var pairs = [], cur = null;
    [].forEach.call(dl.children, function (el) {
      if (el.tagName === 'DIV') { if (el.querySelector('dt')) pairs.push({ els: [el] }); cur = null; }
      else if (el.tagName === 'DT') { cur = { els: [el] }; pairs.push(cur); }
      else if (el.tagName === 'DD' && cur) cur.els.push(el);
    });
    if (!pairs.length) return;
    pairs.forEach(function (p) { p.key = G.norm(p.els.map(function (e) { return e.textContent; }).join(' ')); });
    if (!dl.id) dl.id = 'nlbg-gloss';
    var id = 'nlbg-q-' + Math.random().toString(36).slice(2, 7), box = DOC.createElement('div');
    box.className = 'nlbg-gloss-find';
    box.innerHTML = '<label for="' + id + '">חיפוש במילון המונחים</label><input id="' + id + '" type="search" autocomplete="off" enterkeyhint="search" placeholder="למשל: נסח, משכון, היטל" aria-controls="' + dl.id + '" aria-describedby="' + id + '-n"><p id="' + id + '-n" class="nlbg-gloss-find__n" aria-live="polite"></p>';
    dl.parentNode.insertBefore(box, dl);
    var q = box.querySelector('input'), n = box.querySelector('p');
    function run() {
      var v = G.norm(q.value), c = 0;
      pairs.forEach(function (p) { var hit = !v || p.key.indexOf(v) >= 0; if (hit) c++; p.els.forEach(function (e) { e.hidden = !hit; }); });
      n.textContent = c ? G.count(c) + (v ? ' מתוך ' + pairs.length : '') : 'לא נמצא מונח כזה. נסו מילה אחרת.';
    }
    q.addEventListener('input', run); run();
  }

  function rlBoot() {
    var m = DOC.getElementById('nlbg-map'), g = DOC.getElementById('nlbg-gloss');
    if (m && !m.__nlbg) { m.__nlbg = 1; mapInit(m); }
    if (g && !g.__nlbg && g.tagName === 'DL') { g.__nlbg = 1; glossInit(g); }
  }
  if (DOC) { if (DOC.readyState === 'loading') DOC.addEventListener('DOMContentLoaded', rlBoot); else rlBoot(); }

  /* ------------------------------------------------ the tools: pure logic ------------------------------------------------ */
  var B = W.NLBH;
  if (!B) return;
  var X = W.NLBH3 = {}, n0 = B.n0, pc = B.pc, date = B.date;
  function utc(iso) { var p = String(iso).split('-'); return Date.UTC(+p[0], +p[1] - 1, +p[2]); }
  function isoOf(t) { var d = new Date(t); return d.getUTCFullYear() + '-' + ('0' + (d.getUTCMonth() + 1)).slice(-2) + '-' + ('0' + d.getUTCDate()).slice(-2); }
  X.addDays = function (s, n) { return isoOf(utc(s) + n * 864e5); };  // the rule bdates uses (NLBH2.addDays)
  X.days = function (a, b) { return Math.round((utc(b) - utc(a)) / 864e5); };
  X.advRate = function (O, kind) { return kind === 'none' ? 0 : kind === 'old' ? O.rate_old : O.rate; };

  /* bpay. o: P price, L the buyer's mortgage, S the seller's mortgage balance, pct the first payment in % of the price,
     adv 'std' | 'old' | 'none', sign and hand (ISO, optional), O orechdin.cgt_advance, PT ptax.pay, ltv nrm.ltv_by_status.
     The five payments are by destination; the buyer's own money (P - L) pays first, the mortgage pays what is left of the
     seller's balance and of the advance, and the rest of it goes to the seller. They always add up to the price. */
  X.pay = function (o) {
    var P = Math.round(Math.max(0, +o.P || 0)), L = Math.round(Math.max(0, +o.L || 0)), S = Math.round(Math.max(0, +o.S || 0)), pct = +o.pct || 0;
    var rate = X.advRate(o.O, o.adv), A = Math.round(P * rate), f = Math.round(P * pct / 100), own = P - L, errs = [], warns = [];
    if (!(P > 0)) errs.push({ k: 'price', f: 'P', t: 'הקלידו את מחיר הדירה.' });
    else {
      var okL = L <= P, okF = pct >= 0 && pct <= 100;
      if (!okL) errs.push({ k: 'loan', f: 'L', t: 'המשכנתא (' + n0(L) + ' ₪) גדולה ממחיר הדירה (' + n0(P) + ' ₪).' });
      if (!okF) errs.push({ k: 'pct', f: 'pct', t: 'התשלום הראשון הוא אחוז מהמחיר, בין 0 ל־100.' });
      else if (okL && f > own) errs.push({ k: 'first', f: 'pct', t: 'התשלום הראשון (' + n0(f) + ' ₪) גדול מהכסף שלכם בעסקה: המחיר פחות המשכנתא הוא ' + n0(own) + ' ₪. ביום החתימה המשכנתא עוד לא שוחררה, ולכן את התשלום הראשון משלמים מכספכם.' });
      if (okL && okF && f <= own) {
        if (f + A > P) errs.push({ k: 'over', f: 'pct', t: 'התשלום הראשון והמקדמה יחד (' + n0(f + A) + ' ₪) גדולים מהמחיר. הקטינו את התשלום הראשון.' });
        else if (S > P - f - A) errs.push({ k: 'seller', f: 'S', t: 'יתרת המשכנתא של המוכר (' + n0(S) + ' ₪) גדולה ממה שנשאר מהמחיר אחרי התשלום הראשון והמקדמה (' + n0(P - f - A) + ' ₪). המחיר לא מספיק כדי לסלק את המשכנתא שלו: לפני שחותמים, עורך הדין צריך לבדוק מאיפה המוכר משלים את ההפרש.' });
      }
    }
    var ISOre = /^\d{4}-\d{2}-\d{2}$/, sign = ISOre.test(o.sign || '') ? o.sign : '', hand = ISOre.test(o.hand || '') ? o.hand : '';
    if (sign && hand && hand < sign) errs.push({ k: 'dates', f: 'hand', t: 'תאריך המסירה מוקדם מתאריך החתימה.' });
    var res = { ok: !errs.length, errs: errs, warns: warns, P: P, L: L, S: S, A: A, rate: rate, pct: pct, f: f, own: own, rows: null, cross: -1, dates: null };
    if (sign && o.PT) res.dates = { sign: sign, declare: X.addDays(sign, o.PT.declare_days), pay: X.addDays(sign, o.PT.pay_days), hand: hand && hand >= sign ? hand : '', handDays: hand && hand >= sign ? X.days(sign, hand) : null };
    if (!res.ok) return res;
    var o1 = own - f, sOwn = Math.min(S, o1), sLoan = S - sOwn, o2 = o1 - sOwn, aOwn = Math.min(A, o2), aLoan = A - aOwn, last = o2 - aOwn, p3 = L - sLoan - aLoan;
    res.rows = [{ id: 'first', amt: f, own: f, loan: 0 }, { id: 'seller', amt: S, own: sOwn, loan: sLoan }, { id: 'loan', amt: p3, own: 0, loan: p3 },
      { id: 'adv', amt: A, own: aOwn, loan: aLoan }, { id: 'last', amt: last, own: last, loan: 0 }];
    /* the payment that takes the paid share past the advance threshold, in time order 1, 2, 3, 5 (the advance is held back from it) */
    var lim = o.O.after_paid * P, cum = 0, order = [0, 1, 2, 4];
    for (var i = 0; i < order.length; i++) { cum += res.rows[order[i]].amt; if (cum > lim) { res.cross = order[i]; break; } }
    var lt = o.ltv;
    if (lt && L > lt.cit_first * P + 0.5) warns.push({ k: 'ltv', t: 'המשכנתא היא ' + pc(L / P, 1) + '% מהמחיר. בנק ישראל מתיר עד ' + pc(lt.cit_first) + '% בדירה יחידה, ' + pc(lt.cit_sell) + '% בדירה חלופית ו־' + pc(lt.cit_own) + '% בדירה להשקעה (הוראה 329). בדקו את הסכום שהבנק אישר.' });
    if (sLoan > 0) warns.push({ k: 'split', t: 'יתרת המשכנתא של המוכר גדולה מהכסף שנשאר לכם אחרי התשלום הראשון, ולכן ' + n0(sLoan) + ' ₪ מכספי המשכנתא שלכם עוברים ישירות לבנק של המוכר.' });
    if (aLoan > 0) warns.push({ k: 'advloan', t: 'הכסף שלכם נגמר לפני המקדמה, ולכן ' + n0(aLoan) + ' ₪ מהמקדמה יוצאים מכספי המשכנתא.' });
    if (A > 0 && res.cross === 0) warns.push({ k: 'cross1', t: 'התשלום הראשון כבר עובר ' + pc(o.O.after_paid) + '% מהמחיר, ולכן המקדמה מעוכבת כבר ממנו.' });
    if (last === 0) warns.push({ k: 'nolast', t: '' });  // the text is the data's "none" line of the last payment
    return res;
  };
  /* bmemo: a: { price, flat, dates, paid, subj, both } each true / false; essentials = a price and the flat identified */
  X.MEMO = ['price', 'flat', 'dates', 'paid', 'subj', 'both'];
  X.memo = function (a) {
    a = a || {};
    var left = X.MEMO.filter(function (k) { return a[k] !== true && a[k] !== false; }).length;
    if (left) return { level: null, left: left };
    var e = a.price && a.flat;
    return { level: e && ((a.both && !a.subj) || a.paid) ? 'high' : (e || a.both || a.paid) ? 'mid' : 'low', left: 0, e: e };
  };
  /* breg: the due date of a step from the signing date (only the two dated by the Tax Authority guide) */
  X.regDue = function (it, sign, PT) { return sign && it.due ? X.addDays(sign, it.due === 'declare' ? PT.declare_days : PT.pay_days) : null; };
  X.regCount = function (items, st) { var c = [0, 0, 0]; items.forEach(function (it) { c[(st && st[it.id]) || 0]++; }); return c; };
  X.ticks = function (lists, t) { var n = 0, all = 0; Object.keys(lists).forEach(function (g) { lists[g].forEach(function (x, i) { all++; if (t && t[g] && t[g][i]) n++; }); }); return { n: n, all: all }; };

  if (!W.NadLanInstruments || !DOC || !DOC.createElement || !W.NLPH || !W.NLPH.ui || !B.ui) return;
  /* ------------------------------------------------ the surfaces ------------------------------------------------ */
  var NI = W.NadLanInstruments, U = W.NLPH.ui, esc = U.esc, H = B.ui, ISO = /^\d{4}-\d{2}-\d{2}$/, MEMO = {};  // MEMO: bmemo's answers, in memory only
  function css() {
    if (DOC.getElementById('nlbh3-css')) return;
    var s = DOC.createElement('style'); s.id = 'nlbh3-css';
    s.textContent = [
      '.nlbh3{--b3-grn:#3B7D4A;--b3-grn-ink:#2E6B43;--b3-grn-tint:#EEF5EF;--b3-yel:#F2D15A;--b3-label:"IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace}',  /* labels: Plex Mono digits, Plex Hebrew letters */
      'html body .nli .nlbh3 .nlph-tabs button,html body .nli .nlbh3 .nlbh-acts button,html body .nli .nlbh3 .nli__share button,html body .nli .nlbh3 .nli__share a{min-height:44px}',
      'html body .nli .nlbh3 .nlbh-acts button{padding:10px 16px}',
      '@media (max-width:600px){html body .nli .nlbh3 .nlph-tabs button,html body .nli .nlbh3 .nlbh-acts button,html body .nli .nlbh3 .nli__share button,html body .nli .nlbh3 .nli__share a{min-height:48px}}',
      'html body .nli .nlbh3 .nli__help{display:block;font:400 12.5px/18px var(--nli-sans);color:var(--nli-mute);margin:0}',
      'html body .nli .nlbh3 .nli__in input[type=date]{font:500 16px/1.2 var(--nli-mono);direction:ltr;text-align:right;min-height:46px}',
      'html body .nli .nlbh3 .nli__f.is-bad .nli__in{border-color:var(--nli-survey);box-shadow:0 0 0 1px var(--nli-survey)}',
      'html body .nli .nlbh3 .nlbh3-sh{font:600 14px/20px var(--b3-label) !important;color:var(--nli-sea-deep) !important;letter-spacing:.03em;margin:18px 0 6px !important;padding:0 !important;border:0 !important;text-transform:none;position:relative}',
      'html body .nli .nlbh3 .nlph-tabs{margin:14px 0 0;position:relative}',
      /* notes: a square marker, hairlines top and bottom, no side bar */
      '.nlbh3-note{display:grid;grid-template-columns:12px minmax(0,1fr);gap:10px;margin:12px 0 0;padding:10px 0;border-top:1px solid var(--nli-line);border-bottom:1px solid var(--nli-line);font:400 14px/22px var(--nli-sans);color:var(--nli-ink);position:relative}',
      '.nlbh3-note::before{content:"";width:12px;height:12px;margin-top:5px;border-radius:1px;background:var(--nli-sea)}.nlbh3-note.is-stop::before{background:var(--nli-survey)}.nlbh3-note.is-fig::before{background:var(--b3-yel);outline:1px solid #C9A92B}',
      '.nlbh3-note>div{min-width:0}.nlbh3-note b{display:block;font:600 13px/20px var(--b3-label);letter-spacing:.04em;color:var(--nli-sea-deep)}.nlbh3-note.is-stop b{color:var(--nli-survey)}',
      '.nlbh3-note ul{margin:4px 0 0;padding:0 18px 0 0}html body .nli .nlbh3 .nlbh3-note li{margin:0 0 4px;font:400 14px/22px var(--nli-sans) !important}',
      /* bpay */
      '.nlbh3-bar{display:flex;height:12px;border-radius:2px;overflow:hidden;margin:16px 0 6px;background:var(--nli-line);position:relative}.nlbh3-bar i{display:block;height:100%;min-width:2px}',
      '.nlbh3-c1{background:#2F6F86}.nlbh3-c2{background:#1F4B5C}.nlbh3-c3{background:#4F9A5C}.nlbh3-c4{background:#F2D15A}.nlbh3-c5{background:#12202A}',
      'html body .nli .nlbh3 ul.nlbh3-lg{display:flex;flex-wrap:wrap;gap:4px 14px;list-style:none;margin:0;padding:0;position:relative}html body .nli .nlbh3 .nlbh3-lg li{display:flex;align-items:center;gap:6px;margin:0;font:400 12.5px/18px var(--nli-sans) !important;color:var(--nli-ink2)}.nlbh3-lg li i{width:10px;height:10px;border-radius:1px;display:inline-block}',
      'html body .nli .nlbh3 ol.nlbh3-pay{list-style:none;margin:12px 0 0;padding:0;display:grid;position:relative}',
      'html body .nli .nlbh3 ol.nlbh3-pay>li{display:grid;grid-template-columns:30px minmax(0,1fr);gap:4px 12px;padding:14px 0;margin:0;border-top:1px solid var(--nli-line)}',
      '.nlbh3-no{grid-row:1/span 2;width:26px;height:26px;display:grid;place-items:center;font:500 13px/1 var(--nli-mono);color:#fff;border-radius:2px}.nlbh3-no.nlbh3-c4{color:var(--nli-ink)}',
      '.nlbh3-pay li.is-zero .nlbh3-no{background:none;border:1.5px dashed var(--nli-mute);color:var(--nli-mute)}',
      '.nlbh3-m{display:grid;gap:1px;min-width:0}.nlbh3-m .w{font:600 15px/22px var(--nli-sans);color:var(--nli-ink)}',
      '.nlbh3-m .a{font:500 22px/30px var(--nli-mono);color:var(--nli-ink);direction:ltr;unicode-bidi:plaintext;text-align:right;font-variant-numeric:tabular-nums}.nlbh3-pay li.is-zero .a{color:var(--nli-mute)}',
      '.nlbh3-m .t{font:400 14px/21px var(--nli-sans);color:var(--nli-ink2)}.nlbh3-m .f{font:400 12.5px/18px var(--nli-sans);color:var(--nli-mute)}',
      '.nlbh3-safe{grid-column:2;font:500 13.5px/20px var(--nli-sans);color:var(--b3-grn-ink);min-width:0}.nlbh3-safe.is-law{color:var(--nli-survey)}.nlbh3-safe.is-none{color:var(--nli-mute);font-weight:400}',
      '.nlbh3-safe small{display:block;font:400 12px/17px var(--nli-sans);color:var(--nli-mute);margin-top:2px}html body .nli .nlbh3 .nlbh3-safe a{color:var(--nli-sea) !important;text-decoration:underline}',
      '@media (min-width:760px){html body .nli .nlbh3 ol.nlbh3-pay>li{grid-template-columns:30px minmax(0,1.1fr) minmax(0,1fr);align-items:start}.nlbh3-safe{grid-column:3;grid-row:1/span 2}}',
      'html body .nli .nlbh3 ul.nlbh3-dl{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:2px}html body .nli .nlbh3 .nlbh3-dl li{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 12px;margin:0;padding:6px 0;border-bottom:1px dashed var(--nli-line);font:400 14px/21px var(--nli-sans) !important;color:var(--nli-ink)}',
      '.nlbh3-dl li span{font:500 14px/21px var(--nli-mono);direction:ltr;unicode-bidi:plaintext}.nlbh3-dl li span.is-late{color:var(--nli-survey)}',
      /* checklists (bsign, bkeys) */
      'html body .nli .nlbh3 ul.nlbh3-chk{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:6px;position:relative}html body .nli .nlbh3 ul.nlbh3-chk>li{margin:0;padding:0}',
      'html body .nli .nlbh3 .nlbh3-chk label{display:flex;gap:10px;align-items:flex-start;min-height:48px;padding:11px 12px;border:1px solid var(--nli-line);border-radius:2px;background:#fff;font:400 15px/22px var(--nli-sans);color:var(--nli-ink);cursor:pointer;margin:0;text-transform:none;letter-spacing:0}',
      'html body .nli .nlbh3 .nlbh3-chk input[type=checkbox]{-webkit-appearance:checkbox !important;appearance:auto !important;width:22px !important;height:22px !important;min-width:22px;min-height:0 !important;margin:0 !important;padding:0 !important;flex:none;accent-color:var(--b3-grn);border:0 !important;box-shadow:none !important;background:none !important;position:static;opacity:1}',
      '.nlbh3-chk label span{display:block;min-width:0}.nlbh3-chk label small{display:block;font:400 12.5px/18px var(--nli-sans);color:var(--nli-mute);margin-top:2px}html body .nli .nlbh3 .nlbh3-chk label small a{color:var(--nli-sea) !important;text-decoration:underline}',
      'html body .nli .nlbh3 .nlbh3-chk label:has(input:checked){border-color:var(--b3-grn);background:var(--b3-grn-tint)}',
      'html body .nli .nlbh3 .nlbh3-chk input:focus-visible{outline:2px solid var(--nli-focus);outline-offset:2px}',
      '.nlbh3-cols{display:grid;gap:4px 16px;margin:4px 0 0;position:relative}@media (min-width:860px){.nlbh3-cols{grid-template-columns:repeat(3,minmax(0,1fr))}}.nlbh3-cols>div{min-width:0}',
      '.nlbh3-prog{display:flex;flex-wrap:wrap;align-items:center;gap:4px 12px;margin:14px 0 0;font:500 13px/18px var(--b3-label);color:var(--nli-ink2);position:relative}.nlbh3-prog .nlbh-bar{flex:1 1 160px;margin:0}.nlbh3-prog .nlbh-bar i{background:var(--b3-grn)}',
      'html body .nli .nlbh3 textarea.nlbh3-ta{display:block;width:100%;min-height:92px;border:1px solid var(--nli-line) !important;border-radius:2px;padding:10px 12px;font:400 15px/23px var(--nli-sans);background:#fff !important;box-shadow:none !important;color:var(--nli-ink);margin:0;resize:vertical}',
      'html body .nli .nlbh3 textarea.nlbh3-ta:focus{border-color:var(--nli-sea) !important;outline:0;box-shadow:0 0 0 1px var(--nli-sea) !important}',
      '.nlbh3-two{display:grid;gap:12px 16px;position:relative}@media (min-width:760px){.nlbh3-two{grid-template-columns:repeat(2,minmax(0,1fr))}}',
      /* breg */
      'html body .nli .nlbh3 ol.nlbh3-reg{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:6px;position:relative}',
      'html body .nli .nlbh3 ol.nlbh3-reg>li{display:grid;grid-template-columns:30px minmax(0,1fr);gap:6px 12px;padding:10px 12px;margin:0;border:1px solid var(--nli-line);border-radius:2px;background:#fff}',
      'html body .nli .nlbh3 ol.nlbh3-reg>li.is-2{border-color:var(--b3-grn);background:var(--b3-grn-tint)}',
      '.nlbh3-reg .nlbh3-no{grid-row:auto;background:var(--nli-sea-deep)}.nlbh3-reg li.is-2 .nlbh3-no{background:var(--b3-grn)}',
      '.nlbh3-reg .m{display:grid;gap:2px;min-width:0}.nlbh3-reg .m b{font:600 15px/22px var(--nli-sans);color:var(--nli-ink)}.nlbh3-reg .m small{font:400 13px/19px var(--nli-sans);color:var(--nli-mute)}',
      '.nlbh3-reg .due{font:500 12.5px/18px var(--b3-label);color:var(--nli-sea-deep)}.nlbh3-reg .due.is-late{color:var(--nli-survey)}',
      '.nlbh3-st{grid-column:2;display:flex;flex-wrap:wrap;gap:6px}@media (min-width:760px){html body .nli .nlbh3 ol.nlbh3-reg>li{grid-template-columns:30px minmax(0,1fr) auto;align-items:center}.nlbh3-st{grid-column:3}}',
      'html body .nli .nlbh3 .nlbh3-st button,html body .nli .nlbh3 .nlbh3-yn button{min-width:64px;min-height:44px;padding:6px 12px;border:1px solid var(--nli-line);border-radius:999px;background:#fff;color:var(--nli-ink2);font:500 14px/1 var(--nli-sans);cursor:pointer;margin:0;box-shadow:none;text-transform:none;letter-spacing:0}',
      '@media (max-width:600px){html body .nli .nlbh3 .nlbh3-st button,html body .nli .nlbh3 .nlbh3-yn button{min-height:48px}}',
      'html body .nli .nlbh3 .nlbh3-st button[aria-pressed="true"][data-v="0"]{background:#E9EDEF;border-color:#93A3AE;color:var(--nli-ink)}',
      'html body .nli .nlbh3 .nlbh3-st button[aria-pressed="true"][data-v="1"]{background:var(--nli-sea);border-color:var(--nli-sea);color:#fff}',
      'html body .nli .nlbh3 .nlbh3-st button[aria-pressed="true"][data-v="2"]{background:var(--b3-grn);border-color:var(--b3-grn);color:#fff}',
      'html body .nli .nlbh3 .nlbh3-yn button[aria-pressed="true"]{background:var(--nli-ink);border-color:var(--nli-ink);color:#fff}',
      /* bmemo */
      '.nlbh3-q{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px 14px;align-items:center;padding:10px 0;border-bottom:1px dashed var(--nli-line);position:relative}@media (max-width:520px){.nlbh3-q{grid-template-columns:1fr}}',
      '.nlbh3-q>span{font:400 15px/23px var(--nli-sans);color:var(--nli-ink)}.nlbh3-yn{display:flex;gap:6px}',
      '.nlbh3-risk{border:1px solid var(--nli-ink);border-radius:2px;padding:14px;background:#fff;margin:14px 0 0;position:relative}.nlbh3-risk.is-high{border-color:var(--nli-survey)}.nlbh3-risk.is-low{border-color:var(--b3-grn)}',
      '.nlbh3-risk .lv{display:block;font:700 34px/36px var(--nli-display);color:var(--nli-ink)}.nlbh3-risk.is-high .lv{color:var(--nli-survey)}.nlbh3-risk.is-low .lv{color:var(--b3-grn-ink)}',
      '.nlbh3-risk .d{display:block;font:400 15px/24px var(--nli-sans);color:var(--nli-ink);margin:6px 0 0}.nlbh3-risk .nx{display:block;font:600 15.5px/24px var(--nli-sans);color:var(--nli-ink);margin:8px 0 0}',
      'html body .nli .nlbh3 .nlbh3-risk ul{margin:8px 0 0;padding:0 18px 0 0}html body .nli .nlbh3 .nlbh3-risk li{margin:0 0 2px;font:400 14px/21px var(--nli-sans) !important;color:var(--nli-ink2)}',
      '.nlbh3-risk .disc{display:block;font:500 13px/19px var(--nli-sans);color:var(--nli-mute);border-top:1px solid var(--nli-line);padding-top:8px;margin:10px 0 0}html body .nli .nlbh3 .nlbh3-risk a{color:var(--nli-sea) !important;text-decoration:underline}',
      '.nlbh3-left{margin:14px 0 0;font:500 13.5px/20px var(--nli-sans);color:var(--nli-mute);position:relative}',
      /* print additions (the print host itself is buying.js) */
      '#nlbh-print-host .nlbh3-box{display:inline-block;width:10pt;height:10pt;border:1px solid #000;margin-inline-end:6pt;vertical-align:-1pt;text-align:center;font-size:8pt;line-height:9pt}',
      '#nlbh-print-host .nlbh3-signs{display:grid;grid-template-columns:1fr 1fr;gap:28pt;margin-top:30pt}#nlbh-print-host .nlbh3-signs div{border-top:1px solid #000;padding-top:4pt;font-size:10pt}',
      '#nlbh-print-host small{display:block;color:#444;font-size:9.5pt}'
    ].join('');
    DOC.head.appendChild(s);
  }
  /* the tool's styles go in after the panel's own (prices-common, buying.js), so the 44/48 px rules win the ties */
  function setup(root, kicker, name, D0) { var M = B.model(D0), p = H.panel(root, kicker, name); css(); p.classList.add('nlbh3'); return { M: M, p: p, sub: (p.querySelector('.nli__title') || {}).tagName === 'H3' ? 'h4' : 'h3' }; }
  function sh(tag, text) { return U.el(tag, 'nlbh3-sh', esc(text)); }
  function rid() { return 'nlbh3-' + Math.random().toString(36).slice(2, 8); }
  function getJ(k) { try { var s = W.localStorage.getItem(k); return s ? JSON.parse(s) : null; } catch (e) { return null; } }
  function putJ(k, v) { try { W.localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function delJ(k) { try { W.localStorage.removeItem(k); } catch (e) {} }
  function today() { var d = new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function signGet() { var s = H.load().sign; return ISO.test(s || '') ? s : ''; }
  function signPut(v) { var o = H.load(); if (ISO.test(v || '')) o.sign = v; else delete o.sign; H.save(o); try { DOC.dispatchEvent(new CustomEvent('nlbh:sign', { detail: v || '' })); } catch (e) {} }
  function onSign(cb) { DOC.addEventListener('nlbh:sign', function (e) { cb(e.detail || ''); }); }
  function help(f, text) { if (!text) return f; var id = rid(), s = U.el('span', 'nli__help', esc(text)); s.id = id; f.appendChild(s); var i = f.querySelector('input,select,textarea'); if (i) i.setAttribute('aria-describedby', id); return f; }
  function bad(f, on) { if (!f) return; f.classList.toggle('is-bad', !!on); var i = f.querySelector('input'); if (i) { if (on) i.setAttribute('aria-invalid', 'true'); else i.removeAttribute('aria-invalid'); } }
  function dateField(label, val, on) {
    var f = U.el('div', 'nli__f'), id = rid(), l = U.el('label', '', esc(label)); l.htmlFor = id; f.appendChild(l);
    var ib = U.el('div', 'nli__in'), i = DOC.createElement('input'); i.type = 'date'; i.id = id; i.value = val || '';
    i.addEventListener('change', function () { if (i.value === '' || ISO.test(i.value)) on(i.value); }); ib.appendChild(i); f.appendChild(ib);
    f.set = function (v) { i.value = v || ''; }; f.inp = i; return f;
  }
  function textField(label, unit, val, on) {
    var f = U.el('div', 'nli__f'), id = rid(), l = U.el('label', '', esc(label)); l.htmlFor = id; f.appendChild(l);
    var ib = U.el('div', 'nli__in'), i = DOC.createElement('input'); i.type = 'text'; i.id = id; i.inputMode = 'decimal'; i.autocomplete = 'off'; i.value = val || '';
    i.addEventListener('input', function () { on(i.value.trim()); }); ib.appendChild(i); if (unit) ib.appendChild(U.el('span', 'nlbh-u', esc(unit))); f.appendChild(ib);
    f.set = function (v) { i.value = v || ''; }; return f;
  }
  function area(label, val, on, ph) {
    var f = U.el('div', 'nli__f'), id = rid(), l = U.el('label', '', esc(label)); l.htmlFor = id; f.appendChild(l);
    var t = DOC.createElement('textarea'); t.id = id; t.className = 'nlbh3-ta'; t.value = val || ''; if (ph) t.placeholder = ph;
    t.addEventListener('input', function () { on(t.value); }); f.appendChild(t); f.set = function (v) { t.value = v || ''; }; return f;
  }
  function btn(label, on) { var b = U.el('button', '', esc(label)); b.type = 'button'; b.addEventListener('click', on); return b; }
  function acts(p, list) { var a = U.el('div', 'nlbh-acts'); list.forEach(function (b) { a.appendChild(b); }); p.appendChild(a); return a; }
  function srcLine(list) { var e = U.el('p', 'nli__src'); e.innerHTML = 'מקורות: ' + list.filter(Boolean).map(H.src1).join(' · '); return e; }
  function law(BU, k) { var l = BU.laws && BU.laws[k]; return l ? { label: l.label, url: l.url, date: l.date } : null; }
  function srcOf(BU, s) { return !s ? null : typeof s === 'string' ? law(BU, s) : s.label ? s : null; }
  function note(cls, head, html) { return '<div class="nlbh3-note' + (cls ? ' ' + cls : '') + '"><div>' + (head ? '<b>' + esc(head) + '</b>' : '') + html + '</div></div>'; }
  function prog(n, all, word, more) { return '<div class="nlbh3-prog"><span>' + esc(word + ' ' + n + ' מתוך ' + all + (more ? ' · ' + more : '')) + '</span><div class="nlbh-bar" aria-hidden="true"><i style="width:' + (all ? Math.round(100 * n / all) : 0) + '%"></i></div></div>'; }
  function checklist(items, isOn, onTick) {
    var ul = U.el('ul', 'nlbh3-chk');
    items.forEach(function (x, i) {
      var li = DOC.createElement('li'), lab = DOC.createElement('label'), c = DOC.createElement('input'); c.type = 'checkbox'; c.checked = !!isOn(i);
      c.addEventListener('change', function () { onTick(i, c.checked); });
      lab.appendChild(c); var sp = U.el('span', '', esc(x.t) + (x.d ? '<small>' + x.d + '</small>' : '')); lab.appendChild(sp); li.appendChild(lab); ul.appendChild(li);
    });
    return ul;
  }

  /* ---------------- bpay ---------------- */
  NI.register('bpay', { custom: function (root, D0) {
    var o = setup(root, 'לוח תשלומים · עסקת יד שנייה', 'לוח התשלומים שלכם בעסקת יד שנייה', D0), M = o.M, p = o.p, BU = M.buying, PY = BU.pay, OA = M.orechdin.cgt_advance, NR = M.nrm, KEY = 'nlbh-pay-v1';
    var IT = {}; PY.items.forEach(function (x) { IT[x.id] = x; });
    var advRow = BU.who.filter(function (r) { return r.src === PY.adv_src; })[0], advSrc = { label: M.orechdin.sources.TAX.label, url: M.orechdin.sources.TAX.url, date: M.orechdin.checked };
    var L4 = B.lastQ(M.phub.il.r4, M.phub.q), P0 = L4.v, L0 = Math.round(P0 * NR.ltv_by_status.cit_first / 1000) * 1000;
    p.appendChild(U.el('p', 'nlph-sub', esc('מקלידים את המחיר, המשכנתא ואת מה שסוכם על התשלום הראשון, ומקבלים את חמשת התשלומים לפי הסדר: מתי, כמה, למי, ומה מגן עליכם ברגע של כל תשלום. הנתונים נשמרים רק בדפדפן הזה.')));
    var S0 = getJ(KEY) || {};
    var st = { P: S0.P != null ? S0.P : P0, L: S0.L != null ? S0.L : L0, S: S0.S || 0, pct: S0.pct != null ? S0.pct : 10, adv: S0.adv || 'std', sign: signGet(), hand: ISO.test(S0.hand || '') ? S0.hand : '' };
    var f = U.el('div', 'nlbh-form'), F = {}; p.appendChild(f);
    F.P = help(H.field('מחיר הדירה', '₪', st.P, function (v) { st.P = v || 0; go(); }, true), 'נקודת הפתיחה: המחיר החציוני של דירת 4 חדרים בארץ ב' + W.NLPH.qLabel(L4.q) + ' (רשות המסים). הקלידו את המחיר שלכם.');
    F.L = help(H.field('המשכנתא שלכם', '₪', st.L, function (v) { st.L = v || 0; go(); }, true), 'הסכום שהבנק אישר לכם. נקודת הפתיחה היא ' + pc(NR.ltv_by_status.cit_first) + '% מהמחיר, המימון המרבי בדירה יחידה (הוראה 329 של בנק ישראל).');
    F.S = help(H.field('יתרת המשכנתא של המוכר', '₪', st.S, function (v) { st.S = v || 0; go(); }, true), PY.seller_help);
    F.pct = help(H.field('התשלום הראשון', '% מהמחיר', st.pct, function (v) { st.pct = v == null ? 0 : v; go(); }, false), PY.first_help);
    F.sign = help(dateField('תאריך החתימה (לא חובה)', st.sign, function (v) { st.sign = v; signPut(v); go(); }), 'נותן את המועדים לרשות המסים. אם הקלדתם אותו בלוח הזמנים של העמוד, הוא כבר כאן.');
    F.hand = help(dateField('תאריך המסירה (לא חובה)', st.hand, function (v) { st.hand = v; go(); }), 'כפי שנקבע בחוזה.');
    ['P', 'L', 'S', 'pct', 'sign', 'hand'].forEach(function (k) { f.appendChild(F[k]); });
    var tb = H.tabs('המקדמה על מס השבח של המוכר', [['std', pc(OA.rate) + '% מהמחיר'], ['old', pc(OA.rate_old) + '%: המוכר קנה לפני ' + date(OA.old_before)], ['none', 'לא חלה: המוכר הציג אישור']], st.adv, function (v) { st.adv = v; go(); }, true);
    p.appendChild(tb);
    var out = U.el('div', ''); out.setAttribute('aria-live', 'polite'); p.appendChild(out);
    var x = null, txt = '';
    onSign(function (v) { if (v !== st.sign) { st.sign = v; F.sign.set(v); draw(); } });
    function save() { putJ(KEY, { P: st.P, L: st.L, S: st.S, pct: st.pct, adv: st.adv, hand: st.hand }); }
    function go() { save(); draw(); }
    function from(r) { return r.own && r.loan ? 'מכספכם ' + U.ils(r.own) + ' ומכספי המשכנתא ' + U.ils(r.loan) : r.loan ? 'מכספי המשכנתא' : r.own ? 'מכספכם' : ''; }
    function whenOf(id) {
      var it = IT[id], w = B.fill(it.when, M);
      if (id === 'first' && x.dates) w += ', ' + date(x.dates.sign);
      if (id === 'last' && x.dates && x.dates.hand) w += ', ' + date(x.dates.hand);
      if (id === 'adv' && x.cross >= 0 && x.A > 0) w += ' (כאן: תשלום ' + (x.cross + 1) + ')';
      return w;
    }
    function draw() {
      x = X.pay({ P: st.P, L: st.L, S: st.S, pct: st.pct, adv: st.adv, sign: st.sign, hand: st.hand, O: OA, PT: M.ptax.pay, ltv: NR.ltv_by_status });
      var badF = {}; x.errs.forEach(function (e) { badF[e.f] = 1; }); Object.keys(F).forEach(function (k) { bad(F[k], badF[k]); });
      if (!x.ok) { out.innerHTML = note('is-stop', 'צריך לתקן לפני שהלוח מוכן', '<ul>' + x.errs.map(function (e) { return '<li>' + esc(e.t) + '</li>'; }).join('') + '</ul>'); txt = ''; return; }
      var R = x.rows, last = R[4].amt, h = '';
      h += '<div class="nlph-ans" style="margin-top:14px"><div class="nlph-ans__head"><span>חמשת התשלומים</span><small>' + esc('מחיר ' + U.ils(x.P) + (x.A ? ' · מקדמה ' + pc(x.rate) + '%' : '')) + '</small></div><p class="nlph-ans__a"><b>' + esc('מכספכם ' + U.ils(x.own) + ', ומהמשכנתא ' + U.ils(x.L) + '.') + '</b> ' +
        esc('ביום החתימה משלמים ' + U.ils(x.f) + (last ? ', וביום המסירה ' + U.ils(last) + ', מול המפתחות.' : '. לא נשאר תשלום ליום המסירה.')) + '</p>' +
        H.kpis([['מכספכם', H.big(x.own), pc(x.own / x.P, 1) + '% מהמחיר'], ['מהמשכנתא', H.big(x.L), pc(x.L / x.P, 1) + '% מהמחיר'], ['ביום החתימה', H.big(x.f), pc(x.pct / 100, 2) + '% מהמחיר'], ['ביום המסירה', H.big(last), last ? 'מול המפתחות' : 'לא נשאר', last ? '' : 'is-dn']]) + '</div>';
      var parts = R.map(function (r, i) { return { i: i, w: 100 * r.amt / x.P, t: IT[r.id].t }; }).filter(function (s) { return s.w > 0; });
      h += '<div class="nlbh3-bar" role="img" aria-label="' + esc('חלוקת המחיר: ' + parts.map(function (s) { return (s.i + 1) + '. ' + s.t + ' ' + pc(s.w / 100, 1) + '%'; }).join(', ')) + '">' + parts.map(function (s) { return '<i class="nlbh3-c' + (s.i + 1) + '" style="width:' + s.w.toFixed(3) + '%"></i>'; }).join('') + '</div>';
      h += '<ul class="nlbh3-lg" aria-hidden="true">' + parts.map(function (s) { return '<li><i class="nlbh3-c' + (s.i + 1) + '"></i>' + esc((s.i + 1) + ' ' + s.t) + '</li>'; }).join('') + '</ul>';
      h += '<ol class="nlbh3-pay" role="list">' + R.map(function (r, i) {
        var it = IT[r.id], zero = !r.amt, safe;
        if (r.id === 'adv') safe = zero ? '<div class="nlbh3-safe is-none">' + esc(it.none) + '</div>' : '<div class="nlbh3-safe is-law">' + esc('המקדמה לפי החוק: ' + B.fill(advRow.d, M) + '.') + '<small>מקור: ' + H.src1(advSrc) + '</small></div>';
        else safe = zero && it.none ? '<div class="nlbh3-safe is-none">' + esc(it.none) + '</div>' : '<div class="nlbh3-safe">' + esc('מה מגן עליכם: ' + it.safe) + '</div>';
        return '<li class="' + (zero ? 'is-zero' : '') + '" data-pay="' + r.id + '"><span class="nlbh3-no nlbh3-c' + (i + 1) + '" aria-hidden="true">' + (i + 1) + '</span><div class="nlbh3-m"><span class="w">' + esc(it.t + ': ' + whenOf(r.id)) + '</span><span class="a">' + esc(U.ils(r.amt)) + '</span><span class="t">' + esc(it.to) + '</span>' + (from(r) ? '<span class="f">' + esc(from(r)) + '</span>' : '') + '</div>' + safe + '</li>';
      }).join('') + '</ol>';
      x.warns.forEach(function (w) { h += note('', 'שימו לב', '<span>' + esc(w.k === 'nolast' ? IT.last.none : w.t) + '</span>'); });
      var Pp = M.ptax.pay;
      if (x.dates) h += '<h' + (o.sub === 'h4' ? '4' : '3') + ' class="nlbh3-sh">המועדים מתאריך החתימה</h' + (o.sub === 'h4' ? '4' : '3') + '><ul class="nlbh3-dl"><li>' + esc('הצהרה לרשות המסים, בתוך ' + Pp.declare_days + ' יום') + '<span>' + esc(date(x.dates.declare)) + '</span></li><li>' + esc('תשלום מס הרכישה, בתוך ' + Pp.pay_days + ' יום') + '<span>' + esc(date(x.dates.pay)) + '</span></li>' +
        (x.dates.hand ? '<li>' + esc('המסירה, ' + x.dates.handDays + ' ימים אחרי החתימה') + '<span>' + esc(date(x.dates.hand)) + '</span></li>' : '') + '</ul><p class="nli__src">מקור: ' + H.src1({ label: Pp.label, url: M.ptax.guide.url, date: M.ptax.checked }) + '</p>';
      else h += '<p class="nlph-fine">' + esc('הקלידו את תאריך החתימה, ויופיעו כאן המועדים לרשות המסים: הצהרה בתוך ' + Pp.declare_days + ' יום ותשלום מס הרכישה בתוך ' + Pp.pay_days + ' יום.') + '</p>';
      h += '<p class="nlph-fine">' + esc('הסכומים מחושבים מהמספרים שהקלדתם, לפי הסדר שבו הכסף עובר בעסקת יד שנייה מוגנת. את הלוח בפועל קובעים החוזה ועורך הדין שלכם. מס רכישה, עורך דין ותיווך משולמים בנפרד ולא נכנסו ללוח.') + '</p>';
      out.innerHTML = h;
      txt = 'לוח התשלומים שלי, דירה במחיר ' + U.ils(x.P) + ': ' + R.map(function (r, i) { return (i + 1) + '. ' + IT[r.id].t + ' ' + U.ils(r.amt); }).join('; ') + '. מכספי ' + U.ils(x.own) + ', משכנתא ' + U.ils(x.L) + '.' + (x.dates ? ' הצהרה לרשות המסים עד ' + date(x.dates.declare) + ', מס רכישה עד ' + date(x.dates.pay) + '.' : '');
    }
    draw();
    p.appendChild(srcLine([advSrc, { label: NR.ltv_source.label_he, url: NR.ltv_source.url, date: NR.checked }, { label: M.phub.vsrc.he + ', גרסה ' + M.phub.vsrc.version, url: M.phub.vsrc.url }]));
    p.appendChild(U.share(function () { return txt || 'לוח התשלומים בעסקת יד שנייה'; }));
    acts(p, [H.printBtn(function () {
      if (!x || !x.ok) return '<h2>לוח התשלומים בעסקת יד שנייה</h2><p>' + esc(x ? x.errs.map(function (e) { return e.t; }).join(' ') : '') + '</p>';
      return '<h2>' + esc('לוח התשלומים: דירה במחיר ' + U.ils(x.P)) + '</h2><p>' + esc('מכספכם ' + U.ils(x.own) + ' · מהמשכנתא ' + U.ils(x.L) + (x.dates ? ' · חתימה ' + date(x.dates.sign) : '') + (x.dates && x.dates.hand ? ' · מסירה ' + date(x.dates.hand) : '')) + '</p>' +
        '<table><thead><tr><th>#</th><th>מה ומתי</th><th>כמה</th><th>למי</th><th>מה מגן עליכם</th></tr></thead><tbody>' + x.rows.map(function (r, i) { var it = IT[r.id]; return '<tr><td>' + (i + 1) + '</td><td><b>' + esc(it.t) + '</b><br>' + esc(whenOf(r.id)) + '</td><td>' + esc(U.ils(r.amt)) + (from(r) ? '<small>' + esc(from(r)) + '</small>' : '') + '</td><td>' + esc(it.to) + '</td><td>' + esc(r.id === 'adv' ? (r.amt ? B.fill(advRow.d, M) : it.none) : (!r.amt && it.none ? it.none : it.safe)) + '</td></tr>'; }).join('') + '</tbody></table>' +
        (x.dates ? '<p>' + esc('הצהרה לרשות המסים עד ' + date(x.dates.declare) + '; תשלום מס הרכישה עד ' + date(x.dates.pay) + '.') + '</p>' : '') + '<p><small>' + esc('מקור כלל המקדמה: ' + advSrc.label + ', נבדק ' + date(advSrc.date) + '. הלוח בפועל נקבע בחוזה.') + '</small></p>';
    }), btn('ניקוי הנתונים', function () { delJ(KEY); st.P = P0; st.L = L0; st.S = 0; st.pct = 10; st.adv = 'std'; st.hand = ''; F.P.set(P0); F.L.set(L0); F.S.set(0); F.pct.set(10); F.hand.set(''); [].forEach.call(tb.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-v') === 'std')); }); draw(); })]);
  } });

  /* ---------------- bsign ---------------- */
  NI.register('bsign', { custom: function (root, D0) {
    var o = setup(root, 'רשימה · יום החתימה', 'יום החתימה: מה מביאים, על מה חותמים, עם מה יוצאים', D0), M = o.M, p = o.p, BU = M.buying, SG = BU.sign, KEY = 'nlbh-sign-v1';
    p.appendChild(U.el('p', 'nlph-sub', esc('שלוש רשימות ליום החתימה על חוזה לדירה יד שנייה. מסמנים מה כבר מוכן; הסימון נשמר רק בדפדפן הזה, ואפשר להדפיס או לשמור כ־PDF ולהביא לפגישה.')));
    var t = getJ(KEY) || { b: {}, s: {}, l: {} }, sign = signGet(), G3 = [['b', 'bring', 'מביאים'], ['s', 'sign', 'חותמים'], ['l', 'leave', 'יוצאים עם']];
    var top = U.el('div', ''); top.setAttribute('aria-live', 'polite'); p.appendChild(top);
    var cols = U.el('div', 'nlbh3-cols'); p.appendChild(cols);
    function itemD(x) {
      var d = esc(B.fill(x.d || '', M)), s = srcOf(BU, x.src);
      if (x.dates && sign) d += esc(': עד ' + date(X.addDays(sign, M.ptax.pay.declare_days)) + ' ועד ' + date(X.addDays(sign, M.ptax.pay.pay_days)));
      return d + (s ? ' · ' + H.src1(s) : '');
    }
    function count() { var c = X.ticks({ b: SG.bring, s: SG.sign, l: SG.leave }, t); top.innerHTML = prog(c.n, c.all, 'מוכנים'); }
    function draw() {
      cols.innerHTML = '';
      G3.forEach(function (g) {
        var c = DOC.createElement('div'); c.appendChild(sh(o.sub, g[2]));
        c.appendChild(checklist(SG[g[1]].map(function (x) { return { t: x.t, d: itemD(x) }; }), function (i) { return t[g[0]] && t[g[0]][i]; }, function (i, on) { t[g[0]] = t[g[0]] || {}; if (on) t[g[0]][i] = 1; else delete t[g[0]][i]; putJ(KEY, t); count(); }));
        cols.appendChild(c);
      });
      count();
    }
    draw();
    onSign(function (v) { sign = v; draw(); });
    p.appendChild(U.el('p', 'nlph-fine', esc('הרשימה כללית לעסקת יד שנייה. מה שנקבע בחוזה שלכם, ומה שעורך הדין מבקש, קודם לה.')));
    acts(p, [H.printBtn(function () {
      return '<h2>יום החתימה: מה מביאים, על מה חותמים, עם מה יוצאים</h2>' + (sign ? '<p>' + esc('חתימה ב־' + date(sign)) + '</p>' : '') + G3.map(function (g) {
        return '<h3>' + esc(g[2]) + '</h3><ul style="list-style:none;padding:0">' + SG[g[1]].map(function (x, i) { var on = t[g[0]] && t[g[0]][i]; var s = srcOf(BU, x.src); return '<li><span class="nlbh3-box">' + (on ? '✓' : '') + '</span><b>' + esc(x.t) + '</b>' + (x.d ? '<small>' + esc(B.fill(x.d, M)) + (x.dates && sign ? esc(': עד ' + date(X.addDays(sign, M.ptax.pay.declare_days)) + ' ועד ' + date(X.addDays(sign, M.ptax.pay.pay_days))) : '') + (s ? esc(' · ' + s.label) : '') + '</small>' : '') + '</li>'; }).join('') + '</ul>';
      }).join('');
    }), btn('ניקוי הסימונים', function () { t = { b: {}, s: {}, l: {} }; delJ(KEY); draw(); })]);
  } });

  /* ---------------- bkeys ---------------- */
  NI.register('bkeys', { custom: function (root, D0) {
    var o = setup(root, 'פרוטוקול · יום המסירה', 'פרוטוקול מסירה וקריאת מונים', D0), M = o.M, p = o.p, BU = M.buying, K = BU.keys, KEY = 'nlbh-keys-v1';
    p.appendChild(U.el('p', 'nlph-sub', esc('ביום המסירה רושמים את המונים, סופרים מפתחות ושלטים, כותבים מה נשאר בדירה ומה צריך תיקון, ומסמנים את ההעברות על שמכם. הכול נשמר רק בדפדפן הזה, והדף המודפס מוכן לחתימת שני הצדדים.')));
    var pay = getJ('nlbh-pay-v1') || {}, st = getJ(KEY) || {}; st.m = st.m || {}; st.c = st.c || {}; st.t = st.t || {}; if (!ISO.test(st.date || '')) st.date = ISO.test(pay.hand || '') ? pay.hand : today();
    var F = [];
    function save() { putJ(KEY, st); }
    var g0 = U.el('div', 'nlbh-form'); p.appendChild(g0);
    var fd = dateField('תאריך המסירה', st.date, function (v) { st.date = v; save(); }); F.push(function () { fd.set(st.date); }); g0.appendChild(fd);
    p.appendChild(sh(o.sub, 'קריאת מונים'));
    var g1 = U.el('div', 'nlbh-form'); p.appendChild(g1);
    K.meters.forEach(function (m) { var ff = textField(m.t, m.u, st.m[m.id], function (v) { st.m[m.id] = v; save(); }); if (m.id === 'gas') help(ff, 'אם אין מונה גז בדירה, השאירו ריק.'); F.push(function () { ff.set(st.m[m.id]); }); g1.appendChild(ff); });
    p.appendChild(sh(o.sub, 'מפתחות ושלטים'));
    var g2 = U.el('div', 'nlbh-form'); p.appendChild(g2);
    K.counts.forEach(function (m) { var ff = textField(m.t, m.u, st.c[m.id], function (v) { st.c[m.id] = v; save(); }); F.push(function () { ff.set(st.c[m.id]); }); g2.appendChild(ff); });
    p.appendChild(sh(o.sub, 'ליקויים ומה שנשאר בדירה'));
    var g3 = U.el('div', 'nlbh3-two'); p.appendChild(g3);
    var fa = area('ליקויים שמצאתם במסירה', st.def, function (v) { st.def = v; save(); }, 'כל ליקוי בשורה: איפה, מה, ומי מתקן'), fb = area('מה נשאר בדירה', st.stay, function (v) { st.stay = v; save(); }, 'כל פריט בשורה, כפי שסוכם בחוזה');
    F.push(function () { fa.set(st.def); fb.set(st.stay); }); g3.appendChild(fa); g3.appendChild(fb);
    p.appendChild(sh(o.sub, 'אחרי המסירה: ההעברות על שמכם'));
    var tw = U.el('div', ''); tw.setAttribute('aria-live', 'polite'); p.appendChild(tw);
    function tdesc(x) { var s = srcOf(BU, x.src); return (x.how ? esc(x.how) : '') + (s ? (x.how ? ' · ' : '') + 'מקור: ' + H.src1(s) : ''); }
    function drawT() {
      tw.innerHTML = ''; var n = K.transfers.filter(function (x) { return st.t[x.id]; }).length;
      tw.innerHTML = prog(n, K.transfers.length, 'הועברו');
      tw.appendChild(checklist(K.transfers.map(function (x) { return { t: x.t, d: tdesc(x) }; }), function (i) { return st.t[K.transfers[i].id]; }, function (i, on) { if (on) st.t[K.transfers[i].id] = 1; else delete st.t[K.transfers[i].id]; save(); drawT(); var c = tw.querySelectorAll('input')[i]; if (c) c.focus(); }));
    }
    drawT();
    acts(p, [H.printBtn(function () {
      var rows = function (list, vals) { return list.map(function (m) { return '<tr><td>' + esc(m.t) + '</td><td>' + esc(vals[m.id] || '') + ' ' + esc(vals[m.id] ? m.u : '') + '</td></tr>'; }).join(''); };
      var lines = function (s) { return String(s || '').split(/\n+/).map(function (l) { return l.trim(); }).filter(Boolean); };
      var ul = function (s) { var l = lines(s); return l.length ? '<ul>' + l.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>' : '<p>אין.</p>'; };
      return '<h2>' + esc('פרוטוקול מסירה, ' + date(st.date)) + '</h2><h3>קריאת מונים ומפתחות</h3><table><tbody>' + rows(K.meters, st.m) + rows(K.counts, st.c) + '</tbody></table>' +
        '<h3>ליקויים שנמצאו</h3>' + ul(st.def) + '<h3>מה נשאר בדירה</h3>' + ul(st.stay) +
        '<h3>ההעברות על שם הקונים</h3><ul style="list-style:none;padding:0">' + K.transfers.map(function (x) { var s = srcOf(BU, x.src); return '<li><span class="nlbh3-box">' + (st.t[x.id] ? '✓' : '') + '</span>' + esc(x.t) + (x.how || s ? '<small>' + esc((x.how || '') + (s ? (x.how ? ' · ' : '') + 'מקור: ' + s.label : '')) + '</small>' : '') + '</li>'; }).join('') + '</ul>' +
        '<div class="nlbh3-signs"><div>חתימת הקונים</div><div>חתימת המוכרים</div></div>';
    }), btn('ניקוי הפרוטוקול', function () { delJ(KEY); st = { m: {}, c: {}, t: {}, def: '', stay: '', date: today() }; F.forEach(function (fn) { fn(); }); drawT(); })]);
  } });

  /* ---------------- breg ---------------- */
  NI.register('breg', { custom: function (root, D0) {
    var o = setup(root, 'מעקב · אחרי החתימה', 'מעקב רישום: מהחתימה ועד נסח על שמכם', D0), M = o.M, p = o.p, BU = M.buying, RG = BU.reg, Pp = M.ptax.pay, KEY = 'nlbh-reg-v1', LAB = ['טרם', 'נשלח', 'התקבל'];
    p.appendChild(U.el('p', 'nlph-sub', esc('עשרת השלבים שאחרי החתימה, לפי הסדר: מי עושה כל שלב, איזה מסמך מוכיח שהוא נעשה, ואיפה הוא עומד. עם תאריך החתימה מופיעים גם המועדים לרשות המסים. הסטטוס נשמר רק בדפדפן הזה.')));
    var S0 = getJ(KEY) || {}, st = S0.st || {}, sign = signGet();
    var f = U.el('div', 'nlbh-form'); p.appendChild(f);
    var fs = help(dateField('תאריך החתימה', sign, function (v) { sign = v; signPut(v); draw(); }), 'אם הקלדתם אותו בלוח הזמנים או בלוח התשלומים, הוא כבר כאן.'); f.appendChild(fs);
    onSign(function (v) { if (v !== sign) { sign = v; fs.set(v); draw(); } });
    var top = U.el('div', ''); top.setAttribute('aria-live', 'polite'); p.appendChild(top);
    var ol = U.el('ol', 'nlbh3-reg'); ol.setAttribute('role', 'list'); p.appendChild(ol);
    function save() { putJ(KEY, { st: st }); }
    function head() { var c = X.regCount(RG, st); top.innerHTML = prog(c[2], RG.length, 'התקבלו', c[1] ? 'נשלחו ומחכים ' + c[1] : ''); }
    function draw() {
      ol.innerHTML = ''; var td = today();
      RG.forEach(function (it, i) {
        var v = st[it.id] || 0, due = X.regDue(it, sign, Pp), late = due && due < td && v !== 2, s = srcOf(BU, it.src);
        var li = U.el('li', 'is-' + v); li.setAttribute('data-reg', it.id);
        li.innerHTML = '<span class="nlbh3-no" aria-hidden="true">' + (i + 1) + '</span><div class="m"><b>' + esc(it.t) + '</b><small>' + esc('מי: ' + it.who + ' · מה מוכיח: ' + it.doc) + (s ? ' · ' + H.src1(s) : '') + '</small>' +
          (it.due ? '<span class="due' + (late ? ' is-late' : '') + '">' + esc(due ? 'עד ' + date(due) + (late ? ' · המועד עבר' : '') : 'בתוך ' + (it.due === 'declare' ? Pp.declare_days : Pp.pay_days) + ' יום מהחתימה') + '</span>' : '') + '</div>';
        var g = U.el('div', 'nlbh3-st'); g.setAttribute('role', 'group'); g.setAttribute('aria-label', 'הסטטוס: ' + it.t);
        LAB.forEach(function (lab, k) { var b = U.el('button', '', esc(lab)); b.type = 'button'; b.setAttribute('data-v', String(k)); b.setAttribute('aria-pressed', String(v === k));
          b.addEventListener('click', function () { if (k) st[it.id] = k; else delete st[it.id]; save(); draw(); var nb = ol.querySelector('li[data-reg="' + it.id + '"] button[data-v="' + k + '"]'); if (nb) nb.focus(); }); g.appendChild(b); });
        li.appendChild(g); ol.appendChild(li);
      });
      head();
    }
    draw();
    p.appendChild(U.el('p', 'nlph-fine', esc(BU.reg_note)));
    p.appendChild(srcLine([{ label: Pp.label, url: M.ptax.guide.url, date: M.ptax.checked }, law(BU, 'm324')]));
    acts(p, [H.printBtn(function () {
      return '<h2>מעקב רישום: מהחתימה ועד נסח על שמכם</h2>' + (sign ? '<p>' + esc('חתימה ב־' + date(sign)) + '</p>' : '') + '<table><thead><tr><th>#</th><th>שלב</th><th>מי</th><th>מה מוכיח</th><th>עד</th><th>סטטוס</th></tr></thead><tbody>' +
        RG.map(function (it, i) { var due = X.regDue(it, sign, Pp); return '<tr><td>' + (i + 1) + '</td><td>' + esc(it.t) + '</td><td>' + esc(it.who) + '</td><td>' + esc(it.doc) + '</td><td>' + esc(due ? date(due) : '') + '</td><td>' + esc(LAB[st[it.id] || 0]) + '</td></tr>'; }).join('') + '</tbody></table><p><small>' + esc(BU.reg_note) + '</small></p>';
    }), btn('ניקוי הסטטוס', function () { st = {}; delJ(KEY); draw(); })]);
  } });

  /* ---------------- bmemo ---------------- */
  NI.register('bmemo', { custom: function (root, D0) {
    var o = setup(root, 'בדיקה · זיכרון דברים', 'חתמתם על זיכרון דברים? בודקים בדקה', D0), M = o.M, p = o.p, BU = M.buying, MM = BU.memo, l8 = law(BU, MM.law);
    p.appendChild(U.el('p', 'nlph-sub', esc('שש שאלות על מסמך שכבר חתמתם עליו, או שמבקשים מכם לחתום עליו. התשובות לא נשמרות: הן נמחקות כשיוצאים מהעמוד.')));
    var box = U.el('div', ''); p.appendChild(box);
    var out = U.el('div', ''); out.setAttribute('aria-live', 'polite'); p.appendChild(out);
    function qs() {
      box.innerHTML = '';
      MM.q.forEach(function (q) {
        var row = U.el('div', 'nlbh3-q'), id = rid(), lab = U.el('span', '', esc(q.t)); lab.id = id; row.appendChild(lab);
        var g = U.el('div', 'nlbh3-yn'); g.setAttribute('role', 'group'); g.setAttribute('aria-labelledby', id);
        [[true, 'כן'], [false, 'לא']].forEach(function (a) { var b = U.el('button', '', a[1]); b.type = 'button'; b.setAttribute('data-v', a[0] ? 'y' : 'n'); b.setAttribute('aria-pressed', String(MM_get(q.id) === a[0]));
          b.addEventListener('click', function () { if (MEMO[q.id] === a[0]) delete MEMO[q.id]; else MEMO[q.id] = a[0]; [].forEach.call(g.querySelectorAll('button'), function (z) { z.setAttribute('aria-pressed', String(MEMO[q.id] === (z.getAttribute('data-v') === 'y'))); }); draw(); }); g.appendChild(b); });
        row.appendChild(g); box.appendChild(row);
      });
    }
    function MM_get(k) { return k in MEMO ? MEMO[k] : null; }
    function draw() {
      var r = X.memo(MEMO);
      if (!r.level) { out.innerHTML = '<p class="nlbh3-left">' + esc(r.left === 1 ? 'עוד שאלה אחת, והתוצאה מופיעה כאן.' : 'ענו על עוד ' + r.left + ' שאלות, והתוצאה מופיעה כאן.') + '</p>'; return; }
      var L = MM.levels[r.level];
      out.innerHTML = '<div class="nlbh3-risk is-' + r.level + '" data-level="' + r.level + '"><span class="lv">' + esc(L.t) + '</span><span class="d">' + esc(L.d) + '</span><span class="nx">' + esc(L.next) + '</span>' +
        '<ul>' + MM.q.map(function (q) { return '<li>' + esc(MEMO[q.id] ? q.y : q.n) + '</li>'; }).join('') + '</ul>' +
        (l8 ? '<span class="disc">' + esc('סעיף 8 לחוק המקרקעין: "' + BU.laws[MM.law].text + '" ') + H.src1(l8) + '</span>' : '') + '<span class="disc">' + esc(MM.disc) + '</span></div>';
    }
    qs(); draw();
    acts(p, [btn('התחלה מחדש', function () { Object.keys(MEMO).forEach(function (k) { delete MEMO[k]; }); qs(); draw(); })]);
  } });
})();
