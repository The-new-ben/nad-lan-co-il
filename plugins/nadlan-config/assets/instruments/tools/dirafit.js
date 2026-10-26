/* NadLan Instruments · dirafit + diracost v1 (G1, Ben 26.10.2026: win "מחיר למשתכן" and "דירה בהנחה" on /dira-behanacha/).
   NEW file, local only until a release. Two tools in one file (registry: 'file' => 'dirafit').
   dirafit: who may register, on which track (homeless / housing improver / not eligible), which priorities apply (reserve
     service, local resident, wheelchair), and which three towns gave the most flats per registered household in the newest
     round, beside each town's history in the official lottery file (all registrants and local residents).
   diracost: the flat's price from the price per m2 the lottery page shows, against the median deal price of the same room count
     in the town (data.nadlan.gov.il), with the programme's financing rules (75%, the appraisal route with 100,000 ₪ of own money
     and a 2.1 million ₪ value cap, the 40,000 / 60,000 ₪ grant) and the monthly payment at the Bank of Israel average rate.
   Data: dira-round.json (tools/instruments/build_dira_round.py: the official lottery file + the ministry's releases of 25.5,
   23.6 and 2.8.2026 + gov.il rules + invest.json), boi-mortgage.json, ptax.json. Nothing is estimated: a number the official
   sources do not give is not shown. Pure logic in NLDF for unit checks (tools/instruments/test_dirafit.js). */
(function () {
  'use strict';
  function median(a) { if (!a.length) return null; var s = a.slice().sort(function (x, y) { return x - y; }), m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; }
  function find(list, k) { for (var i = 0; i < list.length; i++) if (list[i].k === k) return list[i]; return null; }
  function town(d, n) { for (var i = 0; i < d.towns.length; i++) if (d.towns[i].n === n) return d.towns[i]; return null; }

  /** Eligibility from the gov.il definitions: {ok, status, first, cont, why}. */
  function eligibility(rules, family, home) {
    var f = find(rules.family, family), h = find(rules.home, home);
    if (!f || !h) return { ok: false, status: 'לא ידוע', why: 'בחרו מצב משפחתי ובעלות על דירה' };
    if (!f.ok) return { ok: false, status: 'לא זכאים', first: false, cont: false, why: f.label + ': ' + (f.note || 'לא מופיע ברשימת הזכאים') };
    if (!h.first && !h.cont) return { ok: false, status: 'לא זכאים', first: false, cont: false, why: h.label };
    return { ok: true, status: h.status, first: !!h.first, cont: !!h.cont, why: h.note || f.note || '' };
  }
  /** Round 11 by town and the national group odds; reserve vs the rest is our calculation (all 7,922 flats won, as the 2.8.2026 release reports about 60% reserve winners). */
  function groups(r11) {
    var res = r11.res_wins / r11.res_regs, rest = (r11.units - r11.res_wins) / (r11.households - r11.res_regs);
    return { all: r11.units / r11.households, res: res, rest: rest, ratio: res / rest, perHH: r11.town_regs / r11.households };
  }
  /** Towns ranked for the reader. sort: 'r11' flats per 100 registered households in round 11, 'hist' median odds of the town's
      lotteries in the file, 'local' median odds of local residents in the file. The local town goes first when the reader is local
      there and the file has local results for it. */
  function rank(d, sort, local) {
    var key = sort === 'hist' ? function (t) { return t.hist.odds; } : sort === 'local' ? function (t) { return t.hist.lodds; } : function (t) { return t.per100 / 100; };
    var list = d.towns.filter(function (t) { return key(t) != null; }).sort(function (a, b) { return key(b) - key(a); });
    var top = list.slice(0, 3).map(function (t) { return t.n; });
    var lt = local ? town(d, local) : null;
    if (lt && lt.hist.lodds != null && top.indexOf(lt.n) < 0) top = [lt.n].concat(top.slice(0, 2));
    else if (lt && top.indexOf(lt.n) > 0) top = [lt.n].concat(top.filter(function (n) { return n !== lt.n; }));
    return { list: list, top: top };
  }
  /** Price and financing (gov.il benefits_in_apartment_funding, 24.2.2026). */
  function pmt(P, ratePct, years) { var r = ratePct / 1200, n = years * 12; return r ? P * r / (1 - Math.pow(1 + r, -n)) : P / n; }
  function cost(v, rules) {
    var price = v.pm * v.size * (v.vat === 'plus' ? 1.18 : 1);
    if (!(price > 0)) return { error: 'price' };
    var A = rules.appraisal, std = rules.ltv * price, cap = std, route = 'std';
    if (v.appraisal > 0 && v.equity >= A.equity_min) {
      var val = v.appraisal <= A.value_cap ? v.appraisal : Math.max(A.value_cap, price);
      var app = Math.min(rules.ltv * val, price - A.equity_min);
      if (app > std) { cap = app; route = 'app'; }
    }
    var grant = Math.min(v.grant || 0, cap), loan = Math.max(0, cap - grant), own = price - cap;
    return { price: price, cap: cap, route: route, grant: grant, loan: loan, own: own, short: Math.max(0, own - (v.equity || 0)),
      pay: pmt(loan, v.rate, v.term), ltv: cap / price };
  }
  function tax(price, br) { var t = 0, lo = 0; for (var i = 0; i < br.length; i++) { var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(price, hi); if (top > lo) t += (top - lo) * br[i][1]; if (price <= hi) break; lo = hi; } return t; }
  window.NLDF = { eligibility: eligibility, groups: groups, rank: rank, cost: cost, pmt: pmt, tax: tax, median: median };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt;
  function pc(x, d) { return x == null ? 'אין נתון' : F.num(100 * x, d == null ? (x < 0.01 ? 2 : 1) : d) + '%'; }
  function q(qk) { var p = String(qk).split('-'); var M = { '03': 'ינואר עד מרץ', '06': 'אפריל עד יוני', '09': 'יולי עד ספטמבר', '12': 'אוקטובר עד דצמבר' }; return p.length === 2 ? (M[p[1]] || p[1]) + ' ' + p[0] : qk; }

  /* ---------------------------------------------------------------- dirafit */
  NI.register('dirafit', {
    kicker: 'בדיקה אישית · דירה בהנחה',
    title: 'מי זכאי, באיזה מסלול, ואיפה הכי כדאי להירשם',
    lede: 'עונים על ארבע שאלות ורואים אם אתם זכאים לפי ההגדרות של משרד הבינוי והשיכון, אילו עדיפויות יש לכם, ואילו שלוש ערים נתנו הכי הרבה דירות לכל משק בית שנרשם בהגרלה האחרונה, לצד ההיסטוריה של כל עיר בקובץ הרשמי.',
    strip: function (dd) { var d = dd.diraround, g = groups(d.r11); return [{ label: 'דירות בהגרלה ה־11', value: F.num(d.r11.units) }, { label: 'משקי בית שנרשמו', value: F.num(d.r11.households) }, { label: 'זכו מכל 100 נרשמים', value: F.num(100 * g.all, 1) }]; },
    defaults: function () { return { family: 'couple', home: 'none', reserve: 'no', local: '', sort: 'r11' }; },
    presets: [
      { key: 'young', label: 'זוג צעיר, בלי דירה', sub: 'בלי מילואים, בלי עיר מגורים בהגרלה', set: { family: 'couple', home: 'none', reserve: 'no', local: '', sort: 'r11' } },
      { key: 'combat', label: 'משרת מילואים לוחם', sub: '60 ימים ומעלה בצו 8', set: { family: 'couple', home: 'none', reserve: 'combat', local: '', sort: 'r11' } },
      { key: 'kgat', label: 'גרים בקריית גת', sub: 'בני מקום', set: { family: 'couple', home: 'none', reserve: 'no', local: 'קריית גת', sort: 'local' } },
      { key: 'single35', label: 'יחידה מגיל 35', sub: 'בלי דירה', set: { family: 'single35', home: 'none', reserve: 'no', local: '', sort: 'r11' } },
      { key: 'upgrade', label: 'משפרי דיור', sub: 'יש דירה יחידה', set: { family: 'couple', home: 'one', reserve: 'no', local: '', sort: 'r11' } }
    ],
    fields: [
      { id: 'family', label: 'מצב משפחתי', type: 'select', optionsFrom: function (v, dd) { return dd.diraround.rules.family.map(function (f) { return { value: f.k, label: f.label }; }); } },
      { id: 'home', label: 'בעלות על דירה', type: 'select', optionsFrom: function (v, dd) { return dd.diraround.rules.home.map(function (h) { return { value: h.k, label: h.label }; }); } },
      { id: 'reserve', label: 'שירות מילואים מ־7.10.2023', type: 'segmented', options: [{ value: 'no', label: 'לא' }, { value: 'yes', label: '60 יום ומעלה' }, { value: 'combat', label: 'לוחם' }],
        help: 'משרת מילואים פעיל: 60 ימים לפחות בצו 8 מ־7.10.2023. את ההגדרה בודקים במוקד המילואים, 1111 שלוחה 4.' },
      { id: 'local', label: 'גרים באחת מערי ההגרלה האחרונה?', type: 'select', optionsFrom: function (v, dd) { return [{ value: '', label: 'לא, באף אחת מהן' }].concat(dd.diraround.towns.slice().sort(function (a, b) { return a.n.localeCompare(b.n, 'he'); }).map(function (t) { return { value: t.n, label: t.n }; })); },
        help: 'בני מקום: גרים בעיר 3 השנים האחרונות, או 4 מתוך 10 השנים האחרונות, לפי רשות האוכלוסין.' },
      { id: 'sort', label: 'סדר הערים לפי', type: 'segmented', options: [{ value: 'r11', label: 'ההגרלה ה־11' }, { value: 'hist', label: 'הקובץ הרשמי' }, { value: 'local', label: 'בני מקום בקובץ' }] }
    ],
    compute: function (v, dd, scen) {
      var d = dd.diraround, R = d.rules, e = eligibility(R, v.family, v.home), g = groups(d.r11), rk = rank(d, v.sort, v.local);
      var res = v.reserve !== 'no', lt = v.local ? town(d, v.local) : null;
      var srcs = [d.sp.regs, d.sp.wins, d.sp.open, R.srcs.zk, R.srcs.el, { label: d.file.source + ', עודכן ' + F.date(d.file.modified), url: d.file.url }];
      var best = town(d, rk.top[0]);
      var answer;
      if (!e.ok) answer = { label: 'לפי ההגדרות של משרד הבינוי והשיכון', value: e.status, tone: 'survey', sub: NI.esc(e.why) };
      else if (!e.first) answer = { label: 'משפרי דיור', value: 'הגרלות המשך בלבד', sub: NI.esc(e.why) };
      else answer = { label: 'העיר הראשונה ברשימה שלכם', value: rk.top[0], sub: (best ? (v.sort === 'r11' || !(lt && lt.n === best.n) ? F.num(best.per100, 1) + ' דירות לכל 100 משקי בית שנרשמו בה בהגרלה ה־11' : 'לבני מקום ' + pc(lt.hist.lodds) + ' בהגרלה טיפוסית בקובץ') : '') + (rk.top.length > 1 ? '. ואחריה ' + rk.top.slice(1).map(NI.esc).join(' ו') : '') };
      // line values stay short (the engine prints them on one line); the explanations go to the note
      var lines = [{ label: 'המעמד שלכם', value: e.ok ? (e.first ? e.status : 'משפר דיור: הגרלות המשך') : e.status }];
      var notes = [];
      if (!e.ok && e.why) notes.push(e.why + '.');
      if (e.ok) {
        lines.push({ label: 'אישור זכאות', value: F.ils(R.cert.cost) + ', עד ' + R.cert.days + ' ימי עבודה' });
        lines.push({ label: 'עדיפות מילואים', value: res ? (v.reserve === 'combat' ? 'כן, כלוחם' : 'כן') : 'לא' });
        lines.push({ label: 'זכו ממשרתי המילואים, הגרלה 11', value: pc(g.res, 1) + ' (' + F.num(d.r11.res_wins) + ' מ־' + F.num(d.r11.res_regs) + ')' });
        lines.push({ label: 'זכו מכל השאר (החישוב שלנו)', value: pc(g.rest, 1) });
        if (lt) {
          lines.push({ label: 'בני מקום ב' + lt.n, value: 'עד ' + pc(R.local.quota, 0) + ' מהדירות' });
          if (lt.hist.lodds != null) lines.push({ label: 'בקובץ: בני מקום מול כולם', value: pc(lt.hist.lodds) + ' מול ' + pc(lt.hist.odds) });
        }
        lines.push({ label: 'ערים להרשמה', value: 'עד ' + R.towns_max + '; בממוצע ' + F.num(g.perHH, 2) });
        if (e.why) notes.push(e.why + '.');
        if (res) notes.push('עדיפות המילואים חלה על אישור זכאות שהונפק אחרי ' + F.date(R.reserve.cert_after) + ', וההגדרה נבדקת מול צה״ל (' + R.reserve.check + '). בהגרלה ה־11 הוקצו כ־50% מהדירות למשרתי מילואים, וכמחצית מהן ללוחמים.');
        if (lt && lt.hist.lodds == null) notes.push('ל' + lt.n + ' אין בקובץ תוצאות של בני מקום, ולכן היא לא עולה לראש הרשימה.');
        notes.push('אישור זכאות מנפיקים דרך ' + R.cert.companies.map(function (c) { return c[0] + ' (' + c[1] + ')'; }).join(', ') + '.');
      }
      lines.push({ label: 'ההגרלה הבאה', value: 'אין הודעה רשמית' });
      notes.push('תנאי לכולם: ' + R.service + '.');
      var sc = [{ key: 'all', name: 'כל הנרשמים, הגרלה 11', value: pc(g.all, 1) }, { key: 'res', name: 'משרתי מילואים', value: pc(g.res, 1) }, { key: 'rest', name: 'כל השאר (החישוב שלנו)', value: pc(g.rest, 1) }];
      var on = scen || (res ? 'res' : 'rest'); sc.forEach(function (s) { s.on = s.key === on; });
      return {
        answer: answer, lines: lines, scenarios: sc, scenarioLabel: 'כמה זכו בהגרלה ה־11, לפי קבוצה',
        note: notes.join(' ') + ' דירות לכל 100 משקי בית = דירות בעיר חלקי משקי הבית שנרשמו להגרלות בה, לפי ההודעה הרשמית מ־23.6.2026. משק בית שנרשם לשלוש ערים זוכה לכל היותר פעם אחת, ולכן זה קרוב לסיכוי בעיר ולא זהה לו. הסיכוי החציוני בקובץ = זוכים חלקי נרשמים בכל הגרלה, החציון של הגרלות העיר מ־' + F.date(d.file.first) + ' עד ' + F.date(d.file.last) + '. ההגרלות ה־10 וה־11 עוד לא נכנסו לקובץ.',
        formula: 'זכו מכל 100 = דירות ÷ משקי בית. מילואים: ' + F.num(d.r11.res_wins) + ' ÷ ' + F.num(d.r11.res_regs) + '. כל השאר: (' + F.num(d.r11.units) + ' − ' + F.num(d.r11.res_wins) + ') ÷ (' + F.num(d.r11.households) + ' − ' + F.num(d.r11.res_regs) + ').',
        sources: srcs,
        table: { title: 'ערי ההגרלה ה־11: דירות, נרשמים וההיסטוריה בקובץ', head: ['עיר', 'סדר', 'דירות', 'משקי בית שנרשמו', 'דירות לכל 100', 'הגרלות בקובץ', 'סיכוי חציוני בקובץ', 'בני מקום בקובץ'], num: [1, 2, 3, 4, 5, 6, 7], phoneHide: [1, 3, 5],
          rows: rk.list.concat(d.towns.filter(function (t) { return rk.list.indexOf(t) < 0; })).map(function (t) { return [t.n + (lt && lt.n === t.n ? ' (אתם בני מקום)' : ''), String(t.order), F.num(t.units), F.num(t.hh), F.num(t.per100, 1), F.num(t.hist.n), t.hist.odds != null ? pc(t.hist.odds) : 'אין', t.hist.lodds != null ? pc(t.hist.lodds) : 'אין']; }) },
        text: e.ok && e.first ? 'דירה בהנחה: שלוש הערים שנתנו את הסיכוי הגבוה ביותר בהגרלה ה־11 בשבילנו: ' + rk.top.join(', ') + '. ' + (res ? 'משרתי מילואים זכו ב־' + pc(g.res, 1) + '.' : 'זכו כ־' + pc(g.rest, 1) + ' מהנרשמים שאינם משרתי מילואים.') : 'דירה בהנחה: ' + e.status + '.'
      };
    }
  });

  /* ---------------------------------------------------------------- diracost */
  NI.register('diracost', {
    kicker: 'מחשבון · דירה בהנחה',
    title: 'כמה תעלה הדירה מההגרלה, ומה ההנחה מול מחירי העסקאות בעיר',
    lede: 'מכניסים את המחיר למ״ר מעמוד הפרויקט באתר ההגרלות ואת שטח הדירה, ורואים את המחיר עם מע״מ, את הפער מול חציון העסקאות של דירות באותו גודל בעיר, כמה הון עצמי צריך לפי כללי התוכנית, ומה ההחזר החודשי.',
    strip: function (dd) { var b = dd.boim; return [{ label: 'מימון לזכאים', value: '75%' }, { label: 'הון עצמי במסלול השמאי', value: F.ils(100000) }, { label: 'ריבית ממוצעת קל״צ, ' + F.month(b.rates.fixed_nl.hist.slice(-1)[0][0]), value: F.num(b.rates.fixed_nl.rate, 2) + '%' }]; },
    defaults: function (dd) { var d = dd.diraround, t = town(d, 'קריית גת') || d.towns[0]; return { town: t.n, pm: t.pm ? t.pm.v : 12000, vat: 'plus', size: 100, rooms: '4', equity: 300000, appraisal: 0, grant: 0, rate: dd.boim.rates.fixed_nl.rate, term: 25 }; },
    presets: function (dd) {
      var d = dd.diraround, P = [];
      [['קריית גת', 100, '4'], ['ראשון לציון', 100, '4'], ['בית שמש', 110, '5'], ['אילת', 90, '4']].forEach(function (x) { var t = town(d, x[0]); if (t && t.pm) P.push({ key: 'p' + t.order, label: x[0] + ', ' + x[1] + ' מ״ר', sub: 'המחיר למ״ר האחרון בקובץ: ' + F.ils(t.pm.v), set: { town: x[0], pm: t.pm.v, size: x[1], rooms: x[2], vat: 'plus' } }); });
      return P;
    },
    fields: [
      { id: 'town', label: 'עיר', type: 'select', optionsFrom: function (v, dd) { return dd.diraround.towns.filter(function (t) { return t.pm || t.mkt; }).sort(function (a, b) { return a.n.localeCompare(b.n, 'he'); }).map(function (t) { return { value: t.n, label: t.n }; }); } },
      { id: 'pm', label: 'מחיר למ״ר בהגרלה', type: 'money', unit: '₪', help: 'המחיר מופיע בעמוד הפרויקט באתר ההגרלות. בפתיחה: המחיר בהגרלה האחרונה של העיר בקובץ הרשמי.' },
      { id: 'vat', label: 'המחיר למ״ר', type: 'segmented', options: [{ value: 'plus', label: 'לפני מע״מ (מוסיפים 18%)' }, { value: 'incl', label: 'כולל מע״מ' }] },
      { id: 'size', label: 'שטח הדירה', type: 'number', unit: 'מ״ר' },
      { id: 'rooms', label: 'השוואה לדירות של', type: 'segmented', options: [{ value: '3', label: '3 חדרים' }, { value: '4', label: '4 חדרים' }, { value: '5', label: '5 חדרים' }] },
      { id: 'equity', label: 'ההון העצמי שלכם', type: 'money', unit: '₪' },
      { id: 'appraisal', label: 'שווי שמאי (אם יש)', type: 'money', unit: '₪', help: 'מסלול השמאי: משכנתא לפי שווי השוק, עם 100,000 ₪ הון עצמי לפחות ושווי עד 2.1 מיליון ₪. 0 = בלי שמאי.' },
      { id: 'grant', label: 'מענק מקום', type: 'segmented', options: [{ value: 0, label: 'אין' }, { value: 40000, label: '40,000 ₪' }, { value: 60000, label: '60,000 ₪' }], help: 'רק ביישובים מזכים, לפי תנאי המכרז.' },
      { id: 'rate', label: 'ריבית המשכנתא', type: 'percent', unit: '%' },
      { id: 'term', label: 'תקופה', type: 'number', unit: 'שנים' }
    ],
    onField: function (id, v, dd, redraw) { if (id === 'town') { var t = town(dd.diraround, v.town); if (t && t.pm) { v.pm = t.pm.v; redraw('pm'); } } },
    compute: function (v, dd, scen) {
      var d = dd.diraround, R = d.rules, t = town(d, v.town);
      if (!(v.pm > 1000)) return { error: { field: 'pm', msg: 'הכניסו מחיר למ״ר מעמוד הפרויקט.' } };
      if (!(v.size >= 30 && v.size <= 250)) return { error: { field: 'size', msg: 'שטח בין 30 ל־250 מ״ר.' } };
      if (!(v.rate >= 0 && v.rate < 15)) return { error: { field: 'rate', msg: 'ריבית בין 0% ל־15%.' } };
      if (!(v.term >= 4 && v.term <= 30)) return { error: { field: 'term', msg: 'תקופה בין 4 ל־30 שנה.' } };
      var w = Object.assign({}, v, { grant: +v.grant || 0 });
      if (scen === 'rate1') w.rate = v.rate + 1; if (scen === 'size10') w.size = v.size + 10;
      var c = cost(w, R), m = t && t.mkt ? t.mkt[v.rooms] : null, ptx = tax(c.price, dd.ptax.tracks.single);
      var gap = m ? m.price - c.price : null;
      var lines = [
        { label: 'מחיר למ״ר עם מע״מ', value: F.ils(c.price / w.size) },
        { label: 'מחיר הדירה, ' + F.num(w.size) + ' מ״ר', value: F.ils(c.price) }];
      if (m) { lines.push({ label: 'חציון ' + v.rooms + ' חדרים, ' + q(m.q), value: F.ils(m.price) }); lines.push({ label: gap >= 0 ? 'מתחת לחציון העסקאות' : 'מעל חציון העסקאות', value: F.ils(Math.abs(gap)) + ' (' + pc(Math.abs(gap) / m.price, 1) + ')' }); }
      else lines.push({ label: 'חציון ' + v.rooms + ' חדרים בעיר', value: 'אין נתון רשמי' });
      lines.push({ label: 'מימון מרבי' + (c.route === 'app' ? ', לפי שמאי' : ''), value: F.ils(c.cap) + ' (' + pc(c.ltv, 0) + ')' });
      if (c.grant) lines.push({ label: 'מתוכו מענק', value: F.ils(c.grant) });
      lines.push({ label: 'הון עצמי נדרש', value: F.ils(c.own) });
      lines.push({ label: c.short ? 'חסרים לכם' : 'ההון שלכם מספיק', value: c.short ? F.ils(c.short) : F.ils((v.equity || 0) - c.own) + ' יותר' });
      lines.push({ label: 'החזר חודשי, ' + F.num(w.rate, 2) + '%, ' + w.term + ' שנה', value: F.ils(c.pay) });
      lines.push({ label: 'מס רכישה, דירה יחידה', value: ptx ? F.ils(ptx) : 'פטור' });
      var rows = d.towns.filter(function (x) { return x.pm && x.mkt && x.mkt[v.rooms]; }).map(function (x) { var p = x.pm.v * w.size * (w.vat === 'plus' ? 1.18 : 1), mm = x.mkt[v.rooms]; return [x.n, F.ils(x.pm.v), F.date(x.pm.date), F.ils(p), F.ils(mm.price), q(mm.q), pc((mm.price - p) / mm.price, 1), (mm.price - p) / mm.price]; })
        .sort(function (a, b) { return b[7] - a[7]; }).map(function (r) { return r.slice(0, 7); });
      return {
        answer: { label: 'מחיר הדירה עם מע״מ', value: F.ils(c.price), sub: m ? (gap >= 0 ? F.ils(gap) + ' מתחת' : F.ils(-gap) + ' מעל') + ' לחציון העסקאות של דירות ' + v.rooms + ' חדרים ב' + NI.esc(t.n) + ' (' + pc(Math.abs(gap) / m.price, 1) + ')' : 'אין חציון עסקאות רשמי להשוואה' },
        breakdown: [{ label: 'הון עצמי', value: c.own, kind: 'sea' }, { label: c.grant ? 'משכנתא ומענק' : 'משכנתא', value: c.cap, kind: 'open' }],  // two segments only: the engine's yellow and purple stay off this page (design law 13.10.2026)
        lines: lines,
        scenarios: [{ key: 'base', name: 'כמו שהכנסתם', value: F.ils(cost(Object.assign({}, v, { grant: +v.grant || 0 }), R).pay) + ' בחודש', on: !scen || scen === 'base' },
          { key: 'rate1', name: 'ריבית גבוהה ב־1%', value: F.ils(cost(Object.assign({}, v, { grant: +v.grant || 0, rate: v.rate + 1 }), R).pay) + ' בחודש', on: scen === 'rate1' },
          { key: 'size10', name: 'דירה גדולה ב־10 מ״ר', value: F.ils(cost(Object.assign({}, v, { grant: +v.grant || 0, size: v.size + 10 }), R).price), on: scen === 'size10' }],
        scenarioLabel: 'ומה אם',
        note: 'חציון העסקאות כולל דירות יד שנייה וחדשות, ולכן הוא לא מחיר של דירה חדשה זהה. המחיר בהגרלה צמוד בחלקו למדד תשומות הבנייה עד המסירה, והמסירה מגיעה שנים אחרי ההגרלה. המחיר למ״ר בפתיחה הוא המחיר בהגרלה האחרונה של העיר בקובץ הרשמי (' + (t && t.pm ? F.date(t.pm.date) : '') + '); בהגרלה חדשה המחיר אחר.',
        formula: 'מחיר = מחיר למ״ר × שטח' + (w.vat === 'plus' ? ' × 1.18' : '') + '. מימון = 75% מהמחיר, או 75% משווי השמאי (עד 2.1 מיליון ₪) עם 100,000 ₪ הון עצמי לפחות; המענק הוא חלק מהמימון. החזר = שפיצר.',
        sources: [R.srcs.fn, { label: d.inv.source + ', גרסה ' + d.inv.version, url: d.inv.url }, { label: d.file.source, url: d.file.url }, { label: 'בנק ישראל, ריביות ממוצעות על משכנתאות', url: 'https://www.boi.org.il/' }],
        table: { title: 'המחיר למ״ר האחרון בכל עיר מול חציון העסקאות, ' + v.rooms + ' חדרים, ' + F.num(w.size) + ' מ״ר', head: ['עיר', 'מחיר למ״ר בקובץ', 'מתאריך', 'מחיר הדירה עם מע״מ', 'חציון העסקאות', 'רבעון', 'הפער'], num: [1, 3, 4, 6], phoneHide: [1, 2, 5], rows: rows },
        text: 'דירה בהנחה ב' + (t ? t.n : '') + ': ' + F.num(w.size) + ' מ״ר ב־' + F.ils(c.price) + ' עם מע״מ' + (m ? ', ' + (gap >= 0 ? F.ils(gap) + ' מתחת' : F.ils(-gap) + ' מעל') + ' לחציון העסקאות' : '') + '. הון עצמי ' + F.ils(c.own) + ', החזר ' + F.ils(c.pay) + ' בחודש.'
      };
    }
  });
})();
