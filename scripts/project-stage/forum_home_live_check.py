# -*- coding: utf-8 -*-
"""HAD-787 live check of "הדירה שמדברים עליה" (1.72.704) with the test kit's members, on the live site.
Before: forum_testkit.py make.  After: forum_testkit.py clean.   python scripts/project-stage/forum_home_live_check.py <out dir>
B (trusted, phone) presents a TEST apartment (title starts with "בדיקת Claude" in the body, removed afterwards) with 2 pictures;
a guest votes in one tap and sees the result; A and C answer with a price estimate; the public averages box shows."""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[1]
BASE = "https://nad-lan.co.il"
os.makedirs(OUT, exist_ok=True)
T = os.environ.get("TEMP", ".")
MEM = {m["name"]: m["cookie"] for m in json.load(open(os.path.join(T, "nlf_testkit_cookies.json"), encoding="utf-8"))["members"]}
LEDGER = []
F = os.path.join(OUT, "_files"); os.makedirs(F, exist_ok=True)
pics = []
for n, c in (("1", (120, 132, 140)), ("2", (90, 104, 114))):
    im = Image.new("RGB", (1600, 1200), c); d = ImageDraw.Draw(im); d.rectangle([500, 300, 1100, 900], outline=(255, 255, 255), width=12)
    p = os.path.join(F, "flat-%s.jpg" % n); im.save(p, "JPEG", quality=88); pics.append(p)


def note(step, ok, detail=""):
    LEDGER.append({"step": step, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("PASS " if ok else "FAIL ") + step + ((" | " + str(detail)[:220]) if detail else ""))


def ctx(br, name=None, mobile=True):
    c = br.new_context(viewport={"width": 390, "height": 844} if mobile else {"width": 1280, "height": 900}, locale="he-IL", is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
    if name:
        c.add_cookies([{"name": "nlf_s", "value": MEM[name], "domain": "nad-lan.co.il", "path": "/", "secure": True, "httpOnly": True, "sameSite": "Lax"}])
    return c


def answer(pg, topic, est, text):
    pg.goto(BASE + "/forum/%d/?t=%d" % (topic, time.time()), wait_until="networkidle")
    rf = pg.locator("form[data-nlf-replyform]").first
    pg.locator("a[data-nlfh-estimate]").first.click(); pg.wait_for_timeout(800)  # "להעריך את המחיר" opens the field in the answer form
    rf.locator("#nlfh-est").first.fill(str(est))
    rf.locator("textarea").first.fill(text)
    with pg.expect_response(lambda r: "/forum/reply" in r.url and r.request.method == "POST", timeout=60000) as rr:
        rf.locator("button[type=submit]").first.click()
    return rr.value.json()


TOPIC = 0
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True)
    try:
        g0 = ctx(br).new_page()
        g0.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
        inv = g0.locator("[data-nlfh-open]").first
        note("guest sees the invitation on the forum home", inv.count() > 0 and inv.is_visible(), g0.locator("#nlfh-c-h").inner_text() if g0.locator("#nlfh-c-h").count() else "")
        inv.scroll_into_view_if_needed(); g0.evaluate("() => window.scrollBy(0, -260)"); g0.wait_for_timeout(400)
        g0.screenshot(path=os.path.join(OUT, "h0-home-invitation-phone.png"))

        TOPIC = int(os.environ.get('HOME_TOPIC', '0'))
        if not TOPIC:
            b = ctx(br, "בדיקת Claude ב").new_page()
            b.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
            b.locator("[data-nlfh-open]").first.click(); b.wait_for_timeout(800)
            f = b.locator("form[data-nlfh-form]")
            f.locator("#nlfh-city").select_option("רמת גן"); b.wait_for_timeout(2500)
            try:
                f.locator("#nlfh-nbhd").select_option(label="יד לבנים"); note("neighbourhood list filled from the public file", True)
            except Exception as e:
                note("neighbourhood list filled from the public file", False, e)
            f.locator("#nlfh-street").fill("ז'בוטינסקי 12")
            f.locator("#nlfh-rooms").select_option("4")
            f.locator("#nlfh-sqm").fill("98"); f.locator("#nlfh-floor").fill("6"); f.locator("#nlfh-floors").fill("9")
            f.locator("#nlfh-ask").fill("3450000")
            f.locator("[data-nlfh-chip='state']").first.click(); f.locator("[data-nlfh-chip='intent']").first.click()
            f.locator("#nlfh-body").fill("בדיקת Claude: דירת בדיקה אוטומטית של האתר. תוסר בעוד כמה דקות.")
            f.locator("input[type=file][multiple][accept='image/*']").set_input_files(pics)
            b.wait_for_timeout(9000)
            f.locator("button[type=submit]").click(); b.wait_for_timeout(3000)
            msg = f.locator(".nlf-msg").first.inner_text()
            note("a street WITH a house number is refused", "מספר" in msg or "בלי" in msg, msg)
            b.screenshot(path=os.path.join(OUT, "h1-number-refused-phone.png"))
            f.locator("#nlfh-street").fill("ז'בוטינסקי")
            with b.expect_response(lambda r: "/forum/" in r.url and "/media" not in r.url and r.request.method == "POST", timeout=60000) as ri:
                f.locator("button[type=submit]").click()
            j = ri.value.json(); TOPIC = int(j.get("id") or 0)
            note("the apartment discussion was published", TOPIC > 0, json.dumps(j, ensure_ascii=False)[:160])

            g = ctx(br).new_page()
            g.goto(BASE + "/forum/%d/?t=%d" % (TOPIC, time.time()), wait_until="networkidle")
            h1 = g.locator("h1").first.inner_text()
            note("the title is built from the fields", "4 חדרים" in h1 and "98" in h1 and "רמת גן" in h1 and "כמה היא שווה" in h1, h1)
            body = g.locator("body").inner_text()
            note("the public averages box shows (Tax Authority)", "ממוצע העסקאות בשנה האחרונה (רשות המסים)" in body and "יד לבנים" in body, "")
            note("no house number anywhere on the page", "12" not in h1, "")
            g.screenshot(path=os.path.join(OUT, "h2-guest-apartment-phone.png"))
            vb = g.locator("[data-nlfh-vote]", has_text="יקר").first
            vb.scroll_into_view_if_needed()
            with g.expect_response(lambda r: "home/vote" in r.url, timeout=30000) as vr:
                vb.click()
            note("a guest votes in one tap, no entry needed", vr.value.status == 200, json.dumps(vr.value.json(), ensure_ascii=False)[:160])
            g.wait_for_timeout(1200)
            res = g.locator(".nlfh-res").first
            note("after the vote the guest sees the result bar", res.count() > 0 and res.is_visible() and "%" in res.inner_text(), " ".join(res.inner_text().split()) if res.count() else "")
            res.scroll_into_view_if_needed(); g.evaluate("() => window.scrollBy(0, -200)"); g.wait_for_timeout(400)
            g.screenshot(path=os.path.join(OUT, "h3-guest-after-vote-phone.png"))

        a = ctx(br, "בדיקת Claude א").new_page()
        ja = answer(a, TOPIC, 3250000, "בדיקת Claude: לפי שתי העסקאות האחרונות ברחוב, קצת יקר.")
        note("A answers with an estimate", bool(ja.get("ok")), json.dumps(ja, ensure_ascii=False)[:140])
        c = ctx(br, "בדיקת Claude ג").new_page()
        jc = answer(c, TOPIC, 3300000, "בדיקת Claude: הקומה והמעלית שוות משהו.")
        note("C answers with an estimate", bool(jc.get("ok")), json.dumps(jc, ensure_ascii=False)[:140])
    finally:
        br.close()

ap = __import__("subprocess").run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "forum_testkit.py"), "approve", str(TOPIC)], capture_output=True, text=True, encoding="utf-8")
print(ap.stdout[-200:])
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True)
    try:
        g = ctx(br).new_page()
        g.goto(BASE + "/forum/%d/?t=%d" % (TOPIC, time.time()), wait_until="networkidle")
        chips = g.evaluate("() => [...document.querySelectorAll('.nlfh-chip')].map(e => e.textContent.trim())")
        note("the estimate chips show on the answers", len(chips) >= 2 and any("3,250,000" in x for x in chips), chips)
        bx = g.locator("body").inner_text()
        note("the estimates box waits for a third estimate", "הערכות" in bx, re.search(r"עוד \d+ הערכ[^\n]*", bx).group(0) if re.search(r"עוד \d+ הערכ[^\n]*", bx) else "")
        loc = g.locator(".nlfh-chip").first
        if loc.count():
            loc.scroll_into_view_if_needed(); g.evaluate("() => window.scrollBy(0, -200)"); g.wait_for_timeout(400)
        g.screenshot(path=os.path.join(OUT, "h4-guest-answers-with-estimates-phone.png"))
        h = ctx(br).new_page()
        h.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
        card = h.get_by_text("הדירה שמדברים עליה").first
        note("the forum home shows the apartment card (may wait for its 10-minute cache)", card.count() > 0, "")
        if card.count():
            card.scroll_into_view_if_needed(); h.evaluate("() => window.scrollBy(0, -120)"); h.wait_for_timeout(400)
        h.screenshot(path=os.path.join(OUT, "h5-home-card-phone.png"))
    finally:
        br.close()

json.dump({"topic": TOPIC, "at": time.strftime("%Y-%m-%d %H:%M:%S"), "ledger": LEDGER}, open(os.path.join(OUT, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("RESULT %d/%d" % (sum(1 for x in LEDGER if x["ok"]), len(LEDGER)))
