# -*- coding: utf-8 -*-
"""HAD-786 live check of the open video room, as real users would use it, on the live site.

Three browsers (the PC's own Chrome, driven by Playwright, with Chrome's fake camera and microphone):
  G  a guest with no session (phone width)       : sees the room button on the forum home, in a discussion and on a card
  A  test member "בדיקת Claude ב" (phone width)   : opens a room from a discussion, gets the link
  B  test member "בדיקת Claude א" (desktop width) : opens the link, joins; both must receive the other's video; the board
  C  test member "בדיקת Claude ג" (phone width)   : the room is locked by A, C must be refused with the "locked" message
The members come from forum_testkit.py make (their sessions are read from %TEMP%\\nlf_testkit_cookies.json and are never
printed); run forum_testkit.py clean afterwards. Every step saves a screenshot; the ledger is printed and saved as JSON.

  python scripts/project-stage/forum_room_live_check.py <out dir> [topic id] [card path]"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[1]
TOPIC = sys.argv[2] if len(sys.argv) > 2 else "6"
CARD = sys.argv[3] if len(sys.argv) > 3 else "/professionals/%D7%91%D7%99%D7%98%D7%95%D7%9F-%D7%9E%D7%90%D7%99%D7%A8/"
BASE = "https://nad-lan.co.il"
os.makedirs(OUT, exist_ok=True)
MEM = {m["name"]: m["cookie"] for m in json.load(open(os.path.join(os.environ.get("TEMP", "."), "nlf_testkit_cookies.json"), encoding="utf-8"))["members"]}
LEDGER = []


def note(step, ok, detail=""):
    LEDGER.append({"step": step, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("PASS " if ok else "FAIL ") + step + ((" | " + str(detail)[:200]) if detail else ""))


def ctx(browser, w, h, name=None, mobile=False):
    c = browser.new_context(viewport={"width": w, "height": h}, locale="he-IL", is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1,
                            permissions=["camera", "microphone"], user_agent=None)
    if name:
        c.add_cookies([{"name": "nlf_s", "value": MEM[name], "domain": "nad-lan.co.il", "path": "/", "secure": True, "httpOnly": True, "sameSite": "Lax"}])
    return c


def shot(page, name):
    page.screenshot(path=os.path.join(OUT, name + ".png"))


def vids(page):
    # how many <video> elements on the call screen really carry a moving picture
    return page.evaluate("""() => [...document.querySelectorAll('.nlfc-stage video, .nlfb-dock video, .nlfb-dtiles video')].filter(v => v.srcObject && v.videoWidth > 0 && !v.paused).length""")


def remote_vids(page):
    return page.evaluate("""() => [...document.querySelectorAll('.nlfc-remote video, .nlfc-strip video')].filter(v => v.srcObject && v.videoWidth > 0).length""")


with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream", "--autoplay-policy=no-user-gesture-required"])
    try:
        # ---------------------------------------------------------------- G: a guest sees the button everywhere
        g = ctx(br, 390, 844, None, True).new_page()
        for label, path in (("home", "/forum/?t=%d" % time.time()), ("discussion", "/forum/%s/?t=%d" % (TOPIC, time.time())), ("card", CARD + "?t=%d" % time.time())):
            g.goto(BASE + path, wait_until="domcontentloaded")
            b = g.locator("[data-nlf-room]").first
            try:
                b.wait_for(state="visible", timeout=15000)
                b.scroll_into_view_if_needed()
                box = b.bounding_box()
                note("guest sees the room button: " + label, True, "%dx%d at y=%d" % (box["width"], box["height"], box["y"]))
            except Exception as e:
                note("guest sees the room button: " + label, False, e)
            shot(g, "g-" + label)
        g.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
        g.locator("[data-nlf-room]").first.click()
        try:
            g.locator(".nlfc-sheet").wait_for(state="visible", timeout=10000)
            note("guest press asks to enter the forum first", "להיכנס" in g.locator(".nlfc-sheet").inner_text(), g.locator(".nlfc-sheet h2").inner_text())
        except Exception as e:
            note("guest press asks to enter the forum first", False, e)
        shot(g, "g-press")

        # ---------------------------------------------------------------- A opens a room from the discussion
        a = ctx(br, 390, 844, "בדיקת Claude ב", True).new_page()
        a.goto(BASE + "/forum/%s/?t=%d" % (TOPIC, time.time()), wait_until="networkidle")
        a.locator("[data-nlf-room]").first.click()
        a.locator(".nlfc-sheet").wait_for(state="visible", timeout=10000)
        note("A: the lobby opens", True, a.locator(".nlfc-sheet h2").inner_text())
        for sw in a.locator(".nlfc-sheet .nlfc-swin").all():
            sw.check(force=True)
        a.wait_for_timeout(1500)
        shot(a, "a1-lobby")
        note("A: camera preview is live in the lobby", a.evaluate("() => { const v = document.querySelector('.nlfc-pv video'); return !!(v && v.srcObject && v.videoWidth > 0); }"))
        a.locator(".nlfc-sheet .nlfc-pri").click()
        a.locator(".nlfc-stage").wait_for(state="visible", timeout=40000)
        note("A: the room opened (call screen)", True)
        a.wait_for_timeout(2500)
        shot(a, "a2-room-invite")
        link = a.evaluate("""() => { const i = [...document.querySelectorAll('.nlfc-sheet input, .nlfc-stage input')].find(x => /#call=/.test(x.value)); return i ? i.value : ''; }""")
        note("A: the invite sheet shows the link", "#call=" in link, link.split("#")[0] + "#call=…")
        wa = a.evaluate("""() => { const x = [...document.querySelectorAll('.nlfc-sheet a, .nlfc-sheet button')].find(e => /וואטסאפ/.test(e.textContent)); return x ? (x.getAttribute('href') || x.getAttribute('data-href') || 'button') : ''; }""")
        note("A: the WhatsApp button is there", bool(wa), wa[:60])

        # ---------------------------------------------------------------- B joins from the link
        b = ctx(br, 1280, 800, "בדיקת Claude א").new_page()
        b.goto(link, wait_until="networkidle")
        b.locator(".nlfc-sheet").wait_for(state="visible", timeout=15000)
        note("B: the link opens the join sheet", True, b.locator(".nlfc-sheet h2").inner_text())
        shot(b, "b1-join")
        for sw in b.locator(".nlfc-sheet .nlfc-swin").all():
            sw.check(force=True)
        b.wait_for_timeout(1200)
        b.locator(".nlfc-sheet .nlfc-pri").click()
        b.locator(".nlfc-stage").wait_for(state="visible", timeout=40000)
        note("B: entered the room", True)
        # close A's invite sheet if it is still open, then wait for the pictures
        try:
            a.locator(".nlfc-sheet .nlfc-x").click(timeout=3000)
        except Exception:
            pass
        ok_a = ok_b = False
        for _ in range(30):
            a.wait_for_timeout(1000)
            ok_a, ok_b = remote_vids(a) >= 1, remote_vids(b) >= 1
            if ok_a and ok_b:
                break
        note("A receives B's live video", ok_a)
        note("B receives A's live video", ok_b)
        shot(a, "a3-in-call")
        shot(b, "b2-in-call")

        # ---------------------------------------------------------------- the shared board
        try:
            a.locator(".nlfc-board").click()
            a.locator(".nlfb, [class^='nlfb-']").first.wait_for(state="visible", timeout=15000)
            b.locator(".nlfc-board").click()
            b.locator(".nlfb, [class^='nlfb-']").first.wait_for(state="visible", timeout=15000)
            count = "() => document.querySelectorAll('[class^=\"nlfb\"] svg path, [class^=\"nlfb\"] svg polyline, [class^=\"nlfb\"] svg line').length"
            before = b.evaluate(count)
            vp = a.viewport_size
            a.mouse.move(vp["width"] * 0.3, vp["height"] * 0.45)
            a.mouse.down()
            for i in range(12):
                a.mouse.move(vp["width"] * (0.3 + i * 0.03), vp["height"] * (0.45 + (i % 3) * 0.02))
            a.mouse.up()
            b.wait_for_timeout(2500)
            after = b.evaluate(count)
            note("board: A's line reaches B", after > before, "%d -> %d marks on B" % (before, after))
            shot(a, "a4-board")
            shot(b, "b3-board")
        except Exception as e:
            note("board: A's line reaches B", False, e)
            shot(a, "a4-board-fail")

        # ---------------------------------------------------------------- lock: C is refused
        try:
            r = a.evaluate("""async (room) => { const s = await (await fetch('/wp-json/nadlan/v1/forum/state', {credentials: 'same-origin'})).json();
                const q = await fetch('/wp-json/nadlan/v1/forum/call/lock', {method: 'POST', credentials: 'same-origin', headers: {'Content-Type': 'application/json', 'X-NLF-Nonce': s.nonce || ''}, body: JSON.stringify({room, lock: 1})});
                return q.status + ' ' + (await q.text()).slice(0, 160); }""", link.split("#call=")[1])
            note("A locks the room", r.startswith("200"), r)
            c = ctx(br, 390, 844, "בדיקת Claude ג", True).new_page()
            c.goto(link, wait_until="networkidle")
            c.wait_for_timeout(3500)
            txt = c.evaluate("() => (document.querySelector('.nlfc-toasts, .nlfc-sheet') || document.body).innerText.slice(0, 400)")
            if "נעול" not in txt:
                try:
                    c.locator(".nlfc-sheet .nlfc-pri").click(timeout=4000)
                    c.wait_for_timeout(3000)
                    txt = c.evaluate("() => (document.querySelector('.nlfc-sheet .nlfc-msg') || document.querySelector('.nlfc-toasts') || document.body).innerText.slice(0, 400)")
                except Exception:
                    pass
            note("C is refused: the room is locked", "נעול" in txt and c.locator(".nlfc-stage").count() == 0, txt.replace("\n", " ")[:160])
            shot(c, "c1-locked")
        except Exception as e:
            note("lock: C is refused", False, e)

        # ---------------------------------------------------------------- leave
        for pg, nm in ((b, "B"), (a, "A")):
            try:
                if pg.locator("[class^='nlfb'] .nlfb-x, .nlfb-close").count():
                    pg.keyboard.press("Escape")
                pg.locator(".nlfc-end").first.click(timeout=5000, force=True)
                pg.wait_for_timeout(1500)
                note(nm + " leaves: the call screen is gone", pg.locator(".nlfc-stage").count() == 0)
            except Exception as e:
                note(nm + " leaves: the call screen is gone", False, e)
    finally:
        br.close()

json.dump({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "base": BASE, "topic": TOPIC, "ledger": LEDGER}, open(os.path.join(OUT, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
bad = [x for x in LEDGER if not x["ok"]]
print("\n%d checks, %d passed, %d failed" % (len(LEDGER), len(LEDGER) - len(bad), len(bad)))
sys.exit(1 if bad else 0)
