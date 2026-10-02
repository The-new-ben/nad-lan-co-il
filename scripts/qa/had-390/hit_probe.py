# -*- coding: utf-8 -*-
"""HAD-390 acceptance (Maya's execution queue item 01): real hit targets, not only overlap.
For every scroll step from the stage to the page end, every CTA and decision text on screen is tested at 5 points (centre and the
middle of its 4 edges, 3px inside): elementFromPoint must be the target or inside it. The usable rect is the viewport minus the
fixed header at the top and minus the ConsultBand at the foot (when present). Points outside it are counted as CLIPPED (geometric
overlap with page chrome, reported separately), never as hits. Four states: before the apartment is chosen, after it is chosen,
after the album (a modal) is opened and closed, and with the accessibility panel open. Plus Maya's two exact checks:
HE 390x844 scrollY 1300 point (333.6, 782.34) and HE 1440x900 scrollY 224 the centre of .nlw-btn--ex.
No contact is ever sent: wa.me requests are aborted and counted.
  python hit_probe.py <tag> [--local] [--only he-390x844,en-1440x900]
--local: route-swap of the page HTML with scripts/project-stage/consult_band_396.py (nothing is deployed)."""
import io, os, sys, time, json, importlib.util
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAG = sys.argv[1]; LOCAL = "--local" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
OUT = os.path.join(REPO, "docs", "qa", "had-390", "hit"); os.makedirs(OUT, exist_ok=True)
HUNKS = []
if LOCAL:
    spec = importlib.util.spec_from_file_location("cb", os.path.join(REPO, "scripts", "project-stage", "consult_band_396.py"))
    cb = importlib.util.module_from_spec(spec); spec.loader.exec_module(cb); HUNKS = cb.HTML_HUNKS
URL = {"he": "https://nad-lan.co.il/projects/hamedina/", "en": "https://nad-lan.co.il/projects/hamedina-en/"}
NW = {"he": "צפון-מערבית", "en": "North-west"}
APPLIED = {}; WA = []
VIEWS = [(320, 740, True), (360, 800, True), (390, 844, True), (412, 915, True), (768, 1024, True), (1440, 900, False),
         (844, 390, True), (1366, 640, False)]


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


HIT = r"""() => {
  const vw = innerWidth, vh = innerHeight;
  const box = document.getElementById('nlcta'), bx = box && box.getBoundingClientRect();
  const band = bx && bx.width >= vw * 0.9 && bx.bottom >= vh - 2 ? bx : null;
  let top = 0;
  for (const e of document.querySelectorAll('header, .nlhp-top')) { const s = getComputedStyle(e); const r = e.getBoundingClientRect(); if ((s.position === 'fixed' || s.position === 'sticky') && r.top <= 1 && r.width >= vw * 0.9 && r.height < vh * 0.3) top = Math.max(top, r.bottom); }
  const U = { l: 0, r: vw, t: top, b: band ? band.top : vh };
  const T = {
    example: '[data-example], .nlw-btn--ex', basket: '[data-basket]', exlink: '.nlw-exlink', hero: '.nlps-hero__cta a',
    tabs: '#nlps .nlw-tab', faces: '#nlps .nlw-face, #nlps .nlw-tower, #nlps .nlw-panel button', apt: '#nlps .nlw-apt',
    deals: '#nlps .nlw-deals', facts: '#nlws-facts td, #nlws-prices td, #nlps .nlw-facts',
  };
  const out = { tested: 0, clipped: 0, fails: [], usable: U, band: !!band };
  for (const [k, q] of Object.entries(T)) {
    for (const e of document.querySelectorAll(q)) {
      if (e.closest('#nlcta, #nla11y, .nlex, .nlbk, .nlat-viewer')) continue;
      const r = e.getBoundingClientRect(); if (r.width < 6 || r.height < 6) continue;
      if (r.bottom <= U.t || r.top >= U.b || r.right <= 0 || r.left >= vw) continue;
      const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || +cs.opacity === 0) continue;
      // an apartment of the key plan is a diamond-like SVG shape: its bounding box's edges fall on the neighbours, so it is tested at its label's centre
      const lab = k === 'apt' ? e.querySelector('text') : null, lr = lab && lab.getBoundingClientRect();
      const P = lr ? [[lr.left + lr.width / 2, lr.top + lr.height / 2, 'c']] : [[r.left + r.width / 2, r.top + r.height / 2, 'c'], [r.left + 3, r.top + r.height / 2, 'l'], [r.right - 3, r.top + r.height / 2, 'r'], [r.left + r.width / 2, r.top + 3, 't'], [r.left + r.width / 2, r.bottom - 3, 'b']];
      let clip = false;
      for (const [x, y, n] of P) {
        if (x < U.l || x > U.r || y < U.t + 1 || y > U.b - 1) { clip = true; continue; } // 1px of rounding at the chrome's edge counts as clipped
        out.tested++;
        const h = document.elementFromPoint(x, y);
        if (!h || !(h === e || e.contains(h))) {
          const who = !h ? 'none' : h.closest('#nlcta') ? 'WHATSAPP' : h.closest('#nla11y') ? 'A11Y' : (h.tagName + '.' + String(h.className && h.className.baseVal !== undefined ? h.className.baseVal : h.className).split(' ')[0]);
          if (out.fails.length < 40) out.fails.push({ k, n, x: Math.round(x * 10) / 10, y: Math.round(y * 10) / 10, who, el: (e.textContent || '').trim().slice(0, 24) });
        }
      }
      if (clip) out.clipped++;
    }
  }
  out.y = Math.round(scrollY);
  return out;
}"""
EXACT = r"""(pt) => { const h = document.elementFromPoint(pt[0], pt[1]); const ex = document.querySelector('.nlw-btn--ex'); const r = ex && ex.getBoundingClientRect();
  const box = document.getElementById('nlcta').getBoundingClientRect(); const band = box.width >= innerWidth * 0.9 && box.bottom >= innerHeight - 2;
  return { hit: !h ? null : h.closest('#nlcta') ? 'WHATSAPP-BAND/BAR' : h.closest('#nla11y') ? 'A11Y' : (ex && (h === ex || ex.contains(h)) ? 'nlw-btn--ex' : h.tagName + '.' + String(h.className).slice(0, 30)),
    exRect: r ? [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)] : null, bandTop: band ? Math.round(box.top) : null, scrollY: Math.round(scrollY) }; }"""


def sweep(pg, H, frm, to, step, label, R):
    agg = {"steps": 0, "tested": 0, "clipped": 0, "fails": []}
    y = frm
    while y <= to:
        pg.evaluate("(y) => window.scrollTo({ top: y, behavior: 'instant' })", y); pg.wait_for_timeout(280)
        m = pg.evaluate(HIT)
        agg["steps"] += 1; agg["tested"] += m["tested"]; agg["clipped"] += m["clipped"]
        for f in m["fails"]:
            if len(agg["fails"]) < 25:
                f["scrollY"] = m["y"]; agg["fails"].append(f)
        agg["band"] = m["band"]
        y += step
    agg["fail_count"] = len(agg["fails"])
    R[label] = agg


def tap(pg, mob, x, y):
    (pg.touchscreen.tap if mob else pg.mouse.click)(int(x), int(y))


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
            pg.goto(URL[L] + "?hp=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(4000)
            R = {}
            total = pg.evaluate("() => document.documentElement.scrollHeight - innerHeight")
            st = pg.evaluate("() => Math.max(0, document.getElementById('nlps').getBoundingClientRect().top + scrollY - 200)")
            step = max(110, int(H * 0.3))
            sweep(pg, H, st, total, step, "before", R)
            # choose the apartment
            pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo({ top: s.getBoundingClientRect().top + scrollY - 80, behavior: 'instant' }); }"); pg.wait_for_timeout(1500)
            rr = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }")
            tap(pg, mob, rr[0] + rr[2] / 2, rr[1] + min(160, rr[3] / 3)); pg.wait_for_timeout(6500)
            if pg.evaluate("() => !!document.querySelector('#nlps .nlw--full')"):
                pg.keyboard.press("Escape"); pg.wait_for_timeout(1500)
            pg.evaluate("(w) => { const g = [...document.querySelectorAll('#nlps .nlw-apt')].find((x) => x.getAttribute('aria-label').includes(w)); if (g) g.scrollIntoView({ block: 'center', behavior: 'instant' }); }", NW[L]); pg.wait_for_timeout(1500)
            b = pg.evaluate("(w) => { const g = [...document.querySelectorAll('#nlps .nlw-apt')].find((x) => x.getAttribute('aria-label').includes(w)); if (!g) return null; const t = g.querySelector('text').getBoundingClientRect(); return [t.left + t.width / 2, t.top + t.height / 2 + 8]; }", NW[L])
            if b:
                tap(pg, mob, b[0], b[1]); pg.wait_for_timeout(2500)
            R["picked"] = pg.evaluate("() => !!document.querySelector('#nlps .nlw-deals')")
            total = pg.evaluate("() => document.documentElement.scrollHeight - innerHeight")
            sweep(pg, H, st, total, step, "after", R)
            # Maya's exact checks
            if key == "he-390x844":
                pg.evaluate("() => window.scrollTo({ top: 1300, behavior: 'instant' })"); pg.wait_for_timeout(600)
                R["exact_333.6_782.34"] = pg.evaluate(EXACT, [333.6, 782.34])
                pg.screenshot(path=os.path.join(OUT, f"{TAG}-{key}-exact.png"))
            if key == "he-1440x900":
                pg.evaluate("() => window.scrollTo({ top: 224, behavior: 'instant' })"); pg.wait_for_timeout(600)
                c = pg.evaluate("() => { const r = document.querySelector('.nlw-btn--ex').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }")
                R["exact_ex_centre"] = pg.evaluate(EXACT, c); R["exact_ex_centre"]["point"] = [round(c[0], 1), round(c[1], 1)]
                R["exact_y815"] = pg.evaluate(EXACT, [c[0], 815])
                pg.screenshot(path=os.path.join(OUT, f"{TAG}-{key}-exact.png"))
            # the album opened and closed
            b = pg.evaluate("() => { const e = document.querySelector('#nlps [data-example]'); if (!e) return null; e.scrollIntoView({ block: 'center', behavior: 'instant' }); return true; }")
            if b:
                pg.wait_for_timeout(900)
                b = pg.evaluate("() => { const r = document.querySelector('#nlps [data-example]').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }")
                tap(pg, mob, b[0], b[1]); pg.wait_for_timeout(3000)
                R["album_opened"] = pg.evaluate("() => !!document.querySelector('.nlex')")
                pg.keyboard.press("Escape"); pg.wait_for_timeout(1200)
                R["album_closed"] = not pg.evaluate("() => !!document.querySelector('.nlex')")
                cy = pg.evaluate("() => { const d = document.querySelector('#nlps .nlw-deals'); return d ? Math.round(d.getBoundingClientRect().top + scrollY) : 0; }")
                sweep(pg, H, max(0, cy - H), cy + H, max(90, int(H * 0.15)), "after_modal", R)
            # the accessibility panel open, at the card
            pg.evaluate("() => { const d = document.querySelector('#nlps .nlw-deals'); if (d) d.scrollIntoView({ block: 'center', behavior: 'instant' }); }"); pg.wait_for_timeout(700)
            ac = pg.evaluate("() => { const r = document.getElementById('nla11y-btn').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }")
            tap(pg, mob, ac[0], ac[1]); pg.wait_for_timeout(800)
            R["a11y_open"] = pg.evaluate("""() => { const p = document.getElementById('nla11y-panel'); if (!p || p.hidden) return null; const r = p.getBoundingClientRect();
              const w = document.querySelector('#nlcta .nlcta-wa').getBoundingClientRect(); const h = document.elementFromPoint(w.left + w.width / 2, w.top + w.height / 2);
              return { panel: [Math.round(r.top), Math.round(r.bottom)], inView: r.top >= 0 && r.bottom <= innerHeight && r.left >= 0 && r.right <= innerWidth, barStillHittable: !!(h && h.closest('#nlcta')) }; }""")
            pg.screenshot(path=os.path.join(OUT, f"{TAG}-{key}-a11y.png"))
            tap(pg, mob, ac[0], ac[1]); pg.wait_for_timeout(500)
            pg.evaluate("() => { const d = document.querySelector('#nlps .nlw-deals'); if (d) d.scrollIntoView({ block: 'center', behavior: 'instant' }); }"); pg.wait_for_timeout(700)
            pg.screenshot(path=os.path.join(OUT, f"{TAG}-{key}-card.png"))
            R["errors"] = errs
            res[key] = R
            print(key, json.dumps({k: (v if not isinstance(v, dict) or "fails" not in v else {"steps": v["steps"], "tested": v["tested"], "clipped": v["clipped"], "fails": v["fail_count"], "first": v["fails"][:2]}) for k, v in R.items()}, ensure_ascii=False), flush=True)
            ctx.close()
    br.close()
res["_applied"] = APPLIED; res["_whatsapp_requests"] = len(WA)
json.dump(res, open(os.path.join(OUT, f"{TAG}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("applied:", APPLIED, "| whatsapp requests:", len(WA))
