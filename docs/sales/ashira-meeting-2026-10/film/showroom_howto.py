# -*- coding: utf-8 -*-
"""HAD-543: a Hebrew how-to film of Ashira's showroom (the LIVE page), real clicks only, captions drawn on the page.
python showroom_howto.py -> film/howto-he.mp4 (1280x720) + film/howto-*.png stills"""
import os, glob, shutil, subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, "howto-raw"); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
URL = "https://nad-lan.co.il/projects/ashira-sde-dov/?nlv=howto"
CAP = """([t,s])=>{let c=document.getElementById('nlhow');if(!c){c=document.createElement('div');c.id='nlhow';
c.style.cssText='position:fixed;left:50%;bottom:28px;transform:translateX(-50%);z-index:2147483647;background:#0F2233;color:#fff;font:600 26px Heebo,Arial;padding:14px 26px;direction:rtl;max-width:86vw;text-align:center;border:2px solid #fff';
document.body.appendChild(c)}c.innerHTML=t+(s?'<div style="font:400 17px Heebo,Arial;margin-top:6px;color:#D9E7F7">'+s+'</div>':'')}"""
STEPS = []
PIN = "p=>{const b=[...document.querySelectorAll('#nlps button, .nlps-stage button')].filter(e=>e.offsetParent&&e.textContent.trim()===p);if(!b.length)throw new Error('no pin '+p);b[0].click();return b.length}"
def cap(pg, t, s="", wait=2600):
    pg.evaluate(CAP, [t, s]); pg.wait_for_timeout(wait)
def safe_click(pg, sel, wait=2500):
    try:
        el = pg.locator(sel).first; el.scroll_into_view_if_needed(timeout=8000); el.click(timeout=8000); pg.wait_for_timeout(wait); STEPS.append((sel, "ok"))
    except Exception as e:
        STEPS.append((sel, "skip: " + str(e)[:60]))
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=False, args=["--window-position=0,0"])
    ctx = b.new_context(viewport={"width": 1280, "height": 720}, record_video_dir=OUT, record_video_size={"width": 1280, "height": 720}, locale="he-IL")
    pg = ctx.new_page(); pg.goto(URL, wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(6000)
    cap(pg, "אולם התצוגה של אשירה · מדריך קצר", "כך בודקים דירה מהבית, צעד אחרי צעד", 3500)
    safe_click(pg, "#nlps .rbs-open, [data-nlps-open], .nlps-stage__open", 4000)
    cap(pg, "1 · בוחרים קומה וכיוון על דגם התלת ממד", "סובבו את הבניין והקישו על קומה")
    safe_click(pg, '[data-nlps-step="view"]', 3000)
    pg.locator("#nlps").scroll_into_view_if_needed(); pg.wait_for_timeout(2500)
    cap(pg, "2 · הנוף מהקומה והמפה", "מה רואים מהחלון, ומה נמצא מסביב ובכמה דקות הליכה")
    pg.screenshot(path=os.path.join(H, "howto-view.png"))
    pg.locator("#nlps").scroll_into_view_if_needed(); pg.wait_for_timeout(800)
    safe_click(pg, '[data-nlps-step="inside"]', 5000)
    cap(pg, "3 · נכנסים לדירה ב-360°", "גררו כדי להסתכל סביב, ובחרו סגנון עיצוב")
    pg.screenshot(path=os.path.join(H, "howto-inside.png"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(1500)
    pg.locator("#nlps").scroll_into_view_if_needed(); pg.wait_for_timeout(1200)
    safe_click(pg, ".nlps-facbtn", 3000)
    pg.locator("#nlps").scroll_into_view_if_needed(); pg.wait_for_timeout(1500)
    cap(pg, "4 · המתקנים: בריכה, ספא, כושר, קולנוע ועולם הילדים", "מקישים על מתקן בדגם, ונכנסים אליו ב-360°")
    for pin, enter, title in (("בריכה וכושר", "כניסה לבריכה", "הבריכה המקורה · הדמיה"), ("ספא", "כניסה לספא", "הספא וחדר המלח · הדמיה"), ("גן ילדים", "כניסה לעולם הילדים", "עולם הילדים · הדמיה")):
        try:
            pg.evaluate(PIN, pin); pg.wait_for_timeout(2200)
            cap(pg, title, "גוררים כדי להסתכל סביב", 10)
            pg.locator(":is(button,a):visible", has_text=enter).first.click(timeout=8000); pg.wait_for_timeout(5000)
            box = pg.viewport_size; cx, cy = box["width"] // 2, box["height"] // 2
            pg.mouse.move(cx + 260, cy); pg.mouse.down()
            for i in range(26): pg.mouse.move(cx + 260 - i * 20, cy, steps=1); pg.wait_for_timeout(40)
            pg.mouse.up(); pg.wait_for_timeout(1800)
            if pin == "בריכה וכושר": pg.screenshot(path=os.path.join(H, "howto-pool.png"))
            STEPS.append((pin, "ok"))
        except Exception as e:
            STEPS.append((pin, "skip: " + str(e)[:60]))
        pg.keyboard.press("Escape"); pg.evaluate(CAP, ["4 · המתקנים", "מקישים על מתקן בדגם"]); pg.wait_for_timeout(1500)
        pg.locator("#nlps").scroll_into_view_if_needed(); pg.wait_for_timeout(800)
    cap(pg, "5 · שאלה? וואטסאפ בלחיצה, או שיחת וידאו עם נציג", "בשיחה כולם רואים את אותה דירה, והנציג מוביל", 3500)
    cap(pg, "nad-lan.co.il · הדמיות להמחשה בלבד", "", 2500)
    v = pg.video.path(); ctx.close(); b.close()
ff = imageio_ffmpeg.get_ffmpeg_exe(); out = os.path.join(H, "howto-he.mp4")
subprocess.run([ff, "-y", "-loglevel", "error", "-i", v, "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", "-an", out], check=True)
print("film", out, os.path.getsize(out)); print("steps", STEPS)
