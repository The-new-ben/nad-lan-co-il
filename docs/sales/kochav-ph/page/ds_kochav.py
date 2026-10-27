# -*- coding: utf-8 -*-
"""Design-system board card for the Kochav listing, round 27.10.2026 (Ben: "אל תעיז לעבוד ללא קלוד דיזיין"): the opening with the price
on the first screen, and the architect's plan section (plan, rendering, room photo), from the live screenshots that were looked at
(shots-27p/, Edge at 390 and 1280). Written into the local copy of the design-system artifact, then published with the Artifact tool.
  python ds_kochav.py"""
import base64, io, os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, "shots-27p")
DS = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components\KochavListing"
SHOTS = [("he-390-first-76.png", "טלפון: התמונות, המחיר והעובדות במסך הראשון (המחיר בגובה 511), 76 מ״ר מרפסות", 1700),
         ("labels-he-390.png", "טלפון: תוכנית הדירה, שמות החדרים קריאים, בלי מידות", None),
         ("he-390-render.png", "טלפון: ההדמיה של התוכנית, החדר שנבחר מסומן, והצילום שלו מהדירה", 2100),
         ("he-1280-kitchen.png", "מחשב: התוכנית ברוחב מלא, החדרים, והצילום ליד שם החדר", 1900),
         ("labels-en-390.png", "English: the same plan with English room names", None)]
PAL = [("#14212B", "ink", "טקסט, מחיר, כפתור נבחר"), ("#1F4B5C", "deep", "וואטסאפ, חדר נבחר"), ("#2F6F86", "sea", "שורת הקטגוריה, סימון החדר"),
       ("#E3E1DA", "line", "מסגרות"), ("#F4F7F8", "surface", "כרטיס החדר")]


def img64(name, crop_h=None, maxw=700):
    im = Image.open(os.path.join(S, name)).convert("RGB")
    if crop_h and im.height > crop_h: im = im.crop((0, 0, im.width, crop_h))
    if im.width > maxw: im = im.resize((maxw, int(im.height * maxw / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


figs = "".join('<figure><img src="%s" alt="%s"><figcaption>%s</figcaption></figure>' % (img64(n, c), cap, cap) for n, cap, c in SHOTS)
pal = "".join('<div class="sw"><i style="background:%s"></i><b>%s</b><code>%s · %s</code></div>' % (h, n, h, u) for h, n, u in PAL)
SUB = ("דף הנכס של מיטל קציר בכוכב הצפון: התמונות שלה, המחיר הגדול והעובדות במסך הראשון, ומתחת לסרט תוכנית הדירה של האדריכל: "
       "תוכנית יוקרתית בלי מידות, מעבר להדמיה, בחירת חדר באצבע אחת והצילום שלו מהדירה.")
HTML = ('<!-- @dsCard group="Pages" height=3400 subtitle="%s" -->\n<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1"><title>KochavListing</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&amp;family=Noto+Serif+Hebrew:wght@600&amp;display=swap">'
        '<style>:root{--ink:#14212B;--ink2:#3E4C58;--line:#E3E1DA;--sea:#2F6F86;--deep:#1F4B5C;--ground:#F4F7F8}'
        'body{margin:0;background:var(--ground);color:var(--ink2);font-family:Assistant,"Segoe UI",Arial,sans-serif}'
        '.w{max-width:1100px;margin:0 auto;padding:20px max(16px,env(safe-area-inset-left,0px)) 40px}'
        'h1{font:600 26px/1.3 "Noto Serif Hebrew",Georgia,serif;color:var(--ink);margin:0 0 6px;text-wrap:balance}p{font:400 15.5px/1.7 Assistant,sans-serif;max-width:72ch}'
        '.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;align-items:start}'
        'figure{margin:0;background:#fff;border:1px solid var(--line);border-radius:10px;padding:8px}img{display:block;width:100%%;height:auto;border-radius:6px}'
        'figcaption{font:700 13.5px/1.5 Assistant,sans-serif;color:var(--ink);margin-top:6px}'
        '.sec{font:700 12.5px Assistant,sans-serif;letter-spacing:.04em;color:var(--sea);margin:26px 0 10px;border-top:1px solid var(--line);padding-top:8px}'
        '.pal{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}.sw{background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden}'
        '.sw i{display:block;height:40px}.sw b{display:block;font:700 13px Assistant;color:var(--ink);padding:6px 8px 0}.sw code{display:block;font:500 12px ui-monospace,Consolas,monospace;color:#5E6A75;padding:0 8px 8px}'
        '.why{border-inline-start:3px solid var(--sea);background:#fff;padding:10px 14px;font:600 14.5px/1.65 Assistant,sans-serif;color:var(--ink)}'
        'ul{margin:0;padding-inline-start:20px;font:400 15px/1.75 Assistant,sans-serif}'
        '@media(max-width:760px){.g{grid-template-columns:1fr}}</style></head><body><div class="w"><h1>מיני פנטהאוז בכוכב הצפון: המסך הראשון ותוכנית הדירה</h1><p>%s</p>'
        '<div class="sec">01 · כפי שעלה לאתר, צילומים מהדף החי (27.10.2026)</div><div class="g">%s</div>'
        '<div class="sec">02 · החוקים של הרכיב</div><ul>'
        '<li>המחיר בשורה משלו במסך הראשון בטלפון (גובה 511, החציון של 13 הדפים המובילים בעולם הוא 534), והעובדות בשורה אחת מתחתיו.</li>'
        '<li>בלי מחיר למטר בדף הזה (מיטל), ובלי מידות בתוכנית: שמות חדרים בלבד, וכיתוב "הדמיה על פי תוכנית האדריכל".</li>'
        '<li>התוכנית מתחת לסרט ולפני גלריית התמונות, והקישור אליה בשורת הקישורים המהירים במסך הראשון.</li>'
        '<li>צילום של חדר מוצג רק אם מיטל צילמה אותו בדירה; ההדמיה היא של התוכנית בלבד, לא של חדרים שכבר צולמו.</li>'
        '<li>הדף נגלל דרך התוכנית: אין לכידת גלגלת, הגדלה בשתי אצבעות, בהקשה כפולה או בכפתורים.</li></ul>'
        '<div class="sec">03 · צבעים וגופנים</div><div class="pal">%s</div>'
        '<p style="margin-top:12px">Noto Serif Hebrew 600 לכותרות ולשם החדר, Assistant 400 עד 800 לטקסט, למחיר ולכפתורים.</p>'
        '<p class="why">למה זה לא המראה הרגיל: הצבעים לקוחים מגיליון של תוכנית אדריכלית (דיו כהה, קווי קיר, כחול ים לסימון), בלי זהב, קרם או מעבר צבע; '
        'הצילומים האמיתיים של מיטל עושים את היוקרה, והתוכנית נראית כמו תוכנית, לא כמו פוסטר.</p>'
        '</div></body></html>') % (SUB[:140], SUB, figs, pal)
README = ("# KochavListing\n\nThe Kochav HaTzafon mini penthouse listing (Meital Katzir), round 27.10.2026: the opening with Meital's photos in a one-finger strip, "
          "the price on its own line on the first screen (y=511 on a 390px phone), the facts row, 'a new home in a new boutique building', WhatsApp and call, "
          "quick links (film, floor plan, location); and under the film the architect's plan: a luxury 2D plan traced from the PDF with room names and no "
          "dimensions, a toggle to the rendering of the plan (Blender, realism pass by gpt-image, checked by edge overlap), a tap on a room highlights it and "
          "shows Meital's own photo of it when one exists, pinch and double tap to zoom, no wheel capture. Hebrew and English. Live on nad-lan.co.il "
          "(posts 7634, 7812). Source of truth: docs/sales/kochav-ph/page/round27.py and round27_plan.py, plan/ for the drawing and the renders.\n")
os.makedirs(DS, exist_ok=True)
io.open(os.path.join(DS, "preview.html"), "w", encoding="utf-8").write(HTML)
io.open(os.path.join(DS, "README.md"), "w", encoding="utf-8").write(README)
print("KochavListing", os.path.getsize(os.path.join(DS, "preview.html")), "bytes")
