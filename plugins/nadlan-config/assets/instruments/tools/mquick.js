/* NadLan Instruments · mquick v1 (1.72.587; v2 1.72.588: the amount field first, id-scoped rules over the theme, the tools switcher; HAD-675, Ben 5.11.2026): the quick mortgage calculator at the top of
   /mortgage-calculator/. Three ways in (the loan, the price and equity, or the payment you can carry), a term and whose average
   mix: all the banks or one bank. The answer is the first monthly payment (or the loan that payment carries), the total repaid and
   the interest, at the Bank of Israel average track mix and effective rates of the latest month (data boi-mortgage.json,
   by_bank: TamInt010.xls). Spitzer schedule per track, monthly rate = (1 + e)^(1/12) - 1, CPI tracks with the index unchanged.
   1,000,000 ILS over 25 years at the system mix of 2026-09 gives 5,428 ILS (the page states the same number). Pure math in NLMQ.
   v3 (HAD-675, English twin /en/mortgage-calculator/): when the tool's section says lang="en" (NadLanInstruments.langOf), every
   word is English, the surface is LTR (shekel sign before the number), bank names come from by_bank.banks[].en, months are English,
   numbers en-US, and the two buttons point at the English page's own anchors (#amortization-schedule, #mortgage-market). An extra
   style block (#nlmq-css-en) is added only in English. The Hebrew surface is byte-identical to v2. */
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

  /* 1.72.588: the tools switcher on the mortgage page. Without scripts every panel shows (readers, search engines, AI answers);
     with scripts one panel at a time, chosen from the chips (MoneySavingExpert's pattern), never a table of contents. #tool-xxx opens a panel. */
  function wireSwitch() {
    ensureCss();
    [].forEach.call(document.querySelectorAll('.nlmx-sw:not([data-on])'), function (sw) {
      sw.setAttribute('data-on', '1');
      var bs = [].slice.call(sw.querySelectorAll('button[data-sw]')), ps = bs.map(function (b) { return document.getElementById(b.getAttribute('data-sw')); });
      function show(id, scroll) {
        bs.forEach(function (b, i) { var on = b.getAttribute('data-sw') === id; b.setAttribute('aria-pressed', String(on)); if (ps[i]) ps[i].hidden = !on; });
        if (scroll) { var p = document.getElementById(id); if (p && p.scrollIntoView) p.scrollIntoView({ block: 'start', behavior: 'smooth' }); }
      }
      bs.forEach(function (b) { b.addEventListener('click', function () { var id = b.getAttribute('data-sw'); show(id, false); try { history.replaceState(null, '', '#' + id); } catch (e) { /* file or sandbox */ } }); });
      var h = (location.hash || '').slice(1), first = bs.length ? bs[0].getAttribute('data-sw') : '';
      show(bs.some(function (b) { return b.getAttribute('data-sw') === h; }) ? h : first, !!h && h.indexOf('tool-') === 0);
      document.addEventListener('click', function (e) { var a = e.target && e.target.closest ? e.target.closest('a[href^="#tool-"]') : null; if (a) { var id = a.getAttribute('href').slice(1); if (document.getElementById(id)) { e.preventDefault(); show(id, true); } } });
    });
  }
  var NI = window.NadLanInstruments, esc = NI.esc;
  var nf = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  function ils(x) { return nf.format(Math.round(x || 0)) + ' ₪'; }
  function num(s) { var n = parseFloat(String(s).replace(/[^\d.]/g, '')); return isFinite(n) ? n : NaN; }
  var HEM = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];
  function month(ym) { var p = String(ym).split('-'); return p.length === 2 ? (HEM[+p[1] - 1] || p[1]) + ' ' + p[0] : ym; }
  var nfEn = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
  function ilsEn(x) { return '₪' + nfEn.format(Math.round(x || 0)); }
  var ENM = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  function monthEn(ym) { var p = String(ym).split('-'); return p.length === 2 ? (ENM[+p[1] - 1] || p[1]) + ' ' + p[0] : ym; }
  var CSS_EN = '#nlmq[lang="en"]{font-family:"IBM Plex Sans","IBM Plex Sans Hebrew",system-ui,sans-serif}'
    + '#nlmq[lang="en"] h2.nlmq__h{font-family:"IBM Plex Sans",system-ui,sans-serif!important}'
    + '#nlmq[lang="en"] .nlmq__in input{text-align:left}#nlmq[lang="en"] .nlmq__src{direction:ltr}';
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
    + '@media (min-width:900px){.nlmq{padding:24px}}'
    + '#nlmq h2.nlmq__h{margin:0!important;padding:0!important;font-size:17px!important;line-height:24px!important;color:#3E4C58!important;border:0!important;font-weight:600!important}#nlmq h2.nlmq__h::before,#nlmq h2.nlmq__h::after{display:none!important}'
    + '#nlmq p.nlmq__src{margin:0!important;font:400 12px/18px "IBM Plex Mono",ui-monospace,monospace!important;color:#5E6A75!important}'
    + '#nlmq .nlmq__seg button{border-radius:2px!important;padding:4px 6px!important;min-height:44px!important;font-size:14px!important;box-shadow:none!important}#nlmq .nlmq__chips button,#nlmq button.nlmq__copy{border-radius:999px!important;box-shadow:none!important;min-height:44px!important}'
    + '#nlmq .nlmq__seg--3 button{font-size:13px!important}#nlmq .nlmq__modes{margin-top:-6px}'
    + '.nlmx-sw{margin:8px 0 18px}.nlmx-sw__chips{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 14px}.nlmx-sw__chips button{min-height:44px;padding:0 14px;border-radius:999px!important;border:1px solid #D3DCE2;background:#fff;color:#3E4C58;font:500 14px/1.2 "IBM Plex Sans Hebrew",system-ui,sans-serif;cursor:pointer;box-shadow:none!important}'
    + '.nlmx-sw__chips button[aria-pressed="true"]{background:#2F6F86;border-color:#2F6F86;color:#fff;font-weight:600}.nlmx-sw__chips button:focus-visible{outline:2px solid #2F6F86;outline-offset:2px}.nlmx-pane[hidden]{display:none!important}';

  NI.register('mquick', {
    custom: function (root, data) {
      var D = data.boim || data.d0, bb = D && D.by_bank;
      if (!bb || !bb.months) return;
      ensureCss();
      var EN = !!(NI.langOf && NI.langOf(root) === 'en');  // v3: English on /en/ (the section's lang); Hebrew otherwise, unchanged
      if (EN && !document.getElementById('nlmq-css-en')) { var st2 = document.createElement('style'); st2.id = 'nlmq-css-en'; st2.textContent = CSS_EN; document.head.appendChild(st2); }
      var IL = EN ? ilsEn : ils, NF = EN ? nfEn : nf, MO = EN ? monthEn : month;
      var T = EN ? {
        all: 'All banks', who_all: 'all banks', h: 'Quick mortgage calculator', amount: 'Mortgage amount', price: 'Home price', equity: 'Your equity (down payment)',
        pay: 'The monthly payment that suits you', ml: 'You can also calculate', m_amount: 'By amount', m_price: 'By price and equity', m_pay: 'By monthly payment',
        tl: 'Term (years)', yr: '', bl: 'Average rate and mix of', principal: 'Principal', interest: 'Interest',
        cta: '<a class="nlmq__btn is-main" href="#amortization-schedule">Yearly amortization schedule</a><a class="nlmq__btn" href="#mortgage-market">Rates by bank this month</a>',
        copy: 'Copy the result', copied: 'Copied', prompt: 'Copy the result'
      } : {
        all: 'כל הבנקים', who_all: 'כל הבנקים', h: 'מחשבון משכנתא מהיר', amount: 'סכום המשכנתא', price: 'מחיר הדירה', equity: 'הון עצמי',
        pay: 'ההחזר החודשי שמתאים לכם', ml: 'אפשר לחשב גם', m_amount: 'לפי סכום', m_price: 'לפי מחיר והון עצמי', m_pay: 'לפי החזר חודשי',
        tl: 'תקופה', yr: ' שנה', bl: 'ריבית ותמהיל ממוצעים לפי', principal: 'הקרן', interest: 'ריבית',
        cta: '<a class="nlmq__btn is-main" href="#mortgage-tool">תמהיל מלא, מסלולים ולוח סילוקין</a><a class="nlmq__btn" href="#bank-offer-check">יש לי הצעה מהבנק: לבדוק אותה</a>',
        copy: 'העתקת התוצאה', copied: 'הועתק', prompt: 'העתיקו את התוצאה'
      };
      // one money field; in English the shekel sign stands before the number (LTR), in Hebrew after it (as before)
      function fld(id, k, lab) { var inp = '<input id="' + id + '" inputmode="numeric" autocomplete="off" data-k="' + k + '">'; return '<div><label class="nlmq__lab" for="' + id + '">' + lab + '</label><div class="nlmq__in">' + (EN ? '<span>₪</span>' + inp : inp + '<span>₪</span>') + '</div></div>'; }
      var names = {}; (bb.banks || []).forEach(function (b) { names[b.k] = EN ? ({ hapoalim: 'Hapoalim', leumi: 'Leumi', discount: 'Discount', mizrahi: 'Mizrahi-Tefahot', fibi: 'First International', mercantile: 'Mercantile', jerusalem: 'Jerusalem' }[b.k] || b.en || b.he) : b.he; }); names.system = T.all;
      var order = ['system'].concat(Object.keys(bb.rate).filter(function (k) { return k !== 'system'; }));
      var v = { mode: 'amount', amount: 1000000, price: 1600000, equity: 400000, pay: 6000, years: 25, bank: 'system' };
      var src = bb.src || {};
      var h = '<div class="nlmq" id="nlmq" dir="' + (EN ? 'ltr' : 'rtl') + '" lang="' + (EN ? 'en' : 'he') + '">'
        + '<h2 class="nlmq__h">' + T.h + '</h2>'
        + '<div class="nlmq__row" data-f="amount">' + fld('nlmq-a', 'amount', T.amount) + '</div>'
        + '<div class="nlmq__row" data-f="price" hidden>' + fld('nlmq-p', 'price', T.price)
        + fld('nlmq-e', 'equity', T.equity) + '</div>'
        + '<div class="nlmq__row" data-f="pay" hidden>' + fld('nlmq-y', 'pay', T.pay) + '</div>'
        + '<div class="nlmq__modes"><span class="nlmq__lab" id="nlmq-ml">' + T.ml + '</span><div class="nlmq__seg nlmq__seg--3" role="group" aria-labelledby="nlmq-ml">'
        + '<button type="button" data-m="amount">' + T.m_amount + '</button><button type="button" data-m="price">' + T.m_price + '</button><button type="button" data-m="pay">' + T.m_pay + '</button></div></div>'
        + '<div><span class="nlmq__lab" id="nlmq-tl">' + T.tl + '</span><div class="nlmq__seg nlmq__seg--4" role="group" aria-labelledby="nlmq-tl">'
        + [15, 20, 25, 30].map(function (y) { return '<button type="button" data-y="' + y + '">' + y + T.yr + '</button>'; }).join('') + '</div></div>'
        + '<div><span class="nlmq__lab" id="nlmq-bl">' + T.bl + '</span><div class="nlmq__chips" role="group" aria-labelledby="nlmq-bl">'
        + order.map(function (k) { return '<button type="button" data-b="' + esc(k) + '">' + esc(names[k] || k) + '</button>'; }).join('') + '</div></div>'
        + '<div class="nlmq__out" aria-live="polite"><span class="nlmq__ol"></span><span class="nlmq__fig"></span><span class="nlmq__sub"></span>'
        + '<div class="nlmq__bar" aria-hidden="true"><i class="p"></i><i class="r"></i></div>'
        + '<div class="nlmq__key"><span><b style="background:#F2D15A"></b>' + T.principal + '</span><span><b style="background:#8E7CC3"></b>' + T.interest + '</span></div>'
        + '<span class="nlmq__ltv" hidden></span></div>'
        + '<p class="nlmq__src"></p>'
        + '<div class="nlmq__cta">' + T.cta + '</div>'
        + '<button type="button" class="nlmq__copy">' + T.copy + '</button>'
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
        var who = v.bank === 'system' ? T.who_all : (EN ? '' : 'בנק ') + (names[v.bank] || v.bank);
        if (v.mode === 'pay') {
          q('.nlmq__ol').textContent = EN ? 'The mortgage this payment carries' : 'המשכנתא שההחזר הזה נושא';
          q('.nlmq__fig').innerHTML = '<bdi>' + IL(r.loan) + '</bdi>';
        } else {
          q('.nlmq__ol').textContent = EN ? 'First monthly payment' : 'ההחזר החודשי הראשון';
          q('.nlmq__fig').innerHTML = '<bdi>' + IL(r.pay) + '</bdi>';
        }
        q('.nlmq__sub').innerHTML = EN
          ? (v.mode === 'pay' ? 'Payment <bdi>' + IL(r.pay) + '</bdi> · ' : '') + 'Total repaid <bdi>' + IL(r.total) + '</bdi> · of which interest <bdi>' + IL(r.interest) + '</bdi>'
          : (v.mode === 'pay' ? 'החזר <bdi>' + ils(r.pay) + '</bdi> · ' : '') + 'סך ההחזרים <bdi>' + ils(r.total) + '</bdi> · מזה ריבית <bdi>' + ils(r.interest) + '</bdi>';
        var tot = r.total > 0 ? r.total : 1;
        q('.nlmq__bar .p').style.width = (r.loan / tot * 100).toFixed(1) + '%';
        q('.nlmq__bar .r').style.width = (r.interest / tot * 100).toFixed(1) + '%';
        var lt = q('.nlmq__ltv');
        if (r.ltv != null) {
          var over = r.ltv > 0.75;
          lt.hidden = false; lt.className = 'nlmq__ltv' + (over ? ' is-over' : '');
          lt.innerHTML = EN
            ? 'Loan to value <bdi>' + (r.ltv * 100).toFixed(1) + '%</bdi>' + (over ? ': above 75%, the Bank of Israel maximum for a single home (70% for a replacement home, 50% for an additional home).' : ' (up to 75% for a single home, 70% for a replacement home, 50% for an additional home).')
            : 'שיעור המימון <bdi>' + (r.ltv * 100).toFixed(1) + '%</bdi>' + (over ? ': מעל 75%, המימון המרבי של בנק ישראל לדירה יחידה (70% לדירה חלופית, 50% לדירה נוספת).' : ' (עד 75% לדירה יחידה, 70% לדירה חלופית, 50% לדירה נוספת).');
        } else { lt.hidden = true; }
        q('.nlmq__src').innerHTML = EN
          ? 'Spitzer schedule; the five tracks at the average mix and effective rates of ' + esc(who) + ' in ' + esc(MO(r.month))
            + ', CPI-linked tracks with the index unchanged. Source: ' + ((src.page_en || src.page) ? '<a href="' + esc(src.page_en || src.page) + '" target="_blank" rel="noopener">Bank of Israel, interest rate comparisons for housing loans</a>' : 'Bank of Israel') + '. An average, not a personal offer.'
          : 'לוח שפיצר, חמשת המסלולים לפי התמהיל והריבית האפקטיבית הממוצעים של ' + esc(who) + ' ב' + esc(month(r.month))
            + ', במסלולים הצמודים בלי שינוי במדד. מקור: ' + (src.page ? '<a href="' + esc(src.page) + '" target="_blank" rel="noopener">בנק ישראל, השוואת ריביות בהלוואות לדיור</a>' : 'בנק ישראל') + '. ממוצע, לא הצעה אישית.';
      }
      qa('input[data-k]').forEach(function (inp) {
        var k = inp.getAttribute('data-k'); inp.value = NF.format(v[k]);
        inp.addEventListener('input', function () { var n = num(inp.value); if (isFinite(n)) { v[k] = n; paint(); } });
        inp.addEventListener('blur', function () { inp.value = NF.format(v[k]); });
      });
      root.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b || !root.contains(b)) return;
        if (b.hasAttribute('data-m')) { v.mode = b.getAttribute('data-m'); paint(); }
        else if (b.hasAttribute('data-y')) { v.years = +b.getAttribute('data-y'); paint(); }
        else if (b.hasAttribute('data-b')) { v.bank = b.getAttribute('data-b'); paint(); }
        else if (b.classList.contains('nlmq__copy') && last) {
          var who = v.bank === 'system' ? T.who_all : (EN ? '' : 'בנק ') + (names[v.bank] || v.bank);
          var tx = EN
            ? 'A ' + IL(last.loan) + ' mortgage over ' + v.years + ' years at the average mix of ' + who + ' in ' + MO(last.month) + ': first payment ' + IL(last.pay) + ', total repaid ' + IL(last.total) + '.\n' + location.origin + location.pathname
            : 'משכנתא של ' + ils(last.loan) + ' ל־' + v.years + ' שנה, בתמהיל הממוצע של ' + who + ' ב' + month(last.month) + ': החזר ראשון ' + ils(last.pay) + ', סך ההחזרים ' + ils(last.total) + '.\n' + location.origin + location.pathname;
          var done = function () { b.textContent = T.copied; setTimeout(function () { b.textContent = T.copy; }, 1600); };
          if (navigator.clipboard) navigator.clipboard.writeText(tx).then(done, function () { window.prompt(T.prompt, tx); }); else window.prompt(T.prompt, tx);
        }
      });
      paint();
    }
  });
  /* 1.72.590: the style is written once CSS is defined (1.72.588 ran the switcher before it and left an empty style element) */
  function ensureCss() { var s = document.getElementById('nlmq-css'); if (!s) { s = document.createElement('style'); s.id = 'nlmq-css'; document.head.appendChild(s); } if (!s.textContent) s.textContent = CSS; }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wireSwitch); else wireSwitch();
})();
