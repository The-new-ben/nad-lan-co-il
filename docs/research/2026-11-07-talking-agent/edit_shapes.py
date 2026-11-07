# Mouth shapes (Rhubarb B..G) and a blink for the talking agent face (Ben 7.11, the woman): gpt-image edits inside a mask, then composited onto the
# base with a feathered mask so everything outside the mouth/eyes stays pixel-identical. Key read inside ther process only.
import base64, io, json, sys, time, uuid, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFilter
KEY = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip().splitlines()[0].strip()
MODEL = "gpt-image-2.6-sunburst"
base = Image.open("base.png").convert("RGBA")
W, H = base.size
MOUTH = (450, 450, 630, 590)      # the region a talking mouth (and jaw) may change
EYES = (420, 300, 660, 385)
SHAPES = {
 "B": "Her mouth is very slightly open, lips just parted, the edge of the upper teeth barely visible, as when saying the sound 'ee' or 's'. Same smile lines and lip colour.",
 "C": "Her mouth is open a medium amount as when saying 'eh', upper and lower teeth visible, relaxed jaw. Same lips colour and skin.",
 "D": "Her mouth is open wide as when saying 'ah', jaw dropped naturally, upper teeth and a little of the tongue visible. Same lips colour and skin.",
 "E": "Her lips are slightly rounded and open as when saying 'oh', small oval opening. Same lips colour and skin.",
 "F": "Her lips are pushed forward and rounded into a small opening as when saying 'oo'. Same lips colour and skin.",
 "G": "Her upper front teeth rest lightly on her lower lip as when saying 'f' or 'v'. Same lips colour and skin.",
 "BLINK": "Her eyes are gently closed in a natural blink, eyelids relaxed, same eyebrows, same eyelashes.",
}
def mask_png(box):
    m = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(m); d.ellipse(box, fill=(0, 0, 0, 0))
    b = io.BytesIO(); m.save(b, "PNG"); return b.getvalue()
def multipart(fields, files):
    bd = "----nl" + uuid.uuid4().hex; out = io.BytesIO()
    for k, v in fields.items():
        out.write(f"--{bd}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode())
    for k, (fn, data) in files.items():
        out.write(f"--{bd}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{fn}\"\r\nContent-Type: image/png\r\n\r\n".encode()); out.write(data); out.write(b"\r\n")
    out.write(f"--{bd}--\r\n".encode()); return out.getvalue(), bd
src = io.BytesIO(); base.save(src, "PNG"); SRC = src.getvalue()
def one(name):
    box = EYES if name == "BLINK" else MOUTH
    prompt = "The same woman in the same photo, identical face, lighting, blonde hair, makeup, clothes and background. Only change: " + SHAPES[name] + " Photorealistic, natural."
    body, bd = multipart({"model": MODEL, "prompt": prompt, "size": "1024x1024", "quality": "medium", "n": "1"},
                         {"image": ("base.png", SRC), "mask": ("mask.png", mask_png(box))})
    req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "multipart/form-data; boundary=" + bd})
    t0 = time.time()
    try:
        r = json.load(urllib.request.urlopen(req, timeout=400))
    except urllib.error.HTTPError as e:
        return name, "HTTP %s %s" % (e.code, e.read()[:300].decode("utf-8", "replace"))
    ed = Image.open(io.BytesIO(base64.b64decode(r["data"][0]["b64_json"]))).convert("RGBA").resize((W, H))
    ed.save(f"raw-{name}.png")
    feather = Image.new("L", (W, H), 0); ImageDraw.Draw(feather).ellipse(box, fill=255); feather = feather.filter(ImageFilter.GaussianBlur(14))
    Image.composite(ed, base, feather).save(f"frame-{name}.png")
    return name, {"secs": round(time.time() - t0, 1), "usage": r.get("usage", {}).get("output_tokens")}
with ThreadPoolExecutor(4) as ex:
    for n, res in ex.map(one, list(SHAPES)):
        print(n, json.dumps(res))
