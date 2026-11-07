"""nlcamp build (7.11.2026): press every control of the international campaign planner in preview.html, headless Chrome (Playwright,
channel chrome), in Hebrew and in English, at 390x844 (is_mobile, touch) and 1280x900, plus one Hebrew phone pass under the live theme
stylesheets (?theme=1, read only).

The brief POST is answered by a local route (nothing reaches the site): first a server error (the planner must keep the form and say
so), then 201 with a reference. Pressed: every market chip on and off, Next with nothing chosen (the message, no move), the buyer cards,
the budget -/+ (to both ends, disabled there), a typed budget off the range, the slider, the split panel (+5 to 105%, the message, -5,
reset), Enter in the budget field, the project cards (the field label follows the kind, the text kept), the plan cards (a plan too small
for the markets: the message), every contact field (empty, a bad email, the consent box), the "שינוי" link back to step 1 and forward
again, copy (the clipboard read back), WhatsApp (wa.me answered locally), send (fail, then saved), the payment step without and with a
product link. On every step: no console error or warning, no horizontal scroll, every visible button, link button, summary, text input
and card at least 44 px high, every input labelled, every group named, no long dash, no tech word, no VAT wording, the survey red on the
yearly total only, focus on the step heading after a move. No request leaves 127.0.0.1 except the Google fonts (and wa.me, stubbed).

The script starts its own http.server on a free 127.0.0.1 port (the repo root) and stops it in finally. Screenshots go to
build-nlcamp/shots, the report to verify.json; exit 1 on any failed check.
Run:  python docs/research/2026-11-07-campaign-network/build/build-nlcamp/verify.py
"""
import json, sys, pathlib, re, socket, subprocess, time, urllib.request, urllib.parse
from playwright.sync_api import sync_playwright

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
s0 = socket.socket(); s0.bind(('127.0.0.1', 0)); PORT = s0.getsockname()[1]; s0.close()
ORIGIN = f'http://127.0.0.1:{PORT}'
BASE = ORIGIN + '/docs/research/2026-11-07-campaign-network/build/build-nlcamp/preview.html'
OUT = HERE / 'shots'
OUT.mkdir(parents=True, exist_ok=True)
report, fails = [], []
REF = 'NLC-261107-T3ST'

def check(name, cond, got=None):
    report.append({'check': name, 'ok': bool(cond), 'got': got})
    print(('  ok   ' if cond else '  FAIL ') + name + ('' if got is None else '  [' + str(got)[:200] + ']'))
    if not cond: fails.append(name)

T = '#pv-camp .nli-host'
BAN = ['ממשק', 'מערכת', 'פלטפורמ', 'אלגוריתם', 'דמו', 'סימולציה', 'הדגמה', 'מנגנון', 'אינטראקטיבי', 'טכנולוגי',
       'interface', 'system', 'platform', 'algorithm', 'demo', 'simulation', 'interactive', 'technology']
L = {
 'he': dict(q='', title='מתכנן הקמפיין', names=['שווקים וקהילות', 'הקונים שאתם מחפשים', 'תקציב פרסום חודשי', 'הפרויקט', 'סיכום ותוכנית'],
   next='המשיכו', back='חזרה', send='שלחו את התוכנית', e_markets='בחרו לפחות שוק או קהילה אחת.', e_buyer='בחרו את הקונים שאתם מחפשים.',
   langs2='אנגלית, צרפתית', langs1='צרפתית', rec2='שלושה שווקים', rec1='שוק אחד', none='עוד לא נבחר',
   aim='הפרסום מכוון לפי מדינה, עיר ושפה, ובעיתונות ובניוזלטרים של הקהילות.', e_budget='בין ₪3,000 ל־₪60,000', e_split='עכשיו: 105%',
   paid='את תקציב הפרסום אתם משלמים ישירות לערוצים עצמם', split_lab='חלוקה מוצעת של התקציב', split_mine='החלוקה שלכם',
   e_kind='בחרו פרויקט חדש או פרויקט שכבר יש לו עמוד.', e_ref='כתבו את כתובת העמוד או את שם הפרויקט.',
   lab_ex='כתובת העמוד או שם הפרויקט', lab_new='שם הפרויקט והעיר (לא חובה)', proj='מגדלי הים, בת ים',
   dl=['צרפת, קנדה', 'אנגלית, צרפתית', 'משקיעים, להשכרה', '₪25,000 בחודש, ₪300,000 בשנה', 'Meta 50%, Google 25%, עיתונות קהילתית 20%, אתרי נדלן 5%', 'פרויקט שכבר יש לו עמוד בנדלן, מגדלי הים, בת ים'],
   tag2='מתאימה ל־2 שווקים שבחרתם', tag3='מתאימה ל־3 שווקים שבחרתם', year='לשנה',
   e_cover='בחרתם 2 שווקים, ובתוכנית "שוק אחד" יש מקום לשוק אחד.', e_name='כתבו שם מלא.', e_email='כתבו כתובת אימייל מלאה.', e_consent='כדי לשלוח, סמנו את האישור.',
   leads='כל פנייה מגיעה אליכם בוואטסאפ, עם מה שהקונה פתח בפרויקט.',
   name='דנה לוי', company='לוי יזמות', phone='050-123 4567', email='dana@example.test',
   clip3='שווקים וקהילות: צרפת, ארצות הברית, קנדה', plan3='התוכנית: שלושה שווקים, ₪72,000 לשנה', e_send='לא הצלחנו לשמור את התוכנית. בדקו את החיבור ונסו שוב.',
   ref_lab='מספר התוכנית שלכם', pay_later='קישור לתשלום יישלח אליכם עוד היום.', launch='הקמפיין יוצא לדרך אחרי התשלום.', t_ref='מספר התוכנית: ' + REF,
   pay_btn='לתשלום: שלושה שווקים, ₪72,000 לשנה', pay_first='לתשלום ראשון: ₪18,000 (שלושה שווקים, ₪72,000 לשנה)',
   pay_rest='את היתרה, ₪54,000, משלמים בתשלומים של עד ₪18,000, בקישורים שנשלחים אליכם.', privacy='מדיניות הפרטיות', title_font='Karantina', sans='IBM Plex Sans Hebrew'),
 'en': dict(q='?lang=en', title='Campaign planner', names=['Markets and communities', 'The buyers you want', 'Monthly ad budget', 'The project', 'Summary and plan'],
   next='Continue', back='Back', send='Send the plan', e_markets='Choose at least one market or community.', e_buyer='Choose the buyers you want.',
   langs2='English, French', langs1='French', rec2='Three markets', rec1='One market', none='Not chosen yet',
   aim='Ads are aimed by country, city and language, plus community press and newsletters.', e_budget='from ₪3,000 to ₪60,000', e_split='Now: 105%',
   paid='You pay the ad budget straight to the channels themselves', split_lab='Suggested budget split', split_mine='Your split',
   e_kind='Choose a new project or a project that already has a page.', e_ref='Write the page address or the project name.',
   lab_ex='The page address or the project name', lab_new='Project name and city (optional)', proj='Sea Towers, Bat Yam',
   dl=['France, Canada', 'English, French', 'Investors (rental)', '₪25,000 a month, ₪300,000 a year', 'Meta 50%, Google 25%, Community press 20%, Property portals 5%', 'A project that already has a page on NadLan, Sea Towers, Bat Yam'],
   tag2='Fits the 2 markets you chose', tag3='Fits the 3 markets you chose', year='a year',
   e_cover='You chose 2 markets, and the "One market" plan has room for 1 market.', e_name='Write your full name.', e_email='Write a full email address.', e_consent='To send, tick the consent box.',
   leads='Every lead reaches you on WhatsApp with what the buyer opened in the project.',
   name='Dana Levi', company='Levi Developments', phone='+44 20 7946 0958', email='dana@example.test',
   clip3='Markets and communities: France, USA, Canada', plan3='The plan: Three markets, ₪72,000 a year', e_send='We could not save the plan. Check your connection and try again.',
   ref_lab='Your plan number', pay_later='A payment link will be sent to you today.', launch='The campaign goes live after payment.', t_ref='Plan number: ' + REF,
   pay_btn='Pay: Three markets, ₪72,000 a year', pay_first='Pay the first part: ₪18,000 (Three markets, ₪72,000 a year)',
   pay_rest='The rest, ₪54,000, is paid in parts of up to ₪18,000 through links we send you.', privacy='Privacy policy', title_font='IBM Plex Sans Condensed', sans='IBM Plex Sans'),
}

JS_HSCROLL = '() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth})'
JS_SMALL = '''(t) => { const out = []; const sel = ['button', 'a[data-act]', 'a.nlcp__pay', '.nli__share a', 'summary', 'select', 'label.nlcp__card', 'label.nlcp__chk',
  'input:not([type=checkbox]):not([type=radio]):not([name=website])'].map(s => t + ' ' + s).join(',');
  document.querySelectorAll(sel).forEach(e => { const b = e.getBoundingClientRect(); if (b.width > 0 && b.height > 0 && getComputedStyle(e).visibility !== 'hidden' && b.height < 43.5)
    out.push(e.tagName + '[' + (e.getAttribute('data-act') || e.getAttribute('data-f') || e.textContent.trim().slice(0, 18)) + '] ' + b.height.toFixed(1)); }); return out; }'''
JS_LABELS = '''(t) => [...document.querySelectorAll(t + ' input, ' + t + ' select')].filter(e => !e.closest('[aria-hidden="true"]')).map(e => ({id: e.getAttribute('data-f') || e.type,
  label: (e.labels && e.labels.length ? e.labels[0].textContent : (e.getAttribute('aria-label') || '')).trim()})).filter(x => !x.label).map(x => x.id)'''
JS_GROUPS = '''(t) => [...document.querySelectorAll(t + ' [role="group"], ' + t + ' fieldset')].filter(g => g.getClientRects().length).map(g => g.tagName === 'FIELDSET'
  ? ((g.querySelector(':scope > legend') || {}).textContent || '').trim() : (g.getAttribute('aria-label') || '').trim())'''
JS_SURVEY = '''(t) => { const out = []; document.querySelectorAll(t + ' *').forEach(e => { if (!e.getClientRects().length) return; const c = getComputedStyle(e);
  if ([c.color, c.backgroundColor, c.borderTopColor, c.borderInlineStartColor].some(v => v === 'rgb(196, 37, 80)')) out.push((e.getAttribute('data-o') || e.tagName) + (e.closest('[data-o="y"]') ? ':y' : '')); }); return out; }'''

def tool_text(page): return page.locator(T).inner_text()
def msgs(page): return ' | '.join(x for x in page.locator(T + ' .nlcp__msg').all_inner_texts() if x.strip())
def count(page): return page.locator(T + ' .nlcp__count').inner_text().strip()
def head(page): return page.locator(T + ' h3.nlcp__h').inner_text().strip()
def press(page, sel, wait=80): page.locator(sel).first.click(); page.wait_for_timeout(wait)
def nxt(page, wait=120): press(page, T + ' button[data-act="next"]', wait)
def typ(page, sel, text):
    loc = page.locator(sel).first; loc.click(); loc.press('Control+A'); loc.press('Backspace')
    if text: page.keyboard.type(text)
    page.wait_for_timeout(80)
def card(page, v): press(page, f'{T} label.nlcp__card:has(input[value="{v}"])')
def focus_on_head(page): return page.evaluate("(t) => document.activeElement === document.querySelector(t + ' h3.nlcp__h')", T)

def common(page, tag, lg, step=True):
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
    check(tag + ' no long dash, no tech word, no VAT wording', not re.search('[–—]', tx) and not hit and not re.search(r'\bAI\b', tx) and not re.search(r'מע.?"?מ|VAT', tx), hit)
    sv = page.evaluate(JS_SURVEY, T)
    check(tag + ' survey red only on the yearly total', all(x.endswith(':y') or x == 'y' for x in sv), sv[:5])

def shot(page, name, full=False):
    if full: page.screenshot(path=str(OUT / f'{name}.png'), full_page=True)
    else: page.locator('#pv-camp').screenshot(path=str(OUT / f'{name}.png'))

def run(ctx, lg, W, mob, state):
    x = L[lg]; tag = f'{lg} {W}'; errs = []; dialogs = []; ext = []
    page = ctx.new_page()
    exp = []  # Chrome logs the deliberate server error of the failure test itself; counted apart, it must happen exactly once
    page.on('console', lambda m: (exp if 'status of 500' in m.text else errs).append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
    page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    page.on('dialog', lambda d: (dialogs.append(d.message), d.dismiss()))
    page.on('request', lambda r: ext.append(r.url) if not r.url.startswith(ORIGIN) and not re.match(r'https://fonts\.(googleapis|gstatic)\.com/', r.url) and not r.url.startswith('https://wa.me/') and not r.url.startswith('data:') else None)
    page.goto(BASE + x['q'], wait_until='networkidle')
    page.wait_for_selector(T + ' .nlcp')

    # the shell
    print(f'\n{tag}: step 1')
    check(tag + ' header: the title, "1 / 5", 5 progress segments, aria step 1', page.locator(T + ' h2.nli__title').inner_text().strip() == x['title'] and count(page) == '1 / 5'
          and page.locator(T + ' .nlcp__bar i').count() == 5 and page.get_attribute(T + ' .nlcp__bar', 'aria-valuenow') == '1' and head(page) == x['names'][0], [count(page), head(page)])
    ff = page.evaluate('(t) => { const h = document.querySelector(t + " h2.nli__title"), c = document.querySelector(t + " .nlcp__chip"), n = document.querySelector(t + " .nlcp__count"); return [getComputedStyle(h).fontFamily, parseFloat(getComputedStyle(h).fontSize), getComputedStyle(c).fontFamily, getComputedStyle(n).fontFamily, document.querySelector(t + " .nlcp").dir, document.querySelector(t + " .nlcp").lang]; }', T)
    check(tag + ' faces: the title in ' + x['title_font'] + (' at 32 px or more' if lg == 'he' else '') + ', the chips in ' + x['sans'] + ', figures in IBM Plex Mono; dir and lang',
          x['title_font'] in ff[0] and (ff[1] >= 32 if lg == 'he' else True) and ff[2].split(',')[0].strip('"') == x['sans'] and 'IBM Plex Mono' in ff[3] and ff[4] == ('rtl' if lg == 'he' else 'ltr') and ff[5] == lg, ff)
    check(tag + ' step 1: Back hidden, Next says "' + x['next'] + '"', page.locator(T + ' button[data-act="back"]').is_hidden() and page.locator(T + ' button[data-act="next"]').inner_text().strip() == x['next'])
    check(tag + ' ten market chips, each with its languages; the targeting line', page.locator(T + ' button.nlcp__chip').count() == 10 and 'EN · FR' in page.locator(T + ' button.nlcp__chip[data-m="ca"]').inner_text() and x['aim'] in tool_text(page))
    side = page.locator(T + ' .nlcp__side')
    check(tag + (' side panel shown (wide)' if not mob else ' side panel hidden on the phone'), side.is_visible() == (not mob))
    common(page, tag + ' step 1', lg)
    nxt(page)
    check(tag + ' Next with no market: the message, still step 1, focus on the first chip', x['e_markets'] in msgs(page) and count(page) == '1 / 5' and page.evaluate("(t) => document.activeElement && document.activeElement.getAttribute('data-m') === 'fr'", T), msgs(page))
    for m in ['fr', 'us', 'uk', 'ca', 'be', 'ch', 'za', 'au', 'ru', 'olim']:
        press(page, f'{T} button.nlcp__chip[data-m="{m}"]', 20)
    check(tag + ' all ten pressed: flagship recommended, languages en fr ru, the message cleared', page.locator(T + ' button.nlcp__chip[aria-pressed="true"]').count() == 10 and page.locator(T + ' [data-o="rec"]').inner_text().startswith('פרויקט דגל' if lg == 'he' else 'Flagship') and not msgs(page), page.locator(T + ' [data-o="rec"]').inner_text())
    for m in ['us', 'uk', 'ca', 'be', 'ch', 'za', 'au', 'ru', 'olim']:
        press(page, f'{T} button.nlcp__chip[data-m="{m}"]', 20)
    check(tag + ' France only: languages "' + x['langs1'] + '", one market ₪36,000', page.locator(T + ' [data-o="langs"]').inner_text() == x['langs1'] and x['rec1'] in page.locator(T + ' [data-o="rec"]').inner_text() and '₪36,000' in page.locator(T + ' [data-o="rec"]').inner_text(), page.locator(T + ' [data-o="rec"]').inner_text())
    press(page, f'{T} button.nlcp__chip[data-m="ca"]')
    check(tag + ' France + Canada: languages "' + x['langs2'] + '", three markets ₪72,000', page.locator(T + ' [data-o="langs"]').inner_text() == x['langs2'] and x['rec2'] in page.locator(T + ' [data-o="rec"]').inner_text() and '₪72,000' in page.locator(T + ' [data-o="rec"]').inner_text())
    shot(page, f'{lg}-{W}-step1')
    nxt(page)

    # 2. buyers
    print(f'{tag}: step 2')
    check(tag + ' step 2: "2 / 5", heading, aria step 2, focus on the heading, Back shown', count(page) == '2 / 5' and head(page) == x['names'][1] and page.get_attribute(T + ' .nlcp__bar', 'aria-valuenow') == '2' and focus_on_head(page) and page.locator(T + ' button[data-act="back"]').is_visible())
    check(tag + ' progress: segment 1 done, segment 2 current', page.evaluate("(t) => [...document.querySelectorAll(t + ' .nlcp__bar i')].map(i => i.className).join(',')", T) == 'is-on,is-now,,,')
    check(tag + ' four buyer cards (one choice)', page.locator(T + ' label.nlcp__card').count() == 4 and page.locator(T + ' input[type="radio"]').count() == 4)
    nxt(page)
    check(tag + ' Next with no buyer: the message, still step 2', x['e_buyer'] in msgs(page) and count(page) == '2 / 5')
    card(page, 'luxury'); card(page, 'invest')
    check(tag + ' one choice: investors checked, luxury not, the message cleared', page.is_checked(f'{T} input[value="invest"]') and not page.is_checked(f'{T} input[value="luxury"]') and not msgs(page))
    common(page, tag + ' step 2', lg)
    shot(page, f'{lg}-{W}-step2')
    press(page, T + ' button[data-act="back"]', 120)
    check(tag + ' Back to step 1: the chips kept', count(page) == '1 / 5' and page.locator(T + ' button.nlcp__chip[aria-pressed="true"]').count() == 2)
    nxt(page); check(tag + ' and forward: investors still checked', count(page) == '2 / 5' and page.is_checked(f'{T} input[value="invest"]'))
    nxt(page)

    # 3. budget
    print(f'{tag}: step 3')
    y = lambda: page.locator(T + ' [data-o="y"]').inner_text().strip()
    m = lambda: page.locator(T + ' [data-o="m"]').inner_text().strip()
    check(tag + ' step 3 opens at ₪10,000 a month, ₪120,000 a year', count(page) == '3 / 5' and m() == '₪10,000' and y() == '₪120,000' and page.input_value(T + ' input[data-f="budget"]') == '10,000', [m(), y()])
    col = page.evaluate("(t) => getComputedStyle(document.querySelector(t + ' [data-o=\"y\"]')).color", T)
    check(tag + ' the yearly total is the survey red figure', col == 'rgb(196, 37, 80)', col)
    for _ in range(3): press(page, T + ' button[data-act="plus"]', 30)
    check(tag + ' + three times: ₪13,000 / ₪156,000', m() == '₪13,000' and y() == '₪156,000', [m(), y()])
    press(page, T + ' button[data-act="minus"]', 30)
    check(tag + ' - once: ₪12,000 / ₪144,000, the slider follows', m() == '₪12,000' and y() == '₪144,000' and page.input_value(T + ' input.nlcp__range') == '12000')
    page.locator(T + ' input.nlcp__range').fill('60000'); page.wait_for_timeout(60)
    check(tag + ' slider to the end: ₪60,000 / ₪720,000, + disabled', m() == '₪60,000' and y() == '₪720,000' and page.locator(T + ' button[data-act="plus"]').is_disabled(), [m(), y()])
    page.locator(T + ' input.nlcp__range').fill('3000'); page.wait_for_timeout(60)
    check(tag + ' slider to the start: ₪3,000 / ₪36,000, - disabled', m() == '₪3,000' and y() == '₪36,000' and page.locator(T + ' button[data-act="minus"]').is_disabled())
    typ(page, T + ' input[data-f="budget"]', '2500'); nxt(page)
    check(tag + ' typed 2,500 and Next: the range message, still step 3', x['e_budget'] in msgs(page) and count(page) == '3 / 5', msgs(page))
    typ(page, T + ' input[data-f="budget"]', '25000')
    lg_items = page.locator(T + ' ul.nlcp__lg li').all_inner_texts()
    check(tag + ' typed 25,000: ₪25,000 / ₪300,000; the split ₪13,750 / ₪6,250 / ₪3,750 / ₪1,250; message cleared', m() == '₪25,000' and y() == '₪300,000' and all(a in ' '.join(lg_items) for a in ['₪13,750', '₪6,250', '₪3,750', '₪1,250']) and not msgs(page), lg_items)
    check(tag + ' the split is labelled a starting point, the ad budget paid straight to the channels', x['split_lab'] in tool_text(page) and x['paid'] in tool_text(page))
    check(tag + ' no reach, lead or cost-per-lead figure on the screen; NLCAMP.benchmarks is null', page.evaluate('window.NLCAMP.benchmarks') is None and not re.search(r'CPL|cost per lead|עלות לליד|לידים בחודש|leads a month', tool_text(page)))
    common(page, tag + ' step 3', lg)
    shot(page, f'{lg}-{W}-step3')
    press(page, T + ' details.nlcp__adj > summary', 120)
    press(page, T + ' button[data-sh="2"][data-d="1"]')
    check(tag + ' split: press +5 = 20%, the total 105%, "' + x['split_mine'] + '"', page.locator(T + ' [data-o="sh2"]').inner_text() == '20%' and page.locator(T + ' [data-o="sum"]').inner_text() == '105%' and x['split_mine'] in tool_text(page))
    nxt(page)
    check(tag + ' Next at 105%: the message, still step 3', x['e_split'] in msgs(page) and count(page) == '3 / 5', msgs(page))
    press(page, T + ' details.nlcp__adj > summary', 60)  # close the panel ...
    nxt(page)
    check(tag + ' ... and Next again: the panel opens itself to show the message', page.get_attribute(T + ' details.nlcp__adj', 'open') is not None and x['e_split'] in msgs(page))
    press(page, T + ' .nlcp__reset')
    check(tag + ' reset: back to 55 / 25 / 15 / 5, the message cleared', [page.locator(f'{T} [data-o="sh{i}"]').inner_text() for i in range(4)] == ['55%', '25%', '15%', '5%'] and not msgs(page) and x['split_lab'] in tool_text(page))
    press(page, T + ' button[data-sh="2"][data-d="1"]'); press(page, T + ' button[data-sh="0"][data-d="-1"]')
    items = ' '.join(page.locator(T + ' ul.nlcp__lg li').all_inner_texts())
    check(tag + ' Meta 50%, press 20%: ₪12,500 and ₪5,000, the total 100%', page.locator(T + ' [data-o="sum"]').inner_text() == '100%' and '₪12,500' in items and '₪5,000' in items, items[:160])
    common(page, tag + ' step 3 split open', lg)
    shot(page, f'{lg}-{W}-step3-split')
    page.locator(T + ' input[data-f="budget"]').focus(); page.keyboard.press('Enter'); page.wait_for_timeout(120)

    # 4. the project
    print(f'{tag}: step 4')
    check(tag + ' Enter in the budget field moves on: step 4', count(page) == '4 / 5' and head(page) == x['names'][3])
    nxt(page)
    check(tag + ' Next with no project kind: the message', x['e_kind'] in msgs(page) and count(page) == '4 / 5')
    card(page, 'existing')
    check(tag + ' existing page: the field "' + x['lab_ex'] + '"', page.locator(T + ' label[for$="-ref"]').inner_text().strip() == x['lab_ex'])
    nxt(page)
    check(tag + ' Next with the field empty: the message, focus in the field', x['e_ref'] in msgs(page) and count(page) == '4 / 5' and page.evaluate("(t) => document.activeElement && document.activeElement.getAttribute('data-f') === 'ref'", T))
    typ(page, T + ' input[data-f="ref"]', x['proj'])
    card(page, 'new')
    check(tag + ' a new project: the label "' + x['lab_new'] + '", the text kept', page.locator(T + ' label[for$="-ref"]').inner_text().strip() == x['lab_new'] and page.input_value(T + ' input[data-f="ref"]') == x['proj'])
    card(page, 'existing')
    common(page, tag + ' step 4', lg)
    shot(page, f'{lg}-{W}-step4')
    nxt(page)

    # 5. summary and plan
    print(f'{tag}: step 5')
    dl = page.locator(T + ' dl.nlcp__dl').inner_text()
    check(tag + ' step 5: "5 / 5", Next says "' + x['send'] + '"', count(page) == '5 / 5' and page.locator(T + ' button[data-act="next"]').inner_text().strip() == x['send'])
    check(tag + ' the summary list: markets, languages, buyers, budget, split, project', all(v in dl for v in x['dl']), [v for v in x['dl'] if v not in dl])
    check(tag + ' a "שינוי" button on each of the 6 rows', page.locator(T + ' dl.nlcp__dl button.nlcp__edit').count() == 6)
    th = page.locator(T + ' label.nlcp__card:has(input[value="three"])').inner_text()
    check(tag + ' the recommended plan is checked: three markets, ₪72,000 ' + x['year'] + ', tagged "' + x['tag2'] + '"', page.is_checked(T + ' input[value="three"]') and '₪72,000' in th and x['year'] in th and x['tag2'] in th, th.replace('\n', ' '))
    pl = ' '.join(page.locator(T + ' label.nlcp__card').all_inner_texts())
    check(tag + ' all three plans with yearly prices: ₪36,000, ₪72,000, ₪144,000', all(p in pl for p in ['₪36,000', '₪72,000', '₪144,000']) and pl.count(x['year']) >= 3)
    check(tag + ' the lead promise line', x['leads'] in tool_text(page))
    check(tag + ' the privacy notice with its link, the consent box unchecked', page.locator(T + ' .nlcp__priv a', has_text=x['privacy']).count() == 1 and not page.is_checked(T + ' input[data-f="consent"]'))
    common(page, tag + ' step 5', lg)
    shot(page, f'{lg}-{W}-step5')
    card(page, 'one')
    nxt(page, 200)
    ms = msgs(page)
    check(tag + ' plan "one market" for two markets and Send: the plan message and every contact message; nothing sent', x['e_cover'] in ms and x['e_name'] in ms and x['e_consent'] in ms and not state['bodies'] and count(page) == '5 / 5', ms[:220])
    check(tag + ' focus on the first invalid control (the plan)', page.evaluate("(t) => document.activeElement && document.activeElement.getAttribute('data-f') === 'plan'", T))
    common(page, tag + ' step 5 errors', lg)
    shot(page, f'{lg}-{W}-step5-errors')
    card(page, 'flag'); card(page, 'three')
    typ(page, T + ' input[data-f="name"]', x['name']); typ(page, T + ' input[data-f="company"]', x['company'])
    typ(page, T + ' input[data-f="phone"]', x['phone']); typ(page, T + ' input[data-f="email"]', 'dana@')
    nxt(page, 200)
    ms = msgs(page)
    check(tag + ' a bad email and no consent: only those two messages', x['e_email'] in ms and x['e_consent'] in ms and x['e_name'] not in ms and not state['bodies'], ms)
    typ(page, T + ' input[data-f="email"]', x['email'])
    press(page, T + ' label.nlcp__chk')
    check(tag + ' the consent box ticked by pressing its label', page.is_checked(T + ' input[data-f="consent"]'))
    # back to step 1 through "שינוי", one more market, forward again
    press(page, T + ' dl.nlcp__dl button.nlcp__edit[data-go="1"]', 150)
    check(tag + ' "שינוי" on the markets row: step 1, focus on the heading', count(page) == '1 / 5' and focus_on_head(page))
    press(page, f'{T} button.nlcp__chip[data-m="us"]')
    for _ in range(4): nxt(page, 100)
    check(tag + ' forward to step 5: three markets, the plan still three (chosen), the tag "' + x['tag3'] + '", the fields kept', count(page) == '5 / 5' and page.is_checked(T + ' input[value="three"]') and x['tag3'] in page.locator(T + ' label.nlcp__card:has(input[value="three"])').inner_text()
          and page.input_value(T + ' input[data-f="name"]') == x['name'] and page.input_value(T + ' input[data-f="email"]') == x['email'] and page.is_checked(T + ' input[data-f="consent"]'))
    # copy and WhatsApp
    press(page, T + ' button[data-act="copy"]', 300)
    clip = page.evaluate('navigator.clipboard.readText()')
    check(tag + ' copy: the plan as text, no name, company, phone or email', clip.startswith('תוכנית קמפיין' if lg == 'he' else 'International campaign plan') and x['clip3'] in clip and x['plan3'] in clip and x['leads'] in clip
          and x['name'] not in clip and x['company'] not in clip and x['phone'] not in clip and '@' not in clip and REF not in clip, clip[:140].replace('\n', ' | '))
    with ctx.expect_page() as pi:
        page.locator(T + ' a[data-act="wa"]').first.click()
    wa = pi.value; wa.wait_for_load_state(); wurl = wa.url; wa.close()
    wtext = urllib.parse.unquote(wurl.split('text=', 1)[-1])
    check(tag + ' WhatsApp: wa.me/?text= (no phone number), the same text (answered locally)', wurl.startswith('https://wa.me/?text=') and x['plan3'] in wtext and x['phone'] not in wtext, wurl[:60])
    # send: the server fails first
    state['fail'] = True
    nxt(page, 500)
    check(tag + ' send with a server error: the message, the form kept, Send pressable again', x['e_send'] in msgs(page) and count(page) == '5 / 5' and not page.locator(T + ' button[data-act="next"]').is_disabled()
          and page.locator(T + ' button[data-act="next"]').inner_text().strip() == x['send'] and page.locator(T + ' .nlcp__ref').count() == 0 and len(state['bodies']) == 1, msgs(page))
    state['fail'] = False
    nxt(page, 500)
    b = state['bodies'][-1] if state['bodies'] else {}
    a = page.locator(T + ' a[data-act="pay"]')
    check(tag + ' saved: the reference ' + REF + ', the payment step, launch after payment', page.locator(T + ' .nlcp__ref').inner_text().strip() == REF and x['ref_lab'] in tool_text(page) and x['launch'] in tool_text(page), tool_text(page)[:160].replace('\n', ' | '))
    check(tag + ' first-payment mode (the config default): "' + x['pay_first'] + '" to the first-payment product 8823 with the reference', a.count() == 1 and a.get_attribute('href') == '/checkout/?add-to-cart=8823&nlc_ref=' + REF
          and a.inner_text().strip() == x['pay_first'], a.inner_text().strip() if a.count() else None)
    check(tag + ' the rest line under it: "' + x['pay_rest'] + '"; no same-day link line', page.locator(T + ' [data-o="rest"]').inner_text().strip() == x['pay_rest'] and x['pay_later'] not in tool_text(page),
          page.locator(T + ' [data-o="rest"]').inner_text().strip() if page.locator(T + ' [data-o="rest"]').count() else None)
    check(tag + ' figures of the pay step in <bdi>: ₪18,000, ₪72,000, ₪54,000', page.evaluate("(t) => [...document.querySelectorAll(t + ' a[data-act=\"pay\"] bdi, ' + t + ' [data-o=\"rest\"] bdi')].map(b => b.textContent).join(' ')", T) == '₪18,000 ₪72,000 ₪54,000 ₪18,000')
    check(tag + ' after saving: the footer gone, "5 / 5", every segment done, focus on the heading', page.locator(T + ' .nlcp__ft').is_hidden() and count(page) == '5 / 5'
          and page.evaluate("(t) => [...document.querySelectorAll(t + ' .nlcp__bar i')].every(i => i.className === 'is-on')", T) and focus_on_head(page))
    check(tag + ' the brief sent: markets fr us ca, investors, 25,000, split 50/25/20/5, existing + text, plan three, consent, honeypot empty, no card field', b.get('markets') == ['fr', 'us', 'ca'] and b.get('buyer') == 'invest' and b.get('budget') == 25000 and b.get('shares') == [50, 25, 20, 5]
          and b.get('kind') == 'existing' and b.get('project') == x['proj'] and b.get('plan') == 'three' and b.get('consent') is True and b.get('hp') == '' and b.get('lang') == lg and b.get('t', 0) >= 2000
          and not [k for k in b if re.search('card|cvv|iban|passw', k)], {k: b.get(k) for k in ('markets', 'plan', 'budget', 't')})
    check(tag + ' sent as JSON by POST to /wp-json/nadlan/v1/campaign-brief, no cookies', state['meta'][-1] == ('POST', 'application/json', ''), state['meta'][-1])
    press(page, T + ' button[data-act="copy"]', 300)
    clip = page.evaluate('navigator.clipboard.readText()')
    check(tag + ' copy after saving carries the reference', x['t_ref'] in clip)
    common(page, tag + ' saved', lg)
    shot(page, f'{lg}-{W}-done'); shot(page, f'{lg}-{W}-done-page', full=True)
    check(tag + ' no dialog (no prompt fallback)', not dialogs, dialogs[:2])
    check(tag + ' nothing sent outside 127.0.0.1 (fonts and the wa.me stub aside)', not ext, ext[:4])
    check(tag + ' no console error or warning, no page error (the one expected 500 of the failure test aside: ' + str(len(exp)) + ')', not errs and len(exp) == 1, errs[:5])
    page.close()

    # the payment step in the two other server settings: the full plan in one charge (first amount 0, products 8809 / 8810 / 8811,
    # once Morning raises the cap), and no product at all (the option 0: the same-day link line)
    for case, js in (('full', "window.NLCAMP.configure({ plans: { three: { productUrl: '/checkout/?add-to-cart=8810', firstPay: null } } })"),
                     ('none', "window.NLCAMP.configure({ plans: { three: { productUrl: null, firstPay: null } } })")):
        page = ctx.new_page(); errs2 = []
        page.on('pageerror', lambda e: errs2.append(str(e)))
        page.goto(BASE + x['q'], wait_until='networkidle'); page.wait_for_selector(T + ' .nlcp')
        page.evaluate(js)
        for mk in ('fr', 'ca'): press(page, f'{T} button.nlcp__chip[data-m="{mk}"]', 20)
        nxt(page); card(page, 'home'); nxt(page); nxt(page); card(page, 'new'); nxt(page)
        typ(page, T + ' input[data-f="name"]', x['name']); typ(page, T + ' input[data-f="company"]', x['company']); typ(page, T + ' input[data-f="phone"]', x['phone']); typ(page, T + ' input[data-f="email"]', x['email'])
        press(page, T + ' label.nlcp__chk'); page.wait_for_timeout(2100); nxt(page, 500)
        a = page.locator(T + ' a[data-act="pay"]')
        if case == 'full':
            check(tag + ' full plan in one charge: "' + x['pay_btn'] + '" to product 8810 with the reference, no rest line', a.count() == 1 and a.get_attribute('href') == '/checkout/?add-to-cart=8810&nlc_ref=' + REF and a.inner_text().strip() == x['pay_btn']
                  and page.locator(T + ' [data-o="rest"]').count() == 0 and x['pay_later'] not in tool_text(page), a.inner_text().strip() if a.count() else None)
        else:
            check(tag + ' no product: no pay button, "' + x['pay_later'] + '"', a.count() == 0 and x['pay_later'] in tool_text(page) and page.locator(T + ' [data-o="rest"]').count() == 0)
        common(page, tag + ' pay ' + case, lg)
        shot(page, f'{lg}-{W}-pay-{case}')
        check(tag + ' (pay ' + case + ') no page error', not errs2, errs2[:3])
        page.close()

server = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(REPO)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(80):
        try: urllib.request.urlopen(BASE, timeout=1); break
        except Exception: time.sleep(0.25)
    with sync_playwright() as p:
        br = p.chromium.launch(channel='chrome', headless=True)
        for lg in ('he', 'en'):
            for W, H, mob in ((390, 844, True), (1280, 900, False)):
                state = {'fail': False, 'bodies': [], 'meta': []}
                def brief(route, request, state=state):
                    try: body = json.loads(request.post_data or '{}')
                    except Exception: body = {}
                    state['bodies'].append(body); state['meta'].append((request.method, (request.headers.get('content-type') or '').split(';')[0], request.headers.get('cookie', '')))
                    if state['fail']: route.fulfill(status=500, content_type='application/json', body='{"code":"nlc_store","message":"Could not save.","data":{"status":500}}')
                    else: route.fulfill(status=201, content_type='application/json', body=json.dumps({'ok': True, 'ref': REF, 'plan': body.get('plan'), 'price': 72000}))
                ctx = br.new_context(viewport={'width': W, 'height': H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, locale='he-IL' if lg == 'he' else 'en-GB')
                ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin=ORIGIN)
                ctx.route('**/wp-json/nadlan/v1/campaign-brief', brief)
                ctx.route('https://wa.me/**', lambda route: route.fulfill(status=200, content_type='text/plain', body='local stub'))
                ctx.route('https://nad-lan.co.il/**', lambda route: route.abort())  # nothing goes to the live site from these runs
                run(ctx, lg, W, mob, state)
                ctx.close()

        # one phone pass under the live theme stylesheets (read only)
        print('\nhe 390 + live theme')
        ctx = br.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=2, locale='he-IL')
        page = ctx.new_page(); errs = []
        page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        page.on('console', lambda m: errs.append(m.text + ' @ ' + str((m.location or {}).get('url', ''))) if m.type == 'error' and 'nad-lan.co.il' not in m.text + str((m.location or {}).get('url', '')) else None)
        page.goto(BASE + '?theme=1', wait_until='networkidle'); page.wait_for_selector(T + ' .nlcp')
        press(page, f'{T} button.nlcp__chip[data-m="fr"]'); press(page, f'{T} button.nlcp__chip[data-m="ru"]')
        common(page, 'theme 390 step 1', 'he')
        ff = page.evaluate('''(t) => { const q = s => getComputedStyle(document.querySelector(t + ' ' + s)); return [q('button.nlcp__chip').fontFamily.split(',')[0], q('button.nlcp__chip[aria-pressed="true"]').backgroundColor, q('button[data-act="next"]').fontFamily.split(',')[0], q('button[data-act="next"]').backgroundColor, q('button.nlcp__chip').borderRadius, q('h2.nli__title').color]; }''', T)
        check('theme 390: chips and buttons keep Plex Sans Hebrew, the pressed chip and Next in sea, chips round, the title in ink', 'Plex Sans Hebrew' in ff[0] and ff[1] == 'rgb(47, 111, 134)' and 'Plex Sans Hebrew' in ff[2] and ff[3] == 'rgb(47, 111, 134)' and ff[4] in ('999px', '9.99e+02px') and ff[5] == 'rgb(18, 32, 42)', ff)
        shot(page, 'theme-he-390-step1')
        nxt(page); card(page, 'parents'); nxt(page)
        common(page, 'theme 390 step 3', 'he')
        fi = page.evaluate("(t) => [getComputedStyle(document.querySelector(t + ' input[data-f=\"budget\"]')).fontFamily.split(',')[0], getComputedStyle(document.querySelector(t + ' ul.nlcp__lg')).listStyleType, getComputedStyle(document.querySelector(t + ' [data-o=\"y\"]')).color]", T)
        check('theme 390 step 3: the budget field in Plex Mono, the legend without bullets, the yearly total survey red', 'Plex Mono' in fi[0] and fi[1] == 'none' and fi[2] == 'rgb(196, 37, 80)', fi)
        shot(page, 'theme-he-390-step3')
        nxt(page); card(page, 'new'); nxt(page)
        common(page, 'theme 390 step 5', 'he')
        shot(page, 'theme-he-390-step5'); page.screenshot(path=str(OUT / 'theme-he-390-page.png'), full_page=True)
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
