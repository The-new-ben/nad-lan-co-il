/* CY-PRUS Instruments: 5% VAT eligibility engine (pure, no DOM).
   a: {buyer: 'person'|'company', home: 'main'|'holiday', price, area, disability: bool, children: 0..n (beyond the third), timing: 'before'|'late'|'over'} */
(function (root) {
  'use strict';

  function check(a, R) {
    var checks = [], ok = true, firstM2, reducedPart = 0, vat5, vat19 = a.price * R.standard, eligible;
    function add(key, pass, soft) { checks.push({ key: key, pass: pass, soft: !!soft }); if (!pass && !soft) { ok = false; } }

    add('person', a.buyer === 'person');
    add('main', a.home === 'main');
    add('area', a.area > 0 && a.area <= R.max_total_area_m2);
    add('value', a.price > 0 && a.price <= R.max_total_value);
    add('timing', a.timing === 'before', a.timing === 'late');

    firstM2 = a.disability ? R.first_m2_disability : R.first_m2 + Math.max(0, a.children || 0) * R.extra_m2_per_child_beyond_third;
    eligible = ok;
    if (eligible) {
      reducedPart = Math.min(a.area, firstM2) * (a.price / a.area);
      reducedPart = Math.min(reducedPart, R.max_first_part_value);
      vat5 = reducedPart * R.reduced + (a.price - reducedPart) * R.standard;
    } else {
      vat5 = vat19;
    }
    return {
      eligible: eligible,
      late: a.timing === 'late',
      checks: checks,
      firstM2: firstM2,
      reducedPart: Math.round(reducedPart),
      vat: Math.round(vat5),
      vatStandard: Math.round(vat19),
      saving: Math.round(vat19 - vat5)
    };
  }

  var api = { check: check };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  else { root.CYXVat5 = api; }
}(typeof window !== 'undefined' ? window : this));
