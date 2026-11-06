"""HAD-675 (mortgage delta A1, A2, A8): press the two new tools of preview.html in headless Chrome (Playwright, channel chrome).

mzakaut: every one of the eight profiles at 390x844 (is_mobile) and 1280x900, each headline checked against window.NLZK on the same
values, plus zone, reserve, 10 פלוס, the rate field and the marriage date; mnomeff: both directions and a chip. On every view: no
console error, no horizontal scroll, every visible control at least 44 px high, every input and select labelled, every group named.
One more phone pass with the live theme stylesheets (?theme=1, read only). The script starts its own local http.server on
127.0.0.1:47986 (the repo root) and stops it at the end, whatever happens. Screenshots go to build-mzakaut/shots, the report to
verify.json; exit 1 on any failed check. Nothing is sent anywhere: the page only reads the local data files.
Run:  python docs/research/2026-11-06-mortgage-delta/build-mzakaut/verify.py
"""
import json, sys, pathlib, re, subprocess, time, urllib.request
from playwright.sync_api import sync_playwright

try: sys.stdout.reconfigure(encoding='utf-8')  # Hebrew in the log on a Windows console
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
PORT = 47986
BASE = f'http://127.0.0.1:{PORT}/docs/research/2026-11-06-mortgage-delta/build-mzakaut/preview.html'
OUT = HERE / 'shots'
OUT.mkdir(parents=True, exist_ok=True)
report, fails = [], []

def check(name, cond, got=None):
    report.append({'check': name, 'ok': bool(cond), 'got': got})
    print(('  ok   ' if cond else '  FAIL ') + name + ('' if got is None else '  [' + str(got)[:160] + ']'))
    if not cond: fails.append(name)

JS_HSCROLL = '() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth})'
JS_SMALL = '''() => { const out = [];
  document.querySelectorAll('#nlzk button, #nlzk input, #nlzk select, #nlne button, #nlne input').forEach(e => { const b = e.getBoundingClientRect();
    if (b.width > 0 && b.height > 0 && b.height < 43.5) out.push(e.tagName + '#' + (e.id || e.getAttribute('data-s') || e.getAttribute('data-p') || '') + ' ' + b.height.toFixed(1)); });
  return out; }'''
JS_LABELS = '''() => [...document.querySelectorAll('#nlzk input, #nlzk select, #nlne input')].map(e => ({id: e.id,
  label: (e.labels && e.labels.length ? e.labels[0].textContent : (e.getAttribute('aria-label') || '')).trim()})).filter(x => !x.label).map(x => x.id)'''
JS_GROUPS = '''() => [...document.querySelectorAll('#nlzk [role="group"], #nlne [role="group"]')].filter(g => g.offsetParent !== null).map(g => {
  const id = g.getAttribute('aria-labelledby'); const l = id && document.getElementById(id); return l ? l.textContent.trim() : ''; })'''
JS_EXPECT = '''async (over) => { const Z = await fetch('/plugins/nadlan-config/assets/instruments/data/zakaut.json').then(r => r.json());
  const v = Object.assign(window.NLZK.defaults(), over); const r = window.NLZK.compute(v, Z);
  return r.error ? {err: r.error.msg} : {head: window.NLZK.headline(r, Z).value, total: r.total, points: r.points, status: r.status}; }'''

def fig(page):
    return page.locator('#nlzk .nlzk__fig').inner_text().strip()

def typ(page, sel, text):
    loc = page.locator(sel); loc.click(); loc.press('Control+A'); loc.press('Backspace')
    if text: page.keyboard.type(text)
    page.wait_for_timeout(250)

def press(page, sel):
    page.locator(sel).click(); page.wait_for_timeout(180)

def common(page, tag):
    hs = page.evaluate(JS_HSCROLL)
    check(tag + ' no horizontal scroll', hs['sw'] <= hs['iw'] + 1, hs)
    small = page.evaluate(JS_SMALL)
    check(tag + ' every visible control at least 44 px high', not small, small[:6])
    check(tag + ' every input and select labelled', not page.evaluate(JS_LABELS), page.evaluate(JS_LABELS))
    groups = page.evaluate(JS_GROUPS)
    check(tag + ' every visible group named', all(groups), groups[:4])

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
            print(f'\n{W}x{H}')
            ctx = br.new_context(viewport={'width': W, 'height': H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, locale='he-IL')
            page = ctx.new_page(); errs = []
            page.on('console', lambda m, errs=errs: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
            page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
            page.goto(BASE, wait_until='networkidle')
            page.wait_for_selector('#nlzk .nlzk__fig bdi'); page.wait_for_selector('#nlne .nlne__res')
            check(tag + ' opens on the family example: 89,856 ₪', fig(page) == '89,856 ₪', fig(page))
            check(tag + ' opening values 3 / 2 / 2 / 4 / 24 / 20', [page.input_value(s) for s in ('#nlzk-years', '#nlzk-children', '#nlzk-sib1', '#nlzk-sib2', '#nlzk-svc1', '#nlzk-svc2')] == ['3', '2', '2', '4', '24', '20'])
            ls = page.locator('#nlzk ol.nlzk__ls').inner_text()
            check(tag + ' lines: 350, 500, 100, 400, 1,350, 62,400, 27,456', all(x in ls for x in ('350 נקודות', '500 נקודות', '100 נקודות', '400 נקודות', '1,350', '62,400 ₪', '27,456 ₪')), ls[:200])
            check(tag + ' source chips carry the page date', page.locator('#nlzk .nlzk__s a', has_text='S3 · עודכן 30.3.2026').count() >= 1 and page.locator('#nlzk .nlzk__s a', has_text='S7 · עודכן 6.5.2024').count() >= 1)
            more = page.locator('#nlzk .nlzk__more').inner_text()
            pcts = sorted(set(re.findall(r'\d+(?:\.\d+)?%', more)))
            check(tag + ' the rate rule in words; the only percentages are 0.5% and 3% of the rule', '0.5% מתחת לממוצע הצמודות של בנק ישראל, ולא יותר מ־3%' in more and pcts == ['0.5%', '3%'], pcts)
            check(tag + ' binding line (S1)', 'מופיעים בתעודת הזכאות' in page.locator('#nlzk .nlzk__bind').inner_text())
            check(tag + ' official links S1 to S14 and the official calculator', page.locator('#nlzk .nlzk__more a[href^="https://www.gov.il/"]').count() >= 14 and page.locator('#nlzk a', has_text='המחשבון הרשמי').count() == 1)
            ff = page.evaluate('() => [".nlzk__lk", ".nlzk__lede", ".nlzk__more li"].map(s => getComputedStyle(document.querySelector("#nlzk " + s)).fontFamily.split(",")[0])')
            check(tag + ' running text in IBM Plex Sans Hebrew', all('Plex Sans Hebrew' in f for f in ff), ff)
            fm = page.evaluate('() => [".nlzk__fig", ".nlzk__lv", "#nlzk-years"].map(s => getComputedStyle(document.querySelector(s.startsWith("#") ? s : "#nlzk " + s)).fontFamily.split(",")[0])')
            check(tag + ' numbers in IBM Plex Mono', all('Plex Mono' in f for f in fm), fm)
            cols = page.evaluate('() => getComputedStyle(document.querySelector("#nlzk .nlzk__grid")).gridTemplateColumns.split(" ").length')
            check(tag + ' layout: ' + ('one column on the phone' if mob else 'form and result side by side'), cols == (1 if mob else 2), cols)
            common(page, tag + ' family')
            page.screenshot(path=str(OUT / f'page-default-{tag}.png'), full_page=True)

            # the eight profiles (state carries over: only the profile changes, as for a reader)
            profiles = page.evaluate('() => window.NLZK.PROFILES.map(p => p.k)')
            for k in profiles:
                press(page, f'#nlzk button[data-p="{k}"]')
                e = page.evaluate(JS_EXPECT, {'profile': k})
                f = fig(page)
                check(f'{tag} profile {k}: pressed, headline = NLZK ({e.get("head")})', page.get_attribute(f'#nlzk button[data-p="{k}"]', 'aria-pressed') == 'true' and f == e.get('head'), f)
                if k in ('olim_family', 'single', 'dis_single', 'oleh') and e.get('status') == 'ok':
                    check(f'{tag} profile {k}: the shekel figure carries the unverified label', 'לפי טבלת הסכומים למשפחות ותיקות (S3); לבדוק בתעודת הזכאות' in page.locator('#nlzk .nlzk__sub').inner_text(), page.locator('#nlzk .nlzk__sub').inner_text())
                if e.get('status') == 'noband':
                    check(f'{tag} profile {k}: {e.get("points")} points is below the S3 table, so no shekel figure and the reason is said', 'אין שורה בטבלת הסכומים' in page.locator('#nlzk .nlzk__sub').inner_text() and '₪' not in fig(page), page.locator('#nlzk .nlzk__sub').inner_text())
                common(page, f'{tag} {k}')
                page.locator('#nlzk').screenshot(path=str(OUT / f'mzakaut-{k}-{tag}.png'))
            # profile fields that appear and hide
            press(page, '#nlzk button[data-p="dis_family"]'); press(page, '#nlzk button[data-s="olim"][data-val="1"]')
            check(tag + ' disabled family + olim: seniority field shown, marriage field hidden', page.locator('#nlzk-israel').is_visible() and not page.locator('#nlzk-years').is_visible())
            e = page.evaluate(JS_EXPECT, {'profile': 'dis_family', 'olim': True}); check(tag + ' disabled olim family headline = NLZK', fig(page) == e['head'], [fig(page), e['head']])
            press(page, '#nlzk button[data-s="olim"][data-val="0"]')

            # family interactions
            press(page, '#nlzk button[data-p="family"]')
            press(page, '#nlzk button[data-s="zone"][data-val="a"]')
            check(tag + " zone א: 222,738 ₪ (85,250 + 37,488 + 100,000)", fig(page) == '222,738 ₪', fig(page))
            page.locator('#nlzk').screenshot(path=str(OUT / f'mzakaut-family-zone-a-{tag}.png'))
            press(page, '#nlzk button[data-s="zone"][data-val="none"]')
            press(page, '#nlzk button[data-s="res1"][data-val="1"]')
            check(tag + ' reserve yes: the days field appears', page.locator('#nlzk-res1d').is_visible())
            typ(page, '#nlzk-res1d', '90')
            check(tag + ' reserve 90 days: 91,728 ₪ and the S2 / S7 wording', fig(page) == '91,728 ₪' and 'עבור כל 15 ימי מילואים מלאים' in page.locator('#nlzk .nlzk__ls').inner_text(), fig(page))
            press(page, '#nlzk button[data-s="res1"][data-val="0"]')
            for q in ('tp_stay', 'tp_fam', 'tp_income'): press(page, f'#nlzk button[data-s="{q}"][data-val="1"]')
            lt = page.locator('#nlzk .nlzk__ls').inner_text()
            check(tag + ' 10 פלוס all yes with 2 children: included', '132,000 ₪' in lt and fig(page) == '221,856 ₪', fig(page))
            press(page, '#nlzk button[data-s="zone"][data-val="b"]')
            check(tag + ' 10 פלוס in a priority zone with 2 children: not included, says 4 children', '4 ילדים לפחות' in page.locator('#nlzk .nlzk__ls').inner_text())
            page.locator('#nlzk').screenshot(path=str(OUT / f'mzakaut-family-tenplus-zone-b-{tag}.png'))
            press(page, '#nlzk button[data-s="zone"][data-val="none"]')
            for q in ('tp_stay', 'tp_fam', 'tp_income'): press(page, f'#nlzk button[data-s="{q}"][data-val="0"]')
            press(page, '#nlzk button[data-s="negev"][data-val="1"]')
            check(tag + ' Negev: the range in words, total unchanged', '48,000 עד 84,000 ₪ לפי היישוב' in page.locator('#nlzk .nlzk__ls').inner_text() and fig(page) == '89,856 ₪', fig(page))
            press(page, '#nlzk button[data-s="negev"][data-val="0"]')
            typ(page, '#nlzk-rate', '2.5')
            check(tag + ' rate 2.5% from the certificate: first payment 355 ₪ for 30 years', '355 ₪ בחודש' in page.locator('#nlzk .nlzk__pay').inner_text(), page.locator('#nlzk .nlzk__pay').inner_text())
            page.select_option('#nlzk-term', '20'); page.wait_for_timeout(200)
            check(tag + ' term select 20 years changes the payment', 'ל־20 שנה' in page.locator('#nlzk .nlzk__pay').inner_text(), page.locator('#nlzk .nlzk__pay').inner_text())
            typ(page, '#nlzk-rate', '')
            check(tag + ' rate emptied: no payment line', not page.locator('#nlzk .nlzk__pay').is_visible())
            page.locator('#nlzk-married').fill('2016-01-10'); page.wait_for_timeout(300)
            check(tag + ' marriage date 10.1.2016 fills 10 full years', page.input_value('#nlzk-years') == '10' and 'שנות נישואין: 10' in page.locator('#nlzk .nlzk__ls').inner_text(), page.input_value('#nlzk-years'))
            typ(page, '#nlzk-years', '1'); typ(page, '#nlzk-children', '0'); typ(page, '#nlzk-sib1', '1'); typ(page, '#nlzk-sib2', '1')
            check(tag + ' under 599 points: "אין הלוואה לפי הניקוד", never "0 ₪"', fig(page) == 'אין הלוואה לפי הניקוד' and '0 ₪' not in page.locator('#nlzk .nlzk__out').inner_text().replace('00 ₪', ''), fig(page))
            page.locator('#nlzk').screenshot(path=str(OUT / f'mzakaut-family-under599-{tag}.png'))
            typ(page, '#nlzk-children', 'x')
            check(tag + ' a bad value: the message on its field', page.locator('[data-err="children"]').inner_text() != '', page.locator('[data-err="children"]').inner_text())
            typ(page, '#nlzk-children', '2')

            # the converter
            typ(page, '#nlne-n', '4.5')
            check(tag + ' 4.5% nominal = 4.59% effective', page.input_value('#nlne-e') == '4.59' and '0.375%' in page.locator('#nlne .nlne__res').inner_text(), page.input_value('#nlne-e'))
            typ(page, '#nlne-e', '4.5')
            check(tag + ' 4.5% effective = 4.41% nominal', page.input_value('#nlne-n') == '4.41', page.input_value('#nlne-n'))
            press(page, '#nlne button[data-t="fixed_nl"]')
            check(tag + ' chip "קבועה לא צמודה": 4.7162% effective = 4.62% nominal, pressed', page.input_value('#nlne-e') == '4.7162' and page.input_value('#nlne-n') == '4.62' and page.get_attribute('#nlne button[data-t="fixed_nl"]', 'aria-pressed') == 'true', [page.input_value('#nlne-e'), page.input_value('#nlne-n')])
            check(tag + ' the example names its month', 'בספטמבר 2026' in page.locator('#nlne').inner_text())
            typ(page, '#nlne-n', '45')
            check(tag + ' 45%: an error on the field', page.locator('[data-err="n"]').inner_text() != '')
            typ(page, '#nlne-n', '4.5')
            common(page, tag + ' converter')
            page.locator('#nlne').screenshot(path=str(OUT / f'mnomeff-{tag}.png'))
            page.screenshot(path=str(OUT / f'page-after-{tag}.png'), full_page=True)
            check(tag + ' no console error or warning, no page error', not errs, errs[:5])
            ctx.close()

        # one phone pass under the live theme stylesheets (read only)
        print('\n390 + live theme')
        ctx = br.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=2, locale='he-IL')
        page = ctx.new_page(); errs = []
        page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
        page.on('console', lambda m, errs=errs: errs.append(m.text + ' @ ' + str((m.location or {}).get('url', ''))) if m.type == 'error' and 'nad-lan.co.il' not in m.text + str((m.location or {}).get('url', '')) else None)  # the live theme's own assets (its fonts refuse a 127.0.0.1 origin) are not ours to judge here
        page.goto(BASE + '?theme=1', wait_until='networkidle')
        page.wait_for_selector('#nlzk .nlzk__fig bdi')
        check('theme 390 opens on 89,856 ₪', fig(page) == '89,856 ₪', fig(page))
        common(page, 'theme 390')
        ff = page.evaluate('() => [getComputedStyle(document.querySelector("#nlzk h2.nlzk__h")).fontFamily.split(",")[0], getComputedStyle(document.querySelector("#nlzk button[data-p]")).borderRadius]')
        check('theme 390: heading face and button radius hold against the theme', 'Plex Sans Hebrew' in ff[0] and ff[1] == '2px', ff)
        page.locator('#nlzk').screenshot(path=str(OUT / 'mzakaut-family-theme-390.png'))
        page.locator('#nlne').screenshot(path=str(OUT / 'mnomeff-theme-390.png'))
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
