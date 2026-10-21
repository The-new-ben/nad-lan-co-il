# -*- coding: utf-8 -*-
"""Kochav HaTzafon listing (Ben 21.10.2026: "not amateur, the best in the world"): photoreal ILLUSTRATIONS of the listing's building
made from OUR 3D frames (ref/<name>.png: the city's building outline, 12 floors, the two top floors set back), gpt-image-2.5 edits.
The facade itself is not known from a photo, so every image is labelled as an illustration on the page.
  python gen_bldg.py [name ...] -> out/<name>_<k>.png (2 variants each)"""
import base64, json, os, sys, urllib.request, urllib.error, uuid, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__))
KEY = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip()
SUBJECT = ("The building in the centre of the reference (the one whose top two floors are set back, highlighted in light blue in the reference) is the "
           "subject: a refined new boutique residential building of 12 floors in north Tel Aviv, finished in warm white stone and white plaster with "
           "large windows and slim balconies; its 11th and 12th floors are set back, with wide sun terraces behind frameless glass railings, planters "
           "and outdoor furniture; the 11th-floor terrace is the hero of the image. Keep its exact position, footprint, height and setback shape. ")
KEEP = (" Keep the exact camera angle, layout, street grid, building positions and heights of the reference. Replace every plain massing block with "
        "real Tel Aviv architecture (white and light stone residential blocks with balconies, glass towers where the reference has towers), real "
        "asphalt streets with cars and pedestrians, mature ficus, palm and eucalyptus trees, real lawns. Photoreal, high-end architectural "
        "photography, natural true colours, crisp detail, no text, no labels, no signs, no logos, no watermarks, no blue highlight.")
P = {
 "park_aerial": "A photoreal aerial photograph at golden hour over the Kochav HaTzafon neighbourhood of north Tel Aviv, Yarkon Park's lawns in front, the city's towers on the horizon. ",
 "top_close": "A photoreal drone photograph at dusk, close to the top of the building, warm light inside the apartments, the city towers behind. ",
 "street_low": "A photoreal photograph in soft morning light from a neighbouring balcony across the street, looking at the building. ",
}


def edit(job):
    name, k = job
    out = os.path.join(H, "out", "%s_%d.png" % (name, k))
    if os.path.exists(out): return out, "exists"
    b = uuid.uuid4().hex; parts = []
    f = lambda kk, v: parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (b, kk, v)).encode())
    f("model", "gpt-image-2.5-sunburst"); f("prompt", P[name] + SUBJECT + KEEP); f("size", "1536x1024"); f("n", "1"); f("quality", "high")
    parts.append(('--%s\r\nContent-Disposition: form-data; name="image[]"; filename="%s.png"\r\nContent-Type: image/png\r\n\r\n' % (b, name)).encode() + open(os.path.join(H, "ref", name + ".png"), "rb").read() + b"\r\n")
    parts.append(("--%s--\r\n" % b).encode())
    rq = urllib.request.Request("https://api.openai.com/v1/images/edits", data=b"".join(parts), headers={"Authorization": "Bearer " + KEY, "Content-Type": "multipart/form-data; boundary=" + b})
    try:
        d = json.load(urllib.request.urlopen(rq, timeout=600))
    except urllib.error.HTTPError as e:
        return out, "ERROR %s %s" % (e.code, e.read().decode()[:200])
    img = d["data"][0]; raw = base64.b64decode(img["b64_json"]) if img.get("b64_json") else urllib.request.urlopen(img["url"]).read()
    open(out, "wb").write(raw); return out, "saved %d" % len(raw)


os.makedirs(os.path.join(H, "out"), exist_ok=True)
jobs = [(n, k) for n in (sys.argv[1:] or list(P)) for k in (1, 2)]
with cf.ThreadPoolExecutor(6) as ex:
    for o, r in ex.map(edit, jobs): print(os.path.basename(o), r, flush=True)
