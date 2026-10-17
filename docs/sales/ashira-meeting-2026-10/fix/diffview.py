import difflib, html, re, os
from playwright.sync_api import sync_playwright
b = open('before-he-4744.html', encoding='utf-8').read().splitlines(); a = open('after-he-4744.html', encoding='utf-8').read().splitlines()
rows = []
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, b, a).get_opcodes():
    if tag == 'equal': continue
    old = html.unescape(re.sub(r'<[^>]+>', '', ' '.join(b[i1:i2]))).strip(); new = html.unescape(re.sub(r'<[^>]+>', '', ' '.join(a[j1:j2]))).strip()
    rows.append("<tr><td class=o>%s</td><td class=n>%s</td></tr>" % (html.escape(old), html.escape(new) or '<i>נמחק</i>'))
css = "body{font-family:Heebo,Arial;margin:24px;color:#0E1B24}h1{font-size:22px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #C5D4D1;padding:10px;vertical-align:top;font-size:15px;line-height:1.6;width:50%}th{background:#0E1B24;color:#fff}.o{background:#FBEAEA;text-decoration:line-through;color:#7a2a2a}.n{background:#E8F4EE}"
page = "<!doctype html><html lang=he dir=rtl><meta charset=utf-8><style>%s</style><h1>אשירה, המאמר בעברית (פוסט 4744): מה משתנה. הכותרת, הכתובת וכל השאר נשארים.</h1><table><tr><th>לפני</th><th>אחרי</th></tr>%s</table></html>" % (css, ''.join(rows))
open('preview-he-diff.html', 'w', encoding='utf-8').write(page)
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome"); pg = br.new_page(viewport={"width": 1200, "height": 900})
    pg.goto('file:///' + os.path.abspath('preview-he-diff.html').replace(os.sep, '/')); pg.screenshot(path='preview-he-diff.png', full_page=True); br.close()
print(len(rows), 'changes')
