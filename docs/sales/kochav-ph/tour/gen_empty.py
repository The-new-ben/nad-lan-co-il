# -*- coding: utf-8 -*-
"""The same 360 rooms with the loose furniture removed (gpt-image-2.5 edit of our own pano): an illustration of the space empty.
python gen_empty.py [room ...] -> pano/<room>-empty.png"""
import base64, json, os, sys, urllib.request, urllib.error, uuid, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__))
KEY = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip()
P = ("This is a 360-degree equirectangular panorama (2:1). Return the SAME panorama, same size, same camera, same projection, with all "
     "loose furniture and objects removed: sofas, armchairs, tables, chairs, stools, rugs, plants, decor, outdoor lounge furniture. Keep "
     "everything built in exactly as it is: walls, floor tiles, ceiling, lights, curtains, windows and doors, the kitchen island and "
     "cabinets, the TV wall cladding, the pergola, the railing, the view. Clean empty floor where the furniture stood, natural light. "
     "The left and right edges must still join seamlessly. No text, no people.")
def gen(room):
    out = os.path.join(H, "pano", room + "-empty.png")
    if os.path.exists(out): return room, "exists"
    b = uuid.uuid4().hex; parts = []
    f = lambda k, v: parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (b, k, v)).encode())
    f("model", "gpt-image-2.5-sunburst"); f("prompt", P); f("size", "2048x1024"); f("n", "1"); f("quality", "high")
    parts.append(('--%s\r\nContent-Disposition: form-data; name="image[]"; filename="%s.png"\r\nContent-Type: image/png\r\n\r\n' % (b, room)).encode() + open(os.path.join(H, "pano", room + ".png"), "rb").read() + b"\r\n")
    parts.append(("--%s--\r\n" % b).encode())
    rq = urllib.request.Request("https://api.openai.com/v1/images/edits", data=b"".join(parts), headers={"Authorization": "Bearer " + KEY, "Content-Type": "multipart/form-data; boundary=" + b})
    try: d = json.load(urllib.request.urlopen(rq, timeout=900))
    except urllib.error.HTTPError as e: return room, "ERROR %s %s" % (e.code, e.read().decode()[:300])
    img = d["data"][0]; raw = base64.b64decode(img["b64_json"]) if img.get("b64_json") else urllib.request.urlopen(img["url"]).read()
    open(out, "wb").write(raw); return room, "saved %d" % len(raw)
with cf.ThreadPoolExecutor(4) as ex:
    for r, m in ex.map(gen, sys.argv[1:] or ["living", "dining", "terrace", "entrance"]): print(r, m, flush=True)
