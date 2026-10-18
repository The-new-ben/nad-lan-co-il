# -*- coding: utf-8 -*-
"""HAD-543: ask gpt-image for a true 360 equirect of a facility, using OUR approved generated view (<name>.png) as the
reference so the room keeps the same look. python gen_pano.py <name> <size> "<prompt>" -> pano-<name>.png"""
import json, base64, sys, urllib.request, uuid
key = open(r'C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt', encoding='utf-8').read().strip()
name, size, prompt = sys.argv[1], sys.argv[2], sys.argv[3]
model = sys.argv[4] if len(sys.argv) > 4 else "gpt-image-2.5-sunburst"
b = uuid.uuid4().hex
parts = []
def field(k, v):
    parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
field("model", model); field("prompt", prompt); field("size", size); field("n", "1")
parts.append(f'--{b}\r\nContent-Disposition: form-data; name="image[]"; filename="{name}.png"\r\nContent-Type: image/png\r\n\r\n'.encode()
             + open(name + ".png", "rb").read() + b"\r\n")
parts.append(f"--{b}--\r\n".encode())
req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=b"".join(parts),
                             headers={"Authorization": "Bearer " + key, "Content-Type": "multipart/form-data; boundary=" + b})
try:
    d = json.load(urllib.request.urlopen(req, timeout=400))
except urllib.error.HTTPError as e:
    print("ERROR", e.code, e.read().decode()[:400]); sys.exit(1)
img = d["data"][0]
raw = base64.b64decode(img["b64_json"]) if img.get("b64_json") else urllib.request.urlopen(img["url"]).read()
out = f"pano-{name}-{size}.png"
open(out, "wb").write(raw); print("saved", out, len(raw), "usage", d.get("usage"))
