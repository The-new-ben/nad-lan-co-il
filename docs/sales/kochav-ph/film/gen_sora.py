# -*- coding: utf-8 -*-
"""Lifestyle clips for the Kochav HaTzafon film (Ben 20.10: "a day in the life... friends grilling on the terrace... international
level"). OpenAI Sora 2 Pro, 1792x1024, 8 s. ILLUSTRATIONS: generic people and places, no brands, no real faces; the film labels them.
  python gen_sora.py [name ...]   -> sora/<name>.mp4 (skips the ones already made)"""
import json, os, sys, time, urllib.request, urllib.error
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "sora")
KEY = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip()
STYLE = (" Shot on a cinema camera, natural Mediterranean light, warm but true colours, shallow depth of field, smooth slow camera move, "
         "photoreal, no text, no logos, no brand names, no watermarks.")
CLIPS = {
 "morning": "Morning in a quiet upscale residential street in north Tel Aviv: a relaxed man in his forties in a white linen shirt steps out of the glass lobby door of a modern white boutique apartment building, sunglasses in hand, ficus and palm trees along the pavement, he smiles and walks on. Camera tracks beside him.",
 "cafe": "A small open-air neighbourhood shopping plaza in north Tel Aviv on a sunny morning: friends in casual summer clothes sit at an outdoor café table under a shade tree, espresso cups and a croissant, easy laughter, a waiter brings coffee, people stroll past low modern shopfronts. Slow dolly in.",
 "deli": "Inside a bright gourmet delicatessen: close shots of a server slicing cured ham, wheels of cheese, olives and fresh bread on the counter, a smiling customer takes a paper bag of groceries. Warm, appetising, slow push in.",
 "park_run": "Early morning in a large green city park beside a calm river in Tel Aviv: joggers and cyclists move along a wide riverside path, eucalyptus and palm trees, dewy lawns, soft golden sunlight, rowers on the river in the distance. Smooth tracking shot alongside a runner.",
 "park_family": "Saturday afternoon on a huge lawn in a Tel Aviv city park: a family with two young children have a picnic on a blanket, the kids run with a kite, friends play frisbee nearby, tall trees and a river glinting behind. Gentle handheld, joyful.",
 "bbq": "Golden hour on a very large modern penthouse sun terrace high above Tel Aviv: a host in his forties grills at a sleek built-in outdoor kitchen, six friends hold wine glasses and laugh around a long wooden table, potted olive trees, a glass railing, the Tel Aviv skyline of towers and the Mediterranean sea glowing in the background. Slow crane move around the table.",
 "night": "Night on the same large penthouse terrace high above Tel Aviv: friends relax on low outdoor lounge sofas under warm string lights, candles on the table, glasses clink, the city's towers and lights sparkle below to the horizon. Slow push in from the railing.",
}


def call(method, path, body=None, raw=False):
    rq = urllib.request.Request("https://api.openai.com/v1" + path, method=method, data=json.dumps(body).encode() if body else None,
                                headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(rq, timeout=300) as r:
        return r.read() if raw else json.loads(r.read())


os.makedirs(OUT, exist_ok=True)
want = [a for a in sys.argv[1:]] or list(CLIPS)
jobs = {}
for name in want:
    if os.path.exists(os.path.join(OUT, name + ".mp4")): continue
    try:
        j = call("POST", "/videos", {"model": "sora-2-pro", "prompt": CLIPS[name] + STYLE, "seconds": "8", "size": "1792x1024"})
        jobs[name] = j["id"]; print("queued", name, j["id"], j.get("status"), flush=True)
    except urllib.error.HTTPError as e:
        print("ERROR", name, e.code, e.read().decode()[:300], flush=True)
while jobs:
    time.sleep(20)
    for name, vid in list(jobs.items()):
        j = call("GET", "/videos/" + vid)
        if j.get("status") == "completed":
            open(os.path.join(OUT, name + ".mp4"), "wb").write(call("GET", "/videos/%s/content" % vid, raw=True)); print("done", name, flush=True); del jobs[name]
        elif j.get("status") in ("failed", "cancelled"):
            print("FAILED", name, json.dumps(j.get("error"))[:300], flush=True); del jobs[name]
print("ALL DONE", flush=True)
