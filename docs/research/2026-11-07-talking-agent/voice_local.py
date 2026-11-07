# Talking agent voice (Ben 7.11.2026: "מדברת עם צ'אטרבוקס"): LOCAL Chatterbox Multilingual (voice-rig venv, cached weights, CPU, no network,
# no paid GPU). Default built-in voice. Writes greet-he.wav + greet-en.wav and reports length and median pitch (female voices sit above ~165 Hz).
import os, sys, time, json
import numpy as np, librosa, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
LINES = {"he": "היי, ברוכים הבאים לנדלן. אני כאן כדי לעזור לכם למצוא את הבית הנכון: מחירים, משכנתא, פרויקטים חדשים, וכל הבדיקות לפני שחותמים. על מה נדבר?",
         "en": "Hi, welcome to NadLan. I'm here to help you find the right home in Israel: prices, mortgages, new projects, and every check before you sign. What shall we talk about?"}
t0 = time.time(); m = ChatterboxMultilingualTTS.from_pretrained(device="cpu"); print("loaded %.0fs" % (time.time() - t0), flush=True)
out = {}
for lang in sys.argv[1:] or ["en", "he"]:
    g0 = time.time(); wav = m.generate(LINES[lang], language_id=lang, exaggeration=0.55, cfg_weight=0.5)
    p = "greet-%s.wav" % lang; ta.save(p, wav, m.sr)
    y, sr = librosa.load(p, sr=16000); f0, vf, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr)
    out[lang] = {"secs": round(len(y) / sr, 2), "gen_secs": round(time.time() - g0), "median_f0": round(float(np.nanmedian(f0)), 1)}
    print(lang, json.dumps(out[lang]), flush=True)
json.dump(out, open("voice-receipt.json", "w"), indent=1)
