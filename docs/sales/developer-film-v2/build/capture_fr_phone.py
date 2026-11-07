"""The French project page on a phone (390 wide, device scale 3), the top 1,700 px of the page, read-only."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from live_common import launch
from playwright.sync_api import sync_playwright
HIDE = "#nlcta, .nlcta, #wpadminbar, [class*='cookie'], [id*='cookie'], [class*='accessib'], [id*='accessib'] { display: none !important; }"
out = sys.argv[1]
with sync_playwright() as p:
    b, ctx = launch(p, 390, 844, dpr=3, mobile=True)
    pg = ctx.new_page()
    r = pg.goto("https://nad-lan.co.il/projects/rainbow-tel-aviv-fr/", wait_until="domcontentloaded", timeout=120000)
    print("status", r.status)
    pg.add_style_tag(content=HIDE)
    pg.wait_for_timeout(9000)
    pg.screenshot(path=os.path.join(out, "fr_phone_full.png"), full_page=True, clip={"x": 0, "y": 0, "width": 390, "height": 1700})
    b.close()
