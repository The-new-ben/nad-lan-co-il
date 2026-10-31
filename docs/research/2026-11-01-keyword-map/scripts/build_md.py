# -*- coding: utf-8 -*-
"""Builds keyword-map.md tables from terms.json (DataForSEO volumes + GSC 90d) plus the hand-decided owner/action rows below."""
import json, io
T = json.load(io.open('terms.json', encoding='utf-8'))
PP = {  # page-level GSC 90d (2.8-30.10.2026): impressions, clicks, avg position
    '/projects/': (25353, 7, 45.8), '/tel-aviv-apartment-prices/': (367, 0, 18.0), '/ramat-gan-apartment-prices/': (1018, 4, 7.7),
    '/givatayim-apartment-prices/': (72, 0, 6.9), '/herzliya-apartment-prices/': (1774, 7, 8.3), '/petah-tikva-apartment-prices/': (437, 0, 7.6),
    '/bat-yam-apartment-prices/': (98, 0, 7.9), '/holon-apartment-prices/': (20, 0, 6.1), '/rishon-lezion-apartment-prices/': (92, 0, 6.3),
    '/ramat-hasharon-apartment-prices/': (360, 1, 7.5), '/kiryat-ono-apartment-prices/': (246, 1, 8.3), '/bnei-brak-apartment-prices/': (107, 0, 7.0),
    '/bat-yam/': (71, 1, 7.2), '/herzliya-projects/': (217, 1, 30.9), '/urban-renewal/map/': (2841, 28, 27.0),
    '/eilat-apartment-prices/': (409, 1, 7.1),
}
def vol(k):
    v = T[k]['vol']
    return '-' if v is None else f"{v:,}"
def gsc(k):
    t = T[k]; i = t['gsc_impr']
    if not i:
        return '0'
    s = f"{i:,} / {t['gsc_clicks']} / {t['gsc_pos']}"
    d = min(t['dead_city_impr'], i)
    if d:
        s += f" ({d} of it on retired /city/ URLs, 410)"
    return s
def pp(u):
    i, c, p = PP[u]
    return f"page: {i:,} / {c} / {p}"

CITY = [  # (city label, term suffix, price page, compounds on site, market projects 25.10)
    ('רמת גן', 'ברמת גן', '/ramat-gan-apartment-prices/', 78, 37),
    ('גבעתיים', 'בגבעתיים', '/givatayim-apartment-prices/', 24, 6),
    ('הרצליה', 'בהרצליה', '/herzliya-apartment-prices/', 25, 19),
    ('פתח תקווה', 'בפתח תקווה', '/petah-tikva-apartment-prices/', 37, 32),
    ('בת ים', 'בבת ים', '/bat-yam-apartment-prices/', 40, 29),
    ('חולון', 'בחולון', '/holon-apartment-prices/', 26, 12),
    ('ראשון לציון', 'בראשון לציון', '/rishon-lezion-apartment-prices/', 20, 14),
    ('רמת השרון', 'ברמת השרון', '/ramat-hasharon-apartment-prices/', 8, 16),
    ('קרית אונו', 'בקרית אונו', '/kiryat-ono-apartment-prices/', 17, 9),
    ('בני ברק', 'בבני ברק', '/bnei-brak-apartment-prices/', 8, 0),
]

rows_center = []
R = rows_center.append
# Tel Aviv + centre-wide
R(('דירות למכירה בתל אביב', 'GAP (registry: "city page, HAD-602, later")', '-',
   'Listing intent; SERP = listing portals. Parked by Ben 25.10 ("the cities later"). Now that the centre is priority 1, HAD-602 needs his word. Until then: only a qualified H2 inside /tel-aviv-apartment-prices/ (kw_guard WARN = allowed as a qualified phrase).'))
R(('פרויקטים חדשים בתל אביב', '/projects/ (registry owner)', '/new-projects/new-projects-tel-aviv/ (28d: 43 impr @59.6 vs /projects/ 374 @55.2); /projects/?city= (canonical to /projects/)',
   'Strengthen the owner: a Tel Aviv block high on /projects/ (H2 "פרויקטים חדשים בתל אביב", the 143 TA projects of market.json 25.10 with sourced from-prices, link to every TA project page). Tel Aviv is the biggest city slice of the hub (5,203 of 23,768 visible query impressions on /projects/, 90d). /projects/ slipped from @41.7 (90d) to @55.2 (28d) on this query: measure again 2-4 weeks after the 25.10 retarget of the TA page.'))
R(('דירות חדשות בתל אביב', '/projects/ (registry)', '/new-projects/new-projects-tel-aviv/ (28d: 22 @58.8)', 'Same TA block on /projects/; the phrase in the block H2/answer paragraph and FAQ.'))
R(('דירות מקבלן בתל אביב', '/projects/', '/ (home, 28d: 22 @61.9); /new-projects/new-projects-tel-aviv/ owns "דירה חדשה מקבלן בתל אביב" (57 @19.1 vs /projects/ 12 @46.4)',
   'Keep the TA page on its own angle (אכלוס מיידי). The /projects/ TA block covers "מקבלן". No change to the home page.'))
R(('מחירי דירות בתל אביב', '/tel-aviv-apartment-prices/', '/projects/ on "מחיר דירה חדשה בתל אביב" (68 @48.7 vs owner 70 @12.2)',
   f'Owner is right ({pp("/tel-aviv-apartment-prices/")}). Add a "מחיר דירה חדשה בתל אביב" table (new-build from-prices from market.json, as published) so the new-price query stays here.'))
R(('פינוי בינוי בתל אביב', '/urban-renewal/pinui-binui-tel-aviv/', '/projects/ (78 @68.2) and /urban-renewal/map/ (22 @41.0) on "פרויקטי פינוי בינוי בתל אביב"',
   'Owner page (85 impr @21.2) links only 2 project pages (Kikar HaMedina, Rainbow) and none of the TA renewal compounds. Add the TA compound list (55 registry compounds on the site) with links, plus a link to the map filtered to TA. Title keeps its lead.'))
R(('תמא 38 תל אביב', '/urban-renewal/tama-38-tel-aviv/', '-',
   'No exact-query row in GSC, but the family ("תמא 38 רובע 3 תל אביב" 67 @46, "יזם תמא 38 תל אביב" 65 @31, "תמא 38 תל אביב פרויקטים" 47 @47) all lands on the owner (page 529 / 2 / 21.5). Add answer lines for רובע 3 and choosing a developer.'))
R(('שדה דב', '/sde-dov/ (registry)', '/sde-dov-luxury-projects-2026/ (12 @67) and /sde-dov/merkaz/ (8 @36) on "שדה דב תל אביב"; /sde-dov/prices/ on "דירות למכירה בשדה דב" (Q7, waiting for Ben)',
   'Owner upgraded 26.10 (S1). 28d position 28.1 vs 21.4 over 90d. The post /sde-dov-luxury-projects-2026/ leads its title with "רובע שדה דב" (kw_guard BLOCK, owner /sde-dov/): re-lead it with its own topic. Q7 decision is Ben\'s.'))
R(('פרויקטים חדשים בצפון תל אביב', 'registry: /projects/; a dedicated page exists: /new-projects/north-tel-aviv-new-projects/', '/projects/ 198 @43.4 vs the dedicated page 0 on this query',
   'Conflict to settle: the dedicated page leads its H1 with the term (kw_guard BLOCK). Volume is small (20) but the family is not ("פרויקטים חדשים בצפון הישן תל אביב" 276, "פרויקטים בצפון תל אביב" 81, all on /projects/). Pick one owner: either update the registry to the dedicated page, or re-lead its H1 with its comparison angle.'))
R(('השקעות נדלן בתל אביב', '/investment-apartment/tel-aviv-investment-neighborhoods/', '/investment/ (185 @71.9, 28d 80 @58.6)',
   'Specific page exists (314 / 0 / 8.3 page-level) but /investment/ takes the query. Exact anchor from the TA row of the /investment/ city table to the owner.'))
R(('נדלן בתל אביב', 'GAP (was /city/, 410 since 25.8)', '/ (home 24 @63)', 'Small (40). No new URL. Leave.'))
R(('פרויקטים חדשים במרכז', '/projects/', '/ (home 8 @65)', 'Add an H2 "פרויקטים חדשים במרכז" on /projects/ that indexes the 11 centre cities (the city sections below).'))
R(('דירות למכירה במרכז', 'GAP (registry: "דירות למכירה" belongs to /properties/)', '-', 'Listing intent, 26 listings site-wide. No action beyond /properties/.'))
# cities
for name, suf, price, comp, mk in CITY:
    if name == 'הרצליה':
        R((f'דירות למכירה {suf}', 'GAP (registry: HAD-602, later)', '-', 'Listing intent; parked HAD-602.'))
        R(('פרויקטים חדשים בהרצליה', '/herzliya-projects/', '/projects/ (164 @40.2 over 90d; 28d 43 @63.5); /herzliya-apartment-prices/ (see next row)',
           f'Owner gets "איזה פרויקטים חדשים יש בהרצליה" 150 @38.5 ({pp("/herzliya-projects/")}). kw_guard BLOCKs its title because the registry gives the bare "פרויקטים חדשים" to /projects/: add a city-level registry row "פרויקטים חדשים בהרצליה" -> /herzliya-projects/. Refresh it with the 19 Herzliya projects of market.json.'))
        R(('דירות חדשות בהרצליה', '/herzliya-projects/ (proposed)', '/herzliya-apartment-prices/ takes it today (75 @27.7; 28d "דירה חדשה בהרצליה" 40 @16)',
           'Real pair. The price page ranks better today. Keep "מחיר דירה חדשה" on the price page; its new-apartments paragraph links "פרויקטים חדשים בהרצליה" to /herzliya-projects/. Re-check in 4 weeks; if the price page still wins, flip ownership rather than fight it.'))
        R((f'מחירי דירות {suf}', price, '-', f'Owner right ({pp(price)}).'))
        R((f'פינוי בינוי {suf}', '/urban-renewal/map/ (city panel)', '-', f'{comp} compounds on the site. Small (10).'))
        continue
    if name == 'בת ים':
        R((f'דירות למכירה {suf}', 'GAP (registry: HAD-602, later)', '-', 'Listing intent; parked HAD-602.'))
        R((f'פרויקטים חדשים {suf}', 'GAP since 25.8; proposed /bat-yam/ (city guide)', 'dead /city/בת-ים/projects/ (410); /projects/?city= (canonical)',
           f'/bat-yam/ is already the city hub (renewal, light rail; {pp("/bat-yam/")}). Add a new-projects section from market.json ({mk} Bat Yam projects, sourced) + the 39 renewal compounds + Aura Pivko and the Rothschild sea tower pages. Same Ben OK as the other cities.'))
        R((f'דירות חדשות {suf}', 'proposed /bat-yam/', 'as above', 'Same section.'))
        R((f'מחירי דירות {suf}', price, '/bat-yam/ (title also promises "מחירי דירות"; no query-level clash seen yet)', f'Owner right ({pp(price)}). Re-lead /bat-yam/ title on the city guide angle so the two do not compete on prices.'))
        R((f'פינוי בינוי {suf}', '/urban-renewal/map/ (city panel)', '/projects/aura-pivko-bat-yam/ (3 @86)', f'{comp} compounds on the site.'))
        R(('נדלן בבת ים', 'proposed /bat-yam/', 'dead /city/בת-ים/ (410)', 'Was 53 impr on the retired city page; the city guide is the natural owner.'))
        continue
    R((f'דירות למכירה {suf}', 'GAP (registry: HAD-602, later)', '-', 'Listing intent; parked HAD-602.'))
    note = (f'GAP since 25.8 (city layer retired, 410). Proposed owner {price} with a "פרויקטים חדשים {suf}" section '
            f'({mk} projects in market.json 25.10, sourced; {comp} renewal compounds on the site). This is proposal 1 of the 25.10 traffic plan, waiting for Ben (pace).') if mk else (
            f'GAP since 25.8. market.json has 0 Bnei Brak projects, so there is nothing honest to list yet; {comp} project pages on the site (5 non-renewal). Leave until there is data.')
    if name in ('רמת גן', 'ראשון לציון', 'קרית אונו'):
        note += ' The retired /city/ page ranked this query at @21 to @28 before 25.8: proof it is winnable.'
    R((f'פרויקטים חדשים {suf}', 'GAP' + (f' -> proposed {price}' if mk else ''), '/projects/ only (28d, @54 to @78)', note))
    R((f'דירות חדשות {suf}', 'GAP' + (f' -> proposed {price}' if mk else ''), '/projects/', 'Same section.' if mk else 'Same as above.'))
    R((f'מחירי דירות {suf}', price, '-', f'Owner right ({pp(price)}); the head phrase itself shows few visible impressions (most of the page\'s impressions are anonymised long-tail).'))
    R((f'פינוי בינוי {suf}', '/urban-renewal/map/ (city panel)', '/projects/' if name == 'בני ברק' else '-', f'{comp} compounds on the site.'))

rows_lux = [
    ('פנטהאוז', '/glossary/penthouse/ (not in the registry yet)', '-',
     'Biggest non-brand luxury head (3,600). Owner is thin: 1,490 words, one H2; page-level 105 / 1 / 8.0, nothing visible for the bare word. Upgrade in place: definition, penthouse vs mini vs garden/roof, rules for roof terraces and building rights, price ranges by city (link /tel-aviv-penthouse-prices/), real listings. Add "פנטהאוז" -> /glossary/penthouse/ to the registry. SERP check first.'),
    ('מיני פנטהאוז', 'GAP -> /glossary/penthouse/', '-',
     'Section on the glossary page (the "penthouse" slug word is already owned, so no new URL). Link the real Kochav HaTzafon mini-penthouse listing (HAD-551).'),
    ('פנטהאוז למכירה', '/properties/ (registry)', '-', 'Listing intent; only real listings. Honest odds low.'),
    ('פנטהאוז בתל אביב', '/tel-aviv-penthouse-prices/', '-',
     'Title already leads with the term (kw_guard OK); page-level 98 / 0 / 7.3, nothing visible on the head. Add a "פנטהאוזים למכירה בתל אביב" section: the real Kochav listing + penthouse from-prices published by TA projects (market.json).'),
    ('פנטהאוז למכירה בתל אביב', '/tel-aviv-penthouse-prices/', '-', 'Same section; CPC 4.24 (commercial).'),
    ('פנטהאוז בהרצליה', 'GAP -> /glossary/penthouse/ city table', '-', 'Small (20 each for Herzliya, Ramat Gan, Bat Yam, Petah Tikva). No new URLs.'),
    ('דירות יוקרה', '/luxury-apartments-israel-guide-he/', '/luxury-apartments-israel-guide/ (English twin, different language)',
     'Owner page-level 147 / 0 / 27.6. "דירת יוקרה" is the same Google Ads group (320). Add a project table (the luxury project pages on the site) and price bands.'),
    ('דירות יוקרה למכירה', '/luxury-apartments-israel-guide-he/', '-', 'Same page.'),
    ('נדלן יוקרה', '/luxury-apartments-israel-guide-he/', '-', 'Same page.'),
    ('מגדלי יוקרה', '/luxury-apartments-israel-guide-he/', '/projects/ (93 @38.6 over 90d, gone in 28d)', 'Owner holds it in 28d (57 @61.5). Towers section on the guide.'),
    ('דירות יוקרה בתל אביב', '/luxury-tel-aviv/', '/property-value/luxury-apartments-tel-aviv/ and /tel-aviv-luxury-apartment-prices/ (title-level: three pages on one head; only 1 visible impression so far)',
     'Owner page-level 75 / 0 / 57.6. Re-lead /property-value/luxury-apartments-tel-aviv/ title with its own topic (the pre-purchase checks) instead of "דירות יוקרה בתל אביב:". The prices page keeps "מחירי דירות יוקרה בתל אביב".'),
    ('דירות יוקרה למכירה בתל אביב', '/luxury-tel-aviv/', 'as above', 'Same page.'),
    ('פרויקטי יוקרה בתל אביב', '/luxury-tel-aviv/', '/projects/ (18 @61.9; 28d 10 @77.5)', 'No Google Ads figure, but 73 GSC impressions. Owner H1 already leads with "פרויקטי היוקרה". Link every TA luxury project from it.'),
    ('מגדלי יוקרה בתל אביב', '/luxury-tel-aviv/ (proposed)', '/projects/hamedina/ catches the towers family ("מגדלים תל אביב" 57, "מגדלים בתל אביב" 51, "מגדלי מגורים בתל אביב" 39 @20.7)',
     'Add a TA towers table to /luxury-tel-aviv/ (Akirov, YOO, Meier on Rothschild, H Infinity, Einstein Tower, Kikar HaMedina, DUO, Park Bavli, Rainbow), each linked. Kikar HaMedina stays a project page.'),
    ('מגדלי מגורים בתל אביב', '/luxury-tel-aviv/ (proposed)', 'as above', 'Same table.'),
    ('מגדלי מגורים', 'GAP -> /luxury-apartments-israel-guide-he/', '-', 'Generic informational (70).'),
    ('קו ראשון לים', '/tel-aviv-seafront-apartment-prices/', '-', 'Owner page-level 66 / 0 / 7.1. Add a "קו ראשון לים במרכז" section (TA, Bat Yam, Herzliya; SIX-8 Herbert Samuel, Marina towers Herzliya) for the generic terms below.'),
    ('דירות על הים', '/tel-aviv-seafront-apartment-prices/ (proposed)', '-', 'Generic (110), not TA-only; same section.'),
    ('דירה מול הים', '/tel-aviv-seafront-apartment-prices/ (proposed)', '-', 'Same section.'),
    ('דירות עם נוף לים', '/tel-aviv-seafront-apartment-prices/ (proposed)', '-', 'Same section.'),
    ('הרצליה פיתוח', '/herzliya-pituach-luxury/ (not in the registry yet)', '/herzliya-pituach-apartment-prices/ (title-level: its SEO title also leads with "הרצליה פיתוח —")',
     'Second-biggest non-brand luxury head (2,900). Owner page-level 44 / 0 / 7.4, nothing visible on the bare name; SERP is mixed (business park, beach, municipality). Re-lead the prices page SEO title with "מחירי וילות ודירות בהרצליה פיתוח" (its H1 already does). Add the term to the registry.'),
    ('בתים למכירה בהרצליה פיתוח', '/herzliya-pituach-apartment-prices/', '/properties/herzliya-pituach-private-estate-for-sale/ (the real listing; "וילות למכירה בהרצליה" 11 @58.6)', 'A "וילות ובתים למכירה בהרצליה פיתוח" section that links the real listing.'),
    ('וילה למכירה בהרצליה פיתוח', '/herzliya-pituach-apartment-prices/', 'as above', 'Same section.'),
    ('פרויקטים חדשים בהרצליה פיתוח', '/herzliya-projects/', 'retired /city/הרצליה/projects/ (67 @39.5, 410)', 'Owner H1 already names פיתוח.'),
    ('מגדלי אקירוב', '/projects/akirov-towers/', '-', 'Owner page-level 98 / 0 / 6.9; the head (480) not visible. Strengthen in place (deals, prices, floor plans as published).'),
    ('מגדלי yoo', '/projects/yoo-tel-aviv/', '/projects/ (4 @27.5)', 'Owner page-level 376 / 1 / 10.7.'),
    ('מגדלי הים התיכון', '/projects/migdalei-hayam-sde-dov/', '-',
     'Brand head (2,400) of a senior-living chain; our page covers the Sde Dov branch only (219 / 1 / 8.3 on AI-style long-tail). Keep it honest to that branch.'),
    ('צוקי אביב', 'GAP (only the rental listing /properties/tzukei-aviv-double-height-mini-penthouse-for-rent/)', '-',
     'The "tzukei" slug word is already held by the listings, so a new project URL needs url_word_audit first. Listing stays the page for now.'),
    ('ישראל קנדה', 'brand (navigational); no company profile on the site', '-', 'Our pages own the projects (Rainbow 2,634 / 30 / 8.9). A profile page needs url_word_audit; do not chase the brand head.'),
    ('אאורה', '/professionals/aura-israel/', '-', 'Profile 131 / 0 / 9.3; brand head is navigational. Strengthen "אאורה פרויקטים" (Aura Pivko Bat Yam).'),
    ('אזורים', '/professionals/azorim/', '-', 'Profile 38 / 0 / 19.2; H1 is the bare name. Navigational head.'),
    ('יוסי אברהמי', 'brand; no profile', '-', 'Navigational head; no project page either.'),
    ('דמרי', 'brand; no company profile (project: /projects/dimri-yama-sde-dov/)', '-', 'The "dimri" slug word is held by the project page; a profile URL needs url_word_audit.'),
    ('גינדי החזקות', 'brand; no company profile (project: /projects/gindi-vogue-sde-dov/)', '-', 'Same: "gindi" is held by the project slug.'),
    ('אפריקה ישראל מגורים', '/professionals/africa-israel-residential/', '-', 'Profile 10 / 0 / 24.8. Ties to DUO (2,967 / 45 / 10.1).'),
]

rows_eilat = [
    ('דירות להשכרה באילת', 'GAP -> /eilat-apartment-prices/ (H1 already names שכירות)', '-',
     'Biggest Eilat term (2,400) but listing intent; we have no Eilat listings. The rent-fairness tool on /דירות-להשכרה/ covers 72 cities: an Eilat rent table on the Eilat page is the honest share.'),
    ('דירות למכירה באילת', 'GAP -> /eilat-apartment-prices/ (qualified H2)', '-', 'Listing intent (590; "דירה למכירה באילת" is the same Ads group). No listings.'),
    ('שחמון אילת', 'GAP -> /eilat-apartment-prices/', '-', 'Page already mentions Shachamon 19 times and has an H2 on it; make it a named section ("שחמון: מחירים, דירות חדשות").'),
    ('וילה למכירה באילת', 'GAP -> /eilat-apartment-prices/', '-', 'Villa/house price section (page has 3 mentions of וילה).'),
    ('בתים למכירה באילת', 'GAP -> /eilat-apartment-prices/', '-', 'Same section.'),
    ('פרויקטים חדשים באילת', 'GAP (was /city/אילת/, 410 since 25.8) -> /eilat-apartment-prices/', '-',
     'New-projects section from market.json 25.10: 5 Eilat projects in marketing (AQUA PORT, AQUA RESORT, Terra & Golf by עמרם אברהם; two by אייל פרץ), from-prices 1.29M to 2.49M as published, plus the 6 renewal compounds.'),
    ('פרויקטים באילת', 'GAP -> /eilat-apartment-prices/', '-', 'Same section.'),
    ('פנטהאוז באילת', 'GAP -> /eilat-apartment-prices/', '-', 'Penthouse line in the room table (page has 0 mentions today).'),
    ('דירה להשקעה באילת', 'GAP -> /eilat-apartment-prices/', '-', 'No /investment/<city> page for Eilat, and a new one would reuse the owned words "eilat" and "investment". Investment section on the Eilat page.'),
    ('שכונות באילת', '/eilat-apartment-prices/', '-', 'Page has a neighbourhoods H2.'),
    ('נדלן אילת', 'GAP (was /city/אילת/, 410) -> /eilat-apartment-prices/', '-', '"נדלן באילת" (40) is the same family.'),
    ('מחיר למשתכן אילת', '/dira-behanacha/ (owner of מחיר למשתכן)', '-', 'Eilat lottery rows on the owner page; link from the Eilat page.'),
    ('מחירי דירות באילת', '/eilat-apartment-prices/', '-',
     'Owner (409 / 1 / 7.1 page-level, 4,639 words). "מחיר דירה באילת" is the same Ads group.'),
    ('פטור ממעמ אילת', 'GAP -> /eilat-apartment-prices/ FAQ', '-', 'Small (20, seasonal spikes to 90). FAQ only after the VAT rules are checked against the official source.'),
    ('דירות יוקרה באילת', 'GAP -> /eilat-apartment-prices/', '-', 'Small (20).'),
    ('דירת נופש באילת למכירה', '/eilat-apartment-prices/', '-', 'Title already leads with "דירת נופש".'),
    ('פינוי בינוי באילת', '/urban-renewal/map/ (city panel) + 6 compound pages', '7 "Eilat street" compounds in other cities whose titles start "אילת, <city>" (Holon x3, Bat Yam, Ramat HaSharon, Tel Aviv, Lod): ambiguity risk, no GSC clash seen',
     'Small (10). Eilat compounds: מתחם 22 צין פארן 390, מתחם 19 לוס אנג׳לס אילות 420, מתחם 12 קדש ירושלים השלמה 450, מתחם 23 סמטת המערות 180, מתחם 6 ברנע 480, שדרות התמרים (סינג סינג) 420 = 2,340 planned units; together 41 impr, 1 click. Link them from the Eilat page.'),
]

def table(rows, title):
    out = [f'## {title}', '', '| מונח | חיפושים בחודש | עמוד בעלים (או GAP) | GSC 90 יום: חשיפות / קליקים / מיקום | עמודים מתחרים (קניבל) | המלצה |', '|---|---|---|---|---|---|']
    for term, owner, cann, act in rows:
        out.append(f'| {term} | {vol(term)} | {owner} | {gsc(term)} | {cann} | {act} |')
    return '\n'.join(out) + '\n'

open('tables.md', 'w', encoding='utf-8').write(
    table(rows_center, '1. המרכז (Centre: Tel Aviv and 10 cities)') + '\n' +
    table(rows_lux, '2. יוקרה (Luxury)') + '\n' +
    table(rows_eilat, '3. אילת (Eilat)'))
print('rows', len(rows_center), len(rows_lux), len(rows_eilat))
