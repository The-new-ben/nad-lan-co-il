# -*- coding: utf-8 -*-
"""S1 local preview check (Playwright, real Chrome): the hub as served on 26.10.2026 with the new sections placed at their anchors
(preview/s1-page-render.html), at 390 px (phone, 2x) and 1280 px. For each width: console errors, sideways scroll (scrollWidth >
clientWidth), the rendered order of the first screen (H1, answer, CTAs), the tool mounted, the default answer, a tap on plot 2270 in the
map opening that plot, the open-tender preset, and element shots into preview/shots/. Serves the repo on 127.0.0.1:47932.
  python docs/research/2026-10-26-upgrades/s1-sde-dov/shot_s1.py"""
import functools, http.server, json, os, sys, threading
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47932), functools.partial(http.server.SimpleHTTPRequestHandler, directory=REPO))
threading.Thread(target=srv.serve_forever, daemon=True).start()
OUT = os.path.join(H, "preview", "shots"); os.makedirs(OUT, exist_ok=True)
URL = "http://127.0.0.1:47932/docs/research/2026-10-26-upgrades/s1-sde-dov/preview/s1-page-render.html"
report = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for w, h, tag, dpr in ((390, 844, "390", 2), (1280, 900, "1280", 1)):
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=dpr)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto(URL, wait_until="networkidle"); pg.wait_for_timeout(1200)
        r = {"errors": errs[:5]}
        r["sideways"] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        r["order"] = pg.evaluate("""() => { const y = s => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().top + scrollY) : null; };
            return { h1: y('h1'), lead: y('.nls1-lead'), cta: y('.nls1-cta'), hero: y('figure.wp-block-image'), tool: y('[data-nli="sdplan"]') }; }""")
        r["mounted"] = pg.evaluate("!!document.querySelector('[data-nli=\"sdplan\"][data-nli-on] .nli__answer')")
        r["answer"] = pg.locator('[data-nli="sdplan"] .nli__answer').inner_text().replace("\n", " | ")
        wide = pg.evaluate("""() => [...document.querySelectorAll('.nls1-t, .nli__tw, svg')].filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX === 'visible').length""")
        r["overflowing_unscrollable"] = wide
        pg.locator(".nls1-lead").screenshot(path=os.path.join(OUT, tag + "-lead.png"))
        top = pg.evaluate("Math.round(document.querySelector('h1').getBoundingClientRect().top + scrollY)")
        pg.screenshot(path=os.path.join(OUT, tag + "-first-screen.png"), clip={"x": 0, "y": max(0, top - 10), "width": w, "height": h})
        tool = pg.locator('[data-nli="sdplan"]')
        tool.screenshot(path=os.path.join(OUT, tag + "-tool-district.png"))
        # a tap on plot 2270 in the compound map: first open a compound list, then tap the plot
        pg.select_option('[data-nli="sdplan"] select[id$="-c"]', "merkaz"); pg.wait_for_timeout(500)
        tool.screenshot(path=os.path.join(OUT, tag + "-tool-merkaz.png"))
        pg.locator('[data-nli="sdplan"] [data-sdplot="2270"]').first.click(); pg.wait_for_timeout(600)
        r["tap_2270"] = pg.locator('[data-nli="sdplan"] .nli__answer').inner_text().replace("\n", " | ")
        tool.screenshot(path=os.path.join(OUT, tag + "-tool-plot-2270.png"))
        pg.locator('[data-nli="sdplan"] .nli__pre button[data-k="open"]').click(); pg.wait_for_timeout(600)
        r["preset_open"] = pg.locator('[data-nli="sdplan"] .nli__answer').inner_text().replace("\n", " | ")
        for i, f in enumerate(pg.locator("figure.nls1-fig").all()):
            f.screenshot(path=os.path.join(OUT, "%s-fig%d.png" % (tag, i + 1)))
        for i, t in enumerate(pg.locator(".nls1-t").all()[:2]):
            t.screenshot(path=os.path.join(OUT, "%s-table%d.png" % (tag, i + 1)))
        r["errors"] = errs[:5]
        report[tag] = r
        print(tag, json.dumps(r, ensure_ascii=False))
    b.close()
srv.shutdown()
json.dump(report, open(os.path.join(OUT, "report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
