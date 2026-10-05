# -*- coding: utf-8 -*-
"""Technical analysis of crawl.jsonl (HAD-435): status, redirects, canonicals, hreflang, titles/H1/meta, thin, orphans, depth."""
import json, csv, collections, os, re, urllib.parse, sys
SP = os.path.dirname(os.path.abspath(__file__))
D = r'C:\Users\777\nad-lan\nad-lan-co-il\docs\seo\audit-2026-10-05\data'
OUT = os.path.join(D, 'crawl'); os.makedirs(OUT, exist_ok=True)


def norm(u):
    s = urllib.parse.urlsplit(u)
    path = urllib.parse.quote(urllib.parse.unquote(s.path or '/'), safe="/%:@!$&'()*+,;=-._~")
    return urllib.parse.urlunsplit(('https', (s.hostname or '').lower(), path, s.query, ''))


def short(u):
    return urllib.parse.unquote(u).replace('https://nad-lan.co.il', '').replace('http://nad-lan.co.il', 'http:')


def sect(u):
    p = urllib.parse.urlsplit(u).path.strip('/')
    return p.split('/')[0] if p else '(home)'


def W(name, header, rows):
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


def main():
    recs = {}
    for line in open(os.path.join(SP, 'crawl.jsonl'), encoding='utf-8'):
        try:
            r = json.loads(line)
        except Exception:
            continue
        recs[norm(r["url"])] = r
    sm = [norm(r['url']) for r in csv.DictReader(open(os.path.join(D, 'sitemap-urls.csv'), encoding='utf-8'))]
    smset = set(sm)
    gsc = {}
    for r in csv.DictReader(open(os.path.join(D, 'gsc-90d-pages.csv'), encoding='utf-8')):
        gsc[norm(r['page'])] = (float(r['clicks']), float(r['impressions']), float(r['position']))
    imp = lambda u: gsc.get(u, (0, 0, 0))[1]
    rep = {}
    # status
    st = collections.Counter(r.get('status') for r in recs.values())
    rep['records'] = len(recs); rep['status'] = dict(st)
    html = {u: r for u, r in recs.items() if r.get('status') == 200 and 'title' in r}
    # inlinks graph
    inl = collections.defaultdict(set); anchors = collections.defaultdict(collections.Counter)
    link_to_bad = []
    for u, r in html.items():
        for l in r.get('links', []):
            t = norm(l[0])
            if t == u: continue
            inl[t].add(u); anchors[t][l[1]] += 1
    # broken / redirected internal link targets
    bad_targets = []
    for t, srcs in inl.items():
        tr = recs.get(t)
        if tr and tr.get('status') not in (200, None):
            bad_targets.append((t, tr.get('status'), short(tr.get('final_url', '')), len(srcs), ' | '.join(short(s) for s in list(srcs)[:3])))
    bad_targets.sort(key=lambda x: -x[3])
    W('internal-links-to-non200.csv', ['target', 'status', 'final', 'n_linking_pages', 'examples'], [[short(a), b, c, d, e] for a, b, c, d, e in bad_targets])
    rep['internal_link_targets_non200'] = collections.Counter(b for _, b, _, _, _ in bad_targets)
    rep['internal_link_targets_non200_top'] = [(short(a), b, d) for a, b, _, d, _ in bad_targets[:15]]
    # redirect chains
    chains = [(short(u), r['status'], len(r['chain']), short(r['final_url']), r.get('final_status')) for u, r in recs.items() if r.get('chain')]
    W('redirects.csv', ['url', 'status', 'hops', 'final', 'final_status'], chains)
    rep['redirects'] = len(chains); rep['redirect_chains_2plus'] = [c for c in chains if c[2] >= 2][:20]
    # http links inside html
    httpl = collections.Counter()
    for u, r in html.items():
        for l in r.get('links', []):
            if l[0].startswith('http://'): httpl[u] += 1
    rep['pages_with_http_links'] = len(httpl)
    # sitemap health
    sm_non200 = [(short(u), recs[u].get('status'), short(recs[u].get('final_url', ''))) for u in sm if u in recs and recs[u].get('status') != 200]
    sm_missing = [short(u) for u in sm if u not in recs]
    W('sitemap-non200.csv', ['url', 'status', 'final'], sm_non200)
    rep['sitemap_urls'] = len(sm); rep['sitemap_non200'] = len(sm_non200); rep['sitemap_non200_sample'] = sm_non200[:15]
    rep['sitemap_not_fetched'] = len(sm_missing)
    # canonicals / robots
    canon_rows = []; noidx = []; canon_issue = collections.Counter()
    for u, r in html.items():
        c = r.get('canonical') or []
        robots = (r.get('robots') or '') + ' ' + (r.get('xrobots') or '')
        if 'noindex' in robots.lower(): noidx.append((short(u), u in smset, imp(u)))
        if not c: canon_issue['missing'] += 1; canon_rows.append((short(u), 'missing', '', u in smset, imp(u))); continue
        if len(set(c)) > 1: canon_issue['multiple'] += 1; canon_rows.append((short(u), 'multiple', ' '.join(c), u in smset, imp(u)))
        cn = norm(urllib.parse.urljoin(u, c[0]))
        if cn != u:
            cr = recs.get(cn)
            kind = 'canonicalised-elsewhere'
            if cr and cr.get('status') != 200: kind = 'canonical-to-non200'
            canon_issue[kind] += 1; canon_rows.append((short(u), kind, short(cn), u in smset, imp(u)))
    W('canonical-issues.csv', ['url', 'issue', 'canonical', 'in_sitemap', 'gsc_impr_90d'], sorted(canon_rows, key=lambda x: -x[4]))
    W('noindex-pages.csv', ['url', 'in_sitemap', 'gsc_impr_90d'], noidx)
    rep['canonical_issues'] = dict(canon_issue); rep['noindex_pages'] = len(noidx); rep['noindex_in_sitemap'] = sum(1 for x in noidx if x[1])
    rep['sitemap_canonicalised_elsewhere'] = [x[:3] for x in canon_rows if x[3] and x[1] != 'missing'][:20]
    # hreflang
    hl_rows = []; hl_pages = 0; hl_issue = collections.Counter()
    for u, r in html.items():
        hl = r.get('hreflang') or []
        if not hl: continue
        hl_pages += 1
        codes = [h[0] for h in hl]
        if 'x-default' not in codes: hl_issue['no-x-default'] += 1
        selfref = any(norm(h[1]) == u for h in hl)
        if not selfref: hl_issue['no-self-reference'] += 1; hl_rows.append((short(u), 'no-self', '', ''))
        for code, href in hl:
            t = norm(urllib.parse.urljoin(u, href))
            if t == u: continue
            tr = recs.get(t)
            if tr is None: hl_issue['target-not-crawled'] += 1; hl_rows.append((short(u), 'target-not-crawled', code, short(t))); continue
            if tr.get('status') != 200: hl_issue['target-non200'] += 1; hl_rows.append((short(u), 'target-non200:%s' % tr.get('status'), code, short(t))); continue
            back = [norm(urllib.parse.urljoin(t, h[1])) for h in (tr.get('hreflang') or [])]
            if u not in back: hl_issue['missing-return'] += 1; hl_rows.append((short(u), 'missing-return', code, short(t)))
            tl = (tr.get('lang') or '').lower()[:2]
            if code != 'x-default' and tl and tl != code[:2]: hl_issue['lang-attr-mismatch'] += 1; hl_rows.append((short(u), 'html-lang=%s' % tl, code, short(t)))
    W('hreflang-issues.csv', ['page', 'issue', 'hreflang', 'target'], hl_rows)
    rep['hreflang_pages'] = hl_pages; rep['hreflang_issues'] = dict(hl_issue)
    # titles / h1 / meta
    idx = {u: r for u, r in html.items() if 'noindex' not in ((r.get('robots') or '') + (r.get('xrobots') or '')).lower()
           and (not r.get('canonical') or norm(urllib.parse.urljoin(u, r['canonical'][0])) == u)}
    rep['indexable_html'] = len(idx)
    tcount = collections.Counter(r['title'] for r in idx.values())
    dcount = collections.Counter((r.get('desc') or '') for r in idx.values())
    hcount = collections.Counter((r.get('h1') or [''])[0] for r in idx.values())
    rows = []
    agg = collections.Counter()
    for u, r in idx.items():
        t = r.get('title') or ''; d = r.get('desc') or ''; h = r.get('h1') or []
        issues = []
        if not t: issues.append('title-missing')
        elif tcount[t] > 1: issues.append('title-duplicate')
        if len(t) > 70: issues.append('title-long')
        if t and len(t) < 25: issues.append('title-short')
        if not d: issues.append('meta-missing')
        elif dcount[d] > 1: issues.append('meta-duplicate')
        if len(d) > 170: issues.append('meta-long')
        if not h: issues.append('h1-missing')
        if len(h) > 1: issues.append('h1-multiple')
        if h and hcount[h[0]] > 1: issues.append('h1-duplicate')
        wm = r.get('words_main') or 0
        if wm < 250: issues.append('thin<250w')
        if re.search(r'[A-Za-z]{3,}', ' '.join(h)) and re.search(r'[\u0590-\u05FF]', ' '.join(h)): issues.append('h1-mixed-he-en')
        for i in issues: agg[i] += 1
        if issues:
            rows.append((short(u), sect(u), ' '.join(issues), t, len(t), (h[0] if h else ''), len(h), wm, imp(u)))
    rows.sort(key=lambda x: -x[8])
    W('onpage-issues.csv', ['url', 'section', 'issues', 'title', 'title_len', 'h1', 'h1_count', 'words_main', 'gsc_impr_90d'], rows)
    rep['onpage_issue_counts'] = dict(agg)
    # issue counts by section
    bysec = collections.defaultdict(collections.Counter)
    for row in rows:
        for i in row[2].split(): bysec[row[1]][i] += 1
    rep['onpage_by_section'] = {k: dict(v) for k, v in sorted(bysec.items(), key=lambda kv: -sum(kv[1].values()))[:15]}
    dup_titles = [(t, n) for t, n in tcount.most_common(25) if n > 1]
    rep['dup_titles_top'] = dup_titles
    rep['dup_h1_top'] = [(t, n) for t, n in hcount.most_common(15) if n > 1]
    # orphans and depth (link graph from home)
    orph = []
    for u in sm:
        r = recs.get(u)
        if r and r.get('status') == 200 and not inl.get(u):
            orph.append((short(u), sect(u), imp(u)))
    orph.sort(key=lambda x: -x[2])
    W('orphans.csv', ['url', 'section', 'gsc_impr_90d'], orph)
    rep['orphans_in_sitemap'] = len(orph); rep['orphans_by_section'] = dict(collections.Counter(o[1] for o in orph).most_common(15))
    rep['orphans_top'] = orph[:25]
    depth = collections.Counter(r.get('depth') for r in html.values())
    rep['depth_distribution'] = {str(k): v for k, v in sorted(depth.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))}
    deep_money = [(short(u), r.get('depth'), imp(u), len(inl.get(u, ()))) for u, r in html.items() if (r.get('depth') is None or r.get('depth') > 3) and imp(u) >= 100]
    deep_money.sort(key=lambda x: -x[2])
    rep['deep_pages_with_impr'] = deep_money[:25]
    # crawled-but-not-in-sitemap (indexable)
    notsm = [(short(u), sect(u), imp(u)) for u in idx if u not in smset]
    notsm.sort(key=lambda x: -x[2])
    W('indexable-not-in-sitemap.csv', ['url', 'section', 'gsc_impr_90d'], notsm)
    rep['indexable_not_in_sitemap'] = len(notsm); rep['indexable_not_in_sitemap_top'] = notsm[:20]
    # key pages inlinks
    keys = ['/', '/projects/', '/projects/hamedina/', '/projects/hamedina-en/', '/projects/hamedina-fr/', '/projects/hamedina-ru/',
            '/projects/hamedina-ar/', '/sde-dov/', '/sde-dov/prices/', '/sde-dov/merkaz/', '/sde-dov-luxury-projects-2026/',
            '/new-projects/new-projects-tel-aviv/', '/new-projects/north-tel-aviv-new-projects/', '/property-value-estimator/',
            '/investment/', '/investment/apartments-for-investment/', '/real-estate-lawyer/', '/real-estate-appraiser/',
            '/home-inspection/', '/purchase-tax-calculator/', '/mortgage-calculator/', '/urban-renewal/map/',
            '/projects/duo-tel-aviv/', '/projects/rainbow-tel-aviv/', '/projects/dimri-yama-sde-dov/', '/herzliya-projects/',
            '/tel-aviv-apartment-prices/', '/properties/', '/luxury-tel-aviv/', '/premium/', '/catalog/', '/site-map/', '/sitemap/']
    kp = []
    for k in keys:
        u = norm('https://nad-lan.co.il' + k); r = recs.get(u, {})
        kp.append((k, r.get('status'), r.get('depth'), len(inl.get(u, ())), r.get('title', '')[:90], (r.get('h1') or [''])[0][:70], r.get('words_main'),
                   anchors[u].most_common(4)))
    rep['key_pages'] = kp
    # thin money pages
    thin = [(short(u), sect(u), r.get('words_main'), imp(u)) for u, r in idx.items() if (r.get('words_main') or 0) < 300 and sect(u) not in ('professionals',)]
    thin.sort(key=lambda x: -x[3])
    rep['thin_non_professional'] = len(thin); rep['thin_top'] = thin[:20]
    rep['thin_professionals'] = sum(1 for u, r in idx.items() if (r.get('words_main') or 0) < 300 and sect(u) == 'professionals')
    # GSC pages (90d, impr>=20) status
    g_bad = []
    for u, (c, i, p) in gsc.items():
        if i < 20: continue
        r = recs.get(u)
        if r is None: g_bad.append((short(u), 'not-crawled', i, c))
        elif r.get('status') != 200: g_bad.append((short(u), r.get('status'), i, c))
    g_bad.sort(key=lambda x: -x[2])
    W('gsc-pages-not-200.csv', ['url', 'status', 'impr_90d', 'clicks_90d'], g_bad)
    rep['gsc_pages_90d_not200_or_uncrawled'] = len(g_bad); rep['gsc_bad_top'] = g_bad[:25]
    # slow pages
    slow = sorted([(short(u), r.get('ms'), r.get('bytes')) for u, r in html.items() if r.get('ms')], key=lambda x: -x[1])
    rep['ttfb_median_ms'] = sorted(r.get('ms') for r in html.values() if r.get('ms'))[len(html) // 2] if html else None
    rep['slowest'] = slow[:10]
    rep['html_bytes_median'] = sorted(r.get('bytes') or 0 for r in html.values())[len(html) // 2] if html else None
    json.dump(rep, open(os.path.join(OUT, 'tech-summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    print(json.dumps(rep, ensure_ascii=False, indent=1, default=str)[:30000])


if __name__ == '__main__':
    main()
