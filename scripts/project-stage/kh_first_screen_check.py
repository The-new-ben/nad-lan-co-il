# -*- coding: utf-8 -*-
"""The phone's first screen on the five Kikar Hamedina pages (design system v104.1, P9a): READ-ONLY public GETs in a real Chrome
(Playwright), 390x844 at 2x with a phone's user agent. At scroll 0, 300 and 700 px it measures, with getBoundingClientRect, the
site's WhatsApp bar (#nlcta .nlcta-wa) against the page top's three buttons (.nlps-hero__cta) and the world's tab bar (the four
tabs and the full-screen button), and reports every overlap in px². Nothing is clicked, nothing is sent (WhatsApp and analytics are
blocked), nothing is written but the shots and the JSON in --out.

  python scripts/project-stage/kh_first_screen_check.py [--base https://nad-lan.co.il] [--out DIR] [--langs he,en,fr,ru,ar]

Exit 1 when the bar covers a button or a tab anywhere; 0 when the five pages are clean. Run it after release 1.72.371 (the
runner prints the reminder), and as the "before" on any page top change.
"""
import argparse, io, json, os, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

MEASURE = r"""() => {
  const R = (e) => { if (!e) return null; const r = e.getBoundingClientRect(); if (!r.height) return null; return { l: Math.round(r.left), r: Math.round(r.right), t: Math.round(r.top), b: Math.round(r.bottom) }; };
  const pill = R(document.querySelector('#nlcta .nlcta-wa'));
  const btns = [...document.querySelectorAll('.nlps-hero__cta a, .nlps-hero__cta button')].map((e) => ({ ev: e.getAttribute('data-nlps-ev'), ...R(e) }));
  const tabs = [...document.querySelectorAll('#nlps .nlw-top .nlw-tab, #nlps .nlw-fullbtn')].map((e) => ({ txt: e.textContent.trim().slice(0, 24) || 'full', ...R(e) }));
  const ov = (a, b) => (a && b && b.t != null ? Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t)) : 0);
  const hits = [];
  for (const b of btns) { const o = ov(pill, b); if (o > 0) hits.push({ with: 'hero:' + b.ev, px2: o }); }
  for (const t of tabs) { const o = ov(pill, t); if (o > 0) hits.push({ with: 'tab:' + t.txt, px2: o }); }
  const box = document.getElementById('nlcta');
  return { y: Math.round(scrollY), vh: innerHeight, pill, lift: box && box.style.getPropertyValue('--nlcta-lift'), cls: box && box.className, btns, tabs, hits };
}"""
PAGES = {"he": "/projects/hamedina/", "en": "/projects/hamedina-en/", "fr": "/projects/hamedina-fr/", "ru": "/projects/hamedina-ru/", "ar": "/projects/hamedina-ar/"}
UA = "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Mobile Safari/537.36"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://nad-lan.co.il")
    ap.add_argument("--out", default=os.path.join(os.environ.get("TEMP", "."), "kh-first-screen"))
    ap.add_argument("--langs", default="he,en,fr,ru,ar")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    res, bad = {}, 0
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        for lang in a.langs.split(","):
            ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=UA)
            ctx.route("**/*", lambda r: r.abort() if any(x in r.request.url for x in ("google-analytics", "googletagmanager", "facebook", "clarity", "hotjar", "wa.me", "doubleclick")) or r.request.method != "GET" else r.fallback())
            pg = ctx.new_page()
            pg.goto(a.base + PAGES[lang] + "?fs=%d" % time.time(), wait_until="load", timeout=120000)
            pg.wait_for_timeout(2500)
            rows = []
            for y in (0, 300, 700):
                pg.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})")
                pg.wait_for_timeout(1000)
                m = pg.evaluate(MEASURE)
                rows.append(m)
                pg.screenshot(path=os.path.join(a.out, f"{lang}-390-y{y}.png"))
                bad += len(m["hits"])
                print(f"{lang} y={m['y']:>4} pill={m['pill']} lift={m['lift'] or '-'} {'OK' if not m['hits'] else 'HITS ' + json.dumps(m['hits'], ensure_ascii=False)}")
            res[lang] = rows
            ctx.close()
        b.close()
    io.open(os.path.join(a.out, "first-screen.json"), "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
    print("RESULT", "OK: the bar covers no button and no tab" if not bad else f"{bad} overlap(s)", "| shots and JSON in", a.out)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
