# -*- coding: utf-8 -*-
"""AreaMap load test (Playwright, headless Chrome). Opens docs/design/area-map-3d/component-preview.html and asserts:
  1. before scrolling: no request to cdnjs, OpenFreeMap or the RTL plugin host; both sections wait with "המפה נטענת"
     and inactive filters;
  2. after scrolling to the first section: it loads, the six project pins and the renewal pins appear, the frame keeps
     its height (no layout jump), and the second section (still far away) has not started;
  3. a project pin opens its card; on the second section (390px frame) a renewal pin opens its card;
  4. zero page errors and zero console errors;
  5. when cdnjs is blocked, the section falls back to the plain list of places, still with zero page errors.
Screenshots go to docs/design/area-map-3d/shots/component-*.png. python test_area_map.py"""
import json
import os
import pathlib
import re
import sys
import time

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
DOCS = (HERE / '..' / '..' / '..' / 'docs' / 'design' / 'area-map-3d').resolve()
URL = (DOCS / 'component-preview.html').as_uri()
SHOTS = DOCS / 'shots'
HEAVY = re.compile(r'cdnjs\.cloudflare\.com|openfreemap\.org|cdn\.jsdelivr\.net')
ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']

STATE = "(id) => document.getElementById(id).getAttribute('data-state')"
INFO = """(id) => { const r = document.getElementById(id), m = r.__nlamMap, f = r.querySelector('.nlam__frame');
  let ren = -1; try { ren = m && m.getLayer('nlam-ren') ? m.queryRenderedFeatures({layers: ['nlam-ren']}).length : -1 } catch (e) {}
  return { state: r.getAttribute('data-state'), frame_h: Math.round(f.getBoundingClientRect().height),
    pins: r.querySelectorAll('.nlam__pin').length, pins_visible: [...r.querySelectorAll('.nlam__pin')].filter(p => p.offsetParent).length,
    renewal_rendered: ren, chips_disabled: [...r.querySelectorAll('.nlam__chip')].filter(c => c.disabled).length,
    wait_text: (r.querySelector('.nlam__wait') || {}).innerText || '' }; }"""
CARD = """(id) => { const c = document.querySelector('#' + id + ' .nlam__card'); if (c.hidden) return {open: false};
  const b = c.getBoundingClientRect(); return {open: true, text: c.innerText.replace(/\\s+/g, ' ').trim(),
  inside: b.left >= 0 && b.right <= innerWidth && b.top >= 0 && b.bottom <= innerHeight}; }"""
REN_PT = """(a) => { const r = document.getElementById(a[0]), m = r.__nlamMap, d = JSON.parse(r.getAttribute('data-cfg'));
  const x = d.rn.find(o => o.a === a[1]), p = m.project([x.x, x.y]), b = m.getCanvas().getBoundingClientRect();
  return {x: b.left + p.x, y: b.top + p.y}; }"""
IDLE = """(id) => new Promise(res => { const m = document.getElementById(id).__nlamMap; if (!m) return res('no map');
  if (m.loaded() && m.areTilesLoaded()) return res('idle'); m.once('idle', () => res('idle')); setTimeout(() => res('timeout'), 30000); })"""


def wait_ready(page, sid):
    page.wait_for_function("(id) => ['ready','fail'].includes(document.getElementById(id).getAttribute('data-state'))", arg=sid, timeout=60000)
    return page.evaluate(STATE, sid)


def main():
    out = {'checks': [], 'page_errors': [], 'console_errors': [], 'requests': []}
    ok = True

    def check(name, cond, info=None):
        nonlocal ok
        out['checks'].append({'check': name, 'pass': bool(cond), 'info': info})
        ok = ok and bool(cond)

    with sync_playwright() as pw:
        b = pw.chromium.launch(channel='chrome', headless=True, args=ARGS)
        ctx = b.new_context(viewport={'width': 1366, 'height': 900}, locale='he-IL')
        page = ctx.new_page()
        t0 = time.time()
        page.on('pageerror', lambda e: out['page_errors'].append(str(e)))
        page.on('console', lambda m: m.type == 'error' and out['console_errors'].append(m.text))
        page.on('request', lambda r: out['requests'].append({'t': round(time.time() - t0, 2), 'url': r.url[:120]}))

        # 1. nothing heavy before the scroll
        page.goto(URL, wait_until='load')
        page.wait_for_timeout(3000)
        heavy_before = [r for r in out['requests'] if HEAVY.search(r['url'])]
        check('no cdnjs / openfreemap / jsdelivr request before scrolling', not heavy_before, heavy_before[:3])
        i1 = page.evaluate(INFO, 'nlam-d')
        check('first section waits with the calm placeholder and inactive filters',
              i1['state'] == 'wait' and 'המפה נטענת' in i1['wait_text'] and i1['chips_disabled'] == 6, i1)
        page.screenshot(path=str(SHOTS / 'component-0-before-scroll.png'))
        n_before_scroll = len(out['requests'])
        out['scroll_at_s'] = round(time.time() - t0, 2)
        page.locator('#nlam-d .nlam__head').scroll_into_view_if_needed()
        page.wait_for_timeout(100)
        page.locator('#nlam-d .nlam__frame').screenshot(path=str(SHOTS / 'component-1-placeholder.png'))
        h_before = page.evaluate(INFO, 'nlam-d')['frame_h']

        # 2. scroll: it loads
        page.locator('#nlam-d .nlam__frame').scroll_into_view_if_needed()
        st = wait_ready(page, 'nlam-d')
        idle = page.evaluate(IDLE, 'nlam-d')
        page.wait_for_timeout(1200)
        i1 = page.evaluate(INFO, 'nlam-d')
        heavy_after = [r for r in out['requests'][n_before_scroll:] if HEAVY.search(r['url'])]
        check('after scrolling the library, the style and tiles load', st == 'ready' and idle == 'idle' and
              any('maplibre-gl.js' in r['url'] for r in heavy_after) and any('openfreemap' in r['url'] for r in heavy_after),
              {'state': st, 'idle': idle, 'first': heavy_after[:4], 'count': len(heavy_after)})
        check('pins appear: 6 project pins and renewal pins on the map', i1['pins'] == 6 and i1['pins_visible'] >= 1 and i1['renewal_rendered'] > 0, i1)
        check('no layout jump: the frame keeps its height', abs(i1['frame_h'] - h_before) <= 1, {'before': h_before, 'after': i1['frame_h']})
        check('the second section has not started yet (far below)', page.evaluate(STATE, 'nlam-ph') == 'wait')
        page.locator('#nlam-d .nlam__frame').screenshot(path=str(SHOTS / 'component-2-loaded.png'))

        # 3a. a project pin opens its card
        foot = page.locator('#nlam-d .nlam__pin--hero .nlam__pf').bounding_box()
        page.mouse.click(foot['x'] + foot['width'] / 2, foot['y'] + foot['height'] / 2)
        page.wait_for_timeout(1200)
        c1 = page.evaluate(CARD, 'nlam-d')
        check('a project pin opens its card with the link to the project page', c1['open'] and 'לעמוד הפרויקט' in c1['text'] and c1['inside'], c1)
        page.locator('#nlam-d .nlam__frame').screenshot(path=str(SHOTS / 'component-3-card-project.png'))

        # 3b. the phone-frame instance on the same page: loads on its own, a renewal pin opens its card
        page.locator('#nlam-ph .nlam__frame').scroll_into_view_if_needed()
        st2 = wait_ready(page, 'nlam-ph')
        page.evaluate(IDLE, 'nlam-ph')
        page.wait_for_timeout(1200)
        i2 = page.evaluate(INFO, 'nlam-ph')
        check('the 390px instance loads too (two instances, no clash)', st2 == 'ready' and i2['pins'] == 6 and i2['renewal_rendered'] > 0, i2)
        pt = page.evaluate(REN_PT, ['nlam-ph', 'זלוציסטי 4'])
        page.mouse.click(pt['x'], pt['y'])
        page.wait_for_timeout(1200)
        c2 = page.evaluate(CARD, 'nlam-ph')
        check('a renewal pin opens its card (390px frame)', c2['open'] and 'התחדשות עירונית' in c2['text'] and c2['inside'], c2)
        page.locator('#nlam-ph').screenshot(path=str(SHOTS / 'component-4-phone-card-renewal.png'))
        ids = page.evaluate("() => { const a = [...document.querySelectorAll('[id]')].map(e => e.id); return a.filter((x, i) => a.indexOf(x) !== i); }")
        check('no duplicate ids on the page', not ids, ids)
        b.close()

        # 5. cdnjs blocked: the plain list instead of the map
        b = pw.chromium.launch(channel='chrome', headless=True, args=ARGS)
        ctx = b.new_context(viewport={'width': 1366, 'height': 900}, locale='he-IL')
        ctx.route(re.compile(r'.*cdnjs\.cloudflare\.com.*'), lambda r: r.abort())
        page = ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto(URL, wait_until='load')
        page.locator('#nlam-d .nlam__frame').scroll_into_view_if_needed()
        stf = wait_ready(page, 'nlam-d')
        lst = page.evaluate("() => { const r = document.getElementById('nlam-d'); return {open: r.querySelector('.nlam__list').open, "
                            "frame: getComputedStyle(r.querySelector('.nlam__frame')).display, items: r.querySelectorAll('.nlam__list li').length, "
                            "note: getComputedStyle(r.querySelector('.nlam__failnote')).display}; }")
        check('cdnjs blocked: the list of places shows instead of the map', stf == 'fail' and lst['open'] and lst['frame'] == 'none' and
              lst['items'] >= 21 and lst['note'] == 'block' and not errs, {'state': stf, 'list': lst, 'errors': errs})
        page.locator('#nlam-d').screenshot(path=str(SHOTS / 'component-5-fallback-list.png'))
        b.close()

    check('zero page errors and console errors', not out['page_errors'] and not out['console_errors'],
          {'page': out['page_errors'], 'console': out['console_errors']})
    heavy = [r for r in out['requests'] if HEAVY.search(r['url'])]
    out['first_heavy_request'] = heavy[0] if heavy else None
    out['heavy_requests'] = len(heavy)
    del out['requests']
    print(json.dumps(out, ensure_ascii=False, indent=1))
    json.dump(out, open(SHOTS / 'component-report.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('ALL PASS' if ok else 'FAILED')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
