# -*- coding: utf-8 -*-
"""The phone's first screen on the five Kikar Hamedina pages (design system v104.1, P9a; extended for v104.2, P9c): READ-ONLY
public GETs in a real Chrome (Playwright), 390x844 at 2x with a phone's user agent. At scroll 0, 300 and 700 px it measures, with
getBoundingClientRect:
  - the site's WhatsApp bar (#nlcta .nlcta-wa) against the page top's three buttons (.nlps-hero__cta) and the world's tab bar (the
    four tabs and the full-screen button): an overlap is a FAIL (v104.1);
  - P9c, the answer paragraph (.nl-lead): the bar must never be LIFTED onto it. At its resting place the bar floats over whatever
    scrolls under it (the paragraph moves up from under it as one reads, like any page's text): that is reported, px² and the
    lines' share, but it is not a failure. Once the bar leaves its resting place to clear a button (--nlcta-lift is set), the
    place it takes must be clear of the paragraph too: an overlap there is a FAIL (the Arabic first screen of 1.72.371);
  - P9c, the accessibility button (#nla11y-btn) against the world's tabs and the page top's buttons: on a world tab it is a FAIL
    (v104.2's AccessibleCorner); on a page-top button it is reported (it stays in its corner when the only free place above is
    the answer paragraph).
Nothing is clicked, nothing is sent (WhatsApp and analytics are blocked), nothing is written but the shots and the JSON in --out.

  python scripts/project-stage/kh_first_screen_check.py [--base https://nad-lan.co.il] [--out DIR] [--langs he,en,fr,ru,ar]

Exit 1 on any FAIL; 0 when the five pages are clean. Run it after a release that touches the page top (the runner prints the
reminder), and as the "before" on any page top change. preview_hamedina.py --p9c runs the same MEASURE on the local release copy.
"""
import argparse, io, json, os, sys, time
if hasattr(sys.stdout, "reconfigure"):  # (not a new wrapper: preview_hamedina.py imports this module, and a second wrapper closes the first)
    sys.stdout.reconfigure(encoding="utf-8")

MEASURE = r"""() => {
  const R = (e) => { if (!e) return null; const r = e.getBoundingClientRect(); if (!r.height) return null; return { l: Math.round(r.left), r: Math.round(r.right), t: Math.round(r.top), b: Math.round(r.bottom) }; };
  const pill = R(document.querySelector('#nlcta .nlcta-wa'));
  const btns = [...document.querySelectorAll('.nlps-hero__cta a, .nlps-hero__cta button')].map((e) => ({ ev: e.getAttribute('data-nlps-ev'), ...R(e) }));
  const tabs = [...document.querySelectorAll('#nlps .nlw-top .nlw-tab, #nlps .nlw-fullbtn')].map((e) => ({ txt: e.textContent.trim().slice(0, 24) || 'full', ...R(e) }));
  const lead = R(document.querySelector('.nl-lead'));
  const a11y = R(document.querySelector('#nla11y-btn'));
  const ov = (a, b) => (a && b && b.t != null ? Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t)) : 0);
  const hits = [];
  for (const b of btns) { const o = ov(pill, b); if (o > 0) hits.push({ with: 'hero:' + b.ev, px2: o }); }
  for (const t of tabs) { const o = ov(pill, t); if (o > 0) hits.push({ with: 'tab:' + t.txt, px2: o }); }
  const box = document.getElementById('nlcta');
  const lift = (box && box.style.getPropertyValue('--nlcta-lift')) || '';
  const lifted = !!lift && parseFloat(lift) > 0;
  const leadPx2 = ov(pill, lead);
  const a11yHits = [];
  for (const b of btns) { const o = ov(a11y, b); if (o > 0) a11yHits.push({ with: 'hero:' + b.ev, px2: o }); }
  for (const t of tabs) { const o = ov(a11y, t); if (o > 0) a11yHits.push({ with: 'tab:' + t.txt, px2: o }); }
  const a11yLift = (document.getElementById('nla11y') || { style: {} }).style.transform || '';
  return { y: Math.round(scrollY), vh: innerHeight, pill, lift, lifted, lead, leadPx2, leadLifted: lifted && leadPx2 > 0, leadAtRest: !lifted && leadPx2 > 0,
           a11y, a11yLift, a11yHits, cls: box && box.className, btns, tabs, hits };
}"""
PAGES = {"he": "/projects/hamedina/", "en": "/projects/hamedina-en/", "fr": "/projects/hamedina-fr/", "ru": "/projects/hamedina-ru/", "ar": "/projects/hamedina-ar/"}
UA = "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Mobile Safari/537.36"


def verdict(m):
    """(fails, notes) for one measure: FAIL = the bar on a control, the bar lifted onto the answer paragraph, the a11y button on a tab"""
    fails = [h["with"] for h in m["hits"]]
    if m.get("leadLifted"):
        fails.append(f"bar lifted onto the lead ({m['leadPx2']} px²)")
    fails += ["a11y on " + h["with"] for h in m.get("a11yHits", []) if h["with"].startswith("tab:")]
    notes = []
    if m.get("leadAtRest"):
        notes.append(f"bar at rest over the lead's lower lines ({m['leadPx2']} px², the text scrolls from under it)")
    notes += ["a11y at rest on " + h["with"] for h in m.get("a11yHits", []) if not h["with"].startswith("tab:")]
    return fails, notes


def line(lang, m):
    fails, notes = verdict(m)
    return (f"{lang} y={m['y']:>4} pill={m['pill']} lift={m['lift'] or '-'} a11y={m['a11y'] and (m['a11y']['t'], m['a11y']['b'])}{' ' + m['a11yLift'] if m.get('a11yLift') else ''} "
            + ("OK" if not fails else "FAIL " + json.dumps(fails, ensure_ascii=False)) + (" | " + "; ".join(notes) if notes else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://nad-lan.co.il")
    ap.add_argument("--out", default=os.path.join(os.environ.get("TEMP", "."), "kh-first-screen"))
    ap.add_argument("--langs", default="he,en,fr,ru,ar")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    res, bad, info = {}, 0, 0
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        for lang in a.langs.split(","):
            ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=UA)
            ctx.route("**/*", lambda r: r.abort() if any(x in r.request.url for x in ("google-analytics", "googletagmanager", "facebook", "clarity", "hotjar", "wa.me", "doubleclick")) or r.request.method != "GET" else r.fallback())
            pg = ctx.new_page()
            pg.goto(a.base + PAGES[lang] + "?fs=%d" % time.time(), wait_until="load", timeout=120000)
            pg.wait_for_timeout(3500)
            rows = []
            for y in (0, 300, 700):
                pg.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})")
                pg.wait_for_timeout(1000)
                m = pg.evaluate(MEASURE)
                rows.append(m)
                pg.screenshot(path=os.path.join(a.out, f"{lang}-390-y{y}.png"))
                f, n = verdict(m)
                bad += len(f)
                info += len(n)
                print(line(lang, m))
            res[lang] = rows
            ctx.close()
        b.close()
    io.open(os.path.join(a.out, "first-screen.json"), "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
    print("RESULT", ("OK: the bar covers no button and no tab, is never lifted onto the answer paragraph, and the accessibility button "
                     "sits on no tab") if not bad else f"{bad} FAIL(s)", f"| {info} note(s) (at rest)", "| shots and JSON in", a.out)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
