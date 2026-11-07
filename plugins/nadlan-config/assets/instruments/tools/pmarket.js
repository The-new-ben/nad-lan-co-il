/* NadLan Instruments · pmarket v1 (HAD-681, Ben 7.11.2026): "מחירי הדירות עכשיו" on /apartment-prices/.
   The answer first: did prices rise or fall, the latest national change in a year and against the previous period, the same
   after inflation and the distance from the peak, with the two-month deal period, "זמני" and the source. Then the six CBS
   districts, and the index over time: one year, five years or since 1994, in the prices of the time (nominal) or after
   inflation (real), the country or one district against the country. Data: prices-hub.json (tools/instruments/build_prices_hub.py).
   Math in prices-common.js (window.NLPH). */
(function () {
  'use strict';
  if (!window.NadLanInstruments || !window.NLPH || !window.NLPH.ui) return;
  var NI = window.NadLanInstruments, P = window.NLPH, U = P.ui, esc = U.esc;

  function series(D, id) { if (id === 'il') return { n: 'כל הארץ', from: D.hpi.from, v: D.hpi.v }; for (var i = 0; i < D.dist.length; i++) if (D.dist[i].id === id) return { n: D.dist[i].n, from: D.dist[i].from, v: D.dist[i].v, dist: true }; return null; }

  function answer(D) {
    var H = { from: D.hpi.from, v: D.hpi.v }, C = D.cpi, x = P.hpiAt(H, C), prev = P.addM(x.k, -1);
    var lead = x.yoy == null ? '' : Math.abs(x.yoy) < 0.0005 ? 'מחירי הדירות בישראל כמעט לא השתנו בשנה האחרונה' : (x.yoy < 0 ? 'כן. מחירי הדירות בישראל ירדו ב־' : 'לא. מחירי הדירות בישראל עלו ב־') + Math.abs(100 * x.yoy).toFixed(1) + '% בשנה';
    var s = '<b>' + esc(lead) + '</b>, לפי מדד מחירי הדירות של הלמ״ס לעסקאות של ' + esc(P.dealLabel(x.k)) + ' (נתון זמני, פורסם ב' + esc(P.pubLabel(x.k)) + '). ';
    if (x.mom != null) s += 'מול התקופה הקודמת (' + esc(P.dealLabel(prev)) + ') המדד ' + esc(U.word(x.mom, 'עלה', 'ירד', 'לא השתנה')) + (Math.abs(x.mom) >= 0.0005 ? ' ב־' + Math.abs(100 * x.mom).toFixed(1) + '%' : '') + '. ';
    if (x.real != null && Math.abs(x.real) >= 0.0005) s += 'אחרי האינפלציה, ' + (x.real < 0 ? 'הירידה' : 'העלייה') + ' בשנה היא ' + Math.abs(100 * x.real).toFixed(1) + '%. ';
    if (x.fromPeak < -0.0005) s += 'המדד נמצא ' + Math.abs(100 * x.fromPeak).toFixed(1) + '% מתחת לשיא של ' + esc(P.dealLabel(x.peakK)) + '.';
    return { x: x, html: s, text: lead + ' (' + P.dealLabel(x.k) + ', הלמ״ס, זמני).' + (x.mom != null ? ' מול התקופה הקודמת: ' + U.pctTxt(x.mom) + '.' : '') + (x.real != null ? ' אחרי אינפלציה: ' + U.pctTxt(x.real) + '.' : '') };
  }

  function chart(box, D, st) {
    var C = D.cpi, S = series(D, st.s), end = P.lastKey(S);
    var from = st.r === '1' ? P.addM(end, -12) : st.r === '5' ? P.addM(end, -60) : S.from;
    if (P.mIndex(S.from, from) < 0) from = S.from;
    var A = P.window(S, C, from, end, st.real), B = S.dist ? P.window({ from: D.hpi.from, v: D.hpi.v }, C, from, end, st.real) : null;
    var W = Math.max(280, Math.min(1000, Math.round(box.clientWidth || 640) - 20)), Hh = W < 520 ? 210 : 260, L = 46, R = W < 520 ? 52 : 64, T = 14, Bm = 26;
    var all = A.map(function (p) { return p.x; }).concat(B ? B.map(function (p) { return p.x; }) : []).concat([100]);
    var lo = Math.min.apply(null, all), hi = Math.max.apply(null, all), pad = Math.max(1, (hi - lo) * 0.08); lo -= pad; hi += pad;
    var X = function (i) { return L + i * (W - L - R) / Math.max(1, A.length - 1); }, Y = function (v) { return T + (hi - v) * (Hh - T - Bm) / (hi - lo); };
    var span = hi - lo, step = [1, 2, 5, 10, 20, 25, 50, 100, 200].filter(function (s) { return span / s <= 6; })[0] || 500;
    var o = '<svg viewBox="0 0 ' + W + ' ' + Hh + '" role="img" aria-label="' + esc(S.n + ': ' + (st.real ? 'אחרי אינפלציה, ' : '') + 'שינוי מאז ' + P.dealLabel(A[0].k) + ' ' + U.pctTxt(A[A.length - 1].x / 100 - 1)) + '">';
    for (var g = Math.ceil((lo - 100) / step) * step; g <= hi - 100; g += step) { var gy = Y(100 + g); o += '<line class="' + (g === 0 ? 'z' : 'g') + '" x1="' + L + '" x2="' + (W - R) + '" y1="' + gy.toFixed(1) + '" y2="' + gy.toFixed(1) + '"/><text x="' + (L - 6) + '" y="' + (gy + 4).toFixed(1) + '" text-anchor="end">' + (g > 0 ? '+' : g < 0 ? '−' : '') + Math.abs(g) + '%</text>'; }
    // x labels: years on long ranges, months on one year
    var every = A.length > 200 ? 60 : A.length > 40 ? 12 : 3;
    A.forEach(function (p, i) { var m = +p.k.slice(5, 7); if ((every >= 12 ? m === 1 && (+p.k.slice(0, 4)) % (every / 12) === 0 : i % every === 0)) o += '<text x="' + X(i).toFixed(1) + '" y="' + (Hh - 6) + '" text-anchor="middle">' + (every >= 12 ? p.k.slice(0, 4) : p.k.slice(5, 7) + '.' + p.k.slice(2, 4)) + '</text>'; });
    var path = function (pts) { return pts.map(function (p, i) { return (i ? 'L' : 'M') + X(i).toFixed(1) + ' ' + Y(p.x).toFixed(1); }).join(''); };
    o += '<path class="ar" d="' + path(A) + 'L' + X(A.length - 1).toFixed(1) + ' ' + Y(100).toFixed(1) + 'L' + X(0).toFixed(1) + ' ' + Y(100).toFixed(1) + 'Z"/>';
    if (B && B.length === A.length) o += '<path class="ln2" d="' + path(B) + '"/>';
    o += '<path class="ln" d="' + path(A) + '"/>';
    var lx = X(A.length - 1), ly = Y(A[A.length - 1].x);
    o += '<circle class="end" cx="' + lx.toFixed(1) + '" cy="' + ly.toFixed(1) + '" r="4.5"/><text class="endl" x="' + (lx + 8).toFixed(1) + '" y="' + (ly + 4).toFixed(1) + '">' + U.pctTxt(A[A.length - 1].x / 100 - 1) + '</text>';
    o += '<line class="cur" x1="0" x2="0" y1="' + T + '" y2="' + (Hh - Bm) + '" visibility="hidden"/><rect x="' + L + '" y="0" width="' + (W - L - R) + '" height="' + Hh + '" fill="transparent" class="hit"/></svg>';
    box.innerHTML = o;
    var svg = box.querySelector('svg'), cur = svg.querySelector('.cur'), tip = U.el('div', 'nlph-tip'); tip.hidden = true; box.appendChild(tip);
    function show(ev) {
      var r = svg.getBoundingClientRect(), sx = (ev.clientX - r.left) * W / r.width, i = Math.max(0, Math.min(A.length - 1, Math.round((sx - L) / ((W - L - R) / Math.max(1, A.length - 1))))), p = A[i];
      cur.setAttribute('x1', X(i)); cur.setAttribute('x2', X(i)); cur.setAttribute('visibility', 'visible');
      tip.innerHTML = '<b>' + esc(P.dealLabel(p.k)) + '</b><span>' + esc((S.dist ? S.n : 'כל הארץ') + ' · מדד ' + p.v.toFixed(1)) + '</span><span>' + esc((st.real ? 'ריאלי ' : '') + U.pctTxt(p.x / 100 - 1) + ' מ' + P.monLabel(A[0].k)) + '</span>';
      tip.hidden = false; var bx = box.getBoundingClientRect(), tx = ev.clientX - bx.left, w = tip.offsetWidth;
      tip.style.left = Math.max(4, Math.min(bx.width - w - 4, tx - w / 2)) + 'px'; tip.style.top = Math.max(0, (Y(p.x) * r.height / Hh) - tip.offsetHeight - 14) + 'px';
    }
    svg.addEventListener('pointermove', show); svg.addEventListener('pointerdown', show);
    svg.addEventListener('pointerleave', function () { tip.hidden = true; cur.setAttribute('visibility', 'hidden'); });
    return { first: A[0], last: A[A.length - 1], nat: B ? B[B.length - 1] : null, n: S.n, dist: !!S.dist, from: from };
  }

  NI.register('pmarket', {
    custom: function (root, D0) {
      var D = D0.phub || D0.d0; U.css();
      if (!root.closest('.nli')) root.classList.add('nli');
      root.setAttribute('dir', 'rtl'); root.innerHTML = '';
      var panel = U.el('div', 'nli__panel nlph'); root.appendChild(panel);
      panel.appendChild(U.el('p', 'nli__kicker', 'מדד · הלשכה המרכזית לסטטיסטיקה'));
      panel.appendChild(U.el('h2', 'nli__title', 'מחירי הדירות עכשיו'));
      var A = answer(D), x = A.x;
      var box = U.el('div', 'nlph-ans'); box.setAttribute('aria-live', 'polite');
      box.innerHTML = '<div class="nlph-ans__head"><span>האם מחירי הדירות ירדו?</span><small>' + esc(P.dealLabel(x.k)) + ' · זמני</small></div><p class="nlph-ans__a">' + A.html + '</p>' +
        '<div class="nlph-kpis">' +
        '<div><span>בשנה</span><strong class="' + (x.yoy < 0 ? 'is-dn' : 'is-up') + '">' + U.pctTxt(x.yoy) + '</strong><small>מול ' + esc(P.dealLabel(P.addM(x.k, -12))) + '</small></div>' +
        '<div><span>מול התקופה הקודמת</span><strong class="' + (x.mom < 0 ? 'is-dn' : 'is-up') + '">' + U.pctTxt(x.mom) + '</strong><small>מול ' + esc(P.dealLabel(P.addM(x.k, -1))) + '</small></div>' +
        '<div><span>בשנה, אחרי אינפלציה</span><strong class="' + (x.real < 0 ? 'is-dn' : 'is-up') + '">' + U.pctTxt(x.real) + '</strong><small>לפי מדד המחירים לצרכן</small></div>' +
        '<div><span>מהשיא</span><strong class="is-dn">' + U.pctTxt(x.fromPeak) + '</strong><small>שיא: ' + esc(P.dealLabel(x.peakK)) + '</small></div></div>';
      panel.appendChild(box);

      /* the districts */
      var sec = U.el('section', 'nlph-sec'); panel.appendChild(sec);
      sec.appendChild(U.el('h3', 'nlph-h', 'מחירי הדירות לפי מחוז'));
      var rows = [{ id: 'il', n: 'כל הארץ' }].concat(D.dist.map(function (d) { return { id: d.id, n: 'מחוז ' + d.n }; })).map(function (r) {
        var S = series(D, r.id), k = P.lastKey(S), v = P.at(S, k);
        return { id: r.id, n: r.n, k: k, yoy: P.chg(v, P.at(S, P.addM(k, -12))), mom: P.chg(v, P.at(S, P.addM(k, -1))), y5: P.chg(v, P.at(S, P.addM(k, -60))), real: P.realChg(v, P.at(S, P.addM(k, -12)), P.cpiDeal(D.cpi, k), P.cpiDeal(D.cpi, P.addM(k, -12))) };
      });
      var nat = rows.shift(); rows.sort(function (a, b) { return a.yoy - b.yoy; });
      var fell = rows.filter(function (r) { return r.yoy < -0.0005; }).length;
      sec.appendChild(U.el('p', 'nlph-sub', esc('בעסקאות של ' + P.dealLabel(x.k) + ', המדד ' + (fell === rows.length ? 'ירד בכל ששת המחוזות' : fell ? 'ירד ב־' + fell + ' מתוך ' + rows.length + ' מחוזות' : 'לא ירד באף מחוז') + ' לעומת שנה קודם. מהירידה הגדולה לקטנה:')));
      var tr = function (r, cls) { return '<tr' + (cls ? ' class="' + cls + '"' : '') + '><th scope="row">' + esc(r.n) + '</th><td class="n">' + U.pct(r.yoy) + '</td><td class="n">' + U.pct(r.real) + '</td><td class="n">' + U.pct(r.mom) + '</td><td class="n nlph-dk">' + U.pct(r.y5, 0) + '</td></tr>'; };
      var tw = U.el('div', 'nlph-tw');
      tw.innerHTML = '<table class="nlph-t"><caption>מדד מחירי הדירות לפי מחוז, עסקאות ' + esc(P.dealLabel(x.k)) + ' (זמני). הלמ״ס.</caption><thead><tr><th scope="col">אזור</th><th scope="col" class="n">בשנה</th><th scope="col" class="n">אחרי אינפלציה</th><th scope="col" class="n">מול התקופה הקודמת</th><th scope="col" class="n nlph-dk">ב־5 שנים</th></tr></thead><tbody>' +
        tr(nat, 'is-nat') + rows.map(function (r) { return tr(r); }).join('') + '</tbody></table>';
      sec.appendChild(tw);

      /* the index over time */
      var cs = U.el('section', 'nlph-sec'); panel.appendChild(cs);
      cs.appendChild(U.el('h3', 'nlph-h', 'מדד מחירי הדירות: גרף מ־1994 ועד היום'));
      var st = { r: '5', real: false, s: 'il' };
      try { var pre = JSON.parse(root.getAttribute('data-nli-set') || '{}'); if (pre.period && /^(1|5|all)$/.test(pre.period)) st.r = pre.period; if (pre.view === 'real') st.real = true; if (pre.region && series(D, pre.region)) st.s = pre.region; } catch (e) {}
      var ctl = U.el('div', 'nlph-ctl'); cs.appendChild(ctl);
      function tabs(label, opts, get, set, sea) {
        var g = U.el('div', 'nlph-tabs' + (sea ? ' is-sea' : '')); g.setAttribute('role', 'group'); g.setAttribute('aria-label', label);
        g.appendChild(U.el('span', 'lab', esc(label)));
        opts.forEach(function (o) { var b = U.el('button', '', esc(o[1])); b.type = 'button'; b.setAttribute('aria-pressed', String(get() === o[0]));
          b.addEventListener('click', function () { set(o[0]); [].forEach.call(g.querySelectorAll('button'), function (z) { z.setAttribute('aria-pressed', String(z === b)); }); draw(); }); g.appendChild(b); });
        return g;
      }
      ctl.appendChild(tabs('תקופה', [['1', 'שנה'], ['5', '5 שנים'], ['all', 'מ־1994']], function () { return st.r; }, function (v) { st.r = v; }));
      ctl.appendChild(tabs('מחירים', [[false, 'במחירי אותה תקופה'], [true, 'אחרי אינפלציה']], function () { return st.real; }, function (v) { st.real = v; }, true));
      var sel = U.el('div', 'nli__f'); var lab = U.el('label', '', 'אזור'); lab.htmlFor = 'nlph-s-' + Math.random().toString(36).slice(2, 7); sel.appendChild(lab);
      var ib = U.el('div', 'nli__in'); var s = document.createElement('select'); s.id = lab.htmlFor;
      [['il', 'כל הארץ']].concat(D.dist.map(function (d) { return [d.id, 'מחוז ' + d.n]; })).forEach(function (o) { var op = U.el('option', '', esc(o[1])); op.value = o[0]; if (o[0] === st.s) op.selected = true; s.appendChild(op); });
      s.addEventListener('change', function () { st.s = s.value; draw(); }); ib.appendChild(s); sel.appendChild(ib); sel.style.minWidth = '180px'; ctl.appendChild(sel);
      var cbox = U.el('div', 'nlph-chart'); cs.appendChild(cbox);
      var key = U.el('ul', 'nlph-key'); cs.appendChild(key);
      var say = U.el('p', 'nlph-sub'); say.setAttribute('aria-live', 'polite'); say.style.marginTop = '10px'; cs.appendChild(say);
      function draw() {
        var c = chart(cbox, D, st), ch = c.last.x / 100 - 1;
        key.innerHTML = '<li><i></i>' + esc(c.n) + (st.real ? ', אחרי אינפלציה' : '') + '</li>' + (c.dist ? '<li><i class="d"></i>כל הארץ, לשם השוואה</li>' : '') + '<li>0% = ' + esc(P.monLabel(c.first.k)) + '</li>';
        say.innerHTML = '<b>' + esc(c.n) + '</b>: ' + esc(U.word(ch, 'עלייה של ', 'ירידה של ', 'בלי שינוי')) + (Math.abs(ch) >= 0.0005 ? Math.abs(100 * ch).toFixed(1) + '%' : '') + esc(' מ' + P.dealLabel(c.first.k) + ' ועד ' + P.dealLabel(c.last.k) + (st.real ? ', אחרי אינפלציה' : ', במחירי אותה תקופה') + '.') +
          (c.nat ? ' ' + esc('כל הארץ באותה תקופה: ' + U.pctTxt(c.nat.x / 100 - 1) + '.') : '') + (c.dist && st.r === 'all' ? ' ' + esc('המדדים לפי מחוז מתחילים ב' + P.monLabel(c.from) + '.') : '');
      }
      draw();
      var rt = 0; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(draw, 150); });
      panel.appendChild(U.el('p', 'nlph-fine', esc('איך מחשבים: הלמ״ס מפרסמת את מדד מחירי הדירות לתקופות של חודשיים, לפי העסקאות שדווחו לרשות המסים, ומעדכנת את החודשים האחרונים בכל פרסום. השינוי בשנה הוא המדד של התקופה חלקי המדד של אותה תקופה שנה קודם. אחרי אינפלציה: אותו חישוב אחרי חלוקה במדד המחירים לצרכן של אותם חודשים. מדד מחירי הדירות אינו חלק ממדד המחירים לצרכן. החישובים שלנו.')));
      var src = U.el('p', 'nli__src'); src.innerHTML = U.srcs([{ label: D.hpi.src.he + ', נקרא ' + F_date(D.hpi.src.read), url: D.hpi.src.url }, { label: D.cpi.src.he, url: D.cpi.src.url }]); panel.appendChild(src);
      panel.appendChild(U.share(function () { return A.text; }));
    }
  });
  function F_date(iso) { var p = String(iso).split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : iso; }
})();
