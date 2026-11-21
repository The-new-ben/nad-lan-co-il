# -*- coding: utf-8 -*-
"""The tour of the example portfolio (HAD-795, rm-tour.js): every stop is the app's REAL screen on the sample data.
Lab page docs/design-lab/rentals/tour.html (the page inc/rentals/page.php prints in sample mode: the bar, the app, rm-tour.js).
For he and en, 1280x800 and 390x664 (the phone also with the site's floating buttons): the bar's "next" is pressed stop after
stop; at each stop the expected real screen is on, the bar's buttons are free, and the screen's own top is not under the bar.
Headless Edge, NOT a real phone.  Usage: python scripts/rentals/lab_tour.py  (server at the repo root on 47921)"""
import sys, json, pathlib, datetime
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47921/docs/design-lab/rentals/tour.html"   # the live address: https://nad-lan.co.il/my-rentals/?sample=1
LIVE = "nad-lan.co.il" in BASE
SEP = "&" if "?" in BASE else "?"
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/rentals/build/opening/shots-lab"; OUT.mkdir(parents=True, exist_ok=True)
results = {"checks": [], "errors": []}


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:260]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:200] if info != "" else ""))


STATE = """() => { const N = window.NLRM, bar = document.getElementById('nlrm-tour'), bb = bar.getBoundingClientRect(), nt2 = document.querySelector('#nt2'), layer = document.querySelector('.nlrm-layer');
  const free = [...bar.querySelectorAll('button:not([disabled]), a')].filter(e => e.getBoundingClientRect().width > 0).every(e => { const b = e.getBoundingClientRect(), t = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2); return !!t && (t === e || e.contains(t)); });
  const app = nt2 && !nt2.hidden ? nt2.querySelector('.nt2-app') : null, top = app ? Math.round(app.getBoundingClientRect().top) : null;
  const lt = layer ? Math.round((layer.querySelector('.nlrm-panel, .nlrm-sheet, [role=dialog]') || layer).getBoundingClientRect().top) : null;
  return { at: window.NLRMTour.at(), hash: location.hash, barBottom: Math.round(bb.bottom), barTop: Math.round(bb.top), free, nt2: !!(nt2 && !nt2.hidden), nt2Top: top, layer: !!layer, layerTop: lt, layerText: layer ? layer.innerText.replace(/\\s+/g, ' ').slice(0, 160) : '',
    idx: !!document.querySelector('#nt2 [data-act="idx-save"], #nt2 .nt2-sw'), tax: !!document.querySelector('#nlrm-tax'), taxTop: (() => { const x = document.getElementById('nlrm-tax'); const c = x && (x.closest('.nlrm-card') || x); return c ? Math.round(c.getBoundingClientRect().top) : null; })(), mainTop: (() => { const m = document.querySelector('.nlrm-main'); return m ? Math.round(m.getBoundingClientRect().top) : null; })(), vh: innerHeight, maker: document.querySelectorAll('[data-act="lease-doc"], [data-act="sign-link"]').length, title: bar.querySelector('.nlrm-tour-t b').textContent, n: window.NLRMTour.stops().length,
    last: !!bar.querySelector('.nlrm-tour-row a.nlrm-tour-go'), lastHref: (bar.querySelector('.nlrm-tour-row a.nlrm-tour-go') || { getAttribute() { return ''; } }).getAttribute('href'),
    links: [...document.querySelectorAll('#nlrm-tour a[href], #nlrm-root a[href], #nt2 a[href], .nlrm-layer a[href]')].map(a => a.getAttribute('href')).filter(h => /wa\\.me|^tel:|^mailto:/i.test(h)), brand: (document.querySelector('.nlrm-brand b') || {}).textContent || '', overflowX: document.scrollingElement.scrollWidth - innerWidth }; }"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for lang in ("he", "en"):
        for w, h, fl in ((1280, 800, 0), (390, 664, 0), (390, 664, 1)):
            tag = "%s %dx%d%s" % (lang, w, h, " with the site's floating buttons" if fl else "")
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, has_touch=w < 900, locale="he-IL")
            ctx.clock.set_fixed_time(datetime.datetime(2026, 11, 10, 9, 0))
            popups = []; pg = ctx.new_page(); errs = []
            ctx.on("page", lambda g: popups.append(g.url))
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:160]))
            pg.goto("%s%s%su=21&floats=%d#/today/21" % (BASE, SEP, "lang=en&" if lang == "en" else ("" if LIVE else "lang=he&"), fl), wait_until="domcontentloaded" if LIVE else "networkidle")
            pg.wait_for_function("window.NLRMTour && window.NLRM && NLRM.store && NLRM.store.d", timeout=40000)
            pg.wait_for_timeout(900)
            s = pg.evaluate(STATE)
            check("%s the tour opens on the apartment's day screen (stop 1 of %d): the real screen is on, starts under the bar (bar ends %s, screen starts %s), the bar's buttons are free" % (tag, s["n"], s["barBottom"], s["nt2Top"]),
                  s["at"] == 0 and s["n"] >= 9 and s["nt2"] and s["hash"] == "#/today/21" and s["free"] and s["nt2Top"] is not None and s["nt2Top"] >= s["barBottom"] - 1 and s["overflowX"] <= 0, s)
            pg.screenshot(path=str((OUT.parent / "shots-live" if LIVE else OUT) / ("tour-%s-%d%s-1.png" % (lang, w, "-floats" if fl else ""))))
            names = pg.evaluate("window.NLRMTour.stops()")
            seen = [names[0]]; bad = []
            for i in range(1, len(names)):
                pg.click("#nlrm-tour [data-tour='next']", timeout=5000)
                pg.wait_for_timeout(2200)
                s = pg.evaluate(STATE)
                t = names[i]; ok = s["at"] == i and s["free"] and not s["links"] and s["overflowX"] <= 0
                kind = ""
                if "#/rent/" in s["hash"] and not s["idx"]:
                    kind = "rent"; ok = ok and s["nt2"] and s["nt2Top"] >= s["barBottom"] - 1
                elif "#/rent/" in s["hash"] and s["idx"]:
                    kind = "index"; ok = ok and s["nt2"]
                elif s["layer"]:
                    kind = "card"; ok = ok and len(s["layerText"]) > 20 and s["maker"] == 0
                elif s["tax"]:
                    kind = "tax"; ok = ok and s["taxTop"] is not None and s["barBottom"] - 2 <= s["taxTop"] <= max(s["barBottom"] + 60, s["vh"] * 0.5)
                elif s["hash"] in ("#/docs", "#/properties", "#/repairs", "#/money"):
                    kind = s["hash"]
                    if s["hash"] in ("#/docs", "#/properties") and i < len(names) - 1:
                        ok = ok and s["mainTop"] is not None and s["barBottom"] - 2 <= s["mainTop"] <= s["barBottom"] + 60
                else:
                    ok = False
                if s["layer"] and s["layerTop"] is not None and s["layerTop"] < s["barBottom"] - 1:
                    ok = False; kind += " UNDER-BAR(%s<%s)" % (s["layerTop"], s["barBottom"])
                seen.append("%s=%s" % (t[:14], kind))
                if not ok:
                    bad.append((i, t, kind, s["hash"], s["free"], s["at"], s["links"][:2], s["overflowX"], s["nt2Top"], s["barBottom"], s["maker"], s["taxTop"], s["mainTop"]))
                if i in (2, 3, 4) and w == 390 and not fl:
                    pg.screenshot(path=str((OUT.parent / "shots-live" if LIVE else OUT) / ("tour-%s-%d-%d.png" % (lang, w, i + 1))))
            check("%s 'next' walks all %d stops, each on the app's own screen, the bar free at every stop, no lease-maker button anywhere, no contact link" % (tag, len(names)), not bad and len(seen) == len(names), bad[:3] or seen)
            s = pg.evaluate(STATE)
            check("%s the last stop offers 'sign up and start' and there is no dead end (back works)" % tag, s["last"] and (("login" in s["lastHref"] or "my-rentals" in s["lastHref"]) if LIVE else s["lastHref"] == "#signup") and len(names) - 1 == s["at"], (s["last"], s["lastHref"]))
            pg.click("#nlrm-tour [data-tour='prev']"); pg.wait_for_timeout(700)
            check("%s the product's name stands in the app's top bar" % tag, pg.evaluate(STATE)["at"] == len(names) - 2 and ("נדל" in s["brand"] or "Rentals" in s["brand"]), s["brand"])
            check("%s nothing opened a tab; no page errors" % tag, not popups and not errs, (popups[:2], errs[:3]))
            ctx.close()
    b.close()
ok = sum(1 for c in results["checks"] if c["ok"]); n = len(results["checks"])
(ROOT / ("docs/rentals/build/opening/%s-tour-results.json" % ("live" if LIVE else "lab"))).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nRESULT %d/%d checks passed" % (ok, n))
sys.exit(0 if ok == n else 1)
