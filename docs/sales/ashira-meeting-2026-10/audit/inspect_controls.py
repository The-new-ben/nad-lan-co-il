# -*- coding: utf-8 -*-
import json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding='utf-8')

for page in ['A', 'B']:
    with open(os.path.join(HERE, f'discover-{page}-d.json'), encoding='utf-8') as f:
        d = json.load(f)
    print(f'=== Page {page} Controls Summary ===')
    for c in d.get('controls', []):
        if not c.get('v'):
            continue
        attrs = c.get('attrs', {})
        sec = c.get('sec', '')
        tag = c.get('tag', '')
        txt = c.get('text', '')
        s_attrs = str(attrs)
        if any(k in s_attrs for k in ['floor', 'tower', 'dir', 'room', 'style', 'phase', 'step', 'layer', 'pg', 'nlps', 'cat', 'wa', 'tour', 'inside', 'deals']):
            print(f"[{sec}] <{tag}> text='{txt[:35]}' attrs={attrs}")
