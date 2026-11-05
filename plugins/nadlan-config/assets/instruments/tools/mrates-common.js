/* NadLan Instruments · mrates common (HAD-675, 5.11.2026): the shared math and parts of the three rate tools of
   /mortgage-calculator/: mdecision ("החלטת הריבית והמשכנתא שלכם"), mreplay ("אם 2022 חוזרת") and mexit ("כמה תעלה היציאה").
   Every payment, balance and fee comes from window.NLMG (tools/mortgage.js: pmt, scenario, track, mix, ef2nom, prepayFee, stream,
   pv); nothing here amortizes on its own. Two small extensions on top of it:
   - a CPI path that changes month by month: NLMG.track runs the linked track in real terms (CPI 0) and every month is multiplied
     by the index ratio. Exact, because a linked Spitzer payment is the real payment times the cumulative index;
   - the early-repayment fee of a loan taken in the past: NLMG.prepayFee with the two averages of the Banking Order read from the
     Bank of Israel files (the average in force on the loan day and today's), passed as a one-bucket term table and a "drop".
   Round E (HAD-675, 6.11.2026), added only: refiAvg and refiExisting (mexit "האם למחזר?") and two style rules (.nli__fig.is-he,
   .mrx__rfg). Nothing above them changed, so mdecision and mreplay behave as before.
   Data: boi-mortgage.json (key "boim": policy, forecast, expect, by_bank, prepay, fees, baskets, term, flows, cpi), boi-rate.json
   (key "boi"), cbs-120010.json (CPI). The pure part runs in node for test_mrates.js; the page part needs core.js (the engine). */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;
  function L() { return G.NLMG; }

  /* ------------------------------------------------------------------------------------------------------- tracks */
  // the five tracks of the Bank of Israel comparison by bank (by_bank, TamInt010.xls), in its order
  var TK = ['fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi'];
  // var_nl_other ("variable not linked, not prime") is taken as variable every 5 years (stated on every tool that uses it)
  var KIND = { fixed_nl: { kind: 'fixed', linked: false, file: 'nl' }, prime: { kind: 'prime', linked: false, file: 'nl' },
    var_nl_other: { kind: 'var5', linked: false, file: 'nl' }, var_cpi: { kind: 'var5', linked: true, file: 'cpi' }, fixed_cpi: { kind: 'fixed', linked: true, file: 'cpi' } };
  var NAME = { fixed_nl: 'קבועה לא צמודה', prime: 'פריים', var_nl_other: 'משתנה לא צמודה, לא פריים', var_cpi: 'משתנה צמודה למדד', fixed_cpi: 'קבועה צמודה למדד' };
  var SHORT = { fixed_nl: 'קל״צ', prime: 'פריים', var_nl_other: 'משתנה לא צמודה', var_cpi: 'משתנה צמודה', fixed_cpi: 'ק״צ' };
  var COL = { fixed_nl: '#1F4B5C', prime: '#2F6F86', var_nl_other: '#4F9A5C', var_cpi: '#8E7CC3', fixed_cpi: '#F2D15A' };
  var BASKET_KEY = { fixed_nl: 'fixed_nl', prime: 'prime', var5_cpi: 'var_cpi', var5_nl: 'var_nl_other', fixed_cpi: 'fixed_cpi' };  // baskets speak mortgage.js names
  var REPLAY = { from: '2022-03', to: '2023-05' };  // the month before the first hike of 14.4.2022, to the last hike of 25.5.2023

  /* the data files, found by their shape (cbs-120010.json has no "key") */
  function pick(data) {
    var o = { D: null, rate: null, cpi: null };
    Object.keys(data || {}).forEach(function (k) {
      var d = data[k]; if (!d || typeof d !== 'object') return;
      if (d.tracks && d.policy) o.D = d; else if (d.changes && d.prime != null) o.rate = d; else if (d.months && String(d.id) === '120010') o.cpi = d;
    });
    return o;
  }

  /* ------------------------------------------------------------------------------------------------------- months */
  function mAdd(k, n) { var y = +k.slice(0, 4), m = +k.slice(5, 7) - 1 + n; y += Math.floor(m / 12); m = ((m % 12) + 12) % 12; return y + '-' + (m < 9 ? '0' : '') + (m + 1); }
  function mDiff(a, b) { return (+b.slice(0, 4) - +a.slice(0, 4)) * 12 + (+b.slice(5, 7) - +a.slice(5, 7)); }
  function nowKey(d) { d = d || new Date(); return d.getFullYear() + '-' + (d.getMonth() < 9 ? '0' : '') + (d.getMonth() + 1); }
  function lastDay(k) { var y = +k.slice(0, 4), m = +k.slice(5, 7); return k + '-' + new Date(Date.UTC(y, m, 0)).getUTCDate(); }
  function parseMonth(s) {  // "2024-11", "11.2024", "11/2024" -> "2024-11"; anything else (or month 13) -> null
    s = String(s || '').trim(); var m = /^(\d{4})-(\d{1,2})$/.exec(s), y, mo;
    if (m) { y = +m[1]; mo = +m[2]; } else { m = /^(\d{1,2})[.\/](\d{4})$/.exec(s); if (!m) return null; y = +m[2]; mo = +m[1]; }
    return mo >= 1 && mo <= 12 && y >= 1990 && y <= 2100 ? y + '-' + (mo < 10 ? '0' : '') + mo : null;
  }

  /* --------------------------------------------------------------------------------------------------------- mixes */
  /* the system's (or one bank's) average mix of the latest month: shares as published, the effective rate turned nominal for a
     monthly payment (NLMG.ef2nom, the same conversion as the Bank of Israel sheet; r = nominal / 1200 = (1 + e)^(1/12) - 1) */
  function bankMix(D, bank) {
    var BB = D && D.by_bank; if (!BB || !BB.latest) return null;
    var row = BB.latest.table.filter(function (x) { return x.bank === (bank || 'system'); })[0]; if (!row) return null;
    return { bank: row.bank, month: BB.latest.month, irr: row.irr,
      rows: TK.map(function (k) { var x = row[k] || { rate: 0, share: 0 }; return { k: k, share: x.share, eff: x.rate, rate: L().ef2nom(x.rate) }; }) };
  }
  function bankList(D) {  // the system and the five largest banks, in the file's market-share order
    var BB = D && D.by_bank; if (!BB || !BB.latest) return [];
    var big = BB.latest.big5_rank_by_irr || [];
    return [{ k: 'system', he: 'כל הבנקים' }].concat((BB.banks || []).filter(function (b) { return big.indexOf(b.k) > -1; }).map(function (b) { return { k: b.k, he: b.he }; }));
  }
  /* mix rows -> NLMG rows: the loan split by share (shares that do not add to 100 are taken by their ratio) */
  function mathRows(rows, amount, years) {
    var tot = rows.reduce(function (a, r) { return a + Math.max(0, +r.share || 0); }, 0) || 1;
    return rows.filter(function (r) { return +r.share > 0; }).map(function (r) {
      var K = KIND[r.k]; return { k: r.k, amount: amount * r.share / tot, rate: +r.rate, years: years, method: 'spitzer', kind: K.kind, linked: K.linked };
    });
  }
  function basketRows(D, b, rateOf) {  // a uniform basket of directive 451, at the reader's own rate for each track
    return b.mix.map(function (x) { var k = BASKET_KEY[x[0]] || x[0]; return { k: k, share: 100 * x[1], rate: rateOf(k) }; });
  }

  /* ------------------------------------------------------------------------------------------- tool 1: mdecision */
  function quarter(B, rate, n, step) { var P = L().pmt; return P(B, (rate + step) / 1200, n) - P(B, rate / 1200, n); }
  /* the forecast horizon: the middle of the third quarter of 2027 (forecast.rate_q3_2027), the same ramp as tools/mortgage.js */
  function rampMonths(D) { var s = String(D.built || D.policy.asof), y0 = +s.slice(0, 4), m0 = +s.slice(5, 7); return Math.max(1, (2027 - y0) * 12 + (8 - m0)); }
  /* the payment on a prime balance once the policy rate has moved by `to` points along the ramp (NLMG.track + NLMG.scenario) */
  function pathPay(B, rate, n, to, months) {
    var S = L().track({ amount: B, rate: rate, years: n / 12, method: 'spitzer', kind: 'prime', linked: false }, L().scenario({ prime: 'boi', rampTo: to, rampMonths: months }));
    var i = Math.max(0, Math.min(months, n) - 1); return { pay: S.pay[i], month: i + 1 };
  }
  /* a whole mix on decision day: only prime moves with the decision; the payment now, the move per step, the payment on a path */
  function decision(rows, step) {
    var o = { now: 0, q: 0, prime: 0, total: 0, rows: [] };
    rows.forEach(function (r) {
      var n = Math.round(r.years * 12), K = KIND[r.k], now = L().pmt(r.amount, r.rate / 1200, n), q = K.kind === 'prime' ? quarter(r.amount, r.rate, n, step == null ? 0.25 : step) : 0;
      o.now += now; o.q += q; o.total += r.amount; if (K.kind === 'prime') o.prime += r.amount;
      o.rows.push({ k: r.k, now: now, q: q, kind: K.kind, linked: K.linked, n: n });
    });
    return o;
  }
  function ladderPay(rows, d) { return rows.reduce(function (a, r) { var n = Math.round(r.years * 12); return a + L().pmt(r.amount, (r.rate + (KIND[r.k].kind === 'prime' ? d : 0)) / 1200, n); }, 0); }
  function pathMix(rows, to, months) { return rows.reduce(function (a, r) { var n = Math.round(r.years * 12); return a + (KIND[r.k].kind === 'prime' ? pathPay(r.amount, r.rate, n, to, months).pay : L().pmt(r.amount, r.rate / 1200, n)); }, 0); }

  /* --------------------------------------------------------------------------------------------- tool 2: mreplay */
  function boiOn(R, iso) { var o = { rate: null, prime: null, from: null }; R.changes.forEach(function (c) { if (c.from <= iso) { o.rate = c.rate; o.prime = c.prime; o.from = c.from; } }); return o; }
  /* the real path, one row per calendar month: the Bank of Israel rate in force on the last day of the month (boi-rate.json) and
     the CPI of the month (cbs-120010.json); month 1 is the month before the first hike, so the first payment is today's */
  function replayPath(R, C, from, to) {
    from = from || REPLAY.from; to = to || REPLAY.to;
    var o = { months: [], boi: [], prime: [], cpi: [], off: [], ratio: [], cpiM: [] };
    for (var k = from; k <= to; k = mAdd(k, 1)) { var b = boiOn(R, lastDay(k)); o.months.push(k); o.boi.push(b.rate); o.prime.push(b.prime); o.cpi.push(C.months[k]); }
    o.months.forEach(function (k, i) { o.off.push(o.boi[i] - o.boi[0]); o.ratio.push(o.cpi[i] / o.cpi[0]); o.cpiM.push(i ? o.cpi[i] / o.cpi[i - 1] - 1 : 0); });
    o.hikes = R.changes.filter(function (c) { return c.from > lastDay(from) && c.from <= lastDay(to); });
    return o;
  }
  /* the mix on the path: prime reprices every month by the change in the BoI rate since month 1 (NLMG.scenario's prime(m));
     fixed tracks keep their rate; variable every 5 years keeps it until month 61 (after the 15 months); linked tracks grow with the
     CPI path. Returns the month-by-month payment, its split (prime / CPI) above the first payment, the peak and the extra. */
  function replay(rows, P) {
    var W = P.months.length, sc = { cpi: 0, all: 0, prime: function (m) { return P.off[Math.min(m, W) - 1]; }, reset: function () { return 0; } };
    var o = { pay: [], primeX: [], cpiX: [], by: [], first: 0, peak: 0, peakIdx: 0, extra: 0, cum: 0, W: W }, i;
    for (i = 0; i < W; i++) { o.pay.push(0); o.primeX.push(0); o.cpiX.push(0); }
    rows.forEach(function (t) {
      var S = L().track(Object.assign({}, t, { prepay: null }), sc), line = [];
      for (var j = 0; j < W; j++) {
        var p = S.pay[j] * (t.linked ? P.ratio[j] : 1); line.push(p); o.pay[j] += p;
        if (t.kind === 'prime') o.primeX[j] += S.pay[j] - S.pay[0];
        if (t.linked) o.cpiX[j] += S.pay[j] * (P.ratio[j] - 1);
      }
      o.by.push({ k: t.k, pay: line });
    });
    o.first = o.pay[0];
    for (i = 0; i < W; i++) { if (o.pay[i] > o.peak + 1e-9) { o.peak = o.pay[i]; o.peakIdx = i; } o.cum += o.pay[i] - o.first; }
    o.extra = o.peak - o.first;
    return o;
  }

  /* ------------------------------------------------------------------------------------------------ tool 3: mexit */
  /* the cost of a mix until year N on a scenario: payments, the balance to repay, the early-repayment fee of every track at month
     12N (NLMG.prepayFee; `drop` = how much lower the Bank of Israel average is on that day than today's), and the price of the
     money = payments + balance + fee - loan = interest + CPI linkage + fee */
  function exitAt(rows, D, sc, years, drop) {
    var R = L().mix(rows.map(function (t) { return Object.assign({}, t, { prepay: null }); }), sc), h = Math.round(years * 12), o = { R: R, h: h, end: h >= R.N, loan: R.loan };
    var n = Math.min(h, R.N), pay = 0, intr = 0, link = 0;
    for (var i = 0; i < n; i++) { pay += R.pay[i]; intr += R.intr[i]; link += R.link[i]; }
    o.pay = pay; o.intr = intr; o.link = link; o.bal = o.end ? 0 : R.bal[h - 1];
    o.fee = 0; o.cpiFee = 0; o.notice = 0; o.op = 0; o.feeBy = [];
    if (!o.end) {
      rows.forEach(function (t, k) {
        var S = R.T[k], b = S.bal[h - 1]; if (!(b > 0.5)) return;
        var f = L().prepayFee(t, { month: h, amount: b, before: b, rate: S.rate[h - 1], share: 1, endBefore: S.end }, D, drop || 0);
        o.fee += f.cap; o.cpiFee += f.cpi; o.notice += f.notice; o.feeBy.push({ k: t.k, cap: f.cap, why: f.why, cut: f.cut || 0, avg: f.avg });
      });
      o.op = D.fees.operational_max;
    }
    o.price = pay + o.bal + o.fee - o.loan;
    return o;
  }
  function exitScenario(D) {
    var POL = D.policy, FC = D.forecast;
    return L().scenario({ cpi: FC.inflation_4q, prime: 'boi', rampTo: FC.rate_q3_2027 - POL.rate, rampMonths: rampMonths(D) });
  }

  /* the Bank of Israel averages for the fee (prepay.nl / prepay.cpi: one row per month, effective annual %, in force from the
     date in column 0); bucket columns by the years to repay (or to the rate change on a variable loan) */
  var BLAB = { gt25: 'מעל 25 שנים', '20_25': 'מעל 20 ועד 25 שנים', '15_20': 'מעל 15 ועד 20 שנים', '10_15': 'מעל 10 ועד 15 שנים', '5_10': 'מעל 5 ועד 10 שנים', '1_5': 'מעל שנה ועד 5 שנים', le1: 'עד שנה', le5: 'עד 5 שנים' };
  function colFor(file, y) {
    if (file === 'cpi') return y <= 5 ? 'le5' : y <= 10 ? '5_10' : y <= 15 ? '10_15' : y <= 20 ? '15_20' : y <= 25 ? '20_25' : 'gt25';
    return y <= 1 ? 'le1' : y <= 5 ? '1_5' : y <= 10 ? '5_10' : y <= 15 ? '10_15' : y <= 20 ? '15_20' : y <= 25 ? '20_25' : 'gt25';
  }
  function avgRow(D, file, iso) { var T = D.prepay && D.prepay[file], r = null; if (!T) return null; T.rows.forEach(function (x) { if (x[0] <= iso) r = x; }); return r; }
  function avgOf(D, file, row, col) { var T = D.prepay[file], i = T.cols.indexOf(col); return row && i > -1 ? row[i] : null; }
  function cpiAt(C, k) { if (!C) return null; var ks = Object.keys(C.months).sort(), v = null; ks.forEach(function (x) { if (x <= k) v = C.months[x]; }); return v; }
  /* the average rate on new mortgages in a month, for a reader who does not remember the rate (flows, BIR_MRTG_99) */
  function rateIn(D, k, month) {
    var F = D.flows; if (!F) return null; var i = F.months.indexOf(month); if (i < 0) return null;
    if (k === 'fixed_nl') return F.series.rate_fixed_nl.v[i];
    if (k === 'fixed_cpi') return F.series.rate_fixed_cpi.v[i];
    if (k === 'var_cpi') return F.series.rate_var_cpi_bench.v[i] + F.series.rate_var_cpi_margin.v[i];
    return null;
  }
  /* the fee of a loan taken in the past, repaid in full in month `now`. o: { date: "2024-11", amount, years, k, rate (nominal %) }.
     The balance: NLMG.track at the loan's rate (a variable loan: as if today's rate ran from the start); a linked balance is
     indexed by the CPI from the loan month. The averages: today's for the years left (to the change day on a variable loan) and
     the one in force on the 15th of the loan month for the loan's term (5 years on a variable one). Unknown average at origination
     (before the file): only s.3(3) is tested. */
  function feeExisting(o, D, C, now) {
    var K = KIND[o.k], N = Math.round(o.years * 12), el = Math.max(0, Math.min(N - 1, mDiff(o.date, now)));
    var S = L().track({ amount: o.amount, rate: o.rate, years: o.years, method: 'spitzer', kind: K.kind, linked: false }, L().scenario({}));
    var real = el ? S.bal[el - 1] : o.amount, ratio = 1, c0 = null, c1 = null;
    if (K.linked && C) { c0 = cpiAt(C, o.date); c1 = cpiAt(C, now); if (c0 && c1) ratio = c1 / c0; }
    var B = real * ratio, left = N - el, file = K.file, out = { el: el, N: N, left: left, real: real, ratio: ratio, bal: B, kind: K.kind, linked: K.linked, file: file, f3: null, f4: null };
    var h = left; if (K.kind === 'var5') { var next = 60 * Math.ceil(el / 60) + 1; h = Math.min(left, next - 1 - el); }
    out.h = h;
    var rows = D.prepay[file].rows, today = rows[rows.length - 1], orig = avgRow(D, file, o.date + '-15');
    var colA = colFor(file, Math.max(h, 1) / 12), colC = colFor(file, K.kind === 'var5' ? Math.min(5, o.years) : o.years);
    var Ae = avgOf(D, file, today, colA), Ce = orig ? avgOf(D, file, orig, colC) : null;
    var A = L().ef2nom(Ae), Cn = Ce != null ? L().ef2nom(Ce) : null;
    Object.assign(out, { Ae: Ae, A: A, Ce: Ce, C: Cn, colA: colA, colC: colC, labA: BLAB[colA], labC: BLAB[colC], todayFrom: today[0], origFrom: orig ? orig[0] : null });
    var Csyn = Cn != null ? Cn : o.rate + 1;  // an unknown average at origination: put it above the loan rate, so s.3(4) stays out
    var Dsyn = { fees: D.fees, cpi: D.cpi, term: {} }; Dsyn.term[file] = { buckets: [{ from: 0, to: null, nom: Csyn, label: BLAB[colA] }] };
    var f = L().prepayFee({ kind: K.kind, linked: K.linked, method: 'spitzer' }, { month: el, amount: B, before: B, rate: o.rate, share: 1, endBefore: N }, Dsyn, Csyn - A);
    out.fee = f.cap; out.cut = f.cut || 0; out.why = f.why; out.op = f.op; out.notice = f.notice; out.cpiFee = f.cpi;
    if (K.kind !== 'prime' && h > 0 && f.why !== 'reset') {  // the two tests of s.3, shown to the reader (the same stream and discounting)
      var s = L().stream(B, o.rate, left, h, 'spitzer'), pvA = L().pv(s, A);
      out.f3 = A < o.rate ? Math.max(0, pvA - B) : 0;
      out.f4 = Cn != null && Cn < o.rate ? Math.max(0, pvA - L().pv(s, Cn)) : null;
    }
    return out;
  }

  /* round E (HAD-675, 6.11.2026): "האם למחזר?" in mexit's "משכנתא שכבר יש לי". The Bank of Israel average for a new loan in the same
     track: a fixed track at the average of the term-to-maturity file in force today for the months left (prepay.nl / prepay.cpi,
     the same column as s.3(3) of the fee); prime and the two variable tracks at the track's average on new mortgages of all the
     banks in the latest month (by_bank, TamInt010.xls), because their rate is set to the next change day, not to the end.
     Effective annual % turned nominal for a monthly payment (NLMG.ef2nom), like every other figure of the page. */
  function refiAvg(D, k, left) {
    var K = KIND[k]; if (!K) return null;
    if (K.kind === 'fixed') {
      var T = D.prepay && D.prepay[K.file]; if (!T) return null;
      var row = T.rows[T.rows.length - 1], col = colFor(K.file, Math.max(left, 1) / 12), e = avgOf(D, K.file, row, col);
      return e == null ? null : { eff: e, nom: L().ef2nom(e), via: 'prepay', file: K.file, col: col, lab: BLAB[col], from: row[0], month: String(row[1]).slice(0, 7), src: T.src };
    }
    var m = bankMix(D, 'system'); if (!m) return null;
    var r = m.rows.filter(function (x) { return x.k === k; })[0]; if (!r || !(r.eff > 0)) return null;
    return { eff: r.eff, nom: r.rate, via: 'by_bank', month: m.month, src: D.by_bank.src };
  }
  /* the balance of feeExisting refinanced today for the months left, at the average (or at o.newRate, the reader's offer, nominal %).
     Payments by NLMG.pmt on the same balance and months: today's at the loan's rate (on a Spitzer loan it is the payment being paid
     now; on a linked one, in today's shekels with the index so far), the new one at the new rate. One-off costs: the capitalization
     fee, the operational fee (up to fees.operational_max), the 0.1% short-notice fee when o.notice is not false, and o.extra (the
     reader's appraiser or file costs: not in any official file, so 0 unless typed). months = ceil(costs / monthly saving); null when
     the saving is under half a shekel (shown as "לא משתלם כרגע"). The fee and costs are paid up front, not added to the new loan. */
  function refiExisting(o, D, C, now, fx) {
    fx = fx || feeExisting(o, D, C, now);
    var avg = refiAvg(D, o.k, fx.left), own = o.newRate != null && isFinite(o.newRate);
    var nom = own ? +o.newRate : avg ? avg.nom : null; if (nom == null) return null;
    var n = fx.left, oldPay = L().pmt(fx.bal, o.rate / 1200, n), newPay = L().pmt(fx.bal, nom / 1200, n), save = oldPay - newPay;
    var notice = o.notice === false ? 0 : fx.notice, extra = Math.max(0, +o.extra || 0), cost = fx.fee + fx.op + notice + extra;
    var months = save >= 0.5 ? Math.ceil(cost / save) : null;
    return { fx: fx, avg: avg, own: own, rate: nom, left: n, bal: fx.bal, oldPay: oldPay, newPay: newPay, save: save,
      fee: fx.fee, op: fx.op, notice: notice, cpiFee: fx.cpiFee, extra: extra, cost: cost, months: months, within: months != null && months <= n };
  }

  var NLMR = { TK: TK, KIND: KIND, NAME: NAME, SHORT: SHORT, COL: COL, BASKET_KEY: BASKET_KEY, REPLAY: REPLAY, BLAB: BLAB,
    pick: pick, mAdd: mAdd, mDiff: mDiff, nowKey: nowKey, lastDay: lastDay, parseMonth: parseMonth,
    bankMix: bankMix, bankList: bankList, mathRows: mathRows, basketRows: basketRows,
    quarter: quarter, rampMonths: rampMonths, pathPay: pathPay, decision: decision, ladderPay: ladderPay, pathMix: pathMix,
    boiOn: boiOn, replayPath: replayPath, replay: replay,
    exitAt: exitAt, exitScenario: exitScenario, colFor: colFor, avgRow: avgRow, avgOf: avgOf, cpiAt: cpiAt, rateIn: rateIn, feeExisting: feeExisting,
    refiAvg: refiAvg, refiExisting: refiExisting };
  G.NLMR = NLMR;
  if (typeof document === 'undefined') return;  // node: the math only

  /* ===================================================================================================== the page parts */
  function NI() { return G.NadLanInstruments; }
  var nf0 = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  var LRI = '⁦', PDI = '⁩';  // a signed amount keeps its sign on the left inside Hebrew text (as tools/mortgage.js does)
  var F = {
    ils: function (n) { return NI().fmt.ils(n); },
    sils: function (n) { return LRI + (n < -0.5 ? '−' : '+') + NI().fmt.ils(Math.abs(n)) + PDI; },
    num: function (n, d) { return NI().fmt.num(n, d); },
    pc: function (n, d) { return NI().fmt.num(n, d == null ? 2 : d) + '%'; },
    spc: function (n, d) { return LRI + (n < 0 ? '−' : n > 0 ? '+' : '') + NI().fmt.num(Math.abs(n), d == null ? 2 : d) + '%' + PDI; },
    date: function (iso) { return NI().fmt.date(iso); },
    month: function (k) { return NI().fmt.month(k); },
    mshort: function (k) { return (+k.slice(5, 7)) + '.' + k.slice(2, 4); }
  };
  function esc(s) { return NI().esc(s); }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function num(v) { var n = parseFloat(String(v == null ? '' : v).replace(/[^\d.\-−]/g, '').replace('−', '-')); return isFinite(n) ? n : NaN; }

  function css() {
    if (document.getElementById('mrx-css')) return;
    var s = document.createElement('style'); s.id = 'mrx-css';
    s.textContent = [
      '.mrx .mrx__sec{margin:24px 0 0;padding:16px 0 0;border-top:1px solid var(--nli-line);position:relative;min-width:0}',
      'html body .nli .mrx h3.mrx__h{font:600 20px/28px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 6px !important;letter-spacing:0;text-transform:none}',
      '.mrx__p{font:400 14px/22px var(--nli-sans);color:var(--nli-ink2);margin:0 0 12px;max-width:72ch}',
      'html body .nli .mrx .nli__fig.is-key{color:var(--nli-ink);text-decoration:underline;text-decoration-color:var(--nli-survey);text-decoration-thickness:2px;text-underline-offset:8px;margin:4px 0 10px}',
      '.mrx .nli__answer{border-color:var(--nli-sea);background:var(--nli-surface)}',
      'html body .nli .mrx .nli__fig.is-he{font:600 30px/38px var(--nli-sans);direction:rtl;unicode-bidi:isolate;text-align:right}',  // round E: "162 חודשים", "לא משתלם כרגע"
      '.mrx .mrx__rfg{margin-top:4px}',
      '.mrx__al{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}',
      '.mrx__eg{font:500 12px/16px var(--nli-sans);color:var(--nli-mute);border:1px solid var(--nli-line);border-radius:999px;padding:2px 10px;white-space:nowrap}',
      '.mrx__src{font:400 12px/18px var(--nli-mono),var(--nli-sans);color:var(--nli-mute);margin:0;overflow-wrap:anywhere}',
      '.mrx__src a{color:var(--nli-sea)}',
      '.mrx__hint{font:400 13px/19px var(--nli-sans);color:var(--nli-mute);margin:0}',
      'html body .nli .mrx .nli__lines dt{min-width:0;flex:1 1 auto}',
      'html body .nli .mrx .nli__lines dd{flex:none;white-space:nowrap;max-width:none}',
      'html body .nli .mrx .nli__lines dd.he{flex:0 1 auto;white-space:normal;max-width:50%;direction:rtl;unicode-bidi:isolate;text-align:left;font-family:var(--nli-sans);font-weight:500}',
      '.mrx__box{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);padding:12px;display:grid;gap:12px;background:var(--nli-ground)}',
      '.mrx__two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px 10px}',
      '.mrx__two.is-amt{grid-template-columns:minmax(0,1.75fr) minmax(0,1fr)}',
      '.mrx__mix{display:grid;gap:6px}',
      '.mrx__mr{display:grid;grid-template-columns:minmax(0,1fr) 88px 92px;gap:8px;align-items:center}',
      'html body .nli .mrx__mr .nli__in input,html body .nli .mrx__rg .nli__in input,html body .nli .mrx__rg .nli__in select{font-size:16px;padding:9px 8px;min-height:44px}',
      '.mrx__mr .nli__unit{padding:0 6px}',
      '.mrx__mh span{font:500 12px/16px var(--nli-sans);color:var(--nli-mute)}',
      '.mrx__tn{font:500 14px/18px var(--nli-sans);color:var(--nli-ink);display:flex;align-items:center;gap:8px;min-width:0}',
      '.mrx__tn i{width:10px;height:10px;border-radius:2px;flex:none;display:inline-block}',
      '.mrx__sum{font:500 13px/18px var(--nli-sans);color:var(--nli-ink2);margin:0}.mrx__sum bdi{font-family:var(--nli-mono)}',
      '.mrx__rows{display:grid;gap:10px}',
      '.mrx__row{border:1px solid var(--nli-line);border-inline-start:4px solid var(--c,#2F6F86);border-radius:var(--nli-r-s);padding:10px;background:var(--nli-surface);display:grid;gap:8px}',
      '.mrx__rh{display:flex;gap:8px;align-items:flex-end}.mrx__rh>.nli__f{flex:1}',
      'html body .nli .mrx button.mrx__x{min-height:44px;min-width:44px;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);color:var(--nli-ink2);cursor:pointer;font:400 18px/1 var(--nli-sans);margin:0;padding:0}',
      '.mrx__rg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}',
      '.mrx__rg label{font:500 12px/16px var(--nli-sans) !important;color:var(--nli-ink2) !important}',
      'html body .nli .mrx__rg .nli__in input{font-size:16px;padding:9px 8px}',
      '.mrx__chart{margin:0;min-width:0}',
      '.mrx__chart svg{display:block;width:100%;height:auto;direction:ltr}',
      '.mrx__chart svg text{font:400 11px var(--nli-mono);fill:#5E6A75}',
      '.mrx__chart svg text.he{font-family:var(--nli-sans);font-size:12px}',
      '.mrx__chart svg text.k{fill:#12202A;font-weight:500}',
      '.mrx__lg{display:flex;flex-wrap:wrap;gap:4px 14px;list-style:none;margin:8px 0 0;padding:0;font:400 12px/16px var(--nli-sans);color:var(--nli-ink2)}',
      '.mrx__lg li{margin:0;display:flex;gap:6px;align-items:center}.mrx__lg i{width:10px;height:10px;border-radius:2px;display:inline-block}.mrx__lg i.d{height:0;border-top:2px dashed #2F6F86;border-radius:0}',
      '.mrx__tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface)}',
      'html body .nli .mrx table.mrx__t{width:100%;border-collapse:collapse;margin:0;display:table !important;font:400 14px/20px var(--nli-sans)}',
      'html body .nli .mrx table.mrx__t thead{display:table-header-group !important}html body .nli .mrx table.mrx__t tbody{display:table-row-group !important}html body .nli .mrx table.mrx__t tr{display:table-row !important}',
      'html body .nli .mrx table.mrx__t th,html body .nli .mrx table.mrx__t td{display:table-cell !important;padding:8px !important;border:0 !important;border-bottom:1px solid var(--nli-line) !important;text-align:right;vertical-align:middle;background:none !important;color:var(--nli-ink);font-size:14px !important;line-height:20px !important;width:auto !important;white-space:nowrap}',
      'html body .nli .mrx table.mrx__t th{font-weight:500;color:var(--nli-mute);font-size:12px !important;line-height:16px !important;white-space:normal;font-family:var(--nli-sans) !important}',
      'html body .nli .mrx table.mrx__t td.n{font-family:var(--nli-mono) !important;font-size:13px !important;direction:ltr;unicode-bidi:plaintext;text-align:right;font-variant-numeric:tabular-nums}',
      'html body .nli .mrx table.mrx__t td small{display:block;font:400 11px/15px var(--nli-sans);color:var(--nli-mute);white-space:normal}',
      'html body .nli .mrx table.mrx__t tr.is-on td{background:var(--nli-ground) !important;font-weight:600}',
      'html body .nli .mrx table.mrx__t tr.is-you td{font-weight:600}',
      '.mrx__tag{display:inline-block;font:500 11px/15px var(--nli-sans);color:#fff;background:#2F6F86;border-radius:999px;padding:1px 8px;margin-inline-start:6px;white-space:nowrap}',
      '.mrx__tag.is-ink{background:#12202A}',
      'html body .nli .mrx details.mrx__more>summary{font:500 15px/22px var(--nli-sans);color:var(--nli-sea);cursor:pointer;min-height:44px;display:flex;align-items:center;border:0 !important;padding:0 !important;background:none !important}',
      /* a wide table turns into one card per row on phones: every value under its own column name */
      '@media (max-width:600px){html body .nli .mrx table.mrx__t.is-cards thead{display:none !important}html body .nli .mrx table.mrx__t.is-cards,html body .nli .mrx table.mrx__t.is-cards tbody{display:block !important}' +
        'html body .nli .mrx table.mrx__t.is-cards tr{display:grid !important;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:6px 12px;padding:10px 12px;border-bottom:1px solid var(--nli-line)}' +
        'html body .nli .mrx table.mrx__t.is-cards td{display:block !important;border:0 !important;padding:0 !important;white-space:normal;text-align:right !important;background:none !important}' +
        'html body .nli .mrx table.mrx__t.is-cards td:empty{display:none !important}' +
        'html body .nli .mrx table.mrx__t.is-cards td[data-l]::before{content:attr(data-l);display:block;font:500 11px/15px var(--nli-sans);color:var(--nli-mute);direction:rtl;text-align:right}' +
        'html body .nli .mrx table.mrx__t.is-cards td:first-child{grid-column:1/-1;font-weight:600}html body .nli .mrx table.mrx__t.is-cards tr.is-on,html body .nli .mrx table.mrx__t.is-cards tr.is-you{background:var(--nli-ground)}}',
      '@media (max-width:420px){.mrx__mr{grid-template-columns:minmax(0,1fr) 80px 86px;gap:6px}.mrx__rg{grid-template-columns:repeat(2,minmax(0,1fr))}}',
      '@media print{.mrx .nli__seg,.mrx .nli__share,.mrx button.mrx__x,.mrx .nli__add{display:none !important}}'
    ].join('\n');
    document.head.appendChild(s);
  }

  /* a field like the engine's: label, a box with the input and its unit, a help line */
  function field(label, val, unit, on, o) {
    o = o || {};
    var w = el('div', 'nli__f'), id = 'mrx-' + Math.random().toString(36).slice(2, 8);
    var lab = el('label', '', esc(label)); lab.htmlFor = id; w.appendChild(lab);
    var box = el('div', 'nli__in'), inp = el('input'); inp.id = id; inp.autocomplete = 'off';
    if (o.type === 'text') { inp.type = 'text'; inp.inputMode = 'decimal'; if (o.ph) inp.placeholder = o.ph; inp.value = val || ''; }  // a month as 11.2024: the same in every browser and locale
    else { inp.type = 'text'; inp.inputMode = 'decimal'; inp.value = val == null || !isFinite(val) ? '' : (o.money ? nf0.format(val) : String(o.dec != null ? Math.round(val * Math.pow(10, o.dec)) / Math.pow(10, o.dec) : val)); }
    inp.addEventListener('input', function () { on(o.type === 'text' ? inp.value : num(inp.value)); });
    if (o.money) inp.addEventListener('blur', function () { var n = num(inp.value); if (isFinite(n)) inp.value = nf0.format(n); });
    box.appendChild(inp); if (unit) box.appendChild(el('span', 'nli__unit', esc(unit)));
    w.appendChild(box); if (o.help) w.appendChild(el('span', 'nli__help', o.help));
    var err = el('span', 'nli__err'); err.setAttribute('aria-live', 'polite'); w.appendChild(err);
    w._inp = inp; w._err = err; return w;
  }
  function seg(label, opts, cur, on) {
    var w = el('div', 'nli__f'); w.appendChild(el('span', 'nli__lab', esc(label)));
    var g = el('div', 'nli__seg'); g.setAttribute('role', 'group'); g.setAttribute('aria-label', label);
    opts.forEach(function (o) {
      var b = el('button', '', esc(o[1])); b.type = 'button'; b.setAttribute('aria-pressed', String(o[0] === cur));
      b.addEventListener('click', function () { [].forEach.call(g.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); on(o[0]); });
      g.appendChild(b);
    });
    w.appendChild(g); w._g = g; return w;
  }
  function select(label, opts, cur, on) {
    var w = el('div', 'nli__f'), id = 'mrx-' + Math.random().toString(36).slice(2, 8);
    var lab = el('label', '', esc(label)); lab.htmlFor = id; w.appendChild(lab);
    var box = el('div', 'nli__in'), s = el('select'); s.id = id;
    opts.forEach(function (o) { var op = el('option', '', esc(o[1])); op.value = o[0]; if (o[0] === cur) op.selected = true; s.appendChild(op); });
    s.addEventListener('change', function () { on(s.value); });
    box.appendChild(s); w.appendChild(box); return w;
  }
  function lines(list) {  // a value with Hebrew words reads right to left and may wrap; a figure stays on one line
    var dl = el('dl', 'nli__lines');
    list.forEach(function (x) { if (x) dl.appendChild(el('div', '', '<dt>' + esc(x[0]) + '</dt><dd' + (/[֐-׿]/.test(x[1]) ? ' class="he"' : '') + '>' + esc(x[1]) + '</dd>')); });
    return dl;
  }
  /* the answer: one decisive number, ink with the survey underline (the only red on the screen), a "דוגמה" tag until the first edit */
  function answer(label, value, sub, ex) {
    var a = el('div', 'nli__answer');
    a.innerHTML = '<div class="mrx__al"><span class="nli__alab">' + esc(label) + '</span>' + (ex ? '<span class="mrx__eg">דוגמה, שנו כל שדה</span>' : '') + '</div>' +
      '<output class="nli__fig is-key">' + esc(value) + '</output>' + (sub ? '<span class="nli__asub">' + sub + '</span>' : '');
    return a;
  }
  function table(head, rows, o) {  // o.num: figure columns; o.cards: one card per row on phones
    o = o || {};
    var h = '<table class="mrx__t' + (o.cards ? ' is-cards' : '') + '"><thead><tr>' + head.map(function (x) { return '<th scope="col">' + esc(x) + '</th>'; }).join('') + '</tr></thead><tbody>';
    rows.forEach(function (r) { h += '<tr' + (r.cls ? ' class="' + r.cls + '"' : '') + '>' + r.cells.map(function (c, i) { return '<td' + ((o.num || []).indexOf(i) > -1 ? ' class="n"' : '') + (o.cards && i && c !== '' ? ' data-l="' + esc(head[i]) + '"' : '') + '>' + c + '</td>'; }).join('') + '</tr>'; });
    return el('div', 'mrx__tw', h + '</tbody></table>');
  }
  /* a source of the data file in Hebrew: sources[] carries the Hebrew label of a file whose own src label is in English */
  function srcHe(D, s, key) { var h = (D.sources || []).filter(function (x) { return x.url && key && x.url.indexOf(key) > -1; })[0]; return h ? { label: h.label, url: s && s.url ? s.url : h.url } : s; }
  function legend(items) { return el('ul', 'mrx__lg', items.map(function (x) { return '<li><i' + (x[2] ? ' class="' + x[2] + '"' : '') + ' style="background:' + x[0] + '"></i>' + esc(x[1]) + '</li>'; }).join('')); }
  function niceMax(v) { if (!(v > 0)) return 1; var p = Math.pow(10, Math.floor(Math.log10(v))), x = v / p; return (x <= 1 ? 1 : x <= 2 ? 2 : x <= 2.5 ? 2.5 : x <= 5 ? 5 : 10) * p; }

  /* the panel: kicker, title, lede, strip, form | result, sections, sources, share, the example line */
  function panel(root, o) {
    root.innerHTML = '';
    if (!root.parentNode || !root.parentNode.closest || !root.parentNode.closest('.nli')) root.classList.add('nli');
    root.setAttribute('dir', 'rtl');
    var p = el('div', 'nli__panel mrx'), X = {};
    p.appendChild(el('p', 'nli__kicker', esc(o.kicker)));
    p.appendChild(el('h2', 'nli__title', esc(o.title)));
    p.appendChild(el('p', 'nli__lede', o.lede));
    if (o.strip && o.strip.length) { var sp = el('div', 'nli__strip'); o.strip.forEach(function (x) { sp.appendChild(el('div', '', '<span>' + esc(x[0]) + '</span><strong>' + esc(x[1]) + '</strong>')); }); p.appendChild(sp); }
    X.top = el('div', ''); p.appendChild(X.top);
    var grid = el('div', 'nli__grid'); X.form = el('form', 'nli__form'); X.form.addEventListener('submit', function (e) { e.preventDefault(); });
    X.out = el('div', 'nli__out'); X.out.setAttribute('aria-live', 'polite');
    grid.appendChild(X.form); grid.appendChild(X.out); p.appendChild(grid);
    X.secs = el('div', ''); p.appendChild(X.secs);
    X.share = el('div', 'nli__share'); p.appendChild(X.share);
    p.appendChild(el('p', 'nli__eg', '<b>דוגמה</b>' + esc(o.eg)));
    root.appendChild(p); X.panel = p;
    return X;
  }
  function sec(box, title, lead) { var s = el('section', 'mrx__sec'); s.appendChild(el('h3', 'mrx__h', esc(title))); if (lead) s.appendChild(el('p', 'mrx__p', lead)); box.appendChild(s); return s; }

  /* the case in the address: #mreplay=... reopens the same numbers (like #mortgage= of the main calculator) */
  function enc(o) { return btoa(unescape(encodeURIComponent(JSON.stringify(o)))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); }
  function fromHash(id) {
    var m = new RegExp('#' + id + '=([A-Za-z0-9_\\-]+)').exec(location.hash || ''); if (!m) return null;
    try { var b = m[1].replace(/-/g, '+').replace(/_/g, '/'); while (b.length % 4) b += '='; return JSON.parse(decodeURIComponent(escape(atob(b)))); } catch (e) { return null; }
  }
  function link(id, o) { return (location.origin && location.origin !== 'null' ? location.origin + location.pathname : location.href.split('#')[0]) + '#' + id + '=' + enc(o); }
  var ICON = { copy: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 7h9v10H7z"/><path d="M4 13V3h9"/></svg>', wa: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16l1-3.2A7 7 0 1 1 7.6 15z"/></svg>',
    link: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M8 12l4-4"/><path d="M9 5l2-2a3 3 0 0 1 4 4l-2 2"/><path d="M11 15l-2 2a3 3 0 0 1-4-4l2-2"/></svg>', print: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 8V3h10v5"/><path d="M5 14H3V8h14v6h-2"/><path d="M6 12h8v5H6z"/></svg>' };
  function shareBar(box, text, url) {
    box.innerHTML = '';
    function copy(btn, txt, lab) { var sp = btn.querySelector('span'); var done = function () { sp.textContent = 'הועתק'; setTimeout(function () { sp.textContent = lab; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, function () { window.prompt('העתיקו', txt); }); else window.prompt('העתיקו', txt); }
    var b1 = el('button', 'is-primary', ICON.copy + '<span>העתקת התוצאה</span>'); b1.type = 'button'; b1.addEventListener('click', function () { copy(b1, text() + '\n' + url(), 'העתקת התוצאה'); });
    var b2 = el('a', '', ICON.wa + '<span>שליחה בוואטסאפ</span>'); b2.target = '_blank'; b2.rel = 'noopener'; b2.href = 'https://wa.me/'; b2.addEventListener('click', function () { b2.href = 'https://wa.me/?text=' + encodeURIComponent(text() + '\n' + url()); });
    var b3 = el('button', '', ICON.link + '<span>קישור למקרה הזה</span>'); b3.type = 'button'; b3.addEventListener('click', function () { copy(b3, url(), 'קישור למקרה הזה'); });
    var b4 = el('button', '', ICON.print + '<span>הדפסה או שמירה כקובץ</span>'); b4.type = 'button'; b4.addEventListener('click', function () { window.print(); });
    [b1, b2, b3, b4].forEach(function (b) { box.appendChild(b); });
  }

  /* the mix editor of mreplay and mexit: the average of all banks or one of the five largest, or the reader's own; five tracks,
     share and rate each. st: { src, rows: [{k, share, rate}] } */
  function mixEditor(box, st, D, onChange) {
    box.innerHTML = '';
    var list = bankList(D), month = D.by_bank && D.by_bank.latest ? D.by_bank.latest.month : null;
    var w = seg('התמהיל והריביות', list.map(function (b) { return [b.k, b.he]; }), st.src, function (k) { var m = bankMix(D, k); if (!m) return; st.src = k; st.rows = m.rows.map(function (r) { return { k: r.k, share: r.share, rate: r.rate }; }); draw(); onChange(); });
    box.appendChild(w);
    var grid = el('div', 'mrx__mix'); box.appendChild(grid);
    var sum = el('p', 'mrx__sum'); box.appendChild(sum);
    box.appendChild(el('p', 'nli__help', 'נפתח בממוצע של ' + esc(month ? F.month(month) : '') + ' לפי בנק ישראל: החלק של כל מסלול בכסף שניתן באותו חודש, והריבית הממוצעת בו כריבית שנתית לתשלום חודשי. הקלידו את התמהיל ואת הריביות שלכם.'));
    function paintSum() { var t = st.rows.reduce(function (a, r) { return a + (+r.share || 0); }, 0); sum.innerHTML = 'סך החלקים: <bdi>' + esc(F.num(t, 1)) + '%</bdi>' + (Math.abs(t - 100) > 0.6 ? ' · חישבנו לפי היחס ביניהם' : ''); }
    function draw() {
      grid.innerHTML = '';
      var hd = el('div', 'mrx__mr mrx__mh', '<span>מסלול</span><span>חלק</span><span>ריבית שנתית</span>'); hd.setAttribute('aria-hidden', 'true'); grid.appendChild(hd);
      st.rows.forEach(function (r) {
        var row = el('div', 'mrx__mr');
        row.appendChild(el('span', 'mrx__tn', '<i style="background:' + COL[r.k] + '"></i>' + esc(NAME[r.k])));
        var a = field('חלק, ' + NAME[r.k], r.share, '%', function (n) { r.share = isFinite(n) ? Math.max(0, n) : 0; own(); paintSum(); onChange(); }, { dec: 1 });
        var b = field('ריבית, ' + NAME[r.k], r.rate, '%', function (n) { r.rate = n; own(); onChange(); }, { dec: 2 });
        [a, b].forEach(function (f) { f.querySelector('label').className = 'nli__sr'; f.querySelector('label').style.cssText = 'position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)'; f._err.remove(); row.appendChild(f); });
        grid.appendChild(row);
      });
      [].forEach.call(w._g.children, function (x, i) { x.setAttribute('aria-pressed', String(list[i].k === st.src)); });
      paintSum();
    }
    function own() { if (st.src !== 'own') { st.src = 'own'; [].forEach.call(w._g.children, function (x) { x.setAttribute('aria-pressed', 'false'); }); } }
    draw();
  }

  /* start a tool once the math (NLMG, NLMR) and the data are in; the scripts may arrive in any order */
  function start(root, data, build) {
    css();
    var X = pick(data);
    if (!X.D || !X.D.policy) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
    build(root, X);
  }
  function resized(fn) { var t = 0, w = window.innerWidth; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(function () { if (Math.abs(window.innerWidth - w) > 30) { w = window.innerWidth; fn(); } }, 180); }); }

  NLMR.ui = { F: F, esc: esc, el: el, num: num, css: css, field: field, seg: seg, select: select, lines: lines, answer: answer, table: table, srcHe: srcHe, legend: legend, niceMax: niceMax,
    panel: panel, sec: sec, fromHash: fromHash, link: link, shareBar: shareBar, mixEditor: mixEditor, start: start, resized: resized };
})();
