# -*- coding: utf-8 -*-
"""Renders the brand kit: site-icon PNG 512/192/180/32, favicon.ico, OG image 1200x630, favicon.svg.
Rasterisation via headless Chrome (one HTML per asset), resize via Pillow. Output: assets/skin-a/brand/out/"""
import os, subprocess, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
MARK = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2F6F86"/><rect x="10" y="30" width="11" height="22" rx="1.5" fill="#F7F6F2" opacity=".72"/><rect x="26.5" y="14" width="11" height="38" rx="1.5" fill="#F7F6F2"/><rect x="43" y="24" width="11" height="28" rx="1.5" fill="#F7F6F2" opacity=".86"/><rect x="8" y="55" width="48" height="2.6" rx="1.3" fill="#F7F6F2"/></svg>'
open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(MARK)

def shot(html_path, w, h, png):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--allow-file-access-from-files",
                    "--user-data-dir=" + os.path.join(OUT, "ud-" + os.path.basename(png)), f"--window-size={w},{h}", "--virtual-time-budget=6000",
                    "--screenshot=" + png, "file:///" + html_path.replace("\\", "/")], check=True, capture_output=True)

# icon 512 (transparent corners are not needed: rounded square on transparent bg for PNG)
icon_html = os.path.join(OUT, "icon.html")
open(icon_html, "w", encoding="utf-8").write('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#F7F6F2}svg{display:block;width:512px;height:512px}</style></head><body>' + MARK + '</body></html>')
shot(icon_html, 512, 512, os.path.join(OUT, "icon-512-flat.png"))
im = Image.open(os.path.join(OUT, "icon-512-flat.png")).convert("RGBA")
# make the background (#F7F6F2) transparent so the rounded square floats
px = im.load(); W, H = im.size
for y in range(H):
    for x in range(W):
        r, g, b, a = px[x, y]
        if abs(r - 0xF7) < 4 and abs(g - 0xF6) < 4 and abs(b - 0xF2) < 4: px[x, y] = (0, 0, 0, 0)
im.save(os.path.join(OUT, "site-icon-512.png"))
for s in (192, 180, 32, 16):
    im.resize((s, s), Image.LANCZOS).save(os.path.join(OUT, f"site-icon-{s}.png"))
im.resize((48, 48), Image.LANCZOS).save(os.path.join(OUT, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])

# OG 1200x630
og_html = os.path.join(OUT, "og.html")
open(og_html, "w", encoding="utf-8").write('''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@700&family=Assistant:wght@400;600&display=swap" rel="stylesheet"><style>html,body{margin:0}.og{width:1200px;height:630px;background:#1F4B5C;color:#F7F6F2;display:flex;flex-direction:column;justify-content:space-between;padding:64px 72px;box-sizing:border-box;font-family:Assistant,Arial,sans-serif}.tag{display:flex;align-items:center;gap:16px;font-size:26px}.tag i{width:48px;height:48px;border-radius:12px;background:#F7F6F2;display:inline-grid;place-items:center}.tag svg{width:30px;height:30px}b{font-family:'Noto Serif Hebrew',serif;font-size:74px;font-weight:700;line-height:1.12;display:block}span{font-size:28px;color:#CFE3EA}</style></head><body><div class="og"><div class="tag"><i><svg viewBox="0 0 64 64"><rect x="10" y="30" width="11" height="22" rx="1.5" fill="#1F4B5C" opacity=".72"/><rect x="26.5" y="14" width="11" height="38" rx="1.5" fill="#1F4B5C"/><rect x="43" y="24" width="11" height="28" rx="1.5" fill="#1F4B5C" opacity=".86"/><rect x="8" y="55" width="48" height="2.6" rx="1.3" fill="#1F4B5C"/></svg></i>nad-lan.co.il</div><b>נדלן<br>פרויקטים חדשים, דירות למכירה ומחירי דירות</b><span>פורטל הנדל״ן של ישראל · סקירה עצמאית לפני שפונים ליזם</span></div></body></html>''')
shot(og_html, 1200, 630, os.path.join(OUT, "og-default-1200x630.png"))
Image.open(os.path.join(OUT, "og-default-1200x630.png")).convert("RGB").save(os.path.join(OUT, "og-default-1200x630.jpg"), "JPEG", quality=86, optimize=True)

# brand sheet for the owner
shot(os.path.join(HERE, "brand-kit.html"), 1440, 900, os.path.join(OUT, "brand-kit-sheet.png"))
for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    if os.path.isfile(p): print(f, os.path.getsize(p))
