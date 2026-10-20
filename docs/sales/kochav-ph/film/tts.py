# -*- coding: utf-8 -*-
"""Narration WAVs (one per scene) + durations.json. python tts.py [--redo]"""
import json, os, sys, urllib.request, wave
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "audio")
N = json.load(open(os.path.join(H, "narration.json"), encoding="utf-8"))
key = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip()
dur = {}
for i, (sid, text) in enumerate(N["scenes"]):
    out = os.path.join(A, "%02d-%s.wav" % (i, sid))
    if "--redo" in sys.argv or not os.path.exists(out):
        body = {"model": N["model"], "voice": N["voice"], "input": N.get("say", {}).get(sid, text), "instructions": N["instructions"], "response_format": "wav"}
        rq = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        open(out, "wb").write(urllib.request.urlopen(rq, timeout=180).read())
    with wave.open(out) as w: dur[sid] = round(w.getnframes() / w.getframerate(), 2)
    print(sid, dur[sid], flush=True)
json.dump(dur, open(os.path.join(A, "durations.json"), "w"), indent=1)
print("total", round(sum(dur.values()), 1))
