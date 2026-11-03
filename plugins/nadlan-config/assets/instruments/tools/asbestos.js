/* NadLan Instruments · asbestos v1 (HAD-668 R11e, Ben 3.11.2026: "the best asbestos page in the world, tools, price guides,
   the authorities, a map"). Four tools of one family, one file ('file' => 'asbestos' in inc/asbestos-tools.php):
   asbcheck  what do I have and what do I do: the item and its state lead to the steps, who to call and whether a permit is needed
             (the MoEP public guide and FAQ, the law and its exemption regulations, the Knesset research of 17.7.2023);
   asbcost   the price guide: the only public reference price (the MoEP home-contractor tender, via the Knesset) and the
             commercial ranges, each labelled as what it is; an estimate, never a quote;
   asbmap    the 348 sites of the Western Galilee friable-asbestos soil project in their three official statuses (MoEP layer),
             on a tilted map (MapLibre GL + OpenFreeMap, the soil map's stack), labelled by locality;
   asbwho    who to call by town: the town's environmental unit (MoEP list, 255 authorities), the licence holders counted in its
             district (MoEP registry, counts only, the names stay on gov.il), the landfill sites and the hotlines.
   Data: data/asbestos.json, built by tools/instruments/build_asbestos_data.py. Hebrew and English (TX, by the engine's lang). */
(function () {
  'use strict';
  if (!window.NadLanInstruments) return;
  var NLI = window.NadLanInstruments, F = NLI.fmt, esc = NLI.esc, EN = NLI.lang === 'en', LG = EN ? 'en' : 'he';
  function f(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  function hl(s) { return esc(s).replace(/\*6911/g, '<span dir="ltr">*6911</span>').replace(/073-2733200/g, '<span dir="ltr">073-2733200</span>'); }
  function t(x) { return x == null ? '' : (typeof x === 'string' ? x : (x[LG] != null ? x[LG] : x.he)); }
  var GOV = { registry: 'https://www.gov.il/he/Departments/DynamicCollectors/asbest_list', guide: 'https://www.gov.il/he/pages/asbestos_guide_for_public',
    faq: 'https://www.gov.il/he/pages/asbestos_faq', knesset: 'https://fs.knesset.gov.il/25/Committees/25_cs_bg_4141427.pdf',
    landfills: 'https://data.gov.il/dataset/asbestoslandfills', wg: 'https://www.gov.il/he/pages/western_galilee_asbestos' };

  /* ---------------------------------------------------------------- asbcheck: what do I have, what do I do */
  var ITEMS = [
    { id: 'roof', ac: 1, he: 'גג או גגון מלוחות גליים אפורים', en: 'Grey corrugated roof sheets or a roof shed' },
    { id: 'wall', ac: 1, he: 'לוחות קיר או חיפוי', en: 'Wall panels or cladding' },
    { id: 'pipe', ac: 1, he: 'צינור מים, ביוב או מרזב', en: 'A water, sewage or gutter pipe' },
    { id: 'chimney', ac: 1, he: 'ארובה או צינור פליטה', en: 'A chimney or flue pipe' },
    { id: 'planter', ac: 1, he: 'אדנית, עציץ או מכל', en: 'A planter, a pot or a tank' },
    { id: 'spray', fr: 1, he: 'ציפוי מרוסס, בידוד צנרת או תקרה אקוסטית', en: 'A sprayed coating, pipe lagging or an acoustic ceiling' },
    { id: 'soil', fr: 1, he: 'שברים אפורים באדמה או בשביל בגליל המערבי', en: 'Grey fragments in soil or a path in Western Galilee' },
    { id: 'debris', fr: 1, he: 'שברים אחרי שרפה, קריסה או פגיעה', en: 'Debris after a fire, a collapse or a strike' }
  ];
  var STATES = [
    { id: 'intact', he: 'שלם', en: 'Intact' }, { id: 'cracked', he: 'סדוק או שבור בחלקו', en: 'Cracked or partly broken' },
    { id: 'crumbling', he: 'מתפורר, שרוף או מפורק', en: 'Crumbling, burnt or broken up' }, { id: 'unsure', he: 'לא יודעים', en: 'Not sure' }
  ];
  var CX = {
    kicker: { he: 'בדיקה · אסבסט בבית', en: 'Check · Asbestos at home' },
    title: { he: 'מה יש לי ומה עושים', en: 'What do I have, and what do I do' },
    lede: { he: 'בוחרים מה מצאתם ובאיזה מצב הוא. מקבלים את הצעדים לפי ההנחיות של המשרד להגנת הסביבה, מי מורשה לטפל, והאם צריך היתר.',
      en: 'Choose what you found and the state it is in. You get the steps under the Ministry of Environmental Protection guidance, who is licensed to deal with it, and whether a permit is needed.' },
    q1: { he: 'מה מצאתם?', en: 'What did you find?' }, q2: { he: 'באיזה מצב?', en: 'In what state?' },
    lvLow: { he: 'שלם: לא מסוכן כל עוד לא פוגעים בו', en: 'Intact: not dangerous as long as it is left alone' },
    lvMid: { he: 'פגוע: לא לגעת, לתכנן פינוי מסודר', en: 'Damaged: do not touch it, plan a proper removal' },
    lvHigh: { he: 'אסבסט פריך או מפגע: מטפלים רק בידי מורשה', en: 'Friable asbestos or a hazard: only a licensed professional deals with it' },
    lvAsk: { he: 'לא ידוע: סקר של סוקר מורשה יגיד', en: 'Not known: a licensed surveyor will tell you' },
    now: { he: 'מה עושים עכשיו', en: 'What to do now' }, who: { he: 'מי מורשה לטפל', en: 'Who is licensed to deal with it' },
    permit: { he: 'היתר', en: 'Permit' },
    hot: { he: 'מפגע אסבסט מדווחים למוקד הסביבה של המשרד להגנת הסביבה: *6911 (שלוחה 5), 24 שעות ביממה.', en: 'Report an asbestos hazard to the Ministry of Environmental Protection environment hotline: *6911 (extension 5), 24 hours a day.' },
    reg: { he: 'לחיפוש בעלי רישיון במרשם הממשלתי', en: 'Search licence holders in the government registry (Hebrew)' },
    src: { he: 'לפי המדריך לציבור והשאלות הנפוצות של המשרד להגנת הסביבה (2025), החוק למניעת מפגעי אסבסט ואבק מזיק ותקנות הפטור, ומרכז המחקר והמידע של הכנסת (17.7.2023). מידע כללי, לא חוות דעת.',
      en: 'Based on the Ministry of Environmental Protection public guide and FAQ (2025), the Prevention of Asbestos and Harmful Dust Hazards Law and its exemption regulations, and the Knesset Research and Information Center (17.7.2023). General information, not a professional opinion.' }
  };
  var DO = {
    keep: { he: 'אל תקדחו, תחתכו, תשייפו, תשברו או תשטפו בלחץ מים. כך הוא נשאר בטוח.', en: 'Do not drill, cut, sand, break or pressure-wash it. That is what keeps it safe.' },
    plan: { he: 'שיפוץ, התקנת מערכת סולרית או פינוי: עבודה של קבלן אסבסט מורשה. התקנת פאנלים על גג אסבסט מחייבת לפנות אותו קודם.', en: 'Renovation, solar panels or removal: work for a licensed asbestos contractor. Solar panels on an asbestos roof require removing it first.' },
    stop: { he: 'הפסיקו כל עבודה במקום, אל תטאטאו ואל תשאבו בשואב אבק.', en: 'Stop any work there, and do not sweep or vacuum.' },
    wet: { he: 'הרחיקו אנשים, סגרו חלונות, ואל תנסו לפנות לבד.', en: 'Keep people away, close the windows, and do not try to clear it yourself.' },
    report: { he: 'מפגע אחרי שרפה, קריסה או פגיעה: דווחו למוקד *6911 (שלוחה 5).', en: 'A hazard after a fire, a collapse or a strike: report it to *6911 (extension 5).' },
    survey: { he: 'הזמינו סקר אסבסט: סוקר מורשה (או עובד אחראי או מפקח, שגם להם סמכות סקר) בודק ונותן חוות דעת בתשלום.', en: 'Order an asbestos survey: a licensed surveyor (or a worker in charge or an inspector, who also hold survey authority) inspects and gives a paid opinion.' },
    lab: { he: 'דגימת אוויר בזמן העבודה ואחריה: מעבדה מורשית לדיגום.', en: 'Air sampling during and after the work: a licensed sampling laboratory.' },
    small: { he: 'מוצר קטן (אדנית או עציץ) עד 700 ק״ג מותר לסלק לבד: להרטיב, לעטוף בשתי שכבות פוליאתילן בעובי 0.15 מ״מ, לסגור בסרט הדבקה, לסמן באזהרת אסבסט ולהביא לאתר הטמנה מורשה.',
      en: 'A small product (a planter or a pot) up to 700 kg may be disposed of yourself: wet it, wrap it in two layers of 0.15 mm polyethylene, seal it with tape, label it with an asbestos warning and take it to a licensed landfill site.' },
    water: { he: 'צינורות מי שתייה מאסבסט-צמנט: איכות מי השתייה באחריות משרד הבריאות.', en: 'Asbestos-cement drinking-water pipes: drinking-water quality is the Ministry of Health\'s responsibility.' },
    over50: { he: 'פינוי של יותר מ־50 מ״ר מחייב קבלן מורשה, על חשבון הבעלים. בתל אביב יפו העירייה דורשת קבלן מורשה גם מתחת ל־50 מ״ר.', en: 'Removing more than 50 m² requires a licensed contractor, at the owner\'s cost. Tel Aviv-Yafo requires a licensed contractor even under 50 m².' },
    wg: { he: 'בגליל המערבי פועל פרויקט ממלכתי לניקוי קרקעות מאסבסט פריך. בדקו את היישוב שלכם במפה בעמוד הזה.', en: 'Western Galilee has a state project to clean soils of friable asbestos. Check your locality on the map on this page.' }
  };
  var WHO = {
    ac: { he: 'קבלן אסבסט צמנט (או קבלן אסבסט פריך)', en: 'An asbestos-cement contractor (or a friable asbestos contractor)' },
    fr: { he: 'מפקח אסבסט פריך וגם קבלן אסבסט פריך', en: 'A friable asbestos inspector and a friable asbestos contractor' },
    fire: { he: 'קבלן אסבסט פריך, או מפקח אסבסט פריך עם קבלן אסבסט צמנט', en: 'A friable asbestos contractor, or a friable inspector together with an asbestos-cement contractor' },
    soil: { he: 'מפקח אסבסט פריך או קבלן אסבסט פריך', en: 'A friable asbestos inspector or a friable asbestos contractor' },
    survey: { he: 'סוקר אסבסט, מפקח אסבסט פריך או עובד אחראי', en: 'An asbestos surveyor, a friable inspector or a worker in charge' }
  };
  var PERMIT = {
    ac: { he: 'עבודה באסבסט צמנט דורשת היתר של המשרד להגנת הסביבה, חוץ מעבודה מצומצמת לפי תקנות הפטור. לפי החוק המשרד מחליט תוך 30 יום; לפי המשרד, בפועל כשבוע וחצי, ובמפגע באותו יום.',
      en: 'Asbestos-cement work needs a Ministry of Environmental Protection permit, except limited work under the exemption regulations. By law the Ministry decides within 30 days; per the Ministry, in practice about a week and a half, and for a hazard the same day.' },
    fr: { he: 'עבודה באסבסט פריך תמיד דורשת היתר של המשרד להגנת הסביבה ומפקח מורשה.', en: 'Friable asbestos work always needs a Ministry of Environmental Protection permit and a licensed inspector.' },
    none: { he: 'שמירה על מוצר שלם לא דורשת היתר. היתר נדרש כשמפרקים, מפנים או משפצים.', en: 'Keeping an intact product needs no permit. A permit is needed to dismantle, remove or renovate.' },
    small: { he: 'סילוק מוצר עד 700 ק״ג לפי ההנחיות לא דורש היתר.', en: 'Disposing of a product up to 700 kg under the guidance needs no permit.' }
  };
  function advise(item, state) {
    var it = ITEMS.filter(function (x) { return x.id === item; })[0], fr = !!it.fr || state === 'crumbling';
    var r = { steps: [], who: '', permit: '', lv: '', tone: '' };
    if (fr) {
      r.lv = CX.lvHigh; r.tone = 'high'; r.steps = [DO.stop, DO.wet];
      if (item === 'debris' || state === 'crumbling') r.steps.push(DO.report);
      if (item === 'soil') r.steps.push(DO.wg);
      r.steps.push(DO.lab);
      r.who = item === 'soil' ? WHO.soil : (item === 'debris' || (state === 'crumbling' && it.ac)) ? WHO.fire : WHO.fr; r.permit = PERMIT.fr;
    } else if (state === 'unsure') {
      r.lv = CX.lvAsk; r.tone = 'ask'; r.steps = [DO.keep, DO.survey]; r.who = WHO.survey; r.permit = PERMIT.none;
    } else if (state === 'cracked') {
      r.lv = CX.lvMid; r.tone = 'mid'; r.steps = [DO.keep, item === 'planter' ? DO.small : DO.over50, DO.survey]; r.who = WHO.ac; r.permit = item === 'planter' ? PERMIT.small : PERMIT.ac;
    } else {
      r.lv = CX.lvLow; r.tone = 'low'; r.steps = [DO.keep, item === 'planter' ? DO.small : DO.plan]; r.who = WHO.ac; r.permit = item === 'planter' ? PERMIT.small : PERMIT.none;
    }
    if (item === 'pipe') r.steps.push(DO.water);
    return r;
  }
  window.NLASB = { advise: advise, ITEMS: ITEMS, STATES: STATES };
  var C = NLI.pick(CX, LG);
  NLI.register('asbcheck', {
    custom: function (root) {
      var v = { item: 'roof', state: 'intact' };
      function chips(name, list) { return '<div class="asbx__q"><span>' + esc(name === 'item' ? C.q1 : C.q2) + '</span><div class="nls__chips asbx__chips" role="group">' + list.map(function (o) {
        return '<button type="button" data-k="' + name + '" data-v="' + o.id + '" aria-pressed="' + (v[name] === o.id) + '">' + esc(t(o)) + '</button>'; }).join('') + '</div></div>'; }
      root.innerHTML = '<div class="nli__panel asbx"><p class="nli__kicker">' + esc(C.kicker) + '</p><h2 class="nli__title">' + esc(C.title) + '</h2><p class="nli__lede">' + esc(C.lede) + '</p>'
        + chips('item', ITEMS) + chips('state', STATES) + '<div class="asbx__out" aria-live="polite"></div>'
        + '<p class="nli__note">' + hl(C.hot) + '</p><p class="nli__src">' + esc(C.src) + ' <a href="' + GOV.guide + '" target="_blank" rel="noopener">gov.il</a></p></div>';
      var out = root.querySelector('.asbx__out');
      function draw() {
        var r = advise(v.item, v.state);
        out.className = 'asbx__out is-' + r.tone;
        out.innerHTML = '<p class="asbx__lv">' + esc(t(r.lv)) + '</p><p class="asbx__h">' + esc(C.now) + '</p><ol>' + r.steps.map(function (s) { return '<li>' + hl(t(s)) + '</li>'; }).join('') + '</ol>'
          + '<p class="asbx__h">' + esc(C.who) + '</p><p>' + esc(t(r.who)) + '. <a href="' + GOV.registry + '" target="_blank" rel="noopener">' + esc(C.reg) + '</a></p>'
          + '<p class="asbx__h">' + esc(C.permit) + '</p><p>' + esc(t(r.permit)) + '</p>';
      }
      root.addEventListener('click', function (e) { var b = e.target.closest('button[data-k]'); if (!b) return; v[b.getAttribute('data-k')] = b.getAttribute('data-v');
        [].forEach.call(root.querySelectorAll('button[data-k="' + b.getAttribute('data-k') + '"]'), function (x) { x.setAttribute('aria-pressed', String(x === b)); }); draw(); });
      draw();
    }
  });

  /* ---------------------------------------------------------------- asbcost: the price guide */
  var PX = {
    kicker: { he: 'מחשבון · פינוי אסבסט', en: 'Calculator · Asbestos removal' },
    title: { he: 'כמה עולה פינוי אסבסט', en: 'What asbestos removal costs' },
    lede: { he: 'מחיר הייחוס הציבורי היחיד שפורסם, ולצדו הטווחים המסחריים, כל אחד מסומן כמו שהוא. זו הערכה לתכנון, לא הצעת מחיר.',
      en: 'The only public reference price that has been published, and beside it the commercial ranges, each labelled as what it is. An estimate for planning, not a quote.' },
    fJob: { he: 'העבודה', en: 'The job' }, jBroken: { he: 'פינוי לוחות שבורים', en: 'Removing broken sheets' },
    jFriable: { he: 'פינוי חומר מתפורר', en: 'Removing crumbled material' }, jRoof: { he: 'החלפת גג אסבסט', en: 'Replacing an asbestos roof' },
    fQty: { he: 'הכמות', en: 'Quantity' }, m2: { he: 'מ״ר', en: 'm²' }, m3: { he: 'מ״ק', en: 'm³' },
    helpFr: { he: 'חומר אחרי שרפה נמדד בנפח, במטרים מעוקבים.', en: 'Material after a fire is measured by volume, in cubic metres.' },
    err: { he: 'הקלידו כמות גדולה מאפס.', en: 'Enter a quantity greater than zero.' },
    aRef: { he: 'מחיר ייחוס לפי מכרז המשרד', en: 'Reference price from the Ministry tender' },
    aRoof: { he: 'גג חלופי, לפי מחירון מסחרי שפורסם', en: 'A replacement roof, from a published commercial price list' },
    subRef: { he: '{p} ₪ ל{u} · פינוי בלבד', en: 'NIS {p} per {u} · removal only' },
    subRoof: { he: 'גג פח כ־440 ₪ למ״ר, פאנל מבודד כ־520 ₪ למ״ר (מחירי פתיחה)', en: 'Steel sheet from about NIS 440 per m², insulated panel from about NIS 520 per m² (opening prices)' },
    lUnit: { he: 'מחיר המכרז ליחידה', en: 'Tender price per unit' }, lQty: { he: 'הכמות', en: 'Quantity' },
    lSteel: { he: 'גג פח (איסכורית), מחיר פתיחה', en: 'Corrugated steel roof, opening price' }, lPanel: { he: 'פאנל מבודד, מחיר פתיחה', en: 'Insulated panel roof, opening price' },
    lJobs: { he: 'עבודות החלפה שדווחו בפלטפורמת השוואת מחירים', en: 'Replacement jobs reported on a price-comparison platform' },
    vJobs: { he: 'רובן בין 6,001 ל־11,000 ₪ לעבודה', en: 'Most between NIS 6,001 and 11,000 per job' },
    lRule: { he: 'מעל 50 מ״ר', en: 'Over 50 m²' }, vRule: { he: 'חובה קבלן מורשה', en: 'A licensed contractor is required' },
    noteRef: { he: 'לפי מרכז המחקר של הכנסת (17.7.2023), מחירי המכרז מעידים על סדר הגודל אך אינם מחירי שוק, שכנראה גבוהים יותר. המחיר משתנה לפי האזור (המרחק מאתר הטמנה), היקף העבודה ומורכבותה: מצב החומר, הגישה והצורך במנוף. המשרד להגנת הסביבה לא מעורב במחירי השוק.',
      en: 'Per the Knesset Research and Information Center (17.7.2023), the tender prices indicate the order of magnitude but are not market prices, which are probably higher. The price varies by region (the distance to a landfill), the scale and the complexity: the state of the material, the access and the need for a crane. The Ministry of Environmental Protection is not involved in market prices.' },
    noteRoof: { he: 'המחירים לגג החלופי לקוחים ממחירון שפרסם אתר מסחרי (10.2026), ופינוי הגג הישן בדרך כלל בנפרד. בקשו כמה הצעות מקבלנים מורשים, ובדקו שההצעה כוללת היתר, פינוי והטמנה באתר מורשה.',
      en: 'The replacement-roof prices come from a price list a commercial site published (10.2026), and removing the old roof is usually separate. Ask several licensed contractors for quotes, and check that each includes the permit, removal and landfilling at a licensed site.' },
    formula: { he: 'הערכה = הכמות × המחיר ליחידה. מכרז "קבלן הבית" של המשרד להגנת הסביבה: 50 ₪ למ״ר אסבסט-צמנט שבור, 1,600 ₪ למ״ק אסבסט-צמנט במצב פריך.',
      en: 'Estimate = quantity × the unit price. The Ministry of Environmental Protection "home contractor" tender: NIS 50 per m² of broken asbestos-cement, NIS 1,600 per m³ of asbestos-cement in a friable state.' },
    sKnesset: { he: 'מרכז המחקר והמידע של הכנסת, חסמים לפינוי מוסדר של אסבסט ממבנים פרטיים (17.7.2023)', en: 'Knesset Research and Information Center, barriers to regulated asbestos removal from private buildings (17.7.2023, Hebrew PDF)' },
    share: { he: 'הערכת עלות {job}: {q} {u}, {v}. מחיר ייחוס, לא הצעת מחיר.', en: 'Cost estimate, {job}: {q} {u}, {v}. A reference price, not a quote.' }
  };
  var P = NLI.pick(PX, LG);
  NLI.register('asbcost', {
    kicker: P.kicker, title: P.title, lede: P.lede,
    defaults: function () { return { job: 'broken', qty: 40 }; },
    fields: [
      { id: 'job', label: P.fJob, type: 'segmented', options: [{ value: 'broken', label: P.jBroken }, { value: 'friable', label: P.jFriable }, { value: 'roof', label: P.jRoof }] },
      { id: 'qty', label: P.fQty, type: 'number', unit: P.m2, help: P.helpFr }
    ],
    compute: function (v, data) {
      var pr = (data.asb && data.asb.prices) || { brokenM2: 50, friableM3: 1600 };
      if (!(v.qty > 0)) return { error: { field: 'qty', msg: P.err } };
      var src = [{ label: P.sKnesset, url: GOV.knesset }], u = v.job === 'friable' ? P.m3 : P.m2, out;
      if (v.job === 'roof') {
        var lo = v.qty * 440, hi = v.qty * 520;
        out = { answer: { label: P.aRoof, value: F.ils(lo) + (EN ? ' to ' : ' עד ') + F.ils(hi), tone: 'ink', sub: P.subRoof },
          lines: [{ label: P.lQty, value: F.num(v.qty) + ' ' + u }, { label: P.lSteel, value: F.ils(lo) }, { label: P.lPanel, value: F.ils(hi) }, { label: P.lJobs, value: P.vJobs }],
          note: P.noteRoof, formula: P.formula, sources: src, text: f(P.share, { job: P.jRoof, q: F.num(v.qty), u: u, v: F.ils(lo) + (EN ? ' to ' : ' עד ') + F.ils(hi) }) };
      } else {
        var unit = v.job === 'friable' ? pr.friableM3 : pr.brokenM2, val = v.qty * unit;
        out = { answer: { label: P.aRef, value: F.ils(val), tone: 'ink', sub: f(P.subRef, { p: F.num(unit), u: u }) },
          lines: [{ label: P.lQty, value: F.num(v.qty) + ' ' + u }, { label: P.lUnit, value: F.ils(unit) }],
          note: P.noteRef, formula: P.formula, sources: src, text: f(P.share, { job: v.job === 'friable' ? P.jFriable : P.jBroken, q: F.num(v.qty), u: u, v: F.ils(val) }) };
        if (v.job === 'broken' && v.qty > 50) out.lines.push({ label: P.lRule, value: P.vRule });
      }
      return out;
    }
  });

  /* ---------------------------------------------------------------- asbmap: the Western Galilee sites */
  var ML = 'https://unpkg.com/maplibre-gl@4.7.1/dist/', RTL = 'https://unpkg.com/@mapbox/mapbox-gl-rtl-text@0.2.3/mapbox-gl-rtl-text.min.js';
  var STYLE = 'https://tiles.openfreemap.org/styles/positron', COL = ['#3F7D5A', '#C9831A', '#B23A2E'];
  var PLACE_EN = { 'נהרייה': 'Nahariya', 'בן עמי': 'Ben Ami', 'בוסתן הגליל': 'Bustan HaGalil', 'בצת': 'Betzet', 'לימן': 'Liman', 'סער': "Sa'ar", 'יחיעם': 'Yechiam',
    'כברי': 'Kabri', 'כפר ראש הנקרה': 'Kfar Rosh HaNikra', 'נתיב השיירה': 'Netiv HaShayara', 'מזרעה': "Mazra'a", 'עברון': 'Evron', 'נס עמים': 'Nes Ammim', 'געתון': "Ga'aton" };
  var MX = {
    kicker: { he: 'מפה · הגליל המערבי', en: 'Map · Western Galilee' },
    title: { he: 'מפת אתרי האסבסט בגליל המערבי', en: 'Map of the asbestos sites in Western Galilee' },
    lede: { he: 'הפסולת של המפעל לייצור מוצרי אסבסט-צמנט בנהריה פוזרה בגליל המערבי כמצע לדרכים, לשבילים ולחצרות. כאן כל 348 האתרים של פרויקט ניקוי הקרקעות, במצב שבו המשרד להגנת הסביבה סימן אותם.',
      en: 'The waste of the asbestos-cement products plant in Nahariya was spread across Western Galilee as a base for roads, paths and yards. Here are all 348 sites of the soil clean-up project, in the status the Ministry of Environmental Protection gave each one.' },
    st0: { he: 'נוקה, לא ידוע על אסבסט שנותר', en: 'Cleaned, no asbestos known to remain' },
    st1: { he: 'נוקה, ידוע שנותר אסבסט תחת התשתיות', en: 'Cleaned, asbestos known to remain under the infrastructure' },
    st2: { he: 'ידוע שיש אסבסט, טרם נוקה', en: 'Asbestos known, not yet cleaned' },
    sites: { he: '{n} אתרים', en: '{n} sites' }, all: { he: 'כל היישובים', en: 'All localities' },
    wait: { he: 'טוען את המפה…', en: 'Loading the map…' }, fail: { he: 'המפה לא נטענה. הטבלה למטה מראה את כל הנתונים.', en: 'The map did not load. The table below has all the data.' },
    d3: { he: 'מבט מוטה', en: 'Tilted view' }, aria: { he: 'מפת אתרי פרויקט ניקוי האסבסט בגליל המערבי', en: 'Map of the Western Galilee asbestos clean-up sites' },
    table: { he: 'כל היישובים והאתרים', en: 'Every locality and its sites' }, thPlace: { he: 'יישוב', en: 'Locality' }, thAll: { he: 'סה״כ', en: 'Total' },
    note: { he: 'הנתונים מתוך השכבה שפרסם המשרד להגנת הסביבה ל־2011 עד 2017 (שלב א׳). שלב ב׳ של הפרויקט נמשך, והתוצאות שלו אינן בשכבה. אין בישראל מפה ארצית של גגות אסבסט: מקום בלי סימון במפה הוא מקום בלי נתונים, לא מקום נקי.',
      en: 'The data come from the layer the Ministry of Environmental Protection published for 2011 to 2017 (stage A). Stage B of the project continues, and its results are not in the layer. Israel has no national map of asbestos roofs: a place with no mark on the map is a place with no data, not a clean place.' },
    srcLine: { he: 'מקור: {src}. המפה: © OpenStreetMap, OpenFreeMap.', en: 'Source: Ministry of Environmental Protection, Western Galilee friable-asbestos soil clean-up layer (data.gov.il). Map: © OpenStreetMap, OpenFreeMap.' }
  };
  var M = NLI.pick(MX, LG);
  function loadML(cb) {
    if (window.maplibregl) return cb();
    var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = ML + 'maplibre-gl.css'; document.head.appendChild(l);
    var s = document.createElement('script'); s.src = ML + 'maplibre-gl.js'; s.async = true;
    s.onload = function () { try { window.maplibregl.setRTLTextPlugin(RTL, true); } catch (e) { /* already set */ } cb(); };
    s.onerror = function () { cb(new Error('map')); }; document.head.appendChild(s);
  }
  function pname(p) { return EN ? (PLACE_EN[p] || p) : p; }
  NLI.register('asbmap', {
    custom: function (root, data) {
      var d = data.asb, phone = window.matchMedia('(max-width: 760px)').matches, sel = '';
      var tot = [0, 0, 0]; d.sites.forEach(function (s) { tot[s[2]]++; });
      var names = Object.keys(d.places);
      root.innerHTML = '<div class="nli__panel asbm"><p class="nli__kicker">' + esc(M.kicker) + '</p><h2 class="nli__title">' + esc(M.title) + '</h2><p class="nli__lede">' + esc(M.lede) + '</p>'
        + '<div class="nli__strip">' + [0, 1, 2].map(function (i) { return '<div><span><b class="asbm__dot" style="background:' + COL[i] + '"></b>' + esc(M['st' + i]) + '</span><strong>' + F.num(tot[i]) + '</strong></div>'; }).join('') + '</div>'
        + '<div class="nls__chips asbm__chips" role="group"><button type="button" data-p="" aria-pressed="true">' + esc(M.all) + '</button>' + names.map(function (p) {
          var n = d.places[p][0] + d.places[p][1] + d.places[p][2]; return '<button type="button" data-p="' + esc(p) + '" aria-pressed="false">' + esc(pname(p)) + ' · ' + F.num(n) + '</button>'; }).join('') + '</div>'
        + '<div class="asbm__map" role="region" aria-label="' + esc(M.aria) + '"><p class="nls__wait">' + esc(M.wait) + '</p></div>'
        + '<div class="nls__bar"><button type="button" class="nls__3d asbm__3d" aria-pressed="true">' + esc(M.d3) + '</button></div>'
        + '<p class="nli__note">' + esc(M.note) + '</p>'
        + '<details class="nli__table"><summary>' + esc(M.table) + '</summary><div class="nli__tw"><table><thead><tr><th scope="col">' + esc(M.thPlace) + '</th>'
        + [0, 1, 2].map(function (i) { return '<th scope="col" class="n">' + esc(M['st' + i]) + '</th>'; }).join('') + '<th scope="col" class="n">' + esc(M.thAll) + '</th></tr></thead><tbody>'
        + names.map(function (p) { var a = d.places[p]; return '<tr><td>' + esc(pname(p)) + '</td><td class="n">' + a[0] + '</td><td class="n">' + a[1] + '</td><td class="n">' + a[2] + '</td><td class="n">' + (a[0] + a[1] + a[2]) + '</td></tr>'; }).join('')
        + '</tbody></table></div></details><p class="nli__src">' + esc(f(M.srcLine, { src: d.sources.sites })) + '</p></div>';
      var mapEl = root.querySelector('.asbm__map'), map = null;
      function fc(only) { return { type: 'FeatureCollection', features: d.sites.filter(function (s) { return !only || s[3] === only; }).map(function (s) {
        return { type: 'Feature', properties: { st: s[2] }, geometry: { type: 'Point', coordinates: [s[0], s[1]] } }; }) }; }
      function labels() { return { type: 'FeatureCollection', features: names.map(function (p) { var xs = d.sites.filter(function (s) { return s[3] === p; }), x = 0, y = 0;
        xs.forEach(function (s) { x += s[0]; y += s[1]; }); var a = d.places[p];
        return { type: 'Feature', properties: { t: pname(p) + '\n' + f(M.sites, { n: F.num(a[0] + a[1] + a[2]) }) }, geometry: { type: 'Point', coordinates: [x / xs.length, y / xs.length] } }; }) }; }
      function bounds(only) { var b = new window.maplibregl.LngLatBounds(); d.sites.forEach(function (s) { if (!only || s[3] === only) b.extend([s[0], s[1]]); }); return b; }
      function choose(p) { sel = p; [].forEach.call(root.querySelectorAll('.asbm__chips button'), function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-p') === p)); });
        if (!map || !map.getSource('asb')) return; map.getSource('asb').setData(fc(p)); map.fitBounds(bounds(p), { padding: phone ? 36 : 70, maxZoom: 15, duration: 800 }); }
      root.querySelector('.asbm__chips').addEventListener('click', function (e) { var b = e.target.closest('button[data-p]'); if (b) choose(b.getAttribute('data-p')); });
      loadML(function (err) {
        if (err || !window.maplibregl) { mapEl.innerHTML = '<p class="nls__wait">' + esc(M.fail) + '</p>'; return; }
        var gl = window.maplibregl;
        map = new gl.Map({ container: mapEl, style: STYLE, bounds: bounds(''), fitBoundsOptions: { padding: phone ? 30 : 60 }, pitch: phone ? 38 : 50, bearing: -16, maxPitch: 65,
          cooperativeGestures: true, attributionControl: { compact: true } });
        map.addControl(new gl.NavigationControl({ showCompass: true }), EN ? 'top-right' : 'top-left');
        map.on('load', function () {
          mapEl.querySelector('.nls__wait') && mapEl.querySelector('.nls__wait').remove();
          map.addSource('asb', { type: 'geojson', data: fc('') });
          map.addLayer({ id: 'asb-pt', type: 'circle', source: 'asb', paint: { 'circle-radius': ['interpolate', ['linear'], ['zoom'], 10, 3.2, 15, 7], 'circle-color': ['match', ['get', 'st'], 0, COL[0], 1, COL[1], COL[2]],
            'circle-stroke-color': '#FFFFFF', 'circle-stroke-width': 1.2, 'circle-pitch-alignment': 'map' } });
          map.addSource('asb-l', { type: 'geojson', data: labels() });
          map.addLayer({ id: 'asb-lab', type: 'symbol', source: 'asb-l', layout: { 'text-field': ['get', 't'], 'text-size': phone ? 11.5 : 12.5, 'text-font': ['Noto Sans Regular'], 'text-offset': [0, -1.6], 'text-anchor': 'bottom',
            'text-allow-overlap': false, 'text-padding': 4 }, paint: { 'text-color': '#121417', 'text-halo-color': '#FFFFFF', 'text-halo-width': 1.6 } });
          var pop = new gl.Popup({ closeButton: false, offset: 8 });
          map.on('click', 'asb-pt', function (e) { var p = e.features[0]; pop.setLngLat(p.geometry.coordinates).setHTML('<b style="color:' + COL[p.properties.st] + '">●</b> ' + esc(M['st' + p.properties.st])).addTo(map); });
          map.on('mouseenter', 'asb-pt', function () { map.getCanvas().style.cursor = 'pointer'; }); map.on('mouseleave', 'asb-pt', function () { map.getCanvas().style.cursor = ''; });
          if (sel) choose(sel);
        });
        var b3 = root.querySelector('.asbm__3d');
        b3.addEventListener('click', function () { var on = b3.getAttribute('aria-pressed') !== 'true'; b3.setAttribute('aria-pressed', String(on)); map.easeTo({ pitch: on ? (phone ? 38 : 50) : 0, bearing: on ? -16 : 0, duration: 700 }); });
      });
    }
  });

  /* ---------------------------------------------------------------- asbwho: who to call, by town */
  var WX = {
    kicker: { he: 'איתור · למי פונים', en: 'Finder · Who to call' },
    title: { he: 'למי פונים באסבסט, לפי העיר', en: 'Who to call about asbestos, by town' },
    lede: { he: 'מקלידים את הרשות המקומית ומקבלים את היחידה הסביבתית שלה, כמה בעלי רישיון רשומים במחוז, את אתרי ההטמנה המורשים ואת המוקדים.',
      en: 'Type the local authority to get its environmental unit, how many licence holders are registered in its district, the licensed landfill sites and the hotlines.' },
    q: { he: 'רשות מקומית', en: 'Local authority (Hebrew name)' }, ph: { he: 'למשל תל אביב יפו, חיפה, נהרייה', en: 'e.g. תל אביב יפו, חיפה, נהרייה' },
    none: { he: 'לא מצאנו רשות בשם הזה. נסו שם אחר, או התקשרו למוקד *6911.', en: 'No authority by that name. Try another spelling in Hebrew, or call *6911.' },
    unit: { he: 'היחידה הסביבתית', en: 'Environmental unit' }, dist: { he: 'מחוז המשרד להגנת הסביבה: {d}', en: 'Ministry district: {d}' },
    tel: { he: 'טלפון', en: 'Phone' }, site: { he: 'לאתר היחידה', en: 'Unit website' },
    inDist: { he: 'בעלי רישיון במחוז {d}', en: 'Licence holders in the {d} district' },
    regNote: { he: 'לפי הכתובת הרשומה במרשם, לא לפי אזור השירות. הפרטים עצמם במרשם הממשלתי.', en: 'By the address in the registry, not the service area. The details are in the government registry.' },
    reg: { he: 'לחיפוש במרשם העוסקים באסבסט', en: 'Search the registry of asbestos operators (Hebrew)' },
    lf: { he: 'אתרי הטמנה ותחנת מעבר מורשים לאסבסט', en: 'Licensed asbestos landfills and transfer station' },
    lines: { he: 'מוקדים', en: 'Hotlines' },
    l1: { he: 'מוקד הסביבה של המשרד להגנת הסביבה, 24/7: *6911 שלוחה 5, או 073-2733200', en: 'Ministry of Environmental Protection environment hotline, 24/7: *6911 extension 5, or 073-2733200' },
    l2: { he: 'מוקד העירייה: 106 (בתל אביב יפו פניות על אסבסט עוברות דרכו)', en: 'Municipal hotline: 106 (in Tel Aviv-Yafo, asbestos enquiries go through it)' },
    l3: { he: 'אירוע חומרים מסוכנים עם סכנת חיים: כבאות והצלה 102, משטרה 100', en: 'A hazardous-materials event with danger to life: Fire and Rescue 102, Police 100' },
    src: { he: 'מקורות: {u}; {r} ({n} רישיונות, נספרו {d}); מטמנות אסבסט, data.gov.il.', en: 'Sources: the Ministry of Environmental Protection list of environmental units; the registry of asbestos operators ({n} licences, counted {d}); asbestos landfills, data.gov.il.' }
  };
  var TYPE_EN = { 'קבלן אסבסט צמנט': 'Asbestos-cement contractor', 'עובד אחראי אסבסט צמנט': 'Asbestos-cement worker in charge', 'סוקר אסבסט': 'Asbestos surveyor',
    'עובד אחראי אסבסט פריך': 'Friable asbestos worker in charge', 'מפקח אסבסט פריך': 'Friable asbestos inspector', 'קבלן אסבסט פריך': 'Friable asbestos contractor' };
  var LF_EN = { 'מילואות דרום, הגליל המערבי': "Milu'ot South, Western Galilee", 'אפעה, אזור תמר': "Ef'e, Tamar area", 'נימרה, אזור אילות': 'Nimra, Eilot area',
    'מחצבות תות, ליד זכרון יעקב': "Tut quarries, near Zichron Ya'akov", 'חרובית, ליד שדות מיכה': 'Haruvit, near Sdot Micha', 'נאות חובב': 'Neot Hovav',
    'תחנת מעבר': 'transfer station', 'אסבסט צמנט, אסבסט פריך': 'asbestos-cement and friable', 'אסבסט צמנט': 'asbestos-cement', 'אסבסט צמנט, פריך': 'asbestos-cement and friable' };
  function lf(x) { return EN ? (LF_EN[x] || x) : x; }
  var DIST_EN = { 'מרכז': 'Center', 'צפון': 'North', 'דרום': 'South', 'חיפה': 'Haifa', 'תל אביב': 'Tel Aviv', 'ירושלים': 'Jerusalem' };
  var W = NLI.pick(WX, LG);
  function norm(s) { return String(s || '').replace(/[״"׳'\-\u2013־,.()]/g, ' ').replace(/\s+/g, ' ').trim(); }
  function tel(s) { var m = String(s || '').match(/0\d{1,2}-?\d{7}/); return m ? m[0].replace('-', '') : ''; }  // the first number of the cell ('04-9888633 100 שלוחה')
  function regDist(d) { return norm(d).replace(/^ה(?=(מרכז|צפון|דרום)$)/, ''); }
  NLI.register('asbwho', {
    custom: function (root, data) {
      var d = data.asb, U = d.units, R = d.registry;
      root.innerHTML = '<div class="nli__panel asbw"><p class="nli__kicker">' + esc(W.kicker) + '</p><h2 class="nli__title">' + esc(W.title) + '</h2><p class="nli__lede">' + esc(W.lede) + '</p>'
        + '<label class="nls__q"><span>' + esc(W.q) + '</span><input type="search" list="asbw-list" enterkeyhint="search" placeholder="' + esc(W.ph) + '" autocomplete="off" dir="rtl"></label>'
        + '<datalist id="asbw-list">' + U.map(function (u) { return '<option value="' + esc(u[0]) + '">'; }).join('') + '</datalist>'
        + '<div class="asbw__out" aria-live="polite"></div>'
        + '<div class="asbw__fix"><p class="asbx__h">' + esc(W.lf) + '</p><ul>' + d.landfills.map(function (x) { return '<li>' + esc(lf(x.place)) + ' <span>· ' + esc(lf(x.type)) + '</span></li>'; }).join('') + '</ul>'
        + '<p class="asbx__h">' + esc(W.lines) + '</p><ul><li>' + hl(W.l1) + '</li><li>' + esc(W.l2) + '</li><li>' + esc(W.l3) + '</li></ul></div>'
        + '<p class="nli__src">' + esc(f(W.src, { u: d.sources.units, r: d.sources.registry, n: F.num(R.total), d: F.date(d.built) })) + '</p></div>';
      var inp = root.querySelector('input'), out = root.querySelector('.asbw__out');
      function find(q) { q = norm(q); if (!q) return null; var hit = null;
        U.forEach(function (u) { if (!hit && norm(u[0]) === q) hit = u; }); if (hit) return hit;
        U.forEach(function (u) { if (!hit && norm(u[0]).indexOf(q) === 0) hit = u; }); return hit; }
      function draw(u) {
        if (!u) { out.innerHTML = inp.value.trim() ? '<p class="nli__note">' + hl(W.none) + '</p>' : ''; return; }
        var rd = regDist(u[1]), types = Object.keys(R.byType), rows = types.map(function (ty) { return [ty, R.byTypeDistrict[ty + '|' + rd] || 0]; }), mx = Math.max.apply(null, rows.map(function (r) { return r[1]; }).concat([1]));
        out.innerHTML = '<div class="asbw__card"><p class="asbx__h">' + esc(W.unit) + '</p><p class="asbw__name">' + esc(u[2]) + '</p><p>' + esc(f(W.dist, { d: EN ? (DIST_EN[rd] || rd) : u[1] })) + '</p>'
          + (u[3] ? '<p>' + esc(W.tel) + ': ' + (tel(u[3]) ? '<a href="tel:' + tel(u[3]) + '" dir="ltr">' + esc(u[3]) + '</a>' : '<span dir="ltr">' + esc(u[3]) + '</span>') + '</p>' : '')
          + (u[4] ? '<p><a href="' + esc(u[4]) + '" target="_blank" rel="noopener">' + esc(W.site) + '</a></p>' : '') + '</div>'
          + '<div class="asbw__bars"><p class="asbx__h">' + esc(f(W.inDist, { d: EN ? (DIST_EN[rd] || rd) : rd })) + '</p>' + rows.map(function (r) {
            return '<div class="asbw__bar"><span>' + esc(EN ? (TYPE_EN[r[0]] || r[0]) : r[0]) + '</span><i style="width:' + Math.round(100 * r[1] / mx) + '%"></i><b>' + F.num(r[1]) + '</b></div>'; }).join('')
          + '<p class="nli__note">' + esc(W.regNote) + ' <a href="' + R.search + '" target="_blank" rel="noopener">' + esc(W.reg) + '</a></p></div>';
      }
      inp.addEventListener('input', function () { draw(find(inp.value)); });
      inp.addEventListener('change', function () { draw(find(inp.value)); });
      inp.value = EN ? 'תל אביב יפו' : 'תל אביב יפו'; draw(find(inp.value));
    }
  });
})();
