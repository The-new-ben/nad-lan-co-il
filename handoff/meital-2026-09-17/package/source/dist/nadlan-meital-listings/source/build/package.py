#!/usr/bin/env python3
"""Assemble the WordPress handoff package: blocks, payloads, SEO, schema, briefs, shot lists, catalog and data."""
import json, os, re, shutil, html, csv, io, sys, subprocess
import build as B

def _safe_copytree(src,dst,*a,**k):
    if not os.path.exists(src):
        print('skip missing', src); return
    return shutil.copytree(src,dst,*a,**k)

from nlxcalc import C, fint, assert_no_dash

PKG = B.BASE + 'dist/nadlan-meital-listings/'
IDS = ['L01', 'L07', 'L08', 'L05', 'L04', 'L06', 'L02', 'L03', 'L09', 'L10', 'L11']
REG = open(B.BASE + 'registry.md').read()
CONF_HE = {'verified': 'מאומת', 'likely': 'סביר', 'unverified': 'לא מאומת'}
PTYPE_EN = {'apartment': 'Apartment', 'penthouse': 'Mini penthouse', 'villa': 'Villa'}

def ig_posts(lid):
    m = re.search(r'### ' + lid + r' \|.*?\n(.*?)(?=\n### |\n## )', REG, re.S)
    out = []
    for code, date in re.findall(r'((?:p|reel)/[A-Za-z0-9_-]+) \((\d{4}-\d{2}-\d{2})', m.group(1)):
        out.append((date, 'https://www.instagram.com/' + code + '/'))
    return out

def strip_tokens(s):
    return re.sub(r'\[\[[^\]]+\]\]', '', s or '')

def wrap_block(h):
    return '<!-- wp:html -->\n' + h.strip() + '\n<!-- /wp:html -->\n'

def price_label(ed, lang):
    he = lang == 'he'
    if ed['deal'] == 'sale':
        if ed.get('price'):
            return (f"{fint(ed['price'])} ₪" if he else f"NIS {fint(ed['price'])}"), ''
        return ('מחיר לפי פנייה' if he else 'Price on request'), ''
    if ed.get('rent'):
        return (f"{fint(ed['rent'])} ₪" if he else f"NIS {fint(ed['rent'])}"), ('לחודש' if he else 'a month')
    return ('שכר דירה לפי פנייה' if he else 'Rent on request'), ''

def specs(ed, lang):
    he = lang == 'he'
    w = ed['wp']
    out = []
    if w.get('rooms'):
        r = w['rooms']; r = int(r) if float(r).is_integer() else r
        out.append(f"{r} חדרים" if he else f"{r} rooms")
    if w.get('size_sqm'):
        area = f"{w['size_sqm']} + {w['balcony_sqm']}" if w.get('balcony_sqm') else f"{w['size_sqm']}"
        out.append(f"{area} מ״ר" if he else f"{area} sqm")
    if w.get('plot_sqm'):
        out.append(f"מגרש {fint(w['plot_sqm'])} מ״ר" if he else f"{fint(w['plot_sqm'])} sqm plot")
    if w.get('floor') is not None and w.get('total_floors') and ed['ptype'] != 'villa':
        out.append(f"קומה {w['floor']} מתוך {w['total_floors']}" if he else f"Floor {w['floor']} of {w['total_floors']}")
    return out

def card(ed, lang):
    he = lang == 'he'
    e = lambda s: html.escape(s or '', quote=True)
    url = B.URL_PATTERN[lang].format(slug=ed['seo'][lang]['slug'])
    p, per = price_label(ed, lang)
    chips = [B.L_(c, lang) for c in ed.get('chips', []) if not c.get('sea')][:2]
    sp = ''.join(f'<li>{B.glue(B.wrapnums(e(x)))}</li>' for x in specs(ed, lang) + chips)
    per_html = f' <small>{e(per)}</small>' if per else ''
    foot_l = 'בלעדיות: מיטל קציר, נדל״ן על הים' if he else 'Exclusive: Meital Katzir'
    foot_r = 'לפרטים' if he else 'Details'
    return (f'<a class="nlx-card-l" href="{e(url)}" data-listing="{ed["id"]}">'
            f'<span class="nlx-card-kicker">{e(B.L_(ed["kicker"], lang))}</span>'
            f'<h3 class="nlx-card-title">{e(B.L_(ed["title"], lang))}</h3>'
            f'<div class="nlx-card-body"><span class="nlx-card-price">{B.glue(B.wrapnums(e(p)))}{per_html}</span><ul class="nlx-card-specs">{sp}</ul></div>'
            f'<span class="nlx-card-foot"><span>{e(foot_l)}</span><b>{e(foot_r)}</b></span></a>')

def catalog(eds, lang):
    he = lang == 'he'
    title = 'נכסים בבלעדיות של מיטל קציר, נדל״ן על הים' if he else 'Exclusive listings by Meital Katzir, Real Estate by the Sea'
    lead = ('אחוזה בהרצליה פיתוח ודירות בצפון תל אביב ובשרונה, עם מספרים, מקורות ובדיקות לכל נכס.' if he else
            'An estate in Herzliya Pituach and homes in north Tel Aviv and Sarona, each with numbers, sources and checks.')
    sales = [x for x in eds if x['deal'] == 'sale']
    rents = [x for x in eds if x['deal'] == 'rent']
    g = lambda lab, items: (f'<p class="nlx-cat-group">{html.escape(lab)}</p><div class="nlx-cat-grid">' + ''.join(card(x, lang) for x in items) + '</div>') if items else ''
    return (f'<section class="nlx nlx-cat" lang="{lang}" dir="{"rtl" if he else "ltr"}"><div class="nlx-wrap">'
            f'<div class="nlx-cat-head"><h2 class="nlx-cat-title">{html.escape(title)}</h2><p class="nlx-cat-lead">{html.escape(lead)}</p></div>'
            + g('למכירה' if he else 'For sale', sales) + g('להשכרה' if he else 'For rent', rents) + '</div></section>')

def meta_for(ed, lang):
    w = dict(ed['wp'])
    he = lang == 'he'
    m = {
        'listing_type': w['listing_type'], 'property_type': w['property_type'], 'price': w.get('price'),
        'price_per_sqm': (round(w['price'] / w['size_sqm']) if (w['listing_type'] == 'sale' and w.get('price') and w.get('size_sqm')) else None),
        'rooms': w.get('rooms'), 'floor': w.get('floor'), 'total_floors': w.get('total_floors'), 'size_sqm': w.get('size_sqm'),
        'balcony_sqm': w.get('balcony_sqm'), 'parking': w.get('parking'), 'elevator': w.get('elevator'), 'ac': w.get('ac'),
        'protected_room': w.get('protected_room'), 'storage': w.get('storage'), 'condition': w.get('condition'),
        'street': w.get('street') or '', 'building_number': '', 'lat': None, 'lng': None,
        'city': B.L_(ed['city'], lang), 'neighborhood': B.L_(ed['area'], lang),
        'arnona_monthly': w.get('arnona_monthly') or None, 'vaad_bayit_monthly': w.get('vaad_bayit_monthly') or None,
        'status': 'active', 'photos_csv': '',
    }
    return m

def seo_for(ed, lang, L):
    s = ed['seo'][lang]
    other = 'en' if lang == 'he' else 'he'
    return {
        'title': s['title'], 'title_chars': len(s['title']), 'metadesc': s['desc'], 'metadesc_chars': len(s['desc']),
        'focus_keyphrase': s['kw'], 'slug': s['slug'], 'slug_status': 'proposed, needs owner approval',
        'url': B.URL_PATTERN[lang].format(slug=s['slug']),
        'hreflang': {lang: B.URL_PATTERN[lang].format(slug=s['slug']), other: B.URL_PATTERN[other].format(slug=ed['seo'][other]['slug']), 'x-default': B.URL_PATTERN['he'].format(slug=ed['seo']['he']['slug'])},
        'og_title': B.L_(ed['title'], lang), 'og_description': s['desc'],
        'yoast_meta': {'_yoast_wpseo_title': s['title'], '_yoast_wpseo_metadesc': s['desc'], '_yoast_wpseo_focuskw': s['kw']},
    }

def shotlist(ed):
    rows = ['| # | קובץ | תיאור (alt בעברית) | Alt text (English) |', '|---|---|---|---|']
    for i, sh in enumerate(ed.get('shots', []), 1):
        stop = {'the', 'and', 'a', 'an', 'of', 'in', 'to', 'from', 'with', 'it', 'its', 'on', 'at', 'for'}
        words = [wd for wd in re.sub(r'[^a-z0-9]+', ' ', sh['en'].lower()).split() if wd not in stop]
        slug = ''
        for wd in words:
            if len(slug) + len(wd) + 1 > 32:
                break
            slug = (slug + '-' + wd).strip('-')
        rows.append(f"| {i} | `{ed['id']}-{i:02d}-{slug}.jpg` | {sh['he']} | {sh['en']} |")
    return (f"# רשימת צילומים, {ed['id']}\n\n"
            "תמונות מקור יתקבלו מהמשווקת. לא להשתמש בתמונות ממודעות של משרדים אחרים.\n\n"
            "מפרט: צד ארוך 2400 פיקסלים לפחות, יחס 3:2 לתמונה הראשית, ייצוא WebP באיכות 82 וגם JPG לגיבוי, בלי סימני מים, בלי טקסט על התמונה, "
            "בלי שיפור בבינה מלאכותית שמוסיף פריטים. שם הקובץ לפי הטבלה. התמונה הראשונה היא התמונה הראשית (featured image).\n\n"
            + '\n'.join(rows) + '\n')

def brief(ed, dos, Lhe):
    lid = ed['id']
    lines = [f"# תקציר פנימי, {lid}: {B.L_(ed['title'], 'he')}", '',
             'קובץ פנימי. אין להעלות אותו לאתר ואין להעביר אותו לצד שלישי.', '',
             '## סטטוס', '',
             f"- סוג עסקה: {'מכירה' if ed['deal'] == 'sale' else 'השכרה'}",
             f"- פרסום אחרון באינסטגרם: {ed['last_post']}",
             f"- סטטוס בחבילה: {'לאישור זמינות לפני העלאה' if ed.get('status') == 'confirm' else 'פעיל לפי האינסטגרם'}",
             f"- מקורות בעמוד: {len(Lhe['sources'])}",
             f"- כתובות מוצעות (לאישור הבעלים): `{ed['seo']['he']['slug']}` ו-`{ed['seo']['en']['slug']}`", '',
             '## פוסטים באינסטגרם', '']
    for d, u in ig_posts(lid):
        lines.append(f"- {d}: {u}")
    lines += ['', '## הערכה', '']
    lines += [f"- {x}" for x in ed['internal']['assessment']]
    lines += ['', '## לאשר מול מיטל לפני העלאה', '']
    lines += [f"- [ ] {x}" for x in ed['internal']['confirm']]
    cross = dos.get('cross_listings', [])
    if cross:
        lines += ['', '## הצלבות עם מודעות אחרות (לא לפרסום)', '']
        for c in cross:
            price = f"{fint(c['price_nis'])} ₪" if c.get('price_nis') else 'ללא מחיר'
            lines.append(f"- {c.get('date')}, {price}, רמת ביטחון: {CONF_HE.get(c.get('confidence'), c.get('confidence'))}. {c.get('url')}")
            lines.append(f"  - תיאור המקור (באנגלית): {c.get('what_en')}")
    lines += ['', '## סיכונים שזוהו במחקר', '']
    lines += [f"- {r['he']}" for r in dos.get('risks', [])]
    lines += ['', '## פערי מידע', '']
    lines += [f"- {g['he']}" for g in dos.get('gaps', [])]
    lines += ['', '## שדות וורדפרס', '', '```json', json.dumps(ed['wp'], ensure_ascii=False, indent=1), '```', '']
    return '\n'.join(lines)

BROKER_SEO = {
    'he': {'title': 'מיטל קציר, נדל״ן על הים | נכסי יוקרה בצפון תל אביב',
           'desc': '11 נכסים בבלעדיות של המתווכת מיטל קציר: אחוזה בהרצליה פיתוח, מיני פנטהאוזים ודירות בצוקי אביב, בנופי ים ובשרונה, עם כל הפרטים וקשר ישיר.',
           'kw': 'מיטל קציר נדל״ן', 'slug': 'meital-katzir', 'parent_slug': 'brokers', 'url': 'https://nad-lan.co.il/brokers/meital-katzir/'},
    'en': {'title': 'Meital Katzir, Real Estate by the Sea | Tel Aviv Homes',
           'desc': '11 exclusive listings from broker Meital Katzir: a Herzliya Pituach estate, mini penthouses and apartments in Tzukei Aviv, Nofei Yam and Sarona.',
           'kw': 'Meital Katzir real estate', 'slug': 'meital-katzir', 'parent_slug': 'brokers', 'url': 'https://nad-lan.co.il/en/brokers/meital-katzir/'},
}

def broker_schema(lang, eds):
    he = lang == 'he'
    seo = BROKER_SEO[lang]
    return {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'RealEstateAgent', '@id': seo['url'] + '#agent',
             'name': 'מיטל קציר, נדל״ן על הים' if he else 'Meital Katzir, Real Estate by the Sea',
             'url': seo['url'], 'telephone': '+972-52-363-1582',
             'areaServed': [{'@type': 'Place', 'name': n} for n in (['צפון תל אביב', 'שרונה', 'הרצליה פיתוח'] if he else ['North Tel Aviv', 'Sarona', 'Herzliya Pituach'])],
             'sameAs': ['https://www.instagram.com/meitalkatzir_realestate/'],
             'identifier': {'@type': 'PropertyValue', 'name': 'רישיון תיווך' if he else 'Brokerage license', 'value': '3131540'}},
            {'@type': 'ItemList', 'name': 'נכסים בבלעדיות' if he else 'Exclusive listings', 'numberOfItems': len(eds),
             'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': B.URL_PATTERN[lang].format(slug=ed['seo'][lang]['slug']), 'name': B.L_(ed['title'], lang)} for i, ed in enumerate(eds)]},
        ],
    }

def broker_bundle(eds):
    import subprocess, glob
    d = PKG + 'broker/'
    os.makedirs(d + 'claude-design-canvas', exist_ok=True)
    subprocess.run([sys.executable, B.B + 'broker/build_broker.py'], check=True, capture_output=True)
    for lang in ('he', 'en'):
        h = open(B.BASE + f'dist/broker/broker-{lang}.html').read()
        open(d + f'broker-{lang}.html', 'w').write(h)
        open(d + f'content-broker-{lang}.html', 'w').write(wrap_block(h))
        seo = BROKER_SEO[lang]
        json.dump({'_about': 'WordPress REST payload for POST /wp-json/wp/v2/pages. Status stays draft. Parent page slug and final slug need owner approval (HANDOFF section 12).',
                   'status': 'draft', 'title': 'מיטל קציר, נדל״ן על הים' if lang == 'he' else 'Meital Katzir, Real Estate by the Sea',
                   'slug': seo['slug'], 'parent_slug': seo['parent_slug'], 'content_file': f'content-broker-{lang}.html', 'excerpt': seo['desc'],
                   'template_hint': 'full-width page template without a sidebar or page title', 'language': lang, 'translation_group': 'broker-meital-katzir',
                   'yoast_meta': {'_yoast_wpseo_title': seo['title'], '_yoast_wpseo_metadesc': seo['desc'], '_yoast_wpseo_focuskw': seo['kw']}},
                  open(d + f'wp-page-{lang}.json', 'w'), ensure_ascii=False, indent=1)
        json.dump(broker_schema(lang, eds), open(d + f'schema-broker-{lang}.jsonld', 'w'), ensure_ascii=False, indent=1)
    json.dump({k: dict(v, title_chars=len(v['title']), desc_chars=len(v['desc']), slug_status='proposed, needs owner approval') for k, v in BROKER_SEO.items()},
              open(d + 'seo-broker.json', 'w'), ensure_ascii=False, indent=1)
    for f in ('nlb-broker.css', 'cards.json', 'CLAUDE-DESIGN-BRIEF.md', 'AI-IMAGE-PROMPTS-HE.md'):
        shutil.copy(B.B + 'broker/' + f, d + f)
    _safe_copytree(B.BASE + 'canvas/project', d + 'claude-design-canvas/project', dirs_exist_ok=True)
    if os.path.isdir(B.BASE + 'minisite/project'):
        _safe_copytree(B.BASE + 'minisite/project', d + 'claude-design-minisite/project', dirs_exist_ok=True)
        open(d + 'claude-design-minisite/README.md', 'w').write(
            '# Claude Design canvas: broker minisite (clickable prototype)\n\n'
            'Live canvas (private until shared): https://claude.ai/artifact/PpECyYJdA4j8LiuZuAjZ9g\n\n'
            'Pages: Main (home with search), Listings (working filters by deal, area and rooms), Property (L07: gallery, buyer-type purchase tax and financing, viewing form), '
            'About (profile, testimonial placeholders, contact form), HomeMobile and PropertyMobile, and ForBrokers (nad-lan page offering the minisite, with a sign-up form).\n\n'
            'Built on Meital Katzir\'s real listing data. Illustrations and labeled photo slots stand in for her photos; testimonials and the profile photo are placeholders to collect. '
            'Pricing for the broker offer is not set and does not appear.\n')
    open(d + 'claude-design-canvas/README.md', 'w').write(
        '# Claude Design canvas: Meital Katzir broker profile\n\n'
        'Live canvas (private until shared): https://claude.ai/artifact/JPqo3LJotmA7yNNuxMuUQr\n\n'
        'Artboards: Main (Hebrew desktop, working deal filter), Mobile (full page), MobileFirst (first screen with the sticky bar), '
        'English (desktop, working deal filter), ListingCard (three states), ShareImage (1080x1350), BusinessCardFront and BusinessCardBack (1050x600).\n\n'
        'These files are the canvas source (Design Components format, one .dc.html per artboard plus canvas.json). '
        'The WordPress page in ../broker-he.html and ../broker-en.html implements the same design responsively.\n\n'
        'Illustrations stand in for photos until Meital\'s own images arrive; they depict no real property.\n')
    os.makedirs(d + 'screenshots', exist_ok=True)
    from PIL import Image
    shots = B.BASE + 'shots/'
    crops = [('wp-he-1440.png', (0, 0, 1440, 1000), 'desktop-he-hero.jpg'), ('wp-he-1440.png', (0, 2600, 1440, 3700), 'desktop-he-cards.jpg'),
             ('wp-en-1440.png', (0, 0, 1440, 1000), 'desktop-en-hero.jpg'), ('m_first.png', None, 'mobile-he-first-screen.jpg'), ('m_cards.png', None, 'mobile-he-card.jpg')]
    for src, box, out in crops:
        if os.path.exists(shots + src):
            im = Image.open(shots + src).convert('RGB')
            if box:
                im = im.crop(box)
            im.save(d + 'screenshots/' + out, quality=84)
    m = PKG + 'media/'
    os.makedirs(m, exist_ok=True)
    for f in ('INSTAGRAM-MEDIA-MANIFEST-HE.md', 'instagram-media-manifest.csv'):
        shutil.copy(B.BASE + 'media/' + f, m + f)
    src = PKG + 'source/build/'
    _safe_copytree(B.B + 'broker', src + 'broker', dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', 'v1'))
    _safe_copytree(B.B + 'design', src + 'design', dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))

def main():
    if os.path.exists(PKG):
        shutil.rmtree(PKG)
    os.makedirs(PKG + 'assets')
    shutil.copy(B.B + 'assets/nlx-prestige.css', PKG + 'assets/nlx-prestige.css')
    res = B.render_all(IDS)
    eds, index = [], []
    for lid in IDS:
        ed = B.load_ed(lid)
        dos = json.load(open(B.BASE + f'dossiers/{lid}.json'))
        eds.append(ed)
        d = PKG + f'listings/{lid}/'
        os.makedirs(d)
        for lang in ('he', 'en'):
            h, L, _ = res[(lid, lang)]
            open(d + f'block-{lang}.html', 'w').write(h)
            open(d + f'content-{lang}.html', 'w').write(wrap_block(h))
            seo = seo_for(ed, lang, L)
            payload = {
                '_about': 'WordPress REST payload for POST /wp-json/wp/v2/nadlan_property. Status stays draft. Verify meta keys and term names first (see HANDOFF).',
                'status': 'draft', 'title': B.L_(ed['title'], lang), 'slug': seo['slug'], 'content_file': f'content-{lang}.html',
                'excerpt': seo['metadesc'], 'meta': meta_for(ed, lang), 'terms': {'nadlan_city': [B.L_(ed['city'], lang)]},
                'yoast_meta': seo['yoast_meta'], 'language': lang, 'translation_group': lid,
            }
            json.dump(payload, open(d + f'wp-{lang}.json', 'w'), ensure_ascii=False, indent=1)
            json.dump(json.loads(L['jsonld']), open(d + f'schema-{lang}.jsonld', 'w'), ensure_ascii=False, indent=1)
            if lang == 'he':
                seo_all = {'he': seo}
                Lhe = L
            else:
                seo_all['en'] = seo
        json.dump(seo_all, open(d + 'seo.json', 'w'), ensure_ascii=False, indent=1)
        open(d + 'shotlist.md', 'w').write(shotlist(ed))
        open(d + 'brief-he.md', 'w').write(brief(ed, dos, Lhe))
        index.append({
            'id': lid, 'deal': ed['deal'], 'status': ed.get('status', 'active'), 'last_instagram_post': ed['last_post'],
            'title': {'he': B.L_(ed['title'], 'he'), 'en': B.L_(ed['title'], 'en')},
            'city': ed['city'], 'area': ed['area'],
            'price_nis': ed.get('price'), 'rent_nis_month': ed.get('rent'), 'rent_band_nis': ed.get('rent_band'),
            'rooms': ed['wp'].get('rooms'), 'size_sqm': ed['wp'].get('size_sqm'), 'balcony_sqm': ed['wp'].get('balcony_sqm'),
            'slug': {'he': ed['seo']['he']['slug'], 'en': ed['seo']['en']['slug']},
            'files': {k: f'listings/{lid}/{k}' for k in ['block-he.html', 'block-en.html', 'content-he.html', 'content-en.html', 'wp-he.json', 'wp-en.json', 'schema-he.jsonld', 'schema-en.jsonld', 'seo.json', 'shotlist.md', 'brief-he.md']},
            'sources_on_page': len(res[(lid, 'he')][1]['sources']),
            'photos_needed': len(ed.get('shots', [])),
        })
    os.makedirs(PKG + 'catalog')
    for lang in ('he', 'en'):
        c = catalog(eds, lang)
        open(PKG + f'catalog/catalog-{lang}.html', 'w').write(c)
        open(PKG + f'catalog/content-catalog-{lang}.html', 'w').write(wrap_block(c))
    os.makedirs(PKG + 'data')
    json.dump({'generated': C['as_of'], 'broker': {'name_he': 'מיטל קציר', 'brand_he': 'נדל״ן על הים', 'license': '3131540', 'phone': '052-3631582'},
               'url_pattern': B.URL_PATTERN, 'listings': index}, open(PKG + 'data/listings.json', 'w'), ensure_ascii=False, indent=1)
    # slug approval sheet
    out = io.StringIO()
    wcsv = csv.writer(out)
    wcsv.writerow(['id', 'lang', 'title', 'proposed_slug', 'proposed_url', 'approved (yes/no)', 'final_slug'])
    for ed in eds:
        for lang in ('he', 'en'):
            wcsv.writerow([ed['id'], lang, B.L_(ed['title'], lang), ed['seo'][lang]['slug'], B.URL_PATTERN[lang].format(slug=ed['seo'][lang]['slug']), '', ''])
    open(PKG + 'data/slugs-for-approval.csv', 'w', encoding='utf-8-sig').write(out.getvalue())
    # pre-publish tracking sheet
    out = io.StringIO()
    wcsv = csv.writer(out)
    wcsv.writerow(['id', 'lang', 'meital_text_approved', 'confirm_list_answered', 'availability_and_price_rechecked_date', 'photos_uploaded', 'slug_approved', 'visual_qa_390_768_1280', 'schema_validated', 'verify_script_passed', 'cta_links_checked', 'published_date'])
    for ed in eds:
        for lang in ('he', 'en'):
            wcsv.writerow([ed['id'], lang] + [''] * 10)
    open(PKG + 'data/pre-publish-checklist.csv', 'w', encoding='utf-8-sig').write(out.getvalue())
    # docs, scripts and the generator source
    for f in ('README-HE.md', 'HANDOFF-claude-code.md'):
        shutil.copy(B.B + 'docs/' + f, PKG + f)
    _safe_copytree(B.B + 'scripts', PKG + 'scripts')
    src = PKG + 'source/'
    os.makedirs(src + 'build')
    for f in ('build.py', 'nlxcalc.py', 'package.py', 'preview.py', 'peek.py', 'constants.json'):
        shutil.copy(B.B + f, src + 'build/' + f)
    for d in ('templates', 'assets', 'editorial', 'scripts', 'docs'):
        _safe_copytree(B.B + d, src + 'build/' + d)
    _safe_copytree(B.BASE + 'dossiers', src + 'dossiers')
    os.makedirs(src + 'research')
    for d in (B.BASE, B.BASE + 'research/'):
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.startswith('research_') and f.endswith('.md'):
                    shutil.copy(d + f, src + 'research/' + f)
    for f in ('registry.md', 'dossier_schema.md'):
        shutil.copy(B.BASE + f, src + f)
    broker_bundle(eds)
    return res, eds

if __name__ == '__main__':
    res, eds = main()
    n = 0
    for root, _, files in os.walk(PKG):
        for f in files:
            n += 1
    print('files', n)
