# Face + transparent mouth/blink patches for the talking-agent demo (same method as HAD-680 make_assets.py, new face).
import json, os
from PIL import Image, ImageDraw, ImageFilter
OUT = "demo"; CROP = (196, 90, 884, 778); S = 512 / (CROP[2] - CROP[0])
MOUTH = (450, 450, 630, 590); EYES = (420, 300, 660, 385); PAD = 22
def to512(b): return [round((b[0] - CROP[0]) * S), round((b[1] - CROP[1]) * S), round((b[2] - CROP[0]) * S), round((b[3] - CROP[1]) * S)]
base = Image.open("base.png").convert("RGB")
base.crop(CROP).resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, "face.webp"), quality=86, method=6)
meta = {"size": 512, "patches": {}}
for name in ["B", "C", "D", "E", "F", "G", "BLINK"]:
    box = EYES if name == "BLINK" else MOUTH
    outer = (box[0] - PAD, box[1] - PAD, box[2] + PAD, box[3] + PAD)
    fr = Image.open(f"frame-{name}.png").convert("RGB")
    feather = Image.new("L", base.size, 0); ImageDraw.Draw(feather).ellipse(box, fill=255); feather = feather.filter(ImageFilter.GaussianBlur(14))
    patch = fr.crop(outer).convert("RGBA"); patch.putalpha(feather.crop(outer))
    b = to512(outer); w, h = b[2] - b[0], b[3] - b[1]
    patch.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, f"m-{name}.webp"), quality=88, method=6)
    meta["patches"][name] = {"x": b[0], "y": b[1], "w": w, "h": h}
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"))
print(json.dumps(meta))
