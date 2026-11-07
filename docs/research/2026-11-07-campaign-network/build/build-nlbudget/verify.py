"""nlbudget build (7.11.2026, HAD-678): press every control of "כמה עולה לשווק את הפרויקט" in preview.html, headless Chrome (Playwright,
channel chrome), in Hebrew and in English, at 390x844 (is_mobile, touch) and 1280x900, plus a pass with the campaign planner on the same page
(?both=1: the plans link scrolls to it) and a Hebrew phone pass under the live theme stylesheets (?theme=1, read only).

Pressed: the units and the price (good, off the range, empty, text), the four stage pills (the lines of the stage and the stage bar
follow), the two seller pills (the commission field appears; empty, off the range, 1.5%), the share abroad field and its slider (typed,
dragged by keyboard, off the range), the months (empty, off the range, 12), leads per deal (empty: no leads; 48; off the range), every
"your price" field of the sheet (typed, wrong, cleared), the anchors panel, the plans link (opens /marketing/ alone; scrolls to the planner
with it), copy (the clipboard read back) and WhatsApp (wa.me answered locally). On every view: no console error or warning, no horizontal
scroll, every visible button, link button, summary, pill, text input at least 44 px high, every input labelled, every group named, no long
dash, no tech word, the survey red on the total only, every source line carries a flag, nothing leaves 127.0.0.1 except Google fonts (and
wa.me, stubbed).

The script starts its own http.server on a free 127.0.0.1 port (the repo root) and stops it in finally. Screenshots go to
build-nlbudget/shots, the report to verify.json; exit 1 on any failed check.
Run:  python docs/research/2026-11-07-campaign-network/build/build-nlbudget/verify.py
"""
import json, sys, pathlib, re, socket, subprocess, time, urllib.request, urllib.parse
from playwright.sync_api import sync_playwright

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
s0 = socket.socket(); s0.bind(('127.0.0.1', 0)); PORT = s0.getsockname()[1]; s0.close()
ORIGIN = f'http://127.0.0.1:{PORT}'
BASE = ORIGIN + '/docs/research/2026-11-07-campaign-network/build/build-nlbudget/preview.html'
OUT = HERE / 'shots'
OUT.mkdir(parents=True, exist_ok=True)
report, fails = [], []

def check(name, cond, got=None):
    report.append({'check': name, 'ok': bool(cond), 'got': got})
    print(('  ok   ' if cond else '  FAIL ') + name + ('' if got is None else '  [' + str(got)[:220] + ']'))
    if not cond: fails.append(name)

T = '#pv-budget .nli-host'
BAN = ['ממשק', 'מערכת', 'פלטפורמ', 'אלגוריתם', 'דמו', 'סימולציה', 'הדגמה', 'מנגנון', 'אינטראקטיבי', 'טכנולוגי', 'דיגיטלי',
       'interface', 'system', 'platform', 'algorithm', 'demo', 'simulation', 'interactive', 'technology']
def R(lo, hi, lg): return f'{lo:,} עד {hi:,} ₪' if lg == 'he' else f'₪{lo:,} to ₪{hi:,}'
L = {
 'he': dict(q='', title='כמה עולה לשווק את הפרויקט', kicker='תקציב שיווק ליזמים', eg='דוגמה', r1_dev='תקציב שיווק ומכירה, כל הפרויקט', r1_co='שיווק ועמלת חברת השיווק, כל הפרויקט',
   sales='מחזור המכירות: 144,000,000 ₪', r3empty='כתבו כמה פניות לעסקה', e_units='כתבו מספר דירות', e_price='כתבו מחיר ממוצע', e_comm='כתבו שיעור עמלה', e_abroad='כתבו אחוז',
   e_months='כתבו מספר חודשים', e_lpd='כתבו מספר פניות', e_own='כתבו סכום בשקלים', nocomm='ועוד העמלה של חברת השיווק', feeNeed='כתבו את שיעור העמלה', year='בשנה, לפי',
   noIl='לא פורסם מחיר ישראלי', included='כלול במנוי נדל״ן', plans='המנויים: שוק אחד 36,000 ₪ לשנה, שלושה שווקים 72,000 ₪ לשנה, פרויקט דגל 144,000 ₪ לשנה', href='/marketing/',
   ln_research='מחקר שוק, אסטרטגיה ותמחור', ln_fee='עמלת חברת השיווק', ln_fee_dev='צוות המכירות שלכם', copied='הועתק', head='תקציב שיווק לפרויקט, לפי נדל״ן',
   split='בישראל 2,304, מחו״ל 576', fix='כתבו מספר דירות ומחיר ממוצע כדי לראות את התקציב.', now='בשלב שלכם', abroadEx='דוגמה מחו״ל', honest='כל טווח מגיע עם המקור שלו ותאריך', title_font='Karantina', sans='IBM Plex Sans Hebrew'),
 'en': dict(q='?lang=en', title='What it costs to market your project', kicker='Marketing budget for developers', eg='Example', r1_dev='Marketing and sales budget, whole project', r1_co="Marketing and the marketing company's commission, whole project",
   sales='Sales value: ₪144,000,000', r3empty='Enter leads per deal', e_units='Enter a number of apartments', e_price='Enter an average price', e_comm='Enter a commission rate', e_abroad='Enter a share',
   e_months='Enter a number of months', e_lpd='Enter a number of leads', e_own='Enter an amount in shekels', nocomm="Plus the marketing company's commission", feeNeed='Enter the commission rate', year='A year, over',
   noIl='No Israeli price published', included='Included in the NadLan plan', plans='The plans: One market ₪36,000 a year, Three markets ₪72,000 a year, Flagship ₪144,000 a year', href='/en/marketing/',
   ln_research='Market research, strategy and pricing', ln_fee='Marketing company commission', ln_fee_dev='Your sales team', copied='Copied', head='Project marketing budget, by NadLan',
   split='In Israel 2,304, abroad 576', fix='Enter the apartments and the average price to see the budget.', now='Your stage', abroadEx='Example abroad', honest='Every range comes with its source and date', title_font='IBM Plex Sans Condensed', sans='IBM Plex Sans'),
}

JS_HSCROLL = '() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth})'
JS_SMALL = '''(t) => { const out = []; const sel = ['button', 'a[data-act]', '.nli__share a', 'summary', 'label.nlbg__pill', '.nlbg__own',
  'input:not([type=checkbox]):not([type=radio]):not([type=range])', 'input[type=range]'].map(s => t + ' ' + s).join(',');
  document.querySelectorAll(sel).forEach(e => { const b = e.getBoundingClientRect(); if (b.width > 0 && b.height > 0 && getComputedStyle(e).visibility !== 'hidden' && b.height < 43.5)
    out.push(e.tagName + '[' + (e.getAttribute('data-act') || e.getAttribute('data-f') || e.getAttribute('data-own') || e.textContent.trim().slice(0, 18)) + '] ' + b.height.toFixed(1)); }); return out; }'''
JS_LABELS = '''(t) => [...document.querySelectorAll(t + ' input, ' + t + ' select')].filter(e => e.getClientRects().length).map(e => ({id: e.getAttribute('data-f') || e.getAttribute('data-own') || e.type,
  label: (e.labels && e.labels.length ? e.labels[0].textContent : (e.getAttribute('aria-label') || '')).trim()})).filter(x => !x.label).map(x => x.id)'''
JS_GROUPS = '''(t) => [...document.querySelectorAll(t + ' [role="group"], ' + t + ' fieldset')].filter(g => g.getClientRects().length).map(g => g.tagName === 'FIELDSET'
  ? ((g.querySelector(':scope > legend') || {}).textContent || '').trim() : (g.getAttribute('aria-label') || '').trim())'''
JS_SURVEY = '''(t) => { const out = []; document.querySelectorAll(t + ' *').forEach(e => { if (!e.getClientRects().length) return; const c = getComputedStyle(e);
  if ([c.color, c.backgroundColor, c.borderTopColor, c.borderBottomColor, c.borderInlineStartColor].some(v => v === 'rgb(196, 37, 80)')) out.push(e.getAttribute('data-o') || e.tagName); }); return out; }'''
JS_FLAGS = '''(t) => [...document.querySelectorAll(t + ' .nlbg__src')].filter(e => e.getClientRects().length).filter(e => !e.querySelector('.nlbg__flag')).length'''
JS_ROWSRC = '''(t) => [...document.querySelectorAll(t + ' tr[data-ln]')].filter(r => !r.querySelector('td[data-o="s"] .nlbg__flag')).map(r => r.getAttribute('data-ln'))'''

def tool_text(page): return page.locator(T).inner_text()
def txt(page, sel): return page.locator(T + ' ' + sel).first.inner_text().strip()
def total(page): return txt(page, 'output[data-o="total"]')
def msgs(page): return ' | '.join(x for x in page.locator(T + ' .nlbg__msg').all_inner_texts() if x.strip())
def put(page, f, v, wait=100):
    loc = page.locator(f'{T} input[data-f="{f}"]').first; loc.click(); loc.fill(v); page.wait_for_timeout(wait)
def own(page, k, v, wait=100):
    loc = page.locator(f'{T} input[data-own="{k}"]').first; loc.click(); loc.fill(v); page.wait_for_timeout(wait)
def pill(page, name, v): page.locator(f'{T} label.nlbg__pill:has(input[data-f="{name}"][value="{v}"])').click(); page.wait_for_timeout(100)
def invalid(page, f): return page.get_attribute(f'{T} input[data-f="{f}"]', 'aria-invalid') == 'true'
def now_rows(page): return page.evaluate("(t) => [...document.querySelectorAll(t + ' tr[data-ln].is-now')].map(r => r.getAttribute('data-ln'))", T)
def sum_text(page): return txt(page, '[data-o="sum"]')

def common(page, tag, lg):
    hs = page.evaluate(JS_HSCROLL)
    check(tag + ' no horizontal scroll', hs['sw'] <= hs['iw'] + 1, hs)
    small = page.evaluate(JS_SMALL, T)
    check(tag + ' every visible control at least 44 px high', not small, small[:6])
    nolab = page.evaluate(JS_LABELS, T)
    check(tag + ' every input labelled', not nolab, nolab)
    groups = page.evaluate(JS_GROUPS, T)
    check(tag + ' every visible group named', all(groups), groups[:6])
    tx = tool_text(page)
    hit = [w for w in BAN if w in tx.lower()]
    check(tag + ' no long dash, no tech word', not re.search('[–—]', tx) and not hit and not re.search(r'\bAI\b', tx), hit)
    sv = page.evaluate(JS_SURVEY, T)
    check(tag + ' survey red only on the total', sv == ['total'], sv)
    nf = page.evaluate(JS_FLAGS, T)
    check(tag + ' every visible source line carries its flag', nf == 0, nf)

def shot(page, name, sel=None, full=False):
    if full: page.screenshot(path=str(OUT / f'{name}.png'), full_page=True)
    else: page.locator(sel or '#pv-budget').first.screenshot(path=str(OUT / f'{name}.png'))

def watch(page, errs, ext):
    page.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
    page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    page.on('request', lambda r: ext.append(r.url) if not r.url.startswith(ORIGIN) and not re.match(r'https://fonts\.(googleapis|gstatic)\.com/', r.url) and not r.url.startswith('https://wa.me/') and not r.url.startswith('data:') else None)

def run(ctx, lg, W, mob):
    x = L[lg]; tag = f'{lg} {W}'; errs = []; ext = []
    page = ctx.new_page(); watch(page, errs, ext)
    page.goto(BASE + x['q'], wait_until='networkidle')
    page.wait_for_selector(T + ' .nlbg')

    print(f'\n{tag}: the example')
    check(tag + ' the shortcode summary is replaced by the tool; kicker and title', page.locator(T + ' .nlbg').count() == 1 and txt(page, 'h2.nli__title') == x['title'] and txt(page, '.nli__kicker') == x['kicker'])
    ff = page.evaluate('(t) => { const q = s => getComputedStyle(document.querySelector(t + " " + s)); return [q("h2.nli__title").fontFamily, parseFloat(q("h2.nli__title").fontSize), q("label.nlbg__pill").fontFamily, q("output[data-o=total] bdi").fontFamily, document.querySelector(t + " .nlbg").dir, document.querySelector(t + " .nlbg").lang]; }', T)
    check(tag + ' faces: the title in ' + x['title_font'] + ', pills in ' + x['sans'] + ', figures in IBM Plex Mono; dir and lang', x['title_font'] in ff[0] and (ff[1] >= 32 if lg == 'he' else True)
          and ff[2].split(',')[0].strip('"') == x['sans'] and 'IBM Plex Mono' in ff[3] and ff[4] == ('rtl' if lg == 'he' else 'ltr') and ff[5] == lg, ff)
    lay = page.evaluate('(t) => { const a = document.querySelector(t + " form.nlbg__in").getBoundingClientRect(), b = document.querySelector(t + " .nlbg__out").getBoundingClientRect(); return [Math.round(a.left), Math.round(b.left), Math.round(a.top), Math.round(b.top)]; }', T)
    if W >= 960: check(tag + ' the inputs panel ' + ('on the right' if lg == 'he' else 'on the left') + ', beside the readouts', (lay[0] > lay[1] if lg == 'he' else lay[0] < lay[1]) and abs(lay[2] - lay[3]) < 4, lay)
    else: check(tag + ' phone: the inputs first, the readouts below', lay[3] > lay[2] + 200, lay)
    check(tag + ' opens on the example (tag "' + x['eg'] + '"), sales value, total ' + R(2880000, 5760000, lg), page.locator(T + ' [data-o="eg"]').is_visible() and x['sales'] in txt(page, '[data-o="sales"]') and total(page) == R(2880000, 5760000, lg), [total(page)])
    r1 = txt(page, '[data-o="r1"]')
    check(tag + ' readout 1: "' + x['r1_dev'] + '", both bounds named (Start Point), the year line, marketing alone', r1.startswith(x['r1_dev']) and txt(page, '[data-o="low"]').startswith('2%') and txt(page, '[data-o="high"]').startswith('4%')
          and ('סטארט פוינט' if lg == 'he' else 'Start Point') in txt(page, '[data-o="low"]') and x['year'] in r1 and ('1,440,000' in txt(page, '[data-o="mkt"]')), r1[:160])
    check(tag + ' readout 2: 3,000 to 23,000 per apartment, 180,000 to 1,380,000 for 60', txt(page, 'output[data-o="unit"]') == R(3000, 23000, lg) and R(180000, 1380000, lg) in txt(page, '[data-o="unitAll"]'))
    check(tag + ' readout 3: asks for the close rate, no number; the leads table hidden', txt(page, 'output[data-o="leadsN"]') == x['r3empty'] and page.locator(T + ' [data-o="leads"]').is_hidden())
    check(tag + ' the honesty line', x['honest'] in txt(page, '.nlbg__honest'))
    rows = page.locator(T + ' tr[data-ln]').count(); nosrc = page.evaluate(JS_ROWSRC, T)
    check(tag + ' the sheet: 17 lines, each with a source and a flag', rows == 17 and not nosrc, [rows, nosrc])
    rr = page.evaluate("(t) => Object.fromEntries([...document.querySelectorAll(t + ' tr[data-ln]')].map(r => [r.getAttribute('data-ln'), r.querySelector('[data-o=\"v\"]').innerText.trim()]))", T)
    check(tag + ' renders 4,000 to 6,000; sales plans 60,000 to 90,000; film 12,000 to 30,000; media about 1,080,000', rr['ext3'] == R(4000, 6000, lg) and rr['plan3d'].startswith(R(60000, 90000, lg))
          and rr['film'] == R(12000, 30000, lg) and '1,080,000' in rr['media'], [rr['ext3'], rr['plan3d'][:40], rr['media'][:30]])
    nos = [k for k in ('research', 'brand', 'photo', 'site', 'crm', 'outdoor', 'print', 'tv', 'pr', 'events', 'office', 'fee') if not rr[k].startswith(x['noIl'])]
    check(tag + ' "' + x['noIl'] + '" on the 11 unpriced lines and the sales team, each with its own field', not nos and page.locator(T + ' .nlbg__own:visible').count() == 12, nos)
    pl = page.locator(T + ' a[data-act="plans"]')
    check(tag + ' the tour line: "' + x['included'] + '" and the plans link (36,000 / 72,000 / 144,000 a year) to ' + x['href'], rr['tour'].startswith(x['included']) and pl.inner_text().strip() == x['plans'] and pl.get_attribute('href') == x['href'], pl.inner_text().strip())
    check(tag + ' the sheet total 1,156,000 to 1,206,000', sum_text(page) == R(1156000, 1206000, lg), sum_text(page))
    bars = page.evaluate("(t) => [...document.querySelectorAll(t + ' .nlbg__col')].map(c => [c.getAttribute('data-b'), c.classList.contains('is-now'), c.innerText.trim(), Math.round(c.querySelector('b').getBoundingClientRect().height)])", T)
    check(tag + ' the spread: 74% / 26% / +22%, the pre-launch bar marked, heights in proportion; labelled "' + x['abroadEx'] + '"', [b[2] for b in bars] == ['74%', '26%', '+22%'] and bars[0][1] and not bars[1][1]
          and bars[0][3] > bars[1][3] > bars[2][3] > 0 and x['abroadEx'] in txt(page, '.nlbg__bh'), bars)
    strip = txt(page, '.nlbg__strip')
    check(tag + ' the ad-spend line: five companies, sourced, list price', len(re.findall(r'(מיליון|million)', strip)) == 5 and ('גלובס' in strip or 'Globes' in strip) and ('במחירון' in strip or 'list price' in strip), strip[:120])
    common(page, tag + ' example', lg)
    shot(page, f'{lg}-{W}-example'); shot(page, f'{lg}-{W}-page', full=True)

    print(f'\n{tag}: units and price')
    put(page, 'units', '120')
    check(tag + ' 120 units: total ' + R(5760000, 11600000, lg) + ' (11,520,000 rounded outward to three figures), the example tag gone', total(page) == R(5760000, 11600000, lg) and page.locator(T + ' [data-o="eg"]').is_hidden(), total(page))
    put(page, 'units', '0')
    check(tag + ' 0 units: the message, the field marked, the readouts ask for the numbers', invalid(page, 'units') and x['e_units'] in msgs(page) and total(page) == x['fix'], [msgs(page), total(page)])
    put(page, 'units', '')
    check(tag + ' empty units: still the message', invalid(page, 'units') and x['e_units'] in msgs(page))
    put(page, 'units', '60'); put(page, 'price', '3,400,000')
    check(tag + ' price 3,400,000: total ' + R(4080000, 8160000, lg) + ', the field unmarked', total(page) == R(4080000, 8160000, lg) and not invalid(page, 'units') and not invalid(page, 'price'), total(page))
    put(page, 'price', 'abc')
    check(tag + ' price "abc": the message', invalid(page, 'price') and x['e_price'] in msgs(page))
    put(page, 'price', '2400000'); page.locator(f'{T} input[data-f="units"]').click(); page.wait_for_timeout(80)
    check(tag + ' back to the example; the price is grouped on leaving the field', total(page) == R(2880000, 5760000, lg) and page.input_value(f'{T} input[data-f="price"]') == '2,400,000' and page.locator(T + ' [data-o="eg"]').is_visible())

    print(f'\n{tag}: stage')
    want = {'pre': ['research', 'brand', 'ext3', 'plan3d', 'tour', 'site', 'outdoor'], 'launch': ['film', 'outdoor', 'print', 'tv', 'events', 'office'], 'build': ['photo', 'events', 'office'], 'last': []}
    for sg in ('launch', 'build', 'last', 'pre'):
        pill(page, 'stage', sg)
        nb = page.evaluate("(t) => [...document.querySelectorAll(t + ' .nlbg__col.is-now')].map(c => c.getAttribute('data-b'))", T)
        check(tag + f' stage {sg}: its lines marked "{x["now"]}" ({len(want[sg])}), the stage bar follows', now_rows(page) == want[sg] and nb == (['pre'] if sg == 'pre' else ['post'])
              and page.locator(f'{T} tr.is-now .nlbg__tag').count() == len(want[sg]), [now_rows(page), nb])
        if sg == 'launch': shot(page, f'{lg}-{W}-stage-launch', T + ' .nlbg__wide')

    print(f'\n{tag}: who sells')
    pill(page, 'seller', 'co')
    cw = page.locator(f'{T} input[data-f="comm"]')
    check(tag + ' marketing company: the commission field appears empty (no default); ' + R(1440000, 2880000, lg) + ' marketing alone, the commission asked for', cw.is_visible() and cw.input_value() == ''
          and txt(page, '[data-o="r1"]').startswith(x['r1_co']) and total(page) == R(1440000, 2880000, lg) and x['nocomm'] in txt(page, '[data-o="nocomm"]'), total(page))
    fee = page.locator(f'{T} tr[data-ln="fee"]')
    check(tag + ' the fee line: "' + x['ln_fee'] + '", asks for the rate, no own field', fee.locator('[data-o="n"]').inner_text().strip() == x['ln_fee'] and x['feeNeed'] in fee.inner_text() and fee.locator('.nlbg__own').is_hidden())
    check(tag + ' bounds: WE DO MEDIA 1% and Feasly 2%', txt(page, '[data-o="low"]').startswith('1%') and 'WE DO MEDIA' in txt(page, '[data-o="low"]') and txt(page, '[data-o="high"]').startswith('2%') and 'Feasly' in txt(page, '[data-o="high"]'))
    common(page, tag + ' company', lg)
    shot(page, f'{lg}-{W}-company')
    put(page, 'comm', '20')
    check(tag + ' commission 20%: the message', invalid(page, 'comm') and x['e_comm'] in msgs(page))
    put(page, 'comm', '1.5')
    check(tag + ' commission 1.5%: ' + R(3600000, 5040000, lg) + ', the fee line 2,160,000', total(page) == R(3600000, 5040000, lg) and '2,160,000' in fee.inner_text() and page.locator(T + ' [data-o="nocomm"]').count() == 0, total(page))
    pill(page, 'seller', 'dev')
    check(tag + ' back to the developer\'s team: the field hidden, the total back, the line "' + x['ln_fee_dev'] + '" with its own field', cw.is_hidden() and total(page) == R(2880000, 5760000, lg)
          and fee.locator('[data-o="n"]').inner_text().strip() == x['ln_fee_dev'] and fee.locator('.nlbg__own').is_visible())

    print(f'\n{tag}: abroad, months, leads')
    put(page, 'abroad', '20')
    rng = page.locator(f'{T} input.nlbg__range')
    check(tag + ' share abroad 20: the slider follows', rng.input_value() == '20')
    rng.focus(); page.keyboard.press('ArrowUp'); page.wait_for_timeout(100)  # ArrowUp raises the value in both directions (ArrowRight lowers it in RTL)
    check(tag + ' the slider by keyboard: 25, the field follows', page.input_value(f'{T} input[data-f="abroad"]') == '25', page.input_value(f'{T} input[data-f="abroad"]'))
    put(page, 'abroad', '101')
    check(tag + ' share 101: the message', invalid(page, 'abroad') and x['e_abroad'] in msgs(page))
    put(page, 'abroad', '20')
    put(page, 'months', '12')
    check(tag + ' 12 months: a year ' + R(2880000, 5760000, lg), R(2880000, 5760000, lg) in txt(page, '[data-o="year"]'))
    put(page, 'months', '')
    check(tag + ' months empty: no year line, no error', page.locator(T + ' [data-o="year"]').count() == 0 and not invalid(page, 'months'))
    put(page, 'months', '0')
    check(tag + ' months 0: the message', invalid(page, 'months') and x['e_months'] in msgs(page))
    put(page, 'months', '24')
    put(page, 'lpd', '48')
    lt = page.locator(T + ' [data-o="leads"]')
    costs = page.evaluate("(t) => [...document.querySelectorAll(t + ' [data-o=\"leads\"] tr[data-k]')].map(r => r.querySelector('[data-o=\"cost\"]').innerText.trim())", T)
    want_c = [R(294000, 399000, lg), R(691000, 1850000, lg), ('$59,000 עד $82,200' if lg == 'he' else '$59,000 to $82,200')]
    check(tag + ' 48 leads per deal: 2,880 leads, ' + x['split'] + '; the cost at three labelled bases', txt(page, 'output[data-o="leadsN"]') == '2,880' and x['split'] in txt(page, '[data-o="split"]') and lt.is_visible() and costs == want_c, costs)
    common(page, tag + ' leads', lg)
    shot(page, f'{lg}-{W}-leads', T + ' .nlbg__out')
    put(page, 'lpd', '0')
    check(tag + ' 0 leads per deal: the message, the leads gone', invalid(page, 'lpd') and x['e_lpd'] in msgs(page) and lt.is_hidden())
    put(page, 'lpd', '48')

    print(f'\n{tag}: your own prices')
    owns = page.evaluate("(t) => [...document.querySelectorAll(t + ' input[data-own]')].filter(e => e.getClientRects().length).map(e => e.getAttribute('data-own'))", T)
    okc = 0
    for k in owns:
        own(page, k, '1000')
        if sum_text(page) == R(1157000, 1207000, lg): okc += 1
        own(page, k, '')
    check(tag + f' every "your price" field ({len(owns)}) joins the total when typed and leaves it when cleared', len(owns) == 12 and okc == 12 and sum_text(page) == R(1156000, 1206000, lg), [len(owns), okc])
    own(page, 'research', '50000'); own(page, 'office', '400000')
    check(tag + ' research 50,000 and sales office 400,000: total ' + R(1606000, 1656000, lg) + ', 10 lines left', sum_text(page) == R(1606000, 1656000, lg) and '10' in txt(page, '[data-o="open"]'), sum_text(page))
    own(page, 'print', 'abc')
    check(tag + ' a wrong own price: its message, the field marked', x['e_own'] in msgs(page) and page.get_attribute(f'{T} input[data-own="print"]', 'aria-invalid') == 'true')
    own(page, 'print', '')
    shot(page, f'{lg}-{W}-sheet', T + ' .nlbg__wide')

    print(f'\n{tag}: anchors, share')
    page.locator(f'{T} details.nlbg__anch > summary').click(); page.wait_for_timeout(120)
    an = page.evaluate("(t) => [...document.querySelectorAll(t + ' [data-o=\"anch\"] tr[data-a]')].map(r => [r.getAttribute('data-a'), !!r.querySelector('.nlbg__flag')])", T)
    check(tag + ' the anchors panel opens: 7 anchors on the project, each flagged', len(an) == 7 and all(a[1] for a in an) and page.locator(f'{T} details.nlbg__anch').get_attribute('open') is not None, an)
    common(page, tag + ' anchors', lg)
    shot(page, f'{lg}-{W}-anchors', f'{T} details.nlbg__anch')
    page.locator(f'{T} button[data-act="copy"]').click(); page.wait_for_timeout(250)
    clip = page.evaluate('navigator.clipboard.readText()').replace(chr(13) + chr(10), chr(10))  # the Windows clipboard stores CRLF
    check(tag + ' copy: the button says "' + x['copied'] + '"; the text holds the heading, the total, the leads, my own prices, the page address', x['copied'] in txt(page, 'button[data-act="copy"]') and clip.split('\n')[0] == x['head']
          and R(2880000, 5760000, lg) in clip and '2,880' in clip and ('50,000 ₪' if lg == 'he' else '₪50,000') in clip and clip.rstrip().endswith('preview.html') and '<' not in clip, clip[:200])
    wa = page.locator(f'{T} a[data-act="wa"]')
    with ctx.expect_page() as pop:
        wa.click()
    p2 = pop.value; p2.wait_for_load_state(); wurl = p2.url; p2.close()
    wtxt = urllib.parse.unquote(wurl.split('text=', 1)[1]) if 'text=' in wurl else ''
    check(tag + ' WhatsApp: wa.me with the same text only', wurl.startswith('https://wa.me/?text=') and wtxt == clip, wurl[:80])
    pl.click(); page.wait_for_load_state(); page.wait_for_timeout(150)
    check(tag + ' the plans link alone opens ' + x['href'] + ' (stubbed here)', page.url == ORIGIN + x['href'], page.url)
    check(tag + ' no console error or warning, no page error', not errs, errs[:5])
    check(tag + ' nothing left 127.0.0.1 except Google fonts and wa.me', not ext, ext[:5])
    page.close()

server = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(REPO)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(80):
        try: urllib.request.urlopen(BASE, timeout=1); break
        except Exception: time.sleep(0.25)
    with sync_playwright() as p:
        br = p.chromium.launch(channel='chrome', headless=True)
        def context(W, H, mob, lg):
            ctx = br.new_context(viewport={'width': W, 'height': H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, locale='he-IL' if lg == 'he' else 'en-GB')
            ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin=ORIGIN)
            ctx.route('https://wa.me/**', lambda route: route.fulfill(status=200, content_type='text/plain', body='local stub'))
            ctx.route('**/marketing/', lambda route: route.fulfill(status=200, content_type='text/html', body='<!doctype html><title>local stub</title>'))
            ctx.route('https://nad-lan.co.il/**', lambda route: route.abort())  # nothing goes to the live site from these runs
            return ctx
        for lg in ('he', 'en'):
            for W, H, mob in ((390, 844, True), (1280, 900, False)):
                ctx = context(W, H, mob, lg); run(ctx, lg, W, mob); ctx.close()

        # with the campaign planner on the same page (the hub): the plans link scrolls to it
        for lg in ('he', 'en'):
            print(f'\n{lg} 1280 + the planner on the page')
            ctx = context(1280, 900, False, lg); page = ctx.new_page(); errs, ext = [], []; watch(page, errs, ext)
            page.goto(BASE + L[lg]['q'] + ('&' if L[lg]['q'] else '?') + 'both=1', wait_until='networkidle'); page.wait_for_selector(T + ' .nlbg'); page.wait_for_selector('#pv-camp .nlcp')
            u0 = page.url; y0 = page.evaluate('window.scrollY'); page.locator(f'{T} a[data-act="plans"]').click(); page.wait_for_timeout(400)
            top, y1, ih = page.evaluate("() => [Math.round(document.querySelector('#pv-camp [data-nli=\"nlcamp\"]').getBoundingClientRect().top), window.scrollY, innerHeight]")
            check(f'{lg} both: the plans link scrolls to the planner on the same page (the address unchanged, the planner in the upper part of the screen)', page.url == u0 and y1 > y0 + 500 and -5 <= top <= ih * 0.4, [y0, y1, top])
            page.screenshot(path=str(OUT / f'{lg}-1280-both-plans.png'))
            check(f'{lg} both: no console error, nothing outside', not errs and not ext, (errs + ext)[:4])
            ctx.close()

        # one phone pass under the live theme stylesheets (read only)
        print('\nhe 390 + live theme')
        ctx = br.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=2, locale='he-IL')
        page = ctx.new_page(); errs = []
        page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        page.on('console', lambda m: errs.append(m.text + ' @ ' + str((m.location or {}).get('url', ''))) if m.type == 'error' and 'nad-lan.co.il' not in m.text + str((m.location or {}).get('url', '')) else None)
        page.goto(BASE + '?theme=1', wait_until='networkidle'); page.wait_for_selector(T + ' .nlbg')
        put(page, 'lpd', '48'); put(page, 'abroad', '20')
        common(page, 'theme 390', 'he')
        ff = page.evaluate('''(t) => { const q = s => getComputedStyle(document.querySelector(t + ' ' + s)); return [q('label.nlbg__pill').fontFamily.split(',')[0], q('label.nlbg__pill:has(input:checked)').backgroundColor, q('label.nlbg__pill').borderRadius,
          q('h2.nli__title').color, q('input[data-f="units"]').fontFamily.split(',')[0], q('table.is-sheet tbody tr').display, q('table.is-sheet thead').display, q('output[data-o="total"]').borderBottomColor]; }''', T)
        check('theme 390: pills in Plex Sans Hebrew, the pressed pill in sea, round; the title in ink; fields in Plex Mono; the sheet stacked (no header row); the total underlined survey red',
              'Plex Sans Hebrew' in ff[0] and ff[1] == 'rgb(47, 111, 134)' and ff[2] in ('999px', '9.99e+02px') and ff[3] == 'rgb(18, 32, 42)' and 'Plex Mono' in ff[4] and ff[5] == 'block' and ff[6] == 'none' and ff[7] == 'rgb(196, 37, 80)', ff)
        shot(page, 'theme-he-390-top'); page.screenshot(path=str(OUT / 'theme-he-390-page.png'), full_page=True)
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
