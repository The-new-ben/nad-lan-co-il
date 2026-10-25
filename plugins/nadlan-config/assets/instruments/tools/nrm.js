/* NadLan Instruments · nrm v2 (U3, 26.10.2026; v1 HAD-575, 21.10.2026): "Your Israeli borrowing limit by passport and paycheck",
   the Israel mortgage calculator for foreign buyers, Israelis abroad and olim, in English and Hebrew.
   Two rulebooks in one answer: the Bank of Israel sizes the loan by citizenship (Directive 329 s.1 and s.2: 75% single home, 70%
   replacement home, 50% investment home; a home a non-citizen buys is an investment home, BoI Q&A 2.4; mixed buyers weighted by
   share), the Tax Authority sizes the purchase tax by residency (ptax.json: foreign resident and additional home 8% / 10%, resident
   single home, oleh 12A). The income test runs in the buyer's own currency at the Bank of Israel representative rate (boi-fx.json):
   payment at most 50% of disposable income (s.5), about one third in practice. Track mixes from the Bank of Israel uniform baskets
   (Directive 451): one track, thirds, half fixed half prime, and a foreign currency loan for non-citizens (outside the two-thirds
   variable cap, s.12.3). Two modes: what can I borrow, and what can my cash buy (the highest price after tax and fees).
   Backward compatible: same id, the v1 fields (price, cur, ltv, years, track, rate, lawyer) keep their meaning, the default case
   is the v1 case (non-citizen, ₪4,000,000, 50%, 25 years, 4.62%) with the same loan, payment, tax and cash to close, and NLNR.compute
   keeps the v1 signature. The language follows the tool's own section (lang="en" or "he"), so the English tool on a Hebrew path
   stays English. Data: nrm.json (BoI averages, caps, baskets), ptax.json, boi-fx.json. Pure logic in NLNR (full) for the checks
   in tools/instruments/test_nrm_math.py. The drawing is LTR in English; in Hebrew it mirrors (direction rtl, start = right end). */
(function () {
  'use strict';
  var EPS = 1e-9;
  function pay(P, annual, months) { var r = annual / 100 / 12; return r === 0 ? P / months : P * r / (1 - Math.pow(1 + r, -months)); }
  function ptax(price, br) { var t = 0, lo = 0; for (var i = 0; i < br.length; i++) { var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(price, hi); if (top > lo) t += (top - lo) * br[i][1]; if (price <= hi) break; lo = hi; } return t; }
  /** v1 (21.10.2026), unchanged: the non-resident case only (used by tools/instruments/test_tools.js). */
  function compute(v, P, N) {
    var loan = v.price * Math.min(v.ltv, 100) / 100, n = Math.round(v.years * 12), m = pay(loan, v.rate, n);
    var tax = ptax(v.price, P.tracks.foreign), lawyer = v.price * (v.lawyer || 0) / 100 * (1 + N.vat);
    var fee = loan > 0 ? Math.min(loan * N.mortgage_fee.rate, N.mortgage_fee.max) : 0, appr = loan > 0 ? N.appraiser : 0;
    var cash = v.price - loan + tax + lawyer + fee + appr;
    return { loan: loan, n: n, monthly: m, interest: m * n - loan, tax: tax, lawyer: lawyer, fee: fee, appr: appr, cash: cash, over: v.ltv / 100 > N.ltv_max + 1e-9 };
  }

  /** The loan-to-value cap for a status (329 s.1, s.2; BoI Q&A: joint buyers of different status weighted by share). */
  function cap(status, share, N) {
    var L = N.ltv_by_status || {}, g = function (k, d) { return L[k] != null ? L[k] : d; };
    if (status === 'mixed') { var s = Math.min(Math.max(+share || 0, 0), 100) / 100; return s * g('cit_first', 0.75) + (1 - s) * g('foreign', N.ltv_max); }
    return g(status, N.ltv_max);
  }
  /** The purchase tax track: residency decides it, not citizenship. A non-citizen is taken as living abroad. */
  function taxTrack(status, live) {
    if (status === 'oleh') return 'oleh';
    if (status === 'foreign' || live !== 'israel') return 'foreign';
    return status === 'cit_own' ? 'extra' : 'single';
  }
  function primeRate(N, spread) { return (N.prime != null ? N.prime : 4.75) + (+spread || 0); }
  /** The parts of the mix: [{ k, w, rate, cpi, prime, variable, fx }]. */
  function parts(v, N) {
    var R = {}; (N.rates || []).forEach(function (r) { R[r.id] = r; });
    var pr = primeRate(N, v.spread);
    function t(id, w, rate) { var r = R[id] || {}; return { k: id, w: w, rate: rate, cpi: !!r.cpi, prime: !!r.prime, variable: !!r.variable || id === 'fx', fx: id === 'fx' }; }
    if (v.mix === 'fx') return [t('fx', 1, +v.rate)];
    var B = N.baskets && N.baskets[v.mix];
    if (B) return B.map(function (x) { var r = R[x[0]] || {}; return t(x[0], x[1], r.prime ? pr : r.rate); });
    return [t(R[v.track] ? v.track : N.rates[0].id, 1, +v.rate)];
  }
  /** Everything for one case. v: status, share, live, mode (borrow | cash), price (₪), cash (buyer's currency), cur, income and
      commit (monthly, buyer's currency), appr (% of price), ltv (% of value), years, mix (one | b2 | b3 | fx), track, rate, spread,
      cpi (% a year), lawyer (% before VAT). Missing fields take the v1 default case. */
  function full(v0, P, N, FX) {
    var D = { status: 'foreign', share: 50, live: 'abroad', mode: 'borrow', price: 4000000, cash: 0, cur: 'USD', income: 0, commit: 0, appr: 100, ltv: 50, years: 25,
      mix: 'one', track: N.rates[0].id, rate: N.rates[0].rate, spread: 0, cpi: N.cpi_forecast != null ? N.cpi_forecast : 2, lawyer: 0.5 }, v = {};
    Object.keys(D).forEach(function (k) { v[k] = v0[k] == null || v0[k] === '' ? D[k] : v0[k]; });
    var fxo = FX && FX.fx ? FX.fx : {}, cur = fxo[v.cur] ? v.cur : (fxo.USD ? 'USD' : Object.keys(fxo)[0]), f = fxo[cur] || { rate: 1 }, fxr = f.rate;
    var RU = N.rules || {}, pmax = RU.pti_max || 0.5, pthird = RU.pti_practice || 1 / 3, prisk = RU.pti_risk || 0.4, vmax = RU.variable_max || 0.6666, tmax = RU.term_max || 30;
    var n = Math.round(v.years * 12), capR = cap(v.status, v.share, N), tt = taxTrack(v.status, v.live), br = P.tracks[tt] || P.tracks.foreign;
    var ps = parts(v, N), k = 0; ps.forEach(function (p) { k += pay(p.w, p.rate, n); });  // the first payment per shekel of loan
    var inc = Math.max(0, +v.income || 0) * fxr, com = Math.max(0, +v.commit || 0) * fxr, disp = inc - com, hasInc = inc > 0;
    var inc50 = hasInc ? Math.max(0, disp) * pmax / k : Infinity, inc33 = hasInc ? Math.max(0, disp) * pthird / k : Infinity;
    var a = Math.min(+v.appr, 100) / 100, l = Math.min(+v.ltv, 100) / 100, clipped = false, cashIls = null, price33 = null, price, loan;
    function costs(price, loan) {
      var tax = ptax(price, br), lawyer = price * (v.lawyer || 0) / 100 * (1 + N.vat);
      var fee = loan > 0 ? Math.min(loan * N.mortgage_fee.rate, N.mortgage_fee.max) : 0, appr = loan > 0 ? N.appraiser : 0;
      return { tax: tax, lawyer: lawyer, fee: fee, appr: appr, cash: price - loan + tax + lawyer + fee + appr };
    }
    if (v.mode === 'cash') {  // the highest price (in ₪1,000 steps) whose cash to close fits the cash; the loan is the lower of the cap and the income limit
      cashIls = Math.max(0, +v.cash || 0) * fxr; clipped = l > capR + EPS; l = Math.min(l, capR);
      var loanAt = function (p, lim) { return Math.max(0, Math.min(p * a * l, lim)); };
      var solve = function (lim) { var lo = 0, hi = 5 * cashIls + 1e6; for (var i = 0; i < 200 && hi - lo > 0.01; i++) { var mid = (lo + hi) / 2; if (costs(mid, loanAt(mid, lim)).cash <= cashIls) lo = mid; else hi = mid; } return Math.floor(lo / 1000 + EPS) * 1000; };
      price = solve(inc50); loan = loanAt(price, inc50); if (hasInc) price33 = solve(inc33);
    } else { price = +v.price; loan = price * a * l; }
    var V = price * a, capLoan = V * capR, maxLoan = Math.min(capLoan, inc50), c = costs(price, loan), cpiF = +v.cpi || 0;
    var tr = ps.map(function (p) { var L = loan * p.w, m = pay(L, p.rate, n); return { k: p.k, w: p.w, rate: p.rate, cpi: p.cpi, prime: p.prime, fx: p.fx, variable: p.variable, loan: L, m: m,
      up: p.prime || p.fx ? pay(L, p.rate + 1, n) : m, year: p.cpi ? m * (1 + cpiF / 100) : m }; });
    var sum = function (key) { return tr.reduce(function (s, x) { return s + x[key]; }, 0); }, has = function (key) { return ps.some(function (p) { return p[key]; }); };
    var first = sum('m'), allFx = ps.every(function (p) { return p.fx; });
    var varShare = ps.reduce(function (s, p) { return s + (p.variable && !(p.fx && v.status === 'foreign') ? p.w : 0); }, 0);  // s.12.3: FX loans to a foreign resident sit outside the cap
    var pti = hasInc ? (disp > 0 ? first / disp : Infinity) : null;
    return {
      cur: cur, fx: f, fxr: fxr, n: n, capR: capR, taxTrack: tt, value: V, capLoan: capLoan, inc: inc, com: com, disp: disp, hasInc: hasInc,
      inc50: hasInc ? inc50 : null, inc33: hasInc ? inc33 : null, maxLoan: maxLoan, binds: hasInc && inc50 < capLoan - 0.5 ? 'income' : 'status',
      loanBind: hasInc && price * a * l > inc50 + 0.5 ? 'income' : 'status',
      price: price, loan: loan, ltvUsed: l, tax: c.tax, lawyer: c.lawyer, fee: c.fee, appr: c.appr, cash: c.cash, cashIls: cashIls, price33: price33,
      tracks: tr, first: first, up1: sum('up'), year1: sum('year'), interest: tr.reduce(function (s, x) { return s + x.m * n - x.loan; }, 0),
      hasPrime: has('prime'), hasCpi: has('cpi'), hasFx: has('fx'), allFx: allFx, varShare: varShare, pti: pti, need50: first / pmax, need33: first / pthird,
      swing: allFx ? { now: first / fxr, weak: first / fxr, strong: first / fxr } : { now: first / fxr, weak: first / (fxr * 1.1), strong: first / (fxr * 0.9) },
      warn: { variable: varShare > vmax + 0.001, term: v.years > tmax, over: loan > capLoan + 0.5, pti: pti != null && pti > pmax + EPS,
        pti40: pti != null && pti > prisk + EPS && pti <= pmax + EPS, clipped: clipped, gap: price - V > 0.5 }
    };
  }
  window.NLNR = { pay: pay, ptax: ptax, compute: compute, cap: cap, taxTrack: taxTrack, primeRate: primeRate, parts: parts, full: full };
  if (!window.NadLanInstruments) return;

  var NI = window.NadLanInstruments, esc = NI.esc;
  var CURS = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'ZAR'], SYM = { USD: '$', EUR: '€', GBP: '£', CAD: 'C$', AUD: 'A$', ZAR: 'R' };  // CAD, AUD, ZAR appear when boi-fx.json carries them
  var STATUS = ['foreign', 'cit_first', 'cit_own', 'cit_sell', 'oleh', 'mixed'], LIVE = { cit_first: 1, cit_own: 1, cit_sell: 1, mixed: 1 };
  var MON = { en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    he: ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'] };
  var TX = {
    kicker: { en: 'Israel mortgage calculator for foreigners', he: 'מחשבון משכנתא לתושבי חוץ, לישראלים בחו״ל ולעולים' },
    title: { en: 'Your Israeli borrowing limit by passport and paycheck', he: 'כמה משכנתא תקבלו בישראל, לפי האזרחות וההכנסה' },
    lede: { en: 'Pick your status, where you live and what you earn. The calculator applies the Bank of Israel loan caps (citizenship sets the loan) and the Tax Authority purchase tax brackets (residency sets the tax), tests the payment against your income in your own currency, and shows the cash to close at the Bank of Israel rate of the day.',
      he: 'בחרו את המעמד שלכם, איפה אתם גרים וכמה אתם מרוויחים. המחשבון מחיל את תקרות המימון של בנק ישראל (האזרחות קובעת את ההלוואה) ואת מדרגות מס הרכישה של רשות המסים (התושבות קובעת את המס), בודק את ההחזר מול ההכנסה במטבע שלכם, ומראה כמה כסף צריך לסגירה לפי השער היציג של בנק ישראל.' },
    egNote: { en: 'The calculator opens with an example: a buyer without Israeli citizenship and a ₪4,000,000 home. Change any number and the result updates.',
      he: 'המחשבון נפתח בדוגמה: קונה בלי אזרחות ישראלית ודירה ב־4,000,000 ₪. שנו כל מספר והתוצאה מתעדכנת.' },
    f_status: { en: 'Your status', he: 'המעמד שלכם' },
    st: { en: { foreign: 'Not an Israeli citizen', cit_first: 'Israeli citizen, no home in Israel', cit_own: 'Israeli citizen, I already own a home in Israel', cit_sell: 'Israeli citizen, selling my Israeli home', oleh: 'New oleh living in Israel', mixed: 'Couple: one Israeli citizen, one not' },
      he: { foreign: 'בלי אזרחות ישראלית', cit_first: 'אזרחות ישראלית, בלי דירה בישראל', cit_own: 'אזרחות ישראלית, כבר יש דירה בישראל', cit_sell: 'אזרחות ישראלית, הדירה הקיימת בישראל תימכר', oleh: 'עולה חדש שגר בישראל', mixed: 'זוג: אחד עם אזרחות ישראלית ואחד בלי' } },
    st_help: { en: 'Citizenship sets the loan (Directive 329); where you live sets the purchase tax.', he: 'האזרחות קובעת את ההלוואה (הוראה 329); מקום המגורים קובע את מס הרכישה.' },
    f_share: { en: 'The Israeli citizen\'s share of the home', he: 'החלק של בן הזוג עם האזרחות הישראלית' },
    share_help: { en: 'The Bank of Israel weighs the cap by each buyer\'s share when the Tax Authority sees you as separate buyers (50/50 gives 62.5%). We assume the Israeli partner owns no other home in Israel. Spouses usually count as one buyer for tax, so ask the bank in writing.',
      he: 'בנק ישראל משקלל את התקרה לפי החלק של כל קונה כשרשות המסים רואה בכם קונים נפרדים (חצי חצי נותן 62.5%). ההנחה: לבן הזוג הישראלי אין דירה אחרת בישראל. בני זוג נחשבים בדרך כלל לקונה אחד לעניין המס, ולכן בקשו מהבנק תשובה בכתב.' },
    f_live: { en: 'Where you live (this sets the purchase tax)', he: 'איפה אתם גרים (זה קובע את מס הרכישה)' },
    live: { en: { abroad: 'Abroad', israel: 'In Israel' }, he: { abroad: 'בחו״ל', israel: 'בישראל' } },
    f_mode: { en: 'What do you want to know?', he: 'מה רוצים לדעת' },
    mode: { en: { borrow: 'What can I borrow?', cash: 'What can my cash buy?' }, he: { borrow: 'כמה אפשר ללוות', cash: 'איזו דירה ההון שלי קונה' } },
    f_price: { en: 'Price of the home', he: 'מחיר הדירה' },
    f_cash: { en: 'Your cash for the purchase, in your currency', he: 'ההון העצמי שלכם לרכישה, במטבע שלכם' },
    cash_help: { en: 'Everything you can put in: the price above the loan, the purchase tax, the lawyer and the fees.', he: 'כל מה שאתם יכולים להביא: המחיר מעל ההלוואה, מס הרכישה, עורך הדין והעמלות.' },
    f_cur: { en: 'Your currency', he: 'המטבע שלכם' },
    cur: { en: { USD: 'US dollar', EUR: 'Euro', GBP: 'Pound', CAD: 'Canadian dollar', AUD: 'Australian dollar', ZAR: 'Rand' }, he: { USD: 'דולר', EUR: 'אירו', GBP: 'לירה שטרלינג', CAD: 'דולר קנדי', AUD: 'דולר אוסטרלי', ZAR: 'ראנד' } },
    f_income: { en: 'Net monthly household income, in your currency', he: 'הכנסה חודשית נטו של משק הבית, במטבע שלכם' },
    income_help: { en: 'After tax. Type 0 to skip the income test.', he: 'אחרי מס. הקלידו 0 כדי לדלג על בדיקת ההכנסה.' },
    f_commit: { en: 'Fixed monthly commitments, in your currency', he: 'התחייבויות חודשיות קבועות, במטבע שלכם' },
    commit_help: { en: 'Loans and other payments running more than 18 months (Directive 329).', he: 'הלוואות ותשלומים שנמשכים יותר מ־18 חודשים (הוראה 329).' },
    f_appr: { en: 'Bank appraisal as a share of the price', he: 'שומת הבנק כאחוז מהמחיר' },
    appr_help: { en: 'The bank lends on the lower of the price and its appraiser\'s value. 100% means the appraisal matches the price.', he: 'הבנק מממן לפי הנמוך מבין המחיר לבין השווי שקבע השמאי שלו. 100% פירושו שהשומה שווה למחיר.' },
    f_ltv: { en: 'Loan as a share of the value', he: 'ההלוואה כאחוז מהשווי' },
    ltv_help: { en: 'Opens at the cap for your status.', he: 'נפתח בתקרה למעמד שלכם.' },
    f_years: { en: 'Years', he: 'שנים' }, u_years: { en: 'years', he: 'שנים' }, u_pts: { en: 'points', he: 'נקודות' },
    f_mix: { en: 'Mortgage mix', he: 'תמהיל המשכנתא' },
    mix: { en: { one: 'One track', b2: 'Thirds (basket 2)', b3: 'Half fixed, half prime (basket 3)', fx: 'Foreign currency loan' },
      he: { one: 'מסלול אחד', b2: 'שלישים (סל 2)', b3: 'חצי קבועה, חצי פריים (סל 3)', fx: 'הלוואה במטבע חוץ' } },
    mix_help: { en: 'The Bank of Israel uniform baskets in every approval in principle. Basket 1 is one track, fixed. Thirds: fixed, prime and CPI-linked variable. A foreign currency loan: non-citizens only.',
      he: 'הסלים האחידים של בנק ישראל בכל אישור עקרוני. סל 1 הוא מסלול אחד, קבועה. שלישים: קבועה, פריים ומשתנה צמודה. הלוואה במטבע חוץ: רק למי שאינו אזרח ישראלי.' },
    f_more: { en: 'Appraisal, interest rate and lawyer fee', he: 'שומה, ריבית ושכר טרחה' }, more: { en: { 0: 'Standard', 1: 'Adjust' }, he: { 0: 'רגיל', 1: 'לשנות' } },
    trk_opt: { en: { fixed: 'Fixed, not linked', linked: 'Fixed, CPI-linked', variable: 'Prime', var5: 'Variable, CPI-linked' }, he: { fixed: 'קבועה לא צמודה', linked: 'קבועה צמודה', variable: 'פריים', var5: 'משתנה צמודה' } },
    f_track: { en: 'Track', he: 'מסלול' }, avg: { en: 'avg', he: 'ממוצע' }, plusCpi: { en: '+ CPI', he: 'ועוד מדד' },
    fxName: { en: 'Foreign currency loan', he: 'הלוואה במטבע חוץ' },
    f_rate: { en: 'Interest rate', he: 'ריבית' },
    rate_help: { en: 'Opens at the Bank of Israel average for the track ({month}). Your bank\'s offer may differ.', he: 'נפתחת בממוצע של בנק ישראל למסלול ({month}). ההצעה של הבנק שלכם יכולה להיות שונה.' },
    f_spread: { en: 'Your bank\'s spread on prime', he: 'המרווח של הבנק על הפריים' },
    spread_help: { en: 'Prime is {prime} (the Bank of Israel rate {boi} plus 1.5). Banks add or take off their own spread: type yours, for example -0.5. The Bank of Israel publishes no average spread.',
      he: 'הפריים {prime} (ריבית בנק ישראל {boi} ועוד 1.5). הבנקים מוסיפים או מורידים מרווח משלהם: הקלידו את שלכם, למשל ‎-0.5. לבנק ישראל אין ממוצע מרווחים.' },
    f_cpi: { en: 'Inflation a year (assumption)', he: 'אינפלציה בשנה (הנחה)' },
    cpi_help: { en: 'For the CPI-linked part. Bank of Israel forecast for the next four quarters: {cpi} ({date}). An assumption, not a promise.', he: 'לחלק הצמוד למדד. תחזית בנק ישראל לארבעת הרבעונים הבאים: {cpi} ({date}). הנחה, לא הבטחה.' },
    f_lawyer: { en: 'Lawyer, before VAT', he: 'עורך דין, לפני מע״מ' },
    lawyer_help: { en: 'Your lawyer\'s fee as a share of the price, plus {vat} VAT. Ask for a written quote.', he: 'שכר הטרחה של עורך הדין כאחוז מהמחיר, ועוד {vat} מע״מ. בקשו הצעה בכתב.' },
    e_price: { en: 'Type the price in shekels.', he: 'הקלידו את המחיר בשקלים.' },
    e_cash: { en: 'Type your cash, in your currency.', he: 'הקלידו את ההון העצמי, במטבע שלכם.' },
    e_money: { en: 'Type a monthly amount, or 0.', he: 'הקלידו סכום חודשי, או 0.' },
    e_share: { en: 'Between 0% and 100%.', he: 'בין 0% ל־100%.' },
    e_appr: { en: 'Between 50% and 100% of the price.', he: 'בין 50% ל־100% מהמחיר.' },
    e_ltv: { en: 'Up to {cap} of the value for your status.', he: 'עד {cap} מהשווי במעמד שלכם.' },
    e_years: { en: 'Between 1 and 40 years (Directive 329 allows up to 30).', he: 'בין 1 ל־40 שנים (הוראה 329 מתירה עד 30).' },
    e_rate: { en: 'An annual rate, e.g. 4.6.', he: 'ריבית שנתית, למשל 4.6.' },
    e_spread: { en: 'A spread between -3 and 3 points.', he: 'מרווח בין מינוס 3 לפלוס 3 נקודות.' },
    e_cpi: { en: 'Between -5% and 15% a year.', he: 'בין מינוס 5% ל־15% בשנה.' },
    e_lawyer: { en: 'Between 0% and 5%.', he: 'בין 0% ל־5%.' },
    s_boi: { en: 'Bank of Israel rate, from {date}', he: 'ריבית בנק ישראל, מ־{date}' }, s_prime: { en: 'Prime', he: 'פריים' },
    s_fixed: { en: 'Fixed not linked, {mon}', he: 'קבועה לא צמודה, {mon}' }, s_fxl: { en: 'Foreign currency loans, {mon}', he: 'הלוואות במטבע חוץ, {mon}' },
    s_max: { en: 'Max loan, non-citizen', he: 'מימון מרבי, בלי אזרחות' }, s_fx: { en: '1 {cur} in ₪, {date}', he: '{cur} בשקלים, {date}' },
    a_borrow: { en: 'The most you can borrow on this home', he: 'הסכום הגבוה ביותר שאפשר ללוות על הדירה הזאת' },
    a_cash: { en: 'The most home your cash buys', he: 'המחיר הגבוה ביותר שההון שלכם קונה' },
    b_status: { en: 'The {cap} cap for your status limits you, not your income: your income would carry {inc}.', he: 'מה שמגביל אתכם הוא תקרת ה־{cap} למעמד שלכם, לא ההכנסה: ההכנסה שלכם נושאת עד {inc}.' },
    b_income: { en: 'Your income, not the {cap} cap, limits you to {max}.', he: 'ההכנסה שלכם, ולא תקרת ה־{cap}, מגבילה אתכם ל־{max}.' },
    b_noinc: { en: 'The cap for your status is {cap} of the value. Add your income to test the payment.', he: 'התקרה למעמד שלכם היא {cap} מהשווי. הוסיפו הכנסה כדי לבדוק את ההחזר.' },
    b_none: { en: 'Your fixed commitments use up your income, so the income test fails.', he: 'ההתחייבויות הקבועות שלכם גדולות מההכנסה, ולכן בדיקת ההכנסה לא עוברת.' },
    c_sub: { en: 'loan {loan}, limited by {why}', he: 'הלוואה של {loan}, והגבול הוא {why}' },
    why_cap: { en: 'the {cap} cap for your status', he: 'תקרת ה־{cap} למעמד שלכם' }, why_inc: { en: 'your income', he: 'ההכנסה שלכם' },
    l_cashils: { en: 'Your cash in shekels at ₪{rate}', he: 'ההון שלכם בשקלים, לפי {rate} ₪' },
    l_p33: { en: 'Price if the bank holds you to one third of income', he: 'המחיר אם הבנק מגביל אתכם לשליש מההכנסה' },
    l_value: { en: 'Value the bank lends on (lower of price and appraisal)', he: 'השווי שהבנק מממן לפיו (הנמוך מבין המחיר לשומה)' },
    l_cap: { en: 'Loan cap for your status, {cap} (Directive 329)', he: 'תקרת המימון למעמד שלכם, {cap} (הוראה 329)' },
    l_inc50: { en: 'Loan your income carries, payment at 50% of disposable income', he: 'ההלוואה שההכנסה נושאת, החזר של 50% מההכנסה הפנויה' },
    l_inc33: { en: 'Same at one third of income, what most banks prefer', he: 'אותו דבר בשליש מההכנסה, מה שרוב הבנקים מעדיפים' },
    l_loan: { en: 'Your loan, {pct} of the value', he: 'ההלוואה שלכם, {pct} מהשווי' },
    l_first: { en: 'First monthly payment, {n} payments', he: 'ההחזר החודשי הראשון, {n} תשלומים' },
    l_up: { en: 'If prime rises 1 point (only the prime part reprices)', he: 'אם הפריים עולה בנקודה (רק החלק בפריים משתנה)' },
    l_up0: { en: 'If prime rises 1 point: no prime part in this mix', he: 'אם הפריים עולה בנקודה: אין פריים בתמהיל הזה' },
    l_upfx: { en: 'If the foreign currency rate rises 1 point', he: 'אם הריבית במטבע החוץ עולה בנקודה' },
    l_year: { en: 'After a year of {cpi} inflation (CPI-linked part)', he: 'אחרי שנה של {cpi} אינפלציה (החלק הצמוד)' },
    l_pti: { en: 'Payment as a share of disposable income', he: 'ההחזר כאחוז מההכנסה הפנויה' },
    l_need: { en: 'Net monthly income this payment needs: at the 50% cap · at one third', he: 'ההכנסה נטו שההחזר הזה דורש: בתקרה של 50% · בשליש' },
    l_tax: { en: 'Purchase tax, {track}', he: 'מס רכישה, {track}' },
    trk: { en: { foreign: 'foreign resident, until {date}', extra: 'additional home, until {date}', single: 'Israeli resident, single home', oleh: 'oleh (regulation 12A)' },
      he: { foreign: 'תושב חוץ, עד {date}', extra: 'דירה נוספת, עד {date}', single: 'תושב ישראל, דירה יחידה', oleh: 'עולה (תקנה 12א)' } },
    l_fees: { en: 'Lawyer incl. VAT, appraiser and file fee (typical, check your bank\'s tariff)', he: 'עורך דין כולל מע״מ, שמאי ועמלת פתיחת תיק (מקובל, בדקו בתעריף של הבנק)' },
    l_cash: { en: 'Cash to close', he: 'הכסף שצריך לסגירה' },
    l_int: { en: 'Total interest if the rates hold (no inflation)', he: 'סך הריבית אם הריביות נשארות (בלי אינפלציה)' },
    l_fx: { en: '1 {cur} = ₪{rate} on {date}; 30-day low / high', he: '{cur} = {rate} ₪ ב־{date}; הנמוך והגבוה ב־30 ימים' },
    bd_down: { en: 'Down payment', he: 'הון עצמי למחיר' }, bd_tax: { en: 'Purchase tax', he: 'מס רכישה' }, bd_fees: { en: 'Lawyer, appraiser, file fee', he: 'עורך דין, שמאי ועמלה' },
    sc_label: { en: 'Your monthly payment in {cur} if the shekel moves 10%', he: 'ההחזר החודשי במטבע שלכם אם השקל זז ב־10%' },
    sc_weak: { en: 'Shekel weakens 10%', he: 'השקל נחלש ב־10%' }, sc_now: { en: 'Today', he: 'היום' }, sc_strong: { en: 'Shekel strengthens 10%', he: 'השקל מתחזק ב־10%' },
    n_foreign: { en: 'Directive 329 treats any home a non-citizen buys as an investment home, so the cap is {cap} even for your first and only home here. Purchase tax for a foreign resident: {br}, from the first shekel, until {date}.',
      he: 'הוראה 329 רואה בכל דירה שקונה מי שאינו אזרח ישראלי דירה להשקעה, ולכן התקרה {cap} גם לדירה הראשונה והיחידה שלכם כאן. מס רכישה לתושב חוץ: {br}, מהשקל הראשון, עד {date}.' },
    n_cit_first_abroad: { en: 'Citizenship sets your loan, residency sets your tax: as an Israeli citizen you can borrow up to {cap} for your only home in Israel, and living abroad you pay the foreign-resident purchase tax, {br}.',
      he: 'האזרחות קובעת את ההלוואה, התושבות קובעת את המס: כאזרחים ישראלים אתם יכולים ללוות עד {cap} לדירה היחידה בישראל, וכשאתם גרים בחו״ל אתם משלמים מס רכישה של תושב חוץ, {br}.' },
    n_cit_first_israel: { en: 'An Israeli citizen buying the only home in Israel: up to {cap}, and the single-home purchase tax brackets of an Israeli resident, {br}.',
      he: 'אזרח ישראלי שקונה את הדירה היחידה בישראל: עד {cap}, ומס רכישה במדרגות של דירה יחידה לתושב ישראל, {br}.' },
    n_cit_own: { en: 'You already own a home in Israel, so this one is an investment home: up to {cap}, and purchase tax on the additional-home brackets, {br}, until {date}.',
      he: 'כבר יש לכם דירה בישראל, ולכן זו דירה להשקעה: עד {cap}, ומס רכישה במדרגות של דירה נוספת, {br}, עד {date}.' },
    n_cit_sell_abroad: { en: 'A replacement home: up to {cap} while you sell the home you own. Living abroad, you pay the foreign-resident purchase tax, {br}.',
      he: 'דירה חלופית: עד {cap} כשאתם מוכרים את הדירה הקיימת. כשאתם גרים בחו״ל, מס הרכישה הוא של תושב חוץ, {br}.' },
    n_cit_sell_israel: { en: 'A replacement home: up to {cap} while you sell the home you own. Purchase tax on the single-home brackets, {br}, when you sell the home you own within the period the law allows; ask your lawyer.',
      he: 'דירה חלופית: עד {cap} כשאתם מוכרים את הדירה הקיימת. מס רכישה במדרגות של דירה יחידה, {br}, כשהדירה הקיימת נמכרת בתוך התקופה שהחוק מאפשר; בדקו עם עורך הדין.' },
    n_oleh: { en: 'A registered oleh counts as an Israeli citizen: up to {cap} for the only home. Purchase tax on the oleh brackets (regulation 12A) for a single home bought from 1 year before to 7 years after aliyah: {br}.',
      he: 'עולה רשום נחשב לאזרח ישראלי: עד {cap} לדירה היחידה. מס רכישה במדרגות של עולה (תקנה 12א) לדירה יחידה שנקנית משנה לפני העלייה ועד 7 שנים אחריה: {br}.' },
    n_mixed: { en: 'The Bank of Israel follows the Tax Authority: as separate buyers your cap is weighted by your shares ({share} at 75% and the rest at 50% gives {cap}). Spouses usually count as one buyer for tax, so get the bank\'s answer in writing.',
      he: 'בנק ישראל הולך לפי רשות המסים: כקונים נפרדים התקרה משוקללת לפי החלקים ({share} ב־75% והשאר ב־50% נותן {cap}). בני זוג נחשבים בדרך כלל לקונה אחד לעניין המס, ולכן בקשו מהבנק תשובה בכתב.' },
    n_mixed_abroad: { en: 'Living abroad, you both pay the foreign-resident purchase tax, {br}.', he: 'כשאתם גרים בחו״ל, שניכם משלמים מס רכישה של תושב חוץ, {br}.' },
    n_mixed_israel: { en: 'We used the single-home brackets, {br}; they hold only if you both count as Israeli residents for tax, so ask the Tax Authority.',
      he: 'חישבנו לפי מדרגות דירה יחידה, {br}; הן חלות רק אם שניכם נחשבים לתושבי ישראל לעניין המס, ולכן בדקו ברשות המסים.' },
    n_fx: { en: 'A foreign currency loan suits you only if you earn in that currency. Its average rate was {rate} in {mon}, and it was {share} of new lending. For a non-citizen it sits outside the two-thirds variable cap (Directive 329 s.12.3). Borrowed in your currency, the payment stays the same whatever the shekel does; which currencies a bank lends in is its own choice.',
      he: 'הלוואה במטבע חוץ מתאימה רק למי שמרוויח במטבע הזה. הריבית הממוצעת עליה הייתה {rate} ב{mon}, והיא הייתה {share} מההלוואות החדשות. למי שאינו אזרח ישראלי היא מחוץ למגבלת שני השלישים במשתנה (הוראה 329 סעיף 12.3). כשלווים במטבע שלכם, ההחזר נשאר זהה מה שלא יקרה לשקל; באילו מטבעות הבנק מלווה, זו החלטה שלו.' },
    w_head: { en: 'Check:', he: 'שימו לב:' },
    w_variable: { en: 'the variable part is {x} of the loan; Directive 329 allows at most 66.66%, so at least one third must be fixed.', he: 'החלק המשתנה הוא {x} מההלוואה; הוראה 329 מתירה עד 66.66%, ולכן לפחות שליש צריך להיות בריבית קבועה.' },
    w_term: { en: 'a term of {y} years; Directive 329 allows at most 30.', he: 'תקופה של {y} שנים; הוראה 329 מתירה עד 30.' },
    w_over: { en: 'your loan is above the cap for your status; an Israeli bank can lend up to {cap} of the value, {x} here.', he: 'ההלוואה מעל התקרה למעמד שלכם; בנק בישראל יכול לממן עד {cap} מהשווי, כאן {x}.' },
    w_pti: { en: 'the payment is {p} of your disposable income; Directive 329 caps it at 50%.', he: 'ההחזר הוא {p} מההכנסה הפנויה; הוראה 329 מגבילה אותו ל־50%.' },
    w_pti0: { en: 'your fixed commitments are as large as your income, so no payment passes the income test.', he: 'ההתחייבויות הקבועות גדולות מההכנסה, ולכן שום החזר לא עובר את בדיקת ההכנסה.' },
    w_pti40: { en: 'above 40% of income the loan carries a 100% risk weight for the bank (Directive 329 s.6).', he: 'מעל 40% מההכנסה ההלוואה נושאת משקל סיכון של 100% אצל הבנק (הוראה 329 סעיף 6).' },
    w_clip: { en: 'we used the cap for your status, {cap}, not the {ltv} you typed.', he: 'חישבנו לפי התקרה למעמד שלכם, {cap}, ולא לפי {ltv} שהקלדתם.' },
    w_gap: { en: 'the appraisal is {x} below the price; the bank lends on the lower figure and you cover the gap in cash.', he: 'השומה נמוכה מהמחיר ב־{x}; הבנק מממן לפי הנמוך, ואת הפער משלימים מההון העצמי.' },
    src_fx: { en: 'Bank of Israel representative exchange rates, {date}', he: 'בנק ישראל, שערים יציגים, {date}' },
    src_tax: { en: 'Israel Tax Authority, purchase tax brackets (instruction 1/2026)', he: '' },
    src_ext: { en: 'Israel Tax Authority, the 8% / 10% rate extended to 10 Feb 2027 (notice of 12 Oct 2026)', he: '' },
    formula: { en: 'Payment per track = loan × r ÷ (1 − (1 + r)^−n), r = annual rate ÷ 12, n = months; a CPI-linked part grows with the index. Value = lower of price and appraisal. Loan cap = value × the cap for your status. Income cap = (net income − commitments) × 50% ÷ the payment per shekel of loan. Cash to close = price − loan + purchase tax + lawyer × {vat} + appraiser + file fee.',
      he: 'החזר לכל מסלול = הלוואה × ⁦r ÷ (1 − (1 + r)^−n)⁩, כאשר r = ריבית שנתית ÷ 12 ו־n = חודשים; חלק צמוד גדל עם המדד. שווי = הנמוך מבין המחיר לשומה. תקרת מימון = שווי × התקרה למעמד. תקרה לפי הכנסה = (הכנסה נטו − התחייבויות) × 50% ÷ ההחזר לכל שקל הלוואה. כסף לסגירה = מחיר − הלוואה + מס רכישה + עורך דין × {vat} + שמאי + עמלת תיק.' },
    t_title: { en: 'Cash to close and the payment, line by line', he: 'הכסף לסגירה וההחזר, שורה אחר שורה' },
    t_item: { en: 'Item', he: 'סעיף' }, t_price: { en: 'Price', he: 'מחיר' }, t_value: { en: 'Value the bank lends on', he: 'השווי לפי הבנק' }, t_loan: { en: 'Mortgage', he: 'משכנתא' },
    t_tax: { en: 'Purchase tax', he: 'מס רכישה' }, t_lawyer: { en: 'Lawyer incl. VAT', he: 'עורך דין כולל מע״מ' }, t_appr: { en: 'Bank appraiser (typical)', he: 'שמאי הבנק (מקובל)' },
    t_fee: { en: 'Mortgage file fee (typical)', he: 'עמלת פתיחת תיק (מקובל)' }, t_cash: { en: 'Cash to close', he: 'הכסף לסגירה' },
    t_part: { en: '{track}, {w} at {rate}', he: '{track}, {w} בריבית {rate}' }, t_first: { en: 'First monthly payment', he: 'ההחזר החודשי הראשון' },
    g_title: { en: 'What limits your loan', he: 'מה מגביל את ההלוואה' },
    g_cap: { en: 'Cap for your status, {cap}', he: 'תקרה למעמד שלכם, {cap}' }, g_inc50: { en: 'Your income, payment at 50%', he: 'ההכנסה שלכם, החזר של 50%' },
    g_inc33: { en: 'Your income, payment at one third', he: 'ההכנסה שלכם, החזר של שליש' }, g_loan: { en: 'Your loan', he: 'ההלוואה שלכם' },
    g_foot: { en: 'Dashed mark: the lower limit, {x}', he: 'הסימון המקווקו: הגבול הנמוך, {x}' },
    g2_title: { en: 'The {price} home: loan and your cash', he: 'דירה ב־{price}: הלוואה והון עצמי' },
    g2_loan: { en: 'Loan', he: 'הלוואה' }, g2_own: { en: 'Your cash toward the price', he: 'ההון שלכם למחיר' }, g2_tax: { en: 'Purchase tax', he: 'מס רכישה' },
    g2_fees: { en: 'Lawyer and fees', he: 'עורך דין ועמלות' }, g2_tot: { en: 'Your cash, all in', he: 'ההון שלכם, הכול כלול' },
    x_borrow: { en: 'Israeli mortgage, {status}: home {price}, the most you can borrow {max}; loan {loan} over {y} years, first payment {m} a month ({mfc}); cash to close {cash} ({cfc}).',
      he: 'משכנתא בישראל, {status}: דירה ב־{price}, הסכום הגבוה ביותר ללוות {max}; הלוואה של {loan} ל־{y} שנים, החזר ראשון {m} בחודש ({mfc}); כסף לסגירה {cash} ({cfc}).' },
    x_cash: { en: 'Israeli mortgage, {status}: {cfc} of cash buys a home of up to {price} with a loan of {loan}; first payment {m} a month ({mfc}).',
      he: 'משכנתא בישראל, {status}: הון של {cfc} קונה דירה עד {price} עם הלוואה של {loan}; החזר ראשון {m} בחודש ({mfc}).' },
    p_foreign: { en: 'Not an Israeli citizen', he: 'בלי אזרחות ישראלית' }, p_foreign_s: { en: '₪4,000,000 · 50% loan', he: '₪4,000,000 · מימון 50%' },
    p_abroad: { en: 'Israeli citizen abroad', he: 'ישראלים שגרים בחו״ל' }, p_abroad_s: { en: 'first home · 75% loan', he: 'דירה ראשונה · מימון 75%' },
    p_oleh: { en: 'New oleh in Israel', he: 'עולה חדש בישראל' }, p_oleh_s: { en: '75% loan · tax 12A', he: 'מימון 75% · מס לפי 12א' },
    p_couple: { en: 'Couple, one Israeli', he: 'זוג, אחד ישראלי' }, p_couple_s: { en: '50/50 · cap 62.5%', he: '50/50 · תקרה 62.5%' },
    p_cash: { en: 'What $800,000 buys', he: 'מה $800,000 קונים' }, p_cash_s: { en: 'non-citizen · thirds mix', he: 'בלי אזרחות · תמהיל שלישים' },
    p_fx: { en: 'Borrow in dollars', he: 'הלוואה בדולרים' }, p_fx_s: { en: 'foreign currency · {rate}', he: 'מטבע חוץ · {rate}' }
  };
  function fill(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }

  /* The drawings: a cross-border buyer's palette (passport navy, visa violet, security-print teal, cool paper, slate; figures in
     IBM Plex Mono). Text 14 to 17 px in a 420-wide box (about 11 to 13 px on a 390 px phone). */
  var C = { navy: '#1E2B47', violet: '#5B3FA0', teal: '#0F7C7A', paper: '#F6F8FA', slate: '#2B3440', line: '#C9D2DB', track: '#E3E8EE', fee: '#6B7785' };
  var MONO = '\'IBM Plex Mono\',ui-monospace,monospace', SEQ = 0;
  function tx(x, y, s, o) {
    o = o || {};
    return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" text-anchor="' + (o.a || 'start') + '" style="font:' + (o.w || 400) + ' ' + (o.s || 14) + 'px ' + (o.m ? MONO : 'var(--nli-sans,sans-serif)') + ';fill:' + (o.f || C.slate) + '">' + esc(s) + '</text>';
  }
  function frame(W, H, rtl, aria, body) {
    return '<svg viewBox="0 0 ' + W + ' ' + H + '"' + (rtl ? ' direction="rtl"' : '') + ' role="img" aria-label="' + esc(aria) + '" style="max-width:520px">'
      + '<rect x="0.5" y="0.5" width="' + (W - 1) + '" height="' + (H - 1) + '" fill="' + C.paper + '" stroke="' + C.line + '"/>' + body + '</svg>';
  }
  /** The two-limit bars: the status cap, the income caps, your loan; a dashed mark on each bar at the lower limit. */
  function figLimits(o) {
    var W = 420, X0 = 14, X1 = 406, SP = X1 - X0, rtl = o.rtl, id = 'nrmh' + (++SEQ), g = [];
    var X = function (x) { return rtl ? W - x : x; };
    var core = Math.max.apply(null, o.rows.filter(function (r) { return r.core; }).map(function (r) { return r.v; }).concat([1]));
    var top = Math.max.apply(null, o.rows.map(function (r) { return r.v; }).concat([1])); if (top > 2.5 * core) top = 2.5 * core;
    var wOf = function (x) { return Math.max(2, SP * Math.min(x, top) / top); };
    g.push('<defs><pattern id="' + id + '" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#CFE6E5"/><rect width="3" height="6" fill="' + C.teal + '"/></pattern></defs>');
    g.push(tx(X(X0), 28, o.title, { w: 600, s: 17, f: C.navy }));
    var y = 60, mw = wOf(o.mark);
    o.rows.forEach(function (r) {
      var by = y + 9, w = wOf(r.v);
      g.push(tx(X(X0), y, r.label, { s: 16 }));
      g.push(tx(X(X1), y, r.shown, { a: 'end', m: true, w: 500, s: 16, f: C.navy }));
      g.push('<rect x="' + X0 + '" y="' + by + '" width="' + SP + '" height="18" fill="' + C.track + '"/>');
      g.push('<rect x="' + (rtl ? W - X0 - w : X0).toFixed(1) + '" y="' + by + '" width="' + w.toFixed(1) + '" height="18" fill="' + (r.hatch ? 'url(#' + id + ')' : r.fill) + '"/>');
      if (r.v > top + 0.5) { var xc = X(X1 - 20); g.push('<path d="M' + (xc - 4).toFixed(1) + ' ' + (by - 2) + ' l6 22 M' + (xc + 2).toFixed(1) + ' ' + (by - 2) + ' l6 22" stroke="' + C.paper + '" stroke-width="3" fill="none"/>'); }
      var mx = X(X0 + mw).toFixed(1);
      g.push('<line x1="' + mx + '" y1="' + (by - 4) + '" x2="' + mx + '" y2="' + (by + 22) + '" stroke="' + C.slate + '" stroke-width="1.6" stroke-dasharray="3 2"/>');
      y += 58;
    });
    var H = y - 58 + 9 + 18 + 36;
    g.push(tx(X(X0), H - 12, o.foot, { s: 14 }));
    return frame(W, H, rtl, o.aria, g.join(''));
  }
  /** The stacked bar of the price, tax and fees: the loan and your cash. */
  function figCash(o) {
    var W = 420, X0 = 14, X1 = 406, SP = X1 - X0, rtl = o.rtl, g = [], tot = o.segs.reduce(function (s, x) { return s + Math.max(0, x.v); }, 0) || 1;
    var X = function (x) { return rtl ? W - x : x; };
    g.push(tx(X(X0), 28, o.title, { w: 600, s: 17, f: C.navy }));
    var cum = 0;
    o.segs.forEach(function (sg) { var w = SP * Math.max(0, sg.v) / tot; if (w > 0) g.push('<rect x="' + (rtl ? W - X0 - cum - w : X0 + cum).toFixed(1) + '" y="44" width="' + w.toFixed(1) + '" height="30" fill="' + sg.fill + '"/>'); cum += w; });
    var y = 106;
    o.segs.forEach(function (sg) {
      g.push('<rect x="' + (rtl ? W - X0 - 13 : X0) + '" y="' + (y - 12) + '" width="13" height="13" fill="' + sg.fill + '"/>');
      g.push(tx(X(X0 + 22), y, sg.label, { s: 16 }));
      g.push(tx(X(X1), y, sg.shown, { a: 'end', m: true, w: 500, s: 16, f: C.navy }));
      y += 28;
    });
    g.push('<line x1="' + X0 + '" y1="' + (y - 16) + '" x2="' + X1 + '" y2="' + (y - 16) + '" stroke="' + C.line + '"/>');
    g.push(tx(X(X0), y + 4, o.total.label, { w: 600, s: 16, f: C.navy }));
    g.push(tx(X(X1), y + 4, o.total.shown, { a: 'end', m: true, w: 600, s: 16, f: C.navy }));
    return frame(W, y + 22, rtl, o.aria, g.join(''));
  }

  /** The spec for one language: the tool follows its own section's lang (an English tool on a Hebrew path stays English). */
  function make(lg, data) {
    var T = NI.pick(TX, lg), EN = lg === 'en', N = data.nrm, P = data.ptax, FX = data.fx, rtl = !EN;
    var LOC = EN ? 'en-US' : 'he-IL', nf = new Intl.NumberFormat(LOC, { maximumFractionDigits: 0 });
    var ils = function (x) { return '₪' + nf.format(Math.round(x)); };
    var fc = function (x, cur) { return SYM[cur] + nf.format(Math.round(x / FX.fx[cur].rate)); };
    var pc = function (x, d) { return new Intl.NumberFormat(LOC, { maximumFractionDigits: d == null ? 2 : d }).format(x) + '%'; };
    var date = function (iso) { var p = String(iso).split('-'); return p.length === 3 ? (EN ? (+p[2]) + ' ' + MON.en[+p[1] - 1].slice(0, 3) + ' ' + p[0] : (+p[2]) + '.' + (+p[1]) + '.' + p[0]) : iso; };
    var mon = function (key, long) { var p = String(key).split('-'), m = +p[1] - 1; if (EN) return (long ? MON.en[m] : MON.en[m].slice(0, 3)) + ' ' + p[0]; return long ? MON.he[m] + ' ' + p[0] : (m + 1) + '.' + p[0]; };
    var R = {}; N.rates.forEach(function (r) { R[r.id] = r; });
    var rl = function (id) { return id === 'fx' ? T.fxName : (EN ? R[id].label : (R[id].label_he || R[id].label)); };
    var src = function (s) { return { label: EN ? s.label : (s.label_he || s.label), url: s.url || '' }; };
    var curs = CURS.filter(function (c) { return FX && FX.fx && FX.fx[c]; });
    var curName = function (c) { return T.cur[c] || c; };
    var trackRate = function (v) { var r = R[v.track] || N.rates[0]; return Math.round(100 * (r.prime ? primeRate(N, v.spread) : r.rate)) / 100; };
    var primeV = function (v) { return v.mix === 'b2' || v.mix === 'b3' || (v.mix === 'one' && !!R[v.track] && !!R[v.track].prime); };
    var cpiV = function (v) { return v.mix === 'b2' || (v.mix === 'one' && !!R[v.track] && !!R[v.track].cpi); };
    var brText = function (br) {
      var out = br.map(function (b) { return b[0] == null ? fill(EN ? '{r} above' : '{r} מעל', { r: pc(100 * b[1]) }) : fill(EN ? '{r} up to {hi}' : '{r} עד {hi}', { r: pc(100 * b[1]), hi: ils(b[0]) }); });
      return out.length > 1 ? out.slice(0, -1).join(', ') + (EN ? ' and ' : ' ו־') + out[out.length - 1] : out[0];
    };
    var VAL = P.valid || {}, fixedRate = N.rates[0].rate, fxRate = N.fx_track ? N.fx_track.rate : 4.86;
    var base = { mode: 'borrow', price: 4000000, appr: 100, years: 25, mix: 'one', track: N.rates[0].id, rate: fixedRate, spread: 0 };
    var ext = function (o) { var x = JSON.parse(JSON.stringify(base)); Object.keys(o).forEach(function (k) { x[k] = o[k]; }); return x; };
    var presets = [
      { key: 'foreign', label: T.p_foreign, sub: T.p_foreign_s, set: ext({ status: 'foreign', live: 'abroad', ltv: 50 }) },
      { key: 'abroad', label: T.p_abroad, sub: T.p_abroad_s, set: ext({ status: 'cit_first', live: 'abroad', ltv: 75 }) },
      { key: 'oleh', label: T.p_oleh, sub: T.p_oleh_s, set: ext({ status: 'oleh', live: 'israel', ltv: 75 }) },
      { key: 'couple', label: T.p_couple, sub: T.p_couple_s, set: ext({ status: 'mixed', share: 50, live: 'abroad', ltv: 62.5 }) }
    ];
    if (FX.fx.USD) {
      presets.push({ key: 'cash', label: T.p_cash, sub: T.p_cash_s, set: { mode: 'cash', status: 'foreign', live: 'abroad', cash: 800000, cur: 'USD', appr: 100, ltv: 50, years: 25, mix: 'b2', spread: 0, cpi: N.cpi_forecast } });
      presets.push({ key: 'fx', label: T.p_fx, sub: fill(T.p_fx_s, { rate: pc(fxRate) }), set: ext({ status: 'foreign', live: 'abroad', ltv: 50, mix: 'fx', rate: fxRate, cur: 'USD' }) });
    }
    return {
      kicker: T.kicker, title: T.title, lede: T.lede, exampleNote: T.egNote, presets: presets,
      strip: function () {
        var u = FX.fx[curs[0]];
        return [{ label: fill(T.s_boi, { date: date(N.boi_rate_from) }), value: pc(N.boi_rate) }, { label: T.s_prime, value: pc(N.prime) },
          { label: fill(T.s_fixed, { mon: mon(N.rates_month) }), value: pc(fixedRate) }, { label: fill(T.s_fxl, { mon: mon(N.fx_track.month) }), value: pc(fxRate) },
          { label: T.s_max, value: pc(100 * N.ltv_by_status.foreign) }, { label: fill(T.s_fx, { cur: EN ? curs[0] : curName(curs[0]), date: date(u.date) }), value: String(u.rate) }];
      },
      defaults: function () {
        return { status: 'foreign', share: 50, live: 'abroad', mode: 'borrow', price: 4000000, cash: 800000, cur: curs[0] || 'USD', income: 12000, commit: 0, appr: 100, ltv: 50, years: 25,
          mix: 'one', track: N.rates[0].id, rate: fixedRate, spread: 0, cpi: N.cpi_forecast, lawyer: 0.5, more: '0' };
      },
      fields: [
        { id: 'status', label: T.f_status, type: 'segmented', options: STATUS.map(function (k) { return { value: k, label: T.st[k] }; }), help: esc(T.st_help) },
        { id: 'share', label: T.f_share, type: 'percent', unit: '%', help: esc(T.share_help), showIf: function (v) { return v.status === 'mixed'; } },
        { id: 'live', label: T.f_live, type: 'segmented', options: [{ value: 'abroad', label: T.live.abroad }, { value: 'israel', label: T.live.israel }], showIf: function (v) { return !!LIVE[v.status]; } },
        { id: 'mode', label: T.f_mode, type: 'segmented', options: [{ value: 'borrow', label: T.mode.borrow }, { value: 'cash', label: T.mode.cash }] },
        { id: 'price', label: T.f_price, type: 'money', unit: '₪', showIf: function (v) { return v.mode !== 'cash'; } },
        { id: 'cash', label: T.f_cash, type: 'money', help: esc(T.cash_help), showIf: function (v) { return v.mode === 'cash'; } },
        { id: 'cur', label: T.f_cur, type: 'segmented', options: curs.map(function (c) { return { value: c, label: curName(c) }; }) },
        { id: 'income', label: T.f_income, type: 'money', help: esc(T.income_help) },
        { id: 'commit', label: T.f_commit, type: 'money', help: esc(T.commit_help) },
                { id: 'ltv', label: T.f_ltv, type: 'percent', unit: '%', help: esc(T.ltv_help) },
        { id: 'years', label: T.f_years, type: 'number', unit: T.u_years },
        { id: 'mix', label: T.f_mix, type: 'select', help: esc(T.mix_help),
          optionsFrom: function (v) { return ['one', 'b2', 'b3', 'fx'].filter(function (m) { return m !== 'fx' || v.status === 'foreign'; }).map(function (m) { return { value: m, label: T.mix[m] }; }); } },
        { id: 'track', label: T.f_track, type: 'select', showIf: function (v) { return v.mix === 'one'; },
          options: N.rates.map(function (r) { return { value: r.id, label: (T.trk_opt[r.id] || rl(r.id)) + ' · ' + pc(r.prime ? N.prime : r.rate) }; }) },
        { id: 'more', label: T.f_more, type: 'segmented', options: [{ value: '0', label: T.more[0] }, { value: '1', label: T.more[1] }] },
        { id: 'rate', label: T.f_rate, type: 'percent', unit: '%', help: esc(fill(T.rate_help, { month: mon(N.rates_month, true) })), showIf: function (v) { return v.more === '1' && (v.mix === 'one' || v.mix === 'fx'); } },
        { id: 'appr', label: T.f_appr, type: 'percent', unit: '%', help: esc(T.appr_help), showIf: function (v) { return v.more === '1'; } },
        { id: 'spread', label: T.f_spread, type: 'number', unit: T.u_pts, help: esc(fill(T.spread_help, { prime: pc(N.prime), boi: pc(N.boi_rate) })), showIf: primeV },
        { id: 'cpi', label: T.f_cpi, type: 'percent', unit: '%', help: esc(fill(T.cpi_help, { cpi: pc(N.cpi_forecast, 1), date: date(N.cpi_forecast_published) })), showIf: cpiV },
        { id: 'lawyer', label: T.f_lawyer, type: 'percent', unit: '%', help: esc(fill(T.lawyer_help, { vat: pc(100 * N.vat, 0) })), showIf: function (v) { return v.more === '1'; } }
      ],
      onField: function (id, v, d, redraw) {
        if (id === 'status' || id === 'share') {
          v.ltv = Math.round(10000 * cap(v.status, v.share, N)) / 100; redraw('ltv');
          if (v.status !== 'foreign' && v.mix === 'fx') { v.mix = 'one'; v.rate = trackRate(v); redraw('rate'); }
        }
        if (id === 'track' || (id === 'spread' && v.mix === 'one' && R[v.track] && R[v.track].prime)) { v.rate = trackRate(v); redraw('rate'); }
        if (id === 'mix') { v.rate = v.mix === 'fx' ? fxRate : trackRate(v); redraw('rate'); }
        if (id === 'more' && v.more === '0') { v.rate = v.mix === 'fx' ? fxRate : trackRate(v); v.appr = 100; v.lawyer = 0.5; redraw('rate'); redraw('appr'); redraw('lawyer'); }  // back to the standard values
      },
      compute: function (v, d, scen) {
        var E = function (f, m) { return { error: { field: f, msg: m } }; }, capR = cap(v.status, v.share, N), capS = pc(100 * capR);
        if (v.mode !== 'cash' && !(v.price >= 300000 && v.price <= 500000000)) return E('price', T.e_price);
        if (v.mode === 'cash' && !(v.cash > 0 && v.cash < 1e9)) return E('cash', T.e_cash);
        if (!(v.income >= 0)) return E('income', T.e_money);
        if (!(v.commit >= 0)) return E('commit', T.e_money);
        if (v.status === 'mixed' && !(v.share >= 0 && v.share <= 100)) return E('share', T.e_share);
        if (!(v.appr >= 50 && v.appr <= 100)) return E('appr', T.e_appr);
        if (!(v.ltv >= 0 && v.ltv < 100)) return E('ltv', fill(T.e_ltv, { cap: capS }));
        if (!(v.years >= 1 && v.years <= 40)) return E('years', T.e_years);
        if ((v.mix === 'one' || v.mix === 'fx') && !(v.rate >= 0 && v.rate <= 15)) return E('rate', T.e_rate);
        if (primeV(v) && !(v.spread >= -3 && v.spread <= 3)) return E('spread', T.e_spread);
        if (cpiV(v) && !(v.cpi >= -5 && v.cpi <= 15)) return E('cpi', T.e_cpi);
        if (!(v.lawyer >= 0 && v.lawyer <= 5)) return E('lawyer', T.e_lawyer);
        var r = full(v, P, N, FX), cur = r.cur, f = r.fx, cashMode = v.mode === 'cash', tt = r.taxTrack;
        var F = function (x) { return fc(x, cur); }, both = function (x) { return ils(x) + ' · ' + F(x); };
        var vd = tt === 'single' || tt === 'oleh' ? (VAL.single || P.frozen_until) : (VAL[tt] || VAL.foreign);
        var trName = fill(T.trk[tt], { date: date(vd) }), br = brText(P.tracks[tt] || P.tracks.foreign);
        var why = !r.hasInc ? fill(T.b_noinc, { cap: capS }) : r.disp <= 0 ? T.b_none : r.binds === 'income' ? fill(T.b_income, { cap: capS, max: ils(r.maxLoan) }) : fill(T.b_status, { cap: capS, inc: ils(r.inc50) });
        var answer = cashMode
          ? { label: T.a_cash, value: ils(r.price), tone: 'survey', sub: esc('≈ ' + F(r.price) + ' · ' + fill(T.c_sub, { loan: ils(r.loan), why: r.loanBind === 'income' ? T.why_inc : fill(T.why_cap, { cap: capS }) })) }
          : { label: T.a_borrow, value: ils(r.maxLoan), tone: 'survey', sub: esc('≈ ' + F(r.maxLoan) + ' · ' + why) };
        var lines = [];
        if (cashMode) {
          lines.push({ label: fill(T.l_cashils, { rate: f.rate }), value: ils(r.cashIls) });
          if (r.price33 != null && r.disp > 0) lines.push({ label: T.l_p33, value: ils(r.price33) });
        }
        if (r.warn.gap) lines.push({ label: T.l_value, value: ils(r.value) });
        lines.push({ label: fill(T.l_cap, { cap: capS }), value: ils(r.capLoan) });
        if (r.hasInc && r.disp > 0) { lines.push({ label: T.l_inc50, value: ils(r.inc50) }); lines.push({ label: T.l_inc33, value: ils(r.inc33) }); }
        lines.push({ label: fill(T.l_loan, { pct: pc(100 * r.loan / (r.value || 1), 1) }), value: ils(r.loan) });
        lines.push({ label: fill(T.l_first, { n: r.n }), value: both(r.first) });
        lines.push({ label: r.hasPrime ? T.l_up : r.hasFx ? T.l_upfx : T.l_up0, value: both(r.up1) });
        if (r.hasCpi) lines.push({ label: fill(T.l_year, { cpi: pc(+v.cpi, 1) }), value: both(r.year1) });
        if (r.hasInc && r.disp > 0) lines.push({ label: T.l_pti, value: pc(100 * r.pti, 1) });
        lines.push({ label: T.l_need, value: F(r.need50) + ' · ' + F(r.need33) });
        lines.push({ label: fill(T.l_tax, { track: trName }), value: ils(r.tax) });
        lines.push({ label: T.l_fees, value: ils(r.lawyer + r.appr + r.fee) });
        lines.push({ label: T.l_cash, value: both(r.cash) });
        lines.push({ label: T.l_int, value: ils(r.interest) });
        lines.push({ label: fill(T.l_fx, { cur: EN ? cur : curName(cur), rate: f.rate, date: date(f.date) }), value: f.min30 + ' / ' + f.max30 });
        // notes: the two rulebooks for this status, then the foreign currency loan, then the warnings
        var o = { cap: capS, br: br, date: date(vd), share: pc(+v.share, 1) }, nt = [];
        if (v.status === 'foreign') nt.push(fill(T.n_foreign, o));
        else if (v.status === 'oleh') nt.push(fill(T.n_oleh, o));
        else if (v.status === 'cit_own') nt.push(fill(T.n_cit_own, o));
        else if (v.status === 'mixed') { nt.push(fill(T.n_mixed, o)); nt.push(fill(v.live === 'israel' ? T.n_mixed_israel : T.n_mixed_abroad, o)); }
        else nt.push(fill(T['n_' + v.status + '_' + (v.live === 'israel' ? 'israel' : 'abroad')], o));
        if (r.hasFx) nt.push(fill(T.n_fx, { rate: pc(fxRate), mon: mon(N.fx_track.month, true), share: pc(N.fx_track.share, 1) }));
        var W = [];
        if (r.warn.over) W.push(fill(T.w_over, { cap: capS, x: ils(r.capLoan) }));
        if (r.warn.clipped) W.push(fill(T.w_clip, { cap: capS, ltv: pc(+v.ltv) }));
        if (r.hasInc && r.disp <= 0) W.push(T.w_pti0); else if (r.warn.pti) W.push(fill(T.w_pti, { p: pc(100 * r.pti, 1) })); else if (r.warn.pti40) W.push(T.w_pti40);
        if (r.warn.variable) W.push(fill(T.w_variable, { x: pc(100 * r.varShare, 1) }));
        if (r.warn.term) W.push(fill(T.w_term, { y: v.years }));
        if (r.warn.gap) W.push(fill(T.w_gap, { x: ils(r.price - r.value) }));
        var note = W.map(function (w) { return '<b>' + esc(T.w_head) + '</b> ' + esc(w); }).join('<br>') + (W.length ? '<br>' : '') + esc(nt.join(' '));
        // the drawing
        var figure;
        if (cashMode) {
          figure = figCash({ rtl: rtl, title: fill(T.g2_title, { price: ils(r.price) }), aria: fill(T.g2_title, { price: ils(r.price) }) + ': ' + T.g2_loan + ' ' + ils(r.loan) + ', ' + T.g2_tot + ' ' + ils(r.cash),
            segs: [{ label: T.g2_loan, v: r.loan, shown: ils(r.loan), fill: C.navy }, { label: T.g2_own, v: r.price - r.loan, shown: ils(r.price - r.loan), fill: C.teal },
              { label: T.g2_tax, v: r.tax, shown: ils(r.tax), fill: C.violet }, { label: T.g2_fees, v: r.lawyer + r.appr + r.fee, shown: ils(r.lawyer + r.appr + r.fee), fill: C.fee }],
            total: { label: T.g2_tot, shown: ils(r.cash) } });
        } else {
          var rows = [{ label: fill(T.g_cap, { cap: capS }), v: r.capLoan, shown: ils(r.capLoan), fill: C.navy, core: true }];
          if (r.hasInc && r.disp > 0) { rows.push({ label: T.g_inc50, v: r.inc50, shown: ils(r.inc50), fill: C.teal }); rows.push({ label: T.g_inc33, v: r.inc33, shown: ils(r.inc33), hatch: true }); }
          rows.push({ label: T.g_loan, v: r.loan, shown: ils(r.loan), fill: C.violet, core: true });
          figure = figLimits({ rtl: rtl, title: T.g_title, rows: rows, mark: r.maxLoan, foot: fill(T.g_foot, { x: ils(r.maxLoan) }),
            aria: T.g_title + ': ' + rows.map(function (x) { return x.label + ' ' + x.shown; }).join(', ') });
        }
        var tbl = [[T.t_price, ils(r.price), F(r.price)]];
        if (r.warn.gap) tbl.push([T.t_value, ils(r.value), F(r.value)]);
        tbl.push([T.t_loan, '−' + ils(r.loan), '−' + F(r.loan)], [T.t_tax + ' (' + trName + ')', ils(r.tax), F(r.tax)], [T.t_lawyer, ils(r.lawyer), F(r.lawyer)],
          [T.t_appr, ils(r.appr), F(r.appr)], [T.t_fee, ils(r.fee), F(r.fee)], [T.t_cash, ils(r.cash), F(r.cash)]);
        r.tracks.forEach(function (t) { tbl.push([fill(T.t_part, { track: rl(t.k), w: pc(100 * t.w, 1), rate: pc(t.rate) }), ils(t.m), F(t.m)]); });
        tbl.push([T.t_first, ils(r.first), F(r.first)]);
        var S = [src(N.ltv_source), src(N.ltv_qa), src(N.rates_source), src(N.prime_source)];
        if (r.hasFx) S.push(src(N.fx_rule));
        if (v.mix === 'b2' || v.mix === 'b3') S.push(src(N.baskets_source));
        if (r.hasCpi) S.push(src(N.forecast_source));
        S.push({ label: fill(T.src_fx, { date: date(f.date) }), url: FX.url });
        if (P.instruction) S.push({ label: EN ? T.src_tax : P.instruction.label, url: P.instruction.url });
        if ((tt === 'foreign' || tt === 'extra') && P.extension) S.push({ label: EN ? T.src_ext : P.extension.label, url: P.extension.url });
        var sw = r.swing, on = scen || 'now', sym = SYM[cur];
        var status = T.st[v.status] || '', out = {
          answer: answer, figure: figure,
          lines: lines, note: note,
          scenarioLabel: fill(T.sc_label, { cur: cur }),
          scenarios: [['weak', T.sc_weak, sw.weak], ['now', T.sc_now, sw.now], ['strong', T.sc_strong, sw.strong]].map(function (x) { return { key: x[0], name: x[1], value: sym + nf.format(Math.round(x[2])), on: on === x[0] }; }),
          table: { title: T.t_title, head: [T.t_item, '₪', cur], num: [1, 2], rows: tbl },
          formula: fill(T.formula, { vat: String(1 + N.vat) }),
          sources: S,
          text: cashMode ? fill(T.x_cash, { status: status, cfc: SYM[cur] + nf.format(Math.round(+v.cash)), price: ils(r.price), loan: ils(r.loan), m: ils(r.first), mfc: F(r.first) })
            : fill(T.x_borrow, { status: status, price: ils(r.price), max: ils(r.maxLoan), loan: ils(r.loan), y: v.years, m: ils(r.first), mfc: F(r.first), cash: ils(r.cash), cfc: F(r.cash) })
        };
        if (!cashMode) out.breakdown = [{ label: T.bd_down, value: r.price - r.loan, kind: 'housing' }, { label: T.bd_tax, value: r.tax, kind: 'survey' }, { label: T.bd_fees, value: r.lawyer + r.appr + r.fee, kind: 'civic' }];
        return out;
      }
    };
  }

  NI.register('nrm', { custom: function (root, data) { NI.mount(root, make(NI.langOf(root), data), data); } });
})();
