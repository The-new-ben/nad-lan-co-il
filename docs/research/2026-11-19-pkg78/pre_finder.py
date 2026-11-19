# -*- coding: utf-8 -*-
"""HAD-793 pre-release: the live /properties/ page with the LOCAL finder.js/css and the live payload plus the v4 areas (computed here
the same way inc/near-finder.php does). Screens desktop + phone into pre/."""
import asyncio, io, json, os, re, sys, urllib.request
from playwright.async_api import async_playwright
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
OUT = os.path.join(os.path.dirname(__file__), "pre" if (sys.argv[1:] or ["pre"])[0] == "pre" else "after"); os.makedirs(OUT, exist_ok=True)
php = io.open(os.path.join(PLUG, "inc", "catalog-plus.php"), encoding="utf-8").read()
XY = {m[0]: (float(m[1]), float(m[2])) for m in re.findall(r"'([^']+)' => array\( ([\d.]+), ([\d.]+) \)", php.split("function nadlan_cp_city_coords", 1)[1].split("}", 1)[0])}
XY.update({'קריית אונו': (32.0631, 34.8557), 'מודיעין מכבים רעות': (31.8969, 35.0104), 'רמת השרון': (32.1461, 34.8394)})
BIG = ['תל אביב יפו', 'ירושלים', 'חיפה', 'באר שבע', 'ראשון לציון', 'פתח תקווה', 'אשדוד', 'נתניה', 'חולון', 'בני ברק', 'רמת גן', 'בת ים', 'רחובות', 'אשקלון', 'הרצליה', 'כפר סבא', 'מודיעין מכבים רעות', 'רעננה', 'אילת', 'הוד השרון', 'גבעתיים', 'קריית אונו', 'רמת השרון', 'יבנה']
V = json.load(io.open(os.path.join(PLUG, "assets", "instruments", "data", "value.json"), encoding="utf-8"))
AREAS = [{"n": n, "lat": XY[n][0], "lng": XY[n][1], "r4": c["r4"], "q": c.get("q4") or c.get("q", ""), "url": c.get("page", ""), "big": (100 - BIG.index(n)) if n in BIG else 0}
         for n, c in V["cities"].items() if c.get("r4") and n in XY]
print("areas", len(AREAS))
live = json.loads(urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il/wp-json/nadlan/v1/near-finder", headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read())
live["areas"] = AREAS; live["areas_src"] = "עסקאות סגורות לפי רשות המסים, חציון לפי עיר ורבעון, קובץ " + V["file"]
print("live listings", len(live["listings"]), "projects", len(live["projects"]))
JS = open(os.path.join(PLUG, "assets", "near-finder", "finder.js"), "rb").read()
CSS = open(os.path.join(PLUG, "assets", "near-finder", "finder.css"), "rb").read()
TAG = sys.argv[1] if len(sys.argv) > 1 else "pre"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        for tag, kw in [("desktop", dict(viewport={"width": 1440, "height": 900})),
                        ("phone", dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True))]:
            ctx = await b.new_context(**kw); pg = await ctx.new_page()
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            if TAG == "pre":
                await pg.route(re.compile(r".*/near-finder/finder\.js.*"), lambda r: r.fulfill(body=JS, content_type="application/javascript"))
                await pg.route(re.compile(r".*/near-finder/finder\.css.*"), lambda r: r.fulfill(body=CSS, content_type="text/css"))
                await pg.route(re.compile(r".*/wp-json/nadlan/v1/near-finder(\?.*)?$"), lambda r: r.fulfill(body=json.dumps(live, ensure_ascii=False), content_type="application/json"))
            await pg.goto("https://nad-lan.co.il/properties/?t793=" + TAG, wait_until="domcontentloaded", timeout=90000)
            await pg.wait_for_timeout(1500)
            await pg.evaluate("document.getElementById('nlnf') && document.getElementById('nlnf').scrollIntoView()")
            await pg.wait_for_timeout(9000)
            await pg.screenshot(path=os.path.join(OUT, "%s-properties-%s.png" % (TAG, tag)))
            info = await pg.evaluate("""()=>{const f=document.getElementById('nlnf-few');return {few: f && !f.hidden ? f.innerText : null, legend: (document.getElementById('nlnf-legend')||{}).innerText, count: (document.getElementById('nlnf-count')||{}).innerText}}""")
            print(tag, json.dumps(info, ensure_ascii=False)); print("errors", errs[:5])
            if tag == "phone":
                await pg.evaluate("document.getElementById('nlnf-few') && document.getElementById('nlnf-few').scrollIntoView({block:'center'})")
                await pg.wait_for_timeout(1200); await pg.screenshot(path=os.path.join(OUT, "%s-properties-phone-few.png" % TAG))
            await ctx.close()
        await b.close()
asyncio.run(main())
