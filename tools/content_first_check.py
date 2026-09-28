# -*- coding: utf-8 -*-
"""Content first, checked where it counts: in the RENDERED page (docs/checklists/PROJECT-PAGE-CHECKLIST.md, rules C3-C4).

Google indexes the phone version. On 25.9.2026 the answer paragraph stayed first in the source while a phone showed it at
2,400px, below the stage, the view and the map, and no check saw it. This one loads each project page like Google's phone
crawler (412x915, a mobile Googlebot user agent) and like a desktop (1440x900) and asserts:
  C3  the answer paragraph (.nl-lead) starts above the stage (#nlps); on the phone within 1.2 screens, on desktop
      within the first screen
  C4  the stage starts within 1.5 screens on the phone (it follows the paragraph at once, never pushed to the end)
Pages without a stage only need the paragraph within the first 1.2 screens.

  python tools/content_first_check.py [url ...]      (default: the project pages with a stage, and two without)
Exit code 1 when any page fails. Read-only: it only loads public pages.
"""
import json, sys, time

PAGES = [
    "https://nad-lan.co.il/projects/rainbow-tel-aviv/",
    "https://nad-lan.co.il/projects/h-infinity-somail-tel-aviv/",
    "https://nad-lan.co.il/projects/dimri-yama-sde-dov/",
    "https://nad-lan.co.il/projects/duo-tel-aviv/",
    "https://nad-lan.co.il/projects/ashira-sde-dov/",
]
GOOGLEBOT_PHONE = ("Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/126.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
PROBE = """(() => { const R = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect();
  return r.height ? Math.round(r.top + scrollY) : null; };
  const X = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return [r.left, r.right]; };
  const a = X('.nl-lead'), b = X('#nlps');
  // stacked: the paragraph and the stage share columns (a phone); side by side (a desktop's first fold) they do not
  const stacked = !!(a && b && Math.min(a[1], b[1]) - Math.max(a[0], b[0]) > 40);
  const h1 = document.querySelector('h1'); const h1hidden = !!(h1 && (h1.getBoundingClientRect().height <= 2 || /screen-reader-text|sr-only/.test(h1.className)));
  return { h1: R('h1'), h1hidden, lead: R('.nl-lead'), stage: R('#nlps'), stacked, vh: innerHeight }; })()"""


def main(urls):
    from playwright.sync_api import sync_playwright
    bad = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        for name, vp, mob, ua, lead_max, stage_max in (
                ("phone", {"width": 412, "height": 915}, True, GOOGLEBOT_PHONE, 1.2, 1.5),
                ("desktop", {"width": 1440, "height": 900}, False, None, 1.0, 1.0)):
            ctx = b.new_context(viewport=vp, is_mobile=mob, has_touch=mob, **({"user_agent": ua} if ua else {}))
            for url in urls:
                pg = ctx.new_page()
                pg.goto(url + ("&" if "?" in url else "?") + "cfc=%d" % time.time(), wait_until="load", timeout=120000)
                time.sleep(2)
                r = pg.evaluate(PROBE)
                pg.close()
                vh = r["vh"]
                why = []
                if r["lead"] is None:
                    why.append("no answer paragraph (.nl-lead)")
                else:
                    if r["lead"] > lead_max * vh:
                        why.append(f"paragraph at {r['lead']}px, past {lead_max} screens")
                    if r["stage"] is not None and r["stacked"] and r["lead"] > r["stage"]:
                        why.append(f"paragraph ({r['lead']}px) below the stage ({r['stage']}px)")
                if r["stage"] is not None and r["stage"] > stage_max * vh:
                    why.append(f"stage at {r['stage']}px, past {stage_max} screens")
                if r.get("h1hidden"):
                    print(f"[WARN] {name:7s} {url}  the H1 is hidden (screen readers only); the checklist's C1 wants it visible (Linear: fleet H1)")
                ok = not why
                print(f"[{'OK ' if ok else 'BAD'}] {name:7s} {url}  h1 {r['h1']} lead {r['lead']} stage {r['stage']}" + ("" if ok else "  <- " + "; ".join(why)))
                if not ok:
                    bad.append((name, url, why))
            ctx.close()
        b.close()
    return bad


if __name__ == "__main__":
    bad = main([a for a in sys.argv[1:] if a.startswith("http")] or PAGES)
    print(json.dumps({"failed": len(bad)}))
    sys.exit(1 if bad else 0)
