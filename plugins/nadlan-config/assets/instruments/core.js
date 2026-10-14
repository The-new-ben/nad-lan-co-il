/* NadLan Instruments core v1 (HAD-527, 14.10.2026). One small engine for every tool: a tool registers a spec (fields,
   defaults, compute) and the engine renders the form, the readout, the breakdown bar, scenarios, the detail table, the
   formula and sources, and the share bar (copy, WhatsApp, print). Example-first: every tool opens filled. No dependencies. */
(function () {
  'use strict';
  var REG = {};
  var nf0 = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });
  var fmt = {
    ils: function (n) { return '₪' + nf0.format(Math.round(n || 0)); },
    num: function (n, d) { return new Intl.NumberFormat('he-IL', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }).format(n || 0); },
    pct: function (n, d) { return (n < 0 ? '-' : '') + new Intl.NumberFormat('he-IL', { minimumFractionDigits: d == null ? 1 : d, maximumFractionDigits: d == null ? 1 : d }).format(Math.abs(n * 100)) + '%'; },
    month: function (key) { var p = String(key).split('-'); return p.length > 1 ? (+p[1]) + '.' + p[0] : key; },
    date: function (iso) { var p = String(iso).split('-'); return p.length === 3 ? (+p[2]) + '.' + (+p[1]) + '.' + p[0] : iso; }
  };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function parseMoney(v) { var n = parseFloat(String(v).replace(/[^\d.\-]/g, '')); return isFinite(n) ? n : NaN; }
  var ICON = {
    copy: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 7h9v10H7z"/><path d="M4 13V3h9"/></svg>',
    wa: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16l1-3.2A7 7 0 1 1 7.6 15z"/></svg>',
    print: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 8V3h10v5"/><path d="M5 14H3V8h14v6h-2"/><path d="M6 12h8v5H6z"/></svg>'
  };

  function field(f, st, onChange) {
    var w = el('div', 'nli__f');
    var id = 'nli-' + st.uid + '-' + f.id;
    if (f.type === 'segmented') {
      w.appendChild(el('span', 'nli__lab', esc(f.label)));
      var seg = el('div', 'nli__seg'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', f.label);
      f.options.forEach(function (o) {
        var b = el('button', '', esc(o.label)); b.type = 'button'; b.setAttribute('aria-pressed', String(st.v[f.id] === o.value));
        b.addEventListener('click', function () { st.v[f.id] = o.value; [].forEach.call(seg.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); onChange(f.id); });
        seg.appendChild(b);
      });
      w.appendChild(seg);
    } else if (f.type === 'rows') {
      w.appendChild(el('span', 'nli__lab', esc(f.label)));
      var rows = el('div', 'nli__rows'); w.appendChild(rows);
      var draw = function () {
        rows.innerHTML = '';
        (st.v[f.id] || []).forEach(function (r, i) {
          var row = el('div', 'nli__row');
          f.cols.forEach(function (c) {
            var box = el('div', 'nli__in');
            var inp = el('input'); inp.type = c.type === 'date' ? 'date' : 'text'; if (c.type !== 'date') inp.inputMode = 'decimal';
            inp.value = r[c.id]; inp.setAttribute('aria-label', c.label + ' ' + (i + 1));
            inp.addEventListener('input', function () { r[c.id] = c.type === 'date' ? inp.value : parseMoney(inp.value); st.v.__custom = true; onChange(f.id, true); });
            box.appendChild(inp); if (c.unit) box.appendChild(el('span', 'nli__unit', esc(c.unit)));
            row.appendChild(box);
          });
          var del = el('button', '', '×'); del.type = 'button'; del.setAttribute('aria-label', 'הסרת שורה ' + (i + 1));
          del.addEventListener('click', function () { st.v[f.id].splice(i, 1); st.v.__custom = true; draw(); onChange(f.id); });
          row.appendChild(del); rows.appendChild(row);
        });
      };
      draw(); st.redraw[f.id] = draw;
      var add = el('button', 'nli__add', '+ ' + esc(f.addLabel || 'הוספת שורה')); add.type = 'button';
      add.addEventListener('click', function () { st.v[f.id].push(f.blank()); st.v.__custom = true; draw(); onChange(f.id); });
      w.appendChild(add);
    } else {
      var lab = el('label', '', esc(f.label)); lab.htmlFor = id; w.appendChild(lab);
      var box2 = el('div', 'nli__in');
      var inp2;
      if (f.type === 'select') {
        inp2 = el('select'); f.options.forEach(function (o) { var op = el('option', '', esc(o.label)); op.value = o.value; if (st.v[f.id] === o.value) op.selected = true; inp2.appendChild(op); });
      } else {
        inp2 = el('input'); inp2.type = (f.type === 'date' || f.type === 'month') ? f.type : 'text';
        if (f.type === 'money' || f.type === 'number' || f.type === 'percent') inp2.inputMode = 'decimal';
      }
      inp2.id = id;
      var show = function () { var x = st.v[f.id]; inp2.value = f.type === 'money' ? nf0.format(x) : (x == null ? '' : x); };
      if (f.type !== 'select') show();
      inp2.addEventListener(f.type === 'select' ? 'change' : 'input', function () {
        st.v[f.id] = (f.type === 'money' || f.type === 'number' || f.type === 'percent') ? parseMoney(inp2.value) : inp2.value; onChange(f.id);
      });
      if (f.type === 'money') inp2.addEventListener('blur', function () { if (isFinite(st.v[f.id])) show(); });
      box2.appendChild(inp2);
      if (f.unit) box2.appendChild(el('span', 'nli__unit', esc(f.unit)));
      w.appendChild(box2);
      if (f.help) w.appendChild(el('span', 'nli__help', f.help));
    }
    var err = el('span', 'nli__err'); err.setAttribute('aria-live', 'polite'); w.appendChild(err); st.err[f.id] = err;
    if (f.showIf) { st.show.push(function () { w.hidden = !f.showIf(st.v); }); }
    return w;
  }

  function mount(root, spec, data) {
    var st = { uid: Math.random().toString(36).slice(2, 7), v: JSON.parse(JSON.stringify(spec.defaults(data))), err: {}, redraw: {}, scen: null, show: [] };
    root.innerHTML = ''; if (!root.parentNode || !root.parentNode.closest || !root.parentNode.closest('.nli')) root.classList.add('nli'); root.setAttribute('dir', 'rtl');
    var panel = el('div', 'nli__panel');
    if (spec.kicker) panel.appendChild(el('p', 'nli__kicker', esc(spec.kicker)));
    if (spec.title) panel.appendChild(el('h2', 'nli__title', esc(spec.title)));
    if (spec.lede) panel.appendChild(el('p', 'nli__lede', spec.lede));
    if (spec.strip) { var s = spec.strip(data); if (s && s.length) { var sp = el('div', 'nli__strip'); s.forEach(function (x) { sp.appendChild(el('div', '', '<span>' + esc(x.label) + '</span><strong>' + esc(x.value) + '</strong>')); }); panel.appendChild(sp); } }
    var grid = el('div', 'nli__grid'); var form = el('form', 'nli__form'); form.addEventListener('submit', function (e) { e.preventDefault(); });
    var out = el('div', 'nli__out'); out.setAttribute('aria-live', 'polite');
    grid.appendChild(form); grid.appendChild(out); panel.appendChild(grid);
    var table = el('details', 'nli__table'); var formula = el('p', 'nli__formula'); var src = el('p', 'nli__src');
    panel.appendChild(table); panel.appendChild(formula); panel.appendChild(src);
    var share = el('div', 'nli__share'); panel.appendChild(share);
    panel.appendChild(el('p', 'nli__eg', '<b>דוגמה</b>' + esc(spec.exampleNote || 'הערכים בפתיחה הם דוגמה. שנו אותם, והתוצאה מתעדכנת מיד.')));
    root.appendChild(panel);
    var last = null, t = 0;
    function onChange(id, keepRows) { if (spec.onField) spec.onField(id, st.v, data, function (fid) { if (st.redraw[fid] && !keepRows) st.redraw[fid](); }); clearTimeout(t); t = setTimeout(run, 90); }
    spec.fields.forEach(function (f) { form.appendChild(field(f, st, onChange)); });
    function run() {
      st.show.forEach(function (fn) { fn(); });
      Object.keys(st.err).forEach(function (k) { st.err[k].textContent = ''; });
      var r;
      try { r = spec.compute(st.v, data, st.scen); } catch (e) { r = { error: { field: null, msg: 'לא הצלחנו לחשב עם הערכים האלה.' } }; }
      if (r.error) { if (r.error.field && st.err[r.error.field]) st.err[r.error.field].textContent = r.error.msg; if (!last) out.innerHTML = '<p class="nli__note">' + esc(r.error.msg) + '</p>'; return; }
      last = r; paint(r);
    }
    function paint(r) {
      out.innerHTML = '';
      var a = el('div', 'nli__answer');
      a.innerHTML = '<span class="nli__alab">' + esc(r.answer.label) + '</span><output class="nli__fig' + (r.answer.tone === 'survey' ? ' is-survey' : '') + '">' + esc(r.answer.value) + '</output>' + (r.answer.sub ? '<span class="nli__asub">' + r.answer.sub + '</span>' : '');
      out.appendChild(a);
      if (r.breakdown) r.breakdown = r.breakdown.filter(function (b) { return b.value > 0.5; });
      if (r.breakdown && r.breakdown.length) {
        var tot = r.breakdown.reduce(function (s, b) { return s + Math.max(0, b.value); }, 0) || 1;
        var bw = el('div', ''); var bar = el('div', 'nli__bar'); bar.setAttribute('role', 'img');
        bar.setAttribute('aria-label', r.breakdown.map(function (b) { return b.label + ' ' + fmt.ils(b.value); }).join(', '));
        var lg = el('ul', 'nli__legend');
        r.breakdown.forEach(function (b) { var i = el('i', 'nli__k-' + b.kind); i.style.width = (100 * Math.max(0, b.value) / tot) + '%'; bar.appendChild(i); lg.appendChild(el('li', '', '<b class="nli__k-' + b.kind + '"></b>' + esc(b.label) + ' <bdi>' + esc(b.shown || fmt.ils(b.value)) + '</bdi>')); });
        bw.appendChild(bar); bw.appendChild(lg); out.appendChild(bw);
      }
      if (r.lines && r.lines.length) { var dl = el('dl', 'nli__lines'); r.lines.forEach(function (l) { dl.appendChild(el('div', '', '<dt>' + esc(l.label) + '</dt><dd>' + esc(l.value) + '</dd>')); }); out.appendChild(dl); }
      if (r.scenarios && r.scenarios.length) {
        var sc = el('div', 'nli__scen'); sc.setAttribute('role', 'group'); sc.setAttribute('aria-label', r.scenarioLabel || 'תרחישים');
        r.scenarios.forEach(function (s) { var b = el('button', '', '<span>' + esc(s.name) + '</span><strong>' + esc(s.value) + '</strong>'); b.type = 'button'; b.setAttribute('aria-pressed', String(!!s.on));
          b.addEventListener('click', function () { st.scen = s.key; run(); }); sc.appendChild(b); });
        if (r.scenarioLabel) out.appendChild(el('span', 'nli__alab', esc(r.scenarioLabel)));
        out.appendChild(sc);
      }
      if (r.note) out.appendChild(el('p', 'nli__note', r.note));
      if (r.table) {
        var open = table.open;
        table.innerHTML = '<summary>' + esc(r.table.title || 'הפירוט המלא') + '</summary><div class="nli__tw"><table><thead><tr>' + r.table.head.map(function (h) { return '<th scope="col">' + esc(h) + '</th>'; }).join('') + '</tr></thead><tbody>' +
          r.table.rows.map(function (row) { return '<tr>' + row.map(function (c, i) { var n = r.table.num && r.table.num.indexOf(i) > -1; return '<td' + (n ? ' class="n"' : '') + '>' + esc(c) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>';
        table.open = open; table.hidden = false;
      } else { table.hidden = true; }
      formula.textContent = r.formula || '';
      src.innerHTML = r.sources && r.sources.length ? 'מקורות: ' + r.sources.map(function (s) { return s.url ? '<a href="' + esc(s.url) + '" target="_blank" rel="noopener">' + esc(s.label) + '</a>' : esc(s.label); }).join(' · ') : '';
    }
    function shareText() { return last && last.text ? last.text + '\n' + location.origin + location.pathname : location.href; }
    var bc = el('button', 'is-primary', ICON.copy + '<span>העתקת התוצאה</span>'); bc.type = 'button';
    bc.addEventListener('click', function () { var tx = shareText(); var lab = bc.querySelector('span');
      var done = function () { lab.textContent = 'הועתק'; setTimeout(function () { lab.textContent = 'העתקת התוצאה'; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(tx).then(done, function () { window.prompt('העתיקו את התוצאה', tx); }); else window.prompt('העתיקו את התוצאה', tx); });
    var bw2 = el('a', '', ICON.wa + '<span>שליחה בוואטסאפ</span>'); bw2.target = '_blank'; bw2.rel = 'noopener';
    bw2.addEventListener('click', function () { bw2.href = 'https://wa.me/?text=' + encodeURIComponent(shareText()); });
    bw2.href = 'https://wa.me/';
    var bp = el('button', '', ICON.print + '<span>הדפסה או שמירה כקובץ</span>'); bp.type = 'button';
    bp.addEventListener('click', function () { table.open = true; window.print(); });
    share.appendChild(bc); share.appendChild(bw2); share.appendChild(bp);
    run();
    return { state: st, run: run };
  }

  function boot() {
    [].forEach.call(document.querySelectorAll('[data-nli]:not([data-nli-on])'), function (root) {
      var id = root.getAttribute('data-nli'); var spec = REG[id]; if (!spec) return;
      root.setAttribute('data-nli-on', '1');
      var srcs = (root.getAttribute('data-nli-data') || '').split(',').filter(Boolean);
      Promise.all(srcs.map(function (u) { return fetch(u, { credentials: 'omit' }).then(function (r) { return r.json(); }); })).then(function (list) {
        var data = {}; list.forEach(function (d, i) { data[d.key || ('d' + i)] = d; data['d' + i] = d; });
        mount(root, spec, data);
      }).catch(function () { root.innerHTML = '<p class="nli__note">הנתונים לא נטענו. רעננו את העמוד.</p>'; });
    });
  }
  window.NadLanInstruments = { register: function (id, spec) { REG[id] = spec; if (document.readyState !== 'loading') boot(); }, mount: mount, boot: boot, fmt: fmt, esc: esc };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
