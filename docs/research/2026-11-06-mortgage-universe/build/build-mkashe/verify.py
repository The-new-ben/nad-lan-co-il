"""HAD-675 (mortgage universe): press every control of the mkashe tool ("כשקשה לשלם") in preview.html, headless Chrome (Playwright).

At 390x844 (is_mobile) and 1280x900: the opening numbers (1,000,000 / 300 months / 4.62% / 3 months: 5,627 before; 5,723, 5,657 and
5,692 after), each of the six month buttons and the three cards checked against window.NLKS on the same values, the payment mode and
back, a bad value, the jump buttons, the date of the first missed payment, all six situations of the rights checklist, the two ended
outlines, the copy button (clipboard read back) and the case link (opened in a new page, the same numbers come back), the sources
list. On every view: no console error or warning, no horizontal scroll, every visible control at least 44 px high, every input
labelled, every group named, no long dash and none of the banned words in the rendered text. One more phone pass with the live
theme stylesheets (?theme=1, read only). The script starts its own http.server on a free 127.0.0.1 port (the repo root) and stops it
in finally. Screenshots go to build-mkashe/shots, the report to verify.json; exit 1 on any failed check. Nothing is sent anywhere.
Run:  python docs/research/2026-11-06-mortgage-universe/build/build-mkashe/verify.py
"""
import json, sys, pathlib, re, socket, subprocess, time, urllib.request
from playwright.sync_api import sync_playwright

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
with socket.socket() as s:
    s.bind(('127.0.0.1', 0)); PORT = s.getsockname()[1]
BASE = f'http://127.0.0.1:{PORT}/docs/research/2026-11-06-mortgage-universe/build/build-mkashe/preview.html'
OUT = HERE / 'shots'
OUT.mkdir(parents=True, exist_ok=True)
report, fails = [], []

def check(name, cond, got=None):
    report.append({'check': name, 'ok': bool(cond), 'got': got})
    print(('  ok   ' if cond else '  FAIL ') + name + ('' if got is None else '  [' + str(got)[:170] + ']'))
    if not cond: fails.append(name)

JS_HSCROLL = '() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth})'
JS_SMALL = '''() => { const out = [];
  document.querySelectorAll('#nlks button, #nlks input, #nlks a.nlks__tel, #nlks summary').forEach(e => { const b = e.getBoundingClientRect();
    if (b.width > 0 && b.height > 0 && b.height < 43.5) out.push(e.tagName + '#' + (e.id || e.getAttribute('data-s') || e.getAttribute('data-kind') || e.getAttribute('data-sel') || e.textContent.trim().slice(0, 12)) + ' ' + b.height.toFixed(1)); });
  return out; }'''
JS_LABELS = '''() => [...document.querySelectorAll('#nlks input')].filter(e => e.offsetParent !== null).map(e => ({id: e.id,
  label: (e.labels && e.labels.length ? e.labels[0].textContent : (e.getAttribute('aria-label') || '')).trim()})).filter(x => !x.label).map(x => x.id)'''
JS_GROUPS = '''() => [...document.querySelectorAll('#nlks [role="group"]')].filter(g => g.offsetParent !== null).map(g => {
  const id = g.getAttribute('aria-labelledby'); const l = id && document.getElementById(id); return l ? l.textContent.trim() : (g.getAttribute('aria-label') || ''); })'''
JS_EXPECT = '''(over) => { const v = Object.assign({b: 1000000, n: 300, m: 'rate', r: 4.62, p: '', d: 3}, over);
  const K = window.__K; const r = window.NLKS.compute(v, K); if (r.error) return {err: r.error.msg};
  const f = x => new Intl.NumberFormat('he-IL', {maximumFractionDigits: 0}).format(Math.round(x)) + ' ₪';
  return {p0: f(r.P0), full: f(r.by.full.after), io: f(r.by.io.after), ext: f(r.by.ext.after), xf: f(r.by.full.extra), xi: f(r.by.io.extra), xe: f(r.by.ext.extra), cheap: r.cheapest, r: r.r}; }'''
BANNED = re.compile('(\u05de\u05de\u05e9\u05e7|\u05d4\u05d3\u05d2\u05de\u05d4|\u05e1\u05d9\u05de\u05d5\u05dc\u05e6\u05d9\u05d4|\u05de\u05e0\u05d2\u05e0\u05d5\u05df|\u05d0\u05d9\u05e0\u05d8\u05e8\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9|\u05d4\u05de\u05e2\u05e8\u05db\u05ea|\u05d4\u05e4\u05dc\u05d8\u05e4\u05d5\u05e8\u05de\u05d4|\u05d8\u05db\u05e0\u05d5\u05dc\u05d5\u05d2\u05d9\u05d4|(^|[^\u0590-\u05ff])\u05d3\u05de\u05d5([^\u0590-\u05ff]|$))')

def txt(page, sel): return page.locator(sel).inner_text().strip()
def card(page, k): return page.locator(f'#nlks button[data-kind="{k}"] .nlks__cf').inner_text().strip()
def typ(page, sel, text):
    loc = page.locator(sel); loc.click(); loc.press('Control+A'); loc.press('Backspace')
    if text: page.keyboard.type(text)
    page.wait_for_timeout(260)
def press(page, sel): page.locator(sel).click(); page.wait_for_timeout(180)

def common(page, tag):
    hs = page.evaluate(JS_HSCROLL)
    check(tag + ' no horizontal scroll', hs['sw'] <= hs['iw'] + 1, hs)
    small = page.evaluate(JS_SMALL)
    check(tag + ' every visible control at least 44 px high', not small, small[:6])
    lab = page.evaluate(JS_LABELS)
    check(tag + ' every visible input labelled', not lab, lab)
    groups = page.evaluate(JS_GROUPS)
    check(tag + ' every visible group named', all(groups), groups[:6])
    body = page.locator('#nlks').inner_text()
    check(tag + ' no long dash, no banned word in the rendered text', not re.search('[\u2013\u2014]', body) and not BANNED.search(body), (re.findall('[\u2013\u2014]', body) + [m.group(0) for m in BANNED.finditer(body)])[:4])

server = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(REPO)],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(80):
        try:
            urllib.request.urlopen(BASE, timeout=1); break
        except Exception:
            time.sleep(0.25)
    with sync_playwright() as p:
        br = p.chromium.launch(channel='chrome', headless=True)
        for W, H, mob in ((390, 844, True), (1280, 900, False)):
            tag = str(W)
            print(f'\n{W}x{H}')
            ctx = br.new_context(viewport={'width': W, 'height': H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, locale='he-IL')
            ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin=f'http://127.0.0.1:{PORT}')
            page = ctx.new_page(); errs = []
            page.on('console', lambda m, errs=errs: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
            page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
            page.goto(BASE, wait_until='networkidle')
            page.wait_for_selector('#nlks .nlks__nf bdi')
            page.evaluate("async () => { window.__K = await fetch('/plugins/nadlan-config/assets/instruments/data/kashe.json').then(r => r.json()); }")
            e = page.evaluate(JS_EXPECT, {})
            check(tag + ' opens on 1,000,000 / 300 / 4.62% / 3 months', [page.input_value(s) for s in ('#nlks-b', '#nlks-n', '#nlks-r')] == ['1,000,000', '300', '4.62'] and page.get_attribute('#nlks button[data-s="d"][data-val="3"]', 'aria-pressed') == 'true')
            check(tag + ' the rate help names the BoI average of 8.2026', '8.2026: 4.62%' in txt(page, '#nlks-r-h'), txt(page, '#nlks-r-h'))
            check(tag + ' payment today 5,627 ₪', txt(page, '#nlks .nlks__nf') == '5,627 ₪' == e['p0'], txt(page, '#nlks .nlks__nf'))
            check(tag + ' three ways side by side: 5,723 / 5,657 / 5,692 ₪', [card(page, k) for k in ('full', 'io', 'ext')] == ['5,723 ₪', '5,657 ₪', '5,692 ₪'], [card(page, k) for k in ('full', 'io', 'ext')])
            cols = page.evaluate('() => getComputedStyle(document.querySelector("#nlks .nlks__cards")).gridTemplateColumns.split(" ").length')
            tops = page.evaluate('() => [...document.querySelectorAll("#nlks .nlks__cards button")].map(b => Math.round(b.getBoundingClientRect().top))')
            check(tag + ' the three cards in one row', cols == 3 and len(set(tops)) == 1, [cols, tops])
            check(tag + ' the cheapest is tagged on "ריבית בלבד" and said in one sentence', page.locator('#nlks button[data-kind="io"] .nlks__tag').count() == 1 and page.locator('#nlks .nlks__tag:not([aria-hidden])').count() == 1 and txt(page, '#nlks .nlks__cheap').startswith('הזולה ביותר בסך הכול: ריבית בלבד, 3,659 ₪'), txt(page, '#nlks .nlks__cheap'))
            check(tag + ' the CPI and the bank are said under the result', 'בלי שינוי במדד' in page.locator('#nlks-calc').inner_text() and 'את תנאי הדחייה בפועל קובע הבנק' in page.locator('#nlks-calc').inner_text())
            gcols = page.evaluate('() => getComputedStyle(document.querySelector("#nlks .nlks__grid")).gridTemplateColumns.split(" ").length')
            check(tag + ' layout: ' + ('one column on the phone' if mob else 'form and result side by side'), gcols == (1 if mob else 2), gcols)
            ff = page.evaluate('() => [".nlks__lede", ".nlks__cn", "#nlks-calc-h"].map(s => getComputedStyle(document.querySelector(s.startsWith("#") ? s : "#nlks " + s)).fontFamily.split(",")[0])')
            check(tag + ' running text in IBM Plex Sans Hebrew', all('Plex Sans Hebrew' in f for f in ff), ff)
            fm = page.evaluate('() => [".nlks__nf", ".nlks__cf", "#nlks-b"].map(s => getComputedStyle(document.querySelector(s.startsWith("#") ? s : "#nlks " + s)).fontFamily.split(",")[0])')
            check(tag + ' numbers in IBM Plex Mono', all('Plex Mono' in f for f in fm), fm)
            common(page, tag + ' open')
            page.screenshot(path=str(OUT / f'page-default-{tag}.png'), full_page=True)
            page.locator('#nlks-calc').screenshot(path=str(OUT / f'calc-{tag}.png'))

            # the three cards
            for k, xf in (('full', e['xf']), ('io', e['xi']), ('ext', e['xe'])):
                press(page, f'#nlks button[data-kind="{k}"]')
                last = page.locator('#nlks dl.nlks__dl > div').last.inner_text()
                check(f'{tag} card {k}: pressed, the breakdown ends on its extra {xf}', page.get_attribute(f'#nlks button[data-kind="{k}"]', 'aria-pressed') == 'true' and xf in last, last.replace('\n', ' '))
            check(tag + ' extension card: "מתארך ב־3 חודשים" in the breakdown', 'מתארך ב־3 חודשים' in txt(page, '#nlks dl.nlks__dl'))
            # the six month buttons
            for d in range(1, 7):
                press(page, f'#nlks button[data-s="d"][data-val="{d}"]')
                e2 = page.evaluate(JS_EXPECT, {'d': d})
                got = [card(page, k) for k in ('full', 'io', 'ext')]
                check(f'{tag} {d} months: pressed, cards = NLKS ({" / ".join(got)})', page.get_attribute(f'#nlks button[data-s="d"][data-val="{d}"]', 'aria-pressed') == 'true' and got == [e2['full'], e2['io'], e2['ext']] and (f'אם דוחים {d} ' in txt(page, '#nlks .nlks__ol')), txt(page, '#nlks .nlks__ol'))
            check(tag + ' 6 months: 5,821 / 5,688 / 5,758 ₪', [card(page, k) for k in ('full', 'io', 'ext')] == ['5,821 ₪', '5,688 ₪', '5,758 ₪'])
            page.locator('#nlks-calc').screenshot(path=str(OUT / f'calc-6months-ext-{tag}.png'))
            press(page, '#nlks button[data-s="d"][data-val="3"]'); press(page, '#nlks button[data-kind="full"]')
            # the payment mode and back
            press(page, '#nlks button[data-s="m"][data-val="pay"]')
            check(tag + ' payment mode: the rate field hides, the payment opens on 5,627 and the rate it implies is said', not page.locator('#nlks-r').is_visible() and page.input_value('#nlks-p') == '5,627' and '4.62%' in txt(page, '[data-help="p"]'), [page.input_value('#nlks-p'), txt(page, '[data-help="p"]')])
            typ(page, '#nlks-p', '6000')
            e3 = page.evaluate(JS_EXPECT, {'m': 'pay', 'p': 6000})
            check(tag + ' payment 6,000: the rate is solved and the cards follow (' + e3['full'] + ')', card(page, 'full') == e3['full'] and txt(page, '#nlks .nlks__nf') == '6,000 ₪', [txt(page, '[data-help="p"]'), card(page, 'full')])
            typ(page, '#nlks-p', '3000')
            check(tag + ' payment 3,000 (below balance / months): the message sits on the payment field', 'בלי ריבית בכלל' in txt(page, '[data-err="p"]') and page.locator('#nlks .nlks__msg').is_visible(), txt(page, '[data-err="p"]'))
            page.locator('#nlks-calc').screenshot(path=str(OUT / f'calc-error-{tag}.png'))
            typ(page, '#nlks-p', '6000')
            press(page, '#nlks button[data-s="m"][data-val="rate"]')
            check(tag + ' back to the rate: the field holds the rate of the 6,000 payment', abs(float(page.input_value('#nlks-r')) - round(e3['r'], 2)) < 0.006, page.input_value('#nlks-r'))
            typ(page, '#nlks-r', '4.62')
            typ(page, '#nlks-b', '5000')
            check(tag + ' balance 5,000: an error on the balance field', 'הקלידו יתרה' in txt(page, '[data-err="b"]'), txt(page, '[data-err="b"]'))
            typ(page, '#nlks-b', '1000000')
            check(tag + ' balance back to 1,000,000: 5,627 ₪ again', txt(page, '#nlks .nlks__nf') == '5,627 ₪')

            # the jump buttons
            for go in ('nlks-late', 'nlks-rights', 'nlks-war', 'nlks-calc'):
                press(page, f'#nlks button[data-go="{go}"]')
                try: page.wait_for_function(f'() => {{ const t = document.getElementById("{go}").getBoundingClientRect().top; return t > -5 && t < 140; }}', timeout=4000)
                except Exception: pass
                top = page.evaluate(f'() => document.getElementById("{go}").getBoundingClientRect().top')
                end = page.evaluate('() => window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2')
                check(f'{tag} jump to {go}: the section comes to the top (or the page reached its end)', -5 <= top <= 140 or (end and top < 300), [round(top), 'end' if end else ''])

            # the timeline
            steps = page.evaluate('() => [...document.querySelectorAll("#nlks ol.nlks__tl > li")].map(li => li.getAttribute("data-step"))')
            check(tag + ' timeline: six steps in order', steps == ['day0', 'notice', 'six', 'office', 'receiver', 'sale'], steps)
            tl = txt(page, '#nlks ol.nlks__tl')
            check(tag + ' timeline: 21 ימי עסקים, 6 חודשים, 20 / 90 ימים, 18 חודשים, 2.5 מיליון ₪', all(x in tl for x in ('21 ימי עסקים', '6 חודשים', 'בתוך 20 ימים', 'ל־90 ימים', '18 חודשים', '2.5 מיליון ₪')), None)
            check(tag + ' timeline: every step has its protection block and its sources', page.locator('#nlks ol.nlks__tl > li .nlks__blk:not(.is-do)').count() == 6 and page.locator('#nlks ol.nlks__tl > li .nlks__s a').count() >= 15)
            page.locator('#nlks-miss').fill('2026-05-10'); page.wait_for_timeout(250)
            check(tag + ' first missed payment 10.5.2026: the 6-month line shows 10.11.2026', 'מ־10.11.2026' in txt(page, '#nlks li[data-step="six"] .nlks__date') and txt(page, '#nlks li[data-step="day0"] .nlks__date') == '10.5.2026')
            page.locator('#nlks-late').screenshot(path=str(OUT / f'late-{tag}.png'))
            tels = page.evaluate('() => [...document.querySelectorAll("#nlks a.nlks__tel")].map(a => a.getAttribute("href"))')
            check(tag + ' bank and help lines are tap-to-call links (*8860 first)', len(tels) >= 13 and tels[0] == 'tel:*8860' and 'tel:118' in tels and 'tel:*2310' in tels, tels[:4])
            check(tag + ' Mizrahi-Tefahot arrears line: שלוחה 4 ואז 3', 'שלוחה 4 ואז 3' in page.locator('#nlks ul.nlks__tels').first.inner_text())

            # the rights checklist
            exp = {'reserve': ['reserve'], 'jobill': ['hardship'], 'birth': ['hardship'], 'death': ['death', 'insurance'], 'zakaut': ['committee'], 'elder': ['elder']}
            for s, ks in exp.items():
                press(page, f'#nlks button[data-sel="{s}"]')
                got = page.evaluate('() => [...document.querySelectorAll("#nlks ul.nlks__rl > li")].map(li => li.getAttribute("data-right"))')
                check(f'{tag} situation {s}: pressed, rights {ks}', page.get_attribute(f'#nlks button[data-sel="{s}"]', 'aria-pressed') == 'true' and got == ks and page.locator('#nlks ul.nlks__rl li .nlks__s a').count() >= 1, got)
                press(page, f'#nlks button[data-sel="{s}"]')
            for s in exp: press(page, f'#nlks button[data-sel="{s}"]')
            got = page.evaluate('() => [...document.querySelectorAll("#nlks ul.nlks__rl > li")].map(li => li.getAttribute("data-right"))')
            check(tag + ' all six ticked: six rights, none twice', len(got) == 6 and len(set(got)) == 6, got)
            page.locator('#nlks-rights').screenshot(path=str(OUT / f'rights-all-{tag}.png'))
            for s in exp: press(page, f'#nlks button[data-sel="{s}"]')
            check(tag + ' nothing ticked: the hint is back, no right listed', page.locator('#nlks [data-none]').is_visible() and page.locator('#nlks ul.nlks__rl > li').count() == 0)
            check(tag + ' the six rights of every borrower are always listed', page.locator('#nlks ul.nlks__al > li').count() == 6)

            # the ended outlines
            st = page.evaluate('() => [...document.querySelectorAll("#nlks .nlks__wc")].map(c => [c.getAttribute("data-prog"), c.querySelector(".nlks__st").textContent])')
            war = txt(page, '#nlks-war')
            check(tag + ' outlines: שאגת הארי and עם כלביא, both "הסתיים", none open', st == [['shaagat', 'הסתיים'], ['kalavi', 'הסתיים']] and 'פתוח' not in war and 'בכל מבצע חדש בנק ישראל מפרסם מתווה; בודקים מול הבנק.' in war, st)
            page.locator('#nlks-war').screenshot(path=str(OUT / f'war-{tag}.png'))

            # copy and link
            press(page, '#nlks button[data-act="copy"]'); page.wait_for_timeout(300)
            clip = page.evaluate('() => navigator.clipboard.readText()')
            check(tag + ' copy: the summary with 5,627 / 5,723 / 3,659 ₪, not legal advice, the #mkashe= link', all(x in clip for x in ('5,627 ₪', '5,723 ₪', '3,659 ₪', 'אינו ייעוץ משפטי', '#mkashe=')) and txt(page, '#nlks button[data-act="copy"]') in ('הועתק', 'העתקת הסיכום'), clip[:120].replace('\n', ' '))
            check(tag + ' copy: no ticked situation and no date in the text', all(x not in clip for x in ('פטירה של לווה', 'לידה', 'מילואים', '10.5.2026')))
            press(page, '#nlks button[data-s="d"][data-val="5"]'); press(page, '#nlks button[data-kind="ext"]')
            press(page, '#nlks button[data-act="link"]'); page.wait_for_timeout(300)
            link = page.evaluate('() => navigator.clipboard.readText()')
            check(tag + ' link: the address holds #mkashe= and the page address itself was not changed', '#mkashe=' in link and '#' not in page.url, link[-60:])
            p2 = ctx.new_page(); p2.goto(link, wait_until='networkidle'); p2.wait_for_selector('#nlks .nlks__nf bdi')
            check(tag + ' the link opens the same case: 5 months, extension pressed', p2.get_attribute('#nlks button[data-s="d"][data-val="5"]', 'aria-pressed') == 'true' and p2.get_attribute('#nlks button[data-kind="ext"]', 'aria-pressed') == 'true' and p2.input_value('#nlks-miss') == '', p2.locator('#nlks .nlks__ol').inner_text())
            p2.close()
            press(page, '#nlks details.nlks__src > summary')
            check(tag + ' the sources list opens: 27 sources, each linked with a date', page.locator('#nlks details.nlks__src[open] li a').count() == 27 and page.locator('#nlks details.nlks__src li small').count() == 27)
            common(page, tag + ' after')
            page.screenshot(path=str(OUT / f'page-after-{tag}.png'), full_page=True)
            check(tag + ' no console error or warning, no page error', not errs, errs[:5])
            ctx.close()

        # one phone pass under the live theme stylesheets (read only)
        print('\n390 + live theme')
        ctx = br.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=2, locale='he-IL')
        page = ctx.new_page(); errs = []
        page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
        page.on('console', lambda m, errs=errs: errs.append(m.text + ' @ ' + str((m.location or {}).get('url', ''))) if m.type == 'error' and 'nad-lan.co.il' not in m.text + str((m.location or {}).get('url', '')) else None)
        page.goto(BASE + '?theme=1', wait_until='networkidle')
        page.wait_for_selector('#nlks .nlks__nf bdi')
        check('theme 390 opens on 5,627 ₪', txt(page, '#nlks .nlks__nf') == '5,627 ₪')
        common(page, 'theme 390')
        ff = page.evaluate('() => [getComputedStyle(document.querySelector("#nlks h2.nlks__h")).fontFamily.split(",")[0], getComputedStyle(document.querySelector("#nlks button[data-kind]")).borderRadius, getComputedStyle(document.querySelector("#nlks h3.nlks__sh")).color]')
        check('theme 390: heading face, card radius and section heading colour hold against the theme', 'Plex Sans Hebrew' in ff[0] and ff[1] == '2px' and ff[2] == 'rgb(31, 75, 92)', ff)
        page.screenshot(path=str(OUT / 'page-theme-390.png'), full_page=True)
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
