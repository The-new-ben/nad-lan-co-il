"""DUO stage harness check (prototype, 28.9.2026): loads scripts/project-stage/duo_harness.html in headless Chrome (a real
GPU through ANGLE), taps a floor on each tower, a side on the ring, the facilities chip and every facility card, the quarter
chip, and saves the screenshots; prints the console errors and the frame rate.
  python -m http.server 47961 --bind 127.0.0.1          (from the repo root, in another shell)
  python scripts/project-stage/duo_shots.py scripts/project-stage/shots/duo-proto [desktop|mobile|both] [quick]"""
import io, json, os, sys, time
from playwright.sync_api import sync_playwright
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

URL = "http://127.0.0.1:47961/scripts/project-stage/duo_harness.html?nlps3d"
OUT = sys.argv[1] if len(sys.argv) > 1 else "shots"
MODE = sys.argv[2] if len(sys.argv) > 2 else "both"
QUICK = "quick" in sys.argv
os.makedirs(OUT, exist_ok=True)
ARGS = ["--use-gl=angle", "--use-angle=d3d11", "--enable-webgl", "--ignore-gpu-blocklist", "--enable-gpu"]


def stage_box(pg):
    return pg.evaluate("(() => { const r = document.getElementById('nlps').getBoundingClientRect(); return {x: r.left, y: r.top, w: r.width, h: r.height}; })()")


def shot(pg, name, full=False):
    p = os.path.join(OUT, name + ".png")
    if full:
        pg.screenshot(path=p, full_page=False)
    else:
        b = stage_box(pg)
        pg.screenshot(path=p, clip={"x": max(0, b["x"]), "y": max(0, b["y"]), "width": b["w"], "height": b["h"]})
    print("shot", p)


def settle(pg, s=2.2):
    time.sleep(s)


def into_view(pg):
    pg.evaluate("document.getElementById('nlps').scrollIntoView({block: 'center'})")
    time.sleep(0.5)


def run(p, kind):
    mob = kind == "mobile"
    b = p.chromium.launch(channel="chrome", headless=True, args=ARGS)
    ctx = b.new_context(viewport={"width": 390, "height": 844} if mob else {"width": 1440, "height": 900}, device_scale_factor=2 if mob else 1,
                        is_mobile=mob, has_touch=mob,
                        user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36" if mob else None)
    pg = ctx.new_page()
    errs = []
    pg.on("console", lambda m: errs.append((m.type, m.text)) if m.type in ("error", "warning") else None)
    pg.on("pageerror", lambda e: errs.append(("pageerror", str(e))))
    pg.set_default_timeout(120000)
    t0 = time.time()
    pg.goto(URL, wait_until="load")
    pg.evaluate("document.getElementById('nlps').scrollIntoView({block: 'center'})")
    pg.wait_for_function("window.__nlpsStage && window.__nlpsStage.phase && window.__nlpsStage.phase !== 'poster'", timeout=120000)
    print(kind, "3D live after %.1f s" % (time.time() - t0))
    pg.wait_for_function("window.__nlpsStage.phase === 'orbit'", timeout=60000)
    st = pg.evaluate("window.__nlpsStage.stats()")
    print(kind, "stats", json.dumps(st))
    pg.evaluate("window.__nlpsStage.setAutoOrbit(false)")
    settle(pg, 2.5)
    tag = "m" if mob else "d"
    if mob:
        pg.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.6)
        shot(pg, tag + "0_page_top", full=True)
        pg.evaluate("document.getElementById('nlps').scrollIntoView({block: 'center'})")
        time.sleep(0.6)
    else:
        shot(pg, tag + "0_page_top", full=True)
    shot(pg, tag + "1_hero")
    if QUICK:
        print("errors", errs)
        b.close()
        return errs
    # picked floor on the north tower: a real tap on the tower's facade
    for tw, fl, name in (("N", 25, "2_floor_north"), ("S", 36, "3_floor_south")):
        pt = pg.evaluate("window.__nlpsStage._engine()._floorScreenPoint(%d, '%s')" % (fl, tw))
        bx = stage_box(pg)
        if not (bx["x"] + 20 < pt["x"] < bx["x"] + bx["w"] - 20 and bx["y"] + 20 < pt["y"] < bx["y"] + bx["h"] - 20):
            # the tower is out of the frame from here: back to the overview first (as a visitor would, with the card's x)
            pg.click(".rbs-label-close")
            settle(pg, 1.6)
            pt = pg.evaluate("window.__nlpsStage._engine()._floorScreenPoint(%d, '%s')" % (fl, tw))
        if mob:
            pg.touchscreen.tap(pt["x"], pt["y"])
        else:
            pg.mouse.move(pt["x"], pt["y"]); time.sleep(0.2); pg.mouse.click(pt["x"], pt["y"])
        settle(pg, 2.2)
        sel = pg.evaluate("window.__nlpsStage.getSelection()")
        print(kind, name, "tapped", pt, "->", sel)
        shot(pg, tag + name)
        if tw == "N":
            # a different side on the same floor: tap the ring on the east side
            rp = pg.evaluate("window.__nlpsStage._engine()._ringScreenPoint(100, %d, 'N')" % fl)
            if not rp["behind"]:
                if mob: pg.touchscreen.tap(rp["x"], rp["y"])
                else: pg.mouse.click(rp["x"], rp["y"])
                settle(pg, 1.2)
                print(kind, "ring tap east ->", pg.evaluate("window.__nlpsStage.getSelection()"))
    # back to the overview
    pg.evaluate("window.__nlpsStage.clearFloor()")
    settle(pg, 1.6)
    # the facilities chip (a real click on the legend)
    pg.click("[data-nlps-phase='facilities']")
    into_view(pg)
    settle(pg, 2.4)
    vis = pg.evaluate("[...document.querySelectorAll('.rbs-qpin--facility')].filter(b => b.style.visibility === 'visible').map(b => b.textContent)")
    print(kind, "facility pins visible:", vis)
    shot(pg, tag + "4_facilities")
    # open each facility card, screenshot the pool's
    names = pg.evaluate("[...document.querySelectorAll('.rbs-qpin--facility')].map((b, i) => [i, b.textContent, b.style.visibility])")
    opened = []
    for i, txt, v in names:
        if v != "visible":
            continue
        pg.evaluate("document.querySelectorAll('.rbs-qpin--facility')[%d].click()" % i)
        time.sleep(0.4)
        title = pg.evaluate("(document.querySelector('.rbs-qcard.is-on .rbs-qcard-title') || {}).textContent || null")
        opened.append((txt, title))
        if txt == "בריכה":
            shot(pg, tag + "5_facility_card")
    print(kind, "cards opened:", opened)
    pg.evaluate("document.querySelector('.rbs-qcard') && document.querySelector('.rbs-qcard').classList.remove('is-on')")
    pg.click("[data-nlps-phase='facilities']")
    settle(pg, 1.8)
    # the quarter: the legend's "being built" chip frames DUO with its neighbour
    pg.click("[data-nlps-phase='building']")
    into_view(pg)
    settle(pg, 2.6)
    shot(pg, tag + "6_quarter")
    pg.click("[data-nlps-phase='building']")
    settle(pg, 1.8)
    # a wide aerial look at the city around (the camera pulled back)
    into_view(pg)
    pg.evaluate("window.__nlpsStage._engine()._view(200, 34, 2.4, 40)")
    settle(pg, 1.6)
    shot(pg, tag + "7_city")
    # straight down on the lot: the towers north and south of each other in the east half (the research's outline)
    into_view(pg)
    pg.evaluate("window.__nlpsStage._engine()._view(180, 84, 1.25, 0)")
    settle(pg, 1.6)
    shot(pg, tag + "8_top")
    st = pg.evaluate("window.__nlpsStage.stats()")
    print(kind, "stats end", json.dumps(st))
    print(kind, "errors", errs)
    b.close()
    return errs


with sync_playwright() as p:
    for k in (["desktop", "mobile"] if MODE == "both" else [MODE]):
        run(p, k)
