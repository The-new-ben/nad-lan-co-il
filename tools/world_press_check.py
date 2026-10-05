# -*- coding: utf-8 -*-
"""Real presses on the Kikar world (HAD-421, 5.10.2026): phone 390 and PC 1366, headless Chrome (the browser pane stalls
IntersectionObserver while hidden). Per address: load, wait for the world to be usable (the poster gone), press the hero's
tour button ([data-nlps-ev="hero-world"]), and read the world's own state: mode must be "walk". Also: page errors, the time the
world became usable, and a screenshot after the press.

  python tools/world_press_check.py https://nad-lan.co.il/projects/hamedina/ [more urls] [--shots DIR]"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

SIZES = [("phone", 390, 844, True), ("pc", 1366, 900, False)]


def check(p, url, name, w, h, mobile, shots):
    b = p.chromium.launch(channel="chrome", headless=True, args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
    sep = "&" if "?" in url else "?"
    pg.goto(url + sep + "nlpress=%d" % time.time(), wait_until="domcontentloaded", timeout=120000)
    t0 = time.time()
    ready = None
    while time.time() - t0 < 60:
        if pg.evaluate("!!document.querySelector('.nlw-poster.is-gone')"):
            ready = round(pg.evaluate("performance.now()") / 1000, 2)
            break
        pg.wait_for_timeout(200)
    btn = pg.query_selector('[data-nlps-ev="hero-world"]')
    pressed = False
    if btn:
        btn.click()
        pressed = True
    pg.wait_for_timeout(3500)
    st = pg.evaluate("() => { try { return window.__nlpsWorld && window.__nlpsWorld.getState ? window.__nlpsWorld.getState() : null; } catch (e) { return String(e); } }")
    mode_attr = pg.evaluate("() => { const r = document.querySelector('#nlps-stage [data-mode]'); return r ? r.dataset.mode : null; }")
    shot = None
    if shots:
        os.makedirs(shots, exist_ok=True)
        slug = url.rstrip("/").split("/")[-1].replace("?", "_").replace("=", "-") or "home"
        shot = os.path.join(shots, "%s-%s.png" % (slug, name))
        pg.screenshot(path=shot)
    b.close()
    mode = st.get("mode") if isinstance(st, dict) else None
    ok = bool(ready) and pressed and mode == "walk" and not errs
    return {"url": url, "size": name, "ok": ok, "world_ready_s": ready, "pressed": pressed, "mode": mode, "mode_attr": mode_attr, "errors": errs[:3], "shot": shot}


def main(argv):
    shots = argv[argv.index("--shots") + 1] if "--shots" in argv else None
    urls = [a for a in argv if a.startswith("http")]
    bad = 0
    with sync_playwright() as p:
        for u in urls:
            for name, w, h, mobile in SIZES:
                r = check(p, u, name, w, h, mobile, shots)
                bad += 0 if r["ok"] else 1
                print(json.dumps(r, ensure_ascii=False))
    print("RESULT", "all pressed and walking" if not bad else "%d failed" % bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
