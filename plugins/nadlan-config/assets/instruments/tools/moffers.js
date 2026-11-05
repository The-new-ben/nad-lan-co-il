/* NadLan Instruments · moffers v1 "שלוש הצעות, טבלה אחת" (HAD-675, 5.11.2026). A custom surface on the instruments engine for
   /mortgage-calculator/. Bank of Israel directive 451 (circular 2694, addendum 5) makes every mortgage approval in principle show
   three uniform baskets: basket 1 = all fixed not linked; basket 2 = one third fixed not linked, one third prime, one third
   variable every 5 years CPI-linked; basket 3 = half fixed not linked, half prime (data: boi-mortgage.json "baskets"). For each
   basket the approval shows the predicted overall interest, the total predicted repayment, the highest predicted monthly payment
   (and the first payment). The visitor types these numbers from 2 or 3 approvals, and optionally the bank's own proposed mix.
   Out:
   1. one normalized table: per basket, the banks side by side, the cheapest marked, the gap in shekels over the loan and in the
      highest monthly payment (approvals for different amounts are scaled to the first one's amount; different terms are
      compared by the overall interest instead of the total);
   2. each offer against that bank's own Bank of Israel average ("קו המשווה", by_bank.latest: overall interest and rate per
      track, effective rates converted to nominal like tools/mortgage.js does), and its place between the cheapest and the
      dearest of the five large banks; the wording says a bank average depends on its mix and clients and is not an offer;
   3. a negotiation text in Hebrew, first person singular, with only the typed numbers and the official averages with their month;
   4. a plain link to /mortgage-advisor/.
   Relation to tools/mortgage.js: its "bank-offer-check" block compares ONE offer, track by track, with the system-wide averages
   (SDMX by track and the average-by-term files). This tool does not repeat it: it compares 2 or 3 approvals on the uniform
   baskets, and each bank with its own published average. Pure logic on window.NLMO (tests: test_moffers.js). Hebrew only (RTL);
   no long dash in any string. */
(function () {
  'use strict';

  /* ===================================================================================================== the pure logic */
  var BASKETS = ['b1', 'b2', 'b3'];
  var METRICS = ['irr', 'total', 'maxPay', 'first'];
  var BIG5 = ['hapoalim', 'leumi', 'discount', 'mizrahi', 'fibi'];
  var BANK_HE = { hapoalim: 'בנק הפועלים', leumi: 'בנק לאומי', discount: 'בנק דיסקונט', mizrahi: 'מזרחי טפחות', fibi: 'הבינלאומי', mercantile: 'מרכנתיל', jerusalem: 'בנק ירושלים', system: 'כל הבנקים' };
  var LETTER = ['בנק א׳', 'בנק ב׳', 'בנק ג׳'];
  var MONTH_HE = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
  var TRACK_HE = { fixed_nl: 'קבועה לא צמודה (קל״צ)', prime: 'פריים', var_nl_other: 'משתנה לא צמודה, לא פריים', var_cpi: 'משתנה צמודה למדד', fixed_cpi: 'קבועה צמודה למדד (ק״צ)' };
  var TRACK_KEYS = ['fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi'];
  var MLAB = { irr: 'ריבית כוללת חזויה', total: 'סך התשלומים הצפוי', maxPay: 'ההחזר החודשי הגבוה הצפוי', first: 'ההחזר הראשון' };

  function fin(x) { return typeof x === 'number' && isFinite(x); }
  function num(v) { if (typeof v === 'number') return v; var n = parseFloat(String(v == null ? '' : v).replace(/[^\d.\-]/g, '')); return isFinite(n) ? n : NaN; }
  function r2(x) { return Math.round(x * 100) / 100; }
  function grp(n) { var a = Math.round(Math.abs(n)), s = String(a).replace(/\B(?=(\d{3})+(?!\d))/g, ','); return (n < 0 && a !== 0 ? '-' : '') + s; }
  function ils(n) { return grp(n) + ' ₪'; }
  function pct(n, d) { return Number(n).toFixed(d == null ? 2 : d) + '%'; }
  function yrs(y) { var s = (Math.round(y * 10) / 10).toString(); return s + (y > 10 ? ' שנה' : ' שנים'); }
  function monthHe(key) { var p = String(key || '').split('-'); return p.length > 1 && MONTH_HE[+p[1] - 1] ? MONTH_HE[+p[1] - 1] + ' ' + p[0] : String(key || ''); }
  function ef2nom(e) { return 1200 * (Math.pow(1 + e / 100, 1 / 12) - 1); }  // the same conversion as tools/mortgage.js (monthly payments)
  function pmt(B, annual, n) { var r = annual / 1200; if (!(n > 0)) return NaN; return r === 0 ? B / n : B * r / (1 - Math.pow(1 + r, -n)); }
  function letterOf(i) { return LETTER[i] || ('בנק ' + (i + 1)); }
  function bankName(k) { return k && k !== 'other' && k !== 'system' && BANK_HE[k] ? BANK_HE[k] : ''; }
  function names(offers) {
    var raw = offers.map(function (o, i) { return bankName(o.bank) || letterOf(i); });
    return raw.map(function (n, i) { return raw.filter(function (x) { return x === n; }).length > 1 ? n + ' (' + (LETTER[i] || String(i + 1)).replace('בנק ', '') + ')' : n; });
  }

  /* The typed numbers checked: a number that cannot be right is dropped from the comparison (drop), a doubtful one is only flagged */
  function check(o) {
    var out = [], L = num(o.loan), Y = num(o.years), n = Y * 12;
    if (!(L > 0)) out.push({ b: '', f: 'loan', msg: 'הקלידו את סכום ההלוואה שבאישור.', drop: true });
    if (!(Y >= 1 && Y <= 30)) out.push({ b: '', f: 'years', msg: 'בין שנה אחת ל־30 שנה, לפי בנק ישראל.', drop: true });
    BASKETS.forEach(function (k) {
      var x = (o.b && o.b[k]) || {}, irr = num(x.irr), tot = num(x.total), mx = num(x.maxPay), fs = num(x.first);
      if (fin(irr) && !(irr > 0 && irr < 20)) out.push({ b: k, f: 'irr', msg: 'ריבית בין 0% ל־20%.', drop: true });
      if (fin(tot) && L > 0 && tot < L) out.push({ b: k, f: 'total', msg: 'סך התשלומים נמוך מסכום ההלוואה. בדקו את המספר.', drop: true });
      else if (fin(tot) && fin(mx) && n > 0 && tot > mx * n * 1.005) out.push({ b: k, f: 'total', msg: 'גבוה מההחזר הגבוה כפול מספר החודשים. בדקו את המספר.', drop: false });
      if (fin(mx) && !(mx > 0)) out.push({ b: k, f: 'maxPay', msg: 'הקלידו סכום חיובי.', drop: true });
      else if (fin(mx) && fin(fs) && fs > 0 && mx < fs - 0.5) out.push({ b: k, f: 'maxPay', msg: 'נמוך מההחזר הראשון. בדקו את המספר.', drop: false });
      if (fin(fs) && !(fs > 0)) out.push({ b: k, f: 'first', msg: 'הקלידו סכום חיובי.', drop: true });
    });
    return out;
  }
  function clean(offers) {
    var issues = [];
    var list = offers.map(function (o) {
      var is = check(o), drop = {}; issues.push(is);
      is.forEach(function (x) { if (x.drop) drop[x.b + ':' + x.f] = 1; });
      var c = { bank: o.bank || '', loan: drop[':loan'] ? NaN : num(o.loan), years: drop[':years'] ? NaN : num(o.years), b: {},
        mix: (o.mix || []).map(function (m) { return { track: m.track, share: num(m.share), rate: num(m.rate), years: num(m.years) }; }) };
      BASKETS.forEach(function (k) { var x = (o.b && o.b[k]) || {}; c.b[k] = {}; METRICS.forEach(function (m) { c.b[k][m] = drop[k + ':' + m] ? NaN : num(x[m]); }); });
      return c;
    });
    return { offers: list, issues: issues };
  }
  function hasAny(o) { return BASKETS.some(function (k) { return METRICS.some(function (m) { return fin(o.b[k][m]); }); }); }

  /* Normalization: every shekel figure is scaled to the loan of the first approval (the payments of a fixed mix are proportional
     to the principal); the overall interest is a rate and is not scaled. */
  function normalize(offers) {
    var base = NaN;
    offers.forEach(function (o) { if (!fin(base) && fin(o.loan) && o.loan > 0) base = o.loan; });
    var live = offers.filter(hasAny);
    var ys = live.map(function (o) { return o.years; });
    var termsEqual = ys.length > 0 && ys.every(function (y) { return fin(y) && Math.abs(y - ys[0]) < 0.01; });
    var loansEqual = live.every(function (o) { return fin(o.loan) && Math.abs(o.loan - base) < 0.5; });
    var rows = offers.map(function (o, i) {
      var f = fin(o.loan) && o.loan > 0 && fin(base) ? base / o.loan : NaN, b = {};
      BASKETS.forEach(function (k) {
        var x = o.b[k];
        b[k] = { irr: x.irr, total: x.total, maxPay: x.maxPay, first: x.first, nTotal: x.total * f, nMax: x.maxPay * f, nFirst: x.first * f, perShekel: x.total / o.loan };
      });
      return { i: i, loan: o.loan, years: o.years, factor: f, live: hasAny(o), b: b };
    });
    return { base: base, termsEqual: termsEqual, loansEqual: loansEqual, rows: rows };
  }

  /* The cheapest per basket: the lowest total predicted repayment when the terms are equal; the lowest overall interest when
     they differ (a total over 20 years and a total over 30 years are not the same thing). Ties are all marked. */
  function compare(norm) {
    var out = {};
    BASKETS.forEach(function (k) {
      var by = norm.termsEqual ? 'total' : 'irr';
      var val = function (r) { return by === 'total' ? r.b[k].nTotal : r.b[k].irr; };
      var tol = by === 'total' ? 0.5 : 0.0005;
      var have = norm.rows.filter(function (r) { return fin(val(r)); });
      var res = { k: k, by: by, have: have.map(function (r) { return r.i; }), cheapest: [], dearest: null, gapTotal: NaN, gapMax: NaN, gapIrr: NaN, gapFirst: NaN, vs: {} };
      if (have.length >= 2) {
        var vals = have.map(val), min = Math.min.apply(null, vals), max = Math.max.apply(null, vals);
        var cheap = have.filter(function (r) { return val(r) - min <= tol; }), c = cheap[0];
        res.cheapest = cheap.map(function (r) { return r.i; });
        var d = max - min > tol ? have.filter(function (r) { return max - val(r) <= tol; })[0] : c;
        if (d !== c) res.dearest = d.i;
        res.gapTotal = d.b[k].nTotal - c.b[k].nTotal; res.gapMax = d.b[k].nMax - c.b[k].nMax; res.gapFirst = d.b[k].nFirst - c.b[k].nFirst;
        res.gapIrr = fin(d.b[k].irr) && fin(c.b[k].irr) ? r2(d.b[k].irr - c.b[k].irr) : NaN;
        have.forEach(function (r) { res.vs[r.i] = { dTotal: r.b[k].nTotal - c.b[k].nTotal, dMax: r.b[k].nMax - c.b[k].nMax, dIrr: r.b[k].irr - c.b[k].irr }; });
      }
      out[k] = res;
    });
    return out;
  }

  /* A bank's own Bank of Israel averages (TamInt010, the newest month) and the five large banks ranked by overall interest */
  function bankRef(D, key) {
    var B = D && D.by_bank, L = B && B.latest;
    if (!L || !L.table) return null;
    var find = function (k) { return L.table.filter(function (x) { return x.bank === k; })[0] || null; };
    var row = find(key);
    if (!row) return null;
    var rank = (L.big5_rank_by_irr && L.big5_rank_by_irr.length ? L.big5_rank_by_irr : BIG5).map(function (k) { var r = find(k); return r ? { k: k, irr: r.irr, name: BANK_HE[k] || k } : null; })
      .filter(Boolean).sort(function (a, b) { return a.irr - b.irr; });
    return { key: key, name: BANK_HE[key] || key, month: L.month, irr: row.irr, row: row, sys: find('system'), rank: rank, min: rank[0], max: rank[rank.length - 1],
      big5: BIG5.indexOf(key) > -1, fileDate: B.src && B.src.file_date };
  }
  /* Where an overall interest sits: against the bank's own average, all banks, and the cheapest and dearest of the five large */
  function place(irr, ref) {
    var x = r2(irr), lo = r2(ref.min.irr), hi = r2(ref.max.irr), own = r2(ref.irr), sys = ref.sys ? r2(ref.sys.irr) : NaN;
    var res = { irr: x, own: own, gapOwn: r2(x - own), sys: sys, gapSys: fin(sys) ? r2(x - sys) : NaN, lo: ref.min, hi: ref.max, gapLo: r2(x - lo), gapHi: r2(x - hi), pos: 'between', under: null, over: null };
    if (x < lo) res.pos = 'below';
    else if (x > hi) res.pos = 'above';
    else {
      ref.rank.forEach(function (r) { if (r2(r.irr) <= x) res.under = r; });
      for (var i = 0; i < ref.rank.length; i++) { if (r2(ref.rank[i].irr) >= x) { res.over = ref.rank[i]; break; } }
      if (res.under && res.over && res.under.k === res.over.k) res.pos = 'equal';
    }
    return res;
  }
  /* One track of the bank's own mix against that bank's average for the track (effective, converted to nominal) */
  function trackCmp(m, ref, loan) {
    var t = ref && ref.row ? ref.row[m.track] : null;
    if (!t || !fin(t.rate)) return null;
    var nom = r2(ef2nom(t.rate)), s = ref.sys && ref.sys[m.track] ? ref.sys[m.track] : null, rate = num(m.rate), share = num(m.share), y = num(m.years);
    var res = { track: m.track, eff: t.rate, nom: nom, bankShare: t.share, sysEff: s ? s.rate : NaN, sysNom: s ? r2(ef2nom(s.rate)) : NaN, sysShare: s ? s.share : NaN, rate: rate, share: share, years: y,
      gap: fin(rate) ? r2(rate - nom) : NaN, amount: NaN, payGap: NaN, totalGap: NaN };
    if (fin(rate) && share > 0 && loan > 0 && y > 0) {
      var A = loan * share / 100, n = Math.round(y * 12);
      res.amount = A; res.payGap = pmt(A, rate, n) - pmt(A, nom, n); res.totalGap = res.payGap * n;
    }
    return res;
  }

  function basketText(D, k) {
    var b = D && D.baskets && D.baskets.list ? D.baskets.list.filter(function (x) { return x.k === k; })[0] : null;
    if (!b) return '';
    var lab = function (t) { return D.tracks && D.tracks[t] ? D.tracks[t].label : t; };
    if (b.mix.length === 1) return 'כל ההלוואה ב' + lab(b.mix[0][0]);
    return b.mix.map(function (x) { var f = x[1], w = Math.abs(f - 0.5) < 0.01 ? 'חצי' : Math.abs(f - 1 / 3) < 0.01 ? 'שליש' : Math.round(100 * f) + '%'; return w + ' ' + lab(x[0]); }).join(' · ');
  }

  /* The negotiation text: first person singular, polite, facts only. Only typed numbers and official averages appear in it. */
  function letter(ctx) {
    var O = ctx.offers, N = ctx.names, t = ctx.target, o = O[t];
    if (!o) return '';
    var L = [];
    L.push('שלום רב,');
    L.push('קיבלתי מכם אישור עקרוני למשכנתא' + (fin(o.loan) ? ' של ' + ils(o.loan) : '') + (fin(o.years) ? ' ל־' + yrs(o.years) : '') + '.');
    var others = O.map(function (x, i) { return i; }).filter(function (i) { return i !== t && hasAny(O[i]); });
    if (others.length) {
      var same = others.every(function (i) { return Math.abs(O[i].loan - o.loan) < 0.5 && Math.abs(O[i].years - o.years) < 0.01; });
      L.push(same ? 'קיבלתי גם ' + (others.length > 1 ? 'אישורים עקרוניים מ' + others.map(function (i) { return N[i]; }).join(' ומ') : 'אישור עקרוני מ' + N[others[0]]) + ' על אותו סכום ולאותה תקופה.'
        : 'קיבלתי גם ' + others.map(function (i) { return 'אישור עקרוני מ' + N[i] + (fin(O[i].loan) ? ' על ' + ils(O[i].loan) : '') + (fin(O[i].years) ? ' ל־' + yrs(O[i].years) : ''); }).join(', ו') + '.');
    }
    BASKETS.forEach(function (k, j) {
      var c = ctx.cmp[k];
      if (!c || c.cheapest.length === 0 || c.cheapest.indexOf(t) > -1 || c.have.indexOf(t) === -1) return;
      var ci = c.cheapest[0], me = o.b[k], th = O[ci].b[k], parts = [];
      var diffAmt = !(Math.abs(O[ci].loan - o.loan) < 0.5);
      if (c.by === 'total') {
        parts.push('סך התשלומים הצפוי ' + ils(th.total) + (diffAmt ? ' על ' + ils(O[ci].loan) : '') + ' מול ' + ils(me.total) + (diffAmt ? ' על ' + ils(o.loan) : '') + ' אצלכם');
        if (fin(th.maxPay) && fin(me.maxPay)) parts.push('ההחזר החודשי הגבוה הצפוי ' + ils(th.maxPay) + ' מול ' + ils(me.maxPay));
        if (fin(th.irr) && fin(me.irr)) parts.push('הריבית הכוללת החזויה ' + pct(th.irr) + ' מול ' + pct(me.irr));
      } else {
        parts.push('הריבית הכוללת החזויה ' + pct(th.irr) + (fin(O[ci].years) ? ' ל־' + yrs(O[ci].years) : '') + ' מול ' + pct(me.irr) + (fin(o.years) ? ' ל־' + yrs(o.years) : '') + ' אצלכם');
      }
      L.push('בסל האחיד ' + (j + 1) + ' ההצעה של ' + N[ci] + ' נמוכה יותר: ' + parts.join(', ו') + '.');
    });
    var ref = ctx.refs[t], sys = ctx.sysRef, fk = ctx.focus, fj = BASKETS.indexOf(fk) + 1, fIrr = o.b[fk] ? o.b[fk].irr : NaN;
    if (ref) {
      L.push('לפי נתוני בנק ישראל, הריבית הכוללת החזויה הממוצעת במשכנתאות החדשות אצלכם ב' + monthHe(ref.month) + ' הייתה ' + pct(ref.irr) + '.'
        + (fin(fIrr) ? ' בהצעה שלכם, בסל האחיד ' + fj + ', היא ' + pct(fIrr) + '.' : '')
        + (ref.min && ref.min.k !== ref.key ? ' באותו חודש הממוצע הנמוך בין חמשת הבנקים הגדולים, ' + pct(ref.min.irr) + ', היה של ' + ref.min.name + '.' : ''));
    } else if (sys) {
      L.push('לפי נתוני בנק ישראל, הריבית הכוללת החזויה הממוצעת בכל המשכנתאות החדשות ב' + monthHe(sys.month) + ' הייתה ' + pct(sys.irr) + '.'
        + (fin(fIrr) ? ' בהצעה שלכם, בסל האחיד ' + fj + ', היא ' + pct(fIrr) + '.' : ''));
    }
    L.push('אשמח לקבל מכם הצעה מעודכנת.');
    L.push('תודה,');
    return L.join('\n');
  }

  /* The table as plain text, for "copy the result" and for the advisor */
  function tableText(ctx) {
    var O = ctx.offers, N = ctx.names, norm = ctx.norm, out = [];
    out.push('השוואת אישורים עקרוניים למשכנתא: שלושת הסלים האחידים');
    var live = O.map(function (o, i) { return i; }).filter(function (i) { return hasAny(O[i]); });
    if (norm.loansEqual && norm.termsEqual && live.length) out.push('הלוואה של ' + ils(O[live[0]].loan) + ' ל־' + yrs(O[live[0]].years) + ', בכל ההצעות');
    else live.forEach(function (i) { out.push(N[i] + ': ' + (fin(O[i].loan) ? ils(O[i].loan) : '') + (fin(O[i].years) ? ' ל־' + yrs(O[i].years) : '')); });
    if (!norm.loansEqual && fin(norm.base)) out.push('הסכומים שונים: סך התשלומים וההחזרים מותאמים להלוואה של ' + ils(norm.base));
    BASKETS.forEach(function (k, j) {
      var c = ctx.cmp[k];
      out.push('');
      out.push('סל אחיד ' + (j + 1) + (ctx.D ? ': ' + basketText(ctx.D, k) : ''));
      live.forEach(function (i) {
        var x = norm.rows[i].b[k], p = [];
        if (fin(x.irr)) p.push(MLAB.irr + ' ' + pct(x.irr));
        if (fin(x.nTotal)) p.push(MLAB.total + ' ' + ils(x.nTotal));
        if (fin(x.nMax)) p.push(MLAB.maxPay + ' ' + ils(x.nMax));
        if (fin(x.nFirst)) p.push(MLAB.first + ' ' + ils(x.nFirst));
        if (p.length) out.push(N[i] + ': ' + p.join(' · ') + (c.cheapest.indexOf(i) > -1 && c.cheapest.length < c.have.length ? ' (הזולה)' : ''));
      });
      if (c.dearest != null) out.push('הפער: ' + (c.by === 'total' ? ils(c.gapTotal) + ' לאורך ההלוואה' + (fin(c.gapMax) ? ', ' + ils(c.gapMax) + ' בהחזר החודשי הגבוה' : '') : pct(c.gapIrr) + ' בריבית הכוללת החזויה'));
    });
    var refs = [];
    O.forEach(function (o, i) { var r = ctx.refs[i]; if (r && refs.indexOf(r.name + ' ' + pct(r.irr)) === -1) refs.push(r.name + ' ' + pct(r.irr)); });
    if (ctx.sysRef) {
      out.push('');
      out.push('ריבית כוללת חזויה ממוצעת לפי בנק ישראל, ' + monthHe(ctx.sysRef.month) + ': ' + refs.concat(['כל הבנקים ' + pct(ctx.sysRef.irr)]).join(', ') + '. ממוצע של בנק תלוי בתמהיל ובלקוחות שלו, ואינו הצעה.');
    }
    return out.join('\n');
  }

  /* The example the tool opens with (marked "דוגמה"): two approvals for 1,200,000 ₪ over 25 years, Spitzer, the linked third of
     basket 2 at the Bank of Israel 2.0% inflation forecast; bank A slightly dearer than bank B. */
  function example() {
    var e = function (a, b, c, d) { return { irr: a, total: b, maxPay: c, first: d }; };
    return { offers: [
      { bank: '', loan: 1200000, years: 25, b: { b1: e(4.96, 2073183, 6911, 6911), b2: e(5.01, 2120212, 7748, 6489), b3: e(4.75, 2031988, 6773, 6773) },
        mix: [{ track: 'fixed_nl', share: 40, rate: 4.85, years: 25 }, { track: 'prime', share: 33, rate: 4.45, years: 25 }, { track: 'var_nl_other', share: 27, rate: 4.7, years: 25 }] },
      { bank: '', loan: 1200000, years: 25, b: { b1: e(4.8, 2042083, 6807, 6807), b2: e(4.84, 2084000, 7617, 6378), b3: e(4.57, 1996170, 6654, 6654) }, mix: [] }
    ], focus: 'b2', tab: 0, target: null };
  }
  function blankOffer(prev) {
    var b = {}; BASKETS.forEach(function (k) { b[k] = { irr: null, total: null, maxPay: null, first: null }; });
    return { bank: '', loan: prev ? prev.loan : null, years: prev ? prev.years : null, b: b, mix: [] };
  }

  window.NLMO = { BASKETS: BASKETS, METRICS: METRICS, BIG5: BIG5, BANK_HE: BANK_HE, TRACK_HE: TRACK_HE, MLAB: MLAB, num: num, grp: grp, ils: ils, pct: pct, yrs: yrs, monthHe: monthHe,
    ef2nom: ef2nom, pmt: pmt, names: names, check: check, clean: clean, hasAny: hasAny, normalize: normalize, compare: compare, bankRef: bankRef, place: place, trackCmp: trackCmp,
    basketText: basketText, letter: letter, tableText: tableText, example: example, blankOffer: blankOffer };
  if (!window.NadLanInstruments || !window.document) return;

  /* ================================================================================================================ the page */
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  var nf0 = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function uils(n) { return F.ils(n); }
  function upct(n, d) { return F.num(n, d == null ? 2 : d) + '%'; }
  function sgn(n, f) { return (n > 0 ? '+' : n < 0 ? '−' : '') + f(Math.abs(n)); }
  function mon(k) { return F.month(k); }
  function fig(s) { return '<bdi class="m" dir="ltr">' + esc(s) + '</bdi>'; }  // a figure inside a Hebrew sentence
  var ADVISOR = 'https://nad-lan.co.il/mortgage-advisor/';
  var ICON = {
    copy: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 7h9v10H7z"/><path d="M4 13V3h9"/></svg>',
    print: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 8V3h10v5"/><path d="M5 14H3V8h14v6h-2"/><path d="M6 12h8v5H6z"/></svg>',
    link: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M8 12l4-4"/><path d="M9 5l2-2a3 3 0 0 1 4 4l-2 2"/><path d="M11 15l-2 2a3 3 0 0 1-4-4l2-2"/></svg>'
  };

  function css() {
    if (document.getElementById('nlo-css')) return;
    var s = document.createElement('style'); s.id = 'nlo-css';
    s.textContent = [
      '.nlo .nlo__sec{margin:28px 0 0;padding:20px 0 0;border-top:1px solid var(--nli-line);position:relative}',
      'html body .nli .nlo h3.nlo__h{font:600 22px/28px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 6px !important;letter-spacing:0;text-transform:none}',
      'html body .nli .nlo h4.nlo__h4{font:600 15px/22px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 !important;letter-spacing:0;text-transform:none}',
      '.nlo__p{font:400 15px/24px var(--nli-sans);color:var(--nli-ink2);margin:0 0 12px;max-width:72ch}',
      '.nlo__fx{font:400 12px/19px "IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace;color:var(--nli-mute);margin:10px 0 0;max-width:96ch;overflow-wrap:anywhere}',
      '.nlo__fx a{color:var(--nli-sea) !important}',
      '.nlo__grid{display:grid;grid-template-columns:minmax(0,1fr);gap:20px;position:relative}',
      '@media (min-width:1000px){.nlo__grid{grid-template-columns:minmax(0,440px) minmax(0,1fr);gap:32px}}',
      '.nlo__bk{list-style:none;margin:0 0 16px;padding:0;display:grid;gap:4px;position:relative}',
      '.nlo__bk li{font:400 14px/21px var(--nli-sans);color:var(--nli-ink2);margin:0;padding:0}.nlo__bk li b{font-weight:600;color:var(--nli-ink)}',
      '.nlo__tabs{display:flex;flex-wrap:wrap;gap:6px}',
      'html body .nli .nlo__tabs button{min-height:44px;padding:10px 14px;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);color:var(--nli-ink2);font:500 15px/20px var(--nli-sans);cursor:pointer;margin:0;text-transform:none;letter-spacing:0;box-shadow:none}',
      'html body .nli .nlo__tabs button[aria-selected="true"]{background:var(--nli-sea);border-color:var(--nli-sea);color:var(--nli-on-sea)}',
      'html body .nli .nlo__tabs button.nlo__add{border:1px dashed var(--nli-sea);color:var(--nli-sea);background:none}',
      '.nlo__pane{display:grid;gap:14px;padding:14px 0 0;min-width:0}',
      '.nlo__two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px;align-items:end}',
      'html body .nli fieldset.nlo__fs{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);padding:8px 12px 12px;margin:0;min-width:0;background:var(--nli-surface);display:grid;gap:8px}',
      'html body .nli fieldset.nlo__fs legend{font:600 15px/22px var(--nli-sans);color:var(--nli-ink);padding:0 6px;margin:0}',
      '.nlo__mx{display:block;font:400 12px/17px var(--nli-sans);color:var(--nli-mute);margin:0}',
      '.nlo .nli__f{gap:4px}',
      'html body .nli .nlo .nli__f>label{font:500 12px/16px var(--nli-sans) !important;color:var(--nli-ink2) !important;margin:0}',
      'html body .nli .nlo .nli__in{min-height:46px}html body .nli .nlo .nli__in input,html body .nli .nlo .nli__in select{min-height:44px}',
      'html body .nli .nlo .nli__in input{font-size:16px;padding:9px 10px}',
      'html body .nli .nlo .nli__in select{font-size:16px;padding:9px 10px}',
      '.nlo .nli__unit{padding:0 10px;font-size:13px}',
      'html body .nli .nlo details.nlo__more{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);padding:0 12px;background:var(--nli-ground)}',
      'html body .nli .nlo details.nlo__more>summary{font:500 15px/22px var(--nli-sans);color:var(--nli-sea);cursor:pointer;min-height:44px;display:flex;align-items:center;border:0 !important;padding:0 !important;background:none !important}',
      '.nlo__mixb{display:grid;gap:10px;padding:0 0 12px}',
      '.nlo__hint{font:400 13px/19px var(--nli-sans);color:var(--nli-mute);margin:0}',
      '.nlo__mr{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) 44px;gap:8px;align-items:end;padding:10px 0 0;border-top:1px solid var(--nli-line)}',
      '.nlo__mr>.nli__f:first-child{grid-column:1/-1}',
      'html body .nli .nlo button.nlo__del{min-height:44px;min-width:44px;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);color:var(--nli-ink2);cursor:pointer;font:400 18px/1 var(--nli-sans);margin:0;padding:0}',
      'html body .nli .nlo button.nlo__plus{justify-self:start;min-height:44px;padding:8px 14px;border:1px dashed var(--nli-sea);border-radius:var(--nli-r-s);background:none;color:var(--nli-sea);font:500 14px/20px var(--nli-sans);cursor:pointer;margin:0}',
      'html body .nli .nlo button.nlo__rm{justify-self:start;min-height:44px;padding:8px 14px;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);color:var(--nli-ink2);font:500 14px/20px var(--nli-sans);cursor:pointer;margin:0}',
      'html body .nli .nlo .nli__fig.nlo__dec{text-decoration:underline;text-decoration-color:var(--nli-survey);text-decoration-thickness:2px;text-underline-offset:8px;margin:6px 0 12px}',
      '.nlo__egc{display:inline-block;font:500 12px/18px var(--nli-sans);color:var(--nli-ink);border:1px solid var(--nli-line);border-radius:999px;padding:0 8px;margin-inline-start:6px;background:var(--nli-surface)}',
      'html body .nli .nlo .nli__lines dd{white-space:normal;max-width:62%;overflow-wrap:anywhere;font:500 14px/20px var(--nli-sans);direction:rtl;unicode-bidi:normal;text-align:left}',
      'html body .nli .nlo bdi.m{font-family:var(--nli-mono);font-variant-numeric:tabular-nums;white-space:nowrap;direction:ltr;unicode-bidi:isolate}',
      'html body .nli .nlo .nli__lines dt{min-width:0}',
      '.nlo__wide{display:none}',
      '@media (min-width:720px){.nlo .nlo__wide{display:block}.nlo .nlo__cards{display:none}}',
      '.nlo__tw{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);overflow:hidden}',
      'html body .nli .nlo table.nlo__t{width:100%;border-collapse:collapse;margin:0;display:table !important;font:400 13px/19px var(--nli-sans)}',
      'html body .nli .nlo table.nlo__t thead{display:table-header-group !important}html body .nli .nlo table.nlo__t tbody{display:table-row-group !important}html body .nli .nlo table.nlo__t tr{display:table-row !important}',
      'html body .nli .nlo table.nlo__t th,html body .nli .nlo table.nlo__t td{display:table-cell !important;padding:7px 8px !important;border:0 !important;border-bottom:1px solid var(--nli-line) !important;text-align:right;vertical-align:middle;background:none !important;color:var(--nli-ink);font-size:13px !important;line-height:19px !important;width:auto !important;font-family:var(--nli-sans) !important}',
      'html body .nli .nlo table.nlo__t thead th{font-weight:500;color:var(--nli-mute);font-size:12px !important;white-space:normal}',
      'html body .nli .nlo table.nlo__t th[scope="row"]{font-weight:400;color:var(--nli-ink2)}',
      'html body .nli .nlo table.nlo__t td.n{font-family:var(--nli-mono) !important;direction:ltr;unicode-bidi:plaintext;text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}',
      'html body .nli .nlo table.nlo__t td.is-best{background:#EDF5EF !important;font-weight:600}',
      'html body .nli .nlo table.nlo__t tr.nlo__bh th{background:var(--nli-ground) !important;font-weight:600;color:var(--nli-ink);font-size:14px !important;padding-top:10px !important}',
      'html body .nli .nlo table.nlo__t tr.nlo__bh.is-focus th{box-shadow:inset -3px 0 0 var(--nli-sea)}',
      'html body .nli .nlo table.nlo__t td small{display:block;font:400 11px/15px var(--nli-sans);color:var(--nli-mute);direction:rtl;text-align:right;white-space:normal}',
      '.nlo__tag{display:inline-flex;align-items:center;gap:6px;font:500 12px/18px var(--nli-sans);color:var(--nli-ink);margin-inline-start:8px;white-space:nowrap}',
      '.nlo__tag::before{content:"";width:10px;height:10px;border-radius:2px;background:var(--nli-open)}',
      '.nlo__cards{display:grid;gap:10px}',
      '.nlo__card{border:1px solid var(--nli-line);border-radius:var(--nli-r-m);background:var(--nli-surface);padding:12px;display:grid;gap:10px;min-width:0}',
      '.nlo__bank{display:grid;gap:8px;padding:10px 0 0;border-top:1px solid var(--nli-line)}',
      '.nlo__bank.is-best{border-inline-start:4px solid var(--nli-open);padding:10px 10px 8px;background:#F3F8F4}',
      '.nlo__bn{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;font:600 15px/20px var(--nli-sans);color:var(--nli-ink)}',
      '.nlo__kv{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px 12px;margin:0}',
      '.nlo__kv div{min-width:0;margin:0}.nlo__kv dt{font:400 12px/16px var(--nli-sans);color:var(--nli-mute);margin:0}',
      '.nlo__kv dd{font:500 16px/22px var(--nli-mono);color:var(--nli-ink);margin:0;direction:ltr;unicode-bidi:plaintext;text-align:right;font-variant-numeric:tabular-nums}',
      '.nlo__gap{font:500 14px/21px var(--nli-sans);color:var(--nli-ink);margin:0;padding:10px 0 0;border-top:1px solid var(--nli-line)}',
      '.nlo__gap bdi,.nlo__pc bdi,.nlo__answer bdi{font-family:var(--nli-mono);font-variant-numeric:tabular-nums}',
      '.nlo__avg{display:grid;gap:12px}@media (min-width:860px){.nlo__avg{grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}}',
      '.nlo__pc{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);padding:12px;background:var(--nli-surface);min-width:0;display:grid;gap:8px;align-content:start}',
      '.nlo__pc p{font:400 14px/21px var(--nli-sans);color:var(--nli-ink2);margin:0}.nlo__pc p b{font-weight:600;color:var(--nli-ink)}',
      '.nlo__trk{border-top:1px solid var(--nli-line);padding:8px 0 0;display:grid;gap:6px}',
      'html body .nli .nlo p.nlo__tn{font:600 14px/20px var(--nli-sans);color:var(--nli-ink);margin:0}.nlo__tn small{display:block;font:400 12px/16px var(--nli-sans);color:var(--nli-mute)}',
      '.nlo__k3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:0}.nlo__k3 div{min-width:0;margin:0}',
      '.nlo__k3 dt{font:400 12px/16px var(--nli-sans);color:var(--nli-mute);margin:0}.nlo__k3 dd{font:500 15px/21px var(--nli-mono);color:var(--nli-ink);margin:0;direction:ltr;unicode-bidi:plaintext;text-align:right;font-variant-numeric:tabular-nums}',
      '.nlo__k3 small{display:block;font:400 11px/15px var(--nli-sans);color:var(--nli-mute)}',
      '.nlo__lad{display:grid;gap:2px;margin:8px 0 0;max-width:720px}',
      '.nlo__lr{display:grid;grid-template-columns:minmax(0,10em) minmax(0,1fr) 4.4em;gap:10px;align-items:center;min-height:34px;padding:0 6px;border-radius:var(--nli-r-s)}',
      '.nlo__lr .l{font:400 13px/17px var(--nli-sans);color:var(--nli-ink2);min-width:0}',
      '.nlo__lr .t{position:relative;height:20px;direction:ltr;background:linear-gradient(var(--nli-line),var(--nli-line)) 0 50%/100% 1px no-repeat}',
      '.nlo__lr .t i{position:absolute;top:5px;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:var(--nli-mute)}',
      '.nlo__lr.is-sys .l{font-weight:600;color:var(--nli-ink)}.nlo__lr.is-sys .t i{background:var(--nli-ink);border-radius:2px}',
      '.nlo__lr.is-offer{background:#EEF4F6}.nlo__lr.is-offer .l{font-weight:600;color:var(--nli-ink)}.nlo__lr.is-offer .t i{background:var(--nli-sea);width:14px;height:14px;top:3px;margin-left:-7px}',
      '.nlo__lr .v{font:500 13px/17px var(--nli-mono);color:var(--nli-ink);direction:ltr;text-align:left;font-variant-numeric:tabular-nums}',
      '@media (max-width:599px){.nlo__lr{grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"l v" "t t";gap:0 10px;padding:4px 6px}.nlo__lr .l{grid-area:l}.nlo__lr .v{grid-area:v}.nlo__lr .t{grid-area:t}}',
      'html body .nli .nlo .nlo__pc table.nlo__t td,html body .nli .nlo .nlo__pc table.nlo__t th{padding:6px 6px !important}',
      '.nlo__lt{display:grid;gap:10px}html body .nli .nlo .nlo__lt pre.nli__doc{max-width:760px}',
      'html body .nli .nlo button.nlo__copy{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:10px 16px;border-radius:999px;border:1px solid var(--nli-sea);background:var(--nli-sea);color:var(--nli-on-sea) !important;font:500 14px/20px var(--nli-sans);cursor:pointer;margin:0;justify-self:start}',
      '.nlo__copy svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:1.5;stroke-linecap:square}',
      '.nlo__adv{display:grid;gap:10px;justify-items:start}',
      'html body .nli .nlo a.nlo__go{display:flex;align-items:center;justify-content:center;min-height:48px;padding:10px 20px;border-radius:var(--nli-r-s);background:var(--nli-sea);color:var(--nli-on-sea) !important;font:600 16px/22px var(--nli-sans);text-decoration:none !important;width:100%;max-width:420px;text-align:center}',
      'html body .nli .nlo a.nlo__go:hover{background:var(--nli-sea-deep)}',
      '@media print{.nlo__tabs,.nlo__pane,.nlo__lt button,.nlo__adv,.nli__seg{display:none !important}.nlo__wide{display:block !important}.nlo__cards{display:none !important}}'
    ].join('\n');
    document.head.appendChild(s);
  }

  NI.register('moffers', {
    custom: function (root, data) {
      css();
      var D = data.boim || data.d0;
      if (!D || !D.by_bank || !D.by_bank.latest || !D.baskets) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
      var BB = D.by_bank, LT = BB.latest, MONTH = LT.month;
      var BANKS = BB.banks.filter(function (b) { return b.k !== 'system'; }).map(function (b) { return b.k; });
      var uid = 'nlo' + Math.random().toString(36).slice(2, 7);
      var v = example(), isEg = true, last = null, errs = {};
      var SYS = bankRef(D, 'system');

      /* a shared link reopens the same numbers */
      function shareState() {
        var s = { o: v.offers.map(function (o) { return [o.bank, o.loan, o.years, BASKETS.map(function (k) { return METRICS.map(function (m) { var x = o.b[k][m]; return fin(x) ? x : null; }); }), (o.mix || []).map(function (m) { return [m.track, m.share, m.rate, m.years]; })]; }), f: v.focus, t: v.target };
        var j = JSON.stringify(s), b = btoa(unescape(encodeURIComponent(j))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
        return (location.origin && location.origin !== 'null' ? location.origin + location.pathname : location.href.split('#')[0]) + '#moffers=' + b;
      }
      function loadState(h) {
        try {
          var b = h.replace(/-/g, '+').replace(/_/g, '/'); while (b.length % 4) b += '=';
          var s = JSON.parse(decodeURIComponent(escape(atob(b))));
          if (!s.o || s.o.length < 1) return false;
          v = { offers: s.o.slice(0, 3).map(function (x) {
            var o = blankOffer(); o.bank = BANKS.indexOf(x[0]) > -1 || x[0] === 'other' ? x[0] : ''; o.loan = x[1]; o.years = x[2];
            BASKETS.forEach(function (k, j) { METRICS.forEach(function (m, q) { o.b[k][m] = x[3] && x[3][j] ? x[3][j][q] : null; }); });
            o.mix = (x[4] || []).slice(0, 6).map(function (m) { return { track: TRACK_KEYS.indexOf(m[0]) > -1 ? m[0] : 'fixed_nl', share: m[1], rate: m[2], years: m[3] }; });
            return o; }), focus: BASKETS.indexOf(s.f) > -1 ? s.f : 'b2', tab: 0, target: s.t != null && s.t < s.o.length ? s.t : null };
          while (v.offers.length < 2) v.offers.push(blankOffer(v.offers[0]));
          isEg = false; return true;
        } catch (e) { return false; }
      }
      var hm = /#moffers=([A-Za-z0-9_\-]+)/.exec(location.hash || '');
      if (hm) loadState(hm[1]);

      /* ------------------------------------------------------------------------------------------------------ the surface */
      root.innerHTML = '';
      if (!root.parentNode || !root.parentNode.closest || !root.parentNode.closest('.nli')) root.classList.add('nli');
      root.setAttribute('dir', 'rtl');
      var panel = el('div', 'nli__panel nlo');
      panel.appendChild(el('p', 'nli__kicker', 'מחשבון · השוואת הצעות משכנתא'));
      panel.appendChild(el('h2', 'nli__title', 'שלוש הצעות, טבלה אחת'));
      panel.appendChild(el('p', 'nli__lede', 'כל אישור עקרוני למשכנתא מציג שלושה סלים אחידים שבנק ישראל קבע, עם אותם מסלולים בכל הבנקים. מקלידים את המספרים של כל סל משתי הצעות או משלוש, ומקבלים טבלה אחת: ההצעה הזולה בכל סל, הפער בשקלים, הממוצע שבנק ישראל פרסם לכל בנק ונוסח מוכן לשיחה עם הבנק.'));
      var strip = el('div', 'nli__strip');
      [['ריבית כוללת חזויה, כל הבנקים, ' + mon(MONTH), upct(SYS.irr)], ['הנמוכה בחמשת הגדולים: ' + SYS.min.name, upct(SYS.min.irr)], ['הגבוהה בחמשת הגדולים: ' + SYS.max.name, upct(SYS.max.irr)]]
        .forEach(function (x) { strip.appendChild(el('div', '', '<span>' + esc(x[0]) + '</span><strong>' + esc(x[1]) + '</strong>')); });
      panel.appendChild(strip);
      var bk = el('ul', 'nlo__bk');
      BASKETS.forEach(function (k, j) { bk.appendChild(el('li', '', '<b>סל אחיד ' + (j + 1) + ':</b> ' + esc(basketText(D, k)))); });
      panel.appendChild(bk);

      var grid = el('div', 'nlo__grid'), form = el('form', 'nli__form nlo__form'), out = el('div', 'nli__out nlo__out');
      form.addEventListener('submit', function (e) { e.preventDefault(); });
      grid.appendChild(form); grid.appendChild(out); panel.appendChild(grid);
      out.appendChild(el('span', 'nli__alab', 'הסל להשוואה'));
      var seg = el('div', 'nli__seg'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', 'הסל להשוואה');
      BASKETS.forEach(function (k, j) { var b = el('button', '', 'סל ' + (j + 1)); b.type = 'button'; b.setAttribute('data-k', k);
        b.addEventListener('click', function () { v.focus = k; markSeg(); paint(); }); seg.appendChild(b); });
      out.appendChild(seg);
      function markSeg() { [].forEach.call(seg.children, function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-k') === v.focus)); }); }
      var ans = el('div', 'nli__answer nlo__answer'); out.appendChild(ans);
      var tbl = el('div', 'nlo__tbl'); out.appendChild(tbl);
      var avgSec = el('section', 'nlo__sec'); panel.appendChild(avgSec);
      var letSec = el('section', 'nlo__sec'); panel.appendChild(letSec);
      var advSec = el('section', 'nlo__sec nlo__adv'); panel.appendChild(advSec);
      var formula = el('p', 'nli__formula'), src = el('p', 'nli__src'); panel.appendChild(formula); panel.appendChild(src);
      var share = el('div', 'nli__share'); panel.appendChild(share);
      var egNote = el('p', 'nli__eg'); panel.appendChild(egNote);
      root.appendChild(panel);

      var t = 0; function changed() { clearTimeout(t); t = setTimeout(paint, 90); }

      /* ------------------------------------------------------------------------------------------------------- the form */
      function inputField(label, type, unit, get, set, key) {
        var w = el('div', 'nli__f'), id = uid + '-' + v.tab + '-' + key;
        var lab = el('label', '', esc(label)); lab.htmlFor = id; w.appendChild(lab);
        var box = el('div', 'nli__in'), inp = el('input'); inp.type = 'text'; inp.inputMode = 'decimal'; inp.id = id; inp.autocomplete = 'off';
        var show = function () { var x = get(); inp.value = !fin(x) ? '' : type === 'money' ? nf0.format(x) : String(x); };
        show();
        inp.addEventListener('input', function () { var n = num(inp.value); set(fin(n) ? n : null); isEg = false; changed(); });
        inp.addEventListener('blur', function () { if (type === 'money' && fin(get())) show(); });
        box.appendChild(inp); if (unit) box.appendChild(el('span', 'nli__unit', esc(unit)));
        w.appendChild(box);
        var er = el('span', 'nli__err'); er.setAttribute('aria-live', 'polite'); w.appendChild(er); errs[key] = er;
        return w;
      }
      function selectField(label, opts, val, onPick, key) {
        var w = el('div', 'nli__f'), id = uid + '-' + v.tab + '-' + key;
        var lab = el('label', '', esc(label)); lab.htmlFor = id; w.appendChild(lab);
        var box = el('div', 'nli__in'), s = el('select'); s.id = id;
        opts.forEach(function (o) { var op = el('option', '', esc(o[1])); op.value = o[0]; if (o[0] === val) op.selected = true; s.appendChild(op); });
        s.addEventListener('change', function () { onPick(s.value); });
        box.appendChild(s); w.appendChild(box);
        return w;
      }
      var tabsBox = null;
      function refreshTabs() { if (!tabsBox) return; var nm = names(v.offers); [].forEach.call(tabsBox.querySelectorAll('[role="tab"]'), function (b, i) { b.textContent = nm[i]; }); }
      function buildForm() {
        form.innerHTML = ''; errs = {};
        if (v.tab >= v.offers.length) v.tab = 0;
        tabsBox = el('div', 'nlo__tabs'); tabsBox.setAttribute('role', 'tablist'); tabsBox.setAttribute('aria-label', 'האישורים שקיבלתם');
        var nm = names(v.offers);
        v.offers.forEach(function (o, i) {
          var b = el('button', '', esc(nm[i])); b.type = 'button'; b.setAttribute('role', 'tab'); b.id = uid + '-tab-' + i;
          b.setAttribute('aria-selected', String(i === v.tab)); b.setAttribute('aria-controls', uid + '-pane'); b.tabIndex = i === v.tab ? 0 : -1;
          b.addEventListener('click', function () { v.tab = i; buildForm(); paint(); var f = document.getElementById(uid + '-tab-' + i); if (f) f.focus(); });
          b.addEventListener('keydown', function (e) { var d = e.key === 'ArrowLeft' ? 1 : e.key === 'ArrowRight' ? -1 : 0; if (!d) return; e.preventDefault(); v.tab = (i + d + v.offers.length) % v.offers.length; buildForm(); paint(); var f = document.getElementById(uid + '-tab-' + v.tab); if (f) f.focus(); });
          tabsBox.appendChild(b);
        });
        if (v.offers.length < 3) {
          var add = el('button', 'nlo__add', '+ הצעה שלישית'); add.type = 'button';
          add.addEventListener('click', function () { v.offers.push(blankOffer(v.offers[0])); v.tab = v.offers.length - 1; buildForm(); paint(); });
          tabsBox.appendChild(add);
        }
        form.appendChild(tabsBox);
        var o = v.offers[v.tab];
        var pane = el('div', 'nlo__pane'); pane.id = uid + '-pane'; pane.setAttribute('role', 'tabpanel'); pane.setAttribute('aria-labelledby', uid + '-tab-' + v.tab);
        pane.appendChild(selectField('הבנק שנתן את האישור', [['', 'בחרו בנק']].concat(BANKS.map(function (k) { return [k, BANK_HE[k] || k]; })).concat([['other', 'בנק אחר']]), o.bank,
          function (val) { o.bank = val; refreshTabs(); paint(); }, 'bank'));  // the numbers are still the example's until one is typed
        var two = el('div', 'nlo__two');
        two.appendChild(inputField('סכום ההלוואה באישור', 'money', '₪', function () { return o.loan; }, function (x) { o.loan = x; }, 'loan'));
        two.appendChild(inputField('תקופה', 'number', 'שנים', function () { return o.years; }, function (x) { o.years = x; }, 'years'));
        pane.appendChild(two);
        BASKETS.forEach(function (k, j) {
          var fs = el('fieldset', 'nlo__fs'); fs.appendChild(el('legend', '', 'סל אחיד ' + (j + 1)));
          fs.appendChild(el('p', 'nlo__mx', esc(basketText(D, k))));
          var g = el('div', 'nlo__two');
          METRICS.forEach(function (m) {
            g.appendChild(inputField(MLAB[m], m === 'irr' ? 'percent' : 'money', m === 'irr' ? '%' : '₪', function () { return o.b[k][m]; }, function (x) { o.b[k][m] = x; }, k + '-' + m));
          });
          fs.appendChild(g); pane.appendChild(fs);
        });
        pane.appendChild(mixBox(o));
        if (v.offers.length > 2) {
          var rm = el('button', 'nlo__rm', 'הסרת ההצעה הזאת'); rm.type = 'button';
          rm.addEventListener('click', function () { v.offers.splice(v.tab, 1); v.tab = 0; if (v.target != null && v.target >= v.offers.length) v.target = null; buildForm(); paint(); });
          pane.appendChild(rm);
        }
        form.appendChild(pane);
      }
      function mixBox(o) {
        var d = el('details', 'nlo__more'); d.open = !!(o.mix && o.mix.length);
        d.appendChild(el('summary', '', 'התמהיל שהבנק הציע (לא חובה)'));
        var b = el('div', 'nlo__mixb'); d.appendChild(b);
        b.appendChild(el('p', 'nlo__hint', 'המסלולים מההצעה, החלק של כל מסלול, הריבית והתקופה. נשווה כל מסלול לממוצע של אותו בנק באותו מסלול.'));
        var rows = el('div', ''); b.appendChild(rows);
        function draw() {
          rows.innerHTML = '';
          o.mix.forEach(function (m, i) {
            var r = el('div', 'nlo__mr'), key = 'mx' + i;
            r.appendChild(selectField('מסלול ' + (i + 1), TRACK_KEYS.map(function (k) { return [k, TRACK_HE[k]]; }), m.track, function (val) { m.track = val; isEg = false; changed(); }, key + '-t'));
            r.appendChild(inputField('חלק (%)', 'percent', '', function () { return m.share; }, function (x) { m.share = x; }, key + '-s'));
            r.appendChild(inputField('ריבית (%)', 'percent', '', function () { return m.rate; }, function (x) { m.rate = x; }, key + '-r'));
            r.appendChild(inputField('שנים', 'number', '', function () { return m.years; }, function (x) { m.years = x; }, key + '-y'));
            var del = el('button', 'nlo__del', '×'); del.type = 'button'; del.setAttribute('aria-label', 'הסרת מסלול ' + (i + 1));
            del.addEventListener('click', function () { o.mix.splice(i, 1); isEg = false; draw(); paint(); });
            r.appendChild(del); rows.appendChild(r);
          });
        }
        draw();
        var add = el('button', 'nlo__plus', '+ מסלול'); add.type = 'button';
        add.addEventListener('click', function () { if (o.mix.length >= 6) return; o.mix.push({ track: 'fixed_nl', share: null, rate: null, years: fin(o.years) ? o.years : null }); isEg = false; draw(); paint(); });
        b.appendChild(add);
        b.appendChild(el('p', 'nlo__hint', 'בפריים מקלידים את הריבית עצמה: פריים של ' + upct(D.policy.prime) + ' פחות 0.4 הם ' + upct(D.policy.prime - 0.4) + '.'));
        return d;
      }

      /* ------------------------------------------------------------------------------------------------------ the result */
      function compute() {
        var cl = clean(v.offers), norm = normalize(cl.offers), cmp = compare(norm), nm = names(v.offers);
        var refs = v.offers.map(function (o) { return o.bank && o.bank !== 'other' ? bankRef(D, o.bank) : null; });
        var auto = cmp[v.focus].dearest != null ? cmp[v.focus].dearest : 0, target = v.target != null && v.target < v.offers.length ? v.target : auto;
        return { cl: cl, offers: cl.offers, norm: norm, cmp: cmp, names: nm, refs: refs, sysRef: SYS, focus: v.focus, target: target, D: D };
      }
      function paint() {
        var R = compute(); last = R;
        markSeg(); paintErrors(R); paintAnswer(R); paintTable(R); paintAvg(R); paintLetter(R);
      }
      function paintErrors(R) {
        Object.keys(errs).forEach(function (k) { errs[k].textContent = ''; });
        (R.cl.issues[v.tab] || []).forEach(function (x) { var k = x.b ? x.b + '-' + x.f : x.f; if (errs[k]) errs[k].textContent = x.msg; });
      }
      function bj(k) { return BASKETS.indexOf(k) + 1; }
      function paintAnswer(R) {
        var c = R.cmp[v.focus], j = bj(v.focus), N = R.names, egc = isEg ? '<b class="nlo__egc">דוגמה</b>' : '';
        var h = '';
        if (c.have.length < 2) {
          h = '<span class="nli__alab">הפער בין ההצעות בסל ' + j + egc + '</span><p class="nli__note">הקלידו את ' + (c.by === 'total' ? 'סך התשלומים הצפוי' : 'הריבית הכוללת החזויה') + ' בסל ' + j + ' בשתי הצעות לפחות.</p>';
        } else if (c.by === 'total') {
          var tie = c.dearest == null, ci = c.cheapest[0];
          h = '<span class="nli__alab">הפער בין ההצעות בסל ' + j + ', לאורך ההלוואה' + egc + '</span><output class="nli__fig nlo__dec">' + esc(uils(tie ? 0 : c.gapTotal)) + '</output>'
            + '<span class="nli__asub">' + (tie ? 'ההצעות שוות בסל הזה.' : esc('ההצעה של ' + N[ci] + ' זולה מזו של ' + N[c.dearest]) + (fin(c.gapMax) ? '. ההחזר החודשי הגבוה הצפוי ' + (c.gapMax >= 0 ? 'נמוך בה ב־' + fig(uils(c.gapMax)) : 'גבוה בה ב־' + fig(uils(-c.gapMax))) : '') + '.') + '</span>';
        } else {
          var ci2 = c.cheapest[0];
          h = '<span class="nli__alab">הפער בריבית הכוללת החזויה, סל ' + j + egc + '</span><output class="nli__fig nlo__dec">' + esc(c.dearest == null ? upct(0) : upct(c.gapIrr)) + '</output>'
            + '<span class="nli__asub">' + (c.dearest == null ? 'ההצעות שוות בסל הזה.' : esc('ההצעה של ' + N[ci2] + ' זולה מזו של ' + N[c.dearest] + '.')) + ' התקופות באישורים שונות, ולכן ההשוואה לפי הריבית הכוללת החזויה ולא לפי סך התשלומים.</span>';
        }
        var lines = BASKETS.map(function (k) {
          var x = R.cmp[k], val;
          if (x.have.length < 2) val = 'חסרים מספרים';
          else if (x.dearest == null) val = 'שוות';
          else val = esc(x.cheapest.map(function (i) { return N[i]; }).join(', ')) + ' · ' + fig(x.by === 'total' ? uils(x.gapTotal) : upct(x.gapIrr)) + ' פחות';
          return '<div><dt>הזולה בסל ' + bj(k) + '</dt><dd>' + (x.have.length < 2 || x.dearest == null ? esc(val) : val) + '</dd></div>';
        }).join('');
        ans.innerHTML = h + '<dl class="nli__lines">' + lines + '</dl>'
          + '<p class="nlo__fx">הפער = ' + (c.by === 'total' ? 'סך התשלומים הצפוי של ההצעה היקרה פחות זה של הזולה' : 'הריבית הכוללת החזויה של ההצעה היקרה פחות זו של הזולה')
          + (R.norm.loansEqual || !fin(R.norm.base) ? '' : ', אחרי התאמת כל הצעה להלוואה של ' + esc(uils(R.norm.base))) + '. מקור: האישורים שהקלדתם.</p>';
      }
      function cellVal(m, x) { return m === 'irr' ? (fin(x.irr) ? upct(x.irr) : '') : m === 'total' ? (fin(x.nTotal) ? uils(x.nTotal) : '') : m === 'maxPay' ? (fin(x.nMax) ? uils(x.nMax) : '') : (fin(x.nFirst) ? uils(x.nFirst) : ''); }
      function gapVal(m, c) {
        if (c.dearest == null) return '';
        var f = function (n) { return uils(n); };
        return m === 'irr' ? (fin(c.gapIrr) ? sgn(c.gapIrr, function (n) { return upct(n); }) : '') : m === 'total' ? (fin(c.gapTotal) ? sgn(c.gapTotal, f) : '') : m === 'maxPay' ? (fin(c.gapMax) ? sgn(c.gapMax, f) : '') : (fin(c.gapFirst) ? sgn(c.gapFirst, f) : '');
      }
      function paintTable(R) {
        var N = R.names, live = R.norm.rows.filter(function (r) { return r.live; }).map(function (r) { return r.i; });
        if (live.length === 0) { tbl.innerHTML = ''; return; }
        var head = '<thead><tr><th scope="col">סל</th>' + live.map(function (i) { return '<th scope="col">' + esc(N[i]) + '</th>'; }).join('') + '<th scope="col">היקרה פחות הזולה</th></tr></thead>';
        var body = '';
        BASKETS.forEach(function (k, j) {
          var c = R.cmp[k], marked = c.dearest != null;
          body += '<tr class="nlo__bh' + (k === v.focus ? ' is-focus' : '') + '"><th scope="rowgroup" colspan="' + (live.length + 2) + '">סל אחיד ' + (j + 1)
            + (marked ? '<span class="nlo__tag">הזולה: ' + esc(c.cheapest.map(function (i) { return N[i]; }).join(', ')) + '</span>' : '') + '<small class="nlo__mx">' + esc(basketText(D, k)) + '</small></th></tr>';
          METRICS.forEach(function (m) {
            body += '<tr><th scope="row">' + esc(MLAB[m]) + '</th>' + live.map(function (i) { var best = marked && c.cheapest.indexOf(i) > -1; return '<td class="n' + (best ? ' is-best' : '') + '">' + esc(cellVal(m, R.norm.rows[i].b[k])) + '</td>'; }).join('')
              + '<td class="n">' + esc(gapVal(m, c)) + '</td></tr>';
          });
        });
        var note = R.norm.loansEqual || !fin(R.norm.base) ? '' : '<p class="nlo__hint">הסכומים באישורים שונים: כל המספרים בשקלים מותאמים להלוואה של ' + fig(uils(R.norm.base)) + '.</p>';
        var termNote = R.norm.termsEqual ? '' : '<p class="nlo__hint">התקופות באישורים שונות: הזולה בכל סל נקבעת לפי הריבית הכוללת החזויה.</p>';
        var wide = '<div class="nlo__wide"><div class="nlo__tw"><table class="nlo__t">' + head + '<tbody>' + body + '</tbody></table></div></div>';
        var k = v.focus, c = R.cmp[k], marked = c.dearest != null;
        var card = '<div class="nlo__cards"><div class="nlo__card"><h4 class="nlo__h4">סל אחיד ' + bj(k) + '</h4><p class="nlo__mx">' + esc(basketText(D, k)) + '</p>'
          + live.map(function (i) {
            var x = R.norm.rows[i].b[k], best = marked && c.cheapest.indexOf(i) > -1;
            return '<div class="nlo__bank' + (best ? ' is-best' : '') + '"><div class="nlo__bn">' + esc(N[i]) + (best ? '<span class="nlo__tag">הזולה בסל</span>' : '') + '</div><dl class="nlo__kv">'
              + METRICS.map(function (m) { var s = cellVal(m, x); return '<div><dt>' + esc(MLAB[m]) + '</dt><dd>' + esc(s || 'לא הוקלד') + '</dd></div>'; }).join('') + '</dl></div>';
          }).join('')
          + (marked && c.by === 'total' ? '<p class="nlo__gap">הפער: ' + fig(uils(c.gapTotal)) + ' לאורך ההלוואה' + (fin(c.gapMax) ? ', ' + fig(sgn(c.gapMax, uils)) + ' בהחזר החודשי הגבוה' : '') + '</p>' : marked ? '<p class="nlo__gap">הפער בריבית הכוללת החזויה: ' + fig(upct(c.gapIrr)) + '</p>' : '')
          + '<p class="nlo__hint">את הסלים האחרים בוחרים למעלה, ב"הסל להשוואה".</p></div></div>';
        tbl.innerHTML = note + termNote + wide + card
          + '<p class="nlo__fx">נרמול: סך התשלומים, ההחזר הגבוה וההחזר הראשון × (סכום ההלוואה של ' + esc(N[live[0]]) + ' ÷ הסכום באישור). הזולה בסל: סך התשלומים הצפוי הנמוך, כשהתקופות שוות. הסלים: ' + esc(D.baskets.src.label) + '.</p>';
      }

      function gapWords(g) { return Math.abs(g) < 0.005 ? 'כמו הממוצע' : (g > 0 ? 'גבוהה ב־' : 'נמוכה ב־') + fig(upct(Math.abs(g))) + ' מהממוצע'; }
      function paintAvg(R) {
        var N = R.names, j = bj(v.focus);
        avgSec.innerHTML = '';
        avgSec.appendChild(el('h3', 'nlo__h', 'כל הצעה מול הממוצע של אותו בנק'));
        avgSec.appendChild(el('p', 'nlo__p', 'בנק ישראל מפרסם בכל חודש, לכל בנק, את הריבית הממוצעת בכל מסלול ואת הריבית הכוללת החזויה על כל המשכנתאות החדשות שהבנק נתן. החודש האחרון שפורסם: ' + esc(monthHe(MONTH)) + '.'));
        var grid2 = el('div', 'nlo__avg');
        R.offers.forEach(function (o, i) {
          if (!hasAny(o) && !(o.mix && o.mix.length)) return;
          var own = R.refs[i], ref = own || SYS, box = el('div', 'nlo__pc');
          box.appendChild(el('h4', 'nlo__h4', esc(N[i] + (own ? ' מול הממוצע של ' + own.name : ' מול הממוצע של כל הבנקים'))));
          if (!own) box.appendChild(el('p', 'nlo__hint', v.offers[i].bank === 'other' ? 'לבנק הזה אין ממוצע נפרד בנתוני בנק ישראל, ולכן ההשוואה מול כל הבנקים.' : 'בחרו את הבנק בטופס, ונשווה לממוצע שלו. בינתיים: מול כל הבנקים.'));
          var dl = '<dl class="nli__lines"><div><dt>ריבית כוללת חזויה ממוצעת, ' + esc(ref.name) + ', ' + esc(mon(ref.month)) + '</dt><dd>' + fig(upct(ref.irr)) + '</dd></div>';
          BASKETS.forEach(function (k, q) { var x = o.b[k].irr; if (fin(x)) { var p = place(x, ref); dl += '<div><dt>סל ' + (q + 1) + ' בהצעה</dt><dd>' + fig(upct(x)) + ' · ' + gapWords(p.gapOwn) + '</dd></div>'; } });
          box.insertAdjacentHTML('beforeend', dl + '</dl>');
          var fx = o.b[v.focus].irr;
          if (fin(fx)) {
            var p = place(fx, ref), s;
            if (p.pos === 'below') s = 'נמוכה מהממוצע של כל חמשת הבנקים הגדולים (הנמוך: ' + esc(p.lo.name) + ', ' + fig(upct(p.lo.irr)) + ').';
            else if (p.pos === 'above') s = 'גבוהה מהממוצע של כל חמשת הבנקים הגדולים (הגבוה: ' + esc(p.hi.name) + ', ' + fig(upct(p.hi.irr)) + ').';
            else if (p.pos === 'equal') s = 'כמו הממוצע של ' + esc(p.under.name) + ' (' + fig(upct(p.under.irr)) + ').';
            else s = 'בין הממוצע של ' + esc(p.under.name) + ' (' + fig(upct(p.under.irr)) + ') לזה של ' + esc(p.over.name) + ' (' + fig(upct(p.over.irr)) + ').';
            box.appendChild(el('p', '', 'בסל ' + j + ' הריבית הכוללת החזויה בהצעה, ' + fig(upct(fx)) + ', ' + s));
          }
          var mx = (o.mix || []).filter(function (m) { return TRACK_KEYS.indexOf(m.track) > -1; });
          if (mx.length) {
            var rows = mx.map(function (m) { return trackCmp(m, ref, o.loan); }).filter(Boolean);
            var tb = '<h4 class="nlo__h4">המסלולים בהצעה מול הממוצע של ' + esc(ref.name) + '</h4>';
            rows.forEach(function (r) {
              tb += '<div class="nlo__trk"><p class="nlo__tn">' + esc(TRACK_HE[r.track]) + (fin(r.share) ? '<small>' + esc(F.num(r.share, r.share % 1 ? 1 : 0) + '% מההלוואה' + (fin(r.years) ? ', ' + F.num(r.years, 0) + ' שנים' : '')) + '</small>' : '') + '</p><dl class="nlo__k3">'
                + '<div><dt>בהצעה</dt><dd>' + esc(fin(r.rate) ? upct(r.rate) : 'לא הוקלד') + '</dd></div>'
                + '<div><dt>ממוצע הבנק</dt><dd>' + esc(upct(r.nom)) + '</dd><small>' + esc('אפקטיבית ' + upct(r.eff) + ', ' + F.num(r.bankShare, 0) + '% מהאשראי') + '</small></div>'
                + '<div><dt>הפער</dt><dd>' + esc(fin(r.gap) ? sgn(r.gap, function (n) { return upct(n); }) : '') + '</dd>' + (fin(r.payGap) ? '<small>' + esc((r.payGap >= 0 ? 'כ־' + uils(r.payGap) + ' יותר' : 'כ־' + uils(-r.payGap) + ' פחות') + ' בחודש') + '</small>' : '') + '</div></dl></div>';
            });
            box.insertAdjacentHTML('beforeend', tb);
          }
          grid2.appendChild(box);
        });
        avgSec.appendChild(grid2);
        /* the ladder: the focus basket of every offer among the five large banks' averages */
        var pts = SYS.rank.map(function (r) { return { label: r.name, v: r.irr, cls: '' }; });
        pts.push({ label: 'כל הבנקים', v: SYS.irr, cls: 'is-sys' });
        R.refs.forEach(function (r) { if (r && !r.big5 && !pts.some(function (p) { return p.label === r.name; })) pts.push({ label: r.name, v: r.irr, cls: '' }); });
        R.offers.forEach(function (o, i) { var x = o.b[v.focus].irr; if (fin(x)) pts.push({ label: 'ההצעה של ' + N[i], v: x, cls: 'is-offer' }); });
        pts.sort(function (a, b) { return a.v - b.v; });
        var lo = Math.min.apply(null, pts.map(function (p) { return p.v; })), hi = Math.max.apply(null, pts.map(function (p) { return p.v; })), pad = Math.max(0.05, (hi - lo) * 0.08);
        var lad = '<h4 class="nlo__h4">הריבית הכוללת החזויה בסל ' + j + ' מול הממוצעים של ' + esc(mon(MONTH)) + '</h4><div class="nlo__lad" role="list">';
        pts.forEach(function (p) { var x = 100 * (p.v - lo + pad) / (hi - lo + 2 * pad); lad += '<div class="nlo__lr ' + p.cls + '" role="listitem"><span class="l">' + esc(p.label) + '</span><span class="t" aria-hidden="true"><i style="left:' + x.toFixed(1) + '%"></i></span><b class="v">' + esc(upct(p.v)) + '</b></div>'; });
        var lw = el('div', 'nlo__pc'); lw.style.marginTop = '12px'; lw.innerHTML = lad + '</div>';
        avgSec.appendChild(lw);
        var jer = R.refs.filter(function (r) { return r && r.key === 'jerusalem'; })[0], extra = '';
        if (jer) { var cp = jer.row.var_cpi.share + jer.row.fixed_cpi.share, sc = SYS.sys.var_cpi.share + SYS.sys.fixed_cpi.share; extra = ' בבנק ירושלים ' + F.num(cp, 0) + '% מהאשראי של ' + mon(MONTH) + ' היה צמוד למדד, מול ' + F.num(sc, 0) + '% בכל הבנקים.'; }
        avgSec.appendChild(el('p', 'nli__note', 'ממוצע של בנק תלוי בתמהיל ובלקוחות של אותו בנק באותו חודש: כמה מהאשראי בפריים וכמה צמוד למדד, איזה שיעור מימון ולאיזו תקופה. הוא אינו הצעה. בנק שהממוצע שלו גבוה יכול לתת הצעה נמוכה, וגם ההפך. הסל האחיד באישור הוא תמהיל קבוע, ולכן הממוצע הוא נקודת ייחוס בלבד.' + esc(extra)));
        avgSec.appendChild(el('p', 'nlo__fx', 'ריבית כוללת חזויה: לפי הנוסחה של הוראה 451, מתחזיות המדד והריבית של בנק ישראל לאותו חודש. ממוצע בנק במסלול: הריבית האפקטיבית שפורסמה, מומרת לנומינלית = <bdi dir="ltr">12 × ((1 + ר)^(1/12) − 1)</bdi>. הפער בחודש: ההחזר בשפיצר בריבית שבהצעה פחות ההחזר בריבית הממוצעת, על החלק של המסלול ולתקופה שלו, בלי הצמדה ובלי שינוי ריבית. מקור: '
          + '<a href="' + esc(BB.src.page) + '" target="_blank" rel="noopener">בנק ישראל, הפיקוח על הבנקים, השוואת ריביות בהלוואות לדיור (קו המשווה)</a>, נתוני ' + esc(mon(MONTH)) + ', הקובץ מ־' + esc(F.date(BB.src.file_date)) + '.'));
      }

      var letSel = null, letDoc = null, letKey = '';
      function buildLetter() {
        letSec.innerHTML = '';
        letSec.appendChild(el('h3', 'nlo__h', 'נוסח לשיחה עם הבנק'));
        letSec.appendChild(el('p', 'nlo__p', 'נוסח מנומס בגוף ראשון, עם המספרים מהאישורים שלכם והממוצעים שבנק ישראל פרסם. מעתיקים, ומשנים מה שרוצים לפני השליחה.'));
        var w = el('div', 'nlo__lt'), f = el('div', 'nli__f'), id = uid + '-target';
        var lab = el('label', '', 'הנוסח מופנה אל'); lab.htmlFor = id; f.appendChild(lab);
        var box = el('div', 'nli__in'); letSel = el('select'); letSel.id = id; box.appendChild(letSel); f.appendChild(box); f.style.maxWidth = '420px';
        letSel.addEventListener('change', function () { v.target = +letSel.value; paint(); });
        w.appendChild(f);
        letDoc = el('pre', 'nli__doc'); w.appendChild(letDoc);
        var cb = el('button', 'nlo__copy', ICON.copy + '<span>העתקת הנוסח</span>'); cb.type = 'button';
        cb.addEventListener('click', function () { copy(cb, letter(last), 'העתקת הנוסח'); });
        w.appendChild(cb);
        letSec.appendChild(w);
        letSec.appendChild(el('p', 'nlo__fx', 'בנוסח מופיעים רק המספרים שהקלדתם והממוצעים שבנק ישראל פרסם ל' + esc(monthHe(MONTH)) + '.'));
      }
      function paintLetter(R) {
        if (!letSel) buildLetter();
        var key = R.names.join('|');
        if (key !== letKey) { letKey = key; letSel.innerHTML = ''; R.names.forEach(function (n, i) { var op = el('option', '', esc(n)); op.value = String(i); letSel.appendChild(op); }); }
        letSel.value = String(R.target);
        letDoc.textContent = letter(R);
      }
      function buildAdv() {
        advSec.innerHTML = '';
        advSec.appendChild(el('h3', 'nlo__h', 'הטבלה אצל יועץ משכנתאות'));
        advSec.appendChild(el('p', 'nlo__p', 'רוצים שמישהו יעבור על ההצעות איתכם? מעתיקים את הטבלה כטקסט, ושולחים אותה ליועץ משכנתאות.'));
        var cb = el('button', 'nlo__copy', ICON.copy + '<span>העתקת הטבלה</span>'); cb.type = 'button';
        cb.addEventListener('click', function () { copy(cb, tableText(last), 'העתקת הטבלה'); });
        advSec.appendChild(cb);
        var a = el('a', 'nlo__go', 'לשלוח את הטבלה ליועץ משכנתאות'); a.href = ADVISOR; advSec.appendChild(a);
      }
      function copy(btn, txt, lab) {
        var sp = btn.querySelector('span'), done = function () { sp.textContent = 'הועתק'; setTimeout(function () { sp.textContent = lab; }, 1600); };
        var ask = function () { try { window.prompt('העתיקו', txt); } catch (e) { /* an in-app browser without prompt(): nothing to copy into */ } };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, ask); else ask();
      }
      function buildFoot() {
        formula.textContent = 'סך התשלומים הצפוי, ההחזר החודשי הגבוה הצפוי וההחזר הראשון מוקלדים מהאישורים; כשהסכומים שונים, כל הצעה מותאמת לסכום של ההצעה הראשונה ביחס ישר. הזולה בסל: סך התשלומים הצפוי הנמוך כשהתקופות שוות, והריבית הכוללת החזויה הנמוכה כשהן שונות. הממוצעים של הבנקים: ' + monthHe(MONTH) + ', כפי שבנק ישראל פרסם.';
        src.innerHTML = 'מקורות: <a href="' + esc(BB.src.page) + '" target="_blank" rel="noopener">בנק ישראל, השוואת ריביות בהלוואות לדיור לפי בנק, ' + esc(mon(MONTH)) + '</a> · '
          + '<a href="' + esc(D.baskets.src.url) + '" target="_blank" rel="noopener">' + esc(D.baskets.src.label) + '</a>. הנתונים עודכנו ב־' + esc(F.date(D.built)) + '.';
        share.innerHTML = '';
        var b1 = el('button', 'is-primary', ICON.copy + '<span>' + esc(NI.TX.copy.he) + '</span>'); b1.type = 'button';
        b1.addEventListener('click', function () { copy(b1, tableText(last) + '\n' + shareState(), NI.TX.copy.he); });
        var b2 = el('button', '', ICON.print + '<span>' + esc(NI.TX.print.he) + '</span>'); b2.type = 'button';
        b2.addEventListener('click', function () { window.print(); });
        var b3 = el('button', '', ICON.link + '<span>קישור שפותח את אותם מספרים</span>'); b3.type = 'button';
        b3.addEventListener('click', function () { copy(b3, shareState(), 'קישור שפותח את אותם מספרים'); });
        share.appendChild(b1); share.appendChild(b2); share.appendChild(b3);
        var e0 = example().offers[0];
        egNote.innerHTML = '<b>דוגמה</b>' + esc('הערכים בפתיחה הם דוגמה: שני אישורים על ' + uils(e0.loan) + ' ל־' + e0.years + ' שנה, מ"בנק א׳" ומ"בנק ב׳". הקלידו את המספרים מהאישורים שלכם ובחרו את הבנקים, והטבלה מתעדכנת מיד. המחשבון אינו הצעה לאשראי ואינו ייעוץ.');
      }

      buildAdv(); buildFoot(); buildForm(); paint();
      window.NLMO.ui = { state: function () { return v; }, last: function () { return last; }, paint: paint, rebuild: function () { buildForm(); paint(); }, link: shareState };
    }
  });
})();
