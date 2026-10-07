# -*- coding: utf-8 -*-
"""Writes docs/design/area-map-3d/component-preview.html: the AreaMap section from render_map.html() + CSS + JS,
twice on one page (full width, then inside a 390px phone frame), below a stand-in for the page above it, so the
lazy loading can be seen and tested. python build_preview.py"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_map  # noqa: E402

OUT = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'docs', 'design', 'area-map-3d', 'component-preview.html'))
d = render_map.load('rova-4')

amx = """
.amx{font-family:Assistant,"Segoe UI",Arial,sans-serif;background:#f7f6f2;padding:24px 0 60px;color:#14212b;margin:0}
.amx-note{max-width:1240px;margin:0 auto 10px;padding:0 24px;font-size:13px;color:#3b4753}
.amx-ctx{max-width:1240px;margin:0 auto;padding:0 24px;display:grid;gap:12px}
.amx-h1{font-family:"Noto Serif Hebrew",Georgia,serif;font-weight:600;font-size:34px;line-height:1.2;margin:0}
.amx-lead{margin:0;font-size:17px;line-height:1.7;color:#3b4753;max-width:72ch}
.amx-block{height:1100px;border-radius:22px;background:#fff;border:1px solid #e3e1da;display:grid;place-items:center;color:#3b4753;font-weight:600}
.amx-gap{max-width:1240px;margin:28px auto 0;padding:0 24px}
.amx-gap div{height:1000px;border-radius:22px;background:#1f4b5c;color:#f7f6f2;display:grid;place-items:center;font-weight:600}
.amx-phone{width:390px;max-width:100%;margin:24px auto 0;border:10px solid #14212b;border-radius:38px;overflow:hidden;background:#f7f6f2;padding:14px 0 24px}
.amx-phone .nlam{padding:0 16px !important}
body{margin:0;background:#f7f6f2}
"""

doc = ('<!-- @dsCard group="Maps" height=3600 width=1280 subtitle="מפת רובע לעמוד אזור ולעמוד פרויקט: הפרויקטים באתר, ההתחדשות '
       'העירונית ומה שיש בשכונה, נטענת רק כשמגיעים אליה" -->\n<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8">'
       '<meta name="viewport" content="width=device-width, initial-scale=1"><title>AreaMap</title>'
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@500;600;700&amp;family=Assistant:wght@400;600;700&amp;display=swap">'
       '<style>' + amx + render_map.CSS + '</style></head><body><div class="amx">'
       '<p class="amx-note">רכיב AreaMap. במחשב: הסקשן יושב מתחת למחירון של רובע 4. עד שמגיעים אליו לא נטען שום דבר כבד: לא הספרייה, לא האריחים.</p>'
       '<div class="amx-ctx"><h1 class="amx-h1">רובע 4 בתל אביב: הצפון החדש, הגבולות, התוכנית ומחירי הדירות</h1>'
       '<p class="amx-lead">(פסקת הפתיחה של העמוד, בלי שינוי.)</p><div class="amx-block">המחירון והמחשבון של רובע 4, בלי שינוי</div></div>' +
       render_map.html(d, '-d') +
       '<div class="amx-gap"><div>המשך העמוד: כיכר המדינה והמגדלים, התחדשות עירונית, תחבורה</div></div>'
       '<p class="amx-note" style="margin-top:32px">בטלפון (מסגרת של 390 פיקסלים): אותו סקשן, הכרטיס נפתח מלמטה, וגלילה באצבע אחת ממשיכה בעמוד.</p>'
       '<div class="amx-phone">' + render_map.html(d, '-ph') + '</div></div>'
       '<script>' + render_map.JS + '</script></body></html>\n')
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(doc)
print('wrote', OUT, len(doc.encode('utf-8')), 'bytes')
