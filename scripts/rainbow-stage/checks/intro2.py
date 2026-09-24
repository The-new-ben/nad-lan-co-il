import time
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--ignore-gpu-blocklist"])
    page = b.new_page(viewport={'width':1440,'height':900})
    page.goto('http://127.0.0.1:47913/index.html?force3d&ao=off')
    page.wait_for_function("document.querySelector('.rbs') && document.querySelector('.rbs').classList.contains('rbs--live')", polling=16)
    t0 = time.time()
    names = []
    for i, t in enumerate([0.05, 0.28, 0.55, 1.0, 2.2, 4.1]):
        while time.time() - t0 < t: time.sleep(0.01)
        n = f'_work/out/i2_{i}.png'; page.screenshot(path=n); names.append((n, round(time.time()-t0,2), page.evaluate('window.__rbs.phase')))
    b.close()
tiles = [Image.open(n).convert('RGB').resize((480,300)) for n,_,_ in names]
sheet = Image.new('RGB', (960, 900))
for i, t in enumerate(tiles): sheet.paste(t, ((i % 2) * 480, (i // 2) * 300))
sheet.save('_work/out/intro2_sheet.png')
print(names)
