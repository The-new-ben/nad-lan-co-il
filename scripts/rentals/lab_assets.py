# -*- coding: utf-8 -*-
"""Rentals v2 lab: an apartment's appliances can be edited and removed (HAD-401), he + en.
Usage: python scripts/rentals/lab_assets.py [base_url]"""
import sys
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
fails = 0


def check(name, ok, info=""):
    global fails
    fails += 0 if ok else 1
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:140] if info != "" else ""))


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader"])
    for lang in ("he", "en"):
        pg = b.new_page(viewport={"width": 1280, "height": 900}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(BASE + "?lang=" + lang + "#/today", wait_until="networkidle"); pg.wait_for_selector(".nlrm-kpis", timeout=15000)
        uid, aid, n0 = pg.evaluate("(() => { const u = NLRM.store.d.units.find(x => ((x.meta||{}).assets||[]).length); return [u.id, u.meta.assets[0].id, u.meta.assets.length]; })()")
        pg.evaluate("(id) => NLRM.open('unit', id)", uid)
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=6000); pg.click(".nlrm-ptabs [data-tab='home']")
        pg.wait_for_selector(".nlrm-layer.is-in [data-act='asset-edit']", timeout=6000)
        pg.click(".nlrm-layer.is-in [data-act='asset-edit'][data-asset='%s']" % aid); pg.wait_for_selector(".nlrm-layer.is-in form [name='brand']", timeout=4000)
        lab = pg.evaluate("document.querySelector(\".nlrm-layer.is-in form [name='label']\").closest('label').innerText")
        check("%s the name field says appliance, not apartment" % lang, ("מכשיר" in lab) or ("Appliance" in lab), lab)
        pg.fill(".nlrm-layer.is-in form [name='brand']", "Tadiran-test"); pg.click(".nlrm-layer.is-in form [type='submit']"); pg.wait_for_timeout(700)
        a = pg.evaluate("([u, a]) => NLRM.store.d.units.find(x => x.id === u).meta.assets.find(x => x.id === a)", [uid, aid])
        check("%s edit keeps the same appliance and saves the change" % lang, a and a["brand"] == "Tadiran-test", a and a.get("brand"))
        for _ in range(3):
            if pg.locator(".nlrm-layer").count():
                pg.keyboard.press("Escape"); pg.wait_for_timeout(250)
        pg.evaluate("(id) => NLRM.open('unit', id)", uid); pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=6000); pg.click(".nlrm-ptabs [data-tab='home']")
        pg.wait_for_selector(".nlrm-layer.is-in [data-act='asset-edit']", timeout=6000)
        pg.click(".nlrm-layer.is-in [data-act='asset-edit'][data-asset='%s']" % aid); pg.wait_for_selector(".nlrm-layer.is-in form [name='remove']", timeout=4000)
        pg.check(".nlrm-layer.is-in form [name='remove']"); pg.click(".nlrm-layer.is-in form [type='submit']"); pg.wait_for_timeout(700)
        n1 = pg.evaluate("(u) => NLRM.store.d.units.find(x => x.id === u).meta.assets.length", uid)
        check("%s remove takes it off the apartment" % lang, n1 == n0 - 1, "%s -> %s" % (n0, n1))
        check("%s no page errors" % lang, not errs, errs[:2])
        pg.close()
    b.close()
print("FAILS", fails)
sys.exit(1 if fails else 0)
