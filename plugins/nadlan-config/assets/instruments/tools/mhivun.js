/* NadLan Instruments · mhivun v1 (HAD-675, 6.11.2026): "עמלת היוון", the early-repayment capitalization fee of a whole mortgage by
   the Banking Order (צו הבנקאות (עמלת פירעון מוקדם), התשס"ב-2002), for /mortgage-calculator/. Hebrew only, RTL. LOCAL BUILD: staged
   in docs/research/2026-11-06-mortgage-universe/build/build-mhivun/ (README, node test, preview, browser check, registry snippet).
   What it does:
   - up to 6 tracks of one mortgage, each with its own track, amount, start month, term (years or months), rate today and, on a
     variable track, how often the rate changes (every 1, 2, 2.5, 5 or 10 years);
   - per track today: the balance, the capitalization fee, the age discount, the Bank of Israel average used (its remaining-term
     column, value and in-force date), the 0.1% short-notice fee; the total for the mortgage with the operational fee once;
     never a bare zero: a track without a fee says why (prime, a rate that changes yearly, the change day, the average);
   - "איך זה חושב": every step with its numbers (payments left, present value at the loan rate, today's average and the loan-day
     average, the two calculations of s.3, the lower one, the discount, the result);
   - partial prepayment: the amount split across the tracks to pay the least fee (tracks without a capitalization fee first, then
     by the fee per shekel, ties to the higher rate), with the fee, the payment drop (or the months cut) and the interest saved;
   - when to prepay: the fee of a full payoff in each of the next 24 months with today's averages, and with them 0.5 point lower
     and higher; the 3 and 5 year discount months and every change day of a variable track; the cheapest month; a table under
     the chart;
   - the bank's number: compared with ours, with the usual reasons for a gap (never an accusation);
   - a copyable Hebrew summary, the case in the address (#mhivun=), nothing personal asked, nothing sent anywhere.
   Math: every fee is NLMR.feeExisting of tools/mrates-common.js (on NLMG.prepayFee of tools/mortgage.js), called as is for the
   fixed tracks, prime and a variable track that changes every 5 years. A variable track with another cycle goes through feeFreq
   below: the steps of feeExisting line for line, with the change cycle FQ in place of its fixed 60 months (the next change day,
   and the loan-day average column of FQ years) and FQ handed to NLMG.prepayFee as t.freq, which already applies it (no
   capitalization fee when the rate changes at least yearly). test_mhivun.js checks that feeFreq with FQ = 60 returns exactly what
   feeExisting returns, field by field. Pure part in window.NLHV (runs in node); the page part needs core.js and NLMR.ui. */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;
  function L() { return G.NLMG; }
  function R() { return G.NLMR; }

  /* ------------------------------------------------------------------------------------------------------ the case */
  var TRACKS = ['fixed_nl', 'fixed_cpi', 'var_cpi', 'var_nl_other', 'prime'];
  var FREQ = [[12, 'כל שנה'], [24, 'כל שנתיים'], [30, 'כל שנתיים וחצי'], [60, 'כל 5 שנים'], [120, 'כל 10 שנים']];
  var MAXROWS = 6;
  /* the opening example, labelled as one on the page: a mortgage of 1,400,000 from 7.2023 in four tracks (typed rates, not averages) */
  var EXAMPLE = { date: '2023-07', pp: 200000, rows: [
    { k: 'fixed_nl', amount: 500000, term: 25, unit: 'y', rate: 5.3, freq: 60 },
    { k: 'prime', amount: 450000, term: 25, unit: 'y', rate: 4.15, freq: 60 },
    { k: 'var_cpi', amount: 300000, term: 25, unit: 'y', rate: 4.2, freq: 60 },
    { k: 'fixed_cpi', amount: 150000, term: 20, unit: 'y', rate: 3.9, freq: 60 }] };

  function isVar(k) { var K = R().KIND[k]; return !!K && K.kind === 'var5'; }
  function freqOf(r) { return isVar(r.k) ? (Math.round(+r.freq) || 60) : null; }
  function monthsOf(r) { return r.unit === 'm' ? Math.round(+r.term) : Math.round(+r.term * 12); }
  /* a calculation row: { k, amount, date "YYYY-MM", n (months), rate (nominal % today), freq (months, variable only), id } */
  function loanOf(r) { return { date: r.date, amount: +r.amount, years: r.n / 12, k: r.k, rate: +r.rate }; }

  /* NLMR.feeExisting with the change cycle FQ (months) of a variable track in place of its 60. Same order, same calls. */
  function feeFreq(o, D, C, now, FQ) {
    var M = L(), Q = R(), K = Q.KIND[o.k], N = Math.round(o.years * 12), el = Math.max(0, Math.min(N - 1, Q.mDiff(o.date, now)));
    var S = M.track({ amount: o.amount, rate: o.rate, years: o.years, method: 'spitzer', kind: K.kind, linked: false }, M.scenario({}));
    var real = el ? S.bal[el - 1] : o.amount, ratio = 1, c0 = null, c1 = null;
    if (K.linked && C) { c0 = Q.cpiAt(C, o.date); c1 = Q.cpiAt(C, now); if (c0 && c1) ratio = c1 / c0; }
    var B = real * ratio, left = N - el, file = K.file, out = { el: el, N: N, left: left, real: real, ratio: ratio, bal: B, kind: K.kind, linked: K.linked, file: file, f3: null, f4: null };
    var h = left; if (K.kind === 'var5') { var next = FQ * Math.ceil(el / FQ) + 1; h = Math.min(left, next - 1 - el); }
    out.h = h;
    var rows = D.prepay[file].rows, today = rows[rows.length - 1], orig = Q.avgRow(D, file, o.date + '-15');
    var colA = Q.colFor(file, Math.max(h, 1) / 12), colC = Q.colFor(file, K.kind === 'var5' ? Math.min(FQ / 12, o.years) : o.years);
    var Ae = Q.avgOf(D, file, today, colA), Ce = orig ? Q.avgOf(D, file, orig, colC) : null;
    var A = M.ef2nom(Ae), Cn = Ce != null ? M.ef2nom(Ce) : null;
    Object.assign(out, { Ae: Ae, A: A, Ce: Ce, C: Cn, colA: colA, colC: colC, labA: Q.BLAB[colA], labC: Q.BLAB[colC], todayFrom: today[0], origFrom: orig ? orig[0] : null });
    var Csyn = Cn != null ? Cn : o.rate + 1;
    var Dsyn = { fees: D.fees, cpi: D.cpi, term: {} }; Dsyn.term[file] = { buckets: [{ from: 0, to: null, nom: Csyn, label: Q.BLAB[colA] }] };
    var f = M.prepayFee({ kind: K.kind, linked: K.linked, method: 'spitzer', freq: FQ }, { month: el, amount: B, before: B, rate: o.rate, share: 1, endBefore: N }, Dsyn, Csyn - A);
    out.fee = f.cap; out.cut = f.cut || 0; out.why = f.why; out.op = f.op; out.notice = f.notice; out.cpiFee = f.cpi;
    if (K.kind !== 'prime' && h > 0 && f.why !== 'reset' && f.why !== 'prime') {
      var s = M.stream(B, o.rate, left, h, 'spitzer'), pvA = M.pv(s, A);
      out.f3 = A < o.rate ? Math.max(0, pvA - B) : 0;
      out.f4 = Cn != null && Cn < o.rate ? Math.max(0, pvA - M.pv(s, Cn)) : null;
    }
    return out;
  }
  /* one track repaid in full in month `now`: the shared function as is, or the same steps with another change cycle */
  function feeOne(r, D, C, now) {
    var FQ = freqOf(r), o = loanOf(r);
    return FQ == null || FQ === 60 ? R().feeExisting(o, D, C, now) : feeFreq(o, D, C, now, FQ);
  }
  /* why a track pays what it pays: fee | prime | yearly | reset | noavg (today's average not lower than the rate) | orig (the
     loan-day average was lower than today's, so s.3(4) is zero) | tiny (under half a shekel) */
  function status(fx, rate) {
    if (fx.kind === 'prime') return 'prime';
    if (fx.why === 'prime') return 'yearly';
    if (fx.why === 'reset') return 'reset';
    if (fx.fee >= 0.5) return 'fee';
    if (!(fx.A < rate)) return 'noavg';
    return fx.f4 === 0 ? 'orig' : 'tiny';
  }
  function freeByRule(s) { return s === 'prime' || s === 'yearly' || s === 'reset'; }

  /* the whole mortgage repaid in month `now`. The operational fee is counted once (one payoff request). */
  function mortgage(rows, D, C, now) {
    var o = { now: now, loans: [], bal: 0, fee: 0, notice: 0, cpiFee: 0, op: 0, n: 0, linked: false, vars: false };
    rows.forEach(function (r, idx) {
      var e = R().mDiff(r.date, now), l = { id: r.id != null ? r.id : idx, row: r, N: r.n, e: e, active: e >= 1 && e < r.n };
      if (l.active) {
        var fx = feeOne(r, D, C, now); l.fx = fx; l.status = status(fx, +r.rate); l.fps = fx.bal > 0 ? fx.fee / fx.bal : 0;
        o.bal += fx.bal; o.fee += fx.fee; o.notice += fx.notice; o.cpiFee += fx.cpiFee; o.n++;
        if (fx.linked) o.linked = true; if (fx.kind === 'var5') o.vars = true;
      } else l.status = e >= r.n ? 'ended' : 'future';
      o.loans.push(l);
    });
    o.op = o.n ? D.fees.operational_max : 0;
    return o;
  }
  function cpiKey(C, k) { if (!C) return null; var v = null; Object.keys(C.months).sort().forEach(function (x) { if (x <= k) v = x; }); return v; }
  /* the numbers behind one track's fee: the payments counted (NLMG.stream, the call prepayFee makes), their present value at the
     loan rate (= the balance), at today's average and at the loan-day average; the lower of s.3(3) and s.3(4) before the discount */
  function detail(l) {
    var fx = l.fx, r = l.row; if (!fx || freeByRule(l.status)) return null;
    var M = L(), Q = R(), s = M.stream(fx.bal, +r.rate, fx.left, fx.h, 'spitzer');
    var o = { n: s.length, first: s[0], last: s[s.length - 1], pvR: M.pv(s, +r.rate), pvA: M.pv(s, fx.A), pvC: fx.C != null ? M.pv(s, fx.C) : null };
    o.lower = fx.f4 == null ? fx.f3 : Math.min(fx.f3, fx.f4); o.which = fx.f4 != null && fx.f4 < fx.f3 ? 4 : 3;
    o.change = fx.kind === 'var5' && fx.h < fx.left ? Q.mAdd(r.date, fx.el + fx.h) : null;  // the next change day, when it comes before the end
    o.cut20 = Q.mAdd(r.date, 36); o.cut30 = Q.mAdd(r.date, 60);
    return o;
  }

  /* today's averages moved by d percentage points (both files), for the scenarios. The moved row is appended with an in-force date
     later than any loan day, so it is "today" for NLMR.feeExisting and never the average on the loan day. */
  function shiftD(D, d) {
    var P = Object.assign({}, D.prepay);
    ['nl', 'cpi'].forEach(function (f) {
      var T = D.prepay[f]; if (!T) return; var last = T.rows[T.rows.length - 1];
      var row = last.map(function (v, i) { return i < 2 || v == null ? v : Math.round((+v + d) * 1e6) / 1e6; });
      row[0] = '9999-12-31';
      P[f] = Object.assign({}, T, { rows: T.rows.concat([row]) });
    });
    return Object.assign({}, D, { prepay: P });
  }

  /* partial prepayment of X: the least capitalization fee. The fee of a partial payoff is the full fee times the share repaid
     (NLMG.prepayFee: cap x share), so the cheapest split fills the tracks by fee per shekel: first the ones with no fee by rule
     (prime, yearly, change day), then the lowest fee per shekel, ties to the higher rate (more interest saved).
     mode reduce: the term stays, the payment drops by pmt(a); shorten: the payment stays, the months fall. Interest saved to the
     end = the payments no longer paid less the amount repaid (today's shekels on a linked track, today's rate on prime/variable). */
  function cut(B, rm, left, a) {
    var M = L(), P = M.pmt(B, rm, left), b = B - a, n = 0, paid = 0;
    while (b > 0.005 && n < left) { var I = b * rm, pay = Math.min(P, b + I); b = b + I - pay; paid += pay; n++; }
    return { months: left - n, saved: P * left - paid - a, pay: P };
  }
  function allocate(MG, X, mode, D) {
    var M = L(), act = MG.loans.filter(function (l) { return l.active && l.fx.bal > 0.5; });
    var tot = act.reduce(function (s, l) { return s + l.fx.bal; }, 0), amt = Math.max(0, Math.min(+X || 0, tot));
    var ord = act.slice().sort(function (a, b) {
      return (freeByRule(b.status) ? 1 : 0) - (freeByRule(a.status) ? 1 : 0) || a.fps - b.fps || +b.row.rate - +a.row.rate || a.id - b.id;
    });
    var o = { asked: +X || 0, amount: amt, capped: (+X || 0) > tot + 0.5, total: tot, items: [], fee: 0, notice: 0, drop: 0, months: 0, saved: 0, mode: mode };
    var rest = amt;
    ord.forEach(function (l) {
      if (rest <= 0.005) return;
      var a = Math.min(rest, l.fx.bal), B = l.fx.bal, rm = +l.row.rate / 1200, left = l.fx.left; rest -= a;
      var it = { id: l.id, l: l, a: a, fee: l.fx.fee * a / B, notice: a * D.fees.notice_rate, full: a >= B - 0.005 };
      if (mode === 'shorten') { var c = cut(B, rm, left, a); it.months = c.months; it.saved = c.saved; it.drop = it.full ? c.pay : 0; }
      else { it.drop = M.pmt(B, rm, left) - M.pmt(B - a, rm, left); it.saved = it.drop * left - a; it.months = it.full ? left : 0; }
      o.items.push(it); o.fee += it.fee; o.notice += it.notice; o.drop += it.drop; o.saved += it.saved;
    });
    o.prop = tot > 0 ? MG.fee * amt / tot : 0;  // the same amount split by the balances
    return o;
  }

  /* the fee of a full payoff in each of the next `months` months (index 0 = now): today's averages, and moved -0.5 / +0.5.
     Events: the 3 and 5 year discounts (where there is a fee), every change day of a variable track, a track's average moving to
     another remaining-term column, a track ending. cheap = the cheapest month after now (0 when none is cheaper). */
  function strip(rows, D, C, now, months) {
    months = months || 24;
    var Q = R(), Dd = shiftD(D, -0.5), Du = shiftD(D, 0.5), prev = {};
    var o = { months: [], base: [], down: [], up: [], ev: [], by: [] };
    for (var j = 0; j <= months; j++) {
      var t = Q.mAdd(now, j), b = 0, dn = 0, up = 0, ev = [], by = [];
      rows.forEach(function (r, idx) {
        var id = r.id != null ? r.id : idx, e = Q.mDiff(r.date, t);
        if (e < 1 || e >= r.n) { if (e >= r.n && prev[id] && prev[id].on) ev.push({ t: 'end', id: id }); prev[id] = { on: false }; by.push(null); return; }
        var f = feeOne(r, D, C, t), s = status(f, +r.rate), FQ = freqOf(r);
        b += f.fee; by.push(f.fee);
        if (j) { dn += feeOne(r, Dd, C, t).fee; up += feeOne(r, Du, C, t).fee; }
        if (s === 'fee' && e === 36) ev.push({ t: 'cut20', id: id });
        if (s === 'fee' && e === 60) ev.push({ t: 'cut30', id: id });
        if (FQ != null && FQ > 12 && e % FQ === 0) ev.push({ t: 'reset', id: id });
        var onFee = s === 'fee' || s === 'noavg' || s === 'orig' || s === 'tiny';
        if (j && onFee && prev[id] && prev[id].on && prev[id].col && prev[id].col !== f.colA) ev.push({ t: 'col', id: id, lab: f.labA });
        prev[id] = { on: true, col: onFee ? f.colA : null };
      });
      o.months.push(t); o.base.push(b); o.down.push(j ? dn : b); o.up.push(j ? up : b); o.ev.push(ev); o.by.push(by);
    }
    var c = 1; for (var i = 2; i <= months; i++) if (o.base[i] < o.base[c] - 1e-9) c = i;
    if (!(o.base[c] < o.base[0] - 0.5)) c = 0;
    o.cheap = c; o.save = c ? o.base[0] - o.base[c] : 0;
    return o;
  }

  /* the bank's number against ours: close when within 2% or 50 ILS */
  function compare(ours, bank) { var d = bank - ours; return { d: d, pct: ours >= 0.5 ? d / ours : null, close: Math.abs(d) <= Math.max(50, 0.02 * ours) }; }

  var NLHV = { TRACKS: TRACKS, FREQ: FREQ, MAXROWS: MAXROWS, EXAMPLE: EXAMPLE, isVar: isVar, freqOf: freqOf, monthsOf: monthsOf, loanOf: loanOf,
    feeFreq: feeFreq, feeOne: feeOne, status: status, freeByRule: freeByRule, mortgage: mortgage, cpiKey: cpiKey, detail: detail,
    shiftD: shiftD, cut: cut, allocate: allocate, strip: strip, compare: compare };
  G.NLHV = NLHV;
  if (typeof document === 'undefined' || !G.NadLanInstruments) return;  // node: the math only

  /* ===================================================================================================== the page */
  G.NadLanInstruments.register('mhivun', {
    custom: function (root, data) {
      var tries = 0;
      (function wait() {
        if (G.NLMG && G.NLMR && G.NLMR.ui) return G.NLMR.ui.start(root, data, build);
        if (++tries > 120) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
        setTimeout(wait, 50);
      })();
    }
  });

  function css() {
    if (document.getElementById('mhv-css')) return;
    var s = document.createElement('style'); s.id = 'mhv-css';
    s.textContent = [
      '.mhv .mhv__rows{display:grid;gap:10px}',
      '.mhv .mhv__row{gap:10px}',
      '.mhv .mrx__rh>.nli__f{flex:1;min-width:0}',
      '.mhv__rg{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px 10px}',
      '.mhv__rg>.is-wide{grid-column:1/-1}',
      'html body .nli .mhv .mhv__row label{font:500 12px/16px var(--nli-sans) !important;color:var(--nli-ink2) !important}',
      'html body .nli .mhv .mhv__row .nli__in input,html body .nli .mhv .mhv__row .nli__in select{font-size:16px;padding:9px 8px;min-height:44px}',
      'html body .nli .mhv .mhv__row .nli__unit{padding:0 8px}',
      /* the live theme restyles plain inputs, selects and buttons: keep the instruments faces and flat boxes inside the tool */
      'html body .nli .mhv .nli__in input{font-family:var(--nli-mono) !important;border-radius:0 !important}',
      'html body .nli .mhv .nli__in select{font-family:var(--nli-sans) !important;border-radius:0 !important;box-shadow:none !important;-webkit-appearance:auto;appearance:auto}',
      'html body .nli .mhv .nli__seg button,html body .nli .mhv button.nli__add,html body .nli .mhv button.mrx__x,html body .nli .mhv .nli__share button,html body .nli .mhv .nli__share a{font-family:var(--nli-sans) !important;letter-spacing:0 !important;text-transform:none !important}',
      'html body .nli .mhv .mhv__term select{flex:none;width:auto;max-width:104px;border:0 !important;border-inline-start:1px solid var(--nli-line) !important;background:var(--nli-ground) !important;font:400 14px/20px var(--nli-sans) !important;padding:0 6px !important;color:var(--nli-ink2)}',
      'html body .nli .mhv button.nli__add[disabled]{opacity:.45;cursor:default}',
      '.mhv .mhv__cards{display:grid;gap:10px}',
      '.mhv .mhv__card{border:1px solid var(--nli-line);border-inline-start:4px solid var(--c,#2F6F86);border-radius:var(--nli-r-s);padding:10px 12px 4px;background:var(--nli-surface);min-width:0}',
      'html body .nli .mhv h3.mhv__ch{font:600 16px/22px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 2px !important;letter-spacing:0;text-transform:none}',
      'html body .nli .mhv .mhv__ch small{display:block;font:400 13px/18px var(--nli-sans);color:var(--nli-mute)}',
      'html body .nli .mhv .mhv__card .nli__lines div{padding:6px 0}',
      'html body .nli .mhv .mhv__card .nli__lines div:last-child{border-bottom:0}',
      'html body .nli .mhv ol.mhv__steps{margin:2px 0 10px !important;padding:0 22px 0 0 !important;display:grid;gap:6px;list-style:decimal outside !important}',
      'html body .nli .mhv ol.mhv__steps li{font:400 14px/22px var(--nli-sans) !important;color:var(--nli-ink2) !important;margin:0 !important;padding:0 !important}',
      'html body .nli .mhv ol.mhv__steps li b{font-weight:600;color:var(--nli-ink)}',
      '.mhv bdi{font-family:var(--nli-mono);font-variant-numeric:tabular-nums}',
      'html body .nli .mhv .mhv__key{font:500 16px/26px var(--nli-sans);color:var(--nli-ink);margin:0 0 10px;padding:10px 12px;border-inline-start:3px solid var(--nli-open);background:var(--nli-ground)}',
      'html body .nli .mhv .mhv__key.is-flat{border-inline-start-color:var(--nli-sea)}',
      'html body .nli .mhv .mhv__ok{border-inline-start:3px solid var(--nli-open)}',
      'html body .nli .mhv .mhv__gap{border-inline-start:3px solid var(--nli-survey)}',
      'html body .nli .mhv ul.mhv__ev,html body .nli .mhv ol.mhv__why{margin:8px 0 0 !important;padding:0 !important;list-style:none !important;display:grid;gap:6px}',
      'html body .nli .mhv ol.mhv__why{padding:0 22px 0 0 !important;list-style:decimal outside !important}',
      'html body .nli .mhv ul.mhv__ev li,html body .nli .mhv ol.mhv__why li{font:400 14px/22px var(--nli-sans) !important;color:var(--nli-ink2) !important;margin:0 !important;padding:0 !important}',
      'html body .nli .mhv ul.mhv__ev li b{font:500 14px/22px var(--nli-mono);color:var(--nli-ink);margin-inline-end:6px}',
      '.mhv .mhv__lg{display:flex;flex-wrap:wrap;gap:6px 14px;list-style:none;margin:8px 0 0;padding:0;font:400 12px/16px var(--nli-sans);color:var(--nli-ink2)}',
      '.mhv .mhv__lg li{display:flex;gap:6px;align-items:center;margin:0}',
      '.mhv .mhv__lg i{display:inline-block;width:12px;height:10px;flex:none}',
      '.mhv .mhv__lg i.ln{height:0;border-top:2px dashed #C42550}.mhv .mhv__lg i.dt{height:0;border-top:2px dotted #12202A}',
      '.mhv .mhv__lg i.dm{width:9px;height:9px;background:#1F4B5C;transform:rotate(45deg)}.mhv .mhv__lg i.ci{width:10px;height:10px;border:2px solid #1F4B5C;border-radius:50%;background:#fff}',
      '.mhv .mhv__what p{font:400 15px/25px var(--nli-sans);color:var(--nli-ink2);margin:0 0 10px;max-width:76ch}',
      '.mhv .mhv__what p b{color:var(--nli-ink);font-weight:600}',
      '.mhv .mrx__chart svg text.v{fill:#12202A;font-weight:500}',
      '.mhv [data-sec="when"] .nli__alab{margin-top:16px}.mhv [data-sec="when"] .mrx__hint{margin-top:12px}.mhv [data-sec="when"] details{margin-top:8px}',
      '@media (max-width:420px){.mhv__rg{gap:8px}html body .nli .mhv .mhv__term select{max-width:88px}}',
      '@media print{.mhv .mhv__row,.mhv button.nli__add{display:none !important}.mhv details{display:block}}'
    ].join('\n');
    document.head.appendChild(s);
  }

  function build(root, X) {
    var Q = G.NLMR, U = Q.ui, F = U.F, esc = U.esc, el = U.el, D = X.D, C = X.cpi;
    if (!D.prepay || !D.prepay.nl || !D.prepay.cpi || !D.fees) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
    css();
    var NOW = Q.nowKey(), TN = D.prepay.nl.rows[D.prepay.nl.rows.length - 1], TC = D.prepay.cpi.rows[D.prepay.cpi.rows.length - 1];
    function pc3(v) { return (Math.round(v * 1000) / 1000).toFixed(3).replace(/0+$/, '').replace(/\.$/, '') + '%'; }
    function b(v) { return '<bdi>' + esc(F.ils(v)) + '</bdi>'; }
    function bp(v) { return '<bdi>' + esc(pc3(v)) + '</bdi>'; }
    function bm(k) { return '<bdi>' + esc(F.month(k)) + '</bdi>'; }
    function bn(v) { return '<bdi>' + esc(F.num(v)) + '</bdi>'; }
    function fname(fq) { var x = FREQ.filter(function (f) { return f[0] === fq; })[0]; return x ? x[1] : ''; }
    function tname(l) { return Q.NAME[l.row.k] + (freqOf(l.row) != null ? ', ' + fname(freqOf(l.row)) : ''); }
    function sname(id) { var r = last && last.calc.filter(function (x) { return x.id === id; })[0]; return 'מסלול ' + (id + 1) + (r ? ', ' + Q.SHORT[r.k] : ''); }

    var st = { ex: true, rows: EXAMPLE.rows.map(function (r) { return Object.assign({ date: EXAMPLE.date }, r); }), pp: EXAMPLE.pp, mode: 'reduce', notice: 'short', bank: null };
    var hs = U.fromHash('mhivun');
    if (hs) {
      if (Array.isArray(hs.r) && hs.r.length) st.rows = hs.r.slice(0, MAXROWS).map(function (x) {
        return { k: Q.KIND[x[0]] ? x[0] : 'fixed_nl', amount: x[1] == null ? NaN : +x[1], date: Q.parseMonth(x[2]) || null, term: x[3] == null ? NaN : +x[3], unit: x[4] === 'm' ? 'm' : 'y', rate: x[5] == null ? NaN : +x[5], freq: [12, 24, 30, 60, 120].indexOf(+x[6]) > -1 ? +x[6] : 60 };
      });
      if (hs.pp != null && isFinite(hs.pp)) st.pp = +hs.pp; if (hs.md === 'shorten') st.mode = 'shorten'; if (hs.nt === 'long') st.notice = 'long'; if (+hs.bk > 0) st.bank = +hs.bk;
      st.ex = false;
    }

    var exTotal = EXAMPLE.rows.reduce(function (a, r) { return a + r.amount; }, 0);
    var P = U.panel(root, {
      kicker: 'פירעון מוקדם · צו הבנקאות',
      title: 'עמלת היוון',
      lede: 'מה זה היוון משכנתא? כשפורעים לפני הזמן מסלול בריבית קבועה, או מסלול משתנה לפני יום שינוי הריבית, הבנק מהוון את התשלומים שנותרו בריבית הממוצעת של בנק ישראל. אם הממוצע נמוך מהריבית שלכם, ההפרש הוא עמלת ההיוון. כאן מחשבים אותה לכל המשכנתא, עד 6 מסלולים: היתרה והעמלה בכל מסלול עם החישוב המלא, פירעון חלקי בחלוקה הזולה, החודש הזול ב־24 החודשים הקרובים, ובדיקה של המספר שקיבלתם מהבנק.',
      strip: [['קבועה לא צמודה, מעל 20 ועד 25 שנים', pc3(Q.avgOf(D, 'nl', TN, '20_25'))], ['קבועה לא צמודה, מעל 10 ועד 15 שנים', pc3(Q.avgOf(D, 'nl', TN, '10_15'))],
        ['צמודה למדד, מעל 10 ועד 15 שנים', pc3(Q.avgOf(D, 'cpi', TC, '10_15'))], ['הממוצעים בתוקף מתאריך', F.date(TN[0])]],
      eg: 'הערכים בפתיחה הם דוגמה: משכנתא של ' + F.ils(exTotal) + ' מ־' + F.month(EXAMPLE.date) + ' בארבעה מסלולים, ופירעון חלקי של ' + F.ils(EXAMPLE.pp) + '. הקלידו את המסלולים שלכם מהדוח השנתי של הבנק, והתוצאה מתעדכנת מיד. מה שמקלידים נשאר בדפדפן. חישוב לפי צו הבנקאות והממוצעים של בנק ישראל, לא ייעוץ.'
    });
    P.panel.classList.add('mhv');
    root.setAttribute('data-mhv', '1');

    var t = 0, refs = [], last = null;
    function edited() { if (!st.ex) return; st.ex = false; [].forEach.call(P.panel.querySelectorAll('.mrx__eg'), function (x) { x.parentNode.removeChild(x); }); }
    function schedule() { clearTimeout(t); t = setTimeout(run, 90); }
    function tag(w, k, v) { var x = w.querySelector('input,select'); if (x) { x.setAttribute('data-f', k); if (v != null) x.setAttribute('data-i', String(v)); } return w; }
    function segTag(w, k) { [].forEach.call(w._g.children, function (bt, i) { bt.setAttribute('data-s', k); bt.setAttribute('data-v', w._opts[i]); }); return w; }
    function seg(label, opts, cur, on, k) { var w = U.seg(label, opts, cur, on); w._opts = opts.map(function (o) { return o[0]; }); return segTag(w, k); }

    /* ------------------------------------------------------------------------------------------------- the form */
    function termField(r, i) {
      var w = el('div', 'nli__f'), id = 'mhv-t-' + Math.random().toString(36).slice(2, 8);
      var lab = el('label', '', 'התקופה המקורית'); lab.htmlFor = id; w.appendChild(lab);
      var box = el('div', 'nli__in mhv__term'), inp = el('input'); inp.id = id; inp.type = 'text'; inp.inputMode = 'decimal'; inp.autocomplete = 'off';
      inp.value = isFinite(r.term) ? String(r.term) : ''; inp.setAttribute('data-f', 'term'); inp.setAttribute('data-i', String(i));
      inp.addEventListener('input', function () { r.term = U.num(inp.value); edited(); schedule(); });
      var s = el('select'); s.setAttribute('aria-label', 'יחידת התקופה, מסלול ' + (i + 1)); s.setAttribute('data-f', 'unit'); s.setAttribute('data-i', String(i));
      [['y', 'שנים'], ['m', 'חודשים']].forEach(function (o) { var op = el('option', '', o[1]); op.value = o[0]; if (o[0] === r.unit) op.selected = true; s.appendChild(op); });
      s.addEventListener('change', function () {
        var n = monthsOf(r); r.unit = s.value;
        if (isFinite(n)) { r.term = r.unit === 'y' ? Math.round(n / 12 * 100) / 100 : n; inp.value = String(r.term); }
        edited(); schedule();
      });
      box.appendChild(inp); box.appendChild(s); w.appendChild(box);
      var err = el('span', 'nli__err'); err.setAttribute('aria-live', 'polite'); w.appendChild(err); w._inp = inp; w._err = err;
      return w;
    }
    function rowEl(r, i) {
      var w = el('div', 'mrx__row mhv__row'); w.style.setProperty('--c', Q.COL[r.k]); w.setAttribute('data-row', String(i));
      var rh = el('div', 'mrx__rh');
      var ts = tag(U.select('מסלול ' + (i + 1), TRACKS.map(function (k) { return [k, Q.NAME[k]]; }), r.k, function (k) { r.k = k; if (isVar(k) && !r.freq) r.freq = 60; edited(); buildForm(); run(); }), 'k', i);
      rh.appendChild(ts);
      if (st.rows.length > 1) {
        var x = el('button', 'mrx__x', '×'); x.type = 'button'; x.setAttribute('aria-label', 'הסרת מסלול ' + (i + 1)); x.setAttribute('data-act', 'del'); x.setAttribute('data-i', String(i));
        x.addEventListener('click', function () { st.rows.splice(i, 1); edited(); buildForm(); run(); });
        rh.appendChild(x);
      }
      w.appendChild(rh);
      var g = el('div', 'mhv__rg'), f = {};
      f.amount = tag(U.field('הסכום שלקחתם', r.amount, '₪', function (n) { r.amount = n; edited(); schedule(); }, { money: true }), 'amount', i);
      f.date = tag(U.field('חודש ההתחלה', r.date ? F.month(r.date) : '', null, function (s) { r.date = Q.parseMonth(s); edited(); schedule(); }, { type: 'text', ph: '7.2023' }), 'date', i);
      f.term = termField(r, i);
      f.rate = tag(U.field('הריבית היום', r.rate, '%', function (n) { r.rate = n; edited(); schedule(); }, { dec: 2 }), 'rate', i);
      [f.amount, f.date, f.term, f.rate].forEach(function (x) { g.appendChild(x); });
      if (isVar(r.k)) {
        var fq = tag(U.select('כל כמה זמן הריבית משתנה', FREQ.map(function (x) { return [String(x[0]), fname(x[0])]; }), String(r.freq || 60), function (v) { r.freq = +v; edited(); schedule(); }), 'freq', i);
        fq.classList.add('is-wide'); g.appendChild(fq);
      }
      w.appendChild(g); refs[i] = f;
      return w;
    }
    function buildForm() {
      P.form.innerHTML = ''; refs = [];
      var hd = el('div', 'nli__f'); hd.appendChild(el('span', 'nli__lab', 'המסלולים במשכנתא שלכם'));
      hd.appendChild(el('span', 'nli__help', 'כל מסלול כמו בדוח השנתי של הבנק: הסכום שלקחתם, חודש ההתחלה, התקופה והריבית שחלה היום. במסלול משתנה: כל כמה זמן הריבית משתנה.'));
      P.form.appendChild(hd);
      var box = el('div', 'mhv__rows'); P.form.appendChild(box);
      st.rows.forEach(function (r, i) { box.appendChild(rowEl(r, i)); });
      var add = el('button', 'nli__add', '+ הוספת מסלול'); add.type = 'button'; add.setAttribute('data-act', 'add'); add.disabled = st.rows.length >= MAXROWS;
      add.addEventListener('click', function () {
        if (st.rows.length >= MAXROWS) return;
        var p = st.rows[st.rows.length - 1] || { date: EXAMPLE.date, term: 25, unit: 'y' };
        st.rows.push({ k: 'fixed_nl', amount: NaN, date: p.date, term: p.term, unit: p.unit, rate: NaN, freq: 60 });
        edited(); buildForm(); run();
        var a = P.form.querySelector('[data-row="' + (st.rows.length - 1) + '"] input[data-f="amount"]'); if (a) a.focus();
      });
      P.form.appendChild(add);
      if (st.rows.length >= MAXROWS) P.form.appendChild(el('p', 'nli__help', 'אפשר עד 6 מסלולים, כמו ברוב המשכנתאות.'));
      P.form.appendChild(seg('מתי מודיעים לבנק על הפירעון', [['short', 'פחות מ־10 ימים מראש'], ['long', '10 ימים מראש ומעלה']], st.notice, function (k) { st.notice = k; edited(); schedule(); }, 'notice'));
    }
    function validRow(r, i) {
      var f = refs[i], ok = true;
      if (f) Object.keys(f).forEach(function (k) { f[k]._err.textContent = ''; });
      function bad(k, msg) { ok = false; if (f && f[k]) f[k]._err.textContent = msg; }
      if (!(r.amount >= 1000 && r.amount <= 50000000)) bad('amount', 'הקלידו את הסכום שלקחתם במסלול.');
      var n = monthsOf(r);
      if (!r.date) bad('date', 'חודש ושנה, למשל 7.2023.');
      else if (Q.mDiff(r.date, NOW) < 1) bad('date', 'החודש צריך להיות לפני ' + F.month(NOW) + '.');
      if (!(n >= 12 && n <= 480)) bad('term', r.unit === 'm' ? 'בין 12 ל־480 חודשים.' : 'בין שנה ל־40 שנה.');
      if (!(r.rate >= 0 && r.rate <= 20)) bad('rate', 'ריבית בין 0% ל־20%.');
      if (ok && Q.mDiff(r.date, NOW) >= n) bad('date', 'לפי החודש והתקופה המסלול כבר נפרע.');
      return ok;
    }

    /* ------------------------------------------------------------------------------------------- the sections */
    var SP = U.sec(P.secs, 'פירעון חלקי: איך לחלק את הסכום', 'מקלידים כמה רוצים לפרוע, ואנחנו מחלקים את הסכום בין המסלולים כך שעמלת ההיוון תהיה הנמוכה ביותר.');
    var gp = el('div', 'nli__grid mrx__rfg'), fp = el('form', 'nli__form'), op = el('div', 'nli__out'); fp.addEventListener('submit', function (e) { e.preventDefault(); }); op.setAttribute('aria-live', 'polite');
    var fpp = tag(U.field('כמה רוצים לפרוע', st.pp, '₪', function (n) { st.pp = n; edited(); clearTimeout(t); t = setTimeout(function () { paintPart(); paintShare(); }, 90); }, { money: true, help: 'הסכום שתשלמו לבנק עכשיו, בלי העמלות.' }), 'pp');
    var bx = el('div', 'mrx__box'); bx.appendChild(fpp);
    bx.appendChild(seg('מה עושים עם הפירעון', [['reduce', 'הקטנת ההחזר החודשי'], ['shorten', 'קיצור התקופה']], st.mode, function (k) { st.mode = k; edited(); paintPart(); paintShare(); }, 'mode'));
    fp.appendChild(bx); gp.appendChild(fp); gp.appendChild(op); SP.appendChild(gp);

    var SW = U.sec(P.secs, 'מתי הכי זול לפרוע: 24 החודשים הקרובים', 'העמלה אם פורעים את כל המשכנתא בכל אחד מ־24 החודשים הקרובים, אם הממוצעים של בנק ישראל לא ישתנו, ובשני תרחישים: ממוצעים נמוכים ב־0.5 נקודת אחוז (העמלה עולה) וגבוהים ב־0.5 (העמלה יורדת).');
    var ow = el('div', ''); SW.appendChild(ow);

    var SB = U.sec(P.secs, 'בדיקת המספר של הבנק', 'קיבלתם מהבנק דוח לסילוק או מכתב עם עמלת ההיוון? הקלידו את הסכום, ונשווה אותו לחישוב.');
    var gb = el('div', 'nli__grid mrx__rfg'), fb = el('form', 'nli__form'), ob = el('div', 'nli__out'); fb.addEventListener('submit', function (e) { e.preventDefault(); }); ob.setAttribute('aria-live', 'polite');
    var fbk = tag(U.field('העמלה שהבנק נתן לכם', st.bank, '₪', function (n) { st.bank = n > 0 ? n : null; edited(); clearTimeout(t); t = setTimeout(function () { paintBank(); paintShare(); }, 90); }, { money: true, help: 'השורה "עמלת היוון" או "הפרשי היוון" בדוח לסילוק. לא חובה, ונשאר בדפדפן.' }), 'bank');
    var bb = el('div', 'mrx__box'); bb.appendChild(fbk); fb.appendChild(bb); gb.appendChild(fb); gb.appendChild(ob); SB.appendChild(gb);

    var SX = U.sec(P.secs, 'מה זה היוון משכנתא', null); SX.classList.add('mhv__what');
    SP.setAttribute('data-sec', 'part'); SW.setAttribute('data-sec', 'when'); SB.setAttribute('data-sec', 'bank'); SX.setAttribute('data-sec', 'what');
    SX.insertAdjacentHTML('beforeend',
      '<p><b>היוון</b> הוא הבאה של תשלומים עתידיים לערך של היום. כשפורעים לפני הזמן מסלול בריבית קבועה, הבנק מהוון את התשלומים שנותרו בריבית הממוצעת שבנק ישראל מפרסם לתקופה שנותרה. אם הממוצע נמוך מהריבית שלכם, הערך של התשלומים גבוה מהיתרה, וההפרש הוא עמלת ההיוון, שנקראת גם <b>הפרשי היוון</b>.</p>' +
      '<p>הבנק עושה שני חישובים וגובה את הנמוך: הממוצע של היום מול הריבית שלכם, והממוצע של היום מול הממוצע ביום שלקחתם את ההלוואה. אחרי 3 שנים מיום ההלוואה העמלה יורדת ב־20%, ואחרי 5 שנים ב־30%. בפירעון חלקי העמלה יחסית לסכום שנפרע.</p>' +
      '<p>אין עמלת היוון במסלול פריים, במסלול שהריבית בו משתנה כל שנה או לעיתים קרובות יותר, וביום שינוי הריבית במסלול משתנה. בכל פירעון יש עמלה תפעולית של עד ' + esc(F.ils(D.fees.operational_max)) + ', ו־0.1% מהסכום אם מודיעים לבנק פחות מ־10 ימים מראש. במסלול צמוד שנפרע בין ה־1 ל־15 בחודש מתווספת מחצית השינוי הממוצע במדד.</p>' +
      '<p><b>עמלת היוון ובנק ישראל:</b> הממוצעים לחישוב מתפרסמים פעם בחודש באתר בנק ישראל ונכנסים לתוקף בערך ב־19 לחודש. הממוצעים בחישוב כאן בתוקף מ־' + esc(F.date(TN[0])) + ', לפי נתוני ' + esc(F.month(String(TN[1]).slice(0, 7))) + '.</p>');

    /* ------------------------------------------------------------------------------------------------------ run */
    function note(box, msg) { box.innerHTML = ''; box.appendChild(el('p', 'nli__note', esc(msg))); }
    function run() {
      var calc = [], bad = [];
      st.rows.forEach(function (r, i) { if (validRow(r, i)) calc.push({ id: i, k: r.k, amount: +r.amount, date: r.date, n: monthsOf(r), rate: +r.rate, freq: isVar(r.k) ? (+r.freq || 60) : null }); else bad.push(i + 1); });
      if (!calc.length) { last = null; note(P.out, 'השלימו לפחות מסלול אחד: סכום, חודש התחלה, תקופה וריבית.'); op.innerHTML = ''; ow.innerHTML = ''; ob.innerHTML = ''; paintShare(); return; }
      last = { calc: calc, bad: bad, MG: G.NLHV.mortgage(calc, D, C, NOW) };
      paintOut(); paintPart(); paintWhen(); paintBank(); paintShare();
    }

    /* ---------------------------------------------------------------------------------------------- the answer */
    function noFee(l) {
      return { prime: 'ללא: פריים, הריבית משתנה במועד לא ידוע', yearly: 'ללא: הריבית משתנה כל שנה', reset: 'ללא: החודש הוא יום שינוי הריבית',
        noavg: 'ללא: הממוצע של היום לא נמוך מהריבית שלכם', orig: 'ללא: הממוצע היום גבוה מהממוצע ביום ההלוואה', tiny: 'פחות משקל אחד' }[l.status] || '';
    }
    function shortNo(l) { return { prime: 'ללא: פריים', yearly: 'ללא: משתנה כל שנה', reset: 'ללא: יום שינוי', noavg: 'ללא: הממוצע לא נמוך', orig: 'ללא', tiny: 'פחות משקל' }[l.status] || 'ללא'; }
    function noticeUsed(MG) { return st.notice === 'short' ? MG.notice : 0; }
    function paintOut() {
      var MG = last.MG, o = P.out, nt = noticeUsed(MG); o.innerHTML = '';
      var act = MG.loans.filter(function (l) { return l.active; }), free = act.filter(function (l) { return l.fx.fee < 0.5; });
      var sub;
      if (MG.fee >= 0.5) {
        sub = 'על יתרה של ' + b(MG.bal) + ' ב־' + bn(MG.n) + ' מסלולים, בפירעון ב־' + bm(NOW) + '.' + (free.length ? ' בלי עמלת היוון: ' + esc(free.map(function (l) { return 'מסלול ' + (l.id + 1) + ' (' + noFee(l).replace(/^ללא: /, '') + ')'; }).join(', ')) + '.' : '') +
          ' ועוד עמלה תפעולית של עד ' + b(MG.op) + (nt > 0.5 ? ' ו־' + b(nt) + ' על הודעה של פחות מ־10 ימים' : '') + '.';
      } else {
        sub = 'באף מסלול אין היום עמלת היוון: ' + esc(act.map(function (l) { return 'מסלול ' + (l.id + 1) + ', ' + noFee(l).replace(/^ללא: /, ''); }).join('; ')) + '. נשארות עמלה תפעולית של עד ' + b(MG.op) + (nt > 0.5 ? ' ו־' + b(nt) + ' על הודעה של פחות מ־10 ימים' : '') + '.';
      }
      var A = U.answer('עמלת היוון לכל המשכנתא, בפירעון ב־' + F.month(NOW), MG.fee >= 0.5 ? F.ils(MG.fee) : 'אין עמלת היוון', sub, st.ex);
      if (MG.fee < 0.5) A.querySelector('.nli__fig').classList.add('is-he');
      o.appendChild(A);
      var li = [['היתרה לסילוק, ' + MG.n + (MG.n === 1 ? ' מסלול' : ' מסלולים'), F.ils(MG.bal)], ['עמלת היוון', MG.fee >= 0.5 ? F.ils(MG.fee) : 'אין'], ['עמלה תפעולית, פעם אחת', 'עד ' + F.ils(MG.op)],
        ['הודעה של פחות מ־10 ימים, 0.1% מהיתרה', st.notice === 'short' ? F.ils(MG.notice) : 'ללא: 10 ימים מראש ומעלה']];
      if (MG.linked && MG.cpiFee > 0.5) li.push(['לא בסך: בפירעון בין ה־1 ל־15 בחודש, במסלולים הצמודים', F.ils(MG.cpiFee)]);
      li.push(['סך העמלות', F.ils(MG.fee + MG.op + nt)], ['סך הכול לסילוק, יתרה ועמלות', F.ils(MG.bal + MG.fee + MG.op + nt)]);
      o.appendChild(U.lines(li));
      if (last.bad.length) o.appendChild(el('p', 'nli__note', esc((last.bad.length === 1 ? 'מסלול ' + last.bad[0] + ' לא נכלל' : 'המסלולים ' + last.bad.join(', ') + ' לא נכללו') + ' עד שכל השדות שלו מלאים ותקינים.')));
      o.appendChild(el('span', 'nli__alab', 'כל מסלול לחוד'));
      var cards = el('div', 'mhv__cards'); o.appendChild(cards);
      act.forEach(function (l) { cards.appendChild(card(l)); });
      o.appendChild(srcLine());
    }
    function card(l) {
      var fx = l.fx, r = l.row, w = el('article', 'mhv__card'); w.style.setProperty('--c', Q.COL[r.k]); w.setAttribute('data-card', String(l.id));
      w.appendChild(el('h3', 'mhv__ch', esc((l.id + 1) + '. ' + tname(l)) + '<small>' + b(r.amount) + ' מ־' + bm(r.date) + ', ' + bn(r.n) + ' חודשים, ריבית ' + bp(r.rate) + '</small>'));
      var li = [['יתרה היום' + (fx.linked ? ', כולל הצמדה' : ''), F.ils(fx.bal)], ['תשלומים ששולמו', F.num(fx.el) + ' מתוך ' + F.num(fx.N)],
        ['עמלת היוון', fx.fee >= 0.5 ? F.ils(fx.fee) : noFee(l)]];
      if (!freeByRule(l.status)) {
        li.push(['הפחתה לוותק', fx.cut ? F.num(100 * fx.cut) + '%, מ־' + F.month(Q.mAdd(r.date, fx.cut >= 0.3 ? 60 : 36)) : 'אין: פחות מ־3 שנים, 20% מ־' + F.month(Q.mAdd(r.date, 36))]);
        li.push(['הממוצע של בנק ישראל, ' + fx.labA + (fx.kind === 'var5' ? ' עד שינוי הריבית' : ' שנותרו'), pc3(fx.Ae) + ' · בתוקף מ־' + F.date(fx.todayFrom)]);
      }
      if (st.notice === 'short') li.push(['הודעה של פחות מ־10 ימים', F.ils(fx.notice)]);
      w.appendChild(U.lines(li));
      var d = el('details', 'mrx__more mhv__how'); d.appendChild(el('summary', '', 'איך זה חושב')); d.setAttribute('data-how', String(l.id));
      d.appendChild(el('ol', 'mhv__steps', steps(l).map(function (s) { return '<li>' + s + '</li>'; }).join('')));
      w.appendChild(d);
      return w;
    }
    /* the step-by-step of one track, one line per step, every number from NLMR.feeExisting and NLHV.detail */
    function steps(l) {
      var fx = l.fx, r = l.row, out = [], d = G.NLHV.detail(l);
      out.push('ההלוואה: ' + b(r.amount) + ' מ־' + bm(r.date) + ' ל־' + bn(r.n) + ' חודשים, ריבית ' + bp(r.rate) + ' היום, לוח שפיצר.');
      out.push('שולמו ' + bn(fx.el) + ' תשלומים ונותרו ' + bn(fx.left) + ', נכון ל־' + bm(NOW) + '.');
      if (fx.linked) {
        var k0 = G.NLHV.cpiKey(C, r.date), k1 = G.NLHV.cpiKey(C, NOW);
        out.push('היתרה לפי הלוח ' + b(fx.real) + (k0 && k1 && fx.ratio !== 1 ? ', כפול ההצמדה: מדד ' + bm(k1) + ' חלקי מדד ' + bm(k0) + ' = <bdi>' + esc(fx.ratio.toFixed(4)) + '</bdi>. היתרה היום: ' + b(fx.bal) + '.' : '. המדד לא נטען, ולכן בלי הצמדה.'));
      } else out.push('היתרה היום: ' + b(fx.bal) + '.');
      if (l.status === 'prime') { out.push('במסלול פריים הריבית משתנה במועד לא ידוע, ולכן אין עמלת היוון (צו הבנקאות, סעיף 4).'); return tail(l, out); }
      if (l.status === 'yearly') { out.push('הריבית במסלול משתנה ' + esc(fname(freqOf(r))) + ', ולכן אין עמלת היוון (צו הבנקאות, סעיף 4).'); return tail(l, out); }
      if (l.status === 'reset') { out.push('החודש הוא יום שינוי הריבית במסלול (' + esc(fname(freqOf(r))) + ' מ־' + bm(r.date) + '), ובו אין עמלת היוון (צו הבנקאות, סעיף 4).'); return tail(l, out); }
      out.push('התשלומים שנכנסים לחישוב: ' + bn(d.n) + (d.change ? ' תשלומים עד יום שינוי הריבית הבא, ' + bm(d.change) + ', ' + b(d.first) + ' בחודש; האחרון כולל את היתרה באותו יום, ' + b(d.last) + '.' : ' תשלומים עד סוף ההלוואה, ' + b(d.first) + ' בחודש.'));
      out.push('הממוצע של בנק ישראל היום, בטור "' + esc(fx.labA) + '" (' + (d.change ? 'עד שינוי הריבית' : 'התקופה שנותרה') + '): ' + bp(fx.Ae) + ' שנתית אפקטיבית, שהם ' + bp(fx.A) + ' לתשלום חודשי. בתוקף מ־<bdi>' + esc(F.date(fx.todayFrom)) + '</bdi>.');
      out.push(fx.origFrom ? 'הממוצע ביום ההלוואה, בטור "' + esc(fx.labC) + '" (' + (fx.kind === 'var5' ? 'התקופה עד שינוי הריבית' : 'תקופת ההלוואה') + '): ' + bp(fx.Ce) + ', שהם ' + bp(fx.C) + ' לתשלום חודשי. בתוקף מ־<bdi>' + esc(F.date(fx.origFrom)) + '</bdi>.'
        : 'הממוצע ביום ההלוואה לא נמצא בקובץ שלנו, שמתחיל ב־' + bm(String(D.prepay[fx.file].rows[0][0]).slice(0, 7)) + ', ולכן נבדק רק החישוב הראשון.');
      out.push('הערך של התשלומים בריבית שלכם, ' + bp(r.rate) + ': ' + b(d.pvR) + ', כלומר היתרה.');
      out.push('הערך שלהם בממוצע של היום, ' + bp(fx.A) + ': ' + b(d.pvA) + '.');
      if (d.pvC != null) out.push('הערך שלהם בממוצע של יום ההלוואה, ' + bp(fx.C) + ': ' + b(d.pvC) + '.');
      out.push('<b>חישוב ראשון</b> (סעיף 3(3)): ' + (fx.A < r.rate ? b(d.pvA) + ' פחות היתרה ' + b(fx.bal) + ' = ' + b(fx.f3) + '.' : 'לא חל: הממוצע של היום לא נמוך מהריבית שלכם.'));
      out.push('<b>חישוב שני</b> (סעיף 3(4)): ' + (fx.f4 != null ? b(d.pvA) + ' פחות ' + b(d.pvC) + (fx.f4 > 0.5 ? ' = ' + b(fx.f4) + '.' : ': הממוצע היום גבוה מהממוצע ביום ההלוואה, ולכן אפס.') : fx.origFrom ? 'לא חל: הממוצע ביום ההלוואה לא היה נמוך מהריבית שלכם.' : 'לא ניתן לבדוק.'));
      if (fx.A < r.rate || fx.f4 != null) out.push('הבנק גובה את הנמוך מבין השניים: ' + (d.lower >= 0.5 ? b(d.lower) : 'אפס') + (fx.f4 != null ? ' (החישוב ' + (d.which === 4 ? 'השני' : 'הראשון') + ').' : ', כי חל רק החישוב הראשון.'));
      out.push(fx.cut ? 'הפחתה לוותק: ' + bn(100 * fx.cut) + '%, כי עברו ' + (fx.cut >= 0.3 ? '5' : '3') + ' שנים מ־' + bm(r.date) + '.' + (fx.cut < 0.3 ? ' מ־' + bm(d.cut30) + ' ההפחתה 30%.' : '')
        : 'אין הפחתה לוותק: עוד לא עברו 3 שנים. מ־' + bm(d.cut20) + ' ההפחתה 20%, ומ־' + bm(d.cut30) + ' 30%.');
      out.push('<b>עמלת ההיוון</b>: ' + (fx.fee >= 0.5 ? (fx.cut ? b(d.lower) + ' × <bdi>' + esc(String(Math.round((1 - fx.cut) * 100) / 100)) + '</bdi> = ' : '') + b(fx.fee) + '.' : noFee(l) + '.'));
      return tail(l, out);
    }
    function tail(l, out) {
      var fx = l.fx;
      out.push('ועוד: ' + b(fx.notice) + ' (0.1% מהיתרה) אם מודיעים לבנק פחות מ־10 ימים מראש' + (fx.cpiFee > 0.5 ? ', ו־' + b(fx.cpiFee) + ' אם פורעים בין ה־1 ל־15 בחודש (מחצית השינוי הממוצע במדד)' : '') + '. העמלה התפעולית, עד ' + b(fx.op) + ', נספרת פעם אחת לכל המשכנתא.');
      return out;
    }
    function srcLine() {
      var hN = U.srcHe(D, D.prepay.nl.src, 'mashfix'), hC = U.srcHe(D, D.prepay.cpi.src, 'pribmash');
      var list = [{ label: 'צו הבנקאות (עמלת פירעון מוקדם), התשס"ב-2002', url: D.fees.src.url },
        { label: hN.label + ', נתוני ' + F.month(String(TN[1]).slice(0, 7)) + ', בתוקף מ־' + F.date(TN[0]), url: hN.url },
        { label: hC.label + ', נתוני ' + F.month(String(TC[1]).slice(0, 7)) + ', בתוקף מ־' + F.date(TC[0]), url: hC.url },
        { label: 'בנק ישראל, חוזר הפיקוח על הבנקים לחישוב העמלה', url: 'https://www.boi.org.il/roles/supervisionregulation/circulars/cir2103/' },
        { label: 'בנק ישראל, שיעורי ריבית', url: 'https://www.boi.org.il/information/interestrates/' }];
      if (last && last.MG.linked && C) list.push({ label: C.source + ', ' + F.month(C.latest), url: D.cpi.src.url });
      return el('p', 'mrx__src', esc('החישוב: לוח שפיצר בריבית שלכם מחודש ההתחלה (במסלול משתנה ובפריים: כאילו הריבית של היום חלה מההתחלה); במסלול צמוד, היתרה כפול המדד האחרון חלקי המדד של חודש ההתחלה. הממוצעים: ריבית שנתית אפקטיבית שהומרה לחודשית, (1 + ר)^(1/12) − 1; הממוצע ביום ההלוואה: הקובץ שהיה בתוקף ב־15 לחודש. מקורות: ') +
        list.map(function (s) { return '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.label) + '</a>'; }).join(' · ') + '.');
    }

    /* ------------------------------------------------------------------------------------------- partial payoff */
    function paintPart() {
      op.innerHTML = ''; if (!last) return;
      if (!(st.pp > 0)) { note(op, 'הקלידו את הסכום שרוצים לפרוע.'); return; }
      var MG = last.MG, A = G.NLHV.allocate(MG, st.pp, st.mode, D), nt = st.notice === 'short' ? A.notice : 0, red = st.mode !== 'shorten';
      var sub = (A.capped ? 'הסכום גבוה מהיתרה, ולכן חישבנו פירעון של כל היתרה, ' + b(A.amount) + '. ' : '') +
        (red ? 'ההחזר החודשי יורד ב־' + b(A.drop) + ', וחוסכים ' + b(A.saved) + ' ריבית עד סוף ההלוואות.' : 'ההחזר החודשי נשאר, התקופה מתקצרת, וחוסכים ' + b(A.saved) + ' ריבית עד סוף ההלוואות.');
      var ans = U.answer('עמלת היוון על פירעון של ' + F.ils(A.amount), A.fee >= 0.5 ? F.ils(A.fee) : 'אין עמלת היוון', sub, st.ex);
      if (A.fee < 0.5) ans.querySelector('.nli__fig').classList.add('is-he');
      op.appendChild(ans);
      op.appendChild(el('p', 'mrx__hint', 'הסדר: קודם מסלולים שאין בהם עמלת היוון (פריים, ריבית שמשתנה כל שנה, יום שינוי הריבית), אחר כך לפי העמלה על כל שקל, מהנמוכה לגבוהה, ובשוויון קודם הריבית הגבוהה.'));
      var z = function (v) { return v >= 0.5 ? F.ils(v) : 'אין'; };
      var rows = A.items.map(function (it) {
        return { cells: [esc(sname(it.id)) + (it.full ? '<small>כל היתרה</small>' : ''), esc(F.ils(it.a)), esc(it.fee >= 0.5 ? F.ils(it.fee) : it.l.status === 'fee' ? 'פחות משקל' : shortNo(it.l)),
          esc(red ? (it.full ? 'נסגר, ' + z(it.drop) : z(it.drop)) : (it.months ? F.num(it.months) + ' חודשים' : 'פחות מחודש')), esc(z(it.saved))] };
      });
      rows.push({ cls: 'is-on', cells: ['סך הכול', esc(F.ils(A.amount)), esc(z(A.fee)), esc(red ? z(A.drop) : ''), esc(z(A.saved))] });
      op.appendChild(U.table(['מסלול', 'כמה נפרע', 'עמלת היוון', red ? 'ההחזר יורד ב' : 'התקופה מתקצרת ב', 'ריבית שנחסכת עד הסוף'], rows, { num: [1, 2, 3, 4], cards: true }));
      var li = [['חלוקה לפי היתרות הייתה עולה', A.prop >= 0.5 ? F.ils(A.prop) + (A.prop - A.fee >= 0.5 ? ' במקום ' + (A.fee >= 0.5 ? F.ils(A.fee) : 'אפס') : '') : 'אין'],
        ['עמלה תפעולית', 'עד ' + F.ils(MG.op)], ['הודעה של פחות מ־10 ימים, 0.1% מהסכום', st.notice === 'short' ? F.ils(A.notice) : 'ללא: 10 ימים מראש ומעלה'],
        ['הריבית שנחסכת, פחות כל העמלות', F.sils(A.saved - A.fee - MG.op - nt)]];
      op.appendChild(U.lines(li));
      op.appendChild(el('p', 'mrx__hint', 'הריבית שנחסכת: התשלומים שלא תשלמו, פחות הסכום שפורעים, בשקלים של היום. במסלול צמוד בלי מדד עתידי, ובפריים ובמשתנה בריבית של היום. בפירעון חלקי עמלת ההיוון יחסית לחלק שנפרע מהמסלול.'));
    }

    /* ------------------------------------------------------------------------------------------- when to prepay */
    var lastW = null;
    function paintWhen() {
      ow.innerHTML = ''; lastW = null; if (!last) return;
      var W = G.NLHV.strip(last.calc, D, C, NOW, 24); lastW = W;
      var key = el('p', 'mhv__key' + (W.cheap ? '' : ' is-flat'));
      key.innerHTML = W.cheap ? 'החודש הזול ביותר ב־24 החודשים, אם הממוצעים לא ישתנו: ' + bm(W.months[W.cheap]) + ', עמלה של ' + (W.base[W.cheap] >= 0.5 ? b(W.base[W.cheap]) : 'אפס') + '. זה ' + b(W.save) + ' פחות מהיום, שבו העמלה ' + b(W.base[0]) + '.'
        : 'אם הממוצעים לא ישתנו, אין ב־24 החודשים הקרובים חודש שבו העמלה נמוכה מהיום' + (W.base[0] >= 0.5 ? ' (' + b(W.base[0]) + ')' : '') + '.';
      ow.appendChild(key);
      var fig = el('figure', 'mrx__chart'); ow.appendChild(fig);
      fig.innerHTML = chart(W, Math.round(Math.max(300, Math.min(1200, SW.clientWidth || 600))));
      fig.appendChild(el('ul', 'mhv__lg', '<li><i style="background:#2F6F86"></i>העמלה, אם הממוצעים לא ישתנו</li><li><i style="background:#12202A"></i>היום</li>' + (W.cheap ? '<li><i style="background:#4F9A5C"></i>החודש הזול</li>' : '') +
        '<li><i class="ln"></i>ממוצעים נמוכים ב־0.5</li><li><i class="dt"></i>ממוצעים גבוהים ב־0.5</li><li><i class="dm"></i>הפחתה לוותק</li><li><i class="ci"></i>יום שינוי ריבית</li>'));
      var evs = [];
      W.ev.forEach(function (list, j) { if (list.length) evs.push('<li><b>' + esc(F.month(W.months[j])) + '</b>' + esc(list.map(evText).join('; ')) + (j ? '. סך העמלה ' + (W.base[j] >= 0.5 ? b(W.base[j]) : 'אפס') + ', בחודש הקודם ' + (W.base[j - 1] >= 0.5 ? b(W.base[j - 1]) : 'אפס') : '') + '.</li>'); });
      if (evs.length) { ow.appendChild(el('span', 'nli__alab', 'החודשים שבהם משהו משתנה')); ow.appendChild(el('ul', 'mhv__ev', evs.join(''))); }
      ow.appendChild(el('p', 'mrx__hint', 'זו השוואה של העמלה בלבד: עד החודש שתבחרו ממשיכים לשלם את ההחזר והריבית. בכל חודש היתרה קטנה, ולכן גם העמלה; היא קופצת כשהתקופה שנותרה עוברת לטור של ממוצע נמוך יותר. אחרי יום שינוי הריבית במסלול משתנה הריבית החדשה עוד לא ידועה, וחישבנו לפי הריבית של היום.'));
      var d = el('details', 'mrx__more mrx__sec'); d.setAttribute('data-when-table', '1'); d.appendChild(el('summary', '', 'הטבלה של 24 החודשים')); ow.appendChild(d);
      var rows = W.months.map(function (k, j) {
        var z = function (v) { return v >= 0.5 ? F.ils(v) : 'אין עמלה'; };
        return { cls: j === 0 || j === W.cheap ? 'is-on' : '', cells: [esc(F.month(k) + (j === 0 ? ', היום' : j === W.cheap ? ', הזול' : '')), esc(z(W.base[j])), esc(j ? z(W.down[j]) : ''), esc(j ? z(W.up[j]) : ''), esc(W.ev[j].map(evText).join('; '))] };
      });
      d.appendChild(U.table(['חודש', 'אם הממוצעים לא ישתנו', 'ממוצעים נמוכים ב־0.5', 'ממוצעים גבוהים ב־0.5', 'מה קורה בחודש'], rows, { num: [1, 2, 3], cards: true }));
    }
    function evText(e) {
      var n = sname(e.id);
      return { cut20: n + ': 3 שנים מההתחלה, הפחתה של 20%', cut30: n + ': 5 שנים מההתחלה, הפחתה של 30%', reset: n + ': יום שינוי הריבית, אין בו עמלת היוון',
        col: n + ': התקופה שנותרה עוברת לטור "' + (e.lab || '') + '"', end: n + ': ההלוואה מסתיימת' }[e.t] || '';
    }
    function chart(W, Wd) {
      var n = W.months.length, H = Math.round(Math.max(220, Math.min(280, Wd * 0.42))), pl = 60, pr = 10, pt = 24, pb = 50, w = Wd - pl - pr, hh = H - pt - pb;
      var mx = U.niceMax(Math.max.apply(null, W.base.concat(W.down)) * 1.12 || 1), s = '', bw = w / n, gap = Math.max(1.5, bw * 0.26);
      function Y(v) { return pt + hh * (1 - Math.max(0, v) / mx); }
      function cx(j) { return pl + bw * j + bw / 2; }
      for (var i = 0; i <= 4; i++) { var v = mx * i / 4; s += '<line x1="' + pl + '" x2="' + (Wd - pr) + '" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '" stroke="#D3DCE2" stroke-width="1"/><text x="' + (pl - 6) + '" y="' + (Y(v) + 4).toFixed(1) + '" text-anchor="end">' + esc(i ? '₪' + F.num(v) : '0') + '</text>'; }
      for (var j = 0; j < n; j++) {
        var x = pl + bw * j + gap / 2, fill = j === 0 ? '#12202A' : j === W.cheap ? '#4F9A5C' : '#2F6F86';
        if (W.base[j] >= 0.5) s += '<rect x="' + x.toFixed(1) + '" y="' + Y(W.base[j]).toFixed(1) + '" width="' + (bw - gap).toFixed(1) + '" height="' + (Y(0) - Y(W.base[j])).toFixed(1) + '" fill="' + fill + '"/>';
        var ev = W.ev[j], my = H - pb + 12, k = 0;
        if (ev.some(function (e) { return e.t === 'cut20' || e.t === 'cut30'; })) { s += '<rect x="' + (cx(j) - 4).toFixed(1) + '" y="' + (my - 4) + '" width="8" height="8" fill="#1F4B5C" transform="rotate(45 ' + cx(j).toFixed(1) + ' ' + my + ')"/>'; k++; }
        if (ev.some(function (e) { return e.t === 'reset'; })) s += '<circle cx="' + cx(j).toFixed(1) + '" cy="' + (my + (k ? 13 : 0)) + '" r="4.5" fill="#FFFFFF" stroke="#1F4B5C" stroke-width="2"/>';
        if (j % (Wd < 560 ? 6 : 3) === 0) s += '<text x="' + cx(j).toFixed(1) + '" y="' + (H - 6) + '" text-anchor="middle">' + esc(F.mshort(W.months[j])) + '</text>';
      }
      /* the two scenarios start next month: today's averages are known */
      function line(arr, col, dash) { var p = arr.slice(1).map(function (v, q) { return cx(q + 1).toFixed(1) + ',' + Y(v).toFixed(1); }).join(' '); return '<polyline points="' + p + '" fill="none" stroke="' + col + '" stroke-width="2" stroke-dasharray="' + dash + '"/>'; }
      s += line(W.down, '#C42550', '5 3') + line(W.up, '#12202A', '1.5 3');
      function lab(j, txt) { var x0 = cx(j), anc = x0 < pl + 40 ? 'start' : x0 > Wd - pr - 40 ? 'end' : 'middle'; return '<text class="v" x="' + (anc === 'start' ? x0 - bw / 2 : anc === 'end' ? x0 + bw / 2 : x0).toFixed(1) + '" y="' + (Y(W.base[j]) - 6).toFixed(1) + '" text-anchor="' + anc + '">' + esc(txt) + '</text>'; }
      s += lab(0, W.base[0] >= 0.5 ? F.ils(W.base[0]) : 'אין');
      if (W.cheap) s += lab(W.cheap, W.base[W.cheap] >= 0.5 ? F.ils(W.base[W.cheap]) : 'אין');
      var aria = 'עמלת ההיוון לכל המשכנתא בכל חודש מ־' + F.month(W.months[0]) + ' עד ' + F.month(W.months[n - 1]) + ', אם הממוצעים לא ישתנו: היום ' + F.ils(W.base[0]) + (W.cheap ? ', החודש הזול ' + F.month(W.months[W.cheap]) + ' ' + F.ils(W.base[W.cheap]) : '') + '. הפירוט בטבלה שמתחת.';
      return '<svg viewBox="0 0 ' + Wd + ' ' + H + '" role="img" aria-label="' + esc(aria) + '">' + s + '</svg>';
    }

    /* ------------------------------------------------------------------------------------------ the bank's number */
    function paintBank() {
      ob.innerHTML = ''; if (!last) return;
      var MG = last.MG;
      if (!(st.bank > 0)) { ob.appendChild(el('p', 'mrx__hint', 'הקלידו את עמלת ההיוון מהדוח לסילוק, ונשווה אותה לחישוב של ' + esc(F.month(NOW)) + ': ' + (MG.fee >= 0.5 ? b(MG.fee) : 'אין עמלת היוון') + '.')); return; }
      var c = G.NLHV.compare(MG.fee, st.bank);
      ob.appendChild(U.lines([['החישוב כאן, ' + F.month(NOW), MG.fee >= 0.5 ? F.ils(MG.fee) : 'אין עמלת היוון'], ['המספר של הבנק', F.ils(st.bank)],
        ['ההפרש', Math.abs(c.d) < 0.5 ? 'אין הפרש' : F.sils(c.d) + (c.pct != null ? ' (' + F.spc(100 * c.pct, 1) + ')' : '')]]));
      var p = el('p', 'nli__note ' + (c.close ? 'mhv__ok' : 'mhv__gap'));
      p.innerHTML = c.close ? 'המספר של הבנק קרוב לחישוב כאן. הפער הקטן הוא עיגול ותאריכים: הבנק מחשב לפי ימים ולפי מועדי התשלום המדויקים.'
        : 'יש פער של ' + b(Math.abs(c.d)) + '. פער לא אומר שמישהו טעה: לבנק יש את הנתונים המדויקים של ההלוואה. אלה הסיבות הרגילות להבדל:';
      ob.appendChild(p);
      if (c.close) return;
      var why = [];
      if (MG.linked) why.push('המדד: הבנק מצמיד את היתרה למדד האחרון שפורסם ביום הפירעון (המדד מתפרסם ב־15 לחודש). כאן המדד של ' + esc(F.month(C ? C.latest : NOW)) + '.');
      why.push('הממוצע ביום הפירעון: בנק ישראל מעדכן את הממוצעים פעם בחודש, בערך ב־19. כאן הממוצעים שבתוקף מ־' + esc(F.date(TN[0])) + '; אם הדוח הוכן ליום אחר, הממוצע בו יכול להיות אחר.');
      why.push('הודעה מוקדמת: אם הודעתם לבנק פחות מ־10 ימים מראש נוספים 0.1% מהסכום (' + b(MG.notice) + ' כאן, בשורה נפרדת). יש דוחות שמצרפים אותם לעמלה.');
      why.push('עיגול ותאריכים: הבנק מחשב לפי ימים ולפי מועדי התשלום המדויקים, וכאן החישוב לפי חודשים שלמים.');
      why.push('נתוני ההלוואה: יתרה אחרי פירעונות קודמים, תקופת גרייס, לוח קרן שווה או ריבית שהשתנתה משנים את החישוב. השוו את היתרה והריבית לדוח השנתי של הבנק.');
      why.push('הוותק: ההפחתה של 20% ו־30% נספרת מיום מתן ההלוואה לפי החוזה' + (MG.vars ? ', ובמסלול משתנה התקופה עד יום שינוי הריבית לפי החוזה' : '') + '.');
      ob.appendChild(el('ol', 'mhv__why', why.map(function (x) { return '<li>' + x + '</li>'; }).join('')));
      ob.appendChild(el('p', 'mrx__hint', 'אפשר לבקש מהבנק את פירוט החישוב: הממוצע שנלקח והתאריך שלו, היתרה ותאריך הפירעון.'));
    }

    /* ------------------------------------------------------------------------------------------------- share */
    function state() {
      var rn = function (v, q) { return isFinite(v) ? Math.round(v * q) / q : null; };
      return { r: st.rows.map(function (r) { return [r.k, rn(r.amount, 1), r.date, rn(r.term, 100), r.unit, rn(r.rate, 10000), isVar(r.k) ? (+r.freq || 60) : null]; }),
        pp: rn(st.pp, 1), md: st.mode, nt: st.notice, bk: st.bank ? rn(st.bank, 1) : null };
    }
    function summary() {
      if (!last) return 'עמלת היוון: השלימו את המסלולים.';
      var MG = last.MG, nt = noticeUsed(MG), tx = ['עמלת היוון למשכנתא, בפירעון ב־' + F.month(NOW) + ':'];
      MG.loans.filter(function (l) { return l.active; }).forEach(function (l) {
        tx.push((l.id + 1) + '. ' + tname(l) + ': יתרה ' + F.ils(l.fx.bal) + ', ' + (l.fx.fee >= 0.5 ? 'עמלת היוון ' + F.ils(l.fx.fee) + (l.fx.cut ? ' (אחרי הפחתה של ' + F.num(100 * l.fx.cut) + '%)' : '') : noFee(l).replace(/^ללא: /, 'אין עמלת היוון, ')) + '.');
      });
      tx.push('סך הכול: יתרה ' + F.ils(MG.bal) + ', עמלת היוון ' + (MG.fee >= 0.5 ? F.ils(MG.fee) : 'אין') + ', עמלה תפעולית עד ' + F.ils(MG.op) + (nt > 0.5 ? ', הודעה של פחות מ־10 ימים ' + F.ils(nt) : '') + '.');
      if (st.pp > 0) { var A = G.NLHV.allocate(MG, st.pp, st.mode, D); tx.push('פירעון חלקי של ' + F.ils(A.amount) + ' בחלוקה הזולה: עמלת היוון ' + (A.fee >= 0.5 ? F.ils(A.fee) : 'אין') + (st.mode === 'shorten' ? ', קיצור התקופה' : ', ההחזר יורד ב־' + F.ils(A.drop)) + ', חיסכון בריבית ' + F.ils(A.saved) + '.'); }
      if (lastW) tx.push(lastW.cheap ? 'החודש הזול ב־24 החודשים, אם הממוצעים לא ישתנו: ' + F.month(lastW.months[lastW.cheap]) + ', ' + F.ils(lastW.base[lastW.cheap]) + ' (' + F.ils(lastW.save) + ' פחות מהיום).' : 'אם הממוצעים לא ישתנו, אין ב־24 החודשים הקרובים חודש זול מהיום.');
      if (st.bank > 0) tx.push('הבנק נתן ' + F.ils(st.bank) + ', הפרש של ' + F.ils(Math.abs(st.bank - MG.fee)) + '.');
      tx.push('לפי צו הבנקאות והממוצעים של בנק ישראל בתוקף מ־' + F.date(TN[0]) + '.');
      return tx.join('\n');
    }
    function paintShare() { U.shareBar(P.share, summary, function () { return U.link('mhivun', state()); }); }

    buildForm(); run();
    U.resized(function () { if (last) paintWhen(); });
  }
})();
