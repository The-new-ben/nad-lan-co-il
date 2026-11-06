/* NadLan Instruments · mnomeff v1 (HAD-675, mortgage delta row A8, 6.11.2026): "ריבית נומינלית וריבית אפקטיבית", a two-field
   converter like the Bank of Israel one, for the tools switcher of /mortgage-calculator/ (pane #tool-nomeff).
   Monthly payments: effective e = (1 + n/12)^12 - 1; nominal n = 12((1 + e)^(1/12) - 1). Typing in one field fills the other.
   The example and the five chips are the all-banks ("system") average effective rates of the latest month of boi-mortgage.json
   (by_bank, TamInt010.xls: "rates are annual adjusted (effective) rates"), labelled with their month; the default example is the
   fixed not linked track. One honest line: the bank publishes effective rates, and the tools on this page turn them into a monthly
   rate with this formula (mquick.js, mkeys.js: (1 + e)^(1/12) - 1).
   Pure logic in window.NLNE (node test: docs/research/2026-11-06-mortgage-delta/build-mzakaut/test_mzakaut.js). Hebrew only, RTL. */
(function () {
  'use strict';
  var G = typeof window !== 'undefined' ? window : globalThis;
  var TR = [{ k: 'fixed_nl', he: 'קבועה לא צמודה' }, { k: 'prime', he: 'פריים' }, { k: 'var_nl_other', he: 'משתנה לא צמודה' }, { k: 'fixed_cpi', he: 'קבועה צמודה' }, { k: 'var_cpi', he: 'משתנה צמודה' }];
  var HEM = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'];

  /* percent in, percent out */
  function toEff(nPct) { return 100 * (Math.pow(1 + nPct / 1200, 12) - 1); }
  function toNom(ePct) { return 1200 * (Math.pow(1 + ePct / 100, 1 / 12) - 1); }
  function monthly(nPct) { return nPct / 12; }
  function monthHe(ym) { var p = String(ym).split('-'); return p.length >= 2 ? (HEM[+p[1] - 1] || p[1]) + ' ' + p[0] : String(ym); }
  /* the all-banks effective rates of the latest month (by_bank, bank "system") */
  function system(D) {
    var bb = D && D.by_bank; if (!bb || !bb.months || !bb.rate || !bb.rate.system) return null;
    var i = bb.months.length - 1, out = [];
    TR.forEach(function (t) { var e = +((bb.rate.system[t.k] || [])[i]); if (e > 0) out.push({ k: t.k, he: t.he, e: e, n: toNom(e) }); });
    return out.length ? { month: bb.months[i], tracks: out, src: bb.src || {} } : null;
  }
  function parse(x) { var s = String(x == null ? '' : x).trim(); if (s.indexOf('.') < 0) s = s.replace(',', '.'); s = s.replace(/[^\d.]/g, ''); if (s === '' || s === '.') return NaN; var n = +s; return isFinite(n) ? n : NaN; }
  function convert(from, val) {  // from 'n' or 'e'; val in percent
    var x = parse(val);
    if (!(x >= 0 && x <= 30)) return { error: 'הקלידו ריבית שנתית באחוזים, מ־0 עד 30.' };
    return from === 'n' ? { n: x, e: toEff(x), m: monthly(x) } : { e: x, n: toNom(x), m: monthly(toNom(x)) };
  }
  function f2(x) { return (Math.round(x * 100) / 100).toFixed(2); }
  function f3(x) { return (Math.round(x * 1000) / 1000).toFixed(3); }
  function sentence(r) { return f2(r.n) + '% נומינלית בשנה = ' + f3(r.m) + '% בחודש = ' + f2(r.e) + '% אפקטיבית בשנה'; }
  function exampleText(S) {
    if (!S) return '';
    var t = S.tracks[0];
    return 'דוגמה: ב' + monthHe(S.month) + ' הריבית האפקטיבית הממוצעת של כל הבנקים ב' + t.he + ' הייתה ' + f2(t.e) + '%, שהן ' + f2(t.n) + '% נומינלית בשנה.';
  }

  G.NLNE = { toEff: toEff, toNom: toNom, monthly: monthly, convert: convert, system: system, parse: parse, sentence: sentence, exampleText: exampleText, monthHe: monthHe, f2: f2, f3: f3, TR: TR };
  if (!G.NadLanInstruments) return;

  /* ------------------------------------------------------------------------------------------------------------ the page */
  var NI = G.NadLanInstruments, esc = NI.esc;
  var CSS = '#nlne{font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#12202A;background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:16px;display:flex;flex-direction:column;gap:12px;margin:8px 0 16px;max-width:760px}'
    + '#nlne *{box-sizing:border-box}#nlne [hidden]{display:none!important}'
    + '#nlne p.nlne__k{margin:0!important;font:500 12px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;letter-spacing:.04em;color:#5E6A75!important}'
    + '#nlne h2.nlne__h{margin:0!important;padding:0!important;border:0!important;font:600 20px/28px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}#nlne h2.nlne__h::before,#nlne h2.nlne__h::after{display:none!important}'
    + '#nlne .nlne__x2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;align-items:start}'
    + '#nlne .nlne__lab{display:block;min-height:36px;font:500 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important;margin:0 0 6px!important}'
    + '#nlne .nlne__in{display:flex;align-items:stretch;gap:6px;height:52px;padding:0 12px;border:1px solid #2F6F86;border-radius:2px;background:#fff}'
    + '#nlne .nlne__in.is-calc{background:#F6F8F9;border-color:#D3DCE2}'
    + '#nlne .nlne__in input{flex:1 1 auto;min-width:0;width:100%!important;height:auto!important;min-height:44px!important;margin:0!important;border:0!important;outline:0;background:transparent!important;box-shadow:none!important;padding:0!important;font:500 22px/1.2 "IBM Plex Mono",ui-monospace,monospace!important;color:#12202A!important;text-align:right;direction:ltr}'
    + '#nlne .nlne__in span{align-self:center;font:400 17px/1 "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}'
    + '#nlne .nlne__in:focus-within{outline:2px solid #2F6F86;outline-offset:1px}'
    + '#nlne .nlne__err{display:block;font:500 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#C42550!important;margin:4px 0 0}#nlne .nlne__err:empty{display:none}'
    + '#nlne p.nlne__res{margin:0!important;padding:10px 12px!important;background:#F6F8F9;border-inline-start:3px solid #2F6F86;font:500 15px/24px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#12202A!important}'
    + '#nlne p.nlne__fx{margin:0!important;font:400 12px/20px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important}#nlne p.nlne__fx bdi{display:block;font-family:"IBM Plex Mono",ui-monospace,monospace!important;white-space:nowrap;text-align:right}'
    + '#nlne .nlne__num{font-family:"IBM Plex Mono",ui-monospace,monospace!important;font-weight:500}#nlne .nlne__lab2{display:block;font:500 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important;margin:0 0 6px!important}'
    + '#nlne .nlne__chips{display:flex;flex-wrap:wrap;gap:6px}'
    + '#nlne .nlne__chips button{min-height:44px!important;margin:0!important;padding:4px 12px!important;border-radius:999px!important;border:1px solid #D3DCE2!important;background:#fff!important;color:#3E4C58!important;font:400 13px/1.25 "IBM Plex Sans Hebrew",system-ui,sans-serif!important;box-shadow:none!important;cursor:pointer;width:auto!important;text-transform:none!important}'
    + '#nlne .nlne__chips button b{font:500 13px/1 "IBM Plex Mono",ui-monospace,monospace!important;color:inherit!important;margin-inline-start:6px}'
    + '#nlne .nlne__chips button[aria-pressed="true"]{background:#2F6F86!important;border-color:#2F6F86!important;color:#fff!important}'
    + '#nlne button:focus-visible{outline:2px solid #1F4B5C!important;outline-offset:2px}'
    + '#nlne p.nlne__t{margin:0!important;font:400 13px/21px "IBM Plex Sans Hebrew",system-ui,sans-serif!important;color:#3E4C58!important}#nlne p.nlne__t a{color:#2F6F86!important}';
  function ensureCss() { if (document.getElementById('nlne-css')) return; var s = document.createElement('style'); s.id = 'nlne-css'; s.textContent = CSS; document.head.appendChild(s); }

  NI.register('mnomeff', {
    custom: function (root, data) {
      if (NI.langOf && NI.langOf(root) === 'en') return;  // Hebrew only
      ensureCss();
      var S = system(data.boim || data.d0);
      var st = { from: 'n', val: '4.5', pick: null };
      var h = '<div class="nlne" id="nlne" dir="rtl" lang="he">'
        + '<p class="nlne__k">מחשבון · המרת ריבית</p>'
        + '<h2 class="nlne__h">ריבית נומינלית וריבית אפקטיבית</h2>'
        + '<div class="nlne__x2">'
        + '<div><label class="nlne__lab" for="nlne-n">ריבית נומינלית שנתית, בתשלום חודשי</label><div class="nlne__in" data-box="n"><input id="nlne-n" inputmode="decimal" autocomplete="off"><span>%</span></div><span class="nlne__err" data-err="n" aria-live="polite"></span></div>'
        + '<div><label class="nlne__lab" for="nlne-e">ריבית אפקטיבית שנתית</label><div class="nlne__in" data-box="e"><input id="nlne-e" inputmode="decimal" autocomplete="off"><span>%</span></div><span class="nlne__err" data-err="e" aria-live="polite"></span></div>'
        + '</div>'
        + '<p class="nlne__res" aria-live="polite"></p>'
        + '<p class="nlne__fx">הנוסחה, כש־n היא הריבית הנומינלית ו־e האפקטיבית: <bdi dir="ltr">e = (1 + n/12)^12 - 1</bdi><bdi dir="ltr">n = 12 × ((1 + e)^(1/12) - 1)</bdi></p>'
        + (S ? '<div><span class="nlne__lab2" id="nlne-cl">הממוצע של כל הבנקים, ' + esc(monthHe(S.month)) + ', ריבית אפקטיבית:</span><div class="nlne__chips" role="group" aria-labelledby="nlne-cl">'
          + S.tracks.map(function (t) { return '<button type="button" data-t="' + esc(t.k) + '">' + esc(t.he) + '<b>' + f2(t.e) + '%</b></button>'; }).join('') + '</div></div>'
          + '<p class="nlne__t">' + esc(exampleText(S)) + '</p>' : '')
        + '<p class="nlne__t">בנק ישראל מפרסם ריביות אפקטיביות, והמחשבונים בעמוד הזה ממירים אותן לריבית חודשית בנוסחה הזאת. '
        + (S && S.src.page ? 'מקור הממוצעים: <a href="' + esc(S.src.page) + '" target="_blank" rel="noopener">בנק ישראל, השוואת ריביות בהלוואות לדיור</a>, נתוני ' + esc(monthHe(S.month)) + '.' : '') + '</p>'
        + '</div>';
      root.innerHTML = h;
      var q = function (s) { return root.querySelector(s); }, qa = function (s) { return [].slice.call(root.querySelectorAll(s)); };
      var IN = q('#nlne-n'), IE = q('#nlne-e');
      function paint(skipTyped) {
        qa('[data-err]').forEach(function (x) { x.textContent = ''; });
        qa('[data-t]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-t') === st.pick)); });
        q('[data-box="n"]').classList.toggle('is-calc', st.from === 'e'); q('[data-box="e"]').classList.toggle('is-calc', st.from === 'n');
        var r = convert(st.from, st.val);
        if (r.error) { q('[data-err="' + st.from + '"]').textContent = r.error; q('.nlne__res').textContent = r.error; return; }
        if (st.from === 'n') { if (!skipTyped) IN.value = st.val; IE.value = f2(r.e); } else { if (!skipTyped) IE.value = st.val; IN.value = f2(r.n); }
        var B = function (x) { return '<bdi class="nlne__num">' + x + '%</bdi>'; };
        q('.nlne__res').innerHTML = B(f2(r.n)) + ' נומינלית בשנה = ' + B(f3(r.m)) + ' בחודש = ' + B(f2(r.e)) + ' אפקטיבית בשנה';  // the words of sentence(r), numbers in the mono face
      }
      IN.addEventListener('input', function () { st.from = 'n'; st.val = IN.value; st.pick = null; paint(true); });
      IE.addEventListener('input', function () { st.from = 'e'; st.val = IE.value; st.pick = null; paint(true); });
      root.addEventListener('click', function (e) {
        var b = e.target && e.target.closest ? e.target.closest('button[data-t]') : null; if (!b || !S) return;
        var t = S.tracks.filter(function (x) { return x.k === b.getAttribute('data-t'); })[0]; if (!t) return;
        st.from = 'e'; st.val = String(t.e); st.pick = t.k; paint(false);
      });
      paint(false);
    }
  });
})();
