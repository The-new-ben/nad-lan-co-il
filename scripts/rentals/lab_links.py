# -*- coding: utf-8 -*-
"""Rentals v2 lab: the personal links card (HAD-401). A link sent to a tenant shows in Settings with
who, until and uses; Cancel asks first, then marks it cancelled and it leaves the live list.
he + en, desk 1440 + phone 390. Usage: python scripts/rentals/lab_links.py [base_url]"""
import sys, pathlib
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs/design-lab/rentals/shots/links"
OUT.mkdir(parents=True, exist_ok=True)
fails = 0


def check(name, ok, info=""):
    global fails
    fails += 0 if ok else 1
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:160] if info != "" else ""))


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for lang in ("he", "en"):
        for dev, vp in (("desk", {"width": 1440, "height": 900}), ("phone", {"width": 390, "height": 844})):
            tag = "%s %s" % (lang, dev)
            ctx = b.new_context(viewport=vp, device_scale_factor=2 if dev == "phone" else 1, is_mobile=(dev == "phone"), has_touch=(dev == "phone"))
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(BASE + "?lang=" + lang + "#/today", wait_until="networkidle")
            pg.wait_for_selector(".nlrm-kpis", timeout=15000)
            # a tenant link, made the way the landlord makes it (the tenant has no phone in this call: the sheet opens)
            pg.evaluate("NLRM.shareLink('tenant', 'lease', 201, null, 'portal_invite', {unit: '7'})")
            pg.wait_for_timeout(500)
            for _ in range(3):
                if pg.locator(".nlrm-layer").count():
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(250)
            pg.evaluate("location.hash = '#/settings'")
            pg.wait_for_selector("#nlrm-links .nlrm-item", timeout=5000)
            items = pg.locator("#nlrm-links .nlrm-item").count()
            txt = pg.inner_text("#nlrm-links")
            check("%s the link is listed with who and until" % tag, items >= 1 and (("ארלוזורוב" in txt) or ("Arlozorov" in txt)), txt[:120].replace("\n", " "))
            pg.locator("#nlrm-links").scroll_into_view_if_needed()
            pg.screenshot(path=str(OUT / ("%s-%s-links.png" % (lang, dev))))
            pg.click("#nlrm-links [data-act='link-revoke']")
            pg.wait_for_selector(".nlrm-layer.is-in [data-yes]", timeout=4000)
            check("%s cancel asks first" % tag, pg.locator(".nlrm-layer.is-in [data-yes]").count() == 1)
            pg.click(".nlrm-layer.is-in [data-yes]"); pg.wait_for_timeout(600)
            st = pg.evaluate("NLRM.store.d.links.filter(k => k.revoked_at).length")
            left = pg.locator("#nlrm-links .nlrm-item").count()
            check("%s cancelled: marked and off the live list" % tag, st >= 1 and left == items - 1, "%s revoked, %s left" % (st, left))
            check("%s no page errors" % tag, not errs, errs[:2])
            ctx.close()
    b.close()
print("FAILS", fails)
sys.exit(1 if fails else 0)
