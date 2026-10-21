/* CY-PRUS Instruments: Cyprus price list engine (pure, no DOM).
   a: {city, type: 'apartment'|'house', deal: 'resale'|'new', size: m2 (optional)} */
(function (root) {
  'use strict';

  function row(c, a) {
    var m2 = a.deal === 'resale' ? c.resale[a.type].m2 : null;
    return {
      median: a.deal === 'resale' ? c.resale[a.type].median : c['new'][a.type].median,
      m2: m2,
      asking: c.asking[a.type],
      yoy: c.yoy[a.type],
      contracts: c.contracts.jan_sep_2026,
      contractsChange: c.contracts.change_pct
    };
  }

  function lookup(a, R) {
    var me = row(R.cities[a.city], a), table = [], k, size = Math.max(0, a.size || 0);
    for (k in R.cities) { if (Object.prototype.hasOwnProperty.call(R.cities, k)) { table.push({ id: k, r: row(R.cities[k], a) }); } }
    table.sort(function (x, y) { return y.r.median - x.r.median; });
    return {
      me: me,
      bySizeDeals: (me.m2 && size) ? Math.round(me.m2 * size / 100) * 100 : null,
      bySizeAsking: size ? Math.round(me.asking * size / 100) * 100 : null,
      table: table
    };
  }

  var api = { lookup: lookup };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  else { root.CYXPriceList = api; }
}(typeof window !== 'undefined' ? window : this));
