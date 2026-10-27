# -*- coding: utf-8 -*-
"""gpt-image edit of OUR Blender render: keep the geometry, only raise realism (images/edits, same call as film/gen_photoreal.py).
The key is read inside this process from the path the existing film/gen_photoreal.py uses; it is never printed or written.
    python edit_photoreal.py <in.png> <out.png> [--prompt-file p.txt] [--no-fidelity]
Appends one line per call to gpt/calls.log (time, model, seconds, usage, estimated cost)."""
import base64, io, json, os, re, sys, time, urllib.request, urllib.error, uuid
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\777\nad-lan\nad-lan-co-il\docs\sales\kochav-ph\film\gen_photoreal.py"
KEYPATH = re.search(r'open\(r"([^"]+openai[^"]+)"', open(SRC, encoding="utf-8").read()).group(1)
MODEL = "gpt-image-2.5-sunburst"
inp, out = sys.argv[1], sys.argv[2]
PROMPT = open(sys.argv[sys.argv.index("--prompt-file") + 1], encoding="utf-8").read().strip() if "--prompt-file" in sys.argv else open(os.path.join(H, "prompt-dollhouse.txt"), encoding="utf-8").read().strip()
im = Image.open(inp).convert("RGB"); im = im.resize((1536, 1024), Image.LANCZOS)
buf = io.BytesIO(); im.save(buf, "PNG"); png = buf.getvalue()
b = uuid.uuid4().hex; parts = []
f = lambda k, v: parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (b, k, v)).encode("utf-8"))
f("model", MODEL); f("prompt", PROMPT); f("size", "1536x1024"); f("n", "1"); f("quality", "high")
if "--no-fidelity" not in sys.argv:
    f("input_fidelity", "high")
parts.append(('--%s\r\nContent-Disposition: form-data; name="image[]"; filename="render.png"\r\nContent-Type: image/png\r\n\r\n' % b).encode() + png + b"\r\n")
parts.append(("--%s--\r\n" % b).encode())
key = open(KEYPATH, encoding="utf-8").read().strip()
rq = urllib.request.Request("https://api.openai.com/v1/images/edits", data=b"".join(parts),
                            headers={"Authorization": "Bearer " + key, "Content-Type": "multipart/form-data; boundary=" + b})
del key
t0 = time.time()
try:
    d = json.load(urllib.request.urlopen(rq, timeout=900))
except urllib.error.HTTPError as e:
    msg = e.read().decode("utf-8", "replace")[:400]
    print("ERROR", e.code, msg)
    open(os.path.join(H, "calls.log"), "a", encoding="utf-8").write("%s | %s | ERROR %s | %s\n" % (time.strftime("%Y-%m-%d %H:%M"), MODEL, e.code, msg[:200].replace("\n", " ")))
    sys.exit(1)
img = d["data"][0]; raw = base64.b64decode(img["b64_json"]) if img.get("b64_json") else urllib.request.urlopen(img["url"]).read()
open(out, "wb").write(raw)
u = d.get("usage") or {}
it = (u.get("input_tokens_details") or {}); ot = (u.get("output_tokens_details") or {})
# estimate with the published gpt-image-1 rates (text in $5/M, image in $10/M, image out $40/M); the 2.5 price sheet is not on file
cost = it.get("text_tokens", 0) * 5e-6 + it.get("image_tokens", 0) * 10e-6 + u.get("output_tokens", 0) * 40e-6
line = "%s | %s | %s -> %s | %.0fs | usage %s | est. cost $%.3f" % (time.strftime("%Y-%m-%d %H:%M"), MODEL, os.path.basename(inp), os.path.basename(out), time.time() - t0, json.dumps(u), cost)
open(os.path.join(H, "calls.log"), "a", encoding="utf-8").write(line + "\n")
print("saved", out, len(raw), "|", line)
