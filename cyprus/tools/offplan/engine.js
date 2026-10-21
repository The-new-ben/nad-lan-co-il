/* CY-PRUS Instruments: off-plan payment schedule engine (pure, no DOM).
   a: {price (before VAT), vat: 'standard'|'reduced', pcts: [5 stage percentages of the price]}
   Each payment carries VAT on top; the 95% Form A release point is marked on the cumulative share. */
(function (root) {
  'use strict';

  function schedule(a, R) {
    var rate = a.vat === 'reduced' ? R.vat.reduced : R.vat.standard, total = a.price * (1 + rate),
      cum = 0, rows = [], i, p, eur, releaseAt = -1, sum = 0;
    for (i = 0; i < a.pcts.length; i += 1) { sum += Math.max(0, a.pcts[i] || 0); }
    for (i = 0; i < a.pcts.length; i += 1) {
      p = Math.max(0, a.pcts[i] || 0);
      eur = total * p / 100;
      cum += p;
      if (releaseAt < 0 && cum >= R.release_share * 100 && p > 0) { releaseAt = i; }
      rows.push({ stage: i, pct: p, cum: cum, eur: Math.round(eur), ils: Math.round(eur * R.fx.eur_ils), ilsShock: Math.round(eur * R.fx.eur_ils * (1 + R.shock)) });
    }
    return {
      rows: rows,
      sum: sum,
      ok: Math.abs(sum - 100) < 0.01,
      total: Math.round(total),
      vat: Math.round(total - a.price),
      ils: Math.round(total * R.fx.eur_ils),
      ilsShock: Math.round(total * R.fx.eur_ils * (1 + R.shock)),
      releaseAt: releaseAt
    };
  }

  var api = { schedule: schedule };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  else { root.CYXOffplan = api; }
}(typeof window !== 'undefined' ? window : this));
