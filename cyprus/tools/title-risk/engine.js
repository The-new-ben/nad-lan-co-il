/* CY-PRUS Instruments: title-deeds risk engine (pure, no DOM). The overall level is the highest level any answer raises;
   the lawyer list is built from fixed lines plus the groups the answers call for. */
(function (root) {
  'use strict';
  var ORDER = { low: 0, medium: 1, high: 2 };

  function assess(a, R) {
    var level = 'low', flags = [], i, q, ans, lv, L = R.lawyer_list, list = [];
    for (i = 0; i < R.questions.length; i += 1) {
      q = R.questions[i]; ans = a[q.id]; lv = q.answers[ans] || 'medium';
      if (ORDER[lv] > ORDER[level]) { level = lv; }
      if (q.flags && q.flags[ans]) { flags.push({ id: q.flags[ans], level: lv }); }
    }
    flags.sort(function (x, y) { return ORDER[y.level] - ORDER[x.level]; });
    list = list.concat(L.always);
    if (a.mortgage !== 'no') { list = list.concat(L.mortgage); }
    if (a.title !== 'yes') { list = list.concat(L.no_title); }
    if (a.assign === 'yes') { list = list.concat(L.assignment); }
    list = list.concat(L.final, L.israeli);
    return { level: level, flags: flags, lawyerList: list };
  }

  var api = { assess: assess };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; }
  else { root.CYXTitleRisk = api; }
}(typeof window !== 'undefined' ? window : this));
