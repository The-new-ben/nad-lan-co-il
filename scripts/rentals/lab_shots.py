# -*- coding: utf-8 -*-
"""Rentals v2 local lab: real clicks through every screen and card, he + en,
desktop 1440 and phone 390, screenshots + console errors + checks.
Usage: python scripts/rentals/lab_shots.py [base_url]   (server: .claude/launch.json rentals-lab)"""
import sys, json, pathlib, time
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs/design-lab/rentals/shots"
OUT.mkdir(parents=True, exist_ok=True)
SCREENS = ["today", "properties", "property/1", "people", "money", "repairs", "leasing", "docs", "reports", "settings"]
results = {"errors": [], "checks": []}

def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": info})
    print(("PASS " if ok else "FAIL ") + name + (" · " + str(info) if info else ""))

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for lang in ("he", "en"):
        for dev, vp in (("desk", {"width": 1440, "height": 900}), ("phone", {"width": 390, "height": 844})):
            ctx = b.new_context(viewport=vp, device_scale_factor=2 if dev == "phone" else 1, is_mobile=(dev == "phone"), has_touch=(dev == "phone"), locale="he-IL" if lang == "he" else "en-GB")
            pg = ctx.new_page()
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "404" not in m.text else None)
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
            pg.goto(BASE + "?lang=" + lang + "#/today", wait_until="networkidle")
            pg.wait_for_selector(".nlrm-kpis", timeout=15000)
            for sc in SCREENS:
                pg.evaluate("location.hash = '#/%s'" % sc)
                pg.wait_for_timeout(700 if sc != "property/1" else 3500)
                pg.screenshot(path=str(OUT / ("%s-%s-%s.png" % (lang, dev, sc.replace("/", "-")))), full_page=True)
                # no horizontal page scroll on any screen
                ow = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                check("%s %s %s no sideways scroll" % (lang, dev, sc), ow <= 1, ow)
            # the 360 card of an apartment: open from Today's list, walk every tab
            pg.evaluate("location.hash = '#/today'"); pg.wait_for_timeout(500)
            pg.click("[data-open^='unit:']")
            pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
            tabs = pg.eval_on_selector_all(".nlrm-ptabs [data-tab]", "els => els.map(e => e.dataset.tab)")
            for tb in tabs:
                pg.click(".nlrm-ptabs [data-tab='%s']" % tb)
                pg.wait_for_timeout(400 if tb != "home" else 2500)
                pg.screenshot(path=str(OUT / ("%s-%s-unit-%s.png" % (lang, dev, tb))))
            check("%s %s unit card tabs" % (lang, dev), len(tabs) == 7, tabs)
            pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
            check("%s %s Escape closes the card" % (lang, dev), pg.locator(".nlrm-layer").count() == 0)
            # a WhatsApp reminder: the text must be in the TENANT's language (Daniel Brooks speaks English)
            pg.evaluate("location.hash = '#/people'"); pg.wait_for_timeout(500)
            pg.click("text=Daniel Brooks")
            pg.wait_for_selector(".nlrm-layer.is-in", timeout=5000)
            pg.screenshot(path=str(OUT / ("%s-%s-contact.png" % (lang, dev))))
            pg.click(".nlrm-layer.is-in [data-act='wa-contact']")
            pg.wait_for_selector(".nlrm-layer.is-in textarea", timeout=5000)
            txt = pg.input_value(".nlrm-layer.is-in textarea")
            check("%s %s message to an English tenant is in English" % (lang, dev), txt.startswith("Hi"), txt[:30])
            pg.keyboard.press("Escape"); pg.wait_for_timeout(350)
            back = pg.locator(".nlrm-layer.is-in #nlrm-ptitle").inner_text() if pg.locator(".nlrm-layer.is-in").count() else ""
            check("%s %s closing the message returns to the tenant card" % (lang, dev), "Daniel Brooks" in back, back)
            for _ in range(3):
                if pg.locator(".nlrm-layer").count():
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
            # record a payment on the late apartment, the colour must change
            pg.evaluate("location.hash = '#/today'"); pg.wait_for_timeout(500)
            late_before = pg.locator(".nlrm-chip.is-late").count()
            pg.click("[data-act='pay']")
            pg.wait_for_selector(".nlrm-layer.is-in form", timeout=5000)
            pg.screenshot(path=str(OUT / ("%s-%s-form-payment.png" % (lang, dev))))
            pg.click(".nlrm-layer.is-in [type='submit']")
            pg.wait_for_timeout(900)
            late_after = pg.locator(".nlrm-chip.is-late").count()
            check("%s %s recording the payment clears a late chip" % (lang, dev), late_after < late_before, "%d -> %d" % (late_before, late_after))
            # a repair with live triage
            pg.click("[data-act='new']"); pg.wait_for_timeout(300)
            pg.click("[data-sheet-act='new-ticket']"); pg.wait_for_timeout(400)
            pg.fill(".nlrm-layer.is-in [name='title']", "אין מים חמים בכלל" if lang == "he" else "No hot water at all")
            pg.wait_for_timeout(200)
            tri = pg.inner_text("#nlrm-tri")
            check("%s %s triage recognises an urgent water-heater fault" % (lang, dev), ("דחוף" in tri) or ("Urgent" in tri), tri)
            pg.screenshot(path=str(OUT / ("%s-%s-form-ticket.png" % (lang, dev))))
            pg.click(".nlrm-layer.is-in [type='submit']"); pg.wait_for_timeout(900)
            check("%s %s new repair opens its card" % (lang, dev), pg.locator(".nlrm-layer.is-in").count() == 1)
            pg.screenshot(path=str(OUT / ("%s-%s-ticket.png" % (lang, dev))))
            for _ in range(3):
                if pg.locator(".nlrm-layer").count():
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
            # switch language in place
            other = "en" if lang == "he" else "he"
            pg.click(".nlrm-lang [data-lang='%s']" % other); pg.wait_for_timeout(900)
            d = pg.evaluate("document.querySelector('.nlrm-app').getAttribute('dir')")
            check("%s %s language switch flips direction" % (lang, dev), d == ("ltr" if other == "en" else "rtl"), d)
            check("%s %s console errors" % (lang, dev), not errs, errs[:3])
            results["errors"] += errs
            ctx.close()
    b.close()
json.dump(results, open(OUT / "results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
fails = [c for c in results["checks"] if not c["ok"]]
print("\n%d checks, %d failed" % (len(results["checks"]), len(fails)))
