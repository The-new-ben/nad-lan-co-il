import sys, json, glob, os, shutil
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]
log = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, has_touch=True, locale="he-IL", record_video_dir=OUT + "/raw", record_video_size={"width": 780, "height": 1688})
    pg = ctx.new_page()
    pg.goto("https://nad-lan.co.il/my-rentals/", wait_until="domcontentloaded")
    pg.wait_for_timeout(8000)
    pg.get_by_role("button", name="לראות", exact=True).click(); pg.wait_for_timeout(4500)
    pg.get_by_role("button", name="לטפל עכשיו", exact=True).click(); pg.wait_for_timeout(5000)
    pg.screenshot(path=OUT + "/journey-phone-0-building.png")
    pg.get_by_role("link", name="להיכנס לדירה").click()
    pg.wait_for_function("window.NLRMTour && window.NLRM && NLRM.store && NLRM.store.d", timeout=40000)
    pg.wait_for_timeout(4000)
    names = pg.evaluate("window.NLRMTour.stops()")
    log.append([0, names[0], pg.evaluate("location.hash")])
    for i in range(1, len(names)):
        pg.click("#nlrm-tour [data-tour='next']"); pg.wait_for_timeout(4500 if i == 3 else 3500)
        log.append([i, names[i], pg.evaluate("location.hash"), pg.evaluate("window.NLRMTour.at()")])
        pg.screenshot(path=OUT + "/journey-phone-stop-%02d.png" % (i + 1))
    last = pg.evaluate("(() => { const a = document.querySelector('#nlrm-tour .nlrm-tour-row a.nlrm-tour-go'); return a ? [a.innerText, a.getAttribute('href')] : null; })()")
    log.append(["last", last])
    pg.wait_for_timeout(2500)
    v = pg.video.path(); ctx.close(); b.close()
    shutil.copy(v, OUT + "/journey-phone.webm")
print(json.dumps(log, ensure_ascii=False))
