"""Contact sheet of frames: python tools/sheet.py OUT.jpg IMG1 IMG2 ... [--cols N] [--w PX]"""
import sys
from PIL import Image, ImageDraw
args = sys.argv[1:]
cols, tw = 4, 400
if "--cols" in args: i = args.index("--cols"); cols = int(args[i + 1]); del args[i:i + 2]
if "--w" in args: i = args.index("--w"); tw = int(args[i + 1]); del args[i:i + 2]
out, files = args[0], args[1:]
ims = [Image.open(f).convert("RGB") for f in files]
th = int(tw * ims[0].height / ims[0].width)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (tw + 8), rows * (th + 26)), "white")
d = ImageDraw.Draw(sheet)
for k, (f, im) in enumerate(zip(files, ims)):
    x, y = (k % cols) * (tw + 8), (k // cols) * (th + 26)
    sheet.paste(im.resize((tw, th)), (x, y + 22))
    d.text((x + 4, y + 4), f.replace("\\", "/").split("/")[-1], fill="black")
sheet.save(out, quality=88)
print(out, sheet.size)
