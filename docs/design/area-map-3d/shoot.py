"""Verify preview.html in headless Chrome (Playwright, channel="chrome") on desktop and phone.

Writes screenshots to shots/ and prints a JSON report: page errors, console errors, failed requests,
whether each card opened, and whether the card stays inside the viewport.
Run: python shoot.py
"""
import json
import os
import pathlib
import time

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)
URL = (HERE / "preview.html").as_uri()
ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]

WAIT_IDLE = """() => new Promise(res => {
  const m = window.__nlam; if (!m) return res('no-map');
  const done = () => res(m.loaded() && m.areTilesLoaded() ? 'idle' : 'timeout');
  if (m.loaded() && m.areTilesLoaded()) { m.once('idle', () => res('idle')); m.triggerRepaint(); setTimeout(done, 4000); return; }
  m.once('idle', () => res('idle')); setTimeout(done, 25000);
})"""

POINT = """(id) => {
  const m = window.__nlam;
  const d = JSON.parse(document.getElementById('nlam-data').textContent);
  const r = d.renewal.find(x => x.id === id);
  const p = m.project([r.lng, r.lat]);
  const b = m.getCanvas().getBoundingClientRect();
  return {x: b.left + p.x, y: b.top + p.y, inside: p.x > 0 && p.y > 0 && p.x < b.width && p.y < b.height};
}"""

CARD = """() => {
  const c = document.getElementById('nlam-card');
  if (c.hidden) return {open: false};
  const r = c.getBoundingClientRect();
  return {open: true, text: c.innerText.replace(/\\s+/g, ' ').trim(),
          left: Math.round(r.left), right: Math.round(r.right), top: Math.round(r.top), bottom: Math.round(r.bottom),
          vw: innerWidth, vh: innerHeight,
          inside: r.left >= 0 && r.right <= innerWidth && r.top >= 0 && r.bottom <= innerHeight};
}"""


def run(pw, name, ctx_args, renewal_id, project_sel):
    report = {"name": name, "page_errors": [], "console_errors": [], "failed_requests": []}
    browser = pw.chromium.launch(channel="chrome", headless=True, args=ARGS)
    ctx = browser.new_context(**ctx_args)
    page = ctx.new_page()
    page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
    page.on("console", lambda m: m.type == "error" and report["console_errors"].append(m.text))
    page.on("requestfailed", lambda r: report["failed_requests"].append(r.url[:140]))
    t0 = time.time()
    page.goto(URL, wait_until="load")
    page.wait_for_function("window.__nlam && window.__nlam.isStyleLoaded()", timeout=60000)
    report["idle"] = page.evaluate(WAIT_IDLE)
    page.wait_for_timeout(1500)
    report["load_s"] = round(time.time() - t0, 1)
    report["map"] = page.evaluate("""() => { const m = window.__nlam; return {
        zoom: +m.getZoom().toFixed(2), pitch: Math.round(m.getPitch()), bearing: Math.round(m.getBearing()),
        cooperative: m.cooperativeGestures.isEnabled(),
        layers: ['nlam-3d','nlam-edge','nlam-places','nlam-renewal','nlam-proj-halo'].filter(l => m.getLayer(l)),
        buildings_rendered: (() => { try { return m.queryRenderedFeatures({layers: ['nlam-3d']}).length; } catch (e) { return 'query error: ' + e.message; } })(),
        places_rendered: (() => { try { return m.queryRenderedFeatures({layers: ['nlam-places']}).length; } catch (e) { return 'query error'; } })(),
        renewal_rendered: (() => { try { return m.queryRenderedFeatures({layers: ['nlam-renewal']}).length; } catch (e) { return 'query error'; } })(),
        pins: document.querySelectorAll('.nlam-pin').length,
        pins_compact: [...document.querySelectorAll('.nlam-pin.is-compact')].map(e => e.getAttribute('aria-label')),
        fonts: {serif: document.fonts.check('600 20px "Noto Serif Hebrew"', 'אב'), sans: document.fonts.check('600 16px Assistant', 'אב')},
        h2_font: getComputedStyle(document.querySelector('.nlam h2')).fontFamily,
        attribution: (document.querySelector('.maplibregl-ctrl-attrib-inner') || {}).innerText || '' }; }""")
    frame = page.locator(".nlam-frame")
    frame.scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    page.screenshot(path=str(SHOTS / f"{name}-full.png"), full_page=True)
    page.screenshot(path=str(SHOTS / f"{name}-map.png"))

    # 1) a renewal pin, drawn on the map canvas
    pt = page.evaluate(POINT, renewal_id)
    report["renewal_point"] = pt
    if ctx_args.get("has_touch"):
        page.touchscreen.tap(pt["x"], pt["y"])
    else:
        page.mouse.click(pt["x"], pt["y"])
    page.wait_for_timeout(1300)
    report["renewal_card"] = page.evaluate(CARD)
    page.screenshot(path=str(SHOTS / f"{name}-card-renewal.png"))
    page.click("#nlam-x")
    page.wait_for_timeout(300)

    # 2) a project pin (HTML marker)
    pin = page.locator(project_sel).first
    report["project_pin_compact"] = "is-compact" in (pin.get_attribute("class") or "")
    box = pin.locator(".nlam-pin-foot").bounding_box()
    fx, fy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    if ctx_args.get("has_touch"):
        page.touchscreen.tap(fx, fy)
    else:
        page.mouse.click(fx, fy)
    page.wait_for_timeout(1300)
    report["project_card"] = page.evaluate(CARD)
    page.screenshot(path=str(SHOTS / f"{name}-card-project.png"))

    # 3) reset view returns home
    page.click("#nlam-reset")
    page.wait_for_timeout(1400)
    report["after_reset"] = page.evaluate("() => ({zoom: +window.__nlam.getZoom().toFixed(2), card_hidden: document.getElementById('nlam-card').hidden})")
    browser.close()
    return report


def main():
    out = []
    with sync_playwright() as pw:
        out.append(run(pw, "desktop-1366", {"viewport": {"width": 1366, "height": 900}, "device_scale_factor": 1, "locale": "he-IL"},
                       "jabotinsky-152", ".nlam-pin--hero"))
        out.append(run(pw, "phone-390", {"viewport": {"width": 390, "height": 844}, "device_scale_factor": 2, "is_mobile": True,
                                         "has_touch": True, "locale": "he-IL"},
                       "zlotisti-4", ".nlam-pin:has-text('DUO')"))
    print(json.dumps(out, ensure_ascii=False, indent=1))
    json.dump(out, open(SHOTS / "report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
