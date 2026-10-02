# -*- coding: utf-8 -*-
"""HAD-390: do the floating WhatsApp bar (#nlcta) and the accessibility button (#nla11y-btn) cover the price, the facts,
.nlw-exlink or any control, in the part of the screen the reader sees? Kikar he + en, widths 320/360/390/412/768/1440, the
apartment chosen (the card docked), the whole page scrolled from top to bottom in steps.
The reading area is the viewport, minus an opaque full-width bottom band when there is one (the band is the page's own reserved
space, like a toolbar: what passes under it is below the fold, not covered).
  python band_probe.py <tag> [--local] [--only he-390,en-768]
--local applies the HUNKS of band_hunks.py to the page's HTML (the inline PHP output) and swaps world.css/world.js/example.js
from the working tree: nothing is deployed."""
import io, os, sys, time, json, importlib.util
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAG = sys.argv[1]; LOCAL = "--local" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
PL = os.path.join(REPO, "plugins", "nadlan-config")
OUT = os.path.join(REPO, "docs", "qa", "had-390"); os.makedirs(OUT, exist_ok=True)
CT = {".js": "application/javascript", ".css": "text/css", ".json": "application/json"}
HUNKS = []
if LOCAL:
    spec = importlib.util.spec_from_file_location("band_hunks", os.path.join(REPO, "scripts", "project-stage", "consult_band_396.py"))
    bh = importlib.util.module_from_spec(spec); spec.loader.exec_module(bh); HUNKS = bh.HTML_HUNKS
URL = {"he": "https://nad-lan.co.il/projects/hamedina/", "en": "https://nad-lan.co.il/projects/hamedina-en/"}
NW = {"he": "צפון-מערבית", "en": "North-west"}
APPLIED = {}


def route(r):
    u = r.request.url; path = u.split("?")[0]
    if "wa.me" in u or "analytics" in u or "googletagmanager" in u or "hotjar" in u or r.request.method != "GET":
        return r.abort()
    if LOCAL and r.request.resource_type == "document":
        resp = r.fetch(); body = resp.text()
        for name, old, new in HUNKS:
            c = body.count(old)
            APPLIED[name] = max(APPLIED.get(name, 0), c)
            body = body.replace(old, new)
        return r.fulfill(response=resp, body=body)
    if LOCAL and "/wp-content/plugins/nadlan-config/assets/project-stage/world/" in path:
        rel = path.split("/wp-content/plugins/nadlan-config/")[1]
        f = os.path.join(PL, *rel.split("/")); ext = os.path.splitext(f)[1]
        if os.path.exists(f) and ext in CT:
            return r.fulfill(status=200, body=open(f, "rb").read(), headers={"content-type": CT[ext]})
    return r.continue_()


MEAS = r"""() => {
  const vw = innerWidth, vh = innerHeight;
  const box = document.getElementById('nlcta'), wa = box && box.querySelector('.nlcta-wa'), acc = document.getElementById('nla11y-btn');
  const R = (e) => { if (!e) return null; const r = e.getBoundingClientRect(); return r.width && r.height ? r : null; };
  const bx = R(box), band = bx && bx.width >= vw * 0.9 && bx.bottom >= vh - 2 ? bx : null;
  const readBottom = band ? band.top : vh;
  const fl = [['wa', R(wa)], ['acc', R(acc)]].filter((x) => x[1]);
  const inter = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
  const clip = (r) => ({ left: Math.max(0, r.left), right: Math.min(vw, r.right), top: Math.max(0, r.top), bottom: Math.min(readBottom, r.bottom) });
  const T = {
    deals: '#nlps .nlw-deals', exlink: '#nlps .nlw-exlink',
    facts: '#nlps .nlw-facts, #nlws-facts td, #nlws-facts th, #nlws-facts li, #nlws-facts p, #nlws-prices td, #nlws-prices th, #nlws-prices p',
    controls: '#nlps button, #nlps a[href], #nlps input, #nlps [role=button], #nlps-pick button, #nlps-pick a[href], .nlps-hero__cta a, main a[href], main button, main summary',
  };
  const out = {};
  for (const [k, q] of Object.entries(T)) {
    let worst = 0, who = null;
    for (const e of document.querySelectorAll(q)) {
      if (e.closest('#nlcta, #nla11y, .nlw--full, .nlex, .nlbk')) continue;
      const r = R(e); if (!r) continue;
      const c = clip(r); if (c.right <= c.left || c.bottom <= c.top) continue;
      for (const [n, f] of fl) { const a = inter(c, f); if (a > worst) { worst = Math.round(a); who = n + ':' + (e.className && e.className.baseVal === undefined ? String(e.className).split(' ')[0] : e.tagName) + ':' + (e.textContent || '').trim().slice(0, 18); } }
    }
    out[k] = [worst, who];
  }
  const wr = R(wa), ar = R(acc);
  out.waAcc = wr && ar ? Math.round(inter(wr, ar)) : 0;
  out.band = !!band; out.waH = wr ? Math.round(wr.height) : 0; out.accH = ar ? Math.round(ar.height) : 0;
  out.y = Math.round(scrollY); out.max = document.documentElement.scrollHeight - vh;
  return out;
}"""
END = r"""() => { const box = document.getElementById('nlcta'); const b = box && box.getBoundingClientRect(); const band = b && b.width >= innerWidth * 0.9 && b.bottom >= innerHeight - 2;
  const readBottom = band ? b.top : innerHeight; const last = [...document.querySelectorAll('footer a, footer p, main p, main a')].filter((e) => e.getBoundingClientRect().height && !e.closest('#nlcta,#nla11y')).pop();
  const r = last && last.getBoundingClientRect(); return { lastBottom: r ? Math.round(r.bottom) : null, readBottom: Math.round(readBottom), reachable: r ? r.bottom <= readBottom + 1 : null, padB: getComputedStyle(document.body).paddingBottom }; }"""

res = {}
CONF = [(L, W) for L in ("he", "en") for W in (320, 360, 390, 412, 768, 1440)]
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    for L, W in CONF:
        key = f"{L}-{W}"
        if ONLY and key not in ONLY:
            continue
        H = 1000 if W >= 1024 else (1024 if W == 768 else (568 if W == 320 else 800 if W == 360 else 844 if W == 390 else 915))
        mob = W <= 768
        kw = dict(viewport={"width": W, "height": H})
        if mob:
            kw.update(is_mobile=True, has_touch=True, device_scale_factor=2)
        ctx = br.new_context(**kw); ctx.route("**/*", route)
        pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        T = pg.touchscreen.tap if mob else pg.mouse.click
        pg.goto(URL[L] + "?bp=%d" % time.time(), wait_until="domcontentloaded", timeout=90000); pg.wait_for_timeout(3500)
        pg.evaluate("() => { const s = document.getElementById('nlps'); window.scrollTo({ top: s.getBoundingClientRect().top + scrollY - 80, behavior: 'instant' }); }"); pg.wait_for_timeout(1500)
        rr = pg.evaluate("() => { const b = document.querySelector('#nlps .nlw').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; }")
        T(int(rr[0] + rr[2] / 2), int(rr[1] + min(160, rr[3] / 3))); pg.wait_for_timeout(6500)
        pg.evaluate("(w) => { const g = [...document.querySelectorAll('#nlps .nlw-apt')].find((x) => x.getAttribute('aria-label').includes(w)); if (g) g.scrollIntoView({ block: 'center', behavior: 'instant' }); }", NW[L]); pg.wait_for_timeout(1500)
        b = pg.evaluate("(w) => { const g = [...document.querySelectorAll('#nlps .nlw-apt')].find((x) => x.getAttribute('aria-label').includes(w)); if (!g) return null; const t = g.querySelector('text').getBoundingClientRect(); return [t.left + t.width / 2, t.top + t.height / 2 + 8]; }", NW[L])
        if b:
            T(int(b[0]), int(b[1])); pg.wait_for_timeout(2500)
        picked = pg.evaluate("() => !!document.querySelector('#nlps .nlw-deals')")
        steps = []; worst = {"deals": [0, None], "exlink": [0, None], "facts": [0, None], "controls": [0, None]}; hit_steps = 0; waacc = 0
        total = pg.evaluate("() => document.documentElement.scrollHeight - innerHeight")
        step = max(120, int(H * 0.22))
        y = 0; shot = 0
        while y <= total + step:
            pg.evaluate("(y) => window.scrollTo({ top: y, behavior: 'instant' })", y); pg.wait_for_timeout(260)
            m = pg.evaluate(MEAS)
            hit = False
            for k in worst:
                if m[k][0] > worst[k][0]:
                    worst[k] = m[k]
                if m[k][0] > 0:
                    hit = True
            if hit:
                hit_steps += 1
                if shot < 2 and m["deals"][0] + m["exlink"][0] > 0:
                    pg.screenshot(path=os.path.join(OUT, f"{TAG}-{key}-hit{shot}.png")); shot += 1
            waacc = max(waacc, m["waAcc"])
            steps.append(m)
            y += step
        end = pg.evaluate(END)
        # the card view, for the eyes
        pg.evaluate("() => { const d = document.querySelector('#nlps .nlw-deals'); if (d) d.scrollIntoView({ block: 'center', behavior: 'instant' }); }"); pg.wait_for_timeout(700)
        pg.screenshot(path=os.path.join(OUT, f"{TAG}-{key}-card.png"))
        res[key] = {"picked": picked, "steps": len(steps), "steps_with_cover": hit_steps, "worst": worst, "wa_acc_overlap": waacc,
                    "band": any(s["band"] for s in steps), "waH": max(s["waH"] for s in steps), "accH": max(s["accH"] for s in steps), "end": end, "errors": errs}
        print(key, json.dumps(res[key], ensure_ascii=False), flush=True)
        ctx.close()
    br.close()
if LOCAL:
    print("hunks applied:", APPLIED)
json.dump(res, open(os.path.join(OUT, f"{TAG}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
