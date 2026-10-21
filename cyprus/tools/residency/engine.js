/* CY-PRUS Instruments: permanent residence by investment (Regulation 6(2)) check engine (pure, no DOM).
   a: {route: 'home'|'other_property'|'company'|'fund', amount (EUR, before VAT), firstSale: bool, spouse: bool,
       minors: n, adults: n (adult children applying too), income (EUR a year), abroad: bool} */
(function (root) {
  'use strict';

  function check(a, R) {
    var route = R.routes[a.route], need = R.min_investment * (1 + Math.max(0, a.adults || 0)),
      incomeNeed = R.income_base + (a.spouse ? R.income_spouse : 0) + Math.max(0, a.minors || 0) * R.income_per_minor,
      people = 1 + (a.spouse ? 1 : 0) + Math.max(0, a.minors || 0) + Math.max(0, a.adults || 0),
      checks = [], ok = true;
    function add(key, pass) { checks.push({ key: key, pass: pass }); if (!pass) { ok = false; } }
    add('amount', a.amount >= need);
    if (route.first_sale_only) { add('first_sale', !!a.firstSale); }
    add('income', a.income >= incomeNeed);
    if (route.funds_from_abroad) { add('abroad', !!a.abroad); }
    return {
      ok: ok,
      checks: checks,
      need: need,
      vatOnTop: route.vat_on_top,
      incomeNeed: incomeNeed,
      amountGap: Math.max(0, need - a.amount),
      incomeGap: Math.max(0, incomeNeed - a.income),
      people: people,
      fees: R.fees.application + R.fees.arc_per_person * people
    };
  }

  var api = { check: check };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  else { root.CYXResidency = api; }
}(typeof window !== 'undefined' ? window : this));
