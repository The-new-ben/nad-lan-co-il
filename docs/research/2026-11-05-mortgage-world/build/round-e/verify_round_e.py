"""HAD-675 round E: press the two tools of preview.html in headless Chrome (Playwright, channel chrome) at 390x844 and 1280x800.
Writes screenshots into round-e/screens and prints a JSON report. Exit 1 on any failed check."""
import json, sys, pathlib
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:47962/docs/research/2026-11-05-mortgage-world/build/round-e/preview.html'
REPO = pathlib.Path(r'C:\Users\777\nad-lan\nad-lan-co-il')
OUT = REPO / 'docs/research/2026-11-05-mortgage-world/build/round-e/screens'
OUT.mkdir(parents=True, exist_ok=True)
LIVE_MQUICK = (REPO / 'plugins/nadlan-config/assets/instruments/tools/mquick.js').read_text(encoding='utf-8')

report, fails = [], []
def check(name, cond, got=None):
    report.append({'check': name, 'ok': bool(cond), 'got': got})
    if not cond: fails.append(name)

def no_hscroll(page):
    return page.evaluate('() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth})')

def small_controls(page, scope):
    return page.evaluate('''(scope) => { const r = document.querySelector(scope); if (!r) return ['no scope'];
      const out = []; r.querySelectorAll('button, select, a.nlmq__btn, .nlmq__in, .nli__in').forEach(e => { const b = e.getBoundingClientRect();
        if (b.width > 0 && b.height > 0 && b.height < 44 - 0.5) out.push((e.tagName + '.' + e.className + ' ' + (e.textContent || '').trim().slice(0, 24) + ' ' + b.height.toFixed(1))); });
      return out; }''', scope)

def long_dashes(page, scope):
    return page.evaluate('(s) => { const t = document.querySelector(s).innerText; return (t.match(/[\\u2013\\u2014]/g) || []).length; }', scope)

with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', headless=True)
    for W, H in ((390, 844), (1280, 800)):
        tag = str(W)
        ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1)
        page = ctx.new_page(); errs = []
        page.on('console', lambda m, errs=errs: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
        page.goto(BASE, wait_until='networkidle')
        page.wait_for_selector('#nlmq .nlmq__fig bdi'); page.wait_for_selector('#pv-exit .mrx')
        # ---- mquick, Hebrew
        q = page.locator('#nlmq')
        check(tag + ' mquick default payment 5,428', '5,428' in q.locator('.nlmq__fig').inner_text(), q.locator('.nlmq__fig').inner_text())
        check(tag + ' city select hidden in amount mode', not page.locator('#nlmq-c').is_visible())
        q.locator('button[data-m="price"]').click()
        check(tag + ' city select visible in price mode', page.locator('#nlmq-c').is_visible())
        opts = page.eval_on_selector_all('#nlmq-c option', 'os => os.map(o => [o.value, o.textContent])')
        check(tag + ' 26 options (placeholder, Israel, 24 cities)', len(opts) == 26 and opts[0][0] == '' and opts[1][1] == 'ישראל', [o[1] for o in opts[:4]])
        check(tag + ' no city: price 1,600,000 and payment unchanged', page.input_value('#nlmq-p') == '1,600,000' and '6,514' in q.locator('.nlmq__fig').inner_text(), q.locator('.nlmq__fig').inner_text())
        sh = page.evaluate('() => { const s = document.querySelector("#nlmq-c"); const b = s.getBoundingClientRect(); const cs = getComputedStyle(s); return {h: b.height, box: s.parentNode.getBoundingClientRect().height, fs: cs.fontSize}; }')
        check(tag + ' select box >= 44 px, font 16 px', sh['box'] >= 44 and sh['h'] >= 44 and sh['fs'] == '16px', sh)
        q.screenshot(path=str(OUT / f'mquick-he-price-nocity-{tag}.png'))
        page.select_option('#nlmq-c', 'תל אביב יפו')
        cq = page.locator('#nlmq .nlmq__cq').inner_text()
        check(tag + ' Tel Aviv-Yafo fills 5,229,800 and its quarter', page.input_value('#nlmq-p') == '5,229,800' and cq == 'חציון 1-3.2026, רשות המסים', [page.input_value('#nlmq-p'), cq])
        fig = q.locator('.nlmq__fig').inner_text(); ltv = q.locator('.nlmq__ltv').inner_text()
        check(tag + ' payment on a 4,829,800 loan, LTV 92.4%', '26,218' in fig and '92.4%' in ltv, [fig, ltv])
        q.screenshot(path=str(OUT / f'mquick-he-city-tlv-{tag}.png'))
        page.select_option('#nlmq-c', 'ישראל')
        check(tag + ' Israel: 2,028,800 (4-6.2026)', page.input_value('#nlmq-p') == '2,028,800' and '4-6.2026' in page.locator('#nlmq .nlmq__cq').inner_text())
        page.fill('#nlmq-p', '2,500,000')
        check(tag + ' typing a price clears the city', page.input_value('#nlmq-c') == '' and not page.locator('#nlmq .nlmq__cq').is_visible(), page.input_value('#nlmq-c'))
        check(tag + ' mquick controls >= 44 px', not small_controls(page, '#nlmq'), small_controls(page, '#nlmq'))
        check(tag + ' mquick no long dashes', long_dashes(page, '#nlmq') == 0)
        # ---- mexit, existing loan + refinance
        X = page.locator('#pv-exit')
        X.get_by_role('button', name='משכנתא שכבר יש לי').click()
        page.wait_for_selector('#pv-exit h3.mrx__h:has-text("האם למחזר?")')
        fee = X.locator('.nli__grid').first.locator('.nli__fig').inner_text()
        check(tag + ' the fee of the worked example still 15,908', '15,908' in fee, fee)
        sec = X.locator('section.mrx__sec').filter(has_text='האם למחזר?')
        rfig = sec.locator('.nli__fig').inner_text(); rtext = sec.inner_text()
        check(tag + ' refinance: 162 months', rfig.strip() == '162 חודשים', rfig)
        for s in ('5,776', '5,671', '105', '15,908', '957', '16,925', '4.79% אפקטיבית', '4.69% לתשלום חודשי', '19.10.2026', '9.2026', '162 מתוך 276', 'לא הוקלדו'):
            check(tag + ' refinance shows ' + s, s in rtext)
        check(tag + ' rate field opens at the average 4.69', sec.locator('input').first.input_value() == '4.69', sec.locator('input').first.input_value())
        check(tag + ' extra costs field empty', sec.locator('input').nth(1).input_value() == '')
        check(tag + ' no "מומלץ" anywhere in mexit', 'מומלץ' not in X.inner_text())
        check(tag + ' mexit no long dashes', long_dashes(page, '#pv-exit') == 0)
        sec.scroll_into_view_if_needed()
        X.screenshot(path=str(OUT / f'mexit-have-refi-{tag}.png'))
        sec.screenshot(path=str(OUT / f'mexit-refi-section-{tag}.png'))
        sec.get_by_role('button', name='10 ימים ומעלה').click(); page.wait_for_timeout(250)
        check(tag + ' notice of 10 days or more: 153 months', sec.locator('.nli__fig').inner_text().strip() == '153 חודשים', sec.locator('.nli__fig').inner_text())
        ex = sec.locator('input').nth(1); ex.click(); page.keyboard.type('3000'); page.wait_for_timeout(250)
        check(tag + ' typing 3000 keeps focus in the field', page.evaluate('() => document.activeElement && document.activeElement.closest("section.mrx__sec") !== null'))
        check(tag + ' extra 3,000 (notice 10+ days): 181 months', sec.locator('.nli__fig').inner_text().strip() == '181 חודשים', sec.locator('.nli__fig').inner_text())
        rr = sec.locator('input').first; rr.click(); rr.press('Control+A'); page.keyboard.type('4.83'); page.wait_for_timeout(250)
        check(tag + ' an offer of 4.83%: "לא משתלם כרגע"', sec.locator('.nli__fig').inner_text().strip() == 'לא משתלם כרגע', sec.locator('.nli__fig').inner_text())
        check(tag + ' typed rate labelled as typed', 'כפי שהקלדתם' in sec.inner_text())
        sec.screenshot(path=str(OUT / f'mexit-refi-not-worth-{tag}.png'))
        # prime: no capitalization fee, said so
        X.locator('select').first.select_option('prime'); page.wait_for_timeout(300)
        sec = X.locator('section.mrx__sec').filter(has_text='האם למחזר?'); t2 = sec.inner_text()
        check(tag + ' prime: "ללא: פריים" and the Banking Order note', 'ללא: פריים' in t2 and 'במסלול הפריים אין עמלת היוון' in t2 and 'משכנתאות חדשות בכל הבנקים, 9.2026' in t2, t2[:120])
        sec.screenshot(path=str(OUT / f'mexit-refi-prime-{tag}.png'))
        X.locator('select').first.select_option('var_cpi'); page.wait_for_timeout(300)
        t3 = X.locator('section.mrx__sec').filter(has_text='האם למחזר?').inner_text()
        check(tag + ' variable: fee to the change day, said so', 'עד יום שינוי הריבית הבא' in t3 and '11.2029' in t3, t3[:80])
        check(tag + ' mexit controls >= 44 px', not small_controls(page, '#pv-exit .mrx__rfg'), small_controls(page, '#pv-exit .mrx__rfg'))
        hs = no_hscroll(page)
        check(tag + ' no horizontal scroll (Hebrew page)', hs['sw'] <= hs['cw'], hs)
        page.screenshot(path=str(OUT / f'page-he-{tag}.png'), full_page=True)
        check(tag + ' no console errors (Hebrew page)', not errs, errs)
        # ---- the Hebrew surface with no city vs the live v3 (the live file served in place of the copy)
        page2 = ctx.new_page()
        page2.route('**/round-e/mquick.js', lambda r: r.fulfill(status=200, content_type='application/javascript', body=LIVE_MQUICK))
        page2.goto(BASE, wait_until='networkidle'); page2.wait_for_selector('#nlmq .nlmq__fig bdi')
        page.goto(BASE, wait_until='networkidle'); page.wait_for_selector('#nlmq .nlmq__fig bdi')
        a1 = page.locator('#nlmq').inner_text(); a2 = page2.locator('#nlmq').inner_text()
        check(tag + ' amount mode: text identical to live v3', a1 == a2)
        b1 = page.locator('#nlmq').screenshot(); b2 = page2.locator('#nlmq').screenshot()
        check(tag + ' amount mode: pixels identical to live v3', b1 == b2)
        page.locator('#nlmq button[data-m="price"]').click(); page2.locator('#nlmq button[data-m="price"]').click()
        p1 = page.evaluate('() => { const c = document.querySelector("#nlmq").cloneNode(true); const x = c.querySelector(".nlmq__city"); x && x.remove(); return c.innerHTML; }')
        p2 = page2.evaluate('() => document.querySelector("#nlmq").innerHTML')
        check(tag + ' price mode without the city block: DOM identical to live v3', p1 == p2)
        page2.close(); ctx.close()

    # ---- English mount
    for W, H in ((390, 844), (1280, 800)):
        tag = str(W)
        ctx = br.new_context(viewport={'width': W, 'height': H}); page = ctx.new_page(); errs = []
        page.on('console', lambda m, errs=errs: errs.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
        page.goto(BASE + '?lang=en', wait_until='networkidle'); page.wait_for_selector('#nlmq .nlmq__fig bdi')
        q = page.locator('#nlmq')
        check(tag + ' EN: lang en, ltr', q.get_attribute('lang') == 'en' and q.get_attribute('dir') == 'ltr')
        q.locator('button[data-m="price"]').click()
        lab = page.locator('label[for="nlmq-c"]').inner_text()
        opts = page.eval_on_selector_all('#nlmq-c option', 'os => os.map(o => o.textContent)')
        check(tag + ' EN: label and options in English, sorted', lab == 'City (median price, 4 rooms)' and opts[:4] == ['Choose a city', 'All of Israel', 'Ashdod', 'Ashkelon'] and opts[-1] == 'Yavne', opts[:4] + opts[-1:])
        page.select_option('#nlmq-c', 'תל אביב יפו')
        cq = page.locator('#nlmq .nlmq__cq').inner_text(); fig = q.locator('.nlmq__fig').inner_text()
        check(tag + ' EN: Tel Aviv-Yafo fills 5,229,800, Q1 2026', page.input_value('#nlmq-p') == '5,229,800' and cq == 'Median, Q1 2026, Israel Tax Authority' and '₪26,218' in fig, [page.input_value('#nlmq-p'), cq, fig])
        heb = page.evaluate('() => (document.querySelector("#nlmq").innerText.match(/[\\u0590-\\u05FF]/g) || []).length')
        check(tag + ' EN: no Hebrew letters in the tool', heb == 0, heb)
        check(tag + ' EN: controls >= 44 px', not small_controls(page, '#nlmq'), small_controls(page, '#nlmq'))
        hs = no_hscroll(page); check(tag + ' EN: no horizontal scroll', hs['sw'] <= hs['cw'], hs)
        q.screenshot(path=str(OUT / f'mquick-en-city-tlv-{tag}.png'))
        check(tag + ' EN: no console errors', not errs, errs)
        ctx.close()

    # ---- the live theme stylesheets (read only) over the select, phone
    ctx = br.new_context(viewport={'width': 390, 'height': 844}); page = ctx.new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.goto(BASE + '?theme=1', wait_until='networkidle'); page.wait_for_selector('#nlmq .nlmq__fig bdi')
    page.locator('#nlmq button[data-m="price"]').click(); page.select_option('#nlmq-c', 'חיפה')
    sh = page.evaluate('() => { const s = document.querySelector("#nlmq-c"); const cs = getComputedStyle(s); return {box: s.parentNode.getBoundingClientRect().height, h: s.getBoundingClientRect().height, fs: cs.fontSize, ff: cs.fontFamily.slice(0, 30), bw: cs.borderTopWidth}; }')
    check('theme: the select keeps 16 px, no own border, box >= 44 px', sh['fs'] == '16px' and sh['bw'] == '0px' and sh['box'] >= 44, sh)
    check('theme: Haifa 1,597,500', page.input_value('#nlmq-p') == '1,597,500')
    page.locator('#nlmq').screenshot(path=str(OUT / 'mquick-he-city-haifa-theme-390.png'))
    page.locator('#pv-exit').get_by_role('button', name='משכנתא שכבר יש לי').click()
    page.wait_for_selector('#pv-exit h3.mrx__h:has-text("האם למחזר?")')
    page.locator('#pv-exit section.mrx__sec').filter(has_text='האם למחזר?').screenshot(path=str(OUT / 'mexit-refi-theme-390.png'))
    hs = no_hscroll(page); check('theme: no horizontal scroll', hs['sw'] <= hs['cw'], hs)
    check('theme: no page errors', not errs, errs)
    ctx.close(); br.close()

print(json.dumps({'checks': len(report), 'failed': fails, 'report': report}, ensure_ascii=False, indent=1))
sys.exit(1 if fails else 0)
