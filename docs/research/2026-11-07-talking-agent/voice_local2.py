# Talking agent voice v2 (Ben 7.11.2026): LOCAL Chatterbox Multilingual, guided by a 10 s female reference cut from our own local Kokoro
# af_heart narration (ref-female.wav), so the voice is clearly a woman's. Each sentence is generated alone (no forced early stop) and
# joined with short pauses. Reports length and median pitch per language.
import json, sys, time, re
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np, librosa, torch, torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
LINES = json.load(open("lines.json", encoding="utf-8"))
t0 = time.time(); m = ChatterboxMultilingualTTS.from_pretrained(device="cpu"); print("loaded %.0fs" % (time.time() - t0), flush=True)
m.prepare_conditionals("ref-female.wav", exaggeration=0.5)
out = {}
for lang in sys.argv[1:] or ["he", "en"]:
    parts = [p.strip() for p in re.split(r"(?<=[.?!:])\s+", LINES[lang]) if p.strip()]
    sil = torch.zeros(1, int(m.sr * 0.22)); chunks = []; g0 = time.time()
    for p in parts:
        w = m.generate(p, language_id=lang, exaggeration=0.5, cfg_weight=0.45, temperature=0.7)
        chunks += [w, sil]; print(" ", lang, "%.1fs" % (w.shape[1] / m.sr), p[:40], flush=True)
    wav = torch.cat(chunks[:-1], dim=1); path = "greet-%s.wav" % lang; ta.save(path, wav, m.sr)
    y, sr = librosa.load(path, sr=16000); f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr)
    out[lang] = {"secs": round(len(y) / sr, 2), "gen_secs": round(time.time() - g0), "median_f0": round(float(np.nanmedian(f0)), 1), "parts": len(parts)}
    print(lang, json.dumps(out[lang]), flush=True)
json.dump(out, open("voice-receipt.json", "w"), indent=1)
