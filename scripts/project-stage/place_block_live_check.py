# -*- coding: utf-8 -*-
"""HAD-787 board 24: the questions block at the end of a place page, looked at and pressed as a guest on the LIVE site, at phone
width and on desktop. Nothing is published: the script never presses the sheet's publish button and counts write requests (0).
  python scripts/project-stage/place_block_live_check.py <out dir> [key=label=path ...]"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
BASE = "https://nad-lan.co.il"
PLACES = [a.split("=") for a in sys.argv[2:]] or [["sde-dov", "שדה דב", "/sde-dov/"], ["hamedina", "כיכר המדינה", "/projects/hamedina/"]]
LEDGER = []


def note(step, ok, detail=""):
    LEDGER.append({"step": step, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("PASS " if ok else "FAIL ") + step + ((" | " + str(detail)[:230]) if detail else ""))


with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True)
    for key, label, path in PLACES:
        for name, mobile in (("phone", True), ("desktop", False)):
            tag = "%s %s" % (key, name)
            c = br.new_context(viewport={"width": 390, "height": 844} if mobile else {"width": 1280, "height": 900}, locale="he-IL", is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
            writes = []
            c.on("request", lambda r, w=writes: w.append(r.url) if r.method == "POST" and "/wp-json/nadlan/v1/forum/" in r.url else None)
            g = c.new_page(); g.goto(BASE + path + "?t=%d" % time.time(), wait_until="networkidle", timeout=120000); g.wait_for_timeout(1500)
            i = g.evaluate("""() => { const b = document.querySelector('.nlfpl[data-nlfpl]'); if (!b) return null; const box = b.querySelector('.nlfpl-box'), h2 = b.querySelector('h2'), btn = b.querySelector('form button'), inp = b.querySelector('form input');
                const r = box.getBoundingClientRect(), cs = (e) => getComputedStyle(e); const host = b.closest('.entry-content'); const kids = host ? [...host.children].filter(e => e.getBoundingClientRect().height > 0) : [];
                const arts = [...document.querySelectorAll('.entry-content h2')].filter(e => !b.contains(e)); const lastH2 = arts[arts.length - 1];
                const foot = document.querySelector('footer');
                return { key: b.getAttribute('data-nlfpl'), count: document.querySelectorAll('.nlfpl[data-nlfpl]').length, w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top + scrollY), page: document.documentElement.scrollHeight,
                         pageW: document.documentElement.scrollWidth, vw: innerWidth, h2: h2.textContent, h2font: cs(h2).fontFamily.split(',')[0] + ' ' + cs(h2).fontSize, h1s: document.querySelectorAll('h1').length,
                         btnH: Math.round(btn.getBoundingClientRect().height), inpH: Math.round(inp.getBoundingClientRect().height), placeholder: inp.placeholder, inHost: !!host, lastInHost: kids.length ? kids[kids.length - 1] === b : null,
                         afterLastArticleH2: lastH2 ? lastH2.getBoundingClientRect().top < r.top : null, beforeFooter: foot ? r.bottom + scrollY <= foot.getBoundingClientRect().top + scrollY + 1 : null,
                         none: (b.querySelector('.nlfpl-none') || {}).textContent || '', rows: b.querySelectorAll('.nlfpl-row').length, compose: !!document.getElementById('nlf-compose'), ld: !!b.querySelector('script') }; }""")
            note(tag + ": the block is on the page, once, with Ben's heading", i and i["count"] == 1 and i["key"] == key and i["h2"] == "שאלות של קונים על " + label, i and i["h2"])
            if not i:
                c.close(); continue
            note(tag + ": it sits after the article and before the footer", i["afterLastArticleH2"] and i["beforeFooter"], {k: i[k] for k in ("top", "page", "lastInHost", "afterLastArticleH2", "beforeFooter")})
            note(tag + ": width, heading face, press targets, no sideways scroll, one h1", (i["w"] <= 760 and i["w"] >= (300 if mobile else 700)) and i["h2font"].startswith("Rubik") and i["btnH"] >= 44 and i["inpH"] >= 44 and i["pageW"] <= i["vw"] + 1 and i["h1s"] == 1, {k: i[k] for k in ("w", "h2font", "btnH", "inpH", "pageW", "h1s")})
            note(tag + ": no discussion yet, so it says so and invents nothing", i["rows"] == 0 and "עוד אין שאלות" in i["none"] and not i["ld"], i["none"])
            g.evaluate("() => { const r = document.querySelector('.nlfpl-box').getBoundingClientRect(); window.scrollBy(0, r.top - %d); }" % (260 if mobile else 240)); g.wait_for_timeout(2500)
            g.screenshot(path=os.path.join(OUT, "p1-%s-%s-block.png" % (key, name)))
            # press: type a question, press "לשאול": the forum's own sheet opens with the title and the place line
            q = "בדיקת מראה בלבד, לא נשלח"
            g.locator(".nlfpl form input").fill(q); g.locator(".nlfpl form button").click(); g.wait_for_timeout(1500)
            s = g.evaluate("""() => { const d = document.getElementById('nlf-compose'); if (!d) return null; const f = d.querySelector('form'); return { open: d.open, title: f.elements.title ? f.elements.title.value : '', text: d.innerText.replace(/\\s+/g, ' ').slice(0, 600) }; }""")
            note(tag + ": 'לשאול' opens the forum's sheet with the question and the place line", s and s["open"] and s["title"] == q and label in s["text"], s and s["text"][-200:])
            g.wait_for_timeout(400)
            g.screenshot(path=os.path.join(OUT, "p2-%s-%s-sheet.png" % (key, name)))
            note(tag + ": nothing was sent to the forum", len(writes) == 0, writes[:2])
            c.close()
    # the filtered list and a control page
    c = br.new_context(viewport={"width": 390, "height": 844}, locale="he-IL", is_mobile=True, has_touch=True, device_scale_factor=2)
    g = c.new_page()
    for key, label, path in PLACES:
        g.goto(BASE + "/forum/?place=%s&t=%d" % (key, time.time()), wait_until="networkidle", timeout=90000)
        f = g.evaluate("""() => ({ chip: (document.querySelector('.nlfpl-fchip') || {}).innerText || '', canon: (document.querySelector('link[rel=canonical]') || {}).href || '', title: document.title, robots: (document.querySelector('meta[name=robots]') || {}).content || '' })""")
        note("list filtered by %s: the chip, the canonical stays /forum/, the title has no place name" % key, label in f["chip"] and f["canon"] == BASE + "/forum/" and label not in f["title"], f)
    g.goto(BASE + "/projects/rainbow-tel-aviv/?t=%d" % time.time(), wait_until="domcontentloaded", timeout=90000)
    note("control: another project page has no block", g.locator(".nlfpl").count() == 0)
    c.close(); br.close()
json.dump({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "ledger": LEDGER}, open(os.path.join(OUT, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("RESULT %d/%d" % (sum(1 for x in LEDGER if x["ok"]), len(LEDGER)))
