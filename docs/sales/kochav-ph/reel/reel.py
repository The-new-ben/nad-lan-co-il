# -*- coding: utf-8 -*-
"""Kochav HaTzafon mini penthouse: a 21-second square reel from Meital's REAL photos only (Ben, 5.11.2026).

Reference: a developer reel for a boutique building (Brodetsky 29) built from architectural renders, six shots of about
3 s, a slow camera move on each, one short caption with a number, an end card with the brand and "לפרטים נוספים".
This home exists and is photographed, so every interior and terrace frame is Meital's own photograph
(memory: real listing = real media). Nothing is generated: the photos only move (push-in or pan), cross-fade, and get
one shared light grade. The aerial frame is labelled as a photo of the neighbourhood, never as the view from the home.
No price (Ben's film rule), no tenancy, no address or building exterior (the building is kept private).

  python reel.py [--music path.mp3] [--out path.mp4]
"""
import io, os, subprocess, sys
from PIL import Image, ImageEnhance, ImageFilter
import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(HERE, "..", "tour", "real")
FF = imageio_ffmpeg.get_ffmpeg_exe()
S, FPS = 1080, 30
SHOT, XF, END = 3.3, 0.3, 3.0
ARGS = sys.argv[1:]
MUSIC = ARGS[ARGS.index("--music") + 1] if "--music" in ARGS else None
OUT = ARGS[ARGS.index("--out") + 1] if "--out" in ARGS else os.path.join(HERE, "_build", "kochav-reel-1080.mp4")

# (photo, move, focus x 0..1, caption, small tag)
SHOTS = [
    ("L07_DV6aYANjLBm_02.jpg", "pan-l", 0.55, "מיני פנטהאוז בכוכב הצפון", ""),
    ("L07_DV6aYANjLBm_01.jpg", "pan-r", 0.45, "5 חדרים · 197 מ״ר", ""),
    ("L07_DX9wx4ziADM_03.jpg", "push", 0.5, "קומה 11 · מרפסות לנוף העיר", ""),
    ("L07_DX9wx4ziADM_01.jpg", "push", 0.5, "מטבח פתוח עם אי", ""),
    ("L07_DX9wx4ziADM_04.jpg", "push", 0.5, "ממ״ד, חניה ומחסן", ""),
    ("L07_DZp43r5DIou_09.jpg", "push-out", 0.5, "כוכב הצפון, ליד פארק הירקון", "צילום אוויר של השכונה"),
]


def grade(im):
    """One shared light grade so the six photos read as one film: a touch of contrast and warmth, nothing moved."""
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.04)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.02)))
    b = b.point(lambda v: int(v * 0.98))
    return Image.merge("RGB", (r, g, b))


def load(name):
    im = Image.open(os.path.join(REAL, name)).convert("RGB")
    return grade(im)


def frame_at(im, move, fx, p):
    """A crop window that moves smoothly (sub-pixel, bicubic): p goes 0..1 over the shot. Eased."""
    e = p * p * (3 - 2 * p)
    w, h = im.size
    side0 = min(w, h)
    if move == "push":
        side = side0 * (1.0 - 0.09 * e)
        cx, cy = w * fx, h / 2
    elif move == "push-out":
        side = side0 * (0.91 + 0.09 * e)
        cx, cy = w * fx, h / 2
    else:  # pan across a landscape photo, a slight push too
        side = side0 * (1.0 - 0.04 * e)
        span = max(0.0, w - side)
        a, b = (0.62, 0.38) if move == "pan-l" else (0.38, 0.62)
        cx = side / 2 + span * (a + (b - a) * e)
        cy = h / 2
    x0, y0 = cx - side / 2, cy - side / 2
    x0 = max(0.0, min(w - side, x0)); y0 = max(0.0, min(h - side, y0))
    return im.transform((S, S), Image.EXTENT, (x0, y0, x0 + side, y0 + side), Image.BICUBIC)


TOP = Image.new("RGBA", (S, S), (0, 0, 0, 0))
for _y in range(400):
    TOP.paste((0, 0, 0, int(150 * (1 - _y / 400) ** 1.6)), (0, _y, S, _y + 1))
LOGO = Image.open(os.path.join(HERE, "..", "film", "wm.png")).convert("RGBA")
LOGO = LOGO.crop(LOGO.getbbox()); LOGO = LOGO.resize((380, int(380 * LOGO.height / LOGO.width)), Image.LANCZOS)


def shade(fr):
    """A soft dark band at the top so the white caption reads on bright rooms (the photo itself is not changed)."""
    return Image.alpha_composite(fr.convert("RGBA"), TOP).convert("RGB")


def end_frame(im, q):
    """The end card over Meital's terrace-at-dusk photo, slowly pushing in, darkened, with the logo."""
    fr = Image.blend(frame_at(im, "push", 0.5, q), Image.new("RGB", (S, S), (10, 20, 28)), 0.55).convert("RGBA")
    fr.alpha_composite(LOGO, ((S - LOGO.width) // 2, 230))
    return fr.convert("RGB")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    ims = [load(s[0]) for s in SHOTS]
    starts = [i * (SHOT - XF) for i in range(len(SHOTS))]
    t_end = starts[-1] + SHOT - XF
    total = t_end + END
    n = int(round(total * FPS))
    endsrc = ims[0]
    silent = OUT.replace(".mp4", "-video.mp4")
    p = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{S}x{S}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    for k in range(n):
        t = k / FPS
        layers = []
        for i, st in enumerate(starts):
            if st <= t < st + SHOT:
                layers.append((i, (t - st) / SHOT))
        if t >= t_end - XF:
            a = min(1.0, max(0.0, (t - (t_end - XF)) / (XF * 2)))
            eb = end_frame(endsrc, min(1.0, max(0.0, (t - t_end + XF) / (END + XF))))
            fr = Image.blend(shade(frame_at(ims[-1], SHOTS[-1][1], SHOTS[-1][2], min(1.0, (t - starts[-1]) / SHOT))), eb, a) if a < 1 else eb
        elif len(layers) == 1:
            i, q = layers[0]
            fr = shade(frame_at(ims[i], SHOTS[i][1], SHOTS[i][2], q))
        else:
            (i, q), (j, r) = layers[0], layers[1]
            a = (t - starts[j]) / XF
            fr = shade(Image.blend(frame_at(ims[i], SHOTS[i][1], SHOTS[i][2], q), frame_at(ims[j], SHOTS[j][1], SHOTS[j][2], r), max(0, min(1, a))))
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()

    def ts(x):
        return "0:%02d:%05.2f" % (int(x // 60), x % 60)
    ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {S}", f"PlayResY: {S}", "WrapStyle: 0", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Cap,Gisha,82,&H00FFFFFF,&H00FFFFFF,&H50000000,&H64000000,1,0,0,0,100,100,0,0,1,0,4,8,70,70,150,-1",
           "Style: Tag,Gisha,34,&H00FFFFFF,&H00FFFFFF,&H8C1A140A,&H8C1A140A,1,0,0,0,100,100,0,0,3,10,0,3,48,48,44,-1",
           "Style: E1,Gisha,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,5,70,70,0,-1",
           "Style: E2,Gisha,32,&H00E6E6E6,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,70,70,0,-1",
           "Style: Pill,Gisha,54,&H00FFFFFF,&H00FFFFFF,&H00866F2F,&H00866F2F,1,0,0,0,100,100,0,0,3,22,0,5,70,70,0,-1",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for i, (_, _, _, cap, tag) in enumerate(SHOTS):
        a, b = starts[i] + 0.25, starts[i] + SHOT - 0.2
        ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{{\\fad(280,220)}}{cap}")
        if tag:
            ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Tag,,0,0,0,,{{\\fad(280,220)}}{tag}")
    e0 = t_end + 0.15
    ass += [f"Dialogue: 0,{ts(e0)},{ts(total)},E1,,0,0,0,,{{\\fad(350,0)\\pos(540,480)}}מיני פנטהאוז בכוכב הצפון",
            f"Dialogue: 0,{ts(e0 + 0.2)},{ts(total)},Pill,,0,0,0,,{{\\fad(350,0)\\pos(540,630)}}  לפרטים נוספים  ",
            f"Dialogue: 0,{ts(e0 + 0.35)},{ts(total)},E2,,0,0,0,,{{\\fad(350,0)\\pos(540,790)}}מיטל קציר · נדל״ן על הים · מתווכת מקרקעין, רישיון 3131540"]
    work = os.path.dirname(OUT)
    with io.open(os.path.join(work, "reel.ass"), "w", encoding="utf-8") as f:
        f.write("\n".join(ass) + "\n")
    cmd = [FF, "-y", "-loglevel", "error", "-i", os.path.basename(silent)]
    if MUSIC:
        cmd += ["-i", MUSIC]
    vf = "ass=reel.ass"
    cmd += ["-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    if MUSIC:
        cmd += ["-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-af", f"afade=t=in:d=0.6,afade=t=out:st={total - 1.6:.2f}:d=1.6", "-shortest"]
    cmd += [os.path.basename(OUT)]
    subprocess.run(cmd, cwd=work, check=True)
    print("OUT", OUT, "seconds", round(total, 2), "frames", n)


if __name__ == "__main__":
    main()
