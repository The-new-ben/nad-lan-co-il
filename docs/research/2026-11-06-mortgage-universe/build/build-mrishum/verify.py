"""HAD-675 (mortgage universe): press the new tool mrishum ("רישום משכנתה ואגרות") of preview.html in headless Chrome (Playwright,
channel chrome), at 390x844 (is_mobile, touch) and 1280x900.

Every path is pressed (4 registries x 5 actions x each "who" the path offers: 33 per width) and the headline is compared with
window.NLRS on the same choices; then the extract choice, the five exemptions, the amendment kind, the pledge years (a good value,
a bad value), the checklist ticks, both copy buttons (clipboard read back), the print button (stubbed), and a shared #mrishum= link.
On every view: no console error or warning, no horizontal scroll, every visible control at least 44 px high, every input labelled,
every visible group named. The page text is checked for long dashes, the banned words and a "sixty days" deadline. One more phone pass
with the live theme stylesheets (?theme=1, read only).
The script starts its own http.server on a free 127.0.0.1 port (the repo root) and stops it in finally, whatever happens.
Screenshots go to build-mrishum/shots, the report to verify.json; exit 1 on any failed check. Nothing is sent anywhere.
Run:  python docs/research/2026-11-06-mortgage-universe/build/build-mrishum/verify.py
"""
import json, sys, pathlib, re, socket, subprocess, time, urllib.request
from playwright.sync_api import sync_playwright

try: sys.stdout.reconfigure(encoding='utf-8')  # Hebrew in the log on a Windows console
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
_s = socket.socket(); _s.bind(('127.0.0.1', 0)); PORT = _s.getsockname()[1]; _s.close()
BASE = f'http://127.0.0.1:{PORT}/docs/research/2026-11-06-mortgage-universe/build/build-mrishum/preview.html'
OUT = HERE / 'shots'
OUT.mkdir(parents=True, exist_ok=True)
report, fails = [], []
LONG = re.compile('[\u2013\u2014]')
BANNED = re.compile('\u05de\u05de\u05e9\u05e7|(^|[^\u0590-\u05ff])\u05d3\u05de\u05d5([^\u0590-\u05ff]|$)|\u05d4\u05d3\u05d2\u05de\u05d4|\u05e1\u05d9\u05de\u05d5\u05dc\u05e6\u05d9\u05d4|\u05de\u05e0\u05d2\u05e0\u05d5\u05df|\u05d0\u05d9\u05e0\u05d8\u05e8\u05d0\u05e7\u05d8\u05d9\u05d1\u05d9|\u05d4\u05de\u05e2\u05e8\u05db\u05ea|\u05d4\u05e4\u05dc\u05d8\u05e4\u05d5\u05e8\u05de\u05d4|\u05d8\u05db\u05e0\u05d5\u05dc\u05d5\u05d2\u05d9\u05d4')
SIXTY = re.compile('(^|[^\\d])6' + '0[\\s\\-]*(\u05d9\u05de\u05d9\u05dd|\u05d9\u05d5\u05dd|days?)', re.I)

def check(name, cond, got=None):
    report.append({'check': name, 'ok': bool(cond), 'got': got})
    print(('  ok   ' if cond else '  FAIL ') + name + ('' if got is None else '  [' + str(got)[:160] + ']'))
    if not cond: fails.append(name)

JS_HSCROLL = '() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth})'
JS_SMALL = '''() => { const out = [];
  document.querySelectorAll('#nlrs button, #nlrs input:not([type="checkbox"]), #nlrs select, #nlrs summary, #nlrs label.nlrs__ck').forEach(e => { const b = e.getBoundingClientRect();
    if (b.width > 0 && b.height > 0 && b.height < 43.5) out.push(e.tagName + '.' + (e.getAttribute('data-s') || '') + '=' + (e.getAttribute('data-val') || e.id || '') + ' ' + b.height.toFixed(1)); });
  return out; }'''
JS_LABELS = '''() => [...document.querySelectorAll('#nlrs input, #nlrs select')].filter(e => e.offsetParent !== null).map(e => ({id: e.id,
  label: (e.labels && e.labels.length ? e.labels[0].textContent : (e.getAttribute('aria-label') || '')).trim()})).filter(x => !x.label).map(x => x.id)'''
JS_GROUPS = '''() => [...document.querySelectorAll('#nlrs [role="group"]')].filter(g => g.offsetParent !== null).map(g => {
  const id = g.getAttribute('aria-labelledby'); const l = id && document.getElementById(id); return l ? l.textContent.trim() : ''; })'''
JS_EXPECT = '''async (over) => { const D = await fetch('/plugins/nadlan-config/assets/instruments/data/rishum.json').then(r => r.json());
  const v = Object.assign(window.NLRS.defaults(), over); const r = window.NLRS.compute(v, D);
  return r.error ? {err: r.error.msg} : {head: window.NLRS.headline(r, D).value, total: r.total, status: r.status, who: r.who, show: window.NLRS.showTotal(r)}; }'''

def fig(page):
    return page.locator('#nlrs .nlrs__fig').inner_text().strip()

def press(page, key, val):
    page.locator(f'#nlrs button[data-s="{key}"][data-val="{val}"]').click(); page.wait_for_timeout(120)

def pressed(page, key, val):
    return page.get_attribute(f'#nlrs button[data-s="{key}"][data-val="{val}"]', 'aria-pressed') == 'true'

def typ(page, sel, text):
    loc = page.locator(sel); loc.click(); loc.press('Control+A'); loc.press('Backspace')
    if text: page.keyboard.type(text)
    page.wait_for_timeout(250)

def common(page, tag):
    hs = page.evaluate(JS_HSCROLL)
    check(tag + ' no horizontal scroll', hs['sw'] <= hs['iw'] + 1, hs)
    small = page.evaluate(JS_SMALL)
    check(tag + ' every visible control at least 44 px high', not small, small[:6])
    nolab = page.evaluate(JS_LABELS)
    check(tag + ' every visible input labelled', not nolab, nolab)
    groups = page.evaluate(JS_GROUPS)
    check(tag + ' every visible group named', all(groups) and len(groups) >= 3, groups[:8])

def words(page, tag):
    tx = page.locator('#nlrs').inner_text()
    check(tag + ' page text: no long dash', not LONG.search(tx))
    check(tag + ' page text: no banned word', not BANNED.search(tx), (BANNED.search(tx) or [''])[0] if BANNED.search(tx) else None)
    check(tag + ' page text: no sixty-day deadline', not SIXTY.search(tx))

server = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(REPO)],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(60):
        try:
            urllib.request.urlopen(BASE, timeout=1); break
        except Exception:
            time.sleep(0.25)
    print('local server on 127.0.0.1:' + str(PORT))
    with sync_playwright() as p:
        br = p.chromium.launch(channel='chrome', headless=True)
        for W, H, mob in ((390, 844, True), (1280, 900, False)):
            tag = str(W)
            print(f'\n{W}x{H}')
            ctx = br.new_context(viewport={'width': W, 'height': H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, locale='he-IL',
                                 permissions=['clipboard-read', 'clipboard-write'])
            page = ctx.new_page(); errs = []
            page.on('console', lambda m, errs=errs: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
            page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
            page.goto(BASE, wait_until='networkidle')
            page.wait_for_selector('#nlrs .nlrs__fig bdi')
            check(tag + ' opens on tabu, registration, lawyer online: 206 ₪ (188 + 18)', fig(page) == '206 ₪', fig(page))
            check(tag + ' the opening tiles are pressed', pressed(page, 'reg', 'tabu') and pressed(page, 'act', 'register') and pressed(page, 'who', 'lawyer') and pressed(page, 'nes', 'online'))
            ls = page.locator('#nlrs ol.nlrs__ls').inner_text()
            check(tag + ' ledger: 188 ₪ registration, 18 ₪ extract, total 206 ₪, items 2(א) and 7(א2)', all(x in ls for x in ('188 ₪', '18 ₪', '206 ₪', 'פרט 2(א)', 'פרט 7(א2)', 'לשלם למדינה')), ls[:160])
            check(tag + ' source chips link the 2026 notice and the regulations', page.locator('#nlrs a[href="https://olaw.org.il/takanot/takanot-12193.pdf"]').count() >= 2 and page.locator('#nlrs a[href*="wikisource"]').count() >= 3)
            check(tag + ' the contact line: *8653, 7 then 1, Sunday to Thursday 8:00 to 16:00, WhatsApp, deed days', all(x in page.locator('#nlrs .nlrs__call').inner_text() for x in ('*8653', 'שלוחה 7 ואז 1', 'ראשון עד חמישי', '8:00 עד 16:00', '073-3929983', 'ראשון ורביעי', '8:30 עד 12:30')))
            check(tag + ' no "לא נקרא" label on the tool (the unread sources are links only)', 'לא נקרא' not in page.locator('#nlrs').inner_text())
            check(tag + ' the source line names the 2026 notice and its dates', all(x in page.locator('#nlrs [data-srcline]').inner_text() for x in ('23.12.2025', '24.12.2025', '12193', 'נבדק ב־6.11.2026')))
            check(tag + ' the checklist is titled "טופס רישום משכנתא" and links the gov.il forms page', 'טופס רישום משכנתא' in page.locator('#nlrs .nlrs__more').inner_text() and page.locator('#nlrs .nlrs__links a[href="https://www.gov.il/he/departments/dynamiccollectors/land-registration-forms"]').count() >= 1)
            ff = page.evaluate('() => [".nlrs__p", ".nlrs__lk", ".nlrs__h"].map(s => getComputedStyle(document.querySelector("#nlrs " + s)).fontFamily.split(",")[0])')
            check(tag + ' running text in IBM Plex Sans Hebrew', all('Plex Sans Hebrew' in f for f in ff), ff)
            fm = page.evaluate('() => [".nlrs__fig", ".nlrs__lv"].map(s => getComputedStyle(document.querySelector("#nlrs " + s)).fontFamily.split(",")[0])')
            check(tag + ' amounts in IBM Plex Mono', all('Plex Mono' in f for f in fm), fm)
            cols = page.evaluate('() => getComputedStyle(document.querySelector("#nlrs .nlrs__grid")).gridTemplateColumns.split(" ").length')
            check(tag + ' layout: ' + ('one column on the phone' if mob else 'the steps and the result side by side'), cols == (1 if mob else 2), cols)
            common(page, tag + ' default'); words(page, tag + ' default')
            page.screenshot(path=str(OUT / f'page-default-{tag}.png'), full_page=True)

            # every path (nesach, exemption, years and amendment stay at their defaults while the path is pressed)
            n_paths = 0
            for reg in ('tabu', 'ila', 'company', 'none'):
                press(page, 'reg', reg)
                for act in ('register', 'second', 'amend', 'cancel', 'death'):
                    press(page, 'act', act)
                    opts = page.evaluate('([r, a]) => window.NLRS.whoOpts(r, a)', [reg, act])
                    for who in opts:
                        press(page, 'who', who)
                        e = page.evaluate(JS_EXPECT, {'reg': reg, 'act': act, 'who': who})
                        f = fig(page); n_paths += 1
                        if e.get('show'):
                            tot_ok = page.locator('#nlrs li.is-total .nlrs__lv').inner_text().strip() == f'{e["total"]:,} ₪'
                        else:
                            tot_ok = page.locator('#nlrs li.is-total').count() == 0
                        check(f'{tag} {reg} · {act} · {who}: pressed, headline = NLRS ({e.get("head")}), total row', pressed(page, 'reg', reg) and pressed(page, 'act', act) and pressed(page, 'who', who) and f == e.get('head') and tot_ok, f)
                        if (reg, act, who) in (('tabu', 'cancel', 'bank'), ('tabu', 'cancel', 'office'), ('tabu', 'death', 'bank'), ('ila', 'register', 'owner'), ('ila', 'register', 'rep'), ('ila', 'amend', 'owner'), ('company', 'register', 'lawyer'), ('company', 'amend', 'lawyer'), ('none', 'register', 'lawyer'), ('ila', 'cancel', 'bank')):
                            page.locator('#nlrs').screenshot(path=str(OUT / f'mrishum-{reg}-{act}-{who}-{tag}.png'))
                        if (reg, act) in (('tabu', 'cancel'), ('ila', 'register'), ('none', 'register'), ('company', 'amend')):
                            common(page, f'{tag} {reg} {act} {who}')
            check(f'{tag} all 33 paths pressed', n_paths == 33, n_paths)
            ct = page.locator('#nlrs').inner_text()
            check(tag + ' after death (none): the s.9ח2 deferral of 12 months is said', 'עד 12 חודשים מהפטירה' in ct)
            words(page, tag + ' after the paths')

            # the Israel Land Authority path (the service page read by hand on 6.11.2026)
            press(page, 'reg', 'ila'); press(page, 'act', 'register')
            check(tag + ' ILA: step 3 offers the rights holder and a representative, the rights holder pressed', pressed(page, 'who', 'owner') and page.locator('#nlrs button[data-s="who"][data-val="rep"]').count() == 1 and page.locator('#nlrs button[data-s="who"][data-val="office"]').count() == 0)
            check(tag + ' ILA: headline "לא מופיעה בדף השירות", no total row', fig(page) == 'לא מופיעה בדף השירות' and page.locator('#nlrs li.is-total').count() == 0, fig(page))
            res = page.locator('#nlrs .nlrs__res').inner_text()
            check(tag + ' ILA: the facts read are on the page (personal area, national identification, 90.02B, digital original, undertaking)', all(x in res for x in ('רמ״י שלי', 'מערכת ההזדהות הלאומית', '90.02B', 'עותק מודפס לא נחשב נסח רשמי', 'אלא אם באותו מעמד תירשם גם המשכנתה')), res[:120])
            check(tag + ' ILA: the warning note is outside the total', 'לא בסך הכול: דף השירות של רמ״י לא מזכיר הערה כזו' in page.locator('#nlrs ol.nlrs__ls').inner_text())
            call = page.locator('#nlrs .nlrs__call').inner_text()
            check(tag + ' ILA: the contact card shows the ILA call centre *5575, 03-9533333, 8:00 to 17:00', page.locator('#nlrs [data-ilacall]').is_visible() and all(x in call for x in ('*5575', '03-9533333', '8:00 עד 17:00')), call[:80])
            ck = page.locator('#nlrs [data-ck]').inner_text()
            check(tag + ' ILA checklist (rights holder): referral letter, everyone signs, the form; no power of attorney', 'מכתב הפנייה מהבנק' in ck and 'כל בעלי הזכויות' in ck and 'ייפוי כוח' not in ck and page.locator('#nlrs [data-ck] a[href="https://www.gov.il/BlobFolder/policy/9002b-procedure/he/forms_wform351.pdf"]').count() == 1, ck[:80])
            check(tag + ' ILA links: the service page and the official form are listed', page.locator('#nlrs [data-ilalink] a[href="https://www.gov.il/he/service/guide-mortgage"]').is_visible() and page.locator('#nlrs [data-ilalink] a[href="https://www.gov.il/BlobFolder/policy/9002b-procedure/he/forms_wform351.pdf"]').is_visible())
            press(page, 'who', 'rep')
            check(tag + ' ILA, a representative: the power of attorney joins the checklist', 'ייפוי כוח כדין' in page.locator('#nlrs [data-ck]').inner_text() and 'המייצג נכנס לאזור האישי' in page.locator('#nlrs [data-steps]').inner_text())
            tx = page.locator('#nlrs').inner_text()
            check(tag + ' ILA: no "לא נקרא" and no "לא ידוע" anywhere in the tool', 'לא נקרא' not in tx and 'לא ידוע' not in tx)
            common(page, tag + ' ILA'); words(page, tag + ' ILA')
            page.locator('#nlrs').screenshot(path=str(OUT / f'mrishum-ila-register-rep-checked-{tag}.png'))
            press(page, 'reg', 'tabu')
            check(tag + ' back to tabu: the ILA call centre and links hide, step 3 is the lawyer and the office again', not page.locator('#nlrs [data-ilacall]').is_visible() and not page.locator('#nlrs [data-ilalink] a[href="https://www.gov.il/he/service/guide-mortgage"]').is_visible() and pressed(page, 'who', 'lawyer'))

            # tabu, registration: the extract and the exemptions
            press(page, 'reg', 'tabu'); press(page, 'act', 'register'); press(page, 'who', 'lawyer')
            press(page, 'nes', 'counter'); check(tag + ' counter extract: 276 ₪ (188 + 88)', fig(page) == '276 ₪', fig(page))
            press(page, 'nes', 'none'); check(tag + ' no extract: 188 ₪', fig(page) == '188 ₪', fig(page))
            press(page, 'nes', 'online'); check(tag + ' online extract: 206 ₪', fig(page) == '206 ₪', fig(page))
            for ex in ('disabled', 'bereaved_idf', 'bereaved_terror', 'terror', 'olim'):
                press(page, 'ex', ex)
                exb = page.locator('#nlrs [data-exb]').inner_text()
                check(f'{tag} exemption {ex}: 188 becomes 0, 18 ₪ left for the extract, conditions shown', fig(page) == '18 ₪' and 'במסלול הזה: 0 ₪' in exb and page.locator('#nlrs .nlrs__exb li').count() >= 3 and page.locator('#nlrs li.is-ex').count() == 1, [fig(page), exb])
                if ex in ('bereaved_idf', 'olim'): page.locator('#nlrs').screenshot(path=str(OUT / f'mrishum-exempt-{ex}-{tag}.png'))
            press(page, 'ex', 'bereaved_idf')
            exs = page.locator('#nlrs .nlrs__exb').inner_text()
            check(tag + ' bereaved IDF families: MoD approval within 7 work days, orphans up to 30, refund within 12 months', '7 ימי עבודה' in exs and 'יתומים עד גיל 30' in exs and 'תוך 12 חודשים' in exs, exs[:120])
            check(tag + ' the exemption approval replaces the fee receipt in the checklist', 'אישור הזכאות לפטור' in page.locator('#nlrs [data-ck]').inner_text() and 'אישור על תשלום האגרה' not in page.locator('#nlrs [data-ck]').inner_text())
            common(page, tag + ' exemption')
            press(page, 'act', 'amend')
            check(tag + ' amendment: the amendment kind appears, 206 ₪, the exemption does not lower it', page.locator('#nlrs [data-g="amend"]').is_visible() and fig(page) == '206 ₪' and 'לא מוריד' in page.locator('#nlrs [data-exb]').inner_text(), fig(page))
            press(page, 'amend', 'inc')
            check(tag + ' amendment, increase of the loan: item 2(א)', 'הגדלת סכום ההלוואה' in page.locator('#nlrs ol.nlrs__ls').inner_text() and 'פרט 2(א)' in page.locator('#nlrs ol.nlrs__ls').inner_text())
            press(page, 'amend', 'terms'); press(page, 'ex', 'none'); press(page, 'act', 'register')
            check(tag + ' exemption back to none: 206 ₪, no exemption block', fig(page) == '206 ₪' and not page.locator('#nlrs [data-exsec]').is_visible(), fig(page))

            # the checklist
            boxes = page.locator('#nlrs [data-ck] input[type="checkbox"]')
            check(tag + ' tabu registration checklist: 8 documents with checkboxes', boxes.count() == 8, boxes.count())
            page.locator('#nlrs label.nlrs__ck').first.click(); page.wait_for_timeout(100)
            check(tag + ' a checklist item ticks by its label', boxes.first.is_checked())

            # copy buttons and print
            page.locator('#nlrs button[data-copy]').click(); page.wait_for_timeout(300)
            clip = page.evaluate('() => navigator.clipboard.readText()')
            check(tag + ' copy summary: the path, the total, the dates and a #mrishum= link', 'לשלם למדינה: 206 ₪' in clip and '#mrishum=tabu.register.lawyer.online.none.25.terms' in clip and '23.12.2025' in clip, clip[:120])
            page.locator('#nlrs button[data-copyck]').click(); page.wait_for_timeout(300)
            clip = page.evaluate('() => navigator.clipboard.readText()')
            check(tag + ' copy checklist: "טופס רישום משכנתא", 8 lines, the forms URL', clip.startswith('טופס רישום משכנתא') and clip.count('[ ] ') == 8 and 'land-registration-forms' in clip, clip[:80])
            page.evaluate('() => { window.__printed = 0; window.print = () => { window.__printed++; }; }')
            page.locator('#nlrs button[data-print]').click(); page.wait_for_timeout(100)
            check(tag + ' print button calls window.print', page.evaluate('() => window.__printed') == 1)

            # not registered yet: the pledge years
            press(page, 'reg', 'none'); press(page, 'act', 'register')
            check(tag + ' pledge: the years field appears, 25 years online = 190 ₪', page.locator('#nlrs-years').is_visible() and fig(page) == '190 ₪', fig(page))
            typ(page, '#nlrs-years', '3')
            check(tag + ' pledge 3 years online: 114 ₪', fig(page) == '114 ₪', fig(page))
            press(page, 'who', 'office')
            check(tag + ' pledge 3 years at the counter: 135 ₪', fig(page) == '135 ₪', fig(page))
            typ(page, '#nlrs-years', '5')
            check(tag + ' pledge 5 years at the counter: 225 ₪', fig(page) == '225 ₪', fig(page))
            press(page, 'who', 'lawyer')
            check(tag + ' pledge 5 years online: 190 ₪', fig(page) == '190 ₪', fig(page))
            typ(page, '#nlrs-years', '0')
            check(tag + ' years 0: the message on its field', page.locator('#nlrs [data-err="years"]').inner_text() != '' and page.locator('#nlrs .nlrs__msg').is_visible(), page.locator('#nlrs [data-err="years"]').inner_text())
            typ(page, '#nlrs-years', '25')
            check(tag + ' years 25 again: 190 ₪', fig(page) == '190 ₪', fig(page))
            press(page, 'nes', 'online')
            check(tag + ' pledge + internet search of the register: 202 ₪ (190 + 12)', fig(page) == '202 ₪', fig(page))
            common(page, tag + ' pledge')
            page.locator('#nlrs').screenshot(path=str(OUT / f'mrishum-none-register-search-{tag}.png'))
            page.screenshot(path=str(OUT / f'page-after-{tag}.png'), full_page=True)
            check(tag + ' no console error or warning, no page error', not errs, errs[:5])
            ctx.close()

            # a shared link opens on its case
            ctx = br.new_context(viewport={'width': W, 'height': H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, locale='he-IL')
            page = ctx.new_page(); errs2 = []
            page.on('pageerror', lambda e, errs2=errs2: errs2.append(str(e)))
            page.goto(BASE + '#mrishum=none.second.office.counter.olim.3.inc', wait_until='networkidle')
            page.wait_for_selector('#nlrs .nlrs__fig bdi')
            check(tag + ' #mrishum=none.second.office.counter.olim.3.inc opens on 173 ₪ (3 x 45 + 38), tiles pressed', fig(page) == '173 ₪' and pressed(page, 'reg', 'none') and pressed(page, 'act', 'second') and pressed(page, 'who', 'office') and pressed(page, 'nes', 'counter') and pressed(page, 'ex', 'olim') and page.input_value('#nlrs-years') == '3', fig(page))
            check(tag + ' shared link: no page error', not errs2, errs2[:3])
            ctx.close()

        # one phone pass under the live theme stylesheets (read only)
        print('\n390 + live theme')
        ctx = br.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=2, locale='he-IL')
        page = ctx.new_page(); errs = []
        page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
        page.on('console', lambda m, errs=errs: errs.append(m.text + ' @ ' + str((m.location or {}).get('url', ''))) if m.type == 'error' and 'nad-lan.co.il' not in m.text + str((m.location or {}).get('url', '')) else None)  # the live theme's own assets (its fonts refuse a 127.0.0.1 origin) are not ours to judge here
        page.goto(BASE + '?theme=1', wait_until='networkidle')
        page.wait_for_selector('#nlrs .nlrs__fig bdi')
        check('theme 390 opens on 206 ₪', fig(page) == '206 ₪', fig(page))
        common(page, 'theme 390')
        ff = page.evaluate('() => [getComputedStyle(document.querySelector("#nlrs h2.nlrs__h")).fontFamily.split(",")[0], getComputedStyle(document.querySelector("#nlrs button.nlrs__o")).borderRadius, getComputedStyle(document.querySelector("#nlrs ol.nlrs__ls > li")).listStyleType]')
        check('theme 390: heading face, tile radius and the ledger list hold against the theme', 'Plex Sans Hebrew' in ff[0] and ff[1] == '2px' and ff[2] == 'none', ff)
        press(page, 'act', 'cancel')
        check('theme 390: cancellation pressed = 0 ₪', fig(page) == '0 ₪', fig(page))
        page.locator('#nlrs').screenshot(path=str(OUT / 'mrishum-theme-cancel-390.png'))
        press(page, 'act', 'register')
        page.locator('#nlrs').screenshot(path=str(OUT / 'mrishum-theme-register-390.png'))
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
