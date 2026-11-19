/* visit trail build (7.11.2026, HAD-678) · node unit test of plugins/nadlan-config/assets/visit-trail/trail.js, on a fake window
   (EventTarget, a fake clock and a fake beacon): the opt-out (Global Privacy Control, Do Not Track, robots: nothing runs, nothing is
   stored, fetch is not wrapped), the visit id (random, kept 30 days from its creation, then new), the batching (40 a request, the
   20 s timer, nothing sent when nothing happened, the same event twice in 1.5 s is one, the view at most every 8 s, 400 a page view),
   the stage events (only the allowed fields: no DOM element, no picture address), the leave record (time in view, scroll depth),
   the lead link (the X-NL-Visit header only on same-origin POSTs to /wp-json/nadlan/v1/*, never on /trail, never on a Request object,
   other headers kept; nl_visit only on admin-post.php forms), no keystrokes and no form values.
   Run:  node docs/research/2026-11-07-campaign-network/build/build-visit-trail/test_trail.js     (exit 1 on any failure) */
'use strict';
var path = require('path'), fs = require('fs');
var REPO = path.resolve(__dirname, '../../../..');
var FILE = path.join(REPO, 'plugins/nadlan-config/assets/visit-trail/trail.js');
var T = require(FILE), SRC = fs.readFileSync(FILE, 'utf8');
var fails = 0, n = 0;
function ok(cond, name, got) { n++; if (!cond) fails++; console.log((cond ? '  ok   ' : '  FAIL ') + name + (got !== undefined ? '  [' + (typeof got === 'string' ? got : JSON.stringify(got)) + ']' : '')); }

function env(o) {
  o = o || {};
  var w = new EventTarget(), d = new EventTarget(), store = {}, calls = [], timers = [];
  d.visibilityState = 'visible';
  d.referrer = o.referrer === undefined ? 'https://www.google.co.il/search?q=rainbow' : o.referrer;
  d.documentElement = { lang: 'he', scrollHeight: 4000 };
  d.body = { scrollHeight: 4000 };
  w.document = d;
  w.location = new URL(o.href || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?utm_source=x');
  w.navigator = Object.assign({ userAgent: 'Mozilla/5.0 (Linux; Android 14) Chrome/130 Mobile', webdriver: false }, o.nav || {});
  w.innerWidth = o.width || 390; w.innerHeight = 800; w.scrollY = 0;
  if (!o.noStorage) w.localStorage = { getItem: function (k) { return k in store ? store[k] : null; }, setItem: function (k, v) { store[k] = String(v); }, removeItem: function (k) { delete store[k]; } };
  w.crypto = globalThis.crypto; w.URL = URL; w.Headers = Headers; w.Request = Request; w.Blob = Blob;
  w.fetch = function (input, init) { calls.push({ input: input, init: init, self: this }); return Promise.resolve({ ok: true }); };
  w.setInterval = function (fn, ms) { timers.push({ fn: fn, ms: ms }); return timers.length; };
  w.clearInterval = function () {};
  w.setTimeout = function (fn) { fn(); return 1; };
  w._store = store; w._calls = calls; w._timers = timers;
  return w;
}
function clock(t) { var c = { t: t || 1762500000000 }; c.now = function () { return c.t; }; return c; }
function rec(w, c, cfg) {
  var sent = [];
  var r = T.create(w, cfg || { endpoint: '/wp-json/nadlan/v1/trail', page: 7001, lang: 'he' }, {
    now: c.now, send: function (url, body) { sent.push({ url: url, body: JSON.parse(body), raw: body }); return true; },
    setInterval: w.setInterval, clearInterval: w.clearInterval });
  r.sent = sent;
  return r;
}
function fire(w, name, detail) { w.dispatchEvent(new CustomEvent(name, { detail: detail })); }
function evAt(target, type, props) { var e = new Event(type); Object.keys(props || {}).forEach(function (k) { Object.defineProperty(e, k, { value: props[k] }); }); target.dispatchEvent(e); return e; }
function allEv(r) { var a = []; r.sent.forEach(function (s) { a = a.concat(s.body.ev); }); return a; }

console.log('1. opt-out: Global Privacy Control, Do Not Track, robots');
ok(T.optedOut({ navigator: { globalPrivacyControl: true } }) === true, 'GPC true opts out');
ok(T.optedOut({ navigator: { doNotTrack: '1' } }) === true, 'DNT "1" opts out');
ok(T.optedOut({ navigator: { doNotTrack: 'yes' } }) === true, 'DNT "yes" (old Firefox) opts out');
ok(T.optedOut({ navigator: {}, doNotTrack: '1' }) === true, 'window.doNotTrack "1" (old IE / Safari) opts out');
ok(T.optedOut({ navigator: { msDoNotTrack: '1' } }) === true, 'msDoNotTrack "1" opts out');
ok(T.optedOut({ navigator: { doNotTrack: '0', globalPrivacyControl: false } }) === false, 'DNT "0" and GPC false record');
ok(T.optedOut({ navigator: { doNotTrack: 'unspecified' } }) === false, 'DNT unspecified records');
ok(T.robot({ navigator: { webdriver: true, userAgent: 'Mozilla/5.0' } }) === true, 'navigator.webdriver is a robot');
ok(T.robot({ navigator: { userAgent: 'Mozilla/5.0 (compatible; Googlebot/2.1)' } }) === true, 'Googlebot is a robot');
ok(T.robot({ navigator: { userAgent: 'Mozilla/5.0 HeadlessChrome/130' } }) === true, 'HeadlessChrome is a robot');
ok(T.robot({ navigator: { userAgent: 'Mozilla/5.0 (iPhone) Safari/605' } }) === false, 'an iPhone is not');
['gpc', 'dnt', 'robot'].forEach(function (k) {
  var w = env({ nav: k === 'gpc' ? { globalPrivacyControl: true } : (k === 'dnt' ? { doNotTrack: '1' } : { webdriver: true }) });
  var f0 = w.fetch;
  w.NL_TRAIL_CFG = { endpoint: '/wp-json/nadlan/v1/trail', page: 1, lang: 'he' };
  var r = T.boot(w);
  fire(w, 'nl:floor', { floor: 23 });
  ok(r === null && Object.keys(w._store).length === 0 && w.fetch === f0 && w._timers.length === 0, k + ': boot returns null, nothing stored, fetch untouched, no timer');
});
(function () {
  var w = env(); w.NL_TRAIL_CFG = { endpoint: '/x', page: 1 };
  var r = T.boot(w);
  ok(r && typeof r.flush === 'function' && w._timers.length === 2 && w._timers[0].ms === 20000 && w._timers[1].ms === 800, 'a normal browser boots: the 20 s batch timer and the 800 ms watcher (1.1.0)', w._timers.map(function (t) { return t.ms; }));
  r.stop();
  ok(!w.fetch.__nlvt, 'stop() gives fetch back');
  var w2 = env(); ok(T.boot(w2) === null, 'no NL_TRAIL_CFG: nothing runs');
})();

console.log('2. the visit id: random, 30 days from its creation, then new');
(function () {
  var w = env(), c = clock();
  var a = T.visitId(w, c.t), b = T.visitId(w, c.t + 5 * 86400000), x = T.visitId(w, c.t + 31 * 86400000);
  ok(/^[A-Za-z0-9_-]{22}$/.test(a.id) && a.kept, 'a 22-character id, kept in localStorage', a.id);
  ok(b.id === a.id, 'the same id 5 days later');
  ok(x.id !== a.id && /^[A-Za-z0-9_-]{22}$/.test(x.id), 'a new id after 30 days');
  ok(JSON.parse(w._store[T.KEY]).at === c.t + 31 * 86400000, 'the new id is stamped with its own creation time (not rolled forward)');
  var ids = {}; for (var i = 0; i < 200; i++) ids[T.visitId(env(), c.t).id] = 1;
  ok(Object.keys(ids).length === 200, '200 fresh browsers, 200 different ids');
  w._store[T.KEY] = '{broken';
  ok(/^[A-Za-z0-9_-]{22}$/.test(T.visitId(w, c.t).id), 'a broken stored value is replaced');
  w._store[T.KEY] = JSON.stringify({ id: 'bad id!', at: c.t });
  ok(T.visitId(w, c.t).id !== 'bad id!', 'a stored value that is not an id is replaced');
  w._store[T.KEY] = JSON.stringify({ id: 'AAAAAAAAAAAAAAAAAAAAAA', at: c.t + 86400000 * 3 });
  ok(T.visitId(w, c.t).id !== 'AAAAAAAAAAAAAAAAAAAAAA', 'a value stamped in the future is replaced');
  var ns = T.visitId(env({ noStorage: true }), c.t);
  ok(ns.kept === false && /^[A-Za-z0-9_-]{22}$/.test(ns.id), 'no storage: an id for this page only');
  var wt = env(); wt.localStorage = { getItem: function () { throw new Error('denied'); }, setItem: function () { throw new Error('denied'); } };
  ok(/^[A-Za-z0-9_-]{22}$/.test(T.visitId(wt, c.t).id), 'storage that throws (private mode): still an id');
  var s = SRC.replace(/\/\*[\s\S]*?\*\//g, '');
  ok(!/document\.cookie/.test(s), 'no cookie is written (localStorage only)');
})();

console.log('3. batching: 40 a request, the 20 s timer, nothing when nothing happened');
(function () {
  var w = env(), c = clock(), r = rec(w, c);
  r.start();
  ok(r.queue.length === 1 && r.queue[0].t === 'open', 'the page view opens with one "open" event');
  w._timers[0].fn();
  ok(r.sent.length === 1 && r.sent[0].url === '/wp-json/nadlan/v1/trail', 'the timer sends the queue', r.sent.length);
  var b = r.sent[0].body;
  ok(b.v === 1 && b.vid === r.vid && b.pv === r.pv && b.seq === 0 && b.page === 7001 && b.lang === 'he' && b.dev === 'm', 'the frame: v, vid, pv, seq 0, page, lang, device class', { seq: b.seq, dev: b.dev });
  ok(b.path === '/projects/rainbow-tel-aviv/', 'the path without the query string', b.path);
  ok(b.ref === 'google.co.il', 'the referring site by name only (no path, no query)', b.ref);
  w._timers[0].fn();
  ok(r.sent.length === 1, 'an empty queue sends nothing');
  for (var i = 1; i <= 45; i++) { c.t += 2000; fire(w, 'nl:floor', { floor: i, heightM: i * 3.1, source: 'user' }); }
  r.flush();
  ok(r.sent.length === 3 && r.sent[1].body.ev.length === 40 && r.sent[2].body.ev.length === 5, '45 events: one request of 40, one of 5', r.sent.slice(1).map(function (s) { return s.body.ev.length; }));
  ok(r.sent[1].body.seq === 1 && r.sent[2].body.seq === 2 && !('ref' in r.sent[1].body), 'seq counts up; the referrer rides the first request only');
  ok(r.sent.every(function (s) { return s.raw.length < 16384; }), 'every request under the server limit of 16 KB', Math.max.apply(null, r.sent.map(function (s) { return s.raw.length; })));
  r.stop();
})();
(function () {
  var w = env(), c = clock(), r = rec(w, c);
  r.start();
  fire(w, 'nl:floor', { floor: 23 }); c.t += 500; fire(w, 'nl:floor', { floor: 23 });
  ok(r.queue.filter(function (e) { return e.t === 'floor'; }).length === 1, 'the same floor twice inside 1.5 s is one event');
  c.t += 2000; fire(w, 'nl:floor', { floor: 23 });
  ok(r.queue.filter(function (e) { return e.t === 'floor'; }).length === 2, 'again after 1.5 s: recorded');
  fire(w, 'nl:view', { mode: 'view', bearing: 270, vert: 0, source: 'user' }); c.t += 3000;
  fire(w, 'nl:view', { mode: 'view', bearing: 280, vert: 0, source: 'user' }); c.t += 6000;
  fire(w, 'nl:view', { mode: 'view', bearing: 290, vert: 0, source: 'user' });
  ok(r.queue.filter(function (e) { return e.t === 'view'; }).map(function (e) { return e.b; }).join() === '270,290', 'turning the view: at most one record per 8 s', r.queue.filter(function (e) { return e.t === 'view'; }).map(function (e) { return e.b; }));
  fire(w, 'nl:view', { bearing: 10, source: 'together' }); c.t += 9000; fire(w, 'nl:view', { bearing: 10, source: 'room' });
  ok(r.queue.filter(function (e) { return e.t === 'view'; }).length === 2, 'a view set from outside (not source user) is not recorded');
  r.stop();
  var w2 = env(), r2 = rec(w2, clock());
  r2.start();
  for (var i = 0; i < 600; i++) { r2.push('click', { k: 'cta', l: 'x' + i }); }
  ok(r2.queue.length === 400, 'a page view records at most 400 events', r2.queue.length);
  r2.stop();
})();

console.log('4. the stage events: only the allowed fields');
(function () {
  var w = env(), c = clock(), r = rec(w, c);
  r.start();
  var dom = { nodeName: 'BUTTON', secret: 'x' };
  fire(w, 'nl:floor', { floor: 23, heightM: 74.2, tower: 'A', towerName: 'מגדל A', source: 'user' }); c.t += 2000;
  fire(w, 'nl:facing', { floor: 23, heightM: 74.2, bearing: 268.4, unit: '23-w', toward: null, tower: 'A', label: 'דירה 23 מערב', source: 'user' }); c.t += 2000;
  fire(w, 'nl:facing', { floor: 12, bearing: -90, facing: 'מערב' }); c.t += 2000;
  fire(w, 'nl:quarter', { kind: 'school', name: 'בית ספר הדר', id: 'q1' }); c.t += 2000;
  fire(w, 'nl:facility', { id: 'pool', name: 'בריכה' }); c.t += 2000;
  fire(w, 'nl:facility-tour', { id: 'pool', src: 'https://nad-lan.co.il/x/tour/pool.jpg', small: 'https://x/s.jpg', title: 'בריכה', note: 'n', opener: dom }); c.t += 2000;
  fire(w, 'nl:floor-cta', { floor: 23, bearing: 268, tower: 'A' }); c.t += 2000;
  fire(w, 'nl:floor-action', { action: 'inside', floor: 23, heightM: 74, bearing: 268, unit: '23-w', tower: 'A' }); c.t += 2000;
  fire(w, 'nl:tour', { open: true, scene: 'living' }); c.t += 2000;
  fire(w, 'nl:tour', { open: false }); c.t += 2000;
  fire(w, 'nl:example', { open: true, id: 'B4', tower: 'B', floor: 18, sceneFloor: 18, facing: 'צפון', bearing: 5, time: 'noon' }); c.t += 2000;
  var q = r.queue, by = function (t) { return q.filter(function (e) { return e.t === t; }); };
  var str = function (o) { var c2 = Object.assign({}, o); delete c2.at; return JSON.stringify(c2); };
  ok(str(by('floor')[0]) === JSON.stringify({ t: 'floor', f: 23, tw: 'A', src: 'user' }), 'nl:floor -> floor {f, tw, src} (no height, no tower name)', str(by('floor')[0]));
  ok(str(by('facing')[0]) === JSON.stringify({ t: 'facing', f: 23, b: 268, u: '23-w', tw: 'A', lbl: 'דירה 23 מערב', src: 'user' }), 'nl:facing -> facing {f, b rounded, u, tw, lbl, src}', str(by('facing')[0]));
  ok(by('facing')[1].b === 270 && by('facing')[1].dir === 'מערב', 'a bearing of -90 is 270; the world\'s direction word is kept', by('facing')[1]);
  ok(str(by('quarter')[0]) === JSON.stringify({ t: 'quarter', k: 'school', n: 'בית ספר הדר' }), 'nl:quarter -> {k, n}');
  ok(str(by('facility')[0]) === JSON.stringify({ t: 'facility', n: 'בריכה', id: 'pool' }), 'nl:facility -> {n, id}');
  ok(str(by('ftour')[0]) === JSON.stringify({ t: 'ftour', id: 'pool', n: 'בריכה' }), 'nl:facility-tour -> {id, n}: no picture address, no DOM element');
  ok(str(by('fcta')[0]) === JSON.stringify({ t: 'fcta', f: 23, b: 268, tw: 'A' }), 'nl:floor-cta -> {f, b, tw}');
  ok(str(by('faction')[0]) === JSON.stringify({ t: 'faction', a: 'inside', f: 23, u: '23-w', tw: 'A' }), 'nl:floor-action -> {a, f, u, tw}');
  ok(str(by('tour')[0]) === JSON.stringify({ t: 'tour', o: 1, s: 'living' }) && str(by('tour')[1]) === JSON.stringify({ t: 'tour', o: 0 }), 'nl:tour open / close');
  ok(str(by('example')[0]) === JSON.stringify({ t: 'example', o: 1, id: 'B4', f: 18, tw: 'B', dir: 'צפון' }), 'nl:example -> {o, id, f, tw, dir}', str(by('example')[0]));
  ok(q.every(function (e) { return JSON.stringify(e).indexOf('http') === -1 && JSON.stringify(e).indexOf('secret') === -1; }), 'no address and no DOM element in any event');
  fire(w, 'nl:floor', { floor: 'abc' }); c.t += 2000; fire(w, 'nl:floor', { floor: 9999 }); c.t += 2000;
  ok(by('floor').length === 1 && q.filter(function (e) { return e.t === 'floor'; }).slice(1).every(function (e) { return !('f' in e); }), 'a floor that is not a number or off the range is dropped from the event');
  var long = new Array(200).join('א');
  fire(w, 'nl:quarter', { kind: 'k', name: long }); c.t += 2000;
  ok(r.queue[r.queue.length - 1].n.length === 60, 'a long name is cut at 60 characters');
  fire(w, 'nl:quarter', { kind: 'k', name: 'line\nbreak\u0000ctl  spaces' });
  ok(r.queue[r.queue.length - 1].n === 'line break ctl spaces', 'control characters and runs of spaces are folded', r.queue[r.queue.length - 1].n);
  r.stop();
})();

console.log('5. time on the page, the leave record');
(function () {
  var w = env(), c = clock(), r = rec(w, c);
  r.start();
  c.t += 30000;
  w.document.visibilityState = 'hidden'; evAt(w.document, 'visibilitychange');
  ok(r.sent.length === 1, 'hidden: the queue is sent');
  var lv = allEv(r).filter(function (e) { return e.t === 'leave'; });
  ok(lv.length === 1 && lv[0].vis === 30000, 'a leave record with 30 s in view', lv[0]);
  c.t += 600000; // ten minutes in another tab: not counted
  w.document.visibilityState = 'visible'; evAt(w.document, 'visibilitychange');
  c.t += 15000;
  w.scrollY = 2200;
  evAt(w, 'scroll');
  evAt(w, 'pagehide');
  var lv2 = allEv(r).filter(function (e) { return e.t === 'leave'; });
  ok(lv2.length === 2 && lv2[1].vis === 45000, 'pagehide: 45 s in view (the 10 minutes away are not counted)', lv2.map(function (e) { return e.vis; }));
  ok(lv2[1].sc === 75, 'scrolled to 75% of the page ((2200 + 800) / 4000)', lv2[1].sc);
  evAt(w, 'pagehide');
  ok(allEv(r).filter(function (e) { return e.t === 'leave'; }).length === 2, 'a second pagehide at the same time adds no second leave');
  r.stop();
})();

console.log('6. the lead link: the visit id rides the page\'s own lead requests');
(function () {
  var w = env();
  ok(T.leadUrl(w, '/wp-json/nadlan/v1/lead') === true, '/wp-json/nadlan/v1/lead');
  ok(T.leadUrl(w, 'https://nad-lan.co.il/wp-json/nadlan/v1/appt-book') === true, 'the booking route');
  ok(T.leadUrl(w, '/?rest_route=/nadlan/v1/lead') === true, '?rest_route=/nadlan/v1/lead');
  ok(T.leadUrl(w, '/wp-admin/admin-post.php') === true, 'admin-post.php');
  ok(T.leadUrl(w, '/wp-json/nadlan/v1/trail') === false && T.leadUrl(w, '/?rest_route=/nadlan/v1/trail') === false, 'never the trail route itself');
  ok(T.leadUrl(w, 'https://api.mapbox.com/wp-json/nadlan/v1/lead') === false, 'never another site');
  ok(T.leadUrl(w, '/wp-json/wp/v2/posts') === false, 'not other REST routes');
  var c = clock(), r = rec(w, c);
  r.start();
  var calls = w._calls;
  w.fetch('/wp-json/nadlan/v1/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{"name":"x"}' });
  var h = calls[0].init.headers;
  ok(h instanceof Headers && h.get('X-NL-Visit') === r.vid && h.get('Content-Type') === 'application/json', 'a lead POST carries X-NL-Visit, its own Content-Type kept', h && h.get && h.get('X-NL-Visit'));
  ok(calls[0].init.body === '{"name":"x"}' && calls[0].self === w, 'the body is untouched; fetch is called on window');
  w.fetch('/wp-json/nadlan/v1/appt-slots?card=1');
  ok(calls[1].init === undefined, 'a GET goes out exactly as it came (no init added)');
  w.fetch('https://api.mapbox.com/x', { method: 'POST', body: 'b' });
  ok(!(calls[2].init.headers), 'another site: no header');
  var rq = new Request('https://nad-lan.co.il/wp-json/nadlan/v1/lead', { method: 'POST', body: 'x' });
  w.fetch(rq);
  ok(calls[3].input === rq && calls[3].init === undefined, 'a Request object goes out untouched');
  w.fetch('/wp-json/nadlan/v1/lead', { method: 'POST', headers: [['X-NL-Visit', 'other-visit-id-0000000']] });
  ok(calls[4].init.headers.get('X-NL-Visit') === 'other-visit-id-0000000', 'a header already set is kept');
  var f1 = w.fetch; T.wrapFetch(w, 'zzz'); ok(w.fetch === f1, 'wrapping twice is a no-op');
  r.stop();
  ok(w.fetch === w.fetch && !w.fetch.__nlvt, 'stop() restores the original fetch');
  // forms: nl_visit only on admin-post.php forms (or a form that asks for it)
  var w2 = env(), r2 = rec(w2, clock());
  r2.start();
  var mk = function (action, extra) { return Object.assign({ nodeName: 'FORM', id: 'f1', className: 'nl-form x', getAttribute: function (k) { return k === 'action' ? action : null; }, hasAttribute: function (k) { return !!(extra && extra[k]); }, closest: function () { return null; } }, extra || {}); };
  var fd = new FormData(); fd.set('lead_phone', '0501234567');
  evAt(w2.document, 'formdata', { target: mk('https://nad-lan.co.il/wp-admin/admin-post.php'), formData: fd });
  ok(fd.get('nl_visit') === r2.vid, 'a form posted to admin-post.php gets nl_visit');
  var fd2 = new FormData();
  evAt(w2.document, 'formdata', { target: mk('/wp-json/nadlan/v1/my-availability'), formData: fd2 });
  ok(fd2.get('nl_visit') === null, 'any other form gets nothing (a script that reads its FormData sees no extra field)');
  var fd3 = new FormData();
  evAt(w2.document, 'formdata', { target: mk('', { 'data-nl-visit': true }), formData: fd3 });
  ok(fd3.get('nl_visit') === r2.vid, 'a form marked data-nl-visit gets it');
  // the submit: the form's kind and id only, never a value
  evAt(w2.document, 'submit', { target: mk('/wp-admin/admin-post.php', { lead_phone: { value: '0501234567' }, elements: [{ name: 'lead_phone', value: '0501234567' }] }) });
  var fe = allEv(r2).filter(function (e) { return e.t === 'form'; });
  ok(fe.length === 1 && fe[0].k === 'lead' && fe[0].id === 'f1' && Object.keys(fe[0]).sort().join() === 'at,id,k,t', 'submit: {k: lead, id} and it is sent at once', fe[0]);
  ok(r2.sent.every(function (s) { return s.raw.indexOf('0501234567') === -1; }), 'the phone typed in the form is in no request');
  r2.stop();
})();

console.log('7. no keystrokes, no mouse paths, no field values');
(function () {
  var w = env(), c = clock(), r = rec(w, c);
  r.start();
  var before = r.queue.length;
  ['keydown', 'keyup', 'keypress', 'input', 'change', 'mousemove', 'pointermove', 'touchmove', 'focusin', 'copy', 'paste'].forEach(function (t) { evAt(w.document, t, { target: { value: 'secret 0501234567' } }); evAt(w, t); });
  ok(r.queue.length === before, 'eleven input and pointer events: nothing recorded', r.queue.length - before);
  var s = SRC.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  ok(!/addEventListener\(['"](key|input|change|mouse|pointer|touch)/.test(s) && !/on\([^,]+,\s*'(key\w*|mouse\w*|pointer\w*|touch\w*)'/.test(s), 'the file listens to no key, mouse, pointer or touch event');
  ok((s.match(/on\([^,]+,\s*'(input|change)'/g) || []).length === 2 && /on\(d, 'change', onCalcInput, true\)/.test(s) && /on\(d, 'input', onCalcInput, true\)/.test(s), '1.1.0: input and change are heard only by the calculator watcher');
  var calcFn = s.slice(s.indexOf('function onCalcInput'), s.indexOf('function onLangTap'));
  ok(calcFn.length > 100 && !/\.value\b/.test(calcFn) && !/valueAsNumber/.test(calcFn), '1.1.0: the calculator watcher never reads what was typed');
  ok(!/\.value\b/.test(s), 'the file never reads a .value');
  ok(!/innerHTML|outerHTML/.test(s), 'the file never reads page markup');
  ok(/'text\/plain;charset=UTF-8'/.test(s) && /sendBeacon/.test(s), 'sent with navigator.sendBeacon as text/plain (no preflight)');
  r.stop();
})();

console.log('8. formKind and the copy rules');
(function () {
  var mk = function (action, id, cls, inSch) { return { id: id || '', className: cls || '', getAttribute: function (k) { return k === 'action' ? action : null; }, closest: function (q) { return inSch && q === '#nlsch' ? {} : null; } }; };
  ok(JSON.stringify(T.formKind(mk('/wp-admin/admin-post.php', 'lead-form'))) === '{"k":"lead","id":"lead-form"}', 'admin-post.php form = lead');
  ok(T.formKind(mk('', '', 'nlsch-form', true)).k === 'book', 'a form inside the booking band = book');
  ok(JSON.stringify(T.formKind(mk('/search', '', 'nl-search big'))) === '{"k":"form","id":"nl-search"}', 'another form: its first class as the id');
  ok(!/[–—]/.test(SRC), 'no long dash in the file');
  ok(T.version === '1.1.0' && /NadLan visit trail 1\.1\.0/.test(SRC), 'version 1.1.0');
  ok(T.MAX_BATCH <= 60 && T.EVERY === 20000 && T.TTL === 30 * 86400000, 'limits: batch under the server cap of 60, 20 s, 30 days');
})();


console.log('9. 1.1.0: window.nlTrack, the nl:track event, the queue, lite mode, the GA mirror, the engine, the calculator, the opt-out');
(function () {
  var a = T.pickAct('basket_add', { project: 'ashira', unit: { id: 'E-4A' }, floor: 4, name: 'Dana', phone: '0501234567', note: 'secret', price: 3000000 });
  ok(a && a.n === 'basket_add' && a.p === 'ashira' && a.u === 'E-4A' && a.f === 4 && !('name' in a) && JSON.stringify(a).indexOf('0501234567') < 0 && JSON.stringify(a).indexOf('secret') < 0 && JSON.stringify(a).indexOf('3000000') < 0, 'pickAct keeps the allow list, drops a name, phone, note and typed price', a);
  ok(T.pickAct('Bad Name!', {}) === null && T.pickAct('', {}) === null && T.pickAct('x', {}) === null, 'a name outside [a-z][a-z0-9_.-]{1,39} is refused');
  ok(T.pickAct('lang_switch', { to: 'fr' }).to === 'fr' && !('to' in T.pickAct('lang_switch', { to: 'de' })), 'lang_switch keeps only he/en/fr/ru/ar');
  ok(T.pickAct('designer_open', { project: { slug: 'rainbow-tel-aviv' } }).p === 'rainbow-tel-aviv', 'a design-order style project object gives its slug');

  // the queue printed with the page, then the published function
  var w = env(); var c = clock();
  w.nlTrackQ = [['call_book', { project: 'rainbow-tel-aviv', k: 'video' }, 1]];
  w.dataLayer = [{ event: 'gtm.js' }, { event: 'basket_open', project: 'Rainbow' }, { event: 'whatsapp_click' }, { event: 'offer_sent', items: 3 }];
  var r = rec(w, c, { endpoint: '/t', page: 7001, proj: 7001, lang: 'fr', mode: 'full' });
  r.start(); T.publish(w, r);
  var sentNow = allEv(r).concat(r.queue);
  var q = sentNow.filter(function (e) { return e.t === 'act'; }).map(function (e) { return e.n; });
  ok(q.indexOf('call_book') > -1, 'a call queued before the file ran is recorded', q);
  ok(q.indexOf('basket_open') > -1 && q.indexOf('offer_sent') > -1 && q.indexOf('whatsapp_click') < 0, 'the dataLayer mirror: basket_open and offer_sent kept, whatsapp_click (already a tap) and gtm.js skipped', q);
  var off = sentNow.filter(function (e) { return e.n === 'offer_sent'; })[0];
  ok(off && off.v === 3 && off.src === 'ga' && !('project' in off), 'a mirrored event keeps items as v, not the display name', off);
  ok(r.sent.length >= 1, 'call_book is urgent: sent at once', r.sent.length);
  w.nlTrack('rfp_send', { project: 'rainbow-tel-aviv', v: 2 });
  fire(w, 'nl:track', { name: 'view_open', data: { floor: 23, bearing: 268 } });
  fire(w, 'nadlan:design-order', { project: { slug: 'ashira' }, unit: { id: 'E-4A', rooms: 4 }, notes: [{ text: 'secret note' }] });
  r.flush();
  var all = allEv(r).filter(function (e) { return e.t === 'act'; });
  var names = all.map(function (e) { return e.n; });
  ok(names.indexOf('rfp_send') > -1 && names.indexOf('view_open') > -1 && names.indexOf('design_order') > -1, 'nlTrack, nl:track and nadlan:design-order all arrive', names);
  ok(JSON.stringify(all).indexOf('secret note') < 0, 'the design order\'s note text is never sent');
  var body = r.sent[r.sent.length - 1].body;
  ok(body.mode === 'full' && body.proj === 7001, 'the batch carries mode and project', { mode: body.mode, proj: body.proj });
  // a mortgage input: once per 30 s per calculator, never the number
  var root = { getAttribute: function (k) { return k === 'data-nl-calc' ? 'cockpit' : null; }, id: '', className: 'nlck' };
  var inp = { nodeName: 'INPUT', type: 'number', id: 'x', value: '2950000', closest: function () { return root; }, getAttribute: function () { return null; } };
  evAt(w.document, 'input', { target: inp, isTrusted: true });
  evAt(w.document, 'change', { target: inp, isTrusted: true });
  c.t += 31000; evAt(w.document, 'input', { target: inp, isTrusted: true });
  r.flush();
  var mc = allEv(r).filter(function (e) { return e.n === 'mortgage_check'; });
  ok(mc.length === 2 && mc[0].k === 'cockpit' && JSON.stringify(mc).indexOf('2950000') < 0, 'mortgage_check: once per 30 s per calculator, the number never sent', mc);
  evAt(w.document, 'input', { target: { nodeName: 'INPUT', type: 'text', closest: function () { return root; }, getAttribute: function () { return null; } }, isTrusted: true });
  ok(r.queue.filter(function (e) { return e.n === 'mortgage_check'; }).length === 0, 'a text field (a name) is not a payment check');
  var quick = { nodeName: 'INPUT', type: 'text', inputMode: 'numeric', id: 'nlmq-a', value: '1500000', closest: function () { return null; }, getAttribute: function (k) { return k === 'inputmode' ? 'numeric' : null; } };
  evAt(w.document, 'input', { target: quick, isTrusted: true });
  var qk = r.queue.filter(function (e) { return e.n === 'mortgage_check'; });
  ok(qk.length === 1 && qk[0].k === 'nlmq' && JSON.stringify(qk).indexOf('1500000') < 0, 'the mortgage page quick calculator (nlmq-, outside any root) counts, keyed nlmq, the number never sent', qk);
  var phone = { nodeName: 'INPUT', type: 'text', inputMode: 'numeric', id: 'lead-phone', closest: function () { return null; }, getAttribute: function (k) { return k === 'inputmode' ? 'numeric' : null; } };
  evAt(w.document, 'input', { target: phone, isTrusted: true });
  ok(r.queue.filter(function (e) { return e.n === 'mortgage_check'; }).length === 1, 'a numeric phone field outside a calculator is not a payment check');
  r.stop();
})();
(function () {
  // the engine page: the start is not a choice; a unit, a tool, a saved unit and a language are
  var w = env(); var c = clock();
  var st = { projectKey: 'rainbow-tel-aviv', unitId: 'A-23', tool: null, favs: [], lang: 'he' };
  w.NadLanEngine = { state: st };
  w.NADLAN_SHOWROOM = { projects: { 'rainbow-tel-aviv': { wp_id: 7001, units: [{ id: 'A-23', floor: 23, rooms: 4, dir: 'west' }, { id: 'B-9', floor: 9, rooms: 3, dir: 'north' }] } } };
  var r = rec(w, c, { endpoint: '/t', page: 7001, proj: 7001, lang: 'he', mode: 'full' });
  r.start();
  r.watchEngine();
  ok(r.queue.filter(function (e) { return e.t === 'act'; }).length === 0, 'engine: the page\'s own start (a deep-linked unit) is not recorded as a choice');
  st.unitId = 'B-9'; r.watchEngine();
  st.tool = 'view'; r.watchEngine();
  st.tool = null; r.watchEngine(); st.tool = 'studio'; r.watchEngine();
  st.favs = ['B-9']; r.watchEngine();
  st.lang = 'fr'; r.watchEngine();
  var acts = r.queue.filter(function (e) { return e.t === 'act'; });
  var nm = acts.map(function (e) { return e.n; });
  ok(JSON.stringify(nm) === JSON.stringify(['unit_open', 'view_open', 'designer_open', 'favorite', 'lang_switch']), 'engine: unit, view, designer, saved, language, in order', nm);
  ok(acts[0].f === 9 && acts[0].u === 'B-9' && acts[0].rooms === 3 && acts[0].p === '7001', 'engine: the unit\'s floor and rooms come from the page\'s own data', acts[0]);
  ok(!/NadLanEngine\.(render|t)\(/.test(SRC) && !/NadLanEngine\.state\.\w+\s*=[^=]/.test(SRC), 'engine: never called, never written (read only)');
  r.stop();
})();
(function () {
  // lite: no open, no taps, no leave; only the tool events
  var w = env({ href: 'https://nad-lan.co.il/tour/designer/?project=ashira' }); var c = clock();
  var r = rec(w, c, { endpoint: '/t', page: 0, proj: 0, lang: 'he', mode: 'lite' });
  r.start();
  fire(w, 'nl:floor', { floor: 3 });
  r.leave();
  w.nlTrack = null; T.publish(w, r);
  w.nlTrack('designer_action', { project: 'ashira', a: 'partition-remove' });
  r.flush();
  var e = allEv(r);
  ok(e.length === 1 && e[0].t === 'act' && e[0].a === 'partition-remove' && r.sent[0].body.mode === 'lite' && r.sent[0].body.page === 0, 'lite: only the tool event is sent (no open, no stage event, no leave)', e.map(function (x) { return x.t; }));
  // the opt-out
  w.nlTrack.off();
  ok(w._store.nl_vt_off === '1' && T.optedOut(w) === true, 'nlTrack.off() stores the visitor\'s own opt-out and boot respects it');
  var w2 = env(); w2._store.nl_vt_off = '1'; w2.NL_TRAIL_CFG = { endpoint: '/x', page: 1 };
  ok(T.boot(w2) === null && typeof w2.nlTrack === 'function' && w2.nlTrack('basket_add', {}) === false, 'opted out: boot returns null and nlTrack is a safe no-op');
  var w3 = env({ nav: { globalPrivacyControl: true } }); w3.NL_TRAIL_CFG = { endpoint: '/x', page: 1 }; w3.nlTrackQ = [['call_book', {}, 1]];
  T.boot(w3);
  ok(w3.nlTrackQ.length === 0 && w3._calls.length === 0, 'GPC: the page\'s queue is emptied, nothing sent');
})();

console.log('\n' + (n - fails) + ' of ' + n + ' passed' + (fails ? ', ' + fails + ' FAILED' : ''));
process.exit(fails ? 1 : 0);
