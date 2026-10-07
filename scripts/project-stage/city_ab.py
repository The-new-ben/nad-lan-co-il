# -*- coding: utf-8 -*-
"""HAD-460: the price list's own load cost, measured as an interleaved A/B on the same page at the same minutes (7.10.2026).
Before/after runs hours apart picked up machine and server noise (wave 2: Givatayim +304 ms tripped the CEO's stop rule while
the control pages, unchanged, had slowed by 370-530 ms). Here each page loads N times with the list and N times with the list's
CSS, section and script stripped from the HTML in the browser (Playwright route), alternating; the cost = median(with) - median(without).
python city_ab.py <path> [<path> ...] [--n 5]      phone 390x844, headless Chrome, loadEventEnd"""
import re
import statistics
import sys
import time

from playwright.sync_api import sync_playwright

N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 5
PATHS = [a for i, a in enumerate(sys.argv[1:], 1) if a.startswith("/") and sys.argv[i - 1] != "--n"]
STRIP = [re.compile(r'<style id="nlpg-css">.*?</style>', re.S), re.compile(r'<section class="nlds nlpg[^"]*" id="nlpg".*?</section>', re.S),
         re.compile(r'<script id="nlpg-js">.*?</script>', re.S)]


def strip(html):
    for r in STRIP:
        html = r.sub("", html, count=1)
    return html


with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome", headless=True)
    for path in PATHS:
        res = {"with": [], "without": []}
        for i in range(2 * N):
            mode = "with" if i % 2 == 0 else "without"
            c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
            p = c.new_page()
            if mode == "without":
                def handle(route, request):
                    if request.resource_type == "document":
                        r = route.fetch()
                        route.fulfill(response=r, body=strip(r.text()))
                    else:
                        route.continue_()
                p.route("**/*", handle)
            p.goto("https://nad-lan.co.il" + path + "?nlab=%d" % (time.time() * 1000 + i), wait_until="load", timeout=120000)
            if mode == "without" and p.evaluate("!!document.getElementById('nlpg')"):
                raise SystemExit(f"{path}: the strip did not remove the list")
            res[mode].append(p.evaluate("()=>Math.round(performance.getEntriesByType('navigation')[0].loadEventEnd)"))
            c.close()
        mw, mo = statistics.median(res["with"]), statistics.median(res["without"])
        print(f"{path}: with {sorted(res['with'])} median {int(mw)} | without {sorted(res['without'])} median {int(mo)} | cost {int(mw - mo)} ms")
    b.close()
