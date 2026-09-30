# -*- coding: utf-8 -*-
"""HAD-376, live, before and after: the view from the floor on the four pages, in Chrome (Playwright, the same engine as
content_first_check.py), at 1440x900 and on a 390x844 phone.

Real input only: the visitor's own "open the 3D" button on the poster (this headless Chrome is a software renderer, so the page
shows the poster first, as on a weak phone), a click on the stage's canvas, then the stage's own keys: ArrowUp picks a floor
and ArrowRight turns to the next example apartment, round the whole floor. At each facing it reads the named labels the view
shows. Each page runs twice in the same way:
  after   the live page as it is (places.json?ver=1.72.372 from the site; every label must be seen in the NEW data)
  before  the same live page with only places.json answered by the OLD file (in this test browser, nothing on the site
          changes; every label must be seen in the OLD data, which proves the swap took)
and the two are compared facing by facing. Screenshots of the view's map: docs/qa/had-376-sightlines/shots/.
Read-only: GET requests only (anything else, analytics and WhatsApp are blocked).

  python scripts/project-stage/sight_live_check.py <before-dir> [--only duo,rainbow] [--w 1440,390]"""
import io, json, os, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BEFORE = sys.argv[1]
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
WIDTHS = [int(w) for w in sys.argv[sys.argv.index("--w") + 1].split(",")] if "--w" in sys.argv else [1440, 390]
OUT = os.path.join(REPO, "docs", "qa", "had-376-sightlines", "shots")
os.makedirs(OUT, exist_ok=True)
PAGES = {"rainbow": "/projects/rainbow-tel-aviv/", "duo": "/projects/duo-tel-aviv/", "dimri": "/projects/dimri-yama-sde-dov/",
         "ashira": "/projects/ashira-sde-dov/"}
W = {"education": 3, "outdoors": 2.4, "transport": 3.2, "food": 2.2, "essentials": 1.9, "health": 2.3, "community": 2}
UA_PHONE = "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36"
BLOCK = ("google-analytics", "googletagmanager", "facebook", "clarity", "hotjar", "wa.me", "api.whatsapp", "doubleclick")


def ang(a, b):
    d = abs((a % 360) - (b % 360))
    return min(d, 360 - d)


def seen_names(pl, bearing, fb):
    """arealife.js around(bearing, {floor, seen: true, half: 48, noBus: true, lang: 'he'}): the names it may label"""
    return {p["name"] for p in pl["places"] if not p.get("generic") and p.get("k") != "bus_stop" and ang(p["bearing"], bearing) <= 48
            and (p.get("sight") or {}).get(str(fb)) and p.get("g") in W and p.get("name")}


def band(pl, floor):
    bs = [int(b) for b in (pl.get("bands") or [10, 25, 36])]
    return min(bs, key=lambda x: abs(x - floor))


STATE_JS = """() => {
  const pins = [...document.querySelectorAll('.nlal-pin')].filter((e) => e.style.visibility !== 'hidden' && e.offsetParent !== null)
    .map((e) => e.textContent.replace(/\\s+/g, ' ').trim());
  const sel = window.__nlpsStage && window.__nlpsStage.getSelection ? window.__nlpsStage.getSelection() : null;
  return {sel, view: window.__nlpsView && window.__nlpsView.getView ? window.__nlpsView.getView() : null, pins};
}"""
# a point of the canvas the pointer really reaches (the stage's buttons sit on top of it in places): the upper sky first
SKY_JS = """() => {
  const c = document.querySelector('#nlps canvas'); if (!c) return null; const r = c.getBoundingClientRect();
  for (const fy of [0.08, 0.14, 0.2, 0.3]) for (const fx of [0.12, 0.88, 0.25, 0.75, 0.5]) {
    const x = r.left + r.width * fx, y = r.top + r.height * fy;
    if (document.elementFromPoint(x, y) === c) return [x, y];
  }
  return null;
}"""
CENTRE_MAP_JS = """() => { const m = document.querySelector('#nlps-view .mapboxgl-map'); if (!m) return false; const r = m.getBoundingClientRect();
  window.scrollBy({top: r.top - (innerHeight - r.height) / 2, behavior: 'instant'}); return true; }"""


def run(br, pk, path, width, old_body):
    phone = width < 600
    ctx = br.new_context(viewport={"width": width, "height": 844 if phone else 900}, device_scale_factor=2 if phone else 1,
                         is_mobile=phone, has_touch=phone, user_agent=UA_PHONE if phone else None, locale="he-IL")
    ctx.route("**/*", lambda r: r.abort() if any(x in r.request.url for x in BLOCK) or r.request.method != "GET" else r.continue_())
    if old_body is not None:   # "before": only the registry answered by the old file, in this browser
        ctx.route("**/project-stage/*/places.json*", lambda r: r.fulfill(status=200, content_type="application/json", body=old_body))
    pg = ctx.new_page()
    got = []
    pg.on("response", lambda resp: got.append((resp.url, resp.status)) if "/places.json" in resp.url else None)
    pg.goto("https://nad-lan.co.il" + path + "?sl=%d" % time.time(), wait_until="load", timeout=120000)
    pg.wait_for_timeout(1500)
    pg.evaluate("document.getElementById('nlps').scrollIntoView({block: 'center', behavior: 'instant'})")
    pg.wait_for_timeout(800)
    if pg.evaluate("!!document.querySelector('#nlps .rbs--fallback')"):
        pg.locator("#nlps .rbs-open").first.click()   # the visitor's own "open the 3D" button on the poster
    pg.evaluate("async () => { await Promise.race([window.__nlpsStage.ready, new Promise((z) => setTimeout(z, 60000))]); }")
    pg.wait_for_timeout(2500)
    pt = pg.evaluate(SKY_JS)
    if pt:
        pg.mouse.click(pt[0], pt[1])                   # a click on the canvas's sky: the canvas takes the keys
    focused = pg.evaluate("document.activeElement && document.activeElement.tagName")
    pg.keyboard.press("ArrowUp")                        # the stage's own key: a floor
    pg.wait_for_timeout(2500)
    facings = []
    for i in range(4):
        if i:
            # back to the stage, the keyboard focus where a Tab would put it (a click on the sky would clear the floor)
            pg.evaluate("document.getElementById('nlps').scrollIntoView({block: 'center', behavior: 'instant'}); document.querySelector('#nlps canvas').focus()")
            pg.keyboard.press("ArrowRight")             # the next example apartment round the floor
            pg.wait_for_timeout(2500)
        st = {}
        for _ in range(20):
            pg.wait_for_timeout(1000)
            st = pg.evaluate(STATE_JS)
            if st.get("view") and (st.get("sel") or {}).get("floor"):
                break
        pg.wait_for_timeout(2500)                       # the map settles (idle), the labels update
        st = pg.evaluate(STATE_JS)
        sel = st.get("sel") or {}
        facings.append({"floor": sel.get("floor"), "unit": sel.get("unit"), "bearing": (st.get("view") or {}).get("bearing"), "pins": st.get("pins") or []})
        try:
            if pg.evaluate(CENTRE_MAP_JS):
                pg.wait_for_timeout(700)
                bb = pg.locator("#nlps-view .mapboxgl-map").first.bounding_box()
                pg.screenshot(path=os.path.join(OUT, f"{pk}-{width}-{'before' if old_body is not None else 'after'}-{sel.get('unit') or i}.png"), clip=bb)
        except Exception as e:
            print("   shot failed", str(e)[:80])
    ctx.close()
    return {"places": got, "focused": focused, "facings": facings}


def main():
    from playwright.sync_api import sync_playwright
    report, bad = {}, 0
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel="chrome", headless=True, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        for pk, path in PAGES.items():
            if ONLY and pk not in ONLY:
                continue
            new = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", pk, "places.json"), encoding="utf-8"))
            old_body = io.open(os.path.join(BEFORE, pk + ".places.json"), encoding="utf-8").read()
            old = json.loads(old_body)
            for width in WIDTHS:
                a = run(br, pk, path, width, None)
                b = run(br, pk, path, width, old_body)
                live_req = [u for u in a["places"] if "ver=1.72.372" in u[0] and u[1] == 200]
                rows = []
                ok = bool(live_req) and bool(a["facings"])
                for fa, fb_ in zip(a["facings"], b["facings"]):
                    if fa["bearing"] is None or not fa["floor"]:
                        ok = False
                        continue
                    bnd = band(new, fa["floor"])
                    ns = seen_names(new, fa["bearing"], bnd)
                    os_ = seen_names(old, fb_["bearing"] if fb_["bearing"] is not None else fa["bearing"], bnd)
                    after_ok = all(any(n in pin for n in ns) for pin in fa["pins"])
                    before_ok = all(any(n in pin for n in os_) for pin in fb_["pins"])
                    ok = ok and after_ok and before_ok
                    rows.append({"unit": fa["unit"], "floor": fa["floor"], "band": bnd, "bearing": fa["bearing"], "before": fb_["pins"], "after": fa["pins"],
                                 "after_all_seen_in_new": after_ok, "before_all_seen_in_old": before_ok,
                                 "gone": [p for p in fb_["pins"] if p not in fa["pins"]], "new": [p for p in fa["pins"] if p not in fb_["pins"]]})
                bad += 0 if ok else 1
                report[f"{pk}-{width}"] = {"ok": ok, "live_places_request": live_req[:1], "focused": a["focused"], "facings": rows}
                print(f"== {pk} {width}: {'OK ' if ok else 'BAD'} | live registry {live_req[:1]} | canvas focus {a['focused']}")
                for r in rows:
                    print(f"   floor {r['floor']} (band {r['band']}) {r['unit']} bearing {r['bearing']}: after {len(r['after'])} labels, all seen in the new data: {r['after_all_seen_in_new']} | before {len(r['before'])}, all seen in the old: {r['before_all_seen_in_old']}")
                    if r["gone"]:
                        print("      shown before, not now:", " | ".join(r["gone"]))
                    if r["new"]:
                        print("      shown now, not before:", " | ".join(r["new"]))
        br.close()
    json.dump(report, io.open(os.path.join(OUT, "live-check.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("bad", bad)
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
