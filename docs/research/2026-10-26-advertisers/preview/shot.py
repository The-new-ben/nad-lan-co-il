import os, sys
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    for w in (390, 1280):
        pg = b.new_page(viewport={"width": w, "height": 900}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
        pg.goto("file:///" + os.path.join(H, "advertise-preview.html").replace("\\", "/")); pg.wait_for_timeout(1500)
        pg.screenshot(path=os.path.join(H, "adv-%d-full.png" % w), full_page=True)
        print(w, "height", pg.evaluate("document.documentElement.scrollHeight"), "sideways", pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"), "errors", errs[:2])
        pg.close()
    b.close()
