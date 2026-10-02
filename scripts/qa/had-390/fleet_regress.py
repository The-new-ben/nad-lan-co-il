# -*- coding: utf-8 -*-
"""HAD-390 regression on DUO and Rainbow (Maya's item 01): ConsultBand must have a FALSE scope there. For each page, phone 390x844
and desktop 1440x900, live vs --local (route-swap of consult_band_396.py), the same steps:
  - scope: --nlcta-band empty, the body's padding-bottom;
  - a sweep of the whole page: the bar's (#nlcta) and the accessibility button's (#nla11y) rects and classes at every step must be
    IDENTICAL live and local;
  - the journey: a choice through ?unit=25-w (as the page's own deep link), the floor card, the map's beam (.nlps-cone path),
    the 360 tour (.nlat__go, a settled tap), the basket ([data-basket] / window.__nlBasket), the accessibility panel; errors.
wa.me is aborted and counted; no form is sent.
  python fleet_regress.py <tag>"""
import io, os, sys, time, json, importlib.util
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAG = sys.argv[1]
MODES = sys.argv[sys.argv.index("--modes") + 1].split(",") if "--modes" in sys.argv else ["live", "local"]
WIDTHS = [int(x) for x in sys.argv[sys.argv.index("--widths") + 1].split(",")] if "--widths" in sys.argv else [390, 1440]
OUT = os.path.join(REPO, "docs", "qa", "had-390", "fleet"); os.makedirs(OUT, exist_ok=True)
spec = importlib.util.spec_from_file_location("cb", os.path.join(REPO, "scripts", "project-stage", "consult_band_396.py"))
cb = importlib.util.module_from_spec(spec); spec.loader.exec_module(cb)
STATE = {"local": False}; APPLIED = {}; WA = []


def route(r):
    u = r.request.url
    if "wa.me" in u or "api.whatsapp" in u:
        WA.append(u[:50]); return r.abort()
    if "analytics" in u or "googletagmanager" in u or "hotjar" in u or r.request.method != "GET":
        return r.abort()
    if STATE["local"] and r.request.resource_type == "document" and "nad-lan.co.il" in u:
        resp = r.fetch(); body = resp.text()
        for name, old, new in cb.HTML_HUNKS:
            APPLIED[u.split("?")[0] + "#" + name] = body.count(old); body = body.replace(old, new)
        return r.fulfill(response=resp, body=body)
    return r.continue_()


FLOAT = """() => { const q = (s) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; };
  const c = document.getElementById('nlcta'); const a = document.getElementById('nla11y');
  return { wa: q('#nlcta .nlcta-wa'), cls: c ? c.className : null, acc: q('#nla11y-btn'), accT: a ? a.style.transform : null }; }"""


def run(pg, mob, H):
    R = {}
    R["scope"] = pg.evaluate("() => ({ band: getComputedStyle(document.body).getPropertyValue('--nlcta-band').trim(), padB: getComputedStyle(document.body).paddingBottom })")
    R["selection"] = pg.evaluate("() => { try { const s = window.__nlpsStage && window.__nlpsStage.getSelection && window.__nlpsStage.getSelection(); return s ? { floor: s.floor, unit: s.unit || null } : null; } catch (e) { return 'err'; } }")
    R["floor_card"] = pg.evaluate("() => !!document.querySelector('#nlps-pick *')")
    R["cone"] = pg.evaluate("() => { const p = document.querySelector('.nlps-cone path'); if (!p) return null; const r = p.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; }")
    total = pg.evaluate("() => document.documentElement.scrollHeight - innerHeight")
    seq = []; y = 0; step = max(120, int(H * 0.3))
    while y <= total:
        pg.evaluate("(y) => window.scrollTo({ top: y, behavior: 'instant' })", y); pg.wait_for_timeout(260)
        seq.append(pg.evaluate(FLOAT)); y += step
    R["float_seq"] = seq
    # the tour
    ok = pg.evaluate("() => { const b = document.querySelector('#nlps-tour .nlat__go'); if (!b) return false; b.scrollIntoView({ block: 'center', behavior: 'instant' }); return true; }")
    if ok:
        pg.wait_for_timeout(900)
        b = pg.evaluate("() => { const r = document.querySelector('#nlps-tour .nlat__go').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }")
        (pg.touchscreen.tap if mob else pg.mouse.click)(int(b[0]), int(b[1])); pg.wait_for_timeout(5000)
        R["tour_open"] = pg.evaluate("() => document.documentElement.classList.contains('nlat-open')")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(1200)
        R["tour_closed"] = not pg.evaluate("() => document.documentElement.classList.contains('nlat-open')")
    # the basket
    R["basket"] = pg.evaluate("() => { if (window.__nlBasket && typeof window.__nlBasket.open === 'function') { window.__nlBasket.open(); const r = document.querySelector('.nlbk'); return r ? !r.hidden : 'no root'; } return 'no api'; }")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(700)
    # the accessibility panel
    pg.evaluate("() => window.scrollTo({ top: 0, behavior: 'instant' })"); pg.wait_for_timeout(500)
    ac = pg.evaluate("() => { const r = document.getElementById('nla11y-btn').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }")
    (pg.touchscreen.tap if mob else pg.mouse.click)(int(ac[0]), int(ac[1])); pg.wait_for_timeout(700)
    R["a11y_panel"] = pg.evaluate("() => { const p = document.getElementById('nla11y-panel'); return !!(p && !p.hidden); }")
    (pg.touchscreen.tap if mob else pg.mouse.click)(int(ac[0]), int(ac[1])); pg.wait_for_timeout(500)
    return R


res = {}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    for slug in ("rainbow-tel-aviv", "duo-tel-aviv"):
        for W, H, mob in [v for v in ((390, 844, True), (1440, 900, False)) if v[0] in WIDTHS]:
            pair = {}
            for mi, mode in enumerate(MODES):
                STATE["local"] = mode == "local"
                mode = mode + str(mi)
                kw = dict(viewport={"width": W, "height": H})
                if mob:
                    kw.update(is_mobile=True, has_touch=True, device_scale_factor=2)
                ctx = br.new_context(**kw); ctx.route("**/*", route)
                pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
                pg.goto(f"https://nad-lan.co.il/projects/{slug}/?unit=25-w&fr=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(8000)
                R = run(pg, mob, H); R["errors"] = errs
                pg.screenshot(path=os.path.join(OUT, f"{TAG}-{slug}-{W}-{mode}.png"))
                pair[mode] = R
                ctx.close()
            A, B = pair[MODES[0] + "0"], pair[MODES[1] + "1"]
            same = A["float_seq"] == B["float_seq"]
            diffs = [i for i, (a, b) in enumerate(zip(A["float_seq"], B["float_seq"])) if a != b]
            journey = {k: (A.get(k), B.get(k)) for k in ("scope", "selection", "floor_card", "cone", "tour_open", "tour_closed", "basket", "a11y_panel", "errors")}
            res[f"{slug}-{W}"] = {"modes": MODES, "float_identical": same, "steps": len(A["float_seq"]), "diff_steps": diffs[:10], "diff_detail": [[i, A["float_seq"][i], B["float_seq"][i]] for i in diffs[:6]], "journey": journey}
            print(f"{slug}-{W}", json.dumps(res[f"{slug}-{W}"], ensure_ascii=False), flush=True)
    br.close()
res["_applied"] = APPLIED; res["_whatsapp_requests"] = len(WA)
json.dump(res, open(os.path.join(OUT, f"{TAG}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("applied:", APPLIED, "| whatsapp requests:", len(WA))
