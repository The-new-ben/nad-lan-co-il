import time, json, sys
from playwright.sync_api import sync_playwright
mode = sys.argv[1] if len(sys.argv) > 1 else 'headless'
query = sys.argv[2] if len(sys.argv) > 2 else 'ao=off'
w = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
h = int(sys.argv[4]) if len(sys.argv) > 4 else 900
args = ["--ignore-gpu-blocklist", "--enable-gpu-rasterization", "--disable-frame-rate-limit", "--disable-gpu-vsync"] if 'nolimit' in mode else ["--ignore-gpu-blocklist"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=(mode.startswith('headless')), args=args)
    dsf = float(sys.argv[5]) if len(sys.argv) > 5 else 1
    page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=dsf)
    logs = []
    page.on('console', lambda m: logs.append(f'[{m.type}] {m.text}'))
    t0 = time.time()
    page.goto(f'http://127.0.0.1:47913/index.html?{query}')
    page.wait_for_function('window.__rbs && window.__rbs.phase !== "poster"', timeout=60000)
    page.evaluate('window.__rbs.ready')
    t_ready = time.time() - t0
    info = page.evaluate('''() => { const c = document.createElement('canvas'); const gl = c.getContext('webgl2'); const e = gl && gl.getExtension('WEBGL_debug_renderer_info'); return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'n/a'; }''')
    print('renderer:', info, ' ready(s):', round(t_ready, 2))
    # sample fps via rAF during the intro and the orbit
    samples = []
    for i in range(14):
        time.sleep(1)
        st = page.evaluate('window.__rbs.stats()')
        ph = page.evaluate('window.__rbs.phase')
        samples.append((i + 1, ph, round(st['fps'], 1), st['dpr'], st['ao'], st.get('aoState'), st['drawCalls'], st['trianglesDrawn']))
    for s in samples: print(s)
    # raw rAF measurement over 3 s
    fps = page.evaluate('''() => new Promise(res => { let n = 0; const t0 = performance.now(); function f(){ n++; if (performance.now() - t0 < 3000) requestAnimationFrame(f); else res(n / ((performance.now() - t0) / 1000)); } requestAnimationFrame(f); })''')
    print('rAF fps (3 s):', round(fps, 1))
    print('\n'.join(l for l in logs if '404' not in l))
    b.close()
