"""Live press of /asbestos/ and /en/asbestos/ in real Chrome: phone 390 and desktop, every tool pressed, map drawn, no sideways scroll."""
import os, json
from playwright.sync_api import sync_playwright
OUT = r"C:\Users\777\nad-lan\nad-lan-co-il\docs\qa\asbestos"
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for url, lg in (("https://nad-lan.co.il/asbestos/", "he"), ("https://nad-lan.co.il/en/asbestos/", "en")):
        for tag, vp in (("m", {"width": 390, "height": 844}), ("d", {"width": 1366, "height": 900})):
            ctx = b.new_context(viewport=vp, device_scale_factor=2 if tag == "m" else 1, is_mobile=tag == "m", has_touch=tag == "m")
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
            pg.on("console", lambda m: errs.append("console:" + m.text[:140]) if m.type == "error" else None)
            pg.goto(url + "?nlv=press1", wait_until="load", timeout=90000); pg.wait_for_timeout(9000)
            r = {}
            r["scrollWidth"] = pg.evaluate("document.documentElement.scrollWidth")
            r["order"] = pg.evaluate("""() => { const y = s => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().top + scrollY) : -1; };
                return {h1: y('h1'), answer: y('.entry-content > p, article p'), cta: y('.asbp-cta'), hero: y('.asbh'), check: y('[data-nli=asbcheck]'), map: y('[data-nli=asbmap]')}; }""")
            pg.screenshot(path=os.path.join(OUT, f"live-{lg}-top-{tag}.png"))
            c = pg.locator('[data-nli="asbcheck"]')
            c.locator("button[data-v=debris]").click(); c.locator("button[data-v=crumbling]").click(); pg.wait_for_timeout(300)
            r["check"] = c.locator(".asbx__out .asbx__lv").inner_text()
            k = pg.locator('[data-nli="asbcost"]'); r["cost"] = k.locator(".nli__fig").inner_text().replace("\n", " ")
            w = pg.locator('[data-nli="asbwho"]'); w.locator("input").fill("חיפה"); pg.wait_for_timeout(400)
            r["who"] = w.locator(".asbw__name").inner_text()
            mp = pg.locator('[data-nli="asbmap"]'); mp.scroll_into_view_if_needed(); pg.wait_for_timeout(5000)
            r["canvas"] = mp.locator("canvas.maplibregl-canvas").count()
            mp.screenshot(path=os.path.join(OUT, f"live-{lg}-map-{tag}.png"))
            pg.locator(".asbh").first.screenshot(path=os.path.join(OUT, f"live-{lg}-hero-{tag}.png"))
            r["errors"] = errs[:4]
            res[f"{lg}-{tag}"] = r
            print(lg, tag, json.dumps(r, ensure_ascii=False))
            ctx.close()
    b.close()
json.dump(res, open(os.path.join(OUT, "press-live.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
