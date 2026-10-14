/* NadLan Instruments · delay v1 (HAD-527): compensation for a late new-apartment delivery, Sale (Apartments) Law s.5א.
   Contracts from 7.7.2022: after one month of grace, rent for months 2-4 from the contractual date, 1.25 x rent for months
   5-10, 1.5 x rent from month 11; each month or part of it counts. Contracts until 6.7.2022: once 60 days passed, 1.5 x rent
   from the contractual date to the end of month 8, then 1.25 x rent from month 9. The higher of the law and the contract.
   Pure logic in NLDX for unit checks. */
(function () {
  'use strict';
  var NEW_LAW = '2022-07-07';
  function d(iso) { var p = iso.split('-').map(Number); return Date.UTC(p[0], p[1] - 1, p[2]); }
  function addM(iso, n) { var p = iso.split('-').map(Number); var x = new Date(Date.UTC(p[0], p[1] - 1 + n, p[2])); if (x.getUTCDate() !== p[2]) x = new Date(Date.UTC(p[0], p[1] - 1 + n + 1, 0)); return x.toISOString().slice(0, 10); }
  function today() { return new Date().toISOString().slice(0, 10); }
  // started months of delay: month k covers (contract + (k-1) months, contract + k months]
  function startedMonths(due, until) { if (d(until) <= d(due)) return 0; var k = 0; while (d(addM(due, k)) < d(until)) k++; return k; }
  function compute(v) {
    var due = v.due, until = v.state === 'open' ? (v.asof || today()) : v.handed, rent = v.rent;
    if (!/^\d{4}-\d{2}-\d{2}$/.test(v.signed || '')) return { error: { field: 'signed', msg: 'בחרו את תאריך חתימת החוזה.' } };
    if (!/^\d{4}-\d{2}-\d{2}$/.test(due || '')) return { error: { field: 'due', msg: 'בחרו את מועד המסירה שנקבע בחוזה.' } };
    if (!/^\d{4}-\d{2}-\d{2}$/.test(until || '')) return { error: { field: 'handed', msg: 'בחרו את תאריך המסירה בפועל.' } };
    if (!(rent > 300)) return { error: { field: 'rent', msg: 'הקלידו דמי שכירות חודשיים של דירה דומה באזור.' } };
    var newLaw = v.signed >= NEW_LAW, n = startedMonths(due, until), months = [], total = 0, days = Math.round((d(until) - d(due)) / 864e5);
    var entitled = newLaw ? n > 1 : days > 60;
    for (var k = 1; k <= n; k++) {
      var mult = newLaw ? (k === 1 ? 0 : k <= 4 ? 1 : k <= 10 ? 1.25 : 1.5) : (k <= 8 ? 1.5 : 1.25);
      if (!entitled) mult = 0;
      var amt = rent * mult; total += amt;
      months.push({ k: k, from: addM(due, k - 1), to: addM(due, k), mult: mult, amt: amt });
    }
    var contractTotal = (v.contract > 0 ? v.contract : 0) * n;
    return { newLaw: newLaw, n: n, days: days, entitled: entitled, months: months, total: total, until: until, contractTotal: contractTotal, best: Math.max(total, contractTotal) };
  }
  window.NLDX = { compute: compute, startedMonths: startedMonths };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  window.NadLanInstruments.register('delay', {
    kicker: 'מחשבון · דירה מקבלן',
    title: 'כמה פיצוי מגיע על איחור במסירה',
    lede: 'תאריך החוזה, מועד המסירה שנקבע בו, והמועד שבו קיבלתם את הדירה (ואם עוד לא קיבלתם, החישוב עד היום): המחשבון מחיל את סעיף 5א לחוק המכר, חודש אחרי חודש, לפי דמי השכירות של דירה דומה באזור.',
    defaults: function () { return { signed: '2023-02-01', due: '2025-12-31', state: 'open', handed: '2026-09-15', asof: '', rent: 7800, contract: 0 }; },
    fields: [
      { id: 'signed', label: 'תאריך חתימת החוזה', type: 'date', help: 'מ־7.7.2022 חל הנוסח החדש של החוק.' },
      { id: 'due', label: 'מועד המסירה בחוזה', type: 'date' },
      { id: 'state', label: 'הדירה', type: 'segmented', options: [{ value: 'open', label: 'עוד לא נמסרה' }, { value: 'done', label: 'נמסרה' }] },
      { id: 'handed', label: 'תאריך המסירה בפועל', type: 'date', showIf: function (v) { return v.state === 'done'; } },
      { id: 'rent', label: 'שכר דירה חודשי של דירה דומה באזור', type: 'money', unit: '₪', help: 'דירה בגודל ובמיקום דומים. מחירי השכירות לפי עיר: <a href="/apartment-prices/">מחירון הדירות</a>.' },
      { id: 'contract', label: 'פיצוי חודשי שנקבע בחוזה (אם יש)', type: 'money', unit: '₪' }
    ],
    compute: function (v) {
      var r = compute(v); if (r.error) return r;
      var lines = [
        { label: 'ימי איחור עד ' + F.date(r.until), value: F.num(r.days) + ' ימים' },
        { label: 'חודשים שהתחילו', value: F.num(r.n) },
        { label: 'הנוסח החל על החוזה', value: r.newLaw ? 'מ־7.7.2022' : 'עד 6.7.2022' }
      ];
      if (r.contractTotal > 0) lines.push({ label: 'לפי הפיצוי שבחוזה', value: F.ils(r.contractTotal) });
      var b = [{ label: '×1', value: 0, kind: 'open' }, { label: '×1.25', value: 0, kind: 'civic' }, { label: '×1.5', value: 0, kind: 'survey' }];
      r.months.forEach(function (m) { if (m.mult === 1) b[0].value += m.amt; else if (m.mult === 1.25) b[1].value += m.amt; else if (m.mult === 1.5) b[2].value += m.amt; });
      var note = !r.entitled ? (r.newLaw ? 'החודש הראשון אחרי מועד המסירה הוא חודש חסד: אם הדירה נמסרה בתוכו, לא מגיע פיצוי לפי החוק.' : 'בחוזה לפני 7.7.2022, הפיצוי מגיע רק כשהאיחור עובר 60 ימים, ואז הוא מחושב מהמועד שבחוזה.') :
        'הפיצוי משולם בסוף כל חודש, בלי צורך להוכיח נזק. הוא לא חל כשהאיחור נגרם רק מהקונה, או בנסיבות של סעיף 18(א) לחוק החוזים (תרופות).';
      return {
        answer: { label: 'הפיצוי לפי חוק המכר', value: F.ils(r.best), tone: 'survey', sub: r.entitled ? '<bdi>' + F.num(r.n) + '</bdi> חודשים · ' + (r.contractTotal > r.total ? 'הפיצוי שבחוזה גבוה יותר, ולכן הוא שקובע' : 'הסכום הגבוה מבין החוק לחוזה') : 'עוד לא מגיע פיצוי לפי החוק' },
        breakdown: b.filter(function (x) { return x.value > 0; }).map(function (x) { return { label: 'שכר דירה ' + x.label, value: x.value, kind: x.kind }; }),
        lines: lines,
        note: note,
        table: { title: 'הפירוט חודש אחרי חודש', head: ['חודש', 'מתאריך', 'עד תאריך', 'מכפיל', 'פיצוי'], num: [0, 3, 4],
          rows: r.months.map(function (m) { return [String(m.k), F.date(m.from), F.date(m.to), m.mult ? '×' + m.mult : 'חסד', F.ils(m.amt)]; }) },
        formula: r.newLaw ? 'חוזה מ־7.7.2022: חודש 1 חסד · חודשים 2 עד 4: שכר דירה · 5 עד 10: שכר דירה × 1.25 · מ־11: שכר דירה × 1.5. כל חודש או חלק ממנו.' : 'חוזה עד 6.7.2022: מעל 60 ימי איחור, מהמועד שבחוזה: חודשים 1 עד 8: שכר דירה × 1.5 · מ־9: שכר דירה × 1.25.',
        sources: [{ label: 'חוק המכר (דירות), סעיף 5א', url: 'https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%9B%D7%A8_(%D7%93%D7%99%D7%A8%D7%95%D7%AA)' }],
        text: 'מחשבון פיצוי על איחור במסירה: מועד מסירה ' + F.date(v.due) + ', איחור ' + F.num(r.days) + ' ימים, שכר דירה ' + F.ils(v.rent) + '. פיצוי לפי חוק המכר: ' + F.ils(r.best) + '.'
      };
    }
  });
})();
