# -*- coding: utf-8 -*-
"""HAD-801 polish loop, cycle 4: a short silent walk recorded from the live tour (light page), for the entry on /sde-dov/.
The tour's on-screen controls are hidden for the take (the canvas only), the walker steps forward from the Ibn Gabirol and
Einstein junction with a slow turn. Raw video from Chrome's recorder, then ffmpeg cuts a clean ~10 s loop:
  desktop 960x540 and phone 750x440 H.264 (no audio track), plus a poster frame.
  python record_entry_clip.py <out dir on D:>"""
import glob, os, subprocess, sys, time
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
CH = os.path.join(os.environ.get("PROGRAMFILES", "C:/Program Files"), "Google/Chrome/Application/chrome.exe")
RAW = os.path.join(OUT, "raw"); os.makedirs(RAW, exist_ok=True)
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=CH, headless=True, args=["--enable-gpu", "--disable-renderer-backgrounding", "--disable-background-timer-throttling"])
    ctx = br.new_context(viewport={"width": 1280, "height": 720}, record_video_dir=RAW, record_video_size={"width": 1280, "height": 720})
    pg = ctx.new_page()
    pg.goto("https://nad-lan.co.il/tour/sde-dov/?walk=1&clip=1", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_function("window.tourReady || (window.round2StreetCell && window.round2StreetCell.live)", timeout=150000)
    try:
        pg.wait_for_function("!window.tour || !window.tour.world || (window.tour.world.artReady && window.tour.world.pendingTiles===0)", timeout=60000)
    except Exception:
        pass
    pg.wait_for_timeout(6000)
    pg.evaluate("""(()=>{const s=document.createElement('style');s.textContent='body *:not(canvas){visibility:hidden!important} canvas{visibility:visible!important}';document.head.appendChild(s);
      const cs=[...document.querySelectorAll('canvas')].sort((a,b)=>b.clientWidth*b.clientHeight-a.clientWidth*a.clientHeight);const big=cs[0];
      cs.slice(1).forEach(c=>c.style.setProperty('visibility','hidden','important'));
      document.querySelectorAll('body *').forEach(e=>{if(e===big||e.contains(big))e.style.setProperty('visibility','visible','important')})})()""")
    pg.mouse.move(640, 360)
    t_mark = time.time()
    pg.keyboard.down("KeyW")
    pg.wait_for_timeout(12000)
    pg.keyboard.up("KeyW")
    pg.wait_for_timeout(800)
    vid = pg.video.path()
    ctx.close(); br.close()
src = vid
print("raw", src, os.path.getsize(src))
# the take starts ~ (time from page open to t_mark); keep the last 11 s of the recording
dur = float(subprocess.run([FF, "-i", src], capture_output=True, text=True).stderr.split("Duration: ")[1].split(",")[0].split(":")[-1]) if False else None
for name, w, h in (("desktop", 960, 540), ("phone", 750, 440)):
    o = os.path.join(OUT, "sde-dov-2036-entry-walk-%s.mp4" % name)
    subprocess.run([FF, "-y", "-sseof", "-11.5", "-i", src, "-t", "10", "-an",
                    "-vf", "scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,fps=30" % (w, h, w, h),
                    "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p", "-crf", "31", "-preset", "slow", "-movflags", "+faststart", o],
                   check=True, capture_output=True)
    print(o, os.path.getsize(o))
subprocess.run([FF, "-y", "-sseof", "-11.5", "-i", src, "-frames:v", "1", "-vf", "scale=960:540", os.path.join(OUT, "sde-dov-2036-entry-walk-poster.jpg")], check=True, capture_output=True)
print("poster done")
