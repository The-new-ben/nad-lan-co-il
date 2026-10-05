# -*- coding: utf-8 -*-
"""Computed-style fingerprint of live pages, to prove a CSS change is cascade-neutral (HAD-421, 5.10.2026).

For every element of each page (headless Chrome, phone 390 and desktop 1366), records the element path and ~30 computed
properties, then a sha256 per page and width. Run before and after a release and compare:

  python tools/style_fingerprint.py --out before.json
  python tools/style_fingerprint.py --out after.json --compare before.json

Elements inside animated or time-dependent parts (the 3D world, films, maps, carousels) are skipped, CSS transitions are
frozen at their end values and opacity is not compared, so equal hashes mean equal styling, not equal timing."""
import argparse, hashlib, io, json, sys, time
from playwright.sync_api import sync_playwright

PAGES = ["/", "/brokers/", "/projects/", "/projects/hamedina/", "/projects/rainbow-tel-aviv/"]
WIDTHS = [(390, 844), (1366, 900)]
PROPS = ["display", "position", "float", "box-sizing", "color", "background-color", "background-image", "font-family", "font-size",
         "font-weight", "font-style", "line-height", "letter-spacing", "text-align", "text-transform", "text-decoration-line",
         "text-decoration-thickness", "text-underline-offset", "text-wrap", "margin-top", "margin-right", "margin-bottom",
         "margin-left", "padding-top", "padding-right", "padding-bottom", "padding-left", "border-top-width", "border-top-style",
         "border-top-color", "border-radius", "outline-style", "outline-width", "outline-offset", "z-index", "gap",
         "flex-direction", "justify-content", "align-items", "grid-template-columns", "max-width", "overflow-x"]
SKIP = "canvas, video, iframe, svg *, .nlws, .nlws *, .nlw-poster, #nlpjx-unimap *, .mapboxgl-map *, [class*=carousel] *, [class*=slider] *"
JS = """([props, skip]) => {
  const skipSet = new Set(document.querySelectorAll(skip));
  const out = [];
  const els = document.body.querySelectorAll('*');
  for (const el of els) {
    if (skipSet.has(el)) continue;
    let path = el.tagName.toLowerCase(), p = el.parentElement, depth = 0;
    while (p && p !== document.body && depth < 4) { path = p.tagName.toLowerCase() + '>' + path; p = p.parentElement; depth++; }
    if (el.id) path += '#' + el.id;
    const cs = getComputedStyle(el);
    out.push(path + '|' + props.map(k => cs.getPropertyValue(k)).join(';'));
    if (out.length >= 6000) break;
  }
  return out;
}"""


def run(base):
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        for w, h in WIDTHS:
            c = b.new_context(viewport={"width": w, "height": h}, is_mobile=w < 768, has_touch=w < 768)
            for u in PAGES:
                pg = c.new_page()
                pg.goto(base + u + ("&" if "?" in u else "?") + "nlsf=%d" % time.time(), wait_until="load", timeout=120000)
                pg.wait_for_timeout(2500)
                # freeze CSS transitions/animations at their end values (a header easing its padding is motion, not styling);
                # opacity is not compared at all (the 3D stages fade their labels every frame from script)
                pg.add_style_tag(content="*,*::before,*::after{transition:none!important;animation:none!important}")
                pg.wait_for_timeout(300)
                rows = pg.evaluate(JS, [PROPS, SKIP])
                res["%s@%d" % (u, w)] = {"n": len(rows), "sha": hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()[:16], "rows": rows}
                pg.close()
            c.close()
        b.close()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://nad-lan.co.il")
    ap.add_argument("--out", required=True)
    ap.add_argument("--compare")
    a = ap.parse_args()
    res = run(a.base)
    io.open(a.out, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False))
    for k, v in res.items():
        print(k, v["n"], v["sha"])
    if a.compare:
        old = json.load(io.open(a.compare, encoding="utf-8"))
        bad = 0
        for k, v in res.items():
            o = old.get(k)
            if not o:
                print("NEW", k); continue
            if o["sha"] == v["sha"]:
                print("SAME", k); continue
            bad += 1
            oset, nset = set(o["rows"]), set(v["rows"])
            print("DIFF", k, "rows before", o["n"], "after", v["n"], "| only before", len(oset - nset), "only after", len(nset - oset))
            for r in list(oset - nset)[:3]:
                print("   -", r[:300])
            for r in list(nset - oset)[:3]:
                print("   +", r[:300])
        print("RESULT", "identical" if not bad else "%d page-widths differ" % bad)
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
