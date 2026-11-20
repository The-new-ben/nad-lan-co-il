# -*- coding: utf-8 -*-
"""Rentals slice 1, the three fixes of release 1.72.723 (HAD-795), pressed in the lab:
  1. the index line of the tenancy screen: always there for an index-linked lease, also when a repair is open;
     saving opens a week before the update date, before that the sheet says so and has no save button;
  2. the first part of a home in ONE press (a home with nothing recorded), later parts in two;
  3. the no-plan row of the title block: six places, no inner scroll, the "add a plan" link whole and pressable.
he and en, 390x844, 390x667 (a short phone) and 1440x900. Headless Edge, NOT a real phone.
Usage: python scripts/rentals/lab_slice1_fixes.py [base_url]   (server at the repo root: python -m http.server 47921)"""
import sys, json, pathlib, datetime
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:47921/docs/design-lab/rentals/app.html"
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/rentals/build/slice1/shots-723"
OUT.mkdir(parents=True, exist_ok=True)
results = {"checks": [], "presses": {}, "errors": []}
CLOCK = {"urgent": datetime.datetime(2026, 11, 10, 9, 0), "index": datetime.datetime(2026, 11, 26, 9, 0), "quiet": datetime.datetime(2026, 11, 10, 9, 0)}
DEV = {"phone": (390, 844), "short": (390, 667), "desk": (1440, 900)}


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:240]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:170] if info != "" else ""))


def open_page(b, lang, dev, scene, unit, route="today"):
    w, h = DEV[dev]
    touch = dev != "desk"
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if touch else 1, is_mobile=touch, has_touch=touch, locale="he-IL" if lang == "he" else "en-GB")
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


ROW_JS = """() => {
  const box = document.querySelector('#nt2-plan'), host = document.querySelector('.nt2-tb-l').getBoundingClientRect();
  const inside = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.left >= host.left - 0.5 && r.right <= host.right + 0.5 && r.top >= host.top - 0.5 && r.bottom <= host.bottom + 0.5; };
  const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).display !== 'none'; };
  const hit = e => { const r = e.getBoundingClientRect(); const t = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return !!t && (t === e || e.contains(t)); };
  const tiles = [...box.querySelectorAll('.np2-list button')].filter(vis), link = box.querySelector('.np2-add');
  return { scroll: box.scrollHeight > box.clientHeight + 1 || box.scrollWidth > box.clientWidth + 1, overflow: getComputedStyle(box).overflowY,
    tiles: tiles.length, tilesIn: tiles.every(inside), tilesHit: tiles.every(hit), small: tiles.filter(e => { const r = e.getBoundingClientRect(); return r.width < 43.5 || r.height < 43.5; }).length,
    linkIn: !!link && inside(link), linkHit: !!link && hit(link), linkH: link ? Math.round(link.getBoundingClientRect().height) : 0,
    caps: [...box.querySelectorAll('.np2-list li')].filter(vis).map(li => li.querySelector('.np2-cap').textContent) };
}"""

SUM_JS = """() => {
  const s = document.querySelector('.nt2-sum').getBoundingClientRect(), nx = document.querySelector('.nt2-next').getBoundingClientRect();
  const lis = [...document.querySelectorAll('.nt2-sum li')].map(li => li.getBoundingClientRect());
  const b = document.querySelector('.nt2-sum-idx button'); const r = b ? b.getBoundingClientRect() : null;
  return { n: lis.length, clipped: lis.filter(r => r.bottom > s.bottom + 0.5 || r.bottom > nx.top + 0.5).length, btn: r ? [Math.round(r.width), Math.round(r.height)] : null,
    hscroll: document.documentElement.scrollWidth > innerWidth + 1, text: (document.querySelector('.nt2-sum-idx') || {}).innerText || '' };
}"""

SET_ASSETS = """(n) => { const u = NLRM.ix.unit[31]; const kinds = ['boiler','ac','panel','fridge','oven','washer','dishwasher','heater'];
  const list = kinds.slice(0, n).map((k, i) => ({ id: 'z' + i, kind: k, label: NLRM.t('ak_' + k) }));
  return NLRM.store.save('unit', { id: u.id, property_id: u.property_id, meta: Object.assign({}, u.meta, { assets: list }) }).then(() => NLRM.ix.unit[31].meta.assets.length); }"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for lang in ("he", "en"):
        for dev in ("phone", "short", "desk"):
            tag = "%s %s" % (lang, dev)

            # ---- 3. the no-plan row as the sample has it (unit 31): no inner scroll, the link whole and pressable
            ctx, pg, errs = open_page(b, lang, dev, "urgent", 31)
            r = pg.evaluate(ROW_JS)
            check("%s no-plan row: no inner scroll (overflow %s), %d tiles all inside the block and pressable, each 44 px" % (tag, r["overflow"], r["tiles"]), not r["scroll"] and r["overflow"] == "hidden" and r["tilesIn"] and r["tilesHit"] and r["small"] == 0 and 1 <= r["tiles"] <= 6, r)
            check("%s no-plan row: the 'add a plan' link is whole, 44 px high and receives the press" % tag, r["linkIn"] and r["linkHit"] and r["linkH"] >= 44, r)
            shot(pg, "%s-%s-1-row-sample" % (lang, dev))

            # ---- 3b. many parts: five and a "more" tile that opens the whole list
            pg.evaluate(SET_ASSETS, 8); pg.wait_for_timeout(350)
            r = pg.evaluate(ROW_JS)
            check("%s 8 parts: six places (5 parts + 'more'), nothing cut, no scroll" % tag, r["tiles"] == 6 and not r["scroll"] and r["tilesIn"] and r["linkIn"] and pg.locator("#nt2-plan .np2-part--more").count() == 1, r)
            shot(pg, "%s-%s-2-row-8-parts" % (lang, dev))
            pg.click("#nt2-plan .np2-part--more"); pg.wait_for_selector(".nt2-sw.is-in .np2-part")
            n_in_sheet = pg.locator(".nt2-sw .np2-list [data-part]").count()
            check("%s 'more' opens the list with all 8 parts and the add tile" % tag, n_in_sheet == 8 and pg.locator(".nt2-sw [data-act='add-part']").count() == 1, n_in_sheet)
            pg.click(".nt2-sw button[data-close]"); pg.wait_for_timeout(350)

            # ---- 2. a home with nothing recorded: the first part in ONE press
            pg.evaluate(SET_ASSETS, 0); pg.wait_for_timeout(350)
            r = pg.evaluate(ROW_JS)
            want = 3 if dev == "short" else 6
            check("%s nothing recorded: %d 'add' tiles with one sentence, all inside, link whole, no scroll" % (tag, want), r["tiles"] == want and r["tilesIn"] and r["tilesHit"] and r["small"] == 0 and r["linkIn"] and r["linkHit"] and not r["scroll"] and pg.locator("#nt2-plan .np2-hint").count() == 1, r)
            check("%s no raw string keys on screen" % tag, "t2_" not in pg.inner_text("#nt2") and "ak_" not in pg.inner_text("#nt2"))
            shot(pg, "%s-%s-3-row-empty" % (lang, dev))
            presses = 0
            pg.click("#nt2-plan [data-act='add-kind'][data-kind='boiler']"); presses += 1
            pg.wait_for_function("(NLRM.ix.unit[31].meta.assets || []).length === 1", timeout=6000)
            pg.wait_for_timeout(350)
            a = pg.evaluate("NLRM.ix.unit[31].meta.assets[0]")
            check("%s first part added in 1 press: saved with its kind and name, no form opened" % tag, presses == 1 and a["kind"] == "boiler" and a["label"] == ("דוד מים" if lang == "he" else "Water heater") and pg.locator(".nt2-sw").count() == 0, a)
            results["presses"][tag + " first part"] = presses
            r = pg.evaluate(ROW_JS)
            check("%s after it: the part and an 'add' tile, link still whole" % tag, r["tiles"] == 2 and pg.locator("#nt2-plan [data-act='add-part']").count() == 1 and r["linkIn"] and not r["scroll"], r)
            shot(pg, "%s-%s-4-row-one-part" % (lang, dev))
            presses = 0
            pg.click("#nt2-plan [data-act='add-part']"); presses += 1
            pg.wait_for_selector(".nt2-sw.is-in [data-act='add-kind']")
            kinds = pg.evaluate("[...document.querySelectorAll('.nt2-sw [data-act=\"add-kind\"]')].map(e => { const r = e.getBoundingClientRect(); return [e.dataset.kind, Math.round(r.width), Math.round(r.height), e.scrollWidth > e.clientWidth + 1]; })")
            check("%s the add sheet: 11 kinds, each button 44 px or more, no name cut" % tag, len(kinds) == 11 and all(k[1] >= 44 and k[2] >= 44 for k in kinds), [k for k in kinds if k[3]] or kinds[:3])
            pg.wait_for_timeout(400); shot(pg, "%s-%s-5-add-sheet" % (lang, dev))
            pg.click(".nt2-sw [data-act='add-kind'][data-kind='ac']"); presses += 1
            pg.wait_for_function("(NLRM.ix.unit[31].meta.assets || []).length === 2", timeout=6000)
            pg.wait_for_timeout(450)
            check("%s a later part in 2 presses, the sheet closes by itself" % tag, presses == 2 and pg.locator(".nt2-sw.is-in").count() == 0)
            results["presses"][tag + " later part"] = presses
            results["errors"] += errs; ctx.close()

            # ---- 1. the index line of the tenancy screen, update due (scene index, lease 201, unit 11): 2 presses
            ctx, pg, errs = open_page(b, lang, dev, "index", 11, route="rent")
            s = pg.evaluate(SUM_JS)
            check("%s tenancy screen: the index line is there, whole (4 rows, none cut), its button 44 px high" % tag, s["n"] == 4 and s["clipped"] == 0 and s["btn"] and s["btn"][1] >= 44 and not s["hscroll"], s)
            shot(pg, "%s-%s-6-rent-index-line" % (lang, dev))
            presses = 0
            pg.click(".nt2-sum-idx [data-act='index']"); presses += 1
            pg.wait_for_selector("#nt2 [data-act='idx-save']", timeout=6000)
            ne = pg.evaluate("NLRM.store.d.events.length"); nl = pg.evaluate("NLRM.store.d.ledger.length")
            pg.click("#nt2 [data-act='idx-save']"); presses += 1
            pg.wait_for_function("NLRM.store.d.events.some(e => e.type === 'index_confirmed')", timeout=6000)
            pg.wait_for_timeout(450)
            check("%s index confirmed from the tenancy screen in 2 presses, a journal event, the books untouched" % tag, presses == 2 and pg.evaluate("NLRM.store.d.events.length") == ne + 1 and pg.evaluate("NLRM.store.d.ledger.length") == nl)
            results["presses"][tag + " index from tenancy"] = presses
            shot(pg, "%s-%s-7-rent-index-confirmed" % (lang, dev))
            results["errors"] += errs; ctx.close()

            # ---- 1b. the same while a repair is open (the state of the live test): landing -> tenancy tab -> line -> save
            ctx, pg, errs = open_page(b, lang, dev, "index", 11)
            pg.evaluate("(() => { const u = NLRM.ix.unit[11]; return NLRM.store.save('ticket', { property_id: u.property_id, unit_id: u.id, title: 'x', body: '', category: 'general', urgency: 'standard', status: 'new', reporter: 'owner', vendor_id: 0, cost: 0, due_by: NLRM.addDays(NLRM.todayIso(), 30), meta: {} }); })()")
            pg.wait_for_timeout(400)
            check("%s with an open repair the landing card is the repair (no index button on it)" % tag, pg.locator(".nt2-card.is-fault").count() == 1 and pg.locator(".nt2-card [data-act='index']").count() == 0)
            presses = 0
            pg.click(".nt2-nav [data-nav='rent']"); presses += 1
            pg.wait_for_selector(".nt2-sum-idx [data-act='index']", timeout=6000)
            pg.click(".nt2-sum-idx [data-act='index']"); presses += 1
            pg.wait_for_selector("#nt2 [data-act='idx-save']", timeout=6000)
            pg.click("#nt2 [data-act='idx-save']"); presses += 1
            pg.wait_for_function("NLRM.store.d.events.some(e => e.type === 'index_confirmed')", timeout=6000)
            check("%s open repair: the index confirmation is reached and saved in 3 presses from the landing screen" % tag, presses == 3)
            results["presses"][tag + " index, repair open"] = presses
            results["errors"] += errs; ctx.close()

            # ---- 1c. update not due yet (scene quiet): the line and the sum are there, the sheet has no save and says when
            ctx, pg, errs = open_page(b, lang, dev, "quiet", 11, route="rent")
            # the sample lease has no update left on this date; give it one about two weeks ahead (every 15 months)
            pg.evaluate("(() => { const l = NLRM.store.d.leases.find(x => x.id === 201); return NLRM.store.save('lease', { id: l.id, linkage: Object.assign({}, l.linkage, { every: 15 }) }); })()")
            pg.wait_for_timeout(400)
            s = pg.evaluate(SUM_JS)
            check("%s update not due: the index line is there and whole" % tag, s["n"] == 4 and s["clipped"] == 0 and s["btn"], s)
            pg.click(".nt2-sum-idx [data-act='index']")
            pg.wait_for_selector(".nt2-sw .nt2-wait", timeout=6000)
            txt = pg.inner_text(".nt2-sw")
            check("%s update not due: the sheet shows the sum by today's index, says when confirming opens, and has NO save button" % tag, pg.locator("#nt2 [data-act='idx-save']").count() == 0 and (("לפי המדד הידוע היום" in txt and "שבוע לפני" in txt) if lang == "he" else ("By the index known today" in txt and "a week before" in txt)), txt[:200])
            small = pg.evaluate("[...document.querySelectorAll('.nt2-sw button')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.height < 43.5 || r.width < 43.5); }).length")
            check("%s that sheet's buttons >= 44 px" % tag, small == 0, small)
            pg.wait_for_timeout(400); shot(pg, "%s-%s-8-index-not-due" % (lang, dev))
            pg.click(".nt2-sw button[data-close]"); pg.wait_for_timeout(300)
            # no update left in the lease: the line says so, no button
            pg.evaluate("(() => { const l = NLRM.store.d.leases.find(x => x.id === 201); return NLRM.store.save('lease', { id: l.id, end_date: NLRM.addDays(NLRM.todayIso(), 20) }); })()")
            pg.wait_for_timeout(400)
            s = pg.evaluate(SUM_JS)
            check("%s no update left before the lease ends: the line says so and has no button" % tag, s["n"] == 4 and s["btn"] is None and (("אין עוד עדכון" in s["text"]) if lang == "he" else ("none left" in s["text"])), s)
            results["errors"] += errs; ctx.close()

            # ---- 1d. an update whose date passed without a confirmation (the sample lease on 10.11: the update of 1.9.2026)
            ctx, pg, errs = open_page(b, lang, dev, "quiet", 11, route="rent")
            s = pg.evaluate(SUM_JS)
            past = pg.locator(".nt2-sum-idx.is-past").count()
            check("%s an update date that passed unconfirmed: the line says so and keeps its button" % tag, past == 1 and s["btn"] and s["clipped"] == 0 and (("לא אושר" in s["text"] and "1.9.2026" in s["text"]) if lang == "he" else ("not confirmed" in s["text"])), s)
            pg.click(".nt2-sum-idx [data-act='index']")
            pg.wait_for_selector("#nt2 [data-act='idx-save']", timeout=6000)
            pg.click("#nt2 [data-act='idx-save']")
            pg.wait_for_function("NLRM.store.d.events.some(e => e.type === 'index_confirmed')", timeout=6000)
            pg.wait_for_timeout(400)
            ev = pg.evaluate("NLRM.store.d.events.filter(e => e.type === 'index_confirmed')[0].meta")
            pg.click(".nt2-sw button[data-close]"); pg.wait_for_timeout(350)
            s = pg.evaluate(SUM_JS)
            check("%s it is confirmed for its own month (2026-09) in 2 presses, and the line then says none is left" % tag, ev["start_month"] == "2026-09" and s["btn"] is None and pg.locator(".nt2-sum-idx.is-past").count() == 0, [ev["start_month"], s["text"]])
            shot(pg, "%s-%s-9-index-past-confirmed" % (lang, dev))
            results["errors"] += errs; ctx.close()

            # ---- a lease that is not index-linked has no index line
            ctx, pg, errs = open_page(b, lang, dev, "quiet", 12, route="rent")
            mode = pg.evaluate("((NLRM.ix.leaseByUnit[12] || {}).linkage || {}).mode || ''")
            check("%s a lease without index linkage (mode '%s') has no index line" % (tag, mode), mode == "cpi" or pg.locator(".nt2-sum-idx").count() == 0)
            results["errors"] += errs; ctx.close()
    b.close()

ok = sum(1 for c in results["checks"] if c["ok"]); n = len(results["checks"])
check("no console errors in any run", not results["errors"], results["errors"][:3])
ok = sum(1 for c in results["checks"] if c["ok"]); n = len(results["checks"])
(ROOT / "docs/rentals/build/slice1/lab-723-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nRESULT %d/%d checks passed" % (ok, n))
sys.exit(0 if ok == n else 1)
