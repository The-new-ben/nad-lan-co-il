"""Cache the public inputs of the v2 proposal (26.10.2026). GET only, read-only toward the live site.

Writes into labels/v2/cache/: the live page (with the public map token REDACTED before it touches disk), the map's city list
(renewal-map-data), the live copies of the tracker data and the price data, and a report comparing them (md5) with the repo
copies the patch reads. The lookup endpoint (renewal-lookup, 30 calls per IP per hour: HAD-605) is NOT called here.

    python fetch_cache.py
"""
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..', '..'))
CACHE = os.path.join(HERE, 'cache')
DATA = os.path.join(REPO, 'plugins', 'nadlan-config', 'assets', 'instruments', 'data')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
SITE = 'https://nad-lan.co.il'
os.makedirs(CACHE, exist_ok=True)


def get(url):
    t = time.time()
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Encoding': 'identity'})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
        return body, dict(r.headers), round((time.time() - t) * 1000)


rep = {'at_utc': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
html, h, ms = get(SITE + '/urban-renewal/map/')
txt = html.decode('utf-8', 'replace')
rep['page'] = {'bytes': len(html), 'ms': ms, 'cache': h.get('X-Cache') or h.get('x-cache') or h.get('CF-Cache-Status'), 'hotjar': 'hotjar' in txt.lower(),
               'has_tracker_host': 'data-nli="urtrack"' in txt, 'pins_in_html': txt.count('nlurm-pin')}
m = re.search(r'data-nli="urtrack"[^>]*data-nli-data="([^"]+)"', txt)
rep['tracker_data_url'] = m.group(1).replace('&#038;', '&') if m else None
safe = re.sub(r'pk\.[A-Za-z0-9._-]{20,}', 'pk.REDACTED', txt)
open(os.path.join(CACHE, 'live-page.redacted.html'), 'w', encoding='utf-8').write(safe)

md, h2, ms2 = get(SITE + '/wp-json/nadlan/v1/renewal-map-data')
open(os.path.join(CACHE, 'renewal-map-data.json'), 'wb').write(md)
d = json.loads(md)
rep['map_data'] = {'total': d.get('total'), 'cities': len(d.get('cities', [])), 'with_point': sum(1 for c in d['cities'] if c.get('lnglat')), 'ms': ms2}

for name in ('renewal-track.json', 'value.json', 'value-series.json'):
    url = SITE + '/wp-content/plugins/nadlan-config/assets/instruments/data/' + name
    try:
        b, hh, ms3 = get(url)
        open(os.path.join(CACHE, 'live-' + name), 'wb').write(b)
        local = open(os.path.join(DATA, name), 'rb').read()
        rep[name] = {'live_bytes': len(b), 'live_md5': hashlib.md5(b).hexdigest(), 'repo_md5': hashlib.md5(local).hexdigest(),
                     'same_as_repo': b == local, 'cache_control': hh.get('Cache-Control'), 'ms': ms3}
    except Exception as e:  # noqa: BLE001
        rep[name] = {'error': str(e)[:200]}

json.dump(rep, open(os.path.join(CACHE, 'fetch-report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(rep, ensure_ascii=False, indent=1))
