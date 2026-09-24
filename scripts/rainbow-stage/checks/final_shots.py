"""Final verification screenshots, rendered with SwiftShader as specified in the brief."""
import time, json, os
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:47913/index.html'
OUT = 'shots'
os.makedirs(OUT, exist_ok=True)
SW = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]
log = {}

def wait_orbit(page, extra):
    page.wait_for_function('window.__rbs && window.__rbs.phase === "orbit"', timeout=240000)
    time.sleep(extra)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=SW)

    # desktop: default experience (opening move, then slow auto-orbit)
    page = b.new_page(viewport={'width': 1440, 'height': 900})
    page.set_default_timeout(240000)
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' and '404' not in m.text else None)
    t0 = time.time()
    page.goto(BASE + '?force3d')
    page.wait_for_function("document.querySelector('.rbs') && document.querySelector('.rbs').classList.contains('rbs--live')")
    time.sleep(1.0)
    page.screenshot(path=f'{OUT}/desktop-opening-start.png')
    wait_orbit(page, 1.5)
    log['intro_wallclock_s'] = round(time.time() - t0, 1)
    page.screenshot(path=f'{OUT}/desktop-sunset.png')
    log['desktop'] = page.evaluate('window.__rbs.stats()')

    # floor 32 picked with a real mouse click on the tower
    pt = page.evaluate('window.__rbs._engine()._floorScreenPoint(32)')
    page.mouse.move(pt['x'], pt['y'])
    page.mouse.click(pt['x'], pt['y'])
    time.sleep(4)
    page.screenshot(path=f'{OUT}/desktop-floor.png')
    log['floor_label'] = page.evaluate("document.querySelector('.rbs-label').innerText")

    # noon preset via the segmented control
    page.click('.rbs-label-close')
    page.click('button[data-preset="noon"]')
    time.sleep(7)
    page.screenshot(path=f'{OUT}/desktop-noon.png')
    log['errors_desktop'] = errs[:]
    page.close()

    # desktop with ambient occlusion forced on (what a fast GPU shows)
    page = b.new_page(viewport={'width': 1440, 'height': 900})
    page.set_default_timeout(240000)
    page.goto(BASE + '?force3d&ao=on&intro=0&orbit=0')
    page.wait_for_function('window.__rbs && window.__rbs.phase === "orbit"')
    page.wait_for_function('window.__rbs.stats().ao === true')
    time.sleep(6)
    page.screenshot(path=f'{OUT}/desktop-sunset-ao.png')
    log['desktop_ao'] = page.evaluate('window.__rbs.stats()')
    page.close()

    # phone 390x844
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=3,
                        user_agent='Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36')
    page = ctx.new_page()
    page.set_default_timeout(240000)
    page.goto(BASE + '?force3d&nogov')
    wait_orbit(page, 1.5)
    page.screenshot(path=f'{OUT}/phone.png')
    log['phone'] = page.evaluate('window.__rbs.stats()')
    pt = page.evaluate('window.__rbs._engine()._floorScreenPoint(14)')
    page.touchscreen.tap(pt['x'], pt['y'])
    time.sleep(6)
    page.screenshot(path=f'{OUT}/phone-floor.png')
    log['phone_label'] = page.evaluate("document.querySelector('.rbs-label').innerText")
    ctx.close()

    # software renderer without force3d: poster + button (the real fallback path)
    page = b.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(BASE)
    time.sleep(2)
    page.screenshot(path=f'{OUT}/fallback-poster.png')
    log['fallback_classes'] = page.evaluate("document.querySelector('.rbs').className")
    page.close()
    b.close()

print(json.dumps(log, ensure_ascii=False, indent=1))
