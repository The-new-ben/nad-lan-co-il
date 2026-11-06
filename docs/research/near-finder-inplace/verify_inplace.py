"""Near finder in place (6.11.2026): local verification on the LIVE pages, nothing deployed.

For each page x width: the live page as it is (before), then the same live page with the edited finder.js / finder.css served by
route interception and the footer block (#nlnf-lidi) swapped for what the edited PHP prints (footer_new.json, made by
render_footer.php from the real nadlan_nf_launcher()). Checks: no floating launcher, the switch both ways, the finder loads in
place, "מסך מלא" opens the dialog and Escape returns the app, #lidi, console errors, horizontal scroll, control sizes, CLS.
Run: python verify_inplace.py  (writes results.json and shots/)
"""
import asyncio, json, pathlib, re, sys, time
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
ASSET = REPO / 'plugins' / 'nadlan-config' / 'assets' / 'near-finder'
SHOTS = HERE / 'shots'
SHOTS.mkdir(exist_ok=True)
FOOT = json.loads((HERE / 'footer_new.json').read_text(encoding='utf-8'))
JS = (ASSET / 'finder.js').read_bytes()
CSS = (ASSET / 'finder.css').read_bytes()

PAGES = {
    'home': {'url': 'https://nad-lan.co.il/', 'kind': 'proj', 'sec': '.nlhp-mapband', 'end': '.nlhp-mapband', 'anchor': '#nldrone-stage'},
    'properties': {'url': 'https://nad-lan.co.il/properties/', 'kind': 'inline', 'sec': '#nlnf', 'end': '#nlnf', 'anchor': '#nlnf'},
    'rent': {'url': 'https://nad-lan.co.il/%D7%93%D7%99%D7%A8%D7%95%D7%AA-%D7%9C%D7%94%D7%A9%D7%9B%D7%A8%D7%94/', 'kind': 'list',
             'sec': 'h2#listings', 'end': '.nlrh-list', 'anchor': '.nlrh-list .nlrh-count'},
    'broker': {'url': 'https://nad-lan.co.il/brokers/meital-katzir/', 'kind': 'nlb', 'sec': 'section#listings', 'end': 'section#listings', 'anchor': 'section#listings .nlb-grid'},
}
VPS = {
    'm390': dict(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=2),
    'd1280': dict(viewport={'width': 1280, 'height': 900}),
}
INIT = r"""
window.__cls = 0; window.__shifts = [];
try {
  new PerformanceObserver(function (l) {
    l.getEntries().forEach(function (e) {
      if (e.hadRecentInput) { return; }
      window.__cls += e.value;
      window.__shifts.push({ v: +e.value.toFixed(5), t: Math.round(e.startTime), src: (e.sources || []).map(function (s) {
        var n = s.node; if (!n) { return '?'; }
        var c = (n.className && typeof n.className === 'string') ? '.' + n.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
        return n.nodeName + (n.id ? '#' + n.id : '') + c; }) });
    });
  }).observe({ type: 'layout-shift', buffered: true });
} catch (e) {}
"""


def swap_footer(html, new):
    i = html.find('<div class="nlnf nlnf-lidi" id="nlnf-lidi"')
    if i < 0:
        raise RuntimeError('no #nlnf-lidi in the live HTML')
    depth = 0
    for m in re.finditer(r'<div\b|</div>', html[i:]):
        depth += -1 if m.group(0) == '</div>' else 1
        if depth == 0:
            return html[:i] + new + html[i + m.end():]
    raise RuntimeError('unbalanced #nlnf-lidi')


async def route_after(page, name, block_js=False):
    base = PAGES[name]['url'].split('#')[0]

    async def handler(route):
        req = route.request
        u = req.url
        if 'near-finder/finder.js' in u:
            if block_js:
                return await route.abort()
            return await route.fulfill(status=200, body=JS, headers={'content-type': 'application/javascript; charset=utf-8', 'cache-control': 'no-store'})
        if 'near-finder/finder.css' in u:
            return await route.fulfill(status=200, body=CSS, headers={'content-type': 'text/css; charset=utf-8', 'cache-control': 'no-store'})
        if req.resource_type == 'document' and u.split('?')[0] == base:
            r = None
            for attempt in range(4):  # the live server drops a connection now and then ("socket hang up")
                try:
                    r = await route.fetch(timeout=60000)
                    break
                except Exception:
                    await asyncio.sleep(2 + attempt * 3)
            if r is None:
                return await route.abort()
            html = (await r.body()).decode('utf-8')
            html = swap_footer(html, FOOT[name])
            h = dict(r.headers)
            for k in list(h):
                if k.lower() in ('content-length', 'content-encoding', 'transfer-encoding'):
                    h.pop(k)
            return await route.fulfill(status=r.status, headers=h, body=html.encode('utf-8'))
        return await route.continue_()
    await page.route('**/*', handler)


async def doc_rect(page, sel):
    return await page.evaluate("""(s) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
        return { top: Math.round(r.top + scrollY), bottom: Math.round(r.bottom + scrollY), h: Math.round(r.height), w: Math.round(r.width), left: Math.round(r.left) }; }""", sel)


async def shot_section(page, name, tag):
    p = PAGES[name]
    a = await doc_rect(page, p['sec'])
    b = await doc_rect(page, p['end'])
    if not a or not b:
        return None
    vw = page.viewport_size['width']
    top = max(0, a['top'] - 24)
    h = min(max(b['bottom'], a['bottom']) + 24 - top, 2200)
    await page.evaluate('(y) => window.scrollTo(0, y)', max(0, top - 80))
    await page.wait_for_timeout(700)
    f = SHOTS / f'{name}-{tag}.png'
    await page.screenshot(path=str(f), full_page=True, clip={'x': 0, 'y': top, 'width': vw, 'height': h})
    return str(f.relative_to(HERE))


async def common(page):
    return await page.evaluate("""() => {
        const l = document.getElementById('nlnf-launch');
        let launchVisible = false;
        if (l) { const r = l.getBoundingClientRect(), cs = getComputedStyle(l); launchVisible = r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.05; }
        const fixed = [...document.querySelectorAll('.nlnf *, .nlnf, .nlnf-sw *')].filter(n => getComputedStyle(n).position === 'fixed' && n.getBoundingClientRect().width > 0).map(n => n.id || n.className);
        return { launchExists: !!l, launchVisible, hScroll: document.documentElement.scrollWidth - window.innerWidth, fixedVisible: fixed, cls: +window.__cls.toFixed(5), shifts: window.__shifts.slice(0, 12) };
    }""")


async def wait_results(page, timeout=25000):
    t0 = time.time()
    while (time.time() - t0) * 1000 < timeout:
        st = await page.evaluate("""() => { const c = document.getElementById('nlnf-count'); const rows = document.querySelectorAll('#nlnf-list > li').length;
            const app = document.getElementById('nlnf-app');
            return { count: c ? c.textContent.trim() : null, rows, nomap: !!(app && app.classList.contains('nlnf--nomap')), canvas: !!document.querySelector('#nlnf-map canvas'),
                     pins: document.querySelectorAll('#nlnf-map .nlnf-pin').length }; }""")
        if st['rows'] > 0 and st['count'] and 'נטענות' not in st['count']:
            await page.wait_for_timeout(1200)
            st2 = await page.evaluate("""() => ({ pins: document.querySelectorAll('#nlnf-map .nlnf-pin').length, canvas: !!document.querySelector('#nlnf-map canvas') })""")
            st.update(st2)
            return st
        await page.wait_for_timeout(400)
    return st


async def run_one(ctx, name, vp, res):
    p = PAGES[name]
    out = res.setdefault(name, {}).setdefault(vp, {})
    errs = {'live': [], 'after': [], 'lidi': []}

    def watch(page, key):
        page.on('console', lambda m: errs[key].append(m.text[:300]) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errs[key].append('pageerror: ' + str(e)[:300]))

    cb = str(int(time.time()))
    # ---------------- before (live)
    page = await ctx.new_page()
    watch(page, 'live')
    await page.goto(p['url'] + '?cb=' + cb, wait_until='load', timeout=90000)
    await page.wait_for_timeout(3500)
    out['live'] = await common(page)
    await page.screenshot(path=str(SHOTS / f'{name}-{vp}-live-first.png'))
    out['live']['shot_first'] = f'shots/{name}-{vp}-live-first.png'
    out['live']['shot_section'] = await shot_section(page, name, f'{vp}-live-section')
    if out['live']['launchExists']:  # the live finder's own count, opened from its launcher (or the inline section on /properties/)
        try:
            await page.evaluate("() => { const b = document.getElementById('nlnf-launch'); if (b) { b.hidden = false; b.classList.remove('is-away'); b.click(); } }")
            out['live']['finder'] = await wait_results(page)
            await page.screenshot(path=str(SHOTS / f'{name}-{vp}-live-dialog.png'))
            out['live']['shot_dialog'] = f'shots/{name}-{vp}-live-dialog.png'
        except Exception as e:
            out['live']['finder_err'] = str(e)[:200]
    await page.close()

    # ---------------- after, finder.js blocked: where the section's content sits with only the held height (CSS)
    page = await ctx.new_page()
    await route_after(page, name, block_js=True)
    await page.goto(p['url'] + '?cb=' + cb, wait_until='load', timeout=90000)
    await page.wait_for_timeout(2500)
    out['nojs_anchor'] = await doc_rect(page, p['anchor'])
    await page.close()

    # ---------------- after (the edited files)
    page = await ctx.new_page()
    watch(page, 'after')
    await route_after(page, name)
    await page.goto(p['url'] + '?cb=' + cb, wait_until='load', timeout=90000)
    await page.wait_for_timeout(3500)
    a = out['after'] = await common(page)
    a['anchor'] = await doc_rect(page, p['anchor'])
    a['anchor_same_as_nojs'] = bool(out['nojs_anchor'] and a['anchor'] and abs(out['nojs_anchor']['top'] - a['anchor']['top']) <= 1)
    a['holder'] = await page.evaluate("() => { const h = document.getElementById('nlnf-hold'); return h ? { hidden: h.hidden, visible: h.getBoundingClientRect().height > 0 } : null; }")
    await page.screenshot(path=str(SHOTS / f'{name}-{vp}-after-first.png'))
    a['shot_first'] = f'shots/{name}-{vp}-after-first.png'
    if p['kind'] != 'inline':
        sw = await page.evaluate("""() => { const r = document.querySelector('.nlnf-sw'); if (!r) return null;
            return { kind: r.className, buttons: [...r.querySelectorAll('.nlnf-sw__b')].map(b => ({ t: b.textContent, pressed: b.getAttribute('aria-pressed'), h: Math.round(b.getBoundingClientRect().height), w: Math.round(b.getBoundingClientRect().width) })),
                     rowH: Math.round(r.getBoundingClientRect().height) }; }""")
        a['switch'] = sw
        a['shot_section_list'] = await shot_section(page, name, f'{vp}-after-section-list')
        if sw:
            await page.click('.nlnf-sw__b[data-v="map"]')
            a['finder'] = await wait_results(page)
            a['map_view'] = await page.evaluate("""() => { const st = document.getElementById('nldrone-stage'), app = document.getElementById('nlnf-app');
                const vis = e => !!e && e.getBoundingClientRect().height > 0;
                return { app_visible: vis(app), app_in_host: !!(app && app.closest('.nlnf--host')), app_h: app ? Math.round(app.getBoundingClientRect().height) : 0,
                         stage_visible: st ? vis(st) : null, grid_visible: vis(document.querySelector('.nlb-grid')) || vis(document.querySelector('.nlrh-list .nlpl-grid')),
                         pressed: [...document.querySelectorAll('.nlnf-sw__b')].map(b => b.getAttribute('aria-pressed')),
                         hScroll: document.documentElement.scrollWidth - window.innerWidth }; }""")
            a['shot_section_map'] = await shot_section(page, name, f'{vp}-after-section-map')
    else:
        a['finder'] = None
        await page.evaluate("() => document.getElementById('nlnf').scrollIntoView()")
        a['finder'] = await wait_results(page)
        a['shot_section_map'] = await shot_section(page, name, f'{vp}-after-section-map')
    # full screen and back
    fs = await page.evaluate("() => { const b = document.getElementById('nlnf-fs'); if (!b) return null; const r = b.getBoundingClientRect(); return { hidden: b.hidden, h: Math.round(r.height), w: Math.round(r.width), visible: r.height > 0 }; }")
    a['fs'] = fs
    if fs and fs['visible']:
        url0 = page.url
        await page.evaluate("() => document.getElementById('nlnf-fs').scrollIntoView({ block: 'center' })")
        await page.click('#nlnf-fs')
        await page.wait_for_timeout(1500)
        a['fs_open'] = await page.evaluate("""() => ({ dlg: !document.getElementById('nlnf-dlg').hidden, inDlg: !!document.getElementById('nlnf-app').closest('.nlnf-dlg'),
                    hash: location.hash, sheet: document.getElementById('nlnf-app').classList.contains('is-sheet'), fsBtnVisible: document.getElementById('nlnf-fs').getBoundingClientRect().height > 0 })""")
        await page.screenshot(path=str(SHOTS / f'{name}-{vp}-after-fullscreen.png'))
        a['shot_fullscreen'] = f'shots/{name}-{vp}-after-fullscreen.png'
        await page.keyboard.press('Escape')
        await page.wait_for_timeout(1000)
        a['fs_closed'] = await page.evaluate("""() => ({ dlg: !document.getElementById('nlnf-dlg').hidden, back: !!document.getElementById('nlnf-app').closest(%s), hash: location.hash,
                    htmlOpen: document.documentElement.classList.contains('nlnf-open'), bodyOverflow: document.body.style.overflow })""" % ("'.nlnf--host'" if p['kind'] != 'inline' else "'#nlnf'"))
        a['fs_closed']['url_same'] = page.url == url0
    if p['kind'] != 'inline' and a.get('switch'):
        await page.click('.nlnf-sw__b[data-v="list"]')
        await page.wait_for_timeout(700)
        a['list_again'] = await page.evaluate("""() => { const st = document.getElementById('nldrone-stage'), app = document.getElementById('nlnf-app');
            const vis = e => !!e && e.getBoundingClientRect().height > 0;
            return { app_visible: vis(app), stage_visible: st ? vis(st) : null,
                     list_visible: st ? vis(st) : (vis(document.querySelector('.nlb-grid')) || vis(document.querySelector('.nlrh-list .nlpl-grid'))),
                     pressed: [...document.querySelectorAll('.nlnf-sw__b')].map(b => b.getAttribute('aria-pressed')),
                     droneCanvasH: (() => { const c = document.querySelector('#nldrone-map canvas'); return c ? Math.round(c.getBoundingClientRect().height) : null; })() }; }""")
    a['hScroll_end'] = await page.evaluate('() => document.documentElement.scrollWidth - window.innerWidth')
    await page.close()

    # ---------------- #lidi deep link
    page = await ctx.new_page()
    watch(page, 'lidi')
    await route_after(page, name)
    await page.goto(p['url'] + '?cb=' + cb + '#lidi', wait_until='load', timeout=90000)
    await page.wait_for_timeout(3000)
    out['lidi'] = await page.evaluate("""() => { const t = document.querySelector('.nlnf-sw') || document.getElementById('nlnf'); const r = t ? t.getBoundingClientRect() : null;
        return { dlg_open: !document.getElementById('nlnf-dlg').hidden, pressed: [...document.querySelectorAll('.nlnf-sw__b')].map(b => b.getAttribute('aria-pressed')),
                 target_top_in_view: r ? Math.round(r.top) : null, scrollY: Math.round(scrollY), app_visible: (() => { const a = document.getElementById('nlnf-app'); return !!a && a.getBoundingClientRect().height > 0; })() }; }""")
    await page.screenshot(path=str(SHOTS / f'{name}-{vp}-after-lidi.png'))
    out['lidi']['shot'] = f'shots/{name}-{vp}-after-lidi.png'
    await page.close()
    out['errors'] = errs


async def main():
    only = sys.argv[1:]  # optional: page names
    res = {}
    async with async_playwright() as pw:
        br = await pw.chromium.launch(channel='chrome', headless=True, args=['--enable-unsafe-swiftshader', '--use-angle=swiftshader'])
        for vp, opts in VPS.items():
            for name in PAGES:
                if only and name not in only:
                    continue
                ctx = await br.new_context(locale='he-IL', geolocation={'latitude': 32.0853, 'longitude': 34.7818}, permissions=['geolocation'],
                                           user_agent=None, **opts)
                await ctx.add_init_script(INIT)
                try:
                    await run_one(ctx, name, vp, res)
                except Exception as e:
                    res.setdefault(name, {}).setdefault(vp, {})['fatal'] = repr(e)[:400]
                await ctx.close()
                print(name, vp, 'done', flush=True)
        await br.close()
    fn = HERE / ('results.json' if not only else 'results-' + '-'.join(only) + '.json')
    fn.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print('wrote', fn)

if __name__ == '__main__':
    asyncio.run(main())
