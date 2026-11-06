"""HAD-675: press the new tool mneches ("כמה אפשר לקבל על דירה קיימת") of preview.html in headless Chrome (Playwright, channel chrome).

At 390x844 (is_mobile) and 1280x900: the switcher chip opens the pane; the opening example (2,800,000 / 350,000, any purpose) shows
1,050,000; every purpose, every term, every rate source, the own-rate field, the balance (0, above the cap), an income-bound case,
the 120,000 exemption and a bad value are pressed or typed, and each headline is checked against window.NLNC on the same values;
the copy button, the WhatsApp link (navigation blocked) and the case link are pressed, and the case link is opened in a fresh page
(the pane opens by itself, the values come back). On every view: no console error or warning, no horizontal scroll, every visible
control at least 44 px high, every input labelled, every group named. One more phone pass with the live theme stylesheets (?theme=1,
read only). The script starts its own http.server on a free 127.0.0.1 port (the repo root) and stops it in finally. Screenshots go
to build-mneches/shots, the report to verify.json; exit 1 on any failed check. Nothing is sent anywhere: the page reads local files.
Run:  python docs/research/2026-11-06-mortgage-universe/build/build-mneches/verify.py
"""
import json, sys, pathlib, re, socket, subprocess, time, urllib.request
from playwright.sync_api import sync_playwright

try: sys.stdout.reconfigure(encoding='utf-8')  # Hebrew in the log on a Windows console
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
with socket.socket() as s:
    s.bind(('127.0.0.1', 0)); PORT = s.getsockname()[1]
ORIGIN = f'http://127.0.0.1:{PORT}'
BASE = f'{ORIGIN}/docs/research/2026-11-06-mortgage-universe/build/build-mneches/preview.html'
OUT = HERE / 'shots'
OUT.mkdir(parents=True, exist_ok=True)
report, fails = [], []
GUIDE = 'https://nad-lan.co.il/mortgage-calculator/mortgage-for-any-purpose/'

def check(name, cond, got=None):
    report.append({'check': name, 'ok': bool(cond), 'got': got})
    print(('  ok   ' if cond else '  FAIL ') + name + ('' if got is None else '  [' + str(got)[:170] + ']'))
    if not cond: fails.append(name)

JS_HSCROLL = '() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth})'
JS_SMALL = '''() => { const out = [];
  document.querySelectorAll('#nlnc button, #nlnc input, #nlnc select, #nlnc .nli__share a, #tools .nlmx-sw__chips button').forEach(e => { const b = e.getBoundingClientRect();
    if (b.width > 0 && b.height > 0 && b.height < 43.5) out.push(e.tagName + '#' + (e.id || e.getAttribute('data-val') || e.getAttribute('data-s') || '') + ' ' + b.height.toFixed(1)); });
  return out; }'''
JS_LABELS = '''() => [...document.querySelectorAll('#nlnc input, #nlnc select')].filter(e => e.offsetParent !== null).map(e => ({id: e.id,
  label: (e.labels && e.labels.length ? e.labels[0].textContent : (e.getAttribute('aria-label') || '')).trim()})).filter(x => !x.label).map(x => x.id)'''
JS_GROUPS = '''() => [...document.querySelectorAll('#nlnc [role="group"]')].filter(g => g.offsetParent !== null).map(g => {
  const id = g.getAttribute('aria-labelledby'); const l = id && document.getElementById(id); return l ? l.textContent.trim() : (g.getAttribute('aria-label') || ''); })'''
JS_SIGN = '''() => { const out = [];  // where the shekel sign sits beside each amount of the figure, the ledger values and the table
  document.querySelectorAll('#nlnc .nlnc__fig, #nlnc .nlnc__lv, #nlnc table.nlnc__t td.n').forEach(el => { const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n;
    while ((n = tw.nextNode())) { const re = /([\d,.]+) ₪/g; let m;
      while ((m = re.exec(n.data))) { const r1 = document.createRange(); r1.setStart(n, m.index); r1.setEnd(n, m.index + m[1].length);
        const r2 = document.createRange(); r2.setStart(n, m.index + m[1].length + 1); r2.setEnd(n, m.index + m[1].length + 2);
        const a = r1.getBoundingClientRect(), b = r2.getBoundingClientRect(); if (a.width && b.width) out.push(b.left > a.left ? 'R' : 'L'); } } });
  return out; }'''
JS_EXPECT = '''async (cur) => { const D = await fetch('/plugins/nadlan-config/assets/instruments/data/boi-mortgage.json').then(r => r.json());
  const N = await fetch('/plugins/nadlan-config/assets/instruments/data/mneches.json').then(r => r.json());
  const v = Object.assign(window.NLNC.defaults(), cur); const r = window.NLNC.compute(v, D, N);
  return r.error ? {err: r.error.msg, field: r.error.field} : {head: window.NLNC.headline(r).value, best: r.best, binds: r.binds, key: r.key, ltv: r.ltvRoom, inc: r.incMax}; }'''

def fig(page):
    return page.locator('#nlnc .nlnc__fig').inner_text().strip()

def typ(page, sel, text):
    loc = page.locator(sel); loc.click(); loc.press('Control+A'); loc.press('Backspace')
    if text: page.keyboard.type(text)
    page.wait_for_timeout(260)

def press(page, sel):
    page.locator(sel).click(); page.wait_for_timeout(200)

def pressed(page, sel):
    return page.get_attribute(sel, 'aria-pressed') == 'true'

def common(page, tag):
    hs = page.evaluate(JS_HSCROLL)
    check(tag + ' no horizontal scroll', hs['sw'] <= hs['iw'] + 1, hs)
    small = page.evaluate(JS_SMALL)
    check(tag + ' every visible control at least 44 px high', not small, small[:6])
    lab = page.evaluate(JS_LABELS)
    check(tag + ' every visible input labelled', not lab, lab)
    groups = page.evaluate(JS_GROUPS)
    check(tag + ' every visible group named', all(groups) and len(groups) >= 3, groups[:5])

def expect(page, cur):
    return page.evaluate(JS_EXPECT, cur)

def same(page, tag, cur):
    e = expect(page, cur); f = fig(page)
    check(tag + ': headline = NLNC (' + str(e.get('head')) + ')', f == e.get('head'), f)
    return e

server = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(REPO)],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(60):
        try:
            urllib.request.urlopen(BASE, timeout=1); break
        except Exception:
            time.sleep(0.25)
    with sync_playwright() as p:
        br = p.chromium.launch(channel='chrome', headless=True)
        for W, H, mob in ((390, 844, True), (1280, 900, False)):
            tag = str(W)
            print(f'\n{W}x{H}  ({BASE})')
            ctx = br.new_context(viewport={'width': W, 'height': H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, locale='he-IL')
            ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin=ORIGIN)
            page = ctx.new_page(); errs = []
            page.on('console', lambda m, errs=errs: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
            page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
            page.on('dialog', lambda d: d.dismiss())
            page.goto(BASE, wait_until='networkidle')
            page.wait_for_selector('#nlnc .nlnc__fig bdi', state='attached')
            check(tag + ' the pane starts hidden behind the first chip (as on the page)', not page.locator('#tool-neches').is_visible())
            press(page, '#tools button[data-sw="tool-neches"]')
            check(tag + ' the chip opens the pane', page.locator('#nlnc .nlnc__fig').is_visible() and pressed(page, '#tools button[data-sw="tool-neches"]'))
            cur = {}
            check(tag + ' opens on the example: 1,050,000 ₪', fig(page) == '1,050,000 ₪', fig(page))
            same(page, tag + ' opening', cur)
            vals = [page.input_value(s) for s in ('#nlnc-value', '#nlnc-balance', '#nlnc-epay', '#nlnc-income', '#nlnc-other')]
            check(tag + ' opening values 2,800,000 / 350,000 / 3,150 / 25,000 / 1,500', vals == ['2,800,000', '350,000', '3,150', '25,000', '1,500'], vals)
            check(tag + ' opening presses: any purpose, 20 years, the any-purpose average', pressed(page, '#nlnc button[data-s="purpose"][data-val="any"]') and pressed(page, '#nlnc button[data-s="years"][data-val="20"]') and pressed(page, '#nlnc button[data-s="src"][data-val="anyp"]'))
            ls = page.locator('#nlnc ol.nlnc__ls').inner_text()
            check(tag + ' ledger: 1,400,000, −350,000, 1,050,000 (קובע), 1,250,000, 8,600, 1,173,288', all(x in ls for x in ('1,400,000 ₪', '−350,000 ₪', '1,050,000 ₪', 'קובע', '1,250,000 ₪', '8,600 ₪', '1,173,288 ₪')), ls[:220])
            check(tag + ' the example tag is shown until the first edit', page.locator('#nlnc [data-eg]').is_visible())
            check(tag + ' title "כמה אפשר לקבל על דירה קיימת"', page.locator('#nlnc h2.nli__title').inner_text().strip() == 'כמה אפשר לקבל על דירה קיימת')
            gl = page.locator(f'#nlnc a[href="{GUIDE}"]')
            check(tag + ' the guide link, exact anchor "משכנתא לכל מטרה"', gl.count() == 1 and gl.inner_text().strip() == 'משכנתא לכל מטרה', gl.count())
            srct = page.locator('#nlnc p.nlnc__src').inner_text()
            check(tag + ' source line: directive 329 version 13, 30.6.2026, Q&A 8.2.2026, checked 6.11.2026', all(x in srct for x in ('גרסה 13', '30.6.2026', '8.2.2026', 'נבדק ב־6.11.2026')), srct[:160])
            check(tag + ' non-bank line, no lender named, no number', 'חוץ בנקאיים' in page.locator('#nlnc p.nlnc__fine').inner_text() and not re.search(r'\d', page.locator('#nlnc p.nlnc__fine').inner_text()))
            check(tag + ' rules, the 1.10.2026 change and the Bank of Israel data are printed', all(x in page.locator('#nlnc .nlnc__more').inner_text() for x in ('סעיף 10א', '120,000', '18 חודשים', '1,386 הלוואות', '23.97%')))
            ff = page.evaluate('() => ["p.nli__lede", ".nlnc__lk", ".nlnc__sub"].map(s => getComputedStyle(document.querySelector("#nlnc " + s)).fontFamily.split(",")[0])')
            check(tag + ' running text in IBM Plex Sans Hebrew', all('Plex Sans Hebrew' in f for f in ff), ff)
            fm = page.evaluate('() => [".nlnc__fig", ".nlnc__lv", "#nlnc-value"].map(s => getComputedStyle(document.querySelector(s.startsWith("#") ? s : "#nlnc " + s)).fontFamily.split(",")[0])')
            check(tag + ' numbers in IBM Plex Mono', all('Plex Mono' in f for f in fm), fm)
            cols = page.evaluate('() => getComputedStyle(document.querySelector("#nlnc .nlnc__grid")).gridTemplateColumns.split(" ").length')
            check(tag + ' layout: ' + ('one column on the phone' if mob else 'form and result side by side'), cols == (1 if mob else 2), cols)
            sides = page.evaluate(JS_SIGN)
            check(tag + ' every amount of the figure, the ledger and the table shows the sign on the same side (as the live tools)', len(sides) > 20 and len(set(sides)) == 1, ''.join(sides)[:60])
            common(page, tag + ' opening')
            page.screenshot(path=str(OUT / f'page-default-{tag}.png'), full_page=True)
            page.locator('#nlnc').screenshot(path=str(OUT / f'mneches-default-{tag}.png'))

            # the four purposes
            for k in ('buy', 'kids', 'close', 'any'):
                press(page, f'#nlnc button[data-s="purpose"][data-val="{k}"]'); cur['purpose'] = k
                e = same(page, f'{tag} purpose {k}', cur)
                pn = page.locator('#nlnc [data-pn]').inner_text()
                rel = page.locator('#nlnc ol.nlnc__ls li', has_text='בשיקול דעת הבנק').count()
                if k == 'buy':
                    check(f'{tag} buy: the housing mix is used, the new home\'s caps (section 2) and a link to the full calculator', pressed(page, '#nlnc button[data-s="src"][data-val="home"]') and '(סעיף 2)' in pn and page.locator('#nlnc [data-pn] a[href="#mortgage-tool"]').count() == 1 and rel == 0, pn[:120])
                    page.locator('#nlnc').screenshot(path=str(OUT / f'mneches-buy-{tag}.png'))
                elif k == 'kids':
                    check(f'{tag} kids: Q&A 2.7 and Annex A 1.3, no 70% relief line', '(שו"ת 2.7)' in pn and '(נספח א, סעיף 1.3)' in pn and rel == 0, pn[:120])
                elif k == 'close':
                    check(f'{tag} close: Q&A 7.7 and the relief line', '(שו"ת 7.7)' in pn and rel == 1, pn[:120])
                else:
                    check(f'{tag} any: back to the any-purpose average and 1,050,000', pressed(page, '#nlnc button[data-s="src"][data-val="anyp"]') and fig(page) == '1,050,000 ₪', fig(page))
            # the five terms
            for y in (10, 15, 25, 30, 20):
                press(page, f'#nlnc button[data-s="years"][data-val="{y}"]'); cur['years'] = y
                same(page, f'{tag} term {y}', cur)
                on = page.locator('#nlnc table.nlnc__t tr.is-on td').first.inner_text()
                check(f'{tag} term {y}: its row is marked in the table', on.startswith(f'{y} שנה'), on[:30])
            check(tag + ' 10 years: the income binds (764,788 ₪ in the table)', '764,788 ₪' in page.locator('#nlnc table.nlnc__t').inner_text())
            # the rate sources
            press(page, '#nlnc button[data-s="src"][data-val="home"]'); cur['src'] = 'home'
            same(page, tag + ' source home', cur)
            check(tag + ' the housing average is labelled with the any-purpose price beside it', '6.61% מול 4.62%' in page.locator('#nlnc [data-help="src"]').inner_text())
            press(page, '#nlnc button[data-s="src"][data-val="own"]'); cur['src'] = 'own'; cur['rate'] = '6.61'
            check(tag + ' own rate: the field appears, opening at 6.61', page.locator('#nlnc-rate').is_visible() and page.input_value('#nlnc-rate') == '6.61', page.input_value('#nlnc-rate'))
            same(page, tag + ' own 6.61%', cur)
            typ(page, '#nlnc-rate', '5'); cur['rate'] = '5'
            same(page, tag + ' own 5%', cur)
            typ(page, '#nlnc-rate', '25')
            check(tag + ' own 25%: an error on its field, no stale result', page.locator('[data-err="rate"]').inner_text() != '' and not page.locator('#nlnc .nlnc__ok').is_visible(), page.locator('[data-err="rate"]').inner_text())
            typ(page, '#nlnc-rate', '5')
            # an income-bound case
            typ(page, '#nlnc-income', '18000'); typ(page, '#nlnc-other', '2000'); cur.update({'income': '18000', 'other': '2000'})
            e = same(page, tag + ' income 18,000, other 2,000, own 5%', cur)
            check(tag + ' income-bound: 734,897 ₪, the income line carries "קובע"', fig(page) == '734,897 ₪' and 'קובע' in page.locator('#nlnc ol.nlnc__ls li', has_text='לפי ההכנסה').inner_text(), fig(page))
            check(tag + ' the sub says the income binds and by how much (315,103)', 'ההכנסה קובעת' in page.locator('#nlnc .nlnc__sub').inner_text() and '315,103' in page.locator('#nlnc .nlnc__sub').inner_text())
            page.locator('#nlnc').screenshot(path=str(OUT / f'mneches-income-{tag}.png'))
            # zero balance: the existing-payment field hides
            typ(page, '#nlnc-balance', '0'); cur['balance'] = '0'
            check(tag + ' balance 0: the existing-payment field hides', not page.locator('#nlnc-epay').is_visible())
            same(page, tag + ' balance 0', cur)
            # a balance above the cap
            typ(page, '#nlnc-balance', '1600000'); cur['balance'] = '1600000'
            same(page, tag + ' balance 1,600,000 on 2,800,000', cur)
            out = page.locator('#nlnc .nlnc__out').inner_text()
            check(tag + ' above the cap: "אין מקום להלוואה נוספת", red underline, no negative amount', fig(page) == 'אין מקום להלוואה נוספת' and 'is-text' in (page.get_attribute('#nlnc .nlnc__fig', 'class') or '') and not re.search(r'(^|[^\d,.])-\d', out), fig(page))
            page.locator('#nlnc').screenshot(path=str(OUT / f'mneches-noroom-{tag}.png'))
            # the 120,000 exemption
            typ(page, '#nlnc-value', '2000000'); typ(page, '#nlnc-balance', '0'); typ(page, '#nlnc-income', '3000'); cur.update({'value': '2000000', 'balance': '0', 'income': '3000'})
            same(page, tag + ' exemption case', cur)
            check(tag + ' income room 500: the 120,000 exemption (sections 11, 12.2)', fig(page) == '120,000 ₪' and 'פטורה ממגבלת ההחזר' in page.locator('#nlnc .nlnc__sub').inner_text(), fig(page))
            # a bad value
            typ(page, '#nlnc-value', '')
            check(tag + ' empty value: the message on its field', page.locator('[data-err="value"]').inner_text() != '', page.locator('[data-err="value"]').inner_text())
            typ(page, '#nlnc-value', '2800000'); typ(page, '#nlnc-balance', '350000'); typ(page, '#nlnc-income', '25000'); typ(page, '#nlnc-other', '1500')
            cur.update({'value': '2800000', 'balance': '350000', 'income': '25000', 'other': '1500'})
            same(page, tag + ' back to the example with own 5%', cur)
            check(tag + ' the example tag is gone after editing', not page.locator('#nlnc [data-eg]').is_visible())
            common(page, tag + ' after typing')
            # the share bar
            press(page, '#nlnc button[data-copy]')
            clip = page.evaluate('() => navigator.clipboard.readText()')
            check(tag + ' copy: the summary and the #tool-neches link', clip.startswith('כמה אפשר לקבל על דירה קיימת:') and '#tool-neches' in clip and 'גרסה 13' in clip, clip[:120])
            page.evaluate('() => document.addEventListener("click", e => { if (e.target.closest && e.target.closest("a[data-wa]")) e.preventDefault(); })')
            press(page, '#nlnc a[data-wa]')
            wa = page.get_attribute('#nlnc a[data-wa]', 'href') or ''
            check(tag + ' WhatsApp: the link carries the summary (navigation blocked in the test)', wa.startswith('https://wa.me/?text=') and '%23tool-neches' in wa, wa[:80])
            press(page, '#nlnc button[data-link]')
            link = page.evaluate('() => navigator.clipboard.readText()')
            check(tag + ' case link: #mneches=', '#mneches=' in link, link[-60:])
            page.screenshot(path=str(OUT / f'page-after-{tag}.png'), full_page=True)
            check(tag + ' no console error or warning, no page error', not errs, errs[:5])
            # the case link in a fresh page: the pane opens by itself and the values come back
            p2 = ctx.new_page(); errs2 = []
            p2.on('pageerror', lambda e, errs2=errs2: errs2.append(str(e)))
            p2.on('console', lambda m, errs2=errs2: errs2.append(m.text) if m.type in ('error', 'warning') else None)
            p2.goto(link, wait_until='networkidle'); p2.wait_for_selector('#nlnc .nlnc__fig bdi'); p2.wait_for_timeout(300)
            e2 = expect(p2, cur)
            check(tag + ' the case link opens the pane, presses its chip and restores the case', p2.locator('#nlnc .nlnc__fig').is_visible() and pressed(p2, '#tools button[data-sw="tool-neches"]')
                  and fig(p2) == e2['head'] and p2.input_value('#nlnc-rate') == '5' and pressed(p2, '#nlnc button[data-s="src"][data-val="own"]'), [fig(p2), e2['head']])
            check(tag + ' the case link page: no console error', not errs2, errs2[:3])
            p2.close(); ctx.close()

        # one phone pass under the live theme stylesheets (read only)
        print('\n390 + live theme')
        ctx = br.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=2, locale='he-IL')
        page = ctx.new_page(); errs = []
        page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
        page.on('console', lambda m, errs=errs: errs.append(m.text + ' @ ' + str((m.location or {}).get('url', ''))) if m.type == 'error' and 'nad-lan.co.il' not in m.text + str((m.location or {}).get('url', '')) else None)  # the live theme's own assets are not ours to judge here
        page.goto(BASE + '?theme=1', wait_until='networkidle')
        page.wait_for_selector('#nlnc .nlnc__fig bdi', state='attached')
        press(page, '#tools button[data-sw="tool-neches"]')
        check('theme 390 opens on 1,050,000 ₪', fig(page) == '1,050,000 ₪', fig(page))
        common(page, 'theme 390')
        ff = page.evaluate('() => [getComputedStyle(document.querySelector("#nlnc .nlnc__lk")).fontFamily.split(",")[0], getComputedStyle(document.querySelector("#nlnc .nlnc__seg button")).borderRadius, getComputedStyle(document.querySelector("#nlnc h3.nlnc__mh")).fontFamily.split(",")[0]]')
        check('theme 390: text face, button radius and sub-heading face hold against the theme', 'Plex Sans Hebrew' in ff[0] and ff[1] == '2px' and 'Plex Sans Hebrew' in ff[2], ff)
        press(page, '#nlnc button[data-s="purpose"][data-val="buy"]')
        check('theme 390: a purpose pressed under the theme', pressed(page, '#nlnc button[data-s="purpose"][data-val="buy"]'))
        press(page, '#nlnc button[data-s="purpose"][data-val="any"]')
        page.locator('#nlnc').screenshot(path=str(OUT / 'mneches-theme-390.png'))
        check('theme 390: no page error and no local console error', not errs, errs[:5])
        ctx.close(); br.close()
finally:
    server.terminate()
    try: server.wait(timeout=5)
    except Exception: server.kill()
    print('\nlocal server stopped')

(HERE / 'verify.json').write_text(json.dumps({'base': BASE, 'checks': len(report), 'failed': fails, 'report': report}, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'\n{len(report) - len(fails)} of {len(report)} checks passed' + (f', {len(fails)} FAILED' if fails else ''))
sys.exit(1 if fails else 0)
