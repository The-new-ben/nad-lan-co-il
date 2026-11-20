# -*- coding: utf-8 -*-
"""The user manual's extra screenshots (HAD-383, 3.10.2026): real presses on the
real app and the real link pages (docs/design-lab/rentals/portal.html renders
rm-portal.js on the sample portfolio), he + en, phone 390 (x2) and desktop 1440.
Writes docs/design-lab/rentals/shots/manual/<lang>-<dev>-<name>.png and
shots/manual/results.json (checks, including what an Excel import does to a
lease that started before this month).
Usage: python scripts/rentals/manual_shots.py [base_dir_url]
       (server: python -m http.server 47914 --bind 127.0.0.1, from the worktree root)"""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47914/docs/design-lab/rentals/"
APP, PORTAL = BASE + "app.html", BASE + "portal.html"
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs/design-lab/rentals/shots/manual"
OUT.mkdir(parents=True, exist_ok=True)
results = {"checks": [], "errors": []}
NAME = {"he": "מיכל אברהם", "en": "Michal Avraham"}
SIG = [(40, 120), (80, 70), (120, 130), (170, 60), (210, 120), (250, 90), (300, 110), (340, 70)]


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:200]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:160] if info != "" else ""))


def shot(pg, lang, dev, name):
    pg.wait_for_timeout(650)  # the layer has finished sliding in
    pg.evaluate("document.querySelectorAll('.nlrm-toast').forEach(function (x) { x.remove(); })")
    pg.screenshot(path=str(OUT / ("%s-%s-%s.png" % (lang, dev, name))))


def close_all(pg):
    for _ in range(5):
        if pg.locator(".nlrm-layer").count():
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(260)


def to_top(pg, sel):
    """scroll an element to the top of its scrolling panel (or the page)"""
    pg.evaluate("(s) => { var el = document.querySelector(s); if (el) { el.scrollIntoView({block: 'start'}); } }", sel)
    pg.wait_for_timeout(250)


def app(pg, lang, hash_="#/today", empty=False):
    pg.goto("about:blank")  # a fresh sample every time (a hash-only change would keep the old state)
    pg.goto(APP + "?lang=" + lang + ("&empty=1" if empty else "") + hash_, wait_until="networkidle")
    pg.wait_for_timeout(700)


def portal(pg, lang, kind):
    pg.goto("about:blank")
    pg.goto(PORTAL + "?lang=%s&kind=%s" % (lang, kind), wait_until="networkidle")
    pg.wait_for_selector(".nlrm-portal .nlrm-card", timeout=10000)
    pg.wait_for_timeout(400)


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for lang in ("he", "en"):
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="he-IL" if lang == "he" else "en-GB")
        pg = ctx.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "404" not in m.text else None)
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        dev = "phone"

        # --- the to-do list on Today
        app(pg, lang)
        to_top(pg, "#nlrm-att-h")
        shot(pg, lang, dev, "today-att")

        # --- an existing lease: the linkage and the securities, with the legal cap line
        pg.evaluate("NLRM.forms.lease(null, 22)")
        pg.wait_for_selector(".nlrm-layer.is-in form", timeout=5000)
        pg.fill(".nlrm-layer.is-in [name='t_name']", NAME[lang])
        pg.fill(".nlrm-layer.is-in [name='rent']", "6000")
        pg.select_option(".nlrm-layer.is-in [name='link_mode']", "cpi")
        pg.fill(".nlrm-layer.is-in [name='sec_cheque']", "18000")
        pg.dispatch_event(".nlrm-layer.is-in [name='sec_cheque']", "input")
        cap = pg.inner_text("#nlrm-capline")
        check("%s lease form shows the legal cap" % lang, "18,000" in cap, cap)
        to_top(pg, ".nlrm-layer.is-in [name='link_mode']")
        pg.evaluate("document.querySelector('.nlrm-layer.is-in .nlrm-pbody').scrollBy(0, -70)")
        shot(pg, lang, dev, "lease-cpi")
        # the same form for a lease that began 14 months ago: "follow payments from"
        start = pg.evaluate("NLRM.addMonths(NLRM.todayIso().slice(0,8) + '01', -14)")
        pg.fill(".nlrm-layer.is-in [name='start_date']", start)
        pg.fill(".nlrm-layer.is-in [name='end_date']", pg.evaluate("(s) => NLRM.addDays(NLRM.addMonths(s, 36), -1)", start))
        pg.dispatch_event(".nlrm-layer.is-in [name='start_date']", "change")
        tf = pg.input_value(".nlrm-layer.is-in [name='track_from']")
        check("%s 'follow payments from' is filled with the 1st of this month" % lang, tf.endswith("-01"), tf)
        pg.evaluate("(() => { var el = document.querySelector(\".nlrm-layer.is-in [name='track_from']\").closest('label'); el.scrollIntoView({block: 'center'}); })()")
        shot(pg, lang, dev, "track-from")
        close_all(pg)

        # --- the apartment card: overview, lease tab
        U = 21 if lang == "he" else 31
        app(pg, lang)
        pg.evaluate("NLRM.open('unit', %d)" % U)
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
        shot(pg, lang, dev, "unit-overview")
        pg.click(".nlrm-ptabs [data-tab='lease']")
        shot(pg, lang, dev, "unit-lease")
        close_all(pg)

        # --- a payment received, and the actions on a line of the books
        app(pg, lang)
        pg.evaluate("NLRM.open('unit', 12)")
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
        pg.click(".nlrm-ptabs [data-tab='money']"); pg.wait_for_timeout(400)
        pg.click(".nlrm-layer.is-in .nlrm-pbody [data-act='pay']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        shot(pg, lang, dev, "payment")
        pg.fill(".nlrm-layer.is-in [name='amount']", "1000")
        pg.click(".nlrm-layer.is-in form [type='submit']"); pg.wait_for_timeout(900)
        row = pg.evaluate("NLRM.store.d.ledger.filter(r => r.lease_id === 202 && r.kind === 'payment' && r.amount === 100000).slice(-1)[0].id")
        pg.click(".nlrm-layer.is-in [data-act='row-more'][data-row='%d']" % row)
        pg.wait_for_selector(".nlrm-layer.is-in [data-sheet-act='void']", timeout=4000)
        shot(pg, lang, dev, "row-more")
        close_all(pg)

        # --- the deposit: above the legal cap is refused, a legal amount is held
        app(pg, lang)
        pg.evaluate("NLRM.open('unit', 31)")
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
        pg.click(".nlrm-ptabs [data-tab='money']"); pg.wait_for_timeout(400)
        pg.click(".nlrm-layer.is-in [data-act='dep-receive']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        pg.fill(".nlrm-layer.is-in [name='amount']", "20000")
        pg.click(".nlrm-layer.is-in form [type='submit']"); pg.wait_for_timeout(700)
        err = pg.inner_text(".nlrm-layer.is-in .nlrm-ferr")
        check("%s deposit above the cap is refused" % lang, "12,900" in err, err)
        shot(pg, lang, dev, "deposit-cap")
        pg.fill(".nlrm-layer.is-in [name='amount']", "5000")
        pg.click(".nlrm-layer.is-in form [type='submit']"); pg.wait_for_timeout(900)
        to_top(pg, ".nlrm-layer.is-in [data-act='dep-apply']")
        pg.evaluate("document.querySelector('.nlrm-layer.is-in .nlrm-pbody').scrollBy(0, -260)")
        shot(pg, lang, dev, "deposit-held")
        # the end of the lease (prorated), then the former tenant's matters on the apartment
        pg.click(".nlrm-ptabs [data-tab='lease']"); pg.wait_for_timeout(400)
        pg.click(".nlrm-layer.is-in [data-act='end-lease']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        shot(pg, lang, dev, "end-lease")
        pg.click(".nlrm-layer.is-in form [type='submit']"); pg.wait_for_timeout(900)
        close_all(pg)
        pg.evaluate("NLRM.open('unit', 31)")
        pg.wait_for_selector(".nlrm-layer.is-in [data-act='former-money']", timeout=5000)
        to_top(pg, ".nlrm-layer.is-in [data-act='former-money']")
        pg.evaluate("document.querySelector('.nlrm-layer.is-in .nlrm-pbody').scrollBy(0, -200)")
        shot(pg, lang, dev, "former")
        close_all(pg)

        # --- a renewal: a new term for the same tenant
        app(pg, lang)
        pg.evaluate("NLRM.open('unit', 11)")
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
        pg.click(".nlrm-ptabs [data-tab='lease']"); pg.wait_for_timeout(400)
        pg.click(".nlrm-layer.is-in [data-act='renew-lease']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        shot(pg, lang, dev, "renew")
        close_all(pg)

        # --- a repair the landlord opens: the urgency is recognised from the words
        app(pg, lang)
        pg.evaluate("NLRM.forms.ticket({ unit: 12 })")
        pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        pg.fill(".nlrm-layer.is-in [name='title']", "אין מים חמים בכלל" if lang == "he" else "No hot water at all")
        pg.dispatch_event(".nlrm-layer.is-in [name='title']", "input")
        tri = pg.inner_text("#nlrm-tri")
        check("%s triage: urgent water heater" % lang, ("דחוף" in tri) or ("Urgent" in tri), tri)
        shot(pg, lang, dev, "ticket-new")
        close_all(pg)

        # --- a WhatsApp reminder, written in the tenant's language
        app(pg, lang)
        pg.evaluate("NLRM.open('unit', %d)" % (21 if lang == "he" else 31))
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
        pg.click(".nlrm-layer.is-in .nlrm-pacts [data-act='wa-remind']")
        pg.wait_for_selector(".nlrm-layer.is-in textarea", timeout=5000)
        txt = pg.input_value(".nlrm-layer.is-in textarea")
        check("%s reminder in the tenant's language" % lang, txt.startswith("שלום" if lang == "he" else "Hi"), txt[:30])
        shot(pg, lang, dev, "wa-remind")
        close_all(pg)

        # --- cheques and the CPI tab on the Money screen
        app(pg, lang, "#/money")
        pg.click("[data-mtab='cheques']"); pg.wait_for_timeout(400)
        to_top(pg, ".nlrm-main .nlrm-seg")
        shot(pg, lang, dev, "cheques")
        pg.click("[data-mtab='cpi']"); pg.wait_for_timeout(400)
        pg.click("#nlrm-cpi [type='submit']"); pg.wait_for_timeout(600)
        to_top(pg, ".nlrm-main .nlrm-seg")
        shot(pg, lang, dev, "cpi")

        # --- a cheque that bounced: the bank fee to the tenant
        app(pg, lang)
        ch = pg.evaluate("NLRM.store.d.ledger.filter(r => r.lease_id === 201 && r.method === 'cheque' && r.status === 'deposited').slice(-1)[0].id")
        pg.evaluate("NLRM.open('unit', 11)")
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
        pg.click(".nlrm-ptabs [data-tab='money']"); pg.wait_for_timeout(400)
        pg.click(".nlrm-layer.is-in [data-act='row-more'][data-row='%d']" % ch); pg.wait_for_timeout(400)
        pg.click(".nlrm-layer.is-in [data-sheet-act='bounce']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        pg.fill(".nlrm-layer.is-in [name='fee']", "25")
        shot(pg, lang, dev, "bounce")
        close_all(pg)

        # --- a former tenant's debt: end the lease, then write the debt off
        app(pg, lang)
        pg.evaluate("NLRM.open('unit', 21)")
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
        pg.click(".nlrm-ptabs [data-tab='lease']"); pg.wait_for_timeout(400)
        pg.click(".nlrm-layer.is-in [data-act='end-lease']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        pg.click(".nlrm-layer.is-in form [type='submit']"); pg.wait_for_timeout(900)
        close_all(pg)
        pg.evaluate("NLRM.open('unit', 21)")
        pg.wait_for_selector(".nlrm-layer.is-in [data-act='former-money']", timeout=5000)
        pg.click(".nlrm-layer.is-in [data-act='former-money']"); pg.wait_for_timeout(500)
        has_wo = pg.locator(".nlrm-layer.is-in [data-act='writeoff']").count()
        check("%s a former tenant's debt offers a write-off" % lang, has_wo == 1, has_wo)
        pg.click(".nlrm-layer.is-in [data-act='writeoff']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        pg.wait_for_timeout(3600)  # the "lease ended" toast fades first
        shot(pg, lang, dev, "writeoff")
        close_all(pg)

        # --- an appliance fault, from the apartment's appliances list
        app(pg, lang)
        pg.evaluate("NLRM.open('unit', 11)")
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
        pg.click(".nlrm-ptabs [data-tab='home']"); pg.wait_for_timeout(2500)
        to_top(pg, ".nlrm-layer.is-in #nlrm-asset-a1")
        pg.evaluate("document.querySelector('.nlrm-layer.is-in .nlrm-pbody').scrollBy(0, -120)")
        shot(pg, lang, dev, "assets")
        close_all(pg)

        # --- choose a professional for a repair
        app(pg, lang)
        pg.evaluate("NLRM.open('ticket', 501)")
        pg.wait_for_selector(".nlrm-layer.is-in [data-act='ticket-vendor']", timeout=5000)
        shot(pg, lang, dev, "ticket-card")
        pg.click(".nlrm-layer.is-in [data-act='ticket-vendor']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        shot(pg, lang, dev, "choose-vendor")
        close_all(pg)

        # --- settings: privacy and the plan
        app(pg, lang, "#/settings")
        to_top(pg, "[data-act='erase']")
        pg.evaluate("window.scrollBy(0, -260)")
        shot(pg, lang, dev, "settings-privacy")

        # --- import from Excel: what happens to a lease that began before this month
        app(pg, lang, "#/today", empty=True)
        sheet = {"he": "כתובת\tעיר\tדירה\tקומה\tשוכר\tטלפון\tשכר דירה\tתחילת חוזה\tסיום חוזה\nהרצל 10\tחולון\tדירה 4\t2\tמיכל אברהם\t050-0000201\t5,200\t1.3.2026\t28.2.2027",
                 "en": "Address\tCity\tApartment\tFloor\tTenant\tPhone\tRent\tLease start\tLease end\n10 Herzl St\tHolon\tApt 4\t2\tMichal Avraham\t050-0000201\t5200\t1.3.2026\t28.2.2027"}[lang]
        pg.click("[data-act='import']"); pg.wait_for_selector(".nlrm-layer.is-in textarea")
        pg.fill(".nlrm-layer.is-in textarea", sheet); pg.click("[data-imp='check']"); pg.wait_for_timeout(300)
        pg.click(".nlrm-layer.is-in [type='submit']"); pg.wait_for_timeout(2000)
        imp = pg.evaluate("(() => { var l = NLRM.store.d.leases[0]; return l ? { start: l.start_date, track_from: (l.terms || {}).track_from || '', open_charges: NLRM.store.d.ledger.filter(r => r.lease_id === l.id && r.kind === 'charge').length, balance: NLRM.moneyOf(l).balance / 100 } : null; })()")
        check("%s import: an old lease is followed from this month (no invented arrears)" % lang, imp is not None and imp["track_from"].endswith("-01") and imp["open_charges"] <= 1, imp)
        results["import_old_lease"] = imp

        # --- the link pages: tenant, payment report, repair report, signing, professional, applicant, quick link
        portal(pg, lang, "t")
        shot(pg, lang, dev, "portal-tenant")
        pg.click("[data-p='paid']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        shot(pg, lang, dev, "portal-paid")
        close_all(pg)
        pg.click("[data-p='ticket']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
        pg.fill(".nlrm-layer.is-in [name='title']", "יש נזילה מתחת לכיור" if lang == "he" else "A leak under the sink")
        shot(pg, lang, dev, "portal-repair")
        close_all(pg)
        portal(pg, lang, "s")
        pg.fill("#nlrm-signform [name='name']", "דנה כהן" if lang == "he" else "Daniel Brooks")
        to_top(pg, "#nlrm-pad")
        box = pg.locator("#nlrm-pad").bounding_box()
        pg.mouse.move(box["x"] + SIG[0][0] * box["width"] / 400, box["y"] + SIG[0][1] * box["height"] / 180)
        pg.mouse.down()
        for x, y in SIG[1:]:
            pg.mouse.move(box["x"] + x * box["width"] / 400, box["y"] + y * box["height"] / 180, steps=6)
        pg.mouse.up()
        pg.check("#nlrm-signform [name='agree']")
        pg.evaluate("window.scrollBy(0, -170)")
        shot(pg, lang, dev, "portal-sign")
        to_top(pg, ".nlrm-leasedoc")
        pg.evaluate("window.scrollBy(0, -120)")
        shot(pg, lang, dev, "portal-lease")
        portal(pg, lang, "v")
        shot(pg, lang, dev, "portal-vendor")
        portal(pg, lang, "a")
        shot(pg, lang, dev, "portal-apply")
        portal(pg, lang, "q")
        shot(pg, lang, dev, "portal-quick")

        check("%s console errors" % lang, not errs, errs[:3])
        results["errors"] += errs
        ctx.close()

        # --- desktop: the appliances list, the printable lease and the yearly summary
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL" if lang == "he" else "en-GB")
        pg = ctx.new_page()
        dev = "desk"
        app(pg, lang)
        pg.evaluate("NLRM.open('unit', %d)" % (11 if lang == "he" else 31))  # the lease prints in the TENANT's language
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
        pg.click(".nlrm-ptabs [data-tab='home']"); pg.wait_for_timeout(2500)
        to_top(pg, ".nlrm-layer.is-in #nlrm-asset-a1")
        pg.evaluate("document.querySelector('.nlrm-layer.is-in .nlrm-pbody').scrollBy(0, -90)")
        shot(pg, lang, dev, "assets")
        pg.click(".nlrm-ptabs [data-tab='lease']"); pg.wait_for_timeout(400)
        with ctx.expect_page() as pop:
            pg.click(".nlrm-layer.is-in [data-act='lease-doc']")
        doc = pop.value
        doc.set_viewport_size({"width": 1000, "height": 900})
        doc.wait_for_load_state(); doc.wait_for_timeout(800)
        doc.screenshot(path=str(OUT / ("%s-desk-lease-doc.png" % lang)))
        check("%s printable lease opens" % lang, doc.locator("h1").count() >= 1, doc.locator("h1").first.inner_text()[:60])
        doc.close()
        close_all(pg)
        # the floor card: building -> floor (its apartments, rent, debt and open repairs)
        app(pg, lang, "#/property/1")
        pg.wait_for_timeout(3000)
        pg.click("[data-act='floor'][data-floor='3']")
        pg.wait_for_selector(".nlrm-layer.is-in .nlrm-kpis", timeout=5000)
        shot(pg, lang, dev, "floor-card")
        close_all(pg)
        app(pg, lang, "#/reports")
        with ctx.expect_page() as pop:
            pg.click("[data-act='rep-year']")
        doc = pop.value
        doc.set_viewport_size({"width": 1000, "height": 900})
        doc.wait_for_load_state(); doc.wait_for_timeout(800)
        doc.screenshot(path=str(OUT / ("%s-desk-rep-year.png" % lang)))
        doc.close()
        ctx.close()
    b.close()
json.dump(results, open(OUT / "results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
fails = [c for c in results["checks"] if not c["ok"]]
print("\n%d checks, %d failed" % (len(results["checks"]), len(fails)))
sys.exit(1 if fails else 0)
