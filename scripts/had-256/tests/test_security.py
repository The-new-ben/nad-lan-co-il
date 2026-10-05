"""L03 (and parts of L01/L02/L05/L07/L16) over HTTP on real WordPress (bench): two synthetic accounts and an anonymous
caller against every door of the journey, with real IDs of the other account and guessed ones.
"""
import json
import re
import time
import urllib.request
import uuid

from bench import reset, record, user, clear, mails, bench, base, fault
from session import Session, ready_draft, full_fields, jpeg_bytes

V = 'after'


def main():
    for i in ('L01', 'L02', 'L03', 'L05', 'L07', 'L16'):
        clear(i, V, 'http: ')
    reset(V)
    a = Session(V).login('dana')
    b = Session(V).login('yoav')
    anon = Session(V)
    anon.page()
    d, rev = ready_draft(a, photos=1)
    ja = a.get('/owner/draft/%d' % d)[1]
    ref = ja['photos'][0]['ref']
    pubk = str(uuid.uuid4())
    # B and anonymous against A's draft (real id) and guessed ids
    doors = [
        ('GET draft', lambda s, i: s.get('/owner/draft/%d' % i)),
        ('save', lambda s, i: s.post('/owner/draft/%d' % i, {'rev': 1, 'fields': full_fields(desc='SYNTHETIC-OVERWRITE-BY-B ' * 3), 'photos': [], 'step': 'details'})),
        ('check', lambda s, i: s.post('/owner/draft/%d/check' % i, {})),
        ('preview', lambda s, i: s.get('/owner/draft/%d/preview' % i)),
        ('publish', lambda s, i: s.post('/owner/draft/%d/publish' % i, {'request_key': pubk, 'rev': rev})),
        ('delete', lambda s, i: s.post('/owner/draft/%d/delete' % i, {})),
        ('restore', lambda s, i: s.post('/owner/draft/%d/restore' % i, {})),
        ('photo into it', lambda s, i: s.upload('/owner/photo', 'x.jpg', jpeg_bytes(), {'draft': i}, 'image/jpeg')),
        ('legacy build', lambda s, i: s.post('/owner/build/%d' % i, {})),
    ]
    rows = []
    for who, s in (('user B', b), ('anonymous', anon)):
        for name, fn in doors:
            for target in (d, d + 1, d + 7, 1):
                st, j = fn(s, target)
                rows.append({'who': who, 'door': name, 'id': target, 'status': st, 'code': j.get('code') if isinstance(j, dict) else None,
                             'leak': any(x in json.dumps(j, ensure_ascii=False) for x in ('שכונת הדוגמה', ref, user('dana')['email'])) if isinstance(j, dict) else False})
    proxy = [{'who': w, 'status': s.fetch('/wp-admin/admin-ajax.php?action=nl_owner_img&d=%d&r=%s&s=f' % (d, ref))[0]} for w, s in (('user B', b), ('anonymous', anon))]
    after = a.get('/owner/draft/%d' % d)[1]
    intact = after.get('rev') == rev and 'SYNTHETIC-OVERWRITE' not in after['fields']['desc'] and len(after['photos']) == 1
    bad = [r for r in rows if r['status'] in (200, 201, 202) or r['leak']]
    ok = not bad and all(p['status'] in (401, 404) for p in proxy) and intact
    record({'id': 'L03', 'variant': V, 'label': 'real-wp', 'title': "http: another account and an anonymous caller against every door of A's draft (real and guessed ids)", 'status': 'pass' if ok else 'fail',
            'evidence': {'requests': len(rows), 'allowed_or_leaking': bad, 'answers': sorted(set((r['who'], r['status'], r['code']) for r in rows)), 'photo_proxy': proxy, 'A_draft_intact': intact}})

    # My listings and listing updates of another account
    r = a.post('/owner/draft/%d/publish' % d, {'request_key': str(uuid.uuid4()), 'rev': rev})
    he = r[1]['he_id']
    upd = [b.post('/owner/update', {'id': he, 'status': 'sold'})[0], b.post('/owner/update', {'id': he, 'price': '1'})[0], b.post('/owner/update', {'id': he, 'action': 'remove'})[0], anon.post('/owner/update', {'id': he, 'action': 'remove'})[0]]
    mine_b = b.get('/owner/listings')[1]
    ok = all(x in (401, 404) for x in upd) and not mine_b.get('listings') and not mine_b.get('drafts')
    record({'id': 'L03', 'variant': V, 'label': 'real-wp', 'title': "http: another account cannot change or list A's published listing", 'status': 'pass' if ok else 'fail', 'evidence': {'updates_by_B_and_anonymous': upd, 'B_my_listings': {k: len(v) if isinstance(v, list) else v for k, v in mine_b.items()}}})

    # L07: a save on a stale revision is refused with the server's version (no silent last-write-wins)
    s1, j1 = a.post('/owner/draft', {'create_key': str(uuid.uuid4()), 'fields': full_fields(rooms='3'), 'step': 'details'})
    x1 = a.post('/owner/draft/%d' % j1['id'], {'rev': j1['rev'], 'fields': full_fields(rooms='4'), 'photos': [], 'step': 'details'})
    x2 = a.post('/owner/draft/%d' % j1['id'], {'rev': j1['rev'], 'fields': full_fields(rooms='5'), 'photos': [], 'step': 'details'})
    srv = a.get('/owner/draft/%d' % j1['id'])[1]
    ok = x1[0] == 200 and x2[0] == 409 and x2[1].get('code') == 'conflict' and (x2[1].get('data') or {}).get('server', {}).get('fields', {}).get('rooms') == '4' and srv['fields']['rooms'] == '4'
    record({'id': 'L07', 'variant': V, 'label': 'real-wp', 'title': 'http: two saves from the same revision: the second gets 409 with the server version; nothing is overwritten', 'status': 'pass' if ok else 'fail',
            'evidence': {'first': x1[0], 'second': [x2[0], x2[1].get('code')], 'server_rooms': srv['fields']['rooms']}})
    # parallel saves from the same revision: exactly one wins (compare-and-swap)
    from session import parallel
    s1, j2 = a.post('/owner/draft', {'create_key': str(uuid.uuid4()), 'fields': full_fields(rooms='3'), 'step': 'details'})
    res = parallel([lambda n=n: a.post('/owner/draft/%d' % j2['id'], {'rev': j2['rev'], 'fields': full_fields(rooms=str(n)), 'photos': [], 'step': 'details'}) for n in (4, 5, 6, 7, 8, 9)])
    codes = [x[0] for x in res]
    srv = a.get('/owner/draft/%d' % j2['id'])[1]
    winner = [x[1]['fields']['rooms'] for x in res if x[0] == 200]
    ok = codes.count(200) == 1 and codes.count(409) == 5 and srv['rev'] == j2['rev'] + 1 and winner == [srv['fields']['rooms']]
    record({'id': 'L07', 'variant': V, 'label': 'real-wp', 'title': 'http: 6 parallel saves from the same revision: one wins, five get 409', 'status': 'pass' if ok else 'fail', 'evidence': {'codes': codes, 'server_rev': srv['rev'], 'winner': winner, 'server_rooms': srv['fields']['rooms']}})

    # L05: a draft create whose answer was lost is the same draft on retry (create key)
    k = str(uuid.uuid4())
    c1 = a.post('/owner/draft', {'create_key': k, 'fields': full_fields(), 'step': 'details'})
    c2 = a.post('/owner/draft', {'create_key': k, 'fields': full_fields(), 'step': 'details'})
    ok = c1[0] == 201 and c2[0] == 200 and c2[1].get('replayed') and c1[1]['id'] == c2[1]['id']
    record({'id': 'L05', 'variant': V, 'label': 'real-wp', 'title': 'http: a draft created twice with the same key (an answer lost) is one draft', 'status': 'pass' if ok else 'fail', 'evidence': {'first': [c1[0], c1[1].get('id')], 'retry': [c2[0], c2[1].get('id'), c2[1].get('replayed')]}})

    # L01: recovery answers the same for a registered and an unknown email; only the registered one gets a mail
    reset(V)
    s = Session(V)
    t0 = time.time(); r1 = s.post('/owner/account/recover', {'email': user('dana')['email'], 'back': base(V) + '/post-listing/'}, nonce=False); t1 = time.time() - t0
    t0 = time.time(); r2 = s.post('/owner/account/recover', {'email': 'nobody.sample@example.test'}, nonce=False); t2 = time.time() - t0
    m = mails(V)
    ok = r1 == r2 or (r1[0] == r2[0] == 200 and r1[1] == r2[1])
    record({'id': 'L01', 'variant': V, 'label': 'real-wp', 'title': 'http: recovery gives one identical answer for a registered and an unknown email', 'status': 'pass' if ok and len(m) == 1 else 'fail',
            'evidence': {'registered': [r1[0], r1[1]], 'unknown': [r2[0], r2[1]], 'seconds': [round(t1, 2), round(t2, 2)], 'mails_in_sink': [x['to'] for x in m]},
            'notes': 'opening an account with an email that has one answers 409 "exists" (as the existing quick-register and auth-signup doors do): the design keeps that, so the journey does not claim blanket non-enumeration'})

    # L16: the old doors and the broker redirect, the promotion has no payment door
    reset(V)
    a = Session(V).login('dana')
    old = [Session(V).post(p, {}, nonce=False)[0] for p in ('/listing-ai-draft', '/listing-submit', '/listing-photo')]
    br = a.post('/owner/submit', {'who': 'broker'})
    sub = a.post('/owner/submit', {'who': 'owner', 'text': 'x'})
    routes = json.loads(urllib.request.urlopen(base(V) + '/wp-json/').read().decode('utf-8')).get('routes', {})
    owner_routes = sorted(r for r in routes if r.startswith('/nadlan/v1/owner'))
    pay = [r for r in owner_routes if re.search(r'promo|pay|charge|checkout|order|price', r)]
    ok = old == [410, 410, 410] and br[1].get('state') == 'broker' and sub[0] == 410 and not pay
    record({'id': 'L16', 'variant': V, 'label': 'real-wp', 'title': 'http: the 1.x doors answer 410, brokers are sent to /brokers/, the owner routes have no payment door', 'status': 'pass' if ok else 'fail',
            'evidence': {'first_wizard_doors': old, 'broker': br[1], 'owner_submit_1x': sub[0], 'owner_routes': owner_routes, 'payment_like_routes': pay}})


if __name__ == '__main__':
    main()
