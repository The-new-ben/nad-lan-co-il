"""Sde Dov stages' harness check (Dimri Yama, Ashira; prototypes, 28.9.2026): loads scripts/project-stage/<key>_harness.html
in headless Chrome (a real GPU through ANGLE) with the COMMITTED bridge.js (?bridge=/__head__/bridge.js, served by a small
server that answers that path with `git show HEAD:plugins/nadlan-config/assets/project-stage/bridge.js`), taps a floor on
each pickable building, a side on the ring, the facilities chip and every facility card, the quarter chip, and saves the
screenshots; prints the console errors and the frame rate. One browser at a time (the machine may be busy).
  python scripts/project-stage/sdedov_serve.py 47962     (the repo root, and the committed bridge.js at /__head__/bridge.js)
  python scripts/project-stage/sdedov_shots.py dimri|ashira <outdir> [desktop|mobile|both] [quick]"""
import io, json, os, sys, time
from playwright.sync_api import sync_playwright
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

KEY = sys.argv[1]
# (building, floor, shot name, a view bearing to turn to first when the building stands behind another from the hero side)
PICKS = {"dimri": (("A", 25, "2_floor_tower", None), ("C", 11, "3_floor_midrise", None)),
         "ashira": (("S1", 25, "2_floor_tower", None), ("N2", 11, "3_floor_midrise", 62))}[KEY]
URL = "http://127.0.0.1:47962/scripts/project-stage/%s_harness.html?nlps3d&bridge=/__head__/bridge.js" % KEY
OUT = sys.argv[2] if len(sys.argv) > 2 else "shots"
MODE = sys.argv[3] if len(sys.argv) > 3 else "both"
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
    for tw, fl, name, turn in PICKS:
        if turn is not None:
            # the visitor turns the stage to see the building (a drag); here the stage's own camera helper does it
            if pg.evaluate("!!document.querySelector('.rbs-label.is-on')"):
                pg.click(".rbs-label-close")
                settle(pg, 1.6)
            pg.evaluate("window.__nlpsStage._engine()._view(%d, 16, 1.0, null)" % turn)
            settle(pg, 1.2)
        pt = pg.evaluate("window.__nlpsStage._engine()._floorScreenPoint(%d, '%s')" % (fl, tw))
        bx = stage_box(pg)
        covered = pg.evaluate("(([x, y]) => { const e = document.elementFromPoint(x, y); return !(e && e.tagName === 'CANVAS'); })", [pt["x"], pt["y"]])
        if covered or not (bx["x"] + 20 < pt["x"] < bx["x"] + bx["w"] - 20 and bx["y"] + 20 < pt["y"] < bx["y"] + bx["h"] - 20):
            # the tower is out of the frame from here: back to the overview first (as a visitor would, with the card's x)
            if pg.evaluate("!!document.querySelector('.rbs-label.is-on')"):
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
        if tw == PICKS[0][0]:  # noqa
            # a different side on the same floor: tap the ring on the south side
            rp = pg.evaluate("window.__nlpsStage._engine()._ringScreenPoint(191, %d, '%s')" % (fl, tw))
            if not rp["behind"]:
                if mob: pg.touchscreen.tap(rp["x"], rp["y"])
                else: pg.mouse.click(rp["x"], rp["y"])
                settle(pg, 1.2)
                print(kind, "ring tap south ->", pg.evaluate("window.__nlpsStage.getSelection()"))
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
        # every card, also of a pin that waits for another angle (its button is there, only hidden)
        pg.evaluate("document.querySelectorAll('.rbs-qpin--facility')[%d].click()" % i)
        time.sleep(0.4)
        title = pg.evaluate("(document.querySelector('.rbs-qcard.is-on .rbs-qcard-title') || {}).textContent || null")
        opened.append((txt, v == "visible", title))
        if v == "visible" and txt in ("בריכות", "בריכה וכושר"):
            shot(pg, tag + "5_facility_card")
    print(kind, "cards opened:", opened)
    pg.evaluate("document.querySelector('.rbs-qcard') && document.querySelector('.rbs-qcard').classList.remove('is-on')")
    pg.click("[data-nlps-phase='facilities']")
    settle(pg, 1.8)
    # the quarter: the legend's "permit" chip frames the project with its nearest neighbours (both at the permit stage)
    pg.click("[data-nlps-phase='permit']")
    into_view(pg)
    settle(pg, 2.6)
    shot(pg, tag + "6_quarter")
    pg.click("[data-nlps-phase='permit']")
    settle(pg, 1.8)
    # a wide aerial look at the city around (the camera pulled back)
    into_view(pg)
    pg.evaluate("window.__nlpsStage._engine()._view(120, 30, 2.6, 40)")
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
