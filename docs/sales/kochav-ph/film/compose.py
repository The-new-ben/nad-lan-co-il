# -*- coding: utf-8 -*-
"""The Kochav HaTzafon film (English, 1920x1080, 30 fps). Ben 20.10.2026: a day in the life, the centre, the bridge, the park, the
home, friends on the terrace, the area's numbers (never the home's price), Meital's voice (temporary voice until her recording).
Sources: Meital's own reels (the home, filmed, no music taken), the 3D world (the planned bridge), photoreal stills made from the 3D
frames (the city's layout) and lifestyle stills (illustrations). Every illustration is tagged on screen.
  python compose.py [--fast]   -> kochav-film-en.mp4"""
import json, os, shutil, subprocess, sys
import imageio_ffmpeg
H = os.path.dirname(os.path.abspath(__file__)); FF = imageio_ffmpeg.get_ffmpeg_exe()
REELS = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\kochav\reels"
TMP = os.path.join(H, "_build"); os.makedirs(TMP, exist_ok=True)
FAST = "--fast" in sys.argv
PRESET = "veryfast" if FAST else "slow"
N = json.load(open(os.path.join(H, "narration.json"), encoding="utf-8"))
D = json.load(open(os.path.join(H, "audio", "durations.json")))
GRADE = "eq=contrast=1.05:saturation=1.07:gamma=0.98,vignette=PI/5"
XF = 0.5  # crossfade between scenes


def ff(*a):
    subprocess.run([FF, "-y", "-loglevel", "error", *a], check=True, cwd=H)


def still(name, dur, z0=1.0, z1=1.12, fx=0.5, fy=0.5, dx=0.0, out=None):
    """Ken Burns on a 3:2 still: cropped to 16:9, 4K inside, eased zoom and drift."""
    n = int(round(dur * 30)); out = out or os.path.join(TMP, "s_%s_%d.mp4" % (name, n))
    if os.path.exists(out): return out
    src = os.path.join(H, "stills", name + ".png")
    e = "(on/%d)" % max(1, n - 1); ease = "(%s*%s*(3-2*%s))" % (e, e, e)
    z = "%f+(%f)*%s" % (z0, z1 - z0, ease)
    x = "(iw-iw/zoom)*(%f+%f*%s)" % (fx, dx, ease); y = "(ih-ih/zoom)*%f" % fy
    ff("-loop", "1", "-i", src, "-vf", "crop=1536:864:0:80,scale=3840:2160:flags=lanczos,zoompan=z='%s':x='%s':y='%s':d=%d:s=1920x1080:fps=30,%s,format=yuv420p" % (z, x, y, n, GRADE),
       "-frames:v", str(n), "-c:v", "libx264", "-preset", PRESET, "-crf", "16", out)
    return out


def seq(name, start=0, count=None, out=None):
    """A rendered 3D shot (1920x1080 frames)."""
    d = os.path.join(H, "shots3d", name); fs = sorted(os.listdir(d)); count = count or len(fs) - start
    out = out or os.path.join(TMP, "q_%s_%d_%d.mp4" % (name, start, count))
    if os.path.exists(out): return out
    ff("-framerate", "30", "-start_number", str(start), "-i", os.path.join(d, "f%05d.jpg"), "-frames:v", str(count), "-vf", GRADE + ",format=yuv420p", "-c:v", "libx264", "-preset", PRESET, "-crf", "16", out)
    return out


def reel(k, t0, t1, speed=1.0, band=0.40, out=None):
    """Meital's vertical footage: a 16:9 band (clear of the burned-in text and logo), sharpened; slow motion by motion interpolation."""
    a, b = int(t0 * 30), int(t1 * 30); out = out or os.path.join(TMP, "r_%s_%d_%d_%s.mp4" % (k, a, b, str(speed).replace(".", "")))
    if os.path.exists(out): return out
    y0 = int(1920 * band)
    vf = "crop=1054:593:8:%d,scale=1920:1080:flags=lanczos,unsharp=5:5:0.6" % y0
    if speed != 1.0: vf += ",setpts=PTS/%f,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir" % speed
    ff("-framerate", "30", "-start_number", str(a), "-i", os.path.join(REELS, k, "f%05d.jpg"), "-frames:v", str(b - a), "-vf", vf + "," + GRADE + ",format=yuv420p",
       "-c:v", "libx264", "-preset", PRESET, "-crf", "16", out)
    return out


def dur(p):
    r = subprocess.run([FF, "-i", p], capture_output=True, text=True, cwd=H).stderr
    import re
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r); return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def join(parts, out, xf=0.35):
    """Shots inside a scene: short crossfades."""
    if os.path.exists(out): return out
    ins = []; [ins.extend(["-i", p]) for p in parts]
    if len(parts) == 1: shutil.copy(parts[0], out); return out
    f = []; acc = dur(parts[0]); prev = "0:v"
    for i in range(1, len(parts)):
        lab = "v%d" % i; f.append("[%s][%d:v]xfade=transition=fade:duration=%f:offset=%f[%s]" % (prev, i, xf, acc - xf, lab)); acc += dur(parts[i]) - xf; prev = lab
    ff(*ins, "-filter_complex", ";".join(f), "-map", "[%s]" % prev, "-c:v", "libx264", "-preset", PRESET, "-crf", "16", "-pix_fmt", "yuv420p", out)
    return out


# ---------------- the scenes: shots, chapter title, tag per shot ----------------
S = [
 ("open", "KOCHAV HATZAFON", [(still, ("real_aerial", 4.6, 1.0, 1.10, 0.5, 0.35, 0.10), "Illustration"), (reel, ("r2", 2.0, 4.2, 0.8, 0.36), "")]),
 ("morning", "MORNING", [(still, ("morning", 6.2, 1.04, 1.14, 0.35, 0.5, 0.2), "Illustration"), (reel, ("r2", 23.4, 26.0, 0.9, 0.42), "")]),
 ("centre", "THE NEIGHBOURHOOD CENTRE", [(still, ("real_centre", 4.2, 1.0, 1.10, 0.6, 0.5, -0.2), "Illustration"), (still, ("cafe", 3.6, 1.06, 1.14, 0.4, 0.5, 0.15), "Illustration"),
    (still, ("deli", 2.4, 1.05, 1.12, 0.5, 0.5, 0.0), "Illustration"), (still, ("nuts", 2.4, 1.10, 1.02, 0.5, 0.5, 0.0), "Illustration")]),
 ("bridge", "THE BRIDGE TO YARKON PARK", [(still, ("real_bridge_top", 5.2, 1.0, 1.12, 0.45, 0.45, 0.1), "Planned bridge · illustration"), (seq, ("walk", 40, 140), "Planned bridge · 3D illustration"),
    (still, ("real_bridge_day", 6.4, 1.10, 1.0, 0.5, 0.5, 0.0), "Planned bridge · illustration")]),
 ("park", "YARKON PARK", [(still, ("park_run", 3.8, 1.02, 1.12, 0.5, 0.5, 0.1), "Illustration"), (still, ("sport", 3.6, 1.08, 1.0, 0.5, 0.5, 0.0), "Illustration"),
    (still, ("park_family", 3.8, 1.0, 1.10, 0.5, 0.5, -0.1), "Illustration")]),
 ("home", "THE HOME", [(reel, ("r2", 6.0, 8.8, 0.9, 0.30), ""), (reel, ("r2", 9.2, 11.4, 0.85, 0.30), ""), (reel, ("r2", 11.0, 12.8, 0.8, 0.30), ""), (reel, ("r2", 16.0, 17.6, 0.85, 0.30), ""), (reel, ("r1", 2.0, 4.4, 0.9, 0.30), ""),
    (reel, ("r2", 18.0, 18.9, 0.6, 0.38), "")]),
 ("terrace", "THE TERRACE", [(reel, ("r2", 20.6, 22.6, 0.75, 0.40), ""), (reel, ("r1", 17.0, 19.6, 0.85, 0.40), ""), (still, ("bbq", 6.0, 1.0, 1.10, 0.5, 0.5, 0.0), "Illustration")]),
 ("numbers", "THE NUMBERS", [(still, ("real_aerial", 12.5, 1.12, 1.24, 0.3, 0.4, 0.3), "Illustration"), (still, ("night", 19.0, 1.0, 1.12, 0.5, 0.5, 0.0), "Illustration")]),
 ("close", "", [(seq, ("night", 30, 180), "Planned bridge · 3D illustration"), (reel, ("r2", 27.0, 29.8, 0.55, 0.38), "")]),
]

scene_files, scene_d, shot_tags = [], [], []
for sid, title, shots in S:
    parts = []
    for fn, args, tag in shots:
        p = fn(*args); parts.append(p)
    # the scene is at least as long as its narration plus air
    need = D[sid] + (1.6 if sid != "close" else 6.5)
    total = sum(dur(p) for p in parts) - 0.35 * (len(parts) - 1)
    if total < need:  # stretch: hold the last shot (a slower Ken Burns or a frozen tail)
        last = parts[-1]; ext = need - total + 0.05
        out = last.replace(".mp4", "_ext%d.mp4" % int(ext * 100))
        if not os.path.exists(out):
            ff("-i", last, "-vf", "tpad=stop_mode=clone:stop_duration=%f" % ext, "-c:v", "libx264", "-preset", PRESET, "-crf", "16", "-pix_fmt", "yuv420p", out)
        parts[-1] = out
    sf = join(parts, os.path.join(TMP, "scene_%s.mp4" % sid))
    if sid == "numbers":  # a soft dark gradient from the left, under the number cards
        g = os.path.join(TMP, "grad.png")
        if not os.path.exists(g):
            from PIL import Image
            import numpy as np
            x = np.linspace(0, 1, 1920); al = (np.clip(1 - x / 0.62, 0, 1) ** 1.6 * 0.78 * 255).astype("uint8")
            im = np.zeros((1080, 1920, 4), "uint8"); im[..., 3] = al[None, :]; Image.fromarray(im, "RGBA").save(g)
        sg = sf.replace(".mp4", "_g.mp4")
        if not os.path.exists(sg):
            ff("-i", sf, "-i", g, "-filter_complex", "[0:v][1:v]overlay=0:0,format=yuv420p", "-c:v", "libx264", "-preset", PRESET, "-crf", "16", sg)
        sf = sg
    scene_files.append(sf); scene_d.append(dur(sf))
    # where each shot sits inside the scene (for its tag)
    t = 0.0; tl = []
    for p, (fn, args, tag) in zip(parts, shots):
        d_ = dur(p); tl.append((t, t + d_ - 0.35, tag)); t += d_ - 0.35
    shot_tags.append(tl)
print("scenes", [round(x, 2) for x in scene_d])

# ---------------- all scenes: crossfades, then the titles, captions, numbers and end card ----------------
starts = []; acc = 0.0
for i, d_ in enumerate(scene_d):
    starts.append(acc); acc += d_ - (XF if i < len(scene_d) - 1 else 0)
TOTAL = acc
body = os.path.join(TMP, "body.mp4")
ins = []; [ins.extend(["-i", p]) for p in scene_files]
f = []; prev = "0:v"; off = 0.0
for i in range(1, len(scene_files)):
    off += scene_d[i - 1] - XF; lab = "b%d" % i
    f.append("[%s][%d:v]xfade=transition=fade:duration=%f:offset=%f[%s]" % (prev, i, XF, off, lab)); prev = lab
ff(*ins, "-filter_complex", ";".join(f), "-map", "[%s]" % prev, "-c:v", "libx264", "-preset", PRESET, "-crf", "16", "-pix_fmt", "yuv420p", body)


def ts(t):
    t = max(0, t); return "%d:%02d:%05.2f" % (t // 3600, (t % 3600) // 60, t % 60)


ACC = "&H00BFB34F"  # sea teal (BGR)
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 0", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Chap,Bahnschrift,40,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,9,0,1,0,2,7,110,110,92,1",
       "Style: Big,Bahnschrift,104,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,1,0,0,0,100,100,2,0,1,0,3,1,110,110,250,1",
       "Style: Sub,Bahnschrift,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,3,14,0,2,260,260,64,1",
       "Style: Tag,Segoe UI,22,&H00E6E6E6,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,1,0,1,0,1,9,60,60,46,1",
       "Style: Num,Bahnschrift,118,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,1,0,0,0,100,100,0,0,1,0,3,1,110,110,330,1",
       "Style: Lab,Segoe UI Semilight,38,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,0,0,1,0,2,1,112,110,270,1",
       "Style: Src,Segoe UI,22,&H00D0D0D0,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,1,0,1,0,1,1,114,110,236,1",
       "Style: End1,Bahnschrift,66,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,1,0,0,0,100,100,2,0,1,0,3,5,110,110,0,1",
       "Style: End2,Segoe UI Semilight,36,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,0,0,1,0,2,5,110,110,0,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ev = lambda a, b, st, txt, l=0: ass.append("Dialogue: %d,%s,%s,%s,,0,0,0,,%s" % (l, ts(a), ts(b), st, txt))
for (sid, title, shots), st, d_, tl in zip(S, starts, scene_d, shot_tags):
    if title and sid != "open":
        ev(st + 0.3, st + 4.2, "Chap", "{\\fad(400,500)}{\\c%s}━━{\\c&H00FFFFFF}  %s" % (ACC, title))
    for a, b, tag in tl:
        if tag: ev(st + a + 0.2, st + b - 0.1, "Tag", "{\\fad(300,300)}" + tag)
    # captions: the narration, sentence by sentence, timed by length
    text = dict(N["scenes"])[sid]; import re
    sents = [s.strip() for s in re.split(r"(?<=[.!?:])\s+", text) if s.strip()]
    t0 = st + 0.5; L = sum(len(s) for s in sents)
    for s_ in sents:
        dd = D[sid] * len(s_) / L
        ev(t0, t0 + dd - 0.05, "Sub", s_); t0 += dd
# the opening title
ev(0.6, 5.6, "Big", "{\\an1\\pos(110,690)\\fad(700,700)}KOCHAV HATZAFON")
ev(1.0, 5.6, "Lab", "{\\an7\\pos(113,712)\\fad(700,700)}{\\c%s}━━{\\c&H00FFFFFF}  A mini penthouse in north Tel Aviv, between the city and Yarkon Park" % ACC)
# the numbers, one card at a time over the numbers scene
i_num = [s[0] for s in S].index("numbers"); n0 = starts[i_num] + 0.8; nd = scene_d[i_num] - 1.6
CARDS = [("NIS 49–51K", "per m², the average home in Kochav HaTzafon", "Bizportal, July 2026"),
         ("NIS 90K+", "per m², new homes in the neighbourhood", "Bizportal, July 2026"),
         ("16,000", "new homes planned in the Sde Dov quarter, to the north", "Approved plan, Tel Aviv District Committee"),
         ("+$136", "per m² for homes within 100 m of Yarkon Park", "Technion study, Shefer & Zakai, 2003"),
         ("+5% to 20%+", "home values next to new city park links abroad", "HR&A Advisors, 2014")]
# the cards follow the narration's sentences: [average, new] on the 2nd sentence, [Sde Dov] on the 3rd, [Technion, abroad] on the 4th
txt = dict(N["scenes"])["numbers"]; import re as _re
sn = [x.strip() for x in _re.split(r"(?<=[.!?:])\s+", txt) if x.strip()]; Ls = sum(len(x) for x in sn); bounds = []; t_ = starts[i_num] + 0.5
for x in sn: dd = D["numbers"] * len(x) / Ls; bounds.append((t_, t_ + dd)); t_ += dd
slots = [(bounds[1][0], (bounds[1][0] + bounds[1][1]) / 2), ((bounds[1][0] + bounds[1][1]) / 2, bounds[1][1]), bounds[2],
         (bounds[3][0], (bounds[3][0] + bounds[3][1]) / 2), ((bounds[3][0] + bounds[3][1]) / 2, starts[i_num] + scene_d[i_num] - 0.6)]
for k, (big, lab, src) in enumerate(CARDS):
    a, b = slots[k][0] + 0.05, slots[k][1] - 0.05
    ev(a, b, "Num", "{\\an1\\pos(110,700)\\fad(350,300)}" + big, 2); ev(a + 0.15, b, "Lab", "{\\an7\\pos(113,722)\\fad(350,300)}" + lab, 2); ev(a + 0.3, b, "Src", "{\\an7\\pos(115,778)\\fad(350,300)}" + src, 2)
ev(n0, n0 + nd, "Tag", "{\\fad(300,300)}Area data, not a valuation of this home")
# the end card
e0 = TOTAL - 6.2
ass.append("Dialogue: 1,%s,%s,End1,,0,0,0,,{\\fad(600,0)}{\\pos(960,400)}Mini penthouse · Kochav HaTzafon" % (ts(e0), ts(TOTAL)))
ass.append("Dialogue: 1,%s,%s,End2,,0,0,0,,{\\fad(600,0)}{\\pos(960,490)}5 rooms  ·  197 m²  ·  74 m² sun terrace  ·  3 exposures  ·  floor 11 of 12" % (ts(e0 + 0.3), ts(TOTAL)))
ass.append("Dialogue: 1,%s,%s,End2,,0,0,0,,{\\fad(600,0)}{\\pos(960,600)}{\\c%s}Private viewing{\\c&H00FFFFFF}   Meital Katzir · Nadlan Al HaYam · +972 52-363-1582" % (ts(e0 + 0.6), ts(TOTAL), ACC))
ass.append("Dialogue: 1,%s,%s,End2,,0,0,0,,{\\fad(600,0)}{\\pos(960,680)}nad-lan.co.il" % (ts(e0 + 0.9), ts(TOTAL)))
open(os.path.join(H, "film.ass"), "w", encoding="utf-8").write("\n".join(ass))

# ---------------- sound: the narration on its scenes, the music bed under it ----------------
mus = os.path.join(H, "audio", "music_final.wav")
mus = mus if os.path.exists(mus) else os.path.join(H, "audio", "music_temp.wav")
ains = ["-i", body, "-i", mus]; af = []
for i, (sid, _, _) in enumerate(S):
    ains += ["-i", os.path.join(H, "audio", "%02d-%s-fixed.wav" % ([s[0] for s in N["scenes"]].index(sid), sid))]
    ms = int((starts[i] + 0.5) * 1000); af.append("[%d:a]adelay=%d|%d,aformat=channel_layouts=stereo[n%d]" % (i + 2, ms, ms, i))
af.append("".join("[n%d]" % i for i in range(len(S))) + "amix=inputs=%d:normalize=0,asplit=2[nar][nar2]" % len(S))
af.append("[1:a]atrim=0:%f,afade=t=in:d=2,afade=t=out:st=%f:d=4,volume=0.42[mb]" % (TOTAL, TOTAL - 4))
af.append("[mb][nar]sidechaincompress=threshold=0.04:ratio=6:attack=40:release=600[duck]")
af.append("[duck][nar2]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.2[aout]")
out = os.path.join(H, "kochav-film-en.mp4")
ff(*ains, "-filter_complex", ";".join(["[0:v]drawbox=x=0:y=0:w=1920:h=1080:color=black@0.5:t=fill:enable='gte(t,%f)',subtitles=film.ass:fontsdir=C\\\\:/Windows/Fonts,fade=t=in:d=0.8,fade=t=out:st=%f:d=1.2[v]" % (TOTAL - 6.4, TOTAL - 1.2)] + af),
   "-map", "[v]", "-map", "[aout]", "-c:v", "libx264", "-preset", PRESET, "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
   "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", "%f" % TOTAL, out)
print("film:", out, round(TOTAL, 2), "s")
