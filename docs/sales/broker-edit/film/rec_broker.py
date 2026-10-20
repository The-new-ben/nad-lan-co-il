# -*- coding: utf-8 -*-
"""The broker self-edit explainer film (Hebrew, narrated): recorded on the LIVE private page with real taps on a phone screen,
on Meital's two DRAFT test listings (never public), then set in a phone frame with a step title, subtitles and the narration.
python rec_broker.py -> broker-edit-he.mp4 (1920x1080)"""
import json, os, shutil, subprocess, time
import imageio_ffmpeg
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "audio")
SCR = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad"
LINK = json.load(open(os.path.join(SCR, "meital_q.json"), encoding="utf-8"))["link"]
NEW = json.load(open(r"C:\Users\777\nad-lan\nad-lan-co-il\scripts\broker-edit\fixtures-run1.json"))["new"]
OLD = json.load(open(r"C:\Users\777\nad-lan\nad-lan-co-il\scripts\broker-edit\fixtures.json"))["old"]
N = json.load(open(os.path.join(H, "narration.json"), encoding="utf-8"))["scenes"]
D = json.load(open(os.path.join(A, "durations.json")))
RAW = os.path.join(H, "raw"); shutil.rmtree(RAW, ignore_errors=True); os.makedirs(RAW)
PH = [os.path.join(os.path.dirname(H), "test-photo-1.jpg"), os.path.join(os.path.dirname(H), "test-photo-2.jpg")]
TAP = r"""(()=>{if(window.__nlt)return;window.__nlt=1;const s=document.createElement('style');s.textContent=`.nltap{position:fixed;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;background:rgba(31,75,92,.28);border:3px solid rgba(255,255,255,.95);box-shadow:0 0 0 2px rgba(31,75,92,.5);z-index:2147483647;pointer-events:none;animation:nltp .7s ease-out forwards}@keyframes nltp{to{transform:scale(1.9);opacity:0}}`;document.head.appendChild(s);
addEventListener('pointerdown',e=>{const d=document.createElement('div');d.className='nltap';d.style.left=e.clientX+'px';d.style.top=e.clientY+'px';document.body.appendChild(d);setTimeout(()=>d.remove(),800)},true)})()"""
LOG = []


def idle(pg, mx=200):
    t = time.time()
    while time.time() - t < mx:
        if pg.locator("#nlew").count() == 0 or pg.locator("#nlew").is_hidden():
            return
        pg.wait_for_timeout(500)


def tap(pg, loc, after=700):
    loc.scroll_into_view_if_needed(timeout=10000); bb = loc.bounding_box()
    pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2); pg.mouse.down(); pg.wait_for_timeout(90); pg.mouse.up(); pg.wait_for_timeout(after)


def typing(pg, sel, text, delay=55):
    pg.locator(sel).click(); pg.keyboard.press("Control+A"); pg.keyboard.press("Delete"); pg.keyboard.type(text, delay=delay)


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=False, args=["--hide-scrollbars"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="he-IL",
                        record_video_dir=RAW, record_video_size={"width": 780, "height": 1688})
    pg = ctx.new_page(); T0 = time.time()
    pg.goto(LINK, wait_until="load"); pg.wait_for_timeout(1800); pg.evaluate(TAP)
    F0 = time.time()

    def sc(i, fn):
        sid = N[i][0]; st = time.time() - F0; t1 = time.time()
        try:
            pg.evaluate(TAP); fn(); ok = "ok"
        except Exception as e:
            ok = "skip: " + " ".join(str(e).split())[:400]
            try: pg.screenshot(path=os.path.join(H, f"fail-{i:02d}.png"))
            except Exception: pass
            try:
                if pg.locator("#nles").is_visible(): pg.locator("#nles [data-cancel]").click(timeout=3000); pg.wait_for_timeout(400)
                if pg.locator("#nles [data-l]").count(): pg.locator("#nles [data-l]").click(timeout=3000)
            except Exception: pass
        left = D[f"{i:02d}-{sid}"] + 0.8 - (time.time() - t1)
        if left > 0:
            pg.wait_for_timeout(int(left * 1000))
        LOG.append({"i": i, "id": sid, "start": round(st, 2), "status": ok}); print(i, sid, round(st, 1), ok)

    def s0(): pg.wait_for_timeout(1500); pg.mouse.wheel(0, 120); pg.wait_for_timeout(900); pg.mouse.wheel(0, -120)
    def s1(): tap(pg, pg.locator("header.top .who"), 600)
    def s2():
        pg.set_input_files("#files", PH); pg.wait_for_timeout(1500)
        typing(pg, "#txt", "להשכרה, 4 חדרים, 105 מ״ר, קומה 6 מתוך 9, מרפסת 12 מ״ר, חניה ומחסן. נופי ים. 16,500 ש״ח לחודש. כניסה מיידית.", 30)
        pg.wait_for_timeout(600); pg.locator("#send").scroll_into_view_if_needed(); pg.wait_for_timeout(800)
    def s3():
        pg.goto(LINK, wait_until="load"); pg.evaluate(TAP); pg.wait_for_timeout(1200)
        pg.locator("#h-mine").scroll_into_view_if_needed(); pg.wait_for_timeout(1500); pg.mouse.wheel(0, 260); pg.wait_for_timeout(1200)
        e = pg.locator(".nle-edit").first; bb = e.bounding_box(); pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2, steps=12)
    def s4():
        pg.evaluate("location.hash='#edit-%d'" % NEW); pg.wait_for_selector("#nle:not([hidden])", timeout=60000); pg.wait_for_timeout(1500)
        tap(pg, pg.locator('#nle [data-st="rented"]'), 300); idle(pg); pg.wait_for_timeout(2200); tap(pg, pg.locator("#nlet button"), 300); idle(pg)
    def s5():
        tap(pg, pg.locator('#nle [data-sec="price"]'), 700); typing(pg, "#nle-price", "21900", 120); pg.wait_for_timeout(500); tap(pg, pg.locator("#nles [data-save]"), 300); idle(pg)
    def s6():
        tap(pg, pg.locator('#nle [data-sec="photos"]'), 900)
        a = pg.locator("#nle-ph li[data-id]").nth(0).bounding_box(); z = pg.locator("#nle-ph li[data-id]").nth(2).bounding_box()
        pg.mouse.move(a["x"] + a["width"] / 2, a["y"] + a["height"] / 2); pg.mouse.down(); pg.wait_for_timeout(500)
        pg.mouse.move(a["x"] + a["width"] / 2 + 5, a["y"] + a["height"] / 2, steps=2); pg.mouse.move(z["x"] + z["width"] / 2, z["y"] + z["height"] / 2, steps=16); pg.wait_for_timeout(250); pg.mouse.up()
        pg.wait_for_timeout(2200); tap(pg, pg.locator("#nle-ph li[data-id]").nth(1).locator("button"), 900)
        tap(pg, pg.locator('#nle-pa [data-a="cover"]'), 300); pg.wait_for_timeout(2200)
        add = pg.locator("#nle-ph li.add"); add.scroll_into_view_if_needed(); bb = add.bounding_box(); pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2, steps=12); pg.wait_for_timeout(900)
        tap(pg, pg.locator("#nles [data-save]"), 400)
    def s7():
        tap(pg, pg.locator('#nle [data-sec="details"]'), 900); pg.locator("#nle-rooms").scroll_into_view_if_needed(); typing(pg, "#nle-rooms", "5.5", 140); pg.wait_for_timeout(500)
        tap(pg, pg.locator("#nles [data-save]"), 300); idle(pg, 240)
    def s8():
        tap(pg, pg.locator('#nle [data-sec="features"]'), 900)
        for k in ("ac", "elevator"):
            c = pg.locator('#nles [data-feat="%s"]' % k)
            if c.get_attribute("aria-pressed") != "true": tap(pg, c, 500)
        pg.locator("#nle-features_he").scroll_into_view_if_needed(); typing(pg, "#nle-features_he", "חדר כושר ושומר בבניין", 60); pg.wait_for_timeout(400)
        tap(pg, pg.locator("#nles [data-save]"), 300); idle(pg, 240)
    def s9():
        tap(pg, pg.locator('#nle [data-sec="text"]'), 900); pg.locator("#nle-title").click(); pg.keyboard.press("End"); pg.keyboard.type(" עם 3 חניות", delay=90)
        tap(pg, pg.locator("#nles [data-save]"), 300); idle(pg); pg.wait_for_timeout(2600); tap(pg, pg.locator("#nles [data-cancel]"), 500)
        lv = pg.locator("#nles [data-l]")
        if lv.count(): tap(pg, lv, 400)
    def s10():
        tap(pg, pg.locator("#nle [data-x]"), 500); pg.evaluate("location.hash='#edit-%d'" % OLD); pg.wait_for_timeout(1200); idle(pg, 240); pg.wait_for_timeout(1500)
    def s11():
        tap(pg, pg.locator("#nle [data-x]"), 500); pg.locator("#nle-pt").scroll_into_view_if_needed(); pg.wait_for_timeout(600); tap(pg, pg.locator("#nle-pe"), 1200)
        pg.locator("#nle-areas").scroll_into_view_if_needed(); pg.wait_for_timeout(1500); tap(pg, pg.locator("#nles [data-cancel]"), 400)
    def s12():
        pg.evaluate("()=>{const e=document.createElement('div');e.style.cssText='position:fixed;inset:0;z-index:2147483647;background:#1F4B5C;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;font-family:Assistant,Arial;text-align:center;padding:24px';e.innerHTML='<b style=\"font-size:34px\">נדל״ן</b><span style=\"font-size:20px\">ניהול מודעות למתווכים, מהטלפון</span><span style=\"font-size:16px;opacity:.85\">nad-lan.co.il</span>';document.body.appendChild(e)}")

    for i, fn in enumerate((s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12)):
        sc(i, fn)
    v = pg.video.path(); ctx.close(); b.close()
off = F0 - T0
json.dump({"log": LOG, "video": v, "off": off}, open(os.path.join(H, "rec-log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------- the frame, titles, subtitles, narration ----------------
ff = imageio_ffmpeg.get_ffmpeg_exe()
SW, SHh = 440, 952; BX, BY = 230, 64; PAD = 16
bez = Image.new("RGBA", (SW + 2 * PAD, SHh + 2 * PAD), (0, 0, 0, 0)); d = ImageDraw.Draw(bez)
d.rounded_rectangle([0, 0, SW + 2 * PAD - 1, SHh + 2 * PAD - 1], radius=64, fill=(10, 16, 22, 255))
d.rounded_rectangle([PAD, PAD, PAD + SW - 1, PAD + SHh - 1], radius=48, fill=(0, 0, 0, 0))
mask = Image.new("L", bez.size, 0); ImageDraw.Draw(mask).rounded_rectangle([PAD, PAD, PAD + SW - 1, PAD + SHh - 1], radius=48, fill=255)
bez.save(os.path.join(H, "bezel.png"))
ends = [LOG[k + 1]["start"] if k + 1 < len(LOG) else LOG[k]["start"] + D[f"{LOG[k]['i']:02d}-{LOG[k]['id']}"] + 1.2 for k in range(len(LOG))]
def ts(t): return "%d:%02d:%05.2f" % (t // 3600, (t % 3600) // 60, t % 60)
ass = ["[Script Info]", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 0", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: K,Arial,34,&H00C9E2EA,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,1,0,1,0,0,9,820,110,250,177",
       "Style: T,Arial,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,9,820,110,300,177",
       "Style: S,Arial,42,&H00FFFFFF,&H00FFFFFF,&H005C4B1F,&H005C4B1F,0,0,0,0,100,100,0,0,3,18,0,3,820,110,170,177",
       "Style: B,Arial,28,&H00C9E2EA,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,3,820,110,60,177", "", "[Events]",
       "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
total = len(N) - 2
for k, x in enumerate(LOG):
    title, text = N[x["i"]][1], N[x["i"]][2]
    a, e = x["start"] + 0.15, ends[k] - 0.05
    if 0 < x["i"] < len(N) - 1:
        ass.append(f"Dialogue: 0,{ts(a)},{ts(e)},K,,0,0,0,,שלב {x['i']} מתוך {total}")
    ass.append(f"Dialogue: 0,{ts(a)},{ts(e)},T,,0,0,0,,{title}")
    ass.append(f"Dialogue: 0,{ts(a + 0.2)},{ts(e)},S,,0,0,0,,{text}")
ass.append(f"Dialogue: 0,{ts(0)},{ts(ends[-1])},B,,0,0,0,,nad-lan.co.il · ניהול מודעות למתווכים · התמונות והמודעות בסרטון הן לדוגמה")
open(os.path.join(H, "film.ass"), "w", encoding="utf-8").write("\n".join(ass))
ins = ["-ss", "%.2f" % off, "-i", v, "-i", os.path.join(H, "bezel.png")]
flt = ["color=c=0x0F2233:s=1920x1080:r=30[bg]", f"[0:v]setpts=PTS-STARTPTS,scale={SW}:{SHh}[scr]",
       f"[bg][scr]overlay={BX + PAD}:{BY + PAD}:shortest=1[a1]", f"[a1][1:v]overlay={BX}:{BY}[a2]", "[a2]subtitles=film.ass[v]"]
for k, x in enumerate(LOG):
    ins += ["-i", os.path.join(A, f"{x['i']:02d}-{x['id']}-fixed.wav")]
    flt.append(f"[{k + 2}:a]adelay={int(x['start'] * 1000 + 300)}|{int(x['start'] * 1000 + 300)}[a{k}]")
flt.append("".join(f"[a{k}]" for k in range(len(LOG))) + f"amix=inputs={len(LOG)}:normalize=0,loudnorm=I=-16:TP=-1.5[aout]")
out = os.path.join(H, "broker-edit-he.mp4")
subprocess.run([ff, "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(flt), "-map", "[v]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "21",
                "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", out], check=True, cwd=H)
print("film", out, os.path.getsize(out))
