/* NadLan Instruments · the Greece family (HAD-592, the page loop, Ben 22.10.2026: "tools ultra complex, with UX that gives
   everything in one tap"). Three tools in one file (registry 'file' => 'greece'):
     grbuy   the whole purchase in euros and shekels: transfer tax or VAT, notary scale, cadastre, lawyer, agent, engineer, a Greek
             mortgage, today and under the draft 15.45% rate for non-EU buyers from 1.7.2027;
     grgv    the golden-visa check: the 2024 tiers by area, the 120 m² single-property rule, the short-let ban, fees for the family;
     gryield the net yield after ENFIA, the 2026 Greek rent brackets and the Israeli side (treaty text, the 15% track, the
             regular track with credit).
   Data: data/greece.json (tools/instruments/build_greece_data.py, from docs/research/2026-10-22-greece/facts.json, every number
   with its source and date) + data/boi-fx.json (Bank of Israel rate). Pure logic in NLGR for unit checks. */
(function () {
  'use strict';
  function scale(v, br) { var t = 0, lo = 0; for (var i = 0; i < br.length; i++) { var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(v, hi); if (top > lo) t += (top - lo) * br[i][1]; if (v <= hi) break; lo = hi; } return t; }
  function band(v, br) { for (var i = 0; i < br.length; i++) { if (br[i][0] == null || v <= br[i][0]) return br[i][1]; } return br[br.length - 1][1]; }
  function buy(v, G) {
    var B = G.buy, p = v.price, vat = 1 + B.svc_vat, loan = p * Math.min(Math.max(v.ltv || 0, 0), 100) / 100;
    var vatNew = v.kind === 'new_vat' ? p * B.vat : 0;
    var rate = v.kind === 'new_vat' ? 0 : (v.when === 'after' ? B.tt_noneu : B.tt);
    var tt = p * rate;
    var notary = (scale(p, B.notary) + B.notary_fixed) * vat;
    var cad = p * B.cad + B.cad_fixed;
    var lawyer = p * (v.lawyer || 0) / 100 * vat;
    var agent = p * (v.agent || 0) / 100 * vat;
    var eng = v.engineer || 0;
    var mort = loan > 0 ? loan * B.cad_mortgage + B.cad_fixed + 750 : 0;
    var costs = vatNew + tt + notary + cad + lawyer + agent + eng + mort;
    return { loan: loan, vatNew: vatNew, rate: rate, tt: tt, notary: notary, cad: cad, lawyer: lawyer, agent: agent, eng: eng, mort: mort, costs: costs, cash: p - loan + costs };
  }
  function enfia(v, G) {
    var E = G.enfia, base = band(v.zone, E.zones), age = E.age[v.age] || 1, fl = E.floor[v.floor] || 1;
    var main = v.m2 * base * age * fl, val = v.price, sur = 0, gam = 0;
    if (val > E.sur_from) sur = main * band(val, E.sur);
    if (val > E.gamma_from) gam = scale(val, E.gamma);
    var tot = main + sur + gam, disc = v.insured === 'yes' ? tot * (val <= 500000 ? E.ins[0] : E.ins[1]) : 0;
    return { main: main, sur: sur, gam: gam, disc: disc, total: tot - disc };
  }
  function yieldCalc(v, G, track) {
    var gross = v.rent * v.months, en = enfia(v, G).total;
    var mg = gross * (v.mgmt || 0) / 100, fees = (v.fees || 0) * 12 + (v.ins || 0);
    var exp = mg + fees + en;
    var gtx = scale(gross * (1 - G.rent.ded), G.rent.br);
    var il = 0;
    if (track === 'flat15') il = Math.max(0, gross - (v.dep || 0)) * G.il.flat;
    else if (track === 'regular') { var ilt = Math.max(0, gross - exp - (v.dep || 0)) * (v.marg || 0) / 100; il = Math.max(0, ilt - gtx); }
    var net = gross - exp - gtx - il;
    var invest = v.price + buy({ price: v.price, kind: 'resale', when: 'now', lawyer: 1, agent: 2, engineer: 0, ltv: 0 }, G).costs;
    return { gross: gross, enfia: en, mg: mg, fees: fees, exp: exp, gtx: gtx, il: il, net: net, invest: invest, gy: gross / v.price, ny: net / invest };
  }
  window.NLGR = { scale: scale, band: band, buy: buy, enfia: enfia, yieldCalc: yieldCalc };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt;
  function ils(e, d) { return '₪' + F.num(Math.round(e * d.fx.fx.EUR.rate)); }
  function both(e, d) { return F.eur(e) + ' · ' + ils(e, d); }
  function reg(d, id) { return d.greece.regions.filter(function (r) { return r.id === id; })[0] || d.greece.regions[0]; }
  function regOpts(d) { return d.greece.regions.map(function (r) { return { value: r.id, label: r.he + ' · €' + F.num(r.m2) + ' למ״ר' }; }); }
  function fxLine(d) { return { label: 'שער היציג של בנק ישראל, ' + F.date(d.fx.fx.EUR.date), url: d.fx.url }; }
  var KIND = { resale: 'יד שנייה', new_susp: 'חדשה, מע״מ מוקפא', new_vat: 'חדשה עם מע״מ 24%' };

  /* ---------------- grbuy ---------------- */
  NI.register('grbuy', {
    kicker: 'מחשבון · קניית דירה ביוון',
    title: 'כמה עולה לקנות דירה ביוון, עד היורו האחרון',
    lede: 'מחיר, אזור וסוג הנכס: המחשבון מוסיף את מס ההעברה או את המע״מ, הנוטריון לפי המדרגות, רישום בקדסטר, עורך דין ומתווך עם מע״מ יווני, ומשכנתא מבנק יווני אם יש, ומראה כמה כסף צריך להביא, ביורו ובשקלים.',
    strip: function (d) { var B = d.greece.buy; return [{ label: 'מס העברה היום', value: F.num(100 * B.tt, 2) + '%' }, { label: 'מס ההעברה המוצע לזרים מ־1.7.2027', value: F.num(100 * B.tt_noneu, 2) + '%' }, { label: 'יורו בשקלים, בנק ישראל', value: '₪' + F.num(d.fx.fx.EUR.rate, 3) }]; },
    presets: function (d) { return [
      { key: 'athens-resale', label: 'דירה יד שנייה במרכז אתונה', sub: '€180,000 · 72 מ״ר', set: { price: 180000, region: 'athens-center', kind: 'resale', when: 'now', agent: 2, lawyer: 1, engineer: 500, ltv: 0 } },
      { key: 'glyfada-new', label: 'דירה חדשה בגליפדה', sub: '€450,000 · מע״מ מוקפא', set: { price: 450000, region: 'athens-south', kind: 'new_susp', when: 'now', agent: 0, lawyer: 1, engineer: 0, ltv: 0 } },
      { key: 'thess', label: 'דירה בסלוניקי', sub: '€160,000', set: { price: 160000, region: 'thessaloniki', kind: 'resale', when: 'now', agent: 2, lawyer: 1, engineer: 500, ltv: 0 } },
      { key: 'chania', label: 'בית בחאניה, כרתים', sub: '€300,000', set: { price: 300000, region: 'chania', kind: 'resale', when: 'now', agent: 2, lawyer: 1, engineer: 800, ltv: 0 } },
      { key: 'gv800', label: 'דירה לגולדן ויזה באטיקה', sub: '€800,000', set: { price: 800000, region: 'athens-south', kind: 'resale', when: 'now', agent: 2, lawyer: 1, engineer: 800, ltv: 0 } },
      { key: 'after2027', label: 'אותה עסקה, חוזה ביולי 2027', sub: '€250,000 · 15.45%', set: { price: 250000, region: 'athens-center', kind: 'resale', when: 'after', agent: 2, lawyer: 1, engineer: 500, ltv: 0 } },
      { key: 'mortgage', label: 'קנייה עם משכנתא יוונית', sub: '€300,000 · 60% מימון', set: { price: 300000, region: 'piraeus', kind: 'resale', when: 'now', agent: 2, lawyer: 1, engineer: 500, ltv: 60 } }
    ]; },
    defaults: function () { return { price: 180000, region: 'athens-center', kind: 'resale', when: 'now', agent: 2, lawyer: 1, engineer: 500, ltv: 0 }; },
    fields: [
      { id: 'price', label: 'מחיר הנכס', type: 'money', unit: '€' },
      { id: 'region', label: 'איפה', type: 'select', optionsFrom: function (v, d) { return regOpts(d); } },
      { id: 'kind', label: 'סוג הנכס', type: 'segmented', options: [{ value: 'resale', label: 'יד שנייה' }, { value: 'new_susp', label: 'חדשה, מע״מ מוקפא' }, { value: 'new_vat', label: 'חדשה עם מע״מ' }] },
      { id: 'when', label: 'מועד החוזה', type: 'segmented', options: [{ value: 'now', label: 'עד 30.6.2027' }, { value: 'after', label: 'מ־1.7.2027, אם ההצעה תעבור' }] },
      { id: 'agent', label: 'מתווך', type: 'percent', unit: '%', help: 'מקובל 2% ועוד מע״מ 24%. לפעמים רק המוכר משלם: אז 0.' },
      { id: 'lawyer', label: 'עורך דין ביוון', type: 'percent', unit: '%', help: 'לרוב 0.5% עד 1.5% ועוד מע״מ 24%.' },
      { id: 'engineer', label: 'מהנדס מטעמכם', type: 'money', unit: '€', help: 'בדיקת חריגות בנייה. את תעודת החוקיות מביא המוכר.' },
      { id: 'ltv', label: 'משכנתא מבנק יווני', type: 'percent', unit: '%', help: 'עד 65% לתושב חוץ. 0 אם קונים במזומן.' }
    ],
    compute: function (v, d) {
      var G = d.greece, B = G.buy, R = reg(d, v.region);
      if (!(v.price >= 20000 && v.price <= 50000000)) return { error: { field: 'price', msg: 'הקלידו את מחיר הנכס ביורו.' } };
      if (!(v.ltv >= 0 && v.ltv <= 65)) return { error: { field: 'ltv', msg: 'בנק יווני מממן לתושב חוץ עד 65%.' } };
      var r = buy(v, G), pct = r.costs / v.price;
      var today = buy(Object.assign({}, v, { when: 'now' }), G), later = buy(Object.assign({}, v, { when: 'after' }), G);
      var m2 = v.price / R.m2;
      var lines = [
        { label: 'עלויות הקנייה, מעבר למחיר', value: both(r.costs, d) + ' · ' + F.num(100 * pct, 1) + '%' },
        v.kind === 'new_vat' ? { label: 'מע״מ 24% על המחיר', value: F.eur(r.vatNew) } : { label: 'מס העברה ' + F.num(100 * r.rate, 2) + '%', value: F.eur(r.tt) },
        { label: 'נוטריון, כולל מע״מ', value: F.eur(r.notary) },
        { label: 'רישום בקדסטר', value: F.eur(r.cad) },
        { label: 'עורך דין, כולל מע״מ', value: F.eur(r.lawyer) }
      ];
      if (r.agent) lines.push({ label: 'מתווך, כולל מע״מ', value: F.eur(r.agent) });
      if (r.eng) lines.push({ label: 'מהנדס', value: F.eur(r.eng) });
      if (r.loan) lines.push({ label: 'משכנתא ' + F.eur(r.loan) + ': רישום ובדיקת הבנק', value: F.eur(r.mort) });
      lines.push({ label: 'במחיר הזה ב' + R.he, value: 'כ־' + F.num(m2) + ' מ״ר, לפי €' + F.num(R.m2) + ' למ״ר' });
      var gvTier = R.gv, gvNote = v.price >= gvTier ? 'המחיר עובר את סף הגולדן ויזה באזור (' + F.eur(gvTier) + '), בתנאי שזה נכס אחד של 120 מ״ר לפחות.' : 'סף הגולדן ויזה באזור הזה: ' + F.eur(gvTier) + '.';
      var notes = [];
      if (v.when === 'after') notes.push('<b>זו הצעת חוק, לא חוק:</b> משרד האוצר היווני הציע 15.45% מס העברה לקונים שתושבי המס שלהם מחוץ לאיחוד, כולל ישראלים, על חוזים מ־1.7.2027. ההערות לציבור עד ' + F.date(B.tt_noneu_consult) + ', והנוסח עוד יכול להשתנות.');
      else notes.push('<b>חוזה לפני 1.7.2027:</b> לפי ההצעה של משרד האוצר היווני, מאותו יום קונה ישראלי ישלם 15.45% במקום 3.09%. באותה עסקה: ' + F.eur(later.costs - today.costs) + ' יותר. ההצעה עוד לא חוק.');
      if (v.kind === 'new_susp') notes.push('דירה חדשה: היזם מבקש השעיה של המע״מ, ואז הקונה משלם 3.09% במקום 24%. ההשעיה בחוק עד ' + F.date(B.vat_susp_until) + ', והארכה עד סוף 2027 מתוכננת.');
      if (R.border) notes.push('<b>' + R.he + ' באזור גבול:</b> קונה מחוץ לאיחוד, כולל ישראלי, צריך היתר מראש. בלי ההיתר העסקה בטלה, וההליך לוקח חודשים.');
      notes.push(gvNote);
      return {
        answer: { label: 'כמה כסף צריך להביא', value: F.eur(r.cash), tone: 'survey', sub: ils(r.cash, d) + ' · עלויות הקנייה ' + F.num(100 * pct, 1) + '% מהמחיר' },
        breakdown: [{ label: 'המחיר' + (r.loan ? ' פחות המשכנתא' : ''), value: v.price - r.loan, kind: 'housing', shown: F.eur(v.price - r.loan) },
          { label: v.kind === 'new_vat' ? 'מע״מ' : 'מס העברה', value: r.vatNew + r.tt, kind: 'survey', shown: F.eur(r.vatNew + r.tt) },
          { label: 'נוטריון וקדסטר', value: r.notary + r.cad, kind: 'civic', shown: F.eur(r.notary + r.cad) },
          { label: 'עורך דין, מתווך ומהנדס', value: r.lawyer + r.agent + r.eng, kind: 'open', shown: F.eur(r.lawyer + r.agent + r.eng) },
          { label: 'עלויות המשכנתא', value: r.mort, kind: 'sea', shown: F.eur(r.mort) }],
        lines: lines,
        scenarioLabel: 'אותה עסקה בשלושה מצבים',
        scenarios: [{ key: 'now', name: 'חוזה עד 30.6.2027', value: F.eur(today.cash), on: v.when === 'now' }, { key: 'after', name: 'חוזה מ־1.7.2027, לפי ההצעה', value: F.eur(later.cash), on: v.when === 'after' },
          { key: 'vat', name: 'דירה חדשה עם מע״מ', value: F.eur(buy(Object.assign({}, v, { kind: 'new_vat' }), G).cash), on: v.kind === 'new_vat' }],
        note: notes.join('<br>'),
        table: { title: 'כל ההוצאות, ביורו ובשקלים', head: ['הוצאה', 'יורו', 'שקלים', 'איך חושב'], num: [1, 2], phoneHide: [],
          rows: [['מחיר הנכס', F.eur(v.price), ils(v.price, d), KIND[v.kind] + ', ' + R.he]]
            .concat(v.kind === 'new_vat' ? [['מע״מ', F.eur(r.vatNew), ils(r.vatNew, d), '24% מהמחיר, במקום מס העברה']] : [['מס העברה', F.eur(r.tt), ils(r.tt, d), F.num(100 * r.rate, 2) + '% על המחיר או על השווי האובייקטיבי, הגבוה מביניהם; משלם הקונה']])
            .concat([['נוטריון', F.eur(r.notary), ils(r.notary, d), '0.8% עד €120,000, 0.7% עד €380,000, 0.65% עד €2 מיליון, ועוד €20 ומע״מ 24%'],
              ['קדסטר', F.eur(r.cad), ils(r.cad, d), '0.5% ועוד €20'], ['עורך דין', F.eur(r.lawyer), ils(r.lawyer, d), F.num(v.lawyer || 0, 2) + '% ועוד מע״מ 24%']])
            .concat(r.agent ? [['מתווך', F.eur(r.agent), ils(r.agent, d), F.num(v.agent || 0, 2) + '% ועוד מע״מ 24%']] : [])
            .concat(r.eng ? [['מהנדס', F.eur(r.eng), ils(r.eng, d), 'הסכום שהזנתם']] : [])
            .concat(r.loan ? [['משכנתא', '−' + F.eur(r.loan), '−' + ils(r.loan, d), F.num(v.ltv) + '% מהמחיר'], ['רישום המשכנתא ובדיקת הבנק', F.eur(r.mort), ils(r.mort, d), '0.8% מההלוואה, €20, ועוד €750 לבנק']] : [])
            .concat([['כמה להביא', F.eur(r.cash), ils(r.cash, d), 'מחיר − משכנתא + כל העלויות']]) },
        formula: 'כמה להביא = מחיר − משכנתא + מס העברה (או מע״מ) + נוטריון × 1.24 + קדסטר + (עורך דין + מתווך) × 1.24 + מהנדס + עלויות המשכנתא.',
        sources: G.sources.slice(0, 3).concat([fxLine(d)]),
        text: 'קניית נכס ביוון ב־' + F.eur(v.price) + ' (' + R.he + ', ' + KIND[v.kind] + '): צריך להביא ' + F.eur(r.cash) + ' (' + ils(r.cash, d) + '), מתוכם ' + F.eur(r.costs) + ' עלויות קנייה.'
      };
    }
  });

  /* ---------------- grgv ---------------- */
  var AREA = { attica: ['אטיקה, כולל אתונה ופיראוס', 0], thess: ['יחידת סלוניקי', 0], mykonos: ['מיקונוס', 0], santorini: ['סנטוריני', 0], bigisland: ['אי עם יותר מ־3,100 תושבים (כרתים, רודוס, קורפו ועוד)', 0], smallisland: ['אי קטן, עד 3,100 תושבים', 1], mainland: ['שאר היבשה, כולל חלקידיקי', 1] };
  NI.register('grgv', {
    kicker: 'בדיקה · גולדן ויזה ביוון',
    title: 'האם הנכס הזה מזכה בגולדן ויזה',
    lede: 'אזור, סוג הנכס, מחיר ושטח: הבדיקה עוברת על כל תנאי החוק של 2024, נכס אחד, 120 מ״ר, איסור השכרה לטווח קצר, ומחשבת את האגרות לכל המשפחה.',
    strip: function (d) { var t = d.greece.gv.t; return [{ label: 'אטיקה, סלוניקי והאיים הגדולים', value: F.eur(t[0]) }, { label: 'שאר יוון', value: F.eur(t[1]) }, { label: 'הסבה או שימור', value: F.eur(t[2]) }]; },
    presets: [
      { key: 'athens800', label: 'דירה באתונה', sub: '€800,000 · 125 מ״ר', set: { area: 'attica', type: 'res', price: 800000, m2: 125, props: 'one', use: 'own', family: 3 } },
      { key: 'halkidiki400', label: 'בית בחלקידיקי', sub: '€400,000 · 140 מ״ר', set: { area: 'mainland', type: 'res', price: 400000, m2: 140, props: 'one', use: 'long', family: 3 } },
      { key: 'crete400', label: 'בית בכרתים', sub: '€400,000 · 150 מ״ר', set: { area: 'bigisland', type: 'res', price: 400000, m2: 150, props: 'one', use: 'own', family: 2 } },
      { key: 'conv250', label: 'הסבה ממשרד לדירה', sub: '€250,000', set: { area: 'attica', type: 'conv', price: 250000, m2: 70, props: 'one', use: 'long', family: 1 } },
      { key: 'two400', label: 'שתי דירות באתונה', sub: '2 × €400,000', set: { area: 'attica', type: 'res', price: 800000, m2: 130, props: 'many', use: 'long', family: 3 } },
      { key: 'airbnb', label: 'דירה לגולדן ויזה ב־Airbnb', sub: '€800,000', set: { area: 'attica', type: 'res', price: 800000, m2: 120, props: 'one', use: 'short', family: 2 } }
    ],
    defaults: function () { return { area: 'attica', type: 'res', price: 800000, m2: 125, props: 'one', use: 'own', family: 3 }; },
    fields: [
      { id: 'area', label: 'איפה הנכס', type: 'select', options: Object.keys(AREA).map(function (k) { return { value: k, label: AREA[k][0] }; }) },
      { id: 'type', label: 'סוג ההשקעה', type: 'segmented', options: [{ value: 'res', label: 'דירה או בית למגורים' }, { value: 'conv', label: 'הסבה ממסחרי למגורים' }, { value: 'listed', label: 'שיקום מבנה לשימור' }] },
      { id: 'price', label: 'מחיר', type: 'money', unit: '€' },
      { id: 'm2', label: 'שטח עיקרי', type: 'number', unit: 'מ״ר' },
      { id: 'props', label: 'כמה נכסים', type: 'segmented', options: [{ value: 'one', label: 'נכס אחד' }, { value: 'many', label: 'כמה נכסים יחד' }] },
      { id: 'use', label: 'מה עושים בנכס', type: 'segmented', options: [{ value: 'own', label: 'שימוש עצמי' }, { value: 'long', label: 'השכרה לטווח ארוך' }, { value: 'short', label: 'השכרה לטווח קצר' }] },
      { id: 'family', label: 'בני משפחה מלבד המבקש', type: 'number', help: 'בן או בת זוג, ילדים עד 21, הורים של שני בני הזוג.' }
    ],
    compute: function (v, d) {
      var G = d.greece, t = G.gv.t, A = AREA[v.area] || AREA.attica;
      if (!(v.price > 0)) return { error: { field: 'price', msg: 'הקלידו מחיר ביורו.' } };
      var need = v.type === 'res' ? t[A[1]] : t[2], ok = true, why = [];
      if (v.price >= need) why.push('✓ המחיר ' + F.eur(v.price) + ' עובר את הסף ' + F.eur(need) + (v.type === 'res' ? ' באזור הזה' : ' במסלול ההסבה או השימור')); else { ok = false; why.push('✗ חסרים ' + F.eur(need - v.price) + ' עד הסף ' + F.eur(need) + (v.type === 'res' && A[1] === 0 && v.area === 'bigisland' ? '. כרתים, רודוס וקורפו נחשבים איים גדולים, ולכן הסף שם 800 אלף' : '')); }
      if (v.type === 'res') { if ((v.m2 || 0) >= G.gv.m2) why.push('✓ שטח עיקרי ' + F.num(v.m2) + ' מ״ר, לפחות 120'); else { ok = false; why.push('✗ השטח העיקרי צריך להיות לפחות 120 מ״ר בנכס אחד'); }
        if (v.props === 'one') why.push('✓ נכס אחד'); else { ok = false; why.push('✗ במסלולי 800 ו־400 אלף הסכום חייב להיות בנכס אחד; חיבור של כמה נכסים לא מזכה'); } }
      if (v.use === 'short') { ok = false; why.push('✗ נכס של גולדן ויזה אסור בהשכרה לטווח קצר: קנס של ' + F.eur(G.gv.str_fine) + ' וביטול ההיתר'); } else why.push('✓ ' + (v.use === 'long' ? 'השכרה לטווח ארוך מותרת' : 'שימוש עצמי מותר'));
      var fam = Math.max(0, Math.round(v.family || 0)), fees = G.gv.fee_main + fam * G.gv.fee_family + (fam + 1) * 16;
      var cost = buy({ price: v.price, kind: 'resale', when: 'now', lawyer: 1, agent: 2, engineer: 0, ltv: 0 }, G).costs;
      var notes = ['ההיתר ל־' + G.gv.years + ' שנים ומתחדש כל עוד הנכס בבעלותכם. הוא נותן תושבות, לא אזרחות, ולא זכות לעבוד כשכירים ביוון.'];
      if (v.area === 'santorini') notes.push('סנטוריני היא אזור גבול: קונה ישראלי צריך היתר מראש לפני העסקה.');
      return {
        answer: { label: 'התוצאה', value: ok ? 'זכאי' : 'לא זכאי', tone: ok ? 'open' : 'survey', sub: ok ? 'כל התנאים שבדקנו מתקיימים' : 'לפחות תנאי אחד לא מתקיים' },
        lines: why.map(function (w) { return { label: w.slice(2), value: w.charAt(0) === '✓' ? 'עובר' : 'לא עובר' }; }).concat([
          { label: 'אגרות: מבקש ' + F.eur(G.gv.fee_main) + ', ' + fam + ' בני משפחה × ' + F.eur(G.gv.fee_family) + ', כרטיסים', value: F.eur(fees) },
          { label: 'עלויות הקנייה, בערך (עם מתווך ועורך דין)', value: F.eur(cost) },
          { label: 'הכסף שיוצא לגולדן ויזה, בלי המחיר', value: both(fees + cost, d) }]),
        note: notes.join('<br>'),
        table: { title: 'הסכומים לפי אזור', head: ['אזור', 'סף ההשקעה', 'תנאי שטח'], rows: [['אטיקה, יחידת סלוניקי, מיקונוס, סנטוריני ואיים מעל 3,100 תושבים', F.eur(t[0]), '120 מ״ר, נכס אחד'], ['שאר יוון', F.eur(t[1]), '120 מ״ר, נכס אחד'], ['הסבה ממסחרי למגורים או שיקום מבנה לשימור, בכל מקום', F.eur(t[2]), 'אין דרישת שטח']] },
        formula: 'זכאות = מחיר ≥ הסף של האזור, ובמסלול המגורים גם שטח עיקרי ≥ 120 מ״ר בנכס אחד; ובכל מסלול: בלי השכרה לטווח קצר.',
        sources: [{ label: 'חוק 5100/2024, סעיף 64', url: '' }].concat([fxLine(d)]),
        text: 'בדיקת גולדן ויזה ביוון: ' + AREA[v.area][0] + ', ' + F.eur(v.price) + ', ' + F.num(v.m2 || 0) + ' מ״ר: ' + (ok ? 'זכאי' : 'לא זכאי') + '.'
      };
    }
  });

  /* ---------------- gryield ---------------- */
  var TR = { treaty: 'לפי נוסח האמנה: מס רק ביוון', flat15: 'מסלול 15% בישראל', regular: 'מסלול רגיל עם זיכוי' };
  function yPreset(d, key, label, rid, price, m2) { var R = reg(d, rid), rent = R.yld ? Math.round(price * R.yld / 12 / 5) * 5 : 0;
    return { key: key, label: label, sub: F.eur(price) + ' · ' + m2 + ' מ״ר · שכירות ' + F.eur(rent), set: { price: price, m2: m2, rent: rent, months: 11, mgmt: 8, fees: 30, ins: 150, zone: 2000, age: '26+', floor: '2nd_3rd', insured: 'yes', track: 'flat15', dep: 0, marg: 35 } }; }
  NI.register('gryield', {
    kicker: 'מחשבון · תשואה ביוון',
    title: 'כמה נשאר ביד מדירה מושכרת ביוון',
    lede: 'שכירות, תפוסה, ניהול, ENFIA, המס ביוון לפי המדרגות של 2026, והצד הישראלי בשלוש הדרכים האפשריות: התשואה נטו על כל הכסף שהשקעתם.',
    strip: function (d) { return [{ label: 'מס על שכירות ביוון עד €12,000', value: '15%' }, { label: 'מ־€12,000 עד €24,000', value: '25%' }, { label: 'מסלול 15% בישראל', value: '15%' }]; },
    presets: function (d) { return [
      yPreset(d, 'athens', 'דירה במרכז אתונה', 'athens-center', 150000, 60),
      yPreset(d, 'piraeus', 'דירה בפיראוס', 'piraeus', 180000, 75),
      yPreset(d, 'west', 'דירה בפרברי המערב', 'athens-west', 140000, 70),
      yPreset(d, 'glyfada', 'דירה בפרברי הדרום', 'athens-south', 400000, 95),
      yPreset(d, 'thess', 'דירה בסלוניקי', 'thessaloniki', 160000, 65)
    ]; },
    defaults: function (d) { return yPreset(d, 'athens', '', 'athens-center', 150000, 60).set; },
    fields: [
      { id: 'price', label: 'מחיר הדירה', type: 'money', unit: '€' },
      { id: 'm2', label: 'שטח', type: 'number', unit: 'מ״ר' },
      { id: 'rent', label: 'שכירות בחודש', type: 'money', unit: '€', help: 'בפתיחה: לפי תשואת ברוטו שפורסמה לאזור.' },
      { id: 'months', label: 'חודשים מושכרים בשנה', type: 'number' },
      { id: 'mgmt', label: 'חברת ניהול', type: 'percent', unit: '%', help: 'טווח ארוך: לרוב 8% עד 10% מהשכירות.' },
      { id: 'fees', label: 'דמי בניין בחודש', type: 'money', unit: '€' },
      { id: 'ins', label: 'ביטוח בשנה', type: 'money', unit: '€' },
      { id: 'zone', label: 'מחיר האזור (τιμή ζώνης) למ״ר', type: 'money', unit: '€', help: 'המחיר הרשמי שעליו מחושב ENFIA. עורך הדין מוציא אותו לכתובת.' },
      { id: 'age', label: 'גיל הבניין', type: 'select', options: [{ value: '26+', label: '26 שנים ומעלה' }, { value: '20-25', label: '20 עד 25' }, { value: '15-19', label: '15 עד 19' }, { value: '10-14', label: '10 עד 14' }, { value: '5-9', label: '5 עד 9' }, { value: '0-4', label: 'עד 4 שנים' }] },
      { id: 'floor', label: 'קומה', type: 'select', options: [{ value: 'ground_1st', label: 'קרקע או ראשונה' }, { value: '2nd_3rd', label: 'שנייה או שלישית' }, { value: '4th_5th', label: 'רביעית או חמישית' }, { value: '6th_plus', label: 'שישית ומעלה' }, { value: 'detached_house', label: 'בית צמוד קרקע' }] },
      { id: 'insured', label: 'ביטוח רעידת אדמה, אש והצפה', type: 'segmented', options: [{ value: 'yes', label: 'יש' }, { value: 'no', label: 'אין' }], help: 'הנחה של 20% ב־ENFIA.' },
      { id: 'track', label: 'המס בישראל', type: 'segmented', options: [{ value: 'treaty', label: TR.treaty }, { value: 'flat15', label: TR.flat15 }, { value: 'regular', label: TR.regular }] },
      { id: 'marg', label: 'שיעור המס השולי שלכם', type: 'percent', unit: '%', showIf: function (v) { return v.track === 'regular'; } },
      { id: 'dep', label: 'פחת שנתי מותר', type: 'money', unit: '€', help: 'לפי רואה החשבון. 0 אם לא ידוע.', showIf: function (v) { return v.track !== 'treaty'; } }
    ],
    compute: function (v, d) {
      var G = d.greece;
      if (!(v.price >= 20000)) return { error: { field: 'price', msg: 'הקלידו את מחיר הדירה ביורו.' } };
      if (!(v.months >= 0 && v.months <= 12)) return { error: { field: 'months', msg: 'בין 0 ל־12 חודשים.' } };
      if (!(v.m2 > 0)) return { error: { field: 'm2', msg: 'הקלידו שטח במ״ר.' } };
      var r = yieldCalc(v, G, v.track), E = enfia(v, G);
      var sc = ['treaty', 'flat15', 'regular'].map(function (k) { var x = yieldCalc(v, G, k); return { key: k, name: TR[k], value: F.pct(x.ny, 2), on: v.track === k }; });
      return {
        answer: { label: 'תשואה נטו על כל ההשקעה', value: F.pct(r.ny, 2), tone: 'survey', sub: 'נשאר ביד ' + F.eur(r.net) + ' בשנה (' + ils(r.net, d) + ') · ברוטו ' + F.pct(r.gy, 2) },
        breakdown: [{ label: 'נשאר ביד', value: Math.max(0, r.net), kind: 'open', shown: F.eur(r.net) }, { label: 'מס ביוון', value: r.gtx, kind: 'survey', shown: F.eur(r.gtx) },
          { label: 'מס בישראל', value: r.il, kind: 'civic', shown: F.eur(r.il) }, { label: 'ENFIA', value: r.enfia, kind: 'housing', shown: F.eur(r.enfia) },
          { label: 'ניהול, בניין וביטוח', value: r.mg + r.fees, kind: 'sea', shown: F.eur(r.mg + r.fees) }],
        lines: [{ label: 'שכירות בשנה', value: F.eur(r.gross) }, { label: 'ENFIA בשנה', value: F.eur(r.enfia) + (E.disc ? ' (אחרי הנחת ביטוח ' + F.eur(E.disc) + ')' : '') },
          { label: 'מס ביוון לפי מדרגות 2026, אחרי ניכוי 5%', value: F.eur(r.gtx) }, { label: TR[v.track], value: F.eur(r.il) },
          { label: 'סך ההשקעה (מחיר ועלויות קנייה)', value: both(r.invest, d) }],
        scenarioLabel: 'אותה דירה, בכל אחת מדרכי המס בישראל',
        scenarios: sc,
        note: '<b>על המס בישראל:</b> לפי הנוסח האנגלי של אמנת המס בין ישראל ליוון, שגובר במחלוקת, הכנסה משכירות של נכס ביוון חייבת במס רק ביוון. רשות המסים לא פרסמה עמדה, והנוסח העברי שונה. לכן הכלי מראה את שלוש הדרכים, ואת הדרך שלכם קובעים עם רואה חשבון. במסלול 15% אין ניכוי הוצאות ואין זיכוי על המס ביוון.',
        table: { title: 'החשבון המלא, שנה אחת', head: ['שורה', 'יורו', 'שקלים'], num: [1, 2],
          rows: [['שכירות: ' + F.eur(v.rent) + ' × ' + v.months + ' חודשים', F.eur(r.gross), ils(r.gross, d)], ['חברת ניהול ' + F.num(v.mgmt || 0) + '%', '−' + F.eur(r.mg), '−' + ils(r.mg, d)],
            ['דמי בניין וביטוח', '−' + F.eur(r.fees), '−' + ils(r.fees, d)], ['ENFIA: ' + F.num(v.m2) + ' מ״ר × מקדם האזור, הגיל והקומה', '−' + F.eur(r.enfia), '−' + ils(r.enfia, d)],
            ['מס ביוון (15% / 25% / 35% / 45%)', '−' + F.eur(r.gtx), '−' + ils(r.gtx, d)], [TR[v.track], '−' + F.eur(r.il), '−' + ils(r.il, d)], ['נשאר ביד', F.eur(r.net), ils(r.net, d)]] },
        formula: 'תשואה נטו = (שכירות − ניהול − דמי בניין − ביטוח − ENFIA − מס ביוון − מס בישראל) ÷ (מחיר + עלויות הקנייה).',
        sources: G.sources.slice(2).concat([fxLine(d)]),
        text: 'דירה ביוון ב־' + F.eur(v.price) + ', שכירות ' + F.eur(v.rent) + ' בחודש: תשואה נטו ' + F.pct(r.ny, 2) + ' (' + TR[v.track] + '), ' + F.eur(r.net) + ' בשנה.'
      };
    }
  });
})();
