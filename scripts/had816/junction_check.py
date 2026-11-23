# HAD-816 1.72.759: the live map at the Ibn Gabirol - Arlozorov junction (one label per interchange), phone 360 + desktop 1440
import os, json
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', 'research', '2026-11-23-transport-shade-maps', 'live')
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    for w, h in ((1440, 900), (360, 780)):
        ctx = b.new_context(viewport={'width': w, 'height': h}, is_mobile=w < 768, has_touch=w < 768)
        pg = ctx.new_page(); errs = []
        pg.on('console', lambda m: errs.append(m.text[:160]) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        pg.goto('https://nad-lan.co.il/transit/?zq=7591', wait_until='load', timeout=90000); pg.wait_for_timeout(7000)
        pg.fill('#nltr-q', 'אבן גבירול - ארלוזורוב'); pg.wait_for_timeout(700)
        items = pg.evaluate("[...document.querySelectorAll('.nltr-res button')].map(b=>b.textContent)")
        pg.click('.nltr-res button'); pg.wait_for_timeout(3500)
        info = pg.evaluate("({h1:document.querySelectorAll('h1').length, docW:document.documentElement.scrollWidth, ver:[...document.scripts].map(s=>s.src).filter(s=>s.includes('transit.js'))[0]})")
        name = 'he-%d-8-junction-ibn-gabirol-arlozorov-1.72.759.png' % w
        pg.screenshot(path=os.path.join(OUT, name))
        res[w] = dict(search=items[:3], info=info, errors=errs, shot=name)
        ctx.close()
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
