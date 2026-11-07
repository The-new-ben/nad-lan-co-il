"""Is Ben's track music or a voice? whisper small on the first 30 s and the whole track (local, no download beyond cached weights)."""
import sys, wave, numpy as np, whisper
w = wave.open(sys.argv[1]); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
m = whisper.load_model("small")
r = m.transcribe(a, language=None, task="transcribe", no_speech_threshold=0.5, condition_on_previous_text=False)
print("lang", r.get("language"))
for s in r["segments"]:
    print(f'{s["start"]:6.1f}-{s["end"]:6.1f} nsp={s["no_speech_prob"]:.2f} lp={s["avg_logprob"]:.2f} {s["text"]}')
