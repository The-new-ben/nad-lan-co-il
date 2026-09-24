"""Screenshot harness for the Rainbow stage (SwiftShader, headless Chrome).
usage: python shoot.py <name> [--w 1440 --h 900] [--query "..."] [--mobile] [--wait 9] [--floor 32] [--preset noon] [--view b,e,d]
"""
import argparse, json, sys, time, os
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument('name')
ap.add_argument('--w', type=int, default=1440)
ap.add_argument('--h', type=int, default=900)
ap.add_argument('--query', default='force3d&ao=off&orbit=0')
ap.add_argument('--mobile', action='store_true')
ap.add_argument('--wait', type=float, default=8)
ap.add_argument('--floor', type=int, default=0)
ap.add_argument('--preset', default='')
ap.add_argument('--view', default='')
ap.add_argument('--out', default='_work/out')
ap.add_argument('--gpu', action='store_true')
ap.add_argument('--capture', default='')
ap.add_argument('--eval', default='')
a = ap.parse_args()

os.makedirs(a.out, exist_ok=True)
args = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]
if a.gpu:
    args = ["--ignore-gpu-blocklist"]
logs = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=args)
    ctx_args = dict(viewport={'width': a.w, 'height': a.h}, device_scale_factor=1)
    if a.mobile:
        ctx_args.update(is_mobile=True, has_touch=True, device_scale_factor=3,
                        user_agent='Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36')
    ctx = b.new_context(**ctx_args)
    page = ctx.new_page()
    page.set_default_timeout(180000)
    page.on('console', lambda m: logs.append(f'[{m.type}] {m.text}'))
    page.on('pageerror', lambda e: logs.append(f'[pageerror] {e}'))
    t0 = time.time()
    page.goto(f'http://127.0.0.1:47913/index.html?{a.query}', wait_until='load')
    try:
        page.wait_for_function('window.__rbs && window.__rbs.phase !== "poster"', timeout=60000)
        page.evaluate('window.__rbs.ready')
    except Exception as ex:
        print('FAILED waiting:', ex)
        print(chr(10).join(logs[-60:]))
        page.screenshot(path=os.path.join(a.out, a.name + '_fail.png'))
        b.close()
        sys.exit(1)
    t_ready = time.time() - t0
    time.sleep(a.wait)
    if a.view:
        bb, ee, dd = [float(x) for x in a.view.split(',')]
        page.evaluate(f'window.__rbs._engine()._view({bb},{ee},{dd})')
        time.sleep(3)
    if a.preset:
        btn = page.locator(f'button[data-preset="{a.preset}"]')
        btn.click()
        time.sleep(4)
    if a.floor:
        pt = page.evaluate(f'window.__rbs._engine()._floorScreenPoint({a.floor})')
        if a.mobile:
            page.touchscreen.tap(pt['x'], pt['y'])
        else:
            page.mouse.move(pt['x'], pt['y'])
            page.mouse.click(pt['x'], pt['y'])
        time.sleep(3)
    if a.eval:
        print('eval:', page.evaluate(a.eval))
    stats = page.evaluate('window.__rbs.stats()'); stats['phase'] = page.evaluate('window.__rbs.phase')
    if a.capture:
        url = page.evaluate(f'window.__rbs._engine()._capture({a.capture})')
        import base64
        data = base64.b64decode(url.split(',', 1)[1])
        open(os.path.join(a.out, a.name + '_capture.jpg'), 'wb').write(data)
    path = os.path.join(a.out, a.name + '.png')
    page.screenshot(path=path)
    info = page.evaluate('''() => { const c = document.createElement('canvas'); const gl = c.getContext('webgl2'); const e = gl && gl.getExtension('WEBGL_debug_renderer_info'); return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'n/a'; }''')
    print(json.dumps({'ready_s': round(t_ready, 2), 'stats': stats, 'renderer': info}, indent=1))
    b.close()
print('\n'.join(logs[-40:]))
print('saved', path)
