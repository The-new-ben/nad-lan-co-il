/* NadLan Instruments · orechdin v1 (G8 moat, HAD-601 round 2, 26.10.2026): "עורך דין מקרקעין" on /real-estate-lawyer/.
   Two views on one set of answers:
   - fee   · כמה עולה עורך דין: the fee level published by law offices in 2026 (about 0.5% plus VAT; 0.5% to 1%; a minimum of about
             5,000 to 6,000), next to the Bar Association's recommended minimum tariff for 2026 (non-binding, s.2 of the rules), the
             legal cap on what a developer may charge the buyer for its lawyer (the lower of 5,915 ₪ and 0.5% of the price, before
             VAT, up to a price of 4,642,750 ₪; plus the price-control list fee), and the Land Registry fees of 2026, with VAT.
   - steps · צעדי העסקה: the steps of the deal type from the first check to registration, who does each and the documents, with
             the dates the law fixes from the signing day (declaration in 30 days and purchase tax in 60, from ptax.json; the capital
             gains advance of 7.5% or 15% after more than 40% of the price, Land Taxation Law s.15).
   Data: data/orechdin.json (tools/instruments/build_pros_data.py) + data/ptax.json (read only). Pure logic in NLOD for unit checks.
   Honesty: general information, not legal advice; ranges labelled as published; the site does not represent anyone. */
(function () {
  'use strict';
  function n0(x) { return String(Math.round(x || 0)).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function ils(x) { return '₪' + n0(x); }
  function dd(iso) { var p = String(iso).split('-'); return (+p[2]) + '.' + (+p[1]) + '.' + p[0]; }
  function addD(iso, n) { var p = iso.split('-').map(Number); return new Date(Date.UTC(p[0], p[1] - 1, p[2] + n)).toISOString().slice(0, 10); }

  /** The Bar Association's recommended minimum for drafting a contract on `value` (2026 amounts; non-binding). */
  function tariff(value, T) {
    if (value > T.top) return { fee: T.top_min, open: true };
    var fee = 0; T.tiers.forEach(function (t) { if (value > t[0]) fee += (Math.min(value, t[1]) - t[0]) * t[2]; });
    return { fee: Math.max(T.min, fee), open: false };
  }
  /** What a developer may charge the buyer for its lawyer (Sale Law s.6ג + the 2014 regulations, 2026 amount), before VAT. */
  function devCap(price, C) {
    if (price > C.ceiling) return { capped: false, max: null };
    return { capped: true, max: Math.min(C.fixed, price * C.pct), by: price * C.pct < C.fixed ? 'pct' : 'fixed' };
  }
  /** The fee level published by law offices: 0.5% to 1% of the price, with the published minimum. */
  function market(price, M) {
    var minLo = 5000, minHi = 6000;
    return { lo: Math.max(price * 0.005, minLo), hi: Math.max(price * 0.01, minHi), mid: Math.max(price * 0.005, minLo) };
  }
  function landFees(L, mortgage) {
    var f = {}; L.forEach(function (r) { f[r[0]] = r[2]; });
    var rows = [['הערת אזהרה לטובתכם', f.warn], ['רישום המכר (העברת הבעלות)', f.sale]];
    if (mortgage) { rows.push(['הערת אזהרה לטובת הבנק', f.warn]); rows.push(['רישום משכנתה', f.mortgage]); }
    return { rows: rows, total: rows.reduce(function (s, r) { return s + r[1]; }, 0), f: f };
  }
  function dates(sign, P) { return { declare: addD(sign, P.declare_days), pay: addD(sign, P.pay_days) }; }

  window.NLOD = { tariff: tariff, devCap: devCap, market: market, landFees: landFees, dates: dates };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  function today() { return new Date().toISOString().slice(0, 10); }
  function src(D, keys) { return keys.filter(function (k, i, a) { return a.indexOf(k) === i; }).map(function (k) { return D.sources[k]; }).filter(Boolean); }

  function svgCompare(bars, price) {
    var XR = 400, XL = 24, top = 46, rh = 44, H = top + bars.length * rh + 26, g = [], max = Math.max.apply(null, bars.map(function (b) { return b.hi || b.v; })) * 1.12 || 1;
    var x = function (v) { return XR - (XR - XL) * v / max; };
    g.push('<text x="410" y="22" text-anchor="start" style="font-size:16px;font-weight:600;fill:#12202A">' + esc('עורך דין בעסקה של ' + ils(price) + ', לפני מע״מ') + '</text>');
    bars.forEach(function (b, i) {
      var y = top + i * rh;
      g.push('<text x="410" y="' + (y + 12) + '" text-anchor="start" style="font-size:12.5px;fill:#3E4C58">' + esc(b.name) + '</text>');
      if (b.hi && b.hi > b.v) g.push('<rect x="' + x(b.hi) + '" y="' + (y + 18) + '" width="' + (XR - x(b.hi)) + '" height="12" fill="' + b.col + '" fill-opacity=".35"/>');
      g.push('<rect x="' + x(b.v) + '" y="' + (y + 18) + '" width="' + (XR - x(b.v)) + '" height="12" fill="' + b.col + '"/>');
      var lab = b.label || (b.hi && b.hi > b.v ? n0(b.v) + '-' + n0(b.hi) : n0(b.v)), lw = lab.length * 7.6, ex = x(b.hi || b.v);
      if (ex - 6 - lw >= 4) g.push('<text x="' + (ex - 6) + '" y="' + (y + 29) + '" text-anchor="start" style="font-size:12.5px;fill:#12202A;font-family:IBM Plex Mono,monospace">' + esc(lab) + '</text>');
      else g.push('<text x="' + (x(b.v) + 6) + '" y="' + (y + 29) + '" text-anchor="end" style="font-size:12.5px;fill:#fff;font-weight:600;font-family:IBM Plex Mono,monospace">' + esc(lab) + '</text>');
    });
    g.push('<text x="410" y="' + (H - 6) + '" text-anchor="start" style="font-size:12px;fill:#3E4C58">' + esc('בשקלים. האדום: מה שמותר לקבלן לגבות מכם על עורך הדין שלו') + '</text>');
    return '<svg direction="rtl" viewBox="0 0 420 ' + H + '" role="img" aria-label="' + esc('השוואת שכר טרחה לעסקה של ' + ils(price)) + '" style="display:block;width:100%;height:auto;background:#fff">' + g.join('') + '</svg>';
  }

  var DEAL = {};
  function viewFee(v, D, P) {
    var price = +v.price, deal = v.deal, vat = D.vat, lines = [], notes = [], bars = [];
    if (!(price >= 100000 && price <= 100000000)) return { error: { field: 'price', msg: 'מחיר העסקה, בשקלים.' } };
    var m = market(price, D.market), t = tariff(price, D.tariff), cap = devCap(price, D.cap), lf = landFees(D.land, v.mortgage === 'yes');
    var answer;
    if (deal === 'new') {
      var own = v.own === 'yes';
      answer = { label: 'דירה מקבלן: מה מותר לקבלן לגבות על עורך הדין שלו', value: cap.capped ? 'עד ' + n0(cap.max) + ' ₪' : 'ללא תקרה', tone: cap.capped ? 'ink' : 'survey',
        sub: esc(cap.capped ? 'ועוד מע״מ. זה הסכום המרבי שמותר לקבלן לדרוש מכם על עורך הדין שלו, ' + (cap.by === 'pct' ? '0.5% מהמחיר' : 'הסכום הקבוע לשנת 2026') + ', ועוד עד 300 ₪ לניהול רשימת הזכויות. משלמים ישירות לעורך הדין ומקבלים חשבונית.' : 'במחיר מעל 4,642,750 ₪ התקנות לא מגבילות את הסכום. בדקו את הסעיף בחוזה לפני החתימה.') };
      lines.push({ label: 'התקרה לשנת 2026 (מתעדכנת לפי המדד בכל ינואר)', value: ils(D.cap.fixed) + ' או 0.5%, הנמוך' });
      if (cap.capped) lines.push({ label: 'המרבי לעסקה הזאת, כולל מע״מ 18%', value: ils(cap.max * (1 + vat)) });
      lines.push({ label: 'ניהול רשימת בעלי הזכויות עד הרישום, לפי צו הפיקוח', value: 'עד ' + ils(D.cap.list_fee) });
      lines.push({ label: 'התעריף המומלץ של הלשכה לעורך הדין של הקבלן (המלצה)', value: '1% מהמחיר: ' + ils(price * D.tariff.dev_lawyer) });
      lines.push({ label: 'התעריף המומלץ לעורך הדין שלכם על בדיקת החוזה והרישום', value: '0.25%: ' + ils(price * D.tariff.buyer_check_new) });
      if (own) lines.push({ label: 'עורך דין משלכם, לפי מה שפורסם במשרדים', value: ils(m.lo) + ' עד ' + ils(m.hi) + ' ועוד מע״מ' });
      bars.push(cap.capped ? { name: 'התקרה שבחוק: הקבלן מכם', v: cap.max, col: '#C42550' } : { name: 'התקרה שבחוק: מעל 4,642,750 ₪ אין', v: 0.0001, label: 'ללא תקרה', col: '#C42550' }); bars.push({ name: 'הלשכה ממליצה לעורך הדין שלכם: 0.25%', v: price * D.tariff.buyer_check_new, col: '#2F6F86' });
      if (own) bars.push({ name: 'עורך דין משלכם, כפי שפורסם', v: m.lo, hi: m.hi, col: '#1F4B5C' });
      notes.push(esc('עורך הדין של הקבלן מייצג את הקבלן. הוא מטפל גם ברישום שלכם, אבל אינו רשאי לייעץ לכם בנפרד. במשא ומתן על החוזה אתם רשאים לשכור עורך דין משלכם ולשלם לו בנפרד (סעיף 6ג לחוק המכר (דירות)).'));
    } else {
      answer = { label: (DEAL[deal] || 'עורך דין') + ': שכר הטרחה שמשרדים פרסמו, ₪ לפני מע״מ', value: n0(m.lo) + '-' + n0(m.hi), sub: esc('עם מע״מ 18%: ' + ils(m.lo * (1 + vat)) + ' עד ' + ils(m.hi * (1 + vat)) + '. רוב המשרדים מפרסמים כ-0.5% מהמחיר, עם מינימום של כ-5,000 עד 6,000 ₪. אין תעריף מחייב; זה טווח שפורסם, לא הצעת מחיר.') };
      lines.push({ label: '0.5% מהמחיר (המקובל ברוב הפרסומים)', value: ils(price * 0.005) });
      lines.push({ label: '1% מהמחיר (הגבוה שפורסם)', value: ils(price * 0.01) });
      lines.push({ label: t.open ? 'התעריף המומלץ של הלשכה לעריכת חוזה: לפי הסכם, לא פחות מ' : 'התעריף המינימלי המומלץ של הלשכה לעריכת חוזה (המלצה שאינה מחייבת)', value: ils(t.fee) });
      bars.push({ name: 'מה שמשרדים פרסמו ב-2026', v: m.lo, hi: m.hi, col: '#1F4B5C' }); bars.push({ name: 'התעריף המומלץ של הלשכה לעריכת חוזה', v: t.fee, col: '#2F6F86' });
      if (deal === 'gift') notes.push(esc('במתנה בתוך המשפחה ובירושה משרדים רבים גובים סכום קבוע ולא אחוז; בקשו הצעה כתובה. מס הרכישה במתנה לקרוב מחושב בדרך אחרת, ראו מחשבון מס רכישה.'));
      notes.push(esc('עורך דין אחד לשני הצדדים: כלל 14 לכללי האתיקה של לשכת עורכי הדין אוסר ייצוג צדדים בעלי אינטרסים מנוגדים באותו ענין, ומתיר עריכת הסכם בידי אותו עורך דין רק כששני הצדדים הסכימו לכך בכתב. גם אז הוא לא יכול לייצג רק אתכם. אנחנו ממליצים שלכל צד יהיה עורך דין משלו.'));
    }
    lf.rows.forEach(function (r) { lines.push({ label: 'אגרה בטאבו: ' + r[0], value: ils(r[1]) }); });
    lines.push({ label: 'אגרות הטאבו בעסקה כזו, יחד', value: ils(lf.total) });
    notes.push(esc('המידע כאן כללי ואינו ייעוץ משפטי. אנחנו אתר מידע ולא מייצגים קונים, מוכרים או יזמים.'));
    var table = { title: 'אגרות לשכת רישום המקרקעין, 2026', head: ['פעולה', 'אגרה'], num: [1], rows: D.land.map(function (r) { return [r[1], ils(r[2])]; }) };
    return { answer: answer, figure: svgCompare(bars, price), lines: lines, note: notes.join('<br>'), table: table,
      formula: deal === 'new' ? 'תקנה 2 לתקנות המכר (דירות) (הגבלת גובה ההוצאות המשפטיות): הנמוך מבין 5,000 ₪ צמוד למדד (5,915 ₪ ב-2026) ו-0.5% מהתמורה, לפני מע״מ; לא חל על דירה שתמורתה מעל 4,642,750 ₪.' : 'מה שפורסם: 0.5% עד 1% מהמחיר ועוד מע״מ, מינימום 5,000 עד 6,000 ₪. התעריף המומלץ של הלשכה לעריכת חוזה: 2% עד 95,004 ₪, 1.5% עד 377,607, 1.25% עד 761,062, 1% עד 2,283,281, 0.75% עד 3,806,082, ומעל לפי הסכם (סכומי 2026).',
      sources: src(D, deal === 'new' ? ['CAP', 'S6C', 'TAR', 'FEES'] : ['DORON', 'ADDA', 'GELB', 'BIZ', 'TAR', 'ETH', 'FEES']),
      text: 'עורך דין מקרקעין, ' + (DEAL[deal] || '') + ' של ' + ils(price) + ': ' + (deal === 'new' ? (cap.capped ? 'הקבלן רשאי לגבות על עורך הדין שלו עד ' + ils(cap.max) + ' ועוד מע״מ.' : 'ללא תקרה מעל 4,642,750 ₪.') : 'שכר טרחה שפורסם ' + ils(m.lo) + ' עד ' + ils(m.hi) + ' ועוד מע״מ; התעריף המומלץ של הלשכה ' + ils(t.fee) + '.') + ' אגרות טאבו ' + ils(lf.total) + '.' };
  }

  function viewSteps(v, D, P) {
    var deal = v.deal, steps = D.steps[deal] || D.steps.buy2, sign = v.sign;
    if (!/^\d{4}-\d{2}-\d{2}$/.test(sign || '')) return { error: { field: 'sign', msg: 'בחרו את יום החתימה (או את היום המשוער).' } };
    var dt = dates(sign, P.pay), lines = [], notes = [];
    lines.push({ label: 'החתימה', value: dd(sign) });
    lines.push({ label: 'הצהרה לרשות המסים (' + P.pay.declare_days + ' יום)', value: dd(dt.declare) });
    if (deal !== 'sell2') lines.push({ label: 'תשלום מס הרכישה (' + P.pay.pay_days + ' יום)', value: dd(dt.pay) });
    if (deal === 'buy2') lines.push({ label: 'מקדמה על מס שבח מתוך התשלום למוכר', value: '7.5% אחרי שעברתם 40% מהמחיר' });
    lines.push({ label: 'איחור בתשלום מס', value: '0.2% לשבוע ועוד הצמדה וריבית' });
    var answer = { label: 'ההצהרה לרשות המסים', value: 'עד ' + dd(dt.declare), sub: esc(deal === 'sell2' ? 'גם המוכר מצהיר בתוך 30 יום. מס השבח, או הפטור, נקבעים בהצהרה.' : 'ומס הרכישה עד ' + dd(dt.pay) + ' (60 יום). בדירה מקבלן שהחזקה ורוב התשלום בה נדחים, התשלום יכול לזוז לפי סעיף 51.') };
    if (deal === 'buy2') notes.push(esc('המקדמה על מס שבח: הקונה מעביר לרשות המסים 7.5% מהמחיר (15% בנכס שהמוכר רכש לפני 7.11.2001), מיד אחרי ששולמו למוכר יותר מ-40% מהתמורה או במועד ההצהרה, המאוחר מביניהם; המקדמה נחשבת כתשלום למוכר. אפשר לבקש מרשות המסים להקטין אותה עד מועד ההצהרה (סעיף 15 לחוק מיסוי מקרקעין).'));
    if (deal === 'new') notes.push(esc('בדירה מקבלן כל תשלום הולך דרך פנקס השוברים לחשבון הפרויקט, ומולו מקבלים ערבות לפי חוק המכר (הבטחת השקעות) או פוליסת ביטוח. משלמים רק בשובר.'));
    notes.push(esc('לפני כל חתימה, גם על זיכרון דברים: עורך דין משלכם. המידע כאן כללי ואינו ייעוץ משפטי.'));
    var table = { title: 'צעדי העסקה: מי עושה ומה המסמכים', head: ['שלב', 'מי', 'מה קורה', 'מסמכים'],
      rows: steps.map(function (s) { return [s[0], s[1], s[2], (s[3] || []).join(', ') || 'אין']; }) };
    return { answer: answer, lines: lines, note: notes.join('<br>'), table: table,
      formula: 'חוק מיסוי מקרקעין: הצהרה בתוך 30 יום מהעסקה (סעיף 73), מס רכישה בתוך 60 יום (סעיף 90א), מקדמה על מס שבח לפי סעיף 15. הנתונים כמו במחשבון מס הרכישה באתר.',
      sources: src(D, ['TAX', 'S6C', 'FEES']).concat([{ label: P.pay.label }]),
      text: (DEAL[deal] || 'עסקה') + ' שנחתמה ב-' + dd(sign) + ': הצהרה לרשות המסים עד ' + dd(dt.declare) + (deal !== 'sell2' ? ', מס רכישה עד ' + dd(dt.pay) : '') + '.' };
  }

  NI.register('orechdin', {
    kicker: 'מחשבון · עורך דין מקרקעין',
    title: 'עורך דין מקרקעין: כמה זה עולה, מה מותר לקבלן לגבות ומה המועדים',
    lede: 'רושמים את סוג העסקה ואת המחיר, ורואים את שכר הטרחה שמשרדים פרסמו לצד התעריף המומלץ של לשכת עורכי הדין, כמה מותר לקבלן לגבות מכם על עורך הדין שלו, ואת אגרות הטאבו. בצעדי העסקה: מה קורה בכל שלב, מי עושה, אילו מסמכים, ועד מתי מצהירים ומשלמים מס.',
    strip: function (data) { var D = data.orechdin; return [{ label: 'התקרה לעורך הדין של הקבלן, 2026', value: F.ils(D.cap.fixed) }, { label: 'או אחוז מהמחיר', value: '0.5%' }, { label: 'הערת אזהרה בטאבו', value: F.ils(188) }, { label: 'הצהרה לרשות המסים', value: '30 יום' }]; },
    presets: function () {
      return [{ key: 'buy2', label: 'קונים יד שנייה ב-2.4 מיליון', sub: 'עם משכנתא', set: { view: 'fee', deal: 'buy2', price: 2400000, mortgage: 'yes' } },
        { key: 'new', label: 'דירה מקבלן ב-3.2 מיליון', sub: 'מה מותר לקבלן לגבות', set: { view: 'fee', deal: 'new', price: 3200000, own: 'yes', mortgage: 'yes' } },
        { key: 'lux', label: 'דירה מקבלן ב-5 מיליון', sub: 'מעל התקרה', set: { view: 'fee', deal: 'new', price: 5000000, own: 'yes', mortgage: 'no' } },
        { key: 'sell', label: 'מוכרים ב-1.9 מיליון', sub: 'שכר טרחה למוכר', set: { view: 'fee', deal: 'sell2', price: 1900000, mortgage: 'no' } },
        { key: 'steps', label: 'צעדי העסקה מהחתימה', sub: 'יד שנייה', set: { view: 'steps', deal: 'buy2', sign: today() } }];
    },
    defaults: function () { return { view: 'fee', deal: 'buy2', price: 2400000, mortgage: 'yes', own: 'yes', sign: today() }; },
    fields: [
      { id: 'view', label: 'מה לבדוק', type: 'segmented', options: [{ value: 'fee', label: 'כמה זה עולה' }, { value: 'steps', label: 'צעדי העסקה' }] },
      { id: 'deal', label: 'סוג העסקה', type: 'select', optionsFrom: function (v, data) { return data.orechdin.deals.map(function (d) { DEAL[d.id] = d.label; return { value: d.id, label: d.label }; }); } },
      { id: 'price', label: 'מחיר העסקה', type: 'money', unit: '₪', showIf: function (v) { return v.view === 'fee'; } },
      { id: 'mortgage', label: 'עם משכנתא', type: 'segmented', showIf: function (v) { return v.view === 'fee' && v.deal !== 'sell2' && v.deal !== 'gift'; }, options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }] },
      { id: 'own', label: 'גם עורך דין משלכם', type: 'segmented', showIf: function (v) { return v.view === 'fee' && v.deal === 'new'; }, options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }] },
      { id: 'sign', label: 'יום החתימה', type: 'date', showIf: function (v) { return v.view === 'steps'; } }
    ],
    compute: function (v, data) {
      var D = data.orechdin, P = data.ptax; if (!D || !D.cap || !P || !P.pay) return { error: { field: null, msg: 'הנתונים לא נטענו.' } };
      if (!Object.keys(DEAL).length) D.deals.forEach(function (d) { DEAL[d.id] = d.label; });
      return v.view === 'steps' ? viewSteps(v, D, P) : viewFee(v, D, P);
    }
  });
})();
