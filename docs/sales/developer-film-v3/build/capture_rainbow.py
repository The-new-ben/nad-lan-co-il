# -*- coding: utf-8 -*-
"""Live captures of the Hebrew Rainbow page for the film v3 (read-only page loads; analytics blocked in this browser only).

  python capture_rainbow.py <out_dir>

Element screenshots at 1440 px wide, device scale 2: the hero with its buttons, the facts row and the price tile, the
"view from the floor" window after a tap and the keyboard control on the stage (in the run of 7.11 the headless tap did not register a floor, so the window shows its empty state), the one-map section, the
360 floor views section, the sold-by-floor section, the price-against-the-area section and the video-call booking band.
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"C:\Users\777\nad-lan\nad-lan-co-il\docs\sales\developer-film-v2\build")
from live_common import launch, EVENTS_JS
from playwright.sync_api import sync_playwright

URL = "https://nad-lan.co.il/projects/rainbow-tel-aviv/"
HIDE = ("#nlcta, .nlcta, #wpadminbar, [class*='cookie'], [id*='cookie'], [class*='accessib'], [id*='accessib'], "
        ".nl-a11y, [class*='a11y-btn'] { display: none !important; }")


def shot(pg, sel, fn, pad=0, log=None):
    el = pg.locator(sel).first
    el.scroll_into_view_if_needed(); pg.wait_for_timeout(1800)
    if pad:
        b = el.bounding_box()
        pg.screenshot(path=fn, clip={"x": max(0, b["x"] - pad), "y": max(0, b["y"] - pad), "width": b["width"] + 2 * pad, "height": b["height"] + 2 * pad})
    else:
        el.screenshot(path=fn)
    if log is not None:
        log.append({"sel": sel, "file": os.path.basename(fn)})
    print(fn, flush=True)


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b, ctx = launch(p, 1440, 1000, dpr=2)
        pg = ctx.new_page()
        r = pg.goto(URL, wait_until="domcontentloaded", timeout=120000)
        log = {"url": URL, "status": r.status, "taken": time.strftime("%Y-%m-%d %H:%M:%S"), "shots": []}
        pg.evaluate(EVENTS_JS)
        pg.add_style_tag(content=HIDE)
        pg.wait_for_timeout(12000)
        pg.screenshot(path=os.path.join(out, "rb_top.png"))
        log["shots"].append({"file": "rb_top.png", "what": "the first screen"})
        # the stage to floor 23 with its own keyboard control (as in v2's capture_live.py), then the view from that floor
        pg.locator("section#nlps").scroll_into_view_if_needed(); pg.wait_for_timeout(2500)
        box = pg.locator("section#nlps canvas").first.bounding_box()
        pg.mouse.move(box["x"] + box["width"] * 0.46, box["y"] + box["height"] * 0.42); pg.wait_for_timeout(700)
        pg.mouse.click(box["x"] + box["width"] * 0.46, box["y"] + box["height"] * 0.42); pg.wait_for_timeout(2500)
        ev = [x for x in pg.evaluate("window.__ev || []") if x["n"] == "nl:floor"]
        floor = ev[-1]["d"]["floor"] if ev else None; guard = 0
        pg.focus("section#nlps canvas")
        while floor is not None and floor != 23 and guard < 40:
            pg.keyboard.press("ArrowUp" if floor < 23 else "ArrowDown"); guard += 1; pg.wait_for_timeout(260)
            ev = [x for x in pg.evaluate("window.__ev || []") if x["n"] == "nl:floor"]; floor = ev[-1]["d"]["floor"]
        for _ in range(3):
            pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(900)
            f = [x for x in pg.evaluate("window.__ev || []") if x["n"] == "nl:facing"]
            if f and abs((((f[-1]["d"].get("bearing") or 0) - 270 + 180) % 360) - 180) < 30:
                break
        log["floor"] = floor; log["facing"] = (f[-1]["d"] if f else None)
        pg.wait_for_timeout(2500)
        pg.screenshot(path=os.path.join(out, "rb_stage_after_tap.png"))
        # the site's sticky header would sit over the element shots: hidden in this browser from here on
        pg.evaluate("""() => { for (const e of document.querySelectorAll('header, .wp-site-blocks > *')) { const p = getComputedStyle(e).position;
            if ((p === 'sticky' || p === 'fixed') && e.getBoundingClientRect().top < 5 && e.getBoundingClientRect().height < 200) e.style.setProperty('display', 'none', 'important'); } }""")
        for sel, fn in [("#nlps-view", "rb_view.png"), (".nlpf", "rb_facts.png"), ("#nlpjx-map", "rb_map.png"),
                        ("#nlps-tour", "rb_tour360.png"), ("#nlps-deals", "rb_deals.png"), ("#nlpjx-price", "rb_price.png"),
                        ("#nlsch", "rb_booking.png")]:
            try:
                shot(pg, sel, os.path.join(out, fn), log=log["shots"])
            except Exception as e:
                print("ERR", sel, str(e)[:200]); log["shots"].append({"sel": sel, "err": str(e)[:200]})
        try:
            t = pg.locator(".nlpf__item", has_text="מחיר ממוצע").first
            t.scroll_into_view_if_needed(); pg.wait_for_timeout(800)
            t.screenshot(path=os.path.join(out, "rb_price_tile.png")); log["tile"] = t.inner_text()
        except Exception as e:
            print("ERR tile", e)
        pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(1500)
        a = pg.locator('a[data-nlps-ev="hero-video"]').first
        bb = a.bounding_box(); log["heroVideo"] = {"text": a.inner_text(), "href": a.get_attribute("href"), "box": bb}
        pg.screenshot(path=os.path.join(out, "rb_hero_buttons.png"),
                      clip={"x": max(0, bb["x"] - 420), "y": max(0, bb["y"] - 150), "width": min(1440, bb["width"] + 840), "height": 330})
        log["events"] = pg.evaluate("window.__ev || []")[-6:]
        json.dump(log, open(os.path.join(out, "rainbow.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        b.close()
