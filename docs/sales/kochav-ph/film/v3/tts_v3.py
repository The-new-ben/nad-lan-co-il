# -*- coding: utf-8 -*-
"""v3 narration: regenerates ONLY the scenes listed in narration_v3.json "changed" (same model, voice and instructions as v2's
tts.py), writes v3/audio/NN-sid.wav + NN-sid-fixed.wav (48 kHz), and durations for all scenes (unchanged scenes = v2's files).
The key is read inside the script and never printed.  python tts_v3.py [--redo]"""
import json, os, subprocess, sys, urllib.request, wave
import imageio_ffmpeg
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "audio"); A2 = os.path.join(H, "..", "audio")
FF = imageio_ffmpeg.get_ffmpeg_exe()
N = json.load(open(os.path.join(H, "narration_v3.json"), encoding="utf-8"))
dur, src = {}, {}
key = None
for i, (sid, text) in enumerate(N["scenes"]):
    if sid in N["changed"]:
        raw = os.path.join(A, "%02d-%s.wav" % (i, sid)); fixed = raw.replace(".wav", "-fixed.wav")
        if "--redo" in sys.argv or not os.path.exists(raw):
            if key is None:
                key = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip()
            body = {"model": N["model"], "voice": N["voice"], "input": N.get("say", {}).get(sid, text), "instructions": N["instructions"], "response_format": "wav"}
            rq = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
            open(raw, "wb").write(urllib.request.urlopen(rq, timeout=180).read())
            if os.path.exists(fixed): os.remove(fixed)
        if not os.path.exists(fixed):  # the API's WAV header carries no length: re-wrap at 48 kHz, as v2's -fixed files
            subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", fixed], check=True)
    else:
        fixed = os.path.join(A2, "%02d-%s-fixed.wav" % (i, sid))
    with wave.open(fixed) as w: dur[sid] = round(w.getnframes() / w.getframerate(), 2)
    src[sid] = os.path.relpath(fixed, H)
    print(sid, dur[sid], src[sid], flush=True)
json.dump({"dur": dur, "src": src}, open(os.path.join(A, "durations_v3.json"), "w"), indent=1)
print("total", round(sum(dur.values()), 1))
