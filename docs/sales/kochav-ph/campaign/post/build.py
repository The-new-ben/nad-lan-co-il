# -*- coding: utf-8 -*-
"""The organic Facebook post for the Kochav HaTzafon mini penthouse (29.10.2026), in he / en / fr / ru:
- reel-9x16.mp4  (Reels and Stories, 1080x1920, ~24 s): Meital's real photos and her own footage in a square window, the words
  in the top band inside the Reels safe zone (Meta: keep text out of the top 14% and the bottom 35%), the broker card at the end;
- feed-4x5.mp4   (feed, 1080x1350): the same cut;
- cover-4x5.jpg  (the post's single image, if the video is not used) and card-1..6.jpg (1080x1080, a multi-photo post).
Real media only: every photo and clip was taken in the home or from it; the plan card is labelled as a rendering of the
architect's plan. The design is the listing's own (plan-sheet ink and sea blue; Noto Serif / Assistant / Noto Sans), not a
template look. Text is laid out as HTML (exact Hebrew, French and Russian typography) and rendered by Edge, the video by ffmpeg.
  python build.py [he en fr ru] [--stills-only]"""
import io, json, os, re, shutil, subprocess, sys, urllib.request
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from post_copy import IMG  # noqa: E402
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); KP = os.path.dirname(os.path.dirname(H))
REAL = os.path.join(KP, "tour", "real"); MEI = os.path.join(KP, "_private-research", "meital-sources")
DYRL = os.path.join(MEI, "ig_DYRLyC6NVyS_01_fresh-2026-10-22.mp4")   # Meital's square reel (interior and terraces), picture only
TMP = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\post\tmp"
os.makedirs(TMP, exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()
LANGS = [a for a in sys.argv[1:] if not a.startswith("--")] or ["he", "en", "fr", "ru"]
INK, DEEP, SEA, MIST = "#14212B", "#1F4B5C", "#2F6F86", "#C9D6DE"
FONTS = ("https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@500;600&family=Assistant:wght@400;600;700;800"
         "&family=Noto+Serif:wght@500;600&family=Noto+Sans:wght@400;500;600;700&display=block")
P = lambda f: os.path.join(REAL, f)
PLAN = os.path.join(KP, "plan", "web", "img", "dollhouse.jpg")  # the rendering of the architect's plan as published (media 8663)
# the cut: (kind, source, from, to or seconds); the end card follows
SEGS = [("photo", P("L07_DV6aYANjLBm_02.jpg"), 0, 3.4), ("clip", DYRL, 3.0, 7.5), ("clip", DYRL, 12.0, 16.0),
        ("clip", DYRL, 23.5, 29.0), ("photo", P("L07_DX9wx4ziADM_08.jpg"), 0, 3.6)]
END_PHOTO, END_S, XF = P("L07_DX9wx4ziADM_03.jpg"), 4.6, 0.4
CARDS = [P("L07_DV6aYANjLBm_02.jpg"), P("L07_DV6aYANjLBm_01.jpg"), P("L07_DZp43r5DIou_04.jpg"), PLAN, P("L07_DX9wx4ziADM_08.jpg")]
URI = lambda p: "file:///" + p.replace("\\", "/")


def fam(c):
    he = c["dir"] == "rtl"
    return ('"Noto Serif Hebrew",Georgia,serif' if he else '"Noto Serif",Georgia,serif',
            'Assistant,"Segoe UI",Arial,sans-serif' if he else '"Noto Sans","Segoe UI",Arial,sans-serif')


def page(c, w, h, body, transparent=False):
    serif, sans = fam(c)
    return ('<!doctype html><html lang="x" dir="%s"><head><meta charset="utf-8"><link rel="stylesheet" href="%s"><style>'
            ':root{--sans:%s}*{box-sizing:border-box;margin:0}html,body{width:%dpx;height:%dpx;overflow:hidden;background:%s}'
            'body{font-family:%s;color:#fff;-webkit-font-smoothing:antialiased;position:relative}'
            '.serif{font-family:%s;font-weight:600}.k{font:700 30px/1.25 %s;color:#8FC1D4;letter-spacing:.03em}'
            '.chip{position:absolute;display:inline-flex;align-items:center;gap:10px;padding:10px 18px;border-radius:999px;background:rgba(20,33,43,.78);'
            'font:600 26px/1 %s;color:#fff;backdrop-filter:blur(4px)}.chip i{width:10px;height:10px;border-radius:50%%;background:#7FD1AE;display:inline-block}'
            '.photo{position:absolute;object-fit:cover;display:block}.fit{white-space:nowrap;min-width:0;overflow:hidden;width:100%%;padding-bottom:.16em;margin-bottom:-.16em}'
            '</style></head><body>%s<script>document.fonts.ready.then(function(){document.querySelectorAll(".fit").forEach(function(e){e.style.textWrap="nowrap";var s=parseFloat(getComputedStyle(e).fontSize),m=+(e.dataset.min||40);while(e.scrollWidth>e.clientWidth+1&&s>m){s-=1;e.style.fontSize=s+"px"}if(e.scrollWidth>e.clientWidth+1)e.style.textWrap="balance"});document.body.setAttribute("data-fit","1")})</script></body></html>') % (c["dir"], FONTS, sans, w, h, "transparent" if transparent else INK, sans, serif, sans, sans, body)


def band916(c, k):
    t, s = c["segs"][k]
    bars = "".join('<i style="flex:1;height:5px;border-radius:3px;background:%s"></i>' % ("#8FC1D4" if j <= k else "rgba(255,255,255,.18)") for j in range(5))
    return page(c, 1080, 1920, (
        '<div style="position:absolute;left:0;right:0;top:0;height:640px;background:%s"></div>' % INK +
        '<div style="position:absolute;inset-inline:64px;top:286px;display:grid;gap:12px">'
        '<div class="k">%s</div><div class="serif fit" data-min="50" style="font-size:%dpx;line-height:1.1;text-wrap:balance">%s</div>'
        '<div style="font:500 33px/1.32 var(--sans);color:%s;text-wrap:balance">%s</div></div>' % (c["kicker"], 74 if len(t) < 26 else 62, t, MIST, s) +
        # the broker line sits in the safe zone (Meta: nothing that matters in the top 14% or the bottom 35% of a Reel)
        '<div style="position:absolute;inset-inline:66px;top:552px;font:600 25px/1.3 var(--sans);color:#8FC1D4">%s · %s</div>' % (c["end"][1], c["lic_short"]) +
        '<div style="position:absolute;inset-inline:66px;top:604px;display:flex;gap:8px">%s</div>' % bars +
        '<span class="chip" style="top:664px;left:66px"><i></i>%s</span>' % c["real"] +
        '<div style="position:absolute;left:0;right:0;top:1720px;bottom:0;background:%s"></div>' % INK), True)


def band45(c, k):
    t, s = c["segs"][k]
    return page(c, 1080, 1350, (
        '<div style="position:absolute;left:0;right:0;top:0;height:270px;background:%s"></div>' % INK +
        '<div style="position:absolute;inset-inline:56px;top:36px;display:grid;gap:8px">'
        '<div class="k" style="font-size:26px">%s</div><div class="serif fit" data-min="40" style="font-size:%dpx;line-height:1.1;text-wrap:balance">%s</div>'
        '<div style="font:500 28px/1.3 var(--sans);color:%s">%s</div></div>' % (c["kicker"], 58 if len(t) < 30 else 50, t, MIST, s) +
        '<span class="chip" style="top:294px;left:26px;font-size:24px"><i></i>%s</span>' % c["real"] +
        '<div style="position:absolute;left:0;right:0;bottom:0;height:150px;background:linear-gradient(0deg,rgba(20,33,43,.88),rgba(20,33,43,0))"></div>'
        '<div style="position:absolute;inset-inline:56px;bottom:26px;font:600 25px/1.3 var(--sans);color:%s">%s · %s</div>' % (MIST, c["end"][1], c["lic_short"])), True)


def end_card(c, w, h):
    cta, name, tel, lic, facts = c["end"]
    top = 300 if h == 1920 else 170
    return page(c, w, h, (
        '<img class="photo" src="%s" style="inset:0;width:100%%;height:100%%;filter:brightness(.42) saturate(.9)">' % URI(END_PHOTO) +
        '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,33,43,.55),rgba(20,33,43,.2) 45%%,rgba(20,33,43,.75))"></div>'
        '<div style="position:absolute;inset-inline:70px;top:%dpx;display:grid;gap:22px;text-align:center;justify-items:center">' % top +
        '<div class="k" style="font-size:32px">%s</div>' % cta +
        '<div class="serif" style="font-size:%dpx;line-height:1.15">%s</div>' % (58 if h == 1920 else 52, name) +
        '<div style="font:800 %dpx/1 var(--sans);letter-spacing:.01em;direction:ltr;unicode-bidi:isolate">%s</div>' % (104 if h == 1920 else 92, tel) +
        '<div style="width:120px;height:3px;background:#8FC1D4;margin:6px 0"></div>'
        '<div style="font:600 32px/1.4 var(--sans);color:%s;max-width:860px;text-wrap:balance">%s</div>' % (MIST, facts) +
        '<div style="font:500 27px/1.4 var(--sans);color:%s">%s</div>' % (MIST, lic) +
        '<div style="font:700 30px/1 var(--sans);color:#fff;margin-top:%dpx;letter-spacing:.02em">%s</div></div>' % (40 if h == 1920 else 18, c["brand"])))


def cover45(c):
    t, s, chips = c["cover"]
    ch = "".join('<span style="padding:10px 18px;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);font:700 27px/1 var(--sans)">%s</span>' % x for x in chips)
    return page(c, 1080, 1350, (
        '<img class="photo" src="%s" style="left:0;right:0;top:206px;width:1080px;height:1144px;object-position:50%% 55%%">' % URI(SEGS[0][1]) +
        '<div style="position:absolute;inset-inline:56px;top:34px;display:grid;gap:10px">'
        '<div class="k" style="font-size:26px">%s</div><div class="serif fit" data-min="40" style="font-size:%dpx;line-height:1.08;text-wrap:balance">%s</div>'
        '<div style="font:500 28px/1.3 var(--sans);color:%s">%s</div></div>' % (c["kicker"], 58, t, MIST, s) +
        '<span class="chip" style="top:230px;left:26px;font-size:24px"><i></i>%s</span>' % c["real"] +
        '<div style="position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(0deg,rgba(20,33,43,.92),rgba(20,33,43,0))"></div>'
        '<div style="position:absolute;inset-inline:56px;bottom:84px;display:flex;flex-wrap:wrap;gap:10px">%s</div>' % ch +
        '<div style="position:absolute;inset-inline:56px;bottom:30px;font:600 25px/1.3 var(--sans);color:%s">%s · %s · %s</div>' % (MIST, c["end"][1], c["end"][2], c["lic_short"])))


def card11(c, i):
    if i == 5:
        return end_card(c, 1080, 1080)
    t, s = c["cards"][i]
    chip = c["render"] if i == 3 else c["real"]
    return page(c, 1080, 1080, (
        ('<div style="position:absolute;inset:0;background:#EEF2F4"></div><img class="photo" src="%s" style="left:0;top:96px;width:1080px;height:720px;object-fit:contain">' % URI(CARDS[i])
         if i == 3 else '<img class="photo" src="%s" style="inset:0;width:100%%;height:100%%">' % URI(CARDS[i])) +
        '<span class="chip" style="top:26px;left:26px;font-size:24px"><i style="%s"></i>%s</span>' % ("background:#8FC1D4" if i == 3 else "", chip) +
        '<div style="position:absolute;left:0;right:0;bottom:0;height:330px;background:linear-gradient(0deg,rgba(20,33,43,.92),rgba(20,33,43,0))"></div>'
        '<div style="position:absolute;inset-inline:56px;bottom:84px;display:grid;gap:10px">'
        '<div class="serif fit" data-min="44" style="font-size:60px;line-height:1.08;text-wrap:balance">%s</div>'
        '<div style="font:500 29px/1.35 var(--sans);color:%s;text-wrap:balance">%s</div></div>' % (t, MIST, s) +
        '<div style="position:absolute;inset-inline:56px;bottom:28px;font:600 23px/1.3 var(--sans);color:%s">%s · %s · %d/6</div>' % (MIST, c["end"][1].split(" · ")[0], c["lic_short"], i + 1)))  # the broker as a broker, not the publisher's domain


def shoot(pg, html, path, w, h, transparent=False):
    f = os.path.join(TMP, "p.html"); io.open(f, "w", encoding="utf-8").write(html)
    pg.set_viewport_size({"width": w, "height": h}); pg.goto(URI(f), wait_until="networkidle")
    pg.wait_for_selector("body[data-fit]", timeout=20000); pg.wait_for_timeout(200)
    pg.screenshot(path=path, omit_background=transparent, type="png")


def ff(*a):
    subprocess.run([FF, "-y", "-loglevel", "error", *[str(x) for x in a]], check=True, cwd=TMP)


ENC = ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30"]


def square_clip(k, kind, src, a, b):
    """1080x1080, 30 fps: a photo with an eased push-in (4K inside), or a piece of Meital's reel, lifted blacks put back."""
    out = os.path.join(TMP, "sq%d.mp4" % k)
    if os.path.exists(out): return out
    if kind == "photo":
        n = int(round(b * 30)); e = "(on/%d)" % (n - 1); ease = "(%s*%s*(3-2*%s))" % (e, e, e)
        ff("-loop", "1", "-i", src, "-vf", "format=rgb24,crop='min(iw,ih)':'min(iw,ih)',scale=2160:2160:flags=lanczos,"
           "zoompan=z='1+0.07*%s':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)*0.45':d=%d:s=1080x1080:fps=30,eq=contrast=1.04:saturation=1.05" % (ease, n),
           "-frames:v", n, *ENC, out)
    else:
        n = int(round((b - a) * 30))
        ff("-ss", "%.3f" % a, "-t", "%.3f" % (b - a + 0.2), "-i", src, "-an", "-vf",
           "scale=1080:1080:flags=lanczos,unsharp=5:5:0.7,eq=contrast=1.06:saturation=1.12:gamma=0.98", "-frames:v", n, *ENC, out)
    return out


def full(k, sq, ov, w, h, y, out):
    n = int(round((SEGS[k][3] if SEGS[k][0] == "photo" else SEGS[k][3] - SEGS[k][2]) * 30))
    ff("-i", sq, "-i", ov, "-filter_complex", "color=c=0x14212B:s=%dx%d:r=30[bg];[bg][0:v]overlay=0:%d:shortest=1[v];[v][1:v]overlay=0:0,format=yuv420p" % (w, h, y),
       "-frames:v", n, *ENC, out)


def still_full(png, secs, w, h, out):
    n = int(round(secs * 30)); e = "(on/%d)" % (n - 1)
    ff("-loop", "1", "-i", png, "-vf", "scale=%d:%d:flags=lanczos,zoompan=z='1+0.025*%s':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=%d:s=%dx%d:fps=30,format=yuv420p"
       % (w * 2, h * 2, e, n, w, h), "-frames:v", n, *ENC, out)


def join(parts, out, durs):
    ins = []; [ins.extend(["-i", p]) for p in parts]
    fc, last, t = [], "0:v", 0.0
    for i in range(1, len(parts)):
        t += durs[i - 1] - XF
        fc.append("[%s][%d:v]xfade=transition=fade:duration=%.2f:offset=%.3f[x%d]" % (last, i, XF, t, i)); last = "x%d" % i
    ff(*ins, "-filter_complex", ";".join(fc), "-map", "[%s]" % last, *ENC, out)
    return t + durs[-1]


def music(secs, out):
    wav = os.path.join(TMP, "music_%d.wav" % int(secs * 10))
    if not os.path.exists(wav):
        os.makedirs(os.path.join(TMP, "audio"), exist_ok=True)
        subprocess.run([sys.executable, os.path.join(KP, "film", "music_temp.py"), "%.1f" % (secs + 1)], check=True, cwd=TMP)
        shutil.move(os.path.join(TMP, "audio", "music_temp.wav"), wav)
    return wav


with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge"); pg = b.new_page(); pg2 = b.new_page(device_scale_factor=4 / 3)
    for lang in LANGS:
        c = IMG[lang]; O = os.path.join(H, "out", lang); os.makedirs(O, exist_ok=True)
        shoot(pg2, cover45(c), os.path.join(TMP, "cover.png"), 1080, 1350)
        for i in range(6):
            shoot(pg2, card11(c, i), os.path.join(TMP, "card%d.png" % i), 1080, 1080)
        if "--stills-only" not in sys.argv:
            for k in range(5):
                shoot(pg, band916(c, k), os.path.join(TMP, "b916_%s_%d.png" % (lang, k)), 1080, 1920, True)
                shoot(pg, band45(c, k), os.path.join(TMP, "b45_%s_%d.png" % (lang, k)), 1080, 1350, True)
            shoot(pg, end_card(c, 1080, 1920), os.path.join(TMP, "e916_%s.png" % lang), 1080, 1920)
            shoot(pg, end_card(c, 1080, 1350), os.path.join(TMP, "e45_%s.png" % lang), 1080, 1350)
        from PIL import Image
        Image.open(os.path.join(TMP, "cover.png")).convert("RGB").save(os.path.join(O, "cover-4x5.jpg"), quality=92)
        for i in range(6):
            Image.open(os.path.join(TMP, "card%d.png" % i)).convert("RGB").save(os.path.join(O, "card-%d.jpg" % (i + 1)), quality=92)
        print(lang, "stills written", flush=True)
    b.close()

if "--stills-only" in sys.argv: sys.exit(0)
sqs = [square_clip(k, *s) for k, s in enumerate(SEGS)]
durs = [s[3] if s[0] == "photo" else s[3] - s[2] for s in SEGS] + [END_S]
for lang in LANGS:
    O = os.path.join(H, "out", lang)
    for fmt, (w, h, y) in (("9x16", (1080, 1920, 640)), ("4x5", (1080, 1350, 270))):
        tag = "b916" if fmt == "9x16" else "b45"
        parts = []
        for k in range(5):
            out = os.path.join(TMP, "f_%s_%s_%d.mp4" % (lang, fmt, k)); full(k, sqs[k], os.path.join(TMP, "%s_%s_%d.png" % (tag, lang, k)), w, h, y, out); parts.append(out)
        out = os.path.join(TMP, "f_%s_%s_end.mp4" % (lang, fmt)); still_full(os.path.join(TMP, "%s_%s.png" % ("e916" if fmt == "9x16" else "e45", lang)), END_S, w, h, out); parts.append(out)
        silent = os.path.join(TMP, "v_%s_%s.mp4" % (lang, fmt)); T = join(parts, silent, durs)
        wav = music(T, None)
        final = os.path.join(O, ("reel-9x16.mp4" if fmt == "9x16" else "feed-4x5.mp4"))
        ff("-i", silent, "-i", wav, "-filter_complex", "[1:a]atrim=0:%.2f,afade=t=in:d=0.8,afade=t=out:st=%.2f:d=1.6,loudnorm=I=-16:TP=-1.5:LRA=11[a]" % (T, T - 1.6),
           "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", final)
        print(lang, fmt, "video %.1f s" % T, os.path.getsize(final) // 1024, "KB", flush=True)
