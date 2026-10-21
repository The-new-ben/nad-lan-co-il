/* CY-PRUS Instruments: net rental yield engine (pure, no DOM). Uses the purchase-cost engine for the true cost of
   buying, so the yield is measured on everything the investor pays, not on the list price.
   Browser: window.CYXNetYield (needs window.CYXPurchaseCost). Node: module.exports, requires ../purchase-cost/engine.js. */
(function (root) {
  'use strict';
  var PC = (typeof module !== 'undefined' && module.exports) ? require('../purchase-cost/engine.js') : root.CYXPurchaseCost;

  function round(n) { return Math.round(n); }

  function netYield(input, rules, pcRules) {
    var r = rules, gross = input.rent * input.months,
      ghs = gross * r.ghs_rate,
      taxable = Math.max(0, gross * (1 - r.deemed_deduction)),
      cyTax = PC.banded(taxable, r.income_tax_bands),
      expenses = Math.max(0, input.expenses || 0),
      netCy = gross - ghs - cyTax - expenses,
      ilTax = input.israelTrack ? gross * r.israel_flat_rate : 0,
      net = netCy - ilTax,
      cost = PC.purchaseCost({ price: input.price, isNew: input.isNew, reducedVat: false, area: 0, buyers: 1, mortgage: 0 }, pcRules);
    return {
      gross: round(gross),
      ghs: round(ghs),
      cyTax: round(cyTax),
      expenses: round(expenses),
      ilTax: round(ilTax),
      net: round(net),
      netMonthly: round(net / 12),
      grossYield: input.price ? gross / input.price : 0,
      netYieldHigh: cost.totalLow ? net / cost.totalLow : 0,
      netYieldLow: cost.totalHigh ? net / cost.totalHigh : 0,
      totalLow: cost.totalLow,
      totalHigh: cost.totalHigh
    };
  }

  var api = { netYield: netYield };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  else { root.CYXNetYield = api; }
}(typeof window !== 'undefined' ? window : this));
