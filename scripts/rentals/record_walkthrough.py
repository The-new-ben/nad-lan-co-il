# -*- coding: utf-8 -*-
"""Records the rentals walkthrough video (sample data, local lab) with on-screen
captions. Output: docs/design-lab/rentals/video/walkthrough-<lang>-<dev>.webm
Usage: python scripts/rentals/record_walkthrough.py [he|en] [desk|phone]"""
import sys, pathlib, shutil
from playwright.sync_api import sync_playwright

LANG = sys.argv[1] if len(sys.argv) > 1 else "he"
DEV = sys.argv[2] if len(sys.argv) > 2 else "desk"
BASE = "http://127.0.0.1:47914/docs/design-lab/rentals/app.html"
OUT = pathlib.Path(__file__).resolve().parents[2] / "docs/design-lab/rentals/video"
OUT.mkdir(parents=True, exist_ok=True)
VP = {"width": 1280, "height": 760} if DEV == "desk" else {"width": 390, "height": 760}

CAP = {
 "he": [
  "ניהול השכרות בנדלן: כל הדירות המושכרות שלכם במסך אחד",
  "מה שולם, מה באיחור, ומה צריך טיפול היום, לפי סדר הסיכון",
  "תזכורת בוואטסאפ נכתבת לבד, בשפה של השוכר, ונשלחת מהטלפון שלכם",
  "כל בניין בתלת ממד, והדירות שלכם צבועות לפי מצב התשלום",
  "לחיצה על דירה פותחת הכול: השוכר, החוזה, התשלומים והביטחונות",
  "המועדים לפי חוק השכירות: הודעה, אופציה, הצמדה למדד והחזרת ביטחונות",
  "הדירה מבפנים: הדוד, המזגן והמונים, עם האחריות של כל מכשיר",
  "תקלות עם המועד שהחוק נותן לתיקון: 3 ימים לדחוף, 30 לרגיל",
  "צ'קים להפקדה, רווח והפסד, והצמדה ישר מהלשכה המרכזית לסטטיסטיקה",
  "השוכר מקבל קישור אישי בוואטסאפ: משלם, מדווח תקלה עם תמונה וחותם על החוזה",
  "ובאנגלית, לבעלי דירות ולשוכרים שמדברים אנגלית",
  "nad-lan.co.il/my-rentals · מתחילים לנהל בחינם",
 ],
 "en": [
  "NadLan rental management: every apartment you rent out, on one screen",
  "What was paid, what is late and what needs you today, riskiest first",
  "A WhatsApp reminder writes itself, in the tenant's language, sent from your phone",
  "Each building in 3D, your apartments coloured by payment status",
  "Tap an apartment for everything: tenant, lease, payments, securities",
  "The Fair Rental Law deadlines: notice, option, CPI linkage, deposit return",
  "Inside the apartment: water heater, A/C, meters, each with its warranty",
  "Repairs against the legal deadline: 3 days urgent, 30 standard",
  "Cheques to deposit, profit and loss, CPI straight from the CBS",
  "Each tenant gets a personal WhatsApp link: pay, report a repair with a photo, sign",
  "And in Hebrew, for Hebrew-speaking landlords and tenants",
  "nad-lan.co.il/my-rentals · start managing, free",
 ],
}[LANG]

CSS = """#cap{position:fixed;inset-inline:0;bottom:22px;z-index:200000;display:flex;justify-content:center;pointer-events:none}
#cap span{max-width:min(92vw,980px);background:rgba(20,33,43,.88);color:#fff;font:700 %dpx/1.35 Assistant,Arial,sans-serif;padding:12px 20px;border-radius:14px;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.25);transition:opacity .25s}""" % (24 if DEV == "desk" else 17)

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport=VP, device_scale_factor=1, is_mobile=(DEV == "phone"), has_touch=(DEV == "phone"))
    pg = ctx.new_page()
    FR = OUT / ("frames-%s-%s" % (LANG, DEV)); shutil.rmtree(FR, ignore_errors=True); FR.mkdir(parents=True)
    frames = []
    cdp = ctx.new_cdp_session(pg)
    def on_frame(ev):
        import base64
        n = len(frames)
        (FR / ("f%05d.jpg" % n)).write_bytes(base64.b64decode(ev["data"]))
        frames.append(ev["metadata"].get("timestamp", 0))
        try: cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]})
        except Exception: pass
    cdp.on("Page.screencastFrame", on_frame)
    def cap(i, ms=2600):
        pg.evaluate("""([css, t]) => { let s = document.getElementById('capcss'); if (!s) { s = document.createElement('style'); s.id = 'capcss'; s.textContent = css; document.head.appendChild(s); }
            let c = document.getElementById('cap'); if (!c) { c = document.createElement('div'); c.id = 'cap'; c.innerHTML = '<span></span>'; document.body.appendChild(c); }
            c.setAttribute('dir', /[\\u0590-\\u05FF]/.test(t) ? 'rtl' : 'ltr'); c.firstChild.textContent = t; }""", [CSS, CAP[i]])
        pg.wait_for_timeout(ms)
    pg.goto(BASE + "?lang=" + LANG + "#/today", wait_until="networkidle")
    pg.wait_for_selector(".nlrm-kpis"); pg.wait_for_timeout(600)
    cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 82, "maxWidth": VP["width"], "maxHeight": VP["height"], "everyNthFrame": 1})
    cap(0, 2800)
    pg.mouse.wheel(0, 260); cap(1, 2800); pg.mouse.wheel(0, -260)
    pg.click("[data-act='wa-remind']"); pg.wait_for_timeout(500); cap(2, 3400)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    pg.evaluate("location.hash = '#/property/2'"); pg.wait_for_timeout(3800); cap(3, 3200)
    pg.evaluate("document.querySelector('.nlrm3d-tag:not(.is-off)').click()"); pg.wait_for_timeout(700); cap(4, 3000)
    pg.click(".nlrm-ptabs [data-tab='lease']"); pg.wait_for_timeout(400)
    pg.evaluate("document.querySelector('.nlrm-pbody').scrollTo({top: 700, behavior: 'smooth'})"); cap(5, 3200)
    pg.click(".nlrm-ptabs [data-tab='home']"); pg.wait_for_timeout(2600)
    pg.evaluate("document.querySelector('.nlrm-pbody').scrollTo({top: 420, behavior: 'smooth'})"); cap(6, 3400)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    pg.evaluate("location.hash = '#/repairs'"); pg.wait_for_timeout(700); cap(7, 2800)
    pg.evaluate("location.hash = '#/money'"); pg.wait_for_timeout(500)
    pg.click("[data-mtab='cheques']"); pg.wait_for_timeout(500); cap(8, 2600)
    pg.evaluate("location.hash = '#/today'"); pg.wait_for_timeout(500)
    pg.click("[data-open^='unit:']"); pg.wait_for_timeout(600)
    pg.click(".nlrm-layer.is-in [data-act='portal-link']"); pg.wait_for_timeout(700); cap(9, 3600)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(250)
    for _ in range(2):
        if pg.locator(".nlrm-layer").count(): pg.keyboard.press("Escape"); pg.wait_for_timeout(250)
    other = "en" if LANG == "he" else "he"
    pg.click(".nlrm-lang [data-lang='%s']" % other); pg.wait_for_timeout(900); cap(10, 3000)
    pg.click(".nlrm-lang [data-lang='%s']" % LANG); pg.wait_for_timeout(700); cap(11, 3200)
    cdp.send("Page.stopScreencast"); pg.wait_for_timeout(300)
    ctx.close(); b.close()
    # durations from the frame timestamps -> an image sequence list for DaVinci + an animated WebP preview
    from PIL import Image
    ts = frames + [frames[-1] + 0.5] if frames else []
    durs = [max(40, int((ts[i + 1] - ts[i]) * 1000)) for i in range(len(frames))]
    (FR / "durations.txt").write_text(chr(10).join("f%05d.jpg %d" % (i, d) for i, d in enumerate(durs)), encoding="utf-8")
    # resample to a steady 8 fps for the preview
    step, t, out, k = 125, 0, [], 0
    total = sum(durs); acc = 0; idx = 0; marks = []
    for i, d in enumerate(durs): marks.append(acc); acc += d
    while t < total:
        while idx + 1 < len(marks) and marks[idx + 1] <= t: idx += 1
        out.append(idx); t += step
    W = 900 if DEV == "desk" else 390
    imgs = []
    for i in out:
        im = Image.open(FR / ("f%05d.jpg" % i)).convert("RGB")
        if im.width > W: im = im.resize((W, int(im.height * W / im.width)))
        imgs.append(im)
    dst = OUT / ("walkthrough-%s-%s.webp" % (LANG, DEV))
    imgs[0].save(dst, save_all=True, append_images=imgs[1:], duration=step, loop=0, quality=72, method=4)
    print("frames", len(frames), "seconds", round(total / 1000, 1), "preview", dst, dst.stat().st_size, "bytes")
