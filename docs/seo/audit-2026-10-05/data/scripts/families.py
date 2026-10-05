# -*- coding: utf-8 -*-
import csv, re, collections, os
D = r'C:\Users\777\nad-lan\nad-lan-co-il\docs\seo\audit-2026-10-05\data'
R = list(csv.DictReader(open(os.path.join(D, 'derived', 'money-words-ranked.csv'), encoding='utf-8')))
labs = {r['keyword']: r for r in csv.DictReader(open(os.path.join(D, 'dfs-ranked-keywords-nadlan.csv'), encoding='utf-8'))}
have = set(r['keyword'] for r in R)
CTR = lambda p: 0.28 if p <= 1.5 else 0.15 if p <= 2.5 else 0.10 if p <= 3.5 else 0.07 if p <= 4.5 else 0.05 if p <= 5.5 else 0.03 if p <= 10.5 else 0.01 if p <= 20.5 else 0.002
reach = lambda p: 0.10 if p is None else 0.9 if p <= 10.5 else 0.75 if p <= 20.5 else 0.5 if p <= 30.5 else 0.3 if p <= 50.5 else 0.15
extra = {'גינדי שדה דב': None, 'מגדלי כיכר המדינה': (260, 3.52, None)}
for k, val in extra.items():
    if k in have: continue
    if val is None:
        l = labs[k]; v = int(l['search_volume'] or 0); c = float(l['cpc_usd'] or 0); p = int(l['rank'])
    else:
        v, c, p = val
    opp = v * (0.10 - (CTR(p) if p else 0)) * c * reach(p)
    R.append({'market': 'IL', 'keyword': k, 'ads_volume': str(v), 'cpc_usd': str(c), 'current_pos_used': str(p or ''),
              'our_main_page': '', 'opportunity_usd_month': str(round(opp, 1))})
CITIES = 'ירושלים|פתח תקווה|ראשון לציון|רמת גן|חיפה|בת ים|באר שבע|אשדוד|נתניה|חולון|רחובות|כפר סבא|רעננה|אשקלון|חדרה|לוד|נהריה|קרית אונו|באר יעקב|גבעתיים|יהוד|נס ציונה|יבנה|מודיעין|נעלה|בלוד|ביבנה'
F = [
    ('Sde Dov hub', '/sde-dov/', r'^(שדה דב|שדה דוב|רובע שדה דב|שדה דב תל אביב|שכונת שדה דב)$'),
    ('Sde Dov projects', '/sde-dov/', r'^(שדה דב פרויקטים|פרויקט שדה דב|פרויקטים בשדה דב|פרויקטים שדה דב)$'),
    ('Sde Dov for sale / prices', '/sde-dov/prices/', r'^(דירות למכירה בשדה דב|דירה למכירה בשדה דב|דירות בשדה דב|שדה דב דירות|שדה דב למכירה|שדה דב מחירים|מחירי דירות בשדה דב)$'),
    ('Sde Dov in English', 'none: English twin of /sde-dov/', r'^(sde dov|sde dov tel aviv)$'),
    ('Gindi Vogue (Sde Dov)', '/projects/gindi-vogue-sde-dov/', r'גינדי'),
    ('Dimri Yama (Sde Dov)', '/projects/dimri-yama-sde-dov/', r'דמרי|דימרי|dimri'),
    ('Ashira (Sde Dov)', '/projects/ashira-sde-dov/', r'אשירה|אביסרור שדה|ashira'),
    ('Rainbow (Sde Dov)', '/projects/rainbow-tel-aviv/', r'ריינבו|rainbow'),
    ('DUO Tel Aviv', '/projects/duo-tel-aviv/', r'^duo|duo$|דואו'),
    ('Kikar Hamedina towers', '/projects/hamedina/ (+ -en)', r'כיכר המדינה|kikar|hamedina'),
    ('New projects in Tel Aviv', '/new-projects/new-projects-tel-aviv/', r'^(פרויקטים|פרויקט|פרוייקטים|דירות חדשות|דירות מקבלן|דירה חדשה מקבלן|דירות חדשות למכירה)( חדשים)? ?(ב)?תל אביב( מחירים)?$|^פרויקט תל אביב$'),
    ('New projects by city (no owner since 25.8)', 'none', r'^(פרויקטים|פרוייקטים|דירות חדשות|פינוי בינוי)( חדשים)? ?(ב)?(' + CITIES + ')$'),
    ('New projects generic', '/projects/', r'^(פרויקטים חדשים|פרוייקטים חדשים|פרויקטים|פרוייקטים|דירות מקבלן|דירה מקבלן|דירות קבלן|דירות חדשות|דירות חדשות למכירה|דירות חדשות מקבלן|דירה חדשה מקבלן|דירה חדשה|פרויקט נדלן|פרויקט דירות|פרויקטים חדשים על הנייר|פרויקטים בבנייה|פרוייקטים בבנייה|פרויקט מגורים|פרויקט בנייה|בניינים חדשים|בתים חדשים|פרויקטים חדשים בישראל|פרויקטים חדשים במרכז|פרויקטים בבניה)$'),
    ('Home head term נדלן', '/ (home)', r'^(נדלן|נדל ן)$'),
    ('Listings: דירות למכירה (+ cities)', '/properties/ (needs inventory)', r'^(דירות למכירה|דירות|נדלן למכירה|בתים למכירה|דירות למכירה ב.+|מגרשים למכירה)$'),
    ('Rentals: דירות להשכרה', 'none (rentals track)', r'^דירות להשכרה'),
    ('Mortgage calculator', '/mortgage-calculator/', r'מחשבון משכנת|משכנתא מחשבון|חישוב משכנתא|^משכנתא$|החזר משכנתא|בדיקת משכנתא|מחשבון מימון|הלוואת בלון|תשלום משכנתא'),
    ('Reverse mortgage', '/mortgage-calculator/reverse-mortgage/', r'משכנתא הפוכה'),
    ('Mortgage adviser', 'none (pros category page)', r'יועץ משכנתאות'),
    ('Valuation', '/property-value-estimator/', r'הערכת שווי|שמאות דירה|כמה שווה|מחשבון שווי|בדיקת שווי|הערכת נכס'),
    ('Investment', '/investment/', r'השקע|להשקעה'),
    ('Real estate abroad', '/global/', r'בחול|באנגליה|במיאמי'),
    ('Purchase tax', '/purchase-tax-calculator/', r'מס רכישה'),
    ('Capital gains tax (מס שבח)', '/real-estate-tax-advisor/capital-gains-tax-guide/', r'מס שבח'),
    ('Tabu extract', '/tabu-extract-check/', r'טאבו'),
    ('Home inspection (בדק בית)', '/home-inspection/', r'בדק בית'),
    ('Real-estate lawyer', '/real-estate-lawyer/', r'עורך דין'),
    ('Appraiser (שמאי)', '/real-estate-appraiser/ + glossary', r'שמאי'),
    ('Brokers (מתווך)', '/brokers/', r'מתווך|משרד תיווך'),
    ('Developers (חברות בנייה)', 'developers directory', r'חברות בני|יזמי'),
    ('Urban renewal head', '/urban-renewal/', r'^התחדשות עירונית$'),
    ('Pinui binui head (+TLV)', '/urban-renewal/pinui-binui/', r'^פינוי בינוי( תל אביב)?$'),
    ('Urban renewal projects / map', '/urban-renewal/map/', r'מפת התחדשות|מתחמי פינוי|פרויקט(ים)? (ב)?(פינוי|התחדשות)|פרויקטים של פינוי'),
    ('TAMA 38', '/urban-renewal/tama-38/', r'תמא'),
    ('Offices for rent / sale', '/commercial-real-estate/office-for-rent/', r'^משרדים (ל|ב)'),
    ('Penthouses', '/tel-aviv-penthouse-prices/', r'פנטהאוז'),
    ('Gov programs: מחיר למשתכן / דירה בהנחה', 'none', r'מחיר למשתכן|דירה בהנחה'),
    ('Yield calculator (מחשבון תשואה)', '/investment-property-cashflow-calculator/', r'תשואה'),
    ('Lease contract (חוזה שכירות)', '/residential-lease-agreement/', r'חוזה שכירות'),
    ('Property management (ניהול נכסים)', '/property-management/', r'ניהול נכס'),
    ('Deals data (עסקאות נדלן)', 'none (gov-dominated)', r'^עסקאות נדלן|עסקת נדלן'),
    ('Luxury Tel Aviv', '/luxury-tel-aviv/', r'יוקרה'),
    ('English portal terms', '/en/', r'real estate|apartments? for sale|property in israel'),
]
fam = collections.OrderedDict(); used = set()
for name, owner, pat in F:
    rows = [r for r in R if r['market'] in ('IL', 'US') and re.search(pat, r['keyword'], re.I) and (r['market'], r['keyword']) not in used]
    for r in rows: used.add((r['market'], r['keyword']))
    if not rows: continue
    opp = sum(float(r['opportunity_usd_month']) for r in rows)
    vol = sum(int(r['ads_volume']) for r in rows if r['market'] == 'IL')
    pos = [float(r['current_pos_used']) for r in rows if r['current_pos_used'] not in ('', 'None')]
    kws = sorted(rows, key=lambda r: -int(r['ads_volume']))[:4]
    fam[name] = (round(opp), vol, owner, round(min(pos), 1) if pos else '', '; '.join('%s%s %s/$%s' % ('[US] ' if r['market'] == 'US' else '', r['keyword'], r['ads_volume'], round(float(r['cpc_usd']), 2)) for r in kws), len(rows))
out = sorted(fam.items(), key=lambda kv: -kv[1][0])
with open(os.path.join(D, 'derived', 'money-families.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['family', 'opportunity_usd_month', 'ads_volume_IL_sum', 'owner_url', 'best_current_pos', 'top_keywords', 'n_keywords'])
    for k, v in out: w.writerow([k] + list(v))
for k, v in out: print(v[0], '|', v[1], '|', k, '|', v[2], '| pos', v[3], '|', v[4], '| n', v[5])
left = [r for r in R if (r['market'], r['keyword']) not in used and r['market'] in ('IL', 'US')]
left.sort(key=lambda r: -float(r['opportunity_usd_month']))
print('--- unassigned top')
for r in left[:25]: print(r['opportunity_usd_month'], r['keyword'], r['ads_volume'], r['cpc_usd'], r['our_main_page'])
