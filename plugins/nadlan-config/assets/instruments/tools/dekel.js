/* NadLan Instruments · dekel v1 (HAD-601, Q3 stage 2, 26.10.2026; 1.72.525 adds dktool and dkboq at the end): the Dekel price-list family of /glossary/מחירון-דקל-לבנייה-ותשתיות/.
   dkpick: the kind of work and its size → the Dekel list that fits, its chapters and items, and a warning when the size is outside the
   band the list is calibrated for; a decision tree with the path lit. dkquote: a contractor's quote line by line against the reader's
   own Dekel unit prices (from a subscription or the contractor's reference), with Dekel's own rules turned into questions for the
   contractor (disposal up to 15 km but not the landfill fee, steel priced apart, remote areas and night work in "תוספות והפחתות").
   No Dekel price is stored or shown: Dekel sells them. Data: data/dekel.json (dekel.co.il, 25.10.2026). Pure logic in NLDK. */
(function () {
  'use strict';
  /** The list for a kind of work, and whether the size is inside its calibrated band (null = the list has no band). */
  function pick(d, kind, budget) {
    var k = d.kinds[kind]; if (!k) return null;
    var L = d.lists[k.list], band = L.min ? (budget >= L.min && budget <= L.max ? 'in' : (budget < L.min ? 'below' : 'above')) : null;
    return { id: k.list, list: L, band: band };
  }
  /** Totals of quote lines: [{q, dk, of}] = quantity, the reader's Dekel unit price, the quote's unit price. */
  function quote(rows) {
    var dk = 0, of = 0, n = 0;
    rows.forEach(function (r) { if (r.q > 0 && r.dk > 0 && r.of > 0) { dk += r.q * r.dk; of += r.q * r.of; n++; } });
    return { dk: dk, of: of, gap: of - dk, pct: dk ? (of / dk - 1) * 100 : 0, n: n };
  }
  window.NLDK = { pick: pick, quote: quote };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;

  function tree(d, kind) {
    var K = Object.keys(d.kinds), W = 420, top = 52, step = 34, g = [];
    g.push('<text x="408" y="20" class="t" text-anchor="start">איזה מחירון: מהעבודה אל המחירון</text>');
    g.push('<text x="408" y="40" class="s" text-anchor="start">העבודה</text><text x="150" y="40" class="s" text-anchor="start">המחירון</text>');
    K.forEach(function (k, i) {
      var y = top + i * step, on = k === kind, L = d.lists[d.kinds[k].list], c = on ? '#1F4FA3' : '#C9D1D8';
      g.push('<rect x="232" y="' + (y - 13) + '" width="176" height="24" fill="' + (on ? '#EAF0FA' : '#fff') + '" stroke="' + c + '" stroke-width="' + (on ? 1.8 : 1) + '"/>');
      g.push('<text x="402" y="' + (y + 4) + '" class="s" text-anchor="start" style="fill:' + (on ? '#12202A' : '#5E6A75') + '">' + esc(d.kinds[k].label) + '</text>');
      g.push('<line x1="232" y1="' + (y - 1) + '" x2="158" y2="' + (y - 1) + '" stroke="' + c + '" stroke-width="' + (on ? 1.8 : 1) + '"/>');
      g.push('<text x="150" y="' + (y + 4) + '" class="s" text-anchor="start" style="fill:' + (on ? '#1F4FA3' : '#8A97A2') + ';font-weight:' + (on ? 600 : 400) + '">' + esc(L.name.replace('מחירון דקל ', '').replace('מחירון ', '')) + '</text>');
    });
    var H = top + K.length * step;
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc('עץ בחירה: ' + d.kinds[kind].label + ' אל ' + d.lists[d.kinds[kind].list].name) + '">' + g.join('') + '</svg>';
  }

  NI.register('dkpick', {
    kicker: 'בחירה · מחירון דקל',
    title: 'איזה מחירון דקל מתאים לעבודה שלכם',
    lede: 'בוחרים את סוג העבודה ואת ההיקף הכספי המשוער, ומקבלים את המחירון של דקל שמתאים לה, כמה פרקים וסעיפים יש בו, והאם ההיקף בתוך הטווח שהמחירים שלו מכוונים אליו.',
    presets: [
      { key: 'new', label: 'פרויקט חדש', sub: '2.5 מיליון ₪', set: { kind: 'new', budget: 2500000 } },
      { key: 'reno', label: 'שיפוץ בבניין קיים', sub: '90 אלף ₪', set: { kind: 'exist', budget: 90000 } },
      { key: 'tenant', label: 'שינויים בדירה מקבלן', sub: 'נספח לחוזה', set: { kind: 'tenant', budget: 60000 } }
    ],
    defaults: function () { return { kind: 'new', budget: 2500000 }; },
    fields: [
      { id: 'kind', label: 'סוג העבודה', type: 'select', optionsFrom: function (v, data) { var k = data.dekel.kinds; return Object.keys(k).map(function (x) { return { value: x, label: k[x].label }; }); } },
      { id: 'budget', label: 'היקף כספי משוער (₪)', type: 'money', help: 'המחירון לבנייה ותשתיות מכוון לפרויקטים של 800 אלף עד 6 מיליון ₪, והמחירון לשיפוצים ואחזקה לעבודות של 150 עד 500 אלף ₪.' }
    ],
    compute: function (v, data) {
      var d = data.dekel, r = pick(d, v.kind, v.budget);
      if (!r) return { error: { field: 'kind', msg: 'בחרו סוג עבודה.' } };
      var L = r.list, lines = [];
      if (L.ch) lines.push({ label: 'פרקים', value: F.num(L.ch) });
      if (L.items) lines.push({ label: 'סעיפים', value: L.items });
      if (L.min) lines.push({ label: 'ההיקף שהמחירים מכוונים אליו', value: '₪' + F.num(L.min) + ' עד ₪' + F.num(L.max) });
      lines.push({ label: 'עדכון', value: 'בכל 1 לחודש' });
      var note = [esc(L.fit) + '.'];
      if (r.band === 'below') note.push('ההיקף שלכם מתחת לטווח: ' + esc(d.rules.size) + '.' + (r.id === 'build' ? ' לעבודה במבנה קיים בחרו את המחירון לשיפוצים ואחזקה.' : ''));
      if (r.band === 'above') note.push('ההיקף שלכם מעל לטווח: ' + esc(d.rules.size) + '.' + (r.id === 'reno' ? ' לפרויקט חדש גדול בחרו את המחירון לבנייה ותשתיות.' : ''));
      note.push(esc(d.rules.incl) + '. ' + esc(d.rules.monthly) + '.');
      note.push('הגישה במנוי בתשלום. דקל לא מפרסם מחיר מנוי באתר (נבדק ב-25.10.2026): ' + esc(d.contact) + '.');
      return {
        answer: { label: 'המחירון שמתאים', value: L.name, tone: r.band && r.band !== 'in' ? 'survey' : '', sub: esc(d.kinds[v.kind].label + (L.min ? ' · ₪' + F.num(v.budget) : '')) },
        figure: tree(d, v.kind),
        lines: lines,
        note: note.join('<br>'),
        table: { title: 'כל מחירוני דקל (לפי אתר דקל, 25.10.2026)', head: ['מחירון', 'פרקים', 'סעיפים', 'למה מתאים'], num: [1], phoneHide: [1],
          rows: Object.keys(d.lists).map(function (k) { var x = d.lists[k]; return [x.name, x.ch ? String(x.ch) : '', x.items || '', x.fit]; }) },
        formula: 'ההתאמה לפי מה שדקל כותב על כל מחירון: למה הוא מיועד ולאיזה היקף עבודה המחירים מכוונים.',
        sources: d.sources,
        text: d.kinds[v.kind].label + ': ' + L.name + (L.ch ? ', ' + L.ch + ' פרקים' : '') + (L.items ? ', ' + L.items + ' סעיפים' : '') + '. מתעדכן בכל 1 לחודש.'
      };
    }
  });

  NI.register('dkquote', {
    kicker: 'בדיקה · הצעת מחיר מול דקל',
    title: 'בדיקת הצעת מחיר של קבלן מול מחירון דקל',
    lede: 'מקלידים לכל סעיף את הכמות, את מחיר היחידה בדקל (מהמנוי שלכם או מההפניה של הקבלן) ואת מחיר היחידה בהצעה, ומסמנים מה יש בעבודה. מקבלים את סך ההפרש ואת השאלות לקבלן לפי הכללים של דקל עצמו.',
    defaults: function () { return { rows: [{ q: 40, dk: 0, of: 0 }, { q: 12, dk: 0, of: 0 }], demo: 'yes', landfill: 'no', steel: 'yes', remote: 'no', night: 'no', month: 'yes' }; },
    exampleNote: 'אין כאן מחירי דקל: מקלידים את המחירים מהמנוי או מההצעה. השאלות מופיעות גם בלי מחירים.',
    fields: [
      { id: 'rows', label: 'סעיפים (כמות, מחיר יחידה בדקל, מחיר יחידה בהצעה)', type: 'rows', addLabel: 'הוספת סעיף',
        cols: [{ id: 'q', label: 'כמות' }, { id: 'dk', label: 'מחיר בדקל', unit: '₪' }, { id: 'of', label: 'מחיר בהצעה', unit: '₪' }], blank: function () { return { q: 1, dk: 0, of: 0 }; } },
      { id: 'demo', label: 'יש בעבודה הריסה ופינוי', type: 'segmented', options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }] },
      { id: 'landfill', label: 'אגרת ההטמנה מופיעה בהצעה', type: 'segmented', options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }], showIf: function (v) { return v.demo === 'yes'; } },
      { id: 'steel', label: 'יש סעיפי בטון מזוין', type: 'segmented', options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }] },
      { id: 'remote', label: 'העבודה באזור מרוחק', type: 'segmented', options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }] },
      { id: 'night', label: 'עבודת לילה, שבת או חג', type: 'segmented', options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא' }] },
      { id: 'month', label: 'מחירי דקל מהמהדורה של החודש שבו ניתנה ההצעה', type: 'segmented', options: [{ value: 'yes', label: 'כן' }, { value: 'no', label: 'לא בטוח' }] }
    ],
    compute: function (v, data) {
      var d = data.dekel, rows = v.rows || [], t = quote(rows), Q = [];
      if (v.demo === 'yes') Q.push(v.landfill === 'yes' ? 'בדקו שאגרת ההטמנה בהצעה אינה כפולה: לפי דקל סעיף ההריסה כולל פינוי עד 15 ק"מ, וההטמנה נפרדת.' : 'לפי דקל סעיף ההריסה כולל פינוי לאתר מורשה עד 15 ק"מ, אבל לא את אגרת ההטמנה. שאלו מי משלם אותה וכמה.');
      if (v.steel === 'yes') Q.push('לפי דקל ברזל הזיון נמדד ומתומחר בנפרד, אלא אם כתוב בסעיף שהוא כלול. שאלו אם הברזל כלול במחיר הבטון בהצעה.');
      if (v.remote === 'yes') Q.push('לאזור מרוחק דקל מוסיף תוספת לפי "תוספות והפחתות". בקשו לראות את התוספת שהקבלן חישב.');
      if (v.night === 'yes') Q.push('לעבודת לילה, שבת וחג יש תוספת לפי "תוספות והפחתות". בקשו לראות אותה בנפרד.');
      if (v.month !== 'yes') Q.push('המחירים מתעדכנים בכל 1 לחודש. השוו למהדורה של החודש שבו ניתנה ההצעה.');
      Q.push('מחירון דקל הוא מחיר ייחוס, לא חוזה: מה שמחייב הוא ההסכם עם הקבלן.');
      var lines = [];
      if (t.n) {
        lines.push({ label: 'סך לפי מחירי דקל', value: F.ils(t.dk) });
        lines.push({ label: 'סך לפי ההצעה', value: F.ils(t.of) });
        lines.push({ label: 'סעיפים שהשוו', value: F.num(t.n) + ' מתוך ' + F.num(rows.length) });
      }
      var out = {
        answer: t.n ? { label: t.gap >= 0 ? 'ההצעה מעל מחירי דקל' : 'ההצעה מתחת למחירי דקל', value: (t.gap >= 0 ? '+' : '') + F.num(t.pct, 1) + '%', tone: t.pct > 0 ? 'survey' : '', sub: esc((t.gap >= 0 ? 'יותר ב-' : 'פחות ב-') + F.ils(Math.abs(t.gap))) }
          : { label: 'השאלות לקבלן', value: Q.length === 1 ? 'שאלה אחת' : F.num(Q.length) + ' שאלות', sub: 'הקלידו מחירי יחידה כדי לראות את ההפרש' },
        lines: lines,
        note: Q.map(function (q, i) { return (i + 1) + '. ' + esc(q); }).join('<br>'),
        formula: 'הפרש באחוזים = (סך ההצעה ÷ סך לפי מחירי דקל − 1) × 100, רק על סעיפים שיש להם כמות ושני מחירים.',
        sources: d.sources,
        text: (t.n ? 'הצעת הקבלן ' + (t.gap >= 0 ? 'מעל' : 'מתחת') + ' למחירי דקל ב-' + F.num(Math.abs(t.pct), 1) + '% (' + F.ils(Math.abs(t.gap)) + '). ' : '') + 'שאלות לקבלן: ' + Q.join(' ')
      };
      if (t.n) out.table = { title: 'ההשוואה סעיף אחר סעיף', head: ['סעיף', 'כמות', 'לפי דקל', 'לפי ההצעה', 'הפרש'], num: [1, 2, 3, 4],
        rows: rows.map(function (r, i) { var ok = r.q > 0 && r.dk > 0 && r.of > 0; return [String(i + 1), F.num(r.q, r.q % 1 ? 2 : 0), ok ? F.ils(r.q * r.dk) : '', ok ? F.ils(r.q * r.of) : '', ok ? F.num((r.of / r.dk - 1) * 100, 1) + '%' : 'חסר מחיר']; }) };
      return out;
    }
  });

  /* 1.72.525 (Q4 /glossary/דקל-תוכנה/): dktool, which Dekel software fits a role, by project stage, with the official address; and
     dkboq, a bill-of-quantities line builder in Dekel's item format with the reader's own unit prices (totals by chapter, contingency,
     VAT as an editable parameter). No price of Dekel's is stored or shown. */
  function boq(rows, cont, vat) {
    var ch = {}, order = [], sub = 0, n = 0;
    rows.forEach(function (r) {
      var q = +r.q, p = +r.p; if (!(q > 0 && p > 0)) return;
      var code = String(r.code || '').trim(), c = (code.split('.')[0] || '').trim() || 'ללא פרק';
      if (!ch[c]) { ch[c] = 0; order.push(c); }
      ch[c] += q * p; sub += q * p; n++;
    });
    var cn = sub * (cont || 0) / 100, net = sub + cn, v = net * (vat || 0) / 100;
    return { ch: ch, order: order, sub: sub, cont: cn, net: net, vat: v, total: net + v, n: n };
  }
  window.NLDK.boq = boq;

  function stages(d, on) {
    var K = Object.keys(d.sw), W = 420, top = 66, step = 30, g = [];
    g.push('<text x="408" y="20" class="t" text-anchor="start">הכלים של דקל לפי שלב בפרויקט</text>');
    g.push('<text x="408" y="40" class="s" text-anchor="start">מסומן: מה שמתאים לתפקיד שבחרתם</text>');
    K.forEach(function (k, i) {
      var y = top + i * step, s = d.sw[k], lit = on.indexOf(k) > -1, c = lit ? '#1F4FA3' : '#C9D1D8';
      g.push('<rect x="12" y="' + (y - 12) + '" width="396" height="24" fill="' + (lit ? '#EAF0FA' : '#fff') + '" stroke="' + c + '" stroke-width="' + (lit ? 1.8 : 1) + '"/>');
      g.push('<text x="402" y="' + (y + 5) + '" class="s" text-anchor="start" style="fill:' + (lit ? '#12202A' : '#8A97A2') + '">' + esc(s.stage) + '</text>');
      g.push('<text x="230" y="' + (y + 5) + '" class="s" text-anchor="start" style="fill:' + (lit ? '#1F4FA3' : '#8A97A2') + ';font-weight:' + (lit ? 600 : 400) + '">' + esc(s.name) + '</text>');
    });
    var H = top + K.length * step;
    return '<svg class="nli__wall" direction="rtl" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc('הכלים של דקל לפי שלב בפרויקט') + '">' + g.join('') + '</svg>';
  }

  NI.register('dktool', {
    kicker: 'בחירה · תוכנת דקל',
    title: 'איזה כלי של דקל מתאים לכם',
    lede: 'בוחרים את התפקיד שלכם בפרויקט ומקבלים את הכלים של דקל שמתאימים לו, מה עושים בכל אחד, הכתובת הרשמית, ואיזה מחירון של דקל עומד מאחוריהם.',
    presets: [
      { key: 'pm', label: 'מפקח או מנהל פרויקט', sub: 'כתב כמויות, ביצוע וחשבונות', set: { role: 'pm' } },
      { key: 'reno', label: 'קבלן שיפוצים', sub: 'מהנייד, בשטח', set: { role: 'reno' } },
      { key: 'buyer', label: 'רוכש דירה', sub: 'שינויי דיירים', set: { role: 'buyer' } }
    ],
    defaults: function () { return { role: 'pm' }; },
    fields: [
      { id: 'role', label: 'התפקיד שלכם', type: 'select', optionsFrom: function (v, data) { var r = data.dekel.roles; return Object.keys(r).map(function (k) { return { value: k, label: r[k].label }; }); } }
    ],
    compute: function (v, data) {
      var d = data.dekel, r = d.roles[v.role];
      if (!r) return { error: { field: 'role', msg: 'בחרו תפקיד.' } };
      var L = d.lists[r.list], lines = r.sw.map(function (k) { var s = d.sw[k]; return { label: s.name + ': ' + s.what, value: s.url || 'דרך דקל בענן' }; });
      lines.push({ label: 'סעיפים במחירון שמאחורי הכלים', value: L.items || '' });
      var note = [];
      if (r.note) note.push(esc(r.note));
      note.push('המחירון: ' + esc(L.name) + ', ' + esc(L.fit) + '.');
      note.push('את המחיר של התוכנה דקל קובעת בהצעה לפי היקף ושימוש, עם הדגמה. ' + esc(d.contact) + '.');
      note.push('כתובות הכניסה הן הכתובות שבמפת האתר של דקל. אתר שנקרא דומה אינו בהכרח של קבוצת דקל.');
      return {
        answer: { label: r.label, value: r.sw.length ? (r.sw.length === 1 ? d.sw[r.sw[0]].name : r.sw.length + ' כלים של דקל') : 'בלי תוכנה', sub: esc(r.sw.length ? r.sw.map(function (k) { return d.sw[k].name; }).join(' · ') : 'מחירון דקל לשינויי דיירים כנספח לחוזה') },
        figure: stages(d, r.sw),
        lines: lines,
        note: note.join('<br>'),
        table: { title: 'כל הכלים של דקל לפי שלב (לפי אתר דקל, 25.10.2026)', head: ['שלב', 'הכלי', 'מה עושים בו', 'כתובת'], phoneHide: [3],
          rows: Object.keys(d.sw).map(function (k) { var s = d.sw[k]; return [s.stage, s.name, s.what, s.url || 'דרך דקל בענן']; }) },
        formula: 'ההתאמה לפי התפקידים שדקל מציינת לכל כלי באתר שלה.',
        sources: d.sources,
        text: r.label + ': ' + (r.sw.length ? r.sw.map(function (k) { return d.sw[k].name + (d.sw[k].url ? ' (' + d.sw[k].url + ')' : ''); }).join(', ') : 'מחירון דקל לשינויי דיירים כנספח לחוזה') + '. ' + L.name + '.'
      };
    }
  });

  NI.register('dkboq', {
    kicker: 'מחשבון · כתב כמויות',
    title: 'כתב כמויות בפורמט דקל: נסו בעצמכם',
    lede: 'מקלידים סעיפים בפורמט של דקל (פרק.תת פרק.סעיף), כמות ומחיר יחידה מהמנוי שלכם או מהצעה, ומקבלים סיכום לכל פרק, בצ"מ (בלתי צפוי מראש) לבחירתכם, מע"מ וסך הכול.',
    defaults: function () { return { rows: [{ code: '02.010.0010', q: 0, p: 0 }, { code: '02.020.0030', q: 0, p: 0 }, { code: '08.011.0050', q: 0, p: 0 }], cont: 5, vat: 18 }; },
    exampleNote: 'אין כאן מחירים של דקל: מקלידים כמות ומחיר יחידה מהמנוי או מהצעה. הקודים לדוגמה מראים רק את המבנה.',
    fields: [
      { id: 'rows', label: 'סעיפים (קוד סעיף, כמות, מחיר יחידה)', type: 'rows', addLabel: 'הוספת סעיף',
        cols: [{ id: 'code', label: 'קוד סעיף', type: 'text', ph: 'פרק.תת פרק.סעיף' }, { id: 'q', label: 'כמות', ph: 'כמות' }, { id: 'p', label: 'מחיר יחידה', unit: '₪', ph: 'מחיר' }],
        blank: function () { return { code: '', q: 0, p: 0 }; } },
      { id: 'cont', label: 'בצ"מ (באחוזים, לבחירתכם)', type: 'percent' },
      { id: 'vat', label: 'מע"מ (באחוזים)', type: 'percent', help: 'מע"מ בישראל: 18%. אפשר לשנות.' }
    ],
    compute: function (v, data) {
      var b = boq(v.rows || [], v.cont, v.vat);
      if (!(v.cont >= 0 && v.cont <= 50)) return { error: { field: 'cont', msg: 'בצ"מ בין 0% ל-50%.' } };
      var lines = b.order.map(function (c) { return { label: 'פרק ' + c, value: F.ils(b.ch[c]) }; });
      if (b.n) {
        lines.push({ label: 'סיכום הסעיפים', value: F.ils(b.sub) });
        if (b.cont) lines.push({ label: 'בצ"מ ' + F.num(v.cont) + '%', value: F.ils(b.cont) });
        lines.push({ label: 'מע"מ ' + F.num(v.vat) + '%', value: F.ils(b.vat) });
      }
      return {
        answer: b.n ? { label: 'סך הכול כולל מע"מ', value: F.ils(b.total), sub: esc(F.num(b.n) + ' סעיפים ב-' + F.num(b.order.length) + (b.order.length === 1 ? ' פרק' : ' פרקים')) }
          : { label: 'כתב הכמויות', value: 'הקלידו כמות ומחיר', sub: 'השורות לדוגמה מראות את מבנה הקוד בלבד' },
        lines: lines,
        note: 'קוד סעיף בדקל בנוי מפרק, תת פרק וסעיף, למשל 68.035.0010 במסמכי מכרז. הסיכום לפי פרק נלקח מהחלק הראשון של הקוד. בכתב כמויות אמיתי מחירי היחידה מגיעים מהמהדורה של החודש.',
        table: b.n ? { title: 'כתב הכמויות', head: ['קוד', 'כמות', 'מחיר יחידה', 'סה"כ'], num: [1, 2, 3],
          rows: (v.rows || []).filter(function (r) { return +r.q > 0 && +r.p > 0; }).map(function (r) { return [String(r.code || ''), F.num(+r.q, +r.q % 1 ? 2 : 0), F.ils(+r.p), F.ils(r.q * r.p)]; }) } : null,
        formula: 'סה"כ = (סכום כמות × מחיר יחידה) × (1 + בצ"מ) × (1 + מע"מ).',
        sources: d0src(data),
        text: b.n ? 'כתב כמויות: ' + F.num(b.n) + ' סעיפים, ' + F.ils(b.sub) + ' לפני בצ"מ ומע"מ, ' + F.ils(b.total) + ' כולל מע"מ.' : 'כתב כמויות בפורמט דקל.'
      };
    }
  });
  function d0src(data) { return data.dekel ? data.dekel.sources : []; }
})();
