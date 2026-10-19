# -*- coding: utf-8 -*-
"""HAD-543: edit the two recordings of rec_call.py into call-en.mp4 with a layout per scene: side by side, or one side big
with the other as a picture in picture, plus the title bar, subtitles (call.ass) and the narration."""
import json, os, subprocess
import imageio_ffmpeg
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "audio")
L = json.load(open(os.path.join(H, "call-log.json"), encoding="utf-8")); D = json.load(open(os.path.join(A, "durations.json")))
scenes = [x for x in L["log"] if "i" in x]
LAYOUT = {"intro": "sbs", "start": "rep", "join": "buyer", "live": "sbs", "follow": "sbs", "invite": "buyer", "notes": "sbs", "end": "sbs"}
def ts(t): return "%d:%02d:%05.2f" % (t // 3600, (t % 3600) // 60, t % 60)
ends = [scenes[k + 1]["start"] if k + 1 < len(scenes) else x["start"] + D[f"call-{x['i']:02d}-{x['id']}"] + 1 for k, x in enumerate(scenes)]
ass = ["[Script Info]", "PlayResX: 1920", "PlayResY: 1080", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: S,Arial,38,&H00FFFFFF,&H00FFFFFF,&H00332210,&H00332210,0,0,0,0,100,100,0,0,3,14,0,2,200,200,40,1", "", "[Events]",
       "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for x, e in zip(scenes, ends):
    if x["id"] != "end":
        ass.append(f"Dialogue: 0,{ts(x['start'] + 0.2)},{ts(e - 0.1)},S,,0,0,0,,{x['text']}")
open(os.path.join(H, "call.ass"), "w", encoding="utf-8").write("\n".join(ass))
F = "fontfile='C\\:/Windows/Fonts/arial.ttf'"; FB = "fontfile='C\\:/Windows/Fonts/arialbd.ttf'"
def lab(t, x, y, size=28, c="0xD9E7F7"): return f"drawtext={F}:text='{t}':fontcolor={c}:fontsize={size}:x={x}:y={y}"
flt = ["[0:v]setpts=PTS-STARTPTS,split=3[r1][r2][r3]", "[1:v]setpts=PTS-STARTPTS,split=3[b1][b2][b3]"]
# side by side
flt += ["[r1]scale=944:590[rs]", "[b1]scale=944:590[bs]", "color=c=0x0F2233:s=1920x1080:r=25[g1]",
        "[g1][bs]overlay=16:190:shortest=1[s1]", "[s1][rs]overlay=960:190," + lab("BUYER", "16+(944-tw)/2", 140) + "," + lab("REPRESENTATIVE", "960+(944-tw)/2", 140) + "[SBS]"]
# one side big, the other in a corner
for big, small, nb, ns, tag in (("b2", "r2", "BUYER", "REPRESENTATIVE", "BUY"), ("r3", "b3", "REPRESENTATIVE", "BUYER", "REP")):
    flt += [f"[{big}]scale=1280:800[{tag}x]", f"[{small}]scale=480:300,pad=488:308:4:4:color=white[{tag}y]", f"color=c=0x0F2233:s=1920x1080:r=25[{tag}g]",
            f"[{tag}g][{tag}x]overlay=60:140:shortest=1[{tag}1]", f"[{tag}1][{tag}y]overlay=1392:560," + lab(nb, 60, 102) + "," + lab(ns, 1396, 522, 26, "white") + f"[{tag}]"]
flt.append("[SBS]split=%d%s" % (len(scenes), "".join(f"[S{k}]" for k in range(len(scenes)))))
flt.append("[BUY]split=%d%s" % (len(scenes), "".join(f"[B{k}]" for k in range(len(scenes)))))
flt.append("[REP]split=%d%s" % (len(scenes), "".join(f"[R{k}]" for k in range(len(scenes)))))
parts = []
for k, (x, e) in enumerate(zip(scenes, ends)):
    lay = LAYOUT.get(x["id"], "sbs"); src = {"sbs": "S", "buyer": "B", "rep": "R"}[lay]
    st = 0 if k == 0 else x["start"]
    for other in "SBR":
        if other != src:
            flt.append(f"[{other}{k}]nullsink")
    flt.append(f"[{src}{k}]trim=start={st:.2f}:end={e:.2f},setpts=PTS-STARTPTS[p{k}]"); parts.append(f"[p{k}]")
flt.append("".join(parts) + f"concat=n={len(parts)}:v=1:a=0[cat]")
flt.append("[cat]drawtext=" + FB + ":text='Live video call inside the project page':fontcolor=white:fontsize=50:x=(w-tw)/2:y=40,subtitles=call.ass[v]")
ins = ["-ss", "%.2f" % L["offr"], "-i", L["rv"], "-ss", "%.2f" % L["offb"], "-i", L["bv"]]
for k, x in enumerate(scenes):
    ins += ["-i", os.path.join(A, f"call-{x['i']:02d}-{x['id']}-fixed.wav")]
    flt.append(f"[{k + 2}:a]adelay={int(x['start'] * 1000 + 250)}|{int(x['start'] * 1000 + 250)}[a{k}]")
flt.append("".join(f"[a{k}]" for k in range(len(scenes))) + f"amix=inputs={len(scenes)}:normalize=0,loudnorm=I=-16:TP=-1.5[aout]")
out = os.path.join(H, "call-en.mp4")
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(flt), "-map", "[v]", "-map", "[aout]",
                "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-pix_fmt", "yuv420p", "-r", "25", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", out], check=True, cwd=H)
print("film", out, os.path.getsize(out))
