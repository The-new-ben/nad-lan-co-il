# -*- coding: utf-8 -*-
"""HAD-783 live check of what 1.72.698 shipped and could not be verified then: a forum member opens an OWN professional card,
the card shows a video-call button to another member, and a real two-person call starts from it (the invited member gets the
in-forum notice and joins). The PC's own Chrome through Playwright, with Chrome's fake camera and microphone.
Test members from forum_testkit.py make; run forum_testkit.py clean afterwards (it trashes the test card too).

  python scripts/project-stage/forum_card_live_check.py <out dir>"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[1]
BASE = "https://nad-lan.co.il"
os.makedirs(OUT, exist_ok=True)
MEM = {m["name"]: m["cookie"] for m in json.load(open(os.path.join(os.environ.get("TEMP", "."), "nlf_testkit_cookies.json"), encoding="utf-8"))["members"]}
LEDGER = []


def note(step, ok, detail=""):
    LEDGER.append({"step": step, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("PASS " if ok else "FAIL ") + step + ((" | " + str(detail)[:200]) if detail else ""))


def ctx(browser, w, h, name, mobile=False):
    c = browser.new_context(viewport={"width": w, "height": h}, locale="he-IL", is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1, permissions=["camera", "microphone"])
    c.add_cookies([{"name": "nlf_s", "value": MEM[name], "domain": "nad-lan.co.il", "path": "/", "secure": True, "httpOnly": True, "sameSite": "Lax"}])
    return c


def remote_vids(page):
    return page.evaluate("""() => [...document.querySelectorAll('.nlfc-remote video, .nlfc-strip video')].filter(v => v.srcObject && v.videoWidth > 0).length""")


with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True, args=["--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream", "--autoplay-policy=no-user-gesture-required"])
    try:
        o = ctx(br, 390, 844, "בדיקת Claude ב", True).new_page()  # the one who opens a card
        o.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
        opener = o.locator("[data-nlfm-open]").first
        opener.wait_for(state="visible", timeout=15000)
        note("member sees the way to open a card", True, opener.inner_text())
        o.screenshot(path=os.path.join(OUT, "o1-forum-home-member.png"))
        opener.click()
        o.locator("#nlfm-form").wait_for(state="visible", timeout=8000)
        o.fill("#nlfm-name", "בדיקת Claude ב")
        opts = o.evaluate("() => [...document.querySelectorAll('#nlfm-trade option')].map(x => [x.value, x.textContent])")
        pick = next((v for v, t in opts if v and "שיפוצ" in t), None) or next(v for v, t in opts if v)
        o.select_option("#nlfm-trade", pick)
        o.fill("#nlfm-city", "תל אביב")
        o.fill("#nlfm-bio", "כרטיס בדיקה אוטומטי של האתר. יוסר בעוד כמה דקות.")
        o.locator("#nlfm-form input[name=how][value=forum]").check(force=True)
        o.wait_for_timeout(400)
        o.screenshot(path=os.path.join(OUT, "o2-form-filled.png"))
        o.locator("[data-nlfm-go]").click()
        try:
            o.wait_for_url("**/professionals/**", timeout=25000)
            card = o.url.split("?")[0]
            note("the card is saved and opens at once", True, card)
        except Exception as e:
            card = ""
            note("the card is saved and opens at once", False, o.locator("#nlfm-form .nlfm-msg").inner_text() if o.locator("#nlfm-form .nlfm-msg").count() else e)
        o.wait_for_load_state("networkidle")
        o.screenshot(path=os.path.join(OUT, "o3-own-card.png"))
        if card:
            note("own card page: the member-made top is there", o.locator("body.nlfm-member-card, .nlfm-card").count() > 0, o.locator("h1").first.inner_text())
            # another member looks at the card
            v = ctx(br, 1280, 800, "בדיקת Claude א").new_page()
            v.goto(card + "?t=%d" % time.time(), wait_until="networkidle")
            cb = v.locator("[data-nlf-callcard]").first
            try:
                cb.wait_for(state="visible", timeout=12000)
                box = cb.bounding_box()
                note("another member sees the video-call button on the card", True, "%s | %dx%d at y=%d" % (cb.inner_text().replace("\n", " ")[:50], box["width"], box["height"], box["y"]))
            except Exception as e:
                note("another member sees the video-call button on the card", False, e)
            v.screenshot(path=os.path.join(OUT, "v1-card-as-visitor-member.png"))
            cb.click()
            v.locator(".nlfc-sheet").wait_for(state="visible", timeout=10000)
            for sw in v.locator(".nlfc-sheet .nlfc-swin").all():
                sw.check(force=True)
            v.wait_for_timeout(1200)
            v.screenshot(path=os.path.join(OUT, "v2-lobby.png"))
            v.locator(".nlfc-sheet .nlfc-pri").click()
            v.locator(".nlfc-stage").wait_for(state="visible", timeout=40000)
            note("the caller is in the call screen", True)
            # the card owner gets the in-forum notice (the page polls at load) and joins
            o.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
            try:
                o.locator(".nlfc-toast").first.wait_for(state="visible", timeout=40000)
                note("the card owner gets the invitation notice", True, o.locator(".nlfc-toast p").first.inner_text())
                o.screenshot(path=os.path.join(OUT, "o4-invite-notice.png"))
                o.locator(".nlfc-toast .nlfc-pri").first.click()
                o.wait_for_timeout(2500)
                if o.locator(".nlfc-sheet").count() == 0:  # the notice led to the card page: the hash opens the join sheet there
                    o.wait_for_load_state("networkidle")
                o.locator(".nlfc-sheet").wait_for(state="visible", timeout=15000)
                for sw in o.locator(".nlfc-sheet .nlfc-swin").all():
                    sw.check(force=True)
                o.wait_for_timeout(1200)
                o.locator(".nlfc-sheet .nlfc-pri").click()
                o.locator(".nlfc-stage").wait_for(state="visible", timeout=40000)
                note("the card owner joined the call", True)
            except Exception as e:
                note("the card owner gets the invitation and joins", False, e)
            ok_v = ok_o = False
            for _ in range(30):
                v.wait_for_timeout(1000)
                ok_v, ok_o = remote_vids(v) >= 1, remote_vids(o) >= 1
                if ok_v and ok_o:
                    break
            note("the caller receives the owner's live video", ok_v)
            note("the owner receives the caller's live video", ok_o)
            v.screenshot(path=os.path.join(OUT, "v3-in-call.png"))
            o.screenshot(path=os.path.join(OUT, "o5-in-call.png"))
            for pg in (v, o):
                try:
                    pg.locator(".nlfc-end").first.click(timeout=5000, force=True)
                except Exception:
                    pass
    finally:
        br.close()

json.dump({"at": time.strftime("%Y-%m-%d %H:%M:%S"), "ledger": LEDGER}, open(os.path.join(OUT, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
bad = [x for x in LEDGER if not x["ok"]]
print("\n%d checks, %d passed, %d failed" % (len(LEDGER), len(LEDGER) - len(bad), len(bad)))
sys.exit(1 if bad else 0)
