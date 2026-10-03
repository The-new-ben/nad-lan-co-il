# -*- coding: utf-8 -*-
"""The cy-prus "Advertise with us" page (/advertise/, English at ?lang=en), rendered to static HTML at build time.
Copy: cyprus-private/advertise-20261003/recommendation.md (portal research, 3.10.2026). Owner rule: the site maps and
presents; no prices, fees, commission, packages, paid prominence or traffic numbers, and the only contact is WhatsApp."""
from html import escape
from urllib.parse import quote

WA = '972525101555'
SITE = 'https://cy-prus.co.il'

COPY = {
 'he': {
  'title': 'הפרויקט או העסק שלכם, על המפה של קפריסין',
  'seo_title': 'פרסמו אצלנו: פרויקטים ועסקים בלימסול, פאפוס ולרנקה | CY-PRUS',
  'seo_desc': 'יזמים, משווקים ועסקים מקומיים בקפריסין: הציגו את הפרויקט או העסק שלכם על המפה של CY-PRUS, בעברית ובאנגלית, יחד עם השכונה וכל מה שסביבה. דברו איתנו בוואטסאפ.',
  'lead': 'CY-PRUS ממפה את לימסול, פאפוס ולרנקה בעברית ובאנגלית: פרויקטים חדשים, שכונות, רחובות, חופים, בתי ספר ושירותים, הכול על מפה אחת. יזמים, משווקים ועסקים מקומיים מוזמנים להופיע בה בעמוד משלהם, שמראה מה אתם מציעים, איפה בדיוק אתם נמצאים ומה יש סביבכם.',
  'cta': 'דברו איתנו בוואטסאפ', 'map_link': 'ראו פרויקטים על המפה', 'reply': 'מענה בעברית',
  'who_h': 'למי זה מתאים',
  'who': [('יזמים', 'בונים בקפריסין? כל פרויקט מקבל עמוד משלו ונקודה על המפה, עם השלב, הנתונים והתוכניות שתמסרו לנו, ועם השכונה כולה מסביב.', 'ליזמים: דברו איתנו', 'dev'),
          ('משווקים ומשרדי תיווך', 'משווקים פרויקטים או מלווים קונים מישראל? הציגו את הפרויקטים שאתם מייצגים, בעברית ובאנגלית, ליד כל מה שקונה רוצה לדעת על האזור.', 'למשווקים: דברו איתנו', 'agency'),
          ('עסקים מקומיים', 'עורכי דין, רואי חשבון, ביטוח, בנקים, ניהול נכסים ושירותים לתושבים חדשים. מי שעובר לקפריסין צריך אנשי מקצוע שאפשר לסמוך עליהם. הציגו את העסק שלכם עם כתובת, פרטי התקשרות ומיקום על המפה.', 'לעסקים: דברו איתנו', 'business')],
  'page_h': 'מה כולל עמוד פרויקט ב-CY-PRUS',
  'page': ['נקודה על המפה האינטראקטיבית, במחוז ובשכונה של הפרויקט', 'תיאור ברור בעברית ובאנגלית',
           'הנתונים שחשובים לקונה: שלב הפרויקט, ייעוד, קומות, גובה ומועד מסירה כשהוא ידוע', 'התוכניות, ההדמיות והתמונות שתמסרו לנו',
           '"בסביבה": חופים, בתי ספר, סופרמרקטים, מרפאות ושירותים ליד הפרויקט', 'כפתור וואטסאפ עם מענה בעברית',
           'קישורים למדריכים שקונים מישראל קוראים: מס רכישה, בדיקת רישום הבעלות ובחירת עורך דין', 'בקרוב: הצגת הפרויקט בתלת־ממד'],
  'why_h': 'למה CY-PRUS',
  'why': [('נבנה עבור ישראלים', 'התוכן, המדריכים והמענה בעברית, ולצידם גרסה באנגלית. קונה מישראל פוגש את הפרויקט שלכם בשפה שלו.'),
          ('השכונה היא חלק מההחלטה', 'קונים לא בוחרים רק דירה, הם בוחרים שכונה. אצלנו הפרויקט מוצג יחד עם הרחובות, החופים, בתי הספר והשירותים שסביבו, כך שקל להבין למה דווקא שם.'),
          ('מידע שאפשר לסמוך עליו', 'אנחנו מציגים את מה שאפשר לבסס: הנתונים שתמסרו, מקורות פומביים ומיקום מדויק כשהוא ידוע. כך מי שמגיע לפרויקט שלכם מגיע עם אמון.'),
          ('שלוש ערים, מפה אחת', 'לימסול, פאפוס ולרנקה במקום אחד. מי שמשווה בין אזורים רואה את הפרויקט שלכם בהקשר הנכון.')],
  'how_h': 'איך זה עובד',
  'how': [('כותבים לנו בוואטסאפ', 'ספרו בכמה מילים מי אתם ומה תרצו להציג.'),
          ('שולחים את החומרים', 'פרטי הפרויקט או העסק, מיקום, תוכניות, הדמיות וקובץ מכירה. מה שיש לכם.'),
          ('העמוד שלכם על המפה', 'נכין את העמוד בעברית ובאנגלית, ונעדכן אותו בכל פעם שתשלחו לנו פרטים חדשים.')],
  'prep_h': 'מה כדאי להכין',
  'prep': ['שם הפרויקט או העסק, והחברה שעומדת מאחוריו', 'כתובת או מיקום המגרש', 'שלב הפרויקט ומועד מסירה משוער', 'סוגי היחידות והגדלים',
           'תוכניות, הדמיות ותמונות שמותר לפרסם', 'קובץ מכירה או מצגת, אם יש', 'איש קשר לעדכונים'],
  'onmap_h': 'כבר על המפה', 'onmap_p': 'ראו איך פרויקטים מוצגים היום:',
  'onmap': [('פרויקטים בלימסול', '/limassol/residential_project/'), ('פרויקטים בפאפוס', '/paphos/residential_project/'), ('חיפוש על המפה', '/browse/')],
  'faq_h': 'שאלות ותשובות',
  'faq': [('מה אפשר להציג ב-CY-PRUS?', 'פרויקטים חדשים למגורים, פרויקטים מסחריים ותיירותיים, ועסקים שנותנים שירות בלימסול, בפאפוס ובלרנקה.'),
          ('הפרויקט שלנו כבר מופיע באתר. מה עושים?', 'חלק מהפרויקטים מוצגים לפי מידע פומבי. אם אתם היזמים או המשווקים, כתבו לנו ונשלים את הפרטים, התוכניות והמיקום המדויק.'),
          ('באילו שפות העמוד מוצג?', 'בעברית ובאנגלית.'),
          ('צריך לפתוח חשבון או למלא טופס?', 'לא. הכול מתחיל בהודעת וואטסאפ אחת.'),
          ('אפשר לעדכן פרטים בהמשך?', 'כן. שלב חדש, מועד מסירה, תוכניות או תמונות: שלחו לנו בוואטסאפ ונעדכן.'),
          ('אתם בודקים את המידע?', 'כן. אנחנו מציגים פרטים שנמסרו לנו או שמופיעים במקורות פומביים, ומה שאי אפשר לבסס נשאר בחוץ.')],
  'end_h': 'רוצים להופיע על המפה?', 'end_p': 'כתבו לנו בוואטסאפ, ונחזור אליכם בעברית.',
  'wa': {'general': ['שלום, הגעתי מהעמוד "פרסמו אצלנו" באתר CY-PRUS.', 'אשמח להציג באתר פרויקט או עסק.', 'שם הפרויקט או העסק:', 'עיר ואזור:'],
         'dev': ['שלום, הגעתי מהעמוד "פרסמו אצלנו" באתר CY-PRUS.', 'פונה מטעם יזם, ואשמח להציג פרויקט באתר.', 'שם הפרויקט:', 'עיר ואזור:', 'שלב הפרויקט:'],
         'agency': ['שלום, הגעתי מהעמוד "פרסמו אצלנו" באתר CY-PRUS.', 'פונה מטעם משרד שיווק או תיווך, ואשמח להציג פרויקטים שאנחנו מייצגים.', 'שם המשרד:', 'עיר ואזור:'],
         'business': ['שלום, הגעתי מהעמוד "פרסמו אצלנו" באתר CY-PRUS.', 'פונה מטעם עסק מקומי, ואשמח להציג אותו באתר.', 'שם העסק ותחום:', 'עיר ואזור:']},
  'url': SITE + '/advertise/',
 },
 'en': {
  'title': 'Your project or business, on the map of Cyprus',
  'seo_title': 'Advertise with us: projects and businesses in Cyprus | CY-PRUS',
  'seo_desc': 'Developers, agents and local businesses in Limassol, Paphos and Larnaca: present your project or business on the CY-PRUS map, in Hebrew and English, together with its neighbourhood. Talk to us on WhatsApp.',
  'lead': 'CY-PRUS maps Limassol, Paphos and Larnaca in Hebrew and English: new projects, neighbourhoods, streets, beaches, schools and services, all on one map. Developers, agents and local businesses are welcome to join it with a page of their own, one that shows what you offer, exactly where you are and what is around you.',
  'cta': 'Talk to us on WhatsApp', 'map_link': 'See projects on the map', 'reply': 'WhatsApp',
  'who_h': "Who it's for",
  'who': [('Developers', 'Building in Cyprus? Every project gets its own page and its own point on the map, with the stage, the key facts and the plans you share with us, and the whole neighbourhood around it.', 'Developers: talk to us', 'dev'),
          ('Marketing and estate agencies', 'Marketing projects, or guiding buyers from Israel? Present the projects you represent, in Hebrew and English, right next to everything a buyer wants to know about the area.', 'Agencies: talk to us', 'agency'),
          ('Local businesses', 'Lawyers, accountants, insurers, banks, property managers and services for newcomers. People moving to Cyprus need professionals they can trust. Present your business with its address, contact details and location on the map.', 'Businesses: talk to us', 'business')],
  'page_h': 'What a project page on CY-PRUS includes',
  'page': ["A point on the interactive map, in the project's own district and neighbourhood", 'A clear description in Hebrew and English',
           'The facts buyers look for: project stage, use, floors, height and completion date when known', 'The plans, renderings and photos you share with us',
           '"Nearby": beaches, schools, supermarkets, clinics and services around the project', 'A WhatsApp button with replies in Hebrew',
           'Links to the guides Israeli buyers read: purchase tax, title deed checks and choosing a lawyer', 'Coming soon: your project in 3D'],
  'why_h': 'Why CY-PRUS',
  'why': [('Built for Israeli buyers', 'Content, guides and replies in Hebrew, with an English version alongside. Buyers from Israel meet your project in their own language.'),
          ('The neighbourhood is part of the decision', "People don't just choose a flat, they choose a neighbourhood. Here your project sits among the streets, beaches, schools and services around it, so it is easy to see why it is where it is."),
          ('Information people can trust', 'We present what can be supported: the facts you give us, public sources, and the exact location when it is known. Buyers who reach your project arrive with confidence.'),
          ('Three cities, one map', 'Limassol, Paphos and Larnaca in one place. Anyone comparing areas sees your project in the right context.')],
  'how_h': 'How it works',
  'how': [('Message us on WhatsApp', 'Tell us in a few words who you are and what you would like to present.'),
          ('Send your materials', 'Project or business details, location, plans, renderings and a brochure. Whatever you have.'),
          ('Your page goes on the map', 'We prepare the page in Hebrew and English, and update it whenever you send us something new.')],
  'prep_h': 'What to prepare',
  'prep': ['The project or business name, and the company behind it', 'Address or plot location', 'Project stage and expected completion date', 'Unit types and sizes',
           'Plans, renderings and photos you are allowed to publish', 'A brochure or presentation, if you have one', 'A contact person for updates'],
  'onmap_h': 'Already on the map', 'onmap_p': 'See how projects are presented today:',
  'onmap': [('Projects in Limassol', '/limassol/residential_project/?lang=en'), ('Projects in Paphos', '/paphos/residential_project/?lang=en'), ('Search the map', '/browse/?lang=en')],
  'faq_h': 'Questions and answers',
  'faq': [('What can be presented on CY-PRUS?', 'New residential projects, commercial and tourism projects, and businesses serving Limassol, Paphos and Larnaca.'),
          ('Our project is already on the site. What now?', 'Some projects are presented from public information. If you are the developer or the marketing agency, message us and we will complete the details, the plans and the exact location.'),
          ('Which languages is the page shown in?', 'Hebrew and English.'),
          ('Do I need an account or a form?', 'No. It all starts with one WhatsApp message.'),
          ('Can we update the details later?', 'Yes. A new stage, a completion date, new plans or photos: send them on WhatsApp and we will update the page.'),
          ('Do you check the information?', 'Yes. We present details you give us or that appear in public sources, and anything we cannot support stays out.')],
  'end_h': 'Want to be on the map?', 'end_p': 'Message us on WhatsApp and we will get back to you.',
  'wa': {'general': ['Hello, I came from the "Advertise with us" page on CY-PRUS.', 'I would like to present a project or a business on the site.', 'Project or business name:', 'City and area:'],
         'dev': ['Hello, I came from the "Advertise with us" page on CY-PRUS.', 'I am writing on behalf of a developer and would like to present a project on the site.', 'Project name:', 'City and area:', 'Project stage:'],
         'agency': ['Hello, I came from the "Advertise with us" page on CY-PRUS.', 'I am writing on behalf of a marketing or estate agency and would like to present the projects we represent.', 'Agency name:', 'City and area:'],
         'business': ['Hello, I came from the "Advertise with us" page on CY-PRUS.', 'I am writing on behalf of a local business and would like to present it on the site.', 'Business name and field:', 'City and area:']},
  'url': SITE + '/advertise/?lang=en',
 },
}

# Owner guardrail: words that must never appear on the advertiser page ("plans" as drawings is allowed).
BANNED = {'he': ['מחיר', 'עלות', 'תשלום', 'עמלה', 'חבילה', 'חינם', 'קידום', 'מודגש', 'ממומן', 'לידים', 'חשיפה מובטחת', 'אטלס'],
          'en': ['price', 'fee', 'cost', 'free', 'commission', 'package', 'featured', 'premium', 'sponsored', 'boost', 'leads', 'traffic', 'visitors', 'atlas']}

CHECK = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>'
WA_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 2.9 2.9 0 0 0-.9 2.2 5 5 0 0 0 1.1 2.7 11.4 11.4 0 0 0 4.4 3.9c1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>')


def wa_href(lang, kind):
    c = COPY[lang]
    return 'https://wa.me/' + WA + '?text=' + quote('\n'.join(c['wa'][kind] + [c['url']]), safe='')


def render(lang):
    c, e = COPY[lang], escape
    d = 'rtl' if lang == 'he' else 'ltr'
    q = '' if lang == 'he' else '?lang=en'
    btn = lambda kind, label, cls='cyad-btn': f'<a class="{cls}" href="{e(wa_href(lang, kind))}" target="_blank" rel="noopener">{WA_ICON}<span>{e(label)}</span></a>'
    h = [f'<div class="cyad alignwide" lang="{lang}" dir="{d}">']
    h.append(f'<section class="cyad-lead"><p class="cyad-lede">{e(c["lead"])}</p><div class="cyad-ctas">{btn("general", c["cta"])}'
             f'<a class="cyad-link" href="/browse/{q}">{e(c["map_link"])}</a></div>'
             f'<p class="cyad-reply">{e(c["reply"])} · <bdi dir="ltr">052-510-1555</bdi></p></section>')
    h.append(f'<section class="cyad-sec"><h2>{e(c["who_h"])}</h2><div class="cyad-who">' + ''.join(
        f'<article class="cyad-card"><h3>{e(t)}</h3><p>{e(p)}</p>{btn(k, b, "cyad-btn cyad-btn--line")}</article>' for t, p, b, k in c['who']) + '</div></section>')
    h.append(f'<section class="cyad-sec cyad-sec--soft"><h2>{e(c["page_h"])}</h2><ul class="cyad-checks">' + ''.join(
        f'<li>{CHECK}<span>{e(x)}</span></li>' for x in c['page']) + '</ul></section>')
    h.append(f'<section class="cyad-sec"><h2>{e(c["why_h"])}</h2><div class="cyad-why">' + ''.join(
        f'<div><h3>{e(t)}</h3><p>{e(p)}</p></div>' for t, p in c['why']) + '</div></section>')
    h.append(f'<section class="cyad-sec"><h2>{e(c["how_h"])}</h2><ol class="cyad-steps">' + ''.join(
        f'<li><span class="cyad-num">{i}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(c['how'], 1)) + '</ol></section>')
    h.append(f'<section class="cyad-sec cyad-sec--soft"><h2>{e(c["prep_h"])}</h2><ul class="cyad-checks cyad-checks--plain">' + ''.join(
        f'<li>{CHECK}<span>{e(x)}</span></li>' for x in c['prep']) + '</ul></section>')
    h.append(f'<section class="cyad-sec"><h2>{e(c["onmap_h"])}</h2><p>{e(c["onmap_p"])}</p><p class="cyad-onmap">' + ''.join(
        f'<a href="{e(u)}">{e(t)}</a>' for t, u in c['onmap']) + '</p></section>')
    h.append(f'<section class="cyad-sec"><h2>{e(c["faq_h"])}</h2><div class="cyad-faq">' + ''.join(
        f'<details><summary>{e(qq)}</summary><p>{e(a)}</p></details>' for qq, a in c['faq']) + '</div></section>')
    h.append(f'<section class="cyad-end"><h2>{e(c["end_h"])}</h2><p>{e(c["end_p"])}</p>{btn("general", c["cta"])}</section>')
    h.append('</div>')
    out = ''.join(h)
    re_ = __import__('re')
    visible = re_.sub(r'<[^>]+>|https?://\S+', ' ', out).lower()
    tokens = set(re_.findall(r'[֐-׿a-z]+', visible))
    prefixes = ('', 'ה', 'ו', 'ב', 'ל', 'מ', 'ש', 'כ', 'וה', 'שה', 'וב', 'ול', 'מה')
    allowed = {'בעלות', 'הבעלות'}  # "ownership", not "cost"
    for w in BANNED[lang]:
        parts = w.split()
        if len(parts) > 1:
            hit = w in visible
        else:
            hit = any((p + w) in tokens and (p + w) not in allowed for p in prefixes) if lang == 'he' else w in tokens
        if hit:
            raise SystemExit(f'advertise page ({lang}): banned word "{w}"')
    return out


CSS = """
.cyad{--n:var(--cy-navy,#12293E);--t:var(--cy-teal,#178076);--tl:var(--cy-teal-light,#2FA79A);--c:var(--cy-cream,#F4EFE6);--s:var(--cy-surface,#FBF8F2);--l:var(--cy-line,#E3DCCE);--m:var(--cy-muted,#5A6B76);--i:var(--cy-ink,#1B2833);color:var(--i);font-family:var(--cy-font-body,"Assistant"),Arial,sans-serif;margin-block:8px 48px}
.cyad *{box-sizing:border-box}
.cyad h2{font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif;color:var(--n);font-size:clamp(24px,3vw,32px);line-height:1.25;margin:0 0 18px;font-weight:700}
.cyad h3{font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif;color:var(--n);font-size:20px;line-height:1.3;margin:0 0 8px;font-weight:700}
.cyad p{margin:0 0 12px;line-height:1.75;font-size:16.5px}
.cyad-lead{max-width:760px;padding-block:4px 30px}
.cyad .cyad-lede{font-size:clamp(17px,2vw,19.5px);line-height:1.8;color:var(--i);margin-bottom:22px}
.cyad-ctas{display:flex;flex-wrap:wrap;align-items:center;gap:12px 22px}
body .cyad a.cyad-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:50px;padding:0 22px;border-radius:6px;background:var(--t);color:#fff;text-decoration:none;font-weight:700;font-size:16px;border:1px solid var(--t)}
body .cyad a.cyad-btn:hover{background:#12685F;color:#fff}
body .cyad a.cyad-btn--line{background:transparent;color:var(--n);border-color:var(--n);min-height:46px;font-size:15px}
body .cyad a.cyad-btn--line:hover{background:var(--n);color:#fff}
.cyad-btn svg{width:20px;height:20px;flex:none}
body .cyad a.cyad-link{color:var(--n);font-weight:600;text-decoration:underline;text-underline-offset:5px}
.cyad .cyad-reply{margin:14px 0 0;color:var(--m);font-size:14.5px}
.cyad-sec{padding-block:34px;border-top:1px solid var(--l)}
.cyad-sec--soft{background:var(--s);border:1px solid var(--l);border-radius:8px;padding:30px clamp(18px,3vw,34px);margin-block:8px}
.cyad-who{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.cyad-card{background:#fff;border:1px solid var(--l);border-radius:8px;padding:22px;display:flex;flex-direction:column;gap:4px}
.cyad-card p{color:var(--m);flex:1}
.cyad-card .cyad-btn{align-self:flex-start;margin-top:6px}
.cyad-checks{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 28px}
.cyad-checks li{display:flex;gap:10px;align-items:flex-start;line-height:1.6;font-size:16px}
.cyad-checks svg{width:20px;height:20px;flex:none;margin-top:3px;color:var(--t)}
.cyad-why{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px 36px}
.cyad-why p{color:var(--m)}
.cyad-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;counter-reset:none}
.cyad-steps li{border:1px solid var(--l);border-radius:8px;padding:20px;background:#fff}
.cyad-num{display:inline-grid;place-content:center;width:34px;height:34px;border-radius:50%;background:var(--c);color:var(--n);font-weight:800;margin-bottom:10px;font-family:var(--cy-font-display,"Frank Ruhl Libre"),Georgia,serif}
.cyad-onmap{display:flex;flex-wrap:wrap;gap:10px 22px}
body .cyad .cyad-onmap a{color:var(--n);font-weight:700;text-decoration:underline;text-underline-offset:5px}
.cyad-faq details{border-bottom:1px solid var(--l);padding:4px 0}
.cyad-faq summary{cursor:pointer;font-weight:700;color:var(--n);padding:12px 0;font-size:16.5px;list-style-position:inside}
.cyad-faq details p{color:var(--m);padding-bottom:6px}
.cyad-end{margin-top:26px;background:var(--n);color:#FBF8F2;border-radius:8px;padding:34px clamp(18px,4vw,44px);text-align:center}
.cyad-end h2{color:#FBF8F2!important}
.cyad-end p{color:#C9D5DE}
.cyad-end .cyad-btn{margin-top:6px}
.cyad[dir=ltr]~*,.cyad[dir=ltr]{text-align:left}
body:has(.cyad[dir=ltr]) .wp-block-post-title{direction:ltr;text-align:left}
@media(max-width:860px){.cyad-who,.cyad-steps{grid-template-columns:1fr}.cyad-checks,.cyad-why{grid-template-columns:1fr}}
@media(max-width:600px){.cyad-ctas .cyad-btn{width:100%}.cyad-sec{padding-block:26px}.cyad-card{padding:18px}}
"""
