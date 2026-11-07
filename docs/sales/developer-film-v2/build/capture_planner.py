# -*- coding: utf-8 -*-
"""The campaign planner (local build, docs/research/2026-11-07-campaign-network/build/build-nlcamp/preview.html) on a phone,
Hebrew, five steps, for the film. The planner's own controls only: France and Canada, investors, 25,000 a month, an existing
page with the field filled as "הפרויקט שלכם" (a neutral demo value instead of the verify run's test address). Nothing is sent
(step 5 is only shown, never submitted). Local http.server on 127.0.0.1, stopped at the end.

  python capture_planner.py <out_dir>
"""
import os, socket, subprocess, sys, time, urllib.request
from playwright.sync_api import sync_playwright

REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
REL = "/docs/research/2026-11-07-campaign-network/build/build-nlcamp/preview.html"
T = "#pv-camp .nli-host"
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", REPO],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(100):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}{REL}", timeout=1).read(10); break
        except Exception:
            time.sleep(0.1)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="he-IL")
        ctx.route("**/*", lambda r: r.abort() if not (r.request.url.startswith(f"http://127.0.0.1:{port}") or "fonts.g" in r.request.url) else r.continue_())
        pg = ctx.new_page()
        pg.goto(f"http://127.0.0.1:{port}{REL}", wait_until="networkidle")
        pg.wait_for_selector(T + " .nlcp")
        pg.evaluate("document.fonts.ready")
        def press(sel, w=150):
            pg.locator(sel).first.click(); pg.wait_for_timeout(w)
        def nxt():
            press(T + ' button[data-act="next"]', 250)
        def shot(k):
            pg.locator("#pv-camp").screenshot(path=os.path.join(out, f"plan{k}.png"))
        press(f'{T} button.nlcp__chip[data-m="fr"]'); press(f'{T} button.nlcp__chip[data-m="ca"]')
        shot(1); nxt()
        press(f'{T} label.nlcp__card:has(input[value="invest"])'); shot(2); nxt()
        f = pg.locator(T + ' input[data-f="budget"]').first; f.click(); f.press("Control+A"); f.press("Backspace"); f.type("25000"); pg.wait_for_timeout(200)
        shot(3); pg.locator(T + ' input[data-f="budget"]').focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
        press(f'{T} label.nlcp__card:has(input[value="existing"])')
        f = pg.locator(T + ' input[data-f="ref"]').first; f.click(); f.type("הפרויקט שלכם"); pg.wait_for_timeout(200)
        pg.evaluate("() => document.activeElement && document.activeElement.blur()")
        shot(4); nxt()
        pg.evaluate("() => window.scrollTo(0, 0)"); shot(5)
        print("count:", pg.locator(T + " .nlcp__count").inner_text())
        b.close()
finally:
    srv.terminate()
