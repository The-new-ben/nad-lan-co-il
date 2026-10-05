# -*- coding: utf-8 -*-
import json, glob, os, re, csv, collections, urllib.parse
D = r'C:\Users\777\nad-lan\nad-lan-co-il\docs\seo\audit-2026-10-05\data'


def ptype(dom, url, title):
    u = urllib.parse.unquote(url).lower(); d = dom.lower()
    if re.search(r'gov\.il|\.muni\.il|kolzchut|wikipedia', d): return 'gov/wiki'
    if re.search(r'bank|leumi|poalim|mizrahi|discount|mercantile|fibi|jerusalem-bank|cav\.co', d): return 'bank'
    if re.search(r'ynet|calcalist|globes|themarker|bizportal|mako|walla|maariv|haaretz|ice\.co|israelhayom|news', d): return 'news'
    if re.search(r'yad2|madlan|homeless|komo|onmap|winwin|nadlancenter|nadlan\.com|yad1|ad\.co|dira|hadashim|project-tlv|newkey|zhg|hon\.co', d):
        if re.search(r'/projects?|new-?projects|/project/|yad1|newproject|פרויקט', u): return 'portal-projects'
        if re.search(r'forsale|for-sale|/sale|realestate/forsale|למכירה', u): return 'portal-listings'
        return 'portal-other'
    if re.search(r'tidhar|azorim|gindi|dimri|ashtrom|africa-israel|aura|yitzhaki|electra|canada|shikun|acro|rotshtein|y-h|ytong|prashkovsky|avisror|hagag|bsr|isras|amot|tama|aviv-group', d): return 'developer'
    if re.search(r'law|adv|lawyer|עורך|attorney|-law', d + u): return 'law-firm'
    if re.search(r'calc|מחשבון|calculator', u + title.lower()): return 'tool'
    return 'other'


def main():
    out = []; dom_count = collections.Counter(); dom_top3 = collections.Counter(); type_count = collections.Counter()
    features = collections.Counter(); ours = []
    rows = []
    for f in sorted(glob.glob(os.path.join(D, 'dfs', 'serp-*.json'))):
        j = json.load(open(f, encoding='utf-8'))
        try: r = j['tasks'][0]['result'][0]
        except Exception: continue
        kw = r['keyword']; lang = j['tasks'][0]['data'].get('language_code')
        feats = [t for t in (r.get('item_types') or []) if t != 'organic']
        for t in feats: features[t] += 1
        org = [it for it in r['items'] if it['type'] == 'organic']
        our = [(it['rank_group'], urllib.parse.unquote(it['url']).replace('https://nad-lan.co.il', '')) for it in org if 'nad-lan.co.il' in (it.get('domain') or '')]
        paa = [ (q.get('title') or '') for it in r['items'] if it['type'] == 'people_also_ask' for q in (it.get('items') or [])]
        top = []
        for it in org[:10]:
            d = (it.get('domain') or '').replace('www.', '')
            t = ptype(d, it.get('url') or '', it.get('title') or '')
            top.append((it['rank_group'], d, t, urllib.parse.unquote(it.get('url') or '')[:110], (it.get('title') or '')[:70]))
            dom_count[d] += 1; type_count[t] += 1
            if it['rank_group'] <= 3: dom_top3[d] += 1
        rows.append({'kw': kw, 'lang': lang, 'features': feats, 'ours': our, 'top': top, 'paa': paa[:4]})
    json.dump(rows, open(os.path.join(D, 'derived', 'serp-summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(os.path.join(D, 'derived', 'serp-top10.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['keyword', 'lang', 'rank', 'domain', 'page_type', 'url', 'title', 'serp_features', 'nadlan_rank'])
        for r in rows:
            for t in r['top']:
                w.writerow([r['kw'], r['lang'], t[0], t[1], t[2], t[3], t[4], ' '.join(r['features']), ' '.join('%s:%s' % o for o in r['ours'])])
    print('SERPs', len(rows))
    print('features', features.most_common())
    print('types', type_count.most_common())
    print('top domains (top10 appearances)', dom_count.most_common(40))
    print('top3 domains', dom_top3.most_common(25))
    for r in rows:
        print('\n##', r['kw'], '| feats:', ','.join(r['features']), '| ours:', r['ours'])
        for t in r['top'][:10]: print('  ', t[0], t[1], t[2], t[3][:90])


if __name__ == '__main__':
    main()
