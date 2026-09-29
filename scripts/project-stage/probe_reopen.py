# -*- coding: utf-8 -*-
"""Codex's open regression (29.9): on an engine page, WITHOUT a reload,
  (a) the studio: open -> close -> is the same unit still selected, and can its studio be opened again?
  (b) "בנו לי הצעה": open -> Escape -> the same unit still selected, and can the dialog be opened again?
Each state records the URL, the selected unit's card (its buttons visible), the focus and the open overlays.
  python scripts/project-stage/preview_v101.py "/projects/aurelia/?unit=aur-t-06-a" --w 390 --h 844 --probe scripts/project-stage/probe_reopen.py"""
import os, re


def run(pg, W, H, mob):
    out = os.environ.get("NL_PROBE_SHOTS", ".")
    uid = re.search(r"unit=([^&]+)", pg.url).group(1)
    S = '[data-act="studio"][data-id="%s"]' % uid
    B = '[data-act="rfp"][data-id="%s"]' % uid
    snap_js = """([S, B]) => {
      const vis = (sel) => { const e = document.querySelector(sel); if (!e) return 'absent'; const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
        return (r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none') ? 'visible' : 'hidden'; };
      const a = document.activeElement;
      return { url: location.search.replace(/[?&]pv101=\\d+/, ''), studio_btn: vis(S), rfp_btn: vis(B), studio_open: !!document.getElementById('nlst'),
        dialog_open: !!document.querySelector('#nlbuy.is-open'), focus: a ? (a.id ? '#' + a.id : a.tagName.toLowerCase() + (a.className && typeof a.className === 'string' ? '.' + a.className.split(' ')[0] : '')) : null }; }"""
    snap = lambda: pg.evaluate(snap_js, [S, B])
    res = {"unit": uid, "width": W}
    pg.wait_for_timeout(1500)
    pg.wait_for_selector(S, timeout=30000)
    res["0_loaded"] = snap()
    only_b = os.environ.get("NL_REOPEN_ONLY") == "b"  # (b) alone, on a fresh page
    # (a) the studio
    for _ in range(0 if only_b else 4):
        pg.locator(S).first.click()
        try:
            pg.wait_for_selector("#nlst", timeout=4000); break
        except Exception:
            pg.wait_for_timeout(800)
    reopened = False
    if not only_b:
        res["a1_studio_open"] = snap()
        pg.click('#nlst [data-st="close"]'); pg.wait_for_timeout(600)
        res["a2_after_close"] = snap()
        pg.screenshot(path=os.path.join(out, "reopen-a-%d.png" % W))
    if not only_b and res["a2_after_close"]["studio_btn"] == "visible":
        pg.locator(S).first.click(); pg.wait_for_timeout(1200); reopened = bool(pg.evaluate("() => !!document.getElementById('nlst')"))
        if reopened:
            pg.click('#nlst [data-st="close"]'); pg.wait_for_timeout(500)
    res["a3_reopened_without_reload"] = reopened
    # (b) the dialog and Escape
    pg.wait_for_timeout(300)
    if snap()["rfp_btn"] == "visible":
        pg.locator(B).first.click(); pg.wait_for_timeout(700)
        res["b1_dialog_open"] = snap()
        pg.keyboard.press("Escape"); pg.wait_for_timeout(600)
        res["b2_after_escape"] = snap()
        pg.screenshot(path=os.path.join(out, "reopen-b-%d.png" % W))
        again = False
        if res["b2_after_escape"]["rfp_btn"] == "visible":
            pg.locator(B).first.click(); pg.wait_for_timeout(800); again = bool(pg.evaluate("() => !!document.querySelector('#nlbuy.is-open')"))
        res["b3_reopened_without_reload"] = again
    else:
        res["b1_dialog_open"] = "the unit's request button was not visible after (a)"
    res["checks"] = {} if only_b else {
        "studio_close_keeps_unit": res["a2_after_close"]["studio_btn"] == "visible" and ("unit=" + uid) in res["a2_after_close"]["url"],
        "studio_reopens": res["a3_reopened_without_reload"]}
    res["checks"].update({
        "escape_keeps_unit": isinstance(res.get("b2_after_escape"), dict) and res["b2_after_escape"]["rfp_btn"] == "visible" and not res["b2_after_escape"]["dialog_open"],
        "dialog_reopens": bool(res.get("b3_reopened_without_reload")),
    })
    return res
