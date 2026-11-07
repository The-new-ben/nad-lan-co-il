/*! NadLan visit trail 1.0.0 (HAD-678, Ben 7.11.2026). First-party record of what a visitor picks on a project page.
 *
 * Why: Hotjar cannot see inside the 3D stage (a canvas), so the floor, the direction, the opened tour or example apartment
 * and the WhatsApp tap were invisible. This file listens to the stage's own window events (nl:floor, nl:facing, nl:view,
 * nl:quarter, nl:floor-cta, nl:floor-action, nl:facility, nl:facility-tour, nl:tour, nl:example: bridge.js, slice.js,
 * tour.js, <dir>/stage.js, world/world.js fire them; nothing here touches the stage or showroom-engine/engine.js) and to
 * clicks on the page's call-to-action links and buttons, and sends a small batch to POST /wp-json/nadlan/v1/trail
 * (inc/visit-trail.php) every 20 seconds and when the page is left.
 *
 * What is recorded: the page, its language, the device class (phone / tablet / computer), the referring site's name, the
 * stage picks above, the kind and label of a tapped CTA (WhatsApp, call, mail, booking, a stage button), the id of a form
 * that is sent, the time the page was in view and how far it was scrolled.
 * What is never recorded: keystrokes, form field values, mouse or touch paths, the link a WhatsApp button opens (its
 * ready text), the IP address (the server does not store it).
 * Opt-out: with Global Privacy Control or Do Not Track on, nothing runs (no id, no storage, no request). Automated browsers
 * (navigator.webdriver) are not recorded either.
 * Visit id: 22 random characters in localStorage ("nl_vid"), valid 30 days from its creation, then a new one. It is sent with
 * the page's own lead requests (an X-NL-Visit header on same-origin POSTs to /wp-json/nadlan/v1/*, and a hidden field
 * nl_visit on forms posted to admin-post.php), so a lead made on this visit carries its trail.
 * Config: window.NL_TRAIL_CFG = { endpoint, page, lang } printed before this file (inc/visit-trail.php).
 * Node: require('./trail.js') returns the factory for the unit tests
 * (docs/research/2026-11-07-campaign-network/build/build-visit-trail/test_trail.js). */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) { module.exports = api; return; }
  if (root && root.document) { root.NL_TRAIL = api; api.boot(root); }
})(typeof window !== 'undefined' ? window : this, function () {
  'use strict';
  var VERSION = '1.0.0';
  var KEY = 'nl_vid';
  var TTL = 30 * 86400000;      // the visit id lives 30 days from its creation
  var EVERY = 20000;            // a batch every 20 s (only when something happened)
  var MAX_BATCH = 40;           // events in one request (the server takes up to 60)
  var MAX_PAGE = 400;           // events one page view may record at all
  var SAME_MS = 1500;           // the same event twice inside 1.5 s is one event
  var VIEW_MS = 8000;           // turning the view from the floor: at most one record per 8 s

  /* the stage's events and the fields kept from each (everything else in the detail is dropped) */
  var STAGE = {
    'nl:floor': 'floor', 'nl:facing': 'facing', 'nl:view': 'view', 'nl:quarter': 'quarter', 'nl:facility': 'facility',
    'nl:facility-tour': 'ftour', 'nl:floor-cta': 'fcta', 'nl:floor-action': 'faction', 'nl:tour': 'tour', 'nl:example': 'example'
  };

  function str(x, n) {
    if (x == null) return '';
    var s = String(x).replace(/[\u0000-\u001f\u007f]+/g, ' ').replace(/\s+/g, ' ').trim();
    return s.length > n ? s.slice(0, n) : s;
  }
  function int(x, lo, hi) {
    var n = Number(x);
    if (!isFinite(n)) return null;
    n = Math.round(n);
    return n < lo || n > hi ? null : n;
  }
  function bearing(x) {
    var n = Number(x);
    if (!isFinite(n)) return null;
    n = Math.round(((n % 360) + 360) % 360);
    return n === 360 ? 0 : n;
  }
  function put(o, k, v) { if (v !== null && v !== '' && v !== undefined) o[k] = v; return o; }

  /** the fields kept from a stage event's detail */
  function pick(type, d) {
    d = d || {};
    var o = {};
    switch (type) {
      case 'floor':
        put(o, 'f', int(d.floor, -5, 300)); put(o, 'tw', str(d.tower, 16)); put(o, 'src', str(d.source, 8)); break;
      case 'facing':
        put(o, 'f', int(d.floor, -5, 300)); put(o, 'b', bearing(d.bearing)); put(o, 'dir', str(d.facing || d.toward, 24));
        put(o, 'u', str(d.unit, 24)); put(o, 'tw', str(d.tower, 16)); put(o, 'lbl', str(d.label, 40)); put(o, 'src', str(d.source, 8)); break;
      case 'view':
        put(o, 'b', bearing(d.bearing)); put(o, 'src', str(d.source, 8)); break;
      case 'quarter':
        put(o, 'k', str(d.kind, 24)); put(o, 'n', str(d.name, 60)); break;
      case 'facility':
        put(o, 'n', str(d.name, 60)); put(o, 'id', str(d.id, 32)); break;
      case 'ftour':
        put(o, 'id', str(d.id, 32)); put(o, 'n', str(d.title, 60)); break;
      case 'fcta':
        put(o, 'f', int(d.floor, -5, 300)); put(o, 'b', bearing(d.bearing)); put(o, 'tw', str(d.tower, 16)); break;
      case 'faction':
        put(o, 'a', str(d.action, 16)); put(o, 'f', int(d.floor, -5, 300)); put(o, 'u', str(d.unit, 24)); put(o, 'tw', str(d.tower, 16)); break;
      case 'tour':
        put(o, 'o', d.open ? 1 : 0); put(o, 's', str(d.scene, 32)); break;
      case 'example':
        put(o, 'o', d.open ? 1 : 0); put(o, 'id', str(d.id, 32)); put(o, 'f', int(d.floor, -5, 300)); put(o, 'tw', str(d.tower, 16));
        put(o, 'dir', str(d.facing, 24)); break;
    }
    return o;
  }

  /* ---------------------------------------------------------------- opt-out and robots */
  function optedOut(w) {
    var n = (w && w.navigator) || {};
    if (n.globalPrivacyControl === true || n.globalPrivacyControl === 'true' || n.globalPrivacyControl === 1) return true;
    var dnt = n.doNotTrack != null ? n.doNotTrack : (w && w.doNotTrack != null ? w.doNotTrack : n.msDoNotTrack);
    return dnt === '1' || dnt === 1 || dnt === 'yes' || dnt === true;
  }
  function robot(w) {
    var n = (w && w.navigator) || {};
    return n.webdriver === true || /bot|crawl|spider|slurp|headless|lighthouse|pagespeed|gtmetrix|pingdom|prerender/i.test(String(n.userAgent || ''));
  }

  /* ---------------------------------------------------------------- ids */
  function rid(w, bytes) {
    var a = [], c = w && (w.crypto || w.msCrypto), i;
    if (c && c.getRandomValues) { a = Array.prototype.slice.call(c.getRandomValues(new Uint8Array(bytes))); }
    else { for (i = 0; i < bytes; i++) a.push(Math.floor(Math.random() * 256)); }
    var abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_', s = '';
    for (i = 0; i < a.length; i++) s += abc[a[i] & 63];
    return s;
  }
  var VID_RE = /^[A-Za-z0-9_-]{16,32}$/;
  /** the visit id: kept 30 days from its creation in localStorage; a page without storage gets an id for this page only */
  function visitId(w, now) {
    var st = null;
    try { st = w.localStorage; } catch (e) { st = null; }
    if (st) {
      try {
        var o = JSON.parse(st.getItem(KEY) || 'null');
        if (o && VID_RE.test(String(o.id)) && Number(o.at) > 0 && now - Number(o.at) < TTL && Number(o.at) <= now + 60000) return { id: o.id, kept: true };
      } catch (e) { /* a broken value is replaced */ }
      var id = rid(w, 22);
      try { st.setItem(KEY, JSON.stringify({ id: id, at: now })); return { id: id, kept: true }; } catch (e) { return { id: id, kept: false }; }
    }
    return { id: rid(w, 22), kept: false };
  }

  /* ---------------------------------------------------------------- clicks on the page's calls to action */
  var WA_RE = /^(https?:)?\/\/(wa\.me|api\.whatsapp\.com|chat\.whatsapp\.com|web\.whatsapp\.com)\//i;
  function where(el) {
    if (!el.closest) return '';
    if (el.closest('#nlcta')) return 'bar';
    if (el.closest('.rbs-qcard,.nlw-card')) return 'card';
    if (el.closest('#nlps-view,#nlps-view-cta,.nlps-below')) return 'view';
    if (el.closest('#nlps,.nlps-stage,.nlps-stagebox')) return 'stage';
    if (el.closest('.nlps-hero,.nlps-hero__cta')) return 'hero';
    if (el.closest('#nlsch')) return 'booking';
    if (el.closest('.nlpg')) return 'price';
    if (el.closest('footer,.nlpc-site-footer')) return 'footer';
    if (el.closest('header,.nlhp-top')) return 'header';
    if (el.closest('.nadlan-project-article')) return 'article';
    return '';
  }
  function label(el) {
    return str(el.getAttribute && (el.getAttribute('data-nl-label') || el.getAttribute('aria-label')) || el.textContent || '', 40);
  }
  /** {k, l, w, id, f} for a tap on a call to action; null for any other click (they are not recorded) */
  function clickKind(target) {
    var el = target && target.closest ? target.closest('a,button,summary,input[type=submit],[role=button],[data-nl-track]') : null;
    if (!el) return null;
    var href = String((el.getAttribute && el.getAttribute('href')) || '');
    var o = {}, m = function (q) { try { return el.matches(q); } catch (e) { return false; } };
    var tr = el.closest('[data-nl-track]');
    if (tr) { o.k = str(tr.getAttribute('data-nl-track'), 16) || 'cta'; }
    else if (m('[data-nl-whatsapp],[data-nlps-wa],[data-nlps-ev="hero-wa"]') || WA_RE.test(href) || /^whatsapp:/i.test(href) || href === '#nlws-wa') { o.k = 'wa'; }
    else if (/^tel:/i.test(href)) { o.k = 'tel'; }
    else if (/^mailto:/i.test(href)) { o.k = 'mail'; }
    else if (el.closest('#nlsch')) { o.k = m('.nlsch-go') ? 'book_send' : (m('.nlsch-day') ? 'book_day' : (m('.nlsch-time') ? 'book_time' : 'book')); }
    else if (m('[data-nlps-floor]')) { o.k = 'deal_floor'; put(o, 'f', int(el.getAttribute('data-nlps-floor'), -5, 300)); }
    else if (m('[data-nlps-tour]')) { o.k = 'tour_btn'; }
    else if (m('[data-nlps-step]')) { o.k = 'step'; put(o, 'id', str(el.getAttribute('data-nlps-step'), 32)); }
    else if (m('[data-nlps-ev]')) { o.k = 'cta'; put(o, 'id', str(el.getAttribute('data-nlps-ev'), 32)); }
    else if (m('button[type=submit],input[type=submit]') && el.form) { o.k = 'send'; put(o, 'id', str(el.form.id || el.form.getAttribute('name') || '', 32)); }
    else if (m('.nlds-btn,.nlps-hero__cta a,.nlcta-wa')) { o.k = 'cta'; }
    else return null;
    if (o.k !== 'book_day' && o.k !== 'book_time') put(o, 'l', label(el)); // a picked date or hour is the visitor's choice of a slot: not kept
    put(o, 'w', where(el));
    return o;
  }
  function formKind(f) {
    var act = String((f.getAttribute && f.getAttribute('action')) || '');
    return { k: /admin-post\.php/i.test(act) ? 'lead' : (f.closest && f.closest('#nlsch') ? 'book' : 'form'),
      id: str(f.id || (f.getAttribute && f.getAttribute('name')) || String(f.className || '').split(/\s+/)[0] || '', 32) };
  }

  /* ---------------------------------------------------------------- the lead link: the visit id rides the page's own lead requests */
  function leadUrl(w, url) {
    var u;
    try { u = new w.URL(String(url), w.location.href); } catch (e) { return false; }
    if (u.origin !== w.location.origin) return false;
    var p = u.pathname, rr = u.searchParams ? String(u.searchParams.get('rest_route') || '') : '';
    if (/\/v1\/trail\/?$/.test(p) || /\/v1\/trail\/?$/.test(rr)) return false;
    return /\/wp-json\/nadlan\/v1\//.test(p) || /^\/nadlan\/v1\//.test(rr) || /\/wp-admin\/admin-(ajax|post)\.php$/.test(p);
  }
  function wrapFetch(w, vid) {
    var of = w.fetch;
    if (typeof of !== 'function' || of.__nlvt) return of;
    var nf = function (input, init) {
      try {
        var isReq = typeof w.Request === 'function' && input instanceof w.Request;
        var url = isReq ? null : (typeof input === 'string' ? input : (input && input.href ? input.href : null));
        var method = String((init && init.method) || 'GET').toUpperCase();
        if (url && method === 'POST' && leadUrl(w, url) && typeof w.Headers === 'function') {
          var h = new w.Headers((init && init.headers) || undefined);
          if (!h.has('X-NL-Visit')) h.set('X-NL-Visit', vid);
          init = Object.assign({}, init, { headers: h });
        }
      } catch (e) { /* the request goes out exactly as it came */ }
      return arguments.length > 1 || init ? of.call(w, input, init) : of.call(w, input);
    };
    nf.__nlvt = true;
    nf.__nlvtOrig = of;
    w.fetch = nf;
    return of;
  }

  /* ---------------------------------------------------------------- the recorder */
  function create(w, cfg, deps) {
    cfg = cfg || {};
    deps = deps || {};
    var now = deps.now || function () { return Date.now(); };
    var d = w.document;
    var t0 = now();
    var vidInfo = visitId(w, t0);
    var vid = vidInfo.id, pv = rid(w, 12), seq = 0, total = 0, stopped = false;
    var queue = [], last = {}, lastView = 0, lastLeave = -1;
    var visMs = 0, visFrom = (!d || d.visibilityState !== 'hidden') ? t0 : 0, scrollMax = 0;
    var origFetch = typeof w.fetch === 'function' ? (w.fetch.__nlvtOrig || w.fetch) : null;
    var nav = w.navigator || {};
    var send = deps.send || function (url, body) {
      try {
        if (nav.sendBeacon && nav.sendBeacon(url, new w.Blob([body], { type: 'text/plain;charset=UTF-8' }))) return true;
      } catch (e) { /* fall through */ }
      try {
        if (origFetch) { origFetch.call(w, url, { method: 'POST', body: body, keepalive: true, credentials: 'same-origin', headers: { 'Content-Type': 'text/plain;charset=UTF-8' } }); return true; }
      } catch (e) { /* nothing more to try */ }
      return false;
    };

    function vis() { return Math.round(visMs + (visFrom ? now() - visFrom : 0)); }
    function dev() {
      var x = Number(w.innerWidth) || 0;
      return x && x < 768 ? 'm' : (x && x < 1100 ? 't' : 'd');
    }
    function refHost() {
      try {
        var r = d && d.referrer ? new w.URL(d.referrer) : null;
        if (!r || r.origin === w.location.origin) return '';
        return str(r.hostname.replace(/^www\./, '').toLowerCase(), 100);
      } catch (e) { return ''; }
    }
    function push(type, data) {
      if (stopped || total >= MAX_PAGE) return false;
      var at = now(), sig = type + JSON.stringify(data || {});
      if (last.sig === sig && at - last.at < SAME_MS) return false;
      if (type === 'view') { if (at - lastView < VIEW_MS) return false; lastView = at; }
      last = { sig: sig, at: at };
      var e = { t: type, at: at };
      for (var k in data) if (Object.prototype.hasOwnProperty.call(data, k)) e[k] = data[k];
      queue.push(e);
      total++;
      return true;
    }
    function payload(evs) {
      var o = { v: 1, vid: vid, pv: pv, seq: seq++, page: Number(cfg.page) || 0, path: str((w.location && w.location.pathname) || '/', 191),
        lang: str(cfg.lang || (d && d.documentElement && d.documentElement.lang) || '', 5).slice(0, 2).toLowerCase(), dev: dev(), now: now(), vis: vis(), ev: evs };
      if (o.seq === 0) put(o, 'ref', refHost());
      return JSON.stringify(o);
    }
    function flush() {
      if (!queue.length || !cfg.endpoint) return 0;
      var n = 0;
      while (queue.length && n < 4) {
        var evs = queue.slice(0, MAX_BATCH);
        if (!send(cfg.endpoint, payload(evs))) break; // kept for the next round
        queue.splice(0, evs.length);
        n++;
      }
      return n;
    }
    function leave() {
      var v = vis();
      if (Math.abs(v - lastLeave) < 1000) return;
      lastLeave = v;
      measure();
      var o = { vis: v };
      put(o, 'sc', int(scrollMax, 0, 100));
      last = {};
      push('leave', o);
    }
    function measure() {
      try {
        var doc = d.documentElement, sh = Math.max((doc && doc.scrollHeight) || 0, (d.body && d.body.scrollHeight) || 0);
        if (!sh) return;
        var p = Math.min(100, Math.round(((w.scrollY || w.pageYOffset || 0) + (w.innerHeight || 0)) / sh * 100));
        if (p > scrollMax) scrollMax = p;
      } catch (e) { /* no layout (a test document) */ }
    }
    var scrollT = 0;
    function onScroll() { // the depth is read at most every 400 ms: no layout read on every scroll frame
      if (scrollT) return;
      scrollT = (w.setTimeout || setTimeout).call(w, function () { scrollT = 0; measure(); }, 400);
    }
    var handlers = [], timer = null;
    function on(target, name, fn, opt) { if (target && target.addEventListener) { target.addEventListener(name, fn, opt); handlers.push([target, name, fn, opt]); } }

    function start() {
      Object.keys(STAGE).forEach(function (name) {
        on(w, name, function (ev) {
          var type = STAGE[name], det = (ev && ev.detail) || {};
          if (type === 'view' && det.source && det.source !== 'user') return; // only the visitor's own turning
          push(type, pick(type, det));
        });
      });
      on(d, 'click', function (ev) {
        var c = clickKind(ev && ev.target);
        if (!c) return;
        push('click', c);
        if (c.k === 'wa' || c.k === 'tel' || c.k === 'mail' || c.k === 'book_send' || c.k === 'send') flush(); // the page may be left at once
      }, true);
      on(d, 'submit', function (ev) {
        var f = ev && ev.target;
        if (!f || String(f.nodeName).toUpperCase() !== 'FORM') return;
        push('form', formKind(f));
        flush();
      }, true);
      on(d, 'formdata', function (ev) {
        var f = ev && ev.target;
        if (!f || !ev.formData || !f.getAttribute) return;
        var act = String(f.getAttribute('action') || '');
        if (/admin-post\.php/i.test(act) || f.hasAttribute('data-nl-visit')) { try { ev.formData.set('nl_visit', vid); } catch (e) { /* read only */ } }
      }, true);
      on(d, 'visibilitychange', function () {
        if (d.visibilityState === 'hidden') { if (visFrom) { visMs += now() - visFrom; visFrom = 0; } leave(); flush(); }
        else if (!visFrom) { visFrom = now(); }
      });
      on(w, 'pagehide', function () { if (visFrom) { visMs += now() - visFrom; visFrom = 0; } leave(); flush(); });
      on(w, 'scroll', onScroll, { passive: true });
      wrapFetch(w, vid);
      push('open', {});
      timer = (deps.setInterval || w.setInterval).call(w, flush, EVERY);
      return api;
    }
    function stop() {
      stopped = true;
      if (timer) (deps.clearInterval || w.clearInterval).call(w, timer);
      handlers.forEach(function (h) { h[0].removeEventListener(h[1], h[2], h[3]); });
      handlers = [];
      if (w.fetch && w.fetch.__nlvt && w.fetch.__nlvtOrig) w.fetch = w.fetch.__nlvtOrig;
    }
    var api = { start: start, stop: stop, flush: flush, push: push, leave: leave,
      get queue() { return queue.slice(); }, get vid() { return vid; }, get pv() { return pv; }, get kept() { return vidInfo.kept; }, vis: vis };
    return api;
  }

  function boot(w) {
    var cfg = w.NL_TRAIL_CFG;
    if (!cfg || !cfg.endpoint || optedOut(w) || robot(w)) return null;
    try { var r = create(w, cfg); r.start(); if (w.NL_TRAIL) w.NL_TRAIL.rec = r; return r; } catch (e) { return null; }
  }

  return { version: VERSION, boot: boot, create: create, optedOut: optedOut, robot: robot, pick: pick, clickKind: clickKind,
    formKind: formKind, visitId: visitId, leadUrl: leadUrl, wrapFetch: wrapFetch, KEY: KEY, TTL: TTL, EVERY: EVERY, MAX_BATCH: MAX_BATCH };
});
