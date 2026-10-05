"""P0 (Maya R1 on d2b8f349) + L03 photo privacy, on real WordPress (Playground) with synthetic photos.

Rule under test: no public copy of an owner's photo exists unless its listing is committed as 'publish'.
After every case EVERY candidate is fetched ANONYMOUSLY: every file under wp-content/uploads (found on disk: the
public copies, their sizes, the sealed private files), and the owner-only proxy. "Exposed" = an anonymous GET returns
bytes that open as an image. The design is publish-then-copy (the copies are written only after the 'publish' status
is committed) with fail-closed revocation (the copies are deleted before a listing leaves 'publish').
"""
import io
import time
import urllib.error
import urllib.request
import uuid

from bench import reset, fault, state, record, REPO, clear
clear("L03", "after")
from session import Session, ready_draft, full_fields, parallel

V = 'after'
UP = REPO / 'scripts' / 'had-256' / 'local' / '.runtime' / V / 'site' / 'wp-content' / 'uploads'
BASE = 'http://127.0.0.1:9401'


def anon(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'Accept': '*/*'}), timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return 0, str(e).encode()


def is_image(b):
    from PIL import Image
    try:
        Image.open(io.BytesIO(b)).verify()
        return True
    except Exception:
        return False


def exposure(draft, refs):
    urls = []
    if UP.exists():
        for p in UP.rglob('*'):
            if p.is_file() and p.name not in ('index.php', '.htaccess'):
                urls.append(BASE + '/wp-content/uploads/' + p.relative_to(UP).as_posix())
    for r in refs:
        for s in ('t', 'f'):
            urls.append(BASE + '/wp-admin/admin-ajax.php?action=nl_owner_img&d=%d&r=%s&s=%s' % (draft, r, s))
    hits = []
    for u in urls:
        s, b = anon(u)
        if s == 200 and is_image(b):
            hits.append(u.replace(BASE, ''))
    return hits, len(urls)


def new_draft(sess, n=2, **over):
    d, rev = ready_draft(sess, photos=n, **over)
    j = sess.get('/owner/draft/%d' % d)[1]
    return d, rev, [p['ref'] for p in j['photos']]


def pub(sess, d, rev, key=None, **extra):
    body = {'request_key': key or str(uuid.uuid4()), 'rev': rev}
    body.update(extra)
    return sess.post('/owner/draft/%d/publish' % d, body)


def listing(d):
    st = state(V, d)
    res = st['drop'].get('nl_result')
    he = int(res['he_id']) if isinstance(res, dict) and res.get('he_id') else 0
    if not he:
        for o in st['options']:
            if o['option_name'] == 'nl_pub_%d_he' % d:
                import json
                he = int(json.loads(o['option_value'])['post'])
    props = {int(p['ID']): p['post_status'] for p in st['properties']}
    return he, props.get(he, '')


def save_desc(sess, d, extra):
    j = sess.get('/owner/draft/%d' % d)[1]
    f = j['fields']
    f['desc'] = f['desc'] + extra
    s, k = sess.post('/owner/draft/%d' % d, {'rev': j['rev'], 'fields': f, 'photos': [{'ref': p['ref']} for p in j['photos']], 'step': 'preview'})
    return k['rev']


def rec(title, ok, ev):
    record({'id': 'L03', 'variant': V, 'label': 'real-wp', 'title': 'public photos: ' + title, 'status': 'pass' if ok else 'fail', 'evidence': ev})


# 1) non-success paths: nothing public
reset(V)
s = Session(V).login('dana')
d, rev, refs = new_draft(s, 2, owner_ok=False)
r = pub(s, d, rev)
hits, n = exposure(d, refs)
rec('a publish refused by validation (422)', r[0] == 422 and not hits, {'publish': r[0], 'exposed': hits, 'checked': n})

reset(V)
s = Session(V).login('dana')
d, rev, refs = new_draft(s, 2)
pre, n0 = exposure(d, refs)
rev = save_desc(s, d, ' מתאים למשפחות.')
r = pub(s, d, rev)
he, st = listing(d)
hits, n = exposure(d, refs)
rec('a fair-housing hold (pending)', not pre and r[0] == 200 and st == 'pending' and not hits, {'before_publish_exposed': pre, 'publish': [r[0], r[1].get('state')], 'status': st, 'exposed': hits, 'checked': n})

reset(V)
a = Session(V).login('admin')
d, rev, refs = new_draft(a, 1)
r = pub(a, d, rev, test='1')
he, st = listing(d)
hits, n = exposure(d, refs)
rec("an admin's test run (stays a draft)", r[0] == 200 and st == 'draft' and not hits, {'publish': [r[0], r[1].get('state')], 'status': st, 'exposed': hits})

for where in ('row', 'claim_pending', 'fenced:owner_claim', 'status_write:draft', 'fenced:owner_content', 'fenced:owner_meta', 'fenced:owner_render', 'fenced:owner_status', 'status_write:publish'):
    reset(V)
    s = Session(V).login('dana')
    d, rev, refs = new_draft(s, 2)
    w, _, to = where.partition(':') if where.startswith('status_write') else (where, '', '')
    fault(V, 'kill', {'where': w, 'n': 1, 'to': to})
    r = pub(s, d, rev)
    he, st = listing(d)
    hits, n = exposure(d, refs)
    rec('killed at %s (before the publish commit)' % where, r[0] == 500 and st != 'publish' and not hits, {'killed': [r[0], r[1].get('where')], 'status': st, 'exposed': hits, 'checked': n})

# 2) killed after the 'publish' commit, before or during the copies: published without pictures (fail-closed), then repaired
for where in ('owner_before_media', 'attach_pending', 'fenced:attach'):
    reset(V)
    s = Session(V).login('dana')
    d, rev, refs = new_draft(s, 2)
    fault(V, 'ttl', {'secs': 3})
    fault(V, 'kill', {'where': where, 'n': 1})
    k = str(uuid.uuid4())
    a1 = pub(s, d, rev, key=k)
    he, st1 = listing(d)
    h1, _ = exposure(d, refs)
    time.sleep(4)
    a2 = pub(s, d, rev, key=k)
    he2, st2 = listing(d)
    h2, _ = exposure(d, refs)
    fault(V, 'ttl', None)
    ok = a1[0] == 500 and st1 == 'publish' and a2[0] == 200 and st2 == 'publish' and len([h for h in h2 if '/nl-listings/' in h]) >= 2
    rec('killed at %s (after the publish commit), then the retry' % where, ok, {'killed': [a1[0], a1[1].get('where')], 'status_after_kill': st1, 'exposed_after_kill (listing is published)': h1, 'retry': [a2[0], a2[1].get('state')], 'exposed_after_retry': len(h2)})

# 3) a run paused at the status commit past the TTL; run B takes over and publishes; A resumes and is fenced out
reset(V)
s = Session(V).login('dana')
d, rev, refs = new_draft(s, 1)
fault(V, 'ttl', {'secs': 3})
fault(V, 'pause', {'where': 'fenced:owner_status', 'secs': 7, 'n': 1})
k = str(uuid.uuid4())
out = {}
parallel([lambda: out.__setitem__('a', pub(s, d, rev, key=k)), lambda: (time.sleep(4.5), out.__setitem__('b', pub(s, d, rev, key=k)))])
he, st = listing(d)
hits, n = exposure(d, refs)
fault(V, 'ttl', None)
rec('run A paused at the status commit past the TTL, run B took over', out['b'][0] == 200 and st == 'publish' and hits, {'A': out['a'][0], 'B': out['b'][0], 'status': st, 'exposed (published)': len(hits)})

# 4) success, then every exit from 'publish' revokes, coming back restores
reset(V)
s = Session(V).login('dana')
d, rev, refs = new_draft(s, 2)
pub(s, d, rev)
he, st = listing(d)
steps = {'published': [st, len(exposure(d, refs)[0])]}
s.post('/owner/update', {'id': he, 'status': 'sold'})
steps['sold (stays published with a notice)'] = [listing(d)[1], len(exposure(d, refs)[0])]
s.post('/owner/update', {'id': he, 'status': 'active'})
s.post('/owner/update', {'id': he, 'action': 'remove'})
steps['removed (trash)'] = [listing(d)[1], len(exposure(d, refs)[0])]
s.post('/owner/update', {'id': he, 'action': 'republish'})
steps['published again'] = [listing(d)[1], len(exposure(d, refs)[0])]
rev2 = save_desc(s, d, ' מתאים למשפחות.')
pub(s, d, rev2)
steps['edited into a hold (pending)'] = [listing(d)[1], len(exposure(d, refs)[0])]
ok = steps['published'][1] >= 2 and steps['sold (stays published with a notice)'][1] >= 2 and steps['removed (trash)'][1] == 0 and steps['published again'][1] >= 2 and steps['edited into a hold (pending)'] == ['pending', 0]
rec('served when published; revoked on remove and on a hold; restored on publishing again', ok, steps)

# 5) killed right before the status row of a REMOVE is written: the copies are already gone (fail-closed), the next view repairs
reset(V)
s = Session(V).login('dana')
d, rev, refs = new_draft(s, 2)
pub(s, d, rev)
he, st = listing(d)
fault(V, 'kill', {'where': 'status_write', 'n': 1})
r = s.post('/owner/update', {'id': he, 'action': 'remove'})
he, st1 = listing(d)
h1, _ = exposure(d, refs)
anon(BASE + '/?p=%d' % he)      # a visitor opens the (still published) listing page
h2, _ = exposure(d, refs)
rec('killed between the withdraw and the remove status write', r[0] == 500 and st1 == 'publish' and not h1 and len(h2) >= 2,
    {'remove': r[0], 'status_after_kill': st1, 'exposed_after_kill': h1, 'exposed_after_a_view (published)': len(h2)})

# 6) the sealed private file itself, and the proxy
reset(V)
s = Session(V).login('dana')
d, rev, refs = new_draft(s, 1)
res = []
for p in UP.rglob('*.bin'):
    stt, b = anon(BASE + '/wp-content/uploads/' + p.relative_to(UP).as_posix())
    res.append({'path': '/wp-content/uploads/' + p.relative_to(UP).as_posix(), 'status': stt, 'opens_as_image': is_image(b), 'starts': b[:4].decode('latin-1')})
pr = anon(BASE + '/wp-admin/admin-ajax.php?action=nl_owner_img&d=%d&r=%s&s=f' % (d, refs[0]))
own = s.fetch('/wp-admin/admin-ajax.php?action=nl_owner_img&d=%d&r=%s&s=f' % (d, refs[0]))
other = Session(V).login('yoav').fetch('/wp-admin/admin-ajax.php?action=nl_owner_img&d=%d&r=%s&s=f' % (d, refs[0]))
ok = bool(res) and all(not x['opens_as_image'] for x in res) and pr[0] == 401 and own[0] == 200 and is_image(own[1]) and other[0] == 404
record({'id': 'L03', 'variant': V, 'label': 'real-wp', 'title': 'a draft photo: the sealed file (anonymous static GET) and the proxy (anonymous, owner, another user)', 'status': 'pass' if ok else 'fail',
        'evidence': {'sealed_files': res, 'proxy_anonymous': pr[0], 'proxy_owner': [own[0], is_image(own[1])], 'proxy_other_user': other[0]},
        'notes': 'Playground serves static files with no .htaccess, so the sealed .bin answers 200 here: its bytes are ciphertext (NLS1 header) and do not open as an image. The live server is not assumed to honour the deny-all .htaccess.'})
