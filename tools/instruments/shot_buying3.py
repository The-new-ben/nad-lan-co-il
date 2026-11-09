# -*- coding: utf-8 -*-
"""HAD-686: screenshots and pressed-control checks of the guide's reading layer and the five Phase 3 tools (build_buying3_harness.py
first).

    python tools/instruments/shot_buying3.py [plain]   -> docs/research/2026-11-08-buying-guide-re/shots-tools/*.png
    python tools/instruments/shot_buying3.py v3        -> the real page content (build_buying3_harness.py <page-9-v3.html> v3 first):
                                                          all 15 tools mount, the map wires every chapter, h3 kept, the glossary
                                                          filters, touch targets, no sideways scroll; shots v3-*.png

Phone 390 x 844 and desktop 1366 x 900, each in a fresh browser context. Before the page loads, the shared plan store holds a
signing date (as bdates now saves it), so bpay and breg must prefill it. For each width: page errors, sideways scroll, heading
levels (h3 inside a chapter, h2 outside, one h1), then presses: bpay (the design case, 15%, three validation errors, dates, reload,
print), bsign (ticks + reload + print), bkeys (readings, defects, a transfer, reload, print with signatures), breg (statuses, due
dates, reload), bmemo (high, mid, nothing kept after reload), the guide map (a jump does not mark, reading marks, reload keeps),
the glossary filter (count, quotes, clear), touch targets (44 px, 48 px on phones), visible focus, the phone table cards. Then
reduced motion and a no-JS render (the five server summaries, the full glossary). One line per check; exit 1 on a failure."""
import functools
import http.server
import os
import sys
import threading

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "docs", "research", "2026-11-08-buying-guide-re", "shots-tools")
os.makedirs(OUT, exist_ok=True)
MODE = sys.argv[1] if len(sys.argv) > 1 else ""
NAME = {"plain": "harness_buying3_plain.html", "v3": "harness_v3.html"}.get(MODE, "harness_buying3.html")


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47944), functools.partial(Q, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = "http://127.0.0.1:47944/tools/instruments/" + NAME
FAIL = []
READY = "document.querySelectorAll('[data-nli-on] .nlbh3').length === 5 && !!document.querySelector('.nlbg-gloss-find')"
SEED = "if (!sessionStorage.getItem('__seed')) { localStorage.setItem('nlbh-plan-v1', JSON.stringify({ sign: '2026-11-08' })); sessionStorage.setItem('__seed', '1'); }"


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info) if info not in ("", None) else ""))
    if not ok:
        FAIL.append(name)


OVER = """() => { const W = document.documentElement.clientWidth, out = [];
  document.querySelectorAll('.nlbp *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.right > W + 1 || r.left < -1)) {
    let p = e.parentElement, clip = false; while (p) { const s = getComputedStyle(p); if (/(auto|scroll|hidden)/.test(s.overflowX)) { clip = true; break; } p = p.parentElement; }
    if (!clip) out.push((e.className || e.tagName) + ' ' + Math.round(r.left) + '..' + Math.round(r.right)); } });
  return { sw: document.documentElement.scrollWidth, W, out: out.slice(0, 8) }; }"""

TARGETS = """(min) => { const bad = [];
  const sel = ['[data-nli-on] .nlbh3 button', '[data-nli-on] .nlbh3 .nli__share a', '[data-nli-on] .nlbh3 .nli__in', '[data-nli-on] .nlbh3 textarea', '[data-nli-on] .nlbh3 .nlbh3-chk label',
    '.nlbg-map .nlbg-map__chips a', '.nlbg-map__prog button', '.nlbg-gloss-find input', '.nlbg-back a', '.nlbg-todo__tool a'];
  sel.forEach(s => document.querySelectorAll(s).forEach(e => { const r = e.getBoundingClientRect(); if (r.width && r.height && r.height < min - 0.5) bad.push(s + ' "' + (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 18) + '" ' + Math.round(r.height)); }));
  return bad.slice(0, 10); }"""


HIDE = "[data-shot-fixed]{visibility:hidden !important}"  # element shots: the theme's fixed header and floating buttons would sit on top


def mark_fixed(pg):
    pg.evaluate("""() => document.querySelectorAll('body *').forEach(e => { if (e.closest('.nlbp')) return; const p = getComputedStyle(e).position; if (p === 'fixed' || p === 'sticky') e.setAttribute('data-shot-fixed', ''); })""")


def shot(loc, name):
    loc.screenshot(path=os.path.join(OUT, name), style=HIDE)


def ready(pg):
    pg.wait_for_function(READY, timeout=20000)
    pg.wait_for_timeout(400)
    mark_fixed(pg)


def to_chapter(pg, cid, share=0.75):
    """scroll so that `share` of the chapter has passed the middle of the screen, then wait for the idle mark"""
    pg.evaluate("""([id, s]) => { const e = document.getElementById(id), r = e.getBoundingClientRect(); window.scrollTo({ top: scrollY + r.top + s * r.height - innerHeight / 2, behavior: 'instant' }); }""", [cid, share])
    pg.wait_for_timeout(900)


def run(b, w, h, tag):
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if tag == "390" else 1, locale="he-IL")
    ctx.add_init_script(SEED)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: m.type == "error" and "favicon" not in m.text and errs.append(m.text))
    pg.goto(URL, wait_until="networkidle")
    ready(pg)
    own = [e for e in errs if "Access to font" not in e and ("127.0.0.1" in e or "nlbh" in e or "NLBH" in e or "nlbg" in e or "Uncaught" in e)]
    check(tag + " no page errors from our code", not own, own[:3])
    o = pg.evaluate(OVER)
    check(tag + " no sideways scroll", o["sw"] <= o["W"] and not o["out"], o)
    hv = pg.evaluate("() => ['bpay', 'bsign', 'breg', 'bmemo', 'bkeys'].map(i => { const t = document.querySelector('[data-nli=\"' + i + '\"] .nli__title'); return t ? t.tagName : '-'; })")
    check(tag + " heading levels after JS: h3 inside a chapter (bpay, bsign, breg, bmemo), h2 outside (bkeys)", hv == ["H3", "H3", "H3", "H3", "H2"], hv)
    check(tag + " exactly one h1", pg.locator("main h1").count() == 1, pg.locator("main h1").count())
    tf = pg.evaluate("() => { const t = document.querySelector('[data-nli=\"bpay\"] h3.nli__title'); const s = getComputedStyle(t); return [s.fontFamily.indexOf('Karantina') >= 0, parseFloat(s.fontSize)]; }")
    check(tag + " the h3 tool title keeps the instruments face", tf[0] and tf[1] >= 34, tf)

    # ---- the guide map: a jump through does not mark a chapter ----
    m = pg.locator("#nlbg-map")
    check(tag + " map: 16 chips, the 5 chapters on the page wired (dot + state)", m.locator("a[href^='#nlbg-c']").count() == 16 and m.locator("a .nlbg-vh").count() == 5 and m.locator("a i[aria-hidden='true']").count() == 5)
    pg.evaluate("() => { location.hash = '#nlbg-c15'; }")
    pg.wait_for_timeout(900)
    rd = pg.evaluate("() => [...document.querySelectorAll('section.nlbg-ch')].filter(s => s.classList.contains('is-read')).map(s => s.id)")
    check(tag + " map: a jump to chapter 15 does not mark the chapters it passed", "nlbg-c9" not in rd and "nlbg-c11" not in rd and "nlbg-c12" not in rd and "nlbg-c13" not in rd, rd)
    pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(500)
    to_chapter(pg, "nlbg-c13")
    st13 = pg.evaluate("() => [document.getElementById('nlbg-c13').classList.contains('is-read'), document.querySelector('a[href=\"#nlbg-c13\"]').classList.contains('is-read'), (document.querySelector('.nlbg-map a.is-now') || {}).getAttribute ? document.querySelector('.nlbg-map a.is-now').getAttribute('href') : null]")
    check(tag + " map: reading 75% of chapter 13 marks it read (chapter + chip) and its chip is current", st13[0] and st13[1] and st13[2] == "#nlbg-c13", st13)
    shot(pg.locator("#nlbg-c13"), f"{tag}-02-chapter13.png")
    vis = pg.evaluate("() => [...document.querySelectorAll('section.nlbg-ch')].every(s => getComputedStyle(s).display !== 'none' && s.offsetHeight > 100)")
    check(tag + " map: no chapter is hidden", vis)
    cards = pg.evaluate("() => { const t = document.querySelector('#nlbg-c13 table.nlbg-tbl'), th = getComputedStyle(t.querySelector('thead')).display, td = t.querySelector('tbody td'); return [th, getComputedStyle(td, '::before').content, getComputedStyle(t).display]; }")
    if tag == "390":
        check(tag + " table: phone rows are labelled cards (thead hidden, td label from data-l)", cards[0] == "none" and "איפה הדירה רשומה" in cards[1], cards)
    else:
        check(tag + " table: wide screens keep a real table", cards[0] == "table-header-group" and cards[2] == "table", cards)

    # ---- bpay ----
    p = pg.locator('[data-nli="bpay"]')
    inp = p.locator(".nlbh-form input")
    check(tag + " bpay: the signing date comes from the shared plan (bdates)", inp.nth(4).input_value() == "2026-11-08", inp.nth(4).input_value())
    for i, v in enumerate(["2450000", "1500000", "420000", "10"]):
        inp.nth(i).fill(v)
    pg.wait_for_timeout(200)
    amts = p.locator("li[data-pay] .a").all_inner_texts()
    exp = ["245,000 ₪", "420,000 ₪", "1,500,000 ₪", "183,750 ₪", "101,250 ₪"]
    check(tag + " bpay: the design case gives the five payments of the design", [a.replace("‏", "").strip() for a in amts] == exp, amts)
    tx = p.inner_text()
    check(tag + " bpay: the 30 and 60 day deadlines from the signing date", "8.12.2026" in tx and "7.1.2027" in tx)
    check(tag + " bpay: the advance names section 15 with its source and date", "סעיף 15" in p.locator("li[data-pay='adv']").inner_text() and "26.10.2026" in p.locator("li[data-pay='adv']").inner_text())
    check(tag + " bpay: the share bar and the five-part bar", p.locator(".nli__share button").count() == 1 and p.locator(".nlbh3-bar i").count() == 5)
    shot(p, f"{tag}-03-bpay.png")
    p.locator(".nlph-tabs button[data-v='old']").click(); pg.wait_for_timeout(150)
    check(tag + " bpay: 15% for a flat bought before 7.11.2001", "367,500" in p.locator("li[data-pay='adv'] .a").inner_text())
    p.locator(".nlph-tabs button[data-v='std']").click()
    inp.nth(1).fill("3000000"); pg.wait_for_timeout(150)
    check(tag + " bpay error: a mortgage above the price, in plain words, the field marked", "גדולה ממחיר הדירה" in p.locator(".nlbh3-note.is-stop").inner_text() and inp.nth(1).get_attribute("aria-invalid") == "true")
    shot(p.locator(".nlbh3-note.is-stop"), f"{tag}-04-bpay-error.png")
    inp.nth(1).fill("1500000"); inp.nth(2).fill("2100000"); pg.wait_for_timeout(150)
    check(tag + " bpay error: the seller balance larger than what is left", "יתרת המשכנתא של המוכר" in p.locator(".nlbh3-note.is-stop").inner_text())
    inp.nth(2).fill("420000"); inp.nth(5).fill("2026-10-01"); pg.wait_for_timeout(150)
    check(tag + " bpay error: a handover before the signing", "תאריך המסירה מוקדם" in p.locator(".nlbh3-note.is-stop").inner_text())
    inp.nth(5).fill("2027-02-01"); pg.wait_for_timeout(150)
    check(tag + " bpay: a valid handover date gives the days from the signing", p.locator(".nlbh3-note.is-stop").count() == 0 and "85 ימים" in p.inner_text())

    # ---- bsign ----
    s = pg.locator('[data-nli="bsign"]')
    check(tag + " bsign: three lists, 12 items, the dates from the signing date", s.locator("input[type=checkbox]").count() == 12 and "8.12.2026" in s.inner_text() and s.locator("h4.nlbh3-sh").count() == 3)
    s.locator(".nlbh3-chk label").nth(0).click(); s.locator(".nlbh3-chk label").nth(5).click(); pg.wait_for_timeout(100)
    check(tag + " bsign: ticks count", "2 מתוך 12" in s.locator(".nlbh3-prog").inner_text())
    shot(s, f"{tag}-05-bsign.png")

    # ---- bkeys ----
    k = pg.locator('[data-nli="bkeys"]')
    ki = k.locator("input[type=text]")
    ki.nth(0).fill("04812"); ki.nth(1).fill("1290.4"); ki.nth(3).fill("4")
    k.locator("textarea").nth(0).fill("סדק בחלון בחדר השינה\nברז מטפטף במטבח"); k.locator("textarea").nth(1).fill("מזגן בסלון")
    k.locator(".nlbh3-chk label").nth(0).click(); pg.wait_for_timeout(100)
    check(tag + " bkeys: an empty official wording is hidden (no invented procedure)", k.locator(".nlbh3-chk small").count() == 0)
    check(tag + " bkeys: a transfer counts", "1 מתוך 5" in k.locator(".nlbh3-prog").inner_text())
    shot(k, f"{tag}-06-bkeys.png")

    # ---- breg ----
    r = pg.locator('[data-nli="breg"]')
    check(tag + " breg: ten steps; the declaration and the tax with their dates", r.locator("li[data-reg]").count() == 10 and "8.12.2026" in r.locator("li[data-reg='declare']").inner_text() and "7.1.2027" in r.locator("li[data-reg='ptax']").inner_text())
    r.locator("li[data-reg='warn'] button[data-v='2']").click(); r.locator("li[data-reg='declare'] button[data-v='1']").click(); pg.wait_for_timeout(100)
    check(tag + " breg: statuses count and colour the step", "1 מתוך 10" in r.locator(".nlbh3-prog").inner_text() and "is-2" in (r.locator("li[data-reg='warn']").get_attribute("class") or ""))
    shot(r, f"{tag}-07-breg.png")

    # ---- bmemo ----
    mm = pg.locator('[data-nli="bmemo"]')
    for qi, v in enumerate(["y", "y", "y", "n", "n", "y"]):
        mm.locator(".nlbh3-q").nth(qi).locator("button[data-v='" + v + "']").click()
    pg.wait_for_timeout(100)
    check(tag + " bmemo: essentials signed by both, not subject to contract: high risk, the next step, not legal advice", mm.locator(".nlbh3-risk").get_attribute("data-level") == "high" and "סיכון גבוה" in mm.inner_text() and "לא משלמים" in mm.inner_text() and "זה לא ייעוץ משפטי" in mm.inner_text() and "סעיף 8" in mm.inner_text())
    shot(mm, f"{tag}-08-bmemo.png")
    mm.locator(".nlbh3-q").nth(4).locator("button[data-v='y']").click(); pg.wait_for_timeout(100)
    check(tag + " bmemo: \"subject to contract\" turns it to medium", mm.locator(".nlbh3-risk").get_attribute("data-level") == "mid")

    # ---- the glossary ----
    gf = pg.locator(".nlbg-gloss-find")
    gi = gf.locator("input[type=search]")
    check(tag + " glossary: a labelled search field and the count", gf.locator("label").get_attribute("for") == gi.get_attribute("id") and "10 מונחים" in gf.locator("p").inner_text())
    gi.fill("משכנתא"); pg.wait_for_timeout(100)
    n_vis = pg.evaluate("() => [...document.querySelectorAll('#nlbg-gloss dt')].filter(d => !d.hidden).length")
    check(tag + " glossary: a word filters terms and definitions", n_vis == 2 and "2 מונחים מתוך 10" in gf.locator("p").inner_text(), [n_vis, gf.locator("p").inner_text()])
    gi.fill('רמ"י'); pg.wait_for_timeout(100)
    check(tag + " glossary: quotes and gershayim are the same letter", "מונח אחד מתוך 10" in gf.locator("p").inner_text())
    shot(pg.locator("section.nlbp-art:has(#nlbg-gloss)"), f"{tag}-09-glossary-filtered.png")
    gi.fill(""); pg.wait_for_timeout(100)
    check(tag + " glossary: clearing shows all terms again", pg.evaluate("() => [...document.querySelectorAll('#nlbg-gloss dt, #nlbg-gloss dd')].every(d => !d.hidden)") and "10 מונחים" in gf.locator("p").inner_text())

    # ---- touch targets and focus ----
    tb = pg.evaluate(TARGETS, 48 if tag == "390" else 44)
    check(tag + " touch targets of the new controls: at least " + ("48" if tag == "390" else "44") + " px", not tb, tb)
    pg.locator(".nlbg-map__chips a").first.focus(); pg.keyboard.press("Tab"); pg.keyboard.press("Shift+Tab")
    fo = pg.evaluate("() => { const a = document.activeElement, s = getComputedStyle(a); return [a.getAttribute('href'), s.outlineStyle, s.outlineWidth]; }")
    check(tag + " visible focus on a map chip (keyboard)", fo[0] == "#nlbg-c1" and fo[1] != "none" and fo[2] != "0px", fo)

    # ---- reload: everything saved comes back, bmemo does not ----
    pg.reload(wait_until="networkidle"); ready(pg)
    p = pg.locator('[data-nli="bpay"]'); s = pg.locator('[data-nli="bsign"]'); k = pg.locator('[data-nli="bkeys"]'); r = pg.locator('[data-nli="breg"]'); mm = pg.locator('[data-nli="bmemo"]')
    check(tag + " reload: bpay keeps its numbers and the handover date", p.locator(".nlbh-form input").nth(0).input_value() == "2,450,000" and p.locator(".nlbh-form input").nth(5).input_value() == "2027-02-01" and "101,250" in p.locator("li[data-pay='last'] .a").inner_text())
    check(tag + " reload: bsign keeps 2 ticks", s.locator("input[type=checkbox]:checked").count() == 2)
    check(tag + " reload: bkeys keeps the readings, the defects and the transfer", k.locator("input[type=text]").nth(0).input_value() == "04812" and "ברז מטפטף" in k.locator("textarea").nth(0).input_value() and k.locator("input[type=checkbox]:checked").count() == 1)
    check(tag + " reload: breg keeps its statuses", "is-2" in (r.locator("li[data-reg='warn']").get_attribute("class") or "") and r.locator("li[data-reg='declare'] button[data-v='1']").get_attribute("aria-pressed") == "true")
    check(tag + " reload: bmemo keeps nothing (privacy)", mm.locator(".nlbh3-risk").count() == 0 and mm.locator("button[aria-pressed='true']").count() == 0 and "6 שאלות" in mm.inner_text())
    rd = pg.evaluate("() => [document.getElementById('nlbg-c13').classList.contains('is-read'), !document.querySelector('.nlbg-map__prog').hidden, document.querySelector('.nlbg-map__prog').textContent]")
    check(tag + " reload: the map remembers chapter 13 and says how many were read", rd[0] and rd[1] and "קראתם" in rd[2], rd)
    shot(pg.locator("#nlbg-map"), f"{tag}-01-map.png")
    shot(pg.locator("#nlbg-c11"), f"{tag}-11-chapter11.png")

    # ---- print views ----
    pg.evaluate("() => { window.__pr = ''; window.print = () => { const h = document.getElementById('nlbh-print-host'); window.__pr = h ? h.innerText : ''; }; }")
    p.locator("button.nlbh-pdf").click()
    pr = pg.evaluate("() => window.__pr")
    check(tag + " print: the payment schedule alone, with the five rows and the source", "183,750" in pr and "101,250" in pr and "סעיף 15" in pr and pg.evaluate("() => document.documentElement.classList.contains('nlbh-printing')"), pr[:80])
    pg.emulate_media(media="print"); pg.evaluate("() => window.scrollTo(0, 0)")
    pg.screenshot(path=os.path.join(OUT, f"{tag}-10-print-bpay.png"))
    pg.emulate_media(media="screen"); pg.evaluate("() => window.dispatchEvent(new Event('afterprint'))")
    k.locator("button.nlbh-pdf").click()
    pr = pg.evaluate("() => window.__pr")
    check(tag + " print: the handover protocol with readings, defects and two signature lines", "04812" in pr and "ברז מטפטף" in pr and "חתימת הקונים" in pr and "חתימת המוכרים" in pr)
    pg.evaluate("() => window.dispatchEvent(new Event('afterprint'))")
    s.locator("button.nlbh-pdf").click()
    check(tag + " print: the signing-day lists", "יוצאים עם" in pg.evaluate("() => window.__pr"))
    pg.evaluate("() => window.dispatchEvent(new Event('afterprint'))")
    r.locator("button.nlbh-pdf").click()
    check(tag + " print: the registration tracker with statuses", "התקבל" in pg.evaluate("() => window.__pr") and "נשלח" in pg.evaluate("() => window.__pr"))
    pg.evaluate("() => window.dispatchEvent(new Event('afterprint'))")
    check(tag + " print: the page comes back after printing", not pg.evaluate("() => document.documentElement.classList.contains('nlbh-printing')"))
    o = pg.evaluate(OVER)
    check(tag + " no sideways scroll after all presses", o["sw"] <= o["W"] and not o["out"], o)
    pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(200)
    pg.screenshot(path=os.path.join(OUT, f"{tag}-00-top.png"))
    ctx.close()


def run_v3(b, w, h, tag):
    """the real page: every tool mounts, every chapter is wired, nothing overflows, the glossary works"""
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if tag == "390" else 1, locale="he-IL")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_function("document.querySelectorAll('[data-nli]').length === document.querySelectorAll('[data-nli-on] .nlbh').length", timeout=30000)
    pg.wait_for_timeout(600)
    mark_fixed(pg)
    tools = pg.evaluate("() => document.querySelectorAll('[data-nli-on] .nlbh').length")
    check(tag + " v3: no page errors, " + str(tools) + " tools mounted", not errs and tools >= 15, errs[:3])
    o = pg.evaluate(OVER)
    check(tag + " v3: no sideways scroll", o["sw"] <= o["W"] and not o["out"], o)
    ch = pg.evaluate("() => [document.querySelectorAll('section.nlbg-ch[id^=\\'nlbg-c\\']').length, document.querySelectorAll('#nlbg-map a .nlbg-vh').length]")
    check(tag + " v3: every chapter is wired to the map", ch[0] > 0 and ch[0] == ch[1], ch)
    hx = pg.evaluate("() => [...document.querySelectorAll('.nlbg-ch [data-nli]')].map(t => [t.getAttribute('data-nli'), t.closest('.nlbg-ch').id, t.querySelector('.nli__title').tagName])")
    h2in = [x[0] + " in " + x[1] for x in hx if x[2] != "H3"]
    check(tag + " v3: every tool inside a chapter titles itself h3 (the shortcode needs h=\"3\")", hx and not h2in, h2in or len(hx))
    first = pg.evaluate("() => document.querySelector('section.nlbg-ch').id")
    to_chapter(pg, first)
    check(tag + " v3: reading the first chapter marks it", pg.evaluate("(id) => document.getElementById(id).classList.contains('is-read')", first))
    if pg.locator(".nlbg-gloss-find input").count():
        n = pg.evaluate("() => document.querySelectorAll('#nlbg-gloss dt').length")
        pg.locator(".nlbg-gloss-find input").fill("נסח"); pg.wait_for_timeout(100)
        vis = pg.evaluate("() => [...document.querySelectorAll('#nlbg-gloss dt')].filter(d => !d.hidden).length")
        check(tag + " v3: the glossary filters with a live count", 0 < vis < n and ("מתוך " + str(n)) in pg.locator(".nlbg-gloss-find p").inner_text(), [n, vis])
        pg.locator(".nlbg-gloss-find input").fill("")
    tb = pg.evaluate(TARGETS, 48 if tag == "390" else 44)
    check(tag + " v3: touch targets of the new controls", not tb, tb)
    pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(300)
    shot(pg.locator("#nlbg-map"), f"v3-{tag}-map.png")
    shot(pg.locator("#" + first), f"v3-{tag}-chapter-first.png")
    if pg.locator("#nlbg-glossary").count():
        shot(pg.locator("#nlbg-glossary"), f"v3-{tag}-glossary.png")
    ctx.close()


with sync_playwright() as pw:
    try:
        b = pw.chromium.launch()
    except Exception:  # noqa: BLE001  (no bundled browser on this PC: the installed Chrome, headless)
        b = pw.chromium.launch(channel="chrome")
    if MODE == "v3":
        run_v3(b, 390, 844, "390")
        run_v3(b, 1366, 900, "1366")
        b.close()
        srv.shutdown()
        print("FAILED: " + ", ".join(FAIL) if FAIL else "ALL PASS")
        sys.exit(1 if FAIL else 0)
    run(b, 390, 844, "390")
    run(b, 1366, 900, "1366")
    rm = b.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce", locale="he-IL").new_page()
    rm.goto(URL, wait_until="networkidle"); rm.wait_for_function(READY, timeout=20000)
    tr = rm.evaluate("() => getComputedStyle(document.querySelector('.nlbg-map__chips a')).transitionDuration")
    check("reduced motion: no transition on the map chips", all(x.strip() in ("0s", "") for x in tr.split(",")), tr)
    rm.context.close()
    nj = b.new_context(viewport={"width": 390, "height": 844}, java_script_enabled=False, locale="he-IL").new_page()
    nj.goto(URL, wait_until="load")
    check("no-JS: the five server summaries print", nj.locator("[data-bhub-sum]").count() == 5)
    check("no-JS: bpay five payments, bsign 12 items, breg 10 rows, bmemo 6 questions, bkeys 5 transfers", nj.locator("[data-bhub-sum='bpay'] li").count() == 5 and nj.locator("[data-bhub-sum='bsign'] li").count() == 12 and nj.locator("[data-bhub-sum='breg'] tbody tr").count() == 10 and nj.locator("[data-bhub-sum='bmemo'] li").count() == 6 and nj.locator("[data-bhub-sum='bkeys'] li").count() == 5)
    check("no-JS: the h3 titles are in the HTML", nj.locator("[data-nli='bpay'] h3.nli__title").count() == 1 and nj.locator("[data-nli='bkeys'] h2.nli__title").count() == 1)
    check("no-JS: the full glossary shows, no search field", nj.locator("#nlbg-gloss dt:visible").count() == 10 and nj.locator(".nlbg-gloss-find").count() == 0)
    check("no-JS: the 16 map chips are links", nj.locator("#nlbg-map a[href^='#nlbg-c']").count() == 16)
    shot(nj.locator("[data-nli='bpay']"), "390-nojs-bpay-summary.png")
    b.close()
srv.shutdown()
print("FAILED: " + ", ".join(FAIL) if FAIL else "ALL PASS")
sys.exit(1 if FAIL else 0)
