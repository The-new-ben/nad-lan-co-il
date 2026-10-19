# -*- coding: utf-8 -*-
"""HAD-543: the English narration of the explainer films, one WAV per scene (gpt-4o-mini-tts, voice cedar).
python tts.py -> audio/<film>-<nn>-<scene>.wav + audio/durations.json"""
import json, os, struct, urllib.request, wave
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "audio"); os.makedirs(A, exist_ok=True)
N = json.load(open(os.path.join(H, "narration.json"), encoding="utf-8"))
key = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip()
dur = {}
for film, scenes in N["films"].items():
    for i, (sid, text) in enumerate(scenes):
        out = os.path.join(A, f"{film}-{i:02d}-{sid}.wav")
        if not os.path.exists(out):
            body = {"model": N["model"], "voice": N["voice"], "input": text, "instructions": N["instructions"], "response_format": "wav"}
            rq = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=json.dumps(body).encode(),
                                        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
            open(out, "wb").write(urllib.request.urlopen(rq, timeout=180).read())
        with wave.open(out) as w:
            dur[f"{film}-{i:02d}-{sid}"] = round(w.getnframes() / w.getframerate(), 2)
        print(film, sid, dur[f"{film}-{i:02d}-{sid}"])
json.dump(dur, open(os.path.join(A, "durations.json"), "w"), indent=1)
