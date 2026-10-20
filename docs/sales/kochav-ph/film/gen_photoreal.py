# -*- coding: utf-8 -*-
"""Photoreal stills that keep the layout of OUR 3D frames (ref/<name>.png, built from the city's maps): gpt-image-2.5 edits.
ILLUSTRATIONS; the bridge is the planned one. python gen_photoreal.py [name ...] -> stills/real_<name>.png"""
import base64, json, os, sys, urllib.request, urllib.error, uuid, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__))
KEY = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip()
KEEP = (" Keep the exact layout, camera angle, street grid, building positions and heights, park shapes and bridge shape of the reference. "
        "Replace the plain white massing with real Tel Aviv architecture: white and light stone residential blocks of 8 to 12 floors with balconies, "
        "glass towers where the reference has towers, real asphalt roads with markings and cars, pavements, mature ficus, palm and eucalyptus trees, "
        "real lawns. Photoreal, editorial architecture photography, true colours, no text, no labels, no signs, no logos, no watermarks.")
P = {
 "aerial": "A photoreal aerial photograph at golden hour of the Kochav HaTzafon neighbourhood in north Tel Aviv: residential blocks around a central park, Yarkon Park's green lawns and the Yarkon river beyond, the Mediterranean on the horizon.",
 "centre": "A photoreal low aerial photograph, late morning, of a small neighbourhood commercial centre in north Tel Aviv: a two-storey row of shops with awnings and café tables in front, people walking, shade trees, residential blocks around.",
 "bridge_day": "A photoreal photograph from the lawn of Yarkon Park, late afternoon, of a new slender white steel pedestrian and cycling bridge with a frameless glass railing curving down from Rokach Boulevard into the park, people walking and cycling on it, families on the lawn below.",
 "bridge_top": "A photoreal aerial photograph, golden hour, of a new slender white pedestrian and cycling bridge crossing a wide city boulevard with traffic and landing in a curve on the lawns of Yarkon Park, cyclists and walkers on the bridge, the Kochav HaTzafon residential blocks on the near side.",
}


def edit(name):
    out = os.path.join(H, "stills", "real_%s.png" % name)
    if os.path.exists(out): return name, "exists"
    b = uuid.uuid4().hex; parts = []
    f = lambda k, v: parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (b, k, v)).encode())
    f("model", "gpt-image-2.5-sunburst"); f("prompt", P[name] + KEEP); f("size", "1536x1024"); f("n", "1"); f("quality", "high")
    parts.append(('--%s\r\nContent-Disposition: form-data; name="image[]"; filename="%s.png"\r\nContent-Type: image/png\r\n\r\n' % (b, name)).encode() + open(os.path.join(H, "ref", name + ".png"), "rb").read() + b"\r\n")
    parts.append(("--%s--\r\n" % b).encode())
    rq = urllib.request.Request("https://api.openai.com/v1/images/edits", data=b"".join(parts), headers={"Authorization": "Bearer " + KEY, "Content-Type": "multipart/form-data; boundary=" + b})
    try:
        d = json.load(urllib.request.urlopen(rq, timeout=600))
    except urllib.error.HTTPError as e:
        return name, "ERROR %s %s" % (e.code, e.read().decode()[:200])
    img = d["data"][0]; raw = base64.b64decode(img["b64_json"]) if img.get("b64_json") else urllib.request.urlopen(img["url"]).read()
    open(out, "wb").write(raw); return name, "saved %d" % len(raw)


with cf.ThreadPoolExecutor(4) as ex:
    for n, r in ex.map(edit, sys.argv[1:] or list(P)): print(n, r, flush=True)
