# -*- coding: utf-8 -*-
"""The tenant's personal page (opened from a WhatsApp link, no app, no password), shown in the lab with
the REAL server's answer (docs/design-lab/rentals/portal-<lang>.json, written by portal_payload.php).
Phone 390 and desktop 1440, he + en: the page, "I paid" (report a payment), "something broke" (a repair).
Screenshots -> docs/design-lab/rentals/shots/portal/ (for the manual and the film).
Usage: python scripts/rentals/lab_portal.py [base_url]   (server: python -m http.server 47914)"""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/design-lab/rentals/shots/portal"
OUT.mkdir(parents=True, exist_ok=True)
checks = []


def check(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:140] if info != "" else ""))


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for lang in ("he", "en"):
        payload = json.loads((ROOT / ("docs/design-lab/rentals/portal-%s.json" % lang)).read_text(encoding="utf-8"))
        for dev, vp in (("phone", {"width": 390, "height": 844}), ("desk", {"width": 1440, "height": 900})):
            ctx = b.new_context(viewport=vp, device_scale_factor=2 if dev == "phone" else 1, is_mobile=(dev == "phone"), has_touch=(dev == "phone"), locale="he-IL" if lang == "he" else "en-GB")
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.route("**/fake-rest/rm/portal", lambda route: route.fulfill(status=200, content_type="application/json", body=json.dumps(payload, ensure_ascii=False)))
            pg.route("**/fake-rest/rm/portal/act", lambda route: route.fulfill(status=200, content_type="application/json", body="{}"))
            pg.goto(BASE + "?lang=" + lang + "#/today", wait_until="networkidle")
            pg.wait_for_selector(".nlrm-kpis", timeout=15000)
            pg.add_script_tag(url="../../../plugins/nadlan-config/assets/rentals/rm-portal.js")
            pg.wait_for_function("typeof NLRM.mountPortal === 'function'")
            pg.evaluate("""async (lang) => {
                const get = (n) => fetch('../../../plugins/nadlan-config/assets/rentals/i18n/' + n + '.json').then(r => r.json());
                const he = await get('he'), en = await get('en');
                const el = document.getElementById('app'); el.innerHTML = ''; el.className = '';
                NLRM.mountPortal(el, { rest: '/fake-rest', lang: lang, strings: { he: he.ui, en: en.ui }, msg: { he: he.msg, en: en.msg } }, { kind: 'tenant', token: 'x'.repeat(43) });
            }""", lang)
            pg.wait_for_timeout(1500)
            txt = pg.inner_text("#app")
            check("%s %s the tenant's page shows the books' balance" % (lang, dev), ("6,400" in txt), "")
            pg.screenshot(path=str(OUT / ("%s-%s-portal.png" % (lang, dev))), full_page=True)
            for q, name in (("paid", "report-paid"), ("ticket", "repair")):
                btn = pg.locator("[data-p='%s']" % q)
                if btn.count():
                    btn.first.click(); pg.wait_for_timeout(600)
                    pg.screenshot(path=str(OUT / ("%s-%s-%s.png" % (lang, dev, name))))
                    for _ in range(2):
                        if pg.locator(".nlrm-layer").count():
                            pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
            check("%s %s no page errors" % (lang, dev), not errs, errs[:2])
            ctx.close()
    b.close()
print("\n%d checks, %d failed" % (len(checks), len([c for c in checks if not c[1]])))
