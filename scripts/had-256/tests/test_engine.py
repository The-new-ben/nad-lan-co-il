"""L08 (and the quota part of the contract) on real WordPress (Playground, SQLite, 6 PHP workers), synthetic data.

AFTER (this worktree, :9401): replay, the same key with another revision, parallel publishes (same key, other keys),
a kill at every step of the build (placeholder insert, before the claim, after the claim, between the row and its
meta, before the page, before the commit), a pause past the lock TTL at every check-to-write gap with a second run
taking over (fencing), validation failures that never cost a publish.
BEFORE (6e9cf930, :9411): the same pressure on the 1.0.0 doors, to show what the old code does.

    python test_engine.py            # both
    python test_engine.py after
"""
import json
import sys
import time
import uuid

from bench import reset, fault, state, record, bench
from session import Session, ready_draft, before_drop, listings_of, parallel

RUN = sys.argv[1:] or ['after', 'before']
TTL = 3


def pub(sess, d, key, rev):
    return sess.post('/owner/draft/%d/publish' % d, {'request_key': key, 'rev': rev})


def clean_auto(rows):
    """an empty placeholder: no owner content (technical title, no meta rows)"""
    return all(p['post_title'].startswith('nl-drop-') and int(p['meta_n']) == 0 for p in rows)


def summary(L):
    return {'content': [(p['ID'], p['post_status'], p['post_name']) for p in L['content']], 'auto_drafts': [(p['ID'], p['post_title'], p['meta_n']) for p in L['auto_drafts']], 'claims': [c['option_name'] for c in L['claims']]}


def after_tests():
    V = 'after'
    # E1 replay + E2 same key other revision
    reset(V)
    s = Session(V).login('dana')
    d, rev = ready_draft(s, photos=2)
    k = str(uuid.uuid4())
    r1 = pub(s, d, k, rev)
    r2 = pub(s, d, k, rev)
    r3 = pub(s, d, str(uuid.uuid4()), rev)
    r4 = pub(s, d, k, rev + 1)
    L = listings_of(V, d)
    ok = r1[0] == 200 and r2[0] == 200 and r2[1].get('replayed') and r2[1]['he_id'] == r1[1]['he_id'] and r3[0] == 200 and r3[1]['he_id'] == r1[1]['he_id'] and r4[0] == 409 and r4[1].get('code') == 'key_reused' and len(L['content']) == 1
    record({'id': 'L08', 'variant': V, 'label': 'real-wp', 'title': 'double submit: the same key again, a new key, the same key with another revision', 'status': 'pass' if ok else 'fail',
            'evidence': {'first': r1[0], 'same_key': [r2[0], r2[1].get('replayed')], 'new_key': [r3[0], r3[1].get('he_id')], 'key_other_rev': [r4[0], r4[1].get('code')], 'rows': summary(L)}})

    # E3 parallel, same key / E4 parallel, different keys
    for mode in ('same key', 'different keys'):
        reset(V)
        s = Session(V).login('dana')
        d, rev = ready_draft(s, photos=1)
        fault(V, 'slow', {'secs': 1.5})
        keys = [str(uuid.uuid4())] * 4 if mode == 'same key' else [str(uuid.uuid4()) for _ in range(4)]
        t0 = time.time()
        res = parallel([lambda k=k: pub(s, d, k, rev) for k in keys])
        took = time.time() - t0
        fault(V, 'slow', None)
        final = pub(s, d, keys[0], rev)
        L = listings_of(V, d)
        codes = [r[0] for r in res]
        ok = len(L['content']) == 1 and final[0] == 200 and all(c in (200, 202) for c in codes) and not L['auto_drafts']
        record({'id': 'L08', 'variant': V, 'label': 'real-wp', 'title': '4 parallel publishes, %s' % mode, 'status': 'pass' if ok else 'fail',
                'evidence': {'codes': codes, 'seconds': round(took, 2), 'final': [final[0], final[1].get('he_id')], 'rows': summary(L)}})

    # E5 a kill at every step, then a retry after the TTL
    for where in ('row', 'claim_pending', 'fenced:content', 'row_meta', 'fenced:before_render'):
        reset(V)
        s = Session(V).login('dana')
        d, rev = ready_draft(s, photos=1)
        fault(V, 'ttl', {'secs': TTL})
        fault(V, 'kill', {'where': where, 'n': 1})
        k = str(uuid.uuid4())
        a = pub(s, d, k, rev)
        mid = listings_of(V, d)
        time.sleep(TTL + 1.5)
        b = pub(s, d, k, rev)
        if b[0] == 202:
            time.sleep(2)
            b = pub(s, d, k, rev)
        L = listings_of(V, d)
        st = state(V, d)['drop']
        res_id = (st.get('nl_result') or {}).get('he_id') if isinstance(st.get('nl_result'), dict) else None
        ok = a[0] == 500 and a[1].get('code') == 'nlj_killed' and b[0] == 200 and len(L['content']) == 1 and int(L['content'][0]['ID']) == int(res_id or 0) and clean_auto(L['auto_drafts'])
        record({'id': 'L08', 'variant': V, 'label': 'real-wp', 'title': 'killed at %s, retried after the lock TTL' % where, 'status': 'pass' if ok else 'fail',
                'evidence': {'killed': [a[0], a[1].get('where')], 'rows_after_kill': summary(mid), 'retry': [b[0], b[1].get('he_id'), b[1].get('state')], 'rows': summary(L), 'nl_result': res_id, 'takeover': st.get('nl_lock_takeover'), 'fence': st.get('nl_fence')}})
    fault(V, 'ttl', None)

    # E6 a run paused right after a check, past the TTL; a second run takes over; the first resumes
    for where in ('fenced:claim', 'claim_pending', 'fenced:content', 'fenced:before_meta', 'fenced:before_render'):
        reset(V)
        s = Session(V).login('dana')
        d, rev = ready_draft(s, photos=1)
        fault(V, 'ttl', {'secs': TTL})
        fault(V, 'pause', {'where': where, 'secs': 8, 'n': 1})
        k = str(uuid.uuid4())
        out = {}

        def run_a():
            out['a'] = pub(s, d, k, rev)

        def run_b():
            time.sleep(TTL + 1.5)
            out['b'] = pub(s, d, k, rev)
        parallel([run_a, run_b])
        time.sleep(0.5)
        final = pub(s, d, k, rev)
        L = listings_of(V, d)
        st = state(V, d)
        dm = st['drop']
        res = dm.get('nl_result') if isinstance(dm.get('nl_result'), dict) else {}
        ok = out['b'][0] == 200 and out['a'][0] in (202, 200) and len(L['content']) == 1 and int(L['content'][0]['ID']) == int(res.get('he_id', 0)) and final[0] == 200 and clean_auto(L['auto_drafts'])
        record({'id': 'L08', 'variant': V, 'label': 'real-wp', 'title': 'run A paused at %s past the TTL, run B took over, A resumed' % where, 'status': 'pass' if ok else 'fail',
                'evidence': {'A': [out['a'][0], out['a'][1].get('state') or out['a'][1].get('code')], 'B': [out['b'][0], out['b'][1].get('he_id')], 'final': [final[0], final[1].get('he_id')], 'rows': summary(L), 'takeover': dm.get('nl_lock_takeover'), 'fence': dm.get('nl_fence'),
                             'log': [l for l in st.get('faults_log', '').splitlines() if 'PAUSE' in l or 'RESUME' in l]}})
    fault(V, 'ttl', None)
    fault(V, 'pause', None)

    # quotas: validation failures never cost a publish; the abuse counter is separate
    reset(V)
    s = Session(V).login('dana')
    d, rev = ready_draft(s, photos=1, owner_ok=False)
    bad = [pub(s, d, str(uuid.uuid4()), rev)[0] for _ in range(10)]
    st, j = s.get('/owner/draft/%d' % d)
    fields = j['fields']
    fields['owner_ok'] = True
    s2, j2 = s.post('/owner/draft/%d' % d, {'rev': j['rev'], 'fields': fields, 'photos': [{'ref': p['ref']} for p in j['photos']], 'step': 'preview'})
    good = pub(s, d, str(uuid.uuid4()), j2['rev'])
    ok = all(c == 422 for c in bad) and good[0] == 200
    record({'id': 'L08', 'variant': V, 'label': 'real-wp', 'title': '10 publishes refused by validation, then a valid one (the publish quota is not spent)', 'status': 'pass' if ok else 'fail',
            'evidence': {'refused': bad, 'valid': [good[0], good[1].get('state')]}})


def before_tests():
    V = 'before'
    # B1 the same send twice: a new drop each time (owner-wizard.php:162)
    reset(V)
    s = Session(V).login('dana')
    d1 = before_drop(s)
    d2 = before_drop(s)
    record({'id': 'L08', 'variant': V, 'label': 'real-wp', 'title': 'the same send twice', 'status': 'fail' if d1 != d2 else 'pass',
            'evidence': {'drops': [d1, d2]}, 'notes': 'two submissions of the same listing: 1.0.0 creates a new drop on every submit'})
    # B2 4 parallel builds of one drop (the 1.0.0 owner door), with the bench's slow-save widening the window
    reset(V)
    s = Session(V).login('dana')
    d = before_drop(s)
    bench(V, '/drop-ready', {'drop': d})   # the facts an AI would have read from the text (AI is off on the bench)
    fault(V, 'slow', {'secs': 1.5})
    res = parallel([lambda: s.post('/owner/build/%d' % d, {}) for _ in range(4)])
    fault(V, 'slow', None)
    L = listings_of(V, d)
    record({'id': 'L08', 'variant': V, 'label': 'real-wp', 'title': '4 parallel builds of one drop', 'status': 'pass' if len(L['content']) == 1 else 'fail',
            'evidence': {'codes': [r[0] for r in res], 'rows': summary(L)}, 'notes': 'more than one row = the duplicate the contract warned about (broker-drop.php:2027/2057/2168). The AI reading of the text is replaced by the bench (drop-ready); the build is the real 1.1.3 code.'})
    # B3 killed between the listing row and its meta, then built again
    reset(V)
    s = Session(V).login('dana')
    d = before_drop(s)
    bench(V, '/drop-ready', {'drop': d})
    fault(V, 'kill', {'where': 'row_meta', 'n': 1})
    a = s.post('/owner/build/%d' % d, {})
    b = s.post('/owner/build/%d' % d, {})
    L = listings_of(V, d)
    record({'id': 'L08', 'variant': V, 'label': 'real-wp', 'title': 'killed between the listing row and its meta, then built again', 'status': 'pass' if len(L['content']) == 1 else 'fail',
            'evidence': {'killed': a[0], 'retry': [b[0], b[1].get('he_id') if isinstance(b[1], dict) else None], 'rows': summary(L)}})
    # B4 the submit quota is spent before validation (owner-wizard.php:132)
    reset(V)
    s = Session(V).login('dana')
    bad = [s.post('/owner/submit', {'text': 'x', 'photos': [], 'name': '', 'phone': '', 'who': 'owner'})[0] for _ in range(8)]
    good = s.post('/owner/submit', {'text': 'למכירה, 4 חדרים, 96 מ״ר, שכונת הדוגמה, תל אביב יפו. 3,450,000 ש״ח.', 'photos': [], 'name': 'דנה', 'phone': '050-0000000', 'who': 'owner', 'owner': '1', 'consent': '1'})
    record({'id': 'L08', 'variant': V, 'label': 'real-wp', 'title': '8 sends refused by validation, then a valid one', 'status': 'pass' if good[0] != 429 else 'fail',
            'evidence': {'refused': bad, 'valid': [good[0], good[1].get('code') if isinstance(good[1], dict) else None]}, 'notes': '429 on the valid send = validation failures spent the publish quota'})


if 'after' in RUN:
    after_tests()
if 'before' in RUN:
    before_tests()
