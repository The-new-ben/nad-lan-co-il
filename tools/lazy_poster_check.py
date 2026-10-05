# -*- coding: utf-8 -*-
"""Read-only: the Kikar film posters are lazy (HAD-421 step 3). In a real headless Chrome at a phone width and at desktop:
1) after load, no film poster was fetched; 2) after scrolling the film into view, the visible videos have their poster set
and fetched, and the hidden ones (display:none at that width) still have none; 3) a press on Play still plays.

  python tools/lazy_poster_check.py https://nad-lan.co.il/projects/hamedina/"""
import json, sys, time

RX = r"/kikar-hamedina-(film|facilities)[^/]*poster/"


def run(p, url, w, h, mobile):
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if mobile else 1, is_mobile=mobile, has_touch=mobile)
    page = ctx.new_page()
    page.goto(url + ("&" if "?" in url else "?") + "nllazy=" + str(int(time.time())), wait_until="load", timeout=120000)
    page.wait_for_timeout(2500)
    js_posters = "() => performance.getEntriesByType('resource').filter(e => new RegExp(%s).test(e.name)).map(e => e.name.split('/').pop())" % json.dumps(RX)
    at_load = page.evaluate(js_posters)
    script_ran = page.evaluate("() => !!document.getElementById('nlws-film-lazy')")
    for _ in range(4):
        page.evaluate("() => { const v = [...document.querySelectorAll('#nlws-film-v2 video')].find(x => getComputedStyle(x).display !== 'none'); v.scrollIntoView({block: 'center'}); }")
        page.wait_for_timeout(900)
    page.wait_for_timeout(1500)
    vids = page.evaluate("() => [...document.querySelectorAll('#nlws-film video')].map(v => ({cls: v.className.split('--')[1], shown: getComputedStyle(v).display !== 'none', poster: (v.getAttribute('poster') || '').split('/').pop(), h: Math.round(v.getBoundingClientRect().height)}))")
    after = page.evaluate(js_posters)
    play = page.evaluate("""async () => { const v = [...document.querySelectorAll('#nlws-film-v2 video')].find(x => getComputedStyle(x).display !== 'none');
        v.muted = true; try { await v.play(); } catch (e) { return 'play error ' + e.message; }
        const a = v.currentTime; await new Promise(r => setTimeout(r, 1500)); const t = v.currentTime; v.pause(); return {paused: v.paused, t1: +a.toFixed(2), t2: +t.toFixed(2)}; }""")
    b.close()
    return {"width": w, "script_in_dom": script_ran, "posters_at_load": at_load, "posters_after_scroll": after, "videos": vids, "play": play}


def main(url):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        out = [run(p, url, 390, 844, True), run(p, url, 1366, 900, False)]
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
