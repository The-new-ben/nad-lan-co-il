"""HAD-675 (mortgage universe): press every control of the new tool mhivun ("עמלת היוון") in preview.html, headless Chrome (Playwright,
channel chrome), at 390x844 (is_mobile) and 1280x900, plus one phone pass under the live theme stylesheets (?theme=1, read only).

Every figure is checked against window.NLHV on the same values (the data files fetched again inside the page). Controls pressed: the
four "איך זה חושב" panels, the notice choice (both), a track change with its change cycle (2.5 years, every year), the term unit
(months and back), add row (to 6, the add button then disabled), remove row (twice), a bad and a future month, the partial amount and
both modes, the 24-month table, the bank's number (a gap and a close one), copy, WhatsApp (answered locally, nothing leaves the
machine), the case link (reopened in a new tab), print (window.print replaced by a counter). On every view: no console error or
warning, no horizontal scroll, every visible button, input, select and summary at least 44 px high, every input and select labelled,
every group named, no long dash, none of the banned words, never a bare "₪0".

The script starts its own http.server on a free 127.0.0.1 port (the repo root) and stops it in finally. Screenshots go to
build-mhivun/shots, the report to verify.json; exit 1 on any failed check.
Run:  python docs/research/2026-11-06-mortgage-universe/build/build-mhivun/verify.py
"""
import json, sys, pathlib, re, socket, subprocess, time, urllib.request
from playwright.sync_api import sync_playwright

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
s0 = socket.socket(); s0.bind(('127.0.0.1', 0)); PORT = s0.getsockname()[1]; s0.close()
ORIGIN = f'http://127.0.0.1:{PORT}'
BASE = ORIGIN + '/docs/research/2026-11-06-mortgage-universe/build/build-mhivun/preview.html'
OUT = HERE / 'shots'
OUT.mkdir(parents=True, exist_ok=True)
report, fails = [], []

def check(name, cond, got=None):
    report.append({'check': name, 'ok': bool(cond), 'got': got})
    print(('  ok   ' if cond else '  FAIL ') + name + ('' if got is None else '  [' + str(got)[:180] + ']'))
    if not cond: fails.append(name)

T = '#pv-hivun .nli-host'
FIG = T + ' .mhv > .nli__grid .nli__fig'
PFIG = T + ' [data-sec="part"] .nli__fig'
EX = [{'k': 'fixed_nl', 'amount': 500000, 'date': '2023-07', 'n': 300, 'rate': 5.3},
      {'k': 'prime', 'amount': 450000, 'date': '2023-07', 'n': 300, 'rate': 4.15},
      {'k': 'var_cpi', 'amount': 300000, 'date': '2023-07', 'n': 300, 'rate': 4.2, 'freq': 60},
      {'k': 'fixed_cpi', 'amount': 150000, 'date': '2023-07', 'n': 240, 'rate': 3.9}]
BANNED = ['ממשק', 'דמו', 'הדגמה', 'סימולציה', 'מנגנון', 'אינטראקטיבי', 'המערכת', 'הפלטפורמה', 'טכנולוגיה', 'interface', 'demo']

JS_EXP = '''async (o) => {
  const base = '/plugins/nadlan-config/assets/instruments/data/';
  const D = window.__D || (window.__D = await fetch(base + 'boi-mortgage.json').then(r => r.json()));
  const C = window.__C || (window.__C = await fetch(base + 'cbs-120010.json').then(r => r.json()));
  const H = window.NLHV, now = window.NLMR.nowKey(), f = window.NadLanInstruments.fmt;
  const rows = o.rows.map((r, i) => ({ id: r.id != null ? r.id : i, k: r.k, amount: r.amount, date: r.date, n: r.n, rate: r.rate, freq: H.isVar(r.k) ? (r.freq || 60) : null }));
  const MG = H.mortgage(rows, D, C, now);
  const out = { fee: MG.fee, figure: MG.fee >= 0.5 ? f.ils(MG.fee) : 'אין עמלת היוון', bal: f.ils(MG.bal), now: now, nowLabel: f.month(now) };
  if (o.pp) { const A = H.allocate(MG, o.pp, o.mode || 'reduce', D); out.pfee = A.fee >= 0.5 ? f.ils(A.fee) : 'אין עמלת היוון'; out.drop = f.ils(A.drop); out.first = A.items.length ? A.items[0].id : null; out.n = A.items.length; }
  if (o.strip) { const W = H.strip(rows, D, C, now, 24); out.cheap = W.cheap; out.cheapMonth = W.cheap ? f.month(W.months[W.cheap]) : null; out.cheapFee = W.cheap ? f.ils(W.base[W.cheap]) : null; out.save = f.ils(W.save); out.months = W.months.length; out.ev = W.ev.map((l, j) => l.length ? f.month(W.months[j]) : null).filter(Boolean); }
  if (o.steps) { const l = MG.loans[0], d = H.detail(l); out.steps = [f.ils(l.fx.f3), f.ils(l.fx.f4), f.ils(l.fx.fee), f.ils(d.pvA), f.ils(d.pvC), f.ils(l.fx.bal)]; }
  return out; }'''
JS_HSCROLL = '() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth})'
JS_SMALL = '''(t) => { const out = []; document.querySelectorAll(t + ' button, ' + t + ' input, ' + t + ' select, ' + t + ' summary').forEach(e => { const b = e.getBoundingClientRect();
  if (b.width > 0 && b.height > 0 && b.height < 43.5) out.push(e.tagName + '[' + (e.getAttribute('data-f') || e.getAttribute('data-act') || e.getAttribute('data-s') || e.textContent.trim().slice(0, 20)) + '] ' + b.height.toFixed(1)); }); return out; }'''
JS_LABELS = '''(t) => [...document.querySelectorAll(t + ' input, ' + t + ' select')].map(e => ({id: e.id || e.getAttribute('data-f'),
  label: (e.labels && e.labels.length ? e.labels[0].textContent : (e.getAttribute('aria-label') || '')).trim()})).filter(x => !x.label).map(x => x.id)'''
JS_GROUPS = '''(t) => [...document.querySelectorAll(t + ' [role="group"]')].filter(g => g.offsetParent !== null).map(g => (g.getAttribute('aria-label') || '').trim())'''

def ex_rows(**ch):
    rows = [dict(r) for r in EX]
    for i, kv in ch.items(): rows[int(i[1:])].update(kv)
    return rows

def fig(page, sel=FIG):
    return page.locator(sel).first.inner_text().strip()

def typ(page, sel, text):
    loc = page.locator(sel).first; loc.click(); loc.press('Control+A'); loc.press('Backspace')
    if text: page.keyboard.type(text)
    page.wait_for_timeout(260)

def press(page, sel, wait=200):
    page.locator(sel).first.click(); page.wait_for_timeout(wait)

def tool_text(page):
    return page.locator(T).inner_text()

def common(page, tag):
    hs = page.evaluate(JS_HSCROLL)
    check(tag + ' no horizontal scroll', hs['sw'] <= hs['iw'] + 1, hs)
    small = page.evaluate(JS_SMALL, T)
    check(tag + ' every visible control at least 44 px high', not small, small[:6])
    nolab = page.evaluate(JS_LABELS, T)
    check(tag + ' every input and select labelled', not nolab, nolab)
    groups = page.evaluate(JS_GROUPS, T)
    check(tag + ' every visible group named', all(groups), groups[:6])
    tx = tool_text(page)
    check(tag + ' no long dash, no banned word, never a bare ₪0', not re.search('[\\u2013\\u2014]', tx) and not [w for w in BANNED if w in tx] and not re.search(r'₪0(?![\d.,])', tx),
          [w for w in BANNED if w in tx] + re.findall(r'.{12}₪0(?![\d.,]).{4}', tx)[:2])

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
            print(f'\n{W}x{H}  ({BASE})')
            ctx = br.new_context(viewport={'width': W, 'height': H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, locale='he-IL')
            ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin=ORIGIN)
            ctx.route('https://wa.me/**', lambda route: route.fulfill(status=200, content_type='text/plain', body='local stub'))
            page = ctx.new_page(); errs = []; dialogs = []
            page.on('console', lambda m, errs=errs: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
            page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
            page.on('dialog', lambda d, dialogs=dialogs: (dialogs.append(d.message), d.dismiss()))
            page.goto(BASE, wait_until='networkidle')
            page.wait_for_selector(T + ' [data-card]')
            e0 = page.evaluate(JS_EXP, {'rows': EX, 'pp': 200000, 'strip': True, 'steps': True})
            print('  today in the page: ' + e0['now'])

            # the opening example
            check(tag + ' opens on the example: total = NLHV (' + e0['figure'] + ')', fig(page) == e0['figure'], fig(page))
            check(tag + ' the example is labelled (tag on the answer and the note under the tool)', page.locator(T + ' .mrx__eg').count() >= 1 and 'הערכים בפתיחה הם דוגמה' in page.locator(T + ' .nli__eg').inner_text())
            check(tag + ' 4 rows, 4 cards', page.locator(T + ' [data-row]').count() == 4 and page.locator(T + ' [data-card]').count() == 4)
            check(tag + ' the prime card says why there is no fee', 'ללא: פריים' in page.locator(T + ' [data-card="1"]').inner_text())
            out = page.locator(T + ' .mhv > .nli__grid .nli__out').inner_text()
            check(tag + ' the lines: balance, operational once, notice, CPI fee, totals', all(x in out for x in (e0['bal'], 'עמלה תפעולית, פעם אחת', 'עד ₪60', 'הודעה של פחות מ־10 ימים', 'בפירעון בין ה־1 ל־15 בחודש', 'סך הכול לסילוק')), out[:200])
            strip = page.locator(T + ' .nli__strip').inner_text()
            check(tag + ' the top strip: the averages and their in-force date', '4.788%' in strip and '4.607%' in strip and '19.10.2026' in strip, strip.replace('\n', ' ')[:160])
            check(tag + ' the source line: the Order, the averages file, cir2103, the rates page, the CPI', all(page.locator(T + ' .mhv > .nli__grid .mrx__src a[href*="' + h + '"]').count() >= 1 for h in ('mashfix', 'pribmash', 'cir2103', 'information/interestrates', 'cbs.gov.il')) and 'צו הבנקאות (עמלת פירעון מוקדם), התשס"ב-2002' in out)
            ff = page.evaluate('(t) => [getComputedStyle(document.querySelector(t + " .nli__lede")).fontFamily.split(",")[0], getComputedStyle(document.querySelector(t + " .mhv > .nli__grid .nli__fig")).fontFamily.split(",")[0], getComputedStyle(document.querySelector(t + " h3.mhv__ch")).fontFamily.split(",")[0]]', T)
            check(tag + ' text in IBM Plex Sans Hebrew, the figure in IBM Plex Mono', 'Plex Sans Hebrew' in ff[0] and 'Plex Mono' in ff[1] and 'Plex Sans Hebrew' in ff[2], ff)
            cols = page.evaluate('(t) => getComputedStyle(document.querySelector(t + " .mhv > .nli__grid")).gridTemplateColumns.split(" ").length', T)
            check(tag + ' layout: ' + ('one column on the phone' if mob else 'form and result side by side'), cols == (1 if mob else 2), cols)
            check(tag + ' "מה זה היוון משכנתא" section', page.locator(T + ' h3.mrx__h', has_text='מה זה היוון משכנתא').count() == 1 and 'הפרשי היוון' in tool_text(page))
            common(page, tag + ' example')
            page.screenshot(path=str(OUT / f'page-default-{tag}.png'), full_page=True)

            # how it is calculated: all four
            for i in range(4):
                press(page, f'{T} details[data-how="{i}"] > summary')
                check(f'{tag} "איך זה חושב" {i + 1} opens with its steps', page.get_attribute(f'{T} details[data-how="{i}"]', 'open') is not None and page.locator(f'{T} details[data-how="{i}"] ol li').count() >= 4, page.locator(f'{T} details[data-how="{i}"] ol li').count())
            s1 = page.locator(f'{T} details[data-how="0"]').inner_text()
            check(tag + ' track 1 steps carry the numbers: s.3(3), s.3(4), the fee, both values, 4.788%, 5.022%, 20%', all(x in s1 for x in e0['steps'] + ['4.788%', '5.022%', '20%', 'סעיף 3(3)', 'סעיף 3(4)']), [x for x in e0['steps'] if x not in s1])
            check(tag + ' track 2 (prime) explains why, section 4', 'אין עמלת היוון (צו הבנקאות, סעיף 4)' in page.locator(f'{T} details[data-how="1"]').inner_text())
            check(tag + ' track 3 (variable) counts payments to the change day 7.2028', '7.2028' in page.locator(f'{T} details[data-how="2"]').inner_text())
            page.locator(f'{T} [data-card="0"]').screenshot(path=str(OUT / f'card-steps-{tag}.png'))
            common(page, tag + ' steps open')

            # notice
            press(page, f'{T} button[data-s="notice"][data-v="long"]', 300)
            check(tag + ' notice "10 ימים ומעלה": the 0.1% line says none', page.get_attribute(f'{T} button[data-s="notice"][data-v="long"]', 'aria-pressed') == 'true' and 'ללא: 10 ימים מראש ומעלה' in page.locator(T + ' .mhv > .nli__grid .nli__out').inner_text())
            check(tag + ' the example tag is gone after the first change', page.locator(T + ' .mrx__eg').count() == 0)
            press(page, f'{T} button[data-s="notice"][data-v="short"]', 300)
            check(tag + ' notice back to under 10 days', page.get_attribute(f'{T} button[data-s="notice"][data-v="short"]', 'aria-pressed') == 'true' and 'ללא: 10 ימים מראש ומעלה' not in page.locator(T + ' .mhv > .nli__grid .nli__out').inner_text())

            # track change and change cycle
            page.select_option(f'{T} select[data-f="k"][data-i="2"]', 'var_nl_other'); page.wait_for_timeout(300)
            check(tag + ' track 3 to "משתנה לא צמודה": the change-cycle select appears', page.locator(f'{T} select[data-f="freq"][data-i="2"]').count() == 1)
            page.select_option(f'{T} select[data-f="freq"][data-i="2"]', '30'); page.wait_for_timeout(350)
            e = page.evaluate(JS_EXP, {'rows': ex_rows(r2={'k': 'var_nl_other', 'freq': 30})})
            check(tag + ' every 2.5 years: total = NLHV (' + e['figure'] + ')', fig(page) == e['figure'], fig(page))
            page.select_option(f'{T} select[data-f="freq"][data-i="2"]', '12'); page.wait_for_timeout(350)
            e = page.evaluate(JS_EXP, {'rows': ex_rows(r2={'k': 'var_nl_other', 'freq': 12})})
            check(tag + ' every year: no fee on track 3, said so; total = NLHV', fig(page) == e['figure'] and 'ללא: הריבית משתנה כל שנה' in page.locator(f'{T} [data-card="2"]').inner_text(), fig(page))
            page.locator(f'{T} [data-card="2"]').screenshot(path=str(OUT / f'card-yearly-{tag}.png'))
            page.select_option(f'{T} select[data-f="k"][data-i="2"]', 'var_cpi'); page.wait_for_timeout(300)
            page.select_option(f'{T} select[data-f="freq"][data-i="2"]', '60'); page.wait_for_timeout(350)
            check(tag + ' back to the example', fig(page) == e0['figure'], fig(page))

            # term unit
            page.select_option(f'{T} select[data-f="unit"][data-i="3"]', 'm'); page.wait_for_timeout(350)
            check(tag + ' term unit to months: 20 years shows 240, same total', page.input_value(f'{T} input[data-f="term"][data-i="3"]') == '240' and fig(page) == e0['figure'], page.input_value(f'{T} input[data-f="term"][data-i="3"]'))
            typ(page, f'{T} input[data-f="term"][data-i="3"]', '239')
            e = page.evaluate(JS_EXP, {'rows': ex_rows(r3={'n': 239})})
            check(tag + ' 239 months: total = NLHV (' + e['figure'] + ')', fig(page) == e['figure'], fig(page))
            typ(page, f'{T} input[data-f="term"][data-i="3"]', '240')
            page.select_option(f'{T} select[data-f="unit"][data-i="3"]', 'y'); page.wait_for_timeout(350)
            check(tag + ' back to years: 20', page.input_value(f'{T} input[data-f="term"][data-i="3"]') == '20' and fig(page) == e0['figure'])

            # add, fill, add to 6, remove
            press(page, f'{T} button[data-act="add"]', 350)
            check(tag + ' add: 5 rows, the new one asks for its amount, the total unchanged with a note', page.locator(T + ' [data-row]').count() == 5 and 'הקלידו את הסכום' in page.locator(f'{T} [data-row="4"]').inner_text() and fig(page) == e0['figure'] and 'מסלול 5 לא נכלל' in page.locator(T + ' .mhv > .nli__grid .nli__out').inner_text(), fig(page))
            typ(page, f'{T} input[data-f="amount"][data-i="4"]', '200000'); typ(page, f'{T} input[data-f="rate"][data-i="4"]', '4.5')
            e = page.evaluate(JS_EXP, {'rows': EX + [{'k': 'fixed_nl', 'amount': 200000, 'date': '2023-07', 'n': 240, 'rate': 4.5}]})
            check(tag + ' row 5 filled (fixed, 7.2023, 20 years copied, 4.5%): total = NLHV (' + e['figure'] + ')', fig(page) == e['figure'] and page.locator(T + ' [data-card]').count() == 5, fig(page))
            press(page, f'{T} button[data-act="add"]', 350)
            check(tag + ' add again: 6 rows and the add button disabled', page.locator(T + ' [data-row]').count() == 6 and page.locator(f'{T} button[data-act="add"]').is_disabled())
            page.screenshot(path=str(OUT / f'form-six-{tag}.png'), full_page=False)
            press(page, f'{T} button[data-act="del"][data-i="5"]', 350); press(page, f'{T} button[data-act="del"][data-i="4"]', 350)
            check(tag + ' remove twice: 4 rows, the example total', page.locator(T + ' [data-row]').count() == 4 and fig(page) == e0['figure'] and not page.locator(f'{T} button[data-act="add"]').is_disabled(), fig(page))

            # a bad and a future month
            typ(page, f'{T} input[data-f="date"][data-i="0"]', '13.2023')
            e = page.evaluate(JS_EXP, {'rows': EX[1:]})
            check(tag + ' month 13.2023: the message on its field, track 1 left out, total = NLHV without it', 'חודש ושנה' in page.locator(f'{T} [data-row="0"]').inner_text() and fig(page) == e['figure'], fig(page))
            typ(page, f'{T} input[data-f="date"][data-i="0"]', '12.2030')
            check(tag + ' a future month: "החודש צריך להיות לפני"', 'החודש צריך להיות לפני' in page.locator(f'{T} [data-row="0"]').inner_text())
            typ(page, f'{T} input[data-f="date"][data-i="0"]', '7.2023')
            check(tag + ' back to 7.2023', fig(page) == e0['figure'], fig(page))

            # partial prepayment
            check(tag + ' partial 200,000: all to prime, no fee, the drop said', fig(page, PFIG) == e0['pfee'] and e0['drop'] in page.locator(T + ' [data-sec="part"]').inner_text(), fig(page, PFIG))
            typ(page, f'{T} input[data-f="pp"]', '600000')
            e = page.evaluate(JS_EXP, {'rows': EX, 'pp': 600000})
            sp = page.locator(T + ' [data-sec="part"]').inner_text()
            check(tag + ' partial 600,000: fee = NLHV (' + e['pfee'] + '), prime first, the order explained, vs the split by balances', fig(page, PFIG) == e['pfee'] and e['first'] == 1 and 'הסדר: קודם מסלולים שאין בהם עמלת היוון' in sp and 'חלוקה לפי היתרות הייתה עולה' in sp, fig(page, PFIG))
            press(page, f'{T} button[data-s="mode"][data-v="shorten"]', 300)
            sp = page.locator(T + ' [data-sec="part"]').inner_text(); th = page.locator(T + ' [data-sec="part"] thead').text_content()
            check(tag + ' mode "קיצור התקופה": months column, prime closed (260 months)', 'התקופה מתקצרת ב' in th and '260 חודשים' in sp and page.get_attribute(f'{T} button[data-s="mode"][data-v="shorten"]', 'aria-pressed') == 'true', sp[:120])
            page.locator(T + ' [data-sec="part"]').screenshot(path=str(OUT / f'partial-shorten-{tag}.png'))
            press(page, f'{T} button[data-s="mode"][data-v="reduce"]', 300)
            check(tag + ' mode back to "הקטנת ההחזר"', 'ההחזר יורד ב' in page.locator(T + ' [data-sec="part"] thead').text_content() and 'ההחזר החודשי יורד ב' in page.locator(T + ' [data-sec="part"]').inner_text())
            typ(page, f'{T} input[data-f="pp"]', '9000000')
            check(tag + ' more than the balance: capped, said so', 'הסכום גבוה מהיתרה' in page.locator(T + ' [data-sec="part"]').inner_text())
            typ(page, f'{T} input[data-f="pp"]', '600000')
            page.locator(T + ' [data-sec="part"]').screenshot(path=str(OUT / f'partial-{tag}.png'))

            # when to prepay
            sw = page.locator(T + ' [data-sec="when"]')
            kt = sw.locator('.mhv__key').inner_text()
            check(tag + ' the cheapest month named with the saving (' + str(e0['cheapMonth']) + ', ' + str(e0['cheapFee']) + ')', e0['cheap'] and e0['cheapMonth'] in kt and e0['cheapFee'] in kt and e0['save'] in kt, kt)
            nb = sw.locator('svg rect').count()
            check(tag + ' the chart: one bar per month (24 or 25) with the event markers', nb >= 25 and sw.locator('svg circle').count() >= 1, nb)
            check(tag + ' the chart is an image with a text alternative', 'עמלת ההיוון לכל המשכנתא בכל חודש' in (sw.locator('svg').get_attribute('aria-label') or ''))
            evt = sw.locator('ul.mhv__ev').inner_text()
            check(tag + ' the months where something changes: the discount and the change day of 7.2028', '7.2028' in evt and 'הפחתה של 30%' in evt and 'יום שינוי הריבית' in evt, evt[:160])
            press(page, f'{T} details[data-when-table] > summary', 300)
            nr = sw.locator('details[data-when-table] tbody tr').count()
            check(tag + ' the 24-month table opens under the chart: 25 rows (today and 24)', nr == 25, nr)
            sw.screenshot(path=str(OUT / f'when-{tag}.png'))
            common(page, tag + ' when')

            # the bank's number
            typ(page, f'{T} input[data-f="bank"]', '16000')
            sb = page.locator(T + ' [data-sec="bank"]').inner_text()
            check(tag + ' bank 16,000: a gap, no accusation, the usual reasons listed', 'יש פער של' in sb and 'פער לא אומר שמישהו טעה' in sb and page.locator(T + ' [data-sec="bank"] ol.mhv__why li').count() >= 5, sb[:120])
            page.locator(T + ' [data-sec="bank"]').screenshot(path=str(OUT / f'bank-gap-{tag}.png'))
            typ(page, f'{T} input[data-f="bank"]', str(round(e0['fee']) + 100))
            check(tag + ' bank within 2%: close', 'קרוב לחישוב כאן' in page.locator(T + ' [data-sec="bank"]').inner_text())

            # share: copy, WhatsApp, link, print
            page.locator(f'{T} .nli__share button.is-primary').click(); page.wait_for_timeout(400)
            clip = page.evaluate('navigator.clipboard.readText()')
            check(tag + ' copy: the Hebrew summary with the case link', clip.startswith('עמלת היוון למשכנתא') and '#mhivun=' in clip and 'סך הכול' in clip and 'פירעון חלקי' in clip, clip[:120].replace('\n', ' | '))
            with ctx.expect_page() as pi:
                page.locator(f'{T} .nli__share a').click()
            wa = pi.value; wa.wait_for_load_state(); wurl = wa.url; wa.close()
            check(tag + ' WhatsApp: opens wa.me with the summary (answered locally)', wurl.startswith('https://wa.me/?text=') and 'mhivun' in wurl, wurl[:80])
            page.locator(f'{T} .nli__share button', has_text='קישור למקרה הזה').click(); page.wait_for_timeout(400)
            url = page.evaluate('navigator.clipboard.readText()')
            check(tag + ' case link copied', url.startswith(BASE) and '#mhivun=' in url, url[-40:])
            page.evaluate('() => { window.__printed = 0; window.print = () => { window.__printed++; }; }')
            page.locator(f'{T} .nli__share button', has_text='הדפסה').click(); page.wait_for_timeout(200)
            check(tag + ' print pressed', page.evaluate('window.__printed') == 1)
            check(tag + ' no dialog fell back to a prompt', not dialogs, dialogs[:2])
            common(page, tag + ' after every control')
            page.screenshot(path=str(OUT / f'page-after-{tag}.png'), full_page=True)

            # the case link reopens the same case
            p2 = ctx.new_page(); p2.on('pageerror', lambda e, errs=errs: errs.append('pageerror (link): ' + str(e)))
            p2.goto(url, wait_until='networkidle'); p2.wait_for_selector(T + ' [data-card]')
            check(tag + ' the link reopens the case: same total, partial 600,000, bank number, no example tag', fig(p2) == e0['figure'] and p2.input_value(f'{T} input[data-f="pp"]') == '600,000' and p2.input_value(f'{T} input[data-f="bank"]') != '' and p2.locator(T + ' .mrx__eg').count() == 0, [fig(p2), p2.input_value(f'{T} input[data-f="pp"]')])
            p2.close()
            check(tag + ' no console error or warning, no page error', not errs, errs[:5])
            ctx.close()

        # one phone pass under the live theme stylesheets (read only)
        print('\n390 + live theme')
        ctx = br.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=2, locale='he-IL')
        page = ctx.new_page(); errs = []
        page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
        page.on('console', lambda m, errs=errs: errs.append(m.text + ' @ ' + str((m.location or {}).get('url', ''))) if m.type == 'error' and 'nad-lan.co.il' not in m.text + str((m.location or {}).get('url', '')) else None)
        page.goto(BASE + '?theme=1', wait_until='networkidle')
        page.wait_for_selector(T + ' [data-card]')
        e0 = page.evaluate(JS_EXP, {'rows': EX})
        check('theme 390 opens on the example total (' + e0['figure'] + ')', fig(page) == e0['figure'], fig(page))
        press(page, f'{T} details[data-how="0"] > summary')
        common(page, 'theme 390')
        ff = page.evaluate('(t) => [getComputedStyle(document.querySelector(t + " h3.mhv__ch")).fontFamily.split(",")[0], getComputedStyle(document.querySelector(t + " ol.mhv__steps")).listStyleType, getComputedStyle(document.querySelector(t + " h3.mrx__h")).color, getComputedStyle(document.querySelector(t + " input[data-f=amount]")).fontFamily.split(",")[0], getComputedStyle(document.querySelector(t + " button[data-s=notice]")).fontFamily.split(",")[0]]', T)
        check('theme 390: card heading face, the steps numbered, section headings in ink, inputs in Plex Mono and buttons in Plex Sans Hebrew against the theme', 'Plex Sans Hebrew' in ff[0] and ff[1] == 'decimal' and ff[2] == 'rgb(18, 32, 42)' and 'Plex Mono' in ff[3] and 'Plex Sans Hebrew' in ff[4], ff)
        page.locator(T + ' [data-card="0"]').screenshot(path=str(OUT / 'card-steps-theme-390.png'))
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
