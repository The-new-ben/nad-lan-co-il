# -*- coding: utf-8 -*-
"""HAD-790 (20.11.2026): press the Kikar showroom journey as a visitor, after the showroom moved under the title, the paragraph
and the buttons. Hebrew and English, a 390 px phone and a 1440 desktop:
  1 order   the title, the paragraph and the buttons come before the showroom (h1 < lead < buttons < #nlsr)
  2 tower   press tower B's handle: the tower opens (the "all towers" button shows)
  3 floor   tap the tower in the picture: a floor and a side are chosen (the page hears nl:facing with a floor)
  4 home    the card's "enter the apartment" opens the apartment screen (#nlck shown)
  5 360     the step "inside" opens the apartment's 360 ([data-360] in the apartment screen)
  6 basket  the step "basket" opens the basket (.nlc__title shown)
  7 call    the video-call link points at a room or the call form on this page (#nlsch exists)
  8 dira    a shared link #dira=B24-262 opens tower B, floor 24, with the showroom in view
  python kikar_journey_check.py <tag>     (KF_LOCAL set = the precheck, see kikar_route.py)
Screenshots and result.json to docs/qa/had-790/kikar-journey/<tag>/."""
import os, sys, json, time
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kikar_route import LOCAL, precheck_routes  # noqa: E402

TAG = sys.argv[1] if len(sys.argv) > 1 else "live"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "qa", "had-790", "kikar-journey", TAG)
os.makedirs(OUT, exist_ok=True)
PAGES = [("he", "/projects/hamedina/"), ("en", "/projects/hamedina-en/")]
DEV = [("phone390", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)),
       ("desk1440", dict(viewport={"width": 1440, "height": 900}))]
INIT = """window.__ev = []; addEventListener('nl:facing', e => window.__ev.push(['facing', e.detail && e.detail.floor, e.detail && e.detail.tower]));
addEventListener('nl:cockpit', e => window.__ev.push(['cockpit', e.detail && e.detail.screen]));"""
VIS = "(s) => { const e = document.querySelector(s); if (!e) return false; const r = e.getBoundingClientRect(); const c = getComputedStyle(e); return r.width > 0 && r.height > 0 && c.display !== 'none' && c.visibility !== 'hidden' && !e.closest('[hidden]'); }"
ORDER = """() => { const T = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return r.height ? Math.round(r.top + scrollY) : null; };
  return { h1: T('h1'), lead: T('.nl-lead'), cta: T('.nlps-ctawrap'), sr: T('#nlsr'), real: !!document.querySelector('#nlsr.nlsr'), map: T('#nlpjx-map') }; }"""


def shot(pg, name):
    pg.screenshot(path=os.path.join(OUT, name + ".png"))


def run(pg, dev, lang, path):
    steps = {}
    base = "https://nad-lan.co.il" + path + "?kf=%d" % time.time()
    pg.goto(base, wait_until="load", timeout=120000)
    try:
        pg.wait_for_selector("#nlsr.nlsr .nlsr-h[data-tower]", state="attached", timeout=30000)
    except Exception:
        raise RuntimeError("no showroom: " + json.dumps(pg.evaluate("() => { const n = document.getElementById('nlsr'); return [location.href, n ? n.className : 'none', n ? n.innerHTML.length : 0, document.querySelectorAll('.nlsr-h').length]; }")))
    pg.wait_for_timeout(1200)
    o = pg.evaluate(ORDER)
    steps["order"] = bool(o["real"] and o["h1"] is not None and o["h1"] < o["lead"] < o["cta"] < o["sr"]), o
    shot(pg, "%s-%s-1-first" % (dev, lang))
    # tower B
    pg.locator("#nlsr .nlsr-h[data-tower='B']").scroll_into_view_if_needed()
    pg.locator("#nlsr .nlsr-h[data-tower='B']").click()
    pg.wait_for_timeout(1500)
    steps["tower"] = pg.evaluate(VIS, "#nlsr .nlsr-back"), None
    # a floor: tap the middle of the tower picture, then a little higher and lower until one is chosen
    st = pg.locator("#nlsr .nlsr-img").bounding_box(); sg = pg.locator("#nlsr .nlsr-stage").bounding_box()
    got = None
    for fy in (0.5, 0.42, 0.58, 0.35, 0.65, 0.3, 0.7):
        x = st["x"] + st["width"] * 0.5; y = max(sg["y"] + 10, min(sg["y"] + sg["height"] - 10, st["y"] + st["height"] * fy))
        if dev.startswith("phone"):
            pg.touchscreen.tap(x, y)
        else:
            pg.mouse.click(x, y)
        pg.wait_for_timeout(900)
        f = [e for e in pg.evaluate("window.__ev") if e[0] == "facing" and e[1]]
        if f:
            got = f[-1]; break
    steps["floor"] = bool(got), got
    shot(pg, "%s-%s-2-floor" % (dev, lang))
    # the apartment screen
    go = pg.locator("#nlsr [data-go='home']")
    if go.count():
        go.first.scroll_into_view_if_needed(); go.first.click(); pg.wait_for_timeout(2500)
    steps["home"] = pg.evaluate(VIS, "#nlck"), [e for e in pg.evaluate("window.__ev") if e[0] == "cockpit"][-1:]
    shot(pg, "%s-%s-3-apartment" % (dev, lang))
    # close the apartment screen (Escape), then the step "inside" (the 360)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(800)
    if pg.evaluate(VIS, "#nlck"):
        x = pg.locator("#nlck [data-x], #nlck .nlck-x, #nlck button[aria-label]").first
        try:
            x.click(timeout=3000); pg.wait_for_timeout(800)
        except Exception:
            pass
    pg.evaluate("() => { const b = document.querySelector('#nlsr [data-step=\"inside\"]'); if (b) b.click(); }")
    pg.wait_for_timeout(3500)
    steps["360"] = pg.evaluate("() => { const c = document.getElementById('nlck'); return !!(c && !c.hidden && c.querySelector('[data-360]')); }"), [e for e in pg.evaluate("window.__ev") if e[0] == "cockpit"][-1:]
    shot(pg, "%s-%s-4-360" % (dev, lang))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(800)
    pg.evaluate("() => { const c = document.getElementById('nlck'); if (c && !c.hidden) { const x = c.querySelector('[data-x], .nlck-x, .nlck__x'); if (x) x.click(); } }")
    pg.wait_for_timeout(600)
    # the basket
    pg.evaluate("() => { const b = document.querySelector('#nlsr [data-step=\"basket\"]'); if (b) b.click(); }")
    pg.wait_for_timeout(2000)
    steps["basket"] = pg.evaluate(VIS, ".nlc__title"), pg.evaluate("() => (document.querySelector('.nlc__title') || {}).textContent || ''")
    shot(pg, "%s-%s-5-basket" % (dev, lang))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(600)
    # the video call
    href = pg.evaluate("() => { const a = document.querySelector('#nlsr .nlsr-call'); return a ? a.getAttribute('href') : null; }")
    steps["call"] = bool(href and ("room=new" in href or (href == "#nlsch" and pg.evaluate("() => !!document.getElementById('nlsch')")))), href
    # the shared apartment link
    pg.goto(base.replace("?kf=", "?kf=d") + "#dira=B24-262", wait_until="load", timeout=120000)
    pg.wait_for_selector("#nlsr.nlsr .nlsr-stage", state="attached", timeout=30000)  # a tower is open: no tower handles
    pg.wait_for_timeout(2500)
    d = pg.evaluate("""() => { const n = document.getElementById('nlsr'); const r = n.getBoundingClientRect();
      const b = document.querySelector('#nlsr .nlsr-back'); return { top: Math.round(r.top), inView: r.top < innerHeight * 0.5 && r.bottom > 0,
      towerOpen: !!(b && !b.hidden), card: ((document.querySelector('#nlsr .nlsr-card') || {}).textContent || '').replace(/\\s+/g, ' ').slice(0, 90) }; }""")
    steps["dira"] = bool(d["inView"] and d["towerOpen"] and "24" in d["card"]), d
    shot(pg, "%s-%s-6-dira" % (dev, lang))
    return steps


res, allok = [], True
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for dev, o in DEV:
        for lang, path in PAGES:
            ctx = b.new_context(**o)
            ctx.add_init_script(INIT)
            if LOCAL:
                precheck_routes(ctx, lang)
            pg = ctx.new_page()
            try:
                s = run(pg, dev, lang, path)
            except Exception as e:
                s = {"error": (False, str(e)[:300])}
            ok = all(v[0] for v in s.values())
            allok &= ok
            res.append(dict(device=dev, lang=lang, ok=ok, steps={k: [v[0], v[1]] for k, v in s.items()}))
            print(("OK  " if ok else "BAD ") + dev + " " + lang + " " + " ".join("%s:%s" % (k, "ok" if v[0] else "BAD(" + json.dumps(v[1], ensure_ascii=False)[:160] + ")") for k, v in s.items()))
            ctx.close()
            time.sleep(1)
    b.close()
json.dump(res, open(os.path.join(OUT, "result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ALL OK" if allok else "SOME BAD")
