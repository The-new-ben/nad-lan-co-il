# -*- coding: utf-8 -*-
"""HAD-787 live check of the chat inside the forum video room (1.72.703), with the test kit's members, on the live site.
Before: forum_testkit.py make.  After: forum_testkit.py clean.   python scripts/project-stage/forum_chat_live_check.py <out dir>
B (trusted, phone) opens a test discussion and its room; A (desktop) joins from the link; they chat, react and pin; C (phone)
joins late and must see the history; B leaves and attaches "מה סוכם בשיחה" to the discussion; a guest sees that answer."""
import json, os, re, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[1]
BASE = "https://nad-lan.co.il"
os.makedirs(OUT, exist_ok=True)
T = os.environ.get("TEMP", ".")
MEM = {m["name"]: m["cookie"] for m in json.load(open(os.path.join(T, "nlf_testkit_cookies.json"), encoding="utf-8"))["members"]}
LEDGER = []
CHAT = "button.nlfc-c:has(small:text-is(\"צ'אט\")):visible"


def note(step, ok, detail=""):
    LEDGER.append({"step": step, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("PASS " if ok else "FAIL ") + step + ((" | " + str(detail)[:200]) if detail else ""))


def ctx(br, w, h, name=None, mobile=False):
    c = br.new_context(viewport={"width": w, "height": h}, locale="he-IL", is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1, permissions=["camera", "microphone"])
    if name:
        c.add_cookies([{"name": "nlf_s", "value": MEM[name], "domain": "nad-lan.co.il", "path": "/", "secure": True, "httpOnly": True, "sameSite": "Lax"}])
    return c


def shot(pg, n):
    pg.screenshot(path=os.path.join(OUT, n + ".png"))


def enter(pg, label):
    pg.locator(".nlfc-sheet").wait_for(state="visible", timeout=15000)
    for sw in pg.locator(".nlfc-sheet .nlfc-swin").all():
        sw.check(force=True)
    pg.wait_for_timeout(1000)
    pg.locator(".nlfc-sheet .nlfc-pri").click()
    try:
        pg.locator(".nlfc-stage").wait_for(state="visible", timeout=40000)
    except Exception:
        shot(pg, "x-enter-failed-" + label.split()[0])
        print("SHEET:", " ".join(pg.locator("body").inner_text().split())[-300:])
        raise
    note(label + " entered the room", True)


def close_sheets(pg):
    for _ in range(2):
        try:
            pg.locator(".nlfc-sheet .nlfc-x").first.click(timeout=2000); pg.wait_for_timeout(400)
        except Exception:
            break


def send(pg, text):
    pg.locator(".nlfch-in").first.fill(text)
    pg.locator(".nlfch-send").first.click()
    pg.wait_for_timeout(1500)


TOPIC = 0
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream", "--autoplay-policy=no-user-gesture-required"])
    try:
        # B opens a test discussion
        b = ctx(br, 390, 844, "בדיקת Claude ב", True).new_page()
        TOPIC = int(os.environ.get("CHAT_TOPIC", "0"))
        if not TOPIC:
            b.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
            b.evaluate("() => document.getElementById('nlf-compose').showModal()")
            f = b.locator("form[data-nlf-composeform]")
            f.locator("#nlf-c-title").fill("בדיקת Claude: צ'אט בחדר הווידאו")
            f.locator("#nlf-c-body").fill("דיון בדיקה אוטומטי של האתר. יוסר בעוד כמה דקות.")
            b.wait_for_timeout(600)
            with b.expect_response(lambda r: "/forum/topic" in r.url and r.request.method == "POST", timeout=60000) as ri:
                f.locator("button[type=submit]").click()
            TOPIC = int(ri.value.json().get("id") or 0)
        note("test discussion published", TOPIC > 0, TOPIC)

        # B opens its room, gets the link
        b.goto(BASE + "/forum/%d/?t=%d" % (TOPIC, time.time()), wait_until="networkidle")
        b.locator("[data-nlf-room]").first.click()
        enter(b, "B (host, phone)")
        b.wait_for_timeout(2000)
        link = b.evaluate("""() => { const i = [...document.querySelectorAll('.nlfc-sheet input, .nlfc-stage input')].find(x => /#call=/.test(x.value)); return i ? i.value : ''; }""")
        note("B has the invite link", "#call=" in link, "")
        close_sheets(b)
        bc = b.locator(CHAT).first
        note("the chat button is in B's control bar", bc.count() > 0 and bc.is_visible(), bc.get_attribute("aria-label") if bc.count() else "")

        # A joins from the link (desktop)
        a = ctx(br, 1280, 800, "בדיקת Claude א").new_page()
        a.goto(link, wait_until="networkidle")
        enter(a, "A (desktop)")
        a.wait_for_timeout(2500)

        # B writes; A gets the toast and the counter
        bc.click(); b.wait_for_timeout(1200)
        shot(b, "c0-after-chat-press")
        note("B's chat opens as a sheet", b.locator(".nlfch-panel").first.is_visible(), b.evaluate("() => [...document.querySelectorAll('.nlfch-panel')].map(e => getComputedStyle(e).display + '/' + e.hidden + '/' + e.getBoundingClientRect().height).join(',')"))
        send(b, "בדיקת Claude: שלום מהטלפון, רואים את הכתם ליד החלון?")
        shot(b, "c1-host-phone-chat")
        try:
            a.locator(".nlfch-toast").first.wait_for(state="visible", timeout=10000)
            note("A sees the new message pop over the video", "שלום מהטלפון" in a.locator(".nlfch-toast").first.inner_text(), a.locator(".nlfch-toast").first.inner_text())
        except Exception as e:
            note("A sees the new message pop over the video", False, e)
        bad = a.locator(".nlfch-badge").first
        note("A's chat button shows an unread counter", bad.count() > 0 and bad.inner_text().strip() not in ("", "0"), bad.inner_text() if bad.count() else "")
        shot(a, "c2-desktop-toast")

        # A opens the chat, answers and reacts
        a.locator(CHAT).first.click(); a.wait_for_timeout(1200)
        note("A sees B's message in the chat", "שלום מהטלפון" in a.locator(".nlfch-list").first.inner_text(), "")
        send(a, "בדיקת Claude: כן, נראה כמו רטיבות מהמרזב.")
        try:
            a.locator(".nlfch-m:not(.is-mine) .nlfch-rxb", has_text="מועיל").first.click(timeout=5000); a.wait_for_timeout(1500)
        except Exception as e:
            print("react:", e)
        b.wait_for_timeout(1500)
        bl = b.locator(".nlfch-list").first.inner_text()
        note("B receives A's answer live", "מהמרזב" in bl, "")
        note("B sees A's reaction on the message", re.search(r"מועיל\s*1", bl) is not None, " ".join(bl.split())[-120:])
        # B pins its own message
        try:
            b.locator(".nlfch-m.is-mine .nlfch-more").first.click(timeout=5000); b.wait_for_timeout(500)
            b.get_by_role("button", name="נעיצה").first.click(timeout=5000); b.wait_for_timeout(1500)
            a.wait_for_timeout(1000)
            note("the pinned bar shows on A", "שלום מהטלפון" in a.locator(".nlfch-pin").first.inner_text(), a.locator(".nlfch-pin").first.inner_text()[:80])
        except Exception as e:
            note("the pinned bar shows on A", False, e)
        shot(a, "c3-desktop-chat-panel")
        shot(b, "c4-host-phone-chat-pinned")

        # C joins late and sees the history
        c = ctx(br, 390, 844, "בדיקת Claude ג", True).new_page()
        c.goto(link, wait_until="networkidle")
        enter(c, "C (late, phone)")
        c.wait_for_timeout(1500); close_sheets(c)
        c.locator(CHAT).first.click(); c.wait_for_timeout(2000)
        ct = c.locator(".nlfch-panel").first.inner_text()
        note("C (late) sees the earlier messages and the divider", "שלום מהטלפון" in ct and "מהמרזב" in ct and "הודעות מלפני שנכנסת" in ct, "")
        shot(c, "c5-late-joiner-history")
        try:
            c.locator(".nlfch-x").first.click(timeout=3000)
            c.locator(".nlfc-end").first.click(timeout=5000)
        except Exception:
            pass

        # B leaves and attaches the summary
        try:
            b.locator(".nlfch-x").first.click(timeout=3000)
        except Exception:
            pass
        b.locator(".nlfc-end").first.click(); b.wait_for_timeout(2000)
        try:
            es = b.locator(".nlfch-endsheet").first
            es.wait_for(state="visible", timeout=10000)
            et = es.inner_text()
            note("B gets the end sheet with the attach question", "השיחה הסתיימה" in et and "מה לצרף לדיון" in et, " ".join(et.split())[:120])
            shot(b, "c6-host-end-sheet")
            with b.expect_response(lambda r: "/forum/chat" in r.url and r.request.method == "POST", timeout=30000) as rr:
                es.get_by_role("button", name=re.compile("לצרף לדיון")).first.click()
            note("the summary was attached", rr.value.status == 200, json.dumps(rr.value.json(), ensure_ascii=False)[:160])
        except Exception as e:
            note("B attaches the summary", False, e)
        try:
            a.locator(".nlfc-end").first.click(timeout=5000)
        except Exception:
            pass

        # a guest sees the summary answer
        g = ctx(br, 390, 844, None, True).new_page()
        g.goto(BASE + "/forum/%d/?t=%d" % (TOPIC, time.time()), wait_until="networkidle")
        body = g.locator("body").inner_text()
        note("guest sees the answer 'מה סוכם בשיחה' with the pinned line", "מה סוכם בשיחה" in body and "שלום מהטלפון" in body, "")
        loc = g.get_by_text("מה סוכם בשיחה").first
        if loc.count():
            loc.scroll_into_view_if_needed(); g.evaluate("() => window.scrollBy(0, -200)"); g.wait_for_timeout(500)
        shot(g, "c7-guest-summary-answer")
    finally:
        br.close()

json.dump({"topic": TOPIC, "at": time.strftime("%Y-%m-%d %H:%M:%S"), "ledger": LEDGER}, open(os.path.join(OUT, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("RESULT %d/%d" % (sum(1 for x in LEDGER if x["ok"]), len(LEDGER)))
