# -*- coding: utf-8 -*-
"""Live captures for the developer film v2 (read-only; nothing is sent to the site but page loads, analytics blocked here).

  python capture_live.py stage   <out> 1920x1080     the Rainbow 3D stage driven by its own controls (noon light, a tap on
                                                      the tower, arrow keys to floor 23, arrow keys to the sea-side example
                                                      apartment), a CDP screencast of the whole drive + stills + the event log
  python capture_live.py pages   <out>               the French project page (desktop scroll + phone), the English page's
                                                      price tile, FAQ block and the language bar (element screenshots)
"""
import base64, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from live_common import launch, CSS_STAGE, EVENTS_JS
from playwright.sync_api import sync_playwright

HE = "https://nad-lan.co.il/projects/rainbow-tel-aviv/"
EN = "https://nad-lan.co.il/projects/rainbow-tel-aviv-en/"
FR = "https://nad-lan.co.il/projects/rainbow-tel-aviv-fr/"
HIDE = "#nlcta, .nlcta, #wpadminbar, [class*='cookie'], [id*='cookie'], [class*='accessib'], [id*='accessib'] { display: none !important; }"


class Cast:
    """CDP screencast: every painted frame (JPEG) with its timestamp."""
    def __init__(self, page, folder, w, h):
        self.c = page.context.new_cdp_session(page); self.folder = folder; self.n = 0; self.log = []
        os.makedirs(folder, exist_ok=True)
        self.c.on("Page.screencastFrame", self.frame)
        self.w, self.h = w, h

    def frame(self, p):
        self.n += 1
        fn = os.path.join(self.folder, "c_%05d.jpg" % self.n)
        open(fn, "wb").write(base64.b64decode(p["data"]))
        self.log.append({"f": os.path.basename(fn), "t": p["metadata"]["timestamp"]})
        try:
            self.c.send("Page.screencastFrameAck", {"sessionId": p["sessionId"]})
        except Exception:
            pass

    def start(self):
        self.c.send("Page.startScreencast", {"format": "jpeg", "quality": 92, "maxWidth": self.w, "maxHeight": self.h, "everyNthFrame": 1})

    def stop(self):
        self.c.send("Page.stopScreencast")
        json.dump(self.log, open(os.path.join(self.folder, "frames.json"), "w"), indent=0)


def ev(page):
    return page.evaluate("window.__ev || []")


def stage(out, size):
    w, h = [int(x) for x in size.split("x")]
    tag = f"{w}x{h}"
    with sync_playwright() as p:
        b, ctx = launch(p, w, h)
        pg = ctx.new_page()
        r = pg.goto(HE, wait_until="domcontentloaded", timeout=120000)
        log = {"url": HE, "status": r.status, "size": [w, h], "taken": time.strftime("%Y-%m-%d %H:%M:%S"), "steps": []}
        pg.evaluate(EVENTS_JS)
        pg.wait_for_selector("section#nlps")
        pg.evaluate("() => document.querySelector('section#nlps').scrollIntoView({block:'center'})")
        pg.add_style_tag(content=CSS_STAGE)
        pg.wait_for_timeout(12000)
        # the stage's own light button: noon (cooler than the default sunset)
        pg.click("section#nlps [data-preset='noon']"); log["steps"].append("click [data-preset=noon]")
        pg.wait_for_timeout(3000)
        pg.mouse.move(int(w * 0.75), int(h * 0.62))
        pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(out, f"stage_hero_{tag}.png"))
        # the tower: find its column from the canvas (the brightest tall structure near the middle) by hovering
        tx, ty = (915, 420) if w > h else (int(w * 0.5), int(h * 0.45))
        if len(sys.argv) > 4:
            tx, ty = [int(v) for v in sys.argv[4].split(",")]
        cast = Cast(pg, os.path.join(out, f"stage_cast_{tag}"), w, h)
        cast.start()
        pg.wait_for_timeout(1200)
        x0, y0 = int(w * 0.75), int(h * 0.62)
        for i in range(1, 31):  # a calm 1.2 s mouse move to the tower
            k = i / 30; k = k * k * (3 - 2 * k)
            pg.mouse.move(x0 + (tx - x0) * k, y0 + (ty - y0) * k); pg.wait_for_timeout(40)
        pg.wait_for_timeout(700)
        pg.mouse.down(); pg.wait_for_timeout(90); pg.mouse.up()
        log["steps"].append(f"tap tower at {tx},{ty}")
        pg.wait_for_timeout(2600)
        e = [x for x in ev(pg) if x["n"] == "nl:floor"]
        floor = e[-1]["d"]["floor"] if e else None
        log["steps"].append(f"nl:floor after tap: {floor}")
        # arrow keys on the canvas to floor 23 (the stage's own keyboard control)
        pg.focus("section#nlps canvas")
        guard = 0
        while floor is not None and floor != 23 and guard < 40:
            pg.keyboard.press("ArrowUp" if floor < 23 else "ArrowDown"); guard += 1
            pg.wait_for_timeout(260)
            e = [x for x in ev(pg) if x["n"] == "nl:floor"]; floor = e[-1]["d"]["floor"]
        log["steps"].append(f"arrows to floor {floor} ({guard} presses)")
        pg.wait_for_timeout(1500)
        # facing: ArrowRight/Left steps one example apartment at a time; stop at the sea side (bearing 270, "w")
        bearing = None; guard = 0
        while guard < 6:
            pg.keyboard.press("ArrowRight"); guard += 1
            pg.wait_for_timeout(900)
            f = [x for x in ev(pg) if x["n"] == "nl:facing"]
            if f:
                bearing = f[-1]["d"].get("bearing")
                if bearing is not None and abs(((bearing - 270 + 180) % 360) - 180) < 30:
                    break
        log["steps"].append(f"facing {bearing} after {guard} ArrowRight presses")
        pg.wait_for_timeout(3000)
        cast.stop()
        pg.screenshot(path=os.path.join(out, f"stage_floor23_{tag}.png"))
        log["events"] = ev(pg)
        log["card"] = pg.evaluate("() => { const l = document.querySelector('section#nlps .rbs-label'); return l ? l.innerText : null; }")
        # the view from that floor, as the page shows it under the stage (its own map window)
        try:
            pg.evaluate("() => { for (const s of document.querySelectorAll('style')) if (s.textContent.includes('position: fixed !important; inset: 0')) s.remove(); }")
            pg.add_style_tag(content=HIDE)
            pg.evaluate("() => { const t = document.getElementById('nlps-view-t'); if (t) t.scrollIntoView({block: 'start'}); window.scrollBy(0, -90); }")
            pg.wait_for_timeout(6000)
            box = pg.evaluate("""() => { const t = document.getElementById('nlps-view-t'); if (!t) return null;
                let el = t; for (let i = 0; i < 6 && el.parentElement; i++) { el = el.parentElement; if (el.getBoundingClientRect().height > 380) break; }
                const r = el.getBoundingClientRect(); return [r.x, r.y, r.width, r.height, el.className]; }""")
            log["viewBox"] = box
            if box:
                pg.screenshot(path=os.path.join(out, f"stage_viewpanel_{tag}.png"),
                              clip={"x": max(0, box[0]), "y": max(0, box[1]), "width": min(box[2], w), "height": min(box[3], h - max(0, box[1]))})
            pg.screenshot(path=os.path.join(out, f"stage_below_{tag}.png"))
        except Exception as ex:
            log["viewErr"] = str(ex)
        json.dump(log, open(os.path.join(out, f"stage_{tag}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(json.dumps({k: v for k, v in log.items() if k != "events"}, ensure_ascii=False, indent=1))
        b.close()


def pages(out):
    with sync_playwright() as p:
        res = {}
        # the French project page, desktop: the top, then a slow scroll (screencast)
        b, ctx = launch(p, 1920, 1080)
        pg = ctx.new_page()
        r = pg.goto(FR, wait_until="domcontentloaded", timeout=120000); res["fr_status"] = r.status
        pg.add_style_tag(content=HIDE)
        pg.wait_for_timeout(9000)
        pg.screenshot(path=os.path.join(out, "fr_top_1920.png"))
        cast = Cast(pg, os.path.join(out, "fr_cast_1920"), 1920, 1080); cast.start()
        pg.wait_for_timeout(800)
        for i in range(45):
            pg.mouse.wheel(0, 14); pg.wait_for_timeout(55)
        pg.wait_for_timeout(1200); cast.stop()
        lb = pg.locator(".nlptop-l").first
        pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(600)
        lb.screenshot(path=os.path.join(out, "fr_langbar_1920.png"))
        b.close()
        # the French page on a phone (for the vertical cut)
        b, ctx = launch(p, 390, 844, dpr=3, mobile=True)
        pg = ctx.new_page()
        pg.goto(FR, wait_until="domcontentloaded", timeout=120000)
        pg.add_style_tag(content=HIDE)
        pg.wait_for_timeout(9000)
        pg.screenshot(path=os.path.join(out, "fr_top_390.png"))
        b.close()
        # the English page: the dated price tile, the FAQ block, the language bar
        b, ctx = launch(p, 1440, 1000, dpr=2)
        pg = ctx.new_page()
        r = pg.goto(EN, wait_until="domcontentloaded", timeout=120000); res["en_status"] = r.status
        pg.add_style_tag(content=HIDE)
        pg.wait_for_timeout(7000)
        tile = pg.locator(".nlpf__item", has_text="Average price").first
        tile.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
        tile.screenshot(path=os.path.join(out, "en_price_tile.png"))
        facts = pg.locator(".nlpf").first
        facts.screenshot(path=os.path.join(out, "en_facts.png"))
        res["tile"] = tile.inner_text()
        h2 = pg.locator("h2", has_text="Frequently asked questions").first
        h2.scroll_into_view_if_needed(); pg.evaluate("() => window.scrollBy(0, -40)"); pg.wait_for_timeout(600)
        box = pg.evaluate("""() => { const h = [...document.querySelectorAll('h2')].find(x => x.textContent.includes('Frequently asked questions'));
            let el = h, last = h; for (let i = 0; i < 6; i++) { el = el.nextElementSibling; if (!el) break; last = el; }
            const a = h.getBoundingClientRect(), z = last.getBoundingClientRect(), par = h.parentElement.getBoundingClientRect();
            return [par.x - 8, a.y - 12, par.width + 16, z.bottom - a.y + 24]; }""")
        pg.screenshot(path=os.path.join(out, "en_faq.png"), clip={"x": box[0], "y": box[1], "width": box[2], "height": box[3]})
        pg.evaluate("() => window.scrollTo(0, 0)"); pg.wait_for_timeout(500)
        pg.locator(".nlptop-l").first.screenshot(path=os.path.join(out, "en_langbar.png"))
        b.close()
        json.dump(res, open(os.path.join(out, "pages.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(res)


if __name__ == "__main__":
    os.makedirs(sys.argv[2], exist_ok=True)
    if sys.argv[1] == "stage":
        stage(sys.argv[2], sys.argv[3])
    else:
        pages(sys.argv[2])
