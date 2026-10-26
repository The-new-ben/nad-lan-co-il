"""Builds the Claude Design board card RenewalMapV2 (26.10.2026): a self-contained preview.html (static tags drawn with the
patch's own CSS, the proof screenshots embedded as JPEG data, palette, faces, the proof table) and README.md, into the design
system folder in the scratchpad. Not published (the owner's session publishes it).

    python ds_build2.py
"""
import base64
import io
import json
import os
import re
import sys

from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
DS = r'C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components\RenewalMapV2'
os.makedirs(DS, exist_ok=True)
R = json.load(open(os.path.join(HERE, 'proof-results.json'), encoding='utf-8'))
css = open(os.path.join(HERE, 'src', 'style.css.txt'), encoding='utf-8').read()
css = css[css.find('<style>') + 7:css.rfind('</style>')]


def img(name, w=900, crop=None):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return ''
    im = Image.open(p).convert('RGB')
    if crop:
        im = im.crop(crop)
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, 'JPEG', quality=84, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


def L(c):
    v = []
    for x in (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)):
        x /= 255
        v.append(x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4)
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def cr(a, b):
    x, y = L(a), L(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


V = R['views']


def st(v, m, z):
    return V[v][m]['states'][z]


def strip(st_):  # stage counts -> strip spans, most advanced first (right side in RTL)
    sc = ["#D3DCE2", "#9DB7C3", "#5C93A8", "#2F6F86", "#1F4B5C", "#12202A"]
    return ''.join('<i style="flex:%d 0 0;background:%s"></i>' % (st_[s], sc[s]) for s in (5, 4, 3, 2, 1, 0) if st_[s])


JLM = [39, 0, 95, 74, 7, 0]   # Jerusalem on the authority map, 25.10.2026 (tracker file)
RG = [15, 2, 31, 32, 0, 0]    # Ramat Gan
TLV = [18, 4, 3, 26, 5, 0]    # Tel Aviv-Yafo


def tag(t, name, f=(), sd='n', st_=None, extra='', x=0, y=0, d=0):
    """a tag drawn with the patch's own classes, anchored at its city point (x, y); the board script places it like the map does"""
    inner = '<span class="nm">%s</span>' % name + ''.join('<span class="f">%s</span>' % s for s in f) + ('<span class="sb">%s</span>' % strip(st_) if st_ else '')
    return ('<div class="nlurm-lb demo" style="position:absolute;left:%dpx;top:%dpx" data-sd="%s" data-d="%d"><i class="ld"></i><span class="dt"></span>'
            '<button type="button" class="tg t%s is-%s %s">%s</button></div>' % (x, y, sd, d, t, sd, extra, inner))


BOARD_JS = """<script>(function(){function go(){[].forEach.call(document.querySelectorAll('.demo'),function(m){var b=m.querySelector('.tg'),w=b.offsetWidth,h=b.offsetHeight,sd=m.getAttribute('data-sd'),d=+m.getAttribute('data-d'),g=b.classList.contains('tS')?7:11,l,t;
if(sd==='n'){l=-w/2;t=-g-h}else if(sd==='s'){l=-w/2;t=g}else if(sd==='w'){l=-g-w;t=-h/2}else if(sd==='e'){l=g;t=-h/2}else{l=-d-w;t=-h/2;var ld=m.querySelector('.ld');ld.style.cssText='display:block;width:'+d+'px;transform:rotate(3.14159rad)'}
b.style.left=Math.round(l)+'px';b.style.top=Math.round(t)+'px'})}
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(go);else go();window.addEventListener('load',go)})();</script>"""


rows = []
for v in ('390', '1280'):
    for z, zl in (('country', 'כל הארץ (התצוגה הראשונה)'), ('central', 'מרכז הארץ'), ('tlv', 'אזור תל אביב')):
        b, a = st(v, 'before', z), st(v, 'after', z)
        rows.append((v, zl, b, a))


def tr(v, zl, b, a):
    def row(lab, s, strong):
        c = '%s:1 / %s:1' % (min(s['contrast_text']), min(s['contrast_facts'])) if s['contrast_text'] else '-'
        cells = [v, zl, lab, s['names_n'], s['facts'], s['facts_per_tag'], s['overlaps'], '<bdi class="n">%s</bdi>' % c, '<bdi class="n">%gx%g</bdi>' % (s['tap_min_w'], s['tap_min_h'])]
        return '<tr%s>' % (' style="font-weight:600"' if strong else '') + ''.join('<td>%s</td>' % x for x in cells) + '</tr>'
    return row('היום', b, False) + row('הצעה', a, True)


ia = V['1280']['after']['interactions']
ip = V['390']['after']['interactions']
pal = [('ink', '#12202A', 'שמות, מספרים'), ('ink2', '#3E4C58', 'שורות העובדות, קווי חיבור'), ('deep', '#1F4B5C', 'מספרים בתווית, עיר נבחרת, כפתור ראשי'),
       ('sea', '#2F6F86', 'שלב "מאושרת" בפס, לא לטקסט'), ('line', '#D3DCE2', 'גבולות, "ללא שלב" בפס'), ('red', '#C42550', 'אזהרה בלבד: מתחם שלא במפת הרשות היום')]
sw = ''.join('<div class="sw"><i style="background:%s"></i><b>%s <span class="n">%s</span></b><span>%s</span><span class="n">%s</span></div>'
             % (h, n, h, u, ('%.2f:1 על לבן' % cr(h, '#FFFFFF'))) for n, h, u in pal)
modes = ''.join('<figure><img src="%s" alt=""><figcaption>%s</figcaption></figure>' % (img('after-1280-mode-%s.png' % m, 520), t)
                for m, t in (('all', 'מתחמים'), ('ap', 'תכניות מאושרות'), ('un', 'דירות חדשות'), ('px', 'מחירי דירות'), ('mv', 'מה זז')))
page = '''<!-- @dsCard group="Tools" height=5200 subtitle="מפת ההתחדשות v2: תוויות סקר שנושאות עובדות (שם, מתחמים, מאושרות, טווח מחירים, פס שלבים), צ'יפים שמחליפים את מה שהתוויות אומרות, לוח ערים לצד המפה, הים כשוליים לתוויות" -->
<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RenewalMapV2</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<style>
:root{--ground:#F4F7F8;--paper:#FFFFFF;--ink:#12202A;--ink2:#3E4C58;--line:#D3DCE2;--sea:#2F6F86;--deep:#1F4B5C;--red:#C42550;--wash:#EEF3F5;--land:#F1F3F2;--water:#DCE6EA}
body{margin:0;background:var(--ground);font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif;color:var(--ink2)}
.w{max-width:1080px;margin:0 auto;padding:20px 16px 48px}
h1{font:600 26px/1.25 "IBM Plex Sans Hebrew";color:var(--ink);margin:0 0 6px}
.lead{font:400 15px/1.7 "IBM Plex Sans Hebrew";max-width:76ch;margin:0 0 8px}
.sec{font:500 12px/16px "IBM Plex Mono",monospace;color:var(--ink2);margin:30px 0 10px;border-top:1px solid var(--line);padding-top:8px;letter-spacing:.02em}
.why{background:var(--paper);border:1px solid var(--line);border-right:3px solid var(--deep);padding:10px 14px;font:400 14px/1.6 "IBM Plex Sans Hebrew";color:var(--ink);margin:10px 0}
.n{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums}
.board{position:relative;height:430px;background:linear-gradient(90deg,var(--water) 0 34%,var(--land) 34% 100%);border:1px solid var(--line);overflow:hidden}
.board .coast{position:absolute;top:0;bottom:0;left:34%;width:1px;background:#B9C7CE}
.board .pt{position:absolute;width:8px;height:8px;margin:-4px 0 0 -4px;border-radius:50%;background:#1F4B5C;box-shadow:0 0 0 1.5px #fff}
.board .pt.z{width:6px;height:6px;margin:-3px 0 0 -3px;background:#8C99A4}
.board .ld{position:absolute;height:1px;background:#3E4C58;transform-origin:0 50%}
.board .cap{position:absolute;font:500 12px/1.4 "IBM Plex Sans Hebrew";color:var(--ink2);background:rgba(255,255,255,.85);padding:2px 6px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.grid5{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}
figure{margin:0;background:var(--paper);border:1px solid var(--line);padding:6px}figure img{display:block;width:100%;height:auto}
figcaption{font:500 13px/1.5 "IBM Plex Sans Hebrew";color:var(--ink);margin:6px 2px 2px}figcaption span{display:block;font:400 12px "IBM Plex Sans Hebrew";color:var(--ink2)}
.pal{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.sw{background:var(--paper);border:1px solid var(--line);padding:0 0 8px;display:flex;flex-direction:column;gap:2px;font-size:12.5px}.sw i{display:block;height:44px;margin-bottom:6px}.sw b,.sw span{padding:0 10px}.sw b{color:var(--ink)}
table{border-collapse:collapse;width:100%;background:var(--paper);font:400 13px/1.5 "IBM Plex Sans Hebrew"}th,td{border:1px solid var(--line);padding:6px 8px;text-align:right;vertical-align:top}th{background:var(--wash);color:var(--ink);font-weight:600}td{color:var(--ink)}
.faces{display:grid;grid-template-columns:1fr 1fr;gap:12px}.face{background:var(--paper);border:1px solid var(--line);padding:12px}.face b{display:block;font:600 22px "IBM Plex Sans Hebrew";color:var(--ink)}.face .m{font:500 22px "IBM Plex Mono";color:var(--deep)}
@media (max-width:760px){.grid2,.grid3,.faces{grid-template-columns:1fr}.grid5{grid-template-columns:1fr 1fr}.board{height:520px}}
''' + css.replace('html body .nlurm-v2', '.nlurm-v2') + '''
.board .nlurm-lb{position:absolute;width:0;height:0}.board .nlurm-lb .tg{position:absolute}
</style>
</head>
<body>
<main class="w">
<h1>RenewalMapV2 · מפת ההתחדשות העירונית</h1>
<p class="lead">התוויות של <span class="n">/urban-renewal/map/</span> מחדש, אחרי שבן דחה את העיגולים עם המספרים (26.10.2026). כל עיר מקבלת תווית קטנה שאפשר לקרוא מרחוק: השם, ומתחתיו העובדות שהצ'יפים בוחרים, ופס דק של שלבי המתחמים. ריחוף עכבר מציג תקציר עם שמות מתחמים, הקשה פותחת את העיר בלוח שליד המפה (בטלפון: כרטיס בתחתית המפה והלוח מתחתיה) עם מקור ותאריך לכל מספר ועם כל המתחמים. הצעה מקומית בלבד, לא באתר.</p>
<div class="why"><b>למה זה לא המראה הרגיל של בינה מלאכותית:</b> הצורה לקוחה מתוויות של תשריט ומפת מדידה (פינות ישרות, פס שלבים בתחתית, מספרים בגופן מונו כמו בגיליון מדידה), הצבעים הם צבעי הים והדיו של בלוק הנתונים בעמוד עצמו, והים משמש שוליים לתוויות כמו בהערות על מפת חוף. בלי זהב, קרם, טרקוטה או סגול, בלי כרטיס רך עם צל שחוזר על עצמו.</div>

<p class="sec">01 · התווית: מבנה ומצבים</p>
<div class="nlurm-v2" style="border:0;background:none">
<div class="board">
  <div class="coast"></div>
  <span class="cap" style="right:8px;top:8px">יבשה</span><span class="cap" style="left:8px;top:8px">ים: שוליים לתוויות</span>
  ''' + tag('L', 'ירושלים', ('<b class="n">215</b> מתחמים · <b class="n">81</b> מאושרות', '3-5 חד׳ · <b class="n">2.4-3.9</b> מיליון ₪'), 'n', JLM, x=700, y=128) + '''
  <span class="cap" style="left:590px;top:142px">L: שם, שתי עובדות ופס שלבים, כשיש מקום</span>
  ''' + tag('M', 'רמת גן', ('<b class="n">80</b> מתחמים · <b class="n">32</b> מאושרות',), 'n', RG, x=940, y=128) + '''
  <span class="cap" style="left:880px;top:142px">M: שם ועובדה אחת</span>
  ''' + tag('S', 'קרית אונו', (), 'w', None, x=700, y=236) + '''
  <span class="cap" style="left:600px;top:256px">S: השם לבד, עם הילה לבנה</span>
  <div class="nlurm-lb is-zero demo-pt" style="position:absolute;left:900px;top:236px"><span class="dt"></span></div><span class="cap" style="left:850px;top:256px">נקודה: מחכה לזום</span>
  ''' + tag('L', 'תל אביב יפו', ('<b class="n">56</b> מתחמים · <b class="n">31</b> מאושרות', '3-5 חד׳ · <b class="n">4.2-7.5</b> מיליון ₪'), 'c', TLV, x=420, y=300, d=64) + '''
  <span class="cap" style="left:30px;top:350px">תווית בים: קו דק עד העיר, כשאין מקום ליד הנקודה</span>
  ''' + tag('M', 'רמת גן', ('<b class="n">80</b> מתחמים · <b class="n">32</b> מאושרות',), 'n', RG, 'is-on', x=940, y=392) + '''
  <span class="cap" style="left:880px;top:404px">נבחרה (פתוחה בלוח)</span>
  ''' + tag('M', 'חולון', ('<b class="n">27</b> מתחמים · <b class="n">11</b> מאושרות',), 'n', [6, 4, 6, 11, 0, 0], 'is-hi', x=700, y=392) + '''
  <span class="cap" style="left:620px;top:404px">ריחוף, או שורה מסומנת ברשימה</span>
</div>
</div>
<p class="lead" style="margin-top:8px">פס השלבים (מימין לשמאל): <span style="color:#1F4B5C">■</span> במימוש · <span style="color:#2F6F86">■</span> תכנית מאושרת · <span style="color:#5C93A8">■</span> תכנון סטטוטורי · <span style="color:#9DB7C3">■</span> תכנון ראשוני · <span style="color:#D3DCE2">■</span> ללא שלב. האורך של כל צבע הוא חלק המתחמים בעיר באותו שלב, לפי מפת הרשות (25.10.2026).</p>

<p class="sec">02 · שלושה זומים, טלפון ומחשב (צילומים מהעמוד החי עם הבלוק המוחלף, בדפדפן מקומי)</p>
<div class="grid3">
<figure><img src="''' + img('after-390-country.png', 420) + '''" alt=""><figcaption>טלפון · כל הארץ</figcaption></figure>
<figure><img src="''' + img('after-390-central.png', 420) + '''" alt=""><figcaption>טלפון · מרכז</figcaption></figure>
<figure><img src="''' + img('after-390-tlv.png', 420) + '''" alt=""><figcaption>טלפון · תל אביב</figcaption></figure>
</div>
<div class="grid3" style="margin-top:12px">
<figure><img src="''' + img('after-1280-country.png', 620) + '''" alt=""><figcaption>מחשב · כל הארץ</figcaption></figure>
<figure><img src="''' + img('after-1280-central.png', 620) + '''" alt=""><figcaption>מחשב · מרכז</figcaption></figure>
<figure><img src="''' + img('after-1280-tlv.png', 620) + '''" alt=""><figcaption>מחשב · תל אביב</figcaption></figure>
</div>

<p class="sec">03 · ריחוף, הקשה, לוח, חיפוש</p>
<div class="grid2">
<figure><img src="''' + img('after-1280-hover.png', 900) + '''" alt=""><figcaption>ריחוף עכבר: תקציר העיר עם שלושת המתחמים המתקדמים<span>הלוח מימין: הערים שבתצוגה, מסודרות לפי הצ'יפ</span></figcaption></figure>
<figure><img src="''' + img('after-1280-city.png', 900) + '''" alt=""><figcaption>לחיצה: העיר בלוח<span>מקור ותאריך לכל מספר, כפתור ליומן המתחמים, כל המתחמים עם שלב, דירות ושינוי אחרון</span></figcaption></figure>
</div>
<div class="grid3" style="margin-top:12px">
<figure><img src="''' + img('after-390-peek.png', 420) + '''" alt=""><figcaption>טלפון: כרטיס בתחתית המפה<span>הלוח המלא מתחת למפה, הגלילה של העמוד לא נעצרת</span></figcaption></figure>
<figure><img src="''' + img('after-390-city.png', 420, (0, 0, 780, 2300)) + '''" alt=""><figcaption>טלפון: העיר והמתחמים</figcaption></figure>
<figure><img src="''' + img('after-390-search.png', 420) + '''" alt=""><figcaption>חיפוש מתחם לפי שם (גניש)</figcaption></figure>
</div>

<p class="sec">04 · הצ'יפים מחליפים את מה שהתוויות אומרות (מחשב, כל הארץ)</p>
<div class="grid5">''' + modes + '''</div>

<p class="sec">05 · צבעים וגופנים</p>
<div class="pal">''' + sw + '''</div>
<div class="faces" style="margin-top:10px"><div class="face"><b>IBM Plex Sans Hebrew 600 / 500 / 400</b><span>שמות ערים, שורות עובדות, כפתורים</span></div><div class="face"><span class="m">215 · 2.4-3.9 · 25.10.2026</span><br><span>IBM Plex Mono 500: כל מספר</span></div></div>

<p class="sec">06 · ההוכחה (היום / ההצעה, אותו עמוד חי, אותו רגע: ''' + R['at_utc'] + ''')</p>
<table><thead><tr><th>רוחב</th><th>זום</th><th></th><th>שמות קריאים</th><th>עובדות על המסך</th><th>עובדות לתווית</th><th>חפיפות</th><th>ניגודיות מינימלית: שמות / עובדות</th><th>מטרת הקשה הקטנה</th></tr></thead><tbody>
''' + ''.join(tr(*r) for r in rows) + '''
</tbody></table>
<p class="lead" style="margin-top:8px">פירוט מלא, כל הלחיצות, הגלילה בטלפון וזמני הטעינה: <span class="n">labels/v2/PROOF.md</span> במאגר.</p>

<p class="sec">07 · היום מול ההצעה, טלפון</p>
<figure><img src="''' + img('compare-phone.png', 1000) + '''" alt=""></figure>
</main>
''' + BOARD_JS + '''
</body>
</html>
'''
page = page.replace('html body .nlurm-v2', '.nlurm-v2')
open(os.path.join(DS, 'preview.html'), 'w', encoding='utf-8', newline='\n').write(page)
print('preview.html', len(page.encode('utf-8')), 'bytes')
