# -*- coding: utf-8 -*-
"""The original image of /mortgage-calculator/ (HAD-675, Ben 5.11.2026: "make some image"). gpt-image, 1536x1024, three variants.
An ILLUSTRATIVE editorial photograph: generic people, no readable text, no logos, no brands. Palette from the subject (bank papers,
morning daylight, white walls, the site's sea blue), never cream, beige, brown, gold. python gen_hero.py [a b c] -> img/hero-<x>.png"""
import base64, json, os, sys, urllib.request, urllib.error, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "img")
KEY = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip()
STYLE = (" Editorial documentary photograph for a serious personal-finance publication, full-frame camera, 35mm lens, soft natural morning "
         "daylight from a large window, true neutral colours with cool white walls, light grey stone, pale blue-teal accents, no warm beige or "
         "golden tint, gentle film grain, shallow depth of field, wide 3:2 frame. Paper documents show only blurred, unreadable lines and simple "
         "table grids, never legible words or numbers. No text, no logos, no bank names, no watermarks, no recognisable real people.")
S = {
    "a": "A young Israeli couple in their early thirties at the kitchen island of a bright, newly built apartment in a modern Israeli city, early "
         "morning. She holds a printed mortgage approval in principle with three columns of figures (blurred), he looks at a smartphone showing a "
         "simple payment calculator screen (abstract shapes, no readable digits). Two coffee cups, a set of new apartment keys on the stone counter. "
         "Through the window: white residential towers and rooftops with solar water heaters, a strip of Mediterranean sea far away.",
    "b": "Close, calm overhead-angled shot of a wooden-free light grey kitchen table: hands of two people comparing two printed bank mortgage offers "
         "side by side (blurred tables), a pen, a smartphone with an abstract chart, a ring of new apartment keys with a small blue tag, morning light "
         "from the window casting soft shadows. A glimpse of a balcony railing and city rooftops in the background.",
    "c": "A woman in her thirties sitting on the floor of a sunlit, still empty new apartment with white walls and large windows, a laptop on a "
         "moving box showing an abstract amortization chart, a folder of mortgage papers beside her (blurred), the apartment keys in her hand, looking "
         "out to the city and a distant sea horizon. Optimistic, quiet, real.",
}


def gen(name):
    out = os.path.join(OUT, "hero-%s.png" % name)
    if os.path.exists(out): return name, "exists"
    body = {"model": "gpt-image-2.5-sunburst", "prompt": S[name] + STYLE, "size": "1536x1024", "n": 1, "quality": "high"}
    rq = urllib.request.Request("https://api.openai.com/v1/images/generations", data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    try:
        d = json.load(urllib.request.urlopen(rq, timeout=600))
    except urllib.error.HTTPError as e:
        return name, "ERROR %s %s" % (e.code, e.read().decode()[:200])
    img = d["data"][0]
    raw = base64.b64decode(img["b64_json"]) if img.get("b64_json") else urllib.request.urlopen(img["url"]).read()
    open(out, "wb").write(raw); return name, "saved %d" % len(raw)


os.makedirs(OUT, exist_ok=True)
with cf.ThreadPoolExecutor(3) as ex:
    for n, r in ex.map(gen, sys.argv[1:] or list(S)): print(n, r, flush=True)
