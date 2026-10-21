/* CY-PRUS Instruments: bank-account documents wizard engine (pure, no DOM).
   answers: {lives: 'israel'|'cyprus', passport: 'il'|'eu'|'us', purpose: 'property'|'relocate'|'company',
             funds: 'salary'|'sale'|'business'|'inheritance'|'loan', hebrew: true|false}
   Returns ordered groups of checklist lines, the opening channels, the fee rows and the fixed notes. */
(function (root) {
  'use strict';

  function checklist(a, R) {
    var groups = [], base = [], i;
    for (i = 0; i < R.base.length; i += 1) {
      if (R.base[i].id === 'bankref' && a.lives === 'cyprus') { continue; }
      base.push({ text: R.base[i].text, who: R.base[i].who });
    }
    if (a.passport === 'us') { base.push({ text: R.us_person.text, who: R.us_person.who }); }
    groups.push({ key: 'base', items: base });
    groups.push({ key: 'funds', items: [{ text: R.source_of_funds[a.funds].text, who: '' }] });
    groups.push({ key: 'purpose', items: R.purpose[a.purpose].items.map(function (t) { return { text: t, who: '' }; }) });
    if (a.hebrew) { groups.push({ key: 'hebrew', items: [{ text: R.hebrew.text, who: '' }] }); }
    return {
      groups: groups,
      channels: R.channels[a.lives === 'cyprus' ? 'cyprus' : 'israel'],
      fees: R.fees,
      basic: (a.lives === 'cyprus' || a.passport === 'eu') ? R.basic_account.text : '',
      always: R.always,
      count: groups.reduce(function (n, g) { return n + g.items.length; }, 0)
    };
  }

  var api = { checklist: checklist };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  else { root.CYXBankDocs = api; }
}(typeof window !== 'undefined' ? window : this));
