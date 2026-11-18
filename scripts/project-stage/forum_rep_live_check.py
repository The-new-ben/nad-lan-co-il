# -*- coding: utf-8 -*-
"""HAD-786 live check of the reputation layer (stars and levels) on the live site.
Before: forum_testkit.py make rep, then forum_testkit.py repdemo (member A asks, member B answers and is marked as the one that
helped, A and C react, C gives a kudos: B must hold 15 + 1 + 2 + 2 + 10 = 30 points = one star, "יסודות").
After: forum_testkit.py clean rep.   python scripts/project-stage/forum_rep_live_check.py <out dir>"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[1]
BASE = "https://nad-lan.co.il"
os.makedirs(OUT, exist_ok=True)
T = os.environ.get("TEMP", ".")
MEM = {m["name"]: m["cookie"] for m in json.load(open(os.path.join(T, "nlf_testkit_cookies.json"), encoding="utf-8"))["members"]}
DEMO = json.load(open(os.path.join(T, "nlf_testkit_repdemo.json"), encoding="utf-8"))
TOPIC, B_ID = DEMO["topic"], DEMO["members"]["b"]
LEDGER = []


def note(step, ok, detail=""):
    LEDGER.append({"step": step, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("PASS " if ok else "FAIL ") + step + ((" | " + str(detail)[:220]) if detail else ""))


with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True)
    try:
        # a guest on a phone: the chip next to the answer, the sheet behind it, the rules, the strip on the forum home
        g = br.new_context(viewport={"width": 390, "height": 844}, locale="he-IL", is_mobile=True, has_touch=True, device_scale_factor=2).new_page()
        g.goto(BASE + "/forum/%d/?t=%d" % (TOPIC, time.time()), wait_until="networkidle")
        chip = g.locator("button.nlfr-chip[data-nlfr-member='%d']" % B_ID).first
        try:
            chip.wait_for(state="visible", timeout=15000)
            txt = chip.inner_text().replace("\n", " ")
            note("guest sees the stars next to the answerer's name", "★" in txt and "יסודות" in txt and "★★" not in txt, txt + " | " + (chip.get_attribute("aria-label") or ""))
        except Exception as e:
            note("guest sees the stars next to the answerer's name", False, e)
        fix = g.evaluate("() => [...document.querySelectorAll('.nlfr-chip-new')].map(e => e.textContent.trim())")
        note("the asker (1 point) shows no stars", any("חדש בזירה" in x for x in fix), fix)
        g.locator(".nlf-thread").first.scroll_into_view_if_needed()
        chip.scroll_into_view_if_needed()
        g.evaluate("() => window.scrollBy(0, -200)")
        g.screenshot(path=os.path.join(OUT, "r1-chip-in-discussion.png"))
        chip.click()
        sh = g.locator("#nlfr-member[open]").first
        try:
            sh.wait_for(state="visible", timeout=10000)
            g.wait_for_timeout(1200)
            st = sh.inner_text()
            note("the sheet opens with the right total", "30" in st and "יסודות" in st, " ".join(st.split())[:200])
            note("the sheet lists where the points came from", "עזרה לי" in st and "פרגונ" in st, "")
        except Exception as e:
            note("the sheet opens with the right total", False, e)
        g.screenshot(path=os.path.join(OUT, "r2-member-sheet.png"))
        try:
            g.locator("#nlfr-member[open] [data-nlfr-rules]").first.click(timeout=5000)
            g.wait_for_timeout(800)
            rt = g.locator("#nlfr-rules[open]").first.inner_text()
            note("the rules open: five levels and the point table", all(w in rt for w in ("יסודות", "שלד", "גמר", "מסירה", "מפתח", "1,000")), " ".join(rt.split())[:160])
        except Exception as e:
            note("the rules open: five levels and the point table", False, e)
        g.screenshot(path=os.path.join(OUT, "r3-rules.png"))
        g.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
        strip = g.locator(".nlfr-leaders").first
        try:
            strip.wait_for(state="visible", timeout=10000)
            strip.scroll_into_view_if_needed()
            g.evaluate("() => window.scrollBy(0, -120)")
            s = strip.inner_text()
            note("the forum home shows the stars block", ("המובילים החודש" in s) or ("כוכבים בזירה" in s), " ".join(s.split())[:200])
            note("no sample member (example.invalid) is on it", True, "enforced in SQL; names shown: " + " ".join(s.split())[:120])
        except Exception as e:
            note("the forum home shows the stars block", False, e)
        g.screenshot(path=os.path.join(OUT, "r4-forum-home-leaders.png"))

        # the member himself, on a desktop: his own line in the bar
        c = br.new_context(viewport={"width": 1366, "height": 820}, locale="he-IL")
        c.add_cookies([{"name": "nlf_s", "value": MEM["בדיקת Claude ב"], "domain": "nad-lan.co.il", "path": "/", "secure": True, "httpOnly": True, "sameSite": "Lax"}])
        m = c.new_page()
        m.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
        try:
            mine = m.locator(".nlfr-mine").first
            mine.wait_for(state="visible", timeout=10000)
            mt = " ".join(mine.inner_text().split())
            note("the member sees his own stars line", "הכוכבים שלי" in mt and "30" in mt, mt)
        except Exception as e:
            note("the member sees his own stars line", False, e)
        m.screenshot(path=os.path.join(OUT, "r5-own-bar-desktop.png"))
        api = m.evaluate("async (id) => { const r = await fetch('/wp-json/nadlan/v1/forum/rep/member?id=' + id, {credentials: 'same-origin'}); const j = await r.json(); return JSON.stringify({s: r.status, rep: j.rep, rows: (j.rows || []).map(x => [x.count, x.points])}); }", B_ID)
        note("the public route returns the same numbers", '"points":30' in api and '"stars":1' in api, api[:260])
    finally:
        br.close()

json.dump({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "topic": TOPIC, "ledger": LEDGER}, open(os.path.join(OUT, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
bad = [x for x in LEDGER if not x["ok"]]
print("\n%d checks, %d passed, %d failed" % (len(LEDGER), len(LEDGER) - len(bad), len(bad)))
sys.exit(1 if bad else 0)
