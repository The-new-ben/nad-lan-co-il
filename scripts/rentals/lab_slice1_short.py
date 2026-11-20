# -*- coding: utf-8 -*-
"""Rentals slice 1, release 1.72.726 (HAD-795): a short screen scrolls like a page, and the layer keeps a free strip for the
site's own floating buttons (stand-ins in the lab at the positions and layer order measured on the live site).
For every size, with and without the floating buttons, on the day screen and on the tenancy screen:
  - every button and link of the screen can be brought into view and RECEIVES the press (nothing covers it);
  - nothing of the screen lies under a floating button that stands over its column;
  - on the tenancy screen the index line opens its sheet and the confirm button receives the press.
Sizes: 390x450, 390x550, 390x600, 390x660, 844x390 (a phone held sideways), 625x451 (the narrowest this machine's Chrome
gives), 1280x451. Headless Edge, NOT a real phone.
Usage: python scripts/rentals/lab_slice1_short.py   (server at the repo root: python -m http.server 47921)"""
import sys, json, pathlib, datetime
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:47921/docs/design-lab/rentals/app.html"
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/rentals/build/slice1/shots-726"
OUT.mkdir(parents=True, exist_ok=True)
SIZES = [(390, 450), (390, 550), (390, 600), (390, 660), (844, 390), (625, 451), (1280, 451)]
results = {"checks": [], "errors": []}


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:260]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:190] if info != "" else ""))


REACH = """async () => {
  const body = document.querySelector('#nt2-body'), bad = [], seen = [];
  const els = [...body.querySelectorAll('button, a[href]')].filter(e => { const s = getComputedStyle(e); return s.display !== 'none' && s.visibility !== 'hidden' && !e.disabled && e.getBoundingClientRect().width > 0 && !e.classList.contains('nt2-tb-open'); });
  for (const e of els) {
    e.scrollIntoView({ block: 'center', inline: 'nearest' });
    await new Promise(r => requestAnimationFrame(() => r()));
    const r = e.getBoundingClientRect(), pts = [[r.left + r.width / 2, r.top + r.height / 2], [r.left + 6, r.top + 6], [r.right - 6, r.bottom - 6]];
    const ok = pts.every(p => { const t = document.elementFromPoint(p[0], p[1]); return !!t && (t === e || e.contains(t) || t.contains(e) && t.closest('#nt2-body')); });
    seen.push(1);
    if (!ok) { const t = document.elementFromPoint(pts[0][0], pts[0][1]); bad.push((e.getAttribute('data-act') || e.getAttribute('data-nav') || e.className || e.tagName).toString().slice(0, 24) + ' <- ' + (t ? (t.id || t.className || t.tagName).toString().slice(0, 20) : 'nothing')); }
  }
  body.scrollTop = 0;
  const host = document.querySelector('#nt2'), col = body.getBoundingClientRect();
  const under = [...document.querySelectorAll('.lab-f')].filter(f => { const r = f.getBoundingClientRect(); return r.right > col.left + 1 && r.left < col.right - 1 && r.bottom > col.top + 1 && r.top < col.bottom - 1; }).map(f => f.id);
  return { n: seen.length, bad, under, keep: host.getAttribute('data-keep'), short: host.classList.contains('is-short'), scrolls: body.scrollHeight > body.clientHeight + 1, col: [Math.round(col.top), Math.round(col.bottom)], H: innerHeight };
}"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for w, h in SIZES:
        for fl in (0, 1):
            tag = "%dx%d %s" % (w, h, "with the site buttons" if fl else "no site buttons")
            for route, unit, scene in (("today", 21, "urgent"), ("today", 31, "urgent"), ("rent", 11, "quiet")):
                ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, has_touch=w < 900, locale="he-IL")
                ctx.clock.set_fixed_time(datetime.datetime(2026, 11, 10, 9, 0))
                pg = ctx.new_page(); errs = []
                pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
                pg.goto("%s?slice=1&scene=%s&lang=he&floats=%d&bar=%d#/%s/%s" % (BASE, scene, fl, fl, route, unit), wait_until="networkidle")
                pg.wait_for_selector("#nt2:not([hidden]) .nt2-app > *", timeout=10000)
                pg.wait_for_timeout(700)
                r = pg.evaluate(REACH)
                check("%s, %s %s: all %d buttons can be reached and receive the press" % (tag, route, unit, r["n"]), r["n"] >= 6 and not r["bad"], r["bad"] or "keep %s short %s" % (r["keep"], r["short"]))
                if fl:
                    check("%s, %s %s: nothing of the screen lies under a floating button (strip top,bottom = %s)" % (tag, route, unit, r["keep"]), not r["under"], r["under"])
                if route == "rent":
                    pg.evaluate("document.querySelector('.nt2-sum-idx [data-act=index]').scrollIntoView({ block: 'center' })")
                    pg.wait_for_timeout(150)
                    pg.click(".nt2-sum-idx [data-act='index']", timeout=5000)
                    pg.wait_for_selector("#nt2 [data-act='idx-save']", timeout=6000)
                    pg.wait_for_timeout(350)
                    s = pg.evaluate("""() => { const sw = document.querySelector('.nt2-sw'), sh = sw.querySelector('.nt2-sheet'), b = sw.querySelector('[data-act=idx-save]'); b.scrollIntoView({ block: 'center' }); const r = b.getBoundingClientRect(), t = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2), q = sh.getBoundingClientRect();
                      const under = [...document.querySelectorAll('.lab-f')].filter(f => { const x = f.getBoundingClientRect(); return x.right > q.left + 1 && x.left < q.right - 1 && x.bottom > q.top + 1 && x.top < q.bottom - 1; }).map(f => f.id);
                      return { gets: !!t && (t === b || b.contains(t)), inView: r.top >= 0 && r.bottom <= innerHeight, under }; }""")
                    check("%s: the index line opens its sheet, the confirm button is in view and receives the press, the sheet is under no floating button" % tag, s["gets"] and s["inView"] and not s["under"], s)
                    pg.click("#nt2 [data-act='idx-save']", timeout=5000)
                    pg.wait_for_function("NLRM.store.d.events.some(e => e.type === 'index_confirmed')", timeout=6000)
                    check("%s: the confirmation is saved from that screen" % tag, True)
                if (w, h) in ((390, 450), (390, 660), (844, 390), (625, 451)) and route != "today" or ((w, h) == (390, 660) and unit == 21):
                    pg.screenshot(path=str(OUT / ("%dx%d-%s-%s%s.png" % (w, h, route, unit, "-floats" if fl else ""))))
                results["errors"] += errs; ctx.close()
    # a tall screen with no site buttons is exactly as before: no strip, no scrolling mode
    ctx = b.new_context(viewport={"width": 390, "height": 844}); ctx.clock.set_fixed_time(datetime.datetime(2026, 11, 10, 9, 0)); pg = ctx.new_page()
    pg.goto(BASE + "?slice=1&scene=urgent&lang=he#/today/21", wait_until="networkidle"); pg.wait_for_timeout(700)
    r = pg.evaluate("(() => { const h = document.querySelector('#nt2'); return [h.getAttribute('data-keep'), h.classList.contains('is-short'), h.classList.contains('is-h700'), getComputedStyle(document.querySelector('#nt2-body')).overflowY]; })()")
    check("390x844 with no site buttons: no strip, not the scrolling mode (as before)", r == ["0,0", False, False, "hidden"], r)
    ctx.close(); b.close()

check("no page errors in any run", not results["errors"], results["errors"][:3])
ok = sum(1 for c in results["checks"] if c["ok"]); n = len(results["checks"])
(ROOT / "docs/rentals/build/slice1/lab-726-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nRESULT %d/%d checks passed" % (ok, n))
sys.exit(0 if ok == n else 1)
