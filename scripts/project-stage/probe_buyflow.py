# -*- coding: utf-8 -*-
"""UnitDesignRequest (v102) on an engine page: the 2D studio -> "בנו לי הצעה" -> the request, in a real Chrome through
preview_v101.py (the branch's showroom-engine files over the live page). POST /wp-json/nadlan/v1/lead and /rfp are answered
by rfp_local_endpoint.php (the branch's real nadlan_rfp_create, in memory), never by the site.
  python scripts/project-stage/preview_v101.py "/projects/aurelia/?unit=aur-t-06-a" --w 390 --h 844 --probe scripts/project-stage/probe_buyflow.py
Screenshots and the endpoint state go to $NL_PROBE_SHOTS."""
import json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def run(pg, W, H, mob):
    out = os.environ.get("NL_PROBE_SHOTS", ".")
    state = os.path.join(out, "bf-state-%d.json" % W)
    units = pg.evaluate("() => window.NADLAN_SHOWROOM.projects.aurelia.units.map(u => ({ id: u.id, label: u.label, floor: u.floor, rooms: u.rooms, sqm: u.sqm, dir: u.dir || '' }))")
    uid = re.search(r"unit=([^&]+)", pg.url).group(1)
    seed = {"seq": 900, "inserts": [], "writes": [], "options": {}, "content": {}, "names": {}, "hooks": [], "leads": [], "fail_insert_times": 0,
            "projects": {"aurelia": 201}, "types": {"201": "nadlan_project"}, "meta": {"201": {"project_3d_units": json.dumps(units, ensure_ascii=False)}}}
    json.dump(seed, open(state, "w", encoding="utf-8"), ensure_ascii=False)
    posts = []

    def endpoint(route):
        op = "lead" if route.request.url.endswith("/lead") else "rfp"
        body = route.request.post_data or "{}"
        posts.append({"op": op, "body": json.loads(body)})
        r = subprocess.run(["php", os.path.join(HERE, "rfp_local_endpoint.php"), op, state], input=body, capture_output=True, text=True, encoding="utf-8")
        res = json.loads(r.stdout)
        route.fulfill(status=res["status"], content_type="application/json", body=json.dumps(res["body"], ensure_ascii=False))

    pg.route(re.compile(r"https://nad-lan\.co\.il/wp-json/nadlan/v1/(lead|rfp)$"), endpoint)
    pg.on("dialog", lambda d: d.accept("כורסה ליד החלון (הערת בדיקה)"))
    res = {"unit": uid}

    def open_studio():
        # the engine may still redraw the unit panel after load: the click is repeated until the studio is open
        for _ in range(4):
            sel = '[data-act="studio"][data-id="%s"]' % uid  # this unit's own button (a phone also lists recent units)
            pg.wait_for_selector(sel, timeout=30000)
            pg.locator(sel).first.click()
            try:
                pg.wait_for_selector("#nlst", timeout=4000); pg.wait_for_timeout(400); return
            except Exception:
                pg.wait_for_timeout(800)
        raise RuntimeError("the studio did not open")
    pg.wait_for_timeout(1500)
    open_studio()
    pg.click('#nlst [data-add="sofa3"]'); pg.click('#nlst [data-add="bed_double"]'); pg.wait_for_timeout(200)
    pg.click('#nlst [data-st="rotate"]'); pg.click('#nlst [data-st="note"]'); pg.wait_for_timeout(200)
    pg.fill("#nlst-notes", "פתח רחב יותר לחדר הרחצה (הערת בדיקה)")
    res["reopen"] = "close+reopen" if not mob else "same session (on phones the unit panel closes with the studio)"
    if not mob:
        pg.click('#nlst [data-st="close"]'); pg.wait_for_timeout(300)
    # Codex STUDIO-B2-EXPORT-STALE, in the page: the storage starts refusing this studio's writes; a 3rd item is added
    pg.evaluate("() => { const set = Storage.prototype.setItem; Storage.prototype.setItem = function (k, v) { if (String(k).indexOf('nlstudio:') === 0) throw new Error('QuotaExceededError (test)'); return set.call(this, k, v); }; }")
    if not mob:
        open_studio()
    pg.click('#nlst [data-add="armchair"]'); pg.wait_for_timeout(300)
    res["studio_status"] = pg.evaluate("() => (document.getElementById('nlst-save') || {}).textContent || ''")
    res["redo_button"] = pg.evaluate("() => !!document.querySelector('#nlst [data-st=\"redo\"]')")
    res["plan_h"] = pg.evaluate("() => Math.round(document.getElementById('nlst-plan').getBoundingClientRect().height)")
    pg.screenshot(path=os.path.join(out, "bf-studio-%d.png" % W))
    res["export"] = pg.evaluate("(u) => { const d = window.NLStudio.exportFor('aurelia', u); return d && { items: d.layers.plan2d.items.map(i => i.type), notes: d.notes.map(n => n.text), persisted: d.persisted, rev: d.geometry_revision }; }", uid)
    # the studio's own "attach to my offer request": it closes and opens "בנו לי הצעה" for the same unit
    pg.click('#nlst [data-st="rfp"]'); pg.wait_for_selector("#nlbuy.is-open", timeout=10000); pg.wait_for_timeout(300)
    res["pill_over_dialog"] = pg.evaluate("() => { const b = [...document.querySelectorAll('#nlbuy [data-buy]')].filter(x => x.getBoundingClientRect().height > 0); return b.some(x => { const r = x.getBoundingClientRect(); const e = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return !!(e && e.closest && e.closest('#nlcta')); }); }")
    pg.click('#nlbuy [data-buy="next"]'); pg.wait_for_timeout(150); pg.click('#nlbuy [data-buy="next"]'); pg.wait_for_timeout(150)
    pg.fill("#nlbuy-name", "בדיקה"); pg.fill("#nlbuy-phone", "0500000000")
    st = json.load(open(state, encoding="utf-8")); st["fail_insert_times"] = 1; json.dump(st, open(state, "w", encoding="utf-8"), ensure_ascii=False)
    pg.click("#nlbuy-send")
    pg.wait_for_selector('#nlbuy [data-buy="docretry"]', timeout=20000); pg.wait_for_timeout(300)
    res["doc_failed"] = pg.evaluate("() => ({ text: (document.querySelector('#nlbuy .nlbuy__err[role=alert]') || {}).textContent || '', stage2_on: !!document.querySelector('#nlbuy-stages .nlbuy__stage[data-i=\"1\"].on') })")
    pg.screenshot(path=os.path.join(out, "bf-docfail-%d.png" % W))
    pg.click('#nlbuy [data-buy="docretry"]')
    pg.wait_for_function("() => { const a = document.querySelector('#nlbuy a.nlbuy__btn--accent'); return !!a && /rfp\\//.test(a.href); }", timeout=20000); pg.wait_for_timeout(300)
    pg.screenshot(path=os.path.join(out, "bf-done-%d.png" % W))
    s = json.loads(subprocess.run(["php", os.path.join(HERE, "rfp_local_endpoint.php"), "state", state], input="{}", capture_output=True, text=True, encoding="utf-8").stdout)["body"]
    rf = [x for x in posts if x["op"] == "rfp"]
    doc = s["docs"][0] if s["docs"] else {}
    res["server"] = {"leads": len(s["leads"]), "docs": len(s["docs"]), "lead_posts": len([x for x in posts if x["op"] == "lead"]), "rfp_posts": len(rf),
                     "same_ref": len({x["body"].get("client_ref") for x in rf}) == 1, "same_design": len({json.dumps(x["body"].get("design"), sort_keys=True) for x in rf}) == 1,
                     "doc_unit": (doc.get("unit") or {}).get("id"), "doc_items": [i.get("type") for i in ((doc.get("design") or {}).get("layers", {}).get("plan2d", {}).get("items", []))],
                     "doc_notes": [n.get("text") for n in (doc.get("design") or {}).get("notes", [])], "lead_linked": bool(doc.get("lead_id")),
                     "lead_payload_names_unit": all(x["body"].get("unit") == uid and x["body"].get("project_slug") == "aurelia" for x in posts if x["op"] == "lead")}
    # a double click on send: one lead, one request
    posts.clear()
    # a fresh page with the same unit (on phones the unit panel closes with the dialog)
    pg.reload(wait_until="domcontentloaded"); pg.wait_for_timeout(3500)
    for _ in range(4):
        sel = '[data-act="rfp"][data-id="%s"]' % uid
        pg.wait_for_selector(sel, timeout=30000); pg.locator(sel).first.click()
        try:
            pg.wait_for_selector("#nlbuy.is-open", timeout=4000); break
        except Exception:
            pg.wait_for_timeout(800)
    pg.click('#nlbuy [data-buy="next"]'); pg.click('#nlbuy [data-buy="next"]'); pg.fill("#nlbuy-name", "בדיקה"); pg.fill("#nlbuy-phone", "0500000000")
    pg.evaluate("() => { const b = document.getElementById('nlbuy-send'); b.click(); b.click(); }")
    pg.wait_for_timeout(6000)
    res["double_click"] = {"lead_posts": len([x for x in posts if x["op"] == "lead"]), "rfp_posts": len([x for x in posts if x["op"] == "rfp"])}
    res["checks"] = {
        "stale_export_fixed": res["export"]["items"] == ["sofa3", "bed_double", "armchair"] and res["export"]["persisted"] is False and "פתח רחב" in " ".join(res["export"]["notes"]),
        "save_failure_said": bool(res["studio_status"]) and res["redo_button"],
        "doc_failure_said_no_false_stage": "לא נוצר" in res["doc_failed"]["text"] and not res["doc_failed"]["stage2_on"],
        "one_lead_one_doc_same_ref": res["server"]["leads"] == 1 and res["server"]["docs"] == 1 and res["server"]["lead_posts"] == 1 and res["server"]["rfp_posts"] == 2 and res["server"]["same_ref"] and res["server"]["same_design"],
        "doc_has_the_design": res["server"]["doc_unit"] == uid and res["server"]["doc_items"] == ["sofa3", "bed_double", "armchair"] and len(res["server"]["doc_notes"]) == 2 and res["server"]["lead_linked"] and res["server"]["lead_payload_names_unit"],
        "double_click_once": res["double_click"] == {"lead_posts": 1, "rfp_posts": 1},
        "plan_not_collapsed": res["plan_h"] > 100,
        "pill_not_over_dialog": not res["pill_over_dialog"],
    }
    return res
