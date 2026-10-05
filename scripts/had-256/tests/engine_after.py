"""L08 on the AFTER code, real WordPress (Playground, SQLite, 6 PHP workers), synthetic data.

Two code paths, each under pressure, and every fault is PROVEN to have fired (the bench's fault log, or the killed
answer), so a fault that never triggers cannot pass as a result:
  J = the owner journey's publish (nl_owner_rest_publish -> nl_owner_build), checkpoints owner_*;
  E = x-broker-drop's shared engine (nl_drop_build), reached through the 1.x owner door /owner/build/<drop> that 2.0
      keeps for drops made before the release (the broker /drop/<token> door runs the same function).
For each: parallel requests, a kill at every step, a run paused right AFTER each check (fence) and BEFORE its write,
past the lock TTL, while a second run takes over; then the rows: exactly one listing per drop and language, the
committed result points at it, an empty placeholder never carries owner content.
"""
import json
import time
import uuid

from bench import reset, fault, state, record, bench, clear, user
from session import Session, ready_draft, listings_of, parallel

V = 'after'
TTL = 3


def clean_auto(rows):
    return all(p['post_title'].startswith('nl-drop-') and int(p['meta_n']) == 0 for p in rows)


def summary(L):
    return {'content': [(p['ID'], p['post_status'], p['post_name']) for p in L['content']], 'empty_placeholders': [(p['ID'], p['post_title'], p['meta_n']) for p in L['auto_drafts']], 'claims': [c['option_name'] for c in L['claims']]}


def fired(where, kind):
    log = state(V).get('faults_log', '')
    return [l for l in log.splitlines() if (kind + ' ') in l and where in l]


def result_id(d):
    r = state(V, d)['drop'].get('nl_result')
    return int(r['he_id']) if isinstance(r, dict) and r.get('he_id') else 0


class J:
    name = 'journey publish'

    def __init__(self):
        self.s = Session(V).login('dana')
        self.d, self.rev = ready_draft(self.s, photos=1)
        self.key = str(uuid.uuid4())

    def go(self, key=None):
        return self.s.post('/owner/draft/%d/publish' % self.d, {'request_key': key or self.key, 'rev': self.rev})


class E:
    name = 'engine build (1.x door)'

    def __init__(self):
        self.s = Session(V).login('dana')
        self.d = bench(V, '/legacy-drop', {'email': user('dana')['email']})[1]['drop']

    def go(self, key=None):
        return self.s.post('/owner/build/%d' % self.d, {})


def rec(path, title, ok, ev):
    record({'id': 'L08', 'variant': V, 'label': 'real-wp', 'title': '%s: %s' % (path.name, title), 'status': 'pass' if ok else 'fail', 'evidence': ev})


def ok_rows(L, d):
    rid = result_id(d)
    return len(L['content']) == 1 and int(L['content'][0]['ID']) == rid and clean_auto(L['auto_drafts'])


def journey_basics():
    reset(V)
    j = J()
    r1 = j.go()
    r2 = j.go()
    r3 = j.go(str(uuid.uuid4()))
    r4 = j.s.post('/owner/draft/%d/publish' % j.d, {'request_key': j.key, 'rev': j.rev + 1})
    L = listings_of(V, j.d)
    ok = r1[0] == 200 and r2[0] == 200 and r2[1].get('replayed') and r2[1]['he_id'] == r1[1]['he_id'] and r3[0] == 200 and r3[1]['he_id'] == r1[1]['he_id'] and r4[0] == 409 and r4[1].get('code') == 'key_reused' and ok_rows(L, j.d)
    rec(J, 'the same key again, a new key, the same key with another revision', ok, {'first': r1[0], 'same_key': [r2[0], r2[1].get('replayed')], 'new_key': [r3[0], r3[1].get('he_id')], 'key_other_rev': [r4[0], r4[1].get('code')], 'rows': summary(L)})
    # validation failures never cost a publish
    reset(V)
    s = Session(V).login('dana')
    d, rev = ready_draft(s, photos=1, owner_ok=False)
    bad = [s.post('/owner/draft/%d/publish' % d, {'request_key': str(uuid.uuid4()), 'rev': rev})[0] for _ in range(10)]
    js = s.get('/owner/draft/%d' % d)[1]
    f = js['fields']
    f['owner_ok'] = True
    j2 = s.post('/owner/draft/%d' % d, {'rev': js['rev'], 'fields': f, 'photos': [{'ref': p['ref']} for p in js['photos']], 'step': 'preview'})[1]
    good = s.post('/owner/draft/%d/publish' % d, {'request_key': str(uuid.uuid4()), 'rev': j2['rev']})
    rec(J, '10 publishes refused by validation, then a valid one (the publish quota is not spent)', all(c == 422 for c in bad) and good[0] == 200, {'refused': bad, 'valid': [good[0], good[1].get('state')]})


def parallel_runs(P, mode):
    reset(V)
    p = P()
    fault(V, 'slow', {'secs': 1.5})
    keys = [p.key if hasattr(p, 'key') else None] * 4 if mode == 'same key' else [str(uuid.uuid4()) for _ in range(4)]
    t0 = time.time()
    res = parallel([lambda k=k: p.go(k) for k in keys])
    fault(V, 'slow', None)
    time.sleep(0.5)
    final = p.go(keys[0])
    L = listings_of(V, p.d)
    codes = [r[0] for r in res]
    rec(P, '4 parallel requests, %s' % mode, ok_rows(L, p.d) and final[0] == 200 and all(c in (200, 202, 409) for c in codes),
        {'codes': codes, 'seconds': round(time.time() - t0, 2), 'final': final[0], 'rows': summary(L)})


def kill_at(P, where):
    reset(V)
    p = P()
    fault(V, 'ttl', {'secs': TTL})
    fault(V, 'kill', {'where': where, 'n': 1})
    a = p.go()
    killed = a[0] == 500 and a[1].get('code') == 'nlj_killed'
    mid = listings_of(V, p.d)
    time.sleep(TTL + 1.5)
    b = p.go()
    for _ in range(5):
        if b[0] in (202, 409):
            time.sleep(2)
            b = p.go()
    L = listings_of(V, p.d)
    fault(V, 'ttl', None)
    fault(V, 'kill', None)
    rec(P, 'killed at %s, retried after the TTL' % where, killed and b[0] == 200 and ok_rows(L, p.d),
        {'kill_fired': killed, 'killed_answer': [a[0], a[1].get('where')], 'rows_after_kill': summary(mid), 'retry': b[0], 'rows': summary(L), 'nl_result': result_id(p.d), 'takeover': state(V, p.d)['drop'].get('nl_lock_takeover')})


def pause_at(P, where):
    reset(V)
    p = P()
    fault(V, 'ttl', {'secs': TTL})
    fault(V, 'pause', {'where': where, 'secs': 8, 'n': 1})
    out = {}
    parallel([lambda: out.__setitem__('a', p.go()), lambda: (time.sleep(TTL + 1.5), out.__setitem__('b', p.go()))])
    time.sleep(0.5)
    final = p.go()
    L = listings_of(V, p.d)
    fl = fired(where, 'PAUSE')
    st = state(V, p.d)
    fault(V, 'ttl', None)
    fault(V, 'pause', None)
    ok = bool(fl) and out['b'][0] == 200 and final[0] == 200 and ok_rows(L, p.d)
    rec(P, 'A paused right after the check at %s, past the TTL; B took over; A resumed' % where, ok,
        {'pause_fired': fl, 'A': [out['a'][0], (out['a'][1] or {}).get('state') or (out['a'][1] or {}).get('code')], 'B': out['b'][0], 'final': final[0], 'rows': summary(L),
         'takeover': st['drop'].get('nl_lock_takeover'), 'fence': st['drop'].get('nl_fence')})


def stale_status(where):
    """A (revision 1, target publish) pauses right before its status write; the owner edits the draft into a fair-housing
    hold; B publishes revision 2 (target pending) after the TTL; A resumes: its status write must fail (fenced), the
    listing stays pending, and no public photo exists."""
    reset(V)
    j = J()
    fault(V, 'ttl', {'secs': TTL})
    fault(V, 'pause', {'where': where, 'secs': 10, 'n': 1})
    out = {}

    def run_b():
        time.sleep(TTL + 1.5)
        js = j.s.get('/owner/draft/%d' % j.d)[1]
        f = js['fields']
        f['desc'] = f['desc'] + ' מתאים למשפחות.'
        sv = j.s.post('/owner/draft/%d' % j.d, {'rev': js['rev'], 'fields': f, 'photos': [{'ref': p['ref']} for p in js['photos']], 'step': 'preview'})
        out['save'] = sv[0]
        out['b'] = j.s.post('/owner/draft/%d/publish' % j.d, {'request_key': str(uuid.uuid4()), 'rev': sv[1].get('rev')})
    parallel([lambda: out.__setitem__('a', j.go()), run_b])
    time.sleep(0.5)
    st = state(V, j.d)
    L = listings_of(V, j.d)
    status = L['content'][0]['post_status'] if L['content'] else None
    pub_files = [a for a in st['attachments'] if a['post_status'] == 'inherit']
    fl = fired(where, 'PAUSE')
    fault(V, 'ttl', None)
    fault(V, 'pause', None)
    ok = bool(fl) and out['a'][0] == 202 and out['b'][0] == 200 and status == 'pending' and len(L['content']) == 1 and not pub_files
    rec(J, 'A paused right before its status write (%s); the draft moved into a hold; B committed pending; A could not publish' % where, ok,
        {'pause_fired': fl, 'A': [out['a'][0], out['a'][1].get('state')], 'save_during': out.get('save'), 'B': [out['b'][0], out['b'][1].get('state')], 'listing_status': status, 'public_attachments': pub_files, 'rows': summary(L)})


if __name__ == '__main__':
    clear('L08', V)
    journey_basics()
    for P in (J, E):
        parallel_runs(P, 'same key')
        parallel_runs(P, 'different keys')
    for w in ('row', 'before_claim', 'claim_pending', 'fenced:owner_claim', 'fenced:owner_content', 'fenced:owner_meta', 'fenced:owner_render', 'fenced:owner_status', 'owner_before_media', 'fenced:attach', 'attach_pending'):
        kill_at(J, w)
    for w in ('fenced:owner_drop_meta', 'fenced:owner_claim', 'before_claim', 'claim_pending', 'fenced:owner_content', 'fenced:owner_meta', 'fenced:owner_render', 'fenced:owner_status', 'fenced:attach', 'fenced:media_meta'):
        pause_at(J, w)
    for w in ('fenced:owner_status', 'owner_status_sql'):
        stale_status(w)
    for w in ('row', 'claim_pending', 'fenced:claim', 'fenced:content', 'row_meta', 'fenced:before_meta', 'fenced:before_render'):
        kill_at(E, w)
    for w in ('fenced:claim', 'before_claim', 'claim_pending', 'fenced:content', 'fenced:before_meta', 'fenced:before_render'):
        pause_at(E, w)
