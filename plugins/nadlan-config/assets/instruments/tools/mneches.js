/* NadLan Instruments · mneches v1 (HAD-675, 6.11.2026): "כמה אפשר לקבל על דירה קיימת", the loan a bank may give against a home the
   reader already owns, for the tools switcher of /mortgage-calculator/ (pane #tool-neches). LOCAL build, not released.
   The two limits of Bank of Israel directive 329, version 13 (circular 2852, 30.6.2026, fetched from boi.org.il 6.11.2026) and its
   Q&A file of 8.2.2026:
   - LTV: a loan secured by a home that is not for buying, building or renovating one ("לכל מטרה") is limited to 50% of the pledged
     home (Q&A 2.2 and 8.2), together with the balance of earlier loans on the same home (section 4). A bank MAY go to 70%, if the part
     above 50% is at most 200,000 ILS, summed over all loans on the home (section 10a, Q&A 2.31): shown as a second figure, never the
     headline. Buying another home on the existing one: at most 50% of the pledged home (Q&A 2.1), and the new home has its own cap
     (section 2). Parents helping a child: an any-purpose loan, 50% of their home (Q&A 2.7); the 70% relief is not applied to it.
   - PTI: the monthly payment up to 50% of disposable income (section 5); disposable = net income minus fixed costs of more than 18
     months (Annex A 1.2); from 1.10.2026 the payment includes earlier loans on the same home with more than 18 months left (Annex A
     1.1, start date moved by circular 2852). Any-purpose loans up to 120,000 ILS, summed, are outside the PTI limit (sections 11,
     12.2, Q&A 8.3).
   The rate: the Bank of Israel average of new any-purpose loans secured by a home (SDMX BIR_MRTG_99, 8.2026, two tracks by volume,
   rate / 12 as published, data/mneches.json), or the average housing mix of all banks (boi-mortgage.json by_bank, effective rates
   turned monthly, the same per-shekel payment as mquick.js), or a rate the reader types. Spitzer, CPI unchanged.
   Worked example (node test): 2,800,000 ILS, balance 350,000, any purpose: 50% = 1,400,000, minus 350,000 = 1,050,000 by the LTV rule.
   Pure logic in window.NLNC (docs/research/2026-11-06-mortgage-universe/build/build-mneches/test_mneches.js). Hebrew only, RTL; on an
   English mount the tool draws nothing. Nothing is sent: the case lives in #mneches= only, written when the reader asks for a link. */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;

  var PURPOSES = [
    { k: 'any', he: 'לכל מטרה', rule: 'any_ltv', relief: true, exempt: true, src: 'anyp' },
    { k: 'buy', he: 'לקניית דירה נוספת', rule: 'pledged_for_purchase', relief: false, exempt: false, src: 'home' },
    { k: 'kids', he: 'עזרה לילדים בקניית דירה', rule: 'parents', relief: false, exempt: false, src: 'anyp' },
    { k: 'close', he: 'סגירת הלוואות', rule: 'any_ltv', relief: true, exempt: true, src: 'anyp' }
  ];
  var TERMS = [10, 15, 20, 25, 30];
  var SRCS = [{ k: 'anyp', he: 'ממוצע לכל מטרה' }, { k: 'home', he: 'ממוצע משכנתאות' }, { k: 'own', he: 'ריבית שקיבלתם' }];
  var TK = ['fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi'];
  var TNAME = { fixed_nl: 'קבועה לא צמודה', prime: 'פריים', var_nl_other: 'משתנה לא צמודה', var_cpi: 'משתנה צמודה', fixed_cpi: 'קבועה צמודה' };
  var HEM = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];

  /* ------------------------------------------------------------------------------------------------------------- helpers */
  var NF = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function nf(x) { return NF.format(Math.round(x || 0)); }
  function ils(x) { return nf(x) + ' ₪'; }
  function neg(x) { return '−' + ils(x); }  // U+2212, a minus sign
  function pc(f, d) { var s = (100 * f).toFixed(d == null ? 0 : d); return s + '%'; }
  function pn(x, d) { return (+x).toFixed(d == null ? 2 : d) + '%'; }
  function month(k) { var p = String(k || '').split('-'); return p.length === 2 ? (HEM[+p[1] - 1] || p[1]) + ' ' + p[0] : String(k || ''); }
  function dmy(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : ''; }
  function money(x) { if (typeof x === 'number') return isFinite(x) ? x : NaN; var s = String(x == null ? '' : x).replace(/[^\d.]/g, ''); if (s === '' || s === '.') return NaN; var n = +s; return isFinite(n) ? n : NaN; }
  function money0(x) { return String(x == null ? '' : x).trim() === '' ? 0 : money(x); }  // optional: empty = 0
  function rateNum(x) { var s = String(x == null ? '' : x).trim(); if (s.indexOf('.') < 0) s = s.replace(',', '.'); s = s.replace(/[^\d.]/g, ''); if (s === '' || s === '.') return NaN; var n = +s; return isFinite(n) ? n : NaN; }
  function pmt(P, r, n) { return r > 0 ? P * r / (1 - Math.pow(1 + r, -n)) : P / n; }
  function down(x) { return Math.floor(x + 1e-6); }  // a limit never rounds up
  function err(field, msg) { return { error: { field: field, msg: msg } }; }
  function purpose(k) { for (var i = 0; i < PURPOSES.length; i++) if (PURPOSES[i].k === k) return PURPOSES[i]; return PURPOSES[0]; }

  function defaults() { return { value: 2800000, balance: 350000, epay: 3150, purpose: 'any', income: 25000, other: 1500, years: 20, src: 'auto', rate: '' }; }

  /* the numbers of the rules: LTV, PTI and term from boi-mortgage.json (rules, the file every mortgage tool reads), the rest from
     mneches.json; a missing value in boi-mortgage.json falls back to mneches.json */
  function rules(D, N) {
    var RU = (D && D.rules) || {}, AP = RU.any_purpose || {}, NR = N.rules;
    function pick(a, b) { return a != null && isFinite(+a) ? +a : +b; }
    return {
      any: pick(AP.ltv, NR.any_ltv.value), upto: pick(AP.ltv_upto, NR.relief.ltv_upto), above: pick(AP.above_cap, NR.relief.above_cap),
      pti: pick(RU.pti_max, NR.pti_max.value), risk: pick(RU.pti_risk, NR.pti_risk.value), termMax: pick(RU.term_max, NR.term_max.value),
      exempt: +NR.pti_exempt.value, months18: +NR.same_asset.months, buyCap: +NR.pledged_for_purchase.value, kidsCap: +NR.parents.value,
      single: pick(RU.ltv && RU.ltv.single, NR.purchase_ltv.single), replace: pick(RU.ltv && RU.ltv.replace, NR.purchase_ltv.replace), invest: pick(RU.ltv && RU.ltv.invest, NR.purchase_ltv.invest)
    };
  }
  function capOf(P, R) { return P.k === 'buy' ? R.buyCap : P.k === 'kids' ? R.kidsCap : R.any; }

  /* the rate: rows of { he, share, r (monthly), annual, linked } */
  function srcKey(v) { return v.src === 'auto' || !v.src ? purpose(v.purpose).src : v.src; }
  function rateSet(key, D, N, own) {
    if (key === 'own') { var x = rateNum(own); return { key: 'own', month: null, rows: [{ he: 'הריבית שהקלדתם', share: 1, r: x / 1200, annual: x, linked: false }] }; }
    if (key === 'home') {
      var BB = D && D.by_bank, row = BB && BB.latest ? BB.latest.table.filter(function (t) { return t.bank === 'system'; })[0] : null; if (!row) return null;
      var tot = TK.reduce(function (a, k) { return a + (row[k] ? +row[k].share : 0); }, 0) || 1;
      return { key: 'home', month: BB.latest.month, rows: TK.filter(function (k) { return row[k] && +row[k].share > 0; }).map(function (k) {
        return { k: k, he: TNAME[k], share: row[k].share / tot, r: Math.pow(1 + row[k].rate / 100, 1 / 12) - 1, annual: row[k].rate, linked: /cpi/.test(k) }; }) };
    }
    var A = N && N.anyp; if (!A) return null;
    var vt = A.tracks.reduce(function (a, t) { return a + t.vol_k; }, 0) || 1;
    return { key: 'anyp', month: A.month, rows: A.tracks.map(function (t) { return { k: t.k, he: t.he, share: t.vol_k / vt, r: t.rate / 1200, annual: t.rate, linked: t.linked }; }) };
  }
  function per1(rs, years) { var n = Math.round(years * 12); return rs.rows.reduce(function (a, t) { return a + t.share * pmt(1, t.r, n); }, 0); }

  /* one term: the most by income (with the 120,000 exemption where it applies), the amount, the payment and the total */
  function atTerm(c, rs, years) {
    var p1 = per1(rs, years), n = years * 12, inc = c.payRoom > 0 ? down(c.payRoom / p1) : 0;
    var exemptOn = c.P.exempt && c.ltvRoom > 0 && inc < c.exemptAmt, best, binds, gap = null;
    if (!(c.ltvRoom > 0)) { best = 0; binds = 'ltv'; }
    else if (exemptOn) { best = c.exemptAmt; binds = c.exemptAmt >= c.ltvRoom ? 'ltv' : 'exempt'; }
    else if (inc < c.ltvRoom) { best = inc; binds = 'income'; gap = c.ltvRoom - inc; }
    else { best = c.ltvRoom; binds = 'ltv'; gap = inc - c.ltvRoom; }
    var pay = best * p1, total = pay * n;
    return { years: years, n: n, per1: p1, incMax: inc, exemptOn: exemptOn, best: best, binds: binds, gap: gap, pay: pay, total: total, interest: total - best };
  }

  function compute(v, D, N) {
    if (!N || !N.rules || !N.anyp) return err(null, 'הנתונים לא נטענו. רעננו את העמוד.');
    var R = rules(D, N), P = purpose(v.purpose);
    var value = money(v.value), balance = money0(v.balance), income = money(v.income), other = money0(v.other), years = +v.years;
    if (!(value >= 100000 && value <= 100000000)) return err('value', 'הקלידו את שווי הדירה בשקלים, למשל 2,800,000.');
    if (!(balance >= 0)) return err('balance', 'הקלידו את יתרת המשכנתא, או 0 אם אין.');
    var epay = 0;
    if (balance > 0) { epay = money(v.epay); if (!(epay >= 0)) return err('epay', 'הקלידו את ההחזר החודשי על המשכנתא הקיימת.'); }
    if (!(income >= 0)) return err('income', 'הקלידו את ההכנסה נטו של משק הבית בחודש.');
    if (!(other >= 0)) return err('other', 'הקלידו את ההחזרים החודשיים, או 0 אם אין.');
    if (!(years >= 1 && years <= R.termMax && Math.round(years) === years)) return err('years', 'תקופה בשנים שלמות, עד ' + R.termMax + '.');
    var key = srcKey(v);
    if (key === 'own') { var rn = rateNum(v.rate); if (!(rn >= 0 && rn <= 20)) return err('rate', 'הקלידו ריבית שנתית בין 0% ל־20%, למשל 6.2.'); }
    var rs = rateSet(key, D, N, v.rate); if (!rs) return err(null, 'הנתונים לא נטענו. רעננו את העמוד.');
    var capR = capOf(P, R), cap = down(capR * value), ltvRoom = Math.max(0, cap - balance);
    var reliefCap = P.relief ? down(Math.min(R.upto * value, R.any * value + R.above)) : null, reliefRoom = P.relief ? Math.max(0, reliefCap - balance) : null;
    var disp = income - other, half = Math.max(0, R.pti * disp), payRoom = Math.max(0, half - epay);
    var c = { P: P, ltvRoom: ltvRoom, payRoom: payRoom, exemptAmt: P.exempt ? Math.min(R.exempt, ltvRoom) : 0 };
    var T = atTerm(c, rs, years);
    var table = TERMS.map(function (y) { return y <= R.termMax ? atTerm(c, rs, y) : null; }).filter(Boolean);
    var kind = !(ltvRoom > 0) ? 'noroom' : !(T.best > 0) ? 'noincome' : 'ok';
    return { v: v, P: P, R: R, rs: rs, key: key, value: value, balance: balance, epay: epay, income: income, other: other, years: years,
      capR: capR, cap: cap, ltvRoom: ltvRoom, reliefCap: reliefCap, reliefRoom: reliefRoom, balPct: balance / value,
      disp: disp, half: half, payRoom: payRoom, incMax: T.incMax, exemptOn: T.exemptOn, exemptAmt: c.exemptAmt, best: T.best, binds: T.binds, gap: T.gap,
      pay: T.pay, n: T.n, total: T.total, interest: T.interest, per1: T.per1, kind: kind,
      ptiAfter: disp > 0 ? (epay + T.pay) / disp : null, table: table };
  }

  /* ---------------------------------------------------------------------------------------------------------------- words */
  function rateShort(r) {
    return r.key === 'own' ? 'בריבית ' + pn(r.rs.rows[0].annual) : r.key === 'home' ? 'בתמהיל הממוצע של המשכנתאות, ' + month(r.rs.month) : 'בממוצע ההלוואות לכל מטרה, ' + month(r.rs.month);
  }
  /* the opening value of "ריבית שקיבלתם": the Bank of Israel fixed not linked average of the same SDMX month, for the purpose's kind of loan */
  function ownStart(P, N) { return P.k === 'buy' ? N.anyp.housing_fixed.nl.rate : N.anyp.fixed.nl.rate; }
  function rateHelp(key, rs, N, P) {
    if (key === 'own') return 'הריבית השנתית מההצעה שקיבלתם. בכל חודש: הריבית חלקי 12, לוח שפיצר. נקודת פתיחה: ' + pn(ownStart(P, N)) + ', הממוצע של בנק ישראל בקבועה לא צמודה ' + (P.k === 'buy' ? 'במשכנתאות לדיור' : 'בהלוואות לכל מטרה') + ', ' + month(N.anyp.month) + '.';
    var parts = rs.rows.map(function (t) { return t.he + ' ' + pn(t.annual) + ' (' + pc(t.share) + ' מהכסף)'; }).join(', ');
    if (key === 'anyp') return 'הממוצע של בנק ישראל בהלוואות חדשות לכל מטרה בשעבוד דירה, ' + month(rs.month) + ': ' + parts + '. חישבנו את הריבית שפורסמה חלקי 12, לוח שפיצר, בלי שינוי במדד.';
    var F = N.anyp.fixed, H = N.anyp.housing_fixed;
    return 'התמהיל והריבית הממוצעים במשכנתאות חדשות לדיור בכל הבנקים, ' + month(rs.month) + ' (בנק ישראל): ' + parts + '.'
      + (P.k === 'buy' ? '' : ' בהלוואות לכל מטרה בשעבוד דירה הריבית הממוצעת גבוהה יותר: בקבועה לא צמודה ' + pn(F.nl.rate) + ' מול ' + pn(H.nl.rate) + ' במשכנתאות, ' + month(N.anyp.month) + '.');
  }
  function headline(r) {
    if (r.kind === 'noroom') return { label: 'כמה אפשר לקבל על הדירה', value: 'אין מקום להלוואה נוספת', text: true };
    if (r.kind === 'noincome') return { label: 'כמה אפשר לקבל על הדירה', value: 'אין מקום לפי ההכנסה', text: true };
    return { label: 'כמה אפשר לקבל על הדירה, לפי שני הכללים של בנק ישראל', value: ils(r.best), text: false };
  }
  function sub(r) {
    var R = r.R;
    if (r.kind === 'noroom') {
      var s = 'יתרת המשכנתא, ' + ils(r.balance) + ', היא ' + pc(r.balPct, 1) + ' משווי הדירה, ובנק ישראל מתיר כאן עד ' + pc(r.capR) + ' יחד עם היתרה.';
      if (r.P.relief) s += r.reliefRoom > 0 ? ' בשיקול דעת הבנק אפשר עד ' + pc(R.upto) + ', כשהחלק שמעל ' + pc(R.any) + ' עד ' + ils(R.above) + ': עד ' + ils(r.reliefRoom) + '.' : ' גם בהקלה של סעיף 10א, עד ' + pc(R.upto) + ', אין מקום.';
      return s;
    }
    if (r.kind === 'noincome') return 'ההחזרים הקיימים כבר מגיעים ל־' + pc(R.pti) + ' מההכנסה הפנויה, ' + ils(r.disp) + ' בחודש. לפי כלל המימון היה מקום עד ' + ils(r.ltvRoom) + '.';
    var line = r.binds === 'income'
      ? 'ההכנסה קובעת: החזר של עד ' + ils(r.payRoom) + ' בחודש נושא ' + ils(r.incMax) + ' ל־' + r.years + ' שנה. לפי כלל המימון אפשר היה עד ' + ils(r.ltvRoom) + ', ' + ils(r.gap) + ' יותר.'
      : r.binds === 'exempt'
        ? 'לפי ההכנסה רק ' + ils(r.incMax) + ', אבל הלוואה לכל מטרה של עד ' + ils(R.exempt) + ' פטורה ממגבלת ההחזר מההכנסה, וההחלטה נשארת של הבנק.'
        : 'כלל המימון קובע: ' + pc(r.capR) + ' משווי הדירה פחות היתרה.' + (r.exemptOn ? ' לפי ההכנסה רק ' + ils(r.incMax) + ', אבל עד ' + ils(R.exempt) + ' ההלוואה פטורה ממגבלת ההחזר.' : ' לפי ההכנסה אפשר עד ' + ils(r.incMax) + ', ' + ils(r.gap) + ' יותר.');
    return line + ' החזר ראשון ' + ils(r.pay) + ' בחודש ל־' + r.years + ' שנה.';
  }
  function capLabel(r) {
    var p = pc(r.capR);
    return r.P.k === 'buy' ? p + ' משווי הדירה המשועבדת, כשקונים דירה אחרת' : r.P.k === 'kids' ? p + ' משווי הבית, בהלוואה של הורים לעזרה בהון העצמי' : p + ' משווי הדירה, המימון המרבי בהלוואה לכל מטרה';
  }
  /* the ledger: { label, value, kind, src: [rule keys], tag, note } */
  function lines(r) {
    var R = r.R, L = [];
    function add(label, value, kind, src, tag, note) { L.push({ label: label, value: value, kind: kind || 'n', src: src || [], tag: tag || '', note: note || '' }); }
    add('שווי הדירה היום', ils(r.value));
    add(capLabel(r), ils(r.cap), 'n', [r.P.rule]);
    add('פחות יתרת המשכנתא על הדירה', r.balance > 0 ? neg(r.balance) : 'אין משכנתא', r.balance > 0 ? 'n' : 'he', ['prior_loans']);
    add('לפי כלל המימון', r.ltvRoom > 0 ? ils(r.ltvRoom) : 'אין מקום', 'sum', [], r.kind !== 'noincome' && r.binds !== 'income' && r.binds !== 'exempt' ? 'קובע' : '',
      r.ltvRoom > 0 && r.binds === 'income' ? 'מרווח של ' + ils(r.gap) + ' מעל מה שההכנסה מאפשרת.' : '');
    if (r.P.relief) add('בשיקול דעת הבנק: עד ' + pc(R.upto) + ', כשהחלק שמעל ' + pc(R.any) + ' עד ' + ils(R.above) + ' בכל ההלוואות על הדירה', r.reliefRoom > 0 ? ils(r.reliefRoom) : 'אין מקום', 'alt', ['relief']);
    add('הכנסה פנויה: נטו פחות החזרי הלוואות אחרות', ils(r.disp), 'n', ['fixed_costs']);
    add(pc(R.pti) + ' ממנה, התקרה להחזר החודשי', ils(r.half), 'n', ['pti_max']);
    if (r.balance > 0) add('פחות ההחזר על המשכנתא הקיימת', neg(r.epay), 'n', ['same_asset']);
    add('נשאר להחזר חודשי חדש', r.payRoom > 0 ? ils(r.payRoom) : 'אין', r.payRoom > 0 ? 'n' : 'he');
    add('לפי ההכנסה, ל־' + r.years + ' שנה ' + rateShort(r), r.incMax > 0 ? ils(r.incMax) : 'אין מקום', 'sum', [], r.binds === 'income' ? 'קובע' : '',
      r.binds === 'ltv' && r.gap > 0 && !r.exemptOn ? 'מרווח של ' + ils(r.gap) + ' מעל כלל המימון.' : '');
    if (r.exemptOn) add('הלוואה לכל מטרה עד ' + ils(R.exempt) + ', במצטבר, פטורה ממגבלת ההחזר מההכנסה', ils(r.exemptAmt), 'alt', ['pti_exempt'], r.binds === 'exempt' ? 'קובע' : '');
    if (r.best > 0) {
      add('ההחזר החודשי הראשון', ils(r.pay), 'key');
      add('סך ההחזרים ל־' + r.years + ' שנה, בלי שינוי במדד', ils(r.total));
      add('מזה ריבית', ils(r.interest));
    }
    if (r.ptiAfter != null) add('ההחזר מההכנסה אחרי ההלוואה', pc(r.ptiAfter, 1), 'n', r.ptiAfter > R.risk ? ['pti_risk'] : [], '',
      r.ptiAfter > R.risk + 1e-9 ? 'מעל ' + pc(R.risk) + ' הבנק נדרש להחזיק יותר הון כנגד ההלוואה (סעיף 6).' : '');
    return L;
  }
  function purposeNote(r) {
    var R = r.R;
    if (r.P.k === 'buy') return 'לקניית דירה נוספת: גם לדירה שקונים יש תקרה משלה, ' + pc(R.single) + ' לדירה יחידה, ' + pc(R.replace) + ' לדירה חלופית ו־' + pc(R.invest) + ' לדירה להשקעה (סעיף 2), והבנק בודק את שתי הדירות.';
    if (r.P.k === 'kids') return 'עזרה לילדים: הורים יכולים לקחת הלוואה בשעבוד הבית שלהם כדי לעזור בהון העצמי, והיא נחשבת הלוואה לכל מטרה, עד ' + pc(R.kidsCap) + ' משווי הבית (שו"ת 2.7). ההקלה עד ' + pc(R.upto) + ' לא חושבה כאן. אם אתם גם ערבים למשכנתא של הילד, הבנק מכיר לכל היותר במחצית מההכנסה הפנויה שלכם (נספח א, סעיף 1.3).';
    if (r.P.k === 'close') return 'סגירת הלוואות: אל תכללו בשדה ההלוואות האחרות את ההחזרים של ההלוואות שייסגרו מהכסף. סגירה של משכנתא קיימת היא מחזור, והיא נשארת במטרה המקורית שלה (שו"ת 7.7).';
    return 'לכל מטרה: הלוואה בשעבוד דירת מגורים שאינה לקנייה, לבנייה, להרחבה או לשיפוץ של דירה (שו"ת 2.2). שיפוץ או בנייה מסווגים אחרת.';
  }
  function copyText(r, N) {
    var t = 'כמה אפשר לקבל על דירה קיימת: דירה בשווי ' + ils(r.value) + (r.balance > 0 ? ' עם יתרת משכנתא של ' + ils(r.balance) : ' בלי משכנתא') + ', ' + r.P.he + '. ';
    t += 'לפי כלל המימון של בנק ישראל (' + pc(r.capR) + ' יחד עם היתרה): ' + (r.ltvRoom > 0 ? 'עד ' + ils(r.ltvRoom) : 'אין מקום') + '. ';
    t += 'לפי ההכנסה, ל־' + r.years + ' שנה: ' + (r.incMax > 0 ? 'עד ' + ils(r.incMax) : 'אין מקום') + '. ';
    if (r.best > 0) t += 'אפשר לקבל עד ' + ils(r.best) + ', החזר ראשון ' + ils(r.pay) + ' בחודש.';
    else t += headline(r).value + '.';
    return t + ' (הוראה 329 של בנק ישראל, גרסה ' + N.sources.D329.version + ', נבדק ב־' + dmy(N.checked) + ')';
  }
  function dataLine(N, D) {
    var A = N.anyp, avg = 1000 * A.volume_k.value / A.loans.value;
    return 'ב' + month(A.month) + ' נתנו הבנקים ' + nf(A.loans.value) + ' הלוואות חדשות לכל מטרה בשעבוד דירה, ' + (A.volume_k.value / 1000).toFixed(1) + ' מיליון ₪, כ־' + nf(Math.round(avg / 1000)) + ' אלף ₪ בממוצע להלוואה. '
      + 'ההחזר הממוצע: ' + pn(A.pti.value) + ' מההכנסה. הריבית הממוצעת: ' + A.tracks.map(function (t) { return pn(t.rate) + ' ב' + t.he; }).join(' ו־') + '; בקבועה לא צמודה ' + pn(A.fixed.nl.rate) + ', מול ' + pn(A.housing_fixed.nl.rate) + ' במשכנתאות לדיור באותו חודש.';
  }
  function bands(N) { var rows = N.anyp.ltv_bands.rows, tot = rows.reduce(function (a, x) { return a + x.vol_k; }, 0) || 1; return rows.map(function (x) { return { label: x.to == null ? 'מעל ' + x.from + '%' : (x.from ? x.from + '% עד ' : 'עד ') + x.to + '%', share: x.vol_k / tot }; }); }

  /* the case in the address: #mneches=... (base64url of a short JSON) */
  var HK = { a: 'value', b: 'balance', c: 'epay', p: 'purpose', i: 'income', o: 'other', y: 'years', s: 'src', r: 'rate' };
  function b64e(s) { return typeof btoa === 'function' ? btoa(unescape(encodeURIComponent(s))) : Buffer.from(s, 'utf8').toString('base64'); }
  function b64d(s) { return typeof atob === 'function' ? decodeURIComponent(escape(atob(s))) : Buffer.from(s, 'base64').toString('utf8'); }
  function enc(v) { var o = {}; Object.keys(HK).forEach(function (k) { o[k] = v[HK[k]]; }); return b64e(JSON.stringify(o)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); }
  function dec(s) {
    try {
      var b = String(s).replace(/-/g, '+').replace(/_/g, '/'); while (b.length % 4) b += '=';
      var o = JSON.parse(b64d(b)), v = defaults();
      Object.keys(HK).forEach(function (k) { if (o[k] == null) return; var f = HK[k], x = o[k];
        if (f === 'purpose') { if (PURPOSES.some(function (p) { return p.k === x; })) v.purpose = x; }
        else if (f === 'src') { if (x === 'auto' || SRCS.some(function (p) { return p.k === x; })) v.src = x; }
        else if (f === 'years') { if (TERMS.indexOf(+x) > -1) v.years = +x; }
        else if (f === 'rate') v.rate = String(x).slice(0, 8);
        else if (isFinite(+x) && +x >= 0) v[f] = +x; });
      return v;
    } catch (e) { return null; }
  }

  G.NLNC = { PURPOSES: PURPOSES, TERMS: TERMS, SRCS: SRCS, defaults: defaults, rules: rules, rateSet: rateSet, per1: per1, pmt: pmt, compute: compute,
    headline: headline, sub: sub, lines: lines, purposeNote: purposeNote, copyText: copyText, dataLine: dataLine, bands: bands, rateHelp: rateHelp, rateShort: rateShort,
    srcKey: srcKey, enc: enc, dec: dec, money: money, rateNum: rateNum, ownStart: ownStart };
  if (!G.NadLanInstruments || typeof document === 'undefined') return;

  /* ------------------------------------------------------------------------------------------------------------ the page */
  var NI = G.NadLanInstruments, esc = NI.esc;
  var C = '#nlnc', HEB = /[א-ת]/;
  var CSS = [
    C + '{display:flex;flex-direction:column;gap:14px}' + C + ' *{box-sizing:border-box}' + C + ' [hidden]{display:none!important}',
    C + ' p.nli__lede{margin:0!important}',
    C + ' .nlnc__grid{display:grid;grid-template-columns:minmax(0,1fr);grid-template-areas:"a" "r" "m";gap:16px;position:relative}',
    '@media (min-width:960px){' + C + ' .nlnc__grid{grid-template-columns:minmax(0,420px) minmax(0,1fr);grid-template-areas:"a r" "m m";gap:20px 32px;align-items:start}}',
    C + ' .nlnc__fa{grid-area:a;display:flex;flex-direction:column;gap:12px;min-width:0}' + C + ' .nlnc__res{grid-area:r;display:flex;flex-direction:column;gap:12px;min-width:0}' + C + ' .nlnc__more{grid-area:m;min-width:0}',
    C + ' p.nlnc__sec{margin:4px 0 0!important;padding:8px 0 0!important;border-top:1px solid var(--nli-line,#D3DCE2);font:600 14px/20px var(--nli-sans)!important;color:var(--nli-sea-deep,#1F4B5C)!important}',
    C + ' p.nlnc__sec:first-child{border-top:0;padding-top:0!important}',
    C + ' .nlnc__x2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;align-items:start}',
    C + ' .nli__f>label,' + C + ' .nli__f>.nli__lab{font:500 13px/18px var(--nli-sans)!important;color:var(--nli-ink,#12202A)!important;margin:0!important}',
    C + ' .nli__in{min-height:48px;border-color:#9FB3BF}',
    C + ' .nli__in input{font:500 17px/24px var(--nli-mono)!important;min-height:46px!important;height:auto!important;width:100%!important;max-width:100%!important;padding:10px 12px!important}',
    C + ' .nli__unit{min-width:40px;justify-content:center}',
    C + ' .nlnc__seg{display:grid;grid-template-columns:repeat(var(--n,2),minmax(0,1fr));gap:6px}',
    C + ' .nlnc__seg button{min-height:44px!important;height:auto!important;margin:0!important;padding:6px 6px!important;border-radius:2px!important;border:1px solid var(--nli-line,#D3DCE2)!important;background:#fff!important;color:var(--nli-ink2,#3E4C58)!important;font:400 14px/1.3 var(--nli-sans)!important;box-shadow:none!important;cursor:pointer;text-align:center;text-transform:none!important;letter-spacing:0!important;width:auto!important;white-space:normal!important}',
    C + ' .nlnc__seg button[aria-pressed="true"]{background:var(--nli-sea,#2F6F86)!important;border-color:var(--nli-sea,#2F6F86)!important;color:#fff!important;font-weight:600!important}',
    C + ' .nlnc__seg.is-num button{font-family:var(--nli-mono)!important;font-size:15px!important}',
    C + ' .nli__help{display:block;font:400 12px/18px var(--nli-sans)!important;color:var(--nli-mute,#5E6A75)!important}',
    C + ' .nli__err{display:block}' + C + ' .nli__err:empty{display:none}',
    C + ' .nlnc__out{display:flex;flex-direction:column;gap:6px;border-top:2px solid var(--nli-ink,#12202A);padding-top:12px}',
    C + ' .nlnc__al{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}',
    C + ' .nlnc__eg{font:500 12px/16px var(--nli-sans);color:var(--nli-mute,#5E6A75);border:1px solid var(--nli-line,#D3DCE2);border-radius:999px;padding:2px 10px;white-space:nowrap}',
    C + ' .nlnc__fig{display:block;font:500 40px/46px var(--nli-mono)!important;color:var(--nli-ink,#12202A)!important;font-variant-numeric:tabular-nums;text-decoration:underline;text-decoration-color:var(--nli-sea,#2F6F86);text-decoration-thickness:2px;text-underline-offset:9px;margin:2px 0 8px}',
    C + ' .nlnc__fig.is-text{font:600 26px/34px var(--nli-sans)!important;text-decoration-color:var(--nli-survey,#C42550)}',
    C + ' p.nlnc__sub{margin:0!important;font:400 14px/22px var(--nli-sans)!important;color:var(--nli-ink2,#3E4C58)!important}',
    C + ' p.nlnc__msg{margin:0!important;padding:10px 12px!important;background:var(--nli-ground,#F6F8F9);border-inline-start:3px solid var(--nli-survey,#C42550);font:500 14px/22px var(--nli-sans)!important;color:var(--nli-ink,#12202A)!important}',
    /* the deed bar: the home's value, split into the balance, the amount, the room to the cap and the relief zone, with the 50% and 70% marks */
    C + ' .nlnc__deed{display:flex;flex-direction:column;gap:6px;margin:6px 0 2px}',
    C + ' .nlnc__bar{position:relative;display:flex;height:18px;border:1px solid var(--nli-ink,#12202A);border-radius:2px;background:#fff;overflow:visible}',
    C + ' .nlnc__bar i{display:block;height:100%}' + C + ' .nlnc__bar i.b{background:var(--nli-sea-deep,#1F4B5C)}' + C + ' .nlnc__bar i.n{background:var(--nli-sea,#2F6F86)}',
    C + ' .nlnc__bar i.u{background:repeating-linear-gradient(135deg,#DCE7EC 0 4px,#fff 4px 8px)}' + C + ' .nlnc__bar i.x{background:repeating-linear-gradient(135deg,#fff 0 5px,#EEF2F4 5px 7px);border-inline-start:1px dashed var(--nli-sea,#2F6F86)}',
    C + ' .nlnc__bar i.o{background:var(--nli-survey,#C42550)}',
    C + ' .nlnc__mk{position:absolute;top:-5px;bottom:-5px;width:0;border-inline-start:2px solid var(--nli-ink,#12202A)}',
    C + ' .nlnc__mk span{position:absolute;top:100%;margin-top:3px;transform:translateX(50%);font:500 11px/14px var(--nli-mono);color:var(--nli-ink,#12202A);white-space:nowrap}',
    C + ' .nlnc__mk.is-x{border-inline-start-style:dashed;border-color:var(--nli-sea,#2F6F86)}' + C + ' .nlnc__mk.is-x span{top:auto;bottom:100%;margin:0 0 3px;color:var(--nli-sea,#2F6F86)}',
    C + ' .nlnc__deed.has-x{padding-top:16px}',
    C + ' ul.nlnc__lg{display:flex;flex-wrap:wrap;gap:4px 14px;list-style:none!important;margin:14px 0 0!important;padding:0!important;font:400 12px/16px var(--nli-sans);color:var(--nli-ink2,#3E4C58)}',
    C + ' ul.nlnc__lg li{margin:0!important;padding:0!important;display:flex;gap:6px;align-items:center;list-style:none!important;background:none!important}' + C + ' ul.nlnc__lg li::before{display:none!important}',
    C + ' ul.nlnc__lg b{display:inline-block;width:10px;height:10px;border:1px solid var(--nli-ink,#12202A)}',
    /* the ledger */
    C + ' ol.nlnc__ls{list-style:none!important;margin:4px 0 0!important;padding:0!important;display:flex;flex-direction:column}',
    C + ' ol.nlnc__ls>li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 12px;margin:0!important;padding:7px 0!important;border-bottom:1px solid var(--nli-line,#D3DCE2);list-style:none!important;background:none!important}',
    C + ' ol.nlnc__ls>li::before,' + C + ' ol.nlnc__ls>li::marker{content:none!important;display:none!important}',
    C + ' .nlnc__lk{font:400 14px/21px var(--nli-sans)!important;color:var(--nli-ink,#12202A)!important}',
    C + ' .nlnc__lv{font:500 15px/21px var(--nli-mono)!important;color:var(--nli-ink,#12202A)!important;white-space:nowrap;text-align:left}',
    C + ' li.is-he .nlnc__lv,' + C + ' .nlnc__lv.is-t,' + C + ' table.nlnc__t td.n.is-t{font-family:var(--nli-sans)!important;font-size:14px!important}',
    C + ' li.is-sum{border-bottom:2px solid var(--nli-line,#D3DCE2)!important}' + C + ' li.is-sum .nlnc__lk{font-weight:600!important}',
    C + ' li.is-alt .nlnc__lk,' + C + ' li.is-alt .nlnc__lv{color:var(--nli-ink2,#3E4C58)!important;font-size:13px!important}',
    C + ' ol.nlnc__ls>li.is-key{background:var(--nli-ground,#F6F8F9)!important;border-inline-start:3px solid var(--nli-sea,#2F6F86);padding:9px 10px!important;margin-top:4px!important}' + C + ' li.is-key .nlnc__lk,' + C + ' li.is-key .nlnc__lv{font-weight:600!important;font-size:16px!important}',
    C + ' .nlnc__tag{display:inline-block;margin-inline-start:8px;padding:0 8px;border-radius:999px;background:var(--nli-sea-deep,#1F4B5C);color:#fff;font:500 11px/18px var(--nli-sans);vertical-align:1px}',
    C + ' .nlnc__ln{grid-column:1/-1;font:400 12px/18px var(--nli-sans)!important;color:var(--nli-mute,#5E6A75)!important}',
    C + ' .nlnc__ln.is-ok{color:var(--nli-open,#4F9A5C)!important;font-weight:500!important}' + C + ' .nlnc__ln.is-warn{color:var(--nli-survey,#C42550)!important;font-weight:500!important}',
    C + ' .nlnc__s{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:2px 10px}',
    C + ' .nlnc__s a{font:400 12px/18px var(--nli-sans)!important;color:var(--nli-sea,#2F6F86)!important;text-decoration:underline!important;text-underline-offset:2px}',
    C + ' p.nlnc__pn{margin:0!important;padding:10px 12px!important;border:1px solid var(--nli-sea-deep,#1F4B5C);border-radius:2px;font:400 14px/22px var(--nli-sans)!important;color:var(--nli-ink,#12202A)!important}',
    C + ' p.nlnc__pn a,' + C + ' p.nlnc__lk2 a,' + C + ' .nlnc__more a{color:var(--nli-sea,#2F6F86)!important;text-decoration:underline!important;text-underline-offset:2px}',
    C + ' p.nlnc__lk2{margin:0!important;font:500 15px/24px var(--nli-sans)!important;color:var(--nli-ink,#12202A)!important}',
    C + ' p.nlnc__fine{margin:0!important;font:400 13px/20px var(--nli-sans)!important;color:var(--nli-ink2,#3E4C58)!important}',
    C + ' p.nlnc__src{margin:0!important;font:400 12px/18px var(--nli-sans)!important;color:var(--nli-mute,#5E6A75)!important}' + C + ' p.nlnc__src a{color:var(--nli-sea,#2F6F86)!important}',
    C + ' .nli__share{margin-top:0}',
    /* below: the term table, the rules, the data */
    C + ' .nlnc__more{display:grid;grid-template-columns:minmax(0,1fr);gap:18px;border-top:1px solid var(--nli-line,#D3DCE2);padding-top:14px}',
    '@media (min-width:1100px){' + C + ' .nlnc__more{grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 28px}' + C + ' .nlnc__more>.is-wide{grid-column:1/-1}}',
    C + ' h3.nlnc__mh{margin:0 0 8px!important;padding:0!important;border:0!important;font:600 16px/22px var(--nli-sans)!important;color:var(--nli-sea-deep,#1F4B5C)!important;letter-spacing:0;text-transform:none}',
    C + ' h3.nlnc__mh::before,' + C + ' h3.nlnc__mh::after{display:none!important}',
    C + ' .nlnc__tw{border:1px solid var(--nli-line,#D3DCE2);border-radius:2px;overflow-x:auto}',
    C + ' table.nlnc__t{width:100%;border-collapse:collapse!important;margin:0!important;display:table!important;border:0!important;background:#fff!important}',
    C + ' table.nlnc__t thead{display:table-header-group!important}' + C + ' table.nlnc__t tbody{display:table-row-group!important}' + C + ' table.nlnc__t tr{display:table-row!important}',
    C + ' table.nlnc__t th,' + C + ' table.nlnc__t td{display:table-cell!important;padding:8px!important;border:0!important;border-bottom:1px solid var(--nli-line,#D3DCE2)!important;background:none!important;text-align:right!important;vertical-align:middle;color:var(--nli-ink,#12202A)!important;font:400 14px/20px var(--nli-sans)!important;white-space:nowrap;width:auto!important}',
    C + ' table.nlnc__t th{font:500 12px/16px var(--nli-sans)!important;color:var(--nli-mute,#5E6A75)!important;white-space:normal}',
    C + ' table.nlnc__t td.n{font-family:var(--nli-mono)!important;font-size:13px!important;font-variant-numeric:tabular-nums}',
    C + ' table.nlnc__t tr.is-on td{background:var(--nli-ground,#F6F8F9)!important;font-weight:600!important}',
    C + ' table.nlnc__t td small{display:block;font:400 11px/15px var(--nli-sans)!important;color:var(--nli-mute,#5E6A75)!important;white-space:normal}',
    '@media (max-width:600px){' + C + ' table.nlnc__t thead{display:none!important}' + C + ' table.nlnc__t,' + C + ' table.nlnc__t tbody{display:block!important}'
      + C + ' table.nlnc__t tr{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:6px 12px;padding:10px 12px;border-bottom:1px solid var(--nli-line,#D3DCE2)}'
      + C + ' table.nlnc__t td{display:block!important;border:0!important;padding:0!important;white-space:normal}'
      + C + ' table.nlnc__t td[data-l]::before{content:attr(data-l);display:block;font:500 11px/15px var(--nli-sans);color:var(--nli-mute,#5E6A75)}'
      + C + ' table.nlnc__t td:first-child{grid-column:1/-1;font-weight:600!important}' + C + ' table.nlnc__t tr.is-on{background:var(--nli-ground,#F6F8F9)}}',
    C + ' ul.nlnc__rl{margin:0!important;padding:0!important;display:flex;flex-direction:column;gap:8px}',
    C + ' ul.nlnc__rl li{list-style:none!important;margin:0!important;padding:0 0 8px!important;border-bottom:1px solid var(--nli-line,#D3DCE2);font:400 14px/22px var(--nli-sans)!important;color:var(--nli-ink,#12202A)!important;background:none!important}',
    C + ' ul.nlnc__rl li::before{display:none!important}' + C + ' ul.nlnc__rl li b{font-weight:600;color:var(--nli-sea-deep,#1F4B5C)}',
    C + ' ul.nlnc__rl small{font:400 12px/18px var(--nli-sans)!important;color:var(--nli-mute,#5E6A75)!important}' + C + ' ul.nlnc__rl small a{white-space:nowrap}' + C + ' bdi{white-space:nowrap}',
    C + ' .nlnc__bands{display:flex;flex-direction:column;gap:6px;margin:10px 0 0}',
    C + ' .nlnc__bd{display:grid;grid-template-columns:96px minmax(0,1fr) 52px;gap:8px;align-items:center;font:400 13px/18px var(--nli-sans);color:var(--nli-ink2,#3E4C58)}',
    C + ' .nlnc__bd i{display:block;height:12px;background:var(--nli-sea,#2F6F86);min-width:1px}' + C + ' .nlnc__bd i.is-hi{background:var(--nli-sea-deep,#1F4B5C)}',
    C + ' .nlnc__bd span:last-child{font-family:var(--nli-mono);text-align:left;direction:ltr}',
    C + ' p.nlnc__p{margin:0 0 6px!important;font:400 14px/22px var(--nli-sans)!important;color:var(--nli-ink,#12202A)!important}',
    C + ' button:focus-visible,' + C + ' a:focus-visible{outline:2px solid var(--nli-sea-deep,#1F4B5C)!important;outline-offset:2px}',
    '@media print{' + C + ' .nlnc__fa,' + C + ' .nli__share{display:none!important}}'
  ].join('\n');
  function ensureCss() { if (document.getElementById('nlnc-css')) return; var s = document.createElement('style'); s.id = 'nlnc-css'; s.textContent = CSS; document.head.appendChild(s); }

  NI.register('mneches', {
    custom: function (root, data) {
      if (NI.langOf && NI.langOf(root) === 'en') return;  // Hebrew only
      var D = data.boim || null, N = data.mneches || null;
      if (!N || !N.rules || !N.anyp) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
      build(root, D, N);
    }
  });

  var ICON = { copy: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 7h9v10H7z"/><path d="M4 13V3h9"/></svg>', wa: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16l1-3.2A7 7 0 1 1 7.6 15z"/></svg>',
    link: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M8 12l4-4"/><path d="M9 5l2-2a3 3 0 0 1 4 4l-2 2"/><path d="M11 15l-2 2a3 3 0 0 1-4-4l2-2"/></svg>' };

  function build(root, D, N) {
    ensureCss();
    var v = defaults(), ex = true, fromLink = false;
    var m = /#mneches=([A-Za-z0-9_\-]+)/.exec(location.hash || ''); if (m) { var hv = dec(m[1]); if (hv) { v = hv; ex = false; fromLink = true; } }
    var S = N.sources;
    function srcA(key) {  // a rule key -> its section chip, linked to the official file
      var ru = N.rules[key]; if (!ru) return ''; var s = S[ru.src];
      return '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc('הוראה 329, ' + ru.where) + '</a>';
    }
    function fld(key, lab, o) {
      o = o || {}; var id = 'nlnc-' + key;
      return '<div class="nli__f"' + (o.show ? ' data-v="' + o.show + '"' : '') + '><label for="' + id + '">' + lab + '</label>'
        + '<div class="nli__in"><input id="' + id + '" type="text" inputmode="' + (o.dec ? 'decimal' : 'numeric') + '" autocomplete="off" data-k="' + key + '"' + (o.help ? ' aria-describedby="' + id + '-h"' : '') + '>'
        + '<span class="nli__unit">' + (o.unit || '₪') + '</span></div>'
        + (o.help ? '<span class="nli__help" id="' + id + '-h"' + (o.dyn ? ' data-help="' + key + '"' : '') + '>' + o.help + '</span>' : '')
        + '<span class="nli__err" data-err="' + key + '" aria-live="polite"></span></div>';
    }
    function seg(key, lab, items, o) {
      o = o || {}; var id = 'nlnc-' + key + '-l';
      return '<div class="nli__f"><span class="nli__lab" id="' + id + '">' + lab + '</span>'
        + '<div class="nlnc__seg' + (o.num ? ' is-num' : '') + '" style="--n:' + (o.cols || items.length) + '" role="group" aria-labelledby="' + id + '">'
        + items.map(function (x) { return '<button type="button" data-s="' + key + '" data-val="' + esc(String(x.k)) + '">' + esc(x.he) + '</button>'; }).join('') + '</div>'
        + (o.help || o.dyn ? '<span class="nli__help"' + (o.dyn ? ' data-help="' + key + '"' : '') + '>' + (o.help || '') + '</span>' : '') + '</div>';
    }
    var R0 = rules(D, N);
    var strip = [['מימון בהלוואה לכל מטרה', pc(R0.any)], ['בשיקול דעת הבנק', 'עד ' + pc(R0.upto)], ['החזר מההכנסה', 'עד ' + pc(R0.pti)], ['ריבית לכל מטרה, ' + month(N.anyp.month) + ': לא צמודה · צמודה', pn(N.anyp.tracks[0].rate) + ' · ' + pn(N.anyp.tracks[1].rate)]];
    var h = '<div class="nli__panel" id="nlnc" dir="rtl" lang="he">'
      + '<p class="nli__kicker">מחשבון · הלוואה בשעבוד דירה</p>'
      + '<h2 class="nli__title">כמה אפשר לקבל על דירה קיימת</h2>'
      + '<p class="nli__lede">משכנתא על דירה קיימת, הגדלת משכנתא או הלוואה בשעבוד הדירה: הקלידו את השווי, את יתרת המשכנתא ואת ההכנסה, ותראו כמה הבנק יכול לתת לפי שני הכללים של בנק ישראל, המימון מול שווי הדירה וההחזר מול ההכנסה. החישוב נעשה כאן בדפדפן, ושום נתון לא נשלח.</p>'
      + '<div class="nli__strip">' + strip.map(function (x) { return '<div><span>' + esc(x[0]) + '</span><strong>' + esc(x[1]) + '</strong></div>'; }).join('') + '</div>'
      + '<div class="nlnc__grid"><div class="nlnc__fa">'
      + '<p class="nlnc__sec">הדירה</p>'
      + fld('value', 'שווי הדירה היום', { help: 'לפי שמאות או לפי מחיר של דירות דומות. הבנק יסתמך על השמאי שלו.' })
      + fld('balance', 'יתרת המשכנתא על הדירה', { help: '0 אם אין. כל הלוואה שרשומה על הדירה, בכל בנק או גוף.' })
      + fld('epay', 'ההחזר החודשי על המשכנתא הזו', { show: 'epay', help: 'מ־1.10.2026 הבנק סופר אותו במבחן ההחזר, אם נותרו להלוואה יותר מ־18 חודשים (נספח א, סעיף 1.1).' })
      + '<p class="nlnc__sec">למה הכסף</p>'
      + seg('purpose', 'מטרת ההלוואה', PURPOSES, { cols: 2 })
      + '<p class="nlnc__sec">ההכנסה</p>'
      + '<div class="nlnc__x2">' + fld('income', 'הכנסה נטו של משק הבית בחודש') + fld('other', 'החזרים על הלוואות אחרות בחודש') + '</div>'
      + '<span class="nli__help">הלוואות שנותרו להן יותר מ־18 חודשים, ומזונות אם יש. הבנק מנכה אותן מההכנסה (נספח א, סעיף 1.2).</span>'
      + '<p class="nlnc__sec">התקופה והריבית</p>'
      + seg('years', 'תקופה בשנים', TERMS.map(function (y) { return { k: y, he: String(y) }; }), { num: true })
      + seg('src', 'הריבית לחישוב', SRCS, { cols: 3, help: '', dyn: true })
      + fld('rate', 'הריבית השנתית שקיבלתם', { show: 'rate', unit: '%', dec: true })
      + '</div>'
      + '<div class="nlnc__res"><div class="nlnc__out" aria-live="polite"><p class="nlnc__msg" data-msg hidden></p><div class="nlnc__ok">'
      + '<div class="nlnc__al"><span class="nli__alab" data-lab></span><span class="nlnc__eg" data-eg>דוגמה, שנו כל שדה</span></div>'
      + '<div class="nlnc__fig"></div><p class="nlnc__sub"></p>'
      + '<div class="nlnc__deed" role="img" data-deed></div>'
      + '<ol class="nlnc__ls" aria-label="החישוב שורה אחרי שורה"></ol></div></div>'
      + '<p class="nlnc__pn" data-pn></p>'
      + '<p class="nlnc__lk2">המדריך המלא באתר: <a href="https://nad-lan.co.il/mortgage-calculator/mortgage-for-any-purpose/">משכנתא לכל מטרה</a></p>'
      + '<p class="nlnc__fine">' + esc(N.rules.banks_only.text.replace(/\.$/, '')) + ' לפי ההוראה. חברות ביטוח וגופים חוץ בנקאיים מפרסמים באתרים שלהם שיעורי מימון גבוהים יותר בהלוואה בשעבוד דירה, בריבית ובתנאים שלהם. אנחנו לא ממליצים על גוף מסוים: השוו את העלות הכוללת.</p>'
      + '<p class="nlnc__src">מקור: <a href="' + esc(S.D329.url) + '" target="_blank" rel="noopener">הוראת ניהול בנקאי תקין 329, גרסה ' + S.D329.version + ' (חוזר 2852, ' + dmy(S.D329.date) + ')</a> ו<a href="' + esc(S.QA329.url) + '" target="_blank" rel="noopener">קובץ השאלות והתשובות (' + dmy(S.QA329.date) + ')</a>, באתר בנק ישראל, נבדק ב־' + dmy(N.checked) + '. ריביות: <a href="' + esc(S.SDMX.url) + '" target="_blank" rel="noopener">בנק ישראל, הלוואות לדיור, ' + month(N.anyp.month) + '</a>' + (D && D.by_bank && D.by_bank.src ? ' ו<a href="' + esc(D.by_bank.src.page || D.by_bank.src.url) + '" target="_blank" rel="noopener">השוואת ריביות, ' + month(D.by_bank.latest.month) + '</a>' : '') + '.</p>'
      + '<div class="nli__share" data-share></div>'
      + '</div>'
      + '<div class="nlnc__more">'
      + '<div class="is-wide"><h3 class="nlnc__mh">לפי תקופה</h3><div class="nlnc__tw" data-table></div><span class="nli__help" style="margin-top:6px">אותה דירה, אותה הכנסה ואותה ריבית. תקופה ארוכה יותר מורידה את ההחזר ומגדילה את הסכום לפי ההכנסה, ואת הריבית הכוללת. עד ' + R0.termMax + ' שנה (סעיף 8).</span></div>'
      + '<div><h3 class="nlnc__mh">מה בנק ישראל קובע</h3><ul class="nlnc__rl" data-rules></ul></div>'
      + '<div><h3 class="nlnc__mh">מה השתנה ב־1.10.2026</h3><p class="nlnc__p" data-changed></p>'
      + '<h3 class="nlnc__mh" style="margin-top:14px!important">הלוואות לכל מטרה בנתוני בנק ישראל</h3><p class="nlnc__p" data-stats></p><div class="nlnc__bands" role="img" data-bands></div>'
      + '<span class="nli__help" style="margin-top:6px">החלק מהכסף של ההלוואות החדשות לכל מטרה לפי שיעור המימון, ' + esc(month(N.anyp.month)) + ', בנק ישראל.</span></div>'
      + '</div></div>'
      + '<p class="nli__eg"><b>דוגמה</b>הערכים בפתיחה הם דוגמה: דירה בשווי 2,800,000 ₪ עם יתרת משכנתא של 350,000 ₪, לכל מטרה. שנו אותם, והתוצאה מתעדכנת מיד. זה חישוב לפי כללי בנק ישראל, לא אישור ולא הצעה של בנק.</p>'
      + '</div>';
    root.innerHTML = h;
    var q = function (s) { return root.querySelector(s); }, qa = function (s) { return [].slice.call(root.querySelectorAll(s)); };

    /* the static parts below the result */
    var RU = N.rules;
    var ruleItems = [
      ['לכל מטרה: עד ' + pc(R0.any) + ' משווי הדירה. ', RU.any_ltv.text.replace(/^[^:]+: /, ''), 'any_ltv'],
      ['יחד עם המשכנתא הקיימת. ', RU.prior_loans.text, 'prior_loans'],
      ['בשיקול דעת הבנק: עד ' + pc(R0.upto) + '. ', RU.relief.text, 'relief'],
      ['החזר עד ' + pc(R0.pti) + ' מההכנסה הפנויה. ', RU.fixed_costs.text, 'pti_max'],
      ['פטור עד ' + nf(R0.exempt) + ' ₪. ', RU.pti_exempt.text, 'pti_exempt'],
      ['דירה נוספת. ', RU.pledged_for_purchase.text + ' לדירה הנרכשת: ' + pc(R0.single) + ' ליחידה, ' + pc(R0.replace) + ' לחלופית, ' + pc(R0.invest) + ' להשקעה.', 'pledged_for_purchase'],
      ['עזרה לילדים. ', RU.parents.text, 'parents'],
      ['מה לא נחשב לכל מטרה. ', RU.not_any_purpose.text, 'not_any_purpose']
    ];
    q('[data-rules]').innerHTML = ruleItems.map(function (x) { return '<li><b>' + wrapNums(esc(x[0])) + '</b>' + wrapNums(esc(x[1])) + ' <small>' + srcA(x[2]) + '</small></li>'; }).join('')
      + '<li>בהוראה 329 בגרסה ' + S.D329.version + ' מ־' + dmy(S.D329.date) + ' ובקובץ השאלות והתשובות מ־' + dmy(S.QA329.date) + ', כפי שהם באתר בנק ישראל ב־' + dmy(N.checked) + '.</li>';
    q('[data-changed]').innerHTML = esc('בהלוואה נוספת על דירה שכבר משועבדת, מבחן ההחזר כולל גם את ההחזרים של ההלוואות הקודמות על אותה דירה שנותרו להן יותר מ־18 חודשים, בכל בנק או גוף. ואם ההלוואה הנוספת באותו בנק, מגבלת שני השלישים בריבית משתנה נבדקת על כל האשראי בשעבוד הדירה.')
      + ' <small>' + srcA('same_asset') + ' · ' + srcA('variable_same_asset') + '</small>';
    q('[data-stats]').innerHTML = wrapNums(esc(dataLine(N, D))) + ' <small>' + '<a href="' + esc(S.SDMX.url) + '" target="_blank" rel="noopener">בנק ישראל, BIR_MRTG_99</a></small>';
    var BD = bands(N), bmax = Math.max.apply(null, BD.map(function (x) { return x.share; })) || 1;
    var bandsEl = q('[data-bands]');
    bandsEl.setAttribute('aria-label', 'ההלוואות לכל מטרה לפי שיעור המימון: ' + BD.map(function (x) { return x.label + ' ' + pc(x.share, 1); }).join(', '));
    bandsEl.innerHTML = BD.map(function (x) { return '<div class="nlnc__bd"><span>' + esc(x.label) + '</span><span><i' + (x.share === bmax ? ' class="is-hi"' : '') + ' style="width:' + (100 * x.share / bmax).toFixed(1) + '%"></i></span><span>' + (x.share > 0 && x.share < 0.0005 ? '&lt;0.1%' : pc(x.share, 1)) + '</span></div>'; }).join('');

    /* inputs */
    function show(k) { var inp = q('[data-k="' + k + '"]'); if (!inp) return; var x = v[k]; inp.value = k === 'rate' ? String(x == null ? '' : x) : (x === '' || x == null || !isFinite(money(x)) ? String(x == null ? '' : x) : nf(money(x))); }
    qa('input[data-k]').forEach(function (inp) {
      var k = inp.getAttribute('data-k'); show(k);
      inp.addEventListener('input', function () { v[k] = inp.value; touched(); later(); });
      if (k !== 'rate') inp.addEventListener('blur', function () { if (String(inp.value).trim() !== '' && isFinite(money(inp.value))) { v[k] = money(inp.value); show(k); } });
    });
    var last = null, t = 0;
    function later() { clearTimeout(t); t = setTimeout(paint, 90); }
    function touched() { if (ex) { ex = false; var e = q('[data-eg]'); if (e) e.hidden = true; } }
    root.addEventListener('click', function (e) {
      var b = e.target && e.target.closest ? e.target.closest('button') : null; if (!b || !root.contains(b)) return;
      if (b.hasAttribute('data-s')) {
        var k = b.getAttribute('data-s'), val = b.getAttribute('data-val');
        v[k] = k === 'years' ? +val : val; touched();
        if (k === 'src' && val === 'own' && String(v.rate == null ? '' : v.rate).trim() === '') { v.rate = String(ownStart(purpose(v.purpose), N)); show('rate'); }
        paint();
      }
    });
    function wrapNums(s) { return s.replace(/(−?[\d,]+(?:\.\d+)? ₪|[\d,]+(?:\.\d+)?%)/g, '<bdi>$1</bdi>'); }

    /* the share bar */
    var sh = q('[data-share]');
    function link() { return (location.origin && location.origin !== 'null' ? location.origin + location.pathname : location.href.split('#')[0]) + '#mneches=' + enc(v); }
    function pageLink() { return (location.origin && location.origin !== 'null' ? location.origin + location.pathname : location.href.split('#')[0]) + '#tool-neches'; }
    function copy(btn, txt, lab) { var sp = btn.querySelector('span'); var done = function () { sp.textContent = 'הועתק'; setTimeout(function () { sp.textContent = lab; }, 1600); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, function () { G.prompt('העתיקו', txt); }); else G.prompt('העתיקו', txt); }
    var b1 = document.createElement('button'); b1.type = 'button'; b1.className = 'is-primary'; b1.setAttribute('data-copy', ''); b1.innerHTML = ICON.copy + '<span>העתקת התוצאה</span>';
    b1.addEventListener('click', function () { if (last) copy(b1, copyText(last, N) + '\n' + pageLink(), 'העתקת התוצאה'); });
    var b2 = document.createElement('a'); b2.target = '_blank'; b2.rel = 'noopener'; b2.href = 'https://wa.me/'; b2.setAttribute('data-wa', ''); b2.innerHTML = ICON.wa + '<span>שליחה בוואטסאפ</span>';
    b2.addEventListener('click', function () { if (last) b2.href = 'https://wa.me/?text=' + encodeURIComponent(copyText(last, N) + '\n' + pageLink()); });
    var b3 = document.createElement('button'); b3.type = 'button'; b3.setAttribute('data-link', ''); b3.innerHTML = ICON.link + '<span>קישור למקרה הזה</span>';
    b3.addEventListener('click', function () { copy(b3, link(), 'קישור למקרה הזה'); });
    [b1, b2, b3].forEach(function (b) { sh.appendChild(b); });

    function deed(r) {
      var V = r.value, pct = function (x) { return Math.max(0, Math.min(100, 100 * x / V)); };
      var bal = Math.min(r.balance, V), nw = r.best, capV = r.cap, rel = r.P.relief ? r.reliefCap : null;
      var over = r.balance > capV, segs = over ? [['b', pct(capV)], ['o', pct(bal) - pct(capV)]] : [['b', pct(bal)], ['n', pct(nw)]], used = pct(bal + nw);
      var toCap = Math.max(0, pct(capV) - used); segs.push(['u', toCap]);
      var after = Math.max(used, pct(capV));
      if (rel != null && rel > capV) { var rx = Math.max(0, pct(rel) - after); segs.push(['x', rx]); }
      var html = '<div class="nlnc__bar">' + segs.filter(function (s) { return s[1] > 0.05; }).map(function (s) { return '<i class="' + s[0] + '" style="width:' + s[1].toFixed(2) + '%"></i>'; }).join('')
        + '<span class="nlnc__mk" style="inset-inline-start:' + pct(capV).toFixed(2) + '%"><span>' + pc(r.capR) + '</span></span>'
        + (rel != null && rel > capV ? '<span class="nlnc__mk is-x" style="inset-inline-start:' + pct(rel).toFixed(2) + '%"><span>' + pc(rel / V) + '</span></span>' : '') + '</div>';
      var lg = [['b', 'יתרת המשכנתא', r.balance > 0], ['o', 'היתרה שמעל התקרה', over], ['n', 'אפשר לקבל', nw > 0], ['u', 'עד התקרה, לא בשימוש', toCap > 0.05], ['x', 'בשיקול דעת הבנק', rel != null && rel > capV]];
      var sw = { b: 'background:#1F4B5C', n: 'background:#2F6F86', u: 'background:repeating-linear-gradient(135deg,#DCE7EC 0 3px,#fff 3px 6px)', x: 'background:#EEF2F4;border-style:dashed', o: 'background:#C42550' };
      html += '<ul class="nlnc__lg">' + lg.filter(function (x) { return x[2]; }).map(function (x) { return '<li><b style="' + sw[x[0]] + '"></b>' + esc(x[1]) + '</li>'; }).join('') + '</ul>';
      return { html: html, aria: 'שווי הדירה ' + ils(V) + ': יתרת משכנתא ' + pc(r.balPct, 1) + ', אפשר לקבל ' + pc(nw / V, 1) + ', התקרה ' + pc(r.capR) + (rel != null && rel > capV ? ', בשיקול דעת הבנק עד ' + pc(rel / V) : '') };
    }
    function table(r) {
      var head = ['תקופה', 'לפי ההכנסה', 'אפשר לקבל', 'החזר חודשי', 'סך ההחזרים'];
      var rows = r.table.map(function (x) {
        var cells = [x.years + ' שנה', x.incMax > 0 ? ils(x.incMax) : 'אין מקום', x.best > 0 ? ils(x.best) : 'אין מקום', x.best > 0 ? ils(x.pay) : 'אין', x.best > 0 ? ils(x.total) : 'אין'];
        var tag = x.best > 0 ? (x.binds === 'income' ? 'ההכנסה קובעת' : x.binds === 'exempt' ? 'הפטור עד ' + nf(r.R.exempt) + ' ₪' : 'כלל המימון קובע') : '';
        return '<tr' + (x.years === r.years ? ' class="is-on"' : '') + '>' + cells.map(function (c, i) { return '<td' + (i ? ' class="n' + (HEB.test(c) ? ' is-t' : '') + '" data-l="' + esc(head[i]) + '"' : '') + '><bdi dir="' + (HEB.test(c) ? 'rtl' : 'ltr') + '">' + esc(c) + '</bdi>' + (i === 0 && tag ? '<small>' + esc(tag) + '</small>' : '') + '</td>'; }).join('') + '</tr>';
      }).join('');
      return '<table class="nlnc__t"><thead><tr>' + head.map(function (x) { return '<th scope="col">' + esc(x) + '</th>'; }).join('') + '</tr></thead><tbody>' + rows + '</tbody></table>';
    }
    function paint() {
      var P = purpose(v.purpose), key = srcKey(v);
      qa('[data-s]').forEach(function (x) { var k = x.getAttribute('data-s'), cur = k === 'src' ? key : String(v[k]); x.setAttribute('aria-pressed', String(x.getAttribute('data-val') === cur)); });
      var bal = money0(v.balance);
      qa('[data-v]').forEach(function (x) { var w = x.getAttribute('data-v'); x.hidden = w === 'epay' ? !(bal > 0) : w === 'rate' ? key !== 'own' : false; });
      var rsH = key === 'own' ? null : rateSet(key, D, N, v.rate);
      q('[data-help="src"]').innerHTML = wrapNums(esc(rsH ? rateHelp(key, rsH, N, P) : rateHelp('own', null, N, P)));
      qa('[data-err]').forEach(function (x) { x.textContent = ''; });
      var r; try { r = compute(v, D, N); } catch (e2) { r = err(null, 'לא הצלחנו לחשב עם הערכים האלה.'); }
      var msg = q('[data-msg]'), ok = q('.nlnc__ok');
      if (r.error) {
        var fe = r.error.field && q('[data-err="' + r.error.field + '"]'); if (fe) fe.textContent = r.error.msg;
        msg.textContent = r.error.msg; msg.hidden = false; ok.hidden = true; last = null; q('[data-pn]').hidden = true; b1.disabled = true; return;
      }
      msg.hidden = true; ok.hidden = false; b1.disabled = false; last = r;
      var hd = headline(r), fig = q('.nlnc__fig');
      q('[data-lab]').textContent = hd.label; q('[data-eg]').hidden = !ex;
      fig.className = 'nlnc__fig' + (hd.text ? ' is-text' : ''); fig.innerHTML = '<bdi>' + esc(hd.value) + '</bdi>';
      q('.nlnc__sub').innerHTML = wrapNums(esc(sub(r)));
      var dd = deed(r), de = q('[data-deed]'); de.innerHTML = dd.html; de.setAttribute('aria-label', dd.aria); de.className = 'nlnc__deed' + (r.P.relief && r.reliefCap > r.cap ? ' has-x' : '');
      q('.nlnc__ls').innerHTML = lines(r).map(function (l) {
        var note = l.note ? '<span class="nlnc__ln' + (/^מרווח/.test(l.note) ? ' is-ok' : /^מעל/.test(l.note) ? ' is-warn' : '') + '">' + wrapNums(esc(l.note)) + '</span>' : '';
        return '<li class="is-' + l.kind + '"><span class="nlnc__lk">' + wrapNums(esc(l.label)) + (l.tag ? '<span class="nlnc__tag">' + esc(l.tag) + '</span>' : '') + '</span><span class="nlnc__lv' + (HEB.test(l.value) ? ' is-t' : '') + '"><bdi dir="' + (HEB.test(l.value) ? 'rtl' : 'ltr') + '">' + esc(l.value) + '</bdi></span>'
          + note + (l.src.length ? '<span class="nlnc__s">' + l.src.map(srcA).join('') + '</span>' : '') + '</li>';
      }).join('');
      var pn2 = q('[data-pn]'); pn2.hidden = false;
      pn2.innerHTML = wrapNums(esc(purposeNote(r))) + (P.k === 'buy' || P.k === 'kids' ? ' את הדירה ' + (P.k === 'kids' ? 'של הילד ' : 'החדשה ') + 'בדקו ב<a href="#mortgage-tool">מחשבון המשכנתא המלא</a>.' : '');
      q('[data-table]').innerHTML = table(r);
    }
    paint();
    if (fromLink) {  // a shared case: open the switcher pane it lives in, then bring it into view
      var pane = root.closest ? root.closest('.nlmx-pane') : null;
      if (pane && pane.hidden && pane.id) { var chip = document.querySelector('button[data-sw="' + pane.id + '"]'); if (chip) chip.click(); }
      if (root.scrollIntoView) root.scrollIntoView({ block: 'start' });
    }
  }
})();
