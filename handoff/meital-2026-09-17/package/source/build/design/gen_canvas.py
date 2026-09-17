#!/usr/bin/env python3
"""Generates the Claude Design canvas (Design artifact type) for Meital Katzir's broker profile on nad-lan.
Writes project/*.dc.html and project/canvas.json under canvas/ (the publish root)."""
import json, os, sys, html, re, io, urllib.parse, datetime
import segno
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE)) + '/'
sys.path.insert(0, HERE)
from scenes import plate, estate_night, hero_scene, card_scene

CARDS = json.load(open(BASE + 'build/broker/cards.json'))
ORDER = ['L01', 'L07', 'L08', 'L05', 'L04', 'L06', 'L02', 'L03', 'L09', 'L10', 'L11']
IMAGES = json.load(open(HERE + '/assets.json')) if os.path.exists(HERE + '/assets.json') else {}
HEIGHTS = json.load(open(HERE + '/heights.json')) if os.path.exists(HERE + '/heights.json') else {}
OUT = BASE + 'canvas/project/'

# ---- tokens (nad-lan Skin A) ----
PAPER, SURF, INK, INK2, MUTE, LINE = '#F7F6F2', '#FFFFFF', '#14212B', '#3B4753', '#5F6B75', '#E3E1DA'
SEA, SEA_H, DEEP, ABYSS, SAND, MIST, FOAM = '#2F6F86', '#255C70', '#1F4B5C', '#10262F', '#EEE9DD', '#CFE3EA', '#E8F1F3'
SANS = "'Assistant', 'Segoe UI', 'Arial Hebrew', sans-serif"
SERIF_HE = "'Noto Serif Hebrew', 'Frank Ruhl Libre', 'Times New Roman', serif"
SERIF_EN = "'Noto Serif Display', 'Noto Serif', Georgia, serif"
NUM = 'font-variant-numeric: tabular-nums lining-nums;'
FONTS = 'https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;500;600;700;800&amp;family=Noto+Serif+Hebrew:wght@300;400;500;600&amp;family=Noto+Serif+Display:ital,wght@0,300;0,400;0,500;1,300;1,400&amp;display=swap'

WA_NUM = '972523631582'
PHONE = {'he': '052-3631582', 'en': '+972 52-363-1582'}
HANDLE = '@meitalkatzir_realestate'
IG_URL = 'https://www.instagram.com/meitalkatzir_realestate/'

ICONS = {
 'rooms': '<path d="M3.5 20V9.5L12 4l8.5 5.5V20M9.5 20v-5.5h5V20"/>',
 'area': '<rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M4 9h3M4 14h3M9 4v3M14 4v3"/>',
 'plot': '<rect x="4" y="4" width="16" height="16" rx="1.5" stroke-dasharray="3 2.4"/><path d="M8.5 15.5l3.5-6 3.5 6z"/>',
 'levels': '<path d="M4 7.5h16M4 12h16M4 16.5h16"/>',
 'balcony': '<path d="M7 11V5h10v6M4 11h16M6 11v8M10 11v8M14 11v8M18 11v8M4 19h16"/>',
 'floor': '<path d="M4 20h4v-4h4v-4h4V8h4"/>',
 'exposure': '<circle cx="12" cy="12" r="8"/><path d="M12 6.5l2.2 5.5L12 17.5 9.8 12z"/>',
 'parking': '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M10 16.5v-9h3.2a2.7 2.7 0 010 5.4H10"/>',
 'storage': '<path d="M4 8.2L12 4l8 4.2v7.6L12 20l-8-4.2z"/><path d="M4 8.2l8 4.2 8-4.2M12 12.4V20"/>',
 'mamad': '<path d="M12 3.5l7 2.8v5.1c0 4.6-2.9 7.6-7 9.1-4.1-1.5-7-4.5-7-9.1V6.3z"/>',
 'elevator': '<rect x="5.5" y="3.5" width="13" height="17" rx="1.5"/><path d="M9.5 9.5l2.5-2.5 2.5 2.5M9.5 14.5l2.5 2.5 2.5-2.5"/>',
 'pool': '<path d="M3 16c2 0 2.2-1.6 4.5-1.6S10 16 12 16s2.3-1.6 4.5-1.6S19 16 21 16M3 20c2 0 2.2-1.6 4.5-1.6S10 20 12 20s2.3-1.6 4.5-1.6S19 20 21 20M8.5 13V6.5a2 2 0 014 0M14.5 13V6.5a2 2 0 014 0M8.5 9.5h6"/>',
 'gym': '<path d="M7 7.5v9M17 7.5v9M4 10v4M20 10v4M7 12h10"/>',
 'guard': '<circle cx="12" cy="8.2" r="3.2"/><path d="M5.5 20c.9-3.7 3.5-5.6 6.5-5.6s5.6 1.9 6.5 5.6"/>',
 'sea': '<path d="M3 11c2.4 0 2.6-2 5-2s2.6 2 5 2 2.6-2 5-2 2.4 2 3 2M3 16c2.4 0 2.6-2 5-2s2.6 2 5 2 2.6-2 5-2 2.4 2 3 2"/>',
 'cinema': '<rect x="3.5" y="6" width="17" height="12" rx="2"/><path d="M10.2 9.4v5.2l4.3-2.6z"/>',
 'phone': '<path d="M5 4h3l1.6 4-2 1.3a11 11 0 005.1 5.1l1.3-2 4 1.6v3a2 2 0 01-2.2 2A16 16 0 013 6.2 2 2 0 015 4z"/>',
 'ig': '<rect x="4" y="4" width="16" height="16" rx="4.5"/><circle cx="12" cy="12" r="3.6"/><circle cx="16.8" cy="7.2" r=".6" fill="currentColor" stroke="none"/>',
 'key': '<circle cx="8" cy="12" r="3.6"/><path d="M11.6 12H20.5M17.5 12v3M20.5 12v2.4"/>',
 'arrow_he': '<path d="M19 12H5M11 6l-6 6 6 6"/>',
 'arrow_en': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
 'pin': '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0113 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
}
ICONS['parking2'] = ICONS['parking']
WA_PATH = '<path fill="currentColor" stroke="none" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/>'

def ico(name, size=18, color='currentColor', sw=1.6):
    body = WA_PATH if name == 'wa' else ICONS[name]
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" aria-hidden="true" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" style="display: block; flex-shrink: 0; color: {color};">{body}</svg>')

AMEN = {'parking': ('חניה', 'Parking'), 'parking2': ('2 חניות', '2 parking'), 'storage': ('מחסן', 'Storage'), 'mamad': ('ממ״ד', 'Safe room'),
        'elevator': ('מעלית', 'Lift'), 'pool': ('בריכה', 'Pool'), 'gym': ('חדר כושר', 'Gym'), 'guard': ('שמירה', 'Security'),
        'sea': ('נוף לים', 'Sea view'), 'cinema': ('קולנוע', 'Cinema')}
KIND = {'L01': 'estate', 'L07': 'penthouse', 'L08': 'twin', 'L05': 'boutique', 'L04': 'boutique', 'L06': 'penthouse',
        'L02': 'twin', 'L03': 'twin', 'L09': 'lowrise', 'L10': 'lowrise', 'L11': 'complex'}

def e(s):
    return html.escape(s, quote=True)

def iso(s):
    return f'<span dir="ltr" style="unicode-bidi: isolate;">{s}</span>'

def fint(n):
    return f'{int(round(n)):,}'

def fdate(s, lang):
    y, m, d = s.split('-')
    if lang == 'he':
        return f'{int(d)}.{int(m)}.{y}'
    return f"{int(d)} {['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m)-1]} {y}"

def qr(data, size, dark=INK):
    q = segno.make(data, error='m')
    buf = io.BytesIO()
    q.save(buf, kind='svg', scale=1, border=0, dark=dark, light=None, xmldecl=False, svgns=True, nl=False, omitsize=True)
    s = buf.getvalue().decode()
    s = re.sub(r'<svg ', f'<svg width="{size}" height="{size}" role="img" aria-label="QR" style="display: block;" shape-rendering="crispEdges" ', s, count=1)
    s = s.replace(' class="segno"', '').replace('<path class="qrline"', '<path')
    return s

def wa_link():
    return '#'

T = {
 'he': dict(
    dir='rtl', start='right', end='left', serif=SERIF_HE,
    eyebrow='נכסים בבלעדיות · nad-lan', name='מיטל קציר', brand='נדל״ן על הים',
    lede='נכסי יוקרה בבלעדיות בקו החוף הצפוני של תל אביב, בשרונה ובהרצליה פיתוח: דירות, מיני פנטהאוזים ואחוזה פרטית.',
    wa='וואטסאפ למיטל', ig='אינסטגרם', nav_all='כל הנכסים', nav_lang='English',
    meta=[('רישיון תיווך', '3131540'), ('נכסים בבלעדיות', '11'), ('נתונים נכונים ל', '16.9.2026')],
    coords='32.18°N 34.81°E · 32.07°N 34.79°E',
    f_eyebrow='הנכס המוביל · הרצליה פיתוח', f_title='האחוזה הפרטית',
    f_lead='כ-700 מ״ר בנויים בשלושה מפלסים על מגרש של כ-1,100 מ״ר, במרחק הליכה מהים וכחמש דקות מכיכר דה שליט, .',
    f_stats=[('700', 'מ״ר בנוי'), ('1,100', 'מ״ר מגרש'), ('7', 'סוויטות'), ('3', 'מפלסים')],
    f_amen='בריכה גדולה, חדר קולנוע, חדר כושר, מרתף יין, מעלית, ממ״ד גדול, חשמל חכם וחימום תת-רצפתי.',
    f_price='מחיר לפי פנייה', f_price_sub='סיורים בתיאום מראש בלבד', f_cta='לתיאום סיור פרטי', f_cta2='לעמוד הנכס המלא', illus='איור',
    n_eyebrow='11 נכסים · 6 שכונות', n_title='המחירים, נכס אחרי נכס',
    n_lead='חמישה נכסים למכירה ושישה להשכרה, מהרצליה פיתוח ועד שרונה. נכס בלי מחיר מפורסם מסומן כמחיר לפי פנייה.',
    sale='למכירה', rent='להשכרה', n_sale_unit='מיליון ₪', n_rent_unit='₪ לחודש', listings_word='נכסים',
    n_on_request='מחיר לפי פנייה', map_caption='מפה סכמטית, לא בקנה מידה. המספר על כל נקודה הוא מספר הנכסים בשכונה.',
    map_sea='הים התיכון', map_north='צפון',
    l_eyebrow='הנכסים', l_title='כל הנכסים בבלעדיות', l_lead='לכל נכס עמוד מלא ב-nad-lan עם מקורות, עלויות, מס רכישה או חוק השכירות, והשוואות שוק.',
    all='הכול', review='זמינות בבדיקה', on_request_sale='מחיר לפי פנייה', on_request_rent='שכר דירה לפי פנייה', on_request_sub='הפרטים נמסרים בפנייה ישירה',
    month='לחודש', per_sqm_sale='למ״ר', per_sqm_rent='למ״ר לחודש', updated='עודכן', c_wa='וואטסאפ', c_page='לעמוד הנכס',
    ig_eyebrow='באינסטגרם', ig_lead='תמונות וסרטונים מכל הנכסים, ישירות מהחשבון של מיטל.', ig_scan='סריקה לאינסטגרם', ig_cta='לעמוד האינסטגרם',
    b_eyebrow='כרטיס ביקור דיגיטלי', b_title='לשמור, לשתף, לסרוק',
    b_lead='צד אחד עם השם והרישיון, צד שני עם טלפון, וואטסאפ, אינסטגרם וקוד QR שפותח שיחה בוואטסאפ.',
    role='מתווכת מורשית · רישיון', direct_wa='וואטסאפ ישיר', areas_line='צפון תל אביב, שרונה, הרצליה פיתוח', scan_wa='סריקה לוואטסאפ',
    k_eyebrow='יצירת קשר', k_title='לתיאום סיור פרטי', k_lead='מיטל קציר, נדל״ן על הים. מתווכת מורשית, רישיון 3131540.', k_call='חיוג',
    method=[('כל מספר עם מקור', 'נתוני הנכס מסומנים כנתוני מיטל קציר, והנתונים מסביב מקושרים למקור ציבורי.'),
            ('העלות האמיתית', 'מס רכישה לפי סוג רוכש, מימון, ארנונה, ועד בית, ובשכירות גם חוק השכירות ההוגנת.'),
            ('השוק והסביבה', 'עסקאות ומודעות להשוואה, בתי ספר, תחבורה ותכניות בנייה סביב הנכס.')],
    legal='העמוד הוכן על ידי nad-lan.co.il בשיתוף מיטל קציר. המידע נאסף ממודעות מיטל קציר ומפרסומים ציבוריים ונכון ל-16.9.2026. אין בו הצעה מחייבת, שמאות או ייעוץ. תמונות: מיטל קציר, נדל״ן על הים.',
    more='הצגת 8 נכסים נוספים', areas=[('הרצליה פיתוח', 1, 32.176, 34.808), ('צוקי אביב', 4, 32.124, 34.801), ('נופי ים', 2, 32.113, 34.796),
                                        ('רמת אביב', 1, 32.114, 34.809), ('כוכב הצפון', 1, 32.099, 34.786), ('שרונה', 2, 32.071, 34.788)],
    share_kicker='nad-lan · נכסים בבלעדיות', share_stats=[('11', 'נכסים בבלעדיות'), ('6', 'שכונות על קו החוף')], share_url='nad-lan.co.il/brokers/meital-katzir',
    share_line='מהרצליה פיתוח ועד שרונה',
 ),
 'en': dict(
    dir='ltr', start='left', end='right', serif=SERIF_EN,
    eyebrow='Broker profile · nad-lan', name='Meital Katzir', brand='Real Estate by the Sea',
    lede='Exclusive luxury listings along north Tel Aviv’s coast, in Sarona and in Herzliya Pituach: apartments, mini penthouses and a private estate.',
    wa='WhatsApp Meital', ig='Instagram', nav_all='All properties', nav_lang='עברית',
    meta=[('Brokerage license', '3131540'), ('Exclusive listings', '11'), ('Data as of', '16 Sep 2026')],
    coords='32.18°N 34.81°E · 32.07°N 34.79°E',
    f_eyebrow='Signature listing · Herzliya Pituach', f_title='The Private Estate',
    f_lead='About 700 sqm built over three levels on a plot of about 1,100 sqm, within walking distance of the sea and about five minutes from De Shalit Square, according to the broker.',
    f_stats=[('700', 'sqm built'), ('1,100', 'sqm plot'), ('7', 'suites'), ('3', 'levels')],
    f_amen='A large pool, cinema room, gym, wine cellar, lift, large safe room, smart electrics and underfloor heating.',
    f_price='Price on request', f_price_sub='Viewings by appointment only', f_cta='Arrange a private viewing', f_cta2='Full listing page', illus='Illustration',
    n_eyebrow='11 listings · 6 neighborhoods', n_title='Every price, listing by listing',
    n_lead='Five for sale and six for rent, from Herzliya Pituach to Sarona. A listing without a published price is marked price on request.',
    sale='For sale', rent='For rent', n_sale_unit='NIS million', n_rent_unit='NIS a month', listings_word='listings',
    n_on_request='Price on request', map_caption='Schematic map, not to scale. The number on each point is the neighborhood’s listing count.',
    map_sea='Mediterranean Sea', map_north='North',
    l_eyebrow='The listings', l_title='Every exclusive listing', l_lead='Each listing has a full nad-lan page with sources, costs, purchase tax or rental law, and market comparisons.',
    all='All', review='Availability being confirmed', on_request_sale='Price on request', on_request_rent='Rent on request', on_request_sub='Details given on direct enquiry',
    month='a month', per_sqm_sale='per sqm', per_sqm_rent='per sqm a month', updated='Updated', c_wa='WhatsApp', c_page='Listing page',
    ig_eyebrow='On Instagram', ig_lead='Photos and videos from every listing, straight from Meital’s account.', ig_scan='Scan for Instagram', ig_cta='Open Instagram',
    b_eyebrow='Digital business card', b_title='Save it, share it, scan it',
    b_lead='One side with the name and license, the other with phone, WhatsApp, Instagram and a QR code that opens a WhatsApp chat.',
    role='Licensed broker · License', direct_wa='Direct WhatsApp', areas_line='North Tel Aviv, Sarona, Herzliya Pituach', scan_wa='Scan for WhatsApp',
    k_eyebrow='Contact', k_title='Arrange a private viewing', k_lead='Meital Katzir, Real Estate by the Sea. Licensed broker, license 3131540.', k_call='Call',
    method=[('Every figure sourced', 'Listing facts are marked as broker-stated, and everything around them links to a public source.'),
            ('The real cost', 'Purchase tax by buyer type, financing, arnona and building fees, and for rentals the Fair Rental Law.'),
            ('Market and setting', 'Sales and listings for comparison, schools, transport and planned construction around the home.')],
    legal='Page prepared by nad-lan.co.il in cooperation with the broker. Information from the broker’s listings and public sources, as of 16 Sep 2026. Not an offer, appraisal or advice. Photos: Meital Katzir, Real Estate by the Sea.',
    more='Show 8 more listings', areas=[('Herzliya Pituach', 1, 32.176, 34.808), ('Tzukei Aviv', 4, 32.124, 34.801), ('Nofei Yam', 2, 32.113, 34.796),
                                         ('Ramat Aviv', 1, 32.114, 34.809), ('Kochav HaTzafon', 1, 32.099, 34.786), ('Sarona', 2, 32.071, 34.788)],
    share_kicker='nad-lan · Broker profile', share_stats=[('11', 'exclusive listings'), ('6', 'coastal neighborhoods')], share_url='nad-lan.co.il/brokers/meital-katzir',
    share_line='From Herzliya Pituach to Sarona',
 ),
}

def eyebrow(text, lang, color=SEA, size=14, line=True, line_color=None):
    ls = '0.14em' if lang == 'en' else '0.03em'
    tt = 'text-transform: uppercase; ' if lang == 'en' else ''
    ln = f'<span style="display: block; width: 40px; height: 1px; background: {line_color or color}; flex-shrink: 0;"></span>' if line else ''
    return (f'<p style="margin: 0; display: flex; align-items: center; gap: 14px; font-family: {SANS}; font-size: {size}px; font-weight: 700; '
            f'letter-spacing: {ls}; {tt}color: {color};">{ln}<span>{e(text)}</span></p>')

def btn(label, kind='sea', icon=None, lang='he', h=52, size=16, full=False, pad=26, aria=None, href='#'):
    styles = {
        'sea': f'background: {SEA}; color: #FFFFFF; border: 1px solid {SEA};',
        'paper': f'background: {PAPER}; color: {ABYSS}; border: 1px solid {PAPER};',
        'abyss': f'background: {ABYSS}; color: {PAPER}; border: 1px solid {ABYSS};',
        'ghost': f'background: transparent; color: {PAPER}; border: 1px solid rgba(247, 246, 242, 0.42);',
        'line': f'background: transparent; color: {INK}; border: 1px solid {INK};',
        'white': f'background: #FFFFFF; color: {INK}; border: 1px solid {LINE};',
    }[kind]
    w = 'width: 100%; ' if full else ''
    ic = ''
    if icon:
        ic_color = SEA if (kind == 'paper' and icon == 'wa') else 'currentColor'
        ic = ico(icon, 19 if h >= 48 else 17, ic_color)
    a = f' aria-label="{e(aria)}"' if aria else ''
    return (f'<a href="{href}"{a} style="{w}box-sizing: border-box; display: inline-flex; align-items: center; justify-content: center; gap: 10px; height: {h}px; '
            f'padding-inline: {pad}px; border-radius: 999px; {styles} font-family: {SANS}; font-size: {size}px; font-weight: 700; text-decoration: none; white-space: nowrap;">'
            f'{ic}<span>{label}</span></a>')

# ---------------------------------------------------------------- listing card
def TL(lang, lid):
    return HEIGHTS.get('title_lines', {}).get(lang, {}).get(lid, 2)

def row_lines(lang, seq, lid):
    k = seq.index(lid)
    row = seq[k - k % 3: k - k % 3 + 3]
    return max(TL(lang, j) for j in row)

def price_block(c, lang, t):
    he = lang == 'he'
    if c['price']:
        if he:
            big = f'<span style="{NUM}">{fint(c["price"])}</span>&nbsp;₪'
        else:
            big = f'NIS&nbsp;<span style="{NUM}">{fint(c["price"])}</span>'
        small = f'<span style="font-size: 15px; font-weight: 600; color: {MUTE};">{t["month"]}</span>' if c['deal'] == 'rent' else ''
        per = ''
        if c.get('per_sqm'):
            unit = t['per_sqm_sale'] if c['deal'] == 'sale' else t['per_sqm_rent']
            per = (f'<span style="{NUM}">{fint(c["per_sqm"])}</span>&nbsp;₪ {unit}' if he else f'NIS&nbsp;<span style="{NUM}">{fint(c["per_sqm"])}</span> {unit}')
        return (f'<div style="height: 58px; display: flex; flex-direction: column; justify-content: center; gap: 4px;">'
                f'<p style="margin: 0; display: flex; align-items: baseline; gap: 8px; font-family: {SANS}; font-size: 27px; line-height: 1.15; font-weight: 800; color: {INK};"><span>{big}</span>{small}</p>'
                f'<p style="margin: 0; font-family: {SANS}; font-size: 14px; line-height: 1.3; color: {MUTE};">{per}</p></div>')
    label = t['on_request_sale'] if c['deal'] == 'sale' else t['on_request_rent']
    return (f'<div style="height: 58px; display: flex; flex-direction: column; justify-content: center; gap: 4px;">'
            f'<p style="margin: 0; font-family: {SANS}; font-size: 23px; line-height: 1.2; font-weight: 800; color: {INK};">{label}</p>'
            f'<p style="margin: 0; font-family: {SANS}; font-size: 14px; line-height: 1.3; color: {MUTE};">{t["on_request_sub"]}</p></div>')

def media_img(key, fallback_svg, alt):
    src = IMAGES.get(key)
    if src:
        return f'<img src="{src}" alt="{e(alt)}" style="display: block; width: 100%; height: 100%; object-fit: cover;">'
    return fallback_svg

def badge(text, kind):
    st = {'sale': f'background: {ABYSS}; color: {PAPER};', 'rent': f'background: {PAPER}; color: {ABYSS};',
          'review': f'background: {SAND}; color: {INK};', 'note': f'background: {MIST}; color: {ABYSS};'}[kind]
    return (f'<span style="display: inline-flex; align-items: center; height: 28px; padding-inline: 12px; border-radius: 999px; {st} '
            f'font-family: {SANS}; font-size: 13px; font-weight: 700; white-space: nowrap;">{e(text)}</span>')

def card(lid, lang, media_h=224, pad=22, mobile=False, title_lines=2, href='#', wa_href='#'):
    t = T[lang]
    c = CARDS[lid]
    he = lang == 'he'
    mode = 'dusk' if c['deal'] == 'sale' else 'day'
    deal_label = t['sale'] if c['deal'] == 'sale' else t['rent']
    badges = [badge(deal_label, c['deal'])]
    if c.get('price_note'):
        badges.append(badge(c['price_note'][lang], 'note'))
    if c['review']:
        badges.append(badge(t['review'], 'review'))
    code_side = t['end']
    m_tag = 'a' if href != '#' else 'div'
    m_attr = (' href="' + href + '" tabindex="-1" aria-hidden="true"') if href != '#' else ''
    media = (f'<{m_tag}{m_attr} style="display: block; position: relative; height: {media_h}px; background: {ABYSS}; overflow: hidden;">'
             f'{media_img(lid, plate(KIND[lid], mode, seed=lid), c["title"][lang])}'
             f'<div style="position: absolute; top: 14px; {t["start"]}: 14px; {t["end"]}: 64px; display: flex; flex-wrap: wrap; gap: 6px;">{"".join(badges)}</div>'
             f'<span style="position: absolute; bottom: 12px; {code_side}: 12px; display: inline-flex; align-items: center; height: 24px; padding-inline: 9px; border-radius: 6px; '
             f'background: rgba(16, 38, 47, 0.62); color: {PAPER}; font-family: {SANS}; font-size: 12px; font-weight: 700; letter-spacing: 0.06em; {NUM}">{lid}</span></{m_tag}>')
    kicker = f'{c["ptype"][lang]} · {c["area"][lang]}'
    title_html = e(c['title'][lang]) if href == '#' else ('<a href="' + href + '" style="color: ' + INK + '; text-decoration: none;">' + e(c['title'][lang]) + '</a>')
    title_size = 22 if he else 21
    specs = ''.join(
        f'<li style="display: flex; align-items: center; gap: 8px; min-width: 0; font-family: {SANS}; font-size: {15 if he else 14}px; line-height: 1.3; font-weight: 600; color: {INK};">'
        f'{ico(k, 18, SEA)}<span style="{NUM}">{e(v[lang])}</span></li>' for k, v in c['specs'])
    his = ''.join(
        f'<li style="display: flex; align-items: flex-start; gap: 10px; font-family: {SANS}; font-size: {14.5 if he else 14}px; line-height: 1.45; color: {INK2};">'
        f'<span style="display: block; width: 5px; height: 5px; margin-top: {8 if he else 8}px; border-radius: 50%; background: {SEA}; flex-shrink: 0;"></span><span style="{NUM}">{e(x)}</span></li>' for x in c['hi'][lang])
    chips = ''.join(
        f'<span style="display: inline-flex; align-items: center; gap: 6px; height: 28px; padding-inline: 10px; border-radius: 999px; background: {FOAM}; color: {DEEP}; '
        f'font-family: {SANS}; font-size: 13px; font-weight: 600; white-space: nowrap;">{ico(a, 14, DEEP)}{AMEN[a][0 if he else 1]}</span>' for a in c['amen'])
    upd = f'{t["updated"]} {fdate(c["updated"], lang)}'
    arrow = ico('arrow_he' if he else 'arrow_en', 16)
    body = (
        f'<div style="padding: {pad}px; display: flex; flex-direction: column;">'
        f'<p style="margin: 0; font-family: {SANS}; font-size: 13px; line-height: 1.3; font-weight: 700; letter-spacing: {"0.02em" if he else "0.06em"}; color: {SEA};">{e(kicker)}</p>'
        f'<h3 style="margin: 8px 0 0;{"" if mobile else " height: " + str(title_lines*round(title_size*1.3)) + "px;"} font-family: {t["serif"]}; font-size: {title_size}px; line-height: 1.3; font-weight: 500; color: {INK}; text-wrap: balance;">{title_html}</h3>'
        f'<div style="margin-top: 12px;">{price_block(c, lang, t)}</div>'
        f'<div style="height: 1px; margin-block: 16px; background: {LINE};"></div>'
        f'<ul style="margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 14px; row-gap: 10px;">{specs}</ul>'
        f'<ul class="hi" style="margin: 16px 0 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 5px;{"" if mobile else " height: " + str(HEIGHTS.get("hi_"+lang, 92)) + "px;"}">{his}</ul>'
        f'<div class="chips" style="margin-top: 14px; display: flex; flex-wrap: wrap; align-content: flex-start; gap: 6px;{"" if mobile else " height: " + str(HEIGHTS.get("chips_"+lang, 28)) + "px;"}">{chips}</div>'
        f'<div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid {LINE}; display: flex; align-items: center; justify-content: space-between; gap: 12px;">'
        f'<span style="display: flex; align-items: center; gap: 7px; font-family: {SANS}; font-size: 14px; font-weight: 600; color: {INK};">{ico("key", 16, SEA)}<span style="{NUM}">{e(c["entry"][lang])}</span></span>'
        f'<span style="font-family: {SANS}; font-size: 13px; color: {MUTE}; white-space: nowrap; {NUM}">{upd}</span></div>'
        f'<div style="margin-top: 14px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px;">'
        f'{btn(t["c_wa"], "sea", "wa", lang, h=44, size=15, full=True, pad=12, href=wa_href)}'
        f'<a href="{href}" style="box-sizing: border-box; display: inline-flex; align-items: center; justify-content: center; gap: 8px; width: 100%; height: 44px; border-radius: 999px; border: 1px solid {INK}; color: {INK}; font-family: {SANS}; font-size: 15px; font-weight: 700; text-decoration: none; white-space: nowrap;"><span>{t["c_page"]}</span>{arrow}</a>'
        f'</div></div>')
    return (f'<article class="lcard" data-deal="{c["deal"]}" style="display: flex; flex-direction: column; background: {SURF}; border: 1px solid {LINE}; border-radius: 10px; overflow: hidden;">'
            f'{media}{body}</article>')

def ig_tile(lang):
    t = T[lang]
    return (f'<aside style="box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; gap: 28px; padding: 32px; background: {ABYSS}; color: {PAPER}; border-radius: 10px;">'
            f'<div style="display: flex; flex-direction: column; gap: 16px;">{ico("ig", 30, MIST)}'
            f'{eyebrow(t["ig_eyebrow"], lang, MIST, 13, False)}'
            f'<p style="margin: 0; font-family: {SERIF_EN}; font-size: 25px; line-height: 1.25; font-weight: 400; color: {PAPER}; overflow-wrap: anywhere;" dir="ltr">{HANDLE}</p>'
            f'<p style="margin: 0; font-family: {SANS}; font-size: 16px; line-height: 1.6; color: rgba(247, 246, 242, 0.8);">{t["ig_lead"]}</p></div>'
            f'<div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 18px;">'
            f'<div style="display: flex; flex-direction: column; gap: 10px;"><div style="padding: 12px; background: #FFFFFF; border-radius: 8px;">{qr(IG_URL, 120, ABYSS)}</div>'
            f'<span style="font-family: {SANS}; font-size: 13px; color: {MIST};">{t["ig_scan"]}</span></div>'
            f'{btn(t["ig_cta"], "ghost", "ig", lang, h=44, size=15, pad=18)}</div></aside>')

MEASURE = os.environ.get('MEASURE') == '1'

# ---------------------------------------------------------------- charts and map
def track_svg(vals, vmin, vmax, ticks, W, rtl, tick_fmt):
    pad, y = 18, 16
    def X(v):
        x = pad + (v - vmin) / (vmax - vmin) * (W - 2 * pad)
        return W - x if rtl else x
    lo, hi = min(v for _, v in vals), max(v for _, v in vals)
    x0, x1 = sorted((X(lo), X(hi)))
    s = [f'<svg viewBox="0 0 {W} 46" width="{W}" height="46" role="img" aria-hidden="true" style="display: block; overflow: visible;">',
         f'<path d="M{pad} {y}H{W-pad}" stroke="{MUTE}" stroke-opacity=".35" stroke-width="1"/>',
         f'<rect x="{x0:.1f}" y="{y-3}" width="{x1-x0:.1f}" height="6" rx="3" fill="{SEA}" fill-opacity=".26"/>']
    for tv in ticks:
        tx = X(tv)
        s.append(f'<path d="M{tx:.1f} {y+8}V{y+13}" stroke="{MUTE}" stroke-opacity=".7"/>')
        s.append(f'<text x="{tx:.1f}" y="{y+28}" text-anchor="middle" direction="ltr" font-family="Assistant, sans-serif" font-size="12" fill="{MUTE}">{tick_fmt(tv)}</text>')
    for _, v in vals:
        s.append(f'<circle cx="{X(v):.1f}" cy="{y}" r="6.5" fill="{DEEP}" stroke="#FFFFFF" stroke-width="2"/>')
    s.append('</svg>')
    return ''.join(s)

def ladder_row(deal, lang, W):
    t = T[lang]
    he = lang == 'he'
    ids = [i for i in ORDER if CARDS[i]['deal'] == deal]
    priced = sorted([(i, CARDS[i]['price']) for i in ids if CARDS[i]['price']], key=lambda x: x[1])
    ask = [i for i in ids if not CARDS[i]['price']]
    if deal == 'sale':
        vmin, vmax, ticks = 4e6, 20e6, [5e6, 10e6, 15e6, 20e6]
        tf = lambda v: f'{v/1e6:g}'
        vf = lambda v: (f'{v/1e6:.2f}'.rstrip('0').rstrip('.') if v % 1e6 else f'{v/1e6:.0f}')
        rng = f'{vf(priced[0][1])}-{vf(priced[-1][1])}'
        unit = t['n_sale_unit']
    else:
        vmin, vmax, ticks = 8000, 28000, [10000, 15000, 20000, 25000]
        tf = lambda v: f'{int(v):,}'
        vf = lambda v: f'{int(v):,}'
        rng = f'{vf(priced[0][1])}-{vf(priced[-1][1])}'
        unit = t['n_rent_unit']
    label = t['sale'] if deal == 'sale' else t['rent']
    chips = ''.join(
        f'<span style="display: inline-flex; align-items: center; gap: 8px; height: 32px; padding-inline: 12px; border-radius: 999px; border: 1px solid {LINE}; background: {PAPER}; '
        f'font-family: {SANS}; font-size: 14px; color: {INK2}; white-space: nowrap;"><b style="font-weight: 800; color: {INK}; letter-spacing: 0.04em;">{i}</b><span style="{NUM}">{vf(v)}</span></span>' for i, v in priced)
    chips += ''.join(
        f'<span style="display: inline-flex; align-items: center; gap: 8px; height: 32px; padding-inline: 12px; border-radius: 999px; border: 1px dashed #AEB8BF; '
        f'font-family: {SANS}; font-size: 14px; color: {MUTE}; white-space: nowrap;"><b style="font-weight: 800; color: {INK2}; letter-spacing: 0.04em;">{i}</b><span>{t["n_on_request"]}</span></span>' for i in ask)
    return (f'<div style="display: flex; flex-direction: column; gap: 12px;">'
            f'<div style="display: flex; align-items: baseline; justify-content: space-between; gap: 16px; flex-wrap: wrap;">'
            f'<p style="margin: 0; display: flex; align-items: baseline; gap: 10px;"><span style="font-family: {SANS}; font-size: 21px; font-weight: 700; color: {INK};">{label}</span>'
            f'<span style="font-family: {SANS}; font-size: 15px; color: {MUTE}; {NUM}">{len(ids)} {t["listings_word"]}</span></p>'
            f'<p style="margin: 0; display: flex; align-items: baseline; gap: 8px;"><span style="font-family: {t["serif"]}; font-size: 34px; line-height: 1.1; font-weight: 400; color: {INK}; {NUM}">{iso(rng)}</span>'
            f'<span style="font-family: {SANS}; font-size: 15px; font-weight: 600; color: {MUTE};">{unit}</span></p></div>'
            f'{track_svg(priced, vmin, vmax, ticks, W, he, tf)}'
            f'<div style="display: flex; flex-wrap: wrap; gap: 8px;">{chips}</div></div>')

def coast_map(lang, width):
    t = T[lang]
    W, H = 520, 600
    lat0, lat1, lon0, lon1 = 32.192, 32.058, 34.725, 34.862
    P = lambda la, lo: ((lo - lon0) / (lon1 - lon0) * W, (lat0 - la) / (lat0 - lat1) * H)
    coast = [(32.20, 34.808), (32.19, 34.806), (32.175, 34.801), (32.155, 34.797), (32.14, 34.795), (32.125, 34.791), (32.11, 34.784), (32.097, 34.775), (32.085, 34.768), (32.07, 34.762), (32.05, 34.756)]
    pts = [P(a, b) for a, b in coast]
    land = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + f' L{W} {H+10} L{W} -10 Z'
    line = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    s = [f'<svg viewBox="0 0 {W} {H}" width="{width}" height="{round(width*H/W)}" role="img" aria-label="{e(t["map_caption"])}" style="display: block;">',
         f'<rect width="{W}" height="{H}" fill="#DCEBEF"/>']
    for yy in range(36, H, 44):
        s.append(f'<path d="M-10 {yy} C 60 {yy-5}, 120 {yy+5}, 200 {yy}" stroke="#FFFFFF" stroke-opacity=".6" fill="none"/>')
    s.append(f'<path d="{land}" fill="{PAPER}"/>')
    s.append(f'<path d="{line}" fill="none" stroke="{SEA}" stroke-width="2"/>')
    y0 = P(32.097, 34.776)
    s.append(f'<path d="M{y0[0]:.0f} {y0[1]:.0f} C {y0[0]+50:.0f} {y0[1]+8:.0f}, {y0[0]+110:.0f} {y0[1]-10:.0f}, {W+10} {y0[1]+14:.0f}" fill="none" stroke="#9CC3CF" stroke-width="4" stroke-linecap="round"/>')
    s.append(f'<text x="44" y="{H/2:.0f}" transform="rotate(-90 44 {H/2:.0f})" text-anchor="middle" font-family="Assistant, sans-serif" font-size="15" font-weight="700" letter-spacing="1" fill="{SEA}">{e(t["map_sea"])}</text>')
    sides = {0: 'r', 1: 'r', 2: 'l', 3: 'r', 4: 'r', 5: 'r'}
    for k, (name, n, la, lo) in enumerate(t['areas']):
        x, y = P(la, lo)
        side = sides[k]
        tx = x + 22 if side == 'r' else x - 22
        anchor = 'start' if side == 'r' else 'end'
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{DEEP}" stroke="#FFFFFF" stroke-width="2.5"/>'
                 f'<text x="{x:.1f}" y="{y+4.8:.1f}" text-anchor="middle" font-family="Assistant, sans-serif" font-size="14" font-weight="800" fill="#FFFFFF">{n}</text>'
                 f'<text x="{tx:.1f}" y="{y+5.2:.1f}" text-anchor="{anchor}" direction="ltr" font-family="Assistant, sans-serif" font-size="16" font-weight="700" fill="{INK}" '
                 f'stroke="{PAPER}" stroke-width="5" stroke-linejoin="round" paint-order="stroke">{e(name)}</text>')
    s.append(f'<g transform="translate(40 40)"><path d="M0 18V-14M-7 -6L0 -14L7 -6" stroke="{INK2}" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<text x="0" y="36" text-anchor="middle" font-family="Assistant, sans-serif" font-size="12" font-weight="700" fill="{INK2}">{e(t["map_north"])}</text></g>')
    s.append('</svg>')
    return ''.join(s)

# ---------------------------------------------------------------- business card faces
def bcard_front(lang, S=1.0, radius=0):
    t = T[lang]
    he = lang == 'he'
    px = lambda v: f'{v*S:.1f}px'
    scene = card_scene(mirror=not he, sun_x=250)
    return (f'<div style="position: relative; width: {px(1050)}; height: {px(600)}; overflow: hidden; background: {ABYSS}; border-radius: {radius}px; color: {PAPER};">'
            f'<div style="position: absolute; inset: 0;">{scene}</div>'
            f'<div style="position: absolute; inset: 0; box-sizing: border-box; padding: {px(64)}; display: flex; flex-direction: column; justify-content: space-between;">'
            f'<p style="margin: 0; display: flex; align-items: center; gap: {px(18)}; font-family: {t["serif"]}; font-size: {px(38)}; line-height: 1.2; font-weight: 300; color: {MIST};">'
            f'<span style="display: block; width: {px(56)}; height: 1px; background: {MIST};"></span><span>{t["brand"]}</span></p>'
            f'<div style="display: flex; flex-direction: column; gap: {px(14)};">'
            f'<p style="margin: 0; font-family: {t["serif"]}; font-size: {px(104 if he else 92)}; line-height: 1; font-weight: 400; color: {PAPER}; white-space: nowrap;">{t["name"]}</p>'
            f'<p style="margin: 0; font-family: {SANS}; font-size: {px(26)}; line-height: 1.3; font-weight: 600; letter-spacing: 0.02em; color: {MIST};">{t["role"]} <span style="{NUM}">3131540</span></p>'
            f'</div></div></div>')

def bcard_back(lang, S=1.0, radius=0, border=True):
    t = T[lang]
    px = lambda v: f'{v*S:.1f}px'
    rows = [('phone', iso(PHONE[lang])), ('wa', t['direct_wa']), ('ig', iso(HANDLE)), ('pin', t['areas_line'])]
    rws = ''.join(f'<div style="display: flex; align-items: center; gap: {px(20)}; font-family: {SANS}; font-size: {px(28)}; line-height: 1.25; font-weight: 600; color: {INK};">'
                  f'{ico(k, max(10, round(28*S)), SEA)}<span style="{NUM}">{v}</span></div>' for k, v in rows)
    bd = f'border: 1px solid {LINE}; ' if border else ''
    return (f'<div style="position: relative; box-sizing: border-box; width: {px(1050)}; height: {px(600)}; overflow: hidden; background: #FFFFFF; {bd}border-radius: {radius}px; '
            f'padding: {px(64)}; display: flex; flex-direction: column; justify-content: space-between;">'
            f'<div style="display: flex; align-items: center; justify-content: space-between; gap: {px(40)};">'
            f'<div style="display: flex; flex-direction: column; gap: {px(26)};">{rws}</div>'
            f'<div style="display: flex; flex-direction: column; align-items: center; gap: {px(12)};">{qr("https://wa.me/" + WA_NUM, round(210*S), INK)}'
            f'<span style="font-family: {SANS}; font-size: {px(19)}; font-weight: 600; color: {MUTE};">{t["scan_wa"]}</span></div></div>'
            f'<div style="display: flex; align-items: center; gap: {px(18)};"><span style="display: block; flex: 1; height: 1px; background: {SEA}; opacity: 0.45;"></span>'
            f'<span dir="ltr" style="font-family: {SANS}; font-size: {px(18)}; font-weight: 600; letter-spacing: 0.02em; color: {MUTE}; unicode-bidi: isolate;">{t["share_url"]}</span></div></div>')

# ---------------------------------------------------------------- sections (desktop)
def nav(lang, pad=80, h=88, compact=False):
    t = T[lang]
    word = (f'<a href="#" dir="ltr" style="display: flex; align-items: baseline; font-family: {SANS}; font-size: {20 if compact else 25}px; font-weight: 800; letter-spacing: -0.01em; color: {PAPER}; text-decoration: none;">'
            f'nad-lan<span style="font-weight: 400; color: {MIST};">.co.il</span></a>')
    if compact:
        right = (f'<button type="button" aria-label="{"תפריט" if lang == "he" else "Menu"}" style="display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; '
                 f'padding: 0; border-radius: 999px; border: 1px solid rgba(247, 246, 242, 0.3); background: transparent; color: {PAPER}; cursor: pointer;">{ico("menu", 20, PAPER)}</button>')
    else:
        right = (f'<div style="display: flex; align-items: center; gap: 28px;"><a href="#" style="font-family: {SANS}; font-size: 16px; font-weight: 600; color: {PAPER}; text-decoration: none;">{t["nav_all"]}</a>'
                 f'<a href="#" style="display: inline-flex; align-items: center; height: 38px; padding-inline: 16px; border-radius: 999px; border: 1px solid rgba(247, 246, 242, 0.35); '
                 f'font-family: {SANS}; font-size: 14px; font-weight: 700; color: {PAPER}; text-decoration: none;">{t["nav_lang"]}</a></div>')
    return (f'<nav style="position: absolute; top: 0; left: 0; right: 0; height: {h}px; box-sizing: border-box; padding-inline: {pad}px; display: flex; align-items: center; '
            f'justify-content: space-between; border-bottom: 1px solid rgba(207, 227, 234, 0.14); z-index: 2;">{word}{right}</nav>')

def hero_desktop(lang):
    t = T[lang]
    he = lang == 'he'
    scene = media_img('hero', hero_scene(1440, 880, hz=700, sun_x=560, sky_x0=40, sky_x1=470, mirror=not he, seed='hero-d'), t['brand'])
    meta = ''.join(f'<div style="display: flex; flex-direction: column; gap: 6px;"><span style="font-family: {SANS}; font-size: 13px; font-weight: 600; letter-spacing: {"0.03em" if he else "0.08em"}; color: {MIST};">{a}</span>'
                   f'<span style="font-family: {SANS}; font-size: 22px; font-weight: 600; color: {PAPER}; {NUM}">{b}</span></div>' for a, b in t['meta'])
    h1 = 150 if he else 128
    return (f'<header style="position: relative; height: 880px; flex-shrink: 0; background: {ABYSS}; overflow: hidden;">'
            f'<div style="position: absolute; inset: 0;">{scene}</div>{nav(lang)}'
            f'<div style="position: absolute; top: 172px; {t["start"]}: 80px; width: {780 if he else 900}px; display: flex; flex-direction: column; align-items: flex-start;">'
            f'{eyebrow(t["eyebrow"], lang, MIST, 15)}'
            f'<h1 style="margin: 26px 0 0; font-family: {t["serif"]}; font-size: {h1}px; line-height: 1; font-weight: 400; letter-spacing: -0.01em; color: {PAPER}; white-space: nowrap;">{t["name"]}</h1>'
            f'<p style="margin: 20px 0 0; font-family: {t["serif"]}; font-size: 42px; line-height: 1.15; font-weight: 300; {"font-style: italic; " if not he else ""}color: {MIST};">{t["brand"]}</p>'
            f'<p style="margin: 28px 0 0; max-width: 600px; font-family: {SANS}; font-size: 21px; line-height: 1.6; color: rgba(247, 246, 242, 0.86);">{t["lede"]}</p>'
            f'<div style="margin-top: 40px; display: flex; flex-wrap: wrap; gap: 12px;">'
            f'{btn(t["wa"], "paper", "wa", lang, h=56, size=17)}{btn(iso(PHONE[lang]), "ghost", "phone", lang, h=56, size=17, aria=PHONE[lang])}{btn(t["ig"], "ghost", "ig", lang, h=56, size=17)}</div></div>'
            f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 104px; box-sizing: border-box; padding-inline: 80px; display: flex; align-items: center; gap: 64px; border-top: 1px solid rgba(207, 227, 234, 0.18);">'
            f'{meta}<span dir="ltr" style="margin-inline-start: auto; font-family: {SANS}; font-size: 13px; letter-spacing: 0.06em; color: rgba(207, 227, 234, 0.7); unicode-bidi: isolate; {NUM}">{t["coords"]}</span></div>'
            f'</header>')

def feature_desktop(lang):
    t = T[lang]
    he = lang == 'he'
    stats = ''.join(f'<div style="display: flex; flex-direction: column; gap: 8px;"><b style="font-family: {SANS}; font-size: 44px; line-height: 1; font-weight: 300; color: {INK}; {NUM}">{a}</b>'
                    f'<span style="font-family: {SANS}; font-size: 14px; color: {MUTE};">{b}</span></div>' for a, b in t['f_stats'])
    media = media_img('L01', estate_night(), t['f_title'])
    return (f'<section style="flex-shrink: 0; padding: 112px 80px; background: {PAPER};">'
            f'<div style="display: flex; gap: 40px; align-items: center;">'
            f'<div style="width: 480px; flex-shrink: 0; display: flex; flex-direction: column;">'
            f'{eyebrow(t["f_eyebrow"], lang)}'
            f'<h2 style="margin: 18px 0 0; font-family: {t["serif"]}; font-size: {64 if he else 58}px; line-height: 1.05; font-weight: 400; color: {INK}; text-wrap: balance;">{t["f_title"]}</h2>'
            f'<p style="margin: 22px 0 0; font-family: {SANS}; font-size: 19px; line-height: 1.65; color: {INK2};">{t["f_lead"]}</p>'
            f'<div style="margin-top: 30px; padding-top: 22px; border-top: 1px solid {LINE}; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px;">{stats}</div>'
            f'<p style="margin: 26px 0 0; font-family: {SANS}; font-size: 16px; line-height: 1.6; color: {INK2};">{t["f_amen"]}</p>'
            f'<div style="margin-top: 26px; display: flex; flex-direction: column; gap: 4px;"><strong style="font-family: {SANS}; font-size: 24px; font-weight: 800; color: {INK};">{t["f_price"]}</strong>'
            f'<span style="font-family: {SANS}; font-size: 15px; color: {MUTE};">{t["f_price_sub"]}</span></div>'
            f'<div style="margin-top: 30px; display: flex; flex-wrap: wrap; gap: 12px;">{btn(t["f_cta"], "abyss", "wa", lang, h=52, size=16)}{btn(t["f_cta2"], "line", None, lang, h=52, size=16)}</div>'
            f'</div>'
            f'<div style="position: relative; flex: 1; min-width: 0; height: 600px; border-radius: 22px; overflow: hidden; background: {ABYSS};">{media}'
            f'<span style="position: absolute; top: 20px; {t["start"]}: 20px; display: inline-flex; align-items: center; height: 30px; padding-inline: 12px; border-radius: 8px; background: rgba(16, 38, 47, 0.62); color: {PAPER}; font-family: {SANS}; font-size: 13px; font-weight: 700; letter-spacing: 0.06em;">L01</span>'
            f'{"" if IMAGES.get("L01") else f"""<span style="position: absolute; bottom: 18px; {t["end"]}: 20px; font-family: {SANS}; font-size: 12px; font-weight: 600; letter-spacing: 0.04em; color: rgba(207, 227, 234, 0.7);">{t["illus"]}</span>"""}'
            f'</div></div></section>')

def numbers_desktop(lang):
    t = T[lang]
    return (f'<section style="flex-shrink: 0; padding: 104px 80px; background: #FFFFFF; border-block: 1px solid {LINE};">'
            f'<div style="display: flex; gap: 64px; align-items: flex-start;">'
            f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column;">'
            f'{eyebrow(t["n_eyebrow"], lang)}'
            f'<h2 style="margin: 18px 0 0; font-family: {t["serif"]}; font-size: 52px; line-height: 1.1; font-weight: 400; color: {INK};">{t["n_title"]}</h2>'
            f'<p style="margin: 18px 0 0; max-width: 640px; font-family: {SANS}; font-size: 18px; line-height: 1.6; color: {INK2};">{t["n_lead"]}</p>'
            f'<div style="margin-top: 48px; display: flex; flex-direction: column; gap: 44px;">{ladder_row("sale", lang, 760)}{ladder_row("rent", lang, 760)}</div>'
            f'</div>'
            f'<figure style="margin: 0; width: 456px; flex-shrink: 0;">'
            f'<div style="border-radius: 14px; overflow: hidden; border: 1px solid {LINE};">{coast_map(lang, 454)}</div>'
            f'<figcaption style="margin-top: 12px; font-family: {SANS}; font-size: 13px; line-height: 1.5; color: {MUTE};">{t["map_caption"]}</figcaption></figure>'
            f'</div></section>')

def pill(key, label, count):
    return (f'<button type="button" onClick="{{{{ pills.{key}.pick }}}}" aria-pressed="{{{{ pills.{key}.pressed }}}}" style="display: inline-flex; align-items: center; gap: 8px; height: 44px; padding-inline: 20px; '
            f'border-radius: 999px; border: 1px solid {{{{ pills.{key}.bd }}}}; background: {{{{ pills.{key}.bg }}}}; color: {{{{ pills.{key}.fg }}}}; font-family: {SANS}; font-size: 15px; font-weight: 700; cursor: pointer;">'
            f'<span>{label}</span><span style="opacity: 0.72; {NUM}">{count}</span></button>')

def listings_desktop(lang):
    t = T[lang]
    n_sale = sum(1 for i in ORDER if CARDS[i]['deal'] == 'sale')
    n_rent = len(ORDER) - n_sale
    cells = ''.join(f'<sc-if value="{{{{ {"showSale" if CARDS[i]["deal"] == "sale" else "showRent"} }}}}" hint-placeholder-val="{{{{ true }}}}">{card(i, lang, title_lines=row_lines(lang, ORDER, i))}</sc-if>' for i in ORDER)
    group_label = 'סינון לפי סוג עסקה' if lang == 'he' else 'Filter by deal type'
    return (f'<section style="flex-shrink: 0; padding: 112px 80px 120px; background: {PAPER};">'
            f'<div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 40px;">'
            f'<div style="max-width: 720px; display: flex; flex-direction: column;">{eyebrow(t["l_eyebrow"], lang)}'
            f'<h2 style="margin: 18px 0 0; font-family: {t["serif"]}; font-size: 56px; line-height: 1.08; font-weight: 400; color: {INK};">{t["l_title"]}</h2>'
            f'<p style="margin: 18px 0 0; font-family: {SANS}; font-size: 18px; line-height: 1.6; color: {INK2};">{t["l_lead"]}</p></div>'
            f'<div role="group" aria-label="{group_label}" style="display: flex; gap: 8px; flex-shrink: 0;">{pill("all", t["all"], len(ORDER))}{pill("sale", t["sale"], n_sale)}{pill("rent", t["rent"], n_rent)}</div>'
            f'</div>'
            f'<div style="margin-top: 48px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: 32px; row-gap: 36px; align-items: stretch;">{cells}{ig_tile(lang)}</div>'
            f'</section>')

def bcards_desktop(lang):
    t = T[lang]
    return (f'<section style="flex-shrink: 0; padding: 96px 80px; background: {SAND};">'
            f'<div style="display: flex; align-items: center; gap: 56px;">'
            f'<div style="width: 360px; flex-shrink: 0; display: flex; flex-direction: column;">{eyebrow(t["b_eyebrow"], lang)}'
            f'<h2 style="margin: 18px 0 0; font-family: {t["serif"]}; font-size: 42px; line-height: 1.12; font-weight: 400; color: {INK}; text-wrap: balance;">{t["b_title"]}</h2>'
            f'<p style="margin: 18px 0 0; font-family: {SANS}; font-size: 17px; line-height: 1.6; color: {INK2};">{t["b_lead"]}</p></div>'
            f'<div style="flex: 1; min-width: 0; display: flex; gap: 24px; justify-content: space-between;">'
            f'<div style="box-shadow: 0 18px 40px rgba(16, 38, 47, 0.18); border-radius: 12px;">{bcard_front(lang, 0.4, 12)}</div>'
            f'<div style="box-shadow: 0 18px 40px rgba(16, 38, 47, 0.12); border-radius: 12px;">{bcard_back(lang, 0.4, 12, border=False)}</div>'
            f'</div></div></section>')

def contact_desktop(lang, grow=True):
    t = T[lang]
    method = ''.join(f'<div style="display: flex; flex-direction: column; gap: 10px;"><h3 style="margin: 0; font-family: {SANS}; font-size: 18px; font-weight: 700; color: {PAPER};">{a}</h3>'
                     f'<p style="margin: 0; font-family: {SANS}; font-size: 15px; line-height: 1.6; color: rgba(207, 227, 234, 0.82);">{b}</p></div>' for a, b in t['method'])
    return (f'<footer style="{"flex-grow: 1; " if grow and not MEASURE else ""}padding: 112px 80px 64px; background: {ABYSS}; color: {PAPER}; display: flex; flex-direction: column;">'
            f'<div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 48px;">'
            f'<div style="max-width: 760px; display: flex; flex-direction: column;">{eyebrow(t["k_eyebrow"], lang, MIST)}'
            f'<h2 style="margin: 20px 0 0; font-family: {t["serif"]}; font-size: 72px; line-height: 1.05; font-weight: 400; color: {PAPER};">{t["k_title"]}</h2>'
            f'<p style="margin: 18px 0 0; font-family: {SANS}; font-size: 20px; line-height: 1.6; color: rgba(207, 227, 234, 0.9);">{t["k_lead"]}</p></div>'
            f'<div style="display: flex; gap: 12px; flex-shrink: 0;">{btn(t["c_wa"], "paper", "wa", lang, h=56, size=17)}{btn(iso(PHONE[lang]), "ghost", "phone", lang, h=56, size=17, aria=PHONE[lang])}</div></div>'
            f'<div style="margin-top: 80px; padding-top: 40px; border-top: 1px solid rgba(207, 227, 234, 0.18); display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 48px;">{method}</div>'
            f'<p style="margin: 48px 0 0; max-width: 980px; font-family: {SANS}; font-size: 13px; line-height: 1.7; color: rgba(207, 227, 234, 0.66);">{t["legal"]}</p>'
            f'<div style="margin-top: 36px; display: flex; align-items: center; justify-content: space-between; font-family: {SANS}; font-size: 13px; color: rgba(207, 227, 234, 0.66);">'
            f'<span dir="ltr" style="unicode-bidi: isolate;">nad-lan.co.il</span><span style="{NUM}">© 2026</span></div>'
            f'</footer>')

# ---------------------------------------------------------------- mobile sections
def hero_mobile(lang, H=780, hz=660, first_screen=False, meta_bottom=0):
    t = T[lang]
    he = lang == 'he'
    scene = media_img('hero_m', hero_scene(390, H, hz=hz, sun_x=70, sky_x0=196, sky_x1=390, mirror=not he, seed='hero-m', sun_r=32, max_h=120), t['brand'])
    meta = ''.join(f'<div style="display: flex; flex-direction: column; gap: 3px; min-width: 0;"><span style="font-family: {SANS}; font-size: 11px; font-weight: 600; color: {MIST};">{a}</span>'
                   f'<span style="font-family: {SANS}; font-size: 15px; font-weight: 600; color: {PAPER}; {NUM}">{b}</span></div>' for a, b in t['meta'])
    return (f'<header style="position: relative; height: {H}px; flex-shrink: 0; background: {ABYSS}; overflow: hidden;">'
            f'<div style="position: absolute; inset: 0;">{scene}</div>{nav(lang, pad=20, h=64, compact=True)}'
            f'<div style="position: absolute; top: 104px; left: 24px; right: 24px; display: flex; flex-direction: column; align-items: stretch;">'
            f'{eyebrow(t["eyebrow"], lang, MIST, 13)}'
            f'<h1 style="margin: 18px 0 0; font-family: {t["serif"]}; font-size: {68 if he else 56}px; line-height: 1.02; font-weight: 400; color: {PAPER};">{t["name"]}</h1>'
            f'<p style="margin: 10px 0 0; font-family: {t["serif"]}; font-size: 26px; line-height: 1.2; font-weight: 300; {"font-style: italic; " if not he else ""}color: {MIST};">{t["brand"]}</p>'
            f'<p style="margin: 18px 0 0; font-family: {SANS}; font-size: 17px; line-height: 1.6; color: rgba(247, 246, 242, 0.86);">{t["lede"]}</p>'
            f'<div style="margin-top: 26px; display: flex; flex-direction: column; gap: 10px;">{btn(t["wa"], "paper", "wa", lang, h=52, size=16, full=True)}'
            f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px;">{btn(iso(PHONE[lang]), "ghost", "phone", lang, h=48, size=15, full=True, pad=10, aria=PHONE[lang])}{btn(t["ig"], "ghost", "ig", lang, h=48, size=15, full=True, pad=10)}</div></div></div>'
            f'<div style="position: absolute; left: 0; right: 0; bottom: {meta_bottom}px; height: 76px; box-sizing: border-box; padding-inline: 24px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); align-items: center; gap: 12px; border-top: 1px solid rgba(207, 227, 234, 0.18);">{meta}</div>'
            f'</header>')

def feature_mobile(lang):
    t = T[lang]
    he = lang == 'he'
    stats = ''.join(f'<div style="display: flex; flex-direction: column; gap: 6px; padding-block: 14px; border-top: 1px solid {LINE};"><b style="font-family: {SANS}; font-size: 34px; line-height: 1; font-weight: 300; color: {INK}; {NUM}">{a}</b>'
                    f'<span style="font-family: {SANS}; font-size: 13px; color: {MUTE};">{b}</span></div>' for a, b in t['f_stats'])
    return (f'<section style="flex-shrink: 0; background: {PAPER};">'
            f'<div style="position: relative; height: 300px; overflow: hidden; background: {ABYSS};">{media_img("L01", estate_night(), t["f_title"])}'
            f'<span style="position: absolute; top: 16px; {t["start"]}: 16px; display: inline-flex; align-items: center; height: 26px; padding-inline: 10px; border-radius: 6px; background: rgba(16, 38, 47, 0.62); color: {PAPER}; font-family: {SANS}; font-size: 12px; font-weight: 700; letter-spacing: 0.06em;">L01</span></div>'
            f'<div style="padding: 36px 24px 48px; display: flex; flex-direction: column;">{eyebrow(t["f_eyebrow"], lang, SEA, 13)}'
            f'<h2 style="margin: 14px 0 0; font-family: {t["serif"]}; font-size: 42px; line-height: 1.08; font-weight: 400; color: {INK};">{t["f_title"]}</h2>'
            f'<p style="margin: 16px 0 0; font-family: {SANS}; font-size: 17px; line-height: 1.65; color: {INK2};">{t["f_lead"]}</p>'
            f'<div style="margin-top: 22px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 20px;">{stats}</div>'
            f'<p style="margin: 14px 0 0; font-family: {SANS}; font-size: 15px; line-height: 1.6; color: {INK2};">{t["f_amen"]}</p>'
            f'<div style="margin-top: 20px; display: flex; flex-direction: column; gap: 2px;"><strong style="font-family: {SANS}; font-size: 22px; font-weight: 800; color: {INK};">{t["f_price"]}</strong>'
            f'<span style="font-family: {SANS}; font-size: 14px; color: {MUTE};">{t["f_price_sub"]}</span></div>'
            f'<div style="margin-top: 22px; display: flex; flex-direction: column; gap: 10px;">{btn(t["f_cta"], "abyss", "wa", lang, h=52, size=16, full=True)}{btn(t["f_cta2"], "line", None, lang, h=52, size=16, full=True)}</div>'
            f'</div></section>')

def numbers_mobile(lang):
    t = T[lang]
    return (f'<section style="flex-shrink: 0; padding: 56px 24px; background: #FFFFFF; border-block: 1px solid {LINE}; display: flex; flex-direction: column;">'
            f'{eyebrow(t["n_eyebrow"], lang, SEA, 13)}'
            f'<h2 style="margin: 14px 0 0; font-family: {t["serif"]}; font-size: 34px; line-height: 1.12; font-weight: 400; color: {INK};">{t["n_title"]}</h2>'
            f'<p style="margin: 14px 0 0; font-family: {SANS}; font-size: 16px; line-height: 1.6; color: {INK2};">{t["n_lead"]}</p>'
            f'<div style="margin-top: 32px; display: flex; flex-direction: column; gap: 36px;">{ladder_row("sale", lang, 342)}{ladder_row("rent", lang, 342)}</div>'
            f'</section>')

def listings_mobile(lang, ids=('L07', 'L06', 'L09')):
    t = T[lang]
    n_sale = sum(1 for i in ORDER if CARDS[i]['deal'] == 'sale')
    pills = ''.join(
        f'<button type="button" aria-pressed="{"true" if k == "all" else "false"}" style="display: inline-flex; align-items: center; gap: 6px; height: 40px; padding-inline: 16px; border-radius: 999px; '
        f'border: 1px solid {INK if k == "all" else LINE}; background: {INK if k == "all" else "transparent"}; color: {PAPER if k == "all" else INK}; font-family: {SANS}; font-size: 14px; font-weight: 700;">'
        f'<span>{lab}</span><span style="opacity: 0.72; {NUM}">{n}</span></button>'
        for k, lab, n in (('all', t['all'], len(ORDER)), ('sale', t['sale'], n_sale), ('rent', t['rent'], len(ORDER) - n_sale)))
    cards = ''.join(card(i, lang, media_h=214, pad=20, mobile=True) for i in ids)
    return (f'<section style="flex-shrink: 0; padding: 56px 24px; background: {PAPER}; display: flex; flex-direction: column;">'
            f'{eyebrow(t["l_eyebrow"], lang, SEA, 13)}'
            f'<h2 style="margin: 14px 0 0; font-family: {t["serif"]}; font-size: 36px; line-height: 1.1; font-weight: 400; color: {INK};">{t["l_title"]}</h2>'
            f'<p style="margin: 14px 0 0; font-family: {SANS}; font-size: 16px; line-height: 1.6; color: {INK2};">{t["l_lead"]}</p>'
            f'<div style="margin-top: 22px; display: flex; gap: 8px;">{pills}</div>'
            f'<div style="margin-top: 24px; display: flex; flex-direction: column; gap: 20px;">{cards}</div>'
            f'<div style="margin-top: 20px;">{btn(t["more"], "line", None, lang, h=52, size=16, full=True)}</div>'
            f'</section>')

def bcards_mobile(lang):
    t = T[lang]
    S = 342 / 1050
    return (f'<section style="flex-shrink: 0; padding: 56px 24px; background: {SAND}; display: flex; flex-direction: column;">'
            f'{eyebrow(t["b_eyebrow"], lang, SEA, 13)}'
            f'<h2 style="margin: 14px 0 0; font-family: {t["serif"]}; font-size: 34px; line-height: 1.12; font-weight: 400; color: {INK};">{t["b_title"]}</h2>'
            f'<p style="margin: 14px 0 0; font-family: {SANS}; font-size: 16px; line-height: 1.6; color: {INK2};">{t["b_lead"]}</p>'
            f'<div style="margin-top: 26px; display: flex; flex-direction: column; gap: 16px;">'
            f'<div style="box-shadow: 0 14px 30px rgba(16, 38, 47, 0.18); border-radius: 10px;">{bcard_front(lang, S, 10)}</div>'
            f'<div style="box-shadow: 0 14px 30px rgba(16, 38, 47, 0.1); border-radius: 10px;">{bcard_back(lang, S, 10, border=False)}</div></div>'
            f'</section>')

def contact_mobile(lang):
    t = T[lang]
    method = ''.join(f'<div style="display: flex; flex-direction: column; gap: 6px; padding-top: 16px; border-top: 1px solid rgba(207, 227, 234, 0.18);"><h3 style="margin: 0; font-family: {SANS}; font-size: 16px; font-weight: 700; color: {PAPER};">{a}</h3>'
                     f'<p style="margin: 0; font-family: {SANS}; font-size: 14px; line-height: 1.6; color: rgba(207, 227, 234, 0.82);">{b}</p></div>' for a, b in t['method'])
    return (f'<footer style="{"flex-grow: 1; " if not MEASURE else ""}padding: 56px 24px 112px; background: {ABYSS}; color: {PAPER}; display: flex; flex-direction: column;">'
            f'{eyebrow(t["k_eyebrow"], lang, MIST, 13)}'
            f'<h2 style="margin: 14px 0 0; font-family: {t["serif"]}; font-size: 40px; line-height: 1.08; font-weight: 400; color: {PAPER};">{t["k_title"]}</h2>'
            f'<p style="margin: 14px 0 0; font-family: {SANS}; font-size: 16px; line-height: 1.6; color: rgba(207, 227, 234, 0.9);">{t["k_lead"]}</p>'
            f'<div style="margin-top: 24px; display: flex; flex-direction: column; gap: 10px;">{btn(t["c_wa"], "paper", "wa", lang, h=52, size=16, full=True)}{btn(iso(PHONE[lang]), "ghost", "phone", lang, h=52, size=16, full=True, aria=PHONE[lang])}</div>'
            f'<div style="margin-top: 40px; display: flex; flex-direction: column; gap: 18px;">{method}</div>'
            f'<p style="margin: 28px 0 0; font-family: {SANS}; font-size: 12px; line-height: 1.7; color: rgba(207, 227, 234, 0.66);">{t["legal"]}</p>'
            f'</footer>')

def sticky_bar(lang):
    t = T[lang]
    return (f'<div style="position: absolute; left: 0; right: 0; bottom: 0; box-sizing: border-box; padding: 12px 16px 16px; background: rgba(247, 246, 242, 0.97); border-top: 1px solid {LINE}; '
            f'display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; z-index: 5;">'
            f'{btn(t["c_wa"], "sea", "wa", lang, h=48, size=16, full=True, pad=10)}{btn(t["k_call"], "white", "phone", lang, h=48, size=16, full=True, pad=10)}</div>')

# ---------------------------------------------------------------- artboard files
def dc_file(lang, w, h, inner, logic='class Component extends DCLogic {\n  renderVals() {\n    return {};\n  }\n}', bg=PAPER, props=None):
    t = T[lang]
    p = {'$preview': {'width': w, 'height': h}}
    if props:
        p.update(props)
    hh = 'auto' if MEASURE else f'{h}px'
    root = (f'<div id="root" dir="{t["dir"]}" lang="{lang}" style="position: relative; width: {w}px; height: {hh}; box-sizing: border-box; display: flex; flex-direction: column; '
            f'overflow: hidden; background: {bg}; color: {INK}; font-family: {SANS}; -webkit-font-smoothing: antialiased;">{inner}</div>')
    return f'''<!doctype html>
<html lang="{lang}" dir="{t["dir"]}">
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="{FONTS}">
  <style>
    body {{ margin: 0; background: {bg}; }}
    a {{ color: {SEA}; }} a:hover {{ color: {SEA_H}; }}
    a:focus-visible, button:focus-visible {{ outline: 2px solid {SEA}; outline-offset: 3px; }}
  </style>
</helmet>
{root}
</x-dc>
<script data-dc-script data-props='{json.dumps(p, ensure_ascii=False)}'>
{logic}
</script>
</body>
</html>
'''

FILTER_LOGIC = '''class Component extends DCLogic {
  renderVals() {
    const f = (this.state && this.state.filter) || 'all';
    const pill = (key) => ({
      pick: () => this.setState({ filter: key }),
      pressed: f === key,
      bg: f === key ? '#14212B' : 'transparent',
      fg: f === key ? '#F7F6F2' : '#14212B',
      bd: f === key ? '#14212B' : '#E3E1DA'
    });
    return {
      showSale: f !== 'rent',
      showRent: f !== 'sale',
      pills: { all: pill('all'), sale: pill('sale'), rent: pill('rent') }
    };
  }
}'''

def page_desktop(lang):
    inner = hero_desktop(lang) + feature_desktop(lang) + numbers_desktop(lang) + listings_desktop(lang) + bcards_desktop(lang) + contact_desktop(lang)
    key = 'Main' if lang == 'he' else 'English'
    return dc_file(lang, 1440, HEIGHTS.get(key, 7400), inner, FILTER_LOGIC, bg=ABYSS)

def page_mobile(lang):
    inner = hero_mobile(lang) + feature_mobile(lang) + numbers_mobile(lang) + listings_mobile(lang) + bcards_mobile(lang) + contact_mobile(lang) + sticky_bar(lang)
    return dc_file(lang, 390, HEIGHTS.get('Mobile', 6400), inner, bg=ABYSS)

def page_first_screen(lang):
    inner = hero_mobile(lang, H=844, hz=660, meta_bottom=76) + sticky_bar(lang)
    return dc_file(lang, 390, 844, inner, bg=ABYSS)

def card_sheet(lang):
    labels = {'he': ['מכירה עם מחיר מפורסם', 'השכרה עם תנאי תשלום', 'זמינות בבדיקה'], 'en': ['Sale with a published price', 'Rent with payment terms', 'Availability being confirmed']}[lang]
    ids = ('L07', 'L06', 'L09')
    lines = max(TL(lang, j) for j in ids)
    cols = ''.join(f'<div style="display: flex; flex-direction: column; gap: 14px;"><p style="margin: 0; font-family: {SANS}; font-size: 14px; font-weight: 700; letter-spacing: 0.03em; color: {MUTE};">{lab}</p>{card(i, lang, title_lines=lines)}</div>'
                   for lab, i in zip(labels, ids))
    inner = f'<div style="box-sizing: border-box; padding: 64px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: 48px; align-items: start;">{cols}</div>'
    return dc_file(lang, 1440, HEIGHTS.get('ListingCard', 1000), inner)

def share_image(lang):
    t = T[lang]
    he = lang == 'he'
    scene = hero_scene(1080, 1350, hz=930, sun_x=250, sky_x0=500, sky_x1=1060, mirror=not he, seed='share')
    stats = ''.join(f'<div style="display: flex; flex-direction: column; gap: 10px;"><b style="font-family: {SANS}; font-size: 118px; line-height: 0.9; font-weight: 300; color: {PAPER}; {NUM}">{a}</b>'
                    f'<span style="font-family: {SANS}; font-size: 30px; font-weight: 600; color: {MIST};">{b}</span></div>' for a, b in t['share_stats'])
    inner = (f'<div style="position: absolute; inset: 0;">{scene}</div>'
             f'<div style="position: absolute; inset: 0; box-sizing: border-box; padding: 88px; display: flex; flex-direction: column;">'
             f'{eyebrow(t["share_kicker"], lang, MIST, 26)}'
             f'<p style="margin: 64px 0 0; font-family: {t["serif"]}; font-size: {172 if he else 140}px; line-height: 0.98; font-weight: 400; color: {PAPER};">{t["name"]}</p>'
             f'<p style="margin: 22px 0 0; font-family: {t["serif"]}; font-size: 60px; line-height: 1.1; font-weight: 300; {"font-style: italic; " if not he else ""}color: {MIST};">{t["brand"]}</p>'
             f'<p style="margin: 40px 0 0; font-family: {SANS}; font-size: 36px; line-height: 1.4; color: rgba(247, 246, 242, 0.88);">{t["share_line"]}</p>'
             f'<div style="margin-top: auto; display: flex; gap: 88px;">{stats}</div>'
             f'<p dir="ltr" style="margin: 56px 0 0; font-family: {SANS}; font-size: 30px; font-weight: 600; letter-spacing: 0.02em; color: {MIST}; text-align: {t["start"]}; unicode-bidi: isolate;">{t["share_url"]}</p>'
             f'</div>')
    return dc_file(lang, 1080, 1350, inner, bg=ABYSS)

def write_all():
    os.makedirs(OUT, exist_ok=True)
    files = {
        'Main.dc.html': page_desktop('he'),
        'English.dc.html': page_desktop('en'),
        'Mobile.dc.html': page_mobile('he'),
        'MobileFirst.dc.html': page_first_screen('he'),
        'ListingCard.dc.html': card_sheet('he'),
        'BusinessCardFront.dc.html': dc_file('he', 1050, 600, bcard_front('he', 1.0, 0), bg=ABYSS),
        'BusinessCardBack.dc.html': dc_file('he', 1050, 600, bcard_back('he', 1.0, 0, border=False), bg='#FFFFFF'),
        'ShareImage.dc.html': share_image('he'),
    }
    for k, v in files.items():
        assert chr(0x2013) not in v and chr(0x2014) not in v, k
        open(OUT + k, 'w').write(v)
    return files

def write_index():
    Hm, He, Hmob, Hc = HEIGHTS.get('Main', 7400), HEIGHTS.get('English', 7400), HEIGHTS.get('Mobile', 6400), HEIGHTS.get('ListingCard', 1000)
    row2 = 1350 + 420
    idx = {
        'v': 3,
        'createdOnFiles': {'v': 1, 'at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
        'title': 'מיטל קציר, נדל״ן על הים',
        'launch': {'view': 'canvas', 'page': 'broker'},
        'pages': [{'id': 'broker', 'name': 'עמוד המתווכת'}, {'id': 'brand', 'name': 'כרטיסים ומיתוג'}],
        'boards': {
            'Main.dc.html': {'x': 0, 'y': 0, 'w': 1440, 'h': Hm, 'title': 'עמוד מתווכת · עברית · דסקטופ', 'page': 'broker', 'is_interactive': True},
            'Mobile.dc.html': {'x': 1520, 'y': 0, 'w': 390, 'h': Hmob, 'title': 'מובייל · העמוד המלא', 'page': 'broker'},
            'MobileFirst.dc.html': {'x': 1990, 'y': 0, 'w': 390, 'h': 844, 'title': 'מובייל · מסך ראשון', 'page': 'broker'},
            'English.dc.html': {'x': 2460, 'y': 0, 'w': 1440, 'h': He, 'title': 'Broker page · English', 'page': 'broker', 'is_interactive': True},
            'ListingCard.dc.html': {'x': 0, 'y': 0, 'w': 1440, 'h': Hc, 'title': 'כרטיס נכס · שלושה מצבים', 'page': 'brand'},
            'ShareImage.dc.html': {'x': 1520, 'y': 0, 'w': 1080, 'h': 1350, 'title': 'פוסט לאינסטגרם · 1080×1350', 'page': 'brand'},
            'BusinessCardFront.dc.html': {'x': 0, 'y': row2, 'w': 1050, 'h': 600, 'title': 'כרטיס ביקור · חזית', 'page': 'brand'},
            'BusinessCardBack.dc.html': {'x': 1130, 'y': row2, 'w': 1050, 'h': 600, 'title': 'כרטיס ביקור · גב', 'page': 'brand'},
        },
        'order': ['Main.dc.html', 'Mobile.dc.html', 'MobileFirst.dc.html', 'English.dc.html', 'ListingCard.dc.html', 'ShareImage.dc.html', 'BusinessCardFront.dc.html', 'BusinessCardBack.dc.html'],
        'notes': {
            'title-broker': {'x': 0, 'y': -300, 'text': 'מיטל קציר · נדל״ן על הים · עמוד מתווכת ב-nad-lan', 'kind': 'title1', 'maxW': 3900, 'page': 'broker'},
            'title-brand': {'x': 0, 'y': -300, 'text': 'כרטיס נכס ופוסט לאינסטגרם', 'kind': 'title1', 'maxW': 2600, 'page': 'brand'},
            'title-bcard': {'x': 0, 'y': row2 - 300, 'text': 'כרטיס ביקור, 3.5×2 אינץ׳', 'kind': 'title1', 'maxW': 2180, 'page': 'brand'},
        },
        'designSystems': [],
    }
    open(OUT + 'canvas.json', 'w').write(json.dumps(idx, ensure_ascii=False, indent=1))
    return idx

if __name__ == '__main__':
    files = write_all()
    write_index()
    for k, v in files.items():
        print(f'{k:28s} {len(v):>8,} bytes')
