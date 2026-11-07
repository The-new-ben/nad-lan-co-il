# HAD-678: press the film on the live /marketing/ page in real Chrome, phone and desktop. Presses PLAY (real click on the player), checks it runs,
# checks the order H1 -> answer paragraph -> CTAs -> film -> tools, one h1, no sideways scroll. Screenshots in shots/film-*.png.
import json, sys, time
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
URL = "https://nad-lan.co.il/marketing/?pf=%d" % time.time()
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=False, args=["--autoplay-policy=no-user-gesture-required"])
    for name, vw in (("phone", {"width": 390, "height": 844}), ("desktop", {"width": 1366, "height": 900})):
        ctx = b.new_context(viewport=vw, locale="he-IL", device_scale_factor=2 if name == "phone" else 1, is_mobile=(name == "phone"), has_touch=(name == "phone"))
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: errs.append(m.text[:160]) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERR " + str(e)[:160]))
        pg.goto(URL, wait_until="networkidle", timeout=120000); time.sleep(2)
        r = pg.evaluate("""() => { const y = s => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().top + scrollY) : null };
          const v = document.querySelector('.nlu1-film video');
          return { sw: document.documentElement.scrollWidth, vw: innerWidth, vh: innerHeight, h1s: document.querySelectorAll('h1').length,
                   y_h1: y('h1'), y_lead: y('.nlu1-lead'), y_cta: y('.nlu1-cta'), y_film: y('.nlu1-film'), y_budget: y('[data-nli="nlbudget"]'), y_planner: y('.nlcp'),
                   film_h: v ? Math.round(v.getBoundingClientRect().height) : null, film_w: v ? Math.round(v.getBoundingClientRect().width) : null,
                   video_ld: [...document.querySelectorAll('script[type="application/ld+json"]')].some(s => s.textContent.includes('VideoObject')),
                   faq_ld: [...document.querySelectorAll('script[type="application/ld+json"]')].some(s => s.textContent.includes('FAQPage')) } }""")
        pg.locator(".nlu1-film").scroll_into_view_if_needed(); time.sleep(1)
        r["poster_ok"] = pg.evaluate("""() => new Promise(res => { const i = new Image(); i.onload = () => res(i.naturalWidth); i.onerror = () => res(0); i.src = document.querySelector('.nlu1-film video').poster })""")
        pg.screenshot(path="shots/film-%s-before.png" % name)
        box = pg.locator(".nlu1-film video").bounding_box()
        pg.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)  # a real click on the player
        time.sleep(1.5)
        playing = pg.evaluate("() => { const v = document.querySelector('.nlu1-film video'); return {paused: v.paused, t: v.currentTime} }")
        if playing["paused"]:  # some players need the play button itself; press the native control by keyboard
            pg.locator(".nlu1-film video").focus(); pg.keyboard.press("Space"); time.sleep(1.5)
        time.sleep(5)
        r["play"] = pg.evaluate("() => { const v = document.querySelector('.nlu1-film video'); return {paused: v.paused, t: Math.round(v.currentTime * 10) / 10, w: v.videoWidth, h: v.videoHeight, dur: Math.round(v.duration), err: v.error ? v.error.code : null} }")
        pg.screenshot(path="shots/film-%s-playing.png" % name)
        pg.goto(URL, wait_until="networkidle", timeout=120000); time.sleep(1.5)
        pg.screenshot(path="shots/film-%s-top.png" % name)
        r["errors"] = errs[:8]; out[name] = r
        ctx.close()
    b.close()
print(json.dumps(out, ensure_ascii=False, indent=1))
