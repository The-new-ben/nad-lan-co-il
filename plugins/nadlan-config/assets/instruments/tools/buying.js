/* NadLan Instruments · buying v1 (HAD-683, Ben 7.11.2026): the four tools of the /buying-apartment/ hub, one file ('file' => 'buying').
   - bplan   (T1+T2) "קניית דירה צעד אחר צעד לפי המצב שלך": 12 buyer statuses, the type of flat and the stage give the rules that
             apply (purchase tax brackets from ptax.json, the Bank of Israel LTV from nrm.json, eligibility-loan items from zakaut.json,
             each with its source and date) and a step plan; every step links its owner page; progress stays in this browser only.
   - bequity (T3+T4) the equity sources and what each adds to the monthly payment (rates: Bank of Israel averages, boi-mortgage.json;
             a loan with no published average gets no number until the reader types the rate of the offer), then the handover
             stress test of a developer offer with little paid now (construction input index, cbs-200010.json).
   - bladder (T20) equity + status (+ income, optional) give the maximum price by the LTV rule, and the cities and room counts
             where the median deal fits (prices-hub.json).
   - boffer  (T14) the asking price against the median deals of the city and rooms, the share of neighbourhoods with a lower
             median (value.json), the district index, and an opening range with its basis. No invented "typical discount".
   Pure logic in window.NLBH (no DOM): tools/instruments/test_buying_hub.js. Design: NadLan Instruments (prices-common.js styles). */
(function () {
  'use strict';
  var W = typeof window !== 'undefined' ? window : this;
  var B = W.NLBH = {};
  function get(o, p) { return String(p).split('.').reduce(function (a, k) { return a == null ? null : a[k]; }, o); }
  function n0(x) { var s = Math.round(+x || 0), neg = s < 0; return (neg ? '-' : '') + String(Math.abs(s)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function pc(x, d) { return String(+(x * 100).toFixed(d == null ? 2 : d)); }
  function date(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : p.length === 2 ? (+p[1]) + '.' + p[0] : String(iso || ''); }
  function ef2nom(e) { return 1200 * (Math.pow(1 + e / 100, 1 / 12) - 1); }
  function pmt(L, e, years) { var r = ef2nom(e) / 1200, n = Math.round(years * 12); return !(L > 0) || n <= 0 ? 0 : r === 0 ? L / n : L * r / (1 - Math.pow(1 + r, -n)); }
  function pv(pay, e, years) { var r = ef2nom(e) / 1200, n = Math.round(years * 12); return r === 0 ? pay * n : pay * (1 - Math.pow(1 + r, -n)) / r; }
  B.get = get; B.n0 = n0; B.pc = pc; B.date = date; B.ef2nom = ef2nom; B.pmt = pmt; B.pv = pv;

  /* the data map of a tool: the files by key, the CBS construction index found by its id, and a few derived percents */
  B.model = function (data) {
    var M = {};
    Object.keys(data).forEach(function (k) { var d = data[k]; if (!/^d\d+$/.test(k)) M[k] = d; if (d && d.id === 200010) M.cbsb = d; });
    if (M.orechdin && M.orechdin.cap) { M.orechdin.cap.pctx = pc(M.orechdin.cap.pct); M.orechdin.cgt_advance.afterx = pc(M.orechdin.cgt_advance.after_paid); M.orechdin.cgt_advance.ratex = pc(M.orechdin.cgt_advance.rate); }
    return M;
  };
  B.fill = function (s, M) { return String(s).replace(/\{([a-z0-9_.]+)\}/gi, function (m, p) { var v = get(M, p); return v == null ? m : typeof v === 'number' ? (v % 1 === 0 ? n0(v) : String(v)) : String(v); }); };
  B.status = function (BU, id) { for (var i = 0; i < BU.statuses.length; i++) if (BU.statuses[i].id === id) return BU.statuses[i]; return BU.statuses[0]; };
  B.has = function (s, f) { return (s.flags || []).indexOf(f) >= 0; };

  /* purchase tax by the brackets of ptax.json; dis: the disabled-buyer rate on a single home up to the cap (as tools/ptax.js) */
  B.tax = function (price, track, PT, dis) {
    var br = PT.tracks[track] || PT.tracks.single;
    if (dis && track === 'single' && PT.disabled && price <= PT.disabled.single_cap) return Math.max(0, price - PT.tracks.single[0][0]) * PT.disabled.rate;
    var t = 0, lo = 0;
    for (var i = 0; i < br.length; i++) { var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(price, hi); if (top > lo) t += (top - lo) * br[i][1]; if (price <= hi) break; lo = hi; }
    return t;
  };
  B.brackets = function (track, PT) {
    var o = [], lo = 0;
    PT.tracks[track].forEach(function (b) { o.push(b[0] == null ? pc(b[1]) + '% מעל ' + n0(lo) + ' ₪' : pc(b[1]) + '% עד ' + n0(b[0]) + ' ₪'); lo = b[0]; });
    return o.slice(0, -1).join(', ') + ' ו־' + o[o.length - 1];
  };
  B.ltv = function (s, NRM) { return NRM.ltv_by_status[s.ltv]; };
  /* the Bank of Israel average rate of new mortgages, fixed not linked (the most conservative published track), with its month */
  B.rate = function (BM) { var r = BM.rates.fixed_nl, h = r.hist || []; return { rate: r.rate, label: r.label, month: h.length ? h[h.length - 1][0] : BM.market.month, src: BM.sources[0] }; };

  /* the rules that apply to a status, each with its source and date */
  B.rules = function (s, M) {
    var PT = M.ptax, NRM = M.nrm, Z = M.zakaut, o = [];
    var pts = { label: PT.source, url: PT.url, date: PT.checked };
    var zs = function (k) { var x = Z.sources[k]; return { label: 'משרד הבינוי והשיכון: ' + x.title, url: x.url, date: x.updated || x.published }; };
    if (s.ptax === 'single') o.push({ k: 'ptax', t: 'מס רכישה על דירה יחידה: ' + B.brackets('single', PT) + '. המדרגות קפואות עד ' + date(PT.frozen_until) + '.', src: pts });
    if (s.ptax === 'extra') o.push({ k: 'ptax', t: 'מס רכישה על דירה נוספת: ' + B.brackets('extra', PT) + ', לרכישה עד ' + date(PT.valid.extra) + ' (הוראת שעה שהוארכה).', src: { label: PT.extension.label, url: PT.extension.url, date: PT.checked } });
    if (s.ptax === 'foreign') o.push({ k: 'ptax', t: 'מס רכישה לתושבי חוץ: ' + B.brackets('foreign', PT) + ', לרכישה עד ' + date(PT.valid.foreign) + '.', src: { label: PT.extension.label, url: PT.extension.url, date: PT.checked } });
    if (s.ptax === 'oleh') o.push({ k: 'ptax', t: 'מס רכישה לעולים: ' + B.brackets('oleh', PT) + ', על דירה שנקנתה מ־' + PT.oleh_window.before_months + ' חודשים לפני העלייה ועד ' + (PT.oleh_window.after_months / 12) + ' שנים אחריה.', src: { label: PT.oleh_window.label, url: PT.instruction.url, date: PT.checked } });
    if (B.has(s, 'ptax_disabled')) o.push({ k: 'ptax_dis', t: 'נכות: בדירה יחידה עד ' + n0(PT.disabled.single_cap) + ' ₪, מס של ' + pc(PT.disabled.rate) + '% על החלק שמעל ' + n0(PT.tracks.single[0][0]) + ' ₪, במקום המדרגות הרגילות.', src: pts });
    if (B.has(s, 'upgrader')) o.push({ k: 'upgrader', t: 'דירה חלופית: משלמים לפי המדרגות של דירה יחידה, אם מוכרים את הדירה הקיימת בתוך ' + PT.upgrader[0].months + ' חודשים.', src: { label: PT.guide.label, url: PT.guide.url, date: PT.checked } });
    var l = B.ltv(s, NRM), ls = { label: NRM.ltv_source.label_he, url: NRM.ltv_source.url, date: NRM.checked };
    if (s.ltv === 'foreign') o.push({ k: 'ltv', t: 'מימון: הבנק מממן עד ' + pc(l) + '% מהשווי, כי דירה שקונה תושב חוץ נחשבת דירה להשקעה.', src: { label: NRM.ltv_qa.label_he, url: NRM.ltv_source.url, date: NRM.checked } });
    else o.push({ k: 'ltv', t: 'מימון: הבנק מממן עד ' + pc(l) + '% מהשווי' + (s.ltv === 'cit_sell' ? ' בדירה חלופית' : s.ltv === 'cit_own' ? ' בדירה להשקעה' : '') + '. השאר, ועוד המס והעלויות, מכספכם.', src: ls });
    if (B.has(s, 'invest')) o.push({ k: 'invest', t: 'אם זו תהיה הדירה היחידה שלכם, גם כשמשכירים אותה, חלים הכללים של דירה יחידה.', src: ls });
    if (B.has(s, 'zakaut')) { var r = Z.bands.rows; o.push({ k: 'zakaut', t: 'הלוואת זכאות של משרד הבינוי והשיכון: בטבלת המשפחות הוותיקות, מ־' + n0(r[0][2]) + ' ₪ (' + n0(r[0][0]) + ' עד ' + n0(r[0][1]) + ' נקודות) ועד ' + n0(r[r.length - 1][2]) + ' ₪ (' + n0(r[r.length - 1][0]) + ' נקודות ומעלה). את הסכום שלכם קובעת תעודת הזכאות.', src: zs(Z.bands.src) }); }
    if (B.has(s, 'marriage')) { var m = Z.vet_family.marriage.by; o.push({ k: 'marriage', t: 'זוג צעיר: הניקוד עולה עם שנות הנישואין: ' + m[0] + ' נקודות לזוג רשום לנישואין או בשנה הראשונה, ' + m[1] + ' אחרי שנה מלאה, ' + m[2] + ' אחרי שנתיים, ועוד ' + Z.vet_family.marriage.step + ' לכל שנה.', src: zs(Z.vet_family.src) }); }
    if (B.has(s, 'service')) o.push({ k: 'service', t: 'שירות חובה או שירות לאומי: תוספת של ' + Z.service.pct_per_month + '% מהמשכנתא הבסיסית לכל חודש שירות מלא, עד ' + Z.service.cap_months + ' חודשים (שירות לאומי עד ' + Z.service.civic_cap_months + ').', src: zs(Z.service.src) });
    if (B.has(s, 'reserve')) o.push({ k: 'reserve', t: 'מילואים: ' + Z.reserve.years + ' שנים לפחות, עם ' + Z.reserve.days_per_year + ' ימים בכל אחת: ' + Z.reserve.pct + '% מהמשכנתא הבסיסית לכל ' + Z.reserve.per_days + ' ימי מילואים, לפחות ' + Z.reserve.min_pct + '% ועד ' + Z.reserve.max_pct_person + '% לאדם.', src: zs(Z.reserve.src) });
    if (B.has(s, 'career')) o.push({ k: 'career', t: 'אנשי קבע: לא מצאנו אצל משרד הבינוי טבלה נפרדת לאנשי קבע, ולכן אין כאן מספר. הזכאות נבנית מאותו ניקוד ומחודשי שירות החובה; הטבות לפי חוזה השירות בודקים מול צה״ל.', src: null });
    if (B.has(s, 'olim')) o.push({ k: 'olim', t: 'עולים: מסלול סיוע לעולים לפי הוותק בארץ, או מסלול המשפחות הוותיקות, לפי הבחירה.', src: zs(Z.olim_family.src) });
    if (B.has(s, 'disability')) o.push({ k: 'disability', t: 'נכות: תוספת נקודות בהלוואת הזכאות; למשל ' + n0(Z.disability.vet_family_75) + ' נקודות למשפחה ותיקה עם נכות של 75%.', src: zs(Z.disability.src) });
    return o;
  };
  /* the steps for a status and a type of flat, numbers filled from the data files */
  B.steps = function (BU, s, ty, M) {
    return BU.steps.filter(function (x) {
      if (x.only && x.only.indexOf(s.id) < 0) return false;
      if (x.flag && !B.has(s, x.flag)) return false;
      if (x.type && ty !== 'any' && x.type !== ty) return false;
      return true;
    }).map(function (x) { return { id: x.id, st: x.st, t: B.fill(x.t, M), d: B.fill(x.d, M), href: (x.alt && x.alt[s.id]) || x.href, a: x.a, who: x.who }; });
  };
  B.next = function (steps, done, stage) { for (var i = 0; i < steps.length; i++) if (steps[i].st >= stage && !done[steps[i].id]) return steps[i]; for (i = 0; i < steps.length; i++) if (!done[steps[i].id]) return steps[i]; return null; };

  /* what the buyer pays from own money at price P: the part the bank does not finance, the purchase tax and the lawyer (low end) */
  B.need = function (P, o) {
    var loan = Math.min(o.ltv * P, o.loanCap == null ? Infinity : o.loanCap), tax = B.tax(P, o.track, o.PT, o.dis), law = P * o.lawyerPct / 100 * (1 + o.vat);
    return { P: P, loan: loan, down: P - loan, tax: tax, law: law, cash: P - loan + tax + law };
  };
  B.loanCap = function (income, share, rate, years) { return income > 0 && share > 0 ? pv(income * share, rate, years) : Infinity; };
  B.maxPrice = function (E, o) {
    var lo = 0, hi = 1e8;
    for (var i = 0; i < 80; i++) { var mid = (lo + hi) / 2; if (B.need(mid, o).cash <= E) lo = mid; else hi = mid; }
    var r = B.need(Math.floor(lo / 1000) * 1000, o); r.capped = o.loanCap != null && isFinite(o.loanCap) && r.loan < o.ltv * r.P - 1; return r;
  };
  B.lastQ = function (arr, Q) { for (var i = (arr || []).length - 1; i >= 0; i--) if (arr[i] != null) return { v: arr[i], q: Q[i], i: i }; return null; };
  B.ladder = function (PH, maxP) {
    return PH.city.map(function (c) {
      var o = { n: c.n, slug: c.slug, code: c.code };
      [3, 4, 5].forEach(function (r) { var x = B.lastQ(c['r' + r], PH.q); o['r' + r] = x; o['f' + r] = !!(x && x.v <= maxP); });
      return o;
    }).sort(function (a, b) { return ((a.r4 && a.r4.v) || 9e9) - ((b.r4 && b.r4.v) || 9e9); });
  };

  /* the equity sources: what is needed, what is there, and what each loan adds every month (only with a rate) */
  B.sources = function (o) {
    var need = o.price * (1 - o.ltv) + o.tax + o.law, have = 0, loanPay = 0, loanInt = 0, rows = [];
    o.items.forEach(function (it) {
      var a = Math.max(0, +it.amt || 0), r = { id: it.id, amt: a, pay: null, interest: null, missing: false }; have += a;
      if (it.kind === 'loan' && a > 0) { if (it.rate > 0 && it.years > 0) { r.pay = pmt(a, it.rate, it.years); r.interest = r.pay * Math.round(it.years * 12) - a; loanPay += r.pay; loanInt += r.interest; } else r.missing = true; }
      rows.push(r);
    });
    var mort = Math.min(o.price * o.ltv, Math.max(0, o.price + o.tax + o.law - have)), mpay = pmt(mort, o.rate, o.years);
    return { need: need, have: have, gap: need - have, mort: mort, mpay: mpay, mint: mpay * Math.round(o.years * 12) - mort, loanPay: loanPay, loanInt: loanInt, total: mpay + loanPay, rows: rows };
  };
  /* the construction input index over the last 12 published months */
  B.cbsYoY = function (C) { var ks = Object.keys(C.months).sort(), a = ks[ks.length - 1], y = (+a.slice(0, 4) - 1) + a.slice(4), v = C.months[a], w = C.months[y]; return w ? { g: v / w - 1, to: a, from: y, v: v, w: w } : null; };
  /* the handover of a developer offer with little paid now: the linked balance, the mortgage the LTV allows, the cash still due */
  B.stress = function (o) {
    var paid = o.price * o.paidPct, def = o.price - paid, add = def * o.share * (Math.pow(1 + o.g, o.months / 12) - 1), due = def + add, linked = o.price + add;
    var value = linked * o.appr, loan = Math.min(o.ltv * value, due), cash = Math.max(0, due - loan);
    return { paid: paid, def: def, add: add, due: due, linked: linked, value: value, loan: loan, cash: cash, own: paid + cash,
      rows: [0, 1, 2].map(function (k) { var r = o.rate + k; return { k: k, rate: r, pay: pmt(loan, r, o.years) }; }) };
  };
  /* the offer helper */
  B.offer = function (PH, V, o) {
    var c = null, i; for (i = 0; i < PH.city.length; i++) if (PH.city[i].code === o.code) c = PH.city[i];
    var arr = c ? c['r' + o.rooms] : PH.il['r' + o.rooms], L = B.lastQ(arr, PH.q); if (!L) return null;
    var four = []; for (i = L.i; i >= 0 && four.length < 4; i--) if (arr[i] != null) four.push({ v: arr[i], q: PH.q[i] });
    var low = four.reduce(function (a, b) { return b.v < a.v ? b : a; }, four[0]);
    var yoy = L.i >= 4 && arr[L.i - 4] != null ? L.v / arr[L.i - 4] - 1 : null;
    var vc = null; if (c && V && V.cities) Object.keys(V.cities).forEach(function (n) { if (V.cities[n].code === o.code) vc = V.cities[n]; });
    var hoods = vc ? (vc.hoods || []).filter(function (h) { return h['r' + o.rooms]; }).map(function (h) { return { id: h.id, n: h.n, v: h['r' + o.rooms][0], q: h['r' + o.rooms][1] }; }) : [];
    var lower = hoods.filter(function (h) { return h.v < o.ask; }).length, hood = null;
    hoods.forEach(function (h) { if (String(h.id) === String(o.hood)) hood = h; });
    var basis = hood ? hood.v : L.v, dip = low.v / L.v, lo = basis * dip, hi = Math.min(o.ask, basis);
    var dist = null;
    if (c && PH.dist) PH.dist.forEach(function (d) { if (d.id === String(c.cbs)) { var n = d.v.length - 1; if (n >= 12 && d.v[n] != null && d.v[n - 12] != null) dist = { n: d.n, yoy: d.v[n] / d.v[n - 12] - 1 }; } });
    return { city: c ? c.n : 'כל הארץ', slug: c ? c.slug : null, rooms: o.rooms, ask: o.ask, med: L.v, q: L.q, yoy: yoy, four: four, low: low, dip: dip,
      hoods: hoods, lower: lower, hood: hood, basis: basis, vs: o.ask / basis - 1, lo: lo, hi: hi, range: o.ask > lo + 1, dist: dist };
  };

  if (!W.NadLanInstruments || typeof document === 'undefined' || !W.NLPH || !W.NLPH.ui) return;
  /* ------------------------------------------------------------------ the surfaces ------------------------------------------------------------------ */
  var NI = W.NadLanInstruments, P = W.NLPH, U = P.ui, esc = U.esc, KEY = 'nlbh-plan-v1';
  function load() { try { var s = W.localStorage.getItem(KEY); return (s && JSON.parse(s)) || {}; } catch (e) { return {}; } }
  function save(o) { try { W.localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} }
  function shareStatus(id) { var o = load(); o.s = id; save(o); try { document.dispatchEvent(new CustomEvent('nlbh:status', { detail: id })); } catch (e) {} }
  function big(n) { return n >= 1e6 ? U.mil(n) : U.ils(n); }
  function src1(s) { return s ? (s.url ? '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.label) + '</a>' : esc(s.label)) + (s.date ? ', ' + esc(date(s.date)) : '') : 'אין מקור רשמי מתוארך, ולכן אין מספר'; }
  function css() {
    if (document.getElementById('nlbh-css')) return;
    var s = document.createElement('style'); s.id = 'nlbh-css';
    s.textContent = [
      '.nlbh .nlbh-q{margin:14px 0 0;position:relative}.nlbh p.nlbh-ql{font:600 13px/18px var(--nli-sans);color:var(--nli-ink);letter-spacing:.03em;margin:0 0 8px;position:relative}',
      '.nlbh-st{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}@media (max-width:760px){.nlbh-st{grid-template-columns:repeat(2,minmax(0,1fr))}}',
      'html body .nli .nlbh .nlbh-st button{display:grid;gap:2px;text-align:right;min-height:58px;padding:9px 11px;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);color:var(--nli-ink);cursor:pointer;margin:0;box-shadow:none;text-transform:none;letter-spacing:0;font:inherit}',
      '.nlbh-st b{font:600 15px/20px var(--nli-sans)}.nlbh-st small{font:400 12px/16px var(--nli-sans);color:var(--nli-mute)}',
      'html body .nli .nlbh .nlbh-st button[aria-pressed="true"]{background:var(--nli-ink);border-color:var(--nli-ink);color:#fff}.nlbh-st button[aria-pressed="true"] small{color:#C9D6DD}',
      '.nlbh-row{display:flex;flex-wrap:wrap;gap:12px 22px;margin:12px 0 0;position:relative}',
      '.nlbh-rules{margin:16px 0 0;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--ph-paper);position:relative}',
      '.nlbh-rules p.h{margin:0;padding:9px 12px;font:600 13px/18px var(--nli-sans);color:var(--nli-ink);border-bottom:1px solid var(--nli-line)}',
      '.nlbh-rules ul{list-style:none;margin:0;padding:0}.nlbh-rules li{margin:0;padding:9px 12px;border-bottom:1px solid var(--nli-line);font:400 14.5px/23px var(--nli-sans);color:var(--nli-ink)}.nlbh-rules li:last-child{border-bottom:0}',
      '.nlbh-rules li small{display:block;font:400 12px/17px var(--nli-sans);color:var(--nli-mute);margin-top:2px}html body .nli .nlbh-rules li small a{color:var(--nli-sea) !important;text-decoration:underline}',
      '.nlbh-bar{height:6px;background:var(--nli-line);border-radius:1px;overflow:hidden;margin:6px 0 0}.nlbh-bar i{display:block;height:100%;background:var(--nli-sea)}',
      '.nlbh-stages{list-style:none;margin:14px 0 0;padding:0;border-top:2px solid var(--nli-ink);position:relative}',
      '.nlbh-stages>li{margin:0;border-bottom:1px solid var(--nli-line)}.nlbh-stages summary{display:flex;justify-content:space-between;gap:10px;align-items:center;min-height:48px;padding:8px 2px;cursor:pointer;list-style:none;font:600 16px/22px var(--nli-sans);color:var(--nli-ink)}',
      '.nlbh-stages summary::-webkit-details-marker{display:none}.nlbh-stages summary span{font:500 12.5px/1 var(--nli-mono);color:var(--nli-mute);white-space:nowrap}.nlbh-stages li.is-now summary{color:var(--nli-sea-deep)}',
      '.nlbh-stages summary::before{content:"+";font:500 16px/1 var(--nli-mono);color:var(--nli-mute);margin-inline-end:8px}.nlbh-stages details[open] summary::before{content:"−"}.nlbh-stages summary b{flex:1;font-weight:600}',
      '.nlbh-step{display:grid;grid-template-columns:40px minmax(0,1fr);gap:10px;padding:10px 0;border-top:1px dashed var(--nli-line)}',
      'html body .nli .nlbh .nlbh-chk{width:36px;height:36px;border:1.5px solid var(--nli-ink2);border-radius:var(--nli-r-s);background:#fff;cursor:pointer;padding:0;margin:0;display:grid;place-items:center;box-shadow:none}',
      '.nlbh-chk svg{width:18px;height:18px;stroke:#fff;fill:none;stroke-width:2.4;opacity:0}html body .nli .nlbh .nlbh-chk[aria-pressed="true"]{background:var(--nli-sea);border-color:var(--nli-sea)}.nlbh-chk[aria-pressed="true"] svg{opacity:1}',
      '.nlbh-step b{display:block;font:600 15.5px/22px var(--nli-sans);color:var(--nli-ink)}.nlbh-step.is-done b{color:var(--nli-mute);text-decoration:line-through;text-decoration-thickness:1px}',
      '.nlbh-step p{margin:2px 0 4px !important;font:400 14px/22px var(--nli-sans);color:var(--nli-ink2)}.nlbh-step small{font:400 12px/16px var(--nli-sans);color:var(--nli-mute);margin-inline-start:10px}',
      'html body .nli .nlbh a.nlbh-go{font:500 14px/20px var(--nli-sans);color:var(--nli-sea) !important;text-decoration:underline;text-underline-offset:3px}',
      '.nlbh-next{margin:16px 0 0;padding:12px 14px;background:var(--nli-ink);color:#fff;border-radius:var(--nli-r-s);position:relative}.nlbh-next span{display:block;font:500 12px/16px var(--nli-sans);color:#C9D6DD;letter-spacing:.03em}',
      '.nlbh-next b{display:block;font:600 17px/25px var(--nli-sans);margin:2px 0}html body .nli .nlbh .nlbh-next a{color:#fff !important;text-decoration:underline;font:500 14px/20px var(--nli-sans)}',
      '.nlbh-acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}html body .nli .nlbh .nlbh-acts button{min-height:40px;padding:8px 14px;border:1px solid var(--nli-line);border-radius:999px;background:#fff;color:var(--nli-ink2);font:500 14px/20px var(--nli-sans);cursor:pointer;margin:0;box-shadow:none}',
      '.nlbh-form{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px 16px;margin:12px 0 0;position:relative}@media (max-width:760px){.nlbh-form{grid-template-columns:1fr 1fr}}@media (max-width:420px){.nlbh-form{grid-template-columns:1fr}}',
      'html body .nli .nlbh .nli__in input{font:500 16px/1.2 var(--nli-mono);border:0 !important;background:none !important;box-shadow:none !important;padding:10px 12px;width:100%;min-width:0;margin:0;height:auto;color:var(--nli-ink);direction:ltr;text-align:right}',
      '.nlbh .nli__in select{border:0;background:none;padding:10px 12px;width:100%;font:500 15px/1.2 var(--nli-sans);color:var(--nli-ink)}',
      '.nlbh-u{display:flex;align-items:center;padding:0 10px;font:500 13px/1 var(--nli-sans);color:var(--nli-mute);border-inline-start:1px solid var(--nli-line);white-space:nowrap}',
      '.nlbh-src{display:grid;gap:0;margin:12px 0 0;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:#fff}',
      '.nlbh-src>div{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr) minmax(0,.8fr) minmax(0,.7fr);gap:8px 12px;align-items:center;padding:10px 12px;border-bottom:1px solid var(--nli-line)}.nlbh-src>div:last-child{border-bottom:0}',
      '.nlbh-src>div>span{font:500 14px/20px var(--nli-sans);color:var(--nli-ink)}.nlbh-src>div>span small{display:block;font:400 12px/17px var(--nli-sans);color:var(--nli-mute)}',
      'html body .nli .nlbh .nlbh-src>div,html body .nli .nlbh .nlbh-form{display:grid !important}',
      '@media (max-width:640px){html body .nli .nlbh .nlbh-src>div{grid-template-columns:repeat(3,minmax(0,1fr));padding:8px 10px}.nlbh-src>div>span{grid-column:1/-1}.nlbh-src>div.is-cash .nli__f{grid-column:1/-1}.nlbh-src .nli__f>label{font-size:11.5px;color:var(--nli-mute)}.nlbh-src .nli__in{min-height:42px}html body .nli .nlbh .nlbh-src .nli__in input{padding:8px 6px;font-size:15px}.nlbh-src .nlbh-u{padding:0 6px}}',
      '.nlbh-risk{margin:10px 0 0;padding:0 18px 0 0;font:400 13.5px/21px var(--nli-sans);color:var(--nli-ink2)}.nlbh-risk li{margin:0 0 4px}.nlbh-risk b{color:var(--nli-ink);font-weight:600}',
      'html body .nli .nlph h3.nlbh-h3{font:700 30px/32px var(--nli-display) !important;color:var(--nli-ink) !important;margin:30px 0 6px !important;padding-top:12px;border-top:2px solid var(--nli-ink);letter-spacing:0}',
      'html body .nli .nlph table.nlph-t td.fit{background:var(--ph-tint) !important;color:var(--nli-sea-deep);font-weight:600}html body .nli .nlph table.nlph-t td.no{color:var(--nli-mute)}',
      'html body .nli .nlph table.nlph-t th a{color:var(--nli-ink) !important;text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--nli-line)}',
      '.nlbh-basis{margin:12px 0 0;padding:0 18px 0 0;font:400 14.5px/23px var(--nli-sans);color:var(--nli-ink)}.nlbh-basis li{margin:0 0 6px}',
      '@media print{.nlbh .nlbh-acts,.nlbh .nlbh-st button[aria-pressed="false"],.nlbh .nlph-tabs{display:none !important}.nlbh-stages details{display:block}.nlbh-stages details>*{display:block !important}}'
    ].join('');
    document.head.appendChild(s);
  }
  function panel(root, kicker, fallback) {
    U.css(); css();
    var t0 = root.querySelector('.nli__title'), title = t0 ? t0.textContent : fallback;
    if (!root.closest('.nli')) root.classList.add('nli');
    root.setAttribute('dir', 'rtl'); root.innerHTML = '';
    var p = U.el('div', 'nli__panel nlph nlbh'); root.appendChild(p);
    p.appendChild(U.el('p', 'nli__kicker', esc(kicker))); p.appendChild(U.el('h2', 'nli__title', esc(title)));
    return p;
  }
  function tabs(label, opts, cur, on, sea) {
    var g = U.el('div', 'nlph-tabs' + (sea ? ' is-sea' : '')); g.setAttribute('role', 'group'); g.setAttribute('aria-label', label);
    g.appendChild(U.el('span', 'lab', esc(label)));
    opts.forEach(function (o) { var b = U.el('button', '', esc(o[1])); b.type = 'button'; b.setAttribute('aria-pressed', String(String(o[0]) === String(cur))); b.setAttribute('data-v', o[0]);
      b.addEventListener('click', function () { [].forEach.call(g.querySelectorAll('button'), function (z) { z.setAttribute('aria-pressed', String(z === b)); }); on(o[0]); }); g.appendChild(b); });
    return g;
  }
  function field(label, unit, val, on, money) {
    var f = U.el('div', 'nli__f'), id = 'nlbh-' + Math.random().toString(36).slice(2, 8), l = U.el('label', '', esc(label)); l.htmlFor = id; f.appendChild(l);
    var ib = U.el('div', 'nli__in'), i = document.createElement('input'); i.id = id; i.type = 'text'; i.inputMode = 'decimal'; i.autocomplete = 'off';
    var show = function (n) { return n == null || n === '' ? '' : money ? U.num(n) : String(n); }; i.value = show(val);
    var rd = function () { var n = parseFloat(String(i.value).replace(/[^\d.]/g, '')); return isFinite(n) ? n : null; };
    i.addEventListener('input', function () { on(rd()); }); i.addEventListener('blur', function () { var n = rd(); if (n != null) i.value = show(n); });
    ib.appendChild(i); ib.appendChild(U.el('span', 'nlbh-u', esc(unit))); f.appendChild(ib); f.set = function (n) { i.value = show(n); }; return f;
  }
  function select(label, opts, cur, on) {
    var f = U.el('div', 'nli__f'), id = 'nlbh-' + Math.random().toString(36).slice(2, 8), l = U.el('label', '', esc(label)); l.htmlFor = id; f.appendChild(l);
    var ib = U.el('div', 'nli__in'), s = document.createElement('select'); s.id = id;
    f.fill = function (list, c) { s.innerHTML = ''; list.forEach(function (o) { var op = U.el('option', '', esc(o[1])); op.value = o[0]; if (String(o[0]) === String(c)) op.selected = true; s.appendChild(op); }); };
    f.fill(opts, cur); s.addEventListener('change', function () { on(s.value); }); ib.appendChild(s); f.appendChild(ib); f.sel = s; return f;
  }
  function statusSelect(BU, cur, on) {
    var f = select('המצב שלכם', BU.statuses.map(function (s) { return [s.id, s.label]; }), cur, function (v) { on(v); shareStatus(v); });
    document.addEventListener('nlbh:status', function (e) { if (f.sel.value !== e.detail) { f.sel.value = e.detail; on(e.detail); } });
    return f;
  }
  function kpis(list) { return '<div class="nlph-kpis">' + list.map(function (k) { return '<div><span>' + esc(k[0]) + '</span><strong' + (k[3] ? ' class="' + k[3] + '"' : '') + '>' + esc(k[1]) + '</strong><small>' + esc(k[2] || '') + '</small></div>'; }).join('') + '</div>'; }
  function pre(root) { try { return JSON.parse(root.getAttribute('data-nli-set') || '{}'); } catch (e) { return {}; } }

  /* ---------------- bplan ---------------- */
  NI.register('bplan', { custom: function (root, D0) {
    var M = B.model(D0), BU = M.buying, p = panel(root, 'התוכנית שלי לקניית דירה', 'קניית דירה צעד אחר צעד לפי המצב שלך');
    p.appendChild(U.el('p', 'nlph-sub', 'בוחרים מי אתם, איזו דירה ובאיזה שלב. מקבלים את הכללים שחלים עליכם, כל אחד עם המקור והתאריך שלו, ואת הצעדים הבאים, כל צעד עם המדריך שלו. ההתקדמות נשמרת רק בדפדפן הזה.'));
    var S = load(), st = { s: S.s || 'first', ty: S.ty || 'any', sg: S.sg != null ? +S.sg : 0, done: S.done || {} }, ps = pre(root); if (ps.kind) st.s = ps.kind;
    var persist = function () { var o = load(); o.s = st.s; o.ty = st.ty; o.sg = st.sg; o.done = st.done; save(o); };
    var q1 = U.el('div', 'nlbh-q'); q1.appendChild(U.el('p', 'nlbh-ql', '1. מי אתם')); var grid = U.el('div', 'nlbh-st'); grid.setAttribute('role', 'group'); grid.setAttribute('aria-label', 'מי אתם'); q1.appendChild(grid); p.appendChild(q1);
    BU.statuses.forEach(function (s) { var b = U.el('button', '', '<b>' + esc(s.label) + '</b><small>' + esc(s.sub) + '</small>'); b.type = 'button'; b.setAttribute('data-v', s.id); b.setAttribute('aria-pressed', String(s.id === st.s));
      b.addEventListener('click', function () { st.s = s.id; [].forEach.call(grid.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); persist(); draw(); shareStatus(s.id); }); grid.appendChild(b); });
    document.addEventListener('nlbh:status', function (e) { if (e.detail !== st.s) { st.s = e.detail; [].forEach.call(grid.children, function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-v') === st.s)); }); draw(); } });
    var q2 = U.el('div', 'nlbh-q'); q2.appendChild(U.el('p', 'nlbh-ql', '2. איזו דירה ובאיזה שלב')); var row = U.el('div', 'nlbh-row'); q2.appendChild(row); p.appendChild(q2);
    row.appendChild(tabs('דירה', BU.types.map(function (t) { return [t.id, t.label]; }), st.ty, function (v) { st.ty = v; persist(); draw(); }));
    row.appendChild(tabs('השלב', BU.stages.map(function (g) { return [g.id, g.label]; }), st.sg, function (v) { st.sg = +v; persist(); draw(); }, true));
    var out = U.el('div', ''); out.setAttribute('aria-live', 'polite'); p.appendChild(out);
    var last = '';
    function draw() {
      var s = B.status(BU, st.s), rules = B.rules(s, M), steps = B.steps(BU, s, st.ty, M), nx = B.next(steps, st.done, st.sg);
      var done = steps.filter(function (x) { return st.done[x.id]; }).length;
      var h = '<div class="nlbh-next"><span>הצעד הבא שלכם</span>' + (nx ? '<b>' + esc(nx.t) + '</b><a href="' + esc(nx.href) + '"' + (/^https?:/.test(nx.href) ? ' target="_blank" rel="noopener"' : '') + '>' + esc(nx.a) + ' ←</a>' : '<b>סימנתם את כל הצעדים. בהצלחה בדירה החדשה.</b>') + '</div>';
      h += '<div class="nlbh-rules"><p class="h">הכללים שחלים על ' + esc(s.label) + '</p><ul>' + rules.map(function (r) { return '<li>' + esc(r.t) + '<small>מקור: ' + src1(r.src) + '</small></li>'; }).join('') + '</ul></div>';
      h += '<p class="nlph-sub" style="margin:16px 0 0">' + esc(done + ' מתוך ' + steps.length + ' צעדים סומנו') + '</p><div class="nlbh-bar" aria-hidden="true"><i style="width:' + Math.round(100 * done / Math.max(1, steps.length)) + '%"></i></div>';
      h += '<ol class="nlbh-stages">' + BU.stages.map(function (g) {
        var list = steps.filter(function (x) { return x.st === g.id; }); if (!list.length) return '';
        var dn = list.filter(function (x) { return st.done[x.id]; }).length;
        return '<li class="' + (g.id === st.sg ? 'is-now' : '') + '"><details' + (g.id === st.sg || g.id === st.sg + 1 ? ' open' : '') + '><summary><b>' + esc(g.t) + '</b><span>' + dn + '/' + list.length + '</span></summary>' +
          list.map(function (x) { var on = !!st.done[x.id];
            return '<div class="nlbh-step' + (on ? ' is-done' : '') + '"><button type="button" class="nlbh-chk" data-id="' + esc(x.id) + '" aria-pressed="' + on + '" aria-label="' + esc((on ? 'בוטל סימון: ' : 'סימון כבוצע: ') + x.t) + '"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10.5l4 4 8-9"/></svg></button><div><b>' + esc(x.t) + '</b><p>' + esc(x.d) + '</p><a class="nlbh-go" href="' + esc(x.href) + '"' + (/^https?:/.test(x.href) ? ' target="_blank" rel="noopener"' : '') + '>' + esc(x.a) + ' ←</a><small>' + esc(x.who) + '</small></div></div>'; }).join('') + '</details></li>';
      }).join('') + '</ol>';
      out.innerHTML = h;
      [].forEach.call(out.querySelectorAll('.nlbh-chk'), function (b) { b.addEventListener('click', function () { var id = b.getAttribute('data-id'); if (st.done[id]) delete st.done[id]; else st.done[id] = 1; persist(); var y = b.getBoundingClientRect().top; draw(); var nb = out.querySelector('.nlbh-chk[data-id="' + id + '"]'); if (nb) { nb.focus({ preventScroll: true }); var d = nb.getBoundingClientRect().top - y; if (Math.abs(d) > 1) W.scrollBy(0, d); } }); });
      last = 'התוכנית שלי לקניית דירה (' + s.label + ', ' + B.status({ statuses: BU.types }, st.ty).label + '): ' + done + ' מתוך ' + steps.length + ' צעדים. הצעד הבא: ' + (nx ? nx.t : 'אין') + '.';
    }
    draw();
    var acts = U.el('div', 'nlbh-acts'); var pr = U.el('button', '', 'הדפסת התוכנית'); pr.type = 'button'; pr.addEventListener('click', function () { [].forEach.call(out.querySelectorAll('details'), function (d) { d.open = true; }); W.print(); });
    var rs = U.el('button', '', 'ניקוי הסימונים'); rs.type = 'button'; rs.addEventListener('click', function () { st.done = {}; persist(); draw(); });
    acts.appendChild(pr); acts.appendChild(rs); p.appendChild(acts);
    p.appendChild(U.el('p', 'nlph-fine', esc('התוכנית היא רשימת צעדים, לא ייעוץ משפטי, מיסויי או פיננסי. הכללים מתעדכנים מהקבצים הרשמיים: רשות המסים (נבדק ' + date(M.ptax.checked) + '), בנק ישראל (נבדק ' + date(M.nrm.checked) + ') ומשרד הבינוי והשיכון (נבדק ' + date(M.zakaut.checked) + '). הסימונים נשמרים בדפדפן הזה בלבד, ואינם נשלחים אלינו.')));
    p.appendChild(U.share(function () { return last; }));
  } });

  /* ---------------- bequity ---------------- */
  var SRC = [
    { id: 'own', label: 'חסכונות שלכם', kind: 'cash', risk: 'הכסף הזול ביותר. משאירים בצד מרווח לתיקונים ולחודשים קשים, ולא מכניסים לעסקה את השקל האחרון.' },
    { id: 'gift', label: 'מתנה מההורים או מהמשפחה', kind: 'cash', risk: 'מתנה לא מחזירים. כותבים שזו מתנה ולמי מבני הזוג, כדי שלא תיחשב הלוואה בפרידה או מול האחים.' },
    { id: 'partner', label: 'שותף או שותפים לדירה', kind: 'cash', risk: 'שותף נרשם בטאבו ובמשכנתא. מסכמים בכתב מה קורה במכירה, בפרידה או אם אחד לא משלם.' },
    { id: 'lien', label: 'משכנתא על הדירה של ההורים', kind: 'loan', boi: true, years: 20, risk: 'הדירה של ההורים משועבדת לבנק עד סוף ההלוואה. אם ההחזר לא משולם, הבנק פונה לנכס שלהם.' },
    { id: 'fund', label: 'הלוואה כנגד קרן השתלמות או קופת גמל', kind: 'loan', years: 5, risk: 'החיסכון ממשיך לעבוד, אבל ההחזר החודשי נספר בחישוב ההכנסה הפנויה בבנק.' },
    { id: 'loan', label: 'הלוואה מבנק או מגוף חוץ בנקאי', kind: 'loan', years: 5, risk: 'הלוואה קצרה מעלה את ההחזר בחודשים הצפופים ביותר, והבנק למשכנתאות מוריד אותה מההכנסה הפנויה.' }
  ];
  NI.register('bequity', { custom: function (root, D0) {
    var M = B.model(D0), BU = M.buying, R = B.rate(M.boim), CB = B.cbsYoY(M.cbsb), il4 = B.lastQ(M.phub.il.r4, M.phub.q);
    var p = panel(root, 'מחשבון · מקורות ההון העצמי', 'קניית דירה ללא הון עצמי: מאיפה מגיע הכסף ומה הוא עולה');
    p.appendChild(U.el('p', 'nlph-sub', esc('בלי הון עצמי אין משכנתא: הבנק מממן חלק מהמחיר, והשאר, ועוד מס הרכישה ועורך הדין, מגיע מכם. כאן רואים כמה צריך, מאיפה אפשר להביא אותו ומה כל מקור מוסיף להחזר החודשי. הריבית על המשכנתא: הממוצע של בנק ישראל ב' + date(R.month) + '.')));
    var st = { price: il4.v, s: load().s || 'first', years: 25, income: null, items: {} };
    SRC.forEach(function (x) { st.items[x.id] = { amt: x.id === 'own' ? 250000 : x.id === 'gift' ? 150000 : 0, rate: x.boi ? R.rate : null, years: x.years || 0 }; });
    var f = U.el('div', 'nlbh-form'); p.appendChild(f);
    f.appendChild(field('מחיר הדירה', '₪', st.price, function (v) { st.price = v || 0; draw(); }, true));
    f.appendChild(statusSelect(BU, st.s, function (v) { st.s = v; draw(); }));
    f.appendChild(field('הכנסה נטו של משק הבית (לא חובה)', '₪ בחודש', null, function (v) { st.income = v; draw(); }, true));
    p.appendChild(tabs('תקופת המשכנתא', [[20, '20 שנה'], [25, '25 שנה'], [30, '30 שנה']], st.years, function (v) { st.years = +v; draw(); }));
    var box = U.el('div', 'nlbh-src'); p.appendChild(box);
    SRC.forEach(function (x) {
      var r = U.el('div', x.kind === 'cash' ? 'is-cash' : ''); r.appendChild(U.el('span', '', esc(x.label) + (x.kind === 'loan' ? '<small>' + (x.boi ? esc('הריבית: הממוצע של בנק ישראל, ' + R.label + ', ' + date(R.month)) : 'הקלידו את הריבית מההצעה שקיבלתם') + '</small>' : '')));
      r.appendChild(field('סכום', '₪', st.items[x.id].amt || null, function (v) { st.items[x.id].amt = v || 0; draw(); }, true));
      if (x.kind === 'loan') { r.appendChild(field('ריבית שנתית', '%', st.items[x.id].rate, function (v) { st.items[x.id].rate = v; draw(); })); r.appendChild(field('שנים', 'שנים', st.items[x.id].years, function (v) { st.items[x.id].years = v || 0; draw(); })); }
      box.appendChild(r);
    });
    var out = U.el('div', ''); out.setAttribute('aria-live', 'polite'); p.appendChild(out);
    var risk = U.el('ul', 'nlbh-risk'); risk.innerHTML = SRC.map(function (x) { return '<li><b>' + esc(x.label) + ':</b> ' + esc(x.risk) + '</li>'; }).join(''); p.appendChild(U.el('p', 'nlbh-ql', 'מה חשוב לדעת על כל מקור')); p.appendChild(risk);
    var txt = '';
    function draw() {
      var s = B.status(BU, st.s), l = B.ltv(s, M.nrm), tax = B.tax(st.price, s.ptax, M.ptax, B.has(s, 'ptax_disabled')), law = st.price * M.cost.lawyer.from / 100 * (1 + M.cost.vat);
      var r = B.sources({ price: st.price, ltv: l, tax: tax, law: law, rate: R.rate, years: st.years, items: SRC.map(function (x) { var it = st.items[x.id]; return { id: x.id, kind: x.kind, amt: it.amt, rate: it.rate, years: it.years }; }) });
      var gap = r.gap > 0 ? 'חסרים ' + U.ils(r.gap) : 'יש לכם ' + U.ils(-r.gap) + ' מעבר לנדרש';
      var h = '<div class="nlph-ans"><div class="nlph-ans__head"><span>כמה הון עצמי צריך</span><small>' + esc(s.label + ' · מימון עד ' + pc(l) + '%') + '</small></div><p class="nlph-ans__a"><b>' + esc('לדירה ב־' + U.ils(st.price) + ' צריך ' + U.ils(r.need) + ' מכספכם') + '</b>' + esc(': ' + U.ils(st.price * (1 - l)) + ' שהבנק לא מממן (' + pc(1 - l) + '%), ' + (tax < 1 ? 'בלי מס רכישה' : 'מס רכישה ' + U.ils(tax)) + ' ועורך דין מ־' + U.ils(law) + ' (' + M.cost.lawyer.from + '% ועוד מע״מ). ' + gap + '.') + '</p>' +
        kpis([['צריך מכספכם', big(r.need), 'לפני שמאי, תיווך ומעבר'], ['יש לכם', big(r.have), 'כל המקורות יחד'], [r.gap > 0 ? 'חסר' : 'נשאר', big(Math.abs(r.gap)), r.gap > 0 ? 'עוד מקור, או דירה זולה יותר' : 'מרווח ביטחון', r.gap > 0 ? 'is-dn' : 'is-up'], ['החזר חודשי כולל', U.ils(r.total), 'משכנתא והלוואות']]) + '</div>';
      h += '<div class="nlph-tw" style="margin-top:12px"><table class="nlph-t"><caption>' + esc('מה כל מקור מוסיף כל חודש. משכנתא: ' + R.label + ', ' + R.rate + '% (ממוצע בנק ישראל, ' + date(R.month) + '), ' + st.years + ' שנה') + '</caption><thead><tr><th scope="col">מקור</th><th scope="col" class="n">סכום</th><th scope="col" class="n">החזר חודשי</th><th scope="col" class="n nlph-dk">ריבית לאורך ההלוואה</th></tr></thead><tbody>' +
        '<tr class="is-nat"><th scope="row">' + esc('משכנתא (' + pc(r.mort / Math.max(1, st.price), 0) + '% מהמחיר)') + '</th><td class="n">' + U.ils(r.mort) + '</td><td class="n">' + U.ils(r.mpay) + '</td><td class="n nlph-dk">' + U.ils(r.mint) + '</td></tr>' +
        r.rows.filter(function (x) { return x.amt > 0; }).map(function (x) { var d = SRC.filter(function (y) { return y.id === x.id; })[0];
          return '<tr><th scope="row">' + esc(d.label) + '</th><td class="n">' + U.ils(x.amt) + '</td><td class="n">' + (x.pay != null ? U.ils(x.pay) : x.missing ? '<span class="nlph-na">הקלידו ריבית</span>' : '·') + '</td><td class="n nlph-dk">' + (x.interest != null ? U.ils(x.interest) : '·') + '</td></tr>'; }).join('') + '</tbody></table></div>';
      if (st.income > 0) { var sh = r.total / st.income, mk = M.boim.market;
        h += '<p class="nlph-sub" style="margin-top:10px"><b>' + esc('ההחזר הכולל הוא ' + pc(sh, 1) + '% מההכנסה.') + '</b> ' + esc('בממוצע, ההחזר במשכנתאות החדשות היה ' + mk.pti_avg + '% מההכנסה (בנק ישראל, ' + date(mk.month) + '). לפי הוראה 329 ההחזר על המשכנתא עד ' + pc(M.nrm.rules.pti_max, 0) + '% מההכנסה הפנויה, ומעל ' + pc(M.nrm.rules.pti_risk, 0) + '% הבנק מחזיק יותר הון כנגד ההלוואה; הכנסה פנויה היא נטו פחות התחייבויות קבועות של יותר מ־18 חודשים.') + '</p>'; }
      out.innerHTML = h;
      txt = 'דירה ב־' + U.ils(st.price) + ' (' + s.label + '): צריך ' + U.ils(r.need) + ' מכספכם, יש ' + U.ils(r.have) + '. החזר חודשי כולל ' + U.ils(r.total) + '.';
      drawS();
    }
    /* T4: the handover stress test */
    p.appendChild(U.el('h3', 'nlbh-h3', 'מבצע של קבלן בלי הון עצמי: מה קורה ביום המסירה'));
    p.appendChild(U.el('p', 'nlph-sub', esc('במבצעים כמו 10/90 משלמים מעט עכשיו, והיתרה, צמודה למדד תשומות הבנייה, ביום המסירה. אז מגיעה המשכנתא, והיא מממנת רק עד שיעור המימון של המצב שלכם. כאן רואים כמה כסף צריך באותו יום, ומה קורה אם הריבית עולה או אם השמאי של הבנק מעריך את הדירה נמוך מהמחיר.')));
    var ss = { paid: 0.1, months: 30, share: 0.5, g: CB ? CB.g : 0, appr: 1 };
    var sf = U.el('div', 'nlbh-form'); p.appendChild(sf);
    sf.appendChild(field('חודשים עד המסירה', 'חודשים', ss.months, function (v) { ss.months = v || 0; drawS(); }));
    sf.appendChild(field('עליית מדד תשומות הבנייה בשנה', '%', +(100 * ss.g).toFixed(2), function (v) { ss.g = (v || 0) / 100; drawS(); }));
    var srow = U.el('div', 'nlbh-row'); p.appendChild(srow);
    srow.appendChild(tabs('משלמים עכשיו', [[0.02, '2%'], [0.1, '10%'], [0.2, '20%']], ss.paid, function (v) { ss.paid = +v; drawS(); }));
    srow.appendChild(tabs('החלק הצמוד מכל תשלום', [[0.5, 'מחצית'], [0.25, 'רבע'], [1, 'הכול (חוזה ישן)']], ss.share, function (v) { ss.share = +v; drawS(); }, true));
    srow.appendChild(tabs('שמאות הבנק', [[1, 'כמו המחיר'], [0.95, 'נמוכה ב־5%'], [0.9, 'נמוכה ב־10%']], ss.appr, function (v) { ss.appr = +v; drawS(); }));
    var sout = U.el('div', ''); sout.setAttribute('aria-live', 'polite'); p.appendChild(sout);
    function drawS() {
      var s = B.status(BU, st.s), l = B.ltv(s, M.nrm), x = B.stress({ price: st.price, paidPct: ss.paid, months: ss.months, share: ss.share, g: ss.g, ltv: l, rate: R.rate, years: st.years, appr: ss.appr });
      sout.innerHTML = '<div class="nlph-ans" style="margin-top:12px"><div class="nlph-ans__head"><span>ביום המסירה</span><small>' + esc('אחרי ' + ss.months + ' חודשים · מימון עד ' + pc(l) + '%') + '</small></div><p class="nlph-ans__a"><b>' + esc('ביום המסירה צריך ' + U.ils(x.cash) + ' מכספכם') + '</b>' + esc(', מעבר ל־' + U.ils(x.paid) + ' ששילמתם בחתימה. היתרה לקבלן אז ' + U.ils(x.due) + ', מתוכה ' + U.ils(x.add) + ' הצמדה, והמשכנתא מממנת ' + U.ils(x.loan) + ' (' + pc(l) + '% מ־' + U.ils(x.value) + ').') + '</p>' +
        kpis([['משלמים בחתימה', big(x.paid), pc(ss.paid, 0) + '% מהמחיר'], ['הצמדה עד המסירה', big(x.add), 'לפי ' + pc(ss.g, 1) + '% בשנה'], ['מכספכם ביום המסירה', big(x.cash), 'אחרי המשכנתא', 'is-dn'], ['סך הכול מכספכם', big(x.own), 'בלי מס ועורך דין']]) + '</div>' +
        '<div class="nlph-tw" style="margin-top:12px"><table class="nlph-t"><caption>' + esc('ההחזר החודשי על המשכנתא ביום המסירה, ' + st.years + ' שנה') + '</caption><thead><tr><th scope="col">הריבית ביום המסירה</th><th scope="col" class="n">ריבית</th><th scope="col" class="n">החזר חודשי</th></tr></thead><tbody>' +
        x.rows.map(function (r) { return '<tr' + (r.k ? '' : ' class="is-nat"') + '><th scope="row">' + esc(r.k === 0 ? 'כמו היום (ממוצע בנק ישראל)' : 'גבוהה ב־' + (r.k === 1 ? 'נקודה' : '2 נקודות')) + '</th><td class="n">' + r.rate.toFixed(2) + '%</td><td class="n">' + U.ils(r.pay) + '</td></tr>'; }).join('') + '</tbody></table></div>';
    }
    draw();
    p.appendChild(U.el('p', 'nlph-fine', esc('איך מחשבים: ההון העצמי הנדרש הוא החלק שהבנק לא מממן לפי הוראה 329, ועוד מס רכישה לפי המדרגות ועורך דין בקצה הנמוך של הטווח. ההחזר החודשי בשיטת שפיצר, אחרי המרת הריבית האפקטיבית של בנק ישראל לריבית חודשית. בהלוואה בלי ממוצע מפורסם אין מספר עד שמקלידים את הריבית של ההצעה. במבחן המסירה: היתרה צמודה בחלק שבחרתם (בחוזה מ־7.7.2022 עד מחצית מכל תשלום, סעיף 5ג לחוק המכר), המדד עולה בקצב שבחרתם, והמשכנתא היא שיעור המימון מהשווי. ' + (CB ? 'ברירת המחדל של המדד: ' + pc(CB.g, 1) + '%, השינוי בפועל מ־' + date(CB.from) + ' עד ' + date(CB.to) + '. ' : '') + 'עליית ריבית ושמאות נמוכה הם תרחישים, לא תחזית.')));
    var src = U.el('p', 'nli__src'); src.innerHTML = U.srcs([R.src, { label: M.nrm.ltv_source.label_he, url: M.nrm.ltv_source.url }, { label: M.ptax.source, url: M.ptax.url }, { label: (M.cbsb && M.cbsb.source) || 'הלמ״ס, מדד תשומות הבנייה', url: 'https://www.cbs.gov.il/' }]); p.appendChild(src);
    p.appendChild(U.share(function () { return txt; }));
  } });

  function cities(n) { return n === 1 ? 'עיר אחת' : n + ' ערים'; }
  /* ---------------- bladder ---------------- */
  NI.register('bladder', { custom: function (root, D0) {
    var M = B.model(D0), BU = M.buying, R = B.rate(M.boim), PH = M.phub;
    var p = panel(root, 'סולם הון עצמי · ערים וחדרים', 'איך לקנות דירה בארץ עם 100 אלף, 300 אלף או 500 אלף ש״ח');
    p.appendChild(U.el('p', 'nlph-sub', esc('מקלידים כמה כסף יש לכם, ובוחרים את המצב שלכם. מקבלים את המחיר המרבי שהכסף הזה מאפשר לפי כללי המימון של בנק ישראל, אחרי מס רכישה ועורך דין, ואת הערים ומספרי החדרים שבהם המחיר החציוני של העסקאות נכנס בתקציב.')));
    var ps = pre(root), st = { e: ps.price || 300000, s: load().s || 'first', income: null, share: 0.3, years: 25 };
    var f = U.el('div', 'nlbh-form'); p.appendChild(f);
    var ef = field('ההון העצמי שלכם', '₪', st.e, function (v) { st.e = v || 0; mark(); draw(); }, true); f.appendChild(ef);
    f.appendChild(statusSelect(BU, st.s, function (v) { st.s = v; draw(); }));
    f.appendChild(field('הכנסה נטו של משק הבית (לא חובה)', '₪ בחודש', null, function (v) { st.income = v; draw(); }, true));
    var r1 = U.el('div', 'nlbh-row'); p.appendChild(r1);
    var et = tabs('דוגמאות', [[100000, '100 אלף'], [300000, '300 אלף'], [500000, '500 אלף'], [1000000, 'מיליון']], st.e, function (v) { st.e = +v; ef.set(st.e); draw(); }); r1.appendChild(et);
    function mark() { [].forEach.call(et.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-v') === st.e)); }); }
    r1.appendChild(tabs('החזר מההכנסה', [[0.3, '30%'], [0.4, '40%'], [0.5, '50%']], st.share, function (v) { st.share = +v; draw(); }, true));
    r1.appendChild(tabs('תקופה', [[25, '25 שנה'], [30, '30 שנה']], st.years, function (v) { st.years = +v; draw(); }));
    var out = U.el('div', ''); out.setAttribute('aria-live', 'polite'); p.appendChild(out);
    var txt = '';
    function draw() {
      var s = B.status(BU, st.s), l = B.ltv(s, M.nrm), cap = B.loanCap(st.income, st.share, R.rate, st.years);
      var x = B.maxPrice(st.e, { ltv: l, track: s.ptax, PT: M.ptax, dis: B.has(s, 'ptax_disabled'), lawyerPct: M.cost.lawyer.from, vat: M.cost.vat, loanCap: cap });
      var L = B.ladder(PH, x.P), n3 = L.filter(function (c) { return c.f3; }).length, n4 = L.filter(function (c) { return c.f4; }).length, n5 = L.filter(function (c) { return c.f5; }).length;
      var il = [3, 4, 5].map(function (r) { return B.lastQ(PH.il['r' + r], PH.q); });
      var h = '<div class="nlph-ans"><div class="nlph-ans__head"><span>איפה אפשר לקנות</span><small>' + esc(s.label + ' · מימון עד ' + pc(l) + '%') + '</small></div><p class="nlph-ans__a"><b>' + esc('עם ' + U.ils(st.e) + ' אפשר לקנות דירה עד כ־' + U.ils(x.P)) + '</b>' +
        esc(x.capped ? ', כי ההחזר מוגבל ל־' + pc(st.share, 0) + '% מההכנסה: המשכנתא נעצרת ב־' + U.ils(x.loan) + '.' : ', עם משכנתא של ' + U.ils(x.loan) + ' (' + pc(l) + '%), ' + (x.tax < 1 ? 'בלי מס רכישה' : 'מס רכישה ' + U.ils(x.tax)) + ' ועורך דין מ־' + U.ils(x.law) + '.') +
        esc(n3 + n4 + n5 ? ' המחיר החציוני נכנס בתקציב ב' + [n3 && cities(n3) + ' בדירת 3 חדרים', n4 && cities(n4) + ' בדירת 4', n5 && cities(n5) + ' בדירת 5'].filter(Boolean).join(', ') + ', מתוך ' + L.length + '.' : ' המחיר החציוני של אף אחת מ־' + L.length + ' הערים עוד לא נכנס בתקציב הזה; הטבלה מראה כמה חסר בכל עיר.') + '</p>' +
        kpis([['מחיר מרבי', big(x.P), 'אחרי מס ועורך דין'], ['משכנתא', big(x.loan), x.capped ? 'לפי ההכנסה' : 'לפי שיעור המימון'], ['החזר חודשי', U.ils(B.pmt(x.loan, R.rate, st.years)), R.rate + '%, ' + st.years + ' שנה'], ['מס רכישה', x.tax < 1 ? 'פטור' : U.ils(x.tax), x.tax < 1 ? 'מתחת למדרגה הראשונה' : s.label]]) + '</div>';
      h += '<div class="nlph-tw" style="margin-top:12px"><table class="nlph-t"><caption>' + esc('המחיר החציוני של דירות שנמכרו, באלפי ₪, ברבעון האחרון שפורסם לכל עיר. מסומן: נכנס בתקציב של ' + U.ils(x.P) + '. רשות המסים דרך אתר הנדל״ן הממשלתי') + '</caption><thead><tr><th scope="col">עיר</th><th scope="col" class="n">3 חדרים</th><th scope="col" class="n">4 חדרים</th><th scope="col" class="n">5 חדרים</th></tr></thead><tbody>' +
        '<tr class="is-nat"><th scope="row">כל הארץ</th>' + il.map(function (q) { return '<td class="n ' + (q && q.v <= x.P ? 'fit' : 'no') + '">' + (q ? U.k(q.v) : '·') + '</td>'; }).join('') + '</tr>' +
        L.map(function (c) { return '<tr><th scope="row">' + (c.slug ? '<a href="/' + esc(c.slug) + '-apartment-prices/">' + esc(c.n) + '</a>' : esc(c.n)) + '</th>' + [3, 4, 5].map(function (r) { var q = c['r' + r]; return '<td class="n ' + (c['f' + r] ? 'fit' : 'no') + '"' + (q ? ' title="' + esc(P.qLabel(q.q)) + '"' : '') + '>' + (q ? U.k(q.v) : '·') + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>';
      out.innerHTML = h;
      txt = 'עם הון עצמי של ' + U.ils(st.e) + ' (' + s.label + '): דירה עד כ־' + U.ils(x.P) + '.' + (n4 ? ' החציון של דירת 4 חדרים נכנס בתקציב ב' + cities(n4) + '.' : '');
    }
    draw();
    p.appendChild(U.el('p', 'nlph-fine', esc('איך מחשבים: מחפשים את המחיר הגבוה ביותר שבו ההון העצמי מכסה את החלק שהבנק לא מממן, את מס הרכישה לפי המדרגות ואת עורך הדין (' + M.cost.lawyer.from + '% ועוד מע״מ). כשמקלידים הכנסה, המשכנתא מוגבלת גם להחזר שבחרתם: 30% קרוב לממוצע של ההלוואות החדשות (' + M.boim.market.pti_avg + '%, בנק ישראל, ' + date(M.boim.market.month) + '), 50% הוא המקסימום של הוראה 329. הריבית: ' + R.label + ', ' + R.rate + '%. החציון הוא של כל הדירות בעיר עם אותו מספר חדרים; שכונה, קומה, מצב ושטח מזיזים את המחיר. בלי שמאי, תיווך, מעבר ושיפוץ.')));
    var src = U.el('p', 'nli__src'); src.innerHTML = U.srcs([{ label: PH.vsrc.he + ', גרסה ' + PH.vsrc.version, url: PH.vsrc.url }, { label: M.nrm.ltv_source.label_he, url: M.nrm.ltv_source.url }, R.src, { label: M.ptax.source, url: M.ptax.url }]); p.appendChild(src);
    p.appendChild(U.share(function () { return txt; }));
  } });

  /* ---------------- boffer ---------------- */
  NI.register('boffer', { custom: function (root, D0) {
    var M = B.model(D0), PH = M.phub, V = M.value;
    var p = panel(root, 'משא ומתן · דירה יד שנייה', 'הצעת מחיר לרכישת דירה: המחיר המבוקש מול העסקאות בעיר');
    p.appendChild(U.el('p', 'nlph-sub', esc('בוחרים עיר, מספר חדרים ומקלידים את המחיר המבוקש. מקבלים את המחיר החציוני של העסקאות שנסגרו, כמה שכונות בעיר נמכרו בחציון נמוך יותר, ומה מבנה טווח פתיחה הגיוני. כל מספר עם הרבעון והמקור שלו.')));
    var ps = pre(root), first = PH.city.filter(function (c) { return c.n === (ps.city || 'רמת גן'); })[0] || PH.city[0];
    var st = { code: first.code, rooms: +(ps.rooms || 4), ask: 0, hood: '' };
    var m0 = B.lastQ(first['r' + st.rooms], PH.q); st.ask = ps.price || Math.round(m0.v * 1.08 / 10000) * 10000;
    var f = U.el('div', 'nlbh-form'); p.appendChild(f);
    var cs = select('עיר', [['0', 'כל הארץ']].concat(PH.city.slice().sort(function (a, b) { return a.n < b.n ? -1 : 1; }).map(function (c) { return [c.code, c.n]; })), st.code, function (v) { st.code = +v; st.hood = ''; hoods(); draw(); }); f.appendChild(cs);
    f.appendChild(field('המחיר המבוקש', '₪', st.ask, function (v) { st.ask = v || 0; draw(); }, true));
    var hs = select('שכונה (לא חובה)', [['', 'כל העיר']], '', function (v) { st.hood = v; draw(); }); f.appendChild(hs);
    p.appendChild(tabs('חדרים', [[3, '3 חדרים'], [4, '4 חדרים'], [5, '5 חדרים']], st.rooms, function (v) { st.rooms = +v; st.hood = ''; hoods(); draw(); }));
    function hoods() { var x = B.offer(PH, V, { code: st.code, rooms: st.rooms, ask: st.ask || 1, hood: '' }); hs.fill([['', 'כל העיר']].concat((x ? x.hoods : []).slice().sort(function (a, b) { return a.n < b.n ? -1 : 1; }).map(function (h) { return [h.id, h.n]; })), st.hood); hs.style.display = x && x.hoods.length ? '' : 'none'; }
    var out = U.el('div', ''); out.setAttribute('aria-live', 'polite'); p.appendChild(out);
    var txt = '';
    function draw() {
      var x = B.offer(PH, V, st); if (!x || !(st.ask > 0)) { out.innerHTML = '<p class="nlph-sub">הקלידו מחיר מבוקש.</p>'; return; }
      var where = x.city + ', ' + x.rooms + ' חדרים', bq = x.hood ? x.hood.q : x.q, bn = x.hood ? 'בשכונת ' + x.hood.n : 'ב' + x.city;
      var lead = x.vs > 0.0005 ? 'המחיר המבוקש גבוה ב־' + pc(x.vs, 1) + '% מהחציון ' + bn : x.vs < -0.0005 ? 'המחיר המבוקש נמוך ב־' + pc(-x.vs, 1) + '% מהחציון ' + bn : 'המחיר המבוקש שווה לחציון ' + bn;
      var h = '<div class="nlph-ans"><div class="nlph-ans__head"><span>' + esc(where) + '</span><small>' + esc(P.qLabel(bq)) + '</small></div><p class="nlph-ans__a"><b>' + esc(lead) + '</b>' + esc(', שעמד על ' + U.ils(x.basis) + ' ב' + P.qLabel(bq) + '.') +
        (x.hoods.length >= 3 ? esc(' ב־' + x.lower + ' מתוך ' + x.hoods.length + ' השכונות בעיר שיש בהן נתון, החציון נמוך מהמחיר המבוקש.') : '') + '</p>' +
        kpis([['החציון', big(x.basis), x.hood ? 'שכונה' : 'כל העיר'], ['המבוקש מול החציון', U.pctTxt(x.vs), '', x.vs > 0 ? 'is-dn' : 'is-up'], ['שכונות זולות יותר', x.hoods.length >= 3 ? x.lower + '/' + x.hoods.length : '·', x.hoods.length >= 3 ? 'לפי החציון' : 'אין מספיק שכונות'], ['טווח פתיחה', x.range ? U.k(x.lo) + ' עד ' + U.k(x.hi) : '·', x.range ? 'באלפי ₪' : 'אין בסיס שוק לירידה']]) + '</div>';
      h += '<p class="nlbh-ql" style="margin-top:14px">על מה הטווח נשען</p><ol class="nlbh-basis">' +
        '<li>' + esc('החציון ' + bn + ': ' + U.ils(x.basis) + ' (' + P.qLabel(bq) + ').') + '</li>' +
        '<li>' + esc('הרבעון הנמוך מבין ארבעת האחרונים שפורסמו ב' + x.city + ': ' + U.ils(x.low.v) + ' ב' + P.qLabel(x.low.q) + ', ' + (x.dip < 0.9995 ? pc(1 - x.dip, 1) + '% מתחת לרבעון האחרון.' : 'הרבעון האחרון הוא הנמוך שבהם.')) + '</li>' +
        (x.yoy != null ? '<li>' + esc('החציון ב' + x.city + ' ' + (x.yoy < 0 ? 'ירד' : 'עלה') + ' ב־' + pc(Math.abs(x.yoy), 1) + '% מול אותו רבעון שנה קודם.') + '</li>' : '') +
        (x.dist ? '<li>' + esc('מדד מחירי הדירות במחוז ' + x.dist.n + ' ' + (x.dist.yoy < 0 ? 'ירד' : 'עלה') + ' ב־' + pc(Math.abs(x.dist.yoy), 1) + '% בשנה (הלמ״ס).') + '</li>' : '') +
        '<li>' + esc(x.range ? 'טווח פתיחה: מ־' + U.ils(x.lo) + ' (החציון, עם הירידה של הרבעון הנמוך) ועד ' + U.ils(x.hi) + ' (' + (x.hi < x.ask ? 'החציון' : 'המחיר המבוקש') + '). זו נקודת פתיחה עם בסיס, לא הערכת שווי של הדירה.' : 'המחיר המבוקש כבר בתחתית הנתונים של השוק. ירידה נוספת נשענת על הדירה עצמה: ממצאי בדק בית, תיקונים נדרשים, מצב הרישום או לוח זמנים שמתאים למוכר.') + '</li></ol>';
      h += '<p class="nlph-fine">' + esc('מה מזיז את המחיר מעל או מתחת לחציון: קומה ומעלית, חניה ומחסן, ממ״ד ומרפסת, מצב ושיפוץ, גיל הבניין, שטח ותכנון ליד. בדירה שמחירה רחוק מהחציון, שמאי מטעמכם לפני ההצעה. אין כאן "הנחה מקובלת": לא מצאנו לה מקור מתוארך.') + '</p>';
      out.innerHTML = h;
      txt = where + ': מבוקש ' + U.ils(st.ask) + ', חציון ' + U.ils(x.basis) + ' (' + P.qLabel(bq) + '), ' + U.pctTxt(x.vs) + '.' + (x.range ? ' טווח פתיחה ' + U.ils(x.lo) + ' עד ' + U.ils(x.hi) + '.' : '');
    }
    hoods(); draw();
    var src = U.el('p', 'nli__src'); src.innerHTML = U.srcs([{ label: PH.vsrc.he + ', גרסה ' + PH.vsrc.version, url: PH.vsrc.url }, { label: V.source + ', קובץ ' + V.file, url: V.url }, { label: PH.hpi.src.he, url: PH.hpi.src.url }]); p.appendChild(src);
    p.appendChild(U.share(function () { return txt; }));
  } });
})();
