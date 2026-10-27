# -*- coding: utf-8 -*-
"""Nano Banana (Gemini image models via OpenRouter) image-to-image on OUR Blender render: keep geometry, raise realism.
Same route as plan/nano/nano_plan.py; the key path is taken from that script and the key is read inside this process only.
    python nano_edit.py <in.png> <out.png> [--model google/gemini-nano-banana-2.1] [--prompt-file p.txt] [--aspect 3:2]
Appends one line per call to gpt/calls.log with the cost OpenRouter reports in the response usage."""
import base64, io, json, os, re, sys, time, urllib.request, urllib.error
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(H), "nano", "nano_plan.py")
KEYPATH = re.search(r'KEY_FILE = r"([^"]+)"', open(SRC, encoding="utf-8").read()).group(1)
a = sys.argv[1:]; inp, out = a[0], a[1]
MODEL = a[a.index("--model") + 1] if "--model" in a else "google/gemini-nano-banana-2.1"
ASPECT = a[a.index("--aspect") + 1] if "--aspect" in a else "3:2"
PROMPT = open(a[a.index("--prompt-file") + 1] if "--prompt-file" in a else os.path.join(H, "prompt-dollhouse.txt"), encoding="utf-8").read().strip()
im = Image.open(inp).convert("RGB"); im.thumbnail((2048, 2048), Image.LANCZOS)
b = io.BytesIO(); im.save(b, "PNG"); data = base64.b64encode(b.getvalue()).decode()
body = {"model": MODEL, "modalities": ["image", "text"], "image_config": {"aspect_ratio": ASPECT},
        "messages": [{"role": "user", "content": [{"type": "text", "text": PROMPT},
                                                   {"type": "image_url", "image_url": {"url": "data:image/png;base64," + data}}]}]}
with open(KEYPATH, encoding="utf-8") as f:
    k = f.read().strip()
req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode("utf-8"),
                             headers={"Authorization": "Bearer " + k, "Content-Type": "application/json",
                                      "HTTP-Referer": "https://nad-lan.co.il", "X-Title": "nad-lan plan visual"})
del k
t0 = time.time()
try:
    d = json.load(urllib.request.urlopen(req, timeout=400))
except urllib.error.HTTPError as e:
    print("ERROR", e.code, e.read().decode("utf-8", "replace")[:300]); sys.exit(1)
msg = d["choices"][0]["message"]; imgs = msg.get("images") or []
u = d.get("usage") or {}
if not imgs:
    print("no image; text:", (msg.get("content") or "")[:300]); sys.exit(1)
raw = base64.b64decode(imgs[0]["image_url"]["url"].split(",", 1)[1]); open(out, "wb").write(raw)
line = "%s | %s | %s -> %s | %.0fs | cost $%s (OpenRouter usage) | tokens %s" % (time.strftime("%Y-%m-%d %H:%M"), MODEL, os.path.basename(inp), os.path.basename(out), time.time() - t0, u.get("cost"), u.get("total_tokens"))
open(os.path.join(H, "calls.log"), "a", encoding="utf-8").write(line + "\n")
print("saved", out, len(raw), "|", line)
