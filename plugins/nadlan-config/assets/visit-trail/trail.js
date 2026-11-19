/*! NadLan visit trail 1.1.0 (HAD-678, Ben 7.11.2026; 1.1.0 HAD-791, 19.11.2026). First-party record of what a visitor picks.
 *
 * 1.1.0: window.nlTrack(name, data) for every tool (contract: docs/research/2026-11-19-buyer-events/CONTRACT.md), the
 * 'nl:track' window event, the designer's 'nadlan:design-order', a mirror of the site's own nadlanGA() events (read from
 * window.dataLayer, nothing wrapped), a number typed into a mortgage calculator (never the number), and on the showroom engine
 * pages a read-only look at window.NadLanEngine.state every 800 ms (engine.js is frozen and untouched). cfg.mode 'lite' (a page
 * that is not a project page): only those tool events, no page-open, no taps, no time on page. The visitor's own opt-out:
 * window.nlTrack.off() or a link to #nl-trail-off (localStorage nl_vt_off = 1).
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
  var VERSION = '1.1.0';
  var OFF_KEY = 'nl_vt_off';     // the visitor's own "do not record me"
  var GA_PREFIX = /^(basket|cockpit|offer|room|tour|journey|showroom|designer|design|call|rfp|mortgage|together|price_alert|nudge)_/;
  var GA_SKIP = { tour_direction: 1, showroom_turn: 1, stage_floor: 1, stage_facing: 1, stage_step: 1, whatsapp_click: 1, deal_floor_click: 1, floor_action: 1, floor_slice: 1 };
  var GA_KEEP = { step: 'k', kind: 'k', tile: 'k', profession: 'k', mode: 'k', items: 'v', floor: 'f', unit: 'u', tower: 'tw' };
  var CALC_SEL = '[data-nl-calc],.nlck,.nlmx-sw,#mortgage-tracks,.nl-mortg,.nmc,.nlpg,[id^="nmc-"]';
  // the mortgage page's own calculators name their fields by prefix (nlmq- the quick one at the top, nlm- the full ones, nlmb- the
  // budget, nmc- the stress test): a field with such an id counts even outside the roots above (found live 19.11.2026)
  var CALC_ID = /^(nmc|nlmq|nlm|nlmb|nlck|nlpg)-/;
  var CALC_MS = 30000;          // one mortgage_check per calculator per 30 s
  var URGENT = { call_book: 1, call_join: 1, rfp_send: 1, basket_add: 1, design_order: 1, offer_sent: 1, basket_send: 1, room_join: 1 };
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

  /** the fields kept from a tool event (window.nlTrack): an allow list, texts cut short; everything else is dropped */
  var NAME_RE = /^[a-z][a-z0-9_.-]{1,39}$/;
  function pickAct(name, d) {
    name = String(name || '').toLowerCase();
    if (!NAME_RE.test(name)) return null;
    d = d && typeof d === 'object' ? d : {};
    var o = { n: name };
    var proj = d.project != null && typeof d.project === 'object' ? (d.project.slug || d.project.id) : d.project;
    if (proj != null && proj !== '') put(o, 'p', str(proj, 60));
    put(o, 'a', str(d.a != null ? d.a : d.action, 24));
    put(o, 'f', int(d.floor != null ? d.floor : d.f, -5, 300));
    var unit = d.unit != null && typeof d.unit === 'object' ? d.unit.id : d.unit;
    put(o, 'u', str(unit, 24));
    put(o, 'tw', str(d.tower, 16));
    put(o, 'b', bearing(d.bearing));
    put(o, 'dir', str(d.dir || d.facing, 24));
    put(o, 'rooms', int(d.rooms, 0, 20));
    put(o, 'k', str(d.k != null ? d.k : d.kind, 24));
    put(o, 'v', int(d.v != null ? d.v : d.items, 0, 100000));
    put(o, 'src', str(d.source, 12));
    var to = str(d.to, 2).toLowerCase();
    if (/^(he|en|fr|ru|ar)$/.test(to)) o.to = to;
    return o;
  }

  /* ---------------------------------------------------------------- opt-out and robots */
  function optedOut(w) {
    var n = (w && w.navigator) || {};
    try { if (w && w.localStorage && w.localStorage.getItem(OFF_KEY) === '1') return true; } catch (e) { /* no storage */ }
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
    var lite = cfg.mode === 'lite';
    function payload(evs) {
      var o = { v: 1, vid: vid, pv: pv, seq: seq++, page: Number(cfg.page) || 0, mode: lite ? 'lite' : 'full', proj: Number(cfg.proj) || 0,
        path: str((w.location && w.location.pathname) || '/', 191),
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
      if (lite) return;
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
    var handlers = [], timer = null, timer2 = null;

    /* ---- 1.1.0: one tool event; returns true when it was queued */
    function track(name, data) {
      var o = pickAct(name, data);
      if (!o) return false;
      var ok = push('act', o);
      if (ok && URGENT[o.n]) flush(); // the buyer may leave right after asking
      return ok;
    }

    /* ---- the site's own nadlanGA() events, read from window.dataLayer (nothing is wrapped) */
    var dlSeen = 0;
    function readDataLayer() {
      var dl = w.dataLayer;
      if (!dl || typeof dl.length !== 'number') return;
      if (dlSeen > dl.length) dlSeen = 0;
      for (; dlSeen < dl.length; dlSeen++) {
        var e = dl[dlSeen];
        if (!e || typeof e !== 'object' || typeof e.event !== 'string') continue;
        var n = e.event.toLowerCase();
        if (!GA_PREFIX.test(n) || GA_SKIP[n]) continue;
        var data = {};
        for (var k in GA_KEEP) if (Object.prototype.hasOwnProperty.call(GA_KEEP, k) && e[k] != null && typeof e[k] !== 'object') {
          var to = GA_KEEP[k];
          data[to === 'k' ? 'k' : (to === 'v' ? 'v' : (to === 'f' ? 'floor' : (to === 'u' ? 'unit' : 'tower')))] = e[k];
        }
        data.source = 'ga';
        track(n, data);
      }
    }

    /* ---- the showroom engine (Rainbow, Ashira, DUO, H Infinity): a read-only look at its public state */
    var eng = { tries: 0, unit: undefined, tool: null, favs: -1, lang: '', key: '' };
    var TOOL = { plan: 'plan_open', view: 'view_open', tour: 'tour_open', studio: 'designer_open', area: 'area_open', contact: 'contact_open', compare: 'compare_open' };
    function engineUnit(SR, key, id) {
      try {
        var list = (SR.projects[key] && SR.projects[key].units) || [];
        for (var i = 0; i < list.length; i++) if (list[i] && list[i].id === id) return list[i];
      } catch (e) { /* data not there */ }
      return null;
    }
    function watchEngine() {
      var E = w.NadLanEngine, SR = w.NADLAN_SHOWROOM;
      if (!E || !E.state || !SR || !SR.projects) { eng.tries++; return; }
      var st = E.state, key = String(st.projectKey || ''), P = SR.projects[key] || {};
      var base = { project: P.wp_id || key, source: 'engine' };
      var u = st.unitId || null;
      if (eng.unit === undefined) { eng.unit = u; eng.favs = (st.favs || []).length; eng.lang = st.lang; eng.key = key; return; } // the page's own start: not a choice
      if (u && u !== eng.unit) {
        var ud = engineUnit(SR, key, u) || {};
        track('unit_open', { project: base.project, unit: u, floor: ud.floor, rooms: ud.rooms, dir: ud.dir, source: 'engine' });
      }
      eng.unit = u;
      var tool = st.tool || null;
      if (tool && tool !== eng.tool && TOOL[tool]) {
        var tu = engineUnit(SR, key, u) || {};
        track(TOOL[tool], { project: base.project, unit: u, floor: tu.floor, dir: tu.dir, source: 'engine' });
      }
      eng.tool = tool;
      var fv = (st.favs || []).length;
      if (eng.favs >= 0 && fv > eng.favs) track('favorite', { project: base.project, unit: u, source: 'engine' });
      eng.favs = fv;
      if (st.lang && eng.lang && st.lang !== eng.lang) track('lang_switch', { project: base.project, to: st.lang, source: 'engine' });
      eng.lang = st.lang;
    }

    /* ---- a number typed into a mortgage calculator: "checked the monthly payment" (the number itself is never read) */
    var calcAt = {};
    function onCalcInput(ev) {
      if (!ev || ev.isTrusted === false) return;
      var t = ev.target;
      if (!t || !t.closest || String(t.nodeName).toUpperCase() !== 'INPUT') return;
      var ty = String(t.type || '').toLowerCase();
      if (ty !== 'number' && ty !== 'range' && !(ty === 'text' && /numeric|decimal/.test(String(t.inputMode || t.getAttribute('inputmode') || '')))) return;
      var root = null;
      try { root = t.closest(CALC_SEL); } catch (e) { root = null; }
      var idm = CALC_ID.exec(String(t.id || ''));
      if (!root && !idm) return;
      var key = str((root && root.getAttribute('data-nl-calc')) || (idm ? idm[1] : '') || (root && root.id) || String((root && root.className) || '').split(/\s+/)[0] || 'calc', 24);
      var at = now();
      if (calcAt[key] && at - calcAt[key] < CALC_MS) return;
      calcAt[key] = at;
      track('mortgage_check', { k: key });
    }

    /* ---- a tap on another language of the same page */
    function onLangTap(el) {
      var a = el && el.closest ? el.closest('a[hreflang],[data-nl-lang]') : null;
      if (!a) return;
      var to = str(a.getAttribute('data-nl-lang') || a.getAttribute('hreflang') || '', 2).toLowerCase();
      var cur = String(cfg.lang || '').slice(0, 2);
      if (/^(he|en|fr|ru|ar)$/.test(to) && to !== cur) track('lang_switch', { to: to });
    }
    function on(target, name, fn, opt) { if (target && target.addEventListener) { target.addEventListener(name, fn, opt); handlers.push([target, name, fn, opt]); } }

    function start() {
      // 1.1.0: the tools' events, on every page
      on(w, 'nl:track', function (ev) { var d = (ev && ev.detail) || {}; track(d.name, d.data); });
      on(w, 'nadlan:design-order', function (ev) {
        var d = (ev && ev.detail) || {};
        track('design_order', { project: d.project && d.project.slug, unit: d.unit && d.unit.id, rooms: d.unit && d.unit.rooms, source: str(d.source, 12) });
      });
      on(d, 'change', onCalcInput, true);
      on(d, 'input', onCalcInput, true);
      if (!lite) Object.keys(STAGE).forEach(function (name) {
        on(w, name, function (ev) {
          var type = STAGE[name], det = (ev && ev.detail) || {};
          if (type === 'view' && det.source && det.source !== 'user') return; // only the visitor's own turning
          push(type, pick(type, det));
        });
      });
      on(d, 'click', function (ev) {
        var tg = ev && ev.target;
        var off = tg && tg.closest ? tg.closest('a[href$="#nl-trail-off"],[data-nl-trail-off]') : null;
        if (off) { optOut(); return; }
        onLangTap(tg);
        if (lite) return; // a page that is not a project page: no taps are recorded
        var c = clickKind(tg);
        if (!c) return;
        push('click', c);
        if (c.k === 'wa' || c.k === 'tel' || c.k === 'mail' || c.k === 'book_send' || c.k === 'send') flush(); // the page may be left at once
      }, true);
      on(d, 'submit', function (ev) {
        if (lite) return;
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
      if (!lite) on(w, 'scroll', onScroll, { passive: true });
      wrapFetch(w, vid);
      if (!lite) push('open', {});
      // the calls a tool made before this file ran (the queue printed with the page)
      var q = w.nlTrackQ;
      if (q && q.length) { for (var i = 0; i < q.length && i < 100; i++) { try { track(q[i][0], q[i][1]); } catch (e) { /* one bad call */ } } }
      w.nlTrackQ = [];
      readDataLayer();
      timer = (deps.setInterval || w.setInterval).call(w, flush, EVERY);
      timer2 = (deps.setInterval || w.setInterval).call(w, function () {
        if (d && d.visibilityState === 'hidden') return;
        readDataLayer();
        if (eng.tries < 75) watchEngine(); // the engine is looked for during the first minute; once found it is watched while the page lives
      }, 800);
      return api;
    }
    function optOut() {
      try { w.localStorage.setItem(OFF_KEY, '1'); } catch (e) { /* no storage: this page only */ }
      queue.length = 0;
      stop();
    }
    function stop() {
      stopped = true;
      if (timer) (deps.clearInterval || w.clearInterval).call(w, timer);
      if (timer2) (deps.clearInterval || w.clearInterval).call(w, timer2);
      handlers.forEach(function (h) { h[0].removeEventListener(h[1], h[2], h[3]); });
      handlers = [];
      if (w.fetch && w.fetch.__nlvt && w.fetch.__nlvtOrig) w.fetch = w.fetch.__nlvtOrig;
    }
    var api = { start: start, stop: stop, flush: flush, push: push, leave: leave, track: track, optOut: optOut, watchEngine: watchEngine, readDataLayer: readDataLayer,
      get queue() { return queue.slice(); }, get vid() { return vid; }, get pv() { return pv; }, get kept() { return vidInfo.kept; }, vis: vis };
    return api;
  }

  /** window.nlTrack(name, data): the one call every tool makes; a no-op when nothing may be recorded, never a throw */
  function publish(w, r) {
    var f = function (name, data) { try { return r ? r.track(name, data) : false; } catch (e) { return false; } };
    f.off = function () { if (r) r.optOut(); else { try { w.localStorage.setItem(OFF_KEY, '1'); } catch (e) { /* none */ } } };
    f.version = VERSION;
    w.nlTrack = f;
    return f;
  }
  function boot(w) {
    var cfg = w.NL_TRAIL_CFG;
    if (!cfg || !cfg.endpoint || optedOut(w) || robot(w)) { publish(w, null); w.nlTrackQ = []; return null; }
    try { var r = create(w, cfg); r.start(); publish(w, r); if (w.NL_TRAIL) w.NL_TRAIL.rec = r; return r; } catch (e) { publish(w, null); return null; }
  }

  return { version: VERSION, boot: boot, create: create, optedOut: optedOut, robot: robot, pick: pick, pickAct: pickAct, publish: publish, clickKind: clickKind,
    formKind: formKind, visitId: visitId, leadUrl: leadUrl, wrapFetch: wrapFetch, KEY: KEY, TTL: TTL, EVERY: EVERY, MAX_BATCH: MAX_BATCH };
});
