"""Maps every occurrence of the old promise ("עם כפתורי וואטסאפ וחיוג אליכם") on /post-listing/ and ?lang=en to its element
(tag, id, class), on any base URL (anonymous GET), or on saved HTML files. Main's live run of 6.10 failed on it: on the live
site (1.0) it sits 5 times: Yoast's meta description, og:description and schema description, the page paragraph, and the
plugin's "איך זה עובד" box.
    python phrase_map.py http://127.0.0.1:9408 [label]      a bench (or any site, anonymously)
    python phrase_map.py --files a.html b.html               saved pages
"""
import io
import json
import re
import sys
import time
import urllib.request

PH = 'עם כפתורי וואטסאפ וחיוג אליכם'


def where(s, i):
    lt = s.rfind('<', 0, i)
    tag = s[lt:s.find('>', lt) + 1]
    if tag.startswith('<meta'):
        m = re.search(r'(name|property)="([^"]+)"', tag)
        return 'meta ' + (m.group(2) if m else '?')
    if tag.startswith('<script'):
        c = re.search(r'class="([^"]+)"', tag) or re.search(r'type="([^"]+)"', tag)
        return 'script ' + (c.group(1) if c else '')
    back = s[max(0, i - 4000):i]
    for name, attrs in reversed(re.findall(r'<([a-z0-9]+)\b([^>]*)>', back)):   # the nearest element with an id or a class
        if 'class=' in attrs or 'id=' in attrs:
            c = re.search(r'class="([^"]+)"', attrs)
            d = re.search(r'id="([^"]+)"', attrs)
            return name + (f'#{d.group(1)}' if d else '') + (f'.{c.group(1).split()[0]}' if c else '')
    return tag[:40]


def map_html(s):
    hits = [where(s, m.start()) for m in re.finditer(re.escape(PH), s)]
    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    return {'count': len(hits), 'where': hits, 'meta_description': desc.group(1) if desc else None, 'plugin_box': s.count('class="nlpub-how"')}


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    out = {}
    if sys.argv[1] == '--files':
        for f in sys.argv[2:]:
            out[f] = map_html(io.open(f, encoding='utf-8').read())
    else:
        base, label = sys.argv[1].rstrip('/'), (sys.argv[2] if len(sys.argv) > 2 else '')
        for path in ('/post-listing/', '/post-listing/?lang=en'):
            url = base + path + ('&' if '?' in path else '?') + 'nlv=%d' % time.time()
            out[label + ' ' + path] = map_html(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 HAD-256 phrase map'}), timeout=90).read().decode('utf-8'))
    for k, v in out.items():
        print(f'{k}: {v["count"]} x {v["where"]} | plugin box {v["plugin_box"]} | meta description: {v["meta_description"]}')
