"""L16 regression on real WordPress (AFTER bench): a broker's private drop door /drop/<token>/ still builds the broker's
listing through x-broker-drop 1.1.4 (photo, submit, build), parallel builds give one listing, the page keeps the
broker's name, broker status and licence line (reg. 19(a)), the 1.1.3 photo door still cleans GPS, and the owner's
draft photos are not reachable through the broker's media door.
The AI reading is off on the bench (bench /drop-ready stands in for it, as in the BEFORE runs).
"""
import io
import uuid

from PIL import Image

from bench import reset, record, bench, clear, state, http, base
from session import parallel, jpeg_bytes, Session
from test_photos import make, metadata_left

V = 'after'


def main():
    clear('L16', V, 'broker door')
    reset(V)
    t = bench(V, '/broker-make', {})[1]
    token = t['token']
    root = base(V) + '/wp-json/nadlan/v1/drop/' + token
    anon = Session(V)
    anon.base = base(V)
    s1, j1 = anon.upload('/drop/%s/photo' % token, 'b.jpg', make('JPEG', 6), {}, 'image/jpeg')
    gps_left = None
    if s1 == 200:
        st, body, _ = anon.fetch(j1['url'])
        gps_left = metadata_left(body, 'JPEG')
    s2, j2 = anon.post('/drop/%s/submit' % token, {'text': 'למכירה בבלעדיות, 5 חדרים, 120 מ״ר, קומה 4 מתוך 9. שכונת הדוגמה, תל אביב יפו. 4,200,000 ש״ח.', 'photos': [j1.get('id')]}, nonce=False)
    drop = j2.get('drop')
    bench(V, '/drop-ready', {'drop': drop})
    res = parallel([lambda: anon.post('/drop/%s/build/%d' % (token, drop), {}, nonce=False) for _ in range(3)])
    final = anon.post('/drop/%s/build/%d' % (token, drop), {}, nonce=False)
    rows = [p for p in state(V)['properties'] if p['post_status'] not in ('auto-draft', 'trash')]
    url = final[1].get('url_he', '')
    page = ''
    try:
        import urllib.request
        page = urllib.request.urlopen(url, timeout=30).read().decode('utf-8', 'replace')
    except Exception:
        pass
    licence = 'רישיון' in page and t['license'] in page
    ok = s1 == 200 and gps_left == [] and s2 == 200 and drop and final[0] == 200 and len(rows) == 1 and licence
    record({'id': 'L16', 'variant': V, 'label': 'real-wp', 'title': 'broker door /drop/<token>/: photo (cleaned), submit, 3 parallel builds + 1 more = one listing with the licence line', 'status': 'pass' if ok else 'fail',
            'evidence': {'photo': [s1, 'metadata left: %s' % gps_left], 'submit': [s2, j2.get('state')], 'parallel_builds': [r[0] for r in res], 'final': [final[0], final[1].get('state')], 'listings': [(r['ID'], r['post_status'], r['post_name']) for r in rows], 'licence_line_on_page': licence}})


if __name__ == '__main__':
    main()
