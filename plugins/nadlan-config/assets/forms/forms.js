/* NadLan: the life of a building, forms and approvals (HAD-768, 1.72.694). The page is printed by inc/forms-hub.php; this file adds
   the live search, the role and kind filters, the "what do I need now" instrument (role + stage -> the checklist with its deadlines,
   to copy, send on WhatsApp or print), deep links (#i-<id> opens and marks the card, #s-<stage> jumps to a stage) and copy buttons.
   No dependencies. */
(function () {
  'use strict';
  var root = document.getElementById('nlfm');
  var dataEl = document.getElementById('nlfm-data');
  if (!root || !dataEl) return;
  var D; try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var byId = {}; (D.items || []).forEach(function (x) { byId[x.id] = x; });
  var cards = [].slice.call(root.querySelectorAll('.nlfm-card'));
  var stages = [].slice.call(root.querySelectorAll('.nlfm-stage'));
  var q = document.getElementById('nlfm-q');
  var none = document.getElementById('nlfm-none');
  var st = { r: '', kd: '', q: '' };
  root.classList.add('is-js');
  var RM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  // Hebrew search: no niqqud, final letters folded, quotes and geresh dropped ("רמ"י" = "רמי", "תמ"א" = "תמא"), separators to spaces
  function norm(s) {
    return String(s || '').toLowerCase().replace(/[֑-ׇ]/g, '').replace(/[ךםןףץ]/g, function (c) { return { 'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ' }[c]; })
      .replace(/["'״׳`]/g, '').replace(/[\/\\\-_.,:;()]+/g, ' ').replace(/\s+/g, ' ').trim();
  }
  cards.forEach(function (c) { c._k = norm(c.getAttribute('data-k') + ' ' + c.textContent.slice(0, 600)); c._r = ' ' + (c.getAttribute('data-r') || '') + ' '; c._kd = c.getAttribute('data-kd'); });

  function toast(msg) {
    var t = document.createElement('div'); t.className = 'nlfm-toast'; t.setAttribute('role', 'status'); t.textContent = msg;
    document.body.appendChild(t); setTimeout(function () { t.remove(); }, 1800);
  }
  function copy(text, input) {
    function done() { toast('הועתק'); }
    function manual() {
      var i = input;
      if (!i) { i = document.createElement('textarea'); i.value = text; i.setAttribute('readonly', ''); i.style.position = 'fixed'; i.style.opacity = '0'; document.body.appendChild(i); }
      i.focus(); i.select();
      try { document.execCommand('copy'); done(); } catch (e) { toast('סמנו את הטקסט והעתיקו'); }
      if (!input) i.remove();
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, manual); else manual();
  }

  /* ---------------------------------------------------------------- filters */
  function apply() {
    var words = norm(st.q).split(' ').filter(Boolean), shown = 0;
    cards.forEach(function (c) {
      var ok = (!st.kd || c._kd === st.kd) && (!st.r || c._r.indexOf(' ' + st.r + ' ') > -1) && words.every(function (w) { return c._k.indexOf(w) > -1; });
      c.hidden = !ok; if (ok) shown++;
    });
    stages.forEach(function (s) { s.hidden = !s.querySelector('.nlfm-card:not([hidden])'); });
    root.classList.toggle('is-filtering', !!(st.r || st.kd || words.length));
    if (none) none.hidden = shown > 0;
  }
  function press(attr, val) { [].forEach.call(root.querySelectorAll('[' + attr + ']'), function (b) { b.setAttribute('aria-pressed', String(b.getAttribute(attr) === val)); }); }
  function clear() { st = { r: '', kd: '', q: '' }; if (q) q.value = ''; press('data-fm-r', ''); press('data-fm-kd', ''); apply(); }
  root.addEventListener('click', function (e) {
    var b = e.target.closest('button,a');
    if (!b || !root.contains(b)) return;
    if (b.hasAttribute('data-fm-r')) { st.r = b.getAttribute('data-fm-r'); press('data-fm-r', st.r); apply(); return; }
    if (b.hasAttribute('data-fm-kd')) { st.kd = b.getAttribute('data-fm-kd'); press('data-fm-kd', st.kd); apply(); return; }
    if (b.hasAttribute('data-fm-copy')) { copy(b.getAttribute('data-fm-copy')); return; }
    if (b.hasAttribute('data-fm-copy-in')) { var inp = document.getElementById(b.getAttribute('data-fm-copy-in')); if (inp) copy(inp.value, inp); return; }
    if (b.hasAttribute('data-fm-more')) { var sg = document.getElementById('s-' + b.getAttribute('data-fm-more')); if (sg) sg.classList.add('is-open'); var nx = sg && sg.querySelector('.nlfm-card.is-more'); if (nx) { var a = nx.querySelector('h3'); nx.setAttribute('tabindex', '-1'); nx.focus({ preventScroll: true }); } return; }
    if (b.hasAttribute('data-fm-go')) { e.preventDefault(); open(b.getAttribute('data-fm-go'), true); return; }
    if (b.hasAttribute('data-fm-stage')) {
      var s = document.getElementById('s-' + b.getAttribute('data-fm-stage'));
      if (s && s.hidden) clear();
    }
  });
  if (q) {
    var tm;
    q.addEventListener('input', function () { clearTimeout(tm); tm = setTimeout(function () { st.q = q.value; apply(); }, 90); });
    q.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') return;
      var first = cards.filter(function (c) { return !c.hidden; })[0];
      if (first) { e.preventDefault(); open(first.id.replace(/^i-/, ''), true); }
    });
  }

  /* ---------------------------------------------------------------- share: filled when a card's details open (keeps the page light) */
  function fillShare(card) {
    var box = card.querySelector('[data-fm-share]'); if (!box || box.childNodes.length) return;
    var id = card.id.replace(/^i-/, ''), t = (card.querySelector('h3') || {}).textContent || '', url = location.origin + '/forms/#i-' + id;
    var code = '<a href="' + url + '">' + t + '</a>';
    box.innerHTML = '<div class="nlfm-row"><button type="button" class="nlfm-chip" data-fm-copy="' + esc(url) + '">העתקת קישור לפריט</button>' +
      '<a class="nlfm-chip" href="https://wa.me/?text=' + encodeURIComponent(t + ': ' + url) + '" rel="noopener" target="_blank">שליחה בוואטסאפ</a></div>' +
      '<div class="nlfm-embed"><label for="fe-' + esc(id) + '">רוצים לקשר לכאן מהאתר שלכם? העתיקו את הקוד:</label><input id="fe-' + esc(id) + '" dir="ltr" readonly value="' + esc(code) + '">' +
      '<button type="button" class="nlfm-chip" data-fm-copy-in="fe-' + esc(id) + '">העתקת הקוד</button></div>';
  }
  root.addEventListener('toggle', function (e) { if (e.target.open && e.target.classList.contains('nlfm-more')) fillShare(e.target.closest('.nlfm-card')); }, true);

  /* ---------------------------------------------------------------- deep links */
  function open(id, push) {
    var c = document.getElementById('i-' + id); if (!c) return;
    if (c.hidden) clear();
    var sg = c.closest('.nlfm-stage'); if (sg) sg.classList.add('is-open');
    var d = c.querySelector('details'); if (d) { d.open = true; fillShare(c); }
    cards.forEach(function (x) { x.classList.toggle('is-hit', x === c); });
    c.scrollIntoView({ block: 'start', behavior: RM ? 'auto' : 'smooth' });
    if (push && history.replaceState) history.replaceState(null, '', '#i-' + id);
  }
  function fromHash() { var m = /^#i-(.+)$/.exec(location.hash); if (m) open(decodeURIComponent(m[1]), false); }
  window.addEventListener('hashchange', fromHash);
  if (location.hash) setTimeout(fromHash, 60);

  /* ---------------------------------------------------------------- the instrument: what do I need now */
  var box = document.getElementById('nlfm-wiz-in');
  if (!box || !D.roles || !D.roles.length || !D.stages) return;
  var ws = { r: D.roles[0].id, st: D.stages[0].id, date: '' };
  var today = new Date(); today.setHours(0, 0, 0, 0);
  function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function he(d) { return d.getDate() + '.' + (d.getMonth() + 1) + '.' + d.getFullYear(); }
  ws.date = iso(today);
  function list() { return (D.items || []).filter(function (x) { return x.st === ws.st && (!x.r.length || x.r.indexOf(ws.r) > -1); }); }
  function draw() {
    var h = '<div class="nlfm-wq"><span>מי אתם</span><div class="nlfm-seg" role="group" aria-label="מי אתם">' + D.roles.map(function (o) {
      return '<button type="button" data-w="r" data-v="' + esc(o.id) + '" aria-pressed="' + (ws.r === o.id) + '">' + esc(o.name) + '</button>';
    }).join('') + '</div></div>';
    h += '<div class="nlfm-wq"><label for="nlfm-wst">באיזה שלב הבניין</label><select id="nlfm-wst" data-w="st">' + D.stages.map(function (s) {
      return '<option value="' + esc(s.id) + '"' + (ws.st === s.id ? ' selected' : '') + '>' + esc(s.n + ' · ' + s.name) + '</option>';
    }).join('') + '</select></div>';
    var L = list(), withDays = L.filter(function (x) { return x.days; });
    if (withDays.length) h += '<div class="nlfm-wq"><label for="nlfm-wd">' + esc(withDays[0].from || 'תאריך תחילת המניין') + '</label><input id="nlfm-wd" type="date" data-w="date" value="' + esc(ws.date) + '"></div>';
    h += '<div class="nlfm-out" aria-live="polite">';
    if (!L.length) {
      h += '<p class="nlfm-out__k">לשלב הזה אין פריטים שמוטלים עליכם בתפקיד הזה. בחרו תפקיד אחר, או עברו על השלב כולו למטה.</p>';
    } else {
      h += '<p class="nlfm-out__k"><bdi>' + L.length + '</bdi> פריטים לשלב הזה</p><div class="nlfm-list">' + L.map(function (x, i) {
        var dl = '';
        if (x.days && ws.date) { var d1 = new Date(ws.date + 'T00:00:00'); d1.setDate(d1.getDate() + x.days); dl = ' <span class="nlfm-due" dir="ltr">' + esc(he(d1)) + '</span>'; }
        return '<div class="nlfm-li"><label><input type="checkbox" data-doc="' + i + '"><span>' + esc(x.t) + dl + '</span></label><a href="#i-' + esc(x.id) + '" data-fm-go="' + esc(x.id) + '" aria-label="פרטים: ' + esc(x.t) + '">פרטים</a></div>';
      }).join('') + '</div>';
      if (withDays.length) h += '<p class="nlfm-formula">המועדים מחושבים מהתאריך שבחרתם לפי המועד שבחוק, כמפורט בכל פריט. ודאו מול המקור.</p>';
      h += '<div class="nlfm-row"><button type="button" class="nlfm-chip" data-w-act="wa">שליחה בוואטסאפ</button><button type="button" class="nlfm-chip" data-w-act="copy">העתקת הרשימה</button><button type="button" class="nlfm-chip" data-w-act="print">הדפסה</button></div>';
    }
    box.innerHTML = h + '</div>';
  }
  function text() {
    var r = D.roles.filter(function (x) { return x.id === ws.r; })[0], s = D.stages.filter(function (x) { return x.id === ws.st; })[0];
    var lines = ['מה צריך עכשיו: ' + (r ? r.name : '') + ' · שלב ' + (s ? s.n + ' ' + s.name : '')];
    [].forEach.call(box.querySelectorAll('.nlfm-li'), function (li) { var c = li.querySelector('input'); lines.push((c && c.checked ? '✓ ' : '☐ ') + li.querySelector('label span').textContent.trim()); });
    lines.push(location.origin + '/forms/#s-' + ws.st);
    return lines.join('\n');
  }
  box.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    if (b.getAttribute('data-w') === 'r') { ws.r = b.getAttribute('data-v'); draw(); return; }
    var act = b.getAttribute('data-w-act');
    if (act === 'copy') copy(text());
    if (act === 'wa') window.open('https://wa.me/?text=' + encodeURIComponent(text()), '_blank', 'noopener');
    if (act === 'print') { document.body.classList.add('nlfm-printing'); setTimeout(function () { window.print(); document.body.classList.remove('nlfm-printing'); }, 30); }
  });
  box.addEventListener('change', function (e) {
    var k = e.target.getAttribute('data-w');
    if (k === 'st') { ws.st = e.target.value; draw(); var f = document.getElementById('nlfm-wst'); if (f) f.focus(); }
    if (k === 'date' && e.target.value) { ws.date = e.target.value; draw(); }
  });
  draw();
})();
