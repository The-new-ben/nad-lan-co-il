# -*- coding: utf-8 -*-
"""Rentals slice 1 (HAD-795): presses the four jobs of the "Today" screen and COUNTS presses by the rule of
docs/rentals/bom/compare/TEN-JOBS.md (every press on the screen counts; typing and scrolling do not; the phone's own camera
counts 2: the shutter and "use photo"; a file chooser stands for it, the file is given with set_files).
  what is waiting ......... 0     repair with a photo ... ours 1 + camera 2 = 3
  index update saved ...... 2     rent received ......... 1
Also: every visible button of the layer >= 44 px, the main card's actions and the camera row between 35% and 98% of the
viewport height, no horizontal scroll, he and en, 390x844 touch phone and 1440x900. Headless Edge, NOT a real phone.
The sample's dates are pinned with the browser clock so each state of the main card can be pressed.
Usage: python scripts/rentals/lab_slice1.py [base_url]   (server at the repo root: python -m http.server 47921)"""
import sys, json, pathlib, base64, datetime
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47921/docs/design-lab/rentals/app.html"
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/rentals/build/slice1/shots"
OUT.mkdir(parents=True, exist_ok=True)
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
results = {"checks": [], "presses": {}, "errors": []}
CLOCK = {"urgent": datetime.datetime(2026, 11, 10, 9, 0), "soon": datetime.datetime(2026, 11, 20, 9, 0), "index": datetime.datetime(2026, 11, 26, 9, 0), "quiet": datetime.datetime(2026, 11, 10, 9, 0)}


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:240]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:150] if info != "" else ""))


class Presses:
    """one count per job: pg.press() is a press of ours, camera() adds the phone's two"""
    def __init__(self, pg):
        self.pg, self.ours, self.cam = pg, 0, 0

    def press(self, sel):
        self.pg.click(sel); self.ours += 1

    def camera(self, sel):
        with self.pg.expect_file_chooser() as fc:
            self.pg.click(sel)
        self.ours += 1
        fc.value.set_files({"name": "fault.png", "mimeType": "image/png", "buffer": PNG})
        self.cam += 2

    @property
    def total(self):
        return self.ours + self.cam


def open_page(b, lang, dev, scene, unit, route="today"):
    vp = {"width": 1440, "height": 900} if dev == "desk" else {"width": 390, "height": 844}
    ctx = b.new_context(viewport=vp, device_scale_factor=2 if dev == "phone" else 1, is_mobile=(dev == "phone"), has_touch=(dev == "phone"), locale="he-IL" if lang == "he" else "en-GB")
    ctx.clock.set_fixed_time(CLOCK[scene])
    pg = ctx.new_page()
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "404" not in m.text and "net::" not in m.text else None)
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    pg.goto("%s?slice=1&scene=%s&lang=%s#/%s/%s" % (BASE, scene, lang, route, unit), wait_until="networkidle")
    pg.wait_for_selector("#nt2:not([hidden]) .nt2-app > *", timeout=10000)
    pg.wait_for_timeout(400)
    return ctx, pg, errs


def shot(pg, name):
    pg.screenshot(path=str(OUT / (name + ".png")))


def geometry(pg, tag, H):
    """buttons >= 44, card actions + camera row inside 35%..98% of the viewport height, no horizontal scroll"""
    info = pg.evaluate("""() => {
      const host = document.querySelector('#nt2'); const vis = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
      const small = [], all = [];
      host.querySelectorAll('button, a[href]').forEach(e => { if (!vis(e)) return; const r = e.getBoundingClientRect(); all.push(1); if (r.height < 43.5 || r.width < 43.5) small.push((e.dataset.act || e.dataset.part || e.className || e.tagName) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height)); });
      const zone = []; host.querySelectorAll('.nt2-card button, .nt2-cam button, .nt2-next button:not(.nt2-round)').forEach(e => { if (!vis(e)) return; const r = e.getBoundingClientRect(); zone.push([e.dataset.act, r.top / innerHeight, r.bottom / innerHeight]); });
      const body = document.querySelector('#nt2-body');
      return { small, n: all.length, zone, hscroll: document.documentElement.scrollWidth > innerWidth + 1 || body.scrollWidth > body.clientWidth + 1 };
    }""")
    check("%s every visible button >= 44 px (%d buttons)" % (tag, info["n"]), not info["small"], info["small"])
    bad = [z for z in info["zone"] if z[1] < 0.35 or z[2] > 0.98]
    check("%s card actions + camera row between 35%% and 98%% of the height (%d)" % (tag, len(info["zone"])), info["zone"] and not bad, bad or ["%s %.0f%%-%.0f%%" % (z[0], z[1] * 100, z[2] * 100) for z in info["zone"]])
    check("%s no horizontal scroll" % tag, not info["hscroll"])
    return info


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for lang in ("he", "en"):
        for dev in ("phone", "desk"):
            tag0 = "%s %s" % (lang, dev)
            H = 900 if dev == "desk" else 844

            # ---- what is waiting: 0 presses (urgent state, the open boiler fault of Apt 7 in building 2)
            ctx, pg, errs = open_page(b, lang, dev, "urgent", 21)
            pr = Presses(pg)
            say = pg.inner_text(".nt2-say"); card = pg.inner_text(".nt2-card")
            check("%s what is waiting is on screen with 0 presses" % tag0, len(say) > 8 and pr.total == 0, say)
            results["presses"][tag0 + " waiting"] = pr.total
            check("%s urgent card: deadline bar, two actions, no dash characters" % tag0, pg.locator(".nt2-bar").count() == 1 and pg.locator(".nt2-card .nt2-btns button").count() == 2 and "—" not in card and "–" not in card)
            check("%s no raw string keys on screen" % tag0, "t2_" not in pg.inner_text("#nt2"))
            check("%s direction/lang follow the language" % tag0, pg.get_attribute("#nt2", "dir") == ("rtl" if lang == "he" else "ltr") and pg.get_attribute("#nt2", "lang") == lang)
            legal = pg.inner_text(".nt2-law") if pg.locator(".nt2-law").count() else ""
            if lang == "he":
                check("%s legal sentences exactly as given, source named (building system)" % tag0, "ליקוי שאינו קל ערך: המשכיר מתקן על חשבונו." in legal and "ליקוי משימוש בלתי סביר בדירה: על השוכר, אלא אם סיכמתם אחרת." in legal and "חוק השכירות והשאילה, סעיף 25ח" in legal, legal)
            else:
                check("%s legal sentences present (building system)" % tag0, "not minor" in legal and "unreasonable use" in legal and "25H" in legal, legal)
            shot(pg, "%s-%s-1-urgent" % (lang, dev))
            geometry(pg, tag0 + " urgent", H)

            # ---- repair with a photo: ours 1 + camera 2 = 3, one request, shown in "done recently"
            n0 = pg.evaluate("NLRM.store.d.tickets.length"); d0 = pg.evaluate("NLRM.store.d.docs.length")
            pg.evaluate("(() => { const a = NLRM.store.adapter, r = a.save; window.__repairCalls = 0; a.save = function (e) { if (e === 'ticket') { window.__repairCalls++; } return r.apply(a, arguments); }; })()")  # the product's own sample path (1.72.725): one ticket write
            pr = Presses(pg)
            pr.camera("#nt2 [data-act='cam-repair']")
            pg.wait_for_function("NLRM.store.d.tickets.length === %d" % (n0 + 1), timeout=6000)
            pg.wait_for_timeout(300)
            check("%s repair with a photo: ours 1, camera 2, total 3" % tag0, pr.ours == 1 and pr.cam == 2 and pr.total == 3, "ours %d camera %d" % (pr.ours, pr.cam))
            results["presses"][tag0 + " repair+photo"] = {"ours": pr.ours, "camera": pr.cam, "total": pr.total}
            tk = pg.evaluate("NLRM.store.d.tickets.slice(-1)[0]")
            check("%s repair saved with no form: one request, ticket + photo, no sheet opened" % tag0, pg.evaluate("window.__repairCalls") == 1 and tk["meta"]["via"] == "today-camera" and pg.evaluate("NLRM.store.d.docs.length") == d0 + 1 and pg.locator(".nt2-sw").count() == 0)
            check("%s the new repair shows in 'done recently'" % tag0, ("תקלה חדשה, עם תמונה" if lang == "he" else "New fault, with a photo") in pg.inner_text(".nt2-recent"), pg.inner_text(".nt2-recent")[:120])
            shot(pg, "%s-%s-2-repair-saved" % (lang, dev))
            results["errors"] += errs; ctx.close()

            # ---- the drawing sheet: parts are real buttons at scale 1
            ctx, pg, errs = open_page(b, lang, dev, "urgent", 21)
            pg.click("#nt2 [data-act='drawing']"); pg.wait_for_selector(".nt2-sw.is-in .np2-part")
            parts = pg.evaluate("[...document.querySelectorAll('.nt2-sw .np2-part')].map(e => { const r = e.getBoundingClientRect(); return [e.tagName, Math.round(r.width), Math.round(r.height)]; })")
            check("%s drawing sheet: %d parts, each a <button> of at least 44 px" % (tag0, len(parts)), len(parts) >= 4 and all(x[0] == "BUTTON" and x[1] >= 44 and x[2] >= 44 for x in parts), parts[:3])
            ov = pg.evaluate("""() => { const hit = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top; const tiles = [...document.querySelectorAll('.nt2-sw .np2-part, .nt2-sw .np2-tag')].map(e => e.getBoundingClientRect()); return [...document.querySelectorAll('.nt2-sw .np2-rl')].filter(l => tiles.some(t => hit(l.getBoundingClientRect(), t))).map(l => l.textContent); }""")
            check("%s no room name sits under a tile or a state tag in the drawing" % tag0, not ov, ov)
            st = pg.evaluate("[...document.querySelectorAll('.nt2-sw .np2-tag')].map(e => e.textContent)")
            pg.wait_for_timeout(450); shot(pg, "%s-%s-3-drawing" % (lang, dev))
            results["errors"] += errs; ctx.close()

            # ---- no plan: the row of icons and the link to add a plan (unit 31 of building 3)
            ctx, pg, errs = open_page(b, lang, dev, "urgent", 31)
            check("%s no plan: a row of the parts' icons and the 'add a plan' link, no made-up floor" % tag0, pg.locator(".np2--row .np2-part").count() >= 4 and pg.locator(".np2-add").count() == 1 and pg.locator(".np2-room").count() == 0)
            shot(pg, "%s-%s-4-noplan" % (lang, dev))
            geometry(pg, tag0 + " no-plan", H)
            results["errors"] += errs; ctx.close()

            # ---- index update that saves: 2 presses
            ctx, pg, errs = open_page(b, lang, dev, "index", 11)
            check("%s due-soon card: rent + index rows" % tag0, pg.locator(".nt2-card [data-act='rent']").count() == 1 and pg.locator(".nt2-card [data-act='index']").count() == 1)
            check("%s due-soon card title is the renamed one; no 'coming soon' wording anywhere on the screen" % tag0, pg.inner_text(".nt2-card .nt2-card-k") == ("בימים הקרובים" if lang == "he" else "In the next days") and "בקרוב" not in pg.inner_text("#nt2"), pg.inner_text(".nt2-card .nt2-card-k"))
            shot(pg, "%s-%s-5-soon" % (lang, dev)); geometry(pg, tag0 + " soon", H)
            pr = Presses(pg)
            pr.press("#nt2 [data-act='index']")
            pg.wait_for_selector("#nt2 [data-act='idx-save']", timeout=6000)
            kv = pg.evaluate("[...document.querySelectorAll('.nt2-kv > div')].map(d => d.innerText.replace(/\\s+/g, ' '))")
            check("%s index sheet shows today's rent, base index, latest index, new rent" % tag0, len(kv) == 4, kv)
            pg.wait_for_timeout(450); shot(pg, "%s-%s-6-index-sheet" % (lang, dev))
            small = pg.evaluate("[...document.querySelectorAll('.nt2-sw button')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.height < 43.5 || r.width < 43.5); }).length")
            check("%s index sheet buttons >= 44 px" % tag0, small == 0, small)
            nl = pg.evaluate("NLRM.store.d.ledger.length"); ne = pg.evaluate("NLRM.store.d.events.length")
            pr.press("#nt2 [data-act='idx-save']")
            pg.wait_for_function("NLRM.store.d.events.some(e => e.type === 'index_confirmed')", timeout=6000)
            pg.wait_for_timeout(500)
            ev = pg.evaluate("NLRM.store.d.events.filter(e => e.type === 'index_confirmed')[0]")
            msg = pg.inner_text(".nt2-sw .nt2-ok") if pg.locator(".nt2-sw .nt2-ok").count() else ""
            want = ("אושר: שכר הדירה מ-" if lang == "he" else "Confirmed: the rent from ")
            check("%s index confirmed in 2 presses, as a journal event (no ledger line)" % tag0, pr.ours == 2 and pr.total == 2 and ev and ev["scope"] == "lease" and ev["meta"]["base_index"] == 100 and ev["meta"]["old_amount"] == 780000 and ev["meta"]["new_amount"] == 809600 and ev["meta"]["client_ref"] and pg.evaluate("NLRM.store.d.ledger.length") == nl and pg.evaluate("NLRM.store.d.events.length") == ne + 1, "presses %d, %s" % (pr.total, ev and ev["meta"]))
            check("%s the sheet says what is true: confirmed, month, amount, recorded in the journal" % tag0, msg.startswith(want) and ("נרשם ביומן הדירה." if lang == "he" else "Recorded in the apartment's journal.") in msg and ("8,096" in msg), msg)
            pg.wait_for_timeout(300); shot(pg, "%s-%s-7-index-confirmed-sheet" % (lang, dev))
            pg.click(".nt2-sw [data-close]"); pg.wait_for_timeout(350)
            card = pg.inner_text(".nt2-card")
            check("%s the card says it too, the index row is gone, and it shows in 'done recently'" % tag0, pg.locator(".nt2-card [data-act='index']").count() == 0 and "8,096" in card and msg.split(".")[0] in card and ("שכר הדירה החדש אושר" if lang == "he" else "The new rent was confirmed") in pg.inner_text(".nt2-recent"), card[:120].replace(chr(10), " "))
            lp = pg.evaluate("NLRM.store.d.leases.find(l => l.id === 201).linkage.mode"); check("%s the lease and the books are untouched (linkage stays, no new ledger row)" % tag0, lp == "cpi" and pg.evaluate("NLRM.store.d.ledger.length") == nl)
            results["presses"][tag0 + " index"] = pr.total
            shot(pg, "%s-%s-7-index-card" % (lang, dev))
            results["errors"] += errs; ctx.close()

            # ---- rent received: 1 press (a transfer tenant: Apt 14, unit 12), then the tenancy axis
            ctx, pg, errs = open_page(b, lang, dev, "soon", 12)
            r0 = pg.evaluate("NLRM.store.d.ledger.filter(r => r.lease_id === 202 && r.kind === 'payment').length")
            pr = Presses(pg)
            pr.press("#nt2 [data-act='rent']")
            pg.wait_for_function("NLRM.store.d.ledger.filter(r => r.lease_id === 202 && r.kind === 'payment').length === %d" % (r0 + 1), timeout=6000)
            pg.wait_for_timeout(400)
            pay = pg.evaluate("NLRM.store.d.ledger.filter(r => r.lease_id === 202 && r.kind === 'payment').slice(-1)[0]")
            check("%s rent received in 1 press: the expected amount, today's date, no form" % tag0, pr.total == 1 and pay["amount"] == 640000 and pay["paid_date"] == "2026-11-20" and pay["status"] == "paid" and pg.locator(".nt2-sw").count() == 0, "presses %d, %s %s" % (pr.total, pay["amount"], pay["paid_date"]))
            check("%s the rent row is gone and it shows in 'done recently'" % tag0, pg.locator(".nt2-card [data-act='rent']").count() == 0 and ("שכר דירה לנובמבר התקבל" if lang == "he" else "Rent for November received") in pg.inner_text(".nt2-recent"), pg.inner_text(".nt2-recent")[:100])
            results["presses"][tag0 + " rent"] = pr.total
            shot(pg, "%s-%s-8-rent-received" % (lang, dev))
            results["errors"] += errs; ctx.close()

            ctx, pg, errs = open_page(b, lang, dev, "soon", 12, route="rent")
            check("%s tenancy axis: twelve month buttons, each 44 px or more" % tag0, pg.evaluate("[...document.querySelectorAll('.nt2-mo')].filter(e => { const r = e.getBoundingClientRect(); return r.height >= 43.5 && r.width >= 43.5; }).length") == 12)
            check("%s next-due sheet is on screen with 0 presses and has the 'received' button" % tag0, pg.locator(".nt2-next [data-act='rent']").count() == 1)
            geometry(pg, tag0 + " axis", H)
            shot(pg, "%s-%s-9-axis" % (lang, dev))
            paid0 = pg.locator(".nt2-mo.is-paid").count()
            pr = Presses(pg)
            pr.press(".nt2-next [data-act='rent']")
            pg.wait_for_function("document.querySelectorAll('.nt2-mo.is-paid').length > %d" % paid0, timeout=6000)
            pg.wait_for_timeout(300)
            check("%s axis: one press marks the month paid on the ruler" % tag0, pr.total == 1 and pg.locator(".nt2-next [data-act='rent']").count() == 0)
            shot(pg, "%s-%s-10-axis-paid" % (lang, dev))
            results["errors"] += errs; ctx.close()

            # ---- quiet day: the earned fact is computed from the ledger, not written
            ctx, pg, errs = open_page(b, lang, dev, "quiet", 11)
            tx = pg.inner_text(".nt2-card")
            data = pg.evaluate("(() => { const m = NLRM.today2.model(); return { state: m.state, year: m.earned.year, streak: m.earned.streak }; })()")
            check("%s quiet state: year total and on-time streak computed (%s)" % (tag0, data), data["state"] == "quiet" and data["year"] > 0 and data["streak"] >= 2 and pg.locator(".nt2-earn").count() == 1, tx[:80].replace("\n", " "))
            shot(pg, "%s-%s-11-quiet" % (lang, dev)); geometry(pg, tag0 + " quiet", H)
            results["errors"] += errs; ctx.close()
    b.close()

results["errors"] = [e for e in results["errors"] if e]
check("no console or page errors in any run", not results["errors"], results["errors"][:3])
ok = sum(1 for c in results["checks"] if c["ok"]); tot = len(results["checks"])
print("\nRESULT %d/%d checks passed" % (ok, tot))
results["summary"] = {"passed": ok, "total": tot}
(ROOT / "docs/rentals/build/slice1/lab-slice1-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf8")
sys.exit(0 if ok == tot else 1)
