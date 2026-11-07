/* NadLan Instruments · pcity v1 (HAD-681, Ben 7.11.2026): "מחירי דירות לפי עיר וחדרים" on /apartment-prices/.
   The 24 cities of the official series and the national line, by rooms (3, 4, 5 or all deals): the median closed-deal price of the
   latest published quarter (Tax Authority deals via nadlan.gov.il), the change against the same quarter a year earlier, the
   change since 1-3.2021 and the same change after inflation. Sorted by any column, filtered by district or name; every city
   links to its own price page. Compare 2 to 4 cities side by side: the medians by rooms, the changes, the median rent of the
   same quarter and the gross yield (only where the rent is published), and the monthly payment on the median 4-room home at the
   75% cap of directive 329 and the Bank of Israel average rate of the latest month (shown with its month).
   Data: prices-hub.json. Math in prices-common.js (window.NLPH). */
(function () {
  'use strict';
  if (!window.NadLanInstruments || !window.NLPH || !window.NLPH.ui) return;
  var NI = window.NadLanInstruments, P = window.NLPH, U = P.ui, esc = U.esc;
  var NAT = 'ישראל';
  var ROOMS = [['3', '3'], ['4', '4'], ['5', '5'], ['a', 'כל הדירות']];
  var PRE = [{ k: 'big', l: 'הערים הגדולות', c: ['תל אביב יפו', 'ירושלים', 'חיפה', 'באר שבע'] }, { k: 'dan', l: 'גוש דן', c: ['תל אביב יפו', 'רמת גן', 'גבעתיים', 'חולון'] },
    { k: 'sharon', l: 'השרון', c: ['הרצליה', 'רעננה', 'כפר סבא', 'נתניה'] }, { k: 'south', l: 'השפלה והדרום', c: ['ראשון לציון', 'רחובות', 'אשדוד', 'באר שבע'] }];
  var SHORT = { 'תל אביב יפו': 'תל אביב', 'מודיעין מכבים רעות': 'מודיעין' };
  function short(n) { return SHORT[n] || n; }
  function css() {
    if (document.getElementById('nlpc-css')) return;
    var s = document.createElement('style'); s.id = 'nlpc-css';
    s.textContent = [
      '.nlpc-bar{display:grid;gap:12px;margin:0 0 12px;position:relative}',
      '@media (min-width:700px){.nlpc-bar{grid-template-columns:auto minmax(0,260px);justify-content:space-between;align-items:end}.nlpc-bar>.nlph-tabs{grid-column:1/-1;order:3}}',
      'html body .nli .nlpc-find input{font:500 16px/22px var(--nli-sans) !important;direction:rtl !important;text-align:right !important}',
      '.nlpc-city{display:flex;align-items:center;gap:8px;min-width:0}',
      'html body .nli .nlpc-city input[type=checkbox]{width:20px;height:20px;margin:0;flex:0 0 20px;accent-color:var(--nli-sea);cursor:pointer}',
      'html body .nli .nlpc-city a{color:var(--nli-ink) !important;text-decoration:underline;text-decoration-color:#9DB4BF;text-underline-offset:3px;font-weight:500}',
      'html body .nli .nlpc-city a:hover{color:var(--nli-sea) !important}',
      '.nlpc-q{display:block;font:400 11.5px/15px var(--nli-mono);color:var(--nli-mute)}',
      'html body .nli .nlph table.nlph-t tr.is-sel td,html body .nli .nlph table.nlph-t tr.is-sel th{background:#EEF5F7 !important}',
      'html body .nli .nlph table.nlph-t tr.is-nat th{background:var(--ph-tint) !important}',
      'html body .nli .nlph table.nlpc-cmp tr.nlpc-lab{display:none !important}',
      'html body .nli .nlph table.nlpc-cmp tr.nlpc-lab th{font:500 12.5px/17px var(--nli-sans) !important;color:var(--nli-mute) !important;background:var(--ph-paper) !important;padding:6px 8px !important;border-bottom:0 !important}',
      '@media (max-width:600px){html body .nli .nlph table.nlpc-cmp tr.nlpc-lab{display:table-row !important}html body .nli .nlph table.nlpc-cmp tr.grp:not(.nlpc-lab) td{border-top:0 !important}html body .nli .nlph table.nlpc-cmp tr.nlpc-lab.grp th{border-top:2px solid var(--nli-ink) !important}html body .nli .nlph table.nlpc-cmp td{text-align:center !important}}',
      '@media (max-width:600px){html body .nli .nlpc-bar .nlph-tabs,html body .nli .nlph > .nlph-tabs{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}html body .nli .nlph .nlph-tabs button{flex:0 0 auto;white-space:nowrap}html body .nli .nlph .nlph-tabs .lab{flex:0 0 auto}}',
      'html body .nli button.nlpc-sort{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:4px;font:inherit;color:inherit;min-height:32px}',
      'html body .nli button.nlpc-sort:focus-visible{outline:2px solid var(--nli-focus);outline-offset:2px}',
      '.nlpc-sort i{font-style:normal;font-size:10px;color:var(--nli-sea);width:8px}',
      'html body .nli .nlph th[aria-sort] button.nlpc-sort{color:var(--nli-ink)}',
      '.nlpc-sel{font:400 14px/22px var(--nli-sans);color:var(--nli-ink2);margin:0 0 10px;min-height:22px}',
      '.nlpc-sel b{color:var(--nli-ink);font-weight:600}',
      '.nlpc-warn{color:var(--nli-survey);font:500 13px/18px var(--nli-sans);min-height:18px;margin:4px 0 0}',
      'html body .nli .nlph table.nlpc-cmp th,html body .nli .nlph table.nlpc-cmp td{vertical-align:top}',
      'html body .nli .nlph table.nlpc-cmp thead th{font:600 14px/19px var(--nli-sans) !important;color:var(--nli-ink) !important}',
      'html body .nli .nlph table.nlpc-cmp thead th a{color:var(--nli-ink) !important}',
      'html body .nli .nlph table.nlpc-cmp tbody th{font:400 13px/18px var(--nli-sans) !important;color:var(--nli-ink2) !important;min-width:96px}',
      'html body .nli .nlph table.nlpc-cmp tr.grp th,html body .nli .nlph table.nlpc-cmp tr.grp td{border-top:2px solid var(--nli-ink) !important}',
      '@media (max-width:600px){html body .nli .nlph table.nlpc-cmp th,html body .nli .nlph table.nlpc-cmp td{padding:7px 4px !important;font-size:12.5px !important}html body .nli .nlph table.nlpc-cmp tbody th{min-width:0;width:30%}}',
      '.nlpc-scroll{max-height:none}',
      '.nlpc-vbar{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;justify-content:space-between;margin:0 0 10px}',
      'html body .nli button.nlpc-csv{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:8px 14px;border:1px solid var(--nli-sea);border-radius:2px;background:var(--nli-surface);color:var(--nli-sea);font:500 14px/20px var(--nli-sans);cursor:pointer;margin:0}',
      '.nlpc-csv svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:1.6}',
      '.nlpc-mps{display:grid;grid-template-columns:minmax(0,1fr);gap:14px}@media (min-width:760px){.nlpc-mps{grid-template-columns:repeat(2,minmax(0,1fr))}}',
      '.nlpc-mp{margin:0;border:1px solid var(--nli-line);border-radius:var(--nli-r-s);background:#EAF1F4;padding:8px 6px 4px;min-width:0}',
      '.nlpc-mp figcaption{font:600 13px/18px var(--nli-sans);color:var(--nli-ink);padding:0 6px 4px}',
      '.nlpc-mp svg{display:block;width:100%;height:auto}',
      '.nlpc-mp .land{fill:#FFFFFF;stroke:#FFFFFF;stroke-width:.8}.nlpc-mp .box{fill:none;stroke:var(--nli-sea);stroke-width:1.4;stroke-dasharray:4 3}',
      '.nlpc-mp g.pt{cursor:pointer;outline:none}.nlpc-mp g.pt line{stroke:#7F929E;stroke-width:1}.nlpc-mp g.pt circle{fill:var(--nli-ink)}',
      '.nlpc-mp g.pt rect{fill:#FFFFFF;stroke:#B9C7D0;stroke-width:1}.nlpc-mp g.pt text{text-anchor:start;direction:rtl}',
      '.nlpc-mp g.pt text.n{font:600 12.5px var(--nli-sans);fill:var(--nli-ink)}.nlpc-mp g.pt text.v{font:500 11.5px var(--nli-mono);fill:var(--nli-ink2)}',
      '.nlpc-mp g.pt.on rect{fill:var(--nli-sea);stroke:var(--nli-sea)}.nlpc-mp g.pt.on text{fill:#FFFFFF}.nlpc-mp g.pt.on circle{fill:var(--nli-sea)}',
      '.nlpc-mp g.pt:hover rect,.nlpc-mp g.pt:focus rect{stroke:var(--nli-ink);stroke-width:1.6}'
    ].join('');
    document.head.appendChild(s);
  }

  NI.register('pcity', {
    custom: function (root, D0) {
      var D = D0.phub || D0.d0; U.css(); css();
      if (!root.closest('.nli')) root.classList.add('nli');
      root.setAttribute('dir', 'rtl');
      var set = {}; try { set = JSON.parse(root.getAttribute('data-nli-set') || '{}'); } catch (e) {}
      root.innerHTML = '';
      var byN = {}; D.city.forEach(function (c) { byN[c.n] = c; }); byN[NAT] = { n: NAT, slug: null, dist: '', r3: D.il.r3, r4: D.il.r4, r5: D.il.r5, ra: D.il.ra, rent: D.il.rent, nat: true };
      var dists = []; D.city.forEach(function (c) { if (dists.indexOf(c.dist) < 0) dists.push(c.dist); });
      var st = { uid: Math.random().toString(36).slice(2, 7), rooms: /^[345]$/.test(String(set.rooms)) ? String(set.rooms) : '4', sk: 'v', sd: -1, dist: '', q: '', sel: PRE[0].c.slice() };
      if (set.city && byN[set.city]) { st.sel = [set.city]; PRE[0].c.forEach(function (n) { if (st.sel.length < 3 && st.sel.indexOf(n) < 0) st.sel.push(n); }); }
      var M = D.mort, rk = function () { return st.rooms === 'a' ? 'ra' : 'r' + st.rooms; };

      var panel = U.el('div', 'nli__panel nlph'); root.appendChild(panel);
      panel.appendChild(U.el('p', 'nli__kicker', 'טבלה · עסקאות שנסגרו'));
      panel.appendChild(U.el('h2', 'nli__title', 'מחירי דירות לפי עיר וחדרים'));
      panel.appendChild(U.el('p', 'nli__lede', esc('המחיר החציוני של הדירות שנמכרו בכל עיר, לפי העסקאות שדווחו לרשות המסים, ברבעון האחרון שפורסם: מה השתנה בשנה, מה השתנה מתחילת 2021, וכמה מזה נשאר אחרי האינפלציה. סמנו 2 עד 4 ערים, ותקבלו השוואה מלאה עם שכר דירה, תשואה והחזר משכנתא.')));
      var bar = U.el('div', 'nlpc-bar'); panel.appendChild(bar);
      bar.appendChild(U.seg('מספר חדרים', ROOMS.map(function (r) { return { value: r[0], label: r[1] }; }), st.rooms, function (v) { st.rooms = v; draw(); }));
      var dg = U.el('div', 'nlph-tabs'); dg.setAttribute('role', 'group'); dg.setAttribute('aria-label', 'מחוז');
      [['', 'כל הארץ']].concat(dists.map(function (d) { return [d, d === 'ירושלים' || d === 'חיפה' ? 'מחוז ' + d : d]; })).forEach(function (o) {
        var b = U.el('button', '', esc(o[1])); b.type = 'button'; b.setAttribute('aria-pressed', String(o[0] === st.dist));
        b.addEventListener('click', function () { st.dist = o[0]; [].forEach.call(dg.children, function (z) { z.setAttribute('aria-pressed', String(z === b)); }); table(); }); dg.appendChild(b);
      });
      bar.appendChild(dg);
      var fw = U.el('div', 'nli__f nlpc-find'); var fl = U.el('label', '', 'חיפוש עיר'); var fid = 'nlpc-q-' + Math.random().toString(36).slice(2, 7); fl.htmlFor = fid; fw.appendChild(fl);
      var fin = U.el('div', 'nli__in'); var qi = document.createElement('input'); qi.type = 'search'; qi.id = fid; qi.placeholder = 'למשל: חולון'; qi.autocomplete = 'off';
      qi.addEventListener('input', function () { st.q = qi.value.trim(); table(); }); fin.appendChild(qi); fw.appendChild(fin); bar.appendChild(fw);

      var pre = U.el('div', 'nlph-tabs is-sea'); pre.setAttribute('role', 'group'); pre.setAttribute('aria-label', 'השוואה מהירה');
      pre.appendChild(U.el('span', 'lab', 'השוואה מהירה:'));
      PRE.forEach(function (p) { var b = U.el('button', '', esc(p.l)); b.type = 'button'; b.setAttribute('data-k', p.k); b.addEventListener('click', function () { st.sel = p.c.slice(); marks(); compare(); }); pre.appendChild(b); });
      panel.appendChild(pre);
      var selLine = U.el('p', 'nlpc-sel'); selLine.setAttribute('aria-live', 'polite'); selLine.style.marginTop = '10px'; panel.appendChild(selLine);
      var warn = U.el('p', 'nlpc-warn'); warn.setAttribute('aria-live', 'assertive');
      var W = D.wage || null, view = 'table';
      var vbar = U.el('div', 'nlpc-vbar'); var vt = U.el('div', 'nlph-tabs'); vt.setAttribute('role', 'group'); vt.setAttribute('aria-label', 'תצוגה');
      [['table', 'טבלה'], ['map', 'מפה']].forEach(function (o) { var b = U.el('button', '', esc(o[1])); b.type = 'button'; b.setAttribute('data-v', o[0]); b.setAttribute('aria-pressed', String(o[0] === view));
        b.addEventListener('click', function () { view = o[0]; [].forEach.call(vt.children, function (z) { z.setAttribute('aria-pressed', String(z === b)); }); tw.hidden = view !== 'table'; mw.hidden = view !== 'map'; if (view === 'map') map(); }); vt.appendChild(b); });
      var csvb = U.el('button', 'nlpc-csv', '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 3v10M6 9l4 4 4-4M4 16h12"/></svg><span>הורדת הטבלה (CSV)</span>'); csvb.type = 'button';
      csvb.addEventListener('click', function () {
        var d = new Date(), t = d.getDate() + '.' + (d.getMonth() + 1) + '.' + d.getFullYear(), blob = new Blob([P.toCSV(P.csvRows(D, t))], { type: 'text/csv;charset=utf-8' });
        var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'mehirei-dirot-nad-lan-' + D.vsrc.version + '.csv'; document.body.appendChild(a); a.click();
        setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
      });
      vbar.appendChild(vt); vbar.appendChild(csvb); panel.appendChild(vbar);
      var tw = U.el('div', 'nlph-tw'); panel.appendChild(tw);
      var mw = U.el('div', 'nlpc-map'); mw.hidden = true; panel.appendChild(mw); panel.appendChild(warn);
      var cmp = U.el('section', 'nlph-sec'); cmp.id = 'nlpc-cmp-' + Math.random().toString(36).slice(2, 7); panel.appendChild(cmp);
      panel.appendChild(U.el('p', 'nlph-fine', esc('איך לקרוא: חציון הוא המחיר שחצי מהעסקאות ברבעון היו מתחתיו וחצי מעליו, לכל הדירות שנמכרו (חדשות ויד שנייה יחד). רבעון עם מעט עסקאות לא מתפרסם (·), ואז מוצג הרבעון האחרון שכן פורסם. השינוי בשנה משווה לאותו רבעון שנה קודם, כדי שעונות השנה לא יטעו. אחרי אינפלציה: לפי ממוצע מדד המחירים לצרכן ברבעון. החישובים שלנו.')));
      var src = U.el('p', 'nli__src'); src.innerHTML = U.srcs([{ label: D.vsrc.he + ', קובץ ' + D.vsrc.version, url: D.vsrc.url }, { label: D.rsrc.he, url: D.rsrc.url }, { label: M.src.he, url: M.src.url }, { label: M.ltvSrc.he, url: M.ltvSrc.url }, { label: D.cpi.src.he, url: D.cpi.src.url }]);
      panel.appendChild(src);
      panel.appendChild(U.share(function () { return shareText(); }));

      function stat(n, k) { var c = byN[n]; return c ? P.cityStat(c[k || rk()], D.q, D.cpi) : null; }
      function commonQ() { var f = {}, best = null; D.city.forEach(function (c) { var s = stat(c.n); if (s) { f[s.q] = (f[s.q] || 0) + 1; if (!best || f[s.q] > f[best]) best = s.q; } }); return best; }
      function href(c) { return c.slug ? '/' + c.slug + '-apartment-prices/' : ''; }
      function marks() {
        [].forEach.call(tw.querySelectorAll('input[type=checkbox]'), function (x) { var on = st.sel.indexOf(x.value) > -1; x.checked = on; x.closest('tr').classList.toggle('is-sel', on); });
        [].forEach.call(pre.querySelectorAll('button'), function (b) { var p = PRE.filter(function (z) { return z.k === b.getAttribute('data-k'); })[0]; b.setAttribute('aria-pressed', String(!!p && p.c.join() === st.sel.join())); });
        selLine.innerHTML = st.sel.length ? 'בהשוואה: <b>' + st.sel.map(function (n) { return esc(short(n)); }).join(', ') + '</b>' + (st.sel.length > 1 ? ' · <a class="nlph-a" href="#' + cmp.id + '">להשוואה</a>' : ' · סמנו עוד עיר') : 'סמנו 2 עד 4 ערים בטבלה, או בחרו השוואה מהירה.';
      }
      function table() {
        var k = rk(), cq = commonQ(), nat = stat(NAT);
        var list = D.city.filter(function (c) { return (!st.dist || c.dist === st.dist) && (!st.q || c.n.indexOf(st.q) > -1 || short(c.n).indexOf(st.q) > -1); })
          .map(function (c) { return { c: c, s: stat(c.n) }; });
        var val = function (r) { var s = r.s; if (st.sk === 'n') return r.c.n; if (!s) return null; return st.sk === 'v' || st.sk === 'sal' ? s.v : s[st.sk]; };
        list.sort(function (a, b) { var x = val(a), y = val(b); if (st.sk === 'n') return st.sd * x.localeCompare(y, 'he'); if (x == null && y == null) return 0; if (x == null) return 1; if (y == null) return -1; return st.sd * (x - y); });
        var row = function (c, s, cls) {
          var on = st.sel.indexOf(c.n) > -1, h = href(c), qn = s && s.q !== cq ? '<span class="nlpc-q">' + esc(P.qShort(s.q)) + '</span>' : '';
          return '<tr class="' + (cls || '') + (on ? ' is-sel' : '') + '"><th scope="row"><div class="nlpc-city"><input type="checkbox" value="' + esc(c.n) + '"' + (on ? ' checked' : '') + ' aria-label="' + esc('השוואה: ' + c.n) + '"><span>' +
            (h ? '<a href="' + esc(h) + '">' + esc(short(c.n)) + '</a>' : esc(c.nat ? 'כל הארץ' : short(c.n))) + qn + '</span></div></th>' +
            '<td class="n">' + (s ? U.k(s.v) : '<span class="nlph-na">·</span>') + (W && s ? '<span class="nlph-ph nlpc-q">' + U.num(P.salaries(s.v, W)) + ' משכורות</span>' : '') + '</td><td class="n">' + U.pct(s && s.yoy) + '</td>' +
            '<td class="n">' + U.pct(s && s.since) + '<span class="nlph-ph nlpc-q">' + (s && s.real != null ? 'ריאלי <bdi>' + U.pctTxt(s.real) + '</bdi>' : '') + '</span></td><td class="n nlph-dk">' + U.pct(s && s.real) + '</td>' + (W ? '<td class="n nlph-dk">' + (s ? U.num(P.salaries(s.v, W)) : '<span class="nlph-na">·</span>') + '</td>' : '') + '</tr>';
        };
        var th = function (key, label, cls) { var on = st.sk === key; return '<th scope="col" class="' + (cls || 'n') + '"' + (on ? ' aria-sort="' + (st.sd > 0 ? 'ascending' : 'descending') + '"' : '') + '><button type="button" class="nlpc-sort" data-k="' + key + '">' + label + '<i aria-hidden="true">' + (on ? (st.sd > 0 ? '▲' : '▼') : '') + '</i></button></th>'; };
        tw.innerHTML = '<table class="nlph-t"><caption>' + esc('חציון מחיר העסקה, ' + (st.rooms === 'a' ? 'כל הדירות' : st.rooms + ' חדרים') + ', באלפי ₪. ' + P.qLabel(cq) + ' (רשות המסים, אתר הנדל״ן הממשלתי, קובץ ' + D.vsrc.version + ').' + (W ? ' משכורות: המחיר חלקי השכר הממוצע, ' + U.num(W.v) + ' ₪ ברוטו (הביטוח הלאומי, מ' + P.monLabel(W.from.slice(0, 7)) + ').' : '') + ' ' + list.length + (list.length === 1 ? ' עיר.' : ' ערים.')) + '</caption><thead><tr>' +
          th('n', 'עיר', '') + th('v', 'חציון') + th('yoy', 'בשנה') + th('since', 'מתחילת 2021') + th('real', 'מתחילת 2021, אחרי אינפלציה', 'n nlph-dk') + (W ? th('sal', 'משכורות', 'n nlph-dk') : '') + '</tr></thead><tbody>' +
          row(byN[NAT], nat, 'is-nat') + list.map(function (r) { return row(r.c, r.s); }).join('') + '</tbody></table>';
        if (!list.length) tw.querySelector('tbody').insertAdjacentHTML('beforeend', '<tr><td colspan="6">' + esc('לא מצאנו עיר בשם הזה. הטבלה כוללת 24 ערים עם מספיק עסקאות.') + '</td></tr>');
        [].forEach.call(tw.querySelectorAll('button.nlpc-sort'), function (b) { b.addEventListener('click', function () { var k2 = b.getAttribute('data-k'); if (st.sk === k2) st.sd = -st.sd; else { st.sk = k2; st.sd = k2 === 'n' ? 1 : -1; } table(); var nb = tw.querySelector('button[data-k="' + k2 + '"]'); if (nb) nb.focus(); }); });
        [].forEach.call(tw.querySelectorAll('input[type=checkbox]'), function (x) { x.addEventListener('change', function () { toggle(x.value, x.checked); }); });
        marks();
      }
      function toggle(n, on) {
        warn.textContent = '';
        var i = st.sel.indexOf(n);
        if (on && i < 0) { if (st.sel.length >= 4) { warn.textContent = 'אפשר להשוות עד 4 ערים בבת אחת. הסירו סימון מעיר אחרת.'; marks(); return; } st.sel.push(n); }
        if (!on && i > -1) st.sel.splice(i, 1);
        marks(); compare();
      }
      function cdata(n) {
        var c = byN[n], k = rk(), s = stat(n), s4 = stat(n, 'r4'), rr = st.rooms === 'a' ? '4' : st.rooms, sr = stat(n, 'r' + rr);
        var rent = sr ? P.rentAt(c.rent, rr, sr.q) : null, pay = s4 ? P.payment(s4.v, M.ltv, M.eff, M.years) : null;
        return { c: c, s: s, s3: stat(n, 'r3'), s4: s4, s5: stat(n, 'r5'), rr: rr, sr: sr, rent: rent, y: sr && rent ? P.grossYield(rent, sr.v) : null, pay: pay };
      }
      function compare() {
        if (st.sel.length < 2) { cmp.innerHTML = ''; return; }
        var X = st.sel.map(cdata), rl = st.rooms === 'a' ? 'כל הדירות' : st.rooms + ' חדרים', mm = P.monLabel(M.month);
        var cell = function (s) { return s ? U.k(s.v) + '<span class="nlpc-q">' + esc(P.qShort(s.q)) + '</span>' : '<span class="nlph-na">·</span>'; };
        var tr = function (label, f, cls) { return '<tr class="nlpc-lab' + (cls ? ' ' + cls : '') + '"><th colspan="' + X.length + '" scope="colgroup">' + label + '</th></tr><tr' + (cls ? ' class="' + cls + '"' : '') + '><th scope="row" class="nlph-dk">' + label + '</th>' + X.map(function (x) { return '<td class="n">' + f(x) + '</td>'; }).join('') + '</tr>'; };
        cmp.innerHTML = '<h3 class="nlph-h">' + esc('השוואה: ' + st.sel.map(short).join(', ')) + '</h3>' +
          '<p class="nlph-sub">' + esc('המחירים באלפי ₪. שכר הדירה והתשואה מאותו רבעון של המחיר בלבד. ההחזר: דירת 4 חדרים במחיר החציוני, משכנתא של ' + Math.round(100 * M.ltv) + '% (המימון המרבי לדירה יחידה), ' + M.years + ' שנה, בריבית ' + M.eff.toFixed(2) + '%, הממוצע של בנק ישראל למסלול ' + M.label + ' ב' + mm + '.') + '</p>' +
          '<div class="nlph-tw"><table class="nlph-t nlpc-cmp"><thead><tr><th scope="col" class="nlph-dk">' + esc(rl) + '</th>' + X.map(function (x) { var h = href(x.c); return '<th scope="col" class="n">' + (h ? '<a href="' + esc(h) + '">' + esc(short(x.c.n)) + '</a>' : esc(x.c.nat ? 'כל הארץ' : short(x.c.n))) + '</th>'; }).join('') + '</tr></thead><tbody>' +
          tr('חציון 3 חדרים (אלפי ₪)', function (x) { return cell(x.s3); }) + tr('חציון 4 חדרים (אלפי ₪)', function (x) { return cell(x.s4); }) + tr('חציון 5 חדרים (אלפי ₪)', function (x) { return cell(x.s5); }) +
          tr(esc('בשנה, ' + rl), function (x) { return U.pct(x.s && x.s.yoy); }, 'grp') + tr(esc('מתחילת 2021, ' + rl), function (x) { return U.pct(x.s && x.s.since); }) + tr('מתחילת 2021, אחרי אינפלציה', function (x) { return U.pct(x.s && x.s.real); }) +
          tr(esc('שכר דירה חציוני, ' + x_rooms(st) + ' (₪)'), function (x) { return x.rent ? U.num(x.rent) : '<span class="nlph-na" title="לא פורסם לאותו רבעון">·</span>'; }, 'grp') +
          tr('תשואה ברוטו בשנה', function (x) { return x.y != null ? '<bdi class="nlph-n">' + (100 * x.y).toFixed(2) + '%</bdi>' : '<span class="nlph-na">·</span>'; }) +
          tr(esc('מקדמה של ' + Math.round(100 * (1 - M.ltv)) + '%, 4 חדרים (אלפי ₪)'), function (x) { return x.s4 ? U.k(x.s4.v * (1 - M.ltv)) : '<span class="nlph-na">·</span>'; }, 'grp') +
          tr('החזר חודשי, 4 חדרים (₪)', function (x) { return x.pay ? '<b>' + U.num(x.pay.pay) + '</b>' : '<span class="nlph-na">·</span>'; }) +
          (W ? tr(esc('משכורות ממוצעות לדירת 4 חדרים (' + U.num(W.v) + ' ₪ לחודש)'), function (x) { return x.s4 ? U.num(P.salaries(x.s4.v, W)) : '<span class="nlph-na">·</span>'; }) : '') +
          '</tbody></table></div>';
        function x_rooms(s) { return s.rooms === 'a' ? '4 חדרים' : s.rooms + ' חדרים'; }
      }
      function shareText() {
        var cq = commonQ(), t = 'מחירי דירות לפי עיר, ' + (st.rooms === 'a' ? 'כל הדירות' : st.rooms + ' חדרים') + ', חציון העסקאות (רשות המסים), ' + P.qLabel(cq) + ':';
        (st.sel.length ? st.sel : [NAT]).forEach(function (n) { var s = stat(n); if (s) t += '\n' + short(n === NAT ? 'כל הארץ' : n) + ': ' + U.num(s.v) + ' ₪' + (s.yoy != null ? ', בשנה ' + U.pctTxt(s.yoy) : ''); });
        return t;
      }
      var CENTER = { s: 31.85, n: 32.34, w: 34.68, e: 34.98 }, ALL = { s: 29.45, n: 33.35, w: 34.2, e: 35.95 };
      function inBox(ll, b) { return ll[0] >= b.s && ll[0] <= b.n && ll[1] >= b.w && ll[1] <= b.e; }
      function panel_(title, id, box, list, split, extra) {
        var Wv = 360, Hv = 560, pr = P.proj(box, Wv, Hv, { x: 92, y: 14 }), k = rk();
        var land = D.map.land.map(function (poly) { return 'M' + poly.map(function (p) { var q = pr(p[1], p[0]); return q[0].toFixed(1) + ' ' + q[1].toFixed(1); }).join('L') + 'Z'; }).join('');
        var pts = list.map(function (c) { var q = pr(c.ll[0], c.ll[1]); return { id: c.n, x: q[0], y: q[1], lon: c.ll[1] }; });
        var L = P.callouts(pts, Hv, 32, split), cid = 'nlpc-clip-' + id + '-' + st.uid;
        var o = '<figure class="nlpc-mp"><figcaption>' + esc(title) + '</figcaption><svg viewBox="0 0 ' + Wv + ' ' + Hv + '" role="group" aria-label="' + esc(title) + '">' +
          '<defs><clipPath id="' + cid + '"><rect x="0" y="0" width="' + Wv + '" height="' + Hv + '"/></clipPath></defs><g clip-path="url(#' + cid + ')"><path class="land" d="' + land + '"/></g>' + (extra ? extra(pr) : '');
        L.forEach(function (l) {
          var s = stat(l.id, k), on = st.sel.indexOf(l.id) > -1, w = 84, bx = l.side === 'L' ? 4 : Wv - 4 - w, ex = l.side === 'L' ? bx + w : bx;
          o += '<g class="pt' + (on ? ' on' : '') + '" data-c="' + esc(l.id) + '" tabindex="0" role="button" aria-pressed="' + on + '" aria-label="' + esc(short(l.id) + (s ? ', ' + U.num(s.v) + ' ₪' : '') + ', השוואה') + '">' +
            '<line x1="' + l.x.toFixed(1) + '" y1="' + l.y.toFixed(1) + '" x2="' + ex.toFixed(1) + '" y2="' + l.ly.toFixed(1) + '"/><circle cx="' + l.x.toFixed(1) + '" cy="' + l.y.toFixed(1) + '" r="3.2"/>' +
            '<rect x="' + bx.toFixed(1) + '" y="' + (l.ly - 15).toFixed(1) + '" width="' + w + '" height="30" rx="2"/>' +
            '<text class="n" x="' + (bx + w - 6).toFixed(1) + '" y="' + (l.ly - 2).toFixed(1) + '">' + esc(short(l.id)) + '</text>' +
            '<text class="v" x="' + (bx + w - 6).toFixed(1) + '" y="' + (l.ly + 11).toFixed(1) + '">' + (s ? U.k(s.v) : '·') + '</text></g>';
        });
        return o + '</svg></figure>';
      }
      function map() {
        if (!D.map || !D.map.land) { mw.innerHTML = ''; return; }
        var cs = D.city.filter(function (c) { return c.ll; }), inC = cs.filter(function (c) { return inBox(c.ll, CENTER); }), out = cs.filter(function (c) { return !inBox(c.ll, CENTER); });
        var rl = st.rooms === 'a' ? 'כל הדירות' : st.rooms + ' חדרים';
        mw.innerHTML = '<p class="nlph-sub">' + esc('חציון ' + rl + ' באלפי ₪, ' + P.qLabel(commonQ()) + '. לחיצה על עיר מוסיפה אותה להשוואה או מוציאה ממנה.') + '</p><div class="nlpc-mps">' +
          panel_('גוש דן, השרון והשפלה', 'c', CENTER, inC, 34.81) +
          panel_('כל הארץ', 'a', ALL, out, 34.9, function (pr) { var a = pr(CENTER.n, CENTER.w), b = pr(CENTER.s, CENTER.e); return '<rect class="box" x="' + a[0].toFixed(1) + '" y="' + a[1].toFixed(1) + '" width="' + (b[0] - a[0]).toFixed(1) + '" height="' + (b[1] - a[1]).toFixed(1) + '"/>'; }) +
          '</div><p class="nlph-fine">' + esc(D.map.src.he + '.') + '</p>';
        [].forEach.call(mw.querySelectorAll('g.pt'), function (g) {
          var go = function () { var n = g.getAttribute('data-c'); toggle(n, st.sel.indexOf(n) < 0); map(); var f = mw.querySelector('g.pt[data-c="' + n + '"]'); if (f && f.focus) f.focus({ preventScroll: true }); };
          g.addEventListener('click', go); g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
        });
      }
      function draw() { table(); compare(); if (view === 'map') map(); }
      draw();
    }
  });
})();
