"""HAD-675 round H: press every chip and field of mkeys ("מהחוזה למפתח") in preview.html, in headless Chrome (Playwright, channel
chrome), at 390x844 (is_mobile) and 1280x900, plus one phone pass over the live theme stylesheets (?theme=1, read only).
Needs the repo root served on 127.0.0.1:47971 (python -m http.server 47971 --bind 127.0.0.1). Writes screenshots into
round-h/shots and prints a JSON report; exit 1 on any failed check."""
import json, sys, pathlib, re
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:47971/docs/research/2026-11-05-mortgage-world/build/round-h/preview.html'
OUT = pathlib.Path(__file__).resolve().parent / 'shots'
OUT.mkdir(parents=True, exist_ok=True)
report, fails = [], []

def check(name, cond, got=None):
    report.append({'check': name, 'ok': bool(cond), 'got': got})
    if not cond: fails.append(name)

JS_HSCROLL = '() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth, cw: document.documentElement.clientWidth})'
JS_SMALL = '''() => { const r = document.querySelector('#nlmk'); const out = [];
  r.querySelectorAll('button, input, select').forEach(e => { const b = e.getBoundingClientRect();
    if (b.width > 0 && b.height > 0 && b.height < 43.5) out.push(e.tagName + '#' + (e.id || '') + ' ' + (e.textContent || '').trim().slice(0, 20) + ' ' + b.height.toFixed(1)); });
  return out; }'''
JS_LABELS = '''() => [...document.querySelectorAll('#nlmk input, #nlmk select')].map(e => ({id: e.id,
  label: (e.labels && e.labels.length ? e.labels[0].textContent : (e.getAttribute('aria-label') || '')).trim()})).filter(x => !x.label)'''
JS_GROUPS = '''() => [...document.querySelectorAll('#nlmk [role="group"]')].map(g => { const id = g.getAttribute('aria-labelledby');
  const l = id && document.getElementById(id); return l ? l.textContent.trim() : ''; })'''
JS_TEXT = '() => document.querySelector("#nlmk").innerText'
JS_FIG = '() => document.querySelector("#nlmk .nlmk__fig").innerText.trim()'
def fmt(x):
    return '{:,}'.format(int(round(x)))

def press(page, sel):
    page.locator(sel).click(); page.wait_for_timeout(150)

def fig(page):
    return page.evaluate(JS_FIG)

def typ(page, sel, text):
    loc = page.locator(sel); loc.click(); loc.press('Control+A'); loc.press('Backspace')
    if text: page.keyboard.type(text)
    page.wait_for_timeout(250)

with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', headless=True)
    for W, H, mob in ((390, 844, True), (1280, 900, False)):
        tag = str(W)
        ctx = br.new_context(viewport={'width': W, 'height': H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1, locale='he-IL')
        try: ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin='http://127.0.0.1:47971')
        except Exception: pass
        page = ctx.new_page(); errs = []
        page.on('console', lambda m, errs=errs: errs.append('console.' + m.type + ': ' + m.text) if m.type in ('error', 'warning') else None)
        page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
        page.goto(BASE, wait_until='networkidle')
        page.wait_for_selector('#nlmk .nlmk__fig bdi')
        today = page.evaluate('() => { const d = new Date(); const p = n => (n < 10 ? "0" : "") + n; return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate()); }')
        check(tag + ' opens on today as the signing date', page.input_value('#nlmk-s') == today, page.input_value('#nlmk-s'))
        y, m, d = today.split('-'); m2 = int(m) - 1 + 36; dl = '%04d-%02d-%s' % (int(y) + m2 // 12, m2 % 12 + 1, d)
        check(tag + ' delivery opens 36 months later', page.input_value('#nlmk-d') == dl, page.input_value('#nlmk-d'))
        check(tag + ' opening values 2,000,000 / 600,000', page.input_value('#nlmk-p') == '2,000,000' and page.input_value('#nlmk-e') == '600,000')
        pressed = page.evaluate('() => [...document.querySelectorAll("#nlmk [aria-pressed=true]")].map(b => b.textContent)')
        check(tag + ' opening chips: stages, interest paid, 25 years', pressed == ['לפי שלבים', 'משלמים ריבית', '25 שנה'], pressed)
        iv = page.input_value('#nlmk-i'); help_ = page.locator('#nlmk-i-h').inner_text()
        check(tag + ' index field opens at the trailing 12-month change with its source months', iv == '3.59' and '9.2025' in help_ and '9.2026' in help_ and '3.6%' in help_, [iv, help_])
        # expected headline from the pure logic with the form's values (data fetched again in the page)
        def expected():
            return page.evaluate('''async () => { const K = window.NLMK, q = s => document.querySelector(s), n = s => parseFloat(String(s).replace(/[^\\d.]/g, ''));
              const [D, C] = await Promise.all(['/plugins/nadlan-config/assets/instruments/data/boi-mortgage.json', '/plugins/nadlan-config/assets/instruments/data/cbs-200010.json'].map(u => fetch(u).then(r => r.json())));
              const pr = b => [...document.querySelectorAll('#nlmk [' + b + ']')].filter(x => x.getAttribute('aria-pressed') === 'true')[0].getAttribute(b);
              const iv = parseFloat(q('#nlmk-i').value), tr = window.NLIX.trailing(C);
              const v = { price: n(q('#nlmk-p').value), equity: n(q('#nlmk-e').value), sign: q('#nlmk-s').value, delivery: q('#nlmk-d').value,
                plan: pr('data-plan'), grace: pr('data-grace'), years: +pr('data-years'), annual: Math.abs(iv - tr * 100) < 0.005 ? null : iv / 100 };
              const r = K.compute(v, D, C); return r.error ? {err: r.error.msg} : {pay: r.pay, no: r.noMortgage, link: r.linkTotal, int: r.interest, bal: r.balance, share: r.share, over: r.over75, rows: r.rows.length}; }''')
        e0 = expected()
        f0 = fig(page)
        check(tag + ' headline = NLMK.compute on the form values', fmt(e0['pay']) in f0, [f0, fmt(e0['pay'])])
        sub = page.locator('#nlmk .nlmk__sub').inner_text()
        check(tag + ' summary line: linkage, interest, mortgage at delivery', fmt(e0['link']) in sub and fmt(e0['int']) in sub and fmt(e0['bal']) in sub, sub)
        ltv = page.locator('#nlmk .nlmk__ltv').inner_text()
        check(tag + ' financing share shown, not flagged at 600,000', ('%.1f%%' % (e0['share'] * 100)) in ltv and 'is-over' not in page.get_attribute('#nlmk .nlmk__ltv', 'class'), ltv)
        n_li = page.locator('#nlmk ol.nlmk__tl > li').count()
        check(tag + ' timeline: one row per payment + the keys row', n_li == e0['rows'] + 1, n_li)
        t_first = page.locator('#nlmk ol.nlmk__tl > li').first.inner_text()
        check(tag + ' first row: 20% at signing without linkage, from equity', 'בלי הצמדה' in t_first and 'מההון העצמי' in t_first and '20% בחתימה' in t_first, t_first)
        t_keys = page.locator('#nlmk ol.nlmk__tl > li.is-keys').inner_text()
        check(tag + ' keys row: balance spread over 25 years and the full payment', 'המפתח' in t_keys and '25 שנה' in t_keys and fmt(e0['pay']) in t_keys, t_keys)
        ff = page.evaluate('() => ["#nlmk .nlmk__t", "#nlmk .nlmk__src", "#nlmk .nlmk__sub"].map(s => getComputedStyle(document.querySelector(s)).fontFamily.split(",")[0])')
        check(tag + ' running sentences in the text face', all('Plex Sans Hebrew' in f for f in ff), ff)
        ffn = page.evaluate('() => [getComputedStyle(document.querySelector("#nlmk .nlmk__fig")).fontFamily.split(",")[0], getComputedStyle(document.querySelector("#nlmk .nlmk__sub bdi")).fontFamily.split(",")[0], getComputedStyle(document.querySelector("#nlmk-p")).fontFamily.split(",")[0]]')
        check(tag + ' numbers in the mono face (headline, summary numbers, money fields)', all('Plex Mono' in f for f in ffn), ffn)
        cols = page.evaluate('() => getComputedStyle(document.querySelector("#nlmk .nlmk__grid")).gridTemplateColumns.split(" ").length')
        check(tag + ' layout: ' + ('one column on the phone' if mob else 'form and result side by side'), cols == (1 if mob else 2), cols)
        page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-default-{tag}.png'))
        page.screenshot(path=str(OUT / f'page-default-{tag}.png'), full_page=True)

        # every chip
        seen = {}
        for g in ('full', 'immediate', 'partial'):
            press(page, f'#nlmk button[data-grace="{g}"]')
            e = expected(); f = fig(page); seen[g] = f
            check(f'{tag} grace {g}: pressed and headline = logic', page.get_attribute(f'#nlmk button[data-grace="{g}"]', 'aria-pressed') == 'true' and fmt(e['pay']) in f, [f, fmt(e['pay'])])
            if g == 'full':
                s2 = page.locator('#nlmk .nlmk__sub').inner_text()
                check(tag + ' full grace: "ריבית שנצברה" and a balance above the draws', 'ריבית שנצברה עד המסירה' in s2 and 'נצברת עליה' in page.locator('#nlmk .nlmk__tl').inner_text(), s2)
                check(tag + ' full grace at 600,000: the capitalized balance flagged above 75%', 'is-over' in page.get_attribute('#nlmk .nlmk__ltv', 'class') and 'עם הריבית שנצברה' in page.locator('#nlmk .nlmk__ltv').inner_text(), page.locator('#nlmk .nlmk__ltv').inner_text())
                page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-grace-full-{tag}.png'))
            if g == 'immediate':
                s3 = page.locator('#nlmk .nlmk__sub').inner_text(); tl = page.locator('#nlmk .nlmk__tl').inner_text()
                check(tag + ' immediate: paid until delivery and its interest, "מכאן החזר" per row', 'שולם לבנק עד המסירה' in s3 and 'מזה ריבית' in s3 and 'מכאן החזר' in tl and 'מיום המשיכה' in tl, s3)
                page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-grace-immediate-{tag}.png'))
        check(tag + ' full grace headline above partial', int(re.sub(r'\D', '', seen['full'])) > int(re.sub(r'\D', '', seen['partial'])), seen)
        for pl in ('end', 'thirds', 'stages'):
            press(page, f'#nlmk button[data-plan="{pl}"]')
            e = expected(); f = fig(page)
            check(f'{tag} plan {pl}: pressed, {e["rows"]} payments, headline = logic', page.get_attribute(f'#nlmk button[data-plan="{pl}"]', 'aria-pressed') == 'true' and fmt(e['pay']) in f and page.locator('#nlmk ol.nlmk__tl > li').count() == e['rows'] + 1, [f, e['rows']])
            if pl == 'end':
                tl = page.locator('#nlmk .nlmk__tl').inner_text()
                check(tag + ' 20/80: no interest before the keys (the draw is at delivery)', 'בלי ריבית לפני המסירה' in page.locator('#nlmk .nlmk__sub').inner_text(), page.locator('#nlmk .nlmk__sub').inner_text())
                page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-plan-2080-{tag}.png'))
            if pl == 'thirds':
                page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-plan-203050-{tag}.png'))
        for yv in (20, 30, 25):
            press(page, f'#nlmk button[data-years="{yv}"]')
            e = expected(); f = fig(page)
            check(f'{tag} term {yv}: pressed, headline = logic, keys row says {yv}', page.get_attribute(f'#nlmk button[data-years="{yv}"]', 'aria-pressed') == 'true' and fmt(e['pay']) in f and f'{yv} שנה' in page.locator('#nlmk li.is-keys').inner_text(), f)

        # every field
        typ(page, '#nlmk-e', '400000'); e = expected()
        ltv = page.locator('#nlmk .nlmk__ltv').inner_text()
        check(tag + ' equity 400,000: share above 75% underlined with the directive 329 sentence', e['over'] and 'is-over' in page.get_attribute('#nlmk .nlmk__ltv', 'class') and 'מעל 75%' in ltv and 'הוראה 329' in ltv, ltv)
        deco = page.evaluate('() => { const s = getComputedStyle(document.querySelector("#nlmk .nlmk__ltv.is-over bdi")); return [s.textDecorationLine, s.textDecorationColor]; }')
        check(tag + ' the underline is #C42550', deco[0] == 'underline' and deco[1] in ('rgb(196, 37, 80)',), deco)
        page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-over75-{tag}.png'))
        page.locator('#nlmk-e').blur(); page.wait_for_timeout(100)
        check(tag + ' money field reformats on blur', page.input_value('#nlmk-e') == '400,000', page.input_value('#nlmk-e'))
        typ(page, '#nlmk-p', '2500000'); e = expected()
        check(tag + ' price 2,500,000: headline = logic', fmt(e['pay']) in fig(page), [fig(page), fmt(e['pay'])])
        page.locator('#nlmk-s').fill('2027-01-20'); page.wait_for_timeout(250)
        check(tag + ' a new signing date moves the untouched delivery 36 months on', page.input_value('#nlmk-d') == '2030-01-20', page.input_value('#nlmk-d'))
        e = expected(); check(tag + ' signing 20.1.2027: headline = logic', fmt(e['pay']) in fig(page), fig(page))
        page.locator('#nlmk-d').fill('2029-06-30'); page.wait_for_timeout(250)
        page.locator('#nlmk-s').fill('2027-02-10'); page.wait_for_timeout(250)
        check(tag + ' a delivery typed by hand stays when the signing date changes', page.input_value('#nlmk-d') == '2029-06-30', page.input_value('#nlmk-d'))
        e = expected(); check(tag + ' delivery 30.6.2029: headline and keys row date', fmt(e['pay']) in fig(page) and '06.2029' in page.locator('#nlmk li.is-keys').inner_text(), fig(page))
        typ(page, '#nlmk-i', '5'); e = expected(); src = page.locator('#nlmk .nlmk__src').inner_text()
        check(tag + ' index change 5%: headline = logic, the note says 5.0% as typed', fmt(e['pay']) in fig(page) and '5.0%' in src and 'כפי שהקלדתם' in src, [fig(page), src[-160:]])
        typ(page, '#nlmk-i', '-1'); e = expected()
        check(tag + ' a negative change is accepted', 'err' not in e and fmt(e['pay']) in fig(page), fig(page))
        dirn = page.evaluate('() => getComputedStyle(document.querySelector("#nlmk-i")).direction')
        check(tag + ' the index field reads left to right (the minus stays before the number)', dirn == 'ltr' and page.input_value('#nlmk-i') == '-1', [dirn, page.input_value('#nlmk-i')])
        page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-index-negative-{tag}.png'))

        # validation
        typ(page, '#nlmk-p', '')
        check(tag + ' empty price: message under the field and in the result, numbers hidden', 'מחיר הדירה' in page.locator('[data-err="nlmk-p"]').inner_text() and page.locator('#nlmk .nlmk__msg').is_visible() and not page.locator('#nlmk .nlmk__ok').is_visible() and not page.locator('#nlmk .nlmk__copy').is_visible(), page.locator('#nlmk .nlmk__msg').inner_text())
        page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-error-price-{tag}.png'))
        typ(page, '#nlmk-p', '2000000'); typ(page, '#nlmk-e', '2500000')
        check(tag + ' equity above price: message under equity', 'גבוה ממחיר הדירה' in page.locator('[data-err="nlmk-e"]').inner_text(), page.locator('[data-err="nlmk-e"]').inner_text())
        typ(page, '#nlmk-e', '600000'); page.locator('#nlmk-d').fill('2026-01-01'); page.wait_for_timeout(250)
        check(tag + ' delivery before signing: message under delivery', 'אחרי תאריך החתימה' in page.locator('[data-err="nlmk-d"]').inner_text(), page.locator('[data-err="nlmk-d"]').inner_text())
        page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-error-delivery-{tag}.png'))
        page.locator('#nlmk-d').fill(''); page.wait_for_timeout(250)
        check(tag + ' empty delivery: message', 'מועד המסירה' in page.locator('[data-err="nlmk-d"]').inner_text(), page.locator('[data-err="nlmk-d"]').inner_text())
        page.locator('#nlmk-s').fill(''); page.wait_for_timeout(250)
        check(tag + ' empty signing date: message', 'חתימת החוזה' in page.locator('[data-err="nlmk-s"]').inner_text(), page.locator('[data-err="nlmk-s"]').inner_text())
        typ(page, '#nlmk-i', '')
        page.locator('#nlmk-s').fill(today); page.locator('#nlmk-d').fill(dl); page.wait_for_timeout(250)
        check(tag + ' empty index change: message', 'שינוי שנתי' in page.locator('[data-err="nlmk-i"]').inner_text(), page.locator('[data-err="nlmk-i"]').inner_text())

        # no mortgage: equity = price, index flat
        typ(page, '#nlmk-i', '0'); typ(page, '#nlmk-e', '2000000'); e = expected()
        f = fig(page)
        check(tag + ' flat index: future rows say "לפי השינוי שבחרתם"', 'לפי השינוי שבחרתם במדד' in page.locator('#nlmk .nlmk__tl').inner_text())
        check(tag + ' equity = price, index flat: "לא צריך משכנתא", not "0 ₪"', e['no'] and f == 'לא צריך משכנתא' and '0 ₪' not in f and not page.locator('#nlmk .nlmk__ltv').is_visible(), f)
        page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-no-mortgage-{tag}.png'))
        typ(page, '#nlmk-e', '600000'); typ(page, '#nlmk-i', '3.59')

        # copy: clipboard, then the prompt fallback
        page.locator('#nlmk .nlmk__copy').click(); page.wait_for_timeout(300)
        clip = None
        try: clip = page.evaluate('() => navigator.clipboard.readText()')
        except Exception as ex: clip = 'ERR ' + str(ex)[:80]
        check(tag + ' copy: the clipboard holds the result and the link', bool(clip) and 'ההחזר המלא אחרי המפתח' in clip and 'preview.html#tool-keys' in clip, (clip or '')[:140])
        check(tag + ' copy: the button says "הועתק"', page.locator('#nlmk .nlmk__copy').inner_text() == 'הועתק', page.locator('#nlmk .nlmk__copy').inner_text())
        page.wait_for_timeout(1700)
        dlg = []
        page.on('dialog', lambda dg, dlg=dlg: (dlg.append(dg.default_value), dg.dismiss()))
        page.evaluate('() => { Object.defineProperty(navigator, "clipboard", {value: undefined, configurable: true}); }')
        page.locator('#nlmk .nlmk__copy').click(); page.wait_for_timeout(300)
        check(tag + ' copy without a clipboard: the prompt shows the text', len(dlg) == 1 and 'מהחוזה למפתח' in dlg[0], dlg[:1])

        # the page-wide checks after all the pressing
        txt = page.evaluate(JS_TEXT)
        check(tag + ' no long dashes in the tool', not re.search('[–—]', txt))
        check(tag + ' no banned words', not re.search(r'\bAI\b|סימולציה|דמו|ממשק|אינטראקטיבי', txt))
        check(tag + ' no NaN or undefined on the surface', not re.search(r'NaN|undefined|Infinity', txt))
        small = page.evaluate(JS_SMALL); check(tag + ' every button and input at least 44 px tall', not small, small)
        nolab = page.evaluate(JS_LABELS); check(tag + ' every input has a label', not nolab, nolab)
        grp = page.evaluate(JS_GROUPS); check(tag + ' every chip group is named', len(grp) == 3 and all(grp), grp)
        hs = page.evaluate(JS_HSCROLL); check(tag + ' no horizontal scroll (scrollWidth - innerWidth = 0)', hs['sw'] - hs['iw'] == 0, hs)
        page.locator('#nlmk').screenshot(path=str(OUT / f'mkeys-after-all-{tag}.png'))
        check(tag + ' no console errors or warnings', not errs, errs)
        ctx.close()

    # the live theme stylesheets (read only) over the tool, phone
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    page = ctx.new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.goto(BASE + '?theme=1', wait_until='networkidle'); page.wait_for_selector('#nlmk .nlmk__fig bdi')
    st = page.evaluate('''() => { const h = getComputedStyle(document.querySelector('#nlmk h2.nlmk__h')), li = getComputedStyle(document.querySelector('#nlmk ol.nlmk__tl > li')),
      b = document.querySelector('#nlmk button[data-plan="end"]'), bs = getComputedStyle(b), i = getComputedStyle(document.querySelector('#nlmk-p'));
      const t = getComputedStyle(document.querySelector('#nlmk .nlmk__t'));
      return {t: t.fontSize + ' ' + t.fontWeight, h2: h.fontSize + ' ' + h.color, li: li.listStyleType + ' ' + li.paddingTop, btnH: b.getBoundingClientRect().height, btnR: bs.borderTopLeftRadius, inFont: i.fontFamily.split(',')[0], inBorder: i.borderTopWidth}; }''')
    check('theme: heading 20px ink, list unstyled, chips 2px radius, mono input without its own border', st['h2'].startswith('20px rgb(18, 32, 42)') and st['li'].startswith('none') and st['btnH'] >= 44 and st['btnR'] == '2px' and 'Plex Mono' in st['inFont'] and st['inBorder'] == '0px' and st['t'] == '13px 400', st)
    small = page.evaluate(JS_SMALL); check('theme: every button and input at least 44 px tall', not small, small)
    hs = page.evaluate(JS_HSCROLL); check('theme: no horizontal scroll', hs['sw'] - hs['iw'] == 0, hs)
    page.locator('#nlmk').screenshot(path=str(OUT / 'mkeys-theme-390.png'))
    check('theme: no page errors', not errs, errs)
    ctx.close(); br.close()

print(json.dumps({'checks': len(report), 'failed': fails, 'report': report}, ensure_ascii=False, indent=1))
sys.exit(1 if fails else 0)
