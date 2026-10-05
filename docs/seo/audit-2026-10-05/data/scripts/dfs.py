# -*- coding: utf-8 -*-
"""Thin DataForSEO caller through the shared launcher; saves raw JSON, logs cost to dfs-costs.csv."""
import json, os, subprocess, time
D = r'C:\Users\777\nad-lan\nad-lan-co-il\docs\seo\audit-2026-10-05\data\dfs'
RUN = r'C:\Users\777\Documents\agent-tools\dataforseo\run.cjs'


def call(path, body, tag):
    fp = os.path.join(D, tag + '.json')
    if os.path.exists(fp):
        j = json.load(open(fp, encoding='utf-8'))
        if all(t.get('status_code') == 20000 for t in j.get('tasks', [])) and j.get('tasks'):
            return j
    args = ['node', RUN, 'request', '-X', 'POST', '-p', path, '--no-ai-mode', '-d', json.dumps(body, ensure_ascii=False)]
    j = None
    for attempt in range(3):
        p = subprocess.run(args, capture_output=True, env=dict(os.environ, MSYS_NO_PATHCONV='1'), timeout=900)
        raw = p.stdout.decode('utf-8', 'replace')
        try:
            j = json.loads(raw[raw.find('{'):]); break
        except Exception:
            print('retry', tag, attempt, (p.stderr or b'')[:200]); time.sleep(5)
    if j is None: return {'tasks': []}
    json.dump(j, open(fp, 'w', encoding='utf-8'), ensure_ascii=False)
    cost = j.get('cost', 0)
    with open(os.path.join(D, 'dfs-costs.csv'), 'a', encoding='utf-8') as f:
        f.write('%s,%s,%s,%s\n' % (time.strftime('%Y-%m-%d %H:%M'), tag, path, cost))
    errs = [(t.get('status_code'), t.get('status_message')) for t in j.get('tasks', []) if t.get('status_code') != 20000]
    print('%s cost=$%s errors=%s' % (tag, cost, errs[:3]), flush=True)
    return j
