# Presses the LIVE talking advisor in real Chrome on a phone size, the way a visitor meets it: she pops up, the visitor taps the page,
# she speaks. Records the screen, adds her voice at the exact moment it started, checks the card does not cover the WhatsApp bar.
import glob, json, os, subprocess, time
from playwright.sync_api import sync_playwright
FF = r"C:\Users\777\AppData\Local\Programs\Shotcut\ffmpeg.exe"
URL = "https://nad-lan.co.il/en/buy-property-in-israel/?pl=%d" % time.time()
os.makedirs("rec-live", exist_ok=True); [os.remove(f) for f in glob.glob("rec-live/*.webm")]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=False)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2,
                        record_video_dir="rec-live", record_video_size={"width": 390, "height": 844})
    ctx.add_init_script("""(()=>{const o=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){const r=o.apply(this,arguments);
      if(r&&r.then)r.then(()=>{window.__playedAt=performance.now()}).catch(e=>{window.__blocked=(window.__blocked||0)+1});return r}})()""")
    pg = ctx.new_page(); t0 = time.time(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
    pg.goto(URL, wait_until="domcontentloaded", timeout=120000); time.sleep(4.5)
    pg.screenshot(path="rec-live/1-popped.png")
    st = pg.evaluate("""() => { const c=document.getElementById('nlag'); const r=c.getBoundingClientRect();
        const t=document.getElementById('nlagt'); const fixed=[...document.querySelectorAll('body *')].filter(e=>{const s=getComputedStyle(e);return s.position==='fixed'&&e.id!=='nlag'&&e.offsetHeight>30&&e.getBoundingClientRect().bottom>innerHeight-120});
        return {on:c.classList.contains('on'), top:Math.round(r.top), bottom:Math.round(r.bottom), tapShown:getComputedStyle(t).display, blocked:window.__blocked||0,
                bars: fixed.map(e=>({cls:(e.className||'').toString().slice(0,40), top:Math.round(e.getBoundingClientRect().top), h:e.offsetHeight})).slice(0,4), sw:document.documentElement.scrollWidth}}""")
    pg.mouse.click(195, 110)  # the visitor taps the page (not the card)
    pg.wait_for_function("window.__playedAt !== undefined", timeout=15000)
    origin, played = pg.evaluate("[performance.timeOrigin, window.__playedAt]")
    time.sleep(13.5); pg.screenshot(path="rec-live/2-after.png")
    st["errors"] = errs; ctx.close(); b.close()
off = (origin + played) / 1000.0 - t0
webm = glob.glob("rec-live/*.webm")[0]; out = "rec-live/agent-live-en.mp4"
subprocess.run([FF, "-y", "-loglevel", "error", "-i", webm, "-i", "greet-en-16.wav", "-filter_complex", "[1:a]adelay=%d|%d,apad[a]" % (off * 1000, off * 1000),
                "-map", "0:v", "-map", "[a]", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-b:a", "128k", out], check=True)
st["offset"] = round(off, 2); print(json.dumps(st, ensure_ascii=False, indent=1)); print(out, os.path.getsize(out))
