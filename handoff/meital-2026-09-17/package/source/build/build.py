#!/usr/bin/env python3
"""Build nad-lan Prestige listing blocks (HE/EN), WP payloads, JSON-LD, briefs and the preview."""
import json, re, os, sys, html, urllib.parse, statistics
from jinja2 import Environment, FileSystemLoader
sys.path.insert(0, os.path.dirname(__file__))
from nlxcalc import C, esc, fint, num, pct, sqm, purchase_taxes, fx, assert_no_dash

def money(n, lang):
    if n is None:
        return ''
    s = fint(n)
    if lang == 'he':
        return f'<span class="nlx-money"><span class="nlx-num">{s}</span>&nbsp;₪</span>'
    return f'<span class="nlx-money"><span class="nlx-num">NIS {s}</span></span>'

NUMRUN = re.compile(r'(?<![\w<>/="#&;])(\+?-?\d[\d,.]*%?(?:\s?(?:-|×|x|÷|/)\s?\d[\d,.]*%?)*)(?![\w"])')
def wrapnums(escaped):
    return NUMRUN.sub(lambda m: f'<span class="nlx-num">{m.group(1)}</span>', escaped)
def glue(h):
    return h.replace(' ₪', '&nbsp;₪').replace('NIS ', 'NIS&nbsp;').replace(' מיליון&nbsp;₪', '&nbsp;מיליון&nbsp;₪')
def tx(s):
    return glue(wrapnums(esc(s))) if s else ''


BASE = os.environ.get('NLX_BASE') or (os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/')
# Public URL patterns. Confirm against the live permalink structure after the drafts exist, then rebuild.
URL_PATTERN = {'he': 'https://nad-lan.co.il/properties/{slug}/', 'en': 'https://nad-lan.co.il/en/properties/{slug}/'}
B = BASE + 'build/'
OUT = BASE + 'dist/'
env = Environment(loader=FileSystemLoader(B + 'templates'), autoescape=True, trim_blocks=False, lstrip_blocks=False)

BROKER = {
    'name': {'he': 'מיטל קציר', 'en': 'Meital Katzir'},
    'brand': {'he': 'נדל״ן על הים', 'en': 'Real Estate by the Sea'},
    'license': '3131540', 'phone': '052-3631582', 'phone_intl': '+972523631582', 'phone_disp_en': '+972 52-363-1582',
    'wa': 'https://wa.me/972523631582',
}

T = {
 'he': dict(toc='תוכן העמוד', rail='מחיר ויצירת קשר', sec_home='הבית', sec_building='הבניין', sec_location='הסביבה',
   sec_future='תכנון סביב', future_h2='מה מתוכנן סביב הנכס', future_lead='תכניות ועבודות שפורסמו, והמשמעות האפשרית שלהן לרוכש או לשוכר. המידע מבוסס על פרסומים ואינו מחליף בדיקה במנהל התכנון.',
   sec_numbers='המספרים', sec_market='השוק', sec_checks='לפני החלטה', sec_faq='שאלות ותשובות', faq_h2='שאלות שכדאי לשאול', sec_broker='המשווקת בבלעדיות',
   sec_sources='מקורות, בסיס הנתונים והערות', distances='מרחקים', schools='חינוך', transport='תחבורה',
   tag_broker='לפי המשווקת', tag_calc='חישוב', tag_src='מקור', tag_tx='עסקה', tag_ask='מבוקש', tag_rep='דווח',
   toc_items=dict(home='הבית', building='הבניין', location='הסביבה', future='תכנון', numbers='המספרים', market='השוק', checks='בדיקות', faq='שאלות', sources='מקורות'),
   cta_wa='וואטסאפ למיטל', cta_wa_short='וואטסאפ', cta_call='חיוג', cta_call_short='חיוג', cta_view='תיאום סיור פרטי',
   rooms='חדרים', updated='עודכן', listing_code='קוד נכס', price_on_request='לפי פנייה',
   legend_broker='נתון שמסרה המשווקת ולא אומת באופן עצמאי', legend_calc='חישוב של nad-lan על בסיס נתונים מצוטטים', legend_src='מספר המקור ברשימה',
   comp_head_sale=['תאריך', 'מיקום', 'חדרים', 'מ״ר', 'קומה', 'מחיר', 'למ״ר', 'סוג'],
   comp_head_rent=['תאריך', 'מיקום', 'חדרים', 'מ״ר', 'שכ״ד לחודש', 'למ״ר', 'סוג'],
   ),
 'en': dict(toc='On this page', rail='Price and contact', sec_home='The residence', sec_building='The building', sec_location='The location',
   sec_future='Planning', future_h2='What is planned nearby', future_lead='Published plans and works, and what they may mean for a buyer or tenant. Based on published reports; not a substitute for a check with the planning authority.',
   sec_numbers='The numbers', sec_market='The market', sec_checks='Before you decide', sec_faq='Questions and answers', faq_h2='Questions worth asking', sec_broker='Exclusive listing broker',
   sec_sources='Sources, data basis and notes', distances='Distances', schools='Schools', transport='Transport',
   tag_broker='Broker-stated', tag_calc='Computed', tag_src='Source', tag_tx='Sale', tag_ask='Asking', tag_rep='Reported',
   toc_items=dict(home='Residence', building='Building', location='Location', future='Planning', numbers='Numbers', market='Market', checks='Checks', faq='FAQ', sources='Sources'),
   cta_wa='WhatsApp Meital', cta_wa_short='WhatsApp', cta_call='Call', cta_call_short='Call', cta_view='Book a private viewing',
   rooms='rooms', updated='Updated', listing_code='Listing code', price_on_request='On request',
   legend_broker='Stated by the listing broker, not independently verified', legend_calc='nad-lan computation from cited figures', legend_src='Number of the source in the list',
   comp_head_sale=['Date', 'Location', 'Rooms', 'sqm', 'Floor', 'Price', 'Per sqm', 'Type'],
   comp_head_rent=['Date', 'Location', 'Rooms', 'sqm', 'Rent / month', 'Per sqm', 'Type'],
   ),
}

ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'
ICON_CALL = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M5 4h3l1.6 4-2 1.3a11 11 0 0 0 5.1 5.1l1.3-2 4 1.6v3a2 2 0 0 1-2.2 2A16 16 0 0 1 3 6.2 2 2 0 0 1 5 4z"/></svg>'

DATE_RE = re.compile(r'(\d{4})-(\d{2})(?:-(\d{2}))?')
MONTHS_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def fdate(s, lang):
    if not s:
        return ''
    m = DATE_RE.search(str(s))
    if not m:
        return esc(s)
    y, mo, d = m.group(1), int(m.group(2)), m.group(3)
    if lang == 'he':
        return num(f"{int(d)}.{mo}.{y}" if d else f"{mo}.{y}")
    return num(f"{int(d)} {MONTHS_EN[mo-1]} {y}" if d else f"{MONTHS_EN[mo-1]} {y}")

def host(url):
    try:
        h = urllib.parse.urlparse(url).netloc
        return h.replace('www.', '')
    except Exception:
        return url


def rooms_cell(r):
    r = str(r or '').strip()
    return num(r) if re.fullmatch(r'\d+(?:\.\d)?', r) else ''

def cdate(sv, lang):
    sv = str(sv or '')
    d = fdate(sv, lang)
    low = sv.lower()
    if 'report' in low or 'not dated' in low:
        return ('דווח ' if lang == 'he' else 'Reported ') + d
    if 'access' in low or 'seen' in low or 'modif' in low:
        return ('מודעה, ' if lang == 'he' else 'Listing, ') + d
    return d

class Book:
    """Numbers sources in order of first citation for one page."""
    def __init__(self, dossier, lang, pid, titles=None):
        self.titles = titles or {}
        self.d = {s['id']: s for s in dossier.get('sources', [])}
        self.g = C['sources']
        self.lang, self.pid = lang, pid
        self.order = []
        self.keys = []
    def _key(self, i):
        s = self.d.get(i) or self.g.get(i) or {}
        u = (s.get('url') or '').strip().rstrip('/').replace('://www.', '://').lower()
        return u or i
    def fn(self, ids):
        ids = [i for i in (ids or []) if i in self.d or i in self.g]
        if not ids:
            return ''
        nums = []
        for i in ids:
            key = self._key(i)
            if key not in self.keys:
                self.keys.append(key)
                self.order.append(i)
            nums.append(self.keys.index(key) + 1)
        nums = sorted(set(nums))
        links = ','.join(f'<a href="#src-{self.pid}-{n}">{n}</a>' for n in nums[:2])
        return f'<sup class="nlx-fn">{links}</sup>'
    def items(self):
        out = []
        for n, i in enumerate(self.order, 1):
            s = self.d.get(i) or self.g.get(i)
            title = s.get('title_he') if (self.lang == 'he' and s.get('title_he')) else s.get('title')
            if i in self.titles:
                title = self.titles[i].get(self.lang) or title
            pub = str(s.get('published', '') or '')
            m = DATE_RE.search(pub)
            pubtxt = ''
            if m:
                pubtxt = (('נצפה ' if self.lang == 'he' else 'accessed ') if 'access' in pub or 'seen' in pub else '') + re.sub(r'<[^>]+>', '', fdate(pub, self.lang))
            out.append({'anchor': f'src-{self.pid}-{n}', 'title': title, 'published': pubtxt, 'url': s.get('url', ''), 'host': host(s.get('url', ''))})
        return out

def tagh(basis, lang):
    t = T[lang]
    if basis == 'broker':
        return f'<span class="nlx-tag nlx-tag--broker">{t["tag_broker"]}</span>'
    if basis in ('calc', 'computed'):
        return f'<span class="nlx-tag nlx-tag--calc">{t["tag_calc"]}</span>'
    return ''

TOK = re.compile(r'\[\[([A-Za-z0-9_,\s]+)\]\]')
def rich(text, book):
    """Escape text, then turn [[S1,S2]] tokens into footnotes."""
    if text is None:
        return ''
    parts, last = [], 0
    for m in TOK.finditer(text):
        parts.append(wrapnums(esc(text[last:m.start()])))
        parts.append(book.fn([x.strip() for x in m.group(1).split(',')]))
        last = m.end()
    parts.append(wrapnums(esc(text[last:])))
    return glue(''.join(parts))

def L_(obj, lang):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(lang)
    return obj

def meters_of(val):
    m = re.search(r'([\d.,]+)\s*(km|m)\b', val or '')
    if not m:
        return None
    v = float(m.group(1).replace(',', ''))
    return v * 1000 if m.group(2) == 'km' else v

SILHOUETTES = {
 'apartment': '<g fill="none" stroke="#1F4B5C" stroke-opacity=".55" stroke-width="2"><rect x="570" y="212" width="120" height="118"/><path d="M590 240h80M590 266h80M590 292h80"/></g>',
 'mini_penthouse': '<g fill="none" stroke="#1F4B5C" stroke-opacity=".55" stroke-width="2"><rect x="550" y="240" width="150" height="90"/><rect x="580" y="212" width="90" height="28"/><path d="M570 266h110M570 292h110"/></g>',
 'tower': '<g fill="none" stroke="#1F4B5C" stroke-opacity=".55" stroke-width="2"><rect x="540" y="212" width="48" height="118"/><rect x="604" y="226" width="48" height="104"/><rect x="668" y="242" width="48" height="88"/></g>',
 'villa': '<g fill="none" stroke="#1F4B5C" stroke-opacity=".55" stroke-width="2"><path d="M470 330V268h250v62M494 268v-40h170v40"/><path d="M500 300h60M590 300h100"/><rect x="460" y="342" width="230" height="22" rx="4" stroke-opacity=".35"/></g>',
}

def build_listing(ed, dos, lang):
    pid = f"{ed['id']}-{lang}"
    t = T[lang]
    book = Book(dos, lang, pid, ed.get('source_titles'))
    deal = ed['deal']
    price, rent = ed.get('price'), ed.get('rent')
    built, balcony = ed.get('built'), ed.get('balcony')
    L = {'lang': lang, 'dir': 'rtl' if lang == 'he' else 'ltr', 'id': ed['id'], 'deal': deal, 't': t}
    L['anchor'] = lambda k: f"{k}-{pid}"
    L['kicker'] = L_(ed['kicker'], lang)
    L['title'] = L_(ed['title'], lang)
    L['dek'] = L_(ed['dek'], lang)
    L['chips'] = [{'text': L_(c, lang), 'sea': c.get('sea', False)} for c in ed.get('chips', [])]
    L['plate'] = {'name': L_(ed['plate_name'], lang),
                  'caption': 'תמונות הנכס יתקבלו מהמשווקת. האיור אינו מתאר את הנכס.' if lang == 'he' else 'Property photography to come from the listing broker. The drawing does not depict the property.',
                  'aria': L_(ed['plate_name'], lang), 'sky': '#EEE9DD' if deal == 'sale' else '#E4EEF1', 'sea': '#CFE3EA' if deal == 'sale' else '#BFD6DE',
                  'sun_x': 600 if lang == 'he' else 200, 'silhouette': SILHOUETTES.get(ed.get('plate', ed['ptype']), SILHOUETTES['apartment'])}
    # key facts
    L['facts'] = []
    all_broker = all(f.get('basis') == 'broker' for f in ed['facts'])
    for f in ed['facts']:
        v = rich(L_(f['value'], lang), book)
        L['facts'].append({'label': L_(f['label'], lang), 'value': v, 'tag': '' if all_broker else tagh(f.get('basis'), lang)})
    L['facts_note'] = (tagh('broker', lang) + ' ' + ('כל נתוני הדירה בשורה זו נמסרו על ידי המשווקת' if lang == 'he' else 'All figures in this row were provided by the listing broker')) if all_broker else ''
    # toc
    keys = ['home', 'building', 'location'] + (['future'] if dos.get('planning_future') and ed.get('future', 'auto') != 'none' else []) + ['numbers', 'market', 'checks'] + (['faq'] if ed.get('faq') else []) + ['sources']
    L['toc'] = [{'href': f'{k}-{pid}', 'label': t['toc_items'][k]} for k in keys]
    # story
    L['story'] = {'h2': L_(ed['story_h2'], lang), 'paras': [rich(p, book) for p in ed['story'][lang]],
                  'features': [{'b': rich(b, book), 's': rich(s, book)} for b, s in ed['features'][lang]]}
    # spec
    L['spec'] = []
    for g in ed['spec']:
        gb = all(r.get('basis') == 'broker' for r in g['rows'])
        rows = [{'dt': L_(r['dt'], lang), 'dd': rich(L_(r['dd'], lang), book) + book.fn(r.get('src')), 'tag': '' if gb else tagh(r.get('basis'), lang)} for r in g['rows']]
        L['spec'].append({'title': L_(g['title'], lang), 'rows': rows, 'tag': tagh('broker', lang) if gb else ''})
    # building
    L['building'] = {'h2': L_(ed['building_h2'], lang), 'lead': rich(L_(ed.get('building_lead'), lang), book) if ed.get('building_lead') else '',
                     'rows': [{'dt': L_(r['dt'], lang), 'dd': rich(L_(r['dd'], lang), book) + book.fn(r.get('src')), 'tag': tagh(r.get('basis'), lang)} for r in ed['building']]}
    # location
    loc = {'h2': L_(ed['location_h2'], lang), 'paras': [rich(p, book) for p in ed['location'][lang]]}
    dsel = ed.get('dist', 'auto')
    dists = dos.get('distances', [])
    idx = range(len(dists)) if dsel == 'auto' else dsel
    dl = []
    for i in idx:
        d = dists[i]
        val = d.get(f'value_{lang}') or d.get('value_en')
        dl.append({'name': d.get(f'to_{lang}'), 'val_raw': val, 'basis': d.get('basis'), 'src': d.get('source_ids'), 'm': (None if i in ed.get('dist_nobar', []) else meters_of(d.get('value_en')))})
    for extra in ed.get('dist_extra', []):
        dl.append({'name': L_(extra['name'], lang), 'val_raw': L_(extra['val'], lang), 'basis': extra.get('basis'), 'src': extra.get('src'), 'm': extra.get('m')})
    mmax = max([x['m'] for x in dl if x['m']] or [0])
    def clean_val(v):
        v = re.sub(r'\s*\((?:לפי המתווכת|לפי המשווקת|broker|broker-stated|per the broker)\)', '', v or '')
        v = re.sub(r',?\s*(?:per the broker|לפי המתווכת)$', '', v)
        return v
    loc['dist'] = [{'name': x['name'], 'val': tx(clean_val(x['val_raw'])) + book.fn(x['src']) + (' ' + tagh(x['basis'], lang) if x['basis'] == 'broker' else ''),
                    'pct': (round(100 * x['m'] / mmax, 1) if (x['m'] and mmax) else None), 'note': ''} for x in dl]
    ssel = ed.get('schools', 'auto')
    sch_all = dos.get('schools', [])
    so = ed.get('schools_override', {})
    loc['schools'] = []
    for i in (range(len(sch_all)) if ssel == 'auto' else ssel):
        sx = sch_all[i]; o = so.get(str(i), {})
        loc['schools'].append({'title': L_(o.get('title'), lang) or sx.get(f'name_{lang}'), 'level': L_(o.get('level'), lang) or sx.get(f'level_{lang}'),
                               'note': (rich(L_(o['note'], lang), book) if o.get('note') else tx(sx.get(f'note_{lang}'))) + book.fn(sx.get('source_ids'))})
    for extra in ed.get('schools_extra', []):
        loc['schools'].append({'title': L_(extra['title'], lang), 'level': L_(extra['level'], lang), 'note': rich(L_(extra.get('note'), lang), book)})
    tsel = ed.get('transport', 'auto')
    tr_all = dos.get('transport', [])
    to = ed.get('transport_override', {})
    loc['transport'] = []
    for i in (range(len(tr_all)) if tsel == 'auto' else tsel):
        x = tr_all[i]; o = to.get(str(i), {})
        loc['transport'].append({'title': L_(o.get('title'), lang) or x.get(f'item_{lang}'),
                                 'status': (rich(L_(o['status'], lang), book) if o.get('status') else tx(x.get(f'status_{lang}'))) + book.fn(x.get('source_ids'))})
    for extra in ed.get('transport_extra', []):
        loc['transport'].append({'title': L_(extra['title'], lang), 'status': rich(L_(extra['status'], lang), book)})
    L['location'] = loc
    # future
    fsel = ed.get('future', 'auto')
    fo = ed.get('future_override', {})
    L['future'] = []
    fidx = list(range(len(dos.get('planning_future', [])))) if fsel == 'auto' else ([] if fsel == 'none' else fsel)
    for i in fidx:
        x = dos['planning_future'][i]; o = fo.get(str(i), {})
        L['future'].append({'title': (rich(L_(o['title'], lang), book) if o.get('title') else tx(x.get(f'item_{lang}'))) + book.fn(x.get('source_ids')),
                            'impact': rich(L_(o['impact'], lang), book) if o.get('impact') else tx(x.get(f'impact_{lang}'))})
    for extra in ed.get('future_extra', []):
        L['future'].append({'title': rich(L_(extra['title'], lang), book), 'impact': rich(L_(extra['impact'], lang), book)})
    # numbers
    L['numbers'] = build_numbers(ed, dos, lang, book)
    # market
    L['market'] = build_market(ed, dos, lang, book)
    # checks
    qsel = ed.get('questions', 'auto')
    qs = dos.get('buyer_or_renter_questions', [])
    qs = [qs[i] for i in (range(len(qs)) if qsel == 'auto' else qsel)]
    items = [tx(q[lang]) for q in qs] + [rich(x, book) for x in ed.get('checks_extra', {}).get(lang, [])]
    L['checks'] = {'h2': L_(ed['checks_h2'], lang), 'lead': L_(ed['checks_lead'], lang), 'items': items}
    L['faq'] = [{'q': L_(f['q'], lang), 'a': rich(L_(f['a'], lang), book)} for f in ed.get('faq', [])]
    # agent + cta
    wa_text = (f"שלום מיטל, אשמח לפרטים ולתיאום סיור: {L['title']} (nad-lan.co.il, {ed['id']})" if lang == 'he' else f"Hello Meital, I would like details and a private viewing: {L['title']} (nad-lan.co.il, {ed['id']})")
    wa = BROKER['wa'] + '?text=' + urllib.parse.quote(wa_text)
    L['cta'] = [
        {'href': wa, 'label': t['cta_view'], 'short': t['cta_wa_short'], 'icon': ICON_WA, 'ext': True, 'ghost': False},
        {'href': 'tel:' + BROKER['phone_intl'], 'label': f"{t['cta_call']} {BROKER['phone'] if lang == 'he' else BROKER['phone_disp_en']}", 'short': t['cta_call_short'], 'icon': ICON_CALL, 'ext': False, 'ghost': True},
    ]
    lic = f"רישיון תיווך {num(BROKER['license'])}" if lang == 'he' else f"Israeli brokerage license {num(BROKER['license'])}"
    L['agent'] = {'mono': 'מ' if lang == 'he' else 'M', 'name': f"{BROKER['name'][lang]}", 
                  'line': (f"{BROKER['brand'][lang]} · {lic} · " + (f"בלעדיות על הנכס. העמוד הוכן על ידי nad-lan.co.il בשיתוף המשווקת." if lang == 'he' else "Exclusive listing. Page prepared by nad-lan.co.il in cooperation with the broker.")),
                  'mini': f"{BROKER['brand'][lang]} · {lic}"}
    # price card
    L['price_card'] = build_price_card(ed, dos, lang, book)
    # sources, legend, disclaimer
    L['legend'] = [f'{tagh("broker", lang)} {t["legend_broker"]}', f'{tagh("calc", lang)} {t["legend_calc"]}', f'<sup class="nlx-fn">1</sup> {t["legend_src"]}']
    L['sources'] = book.items()
    posts = ed.get('posts', [])
    if lang == 'he':
        L['disclaimer'] = ('המידע בעמוד נאסף ונערך על ידי nad-lan.co.il ממודעות המשווקת ומפרסומים ציבוריים, והוא נועד להתמצאות בלבד. אין בו הצעה מחייבת, שמאות, ייעוץ משפטי, ייעוץ מס או ייעוץ השקעות. '
            'חישובי מס, מימון, ארנונה ותשואה הם המחשה לפי הכללים שפורסמו ביום העדכון ועשויים להשתנות. יש לאמת כל נתון מול המסמכים הרשמיים, עורך דין, שמאי ויועץ מס לפני קבלת החלטה. '
            f'מקור הנכס: מודעות אינסטגרם של {BROKER["name"]["he"]} (@meitalkatzir_realestate), הפרסום האחרון {fdate(ed.get("last_post"), "he")}.')
        L['updated'] = f"{t['updated']} {fdate(C['as_of'], 'he')} · {t['listing_code']} {num(ed['id'])}"
    else:
        L['disclaimer'] = ('This page was compiled by nad-lan.co.il from the listing broker\'s advertisements and public sources, for orientation only. It is not an offer, an appraisal, or legal, tax or investment advice. '
            'Tax, financing, arnona and yield figures illustrate the rules published on the update date and may change. Verify every figure against official documents and with an Israeli lawyer, appraiser and tax adviser before deciding. '
            f'Listing source: Instagram posts by {BROKER["name"]["en"]} (@meitalkatzir_realestate), latest post {fdate(ed.get("last_post"), "en")}.')
        L['updated'] = f"{t['updated']} {fdate(C['as_of'], 'en')} · {t['listing_code']} {num(ed['id'])}"
    L['jsonld'] = json.dumps(jsonld(ed, lang, L), ensure_ascii=False)
    return L

def build_price_card(ed, dos, lang, book):
    t = T[lang]
    deal, price, rent = ed['deal'], ed.get('price'), ed.get('rent')
    built, balcony = ed.get('built'), ed.get('balcony')
    pc = {'sub': [], 'rows': []}
    if deal == 'sale':
        pc['label'] = 'מחיר מבוקש' if lang == 'he' else 'Asking price'
        if price:
            pc['price'] = money(price, lang) + book.fn(ed.get('price_src'))
            f = fx(price)
            pc['sub'] = [num(f"≈ ${fint(f['usd'])}"), num(f"≈ €{fint(f['eur'])}")]
            if built:
                pc['rows'].append({'dt': 'למ״ר בנוי' if lang == 'he' else 'Per built sqm', 'dd': money(price / built, lang)})
                if balcony:
                    pc['rows'].append({'dt': 'למ״ר כולל מרפסת' if lang == 'he' else 'Per sqm incl. balcony', 'dd': money(price / (built + balcony), lang)})
        else:
            pc['price'] = esc(t['price_on_request'])
    else:
        pc['label'] = 'שכר דירה לחודש' if lang == 'he' else 'Monthly rent'
        if rent:
            pc['price'] = money(rent, lang) + book.fn(ed.get('rent_src'))
            f = fx(rent)
            pc['sub'] = [num(f"≈ ${fint(f['usd'])}"), num(f"≈ €{fint(f['eur'])}")]
            area = ed.get('rent_area') or built
            if area:
                pc['rows'].append({'dt': 'למ״ר לחודש' if lang == 'he' else 'Per sqm per month', 'dd': money(rent / area, lang)})
            pc['rows'].append({'dt': 'בשנה' if lang == 'he' else 'Per year', 'dd': money(rent * 12, lang)})
        else:
            pc['price'] = esc(t['price_on_request'])
            band = ed.get('rent_band')
            if band:
                pc['sub'] = [((L_(ed.get('rent_band_label'), lang) + ': ') if ed.get('rent_band_label') else ('טווח שוק מחושב לנכסים דומים: ' if lang == 'he' else 'Computed market band for similar units: ')) + num(f"{fint(band[0])}-{fint(band[1])}" + (' ₪' if lang == 'he' else ' NIS')) + book.fn(ed.get('rent_band_src'))]
    for r in ed.get('price_rows', []):
        pc['rows'].append({'dt': L_(r['dt'], lang), 'dd': rich(L_(r['dd'], lang), book)})
    return pc

def build_numbers(ed, dos, lang, book):
    t = T[lang]
    nb = ed['numbers']
    he = lang == 'he'
    N = {'h2': L_(nb['h2'], lang), 'lead': rich(L_(nb['lead'], lang), book), 'kpis': [], 'ledger': []}
    price, rent = ed.get('price'), ed.get('rent')
    built, balcony = ed.get('built'), ed.get('balcony')
    fxs = C['fx']
    if ed['deal'] == 'sale':
        P = price or nb.get('illustrative_price')
        if price:
            N['kpis'].append({'dt': 'מחיר מבוקש' if he else 'Asking price', 'dd': money(price, lang), 'small': num(f"≈ ${fint(price / fxs['usd'])}")})
        if price and built:
            N['kpis'].append({'dt': 'מחיר למ״ר בנוי' if he else 'Price per built sqm', 'dd': money(price / built, lang), 'small': (tagh('calc', lang))})
        if nb.get('median_psqm'):
            m = nb['median_psqm']
            N['kpis'].append({'dt': L_(m['label'], lang), 'dd': (rich(L_(m['value_text'], lang), book) if m.get('value_text') else money(m['value'], lang)) + book.fn(m.get('src')), 'small': L_(m.get('small'), lang) or ''})
        if P:
            N['kpis'].append({'dt': ('משכנתא מרבית, דירה יחידה' if he else 'Max mortgage, single home') , 'dd': money(P * C['ltv']['single'], lang) + book.fn(C['ltv'] and ['G_LTV']), 'small': ('75% מהשווי לפי בנק ישראל' if he else '75% loan-to-value, Bank of Israel')})
        for k in nb.get('extra_kpis', []):
            N['kpis'].append({'dt': L_(k['dt'], lang), 'dd': rich(L_(k['dd'], lang), book), 'small': rich(L_(k.get('small'), lang), book) if k.get('small') else ''})
        # buyer profile tabs
        if nb.get('scenarios'):
            tabs = []
            for sc in nb['scenarios']:
                SP = sc['price']
                tq = purchase_taxes(SP)
                loan = SP * C['ltv']['single']
                oleh_row = ({'dt': ('עולה חדש' if he else 'New immigrant (oleh)') + book.fn(C['oleh_src']), 'dd': ('ללא הטבה' if he else 'No relief'),
                             'note': ('מעל 20,183,565 ₪ חלות מדרגות דירה יחידה או דירה נוספת' if he else 'Above NIS 20,183,565, single-home or additional-home brackets apply')}
                            if tq['oleh_note'] == 'above_cap' else
                            {'dt': ('עולה חדש' if he else 'New immigrant (oleh)') + book.fn(C['oleh_src']), 'dd': money(tq['oleh'], lang), 'note': (('שיעור אפקטיבי ' if he else 'Effective rate ') + pct(tq['oleh'] / SP))})
                rows = [
                    {'dt': 'מחיר להמחשה' if he else 'Illustrative price', 'dd': money(SP, lang), 'note': rich(L_(sc.get('basis'), lang), book) if sc.get('basis') else ''},
                    {'dt': ('מס רכישה, דירה יחידה' if he else 'Purchase tax, single home') + book.fn(['G_TAX_DIR', 'G_KZ_TAX']), 'dd': money(tq['single'], lang), 'note': ('שיעור אפקטיבי ' if he else 'Effective rate ') + pct(tq['single'] / SP)},
                    {'dt': ('מס רכישה, דירה נוספת או תושב חוץ' if he else 'Purchase tax, additional home or foreign resident') + book.fn(['G_KZ_TAX', 'G_GLOBES_TAX']), 'dd': money(tq['additional'], lang), 'note': ('שיעור אפקטיבי ' if he else 'Effective rate ') + pct(tq['additional'] / SP)},
                    oleh_row,
                    {'dt': ('משכנתא מרבית, דירה יחידה' if he else 'Maximum mortgage, single home') + book.fn(['G_LTV']), 'dd': money(loan, lang), 'note': ('75% מהשווי; 50% לרוכש שאינו אזרח ישראלי או לדירה להשקעה' if he else '75% of value; 50% for a buyer who is not an Israeli citizen or for an investment home')},
                    {'dt': 'הון עצמי ומס רכישה, דירה יחידה' if he else 'Equity plus purchase tax, single home', 'dd': money(SP - loan + tq['single'], lang), 'note': ('לפני שכר טרחת עורך דין, תיווך ושמאות' if he else 'Before legal, brokerage and appraisal fees')},
                ]
                tabs.append({'label': L_(sc['label'], lang), 'rows': rows})
            N['seg'] = {'name': f"nlx-scen-{ed['id']}-{lang}", 'title': L_(nb.get('tabs_title'), lang) or '', 'tabs': tabs,
                        'note': ('מדרגות מס הרכישה מוקפאות עד 15.1.2028. שיעורי 8% ו-10% לדירה נוספת קבועים בהוראת שעה שתוקפה עד תחילת 2027. אין בכך ייעוץ מס.' if he else 'Purchase tax brackets are frozen until 15 January 2028. The 8% and 10% rates for additional homes are a temporary order running to early 2027. Not tax advice.') + book.fn(['G_TAX_DIR', 'G_GLOBES_TAX'])}
        elif P:
            tx = purchase_taxes(P)
            illus = (not price)
            def rows_for(kind):
                if kind == 'single':
                    tax, ltv = tx['single'], C['ltv']['single']
                elif kind == 'additional':
                    tax, ltv = tx['additional'], C['ltv']['investment']
                else:
                    tax, ltv = tx['oleh'], C['ltv']['single']
                loan = P * ltv
                eq = P - loan
                rr = [
                    {'dt': ('מס רכישה' if he else 'Purchase tax') + book.fn(C['tax_src'] if kind != 'oleh' else C['oleh_src']), 'dd': money(tax, lang), 'note': (('שיעור אפקטיבי ' if he else 'Effective rate ') + pct(tax / P))},
                    {'dt': ('הלוואה מרבית' if he else 'Maximum loan') + book.fn(['G_LTV']), 'dd': money(loan, lang), 'note': (f"{int(ltv*100)}% " + ('מהשווי' if he else 'of value'))},
                    {'dt': 'הון עצמי מינימלי' if he else 'Minimum equity', 'dd': money(eq, lang), 'note': ''},
                    {'dt': 'הון עצמי ומס רכישה' if he else 'Equity plus purchase tax', 'dd': money(eq + tax, lang), 'note': ('לפני שכר טרחת עורך דין, תיווך ושמאות' if he else 'Before legal, brokerage and appraisal fees')},
                ]
                return rr
            tabs = [
                {'label': 'דירה יחידה' if he else 'Single home, Israeli resident', 'rows': rows_for('single')},
                {'label': 'דירה נוספת או תושב חוץ' if he else 'Additional home or foreign resident', 'rows': rows_for('additional')},
                {'label': 'עולה חדש' if he else 'New immigrant (oleh)', 'rows': rows_for('oleh')},
            ]
            if tx['oleh_note'] == 'above_cap':
                tabs[2]['rows'][0]['note'] = ('מעל 20,183,565 ₪ אין הטבת עולה; חלות מדרגות דירה יחידה' if he else 'Above NIS 20,183,565 there is no oleh relief; single-home brackets apply')
            else:
                tabs[2]['rows'][0]['note'] = (('שיעור אפקטיבי ' if he else 'Effective rate ') + pct(tx['oleh'] / P) + ('. הזכאות: משנה לפני העלייה ועד 7 שנים אחריה' if he else '. Eligibility: from one year before to seven years after aliyah'))
            tabs[1]['rows'][1]['note'] = ('50% מהשווי לדירה להשקעה או לרוכש שאינו אזרח ישראלי' if he else '50% for an investment home or a buyer who is not an Israeli citizen')
            title = ('מה זה עולה לכם, לפי סוג הרוכש' if he else 'What it costs, by buyer profile')
            if illus:
                title += (f" (המחשה לפי {fint(P)} ₪)" if he else f" (illustration at NIS {fint(P)})")
            N['seg'] = {'name': f"nlx-buyer-{ed['id']}-{lang}", 'title': title, 'tabs': tabs,
                        'note': ('מדרגות מס הרכישה מוקפאות עד 15.1.2028. שיעורי 8% ו-10% לדירה נוספת קבועים בהוראת שעה שתוקפה עד תחילת 2027. אין בכך ייעוץ מס.' if he else 'Purchase tax brackets are frozen until 15 January 2028. The 8% and 10% rates for additional homes are a temporary order running to early 2027. Not tax advice.') + book.fn(['G_TAX_DIR', 'G_GLOBES_TAX'])}
        else:
            N['seg'] = {'name': f"nlx-buyer-{ed['id']}-{lang}", 'title': '', 'tabs': [], 'note': ''}
    else:
        # rentals
        R = rent
        area = ed.get('rent_area') or built
        if R:
            N['kpis'].append({'dt': 'שכר דירה לחודש' if he else 'Monthly rent', 'dd': money(R, lang), 'small': num(f"≈ ${fint(R / fxs['usd'])} · €{fint(R / fxs['eur'])}")})
            N['kpis'].append({'dt': 'שכר דירה לשנה' if he else 'Annual rent', 'dd': money(R * 12, lang), 'small': tagh('calc', lang)})
            if area:
                N['kpis'].append({'dt': 'למ״ר לחודש' if he else 'Per sqm per month', 'dd': money(R / area, lang), 'small': (('על ' if he else 'on ') + sqm(area, lang))})
        for k in nb.get('extra_kpis', []):
            N['kpis'].append({'dt': L_(k['dt'], lang), 'dd': rich(L_(k['dd'], lang), book), 'small': rich(L_(k.get('small'), lang), book) if k.get('small') else ''})
        tabs = []
        for tab in nb.get('tabs', []):
            tabs.append({'label': L_(tab['label'], lang), 'rows': [{'dt': rich(L_(r['dt'], lang), book), 'dd': rich(L_(r['dd'], lang), book), 'note': rich(L_(r.get('note'), lang), book) if r.get('note') else ''} for r in tab['rows']]})
        N['seg'] = {'name': f"nlx-lease-{ed['id']}-{lang}", 'title': L_(nb.get('tabs_title'), lang) or '', 'tabs': tabs, 'note': rich(L_(nb.get('tabs_note'), lang), book) if nb.get('tabs_note') else ''}
    # bars (one scale)
    bars = nb.get('bars')
    if bars:
        mx = max(b['value'] for b in bars['items']) or 1
        items = []
        for b in bars['items']:
            val = (money(b['value'], lang) if not b.get('value_text') else rich(L_(b['value_text'], lang), book)) + book.fn(b.get('src'))
            items.append({'label': rich(L_(b['label'], lang), book), 'value': val, 'pct': round(100 * b['value'] / mx, 1), 'this': b.get('this', False)})
        N['bars'] = {'title': L_(bars['title'], lang), 'items': items, 'note': rich(L_(bars.get('note'), lang), book) if bars.get('note') else ''}
    else:
        N['bars'] = {'title': '', 'items': [], 'note': ''}
    N['ledger_title'] = L_(nb.get('ledger_title'), lang) or ('עלויות שוטפות, תשואה ומטבע' if he else 'Running costs, yield and currency')
    for r in nb.get('ledger', []):
        N['ledger'].append({'dt': rich(L_(r['dt'], lang), book), 'dd': rich(L_(r['dd'], lang), book), 'note': rich(L_(r.get('note'), lang), book) if r.get('note') else ''})
    N['ledger'].append({'dt': ('שער דולר ויורו יציג' if he else 'Representative USD and EUR rates') + book.fn(['G_FX']), 'dd': num(f"$1 = {C['fx']['usd']:.4f} ₪ · €1 = {C['fx']['eur']:.4f} ₪") if he else num(f"USD 1 = NIS {C['fx']['usd']:.4f} · EUR 1 = NIS {C['fx']['eur']:.4f}"), 'note': ('בנק ישראל, 15.9.2026' if he else 'Bank of Israel, 15 Sep 2026')})
    N['ledger'].append({'dt': ('ריבית בנק ישראל ופריים' if he else 'Bank of Israel rate and prime') + book.fn(['G_BOI_RATE']), 'dd': num(f"{C['boi']['rate']}% · {C['boi']['prime']}%"), 'note': ('החלטה מ-1.9.2026' if he else 'Decision of 1 Sep 2026')})
    _plain = lambda h: re.sub(r'<sup.*?</sup>', '', h or '')
    _len = max([len(html.unescape(re.sub(r'<[^>]+>', '', _plain(k['dd'])))) for k in N['kpis']] or [0])
    N['kpi_cols'] = 2 if (len(N['kpis']) == 4 and _len > 10) else 0
    N['foot'] = rich(L_(nb.get('foot'), lang), book) if nb.get('foot') else (('כל המספרים בפרק זה הם המחשה מחושבת ואינם הצעת מחיר, שמאות או ייעוץ.' if he else 'All figures in this section are computed illustrations, not a quote, an appraisal or advice.'))
    return N

def build_market(ed, dos, lang, book):
    t = T[lang]
    mk = ed['market']
    he = lang == 'he'
    M = {'h2': L_(mk['h2'], lang), 'lead': rich(L_(mk['lead'], lang), book), 'stats': [], 'tables': []}
    st = dos.get('market_stats', [])
    ssel = mk.get('stats', 'auto')
    st = [st[i] for i in (range(len(st)) if ssel == 'auto' else ssel)]
    stidx = list(range(len(dos.get('market_stats', [])))) if ssel == 'auto' else ssel
    sov = mk.get('stats_override', {})
    for k_i, s in zip(stidx, st):
        o = sov.get(str(k_i), {})
        dt_txt = L_(o.get('dt'), lang) or s.get(f'metric_{lang}')
        dd_html = rich(L_(o['dd'], lang), book) if o.get('dd') else tx(s.get(f'value_{lang}'))
        M['stats'].append({'dt': tx(dt_txt) + (f" <span class=\"nlx-muted\">({fdate(s.get('as_of'), lang)})</span>" if s.get('as_of') else ''), 'dd': dd_html + book.fn(s.get('source_ids'))})
    def kind_tag(k):
        if k == 'transaction':
            return f'<span class="nlx-tag nlx-tag--tx">{t["tag_tx"]}</span>'
        if k == 'reported':
            return f'<span class="nlx-tag">{t["tag_rep"]}</span>'
        return f'<span class="nlx-tag">{t["tag_ask"]}</span>'
    ov = mk.get('where_override', {})
    sc = dos.get('sale_comps', [])
    ssel = mk.get('sale', 'auto')
    sidx = [i for i in (range(len(sc)) if ssel == 'auto' else ssel) if i not in mk.get('sale_exclude', [])]
    if sidx:
        rows = []
        for i in sorted(sidx, key=lambda i: (0 if sc[i].get('kind') == 'transaction' else 1, str(sc[i].get('date'))), reverse=False):
            c = sc[i]
            where = L_(ov.get(f'sale:{i}'), lang) or c.get(f'where_{lang}')
            dov = mk.get('date_override', {}).get(f'sale:{i}')
            rows.append([
                {'v': esc(L_(dov, lang)) if dov else cdate(c.get('date'), lang)}, {'v': tx(where) + book.fn(c.get('source_ids'))}, {'v': rooms_cell(c.get('rooms')), 'r': True},
                {'v': num(f"{c['sqm']:g}") if isinstance(c.get('sqm'), (int, float)) else '', 'r': True}, {'v': num(str(c['floor'])) if isinstance(c.get('floor'), (int, float)) else '', 'r': True},
                {'v': money(c['price_nis'], lang) if c.get('price_nis') else '', 'r': True}, {'v': money(c['price_per_sqm_nis'], lang) if c.get('price_per_sqm_nis') else '', 'r': True},
                {'v': kind_tag(c.get('kind'))}])
        M['tables'].append({'title': L_(mk.get('sale_title'), lang) or ('עסקאות ומודעות מכירה להשוואה' if he else 'Sales and asking prices for comparison'), 'head': t['comp_head_sale'], 'rows': rows,
                            'caption': ('עסקאות מוצגות לפני מודעות. מחיר למ״ר מחושב על השטח שפורסם. יש לאמת עסקאות באתר נדל״ן של רשות המסים. אין זו שמאות.' if he else 'Recorded sales are listed before asking prices. Price per sqm is computed on the published area. Verify sales on the Tax Authority real estate site. This is not an appraisal.')})
    rc = dos.get('rent_comps', [])
    rsel = mk.get('rent', 'auto')
    ridx = [i for i in (range(len(rc)) if rsel == 'auto' else rsel) if i not in mk.get('rent_exclude', [])]
    if ridx:
        rows = []
        for i in ridx:
            c = rc[i]
            where = L_(ov.get(f'rent:{i}'), lang) or c.get(f'where_{lang}')
            dov = mk.get('date_override', {}).get(f'rent:{i}')
            rows.append([
                {'v': esc(L_(dov, lang)) if dov else cdate(c.get('date'), lang)}, {'v': tx(where) + book.fn(c.get('source_ids'))}, {'v': rooms_cell(c.get('rooms')), 'r': True},
                {'v': num(f"{c['sqm']:g}") if isinstance(c.get('sqm'), (int, float)) else '', 'r': True}, {'v': money(c['rent_nis'], lang) if c.get('rent_nis') else '', 'r': True},
                {'v': money(c['rent_per_sqm_nis'], lang) if c.get('rent_per_sqm_nis') else '', 'r': True}, {'v': kind_tag(c.get('kind'))}])
        M['tables'].append({'title': L_(mk.get('rent_title'), lang) or ('שכירות להשוואה' if he else 'Rents for comparison'), 'head': t['comp_head_rent'], 'rows': rows,
                            'caption': ('מחירי שכירות מבוקשים ממודעות, לא חוזים חתומים. שכר דירה למ״ר מחושב על השטח שפורסם.' if he else 'Asking rents from listings, not signed leases. Rent per sqm is computed on the published area.')})
    return M

def jsonld(ed, lang, L):
    he = lang == 'he'
    city = L_(ed['city'], lang)
    area = L_(ed['area'], lang)
    ptype = {'apartment': 'Apartment', 'mini_penthouse': 'Apartment', 'villa': 'SingleFamilyResidence'}.get(ed['ptype'], 'Accommodation')
    item = {'@type': ptype, 'name': L['title'],
            'address': {'@type': 'PostalAddress', 'addressLocality': city, 'addressRegion': area, 'addressCountry': 'IL'}}
    if ed.get('rooms'):
        item['numberOfRooms'] = ed['rooms']
    if ed.get('built'):
        item['floorSize'] = {'@type': 'QuantitativeValue', 'value': ed['built'], 'unitCode': 'MTK'}
    amen = [L_(a, lang) for a in ed.get('amenities', [])]
    if amen:
        item['amenityFeature'] = [{'@type': 'LocationFeatureSpecification', 'name': a, 'value': True} for a in amen]
    offer = {'@type': 'Offer', 'priceCurrency': 'ILS', 'availability': 'https://schema.org/InStock',
             'businessFunction': 'http://purl.org/goodrelations/v1#Sell' if ed['deal'] == 'sale' else 'http://purl.org/goodrelations/v1#LeaseOut',
             'offeredBy': {'@type': 'RealEstateAgent', 'name': f"{BROKER['name'][lang]}, {BROKER['brand'][lang]}", 'telephone': BROKER['phone_intl']}}
    if ed['deal'] == 'sale' and ed.get('price'):
        offer['price'] = ed['price']
    if ed['deal'] == 'rent' and ed.get('rent'):
        offer['priceSpecification'] = {'@type': 'UnitPriceSpecification', 'price': ed['rent'], 'priceCurrency': 'ILS', 'unitCode': 'MON'}
    seo = ed['seo'][lang]
    doc = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'RealEstateListing', 'name': L['title'], 'description': seo['desc'], 'inLanguage': 'he-IL' if he else 'en',
         'datePosted': C['as_of'], 'url': URL_PATTERN[lang].format(slug=seo['slug']), 'about': item, 'offers': offer},
    ]}
    if ed.get('faq'):
        doc['@graph'].append({'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': L_(f['q'], lang), 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'\[\[[^\]]+\]\]', '', L_(f['a'], lang))}} for f in ed['faq']]})
    return doc

def _remap(obj, tmap):
    if isinstance(obj, str):
        def rep(m):
            ids = [x.strip() for x in m.group(1).split(',')]
            return '[[' + ','.join(tmap.get(i, i) for i in ids) + ']]'
        return TOK.sub(rep, obj)
    if isinstance(obj, list):
        return [(_remap(x, tmap) if not (isinstance(x, str) and re.fullmatch(r'S\d+', x)) else tmap.get(x, x)) for x in obj]
    if isinstance(obj, dict):
        return {k: _remap(v, tmap) for k, v in obj.items()}
    return obj

def load_ed(lid):
    ed = json.load(open(B + f'editorial/{lid}.json'))
    if ed.get('extends'):
        base = load_ed(ed['extends'])
        tmap = ed.get('token_map', {})
        for k in ed.get('inherit', []):
            if k not in ed and k in base:
                ed[k] = _remap(base[k], tmap) if tmap else base[k]
    return ed

def render_all(ids):
    tpl = env.get_template('listing.html.j2')
    os.makedirs(OUT, exist_ok=True)
    built = {}
    for lid in ids:
        ed = load_ed(lid)
        dos = json.load(open(BASE + f'dossiers/{lid}.json'))
        for lang in ('he', 'en'):
            L = build_listing(ed, dos, lang)
            htmlout = tpl.render(L=L)
            assert_no_dash(htmlout, f'{lid}-{lang}')
            built[(lid, lang)] = (htmlout, L, ed)
    return built

if __name__ == '__main__':
    ids = sys.argv[1:] or sorted(f[:-5] for f in os.listdir(B + 'editorial') if f.endswith('.json'))
    res = render_all(ids)
    for (lid, lang), (h, L, ed) in res.items():
        d = OUT + f'blocks/{lid}'
        os.makedirs(d, exist_ok=True)
        open(d + f'/{lang}.html', 'w').write(h)
        print(lid, lang, len(h), 'bytes', len(L['sources']), 'sources')
