# -*- coding: utf-8 -*-
"""Rentals, release 1.72.728 (HAD-795): sample people. In the sample portfolio of version 2 (the lab runs the same files):
  - no sample person carries a phone or an e-mail, and the whole sample data holds no number shaped like a phone;
  - every sample person's name wears the example mark, in lists and on the card, he and en;
  - on no screen and in no card is there a link to wa.me, tel: or mailto:;
  - a WhatsApp press on a sample person shows the wording only: a text box, a copy button, and a button (never a link);
    pressing it writes the journal line and opens nothing;
  - the reminder button of the day and tenancy screens still exists for a sample tenant and shows the wording.
Headless Edge, NOT a real phone. The public demo of version 1 is checked by lab_sample_people_v1.py against the live page.
Usage: python scripts/rentals/lab_sample_people.py   (server at the repo root: python -m http.server 47921)"""
import sys, json, pathlib, datetime
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:47921/docs/design-lab/rentals/app.html"
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/rentals/build/slice1/shots-728"
OUT.mkdir(parents=True, exist_ok=True)
results = {"checks": [], "errors": []}
MARK = {"he": "(דוגמה)", "en": "(example)"}
ROUTES = ["today", "properties", "people", "money", "repairs", "leasing", "docs", "reports", "settings", "help"]
LINKS = """() => [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => /wa\\.me|whatsapp\\.com|^tel:|^mailto:|^sms:/i.test(h))"""
NUMS = """() => { const t = document.body.innerText, m = t.match(/(?:\\+?972|0)5\\d[\\s-]?\\d{3}[\\s-]?\\d{4}/g); return m || []; }"""


def check(name, ok, info=""):
    results["checks"].append({"check": name, "ok": bool(ok), "info": str(info)[:260]})
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(info)[:190] if info != "" else ""))


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for lang in ("he", "en"):
        for w, h in ((390, 844), (1280, 800)):
            tag = "%s %dx%d" % (lang, w, h)
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, has_touch=w < 900, locale="he-IL")
            ctx.clock.set_fixed_time(datetime.datetime(2026, 11, 10, 9, 0))
            popups = []
            ctx.on("page", lambda pg2: popups.append(pg2.url))
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
            pg.goto("%s?lang=%s#/people" % (BASE, lang), wait_until="networkidle")
            pg.wait_for_function("window.NLRM && NLRM.store && NLRM.store.d && NLRM.ix && NLRM.ix.unit", timeout=10000)
            pg.wait_for_timeout(500)
            popups.clear()
            d = pg.evaluate("""() => { const d = NLRM.store.d, raw = JSON.stringify(d);
              return { n: d.contacts.length, withPhone: d.contacts.filter(c => c.phone).map(c => c.id), withMail: d.contacts.filter(c => c.email).map(c => c.id),
                names: d.contacts.map(c => c.name), nums: raw.match(/9725\\d{8}|05\\d{8}/g) || [], mails: raw.match(/[\\w.]+@[\\w.]+/g) || [], demo: !!d.demo, isDemo: NLRM.isDemo() }; }""")
            check("%s: the sample has %d people, none carries a phone or an e-mail" % (tag, d["n"]), d["n"] == 10 and not d["withPhone"] and not d["withMail"] and d["demo"] and d["isDemo"], d)
            check("%s: the whole sample data holds no phone-shaped number and no e-mail address" % tag, not d["nums"] and not d["mails"], (d["nums"][:3], d["mails"][:3]))
            check("%s: every sample person's name wears the mark %s" % (tag, MARK[lang]), all(MARK[lang] in n for n in d["names"]), [n for n in d["names"] if MARK[lang] not in n])
            # the people list
            rows = pg.evaluate("() => [...document.querySelectorAll('.nlrm-item .nlrm-person b, .nlrm-person b')].map(e => e.textContent)")
            check("%s: the people list shows %d names, each with the mark" % (tag, len(rows)), len(rows) >= 4 and all(MARK[lang] in r for r in rows), [r for r in rows if MARK[lang] not in r][:4])
            if w == 390:
                pg.screenshot(path=str(OUT / ("people-%s.png" % lang)))
            # every screen
            bad = {}
            for r in ROUTES:
                pg.evaluate("r => { location.hash = '#/' + r; }", r)
                pg.wait_for_timeout(350)
                l = pg.evaluate(LINKS); n = pg.evaluate(NUMS)
                if l or n:
                    bad[r] = (l[:2], n[:2])
            check("%s: none of the %d screens holds a wa.me, tel: or mailto: link or a phone-shaped number" % (tag, len(ROUTES)), not bad, bad)
            # every card
            bad = {}; cards = 0
            ids = pg.evaluate("() => { const d = NLRM.store.d; return { contact: d.contacts.map(x => x.id), unit: d.units.map(x => x.id), ticket: d.tickets.map(x => x.id), lease: d.leases.map(x => x.id) }; }")
            for kind in ("contact", "unit", "ticket", "lease"):
                for i in ids[kind]:
                    pg.evaluate("a => { try { NLRM.ui.close(true); } catch (e) {} NLRM.open(a[0], a[1]); }", [kind, i])
                    pg.wait_for_timeout(180)
                    cards += 1
                    tabs = pg.evaluate("() => [...document.querySelectorAll('.nlrm-layer [data-tab], [role=dialog] [data-tab]')].map(e => e.dataset.tab)")
                    for tb in (tabs or [None]):
                        if tb:
                            pg.evaluate("t => { const e = document.querySelector('[data-tab=\"' + t + '\"]'); if (e) { e.click(); } }", tb)
                            pg.wait_for_timeout(90)
                        l = pg.evaluate(LINKS); n = pg.evaluate(NUMS)
                        if l or n:
                            bad["%s:%s:%s" % (kind, i, tb)] = (l[:2], n[:2])
            check("%s: none of the %d cards (people, homes, repairs, leases, every tab) holds such a link or number" % (tag, cards), cards >= 20 and not bad, bad)
            # a WhatsApp press on each sample person: wording only
            okp = []; badp = []
            for i in ids["contact"]:
                pg.evaluate("i => { try { NLRM.ui.close(true); } catch (e) {} NLRM.open('contact', i); }", i)
                pg.wait_for_timeout(200)
                s0 = pg.evaluate("""i => { const b = document.querySelector('[data-act="wa-contact"][data-id="' + i + '"]'); const head = document.body.innerText;
                  return { tag: b ? b.tagName : '', href: b ? b.getAttribute('href') : null, call: !!document.querySelector('a[href^="tel:"]'), n0: NLRM.store.d.events.length }; }""", i)
                if s0["tag"] != "BUTTON" or s0["href"] or s0["call"]:
                    badp.append(("card", i, s0)); continue
                pg.click('[data-act="wa-contact"][data-id="%d"]' % i, timeout=4000)
                pg.wait_for_selector("textarea[name=txt]", timeout=4000)
                pg.wait_for_timeout(320)
                s1 = pg.evaluate("""() => { const ta = document.querySelector('textarea[name=txt]'), f = ta.closest('form'), s = f.querySelector('[data-send]');
                  return { txt: ta.value.length, send: s.tagName, sendHref: s.getAttribute('href'), copy: !!f.querySelector('[data-copy]'), note: !!f.querySelector('.nlrm-note'),
                    links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => /wa\\.me|^tel:|^mailto:/.test(h)) }; }""")
                if not (s1["txt"] > 3 and s1["send"] == "BUTTON" and not s1["sendHref"] and s1["copy"] and s1["note"] and not s1["links"]):
                    badp.append(("sheet", i, s1)); continue
                if i == ids["contact"][1] and w == 390:
                    pg.screenshot(path=str(OUT / ("wording-%s.png" % lang)))
                url0 = pg.url
                pg.click("[data-send]", timeout=4000)
                pg.wait_for_timeout(250)
                s2 = pg.evaluate("n0 => { const ev = NLRM.store.d.events; return { more: ev.length - n0, last: ev[ev.length - 1] && ev[ev.length - 1].type + '/' + ev[ev.length - 1].channel, ev0: ev[0] && ev[0].type + '/' + ev[0].channel }; }", s0["n0"])
                if s2["more"] != 1 or pg.url.split("#")[0] != url0.split("#")[0]:
                    badp.append(("press", i, s2)); continue
                okp.append(i)
            check("%s: a WhatsApp press on each of the 10 sample people shows the wording with a copy button; the send control is a button, writes one journal line, opens nothing" % tag, len(okp) == 10 and not badp, badp[:2])
            check("%s: no new tab or window was opened in the whole run" % tag, not popups, popups[:3])
            results["errors"] += errs; ctx.close()
        # the reminder of the tenancy screen (slice 1): still there for a sample tenant, shows the wording
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, has_touch=True, locale="he-IL")
        ctx.clock.set_fixed_time(datetime.datetime(2026, 11, 10, 9, 0))
        popups = []; ctx.on("page", lambda pg2: popups.append(pg2.url))
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
        found = None
        for unit in (21, 11, 12, 31):
            pg.goto("%s?slice=1&scene=urgent&lang=%s#/rent/%s" % (BASE, lang, unit), wait_until="networkidle")
            pg.wait_for_selector("#nt2:not([hidden]) .nt2-app > *", timeout=10000)
            pg.wait_for_timeout(500)
            if pg.evaluate("() => !!document.querySelector('#nt2 [data-act=remind]')"):
                found = unit; break
        popups.clear()
        check("%s: the tenancy screen of a sample tenant with rent unpaid still offers the reminder (home %s)" % (lang, found), found is not None)
        if found is not None:
            l = pg.evaluate(LINKS)
            pg.evaluate("document.querySelector('#nt2 [data-act=remind]').scrollIntoView({ block: 'center' })")
            pg.wait_for_timeout(150)
            pg.click("#nt2 [data-act=remind]", timeout=5000)
            pg.wait_for_selector("textarea[name=txt]", timeout=5000)
            pg.wait_for_timeout(450)
            s = pg.evaluate("""() => { const ta = document.querySelector('textarea[name=txt]'), f = ta.closest('form'), s = f.querySelector('[data-send]'), r = ta.getBoundingClientRect(), top = document.elementFromPoint(r.left + r.width / 2, r.top + 12);
              return { txt: ta.value, send: s.tagName, onTop: !!top && (top === ta || ta.contains(top)), nums: ta.value.match(/05\\d[\\s-]?\\d{3}[\\s-]?\\d{4}/g) || [] }; }""")
            check("%s: the reminder shows its wording above the day screen, the send control is a button, the wording holds no phone-shaped number" % lang,
                  len(s["txt"]) > 10 and s["send"] == "BUTTON" and s["onTop"] and not s["nums"] and not l, (s["txt"][:70], s["send"], s["onTop"], s["nums"], l))
            pg.screenshot(path=str(OUT / ("reminder-%s.png" % lang)))
        check("%s: the day and tenancy screens opened no tab" % lang, not popups, popups[:2])
        results["errors"] += errs; ctx.close()
    b.close()

check("no page errors in any run", not results["errors"], results["errors"][:3])
ok = sum(1 for c in results["checks"] if c["ok"]); n = len(results["checks"])
(ROOT / "docs/rentals/build/slice1/lab-728-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nRESULT %d/%d checks passed" % (ok, n))
sys.exit(0 if ok == n else 1)
