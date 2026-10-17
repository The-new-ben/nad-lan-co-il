# -*- coding: utf-8 -*-
"""HAD-543 route-swap preview: live pages, but bridge.js served from the local patched file. Native clicks only."""
import hashlib, os, re, sys, urllib.request
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "plugins", "nadlan-config", "assets", "project-stage", "bridge.js"))
patched = open(LOCAL, "rb").read()
before = open(os.path.join(HERE, "bridge.before.js"), "rb").read()
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for slug in ("ashira-sde-dov", "rainbow-tel-aviv"):
        for mode in ("live", "patched"):
            ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
            pg = ctx.new_page()
            served = {}
            def handle(route, mode=mode):
                r = route.fetch(); body = r.body()
                served["md5"] = hashlib.md5(body).hexdigest()
                route.fulfill(response=r, body=patched if mode == "patched" else body)
            pg.route(re.compile(r".*/project-stage/bridge\.js.*"), handle)
            pg.goto(f"https://nad-lan.co.il/projects/{slug}/", wait_until="domcontentloaded", timeout=90000)
            pg.wait_for_timeout(9000)
            btn = pg.locator('[data-nlps-step="view"]').first
            btn.scroll_into_view_if_needed(); btn.click()
            pg.wait_for_timeout(7000)
            acts = pg.eval_on_selector_all('.rbs-act', 'els => els.map(e => (e.getAttribute("data-act")||"") + ":" + e.textContent.trim())')
            card = pg.locator('#nlps-pick').first
            try:
                card.scroll_into_view_if_needed(); pg.wait_for_timeout(800)
                card.screenshot(path=os.path.join(HERE, f"preview-{slug}-{mode}.png"))
            except Exception as e:
                pg.screenshot(path=os.path.join(HERE, f"preview-{slug}-{mode}.png"))
            res[(slug, mode)] = (acts, served.get("md5"))
            print(slug, mode, "live bridge md5", served.get("md5"), "| repo-before md5", hashlib.md5(before).hexdigest(), "| actions:", acts)
            ctx.close()
    b.close()
