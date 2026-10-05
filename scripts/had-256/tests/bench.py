"""HAD-256 test helpers: the local Playground bench (scripts/had-256/local), synthetic data, Playwright (Python).

Every result is recorded with its label:
  real-wp  = ran against the real modules inside WordPress Playground (SQLite) through HTTP and a real browser
  mock     = ran against a stub or an extracted function only (never counted as a pass for runtime rows)
"""
import json
import os
import pathlib
import re
import time
import urllib.request
import urllib.error

from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[3]
QA = REPO / 'docs' / 'qa' / 'had-256'
SHOTS = QA / 'shots'
RESULTS = QA / 'results.json'
SEED = json.loads((REPO / 'scripts' / 'had-256' / 'local' / 'seed.json').read_text(encoding='utf-8'))
PORTS = {'after': int(os.environ.get('NLJ_AFTER_PORT', 9401)), 'before': 9411}
VIEWPORTS = {'390': {'width': 390, 'height': 844}, '320': {'width': 320, 'height': 740}, '412': {'width': 412, 'height': 915},
             '360': {'width': 360, 'height': 780}, '768': {'width': 768, 'height': 1024}, '1440': {'width': 1440, 'height': 900}}


def base(variant):
    return 'http://127.0.0.1:%d' % PORTS[variant]


def user(key):
    return next(u for u in SEED['users'] if u['key'] == key)


def http(method, url, body=None, headers=None, timeout=60):
    data = None
    h = {'Accept': 'application/json'}
    h.update(headers or {})
    if body is not None:
        data = json.dumps(body).encode('utf-8')
        h['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return r.status, _json(raw), dict(r.headers)
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, _json(raw), dict(e.headers)


def _json(raw):
    try:
        return json.loads(raw.decode('utf-8'))
    except Exception:
        return {'_raw': raw[:400].decode('utf-8', 'replace')}


def bench(variant, path, body=None, method=None):
    # a Playground worker sometimes answers the very first request after an idle spell without the bench mu-plugin's
    # routes (rest_no_route); the call is repeated, and the flake is noted in the README
    for i in range(4):
        r = http(method or ('POST' if body is not None else 'GET'), base(variant) + '/?rest_route=/nlj-test/v1' + path, body)
        if not (r[0] == 404 and isinstance(r[1], dict) and r[1].get('code') == 'rest_no_route'):
            return r
        time.sleep(0.5)
    return r


def reset(variant):
    s, j, _ = bench(variant, '/reset', {})
    assert s == 200, (s, j)
    return j


def fault(variant, name, value=None):
    s, j, _ = bench(variant, '/fault', {'name': name, 'value': value})
    assert s == 200, (s, j)


def state(variant, drop=0):
    return bench(variant, '/state' + ('&drop=%d' % drop if drop else ''))[1]


def mails(variant):
    return bench(variant, '/mail')[1]


def shot(page, variant, name, full=True):
    SHOTS.joinpath(variant).mkdir(parents=True, exist_ok=True)
    p = SHOTS / variant / (name + '.png')
    page.screenshot(path=str(p), full_page=full)
    return str(p.relative_to(REPO)).replace('\\', '/')


class _Lock:
    """a cross-process lock on results.json (several test scripts may record at the same time)"""
    def __enter__(self):
        self.p = str(RESULTS) + '.lock'
        for _ in range(600):
            try:
                self.fd = os.open(self.p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                return self
            except FileExistsError:
                if time.time() - os.path.getmtime(self.p) > 30:
                    try:
                        os.remove(self.p)
                    except OSError:
                        pass
                time.sleep(0.05)
        raise RuntimeError('results.json lock')

    def __exit__(self, *a):
        os.close(self.fd)
        os.remove(self.p)


def record(row):
    with _Lock():
        _record(row)


def _record(row):
    """row: id, title, variant, status (pass|fail|not run|info), label (real-wp|mock|n/a), evidence [], notes"""
    QA.mkdir(parents=True, exist_ok=True)
    rows = json.loads(RESULTS.read_text(encoding='utf-8')) if RESULTS.exists() else []
    key = (row['id'], row.get('variant', ''), row.get('title', ''))
    rows = [r for r in rows if (r['id'], r.get('variant', ''), r.get('title', '')) != key]
    row['at'] = time.strftime('%Y-%m-%d %H:%M:%S')
    rows.append(row)
    rows.sort(key=lambda r: (r['id'], r.get('variant', ''), r.get('title', '')))
    RESULTS.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    print('[%s] %-4s %-7s %-8s %s' % (row['status'].upper(), row['id'], row.get('variant', ''), row.get('label', ''), row.get('title', '')))


class Browser:
    def __init__(self, headless=True):
        self.pw = sync_playwright().start()
        self.b = self.pw.chromium.launch(channel='chrome', headless=headless)

    def ctx(self, vp='390', lang='he', **kw):
        c = self.b.new_context(viewport=VIEWPORTS[vp], locale='he-IL' if lang == 'he' else 'en-US', **kw)
        c.set_default_timeout(20000)
        return c

    def close(self):
        self.b.close()
        self.pw.stop()


def page_url(variant, lang='he', extra=''):
    return base(variant) + '/post-listing/' + ('?lang=en' if lang == 'en' else '') + (('&' if lang == 'en' else '?') + extra if extra else '')


def login_ui(page, variant, key, lang='he'):
    """Signs a synthetic user in. AFTER: the journey's own sign-in tab. BEFORE: WordPress' wp-login.php (the 1.x gate's door)."""
    u = user(key)
    if variant == 'after':
        page.goto(page_url(variant, lang))
        page.click('[data-act="tab-login"] >> nth=-1')
        page.fill('#j-mail2', u['email'])
        page.fill('#j-pw2', u['password'])
        with page.expect_navigation():
            page.click('#j-login-go')
    else:
        page.goto(base(variant) + '/wp-login.php')
        page.fill('#user_login', u['email'])
        page.fill('#user_pass', u['password'])
        with page.expect_navigation():
            page.click('#wp-submit')
        page.goto(page_url(variant, lang))
    page.wait_for_load_state('networkidle')


def nonce_of(page):
    return page.evaluate('() => (window.NLOWNER||{}).nonce || ""')


def rest(page, method, path, body=None, nonce=None):
    """A REST call from inside the page (its cookies), returns {status, j}."""
    return page.evaluate('''async ([m, p, b, n]) => {
        const o = {method: m, credentials: 'same-origin', headers: {'X-WP-Nonce': n || ((window.NLOWNER||{}).nonce || '')}};
        if (b !== null) { o.headers['Content-Type'] = 'application/json'; o.body = JSON.stringify(b); }
        const r = await fetch('/wp-json/nadlan/v1' + p, o);
        const t = await r.text(); let j = null; try { j = JSON.parse(t); } catch (e) { j = {_raw: t.slice(0, 300)}; }
        return {status: r.status, j};
    }''', [method, path, body, nonce])


def wait_status(page, text, timeout=15000):
    page.wait_for_function('t => (document.getElementById("nlj-st")||{}).innerText && document.getElementById("nlj-st").innerText.indexOf(t) > -1', arg=text, timeout=timeout)


def fill_details(page, d=None, deal='sale', ptype='apartment', phone_ok=False):
    d = d or SEED['listing']
    page.click('[data-deal="%s"]' % deal)
    page.select_option('#j-type', ptype)
    for k, sel in (('city', '#j-city'), ('hood', '#j-hood'), ('rooms', '#j-rooms'), ('size', '#j-size'), ('floor', '#j-floor'), ('price', '#j-price'), ('desc', '#j-desc'), ('cname', '#j-cname'), ('phone', '#j-phone')):
        page.fill(sel, d[k])
    if phone_ok:
        page.check('#j-phone-ok')
    page.check('#j-owner-ok')


def clear(id_, variant=None, prefix=''):
    with _Lock():
        _clear(id_, variant, prefix)


def _clear(id_, variant=None, prefix=''):
    """drops earlier rows of a test (so a renamed case does not linger in the table)"""
    if not RESULTS.exists():
        return
    rows = json.loads(RESULTS.read_text(encoding='utf-8'))
    rows = [r for r in rows if not (r['id'] == id_ and (variant is None or r.get('variant') == variant) and r.get('title', '').startswith(prefix))]
    RESULTS.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
