# -*- coding: utf-8 -*-
"""Build the money keyword list (seeds + GSC queries) and pull Google Ads volume/CPC via the
DataForSEO launcher (run.cjs). Saves raw JSON per batch and a merged CSV. Prints cost per call."""
import csv, json, os, re, subprocess, sys, unicodedata
SP = os.path.dirname(os.path.abspath(__file__))
D = r'C:\Users\777\nad-lan\nad-lan-co-il\docs\seo\audit-2026-10-05\data'
RUN = r'C:\Users\777\Documents\agent-tools\dataforseo\run.cjs'
BRAND = re.compile(r'nad[\s\-_.]*lan|נד[\s\-]*לן\b(?!.*\S)|נדלן\.|nadlan', re.I)


def clean(q):
    q = re.sub(r'[\"\'״׳“”‘’?!,;:()\[\]{}<>|\\~`@%^=+*]', ' ', q)
    q = ''.join(ch for ch in q if unicodedata.category(ch) not in ('Cf', 'Cc', 'So', 'Sk'))
    q = ' '.join(q.split()).lower()
    return q


def load_seeds(name):
    return [clean(l) for l in open(os.path.join(SP, name), encoding='utf-8') if l.strip()]


def gsc_queries(min_impr=20):
    rows = list(csv.DictReader(open(os.path.join(D, 'gsc-16m-queries.csv'), encoding='utf-8')))
    out = []
    for r in sorted(rows, key=lambda r: -float(r['impressions'])):
        q = r['query']
        if float(r['impressions']) < min_impr: break
        if re.search(r'nad[\s\-_.]*lan|nadlan', q, re.I): continue
        c = clean(q)
        if not c or len(c) > 80 or len(c.split()) > 10: continue
        out.append(c)
    return out


def call(body, tag):
    fp = os.path.join(D, 'dfs', 'sv-%s.json' % tag)
    if os.path.exists(fp):
        j = json.load(open(fp, encoding='utf-8'))
        if all(t.get('status_code') == 20000 for t in j.get('tasks', [])):
            print('cached', tag); return [r for t in j['tasks'] for r in (t.get('result') or [])], 0
    args = ['node', RUN, 'request', '-X', 'POST', '-p', '/v3/keywords_data/google_ads/search_volume/live',
            '--no-ai-mode', '-d', json.dumps(body, ensure_ascii=False)]
    env = dict(os.environ, MSYS_NO_PATHCONV='1')
    p = subprocess.run(args, capture_output=True, env=env, timeout=600)
    raw = p.stdout.decode('utf-8', 'replace')
    i = raw.find('{')
    j = json.loads(raw[i:])
    json.dump(j, open(os.path.join(D, 'dfs', 'sv-%s.json' % tag), 'w', encoding='utf-8'), ensure_ascii=False)
    cost = j.get('cost')
    if cost is None:
        cost = sum(t.get('cost', 0) for t in j.get('tasks', []))
    print('call %s: status=%s cost=$%s' % (tag, j.get('status_code') or j.get('status'), cost), flush=True)
    res = []
    for t in j.get('tasks', []):
        if t.get('status_code') != 20000: print('  task error', t.get('status_code'), t.get('status_message'))
        res += t.get('result') or []
    return res, cost or 0


def main():
    he = list(dict.fromkeys(load_seeds('seeds_he.txt') + load_seeds('seeds_foreign.txt')))
    gq = [q for q in gsc_queries() if q not in he]
    kws = list(dict.fromkeys(he + gq))[:2000]
    print('keywords total', len(kws), 'seeds', len(he), 'from gsc', len(gq))
    allres, total = [], 0
    B = 500
    for n, i in enumerate(range(0, len(kws), B)):
        res, c = call([{'location_code': 2376, 'keywords': kws[i:i + B]}], 'il-%d' % n)
        for r in res: r['_loc'] = 'IL'
        allres += res; total += c
    # foreign-market check: French keywords in France, English in the US
    fr = [k for k in load_seeds('seeds_foreign.txt') if re.search(r'immobilier|appartement|acheter|investir', k)]
    en = [k for k in load_seeds('seeds_foreign.txt') if re.match(r'^[a-z ]+$', k) and k not in fr]
    for loc, code, ks in (('FR', 2250, fr), ('US', 2840, en)):
        res, c = call([{'location_code': code, 'keywords': ks}], loc.lower())
        for r in res: r['_loc'] = loc
        allres += res; total += c
    with open(os.path.join(D, 'dfs-search-volume.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['market', 'keyword', 'search_volume', 'cpc_usd', 'competition', 'low_bid', 'high_bid', 'seed'])
        seedset = set(he)
        for r in allres:
            w.writerow([r['_loc'], r['keyword'], r.get('search_volume'), r.get('cpc'), r.get('competition'),
                        r.get('low_top_of_page_bid'), r.get('high_top_of_page_bid'), int(r['keyword'] in seedset)])
    print('TOTAL COST $%.4f rows %d' % (total, len(allres)))


if __name__ == '__main__':
    main()
