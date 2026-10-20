# -*- coding: utf-8 -*-
"""Edit of the broker self-edit film from rec_broker.py's recording (rec-log.json): a large phone frame, step titles, a step
progress bar, subtitles and the Hebrew narration. python compose_broker.py -> broker-edit-he.mp4"""
import json, os, subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "audio")
N = json.load(open(os.path.join(H, "narration.json"), encoding="utf-8"))["scenes"]
D = json.load(open(os.path.join(A, "durations.json")))
R = json.load(open(os.path.join(H, "rec-log.json"), encoding="utf-8")); LOG = R["log"]; v = R["video"]; off = R["off"]
# ---------------- the frame, titles, subtitles, narration ----------------
ff = imageio_ffmpeg.get_ffmpeg_exe()
SW, SHh = 480, 1040; BX, BY = 190, 4; PAD = 14
bez = Image.new("RGBA", (SW + 2 * PAD, SHh + 2 * PAD), (0, 0, 0, 0)); d = ImageDraw.Draw(bez)
d.rounded_rectangle([0, 0, SW + 2 * PAD - 1, SHh + 2 * PAD - 1], radius=64, fill=(10, 16, 22, 255))
d.rounded_rectangle([PAD, PAD, PAD + SW - 1, PAD + SHh - 1], radius=48, fill=(0, 0, 0, 0))
mask = Image.new("L", bez.size, 0); ImageDraw.Draw(mask).rounded_rectangle([PAD, PAD, PAD + SW - 1, PAD + SHh - 1], radius=48, fill=255)
bez.save(os.path.join(H, "bezel.png"))
ends = [LOG[k + 1]["start"] if k + 1 < len(LOG) else LOG[k]["start"] + D[f"{LOG[k]['i']:02d}-{LOG[k]['id']}"] + 1.2 for k in range(len(LOG))]
def ts(t): return "%d:%02d:%05.2f" % (t // 3600, (t % 3600) // 60, t % 60)
ass = ["[Script Info]", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 0", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: K,Arial,34,&H00C9E2EA,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,1,0,1,0,0,9,820,110,250,177",
       "Style: T,Arial,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,9,820,110,300,177",
       "Style: S,Arial,44,&H00FFFFFF,&H00FFFFFF,&H005C4B1F,&H005C4B1F,0,0,0,0,100,100,0,0,3,18,0,3,820,110,200,177",
       "Style: B,Arial,28,&H00C9E2EA,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,3,820,110,60,177", "", "[Events]",
       "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
total = len(N) - 2
for k, x in enumerate(LOG):
    title, text = N[x["i"]][1], N[x["i"]][2]
    a, e = x["start"] + 0.15, ends[k] - 0.05
    if 0 < x["i"] < len(N) - 1:
        ass.append(f"Dialogue: 0,{ts(a)},{ts(e)},K,,0,0,0,,שלב {x['i']} מתוך {total}")
    ass.append(f"Dialogue: 0,{ts(a)},{ts(e)},T,,0,0,0,,{title}")
    ass.append(f"Dialogue: 0,{ts(a + 0.2)},{ts(e)},S,,0,0,0,,{text}")
ass.append(f"Dialogue: 0,{ts(0)},{ts(ends[-1])},B,,0,0,0,,nad-lan.co.il · ניהול מודעות למתווכים · התמונות והמודעות בסרטון הן לדוגמה")
open(os.path.join(H, "film.ass"), "w", encoding="utf-8").write("\n".join(ass))
ins = ["-ss", "%.2f" % off, "-i", v, "-i", os.path.join(H, "bezel.png")]
flt = ["color=c=0x0F2233:s=1920x1080:r=30[bg]", f"[0:v]setpts=PTS-STARTPTS,scale={SW}:{SHh}[scr]",
       f"[bg][scr]overlay={BX + PAD}:{BY + PAD}:shortest=1[a1]", f"[a1][1:v]overlay={BX}:{BY}[a2]", "[a2]subtitles=film.ass[a3]"]
# the step bar: 11 segments; the current one light, the done ones mid, the rest dark
steps = [x for x in LOG if 0 < x["i"] < len(N) - 1]
X0, X1, Y, G = 820, 1810, 960, 8; nseg = len(N) - 2; W = (X1 - X0 - G * (nseg - 1)) / nseg
bars = []
for k, x in enumerate(LOG):
    if not (0 < x["i"] < len(N) - 1): continue
    a, e = x["start"], ends[k]
    for j in range(1, nseg + 1):
        col = "0x6FB3C9" if j == x["i"] else ("0x2F6F86" if j < x["i"] else "0x26404F")
        xx = int(X1 - j * W - (j - 1) * G)   # right to left: step 1 at the right
        bars.append(f"drawbox=x={xx}:y={Y}:w={int(W)}:h=10:color={col}:t=fill:enable='between(t,{a:.2f},{e:.2f})'")
flt[-1] = flt[-1].replace("[a3]", "[a3]")
flt.append("[a3]" + (",".join(bars) if bars else "null") + "[v]")
for k, x in enumerate(LOG):
    ins += ["-i", os.path.join(A, f"{x['i']:02d}-{x['id']}-fixed.wav")]
    flt.append(f"[{k + 2}:a]adelay={int(x['start'] * 1000 + 300)}|{int(x['start'] * 1000 + 300)}[a{k}]")
flt.append("".join(f"[a{k}]" for k in range(len(LOG))) + f"amix=inputs={len(LOG)}:normalize=0,loudnorm=I=-16:TP=-1.5[aout]")
out = os.path.join(H, "broker-edit-he.mp4")
subprocess.run([ff, "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(flt), "-map", "[v]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "21",
                "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", out], check=True, cwd=H)
print("film", out, os.path.getsize(out))
