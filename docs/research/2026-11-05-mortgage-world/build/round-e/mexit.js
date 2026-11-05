/* NadLan Instruments · mexit v1 (HAD-675, 5.11.2026): "כמה תעלה היציאה". Two ways in:
   - planning: "I expect to sell, upgrade or refinance in N years" (3 / 5 / 7 / 10 / to the end): for the reader's mix and the
     three uniform baskets of directive 451 (same amount, term and rate per track), the payments until year N, the balance to repay,
     the expected early-repayment fee at year N by the Banking Order (NLMG.prepayFee) and the price of the money (interest, CPI
     linkage and fee), on the Bank of Israel forecast path (prime to forecast.rate_q3_2027, CPI forecast.inflation_4q); the average
     rate on the exit day = today's average for the period left, lower by the forecast fall of the policy rate (with "no change"
     and "1% lower" beside it). Cost by horizon, never a recommendation.
   - "I already have a mortgage": loan month, amount, term, track and rate -> the balance today and the fee if repaid today, from
     the Bank of Israel averages in force today and on the loan day (prepay.nl / prepay.cpi). The data's worked example
     (1,000,000 ILS fixed not linked from 2024-11 at 4.88%) gives 15,908 ILS on 956,994 ILS (test_mrates.js).
   Round E (HAD-675, 6.11.2026), in "I already have a mortgage": "האם למחזר?". The balance refinanced today for the months left in the
   same track at the Bank of Israel average (NLMR.refiAvg: a fixed track at the term-to-maturity file in force today, prime and the
   variable tracks at the track's average of all banks, by_bank, latest month; the reader may type an offer instead), the new
   payment, the monthly saving or extra, the one-off costs found in the data (the capitalization fee, the operational fee up to 60
   ILS, 0.1% for under 10 days notice) plus the reader's own appraiser and file costs (empty by default: not in any official file),
   and the months until the saving covers them; "לא משתלם כרגע" when there is no saving or it does not cover them by the end.
   Costs and months, never a recommendation. The worked example: 956,994 ILS for 276 months, 5,776 a month today at 4.88%; at the
   4.788% average (in force 19.10.2026): 5,671 a month, about 105 less, against 16,925 ILS of costs: 162 months (test_mrates.js).
   Math: NLMR on NLMG. Hebrew only, RTL. */
(function () {
  'use strict';
  if (!window.NadLanInstruments) return;
  window.NadLanInstruments.register('mexit', {
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
    var R = window.NLMR, U = R.ui, F = U.F, esc = U.esc, el = U.el, D = X.D, POL = D.policy, FC = D.forecast;
    if (!D.by_bank || !D.prepay || !D.baskets) { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; return; }
    var sys = R.bankMix(D, 'system'), drop = Math.round((POL.rate - FC.rate_q3_2027) * 100) / 100, NOW = R.nowKey();
    var HZ = [['3', '3 שנים'], ['5', '5 שנים'], ['7', '7 שנים'], ['10', '10 שנים'], ['end', 'עד הסוף']];
    var EX = { date: '2024-11', k: 'fixed_nl' }, exRate = R.rateIn(D, EX.k, EX.date);
    var st = { mode: 'plan', hz: '5', amount: 1000000, years: 25, src: 'system', ex: true, rows: sys.rows.map(function (r) { return { k: r.k, share: r.share, rate: r.rate }; }),
      have: { date: EX.date, amount: 1000000, years: 25, k: EX.k, rate: exRate != null ? exRate : 4.88, touched: false },
      refi: { rate: null, touched: false, extra: null, notice: 'short' } };  // round E: until typed, the refinance rate follows the average
    var h = U.fromHash('mexit');
    if (h) {
      st.ex = false; st.mode = h.mo === 'have' ? 'have' : 'plan'; if (h.hz) st.hz = String(h.hz); if (isFinite(h.a)) st.amount = +h.a; if (isFinite(h.y)) st.years = +h.y; st.src = h.s || 'own';
      if (Array.isArray(h.r)) h.r.forEach(function (x) { var r = st.rows.filter(function (q) { return q.k === x[0]; })[0]; if (r) { r.share = +x[1] || 0; r.rate = +x[2]; } });
      if (h.hv) st.have = { date: R.parseMonth(h.hv[0]) || EX.date, amount: +h.hv[1] || 1000000, years: +h.hv[2] || 25, k: R.KIND[h.hv[3]] ? h.hv[3] : 'fixed_nl', rate: +h.hv[4], touched: true };
      if (Array.isArray(h.rf)) st.refi = { rate: h.rf[0] != null && isFinite(h.rf[0]) ? +h.rf[0] : null, touched: h.rf[0] != null && isFinite(h.rf[0]), extra: +h.rf[1] > 0 ? +h.rf[1] : null, notice: h.rf[2] === 'long' ? 'long' : 'short' };
    }

    var P = U.panel(root, {
      kicker: 'לפני שנכנסים · פירעון מוקדם',
      title: 'כמה תעלה היציאה',
      lede: 'מתכננים למכור, לשדרג או למחזר בעוד כמה שנים? מה תעלה המשכנתא עד אז בכל תמהיל: הריבית, ההצמדה ועמלת הפירעון המוקדם לפי צו הבנקאות, לפי תחזית בנק ישראל. ויש מצב למשכנתא שכבר לקחתם: כמה עולה לפרוע אותה היום, ואם ממחזרים בריבית הממוצעת: ההחזר החדש ובכמה חודשים החיסכון מכסה את העלויות.',
      strip: [['ריבית בנק ישראל היום', F.pc(POL.rate)], ['תחזית חטיבת המחקר, רבע 3 של 2027', F.pc(FC.rate_q3_2027, 1)], ['תחזית המדד לשנה', F.pc(FC.inflation_4q, 1)], ['הממוצעים לעמלת הפירעון', 'מ־' + F.date(D.prepay.nl.rows[D.prepay.nl.rows.length - 1][0])]],
      eg: 'הערכים בפתיחה הם דוגמה: 1,000,000 ₪ ל־25 שנה בתמהיל הממוצע של ' + F.month(sys.month) + ', ובמשכנתא קיימת: 1,000,000 ₪ קבועה לא צמודה מ־' + F.month(EX.date) + '. שנו אותם, והתוצאה מתעדכנת מיד. אלה עלויות לפי מועד היציאה, לא המלצה על תמהיל ולא ייעוץ.'
    });

    var t = 0, fields = {};
    function touch() { st.ex = false; clearTimeout(t); t = setTimeout(run, 90); }

    /* ------------------------------------------------------------------------------------------------- the form */
    function buildForm() {
      P.form.innerHTML = ''; fields = {};
      P.form.appendChild(U.seg('מה בודקים', [['plan', 'משכנתא שאני לוקח'], ['have', 'משכנתא שכבר יש לי']], st.mode, function (k) { if (k === st.mode) return; st.mode = k; buildForm(); touch(); }));
      if (st.mode === 'plan') {
        P.form.appendChild(U.seg('בעוד כמה שנים יוצאים', HZ, st.hz, function (k) { st.hz = k; touch(); }));
        var box = el('div', 'mrx__box');
        fields.amount = U.field('סכום המשכנתא', st.amount, '₪', function (n) { st.amount = n; touch(); }, { money: true });
        fields.years = U.field('תקופה', st.years, 'שנים', function (n) { st.years = n; touch(); });
        var two = el('div', 'mrx__two is-amt'); two.appendChild(fields.amount); two.appendChild(fields.years); box.appendChild(two); P.form.appendChild(box);
        var mb = el('div', 'mrx__box'); P.form.appendChild(mb); U.mixEditor(mb, st, D, touch);
      } else {
        var hv = st.have, b2 = el('div', 'mrx__box');
        fields.date = U.field('החודש שבו לקחתם את ההלוואה', hv.date ? F.month(hv.date) : '', null, function (s) { var k = R.parseMonth(s); if (k) { hv.date = k; autoRate(); } else hv.date = null; touch(); }, { type: 'text', ph: '11.2024', help: 'חודש ושנה, למשל 11.2024.' });
        fields.amount2 = U.field('הסכום שלקחתם', hv.amount, '₪', function (n) { hv.amount = n; touch(); }, { money: true });
        fields.years2 = U.field('התקופה המקורית', hv.years, 'שנים', function (n) { hv.years = n; touch(); });
        var tw = el('div', 'mrx__two is-amt'); tw.appendChild(fields.amount2); tw.appendChild(fields.years2);
        b2.appendChild(fields.date); b2.appendChild(tw);
        b2.appendChild(U.select('המסלול', ['fixed_nl', 'fixed_cpi', 'prime', 'var_nl_other', 'var_cpi'].map(function (k) { return [k, R.NAME[k] + (R.KIND[k].kind === 'var5' ? ', כל 5 שנים' : '')]; }), hv.k, function (k) { hv.k = k; autoRate(); touch(); }));
        fields.rate2 = U.field('הריבית בהלוואה היום', hv.rate, '%', function (n) { hv.rate = n; hv.touched = true; touch(); }, { dec: 2, help: rateHelp() });
        b2.appendChild(fields.rate2); P.form.appendChild(b2);
      }
    }
    function rateHelp() { var hv = st.have, a = hv.date ? R.rateIn(D, hv.k, hv.date) : null; return 'הריבית השנתית בהלוואה, מהדוח השנתי של הבנק.' + (a != null ? ' הממוצע במשכנתאות החדשות ב' + R.NAME[hv.k] + ' ב־' + esc(F.month(hv.date)) + ': ' + esc(F.pc(a)) + ' (בנק ישראל).' : ''); }
    function autoRate() {  // until the reader types a rate, it follows the average of the loan month and track
      var hv = st.have, a = hv.date ? R.rateIn(D, hv.k, hv.date) : null;
      if (!hv.touched && a != null) { hv.rate = a; if (fields.rate2) fields.rate2._inp.value = String(a); }
      if (fields.rate2) { var hp = fields.rate2.querySelector('.nli__help'); if (hp) hp.innerHTML = rateHelp(); }
    }

    /* ------------------------------------------------------------------------------------------------------ run */
    var last = null;
    function clearErr() { Object.keys(fields).forEach(function (k) { fields[k]._err.textContent = ''; }); }
    function note(msg) { P.out.innerHTML = '<p class="nli__note">' + esc(msg) + '</p>'; P.secs.innerHTML = ''; }
    function run() { clearErr(); if (st.mode === 'plan') runPlan(); else runHave(); }

    function yearsOf(hz) { return hz === 'end' ? st.years : Math.min(+hz, st.years); }
    function mixes() {
      var rateOf = function (k) { var r = st.rows.filter(function (x) { return x.k === k; })[0]; return r ? r.rate : 4; };
      return [{ name: 'התמהיל שלכם', rows: R.mathRows(st.rows, st.amount, st.years), you: true }].concat(D.baskets.list.map(function (b) {
        return { name: b.label, sub: basketText(b), rows: R.mathRows(R.basketRows(D, b, rateOf), st.amount, st.years) };
      }));
    }
    function basketText(b) {
      if (b.mix.length === 1) return 'כל ההלוואה ב' + R.SHORT[R.BASKET_KEY[b.mix[0][0]]];
      return b.mix.map(function (x) { var w = Math.abs(x[1] - 0.5) < 1e-6 ? 'חצי' : Math.abs(x[1] - 1 / 3) < 1e-6 ? 'שליש' : F.pc(100 * x[1], 0); return w + ' ' + R.SHORT[R.BASKET_KEY[x[0]]]; }).join(', ');
    }
    function runPlan() {
      if (!(st.amount >= 10000)) { fields.amount._err.textContent = 'הקלידו את סכום המשכנתא.'; return; }
      if (!(st.years >= 4 && st.years <= 30)) { fields.years._err.textContent = 'בין 4 ל־30 שנים.'; return; }
      var M = mixes(); if (!M[0].rows.length) return note('הקלידו חלק לפחות במסלול אחד.');
      for (var i = 0; i < M[0].rows.length; i++) if (!(M[0].rows[i].rate >= 0 && M[0].rows[i].rate <= 20)) return note(R.NAME[M[0].rows[i].k] + ': ריבית בין 0% ל־20%.');
      var sc = R.exitScenario(D), y = yearsOf(st.hz);
      var res = M.map(function (m) { return R.exitAt(m.rows, D, sc, y, drop); });
      var me0 = R.exitAt(M[0].rows, D, sc, y, 0), me1 = R.exitAt(M[0].rows, D, sc, y, 1);
      var grid = HZ.map(function (hz) { var yy = yearsOf(hz[0]); return { hz: hz, y: yy, r: M.map(function (m) { return R.exitAt(m.rows, D, sc, yy, drop); }) }; });
      last = { mode: 'plan', M: M, res: res, me0: me0, me1: me1, y: y, grid: grid };
      paintPlan(last); paintShare(last);
    }
    function runHave() {
      var hv = st.have;
      if (!hv.date) { fields.date._err.textContent = 'בחרו חודש ושנה, למשל 11.2024.'; return; }
      if (R.mDiff(hv.date, NOW) < 1) { fields.date._err.textContent = 'החודש צריך להיות לפני ' + F.month(NOW) + '.'; return; }
      if (!(hv.amount >= 10000)) { fields.amount2._err.textContent = 'הקלידו את הסכום שלקחתם.'; return; }
      if (!(hv.years >= 4 && hv.years <= 35)) { fields.years2._err.textContent = 'בין 4 ל־35 שנים.'; return; }
      if (!(hv.rate >= 0 && hv.rate <= 20)) { fields.rate2._err.textContent = 'ריבית בין 0% ל־20%.'; return; }
      if (R.mDiff(hv.date, NOW) >= Math.round(hv.years * 12)) return note('לפי התאריך והתקופה ההלוואה כבר נפרעה.');
      var r = R.feeExisting(hv, D, X.cpi, NOW), later = [];
      [36, 60].forEach(function (m) { var at = R.mAdd(hv.date, m); if (at > NOW && m < Math.round(hv.years * 12)) later.push({ m: m, at: at, r: R.feeExisting(hv, D, X.cpi, at) }); });
      last = { mode: 'have', r: r, later: later };
      paintHave(last); paintShare(last);
    }

    /* -------------------------------------------------------------------------------------------------- planning */
    function srcLine(list, pre) { return el('p', 'mrx__src', esc(pre) + list.filter(Boolean).map(function (s) { return '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.label) + '</a>'; }).join(' · ') + '.'); }
    function paintPlan(L) {
      var o = P.out, me = L.res[0], end = st.hz === 'end' || me.end; o.innerHTML = '';
      var lab = end ? 'מה תעלה המשכנתא עד הסוף, בתמהיל שלכם' : 'מה תעלה המשכנתא אם יוצאים בעוד ' + F.num(L.y) + ' שנים';
      var sub = 'ריבית <bdi>' + esc(F.ils(me.intr)) + '</bdi>, הצמדה <bdi>' + esc(F.ils(me.link)) + '</bdi>' + (end ? '. אין עמלת פירעון: ההלוואה נפרעת בזמן.' : ' ועמלת פירעון צפויה <bdi>' + esc(F.ils(me.fee)) + '</bdi>. התשלומים עד אז <bdi>' + esc(F.ils(me.pay)) + '</bdi>, והיתרה לפירעון ביציאה <bdi>' + esc(F.ils(me.bal)) + '</bdi>.');
      o.appendChild(U.answer(lab, F.ils(me.price), sub, st.ex));
      var li = [['התשלומים עד ' + (end ? 'הסוף' : 'היציאה'), F.ils(me.pay)], end ? null : ['היתרה לפירעון ביציאה', F.ils(me.bal)], ['ריבית', F.ils(me.intr)], ['הצמדה למדד', me.link > 0.5 ? F.ils(me.link) : 'ללא הצמדה']];
      if (!end) li = li.concat([
        ['עמלת היוון צפויה, אם הממוצע ירד ב־' + F.pc(drop) + ' כמו הריבית בתחזית', F.ils(me.fee)],
        ['אם הממוצע לא ישתנה', F.ils(L.me0.fee)],
        ['אם הממוצע ירד ב־1%', F.ils(L.me1.fee)],
        ['עמלה תפעולית', 'עד ' + F.ils(me.op)],
        ['בהודעה של פחות מ־10 ימים (0.1%)', F.ils(me.notice)],
        me.cpiFee > 0.5 ? ['בפירעון בין ה־1 ל־15 בחודש, במסלולים הצמודים', F.ils(me.cpiFee)] : null]);
      o.appendChild(U.lines(li));
      o.appendChild(srcLine([FC.src, D.fees.src, U.srcHe(D, D.prepay.nl.src, 'mashfix'), U.srcHe(D, D.prepay.cpi.src, 'pribmash'), { label: 'בנק ישראל, השוואת ריביות במשכנתאות לפי בנק, ' + F.month(sys.month), url: D.by_bank.src.page || D.by_bank.src.url }],
        'ריבית, הצמדה ועמלה = התשלומים עד היציאה + היתרה + העמלה − סכום ההלוואה. פריים לפי תחזית חטיבת המחקר (' + F.pc(FC.rate_q3_2027, 1) + ' ברבע 3 של 2027), מדד ' + F.pc(FC.inflation_4q, 1) + ' בשנה. עמלת היוון לפי צו הבנקאות: התשלומים שנותרו (במשתנה: עד יום שינוי הריבית) מהוונים בריבית הממוצעת ביום הפירעון, פחות היתרה, הנמוך משני החישובים של סעיף 3, בהפחתה של 20% אחרי 3 שנים ו־30% אחרי 5; בפריים וביום שינוי הריבית אין עמלת היוון. הממוצע ביום הפירעון: הממוצע של היום לתקופה שתישאר, פחות ' + F.pc(drop) + '. מקורות: '));
      paintPlanSecs(L);
    }
    function paintPlanSecs(L) {
      P.secs.innerHTML = '';
      var end = st.hz === 'end' || L.res[0].end;
      var s1 = U.sec(P.secs, 'התמהיל שלכם מול שלושת הסלים האחידים', 'אותו סכום, אותה תקופה ואותה ריבית לכל מסלול, רק החלוקה בין המסלולים שונה. את שלושת הסלים כל בנק חייב להציג באישור העקרוני (הוראה 451).');
      var fig = el('figure', 'mrx__chart'); s1.appendChild(fig);
      fig.innerHTML = bars(L, Math.round(Math.max(300, Math.min(1200, s1.clientWidth || 600))));
      fig.appendChild(U.legend([['#8E7CC3', 'ריבית'], ['#F2D15A', 'הצמדה'], ['#1F4B5C', 'עמלת פירעון צפויה']]));
      var rows = L.M.map(function (m, i) { var r = L.res[i]; return { cls: m.you ? 'is-you' : '', cells: [esc(m.name) + (m.sub ? '<small>' + esc(m.sub) + '</small>' : ''), esc(F.ils(r.pay)), end ? '' : esc(F.ils(r.bal)), end ? '' : esc(F.ils(r.fee)), esc(F.ils(r.price))] }; });
      s1.appendChild(U.table(['תמהיל', 'תשלומים עד ' + (end ? 'הסוף' : 'היציאה'), 'יתרה לפירעון', 'עמלה צפויה', 'ריבית, הצמדה ועמלה'], rows, { num: [1, 2, 3, 4], cards: true }));
      var s2 = U.sec(P.secs, 'לפי מועד היציאה', 'ריבית, הצמדה ועמלה צפויה בכל מועד יציאה, באותם תנאים.');
      var rows2 = L.grid.map(function (g) { return { cls: g.hz[0] === st.hz ? 'is-on' : '', cells: [esc(g.hz[0] === 'end' ? 'עד הסוף' : 'בעוד ' + g.hz[1])].concat(g.r.map(function (r) { return esc(F.ils(r.price)); })) }; });
      s2.appendChild(U.table(['יוצאים'].concat(L.M.map(function (m) { return m.you ? 'התמהיל שלכם' : m.name; })), rows2, { num: [1, 2, 3, 4], cards: true }));
      s2.appendChild(el('p', 'mrx__hint', 'זו השוואה של עלויות לפי מועד היציאה, לא המלצה על תמהיל. העלות בפועל תלויה בריבית שתקבלו, במדד ובריבית הממוצעת של בנק ישראל ביום הפירעון. משתנה לא צמודה שאינה פריים חושבה כמשתנה כל 5 שנים.'));
    }
    function bars(L, Wd) {
      var n = L.M.length, rh = 50, pt = 6, H = pt + n * rh, pr = 4, pl = 4, w = Wd - pl - pr, s = '';
      var max = Math.max.apply(null, L.res.map(function (r) { return r.intr + r.link + r.fee; })) || 1;
      L.M.forEach(function (m, i) {
        var r = L.res[i], y = pt + i * rh, x = Wd - pr, parts = [[r.intr, '#8E7CC3'], [r.link, '#F2D15A'], [r.fee, '#1F4B5C']];
        s += '<text class="he' + (m.you ? ' k' : '') + '" x="' + (Wd - pr) + '" y="' + (y + 14) + '" text-anchor="end">' + esc(m.name) + '</text>';
        s += '<text class="k" x="' + pl + '" y="' + (y + 14) + '" text-anchor="start">' + esc(F.ils(r.price)) + '</text>';
        parts.forEach(function (p) { var bw = w * Math.max(0, p[0]) / max; if (bw < 0.5) return; x -= bw; s += '<rect x="' + x.toFixed(1) + '" y="' + (y + 22) + '" width="' + bw.toFixed(1) + '" height="16" fill="' + p[1] + '"/>'; });
      });
      var aria = 'ריבית, הצמדה ועמלה ' + (st.hz === 'end' ? 'עד הסוף' : 'עד היציאה בעוד ' + L.y + ' שנים') + ': ' + L.M.map(function (m, i) { return m.name + ' ' + F.ils(L.res[i].price); }).join(', ');
      return '<svg viewBox="0 0 ' + Wd + ' ' + H + '" role="img" aria-label="' + esc(aria) + '">' + s + '</svg>';
    }

    /* ------------------------------------------------------------------------------------------- existing loan */
    function paintHave(L) {
      var r = L.r, hv = st.have, o = P.out; o.innerHTML = '';
      var sub;
      if (r.kind === 'prime') sub = 'במסלול הפריים אין עמלת היוון: הריבית משתנה במועד לא ידוע (צו הבנקאות, סעיף 4). נשארות העמלה התפעולית, עד <bdi>' + esc(F.ils(r.op)) + '</bdi>, ו־0.1% בהודעה של פחות מ־10 ימים.';
      else if (r.why === 'reset') sub = 'החודש הוא יום שינוי הריבית במסלול, ובו אין עמלת היוון (צו הבנקאות, סעיף 4).';
      else sub = 'יתרה <bdi>' + esc(F.ils(r.bal)) + '</bdi> אחרי <bdi>' + r.el + '</bdi> תשלומים, נכון ל־' + esc(F.month(NOW)) + '.' + (r.fee < 0.5 ? ' הריבית הממוצעת היום לא נמוכה מהריבית שלכם, ולכן אין עמלת היוון.' : '');
      o.appendChild(U.answer('עמלת היוון אם פורעים היום', F.ils(r.fee), sub, st.ex));
      var li = [['היתרה היום' + (r.linked ? ', כולל הצמדה' : ''), F.ils(r.bal)], ['תשלומים ששולמו', F.num(r.el) + ' מתוך ' + F.num(r.N)]];
      if (r.linked) li.push(['ההצמדה למדד מאז ההלוואה', F.spc(100 * (r.ratio - 1), 1)]);
      li.push(['הריבית בהלוואה', F.pc(hv.rate)]);
      if (r.kind !== 'prime' && r.why !== 'reset') {
        li.push(['הממוצע היום, ' + r.labA + (r.kind === 'var5' ? ' עד שינוי הריבית' : ' שנותרו') + ', בתוקף מ־' + F.date(r.todayFrom), F.pc(r.Ae) + ' אפקטיבית · ' + F.pc(r.A) + ' לתשלום חודשי']);
        li.push(r.origFrom ? ['הממוצע ביום ההלוואה, ' + r.labC + ', בתוקף מ־' + F.date(r.origFrom), F.pc(r.Ce) + ' · ' + F.pc(r.C)] : ['הממוצע ביום ההלוואה', 'לא בקובץ שלנו, שמתחיל ב־' + F.month(D.prepay[r.file].rows[0][0].slice(0, 7))]);
        li.push(['סעיף 3(3): התשלומים שנותרו מהוונים בממוצע של היום, פחות היתרה', r.f3 > 0.5 ? F.ils(r.f3) : 'ללא: הממוצע לא נמוך מהריבית']);
        li.push(['סעיף 3(4): השינוי בממוצע מאז יום ההלוואה', r.f4 == null ? (r.origFrom ? 'לא חל: הממוצע אז לא היה נמוך מהריבית' : 'לא ניתן לבדוק') : F.ils(r.f4)]);
        li.push(['הבנק גובה את הנמוך מבין השניים, ' + (r.cut ? 'בהפחתה של ' + F.num(100 * r.cut) + '% לוותק' : 'בלי הפחתה: פחות מ־3 שנים'), F.ils(r.fee)]);
      }
      li.push(['עמלה תפעולית', 'עד ' + F.ils(r.op)], ['בהודעה של פחות מ־10 ימים (0.1%)', F.ils(r.notice)]);
      if (r.cpiFee > 0.5) li.push(['בפירעון בין ה־1 ל־15 בחודש (מחצית השינוי הממוצע במדד)', F.ils(r.cpiFee)]);
      o.appendChild(U.lines(li));
      o.appendChild(srcLine([U.srcHe(D, D.prepay[r.file].src, r.file === 'cpi' ? 'pribmash' : 'mashfix'), D.fees.src, r.linked && X.cpi ? { label: X.cpi.source, url: D.cpi.src.url } : null],
        'היתרה: לוח שפיצר בריבית שלכם מהחודש של ההלוואה' + (r.kind === 'var5' || r.kind === 'prime' ? ' (במסלול משתנה: כאילו הריבית של היום חלה מההתחלה)' : '') + (r.linked ? ', כפול המדד האחרון ÷ המדד של חודש ההלוואה' : '') + '. הממוצעים: קובצי בנק ישראל לעמלת פירעון מוקדם, ריבית אפקטיבית שהומרה לנומינלית (1 + ר)^(1/12) − 1; הממוצע ביום ההלוואה: הקובץ שהיה בתוקף ב־15 לחודש. מקורות: '));
      P.secs.innerHTML = '';
      paintRefi(L);
      if (L.later.length && r.kind !== 'prime') {
        var s = U.sec(P.secs, 'אם פורעים מאוחר יותר, בממוצעים של היום', 'אחרי 3 שנים מיום ההלוואה העמלה יורדת ב־20%, ואחרי 5 שנים ב־30%. אותם ממוצעים כמו היום; ביום הפירעון הם יהיו אחרים.');
        var rows = [{ cls: 'is-on', cells: [esc('היום, ' + F.month(NOW)), esc(F.ils(r.bal)), esc(F.ils(r.fee))] }].concat(L.later.map(function (x) {
          return { cells: [esc(F.month(x.at) + ', ' + (x.m / 12) + ' שנים מההלוואה'), esc(F.ils(x.r.bal)), esc(x.r.why === 'reset' ? 'ללא: יום שינוי הריבית' : F.ils(x.r.fee))] };
        }));
        s.appendChild(U.table(['מתי פורעים', 'היתרה', 'עמלת היוון'], rows, { num: [1, 2], cards: true }));
      }
    }

    /* ---------------------------------------------------------------- round E: "האם למחזר?" (the existing loan refinanced today) */
    var lastRefi = null;
    function refiOpts() { var hv = st.have, rf = st.refi; return { date: hv.date, amount: hv.amount, years: hv.years, k: hv.k, rate: hv.rate, newRate: rf.touched ? rf.rate : null, extra: rf.extra, notice: rf.notice !== 'long' }; }
    function avgLabel(a) {  // where the average comes from, and its month
      return a.via === 'prepay'
        ? 'הממוצע של בנק ישראל ל' + R.NAME[st.have.k] + ' של ' + a.lab + ' (התקופה שנותרה), בתוקף מ־' + F.date(a.from) + ', נתוני ' + F.month(a.month)
        : 'הממוצע של בנק ישראל ב' + R.NAME[st.have.k] + ', משכנתאות חדשות בכל הבנקים, ' + F.month(a.month);
    }
    function feeNone(x) { var k = R.KIND[st.have.k].kind; return k === 'prime' ? 'ללא: פריים' : x.fx.why === 'reset' ? 'ללא: יום שינוי הריבית' : 'ללא: הממוצע לא נמוך מהריבית'; }
    function nextChange() { return R.mAdd(st.have.date, 60 * Math.ceil(Math.max(1, R.mDiff(st.have.date, NOW)) / 60)); }
    function paintRefi(L) {
      if (!R.refiAvg || !R.refiExisting) return;  // an older cached mrates-common.js: the fee works as before, the refinance waits
      var fx = L.r, hv = st.have, rf = st.refi, K = R.KIND[hv.k], a = R.refiAvg(D, hv.k, fx.left), t2 = 0;
      lastRefi = null;
      if (rf.touched && rf.k && rf.k !== hv.k) { rf.touched = false; rf.rate = null; }  // a typed offer belongs to its track: another track opens at its own average
      var s = U.sec(P.secs, 'האם למחזר?', 'אם ממחזרים היום את היתרה, ' + F.ils(fx.bal) + ', ל־' + F.num(fx.left) + ' החודשים שנותרו באותו מסלול, בריבית הממוצעת של בנק ישראל: ההחזר החדש, ההפרש בחודש, העלויות של היציאה ובכמה חודשים החיסכון מכסה אותן. עלויות וחודשים, לא המלצה.');
      var g = el('div', 'nli__grid mrx__rfg'), f = el('form', 'nli__form'), o = el('div', 'nli__out');
      f.addEventListener('submit', function (e) { e.preventDefault(); }); o.setAttribute('aria-live', 'polite');
      g.appendChild(f); g.appendChild(o); s.appendChild(g);
      var help = a ? 'נפתח בממוצע של בנק ישראל: ' + esc(F.pc(a.eff)) + ' אפקטיבית, ' + esc(F.pc(a.nom)) + ' לתשלום חודשי. אם קיבלתם הצעה למחזור, הקלידו את הריבית שלה.' : 'אין בקובץ ממוצע למסלול הזה: הקלידו את הריבית שהוצעה לכם.';
      var fr = U.field('הריבית במחזור', rf.touched ? rf.rate : a ? a.nom : null, '%', function (n) { rf.touched = isFinite(n); rf.rate = rf.touched ? n : null; rf.k = hv.k; edited(); }, { dec: 2, help: help });
      var fe = U.field('עלויות נוספות (שמאי, פתיחת תיק)', rf.extra, '₪', function (n) { rf.extra = n > 0 ? n : null; edited(); }, { money: true, help: 'אינן בנתונים הרשמיים, ולכן השדה ריק. הקלידו את הסכום מההצעה שקיבלתם.' });
      var fn = U.seg('הודעה לבנק על הפירעון', [['short', 'פחות מ־10 ימים'], ['long', '10 ימים ומעלה']], rf.notice, function (k) { rf.notice = k; edited(); });
      var box = el('div', 'mrx__box'); [fr, fe, fn].forEach(function (x) { box.appendChild(x); }); f.appendChild(box);
      function edited() { st.ex = false; [].forEach.call(P.panel.querySelectorAll('.mrx__eg'), function (x) { x.parentNode.removeChild(x); }); clearTimeout(t2); t2 = setTimeout(draw, 90); }
      function draw() {
        fr._err.textContent = ''; o.innerHTML = ''; lastRefi = null;
        if (rf.touched && !(rf.rate >= 0 && rf.rate <= 20)) { fr._err.textContent = 'ריבית בין 0% ל־20%.'; return; }
        var x = R.refiExisting(refiOpts(), D, X.cpi, NOW, fx);
        if (!x) { o.appendChild(el('p', 'nli__note', 'אין בקובץ ממוצע של בנק ישראל למסלול הזה. הקלידו את הריבית שהוצעה לכם.')); return; }
        lastRefi = x;
        var b = function (v) { return '<bdi>' + esc(F.ils(v)) + '</bdi>'; }, ok = x.months != null && x.within, sub;
        if (x.months == null) sub = 'ההחזר אחרי מחזור, ' + b(x.newPay) + ', לא נמוך מההחזר היום, ' + b(x.oldPay) + ', ולכן אין חיסכון חודשי שיכסה עלויות של ' + b(x.cost) + '.';
        else if (!ok) sub = 'חיסכון של ' + b(x.save) + ' בחודש מול עלויות של ' + b(x.cost) + ': ' + esc(F.num(x.months)) + ' חודשים, יותר מ־' + esc(F.num(x.left)) + ' החודשים שנותרו להלוואה.';
        else sub = 'ההחזר יורד מ־' + b(x.oldPay) + ' ל־' + b(x.newPay) + ', חיסכון של ' + b(x.save) + ' בחודש, מול עלויות של ' + b(x.cost) + '. ' + esc(F.num(x.months)) + ' חודשים הם כ־' + esc(F.num(x.months / 12, 1)) + ' שנים, מתוך ' + esc(F.num(x.left)) + ' החודשים שנותרו.';
        var A = U.answer('בכמה חודשים החיסכון מכסה את העלויות', ok ? F.num(x.months) + ' חודשים' : 'לא משתלם כרגע', sub, st.ex);
        A.querySelector('.nli__fig').classList.add('is-he'); o.appendChild(A);
        var li = [['ההחזר היום, בריבית ' + F.pc(hv.rate) + (K.linked ? ', בשקלים של היום' : ''), F.ils(x.oldPay)],
          [x.own ? 'הריבית במחזור, כפי שהקלדתם' : avgLabel(a), x.own ? F.pc(x.rate) : F.pc(a.eff) + ' אפקטיבית · ' + F.pc(a.nom) + ' לתשלום חודשי'],
          ['ההחזר אחרי מחזור, ל־' + F.num(x.left) + ' חודשים', F.ils(x.newPay)],
          x.save >= 0.5 ? ['חיסכון בחודש', F.ils(x.save)] : x.save <= -0.5 ? ['תוספת בחודש', F.ils(-x.save)] : ['הפרש בחודש', F.ils(0)],
          ['עמלת היוון', x.fee > 0.5 ? F.ils(x.fee) : feeNone(x)],
          ['עמלה תפעולית', 'עד ' + F.ils(x.op)],
          ['הודעה של פחות מ־10 ימים (0.1% מהיתרה)', rf.notice === 'long' ? 'ללא: 10 ימים ומעלה' : F.ils(x.notice)],
          ['עלויות נוספות (שמאי, פתיחת תיק)', x.extra > 0 ? F.ils(x.extra) : 'לא הוקלדו'],
          ['סך העלויות', F.ils(x.cost)],
          ['חודשים עד שהחיסכון מכסה את העלויות', x.months == null ? 'אין חיסכון' : F.num(x.months) + (x.within ? ' מתוך ' + F.num(x.left) : ', יותר מ־' + F.num(x.left) + ' שנותרו')]];
        if (x.cpiFee > 0.5) li.push(['לא נכלל: בפירעון בין ה־1 ל־15 בחודש במסלול צמוד (מחצית השינוי הממוצע במדד)', F.ils(x.cpiFee)]);
        o.appendChild(U.lines(li));
        var why = K.kind === 'prime' ? 'במסלול הפריים אין עמלת היוון: הריבית משתנה במועד לא ידוע (צו הבנקאות, סעיף 4). נשארות העמלה התפעולית וההודעה המוקדמת.'
          : K.kind === 'var5' ? (fx.why === 'reset' ? 'החודש הוא יום שינוי הריבית במסלול, ובו אין עמלת היוון (צו הבנקאות, סעיף 4).' : 'במסלול משתנה עמלת ההיוון מחושבת רק עד יום שינוי הריבית הבא, ' + F.month(nextChange()) + ', וביום השינוי עצמו אין עמלת היוון (צו הבנקאות, סעיף 4).')
          : 'במסלול קבוע עמלת ההיוון מחושבת מהפרש התשלומים עד סוף ההלוואה, מהוון בריבית הממוצעת של היום (צו הבנקאות, סעיף 3), ולכן היא גדלה ככל שהחיסכון בחודש גדל.';
        o.appendChild(el('p', 'mrx__hint', esc(why)));
        var sa = null;
        if (a && a.via === 'prepay') { var h0 = U.srcHe(D, a.src, a.file === 'cpi' ? 'pribmash' : 'mashfix'); sa = { label: h0.label + ', בתוקף מ־' + F.date(a.from), url: h0.url }; }
        else if (a) sa = { label: 'בנק ישראל, השוואת ריביות במשכנתאות לפי בנק, ' + F.month(a.month), url: D.by_bank.src.page || D.by_bank.src.url };
        o.appendChild(srcLine([sa, D.fees.src], 'ההחזר: לוח שפיצר על היתרה של היום ל־' + F.num(x.left) + ' החודשים שנותרו, בריבית שלכם ובריבית במחזור' + (K.linked ? ', בשקלים של היום (שני ההחזרים צמודים לאותו מדד)' : '') + '. העמלה והעלויות משולמות בנפרד ואינן מתווספות להלוואה החדשה. חודשים עד שהחיסכון מכסה את העלויות = סך העלויות ÷ החיסכון בחודש, מעוגל כלפי מעלה, בלי היוון. ריבית אפקטיבית הומרה לנומינלית: (1 + ר)^(1/12) − 1. מקורות: '));
      }
      draw();
    }

    function state() { return { mo: st.mode, hz: st.hz, a: st.amount, y: st.years, s: st.src, r: st.rows.map(function (r) { return [r.k, Math.round(r.share * 1000) / 1000, Math.round(r.rate * 10000) / 10000]; }), hv: [st.have.date, st.have.amount, st.have.years, st.have.k, st.have.rate],
      rf: [st.refi.touched ? st.refi.rate : null, st.refi.extra, st.refi.notice] }; }
    function paintShare(L) {
      U.shareBar(P.share, function () {
        if (L.mode === 'have') {
          var r = L.r, x = lastRefi, tx = 'פירעון מוקדם היום: הלוואה של ' + F.ils(st.have.amount) + ' ב' + R.NAME[st.have.k] + ' מ־' + F.month(st.have.date) + ' בריבית ' + F.pc(st.have.rate) + ': יתרה ' + F.ils(r.bal) + ', עמלת היוון כ־' + F.ils(r.fee) + '.';
          if (x) tx += ' מחזור בריבית ' + F.pc(x.rate) + (x.own ? '' : ' (הממוצע של בנק ישראל)') + ': החזר ' + F.ils(x.newPay) + ' במקום ' + F.ils(x.oldPay) + (x.months != null && x.within ? ', והחיסכון מכסה עלויות של ' + F.ils(x.cost) + ' אחרי ' + F.num(x.months) + ' חודשים.' : ', לא משתלם כרגע מול עלויות של ' + F.ils(x.cost) + '.');
          return tx;
        }
        var me = L.res[0]; return 'כמה תעלה היציאה: משכנתא של ' + F.ils(st.amount) + ' ל־' + F.num(st.years) + ' שנה, ' + (st.hz === 'end' ? 'עד הסוף' : 'יציאה בעוד ' + F.num(L.y) + ' שנים') + ': ריבית, הצמדה ועמלה ' + F.ils(me.price) + ' בתמהיל שלי' + (me.end ? '.' : ' (עמלה צפויה ' + F.ils(me.fee) + ').');
      }, function () { return U.link('mexit', state()); });
    }

    buildForm(); run();
    U.resized(function () { if (last && last.mode === 'plan') paintPlanSecs(last); });
  }
})();
