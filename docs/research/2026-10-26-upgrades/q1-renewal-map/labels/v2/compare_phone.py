"""compare-phone.png (26.10.2026): today vs the proposal on a phone, three panels, captions in IBM Plex Sans Hebrew rendered by
the browser (correct right-to-left text), numbers read from proof-results.json. Local files only.

    python compare_phone.py
"""
import io
import json
import os
import sys

from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
R = json.load(open(os.path.join(HERE, 'proof-results.json'), encoding='utf-8'))
b = R['views']['390']['before']['states']['country']
a = R['views']['390']['after']['states']['country']
ac = R['views']['390']['after']['states']['central']
bc = R['views']['390']['before']['states']['central']
ci = R['views']['390']['after']['interactions']['city']


def u(n):
    return 'file:///' + os.path.join(HERE, n).replace('\\', '/')


html = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>body{margin:0;background:#F4F7F8;font-family:"IBM Plex Sans Hebrew",sans-serif;color:#12202A}
.w{display:flex;gap:22px;padding:26px 26px 22px;width:max-content}
.p{width:400px;background:#fff;border:1px solid #D3DCE2;padding:12px}
.p h2{margin:0 0 4px;font:600 20px/1.3 "IBM Plex Sans Hebrew"}.p h2 span{display:inline-block;margin-inline-start:8px;padding:1px 8px;font:600 13px/20px "IBM Plex Sans Hebrew";color:#fff;background:#3E4C58;vertical-align:2px}
.p.new h2 span{background:#1F4B5C}
.p p{margin:0 0 10px;font:400 14px/1.55 "IBM Plex Sans Hebrew";color:#3E4C58;min-height:66px}.p p b{color:#12202A;font-weight:600}.n{font-family:"IBM Plex Mono",monospace}
.p img{display:block;width:100%;height:auto}.p .c{max-height:780px;overflow:hidden;border:1px solid #D3DCE2}
.f{padding:0 26px 22px;font:400 13px/1.5 "IBM Plex Sans Hebrew";color:#3E4C58}</style></head><body>
<div class="w">
<div class="p"><h2>היום<span>באתר</span></h2><p>תוויות בצבע זהב עם <b>שם ומספר</b>. במבט הראשון: <b class="n">{}</b> תוויות שנערמות זו על זו (<b class="n">{}</b> חפיפות), <b class="n">{}</b> שמות קריאים, ניגודיות <b class="n">{}:1</b>.</p><div class="c"><img src="{}"></div></div>
<div class="p new"><h2>ההצעה<span>מקומי</span></h2><p>תוויות סקר: שם, מספר המתחמים, ובעיר גדולה גם מאושרות וטווח מחירים, ופס שלבים. <b class="n">{}</b> תוויות בלי אף חפיפה, <b class="n">{}</b> עובדות קריאות על המסך (היום <b class="n">{}</b>), ניגודיות <b class="n">{}:1</b>. ערי החוף הצפופות בים, עם קו.</p><div class="c"><img src="{}"></div></div>
<div class="p new"><h2>הקשה על עיר<span>מקומי</span></h2><p>כרטיס בתחתית המפה עם העובדות וכפתורים, ומתחת למפה כל <b class="n">{}</b> המתחמים של העיר עם שלב, דירות וקישור (היום: <b class="n">8</b> הראשונים). הגלילה בעמוד ממשיכה באצבע אחת.</p><div class="c"><img src="{}"></div></div>
</div>
<div class="f">צילומים מהעמוד החי https://nad-lan.co.il/urban-renewal/map/ ב-'''
vals = (
    b['shown'], b['overlaps'], b['names_n'], min(b['contrast_text']), u('before-390-country.png'),
    a['shown'], a['facts'], b['facts'], min(a['contrast_text']), u('after-390-country.png'),
    ci['rows_all'], u('after-390-city.png'))
TAIL = ''', רוחב 390 פיקסלים. בצד ההצעה הבלוק של המפה הוחלף בדפדפן מקומי בלבד; שום דבר לא עלה לאתר.</div>
</body></html>'''
parts = html.split('{}')
assert len(parts) == len(vals) + 1, (len(parts), len(vals))
html = ''.join(x + (('%.1f' % vals[k]) if isinstance(vals[k], float) else str(vals[k]) if k < len(vals) else '') for k, x in enumerate(parts[:-1])) + parts[-1] + R['at_utc'] + TAIL
p = os.path.join(HERE, 'out', 'compare.html')
open(p, 'w', encoding='utf-8').write(html)
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=CHROME, headless=True, args=['--allow-file-access-from-files'])
    pg = br.new_page(viewport={'width': 1400, 'height': 900}, device_scale_factor=1)
    pg.goto('file:///' + p.replace('\\', '/'))
    pg.evaluate("document.fonts.ready.then(()=>1)")
    pg.wait_for_timeout(1200)
    pg.locator('body').screenshot(path=os.path.join(HERE, 'compare-phone.png'))
    br.close()
print('compare-phone.png written')
