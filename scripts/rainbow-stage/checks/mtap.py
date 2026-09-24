import time, sys, json
from playwright.sync_api import sync_playwright
gpu = '--sw' not in sys.argv
args = ["--ignore-gpu-blocklist"] if gpu else ["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=args)
    ctx = b.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True, device_scale_factor=3,
        user_agent='Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36')
    page = ctx.new_page()
    page.goto('http://127.0.0.1:47913/index.html?force3d&ao=off&orbit=0&intro=0')
    page.wait_for_function('window.__rbs && window.__rbs.phase === "orbit"')
    time.sleep(2 if gpu else 8)
    pt = page.evaluate('window.__rbs._engine()._floorScreenPoint(12)')
    page.touchscreen.tap(pt['x'], pt['y'])
    time.sleep(1.5 if gpu else 6)
    page.screenshot(path='_work/out/m_tap12.png')
    print(json.dumps(page.evaluate("({lbl: document.querySelector('.rbs-label').innerText, cls: document.querySelector('.rbs-label').className, st: document.querySelector('.rbs-label').style.transform})"), ensure_ascii=False))
    # tap the CTA and check the event
    page.tap('.rbs-label-cta')
    time.sleep(0.5)
    print('event:', page.evaluate('JSON.stringify(window.__lastFloorEvent)'))
    b.close()
