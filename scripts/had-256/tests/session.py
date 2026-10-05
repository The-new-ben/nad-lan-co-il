"""An HTTP session on the bench (cookies + the page's REST nonce), synthetic data builders, a parallel runner."""
import http.cookiejar
import io
import json
import re
import threading
import urllib.error
import urllib.parse
import urllib.request
import uuid as _uuid

from bench import base, user, state, SEED, _json


class Session:
    def __init__(self, variant, ip=None):
        self.v = variant
        self.base = base(variant)
        self.jar = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        self.nonce = ''
        self.ip = ip
        self.uid = 0

    def _req(self, method, url, data=None, headers=None, timeout=200):
        h = {'Accept': 'application/json'}
        if self.ip:
            h['X-NLJ-IP'] = self.ip
        h.update(headers or {})
        req = urllib.request.Request(url, data=data, headers=h, method=method)
        try:
            with self.op.open(req, timeout=timeout) as r:
                return r.status, r.read(), dict(r.headers)
        except urllib.error.HTTPError as e:
            return e.code, e.read(), dict(e.headers)
        except Exception as e:   # a dropped connection, a timeout
            return 0, str(e).encode(), {}

    def page(self, extra=''):
        s, raw, _ = self._req('GET', self.base + '/post-listing/' + extra, headers={'Accept': 'text/html'})
        html = raw.decode('utf-8', 'replace')
        m = re.search(r'"nonce":"([a-f0-9]+)"', html)
        self.nonce = m.group(1) if m else ''
        m2 = re.search(r'"uid":(\d+)', html)
        self.uid = int(m2.group(1)) if m2 else 0
        return s, html

    def login(self, key):
        u = user(key)
        if self.v == 'after':
            s, j = self.post('/owner/account/login', {'email': u['email'], 'password': u['password']}, nonce=False)
            assert s == 200, (s, j)
        else:
            self.jar.set_cookie(http.cookiejar.Cookie(0, 'wordpress_test_cookie', 'WP%20Cookie%20check', None, False, '127.0.0.1', False, False, '/', True, False, None, False, None, None, {}))
            data = urllib.parse.urlencode({'log': u['email'], 'pwd': u['password'], 'wp-submit': 'Log In', 'testcookie': '1', 'redirect_to': self.base + '/post-listing/'}).encode()
            self._req('POST', self.base + '/wp-login.php', data, {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html'})
        self.page()
        assert self.nonce, 'no nonce on the page'
        return self

    def rest(self, method, path, body=None, nonce=True, raw=False):
        url = self.base + '/wp-json/nadlan/v1' + path
        h = {}
        if nonce and self.nonce:
            h['X-WP-Nonce'] = self.nonce
        data = None
        if body is not None:
            data = json.dumps(body).encode('utf-8')
            h['Content-Type'] = 'application/json'
        s, b, hd = self._req(method, url, data, h)
        return (s, b, hd) if raw else (s, _json(b))

    def get(self, path, **kw):
        return self.rest('GET', path, **kw)

    def post(self, path, body=None, **kw):
        return self.rest('POST', path, body if body is not None else {}, **kw)

    def upload(self, path, filename, content, fields=None, ctype='application/octet-stream'):
        bnd = '----nlj' + _uuid.uuid4().hex
        buf = io.BytesIO()
        for k, v in (fields or {}).items():
            buf.write(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (bnd, k, v)).encode())
        buf.write(('--%s\r\nContent-Disposition: form-data; name="photo"; filename="%s"\r\nContent-Type: %s\r\n\r\n' % (bnd, filename, ctype)).encode())
        buf.write(content)
        buf.write(('\r\n--%s--\r\n' % bnd).encode())
        h = {'Content-Type': 'multipart/form-data; boundary=' + bnd}
        if self.nonce:
            h['X-WP-Nonce'] = self.nonce
        s, b, _ = self._req('POST', self.base + '/wp-json/nadlan/v1' + path, buf.getvalue(), h)
        return s, _json(b)

    def fetch(self, url, headers=None):
        return self._req('GET', url if url.startswith('http') else self.base + url, headers=dict({'Accept': '*/*'}, **(headers or {})))


def jpeg_bytes(w=800, h=600, color=(47, 111, 134), exif=None, mark=True, fmt='JPEG'):
    from PIL import Image, ImageDraw
    im = Image.new('RGB', (w, h), color)
    if mark:
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, w // 3, h // 4], fill=(240, 200, 40))     # an asymmetric corner block: a turn or a mirror shows
        d.rectangle([w - w // 8, h - h // 3, w - 1, h - 1], fill=(200, 30, 30))
    out = io.BytesIO()
    kw = {'quality': 92} if fmt in ('JPEG', 'WEBP') else {}
    if exif is not None:
        kw['exif'] = exif
    im.save(out, fmt, **kw)
    return out.getvalue()


def full_fields(**over):
    f = dict(SEED['listing'])
    f.update({'deal': 'sale', 'ptype': 'apartment', 'phone_ok': False, 'owner_ok': True})
    f.update(over)
    return f


def ready_draft(sess, photos=1, **over):
    """AFTER: a draft with every field and photos, saved; returns (draft_id, rev)."""
    s, d = sess.post('/owner/draft', {'create_key': str(_uuid.uuid4()), 'fields': full_fields(**over), 'step': 'details'})
    assert s in (200, 201), (s, d)
    refs = []
    for i in range(photos):
        s, j = sess.upload('/owner/photo', 'p%d.jpg' % i, jpeg_bytes(color=(40 + i * 30, 90, 120)), {'draft': d['id']}, 'image/jpeg')
        assert s == 200, (s, j)
        refs.append({'ref': j['ref']})
    s, d2 = sess.post('/owner/draft/%d' % d['id'], {'rev': d['rev'], 'fields': full_fields(**over), 'photos': refs, 'step': 'preview'})
    assert s == 200, (s, d2)
    return d2['id'], d2['rev']


def before_drop(sess, text=None, photos=1):
    """BEFORE (1.0.0 doors): photos, then /owner/submit; returns the drop id (state ready)."""
    ids = []
    for i in range(photos):
        s, j = sess.upload('/owner/photo', 'p%d.jpg' % i, jpeg_bytes(color=(40 + i * 30, 90, 120)), {}, 'image/jpeg')
        assert s == 200, (s, j)
        ids.append(j['id'])
    text = text or 'למכירה, 4 חדרים, 96 מ״ר, קומה 3 מתוך 8. שכונת הדוגמה, תל אביב יפו. 3,450,000 ש״ח.'
    s, j = sess.post('/owner/submit', {'text': text, 'photos': ids, 'name': 'דנה', 'phone': '050-0000000', 'who': 'owner', 'owner': '1', 'consent': '1'})
    assert s == 200 and j.get('drop'), (s, j)
    return j['drop']


def listings_of(variant, drop):
    """The nadlan_property rows of a drop: content rows (by claim or nl_drop_id), and the empty auto-draft placeholders."""
    st = state(variant, drop)
    claims = [o for o in st['options'] if o['option_name'].startswith('nl_pub_%d_' % drop)]
    claimed = set()
    for c in claims:
        try:
            claimed.add(int(json.loads(c['option_value'])['post']))
        except Exception:
            pass
    # every test resets the site first, so every listing row that is not an empty placeholder belongs to this test
    # (a 1.0.0 row killed before its meta has no nl_drop_id yet, and is still a public duplicate)
    content = [p for p in st['properties'] if p['post_status'] not in ('auto-draft', 'trash')]
    empties = [p for p in st['properties'] if p['post_status'] == 'auto-draft']
    return {'content': content, 'auto_drafts': empties, 'claims': claims, 'state': st}


def parallel(fns):
    out = [None] * len(fns)

    def run(i, f):
        out[i] = f()
    ts = [threading.Thread(target=run, args=(i, f)) for i, f in enumerate(fns)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return out
