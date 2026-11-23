# HAD-816 live visitor check on https://nad-lan.co.il/transit/ and /en/transit/ (phone 390 + 360, desktop 1440).
import os, json, sys
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', 'research', '2026-11-23-transport-shade-maps', 'live')
os.makedirs(OUT, exist_ok=True)
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    for lang, w, h in [('he', 390, 844), ('he', 1440, 900), ('en', 390, 844), ('en', 1440, 900), ('he', 360, 780)]:
        ctx = b.new_context(viewport={'width': w, 'height': h}, is_mobile=w < 768, has_touch=w < 768)
        pg = ctx.new_page(); errs = []; fails = []; size = [0]
        pg.on('console', lambda m: errs.append(m.text[:200]) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.on('requestfailed', lambda r: fails.append(r.url[:120]))
        def onresp(r):
            try: size[0] += int(r.headers.get('content-length') or 0)
            except Exception: pass
        pg.on('response', onresp)
        url = 'https://nad-lan.co.il/' + ('en/' if lang == 'en' else '') + 'transit/?zq=816'
        pg.goto(url, wait_until='load', timeout=90000); pg.wait_for_timeout(8000)
        tag = '%s-%d' % (lang, w)
        pg.screenshot(path=os.path.join(OUT, tag + '-1-first.png'))
        info = pg.evaluate("""() => { const m=document.getElementById('nltr-map').getBoundingClientRect(); return {mapTop:Math.round(m.top), mapH:Math.round(m.height), docW:document.documentElement.scrollWidth, winW:innerWidth, h1:document.querySelectorAll('h1').length, h1t:(document.querySelector('h1')||{}).textContent, canvas:!!document.querySelector('#nltr-map canvas'), lang:document.documentElement.lang, dir:document.documentElement.dir}; }""")
        # layers: switch each off and on
        chips = {}
        for k in ('lrt', 'metro', 'rail', 'proj'):
            pg.click('.nltr-chip[data-k=%s]' % k); pg.wait_for_timeout(400)
            chips[k] = pg.get_attribute('.nltr-chip[data-k=%s]' % k, 'aria-pressed')
            if k == 'metro': pg.screenshot(path=os.path.join(OUT, tag + '-2-metro-off.png'))
            pg.click('.nltr-chip[data-k=%s]' % k); pg.wait_for_timeout(300)
        # a station through the search
        pg.fill('#nltr-q', 'ארלוזורוב' if lang == 'he' else 'Arlozorov'); pg.wait_for_timeout(700)
        pg.click('.nltr-res button'); pg.wait_for_timeout(3000)
        card = pg.evaluate("(()=>{const c=document.getElementById('nltr-card'); return c.hidden?null:c.innerText.slice(0,300)})()")
        pg.screenshot(path=os.path.join(OUT, tag + '-3-station.png'))
        # a project from the station card
        link = pg.evaluate("(()=>{const a=document.querySelector('#nltr-card .nltr-list a'); return a?a.href:null})()")
        # project search
        pg.fill('#nltr-q', 'DUO'); pg.wait_for_timeout(700)
        pr = pg.evaluate("[...document.querySelectorAll('.nltr-res button')].map(b=>b.textContent).slice(0,3)")
        if pr: pg.click('.nltr-res button'); pg.wait_for_timeout(3000)
        pcard = pg.evaluate("(()=>{const c=document.getElementById('nltr-card'); return c.hidden?null:c.innerText.slice(0,300)})()")
        pg.screenshot(path=os.path.join(OUT, tag + '-4-project.png'))
        # page scroll is not captured by the map: wheel over the map on desktop, swipe on phone
        y0 = pg.evaluate('scrollY')
        pg.mouse.move(w / 2, min(h - 100, info['mapTop'] + 100)); pg.mouse.wheel(0, 600); pg.wait_for_timeout(800)
        y1 = pg.evaluate('scrollY')
        pg.evaluate('scrollTo(0, document.body.scrollHeight*0.45)'); pg.wait_for_timeout(800)
        pg.screenshot(path=os.path.join(OUT, tag + '-5-tables.png'))
        res[tag] = dict(info=info, chips=chips, card=card, projlink=link, projsearch=pr, pcard=pcard, scroll=[y0, y1], errors=errs[:8], failed=fails[:8], bytes=size[0])
        ctx.close()
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
