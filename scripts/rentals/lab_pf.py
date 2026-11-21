# -*- coding: utf-8 -*-
"""The opening stage of /my-rentals/ (HAD-795, board 5): lab run of the real files (inc/rentals/portfolio.php through
scripts/rentals/build_pf_lab.php, assets/rentals/portfolio/pf.js + pf.css) in a page whose theme stand-in forces button
and heading colours the way the live theme does.
The map key is read at run time from the public page source and passed in the address; never printed, never written.
Chrome with a real GPU (the globe needs it), NOT a real phone.
Usage: python scripts/rentals/lab_pf.py   (server at the repo root: python -m http.server 47921)"""
import re, sys, json, pathlib, subprocess
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/rentals/build/opening/shots-lab"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "http://127.0.0.1:47921/docs/design-lab/rentals-portfolio/stage-%s.html?t=%s"
html = subprocess.run(["curl", "-s", "https://nad-lan.co.il/my-rentals/"], capture_output=True).stdout.decode("utf-8", "replace")
m = re.search(r"pk\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+", html)
if not m:
    sys.exit("no map key found in the public page")
KEY = m.group(0)
results = {"checks": [], "errors": []}
MARK = {"he": "(דוגמה)", "en": "(example)"}


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info).replace(KEY, "…")[:260]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info).replace(KEY, "…")[:190] if info != "" else ""))


def settle(pg, ms=9000):
    try:
        pg.wait_for_function("() => window.__nlpfMap && !window.__nlpfMap.isMoving() && window.__nlpfMap.areTilesLoaded()", timeout=ms)
    except Exception:  # noqa: BLE001
        pass
    pg.wait_for_timeout(700)


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--enable-gpu", "--use-angle=d3d11", "--ignore-gpu-blocklist", "--hide-scrollbars"])
    for lang in ("he", "en"):
        for w, h in ((1280, 800), (390, 664)):
            tag = "%s %dx%d" % (lang, w, h)
            phone = w < 700
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if phone else 1, has_touch=phone, locale="he-IL")
            popups = []; ctx.on("page", lambda g: popups.append(g.url))
            pg = ctx.new_page(); errs = []; popups.clear()
            pg.on("response", lambda r: errs.append("%d %s" % (r.status, r.url.split("?")[0][-70:])) if r.status >= 400 and "favicon" not in r.url else None)
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
            pg.on("console", lambda msg: errs.append("console: " + msg.text[:150]) if msg.type == "error" and "Failed to load resource" not in msg.text else None)
            # --- first paint: hold the map library back, the stage must already work
            held = []
            pg.route(re.compile(r"api\.mapbox\.com/mapbox-gl-js/v3\.14\.0/mapbox-gl\.js"), lambda r: held.append(r))
            pg.goto(BASE % (lang, KEY), wait_until="domcontentloaded")
            pg.wait_for_selector("#nlpf .nlpf-chip", timeout=8000)
            pg.wait_for_timeout(900)
            s = pg.evaluate("""() => { const r = document.getElementById('nlpf'), q = s => [...r.querySelectorAll(s)];
              const h1 = document.querySelector('.nlrm-hero h1').getBoundingClientRect(), sub = document.querySelector('.nlrm-hero .nlrm-one').getBoundingClientRect(), st = r.getBoundingClientRect();
              const po = r.querySelector('.nlpf-poster img'), lk = document.querySelector('.nlrm-hero .nlrm-lk'), para = document.querySelector('.nlrm-hero--after .sub'), stp = [...document.querySelectorAll('.nlrm-steps .nlrm-step')];
              const cs = e => getComputedStyle(e);
              return { cards: q('.nlpf-card').length, pics: q('.nlpf-card img').filter(i => i.complete && i.naturalWidth > 0).length, chips: q('.nlpf-chip').map(c => c.textContent.trim()), say: r.querySelector('.nlpf-say').innerText,
                ex: r.querySelector('.nlpf-ex').textContent, order: h1.top < sub.top && sub.bottom <= st.top + 1,
                poster: !!po && po.complete && po.naturalWidth > 0 && cs(r.querySelector('.nlpf-poster')).opacity === '1', posterSrc: po ? po.currentSrc.split('/').pop().split('?')[0] : '',
                lockup: lk ? lk.innerText.replace(/\s+/g, ' ').trim() : '', lockAbove: !!lk && lk.getBoundingClientRect().bottom <= h1.top + 1, one: document.querySelector('.nlrm-one').textContent, paraAfter: !!para && para.getBoundingClientRect().top >= st.bottom - 1 && para.textContent.length > 80,
                steps: stp.map(e => getComputedStyle(e, '::before').backgroundImage.replace(/.*\//, '').replace(/[\")]+$/, '')), stepNum: stp.map(e => cs(e.querySelector('i')).position + ':' + cs(e.querySelector('i')).backgroundColor), stepLabel: stp.length ? getComputedStyle(stp[0], '::after').content : '', subBottom: Math.round(sub.bottom), stTop: Math.round(st.top), stH: Math.round(st.height), H: innerHeight,
                chipBg: cs(r.querySelector('.nlpf-chip:not(.is-on)')).backgroundColor, cardBg: cs(r.querySelector('.nlpf-card')).backgroundColor, cardRadius: cs(r.querySelector('.nlpf-card')).borderTopLeftRadius, tt: cs(r.querySelector('.nlpf-chip')).textTransform,
                titleCol: cs(r.querySelector('.nlpf-title')).color, overflowX: document.scrollingElement.scrollWidth - innerWidth, h1s: document.querySelectorAll('h1').length,
                small: q('button').filter(e => { const b = e.getBoundingClientRect(); return b.width > 0 && (b.height < 44 || b.width < 44); }).map(e => e.className) }; }""")
            check("%s first paint, map library held back: 9 apartment cards with their pictures, 4 filter chips, the sentence, the example tag" % tag, s["cards"] == 9 and s["pics"] == 9 and len(s["chips"]) == 4 and len(s["say"]) > 8 and len(s["ex"]) > 3, s)
            check("%s the page order: the product's lockup, h1, one plain sentence, then the stage; the page's long paragraph follows the stage word for word; one h1; no sideways overflow" % tag,
                  s["order"] and s["h1s"] == 1 and s["overflowX"] <= 0 and s["lockAbove"] and len(s["lockup"]) >= 8 and len(s["one"]) > 30 and s["paraAfter"], (s["order"], s["h1s"], s["overflowX"], s["lockup"], s["lockAbove"], s["paraAfter"]))
            check("%s first paint, map library held back: the still globe with its marks is drawn (%s)" % (tag, s["posterSrc"]), s["poster"] and ("phone" in s["posterSrc"]) == phone and lang in s["posterSrc"], s["posterSrc"])
            check("%s each of the three steps carries a picture, its number is a small tag on it, and the picture is labelled" % tag, s["steps"] == ["t1-720.webp", "k1-720.webp", "c1-720.webp"] and all(x == "absolute:rgb(20, 33, 43)" for x in s["stepNum"]) and len(s["stepLabel"]) > 4, (s["steps"], s["stepNum"], s["stepLabel"]))
            check("%s the first screen holds the h1, the sentence and the top of the stage (sentence ends %d, stage starts %d, screen %d)" % (tag, s["subBottom"], s["stTop"], s["H"]), s["subBottom"] < s["H"] and s["stTop"] < s["H"] - 120, s["stH"])
            check("%s the theme's forced button colours do not reach the stage (chip white, card white, radius 18, no upper case, title white)" % tag,
                  s["chipBg"].startswith("rgba(255, 255, 255") and s["cardBg"] == "rgb(255, 255, 255)" and s["cardRadius"] == "18px" and s["tt"] == "none" and s["titleCol"] == "rgb(255, 255, 255)", (s["chipBg"], s["cardBg"], s["cardRadius"], s["tt"], s["titleCol"]))
            check("%s every button of the stage is at least 44 px" % tag, not s["small"], s["small"][:4])
            hs = pg.evaluate("""() => { const c = getComputedStyle(document.querySelector('.nlrm-hero h1')), a = getComputedStyle(document.querySelector('.nlrm-hero--after .nlrm-cta--go')); return [c.fontFamily.slice(0, 9), c.fontWeight, a.color, a.backgroundColor]; }""")
            check("%s the theme's forced serif and link colour do not reach the page's h1 and main button (Assistant 800; white on ink)" % tag, "Assistant" in hs[0] and hs[1] == "800" and hs[2] == "rgb(255, 255, 255)" and hs[3] == "rgb(20, 33, 43)", hs)
            pg.screenshot(path=str(OUT / ("%s-%d-0-first-paint.png" % (lang, w))))
            # without the map a card press opens the building at once
            pg.click("#nlpf .nlpf-card[data-id='u11']")
            pg.wait_for_selector("#nlpf .nlpf-panel:not([hidden]) .nlpf-sheet", timeout=4000)
            check("%s without the map a press on a card opens the building and the apartment's card" % tag, True)
            pg.click("#nlpf [data-back]")
            # --- the map arrives
            for r in held:
                r.continue_()
            pg.unroute(re.compile(r"api\.mapbox\.com/mapbox-gl-js/v3\.14\.0/mapbox-gl\.js"))
            try:
                pg.wait_for_selector("#nlpf.is-map", timeout=60000)
            except Exception:  # noqa: BLE001
                check("%s the map is drawn" % tag, False, errs[:3]); ctx.close(); continue
            settle(pg, 20000)
            s = pg.evaluate("""() => { const r = document.getElementById('nlpf'), m = window.__nlpfMap; return { marks: [...r.querySelectorAll('.nlpf-marks > *')].map(e => e.className.split(' ')[0] + ':' + (e.textContent || '').trim().slice(0, 18)), zoom: m.getZoom(), proj: m.getProjection().name, layers: ['nlpf-arcs', 'nlpf-floors', 'nlpf-own', 'nlpf-glow'].filter(l => m.getLayer(l)).length, n: [...r.querySelectorAll('.nlpf-grp b')].reduce((a, e) => a + (+e.textContent), 0) + r.querySelectorAll('.nlpf-pin').length }; }""")
            pg.wait_for_timeout(1100)
            check("%s when the live map is ready the still globe is gone" % tag, pg.evaluate("() => { const c = getComputedStyle(document.querySelector('#nlpf .nlpf-poster')); return c.opacity === '0' || c.visibility === 'hidden'; }"))
            check("%s the map is a globe; the far marks together count all 9 apartments; our 4 layers are in" % tag, s["proj"] == "globe" and s["n"] == 9 and s["layers"] == 4, s)
            pg.screenshot(path=str(OUT / ("%s-%d-1-world.png" % (lang, w))))
            # the wheel over the stage scrolls the page (desktop); a finger drag over the stage scrolls the page (phone)
            box = pg.evaluate("() => { const b = document.getElementById('nlpf').getBoundingClientRect(); return [b.left + b.width / 2, b.top + Math.min(b.height, innerHeight - b.top) / 2]; }")
            z0 = pg.evaluate("window.__nlpfMap.getZoom()"); y0 = pg.evaluate("scrollY")
            pg.mouse.move(box[0], box[1]); pg.mouse.wheel(0, 240); pg.wait_for_timeout(500)
            y1 = pg.evaluate("scrollY"); z1 = pg.evaluate("window.__nlpfMap.getZoom()")
            check("%s the wheel over the map scrolls the page and does not zoom the map (page %d -> %d)" % (tag, y0, y1), y1 > y0 + 100 and abs(z1 - z0) < 0.01, (z0, z1))
            pg.evaluate("scrollTo(0, Math.max(0, document.getElementById('nlpf').getBoundingClientRect().top + scrollY - 70))"); pg.wait_for_timeout(300)
            # --- the sentence points at the apartment that needs care (Kikar HaMedina, example apartment A); first a quiet one: Eilat
            check("%s the sentence offers the one apartment that needs care now" % tag, pg.evaluate("() => { const b = document.querySelector('#nlpf .nlpf-say [data-pick]'); return b ? b.getAttribute('data-pick') : ''; }") == "u21")
            pg.evaluate("document.querySelector(\"#nlpf .nlpf-card[data-id='u31']\").scrollIntoView({ inline: 'center', block: 'nearest' })"); pg.wait_for_timeout(250)
            pg.click("#nlpf .nlpf-card[data-id='u31']")
            pg.wait_for_timeout(3600); settle(pg, 15000)
            s = pg.evaluate("""() => { const r = document.getElementById('nlpf'), m = window.__nlpfMap; const pin = r.querySelector('.nlpf-pin.is-sel');
              return { say: r.querySelector('.nlpf-say').innerText.replace(/\\n/g, ' | '), zoom: m.getZoom(), pitch: m.getPitch(), pin: pin ? pin.className : '', nm: pin && pin.querySelector('.nlpf-nm') ? pin.querySelector('.nlpf-nm').textContent : '', own: m.queryRenderedFeatures({ layers: ['nlpf-own'] }).length, floors: m.queryRenderedFeatures({ layers: ['nlpf-floors'] }).length, world: !r.querySelector('.nlpf-world').hidden }; }""")
            check("%s a press on the Eilat card flies to its building in 3D: tilted, its floors drawn, the example floor lit, and the mark carries the building's name (%s)" % (tag, s["nm"]), s["zoom"] > 15.5 and s["pitch"] > 50 and s["own"] >= 1 and s["floors"] >= 1 and "is-sel" in s["pin"] and len(s["nm"]) > 3 and s["world"], s)
            pg.screenshot(path=str(OUT / ("%s-%d-2-eilat-3d.png" % (lang, w))))
            # the building turns by itself when nobody touches it
            b0 = pg.evaluate("window.__nlpfMap.getBearing()"); pg.wait_for_timeout(7600); b1 = pg.evaluate("window.__nlpfMap.getBearing()")
            check("%s the selected building turns slowly by itself (%.1f -> %.1f degrees)" % (tag, b0, b1), abs(b1 - b0) > 1.5)
            # a press on the lit floor in the 3D map opens the apartment
            pt = pg.evaluate("""() => { const m = window.__nlpfMap, c = m.getCanvas().getBoundingClientRect(); for (let y = 60; y < c.height - 60; y += 6) { for (let x = 20; x < c.width - 20; x += 6) { const f = m.queryRenderedFeatures([x, y], { layers: ['nlpf-own'] }); if (f.length) { const top = document.elementFromPoint(c.left + x, c.top + y); if (top && top.closest('.mapboxgl-canvas-container, .mapboxgl-canvas')) { return [c.left + x, c.top + y]; } } } } return null; }""")
            if pt:
                pg.mouse.click(pt[0], pt[1])
                try:
                    pg.wait_for_selector("#nlpf .nlpf-panel:not([hidden]) .nlpf-sheet", timeout=4000); okf = True
                except Exception:  # noqa: BLE001
                    okf = False
                check("%s a press on the lit floor of the 3D building opens the apartment's card" % tag, okf)
            else:
                check("%s a press on the lit floor of the 3D building opens the apartment's card" % tag, False, "the lit floor is not under a free point of the map")
                pg.click("#nlpf .nlpf-say [data-open]")
                pg.wait_for_selector("#nlpf .nlpf-panel:not([hidden]) .nlpf-sheet", timeout=4000)
            pg.wait_for_timeout(1900)
            s = pg.evaluate("""() => { const r = document.getElementById('nlpf'), pn = r.querySelector('.nlpf-panel'), sh = pn.querySelector('.nlpf-sheet'), pb = pn.getBoundingClientRect(), sb = sh.getBoundingClientRect(), rb = r.getBoundingClientRect();
              const txt = pn.innerText, pic = pn.querySelector('.nlpf-pic');
              return { title: pn.querySelector('.nlpf-p-t').innerText.replace(/\\n/g, ' | '), tenant: [...pn.querySelectorAll('.nlpf-fact b')].map(e => e.textContent), parts: pn.querySelectorAll('.nlpf-part').length, care: [...pn.querySelectorAll('.nlpf-part.is-care em')].map(e => e.textContent),
                partPics: [...pn.querySelectorAll('.nlpf-part img')].filter(i => i.complete && i.naturalWidth > 0).length, pic: !!pic && pic.complete && pic.naturalWidth > 0, st: pn.querySelector('.nlpf-st').textContent, ex: pn.querySelector('.nlpf-ex').textContent, note: pn.querySelector('.nlpf-note').textContent,
                inside: sb.bottom <= rb.bottom + 1 && pb.top >= rb.top - 1, enter: (pn.querySelector('[data-enter]') || { getAttribute() { return ''; } }).getAttribute('href'), scrolls: pn.scrollHeight > pn.clientHeight + 1, visH: Math.round(pn.querySelector('.nlpf-vis').getBoundingClientRect().height), cta: pn.querySelector('[data-cta]').getAttribute('href'),
                links: [...r.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(x => /wa\\.me|^tel:|^mailto:/i.test(x)), nums: txt.match(/(?:\\+?972|0)5\\d[\\s-]?\\d{3}[\\s-]?\\d{4}/g) || [], mails: txt.match(/[\\w.]+@[\\w.]+/g) || [],
                small: [...pn.querySelectorAll('button, a')].filter(e => { const b = e.getBoundingClientRect(); return b.height < 44 || b.width < 44; }).map(e => e.className),
                cut: [...pn.querySelectorAll('.nlpf-btn, .nlpf-s-h b, .nlpf-fact b')].filter(e => e.scrollWidth > e.clientWidth + 1).map(e => e.textContent.slice(0, 24)) }; }""")
            check("%s the Eilat apartment's card: picture, state, rent, a tenant marked %s, 5 parts as pictures, the example tag and note, and 'enter the apartment' leads to that apartment's real screens" % (tag, MARK[lang]),
                  s["pic"] and s["parts"] == 5 and s["partPics"] == 5 and len(s["care"]) == 0 and MARK[lang] in s["tenant"][1] and "sample=1" in s["enter"] and s["enter"].endswith("u=31#/today/31") and len(s["ex"]) > 3 and len(s["note"]) > 6, s)
            check("%s the card fits the stage with no inner scrolling (picture area %d px), buttons at least 44 px, no text cut" % (tag, s["visH"]), s["inside"] and not s["scrolls"] and s["visH"] >= 140 and not s["small"] and not s["cut"], (s["inside"], s["scrolls"], s["small"], s["cut"]))
            check("%s no chat, call or mail link and no phone-shaped number or address in the stage" % tag, not s["links"] and not s["nums"] and not s["mails"], (s["links"], s["nums"], s["mails"]))
            pg.screenshot(path=str(OUT / ("%s-%d-3-eilat-card.png" % (lang, w))))
            pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
            check("%s Escape closes the card" % tag, pg.evaluate("document.querySelector('#nlpf .nlpf-panel').hidden"))
            # --- the Kikar tower: two example apartments, the render turns under the finger
            pg.evaluate("document.querySelector(\"#nlpf .nlpf-card[data-id='u21']\").scrollIntoView({ inline: 'center', block: 'nearest' })")
            pg.wait_for_timeout(250)
            pg.click("#nlpf .nlpf-card[data-id='u21']")
            pg.wait_for_timeout(3600); settle(pg, 15000)
            pg.screenshot(path=str(OUT / ("%s-%d-4-kikar-3d.png" % (lang, w))))
            pg.click("#nlpf .nlpf-say [data-open]")
            pg.wait_for_selector("#nlpf .nlpf-turn img", timeout=4000)
            f0 = pg.evaluate("document.querySelector('#nlpf .nlpf-turn img').src.split('/').pop()")
            pg.wait_for_timeout(5200)
            s = pg.evaluate("""() => { const pn = document.querySelector('#nlpf .nlpf-panel'), tr = pn.querySelector('.nlpf-turn').getBoundingClientRect(), vis = pn.querySelector('.nlpf-vis').getBoundingClientRect();
              return { tags: [...pn.querySelectorAll('.nlpf-tag')].map(e => e.innerText.replace(/\\n/g, ' ') + (e.classList.contains('is-on') ? ' *' : '')), bands: pn.querySelectorAll('.nlpf-fl').length, frame: pn.querySelector('.nlpf-turn img').src.split('/').pop(), img: pn.querySelector('.nlpf-turn img').naturalWidth,
                title: pn.querySelector('.nlpf-p-t').innerText.replace(/\\n/g, ' | '), sheet: pn.querySelector('.nlpf-s-h b').textContent, care: [...pn.querySelectorAll('.nlpf-part.is-care em')].map(e => e.textContent), tw: Math.round(tr.width), th: Math.round(tr.height), in: tr.left >= vis.left - 1 && tr.right <= vis.right + 1,
                bandFree: [...pn.querySelectorAll('.nlpf-fl')].every(e => { const b = e.getBoundingClientRect(), t = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2); return b.top >= vis.top && b.bottom <= vis.bottom && !(t && t.closest('.nlpf-tag')); }),
                onMid: (() => { const b = pn.querySelector('.nlpf-fl.is-on').getBoundingClientRect(); return Math.abs((b.top + b.height / 2) - (vis.top + vis.height / 2)) < 30; })(),
                tagsIn: [...pn.querySelectorAll('.nlpf-tag')].every(e => { const b = e.getBoundingClientRect(); return b.left >= vis.left && b.right <= vis.right && b.top >= vis.top && b.bottom <= vis.bottom; }), scrolls: pn.scrollHeight > pn.clientHeight + 1, dev: /דימרי|dimri|ישראל קנדה|canada/i.test(pn.innerText) }; }""")
            check("%s the Kikar tower comes forward: the tower render with 2 lit floors and 2 example apartments to press, no developer name" % tag, s["img"] > 0 and s["bands"] == 2 and len(s["tags"]) == 2 and s["tagsIn"] and s["in"] and s["bandFree"] and s["onMid"] and s["tw"] >= 180 and not s["dev"] and not s["scrolls"] and len(s["care"]) == 1, s)
            turned = pg.evaluate("window.__f = document.querySelector('#nlpf .nlpf-turn img').src.split('/').pop()")
            tb = pg.evaluate("() => { const b = document.querySelector('#nlpf .nlpf-vis').getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height * 0.3]; }")
            pg.mouse.move(tb[0], tb[1]); pg.mouse.down(); pg.mouse.move(tb[0] + 60, tb[1], steps=6); pg.mouse.move(tb[0] + 110, tb[1], steps=6); pg.mouse.up(); pg.wait_for_timeout(200)
            f2 = pg.evaluate("document.querySelector('#nlpf .nlpf-turn img').src.split('/').pop()")
            check("%s the tower turns under a drag (frame %s -> %s)" % (tag, turned, f2), f2 != turned, f0)
            pg.screenshot(path=str(OUT / ("%s-%d-5-kikar-tower.png" % (lang, w))))
            pg.click("#nlpf .nlpf-tag:not(.is-on)")
            pg.wait_for_timeout(900)
            s2 = pg.evaluate("() => ({ sheet: document.querySelector('#nlpf .nlpf-s-h b').textContent, on: document.querySelector('#nlpf .nlpf-tag.is-on').innerText.replace(/\\n/g, ' ') })")
            mid = pg.evaluate("() => { const pn = document.querySelector('#nlpf .nlpf-panel'), vis = pn.querySelector('.nlpf-vis').getBoundingClientRect(), b = pn.querySelector('.nlpf-fl.is-on').getBoundingClientRect(); return Math.abs((b.top + b.height / 2) - (vis.top + vis.height / 2)) < 30; }")
            check("%s a press on the other apartment in the tower opens its card and slides the tower to its floor" % tag, s2["sheet"] != s["sheet"] and mid, s2)
            pg.screenshot(path=str(OUT / ("%s-%d-6-kikar-other.png" % (lang, w))))
            pg.click("#nlpf [data-back]"); pg.wait_for_timeout(400)
            # --- the filter and the way back to the whole world
            pg.click("#nlpf .nlpf-chip--care"); pg.wait_for_timeout(300)
            n1 = pg.evaluate("document.querySelectorAll('#nlpf .nlpf-card').length")
            pg.click("#nlpf .nlpf-chip--ok"); pg.wait_for_timeout(300)
            n2 = pg.evaluate("document.querySelectorAll('#nlpf .nlpf-card').length")
            pg.click("#nlpf .nlpf-chip--all"); pg.wait_for_timeout(300)
            check("%s the filter: urgent 1, in order 5, all 9" % tag, n1 == 1 and n2 == 5 and pg.evaluate("document.querySelectorAll('#nlpf .nlpf-card').length") == 9, (n1, n2))
            pg.click("#nlpf .nlpf-world"); pg.wait_for_timeout(3400); settle(pg, 12000)
            z = pg.evaluate("window.__nlpfMap.getZoom()")
            check("%s 'the whole world' flies back out" % tag, z < 2.5, z)
            check("%s nothing opened a tab or left the page" % tag, not popups and "stage-%s.html" % lang in pg.url, popups[:2])
            bad = [e for e in errs if "WebGL" not in e and "GPU" not in e]
            check("%s no page errors" % tag, not bad, bad[:3])
            ctx.close()
    # --- a phone WITH the site's floating buttons (stand-ins at the live positions): the stage takes the free height
    for lang in ("he", "en"):
        for w, h in ((390, 664), (360, 620)):
            tag = "%s %dx%d with the site's floating buttons" % (lang, w, h)
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, has_touch=True, locale="he-IL")
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
            pg.goto((BASE % (lang, KEY)) + "&floats=1", wait_until="domcontentloaded")
            try:
                pg.wait_for_selector("#nlpf.is-map", timeout=60000)
            except Exception:  # noqa: BLE001
                check("%s the map is drawn" % tag, False, errs[:3]); ctx.close(); continue
            pg.wait_for_timeout(2600)
            TOPMOST0 = """sel => [...document.querySelectorAll(sel)].map(e => { const b = e.getBoundingClientRect(), t = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2); return { ok: !!t && (t === e || e.contains(t)) && b.top >= 0 && b.bottom <= innerHeight, what: (e.textContent || e.className).trim().slice(0, 18), over: t ? (t.id || t.className).toString().slice(0, 16) : '' }; })"""
            FREE = """() => { const tops = [...document.querySelectorAll('.lab-f')].map(e => e.getBoundingClientRect().top); return Math.min(...tops); }"""
            free = pg.evaluate(FREE)
            s = pg.evaluate("""() => { const r = document.getElementById('nlpf'), b = r.getBoundingClientRect(), pads = getComputedStyle(document.querySelector('.lab-pad')).paddingLeft; return { h: Math.round(b.height), left: Math.round(b.left), right: Math.round(innerWidth - b.right), overflowX: document.scrollingElement.scrollWidth - innerWidth, pads }; }""")
            check("%s the stage is edge to edge (the page has %s side padding) and %d px tall, which fits the %d px free above the buttons" % (tag, s["pads"], s["h"], free), s["left"] == 0 and s["right"] == 0 and s["overflowX"] <= 0 and s["h"] <= free and s["h"] >= 440, s)
            pg.evaluate("scrollTo(0, 0)"); pg.wait_for_timeout(250)
            first = pg.evaluate(TOPMOST0, "#nlpf .nlpf-say button, #nlpf .nlpf-chip")
            sayb = pg.evaluate("() => Math.round((document.querySelector('#nlpf .nlpf-say button') || document.querySelector('#nlpf .nlpf-say')).getBoundingClientRect().bottom)")
            check("%s the very first screen, page not scrolled: the filter and the sentence with its button are on screen, above the floating buttons (its button ends at %d, the floating buttons start at %d) and nothing covers them" % (tag, sayb, free), not [x for x in first if not x["ok"]] and sayb <= free, [x for x in first if not x["ok"]][:2])
            pg.evaluate("document.querySelector(\"#nlpf .nlpf-card[data-id='u31']\").scrollIntoView({ inline: 'center', block: 'nearest' })"); pg.wait_for_timeout(250)
            pg.evaluate("scrollTo(0, 0)"); pg.wait_for_timeout(200)
            pg.evaluate("document.querySelector(\"#nlpf .nlpf-card[data-id='u31']\").click()")
            pg.wait_for_timeout(4200); settle(pg, 12000)
            pg.evaluate("document.querySelector('#nlpf .nlpf-say [data-open]').click()")
            pg.wait_for_selector("#nlpf .nlpf-panel:not([hidden]) .nlpf-sheet", timeout=4000)
            pg.wait_for_timeout(1500)
            TOPMOST = """sel => [...document.querySelectorAll(sel)].map(e => { const b = e.getBoundingClientRect(), t = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2); return { ok: !!t && (t === e || e.contains(t)) && b.top >= 0 && b.bottom <= innerHeight, top: Math.round(b.top), bottom: Math.round(b.bottom), what: (e.textContent || e.className).trim().slice(0, 18), over: t ? (t.id || t.className).toString().slice(0, 16) : '' }; })"""
            s = pg.evaluate("""() => { const r = document.getElementById('nlpf'), pn = r.querySelector('.nlpf-panel'), b = r.getBoundingClientRect(); return { top: Math.round(b.top), bottom: Math.round(b.bottom), scrolls: pn.scrollHeight > pn.clientHeight + 1, vis: Math.round(pn.querySelector('.nlpf-vis').getBoundingClientRect().height) }; }""")
            btns = pg.evaluate(TOPMOST, "#nlpf .nlpf-panel button, #nlpf .nlpf-panel a")
            badb = [x for x in btns if not x["ok"]]
            check("%s opening a building brings the stage to the top (top %d, bottom %d of %d free); every button of the card is on screen and under no floating button; no inner scroll; picture area %d px" % (tag, s["top"], s["bottom"], free, s["vis"]),
                  -3 <= s["top"] <= 6 and s["bottom"] <= free + 1 and not badb and not s["scrolls"] and s["vis"] >= 96, badb[:2] or s)
            pg.screenshot(path=str(OUT / ("%s-%d-floats-card.png" % (lang, w))))
            pg.evaluate("document.querySelector('#nlpf [data-back]').click()"); pg.wait_for_timeout(500)
            cards = pg.evaluate(TOPMOST, "#nlpf .nlpf-say button, #nlpf .nlpf-chip")
            tray = pg.evaluate("() => { const t = document.querySelector('#nlpf .nlpf-tray').getBoundingClientRect(); return Math.round(t.bottom); }")
            badc = [x for x in cards if not x["ok"]]
            check("%s back on the map: the filter, the sentence button and the tray (ends at %d) are above the floating buttons (%d)" % (tag, tray, free), not badc and tray <= free + 1, badc[:2])
            pg.screenshot(path=str(OUT / ("%s-%d-floats-map.png" % (lang, w))))
            check("%s no page errors" % tag, not errs, errs[:3])
            ctx.close()
    b.close()

ok = sum(1 for c in results["checks"] if c["ok"]); n = len(results["checks"])
(ROOT / "docs/rentals/build/opening").mkdir(parents=True, exist_ok=True)
(ROOT / "docs/rentals/build/opening/lab-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nRESULT %d/%d checks passed" % (ok, n))
sys.exit(0 if ok == n else 1)
