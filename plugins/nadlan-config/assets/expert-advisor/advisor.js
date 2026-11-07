/* NadLan real-estate advisor 0.1.2 (HAD-680, 7.11.2026; 0.1.1: starts when the page is ready, so the order of the footer never matters;
   0.1.2: the English guide's own wrapper (.nlint, after its opening paragraph) and never above the page's opening; figures only in bdi). Runs only where inc/expert-advisor.php printed the section
   (?advisor=on on a listed page). It moves the section to its place in the reading order (after the guide's opening, or
   after the project's map), sends the conversation to POST /wp-json/nadlan/v1/advisor, draws the answer, the readout
   cells and the deal stage, and posts the "talk to a person" form to the site's existing lead route /wp-json/nadlan/v1/lead
   (source expert_advisor, with the visit id of the visit trail when there is one). The conversation lives in this page only:
   nothing is kept in the browser's storage. No floating element, nothing fixed on the screen. */
(function (w, d) {
  'use strict';
  var VERSION = '0.1.2';
  function boot() {
  var cfg = w.NL_ADV_CFG || null;
  var root = d.getElementById('nladv');
  if (!cfg || !root || w.NL_ADV) return;
  var S = {};
  try { S = JSON.parse((d.getElementById('nladv-str') || {}).textContent || '{}'); } catch (e) { S = {}; }
  var EN = cfg.lang === 'en';
  var log = d.getElementById('nladv-log');
  var chips = d.getElementById('nladv-chips');
  var ask = d.getElementById('nladv-ask');
  var q = d.getElementById('nladv-q');
  var hand = d.getElementById('nladv-hand');
  var openBtn = d.getElementById('nladv-open');
  var msgs = [];
  var busy = false;
  var answered = 0;

  /* ---------------------------------------------------------------- the place in the page */
  function place() {
    var spots = cfg.kind === 'project'
      ? [['section.nlpjx-map', 'after'], ['.nlps-below', 'after'], ['.nlps-stagebox', 'after'], ['.entry-content', 'append']]
      : [['.nadlan-guide > section.hero', 'after'], ['.nadlan-guide section.hero', 'after'], ['.nlint > p.lede', 'after'], ['.entry-content h1 + p', 'after'],
         ['.entry-content h1 ~ p', 'after'], ['.entry-content > p', 'after'], ['.entry-content', 'append'], ['main', 'append']]; // never above the page's opening
    for (var i = 0; i < spots.length; i++) {
      var el = d.querySelector(spots[i][0]);
      if (!el) continue;
      if (spots[i][1] === 'after') el.parentNode.insertBefore(root, el.nextSibling);
      else if (spots[i][1] === 'append') el.appendChild(root);
      else el.insertBefore(root, el.firstChild);
      root.setAttribute('data-spot', spots[i][0]);
      break;
    }
    root.hidden = false;
  }

  /* ---------------------------------------------------------------- safe text */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }
  function okHref(u) {
    u = String(u || '').trim();
    if (/^\/(?!\/)/.test(u)) return u;
    if (/^https:\/\/([a-z0-9-]+\.)*(nad-lan\.co\.il|gov\.il|boi\.org\.il|cbs\.gov\.il|kolzchut\.org\.il|nevo\.co\.il)(\/|$)/i.test(u)) return u;
    return '';
  }
  function inline(s) {
    var t = esc(s);
    t = t.replace(/\[([^\]]{1,120})\]\(([^)\s]{1,400})\)/g, function (m, label, href) {
      var h = okHref(href.replace(/&amp;/g, '&'));
      if (!h) return label;
      var ext = !/^https:\/\/([a-z0-9-]+\.)*nad-lan\.co\.il/i.test(h) && h.charAt(0) !== '/';
      return '<a href="' + esc(h) + '"' + (ext ? ' target="_blank" rel="noopener"' : '') + '>' + label + '</a>';
    });
    t = t.replace(/\*\*([^*]{1,200})\*\*/g, '<strong>$1</strong>');
    t = t.replace(/(₪\s?[\d,.]*\d|[\d][\d,.]*\s?(?:₪|%))/g, '<bdi>$1</bdi>'); // figures only: a Hebrew word never takes the figure face
    return t;
  }
  /** a small, safe subset: paragraphs, bullet and numbered lists, bold, links to the site and official sites */
  function render(md) {
    var lines = String(md || '').replace(/\r/g, '').split('\n');
    var out = [], list = null, para = [];
    function flushP() { if (para.length) { out.push('<p>' + para.map(inline).join('<br>') + '</p>'); para = []; } }
    function flushL() { if (list) { out.push('<' + list.t + '>' + list.items.map(function (x) { return '<li>' + inline(x) + '</li>'; }).join('') + '</' + list.t + '>'); list = null; } }
    lines.forEach(function (raw) {
      var l = raw.replace(/^#{1,6}\s+/, '').trim();
      var b = /^[-*•]\s+(.*)$/.exec(l), n = /^\d{1,2}[.)]\s+(.*)$/.exec(l);
      if (!l) { flushP(); flushL(); return; }
      if (b || n) {
        flushP();
        var t = b ? 'ul' : 'ol';
        if (!list || list.t !== t) { flushL(); list = { t: t, items: [] }; }
        list.items.push((b || n)[1]);
        return;
      }
      flushL();
      para.push(l);
    });
    flushP(); flushL();
    return out.join('');
  }

  /* ---------------------------------------------------------------- figures */
  function ils(n) { return '₪' + Math.round(Number(n) || 0).toLocaleString('en-US'); }
  function pct(r) { return (Math.round(Number(r) * 10000) / 100) + '%'; }
  function dmy(iso) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || '')); return m ? (+m[3]) + '.' + (+m[2]) + '.' + m[1] : String(iso || ''); }
  function ym(iso) { var m = /^(\d{4})-(\d{2})/.exec(String(iso || '')); return m ? (+m[2]) + '.' + m[1] : String(iso || ''); }
  var TRACK = EN ? { single: 'only home', extra: 'additional home', oleh: 'new immigrant', foreign: 'foreign resident' }
    : { single: 'דירה יחידה', extra: 'דירה נוספת', oleh: 'עולה חדש', foreign: 'תושב חוץ' };
  /** a row: the label (plain words, figures already wrapped) and its value; a range keeps reading order with "עד" / "to" */
  function row(k, v) { return '<li><span>' + k + '</span><b>' + v + '</b></li>'; }
  function fig(n) { return '<bdi>' + ils(n) + '</bdi>'; }
  function span(a, b) { return fig(a) + (EN ? ' to ' : ' עד ') + fig(b); }
  function more(link) {
    var h = okHref(link);
    return h ? ' · <a href="' + esc(h) + '">' + (EN ? 'Full calculator' : 'לחישוב המלא') + '</a>' : '';
  }
  function card(c) {
    var x = c && c.data ? c.data : null;
    if (!x) return '';
    var h = '';
    if (c.kind === 'tax') {
      h += '<p class="nladv__card-k">' + (EN ? 'Purchase tax · ' : 'מס רכישה · ') + esc(TRACK[x.track] || x.track) + ' · ' + ils(x.price) + '</p>';
      h += '<p class="nladv__fig"><span>' + fig(x.tax) + '</span></p><ul class="nladv__rows">';
      (x.brackets || []).forEach(function (b) {
        var lab = b.to === null ? (EN ? 'above ' : 'מעל ') + fig(b.from) : (b.from ? span(b.from, b.to) : (EN ? 'up to ' : 'עד ') + fig(b.to));
        h += row('<bdi>' + pct(b.rate) + '</bdi> · ' + lab, fig(b.tax));
      });
      h += '</ul><p class="nladv__src">' + (EN ? 'Source: Israel Tax Authority brackets, valid until ' : 'מקור: מדרגות רשות המסים, בתוקף עד ') + esc(dmy(x.valid_until)) + more(c.link) + '</p>';
    } else if (c.kind === 'mortgage') {
      h += '<p class="nladv__card-k">' + (EN ? 'Monthly payment · ' : 'החזר חודשי · ') + ils(x.loan) + (EN ? ' over ' : ' ל-') + esc(x.years) + (EN ? ' years' : ' שנים') + '</p>';
      h += '<p class="nladv__fig"><span>' + fig(x.monthly) + '</span><small>' + (EN ? 'a month' : 'בחודש') + '</small></p><ul class="nladv__rows">';
      h += row(esc(EN ? 'Rate used' : 'הריבית בחישוב') + (x.rate_is_market_average ? esc(EN ? ' (BoI average, fixed unlinked)' : ' (ממוצע, קבועה לא צמודה)') : ''), '<bdi>' + esc(x.rate_used) + '%</bdi>');
      h += row(esc(EN ? 'Total repaid' : 'סך כל ההחזרים'), fig(x.total_paid));
      if (x.prime) h += row(esc(EN ? 'Prime today' : 'הפריים היום'), '<bdi>' + esc(x.prime) + '%</bdi>');
      h += '</ul><p class="nladv__src">' + (EN ? 'Source: Bank of Israel, average new mortgage rates ' : 'מקור: בנק ישראל, ריביות המשכנתאות הממוצעות ') + esc(ym(x.market_month)) + more(c.link) + '</p>';
    } else if (c.kind === 'costs') {
      var lo = x.cash_needed[0], hi = x.cash_needed[1];
      h += '<p class="nladv__card-k">' + (EN ? 'Cash needed · ' : 'כמה כסף צריך · ') + esc(TRACK[x.track] || x.track) + ' · ' + ils(x.price) + '</p>';
      h += '<p class="nladv__fig"><span>' + fig(lo) + '</span><small>' + (EN ? 'to ' : 'עד ') + fig(hi) + '</small></p>';
      var share = Math.max(2, Math.min(60, (x.costs_on_top[1] / Math.max(1, x.equity_for_price + x.costs_on_top[1])) * 100));
      h += '<div class="nladv__bar" aria-hidden="true"><i style="width:' + (100 - share) + '%;background:var(--a-open)"></i><i style="width:' + share + '%;background:var(--a-civic)"></i></div><ul class="nladv__rows">';
      h += row(esc(EN ? 'Equity for the price' : 'הון עצמי למחיר') + ' (<bdi>' + Math.round((1 - x.max_ltv) * 100) + '%</bdi>)', fig(x.equity_for_price));
      h += row(esc(EN ? 'Purchase tax' : 'מס רכישה'), fig(x.purchase_tax));
      h += row(esc(EN ? 'Lawyer incl. VAT' : 'עורך דין כולל מע״מ'), span(x.lawyer_with_vat[0], x.lawyer_with_vat[1]));
      h += row(esc(EN ? 'Appraiser and inspection' : 'שמאי ובדק בית'), span(x.appraiser[0] + x.home_inspection[0], x.appraiser[1] + x.home_inspection[1]));
      if (x.broker_with_vat) h += row(esc(EN ? 'Broker incl. VAT' : 'תיווך כולל מע״מ'), fig(x.broker_with_vat));
      h += '</ul><p class="nladv__src">' + (EN ? 'Sources: Tax Authority, Bank of Israel directive 329, fee survey ' : 'מקורות: רשות המסים, הוראה 329 של בנק ישראל, סקירת שכר טרחה ') + esc(dmy(x.checked)) + more(c.link) + '</p>';
    }
    return h ? '<div class="nladv__card">' + h + '</div>' : '';
  }

  /* ---------------------------------------------------------------- the log */
  function now() { var t = new Date(); return ('0' + t.getHours()).slice(-2) + ':' + ('0' + t.getMinutes()).slice(-2); }
  function add(role, html, extra) {
    var el = d.createElement('div');
    el.className = 'nladv__msg nladv__msg--' + (role === 'user' ? 'u' : 'a');
    el.innerHTML = '<p class="nladv__who">' + esc(role === 'user' ? (S.you || '') : (S.adv || '')) + ' · ' + now() + '</p><div class="nladv__body">' + html + '</div>' + (extra || '');
    log.appendChild(el);
    return el;
  }
  function stage(n) {
    n = Number(n) || 0;
    if (!n) return;
    Array.prototype.forEach.call(root.querySelectorAll('.nladv__track li'), function (li) {
      var k = Number(li.getAttribute('data-stage'));
      li.classList.toggle('is-now', k === n);
      li.classList.toggle('is-past', k < n);
    });
  }
  function setChips(list) {
    if (!list || !list.length) return;
    chips.innerHTML = list.map(function (t) { return '<button type="button" class="nladv__chip">' + esc(t) + '</button>'; }).join('');
  }
  function showHand() { hand.hidden = false; openBtn.hidden = true; }

  function send(text) {
    text = String(text || '').trim();
    if (!text || busy) return;
    busy = true;
    var btn = ask.querySelector('.nladv__send');
    btn.disabled = true;
    add('user', '<p>' + esc(text).replace(/\n/g, '<br>') + '</p>');
    msgs.push({ role: 'user', content: text.slice(0, 1200) });
    q.value = '';
    var wait = d.createElement('div');
    wait.className = 'nladv__busy';
    wait.innerHTML = '<span>' + esc(S.busy || '') + '</span><i></i><i></i><i></i>';
    log.appendChild(wait);
    var body = JSON.stringify({ page: cfg.page, tok: cfg.tok, lang: cfg.lang, messages: msgs.slice(-16) });
    w.fetch(cfg.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: body, credentials: 'same-origin' })
      .then(function (r) { return r.json().catch(function () { return { ok: false, code: 'http_' + r.status }; }); })
      .then(function (j) {
        wait.remove();
        if (!j || !j.ok) {
          msgs.pop();
          var cap = j && (j.code === 'nladv_cap');
          add('assistant', '<p class="nladv__err">' + esc(cap ? S.cap : S.err) + '</p>');
          if (cap) showHand();
          return;
        }
        answered++;
        msgs.push({ role: 'assistant', content: String(j.answer).slice(0, 4000) });
        var cards = (j.cards || []).map(card).join('');
        add('assistant', render(j.answer), cards ? '<div class="nladv__cards">' + cards + '</div>' : '');
        stage(j.stage);
        setChips(j.next);
        if (j.handoff) showHand(); else if (answered >= 1 && hand.hidden) openBtn.hidden = false;
      })
      .catch(function () { wait.remove(); msgs.pop(); add('assistant', '<p class="nladv__err">' + esc(S.err) + '</p>'); })
      .then(function () { busy = false; btn.disabled = false; });
  }

  /* ---------------------------------------------------------------- the team's form: the site's existing lead route */
  function visitId() {
    try {
      var o = JSON.parse(w.localStorage.getItem('nl_vid') || 'null');
      if (o && /^[A-Za-z0-9_-]{16,32}$/.test(String(o.id))) return String(o.id);
    } catch (e) { /* no storage */ }
    return '';
  }
  function summary() {
    var lines = [(EN ? 'Conversation with the NadLan advisor on: ' : 'שיחה עם יועץ הנדל״ן בעמוד: ') + cfg.title + ' (' + w.location.pathname + ')'];
    msgs.forEach(function (m) { if (m.role === 'user') lines.push((EN ? 'Q: ' : 'שאלה: ') + m.content.slice(0, 220)); });
    var last = msgs.filter(function (m) { return m.role === 'assistant'; }).pop();
    if (last) lines.push((EN ? 'Last answer: ' : 'תשובה אחרונה: ') + last.content.replace(/\s+/g, ' ').slice(0, 420));
    return lines.join('\n').slice(0, 1500);
  }
  hand.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = hand.elements, go = hand.querySelector('.nladv__go'), done = hand.querySelector('.nladv__done');
    var name = String(f.name.value || '').trim(), phone = String(f.phone.value || '').replace(/[^\d+]/g, ''), email = String(f.email.value || '').trim();
    var bad = !name ? f.name : (phone.replace(/\D/g, '').length < 9 ? f.phone : (!f.consent.checked ? f.consent : null));
    if (bad) { bad.focus(); bad.setAttribute('aria-invalid', 'true'); return; }
    go.disabled = true;
    var h = { 'Content-Type': 'application/json' }, vid = visitId();
    if (vid) h['X-NL-Visit'] = vid;
    var payload = { name: name, phone: phone, email: email, goal: EN ? 'NadLan advisor' : 'יועץ הנדל״ן', message: summary(), source: 'expert_advisor',
      consent: 1, consent_text: S.consent || '', company: f.company.value || '' };
    if (cfg.kind === 'project') { payload.project_title = cfg.title; payload.project_wp_id = cfg.page; }
    w.fetch(cfg.lead, { method: 'POST', headers: h, body: JSON.stringify(payload), credentials: 'same-origin' })
      .then(function (r) { return r.json().then(function (j) { return { s: r.status, j: j }; }).catch(function () { return { s: r.status, j: null }; }); })
      .then(function (x) {
        if (x.s >= 200 && x.s < 300 && x.j && (x.j.ok || x.j.lead_id)) {
          Array.prototype.forEach.call(hand.querySelectorAll('.nladv__fields,.nladv__consent,.nladv__agree,.nladv__go'), function (el) { el.hidden = true; });
          done.textContent = S.thanks || ''; done.hidden = false;
        } else { done.textContent = S.err || ''; done.hidden = false; go.disabled = false; }
      })
      .catch(function () { done.textContent = S.err || ''; done.hidden = false; go.disabled = false; });
  });

  /* ---------------------------------------------------------------- wiring */
  ask.addEventListener('submit', function (e) { e.preventDefault(); send(q.value); });
  q.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); send(q.value); } });
  chips.addEventListener('click', function (e) { var b = e.target.closest ? e.target.closest('.nladv__chip') : null; if (b) send(b.textContent); });
  openBtn.hidden = true;
  openBtn.addEventListener('click', function () { showHand(); var i = hand.querySelector('input[name="name"]'); if (i) i.focus(); });
  place();
  w.NL_ADV = { version: VERSION, send: send, render: render, card: card };
  }
  /* 1.72.603 printed the script before the section, so it found nothing: now it waits for the page when the section is not there yet */
  if (d.getElementById('nladv') || d.readyState !== 'loading') boot(); else d.addEventListener('DOMContentLoaded', boot);
})(window, document);
