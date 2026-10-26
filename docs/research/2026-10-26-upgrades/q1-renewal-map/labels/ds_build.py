"""Builds the design-system component RenewalMapLabels (preview.html + README.md) for the owner's Claude Design board.

Self-contained page: the real label CSS from the patch (states drawn statically), the measured screenshots embedded as WebP,
the palette and faces, and the proof table read from proof-results.json. Writes only into the DS scratch folder.

    python ds_build.py
"""
import base64
import io
import json
import os
import re
import statistics
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib  # noqa: E402

DS = r'C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components\RenewalMapLabels'
os.makedirs(DS, exist_ok=True)
R = json.load(open(os.path.join(HERE, 'proof-results.json'), encoding='utf-8'))


def img(name, width):
    im = Image.open(os.path.join(HERE, name)).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, 'WEBP', quality=80, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


# the label + card CSS exactly as the patch ships it
hunks = {h['name'][:2]: h['new'] for h in lib.parse_patch()}
css_a = hunks['A1']
css_b = hunks['B1'].split('\n', 1)[1]  # drop the unchanged #nlurm-list line
# static copies of the interactive states, so the board can show them without a pointer
static = css_a
static = re.sub(r'\.nlurm-pin:hover', '.nlurm-pin.st-hover', static)
static = re.sub(r'\.nlurm-grp:hover', '.nlurm-grp.st-hover', static)
static = re.sub(r'\.nlurm-pin:active', '.nlurm-pin.st-press', static)
static = re.sub(r'\.nlurm-pin:focus-visible', '.nlurm-pin.st-focus', static)
static = re.sub(r'\.nlurm-pin\.is-q:hover', '.nlurm-pin.is-q.st-hover', static)
static = re.sub(r'\.nlurm-pin\.is-q:focus-visible', '.nlurm-pin.is-q.st-focus', static)
static_only = '\n'.join(l for l in static.split('\n') if 'st-' in l)


def row(v, z):
    b = R['views'][v]['before']['states'][z]
    a = R['views'][v]['after']['states'][z]
    def pct(n, d):
        return '%d%%' % round(100 * n / d) if d else '-'
    def pxm(x):
        return ('%.1f' % statistics.median(x['contrast_pixels'])) if x['contrast_pixels'] else '-'
    return [
        ('ניגודיות טקסט (WCAG, הנמוכה ביותר)', '%.2f:1' % min(b['contrast_text']), '%.2f:1' % min(a['contrast_text'])),
        ('ניגודיות שנמדדה בפיקסלים (חציון)', pxm(b) + ':1', pxm(a) + ':1'),
        ('זוגות תוויות חופפות', str(b['label_overlaps']), str(a['label_overlaps'])),
        ('שמות קריאים (מתוך הערים בתצוגה)', '%d / %d (%s)' % (len(b['names']), b['in_view'], pct(len(b['names']), b['in_view'])), '%d / %d (%s)' % (len(a['names']), a['in_view'], pct(len(a['names']), a['in_view']))),
        ('תווית שלמה: שם ומספר יחד', str(len(b['complete'])), str(len(a['complete']))),
        ('ערים שהמספר שלהן גלוי (לבד או בסכום קבוצה)', '%d / %d' % (len(b['counts_covered']), b['in_view']), '%d / %d' % (len(a['counts_covered']), a['in_view'])),
        ('ערים שאפשר להקיש עליהן בכלל', '%d / %d' % (len(b['tappable']), b['in_view']), '%d / %d' % (len(a['tappable']), a['in_view'])),
        ('יעד הקשה הקטן ביותר (פיקסלים)', '%s×%s' % (b['tap_min_w'], b['tap_min_h']), '%s×%s' % (a['tap_min_w'], a['tap_min_h'])),
        ('יעדי הקשה חופפים', str(b['tap_overlaps']), str(a['tap_overlaps'])),
    ]


ZN = {'country': 'כל הארץ (המבט הראשון של הדף)', 'central': 'מחוז המרכז', 'tlv': 'אזור תל אביב'}
VN = {'390': 'טלפון 390', '1280': 'מחשב 1280'}
tables = []
for v in ('390', '1280'):
    for z in ('country', 'central', 'tlv'):
        rows = ''.join('<tr><th>%s</th><td>%s</td><td>%s</td></tr>' % r for r in row(v, z))
        tables.append('<table class="pt"><caption>%s · %s · זום %s</caption><thead><tr><th></th><th>היום</th><th>ההצעה</th></tr></thead><tbody>%s</tbody></table>'
                      % (VN[v], ZN[z], R['views'][v]['after']['states'][z]['zoom'], rows))

ia = R['views']['390']['after']['interactions']
ib = R['views']['390']['before']['interactions']
da = R['views']['1280']['after']['interactions']
db = R['views']['1280']['before']['interactions']
def listed(i, v, m):
    st = R['views'][v][m].get('lookup_statuses') or []
    if i['list_loaded']:
        return 'כן (%d)' % i['list_loaded']
    return 'חסום זמנית במגבלת האתר (429)' if 429 in st else 'לא נטען'


clicks = [
    ('הקשה על עיר טוענת את רשימת המתחמים (כמו היום)', listed(ib, '390', 'before'), listed(ia, '390', 'after')),
    ('הקשה על עיר פותחת כרטיס עיר', 'אין', 'כן, %d×%d' % (ia['card']['w'], ia['card']['h'])),
    ('הכפתור "יומן המתחמים בעיר" מעביר את היומן לעיר', 'אין', 'כן: ' + str(ia.get('tracker', {}).get('select_value'))),
    ('הקשה על קבוצה מקרבת את המפה', 'אין קבוצות', 'זום %s ← %s' % (ia['group_tap']['zoom_before'], ia['group_tap']['zoom_after']) if ia.get('group_tap') else '-'),
    ('כפתור הזום', '%s ← %s' % (ib['zoom_button']['before'], ib['zoom_button']['after']), '%s ← %s' % (ia['zoom_button']['before'], ia['zoom_button']['after'])),
    ('החלקה באצבע אחת על המפה גוללת את הדף (טלפון)', '%d פיקסלים, המפה לא זזה' % ib['swipe_empty']['page_scrolled_px'], '%d פיקסלים, המפה לא זזה' % ia['swipe_empty']['page_scrolled_px']),
    ('החלקה שמתחילה על תווית גוללת את הדף (טלפון)', '%d פיקסלים' % ib['swipe_label']['page_scrolled_px'], '%d פיקסלים' % ia['swipe_label']['page_scrolled_px']),
    ('גלגלת העכבר מעל המפה גוללת את הדף (מחשב)', '%d פיקסלים, בלי זום' % db['wheel_empty']['page_scrolled_px'], '%d פיקסלים, בלי זום' % da['wheel_empty']['page_scrolled_px']),
    ('גרירה מזיזה את המפה (מחשב)', 'כן' if db['drag_pan']['pans'] else 'לא', 'כן' if da['drag_pan']['pans'] else 'לא'),
]
ctab = '<table class="pt"><caption>לחיצות ושימוש, נבדק בדף החי (טלפון 390 ומחשב 1280)</caption><thead><tr><th></th><th>היום</th><th>ההצעה</th></tr></thead><tbody>' + \
       ''.join('<tr><th>%s</th><td>%s</td><td>%s</td></tr>' % c for c in clicks) + '</tbody></table>'

PH = 520
pics = {k: img(k, w) for k, w in [('before-390-country.png', PH), ('after-390-country.png', PH), ('before-1280-central.png', 1000), ('after-1280-central.png', 1000),
                                  ('after-390-card.png', PH), ('after-1280-state-default.png', 600), ('after-1280-state-hover.png', 600),
                                  ('after-1280-state-pressed.png', 600), ('after-1280-state-selected.png', 600)]}

page = '''<!-- @dsCard group="Tools" height=3400 subtitle="תוויות הערים במפת ההתחדשות: עיגול לפי מספר המתחמים, המספר בתוכו, שם העיר בדיו עם הילה לבנה; בלי חפיפות, קבוצה לערים צמודות, כרטיס עיר בהקשה" -->
<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RenewalMapLabels</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<style>
:root{--ground:#F6F8F9;--paper:#FFFFFF;--ink:#12202A;--ink2:#3E4C58;--mute:#5E6A75;--line:#D3DCE2;--sea:#2F6F86;--deep:#1F4B5C;--red:#C42550;--wash:#E6F0F3;--land:#F1F2F0}
body{margin:0;background:var(--ground);font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif;color:var(--ink2)}
.w{max-width:1040px;margin:0 auto;padding:20px 16px 40px}
h1{font:600 26px/1.25 "IBM Plex Sans Hebrew";color:var(--ink);margin:0 0 6px}
.lead{font:400 15px/1.7 "IBM Plex Sans Hebrew";max-width:72ch;margin:0 0 6px}
.sec{font:500 12px/16px "IBM Plex Mono",monospace;color:var(--mute);margin:28px 0 10px;border-top:1px solid var(--line);padding-top:8px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.pair figure{margin:0;background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:8px}
.pair img{display:block;width:100%;height:auto;border-radius:4px}
.pair figcaption{font:500 13px/1.5 "IBM Plex Sans Hebrew";color:var(--ink);margin:6px 2px 2px}
.pair figcaption span{font:400 12px "IBM Plex Sans Hebrew";color:var(--mute);display:block}
.stage{position:relative;background:var(--land);border:1px solid var(--line);border-radius:6px;display:grid;grid-template-columns:repeat(4,1fr);gap:0}
.cell{position:relative;height:150px;border-inline-start:1px solid var(--line);border-bottom:1px solid var(--line)}
.cell:nth-child(4n+1){border-inline-start:0}
.cell .nlurm-pin{position:absolute;left:38%;top:48%;transform:translate(-50%,-50%)}
.cell p{position:absolute;bottom:6px;right:8px;left:8px;margin:0;font:500 12px/1.4 "IBM Plex Sans Hebrew";color:var(--ink2)}
.cell p i{font:400 11px "IBM Plex Mono";font-style:normal;color:var(--mute);display:block}
.shots{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px}
.shots figure{margin:0}.shots img{width:100%;border:1px solid var(--line);border-radius:4px;display:block}.shots figcaption{font:500 12px "IBM Plex Sans Hebrew";margin-top:4px}
.cardrow{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}
.cardbox{position:relative;height:330px;background:var(--land);border:1px solid var(--line);border-radius:6px;overflow:hidden}
.cardbox .nlurm-card{position:absolute}
.pal{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.sw{background:var(--paper);border:1px solid var(--line);border-radius:6px;overflow:hidden}
.sw i{display:block;height:46px}.sw b{display:block;font:600 13px "IBM Plex Sans Hebrew";color:var(--ink);padding:6px 8px 0}.sw code{display:block;font:500 12px "IBM Plex Mono";color:var(--mute);padding:0 8px 8px}
.faces{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.face{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:12px 14px}
.face .big{font:600 30px/1.2 "IBM Plex Sans Hebrew";color:var(--ink)}.face .mono{font:500 30px/1.2 "IBM Plex Mono";color:var(--deep)}
.face small{display:block;font:400 12px/1.5 "IBM Plex Sans Hebrew";color:var(--mute);margin-top:4px}
.why{border-inline-start:3px solid var(--sea);background:var(--paper);padding:10px 14px;font:500 14px/1.65 "IBM Plex Sans Hebrew";color:var(--ink);margin:12px 0 0}
.tables{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.pt{width:100%;border-collapse:collapse;background:var(--paper);border:1px solid var(--line);font:400 12.5px/1.45 "IBM Plex Sans Hebrew"}
.pt caption{text-align:right;font:600 13.5px "IBM Plex Sans Hebrew";color:var(--ink);padding:0 0 6px}
.pt th,.pt td{border-top:1px solid var(--line);padding:6px 8px;text-align:right;vertical-align:top}
.pt thead th{font:600 12px "IBM Plex Sans Hebrew";color:var(--mute);background:var(--wash)}
.pt tbody th{font-weight:500;color:var(--ink2);width:52%}
.pt td{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ink)}
.pt td:last-child{background:#F3F8FA}
.rules{margin:0;padding:0 18px 0 0;font:400 14px/1.75 "IBM Plex Sans Hebrew"}
.rules b{color:var(--ink);font-weight:600}
@media (max-width:760px){.pair,.cardrow,.faces,.tables{grid-template-columns:1fr}.stage,.shots{grid-template-columns:repeat(2,1fr)}.cell:nth-child(2n+1){border-inline-start:0}}
/* ===== the label CSS exactly as the patch ships it ===== */
''' + css_a + '\n' + css_b + '''
/* static copies of the pointer states, for the board only */
''' + static_only + '''
</style>
</head>
<body>
<div class="w">
<h1>תוויות הערים במפת ההתחדשות</h1>
<p class="lead">עיגול בגודל לפי מספר המתחמים, המספר בתוכו בכתב מונו לבן, ושם העיר בדיו כהה עם הילה לבנה לידו. שום תווית לא נוגעת באחרת. ערים צמודות מדי מתאחדות לעיגול אחד עם הסכום ו"ועוד", והקשה עליו מקרבת. הקשה על עיר טוענת את רשימת המתחמים כמו היום, ופותחת כרטיס עיר עם השלבים, הדירות והמעבר ליומן המתחמים.</p>

<div class="sec">01 · היום מול ההצעה, צילומים מהדף החי (ההצעה מוזרקת מקומית בדפדפן בלבד)</div>
<div class="pair">
<figure><img src="''' + pics['before-390-country.png'] + '''" alt="היום, טלפון, כל הארץ"><figcaption>היום · טלפון 390 · כל הארץ<span>תוויות פליז, ניגודיות 3.73:1, 475 זוגות חופפים</span></figcaption></figure>
<figure><img src="''' + pics['after-390-country.png'] + '''" alt="ההצעה, טלפון, כל הארץ"><figcaption>ההצעה · טלפון 390 · כל הארץ<span>אפס חפיפות, כל 74 הערים בתצוגה עם מספר גלוי, יעד הקשה 44 פיקסלים</span></figcaption></figure>
</div>
<div class="pair" style="margin-top:14px">
<figure><img src="''' + pics['before-1280-central.png'] + '''" alt="היום, מחשב, מחוז המרכז"><figcaption>היום · מחשב 1280 · מחוז המרכז</figcaption></figure>
<figure><img src="''' + pics['after-1280-central.png'] + '''" alt="ההצעה, מחשב, מחוז המרכז"><figcaption>ההצעה · מחשב 1280 · מחוז המרכז</figcaption></figure>
</div>

<div class="sec">02 · מבנה ומצבים (ה-CSS האמיתי של התיקון)</div>
<div class="stage">
<div class="cell"><button class="nlurm-pin is-e" type="button" style="--r:15.1px;--h:22px"><span class="nlurm-dot" style="font-size:12px">17</span><span class="nlurm-name">אשדוד</span></button><p>עיר<i>עיגול deep, שם מימין</i></p></div>
<div class="cell"><button class="nlurm-pin is-e is-big" type="button" style="--r:22.1px;--h:22.1px"><span class="nlurm-dot" style="font-size:13px">76</span><span class="nlurm-name">רמת גן</span></button><p>עיר גדולה (40 ומעלה)<i>שם 15 פיקסלים</i></p></div>
<div class="cell"><button class="nlurm-pin nlurm-grp is-e" type="button" style="--r:26px;--h:26px"><span class="nlurm-dot" style="font-size:13px">228</span><span class="nlurm-name">רמת גן ועוד 7</span></button><p>קבוצה<i>טבעת פנימית, הקשה מקרבת</i></p></div>
<div class="cell"><button class="nlurm-pin is-q" type="button" style="--r:10.5px;--h:22px"><span class="nlurm-dot" style="font-size:11px">1</span><span class="nlurm-name">בית דגן</span></button><p>שם ממתין<i>אין מקום: מופיע בזום, ריחוף או הקשה</i></p></div>
<div class="cell"><button class="nlurm-pin is-e st-hover" type="button" style="--r:15.1px;--h:22px"><span class="nlurm-dot" style="font-size:12px">17</span><span class="nlurm-name">אשדוד</span></button><p>ריחוף<i>הגדלה 1.08, טבעת sea, קו תחתון</i></p></div>
<div class="cell"><button class="nlurm-pin is-e st-press" type="button" style="--r:15.1px;--h:22px"><span class="nlurm-dot" style="font-size:12px">17</span><span class="nlurm-name">אשדוד</span></button><p>לחיצה<i>הקטנה 0.94</i></p></div>
<div class="cell"><button class="nlurm-pin is-e is-on" type="button" style="--r:15.1px;--h:22px"><span class="nlurm-dot" style="font-size:12px">17</span><span class="nlurm-name">אשדוד</span></button><p>נבחרה<i>עיגול ink, טבעת sea, שם הפוך</i></p></div>
<div class="cell"><button class="nlurm-pin is-q st-focus" type="button" style="--r:10.5px;--h:22px"><span class="nlurm-dot" style="font-size:11px">1</span><span class="nlurm-name">בית דגן</span></button><p>מקלדת<i>מסגרת sea, השם מופיע</i></p></div>
</div>
<div class="shots">
<figure><img src="''' + pics['after-1280-state-default.png'] + '''" alt="רגיל"><figcaption>רגיל, בדף החי</figcaption></figure>
<figure><img src="''' + pics['after-1280-state-hover.png'] + '''" alt="ריחוף"><figcaption>ריחוף, בדף החי</figcaption></figure>
<figure><img src="''' + pics['after-1280-state-pressed.png'] + '''" alt="לחיצה"><figcaption>לחיצה, בדף החי</figcaption></figure>
<figure><img src="''' + pics['after-1280-state-selected.png'] + '''" alt="נבחרה"><figcaption>נבחרה, בדף החי</figcaption></figure>
</div>

<div class="sec">03 · כרטיס העיר (נפתח בהקשה, יחד עם הרשימה של היום)</div>
<div class="cardrow">
<div class="cardbox">
<div class="nlurm-card" role="dialog" aria-label="תל אביב יפו" style="top:12px;left:12px;right:auto;bottom:auto;width:320px">
<button type="button" class="nlurm-x" aria-label="סגירה">×</button><div class="ct">תל אביב יפו</div><div class="c1"><b class="n">55</b> מתחמים במפה הזו<span class="m2"> · <b class="n">56</b> במפת הרשות</span></div>
<div class="more"><div class="nlurm-bar" aria-hidden="true"><i style="width:7.14%;background:#9DB7C3"></i><i style="width:5.36%;background:#5C93A8"></i><i style="width:46.43%;background:#2F6F86"></i><i style="width:8.93%;background:#1F4B5C"></i><i style="width:32.14%;background:#D3DCE2"></i></div>
<div class="nlurm-leg"><span style="--c:#9DB7C3"><em>תכנון ראשוני</em><b class="n">4</b></span><span style="--c:#5C93A8"><em>תכנון סטטוטורי</em><b class="n">3</b></span><span style="--c:#2F6F86"><em>מאושרת לפני מימוש</em><b class="n">26</b></span><span style="--c:#1F4B5C"><em>מאושרת במימוש</em><b class="n">5</b></span><span style="--c:#D3DCE2"><em>ללא שלב במפה</em><b class="n">18</b></span></div>
<div class="nlurm-units"><div><span>דירות היום</span><b class="n">7,324</b></div><div><span>אחרי הבנייה</span><b class="n">21,181</b></div></div>
<div class="k">מפת הרשות 25.10.2026 (הדירות מתוך 54 מתחמים עם שני הנתונים). מאז 15.8.2026: 2 נוספו, 1 עלה שלב, 1 לא מופיע עוד.</div></div>
<div class="nlurm-acts"><button type="button" class="go">יומן המתחמים בעיר</button><button type="button" class="ls">רשימת המתחמים</button></div>
</div>
</div>
<figure style="margin:0"><img src="''' + pics['after-390-card.png'] + '''" alt="כרטיס העיר בטלפון, בדף החי" style="width:100%;max-width:360px;border:1px solid var(--line);border-radius:6px;display:block"><figcaption style="font:500 12px 'IBM Plex Sans Hebrew';margin-top:4px">בטלפון, בדף החי: הכרטיס יושב בתחתית המפה</figcaption></figure>
</div>

<div class="sec">04 · צבעים וגופנים</div>
<div class="pal">
<div class="sw"><i style="background:#1F4B5C"></i><b>deep · עיגול</b><code>#1F4B5C · לבן עליו 9.46:1</code></div>
<div class="sw"><i style="background:#12202A"></i><b>ink · שם, נבחרה</b><code>#12202A · על לבן 16.59:1</code></div>
<div class="sw"><i style="background:#2F6F86"></i><b>sea · טבעות, מיקוד</b><code>#2F6F86</code></div>
<div class="sw"><i style="background:#FFFFFF;border-bottom:1px solid #D3DCE2"></i><b>הילה ומסגרת</b><code>#FFFFFF</code></div>
<div class="sw"><i style="background:#D3DCE2"></i><b>line · ללא שלב</b><code>#D3DCE2</code></div>
<div class="sw"><i style="background:linear-gradient(90deg,#9DB7C3 0 25%,#5C93A8 25% 50%,#2F6F86 50% 75%,#1F4B5C 75%)"></i><b>סולם השלבים</b><code>#9DB7C3 #5C93A8 #2F6F86 #1F4B5C</code></div>
<div class="sw"><i style="background:#C42550"></i><b>survey red · שמור לאזהרות</b><code>#C42550 · לא בשימוש כאן</code></div>
</div>
<div class="faces" style="margin-top:12px">
<div class="face"><div class="big">רמת גן ועוד 7</div><small>IBM Plex Sans Hebrew 600 · 13 פיקסלים (15 לעיר של 40 ומעלה) · שמות הערים</small></div>
<div class="face"><div class="mono">228 · 17 · 1</div><small>IBM Plex Mono 500 · 11 עד 13 פיקסלים · המספר בתוך העיגול, טורים מיושרים כמו בגיליון מדידה</small></div>
</div>
<p class="why">למה זה לא המראה הרגיל: הצבעים הם צבעי הים והדיו של הדף עצמו (יומן המתחמים והגרפים לידו), כמו מפת מדידה. אין פליז, זהב, קרם או מעבר צבע. המספרים במונו כמו בגיליון מדידה, והשם יושב עם הילה של קרטוגרף ולא בתוך גלולה.</p>

<div class="sec">05 · ההוכחה: מדידה אוטומטית בדף החי (''' + R['at_utc'] + ''')</div>
<div class="tables">''' + ''.join(tables) + '''</div>
<div style="margin-top:14px">''' + ctab + '''</div>

<div class="sec">06 · הכללים של הטובים בעולם, ואיך הם מתקיימים כאן</div>
<ul class="rules">
<li><b>בלי התנגשויות</b> (Google Maps, Mapbox): שם מוצג רק אם יש לו מקום פנוי, הגדולים קודם. נמדד: 0 חפיפות בכל זום וברוחב.</li>
<li><b>איחוד לפי זום</b> (Mapbox clusters, Zillow, Redfin, מדלן): ערים צמודות מדי לעיגול אחד עם הסכום, הקשה מקרבת אליהן.</li>
<li><b>טקסט עם הילה</b> (Google, NYT): דיו כהה עם הילה לבנה, 16.59:1, מעל AAA.</li>
<li><b>גודל לפי כמות</b> (FT Visual Vocabulary, Mapbox): שטח העיגול גדל עם מספר המתחמים.</li>
<li><b>מספרים במונו</b> (גיליונות מדידה, NYT): IBM Plex Mono בתוך העיגול.</li>
<li><b>יעד הקשה</b> (Apple 44, WCAG 2.5.8): 44 פיקסלים במגע, 24 בעכבר, ואף פעם לא חופפים.</li>
<li><b>שם אחד למקום</b>: השם של המפה עצמה מוסתר כשהתווית שלנו כבר אומרת אותו, ושמות המפה בעברית.</li>
<li><b>שם ליד העיגול שלו</b>: כל שם קרוב לעיגול שלו יותר מלכל עיגול אחר. נמדד: 0 שמות דו משמעיים.</li>
</ul>
</div>
</body>
</html>
'''
open(os.path.join(DS, 'preview.html'), 'w', encoding='utf-8', newline='\n').write(page)
print('preview.html', len(page.encode('utf-8')), 'bytes')
