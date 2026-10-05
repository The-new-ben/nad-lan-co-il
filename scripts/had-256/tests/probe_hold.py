"""Probe: publish, edit into a hold, fix, publish again; the listing row after each step."""
import json
import urllib.request
import uuid
from bench import reset, state, base
from session import Session, ready_draft

V = 'after'
reset(V)
s = Session(V).login('dana')
d, rev = ready_draft(s, photos=1)


def pub(rev):
    return s.post('/owner/draft/%d/publish' % d, {'request_key': str(uuid.uuid4()), 'rev': rev})


def edit(extra=None, desc=None):
    j = s.get('/owner/draft/%d' % d)[1]
    f = j['fields']
    f['desc'] = desc if desc else f['desc'] + extra
    return s.post('/owner/draft/%d' % d, {'rev': j['rev'], 'fields': f, 'photos': [{'ref': p['ref']} for p in j['photos']], 'step': 'preview'})[1]['rev']


def row(tag):
    st = state(V, d)
    p = [x for x in st['properties'] if x['post_status'] != 'auto-draft']
    url = (st['drop'].get('nl_result') or {}).get('url_he')
    try:
        code = urllib.request.urlopen(base(V) + '/?p=%s' % p[0]['ID'], timeout=20).status if p else None
    except urllib.error.HTTPError as e:
        code = e.code
    print(tag, [(x['ID'], x['post_status'], x['post_name']) for x in p], 'result', st['drop'].get('nl_state'), 'http', code)


r = pub(rev); print('pub1', r[0], r[1].get('state')); row('after publish')
r = pub(edit(' מתאים למשפחות.')); print('pub2', r[0], r[1].get('state'), r[1].get('code'), r[1].get('data')); row('after hold')
r = pub(edit(desc='דירה מוארת בקומה שלישית, מרפסת שמש. חניה ומחסן.')); print('pub3', r[0], r[1].get('state'), r[1].get('code'), r[1].get('data')); row('after fix')
