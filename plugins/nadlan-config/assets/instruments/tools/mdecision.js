/* NadLan Instruments · mdecision v1 (HAD-675, 5.11.2026): "החלטת הריבית והמשכנתא שלכם". The prime part of a mortgage and the
   years left (or the whole mix) -> how many shekels a month every quarter point of the Bank of Israel rate moves the payment, the
   next decision date, today's rate and prime, the Research Department forecast with the market and private forecasters, the
   payment if each path happens, every decision from -1% to +1% as a ladder, and the rate since 2022 drawn with the forecast.
   Data: boi-mortgage.json (policy, forecast, expect, by_bank), boi-rate.json (the decisions). Math: NLMR (mrates-common.js) on
   NLMG (tools/mortgage.js). Hebrew only, RTL. No email alert yet: nothing about email is shown. */
(function () {
  'use strict';
  if (!window.NadLanInstruments) return;
  window.NadLanInstruments.register('mdecision', {
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
    var R = window.NLMR, U = R.ui, F = U.F, esc = U.esc, el = U.el, D = X.D, POL = D.policy, FC = D.forecast, RT = X.rate;
    var sys = R.bankMix(D, 'system'), mMonth = sys ? sys.month : D.market.month;
    function rateOf(k) { var r = sys ? sys.rows.filter(function (x) { return x.k === k; })[0] : null; return r ? r.rate : (D.tracks[k] ? D.tracks[k].rate : 4); }
    var m0 = Math.round((rateOf('prime') - POL.prime) * 100) / 100;  // the average prime margin on new mortgages (by_bank, nominal)
    var rm = R.rampMonths(D), toBoi = FC.rate_q3_2027 - POL.rate, toMkt = FC.market_rate - POL.rate, rng = FC.private_rate_range || null;
    var TRK = ['prime', 'fixed_nl', 'fixed_cpi', 'var_nl_other', 'var_cpi'];

    var st = { mode: 'prime', bal: 400000, years: 22, margin: m0, ex: true,
      rows: [{ k: 'prime', amount: 400000, years: 22, rate: rateOf('prime') }, { k: 'fixed_nl', amount: 400000, years: 22, rate: rateOf('fixed_nl') }, { k: 'var_cpi', amount: 200000, years: 22, rate: rateOf('var_cpi') }] };
    var h = U.fromHash('mdecision');
    if (h) {
      st.ex = false; st.mode = h.mo === 'mix' ? 'mix' : 'prime';
      if (isFinite(h.b)) st.bal = +h.b; if (isFinite(h.y)) st.years = +h.y; if (isFinite(h.m)) st.margin = +h.m;
      if (Array.isArray(h.r) && h.r.length) st.rows = h.r.slice(0, 5).filter(function (x) { return R.KIND[x[0]]; }).map(function (x) { return { k: x[0], amount: +x[1] || 0, years: +x[2] || 20, rate: +x[3] }; });
    }

    var P = U.panel(root, {
      kicker: 'יום ההחלטה · ריבית בנק ישראל',
      title: 'החלטת הריבית והמשכנתא שלכם',
      lede: 'כמה כל החלטה של בנק ישראל מזיזה את ההחזר החודשי שלכם, בשקלים: לפי היתרה במסלול הפריים או לפי כל התמהיל, עם מועד ההחלטה הבאה, הריבית של היום ותחזית חטיבת המחקר של בנק ישראל.',
      strip: [['ריבית בנק ישראל, מ־' + F.date(POL.from), F.pc(POL.rate)], ['ריבית הפריים', F.pc(POL.prime)], ['ההחלטה הבאה', F.date(FC.next_decision)], ['תחזית חטיבת המחקר, רבע 3 של 2027', F.pc(FC.rate_q3_2027, 1)]],
      eg: 'הערכים בפתיחה הם דוגמה: יתרה של 400,000 ₪ במסלול הפריים ל־22 שנה, במרווח הממוצע של המשכנתאות החדשות. שנו אותם, והתוצאה מתעדכנת מיד. המחשבון אינו הצעה לאשראי ואינו ייעוץ.'
    });

    var t = 0, fields = {};
    function touch() { if (st.ex) { st.ex = false; } clearTimeout(t); t = setTimeout(run, 90); }

    /* ------------------------------------------------------------------------------------------------- the form */
    function buildForm() {
      P.form.innerHTML = ''; fields = {};
      P.form.appendChild(U.seg('מה לחשב', [['prime', 'חלק הפריים במשכנתא'], ['mix', 'כל התמהיל']], st.mode, function (k) { if (k === st.mode) return; st.mode = k; buildForm(); touch(); }));
      if (st.mode === 'prime') {
        var box = el('div', 'mrx__box');
        fields.bal = U.field('יתרת ההלוואה במסלול הפריים', st.bal, '₪', function (n) { st.bal = n; touch(); }, { money: true, help: 'כתובה בדוח השנתי מהבנק, או באתר הבנק תחת ההלוואות.' });
        fields.years = U.field('שנים שנותרו', st.years, 'שנים', function (n) { st.years = n; touch(); });
        fields.margin = U.field('המרווח מהפריים', st.margin, '%', function (n) { st.margin = n; touch(); },
          { help: 'למשל −0.5 לפריים פחות חצי. בממוצע במשכנתאות החדשות של ' + esc(F.month(mMonth)) + ': פריים ' + (m0 < 0 ? 'פחות ' : 'ועוד ') + esc(F.num(Math.abs(m0), 2)) + '% (בנק ישראל).' });
        box.appendChild(fields.bal); var two = el('div', 'mrx__two'); two.appendChild(fields.years); two.appendChild(fields.margin); box.appendChild(two);
        P.form.appendChild(box);
      } else {
        var lab = el('div', 'nli__f'); lab.appendChild(el('span', 'nli__lab', 'המסלולים שלכם')); P.form.appendChild(lab);
        var rows = el('div', 'mrx__rows'); P.form.appendChild(rows);
        st.rows.forEach(function (r, i) {
          var card = el('div', 'mrx__row'); card.style.setProperty('--c', R.COL[r.k]);
          var hd = el('div', 'mrx__rh');
          hd.appendChild(U.select('מסלול ' + (i + 1), TRK.map(function (k) { return [k, R.NAME[k]]; }), r.k, function (k) { r.k = k; r.rate = k === 'prime' ? POL.prime + m0 : rateOf(k); buildForm(); touch(); }));
          var del = el('button', 'mrx__x', '×'); del.type = 'button'; del.setAttribute('aria-label', 'הסרת מסלול ' + (i + 1)); del.hidden = st.rows.length < 2;
          del.addEventListener('click', function () { st.rows.splice(i, 1); buildForm(); touch(); });
          hd.appendChild(del); card.appendChild(hd);
          var g = el('div', 'mrx__rg');
          g.appendChild(U.field('יתרה', r.amount, '₪', function (n) { r.amount = n; touch(); }, { money: true }));
          g.appendChild(U.field('שנים שנותרו', r.years, 'שנים', function (n) { r.years = n; touch(); }));
          g.appendChild(U.field('ריבית שנתית', r.rate, '%', function (n) { r.rate = n; touch(); }, { dec: 2 }));
          card.appendChild(g); rows.appendChild(card);
        });
        var add = el('button', 'nli__add', '+ הוספת מסלול'); add.type = 'button'; add.hidden = st.rows.length >= 5;
        add.addEventListener('click', function () { st.rows.push({ k: 'prime', amount: 200000, years: 20, rate: POL.prime + m0 }); buildForm(); touch(); });
        P.form.appendChild(add);
        P.form.appendChild(el('p', 'mrx__hint', 'ביום ההחלטה זז רק מסלול הפריים. משתנה כל 5 שנים מתעדכן רק בתחנת היציאה שלו, לפי העוגן שבחוזה; קבועה לא זזה. במסלול צמוד ההחזר זז עם המדד.'));
      }
    }

    /* ------------------------------------------------------------------------------------------------------ run */
    var last = null;
    function rowsNow() {
      if (st.mode === 'prime') return [{ k: 'prime', amount: st.bal, years: st.years, rate: POL.prime + st.margin }];
      return st.rows.filter(function (r) { return r.amount > 0; }).map(function (r) { return { k: r.k, amount: r.amount, years: r.years, rate: r.rate }; });
    }
    function check() {
      Object.keys(fields).forEach(function (k) { fields[k]._err.textContent = ''; });
      if (st.mode === 'prime') {
        if (!(st.bal >= 1000)) { fields.bal._err.textContent = 'הקלידו את היתרה במסלול הפריים.'; return false; }
        if (!(st.years >= 1 && st.years <= 35)) { fields.years._err.textContent = 'בין שנה ל־35 שנים.'; return false; }
        if (!(st.margin >= -3 && st.margin <= 3)) { fields.margin._err.textContent = 'המרווח הוא בדרך כלל בין −1% ל־+1%.'; return false; }
        return true;
      }
      var rs = rowsNow(); if (!rs.length) return 'הקלידו יתרה לפחות במסלול אחד.';
      for (var i = 0; i < rs.length; i++) { if (!(rs[i].years >= 1 && rs[i].years <= 35)) return 'מסלול ' + (i + 1) + ': בין שנה ל־35 שנים.'; if (!(rs[i].rate >= 0 && rs[i].rate <= 20)) return 'מסלול ' + (i + 1) + ': ריבית בין 0% ל־20%.'; }
      return true;
    }
    function run() {
      var ok = check();
      if (ok !== true) { if (typeof ok === 'string' || !last) P.out.innerHTML = '<p class="nli__note">' + esc(typeof ok === 'string' ? ok : 'בדקו את הערכים בטופס.') + '</p>'; return; }
      var rows = rowsNow(), dc = R.decision(rows), now = dc.now;
      var pay = function (to) { return R.pathMix(rows, to, rm); };
      var L = { rows: rows, dc: dc, now: now, boi: pay(toBoi), mkt: pay(toMkt), lo: rng ? pay(rng[0] - POL.rate) : null, hi: rng ? pay(rng[1] - POL.rate) : null };
      last = L; paintOut(L); paintSecs(L); paintShare(L);
    }

    function days() { var d = Math.round((Date.parse(FC.next_decision + 'T12:00:00') - Date.now()) / 864e5); return d; }
    function paintOut(L) {
      var o = P.out, dc = L.dc, pr = dc.rows.filter(function (r) { return r.kind === 'prime'; });
      o.innerHTML = '';
      var sub;
      if (st.mode === 'prime') {
        var rate = POL.prime + st.margin, n = Math.round(st.years * 12);
        sub = 'ההחזר במסלול הפריים היום: <bdi>' + esc(F.ils(L.now)) + '</bdi> בחודש, בריבית <bdi>' + esc(F.pc(rate)) + '</bdi> (פריים <bdi>' + esc(F.pc(POL.prime)) + '</bdi> ' + (st.margin < 0 ? 'פחות' : 'ועוד') + ' <bdi>' + esc(F.pc(Math.abs(st.margin))) + '</bdi>), <bdi>' + n + '</bdi> תשלומים. העלאה מוסיפה את הסכום הזה, הורדה מורידה אותו.';
      } else {
        sub = pr.length ? 'ההחזר של כל התמהיל היום: <bdi>' + esc(F.ils(L.now)) + '</bdi> בחודש. ביום ההחלטה זז רק מסלול הפריים: <bdi>' + esc(F.ils(dc.prime)) + '</bdi> מתוך <bdi>' + esc(F.ils(dc.total)) + '</bdi>.'
          : 'אין בתמהיל מסלול פריים, ולכן ההחלטה לא מזיזה את ההחזר החודשי ביום שהיא נכנסת לתוקף. ההחזר של כל התמהיל היום: <bdi>' + esc(F.ils(L.now)) + '</bdi>.';
      }
      o.appendChild(U.answer('כל רבע אחוז בריבית בנק ישראל, בחודש', F.ils(dc.q), sub, st.ex));
      var d = days(), when = F.date(FC.next_decision) + (d === 0 ? ', היום' : d === 1 ? ', מחר' : d > 1 ? ', בעוד ' + d + ' ימים' : '');
      var li = [['ההחלטה הבאה של בנק ישראל', when],
        ['אם תחזית חטיבת המחקר תתממש: ' + F.pc(FC.rate_q3_2027, 1) + ' ברבע 3 של 2027', F.ils(L.boi) + ' · ' + F.sils(L.boi - L.now)],
        ['אם ציפיות השוק יתממשו: ' + F.pc(FC.market_rate, 1), F.ils(L.mkt) + ' · ' + F.sils(L.mkt - L.now)]];
      if (rng) li.push(['טווח החזאים הפרטיים: ' + F.pc(rng[0], 1) + ' עד ' + F.pc(rng[1], 1), F.ils(L.lo) + ' עד ' + F.ils(L.hi)]);
      if (st.mode === 'mix') {
        dc.rows.forEach(function (r, i) {
          var txt = r.kind === 'prime' ? F.sils(r.q) + ' לכל רבע אחוז' : r.kind === 'var5' ? 'מתעדכן בתחנת היציאה, לפי העוגן' : 'לא זז בהחלטה';
          if (r.linked) txt += ', וזז עם המדד';
          li.push([R.NAME[r.k] + ', ' + F.ils(L.rows[i].amount), txt]);
        });
        var ex = D.expect && D.expect.series && D.expect.series.exp_1y_capital_market;
        if (ex && dc.rows.some(function (r) { return r.linked; })) li.push(['ציפיות האינפלציה לשנה הקרובה, שוק ההון, ' + F.month(ex.last), F.pc(ex.value)]);
      }
      o.appendChild(U.lines(li));
      var srcs = [POL.src, FC.src, D.by_bank ? { label: 'בנק ישראל, השוואת ריביות במשכנתאות לפי בנק, ' + F.month(mMonth), url: D.by_bank.src.page || D.by_bank.src.url } : null];
      if (st.mode === 'mix' && D.expect) srcs.push({ label: 'בנק ישראל, ציפיות האינפלציה', url: D.expect.src.url });
      o.appendChild(el('p', 'mrx__src', esc('החזר חודשי (שפיצר) = יתרה × ר ÷ (1 − (1 + ר)^−מ), ר = הריבית השנתית ÷ 12, מ = מספר התשלומים. רבע אחוז = ההחזר בריבית של היום ועוד 0.25%, פחות ההחזר בריבית של היום. פריים = ריבית בנק ישראל ועוד 1.5%. בתחזיות הריבית זזה בהדרגה עד אוגוסט 2027 וההחזר מחושב מחדש בכל חודש. מקורות: ') +
        srcs.filter(Boolean).map(function (s) { return '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.label) + '</a>'; }).join(' · ') + esc('. הריבית נכונה ל־' + F.date(POL.asof) + '.')));
    }

    /* ---------------------------------------------------------------------------------------------- the sections */
    function paintSecs(L) {
      P.secs.innerHTML = '';
      var s1 = U.sec(P.secs, 'כל החלטה אפשרית, בשקלים', 'ההחזר החודשי שלכם בכל ריבית שבנק ישראל יכול לקבוע, ברבעי אחוז מהריבית של היום. בנק ישראל מזיז את הריבית ברבע אחוז או בחצי אחוז בכל החלטה.');
      var rows = [], tb = Math.round(toBoi * 4) / 4;
      [1, 0.75, 0.5, 0.25, 0, -0.25, -0.5, -0.75, -1].forEach(function (dd) {
        if (POL.rate + dd < 0) return;
        var p = R.ladderPay(L.rows, dd), tag = dd === 0 ? '<span class="mrx__tag is-ink">היום</span>' : Math.abs(dd - tb) < 1e-9 ? '<span class="mrx__tag">התחזית</span>' : '';
        rows.push({ cls: dd === 0 ? 'is-on' : '', cells: ['<bdi>' + esc(F.pc(POL.rate + dd)) + '</bdi>' + tag, esc(F.pc(POL.prime + dd)), esc(F.ils(p)), dd === 0 ? '' : esc(F.sils(p - L.now))] });
      });
      s1.appendChild(U.table(['ריבית בנק ישראל', 'פריים', 'ההחזר בחודש', 'השינוי בחודש'], rows, { num: [1, 2, 3] }));
      var s2 = U.sec(P.secs, 'ריבית בנק ישראל מ־2022, והתחזית');
      var fig = el('figure', 'mrx__chart'); s2.appendChild(fig);
      var W = Math.round(Math.max(300, Math.min(1200, s2.clientWidth || 600)));
      fig.innerHTML = chart(W);
      fig.appendChild(U.legend([['#12202A', 'ריבית בנק ישראל, כל החלטה'], ['#2F6F86', 'תחזית חטיבת המחקר', 'd'], ['rgba(47,111,134,.25)', 'טווח החזאים הפרטיים']]));
      var mv = moves();
      fig.appendChild(el('figcaption', 'mrx__hint', esc(mv.up + ' העלאות בין ' + F.month(mv.first.from.slice(0, 7)) + ' ל־' + F.month(mv.pk.from.slice(0, 7)) + ', ומאז ' + mv.down + ' הורדות. ההחלטות: בנק ישראל, סדרה MNT_RIB_BOI_D; התחזית: חטיבת המחקר, ' + F.date(FC.published) + '.')));
    }
    function moves() {  // the hikes up to the peak since 2022 and the cuts after it, counted from boi-rate.json
      var C = RT.changes, pk = null, up = 0, down = 0, first = null;
      C.forEach(function (c) { if (c.from >= '2022-01-01' && (pk === null || c.rate >= pk.rate)) pk = c; });
      C.forEach(function (c, i) { if (!i || c.from < '2022-01-01') return; if (c.from <= pk.from && c.rate > C[i - 1].rate) { up++; if (!first) first = c; } if (c.from > pk.from && c.rate < C[i - 1].rate) down++; });
      return { pk: pk, up: up, down: down, first: first || pk };
    }

    function chart(W) {
      var H = Math.round(Math.max(210, Math.min(270, W * 0.42))), pl = 40, pr = 14, pt = 30, pb = 28, w = W - pl - pr, hh = H - pt - pb;
      function t(iso) { var p = iso.split('-'); return Date.UTC(+p[0], +p[1] - 1, +(p[2] || 1)); }
      var x0 = t('2022-01-01'), x1 = t('2027-12-31'), fx = t('2027-08-15'), today = t(POL.asof);
      var ch = RT.changes.filter(function (c) { return c.from >= '2022-01-01' && c.from <= POL.asof; });
      var top = Math.max.apply(null, ch.map(function (c) { return c.rate; }).concat(rng ? [rng[1]] : []).concat([POL.rate])), ymax = Math.ceil(top + 0.25);
      function X(ms) { return pl + w * (ms - x0) / (x1 - x0); } function Y(v) { return pt + hh * (1 - v / ymax); }
      var s = '';
      for (var v = 0; v <= ymax; v++) s += '<line x1="' + pl + '" x2="' + (W - pr) + '" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '" stroke="#D3DCE2" stroke-width="1"/><text x="' + (pl - 6) + '" y="' + (Y(v) + 4).toFixed(1) + '" text-anchor="end">' + v + '%</text>';
      for (var y = 2022; y <= 2027; y++) { var xx = X(t(y + '-01-01')); s += '<line x1="' + xx.toFixed(1) + '" x2="' + xx.toFixed(1) + '" y1="' + (pt + hh) + '" y2="' + (pt + hh + 4) + '" stroke="#5E6A75"/><text x="' + (xx + 2).toFixed(1) + '" y="' + (H - 8) + '" text-anchor="start">' + y + '</text>'; }
      var start = R.boiOn(RT, '2022-01-01').rate, d = 'M' + X(x0).toFixed(1) + ' ' + Y(start).toFixed(1);
      ch.forEach(function (c) { if (c.from > '2022-01-01') d += 'H' + X(t(c.from)).toFixed(1) + 'V' + Y(c.rate).toFixed(1); });
      d += 'H' + X(today).toFixed(1);
      if (rng) s += '<rect x="' + (X(fx) - 5).toFixed(1) + '" y="' + Y(rng[1]).toFixed(1) + '" width="10" height="' + (Y(rng[0]) - Y(rng[1])).toFixed(1) + '" fill="#2F6F86" fill-opacity=".25"/>';
      s += '<path d="' + d + '" fill="none" stroke="#12202A" stroke-width="2"/>';
      s += '<path d="M' + X(today).toFixed(1) + ' ' + Y(POL.rate).toFixed(1) + 'L' + X(fx).toFixed(1) + ' ' + Y(FC.rate_q3_2027).toFixed(1) + '" fill="none" stroke="#2F6F86" stroke-width="2" stroke-dasharray="5 4"/>';
      var pk = ch.reduce(function (a, c) { return !a || c.rate > a.rate ? c : a; }, null);
      if (pk) s += '<text class="k" x="' + X(t(pk.from)).toFixed(1) + '" y="' + (Y(pk.rate) - 8).toFixed(1) + '" text-anchor="start">' + esc(F.pc(pk.rate)) + '</text>';
      s += '<circle cx="' + X(today).toFixed(1) + '" cy="' + Y(POL.rate).toFixed(1) + '" r="4" fill="#12202A"/>';
      // labels under the line: since 2023 the rate never went below today's, so the space below-left of the points is free
      s += '<text class="he k" x="' + (X(today) - 6).toFixed(1) + '" y="' + (Y(POL.rate) + 18).toFixed(1) + '" text-anchor="end">' + esc('היום ' + F.pc(POL.rate)) + '</text>';
      s += '<circle cx="' + X(fx).toFixed(1) + '" cy="' + Y(FC.rate_q3_2027).toFixed(1) + '" r="4" fill="#fff" stroke="#2F6F86" stroke-width="2"/>';
      s += '<text class="he" x="' + (X(fx) + 6).toFixed(1) + '" y="' + (Y(rng ? rng[0] : FC.rate_q3_2027) + 26).toFixed(1) + '" text-anchor="end" style="fill:#1F4B5C">' + esc('תחזית ' + F.pc(FC.rate_q3_2027, 1)) + '</text>';
      var aria = 'ריבית בנק ישראל מ־2022: ' + F.pc(start) + ' בינואר 2022, שיא של ' + F.pc(pk.rate) + ' מ־' + F.date(pk.from) + ', ' + F.pc(POL.rate) + ' היום, ותחזית חטיבת המחקר ' + F.pc(FC.rate_q3_2027, 1) + ' ברבע 3 של 2027';
      return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(aria) + '">' + s + '</svg>';
    }

    function state() { return { mo: st.mode, b: st.bal, y: st.years, m: st.margin, r: st.rows.map(function (r) { return [r.k, Math.round(r.amount || 0), r.years, Math.round(r.rate * 1000) / 1000]; }) }; }
    function paintShare(L) {
      U.shareBar(P.share, function () {
        var who = st.mode === 'prime' ? 'מסלול פריים של ' + F.ils(st.bal) + ', ' + F.num(st.years) + ' שנים' : 'תמהיל של ' + F.ils(L.dc.total) + ', מזה פריים ' + F.ils(L.dc.prime);
        return 'החלטת הריבית של בנק ישראל ב־' + F.date(FC.next_decision) + ': כל רבע אחוז משנה את ההחזר החודשי שלי ב־' + F.ils(L.dc.q) + ' (' + who + '). אם תחזית בנק ישראל תתממש (' + F.pc(FC.rate_q3_2027, 1) + '): ' + F.ils(L.boi) + ' בחודש.';
      }, function () { return U.link('mdecision', state()); });
    }

    buildForm(); run();
    U.resized(function () { if (last) paintSecs(last); });
  }
})();
