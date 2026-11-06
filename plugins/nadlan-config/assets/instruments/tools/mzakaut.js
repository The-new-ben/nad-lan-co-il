/* NadLan Instruments · mzakaut v1 (HAD-675, mortgage delta row A1/A2, 6.11.2026): "מחשבון זכאות משכנתא", the state eligibility
   loan of the Ministry of Construction and Housing (הלוואת זכאות), for the tools switcher of /mortgage-calculator/ (pane #tool-zakaut).
   Research and every number: docs/research/2026-11-06-mortgage-delta/eligibility.md (gov.il pages S1 to S17, read 6.11.2026).
   The tables live in data/zakaut.json, each with its source id, URL and page date ("checked": "2026-11-06"); this file holds no
   amount of its own.
   - Eight profiles, as the official calculator (S16): משפחה, משפחת עולים, משפחת נכים, משפחה שבראשה הורה עצמאי, נכה רתוק לכסא
     גלגלים, נכה רווק, רווק/ה, עולה חדש/ה.
   - Points: veteran families by S3 (marriage years or a marriage date, children with a pregnancy from week 24, siblings of EACH
     spouse on its own row, as S3 says; zakaut.com sums them, which is wrong); olim families by S11 (seniority, children, +730,
     floors 1,700 / 1,800); single parent 2,200 (S5); veteran singles by age (S4, cap 1,690); olim singles by S12 (+600 / +400, cap
     1,690; the seniority ladder of S11, labelled); disability +200 and the floors of S10.
   - Amounts: the basic loan by band (S3), the service supplement per month by band (S7, at most 36 months a person as in S16, civic
     service 12), reserve 0.5% per 15 full days (S2's unit; S7's wording shown), at least 2% and at most 10% a person, with the
     46% / 65% cap of S7; priority zone א / ב (S8; families in zone א get the 1,500-point amount, S3); 10 פלוס (S9, yes/no questions
     with the income table); the olim supplements (S11, S12). Negev: the 48,000 to 84,000 range in words, never in a total (S13).
   - For singles and olim the headline is the points, and the shekel figure carries the label of eligibility.md section 4.
   - The rate: the RULE in words only (S2); the current rate was not verified. An optional field takes the rate printed on the
     certificate and gives the first payment (Spitzer, rate / 12, index unchanged).
   Pure logic in window.NLZK (node test: docs/research/2026-11-06-mortgage-delta/build-mzakaut/test_mzakaut.js). Hebrew only, RTL;
   on an English mount the tool draws nothing. Runs in the browser: no form is sent, nothing leaves the page. Style id-scoped with
   !important (the theme restyles headings, buttons, inputs, lists and tables). */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;

  var PROFILES = [
    { k: 'family', he: 'משפחה', base: 'vet_family', family: true, couple: true, tenplus: true },
    { k: 'olim_family', he: 'משפחת עולים', base: 'olim_family', family: true, couple: true, tenplus: true },
    { k: 'dis_family', he: 'משפחת נכים', base: 'vet_family', family: true, couple: true, tenplus: true, dis: 'family', olimToggle: true },
    { k: 'single_parent', he: 'משפחה שבראשה הורה עצמאי', base: 'single_parent', family: true, couple: false, tenplus: true },
    { k: 'wheelchair', he: 'נכה רתוק לכסא גלגלים', base: 'vet_family', family: true, couple: true, tenplus: true, dis: 'wheelchair' },
    { k: 'dis_single', he: 'נכה רווק', base: 'vet_single', family: false, couple: false, dis: 'single' },
    { k: 'single', he: 'רווק/ה', base: 'vet_single', family: false, couple: false },
    { k: 'oleh', he: 'עולה חדש/ה', base: 'olim_single', family: false, couple: false }
  ];
  var DIS_F = [{ k: 'plus', he: 'נכות מוכרת: תוספת 200 נקודות' }, { k: '75one', he: 'נכות קבועה 75% אצל אחד מבני הזוג' }, { k: '75both', he: 'שני בני הזוג 75% לפחות' }];
  var DIS_O = [{ k: 'plus', he: 'נכות מוכרת: תוספת 200 נקודות' }, { k: 'a', he: "דרגה א'" }, { k: 'b', he: "דרגה ב', או שני בני הזוג 75%" }];
  var DIS_S = [{ k: 'a', he: "דרגה א'" }, { k: 'b', he: "דרגה ב'" }];
  var TERMS = [30, 25, 20, 15, 10, 9, 8, 7, 6, 5];

  /* ------------------------------------------------------------------------------------------------------------- helpers */
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function isISO(s) { return /^\d{4}-\d{2}-\d{2}$/.test(String(s || '')) && !isNaN(Date.parse(s)); }
  function todayISO(d) { d = d || new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function fullYears(a, b) { var y = +b.slice(0, 4) - +a.slice(0, 4); if (b.slice(5) < a.slice(5)) y--; return y; }  // full years a -> b
  function whole(x) { var s = String(x == null ? '' : x).replace(/[^\d.\-]/g, ''); if (s === '' || s === '-' || s === '.') return NaN; var n = +s; return isFinite(n) ? Math.floor(n) : NaN; }
  function whole0(x) { var n = whole(x); return isFinite(n) ? n : (String(x == null ? '' : x).trim() === '' ? 0 : NaN); }  // optional: empty = 0
  function num(x) { var s = String(x == null ? '' : x).trim(); if (s.indexOf('.') < 0) s = s.replace(',', '.'); s = s.replace(/[^\d.]/g, ''); if (s === '' || s === '.') return NaN; var n = +s; return isFinite(n) ? n : NaN; }
  function dmy(iso) { var p = String(iso || '').split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : ''; }
  var NF = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function nf(x) { return NF.format(Math.round(x || 0)); }
  function ils(x) { return nf(x) + ' ₪'; }
  function err(field, msg) { return { error: { field: field, msg: msg } }; }
  function profile(k) { for (var i = 0; i < PROFILES.length; i++) if (PROFILES[i].k === k) return PROFILES[i]; return null; }

  /* ---------------------------------------------------------------------------------------------------------- the tables */
  function ladder(t, n) { var by = t.by, last = by.length - 1; n = Math.max(0, Math.floor(n)); return n <= last ? by[n] : by[last] + t.step * (n - last); }
  function band(Z, p) {  // the S3 row of a points total; points are always multiples of 10, so the "עד 599" text and the table's 599 never meet
    var rows = Z.bands.rows;
    for (var i = 0; i < rows.length; i++) { var r = rows[i]; if (p >= r[0] && (r[1] == null || p <= r[1])) return { from: r[0], to: r[1], basic: r[2], svc: r[3] }; }
    return null;
  }
  function bandText(B) { return B.to == null ? nf(B.from) + ' ומעלה' : nf(B.from) + ' עד ' + nf(B.to); }
  function singleAge(S, age) {  // S4: 21 to 30: 30; 31: 250; 32: 300 ... 45: 950; from 46 a one-time +200 (46: 1,200)
    if (age < S.age_min) return null;
    if (age <= 30) return S.upto30;
    if (age === 31) return S.at31;
    return S.at32 + S.step * (age - 32) + (age >= S.bonus_from ? S.bonus : 0);
  }
  function olimSuppRow(Z, y) { var rows = Z.olim_family.supplement.rows; for (var i = 0; i < rows.length; i++) { var r = rows[i]; if (y >= r[0] && (r[1] == null || y <= r[1])) return r; } return null; }
  function pmt(P, r, n) { return r > 0 ? P * r / (1 - Math.pow(1 + r, -n)) : P / n; }
  function srcTag(Z, id) {
    var s = Z && Z.sources && Z.sources[id]; if (!s) return 'gov.il';
    return 'gov.il' + (s.updated ? ' · עודכן ' + dmy(s.updated) : s.version ? ' · נוסח ' + dmy(s.version) : s.published ? ' · פורסם ' + dmy(s.published) : '');
  }
  function yearsHe(n) { return n === 0 ? '0 (השנה הראשונה)' : n === 1 ? 'שנה אחת' : n + ' שנים'; }

  function defaults() {
    return { profile: 'family', years: 3, married: '', children: 2, sib1: 2, sib2: 4, israel: 2, age: 35, olim: false,
      disF: 'plus', disO: 'plus', disS: 'a', svc1: 24, svc1t: 'idf', svc2: 20, svc2t: 'idf', res1: false, res1d: '', res2: false, res2d: '',
      zone: 'none', negev: false, tp_stay: false, tp_fam: false, tp_income: false, rate: '', term: 30 };
  }

  /* ------------------------------------------------------------------------------------------------------------ the math */
  function compute(v, Z, today) {
    if (!Z || !Z.bands || !Z.vet_family || !Z.sources) return err(null, 'הנתונים לא נטענו. רעננו את העמוד.');
    today = isISO(today) ? today : todayISO();
    var P = profile(v.profile); if (!P) return err('profile', 'בחרו מצב משפחתי.');
    var olim = P.base === 'olim_family' || (!!P.olimToggle && v.olim === true);
    var base = P.olimToggle && olim ? 'olim_family' : P.base;
    var F = Z.vet_family, parts = [];
    var o = { profile: P.k, he: P.he, base: base, olim: olim, family: P.family, couple: P.couple, parts: parts, status: 'ok', today: today };
    function add(k, label, pts, src, warn) { parts.push({ k: k, label: label, pts: pts, src: src, warn: warn || '' }); }
    function total() { var s = 0; parts.forEach(function (p) { s += p.pts; }); return s; }

    // 1. service and reserve (read first: a young single's eligibility depends on service)
    var persons = P.couple ? 2 : 1, svc = [], months = 0, served = false, i;
    for (i = 1; i <= persons; i++) {
      var m = whole0(v['svc' + i]), t = v['svc' + i + 't'] === 'civic' ? 'civic' : 'idf';
      if (!(m >= 0 && m <= 120)) return err('svc' + i, 'הקלידו חודשי שירות, מ־0 עד 120.');
      var c = Math.min(m, t === 'civic' ? Z.service.civic_cap_months : Z.service.cap_months);
      svc.push({ m: m, t: t, c: c }); months += c; if (m > 0) served = true;
    }
    var R = Z.reserve, res = [], resPct = 0;
    for (i = 1; i <= persons; i++) {
      var on = v['res' + i] === true, d = whole0(v['res' + i + 'd']), pc = 0;
      if (on) {
        if (!(d >= 0 && d <= 3000)) return err('res' + i + 'd', 'הקלידו ימי מילואים, מ־0 עד 3,000.');
        pc = Math.min(R.max_pct_person, Math.max(R.min_pct, R.pct * Math.floor(d / R.per_days)));
        served = true;
      }
      res.push({ on: on, d: d, pct: pc }); resPct += pc;
    }
    var zone = v.zone === 'a' || v.zone === 'b' ? v.zone : 'none';

    // 2. points
    var kids = 0;
    if (base !== 'vet_single' && base !== 'olim_single') {
      kids = whole(v.children);
      if (!(kids >= 0 && kids <= 20)) return err('children', 'הקלידו את מספר הילדים, מ־0 עד 20.');
    }
    o.kids = kids;
    if (base === 'vet_family') {
      var yrs;
      if (v.married) {
        if (!isISO(v.married) || v.married > today) return err('married', 'בחרו תאריך נישואין שכבר עבר, או מחקו אותו והקלידו שנים.');
        yrs = fullYears(v.married, today); o.fromDate = true;
      } else yrs = whole(v.years);
      if (!(yrs >= 0 && yrs <= 70)) return err('years', 'הקלידו שנות נישואין מלאות, מ־0 עד 70.');
      var s1 = whole(v.sib1), s2 = whole(v.sib2);
      if (!(s1 >= 0 && s1 <= 30)) return err('sib1', 'הקלידו מספר אחים ואחיות, מ־0 עד 30.');
      if (!(s2 >= 0 && s2 <= 30)) return err('sib2', 'הקלידו מספר אחים ואחיות, מ־0 עד 30.');
      o.years = yrs; o.sib = [s1, s2];
      add('marriage', 'שנות נישואין: ' + yrs, ladder(F.marriage, yrs), 'S3');
      add('children', 'ילדים: ' + kids, ladder(F.children, kids), 'S3');
      add('sib1', 'אחים ואחיות של בן/בת הזוג הראשון/ה: ' + s1, ladder(F.siblings, s1), 'S3');
      add('sib2', 'אחים ואחיות של בן/בת הזוג השני/ה: ' + s2, ladder(F.siblings, s2), 'S3');
    } else if (base === 'olim_family') {
      var O = Z.olim_family, iy = whole(v.israel);
      if (!(iy >= 0 && iy <= 80)) return err('israel', 'הקלידו שנים מלאות בארץ, מ־0 עד 80.');
      o.israel = iy;
      add('seniority', 'ותק בארץ: ' + yearsHe(iy), ladder(O.seniority, iy), 'S11');
      add('children', 'ילדים: ' + kids, ladder(F.children, kids), 'S11');
      add('fixed', 'תוספת קבועה למשפחות עולים', O.fixed, 'S11');
      var fl = iy < 1 ? O.floor_first_year : O.floor_from_second_year, t0 = total();
      if (t0 < fl) add('floor', 'רצפה למשפחות עולים ' + (iy < 1 ? 'בשנה הראשונה' : 'מהשנה השנייה') + ': ' + nf(fl), fl - t0, 'S11');
    } else if (base === 'single_parent') {
      add('fixed', 'הורה עצמאי: נקבע לפי ' + nf(Z.single_parent.points) + ' נקודות', Z.single_parent.points, 'S5');
    } else {
      var age = whole(v.age);
      if (!(age >= 16 && age <= 110)) return err('age', 'הקלידו גיל, מ־16 עד 110.');
      o.age = age;
      if (base === 'vet_single') {
        var S = Z.vet_single, sb = whole(v.sib1);
        if (!(sb >= 0 && sb <= 30)) return err('sib1', 'הקלידו מספר אחים ואחיות, מ־0 עד 30.');
        o.sib = [sb];
        var ap = singleAge(S, age);
        if (ap == null) o.status = 'age';
        else {
          add('age', 'גיל: ' + age, ap, 'S4');
          add('sib1', 'אחים ואחיות: ' + sb, ladder(F.siblings, sb), 'S4');
          if (total() > S.max) add('cap', 'תקרה ליחידים: ' + nf(S.max) + ' נקודות', S.max - total(), 'S4');
        }
      } else {
        var OS = Z.olim_single, iy2 = whole(v.israel);
        if (!(iy2 >= 0 && iy2 <= 80)) return err('israel', 'הקלידו שנים מלאות בארץ, מ־0 עד 80.');
        o.israel = iy2;
        if (age < OS.age_min) o.status = 'age';
        else {
          add('seniority', 'ותק בארץ: ' + yearsHe(iy2), ladder(Z.olim_family.seniority, iy2), 'S11', OS.seniority_note);
          add('fixed', age <= 45 ? 'תוספת קבועה לעולים יחידים עד גיל 45' : 'תוספת קבועה לעולים יחידים מעל גיל 45', age <= 45 ? OS.fixed_to45 : OS.fixed_over45, 'S12');
          if (total() > OS.max) add('cap', 'תקרה לעולים יחידים: ' + nf(OS.max) + ' נקודות', OS.max - total(), 'S12');
        }
      }
    }

    // 3. disability (S10): +200, then the floor of the level
    if (P.dis && o.status === 'ok') {
      var D = Z.disability, lvl = '', fl2 = 0, flLab = '';
      add('dis', 'תוספת לנכים', D.plus, 'S10');
      if (P.dis === 'wheelchair') { lvl = 'wheelchair'; fl2 = D.vet_family_wheelchair_or_both75; flLab = 'רתוק לכסא גלגלים'; }
      else if (P.dis === 'family' && !olim) { lvl = v.disF === '75one' || v.disF === '75both' ? v.disF : 'plus'; if (lvl === '75one') { fl2 = D.vet_family_75; flLab = 'נכות קבועה 75%'; } else if (lvl === '75both') { fl2 = D.vet_family_wheelchair_or_both75; flLab = 'שני בני הזוג 75%'; } }
      else if (P.dis === 'family') { lvl = v.disO === 'a' || v.disO === 'b' ? v.disO : 'plus'; if (lvl === 'a') { fl2 = D.olim_family_a; flLab = "דרגה א'"; } else if (lvl === 'b') { fl2 = D.olim_family_b_or_both75; flLab = "דרגה ב' או שני בני הזוג 75%"; } }
      else { lvl = v.disS === 'b' ? 'b' : 'a'; if (lvl === 'a') { fl2 = D.vet_single_a_min; flLab = "דרגה א'"; } else { fl2 = D.vet_single_b; flLab = "דרגה ב'"; } }
      var t2 = total();
      if (fl2 && t2 < fl2) add('disfloor', 'רצפה לנכים, ' + flLab + ': ' + nf(fl2), fl2 - t2, 'S10');
      if (P.dis === 'single' && lvl === 'a' && total() > D.vet_single_a_max) add('discap', "תקרה לדרגה א': " + nf(D.vet_single_a_max), D.vet_single_a_max - total(), 'S10');
      o.disLevel = lvl;
    }

    // 4. the band, the status
    var pts = total(); o.points = pts;
    var B = null;
    if (o.status === 'ok') { B = band(Z, pts); if (!B) o.status = base === 'vet_family' ? 'nopoints' : 'noband'; }
    if (base === 'vet_single' && (o.status === 'ok' || o.status === 'noband') && o.age < Z.vet_single.age_everywhere && !(zone !== 'none' && served)) o.status = 'young';

    // 5. the amounts
    var Bu = B;
    if (B && o.status === 'ok' && zone === 'a' && P.family) { var B15 = band(Z, Z.priority.family_a_basic_points); if (B15 && B15.basic > B.basic) { Bu = B15; o.zoneLift = true; } }
    o.band = o.status === 'ok' ? B : null; o.bandUsed = o.status === 'ok' ? Bu : null;
    o.basic = o.status === 'ok' && Bu ? Bu.basic : 0;
    o.svc = svc; o.months = months; o.res = res; o.resPct = resPct; o.svcAmt = 0; o.resAmt = 0; o.capCut = 0; o.capPct = P.family ? R.cap_family_pct : R.cap_single_pct;
    if (o.basic > 0) {
      o.svcAmt = months * Bu.svc;
      o.resAmt = Math.round(resPct / 100 * o.basic);
      if (months * Z.service.pct_per_month + resPct > o.capPct) o.capCut = Math.max(0, o.svcAmt + o.resAmt - Math.round(o.capPct / 100 * o.basic));
    }
    o.svcRes = o.svcAmt + o.resAmt - o.capCut;
    o.zone = zone; o.zoneAmt = 0; o.zoneFirst = 0; o.zoneSingle = false;
    var live = o.status === 'ok' || o.status === 'nopoints' || o.status === 'noband';
    if (zone !== 'none' && live) { var zz = Z.priority[zone]; o.zoneFirst = P.family ? zz.first_family : zz.first_single; o.zoneAmt = P.family ? zz.amount : 0; o.zoneSingle = !P.family; }
    o.negev = !!v.negev && live;
    o.tenplus = null;
    if (P.tenplus) {
      var T = Z.ten_plus, need = zone !== 'none' ? T.min_children_priority : T.min_children, why = [];
      if (kids < need) why.push(zone !== 'none' ? 'באזור עדיפות לאומית: ' + need + ' ילדים לפחות' : need + ' ילדים לפחות');
      if (v.tp_stay !== true) why.push('10 שנים ברציפות בישראל');
      if (v.tp_fam !== true) why.push('10 שנים כזוג או כמשפחה');
      if (v.tp_income !== true) why.push('הכנסה עד התקרה');
      var okT = !why.length && o.status === 'ok';
      o.tenplus = { ok: okT, why: why, asked: v.tp_stay === true || v.tp_fam === true || v.tp_income === true, amount: okT ? T.amount : 0, need: need };
    }
    o.olimSupp = 0; o.olehSupp = 0; o.olimRow = null;
    if (base === 'olim_family' && o.status === 'ok') { var row = olimSuppRow(Z, o.israel); if (row) { o.olimSupp = row[2]; o.olimRow = row; } }
    if (base === 'olim_single' && o.status === 'ok' && o.age > 45 && o.israel >= Z.olim_single.over45_after_years) o.olehSupp = Z.olim_single.over45_supplement;
    o.tp = o.tenplus ? o.tenplus.amount : 0;
    o.eligible = o.basic + o.svcRes + o.tp + o.olehSupp;     // on eligible-loan terms
    o.total = o.eligible + o.olimSupp + o.zoneAmt;           // plus the loans on their own terms (S11 3% / 28 years, S8 4.5% / 20 years)
    o.amountVerified = base === 'vet_family' || base === 'single_parent';

    // 6. the optional payment, from the rate printed on the certificate
    o.rate = null; o.term = 30; o.pay = null;
    if (v.rate !== '' && v.rate != null) {
      var rt = num(v.rate);
      if (!(rt > 0 && rt <= 10)) return err('rate', 'הקלידו את הריבית שבתעודה באחוזים, למשל 2.5 (עד 10).');
      var term = +v.term; if (TERMS.indexOf(term) < 0) term = 30;
      o.rate = rt; o.term = term;
      if (o.eligible > 0) o.pay = pmt(o.eligible, rt / 1200, term * 12);
    }
    return o;
  }

  /* ----------------------------------------------------------------------------------------------------------- the words */
  function statusText(r, Z) {
    if (r.status === 'age') return r.base === 'olim_single' ? 'הסיוע לעולים יחידים מתחיל בגיל 21 (S12).' : 'הסיוע ליחידים מתחיל בגיל 21 (S4).';
    if (r.status === 'young') return 'לפי S4: יחידים זכאים מגיל 30 בכל מקום, ומגיל 21 רק באזור עדיפות לאומית א\' או ב\', ורק מי ששירת בצה"ל או בשירות לאומי. בחרו אזור עדיפות והקלידו את חודשי השירות כדי לראות את הניקוד.';
    if (r.status === 'nopoints') return 'עד 599 נקודות: "לא יהיו זכאים למשכנתא על פי הניקוד. אלא רק לתוספות סיוע הניתנת ביישובים" (S3).'
      + (r.zone === 'a' ? ' לפי S3 משפחה שרוכשת באזור עדיפות א\' מקבלת לפחות את הסכום של 1,500 נקודות; הדף לא אומר אם זה חל גם מתחת ל־599 נקודות, ולכן הסכום הזה לא נכלל כאן. לבדוק בתעודת הזכאות.' : '');
    if (r.status === 'noband') return 'טבלת הסכומים (S3) מתחילה ב־599 נקודות. סכום ליחידים עם ניקוד נמוך יותר לא מפורסם בדפים הרשמיים שקראנו; לבדוק בתעודת הזכאות.';
    return '';
  }
  function headline(r, Z) {
    if (r.status === 'age' || r.status === 'young') return { label: 'הזכאות', value: 'עדיין לא זכאים', text: true };
    if (r.status === 'nopoints') return r.total > 0 ? { label: 'רק תוספת לפי היישוב', value: ils(r.total), text: false } : { label: 'לפי הניקוד', value: 'אין הלוואה לפי הניקוד', text: true };
    if (r.status === 'noband') return { label: 'הניקוד שלכם', value: nf(r.points) + ' נקודות', text: false };
    if (!r.amountVerified) return { label: 'הניקוד שלכם', value: nf(r.points) + ' נקודות', text: false };
    return { label: 'סך הכול, לפי מה שהקלדתם', value: ils(r.total), text: false };
  }
  function sub(r, Z) {  // the line under the headline (plain text)
    if (r.status === 'age' || r.status === 'young') return r.points > 0 ? nf(r.points) + ' נקודות' : '';
    if (r.status === 'nopoints') return nf(r.points) + ' נקודות';
    if (r.status === 'noband') return 'אין שורה בטבלת הסכומים לניקוד הזה';
    var b = 'קבוצת ניקוד ' + bandText(r.band);
    if (!r.amountVerified) return b + ' · סכום משוער ' + ils(r.total) + ': ' + Z.labels.amount_unverified;
    return nf(r.points) + ' נקודות · ' + b;
  }
  /* every line of the result: { label, value, src: [ids], note, kind } (plain text; the page escapes it) */
  function lines(r, Z) {
    var L = [], U = Z.labels.amount_unverified;
    function line(label, value, src, note, kind) { L.push({ label: label, value: value, src: src || [], note: note || '', kind: kind || 'amt' }); }
    r.parts.forEach(function (p) { line(p.label, (p.pts < 0 ? '-' + nf(-p.pts) : (p.k === 'floor' || p.k === 'disfloor' ? '+' : '') + nf(p.pts)) + ' נקודות', [p.src], p.warn, 'pts'); });
    if (r.parts.length) line('סך הנקודות', nf(r.points), [], '', 'sum');
    if (r.status === 'ok' && r.band) {
      line('המשכנתא הבסיסית, קבוצת ניקוד ' + bandText(r.band), ils(r.basic), ['S3'],
        (r.zoneLift ? 'באזור עדיפות א\' משפחה מקבלת לפחות את הסכום של 1,500 נקודות (S3, S8). ' : '') + (r.amountVerified ? '' : U));
      if (r.months > 0) {
        var capped = r.svc.some(function (s) { return s.c < s.m; });
        line('תוספת שירות חובה: ' + r.months + ' חודשים, ' + ils(r.bandUsed.svc) + ' לחודש', ils(r.svcAmt), ['S7'],
          (capped ? 'נספרו עד ' + Z.service.cap_months + ' חודשים לאדם, כמו במחשבון הרשמי (S16), ושירות אזרחי־לאומי עד ' + Z.service.civic_cap_months + ' חודשים (S7). ' : '') + '1% מהמשכנתא הבסיסית לכל חודש מלא.');
      }
      if (r.res.some(function (x) { return x.on; })) {
        line('תוספת מילואים: ' + r.res.filter(function (x) { return x.on; }).map(function (x) { return x.pct + '%'; }).join(' + ') + ' מהמשכנתא הבסיסית', ils(r.resAmt), ['S7', 'S2'],
          'S7 כותב "0.5%" מהמשכנתא הבסיסית בלי יחידה; S2 כותב "0.5% עבור כל 15 ימי מילואים מלאים". החישוב לפי S2: לפחות 2% ועד 10% לאדם, למי שעשה שש שנים לפחות עם 10 ימים לפחות בכל אחת.');
      }
      if (r.capCut > 0) line('תקרת שירות ומילואים: ' + r.capPct + '% מהמשכנתא הבסיסית', '-' + ils(r.capCut), ['S7'], 'יחד, שירות החובה והמילואים עד 46% ליחיד ועד 65% לזוג או משפחה.');
    }
    if (r.zone !== 'none' && (r.status === 'ok' || r.status === 'nopoints' || r.status === 'noband')) {
      var zz = Z.priority[r.zone], zl = r.zone === 'a' ? "א'" : "ב'";
      if (!r.zoneSingle) line('אזור עדיפות לאומית ' + zl + ': הלוואה נוספת בריבית ' + zz.rate_pct + '% ל־' + zz.years + ' שנה, החזר ראשון ' + ils(zz.first_family), ils(zz.amount), ['S8'], zz.only ? zz.only + '.' : '');
      else line('אזור עדיפות לאומית ' + zl + ': החזר ראשון ליחידים ' + ils(zz.first_single), 'לא נכלל בסך הכול', ['S8'], 'S8 מפרסם ליחידים רק את ההחזר הראשון, בלי הסכום. לבדוק בתעודת הזכאות.' + (zz.only ? ' ' + zz.only + '.' : ''), 'info');
    }
    if (r.tenplus && r.status === 'ok' && (r.tenplus.ok || r.tenplus.asked)) {  // shown once a 10 פלוס question was answered yes
      if (r.tenplus.ok) line('תוכנית 10 פלוס, בתנאי הלוואת זכאות', ils(r.tenplus.amount), ['S9']);
      else line('תוכנית 10 פלוס', 'לא נכלל', ['S9'], 'חסר: ' + r.tenplus.why.join(', ') + '.', 'info');
    }
    if (r.olimSupp > 0) line('תוספת למשפחת עולים, ' + r.israel + ' שנים בארץ, בריבית ' + Z.olim_family.supplement.rate_pct + '% ל־' + Z.olim_family.supplement.years + ' שנה', ils(r.olimSupp), ['S11']);
    if (r.olehSupp > 0) line('תוספת לעולה יחיד מעל גיל 45 אחרי ' + Z.olim_single.over45_after_years + ' שנים בארץ, בתנאי הלוואת זכאות', ils(r.olehSupp), ['S12']);
    if (r.negev) line('יישובי הנגב', nf(Z.negev.min) + ' עד ' + nf(Z.negev.max) + ' ₪ לפי היישוב', ['S13'], 'הסכום לכל יישוב לא מפורסם בדף, ולכן הוא לא נכלל בסך הכול. ' + Z.negev.terms + '.', 'info');
    if (r.total > 0) line('סך הכול', ils(r.total), [], (r.olimSupp > 0 || r.zoneAmt > 0 ? 'מזה בתנאי הלוואת זכאות: ' + ils(r.eligible) + '. ' : '') + (r.amountVerified ? '' : U), 'total');
    return L;
  }
  function payText(r) {
    if (r.rate == null) return '';
    if (!(r.pay > 0)) return 'אין סכום בתנאי זכאות לחשב לו החזר.';
    return 'ההחזר הראשון על ' + ils(r.eligible) + ' בתנאי זכאות, בריבית ' + String(r.rate) + '% ל־' + r.term + ' שנה: ' + ils(r.pay) + ' בחודש (לוח שפיצר, הריבית חלקי 12, בלי שינוי במדד).';
  }
  function copyText(r, Z) {
    var head = 'מחשבון זכאות משכנתא: ' + r.he + '. ';
    var st = statusText(r, Z);
    var body;
    if (r.status === 'ok') {
      body = nf(r.points) + ' נקודות, קבוצת ניקוד ' + bandText(r.band) + '. משכנתא בסיסית ' + ils(r.basic)
        + (r.svcRes > 0 ? ', שירות ומילואים ' + ils(r.svcRes) : '') + (r.tp > 0 ? ', 10 פלוס ' + ils(r.tp) : '') + (r.olimSupp > 0 ? ', תוספת עולים ' + ils(r.olimSupp) : '')
        + (r.olehSupp > 0 ? ', תוספת עולה יחיד ' + ils(r.olehSupp) : '') + (r.zoneAmt > 0 ? ', אזור עדיפות ' + ils(r.zoneAmt) : '') + '. סך הכול ' + ils(r.total) + '.'
        + (r.amountVerified ? '' : ' הסכום בשקלים ' + Z.labels.amount_unverified + '.');
    } else body = (r.points > 0 ? nf(r.points) + ' נקודות. ' : '') + st + (r.total > 0 ? ' סך הכול ' + ils(r.total) + '.' : '');
    return head + body + ' ' + Z.binding.text + ' (S1). לפי דפי משרד הבינוי והשיכון באתר הממשלה, נבדק ב־' + dmy(Z.checked) + '.';
  }

  G.NLZK = { compute: compute, lines: lines, headline: headline, sub: sub, statusText: statusText, payText: payText, copyText: copyText,
    ladder: ladder, band: band, singleAge: singleAge, fullYears: fullYears, srcTag: srcTag, defaults: defaults, pmt: pmt,
    PROFILES: PROFILES, DIS_F: DIS_F, DIS_O: DIS_O, DIS_S: DIS_S, TERMS: TERMS };
  if (!G.NadLanInstruments) return;

  /* ------------------------------------------------------------------------------------------------------------ the page */
  var NI = G.NadLanInstruments, esc = NI.esc;
  var CSS = '#nlzk{font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#12202A;background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:16px;display:flex;flex-direction:column;gap:14px;margin:8px 0 16px}'
    + '#nlzk *{box-sizing:border-box}#nlzk [hidden]{display:none!important}'
    + '#nlzk p.nlzk__k{margin:0!important;font:500 12px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;letter-spacing:.04em;color:#5E6A75!important}'
    + '#nlzk h2.nlzk__h{margin:0!important;padding:0!important;border:0!important;font:600 20px/28px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important;text-wrap:balance}#nlzk h2.nlzk__h::before,#nlzk h2.nlzk__h::after{display:none!important}'
    + '#nlzk p.nlzk__lede{margin:0!important;font:400 14px/22px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important}'
    + '#nlzk .nlzk__grid{display:grid;grid-template-columns:minmax(0,1fr);grid-template-areas:"a" "r" "b" "m";gap:16px}'
    + '@media (min-width:960px){#nlzk{padding:24px}#nlzk .nlzk__grid{grid-template-columns:minmax(0,440px) minmax(0,1fr);grid-template-areas:"a r" "b m";gap:16px 28px;align-items:start}}'
    + '#nlzk .nlzk__fa{grid-area:a}#nlzk .nlzk__fb{grid-area:b}#nlzk .nlzk__res{grid-area:r;min-width:0;display:flex;flex-direction:column;gap:12px}#nlzk .nlzk__more{grid-area:m;min-width:0}'
    + '#nlzk .nlzk__sp{white-space:nowrap}'
    + '#nlzk .nlzk__fa,#nlzk .nlzk__fb{display:flex;flex-direction:column;gap:12px;min-width:0}'
    + '#nlzk p.nlzk__sec{margin:6px 0 0!important;padding:8px 0 0!important;border-top:1px solid #D3DCE2;font:600 14px/20px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#1F4B5C!important}'
    + '#nlzk p.nlzk__pt{margin:0!important;font:600 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}'
    + '#nlzk .nlzk__person{display:flex;flex-direction:column;gap:10px;padding:10px 12px;background:#F6F8F9;border-radius:2px}'
    + '#nlzk .nlzk__x2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;align-items:start}'
    + '#nlzk .nlzk__lab{display:block;font:500 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important;margin:0 0 6px!important}'
    + '#nlzk .nlzk__in{display:flex;align-items:stretch;gap:6px;height:48px;padding:0 10px;border:1px solid #2F6F86;border-radius:2px;background:#fff}'
    + '#nlzk .nlzk__in input,#nlzk .nlzk__in select{flex:1 1 auto;min-width:0;width:100%!important;max-width:100%!important;height:auto!important;min-height:44px!important;margin:0!important;border:0!important;border-radius:0!important;outline:0;background:transparent!important;box-shadow:none!important;padding:0!important;font:400 17px/1.2 "IBM Plex Mono",ui-monospace,monospace!important;color:#12202A!important;text-align:right}'
    + '#nlzk .nlzk__in input[type="date"]{font-size:15px!important}#nlzk .nlzk__in select{-webkit-appearance:menulist!important;appearance:auto!important;font:400 16px/1.2 "IBM Plex Sans Hebrew",system-ui,sans-serif!important;cursor:pointer}'
    + '#nlzk .nlzk__in span{align-self:center;font:400 15px/1 "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}'
    + '#nlzk .nlzk__in:focus-within{outline:2px solid #2F6F86;outline-offset:1px}'
    + '#nlzk .nlzk__help{display:block;margin:6px 0 0;font:400 12px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#5E6A75!important}#nlzk .nlzk__help a{color:#2F6F86!important}'
    + '#nlzk .nlzk__err{display:block;font:500 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#C42550!important;margin:4px 0 0}#nlzk .nlzk__err:empty{display:none}'
    + '#nlzk .nlzk__seg{display:grid;grid-template-columns:repeat(var(--n,2),minmax(0,1fr));gap:6px}'
    + '#nlzk .nlzk__prof{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}@media (min-width:600px){#nlzk .nlzk__prof{grid-template-columns:repeat(4,minmax(0,1fr))}}@media (min-width:960px){#nlzk .nlzk__prof{grid-template-columns:repeat(2,minmax(0,1fr))}}'
    + '#nlzk .nlzk__seg button,#nlzk .nlzk__prof button{min-height:44px!important;height:auto!important;margin:0!important;padding:6px 6px!important;border-radius:2px!important;border:1px solid #D3DCE2!important;background:#fff!important;color:#3E4C58!important;font:400 13px/1.3 "IBM Plex Sans Hebrew",system-ui,sans-serif!important;box-shadow:none!important;cursor:pointer;text-align:center;text-transform:none!important;letter-spacing:0!important;width:auto!important;white-space:normal!important}'
    + '#nlzk .nlzk__prof button{min-height:48px!important;font-size:14px!important}'
    + '#nlzk .nlzk__seg button[aria-pressed="true"],#nlzk .nlzk__prof button[aria-pressed="true"]{background:#2F6F86!important;border-color:#2F6F86!important;color:#fff!important;font-weight:600!important}'
    + '#nlzk button:focus-visible,#nlzk a:focus-visible{outline:2px solid #1F4B5C!important;outline-offset:2px}'
    + '#nlzk table.nlzk__inc{border-collapse:collapse!important;margin:4px 0 0!important;width:auto!important;border:0!important;background:none!important}'
    + '#nlzk table.nlzk__inc th,#nlzk table.nlzk__inc td{padding:3px 10px 3px 0!important;border:0!important;border-bottom:1px solid #D3DCE2!important;background:none!important;font:400 12px/18px "IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace!important;color:#3E4C58!important;text-align:right!important}'
    + '#nlzk table.nlzk__inc th{font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif!important;font-weight:500!important}'
    + '#nlzk .nlzk__out{display:flex;flex-direction:column;gap:6px;border-top:2px solid #12202A;padding-top:12px}'
    + '#nlzk .nlzk__ol{font:500 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important}'
    + '#nlzk .nlzk__fig{font:500 38px/44px "IBM Plex Mono",ui-monospace,monospace!important;color:#12202A!important}#nlzk .nlzk__fig.is-text{font:600 26px/34px "IBM Plex Sans Hebrew",system-ui,sans-serif!important}'
    + '#nlzk p.nlzk__sub{margin:0!important;font:400 13px/21px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important}'
    + '#nlzk p.nlzk__msg{margin:0!important;padding:10px 12px!important;background:#F6F8F9;border-inline-start:3px solid #C42550;font:500 14px/22px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}'
    + '#nlzk p.nlzk__msg.is-info{border-inline-start-color:#2F6F86}'
    + '#nlzk ol.nlzk__ls{list-style:none!important;margin:6px 0 0!important;padding:0!important;display:flex;flex-direction:column}'
    + '#nlzk ol.nlzk__ls>li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 12px;margin:0!important;padding:8px 0!important;border-bottom:1px solid #D3DCE2;list-style:none!important;background:none!important}'
    + '#nlzk ol.nlzk__ls>li::before,#nlzk ol.nlzk__ls>li::marker{content:none!important;display:none!important}'
    + '#nlzk .nlzk__lk{font:400 14px/21px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}'
    + '#nlzk .nlzk__lv{font:500 15px/21px "IBM Plex Mono",ui-monospace,monospace!important;color:#12202A!important;white-space:nowrap;text-align:left}'
    + '#nlzk li.is-info .nlzk__lv{grid-column:1/-1;white-space:normal;text-align:right;font:500 14px/21px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important}'
    + '#nlzk li.is-pts .nlzk__lk,#nlzk li.is-pts .nlzk__lv{font-size:13px!important;color:#3E4C58!important}'
    + '#nlzk li.is-sum{border-bottom:2px solid #D3DCE2!important}#nlzk li.is-sum .nlzk__lk{font-weight:600!important}'
    + '#nlzk ol.nlzk__ls>li.is-total{background:#F6F8F9!important;border-inline-start:3px solid #2F6F86;padding:10px 12px!important;margin-top:6px!important;border-bottom:0!important}#nlzk li.is-total .nlzk__lk,#nlzk li.is-total .nlzk__lv{font-weight:600!important;font-size:16px!important}'
    + '#nlzk .nlzk__ln{grid-column:1/-1;font:400 12px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#5E6A75!important}'
    + '#nlzk .nlzk__s{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:4px 10px}'
    + '#nlzk .nlzk__s a{font:400 11px/16px "IBM Plex Mono",ui-monospace,monospace!important;color:#2F6F86!important;text-decoration:underline!important;text-underline-offset:2px}'
    + '#nlzk p.nlzk__pay{margin:6px 0 0!important;font:500 14px/22px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}'
    + '#nlzk .nlzk__more{display:grid;grid-template-columns:minmax(0,1fr);gap:14px;border-top:1px solid #D3DCE2;padding-top:12px}'
    + '@media (min-width:1100px){#nlzk .nlzk__more{grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 24px}#nlzk .nlzk__more>div:last-child{grid-column:1/-1}}'
    + '#nlzk .nlzk__more p.nlzk__mh{margin:0 0 6px!important;font:600 14px/20px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#1F4B5C!important}'
    + '#nlzk .nlzk__more ul,#nlzk .nlzk__more ol{margin:0!important;padding:0 18px 0 0!important}#nlzk .nlzk__more li{margin:0 0 6px!important;font:400 13px/20px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important;background:none!important}'
    + '#nlzk .nlzk__more ul li{list-style:none!important;padding:0!important}#nlzk .nlzk__more ul li::before{display:none!important}'
    + '#nlzk .nlzk__more a{color:#2F6F86!important;text-decoration:underline!important;text-underline-offset:2px;display:inline-block;min-height:24px}'
    + '#nlzk .nlzk__more small{font:400 11px/16px "IBM Plex Mono",ui-monospace,monospace!important;color:#5E6A75!important}'
    + '#nlzk p.nlzk__bind{margin:0!important;padding:10px 12px!important;border:1px solid #1F4B5C;border-radius:2px;font:500 14px/22px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}'
    + '#nlzk p.nlzk__fine{margin:0!important;font:400 12px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#5E6A75!important}'
    + '#nlzk button.nlzk__copy{align-self:flex-start;min-height:44px!important;margin:0!important;padding:0 16px!important;border-radius:999px!important;border:1px solid #D3DCE2!important;background:#fff!important;color:#3E4C58!important;font:500 14px/1.2 "IBM Plex Sans Hebrew",system-ui,sans-serif!important;box-shadow:none!important;cursor:pointer;width:auto!important}';
  function ensureCss() { if (document.getElementById('nlzk-css')) return; var s = document.createElement('style'); s.id = 'nlzk-css'; s.textContent = CSS; document.head.appendChild(s); }

  NI.register('mzakaut', {
    custom: function (root, data) {
      if (NI.langOf && NI.langOf(root) === 'en') return;  // Hebrew only
      var Z = data.zakaut || data.d0;
      if (!Z || !Z.bands) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
      build(root, Z);
    }
  });

  function build(root, Z) {
    ensureCss();
    var v = defaults();
    function src(id) { var s = Z.sources[id]; return s ? '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(srcTag(Z, id)) + '</a>' : esc(id); }
    function srcP(id, tail) { return '<span class="nlzk__sp">(' + src(id) + (tail || '') + ')</span>'; }  // the brackets stay with the link on a narrow line
    function orList(a) { return a.length > 1 ? a.slice(0, -1).join(', ') + ' או ' + a[a.length - 1] : String(a[0]); }
    function fld(key, lab, opt) {
      opt = opt || {};
      var id = 'nlzk-' + key;
      var inp = opt.date ? '<input id="' + id + '" type="date" data-k="' + key + '"' + (opt.help ? ' aria-describedby="' + id + '-h"' : '') + '>'
        : '<input id="' + id + '" inputmode="' + (opt.dec ? 'decimal' : 'numeric') + '" autocomplete="off" data-k="' + key + '"' + (opt.help ? ' aria-describedby="' + id + '-h"' : '') + '>';
      return '<div class="nlzk__f"' + (opt.show ? ' data-v="' + opt.show + '"' : '') + '><label class="nlzk__lab" for="' + id + '"' + (opt.dyn ? ' data-lab="' + key + '"' : '') + '>' + lab + '</label>'
        + '<div class="nlzk__in">' + inp + (opt.unit ? '<span>' + opt.unit + '</span>' : '') + '</div>'
        + (opt.help ? '<span class="nlzk__help" id="' + id + '-h"' + (opt.dynHelp ? ' data-help="' + key + '"' : '') + '>' + opt.help + '</span>' : '')
        + '<span class="nlzk__err" data-err="' + key + '" aria-live="polite"></span></div>';
    }
    function seg(key, lab, items, show, help, cols) {
      var id = 'nlzk-' + key + '-l';
      return '<div class="nlzk__f"' + (show ? ' data-v="' + show + '"' : '') + '><span class="nlzk__lab" id="' + id + '">' + lab + '</span>'
        + '<div class="nlzk__seg" style="--n:' + (cols || items.length) + '" role="group" aria-labelledby="' + id + '">'
        + items.map(function (x) { return '<button type="button" data-s="' + key + '" data-val="' + esc(String(x.k)) + '">' + esc(x.he) + '</button>'; }).join('') + '</div>'
        + (help ? '<span class="nlzk__help">' + help + '</span>' : '') + '</div>';
    }
    var YN = [{ k: '0', he: 'לא' }, { k: '1', he: 'כן' }];
    var SVT = [{ k: 'idf', he: 'צה"ל' }, { k: 'civic', he: 'לאומי־אזרחי' }];
    function person(n) {
      return '<div class="nlzk__person" data-v="p' + n + '"><p class="nlzk__pt" data-lab="p' + n + '">' + (n === 1 ? 'בן/בת הזוג הראשון/ה' : 'בן/בת הזוג השני/ה') + '</p>'
        + '<div class="nlzk__x2">' + fld('svc' + n, 'חודשי שירות חובה', {}) + seg('svc' + n + 't', 'סוג השירות', SVT) + '</div>'
        + seg('res' + n, 'מילואים פעיל: שש שנים לפחות, 10 ימים לפחות בכל שנה?', YN)
        + fld('res' + n + 'd', 'ימי מילואים מלאים, סך הכול', { show: 'res' + n + 'd' }) + '</div>';
    }
    var kidsHelpVet = 'ילד: לא נשוי, עד גיל 21, גר אצלכם דרך קבע. היריון משבוע 24 נחשב ילד נוסף (S3); ברשימת המסמכים (S2) כתוב "מחודש חמישי".';
    var kidsHelpOlim = 'ילד: לא נשוי ומתחת לגיל 25 בעלייה, וגם ילדים שנולדו אחרי העלייה. היריון משבוע 24 נחשב ילד נוסף (S11).';
    var inc = '<table class="nlzk__inc"><thead><tr><th scope="col">שנה</th><th scope="col">הכנסה בחודש עד</th></tr></thead><tbody>'
      + Z.ten_plus.income.map(function (r) { return '<tr><td>' + r[0] + '</td><td>' + nf(r[1]) + ' ₪</td></tr>'; }).join('') + '</tbody></table>';
    var h = '<div class="nlzk" id="nlzk" dir="rtl" lang="he">'
      + '<p class="nlzk__k">מחשבון · הלוואת זכאות</p>'
      + '<h2 class="nlzk__h">מחשבון זכאות משכנתא: הניקוד, הסכום והתוספות</h2>'
      + '<p class="nlzk__lede">הלוואת הזכאות של משרד הבינוי והשיכון, לפי הטבלאות שפורסמו באתר הממשלה. החישוב נעשה כאן בדפדפן, ושום נתון לא נשלח.</p>'
      + '<div class="nlzk__grid"><div class="nlzk__fa">'
      + '<div class="nlzk__f"><span class="nlzk__lab" id="nlzk-prof-l">מי מבקש</span><div class="nlzk__prof" role="group" aria-labelledby="nlzk-prof-l">'
      + PROFILES.map(function (p) { return '<button type="button" data-p="' + p.k + '">' + esc(p.he) + '</button>'; }).join('') + '</div>'
      + '<span class="nlzk__help" data-v="wheelHelp">רתוק לכסא גלגלים במשפחה ותיקה (S10). יחידים: "נכה רווק". משפחת עולים: "משפחת נכים" ו"גם משפחת עולים".</span></div>'
      + seg('olim', 'גם משפחת עולים?', YN, 'olimq')
      + '<div class="nlzk__x2" data-v="yrs">' + fld('years', 'שנות נישואין מלאות', {}) + fld('married', 'או תאריך הנישואין', { date: true }) + '</div>'
      + '<span class="nlzk__help" data-v="yrs">זוג רשום לנישואין: 0 (30 נקודות, ואישור נישואין מהרבנות תוך שלושה חודשים). ידועים בציבור: מיום שהתחילו משק בית משותף, באישור ועדת חריגים (S3); זוג ותיק: גיל הילד המשותף הבכור ועוד שנה (S6).</span>'
      + fld('israel', 'שנים מלאות בארץ מאז קבלת מעמד עולה', { show: 'israel', help: '0 = השנה הראשונה.' })
      + fld('age', 'גיל', { show: 'age' })
      + fld('children', 'ילדים, כולל היריון משבוע 24', { show: 'kids', help: kidsHelpVet, dynHelp: true })
      + '<div class="nlzk__x2" data-v="sib">' + fld('sib1', 'אחים ואחיות של בן/בת הזוג הראשון/ה', { dyn: true }) + fld('sib2', 'אחים ואחיות של בן/בת הזוג השני/ה', { show: 'sib2' }) + '</div>'
      + '<span class="nlzk__help" data-v="sib">רק אחים ואחיות אזרחים ותושבי ישראל. כל אחד מבני הזוג נספר בנפרד, בטבלה משלו (S3).</span>'
      + seg('disF', 'הנכות', DIS_F, 'disF', '', 1) + seg('disO', 'הנכות', DIS_O, 'disO', '', 1)
      + seg('disS', 'הנכות', DIS_S, 'disS', 'דרגה א\': לפחות 1,500 ועד 1,890 נקודות. דרגה ב\': 2,000 נקודות, והדוגמה באותו דף (S10) מגיעה ל־2,200.')
      + '</div>'
      + '<div class="nlzk__res"><div class="nlzk__out" aria-live="polite"><p class="nlzk__msg" hidden></p>'
      + '<div class="nlzk__ok"><span class="nlzk__ol"></span><div class="nlzk__fig"></div><p class="nlzk__sub"></p><p class="nlzk__msg is-info" data-st hidden></p>'
      + '<ol class="nlzk__ls" aria-label="החישוב שורה אחרי שורה"></ol><p class="nlzk__pay" hidden></p></div></div>'
      + '<p class="nlzk__bind">' + esc(Z.binding.text) + ' ' + srcP('S1') + '. המחשבון הזה מחשב לפי הטבלאות שפורסמו באתר הממשלה ונבדקו ב־' + dmy(Z.checked) + '.</p>'
      + '<button type="button" class="nlzk__copy">העתקת התוצאה</button></div>'
      + '<div class="nlzk__fb">'
      + '<p class="nlzk__sec">שירות חובה ומילואים</p>'
      + person(1) + person(2)
      + '<span class="nlzk__help">שירות חובה בצה"ל נספר עד 36 חודשים לאדם, כמו במחשבון הרשמי; שירות לאומי־אזרחי עד 12 חודשים. חייל בשירות סופר חודשים עד יום הבקשה (S7).</span>'
      + '<p class="nlzk__sec">איפה קונים</p>'
      + seg('zone', 'אזור עדיפות לאומית', [{ k: 'none', he: 'לא' }, { k: 'a', he: "א'" }, { k: 'b', he: "ב'" }], '', '<a href="' + esc(Z.sources.S15.url) + '" target="_blank" rel="noopener">רשימת יישובי עדיפות לאומית</a> באתר משרד הבינוי והשיכון (S15).')
      + seg('negev', 'יישוב בנגב לפי חוק הלוואות לדיור?', YN)
      + '<p class="nlzk__sec" data-v="tp">תוכנית 10 פלוס</p>'
      + '<div class="nlzk__f" data-v="tp"><span class="nlzk__help" style="margin:0">132,000 ₪ בתנאי הלוואת זכאות לזוג או למשפחה שבראשה הורה עצמאי, עם 2 ילדים לפחות (באזור עדיפות לאומית 4 לפחות) (S9).</span></div>'
      + seg('tp_stay', 'גרים בישראל ברציפות 10 שנים לפחות? (נסיעות לחו"ל עד חודשיים מותרות)', YN, 'tp')
      + seg('tp_fam', '10 שנים לפחות כזוג או כמשפחה?', YN, 'tp')
      + seg('tp_income', 'ההכנסה ממשכורת של משק הבית עד הסכום בטבלה, או קצבת הבטחת הכנסה?', YN, 'tp')
      + '<div class="nlzk__f" data-v="tp">' + inc + '</div>'
      + '<p class="nlzk__sec">ההחזר החודשי, אם יש לכם תעודה</p>'
      + '<div class="nlzk__x2">' + fld('rate', 'הריבית שבתעודת הזכאות', { unit: '%', dec: true })
      + '<div class="nlzk__f"><label class="nlzk__lab" for="nlzk-term">לתקופה של</label><div class="nlzk__in"><select id="nlzk-term" data-k="term">'
      + TERMS.map(function (y) { return '<option value="' + y + '">' + y + ' שנה</option>'; }).join('') + '</select></div></div></div>'
      + '<span class="nlzk__help">לא חובה. בלי ריבית אין כאן החזר: הריבית העדכנית לא אומתה, והיא מופיעה בתעודה.</span>'
      + '</div>'
      + '<div class="nlzk__more">'
      + '<div><p class="nlzk__mh">הריבית והתנאים</p><ul>'
      + '<li>הריבית: 0.5% מתחת לממוצע הצמודות של בנק ישראל, ולא יותר מ־3%. כלומר הממוצע של ההלוואות הצמודות למדד בבנקים למשכנתאות, כפי שבנק ישראל מפרסם ' + srcP('S2') + '. את הריבית של החודש לא אימתנו, ולכן אין כאן מספר.</li>'
      + '<li>עד ' + Z.terms.max_years + ' שנה, ואפשר לקצר ל־' + orList(Z.terms.shorter_years) + ' שנה ' + srcP('S2') + '.</li>'
      + '<li>צמודה למדד המחירים לצרכן ' + srcP('S2') + '.</li>'
      + '<li>בלי עמלת פירעון מוקדם מכל סוג: זו הלוואה מכוונת ' + srcP('S17', ', סעיף 2') + '.</li>'
      + '<li>הכסף עובר ישירות לחשבון המוכר או הקבלן ' + srcP('S2') + '.</li></ul></div>'
      + '<div><p class="nlzk__mh">איך מקבלים</p><ol>' + Z.process.steps.map(function (s) { return '<li>' + esc(s) + '.</li>'; }).join('') + '</ol>'
      + '<p class="nlzk__fine">כבר חתמתם? ' + esc(Z.process.after_signing) + ' ' + srcP('S2') + '.</p></div>'
      + '<div><p class="nlzk__mh">הדפים הרשמיים</p><ul>'
      + '<li><a href="' + esc(Z.sources.S1.url) + '" target="_blank" rel="noopener">המחשבון הרשמי של משרד הבינוי והשיכון</a> <small>' + esc(srcTag(Z, 'S1')) + '</small></li>'
      + ['S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14'].map(function (k) { return '<li><a href="' + esc(Z.sources[k].url) + '" target="_blank" rel="noopener">' + esc(Z.sources[k].title) + '</a> <small>' + esc(srcTag(Z, k)) + '</small></li>'; }).join('')
      + '</ul><p class="nlzk__mh" style="margin-top:10px!important">באתר שלנו</p><ul>'
      + '<li><a href="#mortgage-tool">מחשבון המסלולים: יש בו מסלול "הלוואת זכאות", בלי עמלת פירעון</a></li>'
      + '<li><a href="/dira-behanacha/">דירה בהנחה</a></li>'
      + '<li><a href="/mortgage-calculator/mortgage-interest-rates/">ריבית משכנתא היום</a></li>'
      + '<li><a href="/mortgage-advisor/">יועצי משכנתא</a></li></ul></div>'
      + '</div></div>'
      + '</div>';
    root.innerHTML = h;
    var q = function (s) { return root.querySelector(s); }, qa = function (s) { return [].slice.call(root.querySelectorAll(s)); };
    // fill the inputs
    qa('input[data-k]').forEach(function (inp) {
      var k = inp.getAttribute('data-k'); inp.value = v[k] == null ? '' : String(v[k]);
      inp.addEventListener('input', function () {
        v[k] = inp.value;
        if (k === 'married') { if (isISO(inp.value)) { var yy = fullYears(inp.value, todayISO()); if (yy >= 0) { v.years = yy; q('#nlzk-years').value = String(yy); } } }
        if (k === 'years' && v.married) { v.married = ''; q('#nlzk-married').value = ''; }
        later();
      });
      if (inp.type === 'date') inp.addEventListener('change', function () { inp.dispatchEvent(new Event('input')); });
    });
    var sel = q('#nlzk-term'); sel.value = String(v.term);
    sel.addEventListener('change', function () { v.term = +sel.value; paint(); });
    var last = null, t = 0;
    function later() { clearTimeout(t); t = setTimeout(paint, 90); }
    root.addEventListener('click', function (e) {
      var b = e.target && e.target.closest ? e.target.closest('button') : null; if (!b || !root.contains(b)) return;
      if (b.hasAttribute('data-p')) { v.profile = b.getAttribute('data-p'); paint(); }
      else if (b.hasAttribute('data-s')) {
        var k = b.getAttribute('data-s'), val = b.getAttribute('data-val');
        v[k] = YN.some(function (x) { return x.k === val; }) && /^(olim|res1|res2|negev|tp_stay|tp_fam|tp_income)$/.test(k) ? val === '1' : val;
        paint();
      } else if (b.classList.contains('nlzk__copy') && last) {
        var tx = copyText(last, Z) + '\n' + location.origin + location.pathname + '#tool-zakaut';
        var done = function () { b.textContent = 'הועתק'; setTimeout(function () { b.textContent = 'העתקת התוצאה'; }, 1600); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(tx).then(done, function () { G.prompt('העתיקו את התוצאה', tx); }); else G.prompt('העתיקו את התוצאה', tx);
      }
    });
    function vis() {
      var P = profile(v.profile), olim = P.base === 'olim_family' || (P.olimToggle && v.olim === true), base = P.olimToggle && olim ? 'olim_family' : P.base;
      return { P: P, base: base, olim: olim, m: {
        wheelHelp: P.k === 'wheelchair', olimq: !!P.olimToggle, yrs: base === 'vet_family', israel: base === 'olim_family' || base === 'olim_single',
        age: base === 'vet_single' || base === 'olim_single', kids: base !== 'vet_single' && base !== 'olim_single', sib: base === 'vet_family' || base === 'vet_single',
        sib2: base === 'vet_family', disF: P.dis === 'family' && !olim, disO: P.dis === 'family' && olim, disS: P.dis === 'single',
        p1: true, p2: P.couple, res1d: v.res1 === true, res2d: P.couple && v.res2 === true, tp: !!P.tenplus } };
    }
    function bval(k) { var x = v[k]; return typeof x === 'boolean' ? (x ? '1' : '0') : String(x); }
    function paint() {
      var V = vis(), P = V.P;
      qa('[data-p]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-p') === v.profile)); });
      qa('[data-s]').forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-val') === bval(x.getAttribute('data-s')))); });
      qa('[data-v]').forEach(function (x) { x.hidden = !V.m[x.getAttribute('data-v')]; });
      q('[data-lab="sib1"]').textContent = P.couple ? 'אחים ואחיות של בן/בת הזוג הראשון/ה' : 'אחים ואחיות';
      q('[data-lab="p1"]').textContent = P.couple ? 'בן/בת הזוג הראשון/ה' : 'שירות';
      q('[data-help="children"]').textContent = V.base === 'olim_family' ? kidsHelpOlim : kidsHelpVet;
      qa('[data-err]').forEach(function (x) { x.textContent = ''; });
      var r;
      try { r = compute(v, Z); } catch (e2) { r = err(null, 'לא הצלחנו לחשב עם הערכים האלה.'); }
      var msg = q('.nlzk__msg'), ok = q('.nlzk__ok');
      if (r.error) {
        var fe = r.error.field && q('[data-err="' + r.error.field + '"]'); if (fe) fe.textContent = r.error.msg;
        msg.textContent = r.error.msg; msg.hidden = false; ok.hidden = true; last = null; q('.nlzk__copy').hidden = true; return;
      }
      msg.hidden = true; ok.hidden = false; q('.nlzk__copy').hidden = false; last = r;
      var hd = headline(r, Z), fig = q('.nlzk__fig');
      q('.nlzk__ol').textContent = hd.label;
      fig.className = 'nlzk__fig' + (hd.text ? ' is-text' : ''); fig.innerHTML = '<bdi>' + esc(hd.value) + '</bdi>';
      var sb = sub(r, Z), sp = q('.nlzk__sub'); sp.textContent = sb; sp.hidden = !sb;
      var stx = statusText(r, Z), sm = q('[data-st]'); sm.textContent = stx; sm.hidden = !stx;
      q('.nlzk__ls').innerHTML = lines(r, Z).map(function (l) {
        var lv = esc(l.value).replace(/^([+\-][\d,]+)/, '<bdi dir="ltr">$1</bdi>');  // "+270" and "-16,848" keep their sign on the left in RTL
        return '<li class="is-' + l.kind + '"><span class="nlzk__lk">' + esc(l.label) + '</span><span class="nlzk__lv"><bdi>' + lv + '</bdi></span>'
          + (l.note ? '<span class="nlzk__ln">' + esc(l.note) + '</span>' : '')
          + (l.src.length ? '<span class="nlzk__s">' + l.src.map(src).join('') + '</span>' : '') + '</li>';
      }).join('');
      var pt = payText(r), pp = q('.nlzk__pay'); pp.textContent = pt; pp.hidden = !pt;
    }
    paint();
  }
})();
