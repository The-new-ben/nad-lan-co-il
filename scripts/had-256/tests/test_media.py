"""P0 (Maya R1 on d2b8f349) + L03 photo privacy, on real WordPress (Playground) with synthetic photos.

Rule under test: no public copy of an owner's photo exists unless its listing is committed as 'publish'.
For each case every candidate is fetched ANONYMOUSLY: every file under wp-content/uploads (found on disk), the
owner-only proxy, and the sealed private files. "Exposed" = an anonymous GET returns bytes that open as an image.
"""
import hashlib
import io
import json
import pathlib
import time
import urllib.request
import uuid

from bench import reset, fault, state, record, REPO, bench
from session import Session, ready_draft, jpeg_bytes, full_fields

V = 'after'
UP = REPO / 'scripts' / 'had-256' / 'local' / '.runtime' / V / 'site' / 'wp-content' / 'uploads'
BASE = 'http://127.0.0.1:9401'


def anon(url):
    req = urllib.request.Request(url, headers={'Accept': '*/*'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read(), r.headers.get('Content-Type', '')
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get('Content-Type', '')
    except Exception as e:
        return 0, str(e).encode(), ''


def is_image(b):
    from PIL import Image
    try:
        Image.open(io.BytesIO(b)).verify()
        return True
    except Exception:
        return False


def candidates(draft, refs):
    """every file under uploads (anonymous static GET), the proxy (anonymous), for these refs"""
    out = []
    if UP.exists():
        for p in UP.rglob('*'):
            if p.is_file() and p.name not in ('index.php', '.htaccess'):
                out.append(('file', BASE + '/wp-content/uploads/' + p.relative_to(UP).as_posix()))
    for r in refs:
        for s in ('t', 'f'):
            out.append(('proxy', BASE + '/wp-admin/admin-ajax.php?action=nl_owner_img&d=%d&r=%s&s=%s' % (draft, r, s)))
    return out


def exposure(draft, refs):
    hits, seen = [], []
    for kind, url in candidates(draft, refs):
        s, b, ct = anon(url)
        img = s == 200 and is_image(b)
        seen.append({'kind': kind, 'url': url.replace(BASE, ''), 'status': s, 'image': img})
        if img:
            hits.append(url.replace(BASE, ''))
    return hits, seen


def draft_with_photos(sess, n=2, **over):
    d, rev = ready_draft(sess, photos=n, **over)
    st, j = sess.get('/owner/draft/%d' % d)
    return d, rev, [p['ref'] for p in j['photos']]


def pub(sess, d, rev, key=None, **extra):
    body = {'request_key': key or str(uuid.uuid4()), 'rev': rev}
    body.update(extra)
    return sess.post('/owner/draft/%d/publish' % d, body)


def listing_status(d):
    st = state(V, d)
    res = st['drop'].get('nl_result')
    he = int(res['he_id']) if isinstance(res, dict) and res.get('he_id') else 0
    props = {int(p['ID']): p['post_status'] for p in st['properties']}
    return he, props.get(he, ''), props


def case(title, setup, expect_public):
    reset(V)
    s = Session(V).login('dana')
    d, rev, refs = draft_with_photos(s, 2)
    pre_hits, _ = exposure(d, refs)
    info = setup(s, d, rev) or {}
    time.sleep(0.3)
    he, st, props = listing_status(d)
    hits, seen = exposure(d, refs)
    ok = (not pre_hits) and ((bool(hits) and st == 'publish') if expect_public else (not hits))
    record({'id': 'L03', 'variant': V, 'label': 'real-wp', 'title': 'public photos: ' + title, 'status': 'pass' if ok else 'fail',
            'evidence': {'before_publish_exposed': pre_hits, 'listing_status': st, 'exposed_now': hits, 'checked': len(seen), 'info': info}})
    return s, d, rev, refs


# --- no public copy on any non-success path ---
case('validation failure (422)', lambda s, d, rev: {'publish': pub(s, d, rev, key=None)[0]} if not s.post('/owner/draft/%d' % d, {'rev': rev, 'fields': full_fields(owner_ok=False), 'photos': [{'ref': r} for r in s.get('/owner/draft/%d' % d)[1] and [p['ref'] for p in s.get('/owner/draft/%d' % d)[1]['photos']]], 'step': 'preview'})[0] == 200 else {'publish': pub(s, d, rev + 1)[0]}, False)


def held(s, d, rev):
    st, j = s.get('/owner/draft/%d' % d)
    f = j['fields']
    f['desc'] = f['desc'] + ' מתאים למשפחות.'
    s.post('/owner/draft/%d' % d, {'rev': j['rev'], 'fields': f, 'photos': [{'ref': p['ref']} for p in j['photos']], 'step': 'preview'})
    r = pub(s, d, j['rev'] + 1)
    return {'publish': [r[0], r[1].get('state')]}


case('a fair-housing hold (pending)', held, False)


def admin_test(s, d, rev):
    a = Session(V).login('admin')
    # the admin test switch works only for an admin's own run; here: dana's draft cannot use it
    r = pub(s, d, rev, test='1')
    return {'publish': [r[0], r[1].get('state')]}


for where in ('fenced:owner_claim', 'before_claim', 'claim_pending', 'fenced:owner_content', 'fenced:owner_meta', 'fenced:owner_render', 'fenced:owner_status'):
    def killed(s, d, rev, where=where):
        fault(V, 'kill', {'where': where, 'n': 1})
        r = pub(s, d, rev)
        return {'publish': [r[0], r[1].get('where') or r[1].get('code')]}
    case('killed at %s' % where, killed, False)

# killed after 'publish' was committed and before the copies: a published listing without pictures (fail-closed), then the retry repairs
for where in ('owner_before_media', 'attach_pending', 'fenced:attach'):
    reset(V)
    s = Session(V).login('dana')
    d, rev, refs = draft_with_photos(s, 2)
    fault(V, 'ttl', {'secs': 3})
    fault(V, 'kill', {'where': where, 'n': 1})
    k = str(uuid.uuid4())
    a = pub(s, d, rev, key=k)
    he, st1, _ = listing_status(d)
    hits1, _ = exposure(d, refs)
    time.sleep(4.5)
    b = pub(s, d, rev, key=k)
    he2, st2, _ = listing_status(d)
    hits2, _ = exposure(d, refs)
    fault(V, 'ttl', None)
    ok = a[0] == 500 and b[0] == 200 and st2 == 'publish' and len(hits2) >= 2 and (not hits1 or st1 == 'publish')
    record({'id': 'L03', 'variant': V, 'label': 'real-wp', 'title': 'public photos: killed at %s (after the publish commit), then retried' % where, 'status': 'pass' if ok else 'fail',
            'evidence': {'killed': [a[0], a[1].get('where')], 'status_after_kill': st1, 'exposed_after_kill': hits1, 'retry': [b[0], b[1].get('state')], 'status_after_retry': st2, 'exposed_after_retry': hits2}})

# a fenced-out run (paused past the TTL at the status commit) never writes a copy for a listing that is not published
reset(V)
s = Session(V).login('dana')
d, rev, refs = draft_with_photos(s, 1)
fault(V, 'ttl', {'secs': 3})
fault(V, 'pause', {'where': 'fenced:owner_status', 'secs': 7, 'n': 1})
k = str(uuid.uuid4())
from session import parallel
out = {}


def run_a():
    out['a'] = pub(s, d, rev, key=k)


def run_b():
    time.sleep(4.5)
    out['b'] = pub(s, d, rev, key=k)


parallel([run_a, run_b])
he, st, _ = listing_status(d)
hits, _ = exposure(d, refs)
fault(V, 'ttl', None)
record({'id': 'L03', 'variant': V, 'label': 'real-wp', 'title': 'public photos: run A paused at the status commit past the TTL, run B took over', 'status': 'pass' if out['b'][0] == 200 and st == 'publish' and hits else 'fail',
        'evidence': {'A': out['a'][0], 'B': out['b'][0], 'status': st, 'exposed': hits}})

# --- success, then every exit from 'publish' revokes, and coming back restores ---
reset(V)
s = Session(V).login('dana')
d, rev, refs = draft_with_photos(s, 2)
r = pub(s, d, rev)
he, st, _ = listing_status(d)
pub_hits, _ = exposure(d, refs)
steps = {'published': [st, len(pub_hits)]}
s.post('/owner/update', {'id': he, 'status': 'sold'})
steps['sold (still published, notice on the page)'] = [listing_status(d)[1], len(exposure(d, refs)[0])]
s.post('/owner/update', {'id': he, 'status': 'active'})
s.post('/owner/update', {'id': he, 'action': 'remove'})
steps['removed (trash)'] = [listing_status(d)[1], len(exposure(d, refs)[0])]
s.post('/owner/update', {'id': he, 'action': 'republish'})
steps['published again'] = [listing_status(d)[1], len(exposure(d, refs)[0])]
st2, j = s.get('/owner/draft/%d' % d)
f = j['fields']
f['desc'] = f['desc'] + ' מתאים למשפחות.'
s.post('/owner/draft/%d' % d, {'rev': j['rev'], 'fields': f, 'photos': [{'ref': p['ref']} for p in j['photos']], 'step': 'preview'})
pub(s, d, j['rev'] + 1)
steps['edited into a hold (pending)'] = [listing_status(d)[1], len(exposure(d, refs)[0])]
ok = steps['published'][1] >= 2 and steps['sold (still published, notice on the page)'][1] >= 2 and steps['removed (trash)'][1] == 0 and steps['published again'][1] >= 2 and steps['edited into a hold (pending)'][1] == 0
record({'id': 'L03', 'variant': V, 'label': 'real-wp', 'title': 'public photos: served when published; revoked on remove and on a hold; restored on publishing again', 'status': 'pass' if ok else 'fail', 'evidence': steps})

# --- the sealed private file itself: an anonymous static GET gets ciphertext, never the photo ---
reset(V)
s = Session(V).login('dana')
d, rev, refs = draft_with_photos(s, 1)
priv = [p for p in UP.rglob('*.bin')]
res = []
for p in priv:
    stt, b, ct = anon(BASE + '/wp-content/uploads/' + p.relative_to(UP).as_posix())
    res.append({'path': '/wp-content/uploads/' + p.relative_to(UP).as_posix(), 'status': stt, 'opens_as_image': is_image(b), 'starts': b[:4].decode('latin-1')})
pr = anon(BASE + '/wp-admin/admin-ajax.php?action=nl_owner_img&d=%d&r=%s&s=f' % (d, refs[0]))
own = s.fetch('/wp-admin/admin-ajax.php?action=nl_owner_img&d=%d&r=%s&s=f' % (d, refs[0]))
other = Session(V).login('yoav').fetch('/wp-admin/admin-ajax.php?action=nl_owner_img&d=%d&r=%s&s=f' % (d, refs[0]))
ok = res and all(not r['opens_as_image'] for r in res) and pr[0] == 401 and own[0] == 200 and is_image(own[1]) and other[0] == 404
record({'id': 'L03', 'variant': V, 'label': 'real-wp', 'title': 'a draft photo: sealed file (anonymous static GET), the proxy anonymous / owner / other user', 'status': 'pass' if ok else 'fail',
        'evidence': {'sealed_files': res, 'proxy_anonymous': pr[0], 'proxy_owner': [own[0], is_image(own[1])], 'proxy_other_user': other[0]},
        'notes': 'Playground serves static files without .htaccess, so the sealed .bin answers 200 here; its bytes are ciphertext (NLS1 header) and do not open as an image. On the live server the deny-all .htaccess may also refuse it; that is not assumed.'})
