/* NadLan Instruments · mquick v1 (1.72.587, HAD-675, Ben 5.11.2026): the quick mortgage calculator at the top of
   /mortgage-calculator/. Three ways in (the loan, the price and equity, or the payment you can carry), a term and whose average
   mix: all the banks or one bank. The answer is the first monthly payment (or the loan that payment carries), the total repaid and
   the interest, at the Bank of Israel average track mix and effective rates of the latest month (data boi-mortgage.json,
   by_bank: TamInt010.xls). Spitzer schedule per track, monthly rate = (1 + e)^(1/12) - 1, CPI tracks with the index unchanged.
   1,000,000 ILS over 25 years at the system mix of 2026-09 gives 5,428 ILS (the page states the same number). Pure math in NLMQ. */
(function () {
  'use strict';
  var TR = ['fixed_nl', 'prime', 'var_nl_other', 'var_cpi', 'fixed_cpi'];
  function payPer1(bb, bank, i, years) {  // the first payment on 1 ILS at a bank's average mix and rates of month index i
    var mix = bb.mix[bank], rate = bb.rate[bank], n = years * 12, tot = 0, pay = 0, k;
    if (!mix || !rate) return 0;
    for (k = 0; k < TR.length; k++) tot += +mix[TR[k]][i] || 0;
    if (!(tot > 0)) return 0;
    for (k = 0; k < TR.length; k++) {
      var p = (+mix[TR[k]][i] || 0) / tot, r = Math.pow(1 + (+rate[TR[k]][i] || 0) / 100, 1 / 12) - 1;
      pay += r > 0 ? p * r / (1 - Math.pow(1 + r, -n)) : p / n;
    }
    return pay;
  }
  function solve(v, bb) {
    var i = bb.months.length - 1, per1 = payPer1(bb, v.bank, i, v.years), loan, pay;
    if (v.mode === 'pay') { pay = Math.max(0, v.pay); loan = per1 > 0 ? pay / per1 : 0; }
    else { loan = v.mode === 'price' ? Math.max(0, v.price - v.equity) : Math.max(0, v.amount); pay = loan * per1; }
    var n = v.years * 12, total = pay * n;
    return { loan: loan, pay: pay, total: total, interest: Math.max(0, total - loan), ltv: v.mode === 'price' && v.price > 0 ? loan / v.price : null, month: bb.months[i], per1: per1 };
  }
  window.NLMQ = { payPer1: payPer1, solve: solve, TR: TR };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, esc = NI.esc;
  var nf = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function ils(x) { return nf.format(Math.round(x || 0)) + ' ₪'; }
  function num(s) { var n = parseFloat(String(s).replace(/[^\d.]/g, '')); return isFinite(n) ? n : NaN; }
  var HEM = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
  function month(ym) { var p = String(ym).split('-'); return p.length === 2 ? (HEM[+p[1] - 1] || p[1]) + ' ' + p[0] : ym; }
  var CSS = '.nlmq{font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#12202A;background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:16px;display:flex;flex-direction:column;gap:16px;margin:8px 0 16px}'
    + '.nlmq *{box-sizing:border-box}.nlmq .nlmq__h{margin:0!important;font:600 18px/26px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}'
    + '.nlmq__lab{display:block;font-size:13px;line-height:18px;font-weight:500;color:#3E4C58;margin:0 0 8px}'
    + '.nlmq__seg{display:grid;gap:8px}.nlmq__seg--3{grid-template-columns:repeat(3,minmax(0,1fr))}.nlmq__seg--4{grid-template-columns:repeat(4,minmax(0,1fr))}'
    + '.nlmq button,.nlmq a.nlmq__btn{font-family:inherit;cursor:pointer}'
    + '.nlmq__seg button{min-height:44px;border-radius:2px;border:1px solid #D3DCE2;background:#fff;color:#3E4C58;font-size:14px;line-height:1.2;padding:4px 6px}'
    + '.nlmq__seg button[aria-pressed="true"]{background:#2F6F86;border-color:#2F6F86;color:#fff;font-weight:600}'
    + '.nlmq__chips{display:flex;flex-wrap:wrap;gap:8px}.nlmq__chips button{min-height:44px;padding:0 14px;border-radius:999px;border:1px solid #D3DCE2;background:#fff;color:#3E4C58;font-size:14px}'
    + '.nlmq__chips button[aria-pressed="true"]{background:#2F6F86;border-color:#2F6F86;color:#fff;font-weight:600}'
    + '.nlmq__in{display:flex;align-items:center;gap:8px;height:48px;padding:0 12px;border:1px solid #2F6F86;border-radius:2px;background:#fff}'
    + '.nlmq__in input{flex:1 1 auto;min-width:0;border:0!important;outline:0;background:transparent!important;font:400 20px/1 "IBM Plex Mono",ui-monospace,monospace!important;color:#12202A;text-align:right;padding:0!important;box-shadow:none!important;height:auto!important}'
    + '.nlmq__in span{font:400 16px/1 "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}'
    + '.nlmq__row{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:12px}'
    + '.nlmq__out{display:flex;flex-direction:column;gap:6px;border-top:1px solid #D3DCE2;padding-top:12px}'
    + '.nlmq__ol{font-size:13px;line-height:18px;font-weight:500;color:#3E4C58}.nlmq__fig{font:500 40px/44px "IBM Plex Mono",ui-monospace,monospace;color:#12202A}'
    + '.nlmq__sub{font:400 13px/20px "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}.nlmq__bar{display:flex;height:10px;border-radius:2px;overflow:hidden;background:#E7EEF2}'
    + '.nlmq__bar i{display:block;height:100%}.nlmq__bar i.p{background:#F2D15A}.nlmq__bar i.r{background:#8E7CC3}'
    + '.nlmq__key{display:flex;gap:16px;font-size:12px;line-height:16px;color:#5E6A75}.nlmq__key span{display:inline-flex;align-items:center;gap:4px}.nlmq__key b{display:inline-block;width:10px;height:10px}'
    + '.nlmq__ltv{font-size:14px;line-height:20px;color:#3E4C58}.nlmq__ltv.is-over bdi{text-decoration:underline;text-decoration-color:#C42550;text-decoration-thickness:2px;text-underline-offset:5px;color:#12202A}'
    + '.nlmq__src{margin:0;font:400 12px/18px "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}.nlmq__src a{color:#2F6F86}'
    + '.nlmq__cta{display:flex;flex-direction:column;gap:8px}@media (min-width:700px){.nlmq__cta{flex-direction:row;flex-wrap:wrap}}'
    + '.nlmq a.nlmq__btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 18px;border-radius:2px;border:1px solid #2F6F86;background:#fff;color:#2F6F86!important;text-decoration:none!important;font-weight:600;font-size:15px}'
    + '.nlmq a.nlmq__btn.is-main{background:#2F6F86;color:#fff!important}'
    + '.nlmq__copy{align-self:flex-start;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid #D3DCE2;background:#fff;color:#3E4C58;font-size:14px}'
    + '.nlmq button:focus-visible,.nlmq a:focus-visible,.nlmq__in:focus-within{outline:2px solid #2F6F86;outline-offset:2px}'
    + '@media (min-width:900px){.nlmq{padding:24px}}';

  NI.register('mquick', {
    custom: function (root, data) {
      var D = data.boim || data.d0, bb = D && D.by_bank;
      if (!bb || !bb.months) return;
      if (!document.getElementById('nlmq-css')) { var st = document.createElement('style'); st.id = 'nlmq-css'; st.textContent = CSS; document.head.appendChild(st); }
      var names = {}; (bb.banks || []).forEach(function (b) { names[b.k] = b.he; }); names.system = 'כל הבנקים';
      var order = ['system'].concat(Object.keys(bb.rate).filter(function (k) { return k !== 'system'; }));
      var v = { mode: 'amount', amount: 1000000, price: 1600000, equity: 400000, pay: 6000, years: 25, bank: 'system' };
      var src = bb.src || {};
      var h = '<div class="nlmq" dir="rtl" lang="he">'
        + '<h2 class="nlmq__h">מחשבון משכנתא מהיר</h2>'
        + '<div><span class="nlmq__lab" id="nlmq-ml">איך מחשבים</span><div class="nlmq__seg nlmq__seg--3" role="group" aria-labelledby="nlmq-ml">'
        + '<button type="button" data-m="amount">לפי סכום</button><button type="button" data-m="price">לפי מחיר והון עצמי</button><button type="button" data-m="pay">לפי החזר חודשי</button></div></div>'
        + '<div class="nlmq__row" data-f="amount"><div><label class="nlmq__lab" for="nlmq-a">סכום המשכנתא</label><div class="nlmq__in"><input id="nlmq-a" inputmode="numeric" autocomplete="off" data-k="amount"><span>₪</span></div></div></div>'
        + '<div class="nlmq__row" data-f="price" hidden><div><label class="nlmq__lab" for="nlmq-p">מחיר הדירה</label><div class="nlmq__in"><input id="nlmq-p" inputmode="numeric" autocomplete="off" data-k="price"><span>₪</span></div></div>'
        + '<div><label class="nlmq__lab" for="nlmq-e">הון עצמי</label><div class="nlmq__in"><input id="nlmq-e" inputmode="numeric" autocomplete="off" data-k="equity"><span>₪</span></div></div></div>'
        + '<div class="nlmq__row" data-f="pay" hidden><div><label class="nlmq__lab" for="nlmq-y">ההחזר החודשי שמתאים לכם</label><div class="nlmq__in"><input id="nlmq-y" inputmode="numeric" autocomplete="off" data-k="pay"><span>₪</span></div></div></div>'
        + '<div><span class="nlmq__lab" id="nlmq-tl">תקופה</span><div class="nlmq__seg nlmq__seg--4" role="group" aria-labelledby="nlmq-tl">'
        + [15, 20, 25, 30].map(function (y) { return '<button type="button" data-y="' + y + '">' + y + ' שנה</button>'; }).join('') + '</div></div>'
        + '<div><span class="nlmq__lab" id="nlmq-bl">ריבית ותמהיל ממוצעים לפי</span><div class="nlmq__chips" role="group" aria-labelledby="nlmq-bl">'
        + order.map(function (k) { return '<button type="button" data-b="' + esc(k) + '">' + esc(names[k] || k) + '</button>'; }).join('') + '</div></div>'
        + '<div class="nlmq__out" aria-live="polite"><span class="nlmq__ol"></span><span class="nlmq__fig"></span><span class="nlmq__sub"></span>'
        + '<div class="nlmq__bar" aria-hidden="true"><i class="p"></i><i class="r"></i></div>'
        + '<div class="nlmq__key"><span><b style="background:#F2D15A"></b>הקרן</span><span><b style="background:#8E7CC3"></b>ריבית</span></div>'
        + '<span class="nlmq__ltv" hidden></span></div>'
        + '<p class="nlmq__src"></p>'
        + '<div class="nlmq__cta"><a class="nlmq__btn is-main" href="#mortgage-tool">תמהיל מלא, מסלולים ולוח סילוקין</a><a class="nlmq__btn" href="#bank-offer-check">יש לי הצעה מהבנק: לבדוק אותה</a></div>'
        + '<button type="button" class="nlmq__copy">העתקת התוצאה</button>'
        + '</div>';
      root.innerHTML = h;
      var q = function (s) { return root.querySelector(s); }, qa = function (s) { return [].slice.call(root.querySelectorAll(s)); };
      var last = null;
      function paint() {
        qa('[data-m]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-m') === v.mode)); });
        qa('[data-f]').forEach(function (r) { r.hidden = r.getAttribute('data-f') !== v.mode; });
        qa('[data-y]').forEach(function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-y') === v.years)); });
        qa('[data-b]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-b') === v.bank)); });
        var r = solve(v, bb); last = r;
        var who = v.bank === 'system' ? 'כל הבנקים' : 'בנק ' + (names[v.bank] || v.bank);
        if (v.mode === 'pay') {
          q('.nlmq__ol').textContent = 'המשכנתא שההחזר הזה נושא';
          q('.nlmq__fig').innerHTML = '<bdi>' + ils(r.loan) + '</bdi>';
        } else {
          q('.nlmq__ol').textContent = 'ההחזר החודשי הראשון';
          q('.nlmq__fig').innerHTML = '<bdi>' + ils(r.pay) + '</bdi>';
        }
        q('.nlmq__sub').innerHTML = (v.mode === 'pay' ? 'החזר <bdi>' + ils(r.pay) + '</bdi> · ' : '') + 'סך ההחזרים <bdi>' + ils(r.total) + '</bdi> · מזה ריבית <bdi>' + ils(r.interest) + '</bdi>';
        var tot = r.total > 0 ? r.total : 1;
        q('.nlmq__bar .p').style.width = (r.loan / tot * 100).toFixed(1) + '%';
        q('.nlmq__bar .r').style.width = (r.interest / tot * 100).toFixed(1) + '%';
        var lt = q('.nlmq__ltv');
        if (r.ltv != null) {
          var over = r.ltv > 0.75;
          lt.hidden = false; lt.className = 'nlmq__ltv' + (over ? ' is-over' : '');
          lt.innerHTML = 'שיעור המימון <bdi>' + (r.ltv * 100).toFixed(1) + '%</bdi>' + (over ? ': מעל 75%, המימון המרבי של בנק ישראל לדירה יחידה (70% לדירה חלופית, 50% לדירה נוספת).' : ' (עד 75% לדירה יחידה, 70% לדירה חלופית, 50% לדירה נוספת).');
        } else { lt.hidden = true; }
        q('.nlmq__src').innerHTML = 'לוח שפיצר, חמשת המסלולים לפי התמהיל והריבית האפקטיבית הממוצעים של ' + esc(who) + ' ב' + esc(month(r.month))
          + ', במסלולים הצמודים בלי שינוי במדד. מקור: ' + (src.page ? '<a href="' + esc(src.page) + '" target="_blank" rel="noopener">בנק ישראל, השוואת ריביות בהלוואות לדיור</a>' : 'בנק ישראל') + '. ממוצע, לא הצעה אישית.';
      }
      qa('input[data-k]').forEach(function (inp) {
        var k = inp.getAttribute('data-k'); inp.value = nf.format(v[k]);
        inp.addEventListener('input', function () { var n = num(inp.value); if (isFinite(n)) { v[k] = n; paint(); } });
        inp.addEventListener('blur', function () { inp.value = nf.format(v[k]); });
      });
      root.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b || !root.contains(b)) return;
        if (b.hasAttribute('data-m')) { v.mode = b.getAttribute('data-m'); paint(); }
        else if (b.hasAttribute('data-y')) { v.years = +b.getAttribute('data-y'); paint(); }
        else if (b.hasAttribute('data-b')) { v.bank = b.getAttribute('data-b'); paint(); }
        else if (b.classList.contains('nlmq__copy') && last) {
          var who = v.bank === 'system' ? 'כל הבנקים' : 'בנק ' + (names[v.bank] || v.bank);
          var tx = 'משכנתא של ' + ils(last.loan) + ' ל־' + v.years + ' שנה, בתמהיל הממוצע של ' + who + ' ב' + month(last.month) + ': החזר ראשון ' + ils(last.pay) + ', סך ההחזרים ' + ils(last.total) + '.\n' + location.origin + location.pathname;
          var done = function () { b.textContent = 'הועתק'; setTimeout(function () { b.textContent = 'העתקת התוצאה'; }, 1600); };
          if (navigator.clipboard) navigator.clipboard.writeText(tx).then(done, function () { window.prompt('העתיקו את התוצאה', tx); }); else window.prompt('העתיקו את התוצאה', tx);
        }
      });
      paint();
    }
  });
})();
