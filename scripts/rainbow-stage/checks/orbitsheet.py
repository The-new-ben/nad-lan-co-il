import time, sys
from playwright.sync_api import sync_playwright
from PIL import Image
preset = sys.argv[1] if len(sys.argv) > 1 else 'sunset'
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--ignore-gpu-blocklist"])
    page = b.new_page(viewport={'width':960,'height':600})
    page.goto(f'http://127.0.0.1:47913/index.html?force3d&ao=on&orbit=0&intro=0&preset={preset}')
    page.wait_for_function('window.__rbs && window.__rbs.phase === "orbit"')
    time.sleep(1.5)
    tiles = []
    for i, bear in enumerate([188, 143, 98, 53, 8, 323, 278, 233]):
        page.evaluate(f'window.__rbs._engine()._view({bear}, 12, 1)')
        time.sleep(0.8)
        page.screenshot(path=f'_work/out/orb_{i}.png')
        tiles.append(Image.open(f'_work/out/orb_{i}.png').convert('RGB').resize((480, 300)))
    sheet = Image.new('RGB', (960, 1200))
    for i, t in enumerate(tiles): sheet.paste(t, ((i % 2) * 480, (i // 2) * 300))
    sheet.save(f'_work/out/orbit_sheet_{preset}.png')
    b.close()
print('ok')
