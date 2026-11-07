# Records the talking-agent demo in real Chrome (phone size) and muxes her voice back in at the exact moment the page started it.
import glob, os, subprocess, sys, time, pathlib
from playwright.sync_api import sync_playwright
FF = r"C:\Users\777\AppData\Local\Programs\Shotcut\ffmpeg.exe"
lang = sys.argv[1] if len(sys.argv) > 1 else "en"
url = pathlib.Path("demo/index.html").resolve().as_uri() + "?lang=" + lang
os.makedirs("rec", exist_ok=True); [os.remove(f) for f in glob.glob("rec/*.webm")]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=False, args=["--autoplay-policy=no-user-gesture-required"])
    ctx = b.new_context(viewport={"width": 430, "height": 932}, record_video_dir="rec", record_video_size={"width": 430, "height": 932})
    pg = ctx.new_page(); t_create = time.time()
    pg.goto(url, wait_until="load"); 
    pg.wait_for_function("window.__playedAt !== undefined", timeout=20000)
    origin, played = pg.evaluate("[performance.timeOrigin, window.__playedAt]")
    pg.wait_for_function("document.getElementById('au').ended", timeout=60000); time.sleep(1.6)
    pg.screenshot(path="rec/still-%s.png" % lang)
    ctx.close(); b.close()
off = (origin + played) / 1000.0 - t_create
webm = glob.glob("rec/*.webm")[0]; out = "rec/agent-demo-%s.mp4" % lang
subprocess.run([FF, "-y", "-loglevel", "error", "-i", webm, "-i", "greet-%s-16.wav" % lang, "-filter_complex",
                "[1:a]adelay=%d|%d,apad[a]" % (off * 1000, off * 1000), "-map", "0:v", "-map", "[a]", "-shortest",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "128k", out], check=True)
print("offset %.2fs ->" % off, out, os.path.getsize(out))
