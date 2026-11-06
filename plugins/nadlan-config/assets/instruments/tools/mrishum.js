/* NadLan Instruments · mrishum v1 (HAD-675, mortgage universe, 6.11.2026): "רישום משכנתה ואגרות", for the tools switcher of
   /mortgage-calculator/ (pane #tool-rishum). LOCAL build, not released.
   A three-step wizard, phone first: (1) where the home is registered today (טאבו / רמ"י / חברה משכנת / not registered yet, a
   contractor's flat), (2) the action (registration, an additional or second-degree mortgage, an amendment, cancellation after payoff,
   cancellation after death when the life insurance repaid), (3) who files (a lawyer online, by hand at the office, the bank; on the
   ILA path the rights holder or a representative with a power of attorney, online in "רמ"י שלי", per the ILA service page
   gov.il/he/service/guide-mortgage read by hand 6.11.2026; the ILA fee is "not stated on the service page", never a number).
   The result: what is registered where, the 2026 fee lines with a total "לשלם למדינה", the exemption check (regulations 12 and 13 of
   the land fees regulations, with the Kol Zchut and Ministry of Defence conditions read 6.11.2026), the time and who pays (Banking
   (Service to Customer) Law s.9A: the bank files the deletion within 30 days of full payoff, at its cost; s.7ח; s.9ח2), the steps in
   order, the documents of that path ("טופס רישום משכנתא": regulations 9, 10, 14, 16, 21 and 72 of the Land Regulations 2011; no
   official form is hosted or recreated, the gov.il forms page is linked), the contact line, and what is not verified.
   Every amount, condition, deadline and source lives in data/rishum.json ("checked": "2026-11-06"); this file holds no amount.
   Pure logic in window.NLRS (node test: docs/research/2026-11-06-mortgage-universe/build/build-mrishum/test_mrishum.js). Hebrew only,
   RTL; on an English mount the tool draws nothing. Nothing is sent: the case lives in #mrishum= only (no personal data), written into
   the copied text. Style id-scoped (#nlrs) with !important where the theme restyles plain elements. */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;

  var REGS = ['tabu', 'ila', 'company', 'none'];
  var ACTS = [
    { k: 'register', he: 'רישום משכנתה', sub: 'משכנתה חדשה על הדירה' },
    { k: 'second', he: 'משכנתה נוספת', sub: 'או בדרגה שנייה' },
    { k: 'amend', he: 'תיקון משכנתה', sub: 'שינוי תנאים, הגדלה' },
    { k: 'cancel', he: 'ביטול אחרי סילוק', sub: 'פרעתם את כל ההלוואה' },
    { k: 'death', he: 'ביטול אחרי פטירה', sub: 'ביטוח החיים פרע' }
  ];
  var WHO = { lawyer: 'עורך דין במקוון', office: 'ידנית בלשכה', bank: 'הבנק', owner: 'בעל הזכויות', rep: 'מייצג עם ייפוי כוח' };  // owner / rep: the ILA service (online only)
  var NES = ['auto', 'online', 'counter', 'none'];
  var EXK = ['none', 'disabled', 'bereaved_idf', 'bereaved_terror', 'terror', 'olim'];
  var AMEND = [{ k: 'terms', he: 'שינוי תנאים או שמות' }, { k: 'inc', he: 'הגדלת סכום ההלוואה' }];
  var SHORT = { gov_service: 'אתר הממשלה', gov_fees: 'אגרות 2026, אתר הממשלה', gov_forms: 'טפסים, אתר הממשלה', reshumot_land: 'הודעת האגרות 2026',
    reshumot_pledge: 'הודעת המשכון 2026', regs_fees: 'תקנות האגרות', regs_land: 'תקנות הרישום', law_banking: 'חוק הבנקאות', kz_disabled: 'כל זכות',
    kz_idf_disabled: 'כל זכות', kz_terror: 'כל זכות', kz_bereaved_idf: 'כל זכות', kz_bereaved_terror: 'כל זכות', mod_bereaved: 'משרד הביטחון', ila_guide: 'רמ״י, אתר הממשלה', ila_form: 'הטופס של רמ״י', ila_proc: 'נוהל רמ״י 90.02B' };
  var SECW = { ila_proc: 'סעיף', regs_fees: 'תקנה', regs_land: 'תקנה', law_banking: 'סעיף', reshumot_land: 'פרט', reshumot_pledge: 'פרט' };

  /* ------------------------------------------------------------------------------------------------------------- helpers */
  var NF = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function nf(x) { return NF.format(Math.round(x || 0)); }
  function ils(x) { return nf(x) + ' ₪'; }
  function dmy(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : ''; }
  function err(field, msg) { return { error: { field: field, msg: msg } }; }
  function act(k) { for (var i = 0; i < ACTS.length; i++) if (ACTS[i].k === k) return ACTS[i]; return null; }
  function exOf(D, k) { var a = (D && D.exemptions) || []; for (var i = 0; i < a.length; i++) if (a[i].k === k) return a[i]; return null; }
  function reging(a) { return a === 'register' || a === 'second' || a === 'amend'; }
  function ending(a) { return a === 'cancel' || a === 'death'; }
  function whoOpts(reg, a) { if (reg === 'ila') return a === 'register' || a === 'second' ? ['owner', 'rep'] : ['owner']; return reging(a) ? ['lawyer', 'office'] : a === 'cancel' && reg === 'tabu' ? ['bank', 'office'] : ['bank']; }
  function whole(x) { var s = String(x == null ? '' : x).trim(); if (!/^\d{1,3}$/.test(s)) return NaN; return +s; }
  function sum(L) { var s = 0; L.forEach(function (l) { if (l.tot && l.amt > 0) s += l.amt; }); return s; }

  function defaults() { return { reg: 'tabu', act: 'register', who: 'lawyer', nesach: 'auto', ex: 'none', years: 25, amend: 'terms' }; }

  /* ------------------------------------------------------------------------------------------------------------ the math */
  /* every line: { k, label, amt (number or null), shown (text instead of the amount), item, src: [{id, sec}], note, tot (counts in
     "לשלם למדינה"), kind: fee | free | ex | info | later | unk } */
  function compute(v, D) {
    if (!D || !D.land || !D.pledge || !D.src || !D.rules) return err(null, 'הנתונים לא נטענו. רעננו את העמוד.');
    if (REGS.indexOf(v.reg) < 0) return err('reg', 'בחרו איפה הדירה רשומה היום.');
    var A = act(v.act); if (!A) return err('act', 'בחרו מה רוצים לעשות.');
    var reg = v.reg, a = v.act, opts = whoOpts(reg, a), who = opts.indexOf(v.who) > -1 ? v.who : opts[0];
    var F = D.land, P = D.pledge, W = D.where[reg], R = D.rules;
    var nesChoice = NES.indexOf(v.nesach) > -1 ? v.nesach : 'auto';
    var nes = nesChoice === 'auto' ? (reg === 'tabu' && reging(a) ? 'online' : 'none') : nesChoice;
    var online = who === 'lawyer';
    var amend = v.amend === 'inc' ? 'inc' : 'terms';
    var exk = EXK.indexOf(v.ex) > -1 ? v.ex : 'none';
    var X = exk !== 'none' && reging(a) ? exOf(D, exk) : null;
    var years = null;
    if (reg === 'none' && (a === 'register' || a === 'second')) {
      years = whole(v.years);
      if (!(years >= 1 && years <= 40)) return err('years', 'הקלידו מספר שנים שלם, מ־1 עד 40.');
    }
    var L = [], status = 'ok';
    function add(o) { o.src = o.src || []; o.note = o.note || ''; L.push(o); return o; }
    function land(k) { return { id: 'reshumot_land', sec: F[k].item }; }
    function pl(o) { return { id: 'reshumot_pledge', sec: o.item }; }
    var exApplies = !!X && reg === 'tabu' && (a === 'register' || a === 'second');
    var exWhy = '';
    if (X && !exApplies) {
      if (reg === 'tabu') exWhy = 'הפטור מנוסח ״בעד רישום משכנתה״. אם הוא חל גם על ' + (amend === 'inc' ? 'הגדלת הסכום' : 'תיקון') + ', לא מצאנו כתוב, ולכן כאן הוא לא מוריד את האגרה. שאלו את מוקד הרשות.';
      else if (reg === 'none') exWhy = 'הפטור הוא בתקנות האגרות של המקרקעין; בהודעת המשכון אין פטור כזה. הוא יחול כשהמשכנתה תירשם בטאבו.';
      else if (reg === 'ila') exWhy = 'כתב ההתחייבות של רמ״י מופק ממילא ללא אגרה (נוהל 90.02B, סעיף 1.10). הפטור יחול כשהמשכנתה תירשם בטאבו.';
      else exWhy = 'הפטור הוא מאגרה בעד רישום משכנתה, והוא לא כתוב על הערת אזהרה. הוא יחול כשהמשכנתה תירשם בטאבו.';
    }

    if (reg === 'tabu') {
      if (a === 'register' || a === 'second') {
        add({ k: 'mortgage', label: a === 'second' ? 'רישום משכנתה נוספת, גם בדרגה שנייה' : 'רישום משכנתה', amt: exApplies ? 0 : F.mortgage.amount, item: F.mortgage.item,
          src: [land('mortgage'), { id: 'gov_fees' }], tot: true, kind: exApplies ? 'ex' : 'fee',
          note: exApplies ? 'פטור לפי תקנה ' + X.reg + ' (' + X.he + '), במקום ' + ils(F.mortgage.amount) + '.' : '' });
      } else if (a === 'amend') {
        var Fk = amend === 'inc' ? 'mortgage' : 'change';
        add({ k: 'amend', label: amend === 'inc' ? 'הגדלת סכום ההלוואה' : 'שינוי או תיקון בתנאי המשכנתה או בשמות הצדדים', amt: F[Fk].amount, item: F[Fk].item,
          src: [land(Fk), { id: 'gov_fees' }], tot: true, kind: 'fee' });
      } else if (who === 'office') {
        add({ k: 'redeem', label: 'רישום פדיון כשהכסף מופקד בלשכה', amt: F.redeem_deposit.amount, item: F.redeem_deposit.item, src: [land('redeem_deposit'), { id: 'regs_land', sec: '72' }],
          tot: true, kind: 'fee', note: 'כשהבנק מסרב לקבל את החוב: מפקידים אצל הרשם.' });
      } else {
        add({ k: 'redeem', label: 'ביטול המשכנתה (רישום פדיון), כשהכסף שולם ישירות לבנק', amt: 0, item: F.redeem_direct.item, src: [land('redeem_direct'), { id: 'law_banking', sec: '9א(ג)' }],
          tot: true, kind: 'free', note: 'פטור מכל אגרה. הבנק מגיש, והוצאות המחיקה עליו.' });
        status = 'bank';
        if (a === 'death') add({ k: 'inherit', label: 'רישום הירושה בטאבו, בקשה נפרדת של היורשים', amt: F.inherit.amount, item: F.inherit.item, src: [land('inherit')], tot: false, kind: 'info', note: 'לא בסך הכול: זו פעולה נפרדת.' });
      }
    } else if (reg === 'ila') {  // the ILA service page (read by hand) and ILA procedure 90.02B (the official PDF), both 6.11.2026 (D.ila)
      var I = D.ila;
      if (a === 'register' || a === 'second') {
        add({ k: 'commit', label: I.doc + ' ואישור זכויות מרמ״י', amt: I.fee.amount, item: I.fee.sec, src: [{ id: I.fee.src, sec: I.fee.sec }, { id: 'ila_guide' }], tot: true, kind: 'free',
          note: 'ללא תשלום אגרה. הבקשה מקוונת, באזור האישי ״' + I.area + '״.' });
        add({ k: 'note', label: 'הערת אזהרה לטובת הבנק, אם נרשמת גם בטאבו', amt: F.note.amount, item: F.note.item, src: [land('note'), { id: 'regs_land', sec: '21' }], tot: false, kind: 'info',
          note: 'לא בסך הכול: דף השירות ונוהל 90.02B לא מזכירים הערה כזו. אם היא נרשמת, זו השורה הכללית של הערת אזהרה.' });
        add({ k: 'later', label: 'כשהזכויות יירשמו בטאבו: רישום המשכנתה', amt: F.mortgage.amount, item: F.mortgage.item, src: [land('mortgage'), { id: 'ila_proc', sec: 'א.2' }, { id: 'regs_fees', sec: '11א' }], tot: false, kind: 'later',
          note: 'לא בסך הכול. רמ״י לא תרשום את הזכויות בטאבו בלי המשכנתה. ' + R.deposit_at_commitment.he + '.' + (X ? ' הפטור שבחרתם יחול על הרישום הזה.' : '') });
      } else if (a === 'amend') {
        add({ k: 'amend', label: 'תיקון ' + I.doc + ': הפחתת סכום או שינוי דרגה', amt: null, shown: I.fee_other, item: I.amend.sec, src: [{ id: 'ila_proc', sec: I.amend.sec }], tot: false, kind: 'nofee',
          note: I.amend.letter + '.' });
        status = 'ilaamend';
      } else {
        add({ k: 'commit', label: 'סילוק ' + I.doc, amt: null, shown: I.fee_other, item: I.discharge.sec, src: [{ id: 'ila_proc', sec: I.discharge.sec }], tot: false, kind: 'nofee',
          note: I.discharge.he + '.' });
        add({ k: 'note_delete', label: 'מחיקת הערת אזהרה של הבנק, אם נרשמה', amt: F.note_delete.amount, item: F.note_delete.item, src: [land('note_delete')], tot: false, kind: 'info',
          note: 'לא בסך הכול: סעיף 9א(ג) מטיל על הבנק את הוצאות המחיקה של משכנתה או משכון, ולא מזכיר הערת אזהרה. בקשו מהבנק בכתב.' });
        status = 'ilaout';
      }
    } else if (reg === 'company') {
      if (a === 'register' || a === 'second') {
        add({ k: 'commit', label: 'התחייבות לרישום משכנתה מ' + W.body, amt: null, shown: 'לא ידוע', src: [{ id: 'ila_proc', sec: 'א.2' }], tot: false, kind: 'unk',
          note: 'ההתחייבות היא של החברה עצמה; התהליך והאגרה שלה לא נקראו במקור רשמי. ' + W.check + '.' });
        add({ k: 'note', label: 'הערת אזהרה לטובת הבנק, אם נרשמת בטאבו', amt: F.note.amount, item: F.note.item, src: [land('note'), { id: 'regs_land', sec: '21' }], tot: true, kind: 'fee',
          note: 'בטבלת ' + D.year + ' אין שורה נפרדת להערה בגין התחייבות לרישום משכנתה; זו השורה הכללית של הערת אזהרה.' });
        add({ k: 'later', label: 'כשהדירה תירשם בטאבו: רישום המשכנתה', amt: F.mortgage.amount, item: F.mortgage.item, src: [land('mortgage'), { id: 'regs_fees', sec: '11א' }], tot: false, kind: 'later',
          note: 'לא בסך הכול. ' + R.deposit_at_commitment.he + '.' + (X ? ' הפטור שבחרתם יחול על הרישום הזה.' : '') });
      } else if (a === 'amend') {
        add({ k: 'amend', label: 'תיקון ההתחייבות לרישום משכנתה', amt: null, shown: 'לא ידוע', src: [], tot: false, kind: 'unk', note: W.check + ': התהליך והאגרה לא נמצאו במקור רשמי שקראנו.' });
        status = 'unknown';
      } else {
        add({ k: 'commit', label: 'ביטול ההתחייבות לרישום משכנתה', amt: null, shown: 'לא ידוע', src: [{ id: 'law_banking', sec: '9א(א)' }], tot: false, kind: 'unk',
          note: 'הבנק מבטל את השעבודים אחרי פירעון מלא. התהליך מול ' + W.body + ' לא אומת; ' + W.check + '.' });
        add({ k: 'note_delete', label: 'מחיקת הערת אזהרה של הבנק, אם נרשמה', amt: F.note_delete.amount, item: F.note_delete.item, src: [land('note_delete')], tot: false, kind: 'info',
          note: 'לא בסך הכול: סעיף 9א(ג) מטיל על הבנק את הוצאות המחיקה של משכנתה או משכון, ולא מזכיר הערת אזהרה. בקשו מהבנק בכתב.' });
        status = 'bank';
      }
    } else {  // not registered yet: a pledge at the Registrar of Pledges
      if (a === 'register' || a === 'second') {
        var rr = online ? P.reg_online : P.reg_counter, paid = Math.min(years, P.paid_years_max);
        add({ k: 'pledge', label: (a === 'second' ? 'רישום משכון נוסף' : 'רישום משכון') + ' ברשם המשכונות, ' + years + (years === 1 ? ' שנה' : ' שנים') + (online ? ', במקוון' : ', בדלפק'),
          amt: paid * rr.amount, item: rr.item, src: [pl(rr)], tot: true, kind: 'fee',
          note: paid + ' × ' + ils(rr.amount) + ' לשנה' + (years >= P.free_from_year ? '; מהשנה השישית אין אגרה' : '') + '.' });
        add({ k: 'later', label: 'כשהדירה תירשם בטאבו: רישום המשכנתה', amt: F.mortgage.amount, item: F.mortgage.item, src: [land('mortgage')], tot: false, kind: 'later',
          note: 'לא בסך הכול.' + (X ? ' הפטור שבחרתם יחול על הרישום הזה.' : '') });
      } else if (a === 'amend') {
        var ch = online ? P.change_online : P.change_counter, ex2 = online ? P.extend_online : P.extend_counter;
        add({ k: 'change', label: 'שינוי פרטי חייב, נושה, נכס או בעל נכס' + (online ? ', במקוון' : ', בדלפק'), short: 'שינוי פרטים ברשם המשכונות', amt: ch.amount, item: ch.item, src: [pl(ch)], tot: true, kind: 'fee',
          note: 'שינוי בגלל טעות סופר או טעות של הרשם: פטור.' });
        add({ k: 'extend', label: 'הארכת תקופת המשכון, אם צריך', amt: null, shown: ils(ex2.amount) + ' לשנה', item: ex2.item, src: [pl(ex2)], tot: false, kind: 'info',
          note: 'לכל שנה עד חמש שנים; מהשנה השישית פטור. לא בסך הכול.' });
        add({ k: 'inc', label: 'הגדלת הסכום או שינוי תנאים אחר', amt: null, shown: 'לא ברשימה', src: [{ id: 'reshumot_pledge', sec: '' }], tot: false, kind: 'unk',
          note: 'לא מופיעים ברשימת האגרות של רשם המשכונות. בודקים עם הבנק.' });
      } else {
        add({ k: 'cancel', label: 'ביטול המשכון ברשם המשכונות', amt: 0, item: P.cancel.item, src: [pl(P.cancel), { id: 'law_banking', sec: '9א' }], tot: true, kind: 'free',
          note: 'פטור. הבנק מגיש הודעה על המחיקה, והוצאותיה עליו.' });
        status = 'bank';
      }
    }
    // the extract (נסח), a choice of the reader
    if (nes !== 'none') {
      if (reg === 'none') {
        var so = nes === 'online' ? P.search_online : P.search_counter;
        add({ k: 'nesach', label: nes === 'online' ? 'עיון ונסח מרשם המשכונות, באינטרנט' : 'עיון ונסח מרשם המשכונות, בדלפק', amt: so.amount, item: so.item, src: [pl(so)], tot: true, kind: 'fee' });
      } else {
        var nk = nes === 'online' ? 'nesach_online' : 'nesach_counter';
        add({ k: 'nesach', label: (nes === 'online' ? 'נסח רישום מקוון, חתום אלקטרונית' : 'נסח רישום מאושר, בדלפק') + (reg === 'tabu' ? '' : ', אם הנכס רשום בטאבו'), amt: F[nk].amount, item: F[nk].item,
          src: [land(nk)], tot: true, kind: 'fee', note: ending(a) ? 'לבדוק שהשעבוד נמחק.' : '' });
      }
    }
    var exState = X ? { k: X.k, he: X.he, reg: X.reg, applies: exApplies, why: exWhy, saved: exApplies ? F.mortgage.amount : 0 } : null;
    return { reg: reg, act: a, actHe: A.he, who: who, whoOpts: opts, nesChoice: nesChoice, nes: nes, online: online, years: years, amend: amend, exk: exk, ex: exState,
      lines: L, total: sum(L), status: status, where: W };
  }

  /* ----------------------------------------------------------------------------------------------------------- the words */
  function S(id, sec) { return { id: id, sec: sec || '' }; }
  function headline(r, D) {
    var B = r.where.body;
    var I = D.ila;
    if (r.status === 'ilaamend') return { label: 'מה צריך', value: 'מכתב הסכמה מהבנק', text: true, sub: 'להפחתת סכום ההתחייבות או לשינוי הדרגה, עם התאריך המקורי; לא בקשה מקוונת. ' + I.fee_other + ' לתיקון.' };
    if (r.status === 'ilaout') return { label: 'מי פונה לרמ״י', value: 'אתם, עם מסמך הסילוק של הבנק', text: true,
      sub: 'לפי נוהל 90.02B, אחרי פירעון ההלוואה או כשהיא עוברת לנכס אחר. ' + I.fee_other + ' לסילוק.' + (r.total > 0 ? ' הנסח שבחרתם: ' + ils(r.total) + '.' : '') };
    if (r.status === 'unknown') return { label: 'לשלם למדינה', value: r.where.check, text: true, sub: 'לתיקון כזה אין שורה מאומתת בטבלת האגרות של ' + D.year + ', ולכן אין כאן סכום.' };
    if (r.status === 'bank' && r.reg === 'company')
      return { label: 'מי מגיש', value: 'הבנק מבטל את השעבוד', text: true, sub: 'האגרות של ' + B + ' לא אומתו.' + ' מחיקת הערת אזהרה, אם נרשמה: ' + ils(D.land.note_delete.amount) + '.' + (r.total > 0 ? ' הנסח שבחרתם: ' + ils(r.total) + '.' : '') };
    if (r.status === 'bank')
      return { label: 'לשלם למדינה', value: ils(r.total), text: false, sub: (r.reg === 'none' ? 'ביטול משכון פטור' : 'ביטול המשכנתה פטור') + ', והבנק מגיש ומשלם את הוצאות המחיקה.' + (r.total > 0 ? ' ' + ils(r.total) + ' הם הנסח לבדיקה.' : '') };
    var parts = r.lines.filter(function (l) { return l.tot && l.amt > 0; }).map(function (l) { return ils(l.amt) + ' ' + (l.short || l.label.split(',')[0]); });
    var sub = parts.join(' + ');
    if (r.ex && r.ex.applies) sub = 'פטור מאגרת רישום משכנתה לפי תקנה ' + r.ex.reg + (sub ? '. נשאר: ' + sub : '');
    if (r.reg === 'company') sub += (sub ? '. ' : '') + 'בלי האגרה של ' + B + ', שלא אומתה.';
    if (r.reg === 'ila') sub = I.doc + ' ואישור הזכויות: ללא אגרה (נוהל 90.02B, סעיף ' + I.fee.sec + ')' + (sub ? '. נשאר: ' + sub : '') + '. הבקשה מקוונת באזור האישי ״' + I.area + '״, עם מכתב הפנייה מהבנק';
    return { label: 'לשלם למדינה', value: ils(r.total), text: false, sub: sub ? sub + (/[.]$/.test(sub) ? '' : '.') : '' };
  }
  function whereText(r, D) {
    var B = r.where.body;
    if (r.reg === 'tabu') {
      if (r.act === 'register' || r.act === 'second') return { he: 'שטר משכנתה נרשם בפנקס המקרקעין, בלשכת רישום המקרקעין שבה רשום הנכס. השירות מיועד לבעלי זכות הרשומה בפנקסי המקרקעין.', src: [S('regs_land', '9(ב)'), S('gov_service')], ok: true };
      if (r.act === 'amend') return { he: 'התיקון נרשם בפנקס המקרקעין, על המשכנתה הקיימת.', src: [S('reshumot_land', D.land[r.amend === 'inc' ? 'mortgage' : 'change'].item)], ok: true };
      if (r.who === 'office') return { he: 'פדיון בהפקדה: מפקידים את החוב אצל הרשם, והוא רשאי להורות על הפקעת המשכנתה ומחיקתה מפנקס המקרקעין.', src: [S('regs_land', '72')], ok: true };
      return { he: 'המשכנתה נמחקת מפנקס המקרקעין ברישום פדיון. הבנק מגיש, והרשם רשאי לבטל משכנתה לפי בקשת הבנק לבדו, בלי החתימה שלכם.', src: [S('law_banking', '9א'), S('regs_land', '71(ב)(2)')], ok: true };
    }
    if (r.reg === 'none') {
      if (ending(r.act)) return { he: 'המשכון נמחק ברשם המשכונות. ביטול משכון פטור מאגרה, והבנק מגיש את ההודעה על המחיקה.', src: [S('reshumot_pledge', '(2)'), S('law_banking', '9א')], ok: true };
      return { he: 'כל עוד הדירה לא רשומה בטאבו, השעבוד לטובת הבנק נרשם כמשכון ברשם המשכונות. כשהבית יירשם כבית משותף והדירה על שמכם, נרשמת משכנתה בטאבו.', src: [S('reshumot_pledge'), S('gov_service')], ok: true };
    }
    if (r.reg === 'ila') {
      var I = D.ila;
      if (ending(r.act)) return { he: I.discharge.he + '. ההתחייבות רשומה בספרי רמ״י, ואת מסמך הסילוק נותן הבנק. אם נרשמה הערת אזהרה לטובת הבנק, צריך למחוק אותה.',
        src: [S('ila_proc', I.discharge.sec), S('reshumot_land', D.land.note_delete.item)], ok: true };
      if (r.act === 'amend') return { he: I.amend.he + '. ' + I.amend.letter + '.', src: [S('ila_proc', I.amend.sec)], ok: true };
      return { he: I.scope + '. לפי הנוהל הנכס גם לא ניתן לרישום בטאבו. ' + I.undertaking + '. הבקשה מקוונת, באזור האישי ״' + I.area + '״.', src: [S('ila_guide'), S('ila_proc', 'א.2, 1.8')], ok: true };
    }
    if (ending(r.act)) return { he: 'הבנק מבטל את השעבודים אחרי פירעון מלא. מול ' + B + ': ביטול ההתחייבות לרישום משכנתה, בתהליך שלא אימתנו; ' + r.where.check + '. אם נרשמה הערת אזהרה לטובת הבנק, צריך למחוק אותה.', src: [S('law_banking', '9א(א)'), S('reshumot_land', D.land.note_delete.item)], ok: false };
    if (r.act === 'amend') return { he: 'תיקון של התחייבות לרישום משכנתה נעשה מול ' + B + '. את התהליך לא אימתנו; ' + r.where.check + '.', src: [], ok: false };
    return { he: 'כשהזכויות רשומות בחברה משכנת ולא בפנקסי המקרקעין, אין עליהן שטר משכנתה בטאבו: השירות של הרשות מיועד לבעלי זכות הרשומה בפנקסים. ' + D.ila.company_rule.he + '. אם נרשמת הערת אזהרה לטובת הבנק, היא נרשמת לפי תקנה 21. את התהליך ואת האגרה של ' + B + ' לא קראנו; ' + r.where.check + '.',
      src: [S('gov_service'), S('ila_proc', D.ila.company_rule.sec), S('regs_land', '21')], ok: false };
  }
  function timeList(r, D) {
    var R = D.rules, C = D.contact, T = [], B = r.where.body;
    if (reging(r.act)) {
      if (r.reg === 'none') {
        T.push({ he: 'אגרת רשם המשכונות משולמת לכל שנה, עד ' + D.pledge.paid_years_max + ' שנים; מהשנה השישית אין אגרה.', src: [S('reshumot_pledge', D.pledge.reg_counter.item)] });
      } else if (r.reg !== 'tabu') {
        if (r.reg === 'ila' && r.act === 'amend') { T.push({ he: D.ila.fee_other + ' לתיקון.', src: [S('ila_proc', D.ila.amend.sec)] }); T.push(ilaCall(D)); return T; }
        if (r.reg === 'ila') { T.push({ he: D.ila.fee.he + '.', src: [S('ila_proc', D.ila.fee.sec)] }); T.push({ he: D.ila.sla.he + ': ' + D.ila.sla.urban_days + ' ימי עבודה במגזר העירוני, ' + D.ila.sla.agri_days + ' במגזר החקלאי.', src: [S('ila_proc', D.ila.sla.sec)] }); }
        else T.push({ he: 'האגרה של ' + B + ': לא אומתה.', src: [] });
        T.push({ he: 'כשהמשכנתה תירשם בטאבו, את אגרת הרישום משלם הממשכן, כלומר מי שמשעבד את הנכס.', src: [S('regs_fees', R.payer.sec)] });
      } else {
        T.push({ he: R.payer.he + '.', src: [S('regs_fees', R.payer.sec)] });
        T.push({ he: r.who === 'lawyer' ? 'עורך הדין מגיש סמוך לאחר אימות החתימות.' : 'לאימות שטרי משכנתה בלשכה קובעים תור מראש: ימים ' + C.deed_days + ', ' + C.deed_hours + '.', src: r.who === 'lawyer' ? [S('regs_land', '14(ג)')] : [S('gov_service')] });
        T.push({ he: 'משך הטיפול בלשכה: לא מצאנו מועד רשמי, ולכן אין כאן תאריך.', src: [] });
      }
      if (r.reg === 'ila') T.push(ilaCall(D));
      return T;
    }
    if (r.reg === 'tabu' && r.who === 'office') {
      T.push({ he: 'האגרה: ' + ils(D.land.redeem_deposit.amount) + ', כי הכסף מופקד בלשכה.', src: [S('reshumot_land', D.land.redeem_deposit.item)] });
      T.push({ he: 'הרשם מזמין את הבנק לקבל את הכסף ולחתום על שטר פדיון, בתוך ' + R.deposit.notice_days_min + ' ימים לפחות.', src: [S('regs_land', '72(ג)')] });
      return T;
    }
    if (r.reg === 'ila') {
      T.push({ he: 'את הבקשה לסלק את ההתחייבות מגישים לרמ״י, עם מסמך הסילוק של הבנק. ' + D.ila.fee_other + ' לסילוק.', src: [S('ila_proc', D.ila.discharge.sec)] });
      T.push({ he: 'לפי חוק הבנקאות הבנק מבטל את השעבודים אחרי פירעון מלא; המועד של ' + R.s9a.days + ' ימים וההוצאות על הבנק כתובים בחוק למשכנתה או למשכון רשום, לא להתחייבות ברמ״י.', src: [S('law_banking', '9א')] });
    } else T.push({ he: 'הבנק מגיש את ההודעה על מחיקת השעבוד תוך ' + R.s9a.days + ' ימים מיום הפירעון, והוצאות המחיקה עליו. ' + R.s9a.one_deadline + '.', src: [S('law_banking', '9א(א), 9א(ג)')] });
    if (r.reg === 'company') T.push({ he: 'בחוק, המועד וההוצאות על הבנק כתובים למשכנתה או למשכון רשום. על התחייבות בחברה משכנת הוא לא מפרט.', src: [S('law_banking', '9א')] });
    if (r.reg === 'ila') T.push(ilaCall(D));
    if (r.act === 'death') {
      T.push({ he: 'הסעיף מדבר על לקוח שפרע ״בעצמו ולא באמצעות ערב״. איך הוא חל כשחברת ביטוח פרעה, לא מצאנו כתוב: בקשו מהבנק בכתב את מועד ההגשה.', src: [S('law_banking', '9א(א)')] });
      T.push({ he: 'אם הביטוח לא פרע הכול: מי שחייב לפרוע יכול לבקש מהבנק לדחות את התשלומים עד ' + R.s9h2.months + ' חודשים מהפטירה, עם תעודת פטירה, בלי ריבית פיגורים ובלי תשלום נוסף.', src: [S('law_banking', '9ח2')] });
    }
    return T;
  }
  function ilaCall(D) { var c = D.ila.contact; return { he: 'מוקד רמ״י: ' + c.phone + ' או ' + c.phone2 + ', ימים ' + c.days + ', ' + c.hours + '.', src: [S('ila_guide')] }; }
  function steps(r, D) {
    var C = D.contact, R = D.rules, F = D.land, B = r.where.body, s = [];
    function st(he, src) { s.push({ he: he, src: src || [] }); }
    var fee = r.lines.filter(function (l) { return l.k === 'mortgage' || l.k === 'amend'; })[0];
    if (r.reg === 'tabu' && reging(r.act)) {
      st('מוציאים נסח רישום עדכני ומעתיקים ממנו לבקשה את פרטי הנכס: גוש, חלקה ותת־חלקה.', [S('regs_land', '9(ב)')]);
      if (r.act === 'second') st('בודקים בנסח את המשכנתה הקודמת, ומבקשים את הסכמת הבנק הראשון אם היא נדרשת. הבנק לא יסרב סירוב בלתי סביר.', [S('regs_land', '9(ג)(4)'), S('law_banking', '7ח')]);
      st(fee && fee.amt === 0 ? 'מצרפים את אישור הפטור מאגרת רישום משכנתה.' : 'משלמים את האגרה, ' + ils(fee ? fee.amt : 0) + '. את אגרת רישום המשכנתה משלם הממשכן.', [S('regs_land', '9(ג)(3)'), S('regs_fees', '21')]);
      if (r.who === 'lawyer') {
        st('חותמים על השטר בפני עורך הדין, עם תעודת זהות או דרכון בתוקף. עורך הדין מאמת את החתימות ומאשר בכתב שבדק את הפרטים והמסמכים.', [S('regs_land', '14(א), 14(ב)'), S('regs_land', '16')]);
        st('עורך הדין מגיש במקוון, עם כרטיס חכם, סמוך לאחר האימות. שטר סרוק בחתימה אלקטרונית נחשב מקור.', [S('gov_service'), S('regs_land', '9(ג)(1), 14(ג)')]);
      } else {
        st('חותמים על השטר בפני עורך דין, או בלשכה בפני הרשם. לאימות שטרי משכנתה בלשכה קובעים תור מראש: ימים ' + C.deed_days + ', ' + C.deed_hours + '.', [S('gov_service'), S('regs_land', '12')]);
        st('מגישים בלשכה, בדואר, או בתיבות ההפקדה שמחוץ לשערי הלשכות.', [S('gov_service')]);
      }
      st('הרשם בודק את השטר והמסמכים, מאשר ומעביר לביקורת, ואם הכול תקין הרישום נעשה בפנקס.', [S('regs_land', '14(ד), 14(ה)')]);
      st('בודקים בנסח חדש שהרישום נעשה כמו שסוכם.', [S('reshumot_land', F.nesach_online.item)]);
      return s;
    }
    if (r.reg === 'tabu' && r.act === 'cancel' && r.who === 'office') {
      st('הבנק מסרב לקבל את התשלום: מגישים לרשם בקשה להפקיד את החוב אצלו, עם שטר המשכנתה או העתק מאושר, ראיות לסירוב וראיה על סכום החוב.', [S('regs_land', '72(א)')]);
      st('מפקידים את הסכום לפי הוראת הרשם.', [S('regs_land', '72(ב)')]);
      st('הרשם מזמין את הבנק לקבל את הכסף ולחתום על שטר פדיון, בתוך ' + R.deposit.notice_days_min + ' ימים לפחות.', [S('regs_land', '72(ג)')]);
      st('לא הופיע או סירב לחתום: הרשם רשאי להורות על הפקעת המשכנתה ומחיקתה.', [S('regs_land', '72(ד)')]);
      return s;
    }
    if (r.act === 'death') {
      st('מוודאים מול הבנק שביטוח החיים פרע את כל היתרה, ומבקשים אישור בכתב על סילוק מלא ועל מועד ההגשה של המחיקה.', [S('law_banking', '9א')]);
      st('אם נשארה יתרה: מבקשים מהבנק לדחות את התשלומים עד ' + R.s9h2.months + ' חודשים מהפטירה, עם תעודת פטירה.', [S('law_banking', '9ח2')]);
    }
    if (ending(r.act)) {
      if (r.act === 'cancel') st('מסלקים את כל ההלוואה בבנק.', [S('law_banking', '9א(א)')]);
      if (r.reg === 'tabu' || r.reg === 'none') {
        st('הבנק מגיש הודעה על מחיקת ' + (r.reg === 'none' ? 'המשכון' : 'המשכנתה') + ' תוך ' + R.s9a.days + ' ימים מיום הפירעון, והוצאות המחיקה עליו.' + (r.reg === 'tabu' ? ' הרשם רשאי לבטל לפי בקשת הבנק לבדו.' : ''), [S('law_banking', '9א')].concat(r.reg === 'tabu' ? [S('regs_land', '71(ב)(2)')] : []));
        st('אחרי ' + R.s9a.days + ' ימים מוציאים ' + (r.reg === 'none' ? 'נסח מרשם המשכונות' : 'נסח רישום') + ' ובודקים שהשעבוד נמחק. לא נמחק: פונים לבנק בכתב.', [S(r.reg === 'none' ? 'reshumot_pledge' : 'reshumot_land', r.reg === 'none' ? D.pledge.search_online.item : F.nesach_online.item)]);
      } else {
        if (r.reg === 'ila') {
          st('מבקשים מהבנק מסמך סילוק של ההתחייבות. בנק או חברת ביטוח שולחים אותו על נייר ביטחוני או דרך כספות מאובטחות, עם כל הפרטים שבנוהל.', [S('ila_proc', 'ב')]);
          st('פונים לרמ״י בבקשה לסלק את ההתחייבות שרשומה בספרי רמ״י, בצירוף מסמך הסילוק. ' + D.ila.fee_other + ' לסילוק. מוקד רמ״י: ' + D.ila.contact.phone + '.', [S('ila_proc', 'א.3')]);
        } else {
        st('הבנק מבטל את השעבודים אחרי הפירעון.', [S('law_banking', '9א(א)')]);
        st('בודקים מול ' + B + ' שההתחייבות לרישום משכנתה בוטלה; את התהליך שלהם לא אימתנו.', []);
        }
        st('אם נרשמה הערת אזהרה לטובת הבנק: מחיקתה בבקשת הצדדים עולה ' + ils(F.note_delete.amount) + '. בקשו מהבנק בכתב שיגיש אותה.', [S('reshumot_land', F.note_delete.item), S('regs_land', '22')]);
      }
      if (r.act === 'death' && r.reg === 'tabu') st('היורשים רושמים את הירושה בטאבו בבקשה נפרדת (' + ils(F.inherit.amount) + ').', [S('reshumot_land', F.inherit.item)]);
      return s;
    }
    if (r.reg === 'none') {
      if (r.act === 'amend') {
        st('שינוי פרטי חייב, נושה, נכס או בעל נכס נרשם ברשם המשכונות: ' + ils(r.online ? D.pledge.change_online.amount : D.pledge.change_counter.amount) + '. הגדלת סכום או שינוי תנאים אחר לא מופיעים ברשימת האגרות; בודקים עם הבנק.', [S('reshumot_pledge', '(3)')]);
        return s;
      }
      if (r.act === 'second') st('מבקשים את הסכמת הבנק הראשון, אם היא נדרשת. הבנק לא יסרב סירוב בלתי סביר.', [S('law_banking', '7ח')]);
      st('נרשם משכון ברשם המשכונות: ' + ils(r.online ? D.pledge.reg_online.amount : D.pledge.reg_counter.amount) + ' לכל שנה, עד ' + D.pledge.paid_years_max + ' שנים; מהשנה השישית אין אגרה.', [S('reshumot_pledge', (r.online ? D.pledge.reg_online : D.pledge.reg_counter).item)]);
      st('כשהבית יירשם כבית משותף והדירה על שמכם, נרשמת משכנתה בטאבו (' + ils(F.mortgage.amount) + ').', [S('reshumot_land', F.mortgage.item)]);
      return s;
    }
    if (r.reg === 'ila') {
      var I = D.ila, C1 = {}; I.conditions.forEach(function (c) { C1[c.sec] = c.he; });
      if (r.act === 'amend') {
        st('מבקשים מהבנק מכתב הסכמה להפחתת סכום ההתחייבות (גם מ״ללא הגבלה״ לסכום נקוב) או לשינוי הדרגה. המכתב כולל את כל הפרטים של מכתב סילוק.', [S('ila_proc', '1.5ג')]);
        st(I.amend.raise + '.', [S('ila_proc', '1.5ג')]);
        st(I.amend.letter + '.', [S('ila_proc', '1.5')]);
        st('רמ״י מתקנת את ההתחייבות לסכום או לדרגה המעודכנים, ומשאירה את תאריך ההתחייבות המקורי. הסעיף חל רק על הפחתת סכום או שינוי דרגה, לא על שינוי אחר. מוקד רמ״י: ' + I.contact.phone + '.', [S('ila_proc', '1.5ג')]);
        return s;
      }
      st('בודקים את התנאים: הסכם בתוקף, אין עיקול, משכון או הערות מגבילות, אין חובות לרמ״י, אין הפרות או חריגות בנייה, והנכס לא רשום ולא ניתן לרישום בטאבו.', [S('ila_proc', '1.1 עד 1.8')]);
      if (r.act === 'second') st(C1['1.4'] + '. הבנק לא יסרב סירוב בלתי סביר.', [S('ila_proc', '1.4'), S('law_banking', '7ח')]);
      st('מקבלים מהבנק מכתב הפנייה למתן ' + I.doc + '.', [S('ila_guide')]);
      st(r.who === 'rep' ? 'המייצג נכנס לאזור האישי ״' + I.area + '״, מזדהה ב' + I.id + ' ומגיש את הבקשה עם ייפוי כוח כדין.'
        : 'נכנסים לאזור האישי ״' + I.area + '״, מזדהים ב' + I.id + ' ומגישים את הבקשה.', [S('ila_guide')]);
      st(I.sign_all + '. התנאים: ' + I.procedure + '.', [S('ila_guide'), S('ila_proc')]);
      st('רמ״י מנפיקה לכם ולבנק ' + I.doc + ' ואישור זכויות, ללא אגרה. ' + I.digital + '.', [S('ila_proc', I.fee.sec), S('ila_guide')]);
      st('מה רמ״י מתחייבת: ' + I.undertaking.replace(/^רמ״י מתחייבת /, '') + '.', [S('ila_guide'), S('ila_proc', 'א.2')]);
      st('כשהזכויות יירשמו בטאבו, נרשמת באותו מעמד גם המשכנתה לטובת הבנק (' + ils(F.mortgage.amount) + '). אם האגרה הופקדה כבר בעת ההתחייבות, באישור שר האוצר או מי שהסמיך, רואים אותה כאגרה ששולמה.', [S('ila_proc', 'א.2'), S('regs_fees', '11א')]);
      return s;
    }
    // housing company, registration side
    if (r.act === 'amend') { st(r.where.check + ': התהליך והאגרה לתיקון התחייבות לרישום משכנתה לא נמצאו במקור רשמי שקראנו.', []); return s; }
    if (r.act === 'second') st('מבקשים את הסכמת הבנק הראשון, אם היא נדרשת. הבנק לא יסרב סירוב בלתי סביר.', [S('law_banking', '7ח')]);
    st('מבקשים מ' + B + ' התחייבות לרישום משכנתה לטובת הבנק: ההתחייבות היא של החברה עצמה. התהליך והאגרה שלה לא נקראו.', [S('ila_proc', 'א.2')]);
    st('אם נרשמת הערת אזהרה לטובת הבנק: הבקשה חתומה בידי המתחייב או הזכאי ומאומתת בידי עורך דין או רשם, ומצורפים לה ההתחייבות בכתב, הסכמת בעל הזכות הרשומה אם המתחייב אינו הבעלים הרשום, ומסמכי זיהוי.', [S('regs_land', '21')]);
    st('כשהדירה תירשם על שמכם בטאבו, נרשמת משכנתה רגילה (' + ils(F.mortgage.amount) + '). אם האגרה הופקדה כבר בעת ההתחייבות, באישור שר האוצר או מי שהסמיך, רואים אותה כאגרה ששולמה.', [S('regs_fees', '11א')]);
    return s;
  }
  function docs(r, D) {
    var K = D.docs, out = [], B = r.where.body;
    function d(k) { var x = K[k]; out.push({ k: k, he: x.he, src: [S(x.src, x.sec)] }); }
    if (r.reg === 'tabu' && reging(r.act)) {
      d('request'); d('deed');
      if (r.ex && r.ex.applies) out.push({ k: 'exempt', he: K.exempt.he, src: [S(exSrc(r, D))] }); else d('fee');
      d('id'); d('capacity'); d('corp'); d('consent');
      if (r.act === 'second') d('consent_first');
      d('nesach');
      return { items: out, note: '' };
    }
    if (r.reg === 'tabu' && r.act === 'cancel' && r.who === 'office') { d('r72_deed'); d('r72_refusal'); d('r72_sum'); d('id'); return { items: out, note: '' }; }
    if (r.reg === 'ila' && ending(r.act)) {
      d('ila_dis_bank'); d('ila_dis_private'); d('ila_dis_corp'); if (r.act === 'death') d('death_cert');
      return { items: out, note: 'לבקשה לסלק את ההתחייבות ברמ״י (נוהל 90.02B, סעיף ב):' };
    }
    if (ending(r.act)) {
      if (r.act === 'death') d('death_cert');
      return { items: out, note: 'את מחיקת השעבוד מגיש הבנק, לא אתם' + (r.reg === 'company' ? '; מול ' + B + ' בודקים בנפרד.' : '.') };
    }
    if (r.reg === 'none') return { items: out, note: 'רשימת המסמכים של רשם המשכונות לא נקראה במקור רשמי; בודקים עם הבנק או עם עורך הדין.' };
    if (r.reg === 'ila') {
      if (r.act === 'amend') { d('ila_amend_letter'); return { items: out, note: 'לתיקון ברמ״י (נוהל 90.02B, סעיף 1.5):' }; }
      d('ila_referral'); if (r.who === 'rep') d('ila_poa'); d('ila_sign'); d('ila_spouses');
      if (r.act === 'second') d('ila_consent_prev');
      d('ila_form');
      return { items: out, note: 'לבקשה ברמ״י, במקוון באזור האישי ״' + D.ila.area + '״:' };
    }
    if (r.act === 'amend') return { items: out, note: r.where.check + ': רשימת המסמכים לתיקון לא נמצאה במקור רשמי.' };
    out.push({ k: 'commit', he: 'התחייבות לרישום משכנתה מ' + B + ' (התהליך לא אומת)', src: [] });
    d('note_req'); d('note_commit'); d('note_owner'); d('note_id');
    if (r.act === 'second') d('consent_first');
    return { items: out, note: 'לרישום הערת אזהרה, אם נרשמת:' };
  }
  function exSrc(r, D) { var X = exOf(D, r.exk); return X && X.how && X.how.length ? X.how[X.how.length - 1].src : 'regs_fees'; }
  /* an entry shows when every filter it names matches the path ("ex": ["*"] = any exemption picked on a registration step) */
  function unverified(r, D) {
    return (D.unverified || []).filter(function (u) {
      var w = u.when || {}, exNow = r.ex ? r.exk : 'none';
      return (!w.reg || w.reg.indexOf(r.reg) > -1) && (!w.act || w.act.indexOf(r.act) > -1)
        && (!w.ex || (w.ex[0] === '*' ? exNow !== 'none' : w.ex.indexOf(exNow) > -1));
    });
  }
  function showTotal(r) { return !(r.status === 'unknown' || ((r.status === 'ilaamend' || r.status === 'ilaout') && !(r.total > 0))); }
  function pathText(r, D) { return D.where[r.reg].long + ' · ' + r.actHe + ' · ' + WHO[r.who]; }
  function enc(v) {
    var o = [REGS.indexOf(v.reg) > -1 ? v.reg : 'tabu', act(v.act) ? v.act : 'register', WHO[v.who] ? v.who : 'lawyer', NES.indexOf(v.nesach) > -1 ? v.nesach : 'auto',
      EXK.indexOf(v.ex) > -1 ? v.ex : 'none', String(whole(v.years) >= 1 && whole(v.years) <= 40 ? whole(v.years) : 25), v.amend === 'inc' ? 'inc' : 'terms'];
    return o.join('.');
  }
  function dec(s) {
    var p = String(s || '').split('.'); if (p.length !== 7) return null;
    var v = defaults();
    if (REGS.indexOf(p[0]) > -1) v.reg = p[0]; if (act(p[1])) v.act = p[1]; if (WHO[p[2]]) v.who = p[2]; if (NES.indexOf(p[3]) > -1) v.nesach = p[3];
    if (EXK.indexOf(p[4]) > -1) v.ex = p[4]; var y = whole(p[5]); if (y >= 1 && y <= 40) v.years = y; if (p[6] === 'inc') v.amend = 'inc';
    return v;
  }
  function chk(D) { return dmy(D.checked); }
  function itemText(l) { var id = l.src[0] && l.src[0].id; return (id === 'reshumot_pledge' ? 'הודעת המשכון, פרט ' : id === 'ila_proc' ? 'נוהל 90.02B, סעיף ' : 'פרט ') + l.item; }
  function sourceLine(D) {
    var f = D.src.gov_fees, l = D.src.reshumot_land, p = D.src.reshumot_pledge;
    return 'המקור לאגרות: ״' + f.title + '״ באתר הממשלה (פורסם ' + dmy(f.published) + ', עודכן ' + dmy(f.updated) + '), לפי ' + l.title + ' (' + l.where + ') ו' + p.title + ' (' + p.where + '). '
      + D.rules.update.he + '. נבדק ב־' + chk(D) + '.';
  }
  function copyText(r, D, link) {
    var h = headline(r, D), T = [];
    T.push('רישום משכנתה ואגרות ' + D.year + ': ' + pathText(r, D) + '.');
    T.push(h.label + ': ' + h.value + (h.sub ? ' (' + h.sub.replace(/[.]$/, '') + ')' : '') + '.');
    r.lines.forEach(function (l) { T.push('· ' + l.label + ': ' + (l.amt == null ? l.shown : ils(l.amt)) + (l.item ? ' (' + itemText(l) + ')' : '') + (l.tot ? '' : ', לא בסך הכול')); });
    timeList(r, D).forEach(function (t) { T.push('· ' + t.he); });
    if (r.ex) T.push('פטור: ' + r.ex.he + ' (תקנה ' + r.ex.reg + '). ' + (r.ex.applies ? 'על המסלול הזה האגרה יורדת ל־0 ₪.' : r.ex.why));
    var C = D.contact;
    T.push('מוקד ' + C.body + ': ' + C.phone + ', ' + C.ext + ', ימים ' + C.days + ' ' + C.hours + '. וואטסאפ ' + C.whatsapp + '.');
    T.push(sourceLine(D));
    if (link) T.push(link);
    return T.join('\n');
  }
  function checklistText(r, D) {
    var dc = docs(r, D), T = ['טופס רישום משכנתא, מה מגישים: ' + pathText(r, D)];
    if (dc.note) T.push(dc.note);
    dc.items.forEach(function (x) { T.push('[ ] ' + x.he); });
    if (r.reg === 'ila') { T.push('הטופס של רמ״י: ' + D.src.ila_form.url); T.push('דף השירות של רמ״י: ' + D.src.ila_guide.url); }
    else { T.push('הטפסים הרשמיים: ' + D.src.gov_forms.url); T.push('דף השירות: ' + D.src.gov_service.url); }
    return T.join('\n');
  }

  G.NLRS = { compute: compute, headline: headline, whereText: whereText, timeList: timeList, steps: steps, docs: docs, unverified: unverified, copyText: copyText,
    checklistText: checklistText, sourceLine: sourceLine, showTotal: showTotal, pathText: pathText, enc: enc, dec: dec, defaults: defaults, whoOpts: whoOpts, REGS: REGS, ACTS: ACTS, WHO: WHO, EXK: EXK };
  if (!G.NadLanInstruments) return;

  /* ------------------------------------------------------------------------------------------------------------ the page */
  var NI = G.NadLanInstruments, esc = NI.esc;
  var FONT = '"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif', MONO = '"IBM Plex Mono",ui-monospace,monospace';
  var CSS = '#nlrs.nli__panel::before{display:none!important}#nlrs{--ink:#12202A;--ink2:#3E4C58;--mute:#5E6A75;--line:#D3DCE2;--sea:#2F6F86;--deep:#1F4B5C;--red:#C42550;--green:#4F9A5C;--ground:#F6F8F9;font-family:' + FONT + ';color:var(--ink);background:#fff!important}'
    + '#nlrs *{box-sizing:border-box}#nlrs [hidden]{display:none!important}'
    + '#nlrs p,#nlrs li,#nlrs span,#nlrs label,#nlrs dd,#nlrs dt{overflow-wrap:anywhere}'
    + '#nlrs p.nlrs__k{margin:0 0 4px!important;font:500 12px/18px ' + FONT + '!important;letter-spacing:.06em;color:var(--sea)!important;position:relative}'
    + '#nlrs h2.nlrs__h{margin:0 0 6px!important;padding:0!important;border:0!important;background:none!important;font:600 24px/32px ' + FONT + '!important;color:var(--ink)!important;text-wrap:balance;position:relative;letter-spacing:0!important}#nlrs h2.nlrs__h::before,#nlrs h2.nlrs__h::after{display:none!important}'
    + '#nlrs p.nlrs__lede{margin:0 0 14px!important;font:400 15px/24px ' + FONT + '!important;color:var(--ink2)!important;max-width:68ch;position:relative}'
    + '#nlrs .nlrs__grid{display:grid;grid-template-columns:minmax(0,1fr);grid-template-areas:"a" "r" "c" "m";gap:18px;position:relative}'
    + '@media (min-width:960px){#nlrs .nlrs__grid{grid-template-columns:minmax(0,420px) minmax(0,1fr);grid-template-areas:"a r" "c r" "m m";gap:18px 32px;align-items:start}}'
    + '#nlrs .nlrs__form{grid-area:a;display:flex;flex-direction:column;gap:16px;min-width:0}#nlrs .nlrs__res{grid-area:r;min-width:0;display:flex;flex-direction:column;gap:16px}'
    + '#nlrs .nlrs__call{grid-area:c;min-width:0}#nlrs .nlrs__more{grid-area:m;min-width:0;display:grid;grid-template-columns:minmax(0,1fr);gap:16px}'
    + '@media (min-width:960px){#nlrs .nlrs__more{grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:18px 32px}}'
    + '#nlrs .nlrs__q{display:flex;flex-direction:column;gap:8px;min-width:0}'
    + '#nlrs p.nlrs__qh{display:flex;align-items:center;gap:10px;margin:0!important;font:600 15px/22px ' + FONT + '!important;color:var(--ink)!important}'
    + '#nlrs .nlrs__n{display:inline-flex;align-items:center;justify-content:center;flex:0 0 26px;width:26px;height:26px;border:1.5px solid var(--deep);border-radius:2px;font:500 14px/1 ' + MONO + ';color:var(--deep)}'
    + '#nlrs .nlrs__opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}'
    + '#nlrs .nlrs__opts.is-3{grid-template-columns:repeat(3,minmax(0,1fr))}#nlrs .nlrs__opts.is-1{grid-template-columns:minmax(0,1fr)}'
    + '#nlrs .nlrs__opts:not(.is-3)>button:last-child:nth-child(odd){grid-column:1/-1}'
    + '#nlrs button.nlrs__o{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:2px;min-height:52px!important;height:auto!important;width:auto!important;margin:0!important;padding:8px 10px!important;border:1px solid var(--line)!important;border-radius:2px!important;background:#fff!important;color:var(--ink)!important;box-shadow:none!important;text-align:right!important;cursor:pointer;text-transform:none!important;letter-spacing:0!important;white-space:normal!important}'
    + '#nlrs button.nlrs__o b{font:600 14px/19px ' + FONT + '!important;color:inherit!important}#nlrs button.nlrs__o small{font:400 12px/16px ' + FONT + '!important;color:var(--mute)!important}'
    + '#nlrs button.nlrs__o:hover{border-color:var(--sea)!important}'
    + '#nlrs button.nlrs__o[aria-pressed="true"]{background:var(--deep)!important;border-color:var(--deep)!important;color:#fff!important}#nlrs button.nlrs__o[aria-pressed="true"] small{color:#DCE7EC!important}'
    + '#nlrs button:focus-visible,#nlrs a:focus-visible,#nlrs input:focus-visible,#nlrs summary:focus-visible{outline:2px solid var(--sea)!important;outline-offset:2px}'
    + '#nlrs .nlrs__x{display:flex;flex-direction:column;gap:14px;padding:12px;border:1px dashed var(--line);border-radius:2px}'
    + '#nlrs .nlrs__lab{display:block;margin:0 0 6px!important;font:500 13px/18px ' + FONT + '!important;color:var(--ink2)!important}'
    + '#nlrs .nlrs__in{display:flex;align-items:stretch;height:48px;border:1px solid var(--sea);border-radius:2px;background:#fff;max-width:220px}'
    + '#nlrs .nlrs__in input{flex:1 1 auto;min-width:0;width:100%!important;height:auto!important;min-height:44px!important;margin:0!important;padding:0 10px!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;outline:0;font:400 17px/1.2 ' + MONO + '!important;color:var(--ink)!important;text-align:right}'
    + '#nlrs .nlrs__in span{display:flex;align-items:center;flex:0 0 auto;white-space:nowrap;padding:0 12px;border-inline-start:1px solid var(--line);background:var(--ground);font:400 14px/1 ' + FONT + ';color:var(--mute)}'
    + '#nlrs .nlrs__help{display:block;margin:6px 0 0!important;font:400 12px/18px ' + FONT + '!important;color:var(--mute)!important}'
    + '#nlrs .nlrs__err{display:block;margin:4px 0 0;font:500 13px/18px ' + FONT + '!important;color:var(--red)!important}#nlrs .nlrs__err:empty{display:none}'
    + '#nlrs .nlrs__out{display:flex;flex-direction:column;gap:6px;border-top:2px solid var(--ink);padding-top:12px}'
    + '#nlrs .nlrs__path{font:500 12px/18px ' + FONT + '!important;color:var(--mute)!important;margin:0!important}'
    + '#nlrs .nlrs__ol{font:500 13px/18px ' + FONT + '!important;color:var(--ink2)!important}'
    + '#nlrs .nlrs__fig{font:500 40px/46px ' + MONO + '!important;color:var(--ink)!important;font-variant-numeric:tabular-nums}#nlrs .nlrs__fig.is-text{font:600 24px/32px ' + FONT + '!important}'
    + '#nlrs p.nlrs__sub{margin:0!important;font:400 14px/22px ' + FONT + '!important;color:var(--ink2)!important}'
    + '#nlrs p.nlrs__msg{margin:0!important;padding:10px 12px!important;border-inline-start:3px solid var(--red);background:var(--ground);font:500 14px/22px ' + FONT + '!important;color:var(--ink)!important}'
    + '#nlrs .nlrs__sec{display:flex;flex-direction:column;gap:8px;min-width:0}'
    + '#nlrs p.nlrs__sh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0!important;padding:0 0 6px!important;border-bottom:1px solid var(--line);font:600 15px/22px ' + FONT + '!important;color:var(--deep)!important}'
    + '#nlrs h3.nlrs__sh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0!important;padding:0 0 6px!important;border:0!important;border-bottom:1px solid var(--line)!important;background:none!important;font:600 16px/24px ' + FONT + '!important;color:var(--deep)!important;letter-spacing:0!important}#nlrs h3.nlrs__sh::before,#nlrs h3.nlrs__sh::after{display:none!important}'
    + '#nlrs .nlrs__b{display:inline-block;padding:1px 8px;border:1px solid currentColor;border-radius:2px;font:500 11px/18px ' + FONT + ';letter-spacing:.02em}'
    + '#nlrs .nlrs__b.is-ok{color:var(--sea)}#nlrs .nlrs__b.is-no{color:var(--red)}#nlrs .nlrs__b.is-ex{color:#3B7A47;border-color:var(--green)}'
    + '#nlrs p.nlrs__p{margin:0!important;font:400 14px/22px ' + FONT + '!important;color:var(--ink)!important}'
    + '#nlrs .nlrs__s{display:inline-flex;flex-wrap:wrap;gap:2px 10px}'
    + '#nlrs .nlrs__s a,#nlrs a.nlrs__c{font:400 12px/18px ' + FONT + '!important;color:var(--sea)!important;text-decoration:underline!important;text-decoration-color:#9DB8C3!important;text-underline-offset:3px;white-space:nowrap}'
    + '#nlrs ol.nlrs__ls{list-style:none!important;margin:0!important;padding:0!important;display:flex;flex-direction:column}'
    + '#nlrs ol.nlrs__ls>li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 12px;margin:0!important;padding:9px 0!important;border-bottom:1px solid var(--line);list-style:none!important;background:none!important}'
    + '#nlrs ol.nlrs__ls>li::before,#nlrs ol.nlrs__ls>li::marker{content:none!important;display:none!important}'
    + '#nlrs .nlrs__lk{font:400 14px/21px ' + FONT + '!important;color:var(--ink)!important}#nlrs .nlrs__it{display:block;font:400 12px/18px ' + FONT + '!important;color:var(--mute)!important}'
    + '#nlrs .nlrs__lv{font:500 15px/21px ' + MONO + '!important;color:var(--ink)!important;white-space:nowrap;text-align:left}'
    + '#nlrs li.is-free .nlrs__lv,#nlrs li.is-ex .nlrs__lv{color:#3B7A47!important}#nlrs li.is-ex{border-inline-start:3px solid var(--green)!important;padding-inline-start:8px!important}'
    + '#nlrs li.is-info .nlrs__lv,#nlrs li.is-later .nlrs__lv,#nlrs li.is-unk .nlrs__lv{color:var(--mute)!important;font-weight:400!important}#nlrs li.is-unk .nlrs__lv{color:var(--red)!important}'
    + '#nlrs .nlrs__lv.is-txt{font-family:' + FONT + '!important;font-size:13px!important;font-weight:500!important;white-space:normal!important;max-width:11em}#nlrs li.is-nofee .nlrs__lv{color:var(--ink2)!important}'
    + '#nlrs .nlrs__ln{grid-column:1/-1;font:400 12px/18px ' + FONT + '!important;color:var(--mute)!important}'
    + '#nlrs ol.nlrs__ls>li .nlrs__s{grid-column:1/-1}'
    + '#nlrs ol.nlrs__ls>li.is-total{border-bottom:0!important;border-top:2px solid var(--ink);margin-top:-1px!important;padding:12px 0 4px!important}#nlrs li.is-total .nlrs__lk,#nlrs li.is-total .nlrs__lv{font-weight:600!important;font-size:17px!important}'
    + '#nlrs ul.nlrs__ul,#nlrs ol.nlrs__st{margin:0!important;padding:0!important;list-style:none!important;display:flex;flex-direction:column;gap:8px;counter-reset:st}'
    + '#nlrs ul.nlrs__ul>li,#nlrs ol.nlrs__st>li{position:relative;margin:0!important;padding:0 22px 0 0!important;list-style:none!important;background:none!important;font:400 14px/22px ' + FONT + '!important;color:var(--ink)!important}'
    + '#nlrs ul.nlrs__ul>li::marker,#nlrs ol.nlrs__st>li::marker{content:none!important}'
    + '#nlrs ul.nlrs__ul>li::before{content:"";position:absolute;right:4px;top:9px;width:6px;height:6px;background:var(--sea)}'
    + '#nlrs ol.nlrs__st>li{counter-increment:st;padding-right:32px!important}#nlrs ol.nlrs__st>li::before{content:counter(st);position:absolute;right:0;top:0;width:22px;height:22px;border:1px solid var(--deep);border-radius:2px;font:500 12px/20px ' + MONO + ';color:var(--deep);text-align:center}'
    + '#nlrs .nlrs__exb{display:flex;flex-direction:column;gap:8px;padding:12px;border:1px solid var(--line);border-inline-start:3px solid var(--green);border-radius:2px}'
    + '#nlrs .nlrs__exb.is-no{border-inline-start-color:var(--red)}'
    + '#nlrs p.nlrs__mh{margin:4px 0 0!important;font:600 13px/20px ' + FONT + '!important;color:var(--ink2)!important}'
    + '#nlrs .nlrs__form-sheet{border:1px solid var(--ink);border-radius:2px;padding:14px;display:flex;flex-direction:column;gap:10px;background:#fff}'
    + '#nlrs .nlrs__ck{display:grid;grid-template-columns:28px minmax(0,1fr);gap:4px 8px;align-items:start;min-height:44px;padding:8px 0;border-bottom:1px solid var(--line);cursor:pointer}'
    + '#nlrs .nlrs__ck input{width:22px!important;height:22px!important;min-height:0!important;margin:1px 0 0!important;accent-color:#1F4B5C;cursor:pointer}'
    + '#nlrs .nlrs__ck span{font:400 14px/22px ' + FONT + '!important;color:var(--ink)!important}#nlrs .nlrs__ck .nlrs__s{grid-column:2}'
    + '#nlrs .nlrs__btns{display:flex;flex-wrap:wrap;gap:8px}'
    + '#nlrs button.nlrs__btn{display:inline-flex;align-items:center;min-height:44px!important;height:auto!important;width:auto!important;margin:0!important;padding:0 16px!important;border:1px solid var(--line)!important;border-radius:2px!important;background:#fff!important;color:var(--ink)!important;font:500 14px/1.2 ' + FONT + '!important;box-shadow:none!important;cursor:pointer;text-transform:none!important;letter-spacing:0!important}'
    + '#nlrs button.nlrs__btn.is-primary{background:var(--deep)!important;border-color:var(--deep)!important;color:#fff!important}'
    + '#nlrs ul.nlrs__links{margin:0!important;padding:0!important;list-style:none!important;display:flex;flex-direction:column;gap:6px}#nlrs ul.nlrs__links li{margin:0!important;padding:0!important;list-style:none!important;background:none!important;font:400 14px/22px ' + FONT + '!important}#nlrs ul.nlrs__links li::before,#nlrs ul.nlrs__links li::marker{content:none!important;display:none!important}'
    + '#nlrs ul.nlrs__links a,#nlrs .nlrs__call a,#nlrs .nlrs__rel a{color:var(--sea)!important;text-decoration:underline!important;text-underline-offset:3px}'
    + '#nlrs .nlrs__warn{border:1px solid var(--line);border-inline-start:3px solid var(--red);border-radius:2px;padding:12px}'
    + '#nlrs .nlrs__call{border:1px solid var(--deep);border-radius:2px;padding:12px 14px;display:flex;flex-direction:column;gap:6px}'
    + '#nlrs .nlrs__call p{margin:0!important;font:400 14px/22px ' + FONT + '!important;color:var(--ink)!important}#nlrs .nlrs__call b{font-weight:600}'
    + '#nlrs .nlrs__tel{font:500 18px/26px ' + MONO + '!important}'
    + '#nlrs p.nlrs__fine{margin:0!important;font:400 12px/19px ' + FONT + '!important;color:var(--mute)!important}#nlrs p.nlrs__fine a{color:var(--sea)!important}'
    + '#nlrs details.nlrs__all summary{min-height:44px;display:flex;align-items:center;cursor:pointer;font:500 14px/20px ' + FONT + '!important;color:var(--sea)!important;list-style:none}'
    + '#nlrs details.nlrs__all summary::-webkit-details-marker{display:none}#nlrs details.nlrs__all summary::before{content:"+";display:inline-block;width:18px;font:500 15px/1 ' + MONO + '}#nlrs details.nlrs__all[open] summary::before{content:"-"}'
    + '#nlrs bdi{unicode-bidi:isolate}#nlrs bdi[dir="ltr"]{white-space:nowrap}'
    + '@media print{#nlrs .nlrs__form,#nlrs .nlrs__btns,#nlrs button{display:none!important}#nlrs .nlrs__grid{display:block}#nlrs details.nlrs__all{display:block}}';
  function ensureCss() { if (document.getElementById('nlrs-css')) return; var s = document.createElement('style'); s.id = 'nlrs-css'; s.textContent = CSS; document.head.appendChild(s); }

  NI.register('mrishum', {
    custom: function (root, data) {
      if (NI.langOf && NI.langOf(root) === 'en') return;  // Hebrew only
      var D = data.rishum || data.d0;
      if (!D || !D.land || !D.src) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
      build(root, D);
    }
  });

  function build(root, D) {
    ensureCss();
    var v = defaults(), fromLink = false;
    var m = /#mrishum=([A-Za-z0-9_.\-]+)/.exec(location.hash || ''); if (m) { var hv = dec(m[1]); if (hv) { v = hv; fromLink = true; } }
    function chip(s) {
      var x = D.src[s.id]; if (!x) return '';
      var w = s.sec ? (SECW[s.id] ? SECW[s.id] + ' ' : '') + s.sec + ' · ' : '';
      var dt = x.updated && /^kz_/.test(s.id) ? ' · עודכן ' + dmy(x.updated) : '';
      return '<a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(w + SHORT[s.id] + dt) + '</a>';
    }
    function rich(t) { return esc(t).replace(/(\*\d{3,5}|972-[\d-]+|0\d{1,2}-\d{6,7})/g, '<bdi dir="ltr">$1</bdi>'); }  // phone numbers keep their order in RTL
    function chips(a) { return a && a.length ? '<span class="nlrs__s">' + a.map(chip).join('') + '</span>' : ''; }
    function tile(key, val, he, sub) { return '<button type="button" class="nlrs__o" data-s="' + key + '" data-val="' + esc(val) + '"><b>' + esc(he) + '</b>' + (sub ? '<small>' + esc(sub) + '</small>' : '') + '</button>'; }
    function q(n, id, title, inner, cls, show) {
      return '<div class="nlrs__q"' + (show ? ' data-v="' + show + '"' : '') + '><p class="nlrs__qh" id="nlrs-' + id + '-l">' + (n ? '<span class="nlrs__n">' + n + '</span>' : '') + esc(title) + '</p>'
        + '<div class="nlrs__opts' + (cls ? ' ' + cls : '') + '" role="group" aria-labelledby="nlrs-' + id + '-l" data-g="' + id + '">' + inner + '</div></div>';
    }
    var C = D.contact, F = D.land, P = D.pledge;
    var regTiles = REGS.map(function (k) { return tile('reg', k, D.where[k].he, D.where[k].sub); }).join('');
    var actTiles = ACTS.map(function (x) { return tile('act', x.k, x.he, x.sub); }).join('');
    var exTiles = tile('ex', 'none', 'אין פטור', '') + D.exemptions.map(function (x) { return tile('ex', x.k, x.he, 'תקנה ' + x.reg); }).join('');
    var h = '<div class="nli__panel" id="nlrs" dir="rtl" lang="he">'
      + '<p class="nlrs__k">מחשבון · רישום משכנתה · אגרות ' + D.year + '</p>'
      + '<h2 class="nlrs__h">רישום משכנתה ואגרות: מה נרשם, איפה, וכמה משלמים למדינה</h2>'
      + '<p class="nlrs__lede">שלוש בחירות, ומקבלים את מה שנרשם ואיפה, את האגרות של ' + D.year + ' עם סך הכול, את השלבים, את רשימת המסמכים לבקשה ואת הפטורים. החישוב נעשה כאן בדפדפן, ושום פרט לא נשלח.</p>'
      + '<div class="nlrs__grid">'
      + '<div class="nlrs__form">'
      + q(1, 'reg', 'איפה הדירה רשומה היום', regTiles)
      + q(2, 'act', 'מה רוצים לעשות', actTiles)
      + '<div class="nlrs__q"><p class="nlrs__qh" id="nlrs-who-l"><span class="nlrs__n">3</span>מי מגיש</p><div class="nlrs__opts" role="group" aria-labelledby="nlrs-who-l" data-g="who"></div><span class="nlrs__help" data-whohelp></span></div>'
      + '<div class="nlrs__x">'
      + '<div class="nlrs__q" data-v="amend"><p class="nlrs__qh" id="nlrs-amend-l">מה משנים</p><div class="nlrs__opts" role="group" aria-labelledby="nlrs-amend-l" data-g="amend">' + AMEND.map(function (x) { return tile('amend', x.k, x.he, ''); }).join('') + '</div></div>'
      + '<div data-v="years"><label class="nlrs__lab" for="nlrs-years">לכמה שנים נרשם המשכון</label><div class="nlrs__in"><input id="nlrs-years" inputmode="numeric" autocomplete="off" aria-describedby="nlrs-years-h"><span>שנים</span></div>'
      + '<span class="nlrs__help" id="nlrs-years-h">' + esc(ils(P.reg_counter.amount) + ' לכל שנה עד ' + P.paid_years_max + ' שנים בדלפק, ' + ils(P.reg_online.amount) + ' במקוון; מהשנה השישית אין אגרה.') + '</span><span class="nlrs__err" data-err="years" aria-live="polite"></span></div>'
      + '<div class="nlrs__q"><p class="nlrs__qh" id="nlrs-nes-l" data-neslab>נסח רישום</p><div class="nlrs__opts is-3" role="group" aria-labelledby="nlrs-nes-l" data-g="nes"></div></div>'
      + '<div class="nlrs__q" data-v="ex"><p class="nlrs__qh" id="nlrs-ex-l">פטור מאגרת רישום משכנתה</p><div class="nlrs__opts" role="group" aria-labelledby="nlrs-ex-l" data-g="ex">' + exTiles + '</div></div>'
      + '</div></div>'
      + '<div class="nlrs__res"><div class="nlrs__out" aria-live="polite"><p class="nlrs__msg" hidden></p><div class="nlrs__ok"><p class="nlrs__path"></p><span class="nlrs__ol"></span><div class="nlrs__fig"></div><p class="nlrs__sub"></p></div></div>'
      + '<div class="nlrs__sec"><h3 class="nlrs__sh">מה נרשם ואיפה <span class="nlrs__b" data-wb></span></h3><p class="nlrs__p" data-where></p></div>'
      + '<div class="nlrs__sec"><h3 class="nlrs__sh">האגרות ב־' + D.year + '</h3><ol class="nlrs__ls" aria-label="האגרות שורה אחרי שורה"></ol></div>'
      + '<div class="nlrs__sec" data-exsec hidden><h3 class="nlrs__sh">הפטור <span class="nlrs__b" data-exb></span></h3><div class="nlrs__exb"></div></div>'
      + '<div class="nlrs__sec"><h3 class="nlrs__sh">הזמן ומי משלם</h3><ul class="nlrs__ul" data-time></ul></div>'
      + '<div class="nlrs__sec"><h3 class="nlrs__sh">השלבים, לפי הסדר</h3><ol class="nlrs__st" data-steps></ol></div>'
      + '<div class="nlrs__btns"><button type="button" class="nlrs__btn is-primary" data-copy>העתקת הסיכום</button></div>'
      + '</div>'
      + '<div class="nlrs__call"><p data-ilacall hidden><b>' + esc('מוקד ' + D.ila.contact.body) + '</b>: <a class="nlrs__tel" href="tel:' + esc(D.ila.contact.phone) + '"><bdi dir="ltr">' + esc(D.ila.contact.phone) + '</bdi></a> או <bdi dir="ltr">' + esc(D.ila.contact.phone2) + '</bdi>, ימים ' + esc(D.ila.contact.days) + ', ' + esc(D.ila.contact.hours) + '. ' + chips([S('ila_guide')]) + '</p>'
      + '<p><b>' + esc('מוקד ' + C.body) + '</b></p>'
      + '<p><a class="nlrs__tel" href="tel:' + esc(C.phone) + '"><bdi dir="ltr">' + esc(C.phone) + '</bdi></a>, ' + esc(C.ext) + '. ימים ' + esc(C.days) + ', ' + esc(C.hours) + '. מחו״ל: <bdi dir="ltr">' + esc(C.abroad) + '</bdi>.</p>'
      + '<p>וואטסאפ: <bdi dir="ltr">' + esc(C.whatsapp) + '</bdi>. יש גם ' + esc(C.chat) + '.</p>'
      + '<p>לשכות: ' + esc(C.deed) + ', ימים ' + esc(C.deed_days) + ', ' + esc(C.deed_hours) + '; ' + esc(C.boxes) + '.</p>'
      + '<p class="nlrs__fine">' + esc(C.online) + '. ' + esc(C.manual) + '. ' + chips([S('gov_service')]) + '</p></div>'
      + '<div class="nlrs__more">'
      + '<div class="nlrs__sec"><h3 class="nlrs__sh">טופס רישום משכנתא: מה מגישים</h3><div class="nlrs__form-sheet">'
      + '<p class="nlrs__path" data-ckpath></p><p class="nlrs__p" data-cknote hidden></p><div data-ck></div>'
      + '<p class="nlrs__fine">את הטפסים הרשמיים מורידים מאתר הממשלה; אנחנו לא מעתיקים אותם ולא שומרים אותם כאן. הרשימה לפי תקנות המקרקעין (ניהול ורישום) והדפים שבמקורות.</p>'
      + '<div class="nlrs__btns"><button type="button" class="nlrs__btn" data-copyck>העתקת הרשימה</button><button type="button" class="nlrs__btn" data-print>הדפסה</button></div></div>'
      + '<ul class="nlrs__links"><li data-ilalink hidden><a href="' + esc(D.src.ila_guide.url) + '" target="_blank" rel="noopener">התחייבות לרישום משכנתא: דף השירות של רמ״י באתר הממשלה</a></li>'
      + '<li data-ilalink hidden><a href="' + esc(D.src.ila_form.url) + '" target="_blank" rel="noopener">' + esc(D.src.ila_form.title) + '</a></li>' + D.links.map(function (l) { var x = D.src[l.src]; return '<li><a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(l.he) + '</a></li>'; }).join('') + '</ul>'
      + '<p class="nlrs__fine">בדף השירות באתר הממשלה מקושרים גם: ' + esc(C.related.join('; ')) + '.</p></div>'
      + '<div class="nlrs__sec"><div class="nlrs__warn"><h3 class="nlrs__sh">מה לא אימתנו במסלול הזה</h3><ul class="nlrs__ul" data-unv></ul></div>'
      + '<p class="nlrs__fine" data-srcline></p>'
      + '<details class="nlrs__all"><summary>כל המקורות והתאריכים</summary><ul class="nlrs__links" data-all></ul></details></div>'
      + '</div></div></div>';
    root.innerHTML = h;
    var $ = function (s) { return root.querySelector(s); }, $$ = function (s) { return [].slice.call(root.querySelectorAll(s)); };
    var yi = $('#nlrs-years'); yi.value = String(v.years);
    var t = 0, last = null, wkeyLast = null, nkeyLast = null;
    yi.addEventListener('input', function () { v.years = yi.value; clearTimeout(t); t = setTimeout(paint, 90); });
    root.addEventListener('click', function (e) {
      var b = e.target && e.target.closest ? e.target.closest('button') : null; if (!b || !root.contains(b)) return;
      if (b.hasAttribute('data-s')) {
        var k = b.getAttribute('data-s'), val = b.getAttribute('data-val');
        if (k === 'reg' && (v.reg === 'none') !== (val === 'none')) v.nesach = 'auto';  // the extract of the pledge register is another thing: back to the default
        if (k === 'nes') v.nesach = val; else v[k] = val;
        if (k === 'reg' || k === 'act') { var o = whoOpts(v.reg, v.act); if (o.indexOf(v.who) < 0) v.who = o[0]; }
        paint();
      } else if (b.hasAttribute('data-copy') && last) {
        copy(b, copyText(last, D, location.origin + location.pathname + '#mrishum=' + enc(v)), 'העתקת הסיכום');
      } else if (b.hasAttribute('data-copyck') && last) {
        copy(b, checklistText(last, D), 'העתקת הרשימה');
      } else if (b.hasAttribute('data-print')) { G.print(); }
    });
    function copy(b, tx, lab) {
      var done = function () { b.textContent = 'הועתק'; setTimeout(function () { b.textContent = lab; }, 1600); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(tx).then(done, function () { G.prompt('העתיקו', tx); }); else G.prompt('העתיקו', tx);
    }
    $('[data-srcline]').innerHTML = esc(sourceLine(D)) + ' ' + chips([S('gov_fees'), S('reshumot_land'), S('reshumot_pledge')]);
    $('[data-all]').innerHTML = Object.keys(D.src).map(function (k) {
      var x = D.src[k], dt = [x.where, x.published ? 'פורסם ' + dmy(x.published) : '', x.updated ? 'עודכן ' + dmy(x.updated) : '', x.version ? 'נוסח ' + dmy(x.version) : '', x.read ? 'נקרא ' + dmy(x.read) : 'קישור בלבד'].filter(Boolean).join(', ');
      return '<li><a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.title) + '</a> <span class="nlrs__it">' + esc(dt + (x.how ? '. ' + x.how : '')) + '</span></li>';
    }).join('');

    function whoHelp(r) {
      if (r.reg === 'ila' && ending(r.act)) return 'את הבקשה לסלק מגישים לרמ״י, עם מסמך הסילוק של הבנק (נוהל 90.02B, סעיפים א.3 ו־ב).';
      if (r.act === 'cancel' && r.reg === 'tabu') return 'ידנית בלשכה: כשהבנק מסרב לקבל את התשלום, מפקידים את החוב אצל הרשם (תקנה 72).';
      if (ending(r.act)) return 'אחרי פירעון מלא הבנק מגיש את המחיקה (סעיף 9א).';
      if (r.reg === 'none') return 'ברשם המשכונות: במקוון ' + ils(P.reg_online.amount) + ' לשנה, בדלפק ' + ils(P.reg_counter.amount) + ' לשנה.';
      if (r.reg === 'ila') return r.act === 'amend' ? 'הבנק נותן מכתב הסכמה, ומגישים אותו לרמ״י; לא בקשה מקוונת (נוהל 90.02B, סעיף 1.5).' : 'ברמ״י הבקשה מקוונת בלבד, באזור האישי ״' + D.ila.area + '״, אחרי הזדהות ב' + D.ila.id + '.';
      return C.online + '. ' + C.manual + ', או בתיבות ההפקדה.';
    }
    function paint() {
      var r; try { r = compute(v, D); } catch (e) { r = err(null, 'לא הצלחנו לחשב עם הבחירות האלה.'); }
      // the tiles of step 3 and the extract follow the path
      var wo = whoOpts(v.reg, v.act), none = v.reg === 'none';
      var wkey = wo.join() + '|' + none + '|' + ending(v.act) + '|' + (v.reg === 'ila' && v.act === 'amend');  // redraw the tiles only when the set changes (keeps the keyboard focus)
      if (wkey !== wkeyLast) {
        wkeyLast = wkey;
        var wg = $('[data-g="who"]'); wg.className = 'nlrs__opts' + (wo.length === 1 ? ' is-1' : '');
        wg.innerHTML = wo.map(function (k) {
          var sub = k === 'owner' ? (ending(v.act) ? 'עם מסמך הסילוק של הבנק' : v.act === 'amend' ? 'עם מכתב ההסכמה של הבנק' : 'באזור האישי ״' + D.ila.area + '״') : k === 'rep' ? 'עם ייפוי כוח כדין' : k === 'lawyer' ? (none ? 'רשם המשכונות במקוון' : 'עם כרטיס חכם') : k === 'office' ? (ending(v.act) ? 'הבנק מסרב לקבל את התשלום' : (none ? 'בדלפק' : 'בלשכה, בדואר או בתיבה')) : 'הבנק מגיש את המחיקה';
          return tile('who', k, WHO[k], sub);
        }).join('');
      }
      $('[data-neslab]').textContent = none ? 'נסח מרשם המשכונות' : 'נסח רישום' + (v.reg === 'tabu' ? '' : ', אם הנכס רשום בטאבו');
      if (none !== nkeyLast) {
        nkeyLast = none;
        $('[data-g="nes"]').innerHTML = (none ? [['online', 'באינטרנט', ils(P.search_online.amount)], ['counter', 'בדלפק', ils(P.search_counter.amount)], ['none', 'בלי נסח', '']]
          : [['online', 'מקוון', ils(F.nesach_online.amount)], ['counter', 'בדלפק', ils(F.nesach_counter.amount)], ['none', 'בלי נסח', '']]).map(function (x) { return tile('nes', x[0], x[1], x[2]); }).join('');
      }
      var vis = { amend: v.act === 'amend' && v.reg === 'tabu', years: none && (v.act === 'register' || v.act === 'second'), ex: reging(v.act) };
      $$('[data-v]').forEach(function (x) { x.hidden = !vis[x.getAttribute('data-v')]; });
      var nesNow = r && !r.error ? r.nes : (v.nesach === 'auto' ? 'none' : v.nesach);
      $$('button[data-s]').forEach(function (x) {
        var k = x.getAttribute('data-s'), val = x.getAttribute('data-val');
        var cur = k === 'nes' ? nesNow : k === 'who' ? (r && !r.error ? r.who : v.who) : v[k];
        x.setAttribute('aria-pressed', String(val === cur));
      });
      $('[data-whohelp]').textContent = r && !r.error ? whoHelp(r) : '';
      $$('[data-ilacall], [data-ilalink]').forEach(function (x) { x.hidden = v.reg !== 'ila'; });
      $$('[data-err]').forEach(function (x) { x.textContent = ''; });
      var msg = $('.nlrs__msg'), ok = $('.nlrs__ok');
      if (r.error) {
        var fe = r.error.field && $('[data-err="' + r.error.field + '"]'); if (fe) fe.textContent = r.error.msg;
        msg.textContent = r.error.msg; msg.hidden = false; ok.hidden = true; return;
      }
      msg.hidden = true; ok.hidden = false; last = r;
      var hd = headline(r, D), fig = $('.nlrs__fig');
      $('.nlrs__path').textContent = pathText(r, D);
      $('.nlrs__ol').textContent = hd.label;
      fig.className = 'nlrs__fig' + (hd.text ? ' is-text' : ''); fig.innerHTML = '<bdi>' + esc(hd.value) + '</bdi>';
      var sp = $('.nlrs__sub'); sp.innerHTML = rich(hd.sub || ''); sp.hidden = !hd.sub;
      var w = whereText(r, D);
      $('[data-where]').innerHTML = rich(w.he) + ' ' + chips(w.src);
      var wb = $('[data-wb]'); wb.textContent = w.ok ? 'מאומת' : 'לא אומת במלואו'; wb.className = 'nlrs__b ' + (w.ok ? 'is-ok' : 'is-no');
      $('.nlrs__ls').innerHTML = r.lines.map(function (l) {
        var val = l.amt == null ? l.shown : ils(l.amt);
        return '<li class="is-' + l.kind + '"><span class="nlrs__lk">' + esc(l.label) + (l.item ? '<span class="nlrs__it">' + esc(itemText(l)) + '</span>' : '') + '</span>'
          + '<span class="nlrs__lv' + (l.amt == null ? ' is-txt' : '') + '"><bdi>' + esc(val) + '</bdi></span>' + (l.note ? '<span class="nlrs__ln">' + rich(l.note) + '</span>' : '')
          + chips(l.src.map(function (s) { return s.sec && s.sec === l.item ? { id: s.id, sec: '' } : s; })) + '</li>';  // the item is already printed under the label
      }).join('') + (!showTotal(r) ? '' : '<li class="is-total"><span class="nlrs__lk">לשלם למדינה' + (r.reg === 'company' || r.status === 'ilaout' || r.status === 'ilaamend' ? ', לפי מה שאומת' : '') + '</span><span class="nlrs__lv"><bdi>' + esc(ils(r.total)) + '</bdi></span></li>');
      // the exemption
      var es = $('[data-exsec]');
      if (r.ex) {
        var X = null; D.exemptions.forEach(function (x) { if (x.k === r.ex.k) X = x; });
        es.hidden = false;
        var eb = $('[data-exb]'); eb.textContent = r.ex.applies ? 'במסלול הזה: 0 ₪' : 'במסלול הזה: לא מוריד'; eb.className = 'nlrs__b ' + (r.ex.applies ? 'is-ex' : 'is-no');
        var EC = D.exempt_common;
        $('.nlrs__exb').className = 'nlrs__exb' + (r.ex.applies ? '' : ' is-no');
        $('.nlrs__exb').innerHTML = '<p class="nlrs__p"><b>' + esc(X.he + ', תקנה ' + X.reg) + '.</b> ' + esc(r.ex.applies ? 'אגרת רישום המשכנתה יורדת ל־0 ₪, במקום ' + ils(r.ex.saved) + ', אם אחד התנאים חל עליכם.' : r.ex.why) + '</p>'
          + '<p class="nlrs__mh">מי זכאי</p><ul class="nlrs__ul">' + X.conditions.map(function (c) { return '<li>' + esc(c.he) + ' ' + chips([S(c.src, c.sec)]) + '</li>'; }).join('')
          + '<li>' + esc(EC.spouse.he) + ' ' + chips([S('regs_fees', EC.spouse.sec)]) + '</li></ul>'
          + '<p class="nlrs__mh">איך מבקשים</p><ul class="nlrs__ul">' + X.how.map(function (c) { return '<li>' + esc(c.he) + (c.unverified ? ' (לא אומת)' : '') + ' ' + chips([S(c.src)]) + '</li>'; }).join('') + '</ul>'
          + '<p class="nlrs__fine">' + esc(EC.refund.he) + ' ' + chips([S('regs_fees', EC.refund.sec)]) + ' ' + esc(EC.scope.he) + '. ' + chips([S('mod_bereaved')]) + '</p>';
      } else es.hidden = true;
      $('[data-time]').innerHTML = timeList(r, D).map(function (x) { return '<li>' + rich(x.he) + ' ' + chips(x.src) + '</li>'; }).join('');
      $('[data-steps]').innerHTML = steps(r, D).map(function (x) { return '<li>' + rich(x.he) + ' ' + chips(x.src) + '</li>'; }).join('');
      var dc = docs(r, D);
      $('[data-ckpath]').textContent = pathText(r, D);
      var cn = $('[data-cknote]'); cn.textContent = dc.note; cn.hidden = !dc.note;
      $('[data-ck]').innerHTML = dc.items.map(function (x, i) { return '<label class="nlrs__ck"><input type="checkbox" id="nlrs-ck-' + i + '"><span>' + rich(x.he) + '</span>' + chips(x.src) + '</label>'; }).join('');
      $('[data-unv]').innerHTML = unverified(r, D).map(function (u) { return '<li>' + rich(u.he) + (/[.]$/.test(u.he) ? '' : '.') + '</li>'; }).join('');
    }
    paint();
    if (fromLink) {  // a shared case: open the switcher pane it lives in, then bring it into view
      var pane = root.closest ? root.closest('.nlmx-pane') : null;
      if (pane && pane.hidden && pane.id) { var chipB = document.querySelector('button[data-sw="' + pane.id + '"]'); if (chipB) chipB.click(); }
      if (root.scrollIntoView) root.scrollIntoView({ block: 'start' });
    }
  }
})();
