# -*- coding: utf-8 -*-
"""HAD-801: record the first seconds of the live tour as a visitor sees them (no input), then a frame sheet for inspection.
  python record_first10.py <url> <out dir> <seconds> [walk]"""
import os, subprocess, sys
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
URL, OUT, SEC = sys.argv[1], sys.argv[2], int(sys.argv[3]); WALK = len(sys.argv) > 4
os.makedirs(OUT, exist_ok=True); RAW = os.path.join(OUT, "raw"); os.makedirs(RAW, exist_ok=True)
CH = os.path.join(os.environ.get("PROGRAMFILES", "C:/Program Files"), "Google/Chrome/Application/chrome.exe")
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=CH, headless=True, args=["--enable-gpu", "--disable-renderer-backgrounding"])
    ctx = br.new_context(viewport={"width": 1280, "height": 720}, record_video_dir=RAW, record_video_size={"width": 1280, "height": 720})
    pg = ctx.new_page(); pg.goto(URL, wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_function("window.tourReady || (window.round2StreetCell && window.round2StreetCell.live)", timeout=150000)
    try:
        pg.wait_for_function("!window.tour || !window.tour.world || (window.tour.world.artReady && window.tour.world.pendingTiles===0)", timeout=60000)
    except Exception:
        pass
    pg.wait_for_timeout(1500)
    if WALK:
        pg.mouse.move(640, 360); pg.keyboard.down("KeyW")
    pg.wait_for_timeout(SEC * 1000)
    if WALK:
        pg.keyboard.up("KeyW")
    vid = pg.video.path(); ctx.close(); br.close()
subprocess.run([FF, "-y", "-loglevel", "error", "-sseof", "-%d" % SEC, "-i", vid, "-vf", "fps=2,scale=640:360,tile=4x5", "-frames:v", "1", os.path.join(OUT, "sheet.jpg")], check=True)
subprocess.run([FF, "-y", "-loglevel", "error", "-sseof", "-%d" % SEC, "-i", vid, "-vf", "fps=2", os.path.join(OUT, "f%02d.jpg")], check=True)
print(vid)
