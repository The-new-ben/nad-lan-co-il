/* NadLan Instruments · mkeys v1 (HAD-675, round H, 6.11.2026): "מהחוזה למפתח", the 7th tool of the switcher on /mortgage-calculator/
   (design board Keys.dc.html). For a buyer of a new apartment from a developer: every payment to the developer on its date, the
   construction-input-index linkage of the Sale (Apartments) Law, what comes from equity and what is drawn from the mortgage, the
   interest until delivery under three grace choices, and the full payment after the keys.
   - Linkage: NOT computed here. window.NLIX (tools/indexation.js) does it: NLIX.schedule(kind, sign, delivery) gives the plan,
     NLIX.compute(v, cbs, annual) applies s.5ג (contracts from 7.7.2022: the first 20% paid at signing never linked, at most half of
     each later payment, no linkage after the contractual delivery date) on the KNOWN index of each date (CBS 200010, published on
     the 15th for the previous month), future months at the chosen annual change; NLIX.trailing(cbs) is the default change (the
     last 12 months). Share passed: 50% (the legal maximum) from 7.7.2022; for an older contract 100% (the upper bound; said so).
     Payment dates later than the contractual delivery (a short build) are moved to the delivery date before NLIX runs.
   - Funding: equity pays the payments, each with its linkage, in date order until it is used up; the rest is drawn from the mortgage.
   - Rate: the "system" (all banks) average mix and effective rates of the latest month of boi-mortgage.json (by_bank). Before the
     keys: the mix-weighted monthly rate, sum of share x ((1 + e)^(1/12) - 1). A draw in month m bears interest for the months
     m+1 .. delivery month. Grace "partial": that interest is paid every month (balance stays the sum of the draws); "full": it is
     added to the balance every month; "immediate": every draw starts its own Spitzer schedule over the term at once (per track).
   - After the keys: the balance x window.NLMQ.payPer1(by_bank, 'system', last month, term) (tools/mquick.js: Spitzer per track at
     the average mix, CPI tracks with the index unchanged). In "immediate" the full payment is the sum of the draws' own payments.
   - Financing share: the largest sum owed (the draws, or the balance with capitalized interest in full grace) / the contract
     price; above 75% it is marked against directive 329 (rules.ltv.single).
   Pure logic in window.NLMK (node test: docs/research/2026-11-05-mortgage-world/build/round-h/test_mkeys.js). Hebrew only, RTL:
   on an English mount the tool draws nothing. Registry: 'deps' => array( 'indexation', 'mquick' ), data boi-mortgage.json +
   cbs-200010.json. Style id-scoped with !important (the theme restyles headings, buttons, inputs and lists). */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;
  var TR = ['fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi'];  // the order of by_bank (as in mquick.js)
  var NEW_LAW = '2022-07-07';
  var PLANS = [{ k: 'end', he: '20% עכשיו, 80% במסירה' }, { k: 'stages', he: 'לפי שלבים' }, { k: 'thirds', he: '20%, 30% אחרי שנה, 50% במסירה' }];
  var GRACE = [{ k: 'partial', he: 'משלמים ריבית' }, { k: 'full', he: 'הריבית נצברת' }, { k: 'immediate', he: 'החזר מלא מיד' }];
  var TERMS = [20, 25, 30];
  var LTV_MAX = 0.75;

  /* ------------------------------------------------------------------------------------------------ dates (plain calendar) */
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function isISO(s) { return /^\d{4}-\d{2}-\d{2}$/.test(String(s || '')) && !isNaN(Date.parse(s)); }
  function addMonths(iso, n) {  // the same day of the month, clipped to the month's last day
    var p = iso.split('-').map(Number), y = p[0], m = p[1] - 1 + n;
    y += Math.floor(m / 12); m = ((m % 12) + 12) % 12;
    var last = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
    return y + '-' + pad(m + 1) + '-' + pad(Math.min(p[2], last));
  }
  function mDiff(a, b) { return (+b.slice(0, 4) - +a.slice(0, 4)) * 12 + (+b.slice(5, 7) - +a.slice(5, 7)); }  // months a -> b (YYYY-MM...)
  function mmyyyy(iso) { return iso.slice(5, 7) + '.' + iso.slice(0, 4); }
  function todayISO(d) { d = d || new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }

  /* ------------------------------------------------------------------------------------------------------------ the data */
  function pick(data) {  // found by shape: boi-mortgage.json has key "boim" and by_bank; cbs-200010.json has id 200010 and no key
    var o = { D: null, C: null };
    Object.keys(data || {}).forEach(function (k) {
      var d = data[k]; if (!d || typeof d !== 'object') return;
      if (d.by_bank && d.by_bank.months) o.D = d; else if (d.months && String(d.id) === '200010') o.C = d;
    });
    return o;
  }
  /* the all-banks average of the latest month: each track's share and monthly rate, as payPer1 reads them */
  function rates(bb, bank) {
    bank = bank || 'system';
    var i = bb.months.length - 1, mix = bb.mix[bank], rate = bb.rate[bank], tot = 0, out = [], rm = 0;
    if (!mix || !rate) return null;
    TR.forEach(function (k) { tot += +mix[k][i] || 0; });
    if (!(tot > 0)) return null;
    TR.forEach(function (k) {
      var p = (+mix[k][i] || 0) / tot, e = +rate[k][i] || 0, r = Math.pow(1 + e / 100, 1 / 12) - 1;
      if (p > 0) { out.push({ k: k, p: p, e: e, r: r }); rm += p * r; }
    });
    return { bank: bank, i: i, month: bb.months[i], tracks: out, rm: rm };
  }
  /* the balance left of a Spitzer loan of 1 after n of N payments, summed over the tracks by share */
  function left1(R, N, n) {
    return R.tracks.reduce(function (a, t) {
      var b = t.r > 0 ? (Math.pow(1 + t.r, N) - Math.pow(1 + t.r, n)) / (Math.pow(1 + t.r, N) - 1) : 1 - n / N;
      return a + t.p * b;
    }, 0);
  }

  function defaults(now) {
    var s = todayISO(now);
    return { price: 2000000, equity: 600000, sign: s, delivery: addMonths(s, 36), plan: 'stages', grace: 'partial', years: 25, annual: null };
  }

  /* ----------------------------------------------------------------------------------------------------------- the math */
  function compute(v, D, C) {
    var X = G.NLIX, Q = G.NLMQ;
    if (!X || !Q) return { error: { field: null, msg: 'הנתונים לא נטענו. רעננו את העמוד.' } };
    var bb = D && D.by_bank;
    if (!bb || !bb.months || !C || !C.months) return { error: { field: null, msg: 'הנתונים לא נטענו. רעננו את העמוד.' } };
    var P = +v.price, E = +v.equity, s = v.sign, del = v.delivery, years = +v.years || 25;
    if (!(P > 50000)) return { error: { field: 'price', msg: 'הקלידו את מחיר הדירה בחוזה.' } };
    if (!(E >= 0) || v.equity === '' || v.equity == null) return { error: { field: 'equity', msg: 'הקלידו את ההון העצמי שלכם (אפשר גם 0).' } };
    if (E > P) return { error: { field: 'equity', msg: 'ההון העצמי גבוה ממחיר הדירה. הקלידו סכום עד מחיר הדירה.' } };
    if (!isISO(s)) return { error: { field: 'sign', msg: 'בחרו את תאריך חתימת החוזה.' } };
    if (!isISO(del)) return { error: { field: 'delivery', msg: 'בחרו את מועד המסירה בחוזה.' } };
    if (del <= s) return { error: { field: 'delivery', msg: 'מועד המסירה בחוזה צריך להיות אחרי תאריך החתימה.' } };
    var annual = v.annual == null ? X.trailing(C) : +v.annual;
    if (!isFinite(annual) || annual < -0.2 || annual > 0.3) return { error: { field: 'annual', msg: 'הקלידו שינוי שנתי במדד באחוזים, למשל 3.6 (בין מינוס 20 ל־30).' } };
    var R = rates(bb, 'system'); if (!R) return { error: { field: null, msg: 'הנתונים לא נטענו. רעננו את העמוד.' } };
    var per1 = Q.payPer1(bb, 'system', R.i, years), N = years * 12;

    // 1. the plan and its linkage, by NLIX (a date after the contractual delivery is moved to it)
    var newLaw = s >= NEW_LAW;
    var plan = X.schedule(v.plan, s, del).map(function (r) { return { date: r.date > del ? del : r.date, pct: r.pct }; });
    var L = X.compute({ price: P, sign: s, delivery: del, share: newLaw ? 50 : 100, floor: true, rows: plan }, C, annual);
    if (L.error) return { error: { field: L.error.field === 'rows' || L.error.field === 'share' ? null : L.error.field, msg: L.error.msg } };

    // 2. funding in date order, then the grace choice month by month
    var dk = del.slice(0, 7), eqLeft = E, cum = 0, bal = 0, prevKey = null, rows = [];
    var interest = 0, paidBefore = 0, leftAtKeys = 0, balFull = 0;
    L.rows.forEach(function (x) {
      var key = x.date.slice(0, 7), total = x.amt + x.add, fromEq = Math.min(eqLeft, total), draw = total - fromEq, n = Math.max(0, mDiff(key, dk));
      eqLeft -= fromEq; cum += draw;
      if (prevKey != null) bal *= Math.pow(1 + R.rm, Math.max(0, mDiff(prevKey, key)));  // full grace: the interest joins the balance
      bal += draw; prevKey = key;
      interest += draw * R.rm * n;                       // partial: each draw pays its monthly interest until the keys
      balFull += draw * Math.pow(1 + R.rm, n);           // full: each draw compounds until the keys
      paidBefore += draw * per1 * Math.min(n, N); leftAtKeys += draw * left1(R, N, Math.min(n, N));  // immediate: each draw's own schedule
      rows.push({ date: x.date, key: key, pct: x.pct, amt: x.amt, linked: x.linked, add: x.add, known: x.known, exempt: !(x.linked > 0),
        total: total, fromEq: fromEq, draw: draw, cum: cum, n: n, atKeys: n === 0,
        monthInt: cum * R.rm,            // partial: the monthly interest after this draw
        bal: bal,                        // full: the balance right after this draw
        monthPay: cum * per1 });         // immediate: the monthly payment after this draw
    });
    var drawn = cum, o = { newLaw: newLaw, annual: annual, annualDefault: v.annual == null, month: R.month, rm: R.rm, per1: per1, years: years,
      sign: s, delivery: del, deliveryKey: dk, price: P, equity: E, plan: v.plan, grace: v.grace, rows: rows,
      linkTotal: L.total, linkKnown: L.known, linkProjected: L.projected, baseKey: L.baseKey, cbsLatest: C.latest,
      drawn: drawn, eqUsed: E - eqLeft, eqLeft: eqLeft, noMortgage: !(drawn > 0.5) };
    if (v.grace === 'full') { o.interest = balFull - drawn; o.balance = balFull; o.pay = balFull * per1; }
    else if (v.grace === 'immediate') { o.paidBefore = paidBefore; o.balance = leftAtKeys; o.interest = paidBefore - (drawn - leftAtKeys); o.pay = drawn * per1; }
    else { o.interest = interest; o.balance = drawn; o.pay = drawn * per1; }
    if (o.noMortgage) { o.interest = 0; o.balance = 0; o.pay = 0; o.paidBefore = 0; }
    o.owed = Math.max(drawn, o.balance);
    o.share = o.owed / P; o.over75 = o.share > LTV_MAX + 1e-9;
    return o;
  }

  /* ----------------------------------------------------------------------------------------------------------- the words */
  var nf = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function ils(x) { return nf.format(Math.round(x || 0)) + ' ₪'; }
  function b(x) { return '<bdi>' + x + '</bdi>'; }
  function pct1(x) { return (Math.round(x * 1000) / 10).toFixed(1) + '%'; }
  var HEM = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
  function monthHe(ym) { var p = String(ym).split('-'); return p.length >= 2 ? (HEM[+p[1] - 1] || p[1]) + ' ' + p[0] : ym; }
  function monthNum(ym) { var p = String(ym).split('-'); return (+p[1]) + '.' + p[0]; }

  function headline(r) {
    if (r.noMortgage) return { label: 'ההחזר המלא אחרי המפתח', value: 'לא צריך משכנתא', text: true };
    return { label: 'ההחזר המלא אחרי המפתח', value: ils(r.pay), text: false };
  }
  /* one row of the timeline (HTML: fixed words and formatted numbers only) */
  function rowText(x, r) {
    var t = [], lead = x.pct + '%';
    if (x.date === r.sign) lead += ' בחתימה'; else if (x.date === r.delivery) lead += ' במסירה';
    var link;
    if (x.exempt) link = 'בלי הצמדה';
    else if (x.add > 0.5) link = 'הצמדה ' + b(ils(x.add)) + (x.known ? '' : ' (צפי)');
    else link = x.known ? 'בלי תוספת הצמדה (המדד הידוע לא עלה)' : 'בלי תוספת הצמדה (לפי השינוי שבחרתם במדד)';
    t.push(lead + ', ' + b(ils(x.amt)) + ', ' + link + '.');
    if (!(x.draw > 0.5)) t.push(x.fromEq > 0.5 ? 'מההון העצמי.' : '');
    else if (!(x.fromEq > 0.5)) t.push(b(ils(x.draw)) + ' נמשכים מהמשכנתא.');
    else t.push(b(ils(x.fromEq)) + ' מההון העצמי, ' + b(ils(x.draw)) + ' נמשכים מהמשכנתא.');
    if (x.cum > 0.5 && !x.atKeys) {
      if (r.grace === 'full') t.push('יתרת המשכנתא ' + b(ils(x.bal)) + ', והריבית נצברת עליה.');
      else if (r.grace === 'immediate') t.push('מכאן החזר ' + b(ils(x.monthPay)) + ' בחודש.');
      else t.push('מכאן ריבית ' + b(ils(x.monthInt)) + ' בחודש.');
    }
    return t.filter(Boolean).join(' ');
  }
  function keysText(r) {
    if (r.noMortgage) return 'המפתח. בלי משכנתא: ההון העצמי מכסה את כל התשלומים לקבלן, כולל ההצמדה.';
    if (r.grace === 'immediate') return 'המפתח. יתרת המשכנתא ' + b(ils(r.balance)) + ', וההחזר המלא ' + b(ils(r.pay)) + ' בחודש: כל משיכה נפרסת ל־' + r.years + ' שנה מיום המשיכה.';
    return 'המפתח. יתרת המשכנתא ' + b(ils(r.balance)) + ' נפרסת ל־' + r.years + ' שנה, וההחזר המלא ' + b(ils(r.pay)) + ' בחודש.';
  }
  function summary(r) {  // the line under the headline
    var a = [r.linkTotal > 0.5 ? 'ההצמדה עד המסירה ' + b(ils(r.linkTotal)) : 'בלי הצמדה עד המסירה'];
    if (!r.noMortgage) {
      if (r.grace === 'full') a.push(r.interest > 0.5 ? 'ריבית שנצברה עד המסירה ' + b(ils(r.interest)) : 'בלי ריבית לפני המסירה');
      else if (r.grace === 'immediate') a.push(r.paidBefore > 0.5 ? 'שולם לבנק עד המסירה ' + b(ils(r.paidBefore)) + ', מזה ריבית ' + b(ils(r.interest)) : 'בלי תשלום לבנק לפני המסירה');
      else a.push(r.interest > 0.5 ? 'ריבית עד המסירה ' + b(ils(r.interest)) : 'בלי ריבית לפני המסירה');
      a.push('המשכנתא במסירה ' + b(ils(r.balance)));
    }
    return a.join(' · ');
  }
  function ltvText(r) {
    var base = 'שיעור המימון ' + b(pct1(r.share)) + (r.grace === 'full' ? ' (עם הריבית שנצברה)' : '');
    return r.over75 ? base + ': מעל 75%, המימון המרבי של בנק ישראל לדירה יחידה (הוראה 329).' : base + ' (עד 75% לדירה יחידה, לפי הוראה 329 של בנק ישראל).';
  }
  function copyText(r) {
    var pl = PLANS.filter(function (p) { return p.k === r.plan; })[0], gr = GRACE.filter(function (g) { return g.k === r.grace; })[0];
    var head = 'מהחוזה למפתח: דירה ב־' + ils(r.price) + ', הון עצמי ' + ils(r.equity) + ', חתימה ' + mmyyyy(r.sign) + ', מסירה ' + mmyyyy(r.delivery)
      + ', לוח התשלומים ' + (pl ? pl.he : r.plan) + ', עד המסירה: ' + (gr ? gr.he : r.grace) + '.';
    var link = r.linkTotal > 0.5 ? ' ההצמדה עד המסירה ' + ils(r.linkTotal) + '.' : ' בלי הצמדה עד המסירה.';
    if (r.noMortgage) return head + link + ' בלי משכנתא: ההון העצמי מכסה את כל התשלומים.';
    var mid = r.grace === 'immediate' ? ' שולם לבנק עד המסירה ' + ils(r.paidBefore) + ', מזה ריבית ' + ils(r.interest) + '.'
      : r.interest > 0.5 ? (r.grace === 'full' ? ' ריבית שנצברה עד המסירה ' + ils(r.interest) + '.' : ' ריבית עד המסירה ' + ils(r.interest) + '.') : '';
    return head + link + mid + ' המשכנתא במסירה ' + ils(r.balance) + ', שיעור מימון ' + pct1(r.share) + '. ההחזר המלא אחרי המפתח: '
      + ils(r.pay) + ' בחודש ל־' + r.years + ' שנה, בתמהיל ובריבית הממוצעים של כל הבנקים ב' + monthHe(r.month) + ' (בנק ישראל).';
  }

  G.NLMK = { compute: compute, rates: rates, left1: left1, pick: pick, defaults: defaults, addMonths: addMonths, mmyyyy: mmyyyy,
    headline: headline, rowText: rowText, keysText: keysText, summary: summary, ltvText: ltvText, copyText: copyText,
    PLANS: PLANS, GRACE: GRACE, TERMS: TERMS, LTV_MAX: LTV_MAX };
  if (!G.NadLanInstruments) return;

  /* ----------------------------------------------------------------------------------------------------------- the page */
  var NI = G.NadLanInstruments, esc = NI.esc;
  var CSS = '#nlmk{font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#12202A;background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:16px;display:flex;flex-direction:column;gap:14px;margin:8px 0 16px}'
    + '#nlmk *{box-sizing:border-box}'
    + '#nlmk p.nlmk__k{margin:0!important;font:500 12px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;letter-spacing:.04em;color:#5E6A75!important}'
    + '#nlmk h2.nlmk__h{margin:0!important;padding:0!important;border:0!important;font:600 20px/28px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important;text-wrap:balance}#nlmk h2.nlmk__h::before,#nlmk h2.nlmk__h::after{display:none!important}'
    + '#nlmk .nlmk__grid{display:grid;grid-template-columns:minmax(0,1fr);gap:16px}'
    + '@media (min-width:900px){#nlmk{padding:24px}#nlmk .nlmk__grid{grid-template-columns:minmax(0,420px) minmax(0,1fr);gap:28px;align-items:start}}'
    + '#nlmk .nlmk__form{display:flex;flex-direction:column;gap:12px;min-width:0}'
    + '#nlmk .nlmk__x2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;align-items:start}'
    + '#nlmk .nlmk__lab{display:block;font:500 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important;margin:0 0 6px!important}'
    + '#nlmk .nlmk__in{display:flex;align-items:stretch;gap:6px;height:48px;padding:0 10px;border:1px solid #2F6F86;border-radius:2px;background:#fff}'
    + '#nlmk .nlmk__in input{flex:1 1 auto;min-width:0;width:100%!important;height:auto!important;min-height:44px!important;margin:0!important;border:0!important;outline:0;background:transparent!important;box-shadow:none!important;padding:0!important;font:400 17px/1.2 "IBM Plex Mono",ui-monospace,monospace!important;color:#12202A!important;text-align:right}'
    + '#nlmk .nlmk__in input[type="date"]{font-size:15px!important;min-height:44px!important}'
    + '#nlmk #nlmk-i{direction:ltr!important;text-align:right!important}'
    + '#nlmk .nlmk__in span{align-self:center;font:400 15px/1 "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}'
    + '#nlmk .nlmk__in:focus-within{outline:2px solid #2F6F86;outline-offset:1px}'
    + '#nlmk .nlmk__help{display:block;margin:6px 0 0;font:400 12px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#5E6A75!important}'
    + '#nlmk .nlmk__err{display:block;font:500 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#C42550!important;margin:4px 0 0}#nlmk .nlmk__err:empty{display:none}'
    + '#nlmk .nlmk__seg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}'
    + '#nlmk .nlmk__seg button{min-height:44px!important;margin:0!important;padding:4px 6px!important;border-radius:2px!important;border:1px solid #D3DCE2!important;background:#fff!important;color:#3E4C58!important;font:400 13px/1.25 "IBM Plex Sans Hebrew",system-ui,sans-serif!important;box-shadow:none!important;cursor:pointer;text-align:center;text-transform:none!important;letter-spacing:0!important;width:auto!important}'
    + '#nlmk .nlmk__seg button[aria-pressed="true"]{background:#2F6F86!important;border-color:#2F6F86!important;color:#fff!important;font-weight:600!important}'
    + '#nlmk button:focus-visible{outline:2px solid #1F4B5C!important;outline-offset:2px}'
    + '#nlmk .nlmk__out{display:flex;flex-direction:column;gap:6px;border-top:1px solid #D3DCE2;padding-top:12px}'
    + '@media (min-width:900px){#nlmk .nlmk__out{border-top:0;padding-top:0}}'
    + '#nlmk .nlmk__ol{font:500 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important}'
    + '#nlmk .nlmk__fig{font:500 38px/42px "IBM Plex Mono",ui-monospace,monospace!important;color:#12202A!important}#nlmk .nlmk__fig.is-text{font:600 26px/34px "IBM Plex Sans Hebrew",system-ui,sans-serif!important}'
    + '#nlmk p.nlmk__sub,#nlmk p.nlmk__ltv{margin:0!important;font:400 13px/21px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important}'
    + '#nlmk .nlmk__sub bdi,#nlmk .nlmk__ltv bdi{font-family:"IBM Plex Mono",ui-monospace,monospace!important;font-weight:400!important;color:#12202A!important}'
    + '#nlmk p.nlmk__ltv.is-over bdi{text-decoration:underline;text-decoration-color:#C42550;text-decoration-thickness:2px;text-underline-offset:5px}'
    + '#nlmk .nlmk__msg{margin:0!important;padding:10px 12px!important;background:#F6F8F9;border-inline-start:3px solid #C42550;font:500 14px/22px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}'
    + '#nlmk ol.nlmk__tl{list-style:none!important;margin:4px 0 0!important;padding:0!important;display:flex;flex-direction:column}'
    + '#nlmk ol.nlmk__tl>li{display:grid;grid-template-columns:64px minmax(0,1fr);gap:10px;margin:0!important;padding:10px 0!important;border-bottom:1px solid #D3DCE2;list-style:none!important;background:none!important}'
    + '#nlmk ol.nlmk__tl>li::before,#nlmk ol.nlmk__tl>li::marker{content:none!important;display:none!important}'
    + '#nlmk ol.nlmk__tl>li:last-child{border-bottom:0}'
    + '#nlmk .nlmk__d{font:500 13px/20px "IBM Plex Mono",ui-monospace,monospace!important;color:#2F6F86!important;direction:ltr;text-align:right}'
    + '#nlmk .nlmk__t,#nlmk .nlmk__t bdi{font:400 13px/20px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}'
    + '#nlmk ol.nlmk__tl>li.is-keys{background:#F6F8F9!important;border-inline-start:3px solid #2F6F86;padding:10px 8px!important;margin-top:6px!important}#nlmk li.is-keys .nlmk__t,#nlmk li.is-keys .nlmk__t bdi{font-weight:500!important}'
    + '@media (min-width:900px){#nlmk .nlmk__t,#nlmk .nlmk__t bdi{font-size:14px!important;line-height:22px!important}#nlmk .nlmk__d{line-height:22px!important}}'
    + '#nlmk p.nlmk__src{margin:0!important;font:400 12px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#5E6A75!important}#nlmk p.nlmk__src a{color:#2F6F86!important}'
    + '#nlmk button.nlmk__copy{align-self:flex-start;min-height:44px!important;margin:0!important;padding:0 16px!important;border-radius:999px!important;border:1px solid #D3DCE2!important;background:#fff!important;color:#3E4C58!important;font:500 14px/1.2 "IBM Plex Sans Hebrew",system-ui,sans-serif!important;box-shadow:none!important;cursor:pointer;width:auto!important}'
    + '#nlmk [hidden]{display:none!important}';
  function ensureCss() { if (document.getElementById('nlmk-css')) return; var s = document.createElement('style'); s.id = 'nlmk-css'; s.textContent = CSS; document.head.appendChild(s); }
  function num(s) { var n = parseFloat(String(s).replace(/[^\d.]/g, '')); return isFinite(n) ? n : NaN; }
  function signed(s) { var t = String(s).replace(/[−‒]/g, '-').replace(/[^\d.\-]/g, ''); var n = parseFloat(t); return isFinite(n) ? n : NaN; }

  NI.register('mkeys', {
    custom: function (root, data) {
      if (NI.langOf && NI.langOf(root) === 'en') return;  // Hebrew only: the English page does not host this tool
      var tries = 0;
      (function wait() {
        if (G.NLIX && G.NLMQ) return build(root, data);
        if (++tries > 120) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
        setTimeout(wait, 50);
      })();
    }
  });

  function build(root, data) {
    var S = pick(data), D = S.D, C = S.C;
    if (!D || !D.by_bank || !C) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
    ensureCss();
    var v = defaults(), touchedDel = false, tr = G.NLIX.trailing(C), src = D.by_bank.src || {};
    var cbsPrev = (function () { var l = C.latest, y = +l.slice(0, 4) - 1; return y + l.slice(4); })();
    function seg(id, lab, items, key) {
      return '<div><span class="nlmk__lab" id="' + id + '">' + lab + '</span><div class="nlmk__seg" role="group" aria-labelledby="' + id + '">'
        + items.map(function (x) { return '<button type="button" data-' + key + '="' + esc(String(x.k)) + '">' + esc(x.he) + '</button>'; }).join('') + '</div></div>';
    }
    function fld(id, lab, inner, help) {
      return '<div><label class="nlmk__lab" for="' + id + '">' + lab + '</label><div class="nlmk__in">' + inner + '</div>'
        + (help ? '<span class="nlmk__help" id="' + id + '-h">' + help + '</span>' : '') + '<span class="nlmk__err" data-err="' + id + '" aria-live="polite"></span></div>';
    }
    var h = '<div class="nlmk" id="nlmk" dir="rtl" lang="he">'
      + '<p class="nlmk__k">מחשבון · דירה מקבלן</p>'
      + '<h2 class="nlmk__h">מהחוזה למפתח: התשלומים, ההצמדה והמשכנתא</h2>'
      + '<div class="nlmk__grid"><div class="nlmk__form">'
      + '<div class="nlmk__x2">' + fld('nlmk-p', 'מחיר הדירה בחוזה', '<input id="nlmk-p" inputmode="numeric" autocomplete="off"><span>₪</span>')
      + fld('nlmk-e', 'הון עצמי', '<input id="nlmk-e" inputmode="numeric" autocomplete="off"><span>₪</span>') + '</div>'
      + '<div class="nlmk__x2">' + fld('nlmk-s', 'חתימת החוזה', '<input id="nlmk-s" type="date">')
      + fld('nlmk-d', 'מסירה בחוזה', '<input id="nlmk-d" type="date">') + '</div>'
      + seg('nlmk-pl', 'לוח התשלומים לקבלן', PLANS, 'plan')
      + seg('nlmk-gl', 'עד המסירה (גרייס)', GRACE, 'grace')
      + seg('nlmk-tl', 'המשכנתא אחרי המפתח, לתקופה של', TERMS.map(function (y) { return { k: y, he: y + ' שנה' }; }), 'years')
      + fld('nlmk-i', 'שינוי המדד בשנה, בחודשים שעוד לא פורסמו', '<input id="nlmk-i" inputmode="decimal" autocomplete="off" aria-describedby="nlmk-i-h"><span>%</span>',
        'ברירת המחדל: השינוי ב־12 החודשים שבין ' + monthNum(cbsPrev) + ' ל־' + monthNum(C.latest) + ' במדד תשומות הבנייה של הלמ״ס, ' + (Math.round(tr * 1000) / 10).toFixed(1) + '%.')
      + '</div><div class="nlmk__res">'
      + '<div class="nlmk__out" aria-live="polite"><p class="nlmk__msg" hidden></p><div class="nlmk__ok"><span class="nlmk__ol"></span><div class="nlmk__fig"></div>'
      + '<p class="nlmk__sub"></p><p class="nlmk__ltv"></p>'
      + '<ol class="nlmk__tl" aria-label="התשלומים לפי התאריך"></ol></div></div>'
      + '</div></div>'
      + '<p class="nlmk__src"></p>'
      + '<button type="button" class="nlmk__copy">העתקת התוצאה</button>'
      + '</div>';
    root.innerHTML = h;
    var q = function (s) { return root.querySelector(s); }, qa = function (s) { return [].slice.call(root.querySelectorAll(s)); };
    var IP = q('#nlmk-p'), IE = q('#nlmk-e'), IS = q('#nlmk-s'), ID = q('#nlmk-d'), II = q('#nlmk-i');
    IP.value = nf.format(v.price); IE.value = nf.format(v.equity); IS.value = v.sign; ID.value = v.delivery; II.value = (tr * 100).toFixed(2);
    var last = null, t = 0;
    function later() { clearTimeout(t); t = setTimeout(paint, 90); }
    IP.addEventListener('input', function () { v.price = num(IP.value); later(); });
    IE.addEventListener('input', function () { v.equity = IE.value.trim() === '' ? '' : num(IE.value); later(); });
    [IP, IE].forEach(function (inp) { inp.addEventListener('blur', function () { var x = inp === IP ? v.price : v.equity; if (isFinite(x) && x !== '') inp.value = nf.format(x); }); });
    function onSign() { v.sign = IS.value || ''; if (!touchedDel && isISO(v.sign)) { v.delivery = addMonths(v.sign, 36); ID.value = v.delivery; } later(); }
    IS.addEventListener('input', onSign); IS.addEventListener('change', onSign);
    function onDel() { touchedDel = true; v.delivery = ID.value || ''; later(); }
    ID.addEventListener('input', onDel); ID.addEventListener('change', onDel);
    II.addEventListener('input', function () { var x = signed(II.value); v.annual = II.value.trim() === '' ? NaN : x / 100; later(); });
    root.addEventListener('click', function (e) {
      var bt = e.target && e.target.closest ? e.target.closest('button') : null; if (!bt || !root.contains(bt)) return;
      if (bt.hasAttribute('data-plan')) { v.plan = bt.getAttribute('data-plan'); paint(); }
      else if (bt.hasAttribute('data-grace')) { v.grace = bt.getAttribute('data-grace'); paint(); }
      else if (bt.hasAttribute('data-years')) { v.years = +bt.getAttribute('data-years'); paint(); }
      else if (bt.classList.contains('nlmk__copy') && last) {
        var tx = copyText(last) + '\n' + location.origin + location.pathname + '#tool-keys';
        var done = function () { bt.textContent = 'הועתק'; setTimeout(function () { bt.textContent = 'העתקת התוצאה'; }, 1600); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(tx).then(done, function () { G.prompt('העתיקו את התוצאה', tx); }); else G.prompt('העתיקו את התוצאה', tx);
      }
    });
    function paint() {
      qa('[data-plan]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-plan') === v.plan)); });
      qa('[data-grace]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-grace') === v.grace)); });
      qa('[data-years]').forEach(function (x) { x.setAttribute('aria-pressed', String(+x.getAttribute('data-years') === v.years)); });
      qa('[data-err]').forEach(function (x) { x.textContent = ''; });
      var r;
      try { r = compute(v, D, C); } catch (err) { r = { error: { field: null, msg: 'לא הצלחנו לחשב עם הערכים האלה.' } }; }
      var msg = q('.nlmk__msg'), ok = q('.nlmk__ok');
      if (r.error) {
        var map = { price: 'nlmk-p', equity: 'nlmk-e', sign: 'nlmk-s', delivery: 'nlmk-d', annual: 'nlmk-i' }, fe = r.error.field && q('[data-err="' + map[r.error.field] + '"]');
        if (fe) fe.textContent = r.error.msg;
        msg.textContent = r.error.msg; msg.hidden = false; ok.hidden = true; last = null; q('.nlmk__copy').hidden = true; return;
      }
      msg.hidden = true; ok.hidden = false; q('.nlmk__copy').hidden = false; last = r;
      var hd = headline(r);
      q('.nlmk__ol').textContent = hd.label;
      var fig = q('.nlmk__fig'); fig.className = 'nlmk__fig' + (hd.text ? ' is-text' : ''); fig.innerHTML = '<bdi>' + esc(hd.value) + '</bdi>';
      q('.nlmk__sub').innerHTML = summary(r);
      var lt = q('.nlmk__ltv'); lt.hidden = r.noMortgage; lt.className = 'nlmk__ltv' + (r.over75 ? ' is-over' : ''); if (!r.noMortgage) lt.innerHTML = ltvText(r);
      q('.nlmk__tl').innerHTML = r.rows.map(function (x) { return '<li><span class="nlmk__d">' + mmyyyy(x.date) + '</span><span class="nlmk__t">' + rowText(x, r) + '</span></li>'; }).join('')
        + '<li class="is-keys"><span class="nlmk__d">' + mmyyyy(r.delivery) + '</span><span class="nlmk__t">' + keysText(r) + '</span></li>';
      var ann = (Math.round(r.annual * 1000) / 10).toFixed(1) + '%';
      q('.nlmk__src').innerHTML = 'ההנחה: ההון העצמי משלם את התשלומים הראשונים, כל אחד עם ההצמדה שלו, והשאר נמשך מהמשכנתא; בפועל הבנק קובע מתי משחררים את הכסף. '
        + 'הריבית והתמהיל: הממוצע של כל הבנקים ב' + esc(monthHe(r.month)) + ' (' + (src.page ? '<a href="' + esc(src.page) + '" target="_blank" rel="noopener">בנק ישראל</a>' : 'בנק ישראל') + '), במסלולים הצמודים בלי שינוי במדד. '
        + 'המדד: מדד תשומות הבנייה של <a href="https://www.cbs.gov.il/" target="_blank" rel="noopener">הלמ״ס</a>, המדד הידוע בכל תאריך, ובחודשים שעוד לא פורסמו <bdi>' + ann + '</bdi> בשנה'
        + (r.annualDefault ? ' (12 החודשים האחרונים)' : ' (כפי שהקלדתם)') + '. '
        + (r.newLaw ? 'ההצמדה לפי <a href="https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%9B%D7%A8_(%D7%93%D7%99%D7%A8%D7%95%D7%AA)" target="_blank" rel="noopener">חוק המכר, סעיף 5ג</a>.'
          : 'חוזה לפני 7.7.2022: ההצמדה לפי החוזה; כאן כל תשלום מוצמד במלואו, הגבול העליון.')
        + ' ממוצע, לא הצעה אישית.';
    }
    paint();
  }
})();
