# -*- coding: utf-8 -*-
"""HAD-543 walk: textures from gpt-image. python gen_tex.py name size transparent(0/1) "prompt" -> name.png"""
import json, base64, sys, urllib.request
key = open(r'C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt', encoding='utf-8').read().strip()
name, size, tr, prompt = sys.argv[1], sys.argv[2], sys.argv[3] == "1", sys.argv[4]
body = {"model": "gpt-image-2.5-sunburst", "prompt": prompt, "size": size, "n": 1}
if tr: body["background"] = "transparent"
rq = urllib.request.Request("https://api.openai.com/v1/images/generations", data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
try:
    d = json.load(urllib.request.urlopen(rq, timeout=300))
except urllib.error.HTTPError as e:
    print("ERROR", name, e.code, e.read().decode()[:300]); sys.exit(1)
open(name + ".png", "wb").write(base64.b64decode(d["data"][0]["b64_json"])); print("saved", name)
