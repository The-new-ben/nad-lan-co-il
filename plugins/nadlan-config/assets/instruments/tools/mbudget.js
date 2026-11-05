/* NadLan Instruments · mbudget v1 "כמה דירה זה קונה, ואיפה" (HAD-675, the mortgage page panel 1, design board Tools.dc.html).
   In under a minute: net household income, equity, buyer type, optional existing loans and the share of income for the payment
   (default 33%, never above the Bank of Israel cap of 50%). Three answers:
   1. the highest home price that passes BOTH Bank of Israel limits (payment to income, LTV by buyer type) with the purchase tax
      and the lawyer covered by the equity. The solver is the existing window.NLAF.compute (tools/afford.js), fed with one
      equivalent nominal rate that reproduces the blended first payment of the five tracks in the Bank of Israel system average
      mix of the latest month (by_bank.latest.table, row "system"; monthly rate = (1+e/100)^(1/12)-1; 1,000,000 over 25 years
      = 5,428 a month in 9.2026);
   2. where: every city whose official median deal price for 3, 4 or 5 rooms (homes.payments.rows, Tax Authority via
      nadlan.gov.il) is at or under that price, with the household's own first payment at that median;
   3. homes for sale on the site at or under that price, from the public read only endpoint /wp-json/nadlan/v1/near-finder
      (listings only: projects there carry no home price, so none is shown; unknown = omitted). If it fails, 1 and 2 stay.
   Data: boi-mortgage.json (key "boim", v2 keys by_bank + homes + rules), ptax.json, cost.json. Pure logic in window.NLMB (DOM
   free, tested by test_mbudget.js in node). Hebrew only (RTL); no long dash anywhere in visible text. */
(function () {
  'use strict';
  var W = typeof window !== 'undefined' ? window : globalThis;
  var HAS_DOC = typeof document !== 'undefined';
  // afford.js sits next to this file in tools/; when the page did not load it, it is loaded from there before the first run
  var ME = HAS_DOC && document.currentScript ? document.currentScript.src : '';
  var AFF = ME ? ME.replace(/[^\/]*\.js(\?.*)?$/, 'afford.js$1') : '';

  /* =========================================================================================================== the math */
  var TRK = ['fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi'];
  var ROOMS = ['r3', 'r4', 'r5'];
  function mrate(e) { return Math.pow(1 + e / 100, 1 / 12) - 1; }  // effective annual % to a monthly rate
  function pmt(L, r, n) { return r === 0 ? L / n : L * r / (1 - Math.pow(1 + r, -n)); }
  function sysRow(boim) {
    var t = boim && boim.by_bank && boim.by_bank.latest && boim.by_bank.latest.table;
    if (!t) return null;
    for (var i = 0; i < t.length; i++) if (t[i].bank === 'system') return t[i];
    return null;
  }
  /** The blended first payment of 1,000,000 over n months: each track its share of the loan at its own monthly rate. */
  function perMillion(row, n) {
    var sh = 0, tot = 0;
    TRK.forEach(function (k) { sh += +row[k].share; });
    TRK.forEach(function (k) { tot += pmt(1e6 * row[k].share / sh, mrate(+row[k].rate), n); });
    return tot;
  }
  /** The one nominal annual rate (%) whose Spitzer payment equals perM per million over n months (what NLAF.compute takes). */
  function eqRate(perM, n) {
    if (perM <= 1e6 / n) return 0;
    var lo = 0, hi = 0.05;
    for (var i = 0; i < 200; i++) { var mid = (lo + hi) / 2; if (pmt(1e6, mid, n) < perM) lo = mid; else hi = mid; }
    return (lo + hi) / 2 * 1200;
  }
  function brackets(price, br) { var t = 0, lo = 0; for (var i = 0; i < br.length; i++) { var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(price, hi); if (top > lo) t += (top - lo) * br[i][1]; if (price <= hi) break; lo = hi; } return t; }
  function trackOf(P, k, price) { return k === 'oleh' && P.oleh_cap && price > P.oleh_cap ? P.tracks.single : P.tracks[k]; }  // the same oleh cap as afford.js
  function ptax(price, P, k) { return brackets(price, trackOf(P, k, price)); }

  /** inp: {income, equity, track, loans, ratio, years}; D: {boim, ptax, cost}. Returns the model of answer 1. */
  function solve(inp, D) {
    var row = sysRow(D.boim), n = Math.round((+inp.years || 25) * 12);
    var perM = perMillion(row, n), R = eqRate(perM, n);
    var cap = 100 * ((D.boim.rules && D.boim.rules.pti_max) || 0.5);
    var ratio = Math.min(+inp.ratio || 0, cap);
    var lawyer = D.cost.lawyer && D.cost.lawyer.from != null ? +D.cost.lawyer.from : 0.5;
    var k = D.ptax.tracks[inp.track] ? inp.track : 'single';
    var r = W.NLAF.compute({ income: +inp.income || 0, loans: +inp.loans || 0, equity: +inp.equity || 0, track: k, ratio: ratio, rate: R, years: n / 12, lawyer: lawyer }, D.ptax, D.cost);
    var first = D.ptax.tracks[k][0];
    return {
      k: k, price: r.price, loan: r.loan, monthly: r.loan * perM / 1e6, payMax: r.payMax, loanMax: r.loanMax, ltv: r.ltv,
      tax: r.tax, lawyer: r.lawyer, limit: r.limit, perM: perM, rate: R, n: n, years: n / 12, ratio: ratio, cap: cap,
      lawyerPct: lawyer, vat: D.cost.vat, month: D.boim.by_bank.latest.month, taxFree: first && first[1] === 0 ? first[0] : null,
      cash: r.price - r.loan + r.tax + r.lawyer
    };
  }
  /** The loan the household needs at a cheaper price: what the equity does not cover after the tax and the lawyer. */
  function needLoan(price, m, inp, P) { return Math.max(0, price + ptax(price, P, m.k) + m.lawyerPct / 100 * (1 + m.vat) * price - (+inp.equity || 0)); }

  /** Answer 2: every city and room count with an official median at or under the max price. */
  function cities(boim, m, inp, P) {
    var rows = boim.homes.payments.rows, list = [], natl = null, cheapest = {};
    Object.keys(rows).forEach(function (city) {
      ROOMS.forEach(function (rk) {
        var x = rows[city][rk];
        if (!x || !(x.median > 0)) return;
        var rooms = +rk.slice(1), fits = x.median <= m.price;
        var it = { city: city, rooms: rooms, median: x.median, quarter: x.quarter, fits: fits };
        if (fits) { it.loan = needLoan(x.median, m, inp, P); it.payment = it.loan * m.perM / 1e6; }
        if (city === 'ישראל') { natl = natl || {}; natl[rooms] = it; return; }
        if (!cheapest[rooms] || x.median < cheapest[rooms].median) cheapest[rooms] = it;
        if (fits) list.push(it);
      });
    });
    list.sort(function (a, b) { return b.median - a.median; });  // the closest to the budget first
    var count = {}; [3, 4, 5].forEach(function (r) { count[r] = list.filter(function (x) { return x.rooms === r; }).length; });
    var total = Object.keys(rows).filter(function (c) { return c !== 'ישראל'; }).length;
    return { list: list, natl: natl || {}, cheapest: cheapest, count: count, total: total };
  }
  function bestRooms(cs) { return cs.count[4] ? 4 : cs.count[3] ? 3 : 4; }  // the family home first (the design board); 5 rooms is one tap away

  /** Answer 3: homes for sale on the site with a published price at or under the max price (projects carry no price). */
  function safeUrl(u) { return typeof u === 'string' && /^https:\/\/(www\.)?nad-lan\.co\.il\//.test(u) ? u : ''; }
  function listings(nf, max, lim) {
    var L = (nf && nf.listings) || [];
    var sale = L.filter(function (x) { return x && x.deal === 'sale' && +x.price > 0 && safeUrl(x.url) && x.title; });
    var fit = sale.filter(function (x) { return +x.price <= max; }).sort(function (a, b) { return b.price - a.price; });
    return { priced: sale.length, count: fit.length, updated: nf && nf.updated ? String(nf.updated) : '',
      items: fit.slice(0, lim || 6).map(function (x) { return { id: x.id, title: String(x.title), city: x.city ? String(x.city) : '', price: +x.price, rooms: +x.rooms || 0, sqm: +x.sqm || 0, url: safeUrl(x.url) }; }) };
  }

  /* ====================================================================================================== text and html */
  var NAMES = { single: 'דירה יחידה', extra: 'דירה נוספת', oleh: 'עולה חדש', foreign: 'תושב חוץ' };
  var nf0 = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function ils(n) { return '₪' + nf0.format(Math.round(n || 0)); }  // the engine's own format (core.js fmt.ils)
  function num(n, d) { return new Intl.NumberFormat('he-IL', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }).format(n || 0); }
  function pct(n) { return num(n, n % 1 ? 1 : 0) + '%'; }
  function mon(key) { var p = String(key).split('-'); return p.length > 1 ? (+p[1]) + '.' + p[0] : key; }
  function day(iso) { var p = String(iso).slice(0, 10).split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : iso; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function b(x) { return '<bdi>' + esc(x) + '</bdi>'; }
  function math(x) { return '<bdi dir="ltr" class="nlmb__math">' + esc(x) + '</bdi>'; }
  function roomsWord(r) { return r + ' חדרים'; }
  function citiesWord(n) { return n === 1 ? 'עיר אחת' : n + ' ערים'; }

  function srcRates(boim) { var s = boim.by_bank.src; return { label: 'בנק ישראל, ריביות ותמהיל ממוצעים במשכנתאות חדשות, כל הבנקים, ' + mon(s.as_of) + ' (פורסם ' + day(s.file_date) + ')', url: s.page || s.url }; }

  /** The answer column (answer 1). */
  function answerHtml(m, inp, D, eg) {
    var P = D.ptax, C = D.cost, boim = D.boim, h = '';
    h += '<div class="nlmb__answer"><div class="nlmb__alab"><span class="nli__alab">מחיר הדירה הגבוה ביותר</span>' + (eg ? '<span class="nlmb__egb">דוגמה, שנו כל שדה</span>' : '') + '</div>';
    h += '<output class="nlmb__fig">' + b(ils(m.price)) + '</output>';
    h += '<span class="nlmb__sub">' + (m.loan > 0.5 ? 'משכנתא ' + b(ils(m.loan)) + ' · החזר ראשון ' + b(ils(m.monthly)) + ' בחודש' : 'בלי משכנתא') + ' · ' + esc(NAMES[m.k]) + '</span>';
    var parts = [{ l: 'משכנתא', v: m.loan, k: 'sea' }, { l: 'הון עצמי לדירה', v: m.price - m.loan, k: 'housing' }, { l: 'מס רכישה ועורך דין', v: m.tax + m.lawyer, k: 'civic' }].filter(function (x) { return x.v > 0.5; });
    var tot = parts.reduce(function (s, x) { return s + x.v; }, 0) || 1;
    h += '<div class="nli__bar" role="img" aria-label="' + esc(parts.map(function (x) { return x.l + ' ' + ils(x.v); }).join(', ')) + '">' + parts.map(function (x) { return '<i class="nli__k-' + x.k + '" style="width:' + (100 * x.v / tot).toFixed(2) + '%"></i>'; }).join('') + '</div>';
    h += '<ul class="nli__legend">' + parts.map(function (x) { return '<li><b class="nli__k-' + x.k + '"></b>' + esc(x.l) + ' ' + b(ils(x.v)) + '</li>'; }).join('') + '</ul>';
    var lines = [
      ['החזר מרבי לפי ההכנסה (' + pct(m.ratio) + ')', ils(m.payMax) + ' בחודש'],
      ['משכנתא מרבית לפי ההחזר', ils(m.loanMax)],
      ['מימון מרבי, ' + NAMES[m.k], pct(100 * m.ltv) + ' · ' + ils(m.ltv * m.price)],
      ['מס רכישה במחיר הזה', m.tax < 0.5 && m.taxFree ? 'פטור עד ' + ils(m.taxFree) : ils(m.tax)],
      ['עורך דין, ' + pct(m.lawyerPct) + ' ועוד מע״מ', ils(m.lawyer)],
      ['מה שמגביל', m.limit === 'payment' ? 'ההכנסה' : 'ההון העצמי']
    ];
    h += '<dl class="nli__lines">' + lines.map(function (l) { return '<div><dt>' + esc(l[0]) + '</dt><dd>' + esc(l[1]) + '</dd></div>'; }).join('') + '</dl>';
    h += '</div>';
    var note;
    if (m.payMax <= 0) note = '<b>ההלוואות הקיימות גדולות מההחזר שבחרתם,</b> ולכן אין מקום למשכנתא. המחיר מבוסס על ההון העצמי בלבד.';
    else if (m.limit === 'payment') note = '<b>ההכנסה היא מה שמגביל:</b> עוד הון עצמי לא יגדיל את המשכנתא. תקופה ארוכה יותר, הכנסה גבוהה יותר או פחות הלוואות קיימות כן.';
    else note = '<b>ההון העצמי הוא מה שמגביל:</b> הבנק יממן עד ' + pct(100 * m.ltv) + ' מהשווי, ואת השאר, יחד עם מס הרכישה ועורך הדין, צריך להביא מהבית.';
    h += '<p class="nli__note">' + note + '</p>';
    h += '<button type="button" class="nlmb__cta" data-go="homes">הראו לי את הדירות האלה</button>';
    var rs = srcRates(boim);
    var f = '';  // the arithmetic itself runs left to right inside its own isolate, the words around it stay RTL
    if (m.payMax > 0) {
      f += 'החזר מרבי = ' + math(ils(inp.income) + ' × ' + pct(m.ratio) + (+inp.loans > 0 ? ' − ' + ils(inp.loans) : '') + ' = ' + ils(m.payMax)) + '. ';
      f += 'משכנתא מרבית = ' + math(ils(m.payMax) + ' ÷ ' + ils(m.perM) + ' × 1,000,000 = ' + ils(m.loanMax)) + '. ';
    }
    f += b(ils(m.perM)) + ' הוא ההחזר הראשון על מיליון ₪ ל־' + m.years + ' שנה בחמשת המסלולים, כל אחד בחלקו בתמהיל הממוצע של כל הבנקים, ' + b(mon(m.month)) + '. ';
    f += 'מחיר מרבי: המחיר הגבוה ביותר שבו המחיר פחות המשכנתא, ועוד מס רכישה ועורך דין, לא עולה על ההון העצמי, והמשכנתא עד ' + b(pct(100 * m.ltv)) + ' מהמחיר. ממוצע של הבנקים, לא הצעה אישית.';
    h += '<p class="nlmb__src">' + f + '</p>';
    var src = [rs, { label: (C.sources[2] && C.sources[2].label) || 'הוראת ניהול בנקאי תקין 329', url: C.sources[2] && C.sources[2].url }, { label: 'מס רכישה: רשות המסים, מדרגות בתוקף מ־' + day(P.effective) + ', נבדק ' + day(P.checked_v3 || P.checked), url: P.url }, { label: (C.sources[1] && C.sources[1].label) || 'ביזפורטל', url: C.sources[1] && C.sources[1].url }];
    h += '<p class="nlmb__src">מקורות: ' + src.map(function (s) { return s.url ? '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.label) + '</a>' : esc(s.label); }).join(' · ') + '</p>';
    return h;
  }

  /** The room picker counts (answer 2 header). */
  function roomsSegHtml(cs, cur) {
    return [3, 4, 5].map(function (r) { return '<button type="button" data-rooms="' + r + '" aria-pressed="' + (r === cur) + '">' + esc(roomsWord(r)) + (cs.count[r] ? ' · ' + esc(citiesWord(cs.count[r])) : '') + '</button>'; }).join('');
  }
  /** The cities list (answer 2). */
  function citiesHtml(cs, rooms, m, boim) {
    var rows = cs.list.filter(function (x) { return x.rooms === rooms; }), h = '', n = cs.natl[rooms];
    if (rows.length) {
      h += '<p class="nlmb__lead">דירת ' + esc(roomsWord(rooms)) + ' במחיר החציוני נכנסת בסכום של ' + b(ils(m.price)) + ' ב־' + esc(citiesWord(rows.length)) + ' מתוך ' + cs.total + ':</p>';
      h += '<ul class="nlmb__cities">' + rows.map(function (x) {
        var w = Math.max(2, Math.min(100, 100 * x.median / m.price));
        return '<li class="nlmb__city"><div class="nlmb__ch"><b>' + esc(x.city) + '</b>' + b(ils(x.median)) + '</div>' +
          '<div class="nlmb__fill" role="img" aria-label="' + esc('החציון הוא ' + Math.round(w) + '% מהמחיר המרבי') + '"><i style="width:' + w.toFixed(1) + '%"></i></div>' +
          '<span class="nlmb__meta">עסקאות ' + b(x.quarter) + ' · ' + (x.loan > 0.5 ? 'ההחזר שלכם ' + b(ils(x.payment)) + ' בחודש' : 'בלי משכנתא') + '</span></li>';
      }).join('') + '</ul>';
    } else {
      var c = cs.cheapest[rooms];
      h += '<p class="nli__note">בסכום של ' + b(ils(m.price)) + ' אין עדיין עיר ברשימה שבה דירת ' + esc(roomsWord(rooms)) + ' במחיר החציוני נכנסת.' + (c ? ' הזולה ביותר: ' + esc(c.city) + ', ' + b(ils(c.median)) + ' (עסקאות ' + b(c.quarter) + ').' : '') + '</p>';
    }
    if (n) h += '<p class="nlmb__natl">בכל הארץ: דירת ' + esc(roomsWord(rooms)) + ' במחיר החציוני ' + b(ils(n.median)) + ' (עסקאות ' + b(n.quarter) + ')' + (n.fits ? ', בתוך הסכום.' : ', מעל הסכום.') + '</p>';
    var s = boim.homes.medians.src || {};
    h += '<p class="nlmb__src">מקור: ' + (s.url ? '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">רשות המסים, עסקאות שנסגרו (אתר נדל״ן הממשלתי)</a>' : 'רשות המסים, עסקאות שנסגרו') + ', חציון לפי מספר חדרים, הרבעון האחרון שפורסם בכל עיר' + (s.retrieved_at ? ', נקרא ' + day(s.retrieved_at) : '') + '. החציון הוא הדירה שבאמצע, לא דירה מסוימת. ההחזר: ההלוואה שנדרשת אחרי ההון העצמי, מס הרכישה ועורך הדין, בתמהיל הממוצע של ' + mon(m.month) + ' ל־' + m.years + ' שנה.</p>';
    return h;
  }
  /** The homes on the site (answer 3). st: 'loading' | 'error' | 'ok'. */
  var ALL = 'https://nad-lan.co.il/properties/';
  function homesHtml(res, m, st) {
    var h = '', all = '<a class="nlmb__all" href="' + ALL + '">לכל הדירות למכירה באתר</a>';
    if (st === 'loading') return '<p class="nlmb__wait">טוענים את הדירות למכירה באתר…</p>' + all;
    if (st !== 'ok' || !res) return '<p class="nli__note">הדירות באתר לא נטענו כרגע. הן כולן כאן:</p>' + all;
    if (!res.count) return '<p class="nli__note">כרגע אין באתר דירה למכירה עם מחיר מפורסם עד ' + b(ils(m.price)) + '.</p>' + all;
    h += '<ul class="nlmb__homes">' + res.items.map(function (x) {
      var meta = [x.city, x.rooms ? num(x.rooms, x.rooms % 1 ? 1 : 0) + ' חדרים' : '', x.sqm ? num(x.sqm) + ' מ״ר' : ''].filter(Boolean).map(esc).join(' · ');
      return '<li class="nlmb__home"><a href="' + esc(x.url) + '">' + esc(x.title) + '</a>' + (meta ? '<span class="nlmb__meta">' + meta + '</span>' : '') + '<strong>' + b(ils(x.price)) + '</strong></li>';
    }).join('') + '</ul>';
    if (res.count > res.items.length) h += '<p class="nlmb__meta">מוצגות ' + res.items.length + ' מתוך ' + res.count + ' דירות עד הסכום.</p>';
    h += all;
    h += '<p class="nlmb__src">דירות למכירה באתר נדל״ן עם מחיר מפורסם, המחיר כפי שפורסם במודעה' + (res.updated ? ', עודכן ' + day(res.updated) : '') + '. פרויקטים חדשים לא מופיעים כאן כי אין להם מחיר דירה מפורסם.</p>';
    return h;
  }
  function shareText(m, inp, cs, rooms) {
    var rows = cs.list.filter(function (x) { return x.rooms === rooms; }).map(function (x) { return x.city; });
    return 'כמה דירה זה קונה: עם הכנסה נטו של ' + ils(inp.income) + ' בחודש והון עצמי של ' + ils(inp.equity) + ', ' + NAMES[m.k] + ': דירה עד ' + ils(m.price) +
      (m.loan > 0.5 ? ', משכנתא ' + ils(m.loan) + ', החזר ראשון ' + ils(m.monthly) + ' בחודש' : '') + '.' +
      (rows.length ? ' דירת ' + roomsWord(rooms) + ' במחיר החציוני: ' + rows.join(', ') + '.' : '');
  }

  W.NLMB = { pmt: pmt, mrate: mrate, sysRow: sysRow, perMillion: perMillion, eqRate: eqRate, ptax: ptax, solve: solve, needLoan: needLoan,
    cities: cities, bestRooms: bestRooms, listings: listings, safeUrl: safeUrl, ils: ils,
    html: { answer: answerHtml, rooms: roomsSegHtml, cities: citiesHtml, homes: homesHtml }, shareText: shareText, ALL: ALL };
  if (!W.NadLanInstruments || !HAS_DOC) return;

  /* ============================================================================================================== the page */
  var NI = W.NadLanInstruments;
  function css() {
    if (document.getElementById('nlmb-css')) return;
    var s = document.createElement('style'); s.id = 'nlmb-css';
    s.textContent = [
      '.nlmb .nlmb__answer{background:var(--nli-surface);border:1px solid var(--nli-sea);border-radius:var(--nli-r-m);padding:16px;display:grid;gap:10px;min-width:0}',
      '.nlmb__alab{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}',
      '.nlmb__egb{font:400 12px/16px var(--nli-sans);padding:2px 10px;border:1px solid var(--nli-line);border-radius:999px;color:var(--nli-mute)}',
      'html body .nli .nlmb__fig{display:block;font:500 40px/46px var(--nli-mono);color:var(--nli-ink);font-variant-numeric:tabular-nums;text-decoration:underline;text-decoration-color:var(--nli-survey);text-decoration-thickness:2px;text-underline-offset:8px;text-align:right;margin:0 0 4px}',
      '@media (max-width:400px){html body .nli .nlmb__fig{font-size:36px;line-height:42px}}',
      '.nlmb__sub{font:400 14px/20px var(--nli-sans);color:var(--nli-mute)}.nlmb__sub bdi{font-family:var(--nli-mono)}',
      'html body .nli .nlmb .nli__lines dd{white-space:normal;max-width:56%;overflow-wrap:anywhere}html body .nli .nlmb .nli__lines dt{min-width:0}',
      'html body .nli .nlmb .nli__legend bdi{font-family:var(--nli-mono)}',
      '@media (max-width:400px){.nlmb .nlmb__answer{padding:12px}html body .nli .nlmb .nli__lines div{gap:10px}html body .nli .nlmb .nli__lines dd{font-size:13px;max-width:58%}}',
      '.nlmb__math{display:inline-block;max-width:100%;white-space:normal;unicode-bidi:isolate;direction:ltr}',
      '.nli .nlmb{--nli-mono:"IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace}',  // Hebrew words inside a figure cell use Plex Hebrew, never the system Courier (as mortgage.js does)
      'html body .nli .nlmb .nli__in input::placeholder{color:var(--nli-mute);opacity:1;font-family:var(--nli-sans)}',
      'html body .nli .nlmb button.nlmb__cta{display:flex;align-items:center;justify-content:center;width:100%;min-height:48px;border:0;border-radius:var(--nli-r-s);background:var(--nli-sea);color:var(--nli-on-sea);font:600 16px/22px var(--nli-sans);cursor:pointer;margin:0;padding:10px 16px}',
      'html body .nli .nlmb button.nlmb__cta:hover{background:var(--nli-sea-deep)}',
      '.nlmb__src{font:400 12px/18px "IBM Plex Mono","IBM Plex Sans Hebrew",ui-monospace,monospace;color:var(--nli-mute);margin:0;position:relative}',
      'html body .nli .nlmb__src a{color:var(--nli-sea) !important}',
      '.nlmb__two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px;align-items:start}',
      '.nlmb .nlmb__sec{margin:28px 0 0;padding:20px 0 0;border-top:1px solid var(--nli-line);position:relative;display:grid;gap:12px}',
      'html body .nli .nlmb h3.nlmb__h{font:600 22px/28px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 !important;letter-spacing:0;text-transform:none}',
      '.nlmb__lead,.nlmb__natl{font:400 15px/24px var(--nli-sans);color:var(--nli-ink2);margin:0}.nlmb__lead bdi,.nlmb__natl bdi{font-family:var(--nli-mono)}',
      'html body .nli .nlmb__cities,html body .nli .nlmb__homes{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);gap:8px}',
      '@media (min-width:700px){html body .nli .nlmb__cities,html body .nli .nlmb__homes{grid-template-columns:repeat(2,minmax(0,1fr))}}',
      '@media (min-width:1040px){html body .nli .nlmb__cities{grid-template-columns:repeat(3,minmax(0,1fr))}}',
      'html body .nli .nlmb__city,html body .nli .nlmb__home{margin:0;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);padding:10px 12px;display:grid;gap:6px;min-width:0}',
      '.nlmb__ch{display:flex;justify-content:space-between;align-items:baseline;gap:8px}.nlmb__ch b{font:600 15px/22px var(--nli-sans);color:var(--nli-ink)}.nlmb__ch bdi{font:500 15px/22px var(--nli-mono);color:var(--nli-ink);font-variant-numeric:tabular-nums}',
      '.nlmb__fill{height:4px;background:var(--nli-line);border-radius:2px;overflow:hidden}.nlmb__fill i{display:block;height:100%;background:var(--nli-housing)}',
      '.nlmb__meta{display:block;font:400 13px/18px var(--nli-sans);color:var(--nli-mute);margin:0}.nlmb__meta bdi{font-family:var(--nli-mono)}',
      'html body .nli .nlmb__home a{font:600 15px/22px var(--nli-sans);color:var(--nli-sea) !important;text-decoration:underline;text-underline-offset:3px;overflow-wrap:anywhere}',
      '.nlmb__home strong{font:500 17px/22px var(--nli-mono);color:var(--nli-ink);text-align:right;font-variant-numeric:tabular-nums}',
      'html body .nli a.nlmb__all{justify-self:start;display:inline-flex;align-items:center;min-height:44px;padding:10px 16px;border:1px solid var(--nli-sea);border-radius:var(--nli-r-s);color:var(--nli-sea) !important;font:500 15px/20px var(--nli-sans);text-decoration:none !important}',
      '.nlmb__wait{font:400 14px/20px var(--nli-sans);color:var(--nli-mute);margin:0}',
      'html body .nli .nlmb .nli__seg button bdi{font-family:var(--nli-mono)}',
      '@media print{.nlmb__cta,.nlmb .nli__seg,.nlmb__all{display:none !important}}'
    ].join('\n');
    document.head.appendChild(s);
  }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function parse(v) { var n = parseFloat(String(v == null ? '' : v).replace(/[^\d.\-]/g, '')); return isFinite(n) ? n : NaN; }
  function input(id, label, val, unit, help, money, on, ph) {
    var w = el('div', 'nli__f'), iid = 'nlmb-' + id + '-' + Math.random().toString(36).slice(2, 7);
    var lab = el('label', '', esc(label)); lab.htmlFor = iid; w.appendChild(lab);
    var box = el('div', 'nli__in'), inp = el('input'); inp.id = iid; inp.type = 'text'; inp.inputMode = 'decimal'; inp.autocomplete = 'off';
    if (ph) inp.placeholder = ph;  // an optional field opens empty, never with a visible 0
    inp.value = ph && !(val > 0) ? '' : money ? nf0.format(val) : String(val);
    inp.addEventListener('input', function () { on(parse(inp.value)); });
    if (money) inp.addEventListener('blur', function () { var n = parse(inp.value); if (isFinite(n)) inp.value = nf0.format(n); });
    box.appendChild(inp); if (unit) box.appendChild(el('span', 'nli__unit', esc(unit))); w.appendChild(box);
    if (help) w.appendChild(el('span', 'nli__help', help));
    var err = el('span', 'nli__err'); err.setAttribute('aria-live', 'polite'); w.appendChild(err); w._err = err;
    return w;
  }
  function seg(label, opts, cur, on) {
    var w = el('div', 'nli__f'); w.appendChild(el('span', 'nli__lab', esc(label)));
    var g = el('div', 'nli__seg'); g.setAttribute('role', 'group'); g.setAttribute('aria-label', label);
    opts.forEach(function (o) { var bt = el('button', '', esc(o[1])); bt.type = 'button'; bt.setAttribute('aria-pressed', String(o[0] === cur));
      bt.addEventListener('click', function () { [].forEach.call(g.children, function (x) { x.setAttribute('aria-pressed', String(x === bt)); }); on(o[0]); }); g.appendChild(bt); });
    w.appendChild(g); return w;
  }
  var ICON = {
    copy: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 7h9v10H7z"/><path d="M4 13V3h9"/></svg>',
    wa: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16l1-3.2A7 7 0 1 1 7.6 15z"/></svg>',
    print: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 8V3h10v5"/><path d="M5 14H3V8h14v6h-2"/><path d="M6 12h8v5H6z"/></svg>'
  };
  function nearUrl(root) {
    var a = root.getAttribute('data-nli-near'); if (a) return a;
    return /(^|\.)nad-lan\.co\.il$/.test(location.hostname) ? '/wp-json/nadlan/v1/near-finder' : 'https://nad-lan.co.il/wp-json/nadlan/v1/near-finder';
  }

  NI.register('mbudget', {
    custom: function (root, data) {
      var D = { boim: data.boim, ptax: data.ptax, cost: data.cost };
      if (!D.boim || !sysRow(D.boim) || !D.boim.homes || !D.boim.homes.payments || !D.ptax || !D.cost) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
      if (!W.NLAF) {
        if (!AFF) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
        var sc = document.createElement('script'); sc.src = AFF;
        sc.onload = function () { if (W.NLAF) build(root, D); };
        sc.onerror = function () { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; };
        document.head.appendChild(sc); return;
      }
      build(root, D);
    }
  });

  function build(root, D) {
    css();
    var v = { income: 22000, equity: 600000, track: 'single', loans: 0, ratio: 33, years: 25 }, eg = true, rooms = null, last = null, lastCs = null;  // rooms: null = the best fit, a number once picked
    try { var set = JSON.parse(root.getAttribute('data-nli-set') || '{}'); Object.keys(set).forEach(function (k) { if (k in v) { v[k] = k === 'track' ? String(set[k]) : +set[k]; eg = false; } }); } catch (e) {}
    var near = { st: 'loading', data: null };
    root.innerHTML = ''; if (!root.parentNode || !root.parentNode.closest || !root.parentNode.closest('.nli')) root.classList.add('nli'); root.setAttribute('dir', 'rtl');
    var panel = el('div', 'nli__panel nlmb');
    panel.appendChild(el('p', 'nli__kicker', 'מחשבון · מהמשכנתא לדירה'));
    panel.appendChild(el('h2', 'nli__title', 'כמה דירה זה קונה, ואיפה'));
    panel.appendChild(el('p', 'nli__lede', 'הכנסה, הון עצמי וסוג הרכישה. מקבלים את מחיר הדירה הגבוה ביותר שעובר את שתי המגבלות של בנק ישראל, את הערים שבהן דירה במחיר החציוני נכנסת בסכום הזה, ואת הדירות למכירה באתר עד המחיר הזה.'));
    var grid = el('div', 'nli__grid'), form = el('form', 'nli__form'), out = el('div', 'nli__out');
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    out.setAttribute('aria-live', 'polite');
    var t = 0;
    function change(k, x) { v[k] = x; eg = false; clearTimeout(t); t = setTimeout(run, 90); }
    var fIncome = input('income', 'הכנסה נטו של משק הבית', v.income, '₪ בחודש', '', true, function (x) { change('income', x); });
    var fEquity = input('equity', 'הון עצמי', v.equity, '₪', 'כל הכסף לעסקה, כולל מס הרכישה ועורך הדין.', true, function (x) { change('equity', x); });
    form.appendChild(fIncome); form.appendChild(fEquity);
    form.appendChild(seg('סוג הרכישה', [['single', 'דירה יחידה'], ['extra', 'דירה נוספת'], ['oleh', 'עולה חדש'], ['foreign', 'תושב חוץ']], v.track, function (x) { change('track', x); }));
    var two = el('div', 'nlmb__two');
    var fLoans = input('loans', 'הלוואות קיימות', v.loans, '₪ בחודש', 'לא חובה. הבנק מוריד אותן מההחזר.', true, function (x) { change('loans', x); }, 'אין');
    var fRatio = input('ratio', 'חלק מההכנסה להחזר', v.ratio, '%', '', false, function (x) { change('ratio', x); });
    two.appendChild(fLoans); two.appendChild(fRatio); form.appendChild(two);
    form.appendChild(el('span', 'nli__help', 'בנק ישראל לא מתיר החזר של יותר מ־50% מההכנסה הפנויה, ומעל 40% הבנק נדרש להחזיק יותר הון. ' + (D.boim && D.boim.market && D.boim.market.pti_avg ? 'יחס ההחזר הממוצע במשכנתאות החדשות: ' + String(D.boim.market.pti_avg).replace(/(\.\d)\d+$/, '$1') + '% (בנק ישראל, ' + String(D.boim.market.month).split('-').reverse().map(Number).join('.') + ').' : '')));
    form.appendChild(seg('תקופת המשכנתא', [[20, '20 שנה'], [25, '25 שנה'], [30, '30 שנה']], v.years, function (x) { change('years', x); }));
    grid.appendChild(form); grid.appendChild(out); panel.appendChild(grid);

    var sec2 = el('section', 'nlmb__sec'); sec2.setAttribute('aria-label', 'איפה זה נכנס');
    sec2.appendChild(el('h3', 'nlmb__h', 'איפה זה נכנס: דירה במחיר החציוני'));
    var rseg = el('div', 'nli__seg'); rseg.setAttribute('role', 'group'); rseg.setAttribute('aria-label', 'מספר חדרים');
    rseg.addEventListener('click', function (e) { var bt = e.target.closest('button[data-rooms]'); if (!bt) return; rooms = +bt.getAttribute('data-rooms'); paintCities(); });
    var cityBox = el('div', ''); cityBox.setAttribute('aria-live', 'polite');
    sec2.appendChild(rseg); sec2.appendChild(cityBox); panel.appendChild(sec2);

    var sec3 = el('section', 'nlmb__sec'); sec3.setAttribute('aria-label', 'דירות למכירה באתר'); sec3.id = 'nlmb-homes-' + Math.random().toString(36).slice(2, 7);
    var h3 = el('h3', 'nlmb__h', 'דירות למכירה באתר'); sec3.appendChild(h3);
    var homeBox = el('div', ''); homeBox.style.display = 'grid'; homeBox.style.gap = '12px'; homeBox.setAttribute('aria-live', 'polite');
    sec3.appendChild(homeBox); panel.appendChild(sec3);

    var share = el('div', 'nli__share');
    var bc = el('button', 'is-primary', ICON.copy + '<span>העתקת התוצאה</span>'); bc.type = 'button';
    var bw = el('a', '', ICON.wa + '<span>שליחה בוואטסאפ</span>'); bw.target = '_blank'; bw.rel = 'noopener'; bw.href = 'https://wa.me/';
    var bp = el('button', '', ICON.print + '<span>הדפסה או שמירה כקובץ</span>'); bp.type = 'button';
    function curRooms() { return rooms != null ? rooms : bestRooms(lastCs); }
    function txt() { return last ? shareText(last, v, lastCs, curRooms()) + '\n' + location.origin + location.pathname : location.href; }
    bc.addEventListener('click', function () { var tx = txt(), lab = bc.querySelector('span'); var done = function () { lab.textContent = 'הועתק'; setTimeout(function () { lab.textContent = 'העתקת התוצאה'; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(tx).then(done, function () { window.prompt('העתיקו את התוצאה', tx); }); else window.prompt('העתיקו את התוצאה', tx); });
    bw.addEventListener('click', function () { bw.href = 'https://wa.me/?text=' + encodeURIComponent(txt()); });
    bp.addEventListener('click', function () { window.print(); });
    share.appendChild(bc); share.appendChild(bw); share.appendChild(bp); panel.appendChild(share);
    panel.appendChild(el('p', 'nli__eg', '<b>דוגמה</b>הערכים בפתיחה הם דוגמה. שנו אותם, והתוצאה מתעדכנת מיד.'));
    root.appendChild(panel);

    out.addEventListener('click', function (e) { if (e.target.closest('[data-go="homes"]')) { sec3.scrollIntoView({ behavior: 'smooth', block: 'start' }); var a = homeBox.querySelector('a'); if (a) a.focus({ preventScroll: true }); } });

    function paintCities() {
      if (!last) return;
      var r = curRooms();
      rseg.innerHTML = roomsSegHtml(lastCs, r);
      cityBox.innerHTML = citiesHtml(lastCs, r, last, D.boim);
    }
    function paintHomes() {
      if (!last) return;
      h3.innerHTML = 'דירות למכירה באתר עד ' + b(ils(last.price));
      homeBox.innerHTML = homesHtml(near.st === 'ok' ? listings(near.data, last.price, 6) : null, last, near.st);
    }
    function run() {
      [fIncome, fEquity, fLoans, fRatio].forEach(function (f) { f._err.textContent = ''; });
      if (!(v.income > 0)) { fIncome._err.textContent = 'הקלידו את ההכנסה החודשית נטו.'; return; }
      if (!(v.equity >= 0)) { fEquity._err.textContent = 'הקלידו את ההון העצמי.'; return; }
      if (!(v.ratio > 0)) { fRatio._err.textContent = 'בין 1% ל־50% מההכנסה.'; return; }
      if (v.ratio > 50) fRatio._err.textContent = 'בנק ישראל לא מתיר יותר מ־50%. החישוב לפי 50%.';
      var inp = { income: v.income, equity: v.equity, track: v.track, loans: v.loans > 0 ? v.loans : 0, ratio: v.ratio, years: v.years };
      try { last = solve(inp, D); lastCs = cities(D.boim, last, inp, D.ptax); }
      catch (e) { out.innerHTML = '<p class="nli__note">לא הצלחנו לחשב עם הערכים האלה.</p>'; return; }
      out.innerHTML = answerHtml(last, inp, D, eg);
      paintCities(); paintHomes();
    }
    run();
    // 1.72.588: the homes on the site are read only when the tool comes into view (the payload is large; the panel may stay hidden)
    function loadNear() {
      var ctl = typeof AbortController !== 'undefined' ? new AbortController() : null, to = setTimeout(function () { if (ctl) ctl.abort(); }, 9000);
      fetch(nearUrl(root), { credentials: 'omit', signal: ctl ? ctl.signal : undefined }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (j) { clearTimeout(to); near = { st: j && j.listings ? 'ok' : 'error', data: j }; paintHomes(); })
        .catch(function () { clearTimeout(to); near = { st: 'error', data: null }; paintHomes(); });
    }
    if (typeof IntersectionObserver === 'undefined') { loadNear(); }
    else { var io = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); loadNear(); } }, { rootMargin: '200px' }); io.observe(root); }
  }
})();
