# -*- coding: utf-8 -*-
"""HAD-790 live check: presses each package-1 fix on the LIVE site in installed Chrome (headful by default, one browser at a time)
and saves screenshots to docs/qa/had-790/after/. Real mouse moves and wheel events through the browser's input (trusted events).

  python scripts/had790/live_check.py            all checks
  python scripts/had790/live_check.py menu deals  only these (menu deals hazards wide price kikar langs phone)
"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

BASE = "https://nad-lan.co.il"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs", "qa", "had-790", "after")
os.makedirs(OUT, exist_ok=True)
ONLY = set(a for a in sys.argv[1:] if not a.startswith("-"))
R = {}


def want(k):
    return not ONLY or k in ONLY


def ok(k, cond, note=""):
    R[k] = {"pass": bool(cond), "note": note}
    print(("PASS " if cond else "FAIL ") + k + (" | " + note if note else ""))


def go(pg, path):
    pg.goto(BASE + path, wait_until="domcontentloaded", timeout=90000)
    pg.wait_for_timeout(3000)


def shot(pg, name, full=False):
    pg.screenshot(path=os.path.join(OUT, name + ".png"), full_page=full)


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless="--headless" in sys.argv, args=["--window-size=1600,1000"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL")
    pg = ctx.new_page()

    if want("menu"):  # 1: the language menu stays open on a slow move across the gap
        go(pg, "/")
        s = pg.locator("#nlhp-top .nlhp-lang > summary")
        bx = s.bounding_box()
        x, y = bx["x"] + bx["width"] / 2, bx["y"] + bx["height"] / 2
        pg.mouse.move(x, y); pg.wait_for_timeout(400)
        opened = pg.evaluate("document.querySelector('#nlhp-top .nlhp-lang').open")
        for i in range(1, 46):  # 45 px down, one pixel every 25 ms (a slow hand)
            pg.mouse.move(x, y + i); pg.wait_for_timeout(25)
        still = pg.evaluate("document.querySelector('#nlhp-top .nlhp-lang').open")
        shot(pg, "1-menu-slow-he-1440")
        ok("menu_slow_he", opened and still, "opened %s, open after a slow 45 px move %s" % (opened, still))
        pg.mouse.move(10, 600); pg.wait_for_timeout(800)
        ok("menu_closes_on_leave", not pg.evaluate("document.querySelector('#nlhp-top .nlhp-lang').open"))

    if want("langs"):  # 8: the four language homes have the site header and its menus
        for L in ("en", "fr", "ru", "ar"):
            go(pg, "/%s/" % L)
            info = pg.evaluate("""() => { const h=document.querySelector('#nlhp-top'); if(!h) return null;
              const vis = e => { const r=e.getBoundingClientRect(); return r.width>0 && r.height>0; };
              return { lang: h.classList.contains('nlhp-top--lang'), dir: h.getAttribute('dir'), panels: h.querySelectorAll('.nlhp-dd:not(.nlhp-lang)').length,
                links: h.querySelectorAll('.nlhp-mega a').length, oldbar: [...document.querySelectorAll('.nlhv2-browse,.nlhv2-langbar,.nlpc-site-header')].filter(vis).length,
                hebrew: [...h.querySelectorAll('.nlhp-mega a, summary')].map(a=>a.textContent).filter(t=>/[\\u0590-\\u05FF]/.test(t)).slice(0,5),
                dashes: (h.textContent.match(/[\\u2013\\u2014]/g)||[]).length }; }""")
            shot(pg, "8-home-%s-1440" % L)
            # open the first menu, as a visitor
            if info and pg.locator("#nlhp-top .nlhp-dd:not(.nlhp-lang) > summary").count():
                pg.locator("#nlhp-top .nlhp-dd:not(.nlhp-lang) > summary").first.hover(); pg.wait_for_timeout(500)
                shot(pg, "8-home-%s-menu-open-1440" % L)
            pg.mouse.move(10, 700); pg.wait_for_timeout(400)
            ok("lang_home_" + L, info and info["lang"] and info["panels"] >= 5 and info["links"] >= 30 and info["oldbar"] == 0 and not info["hebrew"] and info["dashes"] == 0, json.dumps(info, ensure_ascii=False))

    if want("deals"):  # 2 and 3 on the deals map
        go(pg, "/developer-deals/")
        pg.locator("#nldm-map").scroll_into_view_if_needed(); pg.wait_for_timeout(5000)
        m = pg.locator("#nldm-map").bounding_box()
        y0 = pg.evaluate("scrollY")
        # a wheel that passes over the map (the pointer just arrived): the page scrolls, the map does not zoom
        z0 = pg.evaluate("(() => { const c=document.querySelector('#nldm-map'); return c && c.querySelector('.maplibregl-canvas') ? 1 : 0; })()")
        pg.mouse.move(m["x"] + m["width"] / 2, m["y"] + m["height"] / 2); pg.mouse.wheel(0, 300); pg.wait_for_timeout(700)
        y1 = pg.evaluate("scrollY")
        ok("deals_wheel_passes", y1 > y0, "scrollY %d -> %d" % (y0, y1))
        pg.locator("#nldm-map").scroll_into_view_if_needed(); pg.wait_for_timeout(600)
        m = pg.locator("#nldm-map").bounding_box()
        pg.mouse.move(m["x"] + m["width"] / 2, m["y"] + m["height"] / 2); pg.wait_for_timeout(900)
        y2 = pg.evaluate("scrollY")
        pg.mouse.wheel(0, -500); pg.wait_for_timeout(1200)
        y3 = pg.evaluate("scrollY")
        ok("deals_wheel_zooms_on_rest", y3 == y2, "page stayed at %d -> %d while the pointer rested and wheeled" % (y2, y3))
        shot(pg, "2-3-deals-zoomed-1440")
        cut = pg.evaluate("""() => { const c=document.querySelector('#nldm-map').getBoundingClientRect(); let n=0, cutn=0;
          document.querySelectorAll('#nldm-map .nldm-tag:not(.is-tuck)').forEach(t=>{ const r=t.getBoundingClientRect(); if(!r.width) return;
            const inside = r.right>c.left && r.left<c.right && r.bottom>c.top && r.top<c.bottom; if(!inside) return; n++;
            if (r.left < c.left-1 || r.right > c.right+1 || r.top < c.top-1) cutn++; }); return [n, cutn]; }""")
        ok("deals_tags_inside", cut[1] == 0 and cut[0] > 0, "visible tags %d, cut at the edge %d" % tuple(cut))

    if want("hazards"):  # 3 on the hazards map
        go(pg, "/environmental-hazards/")
        loc = pg.locator(".hzm__map").first
        loc.scroll_into_view_if_needed(); pg.wait_for_timeout(5000)
        m = loc.bounding_box()
        pg.mouse.move(m["x"] + m["width"] / 2, m["y"] + m["height"] / 2); pg.wait_for_timeout(900)
        y2 = pg.evaluate("scrollY")
        pg.mouse.wheel(0, -400); pg.wait_for_timeout(1200)
        y3 = pg.evaluate("scrollY")
        coop = pg.evaluate("!!document.querySelector('.hzm__map .maplibregl-cooperative-gesture-screen.maplibregl-show')")
        shot(pg, "3-hazards-zoom-on-rest-1440")
        ok("hazards_wheel_zooms_on_rest", y3 == y2 and not coop, "page %d -> %d, Ctrl message shown %s" % (y2, y3, coop))

    if want("wide"):  # 9: tools at 1920
        pw = ctx.new_page(); pw.set_viewport_size({"width": 1920, "height": 1080})
        for u in ("/purchase-tax-calculator/", "/apartment-prices/", "/buying-apartment/"):
            go(pw, u)
            w = pw.evaluate("Math.round(document.querySelector('.nli').getBoundingClientRect().width)")
            sw = pw.evaluate("document.documentElement.scrollWidth")
            pw.locator(".nli").first.scroll_into_view_if_needed(); pw.wait_for_timeout(600)
            shot(pw, "9-wide%s-1920" % u.strip("/").replace("/", "-").join(["-", ""]))
            ok("wide" + u, w >= 1300 and sw <= 1920, "tool %d px of 1920, page width %d" % (w, sw))
        pw.close()

    if want("price"):  # 4: the price window shows on the owner's link, no meter on the fresh link
        go(pg, "/projects/rainbow-tel-aviv/?nudge=show"); pg.wait_for_timeout(2500)
        op = pg.evaluate("(() => { const c=document.querySelector('#nlnu .nlpa'); return c ? +getComputedStyle(c).opacity : -1; })()")
        shot(pg, "4-price-window-show-1440")
        ok("price_window_visible", op > 0.9, "card opacity %s" % op)
        go(pg, "/projects/rainbow-tel-aviv/?nudge=fresh"); pg.wait_for_timeout(2500)
        meter = pg.evaluate("[...document.querySelectorAll('div')].some(d => (d.textContent||'').indexOf('מצב בדיקה') === 0)")
        ok("price_fresh_no_meter", not meter, "debug line shown: %s" % meter)

    if want("kikar"):  # 6: the floor-29 card (gap 18), opened by its own link, Hebrew and English
        for path, word, L in (("/projects/hamedina/#dira=B29-270", "הקומה הקרובה שצוירה", "he"), ("/projects/hamedina-en/#dira=B29-270", "nearest rendered floor", "en")):
            go(pg, path); pg.wait_for_timeout(5000)
            cap = pg.evaluate("[...document.querySelectorAll('.nlck-cap')].map(e=>e.textContent).join(' / ')")
            shot(pg, "6-kikar-floor29-%s-1440" % L)
            plain = ("מקומה 30" in cap or "floor 30" in cap) and word not in cap
            ok("kikar_floor29_" + L, cap and not plain, cap[:160])

    if want("phone"):  # phone first: the French home and the deals map on a phone
        ph = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="fr-FR")
        pp = ph.new_page()
        for u, n in (("/fr/", "8-home-fr-phone"), ("/en/", "8-home-en-phone"), ("/developer-deals/", "2-deals-phone"), ("/purchase-tax-calculator/", "9-tax-phone")):
            go(pp, u); shot(pp, n)
        go(pp, "/fr/")
        pp.locator("#nlhp-top .nlhp-ico--menu").tap(); pp.wait_for_timeout(700)
        sheet = pp.evaluate("document.querySelector('#nlhp-top').classList.contains('is-open')")
        shot(pp, "8-home-fr-phone-menu")
        sw = pp.evaluate("document.documentElement.scrollWidth")
        ok("phone_fr_menu", sheet and sw <= 390, "sheet open %s, page width %d" % (sheet, sw))
        ph.close()

    b.close()

json.dump(R, open(os.path.join(OUT, "live-check-%s.json" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("%d/%d passed" % (sum(1 for v in R.values() if v["pass"]), len(R)))
