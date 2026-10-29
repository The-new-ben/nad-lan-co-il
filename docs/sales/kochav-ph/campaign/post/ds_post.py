# -*- coding: utf-8 -*-
"""Design-system card for the Kochav organic post (29.10.2026), written into the local copy of the design-system artifact and
published with the Artifact tool: the frames as built (cover, cards, Reels frames), the palette and faces, the rules.
  python ds_post.py"""
import base64, io, os, subprocess
from PIL import Image
import imageio_ffmpeg
H = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(H, "out")
DS = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components\KochavSocialPost"
FF = imageio_ffmpeg.get_ffmpeg_exe()


def b64(im, maxw=520):
    im = im.convert("RGB")
    if im.width > maxw: im = im.resize((maxw, int(im.height * maxw / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=80); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def frame(video, t):
    p = os.path.join(H, "_frame.png")
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(t), "-i", video, "-frames:v", "1", p], check=True)
    im = Image.open(p).copy(); os.remove(p); return im


figs = []
for lang, cap in (("he", "עברית: תמונת הפוסט 4:5"), ("en", "English: cover 4:5"), ("fr", "Français : couverture 4:5"), ("ru", "Русский: обложка 4:5")):
    figs.append((b64(Image.open(os.path.join(O, lang, "cover-4x5.jpg"))), cap))
for i, cap in ((1, "כרטיס 1: המרפסת, צולם בדירה"), (4, "כרטיס 4: התוכנית, מסומנת הדמיה"), (6, "כרטיס 6: המתווכת והרישיון")):
    figs.append((b64(Image.open(os.path.join(O, "he", "card-%d.jpg" % i))), cap))
reel = os.path.join(O, "he", "reel-9x16.mp4")
if os.path.exists(reel):
    for t, cap in ((1.5, "רילס 0:01, הוו בשלוש השניות הראשונות"), (9.0, "רילס 0:09, צילום מהדירה"), (22.0, "רילס 0:22, כרטיס הסיום")):
        figs.append((b64(frame(reel, t), 360), cap))
cards = "".join('<figure><img src="%s" alt="%s"><figcaption>%s</figcaption></figure>' % (s, c, c) for s, c in figs)
PAL = [("#14212B", "ink", "רצועות, רקע"), ("#1F4B5C", "deep", "כפתורים"), ("#2F6F86", "sea", "סימון"), ("#8FC1D4", "sea light", "שורת קטגוריה, פס התקדמות"),
       ("#C9D6DE", "mist", "שורות משנה"), ("#7FD1AE", "real dot", "נקודת צולם בדירה")]
pal = "".join('<div class="sw"><i style="background:%s"></i><b>%s</b><code>%s · %s</code></div>' % (h, n, h, u) for h, n, u in PAL)
HTML = ('<!-- @dsCard group="Campaigns" height=2600 subtitle="פוסט אורגני לפייסבוק, כוכב הצפון: רילס, פיד, תמונה וקרוסלה בעברית, אנגלית, צרפתית ורוסית" -->\n'
        '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>KochavSocialPost</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&amp;family=Noto+Serif+Hebrew:wght@600&amp;display=swap">'
        '<style>:root{--ink:#14212B;--ink2:#3E4C58;--line:#D3DCE2;--sea:#2F6F86;--ground:#F4F7F8}'
        'body{margin:0;background:var(--ground);color:var(--ink2);font-family:Assistant,"Segoe UI",Arial,sans-serif}'
        '.w{max-width:1120px;margin:0 auto;padding:20px max(16px,env(safe-area-inset-left,0px)) 40px}'
        'h1{font:600 26px/1.3 "Noto Serif Hebrew",Georgia,serif;color:var(--ink);margin:0 0 6px;text-wrap:balance}p{font:400 15.5px/1.7 Assistant,sans-serif;max-width:74ch}'
        '.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;align-items:start}'
        'figure{margin:0;background:#fff;border:1px solid var(--line);border-radius:10px;padding:8px}img{display:block;width:100%%;height:auto;border-radius:6px}'
        'figcaption{font:700 13.5px/1.5 Assistant,sans-serif;color:var(--ink);margin-top:6px}'
        '.sec{font:700 12.5px Assistant,sans-serif;letter-spacing:.04em;color:var(--sea);margin:26px 0 10px;border-top:1px solid var(--line);padding-top:8px}'
        '.pal{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}.sw{background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden}'
        '.sw i{display:block;height:40px}.sw b{display:block;font:700 13px Assistant;color:var(--ink);padding:6px 8px 0}.sw code{display:block;font:500 12px ui-monospace,Consolas,monospace;color:#5E6A75;padding:0 8px 8px}'
        '.why{border-inline-start:3px solid var(--sea);background:#fff;padding:10px 14px;font:600 14.5px/1.65 Assistant,sans-serif;color:var(--ink)}'
        'ul{margin:0;padding-inline-start:20px;font:400 15px/1.75 Assistant,sans-serif}</style></head><body><div class="w">'
        '<h1>כוכב הצפון: הפוסט האורגני לפייסבוק</h1><p>רילס 9:16 ופיד 4:5 מהצילומים והסרטון של מיטל, תמונת פוסט 4:5 וקרוסלה של שישה כרטיסים, בארבע שפות. '
        'כל מילה מהדף החי: 76 מ״ר מרפסות, חדר כושר וחדר דיירים, בלי מחיר למטר, המתווכת והרישיון על כל פריים סיום.</p>'
        '<div class="sec">01 · כפי שנבנה (29.10.2026)</div><div class="g">%s</div>'
        '<div class="sec">02 · החוקים</div><ul>'
        '<li>רק צילומים אמיתיים מהדירה ומהנכס. התוכנית מסומנת "הדמיה על פי תוכנית האדריכל". אין סצנות מצוירות בפוסט.</li>'
        '<li>ברילס, הטקסט החשוב בין 14%% מלמעלה ל-35%% מלמטה (האזור שהאפליקציה לא מכסה). ההוק במסגרת הראשונה: 76 מ״ר של מרפסות.</li>'
        '<li>טקסט לצפייה בלי קול: כל שורה כתובה על המסך, המוזיקה רקע בלבד.</li>'
        '<li>כרטיס הסיום: לתיאום צפייה פרטית, מיטל קציר, הטלפון, בלעדיות ורישיון תיווך 3131540 (חובה לפי כללי האתיקה למתווכים).</li>'
        '<li>הקישור בתגובה הראשונה, לא בגוף הפוסט, עם קוד מעקב לכל שפה.</li></ul>'
        '<div class="sec">03 · צבעים וגופנים</div><div class="pal">%s</div>'
        '<p style="margin-top:12px">Noto Serif Hebrew 600 לכותרות בעברית, Noto Serif לכותרות בלטינית ובקירילית, Assistant ו-Noto Sans לטקסט.</p>'
        '<p class="why">למה זה לא המראה הרגיל: הצבעים הם של דף הנכס ושל גיליון התוכנית (דיו כהה, כחול ים, קו מסומן), הצילומים של מיטל עושים את היוקרה, '
        'ואין זהב, קרם, מעבר צבע או אימוג׳י. אותו מראה כמו הדף שאליו הקישור מוביל, כך שהקורא מזהה אותו מיד.</p>'
        '</div></body></html>') % (cards, pal)
README = ("# KochavSocialPost\n\nThe organic Facebook post for the Kochav HaTzafon mini penthouse (29.10.2026): Reels 9:16 and feed 4:5 videos from "
          "Meital's own photos and footage, a 4:5 cover and a six-card set, in Hebrew, English, French and Russian. Text in the Reels safe zone, "
          "sound-off captions, the broker and licence on the end card, the link in the first comment. Source: docs/sales/kochav-ph/campaign/post/ "
          "(post_copy.py words, build.py frames and videos, post_text.py the post).\n")
os.makedirs(DS, exist_ok=True)
io.open(os.path.join(DS, "preview.html"), "w", encoding="utf-8").write(HTML)
io.open(os.path.join(DS, "README.md"), "w", encoding="utf-8").write(README)
print("KochavSocialPost", os.path.getsize(os.path.join(DS, "preview.html")) // 1024, "KB")
