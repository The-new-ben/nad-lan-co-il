# -*- coding: utf-8 -*-
"""Lifestyle stills for the Kochav HaTzafon film (gpt-image-2.5-sunburst, 1536x1024). ILLUSTRATIONS: generic people and places,
no brands, no real faces; the film labels them. python gen_stills.py [name ...] -> stills/<name>.png"""
import base64, json, os, sys, urllib.request, urllib.error, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "stills")
KEY = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip()
STYLE = (" Editorial lifestyle photograph for an international luxury real-estate campaign, shot on a full-frame cinema camera with a 35mm lens, "
         "natural Mediterranean light, true colours, gentle film grain, shallow depth of field, wide 3:2 frame with room to breathe. "
         "No text, no logos, no brand names, no watermarks, no recognisable real people.")
S = {
 "morning": "Morning on a quiet upscale residential street in north Tel Aviv: a relaxed man in his forties in a white linen shirt steps out of the glass lobby door of a modern white boutique apartment building, holding sunglasses, ficus trees and a palm along the pavement, low sun.",
 "cafe": "A small open-air neighbourhood shopping centre in north Tel Aviv on a sunny morning: three friends in summer clothes at an outdoor café table under a shade tree, espresso cups and a croissant, laughter, people strolling past low modern shopfronts with awnings in the background.",
 "deli": "Inside a bright neighbourhood gourmet delicatessen in Tel Aviv: a server in an apron cuts a wheel of aged cheese behind a glass counter of cheeses, smoked salmon, olives and antipasti, fresh bread on wooden shelves, a smiling woman customer waits, warm appetising light.",
 "nuts": "A colourful Israeli nuts-and-dried-fruit shop counter in a neighbourhood shopping centre: neat rows of roasted nuts, seeds, dates and sweets in bins, a hand scooping almonds into a paper bag, warm light.",
 "park_run": "Early morning in Tel Aviv's Yarkon Park: runners and cyclists on a wide riverside path, eucalyptus and palm trees, dewy lawns, rowers on the calm river in the distance, golden low sunlight and long shadows.",
 "park_family": "Saturday afternoon on a huge green lawn in Tel Aviv's Yarkon Park: a family with two young children on a picnic blanket, the kids flying a kite, friends playing frisbee nearby, tall trees and the river glinting behind.",
 "bbq": "Golden hour on a very large modern penthouse sun terrace high above north Tel Aviv: a host in his forties grilling at a sleek built-in outdoor kitchen, six friends with wine glasses laughing around a long wooden table, potted olive trees, a frameless glass railing, the towers of the Tel Aviv skyline and the sea glowing behind.",
 "night": "Night on a large modern penthouse terrace high above Tel Aviv: friends relaxing on low outdoor lounge sofas under warm string lights, candles on the table, glasses raised in a toast, the city's towers and lights sparkling below to the horizon.",
 "sport": "Morning at a large open-air sports park beside a river in Tel Aviv: tennis courts and a padel court in use, a man in his forties serving, palm trees, green park behind, crisp light.",
}


def gen(name):
    out = os.path.join(OUT, name + ".png")
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
names = sys.argv[1:] or list(S)
with cf.ThreadPoolExecutor(5) as ex:
    for n, r in ex.map(gen, names): print(n, r, flush=True)
