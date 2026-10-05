# -*- coding: utf-8 -*-
"""Money-word opportunity ranking: Ads volume x CPC x reachable position (HAD-435)."""
import csv, glob, json, os, re, urllib.parse, collections
D = r'C:\Users\777\nad-lan\nad-lan-co-il\docs\seo\audit-2026-10-05\data'
OUT = os.path.join(D, 'derived')

MONEY = re.compile(r'דיר|פרויקט|פרוייקט|נדל|מקבלן|משכנת|מס רכישה|מס שבח|שווי|שמא|עורך דין|עורכי דין|מתווך|תיווך|השקע|יוקרה|פנטהאוז|'
                   r'שדה דב|שדה דוב|כיכר המדינה|התחדשות|פינוי|תמא|משרד|חנו|מסחרי|מגרש|בתים|השכרה|שכירות|ניהול נכס|בדק בית|'
                   r'מחיר למשתכן|בהנחה|duo|rainbow|ריינבו|דימרי|דמרי|אשירה|גינדי|zohi|utopia|dimri|ashira|sde dov|kikar|'
                   r'real estate|apartment|property|mortgage|недвиж|квартир|новострой|immobilier|appartement|immeuble|شقق|عقار|مشاريع|'
                   r'קבלן|יזמ|חברות בני|עסקאות|עסקת|נכס|בניינים חדשים|בתים חדשים|על הנייר|טאבו|מחשבון', re.I)
NAV = re.compile(r'madlan|מדלן|יד ?2|yad2|נדלן גוב|נדל ן גוב|מרכז הנדל|נדלן וואן|נדל ן וואן|טו יו|הממשלתי|דן נדל|משכנתאמן|'
                 r'לאומי|פועלים|מזרחי|דיסקונט|טפחות|הפניקס|כלל|מגדל |הראל|מנורה|ynet|homeless|הומלס|onmap|אונמפ|nadlan\.gov|'
                 r'^כן$|^כן בבקשה$|מידע נדל|מידע נדלן|^נדל ן$|nadlan com', re.I)
CTR = lambda p: 0.28 if p <= 1.5 else 0.15 if p <= 2.5 else 0.10 if p <= 3.5 else 0.07 if p <= 4.5 else 0.05 if p <= 5.5 else 0.03 if p <= 10.5 else 0.01 if p <= 20.5 else 0.002


def reach(p):
    if p is None: return 0.10
    return 0.9 if p <= 10.5 else 0.75 if p <= 20.5 else 0.5 if p <= 30.5 else 0.3 if p <= 50.5 else 0.15


def key(s):
    s = re.sub(r'[\"\'״׳“”‘’?!,;:()\[\]{}<>|\\~`@%^=+*]', ' ', s); return ' '.join(s.split()).lower()


def main():
    vol = {}
    for r in csv.DictReader(open(os.path.join(D, 'dfs-search-volume.csv'), encoding='utf-8')):
        if r['search_volume'] in ('', 'None') or int(r['search_volume']) == 0: continue
        k = (r['market'], r['keyword'])
        vol[k] = (int(r['search_volume']), float(r['cpc_usd'] or 0), r['competition'])
    # GSC positions
    gq = {}
    for f, tag in (('gsc-90d-queries.csv', '90'),):
        for r in csv.DictReader(open(os.path.join(D, f), encoding='utf-8')):
            gq[key(r['query'])] = (float(r['position']), float(r['impressions']), float(r['clicks']))
    q28 = collections.defaultdict(lambda: [0, 0, 0])
    for r in csv.DictReader(open(os.path.join(D, 'gsc-28d-qp.csv'), encoding='utf-8')):
        a = q28[key(r['query'])]; a[0] += float(r['impressions']); a[1] += float(r['position']) * float(r['impressions']); a[2] += float(r['clicks'])
    pages = collections.defaultdict(list)
    for r in csv.DictReader(open(os.path.join(D, 'gsc-90d-qp.csv'), encoding='utf-8')):
        pages[key(r['query'])].append((float(r['impressions']), float(r['position']), urllib.parse.unquote(r['page']).replace('https://nad-lan.co.il', '')))
    labs = {}
    for r in csv.DictReader(open(os.path.join(D, 'dfs-ranked-keywords-nadlan.csv'), encoding='utf-8')):
        labs[key(r['keyword'])] = (int(r['rank']), urllib.parse.unquote(r['url']).replace('https://nad-lan.co.il', ''))
    serp = {}
    for f in glob.glob(os.path.join(D, 'dfs', 'serp-*.json')):
        j = json.load(open(f, encoding='utf-8'))
        try: res = j['tasks'][0]['result'][0]
        except Exception: continue
        kw = key(res['keyword']); ours = None; gov = 0; doms = []
        for it in res.get('items') or []:
            if it['type'] != 'organic': continue
            dm = it.get('domain') or ''
            if 'nad-lan.co.il' in dm and ours is None: ours = (it['rank_group'], urllib.parse.unquote(it['url']).replace('https://nad-lan.co.il', ''))
            if it['rank_group'] <= 5:
                doms.append(dm)
                if re.search(r'gov\.il|bank|leumi|hapoalim|mizrahi|discount|wikipedia|kolzchut', dm): gov += 1
        serp[kw] = (ours, gov, doms, res.get('item_types'))
    rows = []
    for (mk, kw), (v, c, comp) in vol.items():
        if not MONEY.search(kw) or NAV.search(kw): continue
        g = gq.get(kw); l = labs.get(kw); s = serp.get(kw)
        a28 = q28.get(kw)
        pos_g = round(g[0], 1) if g else None
        pos_28 = round(a28[1] / a28[0], 1) if a28 and a28[0] else None
        pos_l = l[0] if l else None
        pos_s = s[0][0] if s and s[0] else None
        cands = [p for p in (pos_28, pos_g, pos_l, pos_s) if p]
        cur = pos_s if pos_s else (pos_28 if pos_28 else (min(cands) if cands else None))
        if s and not s[0] and mk == 'IL':
            base = pos_28 or pos_g or pos_l
            cur = max(base, 21) if base else None  # live desktop SERP: not in top ~20
        pg = sorted(pages.get(kw, []), reverse=True)
        main_page = pg[0][2] if pg else (s[0][1] if s and s[0] else (l[1] if l else ''))
        n_pages = len([p for p in pg if p[0] > 0])
        diff = 0.5 if (s and s[1] >= 2) else 1.0
        target_ctr = CTR(3)
        gain = max(0.0, v * (target_ctr - (CTR(cur) if cur else 0)))
        opp = gain * c * reach(cur) * diff
        rows.append([mk, kw, v, round(c, 2), comp, pos_28, pos_g, pos_l, pos_s if s else ('-' if not s else 'not top20'),
                     cur, main_page, n_pages, round(v * c), round(gain, 1), round(opp, 1), diff,
                     ' '.join((s[2] if s else [])[:5])])
    rows.sort(key=lambda r: -r[14])
    seen = set(); ded = []
    for r in rows:
        g = (r[0], r[2], r[3])
        if g in seen: continue
        seen.add(g); ded.append(r)
    rows = ded
    with open(os.path.join(OUT, 'money-words-ranked.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['market', 'keyword', 'ads_volume', 'cpc_usd', 'competition', 'gsc_pos_28d', 'gsc_pos_90d', 'labs_rank',
                    'serp_rank_live', 'current_pos_used', 'our_main_page', 'our_pages_with_impr_90d', 'value_vol_x_cpc',
                    'click_gain_at_pos3', 'opportunity_usd_month', 'serp_difficulty_factor', 'serp_top5_domains'])
        w.writerows(rows)
    print(len(rows))
    for r in rows[:60]: print(r[14], r[0], r[2], r[3], 'cur', r[9], r[1], '->', r[10], '|', r[16][:80])


if __name__ == '__main__':
    main()
