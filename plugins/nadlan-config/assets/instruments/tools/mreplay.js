/* NadLan Instruments · mreplay v1 (HAD-675, 5.11.2026): "אם 2022 חוזרת". The real 2022 to 2023 hiking path of the Bank of Israel
   (boi-rate.json, the rate in force at the end of each month from 3.2022, the month before the first hike, to 5.2023, the last
   one) and the CPI of the same months (cbs-120010.json), replayed on the reader's mix (default: the system-average mix and rates
   of the latest month, by_bank.latest.table, 1,000,000 ILS, 25 years): the payment month by month, the peak, when it comes, and
   the extra shekels, split between prime and the CPI. Prime reprices every month; variable every 5 years keeps its rate (its
   change day is month 61, after the path; "variable not linked, not prime" is taken as every 5 years); fixed keeps its rate;
   linked tracks grow with the CPI path. Math: NLMR.replay on NLMG.track. Hebrew only, RTL. */
(function () {
  'use strict';
  if (!window.NadLanInstruments) return;
  window.NadLanInstruments.register('mreplay', {
    custom: function (root, data) {
      var tries = 0;
      (function wait() {
        if (window.NLMG && window.NLMR && window.NLMR.ui) return window.NLMR.ui.start(root, data, build);
        if (++tries > 120) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
        setTimeout(wait, 50);
      })();
    }
  });

  function build(root, X) {
    var R = window.NLMR, U = R.ui, F = U.F, esc = U.esc, el = U.el, D = X.D;
    if (!X.rate || !X.cpi || !D.by_bank) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
    var PATH = R.replayPath(X.rate, X.cpi), W = PATH.months.length, hk = PATH.hikes, sys = R.bankMix(D, 'system');
    var st = { amount: 1000000, years: 25, src: 'system', ex: true, rows: sys.rows.map(function (r) { return { k: r.k, share: r.share, rate: r.rate }; }) };
    var h = U.fromHash('mreplay');
    if (h) {
      st.ex = false; if (isFinite(h.a)) st.amount = +h.a; if (isFinite(h.y)) st.years = +h.y; st.src = h.s || 'own';
      if (Array.isArray(h.r)) h.r.forEach(function (x) { var r = st.rows.filter(function (q) { return q.k === x[0]; })[0]; if (r) { r.share = +x[1] || 0; r.rate = +x[2]; } });
    }

    var P = U.panel(root, {
      kicker: 'מבחן לחץ · ריבית בנק ישראל 2022 עד 2023',
      title: 'אם 2022 חוזרת',
      lede: hk.length + ' העלאות ריבית בין ' + esc(F.month(hk[0].from.slice(0, 7))) + ' ל־' + esc(F.month(hk[hk.length - 1].from.slice(0, 7))) + ': ריבית בנק ישראל עלתה מ־' + esc(F.pc(PATH.boi[0])) + ' ל־' + esc(F.pc(PATH.boi[W - 1])) + ', והפריים מ־' + esc(F.pc(PATH.prime[0])) + ' ל־' + esc(F.pc(PATH.prime[W - 1])) + '. כאן הן חוזרות על התמהיל שלכם, חודש אחרי חודש, יחד עם המדד של אותם חודשים: מה יהיה ההחזר בשיא, מתי, וכמה יותר תשלמו.',
      strip: [['ריבית בנק ישראל, ' + F.month(PATH.months[0]), F.pc(PATH.boi[0])], ['ריבית בנק ישראל, ' + F.month(PATH.months[W - 1]), F.pc(PATH.boi[W - 1])], ['הפריים', F.pc(PATH.prime[0]) + ' עד ' + F.pc(PATH.prime[W - 1])], ['המדד, ' + F.month(PATH.months[0]) + ' עד ' + F.month(PATH.months[W - 1]), F.spc(100 * (PATH.ratio[W - 1] - 1), 1)]],
      eg: 'הערכים בפתיחה הם דוגמה: 1,000,000 ₪ ל־25 שנה, בתמהיל ובריביות הממוצעות של ' + F.month(sys.month) + ' לפי בנק ישראל. שנו אותם, והתוצאה מתעדכנת מיד. זה שחזור של מה שקרה, לא תחזית, ואינו ייעוץ.'
    });

    var t = 0, fields = {}, mixBox;
    function touch() { st.ex = false; clearTimeout(t); t = setTimeout(run, 90); }
    function buildForm() {
      P.form.innerHTML = '';
      var box = el('div', 'mrx__box');
      fields.amount = U.field('סכום המשכנתא', st.amount, '₪', function (n) { st.amount = n; touch(); }, { money: true });
      fields.years = U.field('תקופה', st.years, 'שנים', function (n) { st.years = n; touch(); });
      var two = el('div', 'mrx__two is-amt'); two.appendChild(fields.amount); two.appendChild(fields.years); box.appendChild(two);
      P.form.appendChild(box);
      mixBox = el('div', 'mrx__box'); P.form.appendChild(mixBox);
      U.mixEditor(mixBox, st, D, touch);
      P.form.appendChild(el('p', 'mrx__hint', 'פריים זז בכל חודש עם ריבית בנק ישראל. משתנה כל 5 שנים שומר על הריבית עד תחנת היציאה, אחרי 60 חודשים, ולכן לא זז בשחזור; משתנה לא צמודה שאינה פריים חושבה כמשתנה כל 5 שנים. קבועה לא זזה. צמודה עולה עם המדד.'));
    }

    var last = null;
    function run() {
      fields.amount._err.textContent = ''; fields.years._err.textContent = '';
      if (!(st.amount >= 10000)) { fields.amount._err.textContent = 'הקלידו את סכום המשכנתא.'; return; }
      if (!(st.years >= 4 && st.years <= 30)) { fields.years._err.textContent = 'בין 4 ל־30 שנים.'; return; }
      var rows = R.mathRows(st.rows, st.amount, st.years);
      if (!rows.length) { P.out.innerHTML = '<p class="nli__note">הקלידו חלק לפחות במסלול אחד.</p>'; return; }
      for (var i = 0; i < rows.length; i++) if (!(rows[i].rate >= 0 && rows[i].rate <= 20)) { P.out.innerHTML = '<p class="nli__note">' + esc(R.NAME[rows[i].k] + ': ריבית בין 0% ל־20%.') + '</p>'; return; }
      var rp = R.replay(rows, PATH), tot = rows.reduce(function (a, r) { return a + r.amount; }, 0);
      var sh = function (f) { return 100 * rows.filter(f).reduce(function (a, r) { return a + r.amount; }, 0) / tot; };
      last = { rows: rows, rp: rp, prime: sh(function (r) { return r.kind === 'prime'; }), linked: sh(function (r) { return r.linked; }) };
      paintOut(last); paintSecs(last); paintShare(last);
    }

    function paintOut(L) {
      var rp = L.rp, i = rp.peakIdx, o = P.out; o.innerHTML = '';
      var sub = rp.extra < 0.5 ? 'בתמהיל הזה ההחזר לא עולה בשחזור: אין בו פריים ואין בו מסלול צמוד.'
        : 'ב־' + esc(F.month(PATH.months[i])) + ', החודש ה־' + (i + 1) + ' של השחזור · בפתיחה <bdi>' + esc(F.ils(rp.first)) + '</bdi> · <bdi>' + esc(F.sils(rp.extra)) + '</bdi> בכל חודש';
      o.appendChild(U.answer('ההחזר החודשי בשיא', F.ils(rp.peak), sub, st.ex));
      o.appendChild(U.lines([
        ['ההחזר בפתיחה, ' + F.month(PATH.months[0]) + ' בשחזור', F.ils(rp.first)],
        ['התוספת בחודש, בשיא', F.sils(rp.extra)],
        ['מזה מהפריים', F.sils(rp.primeX[i])],
        ['מזה מהמדד, במסלולים הצמודים', F.sils(rp.cpiX[i])],
        ['סך התוספת ב־' + W + ' החודשים', F.ils(rp.cum)],
        ['חלק הפריים בתמהיל', F.pc(L.prime, 1)],
        ['חלק הצמוד למדד', F.pc(L.linked, 1)]
      ]));
      var srcs = [X.rate ? { label: X.rate.source + ', עדכון ' + F.date(X.rate.asof), url: 'https://www.boi.org.il/' } : null, D.cpi && D.cpi.src ? { label: X.cpi.source || D.cpi.src.label, url: D.cpi.src.url } : null, { label: 'בנק ישראל, השוואת ריביות במשכנתאות לפי בנק, ' + F.month(sys.month) + ' (פורסם ' + F.date(D.by_bank.src.file_date) + ')', url: D.by_bank.src.page || D.by_bank.src.url }];
      o.appendChild(el('p', 'mrx__src', esc('בכל חודש: ריבית בנק ישראל ביום האחרון של החודש והמדד של החודש. פריים = הריבית שלכם ועוד השינוי בריבית בנק ישראל מאז ' + F.month(PATH.months[0]) + ', וההחזר (שפיצר) מחושב מחדש על היתרה. צמודה: היתרה וההחזר × מדד החודש ÷ מדד ' + F.month(PATH.months[0]) + '. התמהיל: הריבית האפקטיבית שפורסמה, כריבית לתשלום חודשי (1 + ר)^(1/12) − 1. מקורות: ') +
        srcs.filter(Boolean).map(function (s) { return '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.label) + '</a>'; }).join(' · ') + '.'));
    }

    function paintSecs(L) {
      P.secs.innerHTML = '';
      var s1 = U.sec(P.secs, 'התוספת להחזר, חודש אחרי חודש', 'כמה יותר מההחזר בפתיחה תשלמו בכל חודש של השחזור, ומאיפה זה בא: הפריים או המדד.');
      var fig = el('figure', 'mrx__chart'); s1.appendChild(fig);
      fig.innerHTML = chart(L.rp, Math.round(Math.max(300, Math.min(1200, s1.clientWidth || 600))));
      fig.appendChild(U.legend([['#2F6F86', 'מהפריים'], ['#F2D15A', 'מהמדד, במסלולים הצמודים']]));
      var s2 = el('details', 'mrx__more mrx__sec'); s2.appendChild(el('summary', '', 'כל ' + W + ' החודשים של השחזור')); P.secs.appendChild(s2);
      var rows = PATH.months.map(function (k, i) {
        return { cls: i === L.rp.peakIdx ? 'is-on' : '', cells: [esc(F.month(k)), esc(F.pc(PATH.boi[i])), esc(F.pc(PATH.prime[i])), i ? esc(F.spc(100 * PATH.cpiM[i], 1)) : '', esc(F.ils(L.rp.pay[i])), i ? esc(F.sils(L.rp.pay[i] - L.rp.first)) : ''] };
      });
      s2.appendChild(U.table(['חודש', 'ריבית בנק ישראל', 'פריים', 'המדד בחודש', 'ההחזר', 'התוספת'], rows, { num: [1, 2, 3, 4, 5], cards: true }));
    }

    function chart(rp, Wd) {
      var H = Math.round(Math.max(200, Math.min(260, Wd * 0.42))), pl = 52, pr = 8, pt = 26, pb = 26, w = Wd - pl - pr, hh = H - pt - pb, n = rp.W;
      var max = U.niceMax(Math.max(1, rp.extra) * 1.12), s = '', bw = w / n, gap = Math.max(2, bw * 0.22);
      function Y(v) { return pt + hh * (1 - v / max); }
      for (var i = 0; i <= 4; i++) { var v = max * i / 4; s += '<line x1="' + pl + '" x2="' + (Wd - pr) + '" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '" stroke="#D3DCE2" stroke-width="1"/><text x="' + (pl - 6) + '" y="' + (Y(v) + 4).toFixed(1) + '" text-anchor="end">' + esc((i ? '+' : '') + '₪' + F.num(v)) + '</text>'; }
      for (var j = 0; j < n; j++) {
        var x = pl + bw * j + gap / 2, a = Math.max(0, rp.primeX[j]), b = Math.max(0, rp.cpiX[j]);
        s += '<rect x="' + x.toFixed(1) + '" y="' + Y(a).toFixed(1) + '" width="' + (bw - gap).toFixed(1) + '" height="' + (Y(0) - Y(a)).toFixed(1) + '" fill="#2F6F86"/>';
        if (b > 0) s += '<rect x="' + x.toFixed(1) + '" y="' + Y(a + b).toFixed(1) + '" width="' + (bw - gap).toFixed(1) + '" height="' + (Y(a) - Y(a + b)).toFixed(1) + '" fill="#F2D15A"/>';
        if (j === 0 || j === n - 1 || (n - 1 - j) % 3 === 0) s += '<text x="' + (x + (bw - gap) / 2).toFixed(1) + '" y="' + (H - 8) + '" text-anchor="middle">' + esc(F.mshort(PATH.months[j])) + '</text>';
      }
      var pi = rp.peakIdx, px = pl + bw * pi + bw / 2;
      if (rp.extra > 0.5) s += '<text class="k" x="' + Math.min(Wd - pr, px + 2).toFixed(1) + '" y="' + (Y(rp.extra) - 8).toFixed(1) + '" text-anchor="end">' + esc(F.sils(rp.extra)) + '</text>';
      var aria = 'התוספת להחזר בכל חודש של השחזור, מ־' + F.month(PATH.months[0]) + ' עד ' + F.month(PATH.months[n - 1]) + ': בשיא ' + F.sils(rp.extra) + ', מזה ' + F.sils(rp.primeX[pi]) + ' מהפריים ו־' + F.sils(rp.cpiX[pi]) + ' מהמדד';
      return '<svg viewBox="0 0 ' + Wd + ' ' + H + '" role="img" aria-label="' + esc(aria) + '">' + s + '</svg>';
    }

    function state() { return { a: st.amount, y: st.years, s: st.src, r: st.rows.map(function (r) { return [r.k, Math.round(r.share * 1000) / 1000, Math.round(r.rate * 10000) / 10000]; }) }; }
    function paintShare(L) {
      U.shareBar(P.share, function () {
        return 'אם 2022 חוזרת: משכנתא של ' + F.ils(st.amount) + ' ל־' + F.num(st.years) + ' שנה' + (st.src === 'system' ? ' בתמהיל הממוצע של ' + F.month(sys.month) : '') + ' עולה מ־' + F.ils(L.rp.first) + ' ל־' + F.ils(L.rp.peak) + ' בחודש בשיא (' + F.month(PATH.months[L.rp.peakIdx]) + ' בשחזור), תוספת של ' + F.ils(L.rp.extra) + ' בחודש.';
      }, function () { return U.link('mreplay', state()); });
    }

    buildForm(); run();
    U.resized(function () { if (last) paintSecs(last); });
  }
})();
