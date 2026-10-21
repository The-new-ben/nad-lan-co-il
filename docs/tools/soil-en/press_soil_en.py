"""HAD-534 (d): local press of the English soil tools (the staged copies in docs/tools/soil-en/patched/), phone + desktop,
and the Hebrew regression: the same three tools rendered with the live plugin files and with the patched files must show
the same text (the one expected difference: the soil letter of plots with a partial report date, fixed " ב־,").
Harness pages are generated in memory (no files written); the repo root is served on 127.0.0.1:47941.
    python docs/tools/soil-en/press_soil_en.py        -> prints the checks, writes screenshots to docs/tools/soil-en/shots/"""
import functools, http.server, os, re, sys, threading
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.stdout.reconfigure(encoding="utf-8")
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
H = functools.partial(Quiet, directory=ROOT)
PORT = 47941
srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
OUT = os.path.join(ROOT, "docs", "tools", "soil-en", "shots"); os.makedirs(OUT, exist_ok=True)
BASE = {"live": "/plugins/nadlan-config/assets/instruments/", "patched": "/docs/tools/soil-en/patched/assets/instruments/"}
DATA = "/plugins/nadlan-config/assets/instruments/data/sde-dov-soil.json"
FONTS = {"he": "https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap",
         "en": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@600&family=IBM+Plex+Sans+Hebrew:wght@400&family=IBM+Plex+Mono:wght@400;500&display=swap"}
TOOLS = ["soilmap", "pfas", "soilask"]
HEB = re.compile("[֐-׿]")


def page_html(variant, lang):
    b, d = BASE[variant], ("ltr" if lang == "en" else "rtl")
    secs = "".join(f'<section class="nli" dir="{d}" lang="{lang}"><div class="nli-host" data-nli="{t}" data-nli-data="{DATA}"></div></section>' for t in TOOLS)
    js = "".join(f'<script defer src="{b}{s}"></script>' for s in ["core.js"] + [f"tools/{t}.js" for t in TOOLS])
    return (f'<!doctype html><html lang="{lang}" dir="{d}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<link href="{FONTS[lang]}" rel="stylesheet"><link rel="stylesheet" href="{b}core.css">'
            f'<style>body{{margin:0;background:#fff;font-family:system-ui}}.w{{max-width:1160px;margin:0 auto;padding:16px}}</style></head>'
            f'<body><div class="w">{secs}</div>{js}</body></html>')


def open_page(ctx, variant, lang, errs):
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
    pg.on("console", lambda m: errs.append("console:" + m.text[:160]) if m.type == "error" else None)
    html = page_html(variant, lang)
    pg.route(f"**/__harness-{variant}-{lang}.html", lambda r: r.fulfill(status=200, content_type="text/html; charset=utf-8", body=html))
    pg.goto(f"http://127.0.0.1:{PORT}/__harness-{variant}-{lang}.html", wait_until="load")
    pg.wait_for_selector('[data-nli="soilmap"] .nls__card', timeout=20000); pg.wait_for_timeout(7000)
    return pg


def texts(pg):
    return {t: pg.locator(f'[data-nli="{t}"]').inner_text() for t in TOOLS}


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    # 1. Hebrew regression: live files vs patched files, desktop
    ctx = b.new_context(viewport={"width": 1366, "height": 900}, locale="he-IL")
    e1, e2 = [], []
    a, c = texts(open_page(ctx, "live", "he", e1)), texts(open_page(ctx, "patched", "he", e2))
    for t in TOOLS:
        same = a[t] == c[t]
        note = ""
        if not same and t == "soilask" and a[t].replace(" ב־,", ",") == c[t]:
            same, note = True, " (only the expected ' ב־,' date fix in the letter)"
        print(f"HE {t}: {'IDENTICAL' if same else 'DIFFERENT'}{note} ({len(a[t])} chars)")
        if not same:
            for i, (x, y) in enumerate(zip(a[t].splitlines(), c[t].splitlines())):
                if x != y: print("   live:   ", x[:140]); print("   patched:", y[:140]); break
    print("HE errors live/patched:", e1[:3], e2[:3])
    ctx.close()
    # 2. English presses, phone + desktop
    for tag, vp in (("m", {"width": 390, "height": 844}), ("d", {"width": 1366, "height": 900})):
        ctx = b.new_context(viewport=vp, device_scale_factor=2 if tag == "m" else 1, locale="en-US", is_mobile=tag == "m", has_touch=tag == "m")
        errs = []
        pg = open_page(ctx, "patched", "en", errs)
        h = pg.locator('[data-nli="soilmap"]')
        c0 = h.locator(".nls__card").inner_text()[:90].replace("\n", " | ")
        h.locator(".nls__chips button", has_text="2206").first.click(); pg.wait_for_timeout(2000)
        c1 = h.locator(".nls__card").inner_text().replace("\n", " | ")
        h.locator(".nls__chips button", has_text="project in marketing").last.click(); pg.wait_for_timeout(2000)
        c2 = h.locator(".nls__card").inner_text()[:160].replace("\n", " | ")
        h.locator(".nls__q input").fill("2227"); h.locator(".nls__q input").press("Enter"); pg.wait_for_timeout(2000)
        c3 = h.locator(".nls__card").inner_text()[:160].replace("\n", " | ")
        h.locator(".nls__q input").fill("abc"); h.locator(".nls__q input").press("Enter"); pg.wait_for_timeout(600)
        c4 = h.locator(".nls__card").inner_text()[:90]
        canvas = h.locator("canvas.maplibregl-canvas").count()
        h.locator(".nls__chips button", has_text="303").first.click(); pg.wait_for_timeout(2500)
        h.screenshot(path=os.path.join(OUT, f"en-soilmap-{tag}.png"))
        q = pg.locator('[data-nli="pfas"]')
        q.locator(".nli__seg button", has_text="mg/kg").click(); q.locator("input").first.fill("0.127"); pg.wait_for_timeout(400)
        pf = q.locator(".nli__fig").inner_text() + " | " + q.locator(".nli__asub").inner_text()
        q.screenshot(path=os.path.join(OUT, f"en-pfas-{tag}.png"))
        s = pg.locator('[data-nli="soilask"]')
        s.screenshot(path=os.path.join(OUT, f"en-soilask-{tag}.png"))
        dir_en = s.locator("pre.nli__doc").get_attribute("dir")
        s.locator(".nli__seg button", has_text="Hebrew").click(); pg.wait_for_timeout(400)
        dir_he = s.locator("pre.nli__doc").get_attribute("dir"); first_he = s.locator("pre.nli__doc").inner_text().splitlines()[0]
        s.screenshot(path=os.path.join(OUT, f"en-soilask-hebrew-letter-{tag}.png"))
        s.locator(".nli__seg button", has_text="English").click(); pg.wait_for_timeout(300)
        tx = texts(pg)
        heb = {t: len(HEB.findall(tx[t])) for t in TOOLS}
        dirs = pg.evaluate("[...document.querySelectorAll('.nli')].map(e => getComputedStyle(e).direction).join(',')")
        font = pg.evaluate("getComputedStyle(document.querySelector('.nli__title')).fontFamily")
        over = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        print(f"\nEN {tag} | canvas {canvas} | direction {dirs} | title font {font[:40]} | page overflow {over}px")
        print("  start card:", c0, "\n  chip 2206:", c1[:300], "\n  project chip:", c2, "\n  search 2227:", c3, "\n  search abc:", c4)
        print("  pfas 0.127 mg/kg PFOS:", pf, "\n  letter dir en/he:", dir_en, "/", dir_he, "| Hebrew letter opens:", first_he[:60])
        print("  Hebrew letters inside the English tools (English letter selected):", heb, "| errors:", errs[:4])
        ctx.close()
    b.close()
srv.shutdown()
