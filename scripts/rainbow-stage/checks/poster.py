import time, base64, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--ignore-gpu-blocklist"])
    page = b.new_page(viewport={'width':1440,'height':900})
    page.goto('http://127.0.0.1:47913/index.html?force3d&ao=on&orbit=0&intro=0')
    page.wait_for_function('window.__rbs && window.__rbs.phase === "orbit"')
    page.wait_for_function('window.__rbs.stats().ao === true', timeout=30000)
    time.sleep(2)
    url = page.evaluate('window.__rbs._engine()._capture(1600, 1000, 0.86)')
    open('poster.jpg','wb').write(base64.b64decode(url.split(',',1)[1]))
    b.close()
print('ok')
