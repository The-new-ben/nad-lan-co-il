# -*- coding: utf-8 -*-
"""UnitDesignRequest (design system v102, HAD-346 Batch 2): the designer's request path in a real Chrome, at 1440, 390 and
320. The page is the LIVE /tour/designer/ URL answered with the branch's plugin copy (assets/tours/designer-tour.html);
POST /wp-json/nadlan/v1/lead and /rfp are answered by rfp_local_endpoint.php (the branch's REAL nadlan_rfp_create over
in-memory doubles); every other non-GET and WhatsApp are aborted. Nothing reaches the site, no lead, no database.

Codex's acceptance, per width:
  13-e: an armchair turned 12 quarter turns, 8 notes (the wider opening first) -> reload -> another unit (empty) -> back
  (all there) -> summary -> details -> send: the document fails once -> the failure is said, retry makes the document
  only -> received: server ref, document link, 8 notes, one lead, one document, the same client_ref and design twice.
  7-n: a double click on send -> one lead, one request.
  no unit: the demonstration stays, and its end says "מוכנה", not "בדרך ליזם".
  python scripts/project-stage/test_designer_request.py [--out DIR]"""
import argparse, io, json, os, re, subprocess, sys, time, hashlib
from urllib.parse import quote
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGNER = os.path.join(HERE, "..", "..", "plugins", "nadlan-config", "assets", "tours", "designer-tour.html")
ORIGIN = "https://nad-lan.co.il"
NOTES = [("door-bath", "פתח רחב יותר לחדר הרחצה, 90 ס״מ"), ("door-mamad", "דלת ממ״ד נפתחת החוצה"), ("window-bedroom", "תריס חשמלי"),
         ("window-kitchen", "חלון גבוה יותר מעל הכיור"), ("door-entry", "דלת כניסה רחבה"), ("door-balcony", "מסילה שקועה ברצפה"), ("wall", "גוון חם יותר בסלון")]


def url(unit=None):
    if not unit:
        return ORIGIN + "/tour/designer/?rm=1"
    return ORIGIN + "/tour/designer/?rm=1&project=rainbow-tel-aviv&unit=" + unit + "&pn=" + quote("ריינבו תל אביב") + "&ul=" + quote("קומה " + unit.split("-")[0] + " · לכיוון רמת אביב והאוניברסיטה")


E2E = False


def run(W, H, out):
    state = os.path.join(out, "ep-state-%d%s.json" % (W, "-e2e" if E2E else ""))
    if os.path.exists(state):
        os.remove(state)
    posts = []

    def endpoint(route):
        req = route.request
        op = "lead" if req.url.endswith("/nadlan/v1/lead") else "rfp"
        body = req.post_data or "{}"
        posts.append({"op": op, "body": json.loads(body)})
        r = subprocess.run(["php", os.path.join(HERE, "rfp_local_endpoint.php"), op, state], input=body, capture_output=True, text=True, encoding="utf-8")
        res = json.loads(r.stdout)
        route.fulfill(status=res["status"], content_type="application/json", body=json.dumps(res["body"], ensure_ascii=False))

    def guard(route):
        r = route.request
        if re.match(r"https://(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)/", r.url) or r.method != "GET":
            return route.abort()
        return route.fallback()

    def srv_state():
        r = subprocess.run(["php", os.path.join(HERE, "rfp_local_endpoint.php"), "state", state], input="{}", capture_output=True, text=True, encoding="utf-8")
        return json.loads(r.stdout)["body"]

    res = {"viewport": [W, H]}
    mob = W < 600
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
        ctx = b.new_context(viewport={"width": W, "height": H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1)
        ctx.route("**/*", guard)
        ctx.route(re.compile(re.escape(ORIGIN) + r"/wp-json/nadlan/v1/(lead|rfp)$"), endpoint)
        ctx.route(re.compile(re.escape(ORIGIN) + r"/tour/designer/.*"), lambda r: r.fulfill(path=DESIGNER, content_type="text/html; charset=utf-8"))
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:160]))

        def boot(u):
            pg.goto(url(u), wait_until="domcontentloaded", timeout=90000)
            pg.wait_for_function("() => window.__APT && window.__APT.enter", timeout=60000)
            pg.evaluate("() => __APT.enter()"); pg.wait_for_timeout(1800)

        def counts():
            return pg.evaluate("() => ({ notes: Object.keys(__APT.notes()).length, furn: __APT.furn().length, brand: (document.querySelector('#brand .s') || {}).textContent || '' })")

        # 13-e: design, 8 notes, a multi-turn rotation
        boot("13-e")
        pg.screenshot(path=os.path.join(out, "d3-ctx-%d.png" % W))
        pg.evaluate("() => { __APT.addFurn('armchair', 3.2, 0, 12 * Math.PI / 4); }")
        for k, t in NOTES:
            pg.evaluate("([k, t]) => __APT.note(k, t)", [k, t])
        pg.evaluate("() => { const f = __APT.furn()[0]; __APT.note(f.id, 'כורסה ליד החלון'); __APT.save(); }")
        res["after_design"] = counts()
        boot("13-e"); res["after_reload"] = counts()
        boot("25-w"); res["other_unit"] = counts()
        boot("13-e"); res["back"] = counts()
        # the flow, to a real send that fails once at the document
        pg.evaluate("() => __APT.flow('summary')"); pg.wait_for_timeout(700)
        pg.click("#toDetails"); pg.wait_for_timeout(300)
        pg.evaluate("() => __APT.setContact('בדיקה', '0500000000')")
        pg.click("#toPay"); pg.wait_for_timeout(500)
        res["send_step"] = pg.evaluate("() => ({ step: __APT.flowStep(), ribbon: document.querySelector('#demoRibbon').textContent, ctx: document.querySelector('#ctxLine').textContent, bar4: document.querySelector('#flowBar .fs[data-fs=\"3\"] .t').textContent, rows: [...document.querySelectorAll('#sendCard .srow')].map(r => r.textContent) })")
        pg.screenshot(path=os.path.join(out, "d3-send-%d.png" % W))
        pg.click("#sendBtn"); pg.wait_for_timeout(400)
        res["no_consent"] = pg.evaluate("() => ({ err: document.querySelector('#fConsent').classList.contains('err'), posts: 0 })"); res["no_consent"]["posts"] = len(posts)
        st = json.load(open(state, encoding="utf-8")) if os.path.exists(state) else {}
        pg.click("#fConsent input")
        # the document insert fails once (a server-side failure after the lead was received)
        stj = {"seq": 900, "inserts": [], "writes": [], "options": {"nadlan_feature_lead_e2e": "1" if E2E else "0"}, "content": {}, "names": {}, "hooks": [], "leads": [], "transients": {}, "mail": [], "fail_insert_times": 1,
               "projects": {"rainbow-tel-aviv": 101, "duo-tel-aviv": 102}, "types": {"101": "nadlan_project", "102": "nadlan_project"}, "meta": {}}
        json.dump(stj, open(state, "w", encoding="utf-8"))
        pg.click("#sendBtn"); pg.wait_for_selector("#sendErr:not([hidden])", timeout=15000); pg.wait_for_timeout(300)
        res["failure"] = pg.evaluate("() => ({ title: document.querySelector('#sendErrT').textContent, text: document.querySelector('#sendErrP').textContent, retry: document.querySelector('#sendRetry').textContent, step: __APT.flowStep() })")
        pg.screenshot(path=os.path.join(out, "d3-fail-%d.png" % W))
        pg.click("#sendRetry"); pg.wait_for_function("() => __APT.flowStep() === 'done'", timeout=15000); pg.wait_for_timeout(600)
        res["done"] = pg.evaluate("() => { const NL = String.fromCharCode(10); const wa = decodeURIComponent(document.querySelector('#waBtn').href); return { title: document.querySelector('#okTitle').textContent, ref: document.querySelector('#okRef').textContent, text: document.querySelector('#okText').textContent, doc: document.querySelector('#docBtn').href, docShown: !document.querySelector('#docBtn').hidden, waMore: wa.split(NL).filter(l => /ועוד \\d+ הערות/.test(l)), waDoc: wa.split(NL).filter(l => l.indexOf('מסמך הבקשה:') === 0).length, waUnit: wa.split(NL)[1] || '' }; }")
        pg.screenshot(path=os.path.join(out, "d3-done-%d.png" % W))
        s1 = srv_state()
        rfps = [x for x in posts if x["op"] == "rfp"]
        doc = s1["docs"][0] if s1["docs"] else {}
        res["server"] = {"leads": len(s1["leads"]), "docs": len(s1["docs"]), "doc_unit": (doc.get("unit") or {}).get("id"), "doc_notes": len((doc.get("design") or {}).get("notes", [])),
                         "first_note": ((doc.get("design") or {}).get("notes") or [{}])[0].get("text"), "ry": [i.get("ry") for i in (doc.get("design") or {}).get("layers", {}).get("space3d", {}).get("items", [])],
                         "lead_linked": bool(doc.get("lead_id")), "rfp_posts": len(rfps), "same_ref": len({x["body"].get("client_ref") for x in rfps}) == 1,
                         "same_design": len({json.dumps(x["body"].get("design"), sort_keys=True) for x in rfps}) == 1, "lead_posts": len([x for x in posts if x["op"] == "lead"])}
        # 7-n: a double click
        posts.clear()
        boot("7-n")
        pg.evaluate("() => { __APT.note('door-bath', 'פתח רחב יותר'); __APT.save(); __APT.flow('summary'); }"); pg.wait_for_timeout(500)
        pg.click("#toDetails"); pg.evaluate("() => __APT.setContact('בדיקה', '0500000000')"); pg.click("#toPay"); pg.wait_for_timeout(300)
        pg.click("#fConsent input")
        pg.evaluate("() => { const b = document.querySelector('#sendBtn'); b.click(); b.click(); }")
        pg.wait_for_function("() => __APT.flowStep() === 'done'", timeout=15000)
        res["double_click"] = {"lead_posts": len([x for x in posts if x["op"] == "lead"]), "rfp_posts": len([x for x in posts if x["op"] == "rfp"])}
        # no unit: the demonstration
        posts.clear()
        boot(None)
        pg.evaluate("() => { __APT.flow('summary'); }"); pg.wait_for_timeout(400)
        pg.click("#toDetails"); pg.evaluate("() => __APT.setContact('בדיקה', '0500000000')"); pg.click("#toPay"); pg.wait_for_timeout(300)
        res["demo_pay_step"] = pg.evaluate("() => __APT.flowStep()")
        pg.evaluate("() => __APT.pay()"); pg.wait_for_function("() => __APT.flowStep() === 'done'", timeout=10000); pg.wait_for_timeout(400)
        res["demo_done"] = pg.evaluate("() => ({ title: document.querySelector('#okTitle').textContent, text: document.querySelector('#okText').textContent, posts: 0 })"); res["demo_done"]["posts"] = len(posts)
        pg.screenshot(path=os.path.join(out, "d3-demo-done-%d.png" % W))
        res["overflow"] = pg.evaluate("() => document.documentElement.scrollWidth > innerWidth + 1")
        res["page_errors"] = errs[:5]
        b.close()
    ok = {
        "design_kept_per_unit": res["after_design"]["notes"] == 8 and res["after_reload"] == res["after_design"] and res["other_unit"]["notes"] == 0 and res["other_unit"]["furn"] == 0 and res["back"]["notes"] == 8 and res["back"]["furn"] == 1,
        "context_shown": "13" in res["after_design"]["brand"] and "קומה 13" in res["send_step"]["ctx"] and res["send_step"]["bar4"] == "שליחה" and res["send_step"]["step"] == "send",
        "consent_required": res["no_consent"]["err"] and res["no_consent"]["posts"] == 0,
        "failure_said": "מסמך הבקשה לא נוצר" in res["failure"]["title"] and res["failure"]["step"] == "send",
        "received": "התקבלה" in res["done"]["title"] and res["done"]["docShown"] and "8" in res["done"]["text"],
        "whatsapp_all_notes": res["done"]["waMore"] == ["  ועוד 2 הערות במסמך הבקשה"] and res["done"]["waDoc"] == 1 and "13-e" in res["done"]["waUnit"],
        "one_lead_one_doc": res["server"]["leads"] == 1 and res["server"]["docs"] == 1 and res["server"]["lead_posts"] == 1 and res["server"]["rfp_posts"] == 2 and res["server"]["same_ref"] and res["server"]["same_design"],
        "doc_is_13e_with_8_notes": res["server"]["doc_unit"] == "13-e" and res["server"]["doc_notes"] == 8 and res["server"]["first_note"] == NOTES[0][1] and res["server"]["lead_linked"],
        "rotation_one_turn": all(abs(r) <= 3.1416 for r in res["server"]["ry"]),
        "double_click_once": res["double_click"] == {"lead_posts": 1, "rfp_posts": 1},
        "demo_kept_and_honest": res["demo_pay_step"] == "pay" and "מוכנה" in res["demo_done"]["title"] and res["demo_done"]["posts"] == 0,
        "no_page_errors": not res["page_errors"],
        "no_horizontal_scroll": not res["overflow"],
    }
    res["checks"] = ok
    return res


def main():
    global E2E
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=os.path.join(HERE, "_designer_test"))
    ap.add_argument("--lead-e2e", action="store_true", help="run the lead test-mode branch (inc/lead-e2e.php) in the local endpoint")
    ap.add_argument("--widths", default="1440x900,390x844,320x740"); a = ap.parse_args()
    E2E = a.lead_e2e
    os.makedirs(a.out, exist_ok=True)
    allres = [run(int(w.split("x")[0]), int(w.split("x")[1]), a.out) for w in a.widths.split(",")]
    failed = [(r["viewport"], k) for r in allres for k, v in r["checks"].items() if not v]
    print(json.dumps({"mode": "real Chrome; the branch's designer + the branch's /lead and /rfp code via a local endpoint; no request reaches the site", "lead_e2e": E2E,
                      "designer_sha256": hashlib.sha256(open(DESIGNER, "rb").read()).hexdigest(), "failed": failed, "results": allres}, ensure_ascii=False, indent=1))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
