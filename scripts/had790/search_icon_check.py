# -*- coding: utf-8 -*-
"""HAD-790 follow-up (1.72.717): press the header search icon live, on a desktop and a phone, on a project page, an article page and
a language home. Pass = the icon leads to a page that has the search and the search field ends up focused and on screen.
Screenshots to docs/qa/had-790/after-717/. One headless Chrome at a time, closed right after."""
import os, sys, json, time
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "qa", "had-790", "after-717")
os.makedirs(OUT, exist_ok=True)
PAGES = sys.argv[1:] or ["/projects/hamedina/", "/projects/rainbow-tel-aviv/", "/buying-apartment/", "/en/"]
BASE = "https://nad-lan.co.il"
CHECK = """() => { const a = document.activeElement; const r = a ? a.getBoundingClientRect() : null;
  return { url: location.href, tag: a ? a.tagName : '', name: a ? (a.name || '') : '', type: a ? (a.type || '') : '',
           inHero: !!(a && a.closest && a.closest('#nlhp-hero, form.nlhv2-search')),
           onScreen: !!(r && r.width > 0 && r.top >= 0 && r.bottom <= innerHeight) }; }"""
res = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for dev, ctxo in (("desktop1024", dict(viewport={"width": 1024, "height": 768})),
                      ("phone", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2,
                                     user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Mobile Safari/537.36 hd790"))):
        ctx = b.new_context(**ctxo)
        pg = ctx.new_page()
        for path in PAGES:
            pg.goto(BASE + path + ("&" if "?" in path else "?") + "hd790s=1", wait_until="domcontentloaded", timeout=90000)
            pg.wait_for_timeout(1500)
            ico = pg.locator("#nlhp-top .nlhp-ico--search")
            href = ico.get_attribute("href")
            if dev == "phone":  # the icon shows up to 1060 px; wider screens have the full menu instead
                ico.tap()
            else:
                ico.click()
            try:
                pg.wait_for_load_state("domcontentloaded", timeout=30000)
            except Exception:
                pass
            pg.wait_for_timeout(1800)
            st = pg.evaluate(CHECK)
            ok = st["tag"] == "INPUT" and st["inHero"] and st["onScreen"]
            name = "%s-%s.png" % (dev, path.strip("/").replace("/", "_") or "home")
            pg.screenshot(path=os.path.join(OUT, name))
            row = dict(device=dev, page=path, href=href, after=st["url"], focused=st["tag"] + ":" + st["type"], ok=ok, shot=name)
            res.append(row)
            print(("OK  " if ok else "BAD ") + json.dumps(row, ensure_ascii=False))
            time.sleep(1.2)
        ctx.close()
    b.close()
json.dump(res, open(os.path.join(OUT, "result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("%d/%d OK" % (sum(r["ok"] for r in res), len(res)))
