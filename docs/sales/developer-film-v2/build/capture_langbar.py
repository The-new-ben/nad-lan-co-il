"""The French page's breadcrumb and language bar, sharp (device scale 4), read-only."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from live_common import launch
from playwright.sync_api import sync_playwright
out = sys.argv[1]
with sync_playwright() as p:
    b, ctx = launch(p, 1440, 900, dpr=4)
    pg = ctx.new_page()
    pg.goto("https://nad-lan.co.il/projects/rainbow-tel-aviv-fr/", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(5000)
    pg.locator(".nlptop").first.screenshot(path=os.path.join(out, "fr_topbar_x4.png"))
    pg.locator(".nlptop-l").first.screenshot(path=os.path.join(out, "fr_langbar_x4.png"))
    b.close()
