/* NadLan Instruments · invest v1 (U2 /investment/, Ben 25.10.2026): "מפת התשואה והתזרים", how much of the flat the rent buys.
   For every city with official medians (data.nadlan.gov.il, rent and deal price in the same quarter) and 3 / 4 / 5 rooms: the gross
   yield, the investor mortgage at the Bank of Israel cap (50% for an additional home, Spitzer at the August 2026 average fixed not
   linked rate), the monthly cash flow before and after the visitor's own costs, the equity needed (price minus loan plus purchase tax
   as an additional home with its 10.2.2027 end date, lawyer and broker with VAT), the three rental-tax tracks, and the share of the
   price the rent alone carries as a mortgage (rent x annuity factor / price). A budget mode turns own money into the cities where a
   median flat fits, ranked by cash flow. Under the readout: the three tax tracks, a ranked board of every city against the loan cap
   and the national line, and a scatter of yield against price; the visitor's city is marked and every row opens that city.
   Data: invest.json (tools/instruments/build_invest_data.py). Design: the engine's identity; marks in ledger ink (verdigris #00806A for a
   flat whose rent carries the loan, signal red #B8322A for one that needs money every month; the pair passes the dataviz validator, deutan dE 9.2). Pure logic in NLIV for unit checks. */
(function () {
  'use strict';
  var QM = { '03': 'ינואר עד מרץ', '06': 'אפריל עד יוני', '09': 'יולי עד ספטמבר', '12': 'אוקטובר עד דצמבר' };
  var HM = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
  function qlab(q) { var p = String(q).split('-'); return (QM[p[1]] || p[1]) + ' ' + p[0]; }
  function mlab(m) { var p = String(m).split('-'); return (HM[+p[1] - 1] || p[1]) + ' ' + p[0]; }
  function qback(q) { var p = String(q).split('-'); return (+p[0] - 1) + '-' + p[1]; }
  function pmt(P, annual, n) { var r = annual / 1200; return n > 0 ? (r === 0 ? P / n : P * r / (1 - Math.pow(1 + r, -n))) : 0; }
  function af(annual, n) { var r = annual / 1200; return r === 0 ? n : (1 - Math.pow(1 + r, -n)) / r; }
  function ptax(price, br) { var t = 0, lo = 0; for (var i = 0; i < br.length; i++) { var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(price, hi); if (top > lo) t += (top - lo) * br[i][1]; if (price <= hi) break; lo = hi; } return t; }
  function rowOf(D, name) { for (var i = 0; i < D.rows.length; i++) if (D.rows[i].n === name) return D.rows[i]; return null; }
  /* the rent and price the calculator opens on: the government median pair, or the CBS average with its sampling error (same quarter) */
  function pairOf(rw, rooms, src) {
    var p = rw && rw.r[String(rooms)]; if (!p) return null;
    var c = src === 'cbs' && rw.cbs && rw.cbs[String(rooms)];
    if (c) return { q: c.q, rent: c.avg, price: c.price, err: c.err, g: c.g, src: 'cbs', n8: p.n8 };
    return { q: p.q, rent: p.rent, price: p.price, n8: p.n8, ry: p.ry, py: p.py, old: p.old, src: 'gov' };
  }
  function rateOf(v, L) { if (v.rsel === 'own') return v.rate; if (v.rsel === 'prime') return L.boi.prime; for (var i = 0; i < L.rates.length; i++) if (L.rates[i].id === v.rsel) return L.rates[i].rate; return L.rates[0].rate; }
  /* rental tax, monthly test on all the landlord's residential rents together (dna.md 6): exempt up to the ceiling, then the exempt
     part falls shekel for shekel and is gone at twice the ceiling; 10% on the gross rent; the marginal track is personal (method only) */
  function rentTax(rent, other, occ, RT) {
    var tot = rent + (other || 0), ex = tot <= RT.ceiling ? tot : Math.max(0, 2 * RT.ceiling - tot);
    return { total: tot, exempt: ex, taxable: tot - ex, full: tot - ex <= 0, ten: RT.ten * rent * occ };
  }
  function calc(v, D) {
    var L = D.rules, tr = L.ptax[v.track] ? v.track : 'extra', P = v.price, Rn = v.rent, n = Math.round(v.years * 12), rate = rateOf(v, L);
    var ltv = Math.max(0, v.ltv) / 100, loan = P * ltv, pay = pmt(loan, rate, n), A = af(rate, n), vat = 1 + L.vat;
    var tax = ptax(P, L.ptax[tr]), law = P * (v.lawyer || 0) / 100 * vat, brk = P * (v.broker || 0) / 100 * vat, reno = v.reno || 0;
    var equity = P - loan + tax + law + brk + reno, total = P + tax + law + brk + reno;
    var occ = Math.max(0, 12 - (v.empty || 0)) / 12, costs = (v.mgmt || 0) + (v.upkeep || 0), reff = Rn * occ;
    var T = rentTax(Rn, v.other, occ, L.rentTax);
    var taxSel = v.taxtrack === 'ten' ? T.ten : (v.taxtrack === 'exempt' && T.full ? 0 : null);  // null: depends on the visitor's marginal rate
    var cf0 = Rn - pay, cf1 = reff - pay - costs, cf2 = taxSel == null ? null : cf1 - taxSel;
    return { tr: tr, rate: rate, n: n, A: A, loan: loan, pay: pay, tax: tax, law: law, brk: brk, reno: reno, equity: equity, total: total,
      gross: Rn * 12 / P, cf0: cf0, cf1: cf1, cf2: cf2, taxSel: taxSel, T: T, occ: occ, costs: costs,
      be: Rn * A / P, beNet: (reff - costs) * A / P, cap: L.ltv[tr], over: ltv > L.ltv[tr] + 1e-9,
      net: (reff - costs - (taxSel || 0)) * 12 / total, coc: equity > 0 ? (cf2 == null ? cf1 : cf2) * 12 / equity : 0,
      beRent: occ > 0 ? (pay + costs) / occ : 0, months: Rn > 0 ? tax / Rn : 0 };
  }
  /* every city with a same-quarter pair in the newest quarter (the ranking never mixes quarters) */
  function ranking(D, rooms, v) {
    var out = [];
    D.rows.forEach(function (rw) {
      if (rw.nat) return; var p = rw.r[String(rooms)]; if (!p || p.q !== D.cityQ) return;
      var x = calc(Object.assign({}, v, { price: p.price, rent: p.rent, other: 0, reno: 0 }), D);
      out.push({ n: rw.n, rooms: +rooms, q: p.q, rent: p.rent, price: p.price, n8: p.n8, gross: x.gross, pay: x.pay, cf0: x.cf0, cf1: x.cf1, be: x.be, equity: x.equity, inv: rw.inv, pp: rw.pp });
    });
    return out.sort(function (a, b) { return b.be - a.be; });
  }
  /* budget mode: own money (0 = no limit) and a price ceiling (0 = none) -> the median flats that fit, by cash flow after costs */
  function budget(v, D) {
    var rooms = v.brooms === '34' ? ['3', '4'] : [String(v.brooms)], all = [], fit = [];
    rooms.forEach(function (k) { ranking(D, k, v).forEach(function (x) { all.push(x); }); });
    all.forEach(function (x) { x.gap = v.equity > 0 ? x.equity - v.equity : 0; if ((v.equity > 0 ? x.gap <= 0 : true) && (v.cap > 0 ? x.price <= v.cap : true)) fit.push(x); });
    fit.sort(function (a, b) { return b.cf1 - a.cf1; });
    var maxP = 0;
    if (v.equity > 0) { var lo = 0, hi = 100000000; for (var i = 0; i < 70; i++) { var mid = (lo + hi) / 2; if (calc(Object.assign({}, v, { price: mid, rent: 0 }), D).equity <= v.equity) lo = mid; else hi = mid; } maxP = Math.floor(lo / 100) * 100; }
    var near = all.filter(function (x) { return fit.indexOf(x) < 0 && (v.cap > 0 ? x.price <= v.cap : true); }).sort(function (a, b) { return a.gap - b.gap; }).slice(0, 8);
    var cities = {}; fit.forEach(function (x) { cities[x.n] = 1; });
    return { fit: fit, near: near, maxP: maxP, cities: Object.keys(cities).length, rows: all.length };
  }
  window.NLIV = { pmt: pmt, af: af, ptax: ptax, calc: calc, ranking: ranking, budget: budget, pairOf: pairOf, rowOf: rowOf, rentTax: rentTax, qlab: qlab };
  if (!window.NadLanInstruments) return;

  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc, hashUsed = false;  // a shared link opens the first instance on the page
  var TRK = { extra: 'דירה נוספת', single: 'דירה יחידה', foreign: 'תושב חוץ' };
  function signed(x) { return Math.round(x) >= 0 ? 'נשארים ' + F.ils(x) : 'חסרים ' + F.ils(-x); }
  function pct(x, d) { return (x < 0 ? '−' : '') + F.pct(Math.abs(x), d == null ? 1 : d); }
  function chg(x, up, down) { return x == null ? '' : (x >= 0 ? up : down) + ' ' + F.pct(Math.abs(x), 1); }
  function today() { return new Date().toISOString().slice(0, 10); }
  function rtl(t) { return '\u200F' + t + '\u200F'; }  // keeps the trailing marks and numbers inside the Hebrew run of an SVG label
  function css() {
    if (document.getElementById('nliv-css')) return;
    var s = document.createElement('style'); s.id = 'nliv-css';
    s.textContent = '.nliv{--iv-pos:#00806A;--iv-neg:#B8322A;--iv-ink:#12304F;--iv-grid:#3E6FA3;--iv-paper:#F6F8FA}' +
      '.nliv-x{display:grid;gap:22px;margin:24px 0 0;position:relative}.nliv-x>section{min-width:0}' +
      'html body .nli h3.nliv-h{font:600 19px/26px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 4px !important;letter-spacing:0;text-transform:none}' +
      '.nliv-sub{font:400 14px/21px var(--nli-sans);color:var(--nli-ink2);margin:0 0 10px;max-width:72ch}' +
      '.nliv-tax{width:100%;border-collapse:collapse;font:400 14px/20px var(--nli-sans);background:var(--iv-paper)}' +
      'html body .nli .nliv-tax th,html body .nli .nliv-tax td{padding:10px 10px !important;border-bottom:1px solid var(--nli-line) !important;text-align:right;vertical-align:top;background:none !important;color:var(--nli-ink);font-size:14px !important;line-height:20px !important}' +
      'html body .nli .nliv-tax th{font-weight:600;white-space:nowrap}.nliv-tax td.n{font-family:var(--nli-sans);font-variant-numeric:tabular-nums;white-space:nowrap;direction:ltr;unicode-bidi:plaintext}' +
      '.nliv-tax tr.is-best th{box-shadow:inset -3px 0 0 var(--iv-pos)}.nliv-best{display:inline-block;margin-inline-start:6px;font:500 12px/16px var(--nli-sans);color:#fff;background:var(--iv-pos);border-radius:2px;padding:1px 6px}' +
      '.nliv-tax small{display:block;color:var(--nli-mute);font-size:12px;line-height:17px;margin-top:2px}' +
      '.nliv-fig{position:relative;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);padding:8px 8px 4px}' +
      '.nliv-fig svg{display:block;width:100%;height:auto;direction:ltr;overflow:visible}' +
      '.nliv-fig text{font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;fill:var(--nli-ink2);font-size:12px}' +
      '.nliv-fig text.v{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums;fill:var(--nli-ink)}' +
      '.nliv-fig text.vw{fill:var(--nli-ink);font-weight:500;font-size:13px}.nliv-fig text.ax{fill:var(--nli-mute);font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px}' +
      '.nliv-fig .row{cursor:pointer}.nliv-fig .row:hover .hit,.nliv-fig .row:focus .hit{fill:#EEF3F6}.nliv-fig .row:focus{outline:none}' +
      '.nliv-fig .row.is-me text{fill:var(--iv-ink);font-weight:600}.nliv-fig .row.is-me .hit{fill:#E6EEF4}.nliv-fig .row.is-off{opacity:.32}' +
      '.nliv-fig .dot{cursor:pointer;stroke:#fff;stroke-width:2}.nliv-fig .dot.is-thin{fill:#fff !important;stroke-width:2}.nliv-fig .dot.is-off{opacity:.18}' +
      '.nliv-fig .dot:hover,.nliv-fig .dot:focus{stroke:var(--iv-ink);outline:none}' +
      '.nliv-tip{position:absolute;z-index:3;pointer-events:none;background:var(--iv-ink);color:#fff;border-radius:4px;padding:8px 10px;font:400 13px/19px var(--nli-sans);max-width:250px;box-shadow:0 2px 8px rgba(18,48,79,.22);direction:rtl;text-align:right}' +
      '.nliv-tip b{font-weight:600}.nliv-tip span{display:block;font-family:var(--nli-mono);font-variant-numeric:tabular-nums;direction:ltr;unicode-bidi:plaintext;text-align:right}' +
      '.nliv-legend{display:flex;flex-wrap:wrap;gap:6px 16px;list-style:none;margin:8px 0 0;padding:0;font:400 13px/18px var(--nli-sans);color:var(--nli-ink2)}' +
      '.nliv-legend li{display:flex;align-items:center;gap:6px;margin:0}.nliv-legend i{display:inline-block;width:12px;height:12px;border-radius:2px}.nliv-legend i.c{border-radius:50%}' +
      '.nliv-legend i.l{width:14px;height:0;border-top:2px solid var(--iv-ink);border-radius:0}.nliv-legend i.d{width:14px;height:0;border-top:2px dashed var(--nli-mute);border-radius:0}' +
      'html body .nli button.nliv-more{min-height:44px;padding:8px 14px;margin:10px 0 0;border:1px solid var(--nli-sea);border-radius:var(--nli-r-s);background:var(--nli-surface);color:var(--nli-sea);font:500 14px/20px var(--nli-sans);cursor:pointer}' +
      '.nliv-picked{font:500 13px/18px var(--nli-sans);color:var(--iv-pos);min-height:18px;margin:6px 0 0}' +
      '.nliv-limits{font:400 13px/20px var(--nli-sans);color:var(--nli-ink2);margin:0;padding:12px;border-inline-start:3px solid var(--iv-ink);background:var(--iv-paper)}' +
      'html body .nli .nli__lines dd.is-w,html body .nli .nli__scen strong.is-w{font-family:var(--nli-sans)}html body .nli .nli__lines dd.is-pos,html body .nli .nli__scen strong.is-pos{color:var(--iv-pos)}html body .nli .nli__lines dd.is-neg,html body .nli .nli__scen strong.is-neg{color:var(--iv-neg)}' +
      '@media (max-width:600px){html body .nli .nliv-tax,html body .nli .nliv-tax tbody,html body .nli .nliv-tax tr,html body .nli .nliv-tax th,html body .nli .nliv-tax td{display:block !important;width:auto !important}' +
      'html body .nli .nliv-tax tr{padding:8px 0;border-bottom:1px solid var(--nli-line)}html body .nli .nliv-tax th,html body .nli .nliv-tax td{border:0 !important;padding:3px 10px !important;white-space:normal}' +
      'html body .nliv .nli__strip{display:grid;grid-template-columns:1fr 1fr;gap:10px 12px}}' +
      '@media print{.nliv-tip,html body .nli button.nliv-more{display:none !important}.nliv-x{display:block}}';
    document.head.appendChild(s);
  }

  NI.register('invest', {
    custom: function (root, D0) {
      css();
      var D = D0.invest || D0.d0, L = D.rules, nat = D.rows[0];
      var nRank = ranking(D, 4, { price: 0, rent: 0, track: 'extra', ltv: 50, rsel: 'fixed', years: 25, lawyer: L.lawyer }).length;
      var fixedRate = L.rates[0];
      /* the page's own case ([nadlan_tool id="invest" city="חיפה" rooms="3"]) and a shared link (#invest?c=...) open the tool on it */
      var set = {}; try { set = JSON.parse(root.getAttribute('data-nli-set') || '{}'); } catch (e) {}
      if (set.city && !rowOf(D, set.city)) delete set.city;
      try { if (!hashUsed && /^#invest\?/.test(location.hash)) { hashUsed = true; var q = new URLSearchParams(location.hash.slice(8)); var K = { m: 'mode', c: 'city', r: 'rooms', s: 'rsrc', p: 'price', t: 'rent', k: 'track', l: 'ltv', i: 'rsel', a: 'rate', y: 'years', e: 'equity', b: 'brooms', x: 'cap', g: 'mgmt', u: 'upkeep', z: 'empty', w: 'taxtrack', o: 'other', w2: 'lawyer', br: 'broker', rn: 'reno' };
        q.forEach(function (val, key) { var f = K[key]; if (!f) return; set[f] = /^(mode|city|rsrc|track|rsel|brooms|taxtrack)$/.test(f) ? val : parseFloat(val); }); set.more = 1; } } catch (e) {}
      function refill(v) { var p = pairOf(rowOf(D, v.city), v.rooms, v.rsrc); v.price = p ? Math.round(p.price) : 0; v.rent = p ? Math.round(p.rent) : 0; }
      var start = { city: set.city && rowOf(D, set.city) ? set.city : 'ישראל', rooms: set.rooms || 4, rsrc: set.rsrc || 'gov' }; refill(start);
      var host = document.createElement('div'); host.setAttribute('data-nli-set', JSON.stringify(set)); root.innerHTML = ''; root.appendChild(host);
      if (!root.closest('.nli')) root.classList.add('nli'); root.classList.add('nliv'); root.setAttribute('dir', 'rtl');
      var api = null, X = null, showAll = false, budAll = false, lastKey = '', lastMode = '', picked = '';

      function spec() {
        var inBudget = function (v) { return v.mode === 'budget'; }, inCity = function (v) { return v.mode !== 'budget'; }, more = function (v) { return !!v.more; };
        return {
          kicker: 'מחשבון · נדל״ן להשקעה',
          title: 'מפת התשואה והתזרים',
          lede: 'כמה מכניסה דירה להשקעה בכל עיר, כמה נשאר או חסר בחודש אחרי המשכנתא, כמה הון עצמי צריך, ואיזה חלק מהמחיר שכר הדירה לבדו מחזיק. ' + nRank + ' ערים, 3 עד 5 חדרים, לפי החציונים הרשמיים של ' + qlab(D.cityQ) + ', וכל חישוב מסומן "החישוב שלנו".',
          strip: function () { var I = L.idx, pm = String(I.price.m).split('-'); return [
            { label: 'מס רכישה, דירה נוספת', value: '8% עד ' + F.date(L.ptax.until.extra) },
            { label: 'מימון מרבי, דירה להשקעה', value: F.num(100 * L.ltv.extra) + '%' },
            { label: 'ריבית ממוצעת קבועה לא צמודה, ' + mlab(L.ratesPeriod), value: F.num(fixedRate.rate, 2) + '%' },
            { label: 'פטור ממס על שכר דירה', value: F.ils(L.rentTax.ceiling) + ' בחודש' },
            { label: 'שכר הדירה בשנה, הלמ״ס ' + mlab(I.rent.m), value: chg(I.rent.yoy / 100, 'עלה', 'ירד') },
            { label: 'מחירי הדירות בשנה, הלמ״ס ' + HM[+pm[1] - 1] + ' עד ' + HM[+pm[1] % 12] + ' ' + pm[0], value: chg(I.price.yoy / 100, 'עלו', 'ירדו') }]; },
          exampleNote: 'המחשבון נפתח על דירת 4 חדרים בחציון הארצי. בחרו עיר, מספר חדרים או מחיר משלכם, והכול מתעדכן מיד.',
          presets: function () {
            var tlv = pairOf(rowOf(D, 'תל אביב-יפו'), 3, 'gov'), n4 = pairOf(nat, 4, 'gov'), base = { track: 'extra', ltv: 100 * L.ltv.extra };
            var P = [{ key: 'nat4', label: 'דירת 4 חדרים בחציון הארצי', sub: F.ils(n4.price) + ' · ' + F.ils(n4.rent) + ' בחודש', set: Object.assign({ mode: 'city', city: 'ישראל', rooms: 4, rsrc: 'gov', price: n4.price, rent: n4.rent }, base) },
              { key: 'm1', label: 'דירה עד מיליון ₪', sub: '3 או 4 חדרים, כל הערים', set: Object.assign({ mode: 'budget', equity: 0, cap: 1000000, brooms: '34' }, base) },
              { key: 'e200', label: '200 אלף ₪ הון עצמי', sub: 'אילו ערים עובדות', set: Object.assign({ mode: 'budget', equity: 200000, cap: 0, brooms: '34' }, base) },
              { key: 'e400', label: '400 אלף ₪ הון עצמי', sub: 'אילו ערים עובדות', set: Object.assign({ mode: 'budget', equity: 400000, cap: 0, brooms: '34' }, base) }];
            if (tlv) P.push({ key: 'tlv3', label: 'תל אביב, 3 חדרים', sub: F.ils(tlv.price) + ' · ' + F.ils(tlv.rent) + ' בחודש', set: Object.assign({ mode: 'city', city: 'תל אביב-יפו', rooms: 3, rsrc: 'gov', price: tlv.price, rent: tlv.rent }, base) });
            return P;
          },
          defaults: function () { return { mode: 'city', city: start.city, rooms: start.rooms, rsrc: start.rsrc, price: start.price, rent: start.rent, track: 'extra', more: 0, ltv: 100 * L.ltv.extra,
            rsel: 'fixed', rate: fixedRate.rate, years: 25, sign: today(), lawyer: L.lawyer, broker: 0, reno: 0, mgmt: 0, upkeep: 0, empty: 0, taxtrack: 'exempt', other: 0, equity: 400000, cap: 0, brooms: '34' }; },
          fields: [
            { id: 'mode', label: 'מה בודקים', type: 'segmented', options: [{ value: 'city', label: 'דירה בעיר אחת' }, { value: 'budget', label: 'יש לי הון עצמי: אילו ערים עובדות?' }] },
            { id: 'city', label: 'עיר', type: 'select', showIf: inCity, optionsFrom: function () { return [{ value: 'ישראל', label: 'ישראל, החציון הארצי' }].concat(D.rows.slice(1).map(function (r) { return { value: r.n, label: r.n }; }).sort(function (a, b) { return a.label.localeCompare(b.label, 'he'); })); } },
            { id: 'rooms', label: 'חדרים', type: 'segmented', showIf: inCity, options: [{ value: 3, label: '3' }, { value: 4, label: '4' }, { value: 5, label: '5' }] },
            { id: 'rsrc', label: 'שכר הדירה לפי', type: 'segmented', showIf: function (v) { var r = rowOf(D, v.city); return inCity(v) && !!(r && r.cbs && r.cbs[String(v.rooms)]); },
              options: [{ value: 'gov', label: 'אתר הנדל״ן הממשלתי (חציון)' }, { value: 'cbs', label: 'הלמ״ס (ממוצע)' }] },
            { id: 'price', label: 'מחיר הדירה', type: 'money', unit: '₪', showIf: inCity, help: 'נפתח על המחיר החציוני של העסקאות שנסגרו. אפשר להקליד מחיר משלכם.' },
            { id: 'rent', label: 'שכר דירה בחודש', type: 'money', unit: '₪', showIf: inCity, help: 'נפתח על שכר הדירה החציוני באותו רבעון. אפשר להקליד שכר דירה משלכם.' },
            { id: 'equity', label: 'ההון העצמי שלכם', type: 'money', unit: '₪', showIf: inBudget, help: 'כל הכסף לעסקה, כולל מס רכישה ועורך דין. 0 = בלי הגבלה, רק לפי המחיר.' },
            { id: 'cap', label: 'מחיר דירה עד', type: 'money', unit: '₪', showIf: inBudget, help: '0 = בלי תקרת מחיר.' },
            { id: 'brooms', label: 'חדרים', type: 'segmented', showIf: inBudget, options: [{ value: '34', label: '3 או 4' }, { value: '3', label: '3' }, { value: '4', label: '4' }, { value: '5', label: '5' }] },
            { id: 'track', label: 'מי קונה', type: 'segmented', options: [{ value: 'extra', label: 'דירה נוספת' }, { value: 'single', label: 'דירה יחידה' }, { value: 'foreign', label: 'תושב חוץ' }] },
            { id: 'more', label: 'פרטי העסקה', type: 'segmented', options: [{ value: 0, label: 'החישוב המהיר' }, { value: 1, label: 'הכול: מימון, הוצאות ומס' }] },
            { id: 'ltv', label: 'שיעור המימון', type: 'percent', unit: '%', showIf: more, help: 'בנק ישראל (הוראה 329): עד 50% בדירה נוספת ולתושב חוץ, עד 75% בדירה יחידה.' },
            { id: 'rsel', label: 'ריבית', type: 'select', showIf: more, help: 'הממוצע של המשכנתאות החדשות לפי בנק ישראל, ' + mlab(L.ratesPeriod) + '. הפריים בלי המרווח של הבנק.', optionsFrom: function () { return L.rates.map(function (r) { return { value: r.id, label: r.he + ' ' + F.num(r.rate, 2) + '%' }; })
              .concat([{ value: 'prime', label: 'פריים ' + F.num(L.boi.prime, 2) + '%' }, { value: 'own', label: 'ריבית אחרת' }]); } },
            { id: 'rate', label: 'הריבית שלכם', type: 'percent', unit: '%', showIf: function (v) { return v.more && v.rsel === 'own'; } },
            { id: 'years', label: 'שנים', type: 'number', unit: 'שנים', showIf: more },
            { id: 'sign', label: 'מועד החתימה', type: 'date', showIf: function (v) { return v.more && inCity(v) && v.track !== 'single'; } },
            { id: 'lawyer', label: 'עורך דין, לפני מע״מ', type: 'percent', unit: '%', showIf: more },
            { id: 'broker', label: 'תיווך, לפני מע״מ', type: 'percent', unit: '%', showIf: more, help: 'מקובל ' + L.broker + '%. 0 אם קונים בלי מתווך.' },
            { id: 'reno', label: 'שיפוץ וריהוט', type: 'money', unit: '₪', showIf: more },
            { id: 'mgmt', label: 'דמי ניהול בחודש', type: 'money', unit: '₪', showIf: more, help: 'ההוצאות הן שלכם: אין להן נורמה רשמית, ולכן הן נפתחות על 0.' },
            { id: 'upkeep', label: 'ועד בית, ביטוח ותחזוקה בחודש', type: 'money', unit: '₪', showIf: more },
            { id: 'empty', label: 'חודשים בלי שוכר בשנה', type: 'number', showIf: more },
            { id: 'taxtrack', label: 'מסלול המס על שכר הדירה', type: 'segmented', showIf: function (v) { return v.more && inCity(v); }, options: [{ value: 'exempt', label: 'פטור' }, { value: 'ten', label: '10%' }, { value: 'marginal', label: 'מס שולי' }] },
            { id: 'other', label: 'שכר דירה ממגורים שכבר מקבלים', type: 'money', unit: '₪', showIf: function (v) { return v.more && inCity(v) && v.taxtrack === 'exempt'; }, help: 'מבחן הפטור חודשי, על כל שכר הדירה ממגורים שלכם יחד.' }
          ],
          onField: function (id, v, d, redraw) {
            if (id === 'city' || id === 'rooms' || id === 'rsrc') { refill(v); redraw('price'); redraw('rent'); }
            if (id === 'track') { v.ltv = 100 * L.ltv[v.track]; redraw('ltv'); }
          },
          compute: function (v, d, scen) { var r = v.mode === 'budget' ? budgetOut(v) : cityOut(v, scen); setTimeout(function () { extras(v); }, 0); return r; }
        };
      }

      function cityOut(v, scen) {
        var rw = rowOf(D, v.city), p = pairOf(rw, v.rooms, v.rsrc);
        if (!(v.price > 0) || !(v.rent > 0)) return { error: { field: 'price', msg: p ? 'הקלידו מחיר ושכר דירה.' : 'לעיר הזאת לא פורסם חציון ל־' + v.rooms + ' חדרים. בחרו מספר חדרים אחר, או הקלידו מחיר ושכר דירה.' } };
        if (!(v.years >= 4 && v.years <= 30)) return { error: { field: 'years', msg: 'בין 4 ל־30 שנים.' } };
        if (!(v.ltv >= 0 && v.ltv <= 100)) return { error: { field: 'ltv', msg: 'בין 0% ל־100%.' } };
        var w = Object.assign({}, v);
        if (scen === 'rate') { w.rsel = 'own'; w.rate = rateOf(v, L) + 1; } else if (scen === 'rent') w.rent = v.rent * 0.9; else if (scen === 'empty') w.empty = (v.empty || 0) + 1;
        var x = calc(w, D), base = calc(v, D); X = { v: v, x: x, p: p, rw: rw };
        var ownP = !p || Math.round(p.price) !== Math.round(v.price), ownR = !p || Math.round(p.rent) !== Math.round(v.rent), where = rw.nat ? 'ישראל' : v.city;
        var mine = ' · החישוב שלנו', lines = [];
        lines.push({ label: ownP ? 'מחיר הדירה שהקלדתם' : 'מחיר חציוני, ' + v.rooms + ' חדרים, ' + where + ', ' + qlab(p.q), value: F.ils(v.price) });
        lines.push({ label: ownR ? 'שכר הדירה שהקלדתם' : (p.src === 'cbs' ? 'שכר דירה ממוצע (הלמ״ס, ' + p.g.replace('-', ' עד ') + ' חדרים, טעות דגימה ' + F.ils(p.err) + ')' : 'שכר דירה חציוני, ' + qlab(p.q)), value: F.ils(w.rent) });
        lines.push({ label: 'תשואה ברוטו בשנה' + mine, value: pct(x.gross, 2) });
        lines.push({ label: 'משכנתא ' + F.num(v.ltv) + '%, ' + F.num(v.years) + ' שנים, ריבית ' + F.num(x.rate, 2) + '%', value: F.ils(x.loan) });
        lines.push({ label: 'החזר חודשי (שפיצר)' + mine, value: F.ils(x.pay) });
        lines.push({ label: 'שכר הדירה פחות ההחזר' + mine, value: signed(x.cf0) });
        if (x.costs > 0 || w.empty > 0) lines.push({ label: 'אחרי ההוצאות והחודשים הריקים שלכם' + mine, value: signed(x.cf1) });
        if (v.taxtrack === 'ten') lines.push({ label: 'אחרי מס 10% על שכר הדירה' + mine, value: signed(x.cf2) });
        else if (v.taxtrack === 'exempt' && !x.T.full) lines.push({ label: 'אחרי מס: ' + F.ils(x.T.taxable) + ' בחודש חייבים במס שולי', value: 'לפני המס השולי' });
        lines.push({ label: 'הון עצמי נדרש' + mine, value: F.ils(x.equity) });
        lines.push({ label: 'מס רכישה, ' + TRK[x.tr] + (x.months >= 1 ? ' · שווה ' + F.num(x.months, 0) + ' חודשי שכירות' : x.tax > 0.5 ? ' · פחות מחודש שכירות' : ''), value: x.tax > 0.5 ? F.ils(x.tax) : 'אין מס רכישה' });
        if (x.law + x.brk > 0.5) lines.push({ label: (x.brk > 0.5 ? 'עורך דין ותיווך' : 'עורך דין') + ', כולל מע״מ ' + F.num(100 * L.vat) + '%', value: F.ils(x.law + x.brk) });
        lines.push({ label: 'תשואה נטו על העלות הכוללת' + mine, value: pct(x.net, 2) });
        lines.push({ label: 'תשואה על ההון העצמי, בשנה' + mine, value: pct(x.coc, 1) });
        lines.push({ label: 'שכר הדירה שמכסה את ההחזר וההוצאות' + mine, value: F.ils(x.beRent) });
        if (!ownP && p.src === 'gov' && p.py != null) lines.push({ label: 'המחיר החציוני מול ' + qlab(qback(p.q)), value: chg(p.py, 'עלה', 'ירד') });
        if (!ownR && p.src === 'gov' && p.ry != null) lines.push({ label: 'שכר הדירה החציוני מול ' + qlab(qback(p.q)), value: chg(p.ry, 'עלה', 'ירד') });
        if (rw.gy != null) lines.push({ label: 'התשואה באתר הנדל״ן הממשלתי (כל החדרים, שנה)', value: F.num(rw.gy, 2) + '%' });
        var notes = [];
        if (x.over) notes.push('<b>שיעור המימון מעל המותר:</b> ל' + TRK[x.tr] + ' בנק ישראל מתיר עד ' + F.num(100 * x.cap) + '% מהשווי.');
        if (p && p.old && !ownP) notes.push('<b>רבעון אחר:</b> ל' + esc(where) + ' אין חציון של ' + v.rooms + ' חדרים ל' + qlab(D.cityQ) + '. המספרים מ' + qlab(p.q) + ', ולכן העיר לא נכנסת לדירוג.');
        if (p && p.n8 <= 4 && !ownP) notes.push('<b>מעט עסקאות:</b> החציון של ' + v.rooms + ' חדרים ב' + esc(where) + ' פורסם רק ב־' + p.n8 + ' מתוך 8 הרבעונים האחרונים. מספר אחד לא מספר את כל העיר.');
        if (x.tr !== 'single' && v.sign && v.sign > L.ptax.until.extra) notes.push('<b>חתימה אחרי ' + F.date(L.ptax.until.extra) + ':</b> הוראת השעה של 8% ו־10% הוארכה עד התאריך הזה. מה יחול אחריו עוד לא פורסם, והחישוב נשאר לפי 8% ו־10%.');
        if (v.taxtrack === 'marginal') notes.push('<b>מס שולי:</b> מורידים מההכנסה את ההוצאות ואת הפחת, ומשלמים מס לפי המדרגות, מ־' + F.num(100 * L.rentTax.under60) + '% עד גיל 60 ומ־' + F.num(100 * L.rentTax.over60) + '% מגיל 60. החישוב אישי, ולכן התזרים כאן לפני המס.');
        if (!notes.length) notes.push(rw.gy != null ? 'התשואה באתר הנדל״ן הממשלתי היא שכר הדירה החציוני של השנה האחרונה, כל החדרים יחד, כפול 12 חלקי המחיר החציוני השנתי. בדקנו את זה ב־' + D.checks.govYieldFormula[0] + ' ערים. כאן החישוב לפי מספר החדרים ולפי אותו רבעון, ולכן הוא יכול לצאת שונה.' : 'החציון הוא המחיר שחצי מהעסקאות מעליו וחצי מתחתיו.');
        var R = ranking(D, v.rooms, v), ltvTxt = F.num(v.ltv) + '%';
        var sc = [['base', 'כמו שהקלדתם', base], ['rate', 'ריבית גבוהה ב־1%', calc(Object.assign({}, v, { rsel: 'own', rate: rateOf(v, L) + 1 }), D)], ['rent', 'שכר דירה נמוך ב־10%', calc(Object.assign({}, v, { rent: v.rent * 0.9 }), D)], ['empty', 'עוד חודש ריק בשנה', calc(Object.assign({}, v, { empty: (v.empty || 0) + 1 }), D)]];
        var link = location.origin + location.pathname + '#invest?' + new URLSearchParams({ m: 'city', c: v.city, r: v.rooms, s: v.rsrc, p: Math.round(v.price), t: Math.round(v.rent), k: v.track, l: v.ltv, i: v.rsel, a: rateOf(v, L), y: v.years, g: v.mgmt || 0, u: v.upkeep || 0, z: v.empty || 0, w: v.taxtrack, o: v.other || 0, w2: v.lawyer || 0, br: v.broker || 0, rn: v.reno || 0 }).toString();
        return {
          answer: { label: 'כמה מהדירה שכר הדירה קונה', value: pct(x.be, 1),
            sub: 'שכר דירה של ' + F.ils(w.rent) + ' בחודש מחזיק לבדו משכנתא של ' + F.ils(x.be * v.price) + ', ' + pct(x.be, 1) + ' מהמחיר. המימון שלכם ' + ltvTxt + ', ההחזר ' + F.ils(x.pay) + ', ולכן ' + (x.cf0 >= 0 ? '<b style="color:#00806A">' : '<b style="color:#B8322A">') + signed(x.cf0) + ' בחודש</b> לפני הוצאות. החישוב שלנו.' },
          breakdown: [{ label: 'משכנתא', value: x.loan, kind: 'sea' }, { label: 'הון עצמי לדירה', value: v.price - x.loan, kind: 'housing' }, { label: 'מס רכישה', value: x.tax, kind: 'survey' }, { label: 'עורך דין ותיווך עם מע״מ', value: x.law + x.brk, kind: 'civic' }, { label: 'שיפוץ וריהוט', value: x.reno, kind: 'open' }],
          lines: lines,
          scenarioLabel: 'מה אם: שכר הדירה פחות ההחזר וההוצאות, בחודש',
          scenarios: sc.map(function (s) { var y = s[2], val = y.cf2 == null ? y.cf1 : y.cf2; return { key: s[0], name: s[1], value: signed(val), on: (scen || 'base') === s[0] }; }),
          note: notes.join('<br>'),
          table: { title: 'כל ' + R.length + ' הערים, ' + v.rooms + ' חדרים, ' + qlab(D.cityQ) + ': מימון ' + ltvTxt + ', ריבית ' + F.num(x.rate, 2) + '%, ' + v.years + ' שנים', head: ['עיר', 'שכר דירה', 'מחיר', 'תשואה ברוטו', 'החזר', 'שכר דירה פחות החזר', 'כמה מהדירה שכר הדירה קונה', 'הון עצמי'], num: [1, 2, 3, 4, 5, 6, 7], phoneHide: [1, 2, 4, 7],
            rows: R.map(function (c) { return [c.n + (c.n8 <= 4 ? ' (מעט עסקאות)' : ''), F.ils(c.rent), F.ils(c.price), pct(c.gross, 2), F.ils(c.pay), signed(c.cf0), pct(c.be, 1), F.ils(c.equity)]; }) },
          formula: 'תשואה ברוטו = שכר דירה × 12 ÷ מחיר. החזר = לוח שפיצר על המשכנתא, ' + x.n + ' תשלומים בריבית ' + F.num(x.rate, 2) + '%. כמה מהדירה שכר הדירה קונה = שכר דירה × ' + F.num(x.A, 2) + ' (הערך של ' + x.n + ' תשלומים בריבית הזאת) ÷ מחיר. הון עצמי = מחיר פחות משכנתא, ועוד מס רכישה, עורך דין ותיווך עם מע״מ, ושיפוץ. תשואה נטו = (שכר דירה בחודשים המלאים פחות ההוצאות והמס) × 12 ÷ העלות הכוללת.',
          sources: srcs(p && p.src === 'cbs'),
          text: 'מפת התשואה והתזרים, ' + where + ', ' + v.rooms + ' חדרים: מחיר ' + F.ils(v.price) + ', שכר דירה ' + F.ils(w.rent) + ', תשואה ברוטו ' + pct(x.gross, 2) + '. משכנתא ' + ltvTxt + ' בריבית ' + F.num(x.rate, 2) + '%: החזר ' + F.ils(x.pay) + ', ' + signed(x.cf0) + ' בחודש. שכר הדירה קונה ' + pct(x.be, 1) + ' מהדירה. הון עצמי ' + F.ils(x.equity) + ' (החישוב שלנו).\n' + link,
          bare: true
        };
      }

      function budgetOut(v) {
        if (!(v.equity > 0) && !(v.cap > 0)) return { error: { field: 'equity', msg: 'הקלידו הון עצמי או מחיר מרבי.' } };
        if (!(v.years >= 4 && v.years <= 30)) return { error: { field: 'years', msg: 'בין 4 ל־30 שנים.' } };
        var B = budget(v, D), rate = rateOf(v, L), roomsTxt = v.brooms === '34' ? '3 או 4 חדרים' : v.brooms + ' חדרים'; X = { v: v, B: B };
        var top = B.fit[0], ans, lines = [];
        if (v.equity > 0) {
          var m = calc(Object.assign({}, v, { price: B.maxP, rent: 0 }), D);
          ans = { label: 'הדירה היקרה ביותר ש־' + F.ils(v.equity) + ' הון עצמי קונים, במימון ' + F.num(v.ltv) + '%', value: F.ils(B.maxP),
            sub: B.cities ? (B.cities + ' ערים שבהן דירת ' + roomsTxt + ' בחציון נכנסת בסכום הזה' + (top ? '. הכי טוב בתזרים: ' + esc(top.n) + ', ' + top.rooms + ' חדרים, ' + signed(top.cf1) + ' בחודש' : '') + '. החישוב שלנו.')
              : 'אף דירת ' + roomsTxt + ' בחציון של עיר לא נכנסת בסכום הזה. ברשימה למטה: הערים הקרובות ביותר וכמה הון עצמי חסר. החישוב שלנו.' };
          lines.push({ label: 'משכנתא על הדירה הזאת', value: F.ils(m.loan) }, { label: 'מס רכישה, ' + TRK[m.tr], value: F.ils(m.tax) }, { label: 'עורך דין ותיווך עם מע״מ', value: F.ils(m.law + m.brk) });
        } else {
          ans = { label: 'ערים שבהן דירת ' + roomsTxt + ' בחציון עולה עד ' + F.ils(v.cap), value: B.cities ? B.cities + ' ערים' : 'אף עיר',
            sub: top ? 'הכי טוב בתזרים: ' + esc(top.n) + ', ' + top.rooms + ' חדרים, ' + signed(top.cf1) + ' בחודש. החישוב שלנו.' : 'נסו תקרת מחיר גבוהה יותר.' };
        }
        if (v.cap > 0) lines.push({ label: 'תקרת המחיר שבחרתם', value: F.ils(v.cap) });
        lines.push({ label: 'ריבית ותקופה', value: F.num(rate, 2) + '% · ' + v.years + ' שנים' });
        var rows = B.fit.length ? B.fit : B.near, has = !!B.fit.length;
        return {
          answer: ans, lines: lines,
          note: 'החישוב לכל עיר: מחיר חציוני ושכר דירה חציוני מאותו רבעון (' + qlab(D.cityQ) + '), מימון ' + F.num(v.ltv) + '%, מס רכישה ל' + TRK[v.track] + ', עורך דין' + (v.broker ? ' ותיווך' : '') + ' עם מע״מ' + (v.reno ? ' ושיפוץ' : '') + '. התזרים: שכר הדירה פחות ההחזר' + ((v.mgmt || 0) + (v.upkeep || 0) + (v.empty || 0) ? ', ההוצאות והחודשים הריקים שהקלדתם' : '') + ', לפני מס.',
          table: { title: has ? 'כל ' + rows.length + ' הדירות שנכנסות, מהתזרים הטוב לחלש' : 'הערים הקרובות ביותר', head: ['דירה', 'מחיר חציוני', 'הון עצמי נדרש', has ? 'שכר דירה' : 'חסר הון עצמי', 'תזרים בחודש', 'כמה מהדירה שכר הדירה קונה'], num: [1, 2, 3, 4, 5], phoneHide: [1, 3],
            rows: rows.map(function (c) { return [c.n + ', ' + c.rooms + ' חדרים' + (c.n8 <= 4 ? ' (מעט עסקאות)' : ''), F.ils(c.price), F.ils(c.equity), has ? F.ils(c.rent) : F.ils(c.gap), signed(c.cf1), pct(c.be, 1)]; }) },
          formula: 'עיר נכנסת כשמחיר פחות משכנתא, ועוד מס רכישה, עורך דין ותיווך עם מע״מ ושיפוץ, לא עובר את ההון העצמי' + (v.cap > 0 ? ', והמחיר עד התקרה' : '') + '. המחיר המרבי נמצא בחיפוש על אותה נוסחה.',
          sources: srcs(false),
          text: 'מפת התשואה והתזרים: ' + (v.equity > 0 ? 'עם ' + F.ils(v.equity) + ' הון עצמי ומימון ' + F.num(v.ltv) + '%, דירה עד ' + F.ils(B.maxP) + '. ' : 'דירות עד ' + F.ils(v.cap) + '. ') + (B.cities ? B.cities + ' ערים נכנסות' + (top ? ', הכי טוב בתזרים ' + top.n + ' (' + signed(top.cf1) + ' בחודש)' : '') : 'אף חציון לא נכנס') + ' (החישוב שלנו).\n' + location.origin + location.pathname + '#invest?' + new URLSearchParams({ m: 'budget', e: v.equity || 0, x: v.cap || 0, b: v.brooms, k: v.track, l: v.ltv, i: v.rsel, a: rate, y: v.years }).toString(),
          bare: true
        };
      }

      function srcs(cbs) {
        var S = D.src, o = [{ label: S.gov.he + ', נקרא ' + F.date(S.gov.read), url: S.gov.url }];
        if (cbs) o.push({ label: S.cbs49.he, url: S.cbs49.url });
        o.push({ label: S.boiMrtg.he.replace(L.ratesPeriod, mlab(L.ratesPeriod)), url: S.boiMrtg.url }, { label: S.d329.he, url: S.d329.url }, { label: S.ptax.he, url: S.ptax.url }, { label: S.knesset.he, url: S.knesset.url }, { label: S.kz.he, url: S.kz.url });
        return o;
      }

      /* ---------------- under the readout: the tax tracks, the board, the scatter, the limits ---------------- */
      var xs = document.createElement('div'); xs.className = 'nliv-x';
      xs.innerHTML = '<section class="nliv-budS" hidden></section><section class="nliv-taxs"></section><section class="nliv-boardS"></section><section class="nliv-scatS"></section>' +
        '<p class="nliv-limits"></p>';

      function pick(name) {
        if (!api || !rowOf(D, name)) return; var v = api.state.v;
        var wasBudget = v.mode === 'budget'; v.mode = 'city'; v.city = name; refill(v); api.state.pre = null; api.state.scen = null;
        [].forEach.call(host.querySelectorAll('.nli__pre button'), function (b) { b.setAttribute('aria-pressed', 'false'); });
        [].forEach.call(host.querySelectorAll('.nli__seg button'), function (b) { if (b.textContent === 'דירה בעיר אחת') b.setAttribute('aria-pressed', 'true'); if (b.textContent.indexOf('יש לי הון עצמי') === 0) b.setAttribute('aria-pressed', 'false'); });
        if (wasBudget) [].forEach.call(host.querySelectorAll('.nli__seg'), function (g) { var bs = [].map.call(g.children, function (b) { return b.textContent; }); if (bs.join() === '3,4,5') [].forEach.call(g.children, function (b) { b.setAttribute('aria-pressed', String(b.textContent === String(v.rooms))); }); });
        if (api.state.redraw.price) api.state.redraw.price(); if (api.state.redraw.rent) api.state.redraw.rent();
        api.run();
        var a = host.querySelector('.nli__answer'); if (a && a.getBoundingClientRect().top < 0 && a.scrollIntoView) a.scrollIntoView({ block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
        picked = 'נבחרה ' + name + '. המספרים למעלה התעדכנו.'; var pk = xs.querySelector('.nliv-picked'); if (pk) pk.textContent = picked;
      }
      function tipAt(tip, ev, html, box) {
        tip.innerHTML = html; tip.hidden = false;
        var r = box.getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top, w = tip.offsetWidth, h = tip.offsetHeight;
        tip.style.left = Math.max(4, Math.min(r.width - w - 4, x - w / 2)) + 'px'; tip.style.top = Math.max(4, y - h - 14) + 'px';
      }
      function wire(fig, getHtml, before) {
        var tip = document.createElement('div'); tip.className = 'nliv-tip'; tip.hidden = true; fig.appendChild(tip);
        fig.addEventListener('pointermove', function (ev) { if (ev.pointerType === 'touch') return; var t = ev.target.closest && ev.target.closest('[data-c]'); if (!t) { tip.hidden = true; return; } tipAt(tip, ev, getHtml(t.getAttribute('data-c'), t.getAttribute('data-k'), t), fig); });
        fig.addEventListener('pointerleave', function () { tip.hidden = true; });
        fig.addEventListener('click', function (ev) { var t = ev.target.closest && ev.target.closest('[data-c]'); if (t) { tip.hidden = true; if (before) before(t); pick(t.getAttribute('data-c')); } });
        fig.addEventListener('keydown', function (ev) { var t = ev.target.closest && ev.target.closest('[data-c]'); if (t && (ev.key === 'Enter' || ev.key === ' ')) { ev.preventDefault(); if (before) before(t); pick(t.getAttribute('data-c')); } });
      }
      function tipHtml(c, rooms, x) { return '<b>' + esc(c.n) + ', ' + rooms + ' חדרים</b><span>' + F.ils(c.price) + ' · ' + F.ils(c.rent) + ' בחודש</span>' + 'תשואה ברוטו ' + pct(c.gross, 2) + '<br>שכר הדירה קונה ' + pct(c.be, 1) + ' מהדירה<br>' + signed(c.cf0) + ' בחודש אחרי ההחזר' + (c.n8 <= 4 ? '<br>מעט עסקאות: ' + c.n8 + ' מתוך 8 רבעונים' : ''); }

      function extras(v) {
        if (!api) return;
        var B0 = v.mode === 'budget' && X && X.B ? X.B : null;
        [].forEach.call(host.querySelectorAll('.nli__lines dd, .nli__scen strong'), function (e) { var t = e.textContent; e.classList.toggle('is-w', /[\u0590-\u05FF]/.test(t)); e.classList.toggle('is-pos', /^(נשארים|עלה)/.test(t)); e.classList.toggle('is-neg', /^חסרים/.test(t)); });
        if (v.mode !== lastMode) { var tb = host.querySelector('.nli__table'); if (tb) tb.open = v.mode === 'budget'; lastMode = v.mode; } var city = v.mode !== 'budget', rooms = city ? v.rooms : (v.brooms === '34' ? 4 : +v.brooms);
        if (B0 && v.brooms === '34') { var c3 = B0.fit.filter(function (c) { return c.rooms === 3; }).length, c4 = B0.fit.length - c3; rooms = c3 > c4 ? 3 : 4; }
        var R = ranking(D, rooms, v), me = city ? v.city : '', fit = {};
        if (!city && X && X.B) X.B.fit.forEach(function (c) { if (c.rooms === rooms) fit[c.n] = 1; });
        var dim = !city && Object.keys(fit).length > 0;  // budget mode dims the cities that do not fit, only when some do
        var natP = pairOf(nat, rooms, 'gov'), natX = natP ? calc(Object.assign({}, v, { price: natP.price, rent: natP.rent, other: 0 }), D) : null;
        var ltv = Math.max(0, v.ltv) / 100, rate = rateOf(v, L), W = Math.max(300, Math.min(900, (xs.clientWidth || host.clientWidth || 680) - 18));
        var key = [v.mode, v.city, rooms, v.price, v.rent, v.ltv, rate, v.years, v.track, v.mgmt, v.upkeep, v.empty, v.taxtrack, v.other, v.lawyer, v.broker, v.reno, v.equity, v.cap, v.brooms, showAll, budAll, W].join('|');
        if (key === lastKey) return; lastKey = key;
        /* 0. budget mode: the median flats that fit, by monthly cash flow (or the nearest ones, by the money missing) */
        var bu = xs.querySelector('.nliv-budS');
        if (B0) {
          var has = !!B0.fit.length, L2 = has ? B0.fit : B0.near, sh = budAll ? L2 : L2.slice(0, 12), bw = W, blw = W < 480 ? 128 : 170, bvw = W < 480 ? 104 : 128, bx0 = bw - blw;
          var bmax = Math.max.apply(null, L2.map(function (c) { return has ? Math.abs(c.cf1) : c.gap; }).concat([1])), bsx = (bx0 - bvw - 6) / bmax, bh = 26, BH = 8 + sh.length * bh + 4, bg = '';
          sh.forEach(function (c, i) { var y = 6 + i * bh, val = has ? c.cf1 : -c.gap, w = Math.max(2, Math.abs(val) * bsx), col = val >= 0 ? '#00806A' : '#B8322A';
            bg += '<g class="row" data-c="' + esc(c.n) + '" data-r="' + c.rooms + '" tabindex="0" role="button" aria-label="' + esc(c.n + ', ' + c.rooms + ' חדרים: ' + (has ? signed(c.cf1) + ' בחודש' : 'חסרים ' + F.ils(c.gap) + ' הון עצמי')) + '"><rect class="hit" x="0" y="' + (y + 1) + '" width="' + bw + '" height="' + (bh - 2) + '" fill="transparent"/>' +
              '<text x="' + (bw - 4) + '" y="' + (y + 17) + '" text-anchor="end">' + rtl(esc(c.n) + ', ' + c.rooms + ' חדרים' + (c.n8 <= 4 ? ' ◦' : '')) + '</text>' +
              '<rect x="' + (bx0 - w) + '" y="' + (y + 6) + '" width="' + w + '" height="' + (bh - 12) + '" rx="2" fill="' + col + '"' + (c.n8 <= 4 ? ' fill-opacity=".55"' : '') + '/>' +
              '<text class="vw" x="' + (bx0 - w - 6) + '" y="' + (y + 17) + '" text-anchor="end">' + rtl(has ? signed(c.cf1) : 'חסרים ' + F.ils(c.gap)) + '</text></g>'; });
          bu.innerHTML = '<h3 class="nliv-h">' + (has ? (v.equity > 0 ? 'מה ' + F.ils(v.equity) + ' הון עצמי קונים: ' : 'דירות עד ' + F.ils(v.cap) + ': ') + B0.fit.length + ' דירות בחציון, מהתזרים הטוב לחלש' : 'הכי קרוב: כמה הון עצמי חסר') + '</h3>' +
            '<p class="nliv-sub">' + (has ? 'שכר הדירה החציוני פחות ההחזר' + ((v.mgmt || 0) + (v.upkeep || 0) + (v.empty || 0) ? ', ההוצאות והחודשים הריקים שלכם' : '') + ', בחודש, לפני מס. ' : 'אף דירה בחציון של עיר לא נכנסת בסכום הזה. ') + 'כל שורה פותחת את העיר במחשבון. החישוב שלנו.</p>' +
            '<div class="nliv-fig" data-fig="budget"><svg viewBox="0 0 ' + bw + ' ' + BH + '" role="img" aria-label="' + esc(has ? 'הדירות שנכנסות בתקציב, לפי התזרים' : 'הערים הקרובות ביותר') + '">' + bg + '</svg></div>' +
            (L2.length > 12 ? '<button type="button" class="nliv-more">' + (budAll ? 'פחות' : 'כל ' + L2.length + ' הדירות') + '</button>' : '');
          bu.hidden = false; var bb = bu.querySelector('.nliv-more'); if (bb) bb.onclick = function () { budAll = !budAll; lastKey = ''; extras(api.state.v); };
          wire(bu.querySelector('.nliv-fig'), function (n, k, el) { var r = +(el && el.getAttribute('data-r')), c = L2.filter(function (x) { return x.n === n && (!r || x.rooms === r); })[0]; return c ? tipHtml(c, c.rooms) + '<br>הון עצמי נדרש ' + F.ils(c.equity) : ''; }, function (el) { var r = +el.getAttribute('data-r'); if (r) api.state.v.rooms = r; });
        } else { bu.innerHTML = ''; bu.hidden = true; }
        /* 1. the three rental-tax tracks, on this flat's rent */
        var ts = xs.querySelector('.nliv-taxs');
        if (city && X && X.x) {
          var T = X.x.T, RT = L.rentTax, yr = +(v.sign || today()).slice(0, 4);
          var ex = T.full ? 'אין מס, פטור מלא' : T.exempt > 0 ? F.ils(T.taxable) + ' בחודש חייבים במס שולי' : 'אין פטור: ' + F.ils(T.total) + ' חייבים';
          ts.innerHTML = '<h3 class="nliv-h">שלושת מסלולי המס על שכר הדירה</h3><p class="nliv-sub">על שכר דירה של ' + F.ils(v.rent) + (v.other ? ' ועוד ' + F.ils(v.other) + ' מדירות אחרות' : '') + ' בחודש. המבחן חודשי, על כל שכר הדירה ממגורים שלכם יחד.</p>' +
            '<div class="nli__tw"><table class="nliv-tax"><tbody>' +
            '<tr' + (T.full ? ' class="is-best"' : '') + '><th scope="row">פטור' + (T.full ? '<span class="nliv-best">הזול ביותר</span>' : '') + '</th><td class="n">' + ex + '</td><td>עד ' + F.ils(RT.ceiling) + ' בחודש אין מס. מעל זה הפטור קטן שקל מול שקל ונעלם ב־' + F.ils(RT.zero) + '.<small>תקרת ' + RT.years.join(', ') + '.</small></td></tr>' +
            '<tr><th scope="row">10%</th><td class="n">' + F.ils(T.ten) + ' בחודש · ' + F.ils(12 * T.ten) + ' בשנה</td><td>10% משכר הדירה, בלי הוצאות ובלי פחת. משלמים פעם בשנה, עד 30 יום מתום שנת המס: על ' + yr + ' עד 30.1.' + (yr + 1) + '.<small>במכירה בעתיד מוסיפים לחישוב מס השבח את הפחת שאפשר היה לדרוש.</small></td></tr>' +
            '<tr><th scope="row">מס שולי</th><td class="n">לפי ההכנסה שלכם</td><td>מורידים את ההוצאות ואת הפחת, ומשלמים לפי המדרגות: מ־' + F.num(100 * RT.under60) + '% עד גיל 60, מ־' + F.num(100 * RT.over60) + '% מגיל 60.<small>חישוב אישי, ולכן בלי סכום כאן.</small></td></tr>' +
            '</tbody></table></div>' + (!T.full && T.total < RT.zero ? '<p class="nliv-sub" style="margin-top:8px">בין ' + F.ils(RT.ceiling) + ' ל־' + F.ils(RT.zero) + ' בחודש משווים את המס השולי על החלק החייב מול 10% על הכול.</p>' : '');
          ts.hidden = false;
        } else { ts.innerHTML = ''; ts.hidden = true; }
        /* 2. the board: how much of the flat the rent buys, city by city, against the loan cap and the national line */
        var bs = xs.querySelector('.nliv-boardS'), show = R;
        if (!showAll) { show = R.slice(0, 15).concat(R.length > 20 ? R.slice(-5) : R.slice(15)); var mi = R.filter(function (c) { return c.n === me || fit[c.n]; }); mi.forEach(function (c) { if (show.indexOf(c) < 0) show.push(c); }); show.sort(function (a, b) { return b.be - a.be; }); }
        var rh = 24, top = 30, lw = W < 480 ? 104 : 132, vw = 52, x0 = W - lw, maxV = Math.max(0.85, ltv + 0.05, R.length ? R[0].be + 0.03 : 0), sx = (x0 - vw - 6) / maxV;
        var gaps = 0; show.forEach(function (c, i) { if (!showAll && i > 0 && R.indexOf(c) - R.indexOf(show[i - 1]) > 1) gaps++; });
        var H = top + show.length * rh + gaps * 14 + 30, g = '', yo = 0;
        [0, 0.25, 0.5, 0.75].forEach(function (t) { if (t > maxV) return; var gx = x0 - t * sx; g += '<line x1="' + gx + '" x2="' + gx + '" y1="' + (top - 6) + '" y2="' + (H - 8) + '" stroke="#D3DCE2" stroke-width="1"/><text class="ax" x="' + gx + '" y="' + (top - 12) + '" text-anchor="middle">' + F.num(100 * t) + '%</text>'; });
        var gap = false;
        show.forEach(function (c, i) {
          if (!showAll && i > 0 && R.indexOf(c) - R.indexOf(show[i - 1]) > 1) { g += '<text class="ax" x="' + (W - 4) + '" y="' + (top + i * rh + yo + 11) + '" text-anchor="end">' + rtl('⋯ עוד ' + (R.indexOf(c) - R.indexOf(show[i - 1]) - 1) + ' ערים') + '</text>'; yo += 14; gap = true; }
          var y = top + i * rh + yo, w = Math.max(2, c.be * sx), pos = c.be > ltv, col = pos ? '#00806A' : '#B8322A', off = dim && !fit[c.n];
          g += '<g class="row' + (c.n === me ? ' is-me' : '') + (off ? ' is-off' : '') + '" data-c="' + esc(c.n) + '" data-k="b" tabindex="0" role="button" aria-label="' + esc(c.n + ': שכר הדירה קונה ' + pct(c.be, 1) + ' מהדירה') + '">' +
            '<rect class="hit" x="0" y="' + (y + 1) + '" width="' + W + '" height="' + (rh - 2) + '" fill="transparent"/>' +
            '<text x="' + (W - 4) + '" y="' + (y + 16) + '" text-anchor="end">' + rtl(esc(c.n) + (c.n8 <= 4 ? ' ◦' : '')) + '</text>' +
            '<rect x="' + (x0 - w) + '" y="' + (y + 5) + '" width="' + w + '" height="' + (rh - 10) + '" rx="2" fill="' + col + '"' + (c.n8 <= 4 ? ' fill-opacity=".55"' : '') + '/>' +
            (c.n === me ? '<rect x="' + (x0 - w - 2) + '" y="' + (y + 3) + '" width="' + (w + 4) + '" height="' + (rh - 6) + '" rx="3" fill="none" stroke="#12304F" stroke-width="2"/>' : '') +
            '<text class="v" x="' + (x0 - w - 6) + '" y="' + (y + 16) + '" text-anchor="end">' + pct(c.be, 1) + '</text></g>';
        });
        var cx = x0 - ltv * sx, yb = H - 26; g += '<line x1="' + cx + '" x2="' + cx + '" y1="' + (top - 6) + '" y2="' + (yb + 4) + '" stroke="#12304F" stroke-width="2"/><text x="' + (cx - 4) + '" y="' + (yb + 18) + '" text-anchor="end" style="fill:#12304F;font-weight:600">' + rtl('המימון שלכם ' + F.num(100 * ltv) + '%') + '</text>';
        if (natX) { var nx = x0 - natX.be * sx; g += '<line x1="' + nx + '" x2="' + nx + '" y1="' + top + '" y2="' + (yb + 4) + '" stroke="#5E6A75" stroke-width="1.5" stroke-dasharray="4 3"/>' + (Math.abs(nx - cx) > 8 ? '<text x="' + (nx + 4) + '" y="' + (yb + 18) + '" text-anchor="' + (nx > cx ? 'start' : 'end') + '" style="fill:#5E6A75">' + rtl('ישראל ' + pct(natX.be, 1)) + '</text>' : ''); }
        var nPos = R.filter(function (c) { return c.be > ltv; }).length;
        bs.innerHTML = '<h3 class="nliv-h">כמה מהדירה שכר הדירה קונה, עיר אחרי עיר</h3><p class="nliv-sub">' + rooms + ' חדרים, ' + qlab(D.cityQ) + '. משכנתא ' + F.num(100 * ltv) + '% לשנים ' + v.years + ' בריבית ' + F.num(rate, 2) + '%: שכר הדירה מכסה את ההחזר ב־' + nPos + ' מתוך ' + R.length + ' ערים' + (natX ? '; בחציון הארצי (' + qlab(natP.q) + ') ' + pct(natX.be, 1) : '') + '. החישוב שלנו.' + (dim ? ' מודגשות: הערים שנכנסות בתקציב.' : '') + '</p>' +
          '<div class="nliv-fig" data-fig="board"><svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc('כמה מהדירה שכר הדירה קונה ב־' + R.length + ' ערים, ' + rooms + ' חדרים') + '">' + g + '</svg></div>' +
          '<ul class="nliv-legend"><li><i style="background:#00806A"></i>שכר הדירה מכסה את ההחזר</li><li><i style="background:#B8322A"></i>צריך להוסיף כסף כל חודש</li><li><i class="l"></i>המימון שלכם</li>' + (natX ? '<li><i class="d"></i>החציון הארצי</li>' : '') + '<li><i style="background:#00806A;opacity:.55"></i>◦ מעט עסקאות: החציון פורסם בחצי מהרבעונים או פחות</li></ul>' +
          (R.length > show.length || showAll ? '<button type="button" class="nliv-more">' + (showAll ? 'פחות ערים' : 'כל ' + R.length + ' הערים') + '</button>' : '') + '<p class="nliv-picked" aria-live="polite">' + esc(city && picked.indexOf(v.city + '.') > -1 ? picked : '') + '</p>';
        var mb = bs.querySelector('.nliv-more'); if (mb) mb.onclick = function () { showAll = !showAll; lastKey = ''; extras(api.state.v); };
        wire(bs.querySelector('.nliv-fig'), function (n) { var c = R.filter(function (x) { return x.n === n; })[0]; return c ? tipHtml(c, rooms) : ''; });
        /* 3. the scatter: gross yield against price, every city, coloured by the same cash-flow sign */
        var ss = xs.querySelector('.nliv-scatS'), SH = W < 520 ? 300 : 360, ml = 46, mr = 12, mt = 14, mb2 = 40;
        var maxPr = Math.max.apply(null, R.map(function (c) { return c.price; }).concat([natP ? natP.price : 0])) * 1.05, maxY = Math.max(0.055, Math.max.apply(null, R.map(function (c) { return c.gross; })) + 0.004), minY = 0.015;
        var px = function (p) { return ml + p / maxPr * (W - ml - mr); }, py = function (y) { return mt + (maxY - y) / (maxY - minY) * (SH - mt - mb2); }, s2 = '';
        for (var t = 0.02; t <= maxY + 1e-9; t += 0.01) s2 += '<line x1="' + ml + '" x2="' + (W - mr) + '" y1="' + py(t) + '" y2="' + py(t) + '" stroke="#E3E9ED"/><text class="ax" x="' + (ml - 6) + '" y="' + (py(t) + 4) + '" text-anchor="end">' + F.num(100 * t) + '%</text>';
        var stp = maxPr > 6e6 ? 2e6 : 1e6; for (var pp = 0; pp <= maxPr; pp += stp) s2 += '<text class="ax" x="' + px(pp) + '" y="' + (SH - mb2 + 16) + '" text-anchor="middle">' + (pp ? F.num(pp / 1e6, 0) + 'M' : '0') + '</text>';
        s2 += '<text x="' + ((ml + W - mr) / 2) + '" y="' + (SH - 6) + '" text-anchor="middle">' + rtl('מחיר הדירה החציוני, במיליוני שקלים') + '</text>';
        var mine = null;
        R.slice().sort(function (a, b) { return (a.n === me) - (b.n === me); }).forEach(function (c) {
          var col = c.be > ltv ? '#00806A' : '#B8322A', off = dim && !fit[c.n], isMe = c.n === me;
          if (isMe) mine = c;
          s2 += '<circle class="dot' + (c.n8 <= 4 ? ' is-thin' : '') + (off ? ' is-off' : '') + '" data-c="' + esc(c.n) + '" data-k="s" tabindex="0" role="button" aria-label="' + esc(c.n + ': תשואה ' + pct(c.gross, 2) + ', ' + F.ils(c.price)) + '" cx="' + px(c.price).toFixed(1) + '" cy="' + py(c.gross).toFixed(1) + '" r="' + (isMe ? 7 : 5) + '" fill="' + col + '"' + (c.n8 <= 4 ? ' style="stroke:' + col + '"' : '') + '/>';
        });
        if (natX) { var nxp = px(natP.price), nyp = py(natX.gross); s2 += '<path d="M' + (nxp - 6) + ' ' + nyp + 'h12M' + nxp + ' ' + (nyp - 6) + 'v12" stroke="#12304F" stroke-width="2.5"/><text x="' + (nxp + 9) + '" y="' + (nyp + 4) + '" style="fill:#12304F;font-weight:600;paint-order:stroke;stroke:#fff;stroke-width:4px">' + rtl('ישראל') + '</text>'; }
        if (mine) { var mx = px(mine.price), my = py(mine.gross), right = mx > W * 0.6; s2 += '<circle cx="' + mx + '" cy="' + my + '" r="11" fill="none" stroke="#12304F" stroke-width="2"/><text x="' + (right ? mx - 15 : mx + 15) + '" y="' + (my - 10) + '" text-anchor="' + (right ? 'end' : 'start') + '" style="fill:#12304F;font-weight:600;paint-order:stroke;stroke:#fff;stroke-width:4px">' + rtl(esc(mine.n) + ' ' + pct(mine.gross, 2)) + '</text>'; }
        ss.innerHTML = '<h3 class="nliv-h">תשואה ברוטו מול מחיר הדירה</h3><p class="nliv-sub">' + rooms + ' חדרים, ' + qlab(D.cityQ) + ': ככל שהדירה זולה יותר, התשואה ברוטו גבוהה יותר. אותו צבע כמו בדירוג: ירוק כשהשכירות מכסה את ההחזר, אדום כשלא. החישוב שלנו.</p>' +
          '<div class="nliv-fig" data-fig="scatter"><svg viewBox="0 0 ' + W + ' ' + SH + '" role="img" aria-label="' + esc('תשואה ברוטו מול מחיר ב־' + R.length + ' ערים') + '">' + s2 + '</svg></div>' +
          '<ul class="nliv-legend"><li><i class="c" style="background:#00806A"></i>שכר הדירה מכסה את ההחזר</li><li><i class="c" style="background:#B8322A"></i>צריך להוסיף כסף כל חודש</li><li><i class="c" style="border:2px solid #5E6A75;background:#fff"></i>מעט עסקאות</li></ul>';
        wire(ss.querySelector('.nliv-fig'), function (n) { var c = R.filter(function (x) { return x.n === n; })[0]; return c ? tipHtml(c, rooms) : ''; });
        xs.querySelector('.nliv-limits').innerHTML = '<b>מה המספרים האלה ומה לא:</b> חציונים של רבעון אחד מאתר הנדל״ן הממשלתי, קבצים מ־' + F.date(D.src.gov.fileDate || D.built) + ', שכר דירה ומחיר מאותו רבעון. התשואה ברוטו, לפני הוצאות, חודשים ריקים ומס. כל דירה שונה מהחציון של העיר, והחישוב לא מחליף בדיקה של הדירה, של המימון ושל המס עם אנשי מקצוע. זה מידע, לא ייעוץ השקעות. עודכן ' + F.date(D.built) + '.';
      }

      api = NI.mount(host, spec(), D0);
      var grid = host.querySelector('.nli__grid'); if (grid && grid.parentNode) grid.parentNode.insertBefore(xs, grid.nextSibling);
      lastKey = ''; extras(api.state.v);
      var rt = 0; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { extras(api.state.v); }, 150); });
    }
  });
})();
