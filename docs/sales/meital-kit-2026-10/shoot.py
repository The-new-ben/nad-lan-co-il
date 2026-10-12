# -*- coding: utf-8 -*-
"""HAD-495: screenshots of the LIVE project pages for the developer decks (Ashira, Rainbow).
python shoot.py <slug> [<slug>...]   -> shots/<slug>-<part>.png"""
import os, sys, time
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "shots")
PARTS = [("stage", "#nlps-stage"), ("view", "#nlps-view"), ("map", "#nlpjx-map"), ("price", "#nlpg"), ("world", "#nlpjx-world"), ("sch", "#nlsch")]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for slug in sys.argv[1:]:
        for w, h, tag in ((1440, 900, "d"), (390, 844, "m")):
            c = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, locale="he-IL")
            pg = c.new_page()
            pg.goto(f"https://nad-lan.co.il/projects/{slug}/?nlshot={int(time.time())}", wait_until="load", timeout=120000)
            pg.wait_for_timeout(9000)
            pg.screenshot(path=os.path.join(OUT, f"{slug}-{tag}-top.png"))
            for name, sel in PARTS:
                el = pg.query_selector(sel)
                if not el:
                    print(slug, tag, name, "missing"); continue
                el.scroll_into_view_if_needed(); pg.wait_for_timeout(3500)
                try:
                    el.screenshot(path=os.path.join(OUT, f"{slug}-{tag}-{name}.png"))
                    print(slug, tag, name, "ok", el.bounding_box())
                except Exception as e:
                    print(slug, tag, name, "fail", str(e)[:120])
            c.close()
    b.close()
