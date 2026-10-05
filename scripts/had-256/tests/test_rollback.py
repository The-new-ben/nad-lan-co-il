"""L17 rollback drill on real WordPress (Playground), one site with its own data on 127.0.0.1:9421:
  1. the new code (2.0.0 + engine 1.1.4): an owner publishes a listing and leaves a second draft unfinished;
  2. the SAME site restarted with the base code of 6e9cf930 (the rollback): the site works, the 1.0 tool loads for the
     owner, the published listing still renders, the 2.0 drafts are still there (private nadlan_drop posts), no PHP fatal;
  3. the new code again (roll forward): the unfinished draft resumes with its fields and photos, the listing is intact.
2.0 adds post meta and option rows only (no table or column), so a rollback keeps the data; the 1.0 code ignores it.
"""
import json
import pathlib
import re
import subprocess
import time
import urllib.request
import uuid

from bench import record, clear, REPO, http
from session import Session, ready_draft, full_fields, jpeg_bytes

HERE = REPO / 'scripts' / 'had-256'
ROLL = HERE / 'local' / '.runtime' / 'roll'
PORT = 9421
BASE = 'http://127.0.0.1:%d' % PORT


def start(code):
    log = open(ROLL / ('start-%s.log' % code), 'w')
    p = subprocess.Popen(['node', str(HERE / 'local' / 'start.mjs'), 'roll', code], cwd=str(REPO), stdout=log, stderr=subprocess.STDOUT)
    for _ in range(240):
        time.sleep(1)
        if 'ready:' in (ROLL / ('start-%s.log' % code)).read_text(encoding='utf-8', errors='replace'):
            break
    for _ in range(20):
        try:
            urllib.request.urlopen(BASE + '/post-listing/', timeout=20).read()
            break
        except Exception:
            time.sleep(1)
    return p


def stop(p):
    subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
    for _ in range(30):
        r = subprocess.run(['powershell', '-NoProfile', '-Command', '(Get-NetTCPConnection -LocalPort %d -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1).OwningProcess' % PORT], capture_output=True, text=True)
        pid = r.stdout.strip()
        if not pid:
            return
        subprocess.run(['taskkill', '/PID', pid, '/T', '/F'], capture_output=True)
        time.sleep(1)


class S(Session):
    def __init__(self, ip=None):
        super().__init__('after', ip)
        self.base = BASE


def main():
    clear('L17', 'after')
    ROLL.mkdir(parents=True, exist_ok=True)
    import shutil
    if (ROLL / 'site').exists():
        shutil.rmtree(ROLL / 'site')
    ev = {}
    # 1. the new code
    p = start('after')
    a = S()
    a.v = 'after'
    a.login('dana')
    d1, rev1 = ready_draft(a, photos=1)
    r = a.post('/owner/draft/%d/publish' % d1, {'request_key': str(uuid.uuid4()), 'rev': rev1})
    url = r[1].get('url')
    d2, rev2 = ready_draft(a, photos=2, desc='טיוטה שנשארה פתוחה לפני החזרה לאחור, עם מרפסת ומחסן.')
    ev['new_code'] = {'published': [r[0], url], 'open_draft': d2}
    stop(p)
    # 2. rollback: the base code on the same data
    p = start('before')
    s, html = 0, ''
    page = urllib.request.urlopen(url, timeout=30)
    listing_ok = page.status == 200 and 'nlx' in page.read().decode('utf-8', 'replace')
    b = S()
    b.v = 'before'
    b.login('dana')
    st, tool = b.page()
    tool_ok = 'nlow-f' in tool and 'nlj-app' not in tool
    mine = b.get('/owner/listings')[1]
    drafts = json.loads(urllib.request.urlopen(BASE + '/?rest_route=/nlj-test/v1/state', timeout=30).read().decode())['drops']
    dbg = (ROLL / 'site' / 'wp-content' / 'debug.log')
    fatal = 'Fatal' in (dbg.read_text(encoding='utf-8', errors='replace') if dbg.exists() else '')
    ev['rolled_back'] = {'listing_page_http_200': listing_ok, 'the_1_0_tool_loads': tool_ok, 'my_listings_1_0': [x.get('title') for x in mine.get('listings', [])], '2_0_drafts_kept': [x['ID'] for x in drafts], 'php_fatal': fatal}
    stop(p)
    # 3. roll forward
    p = start('after')
    c = S()
    c.v = 'after'
    c.login('dana')
    lst = c.get('/owner/draft')[1].get('drafts', [])
    dj = c.get('/owner/draft/%d' % d2)[1]
    resumed = d2 in [x['id'] for x in lst] and 'החזרה לאחור' in dj.get('fields', {}).get('desc', '') and len(dj.get('photos', [])) == 2
    ph = c.fetch(dj['photos'][0]['full'])[0] if dj.get('photos') else 0
    listing_again = urllib.request.urlopen(url, timeout=30).status == 200
    ev['rolled_forward'] = {'open_draft_resumes': resumed, 'its_photo_opens_for_the_owner': ph, 'listing_page_http_200': listing_again}
    stop(p)
    ok = r[0] == 200 and listing_ok and tool_ok and set([d1, d2]) <= set(int(x['ID']) for x in drafts) and not fatal and resumed and ph == 200 and listing_again
    record({'id': 'L17', 'variant': 'after', 'label': 'real-wp', 'title': 'rollback drill: new code -> base code on the same data -> new code again; nothing lost, no fatal', 'status': 'pass' if ok else 'fail', 'evidence': ev,
            'notes': 'the drill swaps the module files under one SQLite site; on the live site the rollback is the snippet text (707) and the plugin file, and main verifies the backup hashes first'})


if __name__ == '__main__':
    main()
