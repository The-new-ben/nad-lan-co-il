"""Capture stills of a project's live 3D stage (section#nlps) for the project video.

  python capture.py --slug rainbow-tel-aviv --url https://nad-lan.co.il/projects/rainbow-tel-aviv/
  python capture.py --slug rainbow-tel-aviv --url ... --sizes 1920x1080     # one size only
  python capture.py --slug rainbow-tel-aviv --url ... --keep-ui             # keep the stage's own buttons

Read-only: opens the public page in headless Chrome (WebGL through ANGLE), enlarges the stage to the whole viewport
in THIS browser only (a local style tag, nothing is sent to the site), and screenshots it in these states:

  hero        the opening view, after the intro glide settles
  hero-noon   the same view in the stage's noon light (the preset button), then back to the default light
  facilities  after the legend chip [data-nlps-phase="facilities"] (the glide to the lot, the facility pins on)
  lot         the same camera with every pin hidden (a clean close view of the buildings)
  facility-N  one facility card open (a click on the N-th .rbs-qpin--facility pin)
  quarter     after a quarter chip (selling / building / today), when the page has one
  quarter-own the same view with other developers' pins and the rail/school/park pins hidden (the project's own pin,
              the beach and the river mouth stay)

Saves img/<slug>/stage-<state>_<w>x<h>.jpg (quality 92) and img/<slug>/capture_<w>x<h>.json (what was clicked, which
pins and card text were visible, canvas size, blank-canvas check). Look at every still before you use it.
"""
import argparse, io, json, os, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))

# The stage fills the viewport; the site's header, WhatsApp pill and cookie/accessibility widgets are hidden in this
# browser only. The stage's own buttons (floor hint, sunset/noon, "open" button, caption) are hidden unless --keep-ui:
# the video draws its own permanent "הדמיה להמחשה" label instead of the stage caption.
CSS_STAGE = """
section#nlps { position: fixed !important; inset: 0 !important; width: 100vw !important; height: 100vh !important;
  max-width: none !important; max-height: none !important; margin: 0 !important; border-radius: 0 !important;
  border: 0 !important; outline: 0 !important; box-shadow: none !important; z-index: 2147483000 !important; }
section#nlps > * { border: 0 !important; border-radius: 0 !important; }
#nlcta, .nlcta, #wpadminbar, [class*="cookie"], [id*="cookie"], [class*="accessib"], [id*="accessib"] { display: none !important; }
html, body { overflow: hidden !important; }
"""
CSS_NO_UI = """
section#nlps .rbs-hint, section#nlps .rbs-presets, section#nlps .rbs-caption, section#nlps .rbs-open,
section#nlps .rbs-facing, section#nlps .rbs-stats { display: none !important; }
"""
CSS_NO_PROJECT_PINS = """
section#nlps .rbs-qpin--project, section#nlps .rbs-qpin--place { visibility: hidden !important; }
section#nlps .rbs-leader { visibility: hidden !important; }
"""
# the quarter still for a project's own video: other developers' name pins, the planned rail stop and the school/park
# pins are hidden; the project's own pin and the sea-side places (beach, river mouth) stay
CSS_QUARTER_OWN = """
section#nlps .rbs-qpin--project, section#nlps .rbs-qpin--rail, section#nlps .rbs-qpin--school,
section#nlps .rbs-qpin--park { visibility: hidden !important; }
"""

STATE_JS = """() => {
  const s = document.querySelector('section#nlps'); const r = s.getBoundingClientRect();
  const vis = el => { const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return b.width > 0 && b.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && b.right > r.left && b.left < r.right && b.bottom > r.top && b.top < r.bottom; };
  const pins = [...s.querySelectorAll('.rbs-qpin')].filter(vis).map(e => ({ text: e.textContent.trim(), cls: e.className }));
  const card = s.querySelector('.rbs-qcard');
  return { stage: [Math.round(r.width), Math.round(r.height)], pins,
           card: card && vis(card) ? card.innerText.trim() : null, cls: s.firstElementChild ? s.firstElementChild.className : '' };
}"""


def parse_size(s):
    w, h = s.lower().split("x")
    return int(w), int(h)


def shot(page, path, quality=92):
    """Screenshot the stage; returns pixel stats of the still (a flat, empty canvas has a tiny spread)."""
    from PIL import Image, ImageStat
    png = page.locator("section#nlps").screenshot(type="png", animations="disabled")
    im = Image.open(io.BytesIO(png)).convert("RGB")
    im.save(path, "JPEG", quality=quality, optimize=True)
    g = im.convert("L").resize((96, 54))
    st = ImageStat.Stat(g)
    return {"size": list(im.size), "lumaMean": round(st.mean[0], 1), "lumaStd": round(st.stddev[0], 1),
            "blank": st.stddev[0] < 6}


def settle(page, ms):
    page.wait_for_timeout(ms)


def capture_size(p, url, slug, w, h, keep_ui, wait_s):
    out_dir = os.path.join(ROOT, "img", slug)
    os.makedirs(out_dir, exist_ok=True)
    b = p.chromium.launch(channel="chrome", headless=True,
                          args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    page = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1, locale="he-IL")
    page.on("pageerror", lambda e: print(f"  [pageerror] {e}"))
    page.goto(url, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_selector("section#nlps", timeout=60000)
    page.evaluate("() => document.querySelector('section#nlps').scrollIntoView({block: 'center'})")
    page.add_style_tag(content=CSS_STAGE + ("" if keep_ui else CSS_NO_UI))
    # the engine starts when the stage is on screen; give the model and the intro glide time
    settle(page, int(wait_s * 1000))
    try:
        page.wait_for_function("() => { const s = document.querySelector('section#nlps .rbs--settled, section#nlps.rbs--settled'); return !!s; }", timeout=12000)
    except Exception:
        print("  (no rbs--settled class seen; continuing on time)")
    settle(page, 1500)
    log = {"url": url, "size": [w, h], "taken": time.strftime("%Y-%m-%d %H:%M:%S"), "states": {}}

    def record(name, extra=None):
        path = os.path.join(out_dir, f"stage-{name}_{w}x{h}.jpg")
        st = page.evaluate(STATE_JS)
        if extra:
            st.update(extra)
        st["pixels"] = shot(page, path)
        st["file"] = os.path.relpath(path, ROOT).replace("\\", "/")
        log["states"][name] = st
        print(f"  {name}: {st['file']} pins={[x['text'] for x in st['pins']]} card={'yes' if st['card'] else 'no'} pixels={st['pixels']}")

    # 1) hero, the neighbours' name pins hidden (the video is about this project)
    tag = page.add_style_tag(content=CSS_NO_PROJECT_PINS)
    settle(page, 400)
    record("hero")
    # the same view in the stage's other light preset (noon), when the stage has one
    if page.evaluate("() => !!document.querySelector('section#nlps [data-preset=\"noon\"]')"):
        page.evaluate("() => document.querySelector('section#nlps [data-preset=\"noon\"]').click()")
        settle(page, 2500)
        record("hero-noon", {"clicked": "[data-preset=noon]"})
        page.evaluate("() => document.querySelector('section#nlps [data-preset=\"sunset\"]').click()")
        settle(page, 2500)
    page.evaluate("t => t.remove()", tag)

    # 2) facilities: the legend chip glides to the lot and shows the facility pins
    chips = page.evaluate("() => [...document.querySelectorAll('[data-nlps-phase]')].map(e => e.dataset.nlpsPhase)")
    log["chips"] = chips
    if "facilities" in chips:
        page.evaluate("() => document.querySelector('[data-nlps-phase=\"facilities\"]').click()")
        settle(page, 3200)
        record("facilities", {"clicked": "[data-nlps-phase=facilities]"})
        # the same close view of the lot without the pins (for a card about the buildings)
        tag = page.add_style_tag(content="section#nlps .rbs-qpin { visibility: hidden !important; }")
        settle(page, 400)
        record("lot", {"clicked": "[data-nlps-phase=facilities]", "hidden": "all pins"})
        page.evaluate("t => t.remove()", tag)
        settle(page, 300)
        # 3) one facility card per distinct facility (first pin of each name)
        names = page.evaluate("""() => [...document.querySelectorAll('section#nlps .rbs-qpin--facility')]
            .map((e, i) => ({ i, name: e.getAttribute('aria-label') || e.textContent.trim() }))""")
        seen = set()
        for it in names:
            if it["name"] in seen:
                continue
            seen.add(it["name"])
            page.evaluate("i => document.querySelectorAll('section#nlps .rbs-qpin--facility')[i].click()", it["i"])
            settle(page, 2600)
            record(f"facility-{len(seen)}", {"clicked": f".rbs-qpin--facility[{it['i']}]", "facility": it["name"]})
            # close the card (Escape) and return to the facilities overview for the next pin
            page.keyboard.press("Escape")
            settle(page, 600)
            page.evaluate("() => { const x = document.querySelector('section#nlps .rbs-qcard-x'); if (x) x.click(); }")
            settle(page, 400)
            page.evaluate("() => document.querySelector('[data-nlps-phase=\"facilities\"]').click()")
            settle(page, 300)
            if page.evaluate("() => !document.querySelectorAll('section#nlps .rbs-qpin--facility')[0] || getComputedStyle(document.querySelectorAll('section#nlps .rbs-qpin--facility')[0]).visibility === 'hidden'"):
                page.evaluate("() => document.querySelector('[data-nlps-phase=\"facilities\"]').click()")
            settle(page, 2400)
    # 4) the quarter: a phase chip other than facilities
    q = next((c for c in ("selling", "building", "today", "permit") if c in chips), None)
    if q:
        page.evaluate("c => document.querySelector(`[data-nlps-phase=\"${c}\"]`).click()", q)
        settle(page, 3600)
        record("quarter", {"clicked": f"[data-nlps-phase={q}]"})
        tag = page.add_style_tag(content=CSS_QUARTER_OWN)
        settle(page, 400)
        record("quarter-own", {"clicked": f"[data-nlps-phase={q}]", "hidden": "other projects, rail, school, park pins"})
        page.evaluate("t => t.remove()", tag)
    with open(os.path.join(out_dir, f"capture_{w}x{h}.json"), "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=1)
    b.close()
    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--sizes", default="1920x1080,1080x1920")
    ap.add_argument("--wait", type=float, default=8.0, help="seconds to wait for the model before the first still")
    ap.add_argument("--keep-ui", action="store_true")
    args = ap.parse_args()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        for s in args.sizes.split(","):
            w, h = parse_size(s)
            print(f"capturing {w}x{h} ...", flush=True)
            capture_size(p, args.url, args.slug, w, h, args.keep_ui, args.wait)


if __name__ == "__main__":
    main()
