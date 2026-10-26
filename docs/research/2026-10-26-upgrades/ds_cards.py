# -*- coding: utf-8 -*-
"""Design-system board cards for round 2 pages, built from screenshots that were looked at (26.10.2026): a short card per component
with the real renders, the palette and the faces. The agents' full previews stay local as preview-agent.html.
  python docs/research/2026-10-26-upgrades/ds_cards.py SdeDovHub DiraBehanacha"""
import base64, io, os, shutil, sys
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
DS = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components"
CARDS = {
    "SdeDovHub": {
        "title": "רובע שדה דב: כל מגרש, מי זכה, ובאיזה שלב",
        "sub": "הדף של רובע שדה דב: פסקת תשובה מתחת לכותרת, כפתורים, ואז הכלי שרק לנו יש: 73 המגרשים בשלוש התכניות, מכרזי רשות מקרקעי ישראל, השלב הרשמי בעירייה, תחנת הקו הירוק והמרחק מהים.",
        "shots": [("s1-sde-dov/preview/shots/390-first-screen.png", "טלפון: הכותרת, פסקת התשובה והכפתורים"),
                  ("s1-sde-dov/preview/shots/1280-tool-merkaz.png", "מחשב: מרכז הרובע, כל מגרש לפי השלב, התחנות והים"),
                  ("s1-sde-dov/preview/shots/390-tool-district.png", "טלפון: כל הרובע, ספירה לפי שלב וטבלה")],
    },
    "DiraBehanacha": {
        "title": "דירה בהנחה (מחיר למשתכן): זכאות, הגרלות וסיכוי בכל עיר",
        "sub": "הדף של דירה בהנחה: פסקת תשובה, שלושה כפתורים, בדיקת הזכאות והעיר שנותנת הכי הרבה דירות לכל 100 נרשמים, ובדיקת עלות מול מחיר העסקאות בעיר.",
        "shots": [("g1-dira-behanacha/preview/shots/page-390-top.png", "טלפון: הכותרת, פסקת התשובה והכפתורים"),
                  ("g1-dira-behanacha/preview/shots/dirafit-390.png", "טלפון: בדיקת הזכאות והערים"),
                  ("g1-dira-behanacha/preview/shots/fig1-390.png", "איור: דירות לכל 100 נרשמים בעיר, ההגרלה ה־11")],
    },
}
PAL = [("#12202A", "ink", "טקסט וכותרות"), ("#1F4B5C", "deep", "כפתור ראשי, שלב מתקדם"), ("#2F6F86", "sea", "נקודה, טבעת, קישור"),
       ("#D3DCE2", "line", "קווים ומסגרות"), ("#C42550", "survey red", "רק לאזהרה או מכרז פתוח")]


def img64(rel, maxw=760):
    im = Image.open(os.path.join(H, rel)).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def card(name, c):
    figs = "".join('<figure><img src="%s" alt="%s"><figcaption>%s</figcaption></figure>' % (img64(p), cap, cap) for p, cap in c["shots"])
    pal = "".join('<div class="sw"><i style="background:%s"></i><b>%s</b><code>%s · %s</code></div>' % (h, n, h, use) for h, n, use in PAL)
    return ('<!-- @dsCard group="Tools" height=2600 subtitle="%s" -->\n<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1"><title>%s</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;600&amp;family=IBM+Plex+Mono:wght@500&amp;display=swap">'
            '<style>:root{--ink:#12202A;--ink2:#3E4C58;--line:#D3DCE2;--sea:#2F6F86;--deep:#1F4B5C;--ground:#F6F8F9}body{margin:0;background:var(--ground);color:var(--ink2);font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif}'
            '.w{max-width:1040px;margin:0 auto;padding:20px 16px 40px}h1{font:600 24px/1.3 "IBM Plex Sans Hebrew";color:var(--ink);margin:0 0 6px}p{font:400 15px/1.7 "IBM Plex Sans Hebrew";max-width:72ch}'
            '.g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;align-items:start}figure{margin:0;background:#fff;border:1px solid var(--line);border-radius:6px;padding:8px}'
            'img{display:block;width:100%%;height:auto;border-radius:4px}figcaption{font:600 13px/1.5 "IBM Plex Sans Hebrew";color:var(--ink);margin-top:6px}'
            '.sec{font:500 12px "IBM Plex Mono",monospace;color:#5E6A75;margin:26px 0 10px;border-top:1px solid var(--line);padding-top:8px}'
            '.pal{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}.sw{background:#fff;border:1px solid var(--line);border-radius:6px;overflow:hidden}'
            '.sw i{display:block;height:40px}.sw b{display:block;font:600 13px "IBM Plex Sans Hebrew";color:var(--ink);padding:6px 8px 0}.sw code{display:block;font:500 12px "IBM Plex Mono";color:#5E6A75;padding:0 8px 8px}'
            '.why{border-inline-start:3px solid var(--sea);background:#fff;padding:10px 14px;font:500 14px/1.65 "IBM Plex Sans Hebrew";color:var(--ink)}'
            '@media(max-width:760px){.g{grid-template-columns:1fr}}</style></head><body><div class="w"><h1>%s</h1><p>%s</p>'
            '<div class="sec">01 · הדף כפי שנבנה, צילומים מהתצוגה המקומית (26.10.2026)</div><div class="g">%s</div>'
            '<div class="sec">02 · צבעים וגופנים</div><div class="pal">%s</div>'
            '<p style="margin-top:12px">IBM Plex Sans Hebrew 400/600 לטקסט ולכותרות, IBM Plex Mono 500 למספרים ולתאריכים.</p>'
            '<p class="why">למה זה לא המראה הרגיל: צבעי הדיו והים של מכשירי נדלן, כמו גיליון מדידה; אין זהב, קרם או מעבר צבע, המספרים במונו, וכל מספר עם המקור והתאריך שלו.</p>'
            '</div></body></html>') % (c["sub"][:140], name, c["title"], c["sub"], figs, pal)


for name in sys.argv[1:]:
    d = os.path.join(DS, name)
    if os.path.exists(os.path.join(d, "preview.html")) and not os.path.exists(os.path.join(d, "preview-agent.html")):
        shutil.copy(os.path.join(d, "preview.html"), os.path.join(d, "preview-agent.html"))
    io.open(os.path.join(d, "preview.html"), "w", encoding="utf-8").write(card(name, CARDS[name]))
    print(name, os.path.getsize(os.path.join(d, "preview.html")), "bytes")
