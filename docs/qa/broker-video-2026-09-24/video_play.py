# -*- coding: utf-8 -*-
import sys, time, json
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--autoplay-policy=no-user-gesture-required"])
    for W, H, tag in ((1440, 900, "desktop"), (390, 844, "mobile")):
        pg = b.new_page(viewport={"width": W, "height": H}, is_mobile=W < 700, has_touch=W < 700)
        mp4 = []
        pg.on("request", lambda r: mp4.append(r.url.rsplit("/", 1)[-1]) if r.url.endswith(".mp4") else None)
        pg.goto("https://nad-lan.co.il/professionals/meital-katzir/?v=%d" % time.time(), wait_until="networkidle", timeout=90000)
        pg.evaluate("() => document.querySelector('.nlds-video').scrollIntoView({block: 'center'})")
        pg.wait_for_timeout(1500)
        before = list(mp4)
        st = pg.evaluate("""() => { const vs = [...document.querySelectorAll('.nlds-video__v')]; return vs.map(v => ({cls: v.className.split(' ').pop(), shown: getComputedStyle(v).display !== 'none', w: Math.round(v.getBoundingClientRect().width), h: Math.round(v.getBoundingClientRect().height), poster: !!v.poster})); }""")
        pg.screenshot(path="pl/video-%s-poster.png" % tag)
        # press play on the visible one, as a person would
        vis = pg.evaluate("() => [...document.querySelectorAll('.nlds-video__v')].findIndex(v => getComputedStyle(v).display !== 'none')")
        pg.evaluate("(i) => { const v = document.querySelectorAll('.nlds-video__v')[i]; v.muted = true; return v.play(); }", vis)
        pg.wait_for_timeout(1200)
        t1 = pg.evaluate("(i) => document.querySelectorAll('.nlds-video__v')[i].currentTime", vis)
        pg.wait_for_timeout(2500)
        t2 = pg.evaluate("(i) => { const v = document.querySelectorAll('.nlds-video__v')[i]; return [v.currentTime, v.paused, v.readyState, v.videoWidth, v.videoHeight]; }", vis)
        pg.screenshot(path="pl/video-%s-playing.png" % tag)
        print(tag, json.dumps({"videos": st, "mp4 before play": before, "mp4 after play": sorted(set(mp4)), "t1": round(t1, 2), "t2/paused/ready/size": t2}, ensure_ascii=False))
        pg.close()
    b.close()
