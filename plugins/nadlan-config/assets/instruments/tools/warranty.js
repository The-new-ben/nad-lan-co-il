/* NadLan Instruments · warranty v1.2 (HAD-527 turn 4; 1.72.452: the status cell carries its end date, phones hide the two date columns): the Sale (Apartments) Law clock. From the day the apartment was handed
   over: every item of the law's schedule (bdek 1-7 years), the 3-year warranty after each bdek, the 20 years for structural
   defects, and the notice deadline for a defect visible at handover (one year, s.4א). Facts: docs/tools/warranty/facts.md.
   Pure logic in NLWX for unit checks. */
(function () {
  'use strict';
  var ITEMS = [
    ['כל ליקוי אחר (שאינו יסודי)', 1], ['מסגרות ונגרות, אלומיניום ופלסטיק', 2], ['ריצוף וחיפוי פנים, שקיעות ושחיקה', 2],
    ['מכונות ודוודים', 3], ['פיתוח החצר, שקיעות', 3], ['בידוד תרמי', 3], ['צנרת: מים, הסקה ומרזבים', 4],
    ['איטום המבנה, כולל חללים תת־קרקעיים', 4], ['סדקים מעל 1.5 מ"מ ברכיבים לא נושאים', 5], ['חיפויי חוץ: התנתקות, התקלפות, התפוררות', 7]
  ];
  function addY(iso, y) { var p = iso.split('-').map(Number); var d = new Date(Date.UTC(p[0] + y, p[1] - 1, p[2])); if (d.getUTCMonth() !== p[1] - 1) d = new Date(Date.UTC(p[0] + y, p[1], 0)); return d.toISOString().slice(0, 10); }
  function days(a, b) { return Math.round((Date.parse(b) - Date.parse(a)) / 864e5); }
  function compute(handed, asof) {
    var rows = ITEMS.map(function (it) { var be = addY(handed, it[1]), we = addY(be, 3);
      var st = asof <= be ? 'bdek' : asof <= we ? 'warranty' : 'over';
      return { name: it[0], years: it[1], bdekEnd: be, warEnd: we, st: st, left: st === 'bdek' ? days(asof, be) : st === 'warranty' ? days(asof, we) : 0 }; });
    var struct = addY(handed, 20), notice = addY(handed, 1);
    return { rows: rows, struct: struct, notice: notice, inBdek: rows.filter(function (r) { return r.st === 'bdek'; }).length,
      inWar: rows.filter(function (r) { return r.st === 'warranty'; }).length, next: rows.filter(function (r) { return r.st !== 'over'; }).sort(function (a, b) { return a.left - b.left; })[0] || null };
  }
  window.NLWX = { compute: compute, addY: addY };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  window.NadLanInstruments.register('warranty', {
    kicker: 'מחשבון · דירה מקבלן',
    title: 'שעון הבדק והאחריות של הדירה',
    lede: 'מהיום שבו קיבלתם את המפתח: לכל סוג ליקוי לפי התוספת לחוק המכר, מתי נגמרת תקופת הבדק, מתי נגמרת האחריות, וכמה ימים נשארו.',
    defaults: function () { return { handed: '2024-06-15', asof: new Date().toISOString().slice(0, 10) }; },
    fields: [
      { id: 'handed', label: 'תאריך קבלת הדירה (המסירה)', type: 'date' },
      { id: 'asof', label: 'נכון לתאריך', type: 'date', help: 'בדרך כלל היום. אפשר לבדוק גם תאריך עתידי.' }
    ],
    compute: function (v) {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(v.handed || '')) return { error: { field: 'handed', msg: 'בחרו את תאריך קבלת הדירה.' } };
      if (!/^\d{4}-\d{2}-\d{2}$/.test(v.asof || '') || v.asof < v.handed) return { error: { field: 'asof', msg: 'התאריך צריך להיות אחרי המסירה.' } };
      var r = compute(v.handed, v.asof);
      var sub = r.next ? 'הקרוב להסתיים: ' + r.next.name + ' · ' + (r.next.st === 'bdek' ? 'הבדק' : 'האחריות') + ' עד ' + F.date(r.next.st === 'bdek' ? r.next.bdekEnd : r.next.warEnd) : 'כל תקופות הבדק והאחריות שבתוספת הסתיימו. ליקוי יסודי במבנה: עד ' + F.date(r.struct) + '.';
      return {
        answer: { label: 'סוגי ליקויים שעדיין בתקופת בדק', value: F.num(r.inBdek) + ' מתוך 10', tone: r.next && r.next.left < 120 ? 'survey' : 'ink', sub: sub + (r.next ? ' (<bdi>' + F.num(r.next.left) + '</bdi> ימים)' : '') },
        breakdown: [{ label: 'בבדק', value: r.inBdek, kind: 'open', shown: F.num(r.inBdek) }, { label: 'באחריות', value: r.inWar, kind: 'civic', shown: F.num(r.inWar) }, { label: 'הסתיים', value: 10 - r.inBdek - r.inWar, kind: 'sea', shown: F.num(10 - r.inBdek - r.inWar) }],
        lines: [{ label: 'הודעה על ליקוי שנראה כבר במסירה', value: 'עד ' + F.date(r.notice) }, { label: 'ליקוי יסודי (נשיאה ויציבות)', value: 'עד ' + F.date(r.struct) }, { label: 'בבדק / באחריות / הסתיים', value: r.inBdek + ' / ' + r.inWar + ' / ' + (10 - r.inBdek - r.inWar) }],
        note: 'בתקופת הבדק, ליקוי שמתגלה נחשב לליקוי של הקבלן, והקבלן חייב לתקן אותו תוך זמן סביר. בשלוש שנות האחריות שאחריה, הקבלן עדיין אחראי, אבל הקונה צריך להראות שהליקוי נובע מהבנייה. מודיעים לקבלן בכתב, תוך זמן סביר מגילוי הליקוי.',
        table: { title: 'כל סוגי הליקויים לפי התוספת לחוק', head: ['הליקוי ותקופת הבדק', 'המצב היום', 'הבדק עד', 'האחריות עד'], num: [2, 3], phoneHide: [2, 3],
          rows: r.rows.map(function (x) { return [x.name + ' · ' + (x.years === 1 ? 'שנה' : x.years + ' שנים'),
            x.st === 'bdek' ? 'בבדק עד ' + F.date(x.bdekEnd) + ' · ' + F.num(x.left) + ' ימים' : x.st === 'warranty' ? 'באחריות עד ' + F.date(x.warEnd) + ' · ' + F.num(x.left) + ' ימים' : 'האחריות הסתיימה ב־' + F.date(x.warEnd),
            F.date(x.bdekEnd), F.date(x.warEnd)]; })
            .concat([['ליקוי יסודי במבנה · 20 שנה', v.asof <= r.struct ? 'בתוקף עד ' + F.date(r.struct) + ' · ' + F.num(days(v.asof, r.struct)) + ' ימים' : 'הסתיים ב־' + F.date(r.struct), F.date(r.struct), '']]) },
        formula: 'תקופת בדק: מיום המסירה, לפי התוספת לחוק המכר (שנה עד 7 שנים). תקופת אחריות: 3 שנים מסוף תקופת הבדק. ליקוי יסודי: 20 שנה מהמסירה.',
        sources: [{ label: 'חוק המכר (דירות): סעיפים 4, 4א, 4ב והתוספת', url: 'https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%9B%D7%A8_(%D7%93%D7%99%D7%A8%D7%95%D7%AA)' }],
        text: 'שעון הבדק והאחריות: דירה שנמסרה ב־' + F.date(v.handed) + '. נכון ל־' + F.date(v.asof) + ': ' + r.inBdek + ' סוגי ליקויים בבדק, ' + r.inWar + ' באחריות. ' + sub + '.'
      };
    }
  });
})();
