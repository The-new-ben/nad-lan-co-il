# -*- coding: utf-8 -*-
"""P9c (1.72.375, design system v104.2) shots for preview_hamedina.py --p9c: the five Kikar pages on the release copy deploy375
writes, served locally (no WordPress, nothing sent). Per language, at 390x844 (a phone, 2x) and 1440x900:
  1. the phone's first screen at scroll 0 / 300 / 700, measured with kh_first_screen_check.MEASURE (the WhatsApp bar vs the
     buttons, the tabs and the answer paragraph; the accessibility button vs the tabs and the buttons);
  2. the accessibility button swept over the page (every 20 px of scroll): what it sits on, and a shot where the world's tabs
     pass its corner;
  3. the floor view, tower C, floor 30, facing west, the window view: the button "היכנסו לדירה לדוגמה" (and on another facing the
     quiet link that leads to it);
  4. a real click on the button: the album at the floor view's time of day (sunset), then the evening, then the same window on
     floor 20, then the end of the album;
  5. the 360 in the fleet's viewer (tour.js), from the album's button; Escape back to the album, Escape out;
  6. what loaded, and when: nothing of the example before the press; the bytes at the album and at the 360.
Receipt: p9c-shots/receipt.json. Shots: WebP."""
import io, json, os, re, time

UA_PHONE = "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Mobile Safari/537.36"
PLUG = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config")
EX_RE = re.compile(r"/assets/project-stage/(hamedina/tour/|world/example\.(js|css)|tour\.(js|css))")

A11Y_SWEEP = r"""() => { const R = (e) => { const r = e.getBoundingClientRect(); return r.height ? { l: r.left, r: r.right, t: r.top, b: r.bottom } : null; };
 const a = document.querySelector('#nla11y-btn'); const A = a && R(a);
 const ov = (x, y) => x && y ? Math.max(0, Math.min(x.r, y.r) - Math.max(x.l, y.l)) * Math.max(0, Math.min(x.b, y.b) - Math.max(x.t, y.t)) : 0;
 const out = [];
 for (const e of document.querySelectorAll('#nlps button, #nlps a, #nlps input, .nlps-hero__cta a')) { const r = R(e); const o = ov(A, r); if (o > 0) out.push({ w: (e.className || e.tagName).toString().split(' ')[0] + ':' + (e.textContent || '').trim().slice(0, 18), px2: Math.round(o) }); }
 const lead = document.querySelector('.nl-lead'); const L = lead && R(lead);
 return { y: Math.round(scrollY), A: A && { t: Math.round(A.t), b: Math.round(A.b) }, lift: (document.getElementById('nla11y') || { style: {} }).style.transform || '', out, onLead: Math.round(ov(A, L)) }; }"""


def shots(pages, asset, guard, served, receipt, langs, out, origin):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    import kh_first_screen_check as KFS
    receipt.update({"first_screen": {}, "a11y": {}, "example": {}, "bytes": {}})
    sizes = lambda urls: sum(os.path.getsize(os.path.join(PLUG, *u.split("/wp-content/plugins/nadlan-config/", 1)[1].split("?")[0].split("/"))) for u in urls)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader"])
        for lang in langs:
            path = "/projects/hamedina" + ("" if lang == "he" else "-" + lang) + "/"
            for size, w, h, mob in (("390", 390, 844, True), ("1440", 1440, 900, False)):
                ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1,
                                    **({"user_agent": UA_PHONE} if mob else {}), locale={"he": "he-IL", "en": "en-US", "fr": "fr-FR", "ru": "ru-RU", "ar": "ar"}[lang])
                ctx.route("**/*", guard)
                ctx.route(re.compile(r"https://nad-lan\.co\.il/wp-content/plugins/nadlan-config/.*"), asset)
                def serve_page(html):
                    def f(route):
                        route.fulfill(status=200, body=html, content_type="text/html; charset=utf-8")
                    return f
                ctx.route(re.compile(re.escape(origin + path) + r"\?pv=.*"), serve_page(pages[lang]))
                pg = ctx.new_page()
                errs, reqs = [], []
                pg.on("pageerror", lambda e: errs.append(str(e)[:240]))
                pg.on("console", lambda m: errs.append("console " + m.type + ": " + m.text[:200]) if m.type == "error" else None)
                pg.on("request", lambda r: reqs.append(r.url) if EX_RE.search(r.url) else None)
                pg.goto(origin + path + "?pv=%d" % time.time(), wait_until="load", timeout=120000)
                pg.wait_for_timeout(3500)
                pre = f"{lang}-{size}"
                rec = {}
                # 1. the first screen
                if mob:
                    rows = []
                    for y in (0, 300, 700):
                        pg.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})")
                        pg.wait_for_timeout(1100)
                        m = pg.evaluate(KFS.MEASURE)
                        rows.append(m)
                        pg.screenshot(path=os.path.join(out, f"{pre}-first-y{y}.png"))
                        print(KFS.line(pre, m))
                    receipt["first_screen"][lang] = rows
                else:
                    pg.screenshot(path=os.path.join(out, f"{pre}-first-y0.png"))
                # 2. the accessibility button swept over the page
                H = pg.evaluate("document.documentElement.scrollHeight")
                hits, tab_shot = [], None
                for y in range(0, min(2600, H), 20):
                    pg.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})")
                    pg.wait_for_timeout(260)  # the corner's move is a 0.18 s glide: measure where it settles
                    m = pg.evaluate(A11Y_SWEEP)
                    if m["out"]:
                        hits.append(m)
                    if tab_shot is None:
                        tt = pg.evaluate("(() => { const t = document.querySelector('#nlps .nlw-tab'); if (!t) return null; const r = t.getBoundingClientRect(); return r.bottom; })()")
                        if tt is not None and h - 70 <= tt <= h - 10:
                            tab_shot = y
                if tab_shot is not None:
                    pg.evaluate(f"window.scrollTo({{top:{tab_shot},behavior:'instant'}})")
                    pg.wait_for_timeout(700)
                    pg.screenshot(path=os.path.join(out, f"{pre}-a11y-tabs.png"))
                receipt["a11y"][pre] = {"scrolls_with_overlap": [x["y"] for x in hits], "tab_shot_scroll": tab_shot,
                                         "on_tabs": [x for x in hits if any(o["w"].startswith("nlw-tab") for o in x["out"])][:6],
                                         "samples": hits[:4], "a11y_on_lead_px2_max": max([x["onLead"] for x in hits] + [0])}
                print(pre, "a11y overlaps at", len(hits), "scrolls; on a world tab:", len(receipt["a11y"][pre]["on_tabs"]), "| tab shot at", tab_shot)
                # 3. the floor view with the example's button
                pg.evaluate("window.scrollTo({top:0,behavior:'instant'})")
                pg.evaluate("document.getElementById('nlps').scrollIntoView({block:'center'})")
                try:
                    pg.wait_for_function("window.__nlpsWorld && document.querySelector('.nlw-poster.is-gone')", timeout=90000)
                except Exception as e:
                    errs.append("world not ready: " + str(e)[:100])
                pg.wait_for_timeout(800)
                before_press = [u for u in reqs if EX_RE.search(u)]
                pg.evaluate("(()=>{const w=window.__nlpsWorld; w.setMode('tower','user'); w.pickTower('C','user'); w.setFloor(30,'user'); w.setFacing(0,'user');})()")
                pg.wait_for_timeout(1800)
                if not mob or lang in ("he", "en"):  # the quiet link on another facing (the sheet folds on a phone: open it)
                    if mob:
                        pg.evaluate("window.__nlpsWorld.collapse(false)")
                        pg.wait_for_timeout(500)
                    pg.evaluate("document.getElementById('nlps').scrollIntoView({block:'end'})")
                    pg.wait_for_timeout(700)
                    pg.locator("#nlps").screenshot(path=os.path.join(out, f"{pre}-floor-C30-north-link.png"))
                    rec["link"] = pg.evaluate("(document.querySelector('#nlps [data-exgo]')||{}).textContent || null")
                pg.evaluate("(()=>{const w=window.__nlpsWorld; w.setFacing(270,'user'); w.setView('window'); w.setSun({tod:'sunset'});})()")
                pg.wait_for_timeout(2400)
                pg.evaluate("document.getElementById('nlps').scrollIntoView({block:'end'})")
                pg.wait_for_timeout(900)
                pg.locator("#nlps").screenshot(path=os.path.join(out, f"{pre}-floor-C30-west-button.png"))
                btn = pg.locator("#nlps [data-example]").first
                rec["button"] = btn.text_content() if btn.count() else None
                rec["button_box"] = btn.bounding_box() if btn.count() else None
                rec["state"] = pg.evaluate("window.__nlpsWorld.getState()")
                # 4. the press: the album
                reqs_before = len(reqs)
                if btn.count():
                    btn.click()
                    try:
                        pg.wait_for_function("document.querySelector('.nlex .nlex__pic img') && document.querySelector('.nlex .nlex__pic img').complete && document.querySelector('.nlex .nlex__strip img')", timeout=30000)
                    except Exception as e:
                        errs.append("album not ready: " + str(e)[:100])
                    pg.wait_for_timeout(1500)
                    pg.screenshot(path=os.path.join(out, f"{pre}-album.png"))
                    album = pg.evaluate("""() => { const x = window.__nlExample; const r = document.querySelector('.nlex'); const wa = r && r.querySelector('.nlex__wa');
                        return { shown: x && x.shown, tod: x && x.tod, pick: window.__nlpsPick, label: (r.querySelector('.nlex__label') || {}).textContent,
                                 chipOnPicture: !!r.querySelector('.nlex__hero > .nlex__chip'), title: (r.querySelector('.nlex__title') || {}).textContent,
                                 eyebrow: (r.querySelector('.nlex__eyebrow') || {}).textContent, cap: (r.querySelector('[data-cap]') || {}).textContent,
                                 wa: wa && decodeURIComponent((new URL(wa.href).searchParams.get('text')) || ''), dir: r.dir, lang: r.lang,
                                 focus: document.activeElement && document.activeElement.className }; }""")
                    album_reqs = reqs[reqs_before:]
                    rec["album"] = album
                    receipt["bytes"][pre] = {"before_press": before_press, "album_files": sorted(set(u.split("?")[0].rsplit("/", 1)[1] for u in album_reqs)), "album_bytes": sizes(sorted(set(album_reqs)))}
                    # the evening, then the same window on floor 20
                    pg.locator('.nlex [data-tod="evening"]').click()
                    pg.wait_for_timeout(1600)
                    pg.screenshot(path=os.path.join(out, f"{pre}-album-evening.png"))
                    rec["world_tod_after_album_evening"] = pg.evaluate("window.__nlpsWorld.getState().tod")
                    pg.locator('.nlex [data-twist="20"]').click()
                    pg.wait_for_timeout(1600)
                    pg.screenshot(path=os.path.join(out, f"{pre}-album-twist20.png"))
                    pg.evaluate("(() => { const b = document.querySelector('.nlex__body'); b.scrollTop = b.scrollHeight; })()")
                    pg.evaluate("document.querySelector('.nlex__notes').open = true")
                    pg.evaluate("(() => { const b = document.querySelector('.nlex__body'); b.scrollTop = b.scrollHeight; })()")
                    pg.wait_for_timeout(700)
                    pg.screenshot(path=os.path.join(out, f"{pre}-album-end.png"))
                    pg.evaluate("(() => { const b = document.querySelector('.nlex__body'); b.scrollTop = 0; })()")
                    # 5. the 360 in the fleet's viewer
                    r360 = len(reqs)
                    pg.locator(".nlex .nlex__go360").click()
                    try:
                        pg.wait_for_function("document.querySelector('.nlat-viewer.is-ready')", timeout=40000)
                    except Exception as e:
                        errs.append("360 not ready: " + str(e)[:100])
                    pg.wait_for_timeout(2500)
                    pg.screenshot(path=os.path.join(out, f"{pre}-360.png"))
                    rec["viewer"] = pg.evaluate("""() => { const v = document.querySelector('.nlat-viewer'); if (!v) return null;
                        return { dir: v.dir, lang: v.lang, title: (v.querySelector('.nlat-viewer__title') || {}).textContent, chip: (v.querySelector('.nlds-sample') || {}).textContent,
                                 cap: (v.querySelector('.nlat-viewer__cap') || {}).textContent, hint: (v.querySelector('.nlat-viewer__hint') || {}).textContent,
                                 scene: window.__nlTour && window.__nlTour.scene }; }""")
                    viewer_reqs = reqs[r360:]
                    receipt["bytes"][pre].update({"viewer_files": sorted(set(u.split("?")[0].rsplit("/", 1)[1] for u in viewer_reqs)), "viewer_bytes": sizes(sorted(set(viewer_reqs)))})
                    pg.keyboard.press("Escape")
                    pg.wait_for_timeout(600)
                    rec["after_escape_1"] = pg.evaluate("({ viewer: !!document.querySelector('.nlat-viewer'), album: !!document.querySelector('.nlex'), focus: document.activeElement && document.activeElement.className })")
                    pg.keyboard.press("Escape")
                    pg.wait_for_timeout(600)
                    rec["after_escape_2"] = pg.evaluate("({ album: !!document.querySelector('.nlex'), pick: window.__nlpsPick, focus: document.activeElement && (document.activeElement.dataset.example || document.activeElement.className) })")
                rec["errors"] = errs[:12]
                receipt["example"][pre] = rec
                print(pre, json.dumps({k: rec.get(k) for k in ("button", "album", "viewer", "after_escape_1", "after_escape_2", "errors")}, ensure_ascii=False)[:900])
                print(pre, "bytes", json.dumps(receipt["bytes"].get(pre), ensure_ascii=False)[:500])
                ctx.close()
        b.close()
    for f in sorted(os.listdir(out)):
        if f.endswith(".png"):
            Image.open(os.path.join(out, f)).convert("RGB").save(os.path.join(out, f[:-4] + ".webp"), "WEBP", quality=86, method=6)
            os.remove(os.path.join(out, f))
    for f in ["_page-%s.html" % l for l in langs]:  # the rendered pages carry the site's public map token: not kept
        if os.path.exists(os.path.join(out, f)):
            os.remove(os.path.join(out, f))
    receipt["local_files_served"] = served
    io.open(os.path.join(out, "receipt.json"), "w", encoding="utf-8").write(json.dumps(receipt, ensure_ascii=False, indent=1))
    print("shots in", out)
