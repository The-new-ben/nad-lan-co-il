# -*- coding: utf-8 -*-
"""HAD-681: screenshots and pressed-control checks of the new /apartment-prices/ preview (build_prices_harness.py first).

    python tools/instruments/shot_prices.py [plain]   -> docs/research/2026-11-07-prices-buying/shots/*.png

Phone 390 x 844 and desktop 1366 x 900. For each: page errors, horizontal overflow (document scrollWidth against the viewport, and
every element wider than the viewport), the rendered order of the head (H1, answer, CTAs, first tool), the three tools mounted,
then presses: pmarket range/real/region, pcity rooms/sort/district/search/compare (incl. a 5th city refused), panatomy
segment/area/track/broker/presets, and a no-JS render (the server summaries). Prints one line per check; exit 1 on a failure."""
import functools
import http.server
import os
import sys
import threading

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "docs", "research", "2026-11-07-prices-buying", "shots")
os.makedirs(OUT, exist_ok=True)
NAME = "harness_prices_plain.html" if len(sys.argv) > 1 and sys.argv[1] == "plain" else "harness_prices.html"


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47941), functools.partial(Q, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = "http://127.0.0.1:47941/tools/instruments/" + NAME
FAIL = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info) if info else ""))
    if not ok:
        FAIL.append(name)


OVER = """() => { const W = document.documentElement.clientWidth, out = [];
  document.querySelectorAll('.nlap *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.right > W + 1 || r.left < -1)) {
    let p = e.parentElement, clip = false; while (p) { const s = getComputedStyle(p); if (/(auto|scroll|hidden)/.test(s.overflowX)) { clip = true; break; } p = p.parentElement; }
    if (!clip) out.push((e.className || e.tagName) + ' ' + Math.round(r.left) + '..' + Math.round(r.right)); } });
  return { sw: document.documentElement.scrollWidth, W, out: out.slice(0, 8) }; }"""


def run(b, w, h, tag):
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2 if tag == "390" else 1, locale="he-IL")
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: m.type == "error" and "favicon" not in m.text and errs.append(m.text))
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_function("document.querySelectorAll('[data-nli-on] .nlph').length === 3", timeout=20000)
    pg.wait_for_timeout(600)
    own = [e for e in errs if "127.0.0.1" in e or "nlph" in e or "NLPH" in e or "Uncaught" in e]
    check(tag + " no page errors from our code", not own, own[:3])
    o = pg.evaluate(OVER)
    check(tag + " no sideways scroll", o["sw"] <= o["W"] and not o["out"], o)
    order = pg.evaluate("""() => { const q = s => { const e = document.querySelector(s); return e ? Math.round(e.getBoundingClientRect().top + scrollY) : -1; };
      return [q('.nlap h1'), q('.nlap .nlap-answer'), q('.nlap .nlap-cta'), q('[data-nli="pmarket"]'), q('[data-nli="pcity"]'), q('[data-nli="panatomy"]'), q('.nlap-art h2')]; }""")
    check(tag + " rendered order H1 < answer < CTAs < pmarket < pcity < panatomy < article", order == sorted(order) and -1 not in order, order)
    check(tag + " exactly one h1 in the content", pg.locator(".nlap h1").count() == 1 and pg.locator("main h1").count() == 1, pg.locator("main h1").count())
    cta_bottom = pg.evaluate("() => document.querySelector('.nlap-cta').getBoundingClientRect().bottom")
    check(tag + " CTAs within two viewports", cta_bottom < 2 * h, round(cta_bottom))
    pg.screenshot(path=os.path.join(OUT, f"{tag}-full.png"), full_page=True)
    pg.locator(".nlap-head").screenshot(path=os.path.join(OUT, f"{tag}-0-head.png"))
    for i, t in enumerate(["pmarket", "pcity", "panatomy"]):
        pg.locator(f'[data-nli="{t}"]').screenshot(path=os.path.join(OUT, f"{tag}-{i + 1}-{t}.png"))
    pg.locator(".nlap-art").screenshot(path=os.path.join(OUT, f"{tag}-4-article.png"))

    # ---- pmarket ----
    m = pg.locator('[data-nli="pmarket"]')
    ans = m.locator(".nlph-ans__a").inner_text()
    check(tag + " pmarket answer states the change and the period", "1.8%" in ans and "יולי ואוגוסט 2026" in ans and "זמני" in ans, ans[:90])
    check(tag + " pmarket district table has 7 rows", m.locator("table tbody tr").count() == 7)
    m.locator("button", has_text="מ־1994").click(); m.locator("button", has_text="אחרי אינפלציה").click(); pg.wait_for_timeout(200)
    say = m.locator(".nlph-sec p.nlph-sub").last.inner_text()
    check(tag + " pmarket since 1994 real", "1994" in say and "אחרי אינפלציה" in say, say[:100])
    m.locator("select").select_option("60500"); pg.wait_for_timeout(200)
    say2 = m.locator(".nlph-sec p.nlph-sub").last.inner_text()
    check(tag + " pmarket district against the country", "הדרום" in say2 and "כל הארץ באותה תקופה" in say2, say2[:110])
    box = m.locator(".nlph-chart svg").bounding_box()
    pg.mouse.move(box["x"] + box["width"] * 0.6, box["y"] + box["height"] / 2); pg.wait_for_timeout(150)
    check(tag + " pmarket chart tooltip", m.locator(".nlph-tip").is_visible(), m.locator(".nlph-tip").inner_text().replace("\n", " / ")[:80])
    m.screenshot(path=os.path.join(OUT, f"{tag}-1b-pmarket-1994-real-south.png"))

    # ---- pcity ----
    c = pg.locator('[data-nli="pcity"]')
    check(tag + " pcity 25 rows (country + 24 cities)", c.locator(".nlph-tw").first.locator("tbody tr").count() == 25)
    check(tag + " pcity compare opens on 4 cities", c.locator("table.nlpc-cmp thead th").count() == 5)
    pay = c.locator("table.nlpc-cmp tbody tr").last.inner_text()
    check(tag + " pcity compare monthly payment shown", any(ch.isdigit() for ch in pay), pay.replace("\n", " ")[:80])
    c.locator('.nli__seg button[data-v="3"]').click(); pg.wait_for_timeout(150)
    c.locator("button.nlpc-sort[data-k=yoy]").click(); pg.wait_for_timeout(150)
    first = c.locator(".nlph-tw").first.locator("tbody tr").nth(1).inner_text().split("\n")[0]
    check(tag + " pcity sort by change in a year", c.locator("th[aria-sort] button[data-k=yoy]").count() == 1, first)
    c.locator(".nlpc-bar .nlph-tabs button", has_text="הדרום").click(); pg.wait_for_timeout(150)
    n_s = c.locator(".nlph-tw").first.locator("tbody tr").count()
    check(tag + " pcity district filter", 2 < n_s < 25, n_s)
    c.locator(".nlpc-bar .nlph-tabs button", has_text="כל הארץ").click()
    c.locator("input[type=search]").fill("חולון"); pg.wait_for_timeout(150)
    check(tag + " pcity search", c.locator(".nlph-tw").first.locator("tbody tr").count() == 2)
    c.locator("input[type=search]").fill("")
    c.locator('input[type=checkbox][value="חולון"]').click(); pg.wait_for_timeout(100)
    check(tag + " pcity 5th city refused", "עד 4 ערים" in c.locator(".nlpc-warn").inner_text() and c.locator("table.nlpc-cmp thead th").count() == 5)
    c.locator(".nlph-tabs button", has_text="גוש דן").click(); pg.wait_for_timeout(150)
    check(tag + " pcity preset compare", "רמת גן" in c.locator("table.nlpc-cmp thead").inner_text())
    c.screenshot(path=os.path.join(OUT, f"{tag}-2b-pcity-3rooms-dan.png"))

    # ---- panatomy ----
    a = pg.locator('[data-nli="panatomy"]')
    check(tag + " panatomy bar has 4 parts (national)", a.locator(".nlpa-bar button").count() == 4)
    a.locator('.nlpa-seg[data-id="build"]').click(); pg.wait_for_timeout(150)
    check(tag + " panatomy tap opens the construction parts", a.locator("#nlpa-d-build").is_visible() and "מדד תשומות" in a.locator("#nlpa-d-build").inner_text())
    a.locator('.nlpa-row[data-id="rest"]').click(); pg.wait_for_timeout(150)
    rest = a.locator("#nlpa-d-rest").inner_text()
    check(tag + " panatomy rest: VAT exact, marketing flagged, margin without number", "15.3%" in rest and "טענה של חברת שיווק" in rest and "אין מספר ציבורי" in rest)
    a.screenshot(path=os.path.join(OUT, f"{tag}-3b-panatomy-rest-open.png"))
    a.locator(".nli__seg button", has_text="פריפריה").click(); pg.wait_for_timeout(150)
    check(tag + " panatomy periphery: land a tenth, rest hatched", a.locator(".nlpa-seg.is-x").count() == 1 and "כעשירית" in a.locator(".nlpa-list").inner_text())
    a.locator(".nli__seg button", has_text="דירה נוספת").click(); a.locator(".nli__seg button", has_text="עם מתווך").click(); pg.wait_for_timeout(150)
    buy = a.locator(".nlpa-buy").inner_text()
    check(tag + " panatomy extra home 8% tax and broker line", "תיווך" in buy and "8% על" in buy, buy.replace("\n", " ")[:120])
    a.locator(".nlph-tabs button", has_text="תל אביב").click(); pg.wait_for_timeout(150)
    check(tag + " panatomy preset Tel Aviv sets price and centre", "5,229,800" in a.locator("input").first.input_value() and a.locator('.nli__seg button[aria-pressed="true"]', has_text="מרכז הארץ").count() == 1)
    a.screenshot(path=os.path.join(OUT, f"{tag}-3c-panatomy-telaviv-extra.png"))
    o2 = pg.evaluate(OVER)
    check(tag + " no sideways scroll after the presses", o2["sw"] <= o2["W"] and not o2["out"], o2)
    pg.close()


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    run(b, 390, 844, "390")
    run(b, 1366, 900, "1366")
    ctx = b.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
    pg = ctx.new_page(); pg.goto(URL, wait_until="networkidle")
    txt = pg.locator(".nlap").inner_text()
    check("no-JS: the three server summaries with real numbers", "ירדו ב־1.8% בשנה" in txt and "2,028,800" in txt and "15.3%" in txt and pg.locator(".nli__panel table").count() >= 3)
    pg.locator('[data-nli="pcity"]').screenshot(path=os.path.join(OUT, "390-nojs-pcity-summary.png"))
    b.close()
srv.shutdown()
print("FAILED: " + ", ".join(FAIL) if FAIL else "ALL PASS")
sys.exit(1 if FAIL else 0)
