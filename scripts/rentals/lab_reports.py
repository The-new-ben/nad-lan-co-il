# -*- coding: utf-8 -*-
"""Rentals v2 lab: the printed reports by real presses (HAD-401). The evidence file opens its window
inside the press (no popup block) and fills it from the lease's whole history; the yearly summary
asks which year (this year or last year). he + en, desk + phone.
Usage: python scripts/rentals/lab_reports.py [base_url]"""
import sys, pathlib
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs/design-lab/rentals/shots/reports"
OUT.mkdir(parents=True, exist_ok=True)
fails = 0


def check(name, ok, info=""):
    global fails
    fails += 0 if ok else 1
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:160] if info != "" else ""))


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for lang in ("he", "en"):
        for dev, vp in (("desk", {"width": 1440, "height": 900}), ("phone", {"width": 390, "height": 844})):
            tag = "%s %s" % (lang, dev)
            ctx = b.new_context(viewport=vp, is_mobile=(dev == "phone"), has_touch=(dev == "phone"))
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(BASE + "?lang=" + lang + "#/reports", wait_until="networkidle")
            pg.wait_for_selector("[data-act='rep-evidence']", timeout=15000)
            # the evidence file for lease 201
            pg.click("[data-act='rep-evidence']")
            pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
            pg.select_option(".nlrm-layer.is-in [name='l']", "201")
            with ctx.expect_page() as pop:
                pg.click(".nlrm-layer.is-in form [type='submit']")
            w = pop.value
            w.wait_for_function("document.querySelectorAll('table').length >= 3", timeout=8000)
            rows = w.evaluate("document.querySelectorAll('table')[1].querySelectorAll('tr').length")
            want = pg.evaluate("NLRM.store.d.ledger.filter(r => r.lease_id === 201).length")
            check("%s evidence file opens and holds every line of the lease" % tag, rows == want and rows > 0, "%s rows, %s lines" % (rows, want))
            w.screenshot(path=str(OUT / ("%s-%s-evidence.png" % (lang, dev))), full_page=False)
            w.close()
            # the yearly summary: pick the year
            pg.click("[data-act='rep-year']")
            pg.wait_for_selector(".nlrm-layer.is-in [name='y']", timeout=4000)
            opts = pg.evaluate("[...document.querySelector(\".nlrm-layer.is-in [name='y']\").options].map(o => o.value)")
            y0 = pg.evaluate("String(NLRM.today().getFullYear())")
            check("%s the year picker offers this year and last year" % tag, opts == [y0, str(int(y0) - 1)], opts)
            pg.select_option(".nlrm-layer.is-in [name='y']", str(int(y0) - 1))
            with ctx.expect_page() as pop:
                pg.click(".nlrm-layer.is-in form [type='submit']")
            w = pop.value
            w.wait_for_load_state()
            h1 = w.evaluate("(document.querySelector('h1')||{}).textContent || ''")
            check("%s last year's summary opens" % tag, str(int(y0) - 1) in h1, h1)
            w.close()
            check("%s no page errors" % tag, not errs, errs[:2])
            ctx.close()
    b.close()
print("FAILS", fails)
sys.exit(1 if fails else 0)
