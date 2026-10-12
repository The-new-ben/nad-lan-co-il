# -*- coding: utf-8 -*-
"""HAD-495: a short silent pitch film per project (about 50 s, 16:9, Hebrew titles), for WhatsApp and mail.
An HTML timeline (the deck's stills with slow moves, NadLan tokens) recorded by Chrome, then encoded to H.264 MP4.
No voice and no music (no licensed track; the ElevenLabs quota is spent until 21.10). python build_film.py ashira|rainbow"""
import glob
import os
import shutil
import subprocess
import sys

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_deck import P, MEITAL, data_uri  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
key = sys.argv[1]
d = P[key]
im = lambda n: data_uri(os.path.join(HERE, "img", f"{d['img']}-{n}.jpg"))
SC = [  # (kind, image, kicker, line 1, line 2, seconds)
    ("img", "hero", "הצעה לשיתוף פעולה", f"אולם התצוגה של {d['name']}", "פתוח תמיד, בחמש שפות", 5.5),
    ("img", "floor", "הדירה", "הקונה בוחר קומה וכיוון", "על הבניין עצמו, בתוך העיר האמיתית", 5),
    ("img", "fview", "הנוף", "ורואה מה יראה מהחלון", "הים, הפארק והרובע מהקומה שבחר", 5),
    ("img", "fmap", "השכונה", "וכל מה שסביב, על מפה אחת", "חינוך, פארקים, תחבורה ומחירים באזור", 5),
    ("img", "fdoor", "הבית", "נכנס לדירה ומעצב את הבית", "עם בן הזוג והמשפחה בחו״ל, באותו רגע", 5),
    ("text", "", "חמש שפות", "עברית · English · Français · Русский · العربية", "כל שפה נכתבת לקונה שלה. לא מתורגמת.", 5),
    ("text", "", "הפנייה", "הקונה מגיע אליכם מוכן", "עם שאלה על דירה מסוימת", 4.5),
    ("text", "", "הליווי", f"{MEITAL['name']}, מתווכת מהשכונה", "מביאה את הקונה עד החתימה", 5),
    ("text", "", "רישום לקוח", "רישום עם חותמת זמן · 2 ימי עסקים לבדיקה", "12 חודשי הגנה · שכר תיווך רק על חתימה", 5.5),
    ("end", "", "", f"{MEITAL['name']} · {MEITAL['office']}", f"מתווכת מורשית, רישיון {MEITAL['lic']} · {MEITAL['phone']}", 5),
]
scenes, t = [], 0.0
for i, (kind, img, k, a, b, sec) in enumerate(SC):
    bg = f'<div class="ph"><img src="{im(img)}"></div><div class="veil"></div>' if kind == "img" else ""
    extra = '<div class="url">nad-lan.co.il · הדמיות להמחשה בלבד</div>' if kind == "end" else ""
    scenes.append(f'<section class="sc {kind}" data-t="{t:.2f}" data-d="{sec}">{bg}<div class="tx"><div class="k">{k}</div><h1>{a}</h1><p>{b}</p></div>{extra}</section>')
    t += sec
TOTAL = t
html = f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700&family=Heebo:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1280px;height:720px;overflow:hidden;background:#231A12}}
.sc{{position:absolute;inset:0;opacity:0;background:#231A12;color:#F7F1E6;font-family:Heebo,sans-serif;direction:rtl}}
.sc.on{{opacity:1}}.ph{{position:absolute;inset:0;overflow:hidden}}.ph img{{width:100%;height:100%;object-fit:cover;transform:scale(1.02)}}
.veil{{position:absolute;inset:0;background:linear-gradient(0deg,rgba(35,26,18,.92) 0%,rgba(35,26,18,.55) 34%,rgba(35,26,18,0) 62%)}}
.tx{{position:absolute;right:72px;left:72px;bottom:64px;opacity:0}}
.k{{font-size:17px;letter-spacing:.16em;color:#C9A66B;margin-bottom:10px}}
h1{{font-family:"Frank Ruhl Libre",serif;font-weight:700;font-size:54px;line-height:1.12;text-wrap:balance}}
p{{font-size:25px;color:#E4DACA;margin-top:12px}}
.text .tx,.end .tx{{top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}}
.text h1{{font-size:50px}}.text:after,.end:after{{content:"";position:absolute;top:50%;right:50%;width:70px;height:2px;background:#9C7A3C;transform:translate(50%,-150px)}}
.end h1{{font-size:46px}}.url{{position:absolute;bottom:40px;right:0;left:0;text-align:center;color:#BFB29C;font-size:17px;letter-spacing:.04em}}
</style></head><body>{''.join(scenes)}
<script>
var S=[].slice.call(document.querySelectorAll('.sc'));
function cl(x){{return x<0?0:x>1?1:x}}
window.render=function(t){{S.forEach(function(s){{var a=parseFloat(s.dataset.t),d=parseFloat(s.dataset.d),last=s===S[S.length-1];
var o=cl((t-a)/0.9)*(last?1:cl((a+d+0.9-t)/0.9));s.style.opacity=o;s.style.visibility=o>0?'visible':'hidden';
var im=s.querySelector('.ph img');if(im){{var k=cl((t-a)/(d+0.9));im.style.transform='scale('+(1.02+0.11*k)+') translateY('+(-1.5*k)+'%)'}}
var tx=s.querySelector('.tx'),q=cl((t-a-0.35)/0.9);tx.style.opacity=q;tx.style.transform='translateY('+(18*(1-q))+'px)'}})}};
window.render(0);
</script></body></html>"""
src = os.path.join(HERE, f"film-{key}.html")
open(src, "w", encoding="utf-8").write(html)
tmp = os.path.join(HERE, "shots", f"film-{key}-frames")
shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
FPS = 24
N = int((TOTAL + 0.6) * FPS)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.goto("file:///" + src.replace("\\", "/"), wait_until="networkidle")
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
    for i in range(N):
        pg.evaluate(f"render({i / FPS:.4f})")
        pg.screenshot(path=os.path.join(tmp, f"f{i:05d}.jpg"), type="jpeg", quality=92)
    b.close()
out = os.path.join(HERE, f"film-{key}.mp4")
ff = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff, "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%05d.jpg"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "slow",
                "-movflags", "+faststart", "-an", out], check=True, capture_output=True)
subprocess.run([ff, "-y", "-ss", "3", "-i", out, "-frames:v", "1", os.path.join(HERE, "shots", f"film-{key}-f03.png")], capture_output=True)
subprocess.run([ff, "-y", "-ss", f"{TOTAL - 2:.1f}", "-i", out, "-frames:v", "1", os.path.join(HERE, "shots", f"film-{key}-fend.png")], capture_output=True)
print("film", out, os.path.getsize(out), "bytes,", f"{TOTAL:.1f} s")
