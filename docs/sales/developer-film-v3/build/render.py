# -*- coding: utf-8 -*-
"""Render one variant of the developer film from film.html with the installed Chrome (Playwright, headless). Local only.
(Copied from v2's render.py; the length and the scenes come from the variant's timeline.)

  python render.py stills h 1.5,9,20 [--variant <name>]      PNG stills at those seconds -> <WORK>/var/<name>/stills/ (+ the
                                                              number of subtitle lines on each, which must stay <= 2)
  python render.py frames h [--variant <name>] [--workers 4] every frame (30 fps) -> <WORK>/var/<name>/frames_h/00001.jpg
  python render.py encode h [--variant <name>]               H.264 (CRF 17, slow) + AAC 192k of <WORK>/var/<name>/audio/mix.wav,
                                                              moov first -> the variant's outputs.h (outputs.v for "v")
  python render.py web [--variant <name>]                    the site page's copy of outputs.h: 1280x720, H.264 high, CRF
                                                              (variant web.crf, default 26), AAC 128k, moov first -> outputs.web
  (no --variant: main-he, the approved film; --out <dir> writes the finished files to <dir> under the film folder instead)

film.html, assets.json (prep_v3.py), the timelines and the JPEG sequences are served from <WORK>/web by a local http.server on
127.0.0.1 (started and stopped here). film.html is copied there from this folder on every run; the page reads the variant's
timeline from ?tl=timelines/<name>.json.
"""
import os, shutil, socket, subprocess, sys, time, urllib.request
from multiprocessing import Process

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import variant as VAR
FF = r"C:\Users\777\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
FPS, DUR = 30, None   # DUR: web/timeline.json (vo_build.py)


class Server:
    def __init__(self, root):
        s = socket.socket(); s.bind(("127.0.0.1", 0)); self.port = s.getsockname()[1]; s.close()
        # a threading server with a deep listen queue: five browsers load hundreds of JPEGs at once (the default queue of 5
        # refused connections in the first run, which left one worker without its page)
        code = ("import http.server, functools, sys; H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=sys.argv[2]); "
                "S = type('S', (http.server.ThreadingHTTPServer,), {'request_queue_size': 512}); S(('127.0.0.1', int(sys.argv[1])), H).serve_forever()")
        self.p = subprocess.Popen([sys.executable, "-c", code, str(self.port), root], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{self.port}/film.html", timeout=1).read(10); break
            except Exception:
                time.sleep(0.1)
        self.base = f"http://127.0.0.1:{self.port}"

    def stop(self):
        self.p.terminate()


def size(f):
    return (1080, 1920) if f == "v" else (1920, 1080)


def open_page(p, base, f, tl="timeline.json"):
    w, h = size(f)
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
    pg.on("pageerror", lambda e: print("  [pageerror]", e))
    pg.on("console", lambda m: m.type == "error" and print("  [console]", m.text))
    pg.goto(f"{base}/film.html?f={f}&tl={tl}")
    pg.wait_for_function("window.READY === true", timeout=180000)
    return b, pg


def stills(PA, f, times):
    from playwright.sync_api import sync_playwright
    out = os.path.join(PA.work, "stills"); os.makedirs(out, exist_ok=True)
    srv = Server(VAR.WEB)
    try:
        with sync_playwright() as p:
            b, pg = open_page(p, srv.base, f, PA.tl_rel)
            for t in times:
                pg.evaluate("t => window.render(t)", t)
                fn = os.path.join(out, f"{f}_{t:05.2f}.png")
                pg.screenshot(path=fn)
                print(fn, "subtitle lines:", pg.evaluate("window.subLines()"))
            b.close()
    finally:
        srv.stop()


def worker(base, f, frames, out, tl):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, pg = open_page(p, base, f, tl)
        for i in frames:
            fn = os.path.join(out, "%05d.jpg" % (i + 1))
            if os.path.exists(fn):
                continue
            for attempt in range(4):   # a picture that failed to load is loaded again before the frame is taken
                if pg.evaluate("t => window.render(t)", i / FPS):
                    break
                print(f"  frame {i + 1}: a picture failed to load, retry {attempt + 1}")
                pg.wait_for_timeout(500)
            else:
                raise RuntimeError(f"frame {i + 1}: pictures failed to load")
            pg.screenshot(path=fn + ".tmp.jpg", type="jpeg", quality=95)
            os.replace(fn + ".tmp.jpg", fn)
        b.close()


def frames(PA, f, workers):
    out = PA.frames(f); os.makedirs(out, exist_ok=True)
    n = int(DUR * FPS)
    srv = Server(VAR.WEB)
    t0 = time.time()
    try:
        chunk = (n + workers - 1) // workers
        ps = [Process(target=worker, args=(srv.base, f, list(range(k * chunk, min(n, (k + 1) * chunk))), out, PA.tl_rel)) for k in range(workers)]
        for q in ps:
            q.start()
        for q in ps:
            q.join()
    finally:
        srv.stop()
    done = len([x for x in os.listdir(out) if x.endswith(".jpg") and not x.endswith(".tmp.jpg")])
    print(f"{done}/{n} frames in {time.time() - t0:.0f} s -> {out}")


def encode(PA, f):
    src = os.path.join(PA.frames(f), "%05d.jpg"); wav = os.path.join(PA.audio, "mix.wav"); mp4 = PA.files[f]
    os.makedirs(os.path.dirname(mp4), exist_ok=True)
    subprocess.run([FF, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", src, "-i", wav,
                    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-color_range", "tv",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", str(DUR), "-movflags", "+faststart", mp4], check=True)
    print(mp4)


def web(src, out, crf=26):
    """the site page's copy: 1280x720, H.264 high, CRF about 26, AAC 128k, moov first"""
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-profile:v", "high",
                    "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709",
                    "-color_trc", "bt709", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
    print(out, f"{os.path.getsize(out) / 1e6:.1f} MB")


if __name__ == "__main__":
    import json
    VA = VAR.load(); PA = VAR.Paths(VA); cmd = sys.argv[1]
    if cmd == "web":
        web(PA.files["h"], PA.files["web"], int(VA.get("web", {}).get("crf", 26))); sys.exit()
    f = sys.argv[2]
    DUR = json.load(open(PA.tl_web, encoding="utf-8"))["duration"]
    shutil.copyfile(os.path.join(H, "film.html"), os.path.join(VAR.WEB, "film.html"))
    if cmd == "stills":
        stills(PA, f, [float(x) for x in sys.argv[3].split(",")])
    elif cmd == "frames":
        frames(PA, f, int(VAR.arg("--workers", 4)))
    elif cmd == "encode":
        encode(PA, f)
