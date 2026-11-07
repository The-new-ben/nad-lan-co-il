"""nlbudget build (7.11.2026, HAD-678): writes plugins/nadlan-config/assets/instruments/data/nlbudget.json, the only numbers the
"כמה עולה לשווק את הפרויקט" tool shows.

Every figure comes from the teardown (teardown/pages.json, teardown/union.md), the competitor evidence base
(competitors/services.json) or NadLan's own approved plan prices (PLAN.md section 5). Each figure carries its value or range, unit,
currency, scope (il / abroad) and country, the source name (he / en), the source URL, the source date, the retrieval date, the flag as
union.md marks it, and an evidence record: the verbatim value string of the source record. The script refuses to write the file when a
number of a figure does not appear in its evidence string, or when an evidence string is not found verbatim in its file. Nothing here
is estimated, converted or averaged: derived values (ratios, products) are computed by the tool from these figures.

Run from anywhere:  python docs/research/2026-11-07-campaign-network/build/build-nlbudget/build_nlbudget_data.py
"""
import json, pathlib, re, sys

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
RES = HERE.parents[1]                      # docs/research/2026-11-07-campaign-network
REPO = HERE.parents[4]
OUT = REPO / 'plugins/nadlan-config/assets/instruments/data/nlbudget.json'
PAGES = json.loads((RES / 'teardown/pages.json').read_text(encoding='utf-8'))
SERV = json.loads((RES / 'competitors/services.json').read_text(encoding='utf-8'))
PLAN_MD = (RES / 'PLAN.md').read_text(encoding='utf-8')
BYID = {p['id']: p for p in PAGES['pages']}
RETRIEVED = '2026-11-07'

# the source names as the tool shows them; Latin brands stay Latin in Hebrew too
SRC = {
    'B01':  ('סמרנקו', 'Semerenko'),
    'B01c': ('סמרנקו', 'Semerenko'),
    'B01e': ('סמרנקו', 'Semerenko'),
    'B04':  ('מיראי', 'Mirai'),
    'B05b': ('פיקסל נדל״ן', 'Pixel Nadlan'),
    'B06':  ('סטארט פוינט', 'Start Point'),
    'B08a': ('WE DO MEDIA', 'WE DO MEDIA'),
    'B10':  ('גלובס, לפי יפעת בקרת פרסום', 'Globes, from Ifat ad monitoring'),
    'A01':  ('The Urban Developer, אוסטרליה', 'The Urban Developer, Australia'),
    'A02':  ('Feasly, אוסטרליה', 'Feasly, Australia'),
    'A03':  ('LocaliQ, ארצות הברית', 'LocaliQ, USA'),
    'A06':  ('Maverick Frame', 'Maverick Frame'),
    'A07':  ('Pro Builder, ארצות הברית', 'Pro Builder, USA'),
    'R01':  ('מבטים, מחירון הדמיות', 'Mabatim render price list'),
}

def page_date(pid):
    p = BYID[pid]
    if p['id'] == 'A07': return '2004'   # union.md: "2004 (schema date)"
    d = [x for x in (p.get('published'), p.get('modified')) if x]
    return ' / '.join(dict.fromkeys(d)) if d else None

def ev_page(pid, match, claim=None):
    """the verbatim value string of the pages.json number record of page pid that contains match (and claim, in its claim text)"""
    hits = [n['value'] for n in BYID[pid]['numbers'] if match in n['value'] and (claim is None or claim in n['claim'])]
    if len(hits) != 1: raise SystemExit(f'evidence {pid} "{match}": {len(hits)} records')
    return {'file': 'teardown/pages.json', 'id': pid, 'value': hits[0]}

def ev_bench(bid, field='values'):
    b = [x for x in SERV['cost_benchmarks'] if x['id'] == bid]
    if len(b) != 1: raise SystemExit('benchmark ' + bid)
    return {'file': 'competitors/services.json', 'id': bid + ('' if field == 'values' else '.' + field), 'value': b[0][field]}

def ev_serv(sid):
    s = [x for x in SERV['services'] if x['id'] == sid]
    if len(s) != 1: raise SystemExit('service ' + sid)
    return {'file': 'competitors/services.json', 'id': sid, 'value': s[0]['prices_and_terms']['value']}

FLAG = {  # pages.json evidence classes -> the union.md flags
    'cited': 'cited', 'agency claim': 'agency claim', 'agency claim citing unnamed reports or price lists': 'agency claim, unnamed source',
    'illustrative example': 'example', 'vendor price list': 'price list'}

def fig(fid, pid, match, unit, he, en, flag=None, currency='ILS', scope='il', country='IL', **kw):
    e = ev_page(pid, match)
    rec = [n for n in BYID[pid]['numbers'] if n['value'] == e['value']][0]
    f = {'id': fid, 'unit': unit, 'currency': currency, 'scope': scope, 'country': country,
         'src': pid, 'src_he': SRC[pid][0], 'src_en': SRC[pid][1], 'url': BYID[pid]['url'], 'date': page_date(pid), 'retrieved': RETRIEVED,
         'flag': flag or FLAG[rec['evidence']], 'he': he, 'en': en, 'ev': [e]}
    f.update(kw)
    return f

AU = dict(currency='AUD', scope='abroad', country='AU')
US = dict(currency='USD', scope='abroad', country='US')
PCT = dict(currency=None)

FIG = [
    # (1) the budget as a share of sales
    fig('wedo_total', 'B08a', 'about 1% of every apartment', 'pct_sales', 'תקציב השיווק: כ־1% מסך מחירי הדירות בפרויקט', 'Marketing budget: about 1% of the total price of the apartments in the project', v=1, approx='about', **PCT),
    fig('wedo_online', 'B08a', 'about 1% of every apartment', 'pct_sales', 'מתוכו כ־0.75% לפרסום ברשת', 'of which about 0.75% for online advertising', v=0.75, approx='about', **PCT),
    fig('sp_sm', 'B06', '2% to 4% of sales volume', 'pct_sales', 'שיווק ומכירה, כולל צוות מכירות ופרסום', 'Marketing and sales, including the sales team and advertising', lo=2, hi=4, **PCT),
    fig('fe_mkt', 'A02', '0.75% to 2% of GRV', 'pct_sales', 'שיווק בלבד, בלי עמלת מכירה', 'Marketing only, without sales commission', lo=0.75, hi=2, scope='abroad', country='AU', currency=None),
    fig('fe_sm', 'A02', '3% to 5% of GRV', 'pct_sales', 'שיווק ומכירה יחד, כולל עמלה', 'Marketing and selling together, commission included', lo=3, hi=5, scope='abroad', country='AU', currency=None),
    fig('ud_mkt', 'A01', 'between 1 and 2 per cent', 'pct_sales', 'שיווק פרויקט על הנייר, בכתבה ממומנת של משרד פרסום', 'Off-the-plan marketing, in a sponsored piece by an agency', lo=1, hi=2, scope='abroad', country='AU', currency=None),
    fig('mf_mkt', 'A06', 'between 1% and 5%', 'pct_sales', 'עלות שיווק מקובלת ליזם, לפי סטודיו הדמיות', 'Typical developer marketing cost, per a render studio', lo=1, hi=5, scope='abroad', country=None, currency=None),
    fig('pb_sm', 'A07', '6% of home building revenue', 'pct_sales', 'שיווק ומכירה אצל בוני בתים: יעד של 6%, ולעיתים קרובות 8% עד 10% בפועל', 'Sales and marketing at home builders: a 6% target, often 8% to 10% in practice', lo=6, hi=10, target=6, often=[8, 10], scope='abroad', country='US', currency=None),
    fig('se_ex', 'B01', '60 units x 2.4 million', 'example', 'הדוגמה: 60 דירות במחיר ממוצע של 2.4 מיליון ₪, מכירות של כ־144 מיליון ₪, מסגרת שיווק של כ־1.4 מיליון ₪', 'The example: 60 apartments at an average of 2.4 million ₪, about 144 million ₪ of sales, a marketing frame of about 1.4 million ₪', units=60, price=2400000, sales=144000000, mkt=1400000),
    fig('se_window', 'B01c', '12 to 24 months', 'months', 'חלון מכירה של 12 עד 24 חודשים', 'A sales window of 12 to 24 months', lo=12, hi=24, currency=None),
    # (2) advertising per apartment sold
    fig('sp_unit', 'B06', '3,000 to 23,000', 'ils_per_unit', 'פרסום בלבד לכל דירה שנמכרת, לפי דיווחים על יזמים גדולים', 'Advertising alone per apartment sold, per reports on large developers', lo=3000, hi=23000),
    # (3) cost per lead
    fig('sp_leads', 'B06', 'from 173', 'ils_per_lead', 'מחירון לידים בלעדיים לדירות חדשות: 173 ₪ לליד בחבילה של 25, עד 128 ₪ בחבילה של 500, לפני מע״מ, מחירון 4.11.2026', 'Exclusive new-apartment lead price list: 173 ₪ a lead in a pack of 25 down to 128 ₪ in a pack of 500, before VAT, price list of 4.11.2026', lo=128, hi=173, packs=[25, 500], vat='before'),
    fig('se_cpl', 'B01', '₪300 to ₪800', 'ils_per_lead', 'עלות ליד בפועל בקמפיינים של פרויקטים, ולעיתים יותר מ־1,000 ₪', 'Actual cost per lead in project campaigns, sometimes above 1,000 ₪', lo=300, hi=800, over=1000),
    dict(fig('lq_cpl', 'A03', 'CPL $102.51', 'usd_per_lead', 'מודעות חיפוש בנדל״ן בארצות הברית, חציון: 102.51 דולר לליד בכל הנדל״ן, 142.59 דולר לבתים למכירה דרך מתווך; 894 קמפיינים, אפריל 2025 עד מרץ 2026; אין קטגוריה של דירות חדשות', 'US real-estate search ads, medians: $102.51 a lead for all real estate, $142.59 for homes for sale by agent; 894 campaigns, Apr 2025 to Mar 2026; no new-construction category', lo=102.51, hi=142.59, n_campaigns=894, **US), ev=[ev_page('A03', 'CPL $102.51'), ev_page('A03', 'CPL: Apartments'), ev_bench('localiq-search-real-estate-2026'), ev_bench('localiq-search-real-estate-2026', 'period')]),
    # how many leads make a deal: the sources' own worked examples (the tool shows them as a hint, never as a default)
    fig('se_funnel', 'B01e', 'unique inquiries 400 vs 200', 'example', 'דוגמה של שני ערוצים: 400 פניות ו־2 עסקאות, מול 200 פניות ו־5 עסקאות', 'A two-channel example: 400 inquiries and 2 deals, against 200 inquiries and 5 deals', inq=[400, 200], deals=[2, 5]),
    fig('mi_funnel', 'B04', '576 leads', 'example', 'דוגמה: 576 פניות ל־12 עסקאות בחצי שנה', 'An example: 576 leads for 12 deals in six months', leads=576, deals=12),
    # renders, sales plans, film (Israeli price list)
    fig('mb_ext3', 'R01', 'exterior set 3 angles', 'ils', 'סט הדמיות חוץ, 3 זוויות', 'Exterior render set, 3 angles', lo=4000, hi=6000, angles=3),
    fig('mb_plan3d', 'R01', 'colour sales plan', 'ils_per_unit', 'תוכנית מכר בתלת ממד, לדירה', '3D sales plan, per apartment', lo=1000, hi=1500),
    fig('mb_plancol', 'R01', 'colour sales plan', 'ils_per_unit', 'תוכנית מכר צבעונית, לדירה', 'Colour sales plan, per apartment', lo=500, hi=750),
    fig('mb_film', 'R01', 'short video 30-60 seconds', 'ils', 'סרט הדמיה של דקה עד 3 דקות', 'Render film of 1 to 3 minutes', lo=12000, hi=30000, minutes=[1, 3]),
    fig('mb_film_s', 'R01', 'short video 30-60 seconds', 'ils', 'סרט קצר של 30 עד 60 שניות', 'Short film of 30 to 60 seconds', lo=7000, hi=15000, seconds=[30, 60]),
    # the worked example abroad (Feasly, Australia): lines, cash-out timing, a longer sale
    fig('fe_ex', 'A02', '60 apartments, GRV', 'aud', 'דוגמה: 60 דירות, מכירות של 60 מיליון דולר אוסטרלי, שיווק 1.2% (720,000)', 'Example: 60 apartments, 60 million Australian dollars of sales, marketing 1.2% (720,000)',
        units=60, grv=60000000, total=720000, pct=1.2, brand=60000, cgi=120000, suite_fit=320000, suite_run=90000, suite_months=18, media=90000, sign=40000, comm_pct=2.5, comm=1500000, combined=2220000, combined_pct=3.7, **AU),
    fig('fe_pre', 'A02', 'about $530,000 of $720,000', 'aud', 'כ־530,000 מתוך 720,000 הוצאו לפני ההשקה', 'About 530,000 of the 720,000 was spent before launch', v=530000, of=720000, approx='about', **AU),
    fig('fe_delay', 'A02', '+12 months', 'aud', 'אם המכירה נמשכת עוד 12 חודשים: עוד 60,000 לחלל המכירות, 70,000 למדיה ו־30,000 לקריאייטיב חדש; השיווק עולה ל־880,000 (1.47%)', 'If the sale runs 12 more months: 60,000 more for the display suite, 70,000 for media, 30,000 for relaunch creative; marketing rises to 880,000 (1.47%)',
        suite=60000, media=70000, creative=30000, total=880000, pct=1.47, months=12, **AU),
    fig('fe_suite', 'A02', 'roughly $150,000', 'aud', 'חלל תצוגה ומכירה: בדרך כלל השורה הגדולה ביותר בשיווק', 'Display suite: usually the largest marketing line', lo=150000, hi=700000, hi_more=True, **AU),
    fig('fe_comm', 'A02', '2% to 3% of sale price', 'pct_price', 'עמלת סוכנות על מכירה ישירה, ממחיר הדירה', 'Agency commission on a direct sale, of the sale price', lo=2, hi=3, scope='abroad', country='AU', currency=None),
    fig('sp_broker', 'B06', '1% to 2% of the apartment price', 'pct_price', 'דמי תיווך, רק כשמתווך מביא את הקונה, בתוספת מע״מ', 'Brokerage fee, only when a broker brings the buyer, plus VAT', lo=1, hi=2, vat='plus', currency=None),
    # Israeli campaign context (Globes, from Ifat ad monitoring: list prices, not necessarily actual spend)
    dict(fig('gl_2025', 'B10', 'Aura:', 'ils_million', 'השקעה בפרסום ב־2025 לפי בקרת הפרסום של יפעת, במחירון ולא בהכרח בפועל', 'Ad investment in 2025 per Ifat ad monitoring, at list price, not necessarily actual spend',
        list=[{'he': 'אאורה', 'en': 'Aura', 'v': 62, 'approx': 'almost'}, {'he': 'תדהר', 'en': 'Tidhar', 'v': 15}, {'he': 'ישראל קנדה', 'en': 'Israel Canada', 'v': 30.5},
              {'he': 'חגג', 'en': 'Hagag', 'v': 11.5}, {'he': 'דמרי', 'en': 'Dimri', 'v': 6.5}]),
        ev=[ev_page('B10', 'Aura:'), ev_page('B10', 'Tidhar:'), ev_page('B10', 'Israel Canada:'), ev_page('B10', 'Hagag:'), ev_page('B10', 'Dimri:')]),
    dict(fig('gl_camp', 'B10', 'about 2 million', 'ils_million', 'קמפיינים שדווחו: כ־2 מיליון ₪ (ברזני, קצרין: טלוויזיה, רשת ורשתות חברתיות) עד כ־5 מיליון ₪ (דמרי, DIMRI YAMA)', 'Reported campaigns: about 2 million ₪ (Barazani, Katzrin: TV, online, social) to about 5 million ₪ (Dimri, DIMRI YAMA)',
        lo=2, hi=5, approx='about'), ev=[ev_page('B10', 'about 2 million'), ev_page('B10', 'about 5 million ₪', 'Dimri Yama')]),
    # Israeli timing (agency claim)
    fig('px_time', 'B05b', 'strategy and branding 4-8 weeks', 'weeks', 'אסטרטגיה ומיתוג 4 עד 8 שבועות, טרום שיווק 4 עד 8 שבועות, פריסייל 2 עד 6 שבועות, השקה שבוע אחד', 'Strategy and branding 4 to 8 weeks, pre-launch 4 to 8 weeks, presale 2 to 6 weeks, launch one week',
        parts=[[4, 8], [4, 8], [2, 6]], currency=None)  # the launch week is written in words ("one concentrated week"), kept in the text only,
]

# exhibitions for buyers abroad: four checked, no exhibitor price published (our own check, services.json)
EXPO = ['great-israeli-real-estate-event', 'israeli-building-center-diaspora-expos', 'icube-salon-paris', 'bmby-virtual-fair']
FIG.append({'id': 'expo_np', 'unit': 'none', 'currency': None, 'scope': 'abroad', 'country': None, 'src': 'services', 'src_he': 'בדיקה של נדל״ן', 'src_en': 'NadLan check',
            'url': None, 'date': RETRIEVED, 'retrieved': RETRIEVED, 'flag': 'not published', 'n': len(EXPO),
            'he': 'נבדקו 4 תערוכות ויריד לקונים מחו״ל: באף אחד לא פורסם מחיר למציגים', 'en': '4 exhibitions and fairs for buyers abroad were checked: none publishes an exhibitor price',
            'ev': [ev_serv(s) for s in EXPO]})

# the lines no page prices in Israel: the teardown itself (union.md, 50 pages read on 7.11.2026, every number in its data table)
UNION = (RES / 'teardown/union.md').read_text(encoding='utf-8')
TD_LINE = [l for l in UNION.splitlines() if l.startswith('Retrieved 7 Nov 2026. 50 pages read')]
if len(TD_LINE) != 1: raise SystemExit('union.md retrieved line')
FIG.append({'id': 'td_np', 'unit': 'none', 'currency': None, 'scope': 'il', 'country': 'IL', 'src': 'union', 'src_he': 'בדיקה של נדל״ן', 'src_en': 'NadLan check',
            'url': None, 'date': RETRIEVED, 'retrieved': RETRIEVED, 'flag': 'not published', 'pages': 50,
            'he': 'לא פורסם מחיר ישראלי באף אחד מ־50 העמודים המובילים שנקראו', 'en': 'No Israeli price in any of the 50 top-ranking pages read',
            'ev': [{'file': 'teardown/union.md', 'id': 'line 3', 'value': TD_LINE[0]}]})

# NadLan's own plans (approved by Ben 7.11.2026, PLAN.md section 5)
PLAN_LINE = [l for l in PLAN_MD.splitlines() if l.startswith('APPROVED by Ben 7.11.2026')]
if len(PLAN_LINE) != 1: raise SystemExit('PLAN.md approved line')
PLANS = {'one': 36000, 'three': 72000, 'flag': 144000}
FIG.append({'id': 'nl_plans', 'unit': 'ils_year', 'currency': 'ILS', 'scope': 'il', 'country': 'IL', 'src': 'nadlan', 'src_he': 'נדל״ן', 'src_en': 'NadLan',
            'url': None, 'date': '2026-11-07', 'retrieved': RETRIEVED, 'flag': 'own price', 'plans': PLANS,
            'he': 'עמוד הפרויקט בנדל״ן עם הסיור הווירטואלי: כלול במנוי השנתי', 'en': 'The project page on NadLan with the virtual tour: included in the annual plan',
            'ev': [{'file': 'PLAN.md', 'id': 'section 5', 'value': PLAN_LINE[0]}]})

# the rows of the budget sheet. kind: own (no Israeli price: the developer enters his figure), once / unit (a published range, once or
# per apartment), pct (about a share of sales), plan (included in the NadLan plan), fee (who sells). stage: where the line sits
# (pre = before marketing starts, launch, build = during construction, last = last units, all); placement per B05b's timeline and B01's
# line list ("one-time before launch", "renewed by construction stage", "ongoing").
LINES = [
    {'id': 'research', 'kind': 'own', 'stage': ['pre'], 'ctx': []},
    {'id': 'brand', 'kind': 'own', 'stage': ['pre'], 'ctx': ['fe_ex:brand']},
    {'id': 'ext3', 'kind': 'once', 'fig': 'mb_ext3', 'stage': ['pre'], 'ctx': []},
    {'id': 'plan3d', 'kind': 'unit', 'fig': 'mb_plan3d', 'stage': ['pre'], 'ctx': ['mb_plancol']},
    {'id': 'film', 'kind': 'once', 'fig': 'mb_film', 'stage': ['launch'], 'ctx': ['mb_film_s', 'fe_ex:cgi']},
    {'id': 'tour', 'kind': 'plan', 'fig': 'nl_plans', 'stage': ['pre'], 'ctx': []},
    {'id': 'photo', 'kind': 'own', 'stage': ['build'], 'ctx': []},
    {'id': 'site', 'kind': 'own', 'stage': ['pre'], 'ctx': []},
    {'id': 'crm', 'kind': 'own', 'stage': ['all'], 'ctx': []},
    {'id': 'media', 'kind': 'pct', 'fig': 'wedo_online', 'stage': ['all'], 'ctx': ['fe_ex:media']},
    {'id': 'outdoor', 'kind': 'own', 'stage': ['pre', 'launch'], 'ctx': ['fe_ex:sign']},
    {'id': 'print', 'kind': 'own', 'stage': ['launch'], 'ctx': []},
    {'id': 'tv', 'kind': 'own', 'stage': ['launch'], 'ctx': ['gl_camp']},
    {'id': 'pr', 'kind': 'own', 'stage': ['all'], 'ctx': []},
    {'id': 'events', 'kind': 'own', 'stage': ['launch', 'build'], 'ctx': ['expo_np']},
    {'id': 'office', 'kind': 'own', 'stage': ['launch', 'build'], 'ctx': ['fe_suite']},
    {'id': 'fee', 'kind': 'fee', 'stage': ['all'], 'ctx': ['sp_broker', 'fe_comm']},
]

# --------------------------------------------------------------------------------------------- the checks before writing
def nums(f):
    out = []
    for k in ('v', 'lo', 'hi', 'over', 'target', 'units', 'price', 'sales', 'mkt', 'grv', 'total', 'pct', 'brand', 'cgi', 'suite_fit', 'suite_run',
              'suite_months', 'media', 'sign', 'comm_pct', 'comm', 'combined', 'combined_pct', 'of', 'suite', 'creative', 'months', 'leads', 'deals', 'inq',
              'often', 'packs', 'n_campaigns', 'angles', 'minutes', 'seconds', 'pages'):
        x = f.get(k)
        if isinstance(x, list): out += x
        elif isinstance(x, (int, float)) and not isinstance(x, bool): out.append(x)
    for it in f.get('list', []): out.append(it['v'])
    for p in f.get('parts', []): out += p
    out += list(f.get('plans', {}).values())
    return out

def forms(x):
    s = []
    if float(x).is_integer():
        i = int(x); s += [f'{i:,}', str(i)]
        if i >= 1_000_000: s.append(f'{i / 1e6:g} million')
    else:
        s.append(f'{x:g}'); s.append(f'{x:.2f}')
    return s

bad = []
for f in FIG:
    text = ' || '.join(e['value'] for e in f['ev'])
    for e in f['ev']:
        raw = (RES / e['file']).read_text(encoding='utf-8')
        if json.dumps(e['value'], ensure_ascii=False)[1:-1] not in raw and e['value'] not in raw: bad.append(f"{f['id']}: evidence not verbatim in {e['file']}")
    for x in nums(f):
        if not any(re.search(r'(?<![\d.,])' + re.escape(fm) + r'(?![\d]|[.,]\d)', text) for fm in forms(x)): bad.append(f"{f['id']}: {x} not in its evidence")
    if 'n' in f and f['n'] != len(f['ev']): bad.append(f"{f['id']}: n is not the number of records checked")
    if f['flag'] not in ('cited', 'price list', 'agency claim', 'agency claim, unnamed source', 'example', 'own price', 'not published'): bad.append(f['id'] + ': flag')
ids = {f['id'] for f in FIG}
for ln in LINES:
    for r in [ln.get('fig')] + [c.split(':')[0] for c in ln['ctx']]:
        if r and r not in ids: bad.append(ln['id'] + ': unknown figure ' + r)
if bad:
    print('\n'.join(bad)); raise SystemExit(1)

data = {
    'key': 'nlbudget', 'v': 1, 'asof': RETRIEVED,
    'note': 'Every number of the tool "כמה עולה לשווק את הפרויקט" (HAD-678). Built by docs/research/2026-11-07-campaign-network/build/build-nlbudget/build_nlbudget_data.py '
            'from teardown/pages.json, competitors/services.json and PLAN.md (retrieved 7.11.2026). Flags as union.md marks them. Prices as each source published them; '
            'no conversion between currencies. ev = the verbatim value string of the source record.',
    'flags': ['cited', 'price list', 'agency claim', 'agency claim, unnamed source', 'example', 'own price', 'not published'],
    'figures': {f['id']: {k: v for k, v in f.items() if k != 'id'} for f in FIG},
    'lines': LINES,
    'stages': ['pre', 'launch', 'build', 'last'],
    'example': {'units': 60, 'price': 2400000, 'months': 24, 'from': ['se_ex', 'se_window']},
    'plans_href': {'he': '/marketing/', 'en': '/en/marketing/'},
}
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(f'{len(FIG)} figures, {len(LINES)} lines, every number found in its evidence -> {OUT.relative_to(REPO)} ({OUT.stat().st_size:,} bytes)')
