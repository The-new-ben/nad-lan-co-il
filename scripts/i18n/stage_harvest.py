# -*- coding: utf-8 -*-
"""HAD-361: the Hebrew the project stages actually show, harvested from the live pages (read-only). For each stage page:
floors on every tower and every example apartment, every facility pin and quarter pin, every legend chip, the view panel,
the 360 room (every scene, spot and style where there is one), the floor's slice. Every visible text node and every
aria-label / title / alt / placeholder with Hebrew is kept; what the server already printed (the page's HTML, handled by
inc/lang-pages.php) is left out. Numbers become pattern captures. Writes docs/i18n/stage-harvest.json.
  python scripts/i18n/stage_harvest.py"""
import io, json, os, re, sys, time, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = [("rainbow-tel-aviv", [None]), ("duo-tel-aviv", ["N", "S"]), ("dimri-yama-sde-dov", ["A", "C"]), ("ashira-sde-dov", ["S1", "N2"])]
GRAB = r"""() => {
  const HE = /[֐-׿]/, out = [];
  const roots = document.querySelectorAll('.nlps-page, .nlat-viewer, .nlsl, .nlbk, #nlps-view, .rbs');
  const seen = new Set();
  for (const r of roots) {
    const w = document.createTreeWalker(r, NodeFilter.SHOW_TEXT, null);
    let n;
    while ((n = w.nextNode())) {
      const t = n.nodeValue.replace(/\s+/g, ' ').trim();
      if (t && HE.test(t) && !seen.has(t)) { seen.add(t); out.push(t); }
    }
    for (const e of r.querySelectorAll('[aria-label],[title],[alt],[placeholder]')) {
      for (const a of ['aria-label', 'title', 'alt', 'placeholder']) {
        const v = (e.getAttribute(a) || '').replace(/\s+/g, ' ').trim();
        if (v && HE.test(v) && !seen.has(v)) { seen.add(v); out.push(v); }
      }
    }
  }
  return out;
}"""
found = collections.OrderedDict()


def keep(pg, where):
    for t in pg.evaluate(GRAB):
        found.setdefault(t, where)


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    for slug, towers in PAGES:
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.goto("https://nad-lan.co.il/projects/%s/?cb=hv%d" % (slug, time.time()), wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_timeout(9000)
        server = pg.evaluate("document.documentElement.outerHTML")
        keep(pg, slug + ":load")
        pg.evaluate("async () => { await window.__nlpsStage.ready; }")
        # floors and apartments
        for tw in towers:
            top = pg.evaluate("(tw) => { const s = window.__nlpsStage; for (let f = 80; f > 0; f--) if (s.floorHeight(f, tw || undefined)) return f; return 0; }", tw)
            for f in sorted(set([1, 2, 5, 10, 16, 25, max(1, top - 3), max(1, top - 1), top])):
                if f > top:
                    continue
                for side in ("n", "e", "s", "w"):
                    uid = (tw + "-" if tw else "") + "%d-%s" % (f, side)
                    pg.evaluate("(u) => { try { window.__nlpsStage.selectUnit(u, 'user'); } catch (e) {} }", uid)
                    pg.wait_for_timeout(350)
                    keep(pg, slug + ":unit")
        # the legend chips and the pins
        chips = pg.locator("[data-nlps-phase]")
        for i in range(chips.count()):
            try:
                chips.nth(i).click(force=True); pg.wait_for_timeout(1500); keep(pg, slug + ":chip")
                pins = pg.locator(".rbs-qpin")
                for k in range(min(pins.count(), 40)):
                    try:
                        pins.nth(k).click(force=True, timeout=2000); pg.wait_for_timeout(500); keep(pg, slug + ":pin")
                    except Exception:
                        pass
            except Exception:
                pass
        # the slice
        try:
            pg.evaluate("() => { try { window.__nlpsStage.selectUnit((window.__nlpsStage.getSelection() || {}).unit || '25-w', 'user'); } catch (e) {} }")
            pg.wait_for_timeout(800)
            if pg.locator(".nlps-slice").count():
                pg.locator(".nlps-slice").click(force=True); pg.wait_for_timeout(1200); keep(pg, slug + ":slice")
                pg.keyboard.press("Escape"); pg.wait_for_timeout(500)
        except Exception as e:
            print("slice", slug, str(e)[:80])
        # the 360 room
        if pg.locator(".nlat__go").count():
            pg.locator(".nlat__go").click(force=True); pg.wait_for_timeout(5000); keep(pg, slug + ":tour")
            scenes = pg.evaluate("window.__nlTour ? window.__nlTour.scenes.map((s) => s.id) : []")
            for sc in scenes:
                pg.evaluate("(id) => window.__nlTour.setView({ scene: id }, 0)", sc); pg.wait_for_timeout(900); keep(pg, slug + ":tour")
                st = pg.locator(".nlat-style")
                for i in range(st.count()):
                    try:
                        st.nth(i).click(timeout=2000); pg.wait_for_timeout(500); keep(pg, slug + ":style")
                    except Exception:
                        pass
            pg.keyboard.press("Escape"); pg.wait_for_timeout(600)
        # facility rooms (Rainbow)
        if pg.locator("button.rbs-qcard-360").count():
            pg.locator("button.rbs-qcard-360").first.click(force=True); pg.wait_for_timeout(4000); keep(pg, slug + ":room")
            pg.keyboard.press("Escape")
        # drop what the server printed: inc/lang-pages.php translates those
        n0 = len(found)
        for t in list(found):
            if found[t].startswith(slug) and t in server:
                pass
        print(slug, "strings so far:", len(found))
        ctx.close()
        globals()["SERVER_" + slug.replace("-", "_")] = server
    b.close()


def norm(t):
    return re.sub(r"\d[\d,.]*", "#", t)


# server-printed strings are handled by the page pass; only the browser's own are kept
servers = [v for k, v in globals().items() if k.startswith("SERVER_")]
client = [t for t in found if not any(t in s for s in servers)]
pat = collections.OrderedDict()
for t in client:
    k = norm(t)
    pat.setdefault(k, []).append(t)
out = {"note": "HAD-361: the stages' browser-made Hebrew (scripts/i18n/stage_harvest.py, the live site). Keys are the strings with numbers as #; examples as found.",
       "count": len(pat), "strings": [{"shape": k, "examples": v[:3], "where": found[v[0]]} for k, v in pat.items()]}
os.makedirs(os.path.join(REPO, "docs", "i18n"), exist_ok=True)
io.open(os.path.join(REPO, "docs", "i18n", "stage-harvest.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
print("done:", len(found), "found,", len(client), "made in the browser,", len(pat), "shapes")
