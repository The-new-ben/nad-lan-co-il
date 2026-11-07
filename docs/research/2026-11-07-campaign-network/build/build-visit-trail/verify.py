"""visit trail build (7.11.2026, HAD-678): plugins/nadlan-config/assets/visit-trail/trail.js in a real browser (Playwright, channel chrome,
headless) on the SAVED live copy of /projects/rainbow-tel-aviv/ (docs/source-snapshots/projects-rainbow-tel-aviv/, the latest file),
served from 127.0.0.1 with every request to another host blocked (the page's own scripts do not load, so the stage events are fired by
hand, with the payloads the stage files send). trail.js and NL_TRAIL_CFG are injected as inc/visit-trail.php prints them.

The local server answers POST /wp-json/nadlan/v1/trail (logs every body and header, 204), POST /wp-json/nadlan/v1/lead and
POST /wp-admin/admin-post.php (log the visit id they carry).
Pass 1, a phone (390x844, touch), recording on: the ten stage events, taps on the page's real WhatsApp bar (#nlcta) and hero WhatsApp
button, a stage step, a call link, the booking band (day, hour, send), a link that is not a CTA (not recorded), a lead fetch (carries
X-NL-Visit), a form posted to admin-post.php with a phone typed in it (carries nl_visit; the phone is in no trail request); the 20 s
timer sends without any page change; the page left sends the rest with a leave record; a second page view keeps the visit id.
Pass 2, 1280x900, the same visit (the id kept); pass 3 Global Privacy Control, pass 4 Do Not Track, pass 5 an automated browser
(navigator.webdriver): nothing is sent, nothing is stored, fetch is the browser's own, the form carries no visit id.
On every pass: no page error from trail.js. Report: verify.json; exit 1 on any failed check.
Run:  python docs/research/2026-11-07-campaign-network/build/build-visit-trail/verify.py
"""
import json, sys, pathlib, re, socket, threading, time, urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from playwright.sync_api import sync_playwright

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
SNAPDIR = REPO / 'docs' / 'source-snapshots' / 'projects-rainbow-tel-aviv'
SNAP = sorted(SNAPDIR.glob('*.html'))[-1]
TRAIL = REPO / 'plugins' / 'nadlan-config' / 'assets' / 'visit-trail' / 'trail.js'
PAGE_ID = 7001
LOG = {'trail': [], 'lead': [], 'post': []}
LOCK = threading.Lock()

INJECT = ('<script>window.NL_TRAIL_CFG={"endpoint":"/wp-json/nadlan/v1/trail","page":%d,"lang":"he"};</script>\n'
          '<script src="/wp-content/plugins/nadlan-config/assets/visit-trail/trail.js?ver=1.72.602" id="nadlan-visit-trail-js" defer></script>\n') % PAGE_ID
FIXTURE = ('<div id="vt-fixture" style="padding:20px 20px 320px;text-align:center">'  # clear of the corner buttons (the accessibility button, the WhatsApp bar)
           '<a id="vt-tel" href="tel:+972525101555">חיוג למשרד</a> '
           '<a id="vt-plain" href="#vt-fixture">קישור רגיל</a> '
           '<form id="vt-form" action="/wp-admin/admin-post.php" method="post"><input type="hidden" name="action" value="nadlan_lead">'
           '<input id="vt-phone" name="lead_phone" aria-label="טלפון"><button id="vt-send" type="submit">שליחה</button></form></div>\n'
           # a browser with no dialer turns a tel: tap into a failed navigation; the phone's dialer is simulated by keeping the page
           '<script>document.getElementById("vt-tel").addEventListener("click",function(e){e.preventDefault();});</script>\n')


def page_html():
    h = SNAP.read_text(encoding='utf-8')
    i = h.rfind('</body>')
    return h[:i] + FIXTURE + INJECT + h[i:]


HTML = page_html().encode('utf-8')


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body=b'', ctype='text/html; charset=utf-8'):
        self.send_response(code)
        if body:
            self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        p = urllib.parse.urlparse(self.path).path
        if p in ('/projects/rainbow-tel-aviv/', '/projects/rainbow-tel-aviv'):
            return self._send(200, HTML)
        if p.endswith('/visit-trail/trail.js'):
            return self._send(200, TRAIL.read_bytes(), 'application/javascript; charset=utf-8')
        if p == '/other/':
            return self._send(200, b'<!doctype html><title>other</title><p>other</p>')
        return self._send(404, b'')

    def do_POST(self):
        n = int(self.headers.get('Content-Length') or 0)
        body = self.rfile.read(n) if n else b''
        p = urllib.parse.urlparse(self.path).path
        with LOCK:
            if p == '/wp-json/nadlan/v1/trail':
                LOG['trail'].append({'t': time.time(), 'ctype': self.headers.get('Content-Type', ''), 'origin': self.headers.get('Origin', ''), 'len': len(body), 'raw': body.decode('utf-8', 'replace')})
                return self._send(204)
            if p == '/wp-json/nadlan/v1/lead':
                LOG['lead'].append({'visit': self.headers.get('X-NL-Visit', ''), 'body': body.decode('utf-8', 'replace')})
                return self._send(200, b'{"ok":true}', 'application/json')
            if p == '/wp-admin/admin-post.php':
                LOG['post'].append({'body': body.decode('utf-8', 'replace'), 'visit': self.headers.get('X-NL-Visit', '')})
                return self._send(200, b'<!doctype html><p>received</p>')
        return self._send(404)


s0 = socket.socket(); s0.bind(('127.0.0.1', 0)); PORT = s0.getsockname()[1]; s0.close()
ORIGIN = f'http://127.0.0.1:{PORT}'
URL = ORIGIN + '/projects/rainbow-tel-aviv/'
srv = ThreadingHTTPServer(('127.0.0.1', PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

checks, fails = [], 0


def ok(cond, name, got=None):
    global fails
    checks.append({'ok': bool(cond), 'name': name, 'got': got})
    if not cond:
        fails += 1
    print(('  ok   ' if cond else '  FAIL ') + name + ('' if got is None else '  [' + (got if isinstance(got, str) else json.dumps(got, ensure_ascii=False)) + ']'))


def reset():
    with LOCK:
        for k in LOG:
            LOG[k].clear()


def trail_events():
    with LOCK:
        out = []
        for r in LOG['trail']:
            b = json.loads(r['raw'])
            for e in b['ev']:
                e = dict(e); e['_pv'] = b['pv']; e['_vid'] = b['vid']; e['_seq'] = b['seq']
                out.append(e)
        return out


NOT_WD = "Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => false, configurable: true });"
STAGE_EVENTS = """() => {
  const f = (n, d) => window.dispatchEvent(new CustomEvent(n, { detail: d }));
  f('nl:floor', { floor: 23, heightM: 74.2, source: 'user' });
  f('nl:facing', { floor: 23, heightM: 74.2, bearing: 268, unit: '23-w', toward: null });
  f('nl:view', { mode: 'view', bearing: 271.5, vert: -2, source: 'user' });
  f('nl:quarter', { kind: 'park', name: 'פארק החורשות', id: 'q7' });
  f('nl:facility', { id: 'pool', name: 'בריכה' });
  f('nl:facility-tour', { id: 'pool', src: location.origin + '/x/tour/pool.jpg', small: location.origin + '/x/s.jpg', title: 'בריכה', note: 'הדמיה', opener: document.body });
  f('nl:floor-cta', { floor: 23, bearing: 268 });
  f('nl:floor-action', { action: 'inside', floor: 23, heightM: 74, bearing: 268, unit: '23-w' });
  f('nl:tour', { open: true, scene: 'living-25w' });
  f('nl:example', { open: true, id: '23-w', floor: 23, facing: 'מערב', bearing: 268 });
  return true;
}"""


def run_pass(pw_browser, label, viewport, init, record):
    print(f'\n{label}')
    reset()
    phone = viewport['width'] < 600
    ua = ('Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36' if phone else
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')  # a visitor's browser (headless Chrome names itself HeadlessChrome, a robot)
    ctx = pw_browser.new_context(viewport=viewport, is_mobile=phone, has_touch=phone, locale='he-IL', user_agent=ua)
    blocked = []

    def route(rt):
        u = rt.request.url
        if u.startswith(ORIGIN):
            return rt.continue_()
        blocked.append(u.split('?')[0][:90])
        return rt.abort()
    ctx.route('**/*', route)
    for s in init:
        ctx.add_init_script(s)
    if label.startswith('2.'):
        ctx.add_init_script("try{localStorage.setItem('nl_vid', %s)}catch(e){}" % json.dumps(json.dumps(KEEP)))
    errs = []
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append(str(e)))
    ctx.on('page', lambda p: p.close() if p != pg else None)  # WhatsApp opens a new tab (blocked): closed at once
    pg.goto(URL, wait_until='domcontentloaded')
    pg.wait_for_timeout(600)
    rec_on = pg.evaluate('() => !!(window.NL_TRAIL && window.NL_TRAIL.rec)')
    vid = pg.evaluate("() => { try { return (JSON.parse(localStorage.getItem('nl_vid')||'null')||{}).id || '' } catch (e) { return 'ERR' } }")
    wrapped = pg.evaluate('() => !!(window.fetch && window.fetch.__nlvt)')
    if record:
        ok(rec_on and re.fullmatch(r'[A-Za-z0-9_-]{22}', vid or '') and wrapped, 'the recorder runs, the visit id is in localStorage, the lead requests carry it', vid)
    else:
        ok(not rec_on and not vid and not wrapped, 'nothing runs: no recorder, no id stored, fetch is the browser\'s own', {'rec': rec_on, 'vid': vid, 'wrapped': wrapped})
    pg.evaluate(STAGE_EVENTS)
    # real taps on the page's own WhatsApp bar and hero button, a stage step, a call link, a plain link
    for sel in ('#nlcta a.nlcta-wa', 'a[data-nlps-ev="hero-wa"]', 'button[data-nlps-step="view"]', '#vt-tel', '#vt-plain'):
        try:
            pg.locator(sel).first.click(timeout=3000, force=True, no_wait_after=True)
        except Exception as e:
            pg.evaluate("(s) => document.querySelector(s) && document.querySelector(s).click()", sel)
        pg.wait_for_timeout(120)
    # the booking band: a day, an hour, send (the page's own booking script is not loaded: its buttons are added as booking.js draws them)
    pg.evaluate("""() => { const s = document.getElementById('nlsch') || document.body.appendChild(Object.assign(document.createElement('section'), { id: 'nlsch' }));
      s.insertAdjacentHTML('beforeend', '<button class="nlsch-day" id="vt-day">ה׳ <b>13</b></button><button class="nlsch-time" id="vt-time">10:30</button><button class="nlsch-go" id="vt-go">קבעו לי פגישה</button>'); }""")
    for sel in ('#vt-day', '#vt-time', '#vt-go'):
        pg.locator(sel).click(force=True, no_wait_after=True)
        pg.wait_for_timeout(100)
    # a lead request through fetch, as conversion-cta / smart-form / booking.js send it
    pg.evaluate("() => fetch('/wp-json/nadlan/v1/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: 'בדיקה', phone: '0501234567' }) }).then(r => r.status)")
    pg.wait_for_timeout(300)
    if record and label.startswith('1.'):
        pg.evaluate("() => window.dispatchEvent(new CustomEvent('nl:floor', { detail: { floor: 24, source: 'user' } }))")
        with LOCK:
            n0 = len(LOG['trail'])
        pg.wait_for_timeout(21000)  # the 20 s timer, no page change
        with LOCK:
            n1 = len(LOG['trail'])
        ok(n1 > n0, 'the 20 s timer sent a batch while the page stayed open', {'before': n0, 'after': n1})
    # the lead form: a phone typed, then sent (the page is left: pagehide)
    pg.locator('#vt-phone').fill('0501234567')
    pg.locator('#vt-send').click()
    pg.wait_for_load_state('domcontentloaded')
    pg.wait_for_timeout(500)
    # a second page view of the same visit, then away
    pg.goto(URL, wait_until='domcontentloaded')
    pg.wait_for_timeout(400)
    vid2 = pg.evaluate("() => { try { return (JSON.parse(localStorage.getItem('nl_vid')||'null')||{}).id || '' } catch (e) { return '' } }")
    pg.evaluate("() => window.dispatchEvent(new CustomEvent('nl:floor', { detail: { floor: 30, source: 'user' } }))")
    pg.goto(ORIGIN + '/other/', wait_until='domcontentloaded')
    pg.wait_for_timeout(800)
    ctx.close()
    ev = trail_events()
    with LOCK:
        posts, leads, trails = list(LOG['post']), list(LOG['lead']), list(LOG['trail'])
    terr = [e for e in errs if 'trail.js' in e or 'NL_TRAIL' in e]
    ok(not terr, 'no page error from trail.js', terr[:3])
    if not record:
        ok(not trails, 'no trail request at all', len(trails))
        ok(posts and 'nl_visit' not in posts[0]['body'], 'the form carries no visit id', posts[0]['body'][:120] if posts else None)
        ok(leads and leads[0]['visit'] == '', 'the lead fetch carries no X-NL-Visit', leads[0]['visit'] if leads else None)
        ok(not vid2, 'still no id stored after a second page view', vid2)
        return {'label': label, 'trail_requests': len(trails), 'blocked': len(blocked)}
    kinds = [e['t'] for e in ev]
    for t in ('open', 'floor', 'facing', 'view', 'quarter', 'facility', 'ftour', 'fcta', 'faction', 'tour', 'example', 'click', 'form', 'leave'):
        ok(t in kinds, f'recorded: {t}')
    g = lambda t: [e for e in ev if e['t'] == t]
    fc = (g('facing') or [{}])[0]
    ok(fc.get('f') == 23 and fc.get('b') == 268 and fc.get('u') == '23-w', 'facing: floor 23, 268°, unit 23-w', {k: fc.get(k) for k in ('f', 'b', 'u')})
    ft = (g('ftour') or [{}])[0]
    ok(set(ft) - {'at', '_pv', '_vid', '_seq'} == {'t', 'id', 'n'}, 'facility tour: id and name only (no picture address, no element)', ft)
    clicks = g('click')
    ck = [(c.get('k'), c.get('w', '')) for c in clicks]
    ok(('wa', 'bar') in ck, 'the WhatsApp bar tap: click wa, where bar', ck)
    ok(any(k == 'wa' and w == 'hero' for k, w in ck), 'the hero WhatsApp button: click wa, where hero')
    ok(any(c.get('k') == 'step' and c.get('id') == 'view' for c in clicks), 'the stage step "view"')
    ok(any(c.get('k') == 'tel' for c in clicks), 'the call link: click tel')
    ok(not any('קישור רגיל' in json.dumps(c, ensure_ascii=False) for c in clicks), 'a plain link is not recorded')
    bd = [c for c in clicks if c.get('k') in ('book_day', 'book_time', 'book_send')]
    ok([c['k'] for c in bd] == ['book_day', 'book_time', 'book_send'] and not any('l' in c for c in bd[:2]), 'booking: day, hour (their labels not kept), send', bd)
    fm = g('form')
    ok(fm and fm[0].get('k') == 'lead' and fm[0].get('id') == 'vt-form', 'the lead form: form lead vt-form', fm[:1])
    ok(all('0501234567' not in r['raw'] for r in trails), 'the typed phone is in no trail request (nor the lead\'s name)')
    ok(all('בדיקה' not in r['raw'] for r in trails), 'the lead fetch body is in no trail request')
    vids = {e['_vid'] for e in ev}
    ok(len(vids) == 1 and vid in vids and vid2 == vid, 'one visit id for both page views', sorted(vids))
    pvs = []
    for e in ev:
        if e['_pv'] not in pvs:
            pvs.append(e['_pv'])
    ok(len(pvs) == 2, 'two page views (pv), each opened once', len(pvs))
    ok(sum(1 for e in ev if e['t'] == 'open') == 2, 'two "open" events')
    lv = g('leave')
    ok(lv and all(isinstance(e.get('vis'), int) and e['vis'] > 0 for e in lv), 'leave records carry the time in view', [e.get('vis') for e in lv])
    ok(any(e['t'] == 'floor' and e.get('f') == 30 for e in ev), 'the second page view\'s pick arrived on leaving the page')
    ok(leads and leads[0]['visit'] == vid, 'the lead fetch carried X-NL-Visit = the visit id', leads[0]['visit'] if leads else None)
    pb = urllib.parse.parse_qs(posts[0]['body']) if posts else {}
    ok(pb.get('nl_visit') == [vid] and pb.get('lead_phone') == ['0501234567'], 'the form posted to admin-post.php carried nl_visit (and its own fields, untouched)', {k: v for k, v in pb.items() if k != 'lead_phone'})
    ok(all(r['ctype'].startswith('text/plain') and r['len'] < 16384 for r in trails), 'every trail request: text/plain, under 16 KB', max(r['len'] for r in trails))
    ok(all(len(json.loads(r['raw'])['ev']) <= 40 for r in trails), 'at most 40 events a request')
    seq = {}
    for r in trails:
        b = json.loads(r['raw']); seq.setdefault(b['pv'], []).append(b['seq'])
    ok(all(v == list(range(len(v))) for v in seq.values()), 'seq counts 0, 1, 2... per page view', seq)
    ok(all(u.startswith(('https://', 'http://')) for u in blocked), f'{len(blocked)} requests to other hosts blocked (the page\'s own scripts, fonts, WhatsApp): nothing left 127.0.0.1')
    return {'label': label, 'vid': vid, 'trail_requests': len(trails), 'events': len(ev), 'kinds': sorted(set(kinds)), 'blocked': len(blocked)}


KEEP = {}
import hashlib  # noqa: E402
report = {'snapshot': str(SNAP.relative_to(REPO)).replace('\\', '/'), 'trail_md5': hashlib.md5(TRAIL.read_bytes()).hexdigest(), 'passes': []}
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel='chrome', headless=True)
        r1 = run_pass(b, '1. phone 390x844, recording', {'width': 390, 'height': 844}, [NOT_WD], True)
        report['passes'].append(r1)
        KEEP.update({'id': r1['vid'], 'at': int(time.time() * 1000) - 3600000})
        r2 = run_pass(b, '2. desktop 1280x900, the same visit an hour later', {'width': 1280, 'height': 900}, [NOT_WD], True)
        ok(r2['vid'] == r1['vid'], 'pass 2 kept the visit id of pass 1 (30-day id)', r2['vid'])
        report['passes'].append(r2)
        report['passes'].append(run_pass(b, '3. Global Privacy Control on', {'width': 390, 'height': 844},
                                         [NOT_WD, "Object.defineProperty(Navigator.prototype, 'globalPrivacyControl', { get: () => true, configurable: true });"], False))
        report['passes'].append(run_pass(b, '4. Do Not Track on', {'width': 390, 'height': 844},
                                         [NOT_WD, "Object.defineProperty(Navigator.prototype, 'doNotTrack', { get: () => '1', configurable: true });"], False))
        report['passes'].append(run_pass(b, '5. an automated browser (navigator.webdriver, the default under Playwright)', {'width': 390, 'height': 844}, [], False))
        b.close()
finally:
    srv.shutdown()
report['checks'] = checks
report['passed'] = len(checks) - fails
report['failed'] = fails
(HERE / 'verify.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'\n{len(checks) - fails} of {len(checks)} passed' + (f', {fails} FAILED' if fails else ''))
sys.exit(1 if fails else 0)
