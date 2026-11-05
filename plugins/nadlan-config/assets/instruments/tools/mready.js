/* NadLan Instruments · mready v1 "מוכנים לאישור עקרוני?" (HAD-675, /mortgage-calculator/ panel 6 of the design board Tools.dc.html).
   Five quick questions (how the household earns, one or two borrowers, net income and existing loan payments, where the equity
   comes from, the home: buyer type, contractor or second hand, price) and two answers:
   1. a readiness card against the Bank of Israel limits of directive 329 (boim.rules, or the snapshot in mready.json): the first
      payment against the disposable income (income less existing loan payments, the definition of tools/mortgage.js on the same
      page): up to 40% passes, 40% to 50% passes with the capital note, above 50% fails; the LTV cap by buyer type (75 / 70 / 50,
      oleh 75 and foreign resident 50 from cost.json); the equity against the down payment PLUS the purchase tax (ptax.json, the
      oleh cap as in afford.js) and the lawyer with VAT (cost.json); and the documents for the approval in principle. The highest
      price that passes is window.NLAF.compute (tools/afford.js), fed with the disposable income and the one equivalent rate
      that reproduces the first payment of the Bank of Israel all-banks average mix of the latest month (boim.by_bank, the same
      calibration as mbudget: 1,000,000 over 25 years = 5,428 a month in 9.2026);
   2. a PERSONAL documents list by profile (mready.json docs: every item sourced and dated, 'some' = יש בנקים שמבקשים), split
      into the approval in principle and the mortgage itself, as a checklist kept only in the page (ticks only, optional
      localStorage in try/catch; no income or amount is stored or sent), printable and copyable as text.
   No lead form: one plain link to /mortgage-advisor/. Pure logic in window.NLMRD (DOM free, test_mready.js in node). Hebrew only
   (RTL); no long dash, no spaced hyphen in any visible string. */
(function () {
  'use strict';
  var W = typeof window !== 'undefined' ? window : globalThis;
  var HAS_DOC = typeof document !== 'undefined';
  // on the site afford.js sits next to this file in tools/; if the page did not load it, it is loaded from there before the first run
  var ME = HAS_DOC && document.currentScript ? document.currentScript.src : '';
  var AFF = ME ? ME.replace(/[^\/]*\.js(\?.*)?$/, 'afford.js$1') : '';

  /* =========================================================================================================== the math */
  var TRK = ['fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi'];
  var EQ = ['savings', 'gift', 'sale', 'grant'];
  function num(x) { var n = +x; return isFinite(n) ? n : 0; }
  function mrate(e) { return Math.pow(1 + e / 100, 1 / 12) - 1; }  // effective annual % to a monthly rate
  function pmt(L, r, n) { return r === 0 ? L / n : L * r / (1 - Math.pow(1 + r, -n)); }
  function brackets(price, br) { var t = 0, lo = 0; for (var i = 0; i < br.length; i++) { var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(price, hi); if (top > lo) t += (top - lo) * br[i][1]; if (price <= hi) break; lo = hi; } return t; }
  function ptax(price, P, k) { var br = k === 'oleh' && P.oleh_cap && price > P.oleh_cap ? P.tracks.single : P.tracks[k]; return brackets(price, br); }  // the oleh cap of afford.js
  function sysRow(boim) {
    var t = boim && boim.by_bank && boim.by_bank.latest && boim.by_bank.latest.table;
    if (!t) return null;
    for (var i = 0; i < t.length; i++) if (t[i].bank === 'system') return t[i];
    return null;
  }
  /** The first payment of 1,000,000 over n months in the all-banks average mix (each track its share at its own monthly rate);
      without the by-bank file, the official average fixed not linked rate (nominal, as afford.js takes it). */
  function perMillion(boim, n) {
    var row = sysRow(boim);
    if (row) { var sh = 0, tot = 0; TRK.forEach(function (k) { sh += num(row[k] && row[k].share); });
      if (sh > 0) { TRK.forEach(function (k) { if (row[k]) tot += pmt(1e6 * row[k].share / sh, mrate(+row[k].rate), n); }); return { perM: tot, basis: 'mix', month: boim.by_bank.latest.month }; } }
    var r = boim && boim.rates && boim.rates.fixed_nl ? +boim.rates.fixed_nl.rate : 4.62;
    var hist = boim && boim.rates && boim.rates.fixed_nl && boim.rates.fixed_nl.hist;
    return { perM: pmt(1e6, r / 1200, n), basis: 'fixed', rate: r, month: hist && hist.length ? hist[hist.length - 1][0] : null };
  }
  /** The one nominal annual rate (%) whose Spitzer payment equals perM per million over n months (what NLAF.compute takes). */
  function eqRate(perM, n) {
    if (perM <= 1e6 / n) return 0;
    var lo = 0, hi = 0.05;
    for (var i = 0; i < 200; i++) { var mid = (lo + hi) / 2; if (pmt(1e6, mid, n) < perM) lo = mid; else hi = mid; }
    return (lo + hi) / 2 * 1200;
  }
  function rulesOf(D) { return (D.boim && D.boim.rules) || (D.mready && D.mready.rules); }
  var PTAX = { single: 'single', replace: 'single', extra: 'extra', oleh: 'oleh', foreign: 'foreign' };
  function ltvOf(buyer, D) {
    var R = rulesOf(D).ltv, C = (D.cost && D.cost.ltv) || {};
    if (buyer === 'replace') return R.replace;
    if (buyer === 'extra') return R.invest;
    if (buyer === 'oleh') return C.oleh != null ? C.oleh : R.single;
    if (buyer === 'foreign') return C.foreign != null ? C.foreign : 0.5;
    return R.single;
  }
  function equityOf(inp) { return EQ.reduce(function (s, k) { return s + Math.max(0, num(inp[k])); }, 0); }

  /** inp: {type, borrowers, income, loans, savings, gift, sale, grant, buyer, market, price, years}; D: {boim, ptax, cost, mready}. */
  function model(inp, D) {
    var R = rulesOf(D), C = D.cost, P = D.ptax;
    var buyer = PTAX[inp.buyer] ? inp.buyer : 'single', k = PTAX[buyer];
    var years = Math.min(R.term_max || 30, Math.max(4, Math.round(num(inp.years) || 25))), n = years * 12;
    var price = Math.max(0, num(inp.price)), income = Math.max(0, num(inp.income)), loans = Math.max(0, num(inp.loans));
    var equity = equityOf(inp), ltv = ltvOf(buyer, D);
    var tax = ptax(price, P, k);
    var lawyerPct = C.lawyer && C.lawyer.from != null ? +C.lawyer.from : 0.5;
    var lawyer = lawyerPct / 100 * (1 + C.vat) * price;
    var down = price * (1 - ltv), need = down + tax + lawyer;
    var loanNeed = Math.max(0, price + tax + lawyer - equity), loanCap = ltv * price, loan = Math.min(loanNeed, loanCap);
    var PM = perMillion(D.boim, n), payment = loan * PM.perM / 1e6, disp = income - loans;
    var pti = loan <= 0 ? 0 : disp > 0 ? payment / disp : Infinity;
    var checks = [];
    checks.push({ id: 'pti', state: loan <= 0 ? 'pass' : pti > R.pti_max + 1e-9 ? 'fail' : pti > R.pti_risk + 1e-9 ? 'warn' : 'pass', pti: pti, none: loan <= 0 });
    checks.push({ id: 'ltv', state: equity + 0.5 >= down ? 'pass' : 'fail', short: Math.max(0, down - equity), share: price > 0 ? loan / price : 0, needShare: price > 0 ? Math.max(0, price - equity) / price : 0 });
    checks.push({ id: 'equity', state: equity + 0.5 >= need ? 'pass' : 'fail', short: Math.max(0, need - equity) });
    var rate = eqRate(PM.perM, n), max = {};
    if (W.NLAF && disp > 0) {
      var C2 = JSON.parse(JSON.stringify(C)); C2.ltv[k] = ltv;  // a replacement buyer: single-home brackets, the 70% cap
      [R.pti_risk, R.pti_max].forEach(function (x) {
        var r = W.NLAF.compute({ income: disp, loans: 0, equity: equity, track: k, ratio: 100 * x, rate: rate, years: years, lawyer: lawyerPct }, P, C2);
        max[Math.round(100 * x)] = r.price;
      });
    }
    return { buyer: buyer, k: k, years: years, n: n, price: price, income: income, loans: loans, disp: disp, equity: equity, ltv: ltv,
      tax: tax, lawyer: lawyer, lawyerPct: lawyerPct, vat: C.vat, down: down, need: need, loanNeed: loanNeed, loan: loan, payment: payment,
      pti: pti, perM: PM.perM, basis: PM.basis, month: PM.month, rate: rate, max: max, checks: checks, rules: R };
  }

  /* ------------------------------------------------------------------------------------------------------- the documents */
  function has(inp, k) { return num(inp[k]) > 0; }
  function test(w, inp) {
    if (!w) return true;
    if (w.any && !w.any.some(function (x) { return test(x, inp); })) return false;
    if (w.type && w.type.indexOf(inp.type) < 0) return false;
    if (w.buyer && w.buyer.indexOf(inp.buyer) < 0) return false;
    if (w.market && w.market.indexOf(inp.market) < 0) return false;
    if (w.loans && !(num(inp.loans) > 0)) return false;
    if (w.equity && !w.equity.some(function (k) { return has(inp, k); })) return false;
    if (w.noequity && w.noequity.some(function (k) { return has(inp, k); })) return false;
    return true;
  }
  function perText(per, inp) {
    if (+inp.borrowers !== 2 || !per) return '';
    if (per === 'salaried' && inp.type === 'both') return 'ללווה השכיר';
    if (per === 'self' && inp.type === 'both') return 'ללווה העצמאי';
    return 'לכל אחד מהלווים';
  }
  /** The documents of this profile, in the order of mready.json, with the per-borrower words resolved. */
  function docsFor(inp, M) {
    return M.docs.filter(function (d) { return test(d.when, inp); }).map(function (d) {
      return { id: d.id, stage: d.stage, text: d.text, cond: d.cond || '', per: perText(d.per, inp), some: d.level === 'some', core: d.stage === 'aip' && d.level === 'common' && !d.cond, src: d.src };
    });
  }
  /** Short names of the groups behind an item (Discount and Mercantile are one group, every Leumi page one group). */
  function groupsOf(src, M) { var g = []; src.forEach(function (s) { var x = M.sources[s] && M.sources[s].group; if (x && g.indexOf(x) < 0) g.push(x); }); return g.map(function (x) { return M.short[x] || x; }); }
  function line(d) { return (d.cond ? d.cond + ': ' : '') + d.text + (d.per ? ', ' + d.per : '') + (d.some ? ' (יש בנקים שמבקשים)' : ''); }

  /* --------------------------------------------------------------------------------------------------------- the words */
  var nf0 = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function ils(x) { return '₪' + nf0.format(Math.round(x || 0)); }
  function pc(x, d) { return new Intl.NumberFormat('he-IL', { minimumFractionDigits: d == null ? 1 : d, maximumFractionDigits: d == null ? 1 : d }).format(100 * x) + '%'; }
  function ymon(key) { var p = String(key || '').split('-'); return p.length > 1 ? (+p[1]) + '.' + p[0] : ''; }
  var BUYER_IN = { single: 'בדירה יחידה', replace: 'בדירה חליפית', extra: 'בדירה נוספת', oleh: 'לעולה חדש', foreign: 'לתושב חוץ' };
  var LAB = { pti: 'יחס החזר מההכנסה', ltv: 'שיעור מימון', equity: 'הון עצמי מול מס ועלויות', docs: 'המסמכים לאישור העקרוני' };
  var STATE = { pass: 'עובר', warn: 'עובר, מעל 40%', fail: 'לא עובר', todo: 'להשלים', done: 'מוכנים' };
  function checkText(c, m) {
    var R = m.rules, ref329 = m.buyer === 'foreign' ? '' : ' (הוראה 329, סעיף 2)';
    if (c.id === 'pti') {
      if (c.none) return 'ההון העצמי מכסה את כל העסקה: אין צורך במשכנתא.';
      if (!isFinite(c.pti)) return 'ההחזרים של ההלוואות הקיימות גבוהים מההכנסה: אין הכנסה פנויה להחזר.';
      if (c.state === 'fail') return 'ההחזר הוא ' + pc(c.pti) + ' מההכנסה הפנויה. בנק ישראל לא מתיר לבנק לאשר משכנתא שההחזר בה עולה על ' + pc(R.pti_max, 0) + ' (הוראה 329, סעיף 5).';
      if (c.state === 'warn') return 'ההחזר הוא ' + pc(c.pti) + ' מההכנסה הפנויה: מתחת ל־' + pc(R.pti_max, 0) + ' המותרים ומעל ' + pc(R.pti_risk, 0) + '. על משכנתא כזו הבנק נדרש להחזיק יותר הון (הוראה 329, נספח א).';
      return 'ההחזר הוא ' + pc(c.pti) + ' מההכנסה הפנויה, עד ' + pc(R.pti_risk, 0) + ' (הוראה 329, סעיפים 5 ו־6).';
    }
    if (c.id === 'ltv') {
      if (c.state === 'fail') return 'נדרש מימון של ' + pc(c.needShare) + ' ממחיר הדירה, ' + BUYER_IN[m.buyer] + ' הבנק מממן עד ' + pc(m.ltv, 0) + ref329 + '. המקדמה היא ' + ils(m.down) + ' וחסרים לה ' + ils(c.short) + '.';
      return 'המשכנתא היא ' + pc(c.share) + ' ממחיר הדירה. ' + BUYER_IN[m.buyer] + ' הבנק מממן עד ' + pc(m.ltv, 0) + ref329 + '.';
    }
    var tx = m.tax >= 1 ? 'מס רכישה של ' + ils(m.tax) : 'בלי מס רכישה במחיר הזה';
    if (c.state === 'fail') return 'חסרים ' + ils(c.short) + '. ' + (m.tax >= 1 ? 'מס הרכישה (' + ils(m.tax) + ') ועורך הדין (' + ils(m.lawyer) + ')' : 'עורך הדין (' + ils(m.lawyer) + ')') + ' משולמים מההון העצמי, לא מהמשכנתא.';
    return 'ההון העצמי מכסה את המקדמה, ' + tx + ' ועורך דין של ' + ils(m.lawyer) + ' כולל מע״מ.';
  }
  /** The fourth check: the core documents for the approval in principle, all ticked. */
  function docsCheck(list, ticks) {
    var core = list.filter(function (d) { return d.core; }), done = core.filter(function (d) { return ticks[d.id]; }).length;
    return { id: 'docs', state: core.length && done === core.length ? 'done' : 'todo', done: done, total: core.length };
  }
  function score(m, dc) { return m.checks.filter(function (c) { return c.state !== 'fail'; }).length + (dc.state === 'done' ? 1 : 0); }
  /** The plain text of the case and the list: copied, shared, kept. */
  function copyText(inp, m, list, ticks, M) {
    var dc = docsCheck(list, ticks), s = score(m, dc), out = [];
    out.push('מוכנים לאישור עקרוני? ' + s + ' מתוך 4');
    m.checks.forEach(function (c) { out.push(LAB[c.id] + ': ' + STATE[c.state] + '. ' + checkText(c, m)); });
    out.push(LAB.docs + ': ' + STATE[dc.state] + ' (' + dc.done + ' מתוך ' + dc.total + ')');
    out.push('דירה ' + ils(m.price) + ', הון עצמי ' + ils(m.equity) + ', משכנתא ' + ils(m.loan) + ', החזר ראשון ' + ils(m.payment) + ' בחודש ל־' + m.years + ' שנה.');
    ['aip', 'loan'].forEach(function (st) {
      out.push(''); out.push(M.stages[st].label + ':');
      list.filter(function (d) { return d.stage === st; }).forEach(function (d) { out.push((ticks[d.id] ? '[x] ' : '[ ] ') + line(d)); });
    });
    out.push(''); out.push('מקורות: הוראה 329 של בנק ישראל; רשימות המסמכים של הפועלים, לאומי, מזרחי טפחות, דיסקונט ומרכנתיל, הבינלאומי ובנק ירושלים, כל זכות ובנק ישראל, נבדקו ב־' + fdate(M.checked) + '.');
    return out.join('\n');
  }
  function fdate(iso) { var p = String(iso).split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : iso; }

  W.NLMRD = { model: model, docsFor: docsFor, docsCheck: docsCheck, score: score, copyText: copyText, checkText: checkText, groupsOf: groupsOf,
    line: line, test: test, ptax: ptax, perMillion: perMillion, eqRate: eqRate, ltvOf: ltvOf, equityOf: equityOf, pmt: pmt, LAB: LAB, STATE: STATE };
  if (!W.NadLanInstruments || !HAS_DOC) return;

  /* ============================================================================================================== the page */
  var NI = W.NadLanInstruments, esc = NI.esc;
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function parse(v) { var n = parseFloat(String(v == null ? '' : v).replace(/[^\d.\-]/g, '')); return isFinite(n) ? n : NaN; }
  var LS = 'nlmr:ticks:v1';
  function loadTicks() { try { var s = W.localStorage && W.localStorage.getItem(LS); var o = s ? JSON.parse(s) : {}; return o && typeof o === 'object' ? o : {}; } catch (e) { return {}; } }
  function saveTicks(t) { try { if (W.localStorage) W.localStorage.setItem(LS, JSON.stringify(t)); } catch (e) { /* private window or blocked storage: the ticks stay in the page */ } }
  var CHECK_SVG = 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M4.5 10.5l3.5 3.5 7.5-8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="square"/></svg>');

  function css() {
    if (document.getElementById('nlmr-css')) return;
    var s = document.createElement('style'); s.id = 'nlmr-css';
    s.textContent = [
      '.nlmr__grid{display:grid;grid-template-columns:minmax(0,1fr);gap:20px;position:relative}',
      '@media (min-width:1000px){.nlmr__grid{grid-template-columns:minmax(0,460px) minmax(0,1fr);gap:32px;align-items:start}.nlmr__out{position:sticky;top:var(--nlmr-top,12px)}}',
      '.nlmr__form{display:grid;gap:14px;margin:0;min-width:0}',
      'html body .nli fieldset.nlmr__q{border:1px solid var(--nli-line);border-radius:var(--nli-r-m);padding:12px 14px 14px;margin:0;display:grid;gap:12px;min-width:0;background:var(--nli-surface)}',
      'html body .nli .nlmr__q legend{font:600 15px/22px var(--nli-sans);color:var(--nli-ink);padding:0 6px;margin:0 -6px;display:flex;gap:8px;align-items:center}',
      '.nlmr__q legend b{font:500 12px/20px var(--nli-mono);color:#fff;background:var(--nli-ink);border-radius:2px;min-width:22px;text-align:center;display:inline-block}',
      '.nlmr__two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px}',
      '.nlmr__two .nli__f>label{font-size:12px}',
      'html body .nli .nlmr__q .nli__in input{font-size:16px}',
      '.nlmr__sum{margin:0;font:500 14px/20px var(--nli-sans);color:var(--nli-ink)}.nlmr__sum bdi{font-family:var(--nli-mono)}',
      'html body .nli .nlmr__q .nli__seg button{padding:10px 12px}',
      'html body .nli .nlmr .nli__pre small{font-family:var(--nli-sans);direction:rtl;text-align:right;unicode-bidi:normal}',
      '.nlmr__out{display:grid;gap:14px;align-content:start;min-width:0}',
      '.nlmr__card{border:1px solid var(--nli-sea);border-radius:var(--nli-r-m);background:var(--nli-surface);padding:16px}',
      '.nlmr__card .nli__alab{display:flex;gap:8px;align-items:center}',
      '.nlmr__eg{font:500 11px/16px var(--nli-sans);color:var(--nli-ink);border:1px solid var(--nli-line);border-radius:999px;padding:0 8px}',
      '.nlmr__fig{display:inline-flex;align-items:baseline;gap:10px;margin:6px 0 12px;padding:0 0 6px;border-bottom:2px solid var(--nli-survey);color:var(--nli-ink)}',
      '.nlmr__n{font:500 44px/48px var(--nli-mono);font-variant-numeric:tabular-nums}.nlmr__w{font:500 22px/28px var(--nli-sans);color:var(--nli-ink2)}',
      '.nlmr__fig.is-all{border-bottom-color:var(--nli-sea)}',
      '.nlmr__checks{list-style:none;margin:0;padding:0;display:grid;gap:0}',
      '.nlmr__checks li{margin:0;padding:10px 0;border-top:1px solid var(--nli-line);display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 10px;align-items:start}',
      '.nlmr__mk{width:12px;height:12px;margin-top:5px;border-radius:2px;background:var(--nli-open);grid-row:span 2}',
      '.is-warn .nlmr__mk{background:var(--nli-ink)}.is-fail .nlmr__mk{background:var(--nli-survey)}.is-todo .nlmr__mk{background:none;border:2px solid var(--nli-sea);width:12px;height:12px}',
      '.nlmr__ck{display:flex;justify-content:space-between;gap:12px;font:500 14px/22px var(--nli-sans);color:var(--nli-ink)}',
      '.nlmr__ck b{font-weight:600;white-space:nowrap}.is-fail .nlmr__ck b{color:var(--nli-survey)}',
      '.nlmr__ct{margin:0;font:400 13px/20px var(--nli-sans);color:var(--nli-ink2)}',
      '.nlmr__ct bdi,.nlmr__lines dd bdi{font-family:var(--nli-mono)}',
      'html body .nli .nlmr .nli__lines dd{white-space:nowrap;max-width:none}html body .nli .nlmr .nli__lines dt{min-width:0}',
      'html body .nli a.nlmr__adv{display:flex;align-items:center;justify-content:center;min-height:48px;padding:10px 16px;border-radius:var(--nli-r-s);background:var(--nli-sea);color:#fff !important;font:600 16px/22px var(--nli-sans);text-decoration:none !important}',
      'html body .nli a.nlmr__adv:hover{background:var(--nli-sea-deep)}',
      '.nlmr__docs{margin:28px 0 0;padding:20px 0 0;border-top:1px solid var(--nli-line);position:relative}',
      'html body .nli .nlmr h3.nlmr__h{font:600 22px/28px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 6px !important;letter-spacing:0;text-transform:none}',
      'html body .nli .nlmr h4.nlmr__h4{font:600 16px/24px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 4px !important;display:flex;justify-content:space-between;gap:12px;align-items:baseline}',
      '.nlmr__h4 small{font:500 13px/18px var(--nli-mono);color:var(--nli-mute);white-space:nowrap}',
      '.nlmr__p{font:400 14px/22px var(--nli-sans);color:var(--nli-ink2);margin:0 0 10px;max-width:72ch}',
      '.nlmr__stages{display:grid;gap:20px}@media (min-width:1000px){.nlmr__stages{grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}}',
      '.nlmr__list{list-style:none;margin:0;padding:0;display:grid;gap:0}',
      '.nlmr__list li{margin:0;border-top:1px solid var(--nli-line)}',
      'html body .nli .nlmr__list label{display:grid;grid-template-columns:24px minmax(0,1fr);gap:4px 12px;align-items:start;min-height:44px;padding:10px 0;cursor:pointer;margin:0;font:400 15px/22px var(--nli-sans);color:var(--nli-ink)}',
      'html body .nli .nlmr__list input[type=checkbox]{-webkit-appearance:none;appearance:none;width:24px;height:24px;margin:0;border:1.5px solid var(--nli-ink2);border-radius:2px;background:#fff center/18px 18px no-repeat;cursor:pointer;grid-row:span 2}',
      'html body .nli .nlmr__list input[type=checkbox]:checked{background-color:var(--nli-sea);border-color:var(--nli-sea);background-image:url("' + CHECK_SVG + '")}',
      'html body .nli .nlmr__list input[type=checkbox]:focus-visible{outline:2px solid var(--nli-focus);outline-offset:2px}',
      '.nlmr__list input:checked+span{color:var(--nli-ink2)}',
      '.nlmr__list em{font-style:normal;font-weight:600}',
      '.nlmr__tag{display:inline-block;font:500 11px/16px var(--nli-sans);color:var(--nli-ink2);border:1px dashed var(--nli-mute);border-radius:999px;padding:0 8px;margin-inline-start:6px;white-space:nowrap;vertical-align:1px}',
      '.nlmr__ds{grid-column:2;font:400 12px/16px var(--nli-mono);color:var(--nli-mute)}',
      '.nlmr__key{font:400 12px/18px var(--nli-sans);color:var(--nli-mute);margin:10px 0 0}',
      'html body .nli .nlmr details.nlmr__srcs{margin:16px 0 0}',
      'html body .nli .nlmr details.nlmr__srcs>summary{font:500 15px/22px var(--nli-sans);color:var(--nli-sea);cursor:pointer;min-height:44px;display:flex;align-items:center;border:0 !important;padding:0 !important;background:none !important}',
      '.nlmr__srcs ol{margin:4px 0 0;padding:0 18px 0 0;display:grid;gap:6px;font:400 12px/18px var(--nli-mono);color:var(--nli-mute)}',
      'html body .nli .nlmr__srcs a{color:var(--nli-sea) !important;font-family:var(--nli-sans)}',
      '.nlmr__srcline{font:400 12px/18px var(--nli-mono) !important;color:var(--nli-mute) !important}',
      '@media (max-width:420px){.nlmr__n{font-size:40px;line-height:44px}html body .nli .nlmr__q .nli__seg button{padding:10px 10px;font-size:13px}}',
      '@media print{.nlmr .nlmr__form,.nlmr .nli__pre,.nlmr .nli__prelab,.nlmr .nli__share,.nlmr a.nlmr__adv,.nlmr .nli__eg{display:none !important}.nlmr__grid{display:block}.nlmr__out{position:static}.nlmr__srcs ol{display:block}html body .nli .nlmr__list input[type=checkbox]{-webkit-print-color-adjust:exact;print-color-adjust:exact}.nlmr__list li{break-inside:avoid}}'
    ].join('\n');
    document.head.appendChild(s);
  }

  function seg(label, opts, cur, on) {
    var w = el('div', 'nli__f'); w.appendChild(el('span', 'nli__lab', esc(label)));
    var g = el('div', 'nli__seg'); g.setAttribute('role', 'group'); g.setAttribute('aria-label', label);
    opts.forEach(function (o) { var b = el('button', '', esc(o[1])); b.type = 'button'; b.setAttribute('aria-pressed', String(o[0] === cur)); b.addEventListener('click', function () { [].forEach.call(g.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); on(o[0]); }); g.appendChild(b); });
    w.appendChild(g); return w;
  }
  function money(label, val, on, help, unit) {
    var w = el('div', 'nli__f'), id = 'nlmr-' + Math.random().toString(36).slice(2, 8);
    var lab = el('label', '', esc(label)); lab.htmlFor = id; w.appendChild(lab);
    var box = el('div', 'nli__in'), inp = el('input'); inp.id = id; inp.type = 'text'; inp.inputMode = 'decimal'; inp.autocomplete = 'off';
    inp.value = isFinite(val) ? nf0.format(val) : '';
    inp.addEventListener('input', function () { on(parse(inp.value)); });
    inp.addEventListener('blur', function () { var n = parse(inp.value); inp.value = isFinite(n) ? nf0.format(n) : ''; });
    box.appendChild(inp); box.appendChild(el('span', 'nli__unit', esc(unit || '₪')));
    w.appendChild(box); if (help) w.appendChild(el('span', 'nli__help', esc(help)));
    return w;
  }

  NI.register('mready', {
    custom: function (root, data) {
      var M = data.mready, D = { boim: data.boim, ptax: data.ptax, cost: data.cost, mready: M };
      if (!M || !D.ptax || !D.cost || !rulesOf(D)) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
      css();
      var hdr = document.querySelector('header.nlhp-top');  // the result column sticks under the site's own sticky header
      var setTop = function () { var h = 0; if (hdr) { var cs = getComputedStyle(hdr); if (cs.position === 'sticky' || cs.position === 'fixed') h = hdr.getBoundingClientRect().height; } root.style.setProperty('--nlmr-top', Math.round(h + 12) + 'px'); };
      setTop(); W.addEventListener('resize', setTop);
      var R0 = rulesOf(D), v = JSON.parse(JSON.stringify(M.defaults)), pre = 'couple', example = true, ticks = loadTicks();
      try { var S = JSON.parse(root.getAttribute('data-nli-set') || '{}'); if (S.preset) applyPreset(S.preset); Object.keys(S).forEach(function (k) { if (k in v) { v[k] = S[k]; example = false; pre = null; } }); } catch (e) {}
      function applyPreset(key) { var p = M.presets.filter(function (x) { return x.key === key; })[0]; if (!p) return; Object.keys(p.set).forEach(function (k) { v[k] = p.set[k]; }); pre = key; example = true; }

      root.innerHTML = '';
      var panel = el('div', 'nli__panel nlmr');
      panel.appendChild(el('p', 'nli__kicker', 'לפני הבנק · אישור עקרוני'));
      panel.appendChild(el('h2', 'nli__title', 'מוכנים לאישור עקרוני?'));
      panel.appendChild(el('p', 'nli__lede', 'חמש שאלות. כרטיס מוכנות לפי מגבלות בנק ישראל ורשימת מסמכים אישית, לפני שהולכים לבנק.'));
      var strip = el('div', 'nli__strip');
      [['החזר מרבי מההכנסה הפנויה', pc(R0.pti_max, 0)], ['מימון מרבי, דירה יחידה', pc(R0.ltv.single, 0)], ['תוקף מזערי של אישור עקרוני', M.aip.valid_days + ' ימים']].forEach(function (x) { strip.appendChild(el('div', '', '<span>' + esc(x[0]) + '</span><strong>' + esc(x[1]) + '</strong>')); });
      panel.appendChild(strip);
      panel.appendChild(el('span', 'nli__alab nli__prelab', 'מקרים מוכנים: לחיצה אחת ממלאת הכול'));
      var preRow = el('div', 'nli__pre'); preRow.setAttribute('role', 'group'); preRow.setAttribute('aria-label', 'מקרים מוכנים');
      M.presets.forEach(function (p) {
        var b = el('button', '', '<span>' + esc(p.label) + '</span><small>' + esc(p.sub) + '</small>'); b.type = 'button'; b.setAttribute('data-k', p.key);
        b.addEventListener('click', function () { applyPreset(p.key); buildForm(); run(); });
        preRow.appendChild(b);
      });
      panel.appendChild(preRow);
      function markPre() { [].forEach.call(preRow.children, function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-k') === pre)); }); }

      var grid = el('div', 'nlmr__grid'), form = el('form', 'nlmr__form'), out = el('div', 'nlmr__out'); out.setAttribute('aria-live', 'polite');
      form.addEventListener('submit', function (e) { e.preventDefault(); });
      grid.appendChild(form); grid.appendChild(out); panel.appendChild(grid);
      var docs = el('section', 'nlmr__docs'); docs.setAttribute('aria-labelledby', 'nlmr-dh'); panel.appendChild(docs);
      var formula = el('p', 'nli__formula'), srcLine = el('p', 'nli__src nlmr__srcline'), share = el('div', 'nli__share');
      panel.appendChild(formula); panel.appendChild(srcLine); panel.appendChild(share);
      panel.appendChild(el('p', 'nli__eg', '<b>דוגמה</b>הערכים בפתיחה הם דוגמה. שנו אותם, והכרטיס והרשימה מתעדכנים מיד. הנתונים נשארים בדפדפן שלכם ולא נשלחים.'));
      root.appendChild(panel);

      var t = 0;
      function touch() { example = false; pre = null; markPre(); clearTimeout(t); t = setTimeout(run, 90); }
      var sumEl = null;
      function buildForm() {
        form.innerHTML = '';
        function q(n, title) { var f = el('fieldset', 'nlmr__q'); f.appendChild(el('legend', '', '<b>' + n + '</b>' + esc(title))); form.appendChild(f); return f; }
        var q1 = q(1, 'ההכנסה');
        q1.appendChild(seg('איך אתם מרוויחים', [['salaried', 'שכירים'], ['self', 'עצמאים'], ['both', 'שכיר ועצמאי']], v.type, function (x) { v.type = x; touch(); }));
        var q2 = q(2, 'הלווים');
        q2.appendChild(seg('כמה לווים', [['1', 'לווה אחד'], ['2', 'שני לווים']], String(v.borrowers), function (x) { v.borrowers = +x; touch(); }));
        var q3 = q(3, 'הכנסה והלוואות');
        q3.appendChild(money('הכנסה נטו של משק הבית בחודש', v.income, function (x) { v.income = x; touch(); }));
        q3.appendChild(money('החזרים חודשיים של הלוואות קיימות', v.loans, function (x) { v.loans = x; touch(); }, 'הלוואות, ליסינג, מינוס קבוע. הבנק מוריד אותם מההכנסה.'));
        var q4 = q(4, 'ההון העצמי');
        var two = el('div', 'nlmr__two');
        [['savings', 'חיסכון'], ['gift', 'עזרה מהמשפחה'], ['sale', 'ממכירת דירה'], ['grant', 'מענק']].forEach(function (x) { two.appendChild(money(x[1], v[x[0]], function (n) { v[x[0]] = n; touch(); })); });
        q4.appendChild(two);
        sumEl = el('p', 'nlmr__sum'); q4.appendChild(sumEl);
        var q5 = q(5, 'הדירה');
        q5.appendChild(seg('מי קונה', [['single', 'דירה יחידה'], ['replace', 'דירה חליפית'], ['extra', 'דירה נוספת'], ['oleh', 'עולה חדש'], ['foreign', 'תושב חוץ']], v.buyer, function (x) { v.buyer = x; touch(); }));
        q5.appendChild(seg('ממי', [['new', 'מקבלן'], ['used', 'יד שנייה']], v.market, function (x) { v.market = x; touch(); }));
        var two5 = el('div', 'nlmr__two');
        two5.appendChild(money('מחיר הדירה', v.price, function (x) { v.price = x; touch(); }));
        two5.appendChild(money('תקופת המשכנתא', v.years, function (x) { v.years = x; touch(); }, null, 'שנים'));
        q5.appendChild(two5);
        markPre();
      }

      function srcLink(id) { var s = M.sources[id]; return s ? '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.org + ': ' + s.title) + '</a>' : ''; }
      var last = null;
      function run() {
        var bad = !(v.income > 0) ? 'הקלידו את ההכנסה החודשית נטו.' : !(v.price > 0) ? 'הקלידו את מחיר הדירה.' : !(v.years >= 4 && v.years <= (R0.term_max || 30)) ? 'תקופה בין 4 ל־' + (R0.term_max || 30) + ' שנים.' : '';
        if (sumEl) sumEl.innerHTML = 'סך ההון העצמי: <bdi>' + esc(ils(equityOf(v))) + '</bdi>';
        if (bad) { out.innerHTML = '<p class="nli__note">' + esc(bad) + '</p>'; return; }
        var m = model(v, D), list = docsFor(v, M), dc = docsCheck(list, ticks), s = score(m, dc);
        last = { m: m, list: list };
        out.innerHTML = '';
        var card = el('div', 'nlmr__card');
        card.appendChild(el('span', 'nli__alab', 'כרטיס מוכנות' + (example ? ' <span class="nlmr__eg">דוגמה</span>' : '')));
        card.appendChild(el('output', 'nlmr__fig' + (s === 4 ? ' is-all' : ''), '<span class="nlmr__n">' + s + '</span> <span class="nlmr__w">מתוך</span> <span class="nlmr__n">4</span>')).setAttribute('aria-label', s + ' מתוך 4 בדיקות עוברות');
        var ul = el('ul', 'nlmr__checks');
        m.checks.concat([dc]).forEach(function (c) {
          var stt = c.state === 'done' ? 'pass' : c.state;
          var txt = c.id === 'docs' ? (dc.done ? dc.done + ' מתוך ' + dc.total + ' מוכנים.' : dc.total + ' מסמכים, עוד לא סומנו.') + ' הרשימה המלאה למטה, לפי התשובות שלכם.' : checkText(c, m);
          ul.appendChild(el('li', 'is-' + stt, '<i class="nlmr__mk" aria-hidden="true"></i><span class="nlmr__ck"><span>' + esc(LAB[c.id]) + '</span><b>' + esc(STATE[c.state]) + '</b></span><p class="nlmr__ct">' + esc(txt).replace(/(₪[\d,]+|[\d.,]+%)/g, '<bdi>$1</bdi>') + '</p>'));
        });
        card.appendChild(ul); out.appendChild(card);
        var dl = el('dl', 'nli__lines nlmr__lines');
        var rows = [['משכנתא', ils(m.loan) + (m.price > 0 ? ' · ' + pc(m.loan / m.price) : '')], ['החזר חודשי ראשון, ' + m.years + ' שנה', ils(m.payment)], ['הכנסה פנויה', ils(Math.max(0, m.disp))],
          ['מקדמה לפי מימון של ' + pc(m.ltv, 0), ils(m.down)], ['מס רכישה', m.tax >= 1 ? ils(m.tax) : 'אין במחיר הזה'], ['עורך דין, ' + String(m.lawyerPct) + '% ומע״מ', ils(m.lawyer)]];
        if (m.max[40] != null) rows.push(['המחיר הגבוה שעובר, בהחזר עד 40%', ils(m.max[40])]);
        if (m.max[50] != null) rows.push(['בהחזר עד 50%', ils(m.max[50])]);
        rows.forEach(function (r) { dl.appendChild(el('div', '', '<dt>' + esc(r[0]) + '</dt><dd><bdi>' + esc(r[1]) + '</bdi></dd>')); });
        out.appendChild(dl);
        var adv = el('a', 'nlmr__adv', 'לשלוח את התיק ליועץ'); adv.href = 'https://nad-lan.co.il/mortgage-advisor/'; out.appendChild(adv);
        paintDocs(list, dc);
        var mix = m.basis === 'mix' ? 'התמהיל הממוצע של כל הבנקים, ' + ymon(m.month) : 'הריבית הממוצעת בקבועה לא צמודה, ' + ymon(m.month), mixIn = m.basis === 'mix' ? 'בתמהיל הממוצע של כל הבנקים, ' + ymon(m.month) : 'בריבית הממוצעת בקבועה לא צמודה, ' + ymon(m.month);
        formula.textContent = 'החזר ראשון = משכנתא × ההחזר על מיליון ₪ ' + mixIn + ': ' + ils(m.perM) + ' בחודש ל־' + m.years + ' שנה. הכנסה פנויה = הכנסה נטו פחות החזרי הלוואות קיימות. משכנתא = מחיר + מס רכישה + עורך דין פחות הון עצמי, עד שיעור המימון המרבי. המחיר הגבוה שעובר: מחשבון כושר ההחזר של האתר, באותם נתונים.';
        srcLine.innerHTML = 'מקורות: ' + esc(R0.src.label) + ' · ' + (D.ptax.url ? '<a href="' + esc(D.ptax.url) + '" target="_blank" rel="noopener">' + esc(D.ptax.source) + '</a>' : esc(D.ptax.source || '')) + ' · בנק ישראל, ' + esc(mix) + ' · רשימות המסמכים של 7 בנקים, כל זכות ובנק ישראל, נבדקו ב־' + esc(fdate(M.checked));
      }
      function paintDocs(list, dc) {
        docs.innerHTML = '';
        docs.appendChild(el('h3', 'nlmr__h', 'רשימת המסמכים שלכם')).id = 'nlmr-dh';
        var all = list.length, done = list.filter(function (d) { return ticks[d.id]; }).length;
        docs.appendChild(el('p', 'nlmr__p', 'לפי התשובות שלכם: ' + all + ' מסמכים' + (done ? ', ' + done + ' מסומנים' : '') + '. סמנו מה שכבר בידיים; הסימון נשמר רק בדפדפן הזה.'));
        var wrap = el('div', 'nlmr__stages');
        ['aip', 'loan'].forEach(function (st) {
          var items = list.filter(function (d) { return d.stage === st; }), box = el('div', '');
          var dn = items.filter(function (d) { return ticks[d.id]; }).length;
          box.appendChild(el('h4', 'nlmr__h4', esc(M.stages[st].label) + '<small><bdi>' + dn + '/' + items.length + '</bdi></small>'));
          box.appendChild(el('p', 'nlmr__p', esc(M.stages[st].lede)));
          var ul = el('ul', 'nlmr__list');
          items.forEach(function (d) {
            var li = el('li', d.some ? 'is-some' : ''), lab = el('label', ''), cb = el('input');
            cb.type = 'checkbox'; cb.checked = !!ticks[d.id]; cb.setAttribute('data-id', d.id);
            cb.addEventListener('change', function () { if (cb.checked) ticks[d.id] = 1; else delete ticks[d.id]; saveTicks(ticks); run(); var again = docs.querySelector('input[data-id="' + d.id + '"]'); if (again) again.focus(); });
            lab.appendChild(cb);
            lab.appendChild(el('span', '', (d.cond ? '<em>' + esc(d.cond) + ':</em> ' : '') + esc(d.text) + (d.per ? ', ' + esc(d.per) : '') + (d.some ? '<span class="nlmr__tag">יש בנקים שמבקשים</span>' : '')));
            lab.appendChild(el('small', 'nlmr__ds', esc(groupsOf(d.src, M).join(' · '))));
            li.appendChild(lab); ul.appendChild(li);
          });
          box.appendChild(ul); wrap.appendChild(box);
        });
        docs.appendChild(wrap);
        docs.appendChild(el('p', 'nlmr__key', 'בלי תווית: לפחות שני גופים מפרסמים את המסמך (בנקים, כל זכות, בנק ישראל). "יש בנקים שמבקשים": בנק אחד, או קבוצת בנקים אחת, או כתבות בלבד. כל בנק רשאי לבקש עוד מסמכים לפי העסקה.'));
        var det = el('details', 'nlmr__srcs'); det.appendChild(el('summary', '', 'המקורות לכל מסמך, עם תאריך הבדיקה'));
        var used = []; list.forEach(function (d) { d.src.forEach(function (s) { if (used.indexOf(s) < 0) used.push(s); }); });
        M.aip.valid_src.concat(M.aip.docs_optional_src).forEach(function (s) { if (used.indexOf(s) < 0) used.push(s); });
        var ol = el('ol', ''); used.forEach(function (s) { var x = M.sources[s]; ol.appendChild(el('li', '', srcLink(s) + ' · נבדק ' + esc(fdate(x.retrieved.slice(0, 10))))); });
        det.appendChild(ol); docs.appendChild(det);
      }

      function textNow() { return last ? copyText(v, last.m, last.list, ticks, M) + '\n' + location.origin + location.pathname : location.href; }
      var ICON = { copy: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 7h9v10H7z"/><path d="M4 13V3h9"/></svg>', wa: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16l1-3.2A7 7 0 1 1 7.6 15z"/></svg>', print: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 8V3h10v5"/><path d="M5 14H3V8h14v6h-2"/><path d="M6 12h8v5H6z"/></svg>' };
      var bc = el('button', 'is-primary', ICON.copy + '<span>העתקת הכרטיס והרשימה</span>'); bc.type = 'button';
      bc.addEventListener('click', function () { var tx = textNow(), lab = bc.querySelector('span');
        var ok = function () { lab.textContent = 'הועתק'; setTimeout(function () { lab.textContent = 'העתקת הכרטיס והרשימה'; }, 1600); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(tx).then(ok, function () { W.prompt('העתיקו את הרשימה', tx); }); else W.prompt('העתיקו את הרשימה', tx); });
      var bw = el('a', '', ICON.wa + '<span>שליחה בוואטסאפ</span>'); bw.target = '_blank'; bw.rel = 'noopener'; bw.href = 'https://wa.me/';
      bw.addEventListener('click', function () { bw.href = 'https://wa.me/?text=' + encodeURIComponent(textNow()); });
      var bp = el('button', '', ICON.print + '<span>הדפסה או שמירה כקובץ</span>'); bp.type = 'button';
      bp.addEventListener('click', function () { var d = docs.querySelector('details'); if (d) d.open = true; W.print(); });
      share.appendChild(bc); share.appendChild(bw); share.appendChild(bp);

      function start() { buildForm(); run(); }
      if (W.NLAF || !AFF) start();
      else { var sc = document.createElement('script'); sc.src = AFF; sc.onload = start; sc.onerror = start; document.head.appendChild(sc); }
    }
  });
})();
