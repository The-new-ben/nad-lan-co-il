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
        page = open_composer(b, srv.base, args.project, w, h, "still", f"&fonts={args.fonts}" + ("&narr=1" if args.narr else ""))
        info = page.evaluate("window.__info")
        print(json.dumps(info, ensure_ascii=False)[:6000])
        times = [float(x) for x in args.times.split(",")] if args.times else info["checks"]
        for t in times:
            out = os.path.join(ROOT, "frames", f"still_{args.project}_{w}x{h}{'_narrated' if args.narr else ''}_{t:05.2f}.png")
            save_data_url(page.evaluate("t => window.__drawAt(t)", t), out)
            print("saved", out)
        b.close()


def cmd_record(args, w=None, h=None, kbps=None, suffix=None, akbps=None):
    """One take; when the encoder lost more than 2 frames (a visible stutter) the take is recorded again (--retries)."""
    for attempt in range(1 + max(0, args.retries)):
        final, stats, info = _record_once(args, w, h, kbps, suffix, akbps)
        lost = stats["frames"] - (stats.get("encodedSamples", {}).get("vide") if isinstance(stats.get("encodedSamples"), dict)
                                  else stats.get("encodedFrames", stats["frames"]))
        stats["attempt"] = attempt + 1
        if lost <= 2:
            break
        print(f"  RETAKE: {lost} frames lost in take {attempt + 1}" + ("" if attempt < args.retries else " (no retries left, kept)"), flush=True)
    return final, stats, info


def _record_once(args, w=None, h=None, kbps=None, suffix=None, akbps=None):
    from playwright.sync_api import sync_playwright
    if w is None:
        w, h = parse_size(args.size)
    kbps = kbps or args.kbps
    sfx = args.suffix if suffix is None else suffix
    if args.narr and not sfx.startswith("_narrated"):
        sfx = "_narrated" + sfx
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    with Server() as srv, sync_playwright() as p:
        b = launch(p)
        extra = f"&kbps={kbps}&fonts={args.fonts}" + (f"&mime={args.mime}" if getattr(args, "mime", None) else "")
        if args.narr:
            extra += f"&narr=1&akbps={akbps or args.akbps}"
        if args.cut:
            extra += f"&cut={args.cut}"
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
    if args.keep_raw:
        import shutil
        shutil.copyfile(raw, raw + ".keep")
    if ext == "mp4" and args.narr:
        from mp4multi import defragment_multi, count_samples_multi, starts_multi
        counts = count_samples_multi(raw)
        stats["encodedSamples"] = counts
        stats["trackStarts"] = starts_multi(raw)   # the recorder's own first timestamps per track
        n = counts.get("vide", 0)
        lost = stats["frames"] - n
        remux = defragment_multi(raw, final, video_cfr_fps=stats["fps"] if 0 <= lost <= 2 else None)
        print("  remuxed fragmented MP4 (video + audio) -> progressive MP4 (moov first):", json.dumps(remux))
        if lost:
            print(f"  NOTE: {lost} captured frame(s) not encoded")
        os.remove(raw)
    elif ext == "mp4":
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


def cmd_audio(args, video=None, clips=None):
    """The narrated cut's sound: decode it in Chrome, find where each line's speech starts, compare with the plan
    (video time = 0.2 s hold + clip start + the clip's own lead-in), and save a 16 kHz WAV for a transcript."""
    from playwright.sync_api import sync_playwright
    video = video or args.video
    rel = os.path.relpath(os.path.abspath(video), ROOT).replace("\\", "/")
    name = os.path.splitext(os.path.basename(video))[0]
    os.makedirs(os.path.join(ROOT, "frames"), exist_ok=True)
    wav = os.path.join(ROOT, "frames", f"{name}_16k.wav")
    with Server() as srv, sync_playwright() as p:
        b = launch(p)
        if clips is None:
            w, h = parse_size(args.size)
            page = open_composer(b, srv.base, args.project, w, h, "still", f"&fonts={args.fonts}&narr=1")
            clips = page.evaluate("window.__info").get("narration", {}).get("clips", [])
            page.close()
        page = b.new_page()
        page.goto(f"{srv.base}/verify.html?src={rel}")
        a = page.evaluate("() => window.__audio()")
        if "error" in a:
            raise SystemExit("audio decode failed: " + a["error"])
        save_data_url("data:audio/wav;base64," + page.evaluate("() => window.__wav16k()"), wav)
        b.close()
    N = json.load(open(os.path.join(ROOT, "data", f"{args.project}.narration.json"), encoding="utf-8"))
    lead = {L["id"]: L.get("onset", (L.get("speech") or [0, 0])[0]) for L in N["lines"]}
    env = a["env"]; peak = max(env) or 1.0
    report = []
    for c in clips:
        # same rule as narrate.py's 'onset': the first 10 ms window at 5% of this line's loudest window
        exp = HOLD_S + c["start"] + lead.get(c["id"], 0)
        i0, i1 = max(0, int((exp - 0.5) * 100)), min(len(env), int((exp + 0.5) * 100))
        win = env[i0:min(len(env), i0 + int((c.get("secs", 3) + 1) * 100))]
        thr = (max(win) if win else peak) * 0.05
        hit = next((i for i in range(i0, i1) if env[i] >= thr), None)
        got = None if hit is None else hit / 100
        report.append({"id": c["id"], "expected_s": round(exp, 2), "measured_s": got, "delta_ms": None if got is None else round((got - exp) * 1000)})
    # silence where nothing should sound: before the first line
    first = min(r["expected_s"] for r in report) if report else 0
    pre = max(env[: max(1, int((first - 0.3) * 100))]) if first > 0.4 else 0
    out = {"video": video, "audio_duration_s": round(a["duration"], 3), "sample_rate": a["sampleRate"], "channels": a["channels"],
           "peak_rms": round(peak, 4), "silence_before_first_line_rms": round(pre, 5), "onsets": report, "wav16k": wav}
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out


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
    from mp4multi import describe_multi
    print(json.dumps(describe_multi(args.video), indent=1))


def cmd_all(args):
    from mp4tools import describe
    from mp4multi import describe_multi
    desc = describe_multi if args.narr else describe
    report = {}
    for size in ("1920x1080", "1080x1920"):
        w, h = parse_size(size)
        final, stats, info = cmd_record(args, w, h, kbps=args.kbps, suffix="")
        web, wstats, _ = cmd_record(args, w, h, kbps=args.web_kbps, suffix="_web", akbps=args.web_akbps)
        times = [round(t + HOLD_S, 3) for t in info["checks"]]
        meta, saved = cmd_frames(args, video=final, times=times)
        report[size] = {"hq": desc(final), "web": desc(web), "stats": stats, "web_stats": wstats,
                        "meta": meta, "frames": saved, "narration": info.get("narration")}
        if args.narr:
            clips = info["narration"]["clips"]
            report[size]["audio_hq"] = cmd_audio(args, video=final, clips=clips)
            report[size]["audio_web"] = cmd_audio(args, video=web, clips=clips)
    if not args.narr:   # the narrated cut opens on the same title card: the silent film's posters serve both
        cmd_poster(args)
    print(json.dumps(report, indent=1, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["probe", "stills", "record", "frames", "inspect", "all", "poster", "audio"])
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
    ap.add_argument("--narr", action="store_true", help="the narrated cut (data/<project>.narration.json); names get _narrated")
    ap.add_argument("--akbps", type=int, default=128, help="audio bitrate of the narrated cut")
    ap.add_argument("--web-akbps", type=int, default=96, help="audio bitrate of the narrated web cut")
    ap.add_argument("--cut", type=float, default=0, help="record only the first N seconds (tests)")
    ap.add_argument("--retries", type=int, default=2, help="record a take again when the encoder lost more than 2 frames")
    ap.add_argument("--keep-raw", action="store_true", help="keep Chrome's fragmented file as <name>.recorded.mp4.keep")
    args = ap.parse_args()
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    {"probe": cmd_probe, "stills": cmd_stills, "record": cmd_record, "frames": cmd_frames,
     "inspect": cmd_inspect, "all": cmd_all, "poster": cmd_poster, "audio": cmd_audio}[args.cmd](args)


if __name__ == "__main__":
    main()
