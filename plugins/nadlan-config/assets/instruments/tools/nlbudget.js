/* NadLan Instruments · nlbudget v1 (7.11.2026, HAD-678): "כמה עולה לשווק את הפרויקט" / "What it costs to market your project", the second
   instrument of the developer marketing page. LOCAL BUILD: staged in docs/research/2026-11-07-campaign-network/build/build-nlbudget/
   (README, node test, preview, browser check, registry snippet). Hebrew and English in this one file: the language comes from a data-lang
   attribute on the host (or an ancestor), else from the nearest lang attribute; "he" stays Hebrew, any other language is English.
   Every number comes from data/nlbudget.json (built by build_nlbudget_data.py from the teardown: value or range, unit, currency, scope,
   source name, URL, date, flag as union.md marks it, the verbatim evidence). The tool shows the source name and the flag next to every
   figure, gives ranges (never one false-precise number), and where no Israeli price was published it says so and takes the developer's
   own figure. Inputs: units for sale, average price, stage, who sells (commission rate: the developer's, no default), share sold abroad,
   sales period, leads per deal (the developer's, no default). Readouts: (1) the marketing-and-sales budget for the whole project from the
   percent-of-sales anchors, each bound named (the one survey figure); (2) advertising per apartment sold; (3) leads needed, only with the
   developer's own leads per deal, and their cost at three labelled bases. Then the budget sheet line by line, the spend by stage from the
   worked example abroad, and the big developers' published ad spend as a small sourced line. Copy as text and WhatsApp (text only).
   The state lives in memory only. Pure part in window.NLBUDGET (runs in node, takes the data as an argument).
   v1.1 (1.72.601, 7.11.2026): the budget sheet sits in a fold, "כל שורות התקציב (17)" / "All budget lines (17)": closed under 768 px
   (the tool was about 8,000 px tall on a 390 px phone), open on wider screens; a 44 px summary in the anchors panel's open/close look. */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;

  /* ------------------------------------------------------------------------------------------------------ the limits */
  var LIM = {
    units: { min: 1, max: 10000, dec: 0 }, price: { min: 100000, max: 200000000, dec: 0 }, abroad: { min: 0, max: 100, dec: 0 },
    months: { min: 1, max: 120, dec: 0 }, comm: { min: 0.1, max: 10, dec: 2 }, lpd: { min: 1, max: 2000, dec: 1 }, own: { min: 0, max: 1000000000, dec: 0 }
  };
  var STAGES = ['pre', 'launch', 'build', 'last'];
  var SELLERS = ['dev', 'co'];
  /* the percent-of-sales anchors shown on the project, Israel first */
  var ANCHORS = ['wedo_total', 'sp_sm', 'fe_mkt', 'fe_sm', 'ud_mkt', 'mf_mkt', 'pb_sm'];
  var FLAGS = { 'cited': 'cited', 'price list': 'list', 'agency claim': 'claim', 'agency claim, unnamed source': 'unnamed', 'example': 'example', 'own price': 'own', 'not published': 'np' };

  /* ------------------------------------------------------------------------------------------------------ the words */
  var STR = {
    he: {
      kicker: 'תקציב שיווק ליזמים', title: 'כמה עולה לשווק את הפרויקט', eg: 'דוגמה',
      lede: 'כתבו כמה דירות יש למכירה ובאיזה מחיר, ותראו את תקציב השיווק והמכירה של הפרויקט כטווח, את שורות התקציב אחת אחת ואת המקור של כל מספר.',
      egNote: 'הדוגמה של {src}: {units} דירות במחיר ממוצע של {price}. שנו את המספרים לפרויקט שלכם.',
      inLab: 'הפרויקט שלכם', outLab: 'התקציב',
      f_units: 'מספר דירות למכירה', h_units: 'הדירות שעוד לא נמכרו.', f_price: 'מחיר דירה ממוצע', salesLab: 'מחזור המכירות',
      f_stage: 'שלב הפרויקט', st_pre: 'טרום שיווק', st_launch: 'השקה', st_build: 'בבנייה', st_last: 'דירות אחרונות', st_all: 'כל השלבים',
      f_seller: 'מי מוכר', se_dev: 'צוות מכירות של היזם', se_co: 'חברת שיווק בעמלה',
      f_comm: 'שיעור העמלה שסיכמתם', h_comm: 'לא פורסם שיעור עמלה ישראלי לפרויקטים חדשים. כתבו את השיעור שלכם, באחוזים ממחזור המכירות.',
      f_abroad: 'חלק מהדירות לקונים מחו״ל', slider: 'חלק מהדירות לקונים מחו״ל, בגרירה',
      f_months: 'תקופת המכירה בחודשים', h_months: '{src}: חלון מכירה של {lo} עד {hi} חודשים ({flag}).',
      f_lpd: 'כמה פניות צריך לעסקה אחת', h_lpd: 'לא חובה, ואין ערך מוכן: כתבו את הנתון שלכם. בדוגמאות של משרדי שיווק: {ex}.',
      honesty: 'כל טווח מגיע עם המקור שלו ותאריך. טווח שמבוסס על טענה של משרד פרסום מסומן כך.',
      r1_dev: 'תקציב שיווק ומכירה, כל הפרויקט', r1_co: 'שיווק ועמלת חברת השיווק, כל הפרויקט',
      r1pct: '{lo} עד {hi} ממחזור המכירות של {v}', lowB: 'הגבול התחתון', highB: 'הגבול העליון', plusComm: '{a} לשיווק ועוד {c} עמלה שלכם',
      r1noComm: 'ועוד העמלה של חברת השיווק: כתבו את השיעור שלכם כדי לראות אותה בסכום.',
      r1year: 'בשנה, לפי {m} חודשי מכירה: {v}', r1mkt: 'מתוך זה שיווק בלבד: {v} ({pct}), {online} ממחזור המכירות ברשת',
      r2: 'פרסום לכל דירה שנמכרת', r2sub: 'פרסום בלבד, בלי צוות', r2all: 'לכל {n} הדירות: {v}', r2pct: '{lo} עד {hi} ממחיר דירה',
      r3: 'פניות שצריך לקמפיין', r3sub: 'לפי יחס סגירה שאתם קובעים', r3empty: 'כתבו כמה פניות לעסקה',
      r3calc: '{deals} עסקאות כפול {lpd} פניות לעסקה', r3split: 'בישראל {il}, מחו״ל {ab}', r3month: 'כ־{v} פניות בחודש, לפי {m} חודשים',
      leadsHead: 'כמה יעלו הפניות', l_list: 'לפי מחירון לידים בלעדיים', l_real: 'לפי עלות ליד בקמפיינים', l_us: 'קונים מחו״ל: מודעות חיפוש בארצות הברית',
      th_basis: 'לפי', th_per: 'לליד', th_n: 'פניות', th_tot: 'סך הכול',
      noAbroad: 'בחלוקה שבחרתם אין פניות מחו״ל.', noIl: 'בחלוקה שבחרתם אין פניות מישראל.', usNote: 'בדולרים, כפי שפורסם, בלי המרה. אין נתון ישראלי לקונים מחו״ל או לדירות חדשות.',
      anchHead: 'כל העוגנים שפורסמו, על הפרויקט שלכם', th_aSrc: 'מקור', th_aWhat: 'מה כלול', th_aPct: 'אחוז', th_aSum: 'בפרויקט שלכם',
      linesHead: 'כל שורות התקציב ({n})', tabHead: 'שורות התקציב', th_item: 'רכיב', th_range: 'טווח מחיר', th_when: 'מתי', th_src: 'מקור',
      ln_research: 'מחקר שוק, אסטרטגיה ותמחור', ln_brand: 'מיתוג וקריאייטיב: שם, שפה, חוברת מכירה', ln_ext3: 'הדמיות חוץ (3 זוויות)',
      ln_plan3d: 'תוכנית מכר בתלת ממד, לכל דירה', ln_film: 'סרט פרויקט, דקה עד 3 דקות', ln_tour: 'עמוד פרויקט עם סיור וירטואלי',
      ln_photo: 'צילום האתר לאורך הבנייה', ln_site: 'אתר ודפי נחיתה', ln_crm: 'ניהול פניות (CRM) ומעקב שיחות',
      ln_media: 'פרסום ממומן ברשת: Google, Meta, אתרי נדל״ן', ln_outdoor: 'שילוט חוצות וגדר האתר', ln_print: 'דפוס: חוברות, עלונים, עיתונות מקומית',
      ln_tv: 'רדיו וטלוויזיה', ln_pr: 'יחסי ציבור ו־SEO', ln_events: 'אירועים ותערוכות בחו״ל', ln_office: 'משרד מכירות ודירה לדוגמה',
      ln_fee: 'עמלת חברת השיווק', ln_fee_dev: 'צוות המכירות שלכם',
      noIl: 'לא פורסם מחיר ישראלי', own: 'המחיר שלכם', ownAria: 'המחיר שלכם: {x}', perUnitX: '{r} לדירה, כפול {n} דירות',
      included: 'כלול במנוי נדל״ן', plans: 'המנויים: שוק אחד {one} לשנה, שלושה שווקים {three} לשנה, פרויקט דגל {flag} לשנה',
      about: 'כ־{v}', ofSales: '{p} ממחזור המכירות', feeCalc: '{p} ממחזור המכירות, השיעור שלכם', feeNeed: 'כתבו את שיעור העמלה בנתוני הפרויקט.',
      now: 'בשלב שלכם', abroadEx: 'דוגמה מחו״ל', exPart: '{v} ל{part}, בפרויקט של {n} דירות',
      px_brand: 'מיתוג, חומרים ואתר', px_cgi: 'הדמיות וסרט', px_media: 'רשת, אתרי נדל״ן ומדיה ממומנת', px_sign: 'שילוט, גדר ודפוס',
      suiteRange: 'חלל תצוגה ומכירה: {lo} עד יותר מ־{hi}', t_ownNp: 'המחיר שלכם; לא פורסם מחיר ישראלי',
      sumLab: 'סך השורות עם מחיר', sumOpen: 'עוד {n} שורות בלי מחיר ישראלי שלא מילאתם.', sumOpen1: 'עוד שורה אחת בלי מחיר ישראלי שלא מילאתם.', sumAll: 'מילאתם את כל השורות שאין להן מחיר ישראלי.',
      sumNote: 'בלי המנוי של נדל״ן.',
      barsHead: 'איך התקציב מתפזר לאורך הפרויקט', b_pre: 'לפני ההשקה', b_post: 'מההשקה עד סוף המכירות', b_delay: 'עוד 12 חודשי מכירה',
      barsNote: 'בדוגמה: {n} דירות, שיווק של {total} ({pct} ממחזור המכירות). אין דוגמה ישראלית שפורסמה לפיזור לפי שלבים.',
      barsDelay: 'אם המכירה נמשכת עוד {m} חודשים, השיווק עולה ל־{total}, {pct} ממחזור המכירות במקום {was}.',
      timeIl: 'בישראל, משך השלבים: אסטרטגיה ומיתוג {a} שבועות, טרום שיווק {b} שבועות, פריסייל {c} שבועות, והשקה של שבוע אחד.',
      ctxHead: 'לעיון: פרסום של חברות הבנייה', million: '{v} מיליון ₪', almost: 'כמעט {v}',
      fl_cited: 'מקור מצוטט', fl_list: 'מחירון שפורסם', fl_claim: 'טענת משרד פרסום', fl_unnamed: 'טענת משרד, בלי שם המקור', fl_example: 'דוגמה של המקור',
      fl_own: 'המחיר של נדל״ן', fl_np: 'לא פורסם',
      abroad: 'חו״ל', vat_before: 'לפני מע״מ', vat_plus: 'בתוספת מע״מ', noDate: 'בלי תאריך, נקרא {d}',
      e_units: 'כתבו מספר דירות, מ־{min} עד {max}.', e_price: 'כתבו מחיר ממוצע, מ־{min} עד {max}.', e_abroad: 'כתבו אחוז מ־{min} עד {max}.',
      e_months: 'כתבו מספר חודשים, מ־{min} עד {max}.', e_comm: 'כתבו שיעור עמלה מ־{min} עד {max}.', e_lpd: 'כתבו מספר פניות מ־{min} עד {max}.',
      e_own: 'כתבו סכום בשקלים, או השאירו ריק.', fix: 'כתבו מספר דירות ומחיר ממוצע כדי לראות את התקציב.',
      copy: 'העתקת התקציב', copied: 'הועתק', copyPrompt: 'העתיקו את התקציב', wa: 'שליחה בוואטסאפ',
      shareHead: 'תקציב שיווק לפרויקט, לפי נדל״ן', t_proj: 'הפרויקט: {u} דירות, מחיר ממוצע {p}, מחזור מכירות {v}',
      t_set: 'שלב: {s}. מוכר: {w}. קונים מחו״ל: {a}.', t_months: 'תקופת מכירה: {n} חודשים.', t_lines: 'שורות התקציב:', t_src: 'המקור והסימון של כל מספר בעמוד:',
      t_lpd: '{n} פניות לעסקה'
    },
    en: {
      kicker: 'Marketing budget for developers', title: 'What it costs to market your project', eg: 'Example',
      lede: 'Enter how many apartments are for sale and at what price, and see the project\'s marketing and sales budget as a range, the budget lines one by one and the source of every number.',
      egNote: 'The {src} example: {units} apartments at an average of {price}. Change the numbers to your project.',
      inLab: 'Your project', outLab: 'The budget',
      f_units: 'Apartments for sale', h_units: 'The apartments not sold yet.', f_price: 'Average apartment price', salesLab: 'Sales value',
      f_stage: 'Project stage', st_pre: 'Pre-launch', st_launch: 'Launch', st_build: 'Construction', st_last: 'Last units', st_all: 'Every stage',
      f_seller: 'Who sells', se_dev: 'The developer\'s sales team', se_co: 'A marketing company on commission',
      f_comm: 'The commission rate you agreed', h_comm: 'No Israeli commission rate for new projects is published. Enter your own rate, as a percentage of sales value.',
      f_abroad: 'Share of apartments for buyers abroad', slider: 'Share of apartments for buyers abroad, slider',
      f_months: 'Sales period in months', h_months: '{src}: a sales window of {lo} to {hi} months ({flag}).',
      f_lpd: 'Leads needed for one deal', h_lpd: 'Optional, with no preset value: enter your own figure. In marketing firms\' examples: {ex}.',
      honesty: 'Every range comes with its source and date. A range based on an agency\'s own claim is marked as such.',
      r1_dev: 'Marketing and sales budget, whole project', r1_co: 'Marketing and the marketing company\'s commission, whole project',
      r1pct: '{lo} to {hi} of the sales value of {v}', lowB: 'Lower bound', highB: 'Upper bound', plusComm: '{a} for marketing plus your {c} commission',
      r1noComm: 'Plus the marketing company\'s commission: enter your rate to see it in the total.',
      r1year: 'A year, over {m} months of sales: {v}', r1mkt: 'Of this, marketing alone: {v} ({pct}), {online} of sales value online',
      r2: 'Advertising per apartment sold', r2sub: 'Advertising only, no sales team', r2all: 'For all {n} apartments: {v}', r2pct: '{lo} to {hi} of an apartment\'s price',
      r3: 'Leads the campaign needs', r3sub: 'From the close rate you set', r3empty: 'Enter leads per deal',
      r3calc: '{deals} deals times {lpd} leads per deal', r3split: 'In Israel {il}, abroad {ab}', r3month: 'About {v} leads a month, over {m} months',
      leadsHead: 'What the leads would cost', l_list: 'At an exclusive lead price list', l_real: 'At the cost per lead in campaigns', l_us: 'Buyers abroad: US search ads',
      th_basis: 'Basis', th_per: 'Per lead', th_n: 'Leads', th_tot: 'Total',
      noAbroad: 'Your split has no leads from abroad.', noIl: 'Your split has no leads from Israel.', usNote: 'In dollars, as published, not converted. No Israeli figure exists for buyers abroad or for new apartments.',
      anchHead: 'Every published anchor, on your project', th_aSrc: 'Source', th_aWhat: 'What it covers', th_aPct: 'Share', th_aSum: 'On your project',
      linesHead: 'All budget lines ({n})', tabHead: 'The budget lines', th_item: 'Line', th_range: 'Price range', th_when: 'When', th_src: 'Source',
      ln_research: 'Market research, strategy and pricing', ln_brand: 'Branding and creative: name, look, sales brochure', ln_ext3: 'Exterior renders (3 angles)',
      ln_plan3d: '3D sales plan, per apartment', ln_film: 'Project film, 1 to 3 minutes', ln_tour: 'Project page with a virtual tour',
      ln_photo: 'Photography through construction', ln_site: 'Website and landing pages', ln_crm: 'Lead handling (CRM) and call tracking',
      ln_media: 'Paid online ads: Google, Meta, property portals', ln_outdoor: 'Outdoor signs and the site fence', ln_print: 'Print: brochures, leaflets, local press',
      ln_tv: 'Radio and TV', ln_pr: 'PR and SEO', ln_events: 'Events and exhibitions abroad', ln_office: 'Sales office and model apartment',
      ln_fee: 'Marketing company commission', ln_fee_dev: 'Your sales team',
      noIl: 'No Israeli price published', own: 'Your price', ownAria: 'Your price: {x}', perUnitX: '{r} per apartment, times {n} apartments',
      included: 'Included in the NadLan plan', plans: 'The plans: One market {one} a year, Three markets {three} a year, Flagship {flag} a year',
      about: 'about {v}', ofSales: '{p} of sales value', feeCalc: '{p} of sales value, your rate', feeNeed: 'Enter the commission rate in the project details.',
      now: 'Your stage', abroadEx: 'Example abroad', exPart: '{v} for {part}, in a project of {n} apartments',
      px_brand: 'brand, collateral and website', px_cgi: 'renders and film', px_media: 'online, portals and paid media', px_sign: 'signage, hoarding and print',
      suiteRange: 'Display suite: {lo} to beyond {hi}', t_ownNp: 'your price; no Israeli price published',
      sumLab: 'Total of the priced lines', sumOpen: '{n} more lines without an Israeli price that you did not fill.', sumOpen1: 'One more line without an Israeli price that you did not fill.', sumAll: 'You filled every line that has no Israeli price.',
      sumNote: 'Without the NadLan plan.',
      barsHead: 'How the budget spreads over the project', b_pre: 'Before launch', b_post: 'From launch to sell-out', b_delay: '12 more months of sales',
      barsNote: 'In the example: {n} apartments, marketing of {total} ({pct} of sales value). No Israeli example of the spread by stage is published.',
      barsDelay: 'If the sale runs {m} more months, marketing rises to {total}, {pct} of sales value instead of {was}.',
      timeIl: 'In Israel, the stages take: strategy and branding {a} weeks, pre-launch {b} weeks, presale {c} weeks, and a launch of one week.',
      ctxHead: 'For reference: ad spend of the building companies', million: '₪{v} million', almost: 'almost {v}',
      fl_cited: 'Cited source', fl_list: 'Published price list', fl_claim: 'Agency claim', fl_unnamed: 'Agency claim, source not named', fl_example: 'The source\'s own example',
      fl_own: 'NadLan price', fl_np: 'Not published',
      abroad: 'abroad', vat_before: 'before VAT', vat_plus: 'plus VAT', noDate: 'no date, read {d}',
      e_units: 'Enter a number of apartments from {min} to {max}.', e_price: 'Enter an average price from {min} to {max}.', e_abroad: 'Enter a share from {min} to {max}.',
      e_months: 'Enter a number of months from {min} to {max}.', e_comm: 'Enter a commission rate from {min} to {max}.', e_lpd: 'Enter a number of leads from {min} to {max}.',
      e_own: 'Enter an amount in shekels, or leave it empty.', fix: 'Enter the apartments and the average price to see the budget.',
      copy: 'Copy the budget', copied: 'Copied', copyPrompt: 'Copy the budget', wa: 'Send on WhatsApp',
      shareHead: 'Project marketing budget, by NadLan', t_proj: 'The project: {u} apartments, average price {p}, sales value {v}',
      t_set: 'Stage: {s}. Who sells: {w}. Buyers abroad: {a}.', t_months: 'Sales period: {n} months.', t_lines: 'The budget lines:', t_src: 'The source and flag of every number on the page:',
      t_lpd: '{n} leads per deal'
    }
  };

  /* ------------------------------------------------------------------------------------------------------ the logic */
  function nfmt(n, lang, dec) { return new Intl.NumberFormat(lang === 'en' ? 'en-US' : 'he-IL', { maximumFractionDigits: dec == null ? 0 : dec }).format(dec ? +n || 0 : Math.round(+n || 0)); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function B(s) { return '<bdi>' + esc(s) + '</bdi>'; }
  function tpl(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o && o[k] != null ? o[k] : m; }); }
  function tplH(s, o) { return tpl(esc(s), o); }  // o: values that are HTML already
  function T(lang) { return STR[lang === 'en' ? 'en' : 'he']; }
  function r2(x) { return Math.round(x * 1e6) / 1e6; }
  /* a money figure in its own currency, as the source published it (no conversion) */
  function cur(n, c, lang) {
    var dec = n !== Math.round(n) ? 2 : 0, s = nfmt(n, lang, dec);
    if (c === 'USD') return '$' + s;
    if (c === 'AUD') return 'A$' + s;
    return lang === 'en' ? '₪' + s : s + ' ₪';
  }
  function pct(n, lang) { return nfmt(n, lang, 2) + '%'; }
  /* a range: Hebrew shekels share the sign at the end ("4,000 עד 6,000 ₪"), every other figure carries its own sign */
  function rng(lo, hi, c, lang, H) {
    var w = H ? B : function (x) { return x; }, j = lang === 'en' ? ' to ' : ' עד ';
    if (c === '%') return lo === hi ? w(pct(lo, lang)) : w(pct(lo, lang)) + j + w(pct(hi, lang));
    if (lo === hi) return H ? curH(lo, c, lang) : cur(lo, c, lang);
    if (lang !== 'en' && (c === 'ILS' || !c)) return w(nfmt(lo, lang, lo !== Math.round(lo) ? 2 : 0)) + j + w(nfmt(hi, lang, hi !== Math.round(hi) ? 2 : 0)) + ' ₪';
    return w(cur(lo, c, lang)) + j + w(cur(hi, c, lang));
  }
  /* one money figure as HTML: in Hebrew the shekel sign stays outside the isolate, so it sits after the number as Hebrew reads */
  function curH(n, c, lang) { return lang !== 'en' && (c === 'ILS' || !c) ? B(nfmt(n, lang, n !== Math.round(n) ? 2 : 0)) + ' ₪' : B(cur(n, c, lang)); }
  /* three significant figures; dir -1 rounds down, 1 up, 0 to the nearest: a range never claims more precision than its anchor */
  function nice(v, dir) {
    if (!(v > 0)) return 0;
    var e = Math.pow(10, Math.max(0, Math.floor(Math.log10(v)) - 2)), q = r2(v / e);
    return (dir < 0 ? Math.floor(q) : dir > 0 ? Math.ceil(q) : Math.round(q)) * e;
  }
  function parseNum(s) {
    if (typeof s === 'number') return s;
    var t = String(s == null ? '' : s).replace(/[\s,₪%$]/g, '');
    if (!t) return null;
    return /^\d+(\.\d+)?$/.test(t) ? parseFloat(t) : NaN;
  }
  function valid(f, v) {
    var L = LIM[f];
    if (typeof v !== 'number' || !isFinite(v) || v < L.min || v > L.max) return false;
    return L.dec ? r2(v * Math.pow(10, L.dec)) === Math.round(v * Math.pow(10, L.dec)) : v === Math.round(v);
  }
  function newState(D) {
    var x = (D && D.example) || {};
    return { units: x.units || null, price: x.price || null, stage: 'pre', seller: 'dev', comm: null, abroad: 0, months: x.months || null, lpd: null, own: {} };
  }
  function isExample(st, D) { return !!D && st.units === D.example.units && st.price === D.example.price; }
  /* the fields that are filled and wrong (optional fields may stay empty: null) */
  function errors(st) {
    var e = [];
    ['units', 'price'].forEach(function (f) { if (!valid(f, st[f])) e.push(f); });
    if (st.seller === 'co' && st.comm != null && !valid('comm', st.comm)) e.push('comm');
    if (!valid('abroad', st.abroad)) e.push('abroad');
    if (st.months != null && !valid('months', st.months)) e.push('months');
    if (st.lpd != null && !valid('lpd', st.lpd)) e.push('lpd');
    Object.keys(st.own || {}).forEach(function (k) { if (st.own[k] != null && !valid('own', st.own[k])) e.push('own:' + k); });
    return e;
  }
  function lo_(f) { return f.lo != null ? f.lo : f.v; }
  function hi_(f) { return f.hi != null ? f.hi : f.v; }
  /* how many leads make a deal in the sources' own worked examples (a hint, never a default) */
  function lpdExamples(D) {
    var F = D.figures, a = F.se_funnel, b = F.mi_funnel, out = [];
    a.inq.forEach(function (n, i) { out.push({ lpd: n / a.deals[i], fig: 'se_funnel' }); });
    out.push({ lpd: b.leads / b.deals, fig: 'mi_funnel' });
    return out;
  }
  /* everything the page shows, from the state and the data */
  function compute(st, D) {
    var F = D.figures, r = { err: errors(st), ok: false };
    if (!valid('units', st.units) || !valid('price', st.price)) return r;
    var U = st.units, P = st.price, V = U * P, co = st.seller === 'co', c = co && valid('comm', st.comm) ? st.comm : null, M = valid('months', st.months) ? st.months : null;
    r.ok = true; r.V = V; r.months = M;
    r.anchors = ANCHORS.map(function (id) { var f = F[id]; return { id: id, loPct: lo_(f), hiPct: hi_(f), lo: nice(V * lo_(f) / 100, -1), hi: nice(V * hi_(f) / 100, 1) }; });
    /* (1) the whole-project budget: the developer's team = Start Point's 2% to 4% (sales team and advertising included);
       a marketing company = marketing alone, WE DO MEDIA's 1% (Israel) to Feasly's 2% (abroad, marketing only), plus the developer's rate */
    var t = co ? { loPct: r2(F.wedo_total.v + (c || 0)), hiPct: r2(hi_(F.fe_mkt) + (c || 0)), lowFig: 'wedo_total', highFig: 'fe_mkt', comm: c, partial: c == null }
               : { loPct: lo_(F.sp_sm), hiPct: hi_(F.sp_sm), lowFig: 'sp_sm', highFig: 'sp_sm', comm: null, partial: false };
    t.lowAnchor = co ? F.wedo_total.v : lo_(F.sp_sm); t.highAnchor = co ? hi_(F.fe_mkt) : hi_(F.sp_sm);
    t.lo = nice(V * t.loPct / 100, -1); t.hi = nice(V * t.hiPct / 100, 1);
    if (M) { t.yearLo = nice(t.lo * 12 / M, -1); t.yearHi = nice(t.hi * 12 / M, 1); }
    r.total = t;
    r.mkt = { pct: F.wedo_total.v, v: nice(V * F.wedo_total.v / 100, 0), online: F.wedo_online.v };
    /* (2) advertising per apartment sold */
    var fu = F.sp_unit;
    r.unit = { lo: fu.lo, hi: fu.hi, totLo: fu.lo * U, totHi: fu.hi * U, pctLo: r2(fu.lo / P * 100), pctHi: r2(fu.hi / P * 100) };
    /* (3) leads, only with the developer's own leads per deal */
    r.leads = null;
    if (st.lpd != null && valid('lpd', st.lpd)) {
      var n = Math.ceil(r2(U * st.lpd)), ab = Math.round(n * (valid('abroad', st.abroad) ? st.abroad : 0) / 100), il = n - ab, fl = F.sp_leads, fr = F.se_cpl, fq = F.lq_cpl;
      r.leads = { n: n, il: il, ab: ab, deals: U, lpd: st.lpd, perMonth: M ? Math.round(n / M) : null, costs: [
        { k: 'list', fig: 'sp_leads', cur: 'ILS', n: il, per: [fl.lo, fl.hi], lo: nice(il * fl.lo, -1), hi: nice(il * fl.hi, 1) },
        { k: 'real', fig: 'se_cpl', cur: 'ILS', n: il, per: [fr.lo, fr.hi], lo: nice(il * fr.lo, -1), hi: nice(il * fr.hi, 1) },
        { k: 'us', fig: 'lq_cpl', cur: 'USD', n: ab, per: [fq.lo, fq.hi], lo: nice(ab * fq.lo, -1), hi: nice(ab * fq.hi, 1) }] };
    }
    /* the budget sheet */
    var sLo = 0, sHi = 0, open = 0;
    r.lines = D.lines.map(function (ln) {
      var f = ln.fig ? F[ln.fig] : null, o = { id: ln.id, kind: ln.kind, stage: ln.stage, fig: ln.fig || null, ctx: ln.ctx, lo: null, hi: null, cur: 'ILS', approx: false, needs: false,
        now: ln.stage.indexOf(st.stage) > -1 };
      if (ln.kind === 'once') { o.lo = f.lo; o.hi = f.hi; }
      else if (ln.kind === 'unit') { o.lo = f.lo * U; o.hi = f.hi * U; o.per = [f.lo, f.hi]; }
      else if (ln.kind === 'pct') { o.lo = o.hi = nice(V * f.v / 100, 0); o.approx = true; o.pct = f.v; }
      else if (ln.kind === 'fee' && co) { if (c != null) { o.lo = o.hi = Math.round(V * c / 100); o.pct = c; } else o.needs = true; }
      else if (ln.kind === 'own' || ln.kind === 'fee') { o.own = true; var v = st.own[ln.id]; if (v != null && valid('own', v)) { o.lo = o.hi = v; o.mine = true; } else o.needs = true; }
      if (o.lo != null) { sLo += o.lo; sHi += o.hi; }
      if (o.needs) open++;
      return o;
    });
    r.sum = { lo: sLo, hi: sHi, open: open };
    r.bars = spread(D); r.barNow = barNow(st.stage);
    return r;
  }
  /* the spread by stage: the worked example abroad (Feasly), the only published one; after launch = the total less the pre-launch part,
     the longer sale = the three additions of the source */
  function spread(D) {
    var F = D.figures, ex = F.fe_ex, pre = F.fe_pre.v, post = ex.total - pre, dl = F.fe_delay, add = dl.suite + dl.media + dl.creative;
    return [{ k: 'pre', v: pre, share: r2(pre / ex.total * 100) }, { k: 'post', v: post, share: r2(post / ex.total * 100) }, { k: 'delay', v: add, share: r2(add / ex.total * 100) }];
  }
  function barNow(stage) { return stage === 'pre' ? 'pre' : 'post'; }
  function flagKey(f) { return FLAGS[f.flag] || 'np'; }
  /* the flag inside a sentence: lower case in English ("(Mirai, the source's own example)") */
  function flagWord(f, lang) { var w = T(lang)['fl_' + flagKey(f)]; return lang === 'en' ? w.charAt(0).toLowerCase() + w.slice(1) : w; }
  function lastDate(s) { var p = String(s || '').split(' / '); return p[p.length - 1]; }
  function dmy(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? +p[2] + '.' + +p[1] + '.' + p[0] : String(iso || ''); }
  /* "Start Point, 5.11.2026 · Agency claim" (plain text) */
  function srcText(f, lang) {
    var t = T(lang), d = f.date ? dmy(lastDate(f.date)) : tpl(t.noDate, { d: dmy(f.retrieved) });
    return f[lang === 'en' ? 'src_en' : 'src_he'] + (f.scope === 'abroad' && !f.country ? ', ' + t.abroad : '') + ', ' + d + ' · ' + t['fl_' + flagKey(f)] + (f.vat ? ' · ' + t['vat_' + f.vat] : '');
  }
  function srcHTML(f, lang) {
    var t = T(lang), d = f.date ? B(dmy(lastDate(f.date))) : tplH(t.noDate, { d: B(dmy(f.retrieved)) });
    return '<span class="nlbg__src"><span dir="auto">' + esc(f[lang === 'en' ? 'src_en' : 'src_he']) + '</span>' + (f.scope === 'abroad' && !f.country ? ', ' + esc(t.abroad) : '') + ', ' + d
      + ' <i class="nlbg__flag is-' + flagKey(f) + '">' + esc(t['fl_' + flagKey(f)]) + '</i>' + (f.vat ? ' <span class="nlbg__vat">' + esc(t['vat_' + f.vat]) + '</span>' : '') + '</span>';
  }
  function stageText(stages, lang) { var t = T(lang); return stages.map(function (s) { return t['st_' + s]; }).join(', '); }
  function lineName(id, st, lang) { var t = T(lang); return id === 'fee' && st.seller !== 'co' ? t.ln_fee_dev : t['ln_' + id]; }
  /* the range of one line as text or HTML */
  function lineRange(o, lang, H) {
    var t = T(lang);
    if (o.kind === 'plan') return H ? esc(t.included) : t.included;
    if (o.lo == null) return H ? esc(t.noIl) : t.noIl;
    var r = rng(o.lo, o.hi, o.cur, lang, H);
    return o.approx ? (H ? tplH(t.about, { v: r }) : tpl(t.about, { v: r })) : r;
  }
  function plansText(D, lang, H) {
    var p = D.figures.nl_plans.plans, w = H ? function (n) { return curH(n, 'ILS', lang); } : function (n) { return cur(n, 'ILS', lang); };
    return (H ? tplH : tpl)(T(lang).plans, { one: w(p.one), three: w(p.three), flag: w(p.flag) });
  }
  /* the copied / WhatsApp text: the inputs, the three readouts, every line with its source and flag; text only */
  function summaryText(st, D, lang, url) {
    var t = T(lang), r = compute(st, D), F = D.figures, out = [t.shareHead], RL = lang === 'en' ? '' : '‏';
    if (!r.ok) { out.push(t.fix); if (url) out.push(url); return out.join('\n'); }
    out.push(tpl(t.t_proj, { u: nfmt(st.units, lang), p: cur(st.price, 'ILS', lang), v: cur(r.V, 'ILS', lang) }));
    out.push(tpl(t.t_set, { s: t['st_' + st.stage], w: t['se_' + st.seller] + (st.seller === 'co' && r.total.comm != null ? ' (' + pct(r.total.comm, lang) + ')' : ''), a: pct(valid('abroad', st.abroad) ? st.abroad : 0, lang) })
      + (r.months ? ' ' + tpl(t.t_months, { n: r.months }) : '') + (r.leads ? ' ' + tpl(t.t_lpd, { n: nfmt(r.leads.lpd, lang, 1) }) + '.' : ''));
    var T1 = r.total;
    out.push((st.seller === 'co' ? t.r1_co : t.r1_dev) + ': ' + rng(T1.lo, T1.hi, 'ILS', lang) + ' (' + rng(T1.loPct, T1.hiPct, '%', lang) + ': ' + srcText(F[T1.lowFig], lang) + (T1.highFig !== T1.lowFig ? '; ' + srcText(F[T1.highFig], lang) : '') + ')' + RL);
    if (T1.partial) out.push(t.r1noComm);
    if (T1.yearLo != null) out.push(tpl(t.r1year, { m: r.months, v: rng(T1.yearLo, T1.yearHi, 'ILS', lang) }));
    out.push(t.r2 + ': ' + rng(r.unit.lo, r.unit.hi, 'ILS', lang) + '. ' + tpl(t.r2all, { n: nfmt(st.units, lang), v: rng(r.unit.totLo, r.unit.totHi, 'ILS', lang) }) + ' (' + srcText(F.sp_unit, lang) + ')' + RL);
    if (r.leads) {
      out.push(t.r3 + ': ' + nfmt(r.leads.n, lang) + ' (' + tpl(t.r3calc, { deals: nfmt(r.leads.deals, lang), lpd: nfmt(r.leads.lpd, lang, 1) }) + ')');
      r.leads.costs.forEach(function (x) { if (x.n) out.push('· ' + t['l_' + x.k] + ': ' + rng(x.lo, x.hi, x.cur, lang) + ' (' + srcText(F[x.fig], lang) + ')' + RL); });
    }
    out.push(t.t_lines);
    r.lines.forEach(function (o) {
      var src = o.fig ? ' (' + srcText(F[o.fig], lang) + ')' + RL : (o.mine ? ' (' + t.t_ownNp + ')' : '');
      out.push('· ' + lineName(o.id, st, lang) + ': ' + lineRange(o, lang) + src);
    });
    out.push(t.sumLab + ': ' + rng(r.sum.lo, r.sum.hi, 'ILS', lang) + '. ' + t.sumNote);
    if (url) { out.push(t.t_src); out.push(url); }
    return out.join('\n');
  }
  function waUrl(text) { return 'https://wa.me/?text=' + encodeURIComponent(text); }

  var NLBUDGET = { LIM: LIM, STAGES: STAGES, SELLERS: SELLERS, ANCHORS: ANCHORS, FLAGS: FLAGS, STR: STR,
    nfmt: nfmt, esc: esc, tpl: tpl, flagKey: flagKey, flagWord: flagWord, cur: cur, curH: curH, pct: pct, rng: rng, nice: nice, parseNum: parseNum, valid: valid, newState: newState, isExample: isExample, errors: errors,
    lpdExamples: lpdExamples, compute: compute, spread: spread, barNow: barNow, srcText: srcText, stageText: stageText, lineName: lineName, lineRange: lineRange, plansText: plansText,
    summaryText: summaryText, waUrl: waUrl };
  G.NLBUDGET = NLBUDGET;
  if (typeof document === 'undefined' || !G.NadLanInstruments) return;  // node: the logic only

  /* ===================================================================================================== the page */
  var ICON = {
    copy: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 7h9v10H7z"/><path d="M4 13V3h9"/></svg>',
    wa: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16l1-3.2A7 7 0 1 1 7.6 15z"/></svg>'
  };
  G.NadLanInstruments.register('nlbudget', { custom: function (root, data) { mount(root, data && data.nlbudget); } });

  function langFor(root) {
    var d = root.closest('[data-lang]'), a = (d && d.getAttribute('data-lang')) || '';
    if (!a) { var l = root.closest('[lang]'); a = (l && l.getAttribute('lang')) || document.documentElement.getAttribute('lang') || 'he'; }
    return /^(he|iw)\b/i.test(a) ? 'he' : 'en';
  }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }

  function css() {
    if (document.getElementById('nlbg-css')) return;
    var s = document.createElement('style'); s.id = 'nlbg-css';
    s.textContent = [
      /* the NadLan Instruments tokens of core.css (.nli); the live theme restyles buttons, inputs, labels, tables and headings, so the rules
         that must hold carry html body .nli .nlbg and, where the theme insists, !important */
      '.nlbg[dir="rtl"]{direction:rtl}.nlbg[dir="ltr"]{direction:ltr}',
      '.nlbg[lang="en"]{--nli-sans:"IBM Plex Sans","IBM Plex Sans Hebrew",system-ui,sans-serif;--nli-display:"IBM Plex Sans Condensed","IBM Plex Sans",system-ui,sans-serif}',
      'html body .nli .nlbg[lang="en"] h2.nli__title{font:600 36px/40px var(--nli-display) !important;letter-spacing:-.01em}',
      '@media (max-width:520px){html body .nli .nlbg[lang="en"] h2.nli__title{font-size:30px !important;line-height:34px !important}}',
      '.nlbg bdi{font-family:var(--nli-mono);font-variant-numeric:tabular-nums;white-space:nowrap}',
      'html body .nli .nlbg .nlbg__hd{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;margin:0 0 8px;position:relative}',
      'html body .nli .nlbg .nlbg__hd h2.nli__title{margin:0 !important}',
      '.nlbg .nlbg__eg{flex:none;padding-bottom:6px;font:500 13px/18px var(--nli-mono);color:var(--nli-mute)}',
      'html body .nli .nlbg .nlbg__lede{font:400 16px/26px var(--nli-sans);color:var(--nli-ink2);margin:0 0 20px;max-width:68ch;position:relative}',
      '.nlbg .nlbg__grid{display:grid;grid-template-columns:minmax(0,1fr);gap:20px;position:relative}',
      '@media (min-width:960px){.nlbg .nlbg__grid{grid-template-columns:minmax(0,360px) minmax(0,1fr);gap:28px;align-items:start}}',
      /* the inputs panel */
      'html body .nli .nlbg form.nlbg__in{display:grid;gap:16px;align-content:start;margin:0;padding:16px;border:1px solid var(--nli-line);border-radius:var(--nli-r-m);background:var(--nli-ground);min-width:0}',
      'html body .nli .nlbg h3.nlbg__h{font:600 17px/24px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 !important;letter-spacing:0 !important;text-transform:none !important}',
      'html body .nli .nlbg .nli__f>label,html body .nli .nlbg fieldset.nlbg__set>legend{font:500 14px/20px var(--nli-sans) !important;color:var(--nli-ink2) !important;margin:0 !important;padding:0}',
      'html body .nli .nlbg .nli__in input{font-family:var(--nli-mono) !important;border-radius:0 !important;min-height:46px}',
      'html body .nli .nlbg[dir="ltr"] .nli__in input{text-align:left}',
      'html body .nli .nlbg .nli__in:has(input[aria-invalid="true"]){border-color:var(--nli-ink);outline:1px solid var(--nli-ink);outline-offset:-2px}',
      '.nlbg .nlbg__help{font:400 13px/19px var(--nli-sans);color:var(--nli-mute);margin:0}',
      '.nlbg .nlbg__val{font:400 14px/20px var(--nli-sans);color:var(--nli-ink2);margin:0}',
      '.nlbg .nlbg__msg{font:500 14px/20px var(--nli-sans);color:var(--nli-ink);margin:0}',
      '.nlbg .nlbg__msg:not(:empty){padding:8px 12px;background:var(--nli-surface);border-inline-start:3px solid var(--nli-sea-deep)}',
      'html body .nli .nlbg fieldset.nlbg__set{border:0 !important;margin:0 !important;padding:0 !important;min-width:0;background:none !important;display:grid;gap:8px}',
      '.nlbg .nlbg__pills{display:flex;flex-wrap:wrap;gap:6px}',
      'html body .nli .nlbg label.nlbg__pill{position:relative;display:inline-flex;align-items:center;min-height:44px;padding:8px 14px;border:1px solid var(--nli-line);border-radius:999px;background:var(--nli-surface);color:var(--nli-ink);font:500 14px/20px var(--nli-sans) !important;cursor:pointer;margin:0}',
      'html body .nli .nlbg label.nlbg__pill:hover{border-color:var(--nli-sea)}',
      'html body .nli .nlbg label.nlbg__pill input{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:pointer}',
      'html body .nli .nlbg label.nlbg__pill:has(input:checked){background:var(--nli-sea);border-color:var(--nli-sea);color:var(--nli-on-sea) !important}',
      '.nlbg .nlbg__pill:has(input:focus-visible){outline:2px solid var(--nli-focus);outline-offset:2px}',
      'html body .nli .nlbg input.nlbg__range{display:block;width:100%;height:44px;margin:0;padding:0 !important;border:0 !important;background:transparent !important;box-shadow:none !important;accent-color:var(--nli-sea);cursor:pointer}',
      '.nlbg .nlbg__honest{font:400 12px/18px var(--nli-mono);color:var(--nli-mute);margin:0}',
      /* the readouts */
      '.nlbg .nlbg__out{display:grid;gap:16px;min-width:0}',
      '.nlbg .nlbg__reads{display:grid;grid-template-columns:minmax(0,1fr);gap:12px}',
      '@media (min-width:700px){.nlbg .nlbg__reads{grid-template-columns:repeat(2,minmax(0,1fr))}.nlbg .nlbg__reads>.is-main{grid-column:1 / -1}}',
      '.nlbg .nlbg__card{display:grid;gap:6px;align-content:start;padding:16px;border:1px solid var(--nli-line);border-radius:var(--nli-r-m);background:var(--nli-surface);min-width:0}',
      '.nlbg .nlbg__card>span{font:400 14px/20px var(--nli-sans);color:var(--nli-mute)}',
      '.nlbg .nlbg__fig{display:block;justify-self:start;font:500 24px/32px var(--nli-mono);color:var(--nli-ink);font-variant-numeric:tabular-nums}',
      '.nlbg .nlbg__fig.is-text{font:500 16px/24px var(--nli-sans);color:var(--nli-ink2)}',
      '.nlbg .nlbg__fig.is-survey{border-bottom:2px solid var(--nli-survey);padding-bottom:2px}',
      '@media (min-width:520px){.nlbg .nlbg__fig{font-size:28px;line-height:36px}.nlbg .is-main .nlbg__fig{font-size:32px;line-height:40px}}',
      '.nlbg .nlbg__sub{font:400 13px/20px var(--nli-sans);color:var(--nli-mute);margin:0}',
      '.nlbg .nlbg__wide{display:grid;gap:16px;margin-top:20px;min-width:0}',
      'html body .nli .nlbg table.is-sheet{table-layout:fixed}.nlbg col.c1{width:24%}.nlbg col.c2{width:24%}.nlbg col.c3{width:14%}.nlbg col.c4{width:38%}',
      'html body .nli .nlbg table.nlbg__t td{overflow-wrap:break-word}',
      '.nlbg .nlbg__line{font:400 14px/22px var(--nli-sans);color:var(--nli-ink2);margin:0}',
      'html body .nli .nlbg dl.nlbg__bd{margin:4px 0 0;display:grid;border-top:1px solid var(--nli-line)}',
      'html body .nli .nlbg dl.nlbg__bd>div{display:grid;grid-template-columns:minmax(0,7.5em) minmax(0,1fr);gap:2px 12px;padding:6px 0;border-bottom:1px solid var(--nli-line)}',
      'html body .nli .nlbg dl.nlbg__bd dt{font:500 13px/20px var(--nli-sans);color:var(--nli-mute);margin:0}',
      'html body .nli .nlbg dl.nlbg__bd dd{font:400 14px/20px var(--nli-sans);color:var(--nli-ink);margin:0;min-width:0}',
      '.nlbg .nlbg__src{font:400 13px/20px var(--nli-sans);color:var(--nli-mute)}',
      '.nlbg .nlbg__src bdi{font-size:12px}',
      '.nlbg .nlbg__flag{font-style:normal;display:inline-block;padding:0 6px;border:1px solid var(--nli-line);border-radius:999px;font:500 12px/18px var(--nli-sans);color:var(--nli-ink2);white-space:nowrap}',
      '.nlbg .nlbg__flag.is-claim,.nlbg .nlbg__flag.is-unnamed{border-style:dashed;border-color:var(--nli-ink2)}',
      '.nlbg .nlbg__flag.is-cited,.nlbg .nlbg__flag.is-list{border-color:var(--nli-sea);color:var(--nli-sea-deep)}',
      '.nlbg .nlbg__flag.is-own{border-color:var(--nli-open);color:var(--nli-ink)}',
      '.nlbg .nlbg__vat{white-space:nowrap}',
      /* tables (the budget sheet, the leads, the anchors) */
      '.nlbg .nlbg__box{border:1px solid var(--nli-line);border-radius:var(--nli-r-m);background:var(--nli-surface);overflow:hidden;min-width:0}',
      'html body .nli .nlbg table.nlbg__t{width:100%;border-collapse:collapse;margin:0;border:0 !important;background:none !important;font:400 14px/20px var(--nli-sans)}',
      'html body .nli .nlbg table.nlbg__t caption{caption-side:top;text-align:start;padding:12px 14px 8px;font:600 16px/24px var(--nli-sans);color:var(--nli-ink)}',
      'html body .nli .nlbg table.nlbg__t th{font:500 13px/18px var(--nli-sans) !important;color:var(--nli-ink2) !important;text-align:start !important;padding:8px 14px !important;border:0 !important;border-bottom:1px solid var(--nli-line) !important;background:none !important;text-transform:none !important;letter-spacing:0 !important}',
      'html body .nli .nlbg table.nlbg__t td{padding:10px 14px !important;border:0 !important;border-bottom:1px solid var(--nli-line) !important;background:none !important;color:var(--nli-ink) !important;vertical-align:top;text-align:start !important;font:400 14px/20px var(--nli-sans) !important}',
      'html body .nli .nlbg table.nlbg__t tr.is-now td{background:var(--nli-ground) !important}',
      'html body .nli .nlbg table.nlbg__t tr.is-now td:first-child{box-shadow:none !important;border-inline-start:3px solid var(--nli-sea) !important}',
      'html body .nli .nlbg table.nlbg__t td.r bdi{font-size:14px}',
      'html body .nli .nlbg table.nlbg__t tfoot td{font-weight:500 !important;border-bottom:0 !important}',
      '.nlbg td .nlbg__src,.nlbg td .nlbg__sub{display:block;margin-top:4px}',
      '.nlbg .nlbg__ctx{display:block;margin-top:6px;padding-top:6px;border-top:1px dashed var(--nli-line);font:400 13px/20px var(--nli-sans);color:var(--nli-ink2)}',
      '.nlbg .nlbg__tag{display:inline-block;margin-top:4px;padding:0 8px;border-radius:999px;background:var(--nli-sea);color:var(--nli-on-sea);font:500 12px/18px var(--nli-sans)}',
      '.nlbg .nlbg__np{color:var(--nli-ink2)}',
      'html body .nli .nlbg .nlbg__own{margin-top:6px;min-height:44px;max-width:220px}',
      'html body .nli .nlbg .nlbg__own input{min-height:42px !important;font-size:15px !important}',
      'html body .nli .nlbg .nlbg__own input::placeholder{font-family:var(--nli-sans);color:var(--nli-mute);opacity:1}',
      'html body .nli .nlbg a.nlbg__plans{display:block;min-height:44px;padding:12px 0 0;color:var(--nli-sea) !important;text-decoration:underline;text-underline-offset:3px;font:500 13px/20px var(--nli-sans)}',
      '@media (max-width:700px){html body .nli .nlbg table.nlbg__t,html body .nli .nlbg table.nlbg__t tbody,html body .nli .nlbg table.nlbg__t tfoot,html body .nli .nlbg table.nlbg__t tr,html body .nli .nlbg table.nlbg__t td{display:block !important;width:auto !important}'
        + 'html body .nli .nlbg table.nlbg__t caption{display:block}html body .nli .nlbg table.nlbg__t thead{display:none !important}'
        + 'html body .nli .nlbg table.nlbg__t tr{padding:10px 14px;border-bottom:1px solid var(--nli-line)}html body .nli .nlbg table.nlbg__t td{padding:2px 0 !important;border:0 !important}'
        + 'html body .nli .nlbg table.nlbg__t tr.is-now{background:var(--nli-ground)}html body .nli .nlbg table.nlbg__t tr.is-now td{background:none !important}html body .nli .nlbg table.nlbg__t tr.is-now td:first-child{border:0 !important}'
        + 'html body .nli .nlbg table.nlbg__t tr.is-now{border-inline-start:3px solid var(--nli-sea)}'
        + '.nlbg td[data-o="s"]>.nlbg__src:first-child{display:inline}html body .nli .nlbg table.nlbg__t td:first-child{font-weight:500 !important}html body .nli .nlbg table.nlbg__t td[data-th]:not(:first-child)::before{content:attr(data-th) ": ";color:var(--nli-mute);font-size:13px}}',
      'html body .nli .nlbg details.nlbg__anch,html body .nli .nlbg details.nlbg__lines{border:1px solid var(--nli-line);border-radius:var(--nli-r-m);background:var(--nli-surface);padding:0}',
      'html body .nli .nlbg details.nlbg__anch>summary,html body .nli .nlbg details.nlbg__lines>summary{min-height:44px;display:flex;align-items:center;gap:12px;padding:0 14px;font:500 15px/22px var(--nli-sans);color:var(--nli-sea);cursor:pointer;list-style:none}',
      '.nlbg details.nlbg__anch>summary::-webkit-details-marker,.nlbg details.nlbg__lines>summary::-webkit-details-marker{display:none}',
      '.nlbg details.nlbg__anch>summary::after,.nlbg details.nlbg__lines>summary::after{content:"";flex:none;width:8px;height:8px;margin-inline-start:auto;margin-top:-4px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg)}',
      '.nlbg details.nlbg__anch[open]>summary::after,.nlbg details.nlbg__lines[open]>summary::after{margin-top:4px;transform:rotate(-135deg)}',
      /* v1.1: the budget lines' fold; the sheet inside keeps its table, without a second frame; its caption is read, not shown twice */
      'html body .nli .nlbg details.nlbg__lines>.nlbg__box{border:0;border-top:1px solid var(--nli-line);border-radius:0}',
      'html body .nli .nlbg details.nlbg__lines table.nlbg__t caption{position:absolute !important;width:1px;height:1px;padding:0 !important;overflow:hidden;clip-path:inset(50%);white-space:nowrap}',
      '.nlbg .nlbg__note{font:400 13px/20px var(--nli-sans);color:var(--nli-ink2);margin:0;padding:10px 14px}',
      /* the spread by stage */
      '.nlbg .nlbg__bars{display:grid;gap:10px;padding:16px;border:1px solid var(--nli-line);border-radius:var(--nli-r-m);background:var(--nli-surface)}',
      '.nlbg .nlbg__bh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:4px 12px}',
      'html body .nli .nlbg .nlbg__bh h3{font:600 16px/24px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 !important;letter-spacing:0;text-transform:none}',
      '.nlbg .nlbg__bh span{font:500 12px/18px var(--nli-sans);color:var(--nli-mute)}',
      '.nlbg .nlbg__cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;align-items:end;height:150px}',
      '.nlbg .nlbg__col{display:flex;flex-direction:column;justify-content:flex-end;gap:4px;height:100%;min-width:0}',
      '.nlbg .nlbg__col b{display:block;background:var(--nli-sea);border-radius:1px 1px 0 0;min-height:4px}',
      '.nlbg .nlbg__col.is-now b{background:var(--nli-sea-deep)}',
      '.nlbg .nlbg__col.is-delay b{background:var(--nli-surface);border:2px dashed var(--nli-sea);border-bottom:0}',
      '.nlbg .nlbg__col em{font:500 13px/18px var(--nli-mono);font-style:normal;color:var(--nli-ink);text-align:center}',
      '.nlbg .nlbg__labs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;font:400 13px/18px var(--nli-sans);color:var(--nli-ink2);text-align:center}',
      '.nlbg .nlbg__labs .is-now{color:var(--nli-ink);font-weight:500}',
      /* the context line and sharing */
      '.nlbg .nlbg__strip{font:400 13px/21px var(--nli-sans);color:var(--nli-ink2);margin:0;padding:12px 0 0;border-top:1px solid var(--nli-line)}',
      '.nlbg .nlbg__strip b{font-weight:500;color:var(--nli-ink)}',
      'html body .nli .nlbg .nli__share{margin-top:0}',
      'html body .nli .nlbg .nli__share button,html body .nli .nlbg .nli__share a{font-family:var(--nli-sans) !important;letter-spacing:0 !important;text-transform:none !important;box-shadow:none !important}',
      '@media print{.nlbg .nli__share,.nlbg .nlbg__own input{display:none !important}.nlbg details.nlbg__anch{display:block}}'
    ].join('\n');
    document.head.appendChild(s);
  }

  function mount(root, D) {
    var LG = langFor(root), t = T(LG), DIR = LG === 'he' ? 'rtl' : 'ltr';
    if (!D || !D.figures) { root.innerHTML = '<p class="nli__note">' + esc(G.NadLanInstruments.TX && G.NadLanInstruments.TX.noData ? G.NadLanInstruments.TX.noData[LG] || '' : '') + '</p>'; return; }
    css();
    var F = D.figures, uid = 'nlbg-' + Math.random().toString(36).slice(2, 7), st = newState(D), msg = {};
    root.innerHTML = ''; root.setAttribute('dir', DIR);
    var P = el('div', 'nli__panel nlbg'); P.id = uid; P.setAttribute('dir', DIR); P.setAttribute('lang', LG);
    var ex = F.se_ex;
    P.innerHTML = '<header class="nlbg__hd"><div><p class="nli__kicker">' + esc(t.kicker) + '</p><h2 class="nli__title">' + esc(t.title) + '</h2></div><span class="nlbg__eg" data-o="eg">' + esc(t.eg) + '</span></header>'
      + '<p class="nlbg__lede">' + esc(t.lede) + '</p>'
      + '<div class="nlbg__grid"><form class="nlbg__in" novalidate aria-labelledby="' + uid + '-in"><h3 class="nlbg__h" id="' + uid + '-in">' + esc(t.inLab) + '</h3></form>'
      + '<section class="nlbg__out" aria-label="' + esc(t.outLab) + '"></section></div><div class="nlbg__wide"></div>';
    root.appendChild(P);
    var form = P.querySelector('form'), out = P.querySelector('.nlbg__out'), wide = P.querySelector('.nlbg__wide'), egTag = P.querySelector('[data-o="eg"]');
    form.addEventListener('submit', function (e) { e.preventDefault(); });

    function msgSlot(f) { var m = el('p', 'nlbg__msg'); m.id = uid + '-e-' + f; m.setAttribute('aria-live', 'polite'); msg[f] = m; return m; }
    function errText(f) { var L = LIM[f], c = f === 'price' ? function (n) { return cur(n, 'ILS', LG); } : f === 'abroad' || f === 'comm' ? function (n) { return pct(n, LG); } : function (n) { return nfmt(n, LG); };
      return tpl(t['e_' + f], { min: c(L.min), max: c(L.max) }); }
    /* one number field: label, input (+ unit), help, message */
    function numField(f, label, opt) {
      var w = el('div', 'nli__f'), id = uid + '-' + f;
      w.innerHTML = '<label for="' + id + '">' + esc(label) + '</label><div class="nli__in"><input id="' + id + '" data-f="' + f + '" type="text" inputmode="' + (opt.im || 'numeric') + '" autocomplete="off" maxlength="16"'
        + (opt.ph ? ' placeholder="' + esc(opt.ph) + '"' : '') + ' aria-describedby="' + (opt.help ? id + '-h ' : '') + uid + '-e-' + f + '">' + (opt.unit ? '<span class="nli__unit">' + esc(opt.unit) + '</span>' : '') + '</div>'
        + (opt.help ? '<p class="nlbg__help" id="' + id + '-h">' + opt.help + '</p>' : '');
      if (opt.after) w.appendChild(opt.after);
      w.appendChild(msgSlot(f));
      var inp = w.querySelector('input');
      inp.value = st[f] == null ? '' : nfmt(st[f], LG, LIM[f].dec);
      inp.addEventListener('input', function () { var v = parseNum(inp.value); st[f] = v; check(f, inp); paint(); if (opt.onInput) opt.onInput(); });
      inp.addEventListener('blur', function () { if (st[f] != null && valid(f, st[f])) inp.value = nfmt(st[f], LG, LIM[f].dec); });
      return w;
    }
    function check(f, inp) {
      var v = st[f], need = f === 'units' || f === 'price' || f === 'abroad', bad = v == null ? need : !valid(f, v);
      if (bad) { inp.setAttribute('aria-invalid', 'true'); msg[f].textContent = errText(f); } else { inp.removeAttribute('aria-invalid'); msg[f].textContent = ''; }
    }
    function pills(name, legend, items, cur0, onPick) {
      var fs = el('fieldset', 'nlbg__set'); fs.appendChild(el('legend', '', esc(legend)));
      var box = el('div', 'nlbg__pills'); fs.appendChild(box);
      items.forEach(function (it) {
        var lab = el('label', 'nlbg__pill', '<input type="radio" name="' + uid + '-' + name + '" value="' + esc(it.v) + '"' + (it.v === cur0 ? ' checked' : '') + ' data-f="' + name + '"><span>' + esc(it.t) + '</span>');
        lab.querySelector('input').addEventListener('change', function (e) { if (e.target.checked) { onPick(it.v); paint(); } });
        box.appendChild(lab);
      });
      return fs;
    }

    /* ---------------------------------------------------------------- the inputs */
    var egNote = el('p', 'nlbg__help', tplH(t.egNote, { src: '<span dir="auto">' + esc(ex[LG === 'en' ? 'src_en' : 'src_he']) + '</span>', units: B(nfmt(ex.units, LG)), price: curH(ex.price, 'ILS', LG) })); egNote.setAttribute('data-o', 'egnote');
    form.appendChild(egNote);
    form.appendChild(numField('units', t.f_units, { help: esc(t.h_units) }));
    var salesP = el('p', 'nlbg__val'); salesP.setAttribute('data-o', 'sales');
    form.appendChild(numField('price', t.f_price, { unit: '₪', after: salesP }));
    form.appendChild(pills('stage', t.f_stage, STAGES.map(function (s) { return { v: s, t: t['st_' + s] }; }), st.stage, function (v) { st.stage = v; }));
    form.appendChild(pills('seller', t.f_seller, SELLERS.map(function (s) { return { v: s, t: t['se_' + s] }; }), st.seller, function (v) { st.seller = v; commW.hidden = v !== 'co'; }));
    var commW = numField('comm', t.f_comm, { unit: '%', im: 'decimal', help: esc(t.h_comm) }); commW.hidden = true; form.appendChild(commW);
    var abW = numField('abroad', t.f_abroad, { unit: '%', onInput: function () { if (valid('abroad', st.abroad)) rngIn.value = String(st.abroad); } });
    var rngIn = el('input', 'nlbg__range'); rngIn.type = 'range'; rngIn.min = '0'; rngIn.max = '100'; rngIn.step = '5'; rngIn.value = String(st.abroad); rngIn.setAttribute('aria-label', t.slider);
    abW.insertBefore(rngIn, abW.querySelector('.nlbg__msg'));
    rngIn.addEventListener('input', function () { st.abroad = +rngIn.value; var i = abW.querySelector('input[data-f="abroad"]'); i.value = String(st.abroad); check('abroad', i); paint(); });
    form.appendChild(abW);
    var sw = F.se_window;
    form.appendChild(numField('months', t.f_months, { help: tplH(t.h_months, { src: '<span dir="auto">' + esc(sw[LG === 'en' ? 'src_en' : 'src_he']) + '</span>', lo: B(sw.lo), hi: B(sw.hi), flag: esc(flagWord(sw, LG)) }) }));
    var byFig = {}, order = [];
    lpdExamples(D).forEach(function (x) { if (!byFig[x.fig]) { byFig[x.fig] = []; order.push(x.fig); } byFig[x.fig].push(B(nfmt(x.lpd, LG, 1))); });
    var lx = order.map(function (k) { return byFig[k].join(LG === 'en' ? ' or ' : ' או ') + ' (<span dir="auto">' + esc(F[k][LG === 'en' ? 'src_en' : 'src_he']) + '</span>, ' + esc(flagWord(F[k], LG)) + ')'; }).join(', ');
    form.appendChild(numField('lpd', t.f_lpd, { im: 'decimal', help: tplH(t.h_lpd, { ex: lx }) }));
    form.appendChild(el('p', 'nlbg__honest', esc(t.honesty)));

    /* ---------------------------------------------------------------- the readouts and the sheet */
    var reads = el('div', 'nlbg__reads'); reads.setAttribute('aria-live', 'polite'); out.appendChild(reads);
    var c1 = el('div', 'nlbg__card is-main'), c2 = el('div', 'nlbg__card'), c3 = el('div', 'nlbg__card'); c1.setAttribute('data-o', 'r1'); c2.setAttribute('data-o', 'r2'); c3.setAttribute('data-o', 'r3');
    reads.appendChild(c1); reads.appendChild(c2); reads.appendChild(c3);
    var leadsBox = el('div', 'nlbg__box'); leadsBox.setAttribute('data-o', 'leads'); out.appendChild(leadsBox);
    var anch = el('details', 'nlbg__anch'); anch.innerHTML = '<summary>' + esc(t.anchHead) + '</summary><div data-o="anch"></div>'; out.appendChild(anch);
    /* the budget sheet: built once (the own-price inputs keep their focus), the cells painted on every change */
    var sheet = el('div', 'nlbg__box'), tb = '';
    D.lines.forEach(function (ln) {
      tb += '<tr data-ln="' + ln.id + '"><td data-o="n"></td><td class="r" data-th="' + esc(t.th_range) + '"><span data-o="v"></span><span data-o="x"></span></td><td data-th="' + esc(t.th_when) + '" data-o="w"></td><td data-th="' + esc(t.th_src) + '" data-o="s"></td></tr>';
    });
    sheet.innerHTML = '<table class="nlbg__t is-sheet"><caption>' + esc(t.tabHead) + '</caption><colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup><thead><tr><th scope="col">' + esc(t.th_item) + '</th><th scope="col">' + esc(t.th_range) + '</th><th scope="col">' + esc(t.th_when) + '</th><th scope="col">' + esc(t.th_src) + '</th></tr></thead><tbody>' + tb
      + '</tbody><tfoot><tr><td data-o="sumLab">' + esc(t.sumLab) + '</td><td class="r" data-th="' + esc(t.th_range) + '" data-o="sum"></td><td colspan="2" data-o="open"></td></tr></tfoot></table>';
    /* v1.1: the lines in a fold, closed on phones (under 768 px), open on wider screens; widening the window opens it, never closes it */
    var fold = el('details', 'nlbg__lines', '<summary>' + esc(tpl(t.linesHead, { n: D.lines.length })) + '</summary>'); fold.setAttribute('data-o', 'lines');
    var mq = G.matchMedia ? G.matchMedia('(max-width:767px)') : null;
    fold.open = !(mq && mq.matches);
    if (mq) { var widen = function () { if (!mq.matches) fold.open = true; }; if (mq.addEventListener) mq.addEventListener('change', widen); else if (mq.addListener) mq.addListener(widen); }
    fold.appendChild(sheet); wide.appendChild(fold);
    var rowEl = {};
    D.lines.forEach(function (ln) {
      var tr = sheet.querySelector('tr[data-ln="' + ln.id + '"]'); rowEl[ln.id] = tr;
      if (ln.kind === 'own' || ln.kind === 'fee') {  // the developer's own figure: a field under "no Israeli price published"
        var id = uid + '-own-' + ln.id, w = el('div', 'nli__in nlbg__own');
        w.innerHTML = '<input id="' + id + '" data-own="' + ln.id + '" type="text" inputmode="numeric" autocomplete="off" maxlength="14" placeholder="' + esc(t.own) + '" aria-describedby="' + uid + '-e-own-' + ln.id + '"><span class="nli__unit">₪</span>';
        var m = el('p', 'nlbg__msg'); m.id = uid + '-e-own-' + ln.id; m.setAttribute('aria-live', 'polite');
        var inp = w.querySelector('input');
        inp.addEventListener('input', function () { var v = parseNum(inp.value); st.own[ln.id] = v; var bad = v != null && !valid('own', v); if (bad) inp.setAttribute('aria-invalid', 'true'); else inp.removeAttribute('aria-invalid'); m.textContent = bad ? t.e_own : ''; paint(); });
        inp.addEventListener('blur', function () { var v = st.own[ln.id]; if (v != null && valid('own', v)) inp.value = nfmt(v, LG); });
        var x = tr.querySelector('[data-o="x"]'); x.appendChild(w); x.appendChild(m);
      }
      if (ln.kind === 'plan') {
        var a = el('a', 'nlbg__plans', plansText(D, LG, true)); a.href = (D.plans_href && D.plans_href[LG]) || '/'; a.setAttribute('data-act', 'plans');
        a.addEventListener('click', function (e) { var h = document.querySelector('[data-nli="nlcamp"]'); if (h) { e.preventDefault(); h.scrollIntoView({ block: 'start' }); } });  // the planner on the same page
        tr.querySelector('[data-o="x"]').appendChild(a);
      }
    });
    var bars = el('div', 'nlbg__bars'); wide.appendChild(bars);
    var strip = el('p', 'nlbg__strip'); wide.appendChild(strip);
    wide.appendChild(shareBar());
    paintStatic();
    paint();

    function ctxHTML(ref) {
      var k = ref.split(':'), f = F[k[0]], part = k[1];
      if (part) return '<span class="nlbg__ctx"><b>' + esc(t.abroadEx) + ':</b> ' + tplH(t.exPart, { v: B(cur(f[part], f.currency, LG)), part: esc(t['px_' + part]), n: B(nfmt(f.units, LG)) }) + '<br>' + srcHTML(f, LG) + '</span>';
      if (k[0] === 'fe_suite') return '<span class="nlbg__ctx"><b>' + esc(t.abroadEx) + ':</b> ' + tplH(t.suiteRange, { lo: B(cur(f.lo, f.currency, LG)), hi: B(cur(f.hi, f.currency, LG)) }) + '<br>' + srcHTML(f, LG) + '</span>';
      var r = f.lo != null && f.unit !== 'ils_million' ? (f.unit === 'pct_price' ? rng(f.lo, f.hi, '%', LG, true) : rng(f.lo, f.hi, f.currency, LG, true)) : '';
      var lbl = f.scope === 'abroad' ? '<b>' + esc(t.abroadEx) + ':</b> ' : '';
      return '<span class="nlbg__ctx">' + lbl + esc(f[LG]) + (r ? ': ' + r : '') + '<br>' + srcHTML(f, LG) + '</span>';
    }
    /* the parts that do not follow the inputs */
    function paintStatic() {
      D.lines.forEach(function (ln) {
        var tr = rowEl[ln.id], s = tr.querySelector('[data-o="s"]'), f = ln.fig ? F[ln.fig] : null;
        s.innerHTML = (f ? srcHTML(f, LG) : (ln.kind === 'own' || ln.kind === 'fee' ? srcHTML(F.td_np, LG) : '')) + ln.ctx.map(ctxHTML).join('');
      });
      var ex2 = F.fe_ex, dl = F.fe_delay;
      bars.innerHTML = '<div class="nlbg__bh"><h3>' + esc(t.barsHead) + '</h3><span>' + esc(t.abroadEx) + '</span></div><div class="nlbg__cols" role="img"></div><div class="nlbg__labs" aria-hidden="true"></div>'
        + '<p class="nlbg__line">' + tplH(t.barsNote, { n: B(nfmt(ex2.units, LG)), total: B(cur(ex2.total, ex2.currency, LG)), pct: B(pct(ex2.pct, LG)) }) + ' ' + srcHTML(ex2, LG) + '</p>'
        + '<p class="nlbg__line">' + tplH(t.barsDelay, { m: B(dl.months), total: B(cur(dl.total, dl.currency, LG)), pct: B(pct(dl.pct, LG)), was: B(pct(ex2.pct, LG)) }) + '</p>'
        + '<p class="nlbg__line">' + tplH(t.timeIl, { a: B(F.px_time.parts[0].join('-')), b: B(F.px_time.parts[1].join('-')), c: B(F.px_time.parts[2].join('-')) }) + ' ' + srcHTML(F.px_time, LG) + '</p>';
      var g = F.gl_2025;
      strip.innerHTML = '<b>' + esc(t.ctxHead) + ':</b> ' + esc(g[LG]) + '. ' + g.list.map(function (x) { var m = tplH(t.million, { v: B(nfmt(x.v, LG, 1)) }); return '<span dir="auto">' + esc(x[LG]) + '</span> ' + (x.approx === 'almost' ? tplH(t.almost, { v: m }) : m); }).join(', ') + '. ' + srcHTML(g, LG);
    }
    function paint() {
      var r = compute(st, D);
      egTag.hidden = !isExample(st, D);
      salesP.innerHTML = r.ok ? esc(t.salesLab) + ': ' + curH(r.V, 'ILS', LG) : '';
      if (!r.ok) {
        c1.innerHTML = '<span>' + esc(st.seller === 'co' ? t.r1_co : t.r1_dev) + '</span><output class="nlbg__fig is-text is-survey" data-o="total">' + esc(t.fix) + '</output>';
        c2.innerHTML = '<span>' + esc(t.r2) + '</span><output class="nlbg__fig is-text">' + esc(t.fix) + '</output>'; c3.innerHTML = '<span>' + esc(t.r3) + '</span><output class="nlbg__fig is-text">' + esc(t.fix) + '</output>';
        leadsBox.hidden = true; anch.querySelector('[data-o="anch"]').innerHTML = '';
        D.lines.forEach(function (ln) { var tr = rowEl[ln.id]; tr.querySelector('[data-o="n"]').textContent = lineName(ln.id, st, LG); tr.querySelector('[data-o="v"]').textContent = ''; tr.querySelector('[data-o="w"]').innerHTML = esc(stageText(ln.stage, LG)); });
        sheet.querySelector('[data-o="sum"]').textContent = ''; sheet.querySelector('[data-o="open"]').textContent = '';
        paintBars(); return;
      }
      /* (1) */
      var T1 = r.total;
      var lowB = T1.comm != null ? tplH(t.plusComm, { a: B(pct(T1.lowAnchor, LG)), c: B(pct(T1.comm, LG)) }) : B(pct(T1.lowAnchor, LG));
      var hiB = T1.comm != null ? tplH(t.plusComm, { a: B(pct(T1.highAnchor, LG)), c: B(pct(T1.comm, LG)) }) : B(pct(T1.highAnchor, LG));
      c1.innerHTML = '<span>' + esc(st.seller === 'co' ? t.r1_co : t.r1_dev) + '</span><output class="nlbg__fig is-survey" data-o="total">' + rng(T1.lo, T1.hi, 'ILS', LG, true) + '</output>'
        + '<p class="nlbg__sub" data-o="pct">' + tplH(t.r1pct, { lo: B(pct(T1.loPct, LG)), hi: B(pct(T1.hiPct, LG)), v: curH(r.V, 'ILS', LG) }) + '</p>'
        + '<dl class="nlbg__bd"><div><dt>' + esc(t.lowB) + '</dt><dd data-o="low">' + lowB + '<br>' + srcHTML(F[T1.lowFig], LG) + '</dd></div><div><dt>' + esc(t.highB) + '</dt><dd data-o="high">' + hiB + '<br>' + srcHTML(F[T1.highFig], LG) + '</dd></div></dl>'
        + (T1.partial ? '<p class="nlbg__line" data-o="nocomm">' + esc(t.r1noComm) + '</p>' : '')
        + (T1.yearLo != null ? '<p class="nlbg__line" data-o="year">' + tplH(t.r1year, { m: B(r.months), v: rng(T1.yearLo, T1.yearHi, 'ILS', LG, true) }) + '</p>' : '')
        + '<p class="nlbg__line" data-o="mkt">' + tplH(t.r1mkt, { v: tplH(t.about, { v: curH(r.mkt.v, 'ILS', LG) }), pct: tplH(t.about, { v: B(pct(r.mkt.pct, LG)) }), online: B(pct(r.mkt.online, LG)) }) + '<br>' + srcHTML(F.wedo_total, LG) + '</p>';
      /* (2) */
      var u = r.unit;
      c2.innerHTML = '<span>' + esc(t.r2) + '</span><output class="nlbg__fig" data-o="unit">' + rng(u.lo, u.hi, 'ILS', LG, true) + '</output><p class="nlbg__sub">' + esc(t.r2sub) + '</p>'
        + '<p class="nlbg__line" data-o="unitAll">' + tplH(t.r2all, { n: B(nfmt(st.units, LG)), v: rng(u.totLo, u.totHi, 'ILS', LG, true) }) + '</p>'
        + '<p class="nlbg__line">' + tplH(t.r2pct, { lo: B(pct(u.pctLo, LG)), hi: B(pct(u.pctHi, LG)) }) + '</p>' + srcHTML(F.sp_unit, LG);
      /* (3) */
      var L3 = r.leads;
      c3.innerHTML = '<span>' + esc(t.r3) + '</span>' + (L3 ? '<output class="nlbg__fig" data-o="leadsN">' + B(nfmt(L3.n, LG)) + '</output><p class="nlbg__sub">' + tplH(t.r3calc, { deals: B(nfmt(L3.deals, LG)), lpd: B(nfmt(L3.lpd, LG, 1)) }) + '</p>'
          + '<p class="nlbg__line" data-o="split">' + tplH(t.r3split, { il: B(nfmt(L3.il, LG)), ab: B(nfmt(L3.ab, LG)) }) + '</p>' + (L3.perMonth != null ? '<p class="nlbg__line">' + tplH(t.r3month, { v: B(nfmt(L3.perMonth, LG)), m: B(r.months) }) + '</p>' : '')
        : '<output class="nlbg__fig is-text" data-o="leadsN">' + esc(t.r3empty) + '</output><p class="nlbg__sub">' + esc(t.r3sub) + '</p>');
      /* the leads' cost */
      leadsBox.hidden = !L3;
      if (L3) {
        leadsBox.innerHTML = '<table class="nlbg__t"><caption>' + esc(t.leadsHead) + '</caption><thead><tr><th scope="col">' + esc(t.th_basis) + '</th><th scope="col">' + esc(t.th_per) + '</th><th scope="col">' + esc(t.th_n) + '</th><th scope="col">' + esc(t.th_tot) + '</th></tr></thead><tbody>'
          + L3.costs.map(function (x) {
            var f = F[x.fig];
            return '<tr data-k="' + x.k + '"><td>' + esc(t['l_' + x.k]) + srcHTML(f, LG) + (x.k === 'us' ? '<span class="nlbg__sub">' + esc(t.usNote) + '</span>' : '') + '</td><td data-th="' + esc(t.th_per) + '">' + rng(x.per[0], x.per[1], x.cur, LG, true) + '</td><td data-th="' + esc(t.th_n) + '">' + B(nfmt(x.n, LG)) + '</td><td data-th="' + esc(t.th_tot) + '" data-o="cost">'
              + (x.n ? rng(x.lo, x.hi, x.cur, LG, true) : esc(x.k === 'us' ? t.noAbroad : t.noIl)) + '</td></tr>';
          }).join('') + '</tbody></table>';
      }
      /* every anchor on the project */
      anch.querySelector('[data-o="anch"]').innerHTML = '<table class="nlbg__t"><thead><tr><th scope="col">' + esc(t.th_aSrc) + '</th><th scope="col">' + esc(t.th_aWhat) + '</th><th scope="col">' + esc(t.th_aPct) + '</th><th scope="col">' + esc(t.th_aSum) + '</th></tr></thead><tbody>'
        + r.anchors.map(function (a) { var f = F[a.id]; return '<tr data-a="' + a.id + '"><td>' + srcHTML(f, LG) + '</td><td data-th="' + esc(t.th_aWhat) + '">' + esc(f[LG]) + '</td><td data-th="' + esc(t.th_aPct) + '">' + (f.approx ? tplH(t.about, { v: rng(a.loPct, a.hiPct, '%', LG, true) }) : rng(a.loPct, a.hiPct, '%', LG, true)) + '</td><td data-th="' + esc(t.th_aSum) + '">' + rng(a.lo, a.hi, 'ILS', LG, true) + '</td></tr>'; }).join('')
        + '</tbody></table>';
      /* the sheet */
      r.lines.forEach(function (o) {
        var tr = rowEl[o.id];
        tr.className = o.now ? 'is-now' : '';
        tr.querySelector('[data-o="n"]').textContent = lineName(o.id, st, LG);
        var v = tr.querySelector('[data-o="v"]'), extra = '';
        if (o.kind === 'unit') extra = '<span class="nlbg__sub">' + tplH(t.perUnitX, { r: rng(o.per[0], o.per[1], 'ILS', LG, true), n: B(nfmt(st.units, LG)) }) + '</span>';
        else if (o.kind === 'pct') extra = '<span class="nlbg__sub">' + tplH(t.ofSales, { p: tplH(t.about, { v: B(pct(o.pct, LG)) }) }) + '</span>';
        else if (o.kind === 'fee' && st.seller === 'co') extra = o.lo != null ? '<span class="nlbg__sub">' + tplH(t.feeCalc, { p: B(pct(o.pct, LG)) }) + '</span>' : '<span class="nlbg__sub">' + esc(t.feeNeed) + '</span>';
        var np = o.kind === 'own' || (o.kind === 'fee' && (st.seller !== 'co' || o.lo == null));  // the fact stays when the developer fills his own figure
        v.innerHTML = (np ? '<span class="nlbg__np">' + esc(t.noIl) + '</span>' : lineRange(o, LG, true)) + extra;
        var ow = tr.querySelector('.nlbg__own');
        if (ow) { var showOwn = o.kind === 'own' || st.seller !== 'co'; ow.hidden = !showOwn; ow.querySelector('input').setAttribute('aria-label', tpl(t.ownAria, { x: lineName(o.id, st, LG) })); }
        tr.querySelector('[data-o="w"]').innerHTML = esc(stageText(o.stage, LG)) + (o.now ? '<br><span class="nlbg__tag">' + esc(t.now) + '</span>' : '');
      });
      sheet.querySelector('[data-o="sum"]').innerHTML = rng(r.sum.lo, r.sum.hi, 'ILS', LG, true);
      sheet.querySelector('[data-o="open"]').innerHTML = '<span class="nlbg__sub">' + esc(r.sum.open > 1 ? tpl(t.sumOpen, { n: r.sum.open }) : r.sum.open === 1 ? t.sumOpen1 : t.sumAll) + ' ' + esc(t.sumNote) + '</span>';
      paintBars();
    }
    function paintBars() {
      var B3 = spread(D), now = barNow(st.stage), mx = Math.max.apply(null, B3.map(function (b) { return b.v; }));
      var cur0 = F.fe_ex.currency;
      bars.querySelector('.nlbg__cols').innerHTML = B3.map(function (b) {
        return '<div class="nlbg__col' + (b.k === now ? ' is-now' : '') + (b.k === 'delay' ? ' is-delay' : '') + '" data-b="' + b.k + '"><em>' + B((b.k === 'delay' ? '+' : '') + nfmt(b.share, LG, 0) + '%') + '</em><b style="height:' + Math.round(100 * b.v / mx) + '%"></b></div>';
      }).join('');
      bars.querySelector('.nlbg__cols').setAttribute('aria-label', B3.map(function (b) { return t['b_' + b.k] + ': ' + cur(b.v, cur0, LG) + ', ' + (b.k === 'delay' ? '+' : '') + nfmt(b.share, LG, 0) + '%'; }).join('; '));
      bars.querySelector('.nlbg__labs').innerHTML = B3.map(function (b) { return '<span' + (b.k === now ? ' class="is-now"' : '') + '>' + esc(t['b_' + b.k]) + '<br>' + B((b.k === 'delay' ? '+' : '') + cur(b.v, cur0, LG)) + (b.k === now ? '<br>' + esc(t.now) : '') + '</span>'; }).join('');
    }
    function shareBar() {
      var sh = el('div', 'nli__share');
      var bc = el('button', '', ICON.copy + '<span>' + esc(t.copy) + '</span>'); bc.type = 'button'; bc.setAttribute('data-act', 'copy');
      bc.addEventListener('click', function () {
        var tx = text(), lab = bc.querySelector('span'), done = function () { lab.textContent = t.copied; setTimeout(function () { lab.textContent = t.copy; }, 1600); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(tx).then(done, function () { window.prompt(t.copyPrompt, tx); }); else window.prompt(t.copyPrompt, tx);
      });
      var wa = el('a', '', ICON.wa + '<span>' + esc(t.wa) + '</span>'); wa.target = '_blank'; wa.rel = 'noopener'; wa.setAttribute('data-act', 'wa'); wa.href = waUrl(text());
      wa.addEventListener('click', function () { wa.href = waUrl(text()); });
      sh.appendChild(bc); sh.appendChild(wa);
      return sh;
    }
    function text() { return summaryText(st, D, LG, location.origin + location.pathname); }
  }
})();
