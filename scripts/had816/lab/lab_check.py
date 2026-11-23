# HAD-816 local lab check: serves out-<lang>.html + plugin assets through Playwright routes (MapLibre and tiles load from the net).
import sys, os, json, mimetypes
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__))
PLUG = os.path.join(H, '..', '..', '..', 'plugins', 'nadlan-config')
OUT = os.path.join(H, 'shots'); os.makedirs(OUT, exist_ok=True)
def route(r):
    u = r.request.url
    if u.startswith('https://lab.local/plugin/'):
        p = os.path.join(PLUG, u.split('/plugin/', 1)[1].split('?')[0])
        ct = mimetypes.guess_type(p)[0] or 'application/octet-stream'
        if p.endswith('.json'): ct = 'application/json'
        return r.fulfill(path=p, content_type=ct)
    if u.startswith('https://lab.local/'):
        lang = 'en' if '/en' in u else 'he'
        return r.fulfill(path=os.path.join(H, 'out-%s.html' % lang), content_type='text/html; charset=utf-8')
    return r.continue_()
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    for lang, w, h in [('he', 390, 844), ('he', 360, 780), ('he', 1440, 900), ('en', 390, 844), ('en', 1440, 900)]:
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=w < 768, has_touch=w < 768)
        pg = ctx.new_page(); errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('**/*', route)
        pg.goto('https://lab.local/' + ('en/' if lang == 'en' else '') + 'transit/')
        pg.wait_for_timeout(7000)
        tag = '%s-%d' % (lang, w)
        pg.screenshot(path=os.path.join(OUT, tag + '-first.png'))
        info = pg.evaluate("""() => { const m=document.getElementById('nltr-map').getBoundingClientRect(); return {mapTop:Math.round(m.top), mapH:Math.round(m.height), docW:document.documentElement.scrollWidth, h1:document.querySelectorAll('h1').length, canvas:!!document.querySelector('#nltr-map canvas')}; }""")
        # open a station through the search
        pg.fill('#nltr-q', 'ארלוזורוב' if lang == 'he' else 'Arlozorov'); pg.wait_for_timeout(600)
        items = pg.evaluate("[...document.querySelectorAll('.nltr-res button')].map(b=>b.textContent)")
        pg.click('.nltr-res button'); pg.wait_for_timeout(2500)
        card = pg.evaluate("(()=>{const c=document.getElementById('nltr-card'); return c.hidden?null:c.innerText.slice(0,400)})()")
        pg.screenshot(path=os.path.join(OUT, tag + '-station.png'))
        # toggle chips
        pg.click('.nltr-chip[data-k=metro]'); pg.wait_for_timeout(500)
        pressed = pg.evaluate("[...document.querySelectorAll('.nltr-chip')].map(b=>b.dataset.k+':'+b.getAttribute('aria-pressed'))")
        pg.screenshot(path=os.path.join(OUT, tag + '-nometro.png'))
        res[tag] = dict(info=info, search=items[:4], card=card, chips=pressed, errors=errs[:6])
        ctx.close()
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
