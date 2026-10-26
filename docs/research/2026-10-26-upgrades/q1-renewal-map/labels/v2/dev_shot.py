"""Quick look while building (26.10.2026): the live page with the v2 note + block swapped in, screenshots of the map area.
Same safety as proof.py: non-GET to nad-lan.co.il aborted, analytics and recording hosts blocked. Writes out/dev-*.png only.

    python dev_shot.py [390|1280] [zoom center_lng center_lat] [js-to-run-after]
"""
import io
import json
import os
import sys
import time

from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib2  # noqa: E402

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
BLOCK_HOSTS = ['google-analytics.com', 'googletagmanager.com', 'analytics.google.com', 'hotjar.com', 'hotjar.io', 'clarity.ms',
               'facebook.net', 'facebook.com/tr', 'doubleclick.net', 'tiktok.com', 'linkedin.com/px', 'bing.com/action', 'stats.wp.com']
HOOK = """(function(){var _m;Object.defineProperty(window,'mapboxgl',{configurable:true,get:function(){return _m},set:function(v){_m=v;
try{var o=v.Map.prototype.addControl;v.Map.prototype.addControl=function(){window.__nlmap=this;return o.apply(this,arguments)}}catch(e){}}})})();"""


def run(w, z=None, c=None, after=None, tag='dev'):
    mob = w < 700
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME, headless=True, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = br.new_context(viewport={'width': w, 'height': 844 if mob else 900}, is_mobile=mob, has_touch=mob, device_scale_factor=2, locale='he-IL')
        ctx.add_init_script(HOOK)

        def guard(route):
            r = route.request
            u = r.url
            if any(h in u for h in BLOCK_HOSTS) or ('nad-lan.co.il' in u and r.method != 'GET'):
                return route.abort()
            if r.resource_type == 'document' and u.split('?')[0].rstrip('/') == lib2.LIVE_URL.rstrip('/'):
                resp = route.fetch()
                return route.fulfill(response=resp, body=lib2.swapped_live_page(resp.text()), headers={**resp.headers, 'content-type': 'text/html; charset=UTF-8'})
            return route.continue_()
        ctx.route('**/*', guard)
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text[:200]) if m.type in ('error', 'warning') else None)
        pg.goto(lib2.LIVE_URL + '?v2dev=1', wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_function("document.querySelectorAll('.nlurm-lb').length>=70", timeout=90000)
        pg.wait_for_function("window.__nlmap && window.__nlmap.loaded()", timeout=90000)
        time.sleep(2.5)
        pg.add_style_tag(content='#nlhp-top,header.nlhp-top{position:static!important}')  # test browser only: the sticky site header would cut element screenshots
        pg.evaluate("document.querySelector('.nlurm-v2').scrollIntoView({block:'start'}); window.scrollBy(0,-80)")
        if z:
            pg.evaluate("(a)=>window.__nlmap.jumpTo({center:a.c,zoom:a.z})", {'c': c, 'z': z})
            time.sleep(2.5)
        if after:
            print('after:', pg.evaluate(after))
            time.sleep(2)
        info = pg.evaluate("""() => { const t=[...document.querySelectorAll('.nlurm-lb .tg')].filter(b=>b.style.display!=='none');
          const cs=t[0]?getComputedStyle(t[0].querySelector('.nm')):null;
          return {tags:t.length, L:t.filter(b=>b.classList.contains('tL')).length, M:t.filter(b=>b.classList.contains('tM')).length, S:t.filter(b=>b.classList.contains('tS')).length,
            font: cs && [cs.fontFamily, cs.fontWeight, cs.fontSize], zoom: window.__nlmap.getZoom(), wide: document.querySelector('.nlurm-v2').classList.contains('is-wide')}; }""")
        print(w, json.dumps(info, ensure_ascii=False))
        pg.locator('.nlurm-v2').screenshot(path=os.path.join(HERE, 'out', '%s-%d.png' % (tag, w)))
        print('errors:', errs[:12])
        ctx.close()
        br.close()


if __name__ == '__main__':
    a = sys.argv[1:]
    w = int(a[0]) if a else 1280
    z = float(a[1]) if len(a) > 1 else None
    c = [float(a[2]), float(a[3])] if len(a) > 3 else None
    after = a[4] if len(a) > 4 else None
    run(w, z, c, after)
