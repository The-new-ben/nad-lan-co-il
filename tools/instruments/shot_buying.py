# -*- coding: utf-8 -*-
"""HAD-683: screenshots and pressed-control checks of the new /buying-apartment/ preview (build_buying_harness.py first).

    python tools/instruments/shot_buying.py [plain]   -> docs/research/2026-11-07-prices-buying/shots-buying/*.png

Phone 390 x 844 and desktop 1366 x 900, each in a fresh browser context (empty localStorage). For each: page errors, sideways
scroll (document scrollWidth, and every element of the page wider than the viewport), the rendered order (H1, answer, CTAs, the
four tools, the article), one h1, CTAs within two viewports, then presses: bplan status/type/stage/tick + reload (the plan
remembers), the status shared with the other tools, bequity amounts/rate/stress, bladder equity chips, boffer city/rooms/price,
and a no-JS render (the four server summaries). One line per check; exit 1 on a failure."""
import functools
import http.server
import os
import sys
import threading

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "docs", "research", "2026-11-07-prices-buying", "shots-buying")
os.makedirs(OUT, exist_ok=True)
NAME = "harness_buying_plain.html" if len(sys.argv) > 1 and sys.argv[1] == "plain" else "harness_buying.html"


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47943), functools.partial(Q, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = "http://127.0.0.1:47943/tools/instruments/" + NAME
FAIL = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info) if info else ""))
    if not ok:
        FAIL.append(name)


OVER = """() => { const W = document.documentElement.clientWidth, out = [];
  document.querySelectorAll('.nlbp *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.right > W + 1 || r.left < -1)) {
    let p = e.parentElement, clip = false; while (p) { const s = getComputedStyle(p); if (/(auto|scroll|hidden)/.test(s.overflowX)) { clip = true; break; } p = p.parentElement; }
    if (!clip) out.push((e.className || e.tagName) + ' ' + Math.round(r.left) + '..' + Math.round(r.right)); } });
  return { sw: document.documentElement.scrollWidth, W, out: out.slice(0, 8) }; }"""


def ans(loc):
    return loc.locator(".nlph-ans__a").first.inner_text()


def run(b, w, h, tag):
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if tag == "390" else 1, locale="he-IL")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: m.type == "error" and "favicon" not in m.text and errs.append(m.text))
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_function("document.querySelectorAll('[data-nli-on] .nlbh').length === 4", timeout=20000)
    pg.wait_for_timeout(500)
    own = [e for e in errs if "Access to font" not in e and ("127.0.0.1" in e or "nlbh" in e or "NLBH" in e or "Uncaught" in e)]
    check(tag + " no page errors from our code", not own, own[:3])
    o = pg.evaluate(OVER)
    check(tag + " no sideways scroll", o["sw"] <= o["W"] and not o["out"], o)
    order = pg.evaluate("""() => { const q = s => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().top + scrollY) : -1; };
      return [q('.nlbp h1'), q('.nlbp .nlbp-answer'), q('.nlbp .nlbp-cta'), q('[data-nli="bplan"]'), q('[data-nli="bequity"]'), q('[data-nli="bladder"]'), q('[data-nli="boffer"]'), q('.nlbp-art h2')]; }""")
    check(tag + " rendered order H1 < answer < CTAs < bplan < bequity < bladder < boffer < article", order == sorted(order) and -1 not in order, order)
    check(tag + " exactly one h1", pg.locator("main h1").count() == 1, pg.locator("main h1").count())
    cta_bottom = pg.evaluate("() => document.querySelector('.nlbp-cta').getBoundingClientRect().bottom")
    check(tag + " CTAs within two viewports", cta_bottom < 2 * h, round(cta_bottom))
    pg.locator(".nlbp-head").screenshot(path=os.path.join(OUT, f"{tag}-0-head.png"))

    # ---- bplan ----
    p = pg.locator('[data-nli="bplan"]')
    check(tag + " bplan: 12 statuses", p.locator(".nlbh-st button").count() == 12)
    txt = p.inner_text()
    check(tag + " bplan: first home rules (brackets, LTV 75%, eligibility loan)", "1,978,745" in txt and "75%" in txt and "54,240" in txt)
    p.locator(".nlbh-st button", has_text="דירה חלופית").click(); pg.wait_for_timeout(150)
    check(tag + " bplan: replacement adds the sell-the-old-flat step and LTV 70%", "מתכננים את מכירת הדירה הקיימת" in p.evaluate("e => e.textContent") and "70%" in p.inner_text())
    p.locator("button", has_text="מקבלן").first.click(); pg.wait_for_timeout(150)
    t2 = p.evaluate("e => e.textContent")
    check(tag + " bplan: developer type shows the contractor register, hides the tabu extract step", "בודקים את הקבלן בפנקס הקבלנים" in t2 and "נסח טאבו או אישור זכויות" not in t2)
    p.locator("button", has_text="לפני חתימה").first.click(); pg.wait_for_timeout(150)
    nx = p.locator(".nlbh-next b").inner_text()
    check(tag + " bplan: the next step follows the stage", "עורך דין" in nx or "שכר הטרחה" in nx or "ערבות" in nx, nx)
    p.locator(".nlbh-stages li.is-now .nlbh-chk").first.click(); pg.wait_for_timeout(150)
    c1 = p.locator(".nlbh-chk[aria-pressed='true']").count()
    p.screenshot(path=os.path.join(OUT, f"{tag}-1-bplan.png"))
    pg.reload(wait_until="networkidle"); pg.wait_for_function("document.querySelectorAll('[data-nli-on] .nlbh').length === 4", timeout=20000); pg.wait_for_timeout(300)
    p = pg.locator('[data-nli="bplan"]')
    check(tag + " bplan: remembers status, type, stage and ticks after reload", c1 == 1 and p.locator(".nlbh-chk[aria-pressed='true']").count() == 1 and p.locator(".nlbh-st button[aria-pressed='true']").inner_text().startswith("דירה חלופית"))
    p.locator(".nlbh-st button", has_text="תושבי חוץ").click(); pg.wait_for_timeout(200)
    e = pg.locator('[data-nli="bequity"]')
    check(tag + " status shared: bequity follows bplan (foreign, 50%)", "50%" in e.locator(".nlph-ans__head").first.inner_text() and e.locator("select").first.input_value() == "foreign")
    p.locator(".nlbh-st button", has_text="דירה ראשונה").click(); pg.wait_for_timeout(200)

    # ---- bequity ----
    a = ans(e)
    check(tag + " bequity: national 4-room median, need 520,922", "2,028,800" in a and "520,922" in a, a[:120])
    fund = e.locator(".nlbh-src > div").nth(4)
    fund.locator("input").nth(0).fill("60000"); pg.wait_for_timeout(100)
    check(tag + " bequity: a loan with no rate shows no number", "הקלידו ריבית" in e.locator("table").first.inner_text())
    fund.locator("input").nth(1).fill("5.5"); pg.wait_for_timeout(150)
    check(tag + " bequity: the rate gives a monthly payment", "הקלידו ריבית" not in e.locator("table").first.inner_text())
    sa = e.locator(".nlph-ans__a").nth(1).inner_text()
    check(tag + " bequity: handover stress, 325,333 at 10% paid", "325,333" in sa, sa[:120])
    e.locator("button", has_text="נמוכה ב־10%").click(); pg.wait_for_timeout(150)
    check(tag + " bequity: a lower appraisal asks for more", "325,333" not in e.locator(".nlph-ans__a").nth(1).inner_text())
    e.screenshot(path=os.path.join(OUT, f"{tag}-2-bequity.png"))

    # ---- bladder ----
    l = pg.locator('[data-nli="bladder"]')
    l.locator("button", has_text="500 אלף").click(); pg.wait_for_timeout(150)
    la = ans(l)
    check(tag + " bladder: 500K -> 1,953,000, 11 cities for 3 rooms", "1,953,000" in la and "11 ערים בדירת 3 חדרים" in la and "פטור" in l.inner_text(), la[:140])
    check(tag + " bladder: 25 rows, marked cells", l.locator("table tbody tr").count() == 25 and l.locator("td.fit").count() >= 11)
    l.locator("input").nth(1).fill("12000"); pg.wait_for_timeout(150)
    check(tag + " bladder: an income caps the loan", "מוגבל" in ans(l), ans(l)[:120])
    l.screenshot(path=os.path.join(OUT, f"{tag}-3-bladder.png"))

    # ---- boffer ----
    f = pg.locator('[data-nli="boffer"]')
    fa = ans(f)
    check(tag + " boffer: Ramat Gan 4 rooms, +8% over the median, neighbourhood share", "גבוה ב־" in fa and "רמת גן" in f.locator(".nlph-ans__head").inner_text() and "מתוך" in fa, fa[:140])
    f.locator("select").first.select_option(label="תל אביב יפו"); f.locator("button", has_text="3 חדרים").click(); pg.wait_for_timeout(150)
    check(tag + " boffer: city and rooms change the basis", "תל אביב יפו, 3 חדרים" in f.locator(".nlph-ans__head").inner_text())
    f.locator("input").first.fill("1000000"); pg.wait_for_timeout(150)
    check(tag + " boffer: an asking price under the data says so", "בתחתית" in f.inner_text())
    f.locator("input").first.fill("4500000"); pg.wait_for_timeout(150)
    f.screenshot(path=os.path.join(OUT, f"{tag}-4-boffer.png"))

    # ---- the article: deadlines and FAQ ----
    pg.locator(".nlbp-art h2", has_text="המועדים אחרי החתימה").scroll_into_view_if_needed(); pg.wait_for_timeout(150)
    pg.screenshot(path=os.path.join(OUT, f"{tag}-5-deadlines.png"))
    check(tag + " article: FAQ section with 17 questions", pg.locator(".nlbp-art h2:has-text('השאלות שלא שואלים') ~ h3").count() >= 17)
    o = pg.evaluate(OVER)
    check(tag + " no sideways scroll after all presses", o["sw"] <= o["W"] and not o["out"], o)
    ctx.close()


with sync_playwright() as pw:
    try:
        b = pw.chromium.launch()
    except Exception:  # noqa: BLE001  (no bundled browser on this PC: the installed Chrome, headless)
        b = pw.chromium.launch(channel="chrome")
    run(b, 390, 844, "390")
    run(b, 1366, 900, "1366")
    nj = b.new_context(viewport={"width": 390, "height": 844}, java_script_enabled=False, locale="he-IL").new_page()
    nj.goto(URL, wait_until="load")
    check("no-JS: the four server summaries print", nj.locator("[data-bhub-sum]").count() == 4)
    check("no-JS: the status table (12 rows) and the equity ladder table", nj.locator("[data-bhub-sum='bplan'] tbody tr").count() == 12 and nj.locator("[data-bhub-sum='bladder'] tbody tr").count() == 4)
    nj.locator("[data-nli='bladder']").screenshot(path=os.path.join(OUT, "390-nojs-bladder-summary.png"))
    b.close()
srv.shutdown()
print("FAILED: " + ", ".join(FAIL) if FAIL else "ALL PASS")
sys.exit(1 if FAIL else 0)
