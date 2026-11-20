# -*- coding: utf-8 -*-
"""The opening stage of /my-rentals/ on the LIVE site, as a visitor who is not signed in (HAD-795).
Desktop 1440x900 and a phone width 390x664 (Chrome with a real GPU, NOT a real phone), he and en.
Presses the journey and takes the screenshots from the live page: the first screen, the world, a building in 3D,
the apartment's card, the Kikar tower. Nothing is typed, nothing is sent; the sign-up button is never pressed.
Usage: python scripts/rentals/live_pf.py"""
import sys, json, pathlib, random
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/rentals/build/opening/shots-live"
OUT.mkdir(parents=True, exist_ok=True)
SITE = "https://nad-lan.co.il/my-rentals/"
results = {"checks": [], "errors": []}
MARK = {"he": "(דוגמה)", "en": "(example)"}


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:260]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:190] if info != "" else ""))


def settle(pg, ms=15000):
    try:
        pg.wait_for_function("() => window.__nlpfMap && !window.__nlpfMap.isMoving() && window.__nlpfMap.areTilesLoaded()", timeout=ms)
    except Exception:  # noqa: BLE001
        pass
    pg.wait_for_timeout(900)


TOPMOST = """sel => [...document.querySelectorAll(sel)].map(e => { const b = e.getBoundingClientRect(), t = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2); return { ok: !!t && (t === e || e.contains(t)) && b.top >= 0 && b.bottom <= innerHeight, what: (e.textContent || e.className).trim().slice(0, 18), over: t ? (t.id || t.className).toString().slice(0, 18) : '' }; })"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--enable-gpu", "--use-angle=d3d11", "--ignore-gpu-blocklist", "--hide-scrollbars"])
    for lang in ("he", "en"):
        for w, h in ((1440, 900), (390, 664)):
            tag = "%s %dx%d" % (lang, w, h)
            phone = w < 700
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if phone else 1, has_touch=phone, is_mobile=phone, locale="he-IL",
                                user_agent=("Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36" if phone else None))
            pg = ctx.new_page(); errs = []; popups = []
            ctx.on("page", lambda g: popups.append(g.url))
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:140]))
            t0 = pg.evaluate("Date.now()")
            pg.goto(SITE + ("?lang=en&" if lang == "en" else "?") + "lv=%d" % random.randint(1000, 99999), wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_selector("#nlpf .nlpf-chip", timeout=20000)
            pg.wait_for_timeout(1200)
            s = pg.evaluate("""() => { const r = document.getElementById('nlpf'), q = x => [...r.querySelectorAll(x)], g = x => document.querySelector(x), cs = e => getComputedStyle(e);
              const h1 = g('.nlrm-hero h1').getBoundingClientRect(), sub = g('.nlrm-hero .sub').getBoundingClientRect(), st = r.getBoundingClientRect();
              return { admin: !!g('#wpadminbar'), cards: q('.nlpf-card').length, pics: q('.nlpf-card img').filter(i => i.complete && i.naturalWidth > 0).length, order: h1.top < sub.top && sub.bottom <= st.top + 1, h1s: document.querySelectorAll('h1').length,
                h1Top: Math.round(h1.top), subBottom: Math.round(sub.bottom), stTop: Math.round(st.top), stH: Math.round(st.height), stL: Math.round(st.left), stR: Math.round(innerWidth - st.right), H: innerHeight, overflowX: document.scrollingElement.scrollWidth - innerWidth,
                h1Font: cs(g('.nlrm-hero h1')).fontFamily.slice(0, 9), h1W: cs(g('.nlrm-hero h1')).fontWeight, cta: [cs(g('.nlrm-hero--after .nlrm-cta--go')).color, cs(g('.nlrm-hero--after .nlrm-cta--go')).backgroundColor],
                chipBg: cs(r.querySelector('.nlpf-chip:not(.is-on)')).backgroundColor, titleCol: cs(r.querySelector('.nlpf-title')).color, ver: (g('script[src*="portfolio/pf.js"]') || {}).src.split('v=')[1] }; }""")
            check("%s a visitor (not signed in) gets the stage of version %s: 8 pictures in the tray at once" % (tag, s["ver"]), not s["admin"] and s["cards"] == 8 and s["pics"] == 8, s)
            check("%s the page order: one h1, the answer paragraph, then the stage; the first screen holds all three (h1 at %d, paragraph ends %d, stage from %d, screen %d); no sideways overflow" % (tag, s["h1Top"], s["subBottom"], s["stTop"], s["H"]),
                  s["order"] and s["h1s"] == 1 and s["subBottom"] < s["H"] and s["stTop"] < s["H"] - 120 and s["overflowX"] <= 0, (s["order"], s["h1s"], s["overflowX"]))
            check("%s the look holds against the theme: h1 in Assistant 800, the main button white on ink, the stage's chips white, its title white" % tag,
                  "Assistant" in s["h1Font"] and s["h1W"] == "800" and s["cta"] == ["rgb(255, 255, 255)", "rgb(20, 33, 43)"] and s["chipBg"].startswith("rgba(255, 255, 255") and s["titleCol"] == "rgb(255, 255, 255)", (s["h1Font"], s["h1W"], s["cta"]))
            if phone:
                check("%s phone: the stage runs edge to edge (%d, %d) and is %d px tall" % (tag, s["stL"], s["stR"], s["stH"]), s["stL"] == 0 and s["stR"] == 0, s["stH"])
            try:
                pg.wait_for_selector("#nlpf.is-map", timeout=60000)
            except Exception:  # noqa: BLE001
                check("%s the 3D map is drawn" % tag, False, errs[:3]); pg.screenshot(path=str(OUT / ("%s-%d-fail.png" % (lang, w)))); ctx.close(); continue
            ms = pg.evaluate("Date.now()") - t0
            settle(pg, 25000)
            s = pg.evaluate("""() => { const r = document.getElementById('nlpf'), m = window.__nlpfMap; return { proj: m.getProjection().name, n: [...r.querySelectorAll('.nlpf-grp b')].reduce((a, e) => a + (+e.textContent), 0) + r.querySelectorAll('.nlpf-pin').length, gl: mapboxgl.version, stH: Math.round(r.getBoundingClientRect().height) }; }""")
            check("%s the globe is drawn about %.1f s after the page starts; its marks count all 8 properties" % (tag, ms / 1000.0), s["proj"] == "globe" and s["n"] == 8, s)
            pg.screenshot(path=str(OUT / ("%s-%d-1-first-screen.png" % (lang, w))))
            # the wheel / the page scroll is not captured
            if not phone:
                box = pg.evaluate("() => { const b = document.getElementById('nlpf').getBoundingClientRect(); return [b.left + b.width / 2, b.top + 200]; }")
                y0 = pg.evaluate("scrollY"); z0 = pg.evaluate("window.__nlpfMap.getZoom()")
                pg.mouse.move(box[0], box[1]); pg.mouse.wheel(0, 300); pg.wait_for_timeout(600)
                y1 = pg.evaluate("scrollY"); z1 = pg.evaluate("window.__nlpfMap.getZoom()")
                check("%s the wheel over the map scrolls the page (%d -> %d) and does not zoom the map" % (tag, y0, y1), y1 > y0 + 100 and abs(z1 - z0) < 0.01)
            pg.evaluate("scrollTo(0, Math.max(0, document.getElementById('nlpf').getBoundingClientRect().top + scrollY - (innerWidth < 700 ? 2 : 70)))"); pg.wait_for_timeout(700)
            pg.screenshot(path=str(OUT / ("%s-%d-2-world.png" % (lang, w))))
            if phone:
                c = pg.evaluate(TOPMOST, "#nlpf .nlpf-chip, #nlpf .nlpf-say button")
                tray = pg.evaluate("() => { const t = document.querySelector('#nlpf .nlpf-tray').getBoundingClientRect(), f = ['#nlcta', '.nlc-chip-fixed', '#nla11y'].map(s => document.querySelector(s)).filter(Boolean).map(e => e.getBoundingClientRect()).filter(b => b.height > 0 && b.top > innerHeight / 2).map(b => Math.round(b.top)); return { trayBottom: Math.round(t.bottom), floatsTop: f.length ? Math.min(...f) : null, floats: f.length }; }")
                check("%s phone, the stage at the top of the screen: the filter, the sentence button and the tray (ends at %s) are above the site's floating buttons (%s floating, the first at %s)" % (tag, tray["trayBottom"], tray["floats"], tray["floatsTop"]),
                      not [x for x in c if not x["ok"]] and (tray["floatsTop"] is None or tray["trayBottom"] <= tray["floatsTop"] + 1), [x for x in c if not x["ok"]][:2])
            # the property that needs care
            pg.evaluate("document.querySelector('#nlpf .nlpf-say [data-pick]').click()")
            pg.wait_for_timeout(3800); settle(pg, 20000)
            s = pg.evaluate("""() => { const r = document.getElementById('nlpf'), m = window.__nlpfMap, pin = r.querySelector('.nlpf-pin.is-sel'); return { say: r.querySelector('.nlpf-say').innerText.replace(/\\n/g, ' | '), zoom: +m.getZoom().toFixed(1), pitch: Math.round(m.getPitch()), pin: pin ? pin.className : '', own: m.queryRenderedFeatures({ layers: ['nlpf-own'] }).length, floors: m.queryRenderedFeatures({ layers: ['nlpf-floors'] }).length }; }""")
            check("%s 'see it' flies to the Eilat building: the map is tilted (%s degrees, zoom %s), the building's floors are drawn in 3D, the example floor is lit, the mark pulses" % (tag, s["pitch"], s["zoom"]), s["zoom"] > 15.5 and s["pitch"] > 50 and s["own"] >= 1 and s["floors"] >= 1 and "is-care" in s["pin"], s)
            pg.wait_for_timeout(1500)
            pg.screenshot(path=str(OUT / ("%s-%d-3-building-3d.png" % (lang, w))))
            pg.click("#nlpf .nlpf-say [data-open]")
            pg.wait_for_selector("#nlpf .nlpf-panel:not([hidden]) .nlpf-sheet", timeout=5000)
            pg.wait_for_timeout(2200)
            s = pg.evaluate("""() => { const r = document.getElementById('nlpf'), pn = r.querySelector('.nlpf-panel'), txt = pn.innerText;
              return { tenant: [...pn.querySelectorAll('.nlpf-fact b')].map(e => e.textContent), parts: pn.querySelectorAll('.nlpf-part').length, partPics: [...pn.querySelectorAll('.nlpf-part img')].filter(i => i.complete && i.naturalWidth > 0).length, care: [...pn.querySelectorAll('.nlpf-part.is-care em')].map(e => e.textContent),
                pic: pn.querySelector('.nlpf-pic').naturalWidth, ex: pn.querySelector('.nlpf-ex').textContent, note: pn.querySelector('.nlpf-note').textContent, scrolls: pn.scrollHeight > pn.clientHeight + 1, top: Math.round(r.getBoundingClientRect().top),
                links: [...r.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(x => /wa\\.me|^tel:|^mailto:/i.test(x)), nums: txt.match(/(?:\\+?972|0)5\\d[\\s-]?\\d{3}[\\s-]?\\d{4}/g) || [], mails: txt.match(/[\\w.]+@[\\w.]+/g) || [] }; }""")
            check("%s the apartment's card: the building's picture, rent, a tenant marked %s, 5 parts as pictures with the air conditioner asking for care, the example tag and note; no inner scroll" % (tag, MARK[lang]),
                  s["pic"] > 0 and s["parts"] == 5 and s["partPics"] == 5 and len(s["care"]) == 1 and MARK[lang] in s["tenant"][1] and len(s["ex"]) > 3 and len(s["note"]) > 6 and not s["scrolls"], s)
            check("%s no chat, call or mail link and no phone-shaped number or address anywhere in the stage" % tag, not s["links"] and not s["nums"] and not s["mails"], (s["links"], s["nums"], s["mails"]))
            if phone:
                bt = pg.evaluate(TOPMOST, "#nlpf .nlpf-panel button, #nlpf .nlpf-panel a")
                check("%s phone: the card opened with the stage at the top (top %d) and every one of its %d buttons is on screen, under no floating button of the site" % (tag, s["top"], len(bt)), -3 <= s["top"] <= 6 and not [x for x in bt if not x["ok"]], [x for x in bt if not x["ok"]][:2])
            pg.screenshot(path=str(OUT / ("%s-%d-4-apartment-card.png" % (lang, w))))
            pg.click("#nlpf [data-back]"); pg.wait_for_timeout(500)
            # the Kikar tower
            pg.evaluate("document.querySelector(\"#nlpf .nlpf-card[data-id='k2']\").click()")
            pg.wait_for_timeout(3800); settle(pg, 20000)
            pg.screenshot(path=str(OUT / ("%s-%d-5-kikar-3d.png" % (lang, w))))
            pg.click("#nlpf .nlpf-say [data-open]")
            pg.wait_for_selector("#nlpf .nlpf-turn img", timeout=5000)
            pg.wait_for_timeout(5600)
            s = pg.evaluate("""() => { const pn = document.querySelector('#nlpf .nlpf-panel'); return { img: pn.querySelector('.nlpf-turn img').naturalWidth, tags: [...pn.querySelectorAll('.nlpf-tag')].map(e => e.innerText.replace(/\\n/g, ' ')), bands: pn.querySelectorAll('.nlpf-fl').length, frame: pn.querySelector('.nlpf-turn img').src.split('/').pop(), dev: /דימרי|dimri|ישראל קנדה|canada|אקרו|acro/i.test(pn.innerText), ex: pn.querySelector('.nlpf-ex').textContent, scrolls: pn.scrollHeight > pn.clientHeight + 1 }; }""")
            tb = pg.evaluate("() => { const b = document.querySelector('#nlpf .nlpf-vis').getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height * 0.3]; }")
            pg.mouse.move(tb[0], tb[1]); pg.mouse.down(); pg.mouse.move(tb[0] + 60, tb[1], steps=6); pg.mouse.move(tb[0] + 110, tb[1], steps=6); pg.mouse.up(); pg.wait_for_timeout(250)
            f2 = pg.evaluate("document.querySelector('#nlpf .nlpf-turn img').src.split('/').pop()")
            check("%s the Kikar tower comes forward: the tower render, 2 lit floors, 2 example apartments to press, marked as an example, no developer name; it turns under a drag (%s -> %s)" % (tag, s["frame"], f2),
                  s["img"] > 0 and s["bands"] == 2 and len(s["tags"]) == 2 and not s["dev"] and len(s["ex"]) > 3 and f2 != s["frame"] and not s["scrolls"], s)
            pg.screenshot(path=str(OUT / ("%s-%d-6-kikar-tower.png" % (lang, w))))
            sh0 = pg.evaluate("document.querySelector('#nlpf .nlpf-s-h b').textContent")
            pg.click("#nlpf .nlpf-tag:not(.is-on)"); pg.wait_for_timeout(1000)
            check("%s a press on the other apartment in the tower opens its card" % tag, pg.evaluate("document.querySelector('#nlpf .nlpf-s-h b').textContent") != sh0)
            pg.click("#nlpf [data-back]"); pg.wait_for_timeout(400)
            pg.click("#nlpf .nlpf-chip--care"); pg.wait_for_timeout(300)
            n1 = pg.evaluate("document.querySelectorAll('#nlpf .nlpf-card').length")
            pg.click("#nlpf .nlpf-chip--all"); pg.wait_for_timeout(300)
            check("%s the filter works (needs care: 1 card; all: 8)" % tag, n1 == 1 and pg.evaluate("document.querySelectorAll('#nlpf .nlpf-card').length") == 8, n1)
            check("%s nothing opened a tab or left the page; no page errors" % tag, not popups and "/my-rentals/" in pg.url and not errs, (popups[:2], errs[:3]))
            ctx.close()
    b.close()

ok = sum(1 for c in results["checks"] if c["ok"]); n = len(results["checks"])
(ROOT / "docs/rentals/build/opening/live-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nRESULT %d/%d checks passed (the live site, as a visitor)" % (ok, n))
sys.exit(0 if ok == n else 1)
