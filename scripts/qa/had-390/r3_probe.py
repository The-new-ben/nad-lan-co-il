# -*- coding: utf-8 -*-
"""HAD-390 R3 acceptance (Maya, 2.10): after the keyboard settles, the focused control is FULLY between the sticky header's foot
and the band's top (no clipping exemption), in both directions. Live vs --local (route-swap of the page HTML with the 3 hunks of
scripts/project-stage/consult_band_396.py; world.js is NEVER swapped, so HAD-391 is not in this preview).
Per screen and language:
  focus_seq: focus the example CTA ([data-example], else .nlw-exlink), then 12 Tab and 12 Shift+Tab (Maya's sequence);
  forward:   focus [data-view=out] without scrolling, one Tab;
  escape:    Enter on the example CTA opens the album, Escape closes it; the focus returns to a fully visible trigger;
  anchors:   every in-page link (a[href^="#"] to an element in main) clicked; the target's top lands in the usable rect;
  touch:     a CDP touch swipe of 300px on the page text; the scroll distance (no snap, no jump).
Each focus step is classified OK / V-FAIL (header or band or off-screen: the P0) / H-CLIP (clipped sideways by an ancestor or
the viewport: Maya's task 05, reported apart) / CHROME (focus inside the header, band or accessibility box).
  python r3_probe.py <tag> [--local] [--only he-844x390,...]"""
import io, os, sys, time, json, importlib.util
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAG = sys.argv[1]; LOCAL = "--local" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
OUT = os.path.join(REPO, "docs", "qa", "had-390", "r3"); os.makedirs(OUT, exist_ok=True)
HUNKS = []
if LOCAL:
    spec = importlib.util.spec_from_file_location("cb", os.path.join(REPO, "scripts", "project-stage", "consult_band_396.py"))
    cb = importlib.util.module_from_spec(spec); spec.loader.exec_module(cb); HUNKS = cb.HTML_HUNKS
URL = {"he": "https://nad-lan.co.il/projects/hamedina/", "en": "https://nad-lan.co.il/projects/hamedina-en/"}
NW = {"he": "צפון-מערבית", "en": "North-west"}
VIEWS = [(844, 390, True), (390, 844, True), (320, 740, True), (768, 1024, True), (1366, 640, False), (1440, 900, False)]
APPLIED = {}; WA = []; WJS = []


def route(r):
    u = r.request.url
    if "wa.me" in u or "api.whatsapp" in u:
        WA.append(u[:50]); return r.abort()
    if "analytics" in u or "googletagmanager" in u or "hotjar" in u or r.request.method != "GET":
        return r.abort()
    if "/world/world.js" in u:
        WJS.append("live")  # world.js always comes from the live site here (no HAD-391 swap)
    if LOCAL and r.request.resource_type == "document" and "nad-lan.co.il" in u:
        resp = r.fetch(); body = resp.text()
        for name, old, new in HUNKS:
            APPLIED[name] = max(APPLIED.get(name, 0), body.count(old)); body = body.replace(old, new)
        return r.fulfill(response=resp, body=body)
    return r.continue_()


RECT = r"""() => { const vw = innerWidth, vh = innerHeight;
  let hb = 0; for (const h of document.querySelectorAll('.nlhp-top, header')) { const s = getComputedStyle(h); const q = h.getBoundingClientRect(); if ((s.position === 'fixed' || s.position === 'sticky') && q.top <= 1 && q.width >= vw * 0.9 && q.height < vh * 0.4) hb = Math.max(hb, q.bottom); }
  const box = document.getElementById('nlcta'), bx = box && box.getBoundingClientRect(); const band = bx && bx.width >= vw * 0.9 && bx.bottom >= vh - 2;
  return { hb: hb, bt: band ? bx.top : vh, band: !!band, vw: vw, vh: vh }; }"""
FOC = r"""() => { const e = document.activeElement; if (!e || e === document.body || e === document.documentElement) return { cls: 'BODY' };
  const vw = innerWidth, vh = innerHeight; const r = e.getBoundingClientRect();
  let hb = 0; for (const h of document.querySelectorAll('.nlhp-top, header')) { const s = getComputedStyle(h); const q = h.getBoundingClientRect(); if ((s.position === 'fixed' || s.position === 'sticky') && q.top <= 1 && q.width >= vw * 0.9 && q.height < vh * 0.4) hb = Math.max(hb, q.bottom); }
  const box = document.getElementById('nlcta'), bx = box && box.getBoundingClientRect(); const band = bx && bx.width >= vw * 0.9 && bx.bottom >= vh - 2;
  let bt = band ? bx.top : vh;
  if (!band) { for (const q of ['#nlcta .nlcta-wa', '#nla11y-btn']) { const f = document.querySelector(q); if (!f) continue; const g = f.getBoundingClientRect(); if (g.width && g.left < r.right && g.right > r.left && g.top < r.bottom && g.bottom > r.top) bt = Math.min(bt, g.top); } }
  const name = e.tagName + '.' + String(e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className).split(' ').slice(0, 2).join('.');
  const text = (e.getAttribute('aria-label') || e.textContent || '').trim().slice(0, 28);
  const base = { el: name, text, top: Math.round(r.top * 10) / 10, bottom: Math.round(r.bottom * 10) / 10, left: Math.round(r.left), right: Math.round(r.right), hb: Math.round(hb), bt: Math.round(bt), y: Math.round(scrollY) };
  if (e.closest('.nlhp-top, header, #nlcta, #nla11y')) return Object.assign(base, { cls: 'CHROME' });
  if (r.width === 0 && r.height === 0) return Object.assign(base, { cls: 'ZERO' });
  if (r.top < hb - 0.5 || r.bottom > bt + 0.5) return Object.assign(base, { cls: 'V-FAIL' });
  let clip = null;
  for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) { const s = getComputedStyle(a); if (/(hidden|auto|scroll|clip)/.test(s.overflowX + s.overflowY + s.overflow)) { const q = a.getBoundingClientRect(); if (r.left < q.left - 0.5 || r.right > q.right + 0.5) { clip = 'H'; base.clipBy = a.tagName + '.' + String(a.className).split(' ')[0]; break; } if (r.top < q.top - 0.5 || r.bottom > q.bottom + 0.5) { clip = 'V'; base.clipBy = a.tagName + '.' + String(a.className).split(' ')[0]; break; } } }
  if (clip === 'V') return Object.assign(base, { cls: 'V-FAIL' });
  if (clip === 'H' || r.left < -0.5 || r.right > vw + 0.5) return Object.assign(base, { cls: 'H-CLIP' });
  return Object.assign(base, { cls: 'OK' }); }"""


def settle(pg):
    last, same = None, 0
    for _ in range(40):
        y = pg.evaluate("() => scrollY")
        same = same + 1 if y == last else 0
        if same >= 3:
            return
        last = y; pg.wait_for_timeout(100)


def pick(pg, mob, L):
    T = pg.touchscreen.tap if mob else pg.mouse.click
    pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo({ top: s.getBoundingClientRect().top + scrollY - 80, behavior: 'instant' }); }"); pg.wait_for_timeout(1500)
    rr = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }")
    T(int(rr[0] + rr[2] / 2), int(rr[1] + min(160, rr[3] / 3))); pg.wait_for_timeout(6500)
    if pg.evaluate("() => !!document.querySelector('#nlps .nlw--full')"):
        pg.keyboard.press("Escape"); pg.wait_for_timeout(1500)
    pg.evaluate("(w) => { const g = [...document.querySelectorAll('#nlps .nlw-apt')].find((x) => x.getAttribute('aria-label').includes(w)); if (g) g.scrollIntoView({ block: 'center', behavior: 'instant' }); }", NW[L]); pg.wait_for_timeout(1500)
    b = pg.evaluate("(w) => { const g = [...document.querySelectorAll('#nlps .nlw-apt')].find((x) => x.getAttribute('aria-label').includes(w)); if (!g) return null; const t = g.querySelector('text').getBoundingClientRect(); return [t.left + t.width / 2, t.top + t.height / 2 + 8]; }", NW[L])
    if b:
        T(int(b[0]), int(b[1])); pg.wait_for_timeout(2500)
    # a floor with no example apartment shows the link to it (.nlw-exlink); pressing it brings the example's floor and its button
    if not pg.evaluate("() => !!document.querySelector('[data-example]')"):
        e = pg.evaluate("() => { const x = document.querySelector('.nlw-exlink'); if (!x) return null; x.scrollIntoView({ block: 'center', behavior: 'instant' }); return true; }")
        if e:
            pg.wait_for_timeout(700)
            c = pg.evaluate("() => { const r = document.querySelector('.nlw-exlink').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }")
            T(int(c[0]), int(c[1])); pg.wait_for_timeout(3000)
            if pg.evaluate("() => !!document.querySelector('.nlex')"):
                pg.keyboard.press("Escape"); pg.wait_for_timeout(1200)


START = "() => document.querySelector('[data-example]') ? '[data-example]' : (document.querySelector('.nlw-exlink') ? '.nlw-exlink' : null)"

res = {}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    for L in ("he", "en"):
        for W, H, mob in VIEWS:
            key = f"{L}-{W}x{H}"
            if ONLY and key not in ONLY:
                continue
            kw = dict(viewport={"width": W, "height": H})
            if mob:
                kw.update(is_mobile=True, has_touch=True, device_scale_factor=2)
            ctx = br.new_context(**kw); ctx.route("**/*", route)
            pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
            pg.goto(URL[L] + "?r3=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(4000)
            R = {"padding": pg.evaluate("() => { const s = getComputedStyle(document.documentElement); return [s.scrollPaddingTop, s.scrollPaddingBottom]; }")}
            # touch: a 300px swipe on the answer paragraph's area, before anything else moves the page
            if mob:
                pg.evaluate("() => window.scrollTo({ top: 0, behavior: 'instant' })"); pg.wait_for_timeout(500)
                cdp = ctx.new_cdp_session(pg); x = W // 2; y1 = int(H * 0.75); y2 = y1 - 300
                y0 = pg.evaluate("() => scrollY")
                cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y1}]})
                for k in range(1, 11):
                    cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x, "y": y1 - 30 * k}]}); pg.wait_for_timeout(16)
                cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []}); pg.wait_for_timeout(1200); settle(pg)
                R["touch_delta"] = pg.evaluate("() => scrollY") - y0
            pick(pg, mob, L)
            st = pg.evaluate(START); R["start"] = st
            if st:
                # Maya's sequence
                pg.evaluate("(q) => document.querySelector(q).focus()", st); pg.wait_for_timeout(200); settle(pg)
                seq = [pg.evaluate(FOC)]
                for i in range(12):
                    pg.keyboard.press("Tab"); pg.wait_for_timeout(120); settle(pg); seq.append(pg.evaluate(FOC))
                for i in range(12):
                    pg.keyboard.press("Shift+Tab"); pg.wait_for_timeout(120); settle(pg); seq.append(pg.evaluate(FOC))
                R["seq"] = seq
                R["seq_counts"] = {c: sum(1 for s in seq if s.get("cls") == c) for c in ("OK", "V-FAIL", "H-CLIP", "CHROME", "ZERO", "BODY")}
                R["step24"] = seq[-1]
                pg.screenshot(path=os.path.join(OUT, f"{TAG}-{key}-step24.png"))
                # the forward Tab from [data-view=out], the example's top near the band (Maya's first finding)
                at = pg.evaluate("(q) => { const e = document.querySelector(q); const vh = innerHeight; const t = e.getBoundingClientRect().top + scrollY; window.scrollTo({ top: t - (vh - 85), behavior: 'instant' }); return Math.round(scrollY); }", st); pg.wait_for_timeout(500)
                ok = pg.evaluate("() => { const o = document.querySelector('[data-view=\"out\"]'); if (!o) return false; o.focus({ preventScroll: true }); return document.activeElement === o; }")
                if ok:
                    pg.keyboard.press("Tab"); pg.wait_for_timeout(120); settle(pg); R["forward"] = pg.evaluate(FOC)
                # Escape: Enter on the CTA opens the album; Escape returns the focus to a visible trigger
                pg.evaluate("(q) => document.querySelector(q).focus()", st); pg.wait_for_timeout(200); settle(pg)
                if st == "[data-example]":
                    pg.keyboard.press("Enter"); pg.wait_for_timeout(3000)
                    R["album_open"] = pg.evaluate("() => !!document.querySelector('.nlex')")
                    pg.keyboard.press("Escape"); pg.wait_for_timeout(900); settle(pg)
                    R["escape_back"] = pg.evaluate(FOC)
                    R["escape_back"]["is_trigger"] = pg.evaluate("() => !!(document.activeElement && document.activeElement.matches('[data-example]'))")
            # anchors
            links = pg.evaluate("() => [...document.querySelectorAll('main a[href^=\"#\"]')].map((a) => a.getAttribute('href')).filter((h) => h.length > 1 && document.getElementById(decodeURIComponent(h.slice(1))) && !h.startsWith('#wp--')).filter((h, i, A) => A.indexOf(h) === i).slice(0, 8)")
            an = []
            for h in links:
                pg.evaluate("() => window.scrollTo({ top: 0, behavior: 'instant' })"); pg.wait_for_timeout(300)
                ok = pg.evaluate("(h) => { const a = [...document.querySelectorAll('main a[href=\"' + h + '\"]')].find((x) => x.getClientRects().length); if (!a) return false; a.click(); return true; }", h)
                if not ok:
                    continue
                pg.wait_for_timeout(300); settle(pg)
                m = pg.evaluate("(h) => { const t = document.getElementById(decodeURIComponent(h.slice(1))); const r = t.getBoundingClientRect(); return { top: Math.round(r.top) }; }", h)
                rect = pg.evaluate(RECT)
                m.update({"href": h, "hb": round(rect["hb"]), "bt": round(rect["bt"]), "ok": m["top"] >= rect["hb"] - 1 and m["top"] < rect["bt"]})
                an.append(m)
            R["anchors"] = an
            R["errors"] = errs
            res[key] = R
            print(key, json.dumps({k: R.get(k) for k in ("padding", "touch_delta", "start", "seq_counts", "step24", "forward", "album_open", "escape_back")}, ensure_ascii=False), "| anchors ok", sum(1 for a in an if a["ok"]), "/", len(an), flush=True)
            ctx.close()
    # DUO / Rainbow keep no scroll padding
    for slug in ("rainbow-tel-aviv", "duo-tel-aviv"):
        ctx = br.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2); ctx.route("**/*", route)
        pg = ctx.new_page(); pg.goto(f"https://nad-lan.co.il/projects/{slug}/?r3=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3000)
        res[slug] = pg.evaluate("() => { const s = getComputedStyle(document.documentElement); return { scrollPaddingTop: s.scrollPaddingTop, scrollPaddingBottom: s.scrollPaddingBottom, band: getComputedStyle(document.body).getPropertyValue('--nlcta-band').trim() }; }")
        print(slug, res[slug], flush=True)
        ctx.close()
    br.close()
res["_applied"] = APPLIED; res["_whatsapp_requests"] = len(WA); res["_world_js_from"] = sorted(set(WJS))
json.dump(res, open(os.path.join(OUT, f"{TAG}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("applied:", APPLIED, "| whatsapp requests:", len(WA), "| world.js:", sorted(set(WJS)))
