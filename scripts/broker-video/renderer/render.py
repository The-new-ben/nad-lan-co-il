"""Render broker listing videos with the installed Google Chrome (no downloads, no ffmpeg).

  python render.py probe                                   # what this Chrome's MediaRecorder can encode
  python render.py stills  --broker meital-katzir --size 1080x1920 --times 0.5,5,27
  python render.py record  --broker meital-katzir --size 1080x1920 [--kbps 10000]
  python render.py frames  --video out/meital-katzir_1080x1920.mp4 --times 0.5,5,21,41,27,50
  python render.py inspect --video out/meital-katzir_1080x1920.mp4
  python render.py all     --broker meital-katzir          # both sizes + 6 check frames each

Serves this folder with `python -m http.server` on 127.0.0.1 (started and stopped here),
drives composer.html in headless Chrome through Playwright, and saves the recorded Blob.
"""
import argparse, base64, json, os, socket, struct, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
CHUNK = 4 * 1024 * 1024


# ---------------- local server ----------------
class Server:
    def __init__(self):
        s = socket.socket(); s.bind(("127.0.0.1", 0)); self.port = s.getsockname()[1]; s.close()
        self.proc = subprocess.Popen([sys.executable, "-m", "http.server", str(self.port), "--bind", "127.0.0.1",
                                      "--directory", ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{self.port}/composer.html", timeout=1).read(10)
                break
            except Exception:
                time.sleep(0.1)
        self.base = f"http://127.0.0.1:{self.port}"

    def stop(self):
        self.proc.terminate()
        try:
            self.proc.wait(5)
        except Exception:
            self.proc.kill()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.stop()


def launch(p):
    return p.chromium.launch(channel="chrome", headless=True, args=[
        "--autoplay-policy=no-user-gesture-required",
        "--disable-background-timer-throttling",
        "--disable-renderer-backgrounding",
        "--disable-backgrounding-occluded-windows",
        "--disable-frame-rate-limit",          # rAF runs faster than 60 Hz, so each 1/30 s slot is hit on time
        "--disable-gpu-vsync",
    ])


def open_composer(browser, base, broker, w, h, mode, extra=""):
    page = browser.new_page(viewport={"width": 1000, "height": 1000})
    page.on("console", lambda m: m.type in ("error", "warning") and print(f"  [console {m.type}] {m.text}"))
    page.on("pageerror", lambda e: print(f"  [pageerror] {e}"))
    page.goto(f"{base}/composer.html?broker={broker}&w={w}&h={h}&mode={mode}{extra}")
    page.wait_for_function("window.__state === 'ready' || window.__state === 'error'", timeout=180000)
    if page.evaluate("window.__state") == "error":
        raise RuntimeError(page.evaluate("window.__error"))
    return page


def save_data_url(data_url, path):
    with open(path, "wb") as f:
        f.write(base64.b64decode(data_url.split(",", 1)[1]))


def parse_size(s):
    w, h = s.lower().split("x")
    return int(w), int(h)


# ---------------- commands ----------------
def cmd_probe(args):
    from playwright.sync_api import sync_playwright
    with Server() as srv, sync_playwright() as p:
        b = launch(p)
        page = b.new_page()
        page.goto(f"{srv.base}/verify.html")
        print("Chrome", b.version)
        print(json.dumps(page.evaluate("""() => { const c = ['video/mp4;codecs=avc1', 'video/mp4;codecs=avc1.640028', 'video/mp4;codecs=avc1.4d0028',
            'video/mp4;codecs=avc1.42E028', 'video/mp4', 'video/webm;codecs=vp9', 'video/webm'];
            return Object.fromEntries(c.map(m => [m, MediaRecorder.isTypeSupported(m)])); }"""), indent=1))
        b.close()


def cmd_stills(args):
    from playwright.sync_api import sync_playwright
    w, h = parse_size(args.size)
    os.makedirs(os.path.join(ROOT, "frames"), exist_ok=True)
    with Server() as srv, sync_playwright() as p:
        b = launch(p)
        page = open_composer(b, srv.base, args.broker, w, h, "still", f"&per={args.per}&max={args.max}")
        info = page.evaluate("window.__info")
        print(json.dumps(info, ensure_ascii=False, indent=None)[:3000])
        for t in [float(x) for x in args.times.split(",")]:
            out = os.path.join(ROOT, "frames", f"still_{args.broker}_{w}x{h}_{t:05.2f}.png")
            save_data_url(page.evaluate("t => window.__drawAt(t)", t), out)
            print("saved", out)
        b.close()


def cmd_record(args, w=None, h=None):
    from playwright.sync_api import sync_playwright
    if w is None:
        w, h = parse_size(args.size)
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    with Server() as srv, sync_playwright() as p:
        b = launch(p)
        extra = f"&kbps={args.kbps}&per={args.per}&max={args.max}" + (f"&mime={args.mime}" if getattr(args, "mime", None) else "")
        page = open_composer(b, srv.base, args.broker, w, h, "record", extra)
        info = page.evaluate("window.__info")
        print(f"recording {w}x{h}, {info['duration']:.1f} s in real time ...", flush=True)
        t0 = time.time()
        stats = page.evaluate("() => window.__record()")
        print(f"  recorded in {time.time() - t0:.1f} s wall time", json.dumps(stats))
        ext = "mp4" if "mp4" in stats["mime"] else "webm"
        sfx = getattr(args, "suffix", "") or ""
        raw = os.path.join(ROOT, "out", f"{args.broker}_{w}x{h}{sfx}.recorded.{ext}")
        with open(raw, "wb") as f:
            off = 0
            while off < stats["size"]:
                f.write(base64.b64decode(page.evaluate("([o, n]) => window.__slice(o, n)", [off, CHUNK])))
                off += CHUNK
        b.close()
    final = os.path.join(ROOT, "out", f"{args.broker}_{w}x{h}{sfx}.{ext}")
    if ext == "mp4":
        from mp4tools import is_fragmented, defragment, count_samples
        if is_fragmented(raw):
            n = count_samples(raw)
            stats["encodedFrames"] = n
            # Every captured frame k shows exactly t = k/fps, so constant-rate stamps are the true timeline.
            # If the encoder skipped a frame or two, constant stamps are still smoother than the recorder's
            # wall-clock stamps (one 33 ms skip instead of jitter everywhere).
            lost = stats["frames"] - n
            cfr = stats["fps"] if 0 <= lost <= 2 else None
            info = defragment(raw, final, cfr_fps=cfr)
            print("  remuxed fragmented MP4 -> progressive MP4 (moov first):", json.dumps(info))
            if lost:
                print(f"  NOTE: {lost} captured frame(s) not encoded" + ("" if cfr else "; kept recorder timestamps"))
            os.remove(raw)
        else:
            os.replace(raw, final)
    else:
        os.replace(raw, final)
    print("  saved", final, os.path.getsize(final), "bytes")
    return final, stats


def cmd_frames(args, video=None, times=None):
    from playwright.sync_api import sync_playwright
    video = video or args.video
    times = times or [float(x) for x in args.times.split(",")]
    rel = os.path.relpath(os.path.abspath(video), ROOT).replace("\\", "/")
    name = os.path.splitext(os.path.basename(video))[0]
    os.makedirs(os.path.join(ROOT, "frames"), exist_ok=True)
    saved = []
    with Server() as srv, sync_playwright() as p:
        b = launch(p)
        page = b.new_page(viewport={"width": 1000, "height": 1000})
        page.goto(f"{srv.base}/verify.html?src={rel}")
        meta = page.evaluate("() => window.__meta()")
        print("video meta:", meta)
        for t in times:
            out = os.path.join(ROOT, "frames", f"{name}_t{t:05.2f}.png")
            save_data_url(page.evaluate("t => window.__grab(t)", t), out)
            saved.append(out)
            print("saved", out)
        b.close()
    return meta, saved


def cmd_poster(args):
    """out/<broker>_<w>x<h>_poster.jpg: the finished title card (content time 2.0 s), JPG quality --quality."""
    import io
    from PIL import Image
    from playwright.sync_api import sync_playwright
    sizes = [parse_size(s) for s in (args.sizes or "1080x1920,1920x1080").split(",")]
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    with Server() as srv, sync_playwright() as p:
        b = launch(p)
        for w, h in sizes:
            page = open_composer(b, srv.base, args.broker, w, h, "still")
            png = base64.b64decode(page.evaluate("t => window.__drawAt(t)", 2.0).split(",", 1)[1])
            page.close()
            out = os.path.join(ROOT, "out", f"{args.broker}_{w}x{h}_poster.jpg")
            Image.open(io.BytesIO(png)).convert("RGB").save(out, "JPEG", quality=args.quality, optimize=True, progressive=True)
            print("saved", out, os.path.getsize(out), "bytes")
        b.close()


def cmd_inspect(args):
    from mp4tools import describe
    print(json.dumps(describe(args.video), indent=1))


HOLD_S = 6 / 30   # composer.html holds the first and last picture 6 frames (video time = content time + 0.2 s)


def check_times(n_listings, per=4.0):
    """Video times for: 0.5 s, the middle of three listings, a cross-fade, and the outro."""
    S = lambda i: 3.0 + per * i
    picks = [0, n_listings // 2 - 1, n_listings - 2] if n_listings >= 3 else list(range(n_listings))
    t_out = 3.0 + per * n_listings
    xf = S(n_listings // 2)            # middle of a cross-fade between two listings
    return [0.5] + [round(x + HOLD_S, 3) for x in [S(i) + per / 2 for i in picks] + [xf, t_out + 3.0]]


def cmd_all(args):
    d = json.load(open(os.path.join(ROOT, "data", f"{args.broker}.json"), encoding="utf-8"))
    n = len(d["listings"]) if not args.max else min(args.max, len(d["listings"]))
    times = check_times(n, max(3.0, args.per))
    report = {}
    for size in ("1080x1920", "1920x1080"):
        w, h = parse_size(size)
        final, stats = cmd_record(args, w, h)
        meta, saved = cmd_frames(args, video=final, times=times)
        report[size] = {"file": final, "stats": stats, "meta": meta, "frames": saved}
    print(json.dumps(report, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["probe", "stills", "record", "frames", "inspect", "all", "poster"])
    ap.add_argument("--broker", default="meital-katzir")
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--times", default="0.5")
    ap.add_argument("--kbps", type=int, default=8000)
    ap.add_argument("--per", type=float, default=4.0, help="seconds per listing (min 3)")
    ap.add_argument("--max", type=int, default=0, help="only the first N listings (0 = all)")
    ap.add_argument("--mime", default=None)
    ap.add_argument("--video", default=None)
    ap.add_argument("--suffix", default="", help="output name suffix, e.g. _web (keeps other renders)")
    ap.add_argument("--sizes", default=None, help="poster sizes, e.g. 1080x1920,1920x1080")
    ap.add_argument("--quality", type=int, default=82, help="poster JPG quality")
    args = ap.parse_args()
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    {"probe": cmd_probe, "stills": cmd_stills, "record": cmd_record, "frames": cmd_frames,
     "inspect": cmd_inspect, "all": cmd_all, "poster": cmd_poster}[args.cmd](args)


if __name__ == "__main__":
    main()
