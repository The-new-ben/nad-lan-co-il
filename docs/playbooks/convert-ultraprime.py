# -*- coding: utf-8 -*-
# Ultra-prime phase 1 convert: flagship + 4 launch spokes -> seed payload.
# - strips the working-comment header; H1 becomes the post title
# - /projects/ -> /new-projects/ (the commercial anchor owns that intent)
# - links to the 8 NOT-yet-published spokes are unlinked (text kept; each
#   regains its link when its stage publishes)
# - every spoke back-anchor gets a real id on the matching flagship H2
#   (mapped by keyword overlap, fails loudly if no match)
import base64, io, json, re, sys, zlib
import markdown

SRC = r'C:\Users\pro\AppData\Local\Temp\claude\C--Users-pro-nad-lan\a1527a51-5842-4f81-8165-9a594085b50f\scratchpad\ultraprime\nadlan_ultra_prime_content_system'
OUT = r'C:\Users\pro\AppData\Local\Temp\claude\C--Users-pro-nad-lan\a1527a51-5842-4f81-8165-9a594085b50f\scratchpad\ultraprime-payload.b64.txt'

LAUNCH = {
    'ultra-prime-construction': ('05_flagship_draft.md',
        u'איך בונים פרויקט מגורי אולטרה-פריים | מהקרקע עד שנת 15',
        u'מה עושה יזם שרוצה לבנות את פרויקט המגורים הטוב ביותר האפשרי: קרקע, שלד, מעטפת, מערכות, שירות, ספא, מסירה ותחזוקה עד שנת ה-15.',
        u'מסע מן הבריף הראשון ועד התקלה הראשונה, דרך הקרקע, השלד, החזית, המערכות, המלון הנסתר והתחזוקה שמחזיקה את היוקרה בחיים.'),
    'groundwater-deep-basements': ('06_deep_dives/06_01_groundwater_deep_basements.md',
        u'מרתפים עמוקים ומי תהום בפרויקט יוקרה | מדריך',
        u'לפני שהמגדל עולה, הפרויקט יורד לאדמה. כך בודקים קרקע, דיפון, מי תהום, איטום, חניה, משאבות וניטור שכנים בפרויקט שאפתני.',
        u'החפירה, הדיפון, מי התהום והעיר התפעולית שמתחת ללובי קובעים אם המרתף יישאר יבש, נגיש ונוח לאורך שנים.'),
    'residential-tower-envelope-glass': ('06_deep_dives/06_03_residential_tower_envelope_glass.md',
        u'מעטפת וזכוכית במגדל מגורים | מה בודקים',
        u'חזית יוקרתית צריכה לעצור מים, אוויר, חום ורעש, ולאפשר ניקוי והחלפה. מדריך לזכוכית, איטום, בדיקות ותחזוקה.',
        u'חזית היא מכונת אקלים: זכוכית, מסגרות, אטמים, ניקוז, הצללה וגישה לתחזוקה עובדים יחד מול רוח, גשם ושמש.'),
    'luxury-residential-pool-spa': ('06_deep_dives/06_08_luxury_residential_pool_spa.md',
        u'בריכה וספא בבניין יוקרה | ההנדסה מאחורי המים',
        u'בריכה, ספא, סאונה וחדר כושר נראים נהדר בהדמיה. כך בודקים קיבולת, טיפול במים, לחות, רעש, כוח אדם ותחזוקה.',
        u'המים הם רק החלק הנראה. מאחוריהם פועלים סינון, חיטוי, אוורור, איטום, חדרי מכונות וצוות שמחזיק את המתקן פתוח.'),
    'residential-commissioning-year-15': ('06_deep_dives/06_12_residential_commissioning_year_15.md',
        u'Commissioning בבניין מגורים | מסירה ושנת 15',
        u'המסירה אינה סוף הבנייה. כך בודקים מערכות, תרחישי כשל, תיעוד, הדרכת צוות ותכנית חידוש שמחזיקה את הבניין.',
        u'בדיקות משולבות, תכניות עדות, הדרכת צוות וקרן חידוש הופכות בניין חדש למערכת שיודעת לעבוד ולהזדקן.'),
}
LAUNCH_URLS = {'/guides/%s/' % s for s in LAUNCH}

def load(rel):
    t = io.open(SRC + '\\' + rel.replace('/', '\\'), encoding='utf-8').read()
    t = re.sub(r'^<!--.*?-->\s*', '', t, flags=re.S)          # working header
    m = re.match(r'# (.+)\n', t)
    title = m.group(1).strip()
    body = t[m.end():].strip()
    return title, body

# collect every spoke back-anchor (all 12) so future stages just work
anchors = []
import glob as _g, os
for f in sorted(_g.glob(os.path.join(SRC, '06_deep_dives', '06_*.md'))):
    t = io.open(f, encoding='utf-8').read()
    for a in re.findall(r'/guides/ultra-prime-construction/#([^)\s]+)', t):
        anchors.append(a)
anchors = sorted(set(anchors))

pages = []
for slug, (rel, yt, yd, exc) in LAUNCH.items():
    title, body = load(rel)
    if slug == 'ultra-prime-construction':
        body = body.replace('](/projects/)', '](/new-projects/)')
        # unlink not-yet-published spokes, keep their text
        for m in set(re.findall(r'\[([^\]]+)\]\((/guides/[a-z0-9\-]+/)\)', body)):
            text, url = m
            if url not in LAUNCH_URLS and url != '/new-projects/':
                body = body.replace('[%s](%s)' % (text, url), text)
    html = markdown.markdown(body, extensions=['tables', 'sane_lists', 'footnotes'])
    if slug == 'ultra-prime-construction':
        # give each back-anchor a real id on the best-matching h2
        h2s = re.findall(r'<h2>(.*?)</h2>', html)
        for a in anchors:
            words = [w for w in a.replace('-', ' ').split() if len(w) > 1]
            best, score = None, 0
            for h in h2s:
                s = sum(1 for w in words if w in h)
                if s > score:
                    best, score = h, s
            if best is None or score < max(1, len(words) - 2):
                sys.exit('ANCHOR UNRESOLVED: %s' % a)
            html = html.replace('<h2>%s</h2>' % best,
                                '<h2 id="%s">%s</h2>' % (a, best), 1)
    words = len(re.findall(u'[\u0590-\u05ff A-Za-z]{2,}'.replace(' ', ''), re.sub(r'<[^>]+>', ' ', html)))
    pages.append({'slug': slug, 'title': title, 'html': html,
                  'yoast_title': yt, 'yoast_desc': yd, 'excerpt': exc})
    print('%-36s title=%s… html=%dKB words~%d' % (slug, title[:28], len(html) // 1024, words))

payload = json.dumps(pages, ensure_ascii=False).encode('utf-8')
io.open(OUT, 'w').write(base64.b64encode(zlib.compress(payload, 9)).decode())
print('payload: %d pages, %d KB compressed' % (len(pages), len(zlib.compress(payload, 9)) // 1024))
print('anchors wired:', ', '.join(anchors))
