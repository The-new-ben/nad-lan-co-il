"""Load and motion timing for the v2 proposal (26.10.2026): the live page today vs the same page with the v2 block, 3 loads each
at 390 px (phone emulation) and 3 at 1280 px. Same safety as proof2.py (no writes, analytics and recording blocked).
Measured: time from navigation to the first city label on screen, long tasks (main-thread blocks over 50 ms) until then and 3 s
after, the frame intervals while the map zooms 7 -> 10 and 10 -> 7 in 1.5 s (from rest) and while the page scrolls past the map. Software WebGL
(SwiftShader) makes absolute numbers slower than a real phone; the comparison is what counts.

    python timing2.py     (writes out/timing.json)
"""
import io
import json
import os
import statistics
import sys
import time

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib2  # noqa: E402
from proof2 import BLOCK_HOSTS, CHROME, HOOK  # noqa: E402

INIT = HOOK + """window.__lt=[];try{new PerformanceObserver(function(l){l.getEntries().forEach(function(e){window.__lt.push([e.startTime,e.duration])})}).observe({type:'longtask',buffered:true})}catch(e){}"""
FRAMES = """async (kind) => { const m = window.__nlmap, d = [];
  if (kind === 'zoom' || kind === 'zoomout') { m.jumpTo({center: [34.85, 32.05], zoom: kind === 'zoom' ? 7 : 10}); await new Promise(r => setTimeout(r, 1500)); }  // start from rest, like a visitor
  await new Promise(r => { let last = performance.now(), on = true; function f(t) { d.push(t - last); last = t; if (on) requestAnimationFrame(f); }
    requestAnimationFrame(f);
    if (kind === 'zoom' || kind === 'zoomout') { m.easeTo({zoom: kind === 'zoom' ? 10 : 7, duration: 1500}); setTimeout(() => { on = false; r(); }, 1700); }
    else { const y0 = window.scrollY, el = document.getElementById('nlurm-map'); const top = el.getBoundingClientRect().top + y0 - 700; window.scrollTo(0, top);
      let k = 0; const iv = setInterval(() => { window.scrollBy(0, 24); if (++k > 60) { clearInterval(iv); on = false; r(); } }, 16); } });
  d.shift(); d.sort((a, b) => a - b); return {frames: d.length, median_ms: +d[Math.floor(d.length / 2)].toFixed(1), p95_ms: +d[Math.floor(d.length * 0.95)].toFixed(1)}; }"""


def one(br, mode, w, mob):
    ctx = br.new_context(viewport={'width': w, 'height': 844 if mob else 900}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, locale='he-IL')
    ctx.add_init_script(INIT)

    def guard(route):
        r = route.request
        u = r.url
        if any(h in u for h in BLOCK_HOSTS) or ('nad-lan.co.il' in u and r.method != 'GET'):
            return route.abort()
        if mode == 'after' and r.resource_type == 'document' and u.split('?')[0].rstrip('/') == lib2.LIVE_URL.rstrip('/'):
            resp = route.fetch()
            return route.fulfill(response=resp, body=lib2.swapped_live_page(resp.text()), headers={**resp.headers, 'content-type': 'text/html; charset=UTF-8'})
        return route.continue_()
    ctx.route('**/*', guard)
    pg = ctx.new_page()
    pg.goto(lib2.LIVE_URL + '?v2timing=' + mode, wait_until='domcontentloaded', timeout=90000)
    sel = "document.querySelectorAll('.nlurm-pin').length>=76" if mode == 'before' else "[...document.querySelectorAll('.nlurm-lb .tg')].some(b=>b.style.display!=='none')"
    pg.wait_for_function(sel, timeout=90000)
    t = pg.evaluate("performance.now()-window.__t0")
    time.sleep(3)
    lt = pg.evaluate("window.__lt")
    pg.wait_for_function("window.__nlmap && window.__nlmap.loaded()", timeout=60000)
    pg.evaluate("document.getElementById('nlurm-map').scrollIntoView({block:'center'})")
    time.sleep(0.8)
    zoom = pg.evaluate(FRAMES, 'zoom')
    time.sleep(0.5)
    zoomout = pg.evaluate(FRAMES, 'zoomout')
    time.sleep(0.5)
    scroll = pg.evaluate(FRAMES, 'scroll')
    ctx.close()
    return {'ms_to_labels': round(t), 'longtasks_n': len(lt), 'longtasks_ms': round(sum(d for _, d in lt)), 'zoom_frames': zoom, 'zoomout_frames': zoomout, 'scroll_frames': scroll}


def main():
    out = {'note': 'software WebGL (SwiftShader), headless; compare before/after only', 'runs': {}}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME, headless=True, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        for w, mob in ((390, True), (1280, False)):
            for mode in ('before', 'after'):
                rs = [one(br, mode, w, mob) for _ in range(3)]
                key = '%d-%s' % (w, mode)
                out['runs'][key] = rs
                summ = {k: statistics.median([r[k] for r in rs]) for k in ('ms_to_labels', 'longtasks_n', 'longtasks_ms')}
                summ['zoom_median_ms'] = statistics.median([r['zoom_frames']['median_ms'] for r in rs])
                summ['zoom_p95_ms'] = statistics.median([r['zoom_frames']['p95_ms'] for r in rs])
                summ['zoomout_median_ms'] = statistics.median([r['zoomout_frames']['median_ms'] for r in rs])
                summ['zoomout_p95_ms'] = statistics.median([r['zoomout_frames']['p95_ms'] for r in rs])
                summ['scroll_median_ms'] = statistics.median([r['scroll_frames']['median_ms'] for r in rs])
                summ['scroll_p95_ms'] = statistics.median([r['scroll_frames']['p95_ms'] for r in rs])
                out.setdefault('median', {})[key] = summ
                print(key, json.dumps(summ))
        br.close()
    json.dump(out, open(os.path.join(HERE, 'out', 'timing.json'), 'w', encoding='utf-8'), indent=1)


if __name__ == '__main__':
    main()
