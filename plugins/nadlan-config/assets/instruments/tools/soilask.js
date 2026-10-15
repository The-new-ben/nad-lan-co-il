/* NadLan Instruments · soilask v1 (HAD-534): the letter of questions about the soil, for someone buying in Sde Dov (before
   signing or after). It opens with what was published on the chosen plot (a report with its peak, the nine-plot list without a
   report, the developer's own statement, or nothing published) and asks what follows from it: sampling under the 12.2.2026
   guidelines, the full report, the ministry's written adoption, a treatment plan, the schedule and the delivery date, who
   pays, the contract. A full letter or a short WhatsApp message, copied or sent as is (no link of ours). Data:
   data/sde-dov-soil.json. Pure logic in NLAX for unit checks. */
(function () {
  'use strict';
  var NAME = {};  // Ben 15.10.2026: no project or company names on the soil page; the letter names the plot only
  var ORDER = ['303', '301', '2270', '2206', '2255', '2701', '822', '103', '105', '107', '2207', '106', '2102', '2203'];
  function dmy(iso) { var p = String(iso || '').slice(0, 10).split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : ''; }
  function xs(x) { return 'פי ' + (x >= 10 ? Math.round(x).toLocaleString('he-IL') : (Math.round(x * 10) / 10).toString()); }
  function letter(rec, plot, stage, form) {
    var p = plot === 'other' ? '' : plot, st = rec ? rec.status : 'none', q = [], open;
    if (st === 'published_report') open = 'לפי דו״ח סקר הקרקע של מגרש ' + p + ', שפורסם במאגר המשרד להגנת הסביבה' + (rec.report ? ' ב־' + dmy(rec.report) : '') + ', נמצאה במגרש חריגה של PFOS מעל ערך הסף למגע ישיר: השיא ' + xs(rec.pfosX)
      + (rec.pfosDepth != null ? ', בעומק ' + rec.pfosDepth + ' מ׳' : '') + (rec.holes ? ', ב־' + rec.pfosHoles + ' מתוך ' + rec.holes + ' קידוחים' : '') + '.';
    else if (st === 'findings_reported_no_report') open = 'מגרש ' + p + ' מופיע ברשימת תשעת המגרשים ברובע שבהם נמסר על ממצאים, ודו״ח הסקר שלו לא פורסם במאגר המשרד להגנת הסביבה.';
    else if (st === 'developer_reported_no_exceedance') open = 'לפי מה שמסרה החברה, בסקר הקרקע במגרש ' + p + ' לא נמצאו חריגות.';
    else if (st === 'under_testing_per_developer') open = 'לפי מה שמסרה החברה, מגרש ' + p + ' נמצא בבדיקה אחרי הדיגום.';
    else open = 'לאור בדיקות הקרקע לחומרי PFAS ברובע מאז פברואר 2026, אבקש מידע על מצב הקרקע במגרש' + (p ? ' ' + p : ' שבו נמצאת הדירה') + '.';
    q.push('האם המגרש נדגם לפי ההנחיות של המשרד להגנת הסביבה מ־12.2.2026? באילו תאריכים, וכמה קידוחים נעשו?');
    if (st === 'published_report') q.push('האם הוגשה תכנית לטיפול בקרקע, והאם המשרד אישר אותה? מתי הטיפול צפוי להסתיים?');
    else if (st === 'developer_reported_no_exceedance') q.push('אבקש לקבל את מכתב המשרד להגנת הסביבה שמאמץ את ממצאי הסקר, ואת הדו״ח עצמו.');
    else q.push('אבקש לקבל את דו״ח סקר הקרקע המלא של המגרש.');
    q.push('האם המשרד להגנת הסביבה אימץ את ממצאי הסקר בכתב?');
    q.push('האם הבדיקה או הטיפול בקרקע עלולים להשפיע על לוח הזמנים של הבנייה ועל מועד המסירה שבחוזה?');
    q.push('מי נושא בעלות הבדיקה והטיפול בקרקע, והאם יש תרחיש שבו העלות תועבר לרוכשים?');
    q.push('האם ניתן היתר לבנייה או לחפירה ודיפון, והאם יש בו תנאים לגבי הקרקע?');
    q.push(stage === 'after' ? 'אבקש שתעדכנו אותי בכתב בכל ממצא חדש או החלטה של המשרד לגבי המגרש.'
      : 'האם תסכימו להוסיף לחוזה הצהרה שהקרקע טופלה לפי דרישות המשרד להגנת הסביבה לפני מסירת הדירה, והתחייבות לעדכן אותי בכל ממצא חדש?');
    var head = (NAME[p] ? 'לכבוד צוות ' + NAME[p] : 'לכבוד החברה היזמית') + (p ? ', מגרש ' + p + ' בשדה דב' : ', רובע שדה דב');
    if (form === 'wa') { var s = [0, 1, 3, 4]; return { n: s.length, text: 'שלום, ' + (stage === 'after' ? 'אני רוכש/ת דירה ' : 'אני שוקל/ת לקנות דירה ') + (NAME[p] ? 'בפרויקט ' + NAME[p] : 'ברובע שדה דב') + (p ? ' (מגרש ' + p + ')' : '') + '. '
      + open + '\n' + s.map(function (i, k) { return (k + 1) + '. ' + q[i]; }).join('\n') + '\nתודה.' }; }
    return { n: q.length, text: head + '\n\nשלום רב,\n' + (stage === 'after' ? 'אני רוכש/ת דירה ' : 'אני שוקל/ת לקנות דירה ') + (NAME[p] ? 'בפרויקט ' + NAME[p] : 'ברובע שדה דב') + '. ' + open + '\n\nאבקש תשובה בכתב לשאלות הבאות:\n'
      + q.map(function (x, k) { return (k + 1) + '. ' + x; }).join('\n') + '\n\nאודה לתשובתכם בכתב.\nבברכה,\n[השם שלכם]\n[טלפון]' };
  }
  window.NLAX = { letter: letter };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt;
  window.NadLanInstruments.register('soilask', {
    kicker: 'מחולל · שדה דב',
    title: 'מכתב שאלות ליזם על הקרקע במגרש',
    lede: 'בוחרים את המגרש או הפרויקט, ומקבלים מכתב מוכן ליזם, שנפתח במה שפורסם על המגרש ושואל את השאלות שנובעות מזה. מעתיקים או שולחים בוואטסאפ.',
    defaults: function () { return { plot: '2206', stage: 'before', form: 'mail' }; },
    fields: [
      { id: 'plot', label: 'המגרש או הפרויקט', type: 'select', options: ORDER.map(function (p) { return { value: p, label: 'מגרש ' + p + (NAME[p] ? ' · ' + NAME[p] : '') }; }).concat([{ value: 'other', label: 'מגרש אחר ברובע' }]) },
      { id: 'stage', label: 'איפה אתם עומדים', type: 'segmented', options: [{ value: 'before', label: 'לפני חתימה' }, { value: 'after', label: 'כבר חתמתי' }] },
      { id: 'form', label: 'איך שולחים', type: 'segmented', options: [{ value: 'mail', label: 'מכתב מלא' }, { value: 'wa', label: 'הודעת וואטסאפ קצרה' }] }
    ],
    compute: function (v, data) {
      var d = data.soil, rec = null;
      d.records.forEach(function (r) { if (r.plot === v.plot) rec = r; });
      var L = letter(rec, v.plot, v.stage, v.form);
      var what = !rec ? 'לא פורסם דו״ח על המגרש' : rec.status === 'published_report' ? 'דו״ח שפורסם: ' + xs(rec.pfosX) + ' מעל הסף'
        : rec.status === 'findings_reported_no_report' ? 'ברשימת המגרשים עם ממצאים, בלי דו״ח' : rec.status === 'developer_reported_no_exceedance' ? 'לפי היזם: בלי חריגות' : 'לפי היזם: בבדיקה';
      return {
        answer: { label: 'המכתב מוכן', value: F.num(L.n) + ' שאלות', tone: 'ink', sub: (v.plot === 'other' ? 'מגרש אחר ברובע' : 'מגרש ' + v.plot) + ' · ' + what },
        doc: L.text, text: L.text, bare: true,
        note: 'המכתב לא מחליף ייעוץ משפטי. לפני חתימה, כדאי שעורך דין מקרקעין יעבור על החוזה ועל הסעיפים לגבי הקרקע: <a href="/real-estate-lawyer/">עורך דין לקניית דירה</a>. מה פורסם על כל מגרש: במפה בראש העמוד.'
      };
    }
  });
})();
