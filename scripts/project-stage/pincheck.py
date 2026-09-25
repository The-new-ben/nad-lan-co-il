"""The quarter's pins while the stage turns (the site loop, R4; design system QuarterPins): no two visible pins may cover
each other. Drags the stage through 24 steps of its orbit and checks every pair of visible pins at each step.
On 25.9.2026 it found overlaps in 8 of 24 steps on 1.72.264 and none on 1.72.265.
  python scripts/project-stage/pincheck.py <page url> [--mobile]
Leave a pause between runs against the live site: each run loads the page without the cache."""
import json, sys, time
from playwright.sync_api import sync_playwright
url = sys.argv[1]
mob = "--mobile" in sys.argv
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-gpu"])
    ctx = b.new_context(viewport={"width": 390, "height": 844} if mob else {"width": 1440, "height": 900}, device_scale_factor=2 if mob else 1, is_mobile=mob, has_touch=mob,
                        user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36" if mob else None)
    pg = ctx.new_page(); pg.set_default_timeout(180000)
    pg.goto(url, wait_until="load")
    pg.evaluate("document.getElementById('nlps').scrollIntoView({block: 'center'})")
    pg.wait_for_function("window.__nlpsStage && window.__nlpsStage.phase && window.__nlpsStage.phase !== 'poster'", timeout=150000)
    time.sleep(4)
    worst = 0; samples = 0; seen = set()
    # turn the camera through the orbit in steps (the stage's own API when present; otherwise drag)
    box = pg.evaluate("(() => { const r = document.getElementById('nlps').getBoundingClientRect(); return {x: r.left, y: r.top, w: r.width, h: r.height}; })()")
    for i in range(24):
        if i:
            cx, cy = box["x"] + box["w"] * 0.5, box["y"] + box["h"] * 0.55
            pg.mouse.move(cx, cy); pg.mouse.down(); pg.mouse.move(cx - 40, cy, steps=4); pg.mouse.up()
            time.sleep(0.8)
        r = pg.evaluate("""() => { const v = [...document.querySelectorAll('.rbs-qpin')].filter(b => b.style.visibility === 'visible').map(b => { const r = b.getBoundingClientRect(); return {n: b.textContent, x: r.left, y: r.top, w: r.width, h: r.height}; });
          let bad = []; for (let i = 0; i < v.length; i++) for (let j = i + 1; j < v.length; j++) { const a = v[i], c = v[j];
            if (a.x < c.x + c.w && c.x < a.x + a.w && a.y < c.y + c.h && c.y < a.y + a.h) bad.push(a.n + ' x ' + c.n); }
          // 1.72.272: the stage's chrome too (the first-use hint while it shows, the light switch, the caption)
          for (const u of ['.rbs-hint:not(.is-gone)', '.rbs-presets', '.rbs-caption']) {
            const e = document.querySelector(u); if (!e) continue; const r = e.getBoundingClientRect(); if (!r.width) continue;
            for (const a of v) if (a.x < r.left + r.width && r.left < a.x + a.w && a.y < r.top + r.height && r.top < a.y + a.h) bad.push(a.n + ' x ' + u);
          }
          return {n: v.length, names: v.map(x => x.n), bad}; }""")
        samples += 1; worst = max(worst, len(r["bad"])); seen.update(r["names"])
        if r["bad"]: print("OVERLAP at step", i, r["bad"])
    print("samples", samples, "| overlaps (worst step)", worst, "| pins seen:", json.dumps(sorted(seen), ensure_ascii=False))
    b.close()
