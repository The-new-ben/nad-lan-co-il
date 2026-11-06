/* NadLan Instruments · mcheck v1 "בדיקת משכנתא לפני חתימה" (HAD-675, Ben 6.11.2026; spec docs/research/2026-11-06-mortgage-delta/
   presign.md, sections 2 to 6). A custom surface on the instruments engine for /mortgage-calculator/. Built LOCALLY, not deployed.
   The reader copies the approval in principle line by line, in the uniform format of directive 451 (version 22, 7/23, addendum 6):
   - the header (bank, date, guarantors yes / no, price, buyer type, new or second hand, delivery month, the requested loan);
   - the four baskets (the bank's proposed basket "סל מוצע" and the uniform baskets 1, 2 and 3). Quick mode asks the totals row
     only (row 3 term, rows 7 to 11, like tools/moffers.js); one tap opens the tracks of every basket (rows 1 to 6 and 12);
   - the reader's own context, optional and kept in the page: net income, other loan payments, equity, years to a likely exit,
     eligibility checked yes / no / not checked, insurance quotes. No name, ID, phone or email field anywhere.
   Out: 28 checks of presign.md section 3, each one a flag (red / amber / info) with the reader's number, the rule, the source and
   its date, and the page of ours that owns the topic; a check without the data it needs is listed as "לא ניתן לבדוק", never
   guessed. A summary of plain sentences built only from typed numbers and dated official figures (never a recommendation), the
   questions to ask the bank, copy, WhatsApp, a case link (#mcheck=..., the hash only) and print. Nothing is sent to any server.
   Mode 2 ("המסמכים לפני החתימה", check 26): the final loan documents typed the same way, diffed against the proposed basket.
   Math is reused, not copied: NLMG (tools/mortgage.js: mix, scenario, prepayFee, stream, pv, bucket, ef2nom), NLMR
   (tools/mrates-common.js: exitScenario, replayPath, replay, parseMonth, mDiff and the page parts NLMR.ui), NLMO (tools/moffers.js:
   bankRef, place, trackCmp, clean, normalize, compare) and NLMQ.fullCost (tools/mquick.js). Two small pieces are new here: the
   overall rate (IRR) of a cash flow (NLMC.irrOf, a diagnostic for the tests: row 7 is never recomputed, because the banks use the
   451 forecasts and this tool has only the Research forecast), and the capitalization fee of a variable track whose rate
   changes every 2, 2.5, 7 or 10 years (NLMG.prepayFee knows only every 5 years; the same formula with that track's change day).
   Data: boi-mortgage.json (key "boim": by_bank, rules, fees, prepay, term, forecast, baskets, policy, cpi, insurance), and for the
   2022 replay boi-rate.json and cbs-120010.json (optional). Pure logic on window.NLMC (node: build-mcheck/test_mcheck.js).
   Hebrew only (RTL); no long dash in any string; never the words of a recommendation. */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;
  function LG() { return G.NLMG; }
  function LR() { return G.NLMR; }
  function LO() { return G.NLMO; }
  function LQ() { return G.NLMQ; }

  /* ======================================================================================================== constants */
  var BK = ['offer', 'b1', 'b2', 'b3'];
  var BNAME = { offer: 'הסל המוצע', b1: 'סל אחיד 1', b2: 'סל אחיד 2', b3: 'סל אחיד 3' };
  var BTAB = { offer: 'סל מוצע', b1: 'סל 1', b2: 'סל 2', b3: 'סל 3' };
  var BIN = { offer: 'בסל המוצע', b1: 'בסל אחיד 1', b2: 'בסל אחיד 2', b3: 'בסל אחיד 3' };  // "in" + the basket name
  var TRK = ['fixed_nl', 'fixed_cpi', 'prime', 'var_nl', 'var_cpi', 'zakaut'];
  var TNAME = { fixed_nl: 'קבועה לא צמודה', fixed_cpi: 'קבועה צמודה למדד', prime: 'פריים', var_nl: 'משתנה לא צמודה', var_cpi: 'משתנה צמודה למדד', zakaut: 'הלוואת זכאות' };
  /* the engine kind of each track (NLMG), its column in the Bank of Israel comparison by bank (TamInt010) and its average file */
  var TK = {
    fixed_nl: { kind: 'fixed', linked: false, bb: 'fixed_nl', file: 'nl' },
    fixed_cpi: { kind: 'fixed', linked: true, bb: 'fixed_cpi', file: 'cpi' },
    prime: { kind: 'prime', linked: false, bb: 'prime', file: 'nl', variable: true },
    var_nl: { kind: 'var', linked: false, bb: 'var_nl_other', file: 'nl', variable: true },
    var_cpi: { kind: 'var', linked: true, bb: 'var_cpi', file: 'cpi', variable: true },
    zakaut: { kind: 'fixed', linked: true, bb: null, file: 'cpi', directed: true }
  };
  var FREQ = [[12, 'כל שנה'], [24, 'כל שנתיים'], [30, 'כל שנתיים וחצי'], [60, 'כל 5 שנים'], [84, 'כל 7 שנים'], [120, 'כל 10 שנים']];
  var METHOD = [['spitzer', 'שפיצר'], ['equal', 'קרן שווה'], ['balloon', 'בלון'], ['bullet', 'בוליט']];
  var ANCHOR = [['', 'בחרו עוגן'], ['gov', 'אג״ח ממשלתיות'], ['makam', 'מק״מ'], ['other', 'עוגן אחר']];
  var BANKS = ['hapoalim', 'leumi', 'discount', 'mizrahi', 'fibi', 'mercantile', 'jerusalem'];
  var BANK_HE = { hapoalim: 'בנק הפועלים', leumi: 'בנק לאומי', discount: 'בנק דיסקונט', mizrahi: 'מזרחי טפחות', fibi: 'הבינלאומי', mercantile: 'מרכנתיל', jerusalem: 'בנק ירושלים', other: 'בנק אחר' };
  var BUYER = [['single', 'דירה יחידה'], ['replace', 'דירה חליפית'], ['invest', 'דירה להשקעה'], ['reduced', 'דירה במחיר מופחת']];
  var BKEY = { fixed_nl: 'fixed_nl', prime: 'prime', var5_cpi: 'var_cpi', var5_nl: 'var_nl', fixed_cpi: 'fixed_cpi' };
  var TERMS451 = [120, 180, 240, 300, 360];
  /* directive 451, version 22 (7/23), read 6.11.2026 (presign.md): the numbers of the rules this tool states */
  var R451 = { hold: 24, holdNoLien: 12, insDays: 14, noInsUpTo: 30000, insExtra: 20, insNotice: 30, appraisalDays: 90 };
  var SITE = 'https://nad-lan.co.il';
  var PG = {
    pre: { href: SITE + '/mortgage-calculator/mortgage-pre-approval/', label: 'אישור עקרוני למשכנתא' },
    ins: { href: SITE + '/mortgage-home-insurance/', label: 'ביטוח משכנתא' },
    refi: { href: SITE + '/mortgage-refinance/', label: 'מחזור משכנתא ועמלת פירעון מוקדם' },
    adv: { href: SITE + '/mortgage-advisor/', label: 'יועץ משכנתאות' },
    ltv: { href: SITE + '/mortgage-calculator/mortgage-ltv-ratio/', label: 'אחוז מימון' },
    cap: { href: SITE + '/mortgage-calculator/mortgage-repayment-capacity/', label: 'כמה משכנתא אפשר לקחת' },
    rates: { href: SITE + '/mortgage-calculator/mortgage-interest-rates/', label: 'ריבית משכנתא היום' },
    cpi: { href: SITE + '/cpi-calculator/', label: 'הצמדה למדד המחירים לצרכן' },
    cii: { href: SITE + '/new-projects/construction-input-index/', label: 'מדד תשומות הבנייה' }
  };
  var GROUP = { red: 'אדום: חורג מכלל או חסר באישור', amber: 'לבדיקה מול הבנק', info: 'לידיעה, וכללים שהאישור עומד בהם' };
  var GSHORT = { red: 'אדום', amber: 'לבדיקה', info: 'לידיעה' };

  /* ================================================================================================= small helpers */
  function fin(x) { return typeof x === 'number' && isFinite(x); }
  function num(v) { if (typeof v === 'number') return isFinite(v) ? v : null; var s = String(v == null ? '' : v).replace(/[^\d.\-]/g, ''); if (!s) return null; var n = parseFloat(s); return isFinite(n) ? n : null; }
  function grp(n) { var a = Math.round(Math.abs(n)); return String(a).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function ils(n) { return grp(n) + ' ₪'; }
  function pc(n, d) { d = d == null ? 2 : d; return (Math.round(n * Math.pow(10, d)) / Math.pow(10, d)).toFixed(d) + '%'; }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function isoOf(dt) { return dt.getUTCFullYear() + '-' + pad(dt.getUTCMonth() + 1) + '-' + pad(dt.getUTCDate()); }
  function utc(iso) { var p = String(iso).split('-'); return Date.UTC(+p[0], +p[1] - 1, +p[2]); }
  function addDays(iso, n) { return isoOf(new Date(utc(iso) + n * 864e5)); }
  function dayDiff(a, b) { return Math.round((utc(b) - utc(a)) / 864e5); }
  function todayISO(d) { d = d || new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function parseDate(s) {  // "2.11.2026", "2/11/2026", "2.11.26" or "2026-11-02" -> "2026-11-02"; anything else -> null
    s = String(s || '').trim(); var m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s), y, mo, d;
    if (m) { y = +m[1]; mo = +m[2]; d = +m[3]; } else { m = /^(\d{1,2})[.\/](\d{1,2})[.\/](\d{4}|\d{2})$/.exec(s); if (!m) return null; d = +m[1]; mo = +m[2]; y = +m[3]; if (y < 100) y += 2000; }
    if (mo < 1 || mo > 12 || d < 1 || y < 2000 || y > 2100) return null;
    var dt = new Date(Date.UTC(y, mo - 1, d)); return dt.getUTCMonth() === mo - 1 ? isoOf(dt) : null;
  }
  function dateHe(iso) { var p = String(iso).split('-'); return (+p[2]) + '.' + (+p[1]) + '.' + p[0]; }
  function monthHe(key) { var p = String(key).split('-'); return (+p[1]) + '.' + p[0]; }
  function yrs(m) { var y = Math.round(m / 12 * 10) / 10; return y + (y > 10 ? ' שנה' : ' שנים'); }
  function inMonth(m) { var y = Math.floor((m - 1) / 12) + 1; return 'בחודש ' + m + ' (שנה ' + y + ')'; }
  function sum(list, f) { return list.reduce(function (a, x) { return a + (f ? f(x) : x); }, 0); }
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function nameOf(list, v) { var x = list.filter(function (o) { return o[0] === v; })[0]; return x ? x[1] : ''; }
  function bankName(k) { return BANK_HE[k] || ''; }
  function plural(n, one, many) { return n === 1 ? one : n + ' ' + many; }

  /* ===================================================================================================== the sources */
  function src451(sec) { return { label: 'הוראה 451 של בנק ישראל, גרסה 22 (7.2023)' + (sec ? ', ' + sec : ''), url: 'https://boi.org.il/media/utld2tgp/451.pdf' }; }
  function src329(D, sec) { return { label: 'הוראה 329 של בנק ישראל, גרסה 13 (30.6.2026)' + (sec ? ', ' + sec : ''), url: 'https://boi.org.il/media/hjrlkrse/h2852.pdf' }; }
  function srcOrder(D, sec) { return { label: 'צו הבנקאות (פירעון מוקדם של הלוואה לדיור), התשס״ב־2002' + (sec ? ', ' + sec : ''), url: 'https://www.nevo.co.il/law_html/Law01/047_037.htm' }; }
  function srcEq(D) { var B = D.by_bank; return { label: 'בנק ישראל, קו המשווה: ריביות במשכנתאות לפי בנק, נתוני ' + monthHe(B.latest.month) + (B.src && B.src.file_date ? ' (פורסם ' + dateHe(B.src.file_date) + ')' : ''), url: B.src && (B.src.page || B.src.url) }; }
  function srcFc(D) { return { label: 'בנק ישראל, תחזית חטיבת המחקר (' + dateHe(D.forecast.published) + ')', url: 'https://www.boi.org.il/' }; }
  function srcTerm(D, file) { var T = D.term && D.term[file]; return T && T.src ? { label: T.src.label + ', בתוקף מ־' + dateHe(T.inforce), url: T.src.url } : null; }
  var SRC = {
    gov: { label: 'gov.il, המדריך לקבלת משכנתא ממשרד הבינוי והשיכון (עודכן 25.9.2024)', url: 'https://www.gov.il/he/pages/mortgage_guide' },
    kzFile: { label: 'כל זכות, פתיחת תיק משכנתא (עודכן 2.3.2025)', url: 'https://www.kolzchut.org.il/he/' + encodeURIComponent('פתיחת_תיק_משכנתא') },
    kzCredit: { label: 'כל זכות, קבלת מידע על נתוני אשראי (עודכן 27.8.2025)', url: 'https://www.kolzchut.org.il/he/' + encodeURIComponent('קבלת_מידע_על_נתוני_אשראי_ודירוג_האשראי_האישי') },
    credit: { label: 'בנק ישראל, מערכת נתוני האשראי', url: 'https://www.creditdata.org.il/' },
    cfpb: { label: 'CFPB (הרשות האמריקנית להגנה על צרכני שירותים פיננסיים), רשימת הבדיקה לפני החתימה', url: 'https://www.consumerfinance.gov/owning-a-home/closing-disclosure/' },
    life: { label: 'רשות שוק ההון, השוואת ביטוח חיים למשכנתה', url: 'https://life.cma.gov.il/' },
    dira: { label: 'רשות שוק ההון, השוואת ביטוח מבנה', url: 'https://dira.cma.gov.il/' },
    sale: { label: 'חוק המכר (דירות), סעיף 5ג', url: 'https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%9B%D7%A8_(%D7%93%D7%99%D7%A8%D7%95%D7%AA)' },
    calc: { label: 'חישוב מהמספרים שהקלדתם', url: null }
  };

  /* ===================================================================================================== the state */
  function blankBasket() { return { term: null, irr: null, first: null, max: null, maxM: null, total: null, fees: null, tracks: [] }; }
  function blankTrack(k, o) { var t = { k: k || 'fixed_nl', amount: null, months: null, method: 'spitzer', grace: null, graceType: 'partial', rate: null, anchor: '', margin: null, freq: 60, pp: '' }; if (o) Object.keys(o).forEach(function (x) { t[x] = o[x]; }); return t; }
  function blankOther() { return { bank: '', loan: null, b: { b1: blankBasket(), b2: blankBasket(), b3: blankBasket() } }; }
  function blank() {
    var b = {}; BK.forEach(function (k) { b[k] = blankBasket(); });
    return { v: 1, mode: 'ap', full: false, tab: 'offer',
      h: { bank: '', date: '', guar: '', price: null, buyer: 'single', newb: '', delivery: '', loan: null, lien: 'yes', resv: '' },
      b: b, c: { income: null, loans: null, equity: null, hz: null, elig: '', life: null, struct: null, arn: null },
      o: [], f: { date: '', loan: null, guar: '', fees: null, ins: '', tracks: [] } };
  }
  /* a case from the address (#mcheck=...): only known keys of the right type are taken */
  function merge(base, src) {
    if (!src || typeof src !== 'object') return base;
    Object.keys(base).forEach(function (k) {
      var b = base[k], s = src[k];
      if (s === undefined) return;
      if (Array.isArray(b)) {
        if (!Array.isArray(s)) return;
        if (k === 'tracks') base[k] = s.slice(0, 8).map(function (t) { var x = merge(blankTrack(), t); if (!TK[x.k]) x.k = 'fixed_nl'; return x; });
        else if (k === 'o') base[k] = s.slice(0, 2).map(function (t) { return merge(blankOther(), t); });
      } else if (b && typeof b === 'object') base[k] = merge(b, s);
      else if (b === null || typeof b === 'number') base[k] = typeof s === 'number' && isFinite(s) ? s : null;
      else if (typeof b === 'string') base[k] = typeof s === 'string' ? s.slice(0, 40) : b;
      else if (typeof b === 'boolean') base[k] = !!s;
    });
    return base;
  }
  function restore(h) { var st = merge(blank(), h); if (st.mode !== 'fin') st.mode = 'ap'; if (BK.indexOf(st.tab) < 0) st.tab = 'offer'; return st; }

  /* the uniform baskets of directive 451 (data: baskets.list) */
  function basketDef(D, key) {
    var L = (D && D.baskets && D.baskets.list) || [], b = L.filter(function (x) { return x.k === key; })[0];
    return b ? b.mix.map(function (x) { return { k: BKEY[x[0]] || x[0], share: x[1] }; }) : null;
  }
  function frac(s) { return Math.abs(s - 0.5) < 0.01 ? 'חצי' : Math.abs(s - 1 / 3) < 0.01 ? 'שליש' : Math.round(100 * s) + '%'; }
  function defText(D, key) {
    var d = basketDef(D, key); if (!d) return '';
    if (d.length === 1) return 'כל ההלוואה ב' + TNAME[d[0].k];
    return d.map(function (x) { return frac(x.share) + ' ' + TNAME[x.k] + (TK[x.k] && TK[x.k].kind === 'var' ? ' כל 5 שנים' : ''); }).join(', ');
  }
  function splitAmounts(loan, shares) { var out = [], used = 0; shares.forEach(function (s, i) { var a = i === shares.length - 1 ? loan - used : Math.round(loan * s / 1000) * 1000; used += a; out.push(a); }); return out; }
  /* the tracks of a uniform basket from its definition: the loan split by the shares, the term, a rate per track (or empty) */
  function fillDef(D, key, loan, months, rateOf) {
    var d = basketDef(D, key); if (!d) return [];
    var am = fin(loan) ? splitAmounts(loan, d.map(function (x) { return x.share; })) : d.map(function () { return null; });
    return d.map(function (x, i) {
      var r = rateOf ? rateOf(x.k) : null;
      return blankTrack(x.k, { amount: am[i], months: fin(months) ? months : null, rate: fin(r) ? r : null, freq: 60, anchor: TK[x.k].kind === 'var' ? 'gov' : '' });
    });
  }

  /* ====================================================================================================== the model */
  function tracksOk(list) { return (list || []).filter(function (t) { return fin(t.amount) && t.amount > 0; }); }
  function complete(t) { return fin(t.amount) && t.amount > 0 && fin(t.months) && t.months >= 1 && fin(t.rate) && t.rate >= 0 && t.rate < 30; }
  /* a track as an NLMG row. stress: a variable track that changes more often than every 5 years moves from month 1 (like prime) */
  function eng(t, stress) {
    var K = TK[t.k] || TK.fixed_nl, fq = fin(t.freq) ? t.freq : 60;
    var kind = K.kind === 'var' ? (stress && fq < 60 ? 'prime' : 'var5') : K.kind;
    return { k: t.k, amount: t.amount, rate: t.rate, years: t.months / 12, method: t.method || 'spitzer', grace: fin(t.grace) ? t.grace : 0,
      graceType: t.graceType === 'full' ? 'full' : 'partial', kind: kind, linked: K.linked, directed: !!K.directed, freq: fq };
  }
  function bmodel(st, key) {
    var b = st.b[key], tr = tracksOk(b.tracks), s = sum(tr, function (t) { return t.amount; });
    var months = tr.reduce(function (a, t) { return Math.max(a, fin(t.months) ? t.months : 0); }, 0);
    var any = ['term', 'irr', 'first', 'max', 'total', 'fees'].some(function (f) { return fin(b[f]); }) || tr.length > 0;
    return { key: key, b: b, tr: tr, sum: s, term: fin(b.term) ? b.term : (months || null), any: any, full: tr.length > 0 && tr.every(complete) };
  }
  /* the overall rate of a cash flow (effective annual %): the monthly rate at which the payments are worth the money received */
  function irrOf(pay, pv) {
    if (!(pv > 0) || !pay || !pay.length) return null;
    var lo = -0.01, hi = 0.05;
    for (var k = 0; k < 100; k++) { var r = (lo + hi) / 2, s = 0; for (var i = 0; i < pay.length; i++) s += pay[i] / Math.pow(1 + r, i + 1); if (s > pv) lo = r; else hi = r; }
    return 100 * (Math.pow(1 + (lo + hi) / 2, 12) - 1);
  }
  /* rows 8 to 10 recomputed from rows 2, 3, 5 (and 4, 6) on the Bank of Israel Research forecast (NLMR.exitScenario) */
  function recompute(bm, D) {
    if (!bm.full || !LG() || !LR()) return null;
    var rows = bm.tr.map(function (t) { return eng(t); }), X = LG().mix(rows, LR().exitScenario(D));
    return { first: X.first, max: X.highest, maxM: X.highestMonth, total: X.totalPaid, X: X, rows: rows };
  }
  function stressMix(bm, D) {  // +1% on every variable track (prime from month 1, a variable track at its change day), CPI at the forecast
    var rows = bm.tr.map(function (t) { return eng(t, true); });
    var X = LG().mix(rows, LG().scenario({ cpi: D.forecast.inflation_4q, prime: 'custom', shock: 1, shockMonth: 1 }));
    return { max: X.highest, maxM: X.highestMonth };
  }
  function replayMix(bm, XR) {  // the Bank of Israel rate and the CPI of 3.2022 to 5.2023, month by month (NLMR.replay)
    if (!XR || !XR.rt || !XR.cpi || !LR().replayPath) return null;
    try {
      var P = LR().replayPath(XR.rt, XR.cpi), r = LR().replay(bm.tr.map(function (t) { return eng(t, true); }), P);
      return { first: r.first, peak: r.peak, m: r.peakIdx + 1, from: P.months[1] || P.months[0], to: P.months[P.months.length - 1] };
    } catch (e) { return null; }
  }
  /* the capitalization fee of one track repaid in month h (the Banking Order). Fixed tracks and variable every 5 years: NLMG.prepayFee
     itself. A variable track that changes every 12 months or more often: none. Every 2, 2.5, 7 or 10 years: the same formula as
     NLMG.prepayFee (s.3: the lower of the two tests, cut after 3 and 5 years) with the months to that track's own change day. */
  function capFee(t, h, b, rate, endBefore, D, drop) {
    if (t.directed) return { cap: 0, why: 'directed' };
    if (t.kind === 'prime') return { cap: 0, why: 'prime' };
    if (t.kind === 'var5' && t.freq !== 60) {
      if (t.freq <= (D.fees.no_cap_fee_if_change_within_months || 12)) return { cap: 0, why: 'yearly' };
      var left = endBefore - h, next = t.freq * Math.ceil(h / t.freq) + 1, hh = Math.min(left, next - 1 - h);
      if (hh <= 0) return { cap: 0, why: 'reset' };
      var file = t.linked ? 'cpi' : 'nl', bk = LG().bucket(D.term[file].buckets, hh / 12), C = bk.nom, A = C - (drop || 0);
      var s = LG().stream(b, rate, left, hh, t.method), pvA = LG().pv(s, A), pvC = LG().pv(s, C);
      var f3 = A < rate ? Math.max(0, pvA - b) : 0, f4 = C < rate ? Math.max(0, pvA - pvC) : null, cap = f4 === null ? f3 : Math.min(f3, f4), cut = 0;
      (D.fees.reduce || []).forEach(function (x) { if (h / 12 >= x.after_years) cut = x.cut; });
      return { cap: cap * (1 - cut), why: '', cut: cut };
    }
    var f = LG().prepayFee(t, { month: h, amount: b, before: b, rate: rate, share: 1, endBefore: endBefore }, D, drop);
    return { cap: f.cap, why: f.why, cut: f.cut || 0 };
  }
  /* exit in month h on the forecast path: the balance and the fees of every track */
  function feeAt(bm, D, h) {
    var rows = bm.tr.map(function (t) { return eng(t); }), X = LG().mix(rows, LR().exitScenario(D));
    var drop = Math.round((D.policy.rate - D.forecast.rate_q3_2027) * 100) / 100;
    h = Math.round(h); if (h >= X.N) return { end: true, h: h };
    var o = { end: false, h: h, cap: 0, op: D.fees.operational_max, notice: 0, cpi: 0, bal: X.bal[h - 1], by: [], drop: drop };
    rows.forEach(function (t, i) {
      var S = X.T[i], b = S.bal[h - 1]; if (!(b > 0.5)) return;
      var f = capFee(t, h, b, S.rate[h - 1], S.end, D, drop);
      o.cap += f.cap; if (!t.directed) o.notice += b * D.fees.notice_rate;
      if (t.linked && !t.directed && D.cpi && D.cpi.avg_m12 != null) o.cpi += b * D.cpi.avg_m12 / 100 / 2;
      o.by.push({ k: t.k, cap: f.cap, why: f.why, bal: b });
    });
    return o;
  }
  function bankRefOf(D, key) { var O = LO(); if (!O || !O.bankRef) return null; return O.bankRef(D, key && key !== 'other' && BANKS.indexOf(key) > -1 ? key : 'system'); }

  /* ================================================================================================= the typed numbers */
  function validate(st) {
    var e = {}, h = st.h, L = fin(h.loan) ? h.loan : null;
    if (h.date && !parseDate(h.date)) e['h.date'] = 'תאריך כמו באישור, למשל 2.11.2026.';
    if (fin(h.loan) && !(h.loan >= 10000)) e['h.loan'] = 'סכום של 10,000 ₪ לפחות.';
    if (fin(h.price) && L && h.price < L) e['h.price'] = 'נמוך מסכום ההלוואה. בדקו את המספר.';
    if (h.delivery && LR() && !LR().parseMonth(h.delivery)) e['h.delivery'] = 'חודש ושנה, למשל 6.2028.';
    function tracks(list, p) {
      list.forEach(function (t, i) {
        var q = p + i + '.';
        if (fin(t.rate) && !(t.rate >= 0 && t.rate < 20)) e[q + 'rate'] = 'ריבית בין 0% ל־20%.';
        if (fin(t.months) && !(t.months >= 12 && t.months <= 480)) e[q + 'months'] = 'בחודשים, בין 12 ל־480.';
        if (fin(t.grace) && fin(t.months) && t.grace >= t.months) e[q + 'grace'] = 'קצר מתקופת המסלול.';
        if (fin(t.margin) && Math.abs(t.margin) > 10) e[q + 'margin'] = 'מרווח בין מינוס 10% ל־10%.';
      });
    }
    BK.forEach(function (k) {
      var b = st.b[k], p = 'b.' + k + '.';
      if (fin(b.term) && !(b.term >= 12 && b.term <= 480)) e[p + 'term'] = 'בחודשים, למשל 300 ל־25 שנה.';
      if (fin(b.irr) && !(b.irr > 0 && b.irr < 20)) e[p + 'irr'] = 'ריבית בין 0% ל־20%.';
      if (fin(b.first) && !(b.first > 0)) e[p + 'first'] = 'סכום חיובי.';
      if (fin(b.max) && fin(b.first) && b.max < b.first - 0.5) e[p + 'max'] = 'נמוך מההחזר הראשון. בדקו את המספר.';
      if (fin(b.maxM) && !(b.maxM >= 1 && b.maxM <= (fin(b.term) ? b.term : 480))) e[p + 'maxM'] = 'מספר החודש, בין 1 ל־' + (fin(b.term) ? b.term : 480) + '.';
      if (fin(b.total) && L && b.total < L) e[p + 'total'] = 'נמוך מסכום ההלוואה. בדקו את המספר.';
      tracks(b.tracks, p + 't.');
    });
    if (st.f.date && !parseDate(st.f.date)) e['f.date'] = 'תאריך כמו במסמכים, למשל 20.11.2026.';
    tracks(st.f.tracks, 'f.t.');
    return e;
  }
  /* a copy of the state with every value that failed validation taken out, so no check runs on a number that cannot be right */
  function scrub(st, e) {
    var s = clone(st);
    Object.keys(e).forEach(function (path) {
      var p = path.split('.'), o = s;
      for (var i = 0; i < p.length - 1; i++) { var k = p[i] === 't' ? 'tracks' : p[i]; o = o[/^\d+$/.test(k) ? +k : k]; if (!o) return; }
      var last = p[p.length - 1]; o[last] = typeof o[last] === 'string' ? '' : null;
    });
    return s;
  }

  /* ======================================================================================================== the checks */
  function add(res, level, id, title, you, rule, src, page, q) {
    res.flags.push({ id: id, level: level, title: title, you: you || '', rule: rule || '', src: (src || []).filter(Boolean), page: page || null, q: (q || []).filter(Boolean) });
  }
  function na(res, id, title, why) { res.na.push({ id: id, title: title, why: why }); }

  function c1(st, D, res, today) {
    var T = 'תוקף האישור', iso = parseDate(st.h.date);
    if (!iso) return na(res, 1, T, 'לא הוקלד תאריך האישור.');
    if (iso > today) return na(res, 1, T, 'תאריך האישור אחרי היום.');
    var days = st.h.lien === 'no' ? R451.holdNoLien : R451.hold, exp = addDays(iso, days), left = dayDiff(today, exp);
    res.valid = { from: iso, exp: exp, left: left, days: days };
    var rule = 'לפי הוראה 451 הבנק שומר את התנאים ' + days + ' ימים לפחות מתאריך האישור' + (days === R451.holdNoLien ? ', כשלא נדרש שעבוד חדש' : '') + ', והמועד מצוין באישור באופן בולט. אם המסמכים מגיעים אחרי המועד, הבנק מודיע שתקופת השמירה עברה ונותן אישור עקרוני מעודכן.';
    var src = [src451('סעיף 4ג(א)(4), (ו), (ז)')], q = ['עד איזה תאריך שמורים התנאים באישור, ומה קורה לריבית אם החתימה אחרי המועד?'];
    if (left < 0) add(res, 'red', 1, 'תוקף האישור עבר', 'האישור מ־' + dateHe(iso) + '; ' + days + ' הימים הסתיימו ב־' + dateHe(exp) + ', לפני ' + plural(-left, 'יום אחד', 'ימים') + '.', rule, src, PG.pre, q.concat(['האם תוציאו אישור עקרוני מעודכן, ובאילו תנאים?']));
    else if (left < 5) add(res, 'amber', 1, left === 0 ? 'היום האחרון לתוקף האישור' : 'נשארו ' + plural(left, 'יום אחד', 'ימים') + ' לתוקף האישור', 'האישור מ־' + dateHe(iso) + '; התנאים שמורים עד ' + dateHe(exp) + '.', rule, src, PG.pre, q);
    else add(res, 'info', 1, 'תוקף האישור', 'נשארו ' + left + ' ימים, עד ' + dateHe(exp) + ' (האישור מ־' + dateHe(iso) + ').', rule, src, PG.pre, q);
  }

  function c2(st, D, res, M) {
    var miss = BK.filter(function (k) { return !M[k].any; });
    var rule = 'אישור עקרוני כולל את הסל שהבנק מציע ואת שלושת הסלים האחידים. הוראה 451 פוטרת רק מקרים מוגדרים: הלוואה לכל מטרה לפחות מ־10 שנים, הלוואה לדיור בלי שעבוד לפחות מ־10 שנים, והלוואה לפי הסכם עם הממשלה.';
    var src = [src451('סעיף 4ג(א)(2), (3) ותוספת 5')];
    if (miss.length) add(res, 'red', 2, 'חסר סל', 'לא הוקלדו: ' + miss.map(function (k) { return BNAME[k]; }).join(', ') + '. אם הם חסרים גם באישור עצמו, האישור לא מלא.', rule, src, PG.pre, ['למה האישור לא כולל את ' + miss.map(function (k) { return BNAME[k]; }).join(', ') + '? אפשר לקבל אישור מלא?']);
    else add(res, 'info', 2, 'ארבעת הסלים באישור', 'הוקלדו הסל המוצע ושלושת הסלים האחידים.', rule, src, PG.pre);
  }

  function shareMap(bm) { var o = {}; bm.tr.forEach(function (t) { o[t.k] = (o[t.k] || 0) + t.amount / bm.sum; }); return o; }
  function c3(st, D, res, M) {
    var bad = [], ok = [], q = [];
    ['b1', 'b2', 'b3'].forEach(function (k) {
      var m = M[k]; if (!m.any) return;
      var why = [];
      if (fin(m.term) && TERMS451.indexOf(Math.round(m.term)) < 0) why.push('תקופה של ' + Math.round(m.term) + ' חודשים');
      if (m.tr.length) {
        var def = basketDef(D, k) || [], sh = shareMap(m), keys = Object.keys(sh);
        var same = keys.length === def.length && def.every(function (x) { return sh[x.k] != null && Math.abs(sh[x.k] - x.share) <= 0.01; });
        if (!same) why.push('התמהיל: ' + keys.map(function (x) { return TNAME[x] + ' ' + pc(100 * sh[x], 1); }).join(', '));
        m.tr.forEach(function (t) { if (TK[t.k].kind === 'var' && fin(t.freq) && t.freq !== 60) why.push(TNAME[t.k] + ' שמשתנה ' + nameOf(FREQ, t.freq)); });
      }
      if (why.length) { bad.push(BNAME[k] + ': ' + why.join('; ')); q.push('למה ' + BNAME[k] + ' שונה מההגדרה של בנק ישראל?'); } else ok.push(k);
    });
    if (!bad.length && !ok.length) return na(res, 3, 'הסלים האחידים לפי ההגדרה', 'לא הוקלד אף סל אחיד.');
    var rule = 'בסלים האחידים התקופה לבחירה היא 10, 15, 20, 25 או 30 שנה, בלוח שפיצר. סל 1: ' + defText(D, 'b1') + '. סל 2: ' + defText(D, 'b2') + ', על בסיס אג״ח ממשלתיות. סל 3: ' + defText(D, 'b3') + '.';
    var src = [src451('סעיף 4ג(ב)(2), (3) ותוספת 5')];
    if (bad.length) add(res, 'amber', 3, 'סל אחיד שונה מההגדרה', bad.join('. ') + '.', rule, src, PG.pre, q);
    else add(res, 'info', 3, 'הסלים האחידים לפי ההגדרה', ok.map(function (k) { return BNAME[k]; }).join(', ') + ': התקופה' + (ok.some(function (k) { return M[k].tr.length; }) ? ' והתמהיל' : '') + ' לפי ההגדרה.' + (ok.some(function (k) { return !M[k].tr.length; }) ? ' את התמהיל אפשר לבדוק כשמקלידים את המסלולים.' : ''), rule, src, PG.pre);
  }

  function c4(st, D, res, M) {
    var L = st.h.loan, bad = [], okk = [], badK = [];
    BK.forEach(function (k) {
      var m = M[k]; if (!m.tr.length || !fin(L)) return;
      if (Math.abs(m.sum - L) > Math.max(1000, 0.001 * L)) { bad.push(BNAME[k] + ': ' + ils(m.sum) + ' במסלולים מול ' + ils(L)); badK.push(k); } else okk.push(BNAME[k]);
    });
    if (bad.length) {  // baskets with the same sum are said once
      var by = {}; badK.forEach(function (k) { var x = Math.round(M[k].sum); (by[x] = by[x] || []).push(k); });
      bad = Object.keys(by).map(function (x) { var ks = by[x]; return (ks.length === 4 ? 'בכל ארבעת הסלים' : ks.map(function (k) { return BNAME[k]; }).join(', ')) + ': ' + ils(+x) + ' במסלולים מול ' + ils(L) + ' בראש האישור'; });
    }
    if (bad.length) add(res, 'red', 4, 'סכום המסלולים לא שווה לסך ההלוואה', bad.join('; ') + '.', 'סכומי המסלולים בכל סל מסתכמים בסך ההלוואה המבוקשת שבראש האישור. פער הוא טעות הקלדה או סל על סכום אחר.', [SRC.calc], PG.pre, ['למה סכום המסלולים ' + BIN[badK[0]] + ' שונה מסך ההלוואה המבוקשת?']);
    else if (okk.length) add(res, 'info', 4, 'המסלולים מסתכמים בסך ההלוואה', okk.join(', ') + ': ' + ils(L) + '.', '', [SRC.calc], null);
    var E = st.c.equity, P = st.h.price;
    if (fin(E) && fin(P) && fin(L)) {
      var gap = L + E - P;
      if (gap < -0.5) add(res, 'red', 4, 'ההלוואה וההון העצמי לא מכסים את המחיר', 'הלוואה של ' + ils(L) + ' והון עצמי של ' + ils(E) + ' הם ' + ils(L + E) + ', פחות ב־' + ils(-gap) + ' ממחיר הדירה, ' + ils(P) + '.', 'ההלוואה וההון העצמי צריכים לכסות את מחיר הדירה, ומעבר לו את מס הרכישה ואת עורך הדין, שמשולמים מההון העצמי.', [SRC.calc], PG.cap, ['מאיפה יגיע ההפרש של ' + ils(-gap) + '?']);
      else add(res, 'info', 4, 'ההון העצמי מעבר למחיר', 'הלוואה של ' + ils(L) + ' והון עצמי של ' + ils(E) + ': ' + (gap < 0.5 ? 'בדיוק מחיר הדירה, בלי יתרה למס רכישה ולעורך דין.' : 'נשארים ' + ils(gap) + ' מעבר למחיר, למס רכישה, לעורך דין ולעלויות אחרות.'), '', [SRC.calc], PG.cap);
    } else if (!bad.length && !okk.length) na(res, 4, 'הסכומים מסתכמים', 'צריך את סך ההלוואה ואת המסלולים, או את המחיר ואת ההון העצמי.');
  }

  function c5(st, D, res) {
    var L = st.h.loan, P = st.h.price, T = 'שיעור המימון';
    if (!fin(L) || !fin(P) || !(P > 0)) return na(res, 5, T, 'חסרים סך ההלוואה או מחיר הדירה.');
    var R = D.rules, cap = R.ltv[st.h.buyer] != null ? R.ltv[st.h.buyer] : R.ltv.single, r = L / P, bt = nameOf(BUYER, st.h.buyer) || 'דירה יחידה';
    var rule = 'לפי הוראה 329 המשכנתא עד ' + pc(100 * R.ltv.single, 0) + ' משווי דירה יחידה, ' + pc(100 * R.ltv.replace, 0) + ' בדירה חליפית ו־' + pc(100 * R.ltv.invest, 0) + ' בדירה להשקעה. חישבנו לפי המחיר שהקלדתם.';
    var src = [src329(D, R.notes && R.notes.ltv)];
    if (r > cap + 1e-6) add(res, 'red', 5, 'שיעור המימון מעל המגבלה', 'הלוואה של ' + ils(L) + ' על מחיר של ' + ils(P) + ': ' + pc(100 * r, 1) + ', מעל ' + pc(100 * cap, 0) + ' ב' + bt + '.', rule, src, PG.ltv,
      ['על איזה שווי חושב שיעור המימון: המחיר או הערכת השמאי?', 'מה הסכום המרבי לפי המגבלה, ' + ils(Math.floor(cap * P)) + ', ואיך משתנה ההחזר?']);
    else add(res, 'info', 5, T, pc(100 * r, 1) + ' מהמחיר, ' + (Math.abs(r - cap) < 0.0005 ? 'בדיוק במגבלה' : 'מתחת למגבלה') + ' של ' + pc(100 * cap, 0) + ' ב' + bt + '.', rule, src, PG.ltv);
    if (st.h.buyer === 'reduced' && R.reduced) {
      var E = st.c.equity, X = R.reduced, rr = [src329(D, R.notes && R.notes.reduced)];
      if (fin(E) && E < X.own_min_grant) add(res, 'red', 5, 'הון עצמי נמוך מהמינימום בדירה במחיר מופחת', 'הון עצמי של ' + ils(E) + '.', X.text, rr, PG.ltv, ['כמה הון עצמי נדרש בדירה הזאת, ומאיזה מקור?']);
      else if (fin(E) && E < X.own_min) add(res, 'amber', 5, 'הון עצמי בדירה במחיר מופחת', 'הון עצמי של ' + ils(E) + ', בין ' + ils(X.own_min_grant) + ' ל־' + ils(X.own_min) + '.', X.text, rr, PG.ltv, ['האם ניתן על הדירה מענק, כך שהמינימום הוא ' + ils(X.own_min_grant) + '?']);
      else add(res, 'info', 5, 'דירה במחיר מופחת', fin(E) ? 'הון עצמי של ' + ils(E) + '.' : 'ההון העצמי לא הוקלד.', X.text, rr, PG.ltv);
    }
  }

  function payOf(M, RC, k) { var b = M[k].b; return fin(b.first) ? b.first : RC[k] ? RC[k].first : null; }
  function c6(st, D, res, M, RC) {
    var T = 'ההחזר מול ההכנסה', inc = st.c.income, lo = fin(st.c.loans) && st.c.loans > 0 ? st.c.loans : 0;
    if (!fin(inc) || !(inc > 0)) return na(res, 6, T, 'לא הוקלדה ההכנסה הפנויה של משק הבית.');
    var pay = payOf(M, RC, 'offer');
    if (!fin(pay)) return na(res, 6, T, 'לא הוקלד ההחזר הראשון בסל המוצע (שורה 8).');
    var R = D.rules, r = (pay + lo) / inc;
    var oth = ['b1', 'b2', 'b3'].map(function (k) { var p = payOf(M, RC, k); return fin(p) ? (p + lo) / inc : null; }).filter(fin);
    res.pti = r;
    var you = 'החזר ראשון של ' + ils(pay) + (fin(M.offer.b.first) ? '' : ' (לפי החישוב שלנו)') + (lo ? ' ועוד ' + ils(lo) + ' בהלוואות אחרות' : '') + ' מול הכנסה פנויה של ' + ils(inc) + ': ' + pc(100 * r, 1) + '.'
      + (oth.length ? ' בסלים האחידים: ' + (oth.length > 1 ? 'בין ' + pc(100 * Math.min.apply(null, oth), 1) + ' ל־' + pc(100 * Math.max.apply(null, oth), 1) : pc(100 * oth[0], 1)) + '.' : '');
    var rule = 'לפי הוראה 329: עד ' + pc(100 * R.pti_risk, 0) + ' מההכנסה הפנויה; בין ' + pc(100 * R.pti_risk, 0) + ' ל־' + pc(100 * R.pti_max, 0) + ' הבנק נדרש להחזיק יותר הון; מעל ' + pc(100 * R.pti_max, 0) + ' הבנק לא נותן את ההלוואה. חישבנו יחד עם ההחזרים על הלוואות אחרות שהקלדתם.';
    var src = [src329(D, R.notes && R.notes.pti)];
    if (r > R.pti_max + 1e-6) add(res, 'red', 6, 'ההחזר מעל ' + pc(100 * R.pti_max, 0) + ' מההכנסה', you, rule, src, PG.cap, ['איך חושבה ההכנסה הפנויה, ואיזו תקופה או איזה סכום מורידים את ההחזר מתחת ל־' + pc(100 * R.pti_max, 0) + '?']);
    else if (r > R.pti_risk + 1e-6) add(res, 'amber', 6, 'ההחזר בין ' + pc(100 * R.pti_risk, 0) + ' ל־' + pc(100 * R.pti_max, 0) + ' מההכנסה', you, rule, src, PG.cap, ['האם יחס ההחזר מעל ' + pc(100 * R.pti_risk, 0) + ' משפיע על הריבית שהוצעה?']);
    else add(res, 'info', 6, T, you, rule, src, PG.cap);
  }

  function c7(st, D, res, M) {
    var rows = BK.filter(function (k) { return M[k].tr.length; }).map(function (k) { var m = M[k]; return { k: k, s: sum(m.tr.filter(function (t) { return TK[t.k].variable; }), function (t) { return t.amount; }) / m.sum }; });
    if (!rows.length) return na(res, 7, 'החלק בריבית משתנה', 'צריך את המסלולים של הסל (כל השורות).');
    var lim = Math.max(D.rules.variable_max, 2 / 3), over = rows.filter(function (r) { return r.s > lim + 0.0005; });
    var txt = function (list) { return list.map(function (r) { return BNAME[r.k] + ' ' + pc(100 * r.s, 1); }).join(', '); };
    var rule = 'לפי הוראה 329 לפחות שליש מההלוואה בריבית קבועה, כלומר עד שני שלישים (' + pc(100 * lim, 2) + ') במסלולים שהריבית בהם יכולה להשתנות: פריים ומשתנה בכל תדירות.';
    var src = [src329(D, D.rules.notes && D.rules.notes.variable)];
    if (over.length) add(res, 'red', 7, 'יותר משני שלישים בריבית משתנה', txt(over) + '.', rule, src, PG.pre, ['למה ' + BNAME[over[0].k] + ' עובר את המגבלה של שני שלישים בריבית משתנה?']);
    else add(res, 'info', 7, 'החלק בריבית משתנה', txt(rows) + '.', rule, src, PG.pre);
  }

  function c8(st, D, res, M) {
    var max = D.rules.term_max * 12, over = [], longest = 0, any = false;
    BK.forEach(function (k) {
      var m = M[k];
      if (fin(m.b.term)) { any = true; longest = Math.max(longest, m.b.term); if (m.b.term > max) over.push(BNAME[k] + ': ' + m.b.term + ' חודשים'); }
      m.tr.forEach(function (t) { if (fin(t.months)) { any = true; longest = Math.max(longest, t.months); if (t.months > max) over.push(BNAME[k] + ', ' + TNAME[t.k] + ': ' + t.months + ' חודשים'); } });
    });
    if (!any) return na(res, 8, 'תקופת ההלוואה', 'לא הוקלדה תקופה (שורה 3).');
    var rule = 'לפי הוראה 329 כל מסלול עד ' + D.rules.term_max + ' שנה (' + max + ' חודשים).', src = [src329(D, D.rules.notes && D.rules.notes.term)];
    if (over.length) add(res, 'red', 8, 'תקופה מעל ' + D.rules.term_max + ' שנה', over.join('; ') + '.', rule, src, PG.pre, ['למה התקופה במסלול ארוכה מ־' + D.rules.term_max + ' שנה?']);
    else add(res, 'info', 8, 'תקופת ההלוואה', 'התקופה הארוכה באישור: ' + longest + ' חודשים, ' + yrs(longest) + '.', rule, src, PG.pre);
  }

  function gapTo(x, base, noun) { var g = Math.round((x - base) * 100) / 100; return g > 0 ? 'גבוהה ב־' + pc(g) + ' מ' + noun : g < 0 ? 'נמוכה ב־' + pc(-g) + ' מ' + noun : 'שווה ל' + noun.replace(/^ה/, ''); }
  function c9(st, D, res, M) {
    var T = 'הריבית הכוללת החזויה מול קו המשווה', typed = BK.filter(function (k) { return fin(M[k].b.irr); });
    if (!typed.length) return na(res, 9, T, 'לא הוקלדה הריבית הכוללת החזויה (שורה 7).');
    var ref = bankRefOf(D, st.h.bank), sys = bankRefOf(D, 'system');
    if (!ref || !sys) return na(res, 9, T, 'הנתונים של קו המשווה לא נטענו.');
    var own = ref.key !== 'system', main = fin(M.offer.b.irr) ? 'offer' : typed[0], x = M[main].b.irr;
    var you = 'באישור: ' + typed.map(function (k) { return BTAB[k] + ' ' + pc(M[k].b.irr); }).join(', ') + '. ' + BNAME[main] + ', ' + pc(x) + ', ' + (own ? gapTo(x, ref.irr, 'הממוצע של ' + ref.name) + ' ו' : '') + gapTo(x, sys.irr, 'הממוצע של כל הבנקים') + '.';
    var rule = (own ? 'הממוצע של ' + ref.name + ' במשכנתאות החדשות של ' + monthHe(ref.month) + ': ' + pc(ref.irr) + '; ' : 'הבנק לא בקו המשווה, לכן ההשוואה לממוצע של כל הבנקים. ') + 'כל הבנקים: ' + pc(sys.irr) + '; בחמשת הבנקים הגדולים בין ' + pc(sys.min.irr) + ' (' + sys.min.name + ') ל־' + pc(sys.max.irr) + ' (' + sys.max.name + '). ממוצע של בנק תלוי בתמהיל ובלקוחות שלו, ואינו הצעה; הבנקים מדווחים אותו לבנק ישראל.';
    var q = own && x > ref.irr + 0.005 ? ['הריבית הכוללת החזויה ' + BIN[main] + ', ' + pc(x) + ', גבוהה מהממוצע שלכם בקו המשווה של בנק ישראל, ' + pc(ref.irr) + '. אפשר לקבל הצעה מעודכנת?'] : ['לפי איזו תחזית חושבה הריבית הכוללת החזויה, ומה נכלל בה?'];
    add(res, 'info', 9, T, you, rule, [srcEq(D)], PG.rates, q);
  }

  function c10(st, D, res, M) {
    var T = 'הריבית בכל מסלול מול הממוצע', m = M.offer;
    if (!m.tr.length) return na(res, 10, T, 'צריך את המסלולים של הסל המוצע (כל השורות).');
    var ref = bankRefOf(D, st.h.bank), O = LO(); if (!ref || !O || !O.trackCmp) return na(res, 10, T, 'הנתונים של קו המשווה לא נטענו.');
    var own = ref.key !== 'system', hi = [], lo = [], q = [], tbl = [];
    m.tr.forEach(function (t) {
      var K = TK[t.k]; if (!K.bb || !fin(t.rate) || !fin(t.months)) return;
      var c = O.trackCmp({ track: K.bb, share: 100 * t.amount / m.sum, rate: t.rate, years: t.months / 12 }, ref, m.sum); if (!c) return;
      var tb = K.kind === 'fixed' && D.term && D.term[K.file] ? LG().bucket(D.term[K.file].buckets, t.months / 12) : null;
      var line = TNAME[t.k] + ' ' + pc(t.rate) + (t.k === 'prime' ? ' (פריים ' + (t.rate - D.policy.prime < 0 ? 'פחות ' : 'ועוד ') + pc(Math.abs(t.rate - D.policy.prime)) + ')' : '') + ': ממוצע ' + (own ? ref.name : 'כל הבנקים') + ' ' + pc(c.nom)
        + (own && fin(c.sysNom) ? ', כל הבנקים ' + pc(c.sysNom) : '') + (tb ? ', ממוצע לפי תקופה (' + tb.label + ') ' + pc(tb.nom) : '')
        + (fin(c.payGap) && Math.abs(c.payGap) >= 1 ? '; ' + (c.payGap > 0 ? 'יותר' : 'פחות') + ' ' + ils(Math.abs(c.payGap)) + ' בחודש, ' + ils(Math.abs(c.totalGap)) + ' לאורך המסלול' : '');
      tbl.push({ t: t, c: c, tb: tb });
      if (c.gap >= 0.1 && (!fin(c.sysNom) || t.rate - c.sysNom >= 0.1)) { hi.push(line); q.push('במסלול ' + TNAME[t.k] + ' הריבית ' + pc(t.rate) + ', והממוצע ' + (own ? 'שלכם' : 'של כל הבנקים') + ' ב־' + monthHe(ref.month) + ' היה ' + pc(c.nom) + '. אפשר להתאים?'); }
      else lo.push(line);
    });
    res.t10 = { rows: tbl, own: own, ref: ref };
    if (!tbl.length) return na(res, 10, T, 'חסרים ריבית או תקופה במסלולים.');
    var rule = 'הממוצעים של בנק ישראל למשכנתאות החדשות ב־' + monthHe(ref.month) + ', ריבית אפקטיבית שהומרה לריבית שנתית לתשלום חודשי; הממוצע לפי תקופה מקבצי הריבית הממוצעת לפי תקופה לפירעון, בתוקף מ־' + dateHe(D.term.nl.inforce) + '. הפער בשקלים: לוח שפיצר על סכום המסלול לאותה תקופה. הלוואת זכאות לא נבדקת כאן.';
    var src = [srcEq(D), srcTerm(D, 'nl'), srcTerm(D, 'cpi')];
    if (hi.length) add(res, 'amber', 10, 'ריבית מעל הממוצע במסלול', hi.join('. ') + '.', rule, src, PG.rates, q);
    if (lo.length) add(res, 'info', 10, hi.length ? 'שאר המסלולים מול הממוצע' : T, lo.join('. ') + '.', rule, src, PG.rates);
  }

  function c11(st, D, res, M) {
    var T = 'השוואה לבנקים אחרים', O = LO(), others = (st.o || []).filter(function (o) { return ['b1', 'b2', 'b3'].some(function (k) { var b = o.b[k]; return fin(b.irr) || fin(b.total) || fin(b.max) || fin(b.first); }); });
    if (!others.length) return na(res, 11, T, 'לא הוקלד אישור מבנק נוסף.');
    if (!O || !O.compare) return na(res, 11, T, 'כלי ההשוואה לא נטען.');
    var term = function (o, L) { var t = null; ['b1', 'b2', 'b3'].forEach(function (k) { if (t == null && fin(o.b[k].term)) t = o.b[k].term; }); return t; };
    var mine = { bank: st.h.bank, loan: st.h.loan, b: { b1: M.b1.b, b2: M.b2.b, b3: M.b3.b } };
    var list = [mine].concat(others).map(function (o) {
      var t = term(o); var b = {}; ['b1', 'b2', 'b3'].forEach(function (k) { var x = o.b[k]; b[k] = { irr: x.irr, total: x.total, maxPay: x.max, first: x.first }; });
      return { bank: o.bank, loan: o.loan, years: fin(t) ? t / 12 : (fin(M.b1.term) ? M.b1.term / 12 : null), b: b, mix: [] };
    });
    var cl = O.clean(list), nm = O.normalize(cl.offers), cmp = O.compare(nm), N = O.names(list); N[0] = 'האישור הזה';
    var lines = [], q = [], any = false;
    ['b1', 'b2', 'b3'].forEach(function (k) {
      var c = cmp[k]; if (c.have.length < 2 || c.have.indexOf(0) < 0) return; any = true;
      if (c.cheapest.indexOf(0) > -1) { lines.push(BNAME[k] + ': האישור הזה הזול מבין ' + c.have.length); return; }
      var ci = c.cheapest[0], v = c.vs[0];
      lines.push(BNAME[k] + ': ' + N[ci] + ' זול יותר, ' + (c.by === 'total' ? ils(v.dTotal) + ' פחות לאורך ההלוואה' + (fin(v.dMax) && Math.abs(v.dMax) >= 1 ? ' ו־' + ils(Math.abs(v.dMax)) + ' ' + (v.dMax > 0 ? 'פחות' : 'יותר') + ' בהחזר הגבוה' : '') : pc(v.dIrr) + ' פחות בריבית הכוללת החזויה'));
      q.push(BIN[k] + ' ההצעה של ' + N[ci] + ' זולה ב־' + (c.by === 'total' ? ils(v.dTotal) + ' לאורך ההלוואה' : pc(v.dIrr) + ' בריבית הכוללת החזויה') + '. אפשר להשוות אליה?');
    });
    if (!any) return na(res, 11, T, 'אין סל שהוקלד גם כאן וגם באישור האחר.');
    add(res, 'info', 11, T, lines.join('. ') + '.', 'אותו סל, אותו סכום ואותה תקופה: הזול לפי סך התשלומים הצפוי. סכומים שונים הותאמו לסכום של האישור הזה; תקופות שונות הושוו לפי הריבית הכוללת החזויה. מדף ההסבר של הוראה 451: הסלים האחידים נועדו לשפר את היכולת להשוות עלויות.', [src451('תוספת 6, דף ההסבר')], PG.pre, q);
  }

  function c12(st, D, res, M, RC) {
    var T = 'חישוב חוזר של שורות 8 עד 10', lines = [], worst = 0, any = false;
    BK.forEach(function (k) {
      var rc = RC[k], b = M[k].b; if (!rc) return; any = true;
      var g = function (typed, ours) { if (!fin(typed)) return ''; var d = (typed - ours) / ours; return ' (באישור ' + ils(typed) + (Math.abs(d) < 0.005 ? ', זהה' : ', ' + (d > 0 ? 'יותר' : 'פחות') + ' ב־' + pc(100 * Math.abs(d), 1)) + ')'; };
      if (fin(b.first)) worst = Math.max(worst, Math.abs(b.first - rc.first) / rc.first);
      lines.push(BTAB[k] + ': החזר ראשון ' + ils(rc.first) + g(b.first, rc.first) + '; הגבוה ' + ils(rc.max) + ' ' + inMonth(rc.maxM) + g(b.max, rc.max) + '; סך התשלומים ' + ils(rc.total) + g(b.total, rc.total));
    });
    if (!any) return na(res, 12, T, 'צריך בכל מסלול סכום, תקופה וריבית (כל השורות).');
    var FC = D.forecast;
    var rule = 'חישבנו את השורות מהסכום, מהתקופה ומהריבית של כל מסלול, לפי תחזית חטיבת המחקר של בנק ישראל מ־' + dateHe(FC.published) + ' (ריבית בנק ישראל ' + pc(FC.rate_q3_2027, 1) + ' ברבע השלישי של 2027, אינפלציה ' + pc(FC.inflation_4q, 1) + ' בשנה). הבנקים מחשבים לפי התחזיות של הוראה 451, שנגזרות ממחירי אגרות החוב הממשלתיות ומתעדכנות פעם בשבועיים, ולכן פער בהחזר הגבוה ובסך התשלומים צפוי. פער בהחזר הראשון יכול להיות טעות הקלדה או עלות שנכללה בסכום של הבנק.';
    var src = [srcFc(D), src451('תוספת 6, דף ההסבר')];
    if (worst > 0.03) add(res, 'amber', 12, 'ההחזר הראשון באישור שונה מהחישוב', lines.join('. ') + '.', rule, src, PG.pre, ['מה כלול בהחזר החודשי הראשון (שורה 8) מעבר לקרן ולריבית?']);
    else add(res, 'info', 12, T, lines.join('. ') + '.', rule, src, PG.pre);
  }

  function c13(st, D, res, M, RC, XR) {
    var T = 'ההחזר הגבוה הצפוי', b = M.offer.b, rc = RC.offer, inc = st.c.income, lo = fin(st.c.loans) && st.c.loans > 0 ? st.c.loans : 0, max = D.rules.pti_max;
    var hi = fin(b.max) ? b.max : rc ? rc.max : null, hm = fin(b.max) ? b.maxM : rc ? rc.maxM : null;
    var S = M.offer.full ? stressMix(M.offer, D) : null, RP = M.offer.full ? replayMix(M.offer, XR) : null;
    if (!fin(hi) && !S) return na(res, 13, T, 'לא הוקלד ההחזר הגבוה בסל המוצע (שורה 9), ואין מסלולים לחישוב.');
    var p = function (v) { return fin(inc) && inc > 0 ? ' (' + pc(100 * (v + lo) / inc, 1) + ' מההכנסה' + (lo ? ', עם ההלוואות האחרות' : '') + ')' : ''; }, over = false;
    var chk = function (v) { if (fin(inc) && inc > 0 && (v + lo) / inc > max + 1e-6) over = true; };
    var parts = [];
    if (fin(hi)) { chk(hi); parts.push('בסל המוצע ' + ils(hi) + (fin(hm) ? ' ' + inMonth(hm) : '') + p(hi) + (fin(b.max) ? '' : ', לפי החישוב שלנו')); }
    if (S) { chk(S.max); parts.push('אם הריבית בכל מסלול משתנה עולה ב־1%: עד ' + ils(S.max) + ' ' + inMonth(S.maxM) + p(S.max)); }
    if (RP) { chk(RP.peak); parts.push('אם הריבית והמדד של ' + monthHe(RP.from) + ' עד ' + monthHe(RP.to) + ' חוזרים: ' + ils(RP.peak) + ' בחודש ה־' + RP.m + p(RP.peak)); }
    var rule = 'הוראה 451 מחייבת להציג את ההחזר הגבוה ביותר הצפוי לפי התחזית ואת החודש שלו. המבחנים שלנו: תוספת של 1% לריבית בכל מסלול משתנה (פריים מהחודש הראשון, משתנה ביום השינוי שלו), ומסלול הריבית והמדד של 2022 עד 2023 לפי בנק ישראל והלמ״ס.' + (fin(inc) ? ' מעל ' + pc(100 * max, 0) + ' מההכנסה הבנק לא נותן הלוואה חדשה (הוראה 329).' : '');
    var src = [src451('סעיף 4ג(ב)(10)'), D.policy && D.policy.src, D.cpi && D.cpi.src];
    var q = ['מה יהיה ההחזר אם הפריים יעלה ב־1%, ובאיזה מסלול השינוי הכי גדול?'];
    if (over) add(res, 'amber', 13, 'ההחזר הגבוה עובר ' + pc(100 * max, 0) + ' מההכנסה', parts.join('. ') + '.', rule, src, PG.cap, q);
    else add(res, 'info', 13, T, parts.join('. ') + '.', rule, src, PG.cap, q);
  }

  function c14(st, D, res, M) {
    var T = 'סכומי החיובים והעמלות (שורה 11)', typed = BK.filter(function (k) { return fin(M[k].b.fees); });
    var rule8 = 'לפי הוראה 451 הבנק לא גובה עמלה להבטחת הלוואה, כמו דמי שריון או תשלום בגין אופציה לקבלת הלוואה.';
    if (st.h.resv === 'yes') add(res, 'red', 14, 'דמי שריון או תשלום על אופציה', 'סימנתם שבאישור מופיע תשלום להבטחת ההלוואה.', rule8, [src451('סעיף 8')], PG.pre, ['על מה התשלום הזה, ולמה הוא מופיע באישור?']);
    if (!typed.length) { if (st.h.resv !== 'yes') na(res, 14, T, 'לא הוקלדה שורה 11 באף סל.'); return; }
    var parts = typed.map(function (k) { return BTAB[k] + ' ' + ils(M[k].b.fees); }), q = ['מה כלול בסכומי החיובים והעמלות (שורה 11), ואילו מהם הוצאות לצד ג׳?'];
    var uni = ['b1', 'b2', 'b3'].filter(function (k) { return fin(M[k].b.fees); }).map(function (k) { return M[k].b.fees; });
    if (fin(M.offer.b.fees) && uni.length && M.offer.b.fees > Math.max.apply(null, uni) + 0.5) { parts.push('בסל המוצע ' + ils(M.offer.b.fees - Math.max.apply(null, uni)) + ' יותר מהסל האחיד היקר'); q.push('למה החיובים והעמלות בסל המוצע גבוהים ב־' + ils(M.offer.b.fees - Math.max.apply(null, uni)) + ' מהסלים האחידים?'); }
    (st.o || []).forEach(function (o, i) {
      var nm = (o.bank && o.bank !== 'other' && bankName(o.bank)) || ('אישור נוסף ' + (i + 1));
      ['b1', 'b2', 'b3'].forEach(function (k) {
        var a = M[k].b.fees, b2 = o.b[k].fees; if (!fin(a) || !fin(b2) || Math.abs(a - b2) < 0.5) return;
        parts.push(BTAB[k] + ' ב' + nm + ': ' + ils(b2) + (a > b2 ? ', ' + ils(a - b2) + ' פחות' : ', ' + ils(b2 - a) + ' יותר'));
        if (a > b2) q.push('למה סכומי החיובים והעמלות ' + BIN[k] + ' גבוהים ב־' + ils(a - b2) + ' מ' + nm + '?');
      });
    });
    add(res, 'info', 14, T, parts.join('; ') + '.' + (st.h.resv === 'no' ? ' סימנתם שאין דמי שריון.' : ''), 'השורה כוללת את החיובים, העמלות וההוצאות לצד ג׳ (כמו שמאי ורישום), והיא חלק מהריבית הכוללת החזויה. ' + rule8, [src451('סעיף 8 ותוספת 6')], PG.pre, q);
  }

  function c15(st, D, res, M) {
    add(res, 'info', 15, 'עמלת פתיחת תיק', fin(M.offer.b.fees) ? 'בסל המוצע הוקלדו ' + ils(M.offer.b.fees) + ' חיובים ועמלות; בדקו אם פתיחת התיק בתוכם.' : 'לא הוקלדה.', 'הסכום נקבע בתעריפון המשכנתאות של הבנק, והוראה 451 מפנה אליו. כל זכות כותבת עד 360 ₪, בלי מקור לסכום.', [src451('סעיף 4(א)(4)'), SRC.kzFile], PG.pre, ['כמה עולה פתיחת התיק לפי התעריפון שלכם, והאם היא בתוך שורה 11?']);
  }

  function c16(st, D, res, M) {
    var m = M.offer, F = D.fees, amb = [], q = [];
    m.tr.forEach(function (t) {
      var K = TK[t.k], none = t.k === 'prime' || K.directed || (K.kind === 'var' && (t.freq || 60) <= (F.no_cap_fee_if_change_within_months || 12));
      if (t.pp === 'yes' && none) { amb.push(TNAME[t.k] + ': באישור כתוב שיש עמלה בגין הפרשי ריבית, ולפי צו הבנקאות אין עמלת היוון ' + (t.k === 'prime' ? 'בפריים' : K.directed ? 'בהלוואה מכוונת' : 'במסלול שהריבית בו משתנה לפחות פעם בשנה')); q.push('באישור כתוב שיש עמלה בגין הפרשי ריבית במסלול ' + TNAME[t.k] + '. על איזו עמלה מדובר?'); }
    });
    var cuts = (F.reduce || []).map(function (x) { return pc(100 * x.cut, 0) + ' אחרי ' + x.after_years + ' שנים'; }).join(' ו־');
    var rule = 'לפי צו הבנקאות: במסלול קבוע, ובמשתנה עד יום השינוי, עמלת היוון כשהריבית הממוצעת ביום הפירעון נמוכה מהריבית בהלוואה, בהפחתה של ' + cuts + '; עמלה תפעולית עד ' + ils(F.operational_max) + '; ' + pc(100 * F.notice_rate, 1) + ' מהיתרה בהודעה של פחות מ־' + F.notice_days + ' ימים; בפריים, במסלול שהריבית בו משתנה לפחות פעם בשנה ובהלוואה מכוונת אין עמלת היוון.';
    var src = [srcOrder(D, 'סעיפים 2 עד 8 ו־10'), srcTerm(D, 'nl'), srcTerm(D, 'cpi')], hz = st.c.hz, you = '', lvl = amb.length ? 'amber' : 'info';
    var fixedShare = m.tr.length ? sum(m.tr.filter(function (t) { return TK[t.k].kind === 'fixed' && !TK[t.k].directed; }), function (t) { return t.amount; }) / m.sum : null;
    if (fin(hz) && hz > 0 && m.full) {
      var f = feeAt(m, D, hz * 12);
      if (f.end) you = 'בעוד ' + hz + ' שנים ההלוואה כבר נפרעה, ואין עמלת פירעון.';
      else {
        you = 'אם יוצאים בעוד ' + hz + ' שנים: יתרה של כ־' + ils(f.bal) + ', ' + (f.cap >= 0.5 ? 'עמלת היוון צפויה של כ־' + ils(f.cap) : 'בלי עמלת היוון לפי הממוצעים של היום') + ', עמלה תפעולית עד ' + ils(f.op) + ' ו־' + ils(f.notice) + ' בהודעה של פחות מ־' + F.notice_days + ' ימים. בריבית קבועה: ' + pc(100 * fixedShare, 0) + ' מההלוואה.';
        rule += ' החישוב: הממוצע של היום לתקופה שתישאר, פחות ' + pc(f.drop) + ' כמו ירידת הריבית בתחזית של בנק ישראל.';
        if (fixedShare >= 0.5 && f.cap >= 0.5) lvl = 'amber';
        res.exit = f;
      }
      q.push('מה תהיה עמלת הפירעון המוקדם בשנה ה־' + hz + ' בכל מסלול?');
    } else you = m.full ? 'הקלידו בעוד כמה שנים צפויה מכירה, שדרוג או מחזור, ונחשב את העמלה הצפויה.' : 'הקלידו את המסלולים של הסל המוצע ומתי צפויה יציאה, ונחשב את העמלה הצפויה.';
    if (!q.length) q.push('מה העמלה לפירעון מוקדם בכל מסלול, ובאילו מסלולים אין עמלת היוון?');
    var title = amb.length ? 'עמלת פירעון במסלול שהצו פוטר' : lvl === 'amber' ? 'חלק קבוע גדול ויציאה קרובה' : 'עמלת פירעון מוקדם';
    add(res, lvl, 16, title, (amb.length ? amb.join('. ') + '. ' : '') + you, rule, src, PG.refi, q);
  }

  function c17(st, D, res, M, RC) {
    var m = M.offer, rc = RC.offer, items = [], q = [];
    if (!m.tr.length) return na(res, 17, 'בלון, בוליט או גרייס', 'צריך את המסלולים של הסל המוצע (שורה 4).');
    m.tr.forEach(function (t, i) {
      if (t.method === 'balloon' || t.method === 'bullet') {
        var S = rc && rc.X.T[i];
        items.push(TNAME[t.k] + ' ב' + nameOf(METHOD, t.method) + (S && S.lump ? ': תשלום של ' + ils(S.lump) + ' ' + inMonth(S.lumpMonth) : ''));
        q.push(S && S.lump ? 'מאיפה יגיע התשלום של ' + ils(S.lump) + ' ' + inMonth(S.lumpMonth) + ', ומה קורה אם אין אותו?' : 'מה הסכום שמשלמים בסוף מסלול ה' + nameOf(METHOD, t.method) + ', ומתי?');
      }
      if (fin(t.grace) && t.grace > 0) { items.push(TNAME[t.k] + ': גרייס ' + (t.graceType === 'full' ? 'מלא' : 'חלקי') + ' ל־' + t.grace + ' חודשים, ' + (t.graceType === 'full' ? 'לא משלמים והריבית מצטרפת לקרן' : 'משלמים רק את הריבית')); q.push('מה יהיה ההחזר במסלול ' + TNAME[t.k] + ' כשהגרייס נגמר?'); }
    });
    var rule = 'בבלון הקרן והריבית משולמות בסוף; בבוליט משלמים ריבית כל חודש ואת הקרן בסוף; בגרייס מלא לא משלמים והריבית מצטרפת לקרן, ובגרייס חלקי משלמים רק את הריבית.';
    if (items.length) add(res, 'amber', 17, 'בלון, בוליט או גרייס', items.join('. ') + '.', rule, [src451('הגדרות')], PG.pre, q);
    else add(res, 'info', 17, 'לוח הסילוקין', 'כל המסלולים בסל המוצע בתשלום חודשי רגיל, בלי בלון, בוליט או גרייס.', rule, [src451('הגדרות')], PG.pre);
  }

  function c18(st, D, res, M) {
    var m = M.offer, FC = D.forecast, T = 'הצמדה למדד';
    if (!m.tr.length) {
      if (M.b2.any) return add(res, 'info', 18, T, 'בסל אחיד 2 שליש מההלוואה במשתנה צמודה למדד, לפי ההגדרה. בסל המוצע אפשר לבדוק כשמקלידים את המסלולים.', 'תחזית האינפלציה של חטיבת המחקר של בנק ישראל לארבעת הרבעונים הבאים: ' + pc(FC.inflation_4q, 1) + ' (' + dateHe(FC.published) + ').', [srcFc(D)], PG.cpi);
      return na(res, 18, T, 'צריך את המסלולים של הסל המוצע.');
    }
    var lk = m.tr.filter(function (t) { return TK[t.k].linked; }), ls = sum(lk, function (t) { return t.amount; }), sh = ls / m.sum;
    var rule = 'תחזית האינפלציה של חטיבת המחקר של בנק ישראל לארבעת הרבעונים הבאים: ' + pc(FC.inflation_4q, 1) + ' (' + dateHe(FC.published) + '). במסלול צמוד היתרה וההחזר עולים עם המדד.';
    if (!lk.length) return add(res, 'info', 18, T, 'אין מסלול צמוד למדד בסל המוצע.', rule, [srcFc(D)], PG.cpi);
    var you = 'החלק הצמוד למדד: ' + pc(100 * sh, 1) + ', ' + ils(ls) + '.';
    if (lk.every(complete)) {
      var rows = lk.map(function (t) { return eng(t); }), X2 = LG().mix(rows, LG().scenario({ cpi: FC.inflation_4q })), X0 = LG().mix(rows, LG().scenario({}));
      var n = Math.min(60, X2.N), b2 = X2.bal[n - 1], b0 = X0.bal[n - 1];
      you += ' באינפלציה של ' + pc(FC.inflation_4q, 1) + ' בשנה ההחזר במסלולים האלה עולה מ־' + ils(X2.pay[0]) + ' ל־' + ils(X2.pay[n - 1]) + ' אחרי ' + yrs(n) + ', והיתרה בהם אז ' + ils(b2) + (b2 - b0 >= 1 ? ', ' + ils(b2 - b0) + ' יותר מבלי מדד' : '') + '.';
    }
    add(res, 'info', 18, T, you, rule, [srcFc(D)], PG.cpi, sh >= 1 / 3 ? ['באיזה מדד ובאיזה מועד מוצמדת ההלוואה (שורת המידע הנוסף)?'] : null);
  }

  function c19(st, D, res, M) {
    var m = M.offer, T = 'מנגנון הריבית המשתנה';
    if (!m.tr.length) return na(res, 19, T, 'צריך את המסלולים של הסל המוצע (שורה 6).');
    var vs = m.tr.filter(function (t) { return TK[t.k].variable; });
    if (!vs.length) return;
    var lines = [], bad = [], q = [], P = D.policy.prime;
    vs.forEach(function (t) {
      if (t.k === 'prime') {
        if (!fin(t.margin)) { bad.push('פריים: חסר המרווח'); lines.push('פריים: חסר המרווח'); }
        else {
          var s = 'פריים ' + (t.margin < 0 ? 'פחות ' : 'ועוד ') + pc(Math.abs(t.margin)) + ', ' + pc(P + t.margin) + ' לפי הפריים של היום, ' + pc(P);
          if (fin(t.rate) && Math.abs(t.rate - (P + t.margin)) > 0.05) { s += '; באישור ' + pc(t.rate); bad.push('פריים: הריבית ' + pc(t.rate) + ' לא שווה לפריים ועוד המרווח, ' + pc(P + t.margin)); q.push('הריבית במסלול הפריים ' + pc(t.rate) + ', והפריים היום ' + pc(P) + '. מה המרווח המדויק?'); }
          lines.push(s);
        }
      } else {
        var fq = fin(t.freq) ? t.freq : 60, miss = !t.anchor || !fin(t.margin);
        lines.push(TNAME[t.k] + ': ' + (t.anchor ? 'עוגן ' + nameOf(ANCHOR, t.anchor) : 'חסר העוגן') + (fin(t.margin) ? ' ועוד מרווח ' + pc(t.margin) : ', חסר המרווח') + ', משתנה ' + nameOf(FREQ, fq) + '; השינוי הראשון בחודש ' + (fq + 1));
        if (miss) { bad.push(TNAME[t.k] + ': ' + (!t.anchor ? 'חסר העוגן' : 'חסר המרווח')); q.push('מה העוגן והמרווח במסלול ' + TNAME[t.k] + ', ומתי נקודת השינוי הראשונה?'); }
      }
    });
    var rule = 'בריבית משתנה האישור מציג את מנגנון קביעת הריבית (שורה 6): העוגן, המרווח ותדירות השינוי. הריבית באישור נכונה ליום האישור, ו״העוגן (באחוזים) יכול להשתנות ביום מתן ההלוואה״.';
    var src = [src451('סעיף 4ג(ב)(5), (ג)(1)'), D.policy.src ? { label: 'בנק ישראל, ריבית בנק ישראל והפריים מ־' + dateHe(D.policy.from), url: D.policy.src.url } : null];
    if (!q.length) q.push('מה מנגנון העוגן במסלולים המשתנים, ומתי נקודת השינוי הראשונה?');
    if (bad.length) add(res, 'amber', 19, 'חסר או לא מתאים במנגנון הריבית המשתנה', bad.join('. ') + '.', rule + ' ' + lines.join('. ') + '.', src, PG.pre, q);
    else add(res, 'info', 19, T, lines.join('. ') + '.', rule, src, PG.pre, q);
  }

  function c20(st, D, res) {
    if (st.h.guar === 'yes') add(res, 'amber', 20, 'נדרשים ערבים', 'באישור מסומן שנדרשים ערבים להלוואה.', 'השאלה ״האם נדרשים ערבים להלוואה״ מופיעה בראש האישור העקרוני בפורמט של הוראה 451. ערב אחראי לתשלום אם הלווים לא משלמים.', [src451('תוספת 6')], PG.pre, ['למה נדרשים ערבים, כמה, ומה יבטל את הדרישה?', 'על איזה סכום ועד מתי הערבות?']);
    else if (st.h.guar !== 'no') na(res, 20, 'ערבים', 'לא סומן אם נדרשים ערבים.');
  }

  function c21(st, D, res) {
    var L = st.h.loan, c = st.c, lines = ['אפשר לבטח את החיים ואת המבנה בחברה אחרת ולא דרך סוכנות הביטוח של הבנק, והבנק עונה על פוליסה שהוגשה תוך ' + R451.insDays + ' ימים.'];
    if (fin(L) && L <= R451.noInsUpTo) lines.push('על הלוואה או יתרה של עד ' + ils(R451.noInsUpTo) + ' הבנק לא דורש ביטוח חיים או נכס.');
    lines.push('ביטוח הנכס לא גבוה מיתרת ההלוואה המשוערכת, בלי הקרקע ועוד עד ' + R451.insExtra + '%.');
    if (st.h.newb === 'new') lines.push('בדירה חדשה מקבלן הבנק לא דורש ביטוח נכס לפני מועד המסירה שבחוזה' + (st.h.delivery && LR().parseMonth(st.h.delivery) ? ', ' + monthHe(LR().parseMonth(st.h.delivery)) : '') + '.');
    lines.push('הבנק מודיע ' + R451.insNotice + ' ימים לפני תום שנת הביטוח.');
    var you = fin(c.life) || fin(c.struct) ? 'הצעות שהקלדתם: ' + [fin(c.life) ? 'ביטוח חיים ' + ils(c.life) + ' בחודש' : '', fin(c.struct) ? 'ביטוח מבנה ' + ils(c.struct) + ' בחודש' : ''].filter(Boolean).join(', ') + '.' : 'לא הוקלדו הצעות ביטוח.';
    add(res, 'info', 21, 'ביטוח חיים ומבנה', you, lines.join(' '), [src451('סעיף 11'), SRC.life, SRC.dira], PG.ins, ['האם אפשר לקבל את ביטוח החיים והמבנה מחברה אחרת, ומה הבנק צריך לאשר תוך ' + R451.insDays + ' יום?']);
  }

  function c22(st, D, res, M, RC) {
    var T = 'העלות החודשית המלאה', pay = payOf(M, RC, 'offer'), c = st.c;
    if (!fin(pay)) return na(res, 22, T, 'לא הוקלד ההחזר הראשון בסל המוצע.');
    var ins = (fin(c.life) && c.life > 0 ? c.life : 0) + (fin(c.struct) && c.struct > 0 ? c.struct : 0), arn = fin(c.arn) && c.arn > 0 ? c.arn : 0;
    var fc = LQ() && LQ().fullCost ? LQ().fullCost(pay, ins, arn) : { total: pay + ins + arn, ins: ins, arn: arn, any: ins + arn > 0 };
    var rule = 'אין מחירון רשמי לביטוח משכנתא: רשות שוק ההון מפרסמת מחשבוני השוואה לביטוח חיים ולביטוח מבנה. ארנונה וועד בית לפי הרשות המקומית והבניין, ולכן השדות נשארים ריקים עד שמקלידים.';
    var src = [SRC.life, SRC.dira];
    if (!fc.any) return add(res, 'info', 22, T, 'הוקלד רק ההחזר, ' + ils(pay) + '. ביטוח, ארנונה וועד בית לא הוקלדו.', rule, src, PG.ins);
    var inc = c.income, parts = ['החזר ' + ils(pay)];
    if (fc.ins) parts.push('ביטוח ' + ils(fc.ins)); if (fc.arn) parts.push('ארנונה וועד בית ' + ils(fc.arn));
    add(res, 'info', 22, T, parts.join(' ועוד ') + ': ' + ils(fc.total) + ' בחודש' + (fin(inc) && inc > 0 ? ', ' + pc(100 * fc.total / inc, 1) + ' מההכנסה הפנויה' : '') + '.', rule, src, PG.ins);
  }

  function c23(st, D, res) {
    add(res, 'info', 23, 'שמאות', 'הבדיקה הזאת כללית.', 'לפי הוראה 451 הבנק גובה על השמאות את הנמוך מההוצאה בפועל ומהתעריפון; לווה ששילם מקבל העתק של הדוח; ואפשר להשתמש בשומה שנעשתה לבנק אחר אם לא עברו ' + R451.appraisalDays + ' ימים והשמאי ברשימת השמאים של הבנק.', [src451('סעיף 9(ג) עד (ה)')], PG.pre, ['האם אפשר להשתמש בשומה מבנק אחר (פחות מ־' + R451.appraisalDays + ' יום), וכמה עולה שמאות לפי התעריפון?']);
  }

  function c24(st, D, res, M) {
    var e = st.c.elig, rule = 'תעודת זכאות תקפה שנה מיום הבקשה, ואת הבקשה מגישים לפני החתימה על חוזה הרכישה. בהלוואת זכאות אין עמלת פירעון מוקדם.';
    var src = [SRC.gov, srcOrder(D, 'סעיף 2')];
    if (e === 'unk') add(res, 'amber', 24, 'זכאות משרד הבינוי והשיכון לא נבדקה', 'סימנתם שהזכאות לא נבדקה.', rule, src, null, ['האם הלוואת זכאות יכולה להיכלל בתמהיל, ובאיזו ריבית?']);
    else if (e === 'yes') {
      var has = M.offer.tr.some(function (t) { return t.k === 'zakaut'; });
      if (M.offer.tr.length && !has) add(res, 'amber', 24, 'יש תעודת זכאות, ואין הלוואת זכאות בסל המוצע', 'סימנתם שיש זכאות; בסל המוצע אין מסלול של הלוואת זכאות.', rule, src, null, ['למה הלוואת הזכאות לא בתמהיל?']);
      else add(res, 'info', 24, 'זכאות משרד הבינוי והשיכון', has ? 'בסל המוצע יש הלוואת זכאות.' : 'סימנתם שיש זכאות.', rule, src, null);
    } else if (e !== 'no') na(res, 24, 'זכאות', 'לא סומן אם נבדקה זכאות.');
  }

  function c25(st, D, res, M) {
    if (st.h.newb !== 'new') return;
    var dl = st.h.delivery ? LR().parseMonth(st.h.delivery) : null, ap = parseDate(st.h.date), g = M.offer.tr.reduce(function (a, t) { return Math.max(a, fin(t.grace) ? t.grace : 0); }, 0), you;
    var n = dl && ap ? LR().mDiff(ap.slice(0, 7), dl) : null;
    you = dl ? 'מסירה ב־' + monthHe(dl) + (fin(n) ? ', בעוד ' + n + ' חודשים מתאריך האישור' : '') : 'לא הוקלד מועד המסירה';
    if (M.offer.tr.length) you += g ? '; גרייס של ' + g + ' חודשים' + (fin(n) && n > 0 ? (g < n ? ', שנגמר ' + (n - g) + ' חודשים לפני המסירה' : g > n ? ', שנמשך ' + (g - n) + ' חודשים אחרי המסירה' : ', עד המסירה') : '') : '; בלי גרייס באישור';
    add(res, 'info', 25, 'דירה חדשה מקבלן', you + '.', 'בדירה מקבלן התשלומים לקבלן צמודים למדד תשומות הבנייה לפי חוק המכר, והמשכנתא נמשכת לפי מועדי התשלום. הכלי ״מהחוזה למפתח״ בעמוד הזה מחשב את התשלומים, ההצמדה וההחזר עד המסירה.', [SRC.sale], PG.cii, ['איך המשיכות מתואמות עם מועדי התשלום לקבלן, ומה ההחזר עד המסירה?']);
  }

  function c27(st, D, res) {
    add(res, 'info', 27, 'לפני העברת כסף למוכר או לקבלן', 'הבדיקה הזאת כללית.', 'לפני כל העברה מאמתים את פרטי החשבון בשיחת טלפון למספר שנשמר מראש, לא למספר שהגיע בהודעה או במייל. כסף המשכנתא מועבר ישירות למוכר אחרי האישור הסופי.', [SRC.cfpb, SRC.kzFile], PG.pre, ['איך מתבצעת ההעברה למוכר, ואיזה אישור בכתב מקבלים עליה?']);
  }
  function c28(st, D, res) {
    add(res, 'info', 28, 'דוח נתוני אשראי', 'הבדיקה הזאת כללית.', 'פעם בשנה אפשר לקבל בחינם דוח ריכוז נתונים על האשראי שלכם ממערכת נתוני האשראי של בנק ישראל, ולבדוק אותו לפני הבקשה.', [SRC.kzCredit, SRC.credit], null);
  }

  /* ----------------------------------------------------------------------------------------------- mode 2 (check 26) */
  function matchTracks(a, b) {  // each final track to the first unmatched approval track of the same name, in order
    var used = {}, pairs = [];
    b.forEach(function (t) { var j = -1; for (var i = 0; i < a.length; i++) if (!used[i] && a[i].k === t.k) { j = i; break; } if (j > -1) used[j] = 1; pairs.push({ a: j > -1 ? a[j] : null, b: t }); });
    a.forEach(function (t, i) { if (!used[i]) pairs.push({ a: t, b: null }); });
    return pairs;
  }
  function c26(st, D, res, today) {
    var ap = st.b.offer, f = st.f, at = tracksOk(ap.tracks), ft = tracksOk(f.tracks), ch = [];
    var rule = 'כל שינוי מול האישור העקרוני: לשאול למה, לפני החתימה. כך בודקים בארצות הברית את המסמכים הסופיים מול ההצעה.';
    var src = [SRC.cfpb, src451('סעיף 4ג(ו)')];
    var push = function (lvl, title, you, q) { ch.push({ lvl: lvl, title: title, you: you, q: q }); };
    var aL = fin(st.h.loan) ? st.h.loan : (at.length ? sum(at, function (t) { return t.amount; }) : null), fL = fin(f.loan) ? f.loan : (ft.length ? sum(ft, function (t) { return t.amount; }) : null);
    if (!at.length && !fin(aL)) { na(res, 26, 'המסמכים מול האישור', 'כדי להשוות צריך את הסל המוצע באישור: עברו ל״האישור העקרוני״ והקלידו את המסלולים.'); return; }
    if (fin(aL) && fin(fL) && Math.abs(fL - aL) > 0.5) push(fL > aL ? 'red' : 'amber', 'הסכום השתנה', 'במסמכים ' + ils(fL) + ', באישור ' + ils(aL) + ': ' + (fL > aL ? 'יותר' : 'פחות') + ' ב־' + ils(Math.abs(fL - aL)) + '.', 'למה סך ההלוואה במסמכים שונה מהאישור?');
    if (f.guar === 'yes' && st.h.guar !== 'yes') push('red', 'נוספו ערבים', 'במסמכים נדרשים ערבים; באישור ' + (st.h.guar === 'no' ? 'לא נדרשו' : 'זה לא סומן') + '.', 'למה נדרשים עכשיו ערבים?');
    if (fin(f.fees)) {
      if (!fin(ap.fees)) push('amber', 'חיובים ועמלות', 'במסמכים ' + ils(f.fees) + '; באישור לא הוקלדה שורה 11.', 'מה כלול בחיובים ובעמלות במסמכים, ומה היה באישור?');
      else if (f.fees > ap.fees + 0.5) push('red', 'החיובים והעמלות עלו', 'במסמכים ' + ils(f.fees) + ', באישור ' + ils(ap.fees) + ': עוד ' + ils(f.fees - ap.fees) + '.', 'למה החיובים והעמלות עלו ב־' + ils(f.fees - ap.fees) + ' מהאישור העקרוני?');
      else if (f.fees < ap.fees - 0.5) push('amber', 'החיובים והעמלות ירדו', 'במסמכים ' + ils(f.fees) + ', באישור ' + ils(ap.fees) + '.', 'מה השתנה בחיובים ובעמלות מהאישור?');
    }
    if (f.ins === 'yes') push('red', 'דרישת ביטוח חדשה', 'במסמכים מופיעה דרישת ביטוח שלא הופיעה באישור.', 'למה נוספה דרישת ביטוח, והאם אפשר לבטח בחברה אחרת?');
    matchTracks(at, ft).forEach(function (p) {
      if (!p.a) { push('red', 'מסלול חדש', TNAME[p.b.k] + ' של ' + ils(p.b.amount) + ' במסמכים, ואין מסלול כזה בסל המוצע.', 'למה נוסף מסלול ' + TNAME[p.b.k] + ' שלא היה באישור?'); return; }
      if (!p.b) { push('red', 'מסלול חסר', TNAME[p.a.k] + ' של ' + ils(p.a.amount) + ' מהסל המוצע לא מופיע במסמכים.', 'מה קרה למסלול ' + TNAME[p.a.k] + ' שהיה באישור?'); return; }
      var a = p.a, b = p.b, n = TNAME[a.k];
      if (fin(a.amount) && fin(b.amount) && Math.abs(a.amount - b.amount) > 0.5) push(b.amount > a.amount ? 'red' : 'amber', 'הסכום במסלול השתנה', n + ': במסמכים ' + ils(b.amount) + ', באישור ' + ils(a.amount) + '.', 'למה הסכום במסלול ' + n + ' שונה מהאישור?');
      if (fin(a.months) && fin(b.months) && a.months !== b.months) push('red', 'התקופה השתנתה', n + ': במסמכים ' + b.months + ' חודשים, באישור ' + a.months + '.', 'למה התקופה במסלול ' + n + ' שונה מהאישור?');
      if (fin(a.rate) && fin(b.rate) && Math.abs(a.rate - b.rate) >= 0.005) push(b.rate > a.rate ? 'red' : 'amber', b.rate > a.rate ? 'הריבית עלתה' : 'הריבית ירדה', n + ': במסמכים ' + pc(b.rate) + ', באישור ' + pc(a.rate) + '.', 'למה הריבית במסלול ' + n + ' ' + (b.rate > a.rate ? 'גבוהה' : 'שונה') + ' מהאישור, בתוך תקופת השמירה?');
      if (a.method !== b.method) push('red', 'אופן התשלום השתנה', n + ': במסמכים ' + nameOf(METHOD, b.method) + ', באישור ' + nameOf(METHOD, a.method) + '.', 'למה אופן התשלום במסלול ' + n + ' השתנה?');
      if ((fin(a.grace) ? a.grace : 0) !== (fin(b.grace) ? b.grace : 0)) push('red', 'הגרייס השתנה', n + ': במסמכים ' + (fin(b.grace) ? b.grace : 0) + ' חודשי גרייס, באישור ' + (fin(a.grace) ? a.grace : 0) + '.', 'למה הגרייס במסלול ' + n + ' השתנה?');
      if (TK[a.k].variable) {
        if (fin(a.margin) && fin(b.margin) && Math.abs(a.margin - b.margin) >= 0.005) push(b.margin > a.margin ? 'red' : 'amber', 'המרווח השתנה', n + ': במסמכים ' + pc(b.margin) + ', באישור ' + pc(a.margin) + '.', 'למה המרווח במסלול ' + n + ' שונה מהאישור?');
        if (a.k !== 'prime' && a.freq !== b.freq) push('red', 'תדירות השינוי השתנתה', n + ': במסמכים ' + nameOf(FREQ, b.freq) + ', באישור ' + nameOf(FREQ, a.freq) + '.', 'למה תדירות שינוי הריבית במסלול ' + n + ' שונה?');
        if (a.k !== 'prime' && a.anchor && b.anchor && a.anchor !== b.anchor) push('red', 'העוגן השתנה', n + ': במסמכים ' + nameOf(ANCHOR, b.anchor) + ', באישור ' + nameOf(ANCHOR, a.anchor) + '.', 'למה העוגן במסלול ' + n + ' השתנה?');
      }
      if (a.pp === 'no' && b.pp === 'yes') push('red', 'נוספה עמלה בגין הפרשי ריבית', n + ': באישור לא הייתה, במסמכים יש.', 'למה נוספה עמלת פירעון בגין הפרשי ריבית במסלול ' + n + '?');
    });
    var fd = parseDate(f.date), ad = parseDate(st.h.date);
    if (fd && ad) {
      var days = st.h.lien === 'no' ? R451.holdNoLien : R451.hold, exp = addDays(ad, days);
      if (fd > exp) push('amber', 'המסמכים אחרי תקופת השמירה', 'המסמכים מ־' + dateHe(fd) + ', אחרי ' + dateHe(exp) + ' (' + days + ' ימים מהאישור).', 'האם קיבלתם אישור עקרוני מעודכן, כמו שהוראה 451 מחייבת כשהתקופה עברה?');
    }
    res.diff = ch;
    if (!ch.length) add(res, 'info', 26, 'לא נמצאו שינויים מול האישור', 'הושוו סך ההלוואה, הערבים, החיובים והעמלות, ובכל מסלול: הסכום, התקופה, הריבית, אופן התשלום, הגרייס, המנגנון של ריבית משתנה ועמלת הפירעון.', rule, src, PG.pre);
    ch.forEach(function (c) { add(res, c.lvl, 26, c.title, c.you, rule, src, PG.pre, [c.q]); });
  }

  /* ============================================================================================= run, summary, questions */
  function run(st0, D, XR, today) {
    today = today || todayISO();
    var err = validate(st0), st = scrub(st0, err), res = { flags: [], na: [], err: err, today: today, mode: st.mode, st: st };
    var M = {}, RC = {};
    BK.forEach(function (k) { M[k] = bmodel(st, k); });
    res.M = M;
    if (st.mode === 'fin') {
      var f = st.f;
      res.empty = !(fin(f.loan) || tracksOk(f.tracks).length || f.date || fin(f.fees) || f.guar || f.ins);
      if (!res.empty) { c26(st, D, res, today); c1(st, D, res, today); c27(st, D, res); }
      return finish(res, st, D);
    }
    res.empty = !BK.some(function (k) { return M[k].any; }) && !fin(st.h.loan) && !st.h.date && !fin(st.h.price);
    if (res.empty) return finish(res, st, D);
    BK.forEach(function (k) { RC[k] = recompute(M[k], D); });
    res.RC = RC;
    c1(st, D, res, today); c2(st, D, res, M); c3(st, D, res, M); c4(st, D, res, M); c5(st, D, res); c6(st, D, res, M, RC); c7(st, D, res, M); c8(st, D, res, M);
    c9(st, D, res, M); c10(st, D, res, M); c11(st, D, res, M); c12(st, D, res, M, RC); c13(st, D, res, M, RC, XR); c14(st, D, res, M); c15(st, D, res, M);
    c16(st, D, res, M); c17(st, D, res, M, RC); c18(st, D, res, M); c19(st, D, res, M); c20(st, D, res); c21(st, D, res); c22(st, D, res, M, RC); c23(st, D, res);
    c24(st, D, res, M); c25(st, D, res, M); c27(st, D, res); c28(st, D, res);
    return finish(res, st, D);
  }
  function finish(res, st, D) {
    var ord = { red: 0, amber: 1, info: 2 };
    res.flags.forEach(function (f, i) { f.i = i; });
    res.flags.sort(function (a, b) { return ord[a.level] - ord[b.level] || a.id - b.id || a.i - b.i; });
    res.counts = { red: 0, amber: 0, info: 0 };
    res.flags.forEach(function (f) { res.counts[f.level]++; });
    res.sum = res.empty ? [] : st.mode === 'fin' ? summaryFin(res, st, D) : summary(res, st, D);
    res.qs = questions(res);
    return res;
  }
  function questions(res) { var seen = {}, out = []; res.flags.forEach(function (f) { f.q.forEach(function (q) { if (!seen[q]) { seen[q] = 1; out.push(q); } }); }); return out.slice(0, 14); }
  function countText(res) {
    var c = res.counts, p = [];
    p.push(c.red ? 'נמצאו בבדיקה ' + plural(c.red, 'דגל אדום אחד', 'דגלים אדומים') : 'לא נמצאו בבדיקה דגלים אדומים');
    p.push(c.amber ? plural(c.amber, 'נקודה אחת לבדיקה מול הבנק', 'נקודות לבדיקה מול הבנק') : 'אין נקודות לבדיקה מול הבנק');
    if (res.na.length) p.push(plural(res.na.length, 'בדיקה אחת לא רצה', 'בדיקות לא רצו') + ' בלי נתונים נוספים');
    return p.join('; ') + '.';
  }
  /* the summary: plain sentences, only typed numbers and dated official figures, no recommendation */
  function summary(res, st, D) {
    var S = [], h = st.h, M = res.M, RC = res.RC || {}, b = M.offer.b, L = h.loan, inc = st.c.income, lo = fin(st.c.loans) && st.c.loans > 0 ? st.c.loans : 0;
    if (fin(L)) {
      var cap = D.rules.ltv[h.buyer] != null ? D.rules.ltv[h.buyer] : D.rules.ltv.single;
      S.push('האישור העקרוני' + (h.bank && h.bank !== 'other' ? ' מ' + bankName(h.bank) : '') + (parseDate(h.date) ? ' מ־' + dateHe(parseDate(h.date)) : '') + ' הוא על ' + ils(L) + (fin(h.price) && h.price > 0 ? ' לדירה של ' + ils(h.price) + ', מימון של ' + pc(100 * L / h.price, 1) + ' (המגבלה ב' + (nameOf(BUYER, h.buyer) || 'דירה יחידה') + ' לפי הוראה 329: ' + pc(100 * cap, 0) + ')' : '') + '.');
    }
    if (res.valid) { var v = res.valid; S.push(v.left < 0 ? 'תקופת השמירה של ' + v.days + ' ימים לפי הוראה 451 הסתיימה ב־' + dateHe(v.exp) + '.' : 'לפי הוראה 451 התנאים שמורים ' + v.days + ' ימים לפחות: ' + (v.left === 0 ? 'היום הוא היום האחרון' : 'נשארו ' + plural(v.left, 'יום אחד', 'ימים')) + ', עד ' + dateHe(v.exp) + '.'); }
    var pay = payOf(M, RC, 'offer');
    if (fin(pay)) {
      var hi = fin(b.max) ? b.max : RC.offer ? RC.offer.max : null, hm = fin(b.max) ? b.maxM : RC.offer ? RC.offer.maxM : null;
      S.push('בסל המוצע ההחזר הראשון ' + ils(pay) + (fin(inc) && inc > 0 ? ', ' + pc(100 * (pay + lo) / inc, 1) + ' מההכנסה הפנויה' + (lo ? ' יחד עם ההלוואות האחרות' : '') : '') + (fin(hi) ? ', וההחזר הגבוה הצפוי ' + ils(hi) + (fin(hm) ? ' ' + inMonth(hm) : '') + (fin(inc) && inc > 0 ? ', ' + pc(100 * (hi + lo) / inc, 1) : '') : '') + '.');
    }
    var main = fin(b.irr) ? 'offer' : BK.filter(function (k) { return fin(M[k].b.irr); })[0], ref = bankRefOf(D, h.bank), sys = bankRefOf(D, 'system');
    if (main && sys) {
      var x = M[main].b.irr, own = ref && ref.key !== 'system';
      S.push('הריבית הכוללת החזויה ' + BIN[main] + ' היא ' + pc(x) + '; בקו המשווה של בנק ישראל ל־' + monthHe(sys.month) + ' ' + (own ? 'הממוצע של ' + ref.name + ' ' + pc(ref.irr) + ' ו' : '') + 'הממוצע של כל הבנקים ' + pc(sys.irr) + '.');
    }
    var fees = BK.filter(function (k) { return fin(M[k].b.fees); });
    if (fees.length) S.push('סכומי החיובים והעמלות: ' + fees.map(function (k) { return BTAB[k] + ' ' + ils(M[k].b.fees); }).join(', ') + '.');
    if (res.exit) S.push('אם יוצאים מההלוואה בעוד ' + st.c.hz + ' שנים, עמלת ההיוון הצפויה בסל המוצע לפי צו הבנקאות ' + (res.exit.cap >= 0.5 ? 'היא כ־' + ils(res.exit.cap) : 'לא חלה לפי הממוצעים של היום') + ', על יתרה של כ־' + ils(res.exit.bal) + '.');
    var lk = M.offer.tr.length ? sum(M.offer.tr.filter(function (t) { return TK[t.k].linked; }), function (t) { return t.amount; }) / M.offer.sum : null;
    if (fin(lk) && S.length < 7) S.push(lk > 0 ? 'החלק הצמוד למדד בסל המוצע ' + pc(100 * lk, 1) + ', ותחזית האינפלציה של בנק ישראל (' + dateHe(D.forecast.published) + ') היא ' + pc(D.forecast.inflation_4q, 1) + ' בשנה.' : 'בסל המוצע אין מסלול צמוד למדד.');
    S.push(countText(res));
    return S.slice(0, 8);
  }
  function summaryFin(res, st, D) {
    var S = [], d = res.diff || [], red = d.filter(function (c) { return c.lvl === 'red'; }).length, f = st.f, fd = parseDate(f.date), ad = parseDate(st.h.date);
    S.push('השוואה של המסמכים הסופיים' + (fd ? ' מ־' + dateHe(fd) : '') + ' לסל המוצע באישור העקרוני' + (ad ? ' מ־' + dateHe(ad) : '') + '.');
    if (d.length) S.push('נמצאו ' + plural(d.length, 'שינוי אחד', 'שינויים') + ', ' + (red ? plural(red, 'אחד מהם מייקר או מוסיף דרישה', 'מהם מייקרים או מוסיפים דרישה') : 'אף אחד מהם לא מייקר') + '.');
    else if (res.flags.some(function (x) { return x.id === 26; })) S.push('לא נמצאו שינויים בשדות שהוקלדו.');
    var fL = fin(f.loan) ? f.loan : null; if (fL) S.push('סך ההלוואה במסמכים ' + ils(fL) + (fin(st.h.loan) ? ', ובאישור ' + ils(st.h.loan) : '') + '.');
    if (res.valid) S.push(res.valid.left < 0 ? 'תקופת השמירה של האישור הסתיימה ב־' + dateHe(res.valid.exp) + '.' : 'תקופת השמירה של האישור נמשכת עד ' + dateHe(res.valid.exp) + '.');
    S.push('לפני כל העברת כסף מאמתים את פרטי החשבון בטלפון, למספר שנשמר מראש.');
    S.push(countText(res));
    return S.slice(0, 8);
  }
  function text(res, st, today) {
    var L = ['בדיקת משכנתא לפני חתימה, ' + dateHe(today || res.today) + (st.mode === 'fin' ? ': המסמכים הסופיים מול האישור' : '')];
    if (res.empty) { L.push('', 'לא הוקלדו נתונים.'); return L.join('\n'); }
    L.push('', res.sum.join(' '));
    ['red', 'amber', 'info'].forEach(function (lv) {
      var fs = res.flags.filter(function (f) { return f.level === lv; }); if (!fs.length) return;
      L.push('', GROUP[lv] + ':');
      fs.forEach(function (f) { L.push('• ' + f.title + ' (בדיקה ' + f.id + '): ' + f.you + (f.rule ? ' ' + f.rule : '') + (f.src.length ? ' מקור: ' + f.src.map(function (s) { return s.label; }).join('; ') + '.' : '')); });
    });
    if (res.qs.length) { L.push('', 'מה לשאול את הבנק:'); res.qs.forEach(function (q, i) { L.push((i + 1) + '. ' + q); }); }
    L.push('', 'הבדיקה משווה את המספרים שהקלדתם לכללים של בנק ישראל ולנתונים הרשמיים. היא אינה ייעוץ.');
    return L.join('\n');
  }

  /* ============================================================================================== the example (9.2026) */
  /* an approval built from the Bank of Israel averages of the latest month (by_bank, all banks): 1,200,000 ILS for 25 years on a
     1,600,000 ILS home, dated 5 days before today. The proposed basket is the all-banks mix at the all-banks rates (effective turned
     nominal), and its overall rate is the all-banks figure that the Bank of Israel published; the uniform baskets at the same track
     rates. Rows 8 to 10 are this tool's own computation on the Research forecast; row 7 of the uniform baskets and row 11 stay
     empty, because no official figure exists for them. */
  function example(D, today) {
    var st = blank(), sys = LR().bankMix(D, 'system'), nom = {}, L = 1200000, N = 300;
    sys.rows.forEach(function (r) { nom[r.k] = Math.round(r.rate * 100) / 100; });
    var rate = function (k) { return nom[TK[k] ? TK[k].bb : k]; };
    var anchorMargin = function (t) {
      if (t.k === 'prime') { t.anchor = 'prime'; t.margin = Math.round((t.rate - D.policy.prime) * 100) / 100; t.pp = 'no'; }
      else if (TK[t.k].kind === 'var') { t.anchor = 'gov'; t.freq = 60; t.margin = t.k === 'var_cpi' && D.rates && D.rates.var_cpi && fin(D.rates.var_cpi.bench) ? Math.round((t.rate - D.rates.var_cpi.bench) * 100) / 100 : null; t.pp = 'yes'; }
      else t.pp = 'yes';
      return t;
    };
    st.h = { bank: 'other', date: dateHe(addDays(today || todayISO(), -5)), guar: 'no', price: 1600000, buyer: 'single', newb: 'used', delivery: '', loan: L, lien: 'yes', resv: 'no' };
    var map = { fixed_nl: 'fixed_nl', prime: 'prime', var_nl_other: 'var_nl', var_cpi: 'var_cpi', fixed_cpi: 'fixed_cpi' };
    var am = splitAmounts(L, sys.rows.map(function (r) { return r.share / 100; }));
    st.b.offer.tracks = sys.rows.map(function (r, i) { return anchorMargin(blankTrack(map[r.k], { amount: am[i], months: N, rate: nom[r.k] })); });
    ['b1', 'b2', 'b3'].forEach(function (k) { st.b[k].tracks = fillDef(D, k, L, N, rate).map(anchorMargin); });
    BK.forEach(function (k) {
      var b = st.b[k], rc = recompute(bmodel(st, k), D);
      b.term = N; if (rc) { b.first = Math.round(rc.first); b.max = Math.round(rc.max); b.maxM = rc.maxM; b.total = Math.round(rc.total); }
    });
    st.b.offer.irr = Math.round(sys.irr * 100) / 100;
    st.c = { income: 24000, loans: 1200, equity: 450000, hz: 7, elig: 'unk', life: null, struct: null, arn: null };
    return st;
  }

  var NLMC = { BK: BK, BNAME: BNAME, BTAB: BTAB, TRK: TRK, TNAME: TNAME, TK: TK, FREQ: FREQ, METHOD: METHOD, ANCHOR: ANCHOR, BANKS: BANKS, BANK_HE: BANK_HE, BUYER: BUYER,
    R451: R451, PG: PG, GROUP: GROUP, TERMS451: TERMS451,
    num: num, ils: ils, pc: pc, parseDate: parseDate, dateHe: dateHe, monthHe: monthHe, addDays: addDays, dayDiff: dayDiff, todayISO: todayISO,
    blank: blank, blankTrack: blankTrack, blankOther: blankOther, restore: restore, basketDef: basketDef, defText: defText, fillDef: fillDef, splitAmounts: splitAmounts,
    bmodel: bmodel, eng: eng, recompute: recompute, irrOf: irrOf, stressMix: stressMix, replayMix: replayMix, capFee: capFee, feeAt: feeAt,
    validate: validate, run: run, text: text, example: example, matchTracks: matchTracks };
  G.NLMC = NLMC;
  if (typeof document === 'undefined' || !G.NadLanInstruments) return;

  /* ===================================================================================================== the page */
  var PID = 'nlmc';
  function css(id) {
    var sid = 'nlmc-css-' + id; if (document.getElementById(sid)) return;
    var P = '#' + id, SANS = '"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif', MONO = '"IBM Plex Mono",ui-monospace,monospace';
    var r = [
      P + '{--c:#2F6F86}',
      P + ' .is-red{--c:#C42550}' + P + ' .is-amber{--c:#F2D15A}' + P + ' .is-info{--c:#2F6F86}',
      P + ' .nlc__top{display:grid;gap:12px;margin:0 0 16px;position:relative}',
      P + ' .nlc__btns{display:flex;flex-wrap:wrap;gap:8px}',
      P + ' button.nlc__b{display:inline-flex!important;align-items:center;min-height:44px!important;padding:10px 16px!important;border:1px solid #2F6F86!important;border-radius:2px!important;background:#FFFFFF!important;color:#2F6F86!important;font:500 15px/20px ' + SANS + '!important;cursor:pointer;margin:0!important;box-shadow:none!important;text-transform:none!important;letter-spacing:0!important;width:auto!important}',
      P + ' button.nlc__b.is-main{background:#2F6F86!important;color:#FFFFFF!important}',
      P + ' button.nlc__b.is-quiet{border-color:#D3DCE2!important;color:#3E4C58!important}',
      P + ' .nli__form{gap:14px}',
      P + ' fieldset.nlc__fs{border:1px solid #D3DCE2!important;border-radius:2px!important;padding:12px!important;margin:0!important;min-width:0;background:#F6F8F9!important;display:grid;gap:12px}',
      P + ' fieldset.nlc__fs>legend{font:600 16px/22px ' + SANS + '!important;color:#12202A!important;padding:0 6px!important;margin:0!important;border:0!important;width:auto!important;float:none!important;background:none!important}',
      P + ' p.nlc__fh{font:400 13px/19px ' + SANS + '!important;color:#5E6A75!important;margin:0!important}',
      P + ' .nlc__g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;align-items:end}',
      P + ' .nlc__g2>.nlc__wide{grid-column:1/-1}',
      P + ' .nli__f>label{font:500 13px/18px ' + SANS + '!important;color:#3E4C58!important;margin:0!important}',
      P + ' .nli__in{min-height:46px}' + P + ' .nli__in input,' + P + ' .nli__in select{font-size:16px!important;min-height:44px!important;padding:9px 10px!important}',
      P + ' .nli__unit{padding:0 8px;font-size:13px}',
      P + ' .nlc__tabs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}',
      P + ' .nlc__tabs button{min-height:44px!important;padding:6px 4px!important;border:1px solid #D3DCE2!important;border-radius:2px!important;background:#FFFFFF!important;color:#3E4C58!important;font:500 14px/18px ' + SANS + '!important;cursor:pointer;margin:0!important;box-shadow:none!important;text-transform:none!important;letter-spacing:0!important;width:auto!important}',
      P + ' .nlc__tabs button[aria-selected="true"]{background:#2F6F86!important;border-color:#2F6F86!important;color:#FFFFFF!important;font-weight:600!important}',
      P + ' .nlc__tabs button.has::after{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:currentColor;margin-inline-start:6px;vertical-align:middle}',
      P + ' .nlc__pane{display:grid;gap:12px;min-width:0}',
      P + ' p.nlc__def{font:500 14px/20px ' + SANS + '!important;color:#3E4C58!important;margin:0!important;padding:8px 10px!important;border-inline-start:3px solid #2F6F86;background:#FFFFFF}',
      P + ' .nlc__trs{display:grid;gap:10px}',
      P + ' .nlc__tr{border:1px solid #D3DCE2;border-inline-start:4px solid #2F6F86;border-radius:2px;background:#FFFFFF;padding:10px;display:grid;gap:10px;min-width:0}',
      P + ' .nlc__trh{display:flex;align-items:center;justify-content:space-between;gap:8px;font:600 14px/20px ' + SANS + ';color:#12202A}',
      P + ' button.nlc__x{min-height:44px!important;min-width:44px!important;border:1px solid #D3DCE2!important;border-radius:2px!important;background:#FFFFFF!important;color:#3E4C58!important;cursor:pointer;font:400 18px/1 ' + SANS + '!important;margin:0!important;padding:0!important;box-shadow:none!important}',
      P + ' button.nlc__tog{justify-self:start;min-height:44px!important;padding:10px 14px!important;border:1px dashed #2F6F86!important;border-radius:2px!important;background:#FFFFFF!important;color:#2F6F86!important;font:500 14px/20px ' + SANS + '!important;cursor:pointer;margin:0!important;box-shadow:none!important;text-align:right;white-space:normal}',
      P + ' details.nlc__det{border:1px solid #D3DCE2;border-radius:2px;background:#FFFFFF;padding:0 12px}',
      P + ' details.nlc__det>summary{min-height:44px!important;display:flex!important;align-items:center;font:500 15px/22px ' + SANS + '!important;color:#2F6F86!important;cursor:pointer;border:0!important;padding:0!important;background:none!important;list-style:none}',
      P + ' details.nlc__det>summary::-webkit-details-marker{display:none}' + P + ' details.nlc__det>summary::before{content:"+";font:500 18px/1 ' + MONO + ';margin-inline-end:8px;color:#2F6F86}' + P + ' details.nlc__det[open]>summary::before{content:"−"}',
      P + ' .nlc__detb{display:grid;gap:12px;padding:0 0 12px}',
      P + ' .nlc__out{display:grid;gap:16px;align-content:start;min-width:0}',
      P + ' .nlc__score{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}',
      P + ' .nlc__sc{border:1px solid #D3DCE2;border-top:4px solid var(--c);border-radius:2px;background:#FFFFFF;padding:10px 12px;display:grid;gap:2px;min-width:0}',
      P + ' .nlc__sc b{font:500 32px/36px ' + MONO + ';color:#12202A}' + P + ' .nlc__sc span{font:500 13px/18px ' + SANS + ';color:#3E4C58}',
      P + ' .nlc__al{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}',
      P + ' .nlc__alab{font:600 16px/22px ' + SANS + ';color:#12202A}',
      P + ' .nlc__eg{font:500 12px/16px ' + SANS + ';color:#5E6A75;border:1px solid #D3DCE2;border-radius:999px;padding:2px 10px;white-space:nowrap}',
      P + ' p.nlc__valid{margin:0!important;padding:10px 12px!important;border:1px solid #D3DCE2;border-inline-start:4px solid var(--c);background:#FFFFFF;font:500 15px/22px ' + SANS + '!important;color:#12202A!important}',
      P + ' p.nlc__valid.is-red bdi.m{text-decoration:underline;text-decoration-color:#C42550;text-decoration-thickness:2px;text-underline-offset:5px}',
      P + ' .nlc__sumw{display:grid;gap:6px}',
      P + ' h3.nlc__h{font:600 18px/24px ' + SANS + '!important;color:#12202A!important;margin:0!important;letter-spacing:0!important;text-transform:none!important;border:0!important;padding:0!important}',
      P + ' h3.nlc__h::before,' + P + ' h3.nlc__h::after,' + P + ' h4.nlc__gh::before,' + P + ' h4.nlc__gh::after{display:none!important;content:none!important}',
      P + ' p.nlc__sum{font:400 15px/25px ' + SANS + '!important;color:#12202A!important;margin:0!important;padding:12px 14px!important;background:#F6F8F9;border-inline-start:3px solid #12202A}',
      P + ' .nlc__grp{display:grid;gap:8px}',
      P + ' h4.nlc__gh{font:600 16px/22px ' + SANS + '!important;color:#12202A!important;margin:0!important;display:flex!important;align-items:center;gap:8px;letter-spacing:0!important;text-transform:none!important;border:0!important;padding:0!important}',
      P + ' h4.nlc__gh i{width:12px;height:12px;border-radius:2px;background:var(--c);display:inline-block;flex:none}',
      P + ' ul.nlc__fls{list-style:none!important;margin:0!important;padding:0!important;display:grid;gap:8px}',
      P + ' li.nlc__fl{margin:0!important;padding:10px 12px!important;border:1px solid #D3DCE2;border-inline-start:4px solid var(--c);border-radius:2px;background:#FFFFFF;display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 10px;list-style:none!important}',
      P + ' li.nlc__fl::before,' + P + ' li.nlc__fl::marker{display:none!important;content:none!important}',
      P + ' .nlc__n{font:500 12px/18px ' + MONO + ';color:#5E6A75;border:1px solid #D3DCE2;border-radius:2px;padding:0 5px;align-self:start;min-width:26px;text-align:center}',
      P + ' li.nlc__fl p{margin:0!important;font:400 14px/22px ' + SANS + '!important;color:#3E4C58!important}',
      P + ' li.nlc__fl p b{color:#12202A;font-weight:600}',
      P + ' li.nlc__fl.is-red p b{text-decoration:underline;text-decoration-color:#C42550;text-decoration-thickness:2px;text-underline-offset:4px}',
      P + ' li.nlc__fl .r{color:#5E6A75}',
      P + ' li.nlc__fl small{display:block;font:400 12px/18px ' + SANS + '!important;color:#5E6A75!important;margin-top:4px}',
      P + ' li.nlc__fl a,' + P + ' .nlc__na a,' + P + ' p.nlc__method a{color:#2F6F86!important;text-decoration:underline!important;text-underline-offset:2px}',
      P + ' bdi.m{font-family:' + MONO + ';font-variant-numeric:tabular-nums;direction:ltr;unicode-bidi:isolate;white-space:nowrap}',
      P + ' ol.nlc__qs{margin:0!important;padding:0 22px 0 0!important;display:grid;gap:8px;list-style:decimal!important}',
      P + ' ol.nlc__qs li{font:400 15px/23px ' + SANS + '!important;color:#12202A!important;margin:0!important;padding:0!important}',
      P + ' ol.nlc__qs li::before{display:none!important;content:none!important}',
      P + ' .nlc__qw{display:grid;gap:10px;padding:12px 14px;border:1px solid #D3DCE2;border-radius:2px;background:#FFFFFF}',
      P + ' ul.nlc__na{list-style:none!important;margin:0!important;padding:0!important;display:grid;gap:6px}',
      P + ' ul.nlc__na li{font:400 14px/21px ' + SANS + '!important;color:#3E4C58!important;margin:0!important;padding:0!important}' + P + ' ul.nlc__na li::before{display:none!important;content:none!important}',
      P + ' ul.nlc__guide{margin:0!important;padding:0 20px 0 0!important;display:grid;gap:6px}' + P + ' ul.nlc__guide li{font:400 15px/23px ' + SANS + '!important;color:#12202A!important;margin:0!important}',
      P + ' .nlc__empty{display:grid;gap:12px;padding:16px;border:1px solid #D3DCE2;border-inline-start:4px solid #2F6F86;border-radius:2px;background:#F6F8F9}',
      P + ' .nlc__empty p{margin:0!important;font:400 15px/24px ' + SANS + '!important;color:#12202A!important}',
      P + ' a.nlc__go{display:flex!important;align-items:center;justify-content:center;min-height:48px;padding:10px 20px;border-radius:2px;border:1px solid #2F6F86;background:#FFFFFF;color:#2F6F86!important;font:600 15px/22px ' + SANS + '!important;text-decoration:none!important;max-width:420px;text-align:center}',
      P + ' p.nlc__method{font:400 13px/20px ' + SANS + '!important;color:#5E6A75!important;margin:12px 0 0!important;max-width:96ch}',
      P + ' .nlc__secs .mrx__sec{margin-top:20px}',
      '@media (max-width:420px){' + P + ' .nlc__tabs button{font-size:13px!important}' + P + ' .nlc__sc b{font-size:26px;line-height:30px}' + P + ' .nlc__g2{gap:8px}}',
      '@media print{' + P + ' .nlc__top,' + P + ' .nli__form,' + P + ' .nlc__qw button,' + P + ' a.nlc__go{display:none!important}' + P + ' details.nlc__det>summary::before{content:none}}'
    ];
    var s = document.createElement('style'); s.id = sid; s.textContent = r.join('\n'); document.head.appendChild(s);
  }

  function rich(s, esc) {  // a sentence in the text face, every number (and its ₪ or %) in the mono face
    s = String(s == null ? '' : s); var out = '', last = 0, re = /\d[\d,]*(?:[.\/]\d+)*(?:\s?₪|%)?/g, m;
    while ((m = re.exec(s))) { out += esc(s.slice(last, m.index)) + '<bdi class="m">' + esc(m[0]) + '</bdi>'; last = re.lastIndex; }
    return out + esc(s.slice(last));
  }

  G.NadLanInstruments.register('mcheck', {
    custom: function (root, data) {
      var tries = 0;
      (function wait() {
        if (G.NLMG && G.NLMR && G.NLMR.ui && ((G.NLMO && G.NLMQ) || tries > 40)) return G.NLMR.ui.start(root, data, build);
        if (++tries > 120) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
        setTimeout(wait, 50);
      })();
    }
  });

  function build(root, X) {
    var U = G.NLMR.ui, esc = U.esc, el = U.el, D = X.D, XR = { rt: X.rate, cpi: X.cpi };
    if (!D.by_bank || !D.by_bank.latest || !D.rules || !D.baskets || !D.fees || !D.term || !D.forecast) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
    var pid = document.getElementById(PID) ? PID + Math.random().toString(36).slice(2, 6) : PID;
    css(pid);
    var today = todayISO(), st = blank(), isEg = false, last = null, fx = {}, t = 0;
    var hh = U.fromHash('mcheck'); if (hh) st = restore(hh);
    var sys = bankRefOf(D, 'system'), MONTH = D.by_bank.latest.month, R = D.rules;
    var P = U.panel(root, {
      kicker: 'לפני חתימה · אישור עקרוני',
      title: 'בדיקת משכנתא לפני חתימה',
      lede: 'מעתיקים את האישור העקרוני שורה אחרי שורה, כמו בפורמט האחיד של בנק ישראל: הסל המוצע ושלושת הסלים האחידים. הבדיקה מריצה 28 בדיקות: התוקף, המגבלות של בנק ישראל, הריבית מול הממוצע של אותו בנק, עמלות, ערבים, ביטוח, שמאות ועמלת פירעון מוקדם, ומסכמת מה לשאול את הבנק. במצב השני משווים את המסמכים הסופיים לאישור. שום נתון לא נשלח לשרת.',
      strip: [['ריבית כוללת חזויה, כל הבנקים, ' + monthHe(MONTH), sys ? pc(sys.irr) : ''], ['תוקף אישור עקרוני (הוראה 451)', R451.hold + ' ימים לפחות'], ['החזר מההכנסה הפנויה (הוראה 329)', 'עד ' + pc(100 * R.pti_max, 0)], ['מימון בדירה יחידה', 'עד ' + pc(100 * R.ltv.single, 0)]],
      eg: 'כפתור הדוגמה ממלא אישור עקרוני על 1,200,000 ₪ לדירה של 1,600,000 ₪ ל־25 שנה, בתמהיל ובריביות הממוצעים של כל הבנקים ב־' + monthHe(MONTH) + ' לפי בנק ישראל. ההחזרים בדוגמה חושבו לפי תחזית חטיבת המחקר, הריבית הכוללת החזויה בסל המוצע היא הממוצע שבנק ישראל פרסם, ושורה 11 נשארה ריקה כי אין לה נתון רשמי. זו דוגמה, לא הצעה של בנק. מה שמקלידים נשאר בדף ובקישור שאתם יוצרים.'
    });
    P.panel.id = pid; P.panel.classList.add('nlc');
    P.out.classList.add('nlc__out'); P.secs.classList.add('nlc__secs');

    /* --------------------------------------------------------------------------------------------------- the top */
    function buildTop() {
      P.top.innerHTML = ''; P.top.className = 'nlc__top';
      P.top.appendChild(U.seg('מה בודקים', [['ap', 'האישור העקרוני'], ['fin', 'המסמכים לפני החתימה']], st.mode, function (k) { if (k === st.mode) return; st.mode = k; buildForm(); run(); }));
      var bx = el('div', 'nlc__btns');
      var be = el('button', 'nlc__b is-main', 'מילוי דוגמה, ממוצעי ' + esc(monthHe(MONTH))); be.type = 'button';
      be.addEventListener('click', function () { var m = st.mode; st = example(D, today); st.mode = m; if (m === 'fin') copyOffer(); isEg = true; buildTop(); buildForm(); run(); });
      var bc = el('button', 'nlc__b is-quiet', 'ניקוי הטופס'); bc.type = 'button';
      bc.addEventListener('click', function () { var m = st.mode; st = blank(); st.mode = m; isEg = false; buildTop(); buildForm(); run(); });
      bx.appendChild(be); bx.appendChild(bc); P.top.appendChild(bx);
    }
    function touch() { if (isEg) { isEg = false; } clearTimeout(t); t = setTimeout(run, 120); }
    function reg(path, w) { fx[path] = w; return w; }
    function fset(title, help) { var f = el('fieldset', 'nlc__fs'); f.appendChild(el('legend', '', esc(title))); if (help) f.appendChild(el('p', 'nlc__fh', esc(help))); return f; }
    function grid2() { return el('div', 'nlc__g2'); }
    function nfield(path, label, val, unit, set, o) { o = o || {}; return reg(path, U.field(label, val, unit, function (n) { set(fin(n) ? n : null); touch(); }, o)); }
    function tfield(path, label, val, set, o) { o = o || {}; o.type = 'text'; return reg(path, U.field(label, val, null, function (s) { set(String(s || '').trim()); touch(); }, o)); }
    function aria(w, s) { w._inp.setAttribute('aria-label', s); return w; }

    /* --------------------------------------------------------------------------------------------------- the form */
    function buildForm() {
      P.form.innerHTML = ''; fx = {};
      if (st.mode === 'fin') return buildFin();
      var h = st.h;
      var f1 = fset('פרטי האישור', 'מהחלק העליון של האישור העקרוני. בלי שם ובלי תעודת זהות.');
      f1.appendChild(U.select('הבנק', [['', 'בחרו בנק']].concat(BANKS.map(function (k) { return [k, BANK_HE[k]]; })).concat([['other', 'בנק אחר']]), h.bank, function (v) { h.bank = v; touch(); }));
      f1.appendChild(tfield('h.date', 'תאריך האישור', h.date, function (s) { h.date = s; }, { ph: '2.11.2026', help: 'יום, חודש ושנה, כמו באישור.' }));
      var g = grid2(); g.appendChild(nfield('h.loan', 'סך ההלוואה המבוקשת', h.loan, '₪', function (n) { h.loan = n; }, { money: true })); g.appendChild(nfield('h.price', 'מחיר הדירה', h.price, '₪', function (n) { h.price = n; }, { money: true })); f1.appendChild(g);
      f1.appendChild(U.select('סוג הרכישה', BUYER, h.buyer, function (v) { h.buyer = v; touch(); }));
      f1.appendChild(U.seg('הדירה', [['used', 'יד שנייה'], ['new', 'חדשה מקבלן']], h.newb, function (v) { h.newb = v; buildForm(); touch(); }));
      if (h.newb === 'new') f1.appendChild(tfield('h.delivery', 'מועד המסירה בחוזה', h.delivery, function (s) { h.delivery = s; }, { ph: '6.2028', help: 'חודש ושנה.' }));
      f1.appendChild(U.seg('האם נדרשים ערבים להלוואה', [['no', 'לא'], ['yes', 'כן']], h.guar, function (v) { h.guar = v; touch(); }));
      P.form.appendChild(f1);

      var f2 = fset('ארבעת הסלים', 'כל אישור עקרוני מציג את הסל שהבנק מציע ושלושה סלים אחידים. בחרו סל והקלידו את שורת הסה״כ שלו.');
      var tabs = el('div', 'nlc__tabs'); tabs.setAttribute('role', 'tablist'); tabs.setAttribute('aria-label', 'הסלים באישור');
      var pane = el('div', 'nlc__pane'); pane.id = pid + '-pane'; pane.setAttribute('role', 'tabpanel');
      BK.forEach(function (k, i) {
        var b = el('button', bmodel(st, k).any ? 'has' : '', esc(BTAB[k])); b.type = 'button'; b.setAttribute('role', 'tab'); b.id = pid + '-tab-' + k;
        b.setAttribute('aria-selected', String(st.tab === k)); b.setAttribute('aria-controls', pane.id); b.tabIndex = st.tab === k ? 0 : -1;
        b.addEventListener('click', function () { st.tab = k; [].forEach.call(tabs.children, function (x) { var on = x === b; x.setAttribute('aria-selected', String(on)); x.tabIndex = on ? 0 : -1; }); drawBasket(pane); });
        b.addEventListener('keydown', function (e) { var d = e.key === 'ArrowLeft' ? 1 : e.key === 'ArrowRight' ? -1 : 0; if (!d) return; e.preventDefault(); var j = (i + d + BK.length) % BK.length; tabs.children[j].click(); tabs.children[j].focus(); });
        tabs.appendChild(b);
      });
      f2.appendChild(tabs); f2.appendChild(pane);
      pane.setAttribute('aria-labelledby', pid + '-tab-' + st.tab);
      drawBasket(pane);
      var tog = el('button', 'nlc__tog', st.full ? 'רק שורת הסה״כ של כל סל' : 'כל השורות: המסלולים של כל סל (שורות 1 עד 6 ו־12)'); tog.type = 'button'; tog.setAttribute('aria-expanded', String(st.full));
      tog.addEventListener('click', function () { st.full = !st.full; buildForm(); run(); var b2 = P.form.querySelector('.nlc__tog'); if (b2) b2.focus(); });
      f2.appendChild(tog);
      if (st.full) {
        f2.appendChild(U.seg('האם בחיובים מופיעים דמי שריון או תשלום על אופציה לקבלת הלוואה', [['no', 'לא'], ['yes', 'כן']], h.resv, function (v) { h.resv = v; touch(); }));
        f2.appendChild(U.seg('האם נרשם שעבוד חדש על הדירה', [['yes', 'כן'], ['no', 'לא']], h.lien, function (v) { h.lien = v; touch(); }));
      }
      P.form.appendChild(f2);

      var c = st.c, f3 = fset('הנתונים שלכם', 'לא חובה. נשארים בדף ולא נשלחים לשום מקום.');
      var g3 = grid2();
      g3.appendChild(nfield('c.income', 'הכנסה פנויה של משק הבית, נטו', c.income, '₪', function (n) { c.income = n; }, { money: true }));
      g3.appendChild(nfield('c.loans', 'החזרים על הלוואות אחרות', c.loans, '₪', function (n) { c.loans = n; }, { money: true }));
      g3.appendChild(nfield('c.equity', 'הון עצמי', c.equity, '₪', function (n) { c.equity = n; }, { money: true }));
      g3.appendChild(nfield('c.hz', 'בעוד כמה שנים צפויה יציאה', c.hz, 'שנים', function (n) { c.hz = n; }, { help: 'מכירה, שדרוג או מחזור.' }));
      f3.appendChild(g3);
      f3.appendChild(U.seg('זכאות משרד הבינוי והשיכון', [['yes', 'יש'], ['no', 'אין'], ['unk', 'לא נבדק']], c.elig, function (v) { c.elig = v; touch(); }));
      var g4 = grid2();
      g4.appendChild(nfield('c.life', 'הצעה לביטוח חיים, בחודש', c.life, '₪', function (n) { c.life = n; }, { money: true }));
      g4.appendChild(nfield('c.struct', 'הצעה לביטוח מבנה, בחודש', c.struct, '₪', function (n) { c.struct = n; }, { money: true }));
      var ar = nfield('c.arn', 'ארנונה וועד בית, בחודש', c.arn, '₪', function (n) { c.arn = n; }, { money: true }); ar.classList.add('nlc__wide'); g4.appendChild(ar);
      f3.appendChild(g4);
      P.form.appendChild(f3);
      P.form.appendChild(othersBox());
      paintErr();
    }
    function drawBasket(pane) {
      pane.innerHTML = '';
      var k = st.tab, b = st.b[k], p = 'b.' + k + '.';
      pane.setAttribute('aria-labelledby', pid + '-tab-' + k);
      Object.keys(fx).forEach(function (x) { if (x.indexOf('b.') === 0) delete fx[x]; });
      pane.appendChild(el('p', 'nlc__def', k === 'offer' ? 'הסל שהבנק בנה לכם: המסלולים, הסכומים והריביות שהוא מציע.' : esc(BNAME[k] + ': ' + defText(D, k) + ', בלוח שפיצר.')));
      var g = grid2();
      g.appendChild(nfield(p + 'term', 'תקופה (שורה 3)', b.term, 'חודשים', function (n) { b.term = n; }));
      g.appendChild(nfield(p + 'irr', 'ריבית כוללת חזויה (שורה 7)', b.irr, '%', function (n) { b.irr = n; }, { dec: 2 }));
      g.appendChild(nfield(p + 'first', 'החזר חודשי ראשון (שורה 8)', b.first, '₪', function (n) { b.first = n; }, { money: true }));
      g.appendChild(nfield(p + 'max', 'ההחזר הגבוה הצפוי (שורה 9)', b.max, '₪', function (n) { b.max = n; }, { money: true }));
      g.appendChild(nfield(p + 'maxM', 'החודש של ההחזר הגבוה', b.maxM, null, function (n) { b.maxM = n; }));
      g.appendChild(nfield(p + 'total', 'סך הכול עד סוף התקופה (שורה 10)', b.total, '₪', function (n) { b.total = n; }, { money: true }));
      var fe = nfield(p + 'fees', 'חיובים ועמלות, כולל לצד ג׳ (שורה 11)', b.fees, '₪', function (n) { b.fees = n; }, { money: true }); fe.classList.add('nlc__wide'); g.appendChild(fe);
      pane.appendChild(g);
      if (st.full) pane.appendChild(tracksBox(b.tracks, k, p + 't.', function () { drawBasket(pane); }));
      paintErr();
    }
    function tracksBox(list, k, path, redraw) {
      var box = el('div', 'nlc__trs'), withMethod = k === 'offer' || k === 'fin';
      box.appendChild(el('p', 'nlc__fh', esc(k === 'fin' ? 'המסלולים כמו במסמכים.' : 'המסלולים כמו באישור: שם, סכום, תקופה' + (withMethod ? ', אופן התשלום' : '') + ', ריבית, ובמשתנה גם העוגן והמרווח. בפריים, ריבית מתחת לפריים היא מרווח במינוס, למשל מינוס 0.6.')));
      if (k !== 'offer' && k !== 'fin') {
        var fb = el('button', 'nlc__b is-quiet', 'מילוי המסלולים לפי ההגדרה של ' + esc(BNAME[k])); fb.type = 'button';
        fb.addEventListener('click', function () {
          var rateOf = function (kk) { var x = st.b.offer.tracks.filter(function (q) { return q.k === kk && fin(q.rate); })[0]; return x ? x.rate : null; };
          var nl = fillDef(D, k, st.h.loan, st.b[k].term || 300, rateOf); list.splice.apply(list, [0, list.length].concat(nl)); redraw(); touch();
        });
        box.appendChild(fb);
      }
      list.forEach(function (tr, i) {
        var c = el('div', 'nlc__tr'), q = path + i + '.', nm = 'מסלול ' + (i + 1);
        var hd = el('div', 'nlc__trh', '<span>' + esc(nm) + '</span>');
        var x = el('button', 'nlc__x', '×'); x.type = 'button'; x.setAttribute('aria-label', 'הסרת ' + nm);
        x.addEventListener('click', function () { list.splice(i, 1); redraw(); touch(); });
        hd.appendChild(x); c.appendChild(hd);
        var sel = U.select('שם ההלוואה (שורה 1)', TRK.map(function (z) { return [z, TNAME[z]]; }), tr.k, function (v) { tr.k = v; if (TK[v].kind === 'var' && !fin(tr.freq)) tr.freq = 60; redraw(); touch(); });
        sel.querySelector('select').setAttribute('aria-label', nm + ': שם ההלוואה (שורה 1)'); c.appendChild(sel);
        var g = grid2();
        g.appendChild(aria(nfield(q + 'amount', 'סכום (שורה 2)', tr.amount, '₪', function (n) { tr.amount = n; }, { money: true }), nm + ': סכום (שורה 2)'));
        g.appendChild(aria(nfield(q + 'months', 'תקופה (שורה 3)', tr.months, 'חודשים', function (n) { tr.months = n; }), nm + ': תקופה בחודשים (שורה 3)'));
        if (withMethod) {
          var ms = U.select('אופן התשלום (שורה 4)', METHOD, tr.method, function (v) { tr.method = v; touch(); }); ms.querySelector('select').setAttribute('aria-label', nm + ': אופן התשלום (שורה 4)'); g.appendChild(ms);
          g.appendChild(aria(nfield(q + 'grace', 'גרייס', tr.grace, 'חודשים', function (n) { tr.grace = n; }), nm + ': חודשי גרייס'));
          if (fin(tr.grace) && tr.grace > 0) { var gs = U.select('סוג הגרייס', [['partial', 'חלקי: משלמים ריבית'], ['full', 'מלא: לא משלמים']], tr.graceType, function (v) { tr.graceType = v; touch(); }); gs.querySelector('select').setAttribute('aria-label', nm + ': סוג הגרייס'); gs.classList.add('nlc__wide'); g.appendChild(gs); }
        }
        g.appendChild(aria(nfield(q + 'rate', 'ריבית שנתית (שורה 5)', tr.rate, '%', function (n) { tr.rate = n; }, { dec: 2 }), nm + ': ריבית שנתית (שורה 5)'));
        if (TK[tr.k].variable) {
          g.appendChild(aria(nfield(q + 'margin', 'מרווח (שורה 6)', tr.margin, '%', function (n) { tr.margin = n; }, { dec: 2 }), nm + (tr.k === 'prime' ? ': המרווח מהפריים (שורה 6)' : ': המרווח (שורה 6)')));
          if (tr.k !== 'prime') {
            var an = U.select('העוגן (שורה 6)', ANCHOR, tr.anchor, function (v) { tr.anchor = v; touch(); }); an.querySelector('select').setAttribute('aria-label', nm + ': העוגן (שורה 6)'); an.classList.add('nlc__wide'); g.appendChild(an);
            var fq = U.select('תדירות השינוי', FREQ.map(function (z) { return [String(z[0]), z[1]]; }), String(fin(tr.freq) ? tr.freq : 60), function (v) { tr.freq = +v; touch(); }); fq.querySelector('select').setAttribute('aria-label', nm + ': תדירות שינוי הריבית'); fq.classList.add('nlc__wide'); g.appendChild(fq);
          }
        }
        c.appendChild(g);
        var pp = U.seg('עמלת פירעון בגין הפרשי ריבית (שורה 12)', [['yes', 'יש'], ['no', 'אין']], tr.pp, function (v) { tr.pp = v; touch(); });
        pp._g.setAttribute('aria-label', nm + ': עמלת פירעון בגין הפרשי ריבית (שורה 12)'); c.appendChild(pp);
        box.appendChild(c);
      });
      if (list.length < 8) {
        var ad = el('button', 'nlc__b is-quiet', '+ מסלול'); ad.type = 'button'; ad.setAttribute('aria-label', 'הוספת מסלול');
        ad.addEventListener('click', function () { var prev = list[list.length - 1]; list.push(blankTrack('fixed_nl', { months: prev && fin(prev.months) ? prev.months : (fin(st.b[k] && st.b[k].term) ? st.b[k].term : null) })); redraw(); touch(); });
        box.appendChild(ad);
      }
      return box;
    }
    function othersBox() {
      var d = el('details', 'nlc__det'); d.open = st.o.length > 0;
      d.appendChild(el('summary', '', 'אישורים מבנקים אחרים (לא חובה)'));
      var b = el('div', 'nlc__detb'); d.appendChild(b);
      b.appendChild(el('p', 'nlc__fh', 'שורת הסה״כ של הסלים האחידים מאישור של בנק אחר, להשוואה של אותו סל. עד שני אישורים.'));
      st.o.forEach(function (o, i) {
        var f = fset('אישור נוסף ' + (i + 1));
        f.appendChild(U.select('הבנק', [['', 'בחרו בנק']].concat(BANKS.map(function (k) { return [k, BANK_HE[k]]; })).concat([['other', 'בנק אחר']]), o.bank, function (v) { o.bank = v; touch(); }));
        f.appendChild(aria(nfield('o.' + i + '.loan', 'סך ההלוואה באישור', o.loan, '₪', function (n) { o.loan = n; }, { money: true }), 'אישור נוסף ' + (i + 1) + ': סך ההלוואה'));
        ['b1', 'b2', 'b3'].forEach(function (k) {
          var x = o.b[k], g = grid2(), pre = 'אישור נוסף ' + (i + 1) + ', ' + BNAME[k] + ': ';
          var hd = el('p', 'nlc__fh', '<b>' + esc(BNAME[k]) + '</b>'); hd.classList.add('nlc__wide'); g.appendChild(hd);
          g.appendChild(aria(nfield('o.' + i + '.' + k + '.term', 'תקופה', x.term, 'חודשים', function (n) { x.term = n; }), pre + 'תקופה בחודשים'));
          g.appendChild(aria(nfield('o.' + i + '.' + k + '.irr', 'ריבית כוללת חזויה', x.irr, '%', function (n) { x.irr = n; }, { dec: 2 }), pre + 'ריבית כוללת חזויה'));
          g.appendChild(aria(nfield('o.' + i + '.' + k + '.total', 'סך הכול', x.total, '₪', function (n) { x.total = n; }, { money: true }), pre + 'סך הכול עד סוף התקופה'));
          g.appendChild(aria(nfield('o.' + i + '.' + k + '.max', 'ההחזר הגבוה', x.max, '₪', function (n) { x.max = n; }, { money: true }), pre + 'ההחזר הגבוה הצפוי'));
          g.appendChild(aria(nfield('o.' + i + '.' + k + '.first', 'החזר ראשון', x.first, '₪', function (n) { x.first = n; }, { money: true }), pre + 'החזר ראשון'));
          g.appendChild(aria(nfield('o.' + i + '.' + k + '.fees', 'חיובים ועמלות', x.fees, '₪', function (n) { x.fees = n; }, { money: true }), pre + 'חיובים ועמלות'));
          f.appendChild(g);
        });
        var rm = el('button', 'nlc__b is-quiet', 'הסרת האישור הנוסף ' + (i + 1)); rm.type = 'button';
        rm.addEventListener('click', function () { st.o.splice(i, 1); buildForm(); touch(); });
        f.appendChild(rm); b.appendChild(f);
      });
      if (st.o.length < 2) {
        var ad = el('button', 'nlc__b is-quiet', '+ אישור מבנק אחר'); ad.type = 'button';
        ad.addEventListener('click', function () { st.o.push(blankOther()); buildForm(); var dd = P.form.querySelector('details.nlc__det'); if (dd) dd.open = true; touch(); });
        b.appendChild(ad);
      }
      return d;
    }
    function copyOffer() { var o = st.b.offer; st.f.tracks = clone(o.tracks); st.f.loan = st.h.loan; st.f.fees = o.fees; st.f.guar = st.h.guar; st.f.ins = st.f.ins || 'no'; }
    function buildFin() {
      var f = st.f, f1 = fset('המסמכים הסופיים', 'מהמסמכים שהבנק נתן לחתימה, על הסל שאתם חותמים עליו. ההשוואה היא מול הסל המוצע באישור העקרוני.');
      var cp = el('button', 'nlc__b', 'העתקה מהסל המוצע באישור, ואז לתקן מה ששונה'); cp.type = 'button';
      cp.addEventListener('click', function () { copyOffer(); buildForm(); touch(); });
      f1.appendChild(cp);
      f1.appendChild(tfield('f.date', 'תאריך המסמכים', f.date, function (s) { f.date = s; }, { ph: '20.11.2026' }));
      var g = grid2();
      g.appendChild(nfield('f.loan', 'סך ההלוואה במסמכים', f.loan, '₪', function (n) { f.loan = n; }, { money: true }));
      g.appendChild(nfield('f.fees', 'חיובים ועמלות במסמכים', f.fees, '₪', function (n) { f.fees = n; }, { money: true }));
      f1.appendChild(g);
      f1.appendChild(U.seg('האם נדרשים ערבים', [['no', 'לא'], ['yes', 'כן']], f.guar, function (v) { f.guar = v; touch(); }));
      f1.appendChild(U.seg('דרישת ביטוח שלא הופיעה באישור', [['no', 'אין'], ['yes', 'יש']], f.ins, function (v) { f.ins = v; touch(); }));
      P.form.appendChild(f1);
      var f2 = fset('המסלולים במסמכים');
      f2.appendChild(tracksBox(f.tracks, 'fin', 'f.t.', function () { buildForm(); }));
      P.form.appendChild(f2);
      if (!tracksOk(st.b.offer.tracks).length && !fin(st.h.loan)) P.form.appendChild(el('p', 'nli__note', 'כדי להשוות צריך את הסל המוצע באישור. עברו ל״האישור העקרוני״, פתחו את כל השורות והקלידו את המסלולים, או מלאו דוגמה.'));
      paintErr();
    }
    function paintErr() { var e = last ? last.err : NLMC.validate(st); Object.keys(fx).forEach(function (k) { if (fx[k] && fx[k]._err) fx[k]._err.textContent = e[k] || ''; }); }

    /* ---------------------------------------------------------------------------------------------------- the result */
    function run() {
      try { last = NLMC.run(st, D, XR, today); } catch (e) { P.out.innerHTML = '<p class="nli__note">לא הצלחנו לבדוק עם הערכים האלה.</p>'; return; }
      paintErr(); paint(last); paintSecs(last); paintShare(last);
      [].forEach.call(P.form.querySelectorAll('.nlc__tabs button[role="tab"]'), function (b, i) { b.classList.toggle('has', bmodel(st, BK[i]).any); });
    }
    function srcHtml(f) {
      var s = f.src.map(function (x) { return x.url ? '<a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.label) + '</a>' : esc(x.label); }).join(' · ');
      return s + (f.page ? (s ? ' · ' : '') + 'אצלנו: <a href="' + esc(f.page.href) + '">' + esc(f.page.label) + '</a>' : '');
    }
    function flagLi(f) {
      var li = el('li', 'nlc__fl is-' + f.level);
      li.innerHTML = '<span class="nlc__n" aria-label="בדיקה ' + f.id + '">' + f.id + '</span><p><b>' + esc(f.title) + '.</b> ' + rich(f.you, esc) + (f.rule ? ' <span class="r">' + rich(f.rule, esc) + '</span>' : '') + (f.src.length || f.page ? '<small>' + srcHtml(f) + '</small>' : '') + '</p>';
      return li;
    }
    function paint(res) {
      var o = P.out; o.innerHTML = '';
      if (res.empty) {
        var e = el('div', 'nlc__empty');
        e.appendChild(el('p', '', st.mode === 'fin' ? 'הקלידו את המסמכים הסופיים, או העתיקו מהסל המוצע ותקנו מה ששונה. כל שינוי מול האישור יופיע כאן.' : 'הקלידו את האישור העקרוני, או מלאו דוגמה. הבדיקה מתעדכנת אחרי כל שדה.'));
        if (st.mode !== 'fin') e.appendChild(el('ul', 'nlc__guide', ['תוקף האישור: ' + R451.hold + ' ימים לפי הוראה 451', 'ארבעת הסלים והשורות של כל סל', 'המגבלות של בנק ישראל: מימון, החזר מההכנסה, ריבית משתנה ותקופה', 'הריבית מול הממוצע של אותו בנק ומול הממוצע בכל מסלול', 'חיובים ועמלות, ערבים, ביטוח, שמאות ועמלת פירעון מוקדם', 'מה לשאול את הבנק, ובמצב השני: המסמכים הסופיים מול האישור'].map(function (x) { return '<li>' + rich(x, esc) + '</li>'; }).join('')));
        o.appendChild(e); return;
      }
      var hd = el('div', 'nlc__al', '<span class="nlc__alab">מה נמצא בבדיקה</span>' + (isEg ? '<span class="nlc__eg">דוגמה, שנו כל שדה</span>' : ''));
      o.appendChild(hd);
      var sc = el('div', 'nlc__score'); sc.setAttribute('role', 'group'); sc.setAttribute('aria-label', 'מספר הדגלים');
      ['red', 'amber', 'info'].forEach(function (lv) { sc.appendChild(el('div', 'nlc__sc is-' + lv, '<b>' + res.counts[lv] + '</b><span>' + esc(GSHORT[lv]) + '</span>')); });
      o.appendChild(sc);
      if (res.valid) {
        var v = res.valid, lv = v.left < 0 ? 'red' : v.left < 5 ? 'amber' : 'info';
        o.appendChild(el('p', 'nlc__valid is-' + lv, rich(v.left < 0 ? 'תוקף האישור עבר ב־' + dateHe(v.exp) + ', לפני ' + (-v.left) + ' ימים.' : v.left === 0 ? 'היום היום האחרון לתוקף האישור, ' + dateHe(v.exp) + '.' : 'תוקף האישור: נשארו ' + v.left + ' ימים, עד ' + dateHe(v.exp) + '.', esc)));
      }
      var sw = el('div', 'nlc__sumw'); sw.appendChild(el('h3', 'nlc__h', 'בקצרה')); sw.appendChild(el('p', 'nlc__sum', rich(res.sum.join(' '), esc))); o.appendChild(sw);
      ['red', 'amber', 'info'].forEach(function (lv) {
        var fs = res.flags.filter(function (f) { return f.level === lv; }); if (!fs.length) return;
        var ul = el('ul', 'nlc__fls'); fs.forEach(function (f) { ul.appendChild(flagLi(f)); });
        var gh = '<i aria-hidden="true"></i>' + esc(GROUP[lv]) + ' <bdi class="m">(' + fs.length + ')</bdi>';
        if (lv === 'info') {
          var d = el('details', 'nlc__det nlc__grp is-info'); d.open = !res.counts.red && !res.counts.amber;
          d.appendChild(el('summary', '', esc(GROUP[lv]) + ' (' + fs.length + ')')); var db = el('div', 'nlc__detb'); db.appendChild(ul); d.appendChild(db); o.appendChild(d);
        } else { var g = el('section', 'nlc__grp is-' + lv); g.appendChild(el('h4', 'nlc__gh', gh)); g.appendChild(ul); o.appendChild(g); }
      });
      if (res.qs.length) {
        var qw = el('section', 'nlc__qw'); qw.appendChild(el('h3', 'nlc__h', 'מה לשאול את הבנק'));
        qw.appendChild(el('ol', 'nlc__qs', res.qs.map(function (q) { return '<li>' + rich(q, esc) + '</li>'; }).join('')));
        var cq = el('button', 'nlc__b', 'העתקת השאלות'); cq.type = 'button';
        cq.addEventListener('click', function () { var tx = 'מה לשאול את הבנק:\n' + res.qs.map(function (q, i) { return (i + 1) + '. ' + q; }).join('\n'); var lab = cq.textContent; var done = function () { cq.textContent = 'הועתק'; setTimeout(function () { cq.textContent = lab; }, 1600); }; if (navigator.clipboard) navigator.clipboard.writeText(tx).then(done, function () { window.prompt('העתיקו', tx); }); else window.prompt('העתיקו', tx); });
        qw.appendChild(cq); o.appendChild(qw);
      }
      if (res.na.length) {
        var nd = el('details', 'nlc__det'); nd.appendChild(el('summary', '', 'לא ניתן לבדוק בלי נתונים נוספים (' + res.na.length + ')'));
        var nb = el('div', 'nlc__detb'); nb.appendChild(el('ul', 'nlc__na', res.na.map(function (x) { return '<li><b>' + esc(x.title) + '</b> <bdi class="m">(' + x.id + ')</bdi>: ' + esc(x.why) + '</li>'; }).join(''))); nd.appendChild(nb); o.appendChild(nd);
      }
      var adv = el('a', 'nlc__go', 'לשיחה עם יועץ משכנתאות על האישור'); adv.href = PG.adv.href; o.appendChild(adv);
    }
    function paintSecs(res) {
      var S = P.secs; S.innerHTML = '';
      if (res.empty) return;
      if (st.mode === 'fin') {
        if (res.diff && res.diff.length) { var s0 = U.sec(S, 'המסמכים מול האישור', 'כל שינוי שנמצא, לפי הסדר.'); s0.appendChild(U.table(['שינוי', 'מה נמצא'], res.diff.map(function (c) { return { cls: c.lvl === 'red' ? 'is-on' : '', cells: [esc(c.title), rich(c.you, esc)] }; }), { cards: true })); }
      } else {
        var M = res.M, RC = res.RC || {}, live = BK.filter(function (k) { return M[k].any; });
        if (live.length) {
          var s1 = U.sec(S, 'ארבעת הסלים זה לצד זה', 'השורות שהקלדתם, ומתחת לכל אחת החישוב שלנו כשיש מסלולים מלאים.');
          var cell = function (k, f, money) { var v = M[k].b[f], rc = RC[k], r = rc && f !== 'irr' && f !== 'term' && f !== 'fees' ? rc[f] : null, s = fin(v) ? esc(money ? ils(v) : f === 'irr' ? pc(v) : String(v)) : (fin(r) ? 'לא הוקלד' : ''); if (fin(r)) s += '<small>שלנו: ' + esc(money ? ils(r) : String(r)) + '</small>'; return s; };
          var rows = [['תקופה בחודשים (3)', 'term', false], ['ריבית כוללת חזויה (7)', 'irr', false], ['החזר ראשון (8)', 'first', true], ['ההחזר הגבוה (9)', 'max', true], ['בחודש (9)', 'maxM', false], ['סך הכול (10)', 'total', true], ['חיובים ועמלות (11)', 'fees', true]];
          s1.appendChild(U.table(['שורה'].concat(live.map(function (k) { return BTAB[k]; })), rows.map(function (r) { return { cells: [esc(r[0])].concat(live.map(function (k) { return cell(k, r[1], r[2]); })) }; }), { num: live.map(function (k, i) { return i + 1; }), cards: true }));
        }
        if (res.t10 && res.t10.rows.length) {
          var T = res.t10, s2 = U.sec(S, 'המסלולים בסל המוצע מול הממוצע של בנק ישראל', 'ריבית אפקטיבית שהומרה לריבית שנתית לתשלום חודשי, ' + monthHe(T.ref.month) + '. פער חיובי: יותר מהממוצע.');
          s2.appendChild(U.table(['מסלול', 'סכום', 'הריבית', T.own ? 'ממוצע ' + T.ref.name : 'ממוצע כל הבנקים', 'לפי תקופה', 'פער בחודש', 'לאורך המסלול'], T.rows.map(function (x) {
            var none = !fin(x.c.payGap) || Math.abs(x.c.payGap) < 0.5;  // a gap under half a shekel is said in words, never as "0 ₪"
            return { cells: [esc(TNAME[x.t.k]), esc(ils(x.t.amount)), esc(pc(x.t.rate)), esc(pc(x.c.nom)), x.tb ? esc(pc(x.tb.nom)) : '', none ? 'אין פער' : esc((x.c.payGap < 0 ? 'פחות ' : 'יותר ') + ils(Math.abs(x.c.payGap))), none ? 'אין פער' : esc(ils(Math.abs(x.c.totalGap)))] };
          }), { num: [1, 2, 3, 4, 5, 6], cards: true }));
        }
      }
      S.appendChild(el('p', 'nlc__method', esc('איך בודקים: כל בדיקה משווה מספר שהקלדתם לכלל של בנק ישראל או של צו הבנקאות, או לנתון רשמי עם התאריך שלו. ההחזרים מחושבים בלוח שפיצר (או בלוח שבחרתם) לפי תחזית חטיבת המחקר של בנק ישראל, והריבית האפקטיבית מומרת לשנתית לתשלום חודשי: (1 + ר)^(1/12) − 1. הבדיקה לא בוחרת בשבילכם בנק או תמהיל, והיא אינה ייעוץ. מקורות: ') + [src451(), src329(D), srcOrder(D), srcEq(D), srcFc(D)].map(function (x) { return '<a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.label) + '</a>'; }).join(' · ') + '.'));
    }
    function paintShare(res) {
      U.shareBar(P.share, function () { return NLMC.text(res, st, today); }, function () { var s = clone(st); return U.link('mcheck', s); });
    }
    window.addEventListener('beforeprint', function () { [].forEach.call(P.panel.querySelectorAll('details'), function (d) { d.open = true; }); });

    buildTop(); buildForm(); run();
  }
})();
