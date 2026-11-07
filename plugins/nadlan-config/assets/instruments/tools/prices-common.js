/* NadLan Instruments · prices-common v1 (HAD-681, Ben 7.11.2026): the shared math, labels and styles of the three tools of
   /apartment-prices/ (pmarket, pcity, panatomy). Loaded first through 'deps' => prices-common in the registry.
   Pure logic in window.NLPH (no DOM), so tools/instruments/test_prices_hub.js checks every formula in Node:
   - the CBS dwelling index: the API month M is the deals of M and M+1 (two-month periods), published about the 15th of M+3;
     change against the previous period and against the same period a year earlier; the real change deflates by the CPI of
     the same two months (their average);
   - the city medians: the latest published quarter, the same quarter a year earlier, the change since 1-3.2021 and the real
     change since then (the CPI average of each quarter's three months);
   - the monthly mortgage payment: Bank of Israel effective rate turned nominal (1200 x ((1 + e/100)^(1/12) - 1)), Spitzer;
   - the purchase tax by brackets (ptax.json), the gross yield, the VAT inside a price.
   Design: the engine's identity (NadLan Instruments: sea #2F6F86, ink #12202A, ground #F6F8F9; Karantina, IBM Plex Sans Hebrew,
   IBM Plex Mono). Survey ruling, figures in mono, no shadows, no cream. */
(function () {
  'use strict';
  var HM = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
  function ym(k) { var p = String(k).split('-'); return [+p[0], +p[1]]; }
  function key(y, m) { while (m > 12) { m -= 12; y++; } while (m < 1) { m += 12; y--; } return y + '-' + (m < 10 ? '0' : '') + m; }
  function addM(k, d) { var a = ym(k); return key(a[0], a[1] + d); }
  function mIndex(from, k) { var a = ym(from), b = ym(k); return (b[0] - a[0]) * 12 + (b[1] - a[1]); }
  function lastKey(S) { return addM(S.from, S.v.length - 1); }
  function at(S, k) { var i = mIndex(S.from, k); return i >= 0 && i < S.v.length && S.v[i] != null ? S.v[i] : null; }
  /* the CPI of a two-month deal period (M and M+1); M alone when M+1 is not out yet */
  function cpiDeal(C, k) { var a = at(C, k), b = at(C, addM(k, 1)); return a == null ? null : (b == null ? a : (a + b) / 2); }
  function chg(a, b) { return a == null || b == null || !b ? null : a / b - 1; }
  function realChg(pa, pb, ca, cb) { return pa == null || pb == null || ca == null || cb == null || !pb || !cb ? null : (pa / pb) / (ca / cb) - 1; }
  /* the dwelling index at month k (default: the latest): value, the change against the previous period and a year earlier, real */
  function hpiAt(H, C, k) {
    k = k || lastKey(H);
    var v = at(H, k), p = at(H, addM(k, -1)), y = at(H, addM(k, -12));
    var o = { k: k, v: v, mom: chg(v, p), yoy: chg(v, y), real: realChg(v, y, cpiDeal(C, k), cpiDeal(C, addM(k, -12))) };
    // the peak of the last 5 years and the distance from it
    var best = null, bk = null;
    for (var i = 1; i <= 60; i++) { var kk = addM(k, -i), x = at(H, kk); if (x != null && (best == null || x > best)) { best = x; bk = kk; } }
    o.peak = best; o.peakK = bk; o.fromPeak = best != null && best > v ? v / best - 1 : 0;
    return o;
  }
  /* a series from month a to month b, rebased to 100 at a; real: deflated by the deal-period CPI */
  function window_(S, C, a, b, real) {
    var out = [], i0 = Math.max(0, mIndex(S.from, a)), i1 = Math.min(S.v.length - 1, mIndex(S.from, b)), base = null, cb = null;
    for (var i = i0; i <= i1; i++) {
      var k = addM(S.from, i), v = S.v[i]; if (v == null) continue;
      var c = real ? cpiDeal(C, k) : 1; if (c == null) continue;
      var r = v / c; if (base == null) { base = r; cb = k; }
      out.push({ k: k, v: v, x: 100 * r / base });
    }
    return out;
  }
  /* quarters: '1-3.2026' */
  function qMonths(q) { var p = String(q).split('.'), a = p[0].split('-'), y = +p[1], o = []; for (var m = +a[0]; m <= +a[1]; m++) o.push(key(y, m)); return o; }
  function qEnd(q) { var m = qMonths(q); return m[m.length - 1]; }
  function cpiQ(C, q) { var s = 0, n = 0; qMonths(q).forEach(function (k) { var x = at(C, k); if (x != null) { s += x; n++; } }); return n ? s / n : null; }
  function lastIdx(arr) { for (var i = arr.length - 1; i >= 0; i--) if (arr[i] != null) return i; return -1; }
  /* one city and room count: the latest published quarter, the change against the same quarter a year earlier, the change since
     the first quarter of the series (1-3.2021) and the same change after inflation */
  function cityStat(arr, Q, C) {
    var i = lastIdx(arr || []); if (i < 0) return null;
    var v = arr[i], y = i >= 4 ? arr[i - 4] : null, b = arr[0];
    return { i: i, q: Q[i], v: v, yoy: chg(v, y), since: chg(v, b), real: b == null ? null : realChg(v, b, cpiQ(C, Q[i]), cpiQ(C, Q[0])), baseQ: Q[0] };
  }
  /* rent of the same quarter as the price, never another one */
  function rentAt(rent, rooms, q) { var r = rent && rent['r' + rooms]; if (!r) return null; var x = r[qEnd(q)]; return x == null ? null : x; }
  function ef2nom(e) { return 1200 * (Math.pow(1 + e / 100, 1 / 12) - 1); }
  function pmt(P, nom, n) { var r = nom / 1200; return n <= 0 ? 0 : (r === 0 ? P / n : P * r / (1 - Math.pow(1 + r, -n))); }
  function payment(price, ltv, eff, years) { var loan = price * ltv, nom = ef2nom(eff); return { loan: loan, nom: nom, pay: pmt(loan, nom, Math.round(years * 12)) }; }
  function ptax(price, br) { var t = 0, lo = 0, parts = []; for (var i = 0; i < br.length; i++) { var hi = br[i][0] == null ? Infinity : br[i][0], top = Math.min(price, hi); if (top > lo) { t += (top - lo) * br[i][1]; parts.push({ from: lo, to: top, rate: br[i][1], tax: (top - lo) * br[i][1] }); } if (price <= hi) break; lo = hi; } return { tax: t, parts: parts }; }
  function grossYield(rent, price) { return rent && price ? rent * 12 / price : null; }
  function vatIn(price, vat) { return price * vat / (1 + vat); }
  /* labels */
  function monLabel(k) { var a = ym(k); return HM[a[1] - 1] + ' ' + a[0]; }
  function dealLabel(k) { var a = ym(k), b = ym(addM(k, 1)); return a[0] === b[0] ? HM[a[1] - 1] + ' ו' + HM[b[1] - 1] + ' ' + a[0] : HM[a[1] - 1] + ' ' + a[0] + ' ו' + HM[b[1] - 1] + ' ' + b[0]; }
  function pubLabel(k) { return 'אמצע ' + monLabel(addM(k, 3)); }
  function qLabel(q) { var m = qMonths(q), a = ym(m[0]), b = ym(m[m.length - 1]); return HM[a[1] - 1] + ' עד ' + HM[b[1] - 1] + ' ' + a[0]; }
  function qShort(q) { var p = String(q).split('.'); return 'רבעון ' + ({ '1-3': 1, '4-6': 2, '7-9': 3, '10-12': 4 }[p[0]] || p[0]) + ' ' + p[1]; }
  /* months of the official average wage per apartment (gross monthly wage; null without a wage) */
  function salaries(price, wage) { return price && wage && wage.v ? price / wage.v : null; }
  /* the city x rooms table as CSV rows: a source line, a header row, then the country and the 24 cities (raw numbers, % with 1 decimal) */
  function csvRows(D, today) {
    var R = [['3', '3 חדרים'], ['4', '4 חדרים'], ['5', '5 חדרים'], ['a', 'כל הדירות']], p = function (x) { return x == null ? '' : (100 * x).toFixed(1); };
    var head = ['עיר'];
    R.forEach(function (r) { head.push('חציון ' + r[1] + ' (₪)', 'רבעון ' + r[1], 'שינוי בשנה ' + r[1] + ' (%)', 'מתחילת 2021 ' + r[1] + ' (%)', 'מתחילת 2021 אחרי אינפלציה ' + r[1] + ' (%)'); });
    if (D.wage) head.push('משכורות ממוצעות לדירת 4 חדרים');
    var src = 'מחירי דירות לפי עיר וחדרים: חציון העסקאות שדווחו לרשות המסים (אתר הנדל״ן הממשלתי, קובץ ' + D.vsrc.version + ', נקרא ' + D.vsrc.read + '); אחרי אינפלציה לפי מדד המחירים לצרכן של הלמ״ס' +
      (D.wage ? '; שכר ממוצע ' + D.wage.v + ' ₪ (הביטוח הלאומי, סעיף 1, מ־' + D.wage.from + ')' : '') + '; החישובים: nad-lan.co.il/apartment-prices/' + (today ? ', ' + today : '');
    var rows = [[src], head];
    [{ n: 'כל הארץ', r3: D.il.r3, r4: D.il.r4, r5: D.il.r5, ra: D.il.ra }].concat(D.city).forEach(function (c) {
      var row = [c.n];
      R.forEach(function (r) { var s = cityStat(c[r[0] === 'a' ? 'ra' : 'r' + r[0]], D.q, D.cpi); row.push(s ? s.v : '', s ? s.q : '', p(s && s.yoy), p(s && s.since), p(s && s.real)); });
      if (D.wage) { var s4 = cityStat(c.r4, D.q, D.cpi); row.push(s4 ? salaries(s4.v, D.wage).toFixed(0) : ''); }
      rows.push(row);
    });
    return rows;
  }
  function toCSV(rows) { return '﻿' + rows.map(function (r) { return r.map(function (v) { v = String(v == null ? '' : v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(','); }).join('\r\n') + '\r\n'; }
  /* the map: an equirectangular projection of a lat/lon box into a W x H frame (north up, cos(lat) for the east-west scale) */
  function proj(box, W, H, pad) {
    var k = Math.cos((box.s + box.n) / 2 * Math.PI / 180), dx = (box.e - box.w) * k, dy = box.n - box.s, s = Math.min((W - 2 * pad.x) / dx, (H - 2 * pad.y) / dy);
    var ox = (W - dx * s) / 2, oy = (H - dy * s) / 2;
    return function (lat, lon) { return [ox + (lon - box.w) * k * s, oy + (box.n - lat) * s]; };
  }
  /* callout labels in two gutters (west = left, east = right): sorted by height, pushed apart to at least `gap`, kept inside 0..H */
  function callouts(pts, H, gap, split) {
    var out = [];
    ['L', 'R'].forEach(function (side) {
      var g = pts.filter(function (p) { return (p.lon < split) === (side === 'L'); }).map(function (p) { return { id: p.id, x: p.x, y: p.y, side: side, ly: p.y }; }).sort(function (a, b) { return a.y - b.y; });
      for (var i = 0; i < g.length; i++) { g[i].ly = Math.max(gap / 2 + 2, i ? Math.max(g[i].ly, g[i - 1].ly + gap) : g[i].ly); }
      for (var j = g.length - 1; j >= 0; j--) { var lim = j === g.length - 1 ? H - gap / 2 - 2 : g[j + 1].ly - gap; if (g[j].ly > lim) g[j].ly = lim; }
      out = out.concat(g);
    });
    return out;
  }
  window.NLPH = { HM: HM, addM: addM, salaries: salaries, csvRows: csvRows, toCSV: toCSV, proj: proj, callouts: callouts, mIndex: mIndex, lastKey: lastKey, at: at, cpiDeal: cpiDeal, chg: chg, realChg: realChg, hpiAt: hpiAt, window: window_,
    qMonths: qMonths, qEnd: qEnd, cpiQ: cpiQ, lastIdx: lastIdx, cityStat: cityStat, rentAt: rentAt, ef2nom: ef2nom, pmt: pmt, payment: payment,
    ptax: ptax, grossYield: grossYield, vatIn: vatIn, monLabel: monLabel, dealLabel: dealLabel, pubLabel: pubLabel, qLabel: qLabel, qShort: qShort };
  if (!window.NadLanInstruments || typeof document === 'undefined') return;

  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  var nf = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  var U = window.NLPH.ui = {
    esc: esc,
    num: function (n) { return nf.format(Math.round(n || 0)); },
    ils: function (n) { return nf.format(Math.round(n || 0)) + ' ₪'; },
    k: function (n) { return nf.format(Math.round((n || 0) / 1000)); },  // thousands of shekels, for tables
    mil: function (n) { var m = (n || 0) / 1e6; return (m >= 10 ? m.toFixed(1) : m.toFixed(2)).replace(/\.?0+$/, '') + ' מיליון ₪'; },
    /* a signed percent in a bidi-safe box: '+1.8%' / '−1.8%' */
    pct: function (x, d) { if (x == null || !isFinite(x)) return '<span class="nlph-na" title="לא פורסם">·</span>'; var s = Math.abs(x * 100).toFixed(d == null ? 1 : d); var z = +s === 0; return '<bdi class="nlph-n ' + (z ? '' : x > 0 ? 'is-up' : 'is-dn') + '">' + (z ? '' : x > 0 ? '+' : '−') + s + '%</bdi>'; },
    pctTxt: function (x, d) { if (x == null || !isFinite(x)) return ''; var s = Math.abs(x * 100).toFixed(d == null ? 1 : d); return (+s === 0 ? '' : x > 0 ? '+' : '−') + s + '%'; },
    word: function (x, up, dn, flat) { return x == null ? '' : Math.abs(x) < 0.0005 ? (flat || 'לא השתנו') : (x > 0 ? up : dn); },
    el: function (tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; },
    srcs: function (list) { return 'מקורות: ' + list.map(function (s) { return s.url ? '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.label) + '</a>' : esc(s.label); }).join(' · '); },
    /* the engine's share bar (copy, WhatsApp), with the tool's own text */
    share: function (getText) {
      var w = U.el('div', 'nli__share');
      var bc = U.el('button', 'is-primary', '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 7h9v10H7z"/><path d="M4 13V3h9"/></svg><span>העתקת הנתונים</span>'); bc.type = 'button';
      bc.addEventListener('click', function () { var t = getText() + '\n' + location.origin + location.pathname, lab = bc.querySelector('span');
        var done = function () { lab.textContent = 'הועתק'; setTimeout(function () { lab.textContent = 'העתקת הנתונים'; }, 1600); };
        if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, function () { window.prompt('העתיקו את הנתונים', t); }); else window.prompt('העתיקו את הנתונים', t); });
      var wa = U.el('a', '', '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16l1-3.2A7 7 0 1 1 7.6 15z"/></svg><span>שליחה בוואטסאפ</span>'); wa.target = '_blank'; wa.rel = 'noopener'; wa.href = 'https://wa.me/';
      wa.addEventListener('click', function () { wa.href = 'https://wa.me/?text=' + encodeURIComponent(getText() + '\n' + location.origin + location.pathname); });
      w.appendChild(bc); w.appendChild(wa); return w;
    },
    seg: function (label, opts, cur, on) {
      var w = U.el('div', 'nli__f'); w.appendChild(U.el('span', 'nli__lab', esc(label)));
      var g = U.el('div', 'nli__seg'); g.setAttribute('role', 'group'); g.setAttribute('aria-label', label);
      opts.forEach(function (o) { var b = U.el('button', '', esc(o.label)); b.type = 'button'; b.setAttribute('aria-pressed', String(o.value === cur)); b.setAttribute('data-v', o.value);
        b.addEventListener('click', function () { [].forEach.call(g.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); on(o.value); }); g.appendChild(b); });
      w.appendChild(g); return w;
    },
    css: function () {
      if (document.getElementById('nlph-css')) return;
      var s = document.createElement('style'); s.id = 'nlph-css';
      s.textContent = [
        '.nlph{--ph-up:#1F4B5C;--ph-dn:#B3203F;--ph-paper:#F6F8F9;--ph-tint:#E6F0F3}',
        '.nlph bdi.nlph-n{font-family:var(--nli-mono);font-variant-numeric:tabular-nums;direction:ltr;unicode-bidi:isolate;white-space:nowrap}',
        '.nlph .is-up{color:var(--ph-up)}.nlph .is-dn{color:var(--ph-dn)}.nlph .nlph-na{color:var(--nli-mute)}',
        'html body .nli .nlph h3.nlph-h{font:600 19px/26px var(--nli-sans) !important;color:var(--nli-ink) !important;margin:0 0 6px !important;letter-spacing:0;text-transform:none;position:relative}',
        '.nlph-sub{font:400 14px/22px var(--nli-sans);color:var(--nli-ink2);margin:0 0 10px;max-width:72ch;position:relative}',
        '.nlph-sec{margin:26px 0 0;position:relative;min-width:0}',
        /* answer box */
        '.nlph-ans{border:1px solid var(--nli-ink);border-radius:var(--nli-r-s);background:var(--nli-surface);position:relative;overflow:hidden}',
        '.nlph-ans__head{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;justify-content:space-between;padding:10px 14px;background:var(--nli-ink);color:#fff}',
        '.nlph-ans__head span{font:500 13px/18px var(--nli-sans);letter-spacing:.02em}.nlph-ans__head small{font:400 12px/16px var(--nli-mono);color:#C9D6DD}',
        '.nlph-ans__a{margin:0;padding:14px 14px 4px;font:400 17px/28px var(--nli-sans);color:var(--nli-ink)}.nlph-ans__a b{font-weight:600}',
        '.nlph-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--nli-line);margin-top:12px}',
        '.nlph-kpis div{padding:10px 14px 12px;border-inline-start:1px solid var(--nli-line);display:grid;gap:2px;align-content:start;min-width:0}.nlph-kpis div:first-child{border-inline-start:0}',
        '.nlph-kpis span{font:500 12px/16px var(--nli-sans);color:var(--nli-mute)}',
        '.nlph-kpis strong{font:700 40px/40px var(--nli-display);color:var(--nli-ink);direction:ltr;unicode-bidi:plaintext;text-align:right;letter-spacing:.01em}',
        '.nlph-kpis strong.is-dn{color:var(--ph-dn)}.nlph-kpis strong.is-up{color:var(--ph-up)}',
        '.nlph-kpis small{font:400 12px/16px var(--nli-sans);color:var(--nli-mute)}',
        '@media (max-width:640px){.nlph-kpis{grid-template-columns:1fr 1fr}.nlph-kpis div:nth-child(3){border-inline-start:0}.nlph-kpis div:nth-child(n+3){border-top:1px solid var(--nli-line)}.nlph-kpis strong{font-size:34px;line-height:36px}}',
        '.nlph-tag{display:inline-block;font:500 11px/16px var(--nli-sans);padding:0 6px;border:1px solid currentColor;border-radius:999px;color:var(--nli-survey);margin-inline-start:6px;vertical-align:1px}',
        /* tables */
        '.nlph-tw{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);overflow:hidden}',
        'html body .nli .nlph table.nlph-t{width:100%;border-collapse:collapse;margin:0;font:400 14px/20px var(--nli-sans);display:table !important;table-layout:auto}',
        'html body .nli .nlph table.nlph-t caption{caption-side:top;text-align:right;font:400 12.5px/18px var(--nli-sans);color:var(--nli-mute);padding:8px 10px;background:var(--ph-paper);border-bottom:1px solid var(--nli-line)}',
        'html body .nli .nlph table.nlph-t th,html body .nli .nlph table.nlph-t td{padding:8px 10px !important;border:0 !important;border-bottom:1px solid var(--nli-line) !important;background:none !important;text-align:right;vertical-align:middle;color:var(--nli-ink);font-size:14px !important;line-height:20px !important;width:auto !important}',
        'html body .nli .nlph table.nlph-t thead th{font:500 12.5px/17px var(--nli-sans) !important;color:var(--nli-mute) !important;background:var(--ph-paper) !important;white-space:normal;vertical-align:bottom}',
        'html body .nli .nlph table.nlph-t tbody th{font-weight:500 !important;color:var(--nli-ink) !important}',
        /* the theme turns tables into stacked blocks on phones; a data table stays a table (the core.css guard for .nli__table) */
        'html body .nli .nlph table.nlph-t{display:table !important}html body .nli .nlph table.nlph-t thead{display:table-header-group !important}html body .nli .nlph table.nlph-t tbody{display:table-row-group !important}',
        'html body .nli .nlph table.nlph-t tr{display:table-row !important}html body .nli .nlph table.nlph-t th,html body .nli .nlph table.nlph-t td{display:table-cell !important}html body .nli .nlph table.nlph-t caption{display:table-caption !important}',
        'html body .nli .nlph table.nlph-t td::before,html body .nli .nlph table.nlph-t th::before{content:none !important;display:none !important}',
        'html body .nli .nlph table.nlph-t .nlph-ph{display:none !important}',
        '@media (max-width:600px){html body .nli .nlph table.nlph-t .nlph-dk,html body .nli .nlph .nlph-dk{display:none !important}html body .nli .nlph table.nlph-t .nlph-ph{display:block !important}html body .nli .nlph table.nlph-t th,html body .nli .nlph table.nlph-t td{padding:8px 6px !important;font-size:13.5px !important}}',
        'html body .nli .nlph table.nlph-t td.n{text-align:right;font-family:var(--nli-mono) !important;font-variant-numeric:tabular-nums;white-space:nowrap}html body .nli .nlph table.nlph-t th.n{text-align:right}',
        'html body .nli .nlph table.nlph-t tr:last-child td{border-bottom:0 !important}',
        'html body .nli .nlph table.nlph-t tr.is-nat td{background:var(--ph-tint) !important;font-weight:600}',
        /* buttons */
        'html body .nli .nlph .nlph-tabs{display:flex;flex-wrap:wrap;gap:8px;align-items:center}',
        'html body .nli .nlph .nlph-tabs button{font:500 14px/20px var(--nli-sans);min-height:40px;padding:8px 14px;border:1px solid var(--nli-line);border-radius:999px;background:var(--nli-surface);color:var(--nli-ink2);cursor:pointer;margin:0;box-shadow:none;text-transform:none;letter-spacing:0}',
        'html body .nli .nlph .nlph-tabs button[aria-pressed="true"]{background:var(--nli-ink);border-color:var(--nli-ink);color:#fff}',
        'html body .nli .nlph .nlph-tabs.is-sea button[aria-pressed="true"]{background:var(--nli-sea);border-color:var(--nli-sea)}',
        '.nlph-tabs .lab{font:500 12px/16px var(--nli-sans);color:var(--nli-mute);margin-inline-end:2px}',
        /* chart */
        '.nlph-chart{border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:var(--nli-surface);padding:12px 10px 6px;position:relative;min-width:0}',
        '.nlph-chart svg{display:block;width:100%;height:auto;direction:ltr;overflow:visible}',
        '.nlph-chart .g{stroke:#E3E9ED;stroke-width:1}.nlph-chart .z{stroke:#93A3AE;stroke-width:1}',
        '.nlph-chart text{font:400 11px var(--nli-mono);fill:var(--nli-mute)}',
        '.nlph-chart .ln{fill:none;stroke:var(--nli-sea-deep);stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}',
        '.nlph-chart .ln2{fill:none;stroke:#93A3AE;stroke-width:1.4;stroke-dasharray:4 4}',
        '.nlph-chart .ar{fill:var(--nli-sea);opacity:.08}',
        '.nlph-chart .end{fill:var(--nli-sea-deep);stroke:#fff;stroke-width:2}',
        '.nlph-chart .endl{font:600 13px var(--nli-mono);fill:var(--nli-ink)}',
        '.nlph-chart .cur{stroke:var(--nli-ink);stroke-width:1;stroke-dasharray:2 3}',
        '.nlph-tip{position:absolute;z-index:3;pointer-events:none;background:var(--nli-ink);color:#fff;border-radius:4px;padding:7px 10px;font:400 13px/19px var(--nli-sans);direction:rtl;text-align:right;white-space:nowrap}',
        '.nlph-tip b{font-weight:600;display:block}.nlph-tip span{font-family:var(--nli-mono);direction:ltr;unicode-bidi:plaintext;display:block;text-align:right}',
        '.nlph-key{display:flex;flex-wrap:wrap;gap:6px 16px;margin:6px 4px 2px;padding:0;list-style:none;font:400 12.5px/18px var(--nli-sans);color:var(--nli-ink2)}',
        '.nlph-key li{display:flex;align-items:center;gap:6px;margin:0}.nlph-key i{display:inline-block;width:18px;height:0;border-top:2.2px solid var(--nli-sea-deep)}.nlph-key i.d{border-top:1.4px dashed #93A3AE}',
        '.nlph-ctl{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;margin:0 0 10px}',
        '.nlph-fine{font:400 12.5px/19px var(--nli-sans);color:var(--nli-mute);margin:8px 0 0;position:relative}',
        'html body .nli .nlph-fine a,html body .nli .nlph .nli__src a,html body .nli .nlph a.nlph-a{color:var(--nli-sea) !important;text-decoration:underline;text-underline-offset:3px}',
        '@media print{.nlph-tip,.nlph .nli__share,.nlph .nlph-tabs{display:none !important}}'
      ].join('');
      document.head.appendChild(s);
    }
  };
})();
