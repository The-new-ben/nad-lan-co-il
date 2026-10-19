# -*- coding: utf-8 -*-
"""HAD-543: the English explainer film of Ashira's showroom, recorded on the LIVE page with real clicks (headed Chrome, GPU),
a drawn cursor with click ripples, English subtitles, and the narration (audio/showroom-*.wav) laid at each scene's start.
python rec_showroom.py -> showroom-en.mp4 (1920x1080)"""
import json, os, shutil, subprocess, time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "audio")
RAW = os.path.join(H, "raw-showroom"); shutil.rmtree(RAW, ignore_errors=True); os.makedirs(RAW)
N = json.load(open(os.path.join(H, "narration.json"), encoding="utf-8"))["films"]["showroom"]
D = json.load(open(os.path.join(A, "durations.json"), encoding="utf-8"))
URL = "https://nad-lan.co.il/projects/ashira-sde-dov/?nlv=film-en"
W, HH = 1440, 810
OVER = r"""(()=>{if(window.__nlov)return;window.__nlov=1;const s=document.createElement('style');s.textContent=`
#nlcur{position:fixed;left:0;top:0;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;border:3px solid #fff;background:rgba(31,95,168,.35);box-shadow:0 0 0 2px rgba(15,34,51,.6);z-index:2147483647;pointer-events:none;transition:transform .12s}
.nlrip{position:fixed;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;border:3px solid #1F5FA8;z-index:2147483646;pointer-events:none;animation:nlr .6s ease-out forwards}
@keyframes nlr{to{transform:scale(3.2);opacity:0}}
#nlsub{position:fixed;left:50%;bottom:44px;transform:translateX(-50%);max-width:1180px;z-index:2147483647;pointer-events:none;background:rgba(15,34,51,.92);color:#fff;font:500 30px/1.35 'Segoe UI',Arial,sans-serif;padding:14px 26px;border-radius:6px;text-align:center;direction:ltr}
#nlbadge{position:fixed;left:28px;top:24px;z-index:2147483647;pointer-events:none;background:#0F2233;color:#fff;font:600 20px 'Segoe UI',Arial;padding:8px 16px;border-radius:4px;direction:ltr}
#nlend{position:fixed;inset:0;z-index:2147483647;background:#0F2233;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;font-family:'Segoe UI',Arial;direction:ltr}
#nlend b{font-size:64px;letter-spacing:.5px}#nlend span{font-size:28px;color:#D9E7F7}`;document.head.appendChild(s);
const c=document.createElement('div');c.id='nlcur';document.body.appendChild(c);
addEventListener('mousemove',e=>{c.style.left=e.clientX+'px';c.style.top=e.clientY+'px'},true);
addEventListener('mousedown',e=>{c.style.transform='scale(.8)';const r=document.createElement('div');r.className='nlrip';r.style.left=e.clientX+'px';r.style.top=e.clientY+'px';document.body.appendChild(r);setTimeout(()=>r.remove(),700)},true);
addEventListener('mouseup',()=>{c.style.transform=''},true);
const b=document.createElement('div');b.id='nlbadge';b.textContent='NadLan · Ashira showroom';document.body.appendChild(b);})()"""
SUB = """t=>{let s=document.getElementById('nlsub');if(!s){s=document.createElement('div');s.id='nlsub';document.body.appendChild(s)}s.textContent=t;s.style.display=t?'block':'none'}"""
PIN = "p=>{const b=[...document.querySelectorAll('#nlps button, .nlps-stage button')].filter(e=>e.offsetParent&&e.textContent.trim()===p);if(!b.length)throw new Error('no pin '+p);return b[0].getBoundingClientRect().toJSON()}"
LOG, T0 = [], [0.0]


def glide(pg, x, y, steps=28):
    pg.mouse.move(x, y, steps=steps); pg.wait_for_timeout(180)


def click_loc(pg, loc, after=1200):
    loc.scroll_into_view_if_needed(timeout=10000); pg.wait_for_timeout(300)
    bb = loc.bounding_box()
    glide(pg, bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
    pg.mouse.down(); pg.wait_for_timeout(90); pg.mouse.up(); pg.wait_for_timeout(after)


def drag(pg, dx, cy=None, n=40):
    cx, cy = W // 2, cy or HH // 2
    glide(pg, cx + dx // 2, cy); pg.mouse.down()
    for i in range(n):
        pg.mouse.move(cx + dx // 2 - dx * i / n, cy, steps=1); pg.wait_for_timeout(35)
    pg.mouse.up()


def scene(pg, i, fn):
    sid, text = N[i]
    start = time.time() - T0[0]
    pg.evaluate(OVER); pg.evaluate(SUB, text)
    t1 = time.time()
    try:
        fn()
        ok = "ok"
    except Exception as e:  # keep filming; the log says what was skipped
        ok = "skip: " + str(e)[:80]
    left = D[f"showroom-{i:02d}-{sid}"] + 0.7 - (time.time() - t1)
    if left > 0:
        pg.wait_for_timeout(int(left * 1000))
    LOG.append({"i": i, "id": sid, "start": round(start, 2), "status": ok})
    print(i, sid, round(start, 1), ok)


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=False, args=["--window-position=0,0", "--hide-scrollbars"])
    ctx = b.new_context(viewport={"width": W, "height": HH}, locale="he-IL", record_video_dir=RAW, record_video_size={"width": 1920, "height": 1080})
    pg = ctx.new_page(); T0[0] = time.time()
    pg.goto(URL, wait_until="load", timeout=120000); pg.wait_for_timeout(2500)
    stage = pg.locator("#nlps")

    def s0():
        pg.evaluate("scrollTo(0,0)"); glide(pg, 1500, 420, 40); glide(pg, 900, 600, 40)
    def s1():
        stage.scroll_into_view_if_needed(); pg.wait_for_timeout(1500); drag(pg, 520); pg.wait_for_timeout(600)
        click_loc(pg, pg.locator('[data-nlps-step="floor"]').first, 1500)
        stage.scroll_into_view_if_needed(); pg.wait_for_timeout(500); drag(pg, -300)
    def s2():
        click_loc(pg, pg.locator('[data-nlps-step="view"]').first, 2000); stage.scroll_into_view_if_needed()
    def s3():
        stage.scroll_into_view_if_needed(); pg.wait_for_timeout(400)
        click_loc(pg, pg.locator('[data-nlps-step="inside"]').first, 4500); drag(pg, 500)
        click_loc(pg, pg.locator("button:visible", has_text="צפון").first, 2600)
        click_loc(pg, pg.locator("button:visible", has_text="מערב").first, 2000)
    def s4():
        drag(pg, -520, None, 46); pg.wait_for_timeout(500)
        LOG.append({"style_at_open": pg.evaluate("[...document.querySelectorAll('[aria-pressed=true]')].map(b=>b.textContent.trim()).join(' | ')")})
        click_loc(pg, pg.locator("button:visible", has_text="ללא ריהוט").first, 3200)
        click_loc(pg, pg.locator("button:visible", has_text="עם ריהוט").first, 2500)
        click_loc(pg, pg.locator("button:visible", has_text="אבן").first, 1500)
    def s5():
        pg.keyboard.press("Escape"); pg.wait_for_timeout(900)
        x = pg.locator(".nlat-viewer button:visible", has_text="×")
        if x.count(): click_loc(pg, x.first, 900)
        click_loc(pg, pg.locator(".nlps-facbtn").first, 1800); stage.scroll_into_view_if_needed(); pg.wait_for_timeout(600)
        r = pg.evaluate(PIN, "בריכה וכושר"); glide(pg, r["x"] + r["width"] / 2, r["y"] + r["height"] / 2)
        pg.evaluate("p=>{const b=[...document.querySelectorAll('#nlps button, .nlps-stage button')].filter(e=>e.offsetParent&&e.textContent.trim()===p);b[0].click()}", "בריכה וכושר")
        pg.mouse.down(); pg.mouse.up(); pg.wait_for_timeout(1800)
        click_loc(pg, pg.locator(":is(button,a):visible", has_text="כניסה לבריכה").first, 3500); drag(pg, 600)
    def s6():
        pg.keyboard.press("Escape"); pg.wait_for_timeout(700); pg.evaluate("scrollTo({top:0,behavior:'smooth'})"); pg.wait_for_timeout(1200)
        for t in ("לקבלת תוכניות ומחירים", "שיחת וידאו עם נציג"):
            loc = pg.locator("a:visible, button:visible", has_text=t).first; bb = loc.bounding_box(); glide(pg, bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2, 34); pg.wait_for_timeout(1500)
    def s7():
        pg.evaluate("()=>{const e=document.createElement('div');e.id='nlend';e.innerHTML='<b>Ashira · NadLan</b><span>nad-lan.co.il · illustrations for orientation only</span>';document.body.appendChild(e);const s=document.getElementById('nlsub');if(s)s.style.display='none'}")

    for i, fn in enumerate((s0, s1, s2, s3, s4, s5, s6, s7)):
        scene(pg, i, fn)
    v = pg.video.path(); ctx.close(); b.close()

ff = imageio_ffmpeg.get_ffmpeg_exe()
ins, flt = ["-i", v], []
SC = [x for x in LOG if 'i' in x]
for k, s in enumerate(SC):
    ins += ["-i", os.path.join(A, f"showroom-{s['i']:02d}-{s['id']}-fixed.wav")]
    flt.append(f"[{k + 1}:a]adelay={int(s['start'] * 1000 + 250)}|{int(s['start'] * 1000 + 250)}[a{k}]")
flt.append("".join(f"[a{k}]" for k in range(len(SC))) + f"amix=inputs={len(SC)}:normalize=0,loudnorm=I=-16:TP=-1.5[aout]")
out = os.path.join(H, "showroom-en.mp4")
subprocess.run([ff, "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(flt), "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", out], check=True)
json.dump(LOG, open(os.path.join(H, "showroom-log.json"), "w"), indent=1)
print("film", out, os.path.getsize(out))
