# -*- coding: utf-8 -*-
"""HAD-790 (1.72.719): press the new "ניהול השכרה" menu item live, as a visitor: phone 390 (open the menu sheet, tap the item) and
desktop 1080, 1280, 1440 (click it in the bar), from the home and from a project page; plus "Rental management" on /en/.
Pass = the item is visible, the click lands on /my-rentals/ (?lang=en for English) and the rentals page shows its H1.
Screenshots of the header (or the open sheet) before the click and of the page after it go to docs/qa/had-790/after-719/."""
import os, json, time
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "qa", "had-790", "after-719")
os.makedirs(OUT, exist_ok=True)
CASES = [("/", "he"), ("/projects/hamedina/", "he"), ("/en/", "en")]
DEV = [("phone390", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)),
       ("desk1080", dict(viewport={"width": 1080, "height": 800})),
       ("desk1280", dict(viewport={"width": 1280, "height": 800})),
       ("desk1440", dict(viewport={"width": 1440, "height": 900}))]
res = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for dev, o in DEV:
        ctx = b.new_context(**o)
        pg = ctx.new_page()
        for path, lang in CASES:
            pg.goto("https://nad-lan.co.il" + path + "?r719=1", wait_until="domcontentloaded", timeout=90000)
            pg.wait_for_timeout(1500)
            tag = "%s-%s" % (dev, path.strip("/").replace("/", "_") or "home")
            if dev == "phone390":
                pg.locator("#nlhp-top .nlhp-ico--menu").tap(); pg.wait_for_timeout(700)
            it = pg.locator("#nlhp-nav > a.nlhp-nav__keep")
            it.scroll_into_view_if_needed()
            shown = it.is_visible()
            text = it.inner_text().strip() if shown else ""
            if dev == "phone390":
                pg.screenshot(path=os.path.join(OUT, tag + "-sheet.png"))
            else:
                it.hover(); pg.wait_for_timeout(250)
                pg.screenshot(path=os.path.join(OUT, tag + "-bar.png"), clip={"x": 0, "y": 0, "width": o["viewport"]["width"], "height": 90})
            if dev == "phone390":
                it.tap()
            else:
                it.click()
            pg.wait_for_load_state("domcontentloaded", timeout=60000); pg.wait_for_timeout(1500)
            h1 = pg.evaluate("() => { const h = document.querySelector('h1'); return h ? h.textContent.trim().slice(0, 90) : ''; }")
            want = "/my-rentals/?lang=en" if lang == "en" else "/my-rentals/"
            ok = shown and pg.url.split("nad-lan.co.il")[1].startswith(want) and bool(h1)
            pg.screenshot(path=os.path.join(OUT, tag + "-landed.png"))
            row = dict(device=dev, page=path, item=text, landed=pg.url, h1=h1, ok=ok)
            res.append(row)
            print(("OK  " if ok else "BAD ") + json.dumps(row, ensure_ascii=False))
            time.sleep(1.0)
        ctx.close()
    b.close()
json.dump(res, open(os.path.join(OUT, "result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("%d/%d OK" % (sum(r["ok"] for r in res), len(res)))
