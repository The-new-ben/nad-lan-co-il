/* NadLan Instruments · soilask v1 (HAD-534): the letter of questions about the soil, for someone buying in Sde Dov (before
   signing or after). It opens with what was published on the chosen plot (a report with its peak, the nine-plot list without a
   report, the developer's own statement, or nothing published) and asks what follows from it: sampling under the 12.2.2026
   guidelines, the full report, the ministry's written adoption, a treatment plan, the schedule and the delivery date, who
   pays, the contract. A full letter or a short WhatsApp message, copied or sent as is (no link of ours). Data:
   data/sde-dov-soil.json. Pure logic in NLAX for unit checks.
   HAD-534 (d), 21.10.2026: Hebrew and English. On an English page the interface is English and the letter itself can be
   written in English or in Hebrew (an Israeli developer answers a Hebrew letter in writing more readily); a Hebrew letter is
   printed right-to-left inside the English page (r.docDir). Source table: docs/tools/soil-en/strings-en.json (soilask). */
(function () {
  'use strict';
  var NAME = {};  // Ben 15.10.2026: no project or company names on the soil page; the letter names the plot only
  var ORDER = ['303', '301', '2270', '2206', '2255', '2701', '822', '103', '105', '107', '2207', '106', '2102', '2203'];
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  // The letter, in both languages ({p} the plot, {d} a date, {x} times the threshold, {m} metres, {a}/{b} boreholes).
  var LX = {
    he: {
      dmy: function (iso) { var p = String(iso || '').slice(0, 10).split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : ''; },
      xs: function (x) { return 'פי ' + (x >= 10 ? Math.round(x).toLocaleString('he-IL') : (Math.round(x * 10) / 10).toString()); },
      openReport: 'לפי דו״ח סקר הקרקע של מגרש {p}, שפורסם במאגר המשרד להגנת הסביבה{date}, נמצאה במגרש חריגה של PFOS מעל ערך הסף למגע ישיר: השיא {x}{depth}{holes}.',
      openDate: ' ב־{d}', openDepth: ', בעומק {m} מ׳', openHoles: ', ב־{a} מתוך {b} קידוחים',
      openFindings: 'מגרש {p} מופיע ברשימת תשעת המגרשים ברובע שבהם נמסר על ממצאים, ודו״ח הסקר שלו לא פורסם במאגר המשרד להגנת הסביבה.',
      openDevClear: 'לפי מה שמסרה החברה, בסקר הקרקע במגרש {p} לא נמצאו חריגות.',
      openDevTesting: 'לפי מה שמסרה החברה, מגרש {p} נמצא בבדיקה אחרי הדיגום.',
      openNone: 'לאור בדיקות הקרקע לחומרי PFAS ברובע מאז פברואר 2026, אבקש מידע על מצב הקרקע במגרש{p}.', openNoneP: ' {p}', openNoneAny: ' שבו נמצאת הדירה',
      q1: 'האם המגרש נדגם לפי ההנחיות של המשרד להגנת הסביבה מ־12.2.2026? באילו תאריכים, וכמה קידוחים נעשו?',
      q2Report: 'האם הוגשה תכנית לטיפול בקרקע, והאם המשרד אישר אותה? מתי הטיפול צפוי להסתיים?',
      q2DevClear: 'אבקש לקבל את מכתב המשרד להגנת הסביבה שמאמץ את ממצאי הסקר, ואת הדו״ח עצמו.',
      q2Other: 'אבקש לקבל את דו״ח סקר הקרקע המלא של המגרש.',
      q3: 'האם המשרד להגנת הסביבה אימץ את ממצאי הסקר בכתב?',
      q4: 'האם הבדיקה או הטיפול בקרקע עלולים להשפיע על לוח הזמנים של הבנייה ועל מועד המסירה שבחוזה?',
      q5: 'מי נושא בעלות הבדיקה והטיפול בקרקע, והאם יש תרחיש שבו העלות תועבר לרוכשים?',
      q6: 'האם ניתן היתר לבנייה או לחפירה ודיפון, והאם יש בו תנאים לגבי הקרקע?',
      q7After: 'אבקש שתעדכנו אותי בכתב בכל ממצא חדש או החלטה של המשרד לגבי המגרש.',
      q7Before: 'האם תסכימו להוסיף לחוזה הצהרה שהקרקע טופלה לפי דרישות המשרד להגנת הסביבה לפני מסירת הדירה, והתחייבות לעדכן אותי בכל ממצא חדש?',
      headTo: 'לכבוד החברה היזמית', headPlot: ', מגרש {p} בשדה דב', headArea: ', רובע שדה דב',
      meAfter: 'אני רוכש/ת דירה ', meBefore: 'אני שוקל/ת לקנות דירה ', inArea: 'ברובע שדה דב', waPlot: ' (מגרש {p})',
      waHello: 'שלום, ', waThanks: '\nתודה.',
      mailHello: '\n\nשלום רב,\n', mailAsk: '\n\nאבקש תשובה בכתב לשאלות הבאות:\n', mailEnd: '\n\nאודה לתשובתכם בכתב.\nבברכה,\n[השם שלכם]\n[טלפון]'
    },
    en: {
      dmy: function (iso) { var p = String(iso || '').slice(0, 10).split('-'); return p.length === 3 ? (+p[2]) + ' ' + (MON[+p[1] - 1] || p[1]) + ' ' + p[0] : ''; },
      xs: function (x) { return (x >= 10 ? Math.round(x).toLocaleString('en-US') : (Math.round(x * 10) / 10).toString()) + ' times'; },
      openReport: 'According to the soil survey report for plot {p}, published in the Ministry of Environmental Protection database{date}, PFOS was found on the plot above the direct-contact threshold: the peak was {x} the threshold{depth}{holes}.',
      openDate: ' on {d}', openDepth: ', at a depth of {m} m', openHoles: ', in {a} of {b} boreholes',
      openFindings: 'Plot {p} is on the list of nine plots in the district where findings were reported, and its survey report has not been published in the Ministry of Environmental Protection database.',
      openDevClear: 'According to the company, the soil survey on plot {p} found no exceedances.',
      openDevTesting: 'According to the company, plot {p} is under review after sampling.',
      openNone: 'In light of the PFAS soil testing in the district since February 2026, I would like information on the state of the soil on{p}.', openNoneP: ' plot {p}', openNoneAny: ' the plot where the apartment is located',
      q1: 'Was the plot sampled under the Ministry of Environmental Protection guidelines of 12 February 2026? On which dates, and how many boreholes were drilled?',
      q2Report: 'Has a soil treatment plan been submitted, and has the Ministry approved it? When is the treatment expected to be completed?',
      q2DevClear: 'Please send me the Ministry of Environmental Protection letter adopting the survey findings, and the report itself.',
      q2Other: 'Please send me the full soil survey report for the plot.',
      q3: 'Has the Ministry of Environmental Protection adopted the survey findings in writing?',
      q4: 'Could the testing or treatment of the soil affect the construction schedule and the delivery date in the contract?',
      q5: 'Who bears the cost of testing and treating the soil, and is there any scenario in which the cost would be passed on to buyers?',
      q6: 'Has a building permit, or an excavation and shoring permit, been issued, and does it set conditions on the soil?',
      q7After: 'Please update me in writing on any new finding or any Ministry decision about the plot.',
      q7Before: 'Would you agree to add to the contract a declaration that the soil was treated to the Ministry of Environmental Protection requirements before the apartment is handed over, and an undertaking to update me on any new finding?',
      headTo: 'To the development company', headPlot: ', plot {p}, Sde Dov', headArea: ', Sde Dov district',
      meAfter: 'I have signed for an apartment ', meBefore: 'I am considering buying an apartment ', inArea: 'in the Sde Dov district', waPlot: ' (plot {p})',
      waHello: 'Hello, ', waThanks: '\nThank you.',
      mailHello: '\n\nDear Sir or Madam,\n', mailAsk: '\n\nI would be grateful for a written answer to the following questions:\n', mailEnd: '\n\nThank you for your written reply.\nKind regards,\n[Your name]\n[Phone]'
    }
  };
  function f(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  function letter(rec, plot, stage, form, lang) {
    var L = LX[lang === 'en' ? 'en' : 'he'];
    var p = plot === 'other' ? '' : plot, st = rec ? rec.status : 'none', q = [], open;
    var dd = rec && rec.report ? L.dmy(rec.report) : '';  // a partial report date ("2026-07", "2026-06/07 (...)") is left out (the live letter printed " ב־," for it)
    if (st === 'published_report') open = f(L.openReport, { p: p, date: dd ? f(L.openDate, { d: dd }) : '', x: L.xs(rec.pfosX),
      depth: rec.pfosDepth != null ? f(L.openDepth, { m: rec.pfosDepth }) : '', holes: rec.holes ? f(L.openHoles, { a: rec.pfosHoles, b: rec.holes }) : '' });
    else if (st === 'findings_reported_no_report') open = f(L.openFindings, { p: p });
    else if (st === 'developer_reported_no_exceedance') open = f(L.openDevClear, { p: p });
    else if (st === 'under_testing_per_developer') open = f(L.openDevTesting, { p: p });
    else open = f(L.openNone, { p: p ? f(L.openNoneP, { p: p }) : L.openNoneAny });
    q.push(L.q1);
    if (st === 'published_report') q.push(L.q2Report);
    else if (st === 'developer_reported_no_exceedance') q.push(L.q2DevClear);
    else q.push(L.q2Other);
    q.push(L.q3);
    q.push(L.q4);
    q.push(L.q5);
    q.push(L.q6);
    q.push(stage === 'after' ? L.q7After : L.q7Before);
    var head = L.headTo + (p ? f(L.headPlot, { p: p }) : L.headArea);
    if (form === 'wa') { var s = [0, 1, 3, 4]; return { n: s.length, text: L.waHello + (stage === 'after' ? L.meAfter : L.meBefore) + L.inArea + (p ? f(L.waPlot, { p: p }) : '') + '. '
      + open + '\n' + s.map(function (i, k) { return (k + 1) + '. ' + q[i]; }).join('\n') + L.waThanks }; }
    return { n: q.length, text: head + L.mailHello + (stage === 'after' ? L.meAfter : L.meBefore) + L.inArea + '. ' + open + L.mailAsk
      + q.map(function (x, k) { return (k + 1) + '. ' + x; }).join('\n') + L.mailEnd };
  }
  var TX = {
    times: { he: 'פי {n}', en: '{n}×' },
    kicker: { he: 'מחולל · שדה דב', en: 'Generator · Sde Dov' },
    title: { he: 'מכתב שאלות ליזם על הקרקע במגרש', en: 'A letter of soil questions for the developer' },
    lede: { he: 'בוחרים את המגרש או הפרויקט, ומקבלים מכתב מוכן ליזם, שנפתח במה שפורסם על המגרש ושואל את השאלות שנובעות מזה. מעתיקים או שולחים בוואטסאפ.',
      en: 'Choose the plot and get a ready letter for the developer. It opens with what has been published about the plot and asks the questions that follow from it. Copy it or send it on WhatsApp.' },
    fPlot: { he: 'המגרש או הפרויקט', en: 'The plot' },
    optPlot: { he: 'מגרש {p}', en: 'Plot {p}' },
    optOther: { he: 'מגרש אחר ברובע', en: 'Another plot in the district' },
    fStage: { he: 'איפה אתם עומדים', en: 'Where you stand' },
    before: { he: 'לפני חתימה', en: 'Before signing' },
    after: { he: 'כבר חתמתי', en: 'Already signed' },
    fForm: { he: 'איך שולחים', en: 'How you send it' },
    mail: { he: 'מכתב מלא', en: 'Full letter' },
    wa: { he: 'הודעת וואטסאפ קצרה', en: 'Short WhatsApp message' },
    fLang: { he: 'שפת המכתב', en: 'Letter language' },
    langEn: { he: 'אנגלית', en: 'English' },
    langHe: { he: 'עברית', en: 'Hebrew (for the developer)' },
    wNone: { he: 'לא פורסם דו״ח על המגרש', en: 'No report published on the plot' },
    wReport: { he: 'דו״ח שפורסם: {x} מעל הסף', en: 'Published report: {x} the threshold' },
    wFindings: { he: 'ברשימת המגרשים עם ממצאים, בלי דו״ח', en: 'On the list of plots with findings, no report' },
    wDevClear: { he: 'לפי היזם: בלי חריגות', en: 'Per the developer: no exceedances' },
    wDevTesting: { he: 'לפי היזם: בבדיקה', en: 'Per the developer: under review' },
    ready: { he: 'המכתב מוכן', en: 'Your letter is ready' },
    nQ: { he: '{n} שאלות', en: '{n} questions' },
    note: { he: 'המכתב לא מחליף ייעוץ משפטי. לפני חתימה, כדאי שעורך דין מקרקעין יעבור על החוזה ועל הסעיפים לגבי הקרקע: <a href="/real-estate-lawyer/">עורך דין לקניית דירה</a>. מה פורסם על כל מגרש: במפה בראש העמוד.',
      en: 'The letter is not legal advice. Before you sign, have an Israeli real estate lawyer review the contract and its clauses on the soil: <a href="/en/buy-property-in-israel/">buying property in Israel from abroad</a>. What has been published on each plot: on the map at the top of the page.' }
  };
  window.NLAX = { letter: letter, LX: LX, TX: TX };
  if (!window.NadLanInstruments) return;
  var F = window.NadLanInstruments.fmt, EN = window.NadLanInstruments.lang === 'en';
  var T = window.NadLanInstruments.pick(TX, EN ? 'en' : 'he');
  function xs(x) { return f(T.times, { n: x >= 10 ? Math.round(x).toLocaleString(EN ? 'en-US' : 'he-IL') : (Math.round(x * 10) / 10).toString() }); }
  var fields = [
    { id: 'plot', label: T.fPlot, type: 'select', options: ORDER.map(function (p) { return { value: p, label: f(T.optPlot, { p: p }) + (NAME[p] ? ' · ' + NAME[p] : '') }; }).concat([{ value: 'other', label: T.optOther }]) },
    { id: 'stage', label: T.fStage, type: 'segmented', options: [{ value: 'before', label: T.before }, { value: 'after', label: T.after }] },
    { id: 'form', label: T.fForm, type: 'segmented', options: [{ value: 'mail', label: T.mail }, { value: 'wa', label: T.wa }] }
  ];
  if (EN) fields.push({ id: 'lang', label: T.fLang, type: 'segmented', options: [{ value: 'en', label: T.langEn }, { value: 'he', label: T.langHe }] });
  window.NadLanInstruments.register('soilask', {
    kicker: T.kicker,
    title: T.title,
    lede: T.lede,
    defaults: function () { return EN ? { plot: '2206', stage: 'before', form: 'mail', lang: 'en' } : { plot: '2206', stage: 'before', form: 'mail' }; },
    fields: fields,
    compute: function (v, data) {
      var d = data.soil, rec = null;
      d.records.forEach(function (r) { if (r.plot === v.plot) rec = r; });
      var ll = EN ? v.lang : 'he';
      var L = letter(rec, v.plot, v.stage, v.form, ll);
      var what = !rec ? T.wNone : rec.status === 'published_report' ? f(T.wReport, { x: xs(rec.pfosX) })
        : rec.status === 'findings_reported_no_report' ? T.wFindings : rec.status === 'developer_reported_no_exceedance' ? T.wDevClear : T.wDevTesting;
      var r = {
        answer: { label: T.ready, value: f(T.nQ, { n: F.num(L.n) }), tone: 'ink', sub: (v.plot === 'other' ? T.optOther : f(T.optPlot, { p: v.plot })) + ' · ' + what },
        doc: L.text, text: L.text, bare: true,
        note: T.note
      };
      if (EN && ll === 'he') { r.docDir = 'rtl'; r.docLang = 'he'; }  // a Hebrew letter inside the English page reads right to left
      return r;
    }
  });
})();
