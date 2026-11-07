# -*- coding: utf-8 -*-
"""Render the developer film v3 (copied from v2's render.py; the length now comes from web/timeline.json) from film.html with the installed Chrome (Playwright, headless). Local only.

  python render.py stills <scratch>/film3 h 1.5,9,20          PNG stills at those seconds -> <scratch>/film3/stills/ (+ the
                                                              number of subtitle lines on each, which must stay <= 2)
  python render.py frames <scratch>/film3 h [--workers 4]     every frame (30 fps) -> <scratch>/film3/frames_h/00001.jpg
  python render.py encode <scratch>/film3 h <out.mp4> <mix.wav>  H.264 (CRF 17, slow) + AAC 192k, moov first
  python render.py web <film_16x9.mp4> <out.mp4> [crf]           the site page's copy: 1280x720, CRF 26, AAC 128k, moov first

film.html, the assets.json made by prep_v3.py and the JPEG sequences are served from <scratch>/film3/web by a local
http.server on 127.0.0.1 (started and stopped here). film.html is copied there from this folder on every run.
"""
import os, shutil, socket, subprocess, sys, time, urllib.request
from multiprocessing import Process

H = os.path.dirname(os.path.abspath(__file__))
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


def open_page(p, base, f):
    w, h = size(f)
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
    pg.on("pageerror", lambda e: print("  [pageerror]", e))
    pg.on("console", lambda m: m.type == "error" and print("  [console]", m.text))
    pg.goto(f"{base}/film.html?f={f}")
    pg.wait_for_function("window.READY === true", timeout=180000)
    return b, pg


def stills(S, f, times):
    from playwright.sync_api import sync_playwright
    out = os.path.join(S, "stills"); os.makedirs(out, exist_ok=True)
    srv = Server(os.path.join(S, "web"))
    try:
        with sync_playwright() as p:
            b, pg = open_page(p, srv.base, f)
            for t in times:
                pg.evaluate("t => window.render(t)", t)
                fn = os.path.join(out, f"{f}_{t:05.2f}.png")
                pg.screenshot(path=fn)
                print(fn, "subtitle lines:", pg.evaluate("window.subLines()"))
            b.close()
    finally:
        srv.stop()


def worker(base, f, frames, out):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, pg = open_page(p, base, f)
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


def frames(S, f, workers):
    out = os.path.join(S, f"frames_{f}"); os.makedirs(out, exist_ok=True)
    n = int(DUR * FPS)
    srv = Server(os.path.join(S, "web"))
    t0 = time.time()
    try:
        chunk = (n + workers - 1) // workers
        ps = [Process(target=worker, args=(srv.base, f, list(range(k * chunk, min(n, (k + 1) * chunk))), out)) for k in range(workers)]
        for q in ps:
            q.start()
        for q in ps:
            q.join()
    finally:
        srv.stop()
    done = len([x for x in os.listdir(out) if x.endswith(".jpg") and not x.endswith(".tmp.jpg")])
    print(f"{done}/{n} frames in {time.time() - t0:.0f} s -> {out}")


def encode(S, f, mp4, wav):
    src = os.path.join(S, f"frames_{f}", "%05d.jpg")
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
    if sys.argv[1] == "web":       # python render.py web <film_16x9.mp4> <out.mp4> [crf]
        web(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 26); sys.exit()
    cmd, S, f = sys.argv[1], sys.argv[2], sys.argv[3]
    import json
    DUR = json.load(open(os.path.join(S, "web", "timeline.json"), encoding="utf-8"))["duration"]
    shutil.copyfile(os.path.join(H, "film.html"), os.path.join(S, "web", "film.html"))
    if cmd == "stills":
        stills(S, f, [float(x) for x in sys.argv[4].split(",")])
    elif cmd == "frames":
        frames(S, f, int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4)
    elif cmd == "encode":
        encode(S, f, sys.argv[4], sys.argv[5])
