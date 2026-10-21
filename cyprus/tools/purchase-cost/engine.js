/* CY-PRUS Instruments: purchase-cost engine (pure, no DOM). The same function runs in the browser
   (window.CYXPurchaseCost) and in Node for the build-time example and the parity test.
   Every rate comes from the rules object (rules.json, built from official sources); nothing is hard-coded here. */
(function (root) {
  'use strict';

  function round(n) { return Math.round(n); }

  // Marginal bands: [{upto: 85000, rate: 0.03}, {upto: 170000, rate: 0.05}, {upto: null, rate: 0.08}]
  function banded(value, bands) {
    var total = 0, floor = 0, i, b, top, slice;
    for (i = 0; i < bands.length; i += 1) {
      b = bands[i];
      top = (b.upto === null || b.upto === undefined) ? Infinity : b.upto;
      if (value <= floor) { break; }
      slice = Math.min(value, top) - floor;
      if (slice > 0) { total += slice * b.rate; }
      floor = top;
    }
    return total;
  }

  // VAT on a new home. Reduced rate: on the first `reduced_first_m2` of the home only, inside the caps;
  // the rest of the area at the standard rate. Outside the caps the whole price is at the standard rate.
  function vat(input, r) {
    var v = r.vat, price = input.price, area = input.area || 0, perM2, reducedPart, eligible;
    if (!input.isNew) { return { amount: 0, mode: 'none' }; }
    if (!input.reducedVat) { return { amount: price * v.standard, mode: 'standard' }; }
    eligible = area > 0
      && (!v.reduced_max_total_area_m2 || area <= v.reduced_max_total_area_m2)
      && (!v.reduced_max_value || price <= v.reduced_max_value);
    if (!eligible) { return { amount: price * v.standard, mode: 'reduced-not-eligible' }; }
    perM2 = price / area;
    reducedPart = Math.min(area, v.reduced_first_m2) * perM2;
    if (v.reduced_max_value_first_part && reducedPart > v.reduced_max_value_first_part) {
      reducedPart = v.reduced_max_value_first_part;
    }
    return {
      amount: reducedPart * v.reduced + (price - reducedPart) * v.standard,
      mode: 'reduced',
      reducedPart: reducedPart
    };
  }

  function transferFees(input, r) {
    var t = r.transfer, buyers = Math.max(1, input.buyers || 1), share, gross;
    if (input.isNew && t.exempt_when_vat) { return { amount: 0, mode: 'exempt-vat' }; }
    share = t.per_buyer_share ? input.price / buyers : input.price;
    gross = banded(share, t.bands) * (t.per_buyer_share ? buyers : 1);
    return { amount: gross * (1 - (t.reduction || 0)), gross: gross, mode: 'payable' };
  }

  function stampDuty(input, r) {
    var s = r.stamp_duty, amt;
    if (!s || !s.active) { return { amount: 0, mode: 'inactive' }; }
    amt = banded(input.price, s.bands);
    if (s.cap) { amt = Math.min(amt, s.cap); }
    return { amount: amt, mode: 'payable' };
  }

  function mortgageRegistration(input, r) {
    var m = r.mortgage_registration;
    if (!input.mortgage || !m) { return { amount: 0, mode: 'none' }; }
    return { amount: input.mortgage * m.rate, mode: 'payable' };
  }

  // Market ranges (lawyer, valuation, bank): never law; shown as low to high.
  function market(input, r) {
    var out = [], i, m, low, high, base;
    for (i = 0; i < (r.market || []).length; i += 1) {
      m = r.market[i];
      if (m.only_with_mortgage && !input.mortgage) { continue; }
      base = m.basis === 'mortgage' ? (input.mortgage || 0) : input.price;
      low = m.low_rate !== undefined ? base * m.low_rate : (m.low || 0);
      high = m.high_rate !== undefined ? base * m.high_rate : (m.high || 0);
      if (m.vat) { low *= 1 + m.vat; high *= 1 + m.vat; }
      if (m.min) { low = Math.max(low, m.min); high = Math.max(high, m.min); }
      out.push({ key: m.key, low: round(low), high: round(high) });
    }
    return out;
  }

  // Fixed official fees (e.g. depositing the sale contract at the Land Registry).
  function fixedFees(rules) {
    var out = [], i, f;
    for (i = 0; i < (rules.fixed_fees || []).length; i += 1) { f = rules.fixed_fees[i]; out.push({ key: f.key, amount: f.amount }); }
    return out;
  }

  function purchaseCost(input, rules) {
    var v = vat(input, rules), t = transferFees(input, rules), s = stampDuty(input, rules),
      m = mortgageRegistration(input, rules), mk = market(input, rules), ff = fixedFees(rules),
      fixed = v.amount + t.amount + s.amount + m.amount, low = 0, high = 0, i;
    for (i = 0; i < ff.length; i += 1) { fixed += ff[i].amount; }
    for (i = 0; i < mk.length; i += 1) { low += mk[i].low; high += mk[i].high; }
    return {
      price: input.price,
      vat: { amount: round(v.amount), mode: v.mode, reducedPart: v.reducedPart ? round(v.reducedPart) : 0 },
      transfer: { amount: round(t.amount), gross: t.gross ? round(t.gross) : 0, mode: t.mode },
      stamp: { amount: round(s.amount), mode: s.mode },
      mortgageReg: { amount: round(m.amount), mode: m.mode },
      fixedFees: ff,
      market: mk,
      fixedTotal: round(fixed),
      totalLow: round(input.price + fixed + low),
      totalHigh: round(input.price + fixed + high),
      extraLow: round(fixed + low),
      extraHigh: round(fixed + high)
    };
  }

  var api = { purchaseCost: purchaseCost, banded: banded };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  else { root.CYXPurchaseCost = api; }
}(typeof window !== 'undefined' ? window : this));
