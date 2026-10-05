# -*- coding: utf-8 -*-
"""HAD-435 GSC analysis: trend, top pages, brand split, languages, sections, striking distance, cannibalization."""
import csv, re, collections, datetime as dt, urllib.parse, json, os
D = r'C:\Users\777\nad-lan\nad-lan-co-il\docs\seo\audit-2026-10-05\data'
OUT = os.path.join(D, 'derived'); os.makedirs(OUT, exist_ok=True)


def L(f):
    rows = list(csv.DictReader(open(os.path.join(D, f), encoding='utf-8')))
    for r in rows:
        r['c'] = float(r['clicks']); r['i'] = float(r['impressions']); r['p'] = float(r['position'])
        if 'page' in r: r['u'] = urllib.parse.unquote(r['page'])
    return rows


def W(name, header, rows):
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


BRAND = re.compile(r'nad[\s\-_.]*lan|nadlan|נד[\s\-]לן|נדלן\.קו|נדל"ן\.קו|nad lan', re.I)


def lang_of(u):
    p = urllib.parse.urlsplit(u).path
    m = re.match(r'^/(en|fr|ru|ar)(/|$)', p)
    if m: return m.group(1)
    s = re.search(r'-(en|fr|ru|ar)/?$', p)
    if s: return s.group(1)
    return 'he'


def section_of(u):
    p = urllib.parse.urlsplit(u).path
    seg = p.strip('/').split('/')[0] if p.strip('/') else '(home)'
    if seg in ('en', 'fr', 'ru', 'ar'): return 'lang-' + seg
    tools = {'property-value-estimator', 'mortgage-calculator', 'purchase-tax-calculator', 'tabu-extract-check',
             'property-value', 'investment-property-cashflow-calculator', 'post-listing'}
    if seg in tools: return 'tools'
    if seg in ('projects', 'professionals', 'glossary', 'glossary-category', 'commercial-real-estate', 'investment',
               'sde-dov', 'urban-renewal', 'properties', 'global', 'tel-aviv-plans', 'new-projects', 'city', 'cities',
               '(home)', 'guides', 'north-tel-aviv', 'short-term-rentals-abroad', 'real-estate-lawyer',
               'real-estate-tax-advisor', 'selling-apartment', 'buying-apartment'):
        return seg
    if re.search(r'apartment-prices', seg): return 'city-price-pages'
    return 'other-pages'


def main():
    # 1. trend
    daily = L('gsc-16m-daily.csv')
    months = collections.OrderedDict(); weeks = collections.OrderedDict()
    for r in daily:
        d = dt.date.fromisoformat(r['date'])
        for key, bucket in ((r['date'][:7], months), ((d - dt.timedelta(days=d.weekday())).isoformat(), weeks)):
            a = bucket.setdefault(key, [0, 0, 0, 0]); a[0] += r['c']; a[1] += r['i']; a[2] += r['p'] * r['i']; a[3] += 1
    W('trend-monthly.csv', ['month', 'clicks', 'impressions', 'ctr_pct', 'avg_pos', 'days'],
      [[k, int(a[0]), int(a[1]), round(100 * a[0] / a[1], 2) if a[1] else 0, round(a[2] / a[1], 1) if a[1] else 0, a[3]] for k, a in months.items()])
    W('trend-weekly.csv', ['week_start', 'clicks', 'impressions', 'ctr_pct', 'avg_pos', 'days'],
      [[k, int(a[0]), int(a[1]), round(100 * a[0] / a[1], 2) if a[1] else 0, round(a[2] / a[1], 1) if a[1] else 0, a[3]] for k, a in weeks.items()])
    tot = [sum(r['c'] for r in daily), sum(r['i'] for r in daily)]

    # 2. pages
    pages = L('gsc-16m-pages.csv'); p28 = {r['u']: r for r in L('gsc-28d-pages.csv')}
    pages.sort(key=lambda r: -r['c'])
    W('top50-pages-by-clicks.csv', ['page', 'clicks', 'impressions', 'ctr_pct', 'avg_pos', 'clicks_28d', 'impr_28d', 'pos_28d', 'lang', 'section'],
      [[r['u'], int(r['c']), int(r['i']), round(100 * r['c'] / r['i'], 2), round(r['p'], 1),
        int(p28[r['u']]['c']) if r['u'] in p28 else 0, int(p28[r['u']]['i']) if r['u'] in p28 else 0,
        round(p28[r['u']]['p'], 1) if r['u'] in p28 else '', lang_of(r['u']), section_of(r['u'])] for r in pages[:50]])
    pages.sort(key=lambda r: -r['i'])
    W('top50-pages-by-impressions.csv', ['page', 'clicks', 'impressions', 'ctr_pct', 'avg_pos', 'clicks_28d', 'impr_28d', 'pos_28d', 'lang', 'section'],
      [[r['u'], int(r['c']), int(r['i']), round(100 * r['c'] / r['i'], 2), round(r['p'], 1),
        int(p28[r['u']]['c']) if r['u'] in p28 else 0, int(p28[r['u']]['i']) if r['u'] in p28 else 0,
        round(p28[r['u']]['p'], 1) if r['u'] in p28 else '', lang_of(r['u']), section_of(r['u'])] for r in pages[:50]])

    # sections + languages
    sec = collections.defaultdict(lambda: [0, 0, 0, 0]); lang = collections.defaultdict(lambda: [0, 0, 0, 0])
    for r in pages:
        for k, b in ((section_of(r['u']), sec), (lang_of(r['u']), lang)):
            b[k][0] += r['c']; b[k][1] += r['i']; b[k][2] += r['p'] * r['i']; b[k][3] += 1
    W('by-section.csv', ['section', 'clicks', 'impressions', 'avg_pos', 'pages_with_impr'],
      sorted([[k, int(a[0]), int(a[1]), round(a[2] / a[1], 1), a[3]] for k, a in sec.items()], key=lambda x: -x[1]))
    W('by-language.csv', ['lang', 'clicks', 'impressions', 'avg_pos', 'pages_with_impr'],
      sorted([[k, int(a[0]), int(a[1]), round(a[2] / a[1], 1), a[3]] for k, a in lang.items()], key=lambda x: -x[2]))
    langpages = [r for r in pages if lang_of(r['u']) != 'he']
    langpages.sort(key=lambda r: -r['i'])
    W('language-pages.csv', ['page', 'lang', 'clicks', 'impressions', 'avg_pos'],
      [[r['u'], lang_of(r['u']), int(r['c']), int(r['i']), round(r['p'], 1)] for r in langpages])

    # 3. brand split (query-level; anonymised queries are absent)
    q = L('gsc-16m-queries.csv')
    b = [r for r in q if BRAND.search(r['query'])]; nb = [r for r in q if not BRAND.search(r['query'])]
    brand = {'brand_clicks': sum(r['c'] for r in b), 'brand_impr': sum(r['i'] for r in b), 'brand_queries': len(b),
             'nonbrand_clicks': sum(r['c'] for r in nb), 'nonbrand_impr': sum(r['i'] for r in nb), 'nonbrand_queries': len(nb),
             'property_clicks': tot[0], 'property_impr': tot[1],
             'anonymised_clicks': tot[0] - sum(r['c'] for r in q), 'anonymised_impr': tot[1] - sum(r['i'] for r in q),
             'brand_list': sorted([(r['query'], int(r['c']), int(r['i']), round(r['p'], 1)) for r in b], key=lambda x: -x[2])[:30]}
    json.dump(brand, open(os.path.join(OUT, 'brand-split.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # 4. striking distance (90 days): query level for position, qp for the page carrying it
    q90 = L('gsc-90d-queries.csv'); qp90 = L('gsc-90d-qp.csv')
    best = {}
    for r in qp90:
        cur = best.get(r['query'])
        if cur is None or r['i'] > cur['i']: best[r['query']] = r
    npages = collections.Counter(r['query'] for r in qp90 if r['i'] > 0)
    vol = {}
    for r in csv.DictReader(open(os.path.join(D, 'dfs-search-volume.csv'), encoding='utf-8')):
        if r['market'] == 'IL' and r['search_volume'] not in ('', 'None'):
            vol[r['keyword']] = (int(r['search_volume']), float(r['cpc_usd'] or 0))
    def key(s):
        s = re.sub(r'[\"\'״׳“”‘’?!,;:()\[\]{}<>|\\~`@%^=+*]', ' ', s); return ' '.join(s.split()).lower()
    sd = []
    for r in q90:
        if 4.5 <= r['p'] <= 30.5 and r['i'] >= 20 and not BRAND.search(r['query']):
            bp = best.get(r['query']); v, c = vol.get(key(r['query']), ('', ''))
            sd.append([r['query'], int(r['c']), int(r['i']), round(r['p'], 1), bp['u'] if bp else '', npages[r['query']], v, c])
    sd.sort(key=lambda x: -(x[2] * ((x[7] or 0.5) if x[7] != '' else 0.5)))
    W('striking-distance-90d.csv', ['query', 'clicks', 'impressions', 'avg_pos', 'main_page', 'pages_with_impr', 'ads_volume_IL', 'cpc_usd'], sd)

    # 5. cannibalization (90 days)
    byq = collections.defaultdict(list)
    for r in qp90:
        if r['i'] > 0: byq[r['query']].append(r)
    can = []
    for qq, rs in byq.items():
        if len(rs) < 2: continue
        ti = sum(r['i'] for r in rs)
        rs.sort(key=lambda r: -r['i'])
        second_share = rs[1]['i'] / ti
        v, c = vol.get(key(qq), ('', ''))
        can.append([qq, int(sum(r['c'] for r in rs)), int(ti), len(rs), round(second_share, 2), v, c,
                    ' || '.join('%s [%di p%.0f %dc]' % (r['u'], r['i'], r['p'], r['c']) for r in rs[:5])])
    can.sort(key=lambda x: -x[2])
    W('cannibalization-90d.csv', ['query', 'clicks', 'impressions', 'n_pages', 'second_page_share', 'ads_volume_IL', 'cpc_usd', 'pages (top5)'], can)
    print('months', [(k, int(a[0]), int(a[1])) for k, a in months.items()])
    print('total', tot, 'brand', {k: v for k, v in brand.items() if k != 'brand_list'})
    print('striking', len(sd), 'cannib queries', len(can), 'with >=20 impr', len([x for x in can if x[2] >= 20]))


if __name__ == '__main__':
    main()
