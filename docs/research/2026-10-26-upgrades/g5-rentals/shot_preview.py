# -*- coding: utf-8 -*-
"""G5 local preview check: serves the repo over 127.0.0.1, opens preview/g5-page-render.html at 390 and 1280 px in Chrome
(Playwright), presses the tool's ready cases, a neighbourhood and the landlord switch, and records: console errors, sideways
scroll (document wider than the viewport), the rendered order (H1, answer, CTA row, tool, listings, first table) and screenshots
into preview/shots/. Also loads the Claude Design preview when its path is given.
  python shot_preview.py [<ds preview.html>]"""
import functools, http.server, json, os, sys, threading
from playwright.sync_api import sync_playwright
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
OUT = os.path.join(H, "preview", "shots"); os.makedirs(OUT, exist_ok=True)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47958), functools.partial(http.server.SimpleHTTPRequestHandler, directory=REPO))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = "http://127.0.0.1:47958/docs/research/2026-10-26-upgrades/g5-rentals/preview/g5-page-render.html"
ORDER = """() => { const y = s => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().top + scrollY) : -1; };
  return { h1: y('h1'), lead: y('.nlrh-lead'), cta: y('.nlrh-cta'), tool: y('[data-nli="rentfair"]'), list: y('.nlrh-list'), table: y('.nlrh-cap'),
           sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, answer: (document.querySelector('.nli__fig') || {}).textContent }; }"""
report = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for w, hgt, tag in ((390, 844, "390"), (1280, 900, "1280")):
        pg = b.new_page(viewport={"width": w, "height": hgt}, device_scale_factor=2 if w < 600 else 1)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto(URL, wait_until="networkidle"); pg.wait_for_timeout(1500)
        r = pg.evaluate(ORDER); steps = []
        pg.screenshot(path=os.path.join(OUT, "page-%s-top.png" % tag))
        tool = pg.locator('[data-nli="rentfair"]'); tool.screenshot(path=os.path.join(OUT, "rentfair-%s.png" % tag))
        for k in ("jlm4", "hfa4", "bs3", "pt4", "ta3"):
            pg.locator('.nli__pre button[data-k="%s"]' % k).click(); pg.wait_for_timeout(250)
            steps.append((k, pg.locator(".nli__fig").first.inner_text(), pg.evaluate("document.documentElement.scrollWidth")))
        pg.select_option('[data-nli="rentfair"] select >> nth=1', label="נופי ים"); pg.wait_for_timeout(300)
        steps.append(("hood נופי ים", pg.locator(".nli__fig").first.inner_text(), pg.evaluate("document.documentElement.scrollWidth")))
        tool.screenshot(path=os.path.join(OUT, "rentfair-hood-%s.png" % tag))
        pg.locator('[data-nli="rentfair"] .nli__seg button', has_text="משכירים").click(); pg.wait_for_timeout(300)
        steps.append(("landlord", pg.locator(".nli__fig").first.inner_text(), pg.locator(".nli__lines").first.inner_text()[-160:].replace("\n", " | ")))
        months = pg.locator('[data-nli="rentfair"] input').nth(1); months.fill("6"); pg.wait_for_timeout(300)
        g = pg.locator('[data-nli="rentfair"] input').nth(2); g.fill("40000"); pg.wait_for_timeout(300)
        steps.append(("over-cap", pg.locator(".nli__fig").first.inner_text(), pg.locator(".nli__answer").first.inner_text().replace("\n", " | ")[:200]))
        tool.screenshot(path=os.path.join(OUT, "rentfair-overcap-%s.png" % tag))
        for i, f in enumerate(pg.query_selector_all(".nlrh-fig")): f.screenshot(path=os.path.join(OUT, "fig%d-%s.png" % (i + 1, tag)))
        pg.locator(".nlrh-list").screenshot(path=os.path.join(OUT, "listings-%s.png" % tag))
        r2 = pg.evaluate("() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth})")
        report[tag] = {"order": r, "after_presses": r2, "steps": steps, "errors": errs}
        pg.close()
    if len(sys.argv) > 1:
        pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
        pg.goto("file:///" + os.path.abspath(sys.argv[1]).replace("\\", "/"), wait_until="networkidle"); pg.wait_for_timeout(1500)
        pg.screenshot(path=os.path.join(OUT, "ds-390.png"), full_page=False)
        report["ds"] = {"errors": errs, "sw": pg.evaluate("document.documentElement.scrollWidth"), "answers": pg.locator(".nli__fig").all_inner_texts()}
        pg.close()
    b.close()
srv.shutdown()
print(json.dumps(report, ensure_ascii=False, indent=1))
json.dump(report, open(os.path.join(OUT, "report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
