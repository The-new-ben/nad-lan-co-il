"""Quick probe: one publish on each bench (AFTER through the journey's doors, BEFORE through the 1.0 doors)."""
import json
import sys
import uuid
from bench import reset, state, fault
from session import Session, ready_draft, before_drop, listings_of

which = sys.argv[1] if len(sys.argv) > 1 else 'after'
reset(which)
s = Session(which).login('dana')
if which == 'after':
    d, rev = ready_draft(s, photos=2)
    k = str(uuid.uuid4())
    r1 = s.post('/owner/draft/%d/publish' % d, {'request_key': k, 'rev': rev})
    r2 = s.post('/owner/draft/%d/publish' % d, {'request_key': k, 'rev': rev})
    r3 = s.post('/owner/draft/%d/publish' % d, {'request_key': k, 'rev': rev + 1})
    print('first', r1[0], json.dumps(r1[1], ensure_ascii=False)[:300])
    print('replay', r2[0], r2[1].get('replayed'), r2[1].get('he_id'))
    print('same key other rev', r3[0], r3[1].get('code'))
else:
    d = before_drop(s)
    r1 = s.post('/owner/build/%d' % d, {})
    print('build', r1[0], json.dumps(r1[1], ensure_ascii=False)[:300])
L = listings_of(which, d)
print('content rows', [(p['ID'], p['post_status'], p['post_name']) for p in L['content']], 'auto-drafts', len(L['auto_drafts']))
st = state(which, d)
print('drop meta', json.dumps({k: v for k, v in st.get('drop', {}).items() if k != 'nl_draft'}, ensure_ascii=False)[:600])
