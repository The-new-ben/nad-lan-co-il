/* NadLan Instruments · the registered-contractor family (HAD-592, /pinkas-hakablanim/, Ben 22.10.2026: "ultra complex tools
   with UX that gives you everything with one tap"). One file (registry 'file' => 'pinkas'):
     pinkas  search all 17,874 contractors of the official register (server route /wp-json/nadlan/v1/pinkas: name, contractor
             number, company number, city, branch, level, recognised) and show each as a small licence: branches, group and
             level, what the level allows today on one site, restrictions, the official record and our profile. "My job": a
             job type and a budget say whether the law requires a registered contractor and which level, and filter the list.
     sivug   the classification table in force as a ladder: tap a budget and see the lowest level that covers it in every group.
   Design: DS component ContractorCheck (https://claude.ai/artifact/L9Nqz7Viv7K3MYeZrBc9s8): the ministry licence, blue ink on
   white, a red stamp only for a restriction, register numbers in mono. Data: pinkas-meta.json (tools/instruments/build_pinkas.py).
   Amounts come from the official table in force (1.10.2026 to 1.4.2027), never from the dataset's older HEKEF column.
   No phone, email or street is shown; the official record has them. */
(function () {
  'use strict';
  var LV = ['ק', '1', '2', '3', '4', '5'];
  function rank(l) { return l === 'ק' ? 0 : +l; }
  function code(g, l) { return l === 'ק' ? 'ק' : g + l; }  // the official notation: ג1, ב5, and plain ק (renovations only)
  /** The lowest level of group g whose limit covers a job of nis (before VAT); null if none. ק exists only in branch 131. */
  function levelFor(t, g, nis, code) {
    var row = t[g]; if (!row) return null;
    for (var i = 0; i < LV.length; i++) { var l = LV[i]; if (!(l in row)) continue; if (l === 'ק' && code !== 131) continue; if (row[l] === 0 || row[l] * 1000 >= nis) return l; }
    return null;
  }
  function needsRegistered(thr, kind, nis) { return nis > (kind === 'main' ? thr.main : thr.sub); }
  window.NLPK = { levelFor: levelFor, needsRegistered: needsRegistered, rank: rank };
  if (!window.NadLanInstruments) return;
  var NI = window.NadLanInstruments, F = NI.fmt, esc = NI.esc;
  var REC = 'https://www.gov.il/apps/moch/rasham/details/';
  var JOBS = [['reno', 'שיפוץ דירה', 131, 'sub'], ['ext', 'הרחבה או תוספת', 135, 'sub'], ['house', 'בית פרטי', 100, 'main'], ['bldg', 'בניין מגורים', 100, 'main'], ['yard', 'פיתוח חצר', 111, 'sub'], ['road', 'כבישים ותשתית', 200, 'main']];
  var BUDGETS = [50000, 150000, 500000, 2000000, 10000000, 50000000];
  var CHIPS = [[100, 'בנייה'], [131, 'שיפוצים'], [200, 'כבישים ותשתית'], [260, 'מים וביוב'], [160, 'חשמל'], [170, 'מיזוג אוויר']];
  function money(n) { return n >= 1000000 ? F.num(n / 1000000, n % 1000000 ? 1 : 0) + ' מיליון' : F.num(n / 1000) + ' אלף'; }
  function lim(t, g, l) { var v = t[g] && t[g][l]; return v === 0 ? 'ללא הגבלה' : v ? 'עד ' + F.num(v) + ' אלף ₪' : ''; }
  function red(s) { return /מותלה|אינה רשאית|הקפאת|מוקפא|מוחרג/.test(s); }
  function css() {
    if (document.getElementById('nlpk-css')) return;
    var s = document.createElement('style'); s.id = 'nlpk-css';
    s.textContent = '.nlpk{--pk:#1D3E8A;--pkw:#E8EEF8;--pkr:#C42550}' +
      '.nlpk__q{display:flex;align-items:center;gap:8px;border:2px solid var(--pk);border-radius:6px;background:#fff;padding:0 12px;margin:12px 0 0}' +
      '.nlpk__q:focus-within{box-shadow:0 0 0 3px var(--pkw)}html body .nlpk .nlpk__q input,html body .nlpk .nlpk__q input:focus{border:0 !important;outline:0 !important;box-shadow:none !important;background:transparent !important}' +
      '.nlpk__q svg{flex:none}.nlpk__q input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:400 17px/24px var(--nli-sans);color:var(--nli-ink);padding:12px 0;direction:rtl}' +
      '.nlpk__row{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}.nlpk__row button{font:500 13px/18px var(--nli-sans);min-height:40px;padding:8px 12px;border:1px solid var(--nli-line);border-radius:999px;background:#fff;color:var(--nli-ink2);cursor:pointer;margin:0}' +
      '.nlpk__row button i{font:500 11.5px var(--nli-mono);font-style:normal;color:var(--nli-mute);margin-inline-start:4px}' +
      '.nlpk__row button[aria-pressed="true"]{background:var(--pkw);border-color:var(--pk);color:var(--pk)}' +
      '.nlpk__city{font:400 15px var(--nli-sans);min-height:40px;padding:8px 12px;border:1px solid var(--nli-line);border-radius:999px;background:#fff;color:var(--nli-ink);width:170px;max-width:100%}' +
      '.nlpk__job{margin:12px 0 0;border:1px solid var(--nli-line);border-radius:6px;background:#fff;padding:0 12px}.nlpk__job summary{cursor:pointer;list-style:none;min-height:44px;display:flex;align-items:center;gap:8px;font:600 15px/20px var(--nli-sans);color:var(--pk)}' +
      '.nlpk__job summary::-webkit-details-marker{display:none}.nlpk__job summary::before{content:"+";font:600 18px var(--nli-mono);width:18px}.nlpk__job[open] summary::before{content:"−"}.nlpk__job[open]{padding-bottom:12px}' +
      '.nlpk__lic details summary{cursor:pointer;padding:8px 14px;font:500 13px var(--nli-sans);color:var(--pk);list-style:none}.nlpk__lic details summary::-webkit-details-marker{display:none}' +
      '.nlpk__ans{margin:10px 0 0;padding:12px 14px;border-inline-start:4px solid var(--pk);background:var(--pkw);font:500 15px/23px var(--nli-sans);color:var(--nli-ink)}.nlpk__ans b{font-family:var(--nli-mono);font-weight:600;direction:ltr;unicode-bidi:isolate}' +
      '.nlpk__ans.no{border-color:#4F9A5C;background:#EEF6EF}.nlpk__ans a{color:var(--pk)}' +
      '.nlpk__bud{font:400 15px var(--nli-mono);min-height:40px;padding:8px 12px;border:1px solid var(--nli-line);border-radius:999px;width:150px;max-width:100%;direction:ltr;text-align:right}' +
      '.nlpk__meta{font:500 14px/20px var(--nli-sans);color:var(--nli-ink);margin:16px 0 6px}.nlpk__meta span{color:var(--nli-mute);font-weight:400}' +
      '.nlpk__lic{background:#fff;border:1px solid var(--nli-line);border-radius:6px;margin:10px 0;overflow:hidden}' +
      '.nlpk__lic header{background:var(--pkw);border-bottom:1px solid var(--nli-line);padding:10px 14px;display:flex;flex-wrap:wrap;gap:4px 14px;align-items:baseline}' +
      '.nlpk__lic h3{margin:0;font:700 18px/24px var(--nli-sans);color:var(--nli-ink)}.nlpk__lic header span{font:400 13px/18px var(--nli-sans);color:var(--nli-mute)}' +
      '.nlpk__lic header .no{font:500 13px var(--nli-mono);color:var(--pk);direction:ltr;unicode-bidi:isolate}' +
      '.nlpk__br{display:grid;grid-template-columns:minmax(0,1.7fr) 56px minmax(0,1.2fr);gap:4px 12px;padding:7px 14px;border-bottom:1px solid #EDF1F4;font:400 14px/20px var(--nli-sans);color:var(--nli-ink2)}' +
      '.nlpk__br .m{font:600 14px var(--nli-mono);color:var(--nli-ink)}.nlpk__br .c{font:400 12px var(--nli-mono);color:var(--nli-mute)}' +
      '.nlpk__br.hd{font:500 12px var(--nli-sans);color:var(--nli-mute);padding-top:6px;padding-bottom:4px}.nlpk__br.hit{background:#F7F9FD}' +
      '.nlpk__br .note{grid-column:1/-1;font:500 12.5px/18px var(--nli-sans);color:var(--pk)}.nlpk__br .note.r{color:var(--pkr)}' +
      '@media (max-width:600px){.nlpk__br{grid-template-columns:minmax(0,1fr) auto}.nlpk__br .lim{grid-column:1/-1;color:var(--nli-mute)}.nlpk__br.hd{display:none}}' +
      '.nlpk__st{display:flex;flex-wrap:wrap;gap:8px;padding:10px 14px}.nlpk__st span{font:600 12px/16px var(--nli-sans);padding:4px 10px;border:2px solid var(--pk);color:var(--pk);border-radius:3px;transform:rotate(-1.2deg)}' +
      '.nlpk__st span.f{background:var(--pk);color:#fff}.nlpk__st span.r{border-color:var(--pkr);color:var(--pkr)}' +
      '.nlpk__bt{display:flex;flex-wrap:wrap;gap:8px;padding:0 14px 14px}.nlpk__bt a{font:600 14px/18px var(--nli-sans);padding:10px 14px;border-radius:4px;text-decoration:none;min-height:44px;box-sizing:border-box;display:inline-flex;align-items:center}' +
      '.nlpk__bt a.p{background:var(--pk);color:#fff}.nlpk__bt a.s{border:1px solid var(--pk);color:var(--pk)}' +
      '.nlpk__more{display:block;width:100%;margin:8px 0 0;min-height:44px;border:1px solid var(--pk);border-radius:4px;background:#fff;color:var(--pk);font:600 14px var(--nli-sans);cursor:pointer}' +
      '.nlpk__foot{font:400 12.5px/18px var(--nli-sans);color:var(--nli-mute);margin:8px 0 0}' +
      '.nlpk__lad{display:grid;grid-template-columns:64px minmax(0,1fr);gap:10px 10px;align-items:end;margin:14px 0 0}.nlpk__lad .g{font:600 13px/18px var(--nli-sans);color:var(--nli-ink);align-self:center}' +
      '.nlpk__bars{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:4px;align-items:end;height:92px;border-bottom:1px solid var(--nli-line)}' +
      '.nlpk__bars div{background:#B8C6E3;border-radius:2px 2px 0 0;position:relative;transition:background .2s,height .4s}.nlpk__bars div.on{background:var(--pk)}.nlpk__bars div.inf{background:repeating-linear-gradient(135deg,#B8C6E3 0 6px,#CFD9EC 6px 12px)}.nlpk__bars div.inf.on{background:repeating-linear-gradient(135deg,var(--pk) 0 6px,#3B5BA9 6px 12px)}' +
      '.nlpk__bars div span{position:absolute;bottom:100%;inset-inline:0;text-align:center;font:500 10.5px/14px var(--nli-mono);color:var(--nli-ink);margin-bottom:2px;direction:ltr;white-space:nowrap}' +
      '.nlpk__lv{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:4px;font:600 12px var(--nli-mono);color:var(--nli-mute);text-align:center}';
    document.head.appendChild(s);
  }
  function branchMap(d) { var m = {}; d.pk.branches.forEach(function (b) { m[b[0]] = b; }); return m; }

  /* ---------------- pinkas (custom surface) ---------------- */
  NI.register('pinkas', {
    custom: function (root, d) {
      css();
      var M = d.pk, T = M.table, BR = branchMap(d), st = { q: '', anaf: 0, min: '', city: '', mukar: 0, job: '', bud: 0, off: 0 }, items = [], timer = 0, seq = 0;
      root.innerHTML = ''; root.classList.add('nli'); root.setAttribute('dir', 'rtl');
      var panel = document.createElement('div'); panel.className = 'nli__panel nlpk';
      panel.innerHTML = '<p class="nli__kicker">חיפוש · פנקס הקבלנים</p><h2 class="nli__title">בדיקת קבלן רשום</h2>' +
        '<p class="nli__lede">' + F.num(M.stats.contractors) + ' הקבלנים הרשומים בפנקס, בחיפוש אחד. מקלידים שם, מספר קבלן או ח״פ, או בוחרים ענף ועיר, ולכל קבלן רואים מה הסיווג שלו מתיר לבנות היום.</p>';
      var q = document.createElement('label'); q.className = 'nlpk__q';
      q.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="#1D3E8A" stroke-width="2"/><path d="M15.5 15.5 21 21" stroke="#1D3E8A" stroke-width="2" stroke-linecap="round"/></svg>';
      var qi = document.createElement('input'); qi.type = 'search'; qi.placeholder = 'שם הקבלן, מספר קבלן או ח״פ'; qi.setAttribute('aria-label', 'חיפוש קבלן לפי שם, מספר קבלן או ח״פ'); qi.autocomplete = 'off'; q.appendChild(qi); panel.appendChild(q);
      var row = document.createElement('div'); row.className = 'nlpk__row'; row.setAttribute('role', 'group'); row.setAttribute('aria-label', 'ענף ועיר');
      CHIPS.forEach(function (c) { var b = document.createElement('button'); b.type = 'button'; b.setAttribute('data-anaf', c[0]); b.innerHTML = esc(c[1]) + '<i>' + c[0] + '</i>'; b.setAttribute('aria-pressed', 'false');
        b.onclick = function () { st.anaf = st.anaf === c[0] ? 0 : c[0]; st.min = ''; st.job = ''; st.bud = 0; sync(); go(); }; row.appendChild(b); });
      var mk = document.createElement('button'); mk.type = 'button'; mk.textContent = 'מוכר לעבודות ממשלתיות'; mk.setAttribute('aria-pressed', 'false'); mk.onclick = function () { st.mukar = st.mukar ? 0 : 1; sync(); go(); }; row.appendChild(mk);
      var ci = document.createElement('input'); ci.className = 'nlpk__city'; ci.placeholder = 'עיר: כל הארץ'; ci.setAttribute('aria-label', 'עיר'); ci.setAttribute('list', 'nlpk-cities');
      var dl = document.createElement('datalist'); dl.id = 'nlpk-cities'; dl.innerHTML = M.cities.map(function (c) { return '<option value="' + esc(c[0]) + '">'; }).join('');
      ci.addEventListener('change', function () { var v = ci.value.trim(); st.city = M.cities.some(function (c) { return c[0] === v; }) ? v : ''; if (!st.city) ci.value = ''; go(); });
      row.appendChild(ci); row.appendChild(dl); panel.appendChild(row);
      var job = document.createElement('details'); job.className = 'nlpk__job'; if (window.innerWidth >= 860) job.open = true;
      job.innerHTML = '<summary>העבודה שלי: צריך קבלן רשום? באיזה סיווג?</summary>';
      var jr = document.createElement('div'); jr.className = 'nlpk__row'; jr.setAttribute('role', 'group'); jr.setAttribute('aria-label', 'סוג העבודה');
      JOBS.forEach(function (j) { var b = document.createElement('button'); b.type = 'button'; b.textContent = j[1]; b.setAttribute('data-job', j[0]); b.setAttribute('aria-pressed', 'false');
        b.onclick = function () { st.job = st.job === j[0] ? '' : j[0]; if (st.job) { st.q = ''; qi.value = ''; } if (st.job && !st.bud) st.bud = j[3] === 'main' ? 2000000 : 150000; applyJob(); }; jr.appendChild(b); });
      var br = document.createElement('div'); br.className = 'nlpk__row'; br.setAttribute('role', 'group'); br.setAttribute('aria-label', 'היקף העבודה בשקלים, לפני מע״מ');
      BUDGETS.forEach(function (v) { var b = document.createElement('button'); b.type = 'button'; b.textContent = money(v); b.setAttribute('data-bud', v); b.setAttribute('aria-pressed', 'false');
        b.onclick = function () { st.bud = v; bi.value = ''; st.q = ''; qi.value = ''; if (!st.job) st.job = v > 1000000 ? 'bldg' : 'reno'; applyJob(); }; br.appendChild(b); });
      var bi = document.createElement('input'); bi.className = 'nlpk__bud'; bi.inputMode = 'numeric'; bi.placeholder = '₪ סכום אחר'; bi.setAttribute('aria-label', 'היקף העבודה בשקלים');
      bi.addEventListener('input', function () { var v = +bi.value.replace(/[^\d]/g, ''); if (v > 0) { st.bud = v; if (!st.job) st.job = 'reno'; clearTimeout(timer); timer = setTimeout(applyJob, 450); } });
      br.appendChild(bi); job.appendChild(jr); job.appendChild(br);
      var ans = document.createElement('div'); ans.setAttribute('aria-live', 'polite'); job.appendChild(ans); panel.appendChild(job);
      var meta = document.createElement('p'); meta.className = 'nlpk__meta'; meta.setAttribute('aria-live', 'polite'); panel.appendChild(meta);
      var list = document.createElement('div'); panel.appendChild(list);  // the job block sits between the chips and the results: open, it filters them; closed, it is one line
      var foot = document.createElement('p'); foot.className = 'nlpk__foot';
      foot.textContent = 'נכון ל־' + F.date(M.asof) + ', מהמאגר הפתוח של משרד הבינוי והשיכון ב־data.gov.il. הסכומים לפי טבלת הסיווג שבתוקף מ־' + F.date(T.from) + '. הסטטוס העדכני, הטלפון והכתובת נמצאים ברשומה הרשמית של כל קבלן.';
      panel.appendChild(foot); root.appendChild(panel);

      function sync() {
        [].forEach.call(row.querySelectorAll('button[data-anaf]'), function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-anaf') === st.anaf)); });
        mk.setAttribute('aria-pressed', String(!!st.mukar));
        [].forEach.call(jr.children, function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-job') === st.job)); });
        [].forEach.call(br.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-bud') === st.bud && !bi.value)); });
        if (!st.job) ans.innerHTML = '';
      }
      function applyJob() {
        var j = JOBS.filter(function (x) { return x[0] === st.job; })[0];
        if (!j || !st.bud) { sync(); return; }
        job.open = true;
        var b = BR[j[2]], g = b ? b[2] : 'ג', need = needsRegistered(M.thr, j[3], st.bud), lv = levelFor(T, g, st.bud, j[2]);
        var thr = j[3] === 'main' ? M.thr.main : M.thr.sub, bname = b ? b[1] : '';
        st.anaf = j[2]; st.min = lv || '5';
        var h = j[1] + ' ב־<b>₪' + F.num(st.bud) + '</b> (לפני מע״מ): ';
        if (!need) h += 'החוק לא מחייב קבלן רשום, כי הסף ב' + (j[3] === 'main' ? 'ענף ראשי' : 'ענף משנה') + ' הוא <b>₪' + F.num(thr) + '</b>. קבלן רשום עדיין נותן בדיקה רשמית של הכישורים, והנה מי שרשום בענף ' + esc(bname) + '.';
        else h += 'החוק מחייב קבלן רשום (מעל <b>₪' + F.num(thr) + '</b> ב' + (j[3] === 'main' ? 'ענף ראשי' : 'ענף משנה') + '). צריך קבלן בענף ' + esc(bname) + ' (' + j[2] + ') בסיווג <b>' + code(g, lv || '5') + '</b> לפחות (' + (T[g][lv || '5'] === 0 ? 'בלי הגבלת סכום' : lim(T, g, lv || '5')) + ' באתר אחד).' +
          (j[0] === 'bldg' ? ' בבניין מגורים הסיווג קובע גם שטח: בסיווג ' + (lv || '5') + ' ' + (T.sqm[lv || '5'] ? 'עד ' + F.num(T.sqm[lv || '5']) + ' מ״ר' : 'ללא הגבלת שטח') + '.' : '');
        ans.innerHTML = '<p class="nlpk__ans' + (need ? '' : ' no') + '">' + h + '</p>';
        sync(); go();
      }
      function card(it) {
        var bs = it.b.slice().sort(function (x, y) { return ((y[0] === st.anaf) - (x[0] === st.anaf)) || (rank(y[2]) - rank(x[2])) || (x[0] - y[0]); });
        var line = function (b) {
          var name = BR[b[0]] ? BR[b[0]][1] : '', hit = st.anaf && b[0] === st.anaf;
          return '<div class="nlpk__br' + (hit ? ' hit' : '') + '"><span>' + esc(name) + ' <span class="c">' + b[0] + '</span></span><span class="m">' + esc(code(b[1], b[2])) + '</span><span class="lim">' + lim(T, b[1], b[2]) + '</span>' +
            (b[3] ? '<span class="note' + (red(b[3]) ? ' r' : '') + '">' + esc(b[3]) + '</span>' : '') + '</div>';
        };
        var rows = bs.slice(0, 5).map(line).join('') + (bs.length > 5 ? '<details><summary>+ עוד ' + (bs.length - 5) + ' ענפים</summary>' + bs.slice(5).map(line).join('') + '</details>' : '');
        var stamps = '<span>רשום בפנקס' + (it.y ? ' מאז ' + it.y : '') + '</span>' + (it.mukar ? '<span class="f">מוכר לעבודות ממשלתיות בסיווג ' + it.mukar + '</span>' : '') +
          (it.b.some(function (b) { return b[3] && red(b[3]); }) ? '<span class="r">יש הגבלה: בדקו ברשומה הרשמית</span>' : '');
        return '<article class="nlpk__lic"><header><h3>' + esc(it.name) + '</h3><span>' + esc(it.city) + '</span><span class="no">קבלן ' + it.n + (it.co ? ' · ח״פ ' + esc(it.co) : '') + '</span></header>' +
          '<div class="nlpk__br hd"><span>ענף</span><span>סיווג</span><span>מותר באתר אחד, לפני מע״מ</span></div>' + rows +
          '<div class="nlpk__st">' + stamps + '</div><div class="nlpk__bt"><a class="p" href="' + REC + it.n + '" target="_blank" rel="noopener">לרשומה הרשמית ב־gov.il</a>' +
          (it.page ? '<a class="s" href="' + esc(it.page) + '">לפרופיל בנדלן</a>' : '') + '</div></article>';
      }
      function go(more) {
        if (!more) st.off = 0;
        var p = { q: st.q, city: st.city, anaf: st.anaf || '', min: st.min, mukar: st.mukar || '', off: st.off };
        if (!st.q && !st.city && !st.anaf && !st.mukar) { meta.textContent = ''; list.innerHTML = '<p class="nlpk__foot">הקלידו שם או מספר, או בחרו ענף, עיר או סוג עבודה. דוגמה: <a href="#" data-ex="אלקטרה">אלקטרה</a> · <a href="#" data-ex="j:reno">שיפוץ דירה</a> · <a href="#" data-ex="m">קבלני ג5 מוכרים</a></p>'; wireEx(); return; }
        var my = ++seq; meta.innerHTML = 'מחפש…';
        var u = '/wp-json/nadlan/v1/pinkas?' + Object.keys(p).filter(function (k) { return p[k] !== '' && p[k] !== 0; }).map(function (k) { return k + '=' + encodeURIComponent(p[k]); }).join('&');
        fetch(u, { credentials: 'omit' }).then(function (r) { return r.json(); }).then(function (r) {
          if (my !== seq) return;
          items = more ? items.concat(r.items) : r.items;
          meta.innerHTML = r.total ? (r.total === 1 ? 'נמצא <b>קבלן אחד</b>' : 'נמצאו <b>' + F.num(r.total) + '</b> קבלנים') + (r.total > items.length ? ' <span>· מוצגים ' + F.num(items.length) + '</span>' : '') : 'לא נמצא קבלן כזה בפנקס. <span>בדקו את האיות, או חפשו לפי מספר הקבלן.</span>';
          list.innerHTML = items.map(card).join('');
          if (r.total > items.length) { var m = document.createElement('button'); m.type = 'button'; m.className = 'nlpk__more'; m.textContent = 'עוד ' + Math.min(30, r.total - items.length) + ' קבלנים'; m.onclick = function () { st.off = items.length; go(true); }; list.appendChild(m); }
        }).catch(function () { if (my === seq) meta.textContent = 'החיפוש לא זמין כרגע. אפשר לחפש ישירות באתר רשם הקבלנים ב־gov.il.'; });
      }
      function wireEx() {
        [].forEach.call(list.querySelectorAll('a[data-ex]'), function (a) { a.onclick = function (e) { e.preventDefault(); var x = a.getAttribute('data-ex');
          if (x === 'm') { st.anaf = 100; st.min = '5'; st.mukar = 1; sync(); go(); }
          else if (x.indexOf('j:') === 0) { st.job = x.slice(2); st.bud = 150000; applyJob(); }
          else { qi.value = x; st.q = x; go(); } }; });
      }
      qi.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(function () { var v = qi.value.trim(); if (v.length === 1 && !/\d/.test(v)) return; st.q = v; go(); }, 300); });
      var pre = root.getAttribute('data-nli-set'); try { var S = pre ? JSON.parse(pre) : {}; if (S.preset && S.preset.indexOf('job-') === 0) { st.job = S.preset.slice(4); st.bud = S.price || 150000; } } catch (e) {}
      if (st.job) applyJob(); else { sync(); go(); }
    }
  });

  /* ---------------- sivug: the classification ladder ---------------- */
  NI.register('sivug', {
    custom: function (root, d) {
      css();
      var M = d.pk, T = M.table, bud = 2000000;
      root.innerHTML = ''; root.classList.add('nli'); root.setAttribute('dir', 'rtl');
      var panel = document.createElement('div'); panel.className = 'nli__panel nlpk';
      panel.innerHTML = '<p class="nli__kicker">טבלה · סיווג קבלנים</p><h2 class="nli__title">כמה מותר לכל סיווג, באתר אחד</h2>' +
        '<p class="nli__lede">בוחרים סכום, ובכל קבוצה נצבע הסיווג הנמוך שמכסה אותו. הסכומים באלפי ₪, לפני מע״מ, בתוקף מ־' + F.date(T.from) + ' ועד ' + F.date(T.to) + '.</p>';
      var br = document.createElement('div'); br.className = 'nlpk__row'; br.setAttribute('role', 'group'); br.setAttribute('aria-label', 'היקף העבודה');
      [500000, 2000000, 5000000, 10000000, 25000000, 60000000].forEach(function (v) { var b = document.createElement('button'); b.type = 'button'; b.textContent = money(v); b.setAttribute('data-bud', v); b.onclick = function () { bud = v; draw(); }; br.appendChild(b); });
      panel.appendChild(br);
      var lad = document.createElement('div'); lad.className = 'nlpk__lad'; panel.appendChild(lad);
      var out = document.createElement('p'); out.className = 'nlpk__foot'; out.setAttribute('aria-live', 'polite'); panel.appendChild(out);
      var note = document.createElement('p'); note.className = 'nlpk__foot';
      note.textContent = 'סיווג ק קיים רק בענף השיפוצים (131). בבנייה למגורים הסיווג קובע גם שטח: ' + ['1', '2', '3', '4'].map(function (l) { return F.num(T.sqm[l]); }).join(' / ') + ' מ״ר בסיווגים 1 עד 4, ובסיווג 5 ללא הגבלה. הסכומים מתעדכנים ב־1 באפריל וב־1 באוקטובר לפי מדד תשומות הבנייה למגורים.';
      panel.appendChild(note); root.appendChild(panel);
      var max = Math.log(60000), min = Math.log(500);
      function h(v) { return v === 0 ? 84 : Math.max(8, Math.round(76 * (Math.log(v) - min) / (max - min))); }  // room above the tallest bar for its figure
      function draw() {
        [].forEach.call(br.children, function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-bud') === bud)); });
        var html = '<span></span><div class="nlpk__lv">' + LV.map(function (l) { return '<span>' + l + '</span>'; }).join('') + '</div>', say = [];
        ['א', 'ב', 'ג'].forEach(function (g) {
          var need = levelFor(T, g, bud, g === 'א' ? 131 : 0);
          html += '<span class="g">קבוצה ' + g + '</span><div class="nlpk__bars">' + LV.map(function (l) {
            if (!(l in T[g])) return '<div style="height:0;background:none"></div>';
            var v = T[g][l]; return '<div class="' + (v === 0 ? 'inf' : '') + (l === need ? ' on' : '') + '" style="height:' + h(v) + '%"><span>' + (v === 0 ? '∞' : F.num(v)) + '</span></div>';
          }).join('') + '</div>';
          say.push('קבוצה ' + g + ': ' + (need ? 'סיווג ' + code(g, need) : '—'));
        });
        lad.innerHTML = html;
        out.innerHTML = 'עבודה של <b>₪' + F.num(bud) + '</b> באתר אחד: ' + say.join(' · ') + '.';
      }
      draw();
    }
  });
})();
