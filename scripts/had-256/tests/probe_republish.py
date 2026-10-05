"""Probe: the public files and the thumbnail after publish, remove, publish again."""
import json
import uuid
from bench import reset, state, REPO
from session import Session, ready_draft

V = 'after'
UP = REPO / 'scripts' / 'had-256' / 'local' / '.runtime' / V / 'site' / 'wp-content' / 'uploads' / 'nl-listings'
reset(V)
s = Session(V).login('dana')
d, rev = ready_draft(s, photos=2)
r = s.post('/owner/draft/%d/publish' % d, {'request_key': str(uuid.uuid4()), 'rev': rev})
he = r[1]['he_id']
print('published', sorted(p.name for p in UP.glob('*')))
s.post('/owner/update', {'id': he, 'status': 'sold'}); s.post('/owner/update', {'id': he, 'status': 'active'})
s.post('/owner/update', {'id': he, 'action': 'remove'})
print('removed', sorted(p.name for p in UP.glob('*')))
x = s.post('/owner/update', {'id': he, 'action': 'republish'})
print('republish', x)
print('again', sorted(p.name for p in UP.glob('*')))
st = state(V, d)
print([ (a['ID'], a['post_status'], a['post_parent']) for a in st['attachments']])
print([o['option_name'] for o in st['options']])
