/* CY-PRUS Instruments: Israel-to-Cyprus transfer cost engine (pure, no DOM).
   a: {eur: amount that should arrive, channel: 'branch'|'internet', cy: Cyprus bank id}
   Per Israeli bank: transfer fee + conversion fee (USD tiers from the tariff), plus the Cyprus incoming fee (EUR tiers).
   Exchange-rate margins and correspondent costs are not published and are not included. */
(function (root) {
  'use strict';

  // tiers: {up_to_X, fixed_X} | {above_X or from_X, rate_pct, min_X, max_X}; X = 'usd' or 'eur'
  function tierFee(amount, tiers, cur) {
    var i, t, up, fee;
    for (i = 0; i < tiers.length; i += 1) {
      t = tiers[i]; up = t['up_to_' + cur];
      if (up !== undefined && amount <= up) { return t['fixed_' + cur] || 0; }
      if (t.rate_pct !== undefined && up === undefined) {
        fee = amount * t.rate_pct / 100;
        if (t['min_' + cur] !== undefined && t['min_' + cur] !== null) { fee = Math.max(fee, t['min_' + cur]); }
        if (t['max_' + cur] !== undefined && t['max_' + cur] !== null) { fee = Math.min(fee, t['max_' + cur]); }
        return fee;
      }
      if (up === undefined && t['fixed_' + cur] !== undefined) { return t['fixed_' + cur]; }
    }
    return 0;
  }

  function compare(a, R) {
    var usd = a.eur * R.fx.eur_ils / R.fx.usd_ils, ils = a.eur * R.fx.eur_ils, cy, inEur, rows = [], i, b, tr, cv, total;
    for (i = 0; i < R.cyprus.length; i += 1) { if (R.cyprus[i].id === a.cy) { cy = R.cyprus[i]; } }
    inEur = cy ? tierFee(a.eur, cy.incoming.tiers, 'eur') : 0;
    for (i = 0; i < R.israel.length; i += 1) {
      b = R.israel[i];
      tr = tierFee(usd, b.transfer[a.channel].tiers, 'usd') * R.fx.usd_ils;
      cv = tierFee(usd, b.conversion[a.channel].tiers, 'usd') * R.fx.usd_ils;
      total = tr + cv + inEur * R.fx.eur_ils;
      rows.push({ id: b.id, name: b.name, transfer: Math.round(tr), conversion: Math.round(cv), incoming: Math.round(inEur * R.fx.eur_ils), total: Math.round(total), pct: total / ils });
    }
    rows.sort(function (x, y) { return x.total - y.total; });
    return { ils: Math.round(ils), incomingEur: Math.round(inEur * 100) / 100, cyName: cy ? cy.name : '', rows: rows,
             cheapest: rows[0], dearest: rows[rows.length - 1] };
  }

  var api = { compare: compare, tierFee: tierFee };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  else { root.CYXTransfer = api; }
}(typeof window !== 'undefined' ? window : this));
