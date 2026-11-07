# -*- coding: utf-8 -*-
"""Contact sheet of a finished cut: one frame every <step> seconds, decoded from the MP4 itself, with its time.

  python sheet.py <film.mp4> <out.jpg> [--step 3] [--cols 6]
"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

FF = r"C:\Users\777\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
mp4, out = sys.argv[1], sys.argv[2]
step = float(sys.argv[sys.argv.index("--step") + 1]) if "--step" in sys.argv else 3.0
cols = int(sys.argv[sys.argv.index("--cols") + 1]) if "--cols" in sys.argv else 6
r = subprocess.run([FF, "-hide_banner", "-i", mp4], capture_output=True, text=True).stderr
h, m, s = r.split("Duration: ")[1].split(",")[0].split(":"); dur = int(h) * 3600 + int(m) * 60 + float(s)
font = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 26)
tiles = []
with tempfile.TemporaryDirectory() as td:
    t = 0.5
    while t < dur:
        fn = os.path.join(td, "f.png")
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", fn], check=True)
        im = Image.open(fn).convert("RGB")
        im.thumbnail((480, 480))
        d = ImageDraw.Draw(im); lab = f"{int(t // 60)}:{t % 60:04.1f}"
        d.rectangle([0, 0, 112, 34], fill="#12202A"); d.text((8, 3), lab, fill="#FFFFFF", font=font)
        tiles.append(im); t += step
w, hh = tiles[0].size
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (w + 8) + 8, rows * (hh + 8) + 8), "#D3DCE2")
for i, im in enumerate(tiles):
    sheet.paste(im, (8 + (i % cols) * (w + 8), 8 + (i // cols) * (hh + 8)))
sheet.save(out, quality=86)
print(out, len(tiles), "frames", f"{dur:.2f} s")
