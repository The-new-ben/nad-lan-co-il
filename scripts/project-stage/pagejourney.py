"""The visitor's journey on a Rainbow page (local copy or live): the top at rest, floor 32 picked, west picked on its
ring, then the view card and the area map with the beam. Headless Chrome with SwiftShader.
usage: python pagejourney.py <url> <tag> [--mobile]"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

url, tag = sys.argv[1], sys.argv[2]
MOBILE = "--mobile" in sys.argv
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")
os.makedirs(OUT, exist_ok=True)
logs = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-gpu"])
    if MOBILE:
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
                            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36")
    else:
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.set_default_timeout(180000)
    page.on("console", lambda m: logs.append(f"[{m.type}] {m.text}"))
    page.on("pageerror", lambda e: logs.append(f"[pageerror] {e}"))
    page.goto(url, wait_until="load")
    time.sleep(3)
    page.screenshot(path=os.path.join(OUT, f"{tag}_1_top.png"))
    top = page.evaluate("() => { const r = document.getElementById('nlps').getBoundingClientRect(); return {y: r.top + scrollY, h: r.height}; }")
    page.evaluate(f"window.scrollTo(0, {max(0, top['y'] - 90)})")
    ok = True
    try:
        page.wait_for_function("window.__nlpsStage && window.__nlpsStage.phase && window.__nlpsStage.phase !== 'poster'", timeout=120000)
    except Exception as e:
        ok = False
        print("stage never left the poster:", e, page.evaluate("typeof window.__nlpsStage + ' ' + (window.__nlpsStage && window.__nlpsStage.phase)"))
    time.sleep(9)
    page.screenshot(path=os.path.join(OUT, f"{tag}_2_stage.png"))
    if ok:
        eng = "window.__nlpsStage._engine()"
        pt = page.evaluate(f"{eng}._floorScreenPoint(32)")
        (page.touchscreen.tap if MOBILE else page.mouse.click)(pt["x"], pt["y"])
        time.sleep(4)
        rp = page.evaluate(f"{eng}._ringScreenPoint(270, 32)")
        if rp:
            (page.touchscreen.tap if MOBILE else page.mouse.click)(rp["x"], rp["y"])
        time.sleep(4)
        page.screenshot(path=os.path.join(OUT, f"{tag}_3_picked.png"))
        print("selection", json.dumps(page.evaluate("window.__nlpsStage.getSelection()"), ensure_ascii=False))
        below = page.evaluate("() => { const r = document.querySelector('.nlps-below').getBoundingClientRect(); return r.top + scrollY; }")
        page.evaluate(f"window.scrollTo(0, {max(0, below - 80)})")
        time.sleep(10)
        page.screenshot(path=os.path.join(OUT, f"{tag}_4_below.png"))
        info = page.evaluate("""() => ({
            title: (document.getElementById('nlps-view-t')||{}).textContent,
            cap: (document.getElementById('nlps-view-cap')||{}).textContent,
            wa: (document.getElementById('nlps-wa')||{}).href,
            viewCanvas: !!document.querySelector('#nlps-view-map canvas'),
            cone: !!document.querySelector('.nlps-cone'),
            areaMap: !!window.NLPJX_MAP,
            h1: [...document.querySelectorAll('h1')].map(h => h.textContent.trim()),
            railSquare: !!document.querySelector('.nlbsq'), slot: !!document.querySelector('.nlbslot'),
            hScroll: document.documentElement.scrollWidth > innerWidth + 1,
        })""")
        print(json.dumps(info, ensure_ascii=False, indent=1))
        # example apartments (25.9.2026): the pick is an example apartment, and it says so everywhere; the address keeps it
        ex = page.evaluate("""() => {
            const s = window.__nlpsStage && window.__nlpsStage.getSelection();
            const lt = document.querySelector('.rbs-label-title');
            return { unit: s && s.unit, labelTitle: lt && lt.textContent, viewTitle: (document.getElementById('nlps-view-t') || {}).textContent,
                     kicker: (document.getElementById('nlps-view-k') || {}).textContent, url: location.search,
                     caption: (document.querySelector('.rbs-caption') || {}).textContent,
                     deals: document.querySelectorAll('.nlpd__table tbody tr').length, dealButtons: document.querySelectorAll('[data-nlps-floor]').length };
        }""")
        print("example", json.dumps(ex, ensure_ascii=False))
        if ex.get("dealButtons"):
            page.evaluate("document.getElementById('nlps-deals').scrollIntoView({block: 'center'})")
            time.sleep(1.5)
            page.screenshot(path=os.path.join(OUT, f"{tag}_6_deals.png"))
            btn = page.locator('[data-nlps-floor="6"]').first
            if btn.count():
                (btn.tap if MOBILE else btn.click)()
                time.sleep(4)
                print("deal button -> selection", json.dumps(page.evaluate("window.__nlpsStage.getSelection()"), ensure_ascii=False),
                      "| view title", page.evaluate("(document.getElementById('nlps-view-t') || {}).textContent"),
                      "| floor line", page.evaluate("(document.querySelector('.rbs-label-line') || {}).textContent"))
                page.screenshot(path=os.path.join(OUT, f"{tag}_7_dealfloor.png"))
        # the quarter (25.9.2026, design system QuarterPins): pins over our projects and places; a pin's card turns the stage
        qn = page.evaluate("document.querySelectorAll('.rbs-qpin').length")
        if qn:
            page.evaluate("document.getElementById('nlps').scrollIntoView({block: 'center'})")
            page.evaluate("window.__nlpsStage.clearFloor()")
            time.sleep(4)
            vis = page.evaluate("[...document.querySelectorAll('.rbs-qpin')].filter(b => b.style.visibility === 'visible').map(b => b.textContent)")
            print("quarter pins", qn, "| visible:", json.dumps(vis, ensure_ascii=False))
            page.screenshot(path=os.path.join(OUT, f"{tag}_8_quarter.png"))
            target = page.evaluate("(() => { const b = [...document.querySelectorAll('.rbs-qpin--project')].find(x => x.style.visibility === 'visible'); return b ? b.textContent : null; })()")
            if target:
                page.evaluate("(n) => [...document.querySelectorAll('.rbs-qpin')].find(x => x.textContent === n).click()", target)
                time.sleep(1.5)
                card = page.evaluate("(() => { const c = document.querySelector('.rbs-qcard'); return c && c.classList.contains('is-on') ? c.innerText : null; })()")
                print("quarter card:", (card or "").replace("\n", " | ")[:300])
                page.screenshot(path=os.path.join(OUT, f"{tag}_9_qcard.png"))
                page.evaluate("document.querySelector('.rbs-qcard-go') && document.querySelector('.rbs-qcard-go').click()")
                time.sleep(6)
                print("toward ->", json.dumps(page.evaluate("window.__nlpsStage.getSelection()"), ensure_ascii=False),
                      "| view title", page.evaluate("(document.getElementById('nlps-view-t') || {}).textContent"))
                page.screenshot(path=os.path.join(OUT, f"{tag}_10_toward.png"))
        # the quarter's legend under the stage (25.9.2026, design system version 23): a chip shows its group alone
        if ok and page.evaluate("document.querySelectorAll('[data-nlps-phase]').length"):
            page.evaluate("document.getElementById('nlps').scrollIntoView({block: 'center'})")
            page.evaluate("window.__nlpsStage.clearFloor()")
            time.sleep(2)
            vis = "[...document.querySelectorAll('.rbs-qpin--project')].filter(b => b.style.visibility === 'visible').map(b => b.textContent)"
            for ph in ("selling", "today", "building"):
                page.evaluate(f"document.querySelector('[data-nlps-phase=\"{ph}\"]').click()")
                time.sleep(1.5)
                print("legend", ph, "| pressed:", page.evaluate(f"document.querySelector('[data-nlps-phase=\"{ph}\"]').getAttribute('aria-pressed')"),
                      "| project pins:", json.dumps(page.evaluate(vis), ensure_ascii=False))
                if ph == "selling":
                    page.evaluate("document.querySelector('.qp-legend').scrollIntoView({block: 'end'})")
                    time.sleep(0.8)
                    page.screenshot(path=os.path.join(OUT, f"{tag}_11_legend.png"))
                    page.evaluate("document.getElementById('nlps').scrollIntoView({block: 'center'})")
            page.evaluate("document.querySelector('[data-nlps-phase=\"building\"]').click()")
            time.sleep(1)
            print("legend off | pressed:", page.evaluate("[...document.querySelectorAll('[data-nlps-phase]')].filter(b => b.getAttribute('aria-pressed') === 'true').length"),
                  "| project pins:", json.dumps(page.evaluate(vis), ensure_ascii=False))
    rail = page.evaluate("() => { const r = document.querySelector('.nlps-rail'); if (!r) return null; const b = r.getBoundingClientRect(); return b.top + scrollY; }")
    if rail is not None:
        page.evaluate(f"window.scrollTo(0, {max(0, rail - 80)})")
        time.sleep(1.5)
        page.screenshot(path=os.path.join(OUT, f"{tag}_5_rail.png"))
    b.close()
bad = [l for l in logs if ("error" in l.lower() and "favicon" not in l.lower()) or "pageerror" in l]
print("\n".join(bad[:25]))
