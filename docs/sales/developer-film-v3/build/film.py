# -*- coding: utf-8 -*-
"""ONE command that builds one version (variant) of the nad-lan developer film, start to finish. Local only, nothing uploaded.

  python build/film.py --variant <name> [--only a,b] [--from step] [--workers 5] [--out <dir>]
  python build/film.py                                    (no --variant: main-he, the approved film; an approved film is
                                                           rebuilt into out/_rebuild-<name>/, never over its published files
                                                           unless --replace-approved is given on Ben's word)

Steps, in order (each one is also its own script, see START-HERE.md):
  check    the variant's rules: no long dash, no forbidden word, each picture module once            (variant.py)
  voice    the Kokoro takes it still needs, bm_george unless the variant says otherwise              (voice_kokoro.py variant)
  mix      lay the voice, time the Hebrew subtitles, make the bed and the mix, write the timeline   (vo_build.py)
  prep     hand the timeline to the film page (and the shared pictures if they are missing)         (prep_v3.py)
  frames   every frame, 16:9 and 9:16                                                                (render.py frames h|v)
  encode   the two films                                                                             (render.py encode h|v)
  web      the 1280x720 site copy                                                                    (render.py web)
  poster   the poster frame                                                                          (poster.py)
  sheets   the two contact sheets                                                                    (sheet.py)
  subs     every subtitle line drawn once in each layout: line count <= 2 and a strip to check the RTL order by eye
  whisper  local Whisper small on the mix, line by line                                              (whisper_check.py)
--out <dir> (relative to the film folder) writes the finished files there instead of the variant's outputs.dir: a check run.

  python build/film.py --variant <name> --only dry     a draft's picture WITHOUT voice: a timeline guessed from the words
      (2.6 words a second), then one still per scene in both layouts -> <WORK>/var/<name>/dry/ (and a sheet of them). Use it to
      see a new script on screen before anything is voiced; it writes nothing into the film folder.
"""
import json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import variant as VAR

B = os.path.dirname(os.path.abspath(__file__))
STEPS = ["check", "voice", "mix", "prep", "frames", "encode", "web", "poster", "sheets", "subs", "whisper"]


def run(py, script, *a):
    extra = ["--variant", NAME] + (["--out", VAR.arg("--out")] if "--out" in sys.argv else [])
    cmd = [py, os.path.join(B, script), *a, *extra]
    print(">", " ".join(os.path.basename(x) if i < 2 else x for i, x in enumerate(cmd)), flush=True)
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    subprocess.run(cmd, check=True, env=env)


def dry(VA, PA):
    """a guessed timeline (no voice) and one still per scene, to look at a draft before voicing it"""
    from PIL import Image
    t = 0.0; scenes = []; voice = []; cues = []
    for sc in VA["scenes"]:
        a = t; t += sc.get("lead", .35)
        for k, g in enumerate(sc["groups"]):
            if k:
                t += g.get("gap", .32)
            d = max(1.2, len(g["en"].split()) / 2.6)
            voice.append({"scene": sc["id"], "k": k + 1, "a": round(t, 3), "b": round(t + d, 3), "en": g["en"]})
            n = len(g["he"])
            for j, he in enumerate(g["he"]):
                cues.append({"scene": sc["id"], "a": round(t + d * j / n, 3), "b": round(t + d * (j + 1) / n, 3), "he": he})
            t += d
        t += sc.get("tail", .55)
        scenes.append({"id": sc["id"], "a": round(a, 3), "b": round(t, 3), "pic": sc["pic"], "module": sc.get("module", sc["id"]),
                       **({"screen": sc["screen"]} if sc.get("screen") else {}), **({"subs": False} if sc.get("subs") is False else {})})
    tl = {"variant": VA["name"], "dry": True, "duration": round(t, 2), "scenes": scenes, "voice": voice, "cues": cues}
    name = "_dry-" + VA["name"]; os.makedirs(os.path.dirname(PA.tl_web), exist_ok=True)
    json.dump(tl, open(os.path.join(VAR.WEB, "timelines", name + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    times = [round(b["a"] + (b["b"] - b["a"]) * .7, 2) for b in voice if b["k"] == max(x["k"] for x in voice if x["scene"] == b["scene"])]
    out = os.path.join(PA.work, "dry"); os.makedirs(out, exist_ok=True)
    sys.path.insert(0, B)
    import render
    from playwright.sync_api import sync_playwright
    import shutil
    shutil.copyfile(os.path.join(B, "film.html"), os.path.join(VAR.WEB, "film.html"))
    srv = render.Server(VAR.WEB); shots = []
    try:
        with sync_playwright() as p:
            for f in ("h", "v"):
                b, pg = render.open_page(p, srv.base, f, "timelines/%s.json" % name)
                errs = []; pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
                for tt in times:
                    pg.evaluate("t => window.render(t)", tt); fn = os.path.join(out, f"{f}_{tt:06.2f}.png"); pg.screenshot(path=fn); shots.append((f, fn))
                b.close()
                print(f"dry {f}: {len(times)} stills, page errors: {[e for e in errs if 'Failed to load resource' not in e] or 'none'}")
    finally:
        srv.stop()
    for f in ("h", "v"):
        ims = [Image.open(fn).convert("RGB") for ff, fn in shots if ff == f]
        for im in ims:
            im.thumbnail((480, 480))
        w, h = ims[0].size; cols = 4 if f == "h" else 6; rows = (len(ims) + cols - 1) // cols
        sh = Image.new("RGB", (cols * (w + 6), rows * (h + 6)), "#888")
        for i, im in enumerate(ims):
            sh.paste(im, ((i % cols) * (w + 6), (i // cols) * (h + 6)))
        sh.save(os.path.join(out, f"dry_sheet_{f}.jpg"), quality=82)
    print("dry: about %.0f s (guessed from the words); sheets in %s" % (tl["duration"], out))


def subs_check(PA):
    """every cue drawn at its middle in both layouts: the number of lines (must be <= 2) and one strip per layout with all of them"""
    from PIL import Image
    tl = json.load(open(PA.tl_web, encoding="utf-8"))
    times = [round((c["a"] + c["b"]) / 2, 2) for c in tl["cues"] if not any(s["id"] == c["scene"] and (s.get("module") == "s16" or s.get("subs") is False) for s in tl["scenes"])]
    for f in ("h", "v"):
        out = subprocess.run([VAR.SYS_PY, os.path.join(B, "render.py"), "stills", f, ",".join(map(str, times)), "--variant", NAME],
                             capture_output=True, text=True, env=dict(os.environ, PYTHONIOENCODING="utf-8")).stdout
        lines = [l for l in out.splitlines() if "subtitle lines:" in l]
        worst = max(int(l.rsplit(":", 1)[1]) for l in lines) if lines else 0
        crops = []
        for t in times:
            im = Image.open(os.path.join(PA.work, "stills", f"{f}_{t:05.2f}.png")).convert("RGB")
            crops.append(im.crop((0, 860, 1920, 1080)) if f == "h" else im.crop((0, 1460, 1080, 1720)))
        w = crops[0].size[0]; hh = sum(c.size[1] for c in crops)
        strip = Image.new("RGB", (w, hh), "white"); y = 0
        for c in crops:
            strip.paste(c, (0, y)); y += c.size[1]
        fn = os.path.join(PA.work, f"subtitles_check_{f}.jpg"); strip.save(fn, quality=80)
        print(f"subs {f}: {len(times)} lines drawn, most lines on one cue: {worst} (must be <= 2) -> {fn}  LOOK AT IT: Hebrew reads right to left, English names in place")
        if worst > 2:
            raise SystemExit("a subtitle takes more than two lines: shorten it or split the group (\"he\": [two lines], \"split\": [fraction])")


if __name__ == "__main__":
    NAME = VAR.name(); VA = VAR.load(NAME)
    if VA.get("status", "").startswith("APPROVED") and "--out" not in sys.argv and "--replace-approved" not in sys.argv:
        # the published files of an approved film are never overwritten by a rebuild: Chrome draws a few image frames a hair
        # differently from run to run (min PSNR 48 dB on 7.11.2026), so a rebuild is the same film but not the same bytes
        sys.argv += ["--out", "out/_rebuild-" + NAME]
        print(f"{NAME} is approved and published: this rebuild goes to out/_rebuild-{NAME}/ (compare it with build/compare_films.py;"
              " replace the published files only on Ben's word, with --replace-approved)", flush=True)
    PA = VAR.Paths(VA)
    steps = VAR.arg("--only", "").split(",") if "--only" in sys.argv else STEPS[STEPS.index(VAR.arg("--from", "check")):]
    workers = VAR.arg("--workers", "5"); t0 = time.time()
    print(f"variant {NAME}: {len(VA['scenes'])} scenes; work {PA.work}; finished files -> {PA.out}", flush=True)
    for st in steps:
        if st == "check":
            bad = VAR.scenes_check(VA)
            if bad:
                raise SystemExit("variant rules broken:\n  " + "\n  ".join(bad))
            print("check ok", flush=True)
        elif st == "voice":
            run(VAR.KOKORO_PY, "voice_kokoro.py", "variant")
        elif st == "mix":
            run(VAR.KOKORO_PY, "vo_build.py")
        elif st == "prep":
            run(VAR.SYS_PY, "prep_v3.py")
        elif st == "frames":
            import shutil
            for f in ("h", "v"):
                shutil.rmtree(PA.frames(f), ignore_errors=True)   # never reuse frames of an older timeline
                run(VAR.SYS_PY, "render.py", "frames", f, "--workers", workers)
        elif st == "encode":
            for f in ("h", "v"):
                run(VAR.SYS_PY, "render.py", "encode", f)
        elif st == "web":
            run(VAR.SYS_PY, "render.py", "web")
        elif st == "poster":
            run(VAR.SYS_PY, "poster.py")
        elif st == "sheets":
            for f, cols in (("h", "7"), ("v", "10")):
                subprocess.run([VAR.SYS_PY, os.path.join(B, "sheet.py"), PA.files[f], PA.files["sheet_" + f], "--step", "3", "--cols", cols], check=True)
        elif st == "subs":
            subs_check(PA)
        elif st == "dry":
            dry(VA, PA)
        elif st == "whisper":
            run(VAR.KOKORO_PY, "whisper_check.py")
    print(f"done in {time.time() - t0:.0f} s: {PA.out}")
