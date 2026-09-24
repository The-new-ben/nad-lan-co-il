"""Functional checks for the Rainbow stage (GPU headless Chrome, plus one SwiftShader fallback check)."""
import time, json
from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:47913/index.html'
results = []
def check(name, ok, info=''):
    results.append((name, bool(ok), info))
    print(('PASS ' if ok else 'FAIL ') + name + ('  ' + str(info) if info else ''))

CAM = "(() => { const e = window.__rbs._engine(); return null; })()"

with sync_playwright() as p:
    gpu = p.chromium.launch(channel='chrome', headless=True, args=['--ignore-gpu-blocklist'])

    # 1. default load, intro, auto-orbit, console cleanliness
    page = gpu.new_page(viewport={'width': 1440, 'height': 900})
    errors = []
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' and '404' not in m.text else None)
    page.on('pageerror', lambda e: errors.append(str(e)))
    t0 = time.time()
    page.goto(URL)
    page.wait_for_function('window.__rbs && window.__rbs.phase !== "poster"', timeout=30000)
    page.evaluate('window.__rbs.ready')
    check('3D ready (live) on GPU', page.evaluate("document.querySelector('.rbs').classList.contains('rbs--live')"), f'{time.time()-t0:.2f}s after navigation')
    check('intro phase first', page.evaluate('window.__rbs.phase') == 'intro')
    time.sleep(4.2)
    check('intro ends within ~4 s', page.evaluate('window.__rbs.phase') == 'orbit')
    cam1 = page.evaluate("(() => { const c = document.querySelector('canvas'); return window.__rbs.stats(); })()")
    posA = page.evaluate("window.__rbs._engine()._debug().cam")
    time.sleep(3)
    posB = page.evaluate("window.__rbs._engine()._debug().cam")
    moved = sum((a - b) ** 2 for a, b in zip(posA, posB)) ** 0.5
    check('auto-orbit moves the camera after the intro', moved > 1.0, f'{moved:.1f} m in 3 s')
    st = page.evaluate('window.__rbs.stats()')
    check('draw calls under 60 (no AO)', st['drawCalls'] < 60 or st['ao'], st)
    check('scene triangles under 150k', st['sceneTriangles'] < 150000, st['sceneTriangles'])

    # 2. hover shows an unpinned label, leaving hides it
    page.evaluate('window.__rbs.setAutoOrbit(false)')
    time.sleep(0.6)
    pt = page.evaluate('window.__rbs._engine()._floorScreenPoint(30)')
    page.mouse.move(pt['x'] - 40, pt['y'] + 200)
    page.mouse.move(pt['x'], pt['y'], steps=4)
    time.sleep(0.5)
    lbl = page.evaluate("document.querySelector('.rbs-label').className")
    title = page.evaluate("document.querySelector('.rbs-label-title').textContent")
    check('hover shows the floor label', 'is-on' in lbl, title)
    page.mouse.move(60, 450, steps=4)
    time.sleep(1.2)
    lbl2 = page.evaluate("document.querySelector('.rbs-label').className")
    check('leaving the tower hides an unpinned label', 'is-on' not in lbl2)

    # 3. click pins, CTA dispatches nl:floor
    pt = page.evaluate('window.__rbs._engine()._floorScreenPoint(39)')
    page.mouse.move(pt['x'], pt['y'])
    page.mouse.click(pt['x'], pt['y'])
    time.sleep(0.5)
    line = page.evaluate("document.querySelector('.rbs-label-line').textContent")
    ttl = page.evaluate("document.querySelector('.rbs-label-title').textContent")
    check('penthouse floors say פנטהאוזים', line == 'פנטהאוזים', f'{ttl} / {line}')
    page.mouse.move(60, 450, steps=4)
    time.sleep(1.2)
    check('clicked label stays pinned', 'is-on' in page.evaluate("document.querySelector('.rbs-label').className"))
    page.click('.rbs-label-cta')
    time.sleep(0.2)
    ev = page.evaluate('window.__lastFloorEvent')
    check("CTA dispatches CustomEvent('nl:floor')", ev is not None and 'floor' in ev, ev)
    for f, expect in [(5, 'דירות 2 עד 4 חדרים לפי פרסומי השיווק'), (20, 'דירות 2 עד 4 חדרים לפי פרסומי השיווק'), (21, 'דירות 4 עד 5 חדרים לפי פרסומי השיווק'), (37, 'דירות 4 עד 5 חדרים לפי פרסומי השיווק'), (38, 'פנטהאוזים'), (40, 'פנטהאוזים')]:
        page.evaluate(f'window.__rbs.selectFloor({f})')
        got = page.evaluate("document.querySelector('.rbs-label-line').textContent")
        check(f'floor {f} line', got == expect, got)
    page.click('.rbs-label-close')
    time.sleep(0.3)
    check('close button clears the floor', 'is-on' not in page.evaluate("document.querySelector('.rbs-label').className"))

    # 4. keyboard
    page.focus('canvas')
    page.keyboard.press('ArrowUp')
    time.sleep(0.2)
    check('keyboard ArrowUp selects a floor', page.evaluate("document.querySelector('.rbs-label-title').textContent") == 'קומה 20')
    page.keyboard.press('ArrowUp')
    check('ArrowUp again moves up one floor', page.evaluate("document.querySelector('.rbs-label-title').textContent") == 'קומה 21')
    page.keyboard.press('Escape')

    # 5. presets
    page.click('button[data-preset="noon"]')
    time.sleep(1.6)
    check('noon preset button checked', page.evaluate("document.querySelector('button[data-preset=noon]').getAttribute('aria-checked')") == 'true')
    check('handle reports noon', page.evaluate('window.__rbs.preset') == 'noon')
    page.click('button[data-preset="sunset"]')
    time.sleep(1.6)

    # 6. wheel is ignored until the visitor engages, then zooms
    d0 = page.evaluate("(() => { const d = window.__rbs._engine()._debug(); return d.cam; })()")
    page.mouse.move(720, 300)
    page.mouse.wheel(0, -600)
    time.sleep(0.8)
    d1 = page.evaluate("window.__rbs._engine()._debug().cam")
    check('wheel without engagement does not zoom', sum((a - b) ** 2 for a, b in zip(d0, d1)) ** 0.5 < 0.5)
    page.mouse.down(); page.mouse.up()
    page.mouse.wheel(0, -600)
    time.sleep(0.8)
    d2 = page.evaluate("window.__rbs._engine()._debug().cam")
    check('wheel after a click zooms', sum((a - b) ** 2 for a, b in zip(d1, d2)) ** 0.5 > 1.0)

    # 7. dispose and remount
    page.evaluate('window.__rbs.dispose()')
    time.sleep(0.3)
    check('dispose removes the stage', page.evaluate("document.querySelector('.rbs') === null && document.querySelector('canvas') === null"))
    page.evaluate("import('./stage.js').then(m => { window.__rbs = m.mountRainbowStage(document.getElementById('rainbow-stage'), { intro: false }); })")
    page.wait_for_function('window.__rbs && window.__rbs.phase === "orbit"', timeout=20000)
    check('remount after dispose works', page.evaluate("document.querySelectorAll('.rbs').length === 1 && document.querySelectorAll('canvas').length === 1"))
    check('no console errors', len(errors) == 0, errors[:5])
    page.close()

    # 8. reduced motion: no intro, no auto-orbit
    ctx = gpu.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
    page = ctx.new_page()
    page.goto(URL)
    page.wait_for_function('window.__rbs && window.__rbs.phase !== "poster"', timeout=30000)
    check('reduced motion starts at the hero view (no intro)', page.evaluate('window.__rbs.phase') == 'orbit')
    a = page.evaluate("window.__rbs._engine()._debug().cam")
    time.sleep(8)
    b = page.evaluate("window.__rbs._engine()._debug().cam")
    check('reduced motion: no auto-orbit', sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5 < 0.01)
    ctx.close()

    # 9. weak device: hardwareConcurrency 4 + small screen -> poster and button
    ctx = gpu.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=3)
    ctx.add_init_script("Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 4 });")
    page = ctx.new_page()
    page.goto(URL)
    time.sleep(2)
    cls = page.evaluate("document.querySelector('.rbs').className")
    btn = page.evaluate("getComputedStyle(document.querySelector('.rbs-open')).display")
    check('weak phone keeps the poster and offers the button', 'rbs--fallback' in cls and btn != 'none' and page.evaluate('window.__rbs.phase') == 'poster', cls)
    page.screenshot(path='_work/out/fallback_phone.png')
    page.tap('.rbs-open')
    page.wait_for_function('window.__rbs.phase !== "poster"', timeout=30000)
    time.sleep(1.5)
    check('button opens the 3D', 'rbs--live' in page.evaluate("document.querySelector('.rbs').className"))
    ctx.close()
    gpu.close()

    # 10. software renderer (SwiftShader) without force3d -> poster + button
    sw = p.chromium.launch(channel='chrome', headless=True, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    page = sw.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(URL)
    time.sleep(2)
    check('software WebGL falls back to the poster', 'rbs--fallback' in page.evaluate("document.querySelector('.rbs').className"))
    page.screenshot(path='_work/out/fallback_desktop.png')
    sw.close()

print()
print(f"{sum(1 for r in results if r[1])}/{len(results)} checks passed")
