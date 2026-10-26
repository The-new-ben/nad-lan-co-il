"""Which work makes the slow frames while the map zooms (26.10.2026, local diagnosis): wraps requestAnimationFrame and setTimeout
callbacks in the test browser and lists those over 8 ms during a 7 -> 10 zoom, for today and for v2 (and v2 with Hebrew base
labels switched off, to separate the base map from the tags).

    python diag_frames.py
"""
import json
import os
import sys
import time

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib2  # noqa: E402
from proof2 import BLOCK_HOSTS, CHROME, HOOK  # noqa: E402

WRAP = HOOK + """(function(){var o=window.requestAnimationFrame.bind(window);window.__cb=[];window.__rec=false;
window.requestAnimationFrame=function(f){return o(function(t){var s=performance.now();f(t);var d=performance.now()-s;if(window.__rec&&d>8)window.__cb.push([(f.name||'anon')+':'+String(f).slice(0,60).replace(/\\s+/g,' '),+d.toFixed(1)])})};})();"""


def run(mode, variant=''):
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME, headless=True, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = br.new_context(viewport={'width': 1280, 'height': 900}, locale='he-IL')
        ctx.add_init_script(WRAP)

        def guard(route):
            r = route.request
            u = r.url
            if any(h in u for h in BLOCK_HOSTS) or ('nad-lan.co.il' in u and r.method != 'GET'):
                return route.abort()
            if mode == 'after' and r.resource_type == 'document' and u.split('?')[0].rstrip('/') == lib2.LIVE_URL.rstrip('/'):
                resp = route.fetch()
                body = lib2.swapped_live_page(resp.text())
                if variant == 'nohe':
                    body = body.replace('language:"he",', '').replace('mapboxgl.setRTLTextPlugin(', 'void(')
                if variant == 'notags':
                    body = body.replace('map.on("zoom",soonZoom);', '')
                return route.fulfill(response=resp, body=body, headers={**resp.headers, 'content-type': 'text/html; charset=UTF-8'})
            return route.continue_()
        ctx.route('**/*', guard)
        pg = ctx.new_page()
        pg.goto(lib2.LIVE_URL + '?diag=' + mode, wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_function("window.__nlmap && window.__nlmap.loaded()", timeout=90000)
        time.sleep(4)
        pg.evaluate("document.getElementById('nlurm-map').scrollIntoView({block:'center'})")
        time.sleep(1)
        res = pg.evaluate("""async () => { const m = window.__nlmap; m.jumpTo({center: [34.85, 32.05], zoom: 7}); await new Promise(r => setTimeout(r, 800));
          window.__cb = []; window.__rec = true; m.easeTo({zoom: 10, duration: 1500}); await new Promise(r => setTimeout(r, 1800)); window.__rec = false;
          const agg = {}; window.__cb.forEach(([k, d]) => { agg[k] = agg[k] || [0, 0, 0]; agg[k][0]++; agg[k][1] += d; agg[k][2] = Math.max(agg[k][2], d); });
          return Object.entries(agg).map(([k, v]) => [k, v[0], +v[1].toFixed(1), +v[2].toFixed(1)]).sort((a, b) => b[2] - a[2]).slice(0, 6); }""")
        br.close()
        return res


for m, v in (('before', ''), ('after', ''), ('after', 'nohe'), ('after', 'notags')):
    print(m, v or '-', json.dumps(run(m, v), ensure_ascii=False))
