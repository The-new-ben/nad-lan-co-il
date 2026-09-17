#!/usr/bin/env python3
"""Mechanical checks before handing the package over or re-importing it."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASH = re.compile('[\u2013\u2014]')
problems, n = [], 0
for dp, _, files in os.walk(ROOT):
    for f in files:
        p = os.path.join(dp, f)
        if f.endswith(('.png', '.jpg', '.webp', '.zip', '.pyc')):
            continue
        n += 1
        s = open(p, encoding='utf-8', errors='replace').read()
        if DASH.search(s):
            problems.append(f'long dash in {os.path.relpath(p, ROOT)}')
        if f.endswith(('.json', '.jsonld')):
            try:
                json.loads(s)
            except Exception as e:
                problems.append(f'invalid JSON {os.path.relpath(p, ROOT)}: {e}')
idx = json.load(open(os.path.join(ROOT, 'data', 'listings.json')))['listings']
for it in idx:
    for k, rel in it['files'].items():
        if not os.path.exists(os.path.join(ROOT, rel)):
            problems.append(f'missing {rel}')
    for lang in ('he', 'en'):
        c = open(os.path.join(ROOT, 'listings', it['id'], f'content-{lang}.html'), encoding='utf-8').read()
        if not c.startswith('<!-- wp:html -->'):
            problems.append(f"{it['id']} {lang}: content is not wrapped in a Custom HTML block")
        for bad in ('brief-he', 'לא לפרסום', 'לאשר מול מיטל', 'import-map'):
            if bad in c:
                problems.append(f"{it['id']} {lang}: internal marker '{bad}' found in public content")
        p = json.load(open(os.path.join(ROOT, 'listings', it['id'], f'wp-{lang}.json')))
        if p['status'] != 'draft':
            problems.append(f"{it['id']} {lang}: payload status is not draft")
for lang in ('he', 'en'):
    bp = os.path.join(ROOT, 'broker', f'content-broker-{lang}.html')
    if not os.path.exists(bp):
        problems.append(f'missing broker/content-broker-{lang}.html')
        continue
    c = open(bp, encoding='utf-8').read()
    if not c.startswith('<!-- wp:html -->'):
        problems.append(f'broker {lang}: content is not wrapped in a Custom HTML block')
    for bad in ('brief-he', 'לא לפרסום', 'לאשר מול מיטל', 'import-map'):
        if bad in c:
            problems.append(f"broker {lang}: internal marker '{bad}' found in public content")
    ncards = c.count('class="nlb-lcard"')
    if ncards != len(idx):
        problems.append(f'broker {lang}: {ncards} listing cards, expected {len(idx)}')
    wp = json.load(open(os.path.join(ROOT, 'broker', f'wp-page-{lang}.json')))
    if wp['status'] != 'draft':
        problems.append(f'broker {lang}: payload status is not draft')
print(f'checked {n} text files, {len(idx)} listings, broker page in 2 languages')
print('\n'.join(problems) if problems else 'no problems found')
sys.exit(1 if problems else 0)
