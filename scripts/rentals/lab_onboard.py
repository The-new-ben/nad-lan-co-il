# -*- coding: utf-8 -*-
"""An empty account: onboarding, then an Excel paste creates buildings, apartments, tenants and leases."""
import sys, pathlib
from playwright.sync_api import sync_playwright
BASE = "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs/design-lab/rentals/shots"
SHEET = {"he": "כתובת\tעיר\tדירה\tקומה\tשוכר\tטלפון\tשכר דירה\tתחילת חוזה\tסיום חוזה\nהרצל 10\tחולון\tדירה 4\t2\tמיכל אברהם\t050-0000201\t5,200\t1.3.2026\t28.2.2027\nהרצל 10\tחולון\tדירה 9\t4\t\t\t\t\t\nביאליק 5\tרמת השרון\tדירה 1\t1\tJohn Smith\t050-0000202\t8400\t2026-06-01\t2027-05-31",
         "en": "Address\tCity\tApartment\tFloor\tTenant\tPhone\tRent\tLease start\tLease end\n10 Herzl St\tHolon\tApt 4\t2\tMichal Avraham\t050-0000201\t5200\t1.3.2026\t28.2.2027\n10 Herzl St\tHolon\tApt 9\t4\t\t\t\t\t\n5 Bialik St\tRamat HaSharon\tApt 1\t1\tJohn Smith\t050-0000202\t8400\t2026-06-01\t2027-05-31"}
ok = True
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader"])
    for lang in ("he", "en"):
        pg = b.new_page(viewport={"width": 1280, "height": 900}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + "?lang=%s&empty=1#/today" % lang, wait_until="networkidle"); pg.wait_for_timeout(800)
        has_ob = pg.locator("[data-act='sample']").count() == 1
        pg.screenshot(path=str(OUT / ("%s-desk-onboarding.png" % lang)))
        pg.click("[data-act='import']"); pg.wait_for_selector(".nlrm-layer.is-in textarea")
        pg.fill(".nlrm-layer.is-in textarea", SHEET[lang]); pg.click("[data-imp='check']"); pg.wait_for_timeout(300)
        found = pg.inner_text("#nlrm-imp-prev")
        pg.screenshot(path=str(OUT / ("%s-desk-import.png" % lang)))
        pg.click(".nlrm-layer.is-in [type='submit']"); pg.wait_for_timeout(2500)
        props = pg.evaluate("NLRM.store.d.properties.length"); units = pg.evaluate("NLRM.store.d.units.length"); leases = pg.evaluate("NLRM.store.d.leases.length")
        charges = pg.evaluate("NLRM.store.d.ledger.filter(r=>r.kind==='charge').length")
        print(lang, "onboarding:", has_ob, "| preview:", found.split("\n")[0], "| created props/units/leases/charges:", props, units, leases, charges, "| errors:", errs[:2])
        ok = ok and has_ob and props == 2 and units == 3 and leases == 2 and charges > 0 and not errs
        # HAD-401: the same sheet again changes nothing (no second building, apartment, tenant or lease)
        before = pg.evaluate("[NLRM.store.d.properties.length, NLRM.store.d.units.length, NLRM.store.d.contacts.length, NLRM.store.d.leases.length]")
        pg.click("[data-act='add']") if pg.locator("[data-act='add']").count() else None
        pg.evaluate("NLRM.forms.importSheet()"); pg.wait_for_selector(".nlrm-layer.is-in textarea")
        pg.fill(".nlrm-layer.is-in textarea", SHEET[lang]); pg.click("[data-imp='check']"); pg.wait_for_timeout(300)
        again = pg.inner_text("#nlrm-imp-prev")
        pg.click(".nlrm-layer.is-in [type='submit']"); pg.wait_for_timeout(2500)
        after = pg.evaluate("[NLRM.store.d.properties.length, NLRM.store.d.units.length, NLRM.store.d.contacts.length, NLRM.store.d.leases.length]")
        print(lang, "import twice:", before, "->", after, "| preview:", again.split(chr(10))[0][:160])
        ok = ok and before == after and (("כבר קיימ" in again) or ("already" in again))
        # a fifth apartment on one floor: the building grows to show it (apartments per floor never left at 4)
        row = ("ז'בוטינסקי 3", "גבעתיים", "דירה %d") if lang == "he" else ("3 Jabotinsky St", "Givatayim", "Apt %d")
        five = SHEET[lang].split(chr(10))[0] + chr(10) + chr(10).join(chr(9).join([row[0], row[1], row[2] % k, "2", "", "", "", "", ""]) for k in range(1, 6))
        pg.evaluate("NLRM.forms.importSheet()"); pg.wait_for_selector(".nlrm-layer.is-in textarea")
        pg.fill(".nlrm-layer.is-in textarea", five); pg.click("[data-imp='check']"); pg.wait_for_timeout(300)
        pg.click(".nlrm-layer.is-in [type='submit']"); pg.wait_for_timeout(2500)
        upf = pg.evaluate("(() => { const p = NLRM.store.d.properties.find(x => /3|Jabotinsky|ז'בוטינסקי/.test(x.address) && /גבעתיים|Givatayim/.test(x.city)); return p ? [p.units_per_floor, NLRM.store.d.units.filter(u => u.property_id === p.id && u.floor === 2).length] : null; })()")
        print(lang, "five on a floor: units_per_floor, units on floor 2 =", upf)
        ok = ok and upf is not None and upf[0] >= 5 and upf[1] == 5
        pg.evaluate("location.hash='#/properties'"); pg.wait_for_timeout(600)
        pg.screenshot(path=str(OUT / ("%s-desk-after-import.png" % lang)))
        pg.close()
    b.close()
print("ONBOARD+IMPORT", "PASS" if ok else "FAIL")
