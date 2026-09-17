#!/usr/bin/env python3
"""Broker profile page (nlb v2, "Waterline") for Meital Katzir on nad-lan.co.il, Hebrew and English.
Same design as the Claude Design canvas; output is WordPress-ready HTML for a wp:html block."""
import json, os, re, html, base64, urllib.parse, sys
from jinja2 import Environment, FileSystemLoader

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE)) + '/'
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'design'))
import build as B
import gen_canvas as G
from scenes import plate, estate_night, hero_scene, card_scene

CARDS = json.load(open(HERE + '/cards.json'))
ORDER = G.ORDER
PHONE_INTL = '+972523631582'
WA = 'https://wa.me/972523631582'
IG = 'https://www.instagram.com/meitalkatzir_realestate/'

def icon(name):
    body = G.WA_PATH if name == 'wa' else G.ICONS[name]
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'

def fint(n):
    return f"{int(round(n)):,}"

def img_src(path, embed):
    if not path or not os.path.exists(path):
        return None
    if not embed:
        return os.path.relpath(path, BASE)
    return 'data:image/jpeg;base64,' + base64.b64encode(open(path, 'rb').read()).decode()

def responsive_svg(svg):
    """Drop fixed width/height so CSS sizes the drawing."""
    return re.sub(r'^<svg([^>]*?) width="[\d.]+" height="[\d.]+"', r'<svg\1', svg, count=1)

def ladder(deal, lang):
    t = G.T[lang]
    he = lang == 'he'
    ids = [i for i in ORDER if CARDS[i]['deal'] == deal]
    priced = sorted([(i, CARDS[i]['price']) for i in ids if CARDS[i]['price']], key=lambda x: x[1])
    ask = [i for i in ids if not CARDS[i]['price']]
    if deal == 'sale':
        vmin, vmax, ticks = 4e6, 20e6, [5e6, 10e6, 15e6, 20e6]
        tf = lambda v: f'{v/1e6:g}'
        vf = lambda v: (f'{v/1e6:.2f}'.rstrip('0').rstrip('.') if v % 1e6 else f'{v/1e6:.0f}')
        unit = t['n_sale_unit']
    else:
        vmin, vmax, ticks = 8000, 28000, [10000, 15000, 20000, 25000]
        tf = lambda v: f'{int(v):,}'
        vf = lambda v: f'{int(v):,}'
        unit = t['n_rent_unit']
    wide = responsive_svg(G.track_svg(priced, vmin, vmax, ticks, 760, he, tf)).replace(' role="img" aria-hidden="true"', ' aria-hidden="true" focusable="false"')
    narrow = responsive_svg(G.track_svg(priced, vmin, vmax, ticks, 342, he, tf)).replace(' role="img" aria-hidden="true"', ' aria-hidden="true" focusable="false"')
    return {
        'label': t['sale'] if deal == 'sale' else t['rent'],
        'count': f"{len(ids)} {t['listings_word']}",
        'range': f'{vf(priced[0][1])}-{vf(priced[-1][1])}', 'unit': unit,
        'svg_wide': wide, 'svg_narrow': narrow,
        'chips': [{'id': i, 'value': vf(v)} for i, v in priced] + [{'id': i, 'value': None} for i in ask],
    }

def price_html(c, lang, t):
    he = lang == 'he'
    if c['price']:
        big = (f'<span class="nlb-num">{fint(c["price"])}</span>&nbsp;₪' if he else f'NIS&nbsp;<span class="nlb-num">{fint(c["price"])}</span>')
        month = f' <small>{t["month"]}</small>' if c['deal'] == 'rent' else ''
        per = ''
        if c.get('per_sqm'):
            unit = t['per_sqm_sale'] if c['deal'] == 'sale' else t['per_sqm_rent']
            per = (f'<span class="nlb-num">{fint(c["per_sqm"])}</span>&nbsp;₪ {unit}' if he else f'NIS&nbsp;<span class="nlb-num">{fint(c["per_sqm"])}</span> {unit}')
        return f'<strong><span>{big}</span>{month}</strong><span>{per}</span>'
    label = t['on_request_sale'] if c['deal'] == 'sale' else t['on_request_rent']
    return f'<strong class="nlb-ask">{label}</strong><span>{t["on_request_sub"]}</span>'

def build(lang, images, embed, review=True):
    he = lang == 'he'
    t = G.T[lang]
    cards = []
    for lid in ORDER:
        c = CARDS[lid]
        ed = B.load_ed(lid)
        url = B.URL_PATTERN[lang].format(slug=ed['seo'][lang]['slug'])
        wa_text = (f"שלום מיטל, אשמח לפרטים על {c['title']['he']} ({lid}) שראיתי ב-nad-lan" if he else f"Hello Meital, I would like details on {c['title']['en']} ({lid}), seen on nad-lan")
        cards.append({
            'id': lid, 'deal': c['deal'], 'url': url,
            'deal_label': t['sale'] if c['deal'] == 'sale' else t['rent'],
            'note': c['price_note'][lang] if c.get('price_note') else None,
            'kicker': f"{c['ptype'][lang]} · {c['area'][lang]}", 'title': c['title'][lang],
            'price': price_html(c, lang, t),
            'specs': [{'icon': icon(k), 'text': B.glue(B.wrapnums(html.escape(v[lang]))).replace('nlx-num', 'nlb-num')} for k, v in c['specs']],
            'hi': [B.glue(B.wrapnums(html.escape(x))).replace('nlx-num', 'nlb-num') for x in c['hi'][lang]],
            'amen': [{'icon': icon(a), 'text': G.AMEN[a][0 if he else 1]} for a in c['amen']],
            'entry': c['entry'][lang], 'updated': f"{t['updated']} {G.fdate(c['updated'], lang)}",
            'review': review and c['review'], 'img': img_src(images.get(lid), embed),
            'plate': plate(G.KIND[lid], 'dusk' if c['deal'] == 'sale' else 'day', seed=lid),
            'wa': WA + '?text=' + urllib.parse.quote(wa_text),
        })
    ctx = {
        'lang': lang, 'dir': t['dir'], 'he': he, 't': t,
        'hero_img': img_src(images.get('hero'), embed),
        'scene_wide': hero_scene(1440, 880, hz=700, sun_x=560, sky_x0=40, sky_x1=470, mirror=not he, seed='hero-d'),
        'scene_tall': hero_scene(390, 780, hz=660, sun_x=70, sky_x0=196, sky_x1=390, mirror=not he, seed='hero-m', sun_r=32, max_h=120),
        'feature_img': img_src(images.get('L01'), embed), 'estate': estate_night(),
        'ladders': [ladder('sale', lang), ladder('rent', lang)],
        'map': responsive_svg(G.coast_map(lang, 456)),
        'cards': cards, 'n_all': len(cards), 'n_sale': sum(1 for x in cards if x['deal'] == 'sale'), 'n_rent': sum(1 for x in cards if x['deal'] == 'rent'),
        'icon': icon, 'arrow': 'arrow_he' if he else 'arrow_en',
        'filter_label': 'סינון לפי סוג עסקה' if he else 'Filter by deal type',
        'ig_qr': responsive_svg(G.qr(IG, 120, G.ABYSS)), 'wa_qr': responsive_svg(G.qr(WA, 210, G.INK)),
        'card_scene': card_scene(mirror=not he, sun_x=250),
        'wa_general': WA + '?text=' + urllib.parse.quote('שלום מיטל, הגעתי מעמוד המתווכת שלך ב-nad-lan ואשמח לדבר' if he else 'Hello Meital, I found your broker page on nad-lan and would like to talk'),
        'tel': 'tel:' + PHONE_INTL, 'phone': G.PHONE[lang], 'ig': IG,
        'gallery': [{'src': img_src(p, embed), 'cap': cap} for p, cap in images.get('gallery', [])],
        'l01_url': B.URL_PATTERN[lang].format(slug=B.load_ed('L01')['seo'][lang]['slug']),
    }
    env = Environment(loader=FileSystemLoader(HERE), autoescape=False)
    out = env.get_template('broker.html.j2').render(**ctx)
    out = re.sub(r'\n\s*\n', '\n', out)
    B.assert_no_dash(out, f'broker-{lang}')
    return out

if __name__ == '__main__':
    imgs = json.load(open(HERE + '/images.json')) if os.path.exists(HERE + '/images.json') else {}
    for lang in ('he', 'en'):
        h = build(lang, imgs, embed=False)
        os.makedirs(BASE + 'dist/broker', exist_ok=True)
        open(BASE + f'dist/broker/broker-{lang}.html', 'w').write(h)
        print(lang, len(h))
