# -*- coding: utf-8 -*-
"""HAD-787 live check of pictures, plans and files in forum posts (1.72.702) on the live site, with the test kit's members.
Before: forum_testkit.py make.  After: forum_testkit.py clean (removes the members, their posts, files and points).
  python scripts/project-stage/forum_media_live_check.py <out dir>
Member B (trusted) opens a discussion with 3 pictures (one carries a GPS location in its metadata) and one plan (PDF) on a phone;
a guest sees the gallery, the plan card and the full-screen viewer; the stored picture is downloaded and checked for metadata;
member A marks a point on a picture and asks (first post: goes to review, then forum_testkit.py approve); member A sets a picture."""
import io, json, os, re, subprocess, sys, time, urllib.request
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
OUT = sys.argv[1]
BASE = "https://nad-lan.co.il"
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
T = os.environ.get("TEMP", ".")
MEMS = json.load(open(os.path.join(T, "nlf_testkit_cookies.json"), encoding="utf-8"))["members"]
A, B = MEMS[0], MEMS[1]
LEDGER = []


def note(step, ok, detail=""):
    LEDGER.append({"step": step, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("PASS " if ok else "FAIL ") + step + ((" | " + str(detail)[:220]) if detail else ""))


# ---- the test files (made here, honest test pictures) ----
F = os.path.join(OUT, "_files"); os.makedirs(F, exist_ok=True)
cols = [((96, 112, 124), "1"), ((150, 162, 170), "2"), ((70, 84, 96), "3")]
pics = []
for i, (c, n) in enumerate(cols):
    im = Image.new("RGB", (3000, 2000), c); d = ImageDraw.Draw(im)
    for x in range(0, 3000, 150): d.line([(x, 0), (x, 2000)], fill=(min(c[0] + 30, 255),) * 3, width=3)
    d.rectangle([1200, 700, 1800, 1300], outline=(255, 255, 255), width=18)
    p = os.path.join(F, "test-%s.jpg" % n)
    if i == 0:  # GPS in the metadata: 32.08 N, 34.78 E
        ex = Image.Exif(); gps = {1: "N", 2: (32.0, 4.0, 48.0), 3: "E", 4: (34.0, 46.0, 48.0)}
        ex[0x8825] = gps; ex[0x010F] = "TestCam"
        im.save(p, "JPEG", quality=90, exif=ex.tobytes())
    else:
        im.save(p, "JPEG", quality=90)
    pics.append(p)
raw = open(pics[0], "rb").read()
note("test picture 1 carries a GPS block before upload", b"Exif" in raw and b"TestCam" in raw, len(raw))
pdf = os.path.join(F, "plan-test.pdf")
objs = ["<< /Type /Catalog /Pages 2 0 R >>", "<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] >>", "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] >>"]
body, offs = b"%PDF-1.4\n", []
for i, o in enumerate(objs, 1):
    offs.append(len(body)); body += ("%d 0 obj\n%s\nendobj\n" % (i, o)).encode()
xref = len(body)
body += ("xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)).encode() + b"".join(("%010d 00000 n \n" % x).encode() for x in offs)
body += ("trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)).encode()
open(pdf, "wb").write(body)


def ctx_for(br, cookie=None, mobile=True):
    c = br.new_context(viewport={"width": 390, "height": 844} if mobile else {"width": 1280, "height": 900}, locale="he-IL",
                       is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
    if cookie:
        c.add_cookies([{"name": "nlf_s", "value": cookie, "domain": "nad-lan.co.il", "path": "/", "secure": True, "httpOnly": True, "sameSite": "Lax"}])
    return c


TOPIC = int(os.environ.get("PIN_TOPIC", "0"))  # PIN_TOPIC=<id>: only steps 4-6 on an existing test discussion
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True)
    try:
        if not TOPIC:
            # 1. member B writes a discussion with 3 pictures and a plan, on a phone
            b = ctx_for(br, B["cookie"]).new_page()
            b.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
            b.evaluate("() => document.getElementById('nlf-compose').showModal()")
            f = b.locator("form[data-nlf-composeform]")
            b.wait_for_timeout(800)
            picks = f.locator(".nlfmd-pick")
            note("the composer shows camera, pictures and plan buttons", picks.count() == 3, [picks.nth(i).inner_text() for i in range(picks.count())])
            f.locator("#nlf-c-title").fill("בדיקת Claude: תמונות ותוכנית בדיון")
            f.locator("#nlf-c-body").fill("דיון בדיקה אוטומטי של האתר. יוסר בעוד כמה דקות.")
            f.locator("input[type=file][multiple][accept='image/*']").set_input_files(pics)
            f.locator("input[type=file][accept*='pdf']").set_input_files([pdf])
            try:
                b.wait_for_function("() => document.querySelectorAll('form[data-nlf-composeform] .nlfmd-th').length >= 4 && !document.querySelector('form[data-nlf-composeform] .nlfmd-th-bar:not([hidden])')", timeout=90000)
            except Exception as e:
                print("wait thumbs:", e)
            b.wait_for_timeout(1500)
            n = f.locator(".nlfmd-th").count()
            chip = f.locator(".nlfmd-chip-ok").first
            note("4 files uploaded with thumbnails", n >= 4, n)
            note("the chip says the location was removed", chip.count() > 0 and "המיקום הוסר" in chip.inner_text(), chip.inner_text() if chip.count() else "")
            caps = f.locator(".nlfmd-cap")
            if caps.count():
                caps.first.fill("קיר בדיקה, סלון")
            f.screenshot(path=os.path.join(OUT, "m1-composer-phone.png"))
            with b.expect_response(lambda r: "/forum/topic" in r.url and r.request.method == "POST", timeout=60000) as ri:
                f.locator("button[type=submit]").click()
            j = ri.value.json()
            TOPIC = int((j.get("topic") or {}).get("id") or j.get("id") or j.get("topic_id") or 0) if isinstance(j, dict) else 0
            if not TOPIC:
                m = re.search(r'"(?:id|topic_id)"\s*:\s*(\d+)', json.dumps(j)); TOPIC = int(m.group(1)) if m else 0
            note("the discussion was published", TOPIC > 0, json.dumps(j, ensure_ascii=False)[:200])
            json.dump({"topic": TOPIC}, open(os.path.join(T, "nlf_media_check.json"), "w"))

            # 2. a guest on a phone: gallery, plan card, viewer
            g = ctx_for(br).new_page()
            g.goto(BASE + "/forum/%d/?t=%d" % (TOPIC, time.time()), wait_until="networkidle")
            gal = g.locator(".nlfmd-gal").first
            tiles = g.locator(".nlfmd-gal .nlfmd-tile")
            note("guest sees the gallery with 3 pictures", gal.count() > 0 and tiles.count() == 3, tiles.count())
            imgs = g.evaluate("() => [...document.querySelectorAll('.nlfmd-gal img')].map(i => ({src: i.currentSrc || i.src, alt: i.alt, w: i.naturalWidth}))")
            note("pictures have alt text and load", all(i["alt"] for i in imgs) and all(i["w"] > 0 for i in imgs), imgs[:1])
            pdfc = g.locator(".nlfmd-pdf-card").first
            note("guest sees the plan card with page count and both buttons", pdfc.count() > 0 and "2 עמודים" in pdfc.inner_text() and "לשרטט עליה ביחד" in g.locator(".nlfmd-pdf").first.inner_text() and "הורדה" in g.locator(".nlfmd-pdf").first.inner_text(), " ".join(g.locator(".nlfmd-pdf").first.inner_text().split()) if pdfc.count() else "")
            ld = g.evaluate("() => [...document.querySelectorAll('script[type=\"application/ld+json\"]')].map(s => s.textContent).join(' ')")
            note("the page's structured data carries the first picture", '"ImageObject"' in ld and "nlf-media" in ld, "")
            gal.scroll_into_view_if_needed(); g.evaluate("() => window.scrollBy(0, -120)"); g.wait_for_timeout(600)
            g.screenshot(path=os.path.join(OUT, "m2-guest-gallery-phone.png"))
            tiles.first.click(); g.wait_for_timeout(1200)
            lb = g.locator(".nlfmd-lb").first
            cnt = g.locator(".nlfmd-lb-count").first.inner_text() if g.locator(".nlfmd-lb-count").count() else ""
            note("the full-screen viewer opens on picture 1", lb.is_visible() and re.sub(r"\s", "", cnt) in ("1/3",), cnt)
            g.screenshot(path=os.path.join(OUT, "m3-guest-viewer-phone.png"))
            try:
                g.mouse.move(300, 400); g.locator(".nlfmd-lb-next").first.click(timeout=3000)
            except Exception:
                g.keyboard.press("ArrowLeft")
            g.wait_for_timeout(700)
            cnt2 = g.locator(".nlfmd-lb-count").first.inner_text()
            note("the viewer moves to picture 2", re.sub(r"\s", "", cnt2) == "2/3", cnt2)

            # 3. the stored picture has no metadata
            src = imgs[0]["src"] if imgs else ""
            full = re.sub(r"-480\.jpg$", ".jpg", src)
            data = urllib.request.urlopen(urllib.request.Request(full, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read() if full else b""
            try:
                ex = Image.open(io.BytesIO(data)).getexif()
                has_gps = 0x8825 in ex
                sz = Image.open(io.BytesIO(data)).size
            except Exception as e:
                has_gps, sz = True, str(e)
            note("the stored picture has no location and no camera name", data and not has_gps and b"TestCam" not in data, "%s %s bytes, size %s" % (full[-60:], len(data), sz))
            note("the stored picture was shrunk to 2048 on the long side or less", isinstance(sz, tuple) and max(sz) <= 2048, sz)

        # 4. member A marks a point on picture 2 and asks
        a = ctx_for(br, A["cookie"]).new_page()
        a.goto(BASE + "/forum/%d/?t=%d" % (TOPIC, time.time()), wait_until="networkidle")
        a.locator(".nlfmd-gal .nlfmd-tile").nth(1).click(); a.wait_for_timeout(1000)
        try:
            a.locator(".nlfmd-lb-ask").first.click(timeout=5000); a.wait_for_timeout(600)
            st = a.locator(".nlfmd-lb-stage, .nlfmd-lb-img").first.bounding_box()
            a.mouse.click(st["x"] + st["width"] * 0.6, st["y"] + st["height"] * 0.45); a.wait_for_timeout(800)
            a.screenshot(path=os.path.join(OUT, "m4-member-marks-point-phone.png"))
            a.locator(".nlfmd-lb-markbar button", has_text="לשאול על הנקודה").first.click(); a.wait_for_timeout(1200)
            pq = a.locator("form[data-nlf-replyform] .nlfmd-pinq").first
            note("the answer form opens with the marked crop", pq.count() > 0 and pq.is_visible(), "")
            rf = a.locator("form[data-nlf-replyform]").first
            rf.locator("textarea").first.fill("בדיקת Claude: מה זה הכתם כאן?")
            a.screenshot(path=os.path.join(OUT, "m5-answer-with-point-phone.png"))
            with a.expect_response(lambda r: "/forum/reply" in r.url and r.request.method == "POST", timeout=60000) as rr:
                rf.locator("button[type=submit]").first.click()
            note("the answer with the point was sent", rr.value.status == 200, json.dumps(rr.value.json(), ensure_ascii=False)[:160])
        except Exception as e:
            note("member marks a point and asks", False, e)

        # 5. member A sets a profile picture
        try:
            a.goto(BASE + "/forum/?t=%d" % time.time(), wait_until="networkidle")
            a.locator("[data-nlfmd-avatar]").first.click(timeout=8000); a.wait_for_timeout(800)
            sh = a.locator("#nlfmd-avatar")
            sh.locator("input[type=file]").first.set_input_files(pics[1]); a.wait_for_timeout(1500)
            a.screenshot(path=os.path.join(OUT, "m6-member-picture-editor-phone.png"))
            with a.expect_response(lambda r: "/forum/media" in r.url and r.request.method == "POST", timeout=60000) as ar:
                sh.locator(".nlfmd-btn-sea, button.nlfmd-btn-wide").last.click()
            note("the member picture was saved", ar.value.status == 200, json.dumps(ar.value.json(), ensure_ascii=False)[:160])
        except Exception as e:
            note("the member picture was saved", False, e)
    finally:
        br.close()

# 6. approve A's answer (first post goes to review), then a guest sees the point and A's picture
ap = subprocess.run([sys.executable, os.path.join(HERE, "forum_testkit.py"), "approve", str(TOPIC)], capture_output=True, text=True, encoding="utf-8")
print(ap.stdout[-300:])
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome", headless=True)
    try:
        g = ctx_for(br).new_page()
        g.goto(BASE + "/forum/%d/?t=%d" % (TOPIC, time.time()), wait_until="networkidle")
        pin = g.locator(".nlfmd-pinq").first
        note("guest sees the answer with the marked crop", pin.count() > 0, "")
        av = g.evaluate("() => [...document.querySelectorAll('img')].filter(i => /nlf-media/.test(i.src) && i.closest('.nlf-arow, .nlf-acol, .nlf-reply, .nlf-ans, article')).length")
        note("the member picture replaces the initials next to the answer", av > 0, av)
        if pin.count():
            pin.scroll_into_view_if_needed(); g.evaluate("() => window.scrollBy(0, -160)"); g.wait_for_timeout(500)
        g.screenshot(path=os.path.join(OUT, "m7-guest-answer-with-point-phone.png"))
        d = ctx_for(br, mobile=False).new_page()
        d.goto(BASE + "/forum/%d/?t=%d" % (TOPIC, time.time()), wait_until="networkidle")
        d.locator(".nlfmd-gal").first.scroll_into_view_if_needed(); d.evaluate("() => window.scrollBy(0, -140)"); d.wait_for_timeout(600)
        d.screenshot(path=os.path.join(OUT, "m8-guest-gallery-desktop.png"))
    finally:
        br.close()

json.dump({"topic": TOPIC, "at": time.strftime("%Y-%m-%d %H:%M:%S"), "ledger": LEDGER}, open(os.path.join(OUT, "ledger.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("RESULT %d/%d" % (sum(1 for x in LEDGER if x["ok"]), len(LEDGER)))
