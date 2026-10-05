# -*- coding: utf-8 -*-
import dfs, hashlib, os
SP = os.path.dirname(os.path.abspath(__file__))
for line in open(os.path.join(SP, 'serp_kws.txt'), encoding='utf-8'):
    if not line.strip(): continue
    lang, kw = line.strip().split('|', 1)
    loc = 2376
    tag = 'serp-' + lang + '-' + hashlib.md5(kw.encode()).hexdigest()[:8]
    dfs.call('/v3/serp/google/organic/live/advanced', [{'keyword': kw, 'location_code': loc, 'language_code': lang, 'depth': 20, 'device': 'desktop'}], tag)
print('SERP DONE')
