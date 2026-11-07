# -*- coding: utf-8 -*-
"""Live captures for the developer film v3 (read-only page loads, analytics blocked in this browser only, nothing sent).

  python capture_v3.py tour360  <out> <WxH>   Rainbow's 360 example apartment (floor 25, toward the sea): a slow look
                                              around bare, then the page's own "עיצוב הדירה" choices (בהיר, עץ חם), then
                                              the roof pool scene of the same viewer
  python capture_v3.py walk     <out> <WxH>   /tour/sde-dov/: the quarter as planned ("הרובע 2035"), the free walk
                                              (the tour's own forward control), screencast
  python capture_v3.py hamedina <out> <WxH>   /projects/hamedina/: the page's walkable 3D scene, screencast + stills
  python capture_v3.py designer <out> <WxH>   /tour/designer/: enter, morning light, a piece of furniture and a note
                                              (the note stays in this browser: the page has no network call for it)
  python capture_v3.py planner  <out>         /marketing/ on a phone (390x844 @3): the campaign planner's five steps with
                                              its own controls; the last step is shown, never sent (the brief endpoint is
                                              blocked in this browser as a second guard)
  python capture_v3.py pages    <out>         /professionals/, /mortgage-calculator/, /purchase-tax-calculator/ (desktop
                                              first screen + a slow scroll screencast; phone first screen)
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"C:\Users\777\nad-lan\nad-lan-co-il\docs\sales\developer-film-v2\build")
from live_common import launch
from capture_tools import Cast, HIDE, HIDE_STICKY_JS
from playwright.sync_api import sync_playwright

B = "https://nad-lan.co.il"


def page(p, w, h, dpr=1, mobile=False):
    b, ctx = launch(p, w, h, dpr=dpr, mobile=mobile)
    ctx.route("**/campaign-brief**", lambda r: r.abort())
    pg = ctx.new_page(); pg.on("pageerror", lambda e: print("[pageerror]", str(e)[:160]))
    return b, ctx, pg


def drag(pg, x0, y0, dx, dy, steps=60, ms=30):
    pg.mouse.move(x0, y0); pg.mouse.down()
    for i in range(1, steps + 1):
        k = i / steps; k = k * k * (3 - 2 * k)
        pg.mouse.move(x0 + dx * k, y0 + dy * k); pg.wait_for_timeout(ms)
    pg.mouse.up()


def tour360(out, size):
    w, h = [int(x) for x in size.split("x")]; tag = f"{w}x{h}"
    with sync_playwright() as p:
        b, ctx, pg = page(p, w, h)
        r = pg.goto(B + "/projects/rainbow-tel-aviv/", wait_until="domcontentloaded", timeout=120000)
        log = {"url": r.url, "status": r.status, "taken": time.strftime("%Y-%m-%d %H:%M:%S"), "steps": []}
        pg.add_style_tag(content=HIDE); pg.wait_for_timeout(8000)
        pg.evaluate("() => document.getElementById('nlps-tour').scrollIntoView({block: 'center'})"); pg.wait_for_timeout(1500)
        pg.locator("#nlps-tour button", has_text="360").first.click(); pg.wait_for_timeout(9000)
        pg.add_style_tag(content=HIDE)
        pg.screenshot(path=os.path.join(out, f"t360_bare_{tag}.png"))
        cast = Cast(pg, os.path.join(out, f"t360_cast_{tag}"), w, h); cast.start(); pg.wait_for_timeout(700)
        cx, cy = w // 2, int(h * 0.45)
        drag(pg, cx + 200, cy, -420, 20, 70, 32); log["steps"].append("drag: look around (bare)"); pg.wait_for_timeout(700)
        cast.mark("light")
        pg.get_by_text("בהיר", exact=True).first.click(); log["steps"].append("click בהיר"); pg.wait_for_timeout(3500)
        drag(pg, cx + 300, cy, -760, 0, 90, 32); pg.wait_for_timeout(600)
        cast.mark("warm")
        pg.get_by_text("עם ריהוט · עץ חם").first.click(); log["steps"].append("click עם ריהוט · עץ חם"); pg.wait_for_timeout(3500)
        drag(pg, cx + 250, cy, -520, -10, 80, 32); pg.wait_for_timeout(800)
        pg.screenshot(path=os.path.join(out, f"t360_warm_{tag}.png"))
        cast.mark("pool")
        pg.get_by_text("הבריכה על הגג").first.click(); log["steps"].append("click הבריכה על הגג"); pg.wait_for_timeout(5000)
        drag(pg, cx + 150, cy, -380, 0, 80, 32); pg.wait_for_timeout(800)
        cast.stop()
        pg.screenshot(path=os.path.join(out, f"t360_pool_{tag}.png"))
        log["title"] = pg.evaluate("() => { const t = document.querySelector('.nlt-title, [class*=tour] h2, [class*=tour] .title'); return t ? t.innerText : null }")
        json.dump(log, open(os.path.join(out, f"t360_{tag}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(log); b.close()


def walk(out, size):
    w, h = [int(x) for x in size.split("x")]; tag = f"{w}x{h}"
    with sync_playwright() as p:
        b, ctx, pg = page(p, w, h)
        r = pg.goto(B + "/tour/sde-dov/", wait_until="domcontentloaded", timeout=120000)
        log = {"url": r.url, "status": r.status, "taken": time.strftime("%Y-%m-%d %H:%M:%S"), "steps": []}
        pg.add_style_tag(content=HIDE + " #waFab { display: none !important; }"); pg.wait_for_timeout(12000)
        pg.click("#year2035"); log["steps"].append("click הרובע 2035"); pg.wait_for_timeout(4000)
        pg.screenshot(path=os.path.join(out, f"walk_2035_{tag}.png"))
        cast = Cast(pg, os.path.join(out, f"walk_cast_{tag}"), w, h); cast.start(); pg.wait_for_timeout(500)
        pg.locator("button", has_text="התחילו סיור חופשי").first.click(); log["steps"].append("click התחילו סיור חופשי"); pg.wait_for_timeout(5000)
        cast.mark("walk")
        # the tour's own forward control, held (keyboard: ArrowUp walks forward in the free walk)
        pg.mouse.click(w // 2, int(h * 0.35)); pg.wait_for_timeout(300)
        pg.keyboard.down("ArrowUp"); pg.wait_for_timeout(5200); pg.keyboard.up("ArrowUp")
        pg.keyboard.down("ArrowLeft"); pg.wait_for_timeout(900); pg.keyboard.up("ArrowLeft")
        pg.keyboard.down("ArrowUp"); pg.wait_for_timeout(4200); pg.keyboard.up("ArrowUp")
        pg.wait_for_timeout(800)
        cast.stop()
        pg.screenshot(path=os.path.join(out, f"walk_end_{tag}.png"))
        json.dump(log, open(os.path.join(out, f"walk_{tag}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(log); b.close()


def hamedina(out, size):
    w, h = [int(x) for x in size.split("x")]; tag = f"{w}x{h}"
    with sync_playwright() as p:
        b, ctx, pg = page(p, w, h)
        r = pg.goto(B + "/projects/hamedina/", wait_until="domcontentloaded", timeout=120000)
        log = {"url": r.url, "status": r.status, "taken": time.strftime("%Y-%m-%d %H:%M:%S")}
        pg.add_style_tag(content=HIDE); pg.wait_for_timeout(12000)
        pg.screenshot(path=os.path.join(out, f"ham_top_{tag}.png"))
        log["buttons"] = pg.evaluate("""() => [...document.querySelectorAll('button, a.nlds-btn')].filter(b => b.offsetParent)
            .map(b => [b.innerText.trim().slice(0, 40), Math.round(b.getBoundingClientRect().x), Math.round(b.getBoundingClientRect().y + scrollY)]).slice(0, 60)""")
        json.dump(log, open(os.path.join(out, f"ham_{tag}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(json.dumps(log, ensure_ascii=False)[:3000]); b.close()


def designer(out, size):
    w, h = [int(x) for x in size.split("x")]; tag = f"{w}x{h}"
    with sync_playwright() as p:
        b, ctx, pg = page(p, w, h)
        r = pg.goto(B + "/tour/designer/", wait_until="domcontentloaded", timeout=120000)
        log = {"url": r.url, "status": r.status, "taken": time.strftime("%Y-%m-%d %H:%M:%S"), "steps": []}
        pg.wait_for_timeout(9000)
        cast = Cast(pg, os.path.join(out, f"des_cast_{tag}"), w, h); cast.start(); pg.wait_for_timeout(400)
        pg.click("#enterBtn"); log["steps"].append("click פתחו את הדלת"); pg.wait_for_timeout(5000)
        pg.get_by_role("button", name="בוקר").first.click(); log["steps"].append("click בוקר"); pg.wait_for_timeout(2500)
        cast.mark("furn")
        pg.click("#furnBtn"); log["steps"].append("click הוספת ריהוט"); pg.wait_for_timeout(2500)
        pg.screenshot(path=os.path.join(out, f"des_furn_{tag}.png"))
        log["sheet"] = pg.evaluate("() => { const s = document.getElementById('sheet'); return s ? s.innerText.slice(0, 400) : null }")
        json.dump(log, open(os.path.join(out, f"des_{tag}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        pg.wait_for_timeout(1500); cast.stop(); print(log); b.close()


def planner(out):
    T = '.nli-host[data-nli="nlcamp"]'
    with sync_playwright() as p:
        b, ctx, pg = page(p, 390, 844, dpr=3, mobile=True)
        r = pg.goto(B + "/marketing/", wait_until="domcontentloaded", timeout=120000)
        log = {"url": r.url, "status": r.status, "taken": time.strftime("%Y-%m-%d %H:%M:%S"), "steps": []}
        pg.add_style_tag(content=HIDE); pg.wait_for_timeout(8000)
        host = pg.locator(T).first; host.scroll_into_view_if_needed(); pg.wait_for_timeout(1500)
        pg.evaluate(HIDE_STICKY_JS)
        pg.wait_for_selector(T + " .nlcp")

        def press(sel, wt=200):
            pg.locator(sel).first.click(); pg.wait_for_timeout(wt); log["steps"].append("click " + sel.replace(T, "").strip())

        def nxt():
            press(T + ' button[data-act="next"]', 500)

        def shot(k):
            el = pg.locator(T + " .nlcp").first
            el.scroll_into_view_if_needed(); pg.wait_for_timeout(400); pg.evaluate(HIDE_STICKY_JS)
            el.screenshot(path=os.path.join(out, f"plan{k}.png"))
        press(f'{T} button.nlcp__chip[data-m="fr"]'); press(f'{T} button.nlcp__chip[data-m="ca"]'); shot(1); nxt()
        press(f'{T} label.nlcp__card:has(input[value="invest"])'); shot(2); nxt()
        f = pg.locator(T + ' input[data-f="budget"]').first; f.click(); f.press("Control+A"); f.press("Backspace"); f.type("25000"); pg.wait_for_timeout(300)
        pg.evaluate("() => document.activeElement && document.activeElement.blur()"); shot(3); nxt()
        press(f'{T} label.nlcp__card:has(input[value="existing"])')
        f = pg.locator(T + ' input[data-f="ref"]').first; f.click(); f.type("הפרויקט שלכם"); pg.wait_for_timeout(200)
        pg.evaluate("() => document.activeElement && document.activeElement.blur()"); shot(4); nxt()
        shot(5)
        try:
            log["count"] = pg.locator(T + " .nlcp__count").first.inner_text()
        except Exception:
            pass
        json.dump(log, open(os.path.join(out, "planner.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(json.dumps(log, ensure_ascii=False)); b.close()


def pages(out):
    res = {}
    with sync_playwright() as p:
        for slug in ["professionals", "mortgage-calculator", "purchase-tax-calculator"]:
            b, ctx, pg = page(p, 1920, 1080)
            r = pg.goto(f"{B}/{slug}/", wait_until="domcontentloaded", timeout=120000)
            pg.add_style_tag(content=HIDE); pg.wait_for_timeout(8000)
            res[slug] = {"url": r.url, "status": r.status, "title": pg.title(), "h1": pg.evaluate("() => (document.querySelector('h1') || {}).innerText || null")}
            pg.screenshot(path=os.path.join(out, f"pg_{slug}_1920.png"))
            cast = Cast(pg, os.path.join(out, f"pg_cast_{slug}"), 1920, 1080); cast.start(); pg.wait_for_timeout(500)
            for i in range(60):
                pg.mouse.wheel(0, 12); pg.wait_for_timeout(50)
            pg.wait_for_timeout(800); cast.stop()
            b.close()
            b, ctx, pg = page(p, 390, 844, dpr=3, mobile=True)
            pg.goto(f"{B}/{slug}/", wait_until="domcontentloaded", timeout=120000)
            pg.add_style_tag(content=HIDE); pg.wait_for_timeout(8000)
            pg.screenshot(path=os.path.join(out, f"pg_{slug}_390.png"))
            b.close()
            print(slug, res[slug], flush=True)
    json.dump(res, open(os.path.join(out, "pages.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    cmd, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    if cmd in ("tour360", "walk", "hamedina", "designer"):
        globals()[cmd](out, sys.argv[3])
    else:
        globals()[cmd](out)
