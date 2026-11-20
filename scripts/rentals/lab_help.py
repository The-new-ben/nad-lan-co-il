# -*- coding: utf-8 -*-
"""Rentals v2 lab: the Guide screen (he + en, desk + phone): the manual fragment loads in the interface
language, every image loads, the contents links scroll, the PDF button answers 200 with a PDF.
Usage: python scripts/rentals/lab_help.py [base_url]"""
import sys, pathlib
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs/design-lab/rentals/shots/help"
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
            pg.goto(BASE + "?lang=" + lang + "#/help", wait_until="networkidle")
            pg.wait_for_selector("#nlrm-help h2", timeout=15000)
            pg.wait_for_timeout(400)
            n = pg.evaluate("document.querySelectorAll('#nlrm-help h2').length")
            check("%s the guide loads (7 chapters)" % tag, n >= 7, n)
            imgs = pg.evaluate("Promise.all([...document.querySelectorAll('#nlrm-help img')].map(im => (im.loading = 'eager', im.decode().then(() => im.naturalWidth > 0, () => false)))).then(a => [a.length, a.filter(Boolean).length])")
            check("%s every image loads" % tag, imgs[0] >= 30 and imgs[0] == imgs[1], imgs)
            pref = "en-" if lang == "en" else "he-"
            own = pg.evaluate("(p) => [...document.querySelectorAll('#nlrm-help img')].every(im => im.src.indexOf('/img/' + p) > 0)", pref)
            check("%s only its own language's screenshots" % tag, own)
            href = pg.evaluate("(document.querySelector('a[href*=\"manual-\"]') || {}).href || ''")
            r = pg.request.get(href) if href else None
            check("%s the PDF button answers with a PDF" % tag, r is not None and r.status == 200 and r.body()[:4] == b"%PDF", (href[-30:], r and r.status))
            pg.click('#nlrm-help a[href^="#h-"] >> nth=2'); pg.wait_for_timeout(700)
            stays = pg.evaluate("location.hash") == "#/help"
            check("%s the contents link scrolls without leaving the screen" % tag, stays, pg.evaluate("location.hash"))
            pg.goto(BASE + "?lang=" + lang + "#/help", wait_until="networkidle"); pg.wait_for_selector("#nlrm-help h2", timeout=15000)
            pg.screenshot(path=str(OUT / ("%s-%s-help.png" % (lang, dev))))
            check("%s no page errors" % tag, not errs, errs[:2])
            ctx.close()
    b.close()
print("FAILS", fails)
sys.exit(1 if fails else 0)
