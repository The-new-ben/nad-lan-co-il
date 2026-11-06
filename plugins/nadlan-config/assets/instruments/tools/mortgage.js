/* NadLan Instruments · mortgage v1 "Mortgage 2.0" (U1, Ben 25.10.2026; spec: docs/research/2026-10-26-upgrades/u1-mortgage-calculator/
   dna.md 8.5.1 and 8.6). The mortgage calculator of /mortgage-calculator/, a custom surface on the instruments engine:
   - three ways in: by amount, by the monthly payment a household can carry (the loan is solved from the payment), by price and
     equity (the loan, the LTV cap of the buyer type, the equity needed);
   - up to 6 tracks (fixed not linked, fixed CPI-linked, prime, variable every 5 years linked or not, the state eligibility loan),
     each with its amount or share, its rate (opening at the official Bank of Israel average with its date), term 4 to 30 years,
     Spitzer, equal principal, balloon or bullet, and partial or full grace;
   - the CPI and the prime path as scenarios (the October 2026 Bank of Israel forecast, market expectations, +2%, a custom shock
     from a month), the old +1% / +2% check on every track, a future prepayment with the Banking Order fee estimate;
   - outputs: first and highest payment, totals of interest and CPI linkage, payment per shekel, balances after 5 and 10 years,
     payment to income with the three status texts of the old calculator and the 50% cap, LTV, plain-sentence rule checks of
     directive 329, three charts, a yearly schedule (monthly on request), up to 4 mixes side by side, a link that reopens the case;
   - THE MOAT, "ההצעה שלכם מול בנק ישראל": the bank's offer against the official averages for the same track and term (the
     average-by-term files are effective rates, converted to nominal), the gap in shekels over the loan and per month, and the
     loan placed among last month's new mortgages (payment to income, LTV, size, term), with its honest limits.
   Data: data/boi-mortgage.json (key "boim"), built by tools/instruments/build_boi_mortgage_data.py. Pure logic in NLMG for the
   cross-check tools/instruments/test_mortgage_math.py. Hebrew only (RTL); no em or en dash in any visible string.
   v2 (round M, HAD-675, 6.11.2026): six additions from the competitor delta (docs/research/2026-11-06-mortgage-delta/delta.md,
   section c), all additive; with the new controls untouched every payment, total and text of v1 is the same:
   - C1 under each rate field, the lowest and highest of the 7 banks for that track in the latest month of by_bank (Bank of
     Israel "קו המשווה", effective rates shown nominal like every other rate here, and as published); only for the 5 tracks
     by_bank covers (NLMG.band);
   - C2 a change frequency on the variable tracks (every 1, 2, 2.5, 5 or 10 years; 5 as before): the reset path of the scenario
     (the +2% or your own shock) reaches the track only at those months, the moat reference and the Banking Order fee follow it;
   - C3 the term in years or in months (48 to 360), exact to the month (the math was already monthly);
   - C5 "הורדת לוח הסילוקין (CSV)": one row per month, per track and total, UTF-8 with BOM, built in the browser (NLMG.csv);
   - C9 three scenarios side by side in the results: today, the Bank of Israel forecast, and the existing +2% stress;
   - C14 one tap "הסלים האחידים לסכום שלי": the three uniform baskets of directive 451 on your amount and term, beside your mix
     (the file's own basket(), the same rows as NLMR.basketRows of tools/mrates-common.js). Test: build-mortgage-v2/. */
(function () {
  'use strict';

  /* =========================================================================================================== the math */
  function pmt(B, rm, n) { if (n <= 0) return B; return rm === 0 ? B / n : B * rm / (1 - Math.pow(1 + rm, -n)); }
  function solveN(B, rm, P) { if (B <= 0) return 0; if (rm === 0) return Math.ceil(B / P); var x = 1 - B * rm / P; return x > 0 ? Math.ceil(-Math.log(x) / Math.log(1 + rm) - 1e-9) : Infinity; }

  /* One scenario: cpi (annual %), prime(m) and reset(m) (points added to the prime track in month m and to a variable-every-5
     track at a reset in month m), all (points on every track from month 1: the old "+2%" check). */
  function scenario(o) {
    o = o || {};
    var kind = o.prime || 'none', to = o.rampTo || 0, months = Math.max(1, o.rampMonths || 1), sh = +o.shock || 0, from = Math.max(1, Math.round(+o.shockMonth || 1));
    return {
      cpi: +o.cpi || 0, all: +o.all || 0,
      prime: function (m) {
        if (kind === 'boi' || kind === 'market') return to * Math.min(1, m / months);
        if (kind === 'up2') return 2;
        if (kind === 'custom') return m >= from ? sh : 0;
        return 0;
      },
      reset: function (m) { if (kind === 'up2') return 2; if (kind === 'custom') return m >= from ? sh : 0; return 0; }
    };
  }

  /* One track, month by month. t: amount, rate (annual nominal %), years, method (spitzer | equal | balloon | bullet), grace
     (months, inside the term), graceType (partial: interest only | full: nothing paid, interest added), kind (fixed | prime |
     var5), linked (CPI), prepay {month, amount, mode: shorten | reduce} or null.
     A linked balance is indexed every month by the scenario CPI and the payment is recomputed on the indexed balance.
     v2: freq (months between rate changes of a var5 track: 12, 24, 30, 60 or 120; missing = 60, the v1 behaviour). */
  function freqOf(t) { var q = Math.round(+t.freq || 0); return q >= 1 ? q : 60; }
  function track(t, sc) {
    var N = Math.max(1, Math.round((+t.years || 0) * 12)), g = Math.min(Math.max(0, Math.round(+t.grace || 0)), N - 1), FQ = freqOf(t);
    var f = t.linked ? Math.pow(1 + (sc.cpi || 0) / 100, 1 / 12) : 1;
    var B = Math.max(0, +t.amount || 0), C = 0, end = N, r = +t.rate || 0;
    var S = { N: N, pay: [], reg: [], intr: [], prin: [], link: [], bal: [], rate: [], lump: 0, lumpMonth: 0, prepay: null, end: N, sumI: 0, sumL: 0, sumP: 0 };
    for (var m = 1; m <= N; m++) {
      if (B <= 0.005 || m > end) { S.pay.push(0); S.reg.push(0); S.intr.push(0); S.prin.push(0); S.link.push(0); S.bal.push(0); S.rate.push(r); continue; }
      if (t.kind === 'prime') r = t.rate + sc.all + sc.prime(m);
      else if (t.kind === 'var5') { if (m === 1) r = t.rate + sc.all; else if ((m - 1) % FQ === 0) r = t.rate + sc.all + sc.reset(m); }
      else r = t.rate + sc.all;
      var L = B * (f - 1); B += L; C *= f;
      var rm = Math.max(0, r) / 1200, I = B * rm, n = end - m + 1, P, lump = 0;
      if (m <= g) P = t.graceType === 'full' ? 0 : I;
      else if (t.method === 'equal') P = I + B / n;
      else if (t.method === 'bullet') { P = I; if (n === 1) { P = I + B; lump = B; } }
      else if (t.method === 'balloon') { P = 0; if (n === 1) { P = B + I; lump = P; } }
      else P = pmt(B, rm, n);
      var ip, pp;
      if (P < I) { ip = P; C += I - P; pp = 0; } else { var x = Math.min(C, P - I); ip = I + x; C -= x; pp = P - ip; }
      B = B + I - P; if (B < 0.005) B = 0;
      S.sumI += I; S.sumL += L; S.sumP += P;
      if (lump) { S.lump = lump; S.lumpMonth = m; }
      if (t.prepay && m === Math.round(t.prepay.month) && B > 0 && t.prepay.amount > 0) {
        var a = Math.min(+t.prepay.amount, B), share = a / B;
        S.prepay = { month: m, amount: a, before: B, rate: r, share: share, endBefore: end, payBefore: P };
        C -= C * share; B -= a; if (B < 0.005) B = 0;
        if (t.prepay.mode === 'shorten' && m > g && B > 0) {
          if (t.method === 'equal') { var q = P - I; if (q > 0) end = Math.min(end, m + Math.ceil(B / q - 1e-9)); }
          else if (t.method !== 'bullet' && t.method !== 'balloon') { var k = solveN(B, rm, P); if (isFinite(k)) end = Math.min(end, m + k); }
        }
        S.prepay.endAfter = end;
      }
      S.pay.push(P); S.reg.push(P - lump); S.intr.push(I); S.prin.push(P - I); S.link.push(L); S.bal.push(B); S.rate.push(r);
    }
    S.end = end;
    return S;
  }

  /* The whole mix: monthly sums, the first and the highest payment, totals, balances, years. */
  function mix(rows, sc) {
    var T = rows.map(function (t) { return track(t, sc); });
    var N = T.reduce(function (a, s) { return Math.max(a, s.N); }, 0), pay = [], reg = [], bal = [], intr = [], prin = [], link = [];
    for (var i = 0; i < N; i++) {
      var p = 0, g = 0, b = 0, ii = 0, pr = 0, l = 0;
      T.forEach(function (s) { if (i < s.N) { p += s.pay[i]; g += s.reg[i]; b += s.bal[i]; ii += s.intr[i]; pr += s.prin[i]; l += s.link[i]; } });
      pay.push(p); reg.push(g); bal.push(b); intr.push(ii); prin.push(pr); link.push(l);
    }
    var hi = 0, hm = 0; for (var j = 0; j < N; j++) if (reg[j] > hi + 1e-9) { hi = reg[j]; hm = j + 1; }
    var loan = rows.reduce(function (a, t) { return a + (+t.amount || 0); }, 0);
    var pre = T.reduce(function (a, s) { return a + (s.prepay ? s.prepay.amount : 0); }, 0);
    var totI = T.reduce(function (a, s) { return a + s.sumI; }, 0), totL = T.reduce(function (a, s) { return a + s.sumL; }, 0), totP = T.reduce(function (a, s) { return a + s.sumP; }, 0) + pre;
    var years = [];
    for (var y = 0; y * 12 < N; y++) {
      var yr = { y: y + 1, mc: Math.min(N, (y + 1) * 12) - y * 12, pay: 0, reg: 0, intr: 0, prin: 0, link: 0, bal: bal[Math.min(N, (y + 1) * 12) - 1], byTrack: T.map(function () { return 0; }) };
      for (var m = y * 12; m < Math.min(N, (y + 1) * 12); m++) { yr.pay += pay[m]; yr.reg += reg[m]; yr.intr += intr[m]; yr.prin += prin[m]; yr.link += link[m]; T.forEach(function (s, k) { if (m < s.N) yr.byTrack[k] += s.reg[m]; }); }
      years.push(yr);
    }
    return { T: T, N: N, pay: pay, reg: reg, bal: bal, intr: intr, prin: prin, link: link, loan: loan, first: pay[0] || 0, firstBy: T.map(function (s) { return s.pay[0] || 0; }),
      highest: hi, highestMonth: hm, totalPaid: totP, totalInterest: totI, totalLinkage: totL, prepaid: pre, perShekel: loan > 0 ? totP / loan : 0,
      bal60: N >= 60 ? bal[59] : 0, bal120: N >= 120 ? bal[119] : 0, years: years,
      lumps: T.map(function (s, k) { return s.lump ? { k: k, amount: s.lump, month: s.lumpMonth } : null; }).filter(Boolean) };
  }

  /* payment -> loan: every amount in the mix scales with the loan, so the loan that gives a payment is one division */
  function solveLoan(rows, shares, sc, target, basis) {
    var unit = 1000000, tot = shares.reduce(function (a, b) { return a + b; }, 0) || 1;
    var probe = mix(rows.map(function (t, i) { return Object.assign({}, t, { amount: unit * shares[i] / tot, prepay: null }); }), sc);
    var per = basis === 'max' ? probe.highest : probe.first;
    return per > 0 ? target * unit / per : NaN;
  }

  function ef2nom(e) { return 1200 * (Math.pow(1 + e / 100, 1 / 12) - 1); }
  function bucket(list, years) { for (var i = 0; i < list.length; i++) { var b = list[i]; if (years <= (b.to == null ? 1e9 : b.to) && (i === 0 || years > b.from)) return b; } return list[list.length - 1]; }
  function pv(stream, annual) { var q = 1 + annual / 1200, s = 0; for (var i = 0; i < stream.length; i++) s += stream[i] / Math.pow(q, i + 1); return s; }
  /* the future payments of what is left (no further CPI: the Order discounts real payments at real rates on a linked loan), up to
     h months; the balance left at month h is the last payment (a variable track: the balance on the day the rate changes) */
  function stream(B, annual, nLeft, h, method) {
    var rm = annual / 1200, out = [], b = B;
    for (var i = 1; i <= h; i++) {
      var n = nLeft - i + 1, I = b * rm, P;
      if (method === 'equal') P = I + b / n; else if (method === 'bullet') P = n === 1 ? I + b : I; else if (method === 'balloon') P = n === 1 ? b + I : 0; else P = pmt(b, rm, n);
      b = b + I - P; if (i === h && b > 0.005) P += b;
      out.push(P);
    }
    return out;
  }
  /* The Banking Order (early repayment of a housing loan, 2002): operational fee up to 60, 0.1% for under 10 days notice, half
     the average monthly CPI change on a linked loan repaid on the 1st to 15th, and the capitalization fee: on a fixed rate (or a
     variable one until its change day) when the average rate on the day is below the loan rate, the lower of the two formulas,
     cut by 20% after 3 years and 30% after 5; none when the rate changes at least yearly (prime) and none on a directed loan.
     The average on the prepayment day is unknown today: the estimate takes today's average for the same remaining period
     (from the average-by-term file), and "drop" points lower for the second line. */
  function prepayFee(t, P, D, drop) {
    var F = D.fees, out = { op: F.operational_max, notice: P.amount * F.notice_rate, cpi: 0, cap: 0, none: false, why: '' };
    if (t.directed) { out.op = 0; out.notice = 0; out.none = true; out.why = 'directed'; return out; }
    if (t.linked && D.cpi.avg_m12 != null) out.cpi = P.amount * D.cpi.avg_m12 / 100 / 2;
    if (t.kind === 'prime') { out.why = 'prime'; return out; }
    var left = P.endBefore - P.month, h = left, FQ = freqOf(t);
    if (t.kind === 'var5' && FQ !== 60 && FQ <= (F.no_cap_fee_if_change_within_months || 12)) { out.why = 'prime'; return out; }  // v2: a rate that changes at least yearly
    if (t.kind === 'var5') { var next = FQ * Math.ceil(P.month / FQ) + 1; h = Math.min(left, next - 1 - P.month); if (h <= 0) { out.why = 'reset'; return out; } }
    if (left <= 0) return out;
    var file = t.linked ? 'cpi' : 'nl', b = bucket(D.term[file].buckets, h / 12), C = b.nom, A = C - (drop || 0), R = P.rate;
    var s = stream(P.before, R, left, h, t.method), pvA = pv(s, A), pvC = pv(s, C);
    var f3 = A < R ? Math.max(0, pvA - P.before) : 0, f4 = C < R ? Math.max(0, pvA - pvC) : null;
    var cap = f4 === null ? f3 : Math.min(f3, f4), yrs = P.month / 12, cut = 0;
    (F.reduce || []).forEach(function (x) { if (yrs >= x.after_years) cut = x.cut; });
    out.cap = cap * (1 - cut) * P.share; out.cut = cut; out.avg = C; out.bucket = b;
    return out;
  }

  /* ----------------------------------------------------------------------------------------------- v2 helpers (pure) */
  /* C1: the lowest and the highest of the banks in the Bank of Israel comparison by bank (by_bank, TamInt010.xls, latest month,
     the "system" row left out) for a track of this file; null when the data has no by_bank or the track is not one of its five
     (the eligibility loan). The file's rates are effective; nom is the nominal rate of a monthly payment (ef2nom). */
  var BBK = { fixed_nl: 'fixed_nl', fixed_cpi: 'fixed_cpi', prime: 'prime', var5_cpi: 'var_cpi', var5_nl: 'var_nl_other' };
  var HEMON = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
  function monthHe(key) { var p = String(key || '').split('-'); return p.length > 1 && HEMON[+p[1] - 1] ? HEMON[+p[1] - 1] + ' ' + p[0] : String(key || ''); }
  function band(D, trackKey) {
    var BB = D && D.by_bank, k = BBK[trackKey];
    if (!k || !BB || !BB.latest || !Array.isArray(BB.latest.table)) return null;
    var he = {}; (BB.banks || []).forEach(function (b) { he[b.k] = b.he; });
    var rows = BB.latest.table.filter(function (x) { return x.bank !== 'system' && x[k] && isFinite(x[k].rate) && x[k].rate > 0; });
    if (rows.length < 2) return null;
    var lo = rows[0], hi = rows[0];
    rows.forEach(function (x) { if (x[k].rate < lo[k].rate) lo = x; if (x[k].rate > hi[k].rate) hi = x; });
    function one(x) { return { bank: x.bank, he: he[x.bank] || x.bank, eff: x[k].rate, nom: ef2nom(x[k].rate) }; }
    return { month: BB.latest.month, key: k, n: rows.length, min: one(lo), max: one(hi) };
  }
  /* C5: the monthly schedule of a mix() result as CSV text, UTF-8 with BOM (so Excel opens the Hebrew), comma separated, CRLF.
     One row per month; per track and for the whole loan: the payment, the principal (the payment less the interest; below zero in
     a full grace or a balloon month, when the interest joins the balance), the interest, the CPI linkage added to the balance in
     that month, and the balance at the end of the month. A prepayment is not a payment here; the balance already includes it. */
  var CSVCOL = ['תשלום', 'קרן', 'ריבית', 'הצמדה', 'יתרה'];
  function csvCell(s) { s = String(s); return /[",\r\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
  function csv(R, names) {
    function f2(x) { var y = Math.round((+x || 0) * 100) / 100; return (y === 0 ? 0 : y).toFixed(2); }
    var head = ['חודש'];
    R.T.forEach(function (s, k) { var n = names && names[k] ? names[k] : 'מסלול ' + (k + 1); CSVCOL.forEach(function (c) { head.push(n + ': ' + c); }); });
    CSVCOL.forEach(function (c) { head.push('סך הכול: ' + c); });
    var out = [head.map(csvCell).join(',')];
    for (var m = 0; m < R.N; m++) {
      var row = [String(m + 1)];
      R.T.forEach(function (s) { var i = m < s.N; row.push(f2(i ? s.pay[m] : 0), f2(i ? s.prin[m] : 0), f2(i ? s.intr[m] : 0), f2(i ? s.link[m] : 0), f2(i ? s.bal[m] : 0)); });
      row.push(f2(R.pay[m]), f2(R.prin[m]), f2(R.intr[m]), f2(R.link[m]), f2(R.bal[m]));
      out.push(row.join(','));
    }
    return '\uFEFF' + out.join('\r\n') + '\r\n';
  }
  /* C9: three scenarios on the same rows. o = the scenario options of the page (cpi, prime, rampTo, rampMonths, shock, shockMonth).
     today: the rates do not move (no prime path, no shock), the CPI as chosen; boi: the Bank of Israel forecast in the data, the
     policy rate to forecast.rate_q3_2027 on the prime track by the middle of Q3 2027 (the ramp of the page) and the CPI at
     forecast.inflation_4q; stress: the tool's own +2% check of v1 (scen({all: 2}): 2 points on every track from month 1, on the
     chosen path and CPI). */
  function three(rows, D, o) {
    o = o || {}; var FC = D.forecast, POL = D.policy;
    return {
      today: mix(rows, scenario(Object.assign({}, o, { prime: 'none', all: 0 }))),
      boi: mix(rows, scenario({ cpi: FC.inflation_4q, prime: 'boi', rampTo: FC.rate_q3_2027 - POL.rate, rampMonths: o.rampMonths || 1 })),
      stress: mix(rows, scenario(Object.assign({}, o, { all: 2 })))
    };
  }
  /* C14: the three uniform baskets of directive 451 (D.baskets.list, Spitzer, one term for every track) on a loan and a term, each
     track at rateOf(track) (this file's track names; the average of the data when rateOf is missing). The amount of a track is
     loan x its share, as NLMR.mathRows(NLMR.basketRows(...)) of tools/mrates-common.js builds them for mexit. */
  function baskets(D, loan, years, rateOf, sc) {
    var TR = D.tracks || {};
    return ((D.baskets && D.baskets.list) || []).map(function (b) {
      var rows = b.mix.map(function (x) { var T = TR[x[0]] || {}, r = rateOf ? rateOf(x[0]) : T.rate;
        return { track: x[0], amount: loan * x[1], rate: isFinite(r) ? +r : +T.rate, years: years, method: 'spitzer', grace: 0, graceType: 'partial', kind: T.kind, linked: !!T.linked, directed: !!T.directed }; });
      return { k: b.k, label: b.label, mix: b.mix, rows: rows, R: mix(rows, sc || scenario({})) };
    });
  }

  window.NLMG = { pmt: pmt, scenario: scenario, track: track, mix: mix, solveLoan: solveLoan, ef2nom: ef2nom, bucket: bucket, prepayFee: prepayFee, stream: stream, pv: pv,
    freqOf: freqOf, band: band, monthHe: monthHe, csv: csv, three: three, baskets: baskets };  // v2: the last six
  if (!window.NadLanInstruments) return;

  /* ============================================================================================================== the page */
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  var nf0 = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function ils(n) { return F.ils(n); }
  function pc(n, d) { return F.num(n, d == null ? 2 : d) + '%'; }
  function num(v) { var n = parseFloat(String(v == null ? '' : v).replace(/[^\d.\-]/g, '')); return isFinite(n) ? n : NaN; }
  function mon(key) { return F.month(key); }
  function day(iso) { return F.date(iso); }
  function yearsOf(m) { if (!(m >= 1)) return 'בלי החזר חודשי'; var y = Math.floor((m - 1) / 12) + 1, mm = (m - 1) % 12 + 1; return 'שנה ' + y + (mm > 1 ? ', חודש ' + mm : ''); }
  var COL = ['#2F6F86', '#1F4B5C', '#4F9A5C', '#7FA9B8', '#5E6A75', '#12202A'];  // 26.10.2026: sea, deep, open, light sea, slate, ink; red stays for warnings, no mustard (design law 13.10)
  var TRACKS = ['fixed_nl', 'fixed_cpi', 'prime', 'var5_cpi', 'var5_nl', 'zakaut'];
  var TNAME = { fixed_nl: 'קל״צ: קבועה לא צמודה', fixed_cpi: 'ק״צ: קבועה צמודה למדד', prime: 'פריים', var5_cpi: 'משתנה כל 5 שנים, צמודה', var5_nl: 'משתנה כל 5 שנים, לא צמודה', zakaut: 'הלוואת זכאות' };
  var FREQS = [['12', 'כל שנה'], ['24', 'כל שנתיים'], ['30', 'כל 2.5 שנים'], ['60', 'כל 5 שנים'], ['120', 'כל 10 שנים']];  // v2 (C2)
  function freqLabel(q) { var f = FREQS.filter(function (x) { return +x[0] === q; })[0]; return f ? f[1] : 'כל ' + F.num(q / 12, q % 12 ? 1 : 0) + ' שנים'; }
  function isVar(r) { return /^var5_/.test(r.track); }
  function offFreq(r) { return isVar(r) && freqOf(r) !== 60; }  // a variable track on a frequency the user chose (not the v1 five years)
  function tn(r) { var n = TNAME[r.track]; return n && offFreq(r) ? n.replace('כל 5 שנים', freqLabel(freqOf(r))) : n; }  // v2: the name follows the frequency
  var METHODS = [['spitzer', 'שפיצר'], ['equal', 'קרן שווה'], ['balloon', 'בלון'], ['bullet', 'בוליט']];
  var BUYER = [['single', 'דירה יחידה'], ['replace', 'דירה חליפית'], ['invest', 'דירה להשקעה'], ['reduced', 'דירה במחיר מופחת']];
  var MODES = [['amount', 'לפי סכום'], ['payment', 'לפי החזר חודשי'], ['price', 'לפי מחיר והון עצמי']];
  var OLD = {  // the old simple calculator's status texts (nmc), kept word for word (additive law)
    hi: 'יחס ההחזר גבוה לפי הנתונים שהוזנו. כדאי לבדוק סכום נמוך יותר, תקופה אחרת או מרווח ביטחון גדול יותר.',
    mid: 'יחס ההחזר בינוני-גבוה. בדקו תרחיש ריבית גבוה יותר והוצאות חיים לפני החלטה.',
    lo: 'יחס ההחזר נראה מתון לפי הנתונים שהוזנו, אך עדיין צריך לבדוק תמהיל, ביטוחים ועלויות רכישה.'
  };

  function css() {
    if (document.getElementById('nlm-css')) return;
    var s = document.createElement('style'); s.id = 'nlm-css';
    s.textContent = [
      '.nlm .nlm__sec{margin:28px 0 0;padding:20px 0 0;border-top:1px solid var(--nli-line);position:relative}',
      'html body .nli .nlm h3.nlm__h{font:600 22px/28px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 6px !important;letter-spacing:0;text-transform:none}',
      'html body .nli .nlm h4.nlm__h4{font:600 15px/22px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 8px !important}',
      '.nlm__p{font:400 15px/24px var(--nli-sans);color:var(--nli-ink2);margin:0 0 12px;max-width:72ch}',
      '.nlm__grid{display:grid;grid-template-columns:minmax(0,1fr);gap:20px;position:relative}',
      '@media (min-width:1000px){.nlm__grid{grid-template-columns:minmax(0,520px) minmax(0,1fr);gap:32px}}',
      '.nlm__live{position:sticky;top:var(--nlm-top,0px);z-index:3;margin:0 -4px;padding:10px 12px;background:#12202A;color:#fff;border-radius:var(--nli-r-s);display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 14px;box-shadow:0 2px 0 rgba(18,32,42,.08)}',
      '.nlm__live div{display:grid;gap:0}.nlm__live span{font:400 12px/16px var(--nli-sans);color:#C9D6DE}.nlm__live strong{font:500 20px/24px var(--nli-mono);color:#fff;direction:ltr;unicode-bidi:plaintext;text-align:right}',
      'html body .nli .nlm .nli__pre small{font-family:var(--nli-sans);direction:rtl;text-align:right}',
      'html body .nli .nlm__live a{margin-inline-start:auto;color:#fff !important;font:500 13px/18px var(--nli-sans);text-decoration:underline;text-underline-offset:3px;min-height:32px;display:inline-flex;align-items:center}',
      'html body .nli .nlm .nli__lines dd,html body .nli .nlm table.nlm__t td.n{font-family:"IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace !important}',
      'html body .nli .nlm .nli__lines dd{white-space:normal;max-width:52%;overflow-wrap:anywhere}html body .nli .nlm .nli__lines dt{min-width:0}',
      'html body .nli .nlm table.nlm__t td.r bdi{display:block;font:500 13px/18px "IBM Plex Mono",ui-monospace,monospace;direction:ltr;text-align:right}',
      '@media (max-width:600px){html body .nli .nlm .nli__strip{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}}',
      'html body .nli .nlm .nlm__sched td.n{text-align:right !important}',
      '.nlm__rows{display:grid;gap:12px}',
      '.nlm__row{border:1px solid var(--nli-line);border-inline-start:4px solid var(--c,#2F6F86);border-radius:var(--nli-r-s);padding:12px;background:var(--nli-surface);display:grid;gap:10px}',
      '.nlm__rh{display:flex;gap:8px;align-items:center}',
      '.nlm__rh .nli__in{flex:1}',
      'html body .nli .nlm__rh button{min-height:44px;min-width:44px;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);color:var(--nli-ink2);cursor:pointer;font:400 18px/1 var(--nli-sans);margin:0;padding:0}',
      '.nlm__rg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 10px}',
      '@media (min-width:560px){.nlm__rg{grid-template-columns:repeat(3,minmax(0,1fr))}}',
      '.nlm__rg .nli__f{gap:4px}.nlm__rg label{font:500 12px/16px var(--nli-sans) !important;color:var(--nli-ink2) !important}',
      'html body .nli .nlm__rg .nli__in{min-height:44px}html body .nli .nlm__rg .nli__in input,html body .nli .nlm__rg .nli__in select{font-size:16px;padding:9px 10px}',
      '.nlm__hint{font:400 12px/17px var(--nli-sans);color:var(--nli-mute);margin:0}.nlm__hint b{font-weight:500;color:var(--nli-ink2)}',
      '.nlm__sum{font:500 14px/20px var(--nli-sans);color:var(--nli-ink);margin:0}.nlm__sum bdi{font-family:var(--nli-mono)}',
      '.nlm__box{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);padding:12px;display:grid;gap:12px;background:var(--nli-ground)}',
      '.nlm__two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px 10px}',
      'html body .nli .nlm details.nlm__more>summary{font:500 15px/22px var(--nli-sans);color:var(--nli-sea);cursor:pointer;min-height:44px;display:flex;align-items:center;border:0 !important;padding:0 !important;background:none !important}',
      '.nlm__chk{display:flex;gap:8px;align-items:center;font:400 14px/20px var(--nli-sans);color:var(--nli-ink2);min-height:44px}.nlm__chk input{width:20px;height:20px;margin:0}',
      '.nlm__rules{list-style:none;margin:0;padding:0;display:grid;gap:8px}',
      '.nlm__rules li{font:400 14px/21px var(--nli-sans);color:var(--nli-ink2);padding:8px 10px;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:start;margin:0}',
      '.nlm__rules li b{font:600 11px/16px var(--nli-sans);letter-spacing:.04em;padding:2px 8px;border-radius:999px;white-space:nowrap;background:#E3EEF2;color:#1F4B5C}',
      '.nlm__rules li.is-bad{border-color:#C42550;background:#FCF1F4}.nlm__rules li.is-bad b{background:#C42550;color:#fff}',
      '.nlm__rules li.is-warn b{background:#12202A;color:#fff}',
      '.nlm__charts{display:grid;gap:16px}@media (min-width:1000px){.nlm__charts{grid-template-columns:repeat(3,minmax(0,1fr))}}',
      '.nlm__chart{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);padding:12px;background:var(--nli-surface);min-width:0}',
      '.nlm__chart svg{display:block;width:100%;height:auto;direction:ltr}',
      '.nlm__chart svg text{font:400 11px var(--nli-mono);fill:#5E6A75}',
      '.nlm__chart figcaption{font:400 12px/18px var(--nli-sans);color:var(--nli-mute);margin:6px 0 0}',
      '.nlm__lg{display:flex;flex-wrap:wrap;gap:4px 12px;list-style:none;margin:6px 0 0;padding:0;font:400 12px/16px var(--nli-sans);color:var(--nli-ink2)}.nlm__lg li{margin:0;display:flex;gap:6px;align-items:center}.nlm__lg i{width:10px;height:10px;border-radius:2px;display:inline-block}',
      '.nlm__tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--nli-line);border-radius:var(--nli-r-s)}',
      'html body .nli .nlm table.nlm__t{width:100%;border-collapse:collapse;margin:0;display:table !important;font:400 14px/20px var(--nli-sans)}',
      'html body .nli .nlm table.nlm__t th,html body .nli .nlm table.nlm__t td{display:table-cell !important;padding:8px 8px !important;border:0 !important;border-bottom:1px solid var(--nli-line) !important;text-align:right;vertical-align:middle;background:none !important;color:var(--nli-ink);font-size:14px !important;width:auto !important;white-space:nowrap}',
      'html body .nli .nlm table.nlm__t th{font-weight:500;color:var(--nli-mute);font-size:12px !important;white-space:normal}',
      'html body .nli .nlm table.nlm__t td.n{font-family:var(--nli-mono) !important;font-size:13px !important;direction:ltr;unicode-bidi:plaintext;text-align:right;font-variant-numeric:tabular-nums}',
      'html body .nli .nlm table.nlm__t td small{display:block;font:400 11px/15px var(--nli-sans);color:var(--nli-mute);direction:rtl;text-align:right;white-space:normal;max-width:180px}',
      'html body .nli .nlm table.nlm__t tr.is-sum td{font-weight:600;background:var(--nli-ground) !important}',
      'html body .nli .nlm table.nlm__t td.pos{color:#A01D44}html body .nli .nlm table.nlm__t td.neg{color:#2E6B43}',
      'html body .nli .nlm table.nlm__t input{width:84px;min-height:40px;border:1px solid var(--nli-line) !important;border-radius:var(--nli-r-s);font:500 15px/20px var(--nli-mono);padding:6px 8px;direction:ltr;text-align:right;background:#fff !important;margin:0;box-shadow:none !important}',
      '@media (max-width:700px){html body .nli .nlm table.nlm__t.is-cards thead{display:none !important}html body .nli .nlm table.nlm__t.is-cards,html body .nli .nlm table.nlm__t.is-cards tbody{display:block !important}html body .nli .nlm table.nlm__t.is-cards tr{display:grid !important;grid-template-columns:1fr 1fr;gap:2px 10px;padding:10px 0;border-bottom:1px solid var(--nli-line)}html body .nli .nlm table.nlm__t.is-cards td{display:block !important;border:0 !important;padding:2px 8px !important;white-space:normal;text-align:right !important}html body .nli .nlm table.nlm__t.is-cards td[data-l]::before{content:attr(data-l);display:block;font:500 11px/15px var(--nli-sans);color:var(--nli-mute);direction:rtl}html body .nli .nlm table.nlm__t.is-cards td:first-child{grid-column:1/-1;font-weight:600}}',
      '.nlm__verdict{font:500 17px/26px var(--nli-sans);color:var(--nli-ink);margin:12px 0;padding:14px 16px;border:1px solid var(--nli-line);border-inline-start:4px solid #2F6F86;border-radius:var(--nli-r-s);background:var(--nli-ground)}',
      '.nlm__verdict.is-high{border-inline-start-color:#C42550}.nlm__verdict.is-low{border-inline-start-color:#4F9A5C}',
      '.nlm__verdict bdi{font-family:var(--nli-mono);font-weight:500}',
      '.nlm__place{display:grid;gap:12px}@media (min-width:860px){.nlm__place{grid-template-columns:repeat(2,minmax(0,1fr))}}',
      '.nlm__pc{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);padding:12px;background:var(--nli-surface);min-width:0}',
      '.nlm__pc p{font:400 14px/21px var(--nli-sans);color:var(--nli-ink2);margin:6px 0 0}.nlm__pc p b{font-weight:600;color:var(--nli-ink)}',
      '.nlm__pc svg{display:block;width:100%;height:auto;direction:ltr}.nlm__pc svg text{font:400 10px var(--nli-mono);fill:#5E6A75}',
      '.nlm__limits{font:400 13px/20px var(--nli-sans);color:var(--nli-mute);margin:12px 0 0}',
      '.nlm__btns{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}',
      'html body .nli .nlm__btns button{min-height:44px;padding:10px 14px;border:1px solid var(--nli-sea);border-radius:999px;background:var(--nli-surface);color:var(--nli-sea);font:500 14px/20px var(--nli-sans);cursor:pointer;margin:0}',
      'html body .nli .nlm__btns button.is-solid{background:var(--nli-sea);color:#fff}',
      'html body .nli .nlm__btns button[disabled]{opacity:.45;cursor:default}',
      'html body .nli .nlm .nlm__x{min-height:32px;min-width:32px;border:1px solid var(--nli-line);border-radius:999px;background:#fff;color:var(--nli-ink2);cursor:pointer;margin:0 6px 0 0;padding:0 8px;font:400 13px/1 var(--nli-sans)}',
      'html body .nli .nlm .nli__table summary{font:500 15px/22px var(--nli-sans);color:var(--nli-sea)}',
      'html body .nli .nlm button.nlm__link{border:0;background:none;color:var(--nli-sea);text-decoration:underline;text-underline-offset:3px;font:500 14px/20px var(--nli-sans);cursor:pointer;padding:8px 0;min-height:44px;margin:0}',
      '.nlm__stress{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}',
      '.nlm__stress div{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);padding:10px 12px;background:var(--nli-surface)}',
      '.nlm__stress span{display:block;font:500 12px/16px var(--nli-sans);color:var(--nli-ink2)}.nlm__stress strong{display:block;font:500 17px/22px var(--nli-mono);color:var(--nli-ink);direction:ltr;unicode-bidi:plaintext;text-align:right}',
      '.nlm__stress small{display:block;font:400 12px/16px var(--nli-sans);color:var(--nli-mute)}',
      '.nlm__status{font:400 14px/22px var(--nli-sans);color:var(--nli-ink2);margin:0;padding:12px;border-inline-start:3px solid var(--nli-sea);background:var(--nli-ground)}',
      '.nlm__status.is-mid{border-inline-start-color:#12202A}.nlm__status.is-hi{border-inline-start-color:#C42550}',
      /* v2 (round M): the bank band under the rate (C1), the three scenarios (C9), the uniform baskets for my amount (C14) */
      '.nlm__rg{grid-auto-flow:row dense}',
      'html body .nli .nlm p.nlm__band{grid-column:1/-1;margin:-2px 0 2px !important;font:400 12px/18px var(--nli-sans) !important;color:var(--nli-mute) !important;max-width:none}',
      '.nlm__band bdi{font:500 12px/18px var(--nli-mono);color:var(--nli-ink)}.nlm__band b{font-weight:500;color:var(--nli-ink2)}',
      '.nlm__s3,.nlm__s4{display:grid;gap:8px;margin:0 0 12px}.nlm__s3{grid-template-columns:repeat(3,minmax(0,1fr))}.nlm__s4{grid-template-columns:repeat(2,minmax(0,1fr))}',
      '@media (min-width:1000px){.nlm__s4{grid-template-columns:repeat(4,minmax(0,1fr))}}',
      '.nlm__sc{border:1px solid var(--nli-line);border-top:3px solid #2F6F86;border-radius:var(--nli-r-s);padding:10px 10px 8px;background:var(--nli-surface);min-width:0;display:grid;gap:6px;align-content:start;grid-row:span 5;grid-template-rows:subgrid}',  // the five lines of every card on the same rows
      '@media (max-width:599px){.nlm__s3 .nlm__sc{padding:8px 6px 6px}.nlm__s3 .nlm__sc .nlm__scr strong{font-size:clamp(11px,3.3vw,14px);letter-spacing:-.02em;white-space:nowrap;overflow-wrap:normal}}',
      '.nlm__sc.is-me{border-top-color:#12202A;background:var(--nli-ground)}.nlm__sc.is-hard{border-top-color:#C42550}.nlm__sc.is-fc{border-top-color:#1F4B5C}',
      '.nlm__sc .nlm__sct{display:block;font:600 14px/19px var(--nli-sans);color:var(--nli-ink)}',
      '.nlm__sc .nlm__scs{display:block;font:400 11px/15px var(--nli-sans);color:var(--nli-mute)}',
      '.nlm__sc .nlm__scr{display:grid;gap:0;border-top:1px solid var(--nli-line);padding-top:5px}',
      '.nlm__sc .nlm__scr span{font:400 11px/15px var(--nli-sans);color:var(--nli-ink2)}',
      '.nlm__sc .nlm__scr strong{font:500 14px/19px var(--nli-mono);color:var(--nli-ink);direction:ltr;unicode-bidi:plaintext;text-align:right;overflow-wrap:anywhere}',
      '.nlm__sc .nlm__scr small{font:400 11px/14px var(--nli-sans);color:var(--nli-mute)}',
      '.nlm__sc .nlm__scr.is-low strong{color:#2E6B43}',
      'html body .nli .nlm__btns button[aria-pressed="true"]{background:var(--nli-sea);color:#fff}',
      '@media (min-width:600px){.nlm__sc .nlm__scr strong{font-size:15px}}',
      'html body .nli .nlm button.nlm__csv{margin-inline-start:20px}',
      'html body .nli .nlm__rg .nlm__fq .nli__in{border:0;outline:1px solid var(--nli-line);outline-offset:-1px}',  // the same line drawn inside, so the select itself is 44 px
      'html body .nli .nlm__rg .nlm__fq .nli__in:focus-within{outline:2px solid var(--nli-sea);outline-offset:-2px;box-shadow:none}',
      'html body .nli .nlm__rg .nlm__fq select{min-height:44px}',
      '@media print{.nlm__csv,.nlm__bk .nlm__btns{display:none !important}}',
      '@media print{.nlm__live,.nlm__btns,.nlm__x,.nlm__rh button,.nlm .nli__seg,.nlm .nli__pre{display:none !important}.nlm__out{position:static}}'
    ].join('\n');
    document.head.appendChild(s);
  }

  /* ------------------------------------------------------------------------------------------------------ small builders */
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function seg(label, opts, cur, on) {
    var w = el('div', 'nli__f'); w.appendChild(el('span', 'nli__lab', esc(label)));
    var g = el('div', 'nli__seg'); g.setAttribute('role', 'group'); g.setAttribute('aria-label', label);
    opts.forEach(function (o) { var b = el('button', '', esc(o[1])); b.type = 'button'; b.setAttribute('aria-pressed', String(o[0] === cur)); b.addEventListener('click', function () { [].forEach.call(g.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); on(o[0]); }); g.appendChild(b); });
    w.appendChild(g); return w;
  }
  function input(label, val, unit, on, o) {
    o = o || {};
    var w = el('div', 'nli__f'), id = 'nlm-' + Math.random().toString(36).slice(2, 8);
    var lab = el('label', '', esc(label)); lab.htmlFor = id; w.appendChild(lab);
    var box = el('div', 'nli__in'), inp = el('input'); inp.id = id; inp.type = 'text'; inp.inputMode = 'decimal'; inp.autocomplete = 'off';
    var money = o.money; inp.value = val == null || !isFinite(val) ? '' : (money ? nf0.format(val) : String(val));
    inp.addEventListener('input', function () { on(num(inp.value)); });
    if (money) inp.addEventListener('blur', function () { var n = num(inp.value); if (isFinite(n)) inp.value = nf0.format(n); });
    box.appendChild(inp); if (unit) box.appendChild(el('span', 'nli__unit', esc(unit)));
    w.appendChild(box); if (o.help) w.appendChild(el('span', 'nli__help', o.help));
    w._inp = inp; return w;
  }
  function select(label, opts, cur, on) {
    var w = el('div', 'nli__f'), id = 'nlm-' + Math.random().toString(36).slice(2, 8);
    var lab = el('label', '', esc(label)); lab.htmlFor = id; w.appendChild(lab);
    var box = el('div', 'nli__in'), s = el('select'); s.id = id;
    opts.forEach(function (o) { var op = el('option', '', esc(o[1])); op.value = o[0]; if (o[0] === cur) op.selected = true; s.appendChild(op); });
    s.addEventListener('change', function () { on(s.value); });
    box.appendChild(s); w.appendChild(box); return w;
  }

  /* ------------------------------------------------------------------------------------------------------------- charts */
  function niceMax(v) { if (!(v > 0)) return 1; var p = Math.pow(10, Math.floor(Math.log10(v))), x = v / p; return (x <= 1 ? 1 : x <= 2 ? 2 : x <= 2.5 ? 2.5 : x <= 5 ? 5 : 10) * p; }
  function axes(W, H, pl, pb, pt, max, n, fmtY) {
    var s = '', h = H - pb - pt, k = max >= 100000;  // large amounts are shown in thousands of shekels, said once at the top
    if (k) { fmtY = function (v) { return nf0.format(Math.round(v / 1000)); }; }
    s += '<text x="' + (pl - 6) + '" y="' + (pt + 2) + '" text-anchor="end" dominant-baseline="hanging" style="font-family:IBM Plex Sans Hebrew,sans-serif">' + (k ? 'אלפי ₪' : '₪') + '</text>';
    for (var i = 0; i <= 4; i++) { var y = pt + h - h * i / 4, v = max * i / 4; if (i === 4) { s += '<line x1="' + pl + '" x2="' + (W - 6) + '" y1="' + y.toFixed(1) + '" y2="' + y.toFixed(1) + '" stroke="#D3DCE2" stroke-width="1"/>'; continue; } s += '<line x1="' + pl + '" x2="' + (W - 6) + '" y1="' + y.toFixed(1) + '" y2="' + y.toFixed(1) + '" stroke="#D3DCE2" stroke-width="1"/>' + '<text x="' + (pl - 6) + '" y="' + (y + 4).toFixed(1) + '" text-anchor="end">' + esc(fmtY(v)) + '</text>'; }
    var step = n > 24 ? 5 : n > 10 ? (W < 420 ? 5 : 2) : 1, w = (W - 6 - pl) / n;
    for (var k = 0; k < n; k++) { var yr = k + 1; if (yr === 1 || yr % step === 0) s += '<text x="' + (pl + w * (k + 0.5)).toFixed(1) + '" y="' + (H - 6) + '" text-anchor="middle">' + yr + '</text>'; }
    return s;
  }
  function kfmt(v) { return nf0.format(Math.round(v)); }
  function chartPay(R, cols, W) {  // the average monthly payment in each year, stacked by track
    var Y = R.years, n = Y.length, H = Math.round(Math.max(190, W * 0.5)), pl = 54, pb = 22, pt = 18, h = H - pb - pt, w = (W - 6 - pl) / n;
    var max = niceMax(Math.max.apply(null, Y.map(function (y) { return y.reg / y.mc; })) * 1.05), s = axes(W, H, pl, pb, pt, max, n, kfmt);
    var base = Y.map(function () { return 0; });
    R.T.forEach(function (t, k) {
      var top = Y.map(function (y, i) { return base[i] + y.byTrack[k] / y.mc; });
      var d = '';
      for (var i = 0; i < n; i++) d += (i ? 'L' : 'M') + (pl + w * i).toFixed(1) + ' ' + (pt + h - h * top[i] / max).toFixed(1) + 'L' + (pl + w * (i + 1)).toFixed(1) + ' ' + (pt + h - h * top[i] / max).toFixed(1);
      for (var j = n - 1; j >= 0; j--) d += 'L' + (pl + w * (j + 1)).toFixed(1) + ' ' + (pt + h - h * base[j] / max).toFixed(1) + 'L' + (pl + w * j).toFixed(1) + ' ' + (pt + h - h * base[j] / max).toFixed(1);
      s += '<path d="' + d + 'Z" fill="' + cols[k] + '" fill-opacity=".85" stroke="#fff" stroke-width=".6"/>';
      base = top;
    });
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc('ההחזר החודשי הממוצע בכל שנה: ' + ils(Y[0].reg / Y[0].mc) + ' בשנה הראשונה, ' + ils(Y[n - 1].reg / Y[n - 1].mc) + ' בשנה ' + n) + '">' + s + '</svg>';
  }
  function chartBal(R, W) {
    var Y = R.years, n = Y.length, H = Math.round(Math.max(190, W * 0.5)), pl = 54, pb = 22, pt = 18, h = H - pb - pt, w = (W - 6 - pl) / n;
    var max = niceMax(Math.max(R.loan, Math.max.apply(null, Y.map(function (y) { return y.bal; }))) * 1.02), s = axes(W, H, pl, pb, pt, max, n, kfmt);
    var pts = [[pl, pt + h - h * R.loan / max]].concat(Y.map(function (y, i) { return [pl + w * (i + 1), pt + h - h * y.bal / max]; }));
    var line = pts.map(function (p, i) { return (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join('');
    s += '<path d="' + line + 'L' + (pl + w * n).toFixed(1) + ' ' + (pt + h) + 'L' + pl + ' ' + (pt + h) + 'Z" fill="#2F6F86" fill-opacity=".12"/><path d="' + line + '" fill="none" stroke="#1F4B5C" stroke-width="2"/>';
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc('יתרת ההלוואה: ' + ils(R.loan) + ' בהתחלה, ' + ils(R.bal60) + ' אחרי 5 שנים, ' + ils(R.bal120) + ' אחרי 10 שנים') + '">' + s + '</svg>';
  }
  function chartPI(R, W) {  // principal (with the CPI linkage) and interest paid in each year
    var Y = R.years, n = Y.length, H = Math.round(Math.max(190, W * 0.5)), pl = 54, pb = 22, pt = 18, h = H - pb - pt, w = (W - 6 - pl) / n, bw = Math.max(1, w * 0.72);
    var lumpBy = {}; R.lumps.forEach(function (l) { var y = Math.ceil(l.month / 12) - 1; lumpBy[y] = (lumpBy[y] || 0) + l.amount; });
    var rows = Y.map(function (y, i) { var lp = lumpBy[i] || 0, ip = Math.max(0, Math.min(y.intr, y.pay - lp)); return { i: ip, p: Math.max(0, y.pay - lp - ip) }; });
    var max = niceMax(Math.max.apply(null, rows.map(function (r) { return r.i + r.p; })) * 1.05), s = axes(W, H, pl, pb, pt, max, n, kfmt);
    rows.forEach(function (r, i) {
      var x = pl + w * i + (w - bw) / 2, hp = h * r.p / max, hi = h * r.i / max;
      s += '<rect x="' + x.toFixed(1) + '" y="' + (pt + h - hp).toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + hp.toFixed(1) + '" fill="#2F6F86"/>';
      s += '<rect x="' + x.toFixed(1) + '" y="' + (pt + h - hp - hi).toFixed(1) + '" width="' + bw.toFixed(1) + '" height="' + hi.toFixed(1) + '" fill="#C42550" fill-opacity=".85"/>';
    });
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc('קרן וריבית בכל שנה: בשנה הראשונה ' + ils(rows[0].p) + ' קרן ו־' + ils(rows[0].i) + ' ריבית') + '">' + s + '</svg>';
  }
  function bucketsSvg(list, mark, lines, unitTo) {  // the distribution of last month's loans, a marker at the visitor
    var W = 360, H = 132, pl = 6, pr = 6, pt = 26, pb = 22, h = H - pt - pb, n = list.length, w = (W - pl - pr) / n;
    var max = Math.max.apply(null, list.map(function (b) { return b.share; })) || 1, s = '';
    var maxX = list[n - 1].to == null ? (list[n - 2].to + (list[n - 2].to - list[n - 2].from)) : list[n - 1].to;
    function xOf(v) { for (var i = 0; i < n; i++) { var a = list[i].from, b = list[i].to == null ? maxX : list[i].to; if (v <= b || i === n - 1) return pl + w * (i + Math.min(1, Math.max(0, (v - a) / ((b - a) || 1)))); } return W - pr; }
    list.forEach(function (b, i) {
      var bh = h * b.share / max, on = mark != null && mark > b.from && (b.to == null || mark <= b.to);
      s += '<rect x="' + (pl + w * i + 2).toFixed(1) + '" y="' + (pt + h - bh).toFixed(1) + '" width="' + (w - 4).toFixed(1) + '" height="' + Math.max(1, bh).toFixed(1) + '" fill="' + (on ? '#2F6F86' : '#B9C8D1') + '"/>';
      s += '<text x="' + (pl + w * (i + 0.5)).toFixed(1) + '" y="' + (pt + h - bh - 3).toFixed(1) + '" text-anchor="middle">' + (b.share >= 0.05 ? F.num(b.share, b.share < 1 ? 1 : 0) + '%' : '') + '</text>';
      s += '<text x="' + (pl + w * (i + 0.5)).toFixed(1) + '" y="' + (H - 6) + '" text-anchor="middle">' + (b.to == null ? '+' + b.from : b.from + '-' + b.to) + '</text>';
    });
    (lines || []).forEach(function (l) { var x = xOf(l.v); s += '<line x1="' + x.toFixed(1) + '" x2="' + x.toFixed(1) + '" y1="' + pt + '" y2="' + (pt + h) + '" stroke="' + l.c + '" stroke-width="1.5" stroke-dasharray="' + (l.dash || '3 3') + '"/>'; });
    if (mark != null && isFinite(mark)) { var mx = xOf(Math.min(mark, maxX)); s += '<path d="M' + mx.toFixed(1) + ' 10l-5 -8h10z" fill="#12202A"/><line x1="' + mx.toFixed(1) + '" x2="' + mx.toFixed(1) + '" y1="10" y2="' + (pt + h) + '" stroke="#12202A" stroke-width="2"/>'; }
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(unitTo) + '">' + s + '</svg>';
  }

  /* ---------------------------------------------------------------------------------------------------------- the tool */
  NI.register('mortgage', {
    custom: function (root, data) {
      css();
      // 26.10.2026: the result bar sticks under the site's own sticky header (header.nlhp-top, 57 px on phones, 69 px wide), not under it
      var hdr = document.querySelector('header.nlhp-top'), setTop = function () { var h = 0; if (hdr) { var cs = getComputedStyle(hdr); if (cs.position === 'sticky' || cs.position === 'fixed') h = hdr.getBoundingClientRect().height; } root.style.setProperty('--nlm-top', Math.round(h) + 'px'); };
      setTop(); window.addEventListener('resize', setTop);
      var D = data.boim || data.d0;
      if (!D || !D.tracks) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
      var TR = D.tracks, POL = D.policy, FC = D.forecast, MK = D.market;
      var y0 = +String(D.built || POL.asof).slice(0, 4), m0 = +String(D.built || POL.asof).slice(5, 7);
      var rampMonths = Math.max(1, (2027 - y0) * 12 + (8 - m0));  // to the middle of the third quarter of 2027 (the forecast horizon)

      function defRate(k) { return TR[k] ? TR[k].rate : 4; }
      function newRow(k, amount, share, years) { return { track: k, amount: amount, share: share, rate: defRate(k), touched: false, years: years || 25, method: 'spitzer', grace: 0, graceType: 'partial', freq: 60 }; }
      function base() {
        return { mode: 'amount', buyer: 'single', rows: [newRow('fixed_nl', 600000, 50), newRow('prime', 400000, 100 / 3), newRow('var5_cpi', 200000, 50 / 3)],
          target: 6000, basis: 'first', price: 2000000, equity: 500000, value: 2000000, appraisal: null, grant: false,
          cpi: 'boi', cpiCustom: 2.5, prime: 'none', shock: 1, shockMonth: 24, income: 22000, loans: 0, expenses: 0, stress: 1,
          prepay: { on: false, row: 0, month: 60, amount: 100000, mode: 'shorten' }, offer: [], compare: [],
          termUnit: 'y', showBaskets: false };  // v2: the term typed in years or months (C3); the uniform baskets for my amount shown (C14)
      }
      var v = base(), pre = null;
      function basket(k, loan, years) {
        var b = D.baskets.list.filter(function (x) { return x.k === k; })[0];
        return b.mix.map(function (x) { return newRow(x[0], Math.round(loan * x[1]), 100 * x[1], years); });
      }
      /* v2 (C14): the uniform baskets on this loan, on the term of track 1 (the convention of the compare button below), each track at
         the rate typed for it in the mix (a bank offer, if that is what was typed) and at the Bank of Israel average when the mix has
         no such track; NLMG.baskets builds the rows, NLMG.mix computes them on the page's scenario */
      function basketTerm() { var y = v.rows[0] ? +v.rows[0].years : NaN; return isFinite(y) && y > 0 ? y : 25; }
      function basketRate(k) { var r = v.rows.filter(function (x) { return x.track === k && isFinite(x.rate); })[0]; return r ? r.rate : defRate(k); }
      function basketsFor(loan, sc) { return baskets(D, loan, basketTerm(), basketRate, sc); }
      var PRESETS = [
        { key: 'b1', label: 'סל אחיד 1', sub: 'כל ההלוואה בקל״צ' },
        { key: 'b2', label: 'סל אחיד 2', sub: 'שליש קל״צ, שליש פריים, שליש משתנה צמודה' },
        { key: 'b3', label: 'סל אחיד 3', sub: 'חצי קל״צ, חצי פריים' },
        { key: 'three', label: 'שלושה מסלולים', sub: 'קל״צ, פריים ומשתנה צמודה' },
        { key: 'first2m', label: 'דירה ראשונה ב־2 מיליון', sub: 'עם 25% הון עצמי' }
      ];
      function applyPreset(k) {
        var loan = Math.round(resolve().loan) || 1200000, yrs = (v.rows[0] && v.rows[0].years) || 25;
        if (k === 'b1' || k === 'b2' || k === 'b3') { v.rows = basket(k, loan, yrs); }
        else if (k === 'three') { v.mode = 'amount'; v.rows = [newRow('fixed_nl', 600000, 50), newRow('prime', 400000, 100 / 3), newRow('var5_cpi', 200000, 50 / 3)]; }
        else if (k === 'first2m') { v.mode = 'price'; v.buyer = 'single'; v.price = 2000000; v.equity = 500000; v.rows = [newRow('fixed_nl', 750000, 50), newRow('prime', 500000, 100 / 3), newRow('var5_cpi', 250000, 50 / 3)]; }
        if (v.mode !== 'amount') syncShares();
        v.offer = []; pre = k;
      }
      function syncShares() { var t = v.rows.reduce(function (a, r) { return a + (r.amount || 0); }, 0) || 1; v.rows.forEach(function (r) { r.share = 100 * (r.amount || 0) / t; }); }

      /* the loan and the amounts by mode */
      function scenOpts(extra) {  // v2: the options alone, so the three scenarios (C9) start from the same ones
        var c = v.cpi === 'boi' ? FC.inflation_4q : v.cpi === 'market' ? FC.market_inflation : v.cpi === 'zero' ? 0 : (isFinite(v.cpiCustom) ? v.cpiCustom : 0);
        var to = v.prime === 'boi' ? FC.rate_q3_2027 - POL.rate : v.prime === 'market' ? FC.market_rate - POL.rate : 0;
        return Object.assign({ cpi: c, prime: v.prime, rampTo: to, rampMonths: rampMonths, shock: v.shock, shockMonth: v.shockMonth }, extra || {});
      }
      function scen(extra) { return scenario(scenOpts(extra)); }
      function mathRow(r, amount, withPrepay, i) {
        var T = TR[r.track] || TR.fixed_nl;
        return { amount: amount, rate: r.rate, years: r.years, method: r.method, grace: r.grace, graceType: r.graceType, kind: T.kind, linked: !!T.linked, directed: !!T.directed, freq: r.freq,
          prepay: withPrepay && v.prepay.on && v.prepay.row === i ? { month: v.prepay.month, amount: v.prepay.amount, mode: v.prepay.mode } : null };
      }
      function shares() { return v.rows.map(function (r) { return Math.max(0, +r.share || 0); }); }
      function valueFor() {
        if (v.mode !== 'price') return v.value;
        if (v.buyer === 'reduced') { var ap = isFinite(v.appraisal) && v.appraisal > 0 ? v.appraisal : v.price, cap = D.rules.reduced.value_cap; return ap > cap ? Math.max(cap, v.price) : ap; }
        return v.price;
      }
      function capFrac() { return D.rules.ltv[v.buyer] || 0.75; }
      function maxLoan() {
        var val = valueFor(), m = capFrac() * val;
        if (v.buyer === 'reduced' && v.mode === 'price') m = Math.min(m, v.price - (v.grant ? D.rules.reduced.own_min_grant : D.rules.reduced.own_min));
        return Math.max(0, m);
      }
      function resolve() {
        var loan, sh = shares(), tot = sh.reduce(function (a, b) { return a + b; }, 0);
        if (v.mode === 'amount') loan = v.rows.reduce(function (a, r) { return a + (+r.amount || 0); }, 0);
        else if (v.mode === 'price') loan = Math.max(0, (v.price || 0) - (v.equity || 0));
        else loan = solveLoan(v.rows.map(function (r, i) { return mathRow(r, 0, false, i); }), sh, scen(), v.target, v.basis);
        var amounts = v.mode === 'amount' ? v.rows.map(function (r) { return +r.amount || 0; }) : sh.map(function (s) { return tot > 0 ? loan * s / tot : 0; });
        return { loan: loan, amounts: amounts, sharesOk: v.mode === 'amount' || Math.abs(tot - 100) < 0.6, tot: tot };
      }

      /* ------------------------------------------------------------------------------------------------- the surface */
      root.innerHTML = '';
      if (!root.parentNode || !root.parentNode.closest || !root.parentNode.closest('.nli')) root.classList.add('nli');
      root.setAttribute('dir', 'rtl');
      var panel = el('div', 'nli__panel nlm');
      panel.appendChild(el('p', 'nli__kicker', 'מחשבון · משכנתא'));
      panel.appendChild(el('h2', 'nli__title', 'מחשבון משכנתא לפי מסלולים'));
      panel.appendChild(el('p', 'nli__lede', 'סכום, מסלולים ותקופה: המחשבון מראה את ההחזר הראשון, ההחזר הגבוה הצפוי, הריבית וההצמדה עד הסוף, ובודק את התמהיל מול כללי בנק ישראל. כל ריבית נפתחת בממוצע הרשמי של בנק ישראל, עם התאריך. יש לכם הצעה מהבנק? בדקו אותה מול הממוצע, בהמשך.'));
      var strip = el('div', 'nli__strip');
      [['ריבית בנק ישראל, מ־' + day(POL.from), pc(POL.rate)], ['ריבית הפריים', pc(POL.prime)], ['ההחלטה הבאה', day(FC.next_decision)],
       ['מדד המחירים, 12 חודשים עד ' + mon(D.cpi.latest), pc(D.cpi.y12, 1)], ['קל״צ, ממוצע במשכנתאות חדשות, ' + mon(MK.month), pc(D.rates.fixed_nl.rate)],
       ['תחזית בנק ישראל לריבית, רבע 3 של 2027', pc(FC.rate_q3_2027, 1)]].forEach(function (x) { strip.appendChild(el('div', '', '<span>' + esc(x[0]) + '</span><strong>' + esc(x[1]) + '</strong>')); });
      panel.appendChild(strip);
      var modeBox = el('div', ''); panel.appendChild(modeBox);
      panel.appendChild(el('span', 'nli__alab nli__prelab', 'מקרים מוכנים: לחיצה אחת ממלאת הכול'));
      var preRow = el('div', 'nli__pre'); preRow.setAttribute('role', 'group'); preRow.setAttribute('aria-label', 'מקרים מוכנים');
      PRESETS.forEach(function (p) { var b = el('button', '', '<span>' + esc(p.label) + '</span><small>' + esc(p.sub) + '</small>'); b.type = 'button'; b.setAttribute('data-k', p.key);
        b.addEventListener('click', function () { applyPreset(p.key); buildAll(); run(); }); preRow.appendChild(b); });
      panel.appendChild(preRow);
      function markPre() { [].forEach.call(preRow.children, function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-k') === pre)); }); }
      var grid = el('div', 'nlm__grid'), form = el('form', 'nli__form nlm__form'), out = el('div', 'nli__out nlm__out');
      form.addEventListener('submit', function (e) { e.preventDefault(); });
      out.setAttribute('aria-live', 'polite');
      grid.appendChild(form); grid.appendChild(out); panel.appendChild(grid);
      var chartsSec = el('section', 'nlm__sec'); panel.appendChild(chartsSec);
      var moatSec = el('section', 'nlm__sec'); moatSec.id = 'bank-offer-check'; panel.appendChild(moatSec);
      var cmpSec = el('section', 'nlm__sec'); panel.appendChild(cmpSec);
      var schedSec = el('details', 'nli__table nlm__sched'); panel.appendChild(schedSec);
      var formula = el('p', 'nli__formula'), src = el('p', 'nli__src'); panel.appendChild(formula); panel.appendChild(src);
      var share = el('div', 'nli__share'); panel.appendChild(share);
      panel.appendChild(el('p', 'nli__eg', '<b>דוגמה</b>' + esc('הערכים בפתיחה הם דוגמה: שלושה מסלולים על 1.2 מיליון ₪ ל־25 שנה, בריביות הממוצעות של בנק ישראל. שנו אותם, והתוצאה מתעדכנת מיד. המחשבון אינו הצעה לאשראי ואינו ייעוץ.')));
      root.appendChild(panel);

      var t = 0; function soon() { clearTimeout(t); t = setTimeout(run, 90); }
      function touch() { if (pre) { pre = null; markPre(); } soon(); }

      /* ---------------------------------------------------------------------------------------------------- the form */
      var rowsBox, totalBox, offerBox, totalInp = null, liveBox = null;
      function buildAll() { buildMode(); buildForm(); buildMoat(); markPre(); }
      function buildMode() {
        modeBox.innerHTML = '';
        modeBox.appendChild(seg('איך לחשב', MODES, v.mode, function (k) {
          if (k === v.mode) return;
          var R = resolve();
          if (k === 'amount') { v.rows.forEach(function (r, i) { r.amount = Math.round(R.amounts[i] || 0); }); }
          else if (v.mode === 'amount') syncShares();
          v.mode = k; buildForm(); touch();
        }));
      }
      function buildForm() {
        form.innerHTML = ''; totalInp = null;
        liveBox = el('div', 'nlm__live'); liveBox.setAttribute('aria-hidden', 'true'); form.appendChild(liveBox);
        var top = el('div', 'nlm__box');
        if (v.mode === 'amount') {
          top.appendChild(input('סכום המשכנתא', resolve().loan, '₪', function (n) {
            if (!(n > 0)) return; var cur = v.rows.reduce(function (a, r) { return a + (+r.amount || 0); }, 0) || 1;
            v.rows.forEach(function (r) { r.amount = Math.round((r.amount || 0) * n / cur); }); drawRows(); touch();
          }, { money: true, help: 'משנים את הסכום, והחלוקה בין המסלולים נשארת. אפשר גם לשנות כל מסלול בנפרד.' })); totalInp = top.lastChild._inp;
          top.appendChild(input('שווי הדירה, לבדיקת שיעור המימון', v.value, '₪', function (n) { v.value = n; touch(); }, { money: true }));
        } else if (v.mode === 'payment') {
          top.appendChild(input('ההחזר החודשי שאתם יכולים לשלם', v.target, '₪', function (n) { v.target = n; touch(); }, { money: true }));
          top.appendChild(seg('לפי איזה החזר', [['first', 'ההחזר הראשון'], ['max', 'ההחזר הגבוה הצפוי']], v.basis, function (k) { v.basis = k; touch(); }));
          top.appendChild(input('שווי הדירה, לבדיקת שיעור המימון', v.value, '₪', function (n) { v.value = n; touch(); }, { money: true }));
        } else {
          var two = el('div', 'nlm__two');
          two.appendChild(input('מחיר הדירה', v.price, '₪', function (n) { v.price = n; touch(); }, { money: true }));
          two.appendChild(input('הון עצמי', v.equity, '₪', function (n) { v.equity = n; touch(); }, { money: true }));
          top.appendChild(two);
        }
        top.appendChild(seg('מי קונה', BUYER, v.buyer, function (k) { v.buyer = k; buildForm(); touch(); }));
        if (v.buyer === 'reduced' && v.mode === 'price') {
          top.appendChild(input('הערכת שמאי, אם יש', v.appraisal, '₪', function (n) { v.appraisal = n; touch(); }, { money: true, help: 'בדירה במחיר מופחת הבנק יכול לחשב את המימון לפי הערכת השמאי. מעל 2.1 מיליון ₪: לפי 2.1 מיליון ₪ או מחיר הרכישה, הגבוה מביניהם.' }));
          var ck = el('label', 'nlm__chk'); var cb = el('input'); cb.type = 'checkbox'; cb.checked = !!v.grant; cb.addEventListener('change', function () { v.grant = cb.checked; touch(); });
          ck.appendChild(cb); ck.appendChild(document.createTextNode('ניתן על הדירה מענק של מחיר למשתכן החדשה (הון עצמי מינימלי 60,000 ₪ במקום 100,000 ₪)')); top.appendChild(ck);
        }
        totalBox = el('p', 'nlm__sum'); top.appendChild(totalBox);
        form.appendChild(top);
        var rl = el('div', 'nli__f'); rl.appendChild(el('span', 'nli__lab', 'המסלולים')); form.appendChild(rl);
        form.appendChild(seg('התקופה בכל מסלול', [['y', 'בשנים'], ['m', 'בחודשים']], v.termUnit, function (k) { if (k === v.termUnit) return; v.termUnit = k; drawRows(); touch(); }));  // v2 (C3)
        rowsBox = el('div', 'nlm__rows'); form.appendChild(rowsBox); drawRows();
        var add = el('button', 'nli__add', '+ הוספת מסלול'); add.type = 'button'; add.hidden = v.rows.length >= 6;
        add.addEventListener('click', function () { if (v.rows.length >= 6) return; var R = resolve(); var r = newRow('fixed_cpi', v.mode === 'amount' ? 100000 : 0, v.mode === 'amount' ? 0 : 10, 25);
          v.rows.push(r); if (v.mode === 'amount') syncShares(); v.offer = []; buildForm(); buildMoat(); touch(); });
        form.appendChild(add);
        var sc = el('div', 'nlm__box');
        sc.appendChild(seg('מדד המחירים בכל שנה', [['boi', 'תחזית בנק ישראל ' + pc(FC.inflation_4q, 1)], ['market', 'ציפיות השוק ' + pc(FC.market_inflation, 1)], ['zero', 'בלי עליית מדד'], ['custom', 'אחר']], v.cpi, function (k) { v.cpi = k; buildForm(); touch(); }));
        if (v.cpi === 'custom') sc.appendChild(input('מדד בשנה', v.cpiCustom, '%', function (n) { v.cpiCustom = n; touch(); }));
        sc.appendChild(seg('ריבית הפריים מכאן והלאה', [['none', 'ללא שינוי'], ['boi', 'תחזית בנק ישראל: ' + pc(FC.rate_q3_2027, 1) + ' ברבע 3 של 2027'], ['market', 'ציפיות השוק: ' + pc(FC.market_rate, 1)], ['up2', 'עלייה של 2%'], ['custom', 'שינוי משלכם']], v.prime, function (k) { v.prime = k; buildForm(); touch(); }));
        if (v.prime === 'custom') { var tw = el('div', 'nlm__two'); tw.appendChild(input('שינוי בריבית', v.shock, '%', function (n) { v.shock = n; touch(); }, { help: 'למשל 1.5, או −1 לירידה' })); tw.appendChild(input('החל מחודש', v.shockMonth, 'חודש', function (n) { v.shockMonth = n; touch(); })); sc.appendChild(tw); }
        sc.appendChild(el('p', 'nlm__hint', 'עלייה של 2% ושינוי משלכם חלים על הפריים מיד, ועל מסלול משתנה כל 5 שנים בתחנת היציאה הבאה. התחזיות חלות על הפריים בלבד.'));
        form.appendChild(sc);
        var hh = el('div', 'nlm__box');
        hh.appendChild(input('הכנסה חודשית נטו של משק הבית', v.income, '₪', function (n) { v.income = n; touch(); }, { money: true }));
        var t2 = el('div', 'nlm__two');
        t2.appendChild(input('החזרי הלוואות קיימות בחודש', v.loans, '₪', function (n) { v.loans = n; touch(); }, { money: true }));
        t2.appendChild(input('הוצאות חודשיות קבועות נוספות', v.expenses, '₪', function (n) { v.expenses = n; touch(); }, { money: true }));
        hh.appendChild(t2);
        hh.appendChild(el('p', 'nlm__hint', 'הבנק מוריד מההכנסה התחייבויות קבועות ל־18 חודשים לפחות, מזונות ושכר דירה אם לא עוברים לגור בדירה, ומחשב את ההחזר מההכנסה הפנויה.'));
        hh.appendChild(input('בדיקת רגישות: עלייה בריבית באחוזים', v.stress, '%', function (n) { v.stress = n; touch(); }));
        form.appendChild(hh);
        var pd = el('details', 'nlm__more'); pd.open = !!v.prepay.on;
        pd.appendChild(el('summary', '', 'פירעון מוקדם בעתיד, עם הערכת העמלה'));
        var pb = el('div', 'nlm__box');
        var ck2 = el('label', 'nlm__chk'); var cb2 = el('input'); cb2.type = 'checkbox'; cb2.checked = !!v.prepay.on; cb2.addEventListener('change', function () { v.prepay.on = cb2.checked; touch(); });
        ck2.appendChild(cb2); ck2.appendChild(document.createTextNode('לחשב פירעון מוקדם')); pb.appendChild(ck2);
        pb.appendChild(select('באיזה מסלול', v.rows.map(function (r, i) { return [String(i), (i + 1) + '. ' + (tn(r) || r.track)]; }), String(Math.min(v.prepay.row, v.rows.length - 1)), function (k) { v.prepay.row = +k; touch(); }));
        var t3 = el('div', 'nlm__two');
        t3.appendChild(input('בחודש', v.prepay.month, 'חודש', function (n) { v.prepay.month = n; touch(); }, { help: '60 = אחרי 5 שנים' }));
        t3.appendChild(input('סכום', v.prepay.amount, '₪', function (n) { v.prepay.amount = n; touch(); }, { money: true }));
        pb.appendChild(t3);
        pb.appendChild(seg('אחרי הפירעון', [['shorten', 'קיצור תקופה'], ['reduce', 'הקטנת החזר']], v.prepay.mode, function (k) { v.prepay.mode = k; touch(); }));
        pd.appendChild(pb); form.appendChild(pd);
      }
      function rateHint(r) {
        var T = TR[r.track]; if (!T) return '';
        var ref = T.ref || {}, txt;
        if (T.directed) txt = 'הריבית בזכאות נקבעת בתעודת הזכאות. נפתח בממוצע הקבועה הצמודה, ' + pc(D.rates.fixed_cpi.rate) + ' (' + mon(MK.month) + '). הקלידו את הריבית שלכם.';
        else if (ref.type === 'sdmx') { var s = D.rates[ref.key]; txt = 'ממוצע בנק ישראל במשכנתאות חדשות: <b>' + pc(s.rate) + '</b> (' + mon(MK.month) + ')' + (s.bench != null ? ', עוגן ' + pc(s.bench) + ' ועוד מרווח ' + pc(s.margin) : ''); }
        else { var b = D.term[ref.file].buckets[ref.bucket]; txt = 'ממוצע בנק ישראל ל' + (ref.bucket === 0 ? 'ריבית לא צמודה שמשתנה עד שנה, כולל פריים' : 'ריבית לא צמודה שמשתנה בתוך שנה עד 5 שנים') + ': <b>' + pc(b.nom) + '</b> נומינלית (' + pc(b.eff) + ' אפקטיבית), בתוקף מ־' + day(D.term[ref.file].inforce); }
        if (T.kind === 'prime') { var mg = Math.round((r.rate - POL.prime) * 100) / 100; txt += '. הפריים היום ' + pc(POL.prime) + (mg === 0 ? ', כלומר בדיוק הפריים' : ', כלומר פריים ' + (mg < 0 ? 'פחות ' : 'ועוד ') + F.num(Math.abs(mg), 2) + '%'); }
        if (r.touched) txt = 'הריבית שהקלדתם. ' + txt;
        return txt;
      }
      function bandText(b) {  // v2 (C1): the lowest and the highest bank, the month in Hebrew, the source by name
        return 'הריבית ב־' + b.n + ' הבנקים, ' + esc(monthHe(b.month)) + ': מ־<bdi>' + esc(pc(b.min.nom)) + '</bdi> (' + esc(b.min.he) + ') עד <bdi>' + esc(pc(b.max.nom)) + '</bdi> (' + esc(b.max.he) + ') נומינלית, ובריבית אפקטיבית מ־' +
          esc(pc(b.min.eff)) + ' עד ' + esc(pc(b.max.eff)) + '. <b>מקור: קו המשווה של בנק ישראל.</b>';
      }
      function drawRows() {
        rowsBox.innerHTML = '';
        var R = resolve();
        v.rows.forEach(function (r, i) {
          var card = el('div', 'nlm__row'); card.style.setProperty('--c', COL[i % COL.length]);
          var head = el('div', 'nlm__rh');
          var sw = select('מסלול ' + (i + 1), TRACKS.map(function (k) { return [k, TNAME[k]]; }), r.track, function (k) { r.track = k; if (!r.touched) r.rate = defRate(k); v.offer[i] = null; drawRows(); buildMoat(); touch(); });
          sw.querySelector('label').className = 'nli__lab'; head.appendChild(sw); sw.style.flex = '1';
          var del = el('button', '', '×'); del.type = 'button'; del.setAttribute('aria-label', 'הסרת מסלול ' + (i + 1)); del.hidden = v.rows.length < 2;
          del.addEventListener('click', function () { v.rows.splice(i, 1); v.offer.splice(i, 1); if (v.prepay.row >= v.rows.length) v.prepay.row = 0; if (v.mode === 'amount') syncShares(); buildForm(); buildMoat(); touch(); });
          head.appendChild(del); card.appendChild(head);
          var g = el('div', 'nlm__rg');
          if (v.mode === 'amount') g.appendChild(input('סכום', r.amount, '₪', function (n) { r.amount = isFinite(n) ? n : 0; syncShares(); if (totalBox) paintTotal(); touch(); }, { money: true }));
          else g.appendChild(input('חלק מההלוואה', Math.round(r.share * 100) / 100, '%', function (n) { r.share = isFinite(n) ? n : 0; touch(); }));
          var rateF = input('ריבית שנתית', r.rate, '%', function (n) { r.rate = n; r.touched = true; hint.innerHTML = rateHint(r); reset.hidden = false; touch(); });
          g.appendChild(rateF);
          var bd = band(D, r.track); if (bd) g.appendChild(el('p', 'nlm__hint nlm__band', bandText(bd)));  // v2 (C1): only where by_bank has the track
          if (v.termUnit === 'm') g.appendChild(input('חודשים', isFinite(r.years) ? Math.round(r.years * 12) : NaN, 'חודשים', function (n) { r.years = isFinite(n) ? n / 12 : NaN; touch(); }));  // v2 (C3)
          else g.appendChild(input('שנים', r.years % 1 ? Math.round(r.years * 100) / 100 : r.years, 'שנים', function (n) { r.years = n; touch(); }));
          if (isVar(r)) { var fq = select('תדירות שינוי הריבית', FREQS, String(freqOf(r)), function (k) { r.freq = +k; buildMoat(); touch(); }); fq.classList.add('nlm__fq'); g.appendChild(fq); }  // v2 (C2)
          g.appendChild(select('לוח סילוקין', METHODS, r.method, function (k) { r.method = k; touch(); }));
          g.appendChild(input('חודשי גרייס', r.grace, 'חודשים', function (n) { r.grace = isFinite(n) ? n : 0; touch(); }));
          g.appendChild(select('סוג הגרייס', [['partial', 'חלקי'], ['full', 'מלא']], r.graceType, function (k) { r.graceType = k; touch(); }));
          card.appendChild(g);
          var hint = el('p', 'nlm__hint', rateHint(r)); card.appendChild(hint);
          var reset = el('button', 'nlm__link', 'לחזור לממוצע של בנק ישראל'); reset.type = 'button'; reset.hidden = !r.touched;
          reset.addEventListener('click', function () { r.rate = defRate(r.track); r.touched = false; drawRows(); touch(); });
          card.appendChild(reset);
          card._amt = el('p', 'nlm__hint'); card.appendChild(card._amt);
          rowsBox.appendChild(card);
        });
      }
      function paintTotal() {
        var R = resolve();
        if (totalInp && document.activeElement !== totalInp && isFinite(R.loan)) totalInp.value = nf0.format(Math.round(R.loan));
        if (totalBox) totalBox.hidden = v.mode === 'amount';
        if (totalBox) totalBox.innerHTML = (v.mode === 'payment' ? 'המשכנתא שההחזר הזה מאפשר: ' : 'סכום המשכנתא: ') + '<bdi>' + (isFinite(R.loan) ? ils(R.loan) : 'לא ניתן לחשב') + '</bdi>' + (R.sharesOk ? '' : ' · החלקים מסתכמים ל־' + F.num(R.tot, 1) + '%, חישבנו לפי היחס ביניהם');
        [].forEach.call(rowsBox ? rowsBox.children : [], function (c, i) { if (c._amt) c._amt.textContent = v.mode === 'amount' ? 'חלק מההלוואה: ' + F.num(100 * (R.amounts[i] || 0) / (R.loan || 1), 1) + '%' : 'סכום במסלול: ' + ils(R.amounts[i] || 0); });
      }

      /* ---------------------------------------------------------------------------------------------- the moat inputs */
      var moatOut;
      function buildMoat() {
        moatSec.innerHTML = '';
        moatSec.appendChild(el('h3', 'nlm__h', 'ההצעה שלכם מול בנק ישראל'));
        moatSec.appendChild(el('p', 'nlm__p', 'הקלידו את הריבית שהבנק הציע לכם בכל מסלול. נשווה אותה לממוצע שבנק ישראל פרסם לאותו מסלול ולאותה תקופה, ונראה כמה הפער שווה בשקלים לאורך ההלוואה ובכל חודש.'));
        var bt = el('div', 'nlm__btns'), fill = el('button', '', 'למלא מהתמהיל שלמעלה'); fill.type = 'button';
        fill.addEventListener('click', function () { v.offer = []; buildMoat(); soon(); });
        bt.appendChild(fill); moatSec.appendChild(bt);
        offerBox = el('div', 'nlm__tw'); moatSec.appendChild(offerBox);
        moatOut = el('div', ''); moatSec.appendChild(moatOut);
        var tb = '<table class="nlm__t is-cards"><thead><tr><th scope="col">מסלול</th><th scope="col">שנים</th><th scope="col">הריבית בהצעה</th><th scope="col">ממוצע בנק ישראל למסלול</th><th scope="col">ממוצע לאותה תקופה</th><th scope="col">הפער</th><th scope="col">לאורך ההלוואה</th><th scope="col">בחודש הראשון</th></tr></thead><tbody></tbody></table>';
        offerBox.innerHTML = tb;
        var body = offerBox.querySelector('tbody');
        v.rows.forEach(function (r, i) {
          var tr = el('tr', ''); tr.innerHTML = '<td>' + esc((i + 1) + '. ' + tn(r)) + '</td><td class="n" data-y data-l="שנים"></td><td data-l="הריבית בהצעה"></td><td class="r" data-s data-l="ממוצע בנק ישראל למסלול"></td><td class="r" data-b data-l="ממוצע לאותה תקופה"></td><td class="n" data-g data-l="הפער"></td><td class="n" data-ils data-l="לאורך ההלוואה"></td><td class="n" data-m data-l="בחודש הראשון"></td>';
          var inp = el('input'); inp.type = 'text'; inp.inputMode = 'decimal'; inp.setAttribute('aria-label', 'הריבית בהצעה, מסלול ' + (i + 1));
          inp.value = v.offer[i] != null ? String(v.offer[i]) : String(r.rate);
          inp.addEventListener('input', function () { var n = num(inp.value); v.offer[i] = isFinite(n) ? n : null; soon(); });
          tr.children[2].appendChild(inp); body.appendChild(tr);
        });
        var sum = el('tr', 'is-sum'); sum.innerHTML = '<td>כל ההלוואה</td><td></td><td></td><td></td><td></td><td></td><td class="n" data-ils data-l="לאורך ההלוואה"></td><td class="n" data-m data-l="בחודש הראשון"></td>'; body.appendChild(sum);
      }

      /* ------------------------------------------------------------------------------------------------------- run */
      var last = null, monthly = false;
      function err(msg) { out.innerHTML = '<p class="nli__note">' + esc(msg) + '</p>'; }
      function run() {
        paintTotal();
        var R0 = resolve();
        if (!(R0.loan > 0) || !isFinite(R0.loan)) return err(v.mode === 'payment' ? 'הקלידו את ההחזר החודשי, ולפחות מסלול אחד עם חלק מההלוואה.' : v.mode === 'price' ? 'ההון העצמי גדול ממחיר הדירה, או שהמחיר חסר.' : 'הקלידו סכום לפחות במסלול אחד.');
        for (var i = 0; i < v.rows.length; i++) {
          var r = v.rows[i];
          if (v.termUnit === 'm') { var mo = Math.round(r.years * 12); if (!(mo >= 48 && mo <= 360)) return err('מסלול ' + (i + 1) + ': תקופה בין 48 ל־360 חודשים.'); }  // v2 (C3)
          else if (!(r.years >= 4 && r.years <= 35)) return err('מסלול ' + (i + 1) + ': תקופה בין 4 ל־30 שנים.');
          if (!(r.rate >= 0 && r.rate <= 20)) return err('מסלול ' + (i + 1) + ': ריבית שנתית בין 0% ל־20%.');
          if (!(r.grace >= 0 && r.grace < r.years * 12)) return err('מסלול ' + (i + 1) + ': הגרייס צריך להיות קצר מתקופת המסלול.');
        }
        var rows = v.rows.map(function (r, i) { return mathRow(r, R0.amounts[i], true, i); });
        var sc = scen(), R = mix(rows, sc);
        var base0 = mix(v.rows.map(function (r, i) { return mathRow(r, R0.amounts[i], false, i); }), sc);
        var st1 = isFinite(v.stress) && v.stress !== 0 ? mix(v.rows.map(function (r, i) { return mathRow(r, R0.amounts[i], false, i); }), scen({ all: v.stress })) : null;
        var st2 = mix(v.rows.map(function (r, i) { return mathRow(r, R0.amounts[i], false, i); }), scen({ all: 2 }));
        // v2: the three scenarios side by side (C9) and, on request, the uniform baskets on this amount and term (C14)
        var s3 = three(v.rows.map(function (r, i) { return mathRow(r, R0.amounts[i], false, i); }), D, scenOpts());
        var bk = v.showBaskets ? basketsFor(R0.loan, sc) : null;
        last = { R: R, base: base0, R0: R0, sc: sc, st1: st1, st2: st2, s3: s3, bk: bk };
        paintOut(last); paintCharts(last); paintMoat(last); paintCompare(); paintSched(last); paintFoot(last);
      }

      function ptiOf(pay) { var disp = (v.income || 0) - (v.loans || 0) - (v.expenses || 0); return disp > 0 ? pay / disp : NaN; }
      function paintOut(L) {
        var R = L.R, loan = L.R0.loan, val = valueFor(), ltv = val > 0 ? loan / val : NaN, cap = capFrac(), mx = maxLoan();
        out.innerHTML = ''; out.id = out.id || 'nlm-out-' + Math.random().toString(36).slice(2, 7);
        if (liveBox) liveBox.innerHTML = '<div><span>ההחזר הראשון</span><strong>' + esc(ils(R.first)) + '</strong></div><div><span>ההחזר הגבוה הצפוי</span><strong>' + esc(ils(R.highest)) + '</strong></div><a href="#' + out.id + '">לכל התוצאות</a>';
        var a = el('div', 'nli__answer');
        a.innerHTML = '<span class="nli__alab">ההחזר החודשי הראשון</span><output class="nli__fig">' + esc(R.first >= 0.5 ? ils(R.first) : 'ללא תשלום') + '</output><span class="nli__asub">' +
          (R.highest >= 0.5 ? 'ההחזר הגבוה הצפוי: <bdi>' + esc(ils(R.highest)) + '</bdi>, ' + esc(yearsOf(R.highestMonth)) : 'אין החזר חודשי עד התשלום בסוף התקופה') + (R.first < 0.5 && R.highest >= 0.5 ? ' (בחודשי הגרייס המלא אין תשלום)' : '') + ' · משכנתא של <bdi>' + esc(ils(loan)) + '</bdi></span>';
        out.appendChild(a);
        var tot = R.firstBy.reduce(function (s, b) { return s + b; }, 0) || 1, bw = el('div', ''), bar = el('div', 'nli__bar'), lg = el('ul', 'nli__legend');
        bar.setAttribute('role', 'img'); bar.setAttribute('aria-label', 'ההחזר הראשון לפי מסלול: ' + v.rows.map(function (r, i) { return tn(r) + ' ' + ils(R.firstBy[i]); }).join(', '));
        v.rows.forEach(function (r, i) { var x = el('i', ''); x.style.width = (100 * R.firstBy[i] / tot) + '%'; x.style.background = COL[i % COL.length]; bar.appendChild(x);
          lg.appendChild(el('li', '', '<b style="background:' + COL[i % COL.length] + '"></b>' + esc(tn(r)) + ' <bdi>' + esc(ils(R.firstBy[i])) + '</bdi>')); });
        bw.appendChild(bar); bw.appendChild(lg); out.appendChild(bw);
        var pti = ptiOf(R.first), ptiH = ptiOf(R.highest);
        var lines = [['ההחזר הגבוה הצפוי, ' + yearsOf(R.highestMonth), ils(R.highest)], ['סך כל התשלומים', ils(R.totalPaid)], ['סך הריבית', ils(R.totalInterest)], ['סך ההצמדה למדד', R.totalLinkage > 0.5 ? ils(R.totalLinkage) : 'ללא הצמדה'],
          ['החזר לכל שקל', '₪' + F.num(R.perShekel, 2)], ['היתרה אחרי 5 שנים', R.N >= 60 ? ils(R.bal60) : 'ההלוואה נפרעה'], ['היתרה אחרי 10 שנים', R.N >= 120 ? ils(R.bal120) : 'ההלוואה נפרעה'],
          ['החזר מההכנסה, בהחזר הראשון', isFinite(pti) ? pc(100 * pti, 1) : 'הקלידו הכנסה'], ['החזר מההכנסה, בהחזר הגבוה', isFinite(ptiH) ? pc(100 * ptiH, 1) : 'הקלידו הכנסה'],
          ['שיעור מימון (מותר עד ' + pc(100 * cap, 0) + ')', isFinite(ltv) ? pc(100 * ltv, 1) : 'הקלידו שווי']];
        if (v.mode === 'price') lines.push(['ההון העצמי הנדרש לפחות', ils(Math.max(0, v.price - mx))]);
        R.lumps.forEach(function (l) { lines.push([(v.rows[l.k].method === 'balloon' ? 'התשלום בסוף מסלול ' + (l.k + 1) + ' (בלון: הקרן והריבית שנצברה)' : 'הקרן בסוף מסלול ' + (l.k + 1) + ' (בוליט)') + ', ' + yearsOf(l.month), ils(l.amount)]); });
        v.rows.forEach(function (r, i) { if (offFreq(r)) lines.push(['תדירות שינוי הריבית, מסלול ' + (i + 1), freqLabel(freqOf(r))]); });  // v2 (C2): the choice is in the results
        var dl = el('dl', 'nli__lines'); lines.forEach(function (x) { dl.appendChild(el('div', '', '<dt>' + esc(x[0]) + '</dt><dd>' + esc(x[1]) + '</dd>')); }); out.appendChild(dl);
        if (isFinite(pti)) { var cls = pti > 0.4 ? 'is-hi' : pti > 0.3 ? 'is-mid' : ''; out.appendChild(el('p', 'nlm__status ' + cls, esc(pti > 0.4 ? OLD.hi : pti > 0.3 ? OLD.mid : OLD.lo))); }
        var ss = el('div', 'nlm__stress'), b0 = L.base.first;
        function stc(lab, M) { return '<div><span>' + esc(lab) + '</span><strong>' + esc(ils(M.first)) + '</strong><small>' + esc('גידול ' + ils(M.first - b0) + ' בחודש · סך ריבית ' + ils(M.totalInterest)) + '</small></div>'; }
        var html = '';
        if (L.st1 && Math.abs(v.stress - 2) > 1e-9) html += stc('בדיקת עליית ריבית של ⁦' + (v.stress > 0 ? '+' : '') + F.num(v.stress, v.stress % 1 ? 1 : 0) + '%⁩ בכל המסלולים', L.st1);
        html += stc('בדיקת עליית ריבית של ⁦+2%⁩ בכל המסלולים', L.st2);
        ss.innerHTML = html; out.appendChild(el('span', 'nli__alab', 'החזר חודשי אם הריבית תעלה')); out.appendChild(ss);
        out.appendChild(el('span', 'nli__alab', 'מול כללי בנק ישראל'));
        var ul = el('ul', 'nlm__rules');
        rules(R, loan, ltv, cap, pti).forEach(function (x) { ul.appendChild(el('li', x[0] === 'bad' ? 'is-bad' : x[0] === 'warn' ? 'is-warn' : '', '<b>' + esc(x[0] === 'bad' ? 'חריגה' : x[0] === 'warn' ? 'לתשומת לב' : 'תקין') + '</b><span>' + esc(x[1]) + '</span>')); });
        out.appendChild(ul);
        if (v.prepay.on) out.appendChild(prepayBlock(L));
        out.appendChild(threeBlock(L)); out.appendChild(basketBlock(L));  // v2 (C9, C14)
      }
      /* v2: one card of a scenario or a mix: the first payment, the highest with its year, the total paid */
      function scCard(cls, title, sub, M, low) {
        var c = el('div', 'nlm__sc' + (cls ? ' ' + cls : ''));
        c.innerHTML = '<b class="nlm__sct">' + esc(title) + '</b><span class="nlm__scs">' + esc(sub) + '</span>' +
          '<div class="nlm__scr"><span>ההחזר הראשון</span><strong>' + esc(ils(M.first)) + '</strong></div>' +
          '<div class="nlm__scr"><span>ההחזר הגבוה</span><strong>' + esc(ils(M.highest)) + '</strong><small>' + esc(yearsOf(M.highestMonth)) + '</small></div>' +
          '<div class="nlm__scr' + (low ? ' is-low' : '') + '"><span>סך כל התשלומים</span><strong>' + esc(ils(M.totalPaid)) + '</strong></div>';
        return c;
      }
      function threeBlock(L) {  // C9
        var w = el('div', 'nlm__three'), S = L.s3, o = scenOpts();
        w.appendChild(el('span', 'nli__alab', 'שלושה תרחישים זה לצד זה'));
        var g = el('div', 'nlm__s3'); g.setAttribute('role', 'group'); g.setAttribute('aria-label', 'שלושה תרחישים: היום, תחזית בנק ישראל ותרחיש מחמיר');
        g.appendChild(scCard('', 'היום', 'הריביות של היום עד הסוף, מדד ' + pc(o.cpi, 1) + ' בשנה', S.today));
        g.appendChild(scCard('is-fc', 'תחזית בנק ישראל', 'ריבית בנק ישראל ' + pc(FC.rate_q3_2027, 1) + ' ברבע 3 של 2027, מדד ' + pc(FC.inflation_4q, 1) + ' בשנה', S.boi));
        g.appendChild(scCard('is-hard', 'תרחיש מחמיר', 'עלייה של 2% בכל המסלולים מהחודש הראשון', S.stress));
        w.appendChild(g);
        w.appendChild(el('p', 'nlm__hint', 'באותם מסלולים ובאותו סכום, בלי פירעון מוקדם. התחזית של בנק ישראל מ־' + day(FC.published) + ' חלה על מסלול הפריים, כמו בבחירה למעלה. התרחיש המחמיר הוא בדיקת ה־2% שלמעלה, על המדד ומסלול הפריים שבחרתם.'));
        return w;
      }
      function basketBlock(L) {  // C14
        var w = el('div', 'nlm__bk'), bt = el('div', 'nlm__btns'), b = el('button', '', 'הסלים האחידים לסכום שלי'); b.type = 'button';
        b.setAttribute('aria-pressed', String(!!v.showBaskets));
        b.addEventListener('click', function () { v.showBaskets = !v.showBaskets; run(); var nb = out.querySelector('.nlm__bk button'); if (nb) nb.focus(); });
        bt.appendChild(b); w.appendChild(bt);
        if (!v.showBaskets || !L.bk) return w;
        var yrs = basketTerm(), term = v.termUnit === 'm' ? nf0.format(Math.round(yrs * 12)) + ' חודשים' : F.num(yrs, yrs % 1 ? 1 : 0) + ' שנה';
        var mixed = v.rows.some(function (r) { return r.years !== v.rows[0].years; });
        w.appendChild(el('p', 'nlm__hint', esc('שלושת הסלים האחידים של הוראה 451 על ' + ils(L.R0.loan) + ' ל־' + term + (mixed ? ' (התקופה של מסלול 1)' : '') + ', בלוח שפיצר, באותו מדד ובאותו מסלול פריים, ליד התמהיל שלכם.')));
        var all = [{ name: 'התמהיל שלכם', sub: v.rows.length === 1 ? 'מסלול אחד' : v.rows.length + ' מסלולים', M: L.base, cls: 'is-me' }].concat(L.bk.map(function (x) {
          var p = PRESETS.filter(function (q) { return q.key === x.k; })[0]; return { name: x.label, sub: p ? p.sub : '', M: x.R, cls: '' }; }));
        var lo = all.reduce(function (a, x, i) { return x.M.totalPaid < all[a].M.totalPaid - 0.5 ? i : a; }, 0);
        var g = el('div', 'nlm__s4'); g.setAttribute('role', 'group'); g.setAttribute('aria-label', 'התמהיל שלכם ושלושת הסלים האחידים');
        all.forEach(function (x, i) { g.appendChild(scCard(x.cls, x.name, x.sub, x.M, i === lo)); });
        w.appendChild(g);
        w.appendChild(el('p', 'nlm__hint', 'בירוק: סך התשלומים הנמוך מבין הארבעה. בכל אישור עקרוני הבנק חייב להציג את שלושת הסלים בריביות שלו. כאן כל מסלול בריבית שהקלדתם לו בתמהיל, ומסלול שאין בתמהיל בממוצע של בנק ישראל.'));
        return w;
      }
      function rules(R, loan, ltv, cap, pti) {
        var o = [], varAmt = 0, rl = D.rules;
        v.rows.forEach(function (r, i) { var k = (TR[r.track] || {}).kind; if (k === 'prime' || k === 'var5') varAmt += L0amt(i); });
        var vs = loan > 0 ? varAmt / loan : 0;
        o.push(vs > rl.variable_max + 1e-6 ? ['bad', 'החלק בריבית משתנה הוא ' + pc(100 * vs, 1) + ' מההלוואה. בנק ישראל מתיר עד 66.66%, כלומר לפחות שליש בריבית קבועה (הוראה 329, סעיף 7).']
          : ['ok', 'החלק בריבית משתנה (פריים ומשתנה כל 5 שנים): ' + pc(100 * vs, 1) + ', בתוך המגבלה של 66.66% (הוראה 329, סעיף 7).']);
        var longs = v.rows.map(function (r, i) { return r.years > rl.term_max ? i + 1 : 0; }).filter(Boolean);
        o.push(longs.length ? ['bad', 'מסלול ' + longs.join(', ') + ' ארוך מ־30 שנה. בנק ישראל לא מתיר משכנתא ליותר מ־30 שנה (הוראה 329, סעיף 8).'] : ['ok', 'כל המסלולים עד 30 שנה (הוראה 329, סעיף 8).']);
        var bn = { single: 'בדירה יחידה', replace: 'בדירה חליפית', invest: 'בדירה להשקעה', reduced: 'בדירה במחיר מופחת' }[v.buyer];
        if (isFinite(ltv)) o.push(ltv > cap + 1e-6 ? ['bad', 'שיעור המימון ' + pc(100 * ltv, 1) + '. ' + bn + ' הבנק יכול לממן עד ' + pc(100 * cap, 0) + ' מהשווי, ' + ils(cap * valueFor()) + ' כאן (הוראה 329, סעיף 2).' + (v.mode === 'price' ? ' חסרים ' + ils(Math.max(0, loan - maxLoan())) + ' הון עצמי.' : '')]
          : ['ok', 'שיעור המימון ' + pc(100 * ltv, 1) + ', ' + bn + ' מותר עד ' + pc(100 * cap, 0) + ' (הוראה 329, סעיף 2).']);
        if (v.buyer === 'reduced' && v.mode === 'price') { var own = v.grant ? rl.reduced.own_min_grant : rl.reduced.own_min, mine = v.price - loan; o.push(mine + 0.5 < own ? ['bad', 'בדירה במחיר מופחת הקונה משלם מכספו לפחות ' + ils(own) + '. כאן ' + ils(mine) + ' (הוראה 329, סעיף 4א).'] : ['ok', 'הון עצמי ' + ils(mine) + ', מעל המינימום של ' + ils(own) + ' בדירה במחיר מופחת (הוראה 329, סעיף 4א).']); }
        if (isFinite(pti)) o.push(pti > rl.pti_max + 1e-6 ? ['bad', 'ההחזר הוא ' + pc(100 * pti, 1) + ' מההכנסה הפנויה. בנק ישראל אוסר על הבנק לאשר משכנתא שההחזר בה עולה על 50% מההכנסה (הוראה 329, סעיף 5).']
          : pti > rl.pti_risk + 1e-6 ? ['warn', 'ההחזר הוא ' + pc(100 * pti, 1) + ' מההכנסה הפנויה: מתחת ל־50% המותרים, אבל מעל 40%, ובמשכנתא כזו הבנק נדרש להחזיק יותר הון, ולכן רבים מהבנקים מסרבים או מייקרים.']
          : ['ok', 'ההחזר הוא ' + pc(100 * pti, 1) + ' מההכנסה הפנויה, מתחת ל־40% ול־50% המותרים (הוראה 329, סעיפים 5 ו־6).']);
        return o;
      }
      function L0amt(i) { return last && last.R0 ? last.R0.amounts[i] || 0 : 0; }
      function prepayBlock(L) {
        var i = Math.min(v.prepay.row, v.rows.length - 1), S = L.R.T[i], B0 = L.base, w = el('div', 'nlm__box');
        w.appendChild(el('h4', 'nlm__h4', 'פירעון מוקדם במסלול ' + (i + 1) + ': ' + tn(v.rows[i])));
        if (!S || !S.prepay) { w.appendChild(el('p', 'nlm__hint', 'בחודש הזה המסלול כבר נפרע, או שהסכום חסר. בחרו חודש מוקדם יותר.')); return w; }
        var P = S.prepay, tr = mathRow(v.rows[i], L.R0.amounts[i], true, i);
        var f0 = prepayFee(tr, P, D, 0), f1 = prepayFee(tr, P, D, 1);
        var saveI = B0.totalInterest + B0.totalLinkage - L.R.totalInterest - L.R.totalLinkage;
        var li = [['סכום הפירעון, ' + yearsOf(P.month), ils(P.amount)], ['חיסכון בריבית ובהצמדה עד הסוף', ils(saveI)]];
        if (v.prepay.mode === 'shorten') li.push([P.endAfter < P.endBefore ? 'המסלול מסתיים ב' + yearsOf(P.endAfter) : 'המסלול מסתיים', P.endAfter < P.endBefore ? F.num(P.endBefore - P.endAfter) + ' חודשים מוקדם יותר' : 'באותו מועד (בלון, בוליט או גרייס)']);
        else { var nx = S.pay[P.month] || 0, ob = B0.T[i].pay[P.month] || 0; li.push(['ההחזר במסלול בחודש שאחרי (במקום ' + ils(ob) + ')', ils(nx)]); }
        if (f0.none) li.push(['עמלת פירעון', 'ללא עמלה: הלוואת זכאות היא הלוואה מכוונת (צו הבנקאות, סעיף 2)']);
        else {
          li.push(['עמלה תפעולית', 'עד ' + ils(f0.op)]);
          li.push(['עמלת היוון, אם הריבית הממוצעת לא תשתנה', f0.why === 'prime' ? 'ללא: הריבית משתנה לפחות פעם בשנה' : f0.why === 'reset' ? 'ללא: הפירעון ביום שינוי הריבית' : f0.cap > 0.5 ? ils(f0.cap) : 'ללא עמלת היוון']);
          if (f0.why !== 'prime' && f0.why !== 'reset') li.push(['עמלת היוון, אם הממוצע ירד ב־1% עד אז' + (f1.cap > 0.5 && f1.cut ? ' (אחרי הפחתה של ' + F.num(100 * f1.cut) + '%)' : ''), f1.cap > 0.5 ? ils(f1.cap) : 'ללא עמלת היוון']);
          li.push(['בהודעה של פחות מ־10 ימים (0.1%)', ils(f0.notice)]);
          if (f0.cpi > 0.5) li.push(['בפירעון בין ה־1 ל־15 בחודש, במסלול צמוד (מחצית השינוי הממוצע במדד)', ils(f0.cpi)]);
        }
        var dl = el('dl', 'nli__lines'); li.forEach(function (x) { dl.appendChild(el('div', '', '<dt>' + esc(x[0]) + '</dt><dd>' + esc(x[1]) + '</dd>')); }); w.appendChild(dl);
        w.appendChild(el('p', 'nlm__hint', 'עמלת ההיוון לפי צו הבנקאות (פירעון מוקדם של הלוואה לדיור): ההפרש בין התשלומים העתידיים מהוונים בריבית הממוצעת של בנק ישראל לבין היתרה, רק כשהממוצע ביום הפירעון נמוך מהריבית שלכם, הנמוך משני החישובים, בהפחתה של 20% אחרי 3 שנים ו־30% אחרי 5. הממוצע של יום הפירעון לא ידוע היום: לקחנו את הממוצע של היום לתקופה שתישאר' + (f0.bucket ? ' (' + f0.bucket.label + ', ' + pc(f0.avg) + ' נומינלית)' : '') + '.'));
        return w;
      }

      function paintCharts(L) {
        var R = L.R; var cw = chartsSec.clientWidth || 600; chartsSec.innerHTML = ''; var W = Math.round(Math.max(300, Math.min(640, (cw >= 1000 ? (cw - 32) / 3 : cw) - 26)));
        chartsSec.appendChild(el('h3', 'nlm__h', 'המשכנתא לאורך השנים'));
        var g = el('div', 'nlm__charts');
        function fig(title, svg, lg, cap) { var f = el('figure', 'nlm__chart'); f.style.margin = '0'; f.appendChild(el('h4', 'nlm__h4', esc(title))); f.insertAdjacentHTML('beforeend', svg); if (lg) f.appendChild(lg); if (cap) f.appendChild(el('figcaption', '', esc(cap))); return f; }
        var lg1 = el('ul', 'nlm__lg'); v.rows.forEach(function (r, i) { lg1.appendChild(el('li', '', '<i style="background:' + COL[i % COL.length] + '"></i>' + esc((i + 1) + '. ' + tn(r)))); });
        g.appendChild(fig('ההחזר החודשי לפי מסלול', chartPay(R, COL, W), lg1, 'ממוצע ההחזר החודשי בכל שנה, בשקלים של אותה שנה' + (R.lumps.length ? '; בלי תשלום הקרן בסוף מסלולי בלון ובוליט' : '') + '.'));
        g.appendChild(fig('יתרת ההלוואה', chartBal(R, W), null, 'בסוף כל שנה, כולל ההצמדה למדד.'));
        var lg3 = el('ul', 'nlm__lg', '<li><i style="background:#2F6F86"></i>קרן, כולל הצמדה</li><li><i style="background:#C42550"></i>ריבית</li>');
        g.appendChild(fig('קרן וריבית בכל שנה', chartPI(R, W), lg3, 'כמה מהתשלומים של כל שנה הלכו לקרן וכמה לריבית.'));
        chartsSec.appendChild(g);
      }

      /* ---------------------------------------------------------------------------------------------------- the moat */
      function refFor(r) {
        var T = TR[r.track]; if (!T || T.directed) return null;
        var s = T.ref && T.ref.type === 'sdmx' ? D.rates[T.ref.key] : null, b = null, file = T.term_file;
        if (r.track === 'fixed_nl' || r.track === 'fixed_cpi') b = bucket(D.term[file].buckets, r.years);
        else if (offFreq(r)) b = bucket(D.term[file].buckets, freqOf(r) / 12);  // v2 (C2): the period until the rate changes
        else if (T.term_bucket != null) b = D.term[file].buckets[T.term_bucket];
        var main = r.track === 'var5_cpi' && s ? { rate: s.rate, by: 'sdmx' } : b ? { rate: b.nom, by: 'term' } : s ? { rate: s.rate, by: 'sdmx' } : null;
        return { sdmx: s ? s.rate : null, term: b, file: file, main: main };
      }
      function paintMoat(L) {
        if (!offerBox) return;
        var trs = offerBox.querySelectorAll('tbody tr'), loanAll = 0, gapAll = 0, gapM = 0, n = 0, offerRows = [], refRows = [], ok = true;
        v.rows.forEach(function (r, i) {
          var tr = trs[i]; if (!tr) return;
          var o = v.offer[i] != null ? v.offer[i] : r.rate, ref = refFor(r);
          tr.querySelector('[data-y]').textContent = F.num(r.years, r.years % 1 ? 1 : 0);
          var inp = tr.querySelector('input'); if (v.offer[i] == null && document.activeElement !== inp) inp.value = String(r.rate);
          tr.querySelector('[data-s]').innerHTML = ref && ref.sdmx != null ? '<bdi>' + pc(ref.sdmx) + '</bdi><small>' + esc(mon(MK.month)) + '</small>' : ref ? '<small>לא מתפרסם בנפרד</small>' : '';
          tr.querySelector('[data-b]').innerHTML = ref && ref.term ? '<bdi>' + pc(ref.term.nom) + '</bdi><small>' + esc(ref.term.label) + '</small>' : '';
          var g = tr.querySelector('[data-g]'), gi = tr.querySelector('[data-ils]'), gm = tr.querySelector('[data-m]');
          g.className = gi.className = gm.className = 'n';
          var amt = L.R0.amounts[i] || 0;
          offerRows.push(Object.assign(mathRow(r, amt, false, i), { rate: isFinite(o) ? o : r.rate }));
          refRows.push(Object.assign(mathRow(r, amt, false, i), { rate: ref && ref.main ? ref.main.rate : (isFinite(o) ? o : r.rate) }));
          if (!ref || !ref.main) { g.textContent = 'הריבית נקבעת בזכאות'; gi.textContent = ''; gm.textContent = ''; return; }
          var A = mix([offerRows[i]], L.sc), B = mix([refRows[i]], L.sc), dP = A.totalPaid - B.totalPaid, dM = A.first - B.first, gp = o - ref.main.rate;
          var same = Math.abs(gp) < 0.005;
          g.textContent = same ? 'כמו הממוצע' : (gp > 0 ? '+' : '−') + F.num(Math.abs(gp), 2) + '%';
          gi.textContent = same || Math.abs(dP) < 0.5 ? 'ללא פער' : (dP > 0 ? '+' : '−') + ils(Math.abs(dP)); gm.textContent = same || Math.abs(dM) < 0.5 ? 'ללא פער' : (dM > 0 ? '+' : '−') + ils(Math.abs(dM));
          [g, gi, gm].forEach(function (x) { x.className = 'n ' + (gp > 0.004 ? 'pos' : gp < -0.004 ? 'neg' : ''); });
          gapAll += dP; gapM += dM; loanAll += amt; n++;
        });
        var sum = trs[trs.length - 1];
        if (sum) { sum.querySelector('[data-ils]').textContent = Math.abs(gapAll) < 0.5 ? 'ללא פער' : (gapAll > 0 ? '+' : '−') + ils(Math.abs(gapAll)); sum.querySelector('[data-m]').textContent = Math.abs(gapM) < 0.5 ? 'ללא פער' : (gapM > 0 ? '+' : '−') + ils(Math.abs(gapM)); }
        moatOut.innerHTML = '';
        var vd = el('p', 'nlm__verdict ' + (gapAll > 50 ? 'is-high' : gapAll < -50 ? 'is-low' : ''));
        vd.innerHTML = n === 0 ? 'אין במסלולים שלכם מסלול שבנק ישראל מפרסם לו ממוצע.' : Math.abs(gapAll) <= 50 ? 'ההצעה שלכם קרובה מאוד לממוצעים של בנק ישראל לאותם מסלולים ותקופות.'
          : gapAll > 0 ? 'בריבית הממוצעת של בנק ישראל הייתם משלמים <bdi>' + esc(ils(gapAll)) + '</bdi> פחות לאורך ההלוואה, כ־<bdi>' + esc(ils(Math.abs(gapM))) + '</bdi> פחות בחודש הראשון. שווה לחזור לבנק עם המספרים האלה.'
          : 'ההצעה שלכם זולה מהממוצע: בריבית הממוצעת של בנק ישראל הייתם משלמים <bdi>' + esc(ils(-gapAll)) + '</bdi> יותר לאורך ההלוואה, כ־<bdi>' + esc(ils(Math.abs(gapM))) + '</bdi> יותר בחודש הראשון.';
        moatOut.appendChild(vd);
        moatOut.appendChild(el('p', 'nlm__hint', 'ממוצע למסלול: ריבית ממוצעת במשכנתאות החדשות של ' + mon(MK.month) + ' (בנק ישראל). ממוצע לאותה תקופה: הריבית הממוצעת לפי התקופה לפירעון, בתוקף מ־' + day(D.term.nl.inforce) + '; במסלול משתנה התקופה היא עד שינוי הריבית. בנק ישראל מפרסם את הקבצים האלה כריבית אפקטיבית; המרנו לנומינלית לפי תשלום חודשי, כמו בגיליון ההמרה של בנק ישראל. הפער בשקלים מחושב מול ממוצע התקופה, ובמסלול משתנה צמוד מול ממוצע המסלול.'));
        /* where the loan stands among last month's mortgages */
        var R = L.R, loan = L.R0.loan, pti = ptiOf(R.first), ltv = valueFor() > 0 ? loan / valueFor() : NaN;
        var wy = v.rows.reduce(function (a, r, i) { return a + r.years * (L.R0.amounts[i] || 0); }, 0) / (loan || 1);
        moatOut.appendChild(el('h4', 'nlm__h4', 'המשכנתא שלכם בין ' + nf0.format(MK.loans) + ' המשכנתאות החדשות של ' + mon(MK.month)));
        var pl = el('div', 'nlm__place');
        function inB(list, x) { for (var i = 0; i < list.length; i++) { var b = list[i]; if (x > b.from && (b.to == null || x <= b.to)) return b; } return list[0]; }
        var pc1 = el('div', 'nlm__pc'); pc1.appendChild(el('h4', 'nlm__h4', 'החזר מההכנסה'));
        var ptiList = MK.pti.filter(function (b) { return b.from < 50; }).concat([{ from: 50, to: null, share: MK.pti.filter(function (b) { return b.from >= 50; }).reduce(function (a, b) { return a + b.share; }, 0) }]);
        pc1.insertAdjacentHTML('beforeend', bucketsSvg(ptiList, isFinite(pti) ? 100 * pti : null, [{ v: MK.pti_avg, c: '#2F6F86', dash: '2 2' }, { v: 40, c: '#12202A' }, { v: 50, c: '#C42550' }], 'התפלגות ההחזר מההכנסה במשכנתאות החדשות'));
        var pb = isFinite(pti) ? inB(ptiList, 100 * pti) : null;
        pc1.appendChild(el('p', '', isFinite(pti) ? 'ההחזר שלכם <b>' + esc(pc(100 * pti, 1)) + '</b> מההכנסה. ' + esc(F.num(pb.share, 1) + '% מכספי המשכנתאות של החודש ניתנו בטווח ' + (pb.to == null ? 'מעל ' + pb.from + '%' : pb.from + '% עד ' + pb.to + '%')) + '. הממוצע: ' + esc(pc(MK.pti_avg)) + '. הקווים: 40% ו־50% של הוראה 329.' : 'הקלידו הכנסה כדי לראות איפה אתם.'));
        pl.appendChild(pc1);
        var pc2 = el('div', 'nlm__pc'); pc2.appendChild(el('h4', 'nlm__h4', 'שיעור המימון'));
        var ltvList = MK.ltv.filter(function (b) { return b.from < 75; }).concat([{ from: 75, to: null, share: MK.ltv.filter(function (b) { return b.from >= 75; }).reduce(function (a, b) { return a + b.share; }, 0) }]);
        pc2.insertAdjacentHTML('beforeend', bucketsSvg(ltvList, isFinite(ltv) ? 100 * ltv : null, [{ v: 50, c: '#5E6A75' }, { v: 70, c: '#12202A' }, { v: 75, c: '#C42550' }], 'התפלגות שיעור המימון במשכנתאות החדשות'));
        var lb = isFinite(ltv) ? inB(ltvList, 100 * ltv) : null;
        pc2.appendChild(el('p', '', isFinite(ltv) ? 'המימון שלכם <b>' + esc(pc(100 * ltv, 1)) + '</b>. ' + esc(F.num(lb.share, 1) + '% מכספי המשכנתאות של החודש ניתנו בטווח ' + (lb.to == null ? 'מעל ' + lb.from + '%' : lb.from + '% עד ' + lb.to + '%')) + '. הקווים: 50% (דירה להשקעה), 70% (חליפית), 75% (יחידה).' : 'הקלידו את שווי הדירה כדי לראות איפה אתם.'));
        pl.appendChild(pc2);
        var pc3 = el('div', 'nlm__pc'); pc3.appendChild(el('h4', 'nlm__h4', 'גודל ההלוואה ותקופתה'));
        var dz = loan / MK.avg_loan - 1, dt = wy - MK.term_nl;
        pc3.appendChild(el('p', '', 'המשכנתא שלכם <b>' + esc(ils(loan)) + '</b>, ' + esc(Math.abs(dz) < 0.02 ? 'כמו הממוצע' : F.num(Math.abs(100 * dz), 0) + '% ' + (dz > 0 ? 'יותר' : 'פחות') + ' מהממוצע') + ' של ' + esc(ils(MK.avg_loan)) + ' למשכנתא (' + esc(F.num(MK.volume_k / 1e6, 2)) + ' מיליארד ₪ ב־' + esc(nf0.format(MK.loans)) + ' משכנתאות).'));
        pc3.appendChild(el('p', '', 'התקופה הממוצעת בתמהיל שלכם <b>' + esc(F.num(wy, 1)) + ' שנים</b>, ' + esc(Math.abs(dt) < 0.3 ? 'כמו הממוצע' : F.num(Math.abs(dt), 1) + ' שנים ' + (dt > 0 ? 'יותר' : 'פחות') + ' מהממוצע') + ' של ' + esc(F.num(MK.term_nl, 1)) + ' שנים בהלוואות הלא צמודות.'));
        pl.appendChild(pc3);
        var pc4 = el('div', 'nlm__pc'); pc4.appendChild(el('h4', 'nlm__h4', 'איך לקחו משכנתא ב־' + mon(MK.month)));
        var bar = el('div', 'nli__bar'), lg = el('ul', 'nli__legend'), tc = ['#1F4B5C', '#2F6F86', '#4F9A5C', '#7FA9B8', '#5E6A75'];
        MK.tracks.forEach(function (x, i) { var q = el('i', ''); q.style.width = x.share + '%'; q.style.background = tc[i % tc.length]; bar.appendChild(q); lg.appendChild(el('li', '', '<b style="background:' + tc[i % tc.length] + '"></b>' + esc(x.label) + ' <bdi>' + esc(F.num(x.share, 1) + '%') + '</bdi>')); });
        bar.setAttribute('role', 'img'); bar.setAttribute('aria-label', MK.tracks.map(function (x) { return x.label + ' ' + x.share + '%'; }).join(', '));
        pc4.appendChild(bar); pc4.appendChild(lg);
        var vsh = loan > 0 ? 100 * v.rows.reduce(function (a, r, i) { var k = (TR[r.track] || {}).kind; return a + (k === 'prime' || k === 'var5' ? L.R0.amounts[i] || 0 : 0); }, 0) / loan : 0;
        pc4.appendChild(el('p', '', 'אצלכם: <b>' + esc(F.num(vsh, 1)) + '%</b> בריבית משתנה. בכל המשכנתאות של החודש: ' + esc(F.num(MK.tracks.filter(function (x) { return x.k === 'var_nl' || x.k === 'var_cpi'; }).reduce(function (a, x) { return a + x.share; }, 0), 1)) + '%.'));
        pl.appendChild(pc4);
        moatOut.appendChild(pl);
        moatOut.appendChild(el('p', 'nlm__limits', 'הגבולות: הממוצעים כוללים את כל הלווים ואת כל שיעורי המימון, ולווה עם הכנסה יציבה ומימון נמוך יכול לקבל ריבית נמוכה מהממוצע. ההשוואה נעשית מול הנתונים האחרונים שבנק ישראל פרסם, לא מול היום שבו קיבלתם את ההצעה. זו אינה הצעה לאשראי ואינה ייעוץ.'));
      }

      /* ------------------------------------------------------------------------------------------------- compare mixes */
      function snapshot(name, rows) { return { name: name, rows: rows.map(function (r) { return { track: r.track, amount: r.amount, rate: r.rate, years: r.years, method: r.method, grace: r.grace, graceType: r.graceType, freq: r.freq }; }) }; }
      function paintCompare() {
        cmpSec.innerHTML = '';
        cmpSec.appendChild(el('h3', 'nlm__h', 'השוואת תמהילים'));
        cmpSec.appendChild(el('p', 'nlm__p', 'שמרו את התמהיל, שנו מסלולים, ושמרו שוב. עד ארבעה תמהילים זה לצד זה, באותו מדד ובאותה ריבית פריים.'));
        var bt = el('div', 'nlm__btns'), sv = el('button', 'is-solid', 'שמירת התמהיל הזה להשוואה'); sv.type = 'button'; sv.disabled = v.compare.length >= 4;
        sv.addEventListener('click', function () { if (v.compare.length >= 4) return; var R0 = resolve(); v.compare.push(snapshot('תמהיל ' + (v.compare.length + 1), v.rows.map(function (r, i) { return Object.assign({}, r, { amount: Math.round(R0.amounts[i]) }); }))); paintCompare(); });
        var bk = el('button', '', 'הוספת שלושת הסלים האחידים'); bk.type = 'button'; bk.disabled = v.compare.length > 1;
        bk.addEventListener('click', function () { var loan = Math.round(resolve().loan), yrs = (v.rows[0] && v.rows[0].years) || 25; ['b1', 'b2', 'b3'].forEach(function (k, j) { if (v.compare.length < 4) v.compare.push(snapshot('סל אחיד ' + (j + 1) + ', ' + yrs + ' שנה', basket(k, loan, yrs))); }); paintCompare(); });
        bt.appendChild(sv); bt.appendChild(bk); cmpSec.appendChild(bt);
        if (!v.compare.length) return;
        var sc = scen(), cols = [{ name: 'התמהיל הנוכחי', R: last ? last.base : null }].concat(v.compare.map(function (c) { return { name: c.name, R: mix(c.rows.map(function (r) { return mathRow(r, r.amount, false, -1); }), sc), c: c }; }));
        var rowsT = [['סכום', function (R) { return ils(R.loan); }], ['ההחזר הראשון', function (R) { return ils(R.first); }], ['ההחזר הגבוה הצפוי', function (R) { return ils(R.highest); }], ['סך כל התשלומים', function (R) { return ils(R.totalPaid); }],
          ['סך הריבית', function (R) { return ils(R.totalInterest); }], ['סך ההצמדה', function (R) { return R.totalLinkage > 0.5 ? ils(R.totalLinkage) : 'ללא הצמדה'; }], ['החזר לכל שקל', function (R) { return '₪' + F.num(R.perShekel, 2); }], ['היתרה אחרי 5 שנים', function (R) { return ils(R.bal60); }]];
        var h = '<table class="nlm__t"><thead><tr><th scope="col"></th>' + cols.map(function (c, j) { return '<th scope="col">' + esc(c.name) + (j ? ' <button type="button" class="nlm__x" data-x="' + (j - 1) + '" aria-label="הסרה מההשוואה">×</button>' : '') + '</th>'; }).join('') + '</tr></thead><tbody>';
        var best = rowsT.map(function (rt, k) { if (k === 0) return -1; var vals = cols.map(function (c) { return c.R ? [c.R.first, c.R.highest, c.R.totalPaid, c.R.totalInterest, c.R.totalLinkage, c.R.perShekel, c.R.bal60][k - 1] : Infinity; }); return vals.indexOf(Math.min.apply(null, vals)); });
        rowsT.forEach(function (rt, k) { h += '<tr><th scope="row">' + esc(rt[0]) + '</th>' + cols.map(function (c, j) { return '<td class="n' + (best[k] === j && cols.length > 1 ? ' neg' : '') + '">' + (c.R ? esc(rt[1](c.R)) : '') + '</td>'; }).join('') + '</tr>'; });
        h += '<tr><th scope="row">המסלולים</th>' + cols.map(function (c) { var rs = c.c ? c.c.rows : v.rows; return '<td style="white-space:normal;font-size:12px !important">' + esc(rs.map(function (r) { return (tn(r) || '').split(':')[0] + ' ' + F.num(r.rate, 2) + '%'; }).join(' · ')) + '</td>'; }).join('') + '</tr></tbody></table>';
        var tw = el('div', 'nlm__tw', h); cmpSec.appendChild(tw);
        [].forEach.call(tw.querySelectorAll('[data-x]'), function (b) { b.addEventListener('click', function () { v.compare.splice(+b.getAttribute('data-x'), 1); paintCompare(); }); });
        cmpSec.appendChild(el('p', 'nlm__hint', 'בירוק: הנמוך בכל שורה. הסלים האחידים לפי הוראה 451: בכל אישור עקרוני הבנק חייב להציג אותם, בלוח שפיצר, עם הריבית הכוללת, סך ההחזר וההחזר החודשי הגבוה הצפוי. כאן הם בריביות הממוצעות של בנק ישראל.'));
      }

      function paintSched(L) {
        var R = L.R, open = schedSec.open;
        function bl(x) { return x < 0.5 ? 'נפרעה' : ils(x); }
        function pr(x) { return x < -0.5 ? '+' + ils(-x) + ' ליתרה' : ils(Math.max(0, x)); }  // a grace or balloon month: the interest joins the balance
        var h = '<summary>לוח הסילוקין לפי שנה' + (monthly ? ' ולפי חודש' : '') + '</summary><div class="nli__tw"><table><thead><tr><th scope="col">' + (monthly ? 'חודש' : 'שנה') + '</th><th scope="col">תשלומים</th><th scope="col">ריבית</th><th scope="col" class="ph">קרן והצמדה</th><th scope="col">יתרה בסוף</th></tr></thead><tbody>';
        if (!monthly) R.years.forEach(function (y) { h += '<tr><td class="n">' + y.y + '</td><td class="n">' + esc(ils(y.pay)) + '</td><td class="n">' + esc(ils(y.intr)) + '</td><td class="n ph">' + esc(pr(y.pay - y.intr)) + '</td><td class="n">' + esc(bl(y.bal)) + '</td></tr>'; });
        else for (var m = 0; m < R.N; m++) h += '<tr><td class="n">' + (m + 1) + '</td><td class="n">' + esc(ils(R.pay[m])) + '</td><td class="n">' + esc(ils(R.intr[m])) + '</td><td class="n ph">' + esc(pr(R.pay[m] - R.intr[m])) + '</td><td class="n">' + esc(bl(R.bal[m])) + '</td></tr>';
        h += '</tbody></table></div>';
        schedSec.innerHTML = h;
        var b = el('button', 'nlm__link', monthly ? 'לחזור ללוח השנתי' : 'להצגת כל ' + nf0.format(R.N) + ' החודשים'); b.type = 'button';
        b.addEventListener('click', function () { monthly = !monthly; paintSched(last); schedSec.open = true; });
        schedSec.appendChild(b);
        var dc = el('button', 'nlm__link nlm__csv', 'הורדת לוח הסילוקין (CSV)'); dc.type = 'button'; dc.addEventListener('click', downloadCsv); schedSec.appendChild(dc);  // v2 (C5)
        if (R.prepaid > 0) schedSec.appendChild(el('p', 'nlm__hint', 'הפירעון המוקדם (' + ils(R.prepaid) + ') אינו בעמודת התשלומים; היתרה כבר כוללת אותו.'));
        schedSec.open = open;
      }

      /* v2 (C5): the monthly schedule as a CSV file, built in the browser; nothing is sent anywhere */
      function csvNames() { return v.rows.map(function (r, i) { var T = TR[r.track] || {}; return 'מסלול ' + (i + 1) + ' ' + (T.short || r.track) + (offFreq(r) ? ' ' + freqLabel(freqOf(r)) : ''); }); }
      function downloadCsv() {
        if (!last) return;
        var blob = new Blob([csv(last.R, csvNames())], { type: 'text/csv;charset=utf-8' }), url = URL.createObjectURL(blob), a = document.createElement('a');
        a.href = url; a.download = 'mortgage-schedule.csv'; a.style.display = 'none'; document.body.appendChild(a); a.click();
        setTimeout(function () { URL.revokeObjectURL(url); if (a.parentNode) a.parentNode.removeChild(a); }, 1500);
      }

      function shareState() {
        var s = { mo: v.mode, bu: v.buyer, r: v.rows.map(function (r) { return [r.track, Math.round(r.amount || 0), Math.round((r.share || 0) * 100) / 100, r.rate, r.touched ? 1 : 0, r.years, r.method, r.grace, r.graceType].concat(offFreq(r) ? [freqOf(r)] : []); }),
          tg: v.target, ba: v.basis, pr: v.price, eq: v.equity, va: v.value, ap: v.appraisal, gr: v.grant ? 1 : 0, cp: v.cpi, cc: v.cpiCustom, pp: v.prime, sk: v.shock, sm: v.shockMonth,
          in: v.income, lo: v.loans, ex: v.expenses, ss: v.stress, pf: [v.prepay.on ? 1 : 0, v.prepay.row, v.prepay.month, v.prepay.amount, v.prepay.mode], of: v.offer };
        if (v.termUnit === 'm') s.tu = 'm';  // v2: written only when used, so a v1 case keeps its link
        var j = JSON.stringify(s), b = btoa(unescape(encodeURIComponent(j))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
        return (location.origin && location.origin !== 'null' ? location.origin + location.pathname : location.href.split('#')[0]) + '#mortgage=' + b;
      }
      function loadState(h) {
        try {
          var b = h.replace(/-/g, '+').replace(/_/g, '/'); while (b.length % 4) b += '=';
          var s = JSON.parse(decodeURIComponent(escape(atob(b)))), n = base();
          n.mode = s.mo || n.mode; n.buyer = s.bu || n.buyer;
          if (s.r && s.r.length) n.rows = s.r.slice(0, 6).map(function (x) { return { track: TR[x[0]] ? x[0] : 'fixed_nl', amount: +x[1] || 0, share: +x[2] || 0, rate: +x[3], touched: !!x[4], years: +x[5] || 25, method: x[6] || 'spitzer', grace: +x[7] || 0, graceType: x[8] || 'partial', freq: FREQS.some(function (f) { return +f[0] === +x[9]; }) ? +x[9] : 60 }; });
          n.termUnit = s.tu === 'm' ? 'm' : 'y';
          ['tg:target', 'ba:basis', 'pr:price', 'eq:equity', 'va:value', 'ap:appraisal', 'cp:cpi', 'cc:cpiCustom', 'pp:prime', 'sk:shock', 'sm:shockMonth', 'in:income', 'lo:loans', 'ex:expenses', 'ss:stress'].forEach(function (p) { var q = p.split(':'); if (s[q[0]] != null) n[q[1]] = s[q[0]]; });
          n.grant = !!s.gr; if (s.pf) n.prepay = { on: !!s.pf[0], row: +s.pf[1] || 0, month: +s.pf[2] || 60, amount: +s.pf[3] || 0, mode: s.pf[4] || 'shorten' };
          n.offer = Array.isArray(s.of) ? s.of : [];
          n.rows.forEach(function (r) { if (!r.touched) r.rate = defRate(r.track); });  // an untouched rate opens at the newest average
          v = n; return true;
        } catch (e) { return false; }
      }

      function paintFoot(L) {
        var R = L.R;
        formula.textContent = 'שפיצר: החזר = יתרה × ר ÷ (1 − (1 + ר)^−מ), כש־ר היא הריבית השנתית ÷ 12 ומ מספר התשלומים שנותרו. קרן שווה: אותו חלק קרן בכל חודש ועוד ריבית על היתרה. בוליט: רק ריבית בכל חודש והקרן בסוף. בלון: תשלום אחד בסוף, עם הריבית שנצברה. גרייס חלקי: רק ריבית; גרייס מלא: בלי תשלום, והריבית מצטרפת ליתרה. במסלול צמוד היתרה מוצמדת כל חודש למדד שבחרתם, וההחזר מחושב מחדש. פריים: ריבית בנק ישראל ועוד 1.5%; הריבית במסלול זזה לפי מסלול הפריים שבחרתם. משתנה כל 5 שנים: הריבית מתעדכנת בתחילת כל 5 שנים. החזר מההכנסה = ההחזר ÷ (הכנסה נטו − הלוואות קיימות − הוצאות קבועות).' +
          (v.rows.some(offFreq) ? ' במסלול משתנה בתדירות אחרת שבחרתם, הריבית מתעדכנת בתחילת כל תקופה כזו, ועלייה של 2% או שינוי משלכם מגיעים אליו רק בתחנת היציאה הבאה.' : '');  // v2 (C2)
        src.innerHTML = 'מקורות: ' + D.sources.map(function (s) { return '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.label) + '</a>'; }).join(' · ') + '. הנתונים עודכנו ב־' + esc(day(D.built)) + '.';
        share.innerHTML = '';
        var text = 'מחשבון משכנתא: הלוואה ' + ils(L.R0.loan) + ' ב־' + v.rows.length + ' מסלולים, החזר ראשון ' + ils(R.first) + ', החזר גבוה צפוי ' + ils(R.highest) + ', סך תשלומים ' + ils(R.totalPaid) + ' (ריבית ' + ils(R.totalInterest) + ', הצמדה ' + ils(R.totalLinkage) + ').';
        var fq = v.rows.map(function (r, i) { return offFreq(r) ? 'מסלול ' + (i + 1) + ' ' + freqLabel(freqOf(r)) : ''; }).filter(Boolean);
        if (fq.length) text += ' שינוי הריבית במסלול המשתנה: ' + fq.join(', ') + '.';  // v2 (C2): the choice goes into the copied text
        var ICON = { copy: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 7h9v10H7z"/><path d="M4 13V3h9"/></svg>', wa: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16l1-3.2A7 7 0 1 1 7.6 15z"/></svg>',
          print: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 8V3h10v5"/><path d="M5 14H3V8h14v6h-2"/><path d="M6 12h8v5H6z"/></svg>', link: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M8 12l4-4"/><path d="M9 5l2-2a3 3 0 0 1 4 4l-2 2"/><path d="M11 15l-2 2a3 3 0 0 1-4-4l2-2"/></svg>' };
        function copy(btn, txt, lab) { var sp = btn.querySelector('span'); var done = function () { sp.textContent = 'הועתק'; setTimeout(function () { sp.textContent = lab; }, 1600); };
          if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, function () { window.prompt('העתיקו', txt); }); else window.prompt('העתיקו', txt); }
        var b1 = el('button', 'is-primary', ICON.copy + '<span>העתקת התוצאה</span>'); b1.type = 'button'; b1.addEventListener('click', function () { copy(b1, text + '\n' + shareState(), 'העתקת התוצאה'); });
        var b2 = el('a', '', ICON.wa + '<span>שליחה בוואטסאפ</span>'); b2.target = '_blank'; b2.rel = 'noopener'; b2.href = 'https://wa.me/'; b2.addEventListener('click', function () { b2.href = 'https://wa.me/?text=' + encodeURIComponent(text + '\n' + shareState()); });
        var b3 = el('button', '', ICON.link + '<span>קישור שפותח את אותם מספרים</span>'); b3.type = 'button'; b3.addEventListener('click', function () { copy(b3, shareState(), 'קישור שפותח את אותם מספרים'); });
        var b4 = el('button', '', ICON.print + '<span>הדפסה או שמירה כקובץ</span>'); b4.type = 'button'; b4.addEventListener('click', function () { schedSec.open = true; window.print(); });
        var b5 = el('button', '', '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 3v10"/><path d="M6 9l4 4 4-4"/><path d="M4 16h12"/></svg><span>הורדת לוח הסילוקין (CSV)</span>'); b5.type = 'button'; b5.addEventListener('click', downloadCsv);  // v2 (C5)
        share.appendChild(b1); share.appendChild(b2); share.appendChild(b3); share.appendChild(b4); share.appendChild(b5);
      }

      /* the case the page opens on: a shared link, else the page's preset, else the example */
      var opened = false, hm = /#mortgage=([A-Za-z0-9_\-]+)/.exec(location.hash || '');
      if (hm) opened = loadState(hm[1]);
      if (!opened) { try { var P = JSON.parse(root.getAttribute('data-nli-set') || '{}'); if (P.preset && PRESETS.some(function (p) { return p.key === P.preset; })) applyPreset(P.preset); } catch (e) {} }
      buildAll(); run();
      var rz = 0, lastW = chartsSec.clientWidth; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { if (last && Math.abs(chartsSec.clientWidth - lastW) > 40) { lastW = chartsSec.clientWidth; paintCharts(last); } }, 200); });
      window.NLMG.ui = { state: function () { return v; }, last: function () { return last; }, run: run, rebuild: function () { buildAll(); run(); }, link: shareState,
        csv: function () { return last ? csv(last.R, csvNames()) : ''; } };  // v2: csv, the text the download button saves
    }
  });
})();
