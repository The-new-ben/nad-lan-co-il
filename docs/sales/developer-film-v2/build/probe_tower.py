"""Where is the tower on a full-viewport stage? Hover a grid and read the stage's own floor label (read-only)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from live_common import *
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; W, H = int(sys.argv[2]), int(sys.argv[3])
with sync_playwright() as p:
    b, ctx = launch(p, W, H)
    pg = ctx.new_page()
    pg.goto("https://nad-lan.co.il/projects/rainbow-tel-aviv/", wait_until="domcontentloaded", timeout=120000)
    pg.evaluate(EVENTS_JS)
    pg.wait_for_selector("section#nlps")
    pg.evaluate("() => document.querySelector('section#nlps').scrollIntoView({block:'center'})")
    pg.add_style_tag(content=CSS_STAGE)
    pg.wait_for_timeout(12000)
    pg.screenshot(path=os.path.join(OUT, f"tower_{W}x{H}_hero.png"))
    hits = []
    for x in range(int(W*0.3), int(W*0.7), W//40):
        for y in range(int(H*0.1), int(H*0.9), H//30):
            pg.mouse.move(x, y); pg.wait_for_timeout(60)
            lab = pg.evaluate("() => { const l = document.querySelector('section#nlps .rbs-label'); if (!l) return null; const cs = getComputedStyle(l); return (cs.display!=='none' && cs.visibility!=='hidden' && +cs.opacity>0.1) ? l.innerText.trim().split(String.fromCharCode(10))[0] : null; }")
            if lab: hits.append([x, y, lab])
    json.dump(hits, open(os.path.join(OUT, f"tower_{W}x{H}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(len(hits)); print(hits[:5], hits[-5:])
    b.close()
