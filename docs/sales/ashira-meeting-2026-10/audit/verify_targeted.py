# -*- coding: utf-8 -*-
"""Targeted verification and screenshot capture for basket, video, whatsapp and tour buttons."""
import os, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))

with sync_playwright() as p:
    b = p.chromium.launch(
        channel="chrome",
        args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
    )
    for key, url in [("A", "https://nad-lan.co.il/projects/ashira-sde-dov/"), ("B", "https://nad-lan.co.il/projects/rainbow-tel-aviv/")]:
        for w_tag, w, h in [("d", 1440, 900), ("m", 390, 844)]:
            ctx = b.new_context(viewport={"width": w, "height": h}, locale="he-IL")
            pg = ctx.new_page()
            pg.goto(url, wait_until="load", timeout=90000)
            pg.wait_for_timeout(4000)
            
            # 1. Basket
            print(f"[{key}-{w_tag}] Clicking basket...")
            try:
                pg.evaluate("window.scrollTo(0, 0)")
                pg.wait_for_timeout(500)
                b_btn = pg.query_selector('.nlbk-step')
                if b_btn:
                    b_btn.click()
                    pg.wait_for_timeout(1500)
                    pg.screenshot(path=os.path.join(HERE, f"{key}-{w_tag}-basket.png"))
                    pg.screenshot(path=os.path.join(HERE, f"{key}-{'1440' if w_tag=='d' else '390'}-basket.png"))
                    print(f"  [{key}-{w_tag}] basket clicked and shot taken")
            except Exception as e:
                print(f"  [{key}-{w_tag}] basket error: {e}")
                
            # 2. Video
            print(f"[{key}-{w_tag}] Clicking video...")
            try:
                v_btn = pg.query_selector('[data-nlps-ev="hero-video"]')
                if v_btn:
                    v_btn.click()
                    pg.wait_for_timeout(2000)
                    pg.screenshot(path=os.path.join(HERE, f"{key}-{w_tag}-video.png"))
                    pg.screenshot(path=os.path.join(HERE, f"{key}-{'1440' if w_tag=='d' else '390'}-video.png"))
                    print(f"  [{key}-{w_tag}] video clicked and shot taken")
            except Exception as e:
                print(f"  [{key}-{w_tag}] video error: {e}")

            # 3. WhatsApp
            print(f"[{key}-{w_tag}] Capturing WhatsApp...")
            try:
                pg.evaluate("window.scrollTo(0, 800)")
                pg.wait_for_timeout(1000)
                pg.screenshot(path=os.path.join(HERE, f"{key}-{w_tag}-whatsapp.png"))
                pg.screenshot(path=os.path.join(HERE, f"{key}-{'1440' if w_tag=='d' else '390'}-whatsapp.png"))
                print(f"  [{key}-{w_tag}] whatsapp shot taken")
            except Exception as e:
                print(f"  [{key}-{w_tag}] whatsapp error: {e}")

            # 4. Tour on B
            if key == "B":
                print(f"[{key}-{w_tag}] Clicking Tour on B...")
                try:
                    # scroll to #nlps-tour
                    tour_sec = pg.query_selector('#nlps-tour')
                    if tour_sec:
                        tour_sec.scroll_into_view_if_needed()
                        pg.wait_for_timeout(1500)
                        tour_go = pg.query_selector('.nlat__go, [data-nlps-tour]')
                        if tour_go:
                            tour_go.click()
                            pg.wait_for_timeout(3000)
                            pg.screenshot(path=os.path.join(HERE, f"B-{w_tag}-tour.png"))
                            pg.screenshot(path=os.path.join(HERE, f"B-{'1440' if w_tag=='d' else '390'}-tour.png"))
                            print(f"  [B-{w_tag}] Tour opened and shot taken")
                except Exception as e:
                    print(f"  [B-{w_tag}] tour error: {e}")

            ctx.close()
    b.close()
print("Targeted verification completed!")
