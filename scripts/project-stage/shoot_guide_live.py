# -*- coding: utf-8 -*-
"""HAD-743 (17.11.2026): photographs the deals guide on the LIVE page, no parameter, in a real Chrome: phone 375x812 and desktop
1366x900, three moments each: she appears, she answers (a tap on a deal), the leave-details form. With --submit the desktop run
also sends ONE test lead through the form (name "בדיקה אוטומטית - למחיקה", phone 0500000000) and prints the server answer.
python scripts/project-stage/shoot_guide_live.py [--submit]"""
import os, sys, time, json
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(REPO, "docs", "qa", "had-743", "guide-live-" + time.strftime("%Y%m%d-%H%M"))
os.makedirs(OUT, exist_ok=True)
URL = "https://nad-lan.co.il/developer-deals/"
SUBMIT = "--submit" in sys.argv
NOANIM = ".nldg *{transition:none!important}"
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for tag, vp, mobile in (("phone", {"width": 375, "height": 812}, True), ("desktop", {"width": 1366, "height": 900}, False)):
        ctx = b.new_context(viewport=vp, device_scale_factor=2, is_mobile=mobile, has_touch=mobile, locale="he-IL")
        pg = ctx.new_page()
        pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
        pg.add_style_tag(content=NOANIM)
        pg.wait_for_function("() => { const b = document.querySelector('.nldg-bub'); return b && b.classList.contains('is-in') && b.querySelector('.nldg-say').textContent.length > 100; }", timeout=30000)
        pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(OUT, tag + "-1-appears.png"))
        pg.click(".nldg-bx")
        it = pg.locator('.nldm-list [data-pick="upview"]')
        it.scroll_into_view_if_needed(); pg.wait_for_timeout(400); it.click()
        pg.wait_for_function("() => { const b = document.querySelector('.nldg-bub'); return b.classList.contains('is-in') && b.querySelector('.nldg-say').textContent.indexOf('לפי הפרסום') > 0; }", timeout=20000)
        pg.wait_for_timeout(700)
        pg.screenshot(path=os.path.join(OUT, tag + "-2-answers.png"))
        res[tag + "_answer"] = pg.evaluate("() => [document.querySelector('.nldg-bub .nldg-say').textContent, [...document.querySelectorAll('.nldg-bub .nldg-act')].map(a => a.textContent)]")
        pg.click(".nldg-bub .nldg-act >> nth=0")  # "השאירו פרטים על המבצע"
        pg.wait_for_selector("form.nldg-lead:not([hidden])", timeout=10000)
        pg.fill("#nldg-ln", "בדיקה אוטומטית - למחיקה")
        pg.fill("#nldg-lp", "050-0000000")
        pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(OUT, tag + "-3-details.png"))
        res[tag + "_form"] = pg.evaluate("() => ({topic: document.querySelector('.nldg-lt').textContent, consent: document.querySelector('.nldg-lc').textContent.slice(0, 60), video: document.body.innerText.indexOf('שיחת וידאו') >= 0 && !!document.querySelector('.nldg-pan') && document.querySelector('.nldg-pan').innerText.indexOf('וידאו') >= 0})")
        if SUBMIT and tag == "desktop":
            with pg.expect_response(lambda r: "/wp-json/nadlan/v1/lead" in r.url, timeout=30000) as rr:
                pg.click(".nldg-ls")
            r = rr.value
            res["lead_http"] = r.status
            try: res["lead_body"] = r.json()
            except Exception: res["lead_body"] = r.text()[:300]
            pg.wait_for_timeout(1500)
            pg.screenshot(path=os.path.join(OUT, tag + "-4-sent.png"))
            res["sent_text"] = pg.evaluate("() => document.querySelector('.nldg-ans .nldg-say').textContent")
        ctx.close()
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
print("OUT", OUT)
