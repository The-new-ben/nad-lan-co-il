import sys, numpy as np, librosa, whisper
sys.stdout.reconfigure(encoding="utf-8")
wm = whisper.load_model("small")
for p in ["take1/greet-he.wav", r"C:\Users\777\Documents\Hadmaya-Visual-Studio\2026-10-28\voice-research\audio\recovered-chatterbox-he-20260903.wav"]:
    y, sr = librosa.load(p, sr=16000); f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr)
    r = wm.transcribe(y.astype(np.float32), language="he", fp16=False)
    print(p[-40:], "| %.1fs f0 %.0f |" % (len(y)/sr, np.nanmedian(f0)), r["text"].strip()[:200])
