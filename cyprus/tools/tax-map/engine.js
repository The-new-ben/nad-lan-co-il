/* CY-PRUS Instruments: Israel-Cyprus sale tax engine (pure, no DOM).
   a: {buy, sell, costs (purchase and sale expenses), main: lived in it 5 years as home, used: lifetime exemption already used}
   Cyprus: 20% on the gain after the lifetime exemption (before Cyprus CPI indexing, which lowers the gain) + 0.40% seller fee.
   Israel: up to 25% on the gain, minus a credit for the Cyprus tax (capped at the Israeli tax). Estimate in euro. */
(function (root) {
  'use strict';

  function sale(a, R) {
    var gain = Math.max(0, a.sell - a.buy - Math.max(0, a.costs || 0)),
      exemption = a.used ? 0 : (a.main ? R.cy_exempt_main : R.cy_exempt_general),
      cyTaxable = Math.max(0, gain - exemption),
      cyTax = cyTaxable * R.cy_cgt_rate,
      fee = a.sell * R.cy_seller_fee,
      ilGross = gain * R.il_cgt_rate,
      ilNet = Math.max(0, ilGross - cyTax),
      total = cyTax + fee + ilNet;
    return {
      gain: Math.round(gain),
      exemption: exemption,
      cyTax: Math.round(cyTax),
      fee: Math.round(fee),
      ilGross: Math.round(ilGross),
      credit: Math.round(Math.min(cyTax, ilGross)),
      ilNet: Math.round(ilNet),
      total: Math.round(total),
      net: Math.round(a.sell - total)
    };
  }

  var api = { sale: sale };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  else { root.CYXTaxMap = api; }
}(typeof window !== 'undefined' ? window : this));
