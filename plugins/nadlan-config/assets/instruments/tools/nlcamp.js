/* NadLan Instruments · nlcamp v1 (7.11.2026, Ben): "מתכנן הקמפיין", the international campaign planner for property developers.
   LOCAL BUILD: staged in docs/research/2026-11-07-campaign-network/build/build-nlcamp/ (README, node test, preview, browser check,
   registry snippet). Hebrew and English in this one file: the language comes from a data-lang attribute on the host (or an
   ancestor), else from the nearest lang attribute (the shortcode prints lang on the tool section, <html lang> on the page);
   "he" stays Hebrew, any other language is English.
   Five steps, mobile first, Back / Next, a 5-segment progress bar:
     1. markets and communities (multi-select chips, each with the languages it implies; aimed by country, city and language, plus
        community press and newsletters, never by religion or ethnicity: Meta and Google housing rules);
     2. the buyers wanted (one choice);
     3. the monthly ad budget, 3,000 to 60,000 in steps of 1,000, +/- and a slider, the yearly total (the one survey-red figure),
        a suggested split (Meta 55, Google 25, community press and newsletters 15, international portals 5) that the developer can
        change; NO reach, lead or cost-per-lead figure (no sourced benchmark yet: the hook NLCAMP.benchmarks stays null);
     4. the project: a new one (we build the page and the tour from plans and specs) or an existing nad-lan page (its address or name);
     5. summary and plan: the plan follows the number of markets (1 one market, 2-3 three markets, 4+ flagship) with its yearly price,
        the developer can switch; contact fields, a privacy notice and a consent box; the brief is saved through
        POST /wp-json/nadlan/v1/campaign-brief FIRST (inc/campaign-brief.php), then the reference id and the payment step. Payment is
        a link to the WooCommerce product of the plan (NLCAMP.plans[k].productUrl, set by the server through window.NLCAMP_CONFIG), or,
        while null, the line that a payment link is sent the same day. No card data here.
        First-payment mode (7.11.2026: Morning's terminal takes one charge of up to about 20,000): when NLCAMP.plans[k].firstPay is set
        (the server's option nadlan_cb_first_amount, 18,000), the button pays that first part of the yearly price and a line says the
        rest is paid in parts of up to the same amount through links we send. Without firstPay the button pays the full plan.
   Copy the summary as text and share it on WhatsApp (wa.me with text only). The state lives in memory only: nothing in the address,
   nothing in browser storage. The contact details never enter the shared text. Pure part in window.NLCAMP (runs in node). */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;

  /* ------------------------------------------------------------------------------------------------------ the offer */
  var MARKETS = [
    { id: 'fr', langs: ['fr'] }, { id: 'us', langs: ['en'] }, { id: 'uk', langs: ['en'] }, { id: 'ca', langs: ['en', 'fr'] },
    { id: 'be', langs: ['fr'] }, { id: 'ch', langs: ['fr'] }, { id: 'za', langs: ['en'] }, { id: 'au', langs: ['en'] },
    { id: 'ru', langs: ['ru'] }, { id: 'olim', langs: ['en', 'fr', 'ru'] }];
  var LANGS = ['en', 'fr', 'ru'];
  var BUYERS = ['home', 'invest', 'parents', 'luxury'];
  var KINDS = ['new', 'existing'];
  /* the approved annual plans (Ben 7.11.2026); ad spend is separate, paid by the developer straight to the channels.
     markets: how many the plan carries (null = no limit). productUrl: the WooCommerce product, null until it exists. */
  var plans = {
    one: { price: 36000, markets: 1, productUrl: null, firstPay: null },
    three: { price: 72000, markets: 3, productUrl: null, firstPay: null },
    flag: { price: 144000, markets: null, productUrl: null, firstPay: null }
  };
  var PLAN_ORDER = ['one', 'three', 'flag'];
  var BUDGET = { min: 3000, max: 60000, step: 1000, start: 10000 };
  var SPLIT = [{ k: 'meta', pct: 55 }, { k: 'google', pct: 25 }, { k: 'press', pct: 15 }, { k: 'boards', pct: 5 }];
  var SHARE_STEP = 5;
  var REF_RE = /^NLC-[0-9]{6}-[A-Z0-9]{4,8}$/;

  /* ------------------------------------------------------------------------------------------------------ the words */
  var STR = {
    he: {
      kicker: 'קמפיין בינלאומי ליזמים', title: 'מתכנן הקמפיין', progress: 'השלבים בתוכנית', stepOf: 'שלב {n} מתוך 5: {name}',
      s1: 'שווקים וקהילות', s1lede: 'בחרו איפה גרים הקונים שלכם. אפשר לבחור כמה שווקים, ונציג את הפרויקט לכל קהל בשפה שלו.',
      s1aim: 'הפרסום מכוון לפי מדינה, עיר ושפה, ובעיתונות ובניוזלטרים של הקהילות.',
      s1group: 'שווקים וקהילות לקמפיין', langsLab: 'שפות הקמפיין', recLab: 'התוכנית המתאימה', none: 'עוד לא נבחר',
      m_fr: 'צרפת', m_us: 'ארצות הברית', m_uk: 'בריטניה', m_ca: 'קנדה', m_be: 'בלגיה', m_ch: 'שווייץ', m_za: 'דרום אפריקה',
      m_au: 'אוסטרליה', m_ru: 'דוברי רוסית', m_olim: 'עולים חדשים בישראל',
      l_en: 'אנגלית', l_fr: 'צרפתית', l_ru: 'רוסית',
      s2: 'הקונים שאתם מחפשים', s2lede: 'למי הפרויקט מתאים במיוחד? בחרו קהל אחד, ונכוון אליו את המודעות.',
      b_home: 'בית בישראל לעלייה או לחופשות', b_home_d: 'משפחות שמתכננות עלייה, וקונים שרוצים דירה לחגים ולקיץ.',
      b_invest: 'משקיעים, להשכרה', b_invest_d: 'קונים שמחפשים הכנסה משכירות ומנהלים את הדירה מרחוק.',
      b_parents: 'הורים לילדים שגרים בישראל', b_parents_d: 'הורים שרוצים דירה קרוב לילדים ולנכדים.',
      b_luxury: 'יוקרה: פנטהאוזים ודירות גן', b_luxury_d: 'קונים לדירות הגדולות והמיוחדות בפרויקט.',
      s3: 'תקציב פרסום חודשי', s3lede: 'כמה תרצו להשקיע בפרסום בכל חודש? התקציב שלכם, בנפרד ממחיר התוכנית.',
      budgetLab: 'תקציב פרסום בחודש', budgetUnit: 'בחודש', budgetHelp: 'בין {min} ל־{max}, בקפיצות של {step}',
      minus: 'פחות {step}', plus: 'עוד {step}', slider: 'תקציב פרסום בחודש, בגרירה',
      perMonth: 'בחודש', perYear: 'בשנה, סך הכול',
      paidDirect: 'את תקציב הפרסום אתם משלמים ישירות לערוצים עצמם: Meta, Google, העיתונות הקהילתית ואתרי הנדלן. הוא לא חלק ממחיר התוכנית.',
      splitLab: 'חלוקה מוצעת של התקציב', splitMine: 'החלוקה שלכם', splitNote: 'זו נקודת פתיחה, ואתם יכולים לשנות אותה.',
      ch_meta: 'Meta (פייסבוק ואינסטגרם)', ch_google: 'Google (חיפוש ויוטיוב)', ch_press: 'עיתונות קהילתית וניוזלטרים', ch_boards: 'אתרי נדלן בינלאומיים',
      chs_meta: 'Meta', chs_google: 'Google', chs_press: 'עיתונות קהילתית', chs_boards: 'אתרי נדלן',
      adjust: 'שינוי החלוקה', shLess: '{ch}: פחות 5%', shMore: '{ch}: עוד 5%', sum: 'סך הכול', reset: 'חזרה לחלוקה המוצעת',
      s4: 'הפרויקט', s4lede: 'לאן יגיעו הקונים? לעמוד הפרויקט שלכם בנדלן, עם הסיור התלת־ממדי והפרטים שהם צריכים.',
      k_new: 'פרויקט חדש', k_new_d: 'נבנה לכם את עמוד הפרויקט ואת הסיור הווירטואלי מהתוכניות ומהמפרט.',
      k_existing: 'פרויקט שכבר יש לו עמוד בנדלן', k_existing_d: 'הקמפיין יביא את הקונים לעמוד הקיים שלכם.',
      refLabExisting: 'כתובת העמוד או שם הפרויקט', refLabNew: 'שם הפרויקט והעיר (לא חובה)',
      refHelpExisting: 'למשל: שם הפרויקט, הרחוב והעיר, או הקישור לעמוד.', refHelpNew: 'אפשר להשאיר ריק ולספר לנו בשיחה.',
      s5: 'סיכום ותוכנית', s5lede: 'זו התוכנית שלכם. בדקו את הפרטים, בחרו תוכנית שנתית ושלחו.',
      d_markets: 'שווקים וקהילות', d_langs: 'שפות', d_buyer: 'הקונים', d_budget: 'תקציב פרסום', d_split: 'חלוקת התקציב',
      d_project: 'הפרויקט', d_plan: 'התוכנית', d_rec: 'התוכנית המתאימה',
      edit: 'שינוי', editOf: 'שינוי: {x}', budgetLine: '{m} בחודש, {y} בשנה',
      planLab: 'בחרו תוכנית שנתית',
      p_one: 'שוק אחד', p_one_d: 'קמפיין בשוק אחד או בקהילה אחת.',
      p_three: 'שלושה שווקים', p_three_d: 'קמפיין בעד שלושה שווקים וקהילות.',
      p_flag: 'פרויקט דגל', p_flag_d: 'כל השווקים והקהילות שבחרתם, בלי הגבלה.',
      perYearShort: 'לשנה', recTag: 'מתאימה {n} שבחרתם',
      planNote: 'בכל תוכנית: עמוד הפרויקט בנדלן עם הסיור הווירטואלי, בשפות השווקים שבחרתם, והפניות מהקמפיין מגיעות אליו. המחיר לשנה, ותקציב הפרסום בנפרד.',
      leads: 'כל פנייה מגיעה אליכם בוואטסאפ, עם מה שהקונה פתח בפרויקט.',
      contactLab: 'פרטים ליצירת קשר', f_name: 'שם מלא', f_company: 'חברה', f_phone: 'טלפון', f_email: 'אימייל',
      privacy: 'נשתמש בפרטים רק כדי להכין את הקמפיין ולחזור אליכם, ולא נעביר אותם לאף אחד. אין חובה חוקית למסור אותם, אבל בלעדיהם לא נוכל לחזור אליכם.',
      privacyLink: 'מדיניות הפרטיות',
      consent: 'אנחנו מאשרים שצוות נדלן יחזור אלינו בטלפון, בוואטסאפ ובאימייל לגבי הקמפיין הזה.',
      notPay: 'שליחת התוכנית אינה תשלום. המנוי השנתי משולם בשלב הבא, לפני שהקמפיין יוצא לדרך.',
      hp: 'השאירו את השדה הזה ריק',
      next: 'המשיכו', back: 'חזרה', send: 'שלחו את התוכנית', sending: 'שולחים…',
      copy: 'העתקת הסיכום', copied: 'הועתק', copyPrompt: 'העתיקו את הסיכום', wa: 'שליחה בוואטסאפ',
      e_markets: 'בחרו לפחות שוק או קהילה אחת.', e_buyer: 'בחרו את הקונים שאתם מחפשים.',
      e_budget: 'התקציב החודשי צריך להיות בין {min} ל־{max}, בקפיצות של {step}.', e_split: 'החלוקה צריכה להסתכם ב־100%. עכשיו: {sum}.',
      e_kind: 'בחרו פרויקט חדש או פרויקט שכבר יש לו עמוד.', e_ref: 'כתבו את כתובת העמוד או את שם הפרויקט.',
      e_plan: 'בחרו תוכנית שנתית.', e_cover: 'בחרתם {n}, ובתוכנית "{plan}" יש מקום {max}. בחרו תוכנית גדולה יותר, או צמצמו את השווקים בשלב הראשון.',
      e_name: 'כתבו שם מלא.', e_company: 'כתבו את שם החברה.', e_phone: 'כתבו מספר טלפון, אפשר עם קידומת של מדינה.',
      e_email: 'כתבו כתובת אימייל מלאה.', e_consent: 'כדי לשלוח, סמנו את האישור.',
      e_send: 'לא הצלחנו לשמור את התוכנית. בדקו את החיבור ונסו שוב.',
      doneTitle: 'התוכנית נשמרה', refLab: 'מספר התוכנית שלכם', doneText: 'שמרו את המספר. צוות נדלן כבר קיבל את התוכנית.',
      payTitle: 'תשלום המנוי השנתי', payBtn: 'לתשלום: {plan}, {price} לשנה', payFirst: 'לתשלום ראשון: {first} ({plan}, {price} לשנה)',
      payRest: 'את היתרה, {rest}, משלמים בתשלומים של עד {part}, בקישורים שנשלחים אליכם.',
      payNote: 'התשלום בעמוד התשלום המאובטח של האתר. כאן לא מבקשים פרטי כרטיס.',
      payLater: 'קישור לתשלום יישלח אליכם עוד היום.', launch: 'הקמפיין יוצא לדרך אחרי התשלום.',
      side: 'התוכנית שלכם עד עכשיו', shareHead: 'תוכנית קמפיין בינלאומי בנדלן', t_ref: 'מספר התוכנית',
      t_paid: 'תקציב הפרסום משולם ישירות לערוצים, בנפרד מהתוכנית.'
    },
    en: {
      kicker: 'International campaigns for developers', title: 'Campaign planner', progress: 'Progress in the plan', stepOf: 'Step {n} of 5: {name}',
      s1: 'Markets and communities', s1lede: 'Choose where your buyers live. You can choose several markets, and we present the project to each audience in its own language.',
      s1aim: 'Ads are aimed by country, city and language, plus community press and newsletters.',
      s1group: 'Markets and communities for the campaign', langsLab: 'Campaign languages', recLab: 'The plan that fits', none: 'Not chosen yet',
      m_fr: 'France', m_us: 'USA', m_uk: 'UK', m_ca: 'Canada', m_be: 'Belgium', m_ch: 'Switzerland', m_za: 'South Africa',
      m_au: 'Australia', m_ru: 'Russian speakers', m_olim: 'Olim in Israel',
      l_en: 'English', l_fr: 'French', l_ru: 'Russian',
      s2: 'The buyers you want', s2lede: 'Who is the project best for? Choose one audience, and we aim the ads at it.',
      b_home: 'A home in Israel for aliyah or holidays', b_home_d: 'Families planning aliyah, and buyers who want a home for the holidays and the summer.',
      b_invest: 'Investors (rental)', b_invest_d: 'Buyers looking for rental income who manage the home from abroad.',
      b_parents: 'Parents of children living in Israel', b_parents_d: 'Parents who want a home close to their children and grandchildren.',
      b_luxury: 'Luxury: penthouses and garden apartments', b_luxury_d: 'Buyers for the largest and most special homes in the project.',
      s3: 'Monthly ad budget', s3lede: 'How much would you like to put into ads each month? Your budget, separate from the plan price.',
      budgetLab: 'Ad budget per month', budgetUnit: 'a month', budgetHelp: 'From {min} to {max}, in steps of {step}',
      minus: '{step} less', plus: '{step} more', slider: 'Ad budget per month, slider',
      perMonth: 'A month', perYear: 'A year, in total',
      paidDirect: 'You pay the ad budget straight to the channels themselves: Meta, Google, the community press and the property portals. It is not part of the plan price.',
      splitLab: 'Suggested budget split', splitMine: 'Your split', splitNote: 'This is a starting point, and you can change it.',
      ch_meta: 'Meta (Facebook and Instagram)', ch_google: 'Google (Search and YouTube)', ch_press: 'Community press and newsletters', ch_boards: 'International property portals',
      chs_meta: 'Meta', chs_google: 'Google', chs_press: 'Community press', chs_boards: 'Property portals',
      adjust: 'Change the split', shLess: '{ch}: 5% less', shMore: '{ch}: 5% more', sum: 'Total', reset: 'Back to the suggested split',
      s4: 'The project', s4lede: 'Where will the buyers land? On your project page on NadLan, with the 3D tour and the details they need.',
      k_new: 'A new project', k_new_d: 'We build the project page and the virtual tour from your plans and specifications.',
      k_existing: 'A project that already has a page on NadLan', k_existing_d: 'The campaign brings the buyers to your existing page.',
      refLabExisting: 'The page address or the project name', refLabNew: 'Project name and city (optional)',
      refHelpExisting: 'For example: the project name, the street and the city, or the link to the page.', refHelpNew: 'You can leave it empty and tell us on the call.',
      s5: 'Summary and plan', s5lede: 'This is your plan. Check the details, choose an annual plan and send it.',
      d_markets: 'Markets and communities', d_langs: 'Languages', d_buyer: 'Buyers', d_budget: 'Ad budget', d_split: 'Budget split',
      d_project: 'The project', d_plan: 'The plan', d_rec: 'The plan that fits',
      edit: 'Change', editOf: 'Change: {x}', budgetLine: '{m} a month, {y} a year',
      planLab: 'Choose an annual plan',
      p_one: 'One market', p_one_d: 'A campaign in one market or one community.',
      p_three: 'Three markets', p_three_d: 'A campaign in up to three markets and communities.',
      p_flag: 'Flagship', p_flag_d: 'Every market and community you chose, with no limit.',
      perYearShort: 'a year', recTag: 'Fits the {n} you chose',
      planNote: 'Every plan includes your project page on NadLan with the virtual tour, in the languages of the markets you chose, and the campaign leads land on it. The price is per year; the ad budget is separate.',
      leads: 'Every lead reaches you on WhatsApp with what the buyer opened in the project.',
      contactLab: 'Contact details', f_name: 'Full name', f_company: 'Company', f_phone: 'Phone', f_email: 'Email',
      privacy: 'We use these details only to prepare the campaign and get back to you, and we do not pass them to anyone. You are not legally required to give them, but without them we cannot get back to you.',
      privacyLink: 'Privacy policy',
      consent: 'We agree that the NadLan team may contact us by phone, WhatsApp and email about this campaign.',
      notPay: 'Sending the plan is not a payment. The annual subscription is paid in the next step, before the campaign goes live.',
      hp: 'Leave this field empty',
      next: 'Continue', back: 'Back', send: 'Send the plan', sending: 'Sending…',
      copy: 'Copy the summary', copied: 'Copied', copyPrompt: 'Copy the summary', wa: 'Send on WhatsApp',
      e_markets: 'Choose at least one market or community.', e_buyer: 'Choose the buyers you want.',
      e_budget: 'The monthly budget must be from {min} to {max}, in steps of {step}.', e_split: 'The split must add up to 100%. Now: {sum}.',
      e_kind: 'Choose a new project or a project that already has a page.', e_ref: 'Write the page address or the project name.',
      e_plan: 'Choose an annual plan.', e_cover: 'You chose {n}, and the "{plan}" plan has {max}. Choose a bigger plan, or narrow the markets in step 1.',
      e_name: 'Write your full name.', e_company: 'Write the company name.', e_phone: 'Write a phone number, with the country code if you like.',
      e_email: 'Write a full email address.', e_consent: 'To send, tick the consent box.',
      e_send: 'We could not save the plan. Check your connection and try again.',
      doneTitle: 'Your plan is saved', refLab: 'Your plan number', doneText: 'Keep this number. The NadLan team already has your plan.',
      payTitle: 'Paying the annual subscription', payBtn: 'Pay: {plan}, {price} a year', payFirst: 'Pay the first part: {first} ({plan}, {price} a year)',
      payRest: 'The rest, {rest}, is paid in parts of up to {part} through links we send you.',
      payNote: 'Payment is on the site\'s secure payment page. No card details are asked for here.',
      payLater: 'A payment link will be sent to you today.', launch: 'The campaign goes live after payment.',
      side: 'Your plan so far', shareHead: 'International campaign plan on NadLan', t_ref: 'Plan number',
      t_paid: 'The ad budget is paid straight to the channels, separate from the plan.'
    }
  };

  /* ------------------------------------------------------------------------------------------------------ the logic */
  function nfmt(n, lang) { return new Intl.NumberFormat(lang === 'en' ? 'en-US' : 'he-IL', { maximumFractionDigits: 0 }).format(Math.round(+n || 0)); }
  function money(n, lang) { return '₪' + nfmt(n, lang); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function B(s) { return '<bdi>' + esc(s) + '</bdi>'; }
  function tpl(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o && o[k] != null ? o[k] : m; }); }
  function tplH(s, o) { return tpl(esc(s), o); }  // o: values that are HTML already (escaped, figures in <bdi>)
  function T(lang) { return STR[lang === 'en' ? 'en' : 'he']; }
  function market(id) { for (var i = 0; i < MARKETS.length; i++) if (MARKETS[i].id === id) return MARKETS[i]; return null; }

  function newState() { return { step: 1, markets: [], buyer: null, budget: BUDGET.start, shares: SPLIT.map(function (c) { return c.pct; }), kind: null, ref: '', plan: null, planTouched: false, name: '', company: '', phone: '', email: '', consent: false }; }
  function toggleMarket(st, id) {
    if (!market(id)) return st.markets;
    var on = st.markets.indexOf(id) > -1;
    st.markets = MARKETS.map(function (m) { return m.id; }).filter(function (x) { return x === id ? !on : st.markets.indexOf(x) > -1; });
    return st.markets;
  }
  /* 1 -> one market, 2-3 -> three markets, 4+ -> flagship; none -> null */
  function recommend(n) { return n >= 4 ? 'flag' : n >= 2 ? 'three' : n === 1 ? 'one' : null; }
  function covers(plan, n) { var p = plans[plan]; return !!p && (p.markets == null || n <= p.markets); }
  function langsOf(ids) { var s = {}; (ids || []).forEach(function (id) { var m = market(id); if (m) m.langs.forEach(function (l) { s[l] = 1; }); }); return LANGS.filter(function (l) { return s[l]; }); }
  function budgetOk(v) { return typeof v === 'number' && isFinite(v) && v >= BUDGET.min && v <= BUDGET.max && v % BUDGET.step === 0; }
  function clampBudget(v) { v = +v; if (!isFinite(v)) return BUDGET.start; return Math.min(BUDGET.max, Math.max(BUDGET.min, Math.round(v / BUDGET.step) * BUDGET.step)); }
  function stepBudget(st, dir) { st.budget = budgetOk(st.budget) ? clampBudget(st.budget + dir * BUDGET.step) : clampBudget(st.budget); return st.budget; }
  function yearly(m) { return m * 12; }
  function splitSum(shares) { return (shares || []).reduce(function (s, x) { return s + (+x || 0); }, 0); }
  function stepShare(st, i, dir) { st.shares[i] = Math.min(100, Math.max(0, (+st.shares[i] || 0) + dir * SHARE_STEP)); return st.shares[i]; }
  /* the monthly amount of every channel; whole shekels, and when the shares sum to 100 the amounts sum to the budget exactly */
  function splitAmounts(monthly, shares) {
    var out = SPLIT.map(function (c, i) { var p = +shares[i] || 0; return { k: c.k, pct: p, amount: Math.floor(monthly * p / 100) }; });
    if (splitSum(shares) === 100) {
      var rest = monthly - out.reduce(function (s, x) { return s + x.amount; }, 0), big = 0;
      out.forEach(function (x, i) { if (x.pct > out[big].pct) big = i; });
      out[big].amount += rest;
    }
    return out;
  }
  function phoneOk(s) { return /^\+?\d{9,15}$/.test(String(s || '').replace(/[\s\-().]/g, '')); }
  function emailOk(s) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(s || '').trim()); }
  /* the errors of one step, in screen order: [{ f: field, code }] (code defaults to the field) */
  function validate(st, step) {
    var e = [], n = st.markets.length;
    if (step === 1 && !n) e.push({ f: 'markets' });
    if (step === 2 && BUYERS.indexOf(st.buyer) < 0) e.push({ f: 'buyer' });
    if (step === 3) { if (!budgetOk(st.budget)) e.push({ f: 'budget' }); if (splitSum(st.shares) !== 100) e.push({ f: 'split', sum: splitSum(st.shares) }); }
    if (step === 4) { if (KINDS.indexOf(st.kind) < 0) e.push({ f: 'kind' }); else if (st.kind === 'existing' && String(st.ref || '').trim().length < 2) e.push({ f: 'ref' }); }
    if (step === 5) {
      if (!plans[st.plan]) e.push({ f: 'plan' }); else if (!covers(st.plan, n)) e.push({ f: 'plan', code: 'cover' });
      if (String(st.name || '').trim().length < 2) e.push({ f: 'name' });
      if (String(st.company || '').trim().length < 2) e.push({ f: 'company' });
      if (!phoneOk(st.phone)) e.push({ f: 'phone' });
      if (!emailOk(st.email)) e.push({ f: 'email' });
      if (st.consent !== true) e.push({ f: 'consent' });
    }
    return e;
  }
  function validateAll(st) { var e = []; for (var s = 1; s <= 5; s++) validate(st, s).forEach(function (x) { x.step = s; e.push(x); }); return e; }
  function countText(n, lang) { return lang === 'en' ? n + (n === 1 ? ' market' : ' markets') : (n === 1 ? 'שוק אחד' : n + ' שווקים'); }
  function countHTML(n, lang) { return lang === 'en' ? B(n) + (n === 1 ? ' market' : ' markets') : (n === 1 ? 'שוק אחד' : B(n) + ' שווקים'); }
  /* Hebrew "to N markets" with the maqaf before a figure: לשוק אחד, ל־3 שווקים */
  function toText(n) { return n === 1 ? 'לשוק אחד' : 'ל־' + n + ' שווקים'; }
  function toHTML(n) { return n === 1 ? 'לשוק אחד' : 'ל־' + B(n) + ' שווקים'; }
  function planPrice(plan, lang) { return plans[plan] ? money(plans[plan].price, lang) : ''; }
  /* the summary rows, shared by the summary list, the side panel and the copied text: { k, step, label, text, html } */
  function lines(st, lang) {
    var t = T(lang), L = [], b = st.budget, n = st.markets.length;
    var add = function (k, step, label, text, html) { L.push({ k: k, step: step, label: label, text: text, html: html == null ? esc(text) : html }); };
    add('markets', 1, t.d_markets, n ? st.markets.map(function (m) { return t['m_' + m]; }).join(', ') : t.none);
    add('langs', 1, t.d_langs, n ? langsOf(st.markets).map(function (l) { return t['l_' + l]; }).join(', ') : t.none);
    add('buyer', 2, t.d_buyer, st.buyer ? t['b_' + st.buyer] : t.none);
    if (budgetOk(b)) add('budget', 3, t.d_budget, tpl(t.budgetLine, { m: money(b, lang), y: money(yearly(b), lang) }), tplH(t.budgetLine, { m: B(money(b, lang)), y: B(money(yearly(b), lang)) }));
    else add('budget', 3, t.d_budget, t.none);
    /* a Latin channel name and its share inside Hebrew text: each item is isolated (HTML: dir="auto"; plain text: a right-to-left
       mark after each item in Hebrew), else "Meta 55%, Google 25%" reorders and 25% lands beside Meta */
    add('split', 3, t.d_split, SPLIT.map(function (c, i) { return t['chs_' + c.k] + ' ' + st.shares[i] + '%' + (lang === 'en' ? '' : '\u200F'); }).join(', '),
      SPLIT.map(function (c, i) { return '<span dir="auto">' + esc(t['chs_' + c.k]) + ' ' + B(st.shares[i] + '%') + '</span>'; }).join(', '));
    var pr = String(st.ref || '').trim();
    add('project', 4, t.d_project, st.kind ? t['k_' + st.kind] + (pr ? ', ' + pr : '') : t.none);
    if (plans[st.plan]) add('plan', 5, t.d_plan, t['p_' + st.plan] + ', ' + planPrice(st.plan, lang) + ' ' + t.perYearShort, esc(t['p_' + st.plan]) + ', ' + B(planPrice(st.plan, lang)) + ' ' + esc(t.perYearShort));
    return L;
  }
  /* the copied / WhatsApp text: the plan only, never the contact details */
  function summaryText(st, lang, ref, url) {
    var t = T(lang), out = [t.shareHead];
    lines(st, lang).forEach(function (l) { out.push(l.label + ': ' + l.text); });
    out.push(t.t_paid); out.push(t.leads);
    if (ref) out.push(t.t_ref + ': ' + ref);
    if (url) out.push(url);
    return out.join('\n');
  }
  function waUrl(text) { return 'https://wa.me/?text=' + encodeURIComponent(text); }
  /* the body of POST /wp-json/nadlan/v1/campaign-brief (inc/campaign-brief.php checks every field again) */
  function payload(st, lang, ms, page, hp) {
    return { v: 1, lang: lang === 'en' ? 'en' : 'he', markets: st.markets.slice(), buyer: st.buyer, budget: st.budget, shares: st.shares.slice(),
      kind: st.kind, project: String(st.ref || '').trim().slice(0, 200), plan: st.plan, name: String(st.name || '').trim(), company: String(st.company || '').trim(),
      phone: String(st.phone || '').trim(), email: String(st.email || '').trim(), consent: st.consent === true, consent_text: T(lang).consent,
      hp: hp || '', t: Math.max(0, Math.round(+ms || 0)), page: String(page || '').slice(0, 200) };
  }
  function safeUrl(u) { return typeof u === 'string' && (/^https:\/\/[^\s"'<>]+$/.test(u) || /^\/[^\s"'<>]*$/.test(u)) ? u : null; }
  /* the first part of the yearly price, when the server set one: a whole positive amount below the plan price, else null */
  function firstPay(plan) { var p = plans[plan], f = p && p.firstPay; return typeof f === 'number' && isFinite(f) && f === Math.round(f) && f > 0 && f < p.price ? f : null; }
  function restOf(plan) { var f = firstPay(plan); return f ? plans[plan].price - f : 0; }
  function payUrl(plan, ref) { var u = plans[plan] && safeUrl(plans[plan].productUrl); return u ? u + (u.indexOf('?') > -1 ? '&' : '?') + 'nlc_ref=' + encodeURIComponent(ref || '') : null; }
  /* the server config (inc/campaign-brief.php prints window.NLCAMP_CONFIG before this file): the REST address and the product links */
  function configure(cfg) {
    if (!cfg || typeof cfg !== 'object') return;
    if (cfg.endpoint && safeUrl(cfg.endpoint)) NLCAMP.endpoint = cfg.endpoint;
    if (cfg.privacy && safeUrl(cfg.privacy)) NLCAMP.privacy = cfg.privacy;
    if (cfg.plans) Object.keys(cfg.plans).forEach(function (k) {
      var c = cfg.plans[k]; if (!plans[k] || !c) return;
      if ('productUrl' in c) plans[k].productUrl = safeUrl(c.productUrl);
      if ('firstPay' in c) { plans[k].firstPay = typeof c.firstPay === 'number' ? c.firstPay : null; if (!firstPay(k)) plans[k].firstPay = null; }
    });
  }

  var NLCAMP = { MARKETS: MARKETS, LANGS: LANGS, BUYERS: BUYERS, KINDS: KINDS, plans: plans, PLAN_ORDER: PLAN_ORDER, BUDGET: BUDGET, SPLIT: SPLIT,
    SHARE_STEP: SHARE_STEP, REF_RE: REF_RE, STR: STR,
    benchmarks: null,  // hook: sourced reach / lead / cost-per-lead benchmarks per market, once we have them. While null, no such figure is shown.
    endpoint: null, privacy: null,
    nfmt: nfmt, money: money, esc: esc, tpl: tpl, newState: newState, toggleMarket: toggleMarket, recommend: recommend, covers: covers, langsOf: langsOf,
    budgetOk: budgetOk, clampBudget: clampBudget, stepBudget: stepBudget, yearly: yearly, splitSum: splitSum, stepShare: stepShare, splitAmounts: splitAmounts,
    phoneOk: phoneOk, emailOk: emailOk, validate: validate, validateAll: validateAll, countText: countText, toText: toText, lines: lines, summaryText: summaryText,
    waUrl: waUrl, payload: payload, safeUrl: safeUrl, payUrl: payUrl, firstPay: firstPay, restOf: restOf, configure: configure };
  G.NLCAMP = NLCAMP;
  if (G.NLCAMP_CONFIG) configure(G.NLCAMP_CONFIG);
  if (typeof document === 'undefined' || !G.NadLanInstruments) return;  // node: the logic only

  /* ===================================================================================================== the page */
  var CHECK = '<svg class="nlcp__ind" viewBox="0 0 16 16" aria-hidden="true"><rect x="1.5" y="1.5" width="13" height="13" rx="2"/><path class="k" d="M4.4 8.3l2.4 2.4 4.8-5"/></svg>';
  var ICON = {
    copy: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 7h9v10H7z"/><path d="M4 13V3h9"/></svg>',
    wa: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16l1-3.2A7 7 0 1 1 7.6 15z"/></svg>'
  };
  G.NadLanInstruments.register('nlcamp', { custom: function (root) { mount(root); } });

  function langFor(root) {
    var d = root.closest('[data-lang]'), a = (d && d.getAttribute('data-lang')) || '';
    if (!a) { var l = root.closest('[lang]'); a = (l && l.getAttribute('lang')) || document.documentElement.getAttribute('lang') || 'he'; }
    return /^(he|iw)\b/i.test(a) ? 'he' : 'en';
  }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }

  function css() {
    if (document.getElementById('nlcp-css')) return;
    var s = document.createElement('style'); s.id = 'nlcp-css';
    s.textContent = [
      /* the tool keeps the NadLan Instruments tokens of core.css (.nli); the live theme restyles buttons, inputs, labels, lists and
         headings, so the rules that must hold carry html body .nli .nlcp and, where the theme insists, !important */
      '.nlcp[dir="rtl"]{direction:rtl}.nlcp[dir="ltr"]{direction:ltr}',
      '.nlcp[lang="en"]{--nli-sans:"IBM Plex Sans","IBM Plex Sans Hebrew",system-ui,sans-serif;--nli-display:"IBM Plex Sans Condensed","IBM Plex Sans",system-ui,sans-serif}',
      'html body .nli .nlcp[lang="en"] h2.nli__title{font:600 36px/40px var(--nli-display) !important;letter-spacing:-.01em}',
      '@media (max-width:520px){html body .nli .nlcp[lang="en"] h2.nli__title{font-size:30px !important;line-height:34px !important}}',
      '.nlcp .nlcp__sr{position:absolute !important;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}',
      '.nlcp bdi{font-family:var(--nli-mono);font-variant-numeric:tabular-nums}',
      'html body .nli .nlcp .nlcp__hd{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;margin:0 0 12px;position:relative}',
      'html body .nli .nlcp .nlcp__hd h2.nli__title{margin:0 !important}',
      'html body .nli .nlcp .nlcp__hd .nli__kicker{margin:0 0 4px}',
      '.nlcp .nlcp__count{margin:0;padding-bottom:6px;font:500 15px/20px var(--nli-mono);color:var(--nli-mute);white-space:nowrap}',
      '.nlcp .nlcp__bar{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px;margin:0 0 20px;position:relative}',
      '.nlcp .nlcp__bar i{display:block;height:6px;border-radius:1px;background:var(--nli-line)}',
      '.nlcp .nlcp__bar i.is-on{background:var(--nli-sea)}.nlcp .nlcp__bar i.is-now{background:var(--nli-sea-deep)}',
      '.nlcp .nlcp__grid{display:grid;grid-template-columns:minmax(0,1fr);gap:24px;position:relative}',
      '@media (min-width:860px){.nlcp .nlcp__grid{grid-template-columns:minmax(0,1fr) 300px;gap:40px}}',
      '.nlcp .nlcp__form{margin:0;min-width:0}',
      'html body .nli .nlcp h3.nlcp__h{font:600 21px/28px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 6px !important;letter-spacing:0 !important;text-transform:none !important;outline:none}',
      'html body .nli .nlcp h3.nlcp__h:focus-visible{outline:2px solid var(--nli-focus);outline-offset:2px}',
      'html body .nli .nlcp .nlcp__lede{font:400 16px/26px var(--nli-sans);color:var(--nli-ink2);margin:0 0 16px;max-width:62ch}',
      '.nlcp .nlcp__body{display:grid;gap:16px;min-width:0}',
      /* chips */
      '.nlcp .nlcp__chips{display:flex;flex-wrap:wrap;gap:8px}',
      'html body .nli .nlcp button.nlcp__chip{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 16px 8px 14px;border:1px solid var(--nli-line) !important;border-radius:999px !important;background:var(--nli-surface) !important;color:var(--nli-ink) !important;font:500 15px/20px var(--nli-sans) !important;cursor:pointer;margin:0;box-shadow:none !important;text-transform:none !important;letter-spacing:0 !important}',
      'html body .nli .nlcp button.nlcp__chip:hover{border-color:var(--nli-sea) !important}',
      'html body .nli .nlcp button.nlcp__chip[aria-pressed="true"]{background:var(--nli-sea) !important;border-color:var(--nli-sea) !important;color:var(--nli-on-sea) !important}',
      '.nlcp .nlcp__chip small{font:500 11px/16px var(--nli-mono);letter-spacing:.04em;color:var(--nli-mute);direction:ltr;unicode-bidi:isolate}',
      '.nlcp .nlcp__chip[aria-pressed="true"] small{color:var(--nli-on-sea)}',
      '.nlcp .nlcp__ind{width:16px;height:16px;flex:none;fill:none;stroke:currentColor;stroke-width:1.5}',
      '.nlcp .nlcp__ind .k{display:none;stroke-width:2}.nlcp [aria-pressed="true"] .nlcp__ind .k{display:inline}',
      /* the small definition lists (step 1 readout, side panel) and the summary list */
      'html body .nli .nlcp dl.nlcp__mini{margin:0;display:grid;gap:0;border-top:1px solid var(--nli-line)}',
      'html body .nli .nlcp dl.nlcp__mini>div{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:8px 0;border-bottom:1px solid var(--nli-line)}',
      'html body .nli .nlcp dl.nlcp__mini dt{font:400 14px/20px var(--nli-sans);color:var(--nli-ink2);margin:0}',
      'html body .nli .nlcp dl.nlcp__mini dd{font:500 14px/20px var(--nli-sans);color:var(--nli-ink);margin:0;text-align:end}',
      'html body .nli .nlcp dl.nlcp__dl{margin:0;display:grid;border-top:1px solid var(--nli-line)}',
      'html body .nli .nlcp dl.nlcp__dl>div{display:grid;grid-template-columns:minmax(0,8.5em) minmax(0,1fr) auto;gap:4px 12px;align-items:center;padding:6px 0;border-bottom:1px solid var(--nli-line)}',
      'html body .nli .nlcp dl.nlcp__dl dt{font:500 14px/20px var(--nli-sans);color:var(--nli-mute);margin:0}',
      'html body .nli .nlcp dl.nlcp__dl dd{font:400 15px/22px var(--nli-sans);color:var(--nli-ink);margin:0;min-width:0;overflow-wrap:anywhere}',
      '@media (max-width:520px){html body .nli .nlcp dl.nlcp__dl>div{grid-template-columns:minmax(0,1fr) auto;gap:0 12px}html body .nli .nlcp dl.nlcp__dl dt{grid-column:1;grid-row:1}html body .nli .nlcp dl.nlcp__dl dd.nlcp__e{grid-column:2;grid-row:1}html body .nli .nlcp dl.nlcp__dl dd.nlcp__v{grid-column:1 / -1;grid-row:2;padding-bottom:6px}}',
      'html body .nli .nlcp button.nlcp__edit{min-height:44px;padding:0 10px;border:0 !important;background:none !important;color:var(--nli-sea) !important;font:500 14px/20px var(--nli-sans) !important;text-decoration:underline;text-underline-offset:3px;cursor:pointer;margin:0;box-shadow:none !important;text-transform:none !important;letter-spacing:0 !important}',
      '.nlcp .nlcp__note{font:400 14px/22px var(--nli-sans);color:var(--nli-ink2);margin:0;padding:10px 12px;border-inline-start:3px solid var(--nli-sea);background:var(--nli-ground)}',
      '.nlcp .nlcp__note.is-lead{border-inline-start-color:var(--nli-open)}',
      '.nlcp .nlcp__aim{font:400 14px/22px var(--nli-sans);color:var(--nli-ink2);margin:0}',
      /* radio cards */
      'html body .nli .nlcp fieldset.nlcp__set{border:0 !important;margin:0 !important;padding:0 !important;min-width:0;background:none !important}',
      'html body .nli .nlcp fieldset.nlcp__set>legend{padding:0;margin:0 0 8px;font:500 14px/20px var(--nli-sans);color:var(--nli-ink)}',
      '.nlcp .nlcp__cards{display:grid;gap:8px}',
      '@media (min-width:700px){.nlcp .nlcp__cards.is-3{grid-template-columns:repeat(3,minmax(0,1fr))}.nlcp .nlcp__cards.is-2{grid-template-columns:repeat(2,minmax(0,1fr))}}',
      'html body .nli .nlcp label.nlcp__card{position:relative;display:flex;gap:12px;align-items:flex-start;min-height:56px;padding:12px 14px;border:1px solid var(--nli-line);border-radius:var(--nli-r-m);background:var(--nli-surface);cursor:pointer;margin:0;font-weight:400}',
      'html body .nli .nlcp label.nlcp__card:hover{border-color:var(--nli-sea)}',
      'html body .nli .nlcp label.nlcp__card input{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:pointer;z-index:1}',
      '.nlcp .nlcp__dot{flex:none;width:20px;height:20px;margin-top:1px;border:2px solid var(--nli-ink2);border-radius:50%;background:var(--nli-surface);box-sizing:border-box}',
      'html body .nli .nlcp label.nlcp__card:has(input:checked){border-color:var(--nli-sea);background:var(--nli-ground)}',
      '.nlcp .nlcp__card:has(input:checked) .nlcp__dot{border:6px solid var(--nli-sea)}',
      '.nlcp .nlcp__card:has(input:focus-visible){outline:2px solid var(--nli-focus);outline-offset:2px}',
      '.nlcp .nlcp__ct{display:grid;gap:3px;min-width:0}',
      '.nlcp .nlcp__ct b{font:600 16px/22px var(--nli-sans);color:var(--nli-ink)}',
      '.nlcp .nlcp__ct small{font:400 14px/20px var(--nli-sans);color:var(--nli-ink2)}',
      '.nlcp .nlcp__price{font:500 17px/24px var(--nli-sans);color:var(--nli-ink)}.nlcp .nlcp__price bdi{font-weight:500}',
      '.nlcp .nlcp__tag{justify-self:start;margin-top:4px;padding:1px 8px;border:1px solid var(--nli-sea);border-radius:999px;font:500 12px/18px var(--nli-sans);color:var(--nli-sea-deep)}',
      /* fields */
      'html body .nli .nlcp .nli__f>label{font:500 14px/20px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 !important}',
      'html body .nli .nlcp .nli__in input{font-family:var(--nli-mono) !important;border-radius:0 !important;min-height:46px}',
      'html body .nli .nlcp .nli__in input.is-text{font-family:var(--nli-sans) !important;direction:inherit;text-align:start}',
      'html body .nli .nlcp[dir="ltr"] .nli__in input{text-align:left}',
      'html body .nli .nlcp .nli__in:has(input[aria-invalid="true"]){border-color:var(--nli-ink);outline:1px solid var(--nli-ink);outline-offset:-2px}',
      '.nlcp .nlcp__msg{font:500 14px/20px var(--nli-sans);color:var(--nli-ink);margin:0}',
      '.nlcp .nlcp__msg:not(:empty){padding:8px 12px;background:var(--nli-ground);border-inline-start:3px solid var(--nli-sea-deep)}',
      '.nlcp .nlcp__two{display:grid;gap:12px}',
      '@media (min-width:600px){.nlcp .nlcp__two{grid-template-columns:repeat(2,minmax(0,1fr))}}',
      /* budget */
      '.nlcp .nlcp__stp{display:grid;grid-template-columns:48px minmax(0,1fr) 48px;gap:8px;align-items:stretch}',
      'html body .nli .nlcp .nlcp__stp button,html body .nli .nlcp .nlcp__ar button{min-height:48px;min-width:44px;border:1px solid var(--nli-line) !important;border-radius:var(--nli-r-s) !important;background:var(--nli-surface) !important;color:var(--nli-ink) !important;font:500 22px/1 var(--nli-mono) !important;padding:0 !important;cursor:pointer;margin:0;box-shadow:none !important}',
      'html body .nli .nlcp .nlcp__stp button:hover,html body .nli .nlcp .nlcp__ar button:hover{border-color:var(--nli-sea) !important}',
      'html body .nli .nlcp .nlcp__stp button[disabled],html body .nli .nlcp .nlcp__ar button[disabled]{opacity:.4;cursor:default}',
      'html body .nli .nlcp input.nlcp__range{display:block;width:100%;height:44px;margin:4px 0 0;padding:0 !important;border:0 !important;background:transparent !important;box-shadow:none !important;accent-color:var(--nli-sea);cursor:pointer}',
      'html body .nli .nlcp .nlcp__help{font:400 13px/18px var(--nli-sans);color:var(--nli-mute);margin:0}',
      '.nlcp .nlcp__read{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:8px}',
      '.nlcp .nlcp__read>div{display:grid;gap:2px;padding:12px;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-ground);min-width:0}',
      '.nlcp .nlcp__read span{font:500 13px/18px var(--nli-sans);color:var(--nli-ink2)}',
      '.nlcp .nlcp__read output{display:block;font:500 24px/30px var(--nli-mono);color:var(--nli-ink);font-variant-numeric:tabular-nums;overflow-wrap:anywhere}',
      '.nlcp .nlcp__read output.is-survey{color:var(--nli-survey);font-size:28px;line-height:34px}',
      '@media (min-width:520px){.nlcp .nlcp__read output{font-size:28px;line-height:34px}.nlcp .nlcp__read output.is-survey{font-size:36px;line-height:42px}}',
      '.nlcp .nlcp__sbar{display:flex;height:16px;border-radius:var(--nli-r-s);overflow:hidden;background:var(--nli-line);margin:8px 0 0}',
      '.nlcp .nlcp__sbar i{display:block;height:100%}',
      '.nlcp .nlcp__f-meta{background:#2F6F86}.nlcp .nlcp__f-google{background:#1F4B5C}.nlcp .nlcp__f-press{background:#4F9A5C}.nlcp .nlcp__f-boards{background:#8E7CC3}',
      'html body .nli .nlcp ul.nlcp__lg{list-style:none !important;margin:8px 0 0 !important;padding:0 !important;display:grid;gap:0}',
      'html body .nli .nlcp ul.nlcp__lg li{display:grid;grid-template-columns:12px minmax(0,1fr) auto auto;gap:4px 10px;align-items:center;margin:0 !important;padding:7px 0 !important;border-bottom:1px solid var(--nli-line);font:400 14px/20px var(--nli-sans) !important;color:var(--nli-ink2) !important}',
      'html body .nli .nlcp ul.nlcp__lg li::before{display:none !important;content:none !important}',
      '.nlcp .nlcp__lg b{display:block;width:12px;height:12px;border-radius:2px}',
      '.nlcp .nlcp__lg .p{color:var(--nli-mute)}.nlcp .nlcp__lg .a{color:var(--nli-ink);min-width:6.5em;text-align:end}',
      'html body .nli .nlcp details.nlcp__adj{margin:4px 0 0;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);padding:0 12px}',
      'html body .nli .nlcp details.nlcp__adj>summary{min-height:44px;display:flex;align-items:center;gap:12px;font:500 15px/22px var(--nli-sans);color:var(--nli-sea);cursor:pointer;list-style:none}',
      '.nlcp details.nlcp__adj>summary::-webkit-details-marker{display:none}',
      '.nlcp details.nlcp__adj>summary::after{content:"";flex:none;width:8px;height:8px;margin-inline-start:auto;margin-top:-4px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg)}',
      '.nlcp details.nlcp__adj[open]>summary::after{margin-top:4px;transform:rotate(-135deg)}',
      '.nlcp .nlcp__ar{display:grid;grid-template-columns:minmax(0,1fr) 44px 64px 44px;gap:8px;align-items:center;padding:6px 0;border-top:1px solid var(--nli-line)}',
      '.nlcp .nlcp__ar>span{font:400 14px/20px var(--nli-sans);color:var(--nli-ink2);min-width:0}',
      '.nlcp .nlcp__ar output{text-align:center;font:500 16px/22px var(--nli-mono);color:var(--nli-ink)}',
      '.nlcp .nlcp__sum{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:8px 0;border-top:1px solid var(--nli-line);font:500 14px/20px var(--nli-sans);color:var(--nli-ink)}',
      'html body .nli .nlcp button.nlcp__reset{min-height:44px;padding:8px 14px;margin:0 0 10px;border:1px dashed var(--nli-sea) !important;border-radius:var(--nli-r-s) !important;background:none !important;color:var(--nli-sea) !important;font:500 14px/20px var(--nli-sans) !important;cursor:pointer;box-shadow:none !important}',
      /* consent and privacy */
      '.nlcp .nlcp__priv{font:400 13px/20px var(--nli-sans);color:var(--nli-ink2);margin:0}',
      'html body .nli .nlcp .nlcp__priv a{color:var(--nli-sea) !important;text-decoration:underline;text-underline-offset:3px}',
      'html body .nli .nlcp label.nlcp__chk{display:flex;gap:12px;align-items:flex-start;min-height:48px;padding:12px;margin:0;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);cursor:pointer;font:400 14px/22px var(--nli-sans) !important;color:var(--nli-ink) !important}',
      'html body .nli .nlcp label.nlcp__chk input{width:22px;height:22px;min-height:0;margin:0;flex:none;accent-color:var(--nli-sea);cursor:pointer}',
      'html body .nli .nlcp label.nlcp__chk:has(input:checked){border-color:var(--nli-sea);background:var(--nli-ground)}',
      'html body .nli .nlcp label.nlcp__chk:has(input[aria-invalid="true"]){border-color:var(--nli-ink);outline:1px solid var(--nli-ink);outline-offset:-2px}',
      '.nlcp .nlcp__hp{position:absolute !important;inset-inline-start:-10000px;top:auto;width:1px;height:1px;overflow:hidden}',
      /* footer */
      '.nlcp .nlcp__ft{display:flex;align-items:center;gap:8px;margin-top:24px;padding-top:16px;border-top:1px solid var(--nli-line)}',
      'html body .nli .nlcp .nlcp__ft button{min-height:48px;padding:12px 20px;border-radius:var(--nli-r-s) !important;font:600 16px/22px var(--nli-sans) !important;cursor:pointer;margin:0;box-shadow:none !important;text-transform:none !important;letter-spacing:0 !important}',
      'html body .nli .nlcp .nlcp__ft .is-back{background:var(--nli-surface) !important;color:var(--nli-ink) !important;border:1px solid var(--nli-line) !important}',
      'html body .nli .nlcp .nlcp__ft .is-back:hover{border-color:var(--nli-sea) !important}',
      'html body .nli .nlcp .nlcp__ft .is-primary{margin-inline-start:auto;flex:0 1 320px;background:var(--nli-sea) !important;color:var(--nli-on-sea) !important;border:1px solid var(--nli-sea) !important}',
      'html body .nli .nlcp .nlcp__ft .is-primary:hover{background:var(--nli-sea-deep) !important;border-color:var(--nli-sea-deep) !important}',
      'html body .nli .nlcp .nlcp__ft button[disabled]{opacity:.65;cursor:progress}',
      '@media (max-width:520px){html body .nli .nlcp .nlcp__ft .is-primary{flex:1 1 auto}}',
      /* side panel (wide screens) */
      '.nlcp .nlcp__side{display:none}',
      '@media (min-width:860px){.nlcp .nlcp__side{display:block;align-self:start;position:sticky;top:96px;padding:16px;border:1px solid var(--nli-line);border-radius:var(--nli-r-m);background:var(--nli-ground)}}',
      'html body .nli .nlcp .nlcp__side h3{font:600 15px/22px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 8px !important;letter-spacing:0;text-transform:none}',
      'html body .nli .nlcp .nlcp__side dl.nlcp__mini>div{display:grid;gap:2px;justify-content:stretch}',
      'html body .nli .nlcp .nlcp__side dl.nlcp__mini dd{text-align:start}',
      /* done */
      '.nlcp .nlcp__done{display:grid;gap:14px}',
      '.nlcp .nlcp__refbox{padding:14px 16px;border:1px solid var(--nli-line);border-inline-start:3px solid var(--nli-open);border-radius:var(--nli-r-s);background:var(--nli-ground)}',
      '.nlcp .nlcp__refbox span{display:block;font:500 13px/18px var(--nli-sans);color:var(--nli-ink2)}',
      '.nlcp .nlcp__ref{display:block;font:500 28px/36px var(--nli-mono);color:var(--nli-ink);letter-spacing:.02em}',
      'html body .nli .nlcp .nlcp__done p{margin:0}',
      '.nlcp .nlcp__refbox p{margin:6px 0 0;font:400 14px/22px var(--nli-sans);color:var(--nli-ink2)}',
      'html body .nli .nlcp h4.nlcp__h4{font:600 17px/24px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:6px 0 0 !important;letter-spacing:0;text-transform:none}',
      'html body .nli .nlcp a.nlcp__pay{display:flex;align-items:center;justify-content:center;text-align:center;min-height:52px;padding:12px 20px;border-radius:var(--nli-r-s);background:var(--nli-sea);color:var(--nli-on-sea) !important;font:600 16px/22px var(--nli-sans);text-decoration:none !important}',
      'html body .nli .nlcp a.nlcp__pay:hover{background:var(--nli-sea-deep)}',
      'html body .nli .nlcp .nli__share{margin-top:0}',
      'html body .nli .nlcp .nli__share button,html body .nli .nlcp .nli__share a{font-family:var(--nli-sans) !important;letter-spacing:0 !important;text-transform:none !important;box-shadow:none !important}',
      '@media print{.nlcp .nlcp__ft,.nlcp .nli__share,.nlcp button.nlcp__edit,.nlcp .nlcp__side{display:none !important}}'
    ].join('\n');
    document.head.appendChild(s);
  }

  function mount(root) {
    var LG = langFor(root), t = T(LG), DIR = LG === 'he' ? 'rtl' : 'ltr';
    css();
    if (G.NLCAMP_CONFIG) configure(G.NLCAMP_CONFIG);
    var uid = 'nlcp-' + Math.random().toString(36).slice(2, 7), st = newState(), t0 = Date.now(), sent = null, sending = false, err = {}, hp = null;
    var names = ['', t.s1, t.s2, t.s3, t.s4, t.s5], ledes = ['', t.s1lede, t.s2lede, t.s3lede, t.s4lede, t.s5lede];
    root.innerHTML = ''; root.setAttribute('dir', DIR);
    var P = el('div', 'nli__panel nlcp'); P.id = uid; P.setAttribute('dir', DIR); P.setAttribute('lang', LG);
    P.innerHTML = '<header class="nlcp__hd"><div><p class="nli__kicker">' + esc(t.kicker) + '</p><h2 class="nli__title">' + esc(t.title) + '</h2></div><p class="nlcp__count" aria-hidden="true"><bdi></bdi></p></header>'
      + '<div class="nlcp__bar" role="progressbar" aria-label="' + esc(t.progress) + '" aria-valuemin="1" aria-valuemax="5"><i></i><i></i><i></i><i></i><i></i></div>'
      + '<div class="nlcp__grid"><form class="nlcp__form" novalidate><h3 class="nlcp__h" tabindex="-1"></h3><p class="nlcp__lede"></p><div class="nlcp__body"></div>'
      + '<div class="nlcp__ft"><button type="button" class="is-back" data-act="back">' + esc(t.back) + '</button><button type="submit" class="is-primary" data-act="next"></button></div></form>'
      + '<aside class="nlcp__side" aria-label="' + esc(t.side) + '"><h3>' + esc(t.side) + '</h3><dl class="nlcp__mini"></dl></aside></div>';
    root.appendChild(P);
    var Q = function (s) { return P.querySelector(s); };
    var form = Q('form'), head = Q('.nlcp__h'), lede = Q('.nlcp__lede'), body = Q('.nlcp__body'), count = Q('.nlcp__count bdi'), bar = Q('.nlcp__bar'),
      back = Q('[data-act="back"]'), next = Q('[data-act="next"]'), sideDl = Q('.nlcp__side dl'), sendMsg = null;
    back.addEventListener('click', function () { if (st.step > 1 && !sent) go(st.step - 1); });
    form.addEventListener('submit', function (e) { e.preventDefault(); if (sent || sending) return; if (st.step < 5) { var es = validate(st, st.step); if (es.length) return showErrors(es); go(st.step + 1); } else submit(); });

    function endpoint() { return NLCAMP.endpoint || root.getAttribute('data-endpoint') || (location.origin + '/wp-json/nadlan/v1/campaign-brief'); }
    function msgSlot(f) { var m = el('p', 'nlcp__msg'); m.id = uid + '-e-' + f; m.setAttribute('aria-live', 'polite'); err[f] = m; return m; }
    function clearErr(f) { if (err[f]) err[f].textContent = ''; var c = P.querySelector('[data-f="' + f + '"]'); if (c) c.removeAttribute('aria-invalid'); }
    function errText(x) {
      var o = { min: money(BUDGET.min, LG), max: money(BUDGET.max, LG), step: money(BUDGET.step, LG) };
      if (x.f === 'split') return tpl(t.e_split, { sum: x.sum + '%' });
      if (x.f === 'budget') return tpl(t.e_budget, o);
      if (x.code === 'cover') { var n = st.markets.length, mx = plans[st.plan].markets; return tpl(t.e_cover, { n: countText(n, LG), plan: t['p_' + st.plan], max: LG === 'en' ? 'room for ' + countText(mx, LG) : toText(mx) }); }
      return t['e_' + x.f] || t.e_send;
    }
    function showErrors(es) {
      var first = null;
      es.forEach(function (x) {
        if (err[x.f]) { err[x.f].textContent = errText(x); var dt = err[x.f].closest('details'); if (dt) dt.open = true; }
        var c = P.querySelector('[data-f="' + x.f + '"]'); if (c) { c.setAttribute('aria-invalid', 'true'); if (!first) first = c; } else if (!first && err[x.f]) first = err[x.f];
      });
      if (first) { if (first.focus && first.matches('input,button')) first.focus(); else if (first.scrollIntoView) first.scrollIntoView({ block: 'center' }); }
    }
    function go(n) {
      st.step = n;
      if (n === 5 && !st.planTouched) st.plan = recommend(st.markets.length);
      render(); toTop();
    }
    function toTop() {  // the new step starts at the top of the tool (below the site's sticky header), focus on its heading
      var top = P.getBoundingClientRect().top;
      if (top < 0 || top > window.innerHeight * 0.5) window.scrollTo(0, Math.max(0, window.pageYOffset + top - 88));
      head.focus({ preventScroll: true });
    }
    function render() {
      var n = sent ? 5 : st.step; err = {}; sendMsg = null;
      count.textContent = n + ' / 5';
      [].forEach.call(bar.children, function (i, k) { i.className = sent || k < n - 1 ? 'is-on' : k === n - 1 ? 'is-now' : ''; });
      bar.setAttribute('aria-valuenow', String(n)); bar.setAttribute('aria-valuetext', tpl(t.stepOf, { n: n, name: names[n] }));
      head.textContent = sent ? t.doneTitle : names[n]; lede.textContent = sent ? '' : ledes[n]; lede.hidden = !!sent;
      body.innerHTML = '';
      if (sent) bDone(); else [null, b1, b2, b3, b4, b5][n]();
      back.hidden = !!sent || n === 1; next.hidden = !!sent; Q('.nlcp__ft').hidden = !!sent;
      next.textContent = n === 5 ? t.send : t.next; next.disabled = false;
      side();
    }
    function side() {
      var L = lines(st, LG).filter(function (l) { return l.k !== 'split' && l.k !== 'plan'; }), r = recommend(st.markets.length);
      sideDl.innerHTML = L.map(function (l) { return '<div><dt>' + esc(l.label) + '</dt><dd>' + l.html + '</dd></div>'; }).join('')
        + '<div><dt>' + esc(t.d_rec) + '</dt><dd>' + (r ? esc(t['p_' + r]) + ', ' + B(planPrice(r, LG)) + ' ' + esc(t.perYearShort) : esc(t.none)) + '</dd></div>';
    }
    function radios(name, legend, items, cur, cols, onPick) {
      var fs = el('fieldset', 'nlcp__set'), lg = el('legend', legend.hide ? 'nlcp__sr' : '', esc(legend.text)); fs.appendChild(lg);
      var box = el('div', 'nlcp__cards' + (cols ? ' is-' + cols : '')); fs.appendChild(box);
      items.forEach(function (it, i) {
        var lab = el('label', 'nlcp__card');
        lab.innerHTML = '<input type="radio" name="' + uid + '-' + name + '" value="' + esc(it.v) + '"' + (cur === it.v ? ' checked' : '') + (i === 0 ? ' data-f="' + name + '"' : '') + '>'
          + '<span class="nlcp__dot" aria-hidden="true"></span><span class="nlcp__ct"><b>' + esc(it.t) + '</b>' + (it.extra || '') + '<small>' + esc(it.d) + '</small>' + (it.tag || '') + '</span>';
        lab.querySelector('input').addEventListener('change', function (e) { if (e.target.checked) { onPick(it.v); clearErr(name); side(); } });
        box.appendChild(lab);
      });
      fs.appendChild(msgSlot(name));
      return fs;
    }
    function textField(f, label, val, opt) {
      var w = el('div', 'nli__f'), id = uid + '-' + f;
      w.innerHTML = '<label for="' + id + '">' + esc(label) + '</label><div class="nli__in"><input id="' + id + '" data-f="' + f + '" type="' + (opt.type || 'text') + '"'
        + (opt.text ? ' class="is-text" dir="auto"' : '') + (opt.ac ? ' autocomplete="' + opt.ac + '"' : '') + (opt.im ? ' inputmode="' + opt.im + '"' : '')
        + ' maxlength="' + (opt.max || 120) + '" aria-describedby="' + id + '-h ' + uid + '-e-' + f + '"></div>' + (opt.help ? '<span class="nlcp__help" id="' + id + '-h">' + esc(opt.help) + '</span>' : '');
      var inp = w.querySelector('input'); inp.value = val || '';
      if (!opt.help) inp.setAttribute('aria-describedby', uid + '-e-' + f);
      inp.addEventListener('input', function () { opt.set(inp.value); clearErr(f); if (opt.after) opt.after(); });
      w.appendChild(msgSlot(f));
      return w;
    }

    /* 1. markets and communities */
    function b1() {
      var g = el('div', 'nlcp__chips'); g.setAttribute('role', 'group'); g.setAttribute('aria-label', t.s1group); g.setAttribute('aria-describedby', uid + '-e-markets');
      MARKETS.forEach(function (m, i) {
        var b = el('button', 'nlcp__chip', CHECK + '<span>' + esc(t['m_' + m.id]) + '</span><small><span aria-hidden="true">' + m.langs.map(function (l) { return l.toUpperCase(); }).join(' · ') + '</span><span class="nlcp__sr">'
          + esc(m.langs.map(function (l) { return t['l_' + l]; }).join(', ')) + '</span></small>');
        b.type = 'button'; b.setAttribute('data-m', m.id); b.setAttribute('aria-pressed', String(st.markets.indexOf(m.id) > -1)); if (i === 0) b.setAttribute('data-f', 'markets');
        b.addEventListener('click', function () { toggleMarket(st, m.id); b.setAttribute('aria-pressed', String(st.markets.indexOf(m.id) > -1)); clearErr('markets'); read(); side(); });
        g.appendChild(b);
      });
      body.appendChild(g); body.appendChild(msgSlot('markets'));
      body.appendChild(el('p', 'nlcp__aim', esc(t.s1aim)));
      var dl = el('dl', 'nlcp__mini'); dl.setAttribute('aria-live', 'polite'); body.appendChild(dl);
      function read() {
        var n = st.markets.length, r = recommend(n);
        dl.innerHTML = '<div><dt>' + esc(t.langsLab) + '</dt><dd data-o="langs">' + esc(n ? langsOf(st.markets).map(function (l) { return t['l_' + l]; }).join(', ') : t.none) + '</dd></div>'
          + '<div><dt>' + esc(t.recLab) + '</dt><dd data-o="rec">' + (r ? esc(t['p_' + r]) + ', ' + B(planPrice(r, LG)) + ' ' + esc(t.perYearShort) : esc(t.none)) + '</dd></div>';
      }
      read();
    }
    /* 2. buyers */
    function b2() {
      body.appendChild(radios('buyer', { text: t.s2, hide: true }, BUYERS.map(function (k) { return { v: k, t: t['b_' + k], d: t['b_' + k + '_d'] }; }), st.buyer, 2, function (v) { st.buyer = v; }));
    }
    /* 3. budget and split */
    function b3() {
      var id = uid + '-budget', w = el('div', 'nli__f');
      w.innerHTML = '<label for="' + id + '">' + esc(t.budgetLab) + '</label><div class="nlcp__stp"><button type="button" data-act="minus" aria-label="' + esc(tpl(t.minus, { step: money(BUDGET.step, LG) })) + '">−</button>'
        + '<div class="nli__in"><input id="' + id + '" data-f="budget" type="text" inputmode="numeric" autocomplete="off" aria-describedby="' + id + '-h ' + uid + '-e-budget"><span class="nli__unit">' + esc(t.budgetUnit) + '</span></div>'
        + '<button type="button" data-act="plus" aria-label="' + esc(tpl(t.plus, { step: money(BUDGET.step, LG) })) + '">+</button></div>'
        + '<input type="range" class="nlcp__range" min="' + BUDGET.min + '" max="' + BUDGET.max + '" step="' + BUDGET.step + '" aria-label="' + esc(t.slider) + '">'
        + '<span class="nlcp__help" id="' + id + '-h">' + tplH(t.budgetHelp, { min: B(money(BUDGET.min, LG)), max: B(money(BUDGET.max, LG)), step: B(money(BUDGET.step, LG)) }) + '</span>';
      w.appendChild(msgSlot('budget')); body.appendChild(w);
      var inp = w.querySelector('#' + id), rng = w.querySelector('input[type="range"]'), mi = w.querySelector('[data-act="minus"]'), pl = w.querySelector('[data-act="plus"]');
      var rd = el('div', 'nlcp__read', '<div><span>' + esc(t.perMonth) + '</span><output data-o="m"></output></div><div><span>' + esc(t.perYear) + '</span><output data-o="y" class="is-survey"></output></div>');
      body.appendChild(rd);
      body.appendChild(el('p', 'nlcp__note', esc(t.paidDirect)));
      var sp = el('div', 'nlcp__split'); body.appendChild(sp);
      sp.innerHTML = '<span class="nli__alab" data-o="slab"></span><div class="nlcp__sbar" role="img"></div><ul class="nlcp__lg"></ul><p class="nlcp__help">' + esc(t.splitNote) + '</p>';
      var adj = el('details', 'nlcp__adj'); adj.innerHTML = '<summary>' + esc(t.adjust) + '</summary>'; body.appendChild(adj);
      SPLIT.forEach(function (c, i) {
        var r = el('div', 'nlcp__ar', '<span>' + esc(t['ch_' + c.k]) + '</span><button type="button" data-sh="' + i + '" data-d="-1" aria-label="' + esc(tpl(t.shLess, { ch: t['chs_' + c.k] })) + '">−</button><output data-o="sh' + i + '"></output><button type="button" data-sh="' + i + '" data-d="1" aria-label="' + esc(tpl(t.shMore, { ch: t['chs_' + c.k] })) + '">+</button>');
        adj.appendChild(r);
      });
      adj.appendChild(el('div', 'nlcp__sum', '<span>' + esc(t.sum) + '</span><output data-o="sum"></output>'));
      var rs = el('button', 'nlcp__reset', esc(t.reset)); rs.type = 'button'; adj.appendChild(rs);
      adj.appendChild(msgSlot('split'));
      [].forEach.call(adj.querySelectorAll('[data-sh]'), function (b) { b.addEventListener('click', function () { stepShare(st, +b.getAttribute('data-sh'), +b.getAttribute('data-d')); clearErr('split'); paint(); side(); }); });
      rs.addEventListener('click', function () { st.shares = SPLIT.map(function (c) { return c.pct; }); clearErr('split'); paint(); side(); });
      function show() { inp.value = budgetOk(st.budget) ? nfmt(st.budget, LG) : (isFinite(st.budget) ? String(st.budget) : ''); }
      function paint() {
        var ok = budgetOk(st.budget), b = ok ? st.budget : clampBudget(st.budget), sum = splitSum(st.shares), dflt = st.shares.every(function (x, i) { return x === SPLIT[i].pct; });
        rng.value = String(b); mi.disabled = ok && b <= BUDGET.min; pl.disabled = ok && b >= BUDGET.max;
        rd.querySelector('[data-o="m"]').innerHTML = ok ? B(money(b, LG)) : esc(t.none);
        rd.querySelector('[data-o="y"]').innerHTML = ok ? B(money(yearly(b), LG)) : esc(t.none);
        var A = splitAmounts(b, st.shares);
        sp.querySelector('[data-o="slab"]').textContent = dflt ? t.splitLab : t.splitMine;
        var sb = sp.querySelector('.nlcp__sbar'); sb.innerHTML = A.map(function (a) { return a.pct > 0 ? '<i class="nlcp__f-' + a.k + '" style="width:' + (sum ? 100 * a.pct / Math.max(sum, 100) : 0) + '%"></i>' : ''; }).join('');
        sb.setAttribute('aria-label', A.map(function (a) { return t['chs_' + a.k] + ' ' + a.pct + '%'; }).join(', '));
        sp.querySelector('.nlcp__lg').innerHTML = A.map(function (a) { return '<li><b class="nlcp__f-' + a.k + '"></b><span>' + esc(t['ch_' + a.k]) + '</span><bdi class="p">' + a.pct + '%</bdi><bdi class="a">' + (ok ? esc(money(a.amount, LG)) : '') + '</bdi></li>'; }).join('');
        SPLIT.forEach(function (c, i) { adj.querySelector('[data-o="sh' + i + '"]').innerHTML = B(st.shares[i] + '%'); adj.querySelector('[data-sh="' + i + '"][data-d="-1"]').disabled = st.shares[i] <= 0; adj.querySelector('[data-sh="' + i + '"][data-d="1"]').disabled = st.shares[i] >= 100; });
        adj.querySelector('[data-o="sum"]').innerHTML = B(sum + '%');
      }
      inp.addEventListener('input', function () { var v = parseFloat(String(inp.value).replace(/[^\d.]/g, '')); st.budget = isFinite(v) ? v : NaN; clearErr('budget'); paint(); side(); });
      inp.addEventListener('blur', function () { if (budgetOk(st.budget)) show(); });
      rng.addEventListener('input', function () { st.budget = +rng.value; clearErr('budget'); show(); paint(); side(); });
      mi.addEventListener('click', function () { stepBudget(st, -1); clearErr('budget'); show(); paint(); side(); });
      pl.addEventListener('click', function () { stepBudget(st, 1); clearErr('budget'); show(); paint(); side(); });
      show(); paint();
    }
    /* 4. the project */
    function b4() {
      var ref = null;
      body.appendChild(radios('kind', { text: t.s4, hide: true }, KINDS.map(function (k) { return { v: k, t: t['k_' + k], d: t['k_' + k + '_d'] }; }), st.kind, 2, function (v) { st.kind = v; clearErr('ref'); fieldRef(); }));
      var slot = el('div', ''); body.appendChild(slot);
      body.appendChild(el('p', 'nlcp__note', esc(t.s4lede)));
      function fieldRef() {
        slot.innerHTML = ''; if (!st.kind) return;
        ref = textField('ref', st.kind === 'existing' ? t.refLabExisting : t.refLabNew, st.ref, { text: true, max: 200, ac: 'off', help: st.kind === 'existing' ? t.refHelpExisting : t.refHelpNew, set: function (v) { st.ref = v; }, after: side });
        slot.appendChild(ref);
      }
      fieldRef();
    }
    /* 5. summary, plan, contact, send */
    function b5() {
      var dl = el('dl', 'nlcp__dl');
      lines(st, LG).filter(function (l) { return l.k !== 'plan'; }).forEach(function (l) {
        var d = el('div', '', '<dt>' + esc(l.label) + '</dt><dd class="nlcp__v">' + l.html + '</dd><dd class="nlcp__e"></dd>');
        var e = el('button', 'nlcp__edit', esc(t.edit)); e.type = 'button'; e.setAttribute('data-go', String(l.step)); e.setAttribute('aria-label', tpl(t.editOf, { x: l.label }));
        e.addEventListener('click', function () { go(l.step); }); d.querySelector('.nlcp__e').appendChild(e); dl.appendChild(d);
      });
      body.appendChild(dl);
      var n = st.markets.length, r = recommend(n);
      body.appendChild(radios('plan', { text: t.planLab }, PLAN_ORDER.map(function (k) {
        return { v: k, t: t['p_' + k], d: t['p_' + k + '_d'], extra: '<span class="nlcp__price">' + B(planPrice(k, LG)) + ' ' + esc(t.perYearShort) + '</span>',
          tag: k === r ? '<span class="nlcp__tag">' + tplH(t.recTag, { n: LG === 'en' ? countHTML(n, LG) : toHTML(n) }) + '</span>' : '' };
      }), st.plan, 3, function (v) { st.plan = v; st.planTouched = true; }));
      body.appendChild(el('p', 'nlcp__note', esc(t.planNote)));
      body.appendChild(el('p', 'nlcp__note is-lead', esc(t.leads)));
      body.appendChild(shareBar());
      var cf = el('fieldset', 'nlcp__set'); cf.appendChild(el('legend', '', esc(t.contactLab)));
      var two = el('div', 'nlcp__two'); cf.appendChild(two);
      two.appendChild(textField('name', t.f_name, st.name, { text: true, ac: 'name', set: function (v) { st.name = v; } }));
      two.appendChild(textField('company', t.f_company, st.company, { text: true, ac: 'organization', set: function (v) { st.company = v; } }));
      two.appendChild(textField('phone', t.f_phone, st.phone, { type: 'tel', ac: 'tel', im: 'tel', max: 24, set: function (v) { st.phone = v; } }));
      two.appendChild(textField('email', t.f_email, st.email, { type: 'email', ac: 'email', im: 'email', max: 160, set: function (v) { st.email = v; } }));
      var hw = el('div', 'nlcp__hp', '<label>' + esc(t.hp) + ' <input type="text" name="website" tabindex="-1" autocomplete="off"></label>'); hw.setAttribute('aria-hidden', 'true'); cf.appendChild(hw); hp = hw.querySelector('input');
      body.appendChild(cf);
      var priv = NLCAMP.privacy || '/privacy/';
      body.appendChild(el('p', 'nlcp__priv', esc(t.privacy) + ' <a href="' + esc(priv) + '" target="_blank" rel="noopener">' + esc(t.privacyLink) + '</a>'));
      var ck = el('label', 'nlcp__chk', '<input type="checkbox" data-f="consent"' + (st.consent ? ' checked' : '') + ' aria-describedby="' + uid + '-e-consent"><span>' + esc(t.consent) + '</span>');
      ck.querySelector('input').addEventListener('change', function (e) { st.consent = !!e.target.checked; clearErr('consent'); });
      body.appendChild(ck); body.appendChild(msgSlot('consent'));
      body.appendChild(el('p', 'nlcp__help', esc(t.notPay)));
      sendMsg = msgSlot('send'); body.appendChild(sendMsg);
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
    function text() { return summaryText(st, LG, sent, location.origin + location.pathname); }
    function submit() {
      var es = validateAll(st);
      if (es.length) { var s = es[0].step; if (s !== 5) go(s); return showErrors(es.filter(function (x) { return x.step === s; })); }
      sending = true; next.disabled = true; next.textContent = t.sending; if (sendMsg) sendMsg.textContent = '';
      var data = payload(st, LG, Date.now() - t0, location.pathname, hp ? hp.value : '');
      var fail = function (j) {
        sending = false; next.disabled = false; next.textContent = t.send;
        var f = j && j.data && j.data.field;
        if (f && err[f]) showErrors([{ f: f }]); else if (sendMsg) sendMsg.textContent = t.e_send;
      };
      var p;
      try { p = fetch(endpoint(), { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'omit', body: JSON.stringify(data) }); } catch (e) { return fail(null); }
      p.then(function (r) { return r.json().catch(function () { return null; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (x) {
          if (!x.ok || !x.j || x.j.ok !== true || !REF_RE.test(String(x.j.ref || ''))) return fail(x.j);
          sending = false; sent = String(x.j.ref); render(); toTop();
        }, function () { fail(null); });
    }
    /* after the brief is saved: the reference and the payment step */
    function bDone() {
      var w = el('div', 'nlcp__done');
      w.appendChild(el('div', 'nlcp__refbox', '<span>' + esc(t.refLab) + '</span><output class="nlcp__ref" data-o="ref">' + B(sent) + '</output><p>' + esc(t.doneText) + '</p>'));
      w.appendChild(el('h4', 'nlcp__h4', esc(t.payTitle)));
      var dl = el('dl', 'nlcp__mini'); var pl = lines(st, LG).filter(function (l) { return l.k === 'plan' || l.k === 'markets' || l.k === 'budget'; });
      dl.innerHTML = pl.map(function (l) { return '<div><dt>' + esc(l.label) + '</dt><dd>' + l.html + '</dd></div>'; }).join(''); w.appendChild(dl);
      var u = payUrl(st.plan, sent), fp = firstPay(st.plan), pn = esc(t['p_' + st.plan]), pp = B(planPrice(st.plan, LG));
      if (u) {
        var a = el('a', 'nlcp__pay', '<span>' + (fp ? tplH(t.payFirst, { first: B(money(fp, LG)), plan: pn, price: pp }) : tplH(t.payBtn, { plan: pn, price: pp })) + '</span>');
        a.href = u; a.setAttribute('data-act', 'pay');  // the words in one <span>: one flex item, so the spaces around the figure stay
        w.appendChild(a);
        if (fp) w.appendChild(el('p', 'nlcp__help', tplH(t.payRest, { rest: B(money(restOf(st.plan), LG)), part: B(money(fp, LG)) }))).setAttribute('data-o', 'rest');
        w.appendChild(el('p', 'nlcp__help', esc(t.payNote)));
      } else {
        w.appendChild(el('p', 'nlcp__note', esc(t.payLater)));
      }
      w.appendChild(el('p', 'nlcp__help', esc(t.launch)));
      w.appendChild(el('p', 'nlcp__note is-lead', esc(t.leads)));
      w.appendChild(shareBar());
      body.appendChild(w);
    }
    render();
  }
})();
