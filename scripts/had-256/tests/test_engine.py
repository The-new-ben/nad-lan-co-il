"""L08 (and the quota part of the contract) on real WordPress (Playground, SQLite, 6 PHP workers), synthetic data.

AFTER: see engine_after.py. (Kept for the record: replay, the same key with another revision, parallel publishes (same key, other keys),
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
    import runpy
    runpy.run_path('engine_after.py', run_name='__main__')   # the AFTER pressure lives in engine_after.py
if 'before' in RUN:
    before_tests()
