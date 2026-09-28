"""Render a project's video with the installed Google Chrome (no downloads, no ffmpeg).

  python render.py probe                                          # what this Chrome's MediaRecorder can encode
  python render.py stills  --project rainbow-tel-aviv --size 1080x1920 --times 1.5,8,30   # PNG stills, no recording
  python render.py record  --project rainbow-tel-aviv --size 1920x1080 [--kbps 10000] [--suffix _web]
  python render.py frames  --video out/rainbow-tel-aviv_1920x1080.mp4 --times 0.5,5,21
  python render.py poster  --project rainbow-tel-aviv [--sizes 1080x1920,1920x1080] [--quality 82]
  python render.py inspect --video out/rainbow-tel-aviv_1920x1080.mp4
  python render.py all     --project rainbow-tel-aviv              # everything below, both sizes

`all` = high-quality takes (--kbps, default 10000) + web takes (--web-kbps, default 2500, name suffix _web) for
1920x1080 and 1080x1920, posters (JPG q82), and the check frames (the composer's own list: every scene once its text
is in, each view, one crossfade, the outro) decoded from the high-quality files into frames/.

Serves this folder with `python -m http.server` on 127.0.0.1 (started and stopped here), drives composer.html in
headless Chrome through Playwright and saves the recorded Blob. Chrome's fragmented MP4 is remuxed to a progressive
MP4 with the index (moov) first, byte for byte (tools/mp4tools.py), never re-encoded.
"""
import argparse, base64, io, json, os, socket, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
CHUNK = 4 * 1024 * 1024
HOLD_S = 6 / 30   # composer.html holds the first and last picture 6 frames (video time = content time + 0.2 s)


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
        "--disable-frame-rate-limit",
        "--disable-gpu-vsync",
    ])


def open_composer(browser, base, project, w, h, mode, extra=""):
    page = browser.new_page(viewport={"width": 1000, "height": 1000})
    page.on("console", lambda m: m.type in ("error", "warning") and print(f"  [console {m.type}] {m.text}"))
    page.on("pageerror", lambda e: print(f"  [pageerror] {e}"))
    page.goto(f"{base}/composer.html?project={project}&w={w}&h={h}&mode={mode}{extra}")
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
        page = open_composer(b, srv.base, args.project, w, h, "still", f"&fonts={args.fonts}")
        info = page.evaluate("window.__info")
        print(json.dumps(info, ensure_ascii=False)[:4000])
        times = [float(x) for x in args.times.split(",")] if args.times else info["checks"]
        for t in times:
            out = os.path.join(ROOT, "frames", f"still_{args.project}_{w}x{h}_{t:05.2f}.png")
            save_data_url(page.evaluate("t => window.__drawAt(t)", t), out)
            print("saved", out)
        b.close()


def cmd_record(args, w=None, h=None, kbps=None, suffix=None):
    from playwright.sync_api import sync_playwright
    if w is None:
        w, h = parse_size(args.size)
    kbps = kbps or args.kbps
    sfx = args.suffix if suffix is None else suffix
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    with Server() as srv, sync_playwright() as p:
        b = launch(p)
        extra = f"&kbps={kbps}&fonts={args.fonts}" + (f"&mime={args.mime}" if getattr(args, "mime", None) else "")
        page = open_composer(b, srv.base, args.project, w, h, "record", extra)
        info = page.evaluate("window.__info")
        print(f"recording {w}x{h} at {kbps} kbps, {info['duration']:.1f} s in real time (fonts: {info['fonts']}) ...", flush=True)
        t0 = time.time()
        stats = page.evaluate("() => window.__record()")
        print(f"  recorded in {time.time() - t0:.1f} s wall time", json.dumps(stats))
        ext = "mp4" if "mp4" in stats["mime"] else "webm"
        raw = os.path.join(ROOT, "out", f"{args.project}_{w}x{h}{sfx}.recorded.{ext}")
        with open(raw, "wb") as f:
            off = 0
            while off < stats["size"]:
                f.write(base64.b64decode(page.evaluate("([o, n]) => window.__slice(o, n)", [off, CHUNK])))
                off += CHUNK
        b.close()
    final = os.path.join(ROOT, "out", f"{args.project}_{w}x{h}{sfx}.{ext}")
    if ext == "mp4":
        from mp4tools import is_fragmented, defragment, count_samples
        if is_fragmented(raw):
            n = count_samples(raw)
            stats["encodedFrames"] = n
            lost = stats["frames"] - n
            cfr = stats["fps"] if 0 <= lost <= 2 else None
            remux = defragment(raw, final, cfr_fps=cfr)
            print("  remuxed fragmented MP4 -> progressive MP4 (moov first):", json.dumps(remux))
            if lost:
                print(f"  NOTE: {lost} captured frame(s) not encoded" + ("" if cfr else "; kept recorder timestamps"))
            os.remove(raw)
        else:
            os.replace(raw, final)
    else:
        os.replace(raw, final)
    print("  saved", final, os.path.getsize(final), "bytes")
    return final, stats, info


def cmd_frames(args, video=None, times=None):
    from playwright.sync_api import sync_playwright
    video = video or args.video
    if not times and not args.times:
        raise SystemExit("frames: pass --times (seconds, comma separated)")
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
    """out/<project>_<w>x<h>_poster.jpg: the finished title card (content time --poster-t, default 2.0 s)."""
    from PIL import Image
    from playwright.sync_api import sync_playwright
    sizes = [parse_size(s) for s in (args.sizes or "1080x1920,1920x1080").split(",")]
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    with Server() as srv, sync_playwright() as p:
        b = launch(p)
        for w, h in sizes:
            page = open_composer(b, srv.base, args.project, w, h, "still", f"&fonts={args.fonts}")
            png = base64.b64decode(page.evaluate("t => window.__drawAt(t)", args.poster_t).split(",", 1)[1])
            page.close()
            out = os.path.join(ROOT, "out", f"{args.project}_{w}x{h}_poster.jpg")
            Image.open(io.BytesIO(png)).convert("RGB").save(out, "JPEG", quality=args.quality, optimize=True, progressive=True)
            print("saved", out, os.path.getsize(out), "bytes")
        b.close()


def cmd_inspect(args):
    from mp4tools import describe
    print(json.dumps(describe(args.video), indent=1))


def cmd_all(args):
    from mp4tools import describe
    report = {}
    for size in ("1920x1080", "1080x1920"):
        w, h = parse_size(size)
        final, stats, info = cmd_record(args, w, h, kbps=args.kbps, suffix="")
        web, wstats, _ = cmd_record(args, w, h, kbps=args.web_kbps, suffix="_web")
        times = [round(t + HOLD_S, 3) for t in info["checks"]]
        meta, saved = cmd_frames(args, video=final, times=times)
        report[size] = {"hq": describe(final), "web": describe(web), "stats": stats, "web_stats": wstats,
                        "meta": meta, "frames": saved}
    cmd_poster(args)
    print(json.dumps(report, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["probe", "stills", "record", "frames", "inspect", "all", "poster"])
    ap.add_argument("--project", default="rainbow-tel-aviv")
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--times", default=None, help="comma list of seconds (stills: default = the composer's check list)")
    ap.add_argument("--kbps", type=int, default=10000)
    ap.add_argument("--web-kbps", type=int, default=2500)
    ap.add_argument("--mime", default=None)
    ap.add_argument("--video", default=None)
    ap.add_argument("--suffix", default="", help="output name suffix, e.g. _web (keeps other renders)")
    ap.add_argument("--sizes", default=None, help="poster sizes, e.g. 1080x1920,1920x1080")
    ap.add_argument("--quality", type=int, default=82, help="poster JPG quality")
    ap.add_argument("--poster-t", type=float, default=2.0, help="content time of the poster picture")
    ap.add_argument("--fonts", default="strict", choices=["strict", "fallback"])
    args = ap.parse_args()
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    {"probe": cmd_probe, "stills": cmd_stills, "record": cmd_record, "frames": cmd_frames,
     "inspect": cmd_inspect, "all": cmd_all, "poster": cmd_poster}[args.cmd](args)


if __name__ == "__main__":
    main()
