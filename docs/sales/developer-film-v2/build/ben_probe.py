"""Probe Ben's film: one frame per second (numbered sheets) + loudness per half second. Local only."""
import os, subprocess, sys, json, wave, struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont
FF = r"C:\Users\777\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
V = r"C:\Users\777\.claude\uploads\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\479ba69e-VID-20261101-WA0001.mp4"
S = sys.argv[1]
os.makedirs(os.path.join(S, "ben1s"), exist_ok=True)
subprocess.run([FF, "-y", "-loglevel", "error", "-i", V, "-vf", "fps=1,scale=480:-1", os.path.join(S, "ben1s", "f_%03d.jpg")], check=True)
files = sorted(f for f in os.listdir(os.path.join(S, "ben1s")) if f.startswith("f_"))
font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 22)
cols = 6
for sh in range(0, len(files), 30):
    chunk = files[sh:sh+30]
    rows = (len(chunk) + cols - 1) // cols
    W, H = 480, 270
    img = Image.new("RGB", (cols*W, rows*H), "black")
    for i, f in enumerate(chunk):
        im = Image.open(os.path.join(S, "ben1s", f)).resize((W, H))
        d = ImageDraw.Draw(im)
        t = int(f[2:5]) - 1  # fps=1 frame n covers t=n-1..n; frame at ~ (n-1)+0.5
        d.rectangle([0, 0, 70, 28], fill="black"); d.text((4, 2), f"{t}s", fill="yellow", font=font)
        img.paste(im, ((i % cols)*W, (i // cols)*H))
    img.save(os.path.join(S, f"bensheet_{sh//30+1}.jpg"), quality=85)
# audio
wav = os.path.join(S, "ben_audio16k.wav")
subprocess.run([FF, "-y", "-loglevel", "error", "-i", V, "-ac", "1", "-ar", "16000", wav], check=True)
w = wave.open(wav); n = w.getnframes(); a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
step = 8000
rms = [20*np.log10(np.sqrt(np.mean(a[i:i+step]**2)) + 1e-9) for i in range(0, len(a), step)]
print("dB per 0.5s:", " ".join(f"{r:.0f}" for r in rms))
# spectral flatness and zero-crossing as a crude voice/music hint
