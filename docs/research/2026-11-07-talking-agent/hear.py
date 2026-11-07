import sys, json, numpy as np, librosa, whisper
sys.stdout.reconfigure(encoding="utf-8")
wm = whisper.load_model("small")
for lang in ("he", "en"):
    y, sr = librosa.load("greet-%s.wav" % lang, sr=16000)
    r = wm.transcribe(y.astype(np.float32), language=lang, fp16=False)
    print(lang, "|", r["text"].strip())
    for s in r["segments"]: print("   %.1f-%.1f %s" % (s["start"], s["end"], s["text"].strip()))
    # silence map
    iv = librosa.effects.split(y, top_db=35); print("   voiced:", [(round(a/sr,1), round(b/sr,1)) for a, b in iv][:12])
