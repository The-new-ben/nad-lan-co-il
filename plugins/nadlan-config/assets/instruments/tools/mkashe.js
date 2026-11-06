/* NadLan Instruments · mkashe v1 (HAD-675, mortgage universe, 6.11.2026): "כשקשה לשלם", the mortgage hardship tool of
   /mortgage-calculator/ (pane #tool-kashe). LOCAL build, not released. Searches it answers (manual SERP 6.11.2026): אי החזר משכנתא,
   אי תשלום משכנתא, הקפאת משכנתא (לחצי שנה, ל־3 חודשים, השלכות, מילואים, מלחמה, שאגת הארי, עם כלביא), מחשבון הקפאת משכנתא,
   דחיית תשלומי משכנתא, כינוס נכסים משכנתא, משכנתא עם תיק הוצאה לפועל, התנגדות לביצוע משכנתא.
   Five parts, phone first:
   1. מחשבון הקפאת משכנתא: balance, months left, the rate (opens on the Bank of Israel average of new fixed not linked loans of the
      latest month, boi-mortgage.json "boim" rates.fixed_nl, labelled) or the payment (the rate is then solved from it), 1 to 6
      deferral months. Three ways side by side: דחייה מלאה (nothing paid, the interest joins the balance, the end date stays),
      ריבית בלבד (only interest paid, the principal waits, the end date stays), הארכת תקופה (nothing paid, the interest joins the
      balance, the loan grows by the deferral months). For each: the payment after, the extra total to the end, the interest of the
      deferral months; the cheapest in one sentence. Exact Spitzer, monthly rate = annual / 12, CPI unchanged (said on the page).
   2. אם כבר לא שילמתם: the timeline from the first missed payment (kashe.json timeline, ordered), with what protects you and what
      you can do at each step; an optional date gives the day of the 6-month line; the bank lines of banks.json; free help lines.
   3. The rights checklist: six situations, each right with its law section or Kol Zchut page and date.
   4. The wartime outlines of the Bank of Israel, dated, labelled "הסתיים" by date (never shown as open after their last day).
   5. A copyable summary (the numbers and the general rules only: no ticked situation), a link to the case (#mkashe=, the calculator
      numbers only, written only when the reader asks for a link), and every source with its date.
   Every rule, number, program and source is in data/kashe.json ("checked": "2026-11-06"); this file holds labels only.
   Pure logic in window.NLKS (node test: docs/research/2026-11-06-mortgage-universe/build/build-mkashe/test_mkashe.js). Hebrew only,
   RTL; on an English mount the tool draws nothing. No form is sent and nothing leaves the page. Style id-scoped (#nlks) with
   !important where the theme restyles headings, buttons, inputs and lists. */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;

  /* ------------------------------------------------------------------------------------------------------------- helpers */
  var NF = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function nf(x) { return NF.format(Math.round(x || 0)); }
  function ils(x) { return nf(x) + ' ₪'; }
  function pct(x, d) { return new Intl.NumberFormat('he-IL', { minimumFractionDigits: d == null ? 2 : d, maximumFractionDigits: d == null ? 2 : d }).format(x) + '%'; }
  function money(x) { if (typeof x === 'number') return isFinite(x) ? x : NaN; var s = String(x == null ? '' : x).replace(/[^\d.]/g, ''); if (s === '' || s === '.') return NaN; var n = +s; return isFinite(n) ? n : NaN; }
  function dec(x) { if (typeof x === 'number') return isFinite(x) ? x : NaN; var s = String(x == null ? '' : x).trim(); if (s.indexOf('.') < 0) s = s.replace(',', '.'); s = s.replace(/[^\d.]/g, ''); if (s === '' || s === '.') return NaN; var n = +s; return isFinite(n) ? n : NaN; }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function isISO(s) { return /^\d{4}-\d{2}-\d{2}$/.test(String(s || '')) && !isNaN(Date.parse(s)); }
  function todayISO(d) { d = d || new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function dmy(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : ''; }
  function addMonths(iso, m) {  // the same day m calendar months later; the 31st falls back to the month's last day
    var y = +iso.slice(0, 4), mo = +iso.slice(5, 7) - 1 + m, d = +iso.slice(8, 10);
    y += Math.floor(mo / 12); mo = ((mo % 12) + 12) % 12;
    var last = new Date(Date.UTC(y, mo + 1, 0)).getUTCDate();
    return y + '-' + pad(mo + 1) + '-' + pad(Math.min(d, last));
  }
  function err(field, msg) { return { error: { field: field, msg: msg } }; }

  /* --------------------------------------------------------------------------------------------------------------- math */
  function pmt(B, i, n) { return i === 0 ? B / n : B * i / (1 - Math.pow(1 + i, -n)); }
  /** The annual rate (%, monthly rate x 12) of a Spitzer loan from its balance, months and payment; null when no rate fits. */
  function solveRate(B, n, P) {
    if (!(B > 0 && n > 0 && P > 0)) return null;
    if (Math.abs(P * n - B) < 0.005 * n) return 0;
    if (P * n < B) return null;
    var lo = 0, hi = 0.03;  // up to 36% a year
    if (pmt(B, hi, n) < P) return null;
    for (var k = 0; k < 200; k++) { var mid = (lo + hi) / 2; if (pmt(B, mid, n) < P) lo = mid; else hi = mid; }
    return (lo + hi) / 2 * 1200;
  }
  /** Three ways to defer d months of a Spitzer loan: balance B, n months left, annual rate r (%). Totals are plain sums of payments. */
  function deferral(B, n, r, d) {
    var i = r / 1200, P0 = pmt(B, i, n), base = P0 * n, Bd = B * Math.pow(1 + i, d);
    var o = { B: B, n: n, r: r, d: d, i: i, P0: P0, base: base, by: {} };
    var full = { k: 'full', during: 0, acc: Bd - B, paid: false, bal: Bd, after: pmt(Bd, i, n - d), nAfter: n - d, shift: 0 };
    full.total = full.after * full.nAfter;
    var io = { k: 'io', during: B * i, acc: B * i * d, paid: true, bal: B, after: pmt(B, i, n - d), nAfter: n - d, shift: 0 };
    io.total = io.during * d + io.after * io.nAfter;
    var ext = { k: 'ext', during: 0, acc: Bd - B, paid: false, bal: Bd, after: pmt(Bd, i, n), nAfter: n, shift: d };
    ext.total = ext.after * ext.nAfter;
    [full, io, ext].forEach(function (x) { x.extra = x.total - base; x.delta = x.after - P0; o.by[x.k] = x; });
    o.list = [full, io, ext];
    var lo = o.list.reduce(function (a, x) { return x.extra < a.extra ? x : a; }, full), hi = o.list.reduce(function (a, x) { return x.extra > a.extra ? x : a; }, full);
    o.cheapest = hi.extra - lo.extra < 1 ? null : lo.k;  // null: no difference (a 0% rate)
    return o;
  }

  function defaults(boim) {
    var r = boimRate(boim);
    return { b: 1000000, n: 300, m: 'rate', r: r ? r.rate : '', p: '', d: 3, k: 'full', miss: '', sel: [] };
  }
  function boimRate(boim) {
    var s = boim && boim.rates && boim.rates.fixed_nl;
    if (!s || !isFinite(+s.rate)) return null;
    var h = s.hist && s.hist.length ? s.hist[s.hist.length - 1][0] : null;
    return { rate: +s.rate, month: h, label: s.label || '' };
  }

  /** v: {b, n, m: 'rate'|'pay', r, p, d}; K: kashe.json. Returns {error} or the three ways. */
  function compute(v, K) {
    if (!K || !K.calc || !K.rules) return err(null, 'הנתונים לא נטענו. רעננו את העמוד.');
    var C = K.calc, B = money(v.b), n = dec(v.n), d = dec(v.d);
    if (!(B >= 10000 && B <= 20000000)) return err('b', 'הקלידו יתרה בין 10,000 ל־20,000,000 ₪.');
    if (!(n >= 12 && n <= 480 && Math.floor(n) === n)) return err('n', 'הקלידו מספר חודשים שלם, מ־12 עד 480.');
    if (!(d >= C.months_min && d <= C.months_max && Math.floor(d) === d)) return err('d', 'בחרו ' + C.months_min + ' עד ' + C.months_max + ' חודשי דחייה.');
    var r, derived = false;
    if (v.m === 'pay') {
      var P = money(v.p);
      if (!(P > 0)) return err('p', 'הקלידו את ההחזר החודשי היום.');
      r = solveRate(B, n, P);
      if (r == null) return P * n < B ? err('p', 'ההחזר נמוך מדי: בלי ריבית בכלל ההחזר הוא ' + ils(B / n) + ' בחודש.') : err('p', 'ההחזר גבוה מדי ליתרה ולתקופה האלה.');
      if (r > 20) return err('p', 'ההחזר הזה יוצא בריבית של יותר מ־20%. בדקו את היתרה, את מספר החודשים ואת ההחזר.');
      derived = true;
    } else {
      r = dec(v.r);
      if (!(r >= 0 && r <= 20)) return err('r', 'הקלידו ריבית שנתית בין 0 ל־20%.');
    }
    var o = deferral(B, n, r, d);
    o.m = v.m === 'pay' ? 'pay' : 'rate'; o.derived = derived;
    return o;
  }

  /* ---------------------------------------------------------------------------------------------------------- the rules */
  function steps(K, miss) {
    var S = (K.timeline || []).slice().sort(function (a, b) { return a.order - b.order; });
    var at = isISO(miss) ? addMonths(miss, K.rules.enforce_months) : null;
    return S.map(function (s) { var x = Object.assign({}, s); x.date = s.k === 'day0' && at ? miss : s.k === 'six' && at ? at : null; return x; });
  }
  function rightsFor(sel, K) {
    sel = sel || [];
    return (K.rights.items || []).filter(function (it) { return it['for'].some(function (f) { return sel.indexOf(f) > -1; }); });
  }
  function programStatus(p, today) { today = isISO(today) ? today : todayISO(); return today > p.last ? 'ended' : 'open'; }
  function statusText(p, today) { return programStatus(p, today) === 'ended' ? 'הסתיים' : 'פתוח להגשה עד ' + dmy(p.last); }
  function srcOf(ref, K) {
    var a = String(ref).split(':'), id = a[0], sec = a.length > 1 ? a.slice(1).join(':') : '', s = K.sources[id];
    if (!s) return null;
    var dk = { edited: 'נבדק', updated: 'עודכן', published: 'פורסם', read: 'נבדק' }[s.date_kind] || 'נבדק';
    var date = s.date_kind === 'edited' ? s.read : s.date;
    var label = s.kind === 'kz' ? s.s + ': ' + s.t : s.kind === 'boi' ? s.t : s.s + (sec ? ', סעיף ' + sec : '');
    return { id: id, sec: sec, s: s, label: label, date: dk + ' ' + dmy(date), url: s.url, title: s.t };
  }

  var KIND_HE = { full: 'דחייה מלאה', io: 'ריבית בלבד', ext: 'הארכת תקופה' };
  function kindHe(K, k) { var x = (K.calc.kinds || []).filter(function (y) { return y.k === k; })[0]; return x ? x.he : KIND_HE[k]; }
  function cheapText(o, K) {
    if (!o.cheapest) return 'בריבית 0% אין עלות נוספת לאף אחת מהדרכים.';
    var c = o.by[o.cheapest];
    return 'הזולה ביותר בסך הכול: ' + kindHe(K, o.cheapest) + ', ' + ils(c.extra) + ' יותר מהמסלול בלי דחייה'
      + (c.during > 0 ? '. בחודשי הדחייה משלמים בה ' + ils(c.during) + ' בחודש, את הריבית בלבד.' : '.');
  }
  function lines(o, k, K) {  // the breakdown of one way, plain text pairs
    var x = o.by[k], L = [];
    L.push(['ההחזר היום', ils(o.P0)]);
    L.push(['ההחזר בחודשי הדחייה', x.during > 0 ? ils(x.during) : '0 ₪']);
    L.push([x.paid ? 'הריבית של חודשי הדחייה, משולמת בהם' : 'הריבית של חודשי הדחייה, מצטרפת ליתרה', ils(x.acc)]);
    L.push(['היתרה בסוף הדחייה', ils(x.bal)]);
    L.push(['ההחזר אחרי הדחייה', ils(x.after)]);
    L.push(['תשלומים אחרי הדחייה', nf(x.nAfter)]);
    L.push(['סוף ההלוואה', x.shift ? 'מתארך ב־' + x.shift + ' חודשים' : 'לא זז']);
    L.push(['סך התשלומים עד הסוף', ils(x.total)]);
    L.push(['סך התשלומים בלי דחייה', ils(o.base)]);
    L.push(['התוספת בסך הכול', ils(x.extra)]);
    return L;
  }
  function copyText(o, K) {
    var t = ['כשקשה לשלם את המשכנתא'];
    if (o && !o.error) {
      t.push('יתרה ' + ils(o.B) + ', ' + nf(o.n) + ' חודשים, ריבית ' + pct(o.r) + (o.derived ? ' (לפי ההחזר)' : '') + ': ההחזר היום ' + ils(o.P0) + '.');
      t.push('דחייה של ' + o.d + ' חודשים:');
      o.list.forEach(function (x) {
        t.push('· ' + kindHe(K, x.k) + ': ' + (x.during > 0 ? ils(x.during) + ' בחודשי הדחייה, ' : '') + 'אחר כך ' + ils(x.after) + ' בחודש, סך הכול ' + ils(x.extra) + ' יותר' + (x.shift ? '; ההלוואה מתארכת ב־' + x.shift + ' חודשים' : '') + '.');
      });
      t.push(cheapText(o, K));
    }
    t.push(K.texts.copy_rules);
    t.push(K.texts.not_advice + ' נבדק ' + dmy(K.checked) + '.');
    return t.join('\n');
  }

  /* the case in the address: #mkashe=... (base64url of the calculator numbers only) */
  function enc(o) { var s = JSON.stringify(o); var b = typeof btoa === 'function' ? btoa(unescape(encodeURIComponent(s))) : Buffer.from(s, 'utf8').toString('base64'); return b.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); }
  function decH(t) {
    try { var b = String(t).replace(/-/g, '+').replace(/_/g, '/'); while (b.length % 4) b += '='; var s = typeof atob === 'function' ? decodeURIComponent(escape(atob(b))) : Buffer.from(b, 'base64').toString('utf8'); var o = JSON.parse(s); return o && typeof o === 'object' ? o : null; } catch (e) { return null; }
  }
  function caseOf(v) { var o = { b: money(v.b), n: dec(v.n), m: v.m === 'pay' ? 'pay' : 'rate', d: dec(v.d), k: v.k }; if (o.m === 'pay') o.p = money(v.p); else o.r = dec(v.r); return o; }
  function fromCase(o, v) {  // only known keys, only sane values
    if (!o) return false;
    function ok(x) { return typeof x === 'number' && isFinite(x) && x >= 0; }
    if (ok(o.b)) v.b = o.b; if (ok(o.n)) v.n = o.n; if (o.m === 'pay' || o.m === 'rate') v.m = o.m;
    if (ok(o.r)) v.r = o.r; if (ok(o.p)) v.p = o.p; if (ok(o.d)) v.d = o.d; if (KIND_HE[o.k]) v.k = o.k;
    return true;
  }

  G.NLKS = { pmt: pmt, solveRate: solveRate, deferral: deferral, compute: compute, defaults: defaults, boimRate: boimRate, steps: steps,
    rightsFor: rightsFor, programStatus: programStatus, statusText: statusText, srcOf: srcOf, cheapText: cheapText, lines: lines,
    copyText: copyText, addMonths: addMonths, enc: enc, dec: decH, caseOf: caseOf, fromCase: fromCase, kindHe: kindHe, money: money, num: dec };
  if (!G.NadLanInstruments || typeof document === 'undefined') return;

  /* ------------------------------------------------------------------------------------------------------------ the page */
  var NI = G.NadLanInstruments, esc = NI.esc;
  function rich(s) {  // escaped text; amounts and star numbers kept whole in RTL
    return esc(s).replace(/(\d[\d,.]*(?:\s(?:מיליון|אלף))?\s₪)/g, '<bdi>$1</bdi>').replace(/(\*\d{3,5})/g, '<bdi dir="ltr">$1</bdi>');
  }
  var V = 'var(--nli-sans,"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif)', M = 'var(--nli-mono,"IBM Plex Mono",ui-monospace,monospace)';
  var INK = 'var(--nli-ink,#12202A)', INK2 = 'var(--nli-ink2,#3E4C58)', MUTE = 'var(--nli-mute,#5E6A75)', LINE = 'var(--nli-line,#D3DCE2)', SEA = 'var(--nli-sea,#2F6F86)',
    DEEP = 'var(--nli-sea-deep,#1F4B5C)', GROUND = 'var(--nli-ground,#F6F8F9)', RED = 'var(--nli-survey,#C42550)', GREEN = 'var(--nli-open,#4F9A5C)';
  var CSS = '#nlks{font-family:' + V + ';color:' + INK + ';background:#fff;border:1px solid ' + LINE + ';border-radius:6px;padding:16px;display:flex;flex-direction:column;gap:18px;margin:8px 0 16px;text-align:right}'
    + '#nlks *{box-sizing:border-box}#nlks [hidden]{display:none!important}'
    + '#nlks p.nlks__k{margin:0!important;font:500 12px/18px ' + V + '!important;letter-spacing:.04em;color:' + MUTE + '!important}'
    + '#nlks h2.nlks__h{margin:0!important;padding:0!important;border:0!important;font:600 22px/30px ' + V + '!important;color:' + INK + '!important;text-wrap:balance}#nlks h2.nlks__h::before,#nlks h2.nlks__h::after{display:none!important}'
    + '#nlks .nlks__fmiss{max-width:380px}#nlks p.nlks__lede{margin:0!important;font:400 15px/24px ' + V + '!important;color:' + INK2 + '!important;max-width:72ch}'
    + '#nlks .nlks__jump{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}@media (min-width:720px){#nlks .nlks__jump{grid-template-columns:repeat(4,minmax(0,1fr))}}'
    + '#nlks .nlks__jump button{min-height:44px!important;margin:0!important;padding:6px 8px!important;border:1px solid ' + LINE + '!important;border-radius:2px!important;background:#fff!important;color:' + DEEP + '!important;font:500 14px/1.3 ' + V + '!important;box-shadow:none!important;cursor:pointer;text-align:center;width:auto!important;text-transform:none!important;letter-spacing:0!important}'
    + '#nlks section.nlks__sec{display:flex;flex-direction:column;gap:12px;border-top:2px solid ' + INK + ';padding-top:14px;scroll-margin-top:72px}'
    + '#nlks h3.nlks__sh{margin:0!important;padding:0!important;border:0!important;font:600 19px/26px ' + V + '!important;color:' + DEEP + '!important}#nlks h3.nlks__sh::before,#nlks h3.nlks__sh::after{display:none!important}'
    + '#nlks p.nlks__p{margin:0!important;font:400 14px/22px ' + V + '!important;color:' + INK2 + '!important}'
    + '#nlks .nlks__grid{display:grid;grid-template-columns:minmax(0,1fr);gap:16px}@media (min-width:960px){#nlks{padding:24px}#nlks .nlks__grid{grid-template-columns:minmax(0,380px) minmax(0,1fr);gap:16px 28px;align-items:start}}'
    + '#nlks .nlks__form{display:flex;flex-direction:column;gap:12px;min-width:0}'
    + '#nlks .nlks__x2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;align-items:start}'
    + '#nlks .nlks__lab{display:block;font:500 13px/18px ' + V + '!important;color:' + INK2 + '!important;margin:0 0 6px!important}'
    + '#nlks .nlks__in{display:flex;align-items:stretch;gap:6px;height:48px;padding:0 10px;border:1px solid ' + SEA + ';border-radius:2px;background:#fff}'
    + '#nlks .nlks__in input{flex:1 1 auto;min-width:0;width:100%!important;max-width:100%!important;height:auto!important;min-height:44px!important;margin:0!important;border:0!important;border-radius:0!important;outline:0;background:transparent!important;box-shadow:none!important;padding:0!important;font:400 17px/1.2 ' + M + '!important;color:' + INK + '!important;text-align:right}'
    + '#nlks .nlks__in input[type="date"]{font-size:15px!important}'
    + '#nlks .nlks__in span{align-self:center;font:400 15px/1 ' + M + ';color:' + MUTE + '}'
    + '#nlks .nlks__in:focus-within{outline:2px solid ' + SEA + ';outline-offset:1px}'
    + '#nlks .nlks__help{display:block;margin:6px 0 0;font:400 12px/18px ' + V + '!important;color:' + MUTE + '!important}'
    + '#nlks .nlks__err{display:block;font:500 13px/18px ' + V + '!important;color:' + RED + '!important;margin:4px 0 0}#nlks .nlks__err:empty{display:none}'
    + '#nlks .nlks__seg{display:grid;grid-template-columns:repeat(var(--n,2),minmax(0,1fr));gap:6px}'
    + '#nlks .nlks__seg button,#nlks .nlks__chips button{min-height:44px!important;height:auto!important;margin:0!important;padding:6px 6px!important;border-radius:2px!important;border:1px solid ' + LINE + '!important;background:#fff!important;color:' + INK2 + '!important;font:400 14px/1.3 ' + V + '!important;box-shadow:none!important;cursor:pointer;text-align:center;text-transform:none!important;letter-spacing:0!important;width:auto!important;white-space:normal!important}'
    + '#nlks .nlks__seg button[data-s="d"]{font-family:' + M + '!important;font-size:16px!important}'
    + '#nlks .nlks__seg button[aria-pressed="true"],#nlks .nlks__chips button[aria-pressed="true"]{background:' + SEA + '!important;border-color:' + SEA + '!important;color:#fff!important;font-weight:600!important}'
    + '#nlks button:focus-visible,#nlks a:focus-visible,#nlks summary:focus-visible{outline:2px solid ' + DEEP + '!important;outline-offset:2px}'
    + '#nlks .nlks__out{display:flex;flex-direction:column;gap:10px;min-width:0}'
    + '#nlks .nlks__now{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;border-bottom:1px solid ' + LINE + ';padding-bottom:8px}'
    + '#nlks .nlks__nl{font:500 13px/18px ' + V + '!important;color:' + INK2 + '!important}'
    + '#nlks .nlks__nf{font:500 28px/34px ' + M + '!important;color:' + INK + '!important}'
    + '#nlks .nlks__ns{font:400 12px/18px ' + V + '!important;color:' + MUTE + '!important;flex-basis:100%}'
    + '#nlks .nlks__ol{font:600 14px/20px ' + V + '!important;color:' + INK + '!important}'
    + '#nlks .nlks__cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}'
    + '#nlks .nlks__cards button{display:flex!important;flex-direction:column;align-items:stretch;gap:3px;min-height:44px!important;height:auto!important;margin:0!important;padding:8px 6px 10px!important;border-radius:2px!important;border:1px solid ' + LINE + '!important;background:#fff!important;color:' + INK + '!important;box-shadow:none!important;cursor:pointer;text-align:right!important;text-transform:none!important;letter-spacing:0!important;width:auto!important;white-space:normal!important;font:400 13px/1.3 ' + V + '!important;position:relative}'
    + '#nlks .nlks__cards button[aria-pressed="true"]{border:2px solid ' + SEA + '!important;padding:7px 5px 9px!important;background:' + GROUND + '!important}'
    + '#nlks .nlks__cn{font:600 13px/17px ' + V + ';color:' + INK + '}#nlks .nlks__cs{font:400 11px/15px ' + V + ';color:' + MUTE + '}'
    + '#nlks .nlks__cl{font:400 11px/15px ' + V + ';color:' + MUTE + ';margin-top:4px}'
    + '#nlks .nlks__cf{font:500 18px/22px ' + M + ';color:' + INK + '}@media (min-width:600px){#nlks .nlks__cf{font-size:22px;line-height:28px}#nlks .nlks__cards button{padding:10px 10px 12px!important}#nlks .nlks__cards button[aria-pressed="true"]{padding:9px 9px 11px!important}}'
    + '#nlks .nlks__cd{font:400 12px/16px ' + V + ';color:' + INK2 + ';font-variant-numeric:tabular-nums}#nlks .nlks__cd bdi{font-family:' + M + '}'
    + '#nlks .nlks__ct{font:500 13px/18px ' + M + ';color:' + INK + ';border-top:1px solid ' + LINE + ';padding-top:4px;margin-top:2px}'
    + '#nlks .nlks__tag{align-self:flex-start;font:600 11px/14px ' + V + ';color:' + DEEP + ';border:1px solid ' + DEEP + ';border-radius:2px;padding:1px 4px;margin-bottom:2px}'
    + '#nlks p.nlks__cheap,#nlks p.nlks__pn{margin:0!important;padding:10px 12px!important;background:' + GROUND + ';border-inline-start:3px solid ' + SEA + ';font:500 14px/22px ' + V + '!important;color:' + INK + '!important}'
    + '#nlks p.nlks__msg{margin:0!important;padding:10px 12px!important;background:' + GROUND + ';border-inline-start:3px solid ' + RED + ';font:500 14px/22px ' + V + '!important;color:' + INK + '!important}'
    + '#nlks dl.nlks__dl{margin:0!important;padding:0!important;display:flex;flex-direction:column}'
    + '#nlks dl.nlks__dl>div{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 12px;padding:7px 0;border-bottom:1px solid ' + LINE + '}'
    + '#nlks dl.nlks__dl dt{margin:0!important;font:400 14px/20px ' + V + '!important;color:' + INK + '!important}#nlks dl.nlks__dl dd{margin:0!important;font:500 14px/20px ' + M + '!important;color:' + INK + '!important;white-space:nowrap;text-align:left}#nlks dl.nlks__dl dd.is-t{font-family:' + V + '!important}'
    + '#nlks dl.nlks__dl>div:last-child{border-bottom:2px solid ' + LINE + '}#nlks dl.nlks__dl>div:last-child dt,#nlks dl.nlks__dl>div:last-child dd{font-weight:600!important}'
    + '#nlks p.nlks__how{margin:0!important;font:400 13px/20px ' + V + '!important;color:' + INK2 + '!important}'
    + '#nlks p.nlks__fine{margin:0!important;font:400 12px/18px ' + V + '!important;color:' + MUTE + '!important}'
    /* the timeline: a ruled list with a numbered square on the inline start */
    + '#nlks ol.nlks__tl{list-style:none!important;margin:0!important;padding:0!important;display:flex;flex-direction:column;position:relative;max-width:820px}'
    + '#nlks ol.nlks__tl>li{position:relative;margin:0!important;padding:0 40px 16px 0!important;list-style:none!important;background:none!important}'
    + '#nlks ol.nlks__tl>li::before{content:"";position:absolute;right:13px;top:28px;bottom:0;width:2px;background:' + LINE + '}#nlks ol.nlks__tl>li:last-child::before{display:none}'
    + '#nlks ol.nlks__tl>li::marker{content:none!important}'
    + '#nlks .nlks__no{position:absolute;right:0;top:0;width:28px;height:28px;display:flex;align-items:center;justify-content:center;background:' + DEEP + ';color:#fff;font:500 14px/1 ' + M + ';border-radius:2px}'
    + '#nlks .nlks__when{display:inline-block;font:600 12px/18px ' + V + ';color:' + DEEP + ';border:1px solid ' + LINE + ';border-radius:2px;padding:1px 6px;margin:3px 0 4px;background:' + GROUND + '}'
    + '#nlks .nlks__date{display:inline-block;font:600 12px/18px ' + V + ';font-variant-numeric:tabular-nums;color:#fff;background:' + SEA + ';border-radius:2px;padding:1px 6px;margin:3px 6px 4px 0}'
    + '#nlks h4.nlks__th{margin:0 0 4px!important;padding:0!important;border:0!important;font:600 16px/22px ' + V + '!important;color:' + INK + '!important}#nlks h4.nlks__th::before,#nlks h4.nlks__th::after{display:none!important}'
    + '#nlks .nlks__blk{margin:8px 0 0;padding:8px 12px;border-inline-start:3px solid ' + GREEN + ';background:#fff}'
    + '#nlks .nlks__blk.is-do{border-inline-start-color:' + SEA + '}'
    + '#nlks .nlks__bl{display:block;font:600 12px/18px ' + V + ';color:' + INK2 + ';margin:0 0 2px}'
    + '#nlks .nlks__blk ul,#nlks .nlks__rl,#nlks .nlks__al{margin:0!important;padding:0!important;list-style:none!important}'
    + '#nlks .nlks__blk li,#nlks .nlks__al li{position:relative;margin:0 0 4px!important;padding:0 14px 0 0!important;list-style:none!important;background:none!important;font:400 14px/21px ' + V + '!important;color:' + INK + '!important}'
    + '#nlks .nlks__blk li::before,#nlks .nlks__al li::before{content:"";position:absolute;right:0;top:8px;width:6px;height:6px;background:' + GREEN + '}#nlks .nlks__blk.is-do li::before,#nlks .nlks__al li::before{background:' + SEA + '}'
    + '#nlks .nlks__blk li::marker,#nlks .nlks__al li::marker{content:none!important}'
    + '#nlks p.nlks__note{margin:8px 0 0!important;padding:6px 10px!important;border-inline-start:3px solid ' + RED + ';font:400 13px/20px ' + V + '!important;color:' + INK2 + '!important;background:' + GROUND + '}'
    + '#nlks .nlks__s{display:flex;flex-wrap:wrap;gap:4px 10px;margin:6px 0 0}'
    + '#nlks .nlks__s a{font:400 12px/17px ' + V + '!important;color:' + SEA + '!important;text-decoration:underline!important;text-underline-offset:2px}'
    + '#nlks .nlks__lgrid{display:grid;grid-template-columns:minmax(0,1fr);gap:16px}#nlks .nlks__aside{display:flex;flex-direction:column;gap:12px;min-width:0}'
    + '#nlks ul.nlks__rl{display:grid;grid-template-columns:minmax(0,1fr);gap:0;align-items:start}'
    + '@media (min-width:1100px){#nlks .nlks__lgrid{grid-template-columns:minmax(0,1fr) 340px;gap:28px;align-items:start}#nlks .nlks__aside ul.nlks__tels{grid-template-columns:minmax(0,1fr)!important}#nlks ul.nlks__rl{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}#nlks ul.nlks__rl>li{margin:0!important}}'
    + '#nlks .nlks__box{display:flex;flex-direction:column;gap:6px;padding:12px;background:' + GROUND + ';border-radius:2px}'
    + '#nlks p.nlks__bh{margin:0!important;font:600 15px/22px ' + V + '!important;color:' + DEEP + '!important}'
    + '#nlks ul.nlks__tels{margin:0!important;padding:0!important;list-style:none!important;display:grid;grid-template-columns:minmax(0,1fr);gap:0}@media (min-width:760px){#nlks ul.nlks__tels{grid-template-columns:repeat(2,minmax(0,1fr));gap:0 20px}}'
    + '#nlks .nlks__nums .nlks__s{margin:0}#nlks ul.nlks__tels>li{margin:0!important;padding:6px 0!important;border-bottom:1px solid ' + LINE + ';list-style:none!important;background:none!important;display:flex;flex-direction:column;gap:2px}#nlks ul.nlks__tels>li::before,#nlks ul.nlks__tels>li::marker{content:none!important;display:none!important}'
    + '#nlks .nlks__tb{font:600 14px/20px ' + V + ';color:' + INK + '}#nlks .nlks__tp{font:400 13px/19px ' + V + ';color:' + INK2 + '}'
    + '#nlks .nlks__nums{display:flex;flex-wrap:wrap;align-items:center;gap:0 18px}#nlks a.nlks__tel{display:inline-flex;align-items:center;min-height:44px;align-self:flex-start;gap:8px;font:500 17px/1 ' + M + '!important;color:' + DEEP + '!important;text-decoration:underline!important;text-underline-offset:3px}'
    + '#nlks a.nlks__tel small{font:400 13px/1 ' + V + '!important;color:' + INK2 + '!important;text-decoration:none!important}'
    + '#nlks .nlks__chips{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}@media (min-width:600px){#nlks .nlks__chips{grid-template-columns:repeat(3,minmax(0,1fr))}}@media (min-width:1100px){#nlks .nlks__chips{grid-template-columns:repeat(6,minmax(0,1fr))}}'
    + '#nlks .nlks__rl>li{margin:0 0 10px!important;padding:10px 12px!important;border:1px solid ' + LINE + ';border-inline-start:3px solid ' + GREEN + ';border-radius:2px;list-style:none!important;background:#fff!important}#nlks .nlks__rl>li::before,#nlks .nlks__rl>li::marker{content:none!important;display:none!important}'
    + '#nlks .nlks__rt{display:block;font:600 15px/22px ' + V + ';color:' + INK + ';margin:0 0 4px}'
    + '#nlks .nlks__rx{display:block;font:400 14px/22px ' + V + ';color:' + INK + '}#nlks .nlks__rtip{display:block;margin-top:6px;font:400 13px/20px ' + V + ';color:' + INK2 + '}'
    + '#nlks .nlks__war{display:grid;grid-template-columns:minmax(0,1fr);gap:10px}@media (min-width:860px){#nlks .nlks__war{grid-template-columns:repeat(2,minmax(0,1fr))}}'
    + '#nlks .nlks__wc{padding:12px;border:1px solid ' + LINE + ';border-radius:2px;background:#fff;display:flex;flex-direction:column;gap:6px}'
    + '#nlks .nlks__wh{display:flex;align-items:center;justify-content:space-between;gap:8px}#nlks .nlks__wn{font:600 16px/22px ' + V + ';color:' + INK + '}'
    + '#nlks .nlks__st{font:600 12px/16px ' + V + ';color:' + INK2 + ';border:1px solid ' + INK2 + ';border-radius:2px;padding:2px 6px;white-space:nowrap}#nlks .nlks__st.is-open{color:' + DEEP + ';border-color:' + DEEP + '}'
    + '#nlks .nlks__wd{font:500 13px/20px ' + V + ';color:' + INK2 + ';font-variant-numeric:tabular-nums}#nlks .nlks__wt{font:400 14px/21px ' + V + ';color:' + INK + '}#nlks .nlks__wx{font:400 13px/20px ' + V + ';color:' + MUTE + '}'
    + '#nlks .nlks__end{display:flex;flex-direction:column;gap:10px;border-top:2px solid ' + INK + ';padding-top:14px}'
    + '#nlks p.nlks__bind{margin:0!important;padding:10px 12px!important;border:1px solid ' + DEEP + ';border-radius:2px;font:500 14px/22px ' + V + '!important;color:' + INK + '!important}'
    + '#nlks .nlks__share{display:flex;flex-wrap:wrap;gap:8px}'
    + '#nlks .nlks__share button{min-height:44px!important;margin:0!important;padding:0 16px!important;border-radius:999px!important;border:1px solid ' + LINE + '!important;background:#fff!important;color:' + INK2 + '!important;font:500 14px/1.2 ' + V + '!important;box-shadow:none!important;cursor:pointer;width:auto!important;text-transform:none!important;letter-spacing:0!important}'
    + '#nlks .nlks__share button.is-primary{background:' + SEA + '!important;border-color:' + SEA + '!important;color:#fff!important}'
    + '#nlks details.nlks__src{border:1px solid ' + LINE + ';border-radius:2px}#nlks details.nlks__src>summary{min-height:44px;display:flex;align-items:center;padding:0 12px;cursor:pointer;font:600 14px/20px ' + V + ';color:' + DEEP + ';list-style:none}#nlks details.nlks__src>summary::-webkit-details-marker{display:none}'
    + '#nlks details.nlks__src>summary::after{content:"+";margin-inline-start:auto;font:500 18px/1 ' + M + ';color:' + DEEP + '}#nlks details.nlks__src[open]>summary::after{content:"\\2212"}'
    + '#nlks details.nlks__src ul{margin:0!important;padding:0 12px 10px!important;list-style:none!important}#nlks details.nlks__src li{margin:0!important;padding:5px 0!important;border-top:1px solid ' + LINE + ';list-style:none!important;background:none!important;font:400 13px/20px ' + V + '!important;color:' + INK + '!important}#nlks details.nlks__src li::before,#nlks details.nlks__src li::marker{content:none!important;display:none!important}'
    + '#nlks details.nlks__src a{color:' + SEA + '!important;text-decoration:underline!important;text-underline-offset:2px}#nlks details.nlks__src small{font:400 12px/17px ' + V + '!important;color:' + MUTE + '!important}'
    + '@media print{#nlks .nlks__jump,#nlks .nlks__share{display:none!important}#nlks details.nlks__src>ul{display:block}}';
  function ensureCss() { if (document.getElementById('nlks-css')) return; var s = document.createElement('style'); s.id = 'nlks-css'; s.textContent = CSS; document.head.appendChild(s); }

  function findData(data) {
    var K = null, B = null;
    Object.keys(data || {}).forEach(function (k) { var d = data[k]; if (!d || typeof d !== 'object') return; if (d.key === 'kashe' || (d.timeline && d.rights)) K = d; else if (d.key === 'boim' || (d.rates && d.by_bank)) B = d; });
    return { K: K, B: B };
  }

  NI.register('mkashe', {
    custom: function (root, data) {
      if (NI.langOf && NI.langOf(root) === 'en') return;  // Hebrew only
      var X = findData(data);
      if (!X.K || !X.K.timeline) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
      build(root, X.K, X.B);
    }
  });

  function build(root, K, BOIM) {
    ensureCss();
    var R = K.rules, T = K.texts, br = boimRate(BOIM);
    var v = defaults(BOIM);
    var hm = /#mkashe=([A-Za-z0-9_\-]+)/.exec(location.hash || ''); if (hm) fromCase(decH(hm[1]), v);
    function chip(ref) { var s = srcOf(ref, K); return s ? '<a href="' + esc(s.url) + '" target="_blank" rel="noopener" title="' + esc(s.title) + '">' + esc(s.label + ' · ' + s.date) + '</a>' : ''; }
    function chips(list) { return '<span class="nlks__s">' + (list || []).map(chip).join('') + '</span>'; }
    function fld(key, lab, opt) {
      opt = opt || {}; var id = 'nlks-' + key;
      return '<div class="nlks__f"' + (opt.show ? ' data-v="' + opt.show + '"' : '') + '><label class="nlks__lab" for="' + id + '">' + lab + '</label>'
        + '<div class="nlks__in"><input id="' + id + '" ' + (opt.date ? 'type="date"' : 'inputmode="' + (opt.dec ? 'decimal' : 'numeric') + '" autocomplete="off"') + ' data-k="' + key + '"' + (opt.help ? ' aria-describedby="' + id + '-h"' : '') + '>' + (opt.unit ? '<span>' + opt.unit + '</span>' : '') + '</div>'
        + (opt.help ? '<span class="nlks__help" id="' + id + '-h"' + (opt.dyn ? ' data-help="' + key + '"' : '') + '>' + opt.help + '</span>' : '')
        + '<span class="nlks__err" data-err="' + key + '" aria-live="polite"></span></div>';
    }
    function seg(key, lab, items, cols) {
      var id = 'nlks-' + key + '-l';
      return '<div class="nlks__f"><span class="nlks__lab" id="' + id + '">' + lab + '</span><div class="nlks__seg" style="--n:' + (cols || items.length) + '" role="group" aria-labelledby="' + id + '">'
        + items.map(function (x) { return '<button type="button" data-s="' + key + '" data-val="' + esc(String(x[0])) + '">' + esc(x[1]) + '</button>'; }).join('') + '</div>'
        + '<span class="nlks__err" data-err="' + key + '" aria-live="polite"></span></div>';
    }
    var rateHelp = br ? 'נפתח בממוצע של בנק ישראל במשכנתאות חדשות בריבית קבועה לא צמודה, ' + esc(br.month ? (+br.month.slice(5, 7)) + '.' + br.month.slice(0, 4) : '') + ': ' + esc(pct(br.rate)) + '. הקלידו את הריבית שלכם; בתמהיל, הריבית הממוצעת שלו.'
      : 'הקלידו את הריבית השנתית שלכם; בתמהיל, הריבית הממוצעת שלו.';
    var months = []; for (var mm = K.calc.months_min; mm <= K.calc.months_max; mm++) months.push([mm, String(mm)]);

    var h = '<div class="nlks" id="nlks" dir="rtl" lang="he">'
      + '<p class="nlks__k">מחשבון · כשקשה לשלם</p>'
      + '<h2 class="nlks__h">כשקשה לשלם את המשכנתא: הקפאה, דחייה והזכויות שלכם</h2>'
      + '<p class="nlks__lede">' + rich(T.lede) + '</p>'
      + '<nav class="nlks__jump" aria-label="חלקי הכלי"><button type="button" data-go="nlks-calc">מחשבון הקפאה</button><button type="button" data-go="nlks-late">אם כבר לא שילמתם</button><button type="button" data-go="nlks-rights">הזכויות שלכם</button><button type="button" data-go="nlks-war">מתווי מלחמה</button></nav>'
      /* 1. the calculator */
      + '<section class="nlks__sec" id="nlks-calc" aria-labelledby="nlks-calc-h"><h3 class="nlks__sh" id="nlks-calc-h">מחשבון הקפאת משכנתא</h3>'
      + '<div class="nlks__grid"><div class="nlks__form">'
      + fld('b', 'יתרת המשכנתא היום', { unit: '₪' })
      + fld('n', 'חודשים שנותרו', { help: '25 שנה הן 300 חודשים. בדף החשבון של המשכנתא כתוב כמה תשלומים נשארו.' })
      + seg('m', 'מה אתם יודעים', [['rate', 'את הריבית'], ['pay', 'את ההחזר החודשי']])
      + fld('r', 'ריבית שנתית', { unit: '%', dec: true, show: 'rate', help: rateHelp })
      + fld('p', 'ההחזר החודשי היום', { unit: '₪', show: 'pay', help: ' ', dyn: true })
      + seg('d', 'כמה חודשים לדחות', months, months.length)
      + '</div>'
      + '<div class="nlks__out" aria-live="polite"><p class="nlks__msg" hidden></p><div class="nlks__ok">'
      + '<div class="nlks__now"><span class="nlks__nl">ההחזר היום</span><span class="nlks__nf"></span><span class="nlks__ns"></span></div>'
      + '<span class="nlks__ol"></span>'
      + '<div class="nlks__cards" role="group" aria-label="שלוש דרכים לדחות: לחצו כדי לראות את הפירוט">'
      + K.calc.kinds.map(function (x) { return '<button type="button" data-kind="' + esc(x.k) + '"></button>'; }).join('') + '</div>'
      + '<p class="nlks__cheap"></p><dl class="nlks__dl" aria-label="הפירוט של הדרך שבחרתם"></dl><p class="nlks__how"></p>'
      + '<p class="nlks__fine">' + rich(T.calc_note) + '</p><p class="nlks__fine">' + rich(T.calc_law) + ' ' + chips(['bsl:9ח1']) + '</p>'
      + '</div></div></div></section>'
      /* 2. the timeline */
      + '<section class="nlks__sec" id="nlks-late" aria-labelledby="nlks-late-h"><h3 class="nlks__sh" id="nlks-late-h">אם כבר לא שילמתם: מה קורה ומתי</h3>'
      + '<p class="nlks__p">' + rich(T.timeline_lede) + '</p>'
      + '<div class="nlks__fmiss">' + fld('miss', 'התאריך של התשלום הראשון שלא שולם (לא חובה)', { date: true, help: 'נחשב לכם מתי עוברים ' + R.enforce_months + ' החודשים. התאריך נשאר בדפדפן ולא נכנס לקישור.' }) + '</div>'
      + '<div class="nlks__lgrid"><ol class="nlks__tl"></ol><div class="nlks__aside">'
      + '<div class="nlks__box"><p class="nlks__bh">הקו של המשכנתא בבנק שלכם</p><p class="nlks__p">' + rich(K.lines.lede) + '</p><ul class="nlks__tels">'
      + K.lines.banks.map(function (b) {
        return '<li><span class="nlks__tb">' + esc(b.bank) + '</span><span class="nlks__tp">' + esc(b.purpose) + (b.hours ? ', ' + esc(b.hours) : '') + '</span>'
          + '<span class="nlks__nums"><a class="nlks__tel" href="tel:' + esc(b.tel) + '"><bdi dir="ltr">' + esc(b.tel) + '</bdi>' + (b.ext ? '<small>' + esc(b.ext) + '</small>' : '') + '</a>'
          + (b.alt ? '<a class="nlks__tel" href="tel:' + esc(b.alt) + '"><bdi dir="ltr">' + esc(b.alt) + '</bdi></a>' : '') + chips([b.src]) + '</span></li>';
      }).join('') + '</ul><p class="nlks__fine">' + rich(K.lines.note) + '</p></div>'
      + '<div class="nlks__box"><p class="nlks__bh">עזרה בחינם</p><ul class="nlks__tels">'
      + K.help.map(function (x) {
        return '<li><span class="nlks__tb">' + esc(x.name) + '</span><span class="nlks__tp">' + rich(x.what) + '</span>'
          + (x.tel ? '<a class="nlks__tel" href="tel:' + esc(x.tel) + '"><bdi dir="ltr">' + esc(x.tel) + '</bdi></a>' : '') + chips([x.src]) + '</li>';
      }).join('') + '</ul></div></div></div>'
      + '</section>'
      /* 3. the rights */
      + '<section class="nlks__sec" id="nlks-rights" aria-labelledby="nlks-rights-h"><h3 class="nlks__sh" id="nlks-rights-h">הזכויות שלכם לפי המצב</h3>'
      + '<p class="nlks__p" id="nlks-sel-l">' + rich(T.rights_lede) + '</p>'
      + '<div class="nlks__chips" role="group" aria-labelledby="nlks-sel-l">' + K.rights.situations.map(function (s) { return '<button type="button" data-sel="' + esc(s.k) + '" aria-pressed="false">' + esc(s.he) + '</button>'; }).join('') + '</div>'
      + '<p class="nlks__fine" data-none>עוד לא סימנתם מצב. הזכויות של כל לווה מופיעות כאן למטה.</p>'
      + '<ul class="nlks__rl" aria-live="polite"></ul>'
      + '<div class="nlks__box"><p class="nlks__bh">' + esc(K.rights.all_title) + '</p><ul class="nlks__al">'
      + K.rights.all.map(function (a) { return '<li>' + rich(a.text) + ' ' + chips(a.src) + '</li>'; }).join('') + '</ul></div>'
      + '</section>'
      /* 4. the wartime outlines */
      + '<section class="nlks__sec" id="nlks-war" aria-labelledby="nlks-war-h"><h3 class="nlks__sh" id="nlks-war-h">' + esc(K.programs.title) + '</h3>'
      + '<div class="nlks__war">' + K.programs.items.map(function (p) {
        var st = programStatus(p);
        return '<div class="nlks__wc" data-prog="' + esc(p.k) + '"><div class="nlks__wh"><span class="nlks__wn">' + esc(p.name) + '</span><span class="nlks__st' + (st === 'open' ? ' is-open' : '') + '">' + esc(statusText(p)) + '</span></div>'
          + '<span class="nlks__wd">' + esc(p.dates) + '</span><span class="nlks__wt"><b>למי: </b>' + rich(p.who) + '</span><span class="nlks__wt">' + rich(p.terms) + '</span>'
          + (p.excl ? '<span class="nlks__wx">' + rich(p.excl) + '</span>' : '') + chips(p.src) + '</div>';
      }).join('') + '</div><p class="nlks__pn">' + rich(K.programs.note) + '</p>'
      + '</section>'
      /* 5. the end */
      + '<div class="nlks__end"><p class="nlks__bind">' + rich(T.not_advice) + '</p>'
      + '<div class="nlks__share"><button type="button" class="is-primary" data-act="copy">העתקת הסיכום</button><button type="button" data-act="link">קישור למקרה הזה</button></div>'
      + '<p class="nlks__fine">הסיכום והקישור כוללים רק את מספרי המחשבון ואת הכללים הכלליים, לא את המצב שסימנתם ולא את התאריך.</p>'
      + '<details class="nlks__src"><summary>כל המקורות, עם התאריכים</summary><ul>'
      + Object.keys(K.sources).map(function (id) { var s = srcOf(id, K); return '<li><a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.title) + '</a> <small>' + esc(s.date) + (s.s && K.sources[id].note ? ' · ' + esc(K.sources[id].note) : '') + '</small></li>'; }).join('')
      + '</ul></details><p class="nlks__fine">נבדק ב־' + esc(dmy(K.checked)) + '.</p></div>'
      + '</div>';
    root.innerHTML = h;
    var q = function (s) { return root.querySelector(s); }, qa = function (s) { return [].slice.call(root.querySelectorAll(s)); };

    // fill the inputs
    function show(k) { var inp = q('#nlks-' + k); if (!inp) return; var x = v[k]; inp.value = x === '' || x == null ? '' : (k === 'b' || k === 'p') && isFinite(+x) ? nf(+x) : String(x); }
    ['b', 'n', 'r', 'p', 'miss'].forEach(show);
    qa('input[data-k]').forEach(function (inp) {
      var k = inp.getAttribute('data-k');
      inp.addEventListener('input', function () { v[k] = inp.value; if (k === 'miss') paintSteps(); else later(); });
      if (k === 'b' || k === 'p') inp.addEventListener('blur', function () { var x = money(v[k]); if (isFinite(x) && x > 0) { v[k] = x; show(k); } });
      if (inp.type === 'date') inp.addEventListener('change', function () { v[k] = inp.value; paintSteps(); });
    });
    var t = 0, last = null;
    function later() { clearTimeout(t); t = setTimeout(paint, 90); }
    root.addEventListener('click', function (e) {
      var b = e.target && e.target.closest ? e.target.closest('button') : null; if (!b || !root.contains(b)) return;
      if (b.hasAttribute('data-go')) { var target = q('#' + b.getAttribute('data-go')); if (target && target.scrollIntoView) target.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
      if (b.hasAttribute('data-s')) {
        var k = b.getAttribute('data-s'), val = b.getAttribute('data-val');
        if (k === 'm' && val !== v.m) {  // switching keeps the same loan: the payment of the rate, or the rate of the payment
          if (val === 'pay' && last && !last.error) { v.p = Math.round(last.P0); show('p'); }
          if (val === 'rate' && last && !last.error) { v.r = Math.round(last.r * 100) / 100; show('r'); }
        }
        v[k] = k === 'd' ? +val : val; paint(); return;
      }
      if (b.hasAttribute('data-kind')) { v.k = b.getAttribute('data-kind'); paint(); return; }
      if (b.hasAttribute('data-sel')) { var s = b.getAttribute('data-sel'), i = v.sel.indexOf(s); if (i > -1) v.sel.splice(i, 1); else v.sel.push(s); paintRights(); return; }
      var act = b.getAttribute('data-act');
      if (act === 'copy' || act === 'link') {
        var url = (location.origin && location.origin !== 'null' ? location.origin + location.pathname : location.href.split('#')[0]) + '#mkashe=' + enc(caseOf(v));
        var tx = act === 'copy' ? copyText(last, K) + '\n' + url : url, lab = b.textContent;
        var done = function () { b.textContent = 'הועתק'; setTimeout(function () { b.textContent = lab; }, 1600); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(tx).then(done, function () { G.prompt('העתיקו', tx); }); else G.prompt('העתיקו', tx);
      }
    });

    function paint() {
      qa('[data-s]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-val') === String(v[x.getAttribute('data-s')]))); });
      qa('[data-v]').forEach(function (x) { x.hidden = x.getAttribute('data-v') !== v.m; });
      qa('[data-err]').forEach(function (x) { x.textContent = ''; });
      var r;
      try { r = compute(v, K); } catch (e2) { r = err(null, 'לא הצלחנו לחשב עם הערכים האלה.'); }
      var msg = q('.nlks__msg'), ok = q('.nlks__ok');
      if (r.error) {
        var fe = r.error.field && q('[data-err="' + r.error.field + '"]'); if (fe) fe.textContent = r.error.msg;
        msg.textContent = r.error.msg; msg.hidden = false; ok.hidden = true; last = null; return;
      }
      msg.hidden = true; ok.hidden = false; last = r;
      var ph = q('[data-help="p"]'); if (ph) ph.textContent = r.derived ? 'הריבית שיוצאת מהיתרה, מהתקופה ומההחזר: ' + pct(r.r) + ' בשנה.' : '';
      q('.nlks__nf').innerHTML = '<bdi>' + esc(ils(r.P0)) + '</bdi>';
      q('.nlks__ns').textContent = 'יתרה ' + ils(r.B) + ', ' + nf(r.n) + ' חודשים, ריבית ' + pct(r.r) + (r.derived ? ' (לפי ההחזר שהקלדתם)' : '') + '. סך התשלומים עד הסוף בלי דחייה: ' + ils(r.base) + '.';
      q('.nlks__ol').textContent = 'אם דוחים ' + r.d + (r.d === 1 ? ' חודש' : ' חודשים') + ', בשלוש דרכים:';
      qa('[data-kind]').forEach(function (bt) {
        var k = bt.getAttribute('data-kind'), x = r.by[k], meta = K.calc.kinds.filter(function (y) { return y.k === k; })[0];
        bt.setAttribute('aria-pressed', String(v.k === k));
        bt.innerHTML = (r.cheapest ? '<span class="nlks__tag"' + (r.cheapest === k ? '' : ' aria-hidden="true" style="visibility:hidden"') + '>הזולה בסך הכול</span>' : '')
          + '<span class="nlks__cn">' + esc(meta.he) + '</span><span class="nlks__cs">' + esc(meta.sub) + '</span>'
          + '<span class="nlks__cl">ההחזר אחר כך</span><span class="nlks__cf"><bdi>' + esc(ils(x.after)) + '</bdi></span>'
          + '<span class="nlks__cd"><bdi dir="ltr">' + (x.delta >= 0 ? '+' : '-') + esc(nf(Math.abs(x.delta))) + '</bdi> ₪ בחודש</span>'
          + '<span class="nlks__cl">תוספת עד הסוף</span><span class="nlks__ct"><bdi>' + esc(ils(x.extra)) + '</bdi></span>';
      });
      q('.nlks__cheap').innerHTML = rich(cheapText(r, K));
      q('.nlks__dl').innerHTML = lines(r, v.k, K).map(function (l) { return '<div><dt>' + esc(l[0]) + '</dt><dd' + (/[א-ת]{2}/.test(l[1]) ? ' class="is-t"' : '') + '><bdi>' + esc(l[1]) + '</bdi></dd></div>'; }).join('');
      var km = K.calc.kinds.filter(function (y) { return y.k === v.k; })[0];
      q('.nlks__how').innerHTML = '<b>' + esc(km.he) + ':</b> ' + rich(km.how);
    }
    function paintSteps() {
      var S = steps(K, v.miss);
      q('.nlks__tl').innerHTML = S.map(function (s, i) {
        return '<li data-step="' + esc(s.k) + '"><span class="nlks__no" aria-hidden="true">' + (i + 1) + '</span>'
          + '<span class="nlks__when">' + esc(s.when) + '</span>' + (s.date ? '<span class="nlks__date">' + (s.k === 'six' ? 'מ־' : '') + esc(dmy(s.date)) + '</span>' : '')
          + '<h4 class="nlks__th">' + esc(s.title) + '</h4><p class="nlks__p">' + rich(s.what) + '</p>'
          + (s.protect && s.protect.length ? '<div class="nlks__blk"><span class="nlks__bl">מה מגן עליכם</span><ul>' + s.protect.map(function (x) { return '<li>' + rich(x) + '</li>'; }).join('') + '</ul></div>' : '')
          + (s.note ? '<p class="nlks__note">' + rich(s.note) + '</p>' : '')
          + (s.do && s.do.length ? '<div class="nlks__blk is-do"><span class="nlks__bl">מה אפשר לעשות</span><ul>' + s.do.map(function (x) { return '<li>' + rich(x) + '</li>'; }).join('') + '</ul></div>' : '')
          + chips(s.src) + '</li>';
      }).join('');
    }
    function paintRights() {
      qa('[data-sel]').forEach(function (x) { x.setAttribute('aria-pressed', String(v.sel.indexOf(x.getAttribute('data-sel')) > -1)); });
      var L = rightsFor(v.sel, K);
      q('[data-none]').hidden = v.sel.length > 0;
      q('.nlks__rl').innerHTML = L.map(function (it) {
        return '<li data-right="' + esc(it.k) + '"><span class="nlks__rt">' + esc(it.title) + '</span><span class="nlks__rx">' + rich(it.text) + '</span>'
          + (it.tip ? '<span class="nlks__rtip">' + rich(it.tip) + '</span>' : '') + chips(it.src) + '</li>';
      }).join('');
    }
    paint(); paintSteps(); paintRights();
  }
})();
