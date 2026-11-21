# -*- coding: utf-8 -*-
"""HAD-787 board 25: the row from the value estimator to the forum's apartment form, pressed as a visitor (a guest, no session),
on a phone width and on desktop, on the live site.
  python scripts/project-stage/est_forum_live_check.py <out dir>            the live site as it is
  set LOCAL=1 first: the three changed files are served from the repo into the live pages (a check BEFORE a release)
Nothing is published by this script: it never presses "להציג לפורום", and it counts the write requests (must be 0)."""
import json, os, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[1]
BASE = "https://nad-lan.co.il"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(REPO, "plugins", "nadlan-config", "assets")
LOCAL = os.environ.get("LOCAL") == "1"
MAP = {"instruments/tools/pval.js": "application/javascript", "proforum/home.js": "application/javascript", "proforum/home.css": "text/css"}
os.makedirs(OUT, exist_ok=True)
LEDGER = []


def note(step, ok, detail=""):
    LEDGER.append({"step": step, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("PASS " if ok else "FAIL ") + step + ((" | " + str(detail)[:220]) if detail else ""))


def run(br, name, mobile):
    c = br.new_context(viewport={"width": 390, "height": 844} if mobile else {"width": 1280, "height": 900}, locale="he-IL", is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
    writes = []
    c.on("request", lambda r: writes.append(r.url) if r.method == "POST" and "/wp-json/nadlan/v1/forum/" in r.url else None)
    if LOCAL:
        for rel, ct in MAP.items():
            body = open(os.path.join(P, *rel.split("/")), "rb").read()
            c.route("**/assets/" + rel + "*", lambda route, request, body=body, ct=ct: route.fulfill(status=200, body=body, content_type=ct + "; charset=utf-8"))
    g = c.new_page()
    g.goto(BASE + "/property-value-estimator/?t=%d" % time.time(), wait_until="networkidle", timeout=90000)
    g.wait_for_timeout(1500)
    g.evaluate("() => { window.__ev = []; const o = window.nlTrack; window.nlTrack = function (n, d) { window.__ev.push(n); try { return o && o.apply(this, arguments); } catch (e) {} }; }")
    note(name + ": no row on the opening example", g.locator(".nlpvf").count() == 0)
    g.locator(".nli__form button", has_text="3").first.click()
    g.wait_for_timeout(1200)
    row = g.locator(".nlpvf").first
    note(name + ": the row shows after a value was changed", row.count() == 1 and row.is_visible(), g.locator(".nlpvf").count())
    pos = g.evaluate("""() => { const r = document.querySelector('.nlpvf'); if (!r) return null; const p = r.previousElementSibling, a = r.parentNode.querySelector('.nli__answer');
        return { afterNote: !!p && p.classList.contains('nli__note'), noteEnd: p ? p.textContent.trim().slice(-34) : '', belowNumber: a.getBoundingClientRect().top < r.getBoundingClientRect().top,
                 fixed: getComputedStyle(r).position, linkH: Math.round(r.querySelector('a').getBoundingClientRect().height), link: r.querySelector('a').textContent, href: r.querySelector('a').getAttribute('href'),
                 w: Math.round(r.getBoundingClientRect().width), pageW: document.documentElement.scrollWidth, vw: innerWidth }; }""")
    note(name + ": it sits right after the note, below the number, not floating", pos and pos["afterNote"] and pos["belowNumber"] and pos["fixed"] == "static", pos)
    note(name + ": link text and target, 44px or more, no sideways scroll", pos and pos["link"] == "שאלו בפורום על הדירה שלכם" and pos["href"].endswith("/forum/#ask-home") and "?" not in pos["href"] and pos["linkH"] >= 44 and pos["pageW"] <= pos["vw"] + 1, "")
    g.evaluate("() => { const r = document.querySelector('.nlpvf').getBoundingClientRect(); window.scrollBy(0, r.top - %d); }" % (330 if mobile else 300)); g.wait_for_timeout(600)
    g.screenshot(path=os.path.join(OUT, "e1-%s-row-in-estimator.png" % name))
    est = g.locator(".nli__answer output").first.inner_text()
    row.locator("a").click()
    g.wait_for_url("**/forum/#ask-home", timeout=60000); g.wait_for_load_state("networkidle"); g.wait_for_timeout(2500)
    f = g.evaluate("""() => { const d = document.getElementById('nlfh-compose'), f = d && d.querySelector('form'); if (!f) return null; const ch = f.querySelector('[data-nlfh-from]');
        return { open: d.open, city: f.elements.city.value, other: f.elements.city_other.value, nbhd: f.elements.nbhd.value, rooms: f.elements.rooms.value, sqm: f.elements.sqm.value, body: f.elements.body.value, chip: ch ? ch.innerText : '', store: !!sessionStorage.getItem('nlfh_from_est') }; }""")
    note(name + ": the forum form opens filled (city, rooms, size, question, chip)", f and f["open"] and (f["city"] == "תל אביב יפו" or f["other"] == "תל אביב יפו") and f["rooms"] == "3" and f["sqm"] == "100" and "המחשבון נתן לי" in f["body"] and "הועבר מהמחשבון" in f["chip"], f)
    num = "".join(ch for ch in est if ch.isdigit())
    note(name + ": the carried estimate equals the number shown in the tool", f and num and num in f["chip"].replace(",", ""), est)
    g.wait_for_timeout(400)
    g.screenshot(path=os.path.join(OUT, "e2-%s-forum-form-filled.png" % name))
    g.locator("[data-nlfh-from] .nlfh-from-x").click(); g.wait_for_timeout(700)
    f2 = g.evaluate("""() => { const f = document.querySelector('#nlfh-compose form'); return { city: f.elements.city.value, rooms: f.elements.rooms.value, sqm: f.elements.sqm.value, body: f.elements.body.value, chip: !!f.querySelector('[data-nlfh-from]'), store: !!sessionStorage.getItem('nlfh_from_est'), open: document.getElementById('nlfh-compose').open }; }""")
    note(name + ": the chip's X removes the carried details", f2 and not f2["chip"] and not f2["store"] and f2["city"] == "" and f2["rooms"] == "" and f2["sqm"] == "" and f2["body"] == "" and f2["open"], f2)
    note(name + ": nothing was sent to the forum without the last press", len(writes) == 0, writes[:2])
    ev = g.evaluate("() => window.__ev || []")
    # the second pass: the tick off, and the price-per-metre method
    g.goto(BASE + "/property-value-estimator/?t=%d" % time.time(), wait_until="networkidle", timeout=90000); g.wait_for_timeout(1500)
    g.evaluate("() => { window.__ev = []; const o = window.nlTrack; window.nlTrack = function (n, d) { window.__ev.push(n + ':' + JSON.stringify(d || {})); try { return o && o.apply(this, arguments); } catch (e) {} }; }")
    g.locator(".nli__form button", has_text="5").first.click(); g.wait_for_timeout(1200)
    g.locator(".nlpvf input[type=checkbox]").uncheck(); g.wait_for_timeout(300)
    g.locator(".nli__form button", has_text="4").first.click(); g.wait_for_timeout(1200)
    note(name + ": the tick stays off after the result is redrawn", g.locator(".nlpvf input[type=checkbox]").is_checked() is False)
    ev2 = g.evaluate("() => window.__ev")
    note(name + ": the event 'row shown' fires once per page", sum(1 for e in ev2 if e.startswith("est_forum_row")) == 1, ev2)
    g.locator(".nli__form button", has_text="לפי מחיר למ״ר").first.click(); g.wait_for_timeout(1200)
    note(name + ": no row when the result is not a median (price per metre)", g.locator(".nlpvf").count() == 0)
    g.locator(".nli__form button", has_text="לפי עסקאות בשכונה").first.click(); g.wait_for_timeout(1200)
    with g.expect_navigation(timeout=60000):
        g.evaluate("() => { const a = document.querySelector('.nlpvf a'); a.addEventListener('click', () => { window.name = JSON.stringify(window.__ev); }); a.click(); }")
    g.wait_for_load_state("networkidle"); g.wait_for_timeout(2000)
    ev3 = g.evaluate("() => { try { return JSON.parse(window.name || '[]'); } catch (e) { return []; } }")
    note(name + ": the event 'link pressed' fires, with carry 0 when the tick is off", any(e.startswith("est_forum_press") and '"carry":0' in e for e in ev3), ev3)
    f3 = g.evaluate("""() => { const d = document.getElementById('nlfh-compose'), f = d.querySelector('form'); return { open: d.open, city: f.elements.city.value, body: f.elements.body.value, chip: !!f.querySelector('[data-nlfh-from]') }; }""")
    note(name + ": with the tick off the form opens empty", f3["open"] and f3["city"] == "" and f3["body"] == "" and not f3["chip"], f3)
    note(name + ": still nothing sent to the forum", len(writes) == 0, writes[:2])
    c.close()
    return ev


with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True)
    try:
        run(br, "phone", True)
        run(br, "desktop", False)
    finally:
        br.close()
json.dump({"local_files": LOCAL, "at": time.strftime("%Y-%m-%d %H:%M:%S"), "ledger": LEDGER}, open(os.path.join(OUT, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("RESULT %d/%d%s" % (sum(1 for x in LEDGER if x["ok"]), len(LEDGER), "  (LOCAL files routed into the live pages)" if LOCAL else ""))
