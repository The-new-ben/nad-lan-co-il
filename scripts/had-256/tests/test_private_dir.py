"""Draft photos stored OUTSIDE the web root (NL_OWNER_PRIVATE_DIR), on the 'private' bench (127.0.0.1:9431):
the files land in the folder mounted at /nl-private (beside /wordpress, so no URL maps to it), nothing of the draft
lands under wp-content/uploads, the owner still sees the photo through the account-checked route, and publishing
still makes the public copy. Real WordPress (Playground); the live host's path is main's choice (see README).
"""
import io
import urllib.request
import uuid

from PIL import Image

from bench import record, clear, REPO, http
from session import Session, ready_draft

ROOT = REPO / 'scripts' / 'had-256' / 'local' / '.runtime' / 'private'
BASE = 'http://127.0.0.1:9431'


class S(Session):
    def __init__(self):
        super().__init__('after')
        self.base = BASE


def opens(b):
    try:
        Image.open(io.BytesIO(b)).verify()
        return True
    except Exception:
        return False


def main():
    clear('L03', 'after', 'draft photos outside the web root')
    http('POST', BASE + '/?rest_route=/nlj-test/v1/reset', {})
    s = S()
    s.login('dana')
    d, rev = ready_draft(s, photos=1)
    ref = s.get('/owner/draft/%d' % d)[1]['photos'][0]['ref']
    outside = [p for p in (ROOT / 'outside').rglob('*') if p.is_file() and ref in p.name]
    inside = [p for p in (ROOT / 'site' / 'wp-content' / 'uploads').rglob('*') if p.is_file() and ref in p.name]
    own = s.fetch('/wp-admin/admin-ajax.php?action=nl_owner_img&d=%d&r=%s&s=f' % (d, ref))
    guesses = []
    for path in ['/nl-private/', '/wp-content/uploads/nl-private/', '/../nl-private/']:
        for f in outside:
            u = BASE + path + f.relative_to(ROOT / 'outside').as_posix()
            raw = f.read_bytes()
            try:
                with urllib.request.urlopen(u, timeout=10) as r:
                    body = r.read()
                    guesses.append({'url': u.replace(BASE, ''), 'final_url': r.geturl().replace(BASE, ''), 'status': r.status, 'served_the_stored_file': body == raw or raw[:64] in body, 'opens_as_image': opens(body)})
            except urllib.error.HTTPError as e:
                guesses.append({'url': u.replace(BASE, ''), 'status': e.code, 'served_the_stored_file': False, 'opens_as_image': False})
    r = s.post('/owner/draft/%d/publish' % d, {'request_key': str(uuid.uuid4()), 'rev': rev})
    pub = [p for p in (ROOT / 'site' / 'wp-content' / 'uploads' / 'nl-listings').glob(ref + '*')]
    ok = outside and not inside and own[0] == 200 and opens(own[1]) and not any(g['served_the_stored_file'] or g['opens_as_image'] for g in guesses) and r[0] == 200 and pub
    record({'id': 'L03', 'variant': 'after', 'label': 'real-wp', 'title': 'draft photos outside the web root (NL_OWNER_PRIVATE_DIR): stored there only, no URL reaches them, the owner and the publish still work', 'status': 'pass' if ok else 'fail',
            'evidence': {'files_outside_webroot': [p.name for p in outside], 'draft_files_under_uploads': [p.name for p in inside], 'owner_route': own[0], 'anonymous_url_guesses': guesses, 'publish': r[0], 'public_copy_after_publish': [p.name for p in pub]}})


if __name__ == '__main__':
    main()
