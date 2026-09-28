"""TogetherRoom harness (design system TogetherRoom v77, 28.9.2026).

Runs the room over the LIVE Rainbow stage without touching the live site's code or data:
  - the live page https://nad-lan.co.il/projects/rainbow-tel-aviv/ is fetched (a plain read), and Playwright route
    interception swaps in the working tree's bridge.js, rainbow/stage.js, tour.js and assets/together/*;
  - the room's container and script are the ones inc/together.php prints (rendered by scripts/together/router.php on the
    WordPress stand-in), and every /wp-json/nadlan/v1/room... call goes to that same PHP, never to the live server;
  - analytics calls are answered locally with an empty 204 (no test traffic in the owner's data).

Two browser contexts (the representative and a buyer, 1440x900) and a phone (a partner, 390x844) sync the view, the mode
and the notes in the fallback mode (no LiveKit key). Screenshots and a JSON report go to --out.

  python scripts/together/harness.py --out <folder>
Needs: Python Playwright, Google Chrome, PHP 8 (C:/Users/777/tools/php-8.3/php by default, or --php).
"""
import argparse
import asyncio
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request

from playwright.async_api import async_playwright

REPO = pathlib.Path(__file__).resolve().parents[2]
PLUGIN = REPO / 'plugins' / 'nadlan-config'
PAGE = 'https://nad-lan.co.il/projects/rainbow-tel-aviv/'
CHROME = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
PORT = 8765
PHP_BASE = f'http://127.0.0.1:{PORT}'
LOCAL = {
    '/assets/project-stage/bridge.js': PLUGIN / 'assets/project-stage/bridge.js',
    '/assets/project-stage/tour.js': PLUGIN / 'assets/project-stage/tour.js',
    '/assets/project-stage/rainbow/stage.js': PLUGIN / 'assets/project-stage/rainbow/stage.js',
    '/assets/together/together.js': PLUGIN / 'assets/together/together.js',
    '/assets/together/together.css': PLUGIN / 'assets/together/together.css',
}
QUIET = ('google-analytics.com', 'googletagmanager.com', 'hotjar', 'clarity.ms', 'facebook.net', 'facebook.com/tr', 'doubleclick')


def php_get(path):
    with urllib.request.urlopen(PHP_BASE + path, timeout=20) as r:
        return r.read().decode('utf-8')


class Harness:
    def __init__(self, out):
        self.out = out
        self.report = {'checks': [], 'console': {}, 'shots': []}
        self.page_html = None

    def check(self, ok, what, detail=None):
        self.report['checks'].append({'ok': bool(ok), 'what': what, 'detail': detail})
        print(('  ok   ' if ok else '  FAIL ') + what + ('' if detail is None else f'  [{detail}]'), flush=True)

    async def shot(self, page, name, full=False):
        p = self.out / name
        await page.screenshot(path=str(p), full_page=full)
        self.report['shots'].append(str(p))
        print('  shot', p, flush=True)

    async def live_html(self, route):
        if self.page_html is None:
            resp = await route.fetch(url=PAGE)
            self.page_html = await resp.text()
        return self.page_html

    async def context(self, browser, who, ip, mobile=False):
        opts = {'viewport': {'width': 390, 'height': 844} if mobile else {'width': 1440, 'height': 900}, 'locale': 'he-IL'}
        if mobile:
            opts.update(is_mobile=True, has_touch=True, device_scale_factor=1,
                        user_agent='Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Mobile Safari/537.36')
        ctx = await browser.new_context(**opts)
        rep = who == 'rep'

        async def doc(route):
            req = route.request
            if req.resource_type != 'document':
                await route.continue_()
                return
            html = await self.live_html(route)
            q = urllib.parse.urlsplit(req.url).query
            flag = '&rep=1' if rep else ''
            head = php_get('/__head?' + q + flag)
            foot = php_get('/__footer?' + q + flag)
            body = html.replace('</head>', head + '</head>', 1).replace('</body>', foot + '</body>', 1)
            await route.fulfill(status=200, content_type='text/html; charset=utf-8', body=body)

        async def local(route):
            path = urllib.parse.urlsplit(route.request.url).path
            for key, f in LOCAL.items():
                if path.endswith(key):
                    ctype = 'text/css' if key.endswith('.css') else 'text/javascript'
                    await route.fulfill(status=200, content_type=ctype + '; charset=utf-8', body=f.read_text(encoding='utf-8'))
                    return
            await route.continue_()

        async def rest(route):
            req = route.request
            u = urllib.parse.urlsplit(req.url)
            headers = {'X-Test-IP': ip, 'Content-Type': 'application/json'}
            nonce = req.headers.get('x-wp-nonce')
            if nonce:
                headers['X-WP-Nonce'] = nonce
            data = req.post_data.encode('utf-8') if req.post_data else None
            r = urllib.request.Request(PHP_BASE + u.path + ('?' + u.query if u.query else ''), data=data, method=req.method, headers=headers)
            try:
                with urllib.request.urlopen(r, timeout=20) as resp:
                    status, body = resp.status, resp.read()
            except urllib.error.HTTPError as e:
                status, body = e.code, e.read()
            await route.fulfill(status=status, content_type='application/json; charset=utf-8', body=body)

        async def quiet(route):
            await route.fulfill(status=204, body='')

        await ctx.route(PAGE + '**', doc)
        await ctx.route('**/wp-content/plugins/nadlan-config/assets/**', local)
        await ctx.route('https://nad-lan.co.il/wp-json/nadlan/v1/room**', rest)
        await ctx.route(lambda url: any(q in url for q in QUIET), quiet)
        return ctx

    def watch(self, page, who):
        log = self.report['console'].setdefault(who, [])
        page.on('console', lambda m: log.append({'type': m.type, 'text': m.text[:300]}) if m.type in ('error', 'warning') else None)
        page.on('pageerror', lambda e: log.append({'type': 'pageerror', 'text': str(e)[:300]}))

    async def stage_ready(self, page):
        await page.wait_for_function("() => window.__nlpsStage && window.__nlpsStage.phase === 'orbit'", timeout=90000)

    async def join(self, page, name, role=None):
        await page.wait_for_selector('#nltg-name', timeout=60000)
        await page.fill('#nltg-name', name)
        if role:
            await page.click(f'.nltg-roles button[data-role="{role}"]')
        await page.click('.nltg-card .go')
        await page.wait_for_selector('.nltg-dock', timeout=30000)

    async def run(self):
        php = subprocess.Popen([self.php, '-S', f'127.0.0.1:{PORT}', str(REPO / 'scripts/together/router.php')], cwd=str(REPO),
                               env=dict(os.environ, NLTR_STORE=str(pathlib.Path(tempfile.gettempdir()) / 'nltg-harness.json')),
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(50):
                try:
                    php_get('/__reset?rep_now=1')
                    break
                except Exception:
                    time.sleep(0.2)
            async with async_playwright() as p:
                browser = await p.chromium.launch(executable_path=CHROME, args=['--use-gl=angle', '--enable-webgl', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'])
                await self.scenario(browser)
                await browser.close()
        finally:
            php.terminate()
        (self.out / 'report.json').write_text(json.dumps(self.report, ensure_ascii=False, indent=1), encoding='utf-8')
        fails = [c for c in self.report['checks'] if not c['ok']]
        print(f"\n{len(self.report['checks'])} checks, {len(fails)} failed; report: {self.out / 'report.json'}")
        return 1 if fails else 0

    async def scenario(self, browser):
        H = self
        # ---------------- the representative opens a room (?room=new, logged in with edit_posts)
        print('the representative', flush=True)
        rctx = await self.context(browser, 'rep', '10.1.0.1')
        rep = await rctx.new_page()
        self.watch(rep, 'rep')
        await rep.goto(PAGE + '?room=new', wait_until='domcontentloaded', timeout=120000)
        await rep.wait_for_selector('#nltg-name', timeout=60000)
        room = urllib.parse.parse_qs(urllib.parse.urlsplit(rep.url).query).get('room', [''])[0]
        H.check(len(room) == 12 and room != 'new', '?room=new created a room and the address now carries it', room)
        H.check(await rep.input_value('#nltg-name') == 'דנה', 'the representative\'s name is filled in')
        H.check(await rep.get_attribute('.nltg-roles button[data-role="rep"]', 'aria-checked') == 'true', 'the role is the representative')
        await self.stage_ready(rep)
        await rep.wait_for_timeout(1500)
        await self.shot(rep, '01-join-rep-1440.png')
        await rep.click('.nltg-card .go')
        await rep.wait_for_selector('.nltg-dock')
        await rep.wait_for_selector('.nltg-pop', timeout=5000)
        H.check(room in (await rep.input_value('.nltg-pop input')), 'the representative\'s console: the join link is ready to copy')
        await rep.click('.nltg-pop .nltg-btn.ghost')

        # ---------------- a buyer joins from the link
        print('the buyer', flush=True)
        bctx = await self.context(browser, 'buyer', '10.2.0.1')
        buyer = await bctx.new_page()
        self.watch(buyer, 'buyer')
        await buyer.goto(PAGE + '?room=' + room, wait_until='domcontentloaded', timeout=120000)
        await buyer.wait_for_selector('#nltg-name', timeout=60000)
        roles = await buyer.eval_on_selector_all('.nltg-roles button', 'els => els.map(e => e.dataset.role)')
        H.check('rep' not in roles and roles[:1] == ['buyer'], 'a visitor cannot pick the representative role', roles)
        consent = await buyer.text_content('.nltg-card .consent')
        H.check(consent == 'השיחה אינה מוקלטת. ההערות נשמרות בתיק הדירה. השיחה היא עם צוות נדל״ן, פלטפורמה עצמאית, ואינה מטעם היזם. שינויים בדירה כפופים לאישור היזם.', 'the consent line, word for word')
        await self.stage_ready(buyer)
        await buyer.fill('#nltg-name', 'יואב')
        await buyer.wait_for_timeout(800)
        await self.shot(buyer, '02-join-buyer-1440.png')
        await buyer.click('.nltg-card .go')
        await buyer.wait_for_selector('.nltg-dock')
        await buyer.wait_for_timeout(2000)
        chips = await rep.eval_on_selector_all('.nltg-people .nltg-chip', 'els => els.map(e => e.textContent)')
        H.check(any('יואב' in c for c in chips), 'the representative sees the buyer in the room', chips)

        # ---------------- "עקבו אחריי": the representative leads; the buyer follows
        print('following', flush=True)
        await rep.click('.nltg-ctl .nltg-btn.teal')
        await buyer.wait_for_function("() => document.querySelector('.nltg-follow') && document.querySelector('.nltg-follow').textContent.includes('דנה')", timeout=8000)
        H.check(True, 'the buyer sees "כולם רואים את מה שדנה מראה"')
        await rep.evaluate("() => window.__nlpsStage.selectUnit('25-w', 'user')")
        await buyer.wait_for_function("() => { const s = window.__nlpsStage.getSelection(); return s && s.unit === '25-w'; }", timeout=8000)
        H.check(True, 'the representative picks floor 25 toward the sea; the buyer\'s stage picks it too')
        # a real drag on the representative's stage
        box = await rep.eval_on_selector('#nlps canvas', 'c => { const r = c.getBoundingClientRect(); return {x: r.left + r.width * .62, y: r.top + r.height * .55}; }')
        await rep.wait_for_timeout(1500)
        await rep.mouse.move(box['x'], box['y'])
        await rep.mouse.down()
        for i in range(12):
            await rep.mouse.move(box['x'] - 18 * (i + 1), box['y'] + 2 * i)
            await rep.wait_for_timeout(16)
        await rep.mouse.up()
        await rep.wait_for_timeout(1200)
        rv = await rep.evaluate('() => window.__nlpsStage.getView()')
        await buyer.wait_for_timeout(3500)
        bv = await buyer.evaluate('() => window.__nlpsStage.getView()')
        dth = abs(rv['theta'] - bv['theta'])
        H.check(dth < 0.05 and abs(rv['r'] - bv['r']) < max(8, rv['r'] * 0.05), 'the buyer\'s camera follows the representative\'s drag', {'rep': rv, 'buyer': bv})

        # ---------------- a note on the tower (building mode), by the representative
        print('notes', flush=True)
        await rep.click('.nltg-list .nltg-add')
        pt = await rep.evaluate("() => { const e = window.__nlpsStage._engine(); return e._floorScreenPoint(27); }")
        await rep.mouse.click(pt['x'], pt['y'])
        await rep.wait_for_selector('.nltg-compose textarea')
        where = await rep.input_value('.nltg-compose input.nltg-in')
        H.check('קומה' in where, 'the note\'s place is filled in from the tap', where)
        await rep.fill('.nltg-compose textarea', 'חזית המגדל בקומה הזו: מרפסות לכיוון הים')
        await rep.click('.nltg-compose .nltg-btn.teal')
        await rep.wait_for_selector('.nltg-list .nltg-note')
        await buyer.wait_for_function("() => [...document.querySelectorAll('.nltg-list .nltg-note')].some(n => n.textContent.includes('מרפסות'))", timeout=8000)
        H.check(True, 'the buyer receives the representative\'s note')
        pins = await buyer.eval_on_selector_all('.nltg-pin:not([hidden])', 'els => els.length')
        H.check(pins >= 1, 'the note\'s pin stands on the buyer\'s stage', pins)
        await rep.mouse.move(box['x'] - 60, box['y'] - 120)
        await rep.wait_for_timeout(2600)
        await self.shot(rep, '03-rep-building-1440.png')
        await self.shot(buyer, '04-buyer-building-1440.png')

        # ---------------- the mode "בתוך הדירה": the 360 viewer on both sides
        print('inside', flush=True)
        await rep.click('.nltg-modes button[data-mode="inside"]')
        await rep.wait_for_function('() => window.__nlTour', timeout=20000)
        await buyer.wait_for_function('() => window.__nlTour', timeout=20000)
        H.check(True, 'the representative switches to "בתוך הדירה"; the buyer\'s 360 viewer opens')
        await rep.wait_for_timeout(2500)
        sbox = await rep.eval_on_selector('.nlat-viewer__stage', 'c => { const r = c.getBoundingClientRect(); return {x: r.left + r.width * .6, y: r.top + r.height * .5}; }')
        await rep.mouse.move(sbox['x'], sbox['y'])
        await rep.mouse.down()
        for i in range(10):
            await rep.mouse.move(sbox['x'] + 14 * (i + 1), sbox['y'])
            await rep.wait_for_timeout(16)
        await rep.mouse.up()
        await rep.wait_for_timeout(1500)
        ry = await rep.evaluate('() => window.__nlTour.getView()')
        await buyer.wait_for_timeout(3500)
        by = await buyer.evaluate('() => window.__nlTour.getView()')
        dy = abs(((ry['yaw'] - by['yaw'] + 3.14159) % 6.28318) - 3.14159)
        H.check(ry['scene'] == by['scene'] and dy < 0.05, 'the buyer\'s 360 view follows the representative\'s look', {'rep': ry, 'buyer': by})
        # the buyer pins a note inside the apartment (a change to the apartment)
        await buyer.click('.nltg-list .nltg-add')
        await buyer.mouse.click(900, 470)
        await buyer.wait_for_selector('.nltg-compose textarea')
        where2 = await buyer.input_value('.nltg-compose input.nltg-in')
        H.check(where2.startswith('סלון'), 'inside the apartment the place reads "סלון · ..."', where2)
        await buyer.fill('.nltg-compose textarea', 'נקודת חשמל ליד החלון, 40 ס״מ מהרצפה')
        await buyer.click('.nltg-compose .nltg-btn.teal')
        await buyer.wait_for_timeout(600)
        await buyer.click('.nltg-list .nltg-add')
        await buyer.mouse.click(760, 640)
        await buyer.wait_for_selector('.nltg-compose textarea')
        await buyer.fill('.nltg-compose textarea', 'פרקט עץ במקום האריחים?')
        await buyer.check('.nltg-compose input[type=checkbox]')
        await buyer.click('.nltg-compose .nltg-btn.teal')
        await rep.wait_for_function("() => [...document.querySelectorAll('.nltg-list .nltg-note')].some(n => n.textContent.includes('כפוף לאישור היזם'))", timeout=8000)
        H.check(True, 'the representative receives the buyer\'s notes; a change reads "כפוף לאישור היזם"')
        await buyer.click('.nltg-list .nltg-note[data-id]:nth-child(2)')  # the buyer's own note in focus: its label on the view
        H.check(await buyer.is_visible('.nltg-pin-label'), 'a note in focus shows its text beside its pin')
        if await buyer.query_selector('button.nltg-follow'):  # looking at a note of one's own is looking away: back to the leader
            H.check(True, 'a follower who looks away gets "חזרה למה שדנה מראה"')
            await buyer.click('button.nltg-follow')
        for i in range(4):  # the representative's hand over the window, talking about it
            await rep.mouse.move(sbox['x'] + 40 + 6 * i, sbox['y'] + 30)
            await rep.wait_for_timeout(400)
        try:  # the fallback's latency: the leader posts at most every 0.8 s, the others poll every 1.5 s
            await buyer.wait_for_function("() => { const e = document.querySelector('.nltg-pointer'); return e && !e.hidden && e.textContent === 'דנה'; }", timeout=10000)
            ptr = True
        except Exception:
            ptr = False
        H.check(ptr, 'the representative\'s pointer, with the name, on the buyer\'s screen')
        await self.shot(rep, '05-rep-inside-1440.png')
        await self.shot(buyer, '06-buyer-inside-1440.png')

        # ---------------- a partner on a phone (390x844)
        print('the phone', flush=True)
        mctx = await self.context(browser, 'partner', '10.3.0.1', mobile=True)
        phone = await mctx.new_page()
        self.watch(phone, 'partner')
        await phone.goto(PAGE + '?room=' + room, wait_until='domcontentloaded', timeout=120000)
        await phone.wait_for_selector('#nltg-name', timeout=60000)
        await phone.wait_for_timeout(1500)
        await self.shot(phone, '07-phone-join-390.png')
        await self.join(phone, 'מיכל', 'partner')
        await phone.wait_for_function('() => window.__nlTour', timeout=25000)
        H.check(True, 'the phone joins and follows into "בתוך הדירה"')
        await phone.wait_for_timeout(4000)
        # the hit area: the box, grown by a positioned ::before / ::after with negative insets (the design's 34px pin, 40px tabs)
        sizes = await phone.evaluate("""() => [...document.querySelectorAll('.nltg button, .nltg a.nltg-btn')].filter(b => b.offsetParent && getComputedStyle(b).visibility !== 'hidden')
          .map(b => { const r = b.getBoundingClientRect(); let hh = r.height, ww = r.width;
            for (const pe of ['::before', '::after']) { const c = getComputedStyle(b, pe); if (c.content === 'none' || c.position !== 'absolute') continue;
              const px = (v) => parseFloat(v) || 0; hh = Math.max(hh, r.height - px(c.top) - px(c.bottom)); ww = Math.max(ww, r.width - px(c.left) - px(c.right)); }
            return {t: (b.textContent || b.getAttribute('aria-label') || '').trim().slice(0, 24), h: Math.round(hh), w: Math.round(ww)}; })""")
        small = [s for s in sizes if s['h'] < 48 and s['w'] > 0]
        H.check(not small, 'every visible phone control has a 48px target', small or len(sizes))
        await self.shot(phone, '08-phone-inside-390.png')

        # ---------------- the plan and the section; the view from the floor
        print('plan and view', flush=True)
        await rep.click('.nltg-modes button[data-mode="plan"]')
        await buyer.wait_for_function("() => window.__nlTogether.state.mode === 'plan'", timeout=8000)
        H.check(True, 'the representative shows "התוכנית והחתכים"; the buyer follows')
        await rep.wait_for_timeout(800)
        await rep.click('.nltg-list .nltg-add')
        pr = await rep.eval_on_selector('.nltg-plan svg.big', 'e => { const r = e.getBoundingClientRect(); return {x: r.left + r.width * .82, y: r.top + r.height * .35}; }')
        await rep.mouse.click(pr['x'], pr['y'])
        await rep.wait_for_selector('.nltg-compose textarea')
        await rep.fill('.nltg-compose textarea', 'חדר עבודה: שקע רשת ליד הקיר')
        await rep.click('.nltg-compose .nltg-btn.teal')
        await buyer.wait_for_timeout(3500)
        await self.shot(buyer, '09-buyer-plan-1440.png')
        await phone.wait_for_timeout(500)
        await self.shot(phone, '10-phone-plan-390.png')
        await rep.click('.nltg-modes button[data-mode="view"]')
        await buyer.wait_for_function("() => window.__nlTogether.state.mode === 'view'", timeout=10000)
        await rep.wait_for_timeout(6000)
        H.check(await rep.evaluate('() => !!(window.__nlpsView && window.__nlpsView.getView())'), 'the mode "הנוף": the view from the floor, full screen')
        await self.shot(rep, '11-rep-view-1440.png')
        await rep.click('.nltg-modes button[data-mode="building"]')
        await phone.wait_for_function("() => window.__nlTogether.state.mode === 'building'", timeout=10000)
        await phone.wait_for_timeout(3000)
        await self.shot(phone, '12-phone-building-390.png')

        # ---------------- the file: WhatsApp text, the file page
        print('the file', flush=True)
        href = await buyer.get_attribute('.nltg-file a.nltg-filelink', 'href')
        text = urllib.parse.unquote(urllib.parse.urlsplit(href).query.split('text=', 1)[1])
        H.check(href.startswith('https://wa.me/972525101555?'), 'the file goes to the site\'s WhatsApp number (from the settings)', href[:40])
        H.check('קומה 25' in text and 'לכיוון הים' in text and '1. ' in text and 'file=1' in text, 'the file\'s text: project, floor, side, numbered notes, the link', text)
        fpage = await bctx.new_page()
        self.watch(fpage, 'file')
        await fpage.goto(PAGE + '?room=' + room + '&file=1', wait_until='domcontentloaded', timeout=120000)
        await fpage.wait_for_selector('.nltg-filepage .nltg-note', timeout=30000)
        n = await fpage.eval_on_selector_all('.nltg-filepage .nltg-note', 'els => els.length')
        H.check(n >= 4, 'the file page lists the notes', n)
        await self.shot(fpage, '13-file-1440.png')

        # ---------------- leaving
        await buyer.click('.nltg-top .nltg-leave-top')
        await buyer.wait_for_selector('.nltg-out', timeout=5000)
        H.check('room=' not in buyer.url and await buyer.evaluate("() => !!document.querySelector('#nlps') && !document.documentElement.classList.contains('nltg-on')"), 'leaving puts the stage back in the page and drops ?room=')

        # ---------------- the chooser on the hero button (a visitor, a representative available)
        print('the chooser', flush=True)
        vctx = await self.context(browser, 'visitor', '10.4.0.1')
        vis = await vctx.new_page()
        self.watch(vis, 'visitor')
        # the chooser asks /room/available once the page is idle (the page itself is the same with or without it)
        async with vis.expect_response(lambda r: 'room/available' in r.url, timeout=30000) as avail:
            await vis.goto(PAGE, wait_until='domcontentloaded', timeout=120000)
        H.check((await (await avail.value).json()).get('now') is True, 'the page asks /room/available at idle time: a representative is available')
        await vis.wait_for_selector('a[data-nlps-ev="hero-video"]', timeout=30000)
        await vis.wait_for_timeout(300)
        await vis.click('a[data-nlps-ev="hero-video"]')
        await vis.wait_for_selector('.nltg-ch:not([hidden])', timeout=5000)
        await vis.wait_for_timeout(400)
        await self.shot(vis, '14-chooser-1440.png')
        await vis.click('.nltg-ch button.t')
        await vis.wait_for_selector('#nltg-name', timeout=60000)
        vroom = urllib.parse.parse_qs(urllib.parse.urlsplit(vis.url).query).get('room', [''])[0]
        H.check(len(vroom) == 12, '"עכשיו, בחדר משותף" opens a room and the join screen as a buyer', vroom)
        await vis.wait_for_timeout(1500)
        await self.shot(vis, '15-now-join-1440.png')
        # five languages, the direction by the language: English reads left to right
        await vis.click('.nltg-langs button[lang="en"]')
        await vis.wait_for_timeout(300)
        en = await vis.evaluate("() => ({dir: document.getElementById('nltg').dir, go: document.querySelector('.nltg-card .go').textContent, consent: document.querySelector('.nltg-card .consent').textContent})")
        H.check(en['dir'] == 'ltr' and en['go'] == 'Enter the room' and 'not on behalf of the developer' in en['consent'], 'English: left to right, the words translated', en)
        await self.shot(vis, '15b-join-en-1440.png')
        await vis.click('.nltg-langs button[lang="ar"]')
        await vis.wait_for_timeout(200)
        H.check(await vis.evaluate("() => document.getElementById('nltg').dir") == 'rtl', 'Arabic: right to left')

        # ---------------- LiveKit: the pinned library loads; a room with a key but no reachable server falls back
        print('LiveKit', flush=True)
        for c in (rctx, bctx, mctx):
            await c.close()
        lk = await vis.evaluate("async () => { const cfg = JSON.parse(document.getElementById('nltg-root').dataset.cfg); const m = await import(cfg.lkLib); return {url: cfg.lkLib, room: typeof m.Room, ev: typeof m.RoomEvent, v: m.version || null}; }")
        H.check(lk['room'] == 'function' and lk['ev'] == 'object', 'livekit-client loads as an ES module from the pinned URL', lk)
        await vis.goto(PAGE, wait_until='domcontentloaded', timeout=120000)  # the visitor's room page is left before the reset
        php_get('/__reset?rep_now=1&lk=1')
        lctx = await self.context(browser, 'lk', '10.5.0.1')
        lp = await lctx.new_page()
        self.watch(lp, 'lk')
        await lp.goto(PAGE + '?room=new', wait_until='domcontentloaded', timeout=120000)
        await lp.wait_for_selector('.nltg-checks', timeout=60000)
        H.check(True, 'with LiveKit set, the join screen asks about the camera and the microphone (only after the click they are used)')
        await self.join(lp, 'בודק', 'friend')
        await lp.wait_for_function("() => window.__nlTogether && document.querySelector('.nltg-toast') && !document.querySelector('.nltg-toast').hidden", timeout=40000)
        toast = await lp.text_content('.nltg-toast')
        H.check('ממשיכים בלי וידאו' in toast, 'an unreachable LiveKit server falls back to the site sync, and says so', toast)
        admin = await lctx.new_page()
        await admin.goto(PHP_BASE + '/__admin')
        html = await admin.content()
        H.check('נשמר' in html and 'harness-secret' not in html, 'the settings page: the secret is write-only ("נשמר", never printed)')
        await admin.set_viewport_size({'width': 1100, 'height': 900})
        await self.shot(admin, '16-settings.png', full=True)

        # ---------------- the offline harness page (scripts/together/harness.html): the same room over a static picture
        print('the offline harness page', flush=True)
        await lctx.close()
        await vctx.close()
        php_get('/__reset?rep_now=1')
        o1 = await browser.new_context(viewport={'width': 1440, 'height': 900})
        o2 = await browser.new_context(viewport={'width': 1440, 'height': 900})
        orep, obuy = await o1.new_page(), await o2.new_page()
        self.watch(orep, 'offline-rep')
        self.watch(obuy, 'offline-buyer')
        await orep.goto(PHP_BASE + '/harness.html?room=new&rep=1')
        await orep.wait_for_selector('#nltg-name')
        oroom = urllib.parse.parse_qs(urllib.parse.urlsplit(orep.url).query).get('room', [''])[0]
        await orep.click('.nltg-card .go')
        await orep.wait_for_selector('.nltg-dock')
        await orep.click('.nltg-pop .nltg-btn.ghost')
        await obuy.goto(PHP_BASE + '/harness.html?room=' + oroom)
        await self.join(obuy, 'יואב')
        await orep.click('.nltg-ctl .nltg-btn.teal')
        await orep.wait_for_timeout(1500)
        await orep.mouse.move(900, 450)
        await orep.mouse.down()
        await orep.mouse.move(760, 400, steps=8)
        await orep.mouse.up()
        await obuy.wait_for_timeout(3500)
        a = await orep.evaluate('() => window.__nlpsStage.getView().target')
        b = await obuy.evaluate('() => window.__nlpsStage.getView().target')
        H.check(a == b and a != [0, 0, 0], 'harness.html: the buyer\'s picture follows the representative\'s drag', {'rep': a, 'buyer': b})
        await self.shot(obuy, '17-offline-harness-1440.png')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(pathlib.Path(tempfile.gettempdir()) / 'together-harness'))
    ap.add_argument('--php', default=r'C:/Users/777/tools/php-8.3/php')
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    h = Harness(out)
    h.php = a.php
    sys.exit(asyncio.run(h.run()))


if __name__ == '__main__':
    main()
