"""HAD-675 mcheck: press the tool of preview.html in headless Chrome (Playwright, channel chrome) at 390x844 and 1280x900.
Starts `python -m http.server 47971 --bind 127.0.0.1` from the repo root in the background and stops it at the end.
Writes screenshots into build-mcheck/screens and verify.json, prints a summary. Exit 1 on any failed check.
Checks at every step: no console error, no horizontal scroll, every control of the tool at least 44 px tall (buttons, selects,
input boxes, summaries, the advisor link; inline text links inside sentences are not controls), every input and select labelled,
no long dash, no recommendation word, no "0 ₪" for a value nobody typed."""
import json, re, subprocess, sys, time, pathlib, urllib.request
from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[4]
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'screens'
OUT.mkdir(parents=True, exist_ok=True)
PORT = 47971
BASE = f'http://127.0.0.1:{PORT}/docs/research/2026-11-06-mortgage-delta/build-mcheck/preview.html'
TOOL = '#pv-check'

report, fails = [], []
def check(name, cond, got=None):
    report.append({'check': name, 'ok': bool(cond), 'got': got})
    if not cond: fails.append(name)
    print(('  ok   ' if cond else '  FAIL ') + name + ('' if got is None else '  [' + str(got)[:160] + ']'))

JS_SMALL = '''(scope) => { const r = document.querySelector(scope); if (!r) return ['no scope']; const out = [];
  r.querySelectorAll('button, select, .nli__in, summary, a.nlc__go, .nli__share a').forEach(e => { const b = e.getBoundingClientRect();
    if (b.width > 0 && b.height > 0 && b.height < 43.5) out.push(e.tagName + '.' + (e.className || '') + ' "' + (e.textContent || '').trim().slice(0, 24) + '" ' + b.height.toFixed(1)); });
  return out; }'''
JS_UNLABELLED = '''(scope) => { const r = document.querySelector(scope); const out = [];
  r.querySelectorAll('input, select, textarea').forEach(e => { const b = e.getBoundingClientRect(); if (!(b.width > 0)) return;
    const lab = (e.id && document.querySelector('label[for="' + e.id + '"]')) || e.closest('label');
    const al = e.getAttribute('aria-label') || e.getAttribute('aria-labelledby');
    if (!(lab && lab.textContent.trim()) && !al) out.push(e.outerHTML.slice(0, 80)); });
  r.querySelectorAll('button').forEach(e => { const b = e.getBoundingClientRect(); if (b.width > 0 && !(e.textContent.trim() || e.getAttribute('aria-label'))) out.push(e.outerHTML.slice(0, 80)); });
  return out; }'''
JS_HSCROLL = '() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth})'

def text_rules(page, tag, step, zero_check=True):
    t = page.locator(TOOL).inner_text()
    check(f'{tag} {step}: no long dash', not re.search('[–—]', t))
    check(f'{tag} {step}: no recommendation word', not re.search('כדאי|המלצה|מומלץ|ממליצ|עדיף', t))
    if zero_check:
        m = re.search(r'(^|[^\d.,])0 ₪|₪\s?0(?![\d.,])', t)
        check(f'{tag} {step}: no "0 ₪" for an untyped value', not m, m and m.group(0))
    return t

def layout(page, tag, step):
    hs = page.evaluate(JS_HSCROLL)
    check(f'{tag} {step}: no horizontal scroll', hs['sw'] <= hs['cw'], hs)
    sm = page.evaluate(JS_SMALL, TOOL)
    check(f'{tag} {step}: every control >= 44 px', not sm, sm[:6])
    ul = page.evaluate(JS_UNLABELLED, TOOL)
    check(f'{tag} {step}: every input labelled', not ul, ul[:4])

def shot(loc, name):
    loc.screenshot(path=str(OUT / name))

def seg(page, group, name):
    page.locator(f'{TOOL} [role="group"][aria-label="{group}"]').get_by_role('button', name=name, exact=True).click()

srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1'], cwd=str(REPO), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try: urllib.request.urlopen(BASE, timeout=1); break
        except Exception: time.sleep(0.2)
    with sync_playwright() as p:
        br = p.chromium.launch(channel='chrome', headless=True)
        for W, H in ((390, 844), (1280, 900)):
            tag = str(W)
            print(f'\n== {W}x{H}')
            ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, locale='he-IL')
            ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin=f'http://127.0.0.1:{PORT}')
            page = ctx.new_page(); errs = []
            page.on('console', lambda m, errs=errs: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e, errs=errs: errs.append('pageerror: ' + str(e)))
            page.goto(BASE, wait_until='networkidle')
            page.wait_for_selector(f'{TOOL} .nlc__empty')
            T = page.locator(TOOL)
            # ---- 1. the empty state
            check(f'{tag} empty: the guide shows and no flag', T.locator('.nlc__empty').is_visible() and T.locator('li.nlc__fl').count() == 0)
            text_rules(page, tag, 'empty'); layout(page, tag, 'empty')
            shot(T, f'01-empty-{tag}.png')
            # ---- 2. the example (the 9.2026 averages)
            T.get_by_role('button', name=re.compile('^מילוי דוגמה')).click()
            page.wait_for_selector(f'{TOOL} .nlc__score')
            sc = [int(x) for x in T.locator('.nlc__sc b').all_inner_texts()]
            check(f'{tag} example: 0 red, 2 to check', sc[0] == 0 and sc[1] == 2, sc)
            check(f'{tag} example: marked as an example', 'דוגמה, שנו כל שדה' in T.locator('.nlc__al').inner_text())
            summ = T.locator('p.nlc__sum').inner_text()
            n_sent = len([s for s in re.split(r'(?<=\.)\s', summ.strip()) if s])
            check(f'{tag} example: summary of 5 to 8 sentences', 5 <= n_sent <= 8, n_sent)
            check(f'{tag} example: validity 19 days shown prominently', 'נשארו 19 ימים' in T.locator('p.nlc__valid').inner_text() or 'נשארו' in T.locator('p.nlc__valid').inner_text(), T.locator('p.nlc__valid').inner_text())
            check(f'{tag} example: first payment 6,511 in the basket field', page.get_by_label('החזר חודשי ראשון (שורה 8)').input_value() == '6,511')
            ex_text = text_rules(page, tag, 'example'); layout(page, tag, 'example')
            shot(T, f'02-example-{tag}.png')
            shot(T.locator('.nlc__out'), f'03-example-result-{tag}.png')
            shot(T.locator('section.nlc__grp.is-amber'), f'04-group-amber-{tag}.png')
            info = T.locator('details.nlc__grp.is-info'); info.locator('summary').click()
            check(f'{tag} info group opens', info.get_attribute('open') is not None)
            shot(info, f'05-group-info-{tag}.png')
            qw = T.locator('section.nlc__qw')
            check(f'{tag} questions: at least 8, generated from the flags', qw.locator('li').count() >= 8, qw.locator('li').count())
            shot(qw, f'06-questions-{tag}.png')
            # copy: the result text and the case link
            T.locator('.nli__share').get_by_role('button', name='העתקת התוצאה').click(); page.wait_for_timeout(200)
            clip = page.evaluate('() => navigator.clipboard.readText()')
            check(f'{tag} copy: summary, flags and questions copied', 'מה לשאול את הבנק:' in clip and 'אינה ייעוץ' in clip and 'לבדיקה מול הבנק:' in clip, len(clip))
            T.locator('.nli__share').get_by_role('button', name='קישור למקרה הזה').click(); page.wait_for_timeout(200)
            link = page.evaluate('() => navigator.clipboard.readText()')
            check(f'{tag} case link: the state in the hash only', '#mcheck=' in link and '?' not in link.split('#')[0], link[:90])
            # ---- 3. basket switcher and all rows
            T.get_by_role('tab', name='סל 2').click()
            check(f'{tag} basket switcher: basket 2 shows its definition', 'שליש' in T.locator('p.nlc__def').inner_text(), T.locator('p.nlc__def').inner_text())
            T.get_by_role('tab', name='סל מוצע').click()
            T.locator('button.nlc__tog').click()
            page.wait_for_selector(f'{TOOL} .nlc__tr')
            check(f'{tag} all rows: 5 tracks in the proposed basket', T.locator('.nlc__tr').count() == 5, T.locator('.nlc__tr').count())
            layout(page, tag, 'all rows')
            shot(T.locator('form.nli__form'), f'07-form-all-rows-{tag}.png')
            # ---- 4. a red case: expired, over the LTV cap, guarantors, a reservation fee
            d = page.get_by_label('תאריך האישור'); d.fill('1.10.2026')
            page.get_by_label('סך ההלוואה המבוקשת').fill('1,300,000')
            seg(page, 'האם נדרשים ערבים להלוואה', 'כן')
            seg(page, 'האם בחיובים מופיעים דמי שריון או תשלום על אופציה לקבלת הלוואה', 'כן')
            page.wait_for_timeout(400)
            sc = [int(x) for x in T.locator('.nlc__sc b').all_inner_texts()]
            red = T.locator('section.nlc__grp.is-red')
            rt = red.inner_text()
            check(f'{tag} red case: expired, LTV, totals, reservation fee', sc[0] >= 4 and 'תוקף האישור עבר' in rt and 'שיעור המימון מעל המגבלה' in rt and 'דמי שריון' in rt, sc)
            check(f'{tag} red case: guarantors to check', 'נדרשים ערבים' in T.locator('section.nlc__grp.is-amber').inner_text())
            check(f'{tag} red case: the validity strip is red', 'is-red' in (T.locator('p.nlc__valid').get_attribute('class') or ''))
            text_rules(page, tag, 'red case'); layout(page, tag, 'red case')
            red.scroll_into_view_if_needed()
            shot(red, f'08-group-red-{tag}.png')
            shot(T.locator('.nlc__out'), f'09-red-result-{tag}.png')
            # ---- 5. mode 2: the final documents against the approval
            T.get_by_role('button', name='מילוי דוגמה, ממוצעי 9.2026').click(); page.wait_for_timeout(200)
            seg(page, 'מה בודקים', 'המסמכים לפני החתימה')
            T.get_by_role('button', name=re.compile('^העתקה מהסל המוצע')).click(); page.wait_for_timeout(300)
            check(f'{tag} mode 2: a copy of the proposed basket shows no change', 'לא נמצאו שינויים' in T.locator('.nlc__out').inner_text())
            page.get_by_label('מסלול 1: ריבית שנתית (שורה 5)').fill('4.9')
            page.get_by_label('תאריך המסמכים').fill('28.11.2026')
            seg(page, 'דרישת ביטוח שלא הופיעה באישור', 'יש')
            page.wait_for_timeout(400)
            o2 = T.locator('.nlc__out').inner_text()
            check(f'{tag} mode 2: rate up, new insurance, after the hold', 'הריבית עלתה' in o2 and 'דרישת ביטוח חדשה' in o2 and 'אחרי תקופת השמירה' in o2)
            text_rules(page, tag, 'mode 2'); layout(page, tag, 'mode 2')
            shot(T, f'10-mode2-diff-{tag}.png')
            # ---- 6. print: the form hidden, the result kept
            page.emulate_media(media='print')
            check(f'{tag} print: form hidden, flags kept', page.evaluate(f'() => getComputedStyle(document.querySelector("{TOOL} form.nli__form")).display') == 'none' and T.locator('li.nlc__fl').first.is_visible())
            page.emulate_media(media='screen')
            # ---- 7. the case link reopens the same numbers
            p2 = ctx.new_page(); e2 = []
            p2.on('pageerror', lambda e: e2.append(str(e)))
            p2.goto(link.replace('https://nad-lan.co.il/mortgage-calculator/', BASE), wait_until='networkidle'); p2.wait_for_selector(f'{TOOL} .nlc__score')
            check(f'{tag} case link: the same 0 red / 2 to check after reopening', [int(x) for x in p2.locator(f'{TOOL} .nlc__sc b').all_inner_texts()][:2] == [0, 2] and not e2)
            p2.close()
            check(f'{tag} no console errors', not errs, errs[:4])
            page.screenshot(path=str(OUT / f'11-page-{tag}.png'), full_page=True)
            ctx.close()

        # ---- the live theme stylesheets (read only) over the tool, phone
        print('\n== 390x844 with the live theme stylesheets')
        ctx = br.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1); page = ctx.new_page(); perr = []
        page.on('pageerror', lambda e: perr.append(str(e)))
        page.goto(BASE + '?theme=1', wait_until='networkidle'); page.wait_for_selector(f'{TOOL} .nlc__empty')
        T = page.locator(TOOL)
        T.get_by_role('button', name=re.compile('^מילוי דוגמה')).click(); page.wait_for_selector(f'{TOOL} .nlc__score')
        st = page.evaluate(f'''() => {{ const li = document.querySelector("{TOOL} li.nlc__fl"); const lg = document.querySelector("{TOOL} fieldset.nlc__fs > legend"); const tb = document.querySelector("{TOOL} .nlc__tabs button");
          return {{ liStyle: getComputedStyle(li).listStyleType, liBefore: getComputedStyle(li, '::before').content, lgFont: getComputedStyle(lg).fontFamily.slice(0, 22), tbH: tb.getBoundingClientRect().height }}; }}''')
        check('theme: list bullets off, legend in Plex Sans Hebrew, tabs >= 44 px', st['liStyle'] == 'none' and st['liBefore'] in ('none', 'normal') and 'Plex Sans Hebrew' in st['lgFont'] and st['tbH'] >= 44, st)
        layout(page, 'theme', 'example')
        shot(T, '12-theme-example-390.png')
        check('theme: no page errors', not perr, perr[:3])
        ctx.close(); br.close()
finally:
    srv.terminate()
    try: srv.wait(timeout=5)
    except Exception: srv.kill()

(HERE / 'verify.json').write_text(json.dumps({'checks': report, 'failed': fails}, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'\n{len(report) - len(fails)}/{len(report)} passed' + (f', {len(fails)} FAILED' if fails else '') + '; server stopped; screenshots in ' + str(OUT))
sys.exit(1 if fails else 0)
