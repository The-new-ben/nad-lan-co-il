# -*- coding: utf-8 -*-
"""The integrated buyer journey on the LOOPBACK preview (serve_journey.py must be running), in a real Chrome:
Rainbow ?unit=13-e -> the card -> "הנוף והמפה" (the landing, the unit line, the cone) -> "חזרה לבניין" -> "לעצב את הדירה"
-> the designer for 13-e -> 8 notes + a turned armchair -> summary -> details -> send (the branch's /lead and /rfp, local)
-> received -> the rendered document (13-e, all 8 notes) -> "חזרה לעמוד הפרויקט" -> the same unit on the stage.

What is clicked and what is injected (said in the result):
  CLICKED: the card's buttons, the unit line's back button, the designer's door button, the summary button, "המשך",
           the name and phone typed, "המשך לשליחה", the consent box, "שליחת הבקשה", the document link, its back link.
  INJECTED (the designer's QA hooks, because its hotspots are 3D sprites without DOM targets): opening each note's sheet
           (__APT.noteSheet) and placing the armchair (__APT.addFurn). The note TEXT is typed into the real sheet and
           saved with its real "שמירת ההערה" button.
  python scripts/project-stage/test_journey.py [--base http://127.0.0.1:47915] [--out DIR] [--widths 390x844,1440x900]"""
import argparse, io, json, os, re, sys, time, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

NOTES = [("door-bath", "פתח רחב יותר לחדר הרחצה, 90 ס״מ"), ("door-mamad", "דלת ממ״ד נפתחת החוצה"), ("window-bedroom", "תריס חשמלי"),
         ("window-kitchen", "חלון גבוה יותר מעל הכיור"), ("door-entry", "דלת כניסה רחבה"), ("door-balcony", "מסילה שקועה ברצפה"), ("wall", "גוון חם יותר בסלון")]


def journey(base, W, H, out):
    urllib.request.urlopen(base + "/__reset").read()
    res = {"viewport": [W, H], "clicked": [], "injected": []}
    mob = W < 600
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
        ctx = b.new_context(viewport={"width": W, "height": H}, is_mobile=mob, has_touch=mob, device_scale_factor=2 if mob else 1)
        # a second guard in the test itself: nothing but GETs may leave for the real site
        ctx.route(re.compile(r"https://(nad-lan\.co\.il|wa\.me|api\.whatsapp\.com)/.*"), lambda r: r.abort() if r.request.method != "GET" or "whatsapp" in r.request.url or "wa.me" in r.request.url else r.fallback())
        pg = ctx.new_page(); errs = []; csp = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:140]))
        # every Content-Security-Policy refusal the pages hit (analytics, payment, telemetry... must be refused; the journey not)
        onc = lambda m: csp.append(m.text[:200]) if ("Content Security Policy" in m.text or "Refused to" in m.text) else None
        ctx.on("page", lambda np: np.on("console", onc))
        pg.on("console", onc)
        click = lambda sel, what: (pg.locator(sel).first.click(), res["clicked"].append(what))
        pg.goto(base + "/projects/rainbow-tel-aviv/?unit=13-e", wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_timeout(3000)
        pg.evaluate("() => { const e = document.querySelector('#nlps'); scrollTo(0, e.getBoundingClientRect().top + scrollY - 70); }")
        pg.wait_for_function("() => /13/.test((document.querySelector('#nlps-pick .rbs-label-title') || {}).textContent || '')", timeout=45000)
        res["1_card"] = pg.evaluate("() => ({ title: document.querySelector('#nlps-pick .rbs-label-title').textContent, url: location.search })")
        pg.screenshot(path=os.path.join(out, "j1-card-%d.png" % W))
        click('#nlps-pick .rbs-act[data-act="view"]', "הנוף והמפה"); pg.wait_for_timeout(3500)
        res["2_map"] = pg.evaluate("() => { const w = document.querySelector('.nlps-cone path'); const r = w && w.getBoundingClientRect(); return { line: (document.querySelector('.nlps-mapsum-t') || {}).textContent || '', wedge_in_view: !!r && r.top >= 0 && r.bottom <= innerHeight }; }")
        pg.screenshot(path=os.path.join(out, "j2-map-%d.png" % W))
        click(".nlps-mapsum [data-nlps-back]", "חזרה לבניין"); pg.wait_for_timeout(1800)
        res["3_back"] = pg.evaluate("() => ({ title: (document.querySelector('#nlps-pick .rbs-label-title') || {}).textContent || '', stage_top: Math.round(document.querySelector('#nlps').getBoundingClientRect().top) })")
        with pg.expect_navigation(timeout=30000):
            click('#nlps-pick .rbs-act[data-act="design"]', "לעצב את הדירה")
        res["4_designer_url"] = pg.url.replace(base, "")
        pg.wait_for_selector("#enterBtn", timeout=60000)
        pg.wait_for_function("() => window.__APT && window.__APT.enter", timeout=60000)
        pg.wait_for_timeout(1500)
        click("#enterBtn", "פתחו את הדלת")
        pg.wait_for_timeout(1500)
        if pg.locator("#skipChip").is_visible():
            click("#skipChip", "דילוג")
        pg.wait_for_function("() => document.body.classList.contains('ui')", timeout=40000); pg.wait_for_timeout(800)
        res["4_brand"] = pg.evaluate("() => (document.querySelector('#brand .s') || {}).textContent || ''")
        pg.screenshot(path=os.path.join(out, "j4-designer-%d.png" % W))
        pg.evaluate("() => __APT.addFurn('armchair', 3.2, 0, 12 * Math.PI / 4)"); res["injected"].append("addFurn armchair (3D floor tap)")
        fid = pg.evaluate("() => __APT.furn()[0].id")
        for k, t in NOTES + [(fid, "כורסה ליד החלון")]:
            pg.evaluate("(k) => __APT.noteSheet(k)", k); res["injected"].append("noteSheet " + k)
            pg.wait_for_selector("#sheet.on #noteField", timeout=8000)
            pg.fill("#noteField", t); click("#noteSave", "שמירת ההערה")
            pg.wait_for_timeout(250)
            if pg.locator("#sheetClose").is_visible():
                click("#sheetClose", "סגירת החלונית")
            pg.wait_for_timeout(200)
        res["5_notes"] = pg.evaluate("() => Object.keys(__APT.notes()).length")
        click("#styleBtn", "סיכום ושליחה"); pg.wait_for_timeout(1200)
        click("#toDetails", "המשך לפרטים"); pg.wait_for_timeout(300)
        pg.fill("#inName", "בדיקה סינתטית"); pg.fill("#inPhone", "0500000000"); res["clicked"].append("typed name + phone")
        click("#toPay", "המשך לשליחה"); pg.wait_for_timeout(500)
        res["6_send_rows"] = pg.evaluate("() => [...document.querySelectorAll('#sendCard .srow')].map(r => r.textContent.replace(/\\s+/g, ' ').trim())")
        click("#fConsent input", "הסכמה")
        click("#sendBtn", "שליחת הבקשה")
        pg.wait_for_function("() => __APT.flowStep() === 'done'", timeout=30000); pg.wait_for_timeout(800)
        res["7_done"] = pg.evaluate("() => ({ title: document.querySelector('#okTitle').textContent, ref: document.querySelector('#okRef').textContent, doc: document.querySelector('#docBtn').getAttribute('href') })")
        pg.screenshot(path=os.path.join(out, "j7-done-%d.png" % W))
        with ctx.expect_page(timeout=20000) as pop:
            click("#docBtn", "צפייה במסמך הבקשה")
        doc = pop.value; doc.wait_for_load_state("domcontentloaded"); doc.wait_for_timeout(800)
        res["8_doc"] = doc.evaluate("() => { const t = document.body.innerText; return { has_13e: /13-e/.test(t), notes_heading: (t.match(/הערות ובקשות \\((\\d+)\\)/) || [])[1] || null, wider: t.includes('פתח רחב יותר לחדר הרחצה'), back: (document.querySelector('.bar a') || {}).getAttribute ? document.querySelector('.bar a').getAttribute('href') : null }; }")
        doc.screenshot(path=os.path.join(out, "j8-doc-%d.png" % W), full_page=True)
        with doc.expect_navigation(timeout=30000):
            doc.locator(".bar a").first.click(); res["clicked"].append("חזרה לעמוד הפרויקט")
        doc.wait_for_timeout(3000)
        doc.evaluate("() => { const e = document.querySelector('#nlps'); if (e) scrollTo(0, e.getBoundingClientRect().top + scrollY - 70); }")
        try:
            doc.wait_for_function("() => /13/.test((document.querySelector('#nlps-pick .rbs-label-title') || {}).textContent || '')", timeout=45000)
        except Exception:
            pass
        res["9_same_unit"] = doc.evaluate("() => ({ url: location.pathname + location.search, card: (document.querySelector('#nlps-pick .rbs-label-title') || {}).textContent || '', pick: (window.__nlpsPick || {}).unit || '' })")
        doc.screenshot(path=os.path.join(out, "j9-back-%d.png" % W))
        res["page_errors"] = errs[:5]
        hosts = sorted({h for c in csp for h in re.findall(r"https?://([^/'\" ]+)", c)})
        res["csp_refused_hosts"] = hosts
        b.close()
    st = json.loads(urllib.request.urlopen(base + "/__state.json").read().decode("utf-8"))["body"]
    d0 = st["docs"][0] if st["docs"] else {}
    res["10_server"] = {"leads": len(st["leads"]), "docs": len(st["docs"]), "doc_unit": (d0.get("unit") or {}).get("id"), "doc_notes": len((d0.get("design") or {}).get("notes", [])), "lead_linked": bool(d0.get("lead_id"))}
    res["checks"] = {
        "card_13": "13" in res["1_card"]["title"],
        "map_landing": "קומה 13" in res["2_map"]["line"] and res["2_map"]["wedge_in_view"],
        "back_to_building": "13" in res["3_back"]["title"] and res["3_back"]["stage_top"] < 200,
        "designer_for_13e": "unit=13-e" in res["4_designer_url"] and "project=rainbow-tel-aviv" in res["4_designer_url"] and "13" in res["4_brand"],
        "eight_plus_one_notes": res["5_notes"] == 8,
        "received": "התקבלה" in res["7_done"]["title"] and bool(res["7_done"]["doc"]),
        "document_13e_all_notes": res["8_doc"]["has_13e"] and res["8_doc"]["notes_heading"] == "8" and res["8_doc"]["wider"] and "unit=13-e" in (res["8_doc"]["back"] or ""),
        "same_unit_after": "unit=13-e" in res["9_same_unit"]["url"] and res["9_same_unit"]["pick"] == "13-e",
        "one_lead_one_doc": res["10_server"] == {"leads": 1, "docs": 1, "doc_unit": "13-e", "doc_notes": 8, "lead_linked": True},
    }
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--base", default="http://127.0.0.1:47915"); ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "_journey_test"))
    ap.add_argument("--widths", default="390x844,1440x900"); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    manifest = json.loads(urllib.request.urlopen(a.base + "/__manifest.json").read().decode("utf-8"))
    allres = [journey(a.base, int(w.split("x")[0]), int(w.split("x")[1]), a.out) for w in a.widths.split(",")]
    failed = [(r["viewport"], k) for r in allres for k, v in r["checks"].items() if not v]
    manifest2 = json.loads(urllib.request.urlopen(a.base + "/__manifest.json").read().decode("utf-8"))
    print(json.dumps({"mode": "the loopback preview (serve_journey.py): the branch's pages, files and /lead + /rfp callbacks; nothing sent", "head": manifest2["head"],
                      "uncommitted": manifest2["uncommitted"], "served_branch_files": manifest2["served_branch_files"], "failed": failed, "results": allres}, ensure_ascii=False, indent=1))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
