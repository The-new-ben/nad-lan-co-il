# -*- coding: utf-8 -*-
"""Screens of the live site for the developers' film (the owner, 28.9.2026: "a video to present it to developers").
Read-only, headless Chrome with WebGL: each feature as a buyer meets it on a project page. Saved to img/nadlan-developers/.
  python scripts/project-video/capture_dev.py"""
import io, os, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "img", "nadlan-developers")
os.makedirs(OUT, exist_ok=True)
RB = "https://nad-lan.co.il/projects/rainbow-tel-aviv/"
DUO = "https://nad-lan.co.il/projects/duo-tel-aviv/"
W, H = 1600, 1000


def page(b, url, w=W, h=H):
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1.25)
    pg = ctx.new_page()
    pg.goto(url + ("&" if "?" in url else "?") + "cb=dev%d" % time.time(), wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(9000)
    # the floating pill and the accessibility button stay out of the screens
    pg.add_style_tag(content="#nlcta,#nla11y,.nlcta-wa{display:none!important}")
    return ctx, pg


def shot(pg, name, loc=None):
    p = os.path.join(OUT, name + ".jpg")
    (loc or pg).screenshot(path=p, type="jpeg", quality=90)
    print("ok", name)


with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome", headless=True, args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    # 1. the first fold: title, lead and the stage
    ctx, pg = page(b, RB)
    shot(pg, "rb-fold")
    # 2. a floor and an apartment: the stage and the view from it
    pg.evaluate("async () => { const s = window.__nlpsStage; await s.ready; s.selectUnit('25-w', 'user'); }")
    pg.wait_for_timeout(6000)
    pg.locator("#nlps").scroll_into_view_if_needed(); pg.wait_for_timeout(1500)
    shot(pg, "rb-stage-floor", pg.locator(".nlps-stagebox"))
    pg.locator("#nlps-view").scroll_into_view_if_needed(); pg.wait_for_timeout(4000)
    shot(pg, "rb-view", pg.locator(".nlps-below"))
    # 3. the floor's slice
    pg.locator(".nlps-slice").click(); pg.wait_for_timeout(1800)
    shot(pg, "rb-slice", pg.locator(".nlsl__box"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(600)
    # 4. inside the apartment, a design style
    pg.locator(".nlat__go").scroll_into_view_if_needed(); pg.locator(".nlat__go").click(); pg.wait_for_timeout(6000)
    st = pg.locator(".nlat-style")
    for i in range(st.count()):
        if "עץ חם" in st.nth(i).inner_text():
            st.nth(i).click(); break
    pg.wait_for_timeout(6000)
    shot(pg, "rb-inside-warm")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(800)
    # 5. the basket
    pg.evaluate("window.__nlBasket && window.__nlBasket.open()"); pg.wait_for_timeout(1200)
    shot(pg, "rb-basket")
    ctx.close()
    # 6. a facility room: the roof pool
    ctx, pg = page(b, RB)
    pg.locator("#nlps").scroll_into_view_if_needed(); pg.wait_for_timeout(800)
    pg.evaluate("document.querySelector('[data-nlps-phase=facilities]').click()"); pg.wait_for_timeout(3000)
    pins = pg.locator(".rbs-qpin--facility")
    for i in range(pins.count()):
        if "בריכ" in pins.nth(i).inner_text():
            pins.nth(i).click(force=True); break
    pg.wait_for_timeout(1500)
    shot(pg, "rb-facility-card", pg.locator(".nlps-stagebox"))
    btn = pg.locator("button.rbs-qcard-360")
    if btn.count():
        btn.first.click(); pg.wait_for_timeout(7000)
        shot(pg, "rb-pool-360")
    ctx.close()
    # 7. DUO: the stage, and the deals by floor
    ctx, pg = page(b, DUO)
    pg.evaluate("async () => { const s = window.__nlpsStage; await s.ready; s.selectUnit('S-30-w', 'user'); }")
    pg.wait_for_timeout(6000)
    pg.locator("#nlps").scroll_into_view_if_needed(); pg.wait_for_timeout(1200)
    shot(pg, "duo-stage-floor", pg.locator(".nlps-stagebox"))
    d = pg.locator(".nlps-dealswrap"); d.scroll_into_view_if_needed(); pg.wait_for_timeout(600)
    shot(pg, "duo-deals", d)
    ctx.close()
    # 8. the same project in English: since 1.72.351 with the stage in the buyer's language
    ctx, pg = page(b, "https://nad-lan.co.il/projects/rainbow-tel-aviv-en/")
    shot(pg, "rb-en")
    pg.evaluate("async () => { const s = window.__nlpsStage; if (s) { await s.ready; s.selectUnit('25-w', 'user'); } }")
    pg.wait_for_timeout(6000)
    pg.locator("#nlps").scroll_into_view_if_needed(); pg.wait_for_timeout(1500)
    shot(pg, "rb-en-stage", pg.locator(".nlps-stagebox"))
    ctx.close()
    # 9. DUO from the inside (1.72.353): the living room on floor 25
    ctx, pg = page(b, DUO)
    pg.locator(".nlat__go").scroll_into_view_if_needed(); pg.locator(".nlat__go").click(); pg.wait_for_timeout(7000)
    shot(pg, "duo-inside")
    ctx.close()
    b.close()

# every screen fitted into the film's 16:9 frame (2400x1350) on the site's paper, centred, never cropped
from PIL import Image
FIT = os.path.join(OUT, "fit")
os.makedirs(FIT, exist_ok=True)
for f in sorted(os.listdir(OUT)):
    if not f.endswith(".jpg"):
        continue
    im = Image.open(os.path.join(OUT, f)).convert("RGB")
    k = min(2400 / im.width, 1350 / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    c = Image.new("RGB", (2400, 1350), (242, 238, 227))
    c.paste(im, ((2400 - im.width) // 2, (1350 - im.height) // 2))
    c.save(os.path.join(FIT, f), quality=90)
print("fitted", len([f for f in os.listdir(FIT) if f.endswith(".jpg")]))
