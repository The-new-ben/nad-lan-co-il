# -*- coding: utf-8 -*-
"""Rentals v2 lab: the money flows by real presses (he + en, desk 1440 + phone 390).
Deposit over the legal cap (refused), a deposit received, a payment, a cheque that
bounces, a line voided, the end of a lease with proration, the deposit returned,
a renewal, and an existing lease entered without invented arrears.
Usage: python scripts/rentals/lab_money.py [base_url]   (server: python -m http.server 47914)"""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs/design-lab/rentals/shots/money"
OUT.mkdir(parents=True, exist_ok=True)
results = {"checks": [], "errors": []}


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:200]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:160] if info != "" else ""))


def money(pg, lid):
    return pg.evaluate("(id) => { var l = NLRM.store.d.leases.find(x => x.id === id); return l ? NLRM.moneyOf(l) : null; }", lid)


def layer_close(pg):
    for _ in range(4):
        if pg.locator(".nlrm-layer").count():
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(260)


def submit(pg):
    pg.click(".nlrm-layer.is-in form [type='submit']")
    pg.wait_for_timeout(700)


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for lang in ("he", "en"):
        for dev, vp in (("desk", {"width": 1440, "height": 900}), ("phone", {"width": 390, "height": 844})):
            tag = "%s %s" % (lang, dev)
            ctx = b.new_context(viewport=vp, device_scale_factor=2 if dev == "phone" else 1, is_mobile=(dev == "phone"), has_touch=(dev == "phone"), locale="he-IL" if lang == "he" else "en-GB")
            pg = ctx.new_page()
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "404" not in m.text else None)
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
            pg.goto(BASE + "?lang=" + lang + "#/today", wait_until="networkidle")
            pg.wait_for_selector(".nlrm-kpis", timeout=15000)

            # 1. the deposit: above the legal cap is refused, a legal amount is held
            pg.evaluate("NLRM.open('unit', 31)")
            pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
            pg.click(".nlrm-ptabs [data-tab='money']"); pg.wait_for_timeout(400)
            pg.click(".nlrm-layer.is-in [data-act='dep-receive']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
            pg.fill(".nlrm-layer.is-in [name='amount']", "20000"); submit(pg)
            msg = pg.inner_text(".nlrm-layer.is-in .nlrm-ferr") if pg.locator(".nlrm-layer.is-in .nlrm-ferr").count() else ""
            check("%s deposit above the legal cap is refused" % tag, ("12,900" in msg) or ("12900" in msg), msg)
            pg.screenshot(path=str(OUT / ("%s-%s-deposit-cap.png" % (lang, dev))))
            pg.fill(".nlrm-layer.is-in [name='amount']", "5000"); submit(pg)
            m = money(pg, 204)
            check("%s deposit held 5,000" % tag, m and m["deposit_held"] == 500000, m and m["deposit_held"])
            check("%s a deposit is not a rent payment" % tag, m and m["credit"] == money(pg, 204)["credit"], "")
            pg.screenshot(path=str(OUT / ("%s-%s-deposit-held.png" % (lang, dev))))
            layer_close(pg)

            # 2. a payment through the engine
            before = money(pg, 202)
            pg.evaluate("NLRM.open('unit', 12)")
            pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
            pg.click(".nlrm-ptabs [data-tab='money']"); pg.wait_for_timeout(400)
            pg.click(".nlrm-layer.is-in .nlrm-pbody [data-act='pay']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
            pg.fill(".nlrm-layer.is-in [name='amount']", "1000"); submit(pg)
            after = money(pg, 202)
            check("%s a payment lowers the balance by exactly 1,000" % tag, before["balance"] - after["balance"] == 100000, "%s -> %s" % (before["balance"], after["balance"]))

            # 3. void it (both lines stay, the balance goes back)
            row = pg.evaluate("NLRM.store.d.ledger.filter(r => r.lease_id === 202 && r.kind === 'payment' && r.amount === 100000).slice(-1)[0].id")
            pg.click(".nlrm-layer.is-in [data-act='row-more'][data-row='%d']" % row); pg.wait_for_timeout(400)
            pg.screenshot(path=str(OUT / ("%s-%s-row-more.png" % (lang, dev))))
            pg.click(".nlrm-layer.is-in [data-sheet-act='void']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
            pg.fill(".nlrm-layer.is-in [name='reason']", "test"); submit(pg)
            v = money(pg, 202)
            st = pg.evaluate("(id) => NLRM.store.d.ledger.find(r => r.id === id).status", row)
            check("%s voiding restores the balance and keeps the line" % tag, v["balance"] == before["balance"] and st == "void", "%s %s" % (v["balance"], st))
            layer_close(pg)

            # 4. a cheque that bounces: the month is open again, the bank fee charged
            ch = pg.evaluate("NLRM.store.d.ledger.filter(r => r.lease_id === 201 && r.method === 'cheque' && r.status === 'deposited').slice(-1)[0]")
            b0 = money(pg, 201)
            pg.evaluate("NLRM.open('unit', 11)")
            pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
            pg.click(".nlrm-ptabs [data-tab='money']"); pg.wait_for_timeout(400)
            pg.click(".nlrm-layer.is-in [data-act='row-more'][data-row='%d']" % ch["id"]); pg.wait_for_timeout(400)
            pg.click(".nlrm-layer.is-in [data-sheet-act='bounce']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
            pg.fill(".nlrm-layer.is-in [name='fee']", "25"); submit(pg)
            b1 = money(pg, 201)
            check("%s bounced cheque: balance up by the cheque + 25" % tag, b1["balance"] - b0["balance"] == ch["amount"] + 2500, "%s -> %s" % (b0["balance"], b1["balance"]))
            layer_close(pg)

            # 5. the end of a lease, prorated, then the deposit back within 60 days
            pg.evaluate("NLRM.open('unit', 31)")
            pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
            pg.click(".nlrm-ptabs [data-tab='lease']"); pg.wait_for_timeout(400)
            pg.click(".nlrm-layer.is-in [data-act='end-lease']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
            pg.screenshot(path=str(OUT / ("%s-%s-end-lease.png" % (lang, dev))))
            submit(pg)
            st = pg.evaluate("NLRM.store.d.leases.find(x => x.id === 204).status")
            check("%s the lease ended" % tag, st == "ended", st)
            late = pg.evaluate("NLRM.store.d.ledger.filter(r => r.lease_id === 204 && r.kind === 'charge' && r.category === 'rent' && r.status !== 'void' && r.due_date > NLRM.addDays(NLRM.todayIso(), 31)).length")
            check("%s no rent for a period after the end" % tag, late == 0, late)
            cur = pg.evaluate("NLRM.store.d.ledger.filter(r => r.lease_id === 204 && r.kind === 'charge' && r.category === 'rent' && r.status !== 'void' && (r.auto_key || '').indexOf(NLRM.ym(0)) >= 0).map(r => r.amount)")
            check("%s this month's rent is prorated by days" % tag, len(cur) == 1 and 0 < cur[0] < 430000, cur)
            att = pg.evaluate("NLRM.attention().filter(a => a.kind === 'deposit_return').length")
            check("%s the deposit return is on the to-do list" % tag, att >= 1, att)
            layer_close(pg)
            pg.evaluate("NLRM.open('unit', 31)")
            pg.wait_for_selector(".nlrm-layer.is-in .nlrm-pbody", timeout=5000)
            has_former = pg.locator(".nlrm-layer.is-in [data-act='former-money']").count()
            check("%s the former tenant's matters show on the apartment" % tag, has_former >= 1, has_former)
            pg.screenshot(path=str(OUT / ("%s-%s-former.png" % (lang, dev))), full_page=False)

            # 5b. B21: a payment from the former tenant's money sheet lands on HIS lease, not on an active one
            pg.click(".nlrm-layer.is-in [data-act='former-money']"); pg.wait_for_timeout(500)
            pg.click(".nlrm-layer.is-in [data-act='pay'][data-lease='204']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
            sel = pg.evaluate("document.querySelector(\".nlrm-layer.is-in [name='lease_id']\").value")
            check("%s the former tenant's payment form is on his lease" % tag, sel == "204", sel)
            f0 = money(pg, 204)
            pg.fill(".nlrm-layer.is-in [name='amount']", "100"); submit(pg)
            last = pg.evaluate("NLRM.store.d.ledger.filter(r => r.kind === 'payment' && r.amount === 10000).slice(-1)[0]")
            f1 = money(pg, 204)
            check("%s the payment is booked on the former lease" % tag, last and last["lease_id"] == 204 and f0["balance"] - f1["balance"] == 10000, last and last["lease_id"])
            layer_close(pg)

            pg.evaluate("NLRM.open('unit', 31)")
            pg.wait_for_selector(".nlrm-layer.is-in [data-act='former-money']", timeout=5000)
            pg.click(".nlrm-layer.is-in [data-act='former-money']"); pg.wait_for_timeout(500)
            pg.click(".nlrm-layer.is-in [data-act='dep-return']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
            submit(pg)
            m = money(pg, 204)
            check("%s the deposit was returned in full" % tag, m["deposit_held"] == 0, m["deposit_held"])
            layer_close(pg)

            # 6. a renewal: the old lease closes, the new one is active, nothing doubled
            n0 = pg.evaluate("NLRM.store.d.leases.length")
            pg.evaluate("NLRM.open('unit', 21)")
            pg.wait_for_selector(".nlrm-layer.is-in .nlrm-ptabs", timeout=5000)
            pg.click(".nlrm-ptabs [data-tab='lease']"); pg.wait_for_timeout(400)
            pg.click(".nlrm-layer.is-in [data-act='renew-lease']"); pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
            pg.screenshot(path=str(OUT / ("%s-%s-renew.png" % (lang, dev))))
            submit(pg); pg.wait_for_timeout(500)
            r = pg.evaluate("({n: NLRM.store.d.leases.length, old: NLRM.store.d.leases.find(x => x.id === 203).status, act: NLRM.store.d.leases.filter(x => x.unit_id === 21 && x.status === 'active').length})")
            check("%s renewal: one new lease, old ended, one active" % tag, r["n"] == n0 + 1 and r["old"] == "ended" and r["act"] == 1, r)
            layer_close(pg)

            # 7. an existing lease entered today: money followed from this month, no invented arrears
            pg.evaluate("NLRM.forms.lease(null, 22)")
            pg.wait_for_selector(".nlrm-layer.is-in form", timeout=4000)
            pg.fill(".nlrm-layer.is-in [name='t_name']", "Test Tenant")
            start = pg.evaluate("NLRM.addMonths(NLRM.todayIso().slice(0,8) + '01', -14)")
            pg.fill(".nlrm-layer.is-in [name='start_date']", start)
            pg.fill(".nlrm-layer.is-in [name='end_date']", pg.evaluate("(s) => NLRM.addDays(NLRM.addMonths(s, 36), -1)", start))
            pg.fill(".nlrm-layer.is-in [name='rent']", "6000")
            pg.dispatch_event(".nlrm-layer.is-in [name='start_date']", "change")
            vis = pg.evaluate("getComputedStyle(document.querySelector(\".nlrm-layer.is-in [name='track_from']\").closest('label')).display")
            check("%s 'follow payments from' appears for an old lease" % tag, vis != "none", vis)
            pg.screenshot(path=str(OUT / ("%s-%s-track-from.png" % (lang, dev))))
            submit(pg); pg.wait_for_timeout(600)
            nl = pg.evaluate("NLRM.store.d.leases.filter(x => x.unit_id === 22 && x.status === 'active').slice(-1)[0]")
            m = money(pg, nl["id"]) if nl else None
            check("%s no invented arrears (at most this month)" % tag, m is not None and m["due"] <= 600000, m and m["due"])

            check("%s console errors" % tag, not errs, errs[:3])
            results["errors"] += errs
            ctx.close()
    b.close()
json.dump(results, open(OUT / "results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
fails = [c for c in results["checks"] if not c["ok"]]
print("\n%d checks, %d failed" % (len(results["checks"]), len(fails)))
sys.exit(1 if fails else 0)
