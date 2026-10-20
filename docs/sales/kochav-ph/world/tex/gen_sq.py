import json, base64, sys, urllib.request
key = open(r'C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt', encoding='utf-8').read().strip()
name, prompt = sys.argv[1], sys.argv[2]
body = {"model": "gpt-image-2.5-sunburst", "prompt": prompt, "size": "1024x1024", "n": 1}
req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
try:
    d = json.load(urllib.request.urlopen(req, timeout=300))
except urllib.error.HTTPError as e:
    print("ERROR", e.code, e.read().decode()[:300]); sys.exit(1)
img = d["data"][0]
raw = base64.b64decode(img["b64_json"]) if img.get("b64_json") else urllib.request.urlopen(img["url"]).read()
open(name + ".png", "wb").write(raw); print("saved", name, len(raw))
