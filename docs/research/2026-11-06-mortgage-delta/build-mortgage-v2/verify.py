"""Round M (HAD-675, 6.11.2026): Mortgage 2.0 v2 in a real browser. python verify.py

Serves the repo root on 127.0.0.1:47963 (stopped at the end), opens preview.html (the edited tools/mortgage.js) and preview-orig.html
(orig-mortgage.js, the live v1) in Chrome headless (Playwright, channel="chrome"), on a phone (390x844) and a desktop (1280x900):
- the default state of v1 and v2 is the same: every v1 block of the results, the moat, the schedule and the case link;
- C1 the band line under each rate field (3 in the default mix, none on the eligibility loan), the numbers of by_bank latest;
- C2 the frequency select on the variable track only; the same payments with no shock; the +2% at month 25 every two years;
  the choice in the results, the copied text and the track name;
- C3 months: 250 months gives 250 schedule rows; 30 months is refused with the 48 to 360 message;
- C5 the CSV download: BOM, one row per month plus the header, the header names;
- C9 three scenario cards; C14 the basket button and four cards, equal to NLMR (mexit) math in the page;
- no console errors, no horizontal scroll, every new control at least 44 px high and labelled.
Screenshots go to shots/. The English page /en/mortgage-calculator/ does not mount this tool (it mounts mquick only), so there is no
English mount to shoot; the check is recorded below from the saved public source snapshot."""
import json, os, re, socket, subprocess, sys, time, glob
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PORT = 47963
BASE = 'http://127.0.0.1:%d/docs/research/2026-11-06-mortgage-delta/build-mortgage-v2/' % PORT
SHOTS = os.path.join(HERE, 'shots'); os.makedirs(SHOTS, exist_ok=True)
RES = []


def check(name, cond, info=''):
    RES.append((bool(cond), name, info))
    print(('OK   ' if cond else 'FAIL ') + name + (('  [' + str(info) + ']') if info != '' else ''), flush=True)


def wait_port(port, t=15):
    end = time.time() + t
    while time.time() < end:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.2)
    return False


V1_BLOCKS = """() => { const r = document.querySelector('[data-nli="mortgage"]'), q = s => [...r.querySelectorAll(s)].map(e => e.innerText).join('\\n#\\n');
  const out = r.querySelector('.nlm__out');
  return { answer: q('.nlm__out .nli__answer'), lines: q('.nlm__out .nli__lines'), status: q('.nlm__out .nlm__status'), stress: q('.nlm__out .nlm__stress'),
    rules: q('.nlm__out .nlm__rules'), legend: q('.nlm__out .nli__legend'), moat: q('#bank-offer-check .nlm__verdict') + q('#bank-offer-check .nlm__place'),
    sched: r.querySelector('.nlm__sched table') ? r.querySelector('.nlm__sched table').innerText : '', charts: q('.nlm__chart svg[aria-label]') + [...r.querySelectorAll('.nlm__chart svg')].map(s => s.getAttribute('aria-label')).join('|'),
    formula: q('.nli__formula'), strip: q('.nli__strip'), hints: [...r.querySelectorAll('.nlm__row p.nlm__hint:not(.nlm__band)')].map(e => e.innerText).join('|'),
    link: window.NLMG.ui.link().split('#')[1], R: (({ first, highest, highestMonth, totalPaid, totalInterest, totalLinkage, N }) => ({ first, highest, highestMonth, totalPaid, totalInterest, totalLinkage, N }))(window.NLMG.ui.last().R) }; }"""

HSCROLL = "() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth })"

NEW_CONTROLS = """() => { const r = document.querySelector('[data-nli="mortgage"]'), out = [];
  const lab = e => (e.labels && e.labels.length ? [...e.labels].map(l => l.innerText).join(' ') : '') || e.getAttribute('aria-label') || e.innerText || '';
  const add = (kind, e) => { const b = e.getBoundingClientRect(); out.push({ kind, h: Math.round(b.height * 10) / 10, w: Math.round(b.width), label: lab(e).trim().slice(0, 60), vis: b.height > 0 }); };
  r.querySelectorAll('.nlm__form .nli__seg').forEach(g => { if (/התקופה/.test(g.getAttribute('aria-label') || '')) g.querySelectorAll('button').forEach(b => add('term toggle', b)); });
  r.querySelectorAll('.nlm__rg select').forEach(s => { if (s.labels && s.labels[0] && /תדירות/.test(s.labels[0].innerText)) add('frequency select', s); });
  r.querySelectorAll('.nlm__bk .nlm__btns button').forEach(b => add('baskets button', b));
  r.querySelectorAll('.nli__share button').forEach(b => { if (/CSV/.test(b.innerText)) add('csv button (share bar)', b); });
  return out; }"""


def wait_tool(page):
    page.wait_for_selector('[data-nli="mortgage"] .nlm__out .nli__answer', timeout=20000)
    page.wait_for_timeout(400)


def settle(page):
    page.wait_for_timeout(350)


def run_viewport(pw, browser, name, vp, mobile):
    ctx = browser.new_context(viewport=vp, device_scale_factor=2 if mobile else 1, is_mobile=mobile, has_touch=mobile, accept_downloads=True, locale='he-IL')
    errs = []
    page = ctx.new_page()
    page.on('console', lambda m: errs.append(('console', m.text)) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errs.append(('pageerror', str(e))))
    page.on('response', lambda r: errs.append(('http %d' % r.status, r.url)) if r.status >= 400 else None)
    # v1 (the live file) first, for the identity check
    page.goto(BASE + 'preview-orig.html'); wait_tool(page)
    v1 = page.evaluate(V1_BLOCKS)
    page.goto(BASE + 'preview.html'); wait_tool(page)
    v2 = page.evaluate(V1_BLOCKS)
    diff = [k for k in v1 if v1[k] != v2[k]]
    check(name + ': default state, every v1 block and the case link identical to the live v1', not diff, ','.join(diff) or '%d blocks' % len(v1))
    check(name + ': default numbers identical (first, highest, total, interest, linkage, months)', v1['R'] == v2['R'], json.dumps(v2['R']))
    page.screenshot(path=os.path.join(SHOTS, name + '-01-default-top.png'))
    page.locator('[data-nli="mortgage"] .nlm__out').screenshot(path=os.path.join(SHOTS, name + '-02-default-results.png'))
    hs = page.evaluate(HSCROLL); check(name + ': no horizontal scroll (default)', hs['sw'] <= hs['cw'], hs)

    # C1 the band
    bands = page.locator('[data-nli="mortgage"] p.nlm__band')
    bt = bands.all_inner_texts()
    d = json.load(open(os.path.join(ROOT, 'plugins', 'nadlan-config', 'assets', 'instruments', 'data', 'boi-mortgage.json'), encoding='utf-8'))
    tab = [x for x in d['by_bank']['latest']['table'] if x['bank'] != 'system']
    lo = min(x['fixed_nl']['rate'] for x in tab); hi = max(x['fixed_nl']['rate'] for x in tab)
    eff = lambda e: '%.2f%%' % e
    check(name + ': C1 one band line under each of the 3 rate fields', len(bt) == 3, len(bt))
    check(name + ': C1 track 1 line: month in Hebrew, source, the 7 banks, effective min and max of by_bank', bt and 'ספטמבר 2026' in bt[0] and 'קו המשווה של בנק ישראל' in bt[0] and '7 הבנקים' in bt[0] and eff(lo) in bt[0] and eff(hi) in bt[0], bt[0] if bt else '')
    page.locator('[data-nli="mortgage"] .nlm__row').first.screenshot(path=os.path.join(SHOTS, name + '-03-c1-band-track1.png'))
    # the eligibility loan: no band line
    page.locator('[data-nli="mortgage"] .nlm__row').nth(1).locator('select').first.select_option('zakaut'); settle(page)
    check(name + ': C1 no band line on the eligibility loan', page.locator('[data-nli="mortgage"] .nlm__row').nth(1).locator('p.nlm__band').count() == 0)
    page.locator('[data-nli="mortgage"] .nlm__row').nth(1).locator('select').first.select_option('prime'); settle(page)

    # C2 the frequency
    fs = page.get_by_label('תדירות שינוי הריבית')
    check(name + ': C2 the frequency select only on the variable track (1 of 3)', fs.count() == 1, fs.count())
    opts = fs.first.locator('option').all_inner_texts()
    check(name + ': C2 five frequencies, five years chosen', opts == ['כל שנה', 'כל שנתיים', 'כל 2.5 שנים', 'כל 5 שנים', 'כל 10 שנים'] and fs.first.input_value() == '60', ' | '.join(opts))
    t60 = page.evaluate("() => { const R = NLMG.ui.last().R; return [R.first, R.highest, R.totalPaid]; }")
    fs.first.select_option('24'); settle(page)
    t24 = page.evaluate("() => { const R = NLMG.ui.last().R; return [R.first, R.highest, R.totalPaid]; }")
    check(name + ': C2 every 2 years, no shock: the same payments as every 5 years', t60 == t24, t24)
    lines = page.locator('[data-nli="mortgage"] .nlm__out .nli__lines').first.inner_text()
    legend = page.locator('[data-nli="mortgage"] .nlm__out .nli__legend').first.inner_text()
    check(name + ': C2 the choice is in the results (line and track name)', 'תדירות שינוי הריבית, מסלול 3' in lines and 'כל שנתיים' in lines and 'משתנה כל שנתיים, צמודה' in legend)
    page.get_by_role('button', name=re.compile('^עלייה של 2%')).first.click(); settle(page)
    ch = page.evaluate("() => { const S = NLMG.ui.last().R.T[2], out = []; for (let m = 1; m < S.rate.length; m++) if (Math.abs(S.rate[m] - S.rate[m - 1]) > 1e-9) out.push(m + 1); return out; }")
    check(name + ': C2 with the +2% path the variable track changes at month 25 only', ch == [25], ch)
    copied = page.evaluate("() => { const b = [...document.querySelectorAll('.nli__share button')].find(x => /העתקת/.test(x.innerText)); let got = null; const w = navigator.clipboard; try { Object.defineProperty(navigator, 'clipboard', { value: { writeText: t => { got = t; return Promise.resolve(); } }, configurable: true }); } catch (e) {} b.click(); return got; }")
    check(name + ': C2 the choice is in the copied text', bool(copied) and 'שינוי הריבית במסלול המשתנה: מסלול 3 כל שנתיים' in copied, (copied or '')[:140])
    page.locator('[data-nli="mortgage"] .nlm__row').nth(2).screenshot(path=os.path.join(SHOTS, name + '-04-c2-frequency-track3.png'))
    page.get_by_role('button', name='ללא שינוי', exact=True).first.click(); fs.first.select_option('60'); settle(page)

    # C3 months
    page.get_by_role('button', name='בחודשים', exact=True).first.click(); settle(page)
    mf = page.get_by_label('חודשים', exact=True)
    check(name + ': C3 the term in months, 300 in each of 3 tracks', mf.count() == 3 and mf.first.input_value() == '300', mf.count())
    mf.first.fill('250'); settle(page)
    n0 = page.evaluate("() => [NLMG.ui.last().R.T[0].N, NLMG.ui.last().R.N]")
    page.locator('[data-nli="mortgage"] details.nlm__sched summary').click()
    page.locator('[data-nli="mortgage"] details.nlm__sched button.nlm__link').first.click(); settle(page)
    rows = page.locator('[data-nli="mortgage"] details.nlm__sched tbody tr').count()
    t1 = page.evaluate("() => { const S = NLMG.ui.last().R.T[0]; return [S.pay[249] > 0, S.bal[249]]; }")
    check(name + ': C3 250 months on track 1: 250 monthly payments, paid off at month 250, schedule 300 rows (the longest track)', n0 == [250, 300] and t1 == [True, 0] and rows == 300, '%s rows %d' % (n0, rows))
    page.locator('[data-nli="mortgage"] .nlm__row').first.screenshot(path=os.path.join(SHOTS, name + '-05-c3-months-track1.png'))
    mf.first.fill('30'); settle(page)
    msg = page.locator('[data-nli="mortgage"] .nlm__out .nli__note').all_inner_texts()
    check(name + ': C3 30 months refused with the 48 to 360 message', any('בין 48 ל־360 חודשים' in m for m in msg), msg[:1])
    mf.first.fill('300'); settle(page)
    page.locator('[data-nli="mortgage"] details.nlm__sched button.nlm__link').first.click(); settle(page)
    page.get_by_role('button', name='בשנים', exact=True).first.click(); settle(page)
    back = page.evaluate("() => { const R = NLMG.ui.last().R; return [R.first, R.highest, R.totalPaid]; }")
    check(name + ': C3 back to 300 months and years: the default numbers again', back == t60, back)

    # C5 the CSV
    with page.expect_download() as dl:
        page.locator('[data-nli="mortgage"] .nli__share button', has_text='CSV').click()
    f = dl.value; p = os.path.join(HERE, 'sample-schedule-%s.csv' % name); f.save_as(p)
    raw = open(p, 'rb').read(); txt = raw.decode('utf-8-sig'); ls = [l for l in txt.split('\r\n') if l]
    head = ls[0].split(',') if ls else []
    N = page.evaluate("() => NLMG.ui.last().R.N")
    check(name + ': C5 the download: UTF-8 BOM, one row per month plus the header, 21 columns', raw[:3] == b'\xef\xbb\xbf' and len(ls) == N + 1 and len(head) == 21 and f.suggested_filename == 'mortgage-schedule.csv',
          '%s, %d rows, %d columns' % (f.suggested_filename, len(ls), len(head)))
    check(name + ': C5 header names', head[:2] == ['חודש', 'מסלול 1 קל״צ: תשלום'] and head[-1] == 'סך הכול: יתרה', ' | '.join(head[:3] + head[-2:]))
    page.locator('[data-nli="mortgage"] .nli__share').screenshot(path=os.path.join(SHOTS, name + '-06-c5-share-bar.png'))
    check(name + ': C5 the schedule section has the same download', page.locator('[data-nli="mortgage"] details.nlm__sched button.nlm__csv').count() == 1)

    # C9 three scenarios
    cards = page.locator('[data-nli="mortgage"] .nlm__three .nlm__sc')
    ct = cards.all_inner_texts()
    check(name + ': C9 three scenario cards: today, BoI forecast, stress, each with first, highest and its year, total', len(ct) == 3 and 'היום' in ct[0] and 'תחזית בנק ישראל' in ct[1] and 'תרחיש מחמיר' in ct[2] and all('ההחזר הראשון' in c and 'ההחזר הגבוה' in c and 'שנה' in c and 'סך כל התשלומים' in c for c in ct))
    s3 = page.evaluate("() => { const L = NLMG.ui.last(); return [L.s3.stress.totalPaid === L.st2.totalPaid, L.s3.today.totalPaid === L.base.totalPaid]; }")
    check(name + ': C9 the stress card is the existing +2% check, today is the default result', s3 == [True, True], s3)
    page.locator('[data-nli="mortgage"] .nlm__three').screenshot(path=os.path.join(SHOTS, name + '-07-c9-three-scenarios.png'))
    fit = page.evaluate("""() => [...document.querySelectorAll('.nlm__three .nlm__sc strong')].map(e => { const b = e.getBoundingClientRect(), c = e.closest('.nlm__sc').getBoundingClientRect(), lh = parseFloat(getComputedStyle(e).lineHeight) || 19;
      return { one: b.height <= lh * 1.3, inside: b.left >= c.left - 0.5 && b.right <= c.right + 0.5, t: e.innerText }; })""")
    check(name + ': C9 every amount on one line and inside its card', fit and all(x['one'] and x['inside'] for x in fit), [x['t'] for x in fit if not (x['one'] and x['inside'])] or len(fit))
    rows_top = page.evaluate("""() => [...document.querySelectorAll('.nlm__three .nlm__sc')].map(c => [...c.querySelectorAll('.nlm__scr')].map(r => Math.round(r.getBoundingClientRect().top)))""")
    check(name + ': C9 the three cards keep their value rows on the same lines', len(rows_top) == 3 and rows_top[0] == rows_top[1] == rows_top[2], rows_top)

    # C14 the baskets
    bb = page.get_by_role('button', name='הסלים האחידים לסכום שלי')
    check(name + ': C14 the button is there, closed', bb.count() == 1 and bb.get_attribute('aria-pressed') == 'false')
    bb.click(); settle(page)
    k4 = page.locator('[data-nli="mortgage"] .nlm__bk .nlm__sc').all_inner_texts()
    check(name + ': C14 four cards: your mix and the three uniform baskets', len(k4) == 4 and 'התמהיל שלכם' in k4[0] and 'סל אחיד 1' in k4[1] and 'סל אחיד 3' in k4[3])
    cmp = page.evaluate("() => NLMG.ui.last().bk.map(b => b.R.totalPaid)")
    eqn = page.evaluate("""async () => { const D = await fetch('/plugins/nadlan-config/assets/instruments/data/boi-mortgage.json').then(r => r.json()), L = NLMG.ui.last(), v = NLMG.ui.state();
      const BACK = { fixed_nl: 'fixed_nl', prime: 'prime', var_cpi: 'var5_cpi', var_nl_other: 'var5_nl', fixed_cpi: 'fixed_cpi' };
      const rateOf = k => { const r = v.rows.find(x => x.track === BACK[k]); return r ? r.rate : D.tracks[BACK[k]].rate; };
      return L.bk.map(b => { const M = NLMG.mix(NLMR.mathRows(NLMR.basketRows(D, D.baskets.list.find(x => x.k === b.k), rateOf), L.R0.loan, v.rows[0].years), L.sc);
        return Math.abs(M.totalPaid - b.R.totalPaid) < 1e-4 && Math.abs(M.first - b.R.first) < 1e-6 && Math.abs(M.highest - b.R.highest) < 1e-6; }); }""")
    check(name + ': C14 every basket equals the mexit basket math (NLMR) in the page', eqn == [True, True, True], [round(x) for x in cmp])
    page.locator('[data-nli="mortgage"] .nlm__bk').screenshot(path=os.path.join(SHOTS, name + '-08-c14-baskets.png'))
    hs = page.evaluate(HSCROLL); check(name + ': no horizontal scroll (baskets open, months used)', hs['sw'] <= hs['cw'], hs)

    # the case link carries the months and the frequency (written only when used)
    page.get_by_role('button', name='בחודשים', exact=True).first.click(); settle(page)
    page.get_by_label('תדירות שינוי הריבית').first.select_option('24'); settle(page)
    link = page.evaluate("() => NLMG.ui.link()"); want = page.evaluate("() => NLMG.ui.last().R.totalPaid")
    p2 = ctx.new_page(); p2.goto(BASE + 'preview.html#' + link.split('#')[1]); wait_tool(p2)
    got = p2.evaluate("() => { const v = NLMG.ui.state(); return [v.termUnit, v.rows[2].freq, NLMG.ui.last().R.totalPaid, document.querySelectorAll('[data-nli=mortgage] .nlm__fq select').length]; }")
    check(name + ': the case link reopens months and every 2 years', got[:2] == ['m', 24] and abs(got[2] - want) < 1e-6 and got[3] == 1, got)
    p2.close()
    page.get_by_label('תדירות שינוי הריבית').first.select_option('60'); page.get_by_role('button', name='בשנים', exact=True).first.click(); settle(page)
    # controls: size and labels
    ctl = page.evaluate(NEW_CONTROLS)
    small = [c for c in ctl if c['h'] < 44 or not c['label']]
    check(name + ': every new control at least 44 px and labelled (%d controls)' % len(ctl), len(ctl) >= 5 and not small, small or ', '.join('%s %.0fpx' % (c['kind'], c['h']) for c in ctl))
    csvl = page.evaluate("() => { const b = document.querySelector('.nlm__sched button.nlm__csv'); return b.getBoundingClientRect().height; }")
    check(name + ': the schedule CSV link is at least 44 px', csvl >= 44, csvl)
    bad = [e for e in errs]
    check(name + ': no console errors', not bad, bad[:3])
    ctx.close()


def main():
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not wait_port(PORT):
            print('server did not start'); return 2
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel='chrome', headless=True)
            run_viewport(pw, browser, 'phone-390', {'width': 390, 'height': 844}, True)
            run_viewport(pw, browser, 'desktop-1280', {'width': 1280, 'height': 900}, False)
            browser.close()
    finally:
        srv.terminate()
        try: srv.wait(5)
        except Exception: srv.kill()
    # the English page: which tools it mounts (saved public source, latest snapshot)
    snaps = sorted(glob.glob(os.path.join(ROOT, 'docs', 'source-snapshots', 'en-mortgage-calculator', '*.html')))
    if snaps:
        h = open(snaps[-1], encoding='utf-8', errors='replace').read()
        ids = sorted(set(re.findall(r'data-nli="([a-z0-9-]+)"', h)))
        check('English page /en/mortgage-calculator/ does not mount Mortgage 2.0 (snapshot %s): %s' % (os.path.basename(snaps[-1]), ','.join(ids)), 'mortgage' not in ids)
    okc = sum(1 for r in RES if r[0])
    print('\n%d/%d passed' % (okc, len(RES)))
    json.dump([{'ok': r[0], 'check': r[1], 'info': str(r[2])} for r in RES], open(os.path.join(HERE, 'verify-results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return 0 if okc == len(RES) else 1


if __name__ == '__main__':
    sys.exit(main())
