# -*- coding: utf-8 -*-
"""Rentals v2 lab: the 3D drill-down by real presses (he + en, desk 1440 + phone 390).
building -> a floor's hotspot (the floor focuses, its card opens) -> an apartment -> the tenant / a repair;
the 2D floor buttons do the same; an appliance with an open repair is marked in the apartment's 3D plan
and its pin opens the repair; closing the cards returns the building to its whole view.
Usage: python scripts/rentals/lab_drill.py [base_url]   (server: python -m http.server 47914)"""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs/design-lab/rentals/shots/drill"
OUT.mkdir(parents=True, exist_ok=True)
results = {"checks": [], "errors": []}


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:200]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:160] if info != "" else ""))


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for lang in ("he", "en"):
        for dev, vp in (("desk", {"width": 1440, "height": 900}), ("phone", {"width": 390, "height": 844})):
            tag = "%s %s" % (lang, dev)
            ctx = b.new_context(viewport=vp, device_scale_factor=2 if dev == "phone" else 1, is_mobile=(dev == "phone"), has_touch=(dev == "phone"), locale="he-IL" if lang == "he" else "en-GB")
            pg = ctx.new_page()
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "404" not in m.text else None)
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
            pg.goto(BASE + "?lang=" + lang + "#/property/2", wait_until="networkidle")
            pg.wait_for_function("window.NLRM && NLRM._b3d && NLRM._b3d._debug && NLRM._b3d._debug().units > 0", timeout=30000)
            pg.wait_for_timeout(1500)
            d = pg.evaluate("NLRM._b3d._debug()")
            check("%s the building has a hotspot per floor with apartments" % tag, d.get("floorTags", 0) >= 2, d.get("floorTags"))
            check("%s some floor hotspots are visible" % tag, d.get("floorTagsShown", 0) >= 1, d.get("floorTagsShown"))
            badge = pg.locator(".nlrm3d-unit .nlrm3d-bdg").count()
            check("%s an apartment label carries its repair badge" % tag, badge >= 1, badge)
            pg.locator("#nlrm-3d").scroll_into_view_if_needed()
            pg.screenshot(path=str(OUT / ("%s-%s-building.png" % (lang, dev))))
            # a floor hotspot: the floor focuses and its card opens
            ft = pg.locator(".nlrm3d-floor:not(.is-off)").first
            fl = ft.get_attribute("data-id")
            ft.click(force=True)
            pg.wait_for_selector(".nlrm-layer.is-in", timeout=5000)
            pg.wait_for_timeout(900)
            foc = pg.evaluate("NLRM._b3d.focusedFloor()")
            check("%s tapping a floor focuses it in 3D" % tag, foc is not None and ("f%s" % foc) == fl, "%s %s" % (foc, fl))
            title = pg.inner_text(".nlrm-layer.is-in #nlrm-ptitle")
            check("%s the floor's card opens" % tag, str(foc) in title, title)
            n_apts = pg.locator(".nlrm-layer.is-in [data-open^='unit:']").count()
            check("%s the floor card lists its apartments" % tag, n_apts >= 1, n_apts)
            pg.screenshot(path=str(OUT / ("%s-%s-floor.png" % (lang, dev))))
            # deeper: an apartment, then its tenant
            pg.click(".nlrm-layer.is-in [data-open^='unit:']")
            pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
            check("%s the apartment's card opens from the floor" % tag, pg.locator(".nlrm-layer.is-in .nlrm-ptabs [data-tab='money']").count() == 1)
            ten = pg.locator(".nlrm-layer.is-in [data-open^='contact:']")
            if ten.count():
                ten.first.click(); pg.wait_for_timeout(500)
                check("%s and the tenant's card from the apartment" % tag, pg.locator(".nlrm-layer.is-in").count() == 1)
            for _ in range(4):
                if pg.locator(".nlrm-layer").count():
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
            pg.wait_for_timeout(900)
            check("%s closing the cards returns the whole building" % tag, pg.evaluate("NLRM._b3d.focusedFloor()") is None)
            # the 2D floor buttons do the same
            pg.click(".nlrm-floor-btn >> nth=0"); pg.wait_for_selector(".nlrm-layer.is-in", timeout=5000); pg.wait_for_timeout(500)
            check("%s a 2D floor button opens the floor too" % tag, pg.evaluate("NLRM._b3d.focusedFloor()") is not None)
            pg.click(".nlrm-layer.is-in [data-act='floor-back']"); pg.wait_for_timeout(900)
            check("%s 'back to the whole building'" % tag, pg.evaluate("NLRM._b3d.focusedFloor()") is None and pg.locator(".nlrm-layer").count() == 0)
            # the apartment's 3D plan: the water heater has an open repair; its pin opens it
            pg.evaluate("NLRM.open('unit', 21)")
            pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
            pg.click(".nlrm-ptabs [data-tab='home']")
            pg.wait_for_selector(".nlrm3d-pin.is-open", state="attached", timeout=20000)
            pg.wait_for_timeout(1200)
            check("%s the appliance with an open repair is marked" % tag, pg.locator(".nlrm3d-pin.is-open").count() == 1)
            pg.screenshot(path=str(OUT / ("%s-%s-apartment-pin.png" % (lang, dev))))
            pg.evaluate("document.querySelector('.nlrm3d-pin.is-open').click()")
            pg.wait_for_timeout(700)
            tt = pg.inner_text(".nlrm-layer.is-in #nlrm-ptitle") if pg.locator(".nlrm-layer.is-in").count() else ""
            check("%s its pin opens that repair" % tag, ("דוד" in tt) or ("heater" in tt.lower()), tt)
            check("%s console errors" % tag, not errs, errs[:3])
            results["errors"] += errs
            ctx.close()
    b.close()
json.dump(results, open(OUT / "results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
fails = [c for c in results["checks"] if not c["ok"]]
print("\n%d checks, %d failed" % (len(results["checks"]), len(fails)))
sys.exit(1 if fails else 0)
