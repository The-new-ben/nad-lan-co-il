# -*- coding: utf-8 -*-
"""HAD-390, Maya's native-Tab finding (2.10): from [data-view=out] a native Tab moves the focus to [data-example] at y759 while the
button sits half under the band. Reproduces her state (the apartment chosen, the example button's top at y759 on 390x844, y815 on
1440x900), then: one native Tab from [data-view=out]; then 12 Tab and 12 Shift+Tab steps from there. For every step the focused
element must lie fully inside the usable rect (below the fixed header, above the band/bar). Live vs --local (route-swap).
  python tab_probe.py <tag> [--local]"""
import io, os, sys, time, json, importlib.util
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAG = sys.argv[1]; LOCAL = "--local" in sys.argv
OUT = os.path.join(REPO, "docs", "qa", "had-390", "tab"); os.makedirs(OUT, exist_ok=True)
HUNKS = []
if LOCAL:
    spec = importlib.util.spec_from_file_location("cb", os.path.join(REPO, "scripts", "project-stage", "consult_band_396.py"))
    cb = importlib.util.module_from_spec(spec); spec.loader.exec_module(cb); HUNKS = cb.HTML_HUNKS
URL = {"he": "https://nad-lan.co.il/projects/hamedina/", "en": "https://nad-lan.co.il/projects/hamedina-en/"}
NW = {"he": "צפון-מערבית", "en": "North-west"}
APPLIED = {}; WA = []


def route(r):
    u = r.request.url
    if "wa.me" in u or "api.whatsapp" in u:
        WA.append(u[:50]); return r.abort()
    if "analytics" in u or "googletagmanager" in u or "hotjar" in u or r.request.method != "GET":
        return r.abort()
    if LOCAL and r.request.resource_type == "document" and "nad-lan.co.il" in u:
        resp = r.fetch(); body = resp.text()
        for name, old, new in HUNKS:
            APPLIED[name] = max(APPLIED.get(name, 0), body.count(old)); body = body.replace(old, new)
        return r.fulfill(response=resp, body=body)
    return r.continue_()


FOC = r"""() => { const e = document.activeElement; if (!e || e === document.body) return { el: 'body' };
  const vw = innerWidth, vh = innerHeight; const r = e.getBoundingClientRect();
  const box = document.getElementById('nlcta'), bx = box && box.getBoundingClientRect(); const band = bx && bx.width >= vw * 0.9 && bx.bottom >= vh - 2;
  let bot = band ? bx.top : vh;
  if (!band) { for (const q of ['#nlcta .nlcta-wa', '#nla11y-btn']) { const f = document.querySelector(q); if (!f) continue; const g = f.getBoundingClientRect(); if (g.width && g.left < r.right && g.right > r.left && g.top < r.bottom && g.bottom > r.top) bot = Math.min(bot, g.top); } }
  let top = 0; for (const h of document.querySelectorAll('header, .nlhp-top')) { const s = getComputedStyle(h); const q = h.getBoundingClientRect(); if ((s.position === 'fixed' || s.position === 'sticky') && q.top <= 1 && q.width >= vw * 0.9 && q.height < vh * 0.3) top = Math.max(top, q.bottom); }
  const inChrome = !!e.closest('#nlcta, #nla11y, header, .nlhp-top');
  return { el: e.tagName + '.' + String(e.className).split(' ').slice(0, 2).join('.'), text: (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 26),
    top: Math.round(r.top), bottom: Math.round(r.bottom), usableTop: Math.round(top), usableBottom: Math.round(bot), chrome: inChrome,
    ok: inChrome || (r.height === 0) || (r.top >= top - 1 && r.bottom <= bot + 1), scrollY: Math.round(scrollY) }; }"""

def settle(pg):
    # the page scrolls smoothly: wait until scrollY holds still for 3 samples (at most 3 s)
    last, same = None, 0
    for _ in range(30):
        y = pg.evaluate("() => scrollY")
        same = same + 1 if y == last else 0
        if same >= 3:
            return
        last = y; pg.wait_for_timeout(100)


res = {}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    for L, W, H, mob, at in (("he", 390, 844, True, 759), ("en", 390, 844, True, 759), ("he", 1440, 900, False, 815), ("en", 1440, 900, False, 815), ("he", 320, 740, True, 660), ("he", 768, 1024, True, 930)):
        key = f"{L}-{W}x{H}"
        kw = dict(viewport={"width": W, "height": H})
        if mob:
            kw.update(is_mobile=True, has_touch=True, device_scale_factor=2)
        ctx = br.new_context(**kw); ctx.route("**/*", route)
        pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        T = pg.touchscreen.tap if mob else pg.mouse.click
        pg.goto(URL[L] + "?tp=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(4000)
        pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo({ top: s.getBoundingClientRect().top + scrollY - 80, behavior: 'instant' }); }"); pg.wait_for_timeout(1500)
        rr = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }")
        T(int(rr[0] + rr[2] / 2), int(rr[1] + min(160, rr[3] / 3))); pg.wait_for_timeout(6500)
        if pg.evaluate("() => !!document.querySelector('#nlps .nlw--full')"):
            pg.keyboard.press("Escape"); pg.wait_for_timeout(1500)
        pg.evaluate("(w) => { const g = [...document.querySelectorAll('#nlps .nlw-apt')].find((x) => x.getAttribute('aria-label').includes(w)); if (g) g.scrollIntoView({ block: 'center', behavior: 'instant' }); }", NW[L]); pg.wait_for_timeout(1500)
        b = pg.evaluate("(w) => { const g = [...document.querySelectorAll('#nlps .nlw-apt')].find((x) => x.getAttribute('aria-label').includes(w)); if (!g) return null; const t = g.querySelector('text').getBoundingClientRect(); return [t.left + t.width / 2, t.top + t.height / 2 + 8]; }", NW[L])
        if b:
            T(int(b[0]), int(b[1])); pg.wait_for_timeout(2500)
        R = {}
        print("..", key, flush=True)
        if not pg.evaluate("() => !!document.querySelector('[data-example], .nlw-exlink')"):
            R["skipped"] = "no [data-example]: the apartment was not chosen (" + str(pg.evaluate("() => !!document.querySelector('#nlps .nlw-deals')")) + ")"; R["errors"] = errs
            pg.screenshot(path=os.path.join(OUT, f"{TAG}-{key}-nopick.png")); res[key] = R; print(key, R["skipped"], flush=True); ctx.close(); continue
        # Maya's state: the example button's top at y `at`
        y0 = pg.evaluate("(at) => { const e = document.querySelector('[data-example]') || document.querySelector('.nlw-exlink'); const t = e.getBoundingClientRect().top + scrollY; window.scrollTo({ top: t - at, behavior: 'instant' }); return Math.round(scrollY); }", at); pg.wait_for_timeout(700)
        R["state"] = pg.evaluate("() => { const e = document.querySelector('[data-example]') || document.querySelector('.nlw-exlink'); const r = e.getBoundingClientRect(); return { exTop: Math.round(r.top), exBottom: Math.round(r.bottom), scrollY: Math.round(scrollY) }; }")
        R["from_found"] = pg.evaluate("() => { const o = document.querySelector('[data-view=\"out\"]'); if (!o) return false; o.focus({ preventScroll: true }); return document.activeElement === o; }")
        pg.wait_for_timeout(200)
        pg.keyboard.press("Tab"); pg.wait_for_timeout(150); settle(pg)
        R["tab_to_example"] = pg.evaluate(FOC)
        R["tab_to_example"]["is_example"] = pg.evaluate("() => !!(document.activeElement && document.activeElement.matches('[data-example], .nlw-exlink'))")
        pg.screenshot(path=os.path.join(OUT, f"{TAG}-{key}-tab.png"))
        steps = []
        for i in range(12):
            pg.keyboard.press("Tab"); pg.wait_for_timeout(150); settle(pg); steps.append(pg.evaluate(FOC))
        for i in range(12):
            pg.keyboard.press("Shift+Tab"); pg.wait_for_timeout(150); settle(pg); steps.append(pg.evaluate(FOC))
        R["steps_bad"] = [s for s in steps if not s.get("ok")]
        R["steps_n"] = len(steps); R["errors"] = errs
        res[key] = R
        print(key, json.dumps({"state": R["state"], "tab_to_example": R["tab_to_example"], "bad": len(R["steps_bad"]), "first_bad": R["steps_bad"][:2]}, ensure_ascii=False), flush=True)
        ctx.close()
    br.close()
res["_applied"] = APPLIED; res["_whatsapp_requests"] = len(WA)
json.dump(res, open(os.path.join(OUT, f"{TAG}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("applied:", APPLIED, "| whatsapp requests:", len(WA))
