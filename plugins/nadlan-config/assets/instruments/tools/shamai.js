/* NadLan Instruments · shamai family v1 (G7 moat, HAD-601 round 2, 26.10.2026): "שמאי מקרקעין" on /real-estate-appraiser/.
   One file, two tools (registry 'file' => 'shamai'):
   - shamai     · need: which appraisal the reader needs (bank, before signing, sale, betterment levy, section 197, court, urban renewal,
                  rent): who orders, who pays, what the law fixes, the deadline from the reader's own date (45 days from the levy
                  notice, Third Schedule s.14; 3 years from a plan's entry into force, s.197), the published price range, and the
                  page on the site that owns the subject.
                · fee: the published price ranges by appraisal type (Midrag 7.2024, EC 8.2025, d.co.il 9.2026; VAT not stated by any of
                  them), and the decisive appraiser's fee by the official regulation (3% / 2% / 1% / 0.5% by brackets, at least 2,000
                  and at most 100,000 per dispute, plus VAT, half for each side, a quarter on appointment).
   - shamaireg  · a live search of the Ministry of Justice register of licensed real-estate appraisers on data.gov.il (CKAN datastore
                  API, CORS open): by name (prefix words) or licence number. Nothing of the register is copied to our site; the reader's
                  browser asks the official API at the moment of the search.
   Data: data/shamai.json (tools/instruments/build_pros_data.py). Pure logic in NLSH for unit checks. */
(function () {
  'use strict';
  function n0(x) { return String(Math.round(x || 0)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function ils(x) { return '₪' + n0(x); }
  function dd(iso) { var p = String(iso).split('-'); return (+p[2]) + '.' + (+p[1]) + '.' + p[0]; }
  function addD(iso, n) { var p = iso.split('-').map(Number); return new Date(Date.UTC(p[0], p[1] - 1, p[2] + n)).toISOString().slice(0, 10); }
  function addY(iso, y) { var p = iso.split('-').map(Number); var d = new Date(Date.UTC(p[0] + y, p[1] - 1, p[2])); if (d.getUTCMonth() !== p[1] - 1) d = new Date(Date.UTC(p[0] + y, p[1], 0)); return d.toISOString().slice(0, 10); }
  function days(a, b) { return Math.round((Date.parse(b) - Date.parse(a)) / 864e5); }

  /** The decisive appraiser's fee (regulation 2 and the table): marginal brackets on the amount in the request, clamped. */
  function decisiveFee(amount, T) {
    var fee = 0;
    T.table.forEach(function (b) { var lo = b[0], hi = b[1] || Infinity; if (amount > lo) fee += (Math.min(amount, hi) - lo) * b[2]; });
    var raw = fee; fee = Math.max(T.min, Math.min(T.max, fee));
    return { raw: raw, fee: fee, clamped: fee !== raw, half: fee * T.split, upfront: fee * T.upfront };
  }
  function deadline(p, date) { if (!p.deadline || !/^\d{4}-\d{2}-\d{2}$/.test(date || '')) return null; return p.deadline.days ? addD(date, p.deadline.days) : addY(date, p.deadline.years); }
  function priceFor(S, keys) {
    var rows = [];
    S.prices.forEach(function (s) { s.rows.forEach(function (r) { if (keys.indexOf(r[0]) > -1) rows.push({ src: s.src, date: s.date, vat: s.vat, key: r[0], label: r[1], lo: r[2], hi: r[3] }); }); });
    return { rows: rows, lo: rows.length ? Math.min.apply(null, rows.map(function (r) { return r.lo; })) : 0, hi: rows.length ? Math.max.apply(null, rows.map(function (r) { return r.hi; })) : 0 };
  }
  /** The query for the official register: licence number -> exact filter; words -> prefix full-text (tsquery). */
  function regQuery(q) {
    var s = String(q || '').replace(/[^֐-׿A-Za-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
    if (!s) return null;
    if (/^\d{2,8}$/.test(s)) return { filters: JSON.stringify({ 'מספר רשיון': +s }) };
    var words = s.split(' ').filter(function (w) { return w.length >= 2 && !/^\d+$/.test(w); }).slice(0, 4);
    if (!words.length) return null;
    return { q: words.map(function (w) { return w + ':*'; }).join(' & '), plain: 'false' };
  }

  window.NLSH = { decisiveFee: decisiveFee, deadline: deadline, priceFor: priceFor, regQuery: regQuery, addD: addD, addY: addY };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  function today() { return new Date().toISOString().slice(0, 10); }
  function src(D, keys) { return keys.filter(function (k, i, a) { return a.indexOf(k) === i; }).map(function (k) { return D.sources[k]; }).filter(Boolean); }
  function srcName(D, k) { return D.sources[k].label.split(' (')[0].split(',')[0]; }

  function svgBrackets(amount, r, T) {
    var XR = 400, XL = 20, y0 = 60, g = [], top = Math.max(amount, 2500000);
    var x = function (v) { return XR - (XR - XL) * Math.min(1, v / top); };
    g.push('<text x="410" y="22" text-anchor="start" style="font-size:16px;font-weight:600;fill:#12202A">' + esc('שכר השמאי המכריע לפי המדרגות שבתקנות') + '</text>');
    var cols = ['#1F4B5C', '#2F6F86', '#5E8FA1', '#9DBAC5'];
    T.table.forEach(function (b, i) { var lo = b[0], hi = b[1] || top; if (lo >= top) return; var w = x(lo) - x(Math.min(hi, top)); g.push('<rect x="' + x(Math.min(hi, top)) + '" y="' + (y0 - 12) + '" width="' + w + '" height="24" fill="' + cols[i] + '"/>'); if (w > 26) g.push('<text x="' + ((x(lo) + x(Math.min(hi, top))) / 2) + '" y="' + (y0 + 5) + '" text-anchor="middle" style="font-size:13px;fill:#fff;font-weight:600">' + (b[2] * 100) + '%</text>'); });
    var ax = x(amount), al = ils(amount), aw = al.length * 8; g.push('<line x1="' + ax + '" y1="' + (y0 - 24) + '" x2="' + ax + '" y2="' + (y0 + 24) + '" stroke="#C42550" stroke-width="2.4"/>');
    g.push('<text x="' + Math.max(aw / 2 + 4, Math.min(ax, 414 - aw / 2)) + '" y="' + (y0 + 42) + '" text-anchor="middle" style="font-size:13px;fill:#C42550;font-weight:600">' + esc(al) + '</text>');
    g.push('<text x="410" y="' + (y0 + 66) + '" text-anchor="start" style="font-size:12px;fill:#3E4C58">' + esc('המדרגות: עד 500 אלף, עד מיליון, עד 2 מיליון ומעל.') + '</text>');
    g.push('<text x="410" y="' + (y0 + 84) + '" text-anchor="start" style="font-size:12px;fill:#3E4C58">' + esc('השכר: ' + ils(r.fee) + ' ועוד מע״מ') + '</text>');
    return '<svg direction="rtl" viewBox="0 0 420 ' + (y0 + 96) + '" role="img" aria-label="' + esc('שכר שמאי מכריע על ' + ils(amount) + ': ' + ils(r.fee) + ' ועוד מע״מ') + '" style="display:block;width:100%;height:auto;background:#fff">' + g.join('') + '</svg>';
  }

  function viewNeed(v, D) {
    var p = D.purposes.filter(function (x) { return x.id === v.purpose; })[0] || D.purposes[0], lines = [], notes = [];
    var dl = deadline(p, p.deadline && p.deadline.from === 'plan_date' ? v.plan_date : v.levy_date), pr = p.price ? priceFor(D, p.price) : null;
    var asof = today(), answer;
    if (p.deadline) {
      if (!dl) return { error: { field: p.deadline.from, msg: p.deadline.from === 'plan_date' ? 'בחרו את היום שבו התכנית נכנסה לתוקף.' : 'בחרו את היום שבו קיבלתם את דרישת ההיטל.' } };
      var left = days(asof, dl);
      answer = { label: p.label + ': המועד האחרון', value: dd(dl), tone: left < 15 ? 'survey' : 'ink', sub: esc((left >= 0 ? 'נשארו ' + F.num(left) + ' ימים. ' : 'המועד עבר; יושב ראש ועדת הערר או יושב ראש מועצת השמאים רשאים להאריך מטעמים מיוחדים. ') + p.law) };
    } else if (pr && pr.rows.length) answer = { label: p.label + ', בשקלים', value: n0(pr.lo) + '-' + n0(pr.hi), sub: esc('הטווח שפורסם לשומה כזו (מע״מ לא צוין). ' + p.law) };
    else answer = { label: p.label, value: p.id === 'bank' ? 'לפי תעריף הבנק' : p.id === 'renewal' ? 'משלם היזם' : 'לפי ההסכם', sub: esc(p.law) };
    lines.push({ label: 'מי מזמין', value: p.who_s });
    lines.push({ label: 'מי משלם', value: p.pay_s });
    notes.push(esc('מי מזמין: ' + p.who + '. מי משלם: ' + p.pay + '.'));
    if (p.id === 'levy') { lines.push({ label: 'ערר לוועדת הערר או בקשה למינוי שמאי מכריע', value: '45 ימים' }); lines.push({ label: 'יושב ראש מועצת השמאים מודיע מי השמאי המכריע', value: 'בתוך 15 ימים' }); lines.push({ label: 'חיוב עד 90,000 ₪: בחינה חוזרת אצל שמאי הוועדה', value: 'החלטה בתוך 14 ימים' }); lines.push({ label: 'שכר השמאי המכריע', value: 'לפי התקנות, חצי לכל צד' }); }
    if (p.id === 's197') lines.push({ label: 'הגשת תביעה לוועדה המקומית', value: '3 שנים מתחילת תוקף התכנית' });
    if (pr) pr.rows.forEach(function (r) { lines.push({ label: srcName(D, r.src) + ' ' + r.date.slice(0, 4) + ': ' + r.label, value: r.lo === r.hi ? ils(r.lo) : ils(r.lo) + ' עד ' + ils(r.hi) }); });
    if (p.link) notes.push('לעמוד שמרחיב על הנושא: <a href="' + esc(p.link[0]) + '">' + esc(p.link[1]) + '</a>.');
    notes.push(esc('לפני שמזמינים: בדקו שהשמאי רשום בפנקס שמאי המקרקעין (החיפוש בהמשך העמוד). חברות בלשכת השמאים אינה רישיון; הרישיון הוא הרישום בפנקס.'));
    var table = { title: 'כל סוגי השומה: מי מזמין, מי משלם ומה המועד', head: ['מטרה', 'מי מזמין', 'מי משלם', 'מועד בחוק'],
      rows: D.purposes.map(function (x) { return [x.label, x.who, x.pay, x.deadline ? (x.deadline.days ? x.deadline.days + ' ימים' : x.deadline.years + ' שנים') : 'אין']; }) };
    return { answer: answer, lines: lines, note: notes.join('<br>'), table: table,
      formula: p.id === 'levy' ? 'התוספת השלישית לחוק התכנון והבניה, סעיף 14: ערר או פנייה לשמאי מכריע בתוך 45 ימים מיום שהשומה הובאה לידיעת החייב; על לוח שומה בתוך שנה מהצגתו.' : p.id === 's197' ? 'סעיף 197(ב) לחוק התכנון והבניה: התביעה לפיצויים מוגשת לוועדה המקומית תוך שלוש שנים מיום תחילת תוקפה של התכנית; שר הפנים רשאי להאריך.' : 'חוק שמאי מקרקעין: שמאי מקרקעין הוא מי שרשום בפנקס; שומה לבית משפט רק בידי שמאי רשום; שומה בשכר רק בידי שמאי רשום.',
      sources: src(D, p.src.concat(pr ? pr.rows.map(function (r) { return r.src; }) : [])), text: 'שמאי מקרקעין, ' + p.label + ': ' + (dl ? 'המועד האחרון ' + dd(dl) + '. ' : '') + 'מי מזמין: ' + p.who + '. מי משלם: ' + p.pay + '.' };
  }

  var FEEK = { apt: 'דירה בבניין', apt_big: 'דירה גדולה או פנטהאוז', house: 'בית פרטי', invest: 'דירה להשקעה או ייחודית', shop: 'נכס מסחרי קטן', rent: 'קביעת דמי שכירות', inherit: 'ירושה או חלוקת עיזבון', plot: 'מגרש לבית פרטי', court_add: 'חוות דעת לבית משפט (תוספת)', levy: 'שומה נגדית להיטל השבחה', decisive: 'שמאי מכריע לפי התקנות' };
  function viewFee(v, D) {
    var kind = v.fkind, lines = [], notes = [];
    if (kind === 'decisive') {
      var amt = +v.amount; if (!(amt >= 1000 && amt <= 1e9)) return { error: { field: 'amount', msg: 'סכום ההשבחה או התביעה שבבקשה, בשקלים.' } };
      var r = decisiveFee(amt, D.decisive), vat = D.vat;
      lines.push({ label: 'השכר לפי המדרגות', value: ils(r.raw) });
      if (r.clamped) lines.push({ label: r.raw < D.decisive.min ? 'מינימום לפי התקנות' : 'תקרה לפי התקנות', value: ils(r.fee) });
      lines.push({ label: 'שכר השמאי המכריע ועוד מע״מ 18%', value: ils(r.fee * (1 + vat)) });
      lines.push({ label: 'החלק שלכם (מחצית), כולל מע״מ', value: ils(r.half * (1 + vat)) });
      lines.push({ label: 'רבע מהשכר שמותר לדרוש מיד עם המינוי, כולל מע״מ', value: ils(r.upfront * (1 + vat)) });
      notes.push(esc('המבקש והוועדה המקומית נושאים כל אחד במחצית השכר. השמאי המכריע רשאי להטיל את כל השכר על צד אחד, למשל כשהתוצאה מובהקת לטובת צד או כשהבקשה קנטרנית, וגם להתחשב במי שמתקשה לשלם (תקנה 5). היושב ראש רשאי לקבוע שכר חריג בנסיבות מיוחדות (תקנה 3).'));
      notes.push('על המונח עצמו: <a href="/glossary/%D7%A9%D7%9E%D7%90%D7%99-%D7%9E%D7%9B%D7%A8%D7%99%D7%A2/">שמאי מכריע</a>.');
      var t = D.decisive.table;
      return { answer: { label: 'שכר שמאי מכריע על ' + ils(amt) + ', לפני מע״מ', value: n0(r.fee) + ' ₪', sub: esc('ועוד מע״מ. החלק שלכם: ' + ils(r.half * (1 + vat)) + ' כולל מע״מ. לפי תקנות התכנון והבניה (שכרו של שמאי מכריע ושמאי מייעץ).') },
        figure: svgBrackets(amt, r, D.decisive), lines: lines, note: notes.join('<br>'),
        table: { title: 'מדרגות השכר שבתקנות', head: ['על החלק שמעל', 'ועד', 'שיעור'], num: [0, 1, 2], rows: t.map(function (b) { return [b[0] ? ils(b[0]) : 'מהשקל הראשון', b[1] ? ils(b[1]) : 'ומעלה', (b[2] * 100) + '%']; }).concat([['מינימום לכל מחלוקת', '', ils(D.decisive.min)], ['תקרה לכל מחלוקת', '', ils(D.decisive.max)]]) },
        formula: '3% עד 500,000 ₪, 2% על החלק שעד מיליון, 1% על החלק שעד 2 מיליון ו-0.5% על היתרה; לא פחות מ-2,000 ₪ ולא יותר מ-100,000 ₪ למחלוקת; ועוד מע״מ.', sources: src(D, ['DFEE', 'DEC']),
        text: 'שכר שמאי מכריע על ' + ils(amt) + ': ' + ils(r.fee) + ' ועוד מע״מ; החלק שלכם ' + ils(r.half * (1 + vat)) + ' כולל מע״מ.' };
    }
    var keys = kind === 'apt' ? ['apt'] : [kind];
    var pr = priceFor(D, keys); if (!pr.rows.length) return { error: { field: 'fkind', msg: 'אין מחיר שפורסם לסוג הזה.' } };
    pr.rows.forEach(function (r) { lines.push({ label: srcName(D, r.src) + ' ' + r.date.slice(0, 7).split('-').reverse().join('.') + ': ' + r.label, value: r.lo === r.hi ? ils(r.lo) : ils(r.lo) + ' עד ' + ils(r.hi) }); });
    var red = +v.reduction || 0;
    if (kind === 'levy' && red > 0) { var a = pr.rows[0]; lines.push({ label: 'עם 10% מהפחתה של ' + ils(red), value: ils(a.lo + 0.1 * red) + ' עד ' + ils(a.hi + 0.1 * red) }); }
    if (kind === 'court_add') notes.push(esc('זו תוספת על מחיר השומה הרגילה: למשל שומה של 2,500 ₪ לבית תעלה בגרסה לבית משפט 4,000 עד 4,500 ₪ (מידרג).'));
    notes.push(esc('אף אחד מהמקורות לא כתב אם המחיר כולל מע״מ; שאלו. המחיר תלוי בזמן העבודה: נכס עם חריגות בנייה, זכויות לא מנוצלות או כמה בעלים לוקח יותר זמן. שומה שהבנק לא הזמין לא תחליף את שמאי הבנק.'));
    var t2 = { title: 'כל המחירים שפורסמו לסוג הזה', head: ['מקור', 'מה כלול', 'מחיר', 'פורסם'], num: [2], rows: pr.rows.map(function (r) { return [srcName(D, r.src), r.label, r.lo === r.hi ? n0(r.lo) + ' ₪' : n0(r.lo) + ' עד ' + n0(r.hi) + ' ₪', dd(r.date)]; }) };
    return { answer: { label: 'שמאי מקרקעין: ' + FEEK[kind] + ', בשקלים', value: n0(pr.lo) + '-' + n0(pr.hi), sub: esc('הנמוך והגבוה מבין ' + pr.rows.length + ' מחירים שפורסמו (2024 עד 2026). טווח שפורסם, לא הצעת מחיר.') },
      lines: lines, note: notes.join('<br>'), table: t2, formula: 'הטווח: המחיר הנמוך והגבוה שפרסמו מידרג (7.2024), EC שמאות (8.2025) ודפי זהב (נתוני 9.2026) לאותו סוג שומה, כפי שפורסמו.',
      sources: src(D, pr.rows.map(function (r) { return r.src; })), text: 'שמאי מקרקעין, ' + FEEK[kind] + ': ' + ils(pr.lo) + ' עד ' + ils(pr.hi) + ' לפי מחירים שפורסמו.' };
  }

  NI.register('shamai', {
    kicker: 'מחשבון · שמאי מקרקעין',
    title: 'איזה שמאי אתם צריכים, מי משלם, מה המועד וכמה זה עולה',
    lede: 'בוחרים את המטרה: משכנתא, לפני חתימה, היטל השבחה, תכנית שפגעה בשווי, ירושה או התחדשות עירונית. רואים מי מזמין את השמאי ומי משלם, את המועד שהחוק נותן מהתאריך שלכם, ואת המחירים שפורסמו. לשמאי מכריע: השכר המדויק לפי התקנות והחלק שלכם.',
    strip: function (data) { var S = data.shamai; return [{ label: 'שמאים מורשים בפנקס', value: F.num(S.register.count) }, { label: 'ערר על היטל השבחה', value: '45 ימים' }, { label: 'תביעה לפי סעיף 197', value: '3 שנים' }, { label: 'ציון עובר בבחינות', value: String(S.exams.pass) }]; },
    presets: function () {
      return [{ key: 'levy', label: 'קיבלתי דרישת היטל השבחה', sub: 'עד מתי לערער', set: { view: 'need', purpose: 'levy', levy_date: addD(today(), -10) } },
        { key: 'bank', label: 'משכנתא: השמאי של הבנק', sub: 'מי בוחר ומי משלם', set: { view: 'need', purpose: 'bank' } },
        { key: 'buy', label: 'לפני חתימה על חוזה', sub: 'שומה פרטית', set: { view: 'need', purpose: 'buy' } },
        { key: 'dec', label: 'שמאי מכריע על השבחה של 800 אלף', sub: 'השכר לפי התקנות', set: { view: 'fee', fkind: 'decisive', amount: 800000 } },
        { key: 'house', label: 'כמה עולה שמאי לבית פרטי', sub: 'כל המחירים שפורסמו', set: { view: 'fee', fkind: 'house' } }];
    },
    defaults: function () { return { view: 'need', purpose: 'levy', levy_date: addD(today(), -10), plan_date: '2024-03-01', fkind: 'apt', amount: 800000, reduction: 0 }; },
    fields: [
      { id: 'view', label: 'מה לבדוק', type: 'segmented', options: [{ value: 'need', label: 'איזו שומה צריך' }, { value: 'fee', label: 'כמה זה עולה' }] },
      { id: 'purpose', label: 'המטרה', type: 'select', showIf: function (v) { return v.view === 'need'; }, optionsFrom: function (v, data) { return data.shamai.purposes.map(function (p) { return { value: p.id, label: p.label }; }); } },
      { id: 'levy_date', label: 'היום שבו קיבלתם את דרישת ההיטל', type: 'date', showIf: function (v) { return v.view === 'need' && v.purpose === 'levy'; } },
      { id: 'plan_date', label: 'היום שבו התכנית נכנסה לתוקף', type: 'date', showIf: function (v) { return v.view === 'need' && v.purpose === 's197'; } },
      { id: 'fkind', label: 'סוג השומה', type: 'select', showIf: function (v) { return v.view === 'fee'; }, options: Object.keys(FEEK).map(function (k) { return { value: k, label: FEEK[k] }; }) },
      { id: 'amount', label: 'סכום ההשבחה או התביעה שבבקשה', type: 'money', unit: '₪', showIf: function (v) { return v.view === 'fee' && v.fkind === 'decisive'; } },
      { id: 'reduction', label: 'ההפחתה בהיטל שהשמאי השיג (לא חובה)', type: 'money', unit: '₪', showIf: function (v) { return v.view === 'fee' && v.fkind === 'levy'; } }
    ],
    compute: function (v, data) { var D = data.shamai; if (!D || !D.purposes) return { error: { field: null, msg: 'הנתונים לא נטענו.' } }; return v.view === 'fee' ? viewFee(v, D) : viewNeed(v, D); }
  });

  // ------------------------------------------------------------------ shamaireg: the official register, searched live
  NI.register('shamaireg', {
    custom: function (root, data) {
      var S = data.shamai, R = S.register;
      root.innerHTML = ''; root.setAttribute('dir', 'rtl'); if (!root.parentNode || !root.parentNode.closest || !root.parentNode.closest('.nli')) root.classList.add('nli');
      var panel = document.createElement('div'); panel.className = 'nli__panel';
      panel.innerHTML = '<p class="nli__kicker">חיפוש · פנקס שמאי המקרקעין</p><h2 class="nli__title">האם השמאי רשום בפנקס? חיפוש לפי שם או מספר רישיון</h2>' +
        '<p class="nli__lede">החיפוש רץ ישירות מול מאגר שמאי המקרקעין של משרד המשפטים באתר data.gov.il, ברגע שאתם מחפשים. במאגר ' + F.num(R.count) + ' שמאים מורשים (עודכן ' + dd(R.updated) + '). שמאי מקרקעין, לפי החוק, הוא מי שרשום בפנקס.</p>' +
        '<div class="nli__grid"><form class="nli__form" role="search"><div class="nli__f"><label for="nlshr-q">שם השמאי או מספר הרישיון</label><div class="nli__in"><input id="nlshr-q" type="text" autocomplete="off" placeholder="למשל: כהן רמי, או 1096"></div><span class="nli__help">אפשר לכתוב תחילת שם, שם משפחה ושם פרטי, או מספר רישיון.</span></div><div class="nli__share" style="margin:6px 0 0"><button type="submit" class="is-primary"><span>חיפוש בפנקס</span></button></div></form>' +
        '<div class="nli__out" aria-live="polite"><div class="nli__answer"><span class="nli__alab">שמאים מורשים במאגר הרשמי</span><output class="nli__fig">' + F.num(R.count) + '</output><span class="nli__asub">' + esc('מתוכם ' + F.num(R.with_city) + ' עם עיר רשומה. המאגר מתעדכן כל שלושה חודשים.') + '</span></div></div></div>' +
        '<p class="nli__src">מקור: <a href="' + esc(R.page) + '" target="_blank" rel="noopener">מאגר שמאי מקרקעין, משרד המשפטים</a>. לא שמרנו את הרשימה אצלנו; כל חיפוש נשלח למאגר הרשמי.</p>';
      root.appendChild(panel);
      var form = panel.querySelector('form'), inp = panel.querySelector('input'), out = panel.querySelector('.nli__out'), seq = 0;
      function show(html) { out.innerHTML = html; }
      form.addEventListener('submit', function (e) {
        e.preventDefault(); var q = window.NLSH.regQuery(inp.value);
        if (!q) { show('<p class="nli__note">כתבו לפחות שתי אותיות של שם, או מספר רישיון.</p>'); return; }
        var my = ++seq, u = R.api + '?resource_id=' + encodeURIComponent(R.resource) + '&limit=25' + Object.keys(q).map(function (k) { return '&' + k + '=' + encodeURIComponent(q[k]); }).join('');
        show('<p class="nli__note">מחפשים במאגר הרשמי…</p>');
        fetch(u, { credentials: 'omit' }).then(function (r) { return r.json(); }).then(function (j) {
          if (my !== seq) return;
          if (!j || !j.success) throw new Error('api');
          var recs = j.result.records || [], tot = j.result.total || 0;
          if (!recs.length) { show('<div class="nli__answer"><span class="nli__alab">תוצאות במאגר הרשמי</span><output class="nli__fig is-survey">לא נמצא</output><span class="nli__asub">' + esc('לא מצאנו שמאי בשם או במספר הזה. בדקו את האיות, נסו שם משפחה בלבד, או בקשו מהשמאי את מספר הרישיון.') + '</span></div>'); return; }
          show('<div class="nli__answer"><span class="nli__alab">נמצאו במאגר הרשמי</span><output class="nli__fig">' + F.num(tot) + '</output><span class="nli__asub">' + esc(tot > recs.length ? 'מוצגים ' + recs.length + ' הראשונים; צמצמו לפי שם פרטי.' : 'כל התוצאות מוצגות.') + '</span></div>' +
            '<div class="nli__tw"><table><thead><tr><th scope="col">שם</th><th scope="col">מספר רישיון</th><th scope="col">עיר</th></tr></thead><tbody>' +
            recs.map(function (x) { return '<tr><td>' + esc(x['שם שמאי']) + '</td><td class="n">' + esc(x['מספר רשיון']) + '</td><td>' + esc(x['עיר'] || 'לא צוינה') + '</td></tr>'; }).join('') + '</tbody></table></div>' +
            '<p class="nli__note">' + esc('רישום בפנקס הוא התנאי לעסוק בשומה בשכר. הוא לא אומר באיזה תחום השמאי מתמחה: שאלו על שומות דומות שעשה.') + '</p>');
        }).catch(function () { if (my !== seq) return; show('<p class="nli__note">' + esc('המאגר הרשמי לא ענה כרגע. אפשר לחפש ישירות באתר data.gov.il, בקישור שלמטה.') + '</p>'); });
      });
    }
  });
})();
